#!/usr/bin/env python3
"""Build evidence.js from data/evidence-map.json.

Tab 9, Evidence and Requirements. Additive: appends its own section and
button to the existing map shell without touching the map renderer.
Never hand-edit evidence.js.
"""
import json, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data" / "evidence-map.json").read_text(encoding="utf-8"))


def e(s):
    return html.escape(str(s), quote=False)


def sev_class(s):
    return {"Critical": "is-critical", "Major": "is-major", "Minor": "is-minor"}[s]


def finding_card(f):
    return (
        '<article class="ev-find ' + sev_class(f["severity"]) + '">'
        '<div class="ev-find-top"><span class="ev-sev">' + e(f["severity"]) + "</span>"
        '<span class="ev-id">' + e(f["id"]) + "</span></div>"
        "<h4>" + e(f["issue"]) + "</h4>"
        '<p class="ev-read">' + e(f["systemReading"]) + "</p>"
        '<dl class="ev-meta">'
        "<dt>Acts on</dt><dd>" + e(f["edge"]) + "</dd>"
        "<dt>Requirement</dt><dd>" + e(f["requirement"]) + "</dd>"
        "</dl></article>"
    )


def count_row(r):
    return (
        '<div class="ev-count-row"><span class="ev-count-n">' + e(r["count"]) + "</span>"
        "<div><strong>" + e(r["stage"]) + "</strong><em>" + e(r["gloss"]) + "</em></div></div>"
    )


def cluster_card(c):
    chips = "".join('<span class="ev-fr">' + e(f) + "</span>" for f in c["frs"])
    return (
        '<article class="ev-cluster">'
        '<div class="ev-cluster-top"><span class="ev-stage">' + e(c["stage"]) + "</span>"
        '<span class="ev-n">' + str(len(c["frs"])) + " requirements</span></div>"
        "<h4>" + e(c["heading"]) + "</h4>"
        '<div class="ev-frs">' + chips + "</div>"
        "<p>" + e(c["reading"]) + "</p>"
        '<dl class="ev-meta">'
        "<dt>Acts on</dt><dd>" + e(c["acts"]) + "</dd>"
        "<dt>Loop</dt><dd>" + e(c["loop"]) + "</dd>"
        "</dl></article>"
    )


def clock_row(r):
    return (
        '<div class="ev-clock"><strong>' + e(r["name"]) + "</strong>"
        "<p>" + e(r["what"]) + "</p>"
        '<span class="ev-clock-stage">' + e(r["stage"]) + "</span></div>"
    )


def gap_row(r):
    mark = "Seen in testing" if r["observed"] else "Not reached"
    cls = "is-seen" if r["observed"] else "is-untested"
    return (
        '<tr class="' + cls + '">'
        "<td>" + e(r["recorded"]) + "</td>"
        "<td>" + e(r["believed"]) + "</td>"
        "<td>" + e(r["kind"]) + "</td>"
        '<td><span class="ev-mark">' + mark + "</span><em>" + e(r["evidence"]) + "</em></td>"
        "</tr>"
    )


def changed_card(c):
    return (
        '<article class="ev-changed">'
        '<div class="ev-shift"><span class="ev-was">' + e(c["was"]) + "</span>"
        '<span class="ev-arrow">&rarr;</span>'
        '<span class="ev-now ' + ("is-down" if c["now"] == "Contested" else "is-up") + '">' + e(c["now"]) + "</span></div>"
        "<h4>" + e(c["claim"]) + "</h4>"
        "<p>" + e(c["why"]) + "</p></article>"
    )


def source_row(s):
    return (
        '<li><strong>' + e(s["label"]) + "</strong><span>" + e(s["date"]) + "</span>"
        "<em>" + e(s["detail"]) + "</em></li>"
    )


SC = D["stageCounts"]
CL = D["clocks"]
GP = D["gaps"]

