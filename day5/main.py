import api_client
print("===== Todo Viewer =====")
print("请输入任务ID")
try:
    a=int(input())
except ValueError:
    print("请输入正确的数字")
else:
    data=api_client.get_todo(a)
    if data is not None:
        print(data["id"])
        print(data["title"])
        print(data["completed"])