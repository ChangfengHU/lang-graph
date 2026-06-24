# LangGraph 学习手册

你不要从“背 API”开始学 LangGraph。正确顺序是：

```text
看图 -> 看 State -> 看节点 -> 看边 -> 跑代码 -> 改代码 -> 再看图
```

每一课都按这个流程走。

## 每一课怎么学

以第 1 课为例。

### 1. 先看图

```bash
uv run python scripts/show_graph.py 01
```

你先确认这节课的流程长什么样：

```text
__start__ -> write_draft -> __end__
```

这一步回答一个问题：

```text
程序会按什么顺序执行？
```

### 2. 再读 State

打开：

```text
examples/01_hello_graph.py
```

先只看：

```python
class State(TypedDict):
    topic: str
    draft: str
```

这一步回答一个问题：

```text
整个流程中传来传去的数据有哪些？
```

第 1 课只有两个数据：

- `topic`：输入主题
- `draft`：生成出来的草稿

### 3. 再看节点

只看：

```python
def write_draft(state: State) -> dict:
    return {"draft": f"这是一段关于「{state['topic']}」的入门说明。"}
```

这一步回答两个问题：

```text
这个节点读取了 state 里的什么？
这个节点更新了 state 里的什么？
```

答案是：

- 读取：`topic`
- 更新：`draft`

### 4. 再看边

只看：

```python
graph.add_edge(START, "write_draft")
graph.add_edge("write_draft", END)
```

这一步回答一个问题：

```text
节点执行顺序是谁决定的？
```

答案是：边。

### 5. 跑代码

```bash
uv run python examples/01_hello_graph.py
```

你要盯住三段输出：

```text
[input] 初始 state
[node:write_draft] 收到 state
[output] 最终 state
```

这一步不是为了看一句中文输出，而是为了确认：

```text
state 进入图 -> 节点读 state -> 节点返回 partial update -> LangGraph 合并成最终 state
```

### 6. 必须改代码

不改代码，等于没学。

第 1 课你必须做 3 个改动。

#### 改动 1：换输入

把：

```python
input_state = {"topic": "LangGraph", "draft": ""}
```

改成：

```python
input_state = {"topic": "AI Agent", "draft": ""}
```

再运行：

```bash
uv run python examples/01_hello_graph.py
```

你要确认 `draft` 跟着变化。

#### 改动 2：增加一个 State 字段

把：

```python
class State(TypedDict):
    topic: str
    draft: str
```

改成：

```python
class State(TypedDict):
    topic: str
    audience: str
    draft: str
```

然后输入也要改：

```python
input_state = {"topic": "LangGraph", "audience": "零基础学习者", "draft": ""}
```

节点里使用它：

```python
return {"draft": f"这是一段写给{state['audience']}的「{state['topic']}」入门说明。"}
```

这一步你学的是：

```text
State 字段变了，输入 state 和节点逻辑也要跟着变。
```

#### 改动 3：增加第二个节点

新增：

```python
def polish_draft(state: State) -> dict:
    return {"draft": state["draft"] + " 建议先理解 State、Node、Edge 三个概念。"}
```

注册节点：

```python
graph.add_node("polish_draft", polish_draft)
```

改边：

```python
graph.add_edge(START, "write_draft")
graph.add_edge("write_draft", "polish_draft")
graph.add_edge("polish_draft", END)
```

再看图：

```bash
uv run python scripts/show_graph.py 01
```

你应该看到：

```text
__start__ -> write_draft -> polish_draft -> __end__
```

这一步你学的是：

```text
LangGraph 的“图”就是节点和边组合出来的执行流程。
```

## 每一课的学习目标

### 第 1 课：最小图

命令：

```bash
uv run python scripts/show_graph.py 01
uv run python examples/01_hello_graph.py
```

学会：

- 什么是 State
- 什么是 Node
- 什么是 Edge
- `invoke()` 怎么运行一张图

过关标准：

```text
你能自己增加第二个节点，并让图变成三段流程。
```

### 第 2 课：State 更新和 reducer

命令：

```bash
uv run python scripts/show_graph.py 02
uv run python examples/02_state_and_reducers.py
```

学会：

- 普通字段会被覆盖
- reducer 字段可以累积
- 为什么消息列表、步骤列表通常需要 reducer

过关标准：

```text
你能解释为什么 steps 最后有两项，而不是只剩最后一项。
```

### 第 3 课：条件路由

命令：

```bash
uv run python scripts/show_graph.py 03
uv run python examples/03_conditional_routing.py
```

学会：

- 图可以分支
- 路由函数只决定下一步
- 业务节点不应该混杂路由判断

过关标准：

```text
你能新增一个 category，比如 billing，并路由到新的节点。
```

### 第 4 课：Agent Loop

命令：

```bash
uv run python scripts/show_graph.py 04
uv run python examples/04_agent_loop.py
```

学会：

- planner 决定下一步
- tool 执行确定性动作
- final 生成最终答案
- 条件边是 agent 行为的骨架

过关标准：

```text
你能新增一个 subtraction 减法工具。
```

### 第 5 课：Checkpoint 记忆

命令：

```bash
uv run python scripts/show_graph.py 05
uv run python examples/05_memory_checkpoint.py
```

学会：

- 同一个 `thread_id` 会延续状态
- 不同 `thread_id` 状态隔离
- 记忆不是全局变量，而是 checkpoint

过关标准：

```text
你能证明 student-1 和 student-2 的消息不会串。
```

### 第 6 课：人工审批

命令：

```bash
uv run python scripts/show_graph.py 06
uv run python examples/06_human_in_loop.py
```

学会：

- `interrupt()` 会暂停图
- `Command(resume=...)` 会恢复图
- 恢复时必须使用同一个 `thread_id`

过关标准：

```text
你能把 approved=True 改成 False，并解释最终输出为什么变了。
```

### 第 7 课：Streaming

命令：

```bash
uv run python scripts/show_graph.py 07
uv run python examples/07_streaming.py
```

学会：

- `stream()` 可以看到节点级 update
- 前端进度条、日志、实时反馈都依赖 streaming

过关标准：

```text
你能说出每一行 streaming 输出来自哪个节点。
```

### 第 8 课：综合项目

命令：

```bash
uv run python scripts/show_graph.py 08
uv run python examples/08_research_assistant.py
```

学会：

- 多节点工作流
- state 累积
- 条件路由
- 人工审批
- 最终结构化报告

过关标准：

```text
你能把研究助手改成“短视频脚本助手”或“日报生成助手”。
```

## 你的每日学习节奏

每天只学一课，别贪多。

每课 40-60 分钟：

```text
5 分钟：看图
10 分钟：读 State、Node、Edge
10 分钟：运行代码
20 分钟：完成改代码练习
5 分钟：用自己的话写下这节课学到了什么
```

## 判断自己是否学会

不要问“我看懂了吗”。

问这 4 个问题：

```text
1. 这张图有哪些节点？
2. 每个节点读取和更新哪些 state 字段？
3. 边决定了怎样的执行顺序？
4. 如果我要加一个步骤，应该加 state、node，还是 edge？
```

这 4 个问题能答出来，才算学会。
