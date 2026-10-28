# C5 Build Note — thin local intake slice (packet REV2.1 + F21)

**Status:** Code commit C5, built after owner approval recorded below.
This note is part of the code commit; it is not a roadmap rewrite,
not a product acceptance, and not a verification verdict. Overall
system status remains **NOT_VERIFIED**. A reviewer verdict on the
frozen C5/E5 snapshot is still pending, and owner product acceptance
is still **PENDING**.

## Approval record (gate for this build)

- **Source:** Direct Muse chat, web client (the approval channel
  the owner used for this slice).
- **Actor:** NohFinl (owner).
- **Time:** 2026-10-25 23:50:52 Asia/Bangkok, by tapping the option
  "Duyệt build C5 theo packet REV2.1 + F21".
- **Scope:** Build C5 exactly per packet REV2.1 (addendum
  SHA-256 `3a3548367f049742865c238e8059ac917f298a546fa8d30e23bbc98b87475520`,
  checklist SHA-256
  `58bec31694e1955fda93d9b2dc71ae7aeeb5951dd7b51ffe1acb75ac99374627`)
  plus checker fix F21 (commit `bef96ccf3dabda9088491a615eec23cbc8dfe32c`,
  evidence E21 `1e5907658fbe6dd188ef1b8552fa48c053d040a3`).
- **Not approved by this record:** No merge, no PR, no change to
  main or to Orchestrator_Reverse, no product acceptance, no claim
  that the whole system is verified.

## What C5 implements (Steps 1–5 of the checklist)

- **Step 1 — Intake:** `intake --input <file> --store <store>` and
  `intake --stdin --store <store>`. Input is read as bytes, at most
  20,001 bytes, before decode. Byte cap 20,000 before decode, then
  strict UTF-8, BOM rejected (never stripped), NUL, whitespace-only,
  and char cap 10,000 code points, in that order. One deterministic
  reason code per failure, nonzero exit, no record, no event.
  Line endings are classified LF / CRLF / mixed / bare-CR / none
  and preserved verbatim; derived statements split on breaks only.
  Baseline is exactly six fields, all null, with provenance source
  null, until an owner supplies values through a mechanism that is
  **not** part of C5 (no baseline-supply command was in the packet,
  and none was invented).
- **Step 2 — Dedupe and correction:** Same bytes → duplicate
  response only (golden shape) plus a `duplicate_submission`
  event; original record unchanged; no new proposal. Valid
  correction (`--supersedes` pointing at an existing intake, new
  bytes) → new record, new id, old record unchanged. No-op,
  conflict, and supersedes-not-found corrections are rejected with
  reason codes `correction_no_op_same_bytes`,
  `correction_conflict_existing_id`,
  `correction_supersedes_not_found`, each with its own rejection
  event, via `IntakeRejectedError` (the CLI saves the event, then
  fails, mirroring `DecisionRejectedError`).
- **Step 3 — Propose and view:** `propose --store --intake-id`
  returns exactly four fixed template tasks (capture, separate,
  discovery proposal, owner review) with fixed roles, dependencies,
  and reasons; `proposal_id = "PROP-" + intake_id`; digest is
  SHA-256 of the canonical JSON payload, excluding digest,
  timestamps, view, and decision fields. Repeat propose returns
  the golden repeat shape with `already_exists: true`, no second
  proposal, no event. View is computed at `overview` and
  `proposal-view` time (readiness, blocked_reason,
  next_allowed_action per task); it is never stored in the payload
  and never changes the digest.
- **Step 4 — Decide:** `decide --store --proposal-id
  --expected-proposal-digest --expected-brief-revision
  --expected-intake-id --decision --reason --operator --source`.
  All eight flags are required. The backend recomputes the current
  payload digest, brief, and intake and compares them to the
  expected bindings inside the same load/lock/CAS save sequence as
  the decision write (the CLI owns the OS lock and the revision
  CAS check). Missing flags are rejected by the argument parser
  (exit 2, no store change). Wrong-format bindings, an invalid
  decision enum, or an empty reason/operator/source are rejected
  by the backend with a reason code (no event, no decision).
  A binding mismatch is `REJECTED_STALE`: no decision, plus a
  `decision_attempt_rejected` event. A successful decision has
  provenance `OPERATOR_ASSERTED` only; it is not owner
  authentication and not owner product acceptance. A repeat of an
  identical decision returns the existing decision with
  `already_exists: true` and is not double-counted.
