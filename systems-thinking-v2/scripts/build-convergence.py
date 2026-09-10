#!/usr/bin/env python3
"""Assemble data/convergence.json from the per-contributor submissions in
data/submissions/ plus the curated cross-contributor analysis in
data/convergence-map.json.

convergence.json is GENERATED. Edit the submissions or the convergence map,
then re-run this script. Do not hand-edit the output.

Node is not installed on this machine, so this follows the repo's existing
build-script convention in Python.
"""
import json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "convergence.json"

CONTRIBUTORS = [
    {"id": "sly", "displayName": "Sylvester", "submissionId": "SUB-SLY", "status": "received",
     "sourceRef": "Published V1 site: /systems-thinking/ (system-loops.js, leverage-product.js)",
     "note": "Extracted from published work rather than collected via the intake template."},
    {"id": "josh", "displayName": "Josh", "submissionId": "SUB-JOSH", "status": "received-partial",
     "sourceRef": "Josh- Leverage Points and Product Description.docx (Team Zig, Milestone 2)",
     "note": "Leverage points and product description supplied. Causal loop structure referenced but not supplied — see GAP-01."},
]

STRENGTH = {
    "unique": "Proposed by one contributor only.",
    "partial": "Proposed by more than one contributor but with materially different meaning, weight, or boundary.",
    "converged": "Proposed independently by multiple contributors with substantively the same meaning.",
    "contested": "Contributors propose incompatible relationships, polarities, or framings.",
}


def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"missing required file: {path}")
    except json.JSONDecodeError as e:
        sys.exit(f"{path.name} is not valid JSON: {e}")


def main():
    subs = []
    for c in CONTRIBUTORS:
        p = DATA / "submissions" / f"{c['id']}.json"
        if not p.exists():
            print(f"  skip  {c['id']} — no submission file yet")
            continue
        s = load(p)
        if s["id"] != c["submissionId"]:
            sys.exit(f"{p.name}: id {s['id']} does not match contributor submissionId {c['submissionId']}")
        subs.append(s)

    cmap = load(DATA / "convergence-map.json")
    registry = load(DATA / "variable-registry.json")

    known = {s["id"] for s in subs}
    for declared in cmap.get("analysedSubmissions", []):
        if declared not in known:
            sys.exit(f"convergence-map.json analyses {declared}, which has no submission file")

    clusters = cmap["leverageConvergence"] + cmap["productConvergence"]
    counts = {}
    for cl in clusters:
        counts[cl["strength"]] = counts.get(cl["strength"], 0) + 1

    contract = {
        "version": "1.1.0-convergence",
        "generated": True,
        "generatedBy": "scripts/build-convergence.py — do not hand-edit; edit data/submissions/*.json or data/convergence-map.json",
        "modelStatus": "partial-team-coverage",
        "governingInquiry": "Where do Team Zig's independently developed causal loops and product definitions converge, where do they diverge, and what does that tell us about the loyalty system we are designing for?",
        "extends": "data/system-map.json",
        "classificationRule": "Group convergence and hypotheses never become evidence-supported solely through approval. Independent agreement between contributors is recorded as convergence strength, not as evidence.",
        "convergenceStrength": STRENGTH,
        "coverage": {
            "contributorsExpected": "unknown — full Team Zig roster not yet confirmed",
            "contributorsReceived": len(subs),
            "caveat": "Convergence across two contributors is a weak basis for claiming team convergence. Ratings should be revisited as further submissions arrive.",
        },
        "contributors": CONTRIBUTORS,
        "submissions": subs,
        "convergence": {
            "analysisVersion": cmap["analysisVersion"],
            "analysisNote": cmap["analysisNote"],
            "summary": counts,
            "leverage": cmap["leverageConvergence"],
            "product": cmap["productConvergence"],
        },
        "registry": {
            "variables": registry["variables"],
            "loops": registry["loops"],
            "rule": registry["rule"],
            "method": registry["method"],
        },
        "structuralDiagnostic": {
            "headline": "The current map is a value chain, not a feedback structure.",
            "measured": "Sly's approved V2 contract holds 21 nodes and 41 relationships but only 2 closed loops. Three of its four views contain none at all.",
            "byView": [
                {"view": "Current System", "relationships": 17, "closedLoops": 2},
                {"view": "Main Variable Transition", "relationships": 12, "closedLoops": 0},
                {"view": "Future Opportunity", "relationships": 9, "closedLoops": 0},
                {"view": "Outside the Boundary", "relationships": 5, "closedLoops": 0},
            ],
            "interpretation": "39 of 41 relationships run one way and never return. A structure where influence flows forward and does not come back is a pipeline: it can show how value moves, but it cannot explain why the system behaves as it does over time.",
            "remedy": "The team's own loop work already supplies what is missing. Nine canonical loops, all closed, all with stated mechanisms. Making those the primary structure and demoting the eight-step chain to a supporting value-chain view converts the pipeline into a systems map without discarding any of the existing analysis.",
        },
        "divergences": cmap["divergences"],
        "gaps": cmap["gaps"],
    }

    OUT.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  contributors : {len(subs)}")
    print(f"  clusters     : {len(clusters)} " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"  divergences  : {len(cmap['divergences'])} "
          f"({sum(1 for d in cmap['divergences'] if d.get('blocksMerge'))} blocking)")
    print(f"  open gaps    : {len(cmap['gaps'])}")


main()
