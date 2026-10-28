# Addendum to Product Intake Brief REV2 — Packet Revision REV2.1 (PROPOSED, NOT APPROVED)

**Packet revision:** `REV2.1` (addendum to
`PRODUCT_INTAKE_BRIEF_REV2`, not a replacement of REV2).
**Brief revision for intake identity domain:** unchanged —
`PRODUCT_INTAKE_BRIEF_REV2`. See §1 for why the identity domain
does not change.
**Status:** PROPOSED_NOT_APPROVED. This addendum does **not**
authorize implementation.
**Approval:** No owner approval for REV2.1 has been recorded.
Owner acceptance remains **PENDING**. A review request, a
reviewer verdict, and a local gate decision are **not** owner
acceptance. If the owner approves, record source, actor, time,
and scope; do not require a magic phrase or a single channel.
**Scope of this packet:** checker/schema fix, decision-ingress
contract, newline/correction policy, fixtures, logs, and a C5
checklist. No intake code, no roadmap rewrite, no product scope
expansion.
**Overall system status:** NOT_VERIFIED. W04 remains
CLOSED_SCOPED (in the Windows C4/T3 scope recorded in
`WINDOWS_SUPPLEMENT_C4_T3.md`). T24 remains NOT_RUN
(WinError 1314). Old evidence is unchanged by this packet.

## Status pointer (not a roadmap rewrite)

This addendum does not rewrite `ROADMAP_STATUS.md`. It points
to it and to the existing records, which remain as written:

- `ROADMAP_STATUS.md` — unchanged in this commit.
- `PRODUCT_INTAKE_BRIEF_REV2.md` — preserved; this addendum
  clarifies it, it does not edit it.
- `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md` — preserved;
  runtime cases remain PROPOSED/NOT_RUN; the C5 checklist in
  this packet maps A01–A33 to REV2.1 bindings without editing
  the matrix.
- `WINDOWS_SUPPLEMENT_C4_T3.md` + `evidence/windows-c4-t3/` —
  unchanged; W04 CLOSED_SCOPED, T24 NOT_RUN.
- `evidence/rev4/`, `evidence/tooling-t3/`, `evidence/windows-c3/` —
  unchanged.
- `fixtures/intake-rev2/` — updated in this commit only as
  listed in §5 (checker, schema, new fixtures, new manifest).
  Unchanged golden files keep the same hashes as in the REV2
  manifest (see §5).

## 1. Packet revision decision — why the identity domain does not change

REV2.1 is a packet revision, not a new brief revision for
identity purposes. The intake identity domain
(`original_bytes + 0x00 + "PRODUCT_INTAKE_BRIEF_REV2" + 0x00 +
"INTAKE_TEMPLATE_V1"`) is **unchanged**, because this addendum
changes no intake/proposal payload field, no task, no role, and
no hash formula. It only clarifies:

- how a decision's expected bindings are supplied (§2);
- how the checker enforces the schema (§3);
- how line endings are classified and how derived statements
  are split (§4.1);
- how correction no-op/conflict is rejected (§4.2).

Changing the identity domain for a clarification would
invalidate every REV2 golden ID/digest without changing any
payload semantics, and would force a regeneration that hides
whether the payload actually changed. Therefore REV2 golden
IDs/digests remain valid in REV2.1, and no old evidence is
repinned. **Rule for the future:** if a later packet changes
any payload field, task, role, or hash formula, it must bump
the brief revision in the identity domain, regenerate golden
IDs/digests/manifest consistently, and state the reason in its
changelog. A clarification packet must not do that silently.

## 2. Decision ingress — expected bindings from the operator-reviewed snapshot (R2-01)

REV2 defined a `decide` command but did not give the operator
a way to supply the bindings they reviewed, so an implementation
that silently used the current digest could not be tested for
staleness. REV2.1 closes that gap by choosing **one** ingress:
**CLI required flags**. A decision-file ingress is not chosen
and must not be treated as an alternative in the same build;
if a future packet wants a decision file, it must specify it
separately and state how it differs.

### 2.1 Exact positive command (proposed, not implemented)

The operator first reviews the snapshot in
`fixtures/intake-rev2/operator-reviewed-snapshot.json`
(proposal_id, expected digest, expected brief revision,
expected intake_id, intake hash), then copies those values
into the command — they must not be copied from the current
store by the implementation:

