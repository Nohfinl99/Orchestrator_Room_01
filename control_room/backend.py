"""Backend-owned control-plane logic for Orchestrator-Room, revisions 2 and 5.

Revision 5 (C5, packet REV2.1 + F21) appends the intake slice at the
end of this file; see the C5 section header there and
control_room/C5_BUILD_NOTE.md. No revision 2 function behaviour
changed for pre-C5 stores.

Revision 2 repairs findings F01-F06 from the independent review of
1bba803 (see MUSE_REVIEW_NEXT.md on the reviewer branch, read-only).
The important changes, in plain terms:

- Evidence is a proposal, never a verdict. verify() only returns PASS
  for a code-verification mechanism check when a frozen required-case
  plan is fully covered by bound, complete, exit-0 evidence, artifact
  bytes actually match the claimed hash, and a judge review receipt
  covers exactly those records and still matches their content. A
  forged, missing, altered, incomplete, or stale record can never yield
  PASS. A verify() PASS is still not an independent verification and
  is not product/pain validation.
- Product gates bind to content, not to existence. An observation must
  be ready (trigger, problem, source locator present). An inference
  must be owner-REVIEWED with candidate and hypothesis present. A
  brief must be owner-APPROVED and its linked content must still match.
  An owner decision must name a judge report whose snapshot content
  still matches current project content, with findings and per-case
  results present. Content changes after a snapshot invalidate it.
  Audit events are excluded from snapshot content, so merely appending
  an event does not invalidate a snapshot.
- Role arguments are simulation only. They are kept for local demo
  ordering, but they do not authenticate anyone. The CLI marks every
  privileged output as simulated and blocks live adapters.
- Audit events carry a UTC timestamp, content digests before/after,
  and a hash chain. The chain detects accidental corruption and
  tampering by a party that does not recompute the whole chain. It is
  NOT tamper-proof against the owner of the storage, who can rewrite
  history and recompute digests. That limit is stated in the docs and
  in verify-history output.

No function here performs network, provider, shell, or filesystem
access outside the store dict it is given. Text from observations,
inferences, or agent output is data only.
"""
import hashlib
import json
import math
import re
from datetime import datetime, timezone

SCHEMA_VERSION = 2
PROJECT_ID = "product-discovery-pilot"
ROOM_ID = "control-room-1"
CRITERIA_REVISION = "ACCEPTANCE-REV2-1"
VERIFICATION_PLAN_ID = "CONTROL_ROOM_VERIFICATION_PLAN"
VERIFICATION_PLAN_REVISION = "REV3-1"

PRODUCT_STAGES = [
    "INTAKE",
    "NEEDS_EVIDENCE",
    "HYPOTHESIS_DRAFT",
    "OWNER_REVIEW",
    "ACCEPTED_FOR_LOCAL_PROTOTYPE",
    "JUDGE_REVIEW",
    "OWNER_ACCEPTED",
    "OWNER_REJECTED",
    "OWNER_DEFERRED",
]
TASK_STATES = {"TODO", "DOING", "BLOCKED", "DONE"}
EVIDENCE_RESULTS = {"PASS", "FAIL", "NOT_RUN", "INCONCLUSIVE"}

# Frozen required-case plan for verify(). Every case must be covered by
# a bound, complete, exit-0, reviewed PASS record for the same code
# revision, or verify() cannot return PASS.
REQUIRED_VERIFICATION_CASES = [
    "control-room-overview",
    "observation-roundtrip",
    "facts-inferences-separate",
    "task-done-no-advance",
    "illegal-transition-rejected",
    "dependency-cas",
    "owner-decision-binding",
    "hostile-text-inert",
    "store-boundaries",
    "no-network-imports",
]

def _plan_digest():
    return _sha256_text(_canonical({
        "id": VERIFICATION_PLAN_ID,
        "revision": VERIFICATION_PLAN_REVISION,
        "criteria_revision": CRITERIA_REVISION,
        "required_cases": REQUIRED_VERIFICATION_CASES,
    }))


MAX_TEXT = 10000
MAX_LIST_ITEMS = 50
MAX_STORE_BYTES = 1_000_000
_HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


class ControlError(ValueError):
    """Validation / authority / state error. No content change on this error,
    except for the explicitly documented decision_rejected audit event."""


class DecisionRejectedError(ControlError):
    """A gate decision was rejected after recording a decision_rejected
    audit event in the store. Callers must save the store even though
    this error is raised, or the rejected-decision history is lost."""


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

VERIFICATION_PLAN_DIGEST = _plan_digest()


def _utcnow():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _check_text(value, field):
    if value is not None and not isinstance(value, str):
        raise ControlError(f"{field} must be text or null")
    if isinstance(value, str) and len(value) > MAX_TEXT:
        raise ControlError(f"{field} is oversized")


def _require_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ControlError(f"{field} is required")
    _check_text(value, field)
    return value.strip()


def _check_list(value, field):
    if value is None:
        return []
    if not isinstance(value, list):
        raise ControlError(f"{field} must be a list")
    if len(value) > MAX_LIST_ITEMS:
        raise ControlError(f"{field} has too many items (max {MAX_LIST_ITEMS})")
    for item in value:
        if not isinstance(item, str):
            raise ControlError(f"{field} items must be text")
        _check_text(item, field)
    return list(value)


def new_store():
    return {
        "schema_version": SCHEMA_VERSION,
        "project": {
            "id": PROJECT_ID,
            "name": "Product-discovery pilot",
            "room_id": ROOM_ID,
            "soul": {
                "purpose": "Supervise a local product-discovery workflow through evidence, hypothesis, owner review and a measured local prototype.",
                "intended_user": "Project owner, self-use",
                "interaction_principles": "Show what is known, what is inferred, what is missing, the current revision, who may act next, and what evidence supports the state.",
                "authority_note": "Soul is guidance only; it never grants authority.",
            },
            "pain_status": "OWNER_STATED_GOAL_NOT_VALIDATED_PAIN",
        },
        "stage": "INTAKE",
        "revision": 0,
        "observations": [],
        "inferences": [],
        "briefs": [],
        "tasks": [],
        "evidence": [],
        "judge_reports": [],
        "review_receipts": [],
        "events": [],
    }


def content_digest(store):
    """Digest of project content, excluding audit events and the store
    revision counter. Appending an event therefore does not change it."""
    content = {
        "stage": store["stage"],
        "project": store["project"],
        "observations": store["observations"],
        "inferences": store["inferences"],
        "briefs": store["briefs"],
        "tasks": store["tasks"],
        "evidence": store["evidence"],
        "judge_reports": store["judge_reports"],
        "review_receipts": store["review_receipts"],
    }
    # C5 (revision 5): intake, proposal, decision and proposal task
    # status are part of content when present and non-empty, so the
    # history chain anchors them. Empty collections are omitted
    # because they carry no information; omitting them keeps the
    # digest of a pre-C5 store identical, so existing C4 stores
    # keep a valid history anchor.
    for key in ("intakes", "proposals", "decisions", "proposal_task_status"):
        if store.get(key):
            content[key] = store[key]
    # C6 (revision 6): contextual collections are part of content when
    # present and non-empty, same pattern as C5, so the history chain
    # anchors them. Empty collections are omitted, so pre-C6 stores
    # keep an identical digest and a valid history anchor.
    for key in ("context_sources", "clarifications", "rewrites",
                "rewrite_reviews", "contextual_proposals"):
        if store.get(key):
            content[key] = store[key]
    return _sha256_text(_canonical(content))


def snapshot_digest(store):
    """Digest of the content a judge report freezes: observations,
    inferences, briefs, evidence and tasks. Judge reports, review
    receipts, events and the revision counter are excluded, so creating
    the report itself does not invalidate its own snapshot."""
    content = {
        "observations": store["observations"],
        "inferences": store["inferences"],
        "briefs": store["briefs"],
        "evidence": store["evidence"],
        "tasks": store["tasks"],
    }
    return _sha256_text(_canonical(content))


def _event(store, kind, actor, role, before, after, reason, linked_evidence,
           before_digest, extra=None):
    after_digest = content_digest(store)
    prev = store["events"][-1]["event_digest"] if store["events"] else "GENESIS"
    event = {
        "kind": kind,
        "actor": actor,
        "role": role,
        "before_stage": before,
        "after_stage": after,
        "reason": reason,
        "linked_evidence": linked_evidence,
        "store_revision_before": store["revision"],
        "store_revision_after": store["revision"] + 1,
        "timestamp_utc": _utcnow(),
        "content_digest_before": before_digest,
        "content_digest_after": after_digest,
        "prev_event_digest": prev,
    }
    if extra:
        event.update(extra)
    event["event_digest"] = _sha256_text(_canonical(event))
    store["events"].append(event)
    store["revision"] += 1
    return event


def _find(store, collection, item_id):
    for item in store[collection]:
        if item.get("id") == item_id:
            return item
    raise ControlError(f"{collection[:-1]} not found: {item_id}")


def _nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _require_valid_history(store):
    result = verify_history(store)
    if not result["chain_valid"]:
        raise ControlError(
            "history invalid; privileged mutation blocked; "
            "use verify-history for diagnostics: " + "; ".join(result["failures"][:3]))


def observation_ready(obs):
    return (_nonempty_text(obs.get("trigger_or_goal"))
            and _nonempty_text(obs.get("raw_problem_statement"))
            and _nonempty_text(obs.get("source_locator")))


def inference_ready(inf):
    return (inf.get("review_status") == "REVIEWED"
            and _nonempty_text(inf.get("candidate_pain"))
            and _nonempty_text(inf.get("candidate_value_hypothesis")))


def brief_content_digest(brief):
    """Recomputed from actual fields, never from a cached digest field.
    Tampering with title/content/ids therefore changes this digest even
    if the stored content_digest field is left untouched."""
    return _sha256_text(_canonical({
        "title": brief.get("title"),
        "content": brief.get("content"),
        "observation_ids": brief.get("observation_ids"),
        "inference_ids": brief.get("inference_ids"),
    }))


def _linked_digest(store, brief):
    obs = []
    for oid in brief["observation_ids"]:
        obs.append(_find(store, "observations", oid))
    infs = []
    for iid in brief["inference_ids"]:
        infs.append(_find(store, "inferences", iid))
    return _sha256_text(_canonical({
        "brief_content_digest": brief_content_digest(brief),
        "observations": obs,
        "inferences": infs,
    }))


def brief_acceptance_ready(store, brief):
    """Coherence check for the *chosen* brief, not for unrelated records.
    The brief must be approved, its actual content must still match the
    approved digest, and it must reference a nonempty, coherent graph:
    ready observations, reviewed inferences, and each inference linked
    to observations that are themselves in the brief."""
    if brief.get("status") != "APPROVED":
        return False
    if not _nonempty_text(brief.get("title")) or not _nonempty_text(brief.get("content")):
        return False
    if not brief.get("observation_ids") or not brief.get("inference_ids"):
        return False
    try:
        if brief_content_digest(brief) != brief.get("approved_content_digest"):
            return False
        if _linked_digest(store, brief) != brief.get("approved_linked_digest"):
            return False
        obs_ids = set(brief["observation_ids"])
        for oid in brief["observation_ids"]:
            if not observation_ready(_find(store, "observations", oid)):
                return False
        for iid in brief["inference_ids"]:
            inf = _find(store, "inferences", iid)
            if not inference_ready(inf):
                return False
            if not set(inf.get("source_observation_ids") or []).issubset(obs_ids):
                return False
    except ControlError:
        return False
    return True


def brief_approval_valid(store, brief):
    # Kept as a narrow digest check; acceptance also requires
    # brief_acceptance_ready() (coherence, readiness, graph).
    if brief.get("status") != "APPROVED":
        return False
    try:
        if brief_content_digest(brief) != brief.get("approved_content_digest"):
            return False
        return _linked_digest(store, brief) == brief.get("approved_linked_digest")
    except ControlError:
        return False


def add_observation(store, actor, role, obs_id, trigger=None, problem=None,
                    steps=None, elapsed_time_minutes=None, stalled=None,
                    workaround=None, result=None, source_locator=None,
                    source_sha256=None, is_direct_observation=None):
    before = content_digest(store)
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may add an observation (simulated role)")
    _require_text(obs_id, "observation id")
    if any(o["id"] == obs_id for o in store["observations"]):
        raise ControlError(f"duplicate observation id: {obs_id}")
    for name, val in [("trigger", trigger), ("problem", problem),
                      ("stalled", stalled), ("workaround", workaround),
                      ("result", result), ("source_locator", source_locator)]:
        _check_text(val, name)
    steps = _check_list(steps, "steps")
    if elapsed_time_minutes is not None:
        if isinstance(elapsed_time_minutes, bool) or not isinstance(elapsed_time_minutes, (int, float)):
            raise ControlError("elapsed_time_minutes must be a number or null")
        if not math.isfinite(float(elapsed_time_minutes)) or float(elapsed_time_minutes) < 0:
            raise ControlError("elapsed_time_minutes must be finite and nonnegative")
    if source_sha256 is not None and not _HEX64.match(source_sha256):
        raise ControlError("source_sha256 must be a 64-character hex string or null")
    if is_direct_observation is not None and not isinstance(is_direct_observation, bool):
        raise ControlError("is_direct_observation must be true, false or null")
    obs = {
        "id": obs_id, "schema_revision": 1,
        "trigger_or_goal": trigger, "raw_problem_statement": problem,
        "current_steps": steps, "elapsed_time_minutes": elapsed_time_minutes,
        "where_work_stalled_or_repeated": stalled, "current_workaround": workaround,
        "result_or_rework": result, "source_locator": source_locator,
        "source_sha256_if_file": source_sha256,
        "is_direct_observation": is_direct_observation,
        "privacy": {"real_customer_or_business_data": False,
                    "external_provider_upload_allowed": False},
    }
    store["observations"].append(obs)
    _event(store, "observation_added", actor, role, store["stage"], store["stage"],
           f"observation {obs_id} recorded", None, before)
    return obs


