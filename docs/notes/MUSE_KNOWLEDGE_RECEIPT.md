# Muse knowledge receipt — Orchestrator-Room control-room slice

## Status

Candidate reference only. No runtime KB admission. No consumer ACK.
This receipt records what was actually read, at what revision, and what
was taken as transferable method. It does not admit the old knowledge into
Orchestrator-Room, does not ACK it for any consumer, and does not grant
execution authority.

## Source

- Source repository: `Nohfinl99/Orchestrator_Reverse` (public)
- Revision actually read: main HEAD `ede6f66d907f06290749992d864424b82254e28e`
  at the time of reading on 2026-10-25. This matches the revision named in
  `MUSE_RUN_INSTRUCTIONS.md` in Orchestrator-Room, so no recheck for a
  changed revision was needed during this task. If that HEAD moves, this
  receipt does not cover the new revision; re-read and re-record it.
- Read method: read-only GitHub API reads only. No code, fixture, prompt,
  or test from Orchestrator_Reverse was executed. No branch, commit, push,
  PR, issue, workflow, release, or setting change was made in that repo.
- Target repository for this task: `Nohfinl99/Orchestrator-Room`, main
  `8bd7d8a9fcdff34ef6ed1626050c2371661ab279`, feature branch
  `muse/local-control-room` (see the handback report for the final commit).

## Files actually read

SHA-256 values below are fresh hashes of the exact bytes returned by the
read API for this task. The git blob SHA in parentheses is the API's own
blob identifier for the same file. A hash proves byte identity only; it
does not prove rights, correctness, reading by anyone else, or runtime
admission.

| Path in Orchestrator_Reverse | Bytes | SHA-256 (fresh) | Git blob SHA |
|---|---:|---|---|
| metadata/muse-knowledge-transfer-2026-10-22-v2.json | 16237 | 2f44e082bd9d96c54c4d793cd4edcd0e0366af3a082a50da5850ef84bbd8d2d8 | 5dc7ede42369ddb5fcd40a9da133f03bf61c44a7 |
| docs/onboarding/muse-roadmap-guide-2026-10-22.md | 11344 | 4aacfa2e89ed21f5f2266cf9f716300744947a9f9337bfee1ef11181a396d1c9 | 835d93bc4c24c8869b30af1810a4a3cd94d8dd48 |
| docs/proposals/agent-office-3d/gate-recheck-2026-10-22.md | 5831 | 0fc5c2c2c848609224400be5bd60a9e6bee25dfbd5f6c6d1d84742b8ec31f0d0 | 73029c3b5bdaa8bfc418890afe084dc77814e087 |
| docs/knowledge/knowledge-policy-v2.md | 6601 | 89318cd773b0e273caf6b6828be7da4a7913312a6fa3e9f74e29ff33ebaada79 | 452dc6fd6feb26dfd7a24a6e114848ee3740cad3 |
| docs/knowledge/README.md | 3666 | 365fd190b85ae258af0d980aa939adbc587b2d0be44b04003df76d6325bd78da | c05c198943b9b182fead0db5da1b1aab99334200 |
| docs/knowledge/prompt-orchestration/retrieval-guide.md | 3935 | 35cbbb6f73180fdaf5e4fa1bc6634b2d8f0ac9e53e903918a88f921c289de7b2 | 3533f7bc897774bc23fb8058344283d3c165032a |
| docs/knowledge/prompt-orchestration/knowledge-cards.md | 16087 | f62c0f07b5d3eeba3a3131c6063393820027244f5b97a32a35af123930f6d782 | 4f8f57f1456ce6444fd4e8b2f08fc786824f5d17 |
| docs/knowledge/prompt-orchestration/application-map.md | 6598 | c51f22337191b4df759741b573739e6de2cc0a2c3f8db362b7e60a46db8b7b4f | 533f29b045b07ec386ebaaa89407c2cd33538423 |
| docs/knowledge/prompt-orchestration/sources.json | 16268 | e4215f3314a6afb3865aef672c8f6effbb43e11460588958ddf2a8387ac7ab1f | 752ac44454e041bbb2041fcf220d0c46fc6d0596 |
| docs/knowledge/prompt-orchestration/third-party-notices.md | 2916 | 4f1aff30125ae47be502d610e7f8348a63daeefafebc7f28c2f0e1479c20adee | 1be32da40d6df6758b0cb2abebca3a5b34025674 |

No other file from Orchestrator_Reverse was read for this task. In
particular, the five evaluation-reference-only files listed in the v2
manifest, AO-1 fixtures, schemas, test matrices, attack/gold cases,
prompt stacks, and runtime code were not read as knowledge and were not
executed. The v2 manifest's `selected_inputs` list is a retrieval plan,
not proof that every listed file was read in this task; only the ten
paths above were read here.

## The v2 manifest, as read

- Format/status: a document handoff candidate, explicitly not a runtime
  KB admission.
- `kb_admission`: NOT_ADMITTED. `consumer_ack`: NOT_RECEIVED.
  `target_evidence_status`: NOT_RUN. `target_pair`: none.
