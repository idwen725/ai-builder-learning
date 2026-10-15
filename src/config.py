import os
from dotenv import load_dotenv
load_dotenv()
def _parse_int(name, default):
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError:
        raise ValueError(f"{name}必须是整数")
    return value
class Config:
    MODEL = os.getenv("MODEL", "qwen3:4b")
    MAX_RETRIES = _parse_int("MAX_RETRIES", 3)
    URL = os.getenv("URL")
    CONNECT_TIMEOUT = _parse_int("CONNECT_TIMEOUT", 5)
    READ_TIMEOUT = _parse_int("READ_TIMEOUT", 30)
    CONTEXT_CHAR_BUDGET = _parse_int("CONTEXT_CHAR_BUDGET", 1000)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    @classmethod
    def validate(cls):
        if not cls.MODEL:
            raise ValueError("模型名称错误")
        if not cls.URL:
            raise ValueError("URL错误")
        if cls.MAX_RETRIES <=0 :
            raise ValueError("MAX_RETRIES必须大于0")
        if cls.CONNECT_TIMEOUT <=0 :
            raise ValueError("CONNECT_TIMEOUT必须大于0")
        if cls.READ_TIMEOUT <=0 :
            raise ValueError("READ_TIMEOUT必须大于0")
        if cls.CONTEXT_CHAR_BUDGET <=0 :
            raise ValueError("CONTEXT_CHAR_BUDGET必须大于0")
        valid_log_levels = {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL"
        }
        if cls.LOG_LEVEL.upper() not in valid_log_levels:
            raise ValueError("LOG等级错误")