# RUN REPORT — C6R1 bounded fix for CTX-001 (Codex review REV-CTX-001-R0)

- Task: bounded C6R1 fix for review REV-CTX-001-R0 (in reply to
  SUB-CTX-001-R0), findings F01–F03 only, within the
  already-approved CTX-001 scope.
- Work base: `~/workspace/orchestrator-room-work/slice-c6r1/` (copy
  of the frozen C6 snapshot `slice-c6/`; `slice-c6/` was NOT
  modified). Copy verified before work: `backend.py` SHA-256
  `3fe7a8ebcb26b1ee4deed96a2425918f15434073078fd2b81f4711de3397dc5b`
  and `cli.py` SHA-256
  `720266e2ecc17ba9012f78fc2f74d8c1f66d8564694ed3c3103a7073a7bf5c16`,
  both matching the submission pins exactly.
- Nothing was pushed to GitHub. No merge, no PR, no main change,
  no Orchestrator_Reverse change, no credentials, no product
  acceptance claim. Whole system stays NOT_VERIFIED.
- Detail note: `control_room/C6R1_NOTE.md` in the C6R1 tree.

## Environment

- OS: Linux 7.0.0-39-generic x86_64 (runner reports
  `Linux 7.0.0-39-generic`).
- Python: 3.12.3.
- All commands run via the real CLI
  (`python3 -m control_room`, `PYTHONPATH=<slice-c6r1 root>`),
  not unit-logic shortcuts, except the F03 synthetic aggregation
  check which replays the runner's exact frozen assignments.

## Changed files (repo-relative, C6R1 submission tree)

| File | Change | SHA-256 (C6R1 tree) |
|---|---|---|
| `control_room/backend.py` | F01 draft binding + review/propose guards; F02 assess batching | `651eb641af11f5597f363821284d92a35e20c495a516aab3f17cdb3fef1d9b00` |
| `control_room/C6R1_NOTE.md` | New note describing F01–F03 (C6_NOTE.md unchanged) | `71353a2a06901a1d6655245a4c5940d08173152223e172fd82cf02f4d96909aa` |
| `acceptance/run_acceptance_c6.py` | F03 aggregation precedence (`aggregate_full_scope`) | `6559871190760bed6f75769b5028d8304a098275d4e438ef036b0b4c5fc431cb` |
| `tests/test_intake_c6.py` | test_01 (F02 batching) + test_10 (F01 older-draft approval) updated to fixed rules; other C6 tests unchanged | `4c1afe33aac46e461e8306a02ceafb4524e9b78f33ab7c0c142d33706f5a4047` |
| `tests/test_intake_c6r1.py` | New regression file, 10 tests (F01a–e, F02a–d, F03) | `db782eae6e7969ba7dae0634f77f1f779bb154593c3fb512914058464e3bd7d8` |

Unchanged by design (verified by diff against `slice-c6/`):
`control_room/cli.py` (still
`720266e2ecc17ba9012f78fc2f74d8c1f66d8564694ed3c3103a7073a7bf5c16`),
`control_room/__init__.py`, `control_room/README.md`,
`control_room/C6_NOTE.md`, `control_room/C5R1_NOTE.md`,
`control_room/C5_BUILD_NOTE.md`, all fixtures, all C4/C5 tests,
the legacy `propose`/`decide` flow, the C5 acceptance runner.

## Reproduction — before fix (C6 code) vs after fix (C6R1 code)

Full logs: `evidence/c6r1/repro-before-fix.log`,
`evidence/c6r1/repro-after-fix.log`.

### F01a — clarification created after draft, left WAITING_CLARIFICATION

Commands (intake = explicit goal/context/scope/output text):

```
init --store room.json
intake --store room.json --input req.txt
ctx-draft --store room.json --intake-id <IID> --goal G --context C --scope S --desired-output O --next-action N
ctx-clarify --store room.json --intake-id <IID> --questions "Câu hỏi mới 1?" "Câu hỏi mới 2?"
ctx-review-rewrite --store room.json --rewrite-id <RW> --expected-rewrite-digest <DIGEST> --decision APPROVE --reason duyet --operator t --source local-cli
ctx-propose --store room.json --intake-id <IID> --rewrite-id <RW> --expected-rewrite-digest <DIGEST>
```

- Before: review exit 0, propose exit 0 (proposal created despite
  the pending clarification).
- After: review exit 2 (`clarification_open`, no decision),
  propose exit 2, no proposal.

### F01b — source added after draft, before APPROVE

Same intake/draft, then:

```
ctx-add-source --store room.json --intake-id <IID> --source-id SRC-NEW --locator docs/new.md --trust-class reference
ctx-review-rewrite ... --decision APPROVE ...
ctx-propose ...
```

