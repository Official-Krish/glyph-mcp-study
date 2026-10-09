#!/usr/bin/env python3
"""Per-call token ledger for study sessions.

Walks an opencode session export and attributes tokens per step:
each assistant step's input tokens are charged to the tool call(s)
made in that step; output tokens are the step's response size.

Usage:
  scripts/ledger.py runs/<task>-<arm>[-rN].session.json     # one session
  scripts/ledger.py --all                                    # all sessions, table
"""
import glob
import json
import sys

FAMILIES = (
    ("mcp", "code-context_"),
    ("bash", "bash"),
    ("read", "read"),
    ("web", "webfetch"),
    ("web", "websearch"),
    ("edit", "edit"),
    ("write", "write"),
)


def family(tool: str) -> str:
    for fam, prefix in FAMILIES:
        if tool.startswith(prefix):
            return fam
    return "other"


def ledger(path: str) -> dict:
    d = json.load(open(path))
    steps = []
    calls: dict[str, int] = {}
    step_input: dict[str, int] = {}
    for m in d["messages"]:
        info = m.get("info", {})
        if info.get("role") != "assistant":
            continue
        tools = [
            p.get("tool", "?")
            for p in m.get("parts", [])
            if p.get("type") == "tool"
        ]
        tok = info.get("tokens", {})
        steps.append(
            {
                "n": len(steps) + 1,
                "input": tok.get("input", 0),
                "output": tok.get("output", 0),
                "cache_read": tok.get("cache", {}).get("read", 0),
                "tools": tools,
            }
        )
        for t in tools:
            calls[t] = calls.get(t, 0) + 1
            step_input[t] = step_input.get(t, 0) + tok.get("input", 0)
    fam_calls: dict[str, int] = {}
    fam_input: dict[str, int] = {}
    for t, c in calls.items():
        f = family(t)
        fam_calls[f] = fam_calls.get(f, 0) + c
        fam_input[f] = fam_input.get(f, 0) + step_input.get(t, 0)
    return {
        "session": path.split("/")[-1].replace(".session.json", ""),
        "model": d.get("info", {}).get("model"),
        "total": d.get("info", {}).get("tokens", {}),
        "steps": steps,
        "calls": calls,
        "fam_calls": fam_calls,
        "fam_input": fam_input,
    }


def show_one(path: str) -> None:
    L = ledger(path)
    print(f"== {L['session']}  ({L['model']})")
    t = L["total"]
    print(f"total in={t.get('input')} out={t.get('output')} cached={t.get('cache', {}).get('read')}")
    print(f"{'step':>4} {'input':>8} {'output':>7}  tools")
    for s in L["steps"]:
        tools = ",".join(
            t.replace("code-context_", "mcp:") for t in s["tools"]
        )
        print(f"{s['n']:>4} {s['input']:>8} {s['output']:>7}  {tools}")
    print("-- avg context size when each family was called --")
    for fam in sorted(L["fam_calls"]):
        avg = L["fam_input"][fam] // max(1, L["fam_calls"][fam])
        print(f"  {fam}: x{L['fam_calls'][fam]} avg_ctx={avg}")


def show_all() -> None:
    rows = []
    for f in sorted(glob.glob("runs/*.session.json")):
        try:
            L = ledger(f)
        except Exception as e:  # corrupt export, skip loudly
            print(f"SKIP {f}: {e}")
            continue
        t = L["total"]
        fams = " ".join(
            f"{k}={v}" for k, v in sorted(L["fam_calls"].items())
        )
        rows.append(
            (L["session"], t.get("input"), t.get("output"), len(L["steps"]), fams)
        )
    print(f"{'session':<42} {'input':>8} {'output':>7} {'steps':>5}  calls")
    for s, i, o, n, fams in rows:
        print(f"{s:<42} {i:>8} {o:>7} {n:>5}  {fams}")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--all":
        show_all()
    elif len(sys.argv) == 2:
        show_one(sys.argv[1])
    else:
        sys.exit(__doc__)
