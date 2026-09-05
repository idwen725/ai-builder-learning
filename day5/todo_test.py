import requests
url="https://jsonplaceholder.typicode.com/todos/5"
data=requests.get(url).json()
print(f"任务ID：{data['id']}")
print(f"任务名称：{data['title']}")
print(f"是否完成：{data['completed']}")