body = (
    '<div class="ev-wrap">'
    '<header class="ev-hero">'
    '<span class="ev-kicker">Added for the PRD &middot; November 2026</span>'
    "<h3>What we have learned since the map was drawn</h3>"
    "<p>The map was built in September from six people&rsquo;s reasoning, before anything had been put in front of a member. "
    "Since then the team has written a requirements specification, built a prototype, tested it with six participants and "
    "commissioned an independent analysis of the programme. This page places that evidence on the map: where the tested "
    "failures sit, where each requirement acts, and which September assumptions survived contact with a user.</p>"
    '<ul class="ev-sources">' + "".join(source_row(s) for s in D["sources"]) + "</ul>"
    "</header>"

    '<div class="ev-tabs" role="group" aria-label="Evidence sections">'
    '<button type="button" class="btn btn-primary" data-ev-panel="testing" aria-pressed="true">What the testing showed</button>'
    '<button type="button" class="btn" data-ev-panel="reqs" aria-pressed="false">Where the requirements act</button>'
    '<button type="button" class="btn" data-ev-panel="clocks" aria-pressed="false">Four clocks</button>'
    '<button type="button" class="btn" data-ev-panel="gaps" aria-pressed="false">Recorded versus understood</button>'
    '<button type="button" class="btn" data-ev-panel="changed" aria-pressed="false">What changed in our confidence</button>'
    "</div>"

    '<div class="ev-panel" data-ev-body="testing">'
    '<section class="ev-counts"><h4>' + e(SC["lead"]) + "</h4>"
    "<p>" + e(SC["note"]) + "</p>"
    '<div class="ev-count-grid">' + "".join(count_row(r) for r in SC["rows"]) + "</div></section>"
    '<div class="ev-grid">' + "".join(finding_card(f) for f in D["findings"]) + "</div>"
    "</div>"

    '<div class="ev-panel" data-ev-body="reqs" hidden>'
    '<p class="ev-lead">All 42 functional requirements, grouped by the value stage they act on. '
    "Grouping them this way is what exposed the gap: one whole cluster of six had nowhere on the September map to act, "
    "which is why the Extension to the Map now draws a recovery path.</p>"
    '<div class="ev-grid">' + "".join(cluster_card(c) for c in D["requirementClusters"]) + "</div>"
    "</div>"

    '<div class="ev-panel" data-ev-body="clocks" hidden>'
    '<section class="ev-counts"><h4>' + e(CL["lead"]) + "</h4><p>" + e(CL["note"]) + "</p></section>"
    '<div class="ev-clocks">' + "".join(clock_row(r) for r in CL["rows"]) + "</div>"
    '<p class="ev-consequence">' + e(CL["consequence"]) + "</p>"
    "</div>"

    '<div class="ev-panel" data-ev-body="gaps" hidden>'
    '<section class="ev-counts"><h4>' + e(GP["lead"]) + "</h4><p>" + e(GP["note"]) + "</p></section>"
    '<div class="ev-tablewrap"><table class="ev-table">'
    "<thead><tr><th>What the system records</th><th>What the member may believe</th><th>Kind of gap</th><th>Evidence</th></tr></thead>"
    "<tbody>" + "".join(gap_row(r) for r in GP["rows"]) + "</tbody></table></div>"
    '<p class="ev-consequence">' + e(GP["closing"]) + "</p>"
    "</div>"

    '<div class="ev-panel" data-ev-body="changed" hidden>'
    '<p class="ev-lead">The map records how sure we are of each claim, and testing is the only thing that moves those ratings. '
    "Approval never did. Five claims moved &mdash; three up, two down &mdash; and the two that moved down are the ones worth "
    "the team&rsquo;s time on Monday.</p>"
    '<div class="ev-grid ev-grid-changed">' + "".join(changed_card(c) for c in D["whatChanged"]) + "</div>"
    "</div>"
    "</div>"
)

