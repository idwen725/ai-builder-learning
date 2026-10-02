import requests
import logging
import time
import json
from config import Config
class AIClient:
    def __init__(self):
        self.url = Config.URL
        self.model = Config.MODEL
        self.timeout = Config.TIMEOUT
    def ask(self, history):
        start=time.time()
        data = {
            "model": self.model,
            "messages": history,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data,timeout=self.timeout)
            response.raise_for_status()
            cost=time.time()-start
            logging.info(f"AI请求成功，耗时{cost:.2f}秒")
            return response.json()["message"]["content"]
        except Exception as e:
            logging.error(f"AI请求失败{e}")
            return "AI暂时无法响应"

    def ask_stream(self, history):

        start = time.time()

        data = {
            "model": self.model,
            "messages": history,
            "stream": True
        }

        try:

            response = requests.post(
                self.url,
                json=data,
                timeout=self.timeout,
                stream=True
            )

            response.raise_for_status()

            for line in response.iter_lines():

                if line:
                    chunk = json.loads(
                        line.decode("utf-8")
                    )

                    yield chunk["message"]["content"]

            cost = time.time() - start

            logging.info(
                f"AI流式请求完成，耗时{cost:.2f}秒"
            )


        except Exception as e:

            logging.error(
                f"AI流式请求失败:{e}"
            )