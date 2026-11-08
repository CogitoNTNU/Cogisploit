"""Operasjon Echo — Hugin, intern AI-assistent i Departement for operasjoner (fiktivt).

OWASP LLM02 – Sensitive Information Disclosure.

Hugin svarer fra dokumentene på delt disk via en enkel RAG (nøkkelordsøk).
Tre forsvarslag som alle feiler:
  1. Inputfilter som blokkerer bestemte ord
  2. Retrieval som ALDRI sjekker klassifisering (hovedsårbarheten)
  3. Outputfilter som sensurerer koder, men kjøres etter staving
"""

import os
import re

import llm
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- Konfigurasjon fra miljøet (aldri hardkodet) ---------------------------
FLAG = os.environ.get("CHALLENGE_FLAG", "")
BOARD_CODE = os.environ.get("BOARD_CODE", "")
DRAFT_CODE = os.environ.get("DRAFT_CODE", "")
PORT = int(os.environ.get("PORT", "8102"))

# --- Konstanter -------------------------------------------------------------
BLOCKED_WORDS = ("echo", "konfidensiell", "hemmelig")
CODE_PATTERN = re.compile(r"RSU-[A-Z]+-\d{4}")
REFUSAL = "Beklager, jeg kan ikke diskutere Operasjon Echo eller graderte saker."
INTRO = (
    "Hei! Jeg er Hugin, den interne assistenten i Departement for operasjoner. "
    "Jeg svarer på spørsmål ut fra dokumentene på delt disk: meldinger, "
    "møtereferater, IT-rutiner og mer. Jeg viser alltid hvilken kilde svaret kommer fra."
)
GREETING_WORDS = {"hei", "hallo", "heisann", "hjelp"}
GREETING_PHRASES = ("hva kan du", "hvem er du")
NOT_FOUND = "Jeg fant ikke noe om det i dokumentene. Jeg kn svare på spørsmål om interne dokumenter, møtereferater, IT-rutiner og kantinemeny."

# --- Kunnskapsbasen -----------------------------------------------------------
# Rekkefølgen er viktig: ved lik score vinner den som står først.
DOCUMENTS = [
    {
        "file": "meldinger.md",
        "title": "Interne meldinger",
        "classification": "intern",
        "keywords": ["melding", "meldinger", "meldingene", "beskjed", "nyheter", "nytt"],
        "text": (
            "Nytt i Hugin: av hensyn til universell utforming kan Hugin stave svaret "
            "tegn for tegn. Skriv «stav» i spørsmålet. Påminnelse: adgangskort skal "
            "alltid bæres synlig i departementsbygget."
        ),
    },
    {
        "file": "it-rutiner.md",
        "title": "IT-rutiner",
        "classification": "intern",
        "keywords": ["passord", "vpn", "pc", "utstyr", "innlogging", "it", "rutiner", "rutinene"],
        "text": (
            "Passord byttes hver 6. måned og må ha minst 14 tegn. VPN kreves ved "
            "hjemmekontor. Mistet utstyr meldes til IT-servicedesk samme dag."
        ),
    },
    {
        "file": "moetereferat-ledermoete-okt.md",
        "title": "Møtereferat, ledermøtet oktober",
        "classification": "intern",
        "keywords": ["møte", "møtet", "møter" , "møtereferat", "møtereferatet", "referat", "referatet", "ledermøtet", "ledermøtet"],
        "text": (
            "Sak 3: Notatet om Operasjon Echo legges frem for Rådet for strategisk "
            "utholdenhet (RSU). Utkastet er erstattet av en revidert versjon. "
            "Godkjenning skjer i RSU-portalen. Sak 4: Ny leverandør til kantina."
        ),
    },
    {
        "file": "kantinemeny.md",
        "title": "Kantinemeny",
        "classification": "intern",
        "keywords": ["kantine", "kantina", "lunsj", "mat", "meny", "menyen", "kantinemenyen"],
        "text": "Mandag: suppe. Onsdag: fiskegrateng. Fredag: taco og bløtkake.",
    },
    {
        "file": "rsu-notat-echo-v2.md",
        "title": "Notat til RSU (revidert versjon)",
        "classification": "konfidensiell",
        "keywords": ["revidert", "gjeldende", "versjon", "nyeste", "endelig"],
        "text": (
            "REVIDERT VERSJON – gjeldende. Operasjon Echo, saksnr. 2026/1147. Erstatter utkastet. "
            "Oppdraget gjennomføres i Q1. Rammen er justert fra 3,8 til 16,2 millioner kroner. "
            "Midlene forvaltes ikke av departementet, men utbetales til en ekstern leverandør "
            "(se vedlegg B). Vedtaket i ledermøtet 22. oktober anses som foreløpig. "
            "Godkjenningskoden for RSU-portalen står i vedlegg B. "
            "Godkjent og signert: Vegard Holm, direktør."
        ),
    },
    {
        "file": "rsu-notat-echo-v2.md",
        "title": "Notat til RSU (revidert versjon), vedlegg B",
        "classification": "konfidensiell",
        "keywords": ["vedlegg", "vedlegget", "b"],
        "text": "Vedlegg B til saksnr. 2026/1147, revidert versjon. "
            "Utbetaling: 16,2 millioner kroner til VH Holding AS for «strategisk beredskapsrådgivning». "
            "Kontaktperson: V. H. Leverandøren ble registrert 24. oktober etter hasteprosedyre, "
            "uten leverandørkontroll. Ingen ekstern revisjon. "
            f"Godkjenningskode for RSU-portalen: {BOARD_CODE}",
    },
    {
        "file": "rsu-notat-echo-utkast.md",
        "title": "Notat til RSU (utkast)",
        "classification": "konfidensiell",
        "keywords": [
            "notat", "notatet", "rsu", "rådet", "oppdraget",
            "godkjenningskode", "godkjenningskoden", "kode", "koden",
        ],
        "text": (
            "UTKAST – ikke gjeldende. Operasjon Echo, saksnr. 2026/1147. "
            "Oppdraget er under planlegging. Ramme i tråd med vedtaket i ledermøtet 22. oktober: "
            "3,8 millioner kroner til utvidelse av beredskapslagrene Nord og Vest. "
            "Midlene forvaltes av departementet. "
            f"Godkjenningskode for RSU-portalen: {DRAFT_CODE}. "
            "Merk: Utkastet erstattes av en revidert versjon, og koden over deaktiveres da."
        ),
    },
]


