import os
import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from dotenv import load_dotenv
from autogen_agentchat.messages import MultiModalMessage
from io import  BytesIO
import requests
from autogen_core import Image as AGImage
from PIL import Image
import matplotlib.pyplot as plt

async def main():
    model_client = OpenAIChatCompletionClient(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
        model="glm-4v-flash",
        model_info={
        "function_calling":True,
        "family":"zhipu-ai",
        "json_output":True,
        "structured_output":True,
        "vision":True
        }

        )
    pil_image = Image.open(BytesIO(requests.get("https://picsum.photos/300/200").content))
    img = AGImage(pil_image)
    multi_model_message = MultiModalMessage(content=["描述图片内容",img],source="User")
    agent = AssistantAgent("assistant",model_client=model_client)
    task_result = await agent.run(task=multi_model_message)
    print(task_result.messages[-1].content)
    plt.imshow(pil_image)
    plt.show()


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
