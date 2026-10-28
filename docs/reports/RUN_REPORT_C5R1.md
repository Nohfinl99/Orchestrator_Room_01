# Run Report C5R1 — bounded fixes C5-F01..F07 (builder evidence, not a reviewer verdict)

**Code commit C5R1:** `fd3430c9f1b0e98d1f6c9c62067b935f20054498` on branch
`muse/local-control-room` (separate from this evidence commit E5R1).
**Evidence in this commit:** `evidence/c5r1/` plus this report.
**Overall system status: NOT_VERIFIED. Owner product acceptance:
PENDING. Independent reviewer verdict on the frozen C5R1/E5R1
snapshot: PENDING (reviewer Windows rerun requested, not yet done).**

## Reviewer instruction and verdict taken in

- Instruction: `MUSE_AFTER_C5_REVIEW.md` on reviewer branch
  `codex/c5-independent-review`, commit
  `e65a5f82f688d72a1b54ee833fefb54c1e4b2209`, with
  `reviews/2026-10-26-c5/REPORT.md` (read-only reference, not
  copied into this branch). Reviewer verdict: REVISE_C5_BOUNDED.
- Reviewer Windows C5 results taken as history, not rewritten:
  suite 54 attempted, 51 PASS, 1 FAIL (test_c5_10, Windows text
  writer LF→CRLF), 2 SKIP (C4 T24 symlink, C5 symlink,
  WinError 1314), child/helper/BAT 1; acceptance raw 52 PASS /
  1 FAIL with the A15 symlink subcase wrongly recorded as PASS.
  Those old results are preserved in C5/E5 and are not used as
  evidence for C5R1.
- C5R1 scope basis: owner build approval for C5 (direct Muse
  chat, 2026-10-25 23:50:52 Asia/Bangkok, scope packet REV2.1 +
  F21) plus the reviewer statement that bounded bugfixes inside
  this slice do not need a fresh approval round. No new product
  feature, no brief, no roadmap was written in this round. No
  merge, no PR, no change to main or Orchestrator_Reverse.
  This round pushed only to `muse/local-control-room`.

## Code under test (C5R1 commit, remote-blob-verified)

| File | Remote blob SHA-1 (matches local) | SHA-256 (local, pre-commit) |
|---|---|---|
| `control_room/__init__.py` | `aa84dc5689cf32b30d63b18867beba1fbc06fc0b` | `c85da8a3cd662f78cc09e39a2e0548257f25e08b45a0afa6f257bae932ae1158` |
| `control_room/backend.py` | `0d5300ffba08d25f0c35cbde02b7e85d90874d9b` | `a3007504c3eb591efa92b97de4e29d497c52c2a67e674c7dad913f8e19dc5464` |
| `control_room/README.md` | `aaa9f76b7b384311029c896ba05770ac7f898972` | `213378ffd0e3a31119170712864b35efe33fc74dbb1598299069a21c708cf6b9` |
| `control_room/C5R1_NOTE.md` | `c2c4a03516946a9e561fe67243fcec2abf52467d` | `e1e24d544d7d677e86eef6f8ae8fabcd1feafd06fd60e10fb98ad23a7884a97d` |
| `tests/test_intake_c5.py` | `6308f0542f4fd5e324e4b90216486d25e68471a1` | `005dc206cd88d2f11df1dee10f4fed3b797b3b73315d3276b245454b47cd16a0` |
| `acceptance/run_acceptance_c5.py` | `e7d83a3890f6c11859b8fdbc3d3611f09a0b7347` | `5a2da9f2f93eb86233be18e77e37780ec4b218527a1a06b65c2c95633a62df7a` |

Unchanged in C5R1 (verified by blob before committing):
`control_room/cli.py`, `control_room/C5_BUILD_NOTE.md`,
`control_room/__main__.py`, `tests/test_control_room.py`,
`fixtures/intake-rev2/` (manifest SHA-256
`fd1716cb77b93adbe739663a630beb3eb80232dbc463f04cdad631d0c265a39c`).
The acceptance and test runs below were made against local
files byte-identical to the C5R1 commit blobs above.

## Builder test suite (Linux, Python 3.12.3)

- Command: `PYTHONPATH=. python3 -m unittest
  tests.test_control_room tests.test_intake_c5 -v`
- Log: `evidence/c5r1/test-suite-c5r1.log` (raw stdout/stderr).
- Result: **57 tests, 57 PASS, 0 FAIL, 0 skipped on Linux**
  (36 C4 tests unchanged and passing, plus 21 C5 tests: the 18
  C5 tests plus 3 new C5R1 tests for padded reason, T04 next
  action, and Judge scope). These are builder-run local checks
  with synthetic fixtures only. They are not an independent
  review and not a pentest. On Windows, skipped tests (notably
  symlink privilege) remain NOT_RUN, not PASS, and must be
  reported that way by the reviewer rerun.

## Acceptance A01–A33 + variants (builder-run, Linux, Python 3.12.3)

- Runner: `acceptance/run_acceptance_c5.py` in C5R1 (tooling),
  byte-identical copy in `evidence/c5r1/acceptance-runner.py`
  (SHA-256 `5a2da9f2...`). Reproduce from any cwd:
  `python3 acceptance/run_acceptance_c5.py --source-root
  <checkout> --output-dir <outside-the-checkout-dir>`.
- Results: `evidence/c5r1/acceptance-results.json` (per-subcase:
  fixture + SHA-256, scope, exact commands with absolute
  PYTHONPATH, raw stdout/stderr per subcase, PASS/FAIL/NOT_RUN)
  and `evidence/c5r1/acceptance-results.md` (table with scope).
  Runner's own output manifest:
  `evidence/c5r1/acceptance-manifest.json`.
