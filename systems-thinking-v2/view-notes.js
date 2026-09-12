/* GENERATED FROM data/system-map.json by scripts/build-view-notes.py.
   Do not edit directly. */
(function () {
  "use strict";
  var NOTES = {"transition": {"title": "What it's for", "paragraphs": ["It's a diagnostic tool for locating loss. “Members don't get value” is unactionable. Splitting it into five steps lets you ask which step — and each step has a different owner and a different fix. VT03 failing is an operations and posting problem. VT04 failing is a discovery and channel problem. Without the split you'd treat them as one thing and fix the wrong one."], "footnote": "VT01–VT05 are the value transitions: the five steps value passes through, each a place it can stall."}};
  var root = document.querySelector("#loyalty-map-v2");
  var grid = document.querySelector("#lm2-grid");
  if (!root || !grid) return;

  var panel = document.createElement("aside");
  panel.className = "lm2-viewnote";
  panel.hidden = true;
  root.appendChild(panel);

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
