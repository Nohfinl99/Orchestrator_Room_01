# Product Intake Brief — Revision 2 (PROPOSED, NOT APPROVED)

**Brief revision:** `PRODUCT_INTAKE_BRIEF_REV2`
**Supersedes (as a proposal, not as a code change):**
`PRODUCT_INTAKE_BRIEF_REV1` (SHA-256
`fbc881a732178330cad024f4fb7fafa7fcc1defc48a67e3703dd560937b37dbc`).
REV1 is preserved; REV2 does not edit it. Where REV1 and REV2
differ, REV2 is the proposal under review, and REV1's wording
must not be used to fill a REV2 gap.
**Status:** PROPOSED_NOT_APPROVED. This brief does **not**
authorize implementation.
**Approval:** No owner approval for REV2 has been recorded.
A build may start only after the owner gives a clear instruction
approving this exact revision, with its source, actor, time, and
scope recorded (see §2.6). Until then, the build is BLOCKED.
A meeting request, a reviewer verdict, and a local gate decision
are **not** owner product acceptance.
**Scope:** Local only. No provider, worker, listener, auth
server, scheduler, browser, or network is authorized by this
brief, even as a future implication.
**Overall system status:** NOT_VERIFIED. This brief is a
proposal; it is not a verdict, not a pentest, and not product
validation.

## 1. Thin slice — unchanged shape, now with a contract

```
Owner request (local UTF-8 file or stdin, §5)
  -> Immutable intake record (§3, §4)
  -> Deterministic, rule-based task proposal, template INTAKE_TEMPLATE_V1 (§3)
  -> Local operator review gate, OPERATOR_ASSERTED (§2)
  -> STOP. No dispatch, no stage advance, no provider call unless
     a later, separately approved brief authorizes it.
```

No chat listener, provider, background worker, scheduler, or
heartbeat is implied. Sending a chat message does not start
this code, and this code does not listen for chat messages.

## 2. Gate — local operator decision (BRI01)

REV1 promised that "only the real Owner can approve" while
offering no command, no schema, and no authentication. That
promise is withdrawn. REV2 defines what the gate actually is:

### 2.1 What the gate is

- The gate is a **local operator decision**: a person with
  access to the local operating system and store actively
  invokes a decision command on the local machine. That is the
  entire trust boundary.
- **Provenance is `OPERATOR_ASSERTED`, never
  `AUTHENTICATED_OWNER`.** The decision record states who the
  operator claimed to be (a free-text label supplied at
  invocation), the source channel, the time, and the scope. It
  does not prove the operator's identity, role, or authority,
  and it must never be described as owner authentication.
- No login, auth server, or credential check is added by this
  slice. Adding one would need a separate brief and trust model.

### 2.2 Proposed decision command (not implemented)

```sh
python3 -m control_room decide --store room.json \
  --proposal-id PROP-INTAKE-xxxxxxxxxxxxxxxx \
  --decision APPROVE --reason "Owner reviewed proposal" \
  --operator "local-operator" --source "local-cli"
```

`--decision` accepts exactly one of `APPROVE`, `REVISE`,
`REJECT`, `DEFER`. Any other value is rejected, no decision
is recorded, exit is nonzero.

### 2.3 Decision schema

```json
{
  "decision_id": "DEC-<16 hex chars of SHA-256(proposal_digest + 0x00 + decision + 0x00 + reason_utf8)>",
  "proposal_id": "PROP-INTAKE-xxxxxxxxxxxxxxxx",
  "proposal_digest": "<SHA-256 of canonical proposal payload, §3.4>",
  "brief_revision": "PRODUCT_INTAKE_BRIEF_REV2",
  "intake_id": "INTAKE-xxxxxxxxxxxxxxxx",
  "decision": "APPROVE",
  "reason": "<operator-supplied reason, verbatim>",
  "operator_label": "<free-text label supplied at invocation, NOT verified>",
  "source_channel": "local-cli",
  "provenance": "OPERATOR_ASSERTED",
  "decided_utc": "<actual UTC time at decision; NOT part of decision_id or any digest>"
}
```

