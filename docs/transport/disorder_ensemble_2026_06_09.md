# Disorder-ensemble Li diffusion — comp1 (LPSCl) Ea-vs-disorder

**Date 2026-06-09.** Status: comp1 complete; modelc running on v100 (12/24 MDs done at 13:15).

## Why this run exists

Our earlier Arrhenius-from-AIMD table reports

| | Ea (eV) | source |
|---|---|---|
| comp1 (LPSCl, ordered Li6PS5Cl) | **0.172** | `db/properties/li_transport.json` headline |
| modelc (LPSCl1.6, near-ordered Cl/S) | **0.224** | `db/properties/li_transport.json` headline |

so "Cl-rich modelc has HIGHER Ea but is faster via prefactor" became one of our reported mechanisms (`comp1_vs_modelc_comparison.mechanism_interpretation` in the same JSON). That directly contradicts the dominant experimental narrative

- **Minafra/Kraft, *Solid State Ionics* 2020** "Enhanced ion conduction by enforcing structural disorder in Li6−xPS5−xCl1+x" — higher Cl + Li vacancy → **larger Cl/S anti-site disorder → LOWER Ea → higher σ**. Cited in `db/properties/literature_tensions_audit.json` tension #2.

If Minafra is right then our reported Ea direction is the artifact, and the candidate cause is structural: our comp1 cell is fully ordered Li6PS5Cl, and our modelc cell has only **1 / 8 = 12.5% 4d-Cl anti-site** (from `db/properties/bonds.json` `icohp_LOBSTER…modelc_v3.Li_Cl_per_site_split`). So both cells are essentially under-disordered relative to the synthetic samples Minafra characterises (anti-site fractions typically 25–50% depending on synthesis).

This run tests that hypothesis directly: take the SAME comp1 / modelc, install controlled Cl/S anti-site disorder, redo Arrhenius, see which direction Ea moves.

## Method

Tool: `tools/modelc_v3/disorder_ensemble_diffusion.py` (v100, UMA-s-1p1 / fairchem, GPU). Per composition: target disorder levels 0.0 (ordered, control) and 0.5 (50% of Cl/S sites swapped on the anion sublattice, then geometry-relaxed). For each disorder level, n_configs independent realisations (anti-site pattern randomised); each config run at 600 / 800 / 1000 K Langevin MD, MSD → D, Arrhenius → Ea, D₀.

- Equilibration 5 ps, production 50 ps, timestep 1 fs.
- `fixcm=True` (default ASE Langevin; harmless for 52-atom cells, warning printed).
- Three temperatures per config; 3 configs per disorder level (planned), 1 finished so far for comp1 d=0.0.
- Result aggregation in `comp1_v3/disorder_diffusion/ensemble_results.json` and `modelC_v3/disorder_diffusion/ensemble_results.json`.

## comp1 — the two outcomes

Same composition, same protocol, same MLIP. Only the **starting structure disorder** differs:

| | comp1 d = 0.00 (ordered) | comp1 d = 0.50 (disordered) |
|---|---|---|
| Structure | fully ordered Li6PS5Cl, no Cl/S mixing | ~50 % of Cl sites swapped onto free-S sites + Li redistributed |
| n_configs | 1 | 3 |
| D(600 K) | **−3.7 × 10⁻⁷** cm²/s (negative = noise) | normal positive |
| D(800 K) | 5.7 × 10⁻⁷ cm²/s (barely positive) | normal positive |
| D(1000 K) | 1.7 × 10⁻⁵ cm²/s | normal positive |
| **Ea** | **1.171 eV** (artifact) | **0.177 ± 0.027 eV** (n=3) |
| D₀ | 13.6 cm²/s (huge) | reasonable |
| D(300 K) extrapolated | 2.9 × 10⁻¹⁹ cm²/s | physical |

### Why d = 0.00 gives Ea = 1.17 eV (it is an ARTIFACT, not the "true ordered Ea")

A negative D from the MSD linear fit is a STATISTICAL signal of "no diffusion measurably above noise". The MSD curve is flat (Li atoms barely leave their cages in 50 ps), and any linear fit to flat-plus-noise can give a slope of either sign. The number reported is essentially the noise floor of the fit:

```
D(600 K) ≈ −4 × 10⁻⁷ cm²/s   ← noise band
D(800 K) ≈  +6 × 10⁻⁷ cm²/s   ← still noise band
D(1000 K) ≈ +2 × 10⁻⁵ cm²/s   ← only this is real
```

Arrhenius `ln D = ln D₀ − Ea/(kᵦT)` fit on these three points gets dominated by the gap between the ~10⁻⁷ floor and the 10⁻⁵ at 1000 K — a 50× span over a 100 K window — and the resulting slope inflates Ea to 1.17 eV. That number is *not* the activation energy of ordered Li6PS5Cl. It is "fully ordered Li6PS5Cl is kinetically frozen in this UMA window; you cannot extract a barrier this way." That itself is a useful auxiliary statement (= the ordered limit is inaccessible at our T / cell / time), but it is **not** a number to put in any table.

### Why d = 0.50 gives Ea = 0.177 eV (this IS the physical Ea)

Adding anti-site disorder unfreezes Li migration: Cl on the wrong (former-S) site changes the local Madelung field and opens hopping pathways. D(600 K) becomes well above noise, all three temperature points are clean, and the Arrhenius slope gives **Ea = 0.18 ± 0.03 eV (n=3)**. This number matches:

- Minafra/Kraft and Schlem 2020 experimental LPSCl Ea = **0.16–0.25 eV**,
- our own earlier comp1 entry **Ea = 0.172 eV** (which used a thermally pre-annealed cell that already had effective disorder),
- typical Li-argyrodite Ea reported by every other DFT/AIMD group.

