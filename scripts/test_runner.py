"""Regression harness for the corrected runner (v2.1, W04), not product tests.

Run from any directory; it creates its own temp fixtures and never
touches a real product checkout. It is not part of the unittest
discover suite, so its cases do not inflate the product test count.

Cases (all are tool tests, never C3/C4 product failures):
 1. passing suite with one skipped test -> helper 0, child 0, SKIP reported
 2. failing suite -> child 1, helper 1, artifacts preserved
 3. wrong digest / changed source -> preflight 2, no test run
 4. missing source -> preflight 2, no test run
 5. interrupted collection (suite calls os._exit mid-run) -> helper 3, not success
 6. unique run dirs -> two runs do not overwrite each other
 7. BAT static check -> BAT propagates helper exit and has no
    unconditional Done (BAT execution itself is NOT_RUN on Linux;
    on Windows it must be executed separately and reported as such)

Usage:
  python3 scripts/test_runner.py
  py -3.14 scripts/test_runner.py
Exit 0 only if every case passes.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HELPER = Path(__file__).resolve().parent / "run_windows_tests.py"
BAT = Path(__file__).resolve().parent / "run_windows_tests.bat"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def make_source(root, tests_code, extra_files=None):
    (root / "control_room").mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(parents=True, exist_ok=True)
    files = {
        "control_room/__init__.py": "x = 1\n",
        "control_room/backend.py": "# fixture backend\n",
        "tests/test_fixture.py": tests_code,
    }
    if extra_files:
        files.update(extra_files)
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    return {rel: sha(root / rel) for rel in files}


def pinned_manifest(path, digests, commit="fixture-commit-1"):
    data = {"code_commit": commit, "pin_origin": "test_runner fixture (not a product pin)",
            "source_digests": digests}
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


def run_helper(source_root, pinned, output_base, mode="api-snapshot"):
    cp = subprocess.run([sys.executable, str(HELPER),
                         "--source-root", str(source_root),
                         "--pinned-manifest", str(pinned),
                         "--output-base", str(output_base),
                         "--mode", mode],
                        capture_output=True, text=True, timeout=60)
    return cp


def read_run(output_base):
    runs = sorted(Path(output_base).iterdir())
    assert len(runs) == 1, f"expected exactly one run dir, got {runs}"
    run_dir = runs[0]
    manifest = None
    mpath = run_dir / "manifest.json"
    if mpath.exists():
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    pre = run_dir / "preflight.json"
    preflight = json.loads(pre.read_text(encoding="utf-8")) if pre.exists() else None
    return run_dir, manifest, preflight


def check(name, cond, detail=""):
    print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")
    if not cond:
        raise AssertionError(f"{name} failed: {detail}")



def parser_cases():
    """W04 LF/CRLF regression: validate_counts/count_tests must accept
    LF and CRLF equally, and must still reject mismatched, zero,
    missing and truncated summaries. These are parser unit tests on
    synthetic logs; they do not rewrite any raw log file."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("runner_under_test", HELPER)
    r = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(r)

    def run_case(name, raw_text, passed, errors, failures, skipped, expect_valid):
        # Simulate the runner's main path: normalize only a parsing copy.
        parsed = r.normalize_for_parsing(raw_text)
        p_, e_, f_, s_, _ = r.count_tests(parsed)
        valid, ran, _reason = r.validate_counts(parsed, p_, e_, f_, s_)
        check(f"parser {name}: counts", (p_, e_, f_, s_) == (passed, errors, failures, skipped),
              f"got {(p_, e_, f_, s_)} want {(passed, errors, failures, skipped)}")
        check(f"parser {name}: valid={expect_valid}", valid == expect_valid, f"got valid={valid}")

    def log(ending, summary):
        # ending is "\n" or "\r\n"; body lines are joined with it.
        body = ["test_ok (tests.T.test_ok) ... ok", "", "Ran 1 test in 0.001s", "", summary, ""]
        return ending.join(body)

    # Successful: LF and CRLF, with and without skip.
    run_case("LF OK", log("\n", "OK"), 1, 0, 0, 0, True)
    run_case("CRLF OK", log("\r\n", "OK"), 1, 0, 0, 0, True)
    run_case("LF OK skipped", "\n".join(["test_skip (tests.T.test_skip) ... skipped 'x'", "", "Ran 1 test in 0.001s", "", "OK (skipped=1)", ""]),
             0, 0, 0, 1, True)
    run_case("CRLF OK skipped", "\r\n".join(["test_skip (tests.T.test_skip) ... skipped 'x'", "", "Ran 1 test in 0.001s", "", "OK (skipped=1)", ""]),
             0, 0, 0, 1, True)
    # Failing: LF and CRLF must both be valid collections with a failure (helper exit is decided elsewhere, not by validate_counts alone).
    run_case("LF FAILED", "\n".join(["test_fail (tests.T.test_fail) ... FAIL", "", "Ran 1 test in 0.001s", "", "FAILED (failures=1)", ""]),
             0, 0, 1, 0, True)
    run_case("CRLF FAILED", "\r\n".join(["test_fail (tests.T.test_fail) ... FAIL", "", "Ran 1 test in 0.001s", "", "FAILED (failures=1)", ""]),
             0, 0, 1, 0, True)
    # Still rejected: mismatched totals, zero tests, missing summary, truncated summary.
    run_case("CRLF mismatched totals", "\r\n".join(["test_ok (tests.T.test_ok) ... ok", "", "Ran 2 tests in 0.001s", "", "OK", ""]),
             1, 0, 0, 0, False)
    run_case("CRLF zero tests", "\r\n".join(["", "Ran 0 tests in 0.001s", "", "OK", ""]),
             0, 0, 0, 0, False)
    run_case("CRLF missing summary", "\r\n".join(["test_ok (tests.T.test_ok) ... ok", "", ""]),
             1, 0, 0, 0, False)
    run_case("CRLF truncated summary", "\r\n".join(["test_ok (tests.T.test_ok) ... ok", "", "Ran 1 test in 0.001s", ""]),
             1, 0, 0, 0, False)
    # Raw bytes are not normalized by the parser helper: it returns a new string.
    raw = "OK (skipped=1)\r\n"
    check("parser: raw input untouched", raw == "OK (skipped=1)\r\n" and r.normalize_for_parsing(raw) == "OK (skipped=1)\n")