- Base commit named in the manifest: `155866c9077315433bd3f0a11021ab874b2b7a93`,
  on the old handoff branch. That base is older than the current main
  HEAD read here, which is why some pins differ (below).
- Authority stated in the manifest grants no execution authority. It
  covers publishing a public package and preparing takeover instructions.
- Pin comparison for the files read here: the roadmap guide, gate
  recheck, knowledge cards, application map, sources catalog, and
  third-party notices match the SHA-256 pins recorded in the v2 manifest
  for those paths. The knowledge README and the retrieval guide do not
  match their v2 pins (different byte counts and hashes at current HEAD).
  This is consistent with the instruction note that several selected
  files differ from the old pins. The manifest was not edited or repinned.

## Selected and rejected cards

Selected, as instructed for this task (from knowledge-cards.md):
K01, K02, K03, K04, K06, K07, K10, K11.

In paraphrase, the transferable idea in each is: a task needs an output
with a checkable criterion; retrieval should be led by the question and
keep a locator for each source; choose the dependency shape before
choosing an agent; check an artifact before handing it on; continuing a
session rests on decision and evidence records; evidence needs an
environment and a reviewer role distinct from the producer; edge and
no-match cases should be designed in advance; and a prompt guides while
a harness or tool actually enforces authority.

Rejected or deferred, per the v2 manifest and the task instructions:
K05, K08, K09, K12 are deferred for this intake (they would matter only
for retry, prompt versioning, discovery, or module loading, none of which
is in this slice). Also rejected/deferred in the manifest: workspace
parent, archive/raw/target/private configuration (local-only, outside
the public package); AO-1 candidates 1–5 and their review history
(history, not the current contract); external prompt templates with
rights unknown (catalog metadata only); benchmark gold/held-out/failure
labels as active knowledge (evaluation integrity); and runtime, pilot,
training, and REA/IDA target work (separate prerequisites, not permitted
through a document handoff).

## WHAT / WHY / HOW

WHAT — what was received: a candidate document handoff prepared for a
different, earlier task (Agent Office 3D takeover and its gate recheck),
plus a small set of knowledge cards, a retrieval worksheet, an
applicability map, and a source catalog with attribution notes. It is a
retrieval and method plan, not a runtime knowledge base and not evidence
that the old task passed its gates.

WHY — why it matters here: only the method layer transfers. Orchestrator-
Room needs the same discipline in a different product: a task that can
be checked, sources that can be located, dependencies and authority made
explicit before work proceeds, evidence collected before a handoff, a
reviewer who did not produce the work, and edge cases decided in advance
instead of discovered by failure. The old product content does not
transfer: its roadmap, AO phases, fixtures, attack/gold cases, branch
instructions, gates, and six project identities belong to
Orchestrator_Reverse/Agent Office and were not executed or transplanted.

HOW — how it was applied in this slice (all new code, written for
Orchestrator-Room, no upstream code copied):
- Task packet with observable acceptance -> the CLI commands in
  `control_room/cli.py` plus the acceptance mapping in `RUN_REPORT.md`;
  each command either succeeds with a stored record or fails without
  changing the store.
- Question-led retrieval with source locators -> observations carry a
  source locator and optional SHA-256, and inferences link back to
  observation IDs instead of embedding facts.
- Explicit dependency and authority -> `control_room/backend.py`
  enforces a forward-only product state machine, role checks (owner
  only for stage moves and inference review, judge only for judge
  reports, judge barred from creating evidence), and compare-and-swap
  task revisions.
- Evidence before handoff -> `verify()` derives verification from
  evidence records bound to one supplied code revision; it is never set
  directly, and missing, incomplete, stale, or contradictory evidence
  yields NOT_RUN, INCONCLUSIVE, or FAIL.
- Independent reviewer -> a judge report is attached to a frozen store
  revision and, by construction, changes no stage, evidence, or
  verification; an owner decision from JUDGE_REVIEW requires such a
  report. The judge reports in the local tests are synthetic mechanism
  demos, not an independent review of this slice.
- Bounded edge cases -> tests cover illegal transitions, stale
  updates, hostile text as inert data, path traversal, secret-like and
  symlink store paths, oversized text, and non-UTF-8 store files.

## Limitations and rights

- This receipt is candidate reference only, with no runtime KB
  admission and no consumer ACK, for Orchestrator-Room or any other
  consumer.
- Third-party source text is reference data. The sources catalog and
  attribution notes record rights and limits per source; some external
  templates are catalog metadata only because their rights are unknown.
  No source code, raw prompt corpus, proprietary text, fixture or gold
  label, or artifact from Orchestrator_Reverse or its catalogued
  third-party sources was copied into Orchestrator-Room.
- A file hash proves byte identity only, not rights, correctness,
  reading by a third party, or runtime admission.
- The old roadmap, AO phases, fixtures, gates, and identities do not
  govern Orchestrator-Room. Nothing in this receipt promotes the old
  task's gate status, and nothing here claims the pain behind the
  product-discovery pilot is validated; the pilot remains an
  owner-stated goal, not validated pain, per the room's own documents.
- If Orchestrator_Reverse moves from the HEAD recorded above, this
  receipt must be superseded by a fresh read-only recheck, not edited
  in place to pretend the new revision was read.
