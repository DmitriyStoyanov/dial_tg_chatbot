#!/usr/bin/env python3
"""
Test script to verify different model configurations
"""

import asyncio
import logging
from dial_client import DialClient
from model_config import ModelConfig
import config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_model_config():
    """Test model configuration for different model types"""

    # Test different model types
    test_models = [
        'gpt-5-nano-2025-08-07',  # GPT-5 (no temperature)
        'gpt-4o',                 # GPT-4 (supports temperature)
        'o1-mini-2024-09-12',     # Reasoning model (no temperature)
        'claude-3-5-sonnet',      # Claude (supports temperature)
        'gemini-2.0-flash',       # Gemini (different token param)
        'deepseek-r1'             # DeepSeek R1 (no temperature)
    ]

    logger.info("Testing model configurations...")

    for model in test_models:
        logger.info(f"\n--- Testing {model} ---")

        # Test model config
        params = ModelConfig.get_model_parameters(model)
        logger.info(f"Parameters: {params}")
        logger.info(f"Supports temperature: {ModelConfig.supports_temperature(model)}")
        logger.info(f"Token parameter: {ModelConfig.get_token_param_name(model)}")
        logger.info(f"Is reasoning model: {ModelConfig.is_reasoning_model(model)}")

async def test_actual_request():
    """Test actual request with current model"""
    client = DialClient()

    try:
        logger.info(f"\n--- Testing actual request with {config.DIAL_MODEL} ---")

        # Show model info
        model_info = client.get_model_info()
        logger.info(f"Model info: {model_info}")

        # Test a simple request
        response = await client.send_message("What is the capital of France?", "test_user")
        logger.info(f"Response: {response}")

    finally:
        await client.close()

async def main():
    """Main test function"""
    await test_model_config()
    await test_actual_request()

if __name__ == "__main__":
    asyncio.run(main())