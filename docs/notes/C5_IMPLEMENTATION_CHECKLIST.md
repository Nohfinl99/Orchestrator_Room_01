# C5 Implementation Checklist — spec ready for build, NOT executed

**Purpose:** This checklist is the build specification for the
thin local intake slice, prepared so the owner can approve a
concrete packet before any code is written. **Nothing in this
checklist has been implemented, run, or tested as an application.**
All runtime cases below remain **PROPOSED / NOT_RUN**.

**Gate before build:** Owner approval of packet REV2.1 scope
(addendum + this checklist), recorded by source, actor, time,
and scope. Without that approval, the build stays BLOCKED.
After approval, the build is a **separate code commit C5** and
a **separate evidence commit E5**, reviewed by an independent
reviewer on a frozen snapshot. This checklist is not a build,
not a merge, and not an approval.

**Binding revision for this checklist:** Packet REV2.1
(addendum to brief `PRODUCT_INTAKE_BRIEF_REV2`; identity domain
unchanged, see addendum §1). Template `INTAKE_TEMPLATE_V1`.
Decision ingress: CLI required `--expected-*` flags (addendum §2).

**Reuse from C4 (do not reinvent):** whole-store CAS atomic
saves, OS lock file (never unlinked, fcntl POSIX / msvcrt
Windows), audit history anchored to current state with
genesis check, size/input limits, path rules (inside cwd, no
symlink, no `.git`, secret-like filenames refused), backend-owned
stage machine, and binding-vs-implementation separation
(implementation verification stays NOT_VERIFIED in simulation).

## Build steps (in order, each with its evidence)

### Step 1 — Intake: file/stdin binary bounded → immutable store record

- **Input:** local UTF-8 file path inside cwd, or `sys.stdin.buffer`.
  Read as bytes first. Byte cap 20,000 **before** decode.
  Strict UTF-8 decode. BOM rejected (not stripped). NUL rejected.
  Whitespace-only rejected. Char cap 10,000 code points.
  LF/CRLF/mixed/bare-CR/none classified per addendum §4.1 and
  preserved verbatim; derived statements split on breaks only.
- **Proposed commands (not implemented):**
  ```sh
  python3 -m control_room intake --input request.txt --store room.json
  python3 -m control_room intake --stdin --store room.json < request.txt
  ```
- **Output:** immutable intake record per REV2 schema (§5),
  with `intake_id` from bytes + brief + template domain,
  `original_sha256` over original bytes, both lengths, locator,
  `owner_statements` (derived, not verified facts), `baseline`
  (six fields, null until owner supplies, with provenance),
  `duplicate_of: null`, `supersedes: null` (or old id for a
  valid correction).
- **Evidence to collect per run:** command, exit code, raw
  stdout/stderr, store hash before/after, intake record JSON,
  fixture file + SHA-256.
- **Failure modes:** over byte/char cap, invalid UTF-8, BOM,
  NUL, whitespace-only, path outside cwd / symlink / `.git` /
  secret-like filename → reject, nonzero exit, **no** record.

### Step 2 — Dedupe and correction (same step, separate paths)

- **Duplicate:** same bytes + same brief/template → duplicate
  response only (no new record, no new proposal), plus a
  separate `duplicate_submission` history event. Original record
  unchanged.
- **Valid correction:** new bytes, not already in store,
  `supersedes` = existing intake_id → new record, new id, old
  record unchanged.
- **No-op correction:** same bytes as original, supersedes =
  original → reject `correction_no_op_same_bytes`, nonzero exit,
  no record, event `correction_rejected_no_op`.
- **Conflict correction:** bytes already exist, supersedes
  points elsewhere → reject `correction_conflict_existing_id`,
  nonzero exit, no record, no overwrite, event
  `correction_rejected_conflict`.
- **Supersedes not found:** reject `correction_supersedes_not_found`.

### Step 3 — Propose: fixed template → immutable proposal + computed view

- **Proposed command (not implemented):**
  ```sh
  python3 -m control_room propose --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx
  ```
- **Output:** exactly four template tasks (capture, separate,
  discovery proposal, owner review) with fixed roles,
  dependencies, and reasons; `proposal_id = "PROP-" + intake_id`;
  `proposal_digest` = SHA-256 of canonical JSON payload
  (sorted keys, `(",", ":")`, UTF-8), excluding digest itself,
  timestamps, view, and decision fields.
