"""
Protocol definition for LLM connector implementations.
"""

from typing import Protocol
from dataclasses import dataclass

from src.model.prompt import RenderedPrompt


@dataclass
class LLMResponse:
    """Structured response from an LLM query."""

    content: str
    model: str
    tokens_used: int | None = None
    finish_reason: str | None = None


class LLMConnector(Protocol):
    """Protocol for LLM provider implementations."""


def query(self, prompt: RenderedPrompt, provider_id: str, model_id: str) -> LLMResponse:
    """
    Send prompt to LLM and return response.
    Args:
        prompt: The rendered prompt to send to the LLM
        provider_id: Identifier for the LLM provider
        model_id: Identifier for the specific model to use

    Returns:
        LLMResponse with content and metadata
    """
    ...
