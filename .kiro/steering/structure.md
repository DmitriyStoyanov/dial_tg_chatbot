# Project Structure

## File Organization

### Core Application Files
- `bot.py` - Main Telegram bot implementation with command handlers
- `dial_client.py` - AI DIAL API client with async HTTP communication
- `model_config.py` - Model configuration and parameter handling logic
- `config.py` - Environment configuration management
- `run_bot.py` - Enhanced bot runner with connection testing

### Testing & Analysis
- `test_dial_client.py` - Basic DIAL API functionality tests
- `test_different_models.py` - Model configuration validation tests
- `test_complete_implementation.py` - Comprehensive end-to-end tests
- `analyze_model_features.py` - Model analysis and capability detection

### Utilities & Scripts
- `analyze_models.sh` - Shell script for model pricing analysis
- `cheapest_models.sh` - Script to find most cost-effective models
- `quick_commands.md` - Quick reference for common commands

### Configuration & Environment
- `.env` - Environment variables (not in git)
- `.env.example` - Template for environment configuration
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore patterns

### Documentation
- `README.md` - Complete project documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

### Temporary & Generated
- `tmp/` - Temporary files (e.g., `models.json`)
- `__pycache__/` - Python bytecode cache
- `venv/` - Virtual environment

## Code Organization Patterns

### Class Structure
- **TelegramDialBot** - Main bot class with command handlers
- **DialClient** - API client with session management
- **ModelConfig** - Static methods for model parameter handling

### Async Patterns
- All I/O operations use `async/await`
- Proper session lifecycle management
- Error handling with try/except blocks

### Configuration Hierarchy
1. Environment variables (`.env`)
2. Default values in `config.py`
3. Model-specific overrides in `model_config.py`

### Testing Structure
- Unit tests for individual components
- Integration tests for API communication
- End-to-end tests for complete workflows

## Naming Conventions
- **Files**: Snake_case (e.g., `dial_client.py`)
- **Classes**: PascalCase (e.g., `TelegramDialBot`)
- **Functions/Methods**: Snake_case (e.g., `send_message`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `TELEGRAM_BOT_TOKEN`)

## Import Organization
1. Standard library imports
2. Third-party imports
3. Local application imports
4. Relative imports (if any)