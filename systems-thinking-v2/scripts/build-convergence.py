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
    {"id": "joann", "displayName": "Joann", "submissionId": None, "status": "received",
     "sourceRef": "Five-loop systems map (HTML), B1 leverage analysis, initial product description, 5 Sept talking script",
     "note": "Five loops - the largest single set. Loop structures held in variable-registry.json."},
    {"id": "sly", "displayName": "Sylvester", "submissionId": "SUB-SLY", "status": "received",
     "sourceRef": "Published V1 site: /systems-thinking/ (system-loops.js, leverage-product.js)",
     "note": "Extracted from published work rather than collected via the intake template."},
    {"id": "henry", "displayName": "Henry", "submissionId": None, "status": "received",
     "sourceRef": "Reinforcing Loop, Balancing Loop and System Map diagrams; product definition document",
     "note": "His R1 is node-for-node identical to Sly's in different wording."},
    {"id": "josh", "displayName": "Josh", "submissionId": "SUB-JOSH", "status": "received",
     "sourceRef": "Milestone 2 leverage points and product description; 5 Sept working-session transcript",
     "note": "Loop structures reconstructed from his document and the transcript, then approved by him on 10 Sept."},
    {"id": "lia", "displayName": "Lia", "submissionId": None, "status": "received",
     "sourceRef": "Two Connected Loops for Blue Rewards diagram; 5 Sept working session",
     "note": "Two loops - engagement/relevance, and personalization versus member control."},
    {"id": "ola", "displayName": "Ola", "submissionId": None, "status": "received",
     "sourceRef": "BMO Blue Rewards - Digital Business Model System Loops (PDF); 5 Sept working session",
     "note": "Three loops derived from the Digital Business Model Canvas."},
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
        if not c["submissionId"]:
            continue
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
    lps = load(DATA / "leverage-points.json")

    people = {c["id"] for c in CONTRIBUTORS}
    for declared in cmap.get("analysedSubmissions", []):
        if declared not in people:
            sys.exit(f"convergence-map.json analyses {declared!r}, who is not a declared contributor")

    clusters = cmap["leverageConvergence"] + cmap["productConvergence"]
    counts = {}
    for cl in clusters:
        counts[cl["strength"]] = counts.get(cl["strength"], 0) + 1

    contract = {
        "version": "1.1.0-convergence",
        "generated": True,
        "generatedBy": "scripts/build-convergence.py — do not hand-edit; edit data/submissions/*.json or data/convergence-map.json",
        "modelStatus": "full-team-coverage",
        "governingInquiry": "Where do Team Zig's independently developed causal loops and product definitions converge, where do they diverge, and what does that tell us about the loyalty system we are designing for?",
        "extends": "data/system-map.json",
        "classificationRule": "Group convergence and hypotheses never become evidence-supported solely through approval. Independent agreement between contributors is recorded as convergence strength, not as evidence.",
        "convergenceStrength": STRENGTH,
        "coverage": {
            "contributorsExpected": 6,
            "contributorsReceived": len(CONTRIBUTORS),
            "caveat": "All six contributors are represented. Convergence strength still records independent agreement, never evidence.",
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
        "leveragePointsByAuthor": lps,
        "registry": {
            "variables": registry["variables"],
            "loops": registry["loops"],
            "rule": registry["rule"],
            "method": registry["method"],
        },
        "structuralDiagnostic": {
            "headline": "The appendix map read as one-way flow into a single outcome.",
            "scope": "This is a critique of the systems map - its actors, components and the relationships between them. It is not a critique of the causal loop work, which is a separate artefact with a separate job.",
            "measured": "In the Current System view, 8 of 17 relationships pointed into the main variable. Its in-degree was 8 while every other component sat between 0 and 3. Only 7 relationships ran between the surrounding components at all.",
            "interpretation": "That shape is hub-and-spoke: the ecosystem feeds one outcome and barely touches itself. It reads as a funnel because structurally it is one - and a map of a system should show the system, not only what it produces.",
            "byView": [
                {"view": "Relationships in the view", "before": 17, "after": 25},
                {"view": "Pointing into Member Value", "before": 8, "after": 9},
                {"view": "Between other components", "before": 7, "after": 14},
                {"view": "Member Value share of map", "before": "47%", "after": "36%"},
            ],
            "remedy": "Eight targeted relationships, no rebuild and no new nodes: partners into products; products already into decisioning; decisioning into delivery channels; the operational backbone supporting both decisioning and channels; each member population touching more than one part of the system; and engagement returning to realization rather than terminating there. Relationships between the surrounding components doubled, and The main variable went from carrying 47% of the map to 36%.",
            "note": "All eight are marked Inferred and group-converged, so they render in the inferred line style and are visibly distinguishable from the original evidence-traced structure.",
        },
        "divergences": cmap["divergences"],
        "gaps": cmap["gaps"],
    }

    OUT.write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  contributors : {len(CONTRIBUTORS)} ({len(subs)} with submission files)")
    print(f"  clusters     : {len(clusters)} " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    print(f"  divergences  : {len(cmap['divergences'])} "
          f"({sum(1 for d in cmap['divergences'] if d.get('blocksMerge'))} blocking)")
    open_gaps = [g for g in cmap["gaps"] if g.get("status") != "closed"]
    print(f"  gaps         : {len(open_gaps)} open, {len(cmap['gaps'])-len(open_gaps)} closed")


main()
