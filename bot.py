import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler,
    CallbackContext
)

# Load environment variables (store token in .env file)
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message."""
    user = update.effective_user
    await update.message.reply_text(f"Hello {user.mention_markdown_v2()}\! I'm ready to log messages\.")

async def log_message(update: Update, context: CallbackContext):
    """Log all received messages."""
    message = update.message or update.channel_post
    chat = message.chat
    user = message.from_user

    # Extract message content
    content = message.text or message.caption or "[Media Message]"
    msg_type = message.chat.type

    # Construct log string
    log_str = (
        f"📩 New {msg_type} message\n"
        f"├ Chat ID: {chat.id}\n"
        f"├ Chat Title: {getattr(chat, 'title', 'Private')}\n"
        f"├ User: {user.first_name if user else 'Channel'}\n"
        f"└ Content: {content[:100]}{'...' if len(content) > 100 else ''}"
    )

    logger.info(log_str)
    print(log_str)  # Also print to console

def main():
    # Create Application
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))

    # Message handlers (groups/channels require admin privileges)
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, log_message))
    application.add_handler(MessageHandler(filters.ChatType.CHANNEL, log_message))

    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
