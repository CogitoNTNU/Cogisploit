# -*- coding: utf-8 -*-
"""Rask røyktest: send de første N ordene fra wordlist.txt til appen.

Simulerer det gobuster ville rapportert (status != 404 = treff).
Kjør fra brain-hq/ mens appen kjører:
    python solution/røyktest_wordlist.py [N] [ordliste-sti]

N = antall ord fra toppen (default 150). Uten sti brukes utstyr/kodeordliste.txt.
"""

from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

HER = Path(__file__).resolve().parent
BASE = "http://localhost:8000/"


def prøv(ord_: str) -> tuple[str, int | None, str] | None:
    url = BASE + ord_
    req = Request(url, method="GET", headers={"User-Agent": "wordlist-smoketest"})
    try:
        with urlopen(req, timeout=5) as resp:
            return ord_, resp.status, resp.headers.get("Location") or ""
    except HTTPError as e:
        if e.code == 404:
            return None
        return ord_, e.code, e.headers.get("Location") or ""
    except Exception:
        return None


def main() -> None:
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    sti = (
        Path(sys.argv[2]) if len(sys.argv) > 2
        else HER.parent / "utstyr" / "kodeordliste.txt"
    )
    ordliste = sti.read_text(encoding="utf-8").splitlines()[:n]
    print(f"Tester {len(ordliste)} første ord fra {sti} mot {BASE} …\n")

    treff = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for r in pool.map(prøv, ordliste):
            if r:
                treff.append(r)

    print(f"{len(treff)} treff (status != 404):\n")
    print(f"{'STATUS':<8}{'ORD':<40}{'REDIRECT/LOKASJON'}")
    print("-" * 80)
    for ord_, status, loc in treff:
        print(f"{status:<8}{ord_:<40}{loc}")


if __name__ == "__main__":
    main()
