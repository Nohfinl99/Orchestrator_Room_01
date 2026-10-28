"""CLI wrapper for the control-room backend, revisions 2 and 5.

Simulation notice (read first): --role is a simulation argument, not
authentication. A same-user process with direct store access can bypass
it. Privileged outputs therefore carry an explicit simulated-authority
marker, and live adapters are blocked: there is no provider, network,
background, or real-agent interface in this slice.

Persistence, revision 2:
- A mutating command loads the store, records its disk revision and
  bytes, applies backend logic, then saves only if the disk revision
  still matches, under a lock, by writing a temporary file in the same
  directory, fsyncing it, and atomically replacing the store file.
  A stale second writer is rejected and the first writer's update is
  preserved. A failed save reports truthfully: it says the previous
  store is preserved only after verifying the final bytes still match
  the bytes before the save; otherwise it reports that the store state
  differs and must not be assumed unchanged.
- Before any write, the serialized store is checked against the
  1,000,000-byte limit, so an accepted write can never make the store
  unreadable under its own size policy.
- Schema version 1 stores are rejected as superseded: their evidence
  model allowed invented PASS records. Recreate a store with init;
  do not hand-edit a v1 store into v2.

Store-file boundary for this CLI-only slice (no HTTP server, so
Host/Origin/CSRF have no target here and are NOT_RUN in the report,
not PASS): the store path must resolve inside the current working
directory, must not be a symlink or under .git, and secret-like
filenames are refused.

C5 intake slice (packet REV2.1 + F21): intake, propose, decide,
complete, and proposal-view commands. Intake input files use the
same boundary as a store (inside cwd, no symlink, no .git,
secret-like filenames refused) and are read as bytes, at most
20,001 bytes, before decode. A decide is a local operator gate
decision with provenance OPERATOR_ASSERTED; it is not owner
authentication and not owner product acceptance. Missing decide
flags are rejected by the argument parser (exit 2, no store
change); wrong-format or mismatched expected bindings are rejected
by the backend with a reason code, and a mismatch also records a
decision_attempt_rejected event (REJECTED_STALE) before failing.

C6 contextual-intake slice (requirement docs/requirements/contextual-
intake.md): ctx-assess, ctx-add-source, ctx-clarify, ctx-answer,
ctx-draft, ctx-review-rewrite, ctx-propose, ctx-status, ctx-rewrite-
view, ctx-proposal-view. Assessment is a rule-based keyword scan,
not semantic understanding; draft fields are operator-supplied and
structured by the system, not generated from raw text; a rewrite
review is OPERATOR_ASSERTED, not authentication or product
acceptance. The legacy propose/decide flow is unchanged and does
NOT enforce the contextual policy.
"""
import argparse
import contextlib
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

from . import backend

MAX_STORE_BYTES = 1_000_000
SECRET_HINTS = ("secret", ".env", "id_rsa", "credentials", "token", "private_key", ".pem")
AUTHORITY_MARKER = {
    "authority": "SIMULATED_ROLE_ARGUMENT_NOT_AUTHENTICATION",
    "live_adapters": "BLOCKED",
    "authentication": "NONE_IN_THIS_CLI",
    "note": "Role argument is simulation only; it does not authenticate a caller. Do not use this CLI for real privileged execution.",
}


def _fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 2


def resolve_store(raw):
    cwd = Path.cwd().resolve()
    path = Path(raw)
    if path.is_symlink():
        raise backend.ControlError("store path must not be a symlink")
    resolved = (cwd / path).resolve() if not path.is_absolute() else path.resolve()
    if cwd not in resolved.parents and resolved != cwd:
        raise backend.ControlError("store path must be inside the current working directory")
    if ".git" in resolved.parts:
        raise backend.ControlError("store path must not be under .git")
    lowered = resolved.name.lower()
    if any(h in lowered for h in SECRET_HINTS):
        raise backend.ControlError("store path looks like a secret file; refused")
    return resolved


