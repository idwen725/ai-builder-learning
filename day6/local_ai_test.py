import requests
url="http://localhost:11434/api/generate"
print("================")
print("你：")
history=[]
while True:
    prompt=input()
    if prompt == "退出":
        print("再见")
        break
    else:
        history.append("用户：" + prompt)
        data = {
            "model": "qwen3:4b",
            "prompt": "\n".join(history),
            "stream": False
        }
        ai_response=requests.post(url, json=data)
        ai_response.raise_for_status()
        answer=ai_response.json()
        history.append("AI：" + answer["response"])
        print(answer["response"])
        print("================")
        print("你：")