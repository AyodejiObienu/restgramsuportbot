import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask

# --- Telegram Bot Setup ---
TOKEN = os.getenv("BOT_TOKEN")  # Make sure you set BOT_TOKEN in Render's Environment Variables
REPORT_GROUP_ID = os.getenv("REPORT_GROUP_ID")  # Set this to your Telegram group ID in Render

# --- Flask App for Render Health Check ---
app = Flask(__name__)

@app.route("/")
def home():
    return "ResoBridge Telegram Bot is running ✅", 200

# --- Bot Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hey there! Welcome to the ResoBridge Support Bot.\n\n"
        "Use /faq to see frequently asked questions.\n"
        "Use /report <your issue> to send us feedback."
    )

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs = (
        "📌 *Frequently Asked Questions*\n\n"
        "1. *How do I sign up?*\n   Scan a QR code near you or visit https://resobridge.netlify.app\n\n"
        "2. *How do I submit a complaint?*\n   Go to the complaints section in the dashboard.\n\n"
        "3. *Who do I contact for support?*\n   Email resobridge.si@gmail.com\n\n"
        "4. *How do I reset my password?*\n   Use 'Forgot Password' on the login page.\n\n"
        "5. *How do I delete my account?*\n   Go to Settings → Danger Zone → Delete Account.\n\n"
        "_For more details, visit our website or contact support._"
    )
    await update.message.reply_text(faqs, parse_mode="Markdown")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_report = " ".join(context.args)

    if not user_report:
        await update.message.reply_text(
            "⚠️ Please type your report after the command.\nExample: `/report I couldn’t log in.`",
            parse_mode="Markdown"
        )
        return

    # Acknowledge the user
    await update.message.reply_text("✅ Thanks! Your report has been sent to the ResoBridge team.")

    # Send report to your Telegram group
    if REPORT_GROUP_ID:
        await context.bot.send_message(
            chat_id=int(REPORT_GROUP_ID),
            text=f"📢 New report from @{update.message.from_user.username or update.message.from_user.first_name}:\n\n{user_report}"
        )

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: `{chat.id}`", parse_mode="Markdown")

# --- Main Function ---
def main():
    app_bot = Application.builder().token(TOKEN).build()

    # Register bot commands
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("faq", faq))
    app_bot.add_handler(CommandHandler("report", report))
    app_bot.add_handler(CommandHandler("getid", getid))

    # Run polling in the background alongside Flask
    import threading
    threading.Thread(target=app_bot.run_polling, daemon=True).start()

    # Start Flask (needed for Render web service)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

if __name__ == "__main__":
    main()
