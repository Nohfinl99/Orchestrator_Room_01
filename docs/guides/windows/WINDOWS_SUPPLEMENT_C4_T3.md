# Windows Supplement — C4 with Tooling T3 (reviewer-run, not Muse-run)

**This supplement was not produced by Muse running Windows.**
Muse runs on Linux and cannot run a Windows BAT. The run below
was performed by the reviewer on branch
`codex/t3-orchestrator-meeting` (commit
`25ded940fc09145acc034d09da49dc1230c99a4a`, file
`NEXT_MUSE_INSTRUCTIONS.md` blob `2c50ec2de3f8efb404a5e96c9f5102881b69bf03`),
and is accepted here from that reviewer source, with its raw
logs/manifests copied byte-for-byte into `evidence/windows-c4-t3/`
in this commit. Do not describe this as Muse's own Windows run.

## Pins, named separately

| Pin | Value |
|---|---|
| Code C4 | `3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c` |
| Tooling T3 | `55bb2f90ee8a4a7a28555059ce122998d6477aa3` |
| Evidence pin E4 (pinned manifest) | `d09d75f4b3c3b94dcd8cc9ea982d670ccf7e791b` |
| Pinned manifest | `evidence/rev4/c4-pinned-manifest.json`, SHA-256 `9086c094a5ba575284d6282e5568c50b809c8e2eedbd2d7a96a16e34ff59f901` |
| Reviewer branch / commit | `codex/t3-orchestrator-meeting` / `25ded940fc09145acc034d09da49dc1230c99a4a` |
| Reviewer meeting record | `reviews/2026-10-25-t3-meeting/MEETING.md`, SHA-256 `b00ae4d73d45b1e69879c56cfe09bbf0a367e90fb070701ac573b24cce735a92` |
| Reviewer execution receipt | `reviews/2026-10-25-t3-meeting/execution-receipt.json`, SHA-256 `4f776f35ad82575f6320ae60ed029aecf88061c63ea655bd323b7b617db7f03b` |
| Reviewer BAT controls | `reviews/2026-10-25-t3-meeting/bat-controls.json`, SHA-256 `2559c00cc57541f4f2a4296bc8706ecdc5c03f96897653e0627bb6c314b7cc80` |
| Reviewer bundle manifest | `reviews/2026-10-25-t3-meeting/bundle-manifest.json`, SHA-256 `16639e9c2a6d51407c3dc04e8dec64f93555282dcb2dde275dbf48fce002c63c` |

## Windows C4 suite run (reviewer, BAT T3)

- Environment: Windows 11 build 26300, Python 3.14.4, helper 2.1.0.
- Source: clean detached Git checkout of C4, clean detached
  worktree of T3, outputs outside both. All eight pinned source
  digests matched before and after.
- **Counts: 36 attempted, 35 passed, 0 errors, 0 failures,
  1 skipped. `counts_valid=true`.**
- **Exits: child 0, helper 0, BAT 0.**
- Raw log: `evidence/windows-c4-t3/test-run.log`, SHA-256
  `92c6864b421e70cb7051ee9b2db8676eebe4918f3befb40fd06aa61a3129a9c8`.
- Helper manifest: `evidence/windows-c4-t3/manifest.json`,
  SHA-256 `d2a11733ecc92bef7a23ed35d0081221ab5ed0d41a04f8d9a5a71848d4caa8a1`.
- **T24 symlink subcase: WinError 1314, NOT_RUN, not PASS.**
  The skip is preserved in the counts above; it is not a pass.
- This run is a test-suite run, not an independent Judge review
  and not a pentest.

## Tooling regressions on Windows (reviewer, 39 assertions)

- Tooling regression harness on Windows: exit 0, **39 assertion
  PASS**. These are tooling assertions, not C4 product tests,
  and must not be added to the 36 C4 tests.
- Decoded log copy: `evidence/windows-c4-t3/runner-regressions-windows.decoded.log`,
  SHA-256 `fea62bd2980615805ce7faaa0b602370323fee5c9abc80604eb2f99e0237bea7`.
  Note from the receipt: the published log was transformed
  from PowerShell redirected UTF-16 to UTF-8; it is not the
  product raw log. The product raw log is `test-run.log` above.
- **Wording correction (T3-COV):** the invalid parser cases in
  T3 (mismatched totals, zero tests, missing summary, truncated
  summary) currently have CRLF fixtures only; LF invalid cases
  and bare-CR cases are not covered. Do not describe the T3
  parser matrix as fully LF/CRLF for the invalid group. This
  wording correction does not reopen W04 and does not change T3;
  a future tooling task may add those fixtures separately.

## BAT fixture controls (reviewer, synthetic tooling fixtures only)

From `evidence/windows-c4-t3/bat-controls.json` (six runs,
all expected outcomes observed):

| Case | child | helper | BAT |
|---|---|---|---|
| pass, run twice (two run dirs, earlier run unchanged) | 0 | 0 | 0 |
| fail | 1 | 1 | 1 |
| interrupted (child 137) | 137 | 3 | 3 |
| wrong digest (preflight, no child test log) | null | 2 | 2 |
| missing source (preflight, no child test log) | null | 2 | 2 |

These fixtures are tooling tests with synthetic data, not C4
business cases. The reviewer's first harness attempt failed to
launch the fixture helper because of a reviewer cmd quoting
error, was fixed in the harness, and was rerun in fresh
directories; that harness error is not attributed to T3.

## Finding status after this supplement

- **W04: CLOSED_SCOPED** for runner T3 in the Windows runs
  recorded above (reviewer decision in MEETING.md). Scope is
  exactly these runs; it is not a whole-system pass.
- **T2 FAIL history is preserved and not rewritten.** The
  earlier Windows C4 run through T2 (36 attempted, 35 PASS,
  1 SKIP T24, child 0, helper 3, BAT 3, W04) remains the T2
  record. The new T3 run does not edit the T2 raw log, manifest,
  or verdict.
- **T24 remains NOT_RUN** (WinError 1314) in both the T2 and
  T3 Windows runs. It passed on Linux, which does not prove
  the Windows symlink subcase.
- **Overall system: NOT_VERIFIED.** Full C4 acceptance audit,
  full pentest, packet-level egress monitoring, owner product
  acceptance, real disk-failure recovery, and live-agent/runtime
  integration remain NOT_RUN/PENDING.
- **Old evidence unchanged by this supplement:**
  `RUN_REPORT_REV4.md`, `evidence/rev4/`, `evidence/windows-c3/`,
  `evidence/tooling-t3/`, and all earlier reports are not edited
  here. This supplement adds a new record; it does not rewrite
  an old one.
