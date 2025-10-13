"""
Root package for the LLM compensation bias research project.
"""

from .logging_config import setup_logging, get_logger

__version__ = "0.1.0"

__all__ = ["setup_logging", "get_logger", "__version__"]
