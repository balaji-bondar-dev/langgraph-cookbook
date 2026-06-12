from typing import TypedDict,Annotated
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage,BaseMessage
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
import operator
from dotenv import load_dotenv

load_dotenv()

class MessageState(TypedDict):
    messages: Annotated[list["BaseMessage"] , operator.add]

llm = ChatGroq(model="llama-3.1-8b-instant",streaming=True)

def chatbot_node(state:MessageState)-> dict:
    return {"messages":[llm.invoke(state["messages"])]}

def dummy_node(state:MessageState)-> MessageState:
    return state

builder = StateGraph(MessageState)
builder.add_node("chatbot_node",chatbot_node)
builder.add_node("dummy_node",dummy_node)

builder.add_edge(START,"chatbot_node")
builder.add_edge("chatbot_node","dummy_node")
builder.add_edge("dummy_node",END)
0
graph = builder.compile()

# #-----------------------[Method-1] Status='updates'-----------------------
# for event in graph.stream(
#     {
#         "messages" : [HumanMessage("What is the capital of France?")]
#     },
#     stream_mode= "updates",
# ):
#     for node_name,output in event.items():
#          print(f"[{node_name}] {output['messages'][-1].content}")

#-----------------------[Method-2] Status='values'-------------------------
for event in graph.stream(
    {
        "messages" : [HumanMessage("What is the capital of France?")]
    },
    stream_mode= "values",
):
    print(f"✔ The state has {len(event['messages'])} messsages.")
    print(f"Messages: {event['messages']}")
    
    