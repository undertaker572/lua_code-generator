import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from app.agents import AgentNetwork


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local Lua Agent System")
    parser.add_argument("--task", required=True, help="Natural language task in Russian or English.")
    parser.add_argument("--lang", default="auto", help="Language hint: ru, en, or auto.")
    parser.add_argument("--clarifications", default="", help="Optional clarification answers.")
    parser.add_argument("--output", default="output/result.json", help="Path to JSON output report.")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    max_loops = int(os.getenv("MAX_REFINEMENT_LOOPS", "1"))
    result = AgentNetwork(max_refinement_loops=max_loops).run(
        user_task=args.task,
        language=args.lang,
        clarifications=args.clarifications,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Final Lua ===")
    print(result["final_lua"])
    print("\n=== Validation Report ===")
    print(result["validation_report"])
    print(f"\nSaved report to: {output_path}")


if __name__ == "__main__":
    main()
