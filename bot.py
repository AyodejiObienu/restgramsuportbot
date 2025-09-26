import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Flask health check ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running fine!", 200

# --- Telegram bot setup ---
TOKEN = os.getenv("BOT_TOKEN")

application = Application.builder().token(TOKEN).build()



# Example command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive on Render 🚀")

application.add_handler(CommandHandler("start", start))

# Example echo handler
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


GROUP_ID = os.getenv("REPORT_GROUP_ID")
async def forward_to_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and GROUP_ID:
        await context.bot.send_message(chat_id=GROUP_ID, text=f"[User] {update.message.text}")

application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_group))

# --- Main entrypoint ---
if __name__ == "__main__":
    import asyncio
    import threading

    # Run Telegram bot in background
    def run_bot():
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Run Flask (Render needs this to stay alive)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
