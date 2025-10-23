from dotenv import load_dotenv
import os
from openai import OpenAI


load_dotenv()


def generate_response(prompt,model_name):

    api_key = os.environ['DEEPSEEK_API_KEY']
    url = os.environ['DEEPSEEK_BASE_URL']

    client = OpenAI(api_key=api_key,base_url=url)

    messages =[
        {"role":"system", "content":"你是一个热心的智能助手！"},
        {"role":"user", "content":prompt}
    ]


    response = client.chat.completions.create(
        model = model_name,
        messages = messages,
        temperature=0,
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    while True:
        user_input = input('用户输入：')
        resp = generate_response(user_input,'deepseek-chat')
        print(resp)