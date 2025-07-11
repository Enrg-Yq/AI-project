from openai import OpenAI
from dotenv import load_dotenv, find_dotenv 
import os
import json
import functions_tools

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv()) # read local .env file
    client = OpenAI(
        api_key=os.environ['API_KEY'],
        base_url=os.environ['BASE_URL'],
    )
    tools = [functions_tools.BAIDU_SEARCH]

    messages = [
        {"role": "system", "content": "不需要要求用户问题，直接使用工具来回答问题。"},
        {"role": "user", "content": "帮我查一下天津有哪些经典的景点？"},
    ]
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages,
        tools=tools,
        tool_choice="auto",
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
                model="glm-4-flash",
                messages=messages,
                tools=tools,
            )
    print(response.choices[0].message.content)
