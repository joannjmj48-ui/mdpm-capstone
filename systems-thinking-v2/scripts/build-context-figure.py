#!/usr/bin/env python3
"""Build the PRD figure: where the product sits in the Blue Rewards system.

Writes a standalone SVG to figures/product-in-the-system.svg for insertion
into the PRD, and returns the same markup for the site panel.
Joann's MMIE 884 palette and type.
"""
import pathlib, html

W, H = 2040, 1772
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
    a(f'<path d="M{cx-14},{ay} A 14 14 0 1 1 {cx},{ay-14}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-linecap="round"/>')
    a(f'<path d="M{cx-4},{ay-19} L{cx+5},{ay-14} L{cx-4},{ay-9} Z" fill="{colour}"/>')
    ty = cy - ry + 140
    for st, sign in steps:
        words, ln, rows = st.split(), "", []
        for wd in words:
            if len(ln + " " + wd) > 17: rows.append(ln); ln = wd
            else: ln = (ln + " " + wd).strip()
        rows.append(ln)
        a(f'<text x="{cx-rx+16}" y="{ty}" font-family="{SERIF}" font-size="12" fill="{colour}" font-weight="700">{sign}</text>')
        for r2, row in enumerate(rows):
            a(f'<text x="{cx-rx+30}" y="{ty+r2*12}" font-family="{SANS}" font-size="10" fill="{INK}">{e(row)}</text>')
        ty += 12 * len(rows) + 5
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
loop(394, 580, 74, 170, "R1", ["Relevance", "flywheel"], PART,
     [("Member needs, preferences and activity", "+"), ("Personalized, understandable offers", "+"),
      ("Worthwhile benefits received", "+"), ("Repeat participation", "+"),
      ("Stronger BMO banking relationships", "+")],
     "no minuses · it compounds")

# ── BMO, the programme, and the enhancement ──
band(488, 250, 804, 696, "BMO", ["Owns Blue Rewards and funds it. Emerging Business, in gold, is our client.", "Each of the other teams holds a decision we would need."], BMO, dashed=False)
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

band(506, 392, 768, 532, "Blue Rewards programme today", ["The loyalty programme itself: the offers, the points, the catalogue, and the people who resolve cases.", "We would read from these services and write back to them. We would not replace any of them."], PART, dashed=False)
for i, t in enumerate(["Offer service", "Points and transactions", "Catalogue and travel", "Support and cases"]):
    chip(524 + i * 186, 462, 170, 40, [t], PART, fill="#E1F5EE", size=11.5)

a(f'<rect x="524" y="534" width="732" height="366" rx="14" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/>')
a(f'<text x="890" y="566" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{GOLD}" font-weight="700" letter-spacing="1.6">WHAT WE ARE PROPOSING TO BUILD</text>')
a(f'<text x="890" y="588" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#c9c9e0">An enhanced experience within the Blue Rewards app and website</text>')

FEATS = [("Relevant Opportunity\nDiscovery", "Relevance", "ranked options, with the\nreason for the ranking"),
         ("Adaptive Value\nPlanning", "Clarity", "a saved goal and\na saved comparison"),
         ("Transparent Value\nProgression", "Visibility", "what has arrived, and\nwhat is still expected"),
         ("Value Protection\nand Recovery", "Reliability", "a case the member\ncan follow"),
         ("Blue, the conversational\nassistant", "Across all four", "the same saved information,\nasked for in their own words")]
for i2, (t, need, out2) in enumerate(FEATS):
    if i2 < 3:
        x, y = 542 + i2 * 236, 604
    else:
        x, y = 660 + (i2 - 3) * 236, 728
    a(f'<rect x="{x}" y="{y}" width="228" height="112" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2"/>')
    for j2, ln in enumerate(t.split("\n")):
        a(f'<text x="{x+114}" y="{y+26+j2*16}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="#ffffff" font-weight="700">{e(ln)}</text>')
    a(f'<text x="{x+114}" y="{y+76}" text-anchor="middle" font-family="{SERIF}" font-size="10.5" fill="{GOLD}" letter-spacing="1.4">{e(need.upper())}</text>')
    for j2, ln in enumerate(out2.split("\n")):
        a(f'<text x="{x+114}" y="{y+94+j2*13}" text-anchor="middle" font-family="{SANS}" font-size="10" fill="#9a9ab8">{e(ln)}</text>')

