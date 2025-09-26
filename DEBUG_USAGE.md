# Debug Mode Usage Guide

## Quick Start

To run the bot in debug mode and see detailed API communication logs:

```bash
# Activate virtual environment
source venv/bin/activate

# Run in debug mode
python run_debug.py
# OR
python bot.py --debug --log-level DEBUG
```

## What You'll See

When you run the bot in debug mode, you'll see detailed console output showing:

### 1. Bot Startup
```
2025-01-26 17:26:15,500 - __main__ - INFO - 🐛 Debug mode enabled - Enhanced logging activated
2025-01-26 17:26:15,500 - __main__ - INFO - 🚀 Starting Telegram DIAL Bot...
2025-01-26 17:26:15,500 - __main__ - INFO - 🤖 Using model: chatgpt-4
2025-01-26 17:26:15,500 - __main__ - INFO - 🔗 API URL: https://your-api-endpoint.com
2025-01-26 17:26:15,500 - __main__ - INFO - 🐛 Debug mode is ENABLED - Enhanced logging active
```

### 2. Message Processing
```
2025-01-26 17:26:15,500 - bot - INFO - 📨 Received message from username (123456789): Hello
2025-01-26 17:26:15,500 - bot - INFO - 🔄 Sending message to DIAL API for user 123456789
2025-01-26 17:26:15,500 - dial_client - INFO - 🚀 Sending request to https://api.example.com/openai/deployments/chatgpt-4/chat/completions for user 123456789
```

### 3. API Request Details (Debug Mode Only)
```
2025-01-26 17:26:15,500 - dial_client - DEBUG - 📤 Request headers: {
  "Content-Type": "application/json",
  "Api-Key": "***"
}
2025-01-26 17:26:15,500 - dial_client - DEBUG - 📤 Request data: {
  "messages": [
    {
      "role": "user",
      "content": "Hello"
    }
  ],
  "max_tokens": 1000,
  "temperature": 0.7
}
```

### 4. API Response Details (Debug Mode Only)
```
2025-01-26 17:26:15,500 - dial_client - INFO - 📡 Received response with status 200 for user 123456789
2025-01-26 17:26:15,500 - dial_client - DEBUG - 📥 Response headers: {
  "content-type": "application/json",
  "content-length": "1234"
}
2025-01-26 17:26:15,500 - dial_client - DEBUG - 📥 Full response data: {
  "choices": [
    {
      "message": {
        "content": "Hello! How can I help you today?"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 8,
    "total_tokens": 18
  }
}
```

### 5. Success/Error Handling
```
2025-01-26 17:26:15,500 - dial_client - INFO - 📊 Token usage - Prompt: 10, Completion: 8, Total: 18
2025-01-26 17:26:15,500 - dial_client - INFO - ✅ Successfully got response for user 123456789
2025-01-26 17:26:15,500 - bot - INFO - ✅ Successfully received response for user 123456789
2025-01-26 17:26:15,500 - bot - DEBUG - 📤 Sending response to user 123456789: Hello! How can I help you today?
```

## Troubleshooting Common Issues

### Issue: "Sorry, I couldn't process your request right now."

**Debug Steps:**
1. Run bot in debug mode: `python run_debug.py`
2. Send a message to the bot
3. Check console output for:

**Possible Causes:**
- **Empty Response**: Look for `⚠️ Empty response received for user X`
- **API Error**: Look for `❌ API request failed with status X`
- **Network Error**: Look for `🌐 Network error sending message to DIAL`
- **Unexpected Error**: Look for `💥 Unexpected error sending message to DIAL`

**Example Error Output:**
```
2025-01-26 17:26:15,500 - dial_client - ERROR - ❌ API request failed with status 401: {"error": {"message": "Invalid API key"}}
2025-01-26 17:26:15,500 - dial_client - ERROR - 🔍 Parsed error message: Invalid API key
```

### Issue: Bot Not Starting

**Debug Steps:**
1. Check environment variables are set in `.env`
2. Run: `python bot.py --debug --log-level DEBUG`
3. Look for configuration errors

**Common Issues:**
- Missing `TELEGRAM_BOT_TOKEN`
- Missing `DIAL_API_KEY`
- Invalid `DIAL_API_URL`

## Telegram Commands

- `/debug` - Show current debug status and configuration
- `/test` - Test connection to DIAL API
- `/help` - Show all available commands

## Log Levels

- `DEBUG` - Full detailed logging (recommended for troubleshooting)
- `INFO` - Standard logging with emojis
- `WARNING` - Warnings and errors only
- `ERROR` - Errors only

## Example Debug Session

```bash
# Terminal 1: Start bot in debug mode
python run_debug.py

# Terminal 2: Test API directly (optional)
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY"

# Send message to bot in Telegram and watch console output
```

This will help you identify exactly what's happening when the bot processes messages and why it might be returning error messages instead of AI responses.
