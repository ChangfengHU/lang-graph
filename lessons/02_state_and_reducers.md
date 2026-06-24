# 第 2 课：State 更新和 reducer

第 1 课只有一个节点，所以你还看不出多个节点更新 state 时会发生什么。

第 2 课有两个节点：

```text
START -> make_outline -> polish_outline -> END
```

先看图：

```bash
uv run python scripts/show_graph.py 02
```

## 这节课解决什么问题

如果两个节点都更新同一个字段，LangGraph 怎么处理？

答案分两种：

```text
普通字段：后一次更新会写回 state
reducer 字段：按你指定的 reducer 合并
```

## State

```python
class State(TypedDict):
    topic: str
    outline: str
    steps: Annotated[list[str], operator.add]
```

这里最关键的是：

```python
steps: Annotated[list[str], operator.add]
```

它的意思是：

```text
如果多个节点都返回 steps，就用 operator.add 合并。
```

对于 list 来说：

```python
["生成大纲"] + ["补充进阶章节"]
```

结果是：

```python
["生成大纲", "补充进阶章节"]
```

## 节点 1：make_outline

它返回：

```python
{
    "outline": "1. 什么是 LangGraph ...",
    "steps": ["生成大纲"],
}
```

这时 state 里：

```text
outline 有了初版大纲
steps 有了第一步记录
```

## 节点 2：polish_outline

它返回：

```python
{
    "outline": state["outline"] + "\n4. 常见坑和最佳实践",
    "steps": ["补充进阶章节"],
}
```

这时：

```text
outline 被更新成更完整的大纲
steps 不是覆盖，而是累加
```

## 最终结果

```python
steps == ["生成大纲", "补充进阶章节"]
```

如果 `steps` 没有 reducer，第二个节点返回的 `["补充进阶章节"]` 会覆盖前面的 `["生成大纲"]`。

## 过关练习

新增第三个节点：

```python
def add_examples(state: State) -> dict:
    return {
        "outline": state["outline"] + "\n5. 示例代码",
        "steps": ["补充示例"],
    }
```

把图改成：

```text
START -> make_outline -> polish_outline -> add_examples -> END
```

最终 `steps` 应该是：

```python
["生成大纲", "补充进阶章节", "补充示例"]
```
