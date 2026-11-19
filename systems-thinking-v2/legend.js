/* Legend: show only what is on screen, grouped by the question it answers,
   plus a plain-language key for the classifier words. Additive - the original
   legend markup is restructured in place rather than replaced by the renderer. */
(function () {
  "use strict";
  var root = document.querySelector("#loyalty-map-v2");
  var grid = document.querySelector("#lm2-grid");
  var legend = root && root.querySelector(".lm2-legend");
  if (!root || !grid || !legend) return;

  // which legend entries belong to which node style, so we can filter by view
  var STYLE = {
    "Population": "population", "Process / behaviour": "value", "Value state": "state",
    "Partner": "partner", "Capability": "capability", "Future opportunity": "future",
    "Outside boundary": "external", "Intended outcome": "outcome"
  };
  var GROUP = {
    "Population": "boxes", "Process / behaviour": "boxes", "Value state": "boxes",
    "Partner": "boxes", "Capability": "boxes", "Future opportunity": "boxes",
    "Outside boundary": "boxes", "Intended outcome": "boxes",
    "Structural flow": "lines", "Future pathway": "lines", "Inferred relationship": "lines"
  };
  var CLASSIFIERS = ["Supported", "Group convergence", "Hypothesis"];

  var items = [].slice.call(legend.querySelectorAll(".lm2-legend-item"));
  var byLabel = {};
  items.forEach(function (b) { byLabel[b.textContent.trim()] = b; });

  // Data and decisioning carries its own style and had no entry at all
  if (!byLabel["Priority capability"]) {
    var src = byLabel["Capability"];
    if (src) {
      var extra = src.cloneNode(true);
      var help = "A capability the analysis singles out as the first place to act. Currently Data and decisioning.";
      extra.setAttribute("data-legend-help", help);
      extra.setAttribute("data-tooltip", help);
      extra.querySelector("i").className = "lm2-key lm2-key-priority";
      extra.lastChild.nodeValue = "Priority capability";
      src.parentNode.insertBefore(extra, src.nextSibling);
      items.push(extra);
      byLabel["Priority capability"] = extra;
      GROUP["Priority capability"] = "boxes";
      STYLE["Priority capability"] = "priority";
    }
  }

  // rebuild as three labelled groups
  var wrap = legend.querySelector(".lm2-legend-items");
  var groups = {
    boxes: {label: "What the boxes mean", el: null},
    lines: {label: "What the lines mean", el: null},
    sure:  {label: "How sure we are",     el: null}
  };
  Object.keys(groups).forEach(function (k) {
    var g = document.createElement("div");
    g.className = "lm2-legend-group";
    g.setAttribute("data-legend-group", k);
    g.innerHTML = '<span class="lm2-legend-grouplabel">' + groups[k].label + "</span>";
    groups[k].el = g;
    wrap.appendChild(g);
  });
  items.forEach(function (b) {
    var label = b.textContent.trim();
    var key = GROUP[label] || (CLASSIFIERS.indexOf(label) > -1 ? "sure" : "boxes");
    groups[key].el.appendChild(b);
  });

  // plain-language key, collapsed by default
  var glossary = document.createElement("div");
  glossary.className = "lm2-glossary";
  glossary.hidden = true;
  glossary.innerHTML =
    '<p class="lm2-glossary-intro">Every box and arrow carries three labels, answering three different questions.</p>' +
    '<div class="lm2-glossary-cols">' +
      '<div><h4>How sure are we?</h4><dl>' +
        "<dt>Supported</dt><dd>We have evidence for this.</dd>" +
        "<dt>Inferred</dt><dd>Worked out from what we know. Reasonable, not proven.</dd>" +
        "<dt>Assumed</dt><dd>Taken as given so the model holds together. No evidence.</dd>" +
        "<dt>Contested</dt><dd>Credible people disagree.</dd>" +
        "<dt>Unresolved</dt><dd>We cannot honestly call it yet.</dd>" +
      "</dl></div>" +
      '<div><h4>Where did it come from?</h4><dl>' +
        "<dt>Evidence</dt><dd>A source is linked.</dd>" +
        "<dt>Evidence trace pending</dt><dd>Earlier work treated it as evidenced, but nobody has found the source.</dd>" +
        "<dt>Analytical inference</dt><dd>Reasoned from the model, not from data.</dd>" +
        "<dt>Group convergence</dt><dd>The team agreed it. <strong>Agreement is not evidence.</strong></dd>" +
        "<dt>Model definition</dt><dd>A definition we set so the model stays consistent.</dd>" +
      "</dl></div>" +
      '<div><h4>What are we doing about it?</h4><dl>' +
        "<dt>Active direction</dt><dd>We are building on this.</dd>" +
        "<dt>Hypothesis</dt><dd>We think it might work. Needs testing.</dd>" +
        "<dt>Intended outcome</dt><dd>We want this to happen. We have not shown it will.</dd>" +
        "<dt>Unresolved</dt><dd>No call made.</dd>" +
      "</dl></div>" +
    "</div>";
  legend.appendChild(glossary);

  var toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "btn btn-ghost text-small lm2-glossary-toggle";
  toggle.textContent = "What do these words mean?";
  toggle.setAttribute("aria-expanded", "false");
  toggle.addEventListener("click", function () {
    glossary.hidden = !glossary.hidden;
    toggle.setAttribute("aria-expanded", String(!glossary.hidden));
    toggle.textContent = glossary.hidden ? "What do these words mean?" : "Hide";
  });
  legend.querySelector(".lm2-legend-title").insertAdjacentElement("afterend", toggle);

  // only show entries for styles present in the current view
  function sync() {
    var present = {};
    grid.querySelectorAll(".lm2-node").forEach(function (n) {
      var m = n.className.match(/lm2-node-(\w+)/);
      if (m) present[m[1]] = true;
    });
    items.forEach(function (b) {
      var label = b.textContent.trim();
      var style = STYLE[label];
      b.hidden = !!style && !present[style];
    });
    Object.keys(groups).forEach(function (k) {
      var g = groups[k].el;
      var any = [].slice.call(g.querySelectorAll(".lm2-legend-item")).some(function (b) { return !b.hidden; });
      g.hidden = !any;
    });
  }
  new MutationObserver(sync).observe(grid, {childList: true, attributes: true, attributeFilter: ["data-view"]});
  sync();
})();
