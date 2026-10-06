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
