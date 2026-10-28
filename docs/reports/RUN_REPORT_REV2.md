# RUN_REPORT_REV2.md — repair of findings F01–F06 (revision 2)

This report is evidence for implementation commit C only. It does not
rewrite the earlier review verdict. The independent review of 1bba803
verdict was REVISE_REQUIRED, and the overall system stays NOT_VERIFIED
until a new separate reviewer inspects C and its raw evidence and
issues a fresh verdict. Muse's self-run tests below are builder-run
local checks, not independent review.

## Preservation

- The original `RUN_REPORT.md` and `evidence/local-test-run-2026-10-25.log`
  from 1bba803 are preserved unchanged. They are not edited by this
  revision, and they remain historical evidence for the frozen
  1bba803 implementation.
- `MUSE_KNOWLEDGE_RECEIPT.md` is unchanged. Its ten source pins are
  corrected, not replaced, by `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md`
  (in commit C).
- No merge was made. No change was made in `Nohfinl99/Orchestrator_Reverse`.

## Implementation commit C

- Repository: `Nohfinl99/Orchestrator-Room`, branch `muse/local-control-room`
- Base: `1bba80368b5a7dfc75d3b66881ccada6a5252a48`
- Implementation commit C: `d409eca531a202879c2d5bcddc3f9e90794335d3`
- Evidence commit E: this commit, which contains only this report and
  `evidence/rev2/` files. Changing only evidence/docs in E does not
  pretend the tested code was a different implementation; E names C
  and its source digests below.
- Changed paths in C (6 files, verified remote blob SHA = local git blob SHA):
  - `control_room/__init__.py` — version 0.2.0
  - `control_room/backend.py` — schema v2, bound verification, content-bound gates, briefs, review receipts, timestamped hash-chained audit
  - `control_room/cli.py` — atomic compare-and-swap save, aggregate size check, truthful failure reporting, simulation labelling
  - `control_room/README.md` — revision 2 rules and limits
  - `tests/test_control_room.py` — rewritten oracles, including the corrected T10
  - `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md` — new, correcting invalidated application claims
- Unchanged in C, carried from 1bba803: `control_room/__main__.py`,
  `RUN_REPORT.md`, `MUSE_KNOWLEDGE_RECEIPT.md`,
  `evidence/local-test-run-2026-10-25.log`.

## Source digests for C (SHA-256, from the clean checkout)

| Path | SHA-256 |
| control_room/__init__.py | c3d33f52d6aaeee7dc3fe10682b6250bc2f340f42b2780cd4d7fa64cb66021ea |
| control_room/__main__.py | 82d644c5c56a0b05e23ecd9dd2742780c356118cb517148361bdf6ab60874e90 |
| control_room/backend.py | a7df0f57e16c9ddc0bff50bfe1a089d65b40b0e1451aa00713e3eab87ef63eb5 |
| control_room/cli.py | 61d816f4da248513cf65c6ee0537fb50a7d74129afa82d3277b4995858295aad |
| control_room/README.md | 502da4450bc05d0db08e20f188157a71702a2f75301f4e091a4b0c3e78d0aa02 |
| tests/test_control_room.py | 89f9194ccb860a4c1e35c8d09197137d7cade6a34fefb02754018d20973e58d5 |
| MUSE_KNOWLEDGE_RECEIPT_ADDENDUM.md | e7fdf4670487a1a0498036d25021ee4f01ec40da8190257b52b7cf6974e5b8c0 |

## Clean-checkout test run (the run that counts for C)

- Command: `python3 -m unittest discover -s tests -v`
- Run against: a clean checkout of C downloaded via the GitHub API
  (`control_room/` + `tests/` only), verified byte-identical to the
  digests above before running.
- Environment: Python 3.12.3, Linux htch-runtime 7.0.0-39-generic x86_64
- Result: 25 tests run, 25 passed, 0 failed, exit code 0
- Raw log: `evidence/rev2/clean-checkout-test-run-2026-10-25.log`,
  SHA-256 `2d6f3225b3f56683a38d7bb97c753bcf11f4943e6800d3c83cf929fd2a8b65e3`
- Source manifest: `evidence/rev2/clean-checkout-source-digests.json`,
  SHA-256 `55c80113190584259ccd77a61798d8fc5651740aa033ad150ac8ccdc3ae7ef81`