def add_inference(store, actor, role, inf_id, observation_ids, candidate_pain=None,
                  segment=None, hypothesis=None, unknowns=None, alternatives=None):
    before = content_digest(store)
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may add an inference (simulated role)")
    _require_text(inf_id, "inference id")
    if any(i["id"] == inf_id for i in store["inferences"]):
        raise ControlError(f"duplicate inference id: {inf_id}")
    if not isinstance(observation_ids, list) or not observation_ids:
        raise ControlError("inference must link at least one observation")
    if len(observation_ids) > MAX_LIST_ITEMS:
        raise ControlError("too many linked observations")
    for oid in observation_ids:
        _find(store, "observations", oid)
    for name, val in [("candidate_pain", candidate_pain), ("segment", segment),
                      ("hypothesis", hypothesis)]:
        _check_text(val, name)
    inf = {
        "id": inf_id, "source_observation_ids": list(observation_ids),
        "candidate_pain": candidate_pain, "candidate_user_segment": segment,
        "candidate_value_hypothesis": hypothesis,
        "unknowns": _check_list(unknowns, "unknowns"),
        "alternative_explanations": _check_list(alternatives, "alternative_explanations"),
        "author_role": role, "review_status": "DRAFT",
    }
    store["inferences"].append(inf)
    _event(store, "inference_added", actor, role, store["stage"], store["stage"],
           f"inference {inf_id} recorded separately from facts", None, before)
    return inf


def review_inference(store, actor, role, inf_id, status):
    before = content_digest(store)
    _require_valid_history(store)
    if role != "owner":
        raise ControlError("only owner may review an inference (simulated role)")
    if status not in ("REVIEWED", "REJECTED"):
        raise ControlError("inference review status must be REVIEWED or REJECTED")
    inf = _find(store, "inferences", inf_id)
    inf["review_status"] = status
    _event(store, "inference_reviewed", actor, role, store["stage"], store["stage"],
           f"inference {inf_id} -> {status}", None, before)
    return inf


def add_brief(store, actor, role, brief_id, title, content, observation_ids, inference_ids):
    before = content_digest(store)
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may add a brief (simulated role)")
    _require_text(brief_id, "brief id")
    _require_text(title, "brief title")
    _require_text(content, "brief content")
    if any(b["id"] == brief_id for b in store["briefs"]):
        raise ControlError(f"duplicate brief id: {brief_id}")
    for oid in observation_ids or []:
        _find(store, "observations", oid)
    for iid in inference_ids or []:
        _find(store, "inferences", iid)
    brief = {
        "id": brief_id, "title": title, "content": content,
        "observation_ids": list(observation_ids or []),
        "inference_ids": list(inference_ids or []),
        "content_digest": _sha256_text(_canonical({
            "title": title, "content": content,
            "observation_ids": list(observation_ids or []),
            "inference_ids": list(inference_ids or []),
        })),
        "status": "DRAFT", "approved_by": None, "approved_reason": None,
        "approved_at_utc": None, "approved_content_digest": None,
        "approved_linked_digest": None,
    }
    store["briefs"].append(brief)
    _event(store, "brief_added", actor, role, store["stage"], store["stage"],
           f"brief {brief_id} drafted", None, before)
    return brief


def approve_brief(store, actor, role, brief_id, reason):
    before = content_digest(store)
    _require_valid_history(store)
    if role != "owner":
        raise ControlError("only owner may approve a brief (simulated role)")
    if not reason or not reason.strip():
        raise ControlError("brief approval requires a reason")
    brief = _find(store, "briefs", brief_id)
    brief["status"] = "APPROVED"
    brief["approved_by"] = actor
    brief["approved_reason"] = reason.strip()
    brief["approved_at_utc"] = _utcnow()
    brief["approved_content_digest"] = brief_content_digest(brief)
    brief["approved_linked_digest"] = _linked_digest(store, brief)
    _event(store, "brief_approved", actor, role, store["stage"], store["stage"],
           f"brief {brief_id} approved", None, before)
    return brief


def add_task(store, actor, role, task_id, title, owner, depends_on=None):
    before = content_digest(store)
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may add a task (simulated role)")
    _require_text(task_id, "task id")
    _require_text(title, "task title")
    _require_text(owner, "task owner")
    if any(t["id"] == task_id for t in store["tasks"]):
        raise ControlError(f"duplicate task id: {task_id}")
    deps = _check_list(depends_on, "depends_on")
    for dep in deps:
        _find(store, "tasks", dep)
    task = {"id": task_id, "title": title, "owner": owner, "state": "TODO",
            "dependencies": deps, "revision": 0}
    store["tasks"].append(task)
    _event(store, "task_added", actor, role, store["stage"], store["stage"],
           f"task {task_id} added", None, before)
    return task


def update_task(store, actor, role, task_id, state, expected_revision):
    before = content_digest(store)
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may update a task (simulated role)")
    if state not in TASK_STATES:
        raise ControlError(f"unknown task state: {state}")
    task = _find(store, "tasks", task_id)
    if expected_revision is None or int(expected_revision) != task["revision"]:
        raise ControlError(
            f"stale task update for {task_id}: expected revision {expected_revision}, "
            f"current revision {task['revision']}; no overwrite performed")
    task["state"] = state
    task["revision"] += 1
    _event(store, "task_updated", actor, role, store["stage"], store["stage"],
           f"task {task_id} -> {state}", None, before)
    for other in store["tasks"]:
        if task_id in other["dependencies"] and other["state"] == "TODO":
            deps = [_find(store, "tasks", d) for d in other["dependencies"]]
            if all(d["state"] == "DONE" for d in deps):
                _event(store, "dependency_ready", actor, role, store["stage"],
                       store["stage"], f"task {other['id']} dependencies now DONE", None,
                       content_digest(store))
    return task


def add_evidence(store, actor, role, ev_id, claim, artifact, test_case,
                 code_revision, result, reviewer, collector, exit_code=None,
                 output_hash=None, command=None, environment=None,
                 criteria_revision=None, scope_complete=False,
                 artifact_path=None, artifact_sha256=None):
    before = content_digest(store)
    if role == "judge":
        raise ControlError("judge may not create evidence (simulated role)")
    if role not in ("agent", "owner"):
        raise ControlError("only agent or owner may add evidence (simulated role)")
    _require_text(ev_id, "evidence id")
    _require_text(claim, "claim")
    _require_text(code_revision, "code_revision")
    if result not in EVIDENCE_RESULTS:
        raise ControlError(f"unknown evidence result: {result}")
    if any(e["id"] == ev_id for e in store["evidence"]):
        raise ControlError(f"duplicate evidence id: {ev_id}")
    if output_hash is not None and not _HEX64.match(output_hash):
        raise ControlError("output_hash must be a 64-character hex string or null")
    if artifact_sha256 is not None and not _HEX64.match(artifact_sha256):
        raise ControlError("artifact_sha256 must be a 64-character hex string or null")
    if exit_code is not None and (isinstance(exit_code, bool) or not isinstance(exit_code, int)):
        raise ControlError("exit_code must be an integer or null")
    ev = {
        "id": ev_id, "claim": claim, "artifact": artifact, "test_case": test_case,
        "code_revision": code_revision, "result": result, "reviewer": reviewer,
        "collector": collector, "exit_code": exit_code, "output_hash": output_hash,
        "command_or_steps": command, "environment": environment,
        "criteria_revision": criteria_revision, "scope_complete": bool(scope_complete),
        "artifact_path": artifact_path, "artifact_sha256": artifact_sha256,
        "timestamp_utc": _utcnow(),
    }
    store["evidence"].append(ev)
    _event(store, "evidence_added", actor, role, store["stage"], store["stage"],
           f"evidence {ev_id} recorded as proposal with result {result}", ev_id, before)
    return ev


def add_review_receipt(store, actor, role, receipt_id, evidence_ids, decision="REVIEWED_PASS"):
    before = content_digest(store)
    _require_valid_history(store)
    if role != "judge":
        raise ControlError("only judge may create a review receipt (simulated role)")
    _require_text(receipt_id, "review receipt id")
    if any(r["id"] == receipt_id for r in store["review_receipts"]):
        raise ControlError(f"duplicate review receipt id: {receipt_id}")
    if not evidence_ids:
        raise ControlError("review receipt must cover at least one evidence record")
    records = [_find(store, "evidence", eid) for eid in evidence_ids]
    digest = _sha256_text(_canonical(sorted(records, key=lambda r: r["id"])))
    receipt = {
        "id": receipt_id, "evidence_ids": list(evidence_ids), "decision": decision,
        "evidence_digest": digest, "reviewer_actor": actor,
        "timestamp_utc": _utcnow(),
        "note": "Simulation only: a judge role argument is not authentication, and a receipt string does not prove independent review.",
    }
    store["review_receipts"].append(receipt)
    _event(store, "review_receipt_added", actor, role, store["stage"], store["stage"],
           f"review receipt {receipt_id} covering {len(evidence_ids)} evidence records",
           None, before)
    return receipt


def judge_report(store, actor, role, report_id, findings=None, per_case=None):
    before = content_digest(store)
    _require_valid_history(store)
    if role != "judge":
        raise ControlError("only judge may create a judge report (simulated role)")
    _require_text(report_id, "judge report id")
    if any(r["id"] == report_id for r in store["judge_reports"]):
        raise ControlError(f"duplicate judge report id: {report_id}")
    findings = _check_list(findings, "findings")
    per_case = _check_list(per_case, "per_case")
    report = {
        "id": report_id, "frozen_store_revision": store["revision"],
        "stage_at_creation": store["stage"],
        "snapshot_content_digest": snapshot_digest(store),
        "snapshot_artifact_ids": {
            "observations": [o["id"] for o in store["observations"]],
            "inferences": [i["id"] for i in store["inferences"]],
            "briefs": [b["id"] for b in store["briefs"]],
            "evidence": [e["id"] for e in store["evidence"]],
            "tasks": [t["id"] for t in store["tasks"]],
        },
        "findings": findings, "per_case": per_case,
        "timestamp_utc": _utcnow(),
        "note": "Read-only report: creating it does not change stage, evidence, or verification. A report with empty findings/per_case cannot support an owner decision.",
    }
    store["judge_reports"].append(report)
    _event(store, "judge_report_added", actor, role, store["stage"], store["stage"],
           f"judge report {report_id} attached to snapshot digest {report['snapshot_content_digest']}",
           None, before)
    return report


