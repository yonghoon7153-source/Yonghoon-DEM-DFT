# comp4 v2 Adhesion → Narrative Pivot (2026-05-10)

> v15 fair comparison (v1_slab REDO vs v2_slab) reveals comp4 v2 anneal champion
> is NOT anomalous — it's MORE correct than v1 paper figure values. The previous
> "Cl-O density anti-correlation" main descriptor was a sampling artifact.
> ROBUST descriptor: **R(S-Li density vs paper Wad) = -0.896**.

---

## 1. Background

Paper #2 figure 2 (Interface bond densities + paper exp Wad) used hardcoded
`BOND_DATA` in `tools/plot_bond_densities_v9.py`, original from a v15 run on
KISTI. Main narrative: ==R(Cl-O density) = -0.914== anti-correlation with
paper Wad — "Cl atoms at SE surface repel NCM oxygen, less Cl exposure
correlates with stronger adhesion."

When we updated comp4 to v2 anneal champion (rank2_anneal_3.xyz cross-rank,
E=-255.6596 eV, 246 meV gain over h_E_lbfgs), all R values shifted:
- R(Li-O) +0.819 → +0.323
- R(Cl-O) -0.914 → +0.134 (sign flip!)
- R(Br-O) +0.394 → +0.234

This raised the question: "Is comp4 v2 weird?"

## 2. Verification — comp4 v2 is NOT weird

### Step 1 — Fair v1 vs v2 baseline

We re-ran v15 with comp4 **v1 slab** in current ASE/numpy environment
(`phase2a_v15_v1_REDO_results/`). Compared to v2 results
(`phase2a_v15_v2_results/`):

| comp | v2 - v1_REDO (Li-O / Cl-O / Br-O density) |
|---|---|
| comp1 | 0.0000 / 0.0000 / 0.0000 |
| comp2 | 0.0000 / 0.0000 / 0.0000 |
| comp3 | 0.0000 / 0.0000 / 0.0000 |
| **comp4** | **-0.0485 / +0.0881 / -0.0581** |
| comp5 | 0.0000 / 0.0000 / 0.0000 |
| modelC | 0.0000 / 0.0000 / 0.0000 |

✅ ==**Only comp4 changed**==. Other 5 comps' slabs unchanged → identical
output. v2 anneal champion produces a DIFFERENT comp4 slab with Cl exposed
at the SE-NCM interface.

### Step 2 — Old hardcoded vs v1_REDO drift

| comp | hardcoded (paper figure) - v1_REDO |
|---|---|
| comp1 | -0.0009 / -0.0019 / 0 |
| comp2 | -0.0019 / -0.0007 / 0 |
| comp3 | -0.0034 / 0 / 0 |
| comp4 | +0.0093 / 0 / +0.0032 |
| comp5 | +0.0027 / 0 / -0.0018 |
| modelC | +0.0095 / +0.0067 / 0 |

→ Small drift (0.001-0.01 = 1-10%) reflects ASE/numpy/script version
difference between paper figure date and current run. Not significant for
narrative.

### Step 3 — Anneal champion robustness

comp4 v2 champion validation:
- Cross-rank: 5 ranks × 5 anneal trajectories = 25 candidates → champion
  rank2 starting → rank3 Li11 final at E=-255.6596 eV
- Anneal gain vs h_E_lbfgs (-255.4138): **+246 meV** (substantial)
- V0 BM3 fit: V0 = 1253.10 Å³, B0 = **20.77 GPa** (within 0.03 GPa of v1
  paper 20.8 GPa) — EOS unaffected
- V0 relax max atom displacement vs v104: **8 mÅ** (negligible)

→ comp4 v2 is the proper anneal champion. The Cl-exposed surface in v2 is
the TRUE Li5.4PS4.4Cl0.8Br0.8 surface termination, not a bug.

## 3. R(S-Li) = -0.896 — what it really means (CORRECTION)

| descriptor | R(v1_REDO) | R(v2) | robust? |
|---|---|---|---|
| Li-O | +0.819 | +0.323 | NO |
| Cl-O | -0.914 | +0.134 | NO (sign flip) |
| Br-O | +0.394 | +0.234 | weak both |
| **S-Li** | **-0.896** | **-0.896** | ==**family-binary classifier**== |

### Per-comp S-Li density (KISTI v15 results)

| comp | family | S-Li density (Å⁻²) | paper Wad (mJ/m²) |
|---|---|---|---|
| comp1 | Li6 | 0.0500 | 194 (low) |
| comp2 | Li6 | 0.0419 | 180 (low) |
| comp3 | Li5.4 mix | **0.0000** | 316 (high) |
| comp4 | Li5.4 mix | **0.0000** (v1=v2) | 298 (high) |
| comp5 | Li5.4 mix | **0.0000** | 249 (high) |
| modelC | Li5.4 Cl | 0.0249 | — |

