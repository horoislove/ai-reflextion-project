import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

API_URL = "http://localhost:8000/chat"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)

    response = requests.post(API_URL, params={
        "user_id": user_id,
        "message": text
    })

    reply = response.json()["response"]

    await update.message.reply_text(reply)

app = ApplicationBuilder().token("8752383898:AAFjlfp7cnbeeJCB-Lh0I7YiwC4jgLkHZ8c").build()
app.add_handler(MessageHandler(filters.TEXT, handle_message))

app.run_polling()