def transition(store, actor, role, to_stage, reason, linked_evidence=None,
               brief_id=None, judge_report_id=None):
    before = content_digest(store)
    _require_valid_history(store)
    if role != "owner":
        raise ControlError("only owner may move the product stage (simulated role)")
    if to_stage not in PRODUCT_STAGES:
        raise ControlError(f"unknown stage: {to_stage}")
    from_stage = store["stage"]
    allowed = {
        ("INTAKE", "NEEDS_EVIDENCE"),
        ("NEEDS_EVIDENCE", "HYPOTHESIS_DRAFT"),
        ("HYPOTHESIS_DRAFT", "OWNER_REVIEW"),
        ("OWNER_REVIEW", "ACCEPTED_FOR_LOCAL_PROTOTYPE"),
        ("ACCEPTED_FOR_LOCAL_PROTOTYPE", "JUDGE_REVIEW"),
        ("JUDGE_REVIEW", "OWNER_ACCEPTED"),
        ("JUDGE_REVIEW", "OWNER_REJECTED"),
        ("JUDGE_REVIEW", "OWNER_DEFERRED"),
    }
    if (from_stage, to_stage) not in allowed:
        raise ControlError(f"illegal transition: {from_stage} -> {to_stage}")
    if linked_evidence is not None:
        _find(store, "evidence", linked_evidence)
    # Gate prerequisites, checked on content, not on existence alone.
    if (from_stage, to_stage) == ("NEEDS_EVIDENCE", "HYPOTHESIS_DRAFT"):
        if not any(observation_ready(o) for o in store["observations"]):
            raise ControlError("cannot draft a hypothesis: no ready observation (trigger, problem and source locator required)")
    if (from_stage, to_stage) == ("HYPOTHESIS_DRAFT", "OWNER_REVIEW"):
        if not any(inference_ready(i) for i in store["inferences"]):
            raise ControlError("cannot move to owner review: no owner-REVIEWED inference with candidate and hypothesis")
    if (from_stage, to_stage) == ("OWNER_REVIEW", "ACCEPTED_FOR_LOCAL_PROTOTYPE"):
        if not reason or not reason.strip():
            raise ControlError("owner approval requires a reason for this revision")
        if not brief_id:
            raise ControlError("owner approval requires a brief id")
        brief = _find(store, "briefs", brief_id)
        if not brief_acceptance_ready(store, brief):
            _event(store, "decision_rejected", actor, role, from_stage, from_stage,
                   f"brief {brief_id} approval invalid or stale; linked content digest mismatch",
                   linked_evidence, before,
                   extra={"brief_id": brief_id, "approved_linked_digest": brief.get("approved_linked_digest"),
                          "current_linked_digest": None})
            raise DecisionRejectedError(f"brief {brief_id} approval is invalid or stale; decision rejected and recorded, stage unchanged")
    if from_stage == "JUDGE_REVIEW" and to_stage in ("OWNER_ACCEPTED", "OWNER_REJECTED", "OWNER_DEFERRED"):
        if not reason or not reason.strip():
            raise ControlError("owner decision requires a reason")
        if not judge_report_id:
            raise ControlError("owner decision requires a judge report id")
        report = _find(store, "judge_reports", judge_report_id)
        current_snapshot = snapshot_digest(store)
        if report.get("stage_at_creation") != "JUDGE_REVIEW":
            raise ControlError("judge report was not created in JUDGE_REVIEW")
        if not report.get("findings") or not report.get("per_case"):
            raise ControlError("judge report with empty findings or per_case cannot support an owner decision")
        # Revalidate the brief that authorised ACCEPTED_FOR_LOCAL_PROTOTYPE,
        # if one was recorded, so a later content change cannot authorise
        # a terminal decision through a stale approval.
        accepted_brief_id = None
        for ev in reversed(store["events"]):
            if ev.get("kind") == "stage_transition" and ev.get("after_stage") == "ACCEPTED_FOR_LOCAL_PROTOTYPE":
                accepted_brief_id = (ev.get("brief_id") if "brief_id" in ev else None)
                break
        if accepted_brief_id:
            try:
                accepted_brief = _find(store, "briefs", accepted_brief_id)
            except ControlError:
                accepted_brief = None
            if accepted_brief is not None and not brief_acceptance_ready(store, accepted_brief):
                _event(store, "decision_rejected", actor, role, from_stage, from_stage,
                       f"accepted brief {accepted_brief_id} no longer valid; decision rejected",
                       linked_evidence, before,
                       extra={"brief_id": accepted_brief_id})
                raise DecisionRejectedError(f"accepted brief {accepted_brief_id} is no longer valid; decision rejected and recorded, stage unchanged")
        if report.get("snapshot_content_digest") != current_snapshot:
            _event(store, "decision_rejected", actor, role, from_stage, from_stage,
                   "judge snapshot stale: project content changed after the report",
                   linked_evidence, before,
                   extra={"judge_report_id": judge_report_id,
                          "report_snapshot_digest": report.get("snapshot_content_digest"),
                          "current_snapshot_digest": current_snapshot})
            raise DecisionRejectedError("judge snapshot is stale: project content changed after the report; decision rejected and recorded, stage unchanged")
    store["stage"] = to_stage
    return _event(store, "stage_transition", actor, role, from_stage, to_stage,
                  reason or "", linked_evidence, before,
                  extra={"brief_id": brief_id, "judge_report_id": judge_report_id})


def overview(store):
    stage = store["stage"]
    if stage == "INTAKE":
        blocked = "missing ready observation" if not any(observation_ready(o) for o in store["observations"]) else "awaiting owner transition to NEEDS_EVIDENCE"
        nxt = "record a ready observation" if not any(observation_ready(o) for o in store["observations"]) else "owner: transition to NEEDS_EVIDENCE"
    elif stage == "NEEDS_EVIDENCE":
        blocked = "missing ready observation" if not any(observation_ready(o) for o in store["observations"]) else "awaiting hypothesis draft"
        nxt = "record a ready observation" if not any(observation_ready(o) for o in store["observations"]) else "owner: transition to HYPOTHESIS_DRAFT"
    elif stage == "HYPOTHESIS_DRAFT":
        blocked = "missing reviewed inference" if not any(inference_ready(i) for i in store["inferences"]) else "awaiting owner review transition"
        nxt = "record and owner-review an inference" if not any(inference_ready(i) for i in store["inferences"]) else "owner: transition to OWNER_REVIEW"
    elif stage == "OWNER_REVIEW":
        blocked = "awaiting an approved brief and owner approval with reason"
        nxt = "owner: approve a brief, then transition to ACCEPTED_FOR_LOCAL_PROTOTYPE with brief id and reason"
    elif stage == "ACCEPTED_FOR_LOCAL_PROTOTYPE":
        blocked = "awaiting transition to JUDGE_REVIEW"
        nxt = "owner: transition to JUDGE_REVIEW"
    elif stage == "JUDGE_REVIEW":
        has = any(r["stage_at_creation"] == "JUDGE_REVIEW" and r.get("findings") and r.get("per_case") for r in store["judge_reports"])
        blocked = "missing usable judge report for JUDGE_REVIEW stage" if not has else "awaiting owner decision naming a current judge report"
        nxt = "judge: add a judge report with findings and per_case" if not has else "owner: record owner decision with judge report id and reason"
    else:
        blocked = "none - owner decision recorded"
        nxt = "none"
    ready_tasks = []
    for task in store["tasks"]:
        if task["state"] == "TODO":
            deps = [_find(store, "tasks", d) for d in task["dependencies"]]
            if all(d["state"] == "DONE" for d in deps):
                ready_tasks.append(task["id"])
    return {
        "project_id": store["project"]["id"],
        "room_id": store["project"]["room_id"],
        "stage": stage,
        "pain_status": store["project"]["pain_status"],
        "blocked_reason": blocked,
        "next_permitted_action": nxt,
        "owners": sorted({t["owner"] for t in store["tasks"]}),
        "evidence_count": len(store["evidence"]),
        "observation_count": len(store["observations"]),
        "ready_observation_count": sum(1 for o in store["observations"] if observation_ready(o)),
        "inference_count": len(store["inferences"]),
        "ready_inference_count": sum(1 for i in store["inferences"] if inference_ready(i)),
        "brief_count": len(store["briefs"]),
        "task_count": len(store["tasks"]),
        "judge_report_count": len(store["judge_reports"]),
        "review_receipt_count": len(store["review_receipts"]),
        "event_count": len(store["events"]),
        "store_revision": store["revision"],
        "ready_tasks": ready_tasks,
        "intake_count": len(store.get("intakes", {})),
        "proposal_count": len(store.get("proposals", {})),
        "decision_count": len(store.get("decisions", {})),
        "intake_ids": list(store.get("intakes", {}).keys()),
        "proposal_ids": list(store.get("proposals", {}).keys()),
        "decision_ids": list(store.get("decisions", {}).keys()),
        "proposal_views": [proposal_view(store, pid) for pid in store.get("proposals", {})],
        "judge_scope": "C4 collections only (observations, inferences, briefs, evidence, tasks); C5 intake, proposal, decision, and proposal task status freshness are NOT covered by Judge reports or verify snapshots in this slice.",
        "authority_model": "SIMULATED_ROLE_ARGUMENT_NOT_AUTHENTICATION",
        "live_adapters": "BLOCKED",
        "authentication": "NONE_IN_THIS_CLI",
    }


def verify(store, code_revision, artifacts=None, required_cases=None,
           plan_id=None, plan_revision=None, plan_digest=None):
    """Separate binding checks from implementation verification.

    binding_checks / mechanism_result: structural checks only (plan
    coverage, complete records, exit 0, command/environment/criteria,
    scope, timestamp, artifact bytes matching the claimed hash, and a
    judge receipt whose digest still matches). A binding_checks PASS
    proves only that the supplied records are structurally bound; it
    does NOT prove that any command actually ran, that the code
    revision corresponds to a real checkout, or that a trusted
    reviewer examined it. In this simulation, where caller-supplied
    strings and a simulated judge receipt are the only inputs, there
    is no trusted run/code/review binding, so implementation
    verification is always NOT_VERIFIED and the top-level verification
    field is never PASS. Synthetic positive tests must assert
    binding_checks, not an implementation verification PASS.
    """
    base = {
        "binding_checks": "INCONCLUSIVE",
        "mechanism_result": "INCONCLUSIVE",
        "implementation_verification": "NOT_VERIFIED",
        "verification": "INCONCLUSIVE",
        "plan_id": VERIFICATION_PLAN_ID,
        "plan_revision": VERIFICATION_PLAN_REVISION,
        "plan_digest": VERIFICATION_PLAN_DIGEST,
        # C5R1 (F05): legacy Judge/verify scope, stated explicitly.
        # Judge reports and verify snapshots freeze C4 collections
        # only; they do not freeze C5 intake, proposal, decision, or
        # proposal task status freshness. The snapshot domain is
        # deliberately NOT expanded here; a C5-specific Judge domain
        # would be separate work, not a silent repin.
        "judge_scope": "C4 collections only (observations, inferences, briefs, evidence, tasks); C5 intake, proposal, decision, and proposal task status freshness are NOT covered by Judge reports or verify snapshots in this slice.",
    }
    # Frozen plan: any override must match exactly, or it is rejected.
    if required_cases is not None and list(required_cases) != list(REQUIRED_VERIFICATION_CASES):
        base.update({"reason": "unbound plan override rejected: required_cases must equal the frozen plan exactly; empty, reduced, malformed or unrelated plans never yield a binding PASS"})
        return base
    if plan_id is not None and plan_id != VERIFICATION_PLAN_ID:
        base.update({"reason": "unbound plan override rejected: plan_id does not match the frozen plan"})
        return base
    if plan_revision is not None and plan_revision != VERIFICATION_PLAN_REVISION:
        base.update({"reason": "unbound plan override rejected: plan_revision does not match the frozen plan"})
        return base
    if plan_digest is not None and plan_digest != VERIFICATION_PLAN_DIGEST:
        base.update({"reason": "unbound plan override rejected: plan_digest does not match the frozen plan"})
        return base
    # Proof evaluation is blocked on an invalid history.
    hist = verify_history(store)
    if not hist["chain_valid"]:
        base.update({"reason": "history invalid; proof evaluation blocked: " + "; ".join(hist["failures"][:3])})
        return base
    if not code_revision:
        base.update({"reason": "no code revision supplied; verification cannot be bound to a revision"})
        return base
    records = [e for e in store["evidence"] if e["code_revision"] == code_revision]
    if not records:
        base.update({"binding_checks": "NOT_RUN", "mechanism_result": "NOT_RUN",
                     "verification": "NOT_RUN",
                     "reason": f"no evidence for code revision {code_revision}"})
        return base
    if any(e["result"] == "FAIL" for e in records):
        base.update({"binding_checks": "FAIL", "mechanism_result": "FAIL", "verification": "FAIL",
                     "reason": "at least one evidence record for this revision reports FAIL"})
        return base
    if any(e["exit_code"] not in (0, None) for e in records):
        base.update({"binding_checks": "FAIL", "mechanism_result": "FAIL", "verification": "FAIL",
                     "reason": "at least one evidence record has a nonzero exit code"})
        return base
    required = list(REQUIRED_VERIFICATION_CASES)
    by_case = {}
    for e in records:
        if e["result"] == "PASS":
            by_case.setdefault(e["test_case"], []).append(e)
    missing = [c for c in required if c not in by_case]
    if missing:
        base.update({"missing_cases": missing,
                     "reason": f"missing required cases for a binding PASS: {missing}"})
        return base
    chosen = []
    for case in required:
        candidate = None
        for e in by_case[case]:
            if (e["exit_code"] == 0 and e["command_or_steps"] and e["environment"]
                    and e["criteria_revision"] == CRITERIA_REVISION and e["scope_complete"]
                    and e["timestamp_utc"] and e["artifact_path"] and e["artifact_sha256"]):
                candidate = e
                break
        if candidate is None:
            base.update({"missing_cases": [case],
                         "reason": f"required case {case} has no complete, bound PASS record"})
            return base
        chosen.append(candidate)
    if artifacts is None:
        base.update({"reason": "no artifact resolver supplied; claimed hashes cannot be verified against actual bytes"})
        return base
    for e in chosen:
        data = artifacts.get(e["artifact_path"])
        if data is None:
            base.update({"reason": f"artifact missing for evidence {e['id']}: {e['artifact_path']}"})
            return base
        if hashlib.sha256(data).hexdigest() != e["artifact_sha256"]:
            base.update({"reason": f"artifact hash mismatch for evidence {e['id']}: claimed hash does not match actual bytes"})
            return base
    chosen_ids = {e["id"] for e in chosen}
    receipt_ok = False
    receipt_id = None
    for r in store["review_receipts"]:
        if r["decision"] != "REVIEWED_PASS":
            continue
        if not chosen_ids.issubset(set(r["evidence_ids"])):
            continue
        records_for_digest = sorted([e for e in store["evidence"] if e["id"] in r["evidence_ids"]],
                                    key=lambda x: x["id"])
        if _sha256_text(_canonical(records_for_digest)) == r["evidence_digest"]:
            receipt_ok = True
            receipt_id = r["id"]
            break
    if not receipt_ok:
        base.update({"reason": "no judge review receipt covers all chosen evidence records with a still-matching digest"})
        return base
    # Binding checks pass, but this is not implementation verification.
    base.update({
        "binding_checks": "PASS",
        "mechanism_result": "PASS",
        "verification": "INCONCLUSIVE",
        "reason": "binding checks pass (structural only); implementation verification remains INCONCLUSIVE because no trusted run/code/review binding exists in this simulation",
        "evidence_ids": [e["id"] for e in chosen],
        "review_receipt_id": receipt_id,
        "independent_review_established": False,
        "independent_review_note": "A judge role argument in this simulation is not authentication and does not prove independent review. A separate reviewer must still issue a verdict.",
        "scope": "binding_checks_only_not_implementation_verification_not_product_validation",
    })
    return base


