import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Get a configured logger instance with the specified name.

    Args:
        name: The name of the logger (typically __name__)
        level: Optional logging level (defaults to INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if handlers haven't been set up yet
    if not logger.handlers:
        logger.setLevel(level or logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(console_handler)

        # Prevent propagation to root logger to avoid duplicate messages
        logger.propagate = False

    return logger
