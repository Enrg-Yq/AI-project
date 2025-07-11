from openai import OpenAI
from dotenv import load_dotenv, find_dotenv 
import os
import json
import functions_tools

if __name__ == "__main__":
    _ = load_dotenv(find_dotenv()) # 
    client = OpenAI(
        api_key=os.environ['API_KEY'],
        base_url=os.environ['BASE_URL'],
    )
    tools = [functions_tools.JUHE_SEARCH,
             functions_tools.MULTIPLY_TWO_NUMBERS,
             functions_tools.DIV_TWO_NUMBERS,
             ]
    exchange_example="""  
    使用查询到汇率信息动态计算结果。
    例如100人民币可以兑换多少外币：
    1.首先使用“closePri”获得外币汇率，
    2.然后用100人民币除以汇率，得到外币金额
    
    根据上述计算公式，计算不同外币之间的兑换
    根据用户问题，将100人民币兑换成其他任意金额的外币
    计算过程不变
    """ 
    messages = [
        {"role": "system", "content": "不需要要求用户问题，直接使用工具来回答问题。"+exchange_example},
        {"role": "user", "content": "帮我算一下10000日元可以换多少美元？"},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )
    while response.choices[0].message.tool_calls is not None:
        messages.append(response.choices[0].message)
        for tool_call in response.choices[0].message.tool_calls:
            args = tool_call.function.arguments
            try:
                args = json.loads(args)
                function_name = tool_call.function.name
                invoke_fun = getattr(functions_tools, function_name)
                result = invoke_fun(**args)
            except Exception as e:
                # 处理异常，记录错误信息
                result = f"调用函数 {function_name} 时发生错误: {str(e)}"
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
