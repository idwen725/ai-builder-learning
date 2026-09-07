import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    MODEL = os.getenv("MODEL")
    URL = os.getenv("URL")
    TIMEOUT = int(os.getenv("TIMEOUT"))