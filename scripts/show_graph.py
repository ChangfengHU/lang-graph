import argparse
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "examples"


def find_example(lesson: str) -> Path:
    lesson = lesson.zfill(2)
    matches = sorted(EXAMPLES_DIR.glob(f"{lesson}_*.py"))
    if not matches:
        available = ", ".join(path.name[:2] for path in sorted(EXAMPLES_DIR.glob("[0-9][0-9]_*.py")))
        raise SystemExit(f"找不到第 {lesson} 课。可用编号：{available}")
    return matches[0]


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise SystemExit(f"无法加载文件：{path}")
    spec.loader.exec_module(module)
    return module


def main() -> None:
    parser = argparse.ArgumentParser(description="显示某一课的 LangGraph 图。")
    parser.add_argument("lesson", help="课程编号，例如 01、02、08")
    parser.add_argument(
        "--format",
        choices=["ascii", "mermaid"],
        default="ascii",
        help="输出格式，默认 ascii",
    )
    args = parser.parse_args()

    example_path = find_example(args.lesson)
    module = load_module(example_path)

    if not hasattr(module, "build_graph"):
        raise SystemExit(f"{example_path} 里没有 build_graph()，不能自动显示图。")

    app = module.build_graph()
    graph = app.get_graph()

    print(f"[lesson] {example_path.relative_to(ROOT)}")
    if args.format == "ascii":
        print(graph.draw_ascii())
    else:
        print(graph.draw_mermaid())


if __name__ == "__main__":
    main()