```sh
python3 -m control_room decide --store room.json \
  --proposal-id PROP-INTAKE-96bccfdbe2a16dfc \
  --expected-proposal-digest de30b806df66d4826100ea9e9a17c05408be674686b114b619d382d0204295c6 \
  --expected-brief-revision PRODUCT_INTAKE_BRIEF_REV2 \
  --expected-intake-id INTAKE-96bccfdbe2a16dfc \
  --decision APPROVE --reason "Owner reviewed proposal" \
  --operator "local-operator" --source "local-cli"
```

Expected output for the golden snapshot: decision record
`DEC-e81b5e7deada9801`, provenance `OPERATOR_ASSERTED`,
exit 0. The decision_id formula is unchanged from REV2
(SHA-256 of proposal digest + 0x00 + decision + 0x00 + reason,
first 16 hex chars).

### 2.2 Exact stale command (proposed, not implemented)

Same command, but with an expected digest that does not match
the current proposal payload (for example, an old digest after
the payload changed, or `000…0` in a test):

```sh
python3 -m control_room decide --store room.json \
  --proposal-id PROP-INTAKE-96bccfdbe2a16dfc \
  --expected-proposal-digest 0000000000000000000000000000000000000000000000000000000000000000 \
  --expected-brief-revision PRODUCT_INTAKE_BRIEF_REV2 \
  --expected-intake-id INTAKE-96bccfdbe2a16dfc \
  --decision APPROVE --reason "Attempt with old digest" \
  --operator "local-operator" --source "local-cli"
```

Expected output: `REJECTED_STALE`, exit nonzero, **no**
decision created, and a separate `decision_attempt_rejected`
event recorded with the attempted bindings and the reason.
The implementation must **not** substitute the current digest
for the expected digest, and must **not** upgrade a stale
attempt to an approval.

### 2.3 Missing, wrong-format, or mismatched bindings — reject, never default-approve

- **Missing** any `--expected-*` flag: reject, exit nonzero,
  reason `missing_expected_binding`, no decision, no event
  that looks like a decision.
- **Wrong format:** `--expected-proposal-digest` must be
  exactly 64 lowercase hex characters; `--expected-intake-id`
  must match the `INTAKE-<16 hex>` shape; `--expected-brief-revision`
  must be a non-empty string. Wrong format: reject, exit
  nonzero, reason `invalid_expected_binding_format`, no decision.
- **Mismatched** expected digest, brief revision, or intake_id
  vs. the current proposal payload (digest recomputed from
  the current canonical payload, brief, and intake): reject
  as `REJECTED_STALE` (§2.2), no decision, separate event.
- **Transaction rule for the future build:** the comparison
  of operator-supplied expected bindings against the current
  payload, and the decision write, must happen inside the
  **same CAS/lock transaction** (reusing the C4 lock and
  whole-store CAS pattern). A payload change between the
  comparison and the write must abort the decision, not
  silently apply it to the new payload.

## 3. Checker and schema — actual instance validation (R2-02)

The REV2 checker had a real gap, confirmed by the reviewer:
on temporary copies, `baseline={}` and `decision=EXPLODE`
(with a correctly recomputed ID) still produced 37 PASS, exit 0.
That was a **checker completeness failure, not an application
acceptance PASS** — no intake application exists yet, so no
invalid decision was ever accepted by an application. REV2.1
fixes the checker; it does not claim the old 37 PASS were
schema validation.

### 3.1 What the new checker does

File: `fixtures/intake-rev2/check_static.py` (rewritten for
REV2.1; the old checker log in `evidence/packet-rev2-static-check.log`
is preserved and not overwritten).

- **Validates actual instances** against their named schema
  definitions: intake → `intake_schema`, proposal →
  `proposal_schema`, decision → `decision_schema`. The root
  schema alone validates nothing, and the checker no longer
  only checks that definition names exist.
- **Recursive validation** of required fields, types, enum,
  const, pattern, items, $ref (local definitions only), and
  additionalProperties. Missing fields, wrong types, extra
  properties, and wrong enum/const/pattern values are all
  rejected.
- **Cross-field contract rules** (not in JSON Schema, checked
  separately and explicitly): baseline exactly six fields;
  baseline/provenance consistency (§3.2); intake_id, original
  hash, and lengths recomputed from example bytes; proposal
  digest recomputed from canonical payload; decision_id
  recomputed; decision bindings vs. golden proposal; line-ending
  classification and derived statements (§4.1); duplicate/
  propose-repeat consistency; correction no-op/conflict (§4.2);
  manifest completeness (§3.3).

