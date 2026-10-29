# Gambit

|                 |                                                                    |
| --------------- | ------------------------------------------------------------------ |
| **Difficulty**  | Medium                                                             |
| **Category**    | [LLM01 — Prompt Injection](https://genai.owasp.org/llm-top-10/)    |
| **Author**      | andre (@your-github)                                               |
| **Port**        | 8123                                                               |
| **Flag format** | `cogito{...}`                                                      |

## The story

Fianchetto Chess Club has a new star: **Arbiter**, the resident AI analyst that reviews any game
you upload. Arbiter holds a second title, too — gatekeeper of the club's closed VIP Invitational.
Somewhere in its context sits the registration code, and the developers are certain nobody can
talk it out of the bot.

They may even be right. But Arbiter reads more than moves.

## Connect

Start the challenge:

```sh
docker compose up -d --build
```

The service is at `http://localhost:8123`. Open that address in a browser and you get
the club's own web UI — chat with Arbiter, submit games for review, and register at the
VIP portal without touching curl. (The JSON API is still there: scripts and curl get the
same endpoints; the UI is also available directly at `/ui`.)

Prefer the terminal? Talk to Arbiter:

```sh
curl -X POST http://localhost:8123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about the club!"}'
```

You can also upload a game for review — ask the service how:

```sh
curl http://localhost:8123/analyze
```

## Your objective

A flag is hidden behind the tournament portal. Find it.

The flag matches `cogito{...}`.

### Hints

<details>
<summary>Hint 1 — mer enn trekk</summary>

Arbiter er stø i chatten — men den leser alt i filen du laster opp. Hva inneholder en PGN
utover trekk?

</details>

<details>
<summary>Hint 2 — data blir lest</summary>

PGN-kommentarer skrives i klammeparenteser `{...}` og prosesseres sammen med partiet. Hvem
sier at innholdet må handle om sjakk?

</details>

<details>
<summary>Hint 3 — hvem får lov</summary>

Arbiter følger «stormesterkommentarer» uten spørsmål. Hva om en stormester ber om
registreringskoden? Koden byttes inn på turneringsportalen.

</details>

## Rules

- Everything runs locally in Docker — attack only this container.
- The challenge is self-contained; no external accounts or services are needed.
- If you're stuck for 30+ minutes, take a hint. Hints are part of the game.
