"""Pydantic transport mirror of the bigraph-schema contracts.

The bigraph-schema types (schema.py) are canonical; these mirror them for
request/response validation at API boundaries (FastAPI). Keep field names
identical — they ARE the same contract in two representations.
"""
from __future__ import annotations

from typing import Any, Literal, Optional
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
