# Contextual intake — current use (C6R1, after review REV-CTX-001-R1)

This is a docs-only revision. It changes no code, no test, no
fixture, and no frozen commit. It corrects one documentation
defect (CTX-R1-DOC01) and states the current-use and
supervised-trial handoff rules for the contextual-intake slice
exactly as implemented in C6R1. Where this document and an older
note disagree, this document governs for current use; the older
note is left unchanged because its commit is frozen.

## Frozen pins (do not edit)

- Code C6R1: `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255`
  (branch `muse/local-control-room`, 5 paths vs C6).
- Evidence E6R1: `ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7`
  (separate commit; `docs/reports/RUN_REPORT_C6R1.md` + `evidence/c6r1/`).
- Review REV-CTX-001-R1: verdict `APPROVED_SCOPED`, artifact
  commit `17da045bb042fa1927cbd6f96028f3fb73537878` on branch
  `codex/ctx-001-r1-review`, report
  `reviews/ctx-001/r1/REPORT.md`, in reply to submission
  `SUB-CTX-001-R1`.
- Prior pins, preserved: code C6
  `385f503b003479d4ae957d97cf3657e3900e1a37`, evidence E6
  `da2d318cdad0ea268e8fc709f59fc1462321f4c9`.
- Channel: `ORCHESTRATOR_CHANNEL.md` on branch
  `codex/orchestrator-channel`, review R1 at revision 9
  (status `APPROVED_SCOPED`, turn `MUSE`).

## What the slice is, honestly

Local, structured, rule-based contextual intake on top of the
control-room slice. CLI flow: raw immutable intake →
keyword-heuristic assess → locator-only context sources →
2–3 clarification questions → verbatim answers → structured
rewrite draft → owner review of the exact rewrite digest →
contextual proposal bound to the approved rewrite. Assessment is
a keyword scan, not semantic understanding; draft fields are
operator-supplied, not generated; a rewrite review is
`OPERATOR_ASSERTED` — an audit label only, not authentication
and not product acceptance. There is no provider, no live
worker, no chat listener, no runtime knowledge retrieval.

## Verified counts and gaps (no wider claim)

- Linux, Python 3.12.3: suite 83/83 (36 C4 + 21 C5 + 16 C6 +
  10 C6R1 regressions); acceptance 26 subcases: 24 PASS,
  0 FAIL, 2 NOT_RUN, completed required 24/24, full-scope
  verdict NOT_RUN, runner exit 2.
- Windows 11, Python 3.14.4 (reviewer rerun): suite 83
  attempted, 81 PASS, 2 SKIP (legacy WinError 1314 symlink
  cases, NOT_RUN not PASS); acceptance 24 PASS, 2 NOT_RUN,
  runner exit 2.
- Independent reviewer controls: 14 real-CLI scenarios PASS,
  6 synthetic aggregation scenarios PASS, history valid,
  input hash preserved.
- Still open / not run: packet-level no-egress (B16), owner
  product acceptance (B16, test approvals are synthetic),
  full pentest, live integration, measured owner baseline
  (null, NOT_MEASURED). Whole system: NOT_VERIFIED. No merge,
  no PR, no main change, no Orchestrator_Reverse change.

## DOC01 correction — repeat review after context moves

### The incorrect sentence

`control_room/C6R1_NOTE.md` (F01 section, frozen in C6R1)
states, without qualification: "a repeat review (same digest,
decision, and reason) returns the existing review record; it
creates no new approval, and propose still blocks a new
proposal when context moved."

That sentence is true only when context has NOT moved since
the draft. Read on its own, it wrongly promises existing-review
readback even after context moved. This section replaces it.
`C6R1_NOTE.md` itself is not edited, because its commit is
frozen; the correction lives here.

### The corrected rule (code order in `ctx_review_rewrite`)

For a review request, the checks run in this order:

1. Digest binding. If the expected digest does not match the
   stored rewrite digest, or the stored digest does not
   recompute, the review is rejected (`REJECTED_STALE`,
   exit 2, rejection event, no decision).