==**Critical clarification**==: R(v1)=R(v2)=-0.896 is identical NOT because
S-Li is "Li-ordering invariant" — it's because comp4's v1→v2 surface change
(Cl exposed) didn't involve S-Li bonds. Comp4 is S-Li=0 in BOTH.

S-Li density is fundamentally a ==**Li6 vs Li5.4 mix family-binary
classifier**== (Li6 family has S in SE coordinated to Li in NCM at gap_eq;
Li5.4 mix family does not). The R = -0.896 magnitude is driven by:
- Li6 family → S-Li > 0 → low paper Wad
- Li5.4 mix family → S-Li = 0 → high paper Wad

Both Cl-O (v1) and S-Li are family-binary classifiers. The difference:
- Cl-O classifier BROKE in v2 (comp4 anneal exposed Cl → Cl-O > 0 in
  Li5.4 mix family)
- S-Li classifier SURVIVED v2 because comp4 anneal didn't change S-Li
  (which depends on full surface stoichiometry, not just halogen ordering)

→ Whether S-Li is truly Li-ordering invariant requires testing OTHER comps'
v2 anneal champions (comp3/comp5/modelC v2). For now, ==use S-Li as a
family-binary descriptor, NOT a continuous one==.

## 4. Paper #2 narrative pivot — recommended

### OLD narrative (paper figure 2)
- Main descriptor: R(Cl-O density) = -0.914
- Story: "Cl exposure at SE surface anti-correlates with adhesion"
- Problem: contingent on comp4 having Cl-O = 0 in v1, which is NOT the case
  in v2 anneal champion. Sampling artifact.

### NEW narrative (recommended, with caveats)
- Main descriptor: ==**R(S-Li density) = -0.896 family-binary classifier**==
- Story: "Li6 family exhibits S(SE)-Li(NCM) interfacial coordination
  (S-Li > 0); Li5.4 mix family does not (S-Li = 0). Family-binary classifier
  separating Li6 (low Wad) vs Li5.4 mix (high Wad)."
- ==Caveat==: NOT a continuous descriptor — comp3/4/5 all have S-Li = 0 so
  cannot distinguish within Li5.4 mix family. Cannot predict modelC Wad.
- ==Caveat==: comp3/comp5/modelC v2 anneal champions NOT YET tested. v1→v2
  invariance only verified for comp4. To claim "Li-ordering robust" we
  need v2 anneal champions for ALL Li5.4 mix members.

### What we lost in narrative pivot
- ==Cannot claim== "Cl-O density anti-correlates with paper Wad" (broken in v2)
- ==Cannot claim== "S-Li is Li-ordering robust descriptor" (only comp4 tested)
- CAN claim "Li6 vs Li5.4 mix family separation captured by either Cl-O (v1)
  or S-Li (v1=v2). v2 reveals Cl-O is fragile; S-Li survives this specific
  comp4 perturbation."

### Mechanistic interpretation (proposed)
- Li6 family (comp1, comp2): high Li density at surface → S-Li density high → low Wad (weak adhesion)
- Li5.4 family with Br (comp3, comp4, comp5): vacancies + Br lower S-Li at surface → less interphase → higher Wad
- modelC (Li5.4 pure Cl): mid S-Li → mid Wad
- comp4 v2 vs v1: v2's Cl exposure shifts S-Li / Cl-O balance, but TOTAL
  S-Li per area same → R(S-Li) preserved.

## 5. Action items

- [x] `tools/plot_bond_densities_v9.py` BOND_DATA updated to current v1_REDO
  values for all comps + comp4 v2 champion values
- [ ] Regenerate Figure 2 PNG with new BOND_DATA → S-Li bar added (currently
  Li-O / Cl-O / Br-O only)
- [ ] Update `db/properties/adhesion.json` with v1_REDO + v2 results
- [ ] Update paper #2 draft narrative (Cl-O → S-Li)
- [ ] Continue post-proc on V0: DOS / PDOS / Bader (running) → bond length

## 6. Files

| File | Content |
|---|---|
| `output/comp4_v2_BM3_fit.json` | EOS BM3 fit (B0=20.77 GPa) |
| `output/comp4_v2_adhesion/comp4_v2_adhesion_summary.json` | v15+v30u summary |
| `output/comp4_v2_adhesion/v1_v2_REDO_comparison.json` | this comparison data |
| KISTI: `phase2a_v15_v1_REDO_results/results.json` | v1 baseline (current env) |
| KISTI: `phase2a_v15_v2_results/results.json` | v2 (anneal champion) |
| KISTI: `phase2a_v30u_v2_results/summary.json` | UMA Z-scan W_max R=+0.964 |

---

#paper2 #comp4 #v2 #anneal-champion #adhesion #bond-density #narrative-pivot #S-Li-descriptor #robust-descriptor
