# Outcome study: Glyph MCP vs grep (SWE-bench Lite, n=6)

Manual A/B. One human drives OpenCode TUI; the agent fixes real issues twice —
once with Glyph MCP tools, once with grep/glob/read only. Graded blind by the
official FAIL_TO_PASS tests.

## Result

| task | MCP | baseline |
|---|---|---|
| psf__requests-2674 (r2) | ✅ 12/12 · 85k in | ✅ 12/12 · 211k in |
| pallets__flask-4045 | ✅ 2/2 · 50k in | ✅ 2/2 · 84k in |
| pallets__flask-4992 | ✅ 1/1 · 100k in | ✅ 1/1 · 42k in |
| psf__requests-3362 | ✅ 1/1 · 54k in | ❌ wrong fix · 61k in |
| pallets__flask-5063 | ✅ 2/2 · 155k in | ✅ 2/2 · 81k in |
| psf__requests-2317 | ✅ 8/8 · 99k in | ✅ 8/8 · 39k in |

Solve rate **MCP 6/6, baseline 5/6**. Tokens-per-solve (input):
**MCP ~90k, baseline ~103k** — a wash at n=6 with large run-to-run variance
(same arm re-ran 93k→211k with nothing changed). The one split: 3362, where
MCP's fallback-decode passed and baseline's raise-TypeError failed.

Full per-arm detail (tokens in/out, reasoning, cache, tool counts, model
variant, wall time): `tasks/scoreboard.md`. Session exports, patches, and
per-arm prompts: `runs/`.

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
