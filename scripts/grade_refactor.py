"""Grade a refactor arm: structural check + green test subset.

Usage: python scripts/grade_refactor.py <refactor_id> runs/<id>-<arm>
Specs (helper symbol, test command) live in REFACTOR_SPECS below.
Verdict: SOLVED only if the helper exists AND the suite stays green.
"""
import os
import subprocess
import sys

REFACTOR_SPECS = {
    "refactor__requests-rebuild-method": {
        "file": "requests/sessions.py",
        "helper": "def rebuild_method",
        "tests": [
            "test_requests.py", "-q", "-p", "no:cacheprovider",
            "-W", "ignore::DeprecationWarning",
            "-k", "redirect or Redirect or REDIRECT",
        ],
    },
    "refactor__pytest-xfail-extract": {
        "file": "src/_pytest/skipping.py",
        "helper": "def evaluate_xfail_report",
        "tests": ["testing/test_skipping.py", "-q", "-p", "no:cacheprovider"],
    },
    "refactor__flask-routes-table": {
        "file": "src/flask/cli.py",
        "helper": "def format_route_table",
        "tests": [
            "tests/test_cli.py", "-q", "-p", "no:cacheprovider",
            "-W", "ignore::DeprecationWarning", "-k", "route",
        ],
    },
}


def main() -> None:
    task_id, workdir = sys.argv[1], sys.argv[2]
    spec = REFACTOR_SPECS[task_id]
    src = open(f"{workdir}/{spec['file']}").read()
    has_helper = spec["helper"] in src
    # Helper must be CALLED, not just defined (dead code is not a refactor).
    calls = src.count(spec["helper"].replace("def ", "")) >= 2
    print(f"helper defined: {has_helper}, called: {calls}")
    if not (has_helper and calls):
        print("VERDICT: NOT SOLVED (structural check failed)")
        return
    venv = ".venv312" if os.path.exists(f"{workdir}/.venv312") else ".venv"
    pytest = f"{workdir}/{venv}/bin/pytest"
    if not os.path.exists(pytest):
        print("VERDICT: GRADE-ERROR (no venv)")
        return
    cmd = [pytest, *spec["tests"]]
    print("$", " ".join(cmd), f"(cwd={workdir})")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200,
                        cwd=workdir)
    print(r.stdout[-1500:])
    print(r.stderr[-500:])
    print("VERDICT:", "SOLVED" if r.returncode == 0 else "NOT SOLVED")


if __name__ == "__main__":
    main()
