import requests
url="http://localhost:11434/api/generate"
def ask_ai(history):
    data={
        "model":"qwen3:4b",
        "prompt":"\n".join(history),
        "stream":False
    }
    response=requests.post(url,json=data)
    response.raise_for_status()
    return response.json()["response"]