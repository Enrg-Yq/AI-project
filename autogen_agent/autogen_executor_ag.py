from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import CodeExecutorAgent
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.ui import Console
from dotenv import load_dotenv, find_dotenv
import asyncio
import os

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

    executor = CodeExecutorAgent(
        name="code_exec",
        model_client=model_client,
        code_executor=LocalCommandLineCodeExecutor(work_dir='temp_dir',cleanup_temp_files=False)
    )
    await Console(executor.run_stream(task="生成一段python代码，输出'12345'"),output_stats=True)
    await executor.close()



if __name__=="__main__":
    load_dotenv(find_dotenv())
    asyncio.run(main())