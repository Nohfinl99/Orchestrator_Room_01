# Acceptance Matrix — Product Intake Brief REV2 (PROPOSED, NOT RUN)

**Bound to brief:** `PRODUCT_INTAKE_BRIEF_REV2`
**Supersedes (as a proposal, not as a code change):**
`PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1`. REV1 is preserved;
REV2 does not edit it.
**Status of every runtime case below:** PROPOSED / NOT_RUN.
No case is PASS, because the feature is not implemented and no
case has been executed. A case becomes PASS only when it is
executed against the approved brief revision, with a fixture,
exact command, environment, raw output/log, exit code, and
artifact hash recorded. Code inspection alone does not satisfy
a runtime case. The static check in
`fixtures/intake-rev2/check_static.py` validates golden
consistency only; it is **not** an application test suite and
must not be described as app tests.

**How to read status:** DONE = task completed (this matrix was
written); technical check = executed test (none yet for this
matrix); product evidence = owner trial measurement (none yet);
owner acceptance = owner approval of the brief revision (not yet
made). Do not collapse these four into one "verified" claim.

## Revised cases (REV1 wording corrected)

| # | Case | Input / fixture (proposed) | Expected behavior | Evidence to collect when run | Status |
|---|---|---|---|---|---|
| A05 | Preserved unknown baseline, six typed fields | Any valid intake, no owner-supplied baseline | Baseline object has exactly six fields, all null, each with provenance source null; no estimated time, no invented quote or metric | Intake record showing six nulls + provenance | PROPOSED |
| A06 | Duplicate / idempotency, metadata in response/event only | Same bytes submitted twice under same brief+template version | Second submission returns duplicate response (§4.2), no new intake record, no new proposal; original record unchanged (no `duplicate_of` written into it) | Two commands, both outputs, intake count = 1, proposal count = 0 from duplicate | PROPOSED |
| A17 | Gate only, OPERATOR_ASSERTED, not authenticated | Proposal awaiting review, with a simulated role argument claiming approval | Gate remains pending; simulated role does not approve; only a `decide` command by a local operator with matching digest approves; decision provenance is OPERATOR_ASSERTED, never AUTHENTICATED_OWNER | Gate state, history, role argument log, decision record | PROPOSED |

## Carried cases (REV1, unchanged in substance, re-bound to REV2)

| # | Case | Expected behavior | Status |
|---|---|---|---|
| A01 | Unicode Vietnamese input preserved | Intake stores verbatim text and SHA-256 of original bytes; overview shows it unchanged | PROPOSED |
| A02 | Empty input rejected | No intake record, nonzero exit, reason `empty_input` (empty = zero bytes; whitespace-only is A24) | PROPOSED |
| A03 | Oversized input rejected | Byte cap 20,000 and char cap 10,000 enforced (see A23–A25); no intake record, nonzero exit | PROPOSED |
| A04 | Bad encoding rejected | Invalid UTF-8: no replacement, no intake record, nonzero exit, reason `invalid_utf8` | PROPOSED |
| A07 | Statements / interpretations separated | Storage and display keep `owner_statements` (owner-stated claims, not verified facts) separate from proposal `notes` (labelled proposals) | PROPOSED |
| A08 | Hostile text inert — set PASS | Text stored as data only; no stage advance, no PASS, no VERIFIED | PROPOSED |
| A09 | Hostile text inert — forged approval | Pasted "owner approval" in request text is not a gate decision; gate remains pending | PROPOSED |
| A10 | Hostile text inert — upload/send | No network, no file upload, no external message; text stored as data only | PROPOSED |
| A11 | Proposal dependency view | Overview shows dependencies, ready/blocked state, blocked reason, next allowed action for each task; view is computed, not part of payload/digest | PROPOSED |
| A12 | Restart / reload coherent | Intake + proposal + history unchanged and coherent after reload in a new process | PROPOSED |
| A13 | Changed brief invalidates approval | Approval bound to REV2 no longer authorizes a changed brief revision; new approval required | PROPOSED |
| A14 | No auto-PASS | Task DONE, or proposal created, does not advance product/verification state | PROPOSED |
| A15 | Path / binary / symlink refused | Path outside cwd, symlink, `.git` path, binary file, secret-like filename: rejected, no intake record, nonzero exit | PROPOSED |
| A16 | Deterministic proposal | Same intake + same brief+template version, run twice: identical proposal payload and digest | PROPOSED |
| A18 | Immutable intake | Correction is a new record with `supersedes` link; original record unchanged | PROPOSED |

