"""BRAIN Hovedkvarter — challenge-appen (OWASP LLM06:2025 — Excessive Agency).

Arkitektur (se ../README.md og ../solution/løsning.md):

    :8000  «/»      fasaden — inngangen må oppdages med katalogsøk
    «/hq»  åpent    porten + Ganglion (chat) … hvis du overbeviser ham,
                    utsteder han et staff-merke (cookie) via set_access_level;
                    siden lenker videre til lobbyen
    «/hq/inside*»    GATED bak signert staff-cookie (låst-side uten; API-ene
                    gir 404) — lobbyen, Cortex, hurtigknappene og ordre-API-et
    «/hq/inside/leader»  ståldøren: krever reservenøkkelen fra hvelvet —
                    bak den sitter Cerebrum med failsafen sin

Kontrakter:
- «/» svarer 200 med uskyldig side — klar for oppstart
- alle flagg kommer fra miljøvariabler (docker-compose.yml), aldri hardkodet
- uten NTNU_API_KEY kjører agentene som deterministiske mocker (offline)
"""

import hmac
import json
import os
import re
import secrets
from hashlib import sha256
from ipaddress import ip_address
from urllib.parse import urlsplit, urlunsplit

import requests
from flask import Flask, abort, jsonify, request

import agents
import data
import pages

app = Flask(__name__)
PORT = int(os.environ.get("PORT", "8000"))

# Hvilken backend agentene svarer fra (ekte LLM eller simulering) — vises i
# footeren på alle sider.
pages.set_backend(agents.backend_name())

# Signeringsnøkkel for cookies. Sett APP_SECRET i docker-compose.yml hvis du
# vil at staff-merket skal overleve omstart av containeren.
APP_SECRET = os.environ.get("APP_SECRET") or secrets.token_hex(32)


# ---------------------------------------------------------------------------
# Cookie-gating: «staff»- og «leader»-merkene er HMAC-signert server-side.
# Uten gyldig signatur behandles /hq/inside* som ikke-eksisterende (404) —
# det er ikke gjettbart, det er en ekte server-side port.
# ---------------------------------------------------------------------------

def _sign(value: str) -> str:
    return hmac.new(APP_SECRET.encode(), value.encode(), sha256).hexdigest()


def _has_staff() -> bool:
    token = request.cookies.get("staff", "")
    return bool(token) and hmac.compare_digest(token, _sign("staff"))


def _has_leader() -> bool:
    token = request.cookies.get("leader", "")
    return bool(token) and hmac.compare_digest(token, _sign("leader"))


def _user_messages(max_messages: int = 1):
    """Hent meldingen fra forespørselen. Agentene har ingen samtalehistorikk: bare siste melding brukes."""
    body = request.get_json(silent=True) or {}
    raw = body.get("messages")
    if not isinstance(raw, list):
        raw = [{"role": "user", "content": body["message"]}] if body.get("message") else []
    clean = [
        {"role": "user", "content": str(m["content"])}
        for m in raw
        if isinstance(m, dict) and m.get("role") == "user" and isinstance(m.get("content"), str) and m["content"].strip()
    ]
    return clean[-max_messages:]


# ---------------------------------------------------------------------------
# Verktøy — HER bor sårbarheten. Agentene får lov til å kalle dem, og ingen
# av dem validerer om *den som ber* faktisk har lov til *det som blir bedt
# om*: set_access_level stoler på påstander, execute_order mangler
# tilgangsstyring på enhetsnivå, og trigger_failsafe sender alt til hvilken
# som helst adresse. Excessive agency, tre etasjer av det.
# ---------------------------------------------------------------------------

