import logging
import sys

def setup_logger(level: int = logging.INFO) -> logging.Logger:
    """Configures a professional structured logger for enterprise Navix bots."""
    logger = logging.getLogger("navix")
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
