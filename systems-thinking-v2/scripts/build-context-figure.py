#!/usr/bin/env python3
"""Build the PRD figure: where the product sits in the Blue Rewards system.

Writes a standalone SVG to figures/product-in-the-system.svg for insertion
into the PRD, and returns the same markup for the site panel.
Joann's MMIE 884 palette and type.
"""
import pathlib, html

W, H = 1700, 1262
INK, CANV, NAVY, GOLD = "#2b2b33", "#fbfaf6", "#10123f", "#C79A3B"
MUTE, MEMB, BMO, PART, CTX = "#8a8a92", "#185FA5", "#534AB7", "#0F6E56", "#854F0B"
SANS, SERIF = "Helvetica,Arial,sans-serif", "Georgia,serif"

o = []
def a(s): o.append(s)
def e(s): return html.escape(str(s), quote=False)

def band(x, y, w, h, label, note, colour, dashed=True, fill=None):
    notes = note if isinstance(note, (list, tuple)) else ([note] if note else [])
    d = ' stroke-dasharray="7 5"' if dashed else ""
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill or "none"}" stroke="{colour}" stroke-width="1.8"{d}/>')
    a(f'<text x="{x+18}" y="{y+26}" font-family="{SERIF}" font-size="13" fill="{colour}" font-weight="700" letter-spacing="2.2">{e(label.upper())}</text>')
    for i, ln in enumerate(notes):
        a(f'<text x="{x+18}" y="{y+46+i*15}" font-family="{SANS}" font-size="11.5" fill="{MUTE}">{e(ln)}</text>')

