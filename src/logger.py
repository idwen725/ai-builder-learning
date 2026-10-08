import os
import logging
from logging.handlers import RotatingFileHandler
from config import Config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")
def setup_logging():
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper()),
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            RotatingFileHandler(
                LOG_FILE,
                maxBytes=1024 * 1024,
                backupCount=3,
                encoding="utf-8"
            )
        ]
    )