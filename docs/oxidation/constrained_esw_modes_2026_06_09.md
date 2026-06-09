# constrained ESW — three modes, three things they each tell you

**Date 2026-06-09.** Followup on the Cl-scan, after running `--mode=leading`, `--mode=relax`, `--mode=hybrid` of `tools/oxidation/constrained_esw.py`. Honest assessment of what each mode does well, what it gets wrong, and what would be needed to match Gil-González's absolute K_eff=20 GPa anodic limit (~4.3 V for LPSCl1.5).

## TL;DR

| Mode | Composition-resolved edges? | Product-set switching detected? | Absolute V vs Gil-González K=20 | Recommended use |
|---|---|---|---|---|
| **leading** | ✅ Cl-rich widens more (modelc widest, 3.30 V at K=20) | ❌ keeps K=0 onset rxn | underestimates (modelc 3.11 V vs Gil 4.3 V) | **headline trend figure** (Cl-scan reproducing Gil-González Fig 1a qualitatively) |
| **relax** | ❌ all comps identical edges (1.24→2.26 at K=0; collapses to 0.51→0.83 width 0.32 at K=20) | ✅ correct: anodic switches to **Li2PS3 + LiCl + S + Li** at K>0 (Gil-González Table S1 form) | irrelevant (widths collapsed) | **product-set diagnostic only** |
| **hybrid** | ✅ at K=10 (modelc 2.69 anodic, comp1 1.97) | ✅ switched rxn detected | breaks at K=20 (width turns negative because reduction edge crosses oxidation edge — leading-order formula breaks when K·ΔV/n_e is large) | **K_eff ≤ ~10 GPa intermediate range**, not K=20 |

**No single mode gives both the right physical absolute voltages AND the composition-resolved widening across the full K_eff range** in our current implementation. To match Gil-González's K=20 LPSCl1.5 anodic at 4.3 V we would need a fourth mode: SE registered as a phase in the hull with its own DFT energy (our EOS E0 + V0) so the hull encodes composition-specific stability, not just hull-equilibrium at the composition.

## Mode 1 — leading

**Formula.** φ_ox(K) = φ_ox(K=0) + K · ΔV_ox / n_e_ox, where ΔV_ox and n_e_ox come from the K_eff=0 onset reaction. Mirror formula for φ_red(K), with the opposite sign.

**Strength.** The composition-dependent quantity ε_RXN = ΔV/V_SE is computed per composition: LPSCl0.5 ε = −0.086, LPSCl1.0 −0.036, LPSCl1.5 +0.013, modelc +0.023, LPSCl2.0 −0.019. Sign flip at Cl ≈ 1.3 and turn-over at Cl=2.0 give the right qualitative trend (modelc Cl=1.6 is at the sweet spot).

**Limit.** The K=0 onset reaction is `Li6PS5Cl → Li3PS4 + LiCl + S + 2 Li`. At K_eff > 0 the true Fitzhugh minimisation would replace this with `Li6PS5Cl → Li2PS3 + LiCl + 2 S + 3 Li` (P5+ → P3+, S released, ΔV more negative) because the new product set has lower (G_chem + K·V) total. Leading-order does NOT see this switch; it just shifts the K=0 line. So absolute K=20 voltages are pessimistic (modelc 3.11 V where the full method would put it higher).

**Verdict.** Best mode for the headline qualitative Cl-scan plot. Already in `docs/oxidation/constrained_esw_cl_scan_2026_06_09.md`.

## Mode 2 — relax (augmented hull, full re-min)

**Method.** At each K_eff, rebuild a `PhaseDiagram` from `(comp_i, E_i + K_eff·V_i)` for every solid phase; Li metal stays unaugmented (open-element reservoir). Re-run `get_element_profile(Li, comp)` and read the breakpoint voltages and reactions.

**Strength.** The reaction switching is correctly detected at K>0:

| Composition | K=0 anodic rxn | K=10/20 anodic rxn (re-min) |
|---|---|---|
| LPSCl0.5 | Li3PS4 + 0.5 LiCl + 1.5 S + 3 Li | **Li2PS3** + 0.5 LiCl + **2.5 S** + 4 Li |
| LPSCl1.0 (comp1) | Li3PS4 + LiCl + S + 2 Li | **Li2PS3** + LiCl + **2 S** + 3 Li |
| LPSCl1.5 | Li3PS4 + 1.5 LiCl + 0.5 S + Li | **Li2PS3** + 1.5 LiCl + **1.5 S** + 2 Li |
| **modelc** | Li3PS4 + 1.6 LiCl + 0.4 S + 0.8 Li | **Li2PS3** + 1.6 LiCl + **1.4 S** + 1.8 Li |
| LPSCl2.0 | 0.5 P2S7 + 2 LiCl + 0.5 S + 3 Li | **Li2PS3** + 2 LiCl + S + Li |

Every composition switches its anodic reaction at K=10 (or earlier) from `Li3PS4 + S` to **`Li2PS3 + LiCl + S`** (P5+ → P3+, more S released, more Li returned). This product set is exactly the form Gil-González SI Table S1 reports for LPSCl1.5 at K_eff=20 GPa (their products `SCl4 + Li2PS3 + S` differ in the Cl-bearing molecule but share Li2PS3 + S; they include SCl3/SCl4-flavour phases we excluded per their phase-set policy).

