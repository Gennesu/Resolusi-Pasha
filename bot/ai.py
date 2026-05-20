"""AI client wrapper around an OpenAI-compatible Chat Completions API.

Works with OpenAI, OpenRouter, DeepSeek, Groq, local llama.cpp servers,
or any other provider that speaks the OpenAI Chat Completions protocol.
Just point ``OPENAI_BASE_URL`` at the right endpoint.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List

from openai import AsyncOpenAI

from . import config


_client = AsyncOpenAI(
    api_key=config.OPENAI_API_KEY,
    base_url=config.OPENAI_BASE_URL,
)

# Per-user short-term conversation memory. In-process only: cleared on restart.
_history: Dict[int, Deque[dict]] = defaultdict(
    lambda: deque(maxlen=config.HISTORY_LIMIT)
)


def reset(user_id: int) -> None:
    """Clear the stored conversation history for a user."""
    _history[user_id].clear()


async def chat(user_id: int, user_message: str) -> str:
    """Send ``user_message`` to the model and return its reply.

    Maintains a rolling conversation window per ``user_id``.
    """
    history = _history[user_id]
    history.append({"role": "user", "content": user_message})

    messages: List[dict] = [{"role": "system", "content": config.SYSTEM_PROMPT}]
    messages.extend(history)

    response = await _client.chat.completions.create(
        model=config.OPENAI_MODEL,
        messages=messages,
    )
    reply = (response.choices[0].message.content or "").strip()
    history.append({"role": "assistant", "content": reply})
    return reply
