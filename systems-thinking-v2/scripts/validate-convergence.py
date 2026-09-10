#!/usr/bin/env python3
"""Structural validator for data/convergence.json.

Checks each submission is internally coherent before convergence analysis runs.
Merging incoherent submissions produces findings that cannot be traced back to
a real causal claim.

Node is not installed on this machine, so this mirrors the repo's existing Node
validator convention in Python. Exit code 1 on any error.
"""
import json, pathlib, sys

DATA = pathlib.Path(__file__).resolve().parent.parent / "data" / "convergence.json"
POLARITY = {"+", "-"}
errors, warnings = [], []


def err(m): errors.append(m)
def warn(m): warnings.append(m)


def check_submission(sub):
    sid = sub["id"]
    variables = sub.get("variables", [])
    links = sub.get("links", [])
    var_ids = {v["id"] for v in variables}
    if len(var_ids) != len(variables):
        err(f"{sid}: duplicate variable ids")

    seen = {}
    for ln in links:
        lid = ln["id"]
        if lid in seen:
            err(f"{sid}: duplicate link id {lid}")
        seen[lid] = ln
        for end in ("from", "to"):
            if ln[end] not in var_ids:
                err(f"{sid}/{lid}: '{end}' references unknown variable {ln[end]}")
        if ln["polarity"] not in POLARITY:
            err(f"{sid}/{lid}: polarity must be '+' or '-', got {ln['polarity']!r}")
        if not str(ln.get("mechanism", "")).strip():
            err(f"{sid}/{lid}: no mechanism stated — an unexplained link is correlation, "
                f"not causation, and must not be merged")

    if not variables and not links:
        warn(f"{sid}: no causal structure supplied — leverage and product content "
             f"can still be merged, but loop convergence cannot")
    for var in variables:
        vid = var["id"]
        if not any(ln["from"] == vid or ln["to"] == vid for ln in links):
            warn(f"{sid}: variable {vid} ({var['label']}) has no links — orphan")

    for loop in sub.get("loops", []):
        lid, seq = loop["id"], loop.get("sequence", [])
        if loop.get("structureStatus") == "referenced-not-supplied":
            if seq:
                err(f"{sid}/{lid}: marked referenced-not-supplied but carries a sequence")
            warn(f"{sid}/{lid}: '{loop.get('name')}' named but no structure supplied — "
                 f"cannot participate in loop-level convergence")
            continue
        if len(seq) < 3:
            err(f"{sid}/{lid}: loop needs at least 3 steps, got {len(seq)}")
            continue
        if seq[0] != seq[-1]:
            err(f"{sid}/{lid}: does not close — starts at {seq[0]}, ends at {seq[-1]}")
        for step in seq:
            if step not in var_ids:
                err(f"{sid}/{lid}: unknown variable {step} in sequence")

        missing, neg = False, 0
        for a, b in zip(seq, seq[1:]):
            match = [l for l in links if l["from"] == a and l["to"] == b]
            if not match:
                err(f"{sid}/{lid}: no declared link for {a} -> {b}")
                missing = True
            elif match[0]["polarity"] == "-":
                neg += 1
        if not missing:
            derived = "balancing" if neg % 2 else "reinforcing"
            if loop.get("type") != derived:
                err(f"{sid}/{lid}: declared '{loop.get('type')}' but {neg} negative link(s) "
                    f"means it behaves as '{derived}'")

        for ref in loop.get("linkIds", []):
            if ref not in seen:
                err(f"{sid}/{lid}: linkIds references unknown link {ref}")

    for lp in sub.get("leveragePoints", []):
        for vid in lp.get("variableIds", []):
            if vid not in var_ids:
                err(f"{sid}/{lp['id']}: references unknown variable {vid}")

    pd = sub.get("productDefinition") or {}
    if pd:
        lp_ids = {lp["id"] for lp in sub.get("leveragePoints", [])}
        wedge = (pd.get("wedge") or {}).get("leveragePointId")
        if wedge and wedge not in lp_ids:
            err(f"{sid}: product wedge cites unknown leverage point {wedge}")
        if not any(c.get("isWedge") for c in pd.get("capabilities", [])):
            warn(f"{sid}: no capability marked isWedge — the product's starting point is unclear")


