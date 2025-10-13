"""
Centralized logging configuration for the LLM compensation bias project.

This module provides a standardized logging setup with:
- Console and file handlers
- Structured log formatting
- Different log levels for different components
- Sanitization of sensitive data (API keys, tokens)
"""

import logging
import sys
from pathlib import Path
from typing import Any


class SensitiveDataFilter(logging.Filter):
    """Filter that sanitizes sensitive data from log messages."""

    SENSITIVE_PATTERNS = [
        "Bearer ",
        "token",
        "api_key",
        "password",
        "secret",
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """Sanitize sensitive data in log messages."""
        if hasattr(record, "msg"):
            msg = str(record.msg)
            for pattern in self.SENSITIVE_PATTERNS:
                if pattern.lower() in msg.lower():
                    record.msg = self._sanitize_message(msg)
        return True

    def _sanitize_message(self, msg: str) -> str:
        """Replace sensitive data with asterisks."""
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern.lower() in msg.lower():
                return msg[:50] + "..." if len(msg) > 50 else msg
        return msg


def setup_logging(
    log_level: str = "INFO",
    log_file: str | None = None,
    enable_console: bool = True,
) -> None:
    """
    Configure logging for the entire application.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, logs only to console
        enable_console: Whether to enable console logging
    """
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(SensitiveDataFilter())
        root_logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(SensitiveDataFilter())
        root_logger.addHandler(file_handler)

    # Set specific log levels for third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    root_logger.info(f"Logging initialized at level {log_level}")
    if log_file:
        root_logger.info(f"Logging to file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the logger (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
