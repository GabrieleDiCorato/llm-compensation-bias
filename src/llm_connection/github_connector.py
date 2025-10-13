"""
GitHub Models API connector implementation.
"""
import httpx
import logging

from src.settings.settings_model import SecretSettings, LlmSettings, ModelSettings, ProviderSettings
from src.model.prompt import RenderedPrompt
from .llm_connector import LLMConnector, LLMResponse

logger = logging.getLogger(__name__)


class GitHubConnector:
    """GitHub Models API implementation of LLMConnector protocol."""

    def __init__(
        self,
        secret_settings: SecretSettings,
        provider_settings: ProviderSettings,
        model_settings: ModelSettings,
        timeout_sec: int = 60,
    ):
        self.secret_settings = secret_settings
        self.provider_settings = provider_settings
        self.model_settings = model_settings
        self.timeout_sec = timeout_sec

        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.secret_settings.gitHub_token.get_secret_value()}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        }
        
        logger.info(f"GitHubConnector initialized for model: {model_settings.model_id}")
        logger.debug(f"Provider URL: {provider_settings.url}")
        logger.debug(f"Timeout: {timeout_sec} seconds")

    def query(
        self,
        prompt: RenderedPrompt,
        provider_id: str,
        model_id: str
    ) -> LLMResponse:
        """
        Send prompt to GitHub Models API and return response.

        Args:
            prompt: The rendered prompt to send to the LLM

        Returns:
            LLMResponse with content and metadata
        """
        logger.info(f"Sending query to model: {model_id} (strategy: {prompt.strategy_name})")
        logger.debug(f"System prompt length: {len(prompt.system_prompt)} characters")
        logger.debug(f"User prompt length: {len(prompt.user_prompt)} characters")

        payload = {
            "messages": [
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt.user_prompt},
            ],
            "model": model_id,
        }
        # Adding model-specific settings
        payload.update(self.model_settings.additional_settings)
        
        logger.debug(f"Additional settings: {self.model_settings.additional_settings}")

        try:
            with httpx.Client(timeout=self.timeout_sec) as client:
                logger.debug(f"Making POST request to {self.provider_settings.url}")
                response = client.post(
                    headers=self.headers,
                    json=payload,
                    url=self.provider_settings.url,
                )
                response.raise_for_status()
                logger.debug(f"Response received with status code: {response.status_code}")

            data = response.json()
            choice = data["choices"][0]

            llm_response = LLMResponse(
                content=choice["message"]["content"],
                model=data["model"],
                tokens_used=data.get("usage", {}).get("total_tokens"),
                finish_reason=choice.get("finish_reason"),
            )
            
            logger.info(f"Query completed successfully for model: {model_id}")
            logger.info(f"Tokens used: {llm_response.tokens_used}, Finish reason: {llm_response.finish_reason}")
            logger.debug(f"Response content length: {len(llm_response.content)} characters")
            
            return llm_response
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.TimeoutException:
            logger.error(f"Request timed out after {self.timeout_sec} seconds")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during query: {type(e).__name__}: {str(e)}")
            raise

    @property
    def model_name(self) -> str:
        """Return the model identifier."""
        return self.model_settings.model_id
