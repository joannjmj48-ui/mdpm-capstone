#!/usr/bin/env python3
"""Build the canonical variable registry and loop alignment across all six
Team Zig contributors.

The team's divergent thinking produced six independently-named variable sets.
This registry is the join: one canonical variable per underlying construct,
with every contributor's own wording preserved as an alias. Loops become
comparable only once their variables resolve to the same registry entries.

Aliases are a judgement call and are listed in full so they can be disputed.
"""
import json, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "variable-registry.json"

# canonical id -> (label, definition, [(contributor, their wording), ...])
REG = {
"CV-REALIZED": ("Realized value",
 "Value the member actually obtains and can use. Points sitting unspent are value earned, not value realized.",
 [("joann","Realized value"),("sly","Member value-realization rate (V03)"),("henry","Realized Reward Value"),
  ("lia","Perceived Value"),("ola","Value Realized")]),
"CV-ENGAGE": ("Sustained engagement",
 "Repeat use of the program over time — a pattern of earning, checking, redeeming and returning.",
 [("joann","Sustained engagement"),("sly","Repeat participation (V05)"),("henry","Program Usage"),
  ("lia","Member Engagement"),("ola","Member Engagement")]),
"CV-TXN": ("Transactions & participation",
 "What members actually spend and do through the program — swipes, partner purchases, activations, redemptions.",
 [("joann","Transactions & participation"),("sly","Opportunity capture (V02)"),("henry","Member Action / Participation")]),
"CV-SIGNAL": ("Permissioned signal richness",
 "How much the system is permitted to know about a member, and how useful that knowledge is.",
 [("joann","Permissioned signal richness"),("sly","Outcome information (V06)"),("henry","Member Data & Insight"),
  ("lia","Behavioral Insights"),("ola","Transaction Data")]),
"CV-RELEVANCE": ("Decisioning relevance",
 "How well the system picks the right opportunity for the right member at the right moment.",
 [("joann","Decisioning relevance"),("sly","Decisioning quality (V07)"),("henry","Personalization Quality"),
  ("lia","Personalization"),("josh","Personalization toward a segment of one")]),
"CV-OFFERS": ("Relevant, visible opportunities",
 "Worthwhile opportunities an eligible member can discover and understand.",
 [("sly","Relevant, visible opportunities (V01)"),("henry","Relevant Earning & Redemption Opportunities"),
  ("lia","Offer Relevance"),("ola","Relevant Offers")]),
"CV-TRUST": ("Program trust",
 "Confidence that the program will reliably convert its promises into usable value.",
 [("sly","Program trust (V04)"),("henry","Trust & Engagement with Loyalty Program"),("lia","Trust"),("ola","Member Trust")]),
"CV-REDEEM": ("Redemption rate","The share of issued points members actually spend.",
 [("joann","Redemption rate")]),
"CV-BREAKAGE": ("Breakage revenue",
 "Money the program keeps because points were never redeemed.",
 [("joann","Breakage revenue"),("ola","Breakage & Margin"),("josh","Breakage (in B2 Personalized Value & Breakage)")]),
"CV-HEADROOM": ("Offer margin headroom","How much the program can afford to give away and still hit margin.",
 [("joann","Offer margin headroom"),("ola","Scale Investment")]),
"CV-GENEROSITY": ("Offer generosity & point value","How much a point is worth and how good the deals are.",
 [("joann","Offer generosity & point value")]),
"CV-UNRESOLVED": ("Unresolved or uncertain value",
 "Worthwhile value that was promised but has not visibly arrived, or whose state the member cannot determine.",
 [("henry","Unresolved / Uncertain Reward Value"),("sly","Value friction (V10)"),("joann","Missing / expiring states in the ledger")]),
"CV-FRICTION": ("Member uncertainty & friction",
 "Delay, effort and doubt the member absorbs while trying to progress value.",
 [("henry","Member Uncertainty & Friction"),("sly","Value friction (V10)")]),
"CV-DETECT": ("Detection & resolution effort",
 "Work done to identify an interruption, explain it, and resolve or route it.",
 [("henry","Detection, Explanation & Resolution Effort"),("sly","Exception detection and recovery (L03)"),
  ("joann","Missing-value detection and one-tap resolution")]),
"CV-STATUS": ("Reward status visibility & clarity",
 "Whether earned, pending, posted, redeemed, missing and expiring states are accurate and legible to the member.",
 [("henry","Reward Status Accuracy, Visibility & Clarity"),("joann","The ledger — dollars, not points"),
  ("ola","Real-Time Status"),("sly","Shared value-state information (L01)")]),
"CV-DEMAND": ("Reward-processing demand",
 "Volume and complexity of earning, posting, redemption, fulfilment and support activity.",
 [("sly","Reward-processing demand (V08)")]),
"CV-OPSLOAD": ("Operational load","Workload on the capabilities and teams delivering program value.",
 [("sly","Operational load (V09)")]),
"CV-INTENSITY": ("Personalization intensity","How hard the system leans on member data to target offers.",
 [("joann","Personalization intensity"),("lia","Data Use")]),
"CV-INTRUSION": ("Perceived intrusion","How closely watched the personalization makes a member feel.",
 [("joann","Perceived intrusion"),("lia","Privacy / Control Concerns")]),
"CV-CONSENT": ("Consent granted","Whether members agree to this use of their data — and keep agreeing.",
 [("joann","Consent granted"),("lia","Willingness to Share Data"),("josh","Progressive consent / account linking")]),
"CV-OVERLAP": ("Member–client overlap","People who are both Blue Rewards members and BMO banking customers.",
 [("joann","Member–client overlap")]),
"CV-COMBINED": ("Combined signals","What can be seen when a person is viewed as member and client together.",
 [("joann","Combined signals"),("josh","Authorized cross-bank data / CDB signals")]),
"CV-PARTNERSPEND": ("Partner-attributable spend","Spend at a partner brand the partner can see came from Blue Rewards.",
 [("joann","Partner-attributable spend")]),
"CV-ANCHOR": ("Anchor partner retention","Whether big-category weekly partners stay.",
 [("joann","Anchor partner retention")]),
"CV-BREADTH": ("Earn & redeem breadth","How many everyday places a member can earn and spend.",
 [("joann","Earn & redeem breadth")]),
"CV-EVERYDAY": ("Everyday relevance","Whether the program shows up in ordinary weekly life.",
 [("joann","Everyday relevance")]),
"CV-GOAL": ("Member goal achievement","Progress against a goal the member has stated.",
 [("josh","Member goal achievement"),("joann","Goal-linked progress")]),
"CV-PREVIEW": ("Demonstrated value of connecting",
 "Concrete, visible proof that linking an account or granting data returns something the member can use.",
 [("josh","Value preview / visible proof")]),
"CV-FRAGMENT": ("Channel & data fragmentation",
 "Value, status and opportunity split across channels and systems that do not resolve to one view.",
 [("josh","Fragmented data and channels"),("joann","Searching across channels")]),
"CV-REVENUE": ("Engagement & revenue","Program revenue produced by sustained engagement.",
 [("ola","Engagement & Revenue"),("joann","Member-to-client conversion (R2)")]),
}