- Result: **63 subcases: 60 PASS, 0 FAIL, 3 NOT_RUN.**
  **Completed required checks: 60/60 PASS. Full-scope verdict:
  NOT_RUN. Runner exit code: 2** (by design: no FAIL, but
  required NOT_RUN subcases block a full-scope PASS; see below).
  A full-scope PASS is not claimed, and the completed-checks
  verdict is not renamed as a full-scope PASS.
- The 3 NOT_RUN subcases are by design, each with a stated
  reason and scope, none of them a hidden skip:
  A10 packet-level no-egress (needs packet-level monitoring,
  not performed); A13 real changed-brief invalidation (needs a
  brief editor, which C5 does not have); A33 owner product
  acceptance (needs a clear owner instruction with source,
  actor, time, and scope, not present).
- New C5R1 subcases, all PASS on Linux: A11 T04 ready next
  action is decide; A24 CRLF content never trimmed; A32 T04
  DONE distinct from decision; A32 decide before all tasks
  DONE; V07 padded reason verbatim; V07 Unicode reason
  verbatim; V08 legacy Judge scope C4 only. A13 was renamed
  from "changed brief invalidates approval" to "expected-brief
  mismatch rejection" to state its true scope; it is the same
  runnable check, not a new subcase.
- Golden identities verified live and unchanged: intake
  `INTAKE-96bccfdbe2a16dfc`, proposal digest
  `de30b806df66d4826100ea9e9a17c05408be674686b114b619d382d0204295c6`,
  decision `DEC-e81b5e7deada9801`, correction
  `INTAKE-432d09e4f46eaff1`, padded reason decision
  `DEC-6a82e87b3bdd26d0`, stripped reason decision
  `DEC-1e34f4692b242c32`.
- Retained golden-flow store: `evidence/c5r1/golden-flow-store.json`
  (final store SHA-256 for this run
  `b65bd6a7aa3c88d5ac1e947b1b78d464c4b4c13c625dae26a3a9b1eac29ad0fc`
  after init → intake → duplicate → propose → complete T01 →
  decide; step hashes in `golden-flow-steps.txt`;
  `verify-history` valid, event_count 5, overview counts 1/1/1,
  stage INTAKE, judge_scope present). Store hashes are
  run-specific because timestamps are real run times; the
  golden pins are the ids and digests above, not the store hash.
  Acceptance subcase stores were per-subcase temp dirs and are
  not retained individually; per-subcase raw outputs and golden
  hashes are retained in `acceptance-results.json`.

## C5-F01..F07 status and evidence locators

| Finding | Status in C5R1 | Evidence |
|---|---|---|
| F01 evidence truth | FIXED | Runner verdict model + exit codes (see acceptance header); A15 symlink NOT_RUN branch; no placeholder checks remain. Acceptance summary: 60/60 completed, 3 NOT_RUN, full_scope NOT_RUN. |
| F02 byte fixtures + symlink isolation | FIXED | C5 tests and runner use write_bytes throughout; LF and CRLF no-trim cases with hashes from original bytes (test_c5_10, A24). Symlink is its own subcase, NOT_RUN when creation fails. |
| F03 reason verbatim | FIXED | backend decide() stores/hashes reason verbatim (strip only for emptiness check); test_c5_19, acceptance V07 (padded DEC-6a82..., stripped DEC-1e34..., Unicode, whitespace-only rejected). Golden unpadded id unchanged. |
| F04 T04 next action | FIXED | backend proposal_view() gate logic; test_c5_20, acceptance A11 T04 ready, A32 T04 DONE distinct, A32 decide before all DONE. Complete kept as status only; no all-tasks-DONE prerequisite added to decide. |
| F05 Judge scope | FIXED | verify()/overview() judge_scope field (C4 collections only); snapshot_digest() and judge_report() unchanged, no repin; test_c5_21, acceptance V08. |
| F06 coverage split | FIXED | A13, A10, A33 each split into a runnable PASS subcase (narrow scope) and an explicit NOT_RUN subcase; status table states each scope. No brief editor added. |
| F07 runner roots | FIXED | Runner --source-root/--output-dir, auto-detection, absolute PYTHONPATH in recorded commands, reproduce command, tool SHA, and output manifest in the results header. |

## What this report does not claim

- No whole-system VERIFIED claim. Implementation verification
  stays NOT_VERIFIED in simulation, as in C4/C5.
- No owner product acceptance: a C5 `OPERATOR_ASSERTED`
  decision is a local gate decision, not product acceptance,
  and it does not move the C4 product stage.
- Baseline remains six null fields; no efficiency or
  product-value claim is made. The trial preparation after
  bounded review is a separate workspace deliverable, not part
  of this evidence commit.
- Still NOT_RUN / PENDING: independent reviewer verdict on
  the frozen C5R1/E5R1 snapshot, reviewer Windows rerun of
  C5R1 (suite + acceptance, including symlink privilege
  coverage), full independent acceptance audit, full pentest,
  packet-level egress monitoring, real disk-failure recovery,
  live-agent/runtime integration, owner product acceptance,
  and any merge decision.
- Windows results in this report are by the reviewer on the
  old C5 revision (history above). Muse's C5R1 runs are Linux
  only; Linux does not prove Windows.

## Next atomic action

Reviewer reruns the frozen snapshot: code commit C5R1
`fd3430c9f1b0e98d1f6c9c62067b935f20054498` plus this evidence
commit E5R1 (pin to be recorded after push), on Windows and on
Linux, using the runner command in the acceptance header. A
reviewer verdict is not owner acceptance; owner acceptance
still requires a clear owner instruction with source, actor,
time, and scope for the product slice itself.