def chip(x, y, w, h, lines, colour, fill="#ffffff", weight="700", size=13, rx=10, sub=None, subs=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{colour}" stroke-width="1.6"/>')
    cy = (y + 26) if subs else (y + h / 2 - (len(lines) - 1) * 8 + (0 if not sub else -6))
    for i, ln in enumerate(lines):
        a(f'<text x="{x+w/2}" y="{cy+i*16+5}" text-anchor="middle" font-family="{SANS}" font-size="{size}" fill="{colour}" font-weight="{weight}">{e(ln)}</text>')
    if sub:
        a(f'<text x="{x+w/2}" y="{y+h-10}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">{e(sub)}</text>')
    if subs:
        base = y + h - 10 - (len(subs) - 1) * 14
        for i, ln in enumerate(subs):
            a(f'<text x="{x+w/2}" y="{base+i*14}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">{e(ln)}</text>')

def arrow(x1, y1, x2, y2, colour, label=None, dashed=False, lx=None, ly=None, bend=None):
    d = ' stroke-dasharray="6 5"' if dashed else ""
    path = f'M{x1},{y1} Q{bend[0]},{bend[1]} {x2},{y2}' if bend else f'M{x1},{y1} L{x2},{y2}'
    a(f'<path d="{path}" fill="none" stroke="{colour}" stroke-width="2.2"{d} marker-end="url(#ar_{colour[1:]})" opacity="0.9"/>')
    if label:
        mx = lx if lx is not None else (x1 + x2) / 2
        my = ly if ly is not None else (y1 + y2) / 2 - 14
        w = len(label) * 6.0 + 20
        a(f'<rect x="{mx-w/2}" y="{my-11}" width="{w}" height="22" rx="11" fill="{CANV}" stroke="{colour}" stroke-width="1"/>')
        a(f'<text x="{mx}" y="{my+4}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{colour}" font-weight="700">{e(label)}</text>')

# ── canvas and masthead ──
a(f'<rect width="{W}" height="{H}" fill="{CANV}"/>')
a(f'<rect width="{W}" height="86" fill="{NAVY}"/><rect y="86" width="{W}" height="4" fill="{GOLD}"/>')
a(f'<text x="36" y="38" font-family="{SERIF}" font-size="13" fill="{GOLD}" letter-spacing="2.8" font-weight="700">TEAM ZIG  ·  BLUE REWARDS  ·  SYSTEMS MAP FIGURE FOR THE PRD</text>')
a(f'<text x="36" y="70" font-family="{SERIF}" font-size="25" fill="#ffffff" font-weight="700">Where our proposed enhancement would sit</text>')
a(f'<text x="{W-36}" y="48" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">Team Zig · November 2026</text>')
a(f'<text x="{W-36}" y="68" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">An enhanced experience within Blue Rewards</text>')

a(f'<rect x="36" y="104" width="{W-72}" height="36" rx="8" fill="#EEEDFE" stroke="{BMO}" stroke-width="1.2"/>')
a(f'<text x="54" y="127" font-family="{SANS}" font-size="13" fill="{NAVY}">'
  f'<tspan font-weight="700">What this figure shows &#8212; </tspan>'
  f'the Blue Rewards system as it works today, and the one place inside it where Team Zig&#8217;s proposed enhancement would live. '
  f'Read it from the outside in. Only the navy box is new; everything around it already exists.</text>')
SPLIT = len(o)

# ── outside the boundary ──
band(36, 112, W - 72, 96, "Outside the boundary", ["Neither BMO nor this work can change these.", "They set the conditions everything else runs in."], CTX)
for i, t in enumerate(["Regulation and privacy", "Competitor programmes", "Member expectations", "Technology landscape"]):
    chip(330 + i * 330, 152, 300, 42, [t], CTX, fill=CANV, weight="400", size=12.5)

# ── the member, left ──
band(36, 232, 300, 500, "The member", ["The programme sees some of what a member does,", "not all of it."], MEMB)
chip(54, 300, 264, 62, ["Member"], MEMB, fill="#E6F1FB", size=15, sub="with or without a BMO banking relationship")
chip(54, 382, 264, 108, ["Spending they already", "intend to make"], MEMB, fill=CANV, weight="400", size=12.5,
     sub="what the enhancement is built around")
chip(54, 496, 264, 150, ["What the programme", "cannot observe"], MEMB, fill=CANV, weight="400", size=12.5,
     subs=["a purchase made outside a route that earns",
           "a competing programme or cashback card",
           "members named PC Optimum, Scene and RBC",
           "a trip abandoned after checking the price",
           "a plan the member has not told anyone"])
a(f'<text x="186" y="668" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MEMB}" font-weight="700">What the member gets back:</text>')
a(f'<text x="186" y="683" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MEMB}" font-weight="700">fewer steps, less uncertainty</text>')
a(f'<text x="186" y="706" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">What the programme records is what a member did</text>')
a(f'<text x="186" y="721" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">inside it, not everything they bought or wanted.</text>')

# ── BMO → programme → product, centre ──
band(404, 232, 794, 620, "BMO", "Owns Blue Rewards, funds it and carries the cost of the points members hold.", BMO, dashed=False)
for i, t in enumerate(["Finance and risk", "Programme leadership", "Banking relationship"]):
    chip(424 + i * 254, 282, 238, 40, [t], BMO, fill="#EEEDFE", size=12, weight="700")

band(424, 346, 752, 484, "Blue Rewards programme today", "Where the official records live. We would read from these and write back to them, not replace them.", PART, dashed=False)
for i, t in enumerate(["Offer service", "Points and transactions", "Catalogue and travel", "Support and cases"]):
    chip(442 + i * 184, 396, 168, 40, [t], PART, fill="#E1F5EE", size=11.5)

a(f'<rect x="442" y="462" width="714" height="348" rx="14" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/>')
a(f'<text x="799" y="494" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{GOLD}" font-weight="700" letter-spacing="1.6">WHAT WE ARE PROPOSING TO BUILD</text>')
a(f'<text x="799" y="518" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">A dedicated space inside the Blue Rewards app and website. Everything around it already exists.</text>')
CAPS = [("Relevant Opportunity\nDiscovery", "Relevance"), ("Adaptive Value\nPlanning", "Clarity"),
        ("Transparent Value\nProgression", "Visibility"), ("Value Protection\nand Recovery", "Reliability")]
for i, (t, need) in enumerate(CAPS):
    x = 458 + i * 176
    a(f'<rect x="{x}" y="538" width="162" height="96" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2"/>')
    for j, ln in enumerate(t.split("\n")):
        a(f'<text x="{x+81}" y="{568+j*17}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#ffffff" font-weight="700">{e(ln)}</text>')
    a(f'<text x="{x+81}" y="{618}" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{GOLD}" letter-spacing="1.4">{e(need.upper())}</text>')
a(f'<rect x="458" y="650" width="682" height="40" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="6 4"/>')
a(f'<text x="800" y="675" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="#ffffff">Blue, the optional conversational assistant, works across all four and shares the same saved information</text>')
a(f'<text x="799" y="716" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{GOLD}">We would hold none of the official records. What we would own is whether the member understands them.</text>')
a(f'<rect x="458" y="736" width="682" height="58" rx="10" fill="none" stroke="#3C3489" stroke-width="1.4" stroke-dasharray="5 4"/>')
a(f'<text x="800" y="757" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#c9c9e0" font-weight="700">The only new records we would create</text>')
a(f'<text x="800" y="777" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#c9c9e0">A saved goal · a saved comparison · ranked options with the reason for the ranking · a case the member can follow</text>')

# ── evidence authorities, right ──
band(1234, 232, 430, 464, "Who holds the proof", ["Each knows a different part of what happened to a member.", "We would work with all five, and control none of them."], PART)
AUTH = [("Offer sponsor", "sets the terms"), ("Merchant and point of sale", "observes the purchase"),
        ("Card issuer and network", "observes the payment"), ("Affiliate and receipt processing", "attributes the activity"),
        ("Reward supplier and fulfilment", "delivers the reward")]
for i, (t, s) in enumerate(AUTH):
    chip(1256, 316 + i * 78, 386, 60, [t], PART, fill=CANV, size=12.5, sub=s)

# ── arrows ──
for c in (MEMB, BMO, PART, GOLD, MUTE):
    pass
arrow(318, 336, 452, 512, MEMB, "the member uses it", bend=(388, 410), lx=370, ly=388)
arrow(452, 580, 318, 470, MEMB, None, bend=(382, 560))
arrow(700, 456, 700, 462, PART, None)
a(f'<line x1="600" y1="438" x2="600" y2="458" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="612" y="454" font-family="{SANS}" font-size="11" fill="{PART}" font-weight="700">reads records</text>')
a(f'<line x1="968" y1="462" x2="968" y2="438" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="984" y="455" font-family="{SANS}" font-size="11" fill="{PART}" font-weight="700">writes goals and cases</text>')
arrow(1156, 480, 1256, 420, PART, "evidence arrives on their schedule", dashed=True, lx=1210, ly=372)
arrow(1256, 560, 1156, 620, PART, "cases routed to whoever is responsible", dashed=True, lx=1212, ly=676)

# ── journey and scope, bottom ──
a(f'<line x1="36" y1="884" x2="{W-36}" y2="884" stroke="#ddd7c6" stroke-width="1"/>')
a(f'<text x="36" y="916" font-family="{SERIF}" font-size="16" fill="{NAVY}" font-weight="700">The member journey it supports</text>')
JOURNEY = ["Explore · Decide", "Earn or redeem", "Follow progress", "Receive and use"]
x = 36
for i, t in enumerate(JOURNEY):
    w = len(t) * 7.6 + 36
    chip(x, 936, w, 38, [t], NAVY, fill="#ffffff", size=12.5, rx=19)
    x += w + 8
    if i < len(JOURNEY) - 1:
        a(f'<path d="M{x},955 L{x+12},955" stroke="{MUTE}" stroke-width="1.6" marker-end="url(#ar_{MUTE[1:]})"/>')
        x += 24
a(f'<text x="36" y="1004" font-family="{SANS}" font-size="12" fill="{MUTE}">Underneath, value moves through the five stages on the systems map. This enhancement does not move value itself \u2014 existing Blue Rewards services and partners still do that. It changes whether the member can see, judge, follow and recover it.</text>')
a(f'<text x="36" y="1042" font-family="{SERIF}" font-size="14" fill="{NAVY}" font-weight="700">Three measures we propose for these stages</text>')
MEAS = [("Opportunity Capture Rate", "opportunities begun \u00f7 opportunities worth offering", "Did it reach them, and did they act"),
        ("Earned Value Realization Rate", "value received \u00f7 value earned and due", "Did what they earned actually arrive"),
        ("End-to-End Realization Rate", "received and used \u00f7 opportunities available", "The whole journey, end to end")]
mx = 36
for nm, f, where in MEAS:
    w = 296
    a(f'<rect x="{mx}" y="1056" width="{w}" height="58" rx="10" fill="#ffffff" stroke="{PART}" stroke-width="1.5"/>')
    a(f'<text x="{mx+14}" y="1076" font-family="{SANS}" font-size="12" fill="{PART}" font-weight="700">{e(nm)}</text>')
    a(f'<text x="{mx+14}" y="1093" font-family="{SANS}" font-size="11" fill="{INK}">{e(f)}</text>')
    a(f'<text x="{mx+14}" y="1107" font-family="{SANS}" font-size="10.5" fill="{MUTE}">{e(where)}</text>')
    mx += w + 10

a(f'<rect x="980" y="900" width="684" height="212" rx="14" fill="#FCEBEB" stroke="#A32D2D" stroke-width="1.6"/>')
a(f'<text x="1004" y="930" font-family="{SERIF}" font-size="13" fill="#A32D2D" font-weight="700" letter-spacing="2">WHAT THIS ENHANCEMENT DOES NOT REPLACE</text>')
for i, t in enumerate(["Existing earning methods: partner scans, linked-card offers, receipts, Shops and BMO products.",
                       "Redemption fulfilment: gift cards, travel, merchandise and partner redemptions.",
                       "Merchant shopping, checkout and payment.",
                       "BMO and partner support where manual investigation or partner action is required.",
                       "Partner issuance, redemption and reversal: those services need partner credentials, not a member session."]):
    a(f'<text x="1004" y="{958+i*30}" font-family="{SANS}" font-size="12" fill="#4A1B0C">&#8226;  {e(t)}</text>')

a(f'<text x="36" y="{H-14}" font-family="{SANS}" font-size="11" fill="{MUTE}">Team Zig · Blue Rewards capstone · Figure for section 3 of the Product Requirements Document. Full interactive systems map: joannjmj48-ui.github.io/mdpm-capstone/systems-thinking-v2/</text>')

markers = "".join(
    f'<marker id="ar_{c[1:]}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
    f'<path d="M0,0 L9,3 L0,6 Z" fill="{c}"/></marker>' for c in (MEMB, BMO, PART, CTX, MUTE, GOLD, NAVY))

inner = (f'<defs>{markers}</defs>' + "".join(o[:SPLIT])
         + '<g transform="translate(0,46)">' + "".join(o[SPLIT:]) + "</g>")
svg_site = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
  f'aria-label="Where the product sits in the Blue Rewards system. The product is a dedicated space inside the existing '
  f'Blue Rewards app, nested within the programme systems of record, which are nested within BMO. The member is to the '
  f'left, evidence authorities to the right, and forces outside the boundary across the top. The product owns no system '
  f'of record.">{inner}</svg>')
svg_file = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}</svg>\n'

ROOT = pathlib.Path(__file__).resolve().parent.parent
(ROOT / "figures").mkdir(exist_ok=True)
(ROOT / "figures" / "product-in-the-system.svg").write_text(svg_file, encoding="utf-8")
(ROOT / "figures" / "_panel.svg").write_text(svg_site, encoding="utf-8")
print("Wrote figures/product-in-the-system.svg —", len(svg_file), "bytes")

