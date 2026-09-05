import logger
import memory
from ai_client import AIClient
client = AIClient()
history=memory.load_memory()
while True:
    prompt=input("你：")
    if prompt=="退出":
        print("再见")
        break
    else:
        history.append("用户："+prompt)
        memory.save_memory(history)
        answer = client.ask(history)
        history.append( "AI："+answer)
        memory.save_memory(history)
        print("AI："+answer)