- Before: review exit 0, propose exit 0 with
  `new_proposal_created=true` and proposal `source_ids=[]` while
  current sources were `['SRC-NEW']`.
- After: review exit 2 (`REJECTED_STALE`), propose exit 2. A
  fresh draft after the source binds `['SRC-NEW']`, approves
  (exit 0), and proposes with `source_ids=['SRC-NEW']`
  (test_f01b).

### F02a — raw "hello" (4 missing dimensions)

```
intake (text "hello"); ctx-assess; ctx-clarify with the suggested questions
```

- Before: `dimensions_missing=[goal, context, scope,
  desired_output]`, `suggested_questions` count 4; passing all 4
  to `ctx-clarify` → exit 2.
- After: `dimensions_missing` still all four (diagnostic
  unchanged), `suggested_questions` count 3, dimensions
  `[goal, context, scope]`, note naming `desired_output` for a
  follow-up clarification; passing the new 3-question batch to
  `ctx-clarify` → exit 0 (fresh creation; the logged rerun
  returns the existing clarification under the repeat rule —
  fresh creation is covered by test_f02a).

### F02b — goal/context/scope present, output missing (1 missing)

- Before: `dimensions_missing=[desired_output]`,
  `suggested_questions` count 1; passing it to `ctx-clarify` →
  exit 2.
- After: `suggested_questions` count 2 (desired_output template
  + supplement question about additional constraints/limits/
  unknowns, not a repeat of supplied information); passing the
  new 2-question batch to `ctx-clarify` → exit 0 (same
  fresh-creation note as F02a; fresh creation covered by
  test_f02b).

### F03 — runner full-scope aggregation (synthetic, exact frozen assignments)

- Before: `RESULTS=[FAIL]` → `full_scope=NOT_RUN`, exit 1;
  `RESULTS=[FAIL, NOT_RUN]` → `full_scope=NOT_RUN`, exit 1
  (label wrong, exit already right).
- After (`aggregate_full_scope`): `[FAIL]` → `FAIL`, exit 1;
  `[FAIL, NOT_RUN]` → `FAIL`, exit 1; `[PASS, NOT_RUN]` →
  `NOT_RUN`, exit 2; `[PASS]` → `PASS`, exit 0. Covered by
  test_f03.

## Test results

### Full suite (Linux, Python 3.12.3)

Command: `PYTHONPATH=. python3 -m unittest discover -s tests -v`
from the C6R1 tree. Raw log:
`evidence/c6r1/test-suite-c6r1.log`.

- Attempted: 83. Passed: 83. Failed: 0. Errors: 0. Skipped: 0.
  Not run: 0. Exit: 0.
- Breakdown: `test_control_room.py` 36 (C4, unchanged),
  `test_intake_c5.py` 21 (C5, unchanged), `test_intake_c6.py` 16
  (C6, test_01 + test_10 updated to fixed rules),
  `test_intake_c6r1.py` 10 (new).
- Baseline check: 36 + 21 + 16 = 73 prior tests, plus 10 new
  regressions = 83. No prior test was deleted.
- One intermediate failure during the fix (reported honestly):
  the first full run after the F01 fix failed C6 test_10, which
  approved an older draft after a newer draft existed. That flow
  is stale under F01 (a newer draft is a later context event for
  the older draft, and the older draft could never propose under
  the existing newer-rewrite rule), so test_10 was updated to
  approve only the latest draft and the rule is locked in by
  new test_f01e. Final run: 83/83.

### Acceptance runner (C6R1, B01–B17 unchanged)

Command: `python3 acceptance/run_acceptance_c6.py --source-root
<slice-c6r1> --output-dir <staging>`; results copied to
`evidence/c6r1/acceptance-results.json` and
`evidence/c6r1/golden-flow-store.json`.

- Total subcases: 26. PASS: 24. FAIL: 0. NOT_RUN: 2.
  INCONCLUSIVE: 0. Completed required: 24/24 PASS.
- Full-scope verdict: NOT_RUN. Runner exit: 2.
- The 2 NOT_RUN are the pre-existing B16 scope gaps
  (packet-level no-egress, owner product acceptance) — NOT
  counted as PASS, exactly as in E6. No acceptance case was
  added, removed, or reworded; only the aggregation function
  changed.
- Golden flow store: B01 vague-to-contextual-proposal flow,
  verify-history valid, proposal digest recomputes.

## Per-case table (acceptance, from acceptance-results.json)

