import requests
import config
import logging
class AIClient:
    def __init__(self):
        self.url = config.URL
        self.model = config.MODEL
    def ask(self, history):
        data = {
            "model": self.model,
            "prompt": "\n".join(history),
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data,timeout=30)
            response.raise_for_status()
            logging.info("AI请求成功")
            return response.json()["response"]
        except Exception as e:
            logging.error(f"AI请求失败{e}")
            return "AI暂时无法响应"