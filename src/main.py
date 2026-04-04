from loguru import logger
from path_config import LOGS_FOLDER_PATH
from datetime import datetime
from src.utils.validate_config import  ValidateConfig
from config.common_config import config


try:
    cfg = ValidateConfig(**config)
    print(type(cfg))
    print(cfg)
    print(dict(cfg))
except Exception as e:
    logger.error("Config validation failed")
    raise e

exit()



# Log file setup
log_file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_job-aggregator-run.log"
log_file_path = str(LOGS_FOLDER_PATH / log_file_name)
logger.add(log_file_path, rotation="10 MB", level="INFO")