- **Repeat propose:** same proposal, same digest,
  `already_exists: true`, no second proposal.
- **View (computed at overview, not stored in payload):**
  `readiness`, `blocked_reason`, `next_allowed_action` per task.
  View changes do not change payload or digest.
- **Proposed command (not implemented):**
  ```sh
  python3 -m control_room overview --store room.json
  ```

### Step 4 — Decide: expected bindings from the operator-reviewed snapshot

- **Proposed command (not implemented):** see addendum §2.1
  for the exact positive command and §2.2 for the exact stale
  command. Required flags: `--proposal-id`,
  `--expected-proposal-digest`, `--expected-brief-revision`,
  `--expected-intake-id`, `--decision`, `--reason`,
  `--operator`, `--source`.
- **Comparison rule:** operator-supplied expected bindings vs.
  current proposal payload (digest recomputed from current
  canonical payload) **inside the same CAS/lock transaction**
  as the decision write. Mismatch → `REJECTED_STALE`, no
  decision, separate event. Missing/wrong-format expected
  binding → reject, no decision, no default approval.
- **Provenance:** `OPERATOR_ASSERTED` only. This is not owner
  authentication, and a local gate decision is not owner
  product acceptance.

### Step 5 — Audit and reload

- Every intake, duplicate, propose, correction, decision, and
  rejection is recorded as a history event with before/after
  digests and revision continuity, reusing the C4 history
  pattern. No event edits an immutable record.
- Reload in a new process must show the same project, intake,
  proposal, and history, with the same hashes. A changed brief
  revision invalidates prior approvals bound to the old revision.
- Task DONE does not advance product or verification state.
  Proposal creation does not pass anything. No provider,
  worker, listener, scheduler, browser, or network is added
  in C5. Live-agent coordination is out of scope.

## Acceptance A01–A33 — binding revision, fixture, expected output, command (all PROPOSED / NOT_RUN)

Each case below must be run in C5 with its fixture, exact
command, environment, raw output/log, exit code, and artifact
hash recorded before it can be called PASS. Until then, every
case is PROPOSED / NOT_RUN, regardless of the static checker
results in this packet.

