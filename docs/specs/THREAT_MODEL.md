# Threat model for Orchestrator-Room

## Assets

- Raw painpoint observations, private notes and knowledge-source provenance.
- Project hypotheses, decisions, verification artifacts and event history.
- Local repository files, provider credentials and model spend.
- Correctness of gate status: especially PASS/VERIFIED and owner approval.

## Trust boundaries

1. Owner/browser ↔ local control-room server.
2. Hub/state store ↔ UI, Muse/other agents, MCP or future provider adapters.
3. Raw observation/source text ↔ generated analysis and task instructions.
4. Private project workspace ↔ all other filesystem paths and Git repositories.
5. Agent completion claims ↔ independently collected test evidence and Judge verdict.

## Threats and required controls

| Threat | Required control in the first design |
|---|---|
| Prompt injection in a note or imported document changes role/authority | Treat documents as data; backend capability policy is authoritative; test hostile text as inert input |
| Agent claims PASS without running checks | Verification status is derived from evidence records; missing artifact/hash/exit code means NOT RUN or INCONCLUSIVE |
| Agent self-approves its own work | Independent Judge reads a frozen revision and cannot edit evidence or state; owner closes product gate |
| Stolen browser token or cross-site request | Loopback bind, strict Host and Origin checks, short-lived scoped UI session, no long-lived token in HTML/query/referrer, no wildcard CORS |
| Agent or worker accesses secrets/outside workspace | Per-role capability allowlist, canonical path checks, reject traversal and symlink escapes, deny secrets, no arbitrary shell in v1 |
| Provider silently receives local content | Provider adapter disabled by default; explicit per-run consent and visible exact payload/provider; no real data in first slice |
| Task loop, stale assignment or runaway spend | Bounded wake/turn/time/cost limits, idempotent task transitions, cancellation and visible blocked state |
| Concurrent edits or tampered history | Revisioned records, compare-and-swap updates, append-only event log with hashes; failed validation cannot advance state |
| Done is mistaken for verified or pain validation | Separate task, product-evidence and implementation-verification state machines |
| Incomplete checks are reported as successful | Verification policy gates PASS on finished scope and complete, traceable evidence |

## Non-goals for v1

No internet exposure, remote control, real customer data, provider dispatch, background agent sessions, automatic code writes, unattended tool approvals, market-validation claims or security certification. A local UI does not make agent processes sandboxed; the OS/process permission boundary remains part of the threat model.