| Case | Subcase | Result |
|---|---|---|
| B01 | golden vague intake id and hash | PASS |
| B01 | vague assess WAITING_CLARIFICATION | PASS |
| B01 | golden draft digest recomputes | PASS |
| B01 | proposal before approval refused | PASS |
| B01 | golden contextual proposal after APPROVE | PASS |
| B01 | golden reload coherence | PASS |
| B02 | clear assess COMPLETE | PASS |
| B02 | clear draft still needs review before proposal | PASS |
| B03 | clarify count 2-3 enforced | PASS |
| B04 | answer count must match | PASS |
| B05 | draft blocked while clarification open | PASS |
| B06 | REVISE does not enable proposal | PASS |
| B06 | REJECT does not enable proposal | PASS |
| B06 | DEFER does not enable proposal | PASS |
| B07 | wrong digest review REJECTED_STALE | PASS |
| B08 | source added after approval blocks proposal | PASS |
| B09 | newer rewrite blocks old approved proposal | PASS |
| B10 | different context gives different proposal | PASS |
| B11 | hostile text inert | PASS |
| B12 | legacy proposal is not contextual | PASS |
| B13 | raw unchanged and baseline null | PASS |
| B14 | roundtrip reload coherent | PASS |
| B15 | tampered history blocks ctx mutation | PASS |
| B16 | packet-level no-egress | NOT_RUN |
| B16 | owner product acceptance | NOT_RUN |
| B17 | source trust class and locator-only provenance | PASS |

## Extra verification (not in the suite, reported separately)

- Legacy C6 store compatibility: a store built with frozen C6
  code (draft without `ctx_event_count_at_draft`) was reviewed
  with C6R1 code. After a post-draft source add, APPROVE →
  exit 2 (`REJECTED_STALE`, count reconstructed from event
  history). A clean legacy draft (no post-draft change) still
  approves (exit 0) and proposes
  (`new_proposal_created=true`) under C6R1 code.

## Known gaps / OPEN (unchanged from C6)

- Packet-level no-egress: NOT_RUN (B16).
- Owner product acceptance: NOT_RUN (B16) — test approvals are
  synthetic, not a real owner's approval of a real rewrite.
- Whole system: NOT_VERIFIED. No merge, no PR, no main change.
- C6/E6 snapshots preserved unchanged (`slice-c6/` untouched;
  submission pins above).
- Submission (parent session, 2026-10-26): code commit C6R1
  `c7a837e3538aa6902c24ec4fd3fd8fd1cd047255` on
  `muse/local-control-room` (5 paths, remote git blobs verified
  5/5 against this tree); this report plus `evidence/c6r1/` form
  the separate evidence commit E6R1 (its SHA is recorded in the
  channel submission, not here, because this file is part of that
  commit). Channel submission SUB-CTX-001-R1, in reply to review
  REV-CTX-001-R0, sets the channel to READY_FOR_REVIEW, turn
  CODEX.
- Independent re-run by the parent session (same C6R1 tree, before
  pushing): full suite 83/83 OK; acceptance runner 26 subcases,
  24 PASS, 0 FAIL, 2 NOT_RUN (pre-existing B16 gaps), completed
  required 24/24, full-scope NOT_RUN, runner exit 2; per-case
  results identical to `evidence/c6r1/acceptance-results.json`.
  The re-run golden store differs from the frozen one only by
  timestamps (and digests derived from them); all draft content,
  answers, raw intake hash and case outcomes are identical. The
  frozen evidence files above are therefore kept unchanged.
- The F02 post-fix repro log's second new-batch clarify calls
  return the existing clarification under the repeat rule (the
  first calls created them); fresh creation of the new batches
  is proven by tests test_f02a/test_f02b, not by the rerun lines.

## Evidence files (this directory)

- `RUN_REPORT_C6R1.md` (this file).
- `evidence/c6r1/test-suite-c6r1.log` — raw suite log (83 tests).
- `evidence/c6r1/acceptance-results.json` — runner results.
- `evidence/c6r1/golden-flow-store.json` — B01 golden store.
- `evidence/c6r1/repro-before-fix.log` — pre-fix repro.
- `evidence/c6r1/repro-after-fix.log` — post-fix repro.
- `evidence/c6r1/MANIFEST.json` — SHA-256 manifest (self-excluded).

### Evidence SHA-256

- `acceptance-results.json` (146830 bytes):
  `9d89b21bb96703c5309abe8a684e5fa4e4982d451e413592d163c98c99be72b7`
- `golden-flow-store.json` (15850 bytes):
  `9fb82a65ff401d61ff28ff8372fe34723349b9e3ccfcb149ffdbefb04178051f`
- `repro-after-fix.log` (5777 bytes):
  `0925a9fd808ec0c8a2abbda12f02dc35b319808bb1e850e9d92955a46f9a230f`
- `repro-before-fix.log` (3619 bytes):
  `c36063c089dd892c55ee8472aaedda3373232a6558b72732f4a2af5bf9abdd32`
- `test-suite-c6r1.log` (11469 bytes):
  `316b5249e2fc6a127d5915e551c31f82a6225d3863a51201c36e1a65c4843b18`
