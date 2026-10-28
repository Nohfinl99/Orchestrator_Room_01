# Windows run guide, runner v2 — separate code and tooling roots

> This guide + `scripts/run_windows_tests.py` v2 + `scripts/run_windows_tests.bat` v2
> are **tooling, not product code**. They are published in a tooling
> commit separate from any code commit. Reviewing code means reviewing
> the code commit (C4 for the G01 repair, C3 for the Windows
> supplement), not the tooling commit. A tooling commit never proves
> a code commit.
>
> The old T guide had a revision error: checking out C3 removed the
> scripts, because the scripts were added only in T. This guide
> corrects that by keeping code and tooling in separate roots.
> Do not follow the old guide literally.

## 1. Roots — never mix them

```
<work>\
  code\            <- code worktree ONLY, at the target commit (e.g. C4)
  tooling\         <- tooling checkout ONLY, at the tooling commit
  windows-runs\    <- output-base, OUTSIDE code and tooling roots
```

- Code root: contains `control_room/` and `tests/`, nothing from tooling.
- Tooling root: contains `scripts/` and this guide, nothing from code.
- Output-base: a fresh directory outside both roots. Each run
  creates a unique `run-<UTC>-<8 hex>` directory inside it and
  never overwrites an older run.

## 2. Git mode (preferred) — complete, separate-line commands

Run each line separately. Do not join commands onto one line.

```bat
git -c core.autocrlf=false clone --branch muse/local-control-room https://github.com/Nohfinl99/Orchestrator-Room.git code
cd code
git checkout <TARGET_CODE_COMMIT>
git rev-parse HEAD
git status --porcelain
```

- `git rev-parse HEAD` must print exactly `<TARGET_CODE_COMMIT>`.
  If it does not, stop. Do not run tests and do not assign the
  result to that commit.
- `git status --porcelain` must print nothing. A dirty tree fails
  preflight (exit 2).
- `core.autocrlf=false` is the line-ending policy: preserve exact
  source bytes. Do not convert line endings, do not run a
  formatter, do not edit a file to make its digest match. If a
  digest mismatches, stop and report it.

Then, from the tooling root (or any directory, with absolute paths):

```bat
<tooling>\scripts\run_windows_tests.bat <code-root> <pinned-manifest> <output-base>
```

Example with placeholders replaced by real values:

```bat
C:\work\tooling\scripts\run_windows_tests.bat C:\work\code C:\work\pinned-c4.json C:\work\windows-runs
```

The pinned manifest is a JSON file with `code_commit`,
`pin_origin`, and `source_digests` (path -> SHA-256). It is the
independent identity for the run. A `--code-commit` string typed
by hand is **not** accepted by runner v2 and is **not** binding.
For C4, use the pinned manifest published in evidence E4
(`evidence/rev4/c4-pinned-manifest.json`); for a future code
commit, use that commit's own published pinned manifest, never
an older commit's manifest.

Direct Python form (same contract, no BAT):

```bat
py -3.14 -X utf8 <tooling>\scripts\run_windows_tests.py --source-root <code-root> --pinned-manifest <pinned-manifest> --output-base <output-base> --mode git
```

## 3. API-snapshot mode — never call it a Git checkout

If the code was materialized through the GitHub file API instead
of Git:

- Write the files as original bytes, exactly as received.
- Do not claim a Git checkout, a HEAD, or a clean tree.
- Use `--mode api-snapshot` (Python form only; the BAT defaults
  to `--mode git` and must not be used for a snapshot).
- The pinned manifest must still be independent and must match
  every source file before tests run, or preflight fails.

```bat
py -3.14 -X utf8 <tooling>\scripts\run_windows_tests.py --source-root <snapshot-dir> --pinned-manifest <pinned-manifest> --output-base <output-base> --mode api-snapshot
```

## 4. Exit codes — child, helper, BAT, reported separately

| Exit | Meaning |
|---|---|
| child (test process) | 0 = suite passed; nonzero = suite failed/errored |
| helper (Python runner) | 0 = pass + counts valid + sources unchanged; 1 = test failure; 2 = preflight failure; 3 = collection/source-change failure |
| BAT launcher | Must equal the helper exit exactly. On helper nonzero, BAT prints no "Done" and exits with that code. |

Report all three when they were all executed. If BAT was not
used (direct Python invocation, as in the C3 reviewer run),
report BAT as NOT_APPLICABLE, not 0. If BAT was not executed
on this platform (Linux, no `cmd.exe`), report BAT as NOT_RUN
and say so; do not claim a BAT result from a static check.

## 5. SKIP cases — report names, not just a count

- A skipped test is NOT_RUN for that subcase, not PASS.
- The manifest lists `skipped_tests` by name. Copy those names
  into the report back.
- Symlink SKIP on Windows (WinError 1314, privilege not held)
  is the expected NOT_RUN for T24 on a machine without that
  privilege. Do not relabel it, do not enable the privilege
  silently to force a pass, and do not hide it.
- Zero discovered tests, a missing `Ran N tests` summary, or a
  count mismatch is a collection failure (helper exit 3), never
  a success, even if the child exit was 0.

## 6. What to send back

Send the whole unique run directory (`test-run.log` +
`manifest.json`, plus `preflight.json` if preflight failed) and
the console output, to Muse in direct chat — not via Telegram.
The report back must include, in this form:

```
Code commit: <from pinned manifest, not typed>
Pin origin: <pinned manifest file + its SHA-256, computed externally>
Mode: git | api-snapshot
Git HEAD (git mode): <rev-parse output, or null>
Python (selected interpreter): <from manifest>
Platform: <from manifest>
Child exit: <n>
Helper exit: <n>
BAT exit: <n | NOT_APPLICABLE | NOT_RUN>
Attempted / Passed / Errors / Failures / Skipped: <n / n / n / n / n>
Skipped tests: <names from manifest, or none>
Log SHA-256: <from manifest>
Manifest SHA-256: <computed externally from the manifest file, not read from inside it>
Run directory: <run-<id>>
Source changed during run: <true/false>
```

## 7. What this guide does not do

- It does not merge, open a PR, or change main.
- It does not change Orchestrator_Reverse.
- It does not activate a chat listener or a real-agent dispatcher.
  The product entry point is the CLI; see `PILOT_RUNBOOK.md`.
- A green suite does not make the system verified. A separate
  reviewer issues the next verdict.