def verify_history(store):
    """Check the audit hash chain AND anchor it to current state.

    Checks: schema version, genesis (an empty-event store must equal
    the pristine genesis exactly, including project configuration;
    for a non-empty chain, first event prev GENESIS and its
    before digest equals a pristine store digest), per-event revision
    sequence (before == previous after, after == before + 1),
    timestamp parseability, content digest format and continuity,
    event digest recomputation and prev links, and the final anchor:
    last event after_stage == current stage, last event
    store_revision_after == current revision, and last event
    content_digest_after == content_digest(current store). A changed
    observation, a changed revision, or changed event bytes without a
    full chain recompute therefore fails, as in V2_03. Diagnostic
    reads may use this result; privileged mutations and proof
    evaluation are blocked when it is invalid. This still does NOT
    protect against a storage owner who deliberately rewrites the
    entire history and recomputes every digest; that limit is stated
    in the returned tamper_limit.
    """
    failures = []
    if store.get("schema_version") != SCHEMA_VERSION:
        failures.append(f"schema mismatch: expected {SCHEMA_VERSION}, got {store.get('schema_version')}")
    events = store.get("events", [])
    if not events:
        # G01 (Rev4): an empty-event store must match the pristine
        # genesis EXACTLY, in canonical form, including project
        # configuration (id, room_id, pain_status, soul fields) and
        # every list, stage and revision. Checking only that lists
        # are empty allowed project fields to be changed without a
        # chain recompute while still reporting chain_valid=true.
        # A future explicitly bound genesis configuration would be
        # a separate, named genesis record; it is not implied here.
        pristine = new_store()
        if _canonical(store) != _canonical(pristine):
            differing = []
            for key in sorted(set(store) | set(pristine)):
                if _canonical(store.get(key)) != _canonical(pristine.get(key)):
                    differing.append(key)
            failures.append(
                "empty-event state does not match pristine genesis exactly; "
                f"differing top-level fields: {differing}")
        return {
            "chain_valid": not failures,
            "failures": failures,
            "event_count": 0,
            "tamper_limit": "Chain detects corruption and tampering without a full chain recompute. It is NOT tamper-proof against the storage owner, who can rewrite history and recompute digests.",
        }
    genesis_digest = content_digest(new_store())
    if events[0].get("prev_event_digest") != "GENESIS":
        failures.append("event 0: prev link is not GENESIS")
    if events[0].get("content_digest_before") != genesis_digest:
        failures.append("event 0: before digest does not match pristine genesis content")
    if events[0].get("store_revision_before") != 0:
        failures.append("event 0: revision before is not 0")
    prev_digest = "GENESIS"
    prev_after = None
    prev_after_revision = None
    for idx, event in enumerate(events):
        if event.get("prev_event_digest") != prev_digest:
            failures.append(f"event {idx}: prev link mismatch")
        if not event.get("timestamp_utc"):
            failures.append(f"event {idx}: missing timestamp")
        else:
            try:
                datetime.fromisoformat(event["timestamp_utc"].replace("Z", "+00:00"))
            except Exception:
                failures.append(f"event {idx}: timestamp does not parse")
        for field in ("content_digest_before", "content_digest_after"):
            val = event.get(field)
            if not isinstance(val, str) or not _HEX64.match(val):
                failures.append(f"event {idx}: {field} is not a 64-character hex digest")
        if event.get("store_revision_after") != event.get("store_revision_before", -1) + 1:
            failures.append(f"event {idx}: revision after is not before + 1")
        if prev_after_revision is not None and event.get("store_revision_before") != prev_after_revision:
            failures.append(f"event {idx}: revision before does not continue previous revision after")
        copied = {k: v for k, v in event.items() if k != "event_digest"}
        if _sha256_text(_canonical(copied)) != event.get("event_digest"):
            failures.append(f"event {idx}: event digest mismatch (tampered or recomputed incorrectly)")
        if prev_after is not None and event.get("content_digest_before") != prev_after:
            failures.append(f"event {idx}: content continuity break")
        prev_digest = event.get("event_digest")
        prev_after = event.get("content_digest_after")
        prev_after_revision = event.get("store_revision_after")
    last = events[-1]
    if last.get("store_revision_after") != store.get("revision"):
        failures.append(f"final anchor: last event revision after {last.get('store_revision_after')} != current revision {store.get('revision')}")
    if last.get("content_digest_after") != content_digest(store):
        failures.append("final anchor: last event content digest after does not match current store content digest")
    if last.get("after_stage") != store.get("stage"):
        failures.append(f"final anchor: last event after stage {last.get('after_stage')} != current stage {store.get('stage')}")
    return {
        "chain_valid": not failures,
        "failures": failures,
        "event_count": len(events),
        "tamper_limit": "Chain detects corruption and tampering without a full chain recompute. It is NOT tamper-proof against the storage owner, who can rewrite history and recompute digests.",
    }


def evidence_sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# C5 intake slice (revision 5, packet REV2.1 + checker fix F21).
#
# Thin local slice only: bounded file/stdin intake -> immutable intake
# record -> fixed-template proposal + computed view -> operator gate
# decision with required expected bindings -> audit/reload. No provider,
# worker, listener, scheduler, browser, or network is added here.
#
# Design rules, each traceable to the packet:
# - Input is read as bytes first. The byte cap (20,000) is enforced
#   before decode, then strict UTF-8 decode, then BOM (rejected, never
#   stripped), NUL, whitespace-only, and char cap (10,000 code points)
#   checks, in that order, so a failing input reports one deterministic
#   reason and creates no record.
# - Intake identity is SHA-256(original bytes + 0x00 + brief revision
#   + 0x00 + template version), first 16 hex chars, prefixed INTAKE-.
#   Proposal digest is SHA-256 of the canonical JSON payload (sorted
#   keys, (",", ":") separators, UTF-8), excluding digest, timestamps,
#   view, and decision fields. Decision id is SHA-256(proposal digest
#   + 0x00 + decision + 0x00 + reason), first 16 hex chars, prefixed
#   DEC-. Timestamps are never part of an id or digest.
# - Intake records are immutable: they are never edited in place.
#   A correction is a new record with a supersedes link; the old
#   record is unchanged. A duplicate input returns a duplicate
#   response only, plus a separate duplicate_submission event.
# - Proposal tasks are a fixed rule-based template (four tasks, fixed
#   roles, dependencies, reasons). They do not change with the input
#   text, with the project Soul configuration, or with any simulated
#   role argument. View fields (readiness, blocked_reason,
#   next_allowed_action) are computed at overview time and are not
#   part of the proposal payload or digest.
# - A decision is a local operator gate decision only, provenance
#   OPERATOR_ASSERTED. It is not owner authentication and not owner
#   product acceptance. The decide caller must supply expected
#   bindings copied from an operator-reviewed snapshot; the backend
#   recomputes the current digest and compares inside the same
#   load/lock/CAS save sequence as the decision write (the CLI owns
#   the lock and the CAS check). Missing or wrong-format bindings
#   are rejected with no decision and no event. A binding mismatch
#   is REJECTED_STALE: no decision, plus a decision_attempt_rejected
#   event. A rejected intake correction behaves the same way, with
#   its own rejection event, via IntakeRejectedError.
# - Rejected attempts that are format errors (cap, encoding, BOM,
#   NUL, whitespace, empty, path, unknown intake/proposal, blocked
#   dependency) create no event and no record, because they never
#   reach a stored object. Only duplicate submissions, correction
#   rejections, and stale decision attempts append an audit event
#   without creating a domain record; the packet names those events.
# - New domain record timestamps use UTC to the second
#   (YYYY-MM-DDTHH:MM:SSZ), matching the intake schema pattern. The
#   C4 event timestamp format (microseconds, parseable) is kept for
#   audit events, which are not intake schema records.
# - The C4 store structure is unchanged: new_store() has no C5 keys.
#   C5 functions create the intakes/proposals/decisions/
#   proposal_task_status collections on first use. An empty-event
#   store therefore still matches the pristine C4 genesis exactly,
#   and content_digest() omits empty C5 collections, so pre-C5
#   stores keep a valid history anchor.
# ---------------------------------------------------------------------------

INTAKE_BRIEF_REVISION = "PRODUCT_INTAKE_BRIEF_REV2"
INTAKE_TEMPLATE_VERSION = "INTAKE_TEMPLATE_V1"
INTAKE_BYTE_CAP = 20000
INTAKE_CHAR_CAP = 10000
INTAKE_BASELINE_FIELDS = [
    "redacted_example",
    "frequency_per_week",
    "manual_time_minutes",
    "manual_steps",
    "errors_per_occurrence",
    "desired_result",
]
INTAKE_DECISIONS = ("APPROVE", "REVISE", "REJECT", "DEFER")
_INTAKE_ID_RE = re.compile(r"^INTAKE-[0-9a-f]{16}$")
_HEX64_LOWER = re.compile(r"^[0-9a-f]{64}$")


class IntakeRejectedError(ControlError):
    """An intake correction was rejected after recording a rejection
    audit event in the store. Callers must save the store even though
    this error is raised, or the rejection history is lost. This
    mirrors DecisionRejectedError for stale gate decisions."""


def _utcnow_seconds():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _classify_line_endings(text):
    crlf = lf = cr = 0
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "\r":
            if i + 1 < len(text) and text[i + 1] == "\n":
                crlf += 1
                i += 2
            else:
                cr += 1
                i += 1
        elif ch == "\n":
            lf += 1
            i += 1
        else:
            i += 1
    kinds = []
    if crlf:
        kinds.append("CRLF")
    if lf:
        kinds.append("LF")
    if cr:
        kinds.append("bare-CR")
    if not kinds:
        return "none"
    if len(kinds) == 1:
        return kinds[0]
    return "mixed"


def _split_statements(text):
    parts = re.split(r"\r\n|\n|\r", text)
    return [p for p in parts if p != ""]


def _intake_id_for(raw_bytes):
    digest = hashlib.sha256(
        raw_bytes + b"\x00"
        + INTAKE_BRIEF_REVISION.encode("utf-8") + b"\x00"
        + INTAKE_TEMPLATE_VERSION.encode("utf-8")).hexdigest()
    return "INTAKE-" + digest[:16]


def _ensure_intake_collections(store):
    store.setdefault("intakes", {})
    store.setdefault("proposals", {})
    store.setdefault("decisions", {})
    store.setdefault("proposal_task_status", {})
    return store


def build_intake_record(raw_bytes, input_source, source_locator):
    """Validate raw input bytes and build an immutable intake record.

    Raises ControlError with a deterministic reason code and creates
    nothing on failure. This function does not touch the store, so
    it is safe to call before any store mutation."""
    if len(raw_bytes) > INTAKE_BYTE_CAP:
        raise ControlError(
            f"byte_cap_exceeded: input is {len(raw_bytes)} bytes, "
            f"cap {INTAKE_BYTE_CAP} bytes before decode; no record created")
    if len(raw_bytes) == 0:
        raise ControlError("empty_input: input is zero bytes; no record created")
    if raw_bytes.startswith(b"\xef\xbb\xbf"):
        raise ControlError(
            "bom_not_accepted: input starts with a UTF-8 BOM; "
            "BOM is rejected, never stripped; no record created")
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise ControlError(
            "invalid_utf8: input is not strict UTF-8; "
            "no replacement, no record created")
    if "\x00" in text:
        raise ControlError("nul_or_binary: input contains NUL; no record created")
    if text.strip() == "":
        raise ControlError("whitespace_only: input is whitespace only; no record created")
    if len(text) > INTAKE_CHAR_CAP:
        raise ControlError(
            f"char_cap_exceeded: input is {len(text)} characters, "
            f"cap {INTAKE_CHAR_CAP} code points; no record created")
    record = {
        "intake_id": _intake_id_for(raw_bytes),
        "brief_revision": INTAKE_BRIEF_REVISION,
        "template_version": INTAKE_TEMPLATE_VERSION,
        "created_utc": _utcnow_seconds(),
        "input_source": input_source,
        "source_locator": source_locator,
        "original_text": text,
        "original_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "original_length_bytes": len(raw_bytes),
        "original_length_chars": len(text),
        "input_encoding": "UTF-8",
        "bom": "absent",
        "line_endings": _classify_line_endings(text),
        "owner_statements": _split_statements(text),
        "proposed_interpretations": [],
        "unknowns": list(INTAKE_BASELINE_FIELDS),
        "baseline": {field: None for field in INTAKE_BASELINE_FIELDS},
        "baseline_provenance": {
            field: {"source": None, "supplied_utc": None, "note": None}
            for field in INTAKE_BASELINE_FIELDS
        },
        "duplicate_of": None,
        "supersedes": None,
    }
    return record