# canonical loop id -> definition
LOOPS = {
"TR1": {"type":"reinforcing","name":"Relevance flywheel",
  "canonicalChain":["CV-REALIZED","CV-ENGAGE","CV-TXN","CV-SIGNAL","CV-RELEVANCE","CV-OFFERS","CV-REALIZED"],
  "summary":"Value members actually get keeps them engaged; engagement produces permissioned signal; signal improves relevance; relevance produces more realized value.",
  "contributors":{
    "joann":{"originalCode":"R1","name":"Relevance flywheel","chain":["CV-REALIZED","CV-ENGAGE","CV-TXN","CV-SIGNAL","CV-RELEVANCE","CV-REALIZED"],"note":"Collapses opportunity surfacing into the relevance→value link."},
    "sly":{"originalCode":"R1","name":"Value Realization and Learning Flywheel","chain":["CV-REALIZED","CV-TRUST","CV-ENGAGE","CV-SIGNAL","CV-RELEVANCE","CV-OFFERS","CV-TXN","CV-REALIZED"],"note":"Adds trust as an explicit step."},
    "henry":{"originalCode":"R1","name":"Value Realization Flywheel","chain":["CV-REALIZED","CV-TRUST","CV-ENGAGE","CV-SIGNAL","CV-RELEVANCE","CV-OFFERS","CV-TXN","CV-REALIZED"],"note":"Identical to Sly's, node for node, in different words."},
    "lia":{"originalCode":"R","name":"Reinforcing Loop (more engagement)","chain":["CV-REALIZED","CV-ENGAGE","CV-SIGNAL","CV-OFFERS","CV-REALIZED"],"note":"Four-node compression; no trust or capture step."},
    "ola":{"originalCode":"R1","name":"Personalization Flywheel","chain":["CV-ENGAGE","CV-SIGNAL","CV-OFFERS","CV-ENGAGE"],"note":"Three-node compression; realized value implicit."}},
  "convergence":"converged",
  "finding":"Five of six contributors independently drew this loop. It is the same causal structure at four different resolutions, not five different theories."},

"TB1": {"type":"balancing","name":"Program economics — the breakage brake",
  "canonicalChain":["CV-REALIZED","CV-REDEEM","CV-BREAKAGE","CV-HEADROOM","CV-GENEROSITY","CV-REALIZED"],
  "negativeLinks":[["CV-REDEEM","CV-BREAKAGE"]],
  "summary":"Redemption is what members want, but the programme is funded on points nobody uses. Redemption up, breakage down, headroom down, generosity down, value reaching members down.",
  "contributors":{
    "joann":{"originalCode":"B1","name":"Program economics","chain":["CV-REALIZED","CV-REDEEM","CV-BREAKAGE","CV-HEADROOM","CV-GENEROSITY","CV-REALIZED"],"note":"Full five-step form with the inverse link named."},
    "ola":{"originalCode":"B1","name":"Realization vs. Program Margin","chain":["CV-REALIZED","CV-BREAKAGE","CV-HEADROOM","CV-REALIZED"],"note":"Same brake, three-node form."},
    "josh":{"originalCode":"B2","name":"Personalized Value & Breakage","chain":[],"note":"UNRESOLVED. The name pairs two mechanisms this map treats separately, and Josh attaches the same loop to goal alignment in JL01 - a third reading. Not derivable."}},
  "convergence":"partial",
  "finding":"Two contributors drew the same brake and a third may have. It is the only brake where the inverse link is arithmetic rather than behavioural — a point that gets used cannot also go unused."},

"TB2": {"type":"balancing","name":"Trust & consent — the permission brake",
  "canonicalChain":["CV-INTENSITY","CV-INTRUSION","CV-CONSENT","CV-SIGNAL","CV-RELEVANCE","CV-INTENSITY"],
  "negativeLinks":[["CV-INTRUSION","CV-CONSENT"]],
  "summary":"Personalization runs on permission it can spend. Push intensity too hard and members feel watched, consent narrows, signal thins, relevance falls.",
  "contributors":{
    "joann":{"originalCode":"B2","name":"Trust & consent","chain":["CV-INTENSITY","CV-INTRUSION","CV-CONSENT","CV-SIGNAL","CV-RELEVANCE","CV-INTENSITY"],"note":"Framed as the cap on how hard R1 can be pushed."},
    "lia":{"originalCode":"B","name":"Balancing Loop (keeps things in check)","chain":["CV-INTENSITY","CV-INTRUSION","CV-TRUST","CV-CONSENT","CV-RELEVANCE","CV-INTENSITY"],"note":"Routes through trust explicitly before consent."},
    "josh":{"originalCode":"—","name":"Progressive consent (JL02)","chain":[],"note":"Not drawn as a loop; appears as a leverage point on the same mechanism."}},
  "convergence":"converged",
  "finding":"Two contributors drew this independently and a third proposed intervening on it. It is the only brake that acts on the flywheel's fuel rather than its output."},

"TB3": {"type":"balancing","name":"Value gap — the delivery brake",
  "canonicalChain":["CV-UNRESOLVED","CV-FRICTION","CV-DETECT","CV-STATUS","CV-REALIZED","CV-UNRESOLVED"],
  "negativeLinks":[["CV-REALIZED","CV-UNRESOLVED"]],
  "summary":"Value that was promised but did not visibly arrive creates uncertainty and friction, which triggers detection and resolution effort, which restores clarity and realized value — reducing the unresolved value that started it.",
  "contributors":{
    "henry":{"originalCode":"B1","name":"Reward Value Gap Correction","chain":["CV-UNRESOLVED","CV-FRICTION","CV-DETECT","CV-STATUS","CV-REALIZED","CV-UNRESOLVED"],"note":"The only contributor to draw the correction as a closed loop."},
    "sly":{"originalCode":"B1","name":"Operational Friction and Capacity Constraint","chain":["CV-ENGAGE","CV-DEMAND","CV-OPSLOAD","CV-UNRESOLVED","CV-REALIZED","CV-TRUST","CV-ENGAGE"],"note":"Same failure, different cause: capacity not keeping up with volume."},
    "joann":{"originalCode":"—","name":"The six-state ledger","chain":[],"note":"Modelled as a state machine with one capability per failure mode rather than as a loop."}},
  "convergence":"partial",
  "finding":"Henry and Sly describe the same breakdown from opposite ends — Henry from the member's uncertainty, Sly from the operation's capacity. Both end at unresolved value reducing realization and trust."},

"TR2": {"type":"reinforcing","name":"Conversion flywheel",
  "canonicalChain":["CV-ENGAGE","CV-OVERLAP","CV-COMBINED","CV-RELEVANCE","CV-REALIZED","CV-ENGAGE"],
  "summary":"Engagement produces member-client overlap; overlap produces combined signal; combined signal improves relevance; relevance produces realized value.",
  "contributors":{
    "joann":{"originalCode":"R2","name":"Conversion flywheel","chain":["CV-ENGAGE","CV-OVERLAP","CV-COMBINED","CV-RELEVANCE","CV-REALIZED","CV-ENGAGE"],"note":"Proposed as the replacement revenue source if breakage comes off the scorecard."}},
  "convergence":"unique",
  "finding":"Only Joann modelled member-to-client conversion as a closed loop. It matters disproportionately because it is the only revenue source in the team's set that grows when redemption grows."},

"TR3": {"type":"reinforcing","name":"Partner coverage",
  "canonicalChain":["CV-ENGAGE","CV-PARTNERSPEND","CV-ANCHOR","CV-BREADTH","CV-EVERYDAY","CV-ENGAGE"],
  "summary":"The flywheel on the supply side. Engagement produces attributable partner spend, which retains anchor partners, which widens earn-and-redeem breadth, which makes the programme part of ordinary weekly life.",
  "contributors":{
    "joann":{"originalCode":"R3","name":"Partner coverage","chain":["CV-ENGAGE","CV-PARTNERSPEND","CV-ANCHOR","CV-BREADTH","CV-EVERYDAY","CV-ENGAGE"],"note":"Currently running backwards - Sobeys 2022, Shell 2026."}},
  "convergence":"unique",
  "finding":"The only loop anyone claims is currently spinning in the wrong direction, which makes it the least redundant and least examined part of the team's set."},

"TR4": {"type":"reinforcing","name":"Reliability and trust",
  "canonicalChain":["CV-REVENUE","CV-STATUS","CV-TRUST","CV-ENGAGE","CV-REVENUE"],
  "summary":"Investment in reliable, visible status produces trust; trust produces engagement; engagement funds further investment. This loop routes through status visibility rather than through relevance.",
  "contributors":{
    "ola":{"originalCode":"R2","name":"Trust Through Reliable Value","chain":["CV-REVENUE","CV-STATUS","CV-TRUST","CV-REVENUE"],"note":"Three-node form."}},
  "convergence":"unique",
  "finding":"Ola is the only contributor to close reliability into a loop - and it is the loop Joann's six-state ledger acts on directly. The team's most-specified product feature drives the team's least-discussed loop."},

"TR5": {"type":"reinforcing","name":"Connected-data adoption",
  "canonicalChain":["CV-PREVIEW","CV-CONSENT","CV-COMBINED","CV-RELEVANCE","CV-REALIZED","CV-PREVIEW"],
  "summary":"Showing a member what connecting an account would return gives them a reason to connect; connection enriches combined signal; richer signal improves relevance; relevance produces realized value, which is itself the next proof.",
  "contributors":{
    "josh":{"originalCode":"R5","name":"Consumer-Driven Banking Awareness & Adoption","chain":["CV-PREVIEW","CV-CONSENT","CV-COMBINED","CV-RELEVANCE","CV-REALIZED","CV-PREVIEW"],"note":"DERIVED from Josh's JL02 prose; not supplied by him."}},
  "convergence":"derived",
  "derivation":{"confidence":"high","status":"needs-confirmation",
    "basis":"Josh states the chain almost completely in JL02: a value preview gives members a reason to participate, and progressive consent helps the loop gain enough participation to produce useful experiences and visible proof. Reason-to-participate to consent to signal to experiences to proof is a closed reinforcing path.",
    "assumption":"That visible proof feeds back to the value preview rather than terminating. His phrase implies the return arrow; he does not draw it."},
  "finding":"The one Josh loop his prose genuinely supports. Zero negative links, consistent with his reinforcing label."},

"TR6": {"type":"reinforcing","name":"Fragmentation and disengagement",
  "canonicalChain":["CV-FRAGMENT","CV-FRICTION","CV-ENGAGE","CV-SIGNAL","CV-RELEVANCE","CV-FRAGMENT"],
  "negativeLinks":[["CV-FRICTION","CV-ENGAGE"],["CV-RELEVANCE","CV-FRAGMENT"]],
  "summary":"Fragmented channels and data raise the effort of finding and tracking value; effort suppresses engagement; less engagement thins signal; thinner signal degrades relevance; degraded relevance leaves the experience more fragmented still.",
  "contributors":{
    "josh":{"originalCode":"R4","name":"Digital Friction & Engagement","chain":["CV-FRAGMENT","CV-FRICTION","CV-ENGAGE","CV-SIGNAL","CV-RELEVANCE","CV-FRAGMENT"],"note":"DERIVED from the loop name plus JL03. Josh supplied neither variables nor polarities."}},
  "convergence":"derived",
  "derivation":{"confidence":"low","status":"needs-confirmation",
    "basis":"The name pairs friction with engagement, and JL03 treats fragmentation as the thing to restructure. Two negative links - friction suppressing engagement, relevance reducing fragmentation - give an even count, consistent with a reinforcing label.",
    "assumption":"That Josh intends a vicious cycle rather than a virtuous one. A reinforcing loop runs both ways, so this may be the same structure read from the opposite direction. The polarity pattern is entirely inferred."},
  "finding":"Plausible and internally consistent, but the parity is the only evidence for it. Confirm before using."},
}


