from dotenv import load_dotenv
import os
from openai import OpenAI,APIConnectionError
import time

load_dotenv()


def generate_response(messages,model_name):

    api_key = os.environ['DEEPSEEK_API_KEY']
    url = os.environ['DEEPSEEK_BASE_URL']
    #opanai客户端
    client = OpenAI(api_key=api_key,base_url=url)

    for retry_cnt in range(3):
        #连接失败后重试
        try:
            response = client.chat.completions.create(
            model = model_name,
            messages = messages,
            temperature=0,
            )
            #调用成功后终止循环返回调用结果
            return response.choices[0].message.content
        except APIConnectionError as err:
            #当遇到上面APIConnectionError错误时，自动跳转到这里
            retry_cnt += 1
            print(f'deepseek连接失败!重试{retry_cnt+1}次')
            time.sleep(1.5)

        return "deepseek调用失败"

    return response.choices[0].message.content

if __name__ == '__main__':
        
    messages =[
        {"role":"system", "content":"你是一个热心的智能助手！"}
    ]

    while True:

        user_input = input('用户输入：')

        #添加对话内容
        messages.append({"role":"user","content":user_input})

        resp = generate_response(messages,'deepseek-chat')
        print(resp)

        #返回信息存入message
        messages.append({"role":"assistant","content":resp})