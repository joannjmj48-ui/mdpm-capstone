#!/usr/bin/env python3
"""Build the PRD figure: where the product sits in the Blue Rewards system.

Writes a standalone SVG to figures/product-in-the-system.svg for insertion
into the PRD, and returns the same markup for the site panel.
Joann's MMIE 884 palette and type.
"""
import pathlib, html

W, H = 2040, 1722
INK, CANV, NAVY, GOLD = "#2b2b33", "#fbfaf6", "#10123f", "#C79A3B"
MUTE, MEMB, BMO, PART, CTX = "#8a8a92", "#185FA5", "#534AB7", "#0F6E56", "#854F0B"
LOSS = "#A32D2D"
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
a(f'<rect width="{W}" height="92" fill="{NAVY}"/><rect y="92" width="{W}" height="4" fill="{GOLD}"/>')
a(f'<text x="36" y="40" font-family="{SERIF}" font-size="13" fill="{GOLD}" letter-spacing="2.8" font-weight="700">TEAM ZIG  &#183;  BLUE REWARDS  &#183;  SYSTEMS MAP</text>')
a(f'<text x="36" y="74" font-family="{SERIF}" font-size="26" fill="#ffffff" font-weight="700">Systems Map 2.0</text>')
a(f'<text x="{W-36}" y="40" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">Team Zig &#183; November 2026</text>')
a(f'<text x="{W-36}" y="60" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">An enhanced experience within Blue Rewards</text>')
a(f'<text x="{W-36}" y="82" text-anchor="end" font-family="{SANS}" font-size="11" fill="{GOLD}">+ same direction &#183; &#8722; opposite direction &#183; &#8214; significant delay &#183; R reinforcing, B balancing</text>')
SPLIT = len(o)

def loop(cx, cy, rx, ry, code, title, colour, steps, foot):
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" stroke="{colour}" stroke-width="2"/>')
    a(f'<text x="{cx}" y="{cy-ry+26}" text-anchor="middle" font-family="{SERIF}" font-size="12.5" fill="{colour}" font-weight="700" letter-spacing="1.2">{e(code)}</text>')
    for i, ln in enumerate(title):
        a(f'<text x="{cx}" y="{cy-ry+46+i*15}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{colour}" font-weight="700">{e(ln)}</text>')
    ay = cy - ry + 112
    a(f'<path d="M{cx-15},{ay} A 15 15 0 1 1 {cx},{ay-15}" fill="none" stroke="{colour}" stroke-width="2.4" marker-end="url(#ar_{colour[1:]})"/>')
    ty = cy - ry + 146
    for st, sign in steps:
        a(f'<text x="{cx-rx+16}" y="{ty}" font-family="{SERIF}" font-size="12" fill="{colour}" font-weight="700">{sign}</text>')
        a(f'<text x="{cx-rx+32}" y="{ty}" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(st)}</text>')
        ty += 17
    a(f'<text x="{cx}" y="{cy+ry+18}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{colour}" font-weight="700">{e(foot)}</text>')

# ── outside the boundary ──
band(36, 116, W - 72, 104, "Outside the boundary", None, CTX)
OUT = [("Regulation and privacy", "privacy law, consent rules, suitability, disclosure"),
       ("Competitor programmes", "PC Optimum, Scene, bank and card ecosystems"),
       ("Member expectations", "formed by every other app they use, and not always realistic"),
       ("Technology landscape", "AI, identity, interoperability, data portability")]
for i, (t, sb) in enumerate(OUT):
    chip(392 + i * 400, 148, 380, 54, [t], CTX, fill=CANV, weight="700", size=12.5, sub=sb)

# ── the member, far left ──
band(36, 250, 272, 392, "The member", None, MEMB)
chip(54, 300, 236, 60, ["Member"], MEMB, fill="#E6F1FB", size=14, sub="a member, a BMO client, or both")
chip(54, 378, 236, 96, ["Spending they already", "intend to make"], MEMB, fill=CANV, weight="400", size=12,
     sub="what the enhancement is built around")
a(f'<text x="172" y="512" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MEMB}" font-weight="700">&#8722;  What the member gets back:</text>')
a(f'<text x="172" y="527" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{MEMB}" font-weight="700">fewer steps, less uncertainty</text>')
a(f'<text x="172" y="556" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">What the programme records is what</text>')
a(f'<text x="172" y="570" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">a member did inside it, not everything</text>')
a(f'<text x="172" y="584" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">they bought or wanted.</text>')

# ── relevance flywheel, between the member and the core ──
loop(394, 560, 74, 196, "R1", ["Relevance", "flywheel"], PART,
     [("Realized value", "+"), ("Participation", "+"), ("Permissioned signal", "+"),
      ("Decisioning relevance", "+")],
     "no minuses · it compounds")

