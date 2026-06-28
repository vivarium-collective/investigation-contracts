"""Canonical reader for the append-only event log (shared by both spines)."""
from __future__ import annotations

import json
from pathlib import Path


def read_log(path: str | Path, cursor: str | None = None, types: list[str] | None = None) -> list[dict]:
    """Return events from the JSONL log at path, optionally after cursor and filtered by types."""
    p = Path(path)
    if not p.is_file():
        return []
    out: list[dict] = []
    passed_cursor = cursor is None
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:  # noqa: BLE001 — skip malformed, never fatal
            continue
        if not passed_cursor:
            if ev.get("event_id") == cursor:
                passed_cursor = True
            continue
        if types is not None and ev.get("type") not in types:
            continue
        out.append(ev)
    return out
