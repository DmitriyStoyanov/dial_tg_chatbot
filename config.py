import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# AI DIAL Configuration
DIAL_API_URL = os.getenv('DIAL_API_URL', 'https://your-dial-api-endpoint.com')
DIAL_API_KEY = os.getenv('DIAL_API_KEY')
DIAL_MODEL = os.getenv('DIAL_MODEL', 'chatgpt-4')

# Validate required environment variables
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

if not DIAL_API_KEY:
    raise ValueError("DIAL_API_KEY environment variable is required")