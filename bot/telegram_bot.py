import requests
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

from app.core.config import TG_BOT_TOKEN, BACKEND_URL


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)

    # «печатает…», чтобы общение ощущалось живым и спокойным
    await update.message.chat.send_action(ChatAction.TYPING)

    try:
        response = requests.post(
            BACKEND_URL,
            json={"user_id": user_id, "message": text},
            timeout=130,
        )
        response.raise_for_status()
        reply = response.json()["response"]
    except (requests.RequestException, KeyError, ValueError):
        reply = (
            "Мне сейчас не удаётся ответить. Давай попробуем ещё раз чуть позже."
        )

    await update.message.reply_text(reply)


def main():
    if not TG_BOT_TOKEN:
        raise RuntimeError(
            "TG_BOT_TOKEN не задан. Скопируй .env.example в .env и заполни токен."
        )
    app = ApplicationBuilder().token(TG_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()