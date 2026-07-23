# Elastic Constants Calculation

## Overview
Two approaches: DFT 0K clamped-ion (ordered) vs MLIP 600K snapshot (disordered).

> **UPDATE 2026-07-23:** DFT relaxed-ion (comp1 22.06 GPa)이 paper 정본. 600K MLIP elastic은 2026-07-23 db/properties/elastic.json에서 제거됨 (deprecated). 상세는 `computational_methods_canonical.md`.

## DFT 0K Clamped-Ion

**Method:** Finite strain ±0.005, 6 strain patterns × positive/negative = 12 SCF calculations.

**Problem:** Li is ordered at 0K → cooperative shear → C44 overestimated.
- comp5 Basin A: C44 = 39.9 GPa (DFT 0K) vs ~10-14 GPa (600K snapshot)
- Literature Deng et al.: C44 = 7.8 GPa (SQS method)

**QE Stress Convention:**
- QE outputs stress with positive = compression
- Cij = -dσ/dε (use kbar columns 3,4,5 for shear)

## MLIP 600K Snapshot Method (DEPRECATED — removed 2026-07-23)

> **DEPRECATED 2026-07-23:** 이 600K MLIP elastic은 db/properties/elastic.json에서 제거됨. paper 정본은 DFT relaxed-ion (comp1 22.06 GPa). 아래 표/수치는 참고용 이력으로만 유지. 상세는 `computational_methods_canonical.md`.

**Protocol:**
1. MLIP MD at 600K (NVT, Langevin, dt=2fs, ~10ps equilibration + ~20ps production)
2. Extract 5 snapshots (evenly spaced)
3. Quench each snapshot to 0K (FIRE optimizer)
4. Relax (FIRE, fmax=0.01 eV/A)
5. Finite-strain Cij for each snapshot
6. VRH (Voigt-Reuss-Hill) average across 5 snapshots → mean ± std

**Why 600K:** Li⁺ actively hopping → naturally disordered. PS₄ framework intact.
Captures the real thermal average that experiments measure.

**Results (GPa):**

| Comp | E | E_std | K | G | Expt E |
|------|---|-------|---|---|--------|
| comp1 | 29.1 | 1.1 | 21.0 | 11.5 | 28.0±1.8 |
| comp2 | 28.6 | 1.1 | 21.2 | 11.2 | — |
| comp3 | 27.3 | 0.4 | 20.9 | 10.6 | — |
| comp4 | 26.4 | 1.6 | 20.5 | 10.3 | — |
| comp5 | 25.8 | 0.8 | 19.6 | 10.1 | — |

## Basin A vs B (comp5) — Li Ordering Sensitivity

| Property | Basin A | Basin B | Delta | % |
|----------|---------|---------|-------|---|
| C44 (DFT) | 39.9 | 27.2 | +12.7 | 47% |
| E (DFT) | 86.5 | 70.9 | +15.6 | 22% |
| K (DFT) | 42.9 | 41.8 | +1.1 | 2.6% |
| E (600K) | 30.0 | 25.8 | +4.2 | 16% |

**Key Finding:** Li ordering sensitivity manifests primarily in shear (C44),
not compression (K). This is because shear deformation directly probes
Li-anion local bonding geometry.

## Future: Finite-Temperature Methods

| Method | Principle | Pros | Cons |
|--------|-----------|------|------|
| Stress-fluctuation | <σ_ij σ_kl> at NVT | All Cij, thermal included | ns MD needed |
| Stress-strain (ElasT) | Finite-T strain→stress | Fast convergence | Strain needed |
| NPT → B(T) | V(T,P) → B(T) | Direct T-dependence | B only (no G) |

## References
- [pustorino2025] Li+ distribution → E = 10-30 GPa variation
- [deng2016] SQS elastic: C44=7.8, E=22.1 GPa
- [damore2022] Polymorph → B0 difference, QHA B(T)
- [kozuka2025] DFT-D3 E=22.1 GPa, stress-strain strength