def main():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # 1. passing + skipped
        src = td / "src-pass"; src.mkdir()
        dig = make_source(src, "import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n    @unittest.skip('fixture skip')\n    def test_skip(self):\n        pass\n")
        pin = pinned_manifest(td / "pin-pass.json", dig)
        out = td / "out-pass"
        cp = run_helper(src, pin, out)
        run_dir, man, _ = read_run(out)
        check("pass: helper 0", cp.returncode == 0, f"got {cp.returncode}")
        check("pass: child 0", man["child_exit"] == 0)
        check("pass: counts 1 pass 1 skip", man["counts"]["passed"] == 1 and man["counts"]["skipped"] == 1 and man["counts"]["attempted"] == 2, str(man["counts"]))
        check("pass: log exists", (run_dir / "test-run.log").exists())
        check("pass: manifest has no self hash", "manifest_sha256" not in man)

        # 2. failing
        src = td / "src-fail"; src.mkdir()
        dig = make_source(src, "import unittest\nclass T(unittest.TestCase):\n    def test_fail(self):\n        self.fail('synthetic runner failure control')\n")
        pin = pinned_manifest(td / "pin-fail.json", dig)
        out = td / "out-fail"
        cp = run_helper(src, pin, out)
        run_dir, man, _ = read_run(out)
        check("fail: helper 1", cp.returncode == 1, f"got {cp.returncode}")
        check("fail: child 1", man["child_exit"] == 1)
        check("fail: artifacts preserved", (run_dir / "test-run.log").exists() and (run_dir / "manifest.json").exists())

        # 3. changed source (digest mismatch)
        src = td / "src-changed"; src.mkdir()
        dig = make_source(src, "import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
        pin = pinned_manifest(td / "pin-changed.json", dig)
        (src / "control_room/backend.py").write_text("# changed after pin\n", encoding="utf-8")
        out = td / "out-changed"
        cp = run_helper(src, pin, out)
        run_dir, man, pre = read_run(out)
        check("changed: preflight 2", cp.returncode == 2, f"got {cp.returncode}")
        check("changed: no test log claimed", not (run_dir / "test-run.log").exists())
        check("changed: preflight recorded", pre is not None and pre["preflight_failures"])

        # 4. missing source
        src = td / "src-missing"; src.mkdir()
        dig = make_source(src, "import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
        pin = pinned_manifest(td / "pin-missing.json", dig)
        (src / "control_room/backend.py").unlink()
        out = td / "out-missing"
        cp = run_helper(src, pin, out)
        check("missing: preflight 2", cp.returncode == 2, f"got {cp.returncode}")

        # 5. interrupted collection
        src = td / "src-interrupt"; src.mkdir()
        dig = make_source(src, "import unittest, os\nclass T(unittest.TestCase):\n    def test_die(self):\n        os._exit(137)\n")
        pin = pinned_manifest(td / "pin-interrupt.json", dig)
        out = td / "out-interrupt"
        cp = run_helper(src, pin, out)
        run_dir, man, _ = read_run(out)
        check("interrupt: helper 3 not success", cp.returncode == 3, f"got {cp.returncode}")
        check("interrupt: log preserved", (run_dir / "test-run.log").exists())

        # 6. unique run dirs
        src = td / "src-twice"; src.mkdir()
        dig = make_source(src, "import unittest\nclass T(unittest.TestCase):\n    def test_ok(self):\n        pass\n")
        pin = pinned_manifest(td / "pin-twice.json", dig)
        out = td / "out-twice"
        cp1 = run_helper(src, pin, out)
        first = sorted(out.iterdir())
        first_log = (first[0] / "test-run.log").read_bytes()
        cp2 = run_helper(src, pin, out)
        second = sorted(out.iterdir())
        check("unique: two run dirs", len(second) == 2 and cp1.returncode == 0 and cp2.returncode == 0, str(second))
        check("unique: first log untouched", (first[0] / "test-run.log").read_bytes() == first_log)

        # 7. BAT static check (execution NOT_RUN on Linux)
        bat = BAT.read_text(encoding="utf-8", errors="replace")
        check("bat: propagates helper exit", "exit /b %HELPER_EXIT%" in bat)
        check("bat: no unconditional Done before exit check", bat.index("exit /b %HELPER_EXIT%") < bat.rindex("Done."))
        print("BAT execution: NOT_RUN on this platform (static check only); Windows execution must be reported separately.")
    parser_cases()
    print("ALL RUNNER REGRESSIONS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