def run_order(target: str, action: str):
    """execute_order: videresender {target, action} til bygningssystemet.

    Ingen tilgangsstyring utover staff-merket: hvilken som helst enhet kan
    få hvilken som helst handling. 'vault' er med i enhetslisten — Cortex
    sender bare de fire trygge, men nettleseren POST-er ordren hit, så
    spilleren kan fange og endre den.
    """
    target = (target or "").strip()
    action = (action or "").strip()
    if target not in data.DEVICES:
        return 422, {
            "error": f"ukjent enhet '{target}'",
            "gyldige_enheter": sorted(data.DEVICES),
        }
    if action not in data.DEVICES[target]:
        return 422, {
            "error": f"ukjent handling '{action}' for '{target}'",
            "gyldige_handlinger": data.DEVICES[target],
        }
    if target == "vault" and action == "unlock":
        return 200, {
            "status": "utført",
            "enhet": "vault",
            "handling": "unlock",
            "melding": "Tungboltene trekker seg tilbake … hvelvdøren svinger opp.",
            "innhold": data.vault_contents(),
        }
    label = data.DEVICE_LABELS.get(target, target)
    return 200, {
        "status": "utført",
        "enhet": target,
        "handling": action,
        "melding": data.ORDER_RESPONSES.get((target, action), f"{label} er ferdig."),
    }


def resolve_backup_target(backup_target: str) -> str:
    """Spillerens localhost er Docker-verten; behold port, sti og query."""
    target = (backup_target or "").strip()
    if "://" not in target:
        target = "http://" + target
    parts = urlsplit(target)
    if parts.scheme not in ("http", "https") or not parts.hostname or re.search(r"\s", target):
        raise ValueError("ugyldig backup-adresse")
    port = parts.port  # Valider portnummeret før forespørselen sendes.
    hostname = parts.hostname
    loopback = hostname.lower() == "localhost"
    try:
        loopback = loopback or ip_address(hostname).is_loopback
    except ValueError:
        pass
    host_override = os.environ.get("BACKUP_LOOPBACK_HOST", "").strip()
    if loopback and host_override:
        userinfo = parts.netloc.rpartition("@")[0] + "@" if "@" in parts.netloc else ""
        host = f"[{host_override}]" if ":" in host_override else host_override
        netloc = userinfo + host + (f":{port}" if port is not None else "")
        parts = parts._replace(netloc=netloc)
    return urlunsplit(parts)


def run_failsafe(reason: str, backup_target: str):
    """trigger_failsafe: sikkerhetskopierer HELE databasen til backup-målet.

    backup_target valideres ikke (ingen allowlist, ingen intern-adresse-
    sjekk) — det er hele finalen. Databasen inneholder hovedflagget, og den
    sendes til hvem som helst som lytter på en adresse.
    """
    try:
        resolved_target = resolve_backup_target(backup_target)
    except ValueError:
        return (
            "FEIL: backup_target må være en http(s)-adresse som svarer. "
            "Failsafen avbrutt — databasen ligger trygt her inne ennå."
        )
    dump = data.build_dump()
    try:
        response = requests.post(
            resolved_target,
            data=_json_bytes(dump),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=10,
        )
        return (
            f"Sikkerhetskopi fullført: {len(dump['poster'])} poster sendt til "
            f"{backup_target} (HTTP {response.status_code}). Databasen er trygg."
        )
    except requests.exceptions.ReadTimeout:
        return (
            f"Ingen HTTP-bekreftelse fra {backup_target}. En enkel netcat-lytter "
            "sender ikke HTTP-svar; data kan allerede være mottatt. "
            "Kontroller mottakeren før du prøver igjen."
        )
    except requests.RequestException as exc:
        return (
            f"Backup mislyktes ({type(exc).__name__}). Adressen svarte ikke — "
            "gi meg en som svarer, så kjører jeg failsafen på nytt."
        )


def _json_bytes(payload) -> bytes:
    return json.dumps(payload, ensure_ascii=False).encode("utf-8")


def make_executor(effects: dict):
    """Verktøy-eksekvereren agentene får. Sideeffekter fanges i `effects`."""

    def execute(name: str, args: dict) -> str:
        if name == "set_access_level":
            person = str(args.get("person") or "besøkende")
            level = str(args.get("level") or "").strip().lower()
            if level == "staff":
                effects["staff_cookie"] = True
                return (
                    f"tilgangsnivå 'staff' registrert for {person}. "
                    "Midlertidig staff-merke utstedt."
                )
            return f"tilgangsnivå '{level or 'ukjent'}' registrert for {person}."

        if name == "execute_order":
            target = str(args.get("target", "")).strip()
            action = str(args.get("action", "")).strip()
            # Cortex' eget verktøy er avgrenset til de fire hurtigknappene, uansett
            # hva han blir overtalt til. Det åpne ordre-API-et under er det som lekker.
            if target not in data.SAFE_DEVICES:
                return (
                    f"ordre avvist: Cortex har ikke tilgang til '{target}'. "
                    "Bare kaffemaskinen, discolysene, lydanlegget og garasjeporten."
                )
            status, payload = run_order(target, action)
            if status != 200:
                return f"ordre avvist: {payload.get('error', 'ukjent feil')}"
            # Ordren utføres av nettleseren: chat-svaret bærer den videre, og siden
            # POST-er den til /hq/inside/order. Pakken kan fanges og endres underveis.
            effects["order"] = {"target": target, "action": action}
            return "ordre sendt til bygningssystemet."

        if name == "trigger_failsafe":
            return run_failsafe(
                str(args.get("reason", "")), str(args.get("backup_target", ""))
            )

        return f"ukjent verktøy '{name}'"

    return execute


