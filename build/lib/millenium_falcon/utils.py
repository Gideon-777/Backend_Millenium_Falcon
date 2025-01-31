import sys

from loguru import logger


def set_loglevel(LOG_LEVEL):
    logger.remove()
    logger.add(sys.stderr, level=LOG_LEVEL)
    logger.info(f"Logging is set at {LOG_LEVEL}")
