# Evidence for tooling T3 (W04 fix) — Linux regressions only

- Tooling T3: `55bb2f90ee8a4a7a28555059ce122998d6477aa3`
- Code C4 (unchanged by T3): `3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c`
- Pinned-manifest provenance: E4 `evidence/rev4/c4-pinned-manifest.json`,
  SHA-256 `9086c094a5ba575284d6282e5568c50b809c8e2eedbd2d7a96a16e34ff59f901`.
  T3 does not repin C4 and does not change C4.
- Runner v2.1: `scripts/run_windows_tests.py`, SHA-256
  `be76066c5fd940553f2767afd27cdbac91ecbe0e9902f823fa01bef5b6221a9a`
- Regression script: `scripts/test_runner.py`, SHA-256
  `278d21fc5b8fd7e681e9a11ef59e6208747c7abdd160a3ff8a7f9a185af0678c`
- BAT v2 (unchanged by T3): SHA-256
  `01edaf34223299b38d7d4f9a3a509d21a4cdea05aa79a105d847d0a9c9f3af79`
- Clean tooling root: T3 scripts downloaded via GitHub API, separate
  from any code root. Regression log: `runner-regressions-2026-10-25.log`,
  SHA-256 `9e6d9a600ecf27b9ccedb2ddf9f1ed2d1256940d727fad2a1f2a9f662b5b4fa2`.
- Regression result: 39 PASS lines, `ALL RUNNER REGRESSIONS PASS`,
  test-runner exit 0. Parser cases include LF and CRLF for OK,
  OK with skip, FAILED, mismatched totals, zero tests, missing
  summary, and truncated summary. Raw bytes are preserved: the
  parser normalizes only an in-memory copy.
- BAT execution: NOT_RUN on Linux (no `cmd.exe`). BAT exit
  propagation for T3 was checked statically only in the regression
  script. A real Windows BAT rerun for T3 against clean C4 is
  requested and must be reported separately with child/helper/BAT
  exits and skip names. Linux execution does not prove Windows
  BAT execution.
- Old evidence unchanged: E4, C3 Windows supplement, and earlier
  reports were not edited by T3 or by this evidence commit.
