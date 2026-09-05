from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="用一句话解释什么是API"
)

print(response.output_text)