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

  function nameOf(m) {
    var id = m.contributor || m.submissionId;
    var byId = DATA.contributors.filter(function (c) { return c.id === id; })[0];
    var bySub = DATA.contributors.filter(function (c) { return c.submissionId === id; })[0];
    return (byId || bySub || {}).displayName || id;
  }

  function memberList(members) {
    return members.map(function (m) {
      return '<li><span class="cv-who">' + esc(nameOf(m)) + '</span><code>' + esc(m.itemId) + "</code><p>" +
        esc(m.framing) + "</p>" + (m.source ? '<span class="cv-src">' + esc(m.source) + "</span>" : "") + "</li>";
    }).join("");
  }

  // ---- full-ring loop diagram -------------------------------------------
  function wrap(label, per) {
    var words = String(label).split(" "), lines = [""];
    words.forEach(function (w) {
      var i = lines.length - 1;
      if ((lines[i] + " " + w).trim().length > per) lines.push(w);
      else lines[i] = (lines[i] + " " + w).trim();
    });
    return lines.slice(0, 2);
  }

  function loopSvg(chain, negPairs, small, markLeverage) {
    if (!chain || chain.length < 3) return "";
    var seq = chain.slice(0, chain.length - 1);              // drop the repeated closing node
    var n = seq.length;
    if (n < 2) return "";
    var neg = {};
    (negPairs || []).forEach(function (pr) { neg[pr[0] + ">" + pr[1]] = true; });
    var lev = markLeverage ? leverageTargets(chain) : {};

    var W = small ? 480 : 620, H = small ? 430 : 560;
    var CX = W / 2, CY = H / 2 + (small ? 4 : 6);
    var R = small ? 132 : 176;
    var HW = small ? 62 : 78, HH = small ? 21 : 26;
    var uid = "r" + Math.random().toString(36).slice(2, 8);
    var out = ['<svg class="cv-ring" viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Causal loop diagram">'];
    out.push('<defs><marker id="p' + uid + '" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9 z" class="cv-mk-p"/></marker>' +
             '<marker id="n' + uid + '" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M 1 1 L 9 5 L 1 9 z" class="cv-mk-n"/></marker></defs>');

    var pos = seq.map(function (_, i) {
      var a = (-90 + i * (360 / n)) * Math.PI / 180;
      return [CX + R * Math.cos(a), CY + R * Math.sin(a)];
    });

    for (var i = 0; i < n; i++) {
      var a = pos[i], b = pos[(i + 1) % n];
      var isNeg = neg[seq[i] + ">" + seq[(i + 1) % n]];
      var dx = b[0] - a[0], dy = b[1] - a[1], L = Math.sqrt(dx * dx + dy * dy) || 1;
      var bnd = Math.min(dx ? HW / Math.abs(dx) : 1e9, dy ? HH / Math.abs(dy) : 1e9);
      var g = 14 / L;
      var sx = a[0] + dx * (bnd + g), sy = a[1] + dy * (bnd + g);
      var ex = b[0] - dx * (bnd + g), ey = b[1] - dy * (bnd + g);
      var bend = Math.min(46, L * 0.14);
      var px = -dy / L, py = dx / L;
      var mx0 = (sx + ex) / 2, my0 = (sy + ey) / 2;
      if ((mx0 - CX) * px + (my0 - CY) * py < 0) { px = -px; py = -py; }
      var mx = mx0 + px * bend, my = my0 + py * bend;
      out.push('<path d="M ' + sx.toFixed(1) + " " + sy.toFixed(1) + " Q " + mx.toFixed(1) + " " + my.toFixed(1) +
        " " + ex.toFixed(1) + " " + ey.toFixed(1) + '" class="cv-arc' + (isNeg ? " is-neg" : "") +
        '" marker-end="url(#' + (isNeg ? "n" : "p") + uid + ')"/>');
      var sgx = mx0 + px * (bend + 26), sgy = my0 + py * (bend + 26);
      out.push('<text x="' + sgx.toFixed(1) + '" y="' + (sgy + 7).toFixed(1) + '" class="cv-sgn' +
        (isNeg ? " is-neg" : "") + '" text-anchor="middle">' + (isNeg ? "&#8722;" : "+") + "</text>");
    }

    seq.forEach(function (id, i) {
      var v = VARS[id], label = v ? v.label : id;
      var x = pos[i][0], y = pos[i][1];
      out.push('<rect x="' + (x - HW).toFixed(1) + '" y="' + (y - HH).toFixed(1) + '" width="' + HW * 2 +
        '" height="' + HH * 2 + '" rx="3" class="cv-nd' + (i === 0 ? " is-first" : "") +
        (lev[id] ? " is-lever" : "") + '"/>');
      if (lev[id]) {
        out.push('<circle cx="' + (x + HW - 9).toFixed(1) + '" y="0" cy="' + (y - HH + 9).toFixed(1) +
          '" r="5.5" class="cv-lev-dot"/>');
      }
      var lines = wrap(label, small ? 15 : 18);
      if (lines.length > 1) {
        out.push('<text x="' + x.toFixed(1) + '" y="' + (y - 3).toFixed(1) + '" class="cv-ndt" text-anchor="middle">' + esc(lines[0]) + "</text>");
        out.push('<text x="' + x.toFixed(1) + '" y="' + (y + 12).toFixed(1) + '" class="cv-ndt" text-anchor="middle">' + esc(lines[1]) + "</text>");
      } else {
        out.push('<text x="' + x.toFixed(1) + '" y="' + (y + 5).toFixed(1) + '" class="cv-ndt" text-anchor="middle">' + esc(lines[0]) + "</text>");
      }
    });

    var negs = (negPairs || []).length;
    out.push('<text x="' + CX + '" y="' + (CY - 4) + '" class="cv-ctr' + (negs % 2 ? " is-bal" : "") + '" text-anchor="middle">' +
      (negs % 2 ? "BALANCING" : "REINFORCING") + "</text>");
    out.push('<text x="' + CX + '" y="' + (CY + 17) + '" class="cv-ctr2" text-anchor="middle">' +
      negs + " minus" + (negs === 1 ? "" : "es") + " &#183; " + (negs % 2 ? "pushes back" : "compounds") + "</text>");
    out.push("</svg>");
    return out.join("");
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
      return '<div><span class="cv-who">' + esc(nameOf(p)) + "</span><p>" + esc(p.position) + "</p></div>";
    }).join("") + "</div>");
    parts.push('<div class="cv-field"><span>Why it matters</span><p>' + esc(d.whyItMatters) + "</p></div>");
    if (d.resolutionOptions && d.resolutionOptions.length) {
      parts.push('<div class="cv-field"><span>Ways to resolve it</span><ul class="cv-options">' +
        d.resolutionOptions.map(function (o) { return "<li>" + esc(o) + "</li>"; }).join("") + "</ul></div>");
    }
    if (d.synthesis) {
      parts.push('<div class="cv-synth"><span class="cv-kicker">' + esc(d.synthesis.headline) + "</span>");
      parts.push('<ol class="cv-phases">' + d.synthesis.phases.map(function (ph) {
        return '<li><span class="cv-phn">' + ph.n + "</span><div><strong>" + esc(ph.name) + "</strong>" +
          "<p>" + esc(ph.what) + "</p>" +
          '<div class="cv-phwho">' + ph.who.map(function (w) { return "<span>" + esc(w) + "</span>"; }).join("") +
          '<em>' + esc(ph.loop) + "</em></div></div></li>";
      }).join("") + "</ol>");
      parts.push('<p class="cv-note">' + esc(d.synthesis.note) + "</p></div>");
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

  var VARS = {};
  DATA.registry.variables.forEach(function (v) { VARS[v.id] = v; });
  var PEOPLE = { joann:"Joann", sly:"Sly", henry:"Henry", josh:"Josh", lia:"Lia", ola:"Ola" };

  function chainStrip(chain, negPairs) {
    if (!chain || !chain.length) return '<p class="cv-nochain">Structure not supplied.</p>';
    var neg = {};
    (negPairs || []).forEach(function (p) { neg[p[0] + ">" + p[1]] = true; });
    var out = ['<div class="cv-strip-wrap"><div class="cv-strip">'];
    chain.forEach(function (id, i) {
      var v = VARS[id];
      var last = i === chain.length - 1;
      out.push('<span class="cv-v' + (last ? " is-back" : "") + '">' + esc(v ? v.label : id) + "</span>");
      if (!last) {
        var isNeg = neg[id + ">" + chain[i + 1]];
        out.push('<span class="cv-s' + (isNeg ? " is-neg" : "") + '">' + (isNeg ? "&minus;" : "+") + "</span>");
      }
    });
    out.push("</div></div>");
    return out.join("");
  }

  function loopCard(loop) {
    var people = Object.keys(loop.contributors);
    var negs = (loop.negativeLinks || []).length;
    var parity = negs % 2 === 0 ? "compounds" : "pushes back";
    var parts = ['<article class="cv-card cv-loop is-' + esc(loop.convergence) + '">'];
    parts.push('<header><div class="cv-card-head">' +
      '<code class="cv-loopcode">' + esc(loop.id) + "</code>" +
      badge(loop.convergence, loop.convergence) +
      '<span class="cv-tally">' + people.length + " of 6</span></div>");
    parts.push("<h4>" + esc(loop.name) + "</h4></header>");
    parts.push('<p class="cv-loopsum">' + esc(loop.summary) + "</p>");
    parts.push(loopSvg(loop.canonicalChain, loop.negativeLinks, false, true));
    parts.push('<p class="cv-parity"><strong>' + esc(loop.type) + "</strong> &middot; " +
      negs + " minus" + (negs === 1 ? "" : "es") + " &middot; " + parity + "</p>");
    if (loop.derivation) {
      parts.push('<div class="cv-field is-next"><span>Drafted, not supplied &middot; ' +
        esc(loop.derivation.confidence) + ' confidence</span><p>' + esc(loop.derivation.assumption) + "</p></div>");
    }
    parts.push('<div class="cv-field"><span>What this tells us</span><p>' + esc(loop.finding) + "</p></div>");
    var acting = leverageOn(loop.canonicalChain);
    if (acting.length) {
      parts.push('<div class="cv-field"><span>Leverage points acting on this loop</span>' +
        '<ul class="cv-levlist">' + acting.map(function (p) {
          return "<li><code>" + esc(p.ref) + "</code><strong>" + esc(p.title) + "</strong>" +
            '<em>' + esc(p.author) + "</em></li>";
        }).join("") + "</ul></div>");
    }
    parts.push('<div class="cv-drawnby">' + people.map(function (k) {
      return '<span class="cv-who">' + esc(PEOPLE[k] || k) + "</span>";
    }).join("") + "</div>");
    parts.push("</article>");
    return parts.join("");
  }

  function personSection(key) {
    var loops = DATA.registry.loops.filter(function (l) { return l.contributors[key]; });
    if (!loops.length) return "";
    var out = ['<section class="cv-person"><h4>' + esc(PEOPLE[key]) +
      '<span class="cv-personcount">' + loops.length + " loop" + (loops.length === 1 ? "" : "s") + "</span></h4>"];
    out.push('<div class="cv-personloops">');
    loops.forEach(function (l) {
      var c = l.contributors[key];
      out.push('<div class="cv-ploop">' +
        '<div class="cv-ploop-head"><strong>' + esc(c.name) + "</strong>" +
        (c.originalCode && c.originalCode !== "-" ? '<code>their code: ' + esc(c.originalCode) + "</code>" : "") +
        '<code class="cv-maps">maps to ' + esc(l.id) + "</code></div>" +
        (c.chain && c.chain.length ? loopSvg(c.chain, l.negativeLinks, true) : '<p class="cv-nochain">Structure not supplied.</p>') +
        '<p class="cv-pnote">' + esc(c.note) + "</p>" +
        (c.evidence ? '<p class="cv-eff">' + esc(c.evidence) + "</p>" : "") +
        "</div>");
    });
    out.push("</div></section>");
    return out.join("");
  }

  function lpCard(p) {
    var rows = [
      ["Mechanism", p.mechanism], ["Signal", p.signal], ["Result", p.result],
      ["Classification", p.classification], ["Depends on", p.dependency], ["Evidence", p.evidence]
    ].filter(function (r) { return r[1]; });
    return '<article class="cv-lp' + (p.status === "inferred" ? " is-inferred" : "") + '">' +
      '<div class="cv-lp-head"><code>' + esc(p.ref) + "</code>" +
      (p.effect ? '<span class="cv-lp-eff">' + esc(p.effect) + "</span>" : "") +
      (p.status === "inferred" ? '<span class="cv-lp-flag">reconstructed, not stated</span>' : "") +
      "</div><h5>" + esc(p.title) + "</h5>" +
      (p.role ? '<p class="cv-lp-role">' + esc(p.role) + "</p>" : "") +
      rows.map(function (r) {
        return '<div class="cv-field"><span>' + r[0] + "</span><p>" + esc(r[1]) + "</p></div>";
      }).join("") + "</article>";
  }

  function lpSection(c) {
    return '<section class="cv-person"><h4>' + esc(c.displayName) +
      '<span class="cv-personcount">' + c.points.length + " leverage point" +
      (c.points.length === 1 ? "" : "s") + "</span></h4>" +
      '<div class="cv-lp-grid">' + c.points.map(lpCard).join("") + "</div></section>";
  }

  var LEV = [];
  DATA.leveragePointsByAuthor.contributors.forEach(function (c) {
    c.points.forEach(function (p) { LEV.push(p); });
  });
  function leverageOn(chain) {
    var inChain = {};
    (chain || []).forEach(function (v) { inChain[v] = true; });
    return LEV.filter(function (p) {
      return (p.targets || []).some(function (v) { return inChain[v]; });
    });
  }
  function leverageTargets(chain) {
    var hit = {};
    leverageOn(chain).forEach(function (p) {
      (p.targets || []).forEach(function (v) { hit[v] = true; });
    });
    return hit;
  }

  var DIAG = DATA.structuralDiagnostic;

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
        '<button type="button" class="btn btn-primary" data-cv-panel="converge" aria-pressed="true">Where we agree</button>' +
        '<button type="button" class="btn" data-cv-panel="alllev" aria-pressed="false">Every leverage point, by author</button>' +
        '<button type="button" class="btn" data-cv-panel="allloops" aria-pressed="false">Every loop, by author</button>' +
        '<button type="button" class="btn" data-cv-panel="canon" aria-pressed="false">The team&rsquo;s nine loops</button>' +
        '<button type="button" class="btn" data-cv-panel="diverge" aria-pressed="false">Divergence</button>' +
        '<button type="button" class="btn" data-cv-panel="who" aria-pressed="false">Contributors</button>' +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="converge">' +
        '<div class="cv-grid">' + DATA.convergence.leverage.map(clusterCard).join("") + "</div>" +
        '<p class="cv-fine">Product-definition convergence now sits on the Causal Loop Convergence page, with the loops it derives from. Convergence strength describes how independently contributors arrived at the same claim. It never upgrades epistemic status: ' +
        esc(DATA.classificationRule) + "</p>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="alllev" hidden>' +
        '<p class="cv-lead">Every leverage point as its author wrote it, before merging. The merged themes are under Where we agree; this is where each person finds their own work. Anything reconstructed rather than stated is marked.</p>' +
        DATA.leveragePointsByAuthor.contributors.map(lpSection).join("") +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="allloops" hidden>' +
        '<p class="cv-lead">Every loop anyone drew, drawn as a full loop, grouped by author. Each one is labelled with the canonical loop it resolves to, so you can see which of your loops is also someone else&rsquo;s.</p>' +
        ["joann","sly","henry","josh","lia","ola"].map(personSection).join("") +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="canon" hidden>' +
        '<section class="cv-card cv-diag">' +
          '<span class="cv-kicker">Faculty feedback &middot; actioned 10 Sept</span>' +
          "<h3>" + esc(DIAG.headline) + "</h3>" +
          '<p class="cv-scope">' + esc(DIAG.scope) + "</p>" +
          "<p>" + esc(DIAG.measured) + "</p>" +
          "<p>" + esc(DIAG.interpretation) + "</p>" +
          '<div class="cv-diagrid">' + DIAG.byView.map(function (v) {
            return '<div class="cv-diagcell"><span>' + esc(v.view) + "</span>" +
              '<strong><em class="cv-was">' + esc(String(v.before)) + "</em> &rarr; " + esc(String(v.after)) + "</strong></div>";
          }).join("") + "</div>" +
          '<p class="cv-remedy">' + esc(DIAG.remedy) + "</p>" +
          '<p class="cv-note">' + esc(DIAG.note) + "</p>" +
        "</section>" +
        '<div class="cv-grid">' + DATA.registry.loops.map(loopCard).join("") + "</div>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="diverge" hidden>' +
        '<div class="cv-grid">' + DATA.divergences.map(divergenceCard).join("") + "</div>" +
      "</div>" +
      '<div class="cv-panel" data-cv-panel-body="who" hidden>' +
        '<div class="cv-grid">' + DATA.contributors.map(contributorCard).join("") + "</div>" +
      "</div>" +
    "</div>";

  root.appendChild(section);

  var button = el("button", "btn", "5. Convergence");
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
