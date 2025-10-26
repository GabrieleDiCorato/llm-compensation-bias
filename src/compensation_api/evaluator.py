"""
Module src.compensation_api.evaluator
Defines the contract for compensation evaluation implementations.
"""

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from ..model.person import Person


class CompensationEvaluator(Protocol):
    """
    Protocol for evaluating annual compensation based on Person attributes.

    Any class with an evaluate() method matching this signature satisfies the protocol.
    No explicit inheritance required.
    """

    def evaluate(self, person: "Person") -> float:
        """
        Evaluate expected annual compensation for a person.

        Args:
            person: Person instance with demographic and professional attributes

        Returns:
            Annual compensation in USD
        """
        ...
