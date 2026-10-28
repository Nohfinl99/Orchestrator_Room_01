# Control-room slice, revision 6 (local, synthetic data only)

Revision 6 (C6, task CTX-001) adds a contextual-intake slice beside
the legacy C5 flow, without changing C4/C5 behaviour: raw intake
→ rule-based keyword assessment → locator-only context sources →
2–3 clarification questions → verbatim answers → structured
rewrite draft → owner review of the exact rewrite digest →
contextual proposal bound to the approved rewrite. See
`control_room/C6_NOTE.md` for the honest capability boundary:
assessment is a keyword heuristic, not semantic understanding;
draft fields are operator-supplied, not generated; a rewrite
review is OPERATOR_ASSERTED, not authentication or product
acceptance. The legacy fixed-template `propose`/`decide` flow
does NOT enforce the contextual policy and must not be presented
as a contextual proposal. C6 evidence lives in the separate
evidence commit E6, never in the code commit.

```sh
python3 -m control_room ctx-assess --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx
python3 -m control_room ctx-add-source --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx --source-id SRC-1 --locator "docs/requirements/contextual-intake.md" --trust-class reference
python3 -m control_room ctx-clarify --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx --questions "Mục tiêu cụ thể là gì?" "Đầu ra mong muốn là gì?"
python3 -m control_room ctx-answer --store room.json --clarification-id CTXQ-xxxxxxxxxxxxxxxx --answers "Theo dõi revision rõ hơn" "Một brief có cấu trúc"
python3 -m control_room ctx-draft --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx --goal "..." --context "..." --scope "..." --desired-output "..." --next-action "..." --clarification-id CTXQ-xxxxxxxxxxxxxxxx
python3 -m control_room ctx-review-rewrite --store room.json --rewrite-id RW-xxxxxxxxxxxxxxxx --expected-rewrite-digest <64 lowercase hex> --decision APPROVE --reason "..." --operator local-operator --source local-cli
python3 -m control_room ctx-propose --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx --rewrite-id RW-xxxxxxxxxxxxxxxx --expected-rewrite-digest <64 lowercase hex>
python3 -m control_room ctx-status --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx
```

## Control-room slice, revision 5 (local, synthetic data only)

Revision 5 (C5, packet REV2.1 + checker fix F21) adds a thin local
intake slice on top of revision 4, without changing C4 behaviour for
pre-C5 stores. See `control_room/C5_BUILD_NOTE.md` for the approval
record, the exact scope, the deliberate additions flagged for the
reviewer (notably the `complete` command for proposal tasks), and
the honest limits. C5 evidence lives in the separate evidence
commit E5, never in the code commit.

Revision 5.1 (C5R1) is a bounded fix revision for findings
C5-F01..F07 from the independent C5/E5 review: reason verbatim
(no trimming in the stored reason or decision_id), the T04
review-gate next action pointing at decide with expected
bindings, legacy Judge scope labelled as C4 collections only,
and acceptance-runner evidence truth, byte-defined fixtures,
and explicit source/output roots. See
`control_room/C5R1_NOTE.md`. C5/E5 commits, fixtures, C4 tests,
brief, and roadmap are unchanged by C5R1.

## C5 intake slice — commands

```sh
python3 -m control_room intake --store room.json --input request.txt
python3 -m control_room intake --store room.json --stdin < request.txt
python3 -m control_room intake --store room.json --input correction.txt --supersedes INTAKE-xxxxxxxxxxxxxxxx
python3 -m control_room propose --store room.json --intake-id INTAKE-xxxxxxxxxxxxxxxx
python3 -m control_room proposal-view --store room.json --proposal-id PROP-INTAKE-xxxxxxxxxxxxxxxx
python3 -m control_room complete --store room.json --proposal-id PROP-INTAKE-xxxxxxxxxxxxxxxx --task-id PROP-INTAKE-xxxxxxxxxxxxxxxx-T01
python3 -m control_room decide --store room.json --proposal-id PROP-INTAKE-xxxxxxxxxxxxxxxx \
  --expected-proposal-digest <64 lowercase hex> --expected-brief-revision PRODUCT_INTAKE_BRIEF_REV2 \
  --expected-intake-id INTAKE-xxxxxxxxxxxxxxxx --decision APPROVE --reason "Owner reviewed proposal" \
  --operator local-operator --source local-cli
python3 -m control_room overview --store room.json
```

Rules: input is read as bytes (at most 20,001 bytes) before decode;
byte cap 20,000, strict UTF-8, BOM rejected (never stripped), NUL,
whitespace-only, and char cap 10,000, in that order. Intake records
are immutable; a correction is a new record with a supersedes link.
A proposal is a fixed four-task template; its view is computed, not
stored, and never changes its digest. A decide is a local operator
gate decision with provenance OPERATOR_ASSERTED only — it is not
owner authentication and not owner product acceptance, and it does
not move the C4 product stage. Rejections exit 2; duplicates and
repeats exit 0 with an explicit flag. Baseline stays six null fields
until an owner supplies values through a mechanism outside C5.

## Control-room slice, revision 4 (local, synthetic data only)

Revision 4 repairs finding G01 from the independent C3 Windows
review, and adds a pilot runbook. See `RUN_REPORT_REV4.md` (in the
evidence commit) and `MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV4.md`.
The original `RUN_REPORT.md`, `RUN_REPORT_REV2.md`, and
`RUN_REPORT_REV3.md` are preserved unchanged as historical evidence
and are not edited by this revision. The C3 Windows supplement is
preserved separately in `WINDOWS_SUPPLEMENT_C3.md` and
`evidence/windows-c3/`; it is not reused as evidence for C4.

