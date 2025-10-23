import gradio as gr
from dotenv import load_dotenv
import os
from openai import OpenAI,APIConnectionError
import time

load_dotenv()


def generate_response(input,messages):

    api_key = os.environ['DEEPSEEK_API_KEY']
    url = os.environ['DEEPSEEK_BASE_URL']

    #用户输入信息存入message
    messages.append({"role":"user","content":input})

    #opanai客户端
    client = OpenAI(api_key=api_key,base_url=url)

    for retry_cnt in range(3):
        #连接失败后重试
        try:
            response = client.chat.completions.create(
            model = 'deepseek-chat',
            messages = messages,
            temperature=0,
            )
            #调用成功后终止循环返回调用结果
            reply =  response.choices[0].message.content
            #返回信息存入message
            return reply
        except APIConnectionError as err:
            #当遇到上面APIConnectionError错误时，自动跳转到这里
            retry_cnt += 1
            print(f'deepseek连接失败!重试{retry_cnt+1}次')
            time.sleep(1.5)

        return "deepseek调用失败"

def chat_with_gradio(user_input, conversation_state=gr.State([])):
    """
    Gradio 界面的交互函数
    """
    # 获取当前会话状态
    conversation_history = conversation_state
    # 调用聊天函数
    reply = generate_response(user_input,conversation_history)
    
    # 返回机器人回复和更新后的会话历史
    return reply,conversation_history

# 创建 Gradio 界面
iface = gr.Interface(
    fn=chat_with_gradio,
    inputs=[
        gr.Textbox(lines=2, placeholder="请输入...", label="你的问题"),
        gr.State([])  # 用于存储会话历史
    ],
    outputs=[
        gr.Textbox(label="机器人回答",lines = 20),
        gr.State()  # 会话历史（用户不可见）
    ],
    title="聊天机器人",
    description="基于 DeepSeekAPI 的聊天机器人",
    examples=[
        ["给我讲一个科幻故事吧！"],
        ["讲一个小笑话？"]
    ]
)
 
# 启动界面
iface.launch(share=True)