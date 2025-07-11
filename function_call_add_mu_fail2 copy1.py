from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import json
import functions_tools

# 加载环境变量（如API密钥等），优先查找.env文件
load_dotenv(find_dotenv())

# 初始化OpenAI客户端，使用环境变量中的API密钥和自定义API地址
client = OpenAI(
    api_key=os.environ["API_KEY"], base_url=os.environ["BASE_URL"]
)

# 初始化对话消息，用户输入为“计算一下 
messages = [{"role": "user", "content": "计算一下 123*3+10 等于多少"}]

# 定义可用的函数工具（function calling），包括乘法和加法
tools = [
    {
        "type": "function",
        "function": {
            "name": "multiply_two_numbers",
            "description": "两个数相乘",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                },
                "required": ["a", "b"],  # 说明两个参数是必须的
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_two_numbers",
            "description": "两个数相加",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "第一个数字"},
                    "b": {"type": "number", "description": "第二个数字"},
                },
                "required": ["a", "b"],  # 说明两个参数是必须的
            },
        },
    },
]

# 首次调用OpenAI的chat.completions.create接口，获取模型回复
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    tools=tools,  # type: ignore
    messages=messages,  # type: ignore
)

# 如果模型回复中包含函数调用请求，则循环处理
while response.choices[0].message.tool_calls is not None:
    # 记录本次模型回复到消息列表
    messages.append(response.choices[0].message)  # type: ignore

    # 遍历所有的函数调用请求
    for tool_call in response.choices[0].message.tool_calls:
        # 获取函数调用的参数（字符串形式），并解析为字典
        args = tool_call.function.arguments
        args = json.loads(args)

        # 获取要调用的函数名
        function_name = tool_call.function.name

        # 从function_tools模块中获取对应的函数
        invoke_run = getattr(functions_tools, function_name)

        # 调用函数并获取结果
        result = invoke_run(**args)

        # 将函数调用结果以tool角色的消息形式加入消息列表
        messages.append(
            {
                "role": "tool",
                "content": f"{json.dumps(result)}",
                "tool_call_id": tool_call.id,
            }
        )

    # 再次调用OpenAI接口，继续对话流程，直到没有新的函数调用
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        tools=tools,  # type: ignore
        messages=messages,  # type: ignore
    )

# 输出最终模型回复的内容
print(response.choices[0].message.content)
