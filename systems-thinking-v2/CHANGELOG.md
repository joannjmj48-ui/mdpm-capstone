# Version 2 change log

## Baseline scaffold

- Created an isolated copy of the current Version 1 experience.
- Added a visible Version 2 workspace identifier.
- Namespaced browser-only guide and tour preferences so V1 and V2 cannot affect one another.
- Added research-intake and model-contract scaffolding.
- No nodes, relationships, boundaries, evidence, contextual content, layouts, or interaction behavior have been changed.

## Baseline extraction and refreshed-research audit

- Extracted the embedded baseline into `data/baseline-system-map.json` without changing the renderer.
- Preserved 22 nodes, 38 relationships, four views, edge meanings, layout metadata, and contextual narratives.
- Added `STRUCTURAL_AUDIT.md` comparing the baseline with the refreshed analytical architecture contract.
- Proposed changes remain unimplemented pending explicit approval.

## Approved V2 analytical model

- Approved all eight structural decision gates.
- Made Member Value Realization the main variable while retaining the stable `member-value` ID.
- Added five controlled value states and transitions VT01–VT05.
- Reclassified Meaningful Engagement as downstream behaviour and feedback.
- Merged the duplicate future engagement entity into `engagement`.
- Replaced Transition Overview with Main Variable Transition.
- Added JTBD and DVO overlays without treating them as system nodes.
- Added independent epistemic-status, claim-basis, and decision-status classifiers.
- Marked group-converged directions and hypotheses as non-evidentiary.
- Extended the schema and added a deterministic contract-to-renderer adapter.
- Updated only V2; V1 remains untouched.

## Production hardening

- Limited connector rendering and direct-connection lists to relationships whose endpoints are present in the active view.
- Prevented view changes and value-state selection from failing when the full research contract includes relationships outside the active view.

## Team convergence layer

- Added a multi-contributor submission model in `data/submissions/`, one file per contributor.
- Extracted Sylvester's published V1 causal loops, leverage points and product definition as `SUB-SLY`.
- Added Josh's Milestone 2 leverage points and product description as `SUB-JOSH`. His loops R4, R5 and B2 are named but structurally unsupplied and are marked `referenced-not-supplied`.
- Added `data/convergence-map.json` — the curated cross-contributor analysis: 9 clusters, 5 divergences, 4 open gaps.
- Added a Team Convergence view with Convergence, Divergence, Open gaps and Contributors panels.
- The four map views, their renderer and their accessibility behaviour are unchanged; the new view is additive and self-contained in `convergence.js` / `convergence.css`.
- Node is unavailable on the working machine, so the new build and validation scripts are Python equivalents of the existing Node convention. `scripts/sync-index-data.mjs` and `scripts/validate-contract.mjs` were not run and remain untouched.

### Rule preserved

Convergence strength records how independently contributors reached the same claim. It never upgrades epistemic status — two people agreeing is not evidence.

## Evidence and Requirements (November 2026, for the PRD)

- Added tab 8, built additively from `data/evidence-map.json` by `scripts/build-evidence.py`.
- Placed the fourteen issues from the October usability study on the map, each tagged with the
  relationship it acts on and the requirement that answers it. Seven of the fourteen sit at
  Potential Value.
- Mapped all 42 functional requirements to the value stage they act on. One cluster of six —
  diagnose and recover loss — has no corresponding relationship in the map, which is the clearest
  gap the requirements expose.
- Added the four clocks (eligibility, recognition, posting, realization) from the November
  complexity analysis, and the recorded-versus-understood comparison, marked by whether the
  usability study actually reached each row.
- Applied the first primary member evidence to the contract. `SRC-UT-2026-10` is the first source
  with `isEmpiricalEvidence: true`. Interface friction and two relationships moved to Supported;
  three moved to Contested, including the return leg five of six contributors drew independently.
  Convergence still never upgrades epistemic status — testing does.

## Extension to the map (tab 9, November 2026)

Replaces the earlier grid-based attempt, which was drawn in Sly's layout and read as a
replacement rather than an extension. Rebuilt in the format Joann used for MMIE 884, and in the
palette from her own Blue Rewards HTML map.

- Hand-positioned SVG, not the grid renderer. Realized value stays at the centre as the main
  variable. Every link carries a polarity, delays are double-barred, loops are circled and named.
- The relevance flywheel TR1 is drawn muted and dashed: it is what the map already says, and
  nothing here changes it. Colour marks only what the November evidence adds.
- Two new balancing loops, each with exactly one minus. TB4, the recovery brake, is the product:
  unresolved loss triggers recovery capability, which reduces it. TB5, the doubt brake, rides the
  team's own flywheel: realized value creates exposure, unresolved loss creates doubt, and doubt
  withdraws participation.
- Three feeders into unresolved loss: reversals and clawbacks (delayed), unactivated offers, and
  evidence split across five parties.
