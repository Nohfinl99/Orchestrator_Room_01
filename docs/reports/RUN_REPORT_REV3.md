# RUN_REPORT_REV3.md — repair of findings B01–B06 (revision 3)

This report is evidence for implementation commit C3 only. It does not
rewrite earlier verdicts. The Rev2 review recommendation was
REVISE_AGAIN, and the overall system stays NOT_VERIFIED until a new
separate reviewer inspects C3 and its raw evidence and issues a fresh
verdict. Muse's self-run tests below are builder-run local checks,
not independent review.

## Preservation

- The original `RUN_REPORT.md`, `RUN_REPORT_REV2.md`,
  `evidence/local-test-run-2026-10-25.log`,
  `evidence/rev2/*`, `MUSE_KNOWLEDGE_RECEIPT.md`, and
  `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` are preserved unchanged.
  They are not edited by this revision.
- History C/E/D is preserved: code C
  `d409eca531a202879c2d5bcddc3f9e90794335d3`, evidence E
  `25f9f034d9493d447242ab16f674e27617b5605c`, docs D
  `00be60d7440b5ce48e9f392f95fcedb3fa090d61`.
- No merge was made. No change was made in `Nohfinl99/Orchestrator_Reverse`.

## Implementation commit C3

- Repository: `Nohfinl99/Orchestrator-Room`, branch `muse/local-control-room`
- Base for this iteration: C `d409eca531a202879c2d5bcddc3f9e90794335d3`
- Implementation commit C3: `9aca1b91dfe7e85d084bac51392fb65c5e3ee4fa`
- Evidence commit E3: this commit, which contains only this report and
  `evidence/rev3/` files. Changing only evidence/docs in E3 does not
  pretend the tested code was a different implementation; E3 names C3
  and its source digests below.
- Changed paths in C3 (6 files, verified remote blob SHA = local git blob SHA):
  - `control_room/__init__.py` — version 0.3.0
  - `control_room/backend.py` — frozen plan binding, binding vs
    implementation separation, brief recompute and coherence,
    anchored history, privileged-mutation blocking
  - `control_room/cli.py` — stable OS lock (never unlinked), history
    blocking for mutations, history status in overview
  - `control_room/README.md` — revision 3 rules, verification semantics, lock lifecycle
  - `tests/test_control_room.py` — Rev3 oracles, V2_01–V2_07 adaptations,
    in-process boundary tests, real-process lock/CAS tests
  - `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` — new, correcting Rev2
    application claims; ten original knowledge pins unchanged, no new
    knowledge ingested
- Unchanged in C3, carried from earlier commits: `control_room/__main__.py`,
  `RUN_REPORT.md`, `RUN_REPORT_REV2.md`, `MUSE_KNOWLEDGE_RECEIPT.md`,
  `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md`, `OWNER_REVIEW_NOTE_REV2.md`,
  old evidence logs.

## Source digests for C3 (SHA-256, from the clean checkout)

| Path | SHA-256 |
| control_room/__init__.py | 386a72d4662b9fd5656ecd85ffa34bd72d4700d1e18a577cd0483d5479c8c834 |
| control_room/__main__.py | 82d644c5c56a0b05e23ecd9dd2742780c356118cb517148361bdf6ab60874e90 |
| control_room/backend.py | b62c58452ce0c6b4a952456e06fd73475526fae2f0aab416c0124bd4292d905c |
| control_room/cli.py | 0298d4c2c27df22d013d36d1104cf7932c9facdb73c2263615624d9bb8d5a8d5 |
| control_room/README.md | 48523bf4d3a521b412fa667b7fddb98a5932c2ccb8ac41f227c4f4209a71b905 |
| tests/test_control_room.py | 38caedf41c1eca068754d39f9ab83664715b33b45343aef3da3be98bd0161570 |
| MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md | 7b8ef43b5d2dbf3d4cfbd2704e788b0c9213bff3831e4a05a71356c892f325a0 |

Verification plan (frozen): id `CONTROL_ROOM_VERIFICATION_PLAN`,
revision `REV3-1`, digest
`57c3913558aacbd77c949d32a532be892eb5483d50a5124a1abacfe69103bcae`,
criteria `ACCEPTANCE-REV2-1`, ten required cases as in
`backend.REQUIRED_VERIFICATION_CASES`.

## Clean-checkout test run, Linux (the run that counts for C3)

- Command: `python3 -m unittest discover -s tests -v`
- Run against: a clean checkout of C3 downloaded via the GitHub API
  (`control_room/` + `tests/` only), verified byte-identical to the
  digests above before running.
