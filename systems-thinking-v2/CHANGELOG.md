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
