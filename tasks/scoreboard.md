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
