import time

from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    topic: str
    outline: str
    draft: str
    summary: str


def outline(state: State) -> dict:
    time.sleep(0.1)
    return {"outline": f"{state['topic']}：定义、核心概念、实践方式"}


def draft(state: State) -> dict:
    time.sleep(0.1)
    return {"draft": f"围绕 {state['outline']} 展开一篇教学内容。"}


def summarize(state: State) -> dict:
    time.sleep(0.1)
    return {"summary": "完成一篇从概念到实践的教学草稿。"}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("outline", outline)
    graph.add_node("draft", draft)
    graph.add_node("summarize", summarize)
    graph.add_edge(START, "outline")
    graph.add_edge("outline", "draft")
    graph.add_edge("draft", "summarize")
    graph.add_edge("summarize", END)
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    for update in app.stream(
        {"topic": "LangGraph", "outline": "", "draft": "", "summary": ""},
        stream_mode="updates",
    ):
        print(update)
