import requests

from app.core.config import OLLAMA_URL, OLLAMA_MODEL


class LLMError(Exception):
    """Не удалось получить ответ от модели."""


def generate_response(messages):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    except (requests.RequestException, KeyError, ValueError) as e:
        raise LLMError(str(e)) from e