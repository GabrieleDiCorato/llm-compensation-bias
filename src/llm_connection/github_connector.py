"""
GitHub Models API connector implementation.
"""
import httpx
import logging

from src.settings.settings_model import SecretSettings, ModelSettings, ProviderSettings
from src.model.prompt import RenderedPrompt
from src.model.llm_response import LLMResponse

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
        Send prompt to GitHub Models API and return simplified response.

        Args:
            prompt: The rendered prompt to send to the LLM
            provider_id: Provider identifier (for logging)
            model_id: Model identifier

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
        
        # Add generation parameters from provider settings if specified
        if self.provider_settings.max_tokens is not None:
            payload["max_tokens"] = self.provider_settings.max_tokens
        if self.provider_settings.temperature is not None:
            payload["temperature"] = self.provider_settings.temperature
        if self.provider_settings.top_p is not None:
            payload["top_p"] = self.provider_settings.top_p
        if self.provider_settings.presence_penalty is not None:
            payload["presence_penalty"] = self.provider_settings.presence_penalty
        if self.provider_settings.frequency_penalty is not None:
            payload["frequency_penalty"] = self.provider_settings.frequency_penalty
        if self.provider_settings.stop is not None:
            payload["stop"] = self.provider_settings.stop
        
        # Adding backward-compatible additional settings or model-specific overrides, if they exist
        if self.model_settings.additional_settings:
            payload.update(self.model_settings.additional_settings)
        
        logger.debug(f"Generation parameters: max_tokens={self.provider_settings.max_tokens}, temperature={self.provider_settings.temperature}, top_p={self.provider_settings.top_p}, presence_penalty={self.provider_settings.presence_penalty}, frequency_penalty={self.provider_settings.frequency_penalty}, stop={self.provider_settings.stop}")
        logger.debug(f"Additional settings: {self.model_settings.additional_settings}")

        try:
            with httpx.Client(timeout=self.timeout_sec) as client:
                logger.debug(f"Making POST request to {self.provider_settings.url}")
                response = client.post(
                    url=str(self.provider_settings.url),  # Convert HttpUrl to string
                    headers=self.headers,
                    json=payload,
                )
                response.raise_for_status()
                logger.debug(f"Response received with status code: {response.status_code}")

            data = response.json()
            
            logger.debug(f"Raw response keys: {list(data.keys())}")
            logger.debug(f"Number of choices: {len(data.get('choices', []))}")

            # Parse GitHub-specific response into our generic format
            return self._parse_github_response(data, model_id)
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.TimeoutException:
            logger.error(f"Request timed out after {self.timeout_sec} seconds")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during query: {type(e).__name__}: {str(e)}")
            raise

    def _parse_github_response(self, data: dict, model_id: str) -> LLMResponse:
        """
        Parse GitHub API response into our generic LLMResponse format.
        
        This method encapsulates all GitHub-specific parsing logic,
        keeping the response handler decoupled from provider details.
        
        Args:
            data: Raw response from GitHub API
            model_id: Model identifier
            
        Returns:
            Provider-agnostic LLMResponse
            
        Raises:
            ValueError: If response structure is invalid
        """
        try:
            # Extract content from GitHub's structure
            content = data["choices"][0]["message"]["content"]
            finish_reason = data["choices"][0].get("finish_reason")
            
            # Extract token usage if available
            usage = data.get("usage", {})
            total_tokens = usage.get("total_tokens")
            
            # Build metadata dict with provider-specific details
            metadata = {
                "prompt_tokens": usage.get("prompt_tokens"),
                "completion_tokens": usage.get("completion_tokens"),
                "response_id": data.get("id"),
                "created": data.get("created"),
                "object_type": data.get("object"),
                "role": data["choices"][0]["message"].get("role"),
                "choice_index": data["choices"][0].get("index", 0),
            }
            
            logger.info(f"Query completed successfully for model: {model_id}")
            logger.info(f"Tokens used: {total_tokens}, Finish reason: {finish_reason}")
            logger.debug(f"Response content length: {len(content)} characters")
            
            if usage:
                logger.debug(
                    f"Token breakdown - Prompt: {metadata['prompt_tokens']}, "
                    f"Completion: {metadata['completion_tokens']}, "
                    f"Total: {total_tokens}"
                )
            
            return LLMResponse(
                content=content,
                model_id=model_id,
                tokens_used=total_tokens,
                finish_reason=finish_reason,
                metadata=metadata,
                raw_response=data  # Store complete response for debugging
            )
            
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse GitHub response: {e}")
            logger.debug(f"Response structure: {list(data.keys())}")
            raise ValueError(f"Invalid GitHub API response structure: {e}") from e


    @property
    def model_name(self) -> str:
        """Return the model identifier."""
        return self.model_settings.model_id
