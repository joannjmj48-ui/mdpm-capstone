#!/usr/bin/env python3
"""Build extension.js — tab 2, the extension to the systems map.

Drawn in the format Joann used for MMIE 884: main variable in the centre,
every link signed, delays double-barred, feedback loops marked and named.
Muted grey is the structure the team's map already has; colour is what the
November evidence adds. Hand-positioned SVG, not Sly's grid renderer.
"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1720, 1120

INK   = "#2b2b33"
CANV  = "#fbfaf6"
NAVY  = "#10123f"
GOLD  = "#C79A3B"
MUTE  = "#8a8a92"
MEMB  = "#185FA5"
BMO   = "#534AB7"
PART  = "#0F6E56"
LOSS  = "#A32D2D"
SANS  = "Helvetica,Arial,sans-serif"
SERIF = "Georgia,serif"

out = []
def a(s): out.append(s)
def esc(s): return html.escape(str(s), quote=False)

# ───────────────────────────── boxes ──────────────────────────────
BOX = {}
def box(key, cx, cy, w, h, lines, colour, kind="new", sub=None):
    """kind: existing (muted outline) | new (coloured) | centre (navy)."""
    BOX[key] = {"cx": cx, "cy": cy, "w": w, "h": h}
    x, y = cx - w / 2, cy - h / 2
    if kind == "centre":
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{NAVY}" stroke="{GOLD}" stroke-width="2.5"/>')
        a(f'<text x="{cx}" y="{y+30}" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{GOLD}" font-weight="700" letter-spacing="1.5">THE MAIN VARIABLE</text>')
        for i, ln in enumerate(lines):
            a(f'<text x="{cx}" y="{y+60+i*24}" text-anchor="middle" font-family="{SANS}" font-size="16" fill="#ffffff" font-weight="700">{esc(ln)}</text>')
        return
    fill = CANV if kind == "existing" else "#ffffff"
    dash = ' stroke-dasharray="5 4"' if kind == "existing" else ""
    sw = 1.4 if kind == "existing" else 2.2
    a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{colour}" stroke-width="{sw}"{dash}/>')
    n = len(lines)
    top = cy - (n - 1) * 9 + (0 if not sub else -8)
    for i, ln in enumerate(lines):
        weight = "700" if kind == "new" else "400"
        a(f'<text x="{cx}" y="{top+i*18+5}" text-anchor="middle" font-family="{SANS}" font-size="13.5" fill="{colour if kind=="new" else MUTE}" font-weight="{weight}">{esc(ln)}</text>')
    if sub:
        a(f'<text x="{cx}" y="{cy+h/2-11}" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{MUTE}">{esc(sub)}</text>')

# ───────────────────────────── links ──────────────────────────────
def link(p1, p2, sign, label, colour, kind="new", delay=False, bend=None, lx=None, ly=None):
    x1, y1 = p1; x2, y2 = p2
    sw = 1.6 if kind == "existing" else 2.4
    op = "0.55" if kind == "existing" else "0.95"
    marker = "arwmute" if kind == "existing" else ("arwloss" if colour == LOSS else
             "arwmemb" if colour == MEMB else "arwbmo" if colour == BMO else
             "arwpart" if colour == PART else "arwmute")
    if bend:
        d = f'M{x1},{y1} Q{bend[0]},{bend[1]} {x2},{y2}'
        mx = 0.25 * x1 + 0.5 * bend[0] + 0.25 * x2
        my = 0.25 * y1 + 0.5 * bend[1] + 0.25 * y2
    else:
        d = f'M{x1},{y1} L{x2},{y2}'
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    a(f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="{sw}" opacity="{op}" marker-end="url(#{marker})"/>')
    if delay:
        import math
        ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
        a(f'<g transform="translate({mx},{my}) rotate({ang})">'
          f'<line x1="-4" y1="-9" x2="-4" y2="9" stroke="{colour}" stroke-width="2.4"/>'
          f'<line x1="4" y1="-9" x2="4" y2="9" stroke="{colour}" stroke-width="2.4"/></g>')
    tx = lx if lx is not None else mx
    ty = ly if ly is not None else my - 16
    wpx = len(label) * 6.1 + 34
    a(f'<rect x="{tx-wpx/2}" y="{ty-11}" width="{wpx}" height="22" rx="11" fill="{CANV}" stroke="{colour}" stroke-width="1" opacity="0.98"/>')
    a(f'<text x="{tx-wpx/2+13}" y="{ty+5}" font-family="{SERIF}" font-size="15" fill="{colour}" font-weight="700">{sign}</text>')
    a(f'<text x="{tx+8}" y="{ty+4}" text-anchor="middle" font-family="{SANS}" font-size="11.5" fill="{colour}" font-weight="700">{esc(label)}</text>')

def loop_badge(cx, cy, code, name, colour, kind="new"):
    r = 22
    fill = colour if kind == "new" else CANV
    txt = "#ffffff" if kind == "new" else MUTE
    a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{colour}" stroke-width="2"/>')
    a(f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="{SERIF}" font-size="14" fill="{txt}" font-weight="700">{code}</text>')
    a(f'<text x="{cx}" y="{cy+r+17}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{colour}" font-weight="700">{esc(name)}</text>')

# ═════════════════ consequence analysis of our own product ═════════════════
CAPS = [
 {"name":"Relevant Opportunity Discovery", "need":"Relevance", "step":"Explore · Decide",
  "acts":"TR1 relevance flywheel, at decisioning into worthwhile value",
  "intended":"Members find worthwhile opportunities with less search effort.",
  "behaviour":"Members stop browsing the catalogue and start trusting the ranking. Browsing breadth falls, and what is not ranked is effectively not offered.",
  "incentives":"Ranking is already a commercial allocation mechanism — the register notes an existing ordering called collectorrelevance whose inputs are undocumented for this project. What changes is that ours would be visible and explainable, so a partner not surfaced can ask why. The team already holds assumption O12: a control is needed to stop partner payments or BMO product economics overriding the member\u2019s stated objective in ranking. Nobody owns that control today.",
  "relationships":"Partner managers, Finance and risk, and whoever ends up owning ranking policy — which is nobody today.",
  "enables":"The offer service already exposes targeting states, dates and sponsor information. Member preferences and saved goals give the ranker something to rank against.",
  "undermines":"Narrow ranking starves the long tail of partners, which weakens partner coverage — the flywheel eating its own supply side. And Ask Blue accepted a goal the catalogue cannot satisfy in testing; an unbounded ranker surfaces things the programme cannot deliver.",
  "watch":"Share of redemptions concentrated in the top-ranked partners, and churn among partners in the tail.",
  "m3":"Who approves the candidate offer set (BR3 says offer and partner owners retain that authority), who owns the commercial-bias control in O12, and how is a breach investigated?"},

 {"name":"Adaptive Value Planning", "need":"Clarity", "step":"Decide",
  "acts":"Worthwhile value — the stage where seven of fourteen tested issues landed",
  "intended":"Members choose a path toward an intended outcome with less uncertainty.",
  "behaviour":"A goal creates commitment, and commitment defers redemption. A member saving toward a reward is a member choosing not to redeem now.",
  "incentives":"Deferred redemption increases outstanding points liability, which runs directly against programme economics. Finance has a stake in a feature the team currently treats as pure UX.",
  "relationships":"Finance and risk become a stakeholder in an interface decision. Catalogue pricing owners too, because a goal is a promise against a price that can move.",
  "enables":"The points balance, catalogue pricing and the progress tracking participants rated easiest in the study.",
  "undermines":"Your own UH8 says goals must not pressure members to spend more to reach a reward sooner. A goal that accelerates spending is the money's-worth engine — the same reinforcing structure that drives over-ordering in an all-you-can-eat restaurant, reappearing inside a loyalty product.",
  "watch":"Spend per member before and after goal creation, and the ageing of outstanding liability.",
  "m3":"What happens when a reward's points price changes under an active goal? One participant asked this unprompted and we have no answer."},

 {"name":"Transparent Value Progression", "need":"Visibility", "step":"Earn or redeem · Follow progress",
  "acts":"Earned to Available to Realized, across the four clocks",
  "intended":"Members understand requirements and follow actions through to receipt.",
  "behaviour":"Visibility creates expectation. An expected posting date turns a vague wait into a promise the member will hold the programme to.",
  "incentives":"Support demand rises before it falls. Making overdue value visible surfaces losses the programme currently absorbs in silence. This is the least obvious consequence in the product and the one most likely to be read as the feature failing.",
  "relationships":"Service capacity planning, and partner reporting schedules the product does not control.",
  "enables":"Transaction history carries posting dates and sponsor references for the routes it covers.",
  "undermines":"A date we cannot stand behind manufactures distrust. Visibility without accuracy strengthens the doubt brake rather than weakening it — the member now has a specific broken promise instead of a vague absence.",
  "watch":"Inquiries per thousand members, and whether the rate falls after two quarters rather than settling higher.",
  "m3":"Which earning routes can produce an expected date we would defend? D9 says Blue Rewards cannot always distinguish still within the posting period from overdue without manual interpretation, so for some routes the answer today is none."},

 {"name":"Value Protection and Recovery", "need":"Reliability", "step":"Receive and use",
  "acts":"TB4 recovery brake — the loop this product exists to close",
  "intended":"Members identify missing, delayed and at-risk value early, with resolution support.",
  "behaviour":"Members stop absorbing losses quietly and start escalating them. Loss that was invisible becomes measured.",
  "incentives":"Recovered points are a direct cost: every restoration reduces breakage revenue. The programme has to agree to this product succeeding, which is a sentence worth saying out loud to the client.",
  "relationships":"The hardest coordination problem in the product. Five parties can hold the deciding evidence, and routing a case to whichever one is responsible means service expectations with organizations BMO does not control.",
  "enables":"The pre-filled inquiry tested well — participants valued not having to gather the information again. D28 says support employees currently assemble that history from more than one system by hand, so the work is real and already being done, just not by the product.",
  "undermines":"A recovery flow with no authority behind it relocates frustration from where are my points to where is my case. The study's one Critical finding was a submission that never registered. And D27 sets a hard limit: partner issuance, redemption and reversal services cannot be called under a member's own session, because they need credentials issued to approved partner systems. The product can prepare and route a case. It cannot fix one.",
  "watch":"Resolution rate and time by responsible party, and the share of members who file a second inquiry about the same loss.",
  "m3":"Who owns the case when the fault sits with a partner, and what service expectation can be agreed with parties outside BMO?"},

 {"name":"Getting in at all", "need":"Upstream of all four", "step":"Before Explore",
  "acts":"A gate in front of Opportunity. Not currently drawn on the map as a condition of its own.",
  "intended":"Nothing \u2014 this is not one of our capabilities. It is what the operational data says members actually call about.",
  "behaviour":"Of answered calls in Q4 2026, 31.3 per cent were email and password inquiries and 7.0 per cent website navigation: 38.3 per cent on access and getting around. Reward inquiries and eGift cards together were 14.6 per cent. Email and password contacts are 2.5 times their Q2 level, navigation 4.0 times.",
  "incentives":"Every capability in this product sits behind a login. A member who cannot get in generates a support contact and realizes nothing, and none of our four capabilities can influence that.",
  "relationships":"Identity and authentication own the largest and fastest growing driver, and are not currently a stakeholder in this work.",
  "enables":"Nothing in our scope. Assumptions D25 and D26 name the mechanism: separate authenticated sessions across app, web and partner surfaces, and handoffs that lose the originating offer or task.",
  "undermines":"Scoping only the reward journey addresses roughly fifteen per cent of what members contact support about while the other thirty-eight per cent grows. That is a materiality problem for the business case and the first thing a sceptical reviewer will raise.",
  "watch":"Whether email, password and navigation contacts keep rising, and what share of members never reach the reward journey at all.",
  "m3":"Does access friction gate the value this product can realize, and should the scope say so explicitly rather than leave it unaddressed?"},
 {"name":"Conversational assistance — Blue", "need":"Across all four", "step":"Every step",
  "acts":"The information layer, at every stage",
  "intended":"Members explain priorities in their own words and get help completing supported tasks.",
  "behaviour":"Members delegate judgement. Where a screen makes a member read and decide, an assistant invites them to accept an answer.",
  "incentives":"Operating cost per interaction has to be set against value recovered. The vision deck already commits to assessing whether the improvement justifies building, running and maintaining it.",
  "relationships":"Approved AI governance, the security requirements S5 to S7b, and member confirmation under FR18.",
  "enables":"Task routing to conventional software for anything calculable, with the model used only where language is the hard part.",
  "undermines":"Testing showed Ask Blue accepting an unsupported goal and asking irrelevant follow-ups. An assistant that speaks confidently about a system this conditional transfers the complexity into a confident voice, which is worse than a confusing screen because it is harder to doubt.",
  "watch":"Eligibility claims that turn out to be wrong, and the share of conversations ending in escalation rather than a completed task.",
  "m3":"Which actions are bounded and reversible enough to let an assistant take them, and what does it refuse to answer?"},
]

CROSS = [
 {"t":"The engine's return leg is unconfirmed",
  "p":"Every capability here assumes realized value changes what a member does next, and nothing can currently prove it. Two participants said progress tracking would not influence their decisions. Worse, the assumption register says no single record links a recommendation to later activation, qualification, posting and redemption (D23), the funnel is not reported end to end for every route (K2), and incremental activity cannot be separated from activity that would have happened anyway (K4). The return leg is not unproven; it is unmeasurable. Instrumenting it is cheaper than building on it."},
 {"t":"Members already give up, and nobody counts it",
  "p":"Across Q2 to Q4 2026, 92,706 contacts were abandoned before anyone answered \u2014 22,006 in Q4, still 22 per cent of calls offered. Those members had a problem and stopped trying. They leave no case record, so the loss sits outside every measure the programme has. This is the doubt brake, already running at a scale the team can quote."},
 {"t":"Succeeding costs the programme money",
  "p":"Recovery restores points that would otherwise expire unclaimed, and planning defers redemptions that would otherwise lapse. Both reduce breakage. The business case has to carry that as a cost of the product working, not treat it as an edge case."},
 {"t":"Visibility raises support load before it lowers it",
  "p":"Surfacing overdue value converts silent loss into filed cases. There is now a baseline to forecast against: in Q4 2026 reward inquiries were 8.7 per cent of answered calls, about 6,600 contacts and 1,550 agent-hours at a fourteen-minute handle time. If the product works, that number rises before it falls. Without the forecast, the first quarter of data will read as the product creating problems rather than revealing them."},
]

SEQ = ("The team already agreed a sequence in September: make it true, make it safe, make it relevant, make it wider. "
 "This analysis argues the same order from the other direction. Transparent Value Progression and Value Protection "
 "have to land before Relevant Opportunity Discovery, because ranking only works if members believe what they are "
 "shown will actually arrive. Leading with discovery amplifies a flywheel whose return leg is contested, on top of a "
 "delivery path members do not yet trust.")

# ═════════════════════════ canvas and masthead ═════════════════════
a(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{CANV}"/>')
a(f'<rect x="0" y="0" width="{W}" height="96" fill="{NAVY}"/>')
a(f'<rect x="0" y="96" width="{W}" height="4" fill="{GOLD}"/>')
a(f'<text x="40" y="45" font-family="{SERIF}" font-size="15" fill="{GOLD}" letter-spacing="3" font-weight="700">SYSTEMS MAP  ·  EXTENSION  ·  NOVEMBER 2026</text>')
a(f'<text x="40" y="78" font-family="{SERIF}" font-size="27" fill="#ffffff" font-weight="700">What the evidence adds to the map</text>')
a(f'<text x="{W-40}" y="52" text-anchor="end" font-family="{SANS}" font-size="13" fill="#c9c9e0">Team Zig  ·  Product Enablement Lead</text>')
a(f'<text x="{W-40}" y="74" text-anchor="end" font-family="{SANS}" font-size="13" fill="#c9c9e0">Extends the map, does not replace it</text>')

# legend strip
leg = [(MUTE, "Already in the map"), (LOSS, "Where value is lost"),
       (BMO, "What the product adds"), (MEMB, "Member response"), (PART, "Partner and evidence side")]
x = 44
for col, lab in leg:
    a(f'<circle cx="{x}" cy="128" r="7" fill="{col}"/>')
    a(f'<text x="{x+14}" y="133" font-family="{SANS}" font-size="12.5" fill="{INK}">{esc(lab)}</text>')
    x += len(lab) * 7.1 + 50
a(f'<text x="{W-40}" y="133" text-anchor="end" font-family="{SANS}" font-size="12" fill="{MUTE}">'
  f'+ same direction  ·  &#8722; opposite direction  ·  &#8214; significant delay  ·  R reinforcing, B balancing</text>')

# ═════════════════════════ the existing engine ═════════════════════
box("rv", 880, 470, 400, 132, ["Realized value — the value members", "actually obtain and can use"], NAVY, "centre")
box("se", 1330, 672, 250, 70, ["Sustained", "engagement"], MUTE, "existing")
box("ps", 1545, 470, 250, 70, ["Permissioned", "signal richness"], MUTE, "existing")
box("dr", 1330, 268, 250, 70, ["Decisioning", "relevance"], MUTE, "existing")

link((1010, 520), (1240, 650), "+", "more value, more reason to stay", MUTE, "existing", ly=600)
link((1420, 650), (1510, 540), "+", "more activity, richer signal", MUTE, "existing", lx=1560, ly=612)
link((1545, 435), (1400, 310), "+", "better signal, better targeting", MUTE, "existing", lx=1560, ly=345)
link((1240, 290), (1010, 420), "+", "relevance converts into value", MUTE, "existing", ly=330)
loop_badge(1420, 470, "TR1", "Relevance flywheel", MUTE, "existing")

# ═════════════════════════ what November adds ══════════════════════
box("rev", 200, 212, 330, 76, ["Reversals and clawbacks"], PART, sub="returned purchases, failed attribution")
box("una", 580, 212, 300, 76, ["Unactivated offers"], MEMB, sub="saved, never opted in")
box("evi", 940, 212, 330, 76, ["Evidence split across authorities"], PART, sub="five authorities, one member")

box("loss", 420, 470, 330, 84, ["Unresolved loss"], LOSS, sub="value that left and did not come back")
box("rec", 420, 772, 330, 84, ["Recovery capability"], BMO, sub="diagnose · route · restore")
box("doubt", 1060, 900, 300, 76, ["Member doubt"], MEMB, sub="is this programme worth it")

link((285, 250), (360, 428), "+", "posted value removed later", PART, delay=True, lx=210, ly=350)
link((580, 250), (500, 428), "+", "qualifying activity that never counted", MEMB, lx=700, ly=330)
link((880, 250), (585, 440), "+", "no single party can prove what happened", PART, lx=880, ly=390)

link((680, 470), (585, 470), "+", "more value moving, more that can fail", LOSS, lx=700, ly=545)
link((380, 512), (380, 730), "+", "loss triggers the product", BMO, lx=215, ly=600)
link((460, 730), (460, 512), "&#8722;", "found, routed, restored", BMO, delay=True, lx=640, ly=640)
loop_badge(770, 700, "TB4", "Recovery brake  ·  new", BMO)

link((520, 508), (910, 884), "+", "unexplained loss reads as the system failing", LOSS, bend=(700, 790), lx=700, ly=880)
link((1210, 884), (1310, 710), "&#8722;", "doubt withdraws participation", MEMB, lx=1255, ly=812)
loop_badge(1020, 640, "TB5", "Doubt brake  ·  new", LOSS)

a(f'<text x="770" y="762" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">one minus · balancing</text>')
a(f'<text x="1020" y="702" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">one minus · balancing</text>')
a(f'<text x="1420" y="532" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{MUTE}">no minuses · reinforcing</text>')

# ═════════════════════════ the chain, with one position added ══════
a(f'<line x1="40" y1="978" x2="{W-40}" y2="978" stroke="#ddd7c6" stroke-width="1"/>')
a(f'<text x="40" y="1012" font-family="{SERIF}" font-size="16" fill="{INK}" font-weight="700">The same five stages, with one position added</text>')
a(f'<text x="40" y="1034" font-family="{SANS}" font-size="12.5" fill="{MUTE}">The Offer Service records a member state before any</text>')
a(f'<text x="40" y="1052" font-family="{SANS}" font-size="12.5" fill="{MUTE}">earning happens. A member can weigh an offer, choose it,</text>')
a(f'<text x="40" y="1070" font-family="{SANS}" font-size="12.5" fill="{MUTE}">buy the product and still earn nothing.</text>')
chain = [("Opportunity", False), ("Potential Value", False), ("Saved or activated", True),
         ("Earned Value", False), ("Available Value", False), ("Realized Value", False)]
cx = 700
for i, (lab, isnew) in enumerate(chain):
    w = len(lab) * 7.4 + 30
    col = MEMB if isnew else MUTE
    fill = "#E6F1FB" if isnew else CANV
    sw = 2.2 if isnew else 1.2
    dash = "" if isnew else ' stroke-dasharray="5 4"'
    weight = "700" if isnew else "400"
    a(f'<rect x="{cx}" y="1012" width="{w}" height="34" rx="17" fill="{fill}" stroke="{col}" stroke-width="{sw}"{dash}/>')
    a(f'<text x="{cx+w/2}" y="1034" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{col}" font-weight="{weight}">{esc(lab)}</text>')
    cx += w + 10
    if i < len(chain) - 1:
        a(f'<path d="M{cx-8},1029 L{cx+2},1029" stroke="{MUTE}" stroke-width="1.4" marker-end="url(#arwmute)"/>')
        cx += 14

markers = "".join(
    f'<marker id="arw{n}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">'
    f'<path d="M0,0 L9,3 L0,6 Z" fill="{c}"/></marker>'
    for n, c in [("mute", MUTE), ("loss", LOSS), ("memb", MEMB), ("bmo", BMO), ("part", PART)])

svg = (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" '
       f'aria-label="Extension to the Team Zig systems map. Realized value stays the main variable at the centre. '
       f'The existing relevance flywheel TR1 is drawn muted. Two new balancing loops are added: TB4, the recovery brake, '
       f'where unresolved loss triggers recovery capability which reduces it; and TB5, the doubt brake, where realized value '
       f'creates exposure to loss, unresolved loss creates member doubt, and doubt withdraws participation. Reversals, '
       f'unactivated offers and evidence split across parties all feed unresolved loss.">'
       f'<defs>{markers}</defs>' + "".join(out) + '</svg>')

def cap_card(c):
    rows = [("Acts on", c["acts"]), ("Intended effect", c["intended"]),
            ("What it does to behaviour", c["behaviour"]),
            ("What it does to incentives", c["incentives"]),
            ("Who has to coordinate", c["relationships"]),
            ("What enables it", c["enables"]),
            ("What could undermine it", c["undermines"]),
            ("Watch for", c["watch"]),
            ("To settle in M3", c["m3"])]
    dl = "".join("<dt>" + esc(k) + "</dt><dd>" + esc(v) + "</dd>" for k, v in rows)
    return ('<article class="xt-cap"><header><div><h4>' + esc(c["name"]) + "</h4>"
            '<span class="xt-step">' + esc(c["step"]) + "</span></div>"
            '<span class="xt-need">' + esc(c["need"]) + "</span></header>"
            '<dl class="xt-dl">' + dl + "</dl></article>")

NOTES = (
 '<article class="xt-note is-new"><span class="xt-code">TB4</span><h4>Recovery brake</h4>'
 "<p><b>Unresolved loss &rarr;(+) Recovery capability &rarr;(&minus;) Unresolved loss.</b> One minus, so it balances. "
 "This loop is the product. Six requirements &mdash; FR15, FR16, FR17, FR29, FR36 and FR37 &mdash; do nothing except close it. "
 "It carries a delay because diagnosis and routing take time, and the one Critical finding in the usability study is this "
 "loop failing to start: a member believed an inquiry had been submitted when it had not.</p></article>"
 '<article class="xt-note is-new"><span class="xt-code">TB5</span><h4>Doubt brake</h4>'
 "<p><b>Realized value &rarr;(+) Unresolved loss &rarr;(+) Member doubt &rarr;(&minus;) Sustained engagement &rarr;(+) "
 "Permissioned signal &rarr;(+) Decisioning relevance &rarr;(+) Realized value.</b> One minus, so it balances &mdash; and it "
 "rides the team&rsquo;s own flywheel rather than sitting beside it. The more value moves, the more there is to go wrong; "
 "unexplained loss reads to a member as the programme not working. This is the brake nobody drew in September.</p></article>"
 '<article class="xt-note"><span class="xt-code">TR1</span><h4>Relevance flywheel, unchanged</h4>'
 "<p>Five of six contributors drew this independently and it is still the engine. Nothing here replaces it. The October "
 "study did not confirm its return leg, which is why realized value to sustained engagement is now marked Contested on "
 "the main map &mdash; and why TB5 matters: a brake on a loop that may already be weaker than we assumed.</p></article>"
 '<article class="xt-note is-lever"><span class="xt-code">&#9733;</span><h4>Where the leverage is</h4>'
 "<p>TB5 cannot be removed. Activity will always carry exposure to failure, and the structural complexity behind it "
 "&mdash; five authorities, four clocks, heterogeneous earning routes &mdash; is how the programme is built, not an accident "
 "of its interface. TB4 is the lever: it drains unresolved loss so TB5 bites less. That is the same move as adding a "
 "counteracting loop rather than fighting a frozen variable.</p></article>")

CONTEXT_SVG = (ROOT / "figures" / "_panel.svg").read_text(encoding="utf-8")

body = (
 '<div class="xt-wrap">'
 '<header class="xt-intro">'
 '<span class="xt-kicker">Tab 2 &middot; milestone 2</span>'
 "<h3>Systems Map M2</h3>"
 "<p>None of these three replaces M1. Realized value is still the main variable and the relevance flywheel the team "
 "drew in September is still the engine. <b>Systems Map 2.0</b> shows where the product sits inside all of it. "
 "<b>What the evidence adds</b> is the structure November forced that September could not hold. <b>What our product "
 "would do</b> runs our own proposal back through the system and asks what it changes about behaviour, incentives and "
 "relationships, and what could undermine the value it intends to create.</p>"
 "</header>"
 '<div class="xt-tabs" role="group" aria-label="Extension sections">'
 '<button type="button" class="btn btn-primary" data-xt-panel="where" aria-pressed="true">Systems Map 2.0</button>'
 '<button type="button" class="btn" data-xt-panel="map" aria-pressed="false">What the evidence adds</button>'
 '<button type="button" class="btn" data-xt-panel="conseq" aria-pressed="false">What our product would do to the system</button>'
 '<div class="xt-panel" data-xt-body="where">'
 '<p class="xt-how">One picture of where the product sits: nested inside the Blue Rewards systems of record, which are '
 "nested inside BMO, with the member on one side and the five parties that hold the evidence on the other. "
 "<b>We would not change what value exists. We would change how much of it a member actually ends up with</b> &mdash; "
 "by helping them find what is worth having, decide on it, follow it through, and get it back when it goes "
 "missing. That is the whole of the four capabilities, not just the understanding part. The scope boundary is "
 "on the figure rather than in a paragraph, so a reader who only looks at the picture still knows what this does not "
 "replace. This is the figure prepared for section 3 of the PRD.</p>"
 '<figure class="xt-figure"><div class="xt-scroll">' + CONTEXT_SVG + "</div>"
 '<figcaption class="xt-cap-note">Download: '
 '<a href="figures/product-in-the-system.svg" download>SVG</a> (vector, inserts into Word, Docs and PowerPoint) '
 '&middot; <a href="figures/product-in-the-system.png" download>PNG</a> 5120 &times; 2880, 16:9 for a slide.</figcaption>'
 "</figure></div>"
 '<div class="xt-panel" data-xt-body="map" hidden>'
 '<p class="xt-how">Read it the way the toolkit says. Follow an arrow, read its sign, and count the minuses round a loop: '
 "an even number compounds, an odd number pushes back. Both new loops have exactly one minus, so both are brakes. "
 "Grey is what the map already says; colour is what November adds.</p>"
 '<figure class="xt-figure"><div class="xt-scroll">' + svg + "</div></figure>"
 '<div class="xt-notes">' + NOTES + "</div></div>"
 '<div class="xt-panel" data-xt-body="conseq" hidden>'
 '<p class="xt-how">Everything else on this site describes the system as it is. This runs the four capabilities in our own '
 "product vision, and Blue, back through it. For each one: what it changes about how members behave, what it changes about "
 "what the parties around them are rewarded for, who newly has to coordinate, and what could undermine the value it intends "
 "to create. These are questions M3 feasibility has to answer, not only whether the thing can be built.</p>"
 '<div class="xt-caps">' + "".join(cap_card(c) for c in CAPS) + "</div>"
 '<h4 class="xt-crosshead">What could undermine the intended value, whatever we build</h4>'
 '<div class="xt-cross">' + "".join(
   '<article class="xt-note is-warn"><h4>' + esc(x["t"]) + "</h4><p>" + esc(x["p"]) + "</p></article>" for x in CROSS)
 + "</div>"
 '<article class="xt-note is-lever xt-seq"><span class="xt-code">&#9733;</span>'
 "<h4>What this says about sequencing</h4><p>" + esc(SEQ) + "</p></article>"
 "</div>"
"</div></div>"
)

js = ('/* GENERATED by scripts/build-extension.py. Do not edit directly. */\n'
 '(function () {\n  "use strict";\n'
 '  var root = document.querySelector("#loyalty-map-v2");\n'
 '  var controls = root && root.querySelector(".viz-controls");\n'
 '  if (!root || !controls) return;\n\n'
 '  var section = document.createElement("section");\n'
 '  section.id = "extension-view";\n'
 '  section.hidden = true;\n'
 '  section.innerHTML = ' + json.dumps(body, ensure_ascii=False) + ';\n'
 '  root.appendChild(section);\n\n'
 '  var button = document.createElement("button");\n'
 '  button.type = "button";\n  button.className = "btn";\n'
 '  button.textContent = "2. Systems Map M2";\n'
 '  button.setAttribute("data-xt-view", "extension");\n'
 '  button.setAttribute("aria-pressed", "false");\n'
 "  var first = controls.querySelector('[data-map-view=\"current\"]');\n"
 "  if (first && first.nextSibling) controls.insertBefore(button, first.nextSibling);\n"
 "  else controls.appendChild(button);\n\n"
 '  var SIBLINGS = ["#convergence-view", "#narrative-view", "#opportunity-view", "#stakeholders-view", "#evidence-view"];\n'
 '  function standard() {\n'
 '    return root.querySelectorAll(":scope > .lm2-map-wrap, :scope > .lm2-legend, :scope > .lm2-detail, :scope > .lm2-guide, :scope > .lm2-instruction-row, :scope > .card, :scope > .lm2-viewnote");\n'
 '  }\n'
 '  function show() {\n'
 '    root.querySelectorAll("[data-map-view], [data-cv-view], [data-nv-view], [data-sh-view], [data-ev-view]").forEach(function (b) {\n'
 '      b.setAttribute("aria-pressed", "false");\n      b.classList.remove("btn-primary");\n    });\n'
 '    SIBLINGS.forEach(function (sel) { var n = root.querySelector(sel); if (n) n.hidden = true; });\n'
 '    button.setAttribute("aria-pressed", "true");\n    button.classList.add("btn-primary");\n'
 '    standard().forEach(function (s) { s.hidden = true; });\n    section.hidden = false;\n  }\n'
 '  function hide() {\n'
 '    button.setAttribute("aria-pressed", "false");\n    button.classList.remove("btn-primary");\n'
 '    standard().forEach(function (s) { s.hidden = false; });\n    section.hidden = true;\n  }\n'
 '  button.addEventListener("click", show);\n'
 '  root.querySelectorAll("[data-map-view]").forEach(function (b) { b.addEventListener("click", hide); });\n'
 '  root.querySelectorAll("[data-cv-view], [data-nv-view], [data-sh-view], [data-ev-view]").forEach(function (b) {\n'
 '    b.addEventListener("click", function () {\n'
 '      button.setAttribute("aria-pressed", "false");\n      button.classList.remove("btn-primary");\n'
 '      section.hidden = true;\n    });\n  });\n'
 '  section.querySelectorAll("[data-xt-panel]").forEach(function (t) {\n'
 '    t.addEventListener("click", function () {\n'
 '      var name = t.getAttribute("data-xt-panel");\n'
 '      section.querySelectorAll("[data-xt-panel]").forEach(function (o) {\n'
 '        var on = o === t;\n'
 '        o.setAttribute("aria-pressed", String(on));\n'
 '        o.classList.toggle("btn-primary", on);\n'
 '      });\n'
 '      section.querySelectorAll("[data-xt-body]").forEach(function (b) {\n'
 '        b.hidden = b.getAttribute("data-xt-body") !== name;\n'
 '      });\n'
 '    });\n  });\n})();\n')

(ROOT / "extension.js").write_text(js, encoding="utf-8")
print("Wrote extension.js —", len(BOX), "variables,", W, "x", H)
