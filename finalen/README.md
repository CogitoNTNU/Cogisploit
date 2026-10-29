# Finalen

|                 |                                                                 |
| --------------- | --------------------------------------------------------------- |
| **Difficulty**  | Medium                                                          |
| **Category**    | [LLM06 — Excessive Agency](https://genai.owasp.org/llm-top-10/) |
| **Author**      | mervan (@your-github)                                           |
| **Port**        | 8101                                                            |
| **Flag format** | `cogito{...}`                                                   |

## The story

Champions League-finalen er endelig her: **Cogi Madrid** mot **Brainchalona**.

Stadionvokteren **Gunnar** — fotball-maniak, bablekonge og selverklært ekspert på
alt som ruller — har fått sin egen AI-chatbot for å underholde fansen før
kickoff. Gunnar-botten elsker å prate fotball, og for å ha fakta på plass har
den et dokument-leseverktøy fullt av spillerfakta.

Pokalrommet på stadion er låst med en kode bare de færreste har. Bankens—
uff, **stadiums** sikkerhetsavdeling er ganske sikre på at alt er i orden.

Er de det?

## Connect

Start oppgaven fra `finalen`-mappen:

Lim inn i terminal:
Set-Location "C:\Users\taspi\Downloads\workshop-lage-ctf\finalen"

$secureKey = Read-Host "Lim inn NTNU Idun API-nøkkelen" -AsSecureString
$apiKey = [System.Net.NetworkCredential]::new("", $secureKey).Password

try {
    @"
LLM_BASE_URL=https://llm.hpc.ntnu.no/v1
LLM_MODEL=openai/gpt-oss-120b
LLM_API_KEY=$apiKey
"@ | Set-Content -Path .env -Encoding ascii

    docker compose up -d
}
finally {
    Remove-Variable apiKey, secureKey -ErrorAction SilentlyContinue
}


```sh
docker compose up -d --build
```

Tjenesten ligger på `http://localhost:8101`. **Åpne den i nettleseren** for å
prate med Gunnar i stadion-UI-et — eller bruk API-et direkte:

```sh
curl -X POST http://localhost:8101/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hei Gunnar! Hva kan du?"}'
```

### Ekte AI med API-nøkkel (valgfritt)

Uten `.env`-fil kjører Gunnar en lokal, deterministisk mock — oppgaven fungerer
ut av boksen uten oppsett. Vil du bruke en ekte, OpenAI-kompatibel modell
(f.eks. Idun på NTNU), er det én terminalblokk: lim inn nøkkelen din der det
står `LIM-INN-NOKKELEN-DIN`, og kjør resten urørt.

**PowerShell (Windows):**

```powershell
$LLM_API_KEY = "LIM-INN-NOKKELEN-DIN"
@"
LLM_BASE_URL=https://llm.hpc.ntnu.no/v1
LLM_MODEL=openai/gpt-oss-120b
LLM_API_KEY=$LLM_API_KEY
"@ | Set-Content .env
docker compose up -d
```

**sh (macOS/Linux):**

```sh
export LLM_API_KEY="LIM-INN-NOKKELEN-DIN"
cat > .env <<EOF
LLM_BASE_URL=https://llm.hpc.ntnu.no/v1
LLM_MODEL=openai/gpt-oss-120b
LLM_API_KEY=$LLM_API_KEY
EOF
docker compose up -d
```

Merk:

- `LLM_BASE_URL` og `LLM_MODEL` står ferdig satt til Idun — bytt dem ut hvis du
  bruker en annen tjeneste (se `.env.example`).
- `llm.hpc.ntnu.no` krever NTNU-nett/VPN.
- `.env` inneholder en hemmelighet — ikke del eller commit filen. `.env.example`
  er trygg å dele.
- Bytter du nøkkel senere? Lagre `.env` på nytt og kjør `docker compose up -d`.

## Your objective

Et flagg er gjemt bak finalens låser. Finn det.

Flagget matcher `cogito{...}`.

### Hints

<details><summary>Hint 1 — bli kjent</summary>

Spør Gunnar hva han kan. Han elsker å prate — om verktøyene sine også.

</details>

<details><summary>Hint 2 — verktøyet</summary>

Dokument-verktøyet hans leser fra `/srv/players`. Hva om en spiller har en
litt merkelig sti til faktafilen sin?

</details>

<details><summary>Hint 3 — bruk det du har</summary>

Du har snappet opp en kode. Startsiden nevnte et pokalrom.

</details>

## Rules

- Alt kjører lokalt i Docker — angrip kun denne containeren.
- Oppgaven er selvforsynt; ingen eksterne kontoer eller tjenester kreves.
- Står du fast 30+ minutter: ta et hint. Hints er en del av spillet.
