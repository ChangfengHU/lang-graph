from typing_extensions import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    user_input: str
    category: str
    answer: str


def classify(state: State) -> dict:
    text = state["user_input"]
    category = "urgent" if "马上" in text or "紧急" in text else "normal"
    return {"category": category}


def route_by_category(state: State) -> Literal["urgent_path", "normal_path"]:
    if state["category"] == "urgent":
        return "urgent_path"
    return "normal_path"


def urgent_reply(state: State) -> dict:
    return {"answer": "已进入紧急处理流程：先确认影响范围，再执行止血动作。"}


def normal_reply(state: State) -> dict:
    return {"answer": "已进入普通处理流程：先收集上下文，再给出建议。"}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("classify", classify)
    graph.add_node("urgent_reply", urgent_reply)
    graph.add_node("normal_reply", normal_reply)
    graph.add_edge(START, "classify")
    graph.add_conditional_edges(
        "classify",
        route_by_category,
        {
            "urgent_path": "urgent_reply",
            "normal_path": "normal_reply",
        },
    )
    graph.add_edge("urgent_reply", END)
    graph.add_edge("normal_reply", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    print(app.invoke({"user_input": "线上接口马上报错了", "category": "", "answer": ""}))
    print(app.invoke({"user_input": "帮我解释一下 LangGraph", "category": "", "answer": ""}))