# ── BMO, the programme, and the enhancement ──
band(488, 250, 804, 742, "BMO", ["Owns Blue Rewards and funds it. Emerging Business, in gold, is our client.", "Each of the other teams holds a decision we would need."], BMO, dashed=False)
BMO_TEAMS = [("Emerging Business", "our client · Drew’s team", True),
             ("Programme leadership", "sets direction, funds it", False),
             ("Cards and Credit", "the banking earning routes", False),
             ("Data and Analytics", "the records and the decisioning", False),
             ("Finance and risk", "carries the cost of points held", False)]
for i, (t, sb, client) in enumerate(BMO_TEAMS):
    x = 506 + i * 154
    col = GOLD if client else BMO
    a(f'<rect x="{x}" y="326" width="148" height="46" rx="10" fill="{"#FAEEDA" if client else "#EEEDFE"}" stroke="{col}" stroke-width="{2 if client else 1.4}"/>')
    a(f'<text x="{x+74}" y="345" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{"#854F0B" if client else BMO}" font-weight="700">{e(t)}</text>')
    a(f'<text x="{x+74}" y="361" text-anchor="middle" font-family="{SANS}" font-size="9.5" fill="{MUTE}">{e(sb)}</text>')

band(506, 392, 768, 578, "Blue Rewards programme today", ["The loyalty programme itself: the offers, the points, the catalogue, and the people who resolve cases.", "We would read from these services and write back to them. We would not replace any of them."], PART, dashed=False)
for i, t in enumerate(["Offer service", "Points and transactions", "Catalogue and travel", "Support and cases"]):
    chip(524 + i * 186, 462, 170, 40, [t], PART, fill="#E1F5EE", size=11.5)

a(f'<rect x="524" y="534" width="732" height="414" rx="14" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/>')
a(f'<text x="890" y="566" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{GOLD}" font-weight="700" letter-spacing="1.6">WHAT WE ARE PROPOSING TO BUILD</text>')
a(f'<text x="890" y="590" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">A dedicated space inside the Blue Rewards app and website.</text>')
CAPS = [("Relevant Opportunity\nDiscovery", "Relevance"), ("Adaptive Value\nPlanning", "Clarity"),
        ("Transparent Value\nProgression", "Visibility"), ("Value Protection\nand Recovery", "Reliability")]
for i, (t, need) in enumerate(CAPS):
    x = 542 + i * 180
    a(f'<rect x="{x}" y="610" width="164" height="96" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2"/>')
    for j, ln in enumerate(t.split("\n")):
        a(f'<text x="{x+82}" y="{640+j*17}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#ffffff" font-weight="700">{e(ln)}</text>')
    a(f'<text x="{x+82}" y="690" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{GOLD}" letter-spacing="1.4">{e(need.upper())}</text>')
a(f'<rect x="542" y="724" width="692" height="38" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2" stroke-dasharray="6 4"/>')
a(f'<text x="888" y="748" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#ffffff">Blue, the optional conversational assistant, works across all four and shares the same saved information</text>')
a(f'<text x="890" y="786" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{GOLD}">The programme still runs the offers, the points and the rewards. What we would own is whether the member understands them.</text>')
a(f'<rect x="542" y="804" width="692" height="60" rx="10" fill="none" stroke="#3C3489" stroke-width="1.4" stroke-dasharray="5 4"/>')
a(f'<text x="888" y="826" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#c9c9e0" font-weight="700">The only new records we would create</text>')
a(f'<text x="888" y="846" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#c9c9e0">A saved goal &#183; a saved comparison &#183; ranked options with the reason for the ranking &#183; a case the member can follow</text>')
a(f'<text x="890" y="890" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#c9c9e0">The member journey it supports:  Explore and decide  &#8594;  Earn or redeem  &#8594;  Follow progress  &#8594;  Receive and use</text>')
a(f'<text x="890" y="914" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="#9a9ab8">Underneath, value moves through the five stages on the map. This enhancement does not move value; it changes whether the member can see, judge, follow and recover it.</text>')

# ── liability brake, between the core and the proof-holders ──
loop(1374, 560, 74, 196, "B1", ["Liability", "brake"], BMO,
     [("Points issued", "+"), ("Outstanding liability", "+"), ("Cost carried by Finance", "−"),
      ("Offer generosity", "+")],
     "one minus · it pushes back")

# ── who holds the proof, far right ──
band(1468, 250, 536, 520, "Who holds the proof", ["No single one sees a whole journey, so when value goes missing the proof is split", "between them. Each sends what it has on its own schedule, so the programme often", "finds out late. We would ask all five and instruct none."], PART)
AUTH = [("Offer sponsor", "writes the eligibility rules, the reward amount and the deadlines"),
        ("Merchant and point of sale", "the only party that sees what was actually in the basket"),
        ("Card issuer and network", "sees a merchant and an amount, and decides when it settles"),
        ("Affiliate and receipt processing", "ties an online click or a photographed receipt to the member"),
        ("Reward supplier and fulfilment", "ships the gift card, books the trip, decides when it arrives")]