**Limit.** The breakpoint voltages — what `get_element_profile` returns as edge V — turn out **composition-INVARIANT** in this mode: every composition gives the same 1.24 → 2.26 V at K=0 and the same 0.51 → 0.83 V (width 0.32) at K=20. This is correct behaviour from the augmented-hull definition: when every solid is augmented by `K·V_i`, the *μ_Li* at which phases swap is shifted by the same per-electron amount, so phase boundaries (= our edges) move rigidly. The composition-dependent part is the **distance from the parent hull to the augmented hull**, not the breakpoint voltage. We aren't reading that distance.

**Verdict.** Run it to confirm the product-set physics (anodic switches to Li2PS3+LiCl+S; reduction stays on Li2S/LiP path). Do NOT report its edge voltages as composition-resolved.

## Mode 3 — hybrid

**Method.** Use mode 2 to detect the switched anodic / cathodic reaction at each K_eff. Then apply leading-order shifts using the SWITCHED reaction's ΔV and n_e:
- φ_ox(K) = φ_ox(K=0) + K · ΔV(switched_ox)/n_e(switched_ox)
- φ_red(K) = φ_red(K=0) − K · ΔV(switched_red)/n_e(switched_red)

**Strength.** At K_eff = 10 GPa the result is sensible and composition-resolved:

| | LPSCl0.5 | LPSCl1.0 | LPSCl1.5 | **modelc** | LPSCl2.0 |
|---|---|---|---|---|---|
| φ_ox K=10 | 1.78 | 1.97 | **2.45** | **2.69** | 1.99 |

modelc anodic is 2.69 V, exceeding LPSCl1.5 (2.45) and the Cl-poor compositions. Same qualitative Cl-rich-rises-most behaviour as leading mode. The switched anodic rxn for comp1 `Li2PS3 + LiCl + 2 S + 3 Li` has ΔV = −33.9 Å³, n_e = 3, so `K·ΔV/n_e = K·(−0.071) V`, giving a 0.71 V drop at K=10, but applied on TOP of leading-order +0.42 V shift at K=10 from the K=0 onset's strain term — net is the 1.97 V we see.

**Failure mode.** At K_eff = 20 GPa the switched rxn's `K·ΔV/n_e` shift saturates / overshoots: for LPSCl1.0 the shift is K(20)·ΔV(−33.9)/n_e(3) = −2.26 V on top of the K=0 onset 2.26 V → φ_ox K=20 = 0 V. Meanwhile reduction edge moved up to 2.77 V (its own switched rxn has very different ΔV/n_e). Result: **reduction edge > oxidation edge, width turns negative** (−1.93 V). This is the formula breakdown: leading-order `φ += K·ΔV/n_e` is valid only when `K·ΔV/n_e ≪ φ`; in this regime the assumption that the K=0 onset stays linear ceases to hold.

**Verdict.** Useful for K_eff up to ~10 GPa where the shifts stay in the linear regime. Do NOT use K=20 GPa hybrid numbers.

## Why none of the three reaches Gil-González 4.3 V

Gil-González's LPSCl1.5 at K_eff=20 GPa with anodic limit 4.3 V uses a method we are NOT doing: they **register the SE itself as a phase** in their phase diagram, with its DFT energy at its DFT volume. Then the augmented hull `E_i + K·V_i` calculation MUST go through the SE entry to decompose it, and the SE entry's `+K·V_SE` term competes against the product set's `+K·Σ_products V_i`. That competition is what gives the `K·(V_products − V_SE) = K·ε_RXN·V_SE` term WITHIN the breakpoint voltages — composition-resolved and absolute-value-accurate at the same time.

Our implementation treats the SE as a composition at the hull (we never have an MP entry for modelc; we use `Composition` only). So we never get the SE's volume into the phase-boundary calculation, and we have to add the strain term as a leading-order edge shift externally — which gives qualitative-right but quantitative-pessimistic answers.

To close that gap, mode 4 ("SE-as-phase") would need:
- our own DFT E0(V0) for each composition (we have it: `db/properties/eos.json` comp1_v3 E0 = -13917.89 eV @ V0=1016.62 Å³; modelc_v3 has V0=1216.44 but no committed E0 in eos.json — would need to be added from `container:.../modelc_BM_EOS_results.json`),
- register `PDEntry(comp, E0)` for each SE,
- augment its energy by `K·V0_DFT` per K_eff,
- run `get_element_profile` — the SE entry is now part of the hull, and the breakpoint voltage at which it decomposes is composition-specific because its `E0` and `V0` are composition-specific.

This is implementable; not done in this session.

## What to report in the paper / SI

1. **Headline Cl-scan plot:** leading mode (already in `constrained_esw_cl_scan_2026_06_09.md`). Cl-rich widens more, modelc at sweet spot.
2. **Product-set switching (SI):** relax mode reactions table above. Cite as "the constrained decomposition products at K_eff > 0 switch from Li3PS4+S to Li2PS3+LiCl+S, consistent with Gil-González Table S1."
3. **Hybrid result (SI, with caveat):** report K_eff = 0 and 10 GPa hybrid numbers (good); skip K_eff = 20 hybrid because the leading-order formula breaks.
4. **TODO (paper revision / response to reviewer):** SE-as-phase mode 4 if a reviewer asks for absolute-V match to Gil-González.

## Run artifacts

- `constrained_esw_cl_scan.json` — leading mode (gabia path `/data/work/repo/`).
- `constrained_esw_cl_scan_relax.json` — relax mode (gabia path same).
- `constrained_esw_cl_scan_hybrid.json` — hybrid mode (gabia path same).
- Tool `tools/oxidation/constrained_esw.py` supports `--mode {leading,relax,hybrid}` since commit on 2026-06-09.