- A pre-commit run in the working directory also gave 25/25, exit 0.
  The clean-checkout run above is the evidence run; the working-dir
  run is not presented as clean-checkout evidence.

## Finding disposition

- **F01 — false PASS (P0), R01/R02: REPAIRED in mechanism, test T10/T10b.**
  Evidence is now a proposal only. `verify()` requires the frozen
  required-case plan (10 cases), complete records, exit code 0,
  command, environment, criteria revision ACCEPTANCE-REV2-1, scope
  completion, timestamp, artifact bytes matching the claimed hash,
  and a judge review receipt whose digest still matches the covered
  records. Forged evidence, nonzero exit, missing artifact, altered
  artifact, missing required case, and unreviewed evidence all yield
  NOT_RUN, INCONCLUSIVE, or FAIL, never PASS. T10 was rewritten:
  the old invented-hash PASS expectation was removed. A verify PASS
  in these tests is a mechanism check only; it does not establish
  independent review and does not validate product or pain.
- **F02 — empty/stale gates (P1), R04/R05: REPAIRED, tests T08/T19/T20/T22.**
  Gates now require a ready observation, a reviewed inference, an
  approved brief with still-matching linked content, and an owner
  decision naming a judge report with findings and per-case results
  whose snapshot content still matches current project content.
  A stale snapshot rejects the decision, records a
  `decision_rejected` event, and leaves the stage unchanged.
  Audit events are excluded from snapshot content, so appending an
  event alone does not invalidate a snapshot. REJECT/DEFER also
  require a judge report and reason, but do not invent positive evidence.
- **F03 — self-asserted role (P1), R03: REPAIRED by labelling, test T21.**
  Per the repair instruction, this is not fixed by blocking a
  same-user CLI (which would be security theatre). Role arguments are
  now labelled simulation only in every privileged output, in
  overview, and in the docs; live adapters stay blocked; no token
  scheme is claimed. The old reproducer expectation that a CLI stage
  change must fail is therefore superseded: T21 asserts the warning
  and the claimed-actor storage, not a false authentication claim.
  Owner/Judge authority must never come from agent-supplied text in
  any real execution interface; none exists in this slice.
- **F04 — persistence (P1), R06/R07: REPAIRED, tests T17/T18.**
  Saves are whole-store compare-and-swap under a lock, with a
  temporary file, fsync, and atomic replace. A stale second writer is
  rejected and the first writer's update is preserved. A failed save
  (fault-injected by patching `os.replace`) leaves the previous bytes
  untouched and reports preservation only after verifying the final
  bytes match the pre-save bytes. The old false "(store unchanged)"
  claim was removed. Schema v1 stores are rejected as superseded
  (T23), with a recreate instruction, not silently migrated.
- **F05 — unbounded records (P2), R08: REPAIRED, test T12.**
  List items are capped at 50, single text fields at 10,000 chars,
  elapsed time must be finite and nonnegative, and the serialized
  store is checked against 1,000,000 bytes before any write, so an
  accepted write can never make the store unreadable under its own
  policy. Oversized, negative-time, non-finite-time, and
  over-limit-list writes are rejected with no state change, and the
  store remains readable afterwards.
- **F06 — audit/reporting overstatement (P2), R09: REPAIRED, tests T09/T16.**
  Events now carry `timestamp_utc`, `content_digest_before/after`,
  `prev_event_digest`, and `event_digest`. `verify-history` checks
  the chain and content continuity and reports tampering (T16).
  Its limit is stated in the output and docs: the chain is NOT
  tamper-proof against the storage owner, who can rewrite history
  and recompute digests.

## Per-subcriterion matrix (builder-run scope only)

