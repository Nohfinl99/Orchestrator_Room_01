"""Corrected Windows/Linux test runner for the Orchestrator-Room slice, v2.

This runner is TOOLING, not product code. It lives outside the code
worktree it tests. It never claims a caller-supplied commit string
proves code identity, and it never returns 0 for a failing suite.

Contract (all failures are nonzero, artifacts are preserved):
- Identity comes from a PINNED MANIFEST (JSON), not from a
  --code-commit string. The pinned manifest must contain
  code_commit, pin_origin, and source_digests (path -> SHA-256).
- Mode "git": source-root must be a Git checkout whose HEAD equals
  code_commit and whose working tree is clean (git status empty).
  Mode "api-snapshot": there is no Git checkout claim; the pinned
  manifest is the independent identity, and the run is recorded as
  api-snapshot, never as a Git checkout.
- Preflight (exit 2): any required source missing, digest mismatch,
  HEAD mismatch, or dirty tree fails BEFORE tests run. A preflight
  report is still written into the unique run directory.
- Test run: the selected interpreter runs
  "<python> -m unittest discover -s tests -v" with cwd=source-root.
  stdout and stderr are merged in original order into the raw log
  as the child produces them (not concatenated after it exits).
- Counts are validated against unittest's authoritative totals:
  "Ran N tests" plus OK / FAILED summary. Zero discovered tests,
  a missing/unparseable summary, or a count mismatch is a
  collection failure (exit 3), never a success.
- Source hashes are recorded before AND after the run. A change
  during the run is a collection failure (exit 3).
- Exit codes: 0 = tests passed, counts valid, sources unchanged.
  1 = tests failed/errored (child nonzero, counts valid).
  2 = preflight failure. 3 = collection/source-change failure.
  The helper returns its final exit code; the BAT launcher must
  propagate it (see run_windows_tests.bat) and must not print
  "Done" on a nonzero helper exit.
- The manifest contains log_sha256, but NEVER its own hash (no
  self-hash loop). The script prints manifest_sha256 to the console
  only; a caller hashes the manifest file externally and records
  that hash in their report.
- Run directory: <output-base>/run-<UTC timestamp>-<8 hex>.
  An existing run directory is never overwritten; a collision
  generates a new id.

Usage, separate roots (see WINDOWS_RUN_GUIDE.md):
  py -3.14 -X utf8 <tooling>/scripts/run_windows_tests.py \
    --source-root <code worktree> \
    --pinned-manifest <pinned manifest JSON> \
    --output-base <directory OUTSIDE both roots> \
    --mode git
  # or, for an API snapshot (never call it a Git checkout):
  py -3.14 -X utf8 <tooling>/scripts/run_windows_tests.py \
    --source-root <snapshot dir> \
    --pinned-manifest <pinned manifest JSON> \
    --output-base <directory OUTSIDE both roots> \
    --mode api-snapshot

No network, no provider, no upload is performed by this script.
It only reads local files and runs local tests.
"""
import argparse
import hashlib
import json
import platform
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HELPER_VERSION = "2.1.0"
RAN_RE = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
OK_RE = re.compile(r"^OK(?: \(skipped=(\d+)\))?$", re.MULTILINE)
FAILED_RE = re.compile(r"^FAILED", re.MULTILINE)


def normalize_for_parsing(raw_text):
    """W04 fix: normalize CRLF/CR to LF in an IN-MEMORY parsing copy
    only. The raw log file is never rewritten, and log_sha256 is
    always computed from the original raw bytes. Regexes that anchor
    with $ (notably OK_RE) would otherwise fail on Windows CRLF
    summaries ("OK (skipped=1)\\r" does not match "OK...$"),
    turning a successful child exit 0 into helper exit 3."""
    return raw_text.replace("\r\n", "\n").replace("\r", "\n")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def interpreter_info(python):
    """Version/platform of the SELECTED interpreter, not the helper's."""
    try:
        cp = subprocess.run([python, "-c",
                             "import sys, platform; print(sys.version); print(platform.platform())"],
                            capture_output=True, text=True, timeout=30)
        lines = cp.stdout.strip().splitlines()
        return {
            "executable": str(python),
            "version": lines[0] if lines else "",
            "platform": lines[1] if len(lines) > 1 else "",
            "exit_code": cp.returncode,
        }
    except Exception as exc:  # noqa: BLE001 - record, do not crash silently
        return {"executable": str(python), "version": "", "platform": "",
                "exit_code": None, "error": str(exc)}


def git_info(source_root):
    """HEAD and dirty state, or nulls when not a Git checkout."""
    try:
        head = subprocess.run(["git", "-C", str(source_root), "rev-parse", "HEAD"],
                              capture_output=True, text=True, timeout=30)
        status = subprocess.run(["git", "-C", str(source_root), "status", "--porcelain"],
                                capture_output=True, text=True, timeout=30)
        if head.returncode != 0:
            return {"head": None, "dirty": None, "is_git": False}
        return {"head": head.stdout.strip(),
                "dirty": bool(status.stdout.strip()),
                "is_git": True}
    except Exception:  # noqa: BLE001
        return {"head": None, "dirty": None, "is_git": False}


