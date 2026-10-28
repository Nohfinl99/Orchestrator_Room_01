# Roadmap Status — Orchestrator-Room (navigable status, not a verdict)

**Overall system status: NOT_VERIFIED.** This document navigates to
evidence; it does not replace evidence, and it does not claim a
complete independent Judge review or pentest. Historical reports
are preserved; this document adds pointers, it does not rewrite them.

**Correction, stated plainly:** an earlier Muse report said Windows
for C4 was NOT_RUN and BAT for C4 was never run. That statement is
now outdated and is corrected here. The reviewer on branch
`codex/roadmap-c4-review` (commit `55cc753cc5eeff2c12c9bf0070277a3151ca928a`)
did run Windows for C4 through BAT v2: 36 attempted, 35 PASS,
1 SKIP, child 0, helper 3, BAT 3, because of W04 (see Findings).
Do not use the outdated NOT_RUN statement for Windows C4/BAT.

## Goals

- Local control-plane foundation for product discovery, owner
  self-use, with backend-owned state, gates, evidence binding,
  and audit history — in progress, bounded CLI scope only.
- Intake from an owner request (local file/stdin) with an
  inspectable task/role/dependency proposal and an explicit owner
  gate — **proposal only** (see Brief, below); not implemented.
- Evidence and discovery with a real owner workflow and baseline
  — not yet demonstrated; baseline values are null.
- Product review and owner decision — pending owner approval of
  the exact brief revision.
- No live orchestration (chat listener, real worker, provider,
  browser, background heartbeat) — not in scope for the current
  slice; a later separate design and authority gate is required.

## Current supported behavior (C4, actually implemented)

- CLI only: init, overview, history, verify-history, observations,
  inferences, briefs, tasks, evidence, judge reports, owner
  decisions, stage transitions with content-bound prerequisites.
- Backend-owned stage machine: INTAKE -> NEEDS_EVIDENCE ->
  HYPOTHESIS_DRAFT -> OWNER_REVIEW -> ACCEPTED_FOR_LOCAL_PROTOTYPE
  -> JUDGE_REVIEW -> OWNER_ACCEPTED / OWNER_REJECTED / OWNER_DEFERRED.
- Audit history anchored to current state, including the G01
  genesis exact-match check. Same-owner full-recompute limit is
  stated, not hidden.
- Binding checks separated from implementation verification:
  binding PASS is structural only; implementation verification is
  NOT_VERIFIED in simulation; verification is never PASS there.
- Role arguments are simulation only, not authentication. Live
  adapters are BLOCKED. A chat message does not start this code.

## Code / tool / evidence pins

| Pin | Commit / hash |
|---|---|
| Room main (frozen docs) | `8bd7d8a9fcdff34ef6ed1626050c2371661ab279` |
| Code C4 | `3d0bf76bab65c37e6b4bed359dfb6dffca7f8f4c` |
| Evidence E4 (C4 Linux) | `d09d75f4b3c3b94dcd8cc9ea982d670ccf7e791b` |
| Tooling T2 (runner v2) | `ee839572d85392020d1f9ec90d1870d7064e3632` |
| Tooling T3 (W04 fix, this turn) | `55bb2f90ee8a4a7a28555059ce122998d6477aa3` |
| Evidence for T3 (this turn) | See `evidence/tooling-t3/` in the T3 evidence commit; log SHA-256 `9e6d9a600ecf27b9ccedb2ddf9f1ed2d1256940d727fad2a1f2a9f662b5b4fa2` |
| C4 Windows supplement (reviewer, roadmap branch) | Branch `codex/roadmap-c4-review`, commit `55cc753cc5eeff2c12c9bf0070277a3151ca928a`; reviewer report blob `40a29915720b73266c77d2493e96bb470f9d83b4`, execution receipt blob `0838fa88e5ae3b5a52b38fc2678ecc503a63a8e4` |
| C4 pinned manifest (E4) | `evidence/rev4/c4-pinned-manifest.json`, SHA-256 `9086c094a5ba575284d6282e5568c50b809c8e2eedbd2d7a96a16e34ff59f901` |
| Windows C4/T3 supplement (reviewer-run, this packet) | `WINDOWS_SUPPLEMENT_C4_T3.md` + `evidence/windows-c4-t3/` (raw log SHA-256 `92c6864b421e70cb7051ee9b2db8676eebe4918f3befb40fd06aa61a3129a9c8`, helper manifest SHA-256 `d2a11733ecc92bef7a23ed35d0081221ab5ed0d41a04f8d9a5a71848d4caa8a1`); reviewer branch `codex/t3-orchestrator-meeting` commit `25ded940fc09145acc034d09da49dc1230c99a4a` |
| Packet REV2 (proposal, this packet) | `PRODUCT_INTAKE_BRIEF_REV2.md`, `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md`, `fixtures/intake-rev2/` (+ `MANIFEST.json`), `REV2_CHANGELOG.md`; brief status PROPOSED_NOT_APPROVED, owner acceptance PENDING |
| Brief REV1 (proposal, this turn) | `PRODUCT_INTAKE_BRIEF_REV1.md`, SHA-256 `fbc881a732178330cad024f4fb7fafa7fcc1defc48a67e3703dd560937b37dbc` |
| Acceptance matrix REV1 (proposal, this turn) | `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV1.md`, SHA-256 `fd526270c3ad2a916937586cfdd08c9fc58d8322c22c4beb8bf8dc3b29cdd6b8` |
| Orchestrator_Reverse knowledge (candidate only) | Revision `ede6f66d907f06290749992d864424b82254e28e`; v2 manifest status `DOCUMENT_HANDOFF_CANDIDATE_NOT_RUNTIME_KB_ADMISSION`, kb_admission NOT_ADMITTED, consumer_ack NOT_RECEIVED, target_pair none |

