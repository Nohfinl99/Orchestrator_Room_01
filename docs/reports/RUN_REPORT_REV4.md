# RUN_REPORT_REV4.md — G01 repair and corrected runner (revision 4)

This report is evidence for implementation commit C4 only. It does
not rewrite earlier verdicts, and it does **not** reuse the C3
Windows log, the C3 Linux log, or any C3 evidence as proof for C4.
C4 was frozen first, then run fresh with the corrected external
runner. The overall system stays NOT_VERIFIED until a new separate
reviewer inspects C4 and its raw evidence and issues a fresh verdict.
Muse's self-run tests below are builder-run local checks, not
independent review.

## Preservation

- The original `RUN_REPORT.md`, `RUN_REPORT_REV2.md`, and
  `RUN_REPORT_REV3.md` are preserved unchanged.
- History preserved: code C `d409eca531a202879c2d5bcddc3f9e90794335d3`,
  evidence E `25f9f034d9493d447242ab16f674e27617b5605c`, docs D
  `00be60d7440b5ce48e9f392f95fcedb3fa090d61`, code C3
  `9aca1b91dfe7e85d084bac51392fb65c5e3ee4fa`, evidence E3
  `c134d7ae1e871f3fba5338b7a674694c0350d3c6`, tooling T
  `1a163e759380aad186568cfaefbd05653fd35339`, Windows supplement S
  `23f1e4264cdb815383a939868003307f608b39ef`, tooling v2 T2
  `ee839572d85392020d1f9ec90d1870d7064e3632`.
- No merge was made. No change was made in `Nohfinl99/Orchestrator_Reverse`.
- The C3 Windows supplement (`WINDOWS_SUPPLEMENT_C3.md` and
  `evidence/windows-c3/`) remains a C3 record only. Its counts
  (34 attempted, 33 PASS, 1 SKIP) are not C4 counts.

## Implementation commit C4

- Repository: `Nohfinl99/Orchestrator-Room`, branch `muse/local-control-room`
- Base for this iteration: T2 `ee839572d85392020d1f9ec90d1870d7064e3632`
  (tooling only; code at that point was still C3)
- Implementation commit C4: `3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c`
- Evidence commit E4: this commit, which contains only this report
  and `evidence/rev4/` files. Changing only evidence/docs in E4
  does not pretend the tested code was a different implementation;
  E4 names C4 and its source digests below.
- Changed paths in C4 (6 files, verified remote blob SHA = local git blob SHA):
  - `control_room/__init__.py` — version 0.4.0
  - `control_room/backend.py` — G01 genesis exact-match repair
  - `control_room/README.md` — revision 4 notes, genesis integrity
  - `tests/test_control_room.py` — Rev4 tests T33/T34, Rev3 tests retained
  - `PILOT_RUNBOOK.md` — new, CLI-only pilot runbook (docs)
  - `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md` — new, no new knowledge
- Unchanged in C4, carried from earlier commits: `control_room/__main__.py`,
  `control_room/cli.py`, original receipt, Rev2/Rev3 addenda,
  `OWNER_REVIEW_NOTE_REV2.md`, old reports and old evidence logs.

## Source digests for C4 (SHA-256, from the clean checkout)

| Path | SHA-256 |
| control_room/__init__.py | 86e690e4ed354ffd002a3e70cb8c7a8c45607bcf46ea55fe31239ec717dced52 |
| control_room/__main__.py | 82d644c5c56a0b05e23ecd9dd2742780c356118cb517148361bdf6ab60874e90 |
| control_room/backend.py | 28d37113ce65a34e3572af0ef37066a193637e35c75888dd002628eddfaca7fb |
| control_room/cli.py | 0298d4c2c27df22d013d36d1104cf7932c9facdb73c2263615624d9bb8d5a8d5 |
| control_room/README.md | 840cad9b62f177c230737c58ac28b3a5b01656c7e328f7520eb7eb06188355af |
| tests/test_control_room.py | 43f11aedb79cd9e584f332a042cf4eb5b85cbe6a5407837d5e9f5cc2042e5ea6 |
| PILOT_RUNBOOK.md | 4c9ee3e229250aa0c82474753eb53e94396c5b871667e14818dbbaa627eed10e |
| MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md | c76bbc367351f21c42baea1c1d284b84816487135ab37718528266c8d558ee27 |