def _resolve_input(raw):
    """Resolve an intake input file with the same boundary as a store:
    inside the current working directory, not a symlink, not under
    .git, secret-like filenames refused, and must be a regular file.
    The file is read as bytes by the caller, at most 20,001 bytes."""
    cwd = Path.cwd().resolve()
    path = Path(raw)
    if path.is_symlink():
        raise backend.ControlError("input path must not be a symlink")
    resolved = (cwd / path).resolve() if not path.is_absolute() else path.resolve()
    if cwd not in resolved.parents and resolved != cwd:
        raise backend.ControlError("input path must be inside the current working directory")
    if ".git" in resolved.parts:
        raise backend.ControlError("input path must not be under .git")
    lowered = resolved.name.lower()
    if any(h in lowered for h in SECRET_HINTS):
        raise backend.ControlError("input path looks like a secret file; refused")
    if not resolved.exists():
        raise backend.ControlError(f"input file does not exist: {raw}")
    if not resolved.is_file():
        raise backend.ControlError(f"input path is not a regular file: {raw}")
    return resolved


def _resolve_inside(raw, base):
    base = Path(base).resolve()
    path = Path(raw)
    if path.is_symlink():
        raise backend.ControlError("artifact path must not be a symlink")
    resolved = (base / path).resolve() if not path.is_absolute() else path.resolve()
    if base not in resolved.parents and resolved != base:
        raise backend.ControlError("artifact path must be inside the artifact directory")
    if ".git" in resolved.parts:
        raise backend.ControlError("artifact path must not be under .git")
    return resolved


@contextlib.contextmanager
def _store_lock(path):
    """Stable OS locking that releases on process death.

    The lock file is NEVER unlinked, so its identity is stable: on
    POSIX, fcntl.flock on the same inode serialises waiters and the
    OS releases the lock when the holder dies, even abruptly. On
    Windows, msvcrt.locking on the same file behaves the same way:
    the lock file may remain on disk, but it is unlocked after the
    holder dies, so the next writer can acquire it. Deleting a lock
    based only on PID/time is never done, because a live holder
    cannot be distinguished that way. If neither mechanism is
    available, writing is refused rather than using an orphan-prone
    O_EXCL lock file.
    """
    lock_path = path.with_name(path.name + ".lock")
    # POSIX path first (fcntl is unavailable on Windows).
    try:
        import fcntl
    except ImportError:
        fcntl = None
    if fcntl is not None:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
        return
    try:
        import msvcrt
    except ImportError:
        msvcrt = None
    if msvcrt is not None:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        try:
            # Lock one byte; LK_LOCK blocks until the holder releases.
            msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                try:
                    os.lseek(fd, 0, os.SEEK_SET)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                except OSError:
                    pass
        finally:
            try:
                os.close(fd)
            except OSError:
                pass
        return
    raise backend.ControlError(
        "no reliable OS locking available on this platform; refusing to write rather than risk an orphan lock")


def load_store(raw):
    path = resolve_store(raw)
    if not path.exists():
        raise backend.ControlError(f"store does not exist: {raw} (run init first)")
    if path.stat().st_size > MAX_STORE_BYTES:
        raise backend.ControlError("store file is oversized; refused")
    before_bytes = path.read_bytes()
    try:
        data = json.loads(before_bytes.decode("utf-8"))
    except Exception as exc:
        raise backend.ControlError(f"store is not valid UTF-8 JSON: {exc}")
    if not isinstance(data, dict):
        raise backend.ControlError("store is not a JSON object")
    if data.get("schema_version") != backend.SCHEMA_VERSION:
        raise backend.ControlError(
            "store schema version is superseded (v1 evidence model allowed invented PASS); "
            "recreate the store with init; do not hand-edit a v1 store into v2")
    return path, data, data["revision"], before_bytes