- Environment: Python 3.12.3, Linux htch-runtime 7.0.0-39-generic x86_64
- Result: 34 tests run, 34 passed, 0 failed, 0 skipped, exit code 0
- Raw log: `evidence/rev3/clean-checkout-test-run-2026-10-25.log`,
  SHA-256 `dfd3c7df5c537d3b05bd57d82fcf729dedbdc6ee45057ca95e118944b4e567cd`
- Source manifest: `evidence/rev3/clean-checkout-source-digests.json`,
  SHA-256 `62dbf020a5ab08fad7940054800bee0f794bb7f290b2b3b817c3aad41b5949ff`

## Windows results — actual status, not a claim

- **Windows run by Muse in this turn: NOT_RUN.** The Muse VM is
  Linux; there is no Windows host, no wine/powershell, and no
  authorised external Windows runner was provided in this turn.
  No Windows count for C3 is claimed in this report.
- For reference only (Rev2 code, not Rev3): the reviewer Windows run
  on Windows 11 build 26300, Python 3.14.4 gave 25 attempted, 23 PASS,
  1 ERROR (T12 WinError 206), 1 SKIP (symlink WinError 1314), exit 1.
  That baseline is not presented as a Rev3 result.
- What Rev3 changed for Windows portability (so the next Windows run
  can actually execute): T12 no longer sends huge subprocess command
  lines; boundaries and true aggregate overflow are tested
  in-process (T12a), CLI subprocess checks use small arguments only
  and preserve the OS environment (T12b), and symlink remains
  SKIP/NOT_RUN on privilege failure (T24). The Windows msvcrt lock
  branch in `cli._store_lock` is implemented and code-reviewed, but
  it cannot execute on Linux; it needs an actual Windows run to be
  exercised, together with the abrupt-death and two-process cases
  (which are tested on Linux in T29/T30 via fcntl).
- Windows commands for the owner/reviewer (from the manifest):
  clone the branch, `git checkout 9aca1b91dfe7e85d084bac51392fb65c5e3ee4fa`,
  then `py -3.14 -m unittest discover -s tests -v`. Send the raw log
  back in direct chat; it will be packaged as a supplement naming C3
  without changing C3 code, or a separate reviewer can include it in
  the next review. Do not relabel an unexecuted Windows case as PASS.

## Finding disposition (B01–B06, and F01–F06 scope)

- **B01 / F01 plan override: REPAIRED, test T25.** An empty, partial,
  malformed, or unrelated `required_cases` override, or a mismatched
  plan id/revision/digest, is rejected before evidence is checked
  and never yields a binding PASS. The frozen plan is bound by id,
  revision, and digest in every `verify()` output.
- **B02 / F01 binding vs implementation: REPAIRED by separation,
  tests T10/T10b/T26.** `verify()` now returns `binding_checks` /
  `mechanism_result` separately from `implementation_verification`,
  which is always `NOT_VERIFIED` in this simulation, and the
  top-level `verification` field is never PASS. A synthetic case
  with one unrelated file reused for all ten cases (V2_01) yields
  binding PASS structurally, but implementation verification
  INCONCLUSIVE/NOT_VERIFIED — that distinction is the repair, not a
  failure of it. No shell, provider, or fake authentication was added.
  A real allowlisted runner needs its own trust model, proposed
  separately.
- **B03 / F02 brief content and graph: REPAIRED, tests T22/T31/T32.**
  Brief digests are recomputed from actual canonical fields, not a
  cached field. Acceptance requires a nonempty coherent graph:
  ready (non-blank) observations, reviewed inferences linked to
  those observations, and non-blank brief content still matching
  the approved digest. Orphan briefs and whitespace-only fields
  cannot open gates. Later decisions revalidate the accepted brief
  in addition to the judge snapshot.
- **B04 / F06 history anchor: REPAIRED, tests T09/T16/T27/T28.**
  `verify_history()` now checks schema, genesis, revision sequence,
  timestamp parseability, digest format and continuity, and the
  final anchor (last event stage, revision, and content digest
  against the current store). Changed content, changed revision,
  empty-event non-genesis, and changed event bytes without a full
  recompute all fail. Privileged mutations and proof evaluation are
  blocked on an invalid chain; diagnostic reads remain available.
  The same-owner/full-recompute limitation is retained and stated.
