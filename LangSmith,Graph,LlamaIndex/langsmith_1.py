from openai import OpenAI
from dotenv import load_dotenv
import os
from langsmith.wrappers import wrap_openai
# from langchain_openai import ChatOpenAI
from langsmith_1 import traceable


@traceable()
def retriever(query:str):
    results = ["Harrison worked at Kensho"]
    return results
@traceable()
def rag(question):
    docs = retriever(question)
    system_message = """Answer the user question using only the provided information below:{docs}""".format(docs="\n".join(docs))
    return openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": question}
        ]
    )

if __name__ == "__main__":
    load_dotenv()
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGSMITH_API_KEY"] = "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"
    os.environ["LANGSMITH_BASE_URL"] = "pr-virtual-address-26"

    openai_client = wrap_openai(OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    ))
    question = "Where did Harrison work?"
    print(rag(question))