# Scoreboard — I fill one row per task AFTER grading both arms

| task | mcp solved | mcp tokens (in/out) | mcp wall | base solved | base tokens (in/out) | base wall |
|------|-----------|---------------------|----------|-------------|----------------------|-----------|
| psf__requests-2674 (r2, both `high`) | y (12/12 F2P) | 85,255 / 2,796 (+4,674 reasoning; 1,142,981 cache read) | ~1.5 min | y (12/12 F2P) | 210,749 / 3,286 (+3,579 reasoning; 936,058 cache read) | ~2 min |
| psf__requests-2674 (r1, mixed variants — superseded) | y (12/12) | 96,844 / 1,857 | ~1 min | y (12/12) | 93,234 / 3,225 | ~2 min |
| pallets__flask-4045 | y (2/2 F2P) | 50,166 / 2,566 (+1,074 reasoning; 694,371 cache read) | ~1 min | y (2/2 F2P) | 84,188 / 2,678 (+1,880 reasoning; 745,398 cache read) | ~1.5 min |
| pallets__flask-4992 | y (1/1 F2P, graded py3.12) | 99,584 / 2,956 (+930 reasoning; 394,369 cache read) | ~1.5 min | y (1/1 F2P, graded py3.12) | 41,777 / 1,921 (+589 reasoning; 237,644 cache read) | ~1 min |
| psf__requests-3362 | y (1/1 F2P) | 53,960 / 2,468 (+1,714 reasoning; 695,395 cache read) | ~1.5 min | n (raises TypeError instead of fallback-decode) | 60,734 / 2,824 (+2,434 reasoning; 754,087 cache read) | ~2 min |
| pallets__flask-5063 | y (2/2 F2P, graded py3.12) | 155,134 / 3,678 (+1,795 reasoning; 806,582 cache read) | ~2.5 min | y (2/2 F2P, graded py3.12) | 80,530 / 3,519 (+566 reasoning; 497,733 cache read) | ~2.5 min |
| psf__requests-2317 | y (8/8 F2P) | 98,640 / 3,405 (+3,205 reasoning; 734,774 cache read) | ~1.5 min | y (8/8 F2P) | 39,070 / 2,266 (+1,300 reasoning; 564,338 cache read) | ~1 min |

Summary (final, n=6, r2 row for 2674):
- MCP solve rate: 6/6
- Base solve rate: 5/6
- MCP input tokens total: 85,255+50,166+99,584+53,960+155,134+98,640 = 542,739 → 90,457/solve
- Base input tokens total: 210,749+84,188+41,777+60,734+80,530+39,070 = 517,048 → 103,410/solve
- Median wall time per arm: ~1.5 min both

## Batch 2 (all `high`, frozen `tasks/pick2.txt`)

| task | mcp solved | mcp tokens (in/out) | mcp wall | base solved | base tokens (in/out) | base wall |
|------|-----------|---------------------|----------|-------------|----------------------|-----------|
| psf__requests-863 | y (4/4 F2P, 4-line fix) | 67,428 / 1,474 (+1,867 reasoning; 205,162 cache read) | ~1.5 min | y (4/4 F2P, 4-line fix) | 81,336 / 1,704 (+2,527 reasoning; 303,790 cache read) | ~1 min |
| psf__requests-2148 | y (10/10 F2P, 4-line fix) | 177,946 / 2,591 (+1,591 reasoning; 855,591 cache read) | ~3.5 min | n (9/10, 16-line fix, misses socket-error wrap) | 190,134 / 7,585 (+9,921 reasoning; 2,628,618 cache read) | long session, idle overnight |
| pytest-dev__pytest-7432 | y (1/1 F2P, 1-line fix) | 39,299 / 2,958 (+3,847 reasoning; 672,039 cache read) | ~2.5 min | y (1/1 F2P, 12-line rewrite) | 27,974 / 2,682 (+3,127 reasoning; 293,166 cache read) | ~1 min |
| pytest-dev__pytest-8906 (`xhigh` both arms) | y (1/1 F2P, 4-line fix) | 46,322 / 2,097 (+918 reasoning; 683,476 cache read) | ~1 min | y (1/1 F2P, 4-line fix) | 69,573 / 1,733 (+950 reasoning; 511,632 cache read) | ~1 min |
| mwaskom__seaborn-3407 (`xhigh` both) | n (crash fixed, diag_vars comparison missed) | 161,637 / 4,034 (+4,253 reasoning; 942,616 cache read) | ~3 min | n (same ambiguous-truth trap) | 103,546 / 3,397 (+2,616 reasoning; 607,256 cache read) | ~3 min |
| psf__requests-1963 (`high` both) | y (7/7 F2P, 5-line fix) | 68,870 / 2,769 (+2,796 reasoning; 276,428 cache read) | ~1 min | y (7/7 F2P, 5-line fix) | 38,455 / 3,687 (+1,917 reasoning; 684,267 cache read) | ~3 min |
## Summary