for i, (t, sb) in enumerate(AUTH):
    chip(1488, 352 + i * 80, 496, 62, [t], PART, fill=CANV, size=12.5, sub=sb)

# ── arrows across the boundaries ──
arrow(292, 300, 520, 566, MEMB, "+  the member uses it", bend=(430, 288), lx=398, ly=262)
arrow(520, 826, 292, 600, MEMB, None, bend=(398, 846))
a(f'<line x1="640" y1="504" x2="640" y2="528" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="652" y="522" font-family="{SANS}" font-size="11" fill="{PART}" font-weight="700">+  reads records</text>')
a(f'<line x1="1070" y1="528" x2="1070" y2="504" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="1082" y="522" font-family="{SANS}" font-size="11" fill="{PART}" font-weight="700">+  writes goals and cases</text>')
arrow(1466, 460, 1262, 600, PART, "‖  delay — they report on their own timeline", dashed=True, lx=1326, ly=318)
arrow(1262, 760, 1466, 700, PART, "+  we send each case to them", dashed=True, lx=1380, ly=800)

# ── the loop that joins the member to the people holding the proof ──
a(f'<ellipse cx="890" cy="1066" rx="330" ry="66" fill="#ffffff" stroke="{LOSS}" stroke-width="2"/>')
a(f'<text x="890" y="1042" text-anchor="middle" font-family="{SERIF}" font-size="12.5" fill="{LOSS}" font-weight="700" letter-spacing="1.2">B2  &#183;  PROOF AND DOUBT BRAKE</text>')
B2 = [("Member activity", "+"), ("Time to confirm ‖", "+"), ("Member doubt", "−"), ("Participation", "+")]
bx = 590
for st, sign in B2:
    w = len(st) * 6.0 + 18
    a(f'<rect x="{bx}" y="{1054}" width="{w}" height="22" rx="11" fill="{CANV}" stroke="{LOSS}" stroke-width="1.1"/>')
    a(f'<text x="{bx+w/2}" y="{1069}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(st)}</text>')
    bx += w + 5
    if st != B2[-1][0]:
        a(f'<text x="{bx}" y="{1070}" font-family="{SERIF}" font-size="13" fill="{LOSS}" font-weight="700">{sign}</text>')
        bx += 14
a(f'<text x="890" y="1104" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">One minus and a delay. The lag before a member can confirm what happened is what manufactures doubt.</text>')
a(f'<line x1="890" y1="950" x2="890" y2="996" stroke="{LOSS}" stroke-width="2.2" marker-end="url(#ar_{LOSS[1:]})"/>')
a(f'<path d="M1736,772 Q1620,980 1222,1050" fill="none" stroke="{LOSS}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ar_{LOSS[1:]})" opacity="0.65"/>')
a(f'<path d="M172,646 Q300,980 558,1050" fill="none" stroke="{LOSS}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ar_{LOSS[1:]})" opacity="0.65"/>')

a(f'<circle cx="1284" cy="452" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="1284" y="456" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">1</text>')
a(f'<circle cx="1046" cy="600" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="1046" y="604" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">2</text>')
a(f'<circle cx="1222" cy="600" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="1222" y="604" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">3</text>')
a(f'<circle cx="686" cy="600" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="686" y="604" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">4</text>')
a(f'<circle cx="330" cy="356" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="330" y="360" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">5</text>')

a(f'<rect x="36" y="1162" width="{W-72}" height="150" rx="14" fill="#F6F1E4" stroke="{GOLD}" stroke-width="1.6"/>')
a(f'<text x="60" y="1192" font-family="{SERIF}" font-size="15" fill="{NAVY}" font-weight="700" letter-spacing="1.4">LEVERAGE POINTS</text>')
a(f'<text x="256" y="1192" font-family="{SANS}" font-size="11" fill="{MUTE}">Where the team converged on intervening. The numbered markers show where each one acts on this map.</text>')
LEV = [("1", "Make realized value the goal", "Not issued value, not activity, not breakage. Changes what the scoreboard rewards, so it changes B1."),
       ("2", "Connect the value states", "Make what is earned, pending, posted and used visible as one thing. Shortens the delay in B2."),
       ("3", "Detect and resolve missing value", "Find at-risk value early and route it. This is the recovery capability."),
       ("4", "Treat consent as spendable", "Intrusion spends it, so personalization has a ceiling. Caps how hard R1 can be pushed."),
       ("5", "Learn from realized outcomes", "Feed what actually arrived back into relevance. This is the return leg of R1.")]