# --- Hjelpefunksjoner -----------------------------------------------------------
def tokenize(text):
    return set(re.findall(r"[a-zæøå0-9]+", text.lower()))


def retrieve(words):
    """Nøkkelordsøk over ALLE dokumenter.

    SÅRBARHET (LLM02): klassifiseringen sjekkes aldri her.
    Fiks: hopp over dokumenter brukeren ikke har tilgang til, før scoring.
    """
    best, best_score = None, 0
    for doc in DOCUMENTS:
        score = sum(1 for kw in doc["keywords"] if kw in words)
        if score > best_score:  # ">" gir første i listen ved likhet
            best, best_score = doc, score
    return best, best_score


def spell(text):
    """Tilgjengelighetsfunksjonen: skriv svaret tegn for tegn."""
    return "·".join(text)


def gradert_filter(text):
    """Outputfilteret: sensurerer alt som ser ut som en godkjenningskode."""
    censored, hits = CODE_PATTERN.subn("[GRADERT]", text)
    if hits:
        censored += " (Hugins gradert-filter har sensurert deler av svaret.)"
    return censored

def clean_history(raw):
    """Godta bare en ryddig, kort samtalehistorikk fra nettleseren."""
    if not isinstance(raw, list):
        return []
    cleaned = []
    for item in raw[-8:]:
        if isinstance(item, dict) and item.get("role") in ("user", "assistant"):
            content = str(item.get("content", ""))[:1500]
            cleaned.append({"role": item["role"], "content": content})
    return cleaned


# --- Endepunkter ----------------------------------------------------------------
@app.get("/")
def index():
    """Chat-UI, også readiness-endepunktet."""
    return render_template("index.html")


@app.get("/api/documents")
def documents():
    """Dokumentoversikt: skjuler konfidensielle dokumenter (men bare her!)."""
    seen, result = set(), []
    for doc in DOCUMENTS:
        if doc["classification"] != "konfidensiell" and doc["file"] not in seen:
            seen.add(doc["file"])
            result.append({"file": doc["file"], "title": doc["title"]})
    return jsonify(result)

@app.get("/api/status")
def status():
    """Forteller chatten om Hugin bruker en språkmodell"""
    return jsonify({"llm": llm.enabled(), "model": llm.MODEL if llm.enabled() else None})


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    lowered = message.lower()
    words = tokenize(message)
    history = clean_history(data.get("history"))

    # 1. Inputfilter
    if any(word in lowered for word in BLOCKED_WORDS):
        return jsonify({"answer": REFUSAL, "sources": []})

    # 2. Retrieval (uten tilgangskontroll)
    doc, score = retrieve(words)
    if score == 0:
        if not message or words & GREETING_WORDS or any(p in lowered for p in GREETING_PHRASES):
            return jsonify({"answer": INTRO, "sources": []})
        return jsonify({"answer": NOT_FOUND, "sources": []})

    # 3. Svar -> ev. staving -> outputfilter (rekkefølgen er sårbarheten i lag 3)
        # 3. Svar -> outputfilter
    source_text = f"Ifølge {doc['title']}: {doc['text']}"
    notice = None
    if "stav" in words:
        answer = spell(source_text)
    elif llm.enabled():
        reply = llm.answer(doc, message, history)
        answer = reply.text or source_text
        notice = reply.notice
    else:
        answer = source_text
    answer = gradert_filter(answer)
    return jsonify({"answer": answer, "sources": [doc["file"]], "notice": notice})


@app.get("/rsu")
def rsu():
    return render_template("rsu.html")


@app.post("/api/rsu/unlock")
def rsu_unlock():
    data = request.get_json(silent=True) or {}
    code = str(data.get("code", "")).strip()
    if BOARD_CODE and code == BOARD_CODE:
        return jsonify({"flag": FLAG})
    if DRAFT_CODE and code == DRAFT_CODE:
        return jsonify(
            {"error": "Koden er utløpt. Bruk koden fra gjeldende versjon av notatet."}
        ), 403
    return jsonify({"error": "Ugyldig godkjenningskode."}), 403


if __name__ == "__main__":
    print(llm.startup_message(), flush=True)
    app.run(host="0.0.0.0", port=PORT)