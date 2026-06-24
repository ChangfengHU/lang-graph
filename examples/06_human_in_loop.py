from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    topic: str
    draft: str
    approved: bool
    final: str


def write_draft(state: State) -> dict:
    return {"draft": f"准备发布一段关于「{state['topic']}」的内容。"}


def human_review(state: State) -> dict:
    decision = interrupt(
        {
            "question": "是否批准发布？",
            "draft": state["draft"],
            "expected": "传入 {'approved': true} 或 {'approved': false}",
        }
    )
    return {"approved": bool(decision.get("approved"))}


def publish_or_reject(state: State) -> dict:
    if state["approved"]:
        return {"final": f"已发布：{state['draft']}"}
    return {"final": "未发布：人工审核未通过。"}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("write_draft", write_draft)
    graph.add_node("human_review", human_review)
    graph.add_node("publish_or_reject", publish_or_reject)
    graph.add_edge(START, "write_draft")
    graph.add_edge("write_draft", "human_review")
    graph.add_edge("human_review", "publish_or_reject")
    graph.add_edge("publish_or_reject", END)
    return graph.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "approval-demo"}}

    paused = app.invoke(
        {"topic": "LangGraph 人工审批", "draft": "", "approved": False, "final": ""},
        config,
    )
    print("PAUSED:")
    print(paused)

    resumed = app.invoke(Command(resume={"approved": True}), config)
    print("RESUMED:")
    print(resumed)
