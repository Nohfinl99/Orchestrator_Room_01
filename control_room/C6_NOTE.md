# C6 — contextual-intake slice (CTX-001)

Scope basis: owner policy recorded in
`docs/requirements/contextual-intake.md` (pin
`0a9729772b4598c771a5b7b49b62e46c8ae47a38` on branch
`codex/ia-context-audit`) and the Muse–Codex channel
`ORCHESTRATOR_CHANNEL.md` on branch `codex/orchestrator-channel`
(CONTROL revision 3, task CTX-001, round 0). This is a new code
revision, not a repin of C5R1 and not a change to C5/E5/E5R1 or
any old evidence. No merge, no PR, no main change, no
Orchestrator_Reverse change. Whole system stays NOT_VERIFIED;
owner product acceptance stays PENDING.

## What C6 adds, in one paragraph

A local, structured, rule-based contextual-intake flow that sits
beside (never replaces) the legacy fixed-template flow:

`intake` (raw, immutable) → `ctx-assess` (keyword heuristic) →
`ctx-add-source` (locator-only provenance) → `ctx-clarify`
(2–3 questions) → `ctx-answer` (verbatim) → `ctx-draft`
(structured rewrite) → `ctx-review-rewrite` (owner gate on the
exact rewrite digest) → `ctx-propose` (contextual proposal bound
to the approved rewrite). A proposal cannot be created before
answers and an APPROVE review of the exact rewrite revision.

## Honest capability boundary (read before claiming anything)

- Assessment is `RULE_HEURISTIC_KEYWORD_SCAN_V1`: English +
  Vietnamese substring matching for goal / context / scope /
  desired_output. It is not semantic understanding, not a model,
  and not natural-language reasoning. A dimension with no keyword
  hit is UNKNOWN, never a guessed fact.
- Draft fields are supplied by the operator through the CLI. The
  system structures them, binds them by digest, and gates them.
  It does not generate goal, context, scope, or desired_output
  from the raw text.
- Context sources record a locator string only
  (`LOCATOR_ONLY_NOT_FETCHED`, `source_sha256: null`). Content
  was not fetched, read, or hash-verified by `ctx-add-source`.
- A rewrite review and a contextual proposal carry provenance
  `OPERATOR_ASSERTED`. That is an audit label, not
  authentication, not owner product acceptance, and not a
  whole-system verdict. Test approvals in fixtures are synthetic;
  they are not a real owner's approval of a real rewrite.
- No provider, worker, chat listener, browser integration,
  scheduler, or network call is added. No live agent dispatch
  exists in this slice, and the channel file itself is not
  evidence of one.
- Optional baseline fields stay null unless supplied elsewhere.
  A missing baseline never blocks clarification, draft, review,
  or proposal in this slice, and no time-saving claim is made.

## Commands

| Command | Gate / effect |
|---|---|
| `ctx-assess --intake-id` | Read-only. Lists dimensions present/missing, suggested questions, method label. Creates nothing. |
| `ctx-add-source --intake-id --source-id --locator --trust-class {owner_statement,reference,external_text} [--note]` | Records a locator-only source for one intake. |
| `ctx-clarify --intake-id --questions Q1 Q2 [Q3]` | Requires exactly 2–3 distinct non-empty questions. Status `WAITING_CLARIFICATION`. Repeat of identical questions returns the existing record, no new event. |
| `ctx-answer --clarification-id --answers A1 A2 [A3]` | Answer count must match question count, all non-empty, stored verbatim. Status becomes `ANSWERED`. |
| `ctx-draft --intake-id --goal --context --scope --desired-output --next-action [--constraints ...] [--unknowns ...] [--inference "LABEL: text" ...] [--clarification-id]` | Refused while a clarification is open, and refused when assessment reports missing dimensions with no answered clarification. Unknowns are operator-supplied only; assessment-missing dimensions are recorded separately as `assessment_missing_at_draft`, not merged into unknowns. Repeat of an identical draft returns the existing rewrite, no new event. |
| `ctx-review-rewrite --rewrite-id --expected-rewrite-digest --decision APPROVE\|REVISE\|REJECT\|DEFER --reason --operator --source` | Format errors: no event, no decision. Digest mismatch or a stored digest that does not recompute: `REJECTED_STALE` event, no decision. Only `APPROVE` enables `ctx-propose`. `REVISE`, `REJECT`, and `DEFER` do not create a proposal. |
| `ctx-propose --intake-id --rewrite-id --expected-rewrite-digest` | Refused (with a `REJECTED_STALE` or `rewrite_not_approved` event) when: rewrite belongs to another intake, digest mismatches, review is not `APPROVE`, a newer rewrite exists, or context changed after approval (new source, clarification, answer, or draft). A repeat of an already-created proposal returns the frozen proposal. |
| `ctx-status --intake-id`, `ctx-rewrite-view`, `ctx-proposal-view` | Read-only. Views recompute digests and flag a stored-digest mismatch instead of hiding it. |

## Binding and stale rules, precisely

- Rewrite id: `RW-` + first 16 hex of SHA-256(canonical rewrite
  payload). Rewrite digest: full SHA-256 of that payload.
  Payload binds intake id, raw SHA-256, goal, context, scope,
  desired_output, constraints, unknowns,
  `assessment_missing_at_draft`, labelled inferences,
  next_action, source ids, clarification id, and the answers
  snapshot. Any change to any of those produces a different
  id/digest, and the old approval does not apply to it.
- Contextual proposal id: `CPROP-` + first 16 hex of the
  approved rewrite digest. Proposal digest: SHA-256 of the
  canonical proposal payload, which embeds the approved rewrite
  id/digest and all draft fields verbatim.
- Stale detection uses a count of context-change events only:
  `ctx_source_added`, `ctx_clarification_created`,
  `ctx_clarification_answered`, `ctx_rewrite_drafted`. A review
  event, a rejected review, and a rejected proposal do not
  count as context changes (counting the review itself would
  make every approval instantly stale).
- History: C6 collections (`context_sources`,
  `clarifications`, `rewrites`, `rewrite_reviews`,
  `contextual_proposals`) are included in `content_digest()`
  when non-empty, same pattern as C5. Empty collections are
  omitted, so pre-C6 stores keep an identical digest and a
  valid history anchor. All C6 mutations go through the CLI
  lock/CAS save, like C5; a tampered history blocks mutation.
- Hostile text: words such as APPROVE, VERIFIED, upload, or
  send inside a raw request, source locator, answer, or draft
  field are stored as data only. They create no review, no
  decision, and no proposal. Only explicit CLI calls with
  matching expected digests can approve or propose.

## Legacy mode, stated plainly

The C5 `propose` / `decide` flow is unchanged. A legacy
proposal is a fixed 4-task template; it does not run
`ctx-assess`, does not require clarification or rewrite
approval, and must never be presented as a contextual
proposal. `ctx-status` reports `legacy_proposal_exists`
separately from `contextual_proposals` for exactly this reason.

## What C6 does NOT prove

Full-scope acceptance, pentest, packet-level no-egress, live
provider/worker integration, runtime knowledge retrieval,
measured owner baseline, owner feedback, product acceptance,
or whole-system verification. Those remain NOT_RUN / PENDING
unless a real run or a real owner decision establishes them.
The acceptance runner in `acceptance/run_acceptance_c6.py`
is builder evidence, not a reviewer verdict.