def save_store(path, store, expected_revision, before_bytes):
    """Atomic, compare-and-swap save. Raises on stale disk state,
    oversized serialization, or any write failure, with a truthful
    preservation report (see module docstring)."""
    serialized = (json.dumps(store, indent=2, sort_keys=True) + "\n").encode("utf-8")
    if len(serialized) > MAX_STORE_BYTES:
        raise backend.ControlError(
            f"serialized store would be {len(serialized)} bytes, over the {MAX_STORE_BYTES}-byte limit; no write performed, previous store preserved")
    with _store_lock(path):
        if path.exists():
            current_bytes = path.read_bytes()
            try:
                current = json.loads(current_bytes.decode("utf-8"))
            except Exception:
                raise backend.ControlError("disk store is not valid JSON; refusing to overwrite it")
            if current.get("revision") != expected_revision:
                raise backend.ControlError(
                    f"stale store: disk revision {current.get('revision')} != loaded revision {expected_revision}; "
                    "no overwrite performed, first writer's update is preserved")
        else:
            if expected_revision is not None:
                raise backend.ControlError("store disappeared during save; no write performed")
        tmp_fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".tmp-", dir=str(path.parent))
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(tmp_fd, "wb") as f:
                f.write(serialized)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
            try:
                dir_fd = os.open(path.parent, os.O_RDONLY)
                try:
                    os.fsync(dir_fd)
                finally:
                    os.close(dir_fd)
            except OSError:
                pass
        except Exception as exc:
            try:
                tmp_path.unlink()
            except OSError:
                pass
            # Truthful failure report: verify, do not assume.
            if path.exists():
                now_bytes = path.read_bytes()
                if now_bytes == before_bytes:
                    raise backend.ControlError(
                        f"save failed ({exc}); previous store preserved (verified: final bytes match bytes before save)")
                raise backend.ControlError(
                    f"save failed ({exc}); store state differs from before save "
                    f"(before sha256 {hashlib.sha256(before_bytes).hexdigest()}, "
                    f"current sha256 {hashlib.sha256(now_bytes).hexdigest()}); do not assume it is unchanged")
            raise backend.ControlError(f"save failed ({exc}); store file is now missing; do not assume a previous state")
        # Verify the replacement actually landed.
        if path.read_bytes() != serialized:
            raise backend.ControlError("save verification failed: final bytes differ from serialized store")


def _out(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))


