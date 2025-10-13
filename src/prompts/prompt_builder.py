"""
Prompt builder for formatting prompt templates with code snippets.
"""

import inspect
from typing import Any
from ..model.prompt import PromptTemplate
from ..model.person import Person
from ..compensation_api.evaluator import CompensationEvaluator


class PromptBuilder:
    """
    Builds complete prompts from templates by substituting placeholders with code.
    
    This class extracts source code from Python classes and protocols, then
    substitutes them into prompt templates to create final prompts for LLM connectors.
    """

    def build_prompt(self, template: PromptTemplate) -> tuple[str, str]:
        """
        Build a complete prompt from a template by substituting code placeholders.
        
        Args:
            template: The prompt template with placeholders
            
        Returns:
            Tuple of (system_prompt, user_prompt) with placeholders replaced
            
        Example:
            >>> loader = PromptLoader()
            >>> template = loader.load_prompt("neutral")
            >>> builder = PromptBuilder()
            >>> system, user = builder.build_prompt(template)
        """
        person_code = self._extract_source_code(Person)
        evaluator_code = self._extract_source_code(CompensationEvaluator)
        
        substitutions = {
            "person_code": person_code,
            "evaluator_code": evaluator_code,
        }
        
        system_prompt = template.system_prompt.format(**substitutions)
        user_prompt = template.user_prompt.format(**substitutions)
        
        return (system_prompt, user_prompt)

    def _extract_source_code(self, cls: type[Any]) -> str:
        """
        Extract the source code of a class or protocol.
        
        Args:
            cls: The class or protocol to extract source from
            
        Returns:
            String containing the complete source code
            
        Raises:
            OSError: If source code cannot be retrieved
        """
        return inspect.getsource(cls)
