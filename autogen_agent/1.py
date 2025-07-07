import asyncio
import os
from typing import Annotated, Literal
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv, find_dotenv
from autogen_agentchat.ui import Console
from autogen_core.tools import FunctionTool
# 假设 FunctionExecutionResult 从这里导入，根据实际情况调整
from autogen_agentchat.events import FunctionExecutionResult

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
            "function_calling": True,
            "family": "deepseek-chat",
            "json_output": True,
            "structured_output": True,
            "vision": False
        }
    )
    fun_tool = FunctionTool(calculator, description="四则运算")
    agent = AssistantAgent(
        name="assistant",
        model_client=model_client,
        tools=[fun_tool],
        reflect_on_tool_use=True,
    )
    result = agent.run_stream(task="(2*3)+0.5=?")
    final_answer = None
    async for event in result:
        if isinstance(event, FunctionExecutionResult) and not event.is_error:
            final_answer = event.content
        await Console(event, output_stats=True)

    if final_answer is not None:
        print(f"最终答案: {final_answer}")
    await model_client.close()

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    asyncio.run(main())












