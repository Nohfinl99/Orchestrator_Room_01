# Verification and evidence policy

## Rule

Never report the system or a change as verified, PASS, complete, secure, or working unless the relevant scope is finished and concrete evidence for every required check is available and reviewed. An agent's assertion is not evidence.

## Statuses

- NOT_STARTED: no implementation or run has begun.
- IN_PROGRESS: implementation or verification is incomplete.
- BLOCKED: required input, environment, access or authorization is missing.
- NOT_RUN: the check was not executed.
- INCONCLUSIVE: execution occurred but evidence is incomplete or ambiguous.
- FAIL: evidence shows a criterion did not pass.
- PASS: all required criteria for the declared scope passed with complete evidence.

A project can be complete while one optional test is NOT_RUN only if that test is explicitly outside the declared acceptance scope. The overall security or release claim remains NOT VERIFIED whenever a required security test is missing.

## PASS requirements

Every PASS must point to:

1. Exact repository commit SHA and changed scope.
2. Acceptance-criteria revision and test-case IDs.
3. Exact command/UI steps, OS/runtime/dependency versions and configuration.
4. Actual output or log, exit code, timestamp and artifact path.
5. SHA-256 of the raw evidence artifact and input fixture where relevant.
6. Reviewer identity/role separate from the builder for security and Judge checks.
7. No unresolved failure, blocker or contradictory evidence in the declared scope.

If any required item is missing, report NOT_RUN or INCONCLUSIVE. Do not infer PASS from code reading, a green-looking UI, a successful install, an AI Judge summary, or a completion message.

## Independent Judge

The Judge gets a frozen commit, frozen acceptance criteria, source/evidence locators, and raw outputs. The Judge is read-only and cannot invent missing runs, alter evidence, change implementation, or set owner acceptance. It returns per-case results and findings with evidence. A separate owner decision accepts, rejects or defers the product result.

## UI and report behavior

Display status together with the evidence count and latest verified revision. Show Not verified whenever the code revision has changed since the cited tests or required evidence is absent. Never display a completion badge based only on a task done status. Corrections require a new run and a new evidence record; old FAIL and NOT_RUN history remains visible.