## New cases (REV2 — boundary, bytes, hash, stale, correction, golden template)

| # | Case | Input / fixture | Expected behavior | Evidence to collect when run | Status |
|---|---|---|---|---|---|
| A19 | Golden template — fixed four tasks | `fixtures/intake-rev2/example-request.txt` | Proposal is exactly the four template tasks in order, with fixed roles/dependencies/reasons; proposal digest matches `expected-proposal.json` | Command, proposal output, digest recomputation | PROPOSED |
| A20 | Stale decision rejected | `decide` with a proposal digest that does not match the current payload | Outcome `REJECTED_STALE`, nonzero exit, no decision created, `decision_attempt_rejected` event recorded | Command, exit code, event log, decision count = 0 | PROPOSED |
| A21 | Decision binding — brief/intake mismatch | `decide` with wrong brief revision or wrong intake_id | Rejected, no decision created, nonzero exit | Command, exit code, event log | PROPOSED |
| A22 | Knowledge / Soul / Heart honesty | Brief §3.4 and template output | No Orchestrator_Reverse card is cited as authority; Soul changes no task/role/decision; Heart events are history events only, not edits to immutable records; no runtime retrieval or live-agent coordination is claimed | Brief §3.4, template output, no retrieval log claimed | PROPOSED |
| A23 | Byte cap boundary | 20,000 bytes: accepted (if other rules pass); 20,001 bytes: rejected, reason `byte_cap_exceeded`, no record | Byte cap applied **before** decode | Fixture sizes, commands, exit codes | PROPOSED |
| A24 | Whitespace-only rejected | File with only spaces/tabs/newlines | Rejected, reason `whitespace_only`, no record; accepted content is never trimmed | Fixture, command, exit code | PROPOSED |
| A25 | Char cap boundary | Exactly 10,000 chars: accepted (if other rules pass); 10,001 chars: rejected, reason `char_cap_exceeded`, no record | Char count = code points after strict decode | Fixture sizes, commands, exit codes | PROPOSED |
| A26 | BOM rejected, not stripped | Input starting with EF BB BF | Rejected, reason `bom_not_accepted`, no record, no stripped intake | Fixture (base64 in `request-bom.json`), command, exit code | PROPOSED |
| A27 | NUL rejected | Input containing U+0000 | Rejected, reason `nul_or_binary`, no record | Fixture (base64 in `request-nul.json`), command, exit code | PROPOSED |
| A28 | CRLF preserved, not normalized | CRLF request with same lines as LF example | Intake stores CRLF verbatim; `original_sha256` differs from LF example; `line_endings` = `CRLF` | Both intake records, hashes, line_endings fields | PROPOSED |
| A29 | Unicode combining preserved, no normalization | Request with combining characters (e.g. base + combining mark) | Stored verbatim, no NFC/NFKC, hash over original bytes | Fixture bytes, intake record, hash recomputation | PROPOSED |
| A30 | Propose repeat idempotent | `propose` twice for same intake | First creates one proposal; second returns same proposal + digest with `already_exists: true`, no second proposal | Two commands, both outputs, proposal count = 1 | PROPOSED |
| A31 | Correction creates new record, old unchanged | Correction bytes for an existing intake | New intake with `supersedes` = old id, new intake_id, `duplicate: false`; old record byte-identical before/after | Old hash before/after, new record, link field | PROPOSED |
| A32 | Proposal view separate from payload | Proposal payload changed vs. view recomputed | Changing a task's DONE status changes the view (readiness/blocked/next action) but does **not** change proposal payload or digest; changing payload changes digest and invalidates bound decisions | Payload hash before/after, view before/after, decision state | PROPOSED |
| A33 | Owner acceptance recorded, not assumed | No clear owner instruction for REV2 | Owner acceptance = PENDING; meeting/review request/reviewer verdict are not recorded as acceptance | Approval block (empty), no acceptance record | PROPOSED |

**Negative controls that must not be relabelled:** A08, A09, A10,
A17, A20, A21, A26, A27 are negative controls. Their "pass"
would mean the hostile/stale/invalid input had no authority
effect — not that the hostile input succeeded. Record the
input verbatim in the fixture, and record that no authority,
stage, or verdict changed.
