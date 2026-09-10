#!/usr/bin/env python3
"""Render data/convergence.json into convergence.js — a self-contained view
module for the V2 site, following the V1 convention of a generated data module
rather than hand-edited markup.

The module injects its own buttons and sections and coexists with the existing
map renderer without modifying it, honouring the V2 safety contract: the four
map views and their accessibility behaviour are untouched.

Run scripts/build-convergence.py first.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "data" / "convergence.json").read_text(encoding="utf-8"))
OUT = ROOT / "convergence.js"

JS = """/* GENERATED FROM data/convergence.json by scripts/render-convergence.py.
   Do not edit directly — edit data/submissions/*.json or data/convergence-map.json,
   then re-run scripts/build-convergence.py and scripts/render-convergence.py. */
(function () {
  "use strict";

  var DATA = __DATA__;

  var root = document.querySelector("#loyalty-map-v2");
  var controls = root && root.querySelector(".viz-controls");
  if (!root || !controls) return;

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function badge(kind, label) {
    return '<span class="cv-badge is-' + kind + '">' + label + "</span>";
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function memberList(members) {
    return members.map(function (m) {
      var who = (DATA.contributors.filter(function (c) { return c.submissionId === m.submissionId; })[0] || {}).displayName || m.submissionId;
      return '<li><span class="cv-who">' + esc(who) + '</span><code>' + esc(m.itemId) + "</code><p>" + esc(m.framing) + "</p></li>";
    }).join("");
  }

  function clusterCard(c) {
    var parts = ['<article class="cv-card is-' + esc(c.strength) + '">'];
    parts.push('<header><div class="cv-card-head">' + badge(c.strength, c.strength) + '<code class="cv-id">' + esc(c.id) + "</code></div>");
    parts.push("<h4>" + esc(c.theme) + "</h4></header>");
    parts.push('<ul class="cv-members">' + memberList(c.members) + "</ul>");
    if (c.whatConverged) parts.push('<div class="cv-field"><span>What lines up</span><p>' + esc(c.whatConverged) + "</p></div>");
    if (c.whatDiffers) parts.push('<div class="cv-field is-differs"><span>What differs</span><p>' + esc(c.whatDiffers) + "</p></div>");
    if (c.whyItMatters) parts.push('<div class="cv-field"><span>Why it matters</span><p>' + esc(c.whyItMatters) + "</p></div>");
    var tags = [];
    if (c.epistemicStatus) tags.push(esc(c.epistemicStatus));
    if (c.claimBasis) tags.push(esc(c.claimBasis).replace(/-/g, " "));
    if (c.decisionStatus) tags.push(esc(c.decisionStatus).replace(/-/g, " "));
    parts.push('<footer class="cv-classifiers">' + tags.map(function (t) { return "<span>" + t + "</span>"; }).join("") + "</footer>");
    parts.push("</article>");
    return parts.join("");
  }

  function divergenceCard(d) {
    var parts = ['<article class="cv-card cv-divergence is-' + esc(d.severity) + '">'];
    parts.push('<header><div class="cv-card-head">' + badge(d.severity, d.severity) + '<code class="cv-id">' + esc(d.id) + "</code>");
    if (d.blocksMerge) parts.push('<span class="cv-flag">blocks structural merge</span>');
    parts.push("</div><h4>" + esc(d.title) + "</h4></header>");
    parts.push('<div class="cv-positions">' + d.positions.map(function (p) {
      var who = (DATA.contributors.filter(function (c) { return c.submissionId === p.submissionId; })[0] || {}).displayName || p.submissionId;
      return '<div><span class="cv-who">' + esc(who) + "</span><p>" + esc(p.position) + "</p></div>";
    }).join("") + "</div>");
    parts.push('<div class="cv-field"><span>Why it matters</span><p>' + esc(d.whyItMatters) + "</p></div>");
    if (d.resolutionOptions && d.resolutionOptions.length) {
      parts.push('<div class="cv-field"><span>Ways to resolve it</span><ul class="cv-options">' +
        d.resolutionOptions.map(function (o) { return "<li>" + esc(o) + "</li>"; }).join("") + "</ul></div>");
    }
    if (d.recommendedNext) parts.push('<div class="cv-field is-next"><span>Suggested next step</span><p>' + esc(d.recommendedNext) + "</p></div>");
    parts.push("</article>");
    return parts.join("");
  }

  function gapCard(g) {
    return '<article class="cv-card cv-gap"><header><div class="cv-card-head">' + badge("gap", "open gap") +
      '<code class="cv-id">' + esc(g.id) + "</code></div><h4>" + esc(g.title) + "</h4></header>" +
      "<p>" + esc(g.detail) + "</p>" +
      '<div class="cv-field is-next"><span>Ask ' + esc(g.askOf) + "</span><p>" + esc(g.ask) + "</p></div>" +
      '<footer class="cv-classifiers"><span>blocks: ' + g.blocks.map(esc).join(", ") + "</span></footer></article>";
  }

  function contributorCard(c) {
    return '<article class="cv-card cv-contributor is-' + esc(c.status) + '">' +
      '<header><div class="cv-card-head">' + badge(c.status, c.status.replace(/-/g, " ")) + "</div>" +
      "<h4>" + esc(c.displayName) + "</h4></header>" +
      '<div class="cv-field"><span>Source</span><p>' + esc(c.sourceRef) + "</p></div>" +
      '<div class="cv-field"><span>Note</span><p>' + esc(c.note) + "</p></div></article>";
  }

  var summary = DATA.convergence.summary || {};
  var section = el("section", "cv-view");
  section.id = "convergence-view";
  section.hidden = true;
  section.setAttribute("aria-labelledby", "cv-title");
  section.innerHTML =
    '<div class="cv-stack">' +
      '<header class="cv-card cv-hero">' +
        '<div><span class="cv-kicker">Cross-contributor analysis</span>' +
        '<h2 id="cv-title">Where Team Zig converges — and where it does not</h2></div>' +
        "<p>" + esc(DATA.convergence.analysisNote) + "</p>" +
        '<p class="cv-caveat"><strong>Coverage:</strong> ' + DATA.coverage.contributorsReceived +
          " contributor(s) analysed. " + esc(DATA.coverage.caveat) + "</p>" +
        '<div class="cv-tally">' +
          Object.keys(summary).map(function (k) {
            return '<div class="cv-tally-item is-' + esc(k) + '"><strong>' + summary[k] + "</strong><span>" + esc(k) + "</span></div>";
          }).join("") +
          '<div class="cv-tally-item is-material"><strong>' + DATA.divergences.length + "</strong><span>divergences</span></div>" +
          '<div class="cv-tally-item is-gap"><strong>' + DATA.gaps.length + "</strong><span>open gaps</span></div>" +
        "</div>" +
      "</header>" +
      '<div class="cv-subnav" role="group" aria-label="Choose a convergence view">' +
        '<button type="button" class="btn btn-primary" data-cv-panel="converge" aria-pressed="true">Convergence</button>' +
        '<button type="button" class="btn" data-cv-panel="diverge" aria-pressed="false">Divergence</button>' +
        '<button type="button" class="btn" data-cv-panel="gaps" aria-pressed="false">Open gaps</button>' +
        '<button type="button" class="btn" data-cv-panel="who" aria-pressed="false">Contributors</button>' +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="converge">' +
        "<h3>Leverage points</h3>" +
        '<div class="cv-grid">' + DATA.convergence.leverage.map(clusterCard).join("") + "</div>" +
        "<h3>Product definition</h3>" +
        '<div class="cv-grid">' + DATA.convergence.product.map(clusterCard).join("") + "</div>" +
        '<p class="cv-fine">Convergence strength describes how independently contributors arrived at the same claim. It never upgrades epistemic status: ' +
        esc(DATA.classificationRule) + "</p>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="diverge" hidden>' +
        '<div class="cv-grid">' + DATA.divergences.map(divergenceCard).join("") + "</div>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="gaps" hidden>' +
        '<div class="cv-grid">' + DATA.gaps.map(gapCard).join("") + "</div>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="who" hidden>' +
        '<div class="cv-grid">' + DATA.contributors.map(contributorCard).join("") + "</div>" +
      "</div>" +
    "</div>";

  root.appendChild(section);

  var button = el("button", "btn", "Team Convergence");
  button.type = "button";
  button.setAttribute("data-cv-view", "convergence");
  button.setAttribute("aria-pressed", "false");
  controls.appendChild(button);

  function standardSections() {
    return root.querySelectorAll(":scope > .lm2-map-wrap, :scope > .lm2-legend, :scope > .lm2-detail, :scope > .lm2-guide, :scope > .lm2-instruction-row");
  }

  function showConvergence() {
    root.querySelectorAll("[data-map-view]").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
      b.classList.remove("btn-primary");
    });
    button.setAttribute("aria-pressed", "true");
    button.classList.add("btn-primary");
    standardSections().forEach(function (s) { s.hidden = true; });
    section.hidden = false;
  }

  function hideConvergence() {
    button.setAttribute("aria-pressed", "false");
    button.classList.remove("btn-primary");
    standardSections().forEach(function (s) { s.hidden = false; });
    section.hidden = true;
  }

  button.addEventListener("click", showConvergence);
  root.querySelectorAll("[data-map-view]").forEach(function (b) {
    b.addEventListener("click", hideConvergence);
  });

  section.querySelectorAll("[data-cv-panel]").forEach(function (tab) {
    tab.addEventListener("click", function () {
      var name = tab.getAttribute("data-cv-panel");
      section.querySelectorAll("[data-cv-panel]").forEach(function (t) {
        var active = t === tab;
        t.setAttribute("aria-pressed", String(active));
        t.classList.toggle("btn-primary", active);
      });
      section.querySelectorAll("[data-cv-panel-body]").forEach(function (p) {
        p.hidden = p.getAttribute("data-cv-panel-body") !== name;
      });
    });
  });
})();
"""

OUT.write_text(JS.replace("__DATA__", json.dumps(DATA, ensure_ascii=False)), encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")
