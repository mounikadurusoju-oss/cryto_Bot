"""Logging configuration for the trading bot."""
import logging
import os

LOG_FILE = "trading.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.INFO


def setup_logging() -> None:
    """Configure the root logger for file output."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=LOG_LEVEL,
        format=LOG_FORMAT,
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the specified module.

    Args:
        name: The name for the logger (typically __name__).

    Returns:
        A configured logger instance.
    """
    setup_logging()
    return logging.getLogger(name)
