import importlib.util
from pathlib import Path

from langgraph.types import Command


ROOT = Path(__file__).resolve().parents[1]


def load_example(name: str):
    path = ROOT / "examples" / name
    spec = importlib.util.spec_from_file_location(name.replace(".py", ""), path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_hello_graph():
    module = load_example("01_hello_graph.py")
    result = module.build_graph().invoke({"topic": "LangGraph", "draft": ""})
    assert "LangGraph" in result["draft"]


def test_reducer_accumulates_steps():
    module = load_example("02_state_and_reducers.py")
    result = module.build_graph().invoke({"topic": "LangGraph", "outline": "", "steps": []})
    assert result["steps"] == ["生成大纲", "补充进阶章节"]


def test_conditional_routing_urgent():
    module = load_example("03_conditional_routing.py")
    result = module.build_graph().invoke({"user_input": "紧急故障", "category": "", "answer": ""})
    assert result["category"] == "urgent"
    assert "紧急" in result["answer"]


def test_agent_loop_calculates():
    module = load_example("04_agent_loop.py")
    result = module.build_graph().invoke(module.initial_state("7 乘 6"))
    assert result["tool_result"] == 42
    assert "42" in result["answer"]


def test_checkpoint_keeps_thread_memory():
    module = load_example("05_memory_checkpoint.py")
    app = module.build_graph()
    config = {"configurable": {"thread_id": "test-memory"}}
    app.invoke({"messages": ["user: one"]}, config)
    result = app.invoke({"messages": ["user: two"]}, config)
    assert any("第 2 轮" in message for message in result["messages"])


def test_human_in_loop_resume():
    module = load_example("06_human_in_loop.py")
    app = module.build_graph()
    config = {"configurable": {"thread_id": "test-hitl"}}
    paused = app.invoke({"topic": "审批", "draft": "", "approved": False, "final": ""}, config)
    assert "__interrupt__" in paused
    resumed = app.invoke(Command(resume={"approved": True}), config)
    assert resumed["approved"] is True
    assert "已发布" in resumed["final"]


def test_research_assistant_report():
    module = load_example("08_research_assistant.py")
    app = module.build_graph()
    result = app.invoke(module.initial_state("LangGraph"), {"configurable": {"thread_id": "test-report"}})
    assert "# LangGraph 研究报告" in result["report"]