**Provenance, stated independently:** C4, T3, and the pinned
manifest are named separately and must not be conflated. T3
changes tooling only; it does not change C4, does not repin C4,
and does not make an old run appear green. The C4 pinned
manifest above is the E4 manifest, not a new pin created to
fit T3.

## Roadmap stages

| Stage | Status | Evidence / pointer |
|---|---|---|
| Local control-plane foundation (C4) | DONE (task) / bounded checks PASS on Linux (technical) / product evidence NOT_RUN / owner acceptance NOT_RUN | E4, C4 tests T01–T34 |
| Windows C4 run (reviewer, T2) | DONE (task, reviewer) / tooling FAIL (helper/BAT 3, W04) / product evidence NOT_RUN | Roadmap reviewer report, execution receipt |
| W04 tooling repair (T3) | DONE (task, Linux regressions) / Windows BAT rerun NOT_RUN / owner acceptance NOT_RUN | T3, evidence/tooling-t3/ |
| Intake brief + acceptance matrix + status (REV1) | DONE (task, proposal written) / technical checks NOT_RUN (not implemented) / product evidence NOT_RUN / owner acceptance BLOCKED (pending owner approval of exact REV1) | PRODUCT_INTAKE_BRIEF_REV1.md, acceptance matrix REV1, this document |
| Windows C4/T3 run (reviewer, BAT T3) | DONE (task, reviewer) / W04 CLOSED_SCOPED in that scope / product evidence NOT_RUN / owner acceptance NOT_RUN | `WINDOWS_SUPPLEMENT_C4_T3.md`, `evidence/windows-c4-t3/`; 36 attempted, 35 PASS, 1 SKIP (T24 WinError 1314, NOT_RUN), child/helper/BAT 0/0/0, counts_valid=true; tooling regressions 39 assertion PASS (not C4 tests); T2 FAIL history preserved |
| Intake brief + acceptance matrix + status (REV1) | DONE (task, proposal written) / technical checks NOT_RUN (not implemented) / product evidence NOT_RUN / owner acceptance SUPERSEDED AS PROPOSAL (REV2 now under review; REV1 preserved, not edited) | PRODUCT_INTAKE_BRIEF_REV1.md, acceptance matrix REV1, this document (previous version) |
| Intake packet REV2 (docs/schema/fixtures only) | DONE (task, proposal written) / technical checks NOT_RUN (not implemented) / product evidence NOT_RUN / owner acceptance BLOCKED (pending owner approval of exact REV2, recorded by source/actor/time/scope) | PRODUCT_INTAKE_BRIEF_REV2.md, acceptance matrix REV2, fixtures/intake-rev2/, REV2_CHANGELOG.md |
| Intake implementation | BLOCKED (owner gate: approval of exact REV2 required; REV1 approval no longer the gate, since REV2 supersedes it as the proposal under review) | Brief REV2 §Approval block (empty) |
| Full independent C4 acceptance / pentest | NOT_RUN | — |
| Live orchestration (chat/worker/provider/browser) | NOT_RUN, separate future gate | Brief §6 |

