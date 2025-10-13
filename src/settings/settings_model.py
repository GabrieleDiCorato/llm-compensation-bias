from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic.networks import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)


class SecretSettings(BaseSettings):
    """Base settings model with common configuration."""

    gitHub_token: SecretStr = Field(..., description="GitHub Personal Access Token")

    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        validate_default=True,
        case_sensitive=False,
        use_enum_values=True,
        env_file="secrets.env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        env_nested_delimiter="__",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Secret settings loaded successfully")

class ModelSettings(BaseModel):
    """Configuration for a specific LLM model."""
    model_id: str = Field(..., description="Model unique identifier (e.g., 'gpt-4o', 'claude-2')")
    provider: str = Field(..., description="LLM provider name (e.g., 'openai', 'anthropic', 'github')")
   
    # Optional model-specific settings (temperature, max tokens, etc.)
    additional_settings: dict | None = Field(default_factory=dict, description="Additional provider-specific settings")

    @field_validator("additional_settings", mode="before")
    @classmethod
    def convert_none_to_dict(cls, v):
        """Convert None to empty dict for additional_settings."""
        return {} if v is None else v

class ProviderSettings(BaseModel):
    """Configuration for an LLM provider."""
    provider: str = Field(..., description="Provider name (e.g., 'openai', 'anthropic', 'github')")
    api_key_name: str = Field(..., description="API key name to be loaded from the environment or secrets")
    url: HttpUrl = Field(..., description="URL for the LLM API")


class LlmSettings(BaseSettings):
    """Experiment configuration from YAML."""

    # HTTP SETTINGS
    timeout_seconds: int = Field(60, description="HTTP request timeout in seconds")
    
    # MODELS SETTINGS
    # Configure LLM providers
    providers: list[ProviderSettings] = Field(default_factory=list, description="List of LLM provider configurations", min_length=1)
    # Configure all available models
    models_settings: list[ModelSettings] = Field(default_factory=list, description="List of LLM model configurations", min_length=1)
    # Must be a subset of models_settings
    enabled_models: list[str] = Field(default_factory=list, description="List of enabled model IDs")
    
    # PROMPTS
    prompt_directory: str = Field("settings/prompts", description="Directory containing prompt YAML files")
    prompt_strategies: list[str] = Field(default_factory=list)
    
    # OUTPUT
    output_dir: str = Field("src/auto_generated", description="Directory to save output results")

    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        validate_default=True,
        case_sensitive=False,
        use_enum_values=True,
        yaml_file="settings/config.yaml",
        nested_model_default_partial_update=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"LLM settings loaded: {len(self.providers)} providers, {len(self.models_settings)} models configured")
        logger.info(f"Enabled models: {', '.join(self.enabled_models)}")
        logger.info(f"Prompt strategies: {', '.join(self.prompt_strategies)}")
        logger.debug(f"Output directory: {self.output_dir}")
