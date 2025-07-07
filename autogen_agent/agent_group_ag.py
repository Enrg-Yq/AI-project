from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat

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
            "vision": False,
        },
        seed=123,
        temperature=0,
    )

    agent1 = AssistantAgent(
        name="assistant1",
        model_client=model_client,
        system_message="你是1号，是讲相声大师"
    )
    agent2 = AssistantAgent(
    name="assistant2",
    model_client=model_client,
    system_message="你是2号，是00后讲抽象大师"
    )
    team = RoundRobinGroupChat(participants=[agent1,agent2],max_turns=2)
    stream = team.run_stream(task="给我讲个日常笑话")
    await Console(stream)

if __name__=="__main__":
    load_dotenv(find_dotenv())
    asyncio.run(main())