# C5R1 acceptance results (builder-run, A01-A33 + variants)

Full-scope verdict: NOT_RUN. Completed required checks: 59/59 PASS.
Total subcases: 63; PASS: 59; FAIL: 0; NOT_RUN: 4; INCONCLUSIVE: 0.
OS: Windows 11; Python: 3.14.4.
Source root: E:\Kiến Trúc Thông Tin\Orchestrator\artifacts\reviews\2026-10-25-c4-roadmap\c5r1-review\source; runner SHA-256: 5a2da9f2f93eb86233be18e77e37780ec4b218527a1a06b65c2c95633a62df7a.

| Case | Subcase | Result | Scope |
|---|---|---|---|
| A01 | golden intake file | PASS | Golden intake from example-request.txt equals expected-intake.json (id, hash, lengths, verbatim text, statements, seconds timestamp). |
| A02 | empty input | PASS | Empty file (0 bytes) is rejected with empty_input; no record. |
| A03 | byte over cap | PASS | Input over the 20,000-byte cap is rejected with byte_cap_exceeded; no record. |
| A03 | char over cap | PASS | Input over the 10,000-char cap is rejected with char_cap_exceeded; no record. |
| A04 | invalid UTF-8 | PASS | Invalid UTF-8 bytes are rejected with invalid_utf8; no record. |
| A05 | baseline six null + provenance | PASS | Golden intake has exactly six null baseline fields with null provenance entries. |
| A06 | duplicate | PASS | Re-submitting identical bytes returns the golden duplicate response, keeps one intake, leaves the original unchanged, and logs duplicate_submission. |
| A07 | statements vs interpretations separate | PASS | Owner statements stay on the intake record; the proposal has no owner_statements field; proposed_interpretations is empty, not invented. |
| A08 | hostile set PASS inert | PASS | Hostile instruction text in an intake is stored as data only: stage stays INTAKE, no decision, binding NOT_RUN. |
| A09 | pasted approval inert | PASS | Pasted approval words in an intake create no decision. |
| A10 | upload/send text inert | PASS | Local scope only: upload/send words in an intake are stored as data, create no new files besides store/lock/input, and no decision. |
| A10 | packet-level no-egress | NOT_RUN | Packet-level no-egress (network capture/audit). NOT_RUN in C5R1; code inspection alone does not prove it. |
| A11 | proposal dependency view | PASS | Initial proposal view tasks and digest match expected-proposal-view.json and the golden digest. |
| A11 | T04 ready next action is decide | PASS | After T01-T03 DONE, T04 READY points at decide with --expected-proposal-digest, --expected-brief-revision, --expected-intake-id from the operator-reviewed snapshot. |
| A12 | restart/reload coherent | PASS | A new process overview after intake/propose/decide shows the same digest and decision, valid history, unchanged store bytes, and counts 1/1/1. |
| A13 | expected-brief mismatch rejection | PASS | A decide with a wrong expected brief (REV1) against the unchanged REV2 proposal is REJECTED_STALE with no decision; the correct REV2 binding still works after. |
| A13 | real changed-brief invalidation | NOT_RUN | A prior approval followed by an actual brief change. NOT_RUN in C5R1; C5 has no brief-editing command. |
| A14 | no auto-PASS | PASS | Completing all proposal tasks plus a C4 task leaves stage INTAKE, binding NOT_RUN, and implementation NOT_VERIFIED. |
| A15 | outside cwd | PASS | An input path outside the cwd is rejected; no record. |
| A15 | symlink | NOT_RUN | A symlinked input file is rejected; no record. If symlink creation itself is unavailable, this subcase is NOT_RUN, not PASS. |
| A15 | .git path | PASS | An input path under .git is rejected; no record. |
| A15 | secret-like filename | PASS | A secret-like input filename is rejected; no record. |
| A15 | binary (invalid UTF-8) | PASS | Binary/invalid UTF-8 input is rejected; no record. |
| A15 | missing file | PASS | A missing input file is rejected; no record. |
| A16 | deterministic proposal, two stores | PASS | Two independent stores from the same golden bytes give the same intake id and proposal digest. |
| A17 | gate only, OPERATOR_ASSERTED | PASS | A role claim in intake text creates no decision; only a matching-binding decide creates one, with provenance OPERATOR_ASSERTED. |
| A18 | immutable intake via correction | PASS | A correction creates a new intake id superseding the golden intake and leaves the old record byte-identical. |
| A19 | golden template four tasks | PASS | A proposal has exactly four tasks and its payload and digest equal expected-proposal.json. |
| A20 | stale decision rejected | PASS | A decide with a stale expected digest (all zeros) is REJECTED_STALE with no decision but a rejection event. |
| A21 | wrong brief | PASS | A decide with a wrong expected brief is REJECTED_STALE with no decision. |
| A21 | wrong intake | PASS | A decide with a wrong expected intake id is REJECTED_STALE with no decision. |
| A22 | knowledge/Soul/Heart honesty | PASS | Two proposals from different intakes share the same template shape, Soul is unchanged, no Reverse authority is cited, and notes state simulated roles only. |
| A23 | byte cap 20,000 accepted | PASS | Exactly 20,000 bytes (10,000 x e-acute) are accepted with lengths 20000/10000. |
| A23 | byte cap 20,001 rejected | PASS | 20,001 bytes are rejected with byte_cap_exceeded. |
| A24 | whitespace-only rejected | PASS | Whitespace-only input is rejected with whitespace_only. |
| A24 | accepted content never trimmed | PASS | LF input with leading/trailing spaces is stored verbatim (text and statements untrimmed, LF endings). |
| A24 | CRLF content never trimmed | PASS | CRLF input with leading/trailing spaces is stored verbatim (text and statements untrimmed, CRLF endings, hash over original bytes). |
| A25 | char cap 10,000 accepted | PASS | Exactly 10,000 chars are accepted. |
| A25 | char cap 10,001 rejected | PASS | 10,001 chars are rejected with char_cap_exceeded. |
| A26 | request-bom.json | PASS | BOM input (bytes decoded from request-bom.json) is rejected with bom_not_accepted; no record. |
| A27 | request-nul.json | PASS | NUL input (bytes decoded from request-nul.json) is rejected with nul_or_binary; no record. |
| A28 | request-crlf.txt | PASS | CRLF fixture: endings, statements, and hash match expected-line-endings.json. |
| A28 | request-mixed.txt | PASS | Mixed-endings fixture: endings, statements, and hash match expected-line-endings.json. |
| A28 | request-bare-cr.txt | PASS | Bare-CR fixture: endings, statements, and hash match expected-line-endings.json. |
| A28 | request-no-newline.txt | PASS | No-newline fixture: endings, statements, and hash match expected-line-endings.json. |
| A29 | unicode combining preserved | PASS | A combining character is preserved verbatim and the hash is over the original bytes. |
| A30 | propose repeat idempotent | PASS | Repeating propose returns the golden repeat response and keeps exactly one proposal. |
| A31 | correction new record, old unchanged | PASS | A correction creates the golden correction id, supersedes the golden intake, leaves the old record hash unchanged, and gives two intakes. |
| A32 | view change does not change digest | PASS | Completing T01 changes the view but not the proposal digest, and a decide with the original digest still works. |
| A32 | payload change invalidates bound decision | PASS | A decide for the golden proposal using another proposal's digest is REJECTED_STALE. |
| A32 | T04 DONE distinct from decision | PASS | Completing T01-T04 leaves T04 DONE pointing at decide with no decision; a decide after that works and then T04 next is None. |
| A32 | decide before all tasks DONE | PASS | A decide with matching bindings succeeds with no task completed; there is no all-tasks-DONE prerequisite. |
| A33 | owner acceptance recorded, not assumed | PASS | Local scope only: C5 creates no owner_product_acceptance field and its decisions are OPERATOR_ASSERTED only. |
| A33 | owner product acceptance | NOT_RUN | Owner product acceptance itself. NOT_RUN / PENDING; it requires a clear owner instruction with source, actor, time, and scope. |
| V01 | missing expected binding flag | PASS | A decide missing --expected-proposal-digest is rejected by argparse with no decision. |
| V02 | wrong-format bindings | PASS | Wrong-format digest, intake id, and decision values are each rejected with format/enum errors and no decision. |
| V03 | correction rejections with events | PASS | Correction no-op, conflict, and supersedes-not-found are each rejected with their own event, and intake count stays two. |
| V04 | concurrent decide, exactly one | PASS | Two concurrent decide processes with a GO barrier persist exactly one golden decision (CAS); scope is the real race result, not code inspection. |
| V05 | stdin intake | PASS | Stdin intake of the golden bytes gives the same intake id with locator local-stdin. |
| V06 | tampered intake fails history | PASS | Tampering intake text without chain recompute makes verify-history chain_valid false with failures. |
| V07 | padded reason verbatim | PASS | A padded reason gives DEC-6a82e87b3bdd26d0 and is stored verbatim; an exact repeat is already_exists; the stripped reason gives a different id; whitespace-only is rejected. |
| V07 | unicode reason verbatim | PASS | A Unicode reason is stored verbatim and its id is recomputed from the verbatim bytes. |
| V08 | legacy Judge scope C4 only | PASS | CLI overview and verify state Judge scope as C4 collections only, with C5 intake/proposal/decision/task status freshness NOT covered; the label is unchanged by C5 ops. |

NOT_RUN / INCONCLUSIVE reasons:

- A10 / packet-level no-egress: NOT_RUN in C5R1; requires packet-level monitoring/audit outside the local CLI, not performed. The PASS subcase above covers only the local command scope.
- A13 / real changed-brief invalidation: NOT_RUN in C5R1; C5 has no brief-editing command, so a prior approval followed by an actual brief change cannot be demonstrated. The PASS subcase above covers only expected-brief mismatch rejection against the unchanged REV2 proposal.
- A15 / symlink: NOT_RUN: symlink creation failed in this environment ([WinError 1314] A required privilege is not held by the client: 'C:\\Users\\Admin\\AppData\\Local\\Temp\\tmp46g8ua1f\\good.txt' -> 'C:\\Users\\Admin\\AppData\\Local\\Temp\\tmp46g8ua1f\\link.txt'); on Windows this is typically WinError 1314 (privilege). The subcase is not counted as PASS.
- A33 / owner product acceptance: NOT_RUN / PENDING: owner product acceptance requires a clear owner instruction with source, actor, time, and scope for the product slice itself. The PASS subcase above covers only that C5 does not self-create acceptance.
