from investigation_contracts.schema import make_core, validate_envelope, SCHEMA_VERSION


def _good_envelope():
    return {
        "event_id": "0000000001",
        "type": "FindingCreated",
        "occurred_at": "2026-06-28T00:00:00Z",
        "actor": "agentic",
        "subject": "finding/abc123",
        "transition": {"from": "", "to": "proposed"},
        "provenance": {"actor": "agentic", "agent_id": "planner", "timestamp": "t",
                       "source_objects": [], "justification": "j", "tool": "", "commit": ""},
        "payload": {"study": "demo"},
        "schema_version": SCHEMA_VERSION,
    }


def test_core_registers_contract_types():
    core = make_core()
    assert core.check("event_envelope", _good_envelope()) is True
    assert core.check("provenance", _good_envelope()["provenance"]) is True


def test_validate_envelope_accepts_good():
    ok, err = validate_envelope(_good_envelope())
    assert ok is True and err is None


def test_validate_envelope_rejects_bad_type_and_missing_fields():
    bad = {"event_id": 123, "type": "FindingCreated"}  # wrong type + missing fields
    ok, err = validate_envelope(bad)
    assert ok is False and isinstance(err, str)


def test_validate_envelope_rejects_unknown_event_type():
    e = _good_envelope(); e["type"] = "NotARealEvent"
    ok, err = validate_envelope(e)
    assert ok is False
