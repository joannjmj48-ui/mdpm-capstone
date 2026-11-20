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
box("evi", 940, 212, 330, 76, ["Evidence split across parties"], PART, sub="five authorities, one member")

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

body = (
 '<div class="xt-wrap">'
 '<header class="xt-intro">'
 '<span class="xt-kicker">Tab 2 &middot; extension</span>'
 '<h3>What the evidence adds to the map</h3>'
 '<p>This is not a second map. Realized value is still the main variable, and the relevance flywheel the team drew in '
 'September is still the engine &mdash; both are drawn here in grey, unchanged. What is in colour is what the November '
 'evidence adds and the September structure could not hold: a place for value to go when it leaves, a mechanism for '
 'getting it back, and the member&rsquo;s response when it does not come back.</p>'
 '<p class="xt-how">Read it the way the toolkit says. Follow an arrow, read its sign, and count the minuses round a loop: '
 'an even number compounds, an odd number pushes back. Both new loops have exactly one minus, so both are brakes.</p>'
 "</header>"
 '<figure class="xt-figure"><div class="xt-scroll">' + svg + "</div></figure>"
 '<div class="xt-notes">'
 '<article class="xt-note is-new"><span class="xt-code">TB4</span><h4>Recovery brake</h4>'
 '<p><b>Unresolved loss &rarr;(+) Recovery capability &rarr;(&minus;) Unresolved loss.</b> One minus, so it balances. '
 'This loop is the product. Six requirements &mdash; FR15, FR16, FR17, FR29, FR36 and FR37 &mdash; do nothing except close it. '
 'It carries a delay because diagnosis and routing take time, and the one Critical finding in the usability study is this '
 'loop failing to start: a member believed an inquiry had been submitted when it had not.</p></article>'
 '<article class="xt-note is-new"><span class="xt-code">TB5</span><h4>Doubt brake</h4>'
 '<p><b>Realized value &rarr;(+) Unresolved loss &rarr;(+) Member doubt &rarr;(&minus;) Sustained engagement &rarr;(+) '
 'Permissioned signal &rarr;(+) Decisioning relevance &rarr;(+) Realized value.</b> One minus, so it balances &mdash; and it '
 'rides the team&rsquo;s own flywheel rather than sitting beside it. The more value moves, the more there is to go wrong; '
 'unexplained loss reads to a member as the programme not working. This is the brake nobody drew in September.</p></article>'
 '<article class="xt-note"><span class="xt-code">TR1</span><h4>Relevance flywheel, unchanged</h4>'
 '<p>Five of six contributors drew this independently and it is still the engine. Nothing here replaces it. The October '
 'study did not confirm its return leg, which is why realized value to sustained engagement is now marked Contested on '
 'the main map &mdash; and why TB5 matters: a brake on a loop that may already be weaker than we assumed.</p></article>'
 '<article class="xt-note is-lever"><span class="xt-code">&#9733;</span><h4>Where the leverage is</h4>'
 '<p>TB5 cannot be removed. Activity will always carry exposure to failure, and the flat structural complexity behind it '
 '&mdash; five authorities, four clocks, heterogeneous earning routes &mdash; is how the programme is built, not an accident '
 'of its interface. TB4 is the lever: it drains unresolved loss so TB5 bites less. That is the same move as adding a '
 'counteracting loop rather than fighting a frozen variable.</p></article>'
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
 '  button.textContent = "2. Extension to the Map";\n'
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
 '      section.hidden = true;\n    });\n  });\n})();\n')

(ROOT / "extension.js").write_text(js, encoding="utf-8")
print("Wrote extension.js —", len(BOX), "variables,", W, "x", H)
