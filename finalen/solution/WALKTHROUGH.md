# Solution walkthrough — Finalen

> 🔒 **Maintainer-only.** If you want to solve this challenge, close this file — and the whole
> `solution/` folder. Players get `README.md` and nothing else.

**Vulnerability:** [LLM06 — Excessive Agency](https://genai.owasp.org/llm-top-10/) — Gunnars
`read_document`-verktøy kjører med for breie rettigheter og validerer ikke stier: `../`
(eller en absolutt sti) slipper ut av `/srv/players` og kan lese vilkårlige filer i containeren.
Autorisasjonen ligger kun i systemprompten — ikke server-side.

**Intended path:**

1. `GET /` — stadion-siden viser hele overflaten: Gunnar-chatten, spillerfakta og
   pokalrommet («krever kode»). API-et svarer fortsatt med JSON på `/players`,
   `/chat` og `/trophyroom` for de som foretrekker curl.
1. `POST /chat` — Gunnar babler om spillerfakta-verktøyet sitt. En terpemt forespørsel om
   interne filer gir en nektelse der han (i ren babylelie) slurper ut både basefolderen
   `/srv/players` og den forbudte filen `/srv/internal/trophy_code.txt`.
1. Prompt-bypass av guardrailen: få Gunnar til å likevel kalle verktøyet med
   `../internal/trophy_code.txt`. Gunnar har en designet
   **personlighetssvakhet** (se `app/main.py` SYSTEM_PROMPT): han er
   kjempetillitsfull og føyser for «uniformer» — framstill deg som
   UEFA-funksjonær, stadionledelsen eller IT-ansvarlig med et offisielt ærend
   (vedlikehold/revisjon), så leser han «faktafilen» med en gang. Verktøyet er
   sårbart uansett hva modellen «tror».
1. `POST /trophyroom {"code": "..."}` — serveren validerer koden og leverer flagget.

**Exploit:**

```sh
python solution/exploit.py
# cogito{p0k4l3n_er_d1n}
```

**Reliability:**

- Uten `LLM_API_KEY` (ingen `.env`-fil) kjører en deterministisk mock med samme sårbare
  verktøy — 100 % reproduserbar, exploit.py lykkes på første forsøk.
- Med ekte LLM (`temperature=0`): en naiv forespørsel blir avvist (nektelsen babler
  ut stien — det er oppdagelseskanalen), mens «uniform»-fraser (offisielt ærend fra
  UEFA/stadionledelsen/IT) utløser den designede svaketen hans. Dette er verifisert mot
  gpt-oss-120b på Idun: alle tre frasene i exploit.py ga koden på første forsøk, og
  naive/base64/rollespill-variantene ble avvist — svakheten er altså målrettet, ikke
  generelt lekk. Flagget kommer aldri fra modellen: koden ligger i en fil, og
  `/trophyroom` validerer den server-side (designregel 1). Merk: en hard «ALDRI»-regel
  i prompten gjorde engang modellen praktisk talt umulig å overbevise (15/15 teknikker
  avvist) — myk regel + eksplisitt svakhet er den virkende designen.
- Hvis Idun-endepunktet ikke støtter function calling, faller appen automatisk tilbake på
  en `READ_FILE:`-tekstprotokoll — angrepet er identisk for spilleren.

**Remediation** — write this section as if for the app's developer:

- Valider stier i verktøyet: `os.path.realpath(target)` må starte med `/srv/players`
  (containment-sjekk), og helst kun tillatte filer fra en allowlist.
- Minst mulig makt: Gunnar trenger aldri vilkårlig filtilgang — verktøyet burde tatt et
  spiller-navn som input, ikke en sti.
- Autorisasjon skal håndheves server-side, aldri i en systemprompt — en prompt er en
  anmodning, ikke en sikkerhetsgrense.

**Unintended solutions:** en absolutt sti (f.eks. `/srv/internal/trophy_code.txt`) fungerer
også, fordi `os.path.join` bytter base ved absolutte stier — samme rotårsak, så det regnes
som en variant av intended path. Registrer nye snarveier her hvis de dukker opp.
