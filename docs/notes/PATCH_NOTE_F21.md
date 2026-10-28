# Patch Note F21 — checker fix for REV2.1 (short note, not a design rewrite)

**Packet base:** REV2.1 commit `0441decffd456ab1582375b353fd51d5b25b05c0`.
**Reviewer source (read, not merged):** branch
`codex/intake-rev2-1-review`, commit
`77909b1b48b635836e80c12dbcb8a6e6ff1966ee`.
Instruction `MUSE_AFTER_REV2_1_REVIEW.md` SHA-256
`6f3349438a2c819cd9c13d6124b88871e1bbdb63dfe3a8ced24c29c804c323c3`.
Report `reviews/2026-10-25-intake-rev2-1/REPORT.md` SHA-256
`088cafcd6773b60e8598b3681a4282286b43fb7ea4b8e77eede040baa0f098a7`.
Candidate patch
`reviews/2026-10-25-intake-rev2-1/candidate/checker-candidate.patch`
SHA-256
`9f8eeed67048f0013ab2bcda73d36bc7ebc59040b63caef248fd41cbcde212d4`.
Reviewer verdict: `CONTRACT_READY_CHECKER_FIX_REQUIRED`.
Overall system: NOT_VERIFIED. Owner build authorization: PENDING.

## Patch application — verified, not cherry-picked

The candidate patch was applied exactly to
`fixtures/intake-rev2/check_static.py` (no reviewer branch was
merged, no other reviewer file was copied into Muse's branch).
Immediately after applying the patch and before any other change,
the patched checker SHA-256 was
`8c6033dd70ec2f79b3d35ae7f8e13dcb9aeb6caceb55abefe2d40cf8c062d004`,
which matches the reviewer-reported candidate checker SHA-256
exactly. After that verification, one regression-harness addition
was made (the `--schema-probes` mode, §V21-02 below), which
changed the checker SHA-256 to
`f7abfa28cba156b163661d4946260baf3dcf114fd4094c5b5bbc087e06a6f806`.
The patch logic itself was not altered by that addition.

## What the patch fixes

| Finding | Fix applied | Artifact | Check in F21 evidence |
|---|---|---|---|
| V21-01 (P2) manifest path on Windows | Logical manifest paths now use `.as_posix()`; raw fixture bytes unchanged. The original Windows positive result (71 PASS / 1 FAIL / exit 1) is **preserved as history and not rewritten as PASS**. | `fixtures/intake-rev2/check_static.py` (patched line) | Positive bundle manifest check passes on Linux; Windows rerun of the final Muse revision is still requested from a reviewer (see Windows provenance below). |
| V21-02 (P2) schema selectors and $ref siblings | `check_unsupported` now recurses into `intake_schema`, `proposal_schema`, and `decision_schema`, and rejects any schema with `$ref` plus sibling constraints. No validation was loosened and no keyword was whitelisted to force a pass. | `fixtures/intake-rev2/check_static.py` (patched function) + `fixtures/intake-rev2/regression-schema-probes.json` (stored probes) + `--schema-probes` mode | Schema probes: 4/4 rejected, exit 0 (`evidence/rev2-1-f21/schema-probes.log`). |
| V21-03 (P2) decision identity in every mode | One `cross_decision` function is now used for both the positive bundle and `--validate`: it compares proposal_id, proposal_digest, brief_revision, and intake_id against the reviewed proposal, and recomputes decision_id. Wrong proposal_id or wrong decision_id is rejected in either mode. | `fixtures/intake-rev2/check_static.py` (new `cross_decision`) + `fixtures/intake-rev2/negative/decision-wrong-proposal-id.json` + `fixtures/intake-rev2/negative/decision-wrong-decision-id.json` | Negative suite: 13/13 rejected (11 previous + 2 new identity probes); per-fixture: 13 exits = 1. |

## Regression stored in the repo (not only on a reviewer copy)

- Negative fixtures (now 13): the 11 REV2.1 negatives plus the
  two V21-03 identity probes above.
- Schema probes (4): stored in
  `fixtures/intake-rev2/regression-schema-probes.json` and run
  by `python3 check_static.py --schema-probes` (in-memory
  injection of `minimum: 0` into each selector and into one
  definition property; each must be rejected).
- Manifest regenerated: 39 files (36 REV2.1 files + 2 new
  negative fixtures + 1 regression probes file), with bytes,
  SHA-256, and kind for every file. Unchanged golden files keep
  their REV2.1 hashes. Schema file is unchanged in F21.

## Windows provenance — stated separately, not claimed from Linux

- Original Muse REV2.1 checker on Windows (reviewer-run):
  71 PASS / 1 FAIL / exit 1, caused by V21-01 (backslash path
  comparison), not by a missing fixture. That result stands.
- Candidate patch on a reviewer copy on Windows:
  positive 72 PASS / exit 0, negatives 11/11 rejected, identity
  probes 2/2 rejected, schema probes 4/4 rejected (reviewer
  candidate evidence, not Muse's own Windows run).
- Muse F21 checker on Linux (this packet): positive 72 PASS /
  exit 0, negatives 13/13 rejected, schema probes 4/4 rejected.
  **Linux does not prove Windows.** A reviewer Windows rerun of
  the final F21 checker revision is requested; until it exists,
  do not describe F21 as Windows-verified.

## What did NOT change in F21

- Brief identity (`PRODUCT_INTAKE_BRIEF_REV2`), template
  (`INTAKE_TEMPLATE_V1`), golden payloads, schema content,
  `control_room/`, product tests, T3 tooling, `ROADMAP_STATUS.md`,
  brief REV2, addendum REV2.1, matrix REV2, checklist C5, and all
  old evidence (REV2, REV2.1, Windows C4/T3, E4, tooling T3).
- No design rewrite, no new product scope, no provider,
  listener, worker, scheduler, browser, or network.
- No merge, no PR, no main change, no Orchestrator_Reverse change.

## Remaining gaps after F21

- R2-02 is closed only within the probes now stored (13 negatives
  + 4 schema probes). The checker is still a subset validator,
  not a full JSON Schema engine and not an application test suite.
- Application acceptance A01–A33 remains PROPOSED / NOT_RUN.
- C5 build remains **PENDING** until the owner gives a clear
  build authorization for the exact packet scope, recorded by
  source, actor, time, and scope, with exact packet commit +
  addendum/checklist hashes + checker fix revision. A review
  request and a reviewer verdict are not that authorization.