# the four things a member does, from the brief — what all five features serve
STAGES = ["Explore and decide", "Earn or redeem", "Follow progress", "Receive and use"]
for i2, st in enumerate(STAGES):
    sx = 536 + i2 * 180
    a(f'<rect x="{sx}" y="852" width="168" height="42" rx="10" fill="#E6F1FB" stroke="{MEMB}" stroke-width="1.4"/>')
    a(f'<circle cx="{sx+22}" cy="873" r="11" fill="{MEMB}"/>')
    a(f'<text x="{sx+22}" y="877" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="#ffffff" font-weight="700">{i2+1}</text>')
    a(f'<text x="{sx+40}" y="878" font-family="{SANS}" font-size="11.5" fill="{NAVY}" font-weight="700">{e(st)}</text>')
    if i2 < 3:
        a(f'<text x="{sx+174}" y="878" text-anchor="middle" font-family="{SANS}" font-size="13" fill="#9a9ab8">&#8594;</text>')

# ── liability brake, between the core and the proof-holders ──
loop(1374, 580, 74, 170, "B1", ["Liability", "brake"], BMO,
     [("Points issued", "+"), ("Outstanding liability", "+"), ("Cost carried by Finance", "−"),
      ("Offer generosity", "+")],
     "one minus · it pushes back")

# ── who holds the proof, far right ──
band(1468, 250, 536, 520, "Evidence authorities", ["No single party sees a whole journey, so when value goes missing the evidence is split", "between them. Each sends what it has on its own schedule, so the programme often", "finds out late. We would ask all five and instruct none."], PART)
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
arrow(1466, 420, 1262, 446, PART, "‖  delay — they report on their own timeline", dashed=True, bend=(1364, 368), lx=1326, ly=236)
arrow(1256, 822, 1466, 766, PART, "+  we send each case to them", dashed=True, bend=(1372, 848), lx=1374, ly=890)


SPLIT2 = len(o)

# ── the problem the loops explain ──
a(f'<rect x="400" y="1006" width="1240" height="110" rx="14" fill="#FAECE7" stroke="{LOSS}" stroke-width="2"/>')
a(f'<text x="424" y="1036" font-family="{SERIF}" font-size="14" fill="{LOSS}" font-weight="700" letter-spacing="2">THE PROBLEM</text>')
a(f'<text x="424" y="1062" font-family="{SERIF}" font-size="17" fill="{NAVY}" font-weight="700">Available value does not reliably become realized value.</text>')
a(f'<text x="424" y="1084" font-family="{SANS}" font-size="12" fill="{INK}">Members miss opportunities worth having, cannot tell what they are owed, and give up when value goes missing. Realized value is the main variable. These three loops are why it stays lower than it could be:</text>')
EFFECT = [("R1", "should raise realized value \u2014 but its return leg is unconfirmed", PART),
          ("B1", "caps realized value by limiting how generous offers can be", BMO),
          ("B2", "drains realized value by turning delay into withdrawal", LOSS)]
ex = 424
for code, eff, col in EFFECT:
    a(f'<circle cx="{ex+10}" cy="{1100}" r="10" fill="{col}"/>')
    a(f'<text x="{ex+10}" y="{1104}" text-anchor="middle" font-family="{SERIF}" font-size="10" fill="#ffffff" font-weight="700">{code}</text>')
    a(f'<text x="{ex+26}" y="{1104}" font-family="{SANS}" font-size="11.5" fill="{col}">{e(eff)}</text>')
    ex += len(eff) * 6.1 + 60

# ── the loop that joins the member to the people holding the proof ──
a(f'<ellipse cx="890" cy="1196" rx="336" ry="74" fill="#ffffff" stroke="{LOSS}" stroke-width="2"/>')
a(f'<text x="890" y="1174" text-anchor="middle" font-family="{SERIF}" font-size="12.5" fill="{LOSS}" font-weight="700" letter-spacing="1.2">B2  &#183;  PROOF AND DOUBT BRAKE</text>')
B2 = [("Member activity", "+"), ("Time to confirm ‖", "+"), ("Member doubt", "−"), ("Participation", "+")]
bx = 590
for st, sign in B2:
    w = len(st) * 6.0 + 18
    a(f'<rect x="{bx}" y="{1186}" width="{w}" height="22" rx="11" fill="{CANV}" stroke="{LOSS}" stroke-width="1.1"/>')
    a(f'<text x="{bx+w/2}" y="{1201}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(st)}</text>')
    bx += w + 5
    if st != B2[-1][0]:
        a(f'<text x="{bx}" y="{1202}" font-family="{SERIF}" font-size="13" fill="{LOSS}" font-weight="700">{sign}</text>')
        bx += 14
