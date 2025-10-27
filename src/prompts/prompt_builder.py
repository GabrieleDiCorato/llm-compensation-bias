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

    def __init__(self) -> None:
        # Extract entire person.py file (includes all Enums and the Person class)
        self.person_code = self._extract_module_code(Person)
        # Extract just the CompensationEvaluator protocol
        self.evaluator_code = self._extract_source_code(CompensationEvaluator)

        logger.info(f"Extracted person.py module: {len(self.person_code)} characters")
        logger.info(f"Extracted CompensationEvaluator code: {len(self.evaluator_code)} characters")

        # Escape curly braces in the code by doubling them for .format()
        # This prevents Python f-strings in the code from being interpreted as format placeholders
        person_code_escaped = self.person_code.replace("{", "{{").replace("}", "}}")
        evaluator_code_escaped = self.evaluator_code.replace("{", "{{").replace("}", "}}")

        self.substitutions = {
            "person_code": person_code_escaped,
            "evaluator_code": evaluator_code_escaped,
        }
        logger.debug("Completed code extraction and escaping for prompt substitutions.")

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

        system_prompt = template.system_prompt.format(**self.substitutions)
        user_prompt = template.user_prompt.format(**self.substitutions)

        # This also validates that no placeholders remain
        rendered = RenderedPrompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            strategy_name=template.strategy_name,
            description=template.description,
            version=template.version,
        )

        logger.info(f"Successfully built prompt for strategy: {template.strategy_name}")

        # Estimate token usage with different rates for natural language vs code
        # Natural language (template text): ~1 token per 4 chars
        # Code (person.py + evaluator.py): ~1 token per 2.5 chars (code is more dense)
        template_chars = len(template.system_prompt) + len(template.user_prompt)
        code_chars = len(self.person_code) + len(self.evaluator_code)

        template_tokens = template_chars // 4
        code_tokens = code_chars // 2.5
        estimated_total_tokens = int(template_tokens + code_tokens)

        logger.debug(f"System prompt length: {len(system_prompt)} characters")
        logger.debug(f"User prompt length: {len(user_prompt)} characters")
        logger.debug(f"Estimated input tokens: ~{estimated_total_tokens} " f"(~{template_tokens} from template, ~{int(code_tokens)} from code)")

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