def add_intake(store, actor, raw_bytes, input_source, source_locator, supersedes=None):
    """Add an intake, a duplicate response, or a correction.

    Returns the new record for a fresh intake or a valid correction,
    and a duplicate response dict for a repeated input. Raises
    IntakeRejectedError (after appending a rejection event) for
    correction no-op / conflict / supersedes-not-found, and
    ControlError (no event, no record) for format errors."""
    before = content_digest(store)
    _ensure_intake_collections(store)
    record = build_intake_record(raw_bytes, input_source, source_locator)
    intake_id = record["intake_id"]
    if supersedes is not None:
        if supersedes not in store["intakes"]:
            _event(store, "correction_rejected_not_found", actor, "owner",
                   store["stage"], store["stage"],
                   f"correction supersedes not found: {supersedes}", None, before,
                   extra={"intake_id": intake_id, "supersedes": supersedes})
            raise IntakeRejectedError(
                f"correction_supersedes_not_found: supersedes id {supersedes} "
                "is not an existing intake; no record created")
        if intake_id == supersedes:
            _event(store, "correction_rejected_no_op", actor, "owner",
                   store["stage"], store["stage"],
                   f"correction is a no-op: same bytes as {supersedes}", None, before,
                   extra={"intake_id": intake_id, "supersedes": supersedes})
            raise IntakeRejectedError(
                "correction_no_op_same_bytes: correction bytes equal the "
                "original bytes; no new record created")
        if intake_id in store["intakes"]:
            _event(store, "correction_rejected_conflict", actor, "owner",
                   store["stage"], store["stage"],
                   f"correction conflicts: bytes already exist as {intake_id}, "
                   f"supersedes points elsewhere ({supersedes})", None, before,
                   extra={"intake_id": intake_id, "supersedes": supersedes})
            raise IntakeRejectedError(
                "correction_conflict_existing_id: correction bytes already "
                f"exist as {intake_id} while supersedes is {supersedes}; "
                "no overwrite, no new record")
        record["supersedes"] = supersedes
        store["intakes"][intake_id] = record
        _event(store, "intake_correction_created", actor, "owner",
               store["stage"], store["stage"],
               f"correction {intake_id} supersedes {supersedes}", None, before,
               extra={"intake_id": intake_id, "supersedes": supersedes})
        return record
    if intake_id in store["intakes"]:
        _event(store, "duplicate_submission", actor, "owner",
               store["stage"], store["stage"],
               f"duplicate intake submission for {intake_id}", None, before,
               extra={"intake_id": intake_id})
        return {
            "intake_id": intake_id,
            "duplicate": True,
            "duplicate_of": intake_id,
            "new_intake_created": False,
            "new_proposal_created": False,
            "event": "duplicate_submission",
            "note": "Original intake record unchanged.",
        }
    store["intakes"][intake_id] = record
    _event(store, "intake_created", actor, "owner",
           store["stage"], store["stage"],
           f"intake {intake_id} created", None, before,
           extra={"intake_id": intake_id})
    return record


def _proposal_payload(intake):
    proposal_id = "PROP-" + intake["intake_id"]
    tasks = [
        {
            "task_id": proposal_id + "-T01",
            "title": "Capture and preserve request",
            "role": "Intake Steward (simulated)",
            "depends_on": [],
            "reason": "Proposal needs a preserved, hashed intake before any analysis; capture is first because no later step may change the original.",
        },
        {
            "task_id": proposal_id + "-T02",
            "title": "Separate owner statements, interpretations and unknowns",
            "role": "Product Analyst (simulated)",
            "depends_on": [proposal_id + "-T01"],
            "reason": "Analysis needs separated statements; it cannot run before capture, and it must not invent facts.",
        },
        {
            "task_id": proposal_id + "-T03",
            "title": "Draft discovery proposal and dependency view",
            "role": "Product Analyst (simulated)",
            "depends_on": [proposal_id + "-T02"],
            "reason": "Proposal needs separated statements and unknowns; it is a rule-based template output, not agent coordination.",
        },
        {
            "task_id": proposal_id + "-T04",
            "title": "Owner review gate",
            "role": "Owner (real operator)",
            "depends_on": [proposal_id + "-T03"],
            "reason": "Only the owner/operator at the gate may approve, revise, reject or defer; simulated roles cannot decide.",
        },
    ]
    return {
        "proposal_id": proposal_id,
        "brief_revision": INTAKE_BRIEF_REVISION,
        "template_version": INTAKE_TEMPLATE_VERSION,
        "intake_id": intake["intake_id"],
        "intake_original_sha256": intake["original_sha256"],
        "tasks": tasks,
        "notes": [
            "Roles are simulated except Owner; this template does not assign a real worker.",
            "View fields (readiness, blocked_reason, next_allowed_action) are computed at overview time and are not part of this payload or its digest.",
        ],
    }


def _proposal_digest_for(payload):
    return hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()


def propose(store, actor, intake_id):
    """Create (or repeat) the fixed-template proposal for an intake.

    Returns a first-proposal dict for a new proposal, and the golden
    repeat shape (proposal_id, digest, already_exists, no new
    proposal) for a repeat. A repeat creates no event and no record."""
    before = content_digest(store)
    _ensure_intake_collections(store)
    if intake_id not in store["intakes"]:
        raise ControlError(f"intake not found: {intake_id}")
    proposal_id = "PROP-" + intake_id
    if proposal_id in store["proposals"]:
        stored = store["proposals"][proposal_id]
        return {
            "proposal_id": proposal_id,
            "proposal_digest": stored["proposal_digest"],
            "already_exists": True,
            "new_proposal_created": False,
            "note": "Same proposal returned; payload and digest unchanged.",
        }
    payload = _proposal_payload(store["intakes"][intake_id])
    digest = _proposal_digest_for(payload)
    created = _utcnow_seconds()
    store["proposals"][proposal_id] = {
        "proposal": payload,
        "proposal_digest": digest,
        "created_utc": created,
    }
    store["proposal_task_status"][proposal_id] = {
        task["task_id"]: "PENDING" for task in payload["tasks"]
    }
    _event(store, "proposal_created", actor, "owner",
           store["stage"], store["stage"],
           f"proposal {proposal_id} created for {intake_id}", None, before,
           extra={"proposal_id": proposal_id, "intake_id": intake_id})
    return {
        "proposal_id": proposal_id,
        "proposal_digest": digest,
        "created_utc": created,
        "proposal": payload,
        "already_exists": False,
        "new_proposal_created": True,
    }


def proposal_view(store, proposal_id):
    """Compute the dependency view for one proposal.

    The view is computed from the stored payload and the current
    proposal task status; it is never stored in the payload and
    never changes the payload digest. A DONE task reports readiness
    DONE with no next action, except for the Owner review gate task
    (see below). A pending task whose dependencies are all DONE
    reports READY; otherwise it reports BLOCKED with the
    not-yet-DONE dependencies and the first such dependency as the
    next action. The digest shown is recomputed from the current
    payload; a stored digest mismatch is flagged, not hidden.

    C5R1 (F04): the Owner review gate task (template T04, title
    "Owner review gate") is not completed into an approval. When it
    is READY, its next action points at the decide command with the
    required expected bindings from the operator-reviewed snapshot,
    not at completing the task. When it is DONE but no decision
    exists yet for this proposal, its next action still points at
    decide, so task DONE is never displayed as a gate decision.
    When a decision does exist, its next action is None. Decide
    itself has no all-tasks-DONE prerequisite: a matching-binding
    decision is allowed at any task state, as in the golden flow."""
    proposals = store.get("proposals", {})
    if proposal_id not in proposals:
        raise ControlError(f"proposal not found: {proposal_id}")
    stored = proposals[proposal_id]
    payload = stored["proposal"]
    digest = _proposal_digest_for(payload)
    view = {
        "proposal_id": proposal_id,
        "proposal_digest": digest,
        "view_note": "Computed view. View is not part of the proposal payload or digest.",
        "tasks": [],
    }
    if stored.get("proposal_digest") != digest:
        view["stored_proposal_digest_mismatch"] = True
    status = store.get("proposal_task_status", {}).get(proposal_id, {})
    has_decision = any(
        d.get("proposal_id") == proposal_id
        for d in store.get("decisions", {}).values())
    decide_action = (
        f"decide --proposal-id {proposal_id} "
        f"--expected-proposal-digest {digest} "
        f"--expected-brief-revision {payload['brief_revision']} "
        f"--expected-intake-id {payload['intake_id']} "
        "(from operator-reviewed snapshot)")
    for task in payload["tasks"]:
        tid = task["task_id"]
        state = status.get(tid, "PENDING")
        is_gate = task.get("title") == "Owner review gate"
        if state == "DONE":
            view["tasks"].append({
                "task_id": tid,
                "readiness": "DONE",
                "blocked_reason": None,
                # Gate DONE without a decision still points at decide,
                # so DONE is never displayed as an approval.
                "next_allowed_action": None if (not is_gate or has_decision) else decide_action,
            })
            continue
        pending = [d for d in task["depends_on"] if status.get(d, "PENDING") != "DONE"]
        if not pending:
            view["tasks"].append({
                "task_id": tid,
                "readiness": "READY",
                "blocked_reason": None,
                "next_allowed_action": decide_action if is_gate else f"complete {tid}",
            })
        else:
            view["tasks"].append({
                "task_id": tid,
                "readiness": "BLOCKED",
                "blocked_reason": "Depends on not-yet-DONE: " + ", ".join(pending),
                "next_allowed_action": f"complete {pending[0]}",
            })
    return view


def complete_proposal_task(store, actor, proposal_id, task_id):
    """Mark one proposal task DONE, only when its dependencies are DONE.

    Completing a proposal task changes only the computed view. It
    never changes the project stage, verification, proposal payload,
    proposal digest, or any decision. Completing the Owner review
    gate task (T04) records task status only; it does not create a
    gate decision. A repeat complete reports
    already_done and creates no new event. A blocked complete is
    rejected with no event and no change."""
    before = content_digest(store)
    _ensure_intake_collections(store)
    proposals = store["proposals"]
    if proposal_id not in proposals:
        raise ControlError(f"proposal not found: {proposal_id}")
    payload = proposals[proposal_id]["proposal"]
    task_ids = [t["task_id"] for t in payload["tasks"]]
    if task_id not in task_ids:
        raise ControlError(f"proposal task not found: {task_id}")
    status = store["proposal_task_status"].setdefault(proposal_id, {})
    if status.get(task_id) == "DONE":
        return {
            "proposal_id": proposal_id,
            "task_id": task_id,
            "state": "DONE",
            "already_done": True,
            "new_event_created": False,
            "note": "Task was already DONE; view unchanged.",
        }
    task = [t for t in payload["tasks"] if t["task_id"] == task_id][0]
    pending = [d for d in task["depends_on"] if status.get(d, "PENDING") != "DONE"]
    if pending:
        raise ControlError(
            "blocked_dependency: cannot complete "
            f"{task_id} while dependencies are not DONE: {', '.join(pending)}; "
            "no change made")
    status[task_id] = "DONE"
    _event(store, "proposal_task_completed", actor, "owner",
           store["stage"], store["stage"],
           f"proposal task {task_id} completed", None, before,
           extra={"proposal_id": proposal_id, "task_id": task_id})
    return {
        "proposal_id": proposal_id,
        "task_id": task_id,
        "state": "DONE",
        "already_done": False,
        "new_event_created": True,
    }


def _decision_id_for(proposal_digest, decision, reason):
    digest = hashlib.sha256(
        (proposal_digest + "\x00" + decision + "\x00" + reason).encode("utf-8")).hexdigest()
    return "DEC-" + digest[:16]


