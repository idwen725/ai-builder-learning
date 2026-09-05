import json
def load_progress():
    try:
        with open("progress.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {
            "name": "dcx",
            "phase": 1,
            "day": 4,
            "completed_days": 3
        }
        with open("progress.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    return data
def save_progress(data):
    with open("progress.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def show_progress(data):
    print("===== AI Builder Progress =====")
    print(" ")
    print(f"使用者：{data['name']}")
    print(f"当前阶段：{data['phase']}")
    print(f"当前day：{data['day']}")
    print(f"已完成：{data['completed_days']}")