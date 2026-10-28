"""Builder-run local checks for the C6R1 bounded fix (CTX-001).

Covers Codex review REV-CTX-001-R0 findings F01-F03 only. These
tests are the builder's regression suite for the C6R1 build; they
are NOT an independent review, NOT a pentest, and do NOT make the
system verified. A rewrite review here is a local operator gate
record with provenance OPERATOR_ASSERTED, not owner product
acceptance, and test approvals are synthetic, not a real owner's
approval of a real rewrite.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CLEAR = ("Mục tiêu: theo dõi revision rõ hơn. Ngữ cảnh: workflow relay "
         "báo cáo Muse-reviewer-Muse. Phạm vi: chỉ local CLI, không provider. "
         "Đầu ra: một brief có cấu trúc.")
PARTIAL_ONE_MISSING = ("Mục tiêu: theo dõi revision. Ngữ cảnh: workflow relay "
                       "hằng ngày. Phạm vi: chỉ local CLI, không provider.")
GOAL_AND_SCOPE_ONLY = ("Mục tiêu: theo dõi revision. "
                       "Phạm vi: chỉ local CLI, không provider.")
GOAL_ONLY = "Mục tiêu: theo dõi revision."
SUPPLEMENT_QUESTION = (
    "Ngoài những thông tin đã cung cấp, còn ràng buộc, giới hạn hoặc "
    "điểm chưa rõ nào cần ghi rõ thêm trước khi viết lại yêu cầu không?"
)


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


def load_runner_module():
    path = ROOT / "acceptance" / "run_acceptance_c6.py"
    spec = importlib.util.spec_from_file_location("run_acceptance_c6", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestContextualIntakeC6R1(unittest.TestCase):
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
        self.assertNotEqual(proc.returncode, 0, proc.stdout.decode() + proc.stderr.decode())
        return proc

    def draft(self, intake_id, clarification_id=None, **over):
        args = ["ctx-draft", "--store", "room.json", "--intake-id", intake_id,
                "--goal", over.get("goal", "Theo dõi revision rõ hơn"),
                "--context", over.get("context", "Relay báo cáo Muse-reviewer-Muse"),
                "--scope", over.get("scope", "Chỉ local CLI, không provider"),
                "--desired-output", over.get("desired_output", "Brief có cấu trúc"),
                "--next-action", over.get("next_action", "Đọc snapshot rồi quyết định")]
        if clarification_id:
            args += ["--clarification-id", clarification_id]
        return self.ctx(*args)

    def approve(self, rewrite_id, digest, expect=0):
        return self.ctx("ctx-review-rewrite", "--store", "room.json",
                        "--rewrite-id", rewrite_id,
                        "--expected-rewrite-digest", digest,
                        "--decision", "APPROVE",
                        "--reason", "Duyệt rewrite để thử luồng contextual",
                        "--operator", "test-operator", "--source", "local-cli",
                        expect=expect)

    def propose(self, intake_id, rewrite_id, digest, expect=0):
        return self.ctx("ctx-propose", "--store", "room.json",
                        "--intake-id", intake_id,
                        "--rewrite-id", rewrite_id,
                        "--expected-rewrite-digest", digest, expect=expect)

    # ---- F01: post-draft context changes block approval/proposal ----

    def test_f01a_pending_clarification_blocks_approve_and_propose(self):
        rec = self.intake(CLEAR)
        draft = self.draft(rec["intake_id"])
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", "Câu hỏi mới 1?", "Câu hỏi mới 2?")
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")
        # Approval with a pending clarification is rejected, no decision.
        self.approve(draft["rewrite_id"], draft["rewrite_digest"], expect=2)
        store = load_store(self.cwd)
        self.assertEqual(store["rewrite_reviews"], {})
        self.assertEqual(store["rewrites"][draft["rewrite_id"]]["review_status"],
                         "DRAFT_NOT_REVIEWED")
        self.assertTrue(any(e["kind"] == "ctx_rewrite_review_rejected"
                            for e in store["events"]))
        # A new proposal is rejected too.
        self.propose(rec["intake_id"], draft["rewrite_id"],
                     draft["rewrite_digest"], expect=2)
        self.assertEqual(load_store(self.cwd)["contextual_proposals"], {})

    def test_f01b_new_source_after_draft_blocks_until_fresh_draft(self):
        rec = self.intake(CLEAR)
        draft = self.draft(rec["intake_id"])
        self.assertEqual(draft["source_ids"], [])
        self.ctx("ctx-add-source", "--store", "room.json",
                 "--intake-id", rec["intake_id"], "--source-id", "SRC-NEW",
                 "--locator", "docs/new.md", "--trust-class", "reference")
        self.approve(draft["rewrite_id"], draft["rewrite_digest"], expect=2)
        self.propose(rec["intake_id"], draft["rewrite_id"],
                     draft["rewrite_digest"], expect=2)
        self.assertEqual(load_store(self.cwd)["contextual_proposals"], {})
        # A fresh draft binds the current source, so it can be approved
        # and proposed, and the proposal carries SRC-NEW (not []).
        fresh = self.draft(rec["intake_id"])
        self.assertNotEqual(fresh["rewrite_digest"], draft["rewrite_digest"])
        self.assertEqual(fresh["source_ids"], ["SRC-NEW"])
        self.approve(fresh["rewrite_id"], fresh["rewrite_digest"])
        prop = self.propose(rec["intake_id"], fresh["rewrite_id"],
                            fresh["rewrite_digest"])
        self.assertTrue(prop["new_proposal_created"])
        self.assertEqual(prop["proposal"]["source_ids"], ["SRC-NEW"])

    def test_f01c_answered_clarification_after_draft_blocks_until_fresh_draft(self):
        rec = self.intake(CLEAR)
        draft = self.draft(rec["intake_id"])
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", "Câu hỏi mới 1?", "Câu hỏi mới 2?")
        self.ctx("ctx-answer", "--store", "room.json",
                 "--clarification-id", clar["clarification_id"],
                 "--answers", "Trả lời 1", "Trả lời 2")
        self.approve(draft["rewrite_id"], draft["rewrite_digest"], expect=2)
        # Re-drafting identical fields returns the SAME stale rewrite
        # (payload unchanged), so approval is still rejected.
        same = self.draft(rec["intake_id"])
        self.assertTrue(same["already_exists"])
        self.assertEqual(same["rewrite_digest"], draft["rewrite_digest"])
        self.approve(same["rewrite_id"], same["rewrite_digest"], expect=2)
        # A fresh draft that binds the answered clarification passes.
        fresh = self.draft(rec["intake_id"], clar["clarification_id"])
        self.assertNotEqual(fresh["rewrite_digest"], draft["rewrite_digest"])
        self.approve(fresh["rewrite_id"], fresh["rewrite_digest"])
        prop = self.propose(rec["intake_id"], fresh["rewrite_id"],
                            fresh["rewrite_digest"])
        self.assertTrue(prop["new_proposal_created"])
        self.assertEqual(len(prop["proposal"]["answers_snapshot"]), 2)

    def test_f01d_non_approving_decision_on_stale_draft_enables_nothing(self):
        rec = self.intake(CLEAR)
        draft = self.draft(rec["intake_id"])
        self.ctx("ctx-clarify", "--store", "room.json",
                 "--intake-id", rec["intake_id"],
                 "--questions", "Câu hỏi mới 1?", "Câu hỏi mới 2?")
        # REVISE on a stale draft is recorded (it enables no proposal),
        # but proposing still fails, and a later APPROVE is rejected.
        review = self.ctx("ctx-review-rewrite", "--store", "room.json",
                          "--rewrite-id", draft["rewrite_id"],
                          "--expected-rewrite-digest", draft["rewrite_digest"],
                          "--decision", "REVISE", "--reason", "r",
                          "--operator", "t", "--source", "local-cli")
        self.assertEqual(review["decision"], "REVISE")
        self.propose(rec["intake_id"], draft["rewrite_id"],
                     draft["rewrite_digest"], expect=2)
        self.approve(draft["rewrite_id"], draft["rewrite_digest"], expect=2)

    def test_f01e_older_draft_approval_rejected_after_newer_draft(self):
        rec = self.intake(CLEAR)
        d1 = self.draft(rec["intake_id"], context="Context A: relay báo cáo")
        d2 = self.draft(rec["intake_id"], context="Context B: kiểm tra evidence")
        # A newer draft is a later context event for the older draft,
        # so approving the older draft is rejected as stale. The
        # latest draft still approves and proposes normally.
        self.approve(d1["rewrite_id"], d1["rewrite_digest"], expect=2)
        self.assertEqual(load_store(self.cwd)["rewrite_reviews"], {})
        self.approve(d2["rewrite_id"], d2["rewrite_digest"])
        prop = self.propose(rec["intake_id"], d2["rewrite_id"],
                            d2["rewrite_digest"])
        self.assertTrue(prop["new_proposal_created"])
        self.assertEqual(prop["proposal"]["context"],
                         "Context B: kiểm tra evidence")

    # ---- F02: suggested batches are 2-3 questions, accepted by clarify ----

    def test_f02a_four_missing_batch_accepted_by_clarify(self):
        rec = self.intake("hello", name="hello.txt")
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["dimensions_missing"],
                         ["goal", "context", "scope", "desired_output"])
        # Diagnostic still lists four missing, but the actionable batch
        # is capped at three so ctx-clarify accepts it unchanged.
        self.assertEqual(len(assess["suggested_questions"]), 3)
        self.assertEqual(assess["suggested_questions_dimensions"],
                         ["goal", "context", "scope"])
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", *assess["suggested_questions"])
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")
        self.assertEqual(clar["questions"], assess["suggested_questions"])

    def test_f02b_one_missing_batch_accepted_by_clarify(self):
        rec = self.intake(PARTIAL_ONE_MISSING)
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["dimensions_missing"], ["desired_output"])
        # One missing dimension plus the supplement question (about
        # constraints/unknowns, not a repeat of supplied information).
        self.assertEqual(len(assess["suggested_questions"]), 2)
        self.assertEqual(assess["suggested_questions_dimensions"],
                         ["desired_output"])
        self.assertEqual(assess["suggested_questions"][1], SUPPLEMENT_QUESTION)
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", *assess["suggested_questions"])
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")

    def test_f02c_two_missing_batch_accepted_by_clarify(self):
        rec = self.intake(GOAL_AND_SCOPE_ONLY)
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["dimensions_missing"],
                         ["context", "desired_output"])
        self.assertEqual(len(assess["suggested_questions"]), 2)
        self.assertEqual(assess["suggested_questions_dimensions"],
                         ["context", "desired_output"])
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", *assess["suggested_questions"])
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")

    def test_f02d_three_missing_batch_accepted_by_clarify(self):
        rec = self.intake(GOAL_ONLY)
        assess = self.ctx("ctx-assess", "--store", "room.json",
                          "--intake-id", rec["intake_id"])
        self.assertEqual(assess["dimensions_missing"],
                         ["context", "scope", "desired_output"])
        self.assertEqual(len(assess["suggested_questions"]), 3)
        clar = self.ctx("ctx-clarify", "--store", "room.json",
                        "--intake-id", rec["intake_id"],
                        "--questions", *assess["suggested_questions"])
        self.assertEqual(clar["status"], "WAITING_CLARIFICATION")

    # ---- F03: aggregator precedence FAIL > NOT_RUN > PASS ----

    def test_f03_aggregator_precedence(self):
        module = load_runner_module()
        agg = module.aggregate_full_scope
        cases = [
            ([{"result": "FAIL"}], "FAIL", 1),
            ([{"result": "FAIL"}, {"result": "NOT_RUN"}], "FAIL", 1),
            ([{"result": "FAIL"}, {"result": "PASS"}], "FAIL", 1),
            ([{"result": "PASS"}, {"result": "NOT_RUN"}], "NOT_RUN", 2),
            ([{"result": "PASS"}, {"result": "INCONCLUSIVE"}], "NOT_RUN", 2),
            ([{"result": "NOT_RUN"}, {"result": "INCONCLUSIVE"}], "NOT_RUN", 2),
            ([{"result": "PASS"}, {"result": "PASS"}], "PASS", 0),
        ]
        for results, verdict, exit_code in cases:
            with self.subTest(results=results):
                out = agg(results)
                self.assertEqual(out["full_scope_verdict"], verdict)
                self.assertEqual(out["exit_code"], exit_code)
        # Counts on the exact frozen repro inputs.
        out = agg([{"result": "FAIL"}])
        self.assertEqual(out["counts"], {"attempted": 1, "passed": 0,
                                         "failed": 1, "not_run": 0,
                                         "inconclusive": 0})
        out = agg([{"result": "FAIL"}, {"result": "NOT_RUN"}])
        self.assertEqual(out["counts"]["failed"], 1)
        self.assertEqual(out["counts"]["not_run"], 1)


if __name__ == "__main__":
    unittest.main()
