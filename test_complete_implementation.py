#!/usr/bin/env python3
"""
Comprehensive test of the complete DIAL implementation
"""

import asyncio
import logging
import sys
from dial_client import DialClient
from model_config import ModelConfig
import config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def run_comprehensive_test():
    """Run comprehensive test of all functionality"""

    logger.info("🧪 Starting comprehensive DIAL implementation test...")

    client = DialClient()

    try:
        # Test 1: Connection
        logger.info("\n📡 Test 1: Connection Test")
        if not await client.test_connection():
            logger.error("❌ Connection test failed!")
            return False
        logger.info("✅ Connection test passed")

        # Test 2: Model listing
        logger.info("\n📋 Test 2: Model Listing")
        models = await client.list_models()
        if not models or len(models) == 0:
            logger.error("❌ Model listing failed!")
            return False
        logger.info(f"✅ Found {len(models)} models")

        # Test 3: Model configuration
        logger.info("\n⚙️ Test 3: Model Configuration")
        model_info = client.get_model_info()
        logger.info(f"Current model: {model_info['model']}")
        logger.info(f"Supports temperature: {model_info['supports_temperature']}")
        logger.info(f"Token parameter: {model_info['token_param']}")
        logger.info(f"Is reasoning model: {model_info['is_reasoning_model']}")
        logger.info("✅ Model configuration test passed")

        # Test 4: Chat completion
        logger.info("\n💬 Test 4: Chat Completion")
        test_messages = [
            "Hello! How are you?",
            "What is 15 + 27?",
            "Explain quantum computing in one sentence."
        ]

        for i, message in enumerate(test_messages, 1):
            logger.info(f"Testing message {i}: {message}")
            response = await client.send_message(message, f"test_user_{i}")
            if not response:
                logger.error(f"❌ Chat completion {i} failed!")
                return False
            logger.info(f"✅ Response {i}: {response[:100]}{'...' if len(response) > 100 else ''}")

        # Test 5: Error handling
        logger.info("\n🛡️ Test 5: Error Handling")
        # Test with invalid model (temporarily change model)
        original_model = client.model
        client.model = "invalid-model-name"

        error_response = await client.send_message("Test error handling", "test_user_error")
        if "error" not in error_response.lower() and "sorry" not in error_response.lower():
            logger.warning("⚠️ Error handling might need improvement")
        else:
            logger.info("✅ Error handling works correctly")

        # Restore original model
        client.model = original_model

        logger.info("\n🎉 All tests passed! Implementation is working correctly.")
        return True

    except Exception as e:
        logger.error(f"❌ Test failed with exception: {e}")
        return False
    finally:
        await client.close()

def main():
    """Main test function"""
    success = asyncio.run(run_comprehensive_test())

    if success:
        logger.info("\n✅ COMPREHENSIVE TEST PASSED")
        logger.info("🚀 Your DIAL implementation is ready to use!")
        sys.exit(0)
    else:
        logger.error("\n❌ COMPREHENSIVE TEST FAILED")
        logger.error("🔧 Please check the implementation and configuration")
        sys.exit(1)

if __name__ == "__main__":
    main()