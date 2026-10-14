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
    def _create_session(self):
        session_id = str(uuid.uuid4())[:8]
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session_data["sessions"][session_id] = {
            "title": "新会话",
            "created_at": now,
            "updated_at": now,
            "history": []
        }
        return session_id
    def _normalize_session(self, session):
        if "title" not in session:
            session["title"] = "旧会话"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if "created_at" not in session:
            session["created_at"] = now
        if "updated_at" not in session:
            session["updated_at"] = now
        if "history" not in session:
            session["history"] = []
    def __init__(self):
        self.client = AIClient()
        self.long_memory = memory.load_long_term_memory()
        self.context_char_budget = Config.CONTEXT_CHAR_BUDGET
        self.session_data = memory.load_session_data()
        for session in self.session_data["sessions"].values():
            self._normalize_session(session)
        memory.save_session_data(self.session_data)
        if self.session_data["current_session_id"] is None:
            self.session_id = self._create_session()
            self.session_data["current_session_id"] = self.session_id
            memory.save_session_data(self.session_data)
        else:
            self.session_id = self.session_data["current_session_id"]
        self.history = self.session_data["sessions"][self.session_id]["history"]
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
            elif prompt == "/clear":
                self.history.clear()
                memory.save_session_data(self.session_data)
                print("当前会话已清空")
            elif prompt == "/new":
                self.session_id = self._create_session()
                self.session_data["current_session_id"] = self.session_id
                self.history = self.session_data["sessions"][self.session_id]["history"]
                memory.save_session_data(self.session_data)
                print(f"已创建新会话 {self.session_id}")
            elif prompt == "/sessions":
                if not self.session_data["sessions"]:
                    print("没有会话记录")
                else:
                    for session_id in self.session_data["sessions"]:
                        session = self.session_data["sessions"][session_id]
                        if session_id == self.session_id:
                            print(
                                f"* {session_id} | "
                                f"{session['title']} | "
                                f"{session['updated_at']} | 当前会话"
                            )
                        else:
                            print(
                                f"- {session_id} | "
                                f"{session['title']} | "
                                f"{session['updated_at']}"
                            )
            elif prompt.startswith("/switch "):
                requirement = prompt[len("/switch "):]
                if requirement in self.session_data["sessions"]:
                    self.session_data["current_session_id"] = requirement
                    self.session_id = requirement
                    self.history = self.session_data["sessions"][requirement]["history"]
                    memory.save_session_data(self.session_data)
                    print(f"已切换到会话 {requirement}")
                else:
                    print("会话不存在")
            else:
                request_id = str(uuid.uuid4())[:8]
                if self.session_data["sessions"][self.session_id]["title"] == "新会话":
                    self.session_data["sessions"][self.session_id]["title"] = prompt[:20]
                logging.info(
                    f"session_id={self.session_id} | "
                    f"request_id={request_id} | "
                    f"用户请求开始"
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
                    f"session_id={self.session_id} | "
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
                self.session_data["sessions"][self.session_id]["updated_at"] = (
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                logging.info(
                    f"session_id={self.session_id} | "
                    f"request_id={request_id} | "
                    f"span=llm_call | "
                    f"duration={llm_cost:.4f}s"
                )
                logging.info(
                    f"session_id={self.session_id} | "
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
                memory.save_session_data(self.session_data)
