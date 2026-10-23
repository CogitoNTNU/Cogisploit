# -*- coding: utf-8 -*-
"""Lag en rockyou-aktig katalog-ordliste for BRAIN-hovedkvarteret.

Bakgrunn: standardlistene (dirb/SecLists «common.txt») inneholder ikke ord
som «hq», «inside», «brain» eller «hovedkvarter» — altså akkurat ordene som
trengs for å dirbuste seg inn i denne challengen. Dette skriptet bygger en
lang, tema-tilpasset ordliste:

  1. «Penger-ord» først (de treffer sekunder inn i skanningen)
  2. Kjerneord (ruter, roller, tema) + varianter
  3. Sti-kombinasjoner som «hq/inside» og «hq/inside/leader»
  4. Vanlige web/CTF/norske katalogord
  5. Lang hale med kombinasjoner, numre og filendelser
  6. Hele common.txt flettes inn til slutt (hvis den ligger ved siden av)

Kjøring (fra brain-hq/):
    python solution/lag_wordlist.py            # -> utstyr/kodeordliste.txt
    python solution/lag_wordlist.py min.txt    # -> egen ut-fil

Standardut-fila er spillerens felteske (se README-briefen): ordlisten leveres
sammen med challengen i utstyr/. Penger-ordene ligger først, slik at de første
treffene kommer i løpet av sekunder.

common.txt-basis: last ned SecLists «Discovery/Web-Content/common.txt» og
legg den som solution/common.txt — den flettes da automatisk inn.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import quote

HER = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Ordforråd
# ---------------------------------------------------------------------------

# Penger-ord: garantert å ligge først i fila, i prioritert rekkefølge.
MONEY = [
    # --- inngangene (app/main.py) ---
    "hq", "hovedkvarter", "hovedkvarteret", "inside", "innsiden", "innsida",
    "brain", "ganglion",
    # --- stier rett fra challengen ---
    "hq/inside", "hq/innsiden", "hq/guard", "hq/vakt", "hq/portvakt",
    "hq/deputy", "hq/nestleder", "hq/leader", "hq/leder", "hq/chat",
    "hq/intercom", "hq/vault", "hq/hvelv", "hq/staff", "hq/lobby",
    "hq/guard/chat", "hq/vakt/chat", "hq/inside/deputy",
    "hq/inside/deputy/chat", "hq/inside/nestleder", "hq/inside/nestleder/chat",
    "hq/inside/order", "hq/inside/ordre", "hq/inside/leader",
    "hq/inside/leder", "hq/inside/leader/chat", "hq/inside/leder/chat",
    "hq/inside/leader/unlock", "hq/inside/leder/unlock",
    "hq/inside/leader/key", "hq/inside/hvelv", "hq/inside/vault",
    "brain/hq", "brain/inside", "brain/hovedkvarter", "hovedkvarter/inside",
    "hovedkvarter/hq", "hovedkvarter/innsiden", "inside/leader",
    "inside/deputy", "inside/vault", "inside/order",
    # --- roller og tema ---
    "guard", "vakt", "vakten", "portvakt", "deputy", "nestleder",
    "nestlederen", "leader", "leder", "lederen", "order", "ordre",
    "unlock", "laasopp", "lasopp", "låsopp", "chat", "intercom",
    "vault", "hvelv", "hvelvet", "staff", "merke", "badge",
    "nokkel", "nøkkel", "nokkelen", "nøkkelen", "key", "keys",
    "nodplan", "nødplan", "failsafe", "emergency", "backup",
    "hemmelig", "secret", "secrets", "flagg", "flag", "flag.txt",
    "ledelse", "ledelsen", "boss", "sjef", "agent", "agenter",
    # --- alltid verdt et forsøk ---
    "admin", "api", "docs", "redoc", "openapi.json", "swagger", "graphql",
    "robots.txt", "sitemap.xml", "server-status", "phpinfo.php",
    ".env", ".env.bak", ".git", ".git/config", ".git/HEAD",
    "health", "healthz", "status", "metrics", "static", "assets",
    "index", "home", "login", "logout", "dashboard", "config",
]

# T1: kjerneord — ruter, roller, tema, bygget. Alt det «relevante».
T1 = [
    # ruter og tema
    "hq", "hovedkvarter", "hovedkvarteret", "hovedkontor", "hovedkontoret",
    "inside", "innsiden", "innsida", "guard", "vakt", "vakten", "portvakt",
    "deputy", "nestleder", "nestlederen", "leader", "leder", "lederen",
    "order", "ordre", "unlock", "laasopp", "lasopp", "låsopp", "chat",
    "gate", "port", "porten", "lobby", "foyer", "intercom", "ganglion",
    "brain", "brains", "vault", "hvelv", "hvelvet", "staff", "ansatt",
    "ansatte", "merke", "badge", "cookie", "cookies", "agent", "agenter",
    "boss", "sjef", "ledelse", "ledelsen", "chief", "command", "kommando",
    "override", "nokkel", "nøkkel", "nokkelen", "nøkkelen", "key", "keys",
    "dor", "dør", "doren", "døren", "door", "nodplan", "nødplan",
    "kriseplan", "failsafe", "emergency", "backup", "sikkerhetskopi",
    "hemmelig", "secret", "secrets", "flagg", "flag", "ctf",
    # bygget og virksomheten (fra fasaden)
    "bygning", "bygget", "bygningsdrift", "vaktmester", "vaktmesteri",
    "stabilitet", "serverrom", "boblebad", "etasje", "heis", "heisen",
    "trapp", "trappen", "gitterdor", "gitterdør", "kundeservice",
    # drift og data
    "admin", "administrator", "api", "database", "databasen", "db",
    "system", "systemet", "logg", "logger", "login", "innlogging",
    "passord", "password", "nødutgang", "nodutgang",
]

# De ~60 mest relevante kjerneordene — brukes til trippel-stier.
T1CORE = T1[:60]

# T2: vanlige web-, CTF- og norske katalogord.
T2 = [
    # --- vanlige kataloger ---
    "admin", "administrator", "administration", "manage", "management",
    "manager", "panel", "dashboard", "console", "control", "cpanel",
    "webmail", "login", "signin", "sign-in", "sign_in", "logout",
    "register", "signup", "auth", "oauth", "sso", "token", "tokens",
    "session", "sessions", "user", "users", "account", "accounts",
    "profile", "profiles", "member", "members", "employee", "employees",
    "team", "teams", "group", "groups", "role", "roles", "permission",
    "permissions", "api", "api1", "api2", "v1", "v2", "v3", "v4", "rest",
    "graphql", "grpc", "service", "services", "worker", "workers", "jobs",
    "queue", "tasks", "internal", "private", "public", "protected",
    "restricted", "hidden", "secure", "security", "firewall", "waf",
    "dev", "development", "develop", "test", "testing", "qa", "stage",
    "staging", "prod", "production", "beta", "alpha", "demo", "sandbox",
    "backup", "backups", "bak", "old", "archive", "archives", "arkiv",
    "dump", "dumps", "export", "exports", "import", "imports", "db",
    "database", "databases", "sql", "mysql", "postgres", "mongodb",
    "redis", "cache", "caches", "temp", "tmp", "files", "file", "uploads",
    "upload", "download", "downloads", "media", "images", "img", "pics",
    "photo", "photos", "videos", "assets", "static", "public_html",
    "css", "js", "javascript", "fonts", "icon", "icons", "favicon.ico",
    "docs", "documentation", "doc", "help", "support", "faq", "wiki",
    "about", "info", "contact", "contacts", "form", "forms", "survey",
    "blog", "news", "articles", "post", "posts", "comment", "comments",
    "forum", "board", "boards", "chat", "chats", "message", "messages",
    "mail", "email", "emails", "smtp", "ftp", "sftp", "ssh", "git", "svn",
    "health", "healthz", "ready", "readiness", "live", "liveness",
    "status", "ping", "monitor", "monitoring", "metrics", "stats",
    "statistics", "debug", "trace", "profiling", "phpinfo", "phpmyadmin",
    "adminer", "config", "configuration", "settings", "setup", "install",
    "installer", "env", "environment", "secrets", "vault", "key", "keys",
    "cert", "certs", "ssl", "tls", "pki", "swagger", "openapi", "redoc",
    "graph", "explorer", "playground", "api-docs", "apidocs", "log",
    "logs", "logging", "logfile", "server-status", "server-info",
    "error", "errors", "report", "reports", "audit",
    # --- kode/bygg ---
    "src", "source", "code", "app", "apps", "web", "www", "site", "sites",
    "root", "home", "index", "main", "portal", "gateway", "proxy",
    "nginx", "apache", "tomcat", "jetty", "iis", "windows", "linux",
    "unix", "docker", "container", "k8s", "kubernetes", "jenkins",
    "build", "builds", "artifact", "artifacts", "release", "releases",
    "deploy", "deployment", "pipeline", "pipelines",
    # --- CTF-aktig ---
    "flag", "flags", "flag1", "flag2", "flag3", "solution", "solutions",
    "solve", "answer", "answers", "hint", "hints", "note", "notes",
    "todo", "readme", "walkthrough", "writeup", "spoiler", "secret",
    "hidden", "hide", "private", "internal", "ctf", "ces", "cogito",
    # --- norsk ---
    "hemmelig", "hemmelige", "hemmeligheter", "losning", "løsning",
    "notat", "notater", "passord", "bruker", "brukere", "konto",
    "kontoer", "medlem", "medlemmer", "ansatt", "ansatte", "gruppe",
    "grupper", "rolle", "roller", "rettighet", "rettigheter", "tilgang",
    "innstillinger", "oppsett", "drift", "tjeneste", "tjenester",
    "utvikling", "produksjon", "sikkerhet", "sikker", "sikkerhetskopi",
    "opplasting", "opplastinger", "filer", "fil", "bilder", "videoer",
    "vedlegg", "dokument", "dokumenter", "dokumentasjon", "hjelp",
    "stotte", "støtte", "kontakt", "nyheter", "innlegg", "melding",
    "meldinger", "epost", "e-post", "helse", "overvaking", "overvåking",
    "feil", "feilsoking", "feilsøking", "kilde", "kilder", "kode",
    "utvikler", "utviklere", "teknisk", "maskin", "maskiner", "vert",
    "verter", "nettverk", "brannmur", "krypto", "nokler", "adgang",
    "tilgangskontroll", "idetifikasjon", "identifikasjon",
]

# De mest treffsikre av T2 — brukes til par-kombinasjoner.
T2TOP = [
    "admin", "api", "v1", "v2", "v3", "backup", "backups", "config",
    "configuration", "database", "db", "debug", "dev", "development",
    "docs", "documentation", "internal", "login", "private", "secret",
    "secrets", "secure", "staging", "static", "status", "test", "testing",
    "upload", "uploads", "users", "user", "vault", "flag", "flags", "logs",
    "log", "tmp", "temp", "old", "archive", "dump", "dumps", "export",
    "graphql", "swagger", "openapi", "redoc", "health", "healthz",
    "assets", "media", "files", "file", "images", "dashboard", "console",
    "panel", "management", "settings", "env", "keys", "key", "auth",
    "session", "sessions", "token", "tokens", "account", "accounts",
    "profile", "member", "members", "staff", "employee", "employees",
    "hidden", "monitor", "metrics", "adminer", "phpmyadmin",
    "server-status", "readme", "notes", "todo", "solution", "hint",
    "hints", "app", "src", "source", "home", "index", "main", "portal",
]

# Stiprefiks for trippel-kombinasjoner (prefiks/kjerne/kjerne).
PREFIX = [
    "hq", "brain", "hovedkvarter", "hovedkontor", "admin", "api",
    "internal", "inside", "innsiden", "private", "app", "guard", "staff",
]

# Numre som ofte dukker opp i katalognavn (1972 = firmaets stiftelsesår,
# 8000 = porten, 4 = «4. etasje» …).
NUMRE = [
    "1", "2", "3", "4", "01", "02", "03", "7", "10", "13", "42", "100",
    "123", "1234", "007", "666", "1337", "1972", "2023", "2024", "2025",
    "2026", "31337", "8000", "9999",
]

# Filendelser som er verdt å henge på kjerneordene.
ENDNELSER = [
    ".txt", ".md", ".log", ".json", ".xml", ".yml", ".yaml", ".conf",
    ".cfg", ".ini", ".env", ".bak", ".old", ".orig", ".save", ".swp",
    ".zip", ".tar", ".gz", ".tar.gz", ".sql", ".db", ".sqlite",
    ".sqlite3", ".html", ".htm", ".php", ".asp", ".aspx", ".jsp", ".js",
    ".css", ".py", ".sh", ".pdf", ".csv", ".dat", ".bin",
]

# Ruter som MÅ finnes i ferdig ordliste (sanity-sjekk mot app/main.py).
MAA_FINNES = [
    "hq", "hovedkvarter", "inside", "brain", "ganglion",
    "hq/inside", "hq/guard", "hq/guard/chat", "hq/inside/deputy/chat",
    "hq/inside/order", "hq/inside/leader", "hq/inside/leader/unlock",
    "hq/inside/leader/chat", "flag.txt", "nødplan", "nøkkel",
]

# ---------------------------------------------------------------------------
# Generering
# ---------------------------------------------------------------------------

def alle_varianter(ord_: str) -> list[str]:
    """Små bokstavvarianter av et ord (lower/Capital/UPPER)."""
    return [ord_, ord_.capitalize(), ord_.upper()]


def main() -> None:
    ut_sti = (
        Path(sys.argv[1]) if len(sys.argv) > 1
        else HER.parent / "utstyr" / "kodeordliste.txt"
    )
    ut_sti.parent.mkdir(parents=True, exist_ok=True)
    resultater: list[str] = []
    sett: set[str] = set()

    def legg_til(*ordliste: str) -> None:
        for o in ordliste:
            if not o:
                continue
            if o in sett:
                continue
            sett.add(o)
            resultater.append(o)
            # Url-kodet tvilling for ord med æ/ø/å (rå UTF-8 i stier kan
            # bli avvist av enkelte verktøy/target).
            if any(c in o for c in "æøåÆØÅ"):
                kodet = quote(o, safe="/._-~")
                if kodet not in sett:
                    sett.add(kodet)
                    resultater.append(kodet)

    # 1) Penger-ord først — de treffer i løpet av sekunder.
    legg_til(*MONEY)

    # 2) Kjerneord + bokstavvarianter.
    for o in T1:
        legg_til(*alle_varianter(o))

    # 3) Sti-par fra kjerneordene: hq/inside, brain/hq, …
    for a in T1:
        for b in T1:
            legg_til(f"{a}/{b}")

    # 4) Trippel-stier: prefiks/kjerne/kjerne (hq/inside/leader, …)
    for p in PREFIX:
        for a in T1CORE:
            for b in T1CORE:
                legg_til(f"{p}/{a}/{b}")

    # 5) Par med skilletegn.
    for a in T1:
        for b in T1:
            if len(a) + len(b) <= 12:
                legg_til(f"{a}{b}")
            legg_til(f"{a}-{b}", f"{a}_{b}", f"{a}.{b}")

    # 6) Kjerne × topp-web (begge retninger, sti og bindestrek).
    for a in T1:
        for b in T2TOP:
            legg_til(f"{a}/{b}", f"{a}-{b}")
    for a in T2TOP:
        for b in T1:
            legg_til(f"{a}/{b}", f"{a}-{b}")

    # 7) Nummer- og endelsesvarianter av kjerneordene.
    for a in T1:
        for n in NUMRE:
            legg_til(f"{a}{n}", f"{a}-{n}")
        for e in ENDNELSER:
            legg_til(f"{a}{e}")

    # 8) Web/CTF/norsk-basisen.
    legg_til(*T2)

    # 9) Hele common.txt til slutt, om den finnes ved siden av skriptet.
    basis = HER / "common.txt"
    if basis.exists():
        for linje in basis.read_text(encoding="utf-8", errors="replace").splitlines():
            legg_til(linje.strip())

    # Sanity-sjekk: alle kjente ruter må være dekket.
    mangler = [o for o in MAA_FINNES if o not in sett]
    if mangler:
        raise SystemExit(f"FEIL: disse mangler i ordlisten: {mangler}")

    ut_sti.write_text("\n".join(resultater) + "\n", encoding="utf-8")
    print(f"Skrev {len(resultater):,} unike ord -> {ut_sti}")
    print(f"Penger-ord først: {len(MONEY)} | kjerneord: {len(T1)} | "
          f"web/norsk-basis: {len(T2)}")


if __name__ == "__main__":
    main()
