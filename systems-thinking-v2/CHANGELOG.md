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

## Updated Systems Map (tab 9, November 2026)

A second map rather than an edit of the first: the September map stays exactly as the team
knows it, and the revised structure sits beside it.

- **Value can now move backwards.** The developer portal carries `transactionType: RETURN` and
  the issuance interfaces support reversals, so a posted award can be removed after it arrives.
  Three edges are drawn as value leaving the forward chain and styled accordingly, with a new
  legend key.
- **Correction and recovery** is a node with seven connections. The six requirements that had
  nowhere to act — FR15, FR16, FR17, FR29, FR36, FR37 — act here.
- **Five evidence authorities** replace the single partner box in this view: offer sponsor,
  merchant and point of sale, card issuer and network, affiliate and receipt processing, reward
  supplier and fulfilment. Finding F08: one failure the member experiences can belong to any of
  them, and deciding which is what FR15 to FR17 do.
- **Saved and activated offers** sits between Potential Value and Earned Value, taken from the
  Offer Service's own member states (SAVE/SAVED/UNSAVED, OPT_IN/OPTED_IN). It is a recorded
  position, not a sixth kind of value.
- Adds `SRC-DEVPORTAL-2026-09` to the contract as technical documentation, not member evidence.
