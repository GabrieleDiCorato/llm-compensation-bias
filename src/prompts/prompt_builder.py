"""
Prompt builder for formatting prompt templates with code snippets.
"""

import inspect
import logging
from typing import Any

from ..compensation_api.evaluator import CompensationEvaluator
from ..model.person import Person
from ..model.prompt import PromptTemplate, RenderedPrompt

logger = logging.getLogger(__name__)


class PromptBuilder:
    """
    Builds complete prompts from templates by substituting placeholders with code.

    This class extracts source code from Python classes and protocols, then
    substitutes them into prompt templates to create final prompts for LLM connectors.
    """

    def build_prompt(self, template: PromptTemplate) -> RenderedPrompt:
        """
        Build a complete prompt from a template by substituting code placeholders.

        Args:
            template: The prompt template with placeholders

        Returns:
            RenderedPrompt: The prompt with all placeholders filled

        Example:
            >>> loader = PromptLoader()
            >>> template = loader.load_prompt("neutral")
            >>> builder = PromptBuilder()
            >>> rendered = builder.build_prompt(template)
        """
        logger.debug(f"Building prompt for strategy: {template.strategy_name}")

        # Extract entire person.py file (includes all Enums and the Person class)
        person_code = self._extract_module_code(Person)
        # Extract just the CompensationEvaluator protocol
        evaluator_code = self._extract_source_code(CompensationEvaluator)

        logger.debug(f"Extracted person.py module: {len(person_code)} characters")
        logger.debug(f"Extracted CompensationEvaluator code: {len(evaluator_code)} characters")

        # Escape curly braces in the code by doubling them for .format()
        # This prevents Python f-strings in the code from being interpreted as format placeholders
        person_code_escaped = person_code.replace("{", "{{").replace("}", "}}")
        evaluator_code_escaped = evaluator_code.replace("{", "{{").replace("}", "}}")

        substitutions = {
            "person_code": person_code_escaped,
            "evaluator_code": evaluator_code_escaped,
        }

        system_prompt = template.system_prompt.format(**substitutions)
        user_prompt = template.user_prompt.format(**substitutions)

        # This also validates that no placeholders remain
        rendered = RenderedPrompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            strategy_name=template.strategy_name,
            description=template.description,
            version=template.version,
        )

        logger.info(f"Successfully built prompt for strategy: {template.strategy_name}")
        logger.debug(f"System prompt length: {len(system_prompt)} characters")
        logger.debug(f"User prompt length: {len(user_prompt)} characters")

        return rendered

    def _extract_source_code(self, cls: type[Any]) -> str:
        """
        Extract the source code of a class or protocol.
        """
        return inspect.getsource(cls)

    def _extract_module_code(self, cls: type[Any]) -> str:
        """
        Extract the entire source file of the module containing a class.

        This is useful for including all related Enums, constants, and supporting
        code that provide context for the main class.

        Args:
            cls: A class whose module source should be extracted

        Returns:
            Complete source code of the module file
        """
        module = inspect.getmodule(cls)
        if module is None:
            logger.warning(f"Could not find module for {cls.__name__}, falling back to class source")
            return inspect.getsource(cls)

        module_file = inspect.getsourcefile(module)
        if module_file is None:
            logger.warning(f"Could not find source file for module {module.__name__}, falling back to class source")
            return inspect.getsource(cls)

        logger.debug(f"Reading entire module file: {module_file}")
        with open(module_file, encoding="utf-8") as f:
            return f.read()
