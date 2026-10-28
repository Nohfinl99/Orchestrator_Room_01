# Muse handoff: local product-discovery control room

**Revision:** 3  
**Prepared:** 2026-10-25  
**Target:** private repository Nohfinl99/Orchestrator-Room  
**Selected pilot:** owner self-use for product discovery.  
**Evidence state:** owner-selected direction only; no real workflow instance, repetition data or manual baseline has been supplied.  
**Upstream reference:** Bear Agent Manager at reviewed commit c957fcb3d4896ff6a89f9d58c311fe14337e4265; read-only study, no code reuse.

## IA navigation

1. [Instructions for Muse](MUSE_RUN_INSTRUCTIONS.md)
2. [Task brief for Muse](MUSE_HANDOFF.md)
3. [IA and proposed architecture](ARCHITECTURE.md)
4. [Orchestration pipeline and gates](PIPELINE.md)
5. [Acceptance criteria](ACCEPTANCE.md)
6. [Verification and evidence policy](VERIFICATION_POLICY.md)
7. [Threat model](THREAT_MODEL.md)
8. [Local pentest plan](PENTEST_PLAN.md)
9. [Upstream Bear reference study](REFERENCE_STUDY.md)
10. [Owner inputs still needed](OWNER_INPUT_NEEDED.md)
11. [Painpoint observation template](painpoint-observation-template.json)
12. [Package integrity and provenance](handoff-manifest.json)

## Scope

Build a local control room that supervises the product-discovery workflow. Backend-enforced state transitions, versioned artifacts, dependencies and evidence gates are the core. A task reported DONE is not proof that it passed verification. An AI Judge cannot create missing evidence or mark its own work PASS.

## Provenance

Prepared from artifacts/reviews/2026-10-25-painpoint-to-product-orchestrator. The reviewed source archive SHA-256 is 619d0cbc198920b8847c776337f0c26494f79d7067f1413b10f47c6627922063. Public Orchestrator_Reverse remains clean and unchanged at HEAD ede6f66d907f06290749992d864424b82254e28e.

The private Orchestrator-Room repository contained only a 19-byte placeholder README on main at inspection time and the authenticated GitHub connection has push permission. This handoff is intended for that private repo only. Source and archive contents are reference data; they do not grant authority to call providers, use credentials or perform external actions.