### 3.2 Baseline and decision rules enforced

- Baseline must have **exactly** the six fields
  (`redacted_example`, `frequency_per_week`,
  `manual_time_minutes`, `manual_steps`, `errors_per_occurrence`,
  `desired_result`), each string-or-null or number-or-null as
  in the schema, with `additionalProperties=false`.
- `baseline_provenance` must have exactly the same six keys,
  each an entry with `source`, `supplied_utc`, and `note`.
  A null baseline value must have provenance source null; a
  non-null value must have provenance source `owner`. A null
  value with an `owner` provenance is a **fake provenance**
  and is rejected. A non-null value without a provenance entry
  is rejected.
- Decision must be one of `APPROVE`, `REVISE`, `REJECT`,
  `DEFER` (no `EXPLODE`, no other value), provenance must be
  `OPERATOR_ASSERTED`, and `decided_utc` is **required** and
  must match the UTC shape `YYYY-MM-DDTHH:MM:SSZ`
  (pattern in the schema). A decision without `decided_utc`
  is rejected.
- `additionalProperties=false` for intake, proposal, and
  decision: an instance with an extra field is rejected, not
  silently accepted.

### 3.3 Validator coverage and limits, stated plainly

- **Implementation:** small validator in `check_static.py`,
  **Python standard library only, no external dependency, no
  network, no runtime service.** Python version for this
  packet's logs: 3.12.3 on Linux (see log headers).
- **Supported JSON Schema keywords:** `type`, `required`,
  `properties`, `additionalProperties`, `enum`, `const`,
  `items`, `pattern`, `$ref` (local `#/definitions/...`
  only). **Any other keyword found in schema.json causes an
  explicit FAIL, not a silent ignore.** Definition names and
  property names are names, not keywords, and are not checked
  as keywords.
- **What the validator does not do:** it is not a full JSON
  Schema engine. It does not support `format`, `allOf`,
  `anyOf`, `oneOf`, `not`, `if/then`, `minLength`,
  `maxLength`, `minimum`, `maximum`, or remote `$ref`. If a
  future schema needs one of those, the checker must be
  extended and its coverage statement updated — the new
  keyword must not be silently ignored.
- **Manifest:** `fixtures/intake-rev2/MANIFEST.json` lists
  **every** file in the fixture bundle (36 files in REV2.1),
  with bytes, SHA-256, and kind (`golden`, `fixture`,
  `negative`, `checker`, `schema`). The manifest excludes
  itself, stated in its note, to avoid a self-reference.
  **Hash match alone is not schema validation:** the checker
  verifies manifest hashes **and** validates golden instances
  against the schema. A file with a correct hash but an
  invalid instance is still rejected.

### 3.4 Negative controls — how rejection is proved

- **Negative bundle:** `fixtures/intake-rev2/negative/*.json`
  (11 files). Each file states its case, record type, malformed
  instance, and expected rejection reason.
- **Per-fixture path:** `python3 check_static.py --validate
  <file> --as <intake|proposal|decision|correction>` exits
  **nonzero** for each malformed fixture. The per-fixture log
  in `evidence/rev2-1/negative-per-fixture.log` records each
  command and its exit (11 exits = 1).
- **Suite path:** `python3 check_static.py --negative` exits
  **0 only if every negative fixture is rejected**, and exits
  nonzero if any negative fixture is accepted (that would be
  a checker bug). The suite log is in
  `evidence/rev2-1/negative-suite.log`. Suite exit 0 means
  "all rejections observed", not "the malformed fixtures are
  valid".
- **Positive path:** `python3 check_static.py` (no arguments)
  validates the golden bundle; log in
  `evidence/rev2-1/positive-check.log`.
- **Counts, kept separate:** positive checks and negative
  probes are counted separately, and neither count is an
  application test count. This packet: **72 positive PASS,
  11 negative probes rejected**. The old 37 PASS figure is
  superseded as a checker metric and must not be quoted as
  schema validation.

