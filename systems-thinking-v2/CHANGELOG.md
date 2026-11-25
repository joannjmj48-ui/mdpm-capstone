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

## Inherited programme history (November 2026)

Legacy AIR MILES collectors are now on the Current System view — as a structural condition beside
Interface friction, not as a fourth population, because a legacy collector is also a member-only
or member-client participant. What differs is their history.

Grounded in the complexity analysis: "some legacy AIR MILES status benefits continue under
transitional conditions. These are entitlements dependent on history, not merely current
balance." That is finding F06, and it is the one place the map's present-tense structure breaks
down — two members with identical balances can be entitled to different things.

Three relationships: judged against what it used to be worth (to Realized value, negative),
dormant balances and expiry (to Finance and risk, positive — the breakage brake at its most
concrete), and history decides what is on offer (to Meaningful engagement, negative).

`SRC-WEB-2026` records the secondary web summary as unverified. It contradicts itself on
conversion and expiry, so its unique claims — 24-month inactivity, Shell leaving, legacy tiers
ending 2027, Metro and Rexall unconfirmed — upgrade nothing on their own.

## Three named systems maps (November 2026)

- **1. Systems Map M1** — the Current System grid view.
- **2. Systems Map M2** — three panels: **Systems Map 2.0** (where the product sits, the figure
  prepared for PRD section 3, with SVG and PNG downloads), **What the evidence adds** (the
  November causal loop extension), and **What our product would do to the system** (the
  consequence analysis). 2.0 opens by default.

Everything below shifts as expected and ends at 9. Evidence and Requirements. Numbers live in
the generators; every module's cache key is bumped so a half-cached page cannot show two
numbering schemes at once.

## Systems Map 2.0 figure: plain-language pass (November 2026)

Rewritten so the figure answers its own questions.

- Added a purpose bar: what the figure shows, and the instruction to read it from the outside in.
- Title is now "Where our proposed enhancement would sit"; the strapline is "An enhanced
  experience within Blue Rewards".
- "The product" is named throughout: "What we are proposing to build", "this enhancement",
  "What this enhancement does not replace".
- "Evidence authorities" becomes "Who holds the proof". "Systems of record" becomes "where the
  official records live". "Owns no system of record" becomes "we would hold none of the
  official records".
- "What the programme cannot observe" now lists real examples, including the three programmes
  usability participants named themselves.
- "Recorded activity is evidence of programme interaction, not of a life" is gone, replaced with
  "what the programme records is what a member did inside it, not everything they bought or
  wanted".
- The measures carry a plain reading under each formula; the MDPM 830 caption is removed.

## Figure: name the BMO teams, and say why (November 2026)

- The BMO band now names the five teams rather than three generic functions. **Emerging Business**
  is marked in gold as the client, with Drew's team noted. Programme leadership, Cards and Credit,
  Data and Analytics and Finance and risk each carry the decision they hold.
- "Outside the boundary" loses its note. The band name already says nobody here controls it.
- The member band now says *why* the programme sees only part: it records what passes through a
  route that earns — a scan, a linked card, a receipt, a Shops click.
- Blue Rewards is described as the loyalty programme, not a store of records.
- Every line under "Who holds the proof" is elaborated into what that party actually knows, and
  the heading note explains why five parties matter: no single one sees a whole journey, so when
  value goes missing the proof is split between them.

## Figure: strip what a systems map should not carry (November 2026)

Removed: the purpose bar, the "everything around it already exists" line, the PRD framing in
the eyebrow, the "what the programme cannot observe" box, the route-that-earns note, and the
three pilot measures. The measures are a measurement model, not map structure; they stay on
the value states in the contract, where they belong.

Added: real examples under each outside-the-boundary force, pulled from the Outside the
Boundary view. Member is now "a member, a BMO client, or both". Title is Systems Map 2.0.
"Evidence arrives on their schedule" becomes "each reports on its own timetable", moved out of
the gap between two boxes.

## Figure: polarity, loops and downstream impact (November 2026)

- Every arrow now carries a sign, and the reporting arrow carries a delay bar. A notation key
  sits in the masthead.
- Three loops that cross the boundaries the figure draws: R1 relevance flywheel (no minuses,
  compounds), B1 liability brake (one minus, programme to Finance), B2 proof and doubt brake
  (one minus and a delay, member to the five parties holding the proof).
- "Who feels it downstream if this works" names four consequences by owner, drawn from the
  consequence analysis in Systems Map M2.
- Member expectations keeps its place outside the boundary, but the label now says why: formed
  by every other app they use, and not always realistic. We control what we deliver, not the
  standard members arrive with.

## Systems Map 2.0 restructured to the MMIE 884 pitch-deck pattern (November 2026)

Modelled on the Innovation Suite systems map: loops drawn as labelled ellipses inside the map
with their chain listed, and downstream stakeholders as a band across the bottom.

- **R1 Relevance flywheel** sits between the member and the core; **B1 Liability brake** between
  the core and the parties holding the proof; **B2 Proof and doubt brake** spans the width below
  the core, with dashed connectors from the member and from the proof column, because that is
  the loop that crosses both.
- **Impacted / downstream stakeholders** is now a band inside the figure: members, Finance and
  risk, support and operations, earn and redeem partners, Cards and Credit.
- Canvas is 2040 x 1546 to make room for the loops either side of the core.

## Leverage points on the figure (November 2026)

- The five converged leverage clusters from the Convergence tab are now marked on Systems Map
  2.0 with numbered gold badges at the point each one acts, and named in a strip beneath the
  map. Make realized value the goal acts on B1; connect the value states shortens the delay in
  B2; detect and resolve missing value is the recovery capability; treat consent as spendable
  caps R1; learn from realized outcomes is R1's return leg.
- The loop glyph inside each ellipse is a real circular arrow rather than a dashed circle.
- The B2 chain closes with "back to the start" instead of a dangling sign.

## The figure was missing its problem (November 2026)

Loops and leverage points had been added to Systems Map 2.0 without a stated problem for them
to explain, which left the leverage points unanchored: an intervention with nothing identified
to intervene on.

Added a problem band directly under the core:

> **Available value does not reliably become realized value.** Members miss opportunities worth
> having, cannot tell what they are owed, and give up when value goes missing.

With what each loop does to it: R1 should raise it but its return leg is unconfirmed, B1 holds
it down by limiting generosity, B2 holds it down by turning delay into withdrawal. The leverage
strip now reads "each one changes a loop above, which is the only way to move the problem."

## Core box: goal, then features (November 2026)

The box read feature, then programme statement, then feature again, then journey. It now runs
in one direction: what we are proposing &rarr; the goal &rarr; the five features we have so far
&rarr; the journey they support &rarr; what Milestone 3 settles.

- Removed "the only new records we would create", which claimed more certainty about the build
  than M3 allows, and the duplicated programme statement already carried by the band above.
- "Which of these we build, in what order and how far, is what Milestone 3 settles" replaces it.
- The problem band heading is now simply "The problem", and each loop names the variable it
  acts on rather than a dangling "it": R1 should raise realized value, B1 caps it, B2 drains it.

## Arrows around B1, and a two-column footer (November 2026)

- Both ellipses are shorter (ry 170), and the two dashed arrows to the evidence authorities now
  pass over and under B1 rather than through its text — the same treatment the member arrows
  already had around R1.
- Leverage points and what this does not replace sit side by side. Canvas 2040 x 1800.
