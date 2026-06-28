"""Cross-node referential invariants for the Actionable Investigation Graph
(RFC-0002 Phase B). Pure function over a resolved node set."""
from __future__ import annotations


def validate_chain(nodes: dict[str, dict]) -> list[dict]:
    """nodes: {node_id -> node dict}. Returns violation dicts
    {node_id, invariant, message}; [] means the chain is sound."""
    viol: list[dict] = []

    def add(nid, inv, msg):
        viol.append({"node_id": nid, "invariant": inv, "message": msg})

    # evidence_id -> [decision_id] where the decision accepted it
    accepts: dict[str, list[str]] = {}
    for nid, n in nodes.items():
        if n.get("type") == "decision" and n.get("outcome") == "accept":
            for eid in n.get("evidence", []) or []:
                accepts.setdefault(eid, []).append(nid)

    for nid, n in nodes.items():
        t = n.get("type")
        if t == "finding":
            if len(n.get("runs", []) or []) < 1:
                add(nid, "finding->run", "finding references no run")
        elif t == "evidence":
            fids = n.get("findings", []) or []
            if len(fids) < 1:
                add(nid, "evidence->finding", "evidence references no finding")
            for fid in fids:
                ref = nodes.get(fid)
                if ref is None or ref.get("type") != "finding":
                    add(nid, "evidence->finding", f"finding ref does not resolve: {fid}")
            if len([h for h in (n.get("hypotheses", []) or []) if str(h).strip()]) < 1:
                add(nid, "evidence->hypothesis", "evidence references no hypothesis")
        elif t == "conclusion":
            decs = set(n.get("decisions", []) or [])
            for eid in n.get("evidence", []) or []:
                ev = nodes.get(eid)
                if ev is None or ev.get("type") != "evidence":
                    add(nid, "conclusion->evidence", f"evidence ref does not resolve: {eid}")
                    continue
                if ev.get("lifecycle_state") != "accepted":
                    add(nid, "conclusion->accepted", f"evidence not accepted: {eid}")
                if not (set(accepts.get(eid, [])) & decs):
                    add(nid, "conclusion->decision",
                        f"no referenced accept-decision for evidence: {eid}")
    return viol
