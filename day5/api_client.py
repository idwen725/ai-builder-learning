import requests
def get_todo(todo_id):
    try:
        url="https://jsonplaceholder.typicode.com/todos/"+str(todo_id)
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()
        return data
    except requests.RequestException:
        print("API请求失败")
        return None