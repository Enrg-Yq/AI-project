from openai import OpenAI
import os
import json
from dotenv import load_dotenv, find_dotenv
import functions_tools


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    client = OpenAI(
    api_key=os.environ["API_KEY"],
    base_url=os.environ["BASE_URL"])
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
    },
        {
    "type": "function",
    "function": {
        "name": "add_two_numbers",
        "description": "两个数相加",
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

    messages=[{"role": "user", "content": "计算123*4+10是多少"}]
    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages,
    tools=tools,
    )

  
    while response.choices[0].message.tool_calls is not None:
            
        # 把消息存入列表，第二次调用模型时，会把消息作为参数传入，必须放在循环外，
        messages.append(response.choices[0].message)  
        for tool_call in response.choices[0].message.tool_calls:  
            # 调用参数
            args=tool_call.function.arguments
            args=json.loads(args)
            # 函数名称
            function_name=tool_call.function.name
            # 调用外部模块函数
            invoke_fun = getattr(functions_tools, function_name)
            result=invoke_fun(**args)
            # 结果添加到messages中,告知llm调用结果
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"{json.dumps(result)}"
                }
            )
            # 调用模型
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=tools,
            )
    print(response.choices[0].message.content)