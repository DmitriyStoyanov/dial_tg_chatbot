# Telegram AI DIAL Bot

A Telegram chatbot that integrates with EPAM AI DIAL SDK to provide AI-powered responses using various LLM models like ChatGPT-4.

## Features

- 🤖 Telegram bot interface
- 🔗 Integration with EPAM AI DIAL SDK
- 💬 Real-time AI responses
- 📝 Configurable AI models
- 🛡️ Error handling and logging

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DIAL_API_URL=https://your-dial-api-endpoint.com
DIAL_API_KEY=your_dial_api_key_here
DIAL_MODEL=chatgpt-4
```

### 4. Run the Bot

```bash
python bot.py
```

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to initialize
3. Send any message to get AI responses
4. Use `/help` for available commands

## Configuration

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
- `DIAL_API_URL`: Your AI DIAL API endpoint
- `DIAL_API_KEY`: Your AI DIAL API key
- `DIAL_MODEL`: The AI model to use (e.g., chatgpt-4, chatgpt-3.5-turbo)

## Project Structure

```
├── bot.py              # Main bot application
├── dial_client.py      # AI DIAL SDK client wrapper
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Important Notes

⚠️ **DIAL SDK Integration**: The `dial_client.py` file contains a placeholder implementation. You'll need to update it based on the actual aidial-sdk documentation and API structure.

To properly implement the DIAL client:

1. Check the [aidial-sdk documentation](https://github.com/epam/ai-dial-sdk)
2. Update the `send_message` method in `dial_client.py`
3. Implement proper authentication and request formatting

## Troubleshooting

- Ensure all environment variables are set correctly
- Check that your Telegram bot token is valid
- Verify AI DIAL API credentials and endpoint
- Check logs for detailed error information