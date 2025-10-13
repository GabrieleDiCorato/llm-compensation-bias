"""
Prompt builder for formatting prompt templates with code snippets.
"""

import inspect
from typing import Any
from ..model.prompt import PromptTemplate, RenderedPrompt
from ..model.person import Person
from ..compensation_api.evaluator import CompensationEvaluator


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
        person_code = self._extract_source_code(Person)
        evaluator_code = self._extract_source_code(CompensationEvaluator)
        
        substitutions = {
            "person_code": person_code,
            "evaluator_code": evaluator_code,
        }
        
        system_prompt = template.system_prompt.format(**substitutions)
        user_prompt = template.user_prompt.format(**substitutions)
        
        # This also validates that no placeholders remain
        return RenderedPrompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            strategy_name=template.strategy_name,
            description=template.description,
            version=template.version,
            provider_settings=template.provider_settings,
        )

    def _extract_source_code(self, cls: type[Any]) -> str:
        """
        Extract the source code of a class or protocol.
        """
        return inspect.getsource(cls)
