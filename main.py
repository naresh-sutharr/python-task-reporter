#!/usr/bin/env python3
"""Small CLI tool: read JSON tasks, call a mock API, and write useful reports."""

import argparse
import json
from pathlib import Path
from datetime import datetime, timezone


def read_input(path: Path) -> list[dict]:
    """Load and validate tasks from a JSON file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Input file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list):
        raise SystemExit("Input JSON must be a list of task objects.")

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict) or "task" not in item:
            raise SystemExit(f"Item {index} must be an object with a 'task' field.")
    return data


def mock_api(task: str) -> dict:
    """Mock an AI-adjacent API so the project runs without API keys or internet."""
    cleaned = " ".join(task.split())
    words = cleaned.split()
    return {
        "input": cleaned,
        "word_count": len(words),
        "character_count": len(cleaned),
        "summary": f"Task contains {len(words)} words.",
        "status": "mock_api_success",
    }


def process_tasks(tasks: list[dict]) -> list[dict]:
    """Call the mock API for each task and return structured results."""
    results = []
    for item in tasks:
        task = str(item["task"])
        results.append({
            "task_id": item.get("id", len(results) + 1),
            "result": mock_api(task),
        })
    return results


def write_output(results: list[dict], output_dir: Path) -> None:
    """Write JSON data and a human-readable Markdown report."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "api_mode": "mock",
        "total_tasks": len(results),
        "results": results,
    }
    (output_dir / "report.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Python Task Report",
        "",
        f"- Generated (UTC): {payload['generated_at_utc']}",
        "- API mode: mock API (no key required)",
        f"- Tasks processed: {len(results)}",
        "",
        "## Results",
        "",
    ]
    for row in results:
        result = row["result"]
        lines.extend([
            f"### Task {row['task_id']}",
            "",
            f"- Input: {result['input']}",
            f"- Word count: {result['word_count']}",
            f"- Character count: {result['character_count']}",
            f"- Mock API status: `{result['status']}`",
            "",
        ])
    (output_dir / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read tasks from JSON, process them with a mock API, and write reports."
    )
    parser.add_argument("--input", default="sample_input.json", help="Path to input JSON file")
    parser.add_argument("--output-dir", default="output", help="Directory for generated reports")
    args = parser.parse_args()

    tasks = read_input(Path(args.input))
    results = process_tasks(tasks)
    write_output(results, Path(args.output_dir))
    print(f"Processed {len(results)} task(s).")
    print(f"Wrote: {args.output_dir}/report.json")
    print(f"Wrote: {args.output_dir}/report.md")


if __name__ == "__main__":
    main()
