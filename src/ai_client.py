import requests
import logging
import time
import json
from config import Config
class AIClient:
    def __init__(self):
        self.url = Config.URL
        self.model = Config.MODEL
        self.connect_timeout = Config.CONNECT_TIMEOUT
        self.read_timeout = Config.READ_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
    def ask(self, history):
        start=time.time()
        data = {
            "model": self.model,
            "messages": history,
            "stream": False
        }
        try:
            response = requests.post(self.url, json=data,timeout=(
                self.connect_timeout,
                self.read_timeout
            ))
            response.raise_for_status()
            cost=time.time()-start
            logging.info(f"AI请求成功，耗时{cost:.2f}秒")
            return response.json()["message"]["content"]
        except Exception as e:
            logging.error(f"AI请求失败{e}")
            return "AI暂时无法响应"

    def ask_stream(self, history):
        max_retries = self.max_retries
        has_output = False
        for attempt in range(max_retries):
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
                    timeout=(
                        self.connect_timeout,
                        self.read_timeout
                    ),
                    stream=True
                )
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(
                            line.decode("utf-8")
                        )
                        has_output = True
                        yield chunk["message"]["content"]
                cost = time.time() - start
                logging.info(
                    f"AI流式请求完成，耗时{cost:.2f}秒"
                )
                return
            except Exception as e:
                if has_output:
                    logging.error(
                        f"AI流式请求失败:{e}"
                    )
                    raise
                elif attempt == max_retries - 1:
                    logging.error(
                        f"AI流式请求失败:{e}"
                    )
                    raise
                else:
                    time.sleep(2**attempt)
                    logging.warning(f"AI请求失败，准备第{attempt + 2}次尝试")
                    continue