def count_tests(log_text):
    passed = errors = failures = skipped = 0
    skipped_names = []
    for line in log_text.splitlines():
        stripped = line.rstrip()
        if stripped.endswith(" ... ok"):
            passed += 1
        elif stripped.endswith(" ... ERROR"):
            errors += 1
        elif stripped.endswith(" ... FAIL"):
            failures += 1
        elif " ... skipped" in stripped:
            skipped += 1
            skipped_names.append(stripped)
    return passed, errors, failures, skipped, skipped_names


def validate_counts(log_text, passed, errors, failures, skipped):
    """Return (valid, ran_total, reason). Authoritative totals win."""
    m = RAN_RE.search(log_text)
    if not m:
        return False, None, "no 'Ran N tests' summary in log (missing/unparseable results)"
    ran = int(m.group(1))
    if ran == 0:
        return False, ran, "zero discovered tests cannot be declared success"
    total = passed + errors + failures + skipped
    if total != ran:
        return False, ran, f"per-test counts sum {total} != authoritative total {ran}"
    if errors or failures:
        if not FAILED_RE.search(log_text):
            return False, ran, "failures/errors present but no FAILED summary"
    else:
        okm = OK_RE.search(log_text)
        if not okm:
            return False, ran, "no OK summary despite zero errors/failures"
        ok_skipped = int(okm.group(1)) if okm.group(1) else 0
        if ok_skipped != skipped:
            return False, ran, f"OK summary skipped {ok_skipped} != per-test skipped {skipped}"
    return True, ran, ""


