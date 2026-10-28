# Addendum to MUSE_KNOWLEDGE_RECEIPT.md — revision 3

This addendum corrects Rev2 application claims that the independent
review of Rev2 invalidated. It does not edit the original receipt or
the Rev2 addendum, and it does not change the ten source pins. No new
knowledge was read or ingested for this repair; the defects are code
defects, not knowledge defects.

## What was corrected from Rev2

- Rev2 claim, in effect: a complete, bound, reviewed evidence set
  could yield `verification: PASS` (labelled mechanism-only).
  Review finding B02 showed this still reads as implementation
  verification, even though the inputs are caller-supplied strings
  and a simulated receipt. Corrected in Rev3: `verify()` returns
  `binding_checks` / `mechanism_result` separately from
  `implementation_verification`, which is always `NOT_VERIFIED` in
  this simulation, and the top-level `verification` field is never
  PASS. Positive synthetic tests assert binding checks only.
- Rev2 claim, in effect: the required plan was frozen. Review
  finding B01 showed the public `required_cases` parameter could
  override it with an empty plan and still yield PASS. Corrected in
  Rev3: any override must match the frozen plan id
  `CONTROL_ROOM_VERIFICATION_PLAN`, revision `REV3-1`, digest, and
  exact case list, or it is rejected before evidence is checked.
- Rev2 claim, in effect: brief approval was bound by a digest.
  Review finding B03 showed the digest was recomputed from a cached
  field, not actual content, and that orphan/whitespace briefs could
  pass. Corrected in Rev3: digests are recomputed from actual
  canonical fields, and acceptance requires a nonempty coherent
  graph (ready observations, reviewed inferences linked to those
  observations, non-blank content).
- Rev2 claim, in effect: the audit chain was validated. Review
  finding B04 showed it was not anchored to current state. Corrected
  in Rev3: `verify_history()` checks schema, genesis, revision
  sequence, and the final event's stage, revision, and content
  digest against the current store, and privileged mutations and
  proof evaluation are blocked on an invalid chain.
- Rev2 claim, in effect: locking was safe. Review finding B05
  showed an abrupt Windows death could leave an O_EXCL lock file
  blocking later writes, and the POSIX unlink created an inode race.
  Corrected in Rev3: a stable lock file that is never unlinked,
  with fcntl flock on POSIX and msvcrt locking on Windows, both
  released by the OS on process death. No lock is stolen by PID/time.
- Rev2 test claim, in effect: T12 tested boundaries on Windows.
  Review finding B06 showed Windows rejected the huge subprocess
  command line before the app ran. Corrected in Rev3: boundaries
  and true aggregate overflow are tested in-process, CLI subprocess
  checks use small arguments only, and the OS environment is
  preserved for child Python processes.

## What stays valid

- Source repository `Nohfinl99/Orchestrator_Reverse`, revision
  `ede6f66d907f06290749992d864424b82254e28e`, read read-only in
  the original work; no new reading was needed for Rev3.
- All ten file byte counts and SHA-256 values in the original receipt
  remain as recorded. A hash proves byte identity only, not rights,
  correctness, reading comprehension, or runtime admission.
- Status remains candidate reference only: no runtime KB admission,
  no consumer ACK, no execution authority from the v2 manifest.
