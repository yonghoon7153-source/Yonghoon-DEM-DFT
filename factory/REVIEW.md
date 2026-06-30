# factory/ — External Review Bundle

*For external reviewers. Self-contained; pairs with `README.md` (architecture) and the b2o3/sc2o3 cards.*

## What this is
`factory/` is an autonomous, **in-silico report-card validation pipeline** for (doped) solid electrolytes (SEs). Given a composition that the upstream screening "cascade" nominated, it orchestrates our existing DFT/MLIP instruments (BVSE → MLIP-MD conductivity → ESW → SEI gaps → convex hull → elastic/EOS → DOS/charge → phonons → XPS/Raman/NMR fingerprints) and emits **one standardized "electrochemical report card"** (JSON + Markdown) per system. Every section is self-describing — `status` / `confidence (A/B/C)` / `method` / `source` / `caveats` — and a strict provenance rule (a section's `source` lists only files the assembler actually opens; hand-curated scalars are flagged `curation:manual`) prevents over-claiming. It is **computation + testable-prediction only**; real CV/EIS/cycling are out of scope. Exemplar: `b2o3` (a B₂O₃-doped LPSCl1.6 champion). Generalization demo: `sc2o3` (cascade rank-1 dopant, not yet validated).

## Schema / section overview
Contract: `schema/report_card.schema.json` (JSON-Schema Draft 2020-12; both cards validate clean — enforced by `test_factory.py`). Shared `section_with` def: `status` ∈ done/pending/partial/n.a., `confidence` ∈ A/B/C/null, `method`, `source`, `caveats`.

| Section | Key fields | Conf (b2o3) |
|---|---|---|
| `screening` | cascade source_pipeline/candidate_id, rank, score, descriptors, fast estimates | C |
| `transport` | σ300/σ273 (mS/cm), Ea, D0, BVSE barrier (val², not eV) | B |
| `thermodynamic_stability` | e_above_hull (meV/atom), decomposition | B |
| `electrochemical_window` | red/ox/window V, sei_products (all, leaky-first), sei_min_gap (predicted-only), thresholds | B |
| `mechanical` | B/G/E/ν, EOS B0 proxy | pending |
| `electronic` | band gap, N(E_F), VBM character (curated) | B |
| `structure_chemistry` | coordination motifs, bond lengths, Bader oxidation states | A |
| `dynamical_stability` | imaginary modes, verdict | B |
| `testable_predictions` | XPS / Raman-IR / NMR fingerprints | B |
| **Roadmap (n.a.)** | anode-interface, critical-current-density, grain-boundary, air/moisture, electronic-conductivity | n.a. |

**Confidence rubric:** A = DFT, converged, multi-witness or experiment-validated · B = single-config DFT/MLIP or relative-only · C = fast proxy/screening descriptor.

Two scripts: `assemble_report_card.py` (per-system file map in `SYSTEMS`; data-aware — a section is "done" only if its source data loaded, else a clean pending stub) and `orchestrate.py` (scheduler/gatekeeper: diffs done-vs-pending, plans pending stages with backend/cost/gate/exact-command, writes a provenance manifest; no auto-execute; human-in-loop `prep`/`cost`/`rank` gates). `test_factory.py` is a CI guard (builds + schema-validates every system + checks no cross-system physics leakage).

## b2o3 exemplar — headline results
- **Transport:** σ300 ≈ **18.5 mS/cm**, σ273 ≈ 8.7 (MLIP NE). Ea = **0.223 eV — identical to undoped** at the consistent 2–50 ps window; the ~1.33× gain is **D0-driven (prefactor), not a lower barrier**.
- **Thermodynamics:** metastable, **+37.5 meV/atom**, but a real phonon-stable phase. Decomposition independently predicts **Li₃BS₃ (BS₃ thioborate) + Li₄B₇ClO₁₂** — corroborating the motif.
- **ESW:** **NARROW, 0.31 V** (red 1.72 / ox 2.03) — a real risk. SEI is **mixed**: wide-gap passivators (B₂O₃ 8.4, BPO₄ 7.0, Li₃PO₄ 5.7) alongside leaky members in the *same* decomposition (Li₃BS₃ 3.05, Li₂B₂S₅ 2.44, Li₃P 0.7). `sei_min_gap` = 3.05 eV (predicted products only).
- **Structure (grade A):** trigonal **BS₃ confirmed 5 independent ways** (coordination / hull / DOS / ESW / Bader) = multi-witness; bond lengths + Bader oxidation states parsed from source.
- **Dynamical:** 0 imaginary modes (Γ MLIP) → dynamically stable.
- **Mechanical:** EOS B0 = 24.5 GPa (+13% vs undoped); full elastic Cij **pending on KISTI**.

## Honesty caveats (carried in the card)
- Absolute σ is an **MLIP upper bound** (~3–5× over LPSCl); cite **Ea (±0.01 eV) + ratio**, not absolute σ.
- BVSE barrier is **softBV val², not eV** — relative pre-screen, needs NEB calibration.
- Electronic scalars are **curated (GGA, single-config)** → grade B; gap GGA-underestimated.
- ESW passivation is **NOT demonstrated** — interphase morphology / e-tunneling not modeled.
- **Single Li-configuration**; bulk σ ≠ total σ (no grain boundaries).

## Known limitations & roadmap
Not computed (shown as `n.a.`): **anode-interface stability** (Li-metal reduction at the 1.72 V lower limit — headline risk), **critical current density / dendrite**, **grain-boundary transport**, **air/moisture (H₂S)**, **electronic conductivity / self-discharge**. Next: v1.2 new-composition end-to-end; v2 surrogate-AI active learning to pre-screen and cut compute.

## Open questions for reviewers
1. **Descriptor completeness:** Is the section set enough to call a candidate "validated," or are the roadmap items (esp. **anode-interface** and **CCD/dendrite**) blocking gaps that must leave `n.a.` before any recommendation?
2. **Confidence calibration:** Are the A/B/C definitions sensible — esp. **A for structure_chemistry** (5-way multi-witness) and **B as the ceiling for MLIP-MD transport** given the 3–5× absolute-σ error?
3. **Cascade coupling:** Is **versioned loose coupling** (re-link by `version`+`candidate_id`) the right architecture? Is reporting `rank_combined/combined_score` from one file (with divergent `ranked.csv #6` noted) the right honesty stance?
4. **Reuse:** Is the per-section `status/confidence/method/source/caveats` contract reusable across SE chemistries (oxides, halides, other thio-systems), or over-fit to LPSCl-family sulfides?
5. **ESW honesty:** Is `sei_min_gap` over **predicted-decomposition products only** (excluding won't-form phases like BS₂) correct, and are the heuristic passivation thresholds (≥4 passivating, ≥2 marginal) defensible to publish as rules-of-thumb?
6. **Orchestration:** Are human-in-loop **prep/cost/rank** gates + a plan-only (no auto-execute) orchestrator the right autonomy level for paper-grade trust? Is the provenance manifest enough to reproduce a card from `db/` state?

## Readiness checklist
**MUST-FIX before external review — DONE** (verified by `test_factory.py`):
- [x] Cross-system leakage: a not-yet-validated system (`sc2o3`) no longer reports false `done` or b2o3-specific physics — deep sections are clean pending stubs (no leaked verdict/XPS/motif/threshold). CI guard added.
- [x] Schema/card field-name alignment (`oxidation_states_bader_net`); `n_atoms` allows null; card validates.

**NICE-TO-HAVE (open):**
- [ ] Mirror `registry/stages.yaml` and `orchestrate.py STAGE_META` from one source (currently duplicated).
- [ ] Surface `D0_cm2_s` in the `to_md` transport table (JSON-only today).
- [ ] Document the loader key-unwrap convention (`{sysid}_doped` / system-id JSON keys) so 2nd-system db files use matching top-level keys.
- [ ] Declare `jsonschema` as a dev dependency; wire `test_factory.py` into CI.
- [ ] Consider `additionalProperties:false` on `section_with` once field names are frozen.

## External peer-review outcome (acted on)
A skeptical SE-domain peer review (verdict: **Major revision** for both the pipeline-as-method and the b2o3 finding) drove a second honesty pass. **Fixed in-card/in-repo:**
- [x] **`sei_min_gap` data defect** — now computed over hull **∪ voltage-resolved** reduction/oxidation products → **1.08 eV (BP, leaky)**, not the rosy 3.05; the reduction interphase is reported LEAKY (BP 1.08 / Li3P 0.7), "compensated" dropped.
- [x] **Phonon over-claim** — verdict downgraded to "no Γ instabilities (necessary, not sufficient)"; the kb note's retracted Ea=0.207 corrected to 0.223 (=undoped) and the soft-lattice→lower-barrier inference removed.
- [x] **Confidence recalibration** — structure_chemistry A→B ("BS3 5 ways" → ~2 correlated witnesses + literature); framing reworded to "SCREENED candidate, NOT validated"; README scoped to "provenance-disciplined assembly + plan-only layer" (no autonomous/UQ over-claim).

**MUST-DO before any positive recommendation (needs compute):**
- [ ] **ANODE-INTERFACE stability (decisive)** — run `interface_reactivity_v2.py` open to a Li-metal reservoir; the reduction front likely makes b2o3 Li-metal-unstable (BP/Li3P leaky). Until then: "interface UNASSESSED".
- [ ] **Transport error bars** — multi-seed MD; b2o3 high-T 100 ps parity; jump-stats to substantiate "D0-driven".
- [ ] **Finite-q phonon** (supercell/DFPT) before any "dynamically stable" claim.

*Three independent reviews drove this: two background CODE audits (rounds 1-2; 5/6 prior HIGH fixes RESOLVED + generalization fixed/regression-guarded) and one external SCIENCE peer review (the in-card honesty above). The framework's value is exactly this: it surfaced its own over-claims for correction.*