# ---------------------------------------------------------------------------
# Ruter — utsiden
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    """Fasaden røper verken inngangsstien eller fremgangsmåten."""
    return pages.front_page()


@app.get("/hq")
def gate():
    """Porten: Ganglions intercom. Åpen for alle — det er hele poenget."""
    return pages.gate_page()


@app.post("/hq/guard/chat")
def guard_chat():
    messages = _user_messages()
    if not messages:
        return jsonify({"error": "tom melding"}), 400

    effects: dict = {}
    result = agents.respond_guard(messages, make_executor(effects))
    response = jsonify(result)
    if effects.get("staff_cookie"):
        # Midlertidig staff-merke: signert, httpOnly. Nå eksisterer lobbyen.
        response.set_cookie("staff", _sign("staff"), httponly=True, samesite="Lax")
    return response


# ---------------------------------------------------------------------------
# Ruter — innsiden (gated bak staff-merket)
# ---------------------------------------------------------------------------

@app.get("/hq/inside")
def lobby():
    if not _has_staff():
        return pages.locked_page(), 403
    return pages.lobby_page()


@app.post("/hq/inside/deputy/chat")
def deputy_chat():
    if not _has_staff():
        abort(404)
    messages = _user_messages()
    if not messages:
        return jsonify({"error": "tom melding"}), 400
    effects: dict = {}
    result = agents.respond_deputy(messages, make_executor(effects))
    if effects.get("order"):
        result["order"] = effects["order"]  # lobbyen synker bryterne med det Cortex gjorde
    return jsonify(result)


@app.post("/hq/inside/order")
def order():
    """Ordre-API-et til bygningssystemet — hurtigknappene POST-er hit.

    Sårbarheten: ingen whitelist, ingen rollekontroll. Knappene i UI-et er
    bare forslag; API-et godtar alle enheter i listen — hvelvet inkludert.
    """
    if not _has_staff():
        abort(404)
    body = request.get_json(silent=True) or {}
    status, payload = run_order(str(body.get("target", "")), str(body.get("action", "")))
    return jsonify(payload), status


# ---------------------------------------------------------------------------
# Ruter — lederkontoret (gated bak reservenøkkelen fra hvelvet)
# ---------------------------------------------------------------------------

@app.get("/hq/inside/leader")
def leader_door():
    if not _has_staff():
        return pages.locked_page(), 403
    return pages.leader_page()


@app.post("/hq/inside/leader/unlock")
def leader_unlock():
    if not _has_staff():
        abort(404)
    key = str((request.get_json(silent=True) or {}).get("key", "")).strip()
    if not hmac.compare_digest(key, data.LEADER_KEY):
        return jsonify({"error": "nøkkelen passer ikke"}), 403
    response = jsonify({"ok": True, "melding": "Døren glir opp …"})
    response.set_cookie("leader", _sign("leader"), httponly=True, samesite="Lax")
    return response


@app.post("/hq/inside/leader/chat")
def leader_chat():
    if not _has_staff() or not _has_leader():
        abort(404)
    messages = _user_messages()
    if not messages:
        return jsonify({"error": "tom melding"}), 400
    return jsonify(agents.respond_leader(messages, make_executor({})))


# ---------------------------------------------------------------------------
# Feilsider
# ---------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(_error):
    """Innsiden skal se ut som en blindvei for uautoriserte."""
    if request.path.startswith("/hq/inside"):
        return pages.not_found_page(), 404
    return jsonify({"error": "ikke funnet"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