Genesis integrity (G01): a store with no events must match the
pristine genesis exactly, in canonical form, including project
configuration (id, room_id, pain_status, soul fields) and every
list, stage and revision. Changing any genesis field without a
chain recompute now fails `verify-history`, and privileged
mutations and proof evaluation remain blocked on an invalid chain.

A control-plane prototype, not live agent orchestration. Python standard
library only, no dependencies, no network, no provider, no background work.

Revision 3 repaired findings B01–B06; see `RUN_REPORT_REV3.md` and
`MUSE_KNOWLEDGE_RECEIPT_ADDENDUM_REV3.md` for that disposition.
The original `RUN_REPORT.md` and `RUN_REPORT_REV2.md` are preserved
unchanged as historical evidence and are not edited by this revision.

## Simulation notice — read first

`--role` is a simulation argument, not authentication. A same-user
process with direct store access can bypass it. Privileged CLI outputs
carry an explicit simulated-authority marker. Live adapters are
blocked. Do not use this CLI for real privileged execution, and do not
claim a token scheme protects a same-user process with storage access.

## Verification semantics, revision 3 — read before quoting a result

`verify` returns two separate results:

- `binding_checks` / `mechanism_result`: structural checks only
  (frozen plan coverage, complete records, exit 0, command,
  environment, criteria, scope, timestamp, artifact bytes matching
  the claimed hash, and a judge receipt whose digest still matches).
  A binding PASS proves only that the supplied records are
  structurally bound.
- `implementation_verification`: always `NOT_VERIFIED` in this
  simulation, because caller-supplied strings and a simulated judge
  receipt do not prove that any command actually ran, that a revision
  corresponds to a real checkout, or that a trusted reviewer examined
  it. The top-level `verification` field is therefore never PASS.

Synthetic positive tests assert `binding_checks`, never an
implementation verification PASS. A real allowlisted local runner
with a concrete trust model would be a separate proposal; arbitrary
shell/provider execution and fake authentication are not added to
satisfy this.

The verification plan is frozen: id
`CONTROL_ROOM_VERIFICATION_PLAN`, revision `REV3-1`, with the ten
required cases in `backend.REQUIRED_VERIFICATION_CASES`. Any
override that is empty, partial, malformed, or does not match the
plan id/revision/digest exactly is rejected before evidence is
checked.

## Run

```sh
python3 -m control_room --help
python3 -m control_room init --store room.json
python3 -m control_room overview --store room.json
python3 -m control_room history --store room.json
python3 -m control_room verify-history --store room.json
python3 -m control_room verify --store room.json --code-revision test-code-revision-v3 \
  --artifact-dir .
```

A full stage path also needs, in order: a ready observation
(trigger, problem and source locator, all non-blank), a reviewed
inference, an approved brief that references a nonempty coherent
graph (ready observations and reviewed inferences linked to those
observations, with actual content still matching the approved
digest), a transition to JUDGE_REVIEW, a judge report with findings
and per-case results, and an owner decision naming that judge report
id. Content added after the judge report invalidates its snapshot
and the decision is rejected and recorded, with the stage unchanged.
A later change to the accepted brief also invalidates later decisions.

## Rules enforced by the backend, not by labels

- Product stage moves only forward along the fixed machine, and only
  by owner (simulated), with content-bound prerequisites as above.
- Task DONE never moves product stage or verification.
- A judge report is read-only in effect: creating it does not change
  stage, evidence, or verification. An empty report cannot support an
  owner decision.
- Observation facts and inferences live in separate lists.
- Unknown values stay null; an unknown elapsed time is never estimated.
  Elapsed time must be finite and nonnegative when present.
- The store file must live inside the current working directory, must
  not be a symlink or under `.git`, and secret-like filenames are
  refused. A serialized store over 1,000,000 bytes is never written.
- Saves are atomic and compare-and-swap on the whole store, under a
  stable OS lock that is never unlinked and is released by the OS on
  process death (fcntl on POSIX, msvcrt locking on Windows). A stale
  second writer is rejected and the first writer's update is preserved.
  A failed save reports truthfully whether the previous store was
  verified preserved or differs. The lock file (`room.json.lock`)
  remains on disk after a write; it is unlocked when no writer holds
  it, and must not be deleted to "recover" a live lock.
- Audit events carry a UTC timestamp, content digests before/after,
  and a hash chain anchored to current state: schema, genesis,
  revision sequence, and the final event's stage, revision and
  content digest must all match the current store. `verify-history`
  checks this anchor. Privileged mutations and proof evaluation are
  blocked on an invalid history; diagnostic reads (overview,
  history, verify-history) remain available. The chain is NOT
  tamper-proof against the storage owner, who can rewrite history
  and recompute digests.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Tests are builder-run local checks with synthetic fixtures only. They
are not an independent Judge review and not a pentest; the overall
system claim therefore stays NOT VERIFIED. See `RUN_REPORT_REV3.md`.
On Windows, symlink creation may fail with a privilege error; that
subcase is skipped in the test and reported NOT_RUN in the report,
never hidden as a pass. Windows tests in Rev3 use in-process calls
for list/aggregate boundaries (no huge subprocess command lines) and
preserve the OS environment for small CLI subprocess smoke checks.
