# RUN_REPORT_C6 — builder evidence for C6 (CTX-001)

Code commit C6: `385f503b003479d4ae957d97cf3657e3900e1a37`
(branch `muse/local-control-room`, separate from this evidence
commit). Evidence commit E6 is the commit that adds this report
plus `evidence/c6/`; its SHA is recorded in the channel
submission, not here, because this file is part of that commit.

Scope: contextual-intake slice per
`docs/requirements/contextual-intake.md` (pin
`0a9729772b4598c771a5b7b49b62e46c8ae47a38`) and channel task
CTX-001, round 0. Changed code paths only: `control_room/`
(backend.py, cli.py, C6_NOTE.md new, README.md),
`tests/test_intake_c6.py` (new),
`acceptance/run_acceptance_c6.py` (new). No C4 test, no C5 test,
no fixture, no brief, no roadmap, and no old evidence file was
changed. C5R1/E5R1 pins are not repinned as C6 evidence.

## What was built

Local, structured, rule-based contextual intake beside the
legacy flow: raw immutable intake → keyword-heuristic assess →
locator-only context sources → 2–3 clarification questions →
verbatim answers → structured rewrite draft → owner review of
the exact rewrite digest → contextual proposal bound to the
approved rewrite. Assessment is a keyword scan, not semantic
understanding; draft fields are operator-supplied, not
generated; a rewrite review is OPERATOR_ASSERTED, not
authentication or product acceptance. See
`control_room/C6_NOTE.md` for the full boundary.

## Test suite (Linux, Python 3.12.3)

Command: `PYTHONPATH=. python3 -m unittest
tests.test_control_room tests.test_intake_c5 tests.test_intake_c6 -v`

Result: 73/73 OK — 36 C4 + 21 C5 + 16 C6, 0 FAIL, 0 ERROR.
Log: `evidence/c6/test-suite-c6.log` (10,285 bytes, SHA-256
`58ab153a2334d9b7815d5d61e4068822ac7b45d87627114a556aee2b779e8412`).
Legacy C4/C5 tests pass unchanged on C6 code; C6 adds 16 tests
and changes no legacy test.

## Acceptance (builder-run, B01–B17)

Command (from outside the checkout):
`python3 acceptance/run_acceptance_c6.py --source-root <C6 root>
--output-dir <output dir>`; runner SHA-256
`ea5eb7329d3f8aabe1f20bb781e47a319549a5cf7cf72670fff689ceed4a0024`;
OS Linux 7.0.0-39-generic; Python 3.12.3; runner exit 2.

Result: 26 subcases — 24 PASS, 0 FAIL, 2 NOT_RUN.
Completed required checks: 24/24 PASS. Full-scope verdict:
NOT_RUN (not PASS), because two required subcases are
explicitly NOT_RUN and are never merged into PASS:

- B16 packet-level no-egress: NOT_RUN (no packet capture run;
  code inspection alone does not prove it).
- B16 owner product acceptance: NOT_RUN (test approvals are
  synthetic; no real owner decision for a real rewrite).

Per-case table: `evidence/c6/acceptance-results.md`; raw CLI
stdout/stderr for every invocation:
`evidence/c6/acceptance-results.json`.

## Golden flow (synthetic, from the acceptance run)

- Intake `INTAKE-62bc3c29d0f60a68`, raw SHA-256
  `f358ebb324cd8ee57f0492fc674c3e31fba295f2f076b02de2251139a316d5ad`
  (vague synthetic text, 82 bytes).
- Rewrite `RW-d30e3de4ad279a1e`, digest
  `d30e3de4ad279a1e97bdf17e43cd3c601410d6640b2b83e74745034f01a8bbbe`,
  review `CTXR-2b010956b06e406e` (APPROVE, OPERATOR_ASSERTED,
  test operator label only).
- Contextual proposal `CPROP-d30e3de4ad279a1e`, digest
  `6d8881856544f9675717d24a51cae9ebdc6669f218f7b72edd783956e8d7f0a8`.
- Store: 7 events, revision 7, verify-history chain_valid true,
  stage INTAKE, baseline all null.
- Files: `evidence/c6/golden-flow-store.json` (SHA-256
  `42df2ddf4785031994b6499d861cf82d7de601918e9f5d10f24caac2603118cd`),
  `golden-flow-verify-history.json`, `golden-flow-ctx-status.json`,
  `golden-flow-steps.txt`.

## Known gaps (unchanged by C6)

Full pentest, packet-level egress, live provider/worker/chat
integration, runtime knowledge retrieval, measured owner
baseline, owner feedback, product acceptance, and merge.
Whole system: NOT_VERIFIED. This report is builder evidence
only; it is not a reviewer verdict and not owner acceptance.