| Subcriterion | Result | Test / evidence |
| Overview with stage, blocked reason, next action, owners, evidence count | PASS (builder scope) | T01 |
| Observation save/reload, null elapsed time, readiness | PASS | T02 |
| Facts and inferences kept separate | PASS | T03 |
| Locator and SHA-256 retained | PASS | T04 |
| Task DONE does not advance stage or verification | PASS | T05 |
| Illegal and unauthorised changes rejected, store unchanged | PASS | T06 |
| Dependency-ready event, stale task update rejected | PASS | T07 |
| Full stage path with brief and judge binding | PASS | T08 |
| History before/after, timestamp, digests, chain valid | PASS | T09, T16 |
| Verification: no false PASS (forged, nonzero exit, missing/altered artifact, missing case, unreviewed) | PASS (mechanism) | T10, T10b |
| Hostile text inert | PASS | T11 |
| Path, size, list, and finite-time boundaries; store stays readable | PASS | T12 |
| No network/shell imports in slice code (static string check only) | PASS (static scope only) | T13 |
| Reload coherence | PASS | T14 |
| Non-UTF-8 store rejected | PASS | T15 |
| Audit chain tamper detection | PASS | T16 |
| Stale whole-store writer rejected, first update preserved | PASS | T17 |
| Failed save preserves previous store, truthful report | PASS | T18 |
| Stale judge snapshot rejects and records decision | PASS | T19 |
| Empty artifacts cannot close product path | PASS | T20 |
| Role simulation labelled, live adapters blocked | PASS (labelling scope) | T21 |
| Brief approval invalidates on linked tamper | PASS | T22 |
| Schema v1 rejected as superseded | PASS | T23 |
| Symlink store refused (Linux subcase) | PASS | T24 |
| AC8 timestamp requirement (was PASS with a future-requirement note) | CORRECTED: now implemented and tested | T09 |
| AC10/AC11 verification claims (were contradicted by F01) | CORRECTED: now tied to bound verification, mechanism scope only | T10, T10b |
| AC7 concurrent persistence (was in-memory task test only) | CORRECTED: whole-store CAS test added | T17 |
| AC14 packet-level no-egress | NOT_RUN (see below) | — |
| Windows run, including symlink subcase | NOT_RUN (see below) | — |
| Browser/auth boundary | NOT_RUN, scoped exclusion (no HTTP server in slice) | — |
| Approval timeout, fan-out/concurrency limits, real hardware failure recovery | NOT_RUN | — |
| Independent Judge review | NOT_RUN | — |
| Full pentest | NOT_RUN | — |
| Owner decision on the Rev2 slice | NOT_RUN | — |
| Product/pain validation | NEEDS_EVIDENCE, not validated | — |

## Remaining NOT_RUN / INCONCLUSIVE items (do not hide as passes)

- Independent Judge review of C: NOT_RUN. Only a new separate reviewer
  can issue the next verdict after inspecting C and this evidence.
- Full pentest of C: NOT_RUN.
- Owner decision on the Rev2 slice: NOT_RUN.
- Windows run: NOT_RUN. This environment is Linux. The reviewer run
  on Windows 11 / Python 3.14.4 gave 14 passed, 1 ERROR in T12 because
  symlink creation was refused (WinError 1314). That subcase is
  therefore NOT_RUN on Windows with the actual error recorded, and
  the relevant security claim for Windows symlink handling stays
  unresolved. On Linux, T24 passes (symlink store is refused).
  The Windows run is not claimed, and no Windows result is presented
  as a pass.
- Packet-level no-egress (AC14): NOT_RUN. T13 is a static string
  check only; it does not establish packet-level behaviour.
- Browser/auth boundary: NOT_RUN, scoped exclusion. This slice has
  no HTTP server, so Host/Origin/CSRF have no target here; they are
  not PASS.
- Approval timeout, fan-out/recursion/concurrency resource limits,
  and real hardware failure recovery: NOT_RUN. The CLI has no
  asynchronous approval, and T18 covers only fault-injected atomic
  replacement, not a real disk failure.
- The old reproducer harness `review_checks.py` is not rerun as-is
  against Rev2: its `save_store` call signature changed intentionally
  for compare-and-swap, and its R03 expectation is superseded by the
  labelling repair above. Its invariants were adapted into the new
  tests listed in the disposition, not treated as hidden holdouts,
  and its exit code is never used as a product pass.

## Next atomic task

One task only: a new separate reviewer inspects implementation commit
C `d409eca531a202879c2d5bcddc3f9e90794335d3` and evidence commit E
(this commit) with its raw logs and hashes, and issues the next
independent verdict. Do not rewrite REVISE_REQUIRED as a PASS, do not
merge, and do not extend scope (no UI/provider features) until the
remaining NOT_RUN items above are resolved by that review.
