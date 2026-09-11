#!/usr/bin/env python3
"""Build narrative.js / narrative.css from data/narrative-source.html.

The One Engine, Four Brakes narrative is authored as a standalone page. This
adapts it into a view module for the V2 site without touching the existing map
renderer: all of its CSS is scoped under #narrative-view, and its palette
tokens are redefined there in terms of the site's own tokens so it follows the
site's light and dark themes rather than carrying its own.
"""
import re, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "data" / "narrative-source.html").read_text(encoding="utf-8")

style = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
body = src.split("</style>", 1)[1].strip()

# --- palette: express the narrative's tokens in the site's tokens ----------
TOKENS = """#narrative-view {
  --ground:      var(--background);
  --surface:     var(--secondary);
  --sunken:      var(--card);
  --ink:         var(--foreground);
  --ink-soft:    var(--muted-foreground);
  --rule:        var(--border);
  --rule-soft:   var(--border);
  --reinforce:   var(--green);
  --reinforce-w: color-mix(in oklab, var(--green) 14%, transparent);
  --balance:     var(--destructive);
  --balance-w:   color-mix(in oklab, var(--destructive) 14%, transparent);
  --accent:      var(--primary);
  --accent-w:    var(--accent);
  --f-display:   "Newsreader", "Iowan Old Style", Georgia, serif;
  --f-body:      var(--font-sans);
  --f-mono:      var(--font-mono);
  --spine: 68ch;
  --wide: 100%;
}
"""

def scope(css):
    """Prefix every rule selector with #narrative-view."""
    out, i = [], 0
    while i < len(css):
        if css[i] == "@":                       # at-rule: recurse into its block
            head_end = css.index("{", i)
            head = css[i:head_end].strip()
            depth, j = 1, head_end + 1
            while depth:
                if css[j] == "{": depth += 1
                elif css[j] == "}": depth -= 1
                j += 1
            inner = css[head_end + 1:j - 1]
            out.append(head + " {\n" + scope(inner) + "\n}")
            i = j
            continue
        brace = css.find("{", i)
        if brace < 0:
            break
        sels = css[i:brace].strip()
        depth, j = 1, brace + 1
        while depth:
            if css[j] == "{": depth += 1
            elif css[j] == "}": depth -= 1
            j += 1
        block = css[brace + 1:j - 1]
        if sels:
            fixed = []
            for s in (x.strip() for x in sels.split(",")):
                if not s:
                    continue
                if s in (":root", "body"):
                    fixed.append("#narrative-view")
                elif s.startswith(':root:not([data-theme="light"])'):
                    fixed.append("#narrative-view")
                elif s.startswith(':root[data-theme="dark"]'):
                    fixed.append('[data-theme="dark"] #narrative-view')
                elif s == "*":
                    fixed.append("#narrative-view *")
                elif s == ":focus-visible":
                    fixed.append("#narrative-view :focus-visible")
                else:
                    fixed.append("#narrative-view " + s)
            out.append(", ".join(fixed) + " {" + block + "}")
        i = j
    return "\n".join(out)

# drop the narrative's own :root palette blocks; the site's tokens drive it now
style = re.sub(r":root\s*\{[^}]*\}", "", style, count=1)
style = re.sub(r"@media \(prefers-color-scheme: dark\)\s*\{\s*:root:not\(\[data-theme=\"light\"\]\)\s*\{[^}]*\}\s*\}", "", style)
style = re.sub(r":root\[data-theme=\"dark\"\]\s*\{[^}]*\}", "", style)

css = TOKENS + "\n" + scope(style) + """
#narrative-view { padding: 0 0 2rem; }
#narrative-view .wrap { padding: 0; }
#narrative-view section { border-bottom-color: var(--border); }
#narrative-view .masthead { padding-top: 1.25rem; }
#narrative-view table { min-width: 620px; }
"""
(ROOT / "narrative.css").write_text(css, encoding="utf-8")

js = """/* GENERATED FROM data/narrative-source.html by scripts/build-narrative.py.
   Do not edit directly. */
(function () {
  "use strict";
  var root = document.querySelector("#loyalty-map-v2");
  var controls = root && root.querySelector(".viz-controls");
  if (!root || !controls) return;

  var section = document.createElement("section");
  section.id = "narrative-view";
  section.hidden = true;
  section.setAttribute("aria-labelledby", "nv-title");
  section.innerHTML = __HTML__;
  root.appendChild(section);

  var button = document.createElement("button");
  button.type = "button";
  button.className = "btn";
  button.textContent = "One Engine, Four Brakes";
  button.setAttribute("data-nv-view", "narrative");
  button.setAttribute("aria-pressed", "false");
  controls.appendChild(button);

  function standard() {
    return root.querySelectorAll(":scope > .lm2-map-wrap, :scope > .lm2-legend, :scope > .lm2-detail, :scope > .lm2-guide, :scope > .lm2-instruction-row");
  }
  function show() {
    root.querySelectorAll("[data-map-view], [data-cv-view]").forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
      b.classList.remove("btn-primary");
    });
    var cv = root.querySelector("#convergence-view");
    if (cv) cv.hidden = true;
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
  var cvBtn = root.querySelector("[data-cv-view]");
  if (cvBtn) cvBtn.addEventListener("click", function () {
    button.setAttribute("aria-pressed", "false");
    button.classList.remove("btn-primary");
    section.hidden = true;
  });
})();
"""
(ROOT / "narrative.js").write_text(js.replace("__HTML__", json.dumps(body)), encoding="utf-8")
print(f"wrote narrative.css ({(ROOT/'narrative.css').stat().st_size:,} bytes) and "
      f"narrative.js ({(ROOT/'narrative.js').stat().st_size:,} bytes)")
