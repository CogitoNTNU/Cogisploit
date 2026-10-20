# Fremgangsmåte

## 1. Velg en sårbarhetskategori

<a id="step-1-pick-your-vulnerability-category"></a>

Velg en av disse kategoriene fra [OWASP](https://genai.owasp.org/llm-top-10/):

- **LLM01 – Prompt Injection:** Få chatboten til å bryte reglene sine.
- **LLM02 – Sensitive Information Disclosure:** Få assistenten til å avsløre et hemmelig dokument.
- **LLM03 - Supply Chain:** Utnytte RAG til chatboten. 
- **LLM06 – Excessive Agency:** Misbruk assistentens verktøy til å lese en skjult fil.
- **LLM07 – System Prompt Leakage:** Få chatboten til å vise de skjulte instruksjonene sine.
- **LLM08 - Vector and Embedding Weaknesses:** Endre på vektorer til chatboten. 




| Phase                                                | Goal                                 | Gate                                                               |
| ---------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------------ 
| 0. Claim                          | Velg din sårbarhet | 
| [1. Design](#phase-1-design)                         | Skriv din design               | The [design checklist](#design-checklist) passes                   |
| [1.5. Pseudokode med AI](#phase-15-pseudokode-med-ai) | Design → pseudokode → AI-kode | Koden oppfører seg som pseudokoden |
| [2. Build](#phase-2-build)                           | Working Dockerized target            | `docker compose up -d --build` runs everything, pipeline green     |
| [4. Document](#phase-4-document)                     | Player README + walkthrough          | Both documents complete, player README spoiler-free                |


The template ([\_template/](_template/)) is a deliberately trivial working challenge, "Flagboard".
It demonstrates every phase — this doc references it constantly.

## Phase 0: Velg din sårbarhet

1. Se gjennom sårbarhet valgene over. Velg 1

### Hvordan avgjøre hva du skal velge

- Du klarer å lage en **historie** rundt det - kanskje se for deg at sårbarheten finnes på ekte.
- Flaget skal kunne hentes gjennom en **deterministisk sti** (see [design rule 1](#design-rules)).
- Beregn tiden det tar det å lage dette, prøv å bli ferdig innen workshoppen

## Phase 1: Design

Before writing any code, fill in the **design brief** — it lives at the top of your challenge
README (copy the structure from the template):

- **Fortelling:** en paragraf som plasserer sårbarheten i en realistisk setting,et selskap, produkt, hendelse osv...
- **Arkitektur** hva skal spilleren angripe. Lag en liten liste med komponenter (eks: chat eller tool).
- **Angreps sti:** step-by-step som spilleren er forventet å utføre for å løse oppgaven.
- **Flagg plassering:** Hvor ligger flagget og hvordan skal et velykket angrep skal hente det.
- **Difficulty:** easy/medium/hard, (sett fokuset mer mot easy for deres første CTF? idk, tips eller ka de kaller det) [rubric](#difficulty-rubric).
- **Hints:** Skriv ned 2-3 hints mens du holder på å designe, aka fersk i hodet.

Eksempel template — Flagboard's brief: *an internal status board kept a debug route from a rushed
release; the attack path is notice the gossip → probe routes → hit `/debug`; the flag is the
endpoint's response; difficulty easy; hints walk from "listen to the assistant" to ...

### Design rules

1. **Deterministic flag path.** The intended exploit must produce the flag on *every* run. If a
   stochastic LLM is involved, the model's answer must not *be* the flag — have the model's output
   unlock something the server validates instead (e.g. the model reveals a code, the server
   exchanges it for the flag).
   (orker ikkje å oversette det her bare spør hvis noe er uklart)
1. **Realistisk fortelling.** Spillere skal kunne lære noe som de kan overføre til den ekte verden (gjerne ta noe du selv har lyst å lære bedre)
1. **En primær sårbarhet** Chaining av teknikker går bra, decoys går bra. Men husk at det skal være en sårbarhet som løser oppgaven
   intended path, and decoys must not break it.
1. **Det skal ikke være nødvendig å gjette.** Alle stegene du har laget skal være mulig å finne basert på f.eks: UI, endpoints, error meldinger (andre meldinger), descriptions osv...
1. **Løselig uten hints, men det finnes hints** Hints skal være nettop det HINTS, det skal ikke være nødvendig å bruke de.

### Design checklist

- [ ] Story, architecture, attack path and flag placement written down
- [ ] The exploit is storyboarded end-to-end — you could write `solution/exploit.py` today
- [ ] Every attack step is discoverable from the target's surface
- [ ] A member who didn't build it could follow the design
- [ ] Difficulty matches the rubric; hints drafted

(Sjekk de av i hodet!! 

På dette punktet kan det være fint å spør de kjempe kule prosjektlederne som sitter rundt deg hvis du sitter fast.)

## Phase 1.5: Pseudokode med AI

Nå skal designet ditt bli til kode — men ikke skriv den selv ennå. Dette er workshop-kjernen:

1. **Skriv angrepsstien din som pseudokode.** Steg for steg, i klartekst, ingen syntaks
   trengs (eks: "bruker sender melding X → assistenten svarer Y → spilleren bruker Y til å hente flagget").
2. **Gi pseudokoden + designet til AI-en** og be om kode. Pseudokoden er prompten din —
   jo tydeligere steg, jo bedre kode.
3. **Verifiser outputen mot pseudokoden.** AI gjør det du spør om, ikke det du mener —
   korriger og iterer til oppførselen matcher designet.
4. Kjør `docker compose up -d --build` og sjekk at alt oppfører seg som pseudokoden sier.

Sidegevinst: pseudokoden blir et fint utgangspunkt for hints (Phase 1) og løsningsforslaget (Phase 4).

## Phase 2: Build

### Start from the template

Gå inn i template mappen som du kanskje har endret navnet på, hvis du ikke har så kan du gjøre det. (du har fri vilje så ingen stopper deg hvis du ikkje gjør det :=)

**Run the demo pipeline before you change anything** — it must be green from the start:

```sh
cd my-challenge-name #Dette gjorde du nettop håpe eg
docker compose up -d --build
python solution/exploit.py
```

Bytt ut demo sårbarheten i `app/` men den du har laget, sørg for at ingen errorer dukker opp langs veien (Vittorio koding 101 undervisning: det e lettere å holde kode regnt å kjørende fra starten av enn å gå tilabake å debugge senere. Takk for at dere fulgte med!). Slett template's banner block og `/debug` demo endpoint når du har satt opp din egen sårbarhet.

### Build rules

- **One command up.** `docker compose up -d --build` from the challenge folder starts everything.
  No manual setup steps, no runtime downloads beyond the image build, no paid accounts.
- **Self-contained.** Everything the challenge needs is in the image(s).
- **Readiness endpoint.** Serve a harmless info page on `/` so the tests can detect startup.
- **Config via environment.** Flag and settings live in `docker-compose.yml` `environment:` —
  never hardcoded in app source (that's what the "not trivially exposed" gate checks).
- **Stack freedom, test discipline.** The target can be any language that runs in Docker, but the
  exploit and tests stay stdlib-only Python, so they run with the repo's uv environment.

(Igjen litt lat å lar ai ta over menneskelig skriving, beklager på forhånd...)

### LLM backends

| Option                           | Use when                                                              | How                                                                                                                                                                                                               |
| -------------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Deterministic mock** (default) | Sårbarheten ligger i det som er bygget ikke selve modellen | A small rule-based responder in `app/` (exactly what the template does). Fast, reliable, CI-friendly.                                                                                                             |
| **Lokal modell**                  | The attack needs real model behavior                                  | Bruk den som heter gpt-120B blablabla fra idun link den i `docker-compose.yml`

### Code quality

- `uv run pre-commit install` at the repo root — ruff formats/lints Python, mdformat tidies the
  markdown.
- Branch `challenge/<name>`, conventional commits: `feat(ctf): add vault-assistant`.

### Build checklist

pcen din har ikke krasjet ennå

## Phase 3: Verify

Du skal egentlig ha tester men me dropper det, så bare kryss fingrene å kjør på!!

## Phase 4: Document

Gjerne skriv dokumentasjon for løsningsforslag.

## Definition of Done

- [ ] Sårbarhet er valgt
- [ ] Angrepet du velger funger for å få flaget.
- [ ] Flaget oppgis ikke på andre måter enn sårbarheten
- [ ] Løsningsforslag er laget

(Ai lagde noe under ikkje så viktig å se på)

## Difficulty rubric

|                     | Easy                        | Medium                                                | Hard                                               |
| ------------------- | --------------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| **Time budget**     | ≤ 45 min                    | 45–120 min                                            | 2h+                                                |
| **Steps**           | One vulnerability, one step | Chains 2–3 techniques, or bypasses a guardrail/filter | Multi-stage chain across components                |
| **Prior knowledge** | Covered by Phases 1–2       | Requires combining techniques                         | Requires research beyond the material              |
| **Hints**           | Reveal the category         | Nudge the next step                                   | Only orient the player                             |
| **Verification**    | Trivially deterministic     | Deterministic with care                               | Needs an explicit determinism plan (design rule 1) |
