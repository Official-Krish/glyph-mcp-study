# SWE-bench Lite A/B runbook — YOU drive OpenCode TUI, agent fixes, MCP vs grep

## 0. One-time setup — DONE BY ME, skip to section 1

- [x] Glyph stack booted (api :3000, mcp :3002, worker, db, redis, ollama embed)
- [x] Dataset at `tasks/swe_lite.json`
- [x] Frozen picks in `tasks/pick.txt`
- [x] Checkouts + venvs in `runs/`
- [x] Each MCP checkout indexed in Glyph, per-task key in `configs/mcp-<ID>.json`

## 1. Per task — YOUR part (example ID: psf__requests-2674)

### 1.1 MCP arm
Paste into your terminal (in `~/Desktop/test/swe-study`):
```sh
cd runs/psf__requests-2674-mcp
OPENCODE_CONFIG=../../configs/mcp-psf__requests-2674.json opencode
```
Inside the TUI: check `/model` shows the agreed model. Then paste the prompt
from `runs/psf__requests-2674.prompt-mcp.txt` (file contents below in section 3).
Let the agent work until it stops. Optionally ask it "which tools did you use
for search?" to confirm glyph tools were used. Exit the TUI (`/exit`).
Tell me: "mcp done".

### 1.2 Baseline arm
```sh
cd ~/Desktop/test/swe-study/runs/psf__requests-2674-base
OPENCODE_CONFIG=../../configs/base.json opencode
```
Verify `/model` is the SAME model. Paste `runs/psf__requests-2674.prompt-base.txt`.
Exit. Tell me: "base done".

### 1.3 What I do when you report
I snapshot `opencode stats`, save your diffs, grade FAIL_TO_PASS, and log the
row in `tasks/scoreboard.md`. Then I hand you the next task's launch + prompt.

## 2. Rules
- Paste prompts verbatim. Never mention tests to the agent.
- Same `/model` in ALL sessions — verify every time.
- Empty diff = valid `not solved`. No re-runs.
- Lite may be memorized — noted; the GAP is still meaningful.
