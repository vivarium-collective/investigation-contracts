from investigation_contracts.schema import make_core, EVENT_TYPES


def _node(t, **extra):
    base = {"id": f"{t}/x", "type": t, "lifecycle_state": "proposed", "owner": "shared",
            "provenance": {"actor": "agentic", "agent_id": "p", "timestamp": "t",
                           "source_objects": [], "justification": "j", "tool": "", "commit": ""},
            "validation_status": "ok"}
    base.update(extra); return base


def test_new_event_types_registered():
    for e in ("EvidenceLinked", "DecisionRecorded", "ConclusionPublished"):
        assert e in EVENT_TYPES


def test_evidence_type_checks():
    core = make_core()
    good = _node("evidence", findings=["finding/f1"], hypotheses=["H rises"], confidence=0.8, statement="s")
    assert core.check("evidence", good) is True
    bad = _node("evidence", findings=["finding/f1"], hypotheses=["H"], confidence="high", statement="s")  # confidence wrong type
    assert core.check("evidence", bad) is False


def test_decision_type_checks_outcome_enum():
    core = make_core()
    good = _node("decision", owner="human", lifecycle_state="recorded",
                 evidence=["evidence/e1"], outcome="accept", rationale="r", decided_by="curator")
    assert core.check("decision", good) is True
    bad = dict(good); bad["outcome"] = "maybe"
    assert core.check("decision", bad) is False


def test_conclusion_type_checks():
    core = make_core()
    good = _node("conclusion", owner="human", lifecycle_state="draft",
                 evidence=["evidence/e1"], decisions=["decision/d1"], hypotheses=["H"], statement="s")
    assert core.check("conclusion", good) is True
