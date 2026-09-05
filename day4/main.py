import progress_manager


data= progress_manager.load_progress()
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
        progress_manager.save_progress(data)
    elif a==2:
        print("已完成："+str(data["completed_days"]))
    else:
        print("无效数字")
except ValueError:
    print("你输入的不是数字。")