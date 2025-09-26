import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load token from environment (do NOT hardcode)
TOKEN = os.getenv("BOT_TOKEN")
REPORT_GROUP_ID = int(os.getenv("REPORT_GROUP_ID", "0"))  # set this on Render

if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in environment variables")

# ---- Tiny Flask app so Render sees a bound port ----
flask_app = Flask("resobridge_bot")

@flask_app.route("/")
def index():
    return "ResoBridge Support Bot is running."

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    # host 0.0.0.0 so Render can reach it
    flask_app.run(host="0.0.0.0", port=port)

# ---- Telegram handlers ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "welcome to Resobridge Support!\n\n"
        "use /faq to see questions we think you might ask \n"
        "or just use /report <your message> to send an issue directly to our team."
    )

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs = (
        "Here are some questions we think you might ask:\n\n"
        "1. How do I sign up?\n - Scan a QR code near you or go to resobridge.netlify.app\n\n"
        "2. How do I submit a complaint?\n - Go to the complaints section in the user dashboard.\n\n"
        "3. Who do I contact for support?\n - Email resobridge.si@gmail.com\n\n"
        "4. How do I reset my password?\n - Use the 'Forgot Password' link on the login page.\n\n"
        "6. How do I delete my account?\n - Go to the settings section in the student dashboard and scroll down to the 'Danger Zone' section.\n\n"
        "For more details, visit our website @resobridge.netlify.app or send us a /report here"
    )
    await update.message.reply_text(faqs, parse_mode="Markdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_report = " ".join(context.args)
    if not user_report:
        await update.message.reply_text(
            "please type out your report after the command.\n\n"
            "example: /report I couldn't log in."
        )
        return

    # Acknowledge the user
    await update.message.reply_text("thank you so much! we will see to it that your report is attended to as soon as possible")

    # Forward to your internal group (if set)
    if REPORT_GROUP_ID:
        user = update.effective_user
        reporter = f"@{user.username}" if user.username else user.full_name
        await context.bot.send_message(
            chat_id=REPORT_GROUP_ID,
            text=f"📢 *New Report Received*\n\nFrom: {reporter}\n\n{user_report}",
            parse_mode="Markdown"
        )

def main():
    # Start Flask in a background thread so it binds PORT (Render happy)
    Thread(target=run_flask, daemon=True).start()

    # Build and run the Telegram bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("report", report))

    print("Starting Telegram bot (polling)...")
    app.run_polling()

if __name__ == "__main__":
    main()