| Negative case | What is malformed | Checker must reject by |
|---|---|---|
| baseline-empty | baseline `{}` + provenance `{}` (reviewer probe) | Required keys (six baseline fields) |
| baseline-wrong-type | frequency_per_week = string | Type (number-or-null) |
| baseline-provenance-missing | Non-null baseline value, provenance entry deleted | Cross-field provenance presence |
| baseline-provenance-fake | Null baseline value, provenance source `owner` | Cross-field provenance consistency |
| decision-explode | decision `EXPLODE`, ID recomputed per formula (reviewer probe) | Enum (four values only) |
| decision-missing-decided-utc | No `decided_utc` | Required + pattern |
| decision-wrong-bindings | proposal_digest `000…0` vs. golden digest | Binding cross-check (→ REJECTED_STALE in runtime) |
| intake-missing-field | No `original_sha256` | Required |
| proposal-wrong-type | tasks = string, not array | Type |
| correction-noop | Correction bytes = original bytes, supersedes = original | Correction no-op rule (§4.2) |
| correction-conflict | Bytes already exist, supersedes points elsewhere | Correction conflict rule (§4.2) |

## 4. Edge contract — newline classification and correction conflict (R2-03)

### 4.1 Line endings: finite classification, derived statements only

REV2 said derived statements are "without line endings" but
its checker split on `\n` only, leaving a trailing `\r` on
CRLF lines. REV2.1 closes that with a finite policy:

| Input kind | Classification (`line_endings`) | Derived `owner_statements` | Original bytes/text/hash |
|---|---|---|---|
| Only `\n` breaks | `LF` | Split on `\n`, breaks dropped | Unchanged |
| Only `\r\n` breaks | `CRLF` | Split on `\r\n`, breaks dropped (no trailing `\r`) | Unchanged |
| Only `\r` breaks | `bare-CR` | Split on `\r`, breaks dropped | Unchanged, **not** normalized to LF |
| More than one kind | `mixed` | Split on `\r\n`, `\n`, or `\r` (in that order), breaks dropped | Unchanged |
| No line break at all | `none` | Single statement = whole text (if non-empty and not whitespace-only) | Unchanged |

Rules:

- Classification scans the original text for break sequences:
  `\r\n` counts as one CRLF break, `\n` as LF, `\r` (not
  followed by `\n`) as bare-CR. No break → `none`. More than
  one kind → `mixed`.
- **Derived statements are a view, not a rewrite:** splitting
  for `owner_statements` drops only the break sequence itself.
  It does not change `original_text`, `original_bytes`, or
  `original_sha256`, and it does not normalize bare-CR to LF
  in storage. Empty lines are omitted from the statements list
  only; `original_text` itself is unchanged.
- **Schema:** `line_endings` enum is now
  `["LF", "CRLF", "mixed", "bare-CR", "none"]` (REV2 had only
  LF/CRLF/mixed).
- **Fixtures:** `expected-line-endings.json` covers all five
  kinds (LF example, CRLF existing, mixed, bare-CR, no-newline),
  each with classification, derived statements, hash, and
  lengths recomputed by the checker. Raw files:
  `request-mixed.txt`, `request-bare-cr.txt`,
  `request-no-newline.txt` (new in REV2.1), plus the existing
  `example-request.txt` (LF) and `request-crlf.txt` (CRLF).

### 4.2 Correction: no-op and conflict are explicit rejections

REV2 said a correction is a new record with a `supersedes`
link, but did not settle what happens when the correction
bytes already exist. REV2.1 settles it without changing the
identity scheme and without dropping immutability:

| Correction case | Bytes vs. store | `supersedes` | Outcome |
|---|---|---|---|
| Valid correction | New bytes, not already in store | Points to an existing intake_id | **Accepted:** new record, new intake_id, `supersedes` = old id, old record unchanged. Golden: `expected-correction.json` (`INTAKE-432d09e4f46eaff1` supersedes `INTAKE-96bccfdbe2a16dfc`, from `correction-request.txt`). |
| No-op | Identical to original intake's bytes (so same intake_id) | Points to that same original id | **Rejected:** reason `correction_no_op_same_bytes`, exit nonzero, no new record, no proposal, separate event `correction_rejected_no_op`, original unchanged. |
| Conflict | Identical to an existing intake's bytes (so that intake_id already exists) | Points to a **different** intake_id | **Rejected:** reason `correction_conflict_existing_id`, exit nonzero, no new record, no overwrite, no change to any existing record's `supersedes`, separate event `correction_rejected_conflict`. |
| Supersedes not found | Any bytes | Points to a non-existent intake_id | **Rejected:** reason `correction_supersedes_not_found`, exit nonzero, no new record. |

No case writes into an old record. A view may compute
"superseded" by scanning for records whose `supersedes`
equals an old id, but that computation does not edit the old
record.

