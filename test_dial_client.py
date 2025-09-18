#!/usr/bin/env python3
"""
Test script for DIAL client functionality
"""

import asyncio
import logging
from dial_client import DialClient

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def test_dial_client():
    """Test the DIAL client functionality"""
    client = DialClient()

    try:
        # Test connection
        logger.info("Testing connection to DIAL API...")
        connection_ok = await client.test_connection()
        if not connection_ok:
            logger.error("Connection test failed!")
            return

        # List models
        logger.info("Listing available models...")
        models = await client.list_models()
        if models:
            logger.info(f"Found {len(models)} models")
            logger.info(f"First 5 models: {models[:5]}")
        else:
            logger.error("Failed to list models!")
            return

        # Test chat completion
        logger.info("Testing chat completion...")
        test_message = "Hello! Can you tell me what 2+2 equals?"
        response = await client.send_message(test_message, "test_user")

        if response:
            logger.info(f"Chat completion successful!")
            logger.info(f"User message: {test_message}")
            logger.info(f"AI response: {response}")
        else:
            logger.error("Chat completion failed!")

    except Exception as e:
        logger.error(f"Test failed with error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test_dial_client())