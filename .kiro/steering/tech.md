# Technology Stack

## Core Technologies
- **Python 3.x** - Main programming language
- **python-telegram-bot 20.3** - Telegram Bot API wrapper
- **aiohttp** - Async HTTP client for DIAL API communication
- **python-dotenv** - Environment variable management

## Architecture Patterns
- **Async/await** - All I/O operations use async patterns
- **Direct HTTP API** - No SDK dependency, direct REST API calls
- **Model-agnostic design** - Smart parameter handling for different models
- **Session management** - Proper aiohttp session lifecycle

## Environment Setup
```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Environment configuration
cp .env.example .env
# Edit .env with your credentials
```

## Common Commands

### Development & Testing
```bash
# Test DIAL API connection
python test_dial_client.py

# Test different model configurations
python test_different_models.py

# Run comprehensive functionality test
python test_complete_implementation.py

# Analyze model features from API
python analyze_model_features.py
```

### Running the Bot
```bash
# Recommended: Enhanced runner with connection testing
python run_bot.py

# Alternative: Direct bot execution
python bot.py
```

### Model Analysis
```bash
# Get list of available models
curl -s "${DIAL_API_URL}/openai/models" -H "Api-Key: $DIAL_API_KEY"

# Run pricing analysis scripts
./analyze_models.sh
./cheapest_models.sh
```

## Configuration Management
- **Environment variables** via `.env` file
- **Model parameters** automatically selected based on capabilities
- **API endpoints** use OpenAI-compatible format: `/openai/deployments/{model}/chat/completions`

## Error Handling Strategy
- **Network errors** - Graceful degradation with user-friendly messages
- **API errors** - Parse and display meaningful error messages
- **Model incompatibility** - Automatic parameter adjustment
- **Session management** - Proper cleanup on errors