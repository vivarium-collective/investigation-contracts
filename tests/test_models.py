from investigation_contracts.models import FindingCreateBody, EventEnvelope


def test_finding_create_body():
    b = FindingCreateBody(study="demo", statement="X up with Y", runs=["run/1"])
    assert b.study == "demo" and b.runs == ["run/1"]


def test_event_envelope_roundtrips_to_contract_dict():
    from investigation_contracts.schema import validate_envelope
    env = EventEnvelope(
        event_id="01", type="FindingCreated", occurred_at="t", actor="agentic",
        subject="finding/x", transition={"from": "", "to": "proposed"},
        provenance={"actor": "agentic", "agent_id": "p", "timestamp": "t",
                    "source_objects": [], "justification": "j", "tool": "", "commit": ""},
        payload={"study": "demo"}, schema_version=1)
    ok, err = validate_envelope(env.model_dump())
    assert ok is True, err
