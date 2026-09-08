import requests
import logging
import time
from config import Config
class AIClient:
    def __init__(self):
        self.url = Config.URL
        self.model = Config.MODEL
        self.timeout = Config.TIMEOUT
    def ask(self, history):
        start=time.time()
        messages = []
        for item in history:
            messages.append(
                item["role"]+":"+item["content"]
            )
        prompt="\n".join(messages)
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data,timeout=self.timeout)
            response.raise_for_status()
            cost=time.time()-start
            logging.info(f"AI请求成功，耗时{cost:.2f}秒")
            return response.json()["response"]
        except Exception as e:
            logging.error(f"AI请求失败{e}")
            return "AI暂时无法响应"