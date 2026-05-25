from fastapi import APIRouter

from app.services.memory import load_memory, save_memory
from app.services.llm import generate_response
from app.core.prompt import SYSTEM_PROMPT

router = APIRouter()

@router.post("/chat")
def chat(user_id: str, message: str):
    memory = load_memory()

    if user_id not in memory:
        memory[user_id] = []

    # добавляем сообщение пользователя
    memory[user_id].append({
        "role": "user",
        "content": message
    })

    # собираем messages
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += memory[user_id]

    # получаем ответ
    reply = generate_response(messages)

    # сохраняем ответ
    memory[user_id].append({
        "role": "assistant",
        "content": reply
    })

    save_memory(memory)

    return {"response": reply}