from typing_extensions import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    # State 是整张图共享的数据结构。
    # 你可以把它理解成“工作流上下文”：
    # - 每个节点都能读取它
    # - 每个节点可以返回一小部分字段来更新它
    topic: str
    draft: str


def write_draft(state: State) -> dict:
    # node 本质上就是一个普通 Python 函数。
    # LangGraph 会把当前 state 传进来。
    print("[node:write_draft] 收到 state:", state)

    # 这里故意只返回 draft，不返回 topic。
    # 这说明节点不需要返回完整 state，只返回“要更新的字段”即可。
    return {"draft": f"这是一段关于「{state['topic']}」的入门说明。"}


def build_graph():
    # StateGraph(State) 表示：创建一张图，并声明这张图的状态结构是 State。
    # 之后所有节点都围绕这个 State 读写数据。
    graph = StateGraph(State)

    # add_node 给图注册一个节点。
    # 左边的 "write_draft" 是节点名字，右边的 write_draft 是真正执行的函数。
    graph.add_node("write_draft", write_draft)

    # START 是 LangGraph 内置入口。
    # 这条边表示：图一启动，就先执行 write_draft 节点。
    graph.add_edge(START, "write_draft")

    # END 是 LangGraph 内置出口。
    # 这条边表示：write_draft 执行完，整张图结束。
    graph.add_edge("write_draft", END)

    # compile() 会把你声明的“图结构”编译成一个可运行对象。
    # 只有 compile 之后，才能 invoke / stream。
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    print("[graph] 这才是 LangGraph 里的“图”：")
    print(app.get_graph().draw_ascii())

    print("[mermaid] 同一张图的 Mermaid 表达，可以贴到 Markdown 里渲染：")
    print(app.get_graph().draw_mermaid())

    # invoke 的输入就是初始 state。
    # topic 是用户给定的主题，draft 先留空，等待节点生成。
    input_state = {"topic": "LangGraph", "draft": ""}
    print("[input] 初始 state:", input_state)

    # 运行过程：
    # START -> write_draft -> END
    # write_draft 返回 {"draft": "..."} 后，LangGraph 会把这个 partial update 合并回 state。
    result = app.invoke(input_state)

    print("[output] 最终 state:", result)
    print("\n你刚刚验证了 4 件事：")
    print("1. LangGraph 的输入是一份 state。")
    print("2. node 是一个接收 state、返回 dict 的普通函数。")
    print("3. node 返回的 dict 会更新 state。")
    print("4. edge 决定节点执行顺序：START -> write_draft -> END。")
