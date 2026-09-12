#!/usr/bin/env python3
"""Render data/stakeholders.json into stakeholders.js — a power/interest grid
shown as its own view.

Kept separate from the systems map deliberately: it answers who can move the
system, not how the system moves.
"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "data" / "stakeholders.json").read_text(encoding="utf-8"))

def cell(q):
    people = "".join(
        '<li><span class="sh-n">' + str(s["n"]) + "</span><div><strong>" + s["name"] + "</strong>"
        + ('<em>' + s["note"] + "</em>" if s.get("note") else "") + "</div></li>"
        for s in q["stakeholders"])
    return ('<div class="sh-quad is-' + q["id"] + '">'
            '<div class="sh-quad-head"><h4>' + q["label"] + "</h4>"
            '<span>power ' + q["power"] + " &middot; interest " + q["interest"] + "</span></div>"
            '<p class="sh-guidance">' + q["guidance"] + "</p>"
            '<ol class="sh-list">' + people + "</ol></div>")

order = ["satisfied", "manage", "monitor", "informed"]
qs = {q["id"]: q for q in D["quadrants"]}
html = ('<div class="sh-wrap">'
        '<header class="sh-hero"><span class="sh-kicker">Who can move the system</span>'
        '<h3>' + D["title"] + "</h3><p>" + D["framing"] + "</p></header>"
        '<div class="sh-matrix">'
        '<div class="sh-ylabel"><span>Power &rarr;</span></div>'
        '<div class="sh-grid">' + "".join(cell(qs[k]) for k in order) + "</div>"
        '<div class="sh-xlabel"><span>Interest &rarr;</span></div>'
        "</div>"
        '<p class="sh-fine">' + str(sum(len(q["stakeholders"]) for q in D["quadrants"]))
        + " stakeholders. " + D["source"] + "</p></div>")

js = """/* GENERATED FROM data/stakeholders.json by scripts/build-stakeholders.py. */
(function () {
  "use strict";
  var root = document.querySelector("#loyalty-map-v2");
  var controls = root && root.querySelector(".viz-controls");
  if (!root || !controls) return;

  var section = document.createElement("section");
  section.id = "stakeholders-view";
  section.hidden = true;
  section.innerHTML = __HTML__;
  root.appendChild(section);

  var button = document.createElement("button");
  button.type = "button";
  button.className = "btn";
  button.textContent = "4. Stakeholders";
  button.setAttribute("data-sh-view", "stakeholders");
  button.setAttribute("aria-pressed", "false");
  var boundary = controls.querySelector('[data-map-view="external"]');
  if (boundary && boundary.nextSibling) controls.insertBefore(button, boundary.nextSibling);
  else controls.appendChild(button);

  function standard() {
    return root.querySelectorAll(":scope > .lm2-map-wrap, :scope > .lm2-legend, :scope > .lm2-detail, :scope > .lm2-guide, :scope > .lm2-instruction-row, :scope > .card, :scope > .lm2-viewnote");
  }
  function show() {
    root.querySelectorAll("[data-map-view], [data-cv-view], [data-nv-view]").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
      b.classList.remove("btn-primary");
    });
    ["#convergence-view", "#narrative-view", "#opportunity-view"].forEach(function (sel) {
      var el = root.querySelector(sel); if (el) el.hidden = true;
    });
    button.setAttribute("aria-pressed", "true");
    button.classList.add("btn-primary");
    standard().forEach(function (s) { s.hidden = true; });
    section.hidden = false;
  }
  function hide() {
    button.setAttribute("aria-pressed", "false");
    button.classList.remove("btn-primary");
    standard().forEach(function (s) { s.hidden = false; });
    section.hidden = true;
  }
  button.addEventListener("click", show);
  root.querySelectorAll("[data-map-view]").forEach(function (b) { b.addEventListener("click", hide); });
  root.querySelectorAll("[data-cv-view], [data-nv-view]").forEach(function (b) {
    b.addEventListener("click", function () {
      button.setAttribute("aria-pressed", "false");
      button.classList.remove("btn-primary");
      section.hidden = true;
    });
  });
})();
"""
(ROOT / "stakeholders.js").write_text(js.replace("__HTML__", json.dumps(html)), encoding="utf-8")
print(f"wrote stakeholders.js — {sum(len(q['stakeholders']) for q in D['quadrants'])} stakeholders")
