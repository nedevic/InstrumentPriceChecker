import logging
import sys

__all__ = ["logger"]


LOGGING_FORMAT = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setFormatter(LOGGING_FORMAT)
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename=".log")
file_handler.setFormatter(LOGGING_FORMAT)
file_handler.setLevel(logging.INFO)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