## Findings

| Finding | Status | Scope |
|---|---|---|
| B01–B06 (Rev3) | REPAIRED in C3, retained in C4 | Binding, brief, history, lock, Windows test design |
| F01–F06 (Rev2) | REPAIRED in Rev2/Rev3 scope, retained in C4 | False PASS, stale gates, simulation labelling, CAS, size limits, audit |
| G01 genesis project integrity | REPAIRED in C4; scoped independent review only (8 reviewer controls matched) | Empty-event genesis exact match; not proof against a storage owner who rewrites and rehashes all history; not authentication |
| W01 exit swallowed | REPAIRED in tooling v2 | Failing fixture now child 1, helper 1, BAT propagates |
| W02 commit label not binding | REPAIRED in tooling v2 | Pinned manifest + preflight, git HEAD/clean checks |
| W03 repeatability/metadata | REPAIRED in tooling v2 | Unique run dirs, selected interpreter, ordered stream, authoritative counts |
| W04 CRLF summary parsing | REPAIRED in tooling T3; Windows BAT rerun DONE (reviewer, T3): 36 attempted, 35 PASS, 1 SKIP T24, child/helper/BAT 0/0/0, counts_valid=true; finding CLOSED_SCOPED in that scope (reviewer MEETING.md); T2 FAIL history preserved, not rewritten |
| T3-COV parser matrix wording | CORRECTED in wording only (this packet); invalid parser cases in T3 are CRLF only, LF invalid and bare-CR not covered; W04 NOT reopened, T3 NOT changed in this packet | T2 OK_RE `$` failed on CRLF `OK (skipped=1)\r`; T3 normalizes only an in-memory parsing copy, raw log bytes/hashes preserved; validation not relaxed, exit semantics 0/1/2/3 kept |
| C3 Windows (reviewer) | RECORDED, C3 only | 34 attempted, 33 PASS, 1 SKIP (T24 WinError 1314), child 0, helper 0, BAT NOT_APPLICABLE |
| C4 Windows (reviewer, T2) | RECORDED, C4 only, tooling FAIL | 36 attempted, 35 PASS, 1 SKIP (T24 WinError 1314), child 0, helper 3, BAT 3, W04; suite counts independently read from raw output, not a corrected runner verdict; do not report as "36 passed" or successful |

## Decisions pending (owner only)

1. Approve, revise, reject, or defer `PRODUCT_INTAKE_BRIEF_REV2`
   exactly as written (record source/actor/time/scope if approved).
   REV1 is preserved but is no longer the proposal under review;
   a REV1 approval alone is not a REV2 approval.
2. Supply (or decline to supply) one redacted real workflow
   example, frequency, measured manual time/steps/errors, and
   desired result. Until supplied, all baseline values stay null.
3. Decide on merge for any branch/commit. No merge or PR is
   authorized by this status document.
4. Decide on any future worker/browser/provider/chat integration.
   Each needs its own brief, trust model, and approval.

## Next atomic task

**One task only:** owner review of packet REV2 exactly as
written (brief REV2, matrix REV2, fixtures, changelog, and this
status pointer). Implementation of the intake feature remains
BLOCKED until that approval is recorded with source/actor/time/
scope. After approval, the next build is a thin local slice
exactly per REV2, with code commit C5 and evidence E5 separate,
acceptance cases run, and a new independent reviewer on a frozen
snapshot. The Windows BAT rerun for T3 against clean C4, which
was the previous next atomic task, is now DONE (reviewer-run,
see `WINDOWS_SUPPLEMENT_C4_T3.md`); it is not repeated here.

**Pointers, not rewrites:** `RUN_REPORT.md`, `RUN_REPORT_REV2.md`,
`RUN_REPORT_REV3.md`, `RUN_REPORT_REV4.md`,
`WINDOWS_SUPPLEMENT_C3.md`, `WINDOWS_RUN_GUIDE.md`,
`PILOT_RUNBOOK.md`, `WINDOWS_SUPPLEMENT_C4_T3.md`, `PRODUCT_INTAKE_BRIEF_REV2.md`,
`PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md`, `REV2_CHANGELOG.md`, and the reviewer reports on
`codex/windows-c3-review`, `codex/roadmap-c4-review`, and `codex/t3-orchestrator-meeting` remain
as written. This status document does not edit them.
