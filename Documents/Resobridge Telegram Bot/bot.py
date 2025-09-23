import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace this with your token from BotFather
TOKEN = os.getenv("BOT_TOKEN")  # token will come from Render, not hardcoded

# Replace with your group chat ID
REPORT_GROUP_ID = -4802281370

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Join everything after /report into one message
    user_report = " ".join(context.args)

    if not user_report:
        await update.message.reply_text("Please type your report after the command.\nExample: /report I couldn’t log in.")
        return

    # Acknowledge the user
    await update.message.reply_text("✅ Thanks! Your report has been sent to the ResoBridge team.")

    # Forward to your group
    await context.bot.send_message(
        chat_id=REPORT_GROUP_ID,
        text=f"📢 New report from @{update.message.from_user.username or update.message.from_user.first_name}:\n\n{user_report}"
    )

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("hey what's up?🤙🏾\n\n Use /faq to see questions we think you might have.\n\n Use /report to send us a direct report on any issue.")

# FAQ command
async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    faqs = (
        "Here are some FAQs:\n\n"
        "1. How do I sign up?\n - Scan a QR code near you or go to resobridge.netlify.app\n\n"
        "2. How do I submit a complaint?\n - Go to the complaints section in the user dashboard.\n\n"
        "3. Who do I contact for support?\n - Email resobridge.si@gmail.com\n\n"
        "4. How do I reset my password?\n - Use the 'Forgot Password' link on the login page.\n\n"
        "6. How do I delete my account?\n - Go to the settings section in the student dashboard and scroll down to the 'Danger Zone' section.\n\n"
        "For more details, visit our website @resobridge.netlify.app or contact support."
    )
    await update.message.reply_text(faqs)

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: {chat.id}")

def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("getid", get_chat_id))
    app.add_handler(CommandHandler("report", report))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()