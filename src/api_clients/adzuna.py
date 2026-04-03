import os
from loguru import logger
from dotenv import load_dotenv


# Extract secret environment variables from .env file
ADZUNA_APP_ID = None
ADZUNA_API_KEY = None
try:
    load_dotenv()
    ADZUNA_APP_ID = os.environ.get("ADZUNA_APP_ID")
    ADZUNA_API_KEY = os.environ.get("ADZUNA_API_KEY")
except Exception:
    logger.exception("Unable to load ADZUNA secret credentials!")

