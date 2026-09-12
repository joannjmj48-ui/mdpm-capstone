/* Region grouping for the Current System view.
   Groups the eleven components into the five regions declared in
   data/system-map.json, following the region device in Joann's MMIE 884
   systems map. Additive: the map renderer is not modified. It rebuilds the
   grid on every view change, so the bands are re-injected by observation. */
(function () {
  "use strict";

  var BY_VIEW = {
    current: [
      {id: "rpop",  label: "Member populations",    hint: "Who is in the system"},
      {id: "rval",  label: "Value realization",     hint: "The main variable and its feedback"},
      {id: "rgov",  label: "Governance and economics", hint: "Who sets the goal and funds it"},
      {id: "rpart", label: "Partner ecosystem",     hint: "Who supplies the value"},
      {id: "rback", label: "Enabling backbone",     hint: "What delivers it"},
      {id: "rcond", label: "Structural conditions", hint: "What obstructs it"}
    ],
    transition: [
      {id: "rstates", label: "The five value states",       hint: "What value is at each stage"},
      {id: "rmoves",  label: "What moves it between them",  hint: "Each one touches several stages"},
      {id: "rentry",  label: "Conditions and entry",        hint: "What stalls it, and where members join"}
    ]
  };

  var REGIONS = [
    {id: "rpop",  label: "Member populations",    hint: "Who is in the system"},
    {id: "rval",  label: "Value realization",     hint: "The main variable and its feedback"},
    {id: "rpart", label: "Partner ecosystem",     hint: "Who supplies the value"},
    {id: "rback", label: "Enabling backbone",     hint: "What delivers it"},
    {id: "rcond", label: "Structural conditions", hint: "What obstructs it"}
  ];

  var grid = document.querySelector("#lm2-grid");
  if (!grid) return;

  function inject() {
    var regions = BY_VIEW[grid.getAttribute("data-view")];
    if (!regions) return;
    if (grid.querySelector(".lm2-region")) return;
    regions.forEach(function (r, i) {
      var band = document.createElement("div");
      band.className = "lm2-band";
      band.style.gridRow = String(i + 1);
      band.setAttribute("aria-hidden", "true");
      grid.appendChild(band);

      var tag = document.createElement("div");
      tag.className = "lm2-region";
      tag.style.gridArea = r.id;
      tag.innerHTML = "<strong>" + r.label + "</strong><span>" + r.hint + "</span>";
      grid.appendChild(tag);
    });
  }

  new MutationObserver(inject).observe(grid, {childList: true, attributes: true, attributeFilter: ["data-view"]});
  inject();
})();