def main():
    parser = argparse.ArgumentParser(description="Corrected test runner v2.")
    parser.add_argument("--source-root", required=True, help="Code worktree/snapshot to test (never the tooling checkout).")
    parser.add_argument("--pinned-manifest", required=True, help="JSON with code_commit, pin_origin, source_digests.")
    parser.add_argument("--output-base", required=True, help="Directory OUTSIDE source and tooling roots; a unique run-<id> dir is created inside it.")
    parser.add_argument("--mode", required=True, choices=["git", "api-snapshot"], help="git = HEAD must match; api-snapshot = no Git checkout claim.")
    parser.add_argument("--python", default=sys.executable, help="Selected test interpreter (its version is recorded, not the helper's).")
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    output_base = Path(args.output_base).resolve()
    output_base.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for _ in range(20):
        run_id = f"run-{stamp}-{secrets.token_hex(4)}"
        run_dir = output_base / run_id
        if not run_dir.exists():
            break
    else:
        print("error: could not allocate a unique run directory", file=sys.stderr)
        return 3
    run_dir.mkdir(parents=True)

    started = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    interp = interpreter_info(args.python)
    git = git_info(source_root)

    def write_preflight(failures, digests_before):
        report = {
            "run_id": run_id, "helper_version": HELPER_VERSION,
            "started_utc": started, "mode": args.mode,
            "source_root": str(source_root),
            "selected_interpreter": interp, "git": git,
            "preflight_failures": failures,
            "source_digests_before": digests_before,
            "child_exit": None, "helper_exit": 2,
        }
        (run_dir / "preflight.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"preflight failed: {'; '.join(failures)}")
        print(f"run_dir={run_dir}")
        print(f"preflight={run_dir / 'preflight.json'}")
        return 2

    # --- Load pinned manifest (identity, not a caller string) ---
    try:
        pinned = json.loads(Path(args.pinned_manifest).read_text(encoding="utf-8"))
        code_commit = pinned["code_commit"]
        pin_origin = pinned["pin_origin"]
        expected = dict(pinned["source_digests"])
    except Exception as exc:  # noqa: BLE001
        return write_preflight([f"pinned manifest unreadable/invalid: {exc}"], {})

    # --- Preflight ---
    failures = []
    digests_before = {}
    for rel in sorted(expected):
        p = source_root / rel
        if not p.is_file():
            failures.append(f"missing source: {rel}")
        else:
            actual = sha256_file(p)
            digests_before[rel] = actual
            if actual != expected[rel]:
                failures.append(f"digest mismatch: {rel} (expected {expected[rel]}, actual {actual})")
    if args.mode == "git":
        if not git["is_git"]:
            failures.append("mode git but source-root is not a Git checkout")
        elif git["head"] != code_commit:
            failures.append(f"git HEAD {git['head']} != pinned code_commit {code_commit}")
        elif git["dirty"]:
            failures.append("git working tree is dirty; clean checkout required")
    else:  # api-snapshot
        if git["is_git"] and git["head"] == code_commit:
            # Not an error by itself, but record that a Git checkout was
            # present; the run is still recorded as api-snapshot only if
            # the caller explicitly chose that mode. No checkout claim is made.
            pass
    if failures:
        return write_preflight(failures, digests_before)

    # --- Test run, ordered merged stream ---
    log_path = run_dir / "test-run.log"
    env = dict(__import__("os").environ)
    env["PYTHONUTF8"] = "1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    child_exit = None
    try:
        with open(log_path, "wb") as log_f:
            proc = subprocess.Popen(
                [args.python, "-m", "unittest", "discover", "-s", "tests", "-v"],
                cwd=source_root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            while True:
                chunk = proc.stdout.read1(65536) if proc.stdout else b""
                if not chunk:
                    break
                log_f.write(chunk)
                log_f.flush()
            child_exit = proc.wait()
    except Exception as exc:  # noqa: BLE001
        # Preserve whatever log exists; collection failure, not success.
        child_exit = None
        log_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
        # Parsing copy only; this path does not rewrite the raw log.
        log_text = normalize_for_parsing(log_text)
        manifest = _manifest(run_id, started, args, interp, git, code_commit, pin_origin,
                             digests_before, digests_before, child_exit, 3, log_path,
                             0, 0, 0, 0, [], False, None, f"collection interrupted: {exc}")
        (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"collection interrupted: {exc}")
        print(f"run_dir={run_dir}")
        return 3

    log_bytes = log_path.read_bytes()
    log_text = log_bytes.decode("utf-8", errors="replace")
    log_sha = sha256_bytes(log_bytes)
    # W04: parse only the normalized copy; raw bytes/hashes are preserved.
    parsing_text = normalize_for_parsing(log_text)
    passed, errors, failures_n, skipped, skipped_names = count_tests(parsing_text)
    counts_valid, ran, count_reason = validate_counts(parsing_text, passed, errors, failures_n, skipped)

    # --- After-run source check ---
    digests_after = {}
    source_changed = False
    for rel in sorted(expected):
        p = source_root / rel
        if not p.is_file():
            source_changed = True
            digests_after[rel] = None
        else:
            digests_after[rel] = sha256_file(p)
            if digests_after[rel] != digests_before.get(rel):
                source_changed = True

    if not counts_valid:
        final = 3
        reason = f"collection invalid: {count_reason}"
    elif source_changed:
        final = 3
        reason = "source changed during run (before/after digests differ)"
    elif child_exit is None:
        final = 3
        reason = "child exit code unknown"
    elif child_exit != 0:
        final = 1
        reason = "tests failed/errored (child exit nonzero)"
    else:
        final = 0
        reason = "tests passed, counts valid, sources unchanged"

    manifest = _manifest(run_id, started, args, interp, git, code_commit, pin_origin,
                         digests_before, digests_after, child_exit, final, log_path,
                         passed, errors, failures_n, skipped, skipped_names,
                         counts_valid, ran, reason)
    manifest["source_changed"] = source_changed
    manifest["log_sha256"] = log_sha
    # NOTE: manifest_sha256 is deliberately NOT stored inside the manifest.
    manifest_path = run_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_sha = sha256_file(manifest_path)

    print(f"child_exit={child_exit}")
    print(f"helper_exit={final}")
    print(f"attempted={ran if ran is not None else passed + errors + failures_n + skipped} passed={passed} errors={errors} failures={failures_n} skipped={skipped}")
    if skipped_names:
        for name in skipped_names:
            print(f"skipped: {name}")
    print(f"run_dir={run_dir}")
    print(f"log={log_path}")
    print(f"log_sha256={log_sha}")
    print(f"manifest={manifest_path}")
    print(f"manifest_sha256={manifest_sha}  (computed externally, not stored in manifest)")
    print(f"reason={reason}")
    return final


def _manifest(run_id, started, args, interp, git, code_commit, pin_origin,
              before, after, child_exit, final, log_path,
              passed, errors, failures, skipped, skipped_names,
              counts_valid, ran, reason):
    ended = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "run_id": run_id,
        "helper_version": HELPER_VERSION,
        "started_utc": started,
        "ended_utc": ended,
        "mode": args.mode,
        "source_root": str(args.source_root),
        "selected_interpreter": interp,
        "git": git,
        "code_commit": code_commit,
        "pin_origin": pin_origin,
        "child_command": [args.python, "-m", "unittest", "discover", "-s", "tests", "-v"],
        "child_exit": child_exit,
        "helper_exit": final,
        "counts": {"attempted": ran if ran is not None else passed + errors + failures + skipped,
                   "passed": passed, "errors": errors, "failures": failures, "skipped": skipped},
        "counts_valid": counts_valid,
        "skipped_tests": skipped_names,
        "source_digests_before": before,
        "source_digests_after": after,
        "reason": reason,
        "notes": [
            "A skipped test is NOT_RUN for that subcase, not PASS.",
            "This manifest's own hash is not stored inside it; hash it externally.",
            "This run is a test-suite run, not an independent Judge review and not a pentest.",
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
