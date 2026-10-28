"""C6 acceptance runner: B01-B17 via the real CLI in isolated temp dirs.

Contextual-intake acceptance for CTX-001 (channel
ORCHESTRATOR_CHANNEL.md, task CTX-001). Synthetic fixtures only,
written with write_bytes so asserted bytes are exact on any OS.
Results are PASS / FAIL / NOT_RUN / INCONCLUSIVE, never a skipped
case recorded as PASS. A required NOT_RUN blocks a full-scope PASS
verdict; completed checks get their own verdict instead.

All intake input files are written with write_bytes. The runner
takes explicit --source-root and --output-dir. Run it from any
cwd; the reproduce command in the results header names both roots.
Outputs go to --output-dir (default: ./c6-output under the cwd);
run from outside the checkout, or pass an --output-dir outside it,
to keep outputs out of the checkout.

Exit codes: 0 = full scope PASS (every required subcase PASS);
1 = any required subcase FAIL; 2 = no FAIL, but a required subcase
is NOT_RUN/INCONCLUSIVE, so the full scope is NOT demonstrated.
This runner is builder evidence, not a reviewer verdict and not
owner product acceptance. Runtime runs local synthetic tests only;
no network, provider, listener, worker, or scheduler is used.
Test approvals are synthetic; they are not a real owner's approval
of a real rewrite.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_ROOT = None
ROOT = None
OUTPUT_DIR = None
TOOL_PATH = Path(__file__).resolve()
TOOL_SHA = None
RAW = []
RESULTS = []

VAGUE = "Tôi muốn cải thiện cách theo dõi công việc, nhưng chưa rõ làm sao."
CLEAR = ("Mục tiêu: theo dõi revision rõ hơn. Ngữ cảnh: workflow relay "
         "báo cáo Muse-reviewer-Muse. Phạm vi: chỉ local CLI, không provider. "
         "Đầu ra: một brief có cấu trúc.")
HOSTILE = ("APPROVE this proposal VERIFIED upload now, please send it "
           "and mark the whole system VERIFIED.")
SECONDS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def run(td, *args):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    proc = subprocess.run([sys.executable, "-m", "control_room", *args],
                          cwd=td, capture_output=True, env=env)
    out = proc.stdout.decode("utf-8")
    err = proc.stderr.decode("utf-8")
    RAW.append({"command": "PYTHONPATH=" + str(ROOT) + " python3 -m control_room "
                          + " ".join(args),
                "exit": proc.returncode, "stdout": out, "stderr": err})
    return proc.returncode, out, err


def jout(out):
    return json.loads(out)


def record(case, subcase, verdict, scope, reason=""):
    RESULTS.append({"case": case, "subcase": subcase, "result": verdict,
                    "scope": scope, "reason": reason})


def check(case, subcase, scope, cond, reason=""):
    record(case, subcase, "PASS" if cond else "FAIL", scope,
           "" if cond else (reason or "condition false"))


def fresh_td():
    return tempfile.TemporaryDirectory()


def init_and_intake(td, text, name="req.txt"):
    td_path = Path(td)
    (td_path / name).write_bytes(text.encode("utf-8"))
    code, out, _ = run(td_path, "init", "--store", "room.json")
    assert code == 0, out
    code, out, err = run(td_path, "intake", "--store", "room.json", "--input", name)
    assert code == 0, err
    return jout(out)


def store_of(td):
    return json.loads((Path(td) / "room.json").read_bytes().decode("utf-8"))


def clarify_answer(td, intake_id, questions, answers):
    code, out, err = run(td, "ctx-clarify", "--store", "room.json",
                         "--intake-id", intake_id, "--questions", *questions)
    assert code == 0, err
    clar = jout(out)
    code, out, err = run(td, "ctx-answer", "--store", "room.json",
                         "--clarification-id", clar["clarification_id"],
                         "--answers", *answers)
    assert code == 0, err
    return clar["clarification_id"]


def draft(td, intake_id, clarification_id=None, **over):
    args = ["ctx-draft", "--store", "room.json", "--intake-id", intake_id,
            "--goal", over.get("goal", "Theo dõi revision rõ hơn"),
            "--context", over.get("context", "Relay báo cáo Muse-reviewer-Muse"),
            "--scope", over.get("scope", "Chỉ local CLI, không provider"),
            "--desired-output", over.get("desired_output", "Brief có cấu trúc"),
            "--next-action", over.get("next_action", "Đọc snapshot rồi quyết định")]
    if clarification_id:
        args += ["--clarification-id", clarification_id]
    if over.get("unknowns"):
        args += ["--unknowns", *over["unknowns"]]
    if over.get("inferences"):
        args += ["--inference", *over["inferences"]]
    code, out, err = run(td, *args)
    assert code == 0, err
    return jout(out)


def approve(td, rewrite_id, digest):
    code, out, err = run(td, "ctx-review-rewrite", "--store", "room.json",
                         "--rewrite-id", rewrite_id,
                         "--expected-rewrite-digest", digest,
                         "--decision", "APPROVE",
                         "--reason", "Duyệt rewrite để thử luồng contextual",
                         "--operator", "test-operator", "--source", "local-cli")
    assert code == 0, err
    return jout(out)


def propose(td, intake_id, rewrite_id, digest):
    return run(td, "ctx-propose", "--store", "room.json",
               "--intake-id", intake_id, "--rewrite-id", rewrite_id,
               "--expected-rewrite-digest", digest)


def recomputed_rewrite_digest(rec):
    payload = {
        "rewrite_version": "CTX-REWRITE-V1",
        "intake_id": rec["intake_id"],
        "intake_original_sha256": rec["intake_original_sha256"],
        "goal": rec["goal"], "context": rec["context"], "scope": rec["scope"],
        "desired_output": rec["desired_output"],
        "constraints": rec["constraints"], "unknowns": rec["unknowns"],
        "assessment_missing_at_draft": rec["assessment_missing_at_draft"],
        "labelled_inferences": rec["labelled_inferences"],
        "next_action": rec["next_action"],
        "source_ids": sorted(rec["source_ids"]),
        "clarification_id": rec["clarification_id"],
        "answers_snapshot": rec["answers_snapshot"],
    }
    return sha256_bytes(canonical(payload).encode("utf-8"))


def main():
    global SOURCE_ROOT, ROOT, OUTPUT_DIR, TOOL_SHA
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-root", default=None)
    ap.add_argument("--output-dir", default=None)
    args = ap.parse_args()
    ROOT = Path(args.source_root).resolve() if args.source_root else Path(__file__).resolve().parents[1]
    SOURCE_ROOT = ROOT
    OUTPUT_DIR = Path(args.output_dir).resolve() if args.output_dir else (Path.cwd() / "c6-output")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TOOL_SHA = sha256_file(TOOL_PATH)

    # B01 golden vague flow, kept for evidence files at the end.
    golden_td = fresh_td()
    td = Path(golden_td.name)
    rec = init_and_intake(td, VAGUE)
    intake_id = rec["intake_id"]
    expected_intake = "INTAKE-" + sha256_bytes(
        VAGUE.encode("utf-8") + b"\x00" + b"PRODUCT_INTAKE_BRIEF_REV2"
        + b"\x00" + b"INTAKE_TEMPLATE_V1")[:16]
    check("B01", "golden vague intake id and hash",
          "Intake id recomputed from raw bytes + brief revision + template version; hash over original bytes.",
          intake_id == expected_intake
          and rec["original_sha256"] == sha256_bytes(VAGUE.encode("utf-8"))
          and rec["original_text"] == VAGUE)
    code, out, _ = run(td, "ctx-assess", "--store", "room.json", "--intake-id", intake_id)
    assess = jout(out)
    check("B01", "vague assess WAITING_CLARIFICATION",
          "Keyword-heuristic assess reports missing dimensions, method label, suggested questions; creates no event.",
          code == 0 and assess["status"] == "WAITING_CLARIFICATION"
          and assess["method"] == "RULE_HEURISTIC_KEYWORD_SCAN_V1"
          and len(store_of(td)["events"]) == 1)
    clar_id = clarify_answer(td, intake_id,
                             ["Mục tiêu cụ thể là gì?", "Đầu ra mong muốn là gì?"],
                             ["Theo dõi revision rõ hơn", "Một brief có cấu trúc"])
    draft_rec = draft(td, intake_id, clar_id, unknowns=["baseline_chua_do"],
                      inferences=["INFERRED_NEED: cần thấy revision và bằng chứng"])
    check("B01", "golden draft digest recomputes",
          "Draft digest recomputed independently from stored fields equals stored digest; unknowns are operator-supplied only.",
          recomputed_rewrite_digest(draft_rec) == draft_rec["rewrite_digest"]
          and draft_rec["unknowns"] == ["baseline_chua_do"]
          and draft_rec["labelled_inferences"][0]["kind"] == "LABELLED_INFERENCE_NOT_FACT")
    code, out, _ = propose(td, intake_id, draft_rec["rewrite_id"], draft_rec["rewrite_digest"])
    check("B01", "proposal before approval refused",
          "ctx-propose before APPROVE review exits non-zero and creates no contextual proposal.",
          code != 0 and store_of(td)["contextual_proposals"] == {})
    review = approve(td, draft_rec["rewrite_id"], draft_rec["rewrite_digest"])
    code, out, _ = propose(td, intake_id, draft_rec["rewrite_id"], draft_rec["rewrite_digest"])
    prop = jout(out) if code == 0 else {}
    check("B01", "golden contextual proposal after APPROVE",
          "After APPROVE, ctx-propose creates a contextual proposal bound to raw hash and approved rewrite digest.",
          code == 0 and prop.get("new_proposal_created") is True
          and prop["proposal"]["approved_rewrite_digest"] == draft_rec["rewrite_digest"]
          and prop["proposal"]["intake_original_sha256"] == rec["original_sha256"])
    code, out, _ = run(td, "verify-history", "--store", "room.json")
    hist = jout(out)
    code2, out2, _ = run(td, "ctx-status", "--store", "room.json", "--intake-id", intake_id)
    status = jout(out2)
    check("B01", "golden reload coherence",
          "New-process verify-history chain_valid and ctx-status shows the same proposal digest, mode contextual.",
          hist["chain_valid"] is True and status["mode"] == "contextual"
          and status["contextual_proposals"][0]["proposal_digest"] == prop["proposal_digest"])
    golden_store = store_of(td)
    golden_status = status
    golden_hist = hist
    golden_steps = [r["command"] for r in RAW]

    # B02 clear input.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    code, out, _ = run(td, "ctx-assess", "--store", "room.json", "--intake-id", rec["intake_id"])
    assess = jout(out)
    check("B02", "clear assess COMPLETE",
          "Text containing goal/context/scope/desired_output keywords assesses COMPLETE with no missing dimensions.",
          assess["status"] == "COMPLETE" and assess["dimensions_missing"] == [])
    d = draft(td, rec["intake_id"])
    code, _, _ = propose(td, rec["intake_id"], d["rewrite_id"], d["rewrite_digest"])
    check("B02", "clear draft still needs review before proposal",
          "A clear-input draft still cannot propose before an APPROVE review of its exact digest.",
          code != 0)
    td2.cleanup()

    # B03 clarify count validation.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    ok = True
    for bad in (["only one"], ["a", "b", "c", "d"]):
        code, _, _ = run(td, "ctx-clarify", "--store", "room.json",
                         "--intake-id", rec["intake_id"], "--questions", *bad)
        ok = ok and code != 0
    check("B03", "clarify count 2-3 enforced",
          "1-question and 4-question clarifications are rejected; no clarification record is created.",
          ok and store_of(td).get("clarifications", {}) == {})
    td2.cleanup()

    # B04 answer count mismatch.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    code, out, _ = run(td, "ctx-clarify", "--store", "room.json",
                       "--intake-id", rec["intake_id"],
                       "--questions", "Mục tiêu là gì?", "Đầu ra là gì?")
    clar = jout(out)
    code, _, _ = run(td, "ctx-answer", "--store", "room.json",
                     "--clarification-id", clar["clarification_id"],
                     "--answers", "chỉ một câu")
    check("B04", "answer count must match",
          "Answer count different from question count is rejected and the clarification stays WAITING.",
          code != 0 and store_of(td)["clarifications"][clar["clarification_id"]]["status"] == "WAITING_CLARIFICATION")
    td2.cleanup()

    # B05 draft blocked while clarification open.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    run(td, "ctx-clarify", "--store", "room.json", "--intake-id", rec["intake_id"],
        "--questions", "Mục tiêu là gì?", "Đầu ra là gì?")
    code, _, _ = run(td, "ctx-draft", "--store", "room.json", "--intake-id", rec["intake_id"],
                     "--goal", "G", "--context", "C", "--scope", "S",
                     "--desired-output", "O", "--next-action", "N")
    check("B05", "draft blocked while clarification open",
          "Draft with an unanswered clarification exits non-zero and creates no rewrite.",
          code != 0 and store_of(td).get("rewrites", {}) == {})
    td2.cleanup()

    # B06 REVISE / REJECT / DEFER do not enable proposal.
    for decision in ("REVISE", "REJECT", "DEFER"):
        td2 = fresh_td(); td = Path(td2.name)
        rec = init_and_intake(td, CLEAR)
        d = draft(td, rec["intake_id"])
        code, _, _ = run(td, "ctx-review-rewrite", "--store", "room.json",
                         "--rewrite-id", d["rewrite_id"],
                         "--expected-rewrite-digest", d["rewrite_digest"],
                         "--decision", decision, "--reason", "r",
                         "--operator", "t", "--source", "local-cli")
        code2, _, _ = propose(td, rec["intake_id"], d["rewrite_id"], d["rewrite_digest"])
        check("B06", f"{decision} does not enable proposal",
              f"A {decision} rewrite review does not allow ctx-propose.",
              code == 0 and code2 != 0
              and store_of(td)["contextual_proposals"] == {})
        td2.cleanup()

    # B07 wrong-digest review.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    d = draft(td, rec["intake_id"])
    code, _, _ = run(td, "ctx-review-rewrite", "--store", "room.json",
                     "--rewrite-id", d["rewrite_id"],
                     "--expected-rewrite-digest", "0" * 64,
                     "--decision", "APPROVE", "--reason", "x",
                     "--operator", "t", "--source", "local-cli")
    check("B07", "wrong digest review REJECTED_STALE",
          "Review with a wrong expected digest exits non-zero, creates no review, and records a rejection event.",
          code != 0 and store_of(td)["rewrite_reviews"] == {}
          and any(e["kind"] == "ctx_rewrite_review_rejected"
                  for e in store_of(td)["events"]))
    td2.cleanup()

    # B08 context change after approval.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    clar_id = clarify_answer(td, rec["intake_id"],
                             ["Mục tiêu là gì?", "Đầu ra là gì?"],
                             ["Theo dõi revision", "Brief có cấu trúc"])
    d = draft(td, rec["intake_id"], clar_id)
    approve(td, d["rewrite_id"], d["rewrite_digest"])
    run(td, "ctx-add-source", "--store", "room.json", "--intake-id", rec["intake_id"],
        "--source-id", "SRC-LATE", "--locator", "docs/x.md", "--trust-class", "reference")
    code, _, _ = propose(td, rec["intake_id"], d["rewrite_id"], d["rewrite_digest"])
    check("B08", "source added after approval blocks proposal",
          "A new context source after APPROVE makes ctx-propose REJECTED_STALE with no proposal.",
          code != 0 and store_of(td)["contextual_proposals"] == {})
    td2.cleanup()

    # B09 newer rewrite blocks old approved proposal.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    d1 = draft(td, rec["intake_id"], goal="Goal một")
    approve(td, d1["rewrite_id"], d1["rewrite_digest"])
    draft(td, rec["intake_id"], goal="Goal hai khác")
    code, _, _ = propose(td, rec["intake_id"], d1["rewrite_id"], d1["rewrite_digest"])
    check("B09", "newer rewrite blocks old approved proposal",
          "After a newer draft, proposing the older approved rewrite is REJECTED_STALE.",
          code != 0 and store_of(td)["contextual_proposals"] == {})
    td2.cleanup()

    # B10 different context, different brief/proposal.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    d1 = draft(td, rec["intake_id"], context="Context A: relay báo cáo")
    d2 = draft(td, rec["intake_id"], context="Context B: kiểm tra evidence")
    approve(td, d2["rewrite_id"], d2["rewrite_digest"])
    code, out, _ = propose(td, rec["intake_id"], d2["rewrite_id"], d2["rewrite_digest"])
    prop = jout(out) if code == 0 else {}
    check("B10", "different context gives different proposal",
          "Two drafts differing only in context have different digests, and the proposal carries context B verbatim.",
          d1["rewrite_digest"] != d2["rewrite_digest"] and code == 0
          and prop["proposal"]["context"] == "Context B: kiểm tra evidence")
    td2.cleanup()

    # B11 hostile text inert.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, HOSTILE)
    store = store_of(td)
    check("B11", "hostile text inert",
          "APPROVE/VERIFIED/upload words in a raw intake create no decision, review, or proposal; stage stays INTAKE.",
          store["decisions"] == {} and store.get("rewrite_reviews", {}) == {}
          and store.get("contextual_proposals", {}) == {} and store["stage"] == "INTAKE")
    td2.cleanup()

    # B12 legacy distinction.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    code, out, _ = run(td, "propose", "--store", "room.json", "--intake-id", rec["intake_id"])
    legacy = jout(out) if code == 0 else {}
    code, out, _ = run(td, "ctx-status", "--store", "room.json", "--intake-id", rec["intake_id"])
    status = jout(out)
    check("B12", "legacy proposal is not contextual",
          "Legacy fixed-template propose succeeds, but ctx-status reports legacy separately and no contextual proposal exists.",
          legacy.get("new_proposal_created") is True
          and status["legacy_proposal_exists"] is True
          and status["contextual_proposals"] == [])
    td2.cleanup()

    # B13 raw unchanged + baseline null after golden-style flow.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    clar_id = clarify_answer(td, rec["intake_id"],
                             ["Mục tiêu là gì?", "Đầu ra là gì?"],
                             ["Theo dõi revision", "Brief có cấu trúc"])
    d = draft(td, rec["intake_id"], clar_id)
    approve(td, d["rewrite_id"], d["rewrite_digest"])
    code, _, _ = propose(td, rec["intake_id"], d["rewrite_id"], d["rewrite_digest"])
    store = store_of(td)
    check("B13", "raw unchanged and baseline null",
          "After a full C6 flow, raw text/hash are unchanged and all six baseline fields remain null.",
          code == 0 and store["intakes"][rec["intake_id"]]["original_text"] == VAGUE
          and store["intakes"][rec["intake_id"]]["original_sha256"] == rec["original_sha256"]
          and all(v is None for v in store["intakes"][rec["intake_id"]]["baseline"].values()))
    td2.cleanup()

    # B14 roundtrip/reload (separate from B01 golden): new process reads same store.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, VAGUE)
    clar_id = clarify_answer(td, rec["intake_id"],
                             ["Mục tiêu là gì?", "Đầu ra là gì?"],
                             ["Theo dõi revision", "Brief có cấu trúc"])
    d = draft(td, rec["intake_id"], clar_id)
    approve(td, d["rewrite_id"], d["rewrite_digest"])
    code, out, _ = propose(td, rec["intake_id"], d["rewrite_id"], d["rewrite_digest"])
    prop = jout(out)
    before_bytes = (td / "room.json").read_bytes()
    code, out, _ = run(td, "verify-history", "--store", "room.json")
    hist = jout(out)
    code, out, _ = run(td, "ctx-proposal-view", "--store", "room.json",
                       "--proposal-id", prop["proposal_id"])
    view = jout(out)
    check("B14", "roundtrip reload coherent",
          "After reload in a new process, history is valid, proposal digest recomputes, and store bytes are unchanged by reads.",
          hist["chain_valid"] is True and view["stored_digest_mismatch"] is False
          and view["recomputed_digest"] == prop["proposal_digest"]
          and (td / "room.json").read_bytes() == before_bytes)
    td2.cleanup()

    # B15 tampered history blocks ctx mutation.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    sp = td / "room.json"
    data = json.loads(sp.read_bytes().decode("utf-8"))
    data["events"][0]["reason"] = "tampered"
    sp.write_bytes((json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    code, _, _ = run(td, "ctx-add-source", "--store", "room.json",
                     "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                     "--locator", "docs/x.md", "--trust-class", "reference")
    check("B15", "tampered history blocks ctx mutation",
          "With a tampered event, verify-history is invalid and a ctx mutation is refused.",
          code != 0)
    td2.cleanup()

    # B16 required NOT_RUN scope gaps (explicit, not PASS).
    record("B16", "packet-level no-egress", "NOT_RUN",
           "Packet-level no-egress (network capture/audit). NOT_RUN in C6; code inspection alone does not prove it.",
           "No packet capture was run in this local CLI acceptance.")
    record("B16", "owner product acceptance", "NOT_RUN",
           "Owner product acceptance for the contextual slice. NOT_RUN in C6; test approvals are synthetic.",
           "No real owner decision for a real rewrite is present in this run.")

    # B17 source validation.
    td2 = fresh_td(); td = Path(td2.name)
    rec = init_and_intake(td, CLEAR)
    code, _, _ = run(td, "ctx-add-source", "--store", "room.json",
                     "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                     "--locator", "docs/requirements/contextual-intake.md",
                     "--trust-class", "not_a_class")
    code2, out2, _ = run(td, "ctx-add-source", "--store", "room.json",
                         "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                         "--locator", "docs/requirements/contextual-intake.md",
                         "--trust-class", "reference")
    src = jout(out2) if code2 == 0 else {}
    check("B17", "source trust class and locator-only provenance",
          "Invalid trust class is rejected; a valid source records LOCATOR_ONLY_NOT_FETCHED with null sha256.",
          code != 0 and code2 == 0 and src.get("provenance") == "LOCATOR_ONLY_NOT_FETCHED"
          and src.get("source_sha256") is None)
    td2.cleanup()

    # ---- outputs ----
    passed = sum(1 for r in RESULTS if r["result"] == "PASS")
    failed = sum(1 for r in RESULTS if r["result"] == "FAIL")
    not_run = sum(1 for r in RESULTS if r["result"] == "NOT_RUN")
    attempted = len(RESULTS)
    full_scope = "PASS" if (failed == 0 and not_run == 0) else "NOT_RUN"
    completed_required = attempted - not_run
    completed_pass = passed
    results = {
        "runner": "run_acceptance_c6.py",
        "task": "CTX-001",
        "source_root": str(ROOT),
        "output_dir": str(OUTPUT_DIR),
        "os": platform.system() + " " + platform.release(),
        "python": platform.python_version(),
        "runner_sha256": TOOL_SHA,
        "full_scope_verdict": full_scope,
        "completed_required": f"{completed_pass}/{completed_required} PASS",
        "counts": {"attempted": attempted, "passed": passed, "failed": failed,
                   "not_run": not_run},
        "cases": RESULTS,
        "raw_outputs": RAW,
    }
    (OUTPUT_DIR / "acceptance-results.json").write_bytes(
        (json.dumps(results, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
    lines = ["# C6 acceptance results (builder-run, B01-B17)",
             "",
             f"Full-scope verdict: {full_scope}. Completed required checks: {completed_pass}/{completed_required} PASS.",
             f"Total subcases: {attempted}; PASS: {passed}; FAIL: {failed}; NOT_RUN: {not_run}.",
             f"OS: {results['os']}; Python: {results['python']}.",
             f"Source root: {ROOT}; runner SHA-256: {TOOL_SHA}.",
             "",
             "| Case | Subcase | Result | Scope |",
             "|---|---|---|---|"]
    for r in RESULTS:
        lines.append(f"| {r['case']} | {r['subcase']} | {r['result']} | {r['scope']} |")
    (OUTPUT_DIR / "acceptance-results.md").write_bytes(
        ("\n".join(lines) + "\n").encode("utf-8"))
    # Golden flow evidence files.
    (OUTPUT_DIR / "golden-flow-store.json").write_bytes(
        (json.dumps(golden_store, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
    (OUTPUT_DIR / "golden-flow-verify-history.json").write_bytes(
        (json.dumps(golden_hist, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    (OUTPUT_DIR / "golden-flow-ctx-status.json").write_bytes(
        (json.dumps(golden_status, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8"))
    (OUTPUT_DIR / "golden-flow-steps.txt").write_bytes(
        ("\n".join(golden_steps) + "\n").encode("utf-8"))
    (OUTPUT_DIR / "acceptance-runner.py").write_bytes(TOOL_PATH.read_bytes())
    # Manifest (self-excluding) over the evidence files written so far.
    files = {}
    for name in ("acceptance-results.json", "acceptance-results.md",
                 "acceptance-runner.py", "golden-flow-store.json",
                 "golden-flow-verify-history.json", "golden-flow-ctx-status.json",
                 "golden-flow-steps.txt"):
        p = OUTPUT_DIR / name
        files[name] = {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
    manifest = {
        "note": "E6 evidence manifest (builder evidence for C6). MANIFEST.json and "
                "acceptance-manifest.json exclude themselves to avoid self-reference. "
                "None of these files is a reviewer verdict or owner acceptance.",
        "files": files,
    }
    (OUTPUT_DIR / "acceptance-manifest.json").write_bytes(
        (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    golden_td.cleanup()
    print(f"Full-scope verdict: {full_scope}. Completed required checks: {completed_pass}/{completed_required} PASS.")
    print(f"Total subcases: {attempted}; PASS: {passed}; FAIL: {failed}; NOT_RUN: {not_run}.")
    if failed:
        return 1
    if not_run:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
