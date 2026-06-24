import operator
from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    # 普通字段：如果节点返回新的 outline，会覆盖旧值。
    topic: str
    outline: str

    # reducer 字段：Annotated[list[str], operator.add]
    # 表示多个节点都返回 steps 时，不是覆盖，而是用 + 把列表拼起来。
    steps: Annotated[list[str], operator.add]


def make_outline(state: State) -> dict:
    print("[node:make_outline] 收到 state:", state)
    return {
        "outline": f"1. 什么是{state['topic']}\n2. 为什么需要它\n3. 如何开始",
        "steps": ["生成大纲"],
    }


def polish_outline(state: State) -> dict:
    print("[node:polish_outline] 收到 state:", state)
    return {
        "outline": state["outline"] + "\n4. 常见坑和最佳实践",
        "steps": ["补充进阶章节"],
    }


def build_graph():
    graph = StateGraph(State)
    graph.add_node("make_outline", make_outline)
    graph.add_node("polish_outline", polish_outline)
    graph.add_edge(START, "make_outline")
    graph.add_edge("make_outline", "polish_outline")
    graph.add_edge("polish_outline", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    print("[graph] 第 2 节的图：")
    print(app.get_graph().draw_ascii())

    input_state = {"topic": "LangGraph", "outline": "", "steps": []}
    print("[input] 初始 state:", input_state)

    result = app.invoke(input_state)

    print("[output:outline] 最终大纲：")
    print(result["outline"])
    print("[output:steps] 最终步骤：", result["steps"])
    print("\n你刚刚验证了 2 件事：")
    print("1. outline 是普通字段，节点返回新 outline 后会写回 state。")
    print("2. steps 是 reducer 字段，两个节点返回的列表被累加成了两项。")