def _privileged(obj):
    out = dict(obj)
    out.update(AUTHORITY_MARKER)
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="control-room",
        description="Simulation only: --role is not authentication. Live adapters are blocked.")
    sub = parser.add_subparsers(dest="action", required=True)

    def add_store(p):
        p.add_argument("--store", required=True)

    def add_role(p):
        p.add_argument("--role", required=True, choices=["owner", "agent", "judge"])
        p.add_argument("--actor", default="cli-user")

    p = sub.add_parser("init"); add_store(p)
    p = sub.add_parser("overview"); add_store(p)
    p = sub.add_parser("history"); add_store(p)
    p = sub.add_parser("verify-history"); add_store(p)
    p = sub.add_parser("verify"); add_store(p); p.add_argument("--code-revision", required=True); p.add_argument("--artifact-dir", default=".")

    p = sub.add_parser("add-observation"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--trigger"); p.add_argument("--problem")
    p.add_argument("--steps", nargs="*"); p.add_argument("--elapsed", type=float, default=None)
    p.add_argument("--stalled"); p.add_argument("--workaround"); p.add_argument("--result")
    p.add_argument("--source-locator"); p.add_argument("--source-sha256")
    p.add_argument("--direct", choices=["true", "false"], default=None)

    p = sub.add_parser("add-inference"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--observation-ids", nargs="+", required=True)
    p.add_argument("--candidate-pain"); p.add_argument("--segment"); p.add_argument("--hypothesis")
    p.add_argument("--unknowns", nargs="*"); p.add_argument("--alternatives", nargs="*")

    p = sub.add_parser("review-inference"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--status", required=True)

    p = sub.add_parser("add-brief"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--title", required=True); p.add_argument("--content", required=True)
    p.add_argument("--observation-ids", nargs="*"); p.add_argument("--inference-ids", nargs="*")

    p = sub.add_parser("approve-brief"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--reason", required=True)

    p = sub.add_parser("add-task"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--title", required=True)
    p.add_argument("--owner", required=True); p.add_argument("--depends-on", nargs="*")

    p = sub.add_parser("update-task"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--state", required=True)
    p.add_argument("--expected-revision", type=int, required=True)

    p = sub.add_parser("add-evidence"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--claim", required=True)
    p.add_argument("--artifact"); p.add_argument("--test-case"); p.add_argument("--code-revision", required=True)
    p.add_argument("--result", required=True); p.add_argument("--reviewer"); p.add_argument("--collector")
    p.add_argument("--exit-code", type=int, default=None); p.add_argument("--output-hash")
    p.add_argument("--command"); p.add_argument("--environment")
    p.add_argument("--criteria-revision"); p.add_argument("--scope-complete", action="store_true")
    p.add_argument("--artifact-path"); p.add_argument("--artifact-file"); p.add_argument("--artifact-sha256")

    p = sub.add_parser("add-review-receipt"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--evidence-ids", nargs="+", required=True)
    p.add_argument("--decision", default="REVIEWED_PASS")

    p = sub.add_parser("judge-report"); add_store(p); add_role(p)
    p.add_argument("--id", required=True); p.add_argument("--findings", nargs="*")
    p.add_argument("--per-case", nargs="*")

    p = sub.add_parser("transition"); add_store(p); add_role(p)
    p.add_argument("--to", required=True); p.add_argument("--reason", default="")
    p.add_argument("--linked-evidence"); p.add_argument("--brief-id"); p.add_argument("--judge-report-id")

    # C5 intake slice (packet REV2.1 + F21). C5 commands take no
    # --role: proposal roles are simulated template text, and a
    # decide is a local operator gate decision, not authentication.
    # --actor on intake/propose/complete is an audit label only.
    p = sub.add_parser("intake"); add_store(p)
    _ing = p.add_mutually_exclusive_group(required=True)
    _ing.add_argument("--input"); _ing.add_argument("--stdin", action="store_true")
    p.add_argument("--supersedes", default=None); p.add_argument("--actor", default="local-operator")
    p = sub.add_parser("propose"); add_store(p)
    p.add_argument("--intake-id", required=True); p.add_argument("--actor", default="local-operator")
    p = sub.add_parser("decide"); add_store(p)
    p.add_argument("--proposal-id", required=True)
    p.add_argument("--expected-proposal-digest", required=True)
    p.add_argument("--expected-brief-revision", required=True)
    p.add_argument("--expected-intake-id", required=True)
    p.add_argument("--decision", required=True); p.add_argument("--reason", required=True)
    p.add_argument("--operator", required=True); p.add_argument("--source", required=True)
    p = sub.add_parser("complete"); add_store(p)
    p.add_argument("--proposal-id", required=True); p.add_argument("--task-id", required=True)
    p.add_argument("--actor", default="local-operator")
    p = sub.add_parser("proposal-view"); add_store(p)
    p.add_argument("--proposal-id", required=True)

    # C6 contextual-intake slice. Read-only commands first; mutating
    # commands are wired in the mutating chain below.
    p = sub.add_parser("ctx-assess"); add_store(p)
    p.add_argument("--intake-id", required=True)
    p = sub.add_parser("ctx-status"); add_store(p)
    p.add_argument("--intake-id", required=True)
    p = sub.add_parser("ctx-rewrite-view"); add_store(p)
    p.add_argument("--rewrite-id", required=True)
    p = sub.add_parser("ctx-proposal-view"); add_store(p)
    p.add_argument("--proposal-id", required=True)
    p = sub.add_parser("ctx-add-source"); add_store(p)
    p.add_argument("--intake-id", required=True); p.add_argument("--source-id", required=True)
    p.add_argument("--locator", required=True)
    p.add_argument("--trust-class", required=True, choices=["owner_statement", "reference", "external_text"])
    p.add_argument("--note", default=None)
    p = sub.add_parser("ctx-clarify"); add_store(p)
    p.add_argument("--intake-id", required=True); p.add_argument("--questions", nargs="+", required=True)
    p = sub.add_parser("ctx-answer"); add_store(p)
    p.add_argument("--clarification-id", required=True); p.add_argument("--answers", nargs="+", required=True)
    p = sub.add_parser("ctx-draft"); add_store(p)
    p.add_argument("--intake-id", required=True); p.add_argument("--goal", required=True)
    p.add_argument("--context", required=True); p.add_argument("--scope", required=True)
    p.add_argument("--desired-output", required=True); p.add_argument("--next-action", required=True)
    p.add_argument("--constraints", nargs="*"); p.add_argument("--unknowns", nargs="*")
    p.add_argument("--inference", nargs="*"); p.add_argument("--clarification-id", default=None)
    p = sub.add_parser("ctx-review-rewrite"); add_store(p)
    p.add_argument("--rewrite-id", required=True)
    p.add_argument("--expected-rewrite-digest", required=True)
    p.add_argument("--decision", required=True); p.add_argument("--reason", required=True)
    p.add_argument("--operator", required=True); p.add_argument("--source", required=True)
    p = sub.add_parser("ctx-propose"); add_store(p)
    p.add_argument("--intake-id", required=True); p.add_argument("--rewrite-id", required=True)
    p.add_argument("--expected-rewrite-digest", required=True)

    args = parser.parse_args(argv)
    try:
        if args.action == "init":
            path = resolve_store(args.store)
            with _store_lock(path):
                if path.exists():
                    return _fail("store already exists; refusing to overwrite")
                store = backend.new_store()
                serialized = (json.dumps(store, indent=2, sort_keys=True) + "\n").encode("utf-8")
                tmp_fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".tmp-", dir=str(path.parent))
                try:
                    with os.fdopen(tmp_fd, "wb") as f:
                        f.write(serialized); f.flush(); os.fsync(f.fileno())
                    os.replace(tmp_name, path)
                except Exception:
                    try:
                        Path(tmp_name).unlink()
                    except OSError:
                        pass
                    raise
            _out({"ok": True, "store": str(path), "stage": store["stage"], "revision": 0})
            return 0
        path, store, base_revision, before_bytes = load_store(args.store)
        cmd = args.action
        if cmd == "overview":
            out = backend.overview(store)
            hist = backend.verify_history(store)
            out["history_valid"] = hist["chain_valid"]
            out["history_failures"] = hist["failures"][:3]
            _out(out); return 0
        if cmd == "history":
            _out({"events": store["events"]}); return 0
        if cmd == "verify-history":
            _out(backend.verify_history(store)); return 0
        if cmd == "proposal-view":
            _out(backend.proposal_view(store, args.proposal_id)); return 0
        if cmd == "ctx-assess":
            _out(backend.ctx_assess(store, args.intake_id)); return 0
        if cmd == "ctx-status":
            _out(backend.ctx_status(store, args.intake_id)); return 0
        if cmd == "ctx-rewrite-view":
            _out(backend.ctx_rewrite_view(store, args.rewrite_id)); return 0
        if cmd == "ctx-proposal-view":
            _out(backend.ctx_proposal_view(store, args.proposal_id)); return 0
        if cmd == "verify":
            artifact_dir = Path(args.artifact_dir).resolve()
            resolver = {}
            for ev in store["evidence"]:
                ap = ev.get("artifact_path")
                if not ap:
                    continue
                try:
                    apath = _resolve_inside(ap, artifact_dir)
                except backend.ControlError:
                    continue
                if apath.exists() and apath.stat().st_size <= MAX_STORE_BYTES:
                    resolver[ap] = apath.read_bytes()
            _out(backend.verify(store, args.code_revision, artifacts=resolver)); return 0
        # Mutating commands below: save with whole-store CAS, or not at all.
        # A tampered history blocks any further mutation, so a bad
        # store cannot be papered over with new events. Diagnostics
        # (overview/history/verify-history) remain available above.
        _hist = backend.verify_history(store)
        if not _hist["chain_valid"]:
            return _fail("history invalid; mutation blocked; use verify-history for diagnostics: " + "; ".join(_hist["failures"][:3]))
        if cmd == "add-observation":
            direct = None if args.direct is None else args.direct == "true"
            obj = backend.add_observation(store, args.actor, args.role, args.id,
                trigger=args.trigger, problem=args.problem, steps=args.steps,
                elapsed_time_minutes=args.elapsed, stalled=args.stalled,
                workaround=args.workaround, result=args.result,
                source_locator=args.source_locator, source_sha256=args.source_sha256,
                is_direct_observation=direct)
        elif cmd == "add-inference":
            obj = backend.add_inference(store, args.actor, args.role, args.id,
                args.observation_ids, candidate_pain=args.candidate_pain,
                segment=args.segment, hypothesis=args.hypothesis,
                unknowns=args.unknowns, alternatives=args.alternatives)
        elif cmd == "review-inference":
            obj = backend.review_inference(store, args.actor, args.role, args.id, args.status)
            obj = _privileged(obj)
        elif cmd == "add-brief":
            obj = backend.add_brief(store, args.actor, args.role, args.id, args.title,
                args.content, args.observation_ids, args.inference_ids)
        elif cmd == "approve-brief":
            obj = backend.approve_brief(store, args.actor, args.role, args.id, args.reason)
            obj = _privileged(obj)
        elif cmd == "add-task":
            obj = backend.add_task(store, args.actor, args.role, args.id, args.title,
                args.owner, depends_on=args.depends_on)
        elif cmd == "update-task":
            obj = backend.update_task(store, args.actor, args.role, args.id,
                args.state, args.expected_revision)
        elif cmd == "add-evidence":
            artifact_sha256 = args.artifact_sha256
            if args.artifact_file:
                afile = _resolve_inside(args.artifact_file, Path.cwd().resolve())
                if not afile.exists():
                    return _fail(f"artifact file does not exist: {args.artifact_file}")
                artifact_sha256 = hashlib.sha256(afile.read_bytes()).hexdigest()
            obj = backend.add_evidence(store, args.actor, args.role, args.id, args.claim,
                args.artifact, args.test_case, args.code_revision, args.result,
                args.reviewer, args.collector, exit_code=args.exit_code,
                output_hash=args.output_hash, command=args.command,
                environment=args.environment, criteria_revision=args.criteria_revision,
                scope_complete=args.scope_complete, artifact_path=args.artifact_path,
                artifact_sha256=artifact_sha256)
        elif cmd == "add-review-receipt":
            obj = backend.add_review_receipt(store, args.actor, args.role, args.id,
                args.evidence_ids, decision=args.decision)
            obj = _privileged(obj)
        elif cmd == "judge-report":
            obj = backend.judge_report(store, args.actor, args.role, args.id,
                findings=args.findings, per_case=args.per_case)
            obj = _privileged(obj)
        elif cmd == "transition":
            obj = backend.transition(store, args.actor, args.role, args.to,
                args.reason, linked_evidence=args.linked_evidence,
                brief_id=args.brief_id, judge_report_id=args.judge_report_id)
            obj = _privileged(obj)
        elif cmd == "intake":
            if args.stdin:
                if hasattr(sys.stdin, "buffer"):
                    raw = sys.stdin.buffer.read(20001)
                else:
                    raw = sys.stdin.read().encode("utf-8")
                input_source = "stdin"
                source_locator = "local-stdin"
            else:
                ipath = _resolve_input(args.input)
                raw = ipath.open("rb").read(20001)
                try:
                    rel = str(ipath.relative_to(Path.cwd().resolve()))
                except ValueError:
                    rel = ipath.name
                input_source = "file:" + rel
                source_locator = "local-file:" + rel
            obj = backend.add_intake(store, args.actor, raw, input_source,
                source_locator, supersedes=args.supersedes)
        elif cmd == "propose":
            obj = backend.propose(store, args.actor, args.intake_id)
        elif cmd == "decide":
            obj = backend.decide(store, args.operator, args.proposal_id,
                args.expected_proposal_digest, args.expected_brief_revision,
                args.expected_intake_id, args.decision, args.reason,
                args.operator, args.source)
            obj = _privileged(obj)
        elif cmd == "complete":
            obj = backend.complete_proposal_task(store, args.actor,
                args.proposal_id, args.task_id)
        elif cmd == "ctx-add-source":
            obj = backend.ctx_add_source(store, "local-operator", args.intake_id,
                args.source_id, args.locator, args.trust_class, note=args.note)
        elif cmd == "ctx-clarify":
            obj = backend.ctx_clarify(store, "local-operator", args.intake_id, args.questions)
        elif cmd == "ctx-answer":
            obj = backend.ctx_answer(store, "local-operator", args.clarification_id, args.answers)
        elif cmd == "ctx-draft":
            obj = backend.ctx_draft(store, "local-operator", args.intake_id,
                args.goal, args.context, args.scope, args.desired_output,
                args.next_action, constraints=args.constraints, unknowns=args.unknowns,
                inferences=args.inference, clarification_id=args.clarification_id)
        elif cmd == "ctx-review-rewrite":
            obj = backend.ctx_review_rewrite(store, "local-operator", args.rewrite_id,
                args.expected_rewrite_digest, args.decision, args.reason,
                args.operator, args.source)
            obj = _privileged(obj)
        elif cmd == "ctx-propose":
            obj = backend.ctx_propose(store, "local-operator", args.intake_id,
                args.rewrite_id, args.expected_rewrite_digest)
        else:
            return _fail(f"unknown command: {cmd}")
        save_store(path, store, base_revision, before_bytes)
        _out(obj)
        return 0
    except backend.DecisionRejectedError as exc:
        # The backend recorded a decision_rejected event before raising.
        # Save that history, then report the rejection as a failure.
        try:
            save_store(path, store, base_revision, before_bytes)
        except backend.ControlError as save_exc:
            return _fail(f"{exc}; rejected-decision history could not be saved: {save_exc}")
        return _fail(str(exc))
    except backend.IntakeRejectedError as exc:
        # C5: the backend recorded a correction rejection event
        # before raising. Save that history, then report the
        # rejection as a failure.
        try:
            save_store(path, store, base_revision, before_bytes)
        except backend.ControlError as save_exc:
            return _fail(f"{exc}; rejected-intake history could not be saved: {save_exc}")
        return _fail(str(exc))
    except backend.ControlError as exc:
        return _fail(str(exc))
    except SystemExit:
        raise
    except Exception as exc:
        return _fail(f"unexpected error: {exc}")


if __name__ == "__main__":
    sys.exit(main())
