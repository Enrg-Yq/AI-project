from openai import OpenAI
import os
import json
from dotenv import load_dotenv, find_dotenv
import functions_tools

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv())
    client = OpenAI(
        api_key=os.environ['API_KEY'],
        base_url=os.environ['BASE_URL'],
    )
    # 假设 functions_tools 模块中有 weather_search 函数
    tools = [
        {
            "type": "function",
            "function": {
                "name": "weather_search",
                "description": "查询指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "要查询天气的城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]

    messages = [
        {"role": "system", "content": "不需要要求用户问题，直接使用工具来回答问题。"},
        {"role": "user", "content": "帮我查一下今日北京天气"},
    ]

    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages,
        tools=tools,
    )

    while response.choices[0].message.tool_calls:
        # 记录本次模型回复到消息列表
        messages.append(response.choices[0].message)

        for tool_call in response.choices[0].message.tool_calls:
            # 获取函数调用的参数（字符串形式），并解析为字典
            args = tool_call.function.arguments
            args = json.loads(args)

            # 获取要调用的函数名
            function_name = tool_call.function.name

            # 从 functions_tools 模块中获取对应的函数
            invoke_run = getattr(functions_tools, function_name)

            # 调用函数并获取结果
            result = invoke_run(**args)

            # 将函数调用结果以 tool 角色的消息形式加入消息列表
            messages.append(
                {
                    "role": "tool",
                    "content": f"{json.dumps(result)}",
                    "tool_call_id": tool_call.id,
                }
            )

        # 再次调用 OpenAI 接口，继续对话流程，直到没有新的函数调用
        response = client.chat.completions.create(
            model="glm-4-flash",
            tools=tools,
            messages=messages,
        )

    # 输出最终模型回复的内容
    print(response.choices[0].message.content)