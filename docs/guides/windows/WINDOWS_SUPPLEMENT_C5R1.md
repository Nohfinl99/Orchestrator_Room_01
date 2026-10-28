# Windows supplement C5R1 — reviewer-run evidence (Muse did not run Windows)

This supplement records reviewer-run Windows evidence for the
frozen C5R1 code. It adds docs/evidence only. It does not change
C5R1 code, E5R1 evidence, any fixture, any C4 test, main, or
Orchestrator_Reverse, and it does not rewrite any old FAIL
history. Muse's own runs are Linux only; every Windows result
below was run by the reviewer and is labelled as such.

## Source and provenance

- Reviewer branch: `codex/c5r1-owner-pilot`, commit
  `6a48b3f07bd67110b8c8b95768db712994e76499`
  ("Independent C5R1 Windows evidence and bounded owner-pilot
  handoff", 2026-10-25T18:04:35Z).
- Reviewer instruction: `MUSE_AFTER_C5R1_REVIEW.md` on that
  branch. Reviewer report: `reviews/2026-10-26-c5r1/REPORT.md`
  on that branch. Owner pilot protocol:
  `OWNER_PILOT_PROTOCOL.md` on that branch. Those three
  documents remain on the reviewer branch; they are not copied
  into this supplement, which carries only the raw Windows
  evidence files listed below.
- Reviewer verdict: READY_FOR_BOUNDED_OWNER_TRIAL. That is
  readiness for a bounded, supervised local trial. It is not a
  full PASS, not whole-system VERIFIED, not owner product
  acceptance, and not a merge approval.
- Frozen inputs verified by the reviewer and re-checked here
  from the copied files: code C5R1
  `fd3430c9f1b0e98d1f6c9c62067b935f20054498`, evidence E5R1
  `dde7b605b0ef9c97e3ae91156303638f3ba843fd`. The copied
  `review-evidence/execution.json` records the same two
  commits, 50 pinned files, and 9 E5R1 manifest entries with
  no manifest errors.
- Machine (reviewer): Windows 11 build 26300, Python 3.14.4.
  Suite and acceptance both used the exact C5R1 Git checkout.
  Acceptance was run by absolute path with `--source-root`
  and a new external `--output-dir`, from outside the source
  checkout.

## Windows suite (reviewer-run)

- Command: the reviewer's BAT/helper run (see
  `review-evidence/execution.json` for the exact native
  command, and `windows-runs/.../test-run.log` for the raw log).
- Result: **57 attempted, 55 passed, 0 failures, 0 errors,
  2 skipped. Child exit 0, helper exit 0, BAT exit 0.**
- Skipped coverage (NOT_RUN, never PASS): C4 T24 symlink
  store subcase and C5 symlink path-boundary subcase, both
  WinError 1314 (a required privilege is not held by the
  client). The raw BAT stdout log in
  `review-evidence/suite-bat.stdout.log` lists both skips
  with the same WinError 1314 reason.
- Raw log hash check (independently recomputed from the copy
  in this supplement): `windows-runs/.../test-run.log`
  SHA-256
  `c24cb3433e163b457c974908b126c05df342472a44cd0ae68ad1b59de570e7e6`
  matches the reviewer report's suite raw log SHA-256, and
  `windows-runs/.../manifest.json` SHA-256
  `7527ae7a9a70d1e06a5ad6cd40d9f870907b417c5e9e6645e4425f47d4f9ec89`
  matches the reviewer report's suite helper manifest SHA-256.
  Both stderr logs are empty (0 bytes), which matches the
  execution receipt (stderr SHA-256 of empty input).

## Windows acceptance (reviewer-run)

- Runner: C5R1 `acceptance/run_acceptance_c5.py` by absolute
  path, `--source-root` = reviewer checkout,
  `--output-dir` = a new external directory (see
  `acceptance-output/acceptance-results.json` header for the
  exact reviewer paths).
- Result: **63 subcases, 59 PASS, 0 FAIL, 4 NOT_RUN,
  0 INCONCLUSIVE. Completed checks: 59/59 PASS (bounded
  completed-check verdict only). Full-scope verdict: NOT_RUN.
  Runner exit 2** (the intended incomplete-scope result, not
  a new runtime failure).
- The 4 NOT_RUN subcases, with the reasons recorded in the
  copied results file: A10 packet-level no-egress; A13 real
  changed-brief invalidation; A15 symlink privilege
  (WinError 1314, as above); A33 owner product acceptance.
- Independent controls reproduced in
  `review-evidence/independent-controls.json`: padded reason
  preserved with id `DEC-6a82e87b3bdd26d0` distinct from
  unpadded `DEC-1e34f4692b242c32`; T04 DONE without a decision
  still suggests decide, while T04 DONE with a decision has
  next action null; overview/verify explicitly state Judge
  scope as C4-only with C5 freshness not covered, and
  implementation NOT_VERIFIED.