def check_convergence_refs(c):
    """Every itemId a convergence cluster cites must exist in that submission.
    A cluster that merges an item nobody wrote is untraceable by definition."""
    index = {}
    for sub in c.get("submissions", []):
        ids = set()
        for lp in sub.get("leveragePoints", []):
            ids.add(lp["id"])
        for loop in sub.get("loops", []):
            ids.add(loop["id"])
        pd = sub.get("productDefinition") or {}
        for cap in pd.get("capabilities", []):
            ids.add(cap["id"])
        ids.update(k for k in pd if not isinstance(pd[k], (list, dict)))
        index[sub["id"]] = ids

    conv = c.get("convergence", {})
    for cluster in conv.get("leverage", []) + conv.get("product", []):
        if cluster["strength"] not in c.get("convergenceStrength", {}):
            err(f"{cluster['id']}: unknown strength {cluster['strength']!r}")
        subs_seen = set()
        for m in cluster.get("members", []):
            s_id, i_id = m["submissionId"], m["itemId"]
            if s_id not in index:
                err(f"{cluster['id']}: cites unknown submission {s_id}")
            elif i_id not in index[s_id]:
                err(f"{cluster['id']}: cites {i_id}, which does not exist in {s_id}")
            subs_seen.add(s_id)
        if cluster["strength"] == "converged" and len(subs_seen) < 2:
            err(f"{cluster['id']}: rated 'converged' but draws on only "
                f"{len(subs_seen)} contributor(s) — convergence requires independent agreement")
        if cluster["strength"] == "unique" and len(subs_seen) > 1:
            err(f"{cluster['id']}: rated 'unique' but cites {len(subs_seen)} contributors")

    gap_ids = {g["id"] for g in c.get("gaps", [])}
    div_ids = {d["id"] for d in c.get("divergences", [])}
    for cluster in conv.get("leverage", []) + conv.get("product", []):
        for ref in cluster.get("residualDivergenceIds", []):
            if ref not in div_ids:
                err(f"{cluster['id']}: references unknown divergence {ref}")
        for ref in cluster.get("blockedBy", []):
            if ref not in gap_ids:
                err(f"{cluster['id']}: references unknown gap {ref}")
    for d in c.get("divergences", []):
        for ref in d.get("blockedBy", []):
            if ref not in gap_ids:
                err(f"{d['id']}: references unknown gap {ref}")


def main():
    if not DATA.exists():
        print(f"missing {DATA}", file=sys.stderr)
        return 1
    c = json.loads(DATA.read_text(encoding="utf-8"))

    declared = {x["id"] for x in c.get("contributors", [])}
    for sub in c.get("submissions", []):
        if sub.get("contributorId") not in declared:
            err(f"{sub['id']}: contributorId {sub.get('contributorId')!r} not in contributors")
        check_submission(sub)

    for cont in c.get("contributors", []):
        if cont.get("status") == "received" and not any(
                s["id"] == cont.get("submissionId") for s in c.get("submissions", [])):
            err(f"contributor {cont['id']}: marked received but submission "
                f"{cont.get('submissionId')} is absent")

    check_convergence_refs(c)

    print(f"convergence.json — {len(c.get('submissions', []))} submission(s), "
          f"{len(c.get('contributors', []))} contributor(s)")
    for w in warnings:
        print(f"  warn  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print(f"\n{len(errors)} error(s).")
        return 1
    print(f"\nOK{' with ' + str(len(warnings)) + ' warning(s)' if warnings else ''}.")
    return 0


sys.exit(main())
