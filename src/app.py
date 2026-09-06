import memory
from ai_client import AIClient
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
                self.history.append("用户：" + prompt)
                answer = self.client.ask(self.history)
                self.history.append("AI：" + answer)
                memory.save_memory(self.history)
                print("AI：" + answer)
