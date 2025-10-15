"""
Factory for creating LLM connector instances.
"""

import logging

from src.settings.settings_model import LlmSettings, SecretSettings

from .github_connector import GitHubConnector
from .llm_connector import LLMConnector

logger = logging.getLogger(__name__)


def create_connector(model_id: str, settings: LlmSettings, secrets: SecretSettings) -> LLMConnector:
    """
    Factory function to create an LLMConnector instance based on model_id and settings.
    Args:
        model_id: Identifier for the specific model to use
        settings: LlmSettings instance with configuration
        secrets: SecretSettings instance with API keys
    Returns:
        An instance of LLMConnector for the specified model and provider
    """
    logger.info(f"Creating connector for model: {model_id}")

    model_cfg = next((m for m in settings.models_settings if m.model_id == model_id), None)
    if model_cfg is None:
        logger.error(f"Model ID {model_id} not found in settings")
        raise ValueError(f"Model ID {model_id} not found in settings.")

    logger.debug(f"Model configuration found: provider={model_cfg.provider}")

    provider_cfg = next((p for p in settings.providers if p.provider == model_cfg.provider), None)
    if provider_cfg is None:
        logger.error(f"Provider {model_cfg.provider} for model {model_id} not found in settings")
        raise ValueError(
            f"Provider {model_cfg.provider} for model {model_id} not found in settings."
        )

    logger.debug(f"Provider configuration found: {provider_cfg.provider}")

    if provider_cfg.provider == "github":
        logger.info(f"Initializing GitHub connector for model {model_id}")
        return GitHubConnector(
            secret_settings=secrets,
            provider_settings=provider_cfg,
            model_settings=model_cfg,
            timeout_sec=settings.timeout_seconds,
        )
    else:
        logger.error(f"Unknown provider type: {provider_cfg.provider}")
        raise ValueError(
            f"Unknown provider type: {provider_cfg.provider}. Supported providers: github"
        )