Note on `decided_utc`: it is recorded for audit, but it is
**not** part of `decision_id` and not part of any digest.
Two identical decisions (same proposal digest, same decision,
same reason) produce the same `decision_id`; a second identical
invocation is a duplicate decision attempt, not a new decision,
and must be reported as such, not silently double-counted.

### 2.4 Bindings and stale rejection

A decision is accepted only if **all** of these bind:

- `proposal_digest` in the decision matches the current
  canonical proposal payload digest for `proposal_id`;
- `brief_revision` matches `PRODUCT_INTAKE_BRIEF_REV2`;
- `intake_id` matches the proposal's intake;
- `proposal_id` exists and has not been superseded by a new
  proposal for the same intake (there is only one proposal per
  intake in REV2, §4, so supersession here means a changed
  payload, not a second proposal).

If any binding fails, the decision is **REJECTED_STALE**:
exit nonzero, no APPROVE/REVISE/REJECT/DEFER decision is
created, and a separate `decision_attempt_rejected` event is
recorded with the attempted binding values and the reason
`stale_binding`. A stale attempt must never be upgraded to an
approval by reusing an old digest.

### 2.5 Hostile text and pasted approvals are never decisions

- Request text is **data**. Text inside a request that says
  `APPROVE`, `owner approves`, `set PASS`, or pastes a fake
  decision record does **not** create a decision, does not
  change a stage, and does not mark anything PASS.
- A decision exists only when the `decide` command above is
  invoked by a local operator with a matching proposal digest.
  Nothing in the intake text is parsed as a decision command.

### 2.6 Owner product acceptance is a different thing

- The local gate decision (§2.1–§2.5) is an operator assertion
  about a proposal. It is **not** owner product acceptance.
- Owner product acceptance of this brief means: the owner gives
  a clear instruction approving exactly
  `PRODUCT_INTAKE_BRIEF_REV2`, and that instruction is recorded
  with its **source, actor, time, and scope**. The source may
  be any channel where the owner actually gave the instruction;
  REV2 does **not** require a magic phrase and does **not**
  restrict approval to one chat channel, because a channel rule
  cannot limit a real owner's instruction. What it requires is
  a record: what was approved, who said it, when, from where,
  and what scope it covers.
- If no such clear instruction exists, owner acceptance is
  **PENDING**. A meeting, a review request, and a reviewer
  verdict do not count as acceptance.
- **Storage-owner limit, stated plainly:** the same person who
  owns the store can rewrite the whole store, including history,
  if they also recompute its digests. The C4 history chain can
  detect a partial rewrite, but it cannot prove identity or
  prevent a full rewrite by the storage owner. The gate is a
  local control, not a cryptographic proof of who acted.

## 3. Routing — one template, rule-based, deterministic (BRI02)

### 3.1 Template

- **Template version:** `INTAKE_TEMPLATE_V1`. Small, versioned,
  and fixed. It is not a smart agent coordinator and it does not
  choose workers, negotiate, or adapt to the request content.
- For **every** intake, the template produces exactly four
  tasks, in this order, with these fixed roles, dependencies,
  and reasons. Request content does not change the task list,
  the order, the roles, or the dependencies; it only appears
  verbatim in the intake record and in the proposal's intake
  binding.

| Task suffix | Title | Role | Depends on | Reason (fixed template text) |
|---|---|---|---|---|
| -T01 | Capture and preserve request | Intake Steward (simulated) | — | Proposal needs a preserved, hashed intake before any analysis; capture is first because no later step may change the original. |
| -T02 | Separate owner statements, interpretations and unknowns | Product Analyst (simulated) | -T01 | Analysis needs separated statements; it cannot run before capture, and it must not invent facts. |
| -T03 | Draft discovery proposal and dependency view | Product Analyst (simulated) | -T02 | Proposal needs separated statements and unknowns; it is a rule-based template output, not agent coordination. |
| -T04 | Owner review gate | Owner (real operator) | -T03 | Only the owner/operator at the gate may approve, revise, reject or defer; simulated roles cannot decide. |

