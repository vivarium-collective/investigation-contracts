from investigation_contracts.lifecycle import check_transition, initial_state


def test_initial_states():
    assert initial_state("evidence") == "proposed"
    assert initial_state("decision") == "pending"
    assert initial_state("conclusion") == "draft"


def test_evidence_transitions():
    assert check_transition("evidence", "proposed", "accepted") is True
    assert check_transition("evidence", "proposed", "rejected") is True
    assert check_transition("evidence", "accepted", "proposed") is False


def test_decision_transitions():
    assert check_transition("decision", "pending", "recorded") is True
    assert check_transition("decision", "recorded", "pending") is False


def test_conclusion_transitions():
    assert check_transition("conclusion", "draft", "published") is True
    assert check_transition("conclusion", "published", "draft") is False
