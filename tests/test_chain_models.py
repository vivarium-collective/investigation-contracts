from investigation_contracts.models import (EvidenceCreateBody, DecisionCreateBody, ConclusionCreateBody)


def test_evidence_body():
    b = EvidenceCreateBody(study="demo", findings=["finding/f1"], hypotheses=["H rises"],
                           confidence=0.7, statement="s")
    assert b.findings == ["finding/f1"] and b.confidence == 0.7


def test_decision_body_outcome_enum():
    DecisionCreateBody(study="demo", evidence=["evidence/e1"], outcome="accept", rationale="r")
    import pytest
    with pytest.raises(Exception):
        DecisionCreateBody(study="demo", evidence=["evidence/e1"], outcome="maybe")


def test_conclusion_body():
    c = ConclusionCreateBody(study="demo", evidence=["evidence/e1"], decisions=["decision/d1"],
                             hypotheses=["H"], statement="s")
    assert c.decisions == ["decision/d1"]
