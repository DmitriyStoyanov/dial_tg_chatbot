import asyncio
from typing import Optional
from aidial_sdk import DIALApp
from aidial_sdk.chat_completion import ChatCompletion, Request, Response
import config
import logging

logger = logging.getLogger(__name__)

class DialClient:
    def __init__(self):
        self.api_url = config.DIAL_API_URL
        self.api_key = config.DIAL_API_KEY
        self.model = config.DIAL_MODEL

    async def send_message(self, user_message: str, user_id: str) -> Optional[str]:
        """
        Send a message to AI DIAL and get the response
        """
        try:
            # Create a simple chat completion request
            messages = [
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Initialize DIAL client
            # Note: This is a simplified example. You may need to adjust based on actual SDK usage
            request_data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }

            # Here you would use the actual DIAL SDK methods
            # This is a placeholder for the actual implementation
            # You'll need to check the aidial-sdk documentation for exact usage

            # For now, returning a placeholder response
            # Replace this with actual DIAL SDK call
            response_text = f"Response from {self.model}: {user_message}"

            logger.info(f"Successfully got response for user {user_id}")
            return response_text

        except Exception as e:
            logger.error(f"Error sending message to DIAL: {e}")
            return "Sorry, I encountered an error while processing your request."