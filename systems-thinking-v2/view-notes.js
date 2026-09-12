/* GENERATED FROM data/system-map.json by scripts/build-view-notes.py.
   Do not edit directly. */
(function () {
  "use strict";
  var NOTES = {"transition": {"title": "What it's for", "paragraphs": ["Finding where value gets lost. “Members don't get value” is unactionable; five steps let you ask which step — and each has a different owner and a different fix.", "This is a value progression, not a systems map. The sequence holds, but a member can join at any point: signing up grants roughly 750 points, so a new member starts holding a balance. The first two states may belong to a prospect rather than a member."]}};
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
