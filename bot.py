import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dial_client import DialClient
import config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramDialBot:
    def __init__(self):
        self.dial_client = DialClient()
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        """Setup command and message handlers"""
        # Commands
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))

        # Messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = (
            "🤖 Welcome to AI DIAL Telegram Bot!\n\n"
            f"I'm connected to {config.DIAL_MODEL} via EPAM AI DIAL.\n"
            "Just send me any message and I'll respond using AI!\n\n"
            "Use /help for more information."
        )
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            "🔧 Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n\n"
            "💬 How to use:\n"
            "Simply send me any text message and I'll respond using AI DIAL API!\n\n"
            f"🤖 Current Model: {config.DIAL_MODEL}"
        )
        await update.message.reply_text(help_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or "Unknown"

        logger.info(f"Received message from {username} ({user_id}): {user_message}")

        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        try:
            # Get response from AI DIAL
            response = await self.dial_client.send_message(user_message, user_id)

            if response:
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("Sorry, I couldn't process your request right now.")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text("An error occurred while processing your message.")

    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram DIAL Bot...")
        logger.info(f"Using model: {config.DIAL_MODEL}")

        # Run the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    bot = TelegramDialBot()
    bot.run()