import sys

from loguru import logger

logger.add("logs.log", format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add(sys.stderr, level="INFO")
