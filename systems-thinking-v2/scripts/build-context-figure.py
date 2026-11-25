#!/usr/bin/env python3
"""Build the PRD figure: where the product sits in the Blue Rewards system.

Writes a standalone SVG to figures/product-in-the-system.svg for insertion
into the PRD and the slide deck, and returns the same markup for the site
panel. Laid out 16:9 so it drops onto a slide without side margins.
Joann's MMIE 884 palette and type.
"""
import pathlib, html

W, H = 2560, 1440
INK, CANV, NAVY, GOLD = "#2b2b33", "#fbfaf6", "#10123f", "#C79A3B"
MUTE, MEMB, BMO, PART, CTX = "#8a8a92", "#185FA5", "#534AB7", "#0F6E56", "#854F0B"
LOSS = "#A32D2D"
SANS, SERIF = "Helvetica,Arial,sans-serif", "Georgia,serif"

o = []
def a(s): o.append(s)
def e(s): return html.escape(str(s), quote=False)

def wrap(text, n):
    words, ln, rows = text.split(), "", []
    for wd in words:
        if len(ln + " " + wd) > n: rows.append(ln); ln = wd
        else: ln = (ln + " " + wd).strip()
    rows.append(ln)
    return rows

def band(x, y, w, h, label, note, colour, dashed=True, fill=None):
    notes = note if isinstance(note, (list, tuple)) else ([note] if note else [])
    d = ' stroke-dasharray="7 5"' if dashed else ""
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill or "none"}" stroke="{colour}" stroke-width="1.8"{d}/>')
    a(f'<text x="{x+18}" y="{y+26}" font-family="{SERIF}" font-size="15" fill="{colour}" font-weight="700" letter-spacing="2.2">{e(label.upper())}</text>')
    for i, ln in enumerate(notes):
        a(f'<text x="{x+18}" y="{y+48+i*17}" font-family="{SANS}" font-size="13" fill="{MUTE}">{e(ln)}</text>')

def chip(x, y, w, h, lines, colour, fill="#ffffff", weight="700", size=14.5, rx=10, sub=None):
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{colour}" stroke-width="1.6"/>')
    cy = y + h / 2 - (len(lines) - 1) * 9 + (0 if not sub else -8)
    for i, ln in enumerate(lines):
        a(f'<text x="{x+w/2}" y="{cy+i*18+5}" text-anchor="middle" font-family="{SANS}" font-size="{size}" fill="{colour}" font-weight="{weight}">{e(ln)}</text>')
    if sub:
        a(f'<text x="{x+w/2}" y="{y+h-11}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">{e(sub)}</text>')

def arrow(x1, y1, x2, y2, colour, label=None, dashed=False, lx=None, ly=None, bend=None):
    d = ' stroke-dasharray="6 5"' if dashed else ""
    path = f'M{x1},{y1} Q{bend[0]},{bend[1]} {x2},{y2}' if bend else f'M{x1},{y1} L{x2},{y2}'
    a(f'<path d="{path}" fill="none" stroke="{colour}" stroke-width="2.2"{d} marker-end="url(#ar_{colour[1:]})" opacity="0.9"/>')
    if label:
        mx = lx if lx is not None else (x1 + x2) / 2
        my = ly if ly is not None else (y1 + y2) / 2 - 14
        w = len(label) * 6.8 + 24
        a(f'<rect x="{mx-w/2}" y="{my-12}" width="{w}" height="24" rx="12" fill="{CANV}" stroke="{colour}" stroke-width="1"/>')
        a(f'<text x="{mx}" y="{my+4}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{colour}" font-weight="700">{e(label)}</text>')

