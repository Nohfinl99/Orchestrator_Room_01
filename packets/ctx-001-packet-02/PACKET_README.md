# CTX-001-PACKET-02 — inspectable pre-decision packet (attempt-02)

Packet for Codex precheck REV-CTX-001-PACKET02-PRECHECK. Prepared by Muse
(operator-assisted packaging) from the already-created local attempt-02 store.
No code, evidence, raw, manifest, or rewrite/digest was changed by packaging.

## Files

- `REWRITE_DESCRIPTOR.json` — REFERENCE_FORM_NOT_HASH_PAYLOAD. All digest
  payload fields (literals for operator-authored fields; SHA+span references
  for protected literals) plus the exact digest algorithm and numbered
  reconstruction steps. Follow the steps to recompute digest
  `74cd5f5b72e0e01cbe96d08742a0335320dc2dbd1247134691a592b4e8919e97`.
- `ROOM_SNAPSHOT_REDACTED.json` — redacted transcript of the local room record.
  NOT raw bytes: protected literals replaced by references. All other fields
  are literal copies.
- `ROOM_SNAPSHOT_HASHES.json` — SHA-256/bytes of the actual raw local files
  retained locally (identity commitments; content not uploaded).
- `PROVENANCE.md` — review-safe provenance of the reused answers.
- `COMMANDS.md` — command/exit metadata for every CLI step; no protected
  literals reproduced.
- `VERIFY_HISTORY.json` — verbatim safe verify-history output
  (chain_valid true, event_count 4, failures []).
- `MANIFEST.json` — self-excluding manifest of the files above.

## What can and cannot be checked from permitted material

- Digest recomputation: FULLY reproducible via the descriptor + the
  locally-held request (SHA `2bf4740b…`) + spans. Packager self-check passed
  before packaging.
- Intake/clarification binding: checkable from the descriptor bindings
  (intake `INTAKE-0d0bcbe75d4fbee1`, clarification `CTXQ-4723da2edd3488b0`).
- Full history chain recomputation: PARTIAL/UNVERIFIED from permitted material
  alone, because event/content digests cover protected text that is not
  uploaded. The raw room hash in ROOM_SNAPSHOT_HASHES.json commits the raw
  bytes; it does not substitute for content verification. No PASS is claimed
  for this check.
- Review/proposal: NONE. review_status DRAFT_NOT_REVIEWED. No
  ctx-review-rewrite or ctx-propose until a real owner decision bound to the
  presented digest. Owner gate version 1 is preserved, not filled.

## Frozen pins (unchanged by this packet)

- Code C6R1: `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255`
- Evidence E6R1: `ea9c9464b14eb93bf4efe6b00bf6ce73e59218e7`
- Docs (reviewed): `dfedb46e64d0a8af6777cf4b43acb8630251db27`
- Old attempt-01 store/DEC untouched (room.json still `a182794e…`).
- Whole system NOT_VERIFIED; product acceptance PENDING.
