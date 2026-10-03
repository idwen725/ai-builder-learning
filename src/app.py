import memory
from ai_client import AIClient
import datetime
class App:
    def __init__(self):
        self.client = AIClient()
        self.history = memory.load_memory()
        self.long_memory = memory.load_long_term_memory()
    def run(self):
        while True:
            prompt = input("你：")
            if prompt == "退出":
                print("再见")
                break
            elif prompt.startswith("/remember "):
                note = prompt[len("/remember "):]
                self.long_memory.append(note)
                memory.save_long_term_memory(self.long_memory)
                print("长期记忆已更新")
            elif prompt.startswith("/memory"):
                facts = self.long_memory
                for fact in facts:
                    print(fact)
            else:
                self.history.append(
                    {
                        "role":"user",
                        "content":prompt,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                context = memory.build_context(self.history, self.long_memory,10)
                print("AI：", end="")
                answer = ""
                for chunk in self.client.ask_stream(context):
                    print(chunk, end="", flush=True)
                    answer += chunk
                print()
                self.history.append(
                    {
                        "role":"assistant",
                        "content":answer,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                memory.save_memory(self.history)
