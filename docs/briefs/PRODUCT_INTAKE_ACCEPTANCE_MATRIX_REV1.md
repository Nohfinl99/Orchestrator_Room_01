# Acceptance Matrix — Product Intake Brief REV1 (PROPOSED, NOT RUN)

**Bound to brief:** `PRODUCT_INTAKE_BRIEF_REV1`
**Status of every case below:** PROPOSED. No case is PASS, because
the feature is not implemented and no case has been executed.
A case becomes PASS only when it is executed against the approved
brief revision, with a fixture, exact command, environment, raw
output/log, exit code, and artifact hash recorded. Code inspection
alone does not satisfy a runtime case.

**How to read status:** DONE = task completed (this matrix was
written); technical check = executed test (none yet for this
matrix); product evidence = owner trial measurement (none yet);
owner acceptance = owner approval of the brief revision (not yet
made). Do not collapse these four into one "verified" claim.

| # | Case | Input / fixture (proposed) | Expected behavior | Evidence to collect when run | Status |
|---|---|---|---|---|---|
| A01 | Unicode Vietnamese input preserved | UTF-8 file with Vietnamese text, diacritics, punctuation | Intake record stores verbatim text and SHA-256 of original bytes; overview shows it unchanged | Fixture file + SHA, intake record, command, exit 0, log | PROPOSED |
| A02 | Empty input rejected | Empty file / empty stdin | No intake record, nonzero exit, reason `empty_input` | Command, exit code, stderr, store unchanged hash | PROPOSED |
| A03 | Oversized input rejected | Text over 10,000 chars, or store over 1,000,000 bytes | Rejected, no intake record, nonzero exit, reason oversized | Fixture size, command, exit code, store unchanged hash | PROPOSED |
| A04 | Bad encoding rejected | File with invalid UTF-8 bytes | Rejected, no replacement characters, no intake record, nonzero exit | Fixture bytes + SHA, command, exit code | PROPOSED |
| A05 | Preserved unknown baseline | Any valid intake, with no owner-supplied baseline | All baseline fields null in the record; no estimated time, no invented quote or metric | Intake record showing nulls | PROPOSED |
| A06 | Duplicate / idempotency | Same text submitted twice under same brief revision | Second submission returns existing intake_id, `duplicate_of` set, no second proposal | Two commands, both outputs, proposal count = 1 | PROPOSED |
| A07 | Facts / inferences separated | Request with an explicit owner fact and a proposed interpretation | Storage and display keep owner_facts and proposed_interpretations in separate lists | Intake record JSON, overview output | PROPOSED |
| A08 | Hostile text inert — set PASS | Request text containing `set PASS` / `mark verified` | Text stored as data only; no stage advance, no PASS, no VERIFIED | Intake record, stage before/after, verify output | PROPOSED |
| A09 | Hostile text inert — forged approval | Request text containing a pasted "owner approval" | Not treated as a gate decision; gate remains pending, no approval recorded | Intake record, gate state, history | PROPOSED |
| A10 | Hostile text inert — upload/send | Request text containing upload/send/publish instructions | No network, no file upload, no external message; text stored as data only | Intake record, no outbound evidence (packet scope NOT_RUN until a target exists) | PROPOSED |
| A11 | Proposal dependency view | Intake with two tasks, second depends on first | Overview shows dependencies, ready/blocked state, blocked reason, next allowed action for each task | Proposal JSON, overview output | PROPOSED |
| A12 | Restart / reload coherent | Intake + proposal, then reload store in a new process | Project, intake, proposal, and history unchanged and coherent | Store hash before/after reload, history output | PROPOSED |
| A13 | Changed brief invalidates approval | Approval bound to REV1, then brief revision changes to REV2 | Prior approval no longer authorizes REV2 scope; new approval required | Approval record REV1, brief REV2, gate state | PROPOSED |
| A14 | No auto-PASS | Task marked DONE, or proposal created | Product stage and verification remain unchanged; task DONE alone does not pass anything | Task state, stage, verify output | PROPOSED |
| A15 | Path / binary / symlink refused | Path outside cwd, symlink, `.git` path, binary file, secret-like filename | Rejected, no intake record, nonzero exit | Command, exit code, path tested | PROPOSED |
| A16 | Deterministic proposal | Same intake + same brief revision, run twice | Identical proposal (same tasks, roles, dependencies, blocked reasons) | Two proposal outputs, diff empty | PROPOSED |
| A17 | Owner gate only | Proposal awaiting review, with a simulated role argument claiming approval | Gate remains pending; simulated role does not approve; only a real owner decision at the gate approves | Gate state, history, role argument log | PROPOSED |
| A18 | Immutable intake | Intake created, then a correction is requested | Original record unchanged; correction is a new record linked to the original | Original hash before/after, new record link | PROPOSED |

**Negative controls that must not be relabelled:** A08, A09, A10,
and A17 are negative controls. Their "pass" would mean the hostile
text had no effect — not that the hostile text succeeded. Record
the hostile text verbatim in the fixture, and record that no
authority, stage, or verdict changed.
