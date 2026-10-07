import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    MODEL = os.getenv("MODEL")
    URL = os.getenv("URL")
    CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT"))
    READ_TIMEOUT = int(os.getenv("READ_TIMEOUT"))