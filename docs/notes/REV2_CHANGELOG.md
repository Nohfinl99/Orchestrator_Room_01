# REV2 Changelog — brief, short

**Packet revision:** `PRODUCT_INTAKE_BRIEF_REV2` (proposal only,
NOT_APPROVED). This changelog is short by design: it maps each
reviewer finding to a design decision, a file/section, and an
acceptance case. It does not add a general roadmap.

| Finding | Design decision in REV2 | File / section | Acceptance case |
|---|---|---|---|
| BRI01 (P1) — gate promised "only real Owner" but had no command, schema, or authentication | Gate redefined as local operator decision; provenance `OPERATOR_ASSERTED`, never `AUTHENTICATED_OWNER`; `decide` command with APPROVE/REVISE/REJECT/DEFER; decision schema with proposal/brief/intake bindings; stale rejection (`REJECTED_STALE`, event only, no decision); storage-owner full-rewrite limit stated; hostile/pasted approval never a decision; owner product acceptance recorded by source/actor/time/scope, PENDING until a clear instruction exists | Brief REV2 §2; matrix REV2 A17, A20, A21, A33 | A17, A20, A21, A33 |
| BRI02 (P2) — no routing template, rule version, or canonical digest domain; proposal deterministic vs. state view conflated | One fixed template `INTAKE_TEMPLATE_V1` with four tasks, stable IDs, fixed roles/dependencies/reasons; example mapping (capture/inspect → discovery proposal → owner review) is template application, not smart coordination; immutable payload separated from computed view; canonical JSON (sorted keys, `(",", ":")`, UTF-8) and SHA-256 domains; digest excludes digest itself, timestamps, view, and decision fields | Brief REV2 §3; fixtures `expected-proposal.json`, `expected-proposal-view.json` | A19, A32, A11, A16 |
| BRI03 (P2) — duplicate metadata unclear; two intakes could not yield proposal count = 1 | Intake identity on bytes + brief + template version domain; duplicate metadata only in response/event, never in original record; duplicate creates no proposal; propose idempotent (first creates one, repeat returns same); correction is a new record with `supersedes` link, old record unchanged | Brief REV2 §4; fixtures `expected-duplicate-response.json`, `expected-propose-repeat-response.json` | A06, A30, A31, A18 |
| BRI04 (P2) — baseline schema missing six fields; `owner_facts` implied verified facts | Baseline object with exactly six typed/null fields + provenance per field (null → source null; supplied → source `owner` + time + note); `owner_facts` renamed to `owner_statements` (owner-stated claims, not verified facts); owner-stated goal distinguished from unmeasured acceptance threshold; collection template for one redacted workflow, no numbers filled in | Brief REV2 §5.1–§5.3; fixtures `schema.json`, `expected-intake.json`, `collection-template.md` | A05, A07 |
| BRI05 (P2) — bytes/stdin/BOM/newline/Unicode/whitespace/NUL/byte cap not settled | Bytes read first (file or `stdin.buffer`); byte cap 20,000 before decode; strict UTF-8; BOM rejected (not stripped); LF/CRLF/mixed accepted and preserved verbatim; no Unicode normalization; no trimming of accepted content; char cap 10,000 code points; whitespace-only rejected; NUL rejected; hash over original bytes; both lengths recorded | Brief REV2 §5.4; fixtures `request-*.txt`, `request-bom.json`, `request-nul.json` | A01, A03, A04, A23–A29 |
| T3-COV (P3) — parser matrix wording too broad for invalid group | Wording corrected in supplement/status: invalid parser cases in T3 are CRLF only; LF invalid and bare-CR cases are not covered. **No T3 change in this packet; W04 is not reopened.** A future tooling task may add those fixtures separately. | `WINDOWS_SUPPLEMENT_C4_T3.md`; `ROADMAP_STATUS.md` (updated) | — (tooling wording, not a REV2 runtime case) |

## What is NOT in this packet

- No intake code, no `control_room/` change, no test change,
  no T3 script change, no source pin change, no old evidence change.
- No provider, worker, listener, auth server, scheduler, browser,
  or network. No runtime knowledge retrieval. No live-agent coordination.
- No owner decision. Owner decisions still pending:
  1. Approve, revise, reject, or defer `PRODUCT_INTAKE_BRIEF_REV2`
     exactly as written (record source/actor/time/scope if approved).
  2. Supply, or decline to supply, one redacted workflow example
     with frequency, measured manual time/steps/errors, and desired result.
  3. Decide on merge for any branch/commit (no merge/PR authorized here).
  4. Decide on any future worker/browser/provider/chat integration
     (each needs its own brief, trust model, and approval).
