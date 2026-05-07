# Adhesion v23-v25 Maximum Extraction — Complete (2026-05-07)

> Continuation of v9-v22 session. User direction: "narrative 제작보다 최대한
> 으로 뽑아낼 수 있는 부분을 뽑아내보자" — extract everything possible from
> current geometry before narrative crafting.

## Summary

| Version | Purpose | Key result |
|---|---|---|
| v23 | Statistical robustness (Pearson, Spearman, bootstrap, jackknife) | Cl-O density: R=-0.91 stable across all stats |
| v24 | Binding curve shape + multivariate + composition decomp | comp4/5 indistinguishable (Δ<0.005) |
| v25 | Bader-weighted + halogen z-dist + surface termination + collinearity | 6 collinear pairs confirm ~2 independent dim |

## v25 — Final extraction results

### Y1 Bader-weighted bonds: ❌ DEGRADES signal

Approximate Bader charges (Li=+0.85, S=-1.85, Cl=-0.91, Br=-0.89, O=-1.20, Ni=+1.45)
applied to bond counts as weighted attractive/repulsive/net descriptors.

| Descriptor | R vs paper exp | p |
|---|---|---|
| bader_attractive (Li-O × q) | -0.54 | 0.34 |
| bader_repulsive ((Cl,Br)-O × q) | -0.21 | 0.73 |
| bader_net | -0.11 | 0.86 |

**Conclusion**: Geometric bond density (R=-0.91 unweighted) outperforms charge-
weighted descriptor. Charge weighting drives Li-O attractive term to dominate,
washing out the Cl-O repulsion penalty signal.

**Paper #2 method point**: simple geometric counts more robust than charge-
weighted versions for this small dataset.

### Y2 Halogen z-distribution: ⚠️ Weak supporting signal

Cl/Br surface fraction (top + bottom 20% of SE):

| comp | Cl_surf% | Br_surf% | Cl_exposure% | paper_exp |
|---|---|---|---|---|
| comp1 | 41.7 | — | 41.7 | 194 |
| comp2 | 33.3 | 33.3 | 33.3 | 180 |
| comp3 | 20.0 | 33.3 | 20.0 | 316 |
| comp4 | 25.0 | 50.0 | 25.0 | 298 |
| comp5 | 33.3 | 40.0 | 33.3 | 249 |
| modelC | 37.5 | — | 37.5 | — |

R(Cl_surface vs paper) = -0.50, p=0.39

Direction consistent with mechanism (less Cl at surface → less repulsion →
higher adhesion). comp3 has lowest Cl exposure (20%) AND highest paper exp.
But signal weaker than bulk Cl-O density (R=-0.91).

### Y3 ⭐ NEW FINDING — Surface termination

Atom counts in bottom 1Å of SE (interface side after stack):

| comp | total | Li | Cl | Br | S | P | Li/A | S/A |
|---|---|---|---|---|---|---|---|---|
| comp1 | 32 | 16 | 0 | 0 | 16 | 0 | 0.046 | 0.046 |
| comp2 | 24 | 8 | 0 | 0 | 16 | 0 | 0.023 | 0.046 |
| comp3 | 12 | 8 | 0 | 0 | 4 | 0 | 0.045 | 0.011 |
| comp4 | 16 | 8 | 0 | 4 | 4 | 0 | 0.045 | 0.011 |
| comp5 | 16 | 8 | 0 | 4 | 4 | 0 | 0.045 | 0.011 |
| modelC | 12 | 4 | 4 | 0 | 4 | 0 | 0.022 | 0.011 |

**R(surf_S density vs paper exp) = -0.91, p=0.032 ⭐**

S surface termination strongly anti-correlates with paper adhesion. But
mechanistically this just **tracks Li6 vs Li5.4 family** (Li6 family has 16
S at bottom, Li5.4 has 4 S). Same root cause as Cl-O density signal.

### Y4 ⭐ COLLINEARITY MATRIX — Definitive verdict

Cross-correlation Pearson R among 8 descriptors + paper_exp:

```
              Cl-O    Li-O    Br-O    Li/fu   Cl/fu   Br/fu   vacancy Cl+Br
Cl-O dens    +1.00   -0.84   -0.66   +0.99   -0.20   -0.74   -0.99   -0.99
Li-O dens    -0.84   +1.00   +0.37   -0.79   +0.65   +0.29   +0.79   +0.79
Br-O dens    -0.66   +0.37   +1.00   -0.67   -0.32   +0.78   +0.67   +0.67
Li/fu        +0.99   -0.79   -0.67   +1.00   -0.12   -0.80   -1.00   -1.00
Cl/fu        -0.20   +0.65   -0.32   -0.12   +1.00   -0.50   +0.12   +0.12
Br/fu        -0.75   +0.29   +0.78   -0.80   -0.50   +1.00   +0.80   +0.80
vacancy      -0.99   +0.79   +0.67   -1.00   +0.12   +0.80   +1.00   +1.00
Cl+Br        -0.99   +0.79   +0.67   -1.00   +0.12   +0.80   +1.00   +1.00
paper_exp    -0.91   +0.82   +0.39   -0.91   +0.42   +0.54   +0.91   +0.91
```

**6 pairs with |R|>0.95 (essentially equivalent):**
- Cl-O dens ↔ Li/fu (R=0.994)
- Cl-O dens ↔ vacancy (R=0.994)
- Cl-O dens ↔ Cl+Br (R=0.994)
- Li/fu ↔ vacancy (R=1.000, by construction)
- Li/fu ↔ Cl+Br (R=1.000, by stoichiometry)
- vacancy ↔ Cl+Br (R=1.000, by construction)

**Effective independent dimensions: ~2** (Li6/Li5.4 family + within-family
fine variation). All "winning" descriptors (Cl-O density, Li/fu, vacancy,
Cl+Br, surf_S) measure the **same underlying Li6 vs Li5.4 distinction** in
different units.

## Honest paper #2 narrative — final form

> "Among 8 candidate interface descriptors tested, six are mutually collinear
> (|R|>0.95) and reduce to a single physical dimension: Li6 (full
> stoichiometry) vs Li5.4 (vacancy-bearing) family. Within this dimension,
> simple geometric Cl-O contact density at the equilibrium interface gap
> (R=-0.91, p=0.03) and complementary Li-O density (R=+0.82, p=0.09)
> reproduce experimental adhesion ranking, while charge-weighted (Bader)
> versions degrade the signal (R=-0.11). Halogen surface enrichment in the
> SE bulk weakly supports the mechanism (R=-0.50). The remaining variance
> within Li5.4 family (comp3 vs comp4 vs comp5) is below the resolution of
> our descriptors (Δ<0.005), reflecting the system's near-degeneracy at
> fixed vacancy content. We therefore distinguish two regimes: (i) family-
> level prediction (Li6 vs Li5.4) is robust and physically interpretable
> through Cl/vacancy substitution; (ii) intra-family ranking requires
> finer descriptors beyond geometric bond counting at the rigid interface."

## Files

- `필독/adhesion/phase2a_v23_bulletproof.py` — statistical robustness
- `필독/adhesion/phase2a_v24_max_extract.py` — binding curve + multivariate
- `필독/adhesion/phase2a_v25_remaining_extract.py` — Bader + z-dist + termination + collinearity

#paper2 #adhesion #v23-v25 #extraction-complete #collinearity-verdict
