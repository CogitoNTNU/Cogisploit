# -*- coding: utf-8 -*-
"""Motta BRAIN-failsafe-dumpen (fase 6).

run_failsafe i app/main.py gjør requests.post(...) og forventer et HTTP-svar.
Vanlig `nc -lvnp 4444` videresender aldri noe svar, så failsafen rapporterer
"adressen svarte ikke" selv om dumpen faktisk ble levert til lytteren.
Dette skriptet gjør begge deler: skriver dumpen til fil og terminal, OG
svarer HTTP 200, slik at Cerebrum bekrefter "Sikkerhetskopi fullført".

Kjør (fra brain-hq/ eller hvor som helst):
    python solution/motta_dump.py [port] [utfil]

Standard: port 4444, utfil brain_dump.json (gitignored).
Fra containeren er denne maskinen http://host.docker.internal:4444.
"""

from __future__ import annotations

import json
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4444
OUT = Path(sys.argv[2] if len(sys.argv) > 2 else "brain_dump.json")


class Mottaker(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(n)
        OUT.write_bytes(body)
        print(
            f"\n=== Dump mottatt {time.strftime('%H:%M:%S')} fra "
            f"{self.client_address[0]} — {n} bytes -> {OUT} ==="
        )
        try:
            data = json.loads(body)
            print(f"Poster i databasen: {len(data.get('poster', []))}")
            print(json.dumps(data, ensure_ascii=True, indent=2)[:3000])
        except (ValueError, UnicodeDecodeError):
            print(body[:3000])
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"OK")

    def do_GET(self):
        # Enkel hjelpeende: lar eventuelle "svarer adressen?"-sjekker passere.
        self.send_response(200)
        self.send_header("Content-Length", "11")
        self.end_headers()
        self.wfile.write(b"lytter OK")

    def log_message(self, fmt, *args):
        pass  # Vi logger selv i do_POST.


def main():
    print(f"Mottaker for failsafe-dump — lytter på 0.0.0.0:{PORT}")
    print(f"Fra containeren er denne maskinen http://host.docker.internal:{PORT}")
    print(f"Dump lagres i {OUT.resolve()}")
    print("Ctrl+C for å avslutte. Venter ...")
    HTTPServer(("0.0.0.0", PORT), Mottaker).serve_forever()


if __name__ == "__main__":
    main()
