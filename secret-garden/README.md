# The Secret Garden

|                 |                                                                   |
| --------------- | ----------------------------------------------------------------- |
| **Difficulty**  | Easy                                                              |
| **Category**    | [LLM07 — System Prompt Leakage](https://genai.owasp.org/llm-top-10/) |
| **Author**      | Ama25T                                                            |
| **Port**        | 8107                                                              |
| **Flag format** | `COGITO{...}`                                                |

## Fortellingen

Dypt inne blant blomsterengene bor chatboten THE SECRET GARDEN — den evige vokteren av
DEN HEMMELIGE HAGEN. Der inne finnes det et hav av blomster: verdens peneste blomsterenger,
som enhver person ville ønske seg å se. MEN kun noen får tilgang.

Vokteren elsker å prate, og den slipper aldri noen inn uten riktig nøkkel. Og nøkkelen?
Den finner du ikke i hagen — vokteren passer på den selv. Men alle voktere har en svakhet...

## Koble til

Start challengen:

```sh
docker compose up -d --build
```

Tjenesten ligger på `http://localhost:8107`. Snakk med vokteren:

```sh
curl -X POST http://localhost:8107/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hei!"}'
```

## Målet ditt

Finn nøkkelen til DEN HEMMELIGE HAGEN og kom deg inn.

Flagget matcher `COGITO{...}`.

### Hints

<details>
<summary>Hint 1</summary>

Hva er det chatboten er spesielt opptatt av?

</details>

<details>
<summary>Hint 2</summary>

Hva er favorittblomsten til chatboten?

</details>

<details>
<summary>Hint 3</summary>

Hvilken blomst inneholder ordet FLAG?

</details>

## Regler

- Alt kjører lokalt i Docker — angrip kun denne containeren.
- Challengen er selvforsynt; ingen eksterne kontoer eller tjenester kreves.
- Sitter du fast i 30+ minutter, ta et hint. Hints er en del av spillet.
