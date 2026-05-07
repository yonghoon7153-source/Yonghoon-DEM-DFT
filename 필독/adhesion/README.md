# 필독 — Adhesion (Paper #2 SE/NCM Wad)

> **Verified production code mirror for paper #2 SE/NCM adhesion calculations.**
> KISTI 본:  `/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/`

---

## Files

| File | Purpose | Status (2026-05-07) |
|---|---|---|
| `phase2a_v10_sandwich.py` | **v10 Camacho-Forero sandwich + NCM middle FixAtoms hybrid** | ❓ UNKNOWN — pilot 진행 예정 |
| `watchdog_phase2a_v10.sh` | Auto-restart wrapper for KISTI | ❓ UNKNOWN |

---

## v10 method (Camacho-Forero 2020 + Komatsu 2022 anchored)

### Anchors
- **Slab method**: Camacho-Forero & Balbuena, Chem. Mater. 2020, 32, 360-373
  (DOI 10.1021/acs.chemmater.9b03880). Sandwich + no FixAtoms + AIMD 20 ps + /(2A).
  LPSCl/Li2S(001) Wadh = 1.44 J/m² as scale anchor.
- **Bulk thermo**: Komatsu et al., J. Phys. Chem. C 2022, 126, 17482
  (DOI 10.1021/acs.jpcc.2c05336). LiNiO2/LPSCl ΔED,min,mutual = -424 meV/atom (most
  reactive NCM/sulfide pair). Reaction products: Ni3S2 + Li2S + Li2SO4 + Li3PO4 + LiCl.
  Volume change: -11% chemical, -34% at 4.5V.

### Method elements

| Element | Value | Source |
|---|---|---|
| Geometry | Sandwich (PBC z, 2 interfaces) | Camacho-Forero |
| Cell vacuum | None at interface | Camacho-Forero |
| Iso slab vacuum | 30 Å | UMA OOD constraint |
| FixAtoms NCM | Middle 3 atomic layers (of 9) | Hybrid (Sicolo-style bulk preserve) |
| FixAtoms SE | None | Camacho-Forero |
| Wad 분모 | 2A | Camacho-Forero |
| LBFGS fmax | 0.03 | tight (was 0.05 in v5, 200 saturated in v9) |
| LBFGS steps | 400 | (was 200 in v5/v9) |
| Gap | 2.5 Å | (Camacho-Forero used 2.0-2.2; we keep v5 value) |
| NCM thickness | 3L conv (9 atomic layers, 42.57 Å) | (1L is broken structure per user) |
| MD | None | UMA-MD-at-interface failure history (troubleshooting items 19-21) |
| Sampling | 6 high-sym + 30 random = 36 reg, 6 comps round-robin | v5/v9 same |

