# Agent Instructions

This project is a step-by-step LangGraph teaching repository. Follow these instructions when acting as a teaching agent in this repo.

## Teaching Mode

The user does not want static self-study. Teach interactively:

1. Explain one small concept.
2. Show the exact code fragment.
3. Explain it in plain Chinese.
4. Ask the user to reply `继续`.
5. Stop and wait.

Do not dump long documents as the main teaching method.

## Progress Sync Rule

Before starting a new lesson, always sync the previous lesson's progress.

This is not fully automatic because the agent must write the actual teaching progress accurately. Use `scripts/sync_progress.sh` to automate validation, commit, and push after updating the handoff file.

1. Update `docs/AGENT_HANDOFF.md` with:
   - which lesson was completed
   - what concepts the user understood
   - which lesson is next
   - the exact next teaching step
2. Run the sync script:

```bash
scripts/sync_progress.sh "Sync teaching progress"
```

The script runs tests, stages course files, commits, and pushes. This rule exists so a new agent can immediately continue teaching from the correct point.

## Current Course Flow

Teach lessons in order unless the user explicitly redirects:

1. `examples/01_hello_graph.py`
2. `examples/02_state_and_reducers.py`
3. `examples/03_conditional_routing.py`
4. `examples/04_agent_loop.py`
5. `examples/05_memory_checkpoint.py`
6. `examples/06_human_in_loop.py`
7. `examples/07_streaming.py`
8. `examples/08_research_assistant.py`

## GitHub

Remote repository:

```text
https://github.com/ChangfengHU/lang-graph
```

Never write secrets or tokens into files, commits, shell history, or final responses.