def decide(store, actor, proposal_id, expected_digest, expected_brief,
           expected_intake, decision, reason, operator_label, source_channel):
    """Record a local operator gate decision, or reject it.

    Format validation comes first (no event, no decision): decision
    must be one of the schema enums, reason/operator/source must be
    non-empty, expected digest must be 64 lowercase hex, expected
    intake id must match INTAKE-<16 lowercase hex>, expected brief
    must be non-empty. Then the current proposal payload digest,
    brief, and intake are recomputed and compared to the expected
    bindings; any mismatch raises DecisionRejectedError after
    appending a decision_attempt_rejected event (REJECTED_STALE).
    A repeat of an identical decision returns the existing decision
    with already_exists, without double-counting it."""
    if decision not in INTAKE_DECISIONS:
        raise ControlError(
            f"invalid_decision: decision must be one of {list(INTAKE_DECISIONS)}; "
            "no decision created")
    # C5R1 (F03): reason emptiness is validated with strip(), but the
    # stored reason and the decision_id use the reason verbatim, with
    # no trimming. Trimming changed the decision identity: a padded
    # reason previously produced the stripped reason's id.
    if not isinstance(reason, str) or not reason.strip():
        raise ControlError("invalid_decision_input: reason is required; no decision created")
    if not isinstance(operator_label, str) or not operator_label.strip():
        raise ControlError("invalid_decision_input: operator is required; no decision created")
    if not isinstance(source_channel, str) or not source_channel.strip():
        raise ControlError("invalid_decision_input: source is required; no decision created")
    if not isinstance(expected_digest, str) or not _HEX64_LOWER.match(expected_digest):
        raise ControlError(
            "invalid_expected_binding_format: expected proposal digest must be "
            "64 lowercase hex characters; no decision created")
    if not isinstance(expected_intake, str) or not _INTAKE_ID_RE.match(expected_intake):
        raise ControlError(
            "invalid_expected_binding_format: expected intake id must match "
            "INTAKE-<16 lowercase hex>; no decision created")
    if not isinstance(expected_brief, str) or not expected_brief.strip():
        raise ControlError(
            "invalid_expected_binding_format: expected brief revision is required; "
            "no decision created")
    before = content_digest(store)
    _ensure_intake_collections(store)
    proposals = store["proposals"]
    if proposal_id not in proposals:
        raise ControlError(f"proposal not found: {proposal_id}")
    payload = proposals[proposal_id]["proposal"]
    actual_digest = _proposal_digest_for(payload)
    actual_brief = payload["brief_revision"]
    actual_intake = payload["intake_id"]
    if (expected_digest != actual_digest or expected_brief != actual_brief
            or expected_intake != actual_intake):
        _event(store, "decision_attempt_rejected", actor, "owner",
               store["stage"], store["stage"],
               "REJECTED_STALE: expected bindings do not match current proposal",
               None, before,
               extra={"proposal_id": proposal_id,
                      "expected_proposal_digest": expected_digest,
                      "actual_proposal_digest": actual_digest,
                      "expected_brief_revision": expected_brief,
                      "actual_brief_revision": actual_brief,
                      "expected_intake_id": expected_intake,
                      "actual_intake_id": actual_intake})
        raise DecisionRejectedError(
            "REJECTED_STALE: expected bindings do not match the current "
            "proposal (digest, brief revision, or intake id); "
            "no decision created")
    decision_id = _decision_id_for(actual_digest, decision, reason)
    if decision_id in store["decisions"]:
        existing = store["decisions"][decision_id]
        if existing.get("proposal_id") != proposal_id:
            raise ControlError(
                "decision_id_collision: decision id already exists for a "
                "different proposal; no decision created")
        out = dict(existing)
        out["already_exists"] = True
        out["new_decision_created"] = False
        out["note"] = "Same decision returned; it is not double-counted."
        return out
    record = {
        "decision_id": decision_id,
        "proposal_id": proposal_id,
        "proposal_digest": actual_digest,
        "brief_revision": actual_brief,
        "intake_id": actual_intake,
        "decision": decision,
        "reason": reason,
        "operator_label": operator_label.strip(),
        "source_channel": source_channel.strip(),
        "provenance": "OPERATOR_ASSERTED",
        "decided_utc": _utcnow_seconds(),
    }
    store["decisions"][decision_id] = record
    _event(store, "decision_created", actor, "owner",
           store["stage"], store["stage"],
           f"decision {decision_id} ({decision}) for {proposal_id}", None, before,
           extra={"decision_id": decision_id, "proposal_id": proposal_id,
                  "provenance": "OPERATOR_ASSERTED"})
    out = dict(record)
    out["already_exists"] = False
    out["new_decision_created"] = True
    return out


# ---------------------------------------------------------------------------
# C6 contextual-intake slice (requirement docs/requirements/contextual-
# intake.md, owner policy: ask 2-3 questions first when information is
# missing; keep the original request; owner reviews the rewrite before
# any proposal). This section appends only: no C4/C5 function behaviour
# is changed, except content_digest() gains the C6 collections when
# non-empty (same pattern as C5), so C6 records are anchored by the
# history chain while pre-C6 stores keep an identical digest.
#
# Honest capability boundary, stated in code and docs, not marketing:
# - Completeness assessment is a RULE-BASED KEYWORD HEURISTIC
#   (CTX_KEYWORDS below, English + Vietnamese substrings), not
#   semantic understanding, not a model, not natural-language
#   reasoning. A dimension with no keyword hit is UNKNOWN, never
#   an invented fact.
# - Draft fields are supplied by the operator through the CLI; the
#   system structures them, binds them by digest, and gates them.
#   It does not generate goal/context/scope from the raw text.
# - A rewrite review and a contextual proposal are local operator
#   gate records with provenance OPERATOR_ASSERTED. They are not
#   authentication, not owner product acceptance, and not a
#   whole-system verdict.
# - Text in a raw request, a context source locator, an answer, or
#   any other record is DATA. No C6 function treats words such as
#   APPROVE, VERIFIED, upload, or send inside that text as an
#   approval, a verdict, or an external action. Only an explicit
#   ctx-review-rewrite call with a matching expected digest can
#   approve a rewrite, and only an explicit ctx-propose call with
#   matching bindings can create a contextual proposal.
# - The legacy fixed-template propose/decide flow is unchanged and
#   does NOT enforce this contextual policy. A legacy proposal is
#   never presented as a contextual proposal.
# - Optional baseline fields stay null unless supplied elsewhere;
#   a missing baseline never blocks clarification, draft, review,
#   or proposal in this slice.
# ---------------------------------------------------------------------------

CTX_REWRITE_VERSION = "CTX-REWRITE-V1"
CTX_DIMENSIONS = ("goal", "context", "scope", "desired_output")
CTX_TRUST_CLASSES = ("owner_statement", "reference", "external_text")
CTX_REWRITE_DECISIONS = INTAKE_DECISIONS
CTX_KEYWORDS = {
    "goal": ("mục tiêu", "muc tieu", "goal", "objective", "muốn đạt",
             "cần đạt", "want to", "aim"),
    "context": ("ngữ cảnh", "ngu canh", "bối cảnh", "context",
                "workflow", "quy trình", "khi ", "hiện tại"),
    "scope": ("phạm vi", "pham vi", "scope", "chỉ ", "only",
              "không bao gồm", "không gồm", "in scope", "out of scope"),
    "desired_output": ("đầu ra", "dau ra", "output", "kết quả",
                       "deliverable", "result", "báo cáo", "report"),
}
CTX_QUESTION_TEMPLATES = {
    "goal": "Mục tiêu cụ thể của yêu cầu này là gì (kết quả cần đạt, không phải cách làm)?",
    "context": "Ngữ cảnh và workflow hiện tại liên quan là gì (ai, khi nào, ở đâu trong quy trình)?",
    "scope": "Phạm vi của yêu cầu này là gì (bao gồm gì, và cố tình không bao gồm gì)?",
    "desired_output": "Đầu ra mong muốn cụ thể là gì (dạng nào, dùng để làm bước tiếp theo nào)?",
}
# C6R1 (F02): supplement question used ONLY to pad a one-missing
# batch to the 2-question minimum ctx-clarify accepts. It asks about
# additional constraints/unknowns (fields a draft already carries),
# never repeats information the raw text already supplied, and is
# not a dimension question: it covers no missing dimension.
CTX_SUPPLEMENT_QUESTION = (
    "Ngoài những thông tin đã cung cấp, còn ràng buộc, giới hạn hoặc "
    "điểm chưa rõ nào cần ghi rõ thêm trước khi viết lại yêu cầu không?"
)
CTX_EVENT_KINDS = (
    "ctx_source_added",
    "ctx_clarification_created",
    "ctx_clarification_answered",
    "ctx_rewrite_drafted",
    "ctx_rewrite_reviewed",
    "ctx_rewrite_review_rejected",
    "ctx_contextual_proposal_created",
    "ctx_contextual_proposal_rejected",
)


def _ensure_context_collections(store):
    store.setdefault("context_sources", {})
    store.setdefault("clarifications", {})
    store.setdefault("rewrites", {})
    store.setdefault("rewrite_reviews", {})
    store.setdefault("contextual_proposals", {})
    return store


# Only these kinds change the context a rewrite approval binds to. A
# review itself, a rejected review, and a rejected proposal do NOT
# change context: counting them would make every approval instantly
# stale by its own review event.
CTX_CHANGE_KINDS = (
    "ctx_source_added",
    "ctx_clarification_created",
    "ctx_clarification_answered",
    "ctx_rewrite_drafted",
)


def _ctx_event_count(store, intake_id):
    return sum(
        1 for e in store.get("events", [])
        if e.get("kind") in CTX_CHANGE_KINDS and e.get("intake_id") == intake_id
    )


def _ctx_latest_rewrite_id(store, intake_id):
    # Store files are written with sort_keys=True, so dict order after
    # a reload is alphabetical by rewrite id, NOT creation order.
    # Latest must therefore use the creation sequence recorded at
    # draft time (rewrites are never deleted, so the sequence is
    # monotonic). Records without a sequence (none are created by
    # this code) sort as 0.
    candidates = [r for r in store.get("rewrites", {}).values()
                  if r.get("intake_id") == intake_id]
    if not candidates:
        return None
    latest = max(candidates, key=lambda r: r.get("rewrite_seq", 0))
    return latest["rewrite_id"]


def _ctx_count_at_draft(store, rewrite):
    """Context-change count bound at a rewrite's draft time (count
    including the draft event itself).

    C6R1 (F01): a review/proposal must not silently adopt context
    events that arrived after the draft. New drafts record
    ctx_event_count_at_draft directly. Older C6 records lack the
    field; for them the count is reconstructed from the event
    history (change-kind events for this intake up to and including
    this rewrite's draft event). Returns None only if no draft
    event for the rewrite is found; callers then fall back to the
    draft source-ids comparison.
    """
    if "ctx_event_count_at_draft" in rewrite:
        return rewrite["ctx_event_count_at_draft"]
    count = 0
    for e in store.get("events", []):
        if e.get("kind") in CTX_CHANGE_KINDS and e.get("intake_id") == rewrite["intake_id"]:
            count += 1
            if (e.get("kind") == "ctx_rewrite_drafted"
                    and e.get("rewrite_id") == rewrite["rewrite_id"]):
                return count
    return None


def _ctx_open_clarifications(store, intake_id):
    return [c for c in store.get("clarifications", {}).values()
            if c["intake_id"] == intake_id and c["status"] == "WAITING_CLARIFICATION"]


def _ctx_current_source_ids(store, intake_id):
    return sorted(s["source_id"] for s in store.get("context_sources", {}).values()
                  if s["intake_id"] == intake_id)


def ctx_assess(store, intake_id):
    """Rule-based completeness assessment. Pure read: no store change,
    no record, no proposal. Missing dimensions are UNKNOWN, never
    filled with guessed facts. The method label is part of the output
    so a caller cannot mistake this keyword scan for semantic review.

    C6R1 (F02): dimensions_missing stays the full diagnostic list,
    but suggested_questions is an ACTIONABLE batch ctx-clarify
    accepts (exactly 2-3 questions): 0 when complete; the missing
    dimension's question plus the supplement question when exactly
    one dimension is missing; one question per missing dimension
    when 2-3 are missing; the first three dimensions in canonical
    order when all four are missing (the fourth stays missing and
    needs a follow-up clarification). suggested_questions_dimensions
    names the dimensions the batch's template questions cover; the
    supplement question covers no dimension.
    """
    intakes = store.get("intakes", {})
    if intake_id not in intakes:
        raise ControlError(f"intake not found: {intake_id}")
    text = intakes[intake_id].get("original_text", "").lower()
    present = {}
    missing = []
    for dim in CTX_DIMENSIONS:
        hit = any(kw in text for kw in CTX_KEYWORDS[dim])
        present[dim] = hit
        if not hit:
            missing.append(dim)
    if not missing:
        suggested = []
        suggested_dims = []
        batch_note = ("No dimension is missing; no clarification batch "
                      "is suggested.")
    elif len(missing) == 1:
        suggested = [CTX_QUESTION_TEMPLATES[missing[0]], CTX_SUPPLEMENT_QUESTION]
        suggested_dims = [missing[0]]
        batch_note = ("Only one dimension is missing, so the batch pairs "
                      "its question with a supplement question about "
                      "additional constraints/unknowns; it does not repeat "
                      "information already supplied.")
    elif len(missing) <= 3:
        suggested = [CTX_QUESTION_TEMPLATES[d] for d in missing]
        suggested_dims = list(missing)
        batch_note = "The batch covers every missing dimension."
    else:
        suggested_dims = list(CTX_DIMENSIONS[:3])
        suggested = [CTX_QUESTION_TEMPLATES[d] for d in suggested_dims]
        remaining = [d for d in missing if d not in suggested_dims]
        batch_note = ("Four dimensions are missing but ctx-clarify accepts "
                      "at most 3 questions, so the batch covers the first "
                      "three in canonical order; the remaining missing "
                      f"dimension(s) {remaining} need a follow-up clarification.")
    return {
        "intake_id": intake_id,
        "method": "RULE_HEURISTIC_KEYWORD_SCAN_V1",
        "method_note": "Keyword-substring scan only; not semantic understanding, "
                       "not a model, not natural-language reasoning.",
        "dimensions_present": present,
        "dimensions_missing": missing,
        "status": "COMPLETE" if not missing else "WAITING_CLARIFICATION",
        "suggested_questions": suggested,
        "suggested_questions_dimensions": suggested_dims,
        "suggested_questions_note": batch_note,
        "baseline_note": "Optional baseline fields remain null unless supplied "
                         "elsewhere; a missing baseline does not block this slice.",
    }


