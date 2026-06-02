# modelC v2 Slab Construction — Convention Fix

> **Issue resolved 2026-05-05**: modelC v2 champion structure uses different cell convention than comp3/4/5 v1 (paper #1). Original v5 `orthogonalize` flag silently failed; 2×2×1 repeat overflowed cell box (z=42 Å > a3=35 Å). Fix uses pymatgen `get_conventional_standard_structure()` — atomic geometry preserved exactly (max|Δd| = 0).

---

## Problem Discovery

When preparing v2 SE slabs for adhesion (paper #2 baseline + paper #1 cross-check), `verify_slabs.py` reported "✓ a3 z-only (orthogonalized)" for modelC v2 but the slab was actually broken:

| Slab | a1[2] | a2[2] | a3[2] | z_extent (atoms) | Status |
|------|-------|-------|-------|------------------|--------|
| comp1 v2 | 0 | 0 | 29.79 | 29.03 Å | ✅ OK |
| comp2 v2 | 0 | 0 | 29.85 | 29.04 Å | ✅ OK |
| **modelC v2** | **+3.50** | **+3.50** | **35.02** | **42.00 Å** | ❌ **7 Å overflow** |

Root cause: modelC v2 champion was relaxed in QE with **rhombohedral primitive cell** (α=β=γ=60°, |a1|=|a2|=|a3|=7.003), then a3 was multiplied by 5 to give the 62-atom cell. The result has a1, a2 tilted by 30° toward z (each contributes a[2]=+3.502), while a3 is along z. After 2×2×1 repeat in xy, atoms span z = 0 to 42 Å but the box's a3[2] is only 35 Å → ~7 Å of atoms outside box → broken PBC.

`verify_slabs.py` only checked a3[xy] = 0 (true here) and missed the a1[2], a2[2] tilt.

## Convention Mismatch with Paper #1

Paper #1 (comp3/4/5 v1, used for adhesion) used the OPPOSITE convention:
- a1, a2 horizontal (z=0)
- a3 had small xy components (Bravais standard for rhombohedral hexagonal-axes setting)
- v5 `orthogonalize` zeroed a3[xy] → clean cell

modelC v2 champion has:
- a3 already z-only
- a1, a2 tilted with z components

So v5's `orthogonalize: true` did nothing useful (it only fixes a3, not a1/a2).

## Fix: pymatgen Conventional Standard Structure

```python
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

orig_atoms = read("modelc_v2_V0.xyz")  # 62 atoms, rhombo primitive
s = AseAtomsAdaptor.get_structure(orig_atoms)
conv = SpacegroupAnalyzer(s, symprec=0.1).get_conventional_standard_structure()
slab = AseAtomsAdaptor.get_atoms(conv) * (2, 2, 1)  # 248 atoms
```

This relabels lattice vectors as **integer linear combinations** that put a1, a2 in the xy plane (γ=120°, hexagonal-axes setting), at the cost of slight a3 monoclinic tilt (β=97°).

Result for modelC v2:

```
Conventional cell (62 atoms):
  a1 = [-7.003,  0.000,   0.000]
  a2 = [ 3.502,  6.065,   0.000]
  a3 = [ 3.502, -2.022, -28.592]
  α=90°, β=96.97°, γ=120°
  |a|=|b|=7.003, |c|=28.876
```

After 2×2×1: 248 atoms, **z_extent 27.92 Å < a3[2] 28.59 Å** ✅ no overflow.

## Atomic Geometry — Exact Preservation Verified

The user wanted minimum disturbance. Pymatgen's `get_conventional_standard_structure()` is a pure relabeling of lattice vectors — atomic positions in Cartesian coordinates are identical. Verified by comparing sorted bond-length distributions at fixed 3.0 Å cutoff:

| Bond | n (orig) | n (conv) | Δ mean | max\|Δd\| |
|------|----------|----------|--------|-----------|
| P-S | 20 | 20 | 0.0000 | **0.000000 Å** |
| Li-S | 67 | 67 | 0.0000 | **0.000000 Å** |
| Li-Cl | 41 | 41 | 0.0000 | **0.000000 Å** |

Volume identical: 1214.50 Å³ before and after.

**Conclusion**: The cell shape change is purely a basis transformation. No atomic distortion. Safe for paper-quality adhesion.

## Note on β=97° vs Forced β=90°

We considered forcing a3 along z (zero a3[xy]) but this introduced spurious strain:
- Li-S: 2.460 → 2.491 Å (+1.3%)
- P-S: 2.062 → 2.067 Å (+0.2%)

So we **rejected the forced-orthogonal option**. The β=97° monoclinic tilt is preserved in the slab cell; ASE/UMA handle non-orthogonal cells without issue. NCM stacking still works because:
1. SE a1, a2 are horizontal (z=0) → flat top/bottom faces
2. NCM cell is built independently (R-3m hexagonal a=2.878, c=14.19 → 5×5×1 repeat)
3. Lattice match in xy plane is what matters; a3 tilt is irrelevant for adhesion

## Output File

```
/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/modelC_slab_v2_PRESERVED.xyz
  248 atoms (62 × 4)
  cell: monoclinic-ish, β=97°, a1/a2 horizontal
  geometry: identical to original modelC v2 V0 champion
```

## Action Items

1. ⏭ Update `surface_mqa_v5.yaml` orthogonalize comment: "applies to comp3/4/5 v1 convention only; modelC v2 needs pymatgen conventional"
2. ⏭ Run adhesion v6 (LBFGS-only, 5 z-cuts) on:
   - comp1_slab_v2.xyz (already OK, 624 atoms)
   - comp2_slab_v2.xyz (already OK, 624 atoms)
   - modelC_slab_v2_PRESERVED.xyz (fixed, 248 atoms)
3. ⏭ GPU 1 (GPU 0 occupied by Nd enumeration on KISTI scratch)
4. ⏭ Compare v2 results with paper #1 v1 published Wad values

## Related Files

- `db/inputs/adhesion_templates/adhesion_v6_anneal_test.py` — v6 runner
- `db/inputs/adhesion_templates/surface_mqa_v5.yaml` — v5 protocol spec
- `tools/build_ncm_interface.py` — NCM slab builder
- `kb/results/adhesion_v5_full_report.md` — paper #1 final values
- `kb/results/adhesion_troubleshooting.md` — past failure modes (v1-v4)
