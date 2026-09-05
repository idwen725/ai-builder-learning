import ai_client
history=[]
print("----------")
while True:
    prompt=input("你：")
    if prompt=="退出":
        print("再见")
        break
    else:
        history.append("用户："+prompt)
        answer = ai_client.ask_ai(history)
        history.append("AI："+answer)
        print("AI："+answer)
        print("----------")