js = (
    "/* GENERATED FROM data/evidence-map.json by scripts/build-evidence.py.\n"
    "   Do not edit directly - edit the data file and re-run the script. */\n"
    '(function () {\n  "use strict";\n'
    '  var root = document.querySelector("#loyalty-map-v2");\n'
    '  var controls = root && root.querySelector(".viz-controls");\n'
    "  if (!root || !controls) return;\n\n"
    '  var section = document.createElement("section");\n'
    '  section.id = "evidence-view";\n'
    "  section.hidden = true;\n"
    "  section.innerHTML = " + json.dumps(body, ensure_ascii=False) + ";\n"
    "  root.appendChild(section);\n\n"
    '  var button = document.createElement("button");\n'
    '  button.type = "button";\n'
    '  button.className = "btn";\n'
    '  button.textContent = "10. Evidence and Requirements";\n'
    '  button.setAttribute("data-ev-view", "evidence");\n'
    '  button.setAttribute("aria-pressed", "false");\n'
    "  controls.appendChild(button);\n\n"
    "  var SIBLINGS = [\"#convergence-view\", \"#narrative-view\", \"#opportunity-view\", \"#stakeholders-view\"];\n"
    "  function standard() {\n"
    '    return root.querySelectorAll(":scope > .lm2-map-wrap, :scope > .lm2-legend, :scope > .lm2-detail, :scope > .lm2-guide, :scope > .lm2-instruction-row, :scope > .card, :scope > .lm2-viewnote");\n'
    "  }\n"
    "  function show() {\n"
    '    root.querySelectorAll("[data-map-view], [data-cv-view], [data-nv-view], [data-sh-view], [data-op-view]").forEach(function (b) {\n'
    '      b.setAttribute("aria-pressed", "false");\n'
    '      b.classList.remove("btn-primary");\n'
    "    });\n"
    "    SIBLINGS.forEach(function (sel) { var n = root.querySelector(sel); if (n) n.hidden = true; });\n"
    '    button.setAttribute("aria-pressed", "true");\n'
    '    button.classList.add("btn-primary");\n'
    "    standard().forEach(function (s) { s.hidden = true; });\n"
    "    section.hidden = false;\n"
    "  }\n"
    "  function hide() {\n"
    '    button.setAttribute("aria-pressed", "false");\n'
    '    button.classList.remove("btn-primary");\n'
    "    standard().forEach(function (s) { s.hidden = false; });\n"
    "    section.hidden = true;\n"
    "  }\n"
    "  button.addEventListener(\"click\", show);\n"
    '  root.querySelectorAll("[data-map-view]").forEach(function (b) { b.addEventListener("click", hide); });\n'
    '  root.querySelectorAll("[data-cv-view], [data-nv-view], [data-sh-view], [data-op-view]").forEach(function (b) {\n'
    "    b.addEventListener(\"click\", function () {\n"
    '      button.setAttribute("aria-pressed", "false");\n'
    '      button.classList.remove("btn-primary");\n'
    "      section.hidden = true;\n"
    "    });\n"
    "  });\n\n"
    '  section.querySelectorAll("[data-ev-panel]").forEach(function (tab) {\n'
    '    tab.addEventListener("click", function () {\n'
    '      var name = tab.getAttribute("data-ev-panel");\n'
    '      section.querySelectorAll("[data-ev-panel]").forEach(function (t) {\n'
    "        var active = t === tab;\n"
    '        t.setAttribute("aria-pressed", String(active));\n'
    '        t.classList.toggle("btn-primary", active);\n'
    "      });\n"
    '      section.querySelectorAll("[data-ev-body]").forEach(function (p) {\n'
    '        p.hidden = p.getAttribute("data-ev-body") !== name;\n'
    "      });\n"
    "    });\n"
    "  });\n"
    "})();\n"
)

(ROOT / "evidence.js").write_text(js, encoding="utf-8")
print("Wrote evidence.js —", len(D["findings"]), "findings,",
      sum(len(c["frs"]) for c in D["requirementClusters"]), "requirements,",
      len(D["gaps"]["rows"]), "gap rows,", len(D["whatChanged"]), "confidence changes.")
