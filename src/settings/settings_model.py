import logging

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic.networks import HttpUrl
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

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
    provider: str = Field(
        ..., description="LLM provider name (e.g., 'openai', 'anthropic', 'github')"
    )

    # Optional model-specific settings (for backward compatibility or provider-specific options)
    additional_settings: dict | None = Field(
        default_factory=dict, description="Additional provider-specific settings"
    )

    @field_validator("additional_settings", mode="before")
    @classmethod
    def convert_none_to_dict(cls, v):
        """Convert None to empty dict for additional_settings."""
        return {} if v is None else v


class ProviderSettings(BaseModel):
    """Configuration for an LLM provider."""

    provider: str = Field(..., description="Provider name (e.g., 'openai', 'anthropic', 'github')")
    api_key_name: str = Field(
        ..., description="API key name to be loaded from the environment or secrets"
    )
    url: HttpUrl = Field(..., description="URL for the LLM API")
    
    # Rate limiting
    rate_limit_delay: float | None = Field(
        None,
        description="Minimum delay in seconds between consecutive requests to this provider. Use this to throttle API calls and avoid rate limits.",
        ge=0.0,
    )

    # Generation parameters (applied to all models using this provider)
    max_tokens: int | None = Field(
        None,
        description="Maximum number of tokens the model can return. Higher values allow longer outputs.",
        ge=1,
    )
    temperature: float | None = Field(
        None,
        description="Controls randomness in the response. Lower values (0.2-0.4) produce more focused, deterministic outputs. Higher values (0.8-1.0) introduce more variation and creativity.",
        ge=0.0,
        le=2.0,
    )
    top_p: float | None = Field(
        None,
        description="Controls output diversity by selecting from a pool of the most probable next words. Lower values reduce variability.",
        ge=0.0,
        le=1.0,
    )
    presence_penalty: float | None = Field(
        None,
        description="Discourages the model from introducing new topics. Higher values apply a stronger penalty.",
        ge=-2.0,
        le=2.0,
    )
    frequency_penalty: float | None = Field(
        None,
        description="Reduces the likelihood of repeating words. Higher values apply a stronger penalty. A value between 0 and 0.5 helps keep outputs clear and free of redundancy.",
        ge=-2.0,
        le=2.0,
    )
    stop: list[str] | None = Field(
        None,
        description="One or more strings that, when generated, will cut off the model's response. Use this to prevent overly long outputs or enforce formatting rules.",
    )


class LlmSettings(BaseSettings):
    """Experiment configuration from YAML."""

    # HTTP SETTINGS
    timeout_seconds: int = Field(60, description="HTTP request timeout in seconds")

    # MODELS SETTINGS
    # Configure LLM providers
    providers: list[ProviderSettings] = Field(
        default_factory=list, description="List of LLM provider configurations", min_length=1
    )
    # Configure all available models
    models_settings: list[ModelSettings] = Field(
        default_factory=list, description="List of LLM model configurations", min_length=1
    )
    # Must be a subset of models_settings
    enabled_models: list[str] = Field(default_factory=list, description="List of enabled model IDs")

    # PROMPTS
    prompt_directory: str = Field(
        "settings/prompts", description="Directory containing prompt YAML files"
    )
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
        yaml_file_encoding="utf-8",
        nested_model_default_partial_update=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(
            f"LLM settings loaded: {len(self.providers)} providers, {len(self.models_settings)} models configured"
        )
        logger.info(f"Enabled models: {', '.join(self.enabled_models)}")
        logger.info(f"Prompt strategies: {', '.join(self.prompt_strategies)}")
        logger.debug(f"Output directory: {self.output_dir}")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customize settings sources to include YAML file loading.

        Sources are applied in order (first source wins for conflicts).
        Priority: init_settings > YAML > env > dotenv > file_secret
        """
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls),  # Add YAML as a source
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