- A strip along the bottom shows the five stages with the one position the Offer Service's member
  states add: saved or activated.
- The contract is back to the team's agreed model. The nodes, relationships and view added for
  the grid version were removed; the extension holds its own structure in the generator.

## What our product would do to the system (tab 2, second panel)

Added in response to peer feedback asking for sustained systems thinking applied to proposed
changes rather than only to the current system.

- Runs the four capabilities from the November product vision, plus Blue, back through the map.
  For each: what it changes about member behaviour, what it changes about what the surrounding
  parties are rewarded for, who newly has to coordinate, what enables it, what could undermine
  it, what signal to watch, and the question M3 feasibility has to settle.
- Three cross-cutting risks: the engine's return leg is unconfirmed, succeeding costs the
  programme breakage revenue, and visibility raises support load before it lowers it.
- A sequencing conclusion: progression and recovery have to land before discovery, because
  ranking only works if members believe what they are shown will arrive.
- No new tab. Tab 2 now carries two panels.

## PRD figure: where the product sits (tab 2, third panel)

- `scripts/build-context-figure.py` writes `figures/product-in-the-system.svg`, a standalone
  vector figure for section 3 of the PRD, plus `figures/_panel.svg` which the extension
  generator embeds.
- Shows the product nested inside the Blue Rewards systems of record, nested inside BMO, with
  the member on one side, the five evidence authorities on the other, and the uncontrolled
  forces across the top. The scope boundary from section 5.2 is on the figure rather than in a
  paragraph.
- The page offers the file for download; SVG inserts directly into Word, Docs and PowerPoint.

## Working assumption register folded in (November 2026)

`SRC-ASSUMPTIONS-2026` added to the contract: eighty working assumptions prepared for BMO
confirmation. Assumptions, not findings, but several name mechanisms the map was missing.

- **The learning loop cannot currently close.** D23: no single record links a recommendation
  exposure to later activation, qualification, posting and redemption. K2: the funnel is not
  reported end to end for every route. K4: incremental activity cannot be separated from
  activity that would have happened anyway. Engagement to decisioning is now Contested in both
  views — not unproven, unmeasurable.
- **Ranking already exists.** D20 names an existing ordering, `collectorrelevance`, whose inputs
  are undocumented for this project. The product would make ranking visible, not introduce it.
- **O12 confirms the commercial-bias risk** the consequence analysis derived independently: a
  control is needed to stop partner payments or BMO product economics overriding the member's
  stated objective. Nobody owns it today.
- **D27 is a hard boundary.** Partner issuance, redemption and reversal services cannot be
  called under a member's session. Added to the PRD figure's scope panel.
- **D9 makes the four clocks a data gap**, not only a conceptual one. Friction to Available Value
  moves to Supported.
- **D16 and D28** describe current-state recovery: reversals match only for deeply integrated
  partners, and support assembles the history by hand across systems.

## Contact centre data from the client (November 2026)

`SRC-OPS-2026`: calls offered, answered and abandoned, service levels, handle time and the top
five contact drivers for Q2 to Q4 2026. Answered plus abandoned equals offered in every quarter.
Second empirical source in the map and the first operational one.

- **92,706 contacts abandoned across three quarters**, 22,006 in Q4 and still 22 per cent of
  calls offered. Members with a problem who stopped trying, leaving no case record. The doubt
  brake, quantified.
- **Access, not rewards, dominates the contact mix.** Email and password 31.3 per cent of Q4
  answered calls, website navigation 7.0 per cent — 38.3 per cent together, growing 2.5 and 4.0
  times since Q2. Reward inquiries and eGift cards together 14.6 per cent. Added as a sixth
  card in the consequence analysis, because the product's scope addresses the smaller share.
- **Fourteen-minute average handle time**, barely moved while speed of answer halved, which
  points at the investigation rather than the queue — consistent with assumption D28.
- Gives the "visibility raises support load" prediction a baseline: roughly 6,600 reward
  contacts and 1,550 agent-hours in Q4.

## Data pipeline folded in (November 2026)

`SRC-PIPELINE-2026`. The pipeline's recorded-activity chain is the remedy for the measurement
gap the assumption register exposed, so the two now reference each other.

- The three pilot measures are attached to the value stages they actually measure: Opportunity
  Capture Rate on the movement out of Opportunity, Earned Value Realization Rate on Earned Value
  through to receipt, End-to-End Realization Rate on the whole chain. The stages and the
  measures are the same structure.
- Engagement to decisioning stays Contested, but the note now says why: the chain does not exist
  today, and the pipeline is the designed fix, not an absence of a plan.
- The pipeline's seven boundary decisions (deferred, conditional, excluded) are recorded in the
  contract's boundary block.
- The PRD figure gains a measures row and the D27 line in the scope panel. Canvas is now
  1700 x 1215.
