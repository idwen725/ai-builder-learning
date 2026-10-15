import json
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MEMORY_FILE = os.path.join(BASE_DIR,"memory.json")
LONG_MEMORY_FILE = os.path.join(BASE_DIR,"long_term_memory.json")
def default_session_data():
    return {
        "current_session_id":None,
        "sessions":{}
    }
def is_valid_session_data(data):
    if not isinstance(data,dict) or "current_session_id" not in data or "sessions" not in data or not isinstance(data["sessions"],dict):
        return False
    else:
        return True
def load_long_term_memory():
    if not os.path.exists(LONG_MEMORY_FILE):
        return []
    try:
        with open(LONG_MEMORY_FILE,"r",encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return []
            if "facts" not in data:
                return []
            if not isinstance(data["facts"], list):
                return []
            return data["facts"]
    except json.JSONDecodeError:
        return []
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
def load_session_data():
    if not os.path.exists(MEMORY_FILE):
        return default_session_data()
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return default_session_data()
    if not is_valid_session_data(data):
        return default_session_data()
    return data
def save_session_data(session_data):
    with open(MEMORY_FILE,"w",encoding="utf-8") as f:
        json.dump(session_data,f,ensure_ascii=False,indent=4)