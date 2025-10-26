"""
Response handler for processing and saving LLM-generated code implementations.

This module provides functionality to:
- Validate Python syntax in LLM responses
- Generate appropriate filenames based on model, strategy, and timestamp
- Save code implementations and metadata separately
- Handle errors gracefully with detailed logging
"""

import ast
import json
import logging
from datetime import datetime
from pathlib import Path

from src.model.llm_response import LLMResponse
from src.model.prompt import RenderedPrompt

logger = logging.getLogger(__name__)


class CodeValidationError(Exception):
    """Raised when generated code fails validation."""

    pass


class ResponseHandler:
    """
    Handles LLM responses by validating, parsing, and saving generated code.

    This handler expects responses to contain pure, runnable Python code.
    It performs strict validation and saves both the code and metadata separately.
    """

    def __init__(self, output_dir: str = "src/auto_generated"):
        """
        Initialize the response handler.

        Args:
            output_dir: Base directory for saving generated code and metadata
        """
        self.output_dir = Path(output_dir)
        self.implementations_dir = self.output_dir / "implementations"
        self.metadata_dir = self.output_dir / "metadata"

        self._ensure_directories()

        logger.info(f"ResponseHandler initialized with output directory: {self.output_dir}")

    def _ensure_directories(self) -> None:
        """Create output directories if they don't exist."""
        self.implementations_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directories exist: {self.implementations_dir}, {self.metadata_dir}")

    def validate_python_syntax(self, code: str) -> None:
        """
        Validate that the code is syntactically correct Python.

        Args:
            code: Python code string to validate

        Raises:
            CodeValidationError: If code has syntax errors
        """
        try:
            ast.parse(code)
            logger.debug("Python syntax validation passed")
        except SyntaxError as e:
            logger.error(f"Syntax error in generated code: line {e.lineno}, {e.msg}")
            raise CodeValidationError(f"Generated code has syntax error at line {e.lineno}: {e.msg}") from e

    def generate_filename(
        self,
        model_id: str,
        strategy_name: str,
        prompt_version: str,
        timestamp: datetime | None = None,
    ) -> str:
        """
        Generate a filename for the implementation.

        Format: {model}_{strategy}_v{version}_{timestamp}.py

        Args:
            model_id: Full model identifier (e.g., 'openai/gpt-4.1')
            strategy_name: Prompt strategy name (e.g., 'neutral')
            prompt_version: Prompt version (e.g., '1.0')
            timestamp: Optional timestamp (defaults to now)

        Returns:
            Filename without extension
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Sanitize model_id: replace / and . with _
        safe_model = model_id.replace("/", "_").replace(".", "_")

        # Format timestamp
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")

        # Replace . in version with underscore
        safe_version = prompt_version.replace(".", "_")

        filename = f"{safe_model}_{strategy_name}_v{safe_version}_{timestamp_str}"

        logger.debug(f"Generated filename: {filename}")
        return filename

    def save_implementation(self, code: str, filename_base: str) -> Path:
        """
        Save the Python implementation to a file.

        Args:
            code: Python code to save
            filename_base: Base filename without extension

        Returns:
            Path to the saved file
        """
        filepath = self.implementations_dir / f"{filename_base}.py"

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code)
            logger.info(f"Saved implementation to: {filepath}")
            return filepath
        except OSError as e:
            logger.error(f"Failed to save implementation: {e}")
            raise

    def save_metadata(
        self,
        response: LLMResponse,
        prompt: RenderedPrompt,
        filename_base: str,
        model_id: str,
        provider_id: str,
        validation_passed: bool,
        error_message: str | None = None,
    ) -> Path:
        """
        Save metadata about the generation to a JSON file.

        Args:
            response: The LLM response object
            prompt: The rendered prompt used
            filename_base: Base filename (same as implementation)
            model_id: Model identifier
            provider_id: Provider identifier
            validation_passed: Whether code validation passed
            error_message: Optional error message if validation failed

        Returns:
            Path to the saved metadata file
        """
        filepath = self.metadata_dir / f"{filename_base}.json"

        metadata = {
            "generation_info": {
                "model_id": model_id,
                "provider_id": provider_id,
                "strategy_name": prompt.strategy_name,
                "prompt_version": prompt.version,
                "prompt_description": prompt.description,
                "generation_timestamp": datetime.now().isoformat(),
            },
            "request": response.request_payload,  # Full request payload for reproducibility
            "response": {
                "content": response.content,
                "model_id": response.model_id,
                "tokens_used": response.tokens_used,
                "finish_reason": response.finish_reason,
                "metadata": response.metadata,  # Provider-specific details
            },
            "prompts": {"system_prompt": prompt.system_prompt, "user_prompt": prompt.user_prompt},
            "validation": {"passed": validation_passed, "error_message": error_message},
        }

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved metadata to: {filepath}")
            return filepath
        except OSError as e:
            logger.error(f"Failed to save metadata: {e}")
            raise

    def process_response(self, response: LLMResponse, prompt: RenderedPrompt, model_id: str, provider_id: str) -> tuple[Path, Path]:
        """
        Process an LLM response: validate, save code, and save metadata.

        This is the main entry point for handling responses.

        Args:
            response: LLM response containing generated code
            prompt: The rendered prompt that was used
            model_id: Model identifier
            provider_id: Provider identifier

        Returns:
            Tuple of (code_path, metadata_path)

        Raises:
            CodeValidationError: If code validation fails
        """
        logger.info(f"Processing response from {model_id} using strategy '{prompt.strategy_name}'")

        code = response.content.strip()

        # Generate filename
        filename_base = self.generate_filename(
            model_id=model_id,
            strategy_name=prompt.strategy_name or "unknown",
            prompt_version=prompt.version or "0.0",
        )

        validation_passed = False
        error_message = None

        try:
            # Validate Python syntax
            logger.info("Validating Python syntax")
            self.validate_python_syntax(code)
            validation_passed = True

            # Save the implementation
            logger.info("Saving implementation")
            code_path = self.save_implementation(code, filename_base)

            # Save metadata
            logger.info("Saving metadata")
            metadata_path = self.save_metadata(
                response=response,
                prompt=prompt,
                filename_base=filename_base,
                model_id=model_id,
                provider_id=provider_id,
                validation_passed=validation_passed,
            )

            logger.info(f"Successfully processed response: {filename_base}")
            return code_path, metadata_path

        except CodeValidationError as e:
            error_message = str(e)
            logger.error(f"Code validation failed: {error_message}")

            # Save the raw response even though validation failed
            logger.info("Saving invalid code and metadata for analysis")

            # Save with .txt extension to indicate invalid code
            invalid_path = self.implementations_dir / f"{filename_base}_INVALID.txt"
            with open(invalid_path, "w", encoding="utf-8") as f:
                f.write(code)
            logger.info(f"Saved invalid code to: {invalid_path}")

            # Save metadata with error information
            metadata_path = self.save_metadata(
                response=response,
                prompt=prompt,
                filename_base=filename_base,
                model_id=model_id,
                provider_id=provider_id,
                validation_passed=False,
                error_message=error_message,
            )

            logger.error("Validation failed. Saved raw response and metadata.")
            raise
