import streamlit as st

if __name__ == "__main__":
    st.set_page_config(
        page_title="医疗Angel AI",
        page_icon=":smile:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("医疗Angel")
    with st.chat_message("AI"):
        st.write("你好，我是医疗Angel AI，我可以帮助你查询医疗信息。")
    with st.chat_message("Human"):
        st.write("你好，我想知道医疗信息。")
    question = st.chat_input("请输入你的问题")

    with st.sidebar:
        st.header(f"当前对话ID：{1}")
        st.button("开始新的对话")

        with st.expander(f"对话ID：{1}"):
            col1, col2 = st.columns(2)
            col1.button("继续对话")
            col2.button("删除对话")