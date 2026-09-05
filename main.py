import logger
from ai_client import AIClient
client = AIClient()
history=[]
while True:
    prompt=input("你：")
    if prompt=="退出":
        print("再见")
        break
    else:
        history.append("用户："+prompt)
        answer = client.ask(history)
        history.append( "AI："+answer)
        print("AI："+answer)