import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    MODEL = os.getenv("MODEL", "qwen3:4b")
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    URL = os.getenv("URL")
    CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT","5"))
    READ_TIMEOUT = int(os.getenv("READ_TIMEOUT","30"))
    CONTEXT_CHAR_BUDGET = int(os.getenv("CONTEXT_CHAR_BUDGET","1000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    @classmethod
    def validate(cls):
        if not cls.MODEL:
            raise ValueError("模型名称错误")
        if not cls.URL:
            raise ValueError("URL错误")
        if cls.MAX_RETRIES <=0 :
            raise ValueError("MAX_RETRIES不能小于0")
        if cls.CONNECT_TIMEOUT <=0 :
            raise ValueError("CONNECT_TIMEOUT不能小于0")
        if cls.READ_TIMEOUT <=0 :
            raise ValueError("READ_TIMEOUT不能小于0")
        if cls.CONTEXT_CHAR_BUDGET <=0 :
            raise ValueError("CONTEXT_CHAR_BUDGET不能小于0")
        if not cls.LOG_LEVEL:
            raise ValueError("LOG等级错误")