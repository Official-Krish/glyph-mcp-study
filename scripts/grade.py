"""Grade one arm: apply the test patch, run FAIL_TO_PASS with the checkout venv.

Usage: python scripts/grade.py <instance_id> runs/<id>-<arm>

Must run AFTER the model diff is saved (grading mutates the checkout).
Prints PASS/FAIL per test and a final SOLVED / NOT SOLVED verdict.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

STUDY = Path(__file__).parent.parent
# Override grading interpreter, e.g. GRADE_VENV=.venv312 to re-grade under
# a different Python without touching the agent's runtime env.
GRADE_VENV = os.environ.get("GRADE_VENV", ".venv")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main() -> None:
    task_id, workdir = sys.argv[1], sys.argv[2]
    with open(STUDY / "tasks" / "swe_lite.json") as f:
        tasks = json.load(f)
    task = next(t for t in tasks if t["id"] == task_id)

    with tempfile.NamedTemporaryFile("w", suffix=".patch", delete=False) as f:
        f.write(task["test_patch"])
        patch_path = f.name
    r = sh(["git", "-C", workdir, "apply", "--check", patch_path])
    if r.returncode != 0:
        # Maybe already applied (e.g. retry after a failed grade run).
        r2 = sh(["git", "-C", workdir, "apply", "--reverse", "--check", patch_path])
        if r2.returncode != 0:
            print("test_patch did not apply cleanly:")
            print(r.stderr[-2000:])
            print("VERDICT: GRADE-ERROR (do not count; investigate, do not re-run agent)")
            return
        print("test_patch already applied — reusing checkout state.")
    else:
        r = sh(["git", "-C", workdir, "apply", patch_path])
        if r.returncode != 0:
            print("test_patch apply failed unexpectedly:")
            print(r.stderr[-2000:])
            print("VERDICT: GRADE-ERROR (do not count; investigate, do not re-run agent)")
            return

    pytest = f"{workdir}/{GRADE_VENV}/bin/pytest"
    # Newer interpreters emit DeprecationWarnings (e.g. ast.Str on 3.12) that
    # era configs escalate via filterwarnings=error. That's environment noise,
    # not the patch — ignore it during grading.
    cmd = [pytest, "-q", "-p", "no:cacheprovider",
           "-W", "ignore::DeprecationWarning", *task["fail2pass"]]
    print("$", " ".join(cmd), f"(cwd={workdir})")
    r = sh(cmd, timeout=1200, cwd=workdir)
    print(r.stdout[-3000:])
    print(r.stderr[-1000:])
    solved = r.returncode == 0
    print(f"FAIL_TO_PASS: {len(task['fail2pass'])} tests ->",
          "SOLVED" if solved else "NOT SOLVED")


if __name__ == "__main__":
    main()
