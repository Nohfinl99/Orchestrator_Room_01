# C6R1 — bounded fix for Codex review REV-CTX-001-R0 (CTX-001)

Scope basis: Codex review REV-CTX-001-R0 in reply to submission
SUB-CTX-001-R0 (code C6, evidence E6), verdict CHANGES_REQUESTED
with findings F01–F03, next action: bounded C6R1 plus separate
E6R1 evidence, C6/E6/legacy snapshots preserved. This note
describes only the C6R1 delta. `C6_NOTE.md` is unchanged and
still describes the C6 flow; where this note tightens a C6 rule,
this note governs for C6R1. No merge, no PR, no main change, no
Orchestrator_Reverse change, no provider/worker/chat-listener,
no credentials. Whole system stays NOT_VERIFIED; owner product
acceptance stays PENDING.

## F01 — draft-bound context: pending clarification and post-draft changes block approval/proposal

Bug (C6): a review recorded only the context-event count at
review time, and a proposal compared the count at review time
with the count at propose time. Context events between draft and
review were therefore invisible: a clarification created after a
draft and left WAITING_CLARIFICATION did not stop an APPROVE or
a new proposal, and a source added after a draft but before
APPROVE did not stop them either (the proposal then carried the
draft's old `source_ids`, e.g. `[]`, while current sources were
`[SRC-NEW]`).

Fix (minimal, inside the existing optimistic CAS path):

- Each new draft records `ctx_event_count_at_draft`: the count of
  context-change events (`ctx_source_added`,
  `ctx_clarification_created`, `ctx_clarification_answered`,
  `ctx_rewrite_drafted`) for the intake, including the draft
  event itself. The rewrite payload and digest are unchanged:
  the field is record metadata added after digest computation,
  so stored digests still recompute exactly.
- `ctx-review-rewrite` with decision APPROVE now rejects (event
  `ctx_rewrite_review_rejected`, exit 2, no decision) when: an
  unanswered clarification exists for the intake, or the current
  context-change count differs from the draft's bound count, or
  the current source ids differ from the draft's bound source
  ids. A fresh draft (binding the new context, e.g. the new
  source or the answered clarification) plus a fresh review is
  required. Non-approving decisions (REVISE/REJECT/DEFER) are not
  blocked by these checks because they enable no proposal; a
  later APPROVE of the same stale draft is still rejected.
- `ctx-propose` gains the same three checks as defense in depth
  for approvals recorded before this fix (a legacy C6 approval
  whose draft went stale before propose). The existing checks
  (latest-rewrite, count-vs-review-count) are unchanged, and the
  existing repeat rule is unchanged: a repeat of an already
  created proposal returns the frozen proposal; these checks
  govern only the creation of a NEW proposal. Likewise, a repeat
  review (same digest, decision, and reason) returns the existing
  review record; it creates no new approval, and propose still
  blocks a new proposal when context moved.
- Older C6 records lack `ctx_event_count_at_draft`. For them the
  bound count is reconstructed from the event history (change
  events for the intake up to and including the rewrite's draft
  event); if no draft event is found, the source-ids comparison
  is the fallback. Verified manually: an old-C6 store's draft
  rejects a post-source APPROVE under new code (exit 2), while a
  clean old-C6 draft still approves and proposes under new code.

Consequence, stated plainly: approving an older draft after a
newer draft exists is now rejected as stale (the newer draft is
a later context event for the older one). The older draft could
never propose anyway under the C6 newer-rewrite rule, so no
usable flow is lost; the operator approves the latest draft.
C6 test_10 was updated accordingly (it now approves only the
latest draft); its assertion — the proposal carries the newest
context verbatim — is unchanged.

## F02 — suggested questions are an actionable 2–3-question batch

Bug (C6): `ctx-assess` suggested one question per missing
dimension, so a 4-missing intake suggested 4 questions and a
1-missing intake suggested 1 question, and `ctx-clarify`
(exactly 2–3 questions) rejected both batches with exit 2.

