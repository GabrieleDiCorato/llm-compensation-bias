from pathlib import Path
import yaml
from enum import Enum

class PromptStrategy(str, Enum):
    NEUTRAL = "neutral"
    FAIR = "fair"
    REALISTIC = "realistic"

class PromptLoader:
    """Loads prompt templates from YAML files."""

    def __init__(self, prompts_directory: str = "settings/prompts"):
        self.prompts_dir = Path(prompts_directory)

    def load_prompt(self, strategy_name: PromptStrategy) -> dict[str, str]:
        """
        Load a prompt strategy from its YAML file.

        Args:
            strategy_name: Name of the prompt strategy (e.g., 'neutral', 'fair')

        Returns:
            Dictionary with 'system_prompt' and 'user_prompt' keys

        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValueError: If prompt file is invalid
        """
        prompt_file = self.prompts_dir / f"{strategy_name}.yaml"

        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_data = yaml.safe_load(f)

        if not isinstance(prompt_data, dict):
            raise ValueError(f"Invalid prompt file format: {prompt_file}")

        required_keys = {"system_prompt", "user_prompt"}
        if not required_keys.issubset(prompt_data.keys()):
            raise ValueError(f"Prompt file missing required keys {required_keys}: {prompt_file}")

        return {
            "system_prompt": prompt_data["system_prompt"],
            "user_prompt": prompt_data["user_prompt"],
        }

    def load_all_prompts(self, strategy_names: list[PromptStrategy]) -> dict[str, dict[str, str]]:
        """
        Load multiple prompt strategies.

        Args:
            strategy_names: List of strategy names to load

        Returns:
            Dictionary mapping strategy name to prompt data
        """
        return {name: self.load_prompt(name) for name in strategy_names}
