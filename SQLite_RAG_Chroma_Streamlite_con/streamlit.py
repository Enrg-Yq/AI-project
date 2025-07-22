import streamlit as st

if __name__ == "__main__":
    st.set_page_config(page_title="Medical Chatbot", layout="wide")
    st.title("Molly 医疗精灵")

    with st.chat_message("AI"):
        st.write("你好我是Molly医疗精灵，专注于解决你的问题！")
    with st.chat_message("HUMAN"):
        st.write("如何治疗脑卒中的疾病？")

    question = st.chat_input("输入问题提问....")

    with st.sidebar:
        st.header(f"当前对话ID:{{1}}")  # 设置侧边栏的标题
        st.button("开始新对话")  # 侧边栏的按钮，点击后会触发start_session函数

        with st.expander(f"对话ID:{{1}}"):
            col1, col2 = st.columns(2)
            col1.button("继续对话")
            col2.button("删除对话")
