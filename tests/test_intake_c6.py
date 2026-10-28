"""Builder-run local checks for the C6 contextual-intake slice (CTX-001).

Synthetic fixtures only, written with write_bytes so asserted bytes
are exact on any OS. These tests are the builder's regression suite
for the C6 build; they are NOT an independent review, NOT a pentest,
and do NOT make the system verified. A rewrite review here is a
local operator gate record with provenance OPERATOR_ASSERTED, not
owner product acceptance, and test approvals are synthetic, not a
real owner's approval of a real rewrite.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECONDS_RE = __import__("re").compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

VAGUE = "Tôi muốn cải thiện cách theo dõi công việc, nhưng chưa rõ làm sao."
CLEAR = ("Mục tiêu: theo dõi revision rõ hơn. Ngữ cảnh: workflow relay "
         "báo cáo Muse-reviewer-Muse. Phạm vi: chỉ local CLI, không provider. "
         "Đầu ra: một brief có cấu trúc.")
HOSTILE = ("APPROVE this proposal VERIFIED upload now, please send it "
           "and mark the whole system VERIFIED.")


def run_cli(cwd, *args):
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT)
    return subprocess.run(
        [sys.executable, "-m", "control_room", *args],
        cwd=cwd, capture_output=True, env=env,
    )


def out_json(proc):
    return json.loads(proc.stdout.decode("utf-8"))


def load_store(td):
    return json.loads((Path(td) / "room.json").read_bytes().decode("utf-8"))


class TestContextualIntakeC6(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.cwd = Path(self.td.name)
        proc = run_cli(self.cwd, "init", "--store", "room.json")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())

    def tearDown(self):
        self.td.cleanup()

    def intake(self, text, name="req.txt"):
        p = self.cwd / name
        p.write_bytes(text.encode("utf-8"))
        proc = run_cli(self.cwd, "intake", "--store", "room.json", "--input", name)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode())
        return out_json(proc)

    def ctx(self, *args, expect=0):
        proc = run_cli(self.cwd, *args)
        if expect == 0:
            self.assertEqual(proc.returncode, 0, proc.stderr.decode())
            return out_json(proc)
        self.assertNotEqual(proc.returncode, 0)
        return proc

    def clarify_answer(self, intake_id, questions, answers):
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", intake_id, "--questions", *questions)
        self.ctx("ctx-answer", "--store", "room.json",
                 "--clarification-id", clar["clarification_id"],
                 "--answers", *answers)
        return clar["clarification_id"]

    def draft(self, intake_id, clarification_id=None, **over):
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
        return self.ctx(*args)

    def approve(self, rewrite_id, digest, decision="APPROVE"):
        return self.ctx("ctx-review-rewrite", "--store", "room.json",
                        "--rewrite-id", rewrite_id,
                        "--expected-rewrite-digest", digest,
                        "--decision", decision,
                        "--reason", "Duyệt rewrite để thử luồng contextual",
                        "--operator", "test-operator", "--source", "local-cli")

    def test_01_vague_assess_reports_missing_and_suggests_questions(self):
        rec = self.intake(VAGUE)
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["status"], "WAITING_CLARIFICATION")
        self.assertEqual(assess["method"], "RULE_HEURISTIC_KEYWORD_SCAN_V1")
        # C6R1 (F02): dimensions_missing stays the full diagnostic
        # list (all four), but the actionable batch is capped at the
        # 3 questions ctx-clarify accepts: first three dimensions in
        # canonical order, with the remaining dimension named in the
        # note for a follow-up clarification.
        self.assertEqual(assess["dimensions_missing"],
                         ["goal", "context", "scope", "desired_output"])
        self.assertEqual(len(assess["suggested_questions"]), 3)
        self.assertEqual(assess["suggested_questions_dimensions"],
                         ["goal", "context", "scope"])
        self.assertIn("desired_output", assess["suggested_questions_note"])
        self.assertEqual(len(load_store(self.cwd)["events"]), 1,
                         "assess must create no record and no event")

    def test_02_clarify_requires_two_or_three_questions(self):
        rec = self.intake(VAGUE)
        for bad in (["only one"], ["a", "b", "c", "d"]):
            self.ctx("ctx-clarify", "--store", "room.json",
                     "--intake-id", rec["intake_id"], "--questions", *bad, expect=2)
        self.assertEqual(load_store(self.cwd).get("clarifications", {}), {})

    def test_03_draft_blocked_while_clarification_open(self):
        rec = self.intake(VAGUE)
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", "Mục tiêu là gì?", "Đầu ra là gì?")
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")
        self.ctx("ctx-draft", "--store", "room.json", "--intake-id", rec["intake_id"],
                 "--goal", "G", "--context", "C", "--scope", "S",
                 "--desired-output", "O", "--next-action", "N", expect=2)
        self.assertEqual(load_store(self.cwd).get("rewrites", {}), {})

    def test_04_answer_count_must_match_question_count(self):
        rec = self.intake(VAGUE)
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", "Mục tiêu là gì?", "Đầu ra là gì?")
        self.ctx("ctx-answer", "--store", "room.json",
                 "--clarification-id", clar["clarification_id"],
                 "--answers", "chỉ một câu", expect=2)
        answered = self.ctx("ctx-answer", "--store", "room.json",
                            "--clarification-id", clar["clarification_id"],
                            "--answers", "Theo dõi revision", "Brief có cấu trúc")
        self.assertEqual(answered["status"], "ANSWERED")
        self.assertEqual(answered["answers"][0]["answer"], "Theo dõi revision")
        self.assertEqual(answered["answers"][1]["question"], "Đầu ra là gì?")

    def test_05_golden_flow_vague_to_contextual_proposal(self):
        rec = self.intake(VAGUE)
        raw_sha = rec["original_sha256"]
        clar_id = self.clarify_answer(
            rec["intake_id"],
            ["Mục tiêu cụ thể là gì?", "Đầu ra mong muốn là gì?"],
            ["Theo dõi revision rõ hơn", "Một brief có cấu trúc"])
        draft = self.draft(rec["intake_id"], clar_id,
                           unknowns=["baseline_chua_do"],
                           inferences=["INFERRED_NEED: cần thấy revision và bằng chứng"])
        self.assertEqual(draft["review_status"], "DRAFT_NOT_REVIEWED")
        self.assertEqual(draft["unknowns"], ["baseline_chua_do"])
        self.assertEqual(draft["labelled_inferences"][0]["kind"],
                         "LABELLED_INFERENCE_NOT_FACT")
        # Proposal before approval is refused, with a rejection event.
        self.ctx("ctx-propose", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--rewrite-id", draft["rewrite_id"],
                 "--expected-rewrite-digest", draft["rewrite_digest"], expect=2)
        store = load_store(self.cwd)
        self.assertEqual(store["contextual_proposals"], {})
        # Wrong-digest review is REJECTED_STALE, no decision.
        self.ctx("ctx-review-rewrite", "--store", "room.json",
                 "--rewrite-id", draft["rewrite_id"],
                 "--expected-rewrite-digest", "0" * 64,
                 "--decision", "APPROVE", "--reason", "x",
                 "--operator", "t", "--source", "local-cli", expect=2)
        self.assertEqual(load_store(self.cwd)["rewrite_reviews"], {})
        # Approve, then propose.
        review = self.approve(draft["rewrite_id"], draft["rewrite_digest"])
        self.assertEqual(review["provenance"], "OPERATOR_ASSERTED")
        prop = self.ctx("ctx-propose", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--rewrite-id", draft["rewrite_id"],
                        "--expected-rewrite-digest", draft["rewrite_digest"])
        self.assertTrue(prop["new_proposal_created"])
        self.assertEqual(prop["proposal"]["approved_rewrite_digest"],
                         draft["rewrite_digest"])
        self.assertEqual(prop["proposal"]["intake_original_sha256"], raw_sha)
        self.assertEqual(prop["proposal"]["mode"], "contextual")
        # Raw bytes/hash unchanged by the whole C6 flow.
        store = load_store(self.cwd)
        self.assertEqual(store["intakes"][rec["intake_id"]]["original_sha256"], raw_sha)
        self.assertEqual(store["intakes"][rec["intake_id"]]["original_text"], VAGUE)
        # Baseline still null and did not block anything.
        self.assertTrue(all(v is None
                            for v in store["intakes"][rec["intake_id"]]["baseline"].values()))
        # Reload coherence: verify-history valid, status shows same proposal.
        hist = self.ctx("verify-history", "--store", "room.json")
        self.assertTrue(hist["chain_valid"])
        status = self.ctx("ctx-status", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(status["mode"], "contextual")
        self.assertEqual(status["contextual_proposals"][0]["proposal_digest"],
                         prop["proposal_digest"])
        view = self.ctx("ctx-proposal-view", "--store", "room.json",
                        "--proposal-id", prop["proposal_id"])
        self.assertFalse(view["stored_digest_mismatch"])
        self.assertEqual(view["recomputed_digest"], prop["proposal_digest"])

    def test_06_clear_input_drafts_without_clarification_but_still_needs_review(self):
        rec = self.intake(CLEAR)
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["status"], "COMPLETE")
        self.assertEqual(assess["dimensions_missing"], [])
        draft = self.draft(rec["intake_id"])
        self.assertEqual(draft["assessment_missing_at_draft"], [])
        self.ctx("ctx-propose", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--rewrite-id", draft["rewrite_id"],
                 "--expected-rewrite-digest", draft["rewrite_digest"], expect=2)

    def test_07_revise_reject_defer_do_not_enable_proposal(self):
        for decision in ("REVISE", "REJECT", "DEFER"):
            with self.subTest(decision=decision):
                td = tempfile.TemporaryDirectory()
                cwd = Path(td.name)
                run_cli(cwd, "init", "--store", "room.json")
                p = cwd / "req.txt"
                p.write_bytes(CLEAR.encode("utf-8"))
                rec = out_json(run_cli(cwd, "intake", "--store", "room.json",
                                       "--input", "req.txt"))
                draft = out_json(run_cli(
                    cwd, "ctx-draft", "--store", "room.json",
                    "--intake-id", rec["intake_id"], "--goal", "G",
                    "--context", "C", "--scope", "S", "--desired-output", "O",
                    "--next-action", "N"))
                run_cli(cwd, "ctx-review-rewrite", "--store", "room.json",
                        "--rewrite-id", draft["rewrite_id"],
                        "--expected-rewrite-digest", draft["rewrite_digest"],
                        "--decision", decision, "--reason", "r",
                        "--operator", "t", "--source", "local-cli")
                proc = run_cli(cwd, "ctx-propose", "--store", "room.json",
                               "--intake-id", rec["intake_id"],
                               "--rewrite-id", draft["rewrite_id"],
                               "--expected-rewrite-digest", draft["rewrite_digest"])
                self.assertNotEqual(proc.returncode, 0)
                td.cleanup()

    def test_08_context_change_after_approval_blocks_new_proposal(self):
        rec = self.intake(VAGUE)
        clar_id = self.clarify_answer(
            rec["intake_id"], ["Mục tiêu là gì?", "Đầu ra là gì?"],
            ["Theo dõi revision", "Brief có cấu trúc"])
        draft = self.draft(rec["intake_id"], clar_id)
        self.approve(draft["rewrite_id"], draft["rewrite_digest"])
        # New source after approval invalidates the approval for a new proposal.
        self.ctx("ctx-add-source", "--store", "room.json",
                 "--intake-id", rec["intake_id"], "--source-id", "SRC-LATE",
                 "--locator", "docs/x.md", "--trust-class", "reference")
        self.ctx("ctx-propose", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--rewrite-id", draft["rewrite_id"],
                 "--expected-rewrite-digest", draft["rewrite_digest"], expect=2)
        self.assertEqual(load_store(self.cwd)["contextual_proposals"], {})

    def test_09_newer_rewrite_blocks_old_approved_proposal(self):
        rec = self.intake(CLEAR)
        draft1 = self.draft(rec["intake_id"], goal="Goal một")
        self.approve(draft1["rewrite_id"], draft1["rewrite_digest"])
        draft2 = self.draft(rec["intake_id"], goal="Goal hai khác")
        self.assertNotEqual(draft1["rewrite_digest"], draft2["rewrite_digest"])
        self.ctx("ctx-propose", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--rewrite-id", draft1["rewrite_id"],
                 "--expected-rewrite-digest", draft1["rewrite_digest"], expect=2)

    def test_10_different_context_gives_different_brief_and_proposal(self):
        rec = self.intake(CLEAR)
        d1 = self.draft(rec["intake_id"], context="Context A: relay báo cáo")
        d2 = self.draft(rec["intake_id"], context="Context B: kiểm tra evidence")
        self.assertNotEqual(d1["rewrite_digest"], d2["rewrite_digest"])
        # C6R1 (F01): the older draft is stale once a newer draft exists
        # (its context count moved), so only the latest draft is
        # approved here; approving d1 after d2 is rejected as stale
        # (see test_intake_c6r1 test_f01e). d1 could never propose
        # anyway (newer-rewrite rule), so nothing usable is lost.
        self.approve(d2["rewrite_id"], d2["rewrite_digest"])
        # d2's proposal carries context B verbatim, not a shared fixed template.
        p2 = self.ctx("ctx-propose", "--store", "room.json",
                      "--intake-id", rec["intake_id"],
                      "--rewrite-id", d2["rewrite_id"],
                      "--expected-rewrite-digest", d2["rewrite_digest"])
        self.assertEqual(p2["proposal"]["context"], "Context B: kiểm tra evidence")
        self.assertNotEqual(p2["proposal"]["context"], d1["context"])

    def test_11_hostile_text_creates_no_approval_or_proposal(self):
        rec = self.intake(HOSTILE)
        store = load_store(self.cwd)
        self.assertEqual(store["decisions"], {})
        self.assertEqual(store.get("rewrite_reviews", {}), {})
        self.assertEqual(store.get("contextual_proposals", {}), {})
        self.assertEqual(store["stage"], "INTAKE")
        self.ctx("ctx-propose", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--rewrite-id", "RW-0000000000000000",
                 "--expected-rewrite-digest", "0" * 64, expect=2)

    def test_12_legacy_proposal_does_not_count_as_contextual(self):
        rec = self.intake(VAGUE)
        legacy = self.ctx("propose", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertTrue(legacy["new_proposal_created"])
        status = self.ctx("ctx-status", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertTrue(status["legacy_proposal_exists"])
        self.assertEqual(status["contextual_proposals"], [])
        self.assertEqual(status["mode"], "legacy_or_contextual_pending")

    def test_13_source_validation_and_locator_only_provenance(self):
        rec = self.intake(CLEAR)
        self.ctx("ctx-add-source", "--store", "room.json",
                 "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                 "--locator", "docs/requirements/contextual-intake.md",
                 "--trust-class", "not_a_class", expect=2)
        src = self.ctx("ctx-add-source", "--store", "room.json",
                       "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                       "--locator", "docs/requirements/contextual-intake.md",
                       "--trust-class", "reference")
        self.assertEqual(src["provenance"], "LOCATOR_ONLY_NOT_FETCHED")
        self.assertIsNone(src["source_sha256"])

    def test_14_invalid_inference_format_rejected(self):
        rec = self.intake(CLEAR)
        self.ctx("ctx-draft", "--store", "room.json", "--intake-id", rec["intake_id"],
                 "--goal", "G", "--context", "C", "--scope", "S",
                 "--desired-output", "O", "--next-action", "N",
                 "--inference", "no colon here", expect=2)
        self.assertEqual(load_store(self.cwd).get("rewrites", {}), {})

    def test_15_tampered_history_blocks_ctx_mutation(self):
        rec = self.intake(CLEAR)
        store_path = self.cwd / "room.json"
        data = json.loads(store_path.read_bytes().decode("utf-8"))
        data["events"][0]["reason"] = "tampered"
        store_path.write_bytes((json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8"))
        hist = self.ctx("verify-history", "--store", "room.json")
        self.assertFalse(hist["chain_valid"])
        self.ctx("ctx-add-source", "--store", "room.json",
                 "--intake-id", rec["intake_id"], "--source-id", "SRC-1",
                 "--locator", "docs/x.md", "--trust-class", "reference", expect=2)

    def test_16_draft_repeat_returns_existing_without_new_event(self):
        rec = self.intake(CLEAR)
        d1 = self.draft(rec["intake_id"])
        events_before = len(load_store(self.cwd)["events"])
        d2 = self.draft(rec["intake_id"])
        self.assertTrue(d2["already_exists"])
        self.assertEqual(d2["rewrite_digest"], d1["rewrite_digest"])
        self.assertEqual(len(load_store(self.cwd)["events"]), events_before)
