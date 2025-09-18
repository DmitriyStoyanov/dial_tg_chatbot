# Product Overview

## Telegram AI DIAL Bot

A Telegram chatbot that integrates with EPAM AI DIAL SDK to provide AI-powered responses using various LLM models.

### Core Features
- Telegram bot interface with command support
- Integration with EPAM AI DIAL API (80+ models)
- Real-time AI responses with typing indicators
- Model-specific parameter handling and optimization
- Comprehensive error handling and logging
- Connection testing and model information display

### Key Commands
- `/start` - Initialize bot
- `/help` - Show help and available commands
- `/test` - Test DIAL API connection
- `/models` - List available models (first 20)
- `/info` - Show current model capabilities

### Model Support
Supports 80+ AI models including:
- **Reasoning Models**: GPT-5 series, OpenAI o1/o3/o4, DeepSeek R1 (no temperature)
- **Conversational Models**: GPT-4, GPT-3.5, Claude, Gemini (full parameters)
- **Automatic Detection**: Model capabilities and parameter requirements

### Architecture
- **Async/await** throughout for optimal performance
- **Direct HTTP** communication with DIAL API (OpenAI-compatible endpoints)
- **Smart parameter handling** based on model capabilities
- **Session management** with proper cleanup
- **Token usage tracking** and logging