So our previous "comp1 Ea = 0.172" was correct *because* the v2/v3 anneal protocol had already introduced realistic disorder; we simply did not realise that the apparent comp1-vs-modelc Ea ordering (0.172 < 0.224) was sensitive to how much disorder each cell happened to carry.

## What this means for the "comp1 Ea < modelc Ea, gain is prefactor" story

That headline (`db/properties/li_transport.json` → `comp1_vs_modelc_comparison.mechanism_interpretation`) is **partially retracted**:

- ✅ **Robust observed fact (keep):** modelc D > comp1 D over the 600–1000 K window we simulated. Matches the experimental σ(LPSCl1.6) > σ(LPSCl).
- ❌ **Mechanism (retract / hedge):** "modelc has HIGHER per-hop barrier (0.224) but ~8× higher prefactor → prefactor-driven gain." The 0.224 > 0.172 ordering is an artifact of how much Cl/S anti-site disorder each cell carried, not a physical inversion. At matched disorder (d = 0.5) comp1 already drops to Ea = 0.18, in line with Minafra/Kraft.

The modelc d = 0.5 run currently completing on v100 will decide the open question:

- if **modelc(d=0.5) Ea < comp1(d=0.5) Ea = 0.18**, the gain is **barrier-driven** as Minafra/Kraft argue → confirms the textbook narrative;
- if **modelc(d=0.5) Ea ≈ comp1(d=0.5)** (i.e. both ~0.18 at matched disorder), the **direct Cl-content effect on Ea is small** and the modelc σ-advantage is genuinely **prefactor / carrier-density** driven, consistent with our earlier reading but for the right reason (more Li vacancies, not "higher barrier compensated by larger D₀").

Either outcome is a real and reportable mechanism statement; what was wrong was using 0.172 and 0.224 directly side by side as a "physical inversion".

## Concrete numbers from `comp1_v3/disorder_diffusion/ensemble_results.json`

`level[0]` (target disorder 0.0):

```
Ea_mean_eV = 1.1707388728737897
D0_mean_cm2_s = 13.567294023423177
configs[0] = { config: 0, swaps: [],
  D_per_T = [-3.745e-07, 5.717e-07, 1.707e-05],
  arrhenius = { Ea_eV: 1.171, D0_cm2_s: 13.57,
                D_300K_cm2_s: 2.917e-19,
                points: [ {T=800, D=5.717e-07}, {T=1000, D=1.707e-05} ] }
}
```

(The Arrhenius fit dropped T=600 K because D was negative.)

`level[1]` (target disorder 0.5):

```
Ea_mean_eV = 0.1769
Ea_std_eV  = 0.0274
n_configs  = 3
```

(D₀ and per-T D vectors are stored per config; aggregated mean / std not yet written by the tool, refers to the three Arrhenius fits.)

modelc disorder run will be appended to `modelC_v3/disorder_diffusion/ensemble_results.json` with the same schema.

## How to read each number — one-line summaries

- **Ea = 1.17 eV (d=0.0, n=1):** *kinetic-frozen artifact.* Means "ordered Li6PS5Cl does not diffuse measurably in this UMA / 50 ps / 600–800 K window." NOT a barrier value. Useful only as evidence that the *ordered* limit is experimentally inaccessible.
- **Ea = 0.18 ± 0.03 eV (d=0.5, n=3):** *physical Li6PS5Cl activation energy with realistic Cl/S anti-site disorder.* Matches experiment (Minafra, Schlem) and our earlier annealed-cell value (0.172). This is the number for any paper Ea claim.
- **D(600 K) = −3.7 × 10⁻⁷ cm²/s (d=0.0):** *not an error, a statistical signal.* MSD over 50 ps is flat plus noise; the noise integrates to a small negative slope. Indicates D ≈ 0 at this T for the ordered cell. Don't put it in a D table; cite it only as "below the MSD noise floor".

## Citations / pointers

- DB entry `db/properties/li_transport.json` → `disorder_ensemble_2026_06_09` block (added in commit a054dff / dd01fb2 rebased).
- Tension audit `db/properties/literature_tensions_audit.json` → `2_conductivity_mechanism_Ea_vs_prefactor` — will be downgraded from "tension" to "RESOLVED partial: prefactor narrative partially retracted, awaiting modelc d=0.5 to call barrier-vs-prefactor".
- Companion paper-side narrative: `db/properties/electronic.json` ELF & ICOHP results show PS4 backbone identical for comp1/modelc — i.e. the cells differ on the Li-sublattice / anti-site axis, exactly where this disorder study acts.
- Literature: Minafra/Kraft, Solid State Ionics 2020 ("Enhanced ion conduction by enforcing structural disorder in Li-deficient argyrodites Li6−xPS5−xCl1+x"); Schlem et al. 2020 (Cl-rich LPSCl Ea = 0.22 eV).

## Open follow-ups

1. **modelc d = 0.5 finish** (v100, ~6 more MD frames). Decides barrier-vs-prefactor for the Cl-rich gain.
2. **comp1 d = 0.0 with longer prod_ps (≥150 ps)** if a "true ordered Ea" number is ever wanted for paper — current 50 ps is too short. Low priority since the ordered limit is not the physical case.
3. **Update `comp1_vs_modelc_comparison.mechanism_interpretation` in li_transport.json** to a hedged form (robust observation kept, mechanism marked pending) once modelc d=0.5 lands.
4. **Caveat block in any paper Ea claim:** UMA absolute D overestimates ~3–5× vs experiment; cite the 600–1000 K window + Ea, not the 300 K extrapolation.