2. APPROVE guards (C6R1/F01, APPROVE only). If an unanswered
   clarification exists for the intake, the review is rejected
   (`clarification_open`, exit 2, no decision). If the current
   context-change count differs from the draft's bound count,
   or current source ids differ from the draft's bound source
   ids, the review is rejected (`REJECTED_STALE`, exit 2, no
   decision). A fresh draft (binding the new context) plus a
   fresh review is required.
3. Duplicate lookup — only reached when steps 1–2 pass. If a
   review with the same digest, decision, and reason already
   exists, it is returned with `already_exists=true` and
   `new_review_created=false`; it is not double-counted and it
   creates no new approval.

Consequences:

- A repeated identical APPROVE after context moved does NOT
  return the existing review. It exits 2 before the duplicate
  lookup, records a rejection event, and creates no decision.
  That rejection is the safe behavior, not a bug.
- Non-approving decisions (REVISE/REJECT/DEFER) are not
  blocked by the step-2 guards, because they enable no
  proposal; a later APPROVE of the same stale draft is still
  rejected by step 2.
- The repeat-proposal rule is unchanged and separate: a repeat
  of an already created proposal returns the frozen proposal;
  the step-2 guards govern only the creation of a NEW
  proposal. `ctx-propose` repeats the step-2 checks as defense
  in depth for approvals recorded before C6R1.

### Reviewer control that proves it (DOC01 evidence)

From `reviews/ctx-001/r1/review-evidence/repeat-review-doc-control.json`:

1. Intake (explicit goal/context/scope/output), draft, then
   first `ctx-review-rewrite ... APPROVE` → exit 0.
2. `ctx-clarify` creates a pending clarification for the same
   intake (left unanswered).
3. Repeated identical `ctx-review-rewrite ... APPROVE` →
   exit 2, error: `clarification_open: an unanswered
   clarification exists for this intake; no decision created`.
4. `verify-history` → chain valid. No proposal is created by
   the rejected repeat.

Operator instruction: when a repeat APPROVE exits 2, do not
retry it. Answer the clarification (or add the new source
into a fresh draft), draft again, and review the new digest.

## Supervised owner-trial handoff (procedure, not an executed trial)

No real owner trial is claimed here. This is the procedure to
use when a real owner trial is requested, already inside the
CTX-001 scope:

1. Start from a real owner request. Preserve the raw request
   verbatim (immutable intake, SHA-256 recorded); never rewrite
   the raw, never invent missing goal/context/scope/output.
2. If essential goal/context/scope/output is missing, ask one
   batch of 2–3 precise questions and wait. Zero contextual
   proposals before answers. Answers are stored verbatim.
3. Draft the structured rewrite (goal/context/scope/
   desired_output/constraints/unknowns/labelled inferences/
   next_action, with source links, revision, and digest).
   Inferences stay labelled as inferences, never facts.
4. Present the exact rewrite revision and digest to the real
   owner for review. Only a real APPROVE of that exact digest
   may create a contextual proposal, and the proposal must
   bind the raw id, the approved rewrite digest, the answers,
   and the context revision. Any context, answer, or rewrite
   change invalidates the approval; a fresh draft and fresh
   review are required.
5. `WAITING_OWNER` is set only for a genuinely unresolved
   owner decision, with the owner's questions recorded
   verbatim. Never answer on the owner's behalf, never
   fabricate an answer, an approval, or owner feedback, and
   never ask the owner to relay outputs or resupply known
   context.
6. Stop conditions (owner-decision-required, do not proceed
   past them on this slice's authority): merge, PR, main
   change, Orchestrator_Reverse change, provider/worker/chat
   listener, credentials, product acceptance, whole-system
   VERIFIED. Test approvals are synthetic and never count as
   owner approval.

## What this document does not do

It does not change code, tests, fixtures, acceptance cases, or
any frozen commit; it does not add a roadmap; it does not
claim full-scope acceptance, product acceptance, or
whole-system verification; and it is not itself a reviewer
verdict or an owner decision.
