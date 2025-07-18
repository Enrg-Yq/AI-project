from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories.sql import SQLChatmessageHistory
from langchain_openai import ChatOpenAI


import os
def get_history(session_id):
    return SQLChatmessageHistory(session_id,"sqlite:///chat_history.db")

if __name__ == "__main__":
    
    os.environ["OPENAI_API_KEY"] = "sk-mqFF8MxRgLFdX6Gn3c3fB246D7484b46A9A4F58238F6Ef6e"
    os.environ["OPENAI_BASE_URL"] = "https://api.laozhang.ai/v1"

    llm = ChatOpenAI(model= "gpt-3.5-turbo",temperature=0.7)

    llm_hist = RunnableWithMessageHistory(
        llm,
        get_session_history=get_history,
        )

    config = {
        "configurable": {
            "session_id": lambda: "1234",
        }
    }

    resp = llm_hist.invoke(HumanMessage(content="你好"),config=config)
    print(resp)



