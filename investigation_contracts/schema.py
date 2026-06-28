"""Bigraph-schema types for the Actionable Investigation Graph contracts (RFC-0002).

Built on a discovery-free ``Core(BASE_TYPES)`` — NEVER ``allocate_core()`` (it
triggers package discovery, which is broken in this environment).
"""
from __future__ import annotations

import bigraph_schema

SCHEMA_VERSION = 1
EVENT_TYPES = ("FindingCreated", "EvidenceLinked", "DecisionRecorded", "ConclusionPublished")

ACTOR_KIND = {"_type": "enum", "_values": ["human", "agentic", "computational", "shared"]}
EVENT_TYPE = {"_type": "enum", "_values": list(EVENT_TYPES)}
VALIDATION_STATUS = {"_type": "enum", "_values": ["ok", "unresolved", "invalid", "unverified"]}
DECISION_OUTCOME = {"_type": "enum", "_values": ["accept", "reject", "defer"]}

PROVENANCE = {
    "actor": "actor_kind",
    "agent_id": "string",
    "timestamp": "string",
    "source_objects": "list[string]",
    "justification": "string",
    "tool": "string",
    "commit": "string",
}

INVESTIGATION_NODE_FIELDS = {
    "id": "string",
    "type": "string",
    "lifecycle_state": "string",
    "owner": "actor_kind",
    "provenance": "provenance",
    "validation_status": "validation_status",
}

TRANSITION = {"from": "string", "to": "string"}

EVENT_ENVELOPE = {
    "event_id": "string",
    "type": "event_type",
    "occurred_at": "string",
    "actor": "actor_kind",
    "subject": "string",
    "transition": "transition",
    "provenance": "provenance",
    "payload": "tree",
    "schema_version": "integer",
}


def make_core() -> "bigraph_schema.Core":
    core = bigraph_schema.Core(bigraph_schema.BASE_TYPES)
    core.register_type("actor_kind", ACTOR_KIND)
    core.register_type("event_type", EVENT_TYPE)
    core.register_type("validation_status", VALIDATION_STATUS)
    core.register_type("provenance", PROVENANCE)
    core.register_type("transition", TRANSITION)
    core.register_type("decision_outcome", DECISION_OUTCOME)
    core.register_type("investigation_node", dict(INVESTIGATION_NODE_FIELDS))
    core.register_type("finding", {**INVESTIGATION_NODE_FIELDS,
                                   "statement": "string", "runs": "list[string]"})
    core.register_type("evidence", {**INVESTIGATION_NODE_FIELDS,
                                    "findings": "list[string]", "hypotheses": "list[string]",
                                    "confidence": "float", "statement": "string"})
    core.register_type("decision", {**INVESTIGATION_NODE_FIELDS,
                                    "evidence": "list[string]", "outcome": "decision_outcome",
                                    "rationale": "string", "decided_by": "string"})
    core.register_type("conclusion", {**INVESTIGATION_NODE_FIELDS,
                                      "evidence": "list[string]", "decisions": "list[string]",
                                      "hypotheses": "list[string]", "statement": "string"})
    core.register_type("event_envelope", EVENT_ENVELOPE)
    return core


_CORE = None


def _core() -> "bigraph_schema.Core":
    global _CORE
    if _CORE is None:
        _CORE = make_core()
    return _CORE


def validate_envelope(d: dict) -> tuple[bool, str | None]:
    """Return ``(ok, error)`` — structural validation against ``event_envelope``."""
    try:
        if not isinstance(d, dict):
            return False, "envelope must be a dict"
        if d.get("type") not in EVENT_TYPES:
            return False, f"unknown event type: {d.get('type')!r}"
        ok = _core().check("event_envelope", d)
        return (True, None) if ok else (False, "envelope failed event_envelope type check")
    except Exception as e:  # noqa: BLE001 — validation must never raise
        return False, f"validation error: {e}"