lw = (W - 72 - 40 - 4 * 10) / 5
for i, (n, t, sb) in enumerate(LEV):
    x = 56 + i * (lw + 10)
    a(f'<circle cx="{x+16}" cy="{1226}" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
    a(f'<text x="{x+16}" y="{1230}" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">{n}</text>')
    a(f'<text x="{x+38}" y="{1230}" font-family="{SANS}" font-size="12" fill="{NAVY}" font-weight="700">{e(t)}</text>')
    words = sb.split(); ln, out2 = "", []
    for wd in words:
        if len(ln + " " + wd) > 46: out2.append(ln); ln = wd
        else: ln = (ln + " " + wd).strip()
    out2.append(ln)
    for j, l2 in enumerate(out2[:4]):
        a(f'<text x="{x+16}" y="{1256+j*15}" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(l2)}</text>')

# ── downstream stakeholders ──
a(f'<rect x="36" y="1338" width="{W-72}" height="200" rx="14" fill="#F1EFE8" stroke="{MUTE}" stroke-width="1.4"/>')
a(f'<text x="{W/2}" y="1368" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{NAVY}" font-weight="700" letter-spacing="1.4">DOWNSTREAM STAKEHOLDERS</text>')
a(f'<text x="{W/2}" y="1388" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">Who this reaches, and what it would mean for them</text>')
DOWN = [("Members", "Fewer steps and less uncertainty, and a way to see what is owed", MEMB),
        ("Finance and risk", "Recovered points reduce breakage, and liability ages differently", BMO),
        ("Support and operations", "Inquiries rise before they fall, because loss becomes visible", LOSS),
        ("Earn and redeem partners", "Ranking changes who gets seen, and who does not", PART),
        ("Cards and Credit", "More reason to hold the card, but only if the flywheel turns", BMO)]
cw = (W - 72 - 40 - 4 * 12) / 5
for i, (t, sb, col) in enumerate(DOWN):
    x = 56 + i * (cw + 12)
    a(f'<rect x="{x}" y="1408" width="{cw}" height="112" rx="10" fill="#ffffff" stroke="{col}" stroke-width="1.5"/>')
    a(f'<rect x="{x}" y="1408" width="{cw}" height="4" rx="2" fill="{col}"/>')
    a(f'<text x="{x+cw/2}" y="1440" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{col}" font-weight="700">{e(t)}</text>')
    words = sb.split()
    ln, out_lines = "", []
    for wd in words:
        if len(ln + " " + wd) > 34:
            out_lines.append(ln); ln = wd
        else:
            ln = (ln + " " + wd).strip()
    out_lines.append(ln)
    for j, l2 in enumerate(out_lines[:4]):
        a(f'<text x="{x+cw/2}" y="{1464+j*16}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(l2)}</text>')

# ── what this does not replace ──
a(f'<rect x="36" y="1568" width="{W-72}" height="124" rx="14" fill="#FCEBEB" stroke="{LOSS}" stroke-width="1.6"/>')
a(f'<text x="60" y="1596" font-family="{SERIF}" font-size="13" fill="{LOSS}" font-weight="700" letter-spacing="2">WHAT THIS ENHANCEMENT DOES NOT REPLACE</text>')
NR = ["Existing earning methods: partner scans, linked-card offers, receipts, Shops and BMO products.",
      "Redemption fulfilment: gift cards, travel, merchandise and partner redemptions.",
      "Merchant shopping, checkout and payment.",
      "BMO and partner support where manual investigation or partner action is required.",
      "Partner issuance, redemption and reversal: those services need partner credentials, not a member session."]
for i, t in enumerate(NR):
    col_x = 60 if i < 3 else 1060
    row = i if i < 3 else i - 3
    a(f'<text x="{col_x}" y="{1622+row*24}" font-family="{SANS}" font-size="11.5" fill="#4A1B0C">&#8226;  {e(t)}</text>')

a(f'<text x="36" y="{H-18}" font-family="{SANS}" font-size="11" fill="{MUTE}">Team Zig &#183; Blue Rewards capstone &#183; Figure for section 3 of the Product Requirements Document. Full interactive systems map: joannjmj48-ui.github.io/mdpm-capstone/systems-thinking-v2/</text>')


markers = "".join(
    f'<marker id="ar_{c[1:]}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
    f'<path d="M0,0 L9,3 L0,6 Z" fill="{c}"/></marker>' for c in (MEMB, BMO, PART, CTX, MUTE, GOLD, NAVY))

inner = (f'<defs>{markers}</defs>' + "".join(o[:SPLIT])
         + '<g transform="translate(0,0)">' + "".join(o[SPLIT:]) + "</g>")
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

