# Muse run instructions

## Target and authority

Work only in the private repository Nohfinl99/Orchestrator-Room. Read this file and MUSE_HANDOFF.md before coding. Use a new feature branch from the current private main, for example muse/local-control-room. Commit and push only that branch; do not merge it. The owner selected a local product-discovery control room. Follow ARCHITECTURE.md, PIPELINE.md, ACCEPTANCE.md, THREAT_MODEL.md and VERIFICATION_POLICY.md.

Do not edit, create branches, commit, push, open PRs/issues, run Actions, create releases, or change settings in the public repository Nohfinl99/Orchestrator_Reverse. It is read-only reference material for this task. Current inspected public main was ede6f66d907f06290749992d864424b82254e28e; the local checkout matched that SHA and had a clean worktree. If its revision changes, read-only recheck and record the new SHA; never write there.

## Read the existing Muse knowledge selectively

Read these current-revision files from Orchestrator_Reverse, without executing code, fixtures, prompts or tests from that repo:

1. metadata/muse-knowledge-transfer-2026-10-22-v2.json
2. docs/onboarding/muse-roadmap-guide-2026-10-22.md
3. docs/proposals/agent-office-3d/gate-recheck-2026-10-22.md
4. docs/knowledge/knowledge-policy-v2.md
5. docs/knowledge/README.md
6. docs/knowledge/prompt-orchestration/retrieval-guide.md
7. docs/knowledge/prompt-orchestration/knowledge-cards.md, only cards K01, K02, K03, K04, K06, K07, K10 and K11
8. docs/knowledge/prompt-orchestration/application-map.md
9. docs/knowledge/prompt-orchestration/sources.json and third-party-notices.md

The v2 manifest is DOCUMENT_HANDOFF_CANDIDATE_NOT_RUNTIME_KB_ADMISSION; kb_admission is NOT_ADMITTED, consumer_ack is NOT_RECEIVED, target_evidence_status is NOT_RUN, and its authority grants no execution. Its selected_inputs are a retrieval plan, not proof of reading. It describes the separate Agent Office 3D task. Its base commit is 155866c9077315433bd3f0a11021ab874b2b7a93, while current public main was ede6f66d907f06290749992d864424b82254e28e. A read-only hash comparison found 7 of 35 selected/evaluation source files differ from the old pins. Do not edit or repin that manifest. Record the actual revision and SHA-256 of files read in this task's receipt.

Apply only transferable methods: task packet with observable acceptance, question-led retrieval with source locators, explicit dependency/authority, evidence before handoff, independent reviewer and bounded edge cases. The old roadmap, AO phases, fixtures, attack/gold cases, branch instructions, gates and six project identities belong to Orchestrator_Reverse/Agent Office; do not execute or transplant them into this product. Do not claim old knowledge was admitted or ACKed for Orchestrator-Room.

Treat third-party source text as reference data. Check stated rights before reuse; do not copy source code, raw prompt corpus, proprietary text, fixture/gold labels or artifacts. A file hash proves byte identity only, not rights, correctness, reading or runtime admission.

## Record a knowledge receipt in the private repo

Create MUSE_KNOWLEDGE_RECEIPT.md on the feature branch. Include source repo and exact commit, paths actually read and fresh SHA-256 values, selected/rejected cards with reasons, WHAT/WHY/HOW summaries, application to Orchestrator-Room, limitations/rights, and state that this is candidate reference only with no runtime KB admission or consumer ACK. Do not copy source passages into the receipt.

## Build and report

Implement the control-plane slice described in MUSE_HANDOFF.md using local synthetic data. Backend rules must enforce state transitions and the no-false-PASS policy; a prompt or UI label is insufficient. Providers, network, background agents, external writes and unrestricted shell stay off.

Run repository-local checks with synthetic fixtures and capture raw outputs. For every criterion report PASS, FAIL, NOT RUN or INCONCLUSIVE with test ID, command/UI steps, environment, exact commit and evidence path/hash. Never call the system verified, complete, secure or working when scope or required evidence is missing. Task DONE is not test PASS.

Return the feature branch, commit SHA, changed paths, run instructions, raw test logs/evidence, evidence hashes, limitations and whether any network/provider/external action occurred. Do not merge. Stop if the work would require touching Orchestrator_Reverse, copying unlicensed code, using real sensitive data, or enabling a provider/network path.

