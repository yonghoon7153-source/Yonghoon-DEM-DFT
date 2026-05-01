# 0K Cij DFT Protocol Status (Paper #1)

> [!warning] Status as of 2026-05-01
> **comp1 v2**: VERIFIED (clamped-ion, KISTI). Use for paper SI.
> **comp2 v2**: ANOMALOUS (clamped-ion, gabia). DO NOT cite.
> **comp3-5, modelC v2**: 0K Cij not yet recomputed with verified protocol.

---

## Verified protocol — clamped-ion finite-strain SCF

```
calculation='scf'    (no atom relaxation in strained cell)
12 strain  =  6 directions x 2 signs (+, -)
strain magnitude  =  0.005 (0.5%)
ATOMIC_POSITIONS (crystal)  -- atoms scale with cell (affine)
```

This is **clamped-ion** Cij, not the standard "relaxed-ion" paper-quality.
Higher C than relaxed-ion (atoms cannot relieve internal stress).

---

## comp1 v2 (VERIFIED)

| | C11 | C12 | C44 | K_VRH | G_VRH | E_VRH | nu |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| db v2 (paper) | 78.8 | 29.8 | 39.0 | 46.2 | 32.4 | 78.9 | 0.216 |
| recompute 2026-05-01 | 79.27 | 29.68 | 38.87 | 46.21 | 33.24 | 80.43 | 0.210 |

**Match: 0.6%** -> protocol + script verified.

- Machine: KISTI `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/`
- Files: `comp1v2_elastic_{1,2,3,4,5,6}{p,m}.out` (12 files, JOB DONE Apr 14-15 2026)
- Script: `compute_cij_check.py`

---

## comp2 v2 (ANOMALOUS - DO NOT USE)

| | C11 | C12 | C44 | K_VRH | G_VRH | E_VRH | nu |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| comp2 v2 (gabia) | 78.93 | 29.68 | **77.60** | 46.10 | 56.41 | **120.20** | 0.065 |
| comp1 v2 (verified) | 79.27 | 29.68 | **38.87** | 46.21 | 33.24 | **80.43** | 0.210 |
| delta | -0.4% | 0% | **+99.6%** | -0.2% | +69.7% | **+49.5%** | -69% |

> [!error] Anomaly
> Br doping cannot physically increase C44 by ~100%. Same clamped-ion protocol on both. Setup issue on gabia run.

- Machine: gabia `/data/work/bml/manuscript_support/comp2v2_dft_0K/`
- Files: `e{1-6}_{p,m}/scf.out` (12 files, JOB DONE 2026-05-01)
- Script: `compute_cij.py` (gabia copy)

### Possible causes (untested)
- Strain magnitude not exactly 0.005 (need to verify CELL_PARAMETERS in each strain dir)
- Starting structure not at correct V0
- Pseudo or k-grid mismatch with KISTI

---

## comp3, comp4, comp5, modelC v2 0K Cij — STATUS

Not yet recomputed with the verified clamped-ion protocol.
- comp5: some files at `/scratch/x3430a02/kgy/manuscript_support/comp5_basinA/elastic_basinA/` (basin A v1, not v2)
- comp3, comp4, modelC: not found via `find` on KISTI

---

## Decision for paper #1 Section 3 (Mechanical)

> [!success] Use 600K MLIP elastic, NOT 0K Cij
> 0K Cij is **SI material only** with comp1 v2 verified value.
> 600K MLIP elastic (already in db) is the **paper main figure**:
> - comp1 v1: 29.1 GPa
> - comp2 v1: 28.6 GPa (Br -1.7%)
> - comp3 v1: 27.3
> - comp4 v1: 26.4
> - comp5 v1: 25.8
> - comp2 v2 (anneal): 34.7 (+21% stiffening from ordering)

**Action items**:
1. comp2 v2 0K Cij is ANOMALOUS - either fix or omit from paper.
2. If paper Section 3 uses only 600K MLIP, no further 0K work needed.
3. comp1 v2 0K Cij verified value (79.27 / 80.43) is paper-quality reference.

---

## File-level summary

| comp | v1 0K | v2 0K | v2 protocol | Status |
|---|---|---|---|---|
| comp1 | db | db (78.9) | clamped-ion | ✓ verified |
| comp2 | db | 120.2 | clamped-ion | ✗ anomalous |
| comp3 | db | none | n/a | not done |
| comp4 | db | none | n/a | not done |
| comp5 | db | none | n/a | not done |
| modelC | db | none | n/a | not done |

---

#paper1 #elastic #0K #clamped-ion #protocol-status
