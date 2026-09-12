/* GENERATED FROM data/system-map.json by scripts/build-view-notes.py.
   Do not edit directly. */
(function () {
  "use strict";
  var NOTES = {"transition": {"title": "What it's for", "paragraphs": ["It's a diagnostic tool for locating loss. “Members don't get value” is unactionable. Splitting it into five steps lets you ask which step — and each step has a different owner and a different fix. Posting failing is an operations problem. Use and conversion failing is a discovery and channel problem. Without the split you'd treat them as one thing and fix the wrong one.", "This is a value progression, not a systems map. It shows the language we use at each stage, not the structure of the system — that is view 1.", "Read it in three bands. The top row is the five states value passes through — it starts programme-wide as the whole catalogue, narrows to one member, then becomes theirs. The middle row is what moves it between them, and each of those touches several stages rather than one: a member sees an opportunity in a channel, service explains it, data decides what gets surfaced at all. The bottom row is what stalls value, and where members actually join.", "The sequence holds — value cannot reach available without being earned — but a member can join at any point. Signing up grants roughly 750 points, so a new member holds a balance having earned nothing."]}};
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
