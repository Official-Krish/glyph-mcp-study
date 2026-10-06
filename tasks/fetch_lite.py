"""Dump SWE-bench Lite metadata to tasks/swe_lite.json.

Run:  source .venv/bin/activate && python tasks/fetch_lite.py
"""
import ast
import json
from pathlib import Path

from datasets import load_dataset

OUT = Path(__file__).parent / "swe_lite.json"


def as_list(v):
    if isinstance(v, list):
        return list(v)
    if isinstance(v, str):
        try:
            return json.loads(v)
        except json.JSONDecodeError:
            return list(ast.literal_eval(v))
    return list(v)

ds = load_dataset("princeton-nlp/SWE-bench_Lite", split="test")
lite = [
    {
        "id": r["instance_id"],
        "repo": r["repo"],
        "base": r["base_commit"],
        "test_patch": r["test_patch"],
        "fail2pass": as_list(r["FAIL_TO_PASS"]),
        "pass2pass": as_list(r["PASS_TO_PASS"]),
        "statement": r["problem_statement"],
    }
    for r in ds
]
with open(OUT, "w") as f:
    json.dump(lite, f)
print(f"{len(lite)} instances saved to {OUT}")
repos = sorted({t["repo"] for t in lite})
print("repos:", ", ".join(repos))