a(f'<text x="890" y="1230" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">One minus and a delay. The lag before a member can confirm that a purchase</text>')
a(f'<text x="890" y="1245" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{MUTE}">counted, or that a missing reward is being handled, is what manufactures doubt.</text>')
a(f'<line x1="890" y1="996" x2="890" y2="1046" stroke="{LOSS}" stroke-width="2.2" marker-end="url(#ar_{LOSS[1:]})"/>')
a(f'<path d="M1736,822 Q1872,1096 1240,1240" fill="none" stroke="{LOSS}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ar_{LOSS[1:]})" opacity="0.65"/>')
a(f'<path d="M172,696 Q168,1076 540,1240" fill="none" stroke="{LOSS}" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#ar_{LOSS[1:]})" opacity="0.65"/>')

a(f'<circle cx="1284" cy="500" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="1284" y="504" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">1</text>')
a(f'<circle cx="1230" cy="660" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="1230" y="664" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">2</text>')
a(f'<circle cx="876" cy="786" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="876" y="790" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">3</text>')
a(f'<circle cx="758" cy="660" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="758" y="664" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">4</text>')
a(f'<circle cx="330" cy="500" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
a(f'<text x="330" y="504" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">5</text>')

a(f'<rect x="36" y="1522" width="1180" height="254" rx="14" fill="#F6F1E4" stroke="{GOLD}" stroke-width="1.6"/>')
a(f'<text x="60" y="1552" font-family="{SERIF}" font-size="15" fill="{NAVY}" font-weight="700" letter-spacing="1.4">LEVERAGE POINTS</text>')
a(f'<text x="256" y="1552" font-family="{SANS}" font-size="11" fill="{MUTE}">Each one changes a loop above. Grouped under the three candidate leverage points in the faculty brief.</text>')
LEV = [("1", "Make realized value the goal", "Not issued value, not activity, not breakage. Changes what the scoreboard rewards, so it changes B1.", "Objectives and measurement"),
       ("2", "Connect the value states", "Make what is earned, pending, posted and used visible as one thing. Shortens the delay in B2.", "Information flows"),
       ("3", "Detect and resolve missing value", "Find at-risk value early and route it. This is the recovery capability.", "Rules and accountability"),
       ("4", "Treat consent as spendable", "Intrusion spends it, so personalization has a ceiling. Caps how hard R1 can be pushed.", "Rules and accountability"),
       ("5", "Learn from realized outcomes", "Feed what actually arrived back into relevance. This is the return leg of R1.", "Information flows")]
for i2, (n, t, sb, fam) in enumerate(LEV):
    col, row = (0, i2) if i2 < 3 else (1, i2 - 3)
    x = 60 + col * 580
    y = 1586 + row * 66
    a(f'<circle cx="{x+13}" cy="{y}" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
    a(f'<text x="{x+13}" y="{y+4}" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="{NAVY}" font-weight="700">{n}</text>')
    a(f'<text x="{x+34}" y="{y+4}" font-family="{SANS}" font-size="12" fill="{NAVY}" font-weight="700">{e(t)}</text>')
    words = sb.split(); ln, out2 = "", []
    for wd in words:
        if len(ln + " " + wd) > 62: out2.append(ln); ln = wd
        else: ln = (ln + " " + wd).strip()
    out2.append(ln)
    for j2, l2 in enumerate(out2[:2]):
        a(f'<text x="{x+34}" y="{y+22+j2*14}" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(l2)}</text>')
    a(f'<text x="{x+34}" y="{y+50}" font-family="{SERIF}" font-size="9.5" fill="#854F0B" letter-spacing="1.1">{e(fam.upper())}</text>')

# ── downstream stakeholders ──
a(f'<rect x="36" y="1296" width="{W-72}" height="200" rx="14" fill="#F1EFE8" stroke="{MUTE}" stroke-width="1.4"/>')
a(f'<text x="{W/2}" y="1326" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{NAVY}" font-weight="700" letter-spacing="1.4">DOWNSTREAM STAKEHOLDERS</text>')
a(f'<text x="{W/2}" y="1346" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">Who this reaches, and what it would mean for them</text>')
DOWN = [("Members", "Fewer steps and less uncertainty, and a way to see what is owed", MEMB),
        ("Finance and risk", "Recovered points reduce breakage, and liability ages differently", BMO),
        ("Support and operations", "Inquiries rise before they fall, because loss becomes visible", LOSS),
        ("Earn and redeem partners", "Ranking changes who gets seen, and who does not", PART),
        ("Cards and Credit", "More reason to hold the card, but only if the flywheel turns", BMO)]
cw = (W - 72 - 40 - 4 * 12) / 5
for i, (t, sb, col) in enumerate(DOWN):
    x = 56 + i * (cw + 12)
    a(f'<rect x="{x}" y="1366" width="{cw}" height="112" rx="10" fill="#ffffff" stroke="{col}" stroke-width="1.5"/>')
    a(f'<rect x="{x}" y="1366" width="{cw}" height="4" rx="2" fill="{col}"/>')
    a(f'<text x="{x+cw/2}" y="1398" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{col}" font-weight="700">{e(t)}</text>')
    words = sb.split()
    ln, out_lines = "", []
    for wd in words:
        if len(ln + " " + wd) > 34:
            out_lines.append(ln); ln = wd
        else:
            ln = (ln + " " + wd).strip()
    out_lines.append(ln)
    for j, l2 in enumerate(out_lines[:4]):
        a(f'<text x="{x+cw/2}" y="{1422+j*16}" text-anchor="middle" font-family="{SANS}" font-size="10.5" fill="{INK}">{e(l2)}</text>')

# ── what this does not replace ──
a(f'<rect x="1246" y="1522" width="758" height="254" rx="14" fill="#FCEBEB" stroke="{LOSS}" stroke-width="1.6"/>')
a(f'<text x="1270" y="1552" font-family="{SERIF}" font-size="13" fill="{LOSS}" font-weight="700" letter-spacing="2">WHAT THIS DOES NOT REPLACE</text>')
NR = ["Existing earning methods: partner scans, linked-card offers, receipts, Shops and BMO products.",
      "Redemption fulfilment: gift cards, travel, merchandise and partner redemptions.",
      "Merchant shopping, checkout and payment.",
      "BMO and partner support where manual investigation or partner action is required.",
      "Partner issuance, redemption and reversal: those services need partner credentials, not a member session."]
for i, t in enumerate(NR):
    words = t.split(); ln, wrapped = "", []
    for wd in words:
        if len(ln + " " + wd) > 86: wrapped.append(ln); ln = wd
        else: ln = (ln + " " + wd).strip()
    wrapped.append(ln)
    base = 1584 + i * 34
    for k2, l3 in enumerate(wrapped[:2]):
        a(f'<text x="{1270 if k2 == 0 else 1284}" y="{base+k2*14}" font-family="{SANS}" font-size="11" fill="#4A1B0C">{"&#8226;  " if k2 == 0 else ""}{e(l3)}</text>')

a(f'<text x="36" y="{H+28}" font-family="{SANS}" font-size="11" fill="{MUTE}">Team Zig &#183; Blue Rewards capstone &#183; Figure for section 3 of the Product Requirements Document. Full interactive systems map: joannjmj48-ui.github.io/mdpm-capstone/systems-thinking-v2/</text>')


markers = "".join(
    f'<marker id="ar_{c[1:]}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
    f'<path d="M0,0 L9,3 L0,6 Z" fill="{c}"/></marker>' for c in (MEMB, BMO, PART, CTX, MUTE, GOLD, NAVY))

inner = (f'<defs>{markers}</defs>' + "".join(o[:SPLIT])
         + '<g transform="translate(0,0)">' + "".join(o[SPLIT:SPLIT2]) + "</g>"
         + '<g transform="translate(0,-46)">' + "".join(o[SPLIT2:]) + "</g>")
svg_site = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
  f'aria-label="Where the product sits in the Blue Rewards system. The product is a dedicated space inside the existing '
  f'Blue Rewards app, nested within the programme systems of record, which are nested within BMO. The member is to the '
  f'left, evidence authorities to the right, and forces outside the boundary across the top. It holds none of the '
  f'records; what it changes is how much of the available value a member ends up with, by helping them find what is '
  f'worth having, decide on it, follow it through, and recover it when it goes missing. Three feedback loops explain '
  f'why realized value stays lower than it could be, and five leverage points act on those loops.">{inner}</svg>')
svg_file = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}</svg>\n'

ROOT = pathlib.Path(__file__).resolve().parent.parent
(ROOT / "figures").mkdir(exist_ok=True)
(ROOT / "figures" / "product-in-the-system.svg").write_text(svg_file, encoding="utf-8")
(ROOT / "figures" / "_panel.svg").write_text(svg_site, encoding="utf-8")
print("Wrote figures/product-in-the-system.svg —", len(svg_file), "bytes")

