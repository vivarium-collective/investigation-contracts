from investigation_contracts.lifecycle import check_transition, initial_state
from investigation_contracts.schema import make_core


def test_finding_initial_state():
    assert initial_state("finding") == "proposed"


def test_finding_legal_transition():
    assert check_transition("finding", "proposed", "reviewed") is True
    assert check_transition("finding", "reviewed", "accepted") is True


def test_finding_illegal_transition_rejected():
    assert check_transition("finding", "accepted", "proposed") is False
    assert check_transition("finding", "proposed", "accepted") is False  # must go via reviewed


def test_unknown_node_type_rejects():
    assert check_transition("does_not_exist", "a", "b") is False


def test_finding_node_type_checks():
    core = make_core()
    good = {"id": "finding/x", "type": "finding", "lifecycle_state": "proposed",
            "owner": "shared", "provenance": {"actor": "agentic", "agent_id": "p",
            "timestamp": "t", "source_objects": [], "justification": "j", "tool": "", "commit": ""},
            "validation_status": "ok", "statement": "X rises with Y", "runs": ["run/1"]}
    assert core.check("finding", good) is True
