from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory

def get_history(session_id):
    # 创建SQLChatMessageHistory对象，用于存储聊天历史  
    # 如果数据库文件或表不存在，会自动创建
    # 如果session_id不存在，会自动创建对应的聊天历史
    # 如果session_id存在，会返回对应的聊天历史
    # "sqlite:///chat_history.db"是SQLite数据库的连接字符串
    return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

if __name__ == "__main__":
    import os
    os.environ['OPENAI_API_KEY']=''
    os.environ['OPENAI_API_BASE']='https://oa.api2d.net'

    llm = ChatOpenAI(model='gpt-3.5-turbo')

    # 管理聊天历史
    llm_hist = RunnableWithMessageHistory(
        llm,
        get_session_history=get_history
    )

    config = {'configurable': {'session_id': 'abc123'}}

    resp = llm_hist.invoke(HumanMessage(content="你好!"), config=config)
    print(resp)
