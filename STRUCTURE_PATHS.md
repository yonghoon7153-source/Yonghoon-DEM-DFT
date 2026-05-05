# Canonical Structure Paths — Bond / Bader / Adhesion Source Files

> **CANONICAL — 모든 measurement (bond length, Bader, adhesion slab construction)는 이 파일의 경로 사용. 절대 다른 경로 만들지 말 것.**
> Verified: 2026-05-05 (KISTI single-script measurement, all comps consistent cutoff)

---

## Bond Length / Bader Charge Source Files

### Paper-quality (per composition)

| Comp | Family | Pipeline | Source File (KISTI) | Format |
|------|--------|----------|---------------------|--------|
| **comp1** | Li6 | v2 anneal champion | `/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_scf.out` | QE scf.out |
| **comp2** | Li6 | v2 anneal champion | `/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz` | xyz |
| **comp3** | Li5.4 | v1 (paper #1 published) | `/scratch/x3430a02/kgy/manuscript_support/post_relax/comp3_post_relax.out` | QE relax.out |
| **comp4** | Li5.4 | v1 (paper #1 published) | `/scratch/x3430a02/kgy/manuscript_support/post_relax/comp4_post_relax.out` | QE relax.out |
| **comp5** | Li5.4 | v1 (paper #1 published) | `/scratch/x3430a02/kgy/manuscript_support/post_relax/comp5/comp5_scf.out` | QE scf.out |
| **modelC** | Li5.4 | v2 anneal champion | `/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz` | xyz |

**중요**:
- comp1/2: ✅ v2 production (cubic, no slab fix needed)
- comp3/4/5: ⏳ **v2 not yet generated** — paper #1은 v1 사용. v1 .out 파일이 publication source.
- modelC: ✅ v2 production (rhombo, **needs pymatgen conventional fix** for adhesion slab)

### Bader Charges

같은 directory에 ACF.dat:
- comp1-4: `/scratch/x3430a02/kgy/manuscript_support/post_relax/comp{1,2,3,4}_ACF.dat`
- comp5: `/scratch/x3430a02/kgy/manuscript_support/post_relax/comp5/ACF.dat`

Method:
- `pp.x` charge density (`plot_num=21`, all-electron)
- Henkelman `bader_lnx_64` v1.05
- DB Δ ≤ 0.016 e for all elements (cross-validated)

---

## Bond Length Cutoffs (Consistent Across All Comps)

| Bond | Cutoff (Å) |
|------|-----------|
| Li-Cl | 3.2 |
| Li-Br | 3.4 |
| Li-S | 3.0 |
| P-S | 2.3 |

Method: PBE-DFT post-relax, MIC distance, ASE measurement.

---

## Adhesion v2 Slab Construction (2026-05-05)

### Status

| Comp | Source | Slab File | Cell Convention | Status |
|------|--------|-----------|-----------------|--------|
| comp1 | comp1v2_scf.out → V0 | `adhesion_v5_v2/comp1_slab_v2.xyz` | Cubic, a3 z-only ✓ | ✅ Ready |
| comp2 | comp2_v2_V0.xyz | `adhesion_v5_v2/comp2_slab_v2.xyz` | Cubic, a3 z-only ✓ | ✅ Ready |
| comp3 | comp3_post_relax.out | `adhesion_v5_v2/comp3_slab_v1_PRESERVED.xyz` (TODO) | Rhombo → pymatgen conv (β=97°) | ⏳ TODO |
| comp4 | comp4_post_relax.out | `adhesion_v5_v2/comp4_slab_v1_PRESERVED.xyz` (TODO) | Rhombo → pymatgen conv | ⏳ TODO |
| comp5 | comp5/comp5_scf.out | `adhesion_v5_v2/comp5_slab_v1_PRESERVED.xyz` (TODO) | Rhombo → pymatgen conv | ⏳ TODO |
| modelC | modelc_v2_V0.xyz | `adhesion_v5_v2/modelC_slab_v2_PRESERVED.xyz` | Rhombo → pymatgen conv (β=97°) | ✅ Done (5/5) |

### Slab Convention Fix Procedure (rhombohedral comps only)

For comp3/4/5/modelC (rhombohedral primitive cells):

```python
from ase.io import read, write
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

src = "<source_path>"  # from table above
a = read(src)
s = AseAtomsAdaptor.get_structure(a)
conv = SpacegroupAnalyzer(s, symprec=0.1).get_conventional_standard_structure()
new_atoms = AseAtomsAdaptor.get_atoms(conv)
slab = new_atoms * (2, 2, 1)

# Flip z if a3 negative
if slab.cell.array[2, 2] < 0:
    new_cell = slab.cell.array.copy(); new_cell[2] = -new_cell[2]
    slab.set_cell(new_cell, scale_atoms=False)
    pos = slab.positions.copy(); pos[:, 2] = -pos[:, 2]
    slab.set_positions(pos)
    slab.wrap()

write(f"<comp>_slab_<v1or2>_PRESERVED.xyz", slab)
```

**Integrity check** (max|Δd| < 1e-4 must pass):
- Compare sorted bond distributions (P-S, Li-S, Li-Cl, Li-Br) before/after
- Same cutoff (3.0 Å), same MIC distance method

See `kb/methodology/modelC_v2_slab_fix.md` for full reasoning.

---

## QE Output → ASE Read Recipes

### .xyz / .cif (direct)
```python
atoms = read("file.xyz")
```

### QE relax.out / scf.out (need format hint)
```python
atoms = read("file.out", format="espresso-out")
```

For relax.out, last frame = final relaxed coords:
```python
atoms = read("file.out", format="espresso-out", index=-1)
```

---

## Verification Script

To verify all paths are accessible:

```bash
for f in \
  "/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_scf.out" \
  "/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz" \
  "/scratch/x3430a02/kgy/manuscript_support/post_relax/comp3_post_relax.out" \
  "/scratch/x3430a02/kgy/manuscript_support/post_relax/comp4_post_relax.out" \
  "/scratch/x3430a02/kgy/manuscript_support/post_relax/comp5/comp5_scf.out" \
  "/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz"; do
  ls -la "$f" 2>&1 | head -1
done
```

---

## Related Files

- `kb/methodology/modelC_v2_slab_fix.md` — pymatgen conventional transformation reasoning + verification
- `db/compositions/comp{1..5,modelc}.json` — bond_length_v2 entries with this source
- `db/inputs/adhesion_templates/surface_mqa_v5.yaml` — adhesion protocol spec
- `CODE_INVENTORY.md` — pipeline v2 implementation status