contributors = ["joann","sly","henry","josh","lia","ola"]
registry = {
  "version":"1.0.0",
  "purpose":"Canonical variable registry and loop alignment across all six Team Zig contributors. The team's divergent thinking produced six independently-named variable sets; this is the join that makes them comparable.",
  "method":"Each canonical variable carries every contributor's own wording as an alias. Aliasing is judgement and is listed in full so it can be disputed. Loops are aligned only after their variables resolve to registry entries.",
  "rule":"Alignment records that contributors described the same construct. It does not merge their evidence, and it does not upgrade any claim's epistemic status.",
  "contributors":contributors,
  "variables":[
    {"id":k,"label":v[0],"definition":v[1],
     "aliases":[{"contributor":c,"wording":w} for c,w in v[2]],
     "contributorCount":len({c for c,_ in v[2]})}
    for k,v in REG.items()],
  "loops":[dict(id=k, **v) for k,v in LOOPS.items()],
}

OUT.write_text(json.dumps(registry, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
shared = [v for v in registry["variables"] if v["contributorCount"]>=3]
print(f"wrote {OUT.name}")
print(f"  canonical variables : {len(registry['variables'])}")
print(f"  shared by 3+        : {len(shared)}")
for v in sorted(shared,key=lambda x:-x['contributorCount']):
    print(f"      {v['contributorCount']}x  {v['label']}")
print(f"  canonical loops     : {len(registry['loops'])}")
for l in registry["loops"]:
    print(f"      {l['id']} {l['convergence']:10} {l['name']:42} ({len(l['contributors'])} contributors)")
