import asyncio
import aiohttp
import json
from typing import Optional, Dict, Any
import config
import logging
from model_config import ModelConfig

logger = logging.getLogger(__name__)

class DialClient:
    def __init__(self, debug_mode=False):
        self.api_url = config.DIAL_API_URL
        self.api_key = config.DIAL_API_KEY
        self.model = config.DIAL_MODEL
        self.session = None
        self.debug_mode = debug_mode

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session

    async def close(self):
        """Close the aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def test_connection(self) -> bool:
        """Test the connection to DIAL API"""
        session = await self._get_session()

        try:
            endpoint_url = f"{self.api_url}/openai/models"
            headers = {"Api-Key": self.api_key}

            logger.info(f"🔍 Testing connection to {endpoint_url}")
            if self.debug_mode:
                logger.debug(f"📤 Test request headers: {json.dumps(headers, indent=2)}")

            async with session.get(endpoint_url, headers=headers) as response:
                logger.info(f"📡 Test response status: {response.status}")

                if self.debug_mode:
                    response_headers = dict(response.headers)
                    logger.debug(f"📥 Test response headers: {json.dumps(response_headers, indent=2)}")

                if response.status == 200:
                    response_data = await response.json()
                    if self.debug_mode:
                        logger.debug(f"📥 Test response data: {json.dumps(response_data, indent=2)}")
                    logger.info("✅ Successfully connected to DIAL API")
                    return True
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Failed to connect to DIAL API: {response.status} - {error_text}")
                    if self.debug_mode:
                        logger.debug(f"🔍 Full error response: {error_text}")
                    return False
        except Exception as e:
            logger.error(f"💥 Error testing DIAL API connection: {e}")
            if self.debug_mode:
                logger.debug(f"🔍 Full connection test error details: {e}", exc_info=True)
            return False

    async def list_models(self) -> Optional[list]:
        """List available models from DIAL API"""
        session = await self._get_session()

        try:
            endpoint_url = f"{self.api_url}/openai/models"
            headers = {"Api-Key": self.api_key}

            async with session.get(endpoint_url, headers=headers) as response:
                if response.status == 200:
                    response_data = await response.json()
                    if 'data' in response_data:
                        models = [model['id'] for model in response_data['data']]
                        logger.info(f"Found {len(models)} available models")
                        return models
                    else:
                        logger.error("No 'data' field in models response")
                        return None
                else:
                    error_text = await response.text()
                    logger.error(f"Failed to list models: {response.status} - {error_text}")
                    return None
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return None

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "supports_temperature": ModelConfig.supports_temperature(self.model),
            "token_param": ModelConfig.get_token_param_name(self.model),
            "is_reasoning_model": ModelConfig.is_reasoning_model(self.model)
        }

    def _get_model_parameters(self, model: str, max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """Get appropriate parameters for the specific model"""
        return ModelConfig.get_model_parameters(model, max_tokens, temperature)

    async def send_message(self, user_message: str, user_id: str) -> Optional[str]:
        """
        Send a message to AI DIAL and get the response
        """
        session = await self._get_session()

        try:
            # Create chat completion request
            messages = [
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Get model-specific parameters
            model_params = self._get_model_parameters(self.model)

            # Prepare request data
            request_data = {
                "messages": messages,
                **model_params
            }

            # Construct the API endpoint URL
            endpoint_url = f"{self.api_url}/openai/deployments/{self.model}/chat/completions"

            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "Api-Key": self.api_key
            }

            logger.info(f"🚀 Sending request to {endpoint_url} for user {user_id}")
            if self.debug_mode:
                logger.debug(f"📤 Request headers: {json.dumps(headers, indent=2)}")
                logger.debug(f"📤 Request data: {json.dumps(request_data, indent=2)}")

            # Make the API request
            async with session.post(endpoint_url, json=request_data, headers=headers) as response:
                logger.info(f"📡 Received response with status {response.status} for user {user_id}")

                if self.debug_mode:
                    response_headers = dict(response.headers)
                    logger.debug(f"📥 Response headers: {json.dumps(response_headers, indent=2)}")

                if response.status == 200:
                    response_data = await response.json()

                    if self.debug_mode:
                        logger.debug(f"📥 Full response data: {json.dumps(response_data, indent=2)}")

                    # Extract the response text
                    if 'choices' in response_data and len(response_data['choices']) > 0:
                        choice = response_data['choices'][0]
                        if 'message' in choice and 'content' in choice['message']:
                            response_text = choice['message']['content']

                            # Log usage information if available
                            if 'usage' in response_data:
                                usage = response_data['usage']
                                logger.info(f"📊 Token usage - Prompt: {usage.get('prompt_tokens', 0)}, "
                                          f"Completion: {usage.get('completion_tokens', 0)}, "
                                          f"Total: {usage.get('total_tokens', 0)}")

                            logger.info(f"✅ Successfully got response for user {user_id}")
                            if self.debug_mode:
                                logger.debug(f"📤 Response text (first 200 chars): {response_text[:200]}{'...' if len(response_text) > 200 else ''}")
                            return response_text
                        else:
                            logger.error(f"❌ Unexpected response format: {response_data}")
                            return "Sorry, I received an unexpected response format."
                    else:
                        logger.error(f"❌ No choices in response: {response_data}")
                        return "Sorry, I didn't receive a valid response."
                else:
                    error_text = await response.text()
                    logger.error(f"❌ API request failed with status {response.status}: {error_text}")

                    if self.debug_mode:
                        logger.debug(f"🔍 Full error response: {error_text}")

                    # Try to parse error message
                    try:
                        error_data = json.loads(error_text)
                        if 'error' in error_data and 'message' in error_data['error']:
                            error_msg = error_data['error']['message']
                            logger.error(f"🔍 Parsed error message: {error_msg}")
                            return f"API Error: {error_msg}"
                    except json.JSONDecodeError:
                        logger.debug("🔍 Could not parse error response as JSON")

                    return f"Sorry, the AI service returned an error (status {response.status})."

        except aiohttp.ClientError as e:
            logger.error(f"🌐 Network error sending message to DIAL: {e}")
            if self.debug_mode:
                logger.debug(f"🔍 Full network error details: {e}", exc_info=True)
            return "Sorry, I encountered a network error while processing your request."
        except Exception as e:
            logger.error(f"💥 Unexpected error sending message to DIAL: {e}")
            if self.debug_mode:
                logger.debug(f"🔍 Full unexpected error details: {e}", exc_info=True)
            return "Sorry, I encountered an unexpected error while processing your request."