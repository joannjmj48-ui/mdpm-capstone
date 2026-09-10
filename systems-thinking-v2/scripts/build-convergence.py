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
            "headline": "The appendix map read as one-way flow into a single outcome.",
            "scope": "This is a critique of the systems map - its actors, components and the relationships between them. It is not a critique of the causal loop work, which is a separate artefact with a separate job.",
            "measured": "In the Current System view, 8 of 17 relationships pointed into Member Value Realization. Its in-degree was 8 while every other component sat between 0 and 3. Only 7 relationships ran between the surrounding components at all.",
            "interpretation": "That shape is hub-and-spoke: the ecosystem feeds one outcome and barely touches itself. It reads as a funnel because structurally it is one - and a map of a system should show the system, not only what it produces.",
            "byView": [
                {"view": "Relationships in the view", "before": 17, "after": 25},
                {"view": "Pointing into Member Value", "before": 8, "after": 9},
                {"view": "Between other components", "before": 7, "after": 14},
                {"view": "Member Value share of map", "before": "47%", "after": "36%"},
            ],
            "remedy": "Eight targeted relationships, no rebuild and no new nodes: partners into products; products already into decisioning; decisioning into delivery channels; the operational backbone supporting both decisioning and channels; each member population touching more than one part of the system; and engagement returning to realization rather than terminating there. Relationships between the surrounding components doubled, and Member Value Realization went from carrying 47% of the map to 36%.",
            "note": "All eight are marked Inferred and group-converged, so they render in the inferred line style and are visibly distinguishable from the original evidence-traced structure.",
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
