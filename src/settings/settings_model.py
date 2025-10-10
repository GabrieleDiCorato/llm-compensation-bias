from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class LlmSettings(BaseSettings):
    """Experiment configuration from YAML."""

    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        validate_default=True,
        case_sensitive=False,
        use_enum_values=True,
        yaml_file="settings/experiment_config.yaml",
        nested_model_default_partial_update=True,
    )

    llm_providers: list[dict] = Field(default_factory=list)
    prompt_strategies: list[str] = Field(default_factory=list)
    code_context: dict = Field(default_factory=dict)
    output: dict = Field(default_factory=dict)
