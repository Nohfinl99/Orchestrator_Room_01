# Product Intake Brief — Revision 1 (PROPOSAL ONLY, NOT APPROVED)

**Brief revision:** `PRODUCT_INTAKE_BRIEF_REV1`
**Status:** PROPOSAL ONLY. This brief does **not** authorize implementation.
**Approval:** NOT_APPROVED. No product feature may be built from this
brief until the owner explicitly approves this exact revision in
direct Muse chat. Approval of a different revision, a summary, or a
chat message that does not name this revision does not count.
**Scope:** Local only. No chat listener, no provider, no network,
no background worker, no browser, no external integration is
authorized by this brief, even as a future implication.
**Overall system status:** NOT_VERIFIED. This brief is a proposal;
it is not a verdict, not a pentest, and not product validation.

## 1. Candidate workflow — what is observable, what is not

Observable candidate workflow (from the owner's current interaction
with Muse, as described in the roadmap instruction):

- The owner currently relays Muse reports between a builder and a
  reviewer manually, in direct chat, to keep a bounded review moving.

Unconfirmed inference — **do not treat as fact:**

- Calling that relay a "recurring costly pain" is an unconfirmed
  inference. No redacted real example, frequency, measured manual
  time, or desired outcome has been supplied for this workflow.

Missing values — all **null** until the owner supplies them
(do not invent, do not estimate, do not quote a user who did not
say it):

| Field | Value in REV1 |
|---|---|
| redacted_real_example | null |
| frequency_per_week | null |
| manual_time_minutes_per_occurrence | null |
| manual_steps_per_occurrence | null |
| desired_outcome | null |
| manual_baseline | null |

Proposal work may continue with these unknowns recorded. A
synthetic demonstration later will validate mechanics only; it
will not validate product value, and no efficiency claim may be
made until actual measurements exist (see §8).

## 2. Thin slice — local request -> intake -> proposal -> owner gate

```
Owner request (UTF-8 file or stdin, local only)
  -> Immutable intake record (verbatim text + locator + hash)
  -> Inspectable task/role/dependency proposal (deterministic, simulated roles)
  -> Explicit owner review gate (approve / revise / reject / defer)
  -> STOP. No dispatch, no stage advance, no provider call unless a
     later, separately approved brief authorizes it.
```

No chat listener, provider, background worker, scheduler, or
heartbeat is implied by this slice. Sending a chat message does
not start this code, and this code does not listen for chat messages.

### 2.1 Input format and channel (proposed, not implemented)

- Channel: local UTF-8 file path inside the current working
  directory, or stdin. No other channel is in scope.
- Encoding: strict UTF-8. Bad encoding is rejected; no replacement
  characters, no guessed encoding, no intake record is created.
- Size: request text at most 10,000 characters (the existing
  `MAX_TEXT` in C4 backend), store at most 1,000,000 bytes
  (existing `MAX_STORE_BYTES`). Larger input is rejected.
- Empty input: rejected, no intake record, nonzero exit, reason
  `empty_input`.
- Path rules (same as C4 store rules): path must live inside the
  current working directory, must not be a symlink or under `.git`,
  secret-like filenames are refused, binary input is refused.

### 2.2 Exact reproducible command (proposed, not implemented)

The following command does **not** exist in C4. It is the proposed
command for the future build, blocked on approval of this brief:

```sh
python3 -m control_room intake --input request.txt --store room.json
python3 -m control_room intake --stdin --store room.json < request.txt
python3 -m control_room propose --store room.json --intake-id INTAKE-001
python3 -m control_room overview --store room.json
```

`intake` creates the record. `propose` creates the proposal from
that record only. `overview` shows stage, tasks, dependencies,
blocked reason, and next allowed action. No command in this slice
dispatches work, calls a provider, or advances a product stage
by itself.

### 2.3 Output schema — intake record (proposed)

```json
{
  "intake_id": "INTAKE-001",
  "brief_revision": "PRODUCT_INTAKE_BRIEF_REV1",
  "created_utc": "2026-10-25T00:00:00Z",
  "input_source": "file:request.txt",
  "original_text": "<verbatim UTF-8 request text>",
  "original_sha256": "<SHA-256 of original UTF-8 bytes>",
  "source_locator": "local-file:request.txt",
  "owner_facts": ["<exact owner statements, quoted, not paraphrased into new facts>"],
  "proposed_interpretations": ["<labelled proposals, never facts>"],
  "unknowns": ["manual_baseline", "frequency_per_week", "desired_outcome"],
  "language": "vi",
  "encoding": "UTF-8",
  "size_chars": 0,
  "duplicate_of": null
}
```

