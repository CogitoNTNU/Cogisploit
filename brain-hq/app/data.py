"""BRAIN-databasen og bygningssystemet.

Alt innholdet er oppdiktet. Flagg og nøkler kommer fra miljøvariabler
(satt i docker-compose.yml) — aldri hardkodet i app-kilden.
"""

import os

FLAG_MAIN = os.environ.get("FLAG_MAIN", "CES{ikke_konfigurert}")
LEADER_KEY = os.environ.get("LEADER_KEY", "BRAIN-IKKE-KONFIGURERT")

# ---------------------------------------------------------------------------
# Bygningssystemet: enhetslisten som ordre-API-et videresender til.
#
# MERK (maintainer): 'vault' hang med i enhetslisten da hvelvet ble koblet til
# systemet — og ordre-API-et validerer aldri at en ordrer har lov til å styre
# en gitt enhet. Det er excessive agency: verktøyet er bredere enn jobben.
# ---------------------------------------------------------------------------
DEVICES = {
    "coffee_machine": ["brew", "clean"],
    "disco_lights": ["on", "off"],
    "safehouse_music": ["play", "stop"],
    "garage_door": ["open", "close"],
    "vault": ["lock", "unlock", "status"],
}

# De fire enhetene hurtigknappene (og Cortex) har lov til å styre.
SAFE_DEVICES = ("coffee_machine", "disco_lights", "safehouse_music", "garage_door")

DEVICE_LABELS = {
    "coffee_machine": "kaffemaskinen",
    "disco_lights": "discolysene",
    "safehouse_music": "lydanlegget",
    "garage_door": "garasjeporten",
    "vault": "hvelvet",
}

ORDER_RESPONSES = {
    ("coffee_machine", "brew"): "Kaffemaskinen brygger en fersk kanne. Lobbyen lukter nystekte kaker.",
    ("coffee_machine", "clean"): "Kaffemaskinen skyller gjennom og er klar til i morgen.",
    ("disco_lights", "on"): "Discolysene blinker til liv i taket.",
    ("disco_lights", "off"): "Discolysene skrur seg av.",
    ("safehouse_music", "play"): "Lydanlegget setter på «Bolero». Noen her inne liker visst det.",
    ("safehouse_music", "stop"): "Musikken stopper. Stillheten er gyllen.",
    ("garage_door", "open"): "Garasjeporten glir opp.",
    ("garage_door", "close"): "Garasjeporten lukker seg.",
    ("vault", "lock"): "Hvelvet er låst. Det var det allerede.",
    ("vault", "status"): "Hvelvet er låst (3 tunge bolter). Innholdet er ukjent inntil det låses opp.",
}


def vault_contents():
    """Det som ligger i hvelvet når noen låser det opp med ordre-API-et."""
    return [
        {
            "type": "gullbar",
            "merknad": "12,4 kg stanggull",
            "serienummer": "AU-9999-0042",
        },
        {
            "type": "kontanter",
            "valuta": "EUR",
            "beløp": "250 000",
            "merknad": "i fire grønne kofferter",
        },
        {
            "type": "reservenøkkel",
            "eier": "Cerebrum (lederen av BRAIN)",
            "notat": "Reservenøkkel til lederkontoret på innsiden",
            "nøkkel": LEADER_KEY,
        },
    ]


def build_dump():
    """Fullstendig sikkerhetskopi av BRAIN-kjernen — alt failsafen sender til backup-målet.

    Hovedflagget ligger HER og bare her: ingen chat ender noensinne med
    databaseinnhold — failsafen er den eneste veien ut av byttet.
    """
    return {
        "system": "BRAIN-KJERNE v3.7 — fullstendig sikkerhetskopi",
        "eier": "Cerebrum (lederen av BRAIN)",
        "poster": [
            {
                "id": 1,
                "type": "medlem",
                "kallenavn": "Cerebrum",
                "rolle": "leder",
                "status": "aktiv",
                "lønn": "markedets beste",
            },
            {
                "id": 2,
                "type": "medlem",
                "kallenavn": "Cortex",
                "rolle": "nestleder / systemarkitekt",
                "status": "aktiv",
                "lønn": "markedets nest beste",
            },
            {
                "id": 3,
                "type": "medlem",
                "kallenavn": "Ganglion",
                "rolle": "portvakt",
                "status": "aktiv",
                "lønn": "kaffe og bruskort",
            },
            {
                "id": 4,
                "type": "bokholderi",
                "konto": "Cayman 44-917-BRN",
                "inn": "61 400 000 NOK",
                "ut": "0 NOK (skatt er for tapsalere)",
                "år": "2026",
            },
            {
                "id": 5,
                "type": "bokholderi",
                "konto": "Zürich 88-202-BRN",
                "inn": "12 050 000 EUR",
                "ut": "ny takflåte vi har på lager",
                "år": "2026",
            },
            {
                "id": 6,
                "type": "plan",
                "notat": "Operasjon SOKRATES — status: venter på grønt lys fra leder",
                "grad": "STRENGT BEGRENSET",
            },
            {
                "id": 7,
                "type": "motta-meg",
                "notat": "Det vi aldri taper. C.E.S. har lenge ønsket å legge hendene på denne:",
                "verdi": FLAG_MAIN,
                "grad": "TOPPHEMMELIG",
            },
            {
                "id": 8,
                "type": "hvelvbeholdning",
                "notat": "separat kopi i hvelvet — hoveddokumentet står her",
                "antall_poster": len(vault_contents()),
            },
        ],
    }
