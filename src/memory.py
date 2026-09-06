import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEMORY_FILE = os.path.join(BASE_DIR,"memory.json")
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