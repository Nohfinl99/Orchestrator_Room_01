# C5R1 — bounded fixes C5-F01..F07 after independent C5/E5 review

C5R1 is a bounded fix revision of the C5 slice, not a new product
feature (not C6) and not a new proposal. It changes only
`control_room/` code, `tests/test_intake_c5.py`, and the acceptance
runner tooling (`acceptance/run_acceptance_c5.py`). It does not
change the C5 commit, the E5 commit, any old log, any fixture,
any C4 test, the packet brief, or the roadmap. The snapshot domain
is deliberately not expanded (see F05).

Scope basis: the owner build approval for C5 (direct Muse chat,
2026-10-25 23:50:52 Asia/Bangkok, scope packet REV2.1 + F21) plus
the independent reviewer instruction
`MUSE_AFTER_C5_REVIEW.md` (reviewer branch
`codex/c5-independent-review`, commit
`e65a5f82f688d72a1b54ee833fefb54c1e4b2209`, verdict
REVISE_C5_BOUNDED), which states that bounded bugfixes inside this
slice do not need a fresh approval round. Product acceptance and
any merge decision remain PENDING and are not claimed here. The
whole system remains NOT_VERIFIED.

## F01 — acceptance evidence truth

The old runner recorded a symlink subcase that could not run as
PASS (a hardcoded check in place of evidence). The C5R1 runner
records PASS / FAIL / NOT_RUN / INCONCLUSIVE per subcase, with a
scope string per subcase and a reason for every NOT_RUN. A
required NOT_RUN blocks a full-scope PASS verdict; completed
checks are reported separately (completed required checks
PASS/FAIL counts) and are never renamed as full-scope PASS.
Runner exit codes: 0 = full scope PASS, 1 = any FAIL,
2 = no FAIL but a required NOT_RUN/INCONCLUSIVE, so the full
scope is NOT demonstrated. All placeholder checks used in place
of evidence were removed; the three former placeholders are now
explicit NOT_RUN subcases (A10 packet-level no-egress, A13 real
changed-brief invalidation, A33 owner product acceptance).

## F02 — byte-defined fixtures and symlink isolation

All intake input files in the C5 tests and in the acceptance
runner are now written with write_bytes, so the bytes asserted
are exactly the bytes written on any OS (text-mode writing
previously converted LF to CRLF on Windows and broke the
no-trim assertions while the application correctly preserved
the actual bytes). LF and CRLF no-trim cases are tested
separately, each with expected text and hash computed from its
own original bytes; the application is not changed to normalize
newlines. Path-boundary subcases keep their own evidence, and
the symlink subcase is isolated: if symlink creation fails
(typically WinError 1314 on Windows), only that subcase is
NOT_RUN, not PASS, and the other A15 subcases still run.

## F03 — reason verbatim

`decide()` validates reason emptiness with `reason.strip()`
(whitespace-only is still rejected), but the stored reason and
the decision_id now use the reason verbatim, with no trimming.
A padded reason `"  same reason  "` gives
`DEC-6a82e87b3bdd26d0` (the contract id); the stripped reason
`"same reason"` gives a different id
`DEC-1e34f4692b242c32`. The unpadded golden reason keeps its
old id `DEC-e81b5e7deada9801`. Tests and acceptance cover
padded, Unicode, exact-repeat, different-reason, and
whitespace-only cases.

Operator/source label policy (stated, not upgraded): `--operator`
and `--source` are audit labels only. They are stripped of
surrounding whitespace for display, they are not part of the
decision_id, and they are not authentication. Nothing in C5R1
turns a label into an authenticated identity; a decision's
provenance remains `OPERATOR_ASSERTED`.

## F04 — T04 review-gate next action

When the Owner review gate task (template T04) is READY, its
`next_allowed_action` now points at the decide command with the
required expected bindings from the operator-reviewed snapshot
(`--expected-proposal-digest`, `--expected-brief-revision`,
`--expected-intake-id`, with actual values), not at completing
the task. When T04 is DONE but no decision exists yet for that
proposal, its next action still points at decide, so task DONE
is never displayed as a gate decision. When a decision does
exist, its next action is None. The `complete` command is kept
as a minimal status mechanism only; completing T04 creates no
decision, changes no stage, and is not approval. Decide has no
all-tasks-DONE prerequisite, as in the golden flow: a
matching-binding decision is allowed at any task state.

## F05 — legacy Judge scope, stated explicitly

`verify()` and `overview()` now carry a `judge_scope` field:
legacy Judge reports and verify snapshots cover C4 collections
only (observations, inferences, briefs, evidence, tasks); they
do not cover C5 intake, proposal, decision, or proposal task
status freshness. `snapshot_digest()` and `judge_report()` are
unchanged, and no old snapshot is repinned or silently
expanded. A C5-specific Judge domain would be separate future
work and is not a blocker for the local pilot. External review
uses the frozen C5R1/E5R1 pins, not the old C5/E5 run, as
evidence for C5R1.

## F06 — coverage split, not renamed

A13 is now two subcases: expected-brief mismatch rejection
(PASS, tested) and real changed-brief invalidation (NOT_RUN,
because C5 has no brief-editing command; no new brief editor
was added). A10 is split the same way: local upload-text
inertness (PASS, local scope only) and packet-level no-egress
(NOT_RUN; code inspection alone does not prove it). A33 is
split into no self-created product acceptance (PASS, local
scope only) and owner product acceptance itself (NOT_RUN /
PENDING). The status table states the scope of each assertion;
no table title claims a broader scope than its subcases cover.

## F07 — runner roots and reproducibility

The runner takes explicit `--source-root` and `--output-dir`.
It auto-detects a source root by walking up from its own file
until it finds `control_room/backend.py` and
`fixtures/intake-rev2/MANIFEST.json`, and it fails clearly if
it cannot. Case commands are recorded with an absolute
`PYTHONPATH=<source-root>` prefix, and the results header
records the source root, the runner path and SHA-256, the
output directory, whether the output directory sits inside the
source root, and an exact reproduce command. The runner writes
its own output manifest (`acceptance-manifest.json`) for its
two result files. Runtime runs local synthetic tests only; no
network, provider, listener, worker, browser, or scheduler is
used, and no unbounded input or text wrapper changes input
bytes (the CLI reads at most 20,001 bytes before decoding).

## Concurrency precision (reviewer note, no code change)

Decide compares expected bindings after loading the store and
then saves under lock with a CAS revision check. The lock is
not held during the comparison; competing writers are rejected
by the CAS check at save time. This is an optimistic
transaction, not a lock-held atomic section, and it is not
claimed otherwise. The competing-writer acceptance case (V04)
and unit test (c5_17) measure the real race result through two
processes, not code inspection alone.

## What is unchanged

- C5 commit `0a3d5a4d...` and E5 commit `18d74aa1...`: untouched.
- Fixtures (`fixtures/intake-rev2/`, manifest SHA-256
  `fd1716cb...`): untouched.
- C4 tests (`tests/test_control_room.py`): untouched.
- Packet brief REV2 / addendum REV2.1, roadmap, and main:
  untouched. No brief or roadmap was written in this round.
- Golden identities: intake `INTAKE-96bccfdbe2a16dfc`,
  proposal digest `de30b806...`, decision
  `DEC-e81b5e7deada9801`, correction
  `INTAKE-432d09e4f46eaff1`: unchanged.
- Rejection events still do not create domain records; a
  duplicate submission still exits 0 with a flag, not a new
  record; the C4 stage machine is unchanged.
