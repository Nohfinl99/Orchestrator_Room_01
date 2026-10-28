# Windows supplement for code C3 — reviewer-executed, not Muse-executed

This supplement preserves, byte-for-byte as downloaded from the
reviewer branch `codex/windows-c3-review`, the actual Windows run
of code C3. It does **not** rewrite `RUN_REPORT_REV3.md`, whose
historical wording "Windows NOT_RUN_BY_MUSE" remains true: Muse
did not execute this Windows run; an independent reviewer did, on
Windows, and this supplement records that fact exactly.

Do **not** use this supplement as evidence for C4 or any later
source change. A changed source needs its own frozen commit and
its own fresh evidence (see `RUN_REPORT_REV4.md` for C4).

## Identity

- Code C3: `9aca1b91dfe7e85d084bac51392fb65c5e3ee4fa`
- Builder evidence E3: `c134d7ae1e871f3fba5338b7a674694c0350d3c6`
- Guide/tooling T: `1a163e759380aad186568cfaefbd05653fd35339`
- Reviewer branch: `codex/windows-c3-review`
- Reviewer report (copy in this supplement): `evidence/windows-c3/REPORT.md`

## Actual Windows result for C3 — read the counts exactly

- Environment: Windows 11 build 26300, Python 3.14.4
- **34 attempted, 33 PASS, 0 ERROR, 0 FAIL, 1 SKIP**
- **Test-process (child) exit: 0**
- **Helper-process exit: 0**
- **BAT exit: NOT_APPLICABLE for this run** — the reviewer invoked
  the Python helper directly from a separate tooling directory,
  not through `run_windows_tests.bat`. No BAT exit code is claimed
  for the C3 suite.
- **SKIP case: T24 symlink, SKIP / NOT_RUN, WinError 1314**
  (privilege not held). It is not a pass, and it is not hidden.
- **Not all 34 cases passed.** 33 passed and 1 skipped. Any summary
  saying "34 passed" is wrong.
- Lock subcases: T29 abrupt-death recovery and T30 synchronized
  two-process write both reported ok on Windows, exercising the
  msvcrt path.
- Source acquisition: C3 source was fetched at its exact commit
  through the authenticated GitHub file API and materialized as
  original UTF-8 bytes. This is an **API snapshot, not a claimed
  local Git checkout**. All seven E3 source pins matched before
  and after execution; the helper's six source hashes also match C3.
- No C3 source/test file or T tooling file was edited for this run.

## Preserved files (SHA-256, as copied)

| File in this supplement | SHA-256 |
| evidence/windows-c3/REPORT.md | 4f0629e0858609ae039cf86efa81eed290b5f20c3731d9e0c8fc5e4283829144 |
| evidence/windows-c3/windows-test-run-2026-10-25.log | d2a226190d43ac7db4ac08c5ca352ab9c0c947ebb2485f096ed638c734e75f9e |
| evidence/windows-c3/windows-test-manifest.json | e554112b1b2b1d32fcc96252169944c2cc474701f9492e7587ed85a05194afde |
| evidence/windows-c3/windows-helper-console.log | fc3be44b4df45373c27dbb9bbe7d027e7aca8f20c7de0c0b7750776a1ef938ba |
| evidence/windows-c3/execution-receipt.json | d1299b2e5d21a6c3950ec69dd70f29afe8c15466628bb5716b5860f96e0ea20e |
| evidence/windows-c3/bundle-manifest.json | 30d16417118b129f11021251af3ce4bed3be7d2b08cfae0add2b51dbe3111357 |
| evidence/windows-c3/smoke-and-controls.json | bd07dcaa7909952f307e2852855cb71e9807d7bb1a8f1460d25e430388c6f575 |
| evidence/windows-c3/tooling-negative/result.json | 68cd4fae3a2fa2d4edb87998a2c16a83de48fea0ba07c7648634a07ef070fd3a |
| evidence/windows-c3/tooling-negative/failing-suite.log | 7af880436ce6cbca1817ef078a6ed9f95220d63bb34cc1d312b9889a84e77849 |
| evidence/windows-c3/tooling-negative/launcher-console.log | efeb6aaf1b8f2975f1bc373561baaf58ee4e5726c1d187e2d04111e7b11d4d6a |
| evidence/windows-c3/tooling-negative/helper-manifest.json | e55eb35a27d38a11d43dd9ece28df18ee83dc72def6f35e9c32ac4ec55144500 |

## Reviewer findings carried forward (disposition is in later commits)

- **W01 (runner exit swallowed):** in the old T tooling, a synthetic
  failing fixture gave child exit 1, helper exit 0, BAT exit 0.
  See `evidence/windows-c3/tooling-negative/`. That fixture is a
  tool test, never a C3 product failure. Repaired in the corrected
  runner (tooling revision after T); see `WINDOWS_RUN_GUIDE.md`.
- **W02 (commit label not binding):** the same fixture had an empty
  `control_room/` directory and all six expected sources missing,
  yet the old helper still recorded C3 and returned 0. Repaired by
  fail-closed preflight in the corrected runner.
- **W03 (repeatability/metadata):** old log names used only the
  date, the manifest had one fixed filename, the helper recorded
  its own version even if `--python` selected another interpreter,
  and stdout/stderr were concatenated after the child exited.
  Repaired in the corrected runner: unique run directories,
  selected-interpreter metadata, ordered merged stream, and
  authoritative count validation.
- **G01 (genesis project integrity, P2):** with no events, changing
  `project.pain_status` and `project.soul.purpose` without a chain
  recompute still returned `chain_valid=true` in C3. Repaired in
  source commit C4, not by relabelling this supplement.
- Smoke/controls: 6 PASS, 1 FAIL (the G01 case) in
  `evidence/windows-c3/smoke-and-controls.json`.
- Reproducers remain on the reviewer branch at
  `reviews/2026-10-25-c3-windows/smoke_and_controls.py` (SHA-256
  `b61d78c1ad8dd18832a4c13355d748c2490126763cf9438db722dd77d8630e11`)
  and `reviews/2026-10-25-c3-windows/tooling_checks.py` (SHA-256
  `d47fc6fa268cebfde94a13f2844ed2eca8ea1ca7be15c8cd7fa7c95f4afde0ab`);
  they are referenced here, not copied as working-branch code.
  Regressions for the corrected runner are implemented separately
  in `scripts/test_runner.py` on the working branch.

## Overall status

**NOT_VERIFIED.** This supplement is a bounded Windows run plus
bounded review. It is not a full pentest, not a complete independent
acceptance of all C3 behavior, not packet-level no-egress evidence,
and not an owner merge decision. A separate reviewer issues the
next verdict.
