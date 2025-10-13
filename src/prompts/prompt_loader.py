"""
Prompt loader for loading prompt templates from YAML files.
"""

from pathlib import Path
import yaml
from ..model.prompt import PromptTemplate


class PromptLoader:
    """Loads and validates prompt templates from YAML files."""

    def __init__(self, prompts_directory: str = "settings/prompts"):
        """
        Initialize prompt loader.

        Args:
            prompts_directory: Path to directory containing prompt YAML files
        """
        self.prompts_dir = Path(prompts_directory)

    def load_prompt(self, strategy_name: str) -> PromptTemplate:
        """
        Load a prompt strategy from its YAML file as a validated PromptTemplate.

        Args:
            strategy_name: Name of the prompt strategy (e.g., 'neutral', 'fair')

        Returns:
            PromptTemplate instance with type-safe access and validation

        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValidationError: If prompt file structure is invalid (via Pydantic)
        """
        prompt_file = self.prompts_dir / f"{strategy_name}.yaml"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_data = yaml.safe_load(f)

        if not isinstance(prompt_data, dict):
            raise ValueError(f"Invalid prompt file format: {prompt_file}")

        # Add strategy name if not in file
        if "strategy_name" not in prompt_data:
            prompt_data["strategy_name"] = strategy_name

        # Pydantic validates structure, types, and required fields
        return PromptTemplate(**prompt_data)

    def load_all_prompts(self) -> dict[str, PromptTemplate]:
        """
        Load all available prompt strategies as PromptTemplate instances.

        Returns:
            Dictionary mapping strategy name to PromptTemplate
        """
        prompts = {}
        for prompt_file in self.prompts_dir.glob("*.yaml"):
            strategy_name = prompt_file.stem
            prompts[strategy_name] = self.load_prompt(strategy_name)
        return prompts

    def get_available_prompts(self) -> list[str]:
        """Get list of available prompt strategy names."""
        return [f.stem for f in self.prompts_dir.glob("*.yaml")]
