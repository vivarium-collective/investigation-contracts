from investigation_contracts.chain import validate_chain


def _finding(i, runs=("run/1",)):
    return {"id": f"finding/{i}", "type": "finding", "lifecycle_state": "proposed", "runs": list(runs)}

def _evidence(i, findings=("finding/f1",), hyps=("H",), state="proposed"):
    return {"id": f"evidence/{i}", "type": "evidence", "lifecycle_state": state,
            "findings": list(findings), "hypotheses": list(hyps), "confidence": 0.5}

def _decision(i, evidence=("evidence/e1",), outcome="accept"):
    return {"id": f"decision/{i}", "type": "decision", "lifecycle_state": "recorded",
            "evidence": list(evidence), "outcome": outcome}

def _conclusion(i, evidence=("evidence/e1",), decisions=("decision/d1",)):
    return {"id": f"conclusion/{i}", "type": "conclusion", "lifecycle_state": "draft",
            "evidence": list(evidence), "decisions": list(decisions)}

def _idx(*nodes):
    return {n["id"]: n for n in nodes}


def test_sound_chain_has_no_violations():
    nodes = _idx(_finding("f1"), _evidence("e1", state="accepted"),
                 _decision("d1"), _conclusion("c1"))
    assert validate_chain(nodes) == []

def test_finding_without_run():
    nodes = _idx(_finding("f1", runs=()))
    v = validate_chain(nodes)
    assert any(x["invariant"] == "finding->run" for x in v)

def test_evidence_without_finding():
    nodes = _idx(_evidence("e1", findings=()))
    v = validate_chain(nodes)
    assert any(x["invariant"] == "evidence->finding" for x in v)

def test_evidence_finding_ref_unresolved():
    nodes = _idx(_evidence("e1", findings=("finding/nope",), hyps=("H",)))
    v = validate_chain(nodes)
    assert any(x["invariant"] == "evidence->finding" for x in v)

def test_evidence_without_hypothesis():
    nodes = _idx(_finding("f1"), _evidence("e1", hyps=("", "  ")))
    v = validate_chain(nodes)
    assert any(x["invariant"] == "evidence->hypothesis" for x in v)

def test_conclusion_evidence_not_accepted():
    nodes = _idx(_finding("f1"), _evidence("e1", state="proposed"),
                 _decision("d1"), _conclusion("c1"))
    v = validate_chain(nodes)
    assert any(x["invariant"] == "conclusion->accepted" and x["node_id"] == "conclusion/c1" for x in v)

def test_conclusion_no_accepting_decision():
    nodes = _idx(_finding("f1"), _evidence("e1", state="accepted"),
                 _conclusion("c1", decisions=()))   # no decision referenced
    v = validate_chain(nodes)
    assert any(x["invariant"] == "conclusion->decision" and x["node_id"] == "conclusion/c1" for x in v)

def test_conclusion_accept_decision_not_referenced():
    nodes = _idx(_finding("f1"), _evidence("e1", state="accepted"),
                 _decision("d1", evidence=("evidence/e1",), outcome="accept"),
                 _conclusion("c1", evidence=("evidence/e1",), decisions=()))  # decision NOT referenced
    v = validate_chain(nodes)
    assert any(x["invariant"] == "conclusion->decision" and x["node_id"] == "conclusion/c1" for x in v)
