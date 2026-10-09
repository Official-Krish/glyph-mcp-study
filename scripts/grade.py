"""Grade one arm: apply the test patch, run FAIL_TO_PASS with the checkout venv.

Usage: python scripts/grade.py <instance_id> runs/<id>-<arm>

Must run AFTER the model diff is saved (grading mutates the checkout).
Prints PASS/FAIL per test and a final SOLVED / NOT SOLVED verdict.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

STUDY = Path(__file__).parent.parent
# Override grading interpreter, e.g. GRADE_VENV=.venv312 to re-grade under
# a different Python without touching the agent's runtime env.
GRADE_VENV = os.environ.get("GRADE_VENV", ".venv")


def resolve_django_doc_label(workdir, entry):
    """Map a docstring/comment-style F2P entry (no parens) to a dotted
    test label by finding the enclosing `def test_*` (+ class) in tests/."""
    needle = entry.lstrip("#").strip().rstrip(".")
    tests_dir = Path(workdir) / "tests"
    if not tests_dir.is_dir():
        return None
    for path in sorted(tests_dir.rglob("test_*.py")):
        try:
            lines = path.read_text().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if needle[:40] not in line:
                continue
            method = cls = None
            for back in lines[:i][::-1]:
                if method is None:
                    m = re.match(r"\s*def (test_\w+)\(", back)
                    if m:
                        method = m.group(1)
                if cls is None:
                    m = re.match(r"\s*class (\w+)", back)
                    if m:
                        cls = m.group(1)
                if method and cls:
                    break
            if method:
                mod = path.relative_to(workdir).with_suffix("").as_posix()
                mod = mod.replace("/", ".")
                # runtests.py labels omit the leading tests/ package.
                if mod.startswith("tests."):
                    mod = mod[len("tests."):]
                return f"{mod}.{cls}.{method}" if cls else f"{mod}.{method}"
    return None


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
    # Django repos run their own runner: tests/runtests.py <test labels>.
    runner = Path(workdir) / "tests" / "runtests.py"
    test_ids: list = list(task["fail2pass"])
    if runner.exists():
        # Django F2P ids look like "test_x (module.Class)" — reassemble
        # to the dotted label runtests.py expects: module.Class.test_x.
        fixed = []
        for tid in test_ids:
            if " (" in tid and tid.endswith(")"):
                name, loc = tid[:-1].split(" (", 1)
                # Dataset is inconsistent: some locs already end with the
                # test method (16820), others stop at the class (11019).
                fixed.append(loc if loc.endswith(f".{name}") else f"{loc}.{name}")
            elif " (" not in tid:
                # Docstring/comment-style django id: resolve to parent test.
                resolved = resolve_django_doc_label(workdir, tid)
                if resolved:
                    print(f"resolved {tid!r} -> {resolved}")
                    fixed.append(resolved)
                else:
                    print(f"UNRESOLVED test id: {tid!r} (skipped)")
            else:
                fixed.append(tid)
        test_ids = fixed
        if not test_ids:
            print("VERDICT: GRADE-ERROR (no runnable test ids)")
            return
        cmd = [
            f"{workdir}/{GRADE_VENV}/bin/python",
            str(runner),
            *test_ids,
        ]
    else:
        cmd = [pytest, "-q", "-p", "no:cacheprovider",
               "-W", "ignore::DeprecationWarning", *test_ids]
    print("$", " ".join(cmd), f"(cwd={workdir})")
    r = sh(cmd, timeout=1200, cwd=workdir)
    print(r.stdout[-3000:])
    print(r.stderr[-1000:])
    solved = r.returncode == 0
    print(f"FAIL_TO_PASS: {len(task['fail2pass'])} tests ->",
          "SOLVED" if solved else "NOT SOLVED")


if __name__ == "__main__":
    main()
