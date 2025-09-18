"""
Model configuration and parameter handling for different AI DIAL models
"""

from typing import Dict, Any

class ModelConfig:
    """Configuration handler for different AI DIAL models"""

    # Models that don't support temperature
    NO_TEMPERATURE_MODELS = {
        'gpt-5-2025-08-07',
        'gpt-5-chat-2025-08-07',
        'gpt-5-mini-2025-08-07',
        'gpt-5-nano-2025-08-07',
        'o1-mini-2024-09-12',
        'o3-mini-2025-01-31',
        'o3-2025-04-16',
        'o4-mini-2025-04-16',
        'o1-2024-12-17',
        'deepseek.r1-v1:0',
        'deepseek-r1',
        'gpt-oss-120b'
    }

    # Models that use max_completion_tokens instead of max_tokens
    MAX_COMPLETION_TOKENS_MODELS = {
        'gpt-5-2025-08-07',
        'gpt-5-chat-2025-08-07',
        'gpt-5-mini-2025-08-07',
        'gpt-5-nano-2025-08-07',
        'o1-mini-2024-09-12',
        'o3-mini-2025-01-31',
        'o3-2025-04-16',
        'o4-mini-2025-04-16',
        'o1-2024-12-17'
    }

    # Models that use max_output_tokens (Gemini models)
    MAX_OUTPUT_TOKENS_MODELS = {
        'gemini-1.5-pro-google-search',
        'gemini-1.5-pro-002',
        'gemini-1.5-flash-002',
        'gemini-2.0-flash-lite',
        'gemini-2.0-flash',
        'gemini-2.0-flash-exp',
        'gemini-2.0-flash-exp-google-search',
        'gemini-2.5-pro',
        'gemini-2.5-pro-google-search',
        'gemini-2.5-flash',
        'gemini-2.5-flash-lite'
    }

    @classmethod
    def get_model_parameters(cls, model: str, max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Get appropriate parameters for the specific model

        Args:
            model: Model identifier
            max_tokens: Maximum tokens to generate
            temperature: Temperature for randomness (0.0 to 1.0)

        Returns:
            Dictionary of parameters suitable for the model
        """
        params = {}

        # Handle token limit parameter
        if model in cls.MAX_COMPLETION_TOKENS_MODELS:
            params["max_completion_tokens"] = max_tokens
        elif model in cls.MAX_OUTPUT_TOKENS_MODELS:
            params["max_output_tokens"] = max_tokens
        else:
            params["max_tokens"] = max_tokens

        # Handle temperature parameter
        if model not in cls.NO_TEMPERATURE_MODELS:
            params["temperature"] = temperature

        return params

    @classmethod
    def supports_temperature(cls, model: str) -> bool:
        """Check if model supports temperature parameter"""
        return model not in cls.NO_TEMPERATURE_MODELS

    @classmethod
    def get_token_param_name(cls, model: str) -> str:
        """Get the correct token parameter name for the model"""
        if model in cls.MAX_COMPLETION_TOKENS_MODELS:
            return "max_completion_tokens"
        elif model in cls.MAX_OUTPUT_TOKENS_MODELS:
            return "max_output_tokens"
        else:
            return "max_tokens"

    @classmethod
    def is_reasoning_model(cls, model: str) -> bool:
        """Check if model is a reasoning model (o1, o3, o4, GPT-5, DeepSeek R1)"""
        reasoning_prefixes = ['o1-', 'o3-', 'o4-', 'gpt-5-']
        reasoning_models = ['deepseek.r1-v1:0', 'deepseek-r1', 'gpt-oss-120b']

        return (any(model.startswith(prefix) for prefix in reasoning_prefixes) or
                model in reasoning_models)