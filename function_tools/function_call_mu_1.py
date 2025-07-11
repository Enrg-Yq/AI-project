from openai import OpenAI
import os
import json
from dotenv import load_dotenv, find_dotenv
import functions_tools


if __name__=="__main__":

    load_dotenv(find_dotenv())
# def multiply_two_numbers(a,b):
#     result=a*b
#     return result
    client = OpenAI(
        api_key=os.environ["API_KEY"],
        base_url=os.environ["BASE_URL"],
    )
    tools=[
        {
        "type": "function",
        "function": {
            "name": "multiply_two_numbers",
            "description": "两个数相乘",
            "parameters": {
            "type": "object",
            "properties": {
                "a":{"type":"number",
                "description":"第一个数字"
                },
                "b":{"type":"number",
                "description":"第二个数字"
                }
            },
            "required": ["a", "b"]
            }
        }
        }

    ]
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "123*3是多少"}],
    tools=tools,
    )
# print(response.choices[0].message.tool_calls)
# 函数是数据类型
if (response.choices[0].message.tool_calls) is not None:
    # 调用参数
    args=response.choices[0].message.tool_calls[0].function.arguments
    args=json.loads(args) 
    function_name=response.choices[0].message.tool_calls[0].function.name
    # 调用本地函数
    # invoke_fun = globals()[function_name]
    # 调用外部模块函数
    invoke_fun = getattr(functions_tools, function_name)
    result=invoke_fun(**args)

    print(f"函数调用结果{result}")