- **B05 / F04 lock lifecycle: REPAIRED on POSIX, Windows branch
  implemented but not executed here, tests T29/T30/T17/T18.**
  The lock file is never unlinked. POSIX uses fcntl flock on a
  stable inode, released by the OS on process death; Windows uses
  msvcrt locking on the same file, also released on process death.
  No lock is stolen by PID/time. Linux tests prove abrupt-death
  recovery and exactly-one-writer for two real processes. The
  Windows msvcrt branch still needs an actual Windows run (see
  Windows section above); it is not claimed as tested.
- **B06 / Windows test boundary: REPAIRED in test design, tests
  T12a/T12b/T24.** No huge subprocess command lines remain in the
  suite. Aggregate overflow is tested in-process with true sizes
  (two accepted stores under 1,000,000 bytes, third rejected with
  prior bytes preserved). CLI smoke checks preserve the OS
  environment. Symlink remains SKIP/NOT_RUN on privilege failure.
- **Kept working from Rev2:** exit-9 rejection, missing-case
  rejection, ordinary stale Judge invalidation, truthful pre-replace
  failure preservation, sequential CAS, aggregate size checks, and
  F03 simulation labelling (labelling only, not authentication).

## Per-subcriterion matrix (builder-run Linux scope only)

| Subcriterion | Result | Test / evidence |
| Overview, history, chain, overview history_valid | PASS (Linux) | T01, T09, T16 |
| Observation, facts/inferences, locator/hash, task DONE | PASS | T02–T05 |
| Illegal/unauthorised rejected, dependency CAS | PASS | T06, T07 |
| Full stage path with brief and judge binding | PASS | T08 |
| Binding separation: forged, exit-9, missing case, tampered artifact, no receipt | PASS (binding scope) | T10, T10b, T26 |
| Hostile text inert | PASS | T11 |
| In-process boundaries and true aggregate overflow | PASS | T12a |
| CLI smoke with preserved env, path boundaries | PASS | T12b |
| No network/shell imports (static scope only) | PASS (static) | T13 |
| Reload, binary store rejected | PASS | T14, T15 |
| Stale writer, failed save preservation | PASS | T17, T18 |
| Stale judge snapshot, empty gates, simulation labelling | PASS | T19–T21 |
| Brief recompute, orphan, whitespace | PASS | T22, T31, T32 |
| Schema v1 rejected, symlink (Linux) | PASS | T23, T24 |
| Frozen plan override rejected | PASS | T25 |
| History anchor and controls | PASS | T27, T28 |
| Lock death recovery (Linux fcntl), two real processes | PASS | T29, T30 |
| Implementation verification | NOT_VERIFIED (by design in simulation) | T10, T26 |
| Windows suite for C3, including msvcrt lock branch | NOT_RUN (see Windows section) | — |
| Packet-level no-egress | NOT_RUN (T13 is static only) | — |
| Browser/auth | NOT_RUN, scoped exclusion (no HTTP server) | — |
| Independent Judge review | NOT_RUN | — |
| Full pentest | NOT_RUN | — |
| Owner decision on Rev3 | NOT_RUN | — |
| Product/pain validation | NEEDS_EVIDENCE | — |

## Remaining gaps (do not hide as passes)

- Actual Windows run for C3, including the msvcrt lock branch,
  abrupt-death recovery on Windows, and symlink SKIP/NOT_RUN on
  Windows: NOT_RUN by Muse in this turn (see Windows section).
- Independent Judge review of C3: NOT_RUN.
- Full pentest of C3: NOT_RUN.
- Owner decision on Rev3: NOT_RUN.
- Packet monitoring, browser/auth target, approval timeout,
  fan-out/concurrency limits, real hardware failure recovery: NOT_RUN.
- The Rev2 reproducer `rev2_checks.py` is for frozen C; its
  invariants were adapted into the Rev3 tests above (notably
  V2_01–V2_07 into T25–T32, T12a, T29, T30), and its exit code is
  never used as a product pass. V2_01 under Rev3 semantics yields
  binding PASS but implementation NOT_VERIFIED, which is the
  intended separation.

## Next atomic task

One task only: obtain an actual Windows run for C3 (owner/reviewer
on Windows, or an owner-approved external Windows runner), package
its raw log as a supplement naming C3 without changing C3 code,
and then have a new separate reviewer inspect C3, E3, and the
Windows supplement and issue the next independent verdict. Do not
rewrite REVISE_AGAIN as a PASS, do not merge, and do not extend
scope until the remaining NOT_RUN items above are resolved.
