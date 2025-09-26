import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get environment variables
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("REPORT_GROUP_ID")

# Initialize bot application
application = Application.builder().token(TOKEN).build()

# Flask app for Render health check
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!", 200

# Telegram command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! 👋 I’m your support bot. How can I help you?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a message and I’ll forward it to the support team.")

# Register handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    import threading

    # Start Flask in background thread
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

    # Run Telegram bot in main thread (fixes asyncio error)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