- **Step 5 — Audit and reload:** Every intake, duplicate, propose,
  correction, decision, rejection event, and proposal task
  completion is recorded as a history event with before/after
  content digests and revision continuity, reusing the C4 history
  pattern. No event edits an immutable record. Reload in a new
  process shows the same intake, proposal, decision, and history
  hashes. Task DONE does not advance the product stage or
  verification. No provider, worker, listener, scheduler, browser,
  or network is added in C5.

## Deliberate additions beyond the literal checklist (flagged for the reviewer)

1. **`complete` command** (proposal task completion). The checklist
   names `next_allowed_action: complete <task>` in the view and
   acceptance A32 ("overview before/after task DONE"), but lists no
   command that can mark a proposal task DONE. Without one, the view
   is static and A32 cannot be exercised. C5 therefore adds a
   minimal `complete --store --proposal-id --task-id`: it succeeds
   only when the task's dependencies are DONE, otherwise it rejects
   with `blocked_dependency` (no event, no change); a repeat reports
   `already_done` with no new event; completing never changes the
   project stage, verification, proposal payload, proposal digest,
   or any decision. If the reviewer rejects this addition, it can
   be removed without touching intake, propose, or decide.
2. **DONE view state.** The golden view covers only the initial
   state (READY / BLOCKED). C5 extends the view with readiness
   `DONE`, blocked_reason null, next_allowed_action null for a
   completed task. No other view field changes.
3. **Exit codes.** C4's CLI reports failures with exit 2
   (`_fail`). C5 rejections therefore exit 2, not 1. The checklist
   and acceptance cases say "nonzero exit"; C5 pins that to 2.
   Duplicate, propose repeat, decide repeat, and complete repeat
   exit 0 with an explicit already-exists / duplicate flag.
4. **Record timestamps to the second.** New C5 domain records use
   UTC `YYYY-MM-DDTHH:MM:SSZ`, matching the intake schema pattern.
   The C4 event timestamp format (microseconds, parseable) is kept
   for audit events, which are not intake schema records. Timestamps
   are never part of an id or digest.
5. **Content digest and genesis compatibility.** `new_store()` is
   unchanged (no C5 keys), so an empty-event store still matches
   the pristine C4 genesis exactly and all C4 tests pass unchanged.
   C5 collections are created on first C5 use and are included in
   `content_digest()` only when non-empty, so pre-C5 stores keep a
   valid history anchor while non-empty C5 data is anchored by the
   chain (a tampered intake record fails `verify-history`).
6. **Actor labels.** C5 commands take no `--role` (proposal roles
   are simulated template text). Intake/propose/complete take an
   optional `--actor` audit label (default `local-operator`).
   Decide takes no separate `--actor`; its event actor is the
   `--operator` label. Labels are not authentication.

## What C5 does not do (honest limits)

- No runtime retrieval, admission, ACK, or live-agent coordination
  has been demonstrated. Knowledge/Soul/Heart stay as in REV2:
  only Room main docs and C4 behavior were used; Soul is versioned
  project configuration ("guidance only; never grants authority")
  and changes no task, role, or decision; Heart is local state plus
  append-only event history, with no live heartbeat, worker,
  scheduler, chat listener, or provider.
- Baseline values remain null. No efficiency or product-value claim
  is made. The changed-brief case (A13) is tested via expected
  brief mismatch, because C5 has no brief-editing command; a real
  brief edit invalidating a prior approval is a contract property,
  not a demonstrated C5 run.
- Packet-level egress monitoring, full pentest, real disk-failure
  recovery, Windows runs, and a full independent C4/C5 acceptance
  audit remain NOT_RUN and are not claimed here.
- The C5 decide does **not** move the C4 product stage (which stays
  INTAKE in a fresh store). The C5 gate and the C4 stage machine are
  separate; a C5 OPERATOR_ASSERTED decision must not be read as a
  C4 owner stage transition or as product acceptance.

## Files changed in C5 (code commit only)

- `control_room/backend.py` (C5 section appended; `content_digest`
  and `overview` extended as described above; no C4 function
  behaviour changed for pre-C5 stores).
- `control_room/cli.py` (C5 commands, input boundary, rejection
  event save; no C4 command changed).
- `control_room/__init__.py` (version 0.5.0).
- `control_room/README.md` (C5 section appended; C4 docs kept).
- `control_room/C5_BUILD_NOTE.md` (this file).
- `tests/test_intake_c5.py` (18 builder tests; C4 tests untouched).

Evidence (test logs, A01–A33 acceptance results, store hashes) is
in the separate evidence commit E5, never in this code commit.
