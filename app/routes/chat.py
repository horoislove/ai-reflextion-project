from fastapi import APIRouter
from pydantic import BaseModel

from app.core.config import HISTORY_WINDOW
from app.core.prompt import SYSTEM_PROMPT
from app.core.safety import is_crisis, CRISIS_RESPONSE
from app.services.llm import generate_response, LLMError
from app.services.memory import load_memory, save_memory

router = APIRouter()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@router.post("/chat")
def chat(req: ChatRequest):
    memory = load_memory()
    history = memory.setdefault(req.user_id, [])

    # сообщение пользователя сохраняем всегда
    history.append({"role": "user", "content": req.message})

    # Кризисный слой: при маркерах острого кризиса не отдаём разговор модели,
    # а отвечаем бережным выверенным текстом с контактами помощи.
    if is_crisis(req.message):
        reply = CRISIS_RESPONSE
        history.append({"role": "assistant", "content": reply})
        save_memory(memory)
        return {"response": reply, "crisis": True}

    # Скользящее окно: системный промпт + последние N сообщений,
    # чтобы не упираться в лимит контекста модели.
    window = history[-HISTORY_WINDOW:]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + window

    try:
        reply = generate_response(messages)
    except LLMError:
        # Откатываем сообщение пользователя, чтобы не копить «висящие» реплики
        # без ответа, и просим повторить.
        history.pop()
        save_memory(memory)
        return {
            "response": "Кажется, я сейчас не на связи. Дай мне минутку и "
            "напиши, пожалуйста, ещё раз.",
            "error": True,
        }

    history.append({"role": "assistant", "content": reply})
    save_memory(memory)
    return {"response": reply}