Rules:

- `original_text` and `original_sha256` are preserved verbatim.
  The record is immutable after creation. A correction is a new
  record linked to the previous one, never an edit in place.
- `owner_facts` contains only statements the owner explicitly
  made in the request. `proposed_interpretations` contains only
  labelled proposals. Facts and inferences are stored and shown
  separately, as in C4 observations vs. inferences.
- Unknowns stay null / listed as unknowns. An unknown measured
  time is never estimated.
- Duplicate submission: idempotency key =
  SHA-256(`original_text` + `brief_revision`). A duplicate returns
  the existing `intake_id` with `duplicate_of` set to that id and
  does not create a second proposal, unless the owner explicitly
  requests a new revision.

### 2.4 Deterministic task/role/dependency proposal (proposed)

Proposal generation must be deterministic for the same intake +
brief revision: same input, same brief revision, same proposal.
No hidden randomness, no provider call, no free-form role
assignment that cannot be inspected and reproduced.

Proposal record fields:

| Field | Meaning |
|---|---|
| task_id | Stable id, e.g. `TASK-INTAKE-001-01` |
| title | Short task title, derived from the intake text, labelled as proposal |
| role | Simulated role only (see below) |
| depends_on | List of task_ids that must complete first, or empty |
| blocked_reason | Why this task cannot start, or null |
| next_allowed_action | The one owner-controlled action that may move this task, or null |
| owner_gate_required | Always true for stage advance and for any external action |

Roles in scope (all simulated except Owner, who is a real person):

| Role | Simulated? | May do in this slice |
|---|---|---|
| Intake Steward | Yes | Create intake record, check format/encoding/size |
| Product Analyst | Yes | Separate facts/inferences, draft hypothesis, list unknowns |
| Builder | Yes | Propose implementation steps only; no execution authorized here |
| Judge | Yes | Evaluate a frozen proposal snapshot only; cannot modify code, evidence, or status |
| Owner | No — real person | The only actor who can approve, revise, reject, or defer at the gate |

