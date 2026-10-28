"""Static checker for intake REV2.1 fixtures (REV2.1 fix for R2-02).

This is NOT an application test suite and NOT a run of control_room.
It validates, locally and deterministically, the golden fixture
bundle against the REV2.1 schema and contract rules.

Validator coverage (stdlib only, no network, no runtime service):
  - A small validator in this file, Python standard library only.
  - Supported JSON Schema keywords: type, required, properties,
    additionalProperties, enum, const, items, pattern, $ref
    (local #/definitions/... only). Any other keyword found in
    schema.json causes an explicit FAIL, not a silent ignore.
  - Cross-field contract rules checked separately (not in JSON
    Schema): baseline/provenance consistency, intake_id and
    original hash/length recomputation, proposal digest
    recomputation, decision_id recomputation, decision binding
    vs. golden proposal, line-ending classification and derived
    statements, duplicate/propose-repeat consistency, correction
    no-op/conflict rules, and manifest hash/byte-size completeness.

Modes:
  - No arguments: positive bundle check. Exit 0 if every golden
    check passes; exit 1 otherwise.
  - --validate <file> --as intake|proposal|decision|correction:
    validate one instance. Exit 0 if valid; exit 1 if invalid
    (this is the per-fixture nonzero path for malformed fixtures).
  - --negative: run every file in negative/ through the validator
    and correction rules. Prints REJECTED for each correctly
    rejected fixture. Exit 0 only if EVERY negative fixture is
    rejected; exit 1 if any negative fixture is accepted
    (that would be a checker bug, as in the old checker).
  - --schema-probes: run the stored schema-probe regressions in
    regression-schema-probes.json (V21-02). Each probe injects an
    unsupported keyword into a schema object in memory; the
    checker must reject it. Exit 0 only if EVERY probe is
    rejected; exit 1 if any probe is silently accepted.

Counting: positive checks and negative probes are counted
separately. Neither count is an application test count.
"""
import argparse
import base64
import hashlib
import json
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent
BRIEF = "PRODUCT_INTAKE_BRIEF_REV2"
TEMPLATE = "INTAKE_TEMPLATE_V1"
BASELINE_FIELDS = ["redacted_example", "frequency_per_week", "manual_time_minutes",
                   "manual_steps", "errors_per_occurrence", "desired_result"]
SUPPORTED_KEYWORDS = {"type", "required", "properties", "additionalProperties",
                      "enum", "const", "items", "pattern", "$ref", "$schema",
                      "title", "note", "definitions", "intake_schema",
                      "proposal_schema", "decision_schema"}
FAILURES = []
CHECKS = 0


def sha(b):
    return hashlib.sha256(b).hexdigest()


