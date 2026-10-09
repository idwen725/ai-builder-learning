import os
import time
import uuid
import logging
import memory
from ai_client import AIClient
import datetime
import context_manager
from config import Config
class App:
    def __init__(self):
        self.client = AIClient()
        self.history = memory.load_memory()
        self.long_memory = memory.load_long_term_memory()
        self.context_char_budget = Config.CONTEXT_CHAR_BUDGET
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
            elif prompt == "/memory":
                facts = self.long_memory
                for fact in facts:
                    print(fact)
            else:
                request_id = str(uuid.uuid4())[:8]
                logging.info(
                    f"request_id={request_id} | 用户请求开始"
                )
                self.history.append(
                    {
                        "role":"user",
                        "content":prompt,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                )
                context_start = time.time()
                context = context_manager.build_context(self.history, self.long_memory,self.context_char_budget)
                context_cost =time.time() - context_start
                logging.info(
                    f"request_id={request_id} | "
                    f"span=context_build | "
                    f"duration={context_cost:.4f}s"
                )
                print("AI：", end="")
                answer = ""
                success = False
                llm_start = time.time()
                try:
                    for chunk in self.client.ask_stream(context, request_id):
                        print(chunk, end="", flush=True)
                        answer += chunk
                    success = True
                except Exception:
                    print("\n[AI生成中断]")
                print()
                print(
                    "Context长度:",
                    context_manager.count_context_length(context)
                )
                llm_cost = time.time() - llm_start
                logging.info(
                    f"request_id={request_id} | "
                    f"span=llm_call | "
                    f"duration={llm_cost:.4f}s"
                )
                logging.info(
                    f"request_id={request_id} | "
                    f"success={success} | "
                    f"Context长度={context_manager.count_context_length(context)} | "
                    f"回答长度={len(answer)} | "
                    f"用户请求结束"
                )
                if success:
                    self.history.append(
                        {
                            "role":"assistant",
                            "content":answer,
                            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    )
                memory.save_memory(self.history)
