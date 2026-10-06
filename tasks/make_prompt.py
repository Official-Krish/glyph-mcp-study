"""Build the two frozen arm prompts for a task.

Usage: python tasks/make_prompt.py <instance_id>
Writes runs/<id>.prompt-mcp.txt and runs/<id>.prompt-base.txt.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
STUDY = HERE.parent

MCP_HEADER = """You are fixing a GitHub issue in this repository. Edit files to resolve it. When done, stop.
For code search and context, use the glyph MCP tools (search_code, get_context, get_symbol, find_references, analyze_impact, get_file_outline). Prefer them over grep.

ISSUE:
"""

BASE_HEADER = """You are fixing a GitHub issue in this repository. Edit files to resolve it. When done, stop.
For code search and context, use grep, glob, and read.

ISSUE:
"""


def main() -> None:
    task_id = sys.argv[1]
    with open(STUDY / "tasks" / "swe_lite.json") as f:
        tasks = json.load(f)
    match = [t for t in tasks if t["id"] == task_id]
    if not match:
        raise SystemExit(f"task {task_id} not in tasks/swe_lite.json")
    stmt = match[0]["statement"]
    with open(STUDY / "runs" / f"{task_id}.prompt-mcp.txt", "w") as f:
        f.write(MCP_HEADER + stmt + "\n")
    with open(STUDY / "runs" / f"{task_id}.prompt-base.txt", "w") as f:
        f.write(BASE_HEADER + stmt + "\n")
    print(f"wrote runs/{task_id}.prompt-{{mcp,base}}.txt")


if __name__ == "__main__":
    main()