- **Task IDs are stable:** `task_id = proposal_id + "-T01"` …
  `"-T04"`. No timestamp, no random value, no counter that
  depends on machine state is in a task ID.
- **Example concrete mapping** (golden fixture, §6): a synthetic
  request "summarise the weekly report for owner review" maps
  to exactly the four tasks above, because the template is
  fixed. The example is not evidence that the template
  understands the request; it is evidence that the template
  applies the same rules to every request.

### 3.2 Immutable proposal payload vs. computed view

- **Immutable proposal payload** (frozen at first `propose`,
  §4): `proposal_id`, `brief_revision`, `template_version`,
  `intake_id`, `intake_original_sha256`, `tasks` (each with
  `task_id`, `title`, `role`, `depends_on`, `reason`), and
  `notes` (labelled proposals only, e.g. "Roles are simulated
  except Owner; this template does not assign a real worker.").
- **Computed view** (recomputed at `overview` time, never
  stored in the payload): for each task, `readiness`
  (`READY` if every `depends_on` task is marked DONE in the
  store, otherwise `BLOCKED`), `blocked_reason` (template
  reason plus the list of not-yet-DONE dependencies, or null
  when ready), and `next_allowed_action` (for a blocked task:
  `complete <dependency task_id>`; for the review task when
  ready: `operator decide`; otherwise null).
- View changes do **not** change the proposal payload and do
  **not** change its digest. Payload changes do change the
  digest and invalidate any decision bound to the old digest
  (§2.4).

### 3.3 Canonical serialization and hash domains

- Canonical JSON: keys sorted, separators `(",", ":")`,
  `ensure_ascii=False`, encoded as UTF-8. No trailing newline
  is included in the hash input unless it is part of the
  canonical JSON itself (it is not: the canonical form has no
  trailing newline).
- `proposal_digest = SHA-256(canonical_json(proposal_payload))`.
- **Excluded from the digest** (to avoid self-reference and
  timestamp drift): `proposal_digest` itself, `created_utc`,
  `decided_utc`, all view fields (`readiness`,
  `blocked_reason`, `next_allowed_action`), and all decision
  fields. A proposal's identity and determinism never depend
  on a timestamp.
- **Included in the digest:** every payload field listed in
  §3.2, including `tasks` in order, `depends_on` in order,
  and `notes` in order. Changing any of them changes the digest.
- **UTF-8 domain:** all hashes in REV2 are SHA-256 over UTF-8
  bytes of the canonical JSON, except `original_sha256`, which
  is SHA-256 over the original request bytes (§5). No other
  hash function, encoding, or normalization is used.

### 3.4 Knowledge / Soul / Heart — what actually affects output

REV2 uses **only** Room documents for its rules. No
Orchestrator_Reverse knowledge is active, and no runtime
retrieval or live-agent coordination is claimed.

| Constraint / rule that actually affects template output | Locator | Behavior in REV2 | Acceptance case |
|---|---|---|---|
| Local-only, synthetic/redacted data, no provider by default | Room main `MUSE_HANDOFF.md` (main `8bd7d8a9…`), PIPELINE.md | Thin slice is file/stdin only; no provider/worker/listener in template tasks | Matrix REV2, A01–A04, A15 |
| Facts/inferences separated; unknowns stay null, never estimated | Room main `ACCEPTANCE.md`, `MUSE_HANDOFF.md` | `owner_statements` vs. `notes` separated; baseline nulls preserved (§4) | A07, A05 |
| Owner-only gate, bound to a specific revision, with actor/time/decision/reason/evidence | Room main `ACCEPTANCE.md`, `PIPELINE.md` | Gate in §2, bound to brief+proposal+intake, OPERATOR_ASSERTED, stale rejection | A17, A20, A21 |
| Backend-owned stage machine; task DONE does not advance product/verification | C4 backend (C4 `3d0bf76b…`), PIPELINE.md | Proposal view shows readiness only; no auto stage advance | A14 |
| Soul = versioned project configuration, guidance only, never authority | C4 `new_store()` project.soul; Room `MUSE_HANDOFF.md` | Soul purpose/principles constrain the template's wording (show known/inferred/missing, revision, next actor, evidence); Soul never grants authority and never changes a task, role, or decision | A22 |
| Heart = local state + append-only event history, v1 manual/event-driven | Room `MUSE_HANDOFF.md`; C4 store/events | Duplicate, propose-repeat, correction, and stale-decision events are recorded as history events, not as edits to immutable records (§4) | A06, A18, A20 |
| Orchestrator_Reverse knowledge | Candidate only: kb_admission NOT_ADMITTED, consumer_ack NOT_RECEIVED, target_pair none, revision `ede6f66d…` | **NOT USED.** No card, principle, retrieval, or ACK is used to authorise, decide, or design any step in REV2. If a future brief wants a card, it must name the card, pin, principle, intended decision, observable behavior, and test, and record admission/ACK honestly at that time. | A22 |

## 4. Dedupe, propose idempotency, correction (BRI03)

### 4.1 Intake identity (bytes + version domain)

- `intake_identity_input = original_bytes + 0x00 +
  "PRODUCT_INTAKE_BRIEF_REV2" (UTF-8) + 0x00 +
  "INTAKE_TEMPLATE_V1" (UTF-8)`.
- `intake_id = "INTAKE-" + first 16 hex chars of
  SHA-256(intake_identity_input)`.
- Same bytes under the same brief+template version produce
  the same intake_id. Different bytes, or a different brief
  or template version, produce a different intake_id. Identity
  never depends on a timestamp, filename, or machine state.

### 4.2 Duplicate submission — metadata only in response/event

- A second intake of the same bytes under the same
  brief+template version returns a **duplicate response**,
  not a new intake record:

```json
{
  "intake_id": "<existing intake_id>",
  "duplicate": true,
  "duplicate_of": "<existing intake_id>",
  "new_intake_created": false,
  "new_proposal_created": false,
  "event": "duplicate_submission",
  "note": "Original intake record unchanged."
}
```

- The original intake record is **not modified**: no
  `duplicate_of` field is written into it, no counter is
  incremented inside it. Duplicate metadata lives only in
  the response and in a separate history event.
- A duplicate intake does **not** create a proposal. Proposal
  creation is a separate `propose` step (§4.3).

### 4.3 Propose idempotency

- First `propose` for an intake creates exactly **one**
  proposal: `proposal_id = "PROP-" + intake_id`, with the
  payload in §3.2 and digest in §3.3.
- Repeating `propose` for the same intake returns the same
  proposal, same digest, with `already_exists: true` and
  `new_proposal_created: false`. It does not create a second
  proposal, does not change the payload, and does not change
  the digest.
- **Expected outputs, stated for the builder:**
  - intake (first): intake record + `duplicate: false`.
  - intake (duplicate): duplicate response above, no new record.
  - propose (first): proposal payload + digest + `new_proposal_created: true`.
  - propose (repeat): same proposal + digest + `already_exists: true`.
  - correction: new intake record (see §4.4) + `duplicate: false`.
  - decide (valid): decision record, §2.3.
  - decide (stale): `REJECTED_STALE`, no decision, event only.
  - decide (hostile text only, no command): no decision at all.

### 4.4 Correction — new record, explicit link, old record unchanged

- A correction is a **new** intake record for the corrected
  bytes, with `supersedes: <old intake_id>` and a link
  `link: "supersedes"`. Its `intake_id` is computed from the
  new bytes under §4.1, so it differs from the old id.
- The old record is **not edited**: no `superseded_by` field
  is written into it. A view may compute "superseded" by
  scanning for records whose `supersedes` equals the old id,
  but that computation is view-only and does not change the
  old record.
- A correction does not automatically create a proposal.
  `propose` for the corrected intake creates its own proposal
  (`PROP-` + new intake_id), bound to the new intake.

## 5. Baseline, statements, and input bytes (BRI04 + BRI05)

### 5.1 Baseline schema — six typed fields, null until supplied

```json
{
  "baseline": {
    "redacted_example": null,
    "frequency_per_week": null,
    "manual_time_minutes": null,
    "manual_steps": null,
    "errors_per_occurrence": null,
    "desired_result": null
  },
  "baseline_provenance": {
    "redacted_example": {"source": null, "supplied_utc": null, "note": null},
    "frequency_per_week": {"source": null, "supplied_utc": null, "note": null},
    "manual_time_minutes": {"source": null, "supplied_utc": null, "note": null},
    "manual_steps": {"source": null, "supplied_utc": null, "note": null},
    "errors_per_occurrence": {"source": null, "supplied_utc": null, "note": null},
    "desired_result": {"source": null, "supplied_utc": null, "note": null}
  }
}
```

- Types: `redacted_example` and `desired_result` are
  string-or-null; the other four are number-or-null.
  A non-null value must have provenance `source: "owner"`,
  a `supplied_utc`, and a note stating how it was supplied.
  A null value must have provenance source null. No value
  may be estimated by Muse, and no number may be filled in
  on the owner's behalf.
- **Owner-stated goal vs. acceptance threshold:** the
  owner's stated goal (in `owner_statements`) is a claim
  about what the owner wants, not a measured threshold.
  `desired_result` is the owner's stated desired outcome
  (string, or null if not stated). A threshold that could be
  tested (e.g. "manual time below X minutes") does not exist
  until the owner supplies a measured baseline **and** a
  desired result; until then, both are unknown, and no
  efficiency claim may be made.

### 5.2 Owner statements — renamed, not upgraded to facts

- REV1 used `owner_facts`. That name is **superseded** in
  REV2 because it implied verified facts. REV2 uses
  **`owner_statements`**: statements the owner made, quoted
  verbatim, **not** verified facts.
- Rule: `owner_statements` = the non-empty lines of
  `original_text`, verbatim, in order, without line endings.
  Empty lines are omitted from this list only; `original_text`
  itself is unchanged. This rule is deterministic and does
  not add interpretation.
- `proposed_interpretations` in an intake record starts as
  `[]`. Interpretations, if any, appear only in the proposal's
  `notes`, labelled as proposals, never as intake facts.

### 5.3 Collection template for one redacted workflow (no numbers filled in)

The owner is asked to supply, for **one** workflow, with
redaction (no secrets, no credentials, no real user data,
names replaced by placeholders):

1. Redacted example: the workflow steps, with sensitive
   details removed, as text.
2. Frequency: occurrences per week (number).
3. Manual time: minutes per occurrence, measured by the owner
   (number, not estimated).
4. Manual steps: steps per occurrence (number).
5. Errors: errors per occurrence, as observed by the owner
   (number, or 0 if none observed — only if the owner says so).
6. Desired result: what the owner wants instead, as text.

A synthetic example of the **format** (not real data) is in
`fixtures/intake-rev2/collection-template.md`. It contains
no real workflow, no real numbers, and must not be quoted as
owner data.

### 5.4 Input bytes — caps, encoding, and boundaries (BRI05)

- **Read as bytes first.** For a file, read the file bytes.
  For stdin, read `sys.stdin.buffer`. Apply the byte cap
  **before** decoding.
- **Byte cap:** 20,000 bytes per request. Over 20,000 bytes:
  reject, no intake record, nonzero exit, reason
  `byte_cap_exceeded`. Exactly 20,000 bytes: accepted (if all
  other rules pass).
- **Decode:** strict UTF-8 (`errors="strict"`). Invalid
  UTF-8: reject, no record, reason `invalid_utf8`.
- **BOM:** a leading UTF-8 BOM (`EF BB BF`) is **rejected**,
  reason `bom_not_accepted`. BOM is not stripped, because
  stripping would make `original_text` differ from
  `original_bytes` without a clear rule. The owner must
  resubmit without BOM.
- **Line endings:** LF, CRLF, and mixed line endings are
  all **accepted** and **preserved verbatim** in
  `original_text` and in `original_sha256`. No newline
  normalization is applied to intake content. (This is
  different from the T3 runner, which normalizes only an
  in-memory copy for parsing test logs; intake content is
  never normalized.)
- **Unicode combining:** preserved as-is. No NFC, NFKC, or
  other Unicode normalization. No trimming of accepted
  content: leading/trailing whitespace in an accepted request
  is preserved verbatim.
- **Character cap:** after decoding, character count =
  `len(decoded_text)` in code points. Cap: 10,000 characters.
  Over 10,000: reject, reason `char_cap_exceeded`. Exactly
  10,000: accepted (if all other rules pass).
- **Whitespace-only:** if the decoded text, after stripping
  whitespace for this check only, is empty, reject, reason
  `whitespace_only`. This is a rejection rule, not a
  modification: accepted content is never trimmed.
- **NUL / binary:** if the decoded text contains U+0000,
  reject, reason `nul_or_binary`. (Invalid UTF-8 already
  rejects most binary input; NUL is the explicit remaining
  case.)
- **Hash:** `original_sha256 = SHA-256(original_bytes)`.
  The hash is over bytes, not over a normalized or trimmed
  text. `original_length_bytes` and `original_length_chars`
  are both recorded, so a byte/char distinction is visible.
- **Source locator:** for a file, `local-file:<path as given,
  inside the current working directory>`; for stdin, `stdin`.
  Path rules from C4 still apply: inside cwd, not a symlink,
  not under `.git`, secret-like filenames refused, binary
  input refused (see matrix A15).
- **Immutable original:** `original_text` and
  `original_sha256` are stored verbatim and never edited.
  A correction is a new record (§4.4), never an edit.

## 6. Golden fixtures

`fixtures/intake-rev2/` contains the schema, one synthetic
example request, and the expected intake, proposal, proposal
view, duplicate response, propose-repeat response, decision,
and negative decision for that example, plus boundary fixtures
for the input-byte rules. All golden examples use a fixed
synthetic timestamp `2026-10-25T00:00:00Z` and are labelled
synthetic; that timestamp is not a real run time and is not
part of any identity or digest. The fixture manifest lists
every fixture file with its SHA-256. The static check in
`fixtures/intake-rev2/check_static.py` validates JSON parsing,
schema fields, hash/digest recomputation, and golden
consistency; it is a static check, not an application test
suite, and its output must not be described as app tests.

## 7. What this brief does NOT do

- It does not implement, enable, or authorize any product
  feature, provider, worker, listener, auth server, scheduler,
  browser, or network access.
- It does not change `control_room/`, `tests/test_control_room.py`,
  T3 scripts, C4 code, T3 tooling, or any old evidence or source pin.
- It does not merge, open a PR, change main, or change
  Orchestrator_Reverse.
- It does not claim the whole system is VERIFIED, secure,
  production-ready, or valuable. Those claims remain unproven
  until the evidence for them exists.
- It does not claim runtime knowledge retrieval, live-agent
  coordination, or owner authentication. None of those exist
  in this slice.

## 8. Approval block (to be filled by a real owner instruction only)

- Brief revision: `PRODUCT_INTAKE_BRIEF_REV2`
- Owner decision: _[not yet made — PENDING]_
- Owner reason: _[not yet made]_
- Source / actor / time / scope of the instruction: _[not yet made]_
- Scope authorized by approval (if any): _[only the local scope
  stated in this brief, if the owner writes it here]_