### Wad formula
```
Wad = (E_iso_NCM_vacuum + E_iso_SE_vacuum − E_int_sandwich) / (2 A)  [eV/Å²]
    × 16.0218  → J/m²
```
- `E_iso_NCM`: NCM 3Lconv with vacuum 30 Å, FixAtoms middle 3 atomic layers
- `E_iso_SE`: SE 2x2x{1,3} (paper #1 v2 anneal champion) strained to NCM lateral, vacuum 30 Å, no FixAtoms
- `E_int`: NCM + SE sandwich, NCM middle FixAtoms only
- `2A`: PBC z creates 2 interfaces

### Inputs (verified, from STRUCTURE_PATHS.md)

```
SE slabs (KISTI):
  comp1_slab_v2.xyz            (cubic, paper #1 v2 anneal champion)
  comp2_slab_v2.xyz            (cubic, paper #1 v2)
  comp3_slab_v1_PRESERVED.xyz  (rhombo → pymatgen conv)
  comp4_slab_v1_PRESERVED.xyz
  comp5_slab_v1_PRESERVED.xyz
  modelC_slab_v2_PRESERVED.xyz (rhombo, β=97°)

NCM 3Lconv (KISTI):
  ncm_7x7x1_3Lconv.xyz  (Li6 family, 1764 atoms, 147×3 Li + 147×3 Ni + 294×3 O)
  ncm_5x5x1_3Lconv.xyz  (Li5.4 family, 900 atoms, 75×3 Li + 75×3 Ni + 150×3 O)

Both NCM = LiNiO2 (R-3m), generated via:
  ase.read('ncm_*x*x1_PRESERVED.xyz') * (1, 1, 3)  → write *_3Lconv.xyz
```

---

## How to deploy on KISTI (pilot run)

```bash
cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/

# 1. Copy the script (paste from this repo or from this README)
#    Save as phase2a_v10_sandwich.py and watchdog_phase2a_v10.sh

chmod +x watchdog_phase2a_v10.sh

# 2. Verify GPU1 free
nvidia-smi | tail -10

# 3. Pilot — full 6 comps × 36 reg round-robin (~22 hours estimated)
nohup bash watchdog_phase2a_v10.sh > /dev/null 2>&1 &

# Or: pilot only 1 cycle first (modify N_RANDOM=0 in script for high-sym only = 6 reg = 6 comps × 6 = 36 interfaces ~= 4-5 h)

# 4. Monitor
tail -f phase2a_v10_results/progress.log
```

### Time estimates (Stage A iso + Stage B round-robin)

| Stage | atoms | est. time |
|---|---|---|
| Iso NCM 7x7x1_3Lconv (1764at, fix 588) | 1764 | ~10 min |
| Iso NCM 5x5x1_3Lconv (900at, fix 300) | 900 | ~5 min |
| Iso SE comp1/2 (624at, no fix) | 624 | ~3 min × 2 = 6 min |
| Iso SE comp3/4/5/modelC (248at, no fix) | 248 | ~2 min × 4 = 8 min |
| **Stage A total** | — | **~30 min** |
| Stage B Li6 (NCM 1764 + SE 624 = 2388at) × 2 comps × 36 reg | 2388 | ~10 min/relax × 72 = 12 h |
| Stage B Li5.4 (NCM 900 + SE 248 = 1148at) × 4 comps × 36 reg | 1148 | ~4 min/relax × 144 = 9.6 h |
| **Stage B total** | — | **~22 h** |
| **Grand total** | — | **~22.5 h ≈ 1 day** |

### Validation against v5 paper

| comp | v5 paper Wad (J/m²) | v10 expected (J/m²) | Notes |
|---|:-:|:-:|---|
| comp1 (LPSCl/Li6) | 1.28 | 1.5-3.0 | Camacho-Forero LPSCl/Li2S(001)=1.44 ref |
| comp2B (LPSCBr/Li6) | 1.18 | 1.4-2.8 | |
| comp3 (Li5.4) | 2.10 | 2.5-4.0 | vacancy chemistry now allowed |
| comp4 | 1.97 | 2.3-3.8 | |
| comp5 | 1.65 | 1.9-3.2 | |
| modelC | — | 2.0-3.5 | |

**Key cross-family check**: v10 should preserve Li5.4 > Li6 (vacancy chemical anchor effect).
If v10 inverts to Li6 > Li5.4 → method bug or UMA OOD on sandwich.

---

## CODE_INVENTORY status

- **F2** `phase2a_v10_sandwich.py`: ❓ UNKNOWN (this file)
- **F1** `phase2a_lbfgs_wad.py` (v5 paper baseline): ✅ VERIFIED (paper #1 published values)
- v8 `phase2a_v8_surface_mqa.py`: ❌ INVERTED (cross-family failed)
- v9 `phase2a_v9_cleavage.py`: ❌ INVERTED (24/216 stopped 2026-05-07; comp3 0.82 ≪ paper 2.10)

---

## Decision history (why v10 design)

| Constraint | Decision | Rationale |
|---|---|---|
| UMA-MD-at-interface fails (troubleshooting 19-21) | LBFGS only, no AIMD | UMA force errors blow up at vacuum; sandwich removes vacuum but MD at interface still risky |
| FixAtoms NCM bottom only? | Middle 3L instead | Bottom-only breaks PBC interface symmetry (one interface frozen, other free) |
| 1L vs 3L NCM | 3L conv (per user, 1L is broken) | Ensures bulk reference + 6 free atomic layers for chemistry |
| /A vs /(2A) | /(2A) for sandwich | Camacho-Forero math: 2 interfaces → 2A normalization |
| fmax 0.05 → 0.03 | tightened | v9 hit 200 steps unconverged; need higher steps + tighter fmax |

---

#paper2 #adhesion #v10 #sandwich #LPSCl #NCM #LiNiO2 #UMA #LBFGS-only #must-read
