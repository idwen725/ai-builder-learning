import json
try:
    with open("progress.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    data = {
        "name": "dcx",
        "phase": 1,
        "day": 3,
        "completed_days": 2
    }
    with open("progress.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    with open("progress.json", "r", encoding="utf-8") as file:
        data = json.load(file)


print("===== AI Builder Progress =====")
print(" ")
print("使用者："+data["name"])
print("当前阶段："+str(data["phase"]))
print("当前day："+str(data["day"]))
print("已完成："+str(data["completed_days"]))
print(" ")
print("请选择：")
print(" ")
print("1.完成今天")
print("2.查看进度")
try:
    a=int(input())
    if a==1:
        data["completed_days"] = data["completed_days"] + 1
        with open("progress.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False,indent=4)
    elif a==2:
        print("已完成："+str(data["completed_days"]))
    else:
        print("无效数字")
except ValueError:
    print("你输入的不是数字。")