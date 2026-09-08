import memory
from ai_client import AIClient
import datetime
class App:
    def __init__(self):
        self.client = AIClient()
        self.history = memory.load_memory()
    def run(self):
        while True:
            prompt = input("你：")
            if prompt == "退出":
                print("再见")
                break
            else:
                self.history.append(
                    {
                        "role":"user",
                        "content":prompt,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                answer = self.client.ask(self.history)
                self.history.append(
                    {
                        "role":"assistant",
                        "content":answer,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                memory.save_memory(self.history)
                print("AI：" + answer)