## Linux vs Windows — do not conflate

- Linux (Muse, E5R1): suite 57/57, acceptance 60 PASS
  (symlink ran on Linux), full-scope NOT_RUN (3 NOT_RUN:
  A10, A13, A33), exit 2.
- Windows (reviewer, this supplement): suite 55 PASS + 2
  SKIP, acceptance 59 PASS + 4 NOT_RUN (the same 3 plus
  A15 symlink), full-scope NOT_RUN, exit 2.
- Never report Windows as 60 PASS, and never merge the
  skipped/not-run subcases into a PASS total. The only
  difference between the Linux and Windows acceptance totals
  is the symlink privilege subcase, which ran on Linux and
  did not run on Windows.

## Minor residuals — backlog, not fixed in frozen C5R1

These were raised by the reviewer as P3, not trial blockers.
They are recorded here, not fixed here, because C5R1 stays
frozen for the first trial. Any later fix needs its own
revision and test rerun; it must not be smuggled into this
supplement.

- R1-UX01: T01–T03 DONE, T04 READY, with an existing matching
  decision still produces next action decide. The note that a
  decision removes the next action is true only when T04 is
  DONE. This suggests a duplicate review; it does not create
  approval and does not change stage or verification. Do not
  interpret a suggested repeat as a new required approval.
- R1-TOOL01: the acceptance output root is configurable but
  not enforced outside the source checkout, and the same
  output directory overwrites fixed filenames. Header
  command strings use unquoted paths and POSIX PYTHONPATH
  style. Do not claim filesystem-boundary or no-overwrite
  enforcement from this run. Use the quoted PowerShell
  runbook in the owner pilot protocol for trial runs.
- R1-SCOPE01: A32's title says payload-change invalidation,
  but its actual probe rejects a digest from a different
  proposal. Its detailed scope is narrower and explicit; do
  not interpret it as a demonstrated edit of an existing
  payload followed by invalidation of an earlier approval.
  No new brief editor or mutation command is needed for the
  pilot.

## What is not in this supplement

- No C5R1 code change, no E5R1 change, no fixture change.
- No trial input, manual baseline, or owner feedback: the
  owner trial is a separate bundle outside the source
  checkout (see OWNER_TRIAL_01 preparation; status
  WAITING_OWNER_INPUT because no real owner request has been
  supplied yet). The Muse-authored redacted template from
  the previous report is NOT owner evidence and is NOT
  copied into this supplement as trial input.
- No product acceptance, no merge, no whole-system VERIFIED
  claim. Remaining open scope (from the reviewer report):
  full pentest, packet-level egress, real changed-brief
  invalidation, symlink privileged coverage, real
  disk-failure recovery, live provider/worker/chat
  integration, admitted knowledge retrieval, measured owner
  baseline, owner product acceptance, and merge. W04 stays
  CLOSED_SCOPED.

## Evidence files in this supplement

All files under `evidence/windows-c5r1/` are byte-for-byte
copies of reviewer-branch files (relative paths below are
under `evidence/windows-c5r1/`; reviewer-branch paths are
`reviews/2026-10-26-c5r1/` + the same relative path).
Hashes are SHA-256, recomputed from the copies in this
supplement; the full manifest is
`evidence/windows-c5r1/MANIFEST.json` (which excludes itself).

- `acceptance-output/acceptance-results.json` — Windows
  acceptance results (63 subcases, 59 PASS, 4 NOT_RUN).
- `acceptance-output/acceptance-results.md` — Windows
  acceptance table with scope.
- `acceptance-output/acceptance-manifest.json` — reviewer
  runner output manifest for the two files above.
- `bundle-manifest.json` — reviewer bundle manifest.
- `c5r1-pinned-manifest.json` — reviewer 50-file pinned
  manifest for the detached C5R1 checkout.
- `execution-receipt.json` — reviewer execution receipt.
- `review-evidence/execution.json` — reviewer execution
  record (commits, suite/acceptance commands, exits, hashes).
- `review-evidence/independent-controls.json` — reviewer
  independent reason/T04/Judge controls.
- `review-evidence/suite-bat.stdout.log` — raw BAT suite
  stdout (57 attempted, 55 passed, 2 skipped).
- `review-evidence/suite-bat.stderr.log` — empty (0 bytes).
- `review-evidence/acceptance-windows.stdout.log` — raw
  Windows acceptance stdout (59 PASS, 4 NOT_RUN, exit 2).
- `review-evidence/acceptance-windows.stderr.log` — empty
  (0 bytes).
- `windows-runs/run-20261025T175748Z-6f8195a8/test-run.log`
  — raw suite run log (SHA-256 c24cb343... as above).
- `windows-runs/run-20261025T175748Z-6f8195a8/manifest.json`
  — suite run manifest (SHA-256 7527ae7a... as above).
