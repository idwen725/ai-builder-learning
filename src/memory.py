import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEMORY_FILE = os.path.join(BASE_DIR,"memory.json")
LONG_MEMORY_FILE = os.path.join(BASE_DIR,"long_term_memory.json")
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
def save_memory(history):
    with open(MEMORY_FILE,"w",encoding="utf-8") as f:
        json.dump(history,f,ensure_ascii=False,indent=4)
def get_recent_history(history, n):
    return history[-n:]
def load_long_term_memory():
    if not os.path.exists(LONG_MEMORY_FILE):
        return []
    try:
        with open(LONG_MEMORY_FILE,"r",encoding="utf-8") as f:
            fact = json.load(f)["facts"]
            return fact
    except json.JSONDecodeError:
        return []
def build_context(history, long_memory, n):
    context = []
    long_memory = {
        "role": "system",
        "content": "\n".join(long_memory)
    }
    context.append(long_memory)
    context.extend(get_recent_history(history,n))
    return context
def save_long_term_memory(long_memory):
    data = {
        "facts": long_memory
    }

    with open(LONG_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )