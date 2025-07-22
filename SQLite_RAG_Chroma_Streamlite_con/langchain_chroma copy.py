from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
import sqlite3
from dotenv import load_dotenv


# 系统提示词
system_prompt = """你是一个名叫Molly的医学专家，
        对于用户提问的医学相关问题，你需要按照给出的参考文献资料对问题进行回答。
        你的回答需要按照以下步骤：
            1. 分析用户问题、对话历史以及参考文献，判断参考资料的哪些内容可以解答用户的问题，并将这一过程进行说明。
            2. 如果参考文献可以解答用户的问题，则根据文献内容对问题进行解答。
            3. 如果参考文献不能解答用户问题，告诉用户信息不足，无法回答，建议用户寻求专业人士帮助，不要自行发挥。
        你的回答需要注意以下几点： 
            1. 保证你的回答是清晰的、明确的。如果你参考了参考资料，应该指出参考资料的标题等。
            2. 结合用户的对话历史，分析用户的问题意图。但不要复述问题。
            2. 回复用户时，使用对话的口吻，有礼貌地称呼用户为”您“，不要使用“用户”来称呼！
            3. 如果用户的问题与医学无关，判断用户的目的，并温柔地提示其回到医学话题。
        再次提醒：请严格遵守以上规则，当参考资料不足时，拒绝回答问题，不要自行发挥！"""

# 欢迎提示词   
greeting_prompt = "你好！我是Molly医疗精灵，专注解决你的医疗问题。请问你需要什么帮助？"

def check_session_id():
    # 查询session_id是否存在
    con = sqlite3.connect('chat_history.db')
    cursor = con.cursor()
# 查询表是否存在
    valid_table_exists_sql = "select count(*) from sqlite_master where type='table' and name='message_store'"
    res = cursor.execute(valid_table_exists_sql)

# 第一次运行时，表不存在
    if res.fetchone()[0] == 0:
        return []
# 查询session_id是否存在
    # 这里使用distinct是为了确保只获取唯一的session_id
    search_session_id_sql = f"select distinct session_id from message_store"
    res = cursor.execute(search_session_id_sql)    
    all_session_id = res.fetchall()
    # 关闭数据库连接
    cursor.close()
    con.close()
    
# 返回查询结果
    return [item[0] for item in all_session_id]

def get_history(session_id):

    # 有就返回，没有对应的session_id就创建
    history = SQLChatMessageHistory(session_id, "sqlite:///chat_history.db")
    if session_id not in check_session_id():                   
        history.add_message(SystemMessage(content=system_prompt))
        history.add_message(AIMessage(content=greeting_prompt))
    return history
    

if __name__ == "__main__":
    
    load_dotenv()
    
    llm = ChatOpenAI(model='gpt-3.5-turbo')

    # 管理聊天历史
    llm_hist = RunnableWithMessageHistory(
        llm,
        get_session_history=get_history
    )

    config = {'configurable': {'session_id': 'abc123'}}

    resp = llm_hist.invoke(HumanMessage(content="你好!我叫什么"), config=config)
    print(resp)
