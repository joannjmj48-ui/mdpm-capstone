#!/usr/bin/env python3
"""Python port of scripts/sync-index-data.mjs — deterministically adapts
data/system-map.json into the generated data block inside index.html.

Node is not installed on this machine. This is a faithful port, not a rewrite:
same output shape, same generated marker, same block boundaries, so either
script can be run and the result is identical.
"""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
contract = json.loads((ROOT / "data" / "system-map.json").read_text(encoding="utf-8"))
index_path = ROOT / "index.html"

def title_case(v):
    return re.sub(r'(^|[-\s])([a-z])', lambda m: m.group(1) + m.group(2).upper(), v)

BASIS = {"evidence": "Evidence", "legacy-evidence-synthesis": "Evidence trace pending",
         "analytical-inference": "Analytical inference", "group-convergence": "Group convergence",
         "model-definition": "Model definition"}
DECISION = {"active-direction": "Active direction", "hypothesis": "Hypothesis",
            "intended-outcome": "Intended outcome", "unresolved": "Unresolved"}
basis = lambda v: BASIS.get(v, title_case(v or ""))
decision = lambda v: DECISION.get(v, title_case(v or ""))

overlays = {o["id"]: o for o in contract["overlays"]}

nodes = {}
for n in contract["nodes"]:
    nodes[n["id"]] = {
        "label": n["displayLabel"], "sub": n.get("subtitle") or "",
        "kind": "value" if n.get("kind") == "value-process" else n.get("kind"),
        "phase": n.get("phase") or " • ".join(title_case(t) for t in n["applicableTabs"]),
        "status": n["epistemicStatus"], "basis": basis(n["claimBasis"]),
        "decision": decision(n["decisionStatus"]), "category": n["category"],
        "definition": n["definition"], "role": n["roleInSystem"],
        "why": n.get("whyItMatters"), "known": n.get("known"),
        "provisional": n.get("provisional"), "opportunity": n.get("opportunityImplication"),
        "chain": n.get("chain") or [], "dimensions": n.get("dimensions") or [],
        "systemLinks": n.get("systemLinks") or [],
    }

for st in contract["valueStates"]:
    out = next((t for t in contract["valueTransitions"] if t["fromState"] == st["id"]), None)
    jt = overlays[out["jtbdRefs"][0]] if out else None
    dv = overlays[out["dvoRefs"][0]] if out else None
    to_label = (nodes.get(out["toState"], {}).get("label") or title_case(out["toState"])) if out else None
    nodes[st["id"]] = {
        "label": st["label"],
        "sub": f"{out['id']} begins here" if out else "Canonical value-state outcome",
        "kind": "state", "phase": "Main Variable Transition",
        "status": st["epistemicStatus"], "basis": basis(st["claimBasis"]),
        "decision": decision(st["decisionStatus"]), "category": "Controlled value state",
        "definition": st["definition"],
        "role": f"Entry condition: {st['entryCondition']} Exit condition: {st['exitCondition']}",
        "why": "This state is analytically distinct so qualification, posting, access, use and perceived worth are not collapsed into generic value.",
        "known": "The state definition is an approved group-converged modeling decision. Current volumes, conversion rates and delays are not yet established.",
        "provisional": " ".join(out["openQuestions"]) if out else "The effect of Realized Value on subsequent behaviour remains unvalidated.",
        "opportunity": dv["statement"] if dv else "Evaluate the realized outcome and its relationship to future participation without assuming causality.",
        "chain": [st["label"], out["id"], to_label] if out else [st["label"], "Outcome evaluation"],
        "dimensions": out["possibleIndicators"] if out else [],
        "systemLinks": ([
            {"phase": out["id"], "targets": [f"{title_case(out['fromState'])} → {title_case(out['toState'])}"], "explanation": out["definition"]},
            {"phase": "Member progress / JTBD", "targets": [jt["statement"]], "explanation": "Analytical overlay • not an operating system component."},
            {"phase": "Digital Value Opportunity", "targets": [dv["statement"]], "explanation": "Group-converged opportunity space • not a proven leverage point."},
        ] if out else []),
    }

layouts = {
    "current": {"member-only": "mo", "member-client": "mc", "client-only": "co", "partner": "partner",
                "member-value": "value", "engagement": "engagement", "products": "products", "data": "data",
                "channels": "channels", "service": "service", "friction": "friction"},
    "transition": {"opportunity": "opportunity", "potential-value": "potential", "earned-value": "earned",
                   "available-value": "available", "realized-value": "realized", "partner": "partner",
                   "products": "products", "data": "data", "service": "service", "channels": "channels",
                   "friction": "friction", "engagement": "engagement"},
    "future": {"identity": "identity", "orchestration": "orchestration", "delivery": "delivery", "partner": "partner",
               "member-value": "value", "engagement": "futureengagement", "intersection": "intersection", "net-value": "net"},
    "external": {"regulation": "regulation", "technology-landscape": "technology", "expectations": "expectations",
                 "competitors": "competitors", "neither": "neither"},
}

by_id = {r["id"]: r for r in contract["relationships"]}
rel_meta, edge_meanings, views = {}, {}, {}

for view in contract["views"]:
    edges = []
    for rid in view["relationshipIds"]:
        r = by_id[rid]
        phase = ("future" if view["id"] == "future" and r["epistemicStatus"] == "Assumed"
                 else "inferred" if r["epistemicStatus"] == "Inferred" else "current")
        rel_meta[rid] = {"epistemicStatus": r["epistemicStatus"], "claimBasis": basis(r["claimBasis"]),
                         "decisionStatus": decision(r["decisionStatus"]),
                         "transitionIds": r.get("valueTransitionIds") or [],
                         "evidenceRefs": r.get("evidenceRefs") or []}
        edge_meanings[r["displayLabel"]] = r["relationshipDefinition"]
        edges.append([r["sourceId"], r["targetId"], r["displayLabel"], phase, None, rid])
    views[view["id"]] = {"label": view["heading"], "description": view["contextParagraph"],
                         "areas": layouts[view["id"]], "edges": edges}

def ser(v):
    return "\n".join("  " + ln for ln in json.dumps(v, indent=2, ensure_ascii=False).split("\n"))

MARK = "  /* GENERATED FROM data/system-map.json. Run scripts/sync-index-data.mjs after contract changes. */"
block = (MARK + "\n"
         + f"  var nodes = {ser(nodes).lstrip()};\n\n"
         + f"  var views = {ser(views).lstrip()};\n\n"
         + f"  var edgeMeanings = {ser(edge_meanings).lstrip()};\n\n"
         + f"  var relationshipMeta = {ser(rel_meta).lstrip()};\n\n")

html = index_path.read_text(encoding="utf-8")
start = html.find(MARK)
if start < 0:
    start = html.find("  var nodes = {")
end = html.find("  var currentView = ")
if start < 0 or end < 0 or end <= start:
    sys.exit("Could not locate embedded map-data block")
index_path.write_text(html[:start] + block + html[end:], encoding="utf-8")
print(f"Synchronized {len(nodes)} renderable entities and {len(contract['relationships'])} relationships.")
