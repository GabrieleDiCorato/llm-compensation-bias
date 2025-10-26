"""
Simplified, provider-agnostic LLM response model.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LLMResponse(BaseModel):
    """
    Minimal, provider-agnostic LLM response.

    Connectors translate provider-specific responses into this common format.
    This design decouples the response handler from any specific API structure.
    """

    content: str = Field(..., description="The generated text content")

    # Optional common metadata
    model_id: str | None = Field(None, description="Model that generated this response")
    tokens_used: int | None = Field(None, description="Total tokens consumed")
    finish_reason: str | None = Field(
        None, description="Why generation stopped (e.g., 'stop', 'length')"
    )

    # Provider-specific metadata
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Provider-specific metadata (tokens breakdown, IDs, etc.)"
    )

    # Raw response for debugging (excluded from serialization by default)
    raw_response: dict[str, Any] | None = Field(
        None, description="Complete raw response from provider for debugging", exclude=True
    )
    
    # Request payload for debugging and reproducibility
    request_payload: dict[str, Any] | None = Field(
        None, description="Complete request payload sent to provider for debugging and reproducibility", exclude=True
    )

    model_config = ConfigDict(frozen=True, extra="forbid")
