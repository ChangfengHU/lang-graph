# LangGraph 从入门到精通：代码驱动课程

这个仓库是一套面向零基础的 LangGraph 学习路线。它不是只讲概念，而是把每个核心概念都落到可运行代码里。

不知道怎么开始时，先读：

- `STUDY_GUIDE.md`

如果新的 agent 接手这个教学项目，先读：

- `docs/AGENT_HANDOFF.md`

## 先决条件

- 推荐使用 `uv`
- Python 3.10+

安装依赖：

```bash
uv sync
```

运行全部测试：

```bash
uv run pytest
```

运行任意课程示例：

```bash
uv run python examples/01_hello_graph.py
uv run python examples/06_human_in_loop.py
```

只看某一课的图：

```bash
uv run python scripts/show_graph.py 01
uv run python scripts/show_graph.py 04
uv run python scripts/show_graph.py 04 --format mermaid
```

## 学习路线

### 第 1 阶段：先理解 LangGraph 在解决什么问题

目标：知道 LangGraph 不是“聊天 API 封装”，而是 agent / workflow 编排框架。

你要掌握：

- `StateGraph`：定义状态机 / 工作流图
- `State`：节点之间共享的数据结构
- `node`：一个普通 Python 函数
- `edge`：节点之间的执行顺序
- `START` / `END`：图的入口和出口

对应代码：

- `examples/01_hello_graph.py`
- `lessons/01_hello_graph.md`

### 第 2 阶段：状态与 reducer

目标：理解 LangGraph 的状态更新不是随便改变量，而是“节点返回 partial state update”。

你要掌握：

- 节点只返回自己负责更新的字段
- 普通字段会覆盖
- reducer 字段可以累积，比如列表追加
- 为什么 agent 需要把消息、步骤、工具结果都放进 state

对应代码：

- `examples/02_state_and_reducers.py`
- `lessons/02_state_and_reducers.md`

### 第 3 阶段：条件路由

目标：让图从线性流程变成可分支流程。

你要掌握：

- `add_conditional_edges`
- 路由函数只负责判断下一步
- 业务节点只负责业务逻辑
- 复杂 agent 的可控性来自显式路由

对应代码：

- `examples/03_conditional_routing.py`

### 第 4 阶段：工具调用与 agent loop

目标：理解 ReAct / tool-calling agent 的本质：模型决定是否调用工具，图负责执行和回到模型。

这个仓库先用 mock planner 模拟 LLM，避免你第一天就被 API Key、模型兼容性和账单干扰。

你要掌握：

- planner 节点如何决定下一步
- tool 节点如何只做确定性计算
- 条件边如何形成循环
- 最终回答如何由 state 组装出来

对应代码：

- `examples/04_agent_loop.py`

### 第 5 阶段：短期记忆与 checkpoint

目标：理解“多轮会话”和“可恢复执行”依赖 checkpoint，而不是全局变量。

你要掌握：

- `InMemorySaver`
- `thread_id`
- 同一 thread 里的状态延续
- 不同 thread 之间的隔离

对应代码：

- `examples/05_memory_checkpoint.py`

### 第 6 阶段：Human-in-the-loop

目标：让工作流在关键节点暂停，等人类审批后继续。

你要掌握：

- `interrupt()`
- `Command(resume=...)`
- 为什么必须使用同一个 `thread_id` 恢复
- 审批、修改、拒绝这类场景如何落图

对应代码：

- `examples/06_human_in_loop.py`

### 第 7 阶段：Streaming

目标：把“最终一次性返回结果”升级为“运行过程可观察”。

你要掌握：

- `graph.stream(..., stream_mode="updates")`
- 每个节点的 state update
- 如何给前端展示进度

对应代码：

- `examples/07_streaming.py`

### 第 8 阶段：综合项目

目标：把前面所有概念组合成一个小型“研究报告助手”。

你要掌握：

- 多节点 workflow
- 条件路由
- state 累积
- 人工审批点
- 最终结构化输出

对应代码：

- `examples/08_research_assistant.py`

## 建议学习节奏

### 第 1 周：图和状态

只看 `01`、`02`、`03`。每个文件至少改 3 次：

- 增加一个 state 字段
- 增加一个 node
- 改一次路由条件

### 第 2 周：agent loop

重点看 `04`。你要能手写下面这条链路：

```text
用户问题 -> planner -> 是否需要工具 -> tool -> planner/final -> 答案
```

### 第 3 周：记忆和人工介入

重点看 `05`、`06`。这是 LangGraph 相比普通链式调用最重要的部分。

### 第 4 周：工程化

重点看 `07`、`08` 和 `tests/`。你需要开始用测试保护节点逻辑，而不是靠手动运行。

### 第 5-8 周：进阶到生产

把 mock planner 换成真实 LLM：

- 用 LangChain chat model 或 OpenAI SDK 写 planner
- 给工具加参数校验
- 把 `InMemorySaver` 换成 Postgres checkpoint
- 接入 LangSmith 做 tracing
- 把图包装成 FastAPI 服务
- 增加权限审批、重试、超时和错误恢复

## 官方文档建议阅读顺序

1. LangGraph Overview
2. Quickstart
3. Graph API
4. Persistence / Memory
5. Interrupts
6. Streaming
7. Testing

## 学习原则

每学一个概念，都回答 4 个问题：

1. 这个状态字段是谁写入的？
2. 这个节点是否只做一件事？
3. 这条边为什么指向下一个节点？
4. 如果中途失败，是否可以恢复？
