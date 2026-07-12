from datetime import datetime
from path_config import LOGS_FOLDER_PATH
from loguru import logger


LOGS_FOLDER_PATH.mkdir(exist_ok=True)
logger.remove()

logger.add(
    LOGS_FOLDER_PATH / datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    rotation="10 MB",
    retention="14 days",
    enqueue=True,
    level="INFO",
)

logger.add(
    lambda msg: print(msg, end=""),
    level="INFO",
)

__all__ = ["logger"]