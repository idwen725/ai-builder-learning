import time
import requests

from ai_client import AIClient


class FakeResponse:
    def __init__(self):
        self.headers = {
            "Retry-After": "10"
        }


client = AIClient()

fake_response = FakeResponse()

fake_error = requests.exceptions.HTTPError(
    "Synthetic HTTP 429"
)

operation_start = time.time() - 1.5

client._handle_rate_limit(
    response=fake_response,
    request_id="test-429-deadline",
    attempt=0,
    max_retries=5,
    has_output=False,
    error_name="HTTP 429",
    error=fake_error,
    operation_start=operation_start
)