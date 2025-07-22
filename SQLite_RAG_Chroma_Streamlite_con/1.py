from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage

from langchain_core.runnables import RunnableLambda,RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
import sqlite3
from langchain.prompts.chat import ChatPromptTemplate
from dotenv import load_dotenv


class Prompts:
    # 系统提示词
    system_prompt = """
    """
    greeting_prompt = ""
    prompt_template = """
    """

class Robot:
    def __init__(self, model_config, retriever=None):
        self.prompts = Prompts()

        llm = ChatOpenAI(**model_config)

        # template填充的human_message
        template = ChatPromptTemplate.from_messages([("human", self.prompts.prompt_template)])

        # 通过注入式方式，实现更多数据链传入
        if retriever is None:
            retriever = RunnableLambda(lambda input: "")

        # 带消息历史
        llm_hist = RunnableWithMessageHistory(
            template | llm,
            get_session_history=self.get_history,
            history_messages_key="chat_history"  # chain被invoke时，传入的chat_history会被存储在该key中
        )

        self.chain = {'input': RunnablePassthrough(), 'rag_results': retriever, 'chat_history': RunnablePassthrough()} | llm_hist

    def check_session_id(self):
        # 建表和获取所有session_id,若不存在
        con = sqlite3.connect("chat_history.db")
        cursor = con.cursor()

        valid_table_exists_sql = "select count(*) from sqlite_master where type='table' and name='message_store'"
        res = cursor.execute(valid_table_exists_sql)

        if res.fetchone()[0] == 0:
            return False

        search_session_id_sql = f"select distinct session_id from message_store"
        res = cursor.execute(search_session_id_sql)

        # 结果查询输出
        all_session_id = res.fetchall()

        # 关闭游标和连接
        cursor.close()
        con.close()

        return [item[0] for item in all_session_id]

    def get_history(self, session_id):
        if session_id not in self.check_session_id():
            history = SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")
            # 当#session_id#不存在, 则添加系统提示和欢迎语
            history.add_message(SystemMessage(content=self.prompts.system_prompt))
            history.add_message(AIMessage(content=self.prompts.greeting_prompt))
            return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")
        return SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")

    def chat(self, input, session_id):
        config = {'configurable': {'session_id': session_id}}
        response = self.chain.invoke(input, config=config)
        return response.content

    def stream(self, inputs, session_id):
        config = {'configurable': {'session_id': session_id}}
        response = self.chain.stream(inputs, config=config)
        return response

if __name__ == "__main__":
    load_dotenv()

    robot = Robot(model_config={'model': 'gpt-3.5-turbo'})
    result = robot.chat('你能帮我找找附近的美食吗？', session_id='abc789')
    print("答复：", result)
        



