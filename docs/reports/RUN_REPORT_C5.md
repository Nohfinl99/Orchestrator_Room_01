# Run Report C5 — thin local intake slice (builder evidence, not a reviewer verdict)

**Code commit C5:** `0a3d5a4d6606f3427b10162671a99adc3ef5b39b` on branch
`muse/local-control-room` (separate from this evidence commit E5).
**Evidence in this commit:** `evidence/c5/` plus this report.
**Overall system status: NOT_VERIFIED. Owner product acceptance:
PENDING. Independent reviewer verdict on the frozen C5/E5 snapshot:
PENDING.**

## Approval record (gate for the build)

- Source: Direct Muse chat, web client.
- Actor: NohFinl (owner).
- Time: 2026-10-25 23:50:52 Asia/Bangkok, by tapping the option
  "Duyệt build C5 theo packet REV2.1 + F21".
- Scope: Build C5 exactly per packet REV2.1 (addendum SHA-256
  `3a3548367f049742865c238e8059ac917f298a546fa8d30e23bbc98b87475520`,
  checklist SHA-256
  `58bec31694e1955fda93d9b2dc71ae7aeeb5951dd7b51ffe1acb75ac99374627`)
  plus checker fix F21 (`bef96ccf3dabda9088491a615eec23cbc8dfe32c`,
  evidence E21 `1e5907658fbe6dd188ef1b8552fa48c053d040a3`).
- Not approved by this record: no merge, no PR, no change to main
  or to Orchestrator_Reverse, no product acceptance, no whole-system
  verification claim. This round pushed only to
  `muse/local-control-room`; no merge or PR was opened.

## Code under test (C5 commit, remote-blob-verified)

| File | Remote blob SHA-1 (matches local) | SHA-256 (local, pre-commit) |
|---|---|---|
| `control_room/__init__.py` | `daa321c6bab298cbc6d478673052dd30da1af47b` | `2c28137567016b68858965e2cb01b5f7ddd98c36fb5581f065fcffdb61d85d01` |
| `control_room/backend.py` | `3dbd45f195edf62136a8e4c2752589bab88979da` | `66cc1dbe8a434dd9a95f493424478568c419d2a644e602c413a15018419605d8` |
| `control_room/cli.py` | `72be482acf956926952075c3fd108f624a479b05` | `86b189645d66381fd586c17fffb032eb69ba8c187205612b8c05709f3f87d4ae` |
| `control_room/README.md` | `4fc1e154b7590b1c9eecb18cbcd9108a94f8df21` | `9d09fa0435d4228d2fd7da2864b0a184e68021a26cfffe1c0269008ae829bcb1` |
| `control_room/C5_BUILD_NOTE.md` | `175478b025d5f0cb016e2d5d59b06dda5e412bde` | `70ca604aac499c9679c8d4826afc06e1820b272e134f50e485b125dd5d51f502` |
| `tests/test_intake_c5.py` | `a7eb2503f73a14e2562c8958e19c9eda2eed388b` | `24e145707882488c59456f6d2afb30ab90162cbc38c11cf313ff60f5573bc91e` |

C4 tests (`tests/test_control_room.py`) are untouched in C5; their
remote blob is unchanged (`9d24da3b65a285f4b1e0b156b00849553ed1bf14`).
Fixtures (`fixtures/intake-rev2/`, manifest SHA-256
`fd1716cb77b93adbe739663a630beb3eb80232dbc463f04cdad631d0c265a39c`)
are unchanged in C5. The acceptance and test runs below were made
against local files byte-identical to the C5 commit blobs above.

## Builder test suite (Linux, Python 3.12.3)

- Command: `PYTHONPATH=. python3 -m unittest
  tests.test_control_room tests.test_intake_c5 -v`
- Log: `evidence/c5/test-suite-c5.log`.
- Result: **54 tests, 54 PASS, 0 FAIL** (36 C4 tests unchanged and
  passing, plus 18 new C5 tests). These are builder-run local checks
  with synthetic fixtures only. They are not an independent review
  and not a pentest.

## Acceptance A01–A33 + variants (builder-run, Linux, Python 3.12.3)

- Runner: `evidence/c5/acceptance-runner.py` (the exact runner used;
  rerun it against a C5 checkout to reproduce).
- Results: `evidence/c5/acceptance-results.json` (per-subcase:
  fixture + SHA-256, exact commands, checks, raw detail) and
  `evidence/c5/acceptance-results.md` (table).
