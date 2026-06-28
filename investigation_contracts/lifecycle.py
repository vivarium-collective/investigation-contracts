"""The thin lifecycle transition-table layer (RFC-0002 §2 caveat).

State machines per node type. ``check_transition`` is the enforcement the
graph's apply-path calls; promoting it to a bigraph-schema custom ``_apply`` is
a Phase-B refinement.
"""
from __future__ import annotations

# node_type -> {from_state: [allowed_to_states]}; "" is the pre-creation state.
LIFECYCLES: dict[str, dict[str, list[str]]] = {
    "finding": {
        "": ["proposed"],
        "proposed": ["reviewed"],
        "reviewed": ["accepted", "rejected"],
        "accepted": [],
        "rejected": [],
    },
    "evidence": {"": ["proposed"], "proposed": ["accepted", "rejected"],
                 "accepted": [], "rejected": []},
    "decision": {"": ["pending"], "pending": ["recorded"], "recorded": []},
    "conclusion": {"": ["draft"], "draft": ["published"], "published": []},
}


def initial_state(node_type: str) -> str:
    table = LIFECYCLES.get(node_type)
    if not table:
        raise KeyError(f"no lifecycle for node type {node_type!r}")
    return table[""][0]


def check_transition(node_type: str, frm: str, to: str) -> bool:
    table = LIFECYCLES.get(node_type)
    if not table:
        return False
    return to in table.get(frm, [])