def badge(cx, cy, n):
    a(f'<circle cx="{cx}" cy="{cy}" r="13" fill="{GOLD}" stroke="{NAVY}" stroke-width="1.4"/>')
    a(f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="{SERIF}" font-size="12" fill="{NAVY}" font-weight="700">{n}</text>')

def loop(cx, cy, rx, ry, code, title, colour, steps, foot):
    a(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#ffffff" stroke="{colour}" stroke-width="2"/>')
    a(f'<text x="{cx}" y="{cy-ry+26}" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{colour}" font-weight="700" letter-spacing="1.2">{e(code)}</text>')
    for i, ln in enumerate(title):
        a(f'<text x="{cx}" y="{cy-ry+48+i*17}" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{colour}" font-weight="700">{e(ln)}</text>')
    ay = cy - ry + 112
    a(f'<path d="M{cx-14},{ay} A 14 14 0 1 1 {cx},{ay-14}" fill="none" stroke="{colour}" stroke-width="2.2" stroke-linecap="round"/>')
    a(f'<path d="M{cx-4},{ay-19} L{cx+5},{ay-14} L{cx-4},{ay-9} Z" fill="{colour}"/>')
    ty = cy - ry + 140
    for st, sign in steps:
        rows = wrap(st, 17)
        a(f'<text x="{cx-rx+16}" y="{ty}" font-family="{SERIF}" font-size="13" fill="{colour}" font-weight="700">{sign}</text>')
        for r2, row in enumerate(rows):
            a(f'<text x="{cx-rx+34}" y="{ty+r2*13}" font-family="{SANS}" font-size="11" fill="{INK}">{e(row)}</text>')
        ty += 13 * len(rows) + 5
    a(f'<text x="{cx}" y="{cy+ry+20}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{colour}" font-weight="700">{e(foot)}</text>')


# ── canvas and masthead ──────────────────────────────────────────────────
a(f'<rect width="{W}" height="{H}" fill="{CANV}"/>')
a(f'<rect width="{W}" height="88" fill="{NAVY}"/><rect y="88" width="{W}" height="4" fill="{GOLD}"/>')
a(f'<text x="36" y="38" font-family="{SERIF}" font-size="13" fill="{GOLD}" letter-spacing="2.8" font-weight="700">TEAM ZIG  &#183;  BLUE REWARDS  &#183;  SYSTEMS MAP</text>')
a(f'<text x="36" y="72" font-family="{SERIF}" font-size="25" fill="#ffffff" font-weight="700">Systems Map 2.0</text>')
a(f'<text x="{W-36}" y="36" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">Team Zig &#183; November 2026</text>')
a(f'<text x="{W-36}" y="56" text-anchor="end" font-family="{SANS}" font-size="12.5" fill="#c9c9e0">An enhanced experience within Blue Rewards</text>')
a(f'<text x="{W-36}" y="78" text-anchor="end" font-family="{SANS}" font-size="11.5" fill="{GOLD}">+ same direction &#183; &#8722; opposite direction &#183; &#8214; significant delay &#183; R reinforcing, B balancing</text>')

# ── the problem leads the figure, with the loop that most directly explains it ──
a(f'<rect x="36" y="108" width="1480" height="144" rx="14" fill="#FAECE7" stroke="{LOSS}" stroke-width="2"/>')
a(f'<text x="776" y="138" text-anchor="middle" font-family="{SERIF}" font-size="15" fill="{LOSS}" font-weight="700" letter-spacing="2">THE PROBLEM</text>')
a(f'<text x="776" y="170" text-anchor="middle" font-family="{SERIF}" font-size="20" fill="{NAVY}" font-weight="700">Available value does not reliably become realized value.</text>')
a(f'<text x="776" y="196" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{INK}">Members miss opportunities worth having, cannot tell what they are owed, and give up when value goes missing. Realized value is the main variable.</text>')
EFFECT = [("R1", "should raise realized value — but its return leg is unconfirmed", PART),
          ("B1", "caps realized value by limiting how generous offers can be", BMO),
          ("B2", "drains realized value by turning delay into withdrawal", LOSS)]
widths = [len(eff) * 6.6 + 30 for _, eff, _ in EFFECT]
ex = 776 - (sum(widths) - 30) / 2
for (code, eff, col), wid in zip(EFFECT, widths):
    a(f'<circle cx="{ex+11}" cy="226" r="11" fill="{col}"/>')
    a(f'<text x="{ex+11}" y="230" text-anchor="middle" font-family="{SERIF}" font-size="11" fill="#ffffff" font-weight="700">{code}</text>')
    a(f'<text x="{ex+29}" y="230" font-family="{SANS}" font-size="12.5" fill="{col}">{e(eff)}</text>')
    ex += wid

a(f'<ellipse cx="2030" cy="180" rx="470" ry="72" fill="#ffffff" stroke="{LOSS}" stroke-width="2"/>')
a(f'<line x1="1520" y1="180" x2="1552" y2="180" stroke="{LOSS}" stroke-width="2.2" marker-end="url(#ar_{LOSS[1:]})"/>')
a(f'<text x="2030" y="148" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{LOSS}" font-weight="700" letter-spacing="1.2">B2  &#183;  PROOF AND DOUBT BRAKE</text>')
B2 = [("Member activity", "+"), ("Time to confirm &#8214;", "+"), ("Member doubt", "&#8722;"), ("Participation", "+")]
B2W = [len(st.replace("&#8214;", "x")) * 6.8 + 22 for st, _ in B2]
bx = 2030 - (sum(B2W) + 3 * 19) / 2
for (st, sign), wid in zip(B2, B2W):
    a(f'<rect x="{bx}" y="164" width="{wid}" height="26" rx="13" fill="{CANV}" stroke="{LOSS}" stroke-width="1.1"/>')
    a(f'<text x="{bx+wid/2}" y="182" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{INK}">{st}</text>')
    bx += wid + 5
    if st != B2[-1][0]:
        a(f'<text x="{bx}" y="184" font-family="{SERIF}" font-size="14.5" fill="{LOSS}" font-weight="700">{sign}</text>')
        bx += 14
a(f'<text x="2030" y="210" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">One minus and a delay. The lag before a member can confirm that a purchase</text>')
a(f'<text x="2030" y="227" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">counted, or that a missing reward is being handled, is what manufactures doubt.</text>')

# ── outside the boundary ─────────────────────────────────────────────────
band(36, 268, W - 72, 76, "Outside the boundary", None, CTX)
OUT = [("Regulation and privacy", "privacy law, consent rules, suitability, disclosure"),
       ("Competitor programmes", "PC Optimum, Scene, bank and card ecosystems"),
       ("Member expectations", "formed by every other app they use, and not always realistic"),
       ("Technology landscape", "AI, identity, interoperability, data portability")]
for i, (t, sb) in enumerate(OUT):
    chip(330 + i * 558, 276, 520, 60, [t], CTX, fill=CANV, size=14, sub=sb)

# ── the member, far left ─────────────────────────────────────────────────
band(36, 370, 304, 400, "The member", None, MEMB)
chip(54, 422, 268, 68, ["Member"], MEMB, fill="#E6F1FB", size=15.5, sub="a member, a BMO client, or both")
chip(54, 506, 268, 92, ["Spending they already", "intend to make"], MEMB, fill=CANV, weight="400", size=13.5,
     sub="what the enhancement is built around")
a(f'<text x="188" y="638" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MEMB}" font-weight="700">&#8722;  What the member gets back:</text>')
a(f'<text x="188" y="656" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{MEMB}" font-weight="700">fewer steps, less uncertainty</text>')
a(f'<text x="188" y="688" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">What the programme records is what</text>')
a(f'<text x="188" y="704" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">a member did inside it, not everything</text>')
a(f'<text x="188" y="720" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">they bought or wanted.</text>')

# ── relevance flywheel, between the member and the core ──────────────────
loop(428, 670, 84, 190, "R1", ["Relevance", "flywheel"], PART,
     [("Member needs, preferences and activity", "+"), ("Personalized, understandable offers", "+"),
      ("Worthwhile benefits received", "+"), ("Repeat participation", "+"),
      ("Stronger BMO banking relationships", "+")],
     "no minuses · it compounds")

# ── BMO, the programme, and the enhancement ──────────────────────────────
band(528, 370, 1184, 616, "BMO", ["Owns Blue Rewards and funds it. Emerging Business, in gold, is our client.",
                                  "Each of the other teams holds a decision we would need."], BMO, dashed=False)
BMO_TEAMS = [("Emerging Business", "our client &#183; Drew’s team", True),
             ("Programme leadership", "sets direction, funds it", False),
             ("Cards and Credit", "the banking earning routes", False),
             ("Data and Analytics", "the records and the decisioning", False),
             ("Finance and risk", "carries the cost of points held", False)]
for i, (t, sb, client) in enumerate(BMO_TEAMS):
    x = 546 + i * 228
    col = GOLD if client else BMO
    a(f'<rect x="{x}" y="446" width="220" height="54" rx="10" fill="{"#FAEEDA" if client else "#EEEDFE"}" stroke="{col}" stroke-width="{2 if client else 1.4}"/>')
    a(f'<text x="{x+110}" y="469" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{"#854F0B" if client else BMO}" font-weight="700">{e(t)}</text>')
    a(f'<text x="{x+110}" y="488" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">{sb}</text>')

band(546, 512, 1148, 452, "Blue Rewards programme today",
     ["The loyalty programme itself: the offers, the points, the catalogue, and the people who resolve cases.",
      "We would read from these services and write back to them. We would not replace any of them."], PART, dashed=False)
for i, t in enumerate(["Offer service", "Points and transactions", "Catalogue and travel", "Support and cases"]):
    chip(564 + i * 282, 586, 260, 46, [t], PART, fill="#E1F5EE", size=13)

a(f'<rect x="564" y="658" width="1112" height="292" rx="14" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/>')
a(f'<text x="1120" y="692" text-anchor="middle" font-family="{SERIF}" font-size="16" fill="{GOLD}" font-weight="700" letter-spacing="1.6">WHAT WE ARE PROPOSING TO BUILD</text>')
a(f'<text x="1120" y="716" text-anchor="middle" font-family="{SANS}" font-size="13.5" fill="#c9c9e0">An enhanced experience within the Blue Rewards app and website</text>')

FEATS = [("Relevant Opportunity Discovery", "Relevance", "ranked options, with the reason for the ranking"),
         ("Adaptive Value Planning", "Clarity", "a saved goal and a saved comparison"),
         ("Transparent Value Progression", "Visibility", "what has arrived, and what is still expected"),
         ("Value Protection and Recovery", "Reliability", "a case the member can follow"),
         ("Blue, the conversational assistant", "Across all four", "the same saved information, in their own words")]
for i2, (t, need, out2) in enumerate(FEATS):
    x, y = (574 + i2 * 376, 734) if i2 < 3 else (762 + (i2 - 3) * 376, 842)
    a(f'<rect x="{x}" y="{y}" width="340" height="96" rx="10" fill="#1b1e55" stroke="{GOLD}" stroke-width="1.2"/>')
    a(f'<text x="{x+170}" y="{y+30}" text-anchor="middle" font-family="{SANS}" font-size="14" fill="#ffffff" font-weight="700">{e(t)}</text>')
    a(f'<text x="{x+170}" y="{y+56}" text-anchor="middle" font-family="{SERIF}" font-size="12" fill="{GOLD}" letter-spacing="1.4">{e(need.upper())}</text>')
    a(f'<text x="{x+170}" y="{y+78}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="#9a9ab8">{e(out2)}</text>')

# ── liability brake, between the core and the proof-holders ──────────────
loop(1806, 670, 86, 190, "B1", ["Liability", "brake"], BMO,
     [("Points issued", "+"), ("Outstanding liability", "+"), ("Cost carried by Finance", "&#8722;"),
      ("Offer generosity", "+")],
     "one minus · it pushes back")

# ── who holds the proof, far right ───────────────────────────────────────
band(1908, 370, 616, 540, "Evidence authorities",
     ["No single party sees a whole journey, so when value goes missing the evidence is",
      "split between them. Each sends what it has on its own schedule, so the programme",
      "often finds out late. We would ask all five and instruct none."], PART)
AUTH = [("Offer sponsor", "writes the eligibility rules, the reward amount and the deadlines"),
        ("Merchant and point of sale", "the only party that sees what was actually in the basket"),
        ("Card issuer and network", "sees a merchant and an amount, and decides when it settles"),
        ("Affiliate and receipt processing", "ties an online click or a photographed receipt to the member"),
        ("Reward supplier and fulfilment", "ships the gift card, books the trip, decides when it arrives")]
for i, (t, sb) in enumerate(AUTH):
    chip(1926, 474 + i * 84, 580, 68, [t], PART, fill=CANV, size=14.5, sub=sb)

# ── arrows across the boundaries ─────────────────────────────────────────
arrow(324, 422, 560, 690, MEMB, "+  the member uses it", bend=(460, 410), lx=436, ly=382)
arrow(560, 930, 324, 730, MEMB, None, bend=(440, 952))
a(f'<line x1="700" y1="636" x2="700" y2="654" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="712" y="652" font-family="{SANS}" font-size="12.5" fill="{PART}" font-weight="700">+  reads records</text>')
a(f'<line x1="1456" y1="654" x2="1456" y2="636" stroke="{PART}" stroke-width="2.2" marker-end="url(#ar_{PART[1:]})"/>')
a(f'<text x="1468" y="652" font-family="{SANS}" font-size="12.5" fill="{PART}" font-weight="700">+  writes goals and cases</text>')
arrow(1906, 544, 1682, 570, PART, "‖  delay — they report on their own timeline", dashed=True, bend=(1800, 426), lx=1620, ly=358)
arrow(1676, 930, 1906, 866, PART, "+  we send each case to them", dashed=True, bend=(1800, 948), lx=1806, ly=920)

# ── where the five leverage points act ───────────────────────────────────
badge(1700, 570, "1")
badge(1654, 736, "2")
badge(1090, 844, "3")
badge(902, 736, "4")
badge(352, 582, "5")

# ── what the system above would do to the people downstream of it ────────
a(f'<line x1="1120" y1="990" x2="1120" y2="1018" stroke="{NAVY}" stroke-width="3.2" marker-end="url(#ar_{NAVY[1:]})"/>')
a(f'<rect x="36" y="1024" width="{W-72}" height="104" rx="14" fill="#F1EFE8" stroke="{MUTE}" stroke-width="1.4"/>')
a(f'<text x="56" y="1052" font-family="{SERIF}" font-size="15" fill="{NAVY}" font-weight="700" letter-spacing="1.4">DOWNSTREAM STAKEHOLDERS</text>')
a(f'<text x="372" y="1052" font-family="{SANS}" font-size="11.5" fill="{MUTE}">Who this reaches, and what it would mean for them</text>')
DOWN = [("Members", "Fewer steps and less uncertainty, and a way to see what is owed", MEMB),
        ("Finance and risk", "Recovered points reduce breakage, and liability ages differently", BMO),
        ("Support and operations", "Inquiries rise before they fall, because loss becomes visible", LOSS),
        ("Earn and redeem partners", "Ranking changes who gets seen, and who does not", PART),
        ("Cards and Credit", "More reason to hold the card, but only if the flywheel turns", BMO)]
for i, (t, sb, col) in enumerate(DOWN):
    x = 56 + i * 492
    a(f'<rect x="{x}" y="1064" width="476" height="52" rx="9" fill="#ffffff" stroke="{col}" stroke-width="1.5"/>')
    a(f'<rect x="{x}" y="1064" width="476" height="4" rx="2" fill="{col}"/>')
    a(f'<text x="{x+238}" y="1088" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{col}" font-weight="700">{e(t)}</text>')
    a(f'<text x="{x+238}" y="1106" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{INK}">{e(sb)}</text>')

# ── leverage points ──────────────────────────────────────────────────────
a(f'<rect x="36" y="1152" width="1500" height="228" rx="14" fill="#F6F1E4" stroke="{GOLD}" stroke-width="1.6"/>')
a(f'<text x="60" y="1186" font-family="{SERIF}" font-size="16" fill="{NAVY}" font-weight="700" letter-spacing="1.4">LEVERAGE POINTS</text>')
a(f'<text x="276" y="1186" font-family="{SANS}" font-size="11.5" fill="{MUTE}">Each one changes a loop above. Grouped under the three candidate leverage points in the faculty brief.</text>')
LEV = [("1", "Make realized value the goal", "Not issued value, not activity, not breakage. Changes what the scoreboard rewards, so it changes B1.", "Objectives and measurement"),
       ("2", "Connect the value states", "Make what is earned, pending, posted and used visible as one thing. Shortens the delay in B2.", "Information flows"),
       ("3", "Detect and resolve missing value", "Find at-risk value early and route it. This is the recovery capability.", "Rules and accountability"),
       ("4", "Treat consent as spendable", "Intrusion spends it, so personalization has a ceiling. Caps how hard R1 can be pushed.", "Rules and accountability"),
       ("5", "Learn from realized outcomes", "Feed what actually arrived back into relevance. This is the return leg of R1.", "Information flows")]
for i2, (n2, t, sb, fam) in enumerate(LEV):
    x, y = 58 + (i2 // 3) * 750, 1224 + (i2 % 3) * 56
    badge(x + 13, y, n2)
    a(f'<text x="{x+34}" y="{y+5}" font-family="{SANS}" font-size="13" fill="{NAVY}" font-weight="700">{e(t)}</text>')
    a(f'<text x="{x+34}" y="{y+23}" font-family="{SANS}" font-size="11.5" fill="{INK}">{e(sb)}</text>')
    a(f'<text x="{x+34}" y="{y+40}" font-family="{SERIF}" font-size="10.5" fill="#854F0B" letter-spacing="1.1">{e(fam.upper())}</text>')

# ── what this does not replace ───────────────────────────────────────────
a(f'<rect x="1560" y="1152" width="964" height="228" rx="14" fill="#FCEBEB" stroke="{LOSS}" stroke-width="1.6"/>')
a(f'<text x="1584" y="1186" font-family="{SERIF}" font-size="14" fill="{LOSS}" font-weight="700" letter-spacing="2">WHAT THIS DOES NOT REPLACE</text>')
NR = ["Existing earning methods: partner scans, linked-card offers, receipts, Shops and BMO products.",
      "Redemption fulfilment: gift cards, travel, merchandise and partner redemptions.",
      "Merchant shopping, checkout and payment.",
      "BMO and partner support where manual investigation or partner action is required.",
      "Partner issuance, redemption and reversal: those services need partner credentials, not a member session."]
for i, t in enumerate(NR):
    a(f'<text x="1584" y="{1226 + i * 34}" font-family="{SANS}" font-size="11.5" fill="#4A1B0C">&#8226;  {e(t)}</text>')

a(f'<text x="36" y="1414" font-family="{SANS}" font-size="12.5" fill="{MUTE}">Team Zig &#183; Blue Rewards capstone &#183; Figure for section 3 of the Product Requirements Document. Full interactive systems map: joannjmj48-ui.github.io/mdpm-capstone/systems-thinking-v2/</text>')

markers = "".join(
    f'<marker id="ar_{c[1:]}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
    f'<path d="M0,0 L9,3 L0,6 Z" fill="{c}"/></marker>' for c in (MEMB, BMO, PART, CTX, MUTE, GOLD, NAVY, LOSS))

inner = f'<defs>{markers}</defs>' + "".join(o)
svg_site = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
  f'aria-label="The problem leads the figure: available value does not reliably become realized value. Below it, where '
  f'the product sits in the Blue Rewards system. The product is an enhanced experience inside the existing Blue Rewards '
  f'app and website, nested within the programme systems of record, which are nested within BMO. The member is to the '
  f'left, evidence authorities to the right, and forces outside the boundary across the top. It holds none of the '
  f'records; what it changes is how much of the available value a member ends up with. Three feedback loops explain '
  f'why realized value stays lower than it could be, five leverage points act on those loops, and the system feeds '
  f'down into five downstream stakeholders.">{inner}</svg>')
svg_file = f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{inner}</svg>\n'

ROOT = pathlib.Path(__file__).resolve().parent.parent
(ROOT / "figures").mkdir(exist_ok=True)
(ROOT / "figures" / "product-in-the-system.svg").write_text(svg_file, encoding="utf-8")
(ROOT / "figures" / "_panel.svg").write_text(svg_site, encoding="utf-8")
print(f"Wrote figures/product-in-the-system.svg — {len(svg_file)} bytes — {W}x{H} ({W/H:.3f}:1)")