def ctx_add_source(store, actor, intake_id, source_id, locator, trust_class, note=None):
    before = content_digest(store)
    _ensure_context_collections(store)
    if intake_id not in store.get("intakes", {}):
        raise ControlError(f"intake not found: {intake_id}")
    if not _nonempty_text(source_id):
        raise ControlError("invalid_source: source id is required; no record created")
    if source_id in store["context_sources"]:
        raise ControlError(f"source already exists: {source_id}; no record created")
    if not _nonempty_text(locator):
        raise ControlError("invalid_source: locator is required; no record created")
    if trust_class not in CTX_TRUST_CLASSES:
        raise ControlError(
            f"invalid_source: trust class must be one of {list(CTX_TRUST_CLASSES)}; "
            "no record created")
    record = {
        "source_id": source_id,
        "intake_id": intake_id,
        "locator": locator,
        "trust_class": trust_class,
        "note": note,
        "source_sha256": None,
        "provenance": "LOCATOR_ONLY_NOT_FETCHED",
        "provenance_note": "Only the locator string is recorded; source content "
                          "was not fetched, read, or hash-verified by this command.",
        "created_utc": _utcnow_seconds(),
    }
    store["context_sources"][source_id] = record
    _event(store, "ctx_source_added", actor, "owner",
           store["stage"], store["stage"],
           f"context source {source_id} added for {intake_id}", None, before,
           extra={"intake_id": intake_id, "source_id": source_id})
    out = dict(record)
    out["new_source_created"] = True
    return out


def ctx_clarify(store, actor, intake_id, questions):
    before = content_digest(store)
    _ensure_context_collections(store)
    if intake_id not in store.get("intakes", {}):
        raise ControlError(f"intake not found: {intake_id}")
    if not isinstance(questions, (list, tuple)) or not (2 <= len(questions) <= 3):
        raise ControlError(
            "invalid_clarification: exactly 2 or 3 questions are required; "
            "no record created")
    if any(not _nonempty_text(q) for q in questions):
        raise ControlError("invalid_clarification: every question must be non-empty; "
                           "no record created")
    if len(set(q.strip() for q in questions)) != len(questions):
        raise ControlError("invalid_clarification: questions must be distinct; "
                           "no record created")
    assess = ctx_assess(store, intake_id)
    clarification_id = "CTXQ-" + hashlib.sha256(
        _canonical({"intake_id": intake_id, "questions": list(questions)}).encode("utf-8")
    ).hexdigest()[:16]
    if clarification_id in store["clarifications"]:
        existing = store["clarifications"][clarification_id]
        out = dict(existing)
        out["already_exists"] = True
        out["new_clarification_created"] = False
        out["note"] = "Same clarification returned; no new record, no new event."
        return out
    record = {
        "clarification_id": clarification_id,
        "intake_id": intake_id,
        "questions": list(questions),
        "asked_because_missing_dimensions": assess["dimensions_missing"],
        "answers": [],
        "status": "WAITING_CLARIFICATION",
        "created_utc": _utcnow_seconds(),
    }
    store["clarifications"][clarification_id] = record
    _event(store, "ctx_clarification_created", actor, "owner",
           store["stage"], store["stage"],
           f"clarification {clarification_id} created for {intake_id}", None, before,
           extra={"intake_id": intake_id, "clarification_id": clarification_id})
    out = dict(record)
    out["already_exists"] = False
    out["new_clarification_created"] = True
    return out


def ctx_answer(store, actor, clarification_id, answers):
    before = content_digest(store)
    _ensure_context_collections(store)
    clarifications = store["clarifications"]
    if clarification_id not in clarifications:
        raise ControlError(f"clarification not found: {clarification_id}")
    record = clarifications[clarification_id]
    if record["status"] != "WAITING_CLARIFICATION":
        raise ControlError(
            f"clarification already answered: {clarification_id}; no change made")
    if not isinstance(answers, (list, tuple)) or len(answers) != len(record["questions"]):
        raise ControlError(
            "invalid_answers: answer count must match question count; no change made")
    if any(not _nonempty_text(a) for a in answers):
        raise ControlError("invalid_answers: every answer must be non-empty; no change made")
    answered_utc = _utcnow_seconds()
    record["answers"] = [
        {"question": q, "answer": a, "answered_utc": answered_utc}
        for q, a in zip(record["questions"], answers)
    ]
    record["status"] = "ANSWERED"
    record["answered_utc"] = answered_utc
    _event(store, "ctx_clarification_answered", actor, "owner",
           store["stage"], store["stage"],
           f"clarification {clarification_id} answered", None, before,
           extra={"intake_id": record["intake_id"], "clarification_id": clarification_id})
    out = dict(record)
    out["new_answers_recorded"] = True
    return out


def _ctx_rewrite_payload(intake, goal, context, scope, desired_output,
                         constraints, unknowns, inferences, next_action,
                         source_ids, clarification_id, answers_snapshot,
                         assessment_missing_at_draft=None):
    return {
        "rewrite_version": CTX_REWRITE_VERSION,
        "intake_id": intake["intake_id"],
        "intake_original_sha256": intake["original_sha256"],
        "goal": goal,
        "context": context,
        "scope": scope,
        "desired_output": desired_output,
        "constraints": list(constraints),
        # Unknowns are operator-supplied only. Assessment-missing
        # dimensions are recorded separately, NOT merged into unknowns:
        # a draft supplies goal/context/scope/desired_output fields,
        # so those dimensions are addressed by the draft itself, and
        # listing them as unknown would misstate the draft.
        "unknowns": list(unknowns),
        "assessment_missing_at_draft": list(assessment_missing_at_draft or []),
        "labelled_inferences": list(inferences),
        "next_action": next_action,
        "source_ids": sorted(source_ids),
        "clarification_id": clarification_id,
        "answers_snapshot": list(answers_snapshot),
    }


def ctx_draft(store, actor, intake_id, goal, context, scope, desired_output,
              next_action, constraints=None, unknowns=None, inferences=None,
              clarification_id=None):
    before = content_digest(store)
    _ensure_context_collections(store)
    intakes = store.get("intakes", {})
    if intake_id not in intakes:
        raise ControlError(f"intake not found: {intake_id}")
    for name, value in (("goal", goal), ("context", context), ("scope", scope),
                        ("desired_output", desired_output), ("next_action", next_action)):
        if not _nonempty_text(value):
            raise ControlError(f"invalid_rewrite: {name} is required; no record created")
    open_clar = [c for c in store["clarifications"].values()
                 if c["intake_id"] == intake_id and c["status"] == "WAITING_CLARIFICATION"]
    if open_clar:
        raise ControlError(
            "clarification_open: an unanswered clarification exists for this intake; "
            "answer it before drafting; no record created")
    answers_snapshot = []
    if clarification_id is not None:
        clarifications = store["clarifications"]
        if clarification_id not in clarifications:
            raise ControlError(f"clarification not found: {clarification_id}")
        clar = clarifications[clarification_id]
        if clar["intake_id"] != intake_id:
            raise ControlError("clarification belongs to a different intake; no record created")
        if clar["status"] != "ANSWERED":
            raise ControlError("clarification is not answered yet; no record created")
        answers_snapshot = clar["answers"]
    assess = ctx_assess(store, intake_id)
    if assess["dimensions_missing"] and not answers_snapshot:
        raise ControlError(
            "missing_context: assessment reports missing dimensions "
            f"{assess['dimensions_missing']} and no answered clarification exists; "
            "ask 2-3 questions and answer them before drafting; no record created")
    parsed_inferences = []
    for raw_inf in (inferences or []):
        if not _nonempty_text(raw_inf) or ":" not in raw_inf:
            raise ControlError(
                "invalid_inference: each inference must be 'LABEL: text'; no record created")
        label, text = raw_inf.split(":", 1)
        if not _nonempty_text(label) or not _nonempty_text(text):
            raise ControlError(
                "invalid_inference: inference label and text must both be non-empty; "
                "no record created")
        parsed_inferences.append({"label": label.strip(), "text": text.strip(),
                                  "kind": "LABELLED_INFERENCE_NOT_FACT"})
    source_ids = sorted(s["source_id"] for s in store["context_sources"].values()
                        if s["intake_id"] == intake_id)
    payload = _ctx_rewrite_payload(
        intakes[intake_id], goal, context, scope, desired_output,
        constraints or [], list(unknowns or []), parsed_inferences, next_action,
        source_ids, clarification_id, answers_snapshot,
        assessment_missing_at_draft=assess["dimensions_missing"])
    digest = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
    rewrite_id = "RW-" + digest[:16]
    if rewrite_id in store["rewrites"]:
        existing = store["rewrites"][rewrite_id]
        out = dict(existing)
        out["already_exists"] = True
        out["new_rewrite_created"] = False
        out["note"] = "Same rewrite returned; payload and digest unchanged."
        return out
    record = dict(payload)
    record.update({
        "rewrite_id": rewrite_id,
        "rewrite_digest": digest,
        # Creation sequence for latest-rewrite ordering (see
        # _ctx_latest_rewrite_id: sorted-key reloads lose insertion order).
        "rewrite_seq": len(store["rewrites"]) + 1,
        # C6R1 (F01): context-change count including this draft event.
        # A later review/proposal must see exactly this count (plus no
        # new change event) or the draft is stale and needs a fresh
        # draft. Counted here, before the draft event is appended.
        "ctx_event_count_at_draft": _ctx_event_count(store, intake_id) + 1,
        "review_status": "DRAFT_NOT_REVIEWED",
        "review_id": None,
        "created_utc": _utcnow_seconds(),
    })
    store["rewrites"][rewrite_id] = record
    _event(store, "ctx_rewrite_drafted", actor, "owner",
           store["stage"], store["stage"],
           f"rewrite {rewrite_id} drafted for {intake_id}", None, before,
           extra={"intake_id": intake_id, "rewrite_id": rewrite_id})
    out = dict(record)
    out["already_exists"] = False
    out["new_rewrite_created"] = True
    return out


