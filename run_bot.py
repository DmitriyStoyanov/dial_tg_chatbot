#!/usr/bin/env python3
"""
Enhanced bot runner with connection testing and error handling
"""

import asyncio
import logging
import sys
from telegram import Update
from bot import TelegramDialBot
from dial_client import DialClient

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_dial_connection():
    """Test DIAL connection before starting the bot"""
    logger.info("Testing DIAL API connection...")

    client = DialClient()
    try:
        # Test connection
        if not await client.test_connection():
            logger.error("❌ Failed to connect to DIAL API!")
            logger.error("Please check your DIAL_API_URL and DIAL_API_KEY in .env file")
            return False

        # Show model info
        model_info = client.get_model_info()
        logger.info(f"✅ Connected to DIAL API successfully!")
        logger.info(f"🤖 Using model: {model_info['model']}")
        logger.info(f"🌡️  Temperature support: {'Yes' if model_info['supports_temperature'] else 'No'}")
        logger.info(f"🧠 Reasoning model: {'Yes' if model_info['is_reasoning_model'] else 'No'}")

        return True

    except Exception as e:
        logger.error(f"❌ Error testing DIAL connection: {e}")
        return False
    finally:
        await client.close()

async def main():
    """Main async function to run the bot"""
    logger.info("🚀 Starting Telegram DIAL Bot...")

    # Test DIAL connection first
    if not await test_dial_connection():
        logger.error("❌ Cannot start bot due to DIAL connection issues")
        sys.exit(1)

    # Start the bot
    bot = None
    try:
        bot = TelegramDialBot()
        logger.info("✅ Bot initialized successfully!")
        logger.info("🔄 Starting polling...")

        # Run the bot using the application's async method
        await bot.application.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot crashed: {e}")
        sys.exit(1)
    finally:
        # Clean up the DIAL client session
        if bot:
            await bot.dial_client.close()

def run_bot():
    """Synchronous wrapper to run the async main function"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"❌ Bot runner crashed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_bot()