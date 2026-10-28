# Provenance — CTX-001-PACKET-02 (review-safe)

## Source reconciliation mapping (GATE01)

Reused input: 504 bytes, 406 chars, SHA-256
`2bf4740b8e478ecae833171bb3a8acedce3562b089d065416c9c5618b9dd8907`.
Provenance of the source itself: owner direct Muse chat message 2026-10-26 01:31:05 +07;
owner did NOT send a file — the file was created per owner instruction step 2;
permission for the agreed local trial is recorded in attempt-01 provenance.
Template/synthetic preparation files were NOT used.

| Field | Source span (chars, 0-based, end-exclusive) | Span SHA-256 |
|---|---|---|
| goal (tracking) | 110–234 | `aff75fe3b991f23402d0abc2981ccfa8b750a6191d2d74b275dc2af884e1ef9d` |
| scope (local trial) | 236–325 | `aa5721f487881e1cca0977bbf10a8494b5a22e37ea4a25a5c033bc480b745c36` |
| desired_output (observability) | 326–405 | `bfc4c1d32525eab64e3dbbba97389dd1356775803b3ec85c961f7faf548eb5e9` |
| context (relay workflow) | 0–110 (first part of paragraph 1) | covered by whole-input hash |

## Reused answers — exact labelling

- Clarification `CTXQ-4723da2edd3488b0` (2 assess questions verbatim).
- Answer 1 (goal question) = source span chars 110–234, span SHA above.
  Answer 2 (scope question) = source span chars 236–325, span SHA above.
- Label: **REUSED_PRIOR_OWNER_STATEMENT** for both.
- Original source time: 2026-10-26 01:31:05 +07.
- CLI ledger record time (`answered_utc`): 2026-10-26T12:55:13Z.
  That timestamp is when the executor recorded the reused statements into the
  CLI ledger; it is NOT the time the owner answered, NOT a new human exchange,
  NOT new consent, NOT approval.
- Executor: Muse (operator-assisted source reconciliation, per GATE01 step 3).
- No ctx-add-source was executed: the draft record has `source_ids: []`.
  Source mapping lives in this ledger, not as a falsely fetched CLI field.
  The app's locator-only provenance is kept honest: no claim of fetched or
  admitted knowledge is made from the CLI record.

## What this packet does NOT claim

- No `ctx-review-rewrite`, no `ctx-propose`: review_status is
  DRAFT_NOT_REVIEWED, proposal NONE.
- No owner decision: the real owner decision on digest
  `74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`
  is still pending (channel owner gate version 1, preserved).
- Previous C5 approval and test approvals do not authorize this rewrite.
- No raw owner request text and no full raw store are uploaded in this packet.
