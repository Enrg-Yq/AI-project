import asyncio
import os
from typing import Annotated,Literal
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv,find_dotenv
from typing import Annotated, Literal
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool

Operator = Literal["+", "-", "*", "/"]

# 类型声明
def calculator(a: float, b: float, operator: Annotated[Operator, "operator"]) -> float:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    else:
        raise ValueError("Invalid operator")

async def main():

    model_client = OpenAIChatCompletionClient(
        model= "deepseek-chat",
        api_key=os.environ["API_KEY"],
        base_url=os.environ["BASE_URL"],
        model_info={
        "function_calling":True,
        "family":"deepseek-chat",
        "json_output":True,
        "structured_output":True,
        "vision":False
        }

    )
    # response = await model_client.create(messages=[UserMessage(content="你好",source="user")])
    # print(response.content)
    fun_tool = FunctionTool(calculator,description="四则运算")
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[fun_tool],
        reflect_on_tool_use=True,
    )
    result = agent.run_stream(task="(2*3)+0.5=?")
    await Console(result,output_stats=True)
    await model_client.close()

if __name__=="__main__":
    load_dotenv(find_dotenv())
    asyncio.run(main())












