import memory
from ai_client import AIClient
class App:
    def __init__(self):
        self.client = AIClient()
        self.history = memory.get_memory()
    def run(self):
        history = memory.load_memory()
        while True:
            prompt = input("你：")
            if prompt == "退出":
                print("再见")
                break
            else:
                history.append("用户：" + prompt)
                answer = self.client.ask(history)
                history.append("AI：" + answer)
                memory.save_memory(history)
                print("AI：" + answer)
