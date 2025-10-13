"""
Pydantic models for structured prompt templates.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Any


class PromptTemplate(BaseModel):
    """
    Structured prompt template with system and user components.

    This model provides type-safe access to prompt templates, validation of required fields,
    and support for optional model-specific and provider-specific configuration.
    """

    # Mandatory fields
    system_prompt: str = Field(
        ...,
        description="System-level instructions for the LLM",
        min_length=1,
    )
    user_prompt: str = Field(
        ...,
        description="User query template with placeholders like \\{person_code}, \\{evaluator_code}",
        min_length=1,
    )

    # Optional metadata
    strategy_name: str | None = Field(
        None,
        description="Name of this prompt strategy (e.g. neutral, fair, realistic)",
    )
    description: str | None = Field(
        None,
        description="Human-readable description of this prompt's purpose",
    )
    version: str | None = Field(
        None,
        description="Version string for this prompt template",
    )

    # Optional provider-specific settings
    provider_settings: dict[str, Any] = Field(
        default_factory=dict,
        description="Provider-specific configuration (e.g., Claude's thinking_budget, OpenAI's response_format)",
    )

    model_config = ConfigDict(
        frozen=True,  # Immutable after creation
        extra="forbid",  # Reject unknown fields in YAML  
    )
