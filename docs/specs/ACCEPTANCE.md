# Acceptance criteria and review evidence

Muse reports each item as PASS, FAIL, NOT RUN or INCONCLUSIVE and links the exact evidence. Code inspection alone does not satisfy runtime criteria.

## Control room

1. Owner can open the local project room and see stage, task owner, dependencies, blocked reason, next allowed action, evidence count and verification revision.
2. One synthetic observation can be created, saved and reloaded; missing fields remain unknown/null.
3. Observation facts and generated inference are distinct in storage and display.
4. A source locator and optional content hash are retained.
5. Task DONE does not advance product or verification state.
6. Backend rejects illegal state changes and direct agent changes to owner/Judge/verification status.
7. A dependency becoming ready produces an inspectable event; duplicate or stale updates do not silently overwrite newer state.
8. Owner review is bound to a specific record/brief revision with actor, time, decision, reason and evidence.
9. Event history shows before/after state, actor/role, revision and linked evidence.

## Verification truth

10. Incomplete scope, skipped required checks, missing logs, non-zero exit, stale commit or evidence hash mismatch can never display PASS/VERIFIED.
11. Each PASS links to exact commit, criteria revision, test ID, command/steps, environment, raw output/log, exit code and artifact hash.
12. Judge cannot modify code, evidence, or status. Judge output without raw evidence remains INCONCLUSIVE.
13. Changing code after a test invalidates PASS for the new revision until checks are rerun.

## Security and data boundary

14. No provider credentials or network required for the default local workflow; confirm no unexpected outbound request during local checks.
15. Synthetic/redacted data only. No external writes/messages, public repo edits, unrestricted shell, bypass flag or background job.
16. Untrusted prompt-like content cannot change role authority, permission, state, or verdict.
17. Path traversal, out-of-workspace paths, symlink/junction escape, secret files, .git and oversized/binary inputs are refused.
18. Missing/expired permission approval fails closed; no default broad tool permissions.
19. UI status does not imply market validation, production readiness, security certification or live agent orchestration if only a control-plane stub exists.

## Minimum scenarios

- Missing source/observation → NEEDS_EVIDENCE.
- Unknown measured time → remains null; never estimated.
- Synthetic record → facts and inferences remain separate.
- Agent reports task done with missing test log → task may be DONE, verification remains NOT_RUN/INCONCLUSIVE.
- Owner accepts a review revision → audit event identifies exact revision and reason.
- Changed implementation commit with prior PASS evidence → new commit shows Not verified.
- Hostile source text asks the app to set PASS or upload data → no authority/state/network change.
- Restart/reload → project and history remain coherent.

## Evidence format

For every scenario report fixture path and SHA-256, exact command or UI actions, environment, actual output/log path and hash, exit code, timestamp, test ID and status. If a scenario was not executed, mark NOT RUN. Any required failure blocks an overall verification claim until fixed and retested.