def ctx_review_rewrite(store, actor, rewrite_id, expected_digest, decision,
                       reason, operator_label, source_channel):
    if decision not in CTX_REWRITE_DECISIONS:
        raise ControlError(
            f"invalid_decision: decision must be one of {list(CTX_REWRITE_DECISIONS)}; "
            "no decision created")
    if not _nonempty_text(reason):
        raise ControlError("invalid_decision_input: reason is required; no decision created")
    if not _nonempty_text(operator_label):
        raise ControlError("invalid_decision_input: operator is required; no decision created")
    if not _nonempty_text(source_channel):
        raise ControlError("invalid_decision_input: source is required; no decision created")
    if not isinstance(expected_digest, str) or not _HEX64_LOWER.match(expected_digest):
        raise ControlError(
            "invalid_expected_binding_format: expected rewrite digest must be "
            "64 lowercase hex characters; no decision created")
    before = content_digest(store)
    _ensure_context_collections(store)
    rewrites = store["rewrites"]
    if rewrite_id not in rewrites:
        raise ControlError(f"rewrite not found: {rewrite_id}")
    rewrite = rewrites[rewrite_id]
    actual_digest = rewrite["rewrite_digest"]
    recomputed = hashlib.sha256(_canonical(
        _ctx_rewrite_payload(
            {"intake_id": rewrite["intake_id"],
             "original_sha256": rewrite["intake_original_sha256"]},
            rewrite["goal"], rewrite["context"], rewrite["scope"],
            rewrite["desired_output"], rewrite["constraints"], rewrite["unknowns"],
            rewrite["labelled_inferences"], rewrite["next_action"],
            rewrite["source_ids"], rewrite["clarification_id"],
            rewrite["answers_snapshot"],
            assessment_missing_at_draft=rewrite.get("assessment_missing_at_draft", [])
            )).encode("utf-8")).hexdigest()
    if expected_digest != actual_digest or recomputed != actual_digest:
        _event(store, "ctx_rewrite_review_rejected", actor, "owner",
               store["stage"], store["stage"],
               "REJECTED_STALE: expected rewrite digest does not match current rewrite",
               None, before,
               extra={"intake_id": rewrite["intake_id"], "rewrite_id": rewrite_id,
                      "expected_rewrite_digest": expected_digest,
                      "actual_rewrite_digest": actual_digest})
        raise DecisionRejectedError(
            "REJECTED_STALE: expected rewrite digest does not match the current "
            "rewrite (or the stored digest does not recompute); no decision created")
    # C6R1 (F01): an APPROVE binds the draft to the CURRENT context.
    # A pending clarification, or any context-change event after the
    # draft (new source, clarification, answer, or draft), makes the
    # draft stale: the approval is rejected and a fresh draft/review
    # is required. Non-approving decisions (REVISE/REJECT/DEFER) do not
    # enable a proposal, so they are not blocked here; a later APPROVE
    # of the same stale draft is still rejected by these checks.
    if decision == "APPROVE":
        if _ctx_open_clarifications(store, rewrite["intake_id"]):
            _event(store, "ctx_rewrite_review_rejected", actor, "owner",
                   store["stage"], store["stage"],
                   "clarification_open: an unanswered clarification exists for "
                   "this intake; answer it (or draft it into a fresh rewrite) "
                   "before approving",
                   None, before,
                   extra={"intake_id": rewrite["intake_id"], "rewrite_id": rewrite_id,
                          "expected_rewrite_digest": expected_digest,
                          "actual_rewrite_digest": actual_digest})
            raise DecisionRejectedError(
                "clarification_open: an unanswered clarification exists for this "
                "intake; no decision created")
        draft_count = _ctx_count_at_draft(store, rewrite)
        current_count = _ctx_event_count(store, rewrite["intake_id"])
        stale = False
        stale_reason = ""
        if draft_count is not None and current_count != draft_count:
            stale = True
            stale_reason = ("context changed after draft (new source, "
                            "clarification, answer, or draft)")
        elif _ctx_current_source_ids(store, rewrite["intake_id"]) != sorted(rewrite["source_ids"]):
            stale = True
            stale_reason = ("current context sources differ from the sources "
                            "bound in the draft")
        if stale:
            _event(store, "ctx_rewrite_review_rejected", actor, "owner",
                   store["stage"], store["stage"],
                   "REJECTED_STALE: " + stale_reason
                   + "; a fresh draft/review is required",
                   None, before,
                   extra={"intake_id": rewrite["intake_id"], "rewrite_id": rewrite_id,
                          "expected_rewrite_digest": expected_digest,
                          "actual_rewrite_digest": actual_digest})
            raise DecisionRejectedError(
                "REJECTED_STALE: " + stale_reason
                + "; a fresh draft/review is required; no decision created")
    review_id = "CTXR-" + hashlib.sha256(
        (actual_digest + "\x00" + decision + "\x00" + reason).encode("utf-8")
    ).hexdigest()[:16]
    if review_id in store["rewrite_reviews"]:
        existing = store["rewrite_reviews"][review_id]
        out = dict(existing)
        out["already_exists"] = True
        out["new_review_created"] = False
        out["note"] = "Same review returned; it is not double-counted."
        return out
    ctx_count = _ctx_event_count(store, rewrite["intake_id"])
    record = {
        "review_id": review_id,
        "rewrite_id": rewrite_id,
        "intake_id": rewrite["intake_id"],
        "rewrite_digest": actual_digest,
        "decision": decision,
        "reason": reason,
        "operator_label": operator_label.strip(),
        "source_channel": source_channel.strip(),
        "provenance": "OPERATOR_ASSERTED",
        "provenance_note": "Audit label only; not authentication and not product acceptance.",
        "ctx_event_count_at_review": ctx_count,
        "reviewed_utc": _utcnow_seconds(),
    }
    store["rewrite_reviews"][review_id] = record
    rewrite["review_status"] = decision
    rewrite["review_id"] = review_id
    _event(store, "ctx_rewrite_reviewed", actor, "owner",
           store["stage"], store["stage"],
           f"rewrite review {review_id} ({decision}) for {rewrite_id}", None, before,
           extra={"intake_id": rewrite["intake_id"], "rewrite_id": rewrite_id,
                  "review_id": review_id})
    out = dict(record)
    out["already_exists"] = False
    out["new_review_created"] = True
    return out


def _ctx_proposal_payload(rewrite, proposal_id):
    tasks = [
        {
            "task_id": proposal_id + "-T01",
            "title": "Preserve raw request and context sources",
            "role": "Intake Steward (simulated)",
            "depends_on": [],
            "reason": "The approved rewrite must stay bound to the exact raw bytes and recorded sources; nothing here rewrites the original.",
        },
        {
            "task_id": proposal_id + "-T02",
            "title": "Carry out the draft next_action as written",
            "role": "Planned step (not a live worker)",
            "depends_on": [proposal_id + "-T01"],
            "reason": "This task echoes the approved draft next_action verbatim; it is a plan step, not semantic agent assignment and not live execution.",
            "next_action_verbatim": rewrite["next_action"],
        },
        {
            "task_id": proposal_id + "-T03",
            "title": "Owner review gate for contextual proposal",
            "role": "Owner (real operator)",
            "depends_on": [proposal_id + "-T02"],
            "reason": "Only the owner/operator at the gate may approve, revise, reject or defer; simulated roles cannot decide.",
        },
    ]
    return {
        "proposal_id": proposal_id,
        "mode": "contextual",
        "mode_note": "Structured/rule-based template with approved-draft fields inserted "
                    "verbatim; not semantic routing and not a live worker assignment.",
        "intake_id": rewrite["intake_id"],
        "intake_original_sha256": rewrite["intake_original_sha256"],
        "approved_rewrite_id": rewrite["rewrite_id"],
        "approved_rewrite_digest": rewrite["rewrite_digest"],
        "rewrite_version": rewrite["rewrite_version"],
        "goal": rewrite["goal"],
        "context": rewrite["context"],
        "scope": rewrite["scope"],
        "desired_output": rewrite["desired_output"],
        "constraints": rewrite["constraints"],
        "unknowns": rewrite["unknowns"],
        "labelled_inferences": rewrite["labelled_inferences"],
        "next_action": rewrite["next_action"],
        "source_ids": rewrite["source_ids"],
        "answers_snapshot": rewrite["answers_snapshot"],
        "tasks": tasks,
    }


def ctx_propose(store, actor, intake_id, rewrite_id, expected_digest):
    if not isinstance(expected_digest, str) or not _HEX64_LOWER.match(expected_digest):
        raise ControlError(
            "invalid_expected_binding_format: expected rewrite digest must be "
            "64 lowercase hex characters; no proposal created")
    before = content_digest(store)
    _ensure_context_collections(store)
    rewrites = store["rewrites"]
    if rewrite_id not in rewrites:
        raise ControlError(f"rewrite not found: {rewrite_id}")
    rewrite = rewrites[rewrite_id]
    proposal_id = "CPROP-" + rewrite["rewrite_digest"][:16]

    def _reject(reason_text):
        _event(store, "ctx_contextual_proposal_rejected", actor, "owner",
               store["stage"], store["stage"], reason_text, None, before,
               extra={"intake_id": intake_id, "rewrite_id": rewrite_id,
                      "proposal_id": proposal_id})
        raise DecisionRejectedError(reason_text + "; no proposal created")

    if rewrite["intake_id"] != intake_id:
        _reject("REJECTED_STALE: rewrite belongs to a different intake")
    if expected_digest != rewrite["rewrite_digest"]:
        _reject("REJECTED_STALE: expected rewrite digest does not match current rewrite")
    if rewrite.get("review_status") != "APPROVE":
        _reject("rewrite_not_approved: contextual proposal requires an APPROVE "
                "review of the exact rewrite revision; "
                f"current review status is {rewrite.get('review_status')}")
    review = store["rewrite_reviews"].get(rewrite.get("review_id") or "")
    if review is None:
        _reject("rewrite_not_approved: no review record bound to this rewrite")
    # Repeat of an already-created proposal returns the frozen proposal
    # (its own bindings are unchanged); the stale checks below govern
    # only the creation of a NEW proposal after context changed.
    if proposal_id in store["contextual_proposals"]:
        stored = store["contextual_proposals"][proposal_id]
        out = dict(stored)
        out["already_exists"] = True
        out["new_proposal_created"] = False
        out["note"] = "Same contextual proposal returned; payload and digest unchanged."
        return out
    if _ctx_latest_rewrite_id(store, intake_id) != rewrite_id:
        _reject("REJECTED_STALE: a newer rewrite exists for this intake; "
                "the approved rewrite is no longer the latest")
    if _ctx_event_count(store, intake_id) != review["ctx_event_count_at_review"]:
        _reject("REJECTED_STALE: context changed after rewrite approval "
                "(new source, clarification, answer, or draft); "
                "a fresh review of the current rewrite is required")
    # C6R1 (F01), defense in depth for approvals recorded before this
    # fix: the draft itself must still be current. A pending
    # clarification, a context change after the draft, or current
    # sources differing from the draft's bound sources all reject the
    # new proposal; a fresh draft/review is required. (A repeat of an
    # already-created proposal returned above; these checks govern
    # only the creation of a NEW proposal.)
    if _ctx_open_clarifications(store, intake_id):
        _reject("clarification_open: an unanswered clarification exists for "
                "this intake; a fresh draft/review is required")
    draft_count = _ctx_count_at_draft(store, rewrite)
    if draft_count is not None and _ctx_event_count(store, intake_id) != draft_count:
        _reject("REJECTED_STALE: context changed after draft (new source, "
                "clarification, answer, or draft); "
                "a fresh draft/review is required")
    if _ctx_current_source_ids(store, intake_id) != sorted(rewrite["source_ids"]):
        _reject("REJECTED_STALE: current context sources differ from the "
                "sources bound in the draft; a fresh draft/review is required")
    payload = _ctx_proposal_payload(rewrite, proposal_id)
    digest = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
    record = {
        "proposal_id": proposal_id,
        "proposal_digest": digest,
        "proposal": payload,
        "created_utc": _utcnow_seconds(),
    }
    store["contextual_proposals"][proposal_id] = record
    _event(store, "ctx_contextual_proposal_created", actor, "owner",
           store["stage"], store["stage"],
           f"contextual proposal {proposal_id} created for {intake_id}", None, before,
           extra={"intake_id": intake_id, "rewrite_id": rewrite_id,
                  "proposal_id": proposal_id})
    out = dict(record)
    out["already_exists"] = False
    out["new_proposal_created"] = True
    return out


def ctx_status(store, intake_id):
    _ensure_context_collections(store)
    intakes = store.get("intakes", {})
    if intake_id not in intakes:
        raise ControlError(f"intake not found: {intake_id}")
    intake = intakes[intake_id]
    sources = [s for s in store["context_sources"].values() if s["intake_id"] == intake_id]
    clarifications = [c for c in store["clarifications"].values() if c["intake_id"] == intake_id]
    rewrites = [r for r in store["rewrites"].values() if r["intake_id"] == intake_id]
    proposals = [p for p in store["contextual_proposals"].values()
                 if p["proposal"]["intake_id"] == intake_id]
    legacy_proposal_id = "PROP-" + intake_id
    return {
        "intake_id": intake_id,
        "intake_original_sha256": intake["original_sha256"],
        "baseline": intake.get("baseline"),
        "baseline_note": "Optional baseline stays null unless supplied elsewhere; "
                         "it does not block this slice.",
        "assessment": ctx_assess(store, intake_id),
        "context_sources": sources,
        "clarifications": clarifications,
        "rewrites": rewrites,
        "contextual_proposals": proposals,
        "legacy_proposal_exists": legacy_proposal_id in store.get("proposals", {}),
        "legacy_note": "A legacy fixed-template proposal, if present, does NOT "
                      "enforce the contextual policy and is not a contextual proposal.",
        "mode": "contextual" if proposals else "legacy_or_contextual_pending",
    }


def ctx_rewrite_view(store, rewrite_id):
    rewrites = store.get("rewrites", {})
    if rewrite_id not in rewrites:
        raise ControlError(f"rewrite not found: {rewrite_id}")
    record = rewrites[rewrite_id]
    payload = _ctx_rewrite_payload(
        {"intake_id": record["intake_id"],
         "original_sha256": record["intake_original_sha256"]},
        record["goal"], record["context"], record["scope"],
        record["desired_output"], record["constraints"], record["unknowns"],
        record["labelled_inferences"], record["next_action"],
        record["source_ids"], record["clarification_id"],
        record["answers_snapshot"],
        assessment_missing_at_draft=record.get("assessment_missing_at_draft", []))
    digest = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
    view = dict(record)
    view["recomputed_digest"] = digest
    view["stored_digest_mismatch"] = digest != record["rewrite_digest"]
    return view


def ctx_proposal_view(store, proposal_id):
    proposals = store.get("contextual_proposals", {})
    if proposal_id not in proposals:
        raise ControlError(f"contextual proposal not found: {proposal_id}")
    stored = proposals[proposal_id]
    payload = stored["proposal"]
    digest = hashlib.sha256(_canonical(payload).encode("utf-8")).hexdigest()
    view = dict(stored)
    view["recomputed_digest"] = digest
    view["stored_digest_mismatch"] = digest != stored["proposal_digest"]
    return view
