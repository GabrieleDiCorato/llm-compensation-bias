"""
Prompt loader for loading prompt templates from YAML files.

Prompt files must have the suffix '*.prompt.yml'.
"""

from pathlib import Path
import yaml
import logging
from ..model.prompt import PromptTemplate

logger = logging.getLogger(__name__)

prompt_suffix = ".prompt.yml"

class PromptLoader:
    """Loads and validates prompt templates from '*.prompt.yml' files."""

    def __init__(self, prompts_directory: str = "settings/prompts"):
        """
        Initialize prompt loader.

        Args:
            prompts_directory: Path to directory containing '*.prompt.yml' files
        """
        self.prompts_dir = Path(prompts_directory)
        logger.info(f"PromptLoader initialized with directory: {self.prompts_dir}")

    def load_prompt(self, strategy_name: str) -> PromptTemplate:
        """
    Load a prompt strategy from its '*.prompt.yml' file as a validated PromptTemplate.

        Args:
            strategy_name: Name of the prompt strategy (e.g., 'neutral', 'fair')

        Returns:
            PromptTemplate instance with type-safe access and validation

        Raises:
            FileNotFoundError: If prompt file doesn't exist
            ValidationError: If prompt file structure is invalid (via Pydantic)
        """
        prompt_file = self.prompts_dir / f"{strategy_name}{prompt_suffix}"
        logger.debug(f"Loading prompt strategy: {strategy_name} from {prompt_file}")

        if not prompt_file.exists():
            logger.error(f"Prompt file not found: {prompt_file}")
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt_data = yaml.safe_load(f)

        if not isinstance(prompt_data, dict):
            logger.error(f"Invalid prompt file format: {prompt_file}")
            raise ValueError(f"Invalid prompt file format: {prompt_file}")

        # Add strategy name if not in file
        if "strategy_name" not in prompt_data:
            prompt_data["strategy_name"] = strategy_name

        # Pydantic validates structure, types, and required fields
        template = PromptTemplate(**prompt_data)
        logger.info(f"Successfully loaded prompt strategy: {strategy_name}")
        return template

    def load_all_prompts(self) -> dict[str, PromptTemplate]:
        """
        Load all available prompt strategies as PromptTemplate instances.

        Returns:
            Dictionary mapping strategy name to PromptTemplate
        """
        logger.info("Loading all available prompt strategies")
        prompts = {}
        for prompt_file in self.prompts_dir.glob(f"*{prompt_suffix}"):
            strategy_name = prompt_file.stem
            prompts[strategy_name] = self.load_prompt(strategy_name)
        logger.info(f"Loaded {len(prompts)} prompt strategies: {', '.join(prompts.keys())}")
        return prompts

    def get_available_prompts(self) -> list[str]:
        """Get list of available prompt strategy names."""
        available = [f.stem for f in self.prompts_dir.glob(f"*{prompt_suffix}")]
        logger.debug(f"Available prompt strategies: {', '.join(available)}")
        return available
