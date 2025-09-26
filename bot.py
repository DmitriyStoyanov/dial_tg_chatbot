import asyncio
import logging
import argparse
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dial_client import DialClient
import config

class TelegramDialBot:
    def __init__(self, debug_mode=False):
        self.debug_mode = debug_mode
        self.dial_client = DialClient(debug_mode=debug_mode)
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

        # Configure logging level based on debug mode
        if debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)
            logging.getLogger('dial_client').setLevel(logging.DEBUG)
            logging.getLogger('telegram').setLevel(logging.DEBUG)
            logging.getLogger(__name__).info("🐛 Debug mode enabled - Enhanced logging activated")

    def setup_handlers(self):
        """Setup command and message handlers"""
        # Commands
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("models", self.models_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("debug", self.debug_command))

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
        if self.debug_mode:
            welcome_message += "\n\n🐛 Debug mode is active"
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_message = (
            "🔧 Available Commands:\n\n"
            "/start - Start the bot\n"
            "/help - Show this help message\n"
            "/test - Test connection to AI DIAL\n"
            "/models - List available models\n"
            "/info - Show current model information\n"
            "/debug - Toggle debug information\n\n"
            "💬 How to use:\n"
            "Simply send me any text message and I'll respond using AI DIAL API!\n\n"
            f"🤖 Current Model: {config.DIAL_MODEL}"
        )
        if self.debug_mode:
            help_message += "\n\n🐛 Debug mode is active"
        await update.message.reply_text(help_message)

    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /test command"""
        await update.message.reply_text("🔍 Testing connection to AI DIAL...")

        success = await self.dial_client.test_connection()
        if success:
            await update.message.reply_text("✅ Connection to AI DIAL is working!")
        else:
            await update.message.reply_text("❌ Failed to connect to AI DIAL. Please check the configuration.")

    async def debug_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /debug command"""
        debug_info = (
            f"🐛 **Debug Information**\n\n"
            f"**Debug Mode:** {'✅ Enabled' if self.debug_mode else '❌ Disabled'}\n"
            f"**API URL:** `{config.DIAL_API_URL}`\n"
            f"**Model:** `{config.DIAL_MODEL}`\n"
            f"**User ID:** `{update.effective_user.id}`\n"
            f"**Chat ID:** `{update.effective_chat.id}`\n\n"
            f"**Logging Level:** {'DEBUG' if self.debug_mode else 'INFO'}\n"
        )

        if self.debug_mode:
            debug_info += "🔍 Enhanced API request/response logging is active"
        else:
            debug_info += "💡 Start bot with --debug flag to enable detailed logging"

        await update.message.reply_text(debug_info, parse_mode='Markdown')

    async def models_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /models command"""
        await update.message.reply_text("📋 Fetching available models...")

        models = await self.dial_client.list_models()
        if models:
            # Show first 20 models to avoid message length limits
            models_to_show = models[:20]
            models_text = "\n".join([f"• {model}" for model in models_to_show])

            message = f"🤖 Available Models ({len(models)} total, showing first {len(models_to_show)}):\n\n{models_text}"

            if len(models) > 20:
                message += f"\n\n... and {len(models) - 20} more models"

            message += f"\n\n📌 Current model: {config.DIAL_MODEL}"

            await update.message.reply_text(message)
        else:
            await update.message.reply_text("❌ Failed to fetch models list.")

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        model_info = self.dial_client.get_model_info()

        info_message = (
            f"🤖 **Current Model Information**\n\n"
            f"**Model:** `{model_info['model']}`\n"
            f"**Supports Temperature:** {'✅ Yes' if model_info['supports_temperature'] else '❌ No'}\n"
            f"**Token Parameter:** `{model_info['token_param']}`\n"
            f"**Reasoning Model:** {'🧠 Yes' if model_info['is_reasoning_model'] else '💬 No'}\n\n"
        )

        if model_info['is_reasoning_model']:
            info_message += "🧠 This is a reasoning model that excels at complex problem-solving, math, and coding tasks."
        else:
            info_message += "💬 This is a general-purpose conversational model."

        await update.message.reply_text(info_message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming text messages"""
        user_message = update.message.text
        user_id = str(update.effective_user.id)
        username = update.effective_user.username or "Unknown"
        logger = logging.getLogger(__name__)

        logger.info(f"📨 Received message from {username} ({user_id}): {user_message}")

        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        try:
            # Get response from AI DIAL
            logger.info(f"🔄 Sending message to DIAL API for user {user_id}")
            response = await self.dial_client.send_message(user_message, user_id)

            if response:
                logger.info(f"✅ Successfully received response for user {user_id}")
                if self.debug_mode:
                    logger.debug(f"📤 Sending response to user {user_id}: {response[:100]}{'...' if len(response) > 100 else ''}")
                await update.message.reply_text(response)
            else:
                logger.warning(f"⚠️ Empty response received for user {user_id}")
                await update.message.reply_text("Sorry, I couldn't process your request right now.")

        except Exception as e:
            logger.error(f"❌ Error handling message for user {user_id}: {e}")
            if self.debug_mode:
                logger.debug(f"🔍 Full error details: {e}", exc_info=True)
            await update.message.reply_text("An error occurred while processing your message.")

    def run(self):
        """Start the bot (synchronous version)"""
        logger = logging.getLogger(__name__)
        logger.info("🚀 Starting Telegram DIAL Bot...")
        logger.info(f"🤖 Using model: {config.DIAL_MODEL}")
        logger.info(f"🔗 API URL: {config.DIAL_API_URL}")
        if self.debug_mode:
            logger.info("🐛 Debug mode is ENABLED - Enhanced logging active")

        # Run the bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Telegram DIAL Bot')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode with enhanced logging')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Set logging level')

    args = parser.parse_args()

    # Configure logging
    log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=log_level
    )

    logger = logging.getLogger(__name__)

    try:
        bot = TelegramDialBot(debug_mode=args.debug)
        bot.run()
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        if args.debug:
            logger.debug("🔍 Full error details:", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()