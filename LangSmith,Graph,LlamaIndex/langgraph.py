from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
import os
from langchain.chat_models import init_chat_model

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
def chatbot(state:State):
    return{"messages": [llm.invoke(state["messages"])]}

def dtream_graph_updates(user_input:str):
    for event in graph.stream(
        {"messages":[{"role":"user","content":user_input}]
         }):
        for value in event.values():
            print("Assistant",value["messages"][-1]["content"])

if __name__ == "__main__":
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGSMITH_API_KEY"] = "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"
    os.environ["LANGSMITH_BASE_URL"] = "langgraph"
    graph_bulider = StateGraph(State)
    os.environ["OPENAI_API_KEY"] = "sk-1234567890"
    os.environ["OPENAI_API_BASE"] = ""
    llm = init_chat_model("openai:gpt-3.5-turbo")
    graph_bulider.add_node("chatbot",chatbot)
    graph_bulider.add_edge(START,"chatbot")
    graph_bulider.add_edge("chatbot",END)
    graph = graph_bulider.compile()
    while True:
        user_input = input("User:")
        if user_input.lower() == "exit":
            
            break
        dtream_graph_updates(user_input)
