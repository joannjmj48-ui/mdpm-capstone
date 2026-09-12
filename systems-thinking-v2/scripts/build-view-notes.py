#!/usr/bin/env python3
"""Generate view-notes.js from any view in data/system-map.json carrying a
`viewNote`. The note renders under the map for that view only.

Content lives in the contract, not in the module, so a note is added or edited
by changing system-map.json and re-running this script.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((ROOT / "data" / "system-map.json").read_text(encoding="utf-8"))
notes = {v["id"]: v["viewNote"] for v in d["views"] if v.get("viewNote")}

js = """/* GENERATED FROM data/system-map.json by scripts/build-view-notes.py.
   Do not edit directly. */
(function () {
  "use strict";
  var NOTES = __NOTES__;
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
"""
(ROOT / "view-notes.js").write_text(js.replace("__NOTES__", json.dumps(notes, ensure_ascii=False)), encoding="utf-8")
print(f"wrote view-notes.js for: {', '.join(notes) or '(no views carry a note)'}")
