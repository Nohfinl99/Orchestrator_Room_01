# IA and proposed architecture

## Product boundary

Orchestrator-Room is the owner's local control room for moving one product-discovery workflow through evidence, hypothesis, owner review and a measured local prototype. It supervises work and evidence; it does not manufacture product truth. The selected pilot is an owner-stated direction, not validated pain.

## Information architecture

Control Room
- Overview: project stage, blocked reason, next permitted action, active tasks, evidence and verification status.
- Projects
  - Product-discovery pilot
    - Intake and observations
    - Evidence ledger
    - Inferences and hypotheses
    - Product brief and prototype plan
    - Tasks and dependencies
    - Judge reviews and owner decisions
- Knowledge: local sources with provenance, rights, revision and applicability.
- Agent profiles: role, allowed capabilities, provider state, limits and last activity.
- Audit: event history and evidence manifest.

Keep the navigation shallow and status visible. Every view should answer: What is known? What is inferred? What is missing? What is the current revision? Who can perform the next action? What evidence supports the state?

## Separate state machines

Product-discovery state: INTAKE → NEEDS_EVIDENCE → HYPOTHESIS_DRAFT → OWNER_REVIEW → ACCEPTED_FOR_LOCAL_PROTOTYPE → JUDGE_REVIEW → OWNER_ACCEPTED / REJECTED / DEFERRED.

Implementation state: NOT_STARTED → IN_PROGRESS → BUILT_PENDING_CHECKS → CHECKS_IN_PROGRESS → PASS / FAIL / NOT_RUN / INCONCLUSIVE.

Task state: TODO / DOING / BLOCKED / DONE. DONE is an agent/owner progress report only. It cannot advance product-discovery or implementation-verification state by itself.

The backend validates legal transitions and required evidence. UI and agent text cannot write a verification status directly. Missing observations, approval, a test output or matching revision keep the project blocked or unverified.

## Minimum record model

Observation: stable ID, schema revision, timestamps, raw goal/problem, steps, actual measured elapsed time or null, blockage/repetition, workaround, outcome/rework, source locator, optional file hash, direct-observation marker and privacy classification.

Inference: candidate pain, user segment, value hypothesis, unknowns, alternative explanations, author/agent, source observation revisions and review status. Never store inference in a fact field.

Evidence: stable ID, type, linked claim/case, target commit/revision, input hash, command or UI procedure, environment, output/log path and hash, exit code, timestamp, collector and reviewer.

Decision event: prior/new state, actor and role, reason, linked evidence, timestamp and event hash. Corrections append a new event instead of rewriting history.

## Runtime flow

1. Capture owner observation locally; unknown values stay null.
2. Build an evidence ledger with source locators and provenance.
3. Keep analyst inferences in a separate block and show unresolved alternatives.
4. Backend blocks any validation claim while required observations, thresholds or review are absent.
5. Owner reviews and approves a hypothesis/brief revision.
6. Builder produces a local synthetic-data prototype within the private repo.
7. Independent Judge receives frozen criteria, commit, fixtures and raw outputs; Judge is read-only.
8. Owner accepts, revises, rejects or defers; event log records the decision.

## Soul, Knowledge, Heart

- Soul: versioned purpose, persona, user profile and interaction principles; guidance only, never authorization.
- Knowledge: local/versioned source material with provenance, rights, date, applicability and retrieval locator.
- Heart: project/task state, evidence, decisions, feedback and append-only event history. Manual/event-driven in v1.

## Local-first security boundary

Bind the control room to loopback. Authenticate each control action. Validate Host and Origin. Do not put long-lived tokens in HTML, URLs, logs or room content. Keep providers off by default. Use per-role capabilities, read-only Judge identity and explicit human approval. Resolve canonical paths and reject traversal, symlink escapes, secret files and writes outside the private workspace. Log decisions without copying secrets. No scheduled background execution in v1.
