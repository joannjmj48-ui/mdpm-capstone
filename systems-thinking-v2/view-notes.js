/* GENERATED FROM data/system-map.json by scripts/build-view-notes.py.
   Do not edit directly. */
(function () {
  "use strict";
  var NOTES = {"transition": {"title": "What it's for", "paragraphs": ["It's a diagnostic tool for locating loss. “Members don't get value” is unactionable. Splitting it into five steps lets you ask which step — and each step has a different owner and a different fix. VT03 failing is an operations and posting problem. VT04 failing is a discovery and channel problem. Without the split you'd treat them as one thing and fix the wrong one.", "This is a value progression, not a systems map. It shows the language we use for each stage, not the structure of the system — that is view 1.", "The progression is sequential - value cannot reach Available Value without being earned first - but an individual member can join it at any point. Signing up grants roughly 750 points, so a new member starts holding Available Value without having earned anything. The diagram shows the end-to-end flow, not one mandatory journey.", "Under review from 12 September: A state earns its own name only if we can say what observably changes when value enters it. If we cannot tell what refines an offer from one stage into the next, it does not require an independent stage name. Agreed 12 September. Potential Value is the state this test currently challenges, because nobody could name what observably changes between an offer and a targeted offer."], "footnote": "VT01–VT05 are the value transitions: the five steps value passes through, each a place it can stall."}};
  var root = document.querySelector("#loyalty-map-v2");
  var grid = document.querySelector("#lm2-grid");
  if (!root || !grid) return;

  var panel = document.createElement("aside");
  panel.className = "lm2-viewnote";
  panel.hidden = true;
  // sits at the top of the page, directly under the tabs: purpose first,
  // then how to read, then the map itself
  var controls = root.querySelector(".viz-controls");
  if (controls && controls.nextSibling) root.insertBefore(panel, controls.nextSibling);
  else root.appendChild(panel);

  function esc(s) {
    return String(s).replace(/[&<>]/g, function (c) {
      return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}[c];
    });
  }

  function sync() {
    var note = NOTES[grid.getAttribute("data-view")];
    var mapShowing = !root.querySelector(":scope > .lm2-map-wrap").hidden;
    if (!note || !mapShowing) { panel.hidden = true; return; }
    panel.innerHTML = "<h3>" + esc(note.title) + "</h3>" +
      note.paragraphs.map(function (p) { return "<p>" + esc(p) + "</p>"; }).join("") +
      (note.footnote ? '<p class="lm2-viewnote-fn">' + esc(note.footnote) + "</p>" : "");
    panel.hidden = false;
  }

  new MutationObserver(sync).observe(grid, {attributes: true, attributeFilter: ["data-view"]});
  root.querySelectorAll("[data-map-view], [data-cv-view], [data-nv-view]").forEach(function (b) {
    b.addEventListener("click", function () { setTimeout(sync, 0); });
  });
  sync();
})();