- Result: **53 subcases, 53 PASS, 0 FAIL.** Every A-case passes:
  A01–A33 all PASS, including A15 (6 path subcases), A21 (2 binding
  subcases), A23/A24/A25 (boundary pairs), A28 (4 line-ending
  subcases), A32 (view-change and payload-change subcases), plus
  variants V01 (missing flag), V02 (wrong-format bindings), V03
  (correction rejections with events), V04 (concurrent decide,
  exactly one decision persisted), V05 (stdin intake), V06 (tampered
  intake fails history). No failure was averaged away; a single
  failed subcase would have failed its case.
- Golden identities verified live (not only in fixtures):
  intake `INTAKE-96bccfdbe2a16dfc`, original SHA-256
  `7a1dd7610d07a7407fe6e8558c77433e37dff71a46600c8c1b433695e9d99df3`
  (222 bytes, 165 chars), proposal digest
  `de30b806df66d4826100ea9e9a17c05408be674686b114b619d382d0204295c6`,
  decision `DEC-e81b5e7deada9801` (APPROVE, provenance
  `OPERATOR_ASSERTED`), correction `INTAKE-432d09e4f46eaff1`
  superseding the golden intake.
- Retained golden-flow store: `evidence/c5/golden-flow-store.json`
  (final store SHA-256
  `9e343408acb4deadb99494db69999b142913ef5d9d24608fe1a2b6080c337995`
  after init → intake → duplicate → propose → complete T01 →
  decide; step hashes in `evidence/c5/golden-flow-steps.txt`;
  `verify-history` valid, overview counts 1/1/1, stage INTAKE).
  Acceptance subcase stores were per-subcase temp dirs and are not
  retained individually; per-subcase commands, exits, and golden
  hashes are retained in `acceptance-results.json`, and the retained
  golden-flow store above gives the reviewer a concrete store to
  inspect and re-verify.

## Deliberate deviations flagged for the reviewer (see C5_BUILD_NOTE.md)

1. `complete` command for proposal tasks (checklist names
   `next_allowed_action: complete <task>` and A32 "before/after task
   DONE" but lists no completion command; without one the view is
   static). Strict rules: dependencies must be DONE first, repeat
   reports already_done, completing never changes stage,
   verification, payload, digest, or decisions.
2. DONE view state (readiness DONE, no next action) beyond the
   golden initial view (READY / BLOCKED only).
3. Rejection exit code pinned to 2 (C4 `_fail` convention); the
   checklist says "nonzero exit".
4. Domain record timestamps to the second (schema pattern); C4
   event timestamps (microseconds) kept for audit events.
5. `new_store()` unchanged and `content_digest()` includes C5
   collections only when non-empty, so pre-C5 stores keep a valid
   history anchor and all C4 tests pass unchanged.
6. C5 commands take no `--role`; decide's event actor is the
   `--operator` label. Labels are not authentication.

## What this report does not claim

- No whole-system VERIFIED claim. Implementation verification stays
  NOT_VERIFIED in simulation, as in C4.
- No owner product acceptance: a C5 `OPERATOR_ASSERTED` decision is
  a local gate decision, not product acceptance, and it does not
  move the C4 product stage (which stays INTAKE in a fresh store).
- Baseline remains six null fields; no efficiency or product-value
  claim is made.
- A13 (changed brief) is tested via expected-brief mismatch,
  because C5 has no brief-editing command (see C5_BUILD_NOTE.md).
- A10 (no upload/send) means the local command made no network call
  by construction (no network code in the slice, C4 test_13);
  packet-level egress monitoring remains NOT_RUN.
- Still NOT_RUN / PENDING: independent reviewer verdict on the
  frozen C5/E5 snapshot, reviewer Windows rerun of the F21 checker
  and of C5, full independent C4/C5 acceptance audit, full pentest,
  real disk-failure recovery, live-agent/runtime integration, owner
  product acceptance, and any merge decision.

## Next step for the reviewer

Review the frozen snapshot: code commit C5
`0a3d5a4d6606f3427b10162671a99adc3ef5b39b` plus this evidence
commit E5 (pins to be recorded after push). A reviewer verdict is
not owner acceptance; owner acceptance still requires a clear owner
instruction with source, actor, time, and scope for the product
slice itself.
