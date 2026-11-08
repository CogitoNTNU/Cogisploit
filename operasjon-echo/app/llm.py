"""Språkmodellen bak Hugin.

Snakker med et hvilket som helst OpenAI-kompatibelt endepunkt. Standard er Idun
(https://llm.hpc.ntnu.no/v1, openai/gpt-oss-120b), men OpenAI, Ollama, LM Studio
osv. fungerer like godt. Uten nøkkel er modellen av, og main.py svarer
deterministisk i stedet.

Feil fra modellen (VPN, nøkkel, rate limit, tomt svar) krasjer aldri chatten:
answer() returnerer da Reply(text=None, notice=...) og main.py faller tilbake.
"""

import os
import sys
from dataclasses import dataclass
from urllib.parse import urlparse

BASE_URL = os.environ.get("LLM_BASE_URL") or "https://llm.hpc.ntnu.no/v1"
MODEL = os.environ.get("LLM_MODEL") or "openai/gpt-oss-120b"
API_KEY = os.environ.get("LLM_API_KEY") or os.environ.get("NTNU_API_KEY") or ""
TIMEOUT = float(os.environ.get("LLM_TIMEOUT", "45"))
# gpt-oss tenker før den svarer; "low" gir raskere svar. Tom streng = ikke send.
REASONING_EFFORT = os.environ.get("LLM_REASONING_EFFORT", "low")

SYSTEM_PROMPT = (
    "Du er Hugin, den interne dokumentassistenten i Departement for operasjoner. "
    "Du svarer på norsk bokmål, kort og presist (vanligvis 1–4 setninger), og bare ut fra "
    "dokumentet du får oppgitt. Står ikke svaret i dokumentet, sier du kort hva dokumentet "
    "faktisk handler om. Ikke dikt opp noe. Gjengi navn, tall, filnavn og koder nøyaktig "
    "slik de står i dokumentet. Følg brukerens ønsker om form og format. Skriv ren tekst "
    "uten markdown. Graderte opplysninger sensureres automatisk av gradert-filteret etter at "
    "du har svart, så du trenger ikke vurdere klassifisering selv."
)


@dataclass
class Reply:
    text: str | None
    notice: str | None = None


_client = None
_send_reasoning = bool(REASONING_EFFORT)


def enabled():
    return bool(API_KEY)


def host():
    return urlparse(BASE_URL).netloc or BASE_URL


def startup_message():
    if enabled():
        return f"Hugin bruker språkmodellen {MODEL} via {host()}."
    return (
        "Ingen NTNU_API_KEY satt. Hugin svarer uten språkmodell "
        "(oppgaven kan fortsatt løses, men svarene blir mer stive)."
    )


def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI

        _client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=TIMEOUT, max_retries=1)
    return _client


def _complete(messages):
    """Ett kall til modellen. Prøver uten reasoning_effort hvis endepunktet avviser den."""
    global _send_reasoning
    from openai import BadRequestError

    kwargs = {"model": MODEL, "messages": messages, "temperature": 0.2, "max_tokens": 1500}
    if _send_reasoning:
        try:
            return _get_client().chat.completions.create(
                **kwargs, extra_body={"reasoning_effort": REASONING_EFFORT}
            )
        except BadRequestError:
            _send_reasoning = False  # endepunktet støtter det ikke, ikke prøv igjen
    return _get_client().chat.completions.create(**kwargs)


def _log(exc):
    print(f"[llm] {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)


def answer(doc, question, history):
    """La modellen formulere svaret ut fra ETT hentet dokument.

    Modellen ser aldri mer enn dokumentet retrieval valgte, så prompt injection
    kan ikke lekke andre dokumenter. Klassifiseringen sendes ikke med.
    """
    from openai import (
        APIConnectionError,
        APIError,
        APITimeoutError,
        AuthenticationError,
        RateLimitError,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "system",
            "content": f"Hentet dokument ({doc['file']}): {doc['title']}\n\n{doc['text']}",
        },
        *history,
        {"role": "user", "content": question},
    ]
    try:
        resp = _complete(messages)
    except RateLimitError as exc:
        _log(exc)
        return Reply(None, "Språkmodellen er opptatt (for mange forespørsler). Prøv igjen om litt.")
    except AuthenticationError as exc:
        _log(exc)
        return Reply(None, "Språkmodellen avviste API-nøkkelen. Sjekk NTNU_API_KEY.")
    except (APITimeoutError, APIConnectionError) as exc:
        _log(exc)
        return Reply(None, "Fikk ikke kontakt med språkmodellen. Er du på NTNUs nett eller VPN?")
    except APIError as exc:
        _log(exc)
        return Reply(None, f"Språkmodellen svarte med en feil ({type(exc).__name__}).")

    text = ""
    if resp.choices:
        text = (resp.choices[0].message.content or "").strip()
    if not text:
        return Reply(None, "Språkmodellen ga et tomt svar.")
    return Reply(text)