Batch 1 (all `high`): MCP 6/6, base 5/6. MCP input 542,739 (90,457/solve); base 517,048 (103,410/solve).
Batch 2 (`high` except 8906 + 3407 `xhigh` both arms): MCP 4/6, base 3/6.
Combined (12 tasks): MCP 10/12, base 8/12.

## Batch 4 = batch-3 django pair, run now (all `high` unless labeled)

| task | mcp solved | mcp tokens (in/out) | mcp wall | base solved | base tokens (in/out) | base wall |
|------|-----------|---------------------|----------|-------------|----------------------|-----------|
| django__django-11019 (r2, improved MCP) | y (16/16 F2P, 36+/40-) | 140,952 / 9,287 (+8,668 reasoning; 4,698,544 cache read) | ~3.5 min | y (9/16 F2P, 36+/40- rewrite) | 90,195 / 3,833 (+2,474 reasoning; 785,718 cache read) | ~1.5 min |
| django__django-11019 (r3 redo, opencode `muse-spark-1.3-contributor-free`) | y (16/16 F2P, 37+/40-, default variant) | 98,509 / 4,255 (+4,238 reasoning; 1,722,091 cache read) | ~3 min | y (16/16 F2P, 36+/40-, `medium` variant) | 63,060 / 3,938 (+2,453 reasoning; 1,066,505 cache read) | ~3 min |
| django__django-16820 | y (7/7 F2P, 65+ pure addition) | 95,254 / 3,929 (+2,544 reasoning; 2,231,328 cache read) | ~2 min | y (7/7 F2P, 65+ pure addition) | 70,563 / 4,870 (+2,195 reasoning; 1,497,790 cache read) | ~1.5 min |
| django__django-16820 (r3 redo, opencode `muse-spark-1.3-contributor-free`, both `medium`) | y (7/7 F2P, 65+ pure addition) | 53,639 / 5,735 (+3,196 reasoning; 2,527,204 cache read) | ~3 min | y (7/7 F2P, 65+ pure addition, `medium` variant) | 63,044 / 3,785 (+2,445 reasoning; 1,002,505 cache read) | ~4.5 min |

## Batch 3 refactors (r1, opencode `muse-spark-1.3-contributor-free`)

| task | mcp solved | mcp tokens (in/out) | mcp wall | base solved | base tokens (in/out) | base wall |
|------|-----------|---------------------|----------|-------------|----------------------|-----------|
| refactor__requests-rebuild-method | y (helper defined+called, 4 redirect tests pass, `medium`) | 34,164 / 2,469 (+1,330 reasoning; 332,108 cache read) | ~2 min | y (helper defined+called, 4 redirect tests pass, `medium`) | 25,717 / 2,829 (+1,356 reasoning; 253,403 cache read) | <1 min |
| refactor__pytest-xfail-extract | y (helper defined+called, 77 tests pass, `medium`) | 28,934 / 2,445 (+7,045 reasoning; 267,370 cache read) | ~1.5 min | y (helper defined+called, 77 tests pass, `medium`) | 34,812 / 3,389 (+6,937 reasoning; 574,819 cache read) | ~3 min |
| refactor__flask-routes-table | y (helper defined+called, 4 route tests pass, `medium`) | 24,527 / 2,435 (+1,348 reasoning; 291,148 cache read) | ~1 min | y (helper defined+called, 4 route tests pass, default variant) | 38,417 / 1,639 (+1,147 reasoning; 215,304 cache read) | <1 min |

## Batch 2 rerun r4 (pick2.txt, opencode `muse-spark-1.3-contributor-free`, web OFF both arms, raw statements, no hints)

Protocol deltas vs original batch 2: nested `.git` dirs were gone (publish scrub) — restored via shallow fetch + `reset --hard` to pinned base; fresh MCP keys; `tools.webfetch/websearch: false` in all 12 configs; prompts = frozen concise headers + raw `problem_statement`. Index vintage: batch-1/2 indexes predate the import-edge extractor fix — indexed commits verified equal to pinned base commits.

| task | mcp solved | mcp tokens (in/out) | mcp wall | base solved | base tokens (in/out) | base wall |
|------|-----------|---------------------|----------|-------------|----------------------|-----------|

Agent-reported tool value (16820, verbatim summary): get_context (squash path via
optimizer, callers/tests), search_code (warning source options.py + ModelState
handling), get_file_outline (optimizer mechanism), analyze_impact
(CreateModel.reduce: 10 dependents, mainly optimize_inner — safe to extend).
Web for ticket #34529/PR #16820 + commit diff (exact expected fix); final fix
matched upstream, self-verified by 39 optimizer tests + manual rename case.
Same division as 11019: MCP for code, web for canonical spec.

Agent-reported tool value (11019-r2, verbatim summary): get_context (first call,
Media.merge impl + callers + tests), get_file_outline + get_symbol (Media layout,
__add__ concatenates), search_code (merging sites + confirmed scenario not
in-repo), analyze_impact (only _css/_js + tests depend → safe signature change).
Web search used for canonical issue spec + upstream ticket 30179/PR 11019
(topological_sort + OrderedSet), not for code. Local search correctly had no
ColorPicker example — out of index scope by design.