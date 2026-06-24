import operator
import re
from typing import Annotated

from typing_extensions import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    question: str
    operation: str
    numbers: list[int]
    tool_result: int | None
    answer: str
    trace: Annotated[list[str], operator.add]


def planner(state: State) -> dict:
    numbers = [int(x) for x in re.findall(r"-?\d+", state["question"])]
    if "加" in state["question"] or "+" in state["question"]:
        operation = "add"
    elif "乘" in state["question"] or "*" in state["question"]:
        operation = "multiply"
    else:
        operation = "unknown"

    return {
        "numbers": numbers,
        "operation": operation,
        "trace": [f"planner: operation={operation}, numbers={numbers}"],
    }


def should_use_tool(state: State) -> Literal["tool", "final"]:
    if state["operation"] in {"add", "multiply"} and len(state["numbers"]) >= 2:
        return "tool"
    return "final"


def calculator_tool(state: State) -> dict:
    if state["operation"] == "add":
        result = sum(state["numbers"])
    else:
        result = 1
        for number in state["numbers"]:
            result *= number

    return {"tool_result": result, "trace": [f"tool: result={result}"]}


def final_answer(state: State) -> dict:
    if state["tool_result"] is None:
        answer = "我没有识别到可计算的问题。请尝试输入：3 加 5。"
    else:
        answer = f"计算结果是：{state['tool_result']}"

    return {"answer": answer, "trace": ["final: answer ready"]}


def build_graph():
    graph = StateGraph(State)
    graph.add_node("planner", planner)
    graph.add_node("calculator_tool", calculator_tool)
    graph.add_node("final_answer", final_answer)
    graph.add_edge(START, "planner")
    graph.add_conditional_edges(
        "planner",
        should_use_tool,
        {
            "tool": "calculator_tool",
            "final": "final_answer",
        },
    )
    graph.add_edge("calculator_tool", "final_answer")
    graph.add_edge("final_answer", END)
    return graph.compile()


def initial_state(question: str) -> State:
    return {
        "question": question,
        "operation": "",
        "numbers": [],
        "tool_result": None,
        "answer": "",
        "trace": [],
    }


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke(initial_state("12 加 30 等于多少？"))
    print(result["answer"])
    print(result["trace"])
