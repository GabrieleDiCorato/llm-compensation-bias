"""
GitHub Models API connector implementation.
"""
import httpx

from src.settings.settings_model import SecretSettings, LlmSettings, ModelSettings, ProviderSettings
from src.model.prompt import RenderedPrompt
from .llm_connector import LLMConnector, LLMResponse


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

        payload = {
            "messages": [
                {"role": "system", "content": prompt.system_prompt},
                {"role": "user", "content": prompt.user_prompt},
            ],
            "model": model_id,
        }
        # Adding model-specific settings
        payload.update(self.model_settings.additional_settings)

        with httpx.Client(timeout=self.timeout_sec) as client:
            response = client.post(
                headers=self.headers,
                json=payload,
                url=self.provider_settings.url,
            )
            response.raise_for_status()

        data = response.json()
        choice = data["choices"][0]

        return LLMResponse(
            content=choice["message"]["content"],
            model=data["model"],
            tokens_used=data.get("usage", {}).get("total_tokens"),
            finish_reason=choice.get("finish_reason"),
        )

    @property
    def model_name(self) -> str:
        """Return the model identifier."""
        return self.model_settings.model_id
