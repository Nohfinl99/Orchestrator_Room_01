# C6 acceptance results (builder-run, B01-B17)

Full-scope verdict: NOT_RUN. Completed required checks: 24/24 PASS.
Total subcases: 26; PASS: 24; FAIL: 0; NOT_RUN: 2.
OS: Linux 7.0.0-39-generic; Python: 3.12.3.
Source root: /home/hatch/workspace/orchestrator-room-work/slice-c6; runner SHA-256: ea5eb7329d3f8aabe1f20bb781e47a319549a5cf7cf72670fff689ceed4a0024.

| Case | Subcase | Result | Scope |
|---|---|---|---|
| B01 | golden vague intake id and hash | PASS | Intake id recomputed from raw bytes + brief revision + template version; hash over original bytes. |
| B01 | vague assess WAITING_CLARIFICATION | PASS | Keyword-heuristic assess reports missing dimensions, method label, suggested questions; creates no event. |
| B01 | golden draft digest recomputes | PASS | Draft digest recomputed independently from stored fields equals stored digest; unknowns are operator-supplied only. |
| B01 | proposal before approval refused | PASS | ctx-propose before APPROVE review exits non-zero and creates no contextual proposal. |
| B01 | golden contextual proposal after APPROVE | PASS | After APPROVE, ctx-propose creates a contextual proposal bound to raw hash and approved rewrite digest. |
| B01 | golden reload coherence | PASS | New-process verify-history chain_valid and ctx-status shows the same proposal digest, mode contextual. |
| B02 | clear assess COMPLETE | PASS | Text containing goal/context/scope/desired_output keywords assesses COMPLETE with no missing dimensions. |
| B02 | clear draft still needs review before proposal | PASS | A clear-input draft still cannot propose before an APPROVE review of its exact digest. |
| B03 | clarify count 2-3 enforced | PASS | 1-question and 4-question clarifications are rejected; no clarification record is created. |
| B04 | answer count must match | PASS | Answer count different from question count is rejected and the clarification stays WAITING. |
| B05 | draft blocked while clarification open | PASS | Draft with an unanswered clarification exits non-zero and creates no rewrite. |
| B06 | REVISE does not enable proposal | PASS | A REVISE rewrite review does not allow ctx-propose. |
| B06 | REJECT does not enable proposal | PASS | A REJECT rewrite review does not allow ctx-propose. |
| B06 | DEFER does not enable proposal | PASS | A DEFER rewrite review does not allow ctx-propose. |
| B07 | wrong digest review REJECTED_STALE | PASS | Review with a wrong expected digest exits non-zero, creates no review, and records a rejection event. |
| B08 | source added after approval blocks proposal | PASS | A new context source after APPROVE makes ctx-propose REJECTED_STALE with no proposal. |
| B09 | newer rewrite blocks old approved proposal | PASS | After a newer draft, proposing the older approved rewrite is REJECTED_STALE. |
| B10 | different context gives different proposal | PASS | Two drafts differing only in context have different digests, and the proposal carries context B verbatim. |
| B11 | hostile text inert | PASS | APPROVE/VERIFIED/upload words in a raw intake create no decision, review, or proposal; stage stays INTAKE. |
| B12 | legacy proposal is not contextual | PASS | Legacy fixed-template propose succeeds, but ctx-status reports legacy separately and no contextual proposal exists. |
| B13 | raw unchanged and baseline null | PASS | After a full C6 flow, raw text/hash are unchanged and all six baseline fields remain null. |
| B14 | roundtrip reload coherent | PASS | After reload in a new process, history is valid, proposal digest recomputes, and store bytes are unchanged by reads. |
| B15 | tampered history blocks ctx mutation | PASS | With a tampered event, verify-history is invalid and a ctx mutation is refused. |
| B16 | packet-level no-egress | NOT_RUN | Packet-level no-egress (network capture/audit). NOT_RUN in C6; code inspection alone does not prove it. |
| B16 | owner product acceptance | NOT_RUN | Owner product acceptance for the contextual slice. NOT_RUN in C6; test approvals are synthetic. |
| B17 | source trust class and locator-only provenance | PASS | Invalid trust class is rejected; a valid source records LOCATOR_ONLY_NOT_FETCHED with null sha256. |