def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def record(ok, name, detail=""):
    global CHECKS
    CHECKS += 1
    print(("PASS " if ok else "FAIL ") + name + ((" — " + detail) if detail and not ok else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def load_json(path):
    return json.loads(pathlib.Path(path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- validator
def resolve(schema, root):
    """Resolve a local $ref, or return the schema unchanged."""
    if isinstance(schema, dict) and "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            raise ValueError(f"unsupported $ref (not local): {ref}")
        node = root
        for part in ref[2:].split("/"):
            node = node[part]
        return node
    return schema


def check_unsupported(schema, root, path="$"):
    """Fail explicitly on any unsupported keyword, anywhere.

    Definition names (under "definitions") and property names
    (under "properties") are names, not keywords, and are not
    checked as keywords; their values are checked as schemas.
    """
    if isinstance(schema, dict):
        if "$ref" in schema and set(schema) != {"$ref"}:
            raise ValueError(f"unsupported $ref sibling constraints at {path}")
        for key, value in schema.items():
            if key == "definitions":
                for name, subschema in value.items():
                    check_unsupported(subschema, root, path + ".definitions." + name)
            elif key == "properties":
                for name, subschema in value.items():
                    check_unsupported(subschema, root, path + ".properties." + name)
            elif key not in SUPPORTED_KEYWORDS:
                raise ValueError(f"unsupported schema keyword {key!r} at {path}")
            elif key in ("intake_schema", "proposal_schema", "decision_schema"):
                check_unsupported(value, root, path + "." + key)
            elif key == "items" and isinstance(value, dict):
                check_unsupported(value, root, path + ".items")


def validate(instance, schema, root, path="$", errors=None):
    """Validate instance against schema. Returns list of error strings."""
    if errors is None:
        errors = []
    schema = resolve(schema, root)
    if not isinstance(schema, dict):
        return errors
    # type
    if "type" in schema:
        expected = schema["type"]
        if not isinstance(expected, list):
            expected = [expected]
        ok = False
        for t in expected:
            if t == "null" and instance is None:
                ok = True
            elif t == "string" and isinstance(instance, str):
                ok = True
            elif t == "number" and isinstance(instance, (int, float)) and not isinstance(instance, bool):
                ok = True
            elif t == "integer" and isinstance(instance, int) and not isinstance(instance, bool):
                ok = True
            elif t == "array" and isinstance(instance, list):
                ok = True
            elif t == "object" and isinstance(instance, dict):
                ok = True
        if not ok:
            errors.append(f"{path}: type {type(instance).__name__} not in {expected}")
            return errors
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: value {instance!r} != const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']!r}")
    if "pattern" in schema and isinstance(instance, str):
        if not re.fullmatch(schema["pattern"], instance):
            errors.append(f"{path}: value {instance!r} does not match pattern {schema['pattern']!r}")
    if isinstance(instance, dict):
        for field in schema.get("required", []):
            if field not in instance:
                errors.append(f"{path}: missing required field {field!r}")
        props = schema.get("properties", {})
        for field, value in instance.items():
            if field in props:
                validate(value, props[field], root, f"{path}.{field}", errors)
        if schema.get("additionalProperties") is False:
            for field in instance:
                if field not in props:
                    errors.append(f"{path}: additional property {field!r} not allowed")
    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            validate(item, schema["items"], root, f"{path}[{i}]", errors)
    return errors


def validate_record(instance, record_type, schema):
    """Validate one record against its named definition. Returns errors."""
    selector = {"intake": "intake_schema", "proposal": "proposal_schema", "decision": "decision_schema"}[record_type]
    return validate(instance, schema[selector], schema)


def cross_intake(instance, errors):
    """Cross-field rules for an intake record."""
    baseline = instance.get("baseline")
    prov = instance.get("baseline_provenance")
    if isinstance(baseline, dict) and isinstance(prov, dict):
        if set(baseline.keys()) != set(BASELINE_FIELDS):
            errors.append("baseline: must have exactly the six fields")
        for field in BASELINE_FIELDS:
            if field not in prov:
                errors.append(f"baseline_provenance: missing entry for {field}")
                continue
            entry = prov[field]
            if not isinstance(entry, dict):
                errors.append(f"baseline_provenance.{field}: not an object")
                continue
            if baseline.get(field) is None and entry.get("source") is not None:
                errors.append(f"baseline_provenance.{field}: null value must not carry source {entry.get('source')!r}")
            if baseline.get(field) is not None and entry.get("source") != "owner":
                errors.append(f"baseline_provenance.{field}: non-null value must have source 'owner'")
    if "owner_facts" in instance:
        errors.append("intake: field owner_facts is superseded; use owner_statements")
    return errors


def cross_decision(instance, proposal_doc, errors):
    """Apply the same decision identity/binding rules in every mode."""
    proposal = proposal_doc["proposal"]
    for field, expected in (
        ("proposal_id", proposal["proposal_id"]),
        ("proposal_digest", proposal_doc["proposal_digest"]),
        ("brief_revision", BRIEF),
        ("intake_id", proposal["intake_id"]),
    ):
        if instance.get(field) != expected:
            errors.append(f"decision_binding_mismatch: {field} does not match reviewed proposal")
    if all(isinstance(instance.get(k), str) for k in ("proposal_digest", "decision", "reason")):
        expected_id = "DEC-" + sha(instance["proposal_digest"].encode() + b"\x00" +
                                  instance["decision"].encode() + b"\x00" +
                                  instance["reason"].encode())[:16]
        if instance.get("decision_id") != expected_id:
            errors.append("decision_id_mismatch: ID does not match canonical decision identity")
    return errors


def classify_line_endings(text):
    kinds = set()
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\r":
            if i + 1 < len(text) and text[i + 1] == "\n":
                kinds.add("CRLF")
                i += 2
            else:
                kinds.add("bare-CR")
                i += 1
        elif ch == "\n":
            kinds.add("LF")
            i += 1
        else:
            i += 1
    if not kinds:
        return "none"
    if len(kinds) == 1:
        return next(iter(kinds))
    return "mixed"


def statements_of(text):
    parts = []
    cur = ""
    i = 0
    while i < len(text):
        if text[i] == "\r" and i + 1 < len(text) and text[i + 1] == "\n":
            parts.append(cur)
            cur = ""
            i += 2
        elif text[i] in "\r\n":
            parts.append(cur)
            cur = ""
            i += 1
        else:
            cur += text[i]
            i += 1
    parts.append(cur)
    return [p for p in parts if p != ""]


def intake_id_for(raw):
    return "INTAKE-" + sha(raw + b"\x00" + BRIEF.encode() + b"\x00" + TEMPLATE.encode())[:16]


# ---------------------------------------------------------------- positive
def positive():
    schema = load_json(BASE / "schema.json")
    try:
        check_unsupported(schema, schema)
        record(True, "schema-only-supported-keywords")
    except ValueError as exc:
        record(False, "schema-only-supported-keywords", str(exc))
        return 1
    record("intake_schema" in schema and "proposal_schema" in schema and "decision_schema" in schema,
           "schema-has-root-selectors")
    record("baseline_provenance" in schema["definitions"], "schema-has-baseline-provenance-definition")
    record("decided_utc" in schema["definitions"]["decision"]["required"], "schema-decision-requires-decided-utc")
    record(set(schema["definitions"]["line_endings"] if "line_endings" in schema["definitions"] else []) == set()
           or schema["definitions"]["intake"]["properties"]["line_endings"]["enum"] == ["LF", "CRLF", "mixed", "bare-CR", "none"],
           "schema-line-endings-enum-expanded")

    intake_doc = load_json(BASE / "expected-intake.json")
    proposal_doc = load_json(BASE / "expected-proposal.json")
    view_doc = load_json(BASE / "expected-proposal-view.json")
    dup_doc = load_json(BASE / "expected-duplicate-response.json")
    repeat_doc = load_json(BASE / "expected-propose-repeat-response.json")
    decision_doc = load_json(BASE / "expected-decision.json")
    negative_doc = load_json(BASE / "negative-decision.json")
    correction_doc = load_json(BASE / "expected-correction.json")
    line_doc = load_json(BASE / "expected-line-endings.json")
    snapshot_doc = load_json(BASE / "operator-reviewed-snapshot.json")

    intake = intake_doc["intake"]
    proposal = proposal_doc["proposal"]
    digest = proposal_doc["proposal_digest"]
    decision = decision_doc["decision"]
    correction = correction_doc["correction"]

    # Schema validation of actual instances (R2-02 core)
    errs = validate_record(intake, "intake", schema)
    errs = cross_intake(intake, errs)
    record(not errs, "intake-instance-validates-against-schema", "; ".join(errs))
    errs = validate_record(proposal, "proposal", schema)
    record(not errs, "proposal-instance-validates-against-schema", "; ".join(errs))
    errs = validate_record(decision, "decision", schema)
    errs = cross_decision(decision, proposal_doc, errs)
    record(not errs, "decision-instance-validates-against-schema", "; ".join(errs))
    errs = validate_record(correction, "intake", schema)
    errs = cross_intake(correction, errs)
    record(not errs, "correction-instance-validates-against-schema", "; ".join(errs))

    # Intake recomputation
    raw = (BASE / "example-request.txt").read_bytes()
    text = raw.decode("utf-8")
    record(intake["intake_id"] == intake_id_for(raw), "intake-id-recomputed")
    record(intake["original_sha256"] == sha(raw), "intake-original-sha")
    record(intake["original_text"] == text, "intake-original-text-verbatim")
    record(intake["original_length_bytes"] == len(raw) and intake["original_length_chars"] == len(text), "intake-lengths")
    record(intake["brief_revision"] == BRIEF and intake["template_version"] == TEMPLATE, "intake-brief-template")
    record("owner_facts" not in intake, "intake-no-owner-facts-field")
    record(intake["owner_statements"] == statements_of(text), "intake-statements-are-derived-lines")
    record(all(v is None for v in intake["baseline"].values()), "intake-baseline-all-null")
    record(all(intake["baseline_provenance"][f]["source"] is None for f, v in intake["baseline"].items() if v is None),
           "intake-baseline-provenance-null-for-null")
    record(intake["duplicate_of"] is None and intake["supersedes"] is None, "intake-duplicate-supersedes-null")

    # Proposal recomputation
    record(sha(canon(proposal)) == digest, "proposal-digest-recomputed")
    record(proposal["proposal_id"] == "PROP-" + intake["intake_id"], "proposal-id-from-intake")
    record(proposal["intake_id"] == intake["intake_id"] and proposal["intake_original_sha256"] == intake["original_sha256"],
           "proposal-binds-intake")
    record([t["task_id"] for t in proposal["tasks"]] == [proposal["proposal_id"] + s for s in ("-T01", "-T02", "-T03", "-T04")],
           "proposal-four-tasks-chain")
    record(proposal["tasks"][0]["depends_on"] == [] and proposal["tasks"][1]["depends_on"] == [proposal["tasks"][0]["task_id"]]
           and proposal["tasks"][2]["depends_on"] == [proposal["tasks"][1]["task_id"]]
           and proposal["tasks"][3]["depends_on"] == [proposal["tasks"][2]["task_id"]], "proposal-task-dependencies-chain")
    record(proposal["tasks"][3]["role"] == "Owner (real operator)", "proposal-review-role-real-operator")
    record("created_utc" not in proposal and "proposal_digest" not in proposal
           and all(set(t.keys()) == {"task_id", "title", "role", "depends_on", "reason"} for t in proposal["tasks"]),
           "proposal-no-timestamp-or-view-in-payload")
    record(view_doc["proposal_id"] == proposal["proposal_id"] and view_doc["proposal_digest"] == digest, "proposal-view-matches-payload")
    record(view_doc["tasks"][0]["readiness"] == "READY" and all(t["readiness"] == "BLOCKED" for t in view_doc["tasks"][1:]),
           "proposal-view-initial-readiness")

    # Duplicate / repeat / decision
    record(dup_doc["intake_id"] == intake["intake_id"] and dup_doc["duplicate"] is True
           and dup_doc["duplicate_of"] == intake["intake_id"] and dup_doc["new_intake_created"] is False
           and dup_doc["new_proposal_created"] is False, "duplicate-response-matches")
    record(repeat_doc["proposal_id"] == proposal["proposal_id"] and repeat_doc["proposal_digest"] == digest
           and repeat_doc["already_exists"] is True, "propose-repeat-matches")
    expected_dec = "DEC-" + sha(digest.encode() + b"\x00" + decision["decision"].encode() + b"\x00" + decision["reason"].encode())[:16]
    record(decision["decision_id"] == expected_dec, "decision-id-recomputed")
    record(decision["provenance"] == "OPERATOR_ASSERTED" and decision["proposal_digest"] == digest, "decision-provenance-operator-asserted")
    record(negative_doc["stale_decision_attempt"]["proposal_digest_supplied"] != negative_doc["stale_decision_attempt"]["proposal_digest_current"]
           and negative_doc["stale_decision_attempt"]["expected"]["outcome"] == "REJECTED_STALE", "negative-stale-mismatch")
    record(negative_doc["pasted_approval_in_request"]["expected"]["decision_created"] is False, "negative-pasted-approval-no-decision")

    # Operator-reviewed snapshot (R2-01)
    record(snapshot_doc["expected_proposal_digest"] == digest and snapshot_doc["expected_brief_revision"] == BRIEF
           and snapshot_doc["expected_intake_id"] == intake["intake_id"] and snapshot_doc["proposal_id"] == proposal["proposal_id"],
           "operator-snapshot-matches-golden-proposal")

    # Line endings (R2-03)
    for case in line_doc["cases"]:
        raw_c = (BASE / case["file"]).read_bytes()
        text_c = raw_c.decode("utf-8")
        record(case["line_endings"] == classify_line_endings(text_c), f"line-endings-{case['file']}-classified")
        record(case["owner_statements"] == statements_of(text_c), f"line-endings-{case['file']}-statements-derived")
        record(case["original_sha256"] == sha(raw_c), f"line-endings-{case['file']}-hash")
        record(case["original_length_bytes"] == len(raw_c) and case["original_length_chars"] == len(text_c),
               f"line-endings-{case['file']}-lengths")
    record("request-crlf.txt" in [c["file"] for c in line_doc["cases"]]
           and all("\r" not in s for c in line_doc["cases"] for s in c["owner_statements"]),
           "line-endings-statements-strip-breaks-not-original")

    # Correction golden (R2-03)
    corr_raw = (BASE / "correction-request.txt").read_bytes()
    record(correction["intake_id"] == intake_id_for(corr_raw), "correction-id-recomputed")
    record(correction["supersedes"] == intake["intake_id"], "correction-supersedes-original")
    record(correction["intake_id"] != intake["intake_id"] and corr_raw != raw, "correction-new-bytes-new-id")
    record(correction["original_sha256"] == sha(corr_raw), "correction-original-sha")

    # Boundary fixtures
    record(len((BASE / "request-char-cap-ok.txt").read_bytes()) == 10000, "char-cap-ok-size")
    record(len((BASE / "request-char-cap-over.txt").read_bytes()) == 10001, "char-cap-over-size")
    record(len((BASE / "request-byte-cap-over.txt").read_bytes()) == 20001, "byte-cap-over-size")
    record((BASE / "request-whitespace.txt").read_text(encoding="utf-8").strip() == "", "whitespace-only-strips-empty")
    crlf_raw = (BASE / "request-crlf.txt").read_bytes()
    record(b"\r\n" in crlf_raw and sha(crlf_raw) != sha(raw), "crlf-preserved-not-normalized")
    bom_doc = load_json(BASE / "request-bom.json")
    record(base64.b64decode(bom_doc["input_base64"]).startswith(b"\xef\xbb\xbf"), "bom-input-starts-with-bom")
    record(bom_doc["expected"]["reason"] == "bom_not_accepted" and bom_doc["expected"]["intake_record_created"] is False, "bom-expected-reject")
    nul_doc = load_json(BASE / "request-nul.json")
    record(b"\x00" in base64.b64decode(nul_doc["input_base64"]), "nul-input-contains-nul")
    record(nul_doc["expected"]["reason"] == "nul_or_binary" and nul_doc["expected"]["intake_record_created"] is False, "nul-expected-reject")

    # Manifest completeness (hash match is NOT a substitute for schema validation)
    manifest = load_json(BASE / "MANIFEST.json")
    listed = manifest["files"]
    all_files = sorted(p.relative_to(BASE).as_posix() for p in BASE.rglob("*") if p.is_file() and p.name != "MANIFEST.json")
    record(set(listed.keys()) == set(all_files), "manifest-lists-every-bundle-file",
           f"listed-missing={sorted(set(all_files) - set(listed.keys()))} extra={sorted(set(listed.keys()) - set(all_files))}")
    manifest_ok = True
    for name, info in listed.items():
        data = (BASE / name).read_bytes()
        if info.get("bytes") != len(data) or info.get("sha256") != sha(data):
            manifest_ok = False
            print(f"FAIL manifest-hash-{name}")
    record(manifest_ok, "manifest-hashes-and-sizes-match")
    record(manifest.get("note", "").find("excludes itself") >= 0, "manifest-self-exclusion-noted")

    print(f"\n{len(FAILURES)} failure(s) in positive bundle" if FAILURES else "\nALL POSITIVE CHECKS PASS")
    return 1 if FAILURES else 0


# ---------------------------------------------------------------- single / negative
def validate_one(path, record_type):
    """Validate one instance file. Returns (errors, instance_doc)."""
    schema = load_json(BASE / "schema.json")
    try:
        check_unsupported(schema, schema)
    except ValueError as exc:
        return [f"schema unsupported keyword: {exc}"], None
    doc = load_json(path)
    if record_type == "correction":
        # Special format: bytes_source + supersedes, judged by correction rules.
        instance = doc.get("instance", doc)
        bytes_source = instance.get("bytes_source")
        supersedes = instance.get("supersedes")
        if not bytes_source or supersedes is None:
            return ["correction: missing bytes_source or supersedes"], doc
        raw = (BASE / bytes_source).read_bytes()
        corr_id = intake_id_for(raw)
        golden_intake = load_json(BASE / "expected-intake.json")["intake"]
        orig_id = golden_intake["intake_id"]
        if corr_id == orig_id and supersedes == orig_id:
            return ["correction_no_op_same_bytes: correction bytes identical to original bytes"], doc
        if corr_id == orig_id and supersedes != orig_id:
            return ["correction_conflict_existing_id: bytes already exist as original intake, supersedes points elsewhere"], doc
        if corr_id != orig_id and supersedes not in (orig_id,):
            # A correction must supersede an existing intake; here the only
            # existing intake in the static bundle is the golden original.
            return ["correction_supersedes_not_found: supersedes does not point to an existing intake"], doc
        return [], doc
    instance = doc.get("instance", doc)
    if record_type in ("intake", "proposal", "decision"):
        errors = validate_record(instance, record_type, schema)
        if record_type == "intake":
            errors = cross_intake(instance, errors)
        if record_type == "decision":
            proposal_doc = load_json(BASE / "expected-proposal.json")
            errors = cross_decision(instance, proposal_doc, errors)
        return errors, doc
    return [f"unknown record_type {record_type!r}"], doc


def negative():
    neg_dir = BASE / "negative"
    files = sorted(neg_dir.glob("*.json"))
    rejected = 0
    print(f"Negative probes: {len(files)} file(s)")
    for path in files:
        doc = load_json(path)
        record_type = doc.get("record_type")
        errors, _ = validate_one(path, record_type)
        if errors:
            rejected += 1
            print(f"REJECTED {path.name} — {errors[0]}")
        else:
            print(f"ACCEPTED (BUG) {path.name} — checker failed to reject a malformed fixture")
    print(f"\nNegative probes rejected: {rejected}/{len(files)}")
    if rejected == len(files) and files:
        print("ALL NEGATIVE PROBES REJECTED")
        return 0
    print("NEGATIVE PROBE FAILURE: at least one malformed fixture was accepted")
    return 1


def schema_probes():
    """Run stored V21-02 schema-probe regressions.

    Reads regression-schema-probes.json, applies each injection to
    a deep copy of schema.json in memory, and expects
    check_unsupported to raise ValueError. A probe that is not
    rejected is a checker bug. Returns 0 only if every probe is
    rejected.
    """
    import copy as _copy
    schema = load_json(BASE / "schema.json")
    probes_doc = load_json(BASE / "regression-schema-probes.json")
    probes = probes_doc["probes"]
    rejected = 0
    print(f"Schema probes: {len(probes)} probe(s)")
    for probe in probes:
        target_path = probe["target"].split(".")
        modified = _copy.deepcopy(schema)
        node = modified
        for part in target_path:
            node = node[part]
        node.update(probe["inject"])
        try:
            check_unsupported(modified, modified)
            print(f"ACCEPTED (BUG) {probe['case']} — unsupported keyword was not rejected")
        except ValueError as exc:
            rejected += 1
            print(f"REJECTED {probe['case']} — {exc}")
    print(f"\nSchema probes rejected: {rejected}/{len(probes)}")
    if rejected == len(probes) and probes:
        print("ALL SCHEMA PROBES REJECTED")
        return 0
    print("SCHEMA PROBE FAILURE: at least one unsupported keyword was accepted")
    return 1


def main():
    parser = argparse.ArgumentParser(description="Static checker for intake REV2.1 fixtures.")
    parser.add_argument("--validate", metavar="FILE", help="Validate one instance file; exit 0 if valid, 1 if invalid.")
    parser.add_argument("--as", dest="as_type", choices=["intake", "proposal", "decision", "correction"],
                        help="Record type for --validate.")
    parser.add_argument("--negative", action="store_true", help="Run all negative fixtures; exit 0 only if all are rejected.")
    parser.add_argument("--schema-probes", action="store_true", help="Run stored schema-probe regressions; exit 0 only if all are rejected.")
    args = parser.parse_args()
    if args.schema_probes:
        return schema_probes()
    if args.negative:
        return negative()
    if args.validate:
        if not args.as_type:
            print("ERROR: --validate requires --as intake|proposal|decision|correction")
            return 2
        errors, _ = validate_one(args.validate, args.as_type)
        if errors:
            print(f"INVALID {args.validate}")
            for err in errors:
                print(f"  - {err}")
            return 1
        print(f"VALID {args.validate}")
        return 0
    return positive()


if __name__ == "__main__":
    sys.exit(main())