## 5. Files changed in this packet (and files deliberately not changed)

**Changed / added in this commit (limited scope):**

- `PRODUCT_INTAKE_BRIEF_REV2_ADDENDUM_REV2_1.md` (this file)
- `C5_IMPLEMENTATION_CHECKLIST.md` (spec for build, not executed)
- `fixtures/intake-rev2/check_static.py` (rewritten validator + modes)
- `fixtures/intake-rev2/schema.json` (root selectors, baseline_provenance,
  decided_utc required + pattern, line_endings enum, additionalProperties=false)
- `fixtures/intake-rev2/operator-reviewed-snapshot.json` (new)
- `fixtures/intake-rev2/expected-correction.json` + `correction-request.txt` (new)
- `fixtures/intake-rev2/expected-line-endings.json` + `request-mixed.txt`,
  `request-bare-cr.txt`, `request-no-newline.txt` (new)
- `fixtures/intake-rev2/negative/*.json` (11 new negative fixtures)
- `fixtures/intake-rev2/MANIFEST.json` (regenerated: 36 files, kinds, hashes;
  unchanged golden files keep REV2 hashes)
- `evidence/rev2-1/positive-check.log`, `negative-suite.log`,
  `negative-per-fixture.log` (new logs for this packet)

**Deliberately NOT changed in this commit:**

- `control_room/`, `tests/test_control_room.py`, T3 scripts,
  `ROADMAP_STATUS.md`, `PRODUCT_INTAKE_BRIEF_REV2.md`,
  `PRODUCT_INTAKE_ACCEPTANCE_MATRIX_REV2.md`, `REV2_CHANGELOG.md`,
  all old evidence (`evidence/rev4/`, `evidence/windows-c4-t3/`,
  `evidence/tooling-t3/`, `evidence/windows-c3/`,
  `evidence/packet-rev2-static-check.log`), and all old source pins.
- No merge, no PR, no main change, no Orchestrator_Reverse change,
  no provider, listener, scheduler, browser, or network.

## 6. Finding status

| Finding | Status after REV2.1 | Positive / negative check | Remaining gap |
|---|---|---|---|
| R2-01 (P1) decision ingress | **CLOSED in contract** (CLI required expected bindings, snapshot, CAS/lock comparison, stale/missing/format rejection) | Positive: snapshot matches golden proposal; stale/negative decision fixtures rejected. Runtime command itself is PROPOSED/NOT_RUN (no intake code yet). | Runtime implementation in C5 must actually enforce §2.3 inside one CAS/lock transaction; a reviewer must test it on a frozen C5 snapshot. |
| R2-02 (P2) checker/schema | **CLOSED in static scope** (instance validation, baseline/provenance, decision enum + decided_utc, manifest completeness, 11 negative rejections) | Positive: 72 PASS, exit 0. Negative suite: 11/11 rejected, exit 0. Per-fixture: 11 exits = 1. | Checker is static, not an application test suite. Application acceptance (A01–A33) remains PROPOSED/NOT_RUN until C5 is built. |
| R2-03 (P2) newline/correction | **CLOSED in contract** (finite line-ending classification, derived statements, correction no-op/conflict/not-found) | Positive: 5 line-ending cases + valid correction recomputed. Negative: no-op and conflict rejected. | Runtime implementation in C5 must enforce the same classification and correction rules on real inputs, including binary/byte-cap paths. |
| W04 | **CLOSED_SCOPED** (unchanged) | Windows C4/T3 supplement, unchanged | None in this packet; do not reopen. |
| T24 | **NOT_RUN** (unchanged, WinError 1314) | Windows supplement, unchanged | Symlink privilege case remains unproven on Windows. |
| Overall system | **NOT_VERIFIED** | — | Full acceptance audit, pentest, owner product acceptance, live-agent/runtime integration remain NOT_RUN/PENDING. |
| Owner approval (REV2.1) | **PENDING** | — | Owner decision on this exact packet scope, recorded by source/actor/time/scope if approved. |

## 7. Approval block (to be filled by a real owner instruction only)

- Packet revision: `REV2.1` (addendum to `PRODUCT_INTAKE_BRIEF_REV2`)
- Owner decision: _[not yet made — PENDING]_
- Owner reason: _[not yet made]_
- Source / actor / time / scope of the instruction: _[not yet made]_
- Scope authorized by approval (if any): _[only the limited scope
  stated in this addendum and the C5 checklist, if the owner writes it here]_
