# Addendum to MUSE_KNOWLEDGE_RECEIPT.md — revision 4

This addendum records that no new knowledge was read or ingested
for revision 4. G01 is a code defect in the audit chain, not a
knowledge defect, and its repair does not change any source pin.

What changed in Rev4, in brief:

- `verify_history()` now compares an empty-event store against
  the complete pristine genesis in canonical form, including
  project configuration, instead of checking only that lists are
  empty. Privileged mutations and proof evaluation remain blocked
  on an invalid chain, as in Rev3.
- The Windows runner and guide were repaired separately (tooling
  revision after T): separate code/tooling roots, fail-closed
  source preflight against a pinned manifest, unique run
  directories, ordered merged streams, authoritative count
  validation, and exact exit propagation (child/helper/BAT).
- A short local pilot runbook (`PILOT_RUNBOOK.md`) states the
  honest CLI-only entry point: no chat listener, no live-agent
  dispatcher, live adapters BLOCKED.

What stays valid:

- Source repository `Nohfinl99/Orchestrator_Reverse`, revision
  `ede6f66d907f06290749992d864424b82254e28e`, read read-only in
  the original work; no new reading was needed for Rev4.
- All ten file byte counts and SHA-256 values in the original
  receipt remain as recorded. A hash proves byte identity only,
  not rights, correctness, reading comprehension, or runtime
  admission.
- Status remains candidate reference only: no runtime KB admission,
  no consumer ACK, no execution authority from the v2 manifest.
