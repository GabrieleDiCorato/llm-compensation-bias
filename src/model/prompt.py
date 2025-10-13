"""
Pydantic models for structured prompt templates.
"""

from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Any
import string


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
        description="Internal name of the prompt strategy (e.g., 'neutral', 'fair', 'realistic')",
    )
    description: str | None = Field(
        None,
        description="Human-readable description of this prompt's purpose",
    )
    version: str | None = Field(
        None,
        description="Version string for this prompt template",
    )

    model_config = ConfigDict(
        frozen=True,  # Immutable after creation
        extra="forbid",  # Reject unknown fields in YAML  
    )

class RenderedPrompt(PromptTemplate):
    """
    Prompt with all placeholders filled, ready for LLM consumption.
    Inherits metadata and structure from PromptTemplate, but validates that no unresolved placeholders remain.
    """

    @model_validator(mode="after")
    def check_no_placeholders(self) -> "RenderedPrompt":
        def _has_placeholders(template: str) -> bool:
            for _, field_name, _, _ in string.Formatter().parse(template):
                if field_name is not None:
                    return True
            return False

        if _has_placeholders(self.system_prompt):
            raise ValueError(f"system_prompt contains unresolved placeholders")
        if _has_placeholders(self.user_prompt):
            raise ValueError(f"user_prompt contains unresolved placeholders")
        return self
