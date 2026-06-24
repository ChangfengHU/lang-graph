# Agent Handoff: LangGraph Teaching Repo

This repository is a runnable, code-first LangGraph course for a complete beginner.

## Current Teaching Status

Teaching is paused during Lesson 2.

Completed with the user:

- Lesson 1: `examples/01_hello_graph.py`
- Conceptual model:
  - `State` = data passed through the graph
  - `Node` = Python function that reads state and returns a partial state update
  - `Edge` = execution order between nodes
  - `Graph` = nodes plus edges
  - `invoke()` = run a compiled graph with an initial state
- The user understood the first lesson and said: "第一节可以了 很基础"

Started but not completed:

- Lesson 2: `examples/02_state_and_reducers.py`
- The opening setup was given:
  - show graph with `uv run python scripts/show_graph.py 02`
  - explain that Lesson 2 has `make_outline` then `polish_outline`
  - introduce the core question: when multiple nodes update state, does LangGraph overwrite or accumulate?
- The `State` definition was explained:
  - `topic` = topic
  - `outline` = outline text
  - `steps` = execution-step list
  - `steps: Annotated[list[str], operator.add]` means multiple returned lists are accumulated with `+`
  - plain explanation given: normal fields are written back; reducer fields are merged by the configured rule

Next teaching step:

- Continue Lesson 2 by explaining the first node `make_outline`.
- Show only this fragment first:

```python
def make_outline(state: State) -> dict:
    print("[node:make_outline] 收到 state:", state)
    return {
        "outline": f"1. 什么是{state['topic']}\n2. 为什么需要它\n3. 如何开始",
        "steps": ["生成大纲"],
    }
```

Focus on:

- it reads `state["topic"]`
- it returns a new `outline`
- it returns `steps: ["生成大纲"]`
- this is the first contribution to the reducer-backed `steps` list

## Required Teaching Style

The user explicitly does not want to read static documentation alone. Do not dump a long guide and ask them to self-study.

Use this pattern:

1. Explain one small idea.
2. Show the exact code fragment.
3. Explain what it means in plain Chinese.
4. Ask the user to reply `继续`.
5. Wait.

Keep each teaching message short. The user wants step-by-step guidance.

Good style:

```text
第 2 步：看 State

只看这一段...

你现在只需要记住一句...

你回复：继续
```

Avoid:

- Long lectures
- Large pasted docs
- Multiple concepts in one response
- "Go read README" as the main instruction

## Required Progress Sync

Before starting a new lesson, update this handoff document with the previous lesson's completed status, then run the sync script.

Standard command:

```bash
scripts/sync_progress.sh "Sync teaching progress"
```

This is semi-automatic: the script handles tests, commit, and push; the agent is still responsible for accurately updating this handoff file before running it.

## Repo Structure

- `README.md`: overview and command list
- `STUDY_GUIDE.md`: full self-study plan, useful as reference but not the active teaching mode
- `lessons/`: written lesson notes
- `examples/`: runnable LangGraph examples
- `scripts/show_graph.py`: show a lesson graph by number
- `tests/`: pytest coverage for example behavior

## Useful Commands

Install dependencies:

```bash
uv sync
```

Run tests:

```bash
uv run pytest
```

Show a graph:

```bash
uv run python scripts/show_graph.py 01
uv run python scripts/show_graph.py 02
uv run python scripts/show_graph.py 04 --format mermaid
```

Run examples:

```bash
uv run python examples/01_hello_graph.py
uv run python examples/02_state_and_reducers.py
```

## Validation Status

Last known validation:

```text
uv run pytest
7 passed
```

Before making further teaching-code changes, run:

```bash
uv run pytest
```

## Security Note

The user pasted a GitHub token in the chat while asking to publish this repo. Do not write that token into files, commits, shell history, README, docs, or final responses.
