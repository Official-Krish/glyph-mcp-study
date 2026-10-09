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
This repo is indexed by Glyph over MCP. Rules:
- Call `get_context` BEFORE reading any files. One call replaces grep/glob/read for exploration.
- Code shown in MCP output IS the source. Cite the shown line numbers and edit directly — never re-read a file already shown in MCP output.
- Use bash ONLY for: running tests, or checking a runtime value that cannot be answered from code. NOT for file reading, grep, or exploration.
- Check `analyze_impact` before modifying any shared function, type, or API.
- After editing, run the single most relevant test with -q. If it passes, stop — do not run extra verification.

MCP tools: search_code, get_context, get_symbol, find_references, analyze_impact, get_file_outline.

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