| # | Case (REV2 name) | Fixture / expected (REV2.1 bundle) | Expected output in C5 | Proposed command (not implemented) |
|---|---|---|---|---|
| A01 | Unicode Vietnamese preserved | `example-request.txt` / `expected-intake.json` | Verbatim text + original SHA preserved | `intake --input example-request.txt` |
| A02 | Empty input rejected | Empty file | No record, nonzero exit, `empty_input` | `intake --input empty.txt` |
| A03 | Oversized rejected | Byte/char cap files (A23/A25) | No record, nonzero exit, cap reason | `intake --input <over-cap file>` |
| A04 | Bad encoding rejected | Invalid UTF-8 file | No replacement, no record, `invalid_utf8` | `intake --input <bad-utf8 file>` |
| A05 | Baseline six fields, null + provenance | `expected-intake.json` | Exactly six null fields, provenance source null | `intake` + inspect record |
| A06 | Duplicate, metadata in response/event only | Same bytes twice / `expected-duplicate-response.json` | Duplicate response, intake count 1, original unchanged | `intake` twice, same file |
| A07 | Statements / interpretations separated | `expected-intake.json` + proposal notes | `owner_statements` vs. proposal `notes` separate | `intake`, `propose`, `overview` |
| A08 | Hostile text inert — set PASS | Hostile request text | Data only, no stage advance, no PASS | `intake` with hostile text |
| A09 | Hostile text inert — forged approval | Pasted approval in request | No decision, gate pending | `intake` with pasted approval |
| A10 | Hostile text inert — upload/send | Upload/send text in request | No network/upload/message | `intake` with upload text |
| A11 | Proposal dependency view | `expected-proposal-view.json` | Dependencies, readiness, blocked reason, next action | `overview` |
| A12 | Restart / reload coherent | Intake + proposal, reload | Same hashes, coherent history | `overview` in new process |
| A13 | Changed brief invalidates approval | Approval bound to REV2, brief changed | Prior approval no longer authorizes new scope | `decide` after brief change |
| A14 | No auto-PASS | Task DONE / proposal created | Product/verification unchanged | Task DONE, then `overview` |
| A15 | Path / binary / symlink refused | Outside-cwd / symlink / `.git` / binary / secret-like path | Rejected, no record, nonzero exit | `intake --input <bad path>` |
| A16 | Deterministic proposal | Same intake + same brief/template, twice | Identical payload + digest | `propose` twice |
| A17 | Gate only, OPERATOR_ASSERTED | Simulated role argument claiming approval | Gate pending; only `decide` with matching expected bindings approves; provenance OPERATOR_ASSERTED | Simulated role argument, then `decide` |
| A18 | Immutable intake | Correction (valid) | New record, old unchanged | `intake` correction |
| A19 | Golden template — fixed four tasks | `expected-proposal.json` | Exactly four template tasks, digest matches | `propose` for golden intake |
| A20 | Stale decision rejected | Addendum §2.2 command / `negative-decision.json` | `REJECTED_STALE`, nonzero exit, no decision, event | `decide` with old/wrong expected digest |
| A21 | Decision binding — brief/intake mismatch | Wrong expected brief/intake in `decide` | Rejected, no decision, nonzero exit | `decide` with wrong expected brief/intake |
| A22 | Knowledge / Soul / Heart honesty | Brief REV2 §3.4 + addendum §1 | No Reverse card cited as authority; Soul changes no task/role/decision; Heart events are history only; no runtime retrieval or live-agent claim | Inspect brief/template output |
| A23 | Byte cap boundary | 20,000 bytes accepted; 20,001 rejected (`request-byte-cap-over.txt`) | Byte cap before decode, `byte_cap_exceeded` for over | `intake` with boundary files |
| A24 | Whitespace-only rejected | `request-whitespace.txt` | Rejected, `whitespace_only`, no record; accepted content never trimmed | `intake --input request-whitespace.txt` |
| A25 | Char cap boundary | `request-char-cap-ok.txt` (10,000) / `request-char-cap-over.txt` (10,001) | Exactly 10,000 accepted, 10,001 rejected `char_cap_exceeded` | `intake` with boundary files |
| A26 | BOM rejected, not stripped | `request-bom.json` (base64 input) | Rejected, `bom_not_accepted`, no record | `intake` with BOM input |
| A27 | NUL rejected | `request-nul.json` (base64 input) | Rejected, `nul_or_binary`, no record | `intake` with NUL input |
| A28 | CRLF preserved, not normalized | `request-crlf.txt` / `expected-line-endings.json` | CRLF verbatim, hash differs from LF, `line_endings=CRLF` | `intake --input request-crlf.txt` |
| A29 | Unicode combining preserved | Combining-character request | Verbatim, no NFC/NFKC, hash over original bytes | `intake` with combining text |
| A30 | Propose repeat idempotent | `expected-propose-repeat-response.json` | First creates one, repeat returns same + `already_exists: true` | `propose` twice |
| A31 | Correction creates new record, old unchanged | `expected-correction.json` / `correction-request.txt` | New id, `supersedes` = old id, old hash unchanged | `intake` correction (valid) |
| A32 | Proposal view separate from payload | Payload change vs. view recompute | View change does not change digest; payload change does and invalidates bound decisions | `overview` before/after task DONE; `decide` after payload change |
| A33 | Owner acceptance recorded, not assumed | No clear owner instruction | Acceptance = PENDING; meeting/review/reviewer verdict not recorded as acceptance | Inspect approval block (empty) |

## C5 commit and evidence discipline (for the future build, not this packet)

- **Code commit C5** (separate): only `control_room/` changes
  needed for Steps 1–5, plus C5 tests. No provider, worker,
  listener, scheduler, browser, or network in C5.
- **Evidence commit E5** (separate): raw logs, manifests,
  store hashes before/after, and per-case A01–A33 results with
  exact commands, OS/Python, and exits. C5 logs must not reuse
  C4/E4, REV2, or REV2.1 static-check logs as application evidence.
- **Reviewer:** independent reviewer on a frozen C5 snapshot
  (code + evidence pins named separately), with its own verdict.
  A reviewer verdict is not owner acceptance.
- **Stop conditions:** if owner approval for REV2.1 is not
  recorded, stop. If any A-case fails in C5, do not claim PASS
  for that case, do not average failures away, and do not merge.
- **No merge / no PR** is authorized by this checklist.
  Main and Orchestrator_Reverse are unchanged by this packet
  and must remain unchanged by C5 unless the owner separately
  authorizes a merge for a specific commit.
