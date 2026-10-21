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
        self.api_key = Config.API_KEY
        self.user_agent = Config.USER_AGENT
        self.session = requests.Session()
        self.session.headers.update(self._build_headers())
    def _build_headers(self):
        headers = {
            "User-Agent": self.user_agent
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    def _to_api_messages(self, history):
        result = []
        for item in history:
            result.append({
                "role": item["role"],
                "content": item["content"]
            })
        return result
    def _handle_retry(
            self,
            request_id,
            attempt,
            max_retries,
            has_output,
            error,
            error_name
    ):
        if has_output:
            logging.error(
                f"request_id={request_id} | "
                f"AI流式请求已部分输出后发生{error_name}:{error}"
            )
            raise error

        if attempt == max_retries - 1:
            logging.error(
                f"request_id={request_id} | "
                f"AI发生{error_name}，已达到最大尝试次数:{error}"
            )
            raise error

        wait_time = 2 ** attempt

        logging.warning(
            f"request_id={request_id} | "
            f"AI发生{error_name}，"
            f"{wait_time}秒后进行第{attempt + 2}次尝试"
        )

        time.sleep(wait_time)

    def _handle_rate_limit(
            self,
            response,
            request_id,
            attempt,
            max_retries,
            has_output,
            error_name,
            error
    ):
        if has_output:
            logging.error(
                f"request_id={request_id} | "
                f"AI流式请求已部分输出后发生{error_name}:{error}"
            )
            raise error

        if attempt == max_retries - 1:
            logging.error(
                f"request_id={request_id} | "
                f"AI发生{error_name}，已达到最大尝试次数:{error}"
            )
            raise error

        retry_after = response.headers.get("Retry-After")
        if retry_after is not None:
            try:
                wait_time = int(retry_after)
            except ValueError:
                wait_time = 2 ** attempt
        else:
            wait_time = 2 ** attempt
        logging.warning(
            f"request_id={request_id} | "
            f"AI发生{error_name}，"
            f"{wait_time}秒后进行第{attempt + 2}次尝试"
        )
        time.sleep(wait_time)


    def ask_stream(self, history, request_id):
        max_retries = self.max_retries
        has_output = False
        for attempt in range(max_retries):
            start = time.time()
            messages = self._to_api_messages(history)
            data = {
                "model": self.model,
                "messages": messages,
                "stream": True
            }
            try:
                response = self.session.post(
                    self.url,
                    json=data,
                    timeout=(
                        self.connect_timeout,
                        self.read_timeout
                    ),
                    stream=True
                )
                status_code = response.status_code
                content_type = response.headers.get("content-type")
                logging.info(
                    f"request_id={request_id} | "
                    f"user_agent={self.session.headers.get("User-Agent")} | "
                    f"has_authorization={"Authorization" in self.session.headers} | "
                    f"status_code={status_code} | "
                    f"content_type={content_type}"
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
                    f"request_id={request_id} | "
                    f"AI流式请求完成，耗时{cost:.2f}秒"
                )
                return
            except requests.exceptions.Timeout as e:
                self._handle_retry(
                    request_id,
                    attempt,
                    max_retries,
                    has_output,
                    e,
                    "Timeout"
                )
                continue
            except requests.exceptions.ConnectionError as e:
                self._handle_retry(
                    request_id,
                    attempt,
                    max_retries,
                    has_output,
                    e,
                    "ConnectionError"
                )
                continue
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 429:
                    self._handle_rate_limit(
                        e.response,
                        request_id,
                        attempt,
                        max_retries,
                        has_output,
                        "HTTP 429",
                        e
                    )
                    continue
                elif 500 <= status_code < 600:
                    self._handle_retry(
                        request_id,
                        attempt,
                        max_retries,
                        has_output,
                        e,
                        f"HTTP {status_code}"
                    )
                    continue
                else:
                    logging.error(
                        f"request_id={request_id} | "
                        f"AI流式请求失败:{e}"
                    )
                    raise
            except json.JSONDecodeError as e:
                logging.error(
                    f"request_id={request_id} | "
                    f"AI流式请求失败:{e}"
                )
                raise
            except Exception as e:
                logging.error(
                    f"request_id={request_id} | "
                    f"AI流式请求失败:{e}"
                )
                raise