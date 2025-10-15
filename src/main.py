"""
Main entry point for the LLM Compensation Bias research project.

This script orchestrates the entire experiment:
1. Sets up logging and loads configuration
2. For each enabled model, creates a connector
3. For each prompt strategy, generates and validates code implementations
4. Saves all implementations and metadata for analysis

Usage:
    python -m src.main

Configuration is controlled via:
    - settings/config.yaml (models, strategies, output paths)
    - settings/secrets.env (API keys)
    - settings/prompts/*.prompt.yml (prompt templates; each strategy must have a corresponding '*.prompt.yml' file)
"""

import sys
from datetime import datetime
from pathlib import Path

from src.logging_config import setup_logging, get_logger
from src.settings.settings_model import LlmSettings, SecretSettings
from src.llm_connection.connector_factory import create_connector
from src.llm_connection.response_handler import ResponseHandler, CodeValidationError
from src.prompts.prompt_loader import PromptLoader
from src.prompts.prompt_builder import PromptBuilder

logger = get_logger(__name__)


class ExperimentRunner:
    """Orchestrates the LLM bias experiment across models and prompt strategies."""

    def __init__(
        self,
        settings: LlmSettings,
        secrets: SecretSettings,
        response_handler: ResponseHandler,
        prompt_loader: PromptLoader,
        prompt_builder: PromptBuilder,
    ):
        """
        Initialize the experiment runner.

        Args:
            settings: LLM configuration settings
            secrets: API keys and secrets
            response_handler: Handler for processing LLM responses
            prompt_loader: Loader for prompt templates
            prompt_builder: Builder for rendering prompts with code
        """
        self.settings = settings
        self.secrets = secrets
        self.response_handler = response_handler
        self.prompt_loader = prompt_loader
        self.prompt_builder = prompt_builder

        self.stats = {
            "total_experiments": 0,
            "successful": 0,
            "failed_validation": 0,
            "failed_generation": 0,
            "models_tested": set(),
            "strategies_tested": set(),
        }

    def run_single_experiment(
        self,
        model_id: str,
        strategy_name: str,
    ) -> bool:
        """
        Run a single experiment: query model with strategy and save result.

        Args:
            model_id: Model identifier (e.g., 'openai/gpt-4.1')
            strategy_name: Prompt strategy name (e.g., 'neutral')

        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Starting experiment: model={model_id}, strategy={strategy_name}")

        try:
            # Load and build prompt
            logger.info(f"Loading prompt strategy: {strategy_name}")
            template = self.prompt_loader.load_prompt(strategy_name)
            prompt = self.prompt_builder.build_prompt(template)

            # Create connector
            logger.info(f"Creating connector for model: {model_id}")
            
            # Extract provider from model settings
            model_cfg = next(
                (m for m in self.settings.models_settings if m.model_id == model_id),
                None
            )
            if not model_cfg:
                logger.error(f"Model {model_id} not found in settings")
                return False
            
            provider_id = model_cfg.provider
            connector = create_connector(model_id, self.settings, self.secrets)

            # Query the model
            logger.info(f"Querying model: {model_id}")
            response = connector.query(prompt, provider_id, model_id)

            logger.info(
                f"Received response: {len(response.content)} characters, "
                f"{response.tokens_used or 'unknown'} tokens"
            )

            # Process and save response
            logger.info("Processing and saving response")
            code_path, metadata_path = self.response_handler.process_response(
                response=response,
                prompt=prompt,
                model_id=model_id,
                provider_id=provider_id,
            )

            logger.info(f"Experiment successful: {code_path.name}")
            self.stats["successful"] += 1
            return True

        except CodeValidationError as e:
            logger.warning(f"Code validation failed: {e}")
            self.stats["failed_validation"] += 1
            return False

        except Exception as e:
            logger.error(f"Experiment failed with error: {e}", exc_info=True)
            self.stats["failed_generation"] += 1
            return False

    def run_for_model(self, model_id: str, strategies: list[str]) -> dict[str, bool]:
        """
        Run experiments for a single model across all specified strategies.

        Args:
            model_id: Model identifier
            strategies: List of prompt strategy names

        Returns:
            Dictionary mapping strategy name to success status
        """
        logger.info(f"Running experiments for model: {model_id}")
        logger.info(f"Strategies to test: {', '.join(strategies)}")

        results = {}
        for strategy_name in strategies:
            self.stats["total_experiments"] += 1
            self.stats["models_tested"].add(model_id)
            self.stats["strategies_tested"].add(strategy_name)

            success = self.run_single_experiment(model_id, strategy_name)
            results[strategy_name] = success

            if success:
                logger.info(f"Completed: {model_id} x {strategy_name}")
            else:
                logger.warning(f"Failed: {model_id} x {strategy_name}")

        return results

    def run_all(
        self,
        models: list[str] | None = None,
        strategies: list[str] | None = None,
    ) -> dict[str, dict[str, bool]]:
        """
        Run experiments for all specified models and strategies.

        Args:
            models: List of model IDs to test (defaults to all enabled models)
            strategies: List of strategies to test (defaults to all configured strategies)

        Returns:
            Nested dictionary: {model_id: {strategy_name: success}}
        """
        # Use configured values if not specified
        models = models or self.settings.enabled_models
        strategies = strategies or self.settings.prompt_strategies

        logger.info("Starting experiment batch")
        logger.info(f"Models: {', '.join(models)}")
        logger.info(f"Strategies: {', '.join(strategies)}")
        logger.info(f"Total experiments: {len(models) * len(strategies)}")

        all_results = {}

        for model_id in models:
            logger.info(f"Processing model {model_id}")
            model_results = self.run_for_model(model_id, strategies)
            all_results[model_id] = model_results

        return all_results

    def print_summary(self) -> None:
        """Print experiment summary statistics."""
        logger.info("=" * 60)
        logger.info("Experiment Summary:")
        logger.info(f"  Total experiments: {self.stats['total_experiments']}")
        logger.info(f"  Successful: {self.stats['successful']}")
        logger.info(f"  Failed (validation): {self.stats['failed_validation']}")
        logger.info(f"  Failed (generation): {self.stats['failed_generation']}")
        logger.info(f"  Models tested: {len(self.stats['models_tested'])}")
        logger.info(f"  Strategies tested: {len(self.stats['strategies_tested'])}")

        if self.stats["total_experiments"] > 0:
            success_rate = (
                self.stats["successful"] / self.stats["total_experiments"] * 100
            )
            logger.info(f"  Success rate: {success_rate:.1f}%")
        logger.info("=" * 60)


def load_settings() -> tuple[LlmSettings, SecretSettings]:
    """
    Load configuration and secrets from default locations.

    Returns:
        Tuple of (LlmSettings, SecretSettings)

    Raises:
        FileNotFoundError: If configuration or secrets files are missing
    """
    config_path = "settings/config.yaml"
    secrets_path = "settings/secrets.env"

    logger.info("Loading configuration")
    logger.debug(f"Config file: {config_path}")
    logger.debug(f"Secrets file: {secrets_path}")

    # Check if files exist
    if not Path(config_path).exists():
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    if not Path(secrets_path).exists():
        logger.error(f"Secrets file not found: {secrets_path}")
        raise FileNotFoundError(f"Secrets file not found: {secrets_path}")

    # Load settings - Pydantic will automatically load from YAML via YamlConfigSettingsSource
    settings = LlmSettings()
    secrets = SecretSettings(_env_file=secrets_path)

    logger.info("Configuration loaded successfully")
    return settings, secrets


def main() -> int:
    """
    Main entry point for the experiment.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    start_time = datetime.now()

    # Setup logging with both console and file output
    log_filename = f"logs/experiment_{start_time.strftime('%Y%m%d_%H%M%S')}.log"
    setup_logging(log_level="DEBUG", log_file=log_filename)

    logger.info("LLM Compensation Bias Experiment")
    logger.info(f"Start time: {start_time.isoformat()}")
    logger.info("-" * 60)

    try:
        # Load configuration
        settings, secrets = load_settings()

        # Show what will be run
        logger.info("Experiment Configuration:")
        logger.info(f"  Models: {', '.join(settings.enabled_models)}")
        logger.info(f"  Strategies: {', '.join(settings.prompt_strategies)}")
        logger.info(f"  Total experiments: {len(settings.enabled_models) * len(settings.prompt_strategies)}")
        logger.info(f"  Output directory: {settings.output_dir}")
        logger.info("-" * 60)

        # Initialize components
        logger.info("Initializing experiment components")
        response_handler = ResponseHandler(settings.output_dir)
        prompt_loader = PromptLoader(settings.prompt_directory)
        prompt_builder = PromptBuilder()

        # Create experiment runner
        runner = ExperimentRunner(
            settings=settings,
            secrets=secrets,
            response_handler=response_handler,
            prompt_loader=prompt_loader,
            prompt_builder=prompt_builder,
        )

        # Run experiments
        logger.info("Starting experiments")
        logger.info("=" * 60)
        results = runner.run_all()
        logger.info("=" * 60)

        # Print summary
        runner.print_summary()

        # Calculate duration
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"End time: {end_time.isoformat()}")
        logger.info(f"Total duration: {duration}")

        # Return success if at least some experiments succeeded
        if runner.stats["successful"] > 0:
            logger.info("Experiment completed successfully")
            return 0
        else:
            logger.error("All experiments failed")
            return 1

    except KeyboardInterrupt:
        logger.warning("Experiment interrupted by user")
        return 130  # Standard exit code for SIGINT

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
