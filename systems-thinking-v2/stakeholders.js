/* GENERATED FROM data/stakeholders.json by scripts/build-stakeholders.py. */
(function () {
  "use strict";
  var root = document.querySelector("#loyalty-map-v2");
  var controls = root && root.querySelector(".viz-controls");
  if (!root || !controls) return;

  var section = document.createElement("section");
  section.id = "stakeholders-view";
  section.hidden = true;
  section.innerHTML = "<div class=\"sh-wrap\"><header class=\"sh-hero\"><span class=\"sh-kicker\">Who can move the system</span><h3>Stakeholder analysis \u2014 power and interest</h3><p>Separate from the systems map and deliberately so: this answers who can move the system, not how the system moves. Members are individually low-power but collectively decisive \u2014 mass churn is the real source of member power, and it enters the map through partner coverage.</p></header><div class=\"sh-matrix\"><div class=\"sh-ylabel\"><span>Power &rarr;</span></div><div class=\"sh-grid\"><div class=\"sh-quad is-satisfied\"><div class=\"sh-quad-head\"><h4>Keep satisfied</h4><span>power high &middot; interest low</span></div><p class=\"sh-guidance\">High power, low interest. They will not follow the detail, but they can stop it.</p><ol class=\"sh-list\"><li><span class=\"sh-n\">5</span><div><strong>Diversified Royalty Corp</strong></div></li><li><span class=\"sh-n\">6</span><div><strong>Regulators</strong><em>Competition Bureau, IFRS.</em></div></li><li><span class=\"sh-n\">7</span><div><strong>Finance & Risk</strong><em>Liability owners \u2014 and the owners of the breakage brake.</em></div></li><li><span class=\"sh-n\">8</span><div><strong>Expedia</strong><em>Travel platform vendor.</em></div></li></ol></div><div class=\"sh-quad is-manage\"><div class=\"sh-quad-head\"><h4>Manage closely</h4><span>power high &middot; interest high</span></div><p class=\"sh-guidance\">High power and high interest. These decide whether the work proceeds.</p><ol class=\"sh-list\"><li><span class=\"sh-n\">1</span><div><strong>Emerging Business team</strong><em>The client.</em></div></li><li><span class=\"sh-n\">2</span><div><strong>BMO exec sponsors / leadership</strong></div></li><li><span class=\"sh-n\">3</span><div><strong>Cards & Credit business</strong></div></li><li><span class=\"sh-n\">4</span><div><strong>Data & Analytics / product tech</strong></div></li></ol></div><div class=\"sh-quad is-monitor\"><div class=\"sh-quad-head\"><h4>Monitor</h4><span>power low &middot; interest low</span></div><p class=\"sh-guidance\">Low power, low interest. Watch for change rather than manage.</p><ol class=\"sh-list\"><li><span class=\"sh-n\">12</span><div><strong>Non-BMO casual members</strong></div></li><li><span class=\"sh-n\">13</span><div><strong>Prospective members / public</strong><em>The prospect who weighs a join offer before becoming a member.</em></div></li><li><span class=\"sh-n\">14</span><div><strong>Lapsed collectors</strong></div></li></ol></div><div class=\"sh-quad is-informed\"><div class=\"sh-quad-head\"><h4>Keep informed</h4><span>power low &middot; interest high</span></div><p class=\"sh-guidance\">Low individual power, high interest. Collectively decisive: mass churn is the real source of member power.</p><ol class=\"sh-list\"><li><span class=\"sh-n\">9</span><div><strong>Everyday active members</strong><em>The primary user in the team's product definitions.</em></div></li><li><span class=\"sh-n\">10</span><div><strong>Legacy AIR MILES collectors</strong></div></li><li><span class=\"sh-n\">11</span><div><strong>Earn / redeem partners</strong><em>The supply side of partner coverage.</em></div></li></ol></div></div><div class=\"sh-xlabel\"><span>Interest &rarr;</span></div></div><p class=\"sh-fine\">14 stakeholders. Joann's five-loop systems map (Stakeholder analysis + systems map V2).</p></div>";
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