Fix: `dimensions_missing` stays the full diagnostic list, but
`suggested_questions` is now the actionable batch
`ctx-clarify` accepts:

- 0 missing: no suggested questions.
- 1 missing: the missing dimension's template question plus one
  supplement question asking about additional constraints,
  limits, or unknowns — fields a draft already carries — never
  a repeat of information the raw text already supplied.
- 2–3 missing: one template question per missing dimension.
- 4 missing: the first three dimensions in canonical order
  (goal, context, scope); the remaining dimension stays missing
  and is named in `suggested_questions_note` for a follow-up
  clarification.

New output fields (additive, no existing field changed meaning):
`suggested_questions_dimensions` (dimensions the batch's
template questions cover; the supplement question covers none)
and `suggested_questions_note` (batching rule in words).
Assessment is still the same keyword heuristic, not a model and
not semantic understanding; no provider or semantic-model scope
was added. C6 test_01 was updated to the new batching rule
(4 missing → 3 suggested, dimensions `[goal, context, scope]`,
note naming `desired_output`).

## F03 — full-scope verdict precedence in the C6 acceptance runner

Bug (C6): `acceptance/run_acceptance_c6.py` computed
`full_scope = "PASS" if (failed == 0 and not_run == 0) else
"NOT_RUN"`, so synthetic `RESULTS=[FAIL]` and
`[FAIL, NOT_RUN]` both yielded `full_scope=NOT_RUN` even
though the exit code was already 1.

Fix: the aggregation is extracted into `aggregate_full_scope()`
and now applies precedence any required FAIL → verdict FAIL,
exit 1; else any required NOT_RUN/INCONCLUSIVE → verdict
NOT_RUN (incomplete), exit 2; else PASS, exit 0. Counts now
include `inconclusive`, and completed-required excludes both
NOT_RUN and INCONCLUSIVE. No acceptance case (B01–B17) was added,
removed, or reworded; the real C6R1 run keeps the healthy
24 PASS / 2 NOT_RUN shape (exit 2, full_scope NOT_RUN). The C5
runner is untouched.

## Files changed (repo-relative, C6R1 submission)

- `control_room/backend.py` — F01 draft binding + review/propose
  guards; F02 assess batching.
- `control_room/C6R1_NOTE.md` — this note (new file).
- `acceptance/run_acceptance_c6.py` — F03 aggregation precedence.
- `tests/test_intake_c6.py` — test_01 (F02 batching) and test_10
  (F01 older-draft approval) updated to the fixed rules; all
  other C6 tests unchanged.
- `tests/test_intake_c6r1.py` — new regression file (10 tests):
  F01a pending clarification blocks approve/propose; F01b new
  source blocks until fresh draft; F01c answered clarification
  blocks until fresh draft (including identical re-draft still
  stale); F01d REVISE on a stale draft enables nothing; F01e
  older-draft approval rejected after a newer draft; F02a–d
  suggested batches accepted by `ctx-clarify` for 4/1/2/3
  missing dimensions; F03 aggregator precedence on synthetic
  cases including the exact frozen repro inputs.

Unchanged by design: `control_room/cli.py`, `control_room/
__init__.py`, `control_room/README.md`, `control_room/
C6_NOTE.md`, `control_room/C5R1_NOTE.md`, `control_room/
C5_BUILD_NOTE.md`, all fixtures, all C4/C5 tests, the legacy
`propose`/`decide` flow, and the C5 acceptance runner.

## What C6R1 does NOT prove

Same boundary as C6: full-scope acceptance, pentest,
packet-level no-egress, live provider/worker integration,
runtime knowledge retrieval, measured owner baseline, owner
feedback, product acceptance, or whole-system verification.
Those remain NOT_RUN / PENDING unless a real run or a real
owner decision establishes them. The acceptance runner is
builder evidence, not a reviewer verdict.
