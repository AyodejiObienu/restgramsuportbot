import os
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Your bot token from BotFather
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Your Render URL (https://your-app.onrender.com/webhook/<TOKEN>)

bot = Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher to handle commands
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

# --- Command Handlers ---
def start(update: Update, context):
    update.message.reply_text(
        "👋 Welcome! I am your ResoBridge Support Bot.\n\n"
        "Use /report to submit an issue or /faq to see common answers."
    )

def report(update: Update, context):
    update.message.reply_text(
        "📝 Please type your report in detail.\n\n"
        "Our team will review it and get back to you soon!"
    )

def faq(update: Update, context):
    update.message.reply_text(
        "❓ *Frequently Asked Questions*\n\n"
        "1. How do I submit a request?\n   → Use the /report command.\n\n"
        "2. Who can see my reports?\n   → Only the admin team.\n\n"
        "3. How fast will I get a response?\n   → Usually within 24 hours.",
        parse_mode="Markdown"
    )

# Register handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("report", report))
dispatcher.add_handler(CommandHandler("faq", faq))

# --- Flask Routes ---
@app.route("/")
def home():
    return "ResoBridge Bot is running 🚀"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    # Set webhook (only needed once, after deployment)
    if WEBHOOK_URL:
        bot.set_webhook(f"{WEBHOOK_URL}/webhook/{TOKEN}")
        logger.info("Webhook set to %s/webhook/%s", WEBHOOK_URL, TOKEN)

    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
