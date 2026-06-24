import operator
from typing import Annotated

from typing_extensions import Literal, TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class State(TypedDict):
    topic: str
    sources: Annotated[list[str], operator.add]
    notes: Annotated[list[str], operator.add]
    report: str
    approved: bool


def collect_sources(state: State) -> dict:
    return {
        "sources": [
            f"官方文档：{state['topic']} overview",
            f"实践案例：{state['topic']} agent workflow",
        ]
    }


def take_notes(state: State) -> dict:
    return {
        "notes": [
            "LangGraph 适合有状态、多步骤、可恢复的 agent 工作流。",
            "图结构让节点和路由显式可见，便于测试和维护。",
        ]
    }


def needs_review(state: State) -> Literal["review", "write_report"]:
    if len(state["sources"]) < 2:
        return "review"
    return "write_report"


def human_review(state: State) -> dict:
    decision = interrupt(
        {
            "question": "资料是否足够？",
            "sources": state["sources"],
            "expected": "传入 {'approved': true} 继续，或 {'approved': false} 停止。",
        }
    )
    return {"approved": bool(decision.get("approved"))}


def route_after_review(state: State) -> Literal["write_report", "end"]:
    return "write_report" if state["approved"] else "end"


def write_report(state: State) -> dict:
    bullets = "\n".join(f"- {note}" for note in state["notes"])
    sources = "\n".join(f"- {source}" for source in state["sources"])
    return {
        "report": (
            f"# {state['topic']} 研究报告\n\n"
            f"## 结论\n{bullets}\n\n"
            f"## 参考资料\n{sources}"
        )
    }


def build_graph():
    graph = StateGraph(State)
    graph.add_node("collect_sources", collect_sources)
    graph.add_node("take_notes", take_notes)
    graph.add_node("human_review", human_review)
    graph.add_node("write_report", write_report)
    graph.add_edge(START, "collect_sources")
    graph.add_edge("collect_sources", "take_notes")
    graph.add_conditional_edges(
        "take_notes",
        needs_review,
        {
            "review": "human_review",
            "write_report": "write_report",
        },
    )
    graph.add_conditional_edges(
        "human_review",
        route_after_review,
        {
            "write_report": "write_report",
            "end": END,
        },
    )
    graph.add_edge("write_report", END)
    return graph.compile(checkpointer=InMemorySaver())


def initial_state(topic: str) -> State:
    return {
        "topic": topic,
        "sources": [],
        "notes": [],
        "report": "",
        "approved": False,
    }


if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "research-demo"}}
    result = app.invoke(initial_state("LangGraph"), config)

    if "__interrupt__" in result:
        result = app.invoke(Command(resume={"approved": True}), config)

    print(result["report"])
