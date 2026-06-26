# Li6PS5Cl (LPSCl) electrolyte parameters — literature (Stage-4 DFN inputs)

Background research agent digest (2026-06-24).  ⚠ Proxy blocked full-text (403 on all
publisher CONNECTs) → values from search snippets of the primary sources + project conventions.
Every value carries a source.  These feed the Stage-4 DFN electrolyte model AND confirm the
Stage-2 voxel-solver SE σ (= 3.0 mS/cm, already used).

## Ionic conductivity (RT ~25 °C)
| condition | σ_ion | source |
|---|---|---|
| single-crystal / grain-interior (project value) | **3.0 mS/cm** (Cronau adopted) | Cronau 2021 ACS Energy Lett. doi:10.1021/acsenergylett.1c01299 ⚠ exact single-crystal digit NOT verified (proxy) — verify from ACS PDF before manuscript |
| cold-pressed pellet (robust bracket) | **1–3 mS/cm** | Boulineau 2012 (1.33), Frontiers 2021 (dry 2.39 / wet 1.0–1.9) |
| densified / sintered / annealed | **3–6 mS/cm** (up to 6.11) | Yu 2018 (3.15→4.96), Zhou 2020 (6.11) |
- Key: measured (cold-pressed) σ UNDER-estimates true bulk by ~1 order at low stack pressure
  (GB + contact resistance) → >50 MPa needed for reliable σ (Cronau 2021).  Mirrors our DEM
  σ_grain=3.0 × Cronau(r_SE) GB factor.

## Density
- **1.64 g/cm³** theoretical (argyrodite cubic F-43m; Yu 2018 + Ampcera/MSE datasheet).
  Pellet apparent density lower by porosity (cold-press ~80–90 % of theoretical).

## Transference number (single-ion)
- **t₊ ≈ 1** — only Li⁺ mobile; [PS₄]³⁻/Cl⁻ framework fixed (Deiseroth 2008 doi:10.1002/anie.200703900).
- electronic σ_e ≈ **2.2–2.9 × 10⁻⁶ S/cm** ≪ σ_ion ~10⁻³ → ~99.9 % ionic (Frontiers 2021).
  → DFN: single-ion electrolyte (t₊=1), no convection; σ_e tiny but matters for interphase growth.

## Activation energy (Arrhenius σ = A·exp(−Eₐ/k_BT))
- pure LPSCl **0.2–0.36 eV** (0.16–0.20 highly crystalline/annealed; ~0.33 ball-milled microcrystalline).
  Boulineau 2012 (~0.33), Yu 2018 (0.32–0.36), Frontiers 2021 (0.20–0.245).

## Sources
Cronau 2021 (doi:10.1021/acsenergylett.1c01299) · Deiseroth 2008 (doi:10.1002/anie.200703900) ·
Frontiers Chem. 2021 (doi:10.3389/fchem.2021.778057, PMC8717468) · Yu 2018 (doi:10.1021/acsami.8b07476) ·
Boulineau 2012 (doi:10.1016/j.ssi.2012.06.008) · Zhou 2020 (doi:10.1021/acs.nanolett.0c02489).
