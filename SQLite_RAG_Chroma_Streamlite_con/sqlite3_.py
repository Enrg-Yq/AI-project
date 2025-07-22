import sqlite3

def check_session(session_id):
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
    search_session_id_sql = f"select session_id from message_store where session_id = '{session_id}'"
    res = cursor.execute(search_session_id_sql)    
    session_id = res.fetchone()
    # 关闭数据库连接
    cursor.close()
    con.close()
    
# 返回查询结果
    return session_id is not None
if __name__ == "__main__":
    print(check_session("abc123"))
    


