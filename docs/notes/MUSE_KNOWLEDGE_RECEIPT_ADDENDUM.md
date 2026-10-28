# Addendum to MUSE_KNOWLEDGE_RECEIPT.md — revision 2

This addendum corrects application claims from the first slice that
the independent review of 1bba803 invalidated. It does not edit the
original receipt, and it does not change its ten source pins.

## What stays valid

- Source repository `Nohfinl99/Orchestrator_Reverse`, revision
  `ede6f66d907f06290749992d864424b82254e28e`, read read-only.
- All ten file byte counts and SHA-256 values in the original receipt
  remain as recorded; the reviewer confirmed they match the pinned
  public checkout. A hash proves byte identity only, not rights,
  correctness, reading comprehension, or runtime admission.
- Status remains candidate reference only: no runtime KB admission,
  no consumer ACK, no execution authority from the v2 manifest.
- The old Agent Office roadmap, AO phases, fixtures, gates, and six
  identities were not transplanted into Orchestrator-Room code.

## What was invalidated, and what changed in revision 2

- Original claim, in effect: evidence records with a present exit
  code, hash, and differing reviewer/collector strings could yield
  PASS, and the test oracle T10 encoded that as expected behaviour.
  Review finding F01 showed this allows invented evidence and nonzero
  exits to produce PASS. Corrected in revision 2: evidence is a
  proposal only; `verify()` requires a frozen required-case plan,
  complete records, exit code 0, command, environment, criteria
  revision ACCEPTANCE-REV2-1, scope completion, a timestamp, artifact
  bytes that actually match the claimed hash, and a judge review
  receipt whose digest still matches the covered records. T10 was
  rewritten as a negative-control oracle: forged, nonzero-exit,
  missing-artifact, altered-artifact, missing-case, and unreviewed
  records never yield PASS.
- Original claim, in effect: existence of an observation, inference,
  and judge report could satisfy product gates. Review finding F02
  showed empty and stale artifacts could reach OWNER_ACCEPTED.
  Corrected in revision 2: gates require ready observations, reviewed
  inferences, an approved brief with still-matching linked content,
  and an owner decision naming a judge report whose snapshot content
  still matches current project content, with findings and per-case
  results present. Stale decisions are rejected and recorded, with
  the stage unchanged.
- Original claim, in effect: role arguments enforced authority.
  Review finding F03 showed a caller could self-assert owner. Corrected
  in revision 2: role arguments are labelled simulation only in every
  privileged output and in the docs; live adapters stay blocked; no
  token scheme is claimed to protect a same-user process with storage
  access.
- Original persistence and audit claims were overstated (findings
  F04–F06). Corrected in revision 2: whole-store compare-and-swap
  with atomic replacement and truthful failure reporting; aggregate
  size and list limits validated before any write; finite nonnegative
  time; UTC timestamps, content digests, and a hash chain on audit
  events, with the explicit limit that the chain is not tamper-proof
  against the storage owner.
- Original RUN_REPORT.md treated a missing timestamp as a possible
  future requirement while still labelling AC8 PASS, and treated
  static string checks as establishing no network egress. Both are
  corrected in RUN_REPORT_REV2.md: AC8 is now judged on the actual
  timestamp/digest implementation, AC14 packet capture remains
  NOT_RUN, and missing mandatory subcriteria keep a criterion
  incomplete rather than PASS.

No new knowledge was read for this addendum, and no file in
Orchestrator_Reverse was changed, read again for admission, or
executed. The ten pins above are the only knowledge provenance this
addendum relies on.