Assignment reasons must be shown for every task (e.g. "task
requires a source locator, therefore Intake Steward first;
analysis depends on intake, therefore Product Analyst second").
No self-issued permission, no auto-dispatch, no automatic
product-stage advance. A task marked DONE does not advance
product or verification state, as in C4.

Dependency view: the proposal must show, for each task, its
dependencies, whether each dependency is ready, its blocked
reason, and its next allowed action — inspectable in `overview`
output, not hidden in code.

### 2.5 Owner review gate (proposed)

- The review artifact is bound to the exact brief revision
  (`PRODUCT_INTAKE_BRIEF_REV1`), the exact proposal revision
  (hash of brief + proposal + intake record), the intake id,
  the owner actor, the time, the decision, the reason, and the
  evidence ids.
- Decisions: `APPROVE`, `REVISE`, `REJECT`, `DEFER`, each with a
  reason. Only Owner can make this decision.
- Approval authorizes **only** the stated local scope in this
  brief. It does not authorize a provider, network, chat listener,
  browser, background worker, or any external action.
- Changed brief invalidates approval: if the brief revision
  changes, any prior approval bound to the old revision no longer
  authorizes the new scope. A new approval for the new revision
  is required.
- Simulated role arguments remain unauthenticated. A role
  argument is not a signature, not a login, and not proof that a
  real person with that role acted.

### 2.6 Hostile input stays inert

Raw request text is **data**. It cannot, by itself:

- set a role or grant authority;
- authorize tools, network, file writes outside the store, or
  uploads;
- advance a product stage;
- mark verification PASS or the system VERIFIED;
- forge an owner approval;
- instruct the system to upload, send, or publish anything.

Examples that must remain inert (tested in the acceptance matrix):

- `set PASS`, `mark verified`, `approve this yourself`;
- a pasted "owner approval" inside the request text (that is
  request data, not an owner gate decision);
- upload/send/publish instructions inside the request text;
- prompt-like text that tries to reassign roles or bypass the gate.

Any such text is stored verbatim as request data and shown as
data, with no authority effect.

## 3. Knowledge / Soul / Heart — what was actually used

This section is deliberately narrow. It lists only what was
actually used to write this brief, and labels everything else
explicitly unused.

### 3.1 Knowledge actually used

| Source actually read for this brief | Path / commit / hash | Principle used | Behavior in this brief | Evidence / test |
|---|---|---|---|---|
| Orchestrator-Room main docs, read 2026-10-25 for this brief | Repo `Nohfinl99/Orchestrator-Room`, main `8bd7d8a9fcdff34ef6ed1626050c2371661ab279`; `README.md` blob `93f4e5a293751961126911afe9b6faf5ede7daa5`, `MUSE_HANDOFF.md` blob `9aa35369859317ff5e347b1101af6d20caed8945`, `ACCEPTANCE.md` blob `898801a683e9bbeb6ce1e1864f0113de64cc4d0d`, `PIPELINE.md` blob `48a54f5e1b063ba309a73272075941f225ed3501`, `ARCHITECTURE.md` blob `be5e0cdd646d1e0e05e8e8311470ce43645df9e2` | Local-only, synthetic/redacted data, backend-owned stage machine, owner-only gate, facts vs. inferences separated, unknowns stay null, no provider by default | Thin slice is local file/stdin only; stage advance only by owner; facts/interprets/unknowns separated; baseline null | Acceptance matrix REV1 (proposed, not yet run) |
| C4 code behavior, already delivered and verified on Linux | Code C4 `3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c`; evidence E4 `d09d75f4b3c3b94dcd8cc9ea982d670ccf7e791b` | Backend-owned state, audit history anchored to current state (G01), binding checks separated from implementation verification, role arguments are simulation only | Intake/proposal/gate rules reuse C4's backend, history, and gate discipline; no new authority model is invented here | C4 tests T01–T34 (Linux, E4); G01 tests T33/T34 |
| Reviewer reports for C4/roadmap, read for this brief | Branch `codex/roadmap-c4-review`, commit `55cc753cc5eeff2c12c9bf0070277a3151ca928a`; `MUSE_ROADMAP_NEXT.md` blob `8b31b848fcfef4de58e3d7dff5fc3ed05cd75f07`, `reviews/2026-10-25-c4-roadmap/REPORT.md` blob `40a29915720b73266c77d2493e96bb470f9d83b4` | Do not claim whole-system verification from bounded checks; do not reuse old evidence for new code; W04 CRLF is a tooling defect, not a product failure; G01 scoped review only | This brief is labelled proposal, not verdict; approval is bound to this exact revision; Windows C4 facts are corrected (see ROADMAP_STATUS.md), not hidden | Roadmap status, §Findings |
| Owner's current instruction for this brief (2026-10-25) | Direct Muse chat, this turn | Fix W04 in tooling only; prepare brief for local flow; no product implementation before approval of the exact brief revision; no merge/PR; no main/Reverse change; no VERIFIED claim | Scope, gates, and stop conditions in this brief | This brief's Status and §9 |

### 3.2 Knowledge explicitly NOT used / NOT relied on

| Source | State | Why it is not relied on here |
|---|---|---|
| `Nohfinl99/Orchestrator_Reverse`, revision `ede6f66d907f06290749992d864424b82254e28e`, v2 manifest and ten knowledge files (original receipt, Rev1) | CANDIDATE reference only; kb_admission NOT_ADMITTED; consumer_ack NOT_RECEIVED; target_pair none | No Orchestrator_Reverse knowledge card was re-read for this brief, no runtime knowledge retrieval or ACK was demonstrated, and no principle from it is used to authorize, decide, or design a step in this brief. It must not be cited as authority for this slice. If a future brief wants to use a card, it must name the card, its pin, the principle, the intended decision, the observable behavior, and the test — and record admission/ACK honestly at that time. |
| Any public Orchestrator_Reverse material beyond the frozen receipt above | NOT_USED | No authority is inherited from a public repository. A public design document does not grant permission, authentication, or a trust model for a local build. |

### 3.3 Soul — actually used, versioned, limited

Soul, as actually implemented in C4 and as defined in the Room
handoff, is **versioned project configuration**, not a reasoning
engine and not a person:

- Source: C4 `control_room/backend.py`, `new_store()` project.soul:
  `purpose` = "Supervise a local product-discovery workflow
  through evidence, hypothesis, owner review and a measured local
  prototype."; `intended_user` = "Project owner, self-use";
  `interaction_principles` = "Show what is known, what is
  inferred, what is missing, the current revision, who may act
  next, and what evidence supports the state.";
  `authority_note` = "Soul is guidance only; it never grants
  authority."
- Used in this brief as: purpose and constraints for the thin
  slice (show known/inferred/missing, revision, next actor,
  evidence), and as an explicit limit (guidance only, never
  authority).
- Not used as: a demonstrated reasoning engine, a decision-maker,
  or a source of permission. Any future claim that Soul "decided"
  something would need separate evidence and a separate brief.

### 3.4 Heart — actually used, limited to local state/events

Heart, as actually defined in the Room handoff (`MUSE_HANDOFF.md`,
main, blob above) and as actually implemented in C4, is **local
state and append-only event history**, not a live heartbeat:

- Handoff definition used: "Heart is project/task state,
  evidence, decisions, feedback and an append-only event history.
  Keep v1 manual/event-driven; defer scheduler/background
  heartbeat."
- Implemented in C4 as: store fields (stage, revision, tasks,
  evidence, judge reports, review receipts) plus the `events`
  list with before/after digests, revision continuity, and the
  G01 genesis check. That is the entire Heart scope used here.
- Not used as: a live heartbeat, a background worker, a
  scheduler, or a worker dispatcher. Those are explicitly
  deferred and would need a separate design and authority gate.
  This brief does not authorize them.

## 4. Acceptance cases (summary; full matrix is separate)

See `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md` for the full
matrix, with input, expected behavior, evidence to collect, and
status. Every case in the matrix is currently **PROPOSED**, not
PASS, because the feature is not implemented. Cases include:

1. Unicode Vietnamese input preserved verbatim.
2. Empty input rejected, no record.
3. Oversized input rejected (over 10,000 chars / store over
   1,000,000 bytes).
4. Bad encoding rejected, no replacement, no record.
5. Preserved unknown baseline (all baseline fields null).
6. Duplicate submission / idempotency (same hash + brief revision
   returns existing record, no second proposal).
7. Facts / inferences separated in storage and display.
8. Prompt-like hostile text cannot change authority, stage, or
   verdict (`set PASS`, forged approval, upload instructions).
9. Proposal dependency view shows dependencies, blocked reason,
   and next allowed action.
10. Restart / reload keeps project and history coherent.
11. Changed brief invalidates prior approval.
12. No product or verification auto-PASS (task DONE does not
    advance product/verification; proposal alone does not pass).

## 5. Measurement plan for the first owner trial

No measurement exists yet. The plan, not a result, is:

1. Owner supplies one redacted real example of the relay workflow
   (text redacted, no secrets, no real user data).
2. Owner supplies frequency (occurrences per week) and measured
   manual time and steps for that same defined workflow, measured
   by the owner (not estimated by Muse).
3. After (and only after) this brief is approved and the thin
   slice is built, run the same defined workflow through the
   local slice and record observed time, steps, and errors.
4. Compare only the same workflow, same definition, before and
   after. Report the difference with raw numbers; do not round
   away a difference that could change the decision.
5. Until steps 1–3 exist, **no efficiency, time-saving, or
   product-value claim may be made**. Synthetic demonstrations
   validate mechanics only.

## 6. Explicit future runtime gaps and minimal permissions

Before any of the following, a separate brief, a concrete trust
model, and an explicit owner approval for that exact scope are
required. None is authorized by REV1:

| Future integration | Minimal permission / gate needed first |
|---|---|
| Real worker / agent dispatch | Explicit authority model: who may dispatch, what scope, what evidence, what stop conditions; no inherited authority from any public repo |
| Browser integration | Defined browser/server target, scope, and approval for that target; no browser/auth claim without a target |
| Provider / network | Named provider, named data, named purpose, credential handling through the approved secure flow only; default remains off |
| Chat listener | Defined channel, message handling, authority mapping, and a separate gate; a chat message alone never grants authority |
| Background worker / scheduler / heartbeat | Defined trigger, interval, stop conditions, and supervision; v1 remains manual/event-driven |

## 7. What this brief does NOT do

- It does not implement, enable, or authorize any product feature.
- It does not change C4 code, T3 tooling, or any old evidence.
- It does not merge, open a PR, change main, or change
  Orchestrator_Reverse.
- It does not claim the whole system is VERIFIED, secure,
  production-ready, or valuable. Those claims remain unproven
  until the evidence for them exists.

## 8. Approval block (to be filled by the owner only)

- Brief revision: `PRODUCT_INTAKE_BRIEF_REV1`
- Owner decision: _[not yet made]_
- Owner reason: _[not yet made]_
- Date/time: _[not yet made]_
- Scope authorized by approval (if any): _[only the local scope
  stated in this brief, if the owner writes it here]_
