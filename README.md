# Outcome study: Glyph MCP vs grep (SWE-bench Lite, n=12)

Manual A/B. One human drives OpenCode TUI; the agent fixes real issues twice —
once with Glyph MCP tools, once with grep/glob/read only. Graded blind by the
official FAIL_TO_PASS tests.

## Result (combined)

Solve rate **MCP 10/12, baseline 8/12**.

| task | MCP | baseline |
|---|---|---|
| psf__requests-2674 (r2) | ✅ 12/12 · 85k in · 4-line | ✅ 12/12 · 211k in |
| pallets__flask-4045 | ✅ 2/2 · 50k in | ✅ 2/2 · 84k in |
| pallets__flask-4992 | ✅ 1/1 · 100k in | ✅ 1/1 · 42k in |
| psf__requests-3362 | ✅ 1/1 · 54k in | ❌ wrong fix · 61k in |
| pallets__flask-5063 | ✅ 2/2 · 155k in | ✅ 2/2 · 81k in |
| psf__requests-2317 | ✅ 8/8 · 99k in | ✅ 8/8 · 39k in |
| psf__requests-863 | ✅ 4/4 · 67k in · 4-line | ✅ 4/4 · 81k in · 4-line |
| psf__requests-2148 | ✅ 10/10 · 178k in · 4-line | ❌ 9/10 · 190k in · 16-line |
| pytest-dev__pytest-7432 | ✅ 1/1 · 39k in · 1-line | ✅ 1/1 · 28k in · 12-line |
| pytest-dev__pytest-8906 | ✅ 1/1 · 46k in · 4-line | ✅ 1/1 · 70k in · 4-line |
| mwaskom__seaborn-3407 | ❌ near-miss · 162k in | ❌ same trap · 104k in |
| psf__requests-1963 | ✅ 7/7 · 19k in · 5-line | ✅ 7/7 · 38k in · 5-line |

MCP-only solves (2): 3362 (fallback-decode vs TypeError), 2148 (socket-error
wrap vs 9/10 miss) — both needed context beyond the obvious file. Both-fail
(1): 3407, identical numpy ambiguous-truth trap — task hardness, not tooling.
Tokens-per-solve is a wash with large run-to-run variance; fix sizes skew
minimal on MCP solves (1/4/4/5-line) vs occasional baseline rewrites
(12/16-line).

Full per-arm detail (tokens in/out, reasoning, cache, tool counts, model
variant, wall time): `tasks/scoreboard.md`. Session exports, patches, and
per-arm prompts: `runs/`. Batch 1 = `tasks/pick.txt`, batch 2 = `tasks/pick2.txt`.
Variant log: batch 1 all `high` (2674-r1 mixed, superseded); batch 2 `high`
except 8906 + 3407 matched-`xhigh` pairs (kept, labeled).

## Protocol (frozen before run 1)

- Task list frozen in `tasks/pick.txt` — 6 instances, requests + flask (fast suites).
- Same model + variant every session (`muse-spark-1.3-contributor-free`, `high`).
  2674-r1 ran mixed variants and is superseded (kept in scoreboard, excluded).
- Prompts frozen (`tasks/make_prompt.py`): same issue text both arms; MCP arm
  names the glyph tools, baseline arm names grep/glob/read. Never the tests.
- Fresh checkout per arm at the pinned `base_commit`; agent diff saved BEFORE
  applying the test patch (`scripts/grade.py`).
- Arm-validity rule: an MCP run with zero MCP tool calls is void and re-run
  (happened once, 2674-r2 first attempt — discarded, checkout reset).
- Flask eras need era deps for grading: `werkzeug==2.2.2`, `pytest==7.4.*`,
  and 4992/5063 grade under Python 3.12 (tomllib). Identical grading env both
  arms. `GRADE_VENV=.venv312` selects it.

## Reproduce

1. Boot a Glyph stack (api, worker, mcp-server, Postgres, Redis, Ollama).
2. Index each `<id>-mcp` checkout; mint a per-repo `ctx_live_…` key.
3. Put the key in `<id>-mcp/opencode.json` (`code-context` remote MCP);
   `<id>-base/opencode.json` stays MCP-free.
4. Paste `runs/<id>.prompt-{mcp,base}.txt` into OpenCode TUI in each dir.
5. `scripts/grade.py <id> runs/<id>-<arm>` after saving the diff.

## Secrets note

All `ctx_live_…` keys in this folder are **revoked server-side** (deleted from
the database before publishing) and replaced with a placeholder. They will
not authenticate anywhere. Mint your own against your own stack to reproduce.
