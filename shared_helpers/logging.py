import os
import sys

from loguru import logger

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# remove the default loguru logger (cannot change its level otherwise and stream)
logger.remove()
# separate channels might result in slightly out of order logs  ¯\_(ツ)_/¯
logger.add(sys.stdout, level=LOG_LEVEL, filter=lambda record: record["level"].name != "ERROR")
logger.add(sys.stderr, level="ERROR")
