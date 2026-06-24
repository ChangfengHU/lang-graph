import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    messages: Annotated[list[str], operator.add]


def echo_with_memory(state: State) -> dict:
    user_message = state["messages"][-1]
    seen = len([m for m in state["messages"] if m.startswith("user:")])
    return {"messages": [f"assistant: 第 {seen} 轮收到：{user_message}"]}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("echo_with_memory", echo_with_memory)
    graph.add_edge(START, "echo_with_memory")
    graph.add_edge("echo_with_memory", END)
    return graph.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "student-1"}}

    print(app.invoke({"messages": ["user: 你好"]}, config))
    print(app.invoke({"messages": ["user: 我想继续学习"]}, config))

    isolated_config = {"configurable": {"thread_id": "student-2"}}
    print(app.invoke({"messages": ["user: 新线程从第一轮开始"]}, isolated_config))
