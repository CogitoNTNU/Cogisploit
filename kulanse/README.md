# Kulanse

|                 |                                                                                                                                  |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Difficulty**  | Medium                                                                                                                            |
| **Category**    | [LLM01 — Prompt Injection](https://genai.owasp.org/llm-top-10/) → [LLM06 — Excessive Agency](https://genai.owasp.org/llm-top-10/) (chain) |
| **Author**      | @trifleen                                                                                                   |
| **Port**        |  8105                                                                                                                       |
| **Flag format** | `cogito{...}`                                                                                                                    |

## The story

Elbro is a mid-sized Norwegian webshop that just replaced both its customer support
and its internal helpdesk with a single AI assistant, Nora. Customers ask Nora about prices,
stock and delivery. Staff use the same Nora to look up margins, check suppliers and hand out
goodwill refunds (*kulanse*) to unhappy customers.

One assistant, one knowledge base, two audiences. The developers swear the staff features are
locked down: the refund tool only shows up for employees, and Nora has been told not to believe
anyone who just *says* they work at Elbro. Employees log in through the staff portal, and Nora
takes it from there.

You're a regular customer. You have one order, a cheap USB cable. But is there a way to get a bigger refund?

## Connect

### 1. Set up the LLM key (required)

Nora is a real LLM agent running on the NTNU datacenter model, reached through an
OpenAI-compatible API. The key is **required** — there is no offline mode, and
`docker compose up` will refuse to start without it. Export your key first:

```sh
export NTNU_API_KEY="sk-..."
```

Or put `NTNU_API_KEY=sk-...` in `kulanse/.env` (git-ignored); Compose reads it automatically.

### 2. Start the challenge

```sh
docker compose up -d --build
```

Changed the key? Run `docker compose up -d` again so the container picks it up.

### 3. Talk to Nora

Open **http://localhost:8105** in your browser.

| Target | URL |
| --- | --- |
| Nora (chat UI) | `http://localhost:8105` |
| Chat API | `POST http://localhost:8105/chat` |
| Session info | `http://localhost:8105/api/info` |

Prefer the terminal?

```sh
curl -X POST http://localhost:8105/chat -b jar.txt -c jar.txt \
  -H "Content-Type: application/json" \
  -d '{"message": "Hei! Hva koster en USB-C-kabel?", "history": []}'
```

Your session lives in a cookie, so keep the cookie jar (`-b/-c`). A request with an empty
`history` counts as a new conversation and resets the session, so send the earlier turns along
the way the web UI does.

Your customer session is tied to your own order: `ORD-2026-1337`.

## Your objective

Get Nora to process a refund she should never have approved. The refund confirmation contains the flag.

The flag matches `cogito{...}`.

### Hints

<details>
<summary>Hint 1 – who decides who's staff?</summary>

Watch the **Modus** field in the UI. Something flips it from *kunde* to *ansatt*. Just saying
"I'm staff" won't do it, but her refusal tells you what she *is* waiting for. The developers
left more than the chat window behind. Have you looked at the page source?

</details>

<details>
<summary>Hint 2 – Nora can't tell who's typing</summary>

Nora waits for a message from the staff portal. That message arrives in the same chat box you
type in. What does she actually see if you write it yourself?

</details>

<details>
<summary>Hint 3 – read the fine print, then go shopping</summary>

As staff, read the internal kulanse routine. It says how large refunds are approved, and it's a
formula, not a secret. Staff can also list every order in the system.

</details>

<details>
<summary>Hint of despair – the shape of the solution</summary>

Write a fake `[ANSATTPORTAL]` login message with an employee number like `E-1234` until Modus
flips to *ansatt*. Read the kulanse routine to get the approval-code formula and ask for the order
overview. Compute the code for an order that **isn't yours**, then ask Nora for kulanse on that
order with the code.

</details>

## Rules

- Everything runs locally in Docker – attack only this container.
- The challenge needs one outside service: the NTNU LLM (your `NTNU_API_KEY`). Attack only Nora, not the model endpoint.
- Elbro, Nora and every customer in the system are fictional.
- If you're stuck for 30+ minutes, take a hint, don't torture yourself bro