Pinned manifest used for the run: `evidence/rev4/c4-pinned-manifest.json`,
SHA-256 `9086c094a5ba575284d6282e5568c50b809c8e2eedbd2d7a96a16e34ff59f901`.
It contains code_commit C4, pin_origin, and the eight digests above.
Future Windows runners must use this pinned manifest (or a later
commit's own pinned manifest), never a typed commit string and
never the C3 manifest.

## Tooling revision used for the C4 run (external, separate roots)

- Tooling T2: `ee839572d85392020d1f9ec90d1870d7064e3632`
- Runner: `scripts/run_windows_tests.py` v2, SHA-256
  `1ff9e2ef998ba136e0c7b29e9ffcd674ecdecc8ba87b50f0b24442b352bc4e70`
- BAT: `scripts/run_windows_tests.bat` v2, SHA-256
  `01edaf34223299b38d7d4f9a3a509d21a4cdea05aa79a105d847d0a9c9f3af79`
- Runner regressions: `scripts/test_runner.py`, SHA-256
  `28e14003b4047e52879b06c621ed403ff79f3ffab084e93c73dff13facf30dbe`
- Code root (clean API checkout of C4, `control_room/` + `tests/` +
  the two new C4 docs, downloaded via the GitHub API): separate
  from the tooling root (clean API download of T2 scripts/guide).
  Output-base was outside both roots.
- Mode: **api-snapshot**. This run is not claimed as a Git checkout.
  No Git HEAD or clean-tree claim is made for the clean checkout;
  identity comes from the pinned manifest above, verified before
  and after the run.

## Clean-checkout test run, Linux, via corrected runner (the run that counts for C4)

- Child command: `<selected Python> -m unittest discover -s tests -v`
- Environment: Python 3.12.3, Linux htch-runtime 7.0.0-39-generic x86_64
- Run directory (unique, not overwritten): `run-20261025T103957Z-d41449a3`
- **Child exit: 0**
- **Helper exit: 0**
- **BAT exit: NOT_RUN** — Linux has no `cmd.exe`; the BAT was not
  executed in this run. Its exit propagation was checked only
  statically by the runner regressions below. A BAT exit code for
  C4 must come from an actual Windows run, not from this Linux run.
- **Counts: 36 attempted, 36 passed, 0 errors, 0 failures, 0 skipped**
- **SKIP cases in this Linux run: none.** T24 symlink passes on
  Linux, so there is no Linux SKIP to report. The C3 Windows SKIP
  (T24, WinError 1314) is a C3 Windows fact; it is **not** a C4
  Windows fact, because C4 has not been run on Windows yet.
  Windows SKIP for C4 is therefore **NOT_RUN**, not 0 and not 1.
- Source changed during run: false (before/after digests identical).
- Counts validated against unittest's authoritative totals
  (`Ran 36 tests`, `OK`); counts_valid true in the manifest.
- Raw log: `evidence/rev4/clean-checkout-test-run-2026-10-25.log`,
  SHA-256 `52a601af16982e182ec5fc0324ace232234d5ef0f8758a238dcdf70c960aa186`
- Runner manifest: `evidence/rev4/clean-checkout-manifest.json`,
  SHA-256 `dd5233f853e334cd2aab23d02e5806179b09c9baa74061d9d67cebcb26010dcb`
  (computed externally; the manifest does not contain its own hash)
- Runner console: `evidence/rev4/runner-console-c4.txt`,
  SHA-256 `19eb85eadf207b667f7a7bea0f51dcb53a6a378e62c79f1d79601742c48976f1`

## Runner regressions (tool tests, never product failures)

Run from the clean T2 tooling root, log in
`evidence/rev4/runner-regressions-2026-10-25.log`, SHA-256
`28ff307015695472ff6d6dae00208eaa281f914415007eb6c5d0096dbb46d043`:
- Passing suite with one skipped test: child 0, helper 0, SKIP reported by name.
- Failing suite: child 1, helper 1, artifacts preserved.
- Changed source / wrong digest: preflight 2, no test run, preflight recorded.
- Missing source: preflight 2, no test run.
- Interrupted collection (suite calls `os._exit` mid-run): helper 3, not success, log preserved.
- Unique run dirs: two runs do not overwrite each other; first log untouched.
- BAT static check only: BAT contains `exit /b %HELPER_EXIT%` and
  no unconditional Done before that check. BAT execution itself
  is NOT_RUN on Linux; it must be executed and reported separately
  on Windows.

## Finding disposition (W01–W03, G01)

- **W01 exit swallowed: REPAIRED in tooling v2, proven by regression.**
  Old T: child 1, helper 0, BAT 0. New v2: failing fixture gives
  child 1, helper 1, and BAT code propagates helper exit exactly.
  BAT execution for C4 itself is still NOT_RUN (see above).
- **W02 commit label not binding: REPAIRED in tooling v2, proven by regression.**
  Runner v2 accepts no `--code-commit` string as identity. It
  requires a pinned manifest, fails preflight (exit 2) on any
  missing file or digest mismatch, and in git mode also requires
  HEAD == pinned commit and a clean tree.
- **W03 repeatability/metadata: REPAIRED in tooling v2, proven by regression.**
  Unique run directories, selected-interpreter version recorded
  (not the helper's), ordered merged stream (not concatenated
  after exit), authoritative count validation, zero-discovered and
  unparseable results rejected as collection failures (exit 3),
  before/after source hashes, and manifest hash computed externally.
- **G01 genesis project integrity: REPAIRED in C4, tests T33/T34.**
  Empty-event `verify_history()` now compares the complete
  canonical store against the pristine genesis, including
  `project.id`, `room_id`, `pain_status`, and soul fields, plus
  any extra top-level field. The reviewer's exact tampers
  (`pain_status` -> `VALIDATED_WITHOUT_EVIDENCE`,
  `soul.purpose` changed, no chain recompute) now fail, and
  privileged mutation and proof evaluation remain blocked.
  Normal genesis still passes, including through the CLI
  (`verify-history` on a pristine `init` store).

## Entry point, honestly (pilot runbook)

- The product entry point is the CLI only. See `PILOT_RUNBOOK.md`
  for exact supported commands and observable next steps.
- The smoke run confirms only CLI state capture and next-step
  guidance. It does not activate a chat listener or a real-agent
  dispatcher when the owner sends a chat message.
- If a user-message entry/adapter is required next, it is one
  explicit atomic task (input -> intake record -> task/role
  proposal -> owner gate), defined in the runbook, not implemented
  here, and not silently enabled with a provider.

## Per-subcriterion matrix (builder-run Linux scope only)

| Subcriterion | Result | Test / evidence |
| G01 genesis integrity (project fields, soul, extra field, CLI) | PASS (Linux) | T33, T34 |
| Rev3 regressions B01–B06 (plan, binding separation, brief, history anchor, lock, boundaries) | PASS | T01–T32 (retained) |
| Binding separation: binding PASS is not implementation PASS | PASS (binding scope) | T10, T26 |
| Implementation verification | NOT_VERIFIED (by design in simulation) | T10, T26 |
| Runner regressions (fail, preflight, interrupt, unique dirs) | PASS (tool tests) | runner-regressions log |
| BAT exit propagation | STATIC CHECK ONLY on Linux; execution NOT_RUN | runner-regressions log |
| Windows suite for C4, including msvcrt lock branch and T24 SKIP | NOT_RUN (no Windows run for C4 yet; C3 Windows log not reused) | — |
| Packet-level no-egress | NOT_RUN (static import check only) | — |
| Browser/auth | NOT_RUN, scoped exclusion (no HTTP server) | — |
| Independent Judge review of C4 | NOT_RUN | — |
| Full pentest of C4 | NOT_RUN | — |
| Owner decision on Rev4 | NOT_RUN | — |
| Product/pain validation | NEEDS_EVIDENCE | — |

## Remaining gaps (do not hide as passes)

- Actual Windows run for C4, with child/helper/BAT exits and SKIP
  names reported separately: NOT_RUN. Use the corrected runner
  v2 and the C4 pinned manifest in E4; do not reuse the C3
  Windows log.
- Independent Judge review of C4: NOT_RUN.
- Full pentest of C4: NOT_RUN.
- Owner decision on Rev4: NOT_RUN.
- Packet monitoring, browser/auth target, approval timeout,
  fan-out/concurrency limits, real hardware failure recovery: NOT_RUN.

## Next atomic task

One task only: obtain an actual Windows run for C4 using runner
v2 and the C4 pinned manifest, package its raw run directory as
a Windows supplement naming C4 without changing C4 code, and
then have a new separate reviewer inspect C4, E4, and the
Windows supplement and issue the next independent verdict. Do
not rewrite any earlier verdict as a PASS, do not merge, and do
not extend scope until the remaining NOT_RUN items above are
resolved.
