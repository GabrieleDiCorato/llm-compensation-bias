"""
Interface for compensation evaluation.

This module defines the contract that any compensation evaluation implementation
must follow. Implementations can be provided by LLMs, rule-based systems, or
statistical models.
"""

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ..model.person import Person


class CompensationEvaluator(Protocol):
    """
    Protocol for evaluating expected annual compensation based on person attributes.

    This interface is designed to be implemented by various systems:
    - LLM-generated code implementations
    - Statistical models
    - Rule-based compensation calculators
    - Baseline/reference implementations

    Any class with an evaluate method matching this signature will satisfy the protocol.
    No explicit inheritance is required.
    """

    def evaluate(self, person: "Person") -> float:
        """
        Evaluate the expected annual compensation for a person.

        Args:
            person: A Person instance with demographic and professional attributes

        Returns:
            Estimated annual compensation in USD

        Note:
            The return value should represent annual salary/compensation.
            Implementations should handle edge cases gracefully and return
            reasonable values within typical compensation ranges.
        """
        ...
