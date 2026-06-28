"""Pydantic transport mirror of the bigraph-schema contracts.

The bigraph-schema types (schema.py) are canonical; these mirror them for
request/response validation at API boundaries (FastAPI). Keep field names
identical — they ARE the same contract in two representations.
"""
from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field


class Provenance(BaseModel):
    actor: Literal["human", "agentic", "computational"]
    agent_id: str = ""
    timestamp: str = ""
    source_objects: list[str] = Field(default_factory=list)
    justification: str = ""
    tool: str = ""
    commit: str = ""


class EventEnvelope(BaseModel):
    event_id: str
    type: Literal["FindingCreated"]
    occurred_at: str
    actor: Literal["human", "agentic", "computational"]
    subject: str
    transition: dict
    provenance: Provenance
    payload: dict
    schema_version: int


class Finding(BaseModel):
    id: str
    type: Literal["finding"] = "finding"
    lifecycle_state: str = "proposed"
    owner: Literal["shared"] = "shared"
    provenance: Provenance
    validation_status: Literal["ok", "unresolved", "invalid", "unverified"] = "ok"
    statement: str
    runs: list[str] = Field(default_factory=list)


class FindingCreateBody(BaseModel):
    study: str
    statement: str
    runs: list[str] = Field(default_factory=list)
    hypothesis: Optional[str] = None


class Evidence(BaseModel):
    id: str
    type: Literal["evidence"] = "evidence"
    lifecycle_state: str = "proposed"
    owner: Literal["shared"] = "shared"
    provenance: Provenance
    validation_status: Literal["ok", "unresolved", "invalid", "unverified"] = "ok"
    findings: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    statement: str = ""


class Decision(BaseModel):
    id: str
    type: Literal["decision"] = "decision"
    lifecycle_state: str = "recorded"
    owner: Literal["human"] = "human"
    provenance: Provenance
    validation_status: Literal["ok", "unresolved", "invalid", "unverified"] = "ok"
    evidence: list[str] = Field(default_factory=list)
    outcome: Literal["accept", "reject", "defer"]
    rationale: str = ""
    decided_by: str = ""


class Conclusion(BaseModel):
    id: str
    type: Literal["conclusion"] = "conclusion"
    lifecycle_state: str = "draft"
    owner: Literal["human"] = "human"
    provenance: Provenance
    validation_status: Literal["ok", "unresolved", "invalid", "unverified"] = "ok"
    evidence: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    statement: str = ""


class EvidenceCreateBody(BaseModel):
    study: str
    findings: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    statement: str = ""


class DecisionCreateBody(BaseModel):
    study: str
    evidence: list[str] = Field(default_factory=list)
    outcome: Literal["accept", "reject", "defer"]
    rationale: str = ""
    decided_by: str = ""


class ConclusionCreateBody(BaseModel):
    study: str
    evidence: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    statement: str = ""
