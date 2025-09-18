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
python3 -m venv venv
source venv/bin/activate
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
# Recommended: Enhanced runner with connection testing
python run_bot.py

# Alternative: Run directly (basic version)
python bot.py
```

**Note**: The enhanced runner (`run_bot.py`) is recommended as it:
- Tests DIAL API connection before starting
- Shows model capabilities and configuration
- Provides better error handling and logging
- Properly manages async/sync interactions

## Usage

1. Start a chat with your bot on Telegram
2. Send `/start` to initialize
3. Send any message to get AI responses
4. Use `/help` for available commands

### Available Commands

- `/start` - Initialize the bot
- `/help` - Show help message
- `/test` - Test connection to AI DIAL
- `/models` - List available models (first 20)
- `/info` - Show current model information and capabilities

### Testing the Implementation

You can test the DIAL client independently:

```bash
# Test basic functionality
python test_dial_client.py

# Test different model configurations
python test_different_models.py

# Analyze model features from the API
python analyze_model_features.py

# Run comprehensive test of all functionality
python test_complete_implementation.py
```

### Model Support

The implementation automatically handles different model types and their specific requirements:

**Reasoning Models** (no temperature support):
- GPT-5 series (gpt-5-nano, gpt-5-mini, etc.)
- OpenAI o1/o3/o4 series
- DeepSeek R1 models

**Conversational Models** (full parameter support):
- GPT-4 series
- GPT-3.5 series
- Anthropic Claude models
- Google Gemini models (uses `max_output_tokens`)

**Features:**
- Automatic parameter selection based on model capabilities
- Proper error handling for unsupported parameters
- Token usage logging
- Model capability detection

## Configuration

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from BotFather
- `DIAL_API_URL`: Your AI DIAL API endpoint
- `DIAL_API_KEY`: Your AI DIAL API key
- `DIAL_MODEL`: The AI model to use (e.g., chatgpt-4, chatgpt-3.5-turbo)

## Project Structure

```
├── bot.py                      # Main bot application
├── dial_client.py              # AI DIAL API client implementation
├── model_config.py             # Model configuration and parameter handling
├── config.py                   # Configuration management
├── run_bot.py                  # Enhanced bot runner with connection testing
├── test_dial_client.py         # Basic functionality test
├── test_different_models.py    # Model configuration test
├── test_complete_implementation.py # Comprehensive functionality test
├── analyze_model_features.py   # Model analysis utility
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── README.md                   # This file
```

## DIAL SDK Integration

✅ **DIAL Client Implementation**: The `dial_client.py` file now contains a fully functional implementation that communicates directly with the AI DIAL API using HTTP requests.

**Key Features:**
- Direct HTTP communication with DIAL API using OpenAI-compatible endpoints
- Model-specific parameter handling (different models support different parameters)
- Proper error handling and logging
- Connection testing and model listing capabilities
- Async/await support for optimal performance

**Note**: The `aidial-sdk` package is designed for creating DIAL applications, not consuming them. This implementation uses direct HTTP requests to the DIAL API instead.

## Troubleshooting

### Common Issues

**Event Loop Errors**:
- Use `python run_bot.py` instead of `python bot.py` for better async handling
- The enhanced runner properly manages async/sync interactions

**Connection Issues**:
- Ensure all environment variables are set correctly in `.env`
- Check that your Telegram bot token is valid
- Verify AI DIAL API credentials and endpoint
- Test connection with: `python test_dial_client.py`

**Model Parameter Errors**:
- Different models support different parameters (temperature, token limits)
- The implementation automatically handles model-specific requirements
- Use `/info` command in the bot to see current model capabilities

**Bot Not Responding**:
- Check logs for detailed error information
- Verify the bot has proper permissions in Telegram
- Test DIAL API connection with `/test` command

### Debug Commands

```bash
# Test DIAL API connection
python test_dial_client.py

# Test different model configurations
python test_different_models.py

# Run comprehensive functionality test
python test_complete_implementation.py
```

# Notes
## Get list of models from AI Dial

```shell
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY"
```