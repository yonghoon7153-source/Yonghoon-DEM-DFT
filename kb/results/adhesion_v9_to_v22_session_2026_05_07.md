# Adhesion Method Iteration v9-v22 — Session Report (2026-05-07)

> Context: Server data lost (paper #1 v5 results gone). R²=0.9999 cross-family
> match was user-curated. Need from-scratch validation with literature anchors:
> Haruyama 2014 (slab method), Komatsu 2022 (bulk thermo), Camacho-Forero 2020
> (sandwich + AIMD).

## Summary table

| Version | Method | Cross-family | Status |
|---|---|:-:|---|
| v9 | Sandwich + cleavage (LBFGS iface, rigid sep) | ❌ INVERTED | Stopped 13:45 |
| v10 | Sandwich + NCM mid-fix + LBFGS + /(2A) | ❌ INVERTED | Stopped ~13:00 |
| v10b | Sandwich + NCM/SE mid-fix + LBFGS + /(2A) | ❌ INVERTED | Stopped 14:40 |
| v11 | Single + vacuum + Haruyama-style + LBFGS | ❌ INVERTED | Stopped 15:30 |
| **v12** | Single + vacuum + Haruyama + **NO LBFGS (rigid)** | **(coincidental ✓)** | Done 3.7 min |
| v13 | Z-scan validation of v12 | revealed gap dependence | Done |
| v14 | Equilibrium gap + bond count + Pearson R | hybrid descriptor | Done 1.1 min |
| v15 | Bond count 36 reg robustness | ✓ ROBUST (CV 6.1%) | Done 2.1 min |
| v16-22 | Comprehensive validation suite | (TBD) | Designed, awaiting deploy |

## Key methodological lessons

### LBFGS causes Li intermixing artifact (v9-v11)
- Li6 SE has ~6 Li/fu (high density) + frustrated sublattice (Li ordering spread 1162 meV per paper #1)
- Li5.4 SE has ~5.4 Li/fu (vacancy) + ordered sublattice (0.1 meV)
- LBFGS perturbation → Li6 frustrated atoms migrate easily → ~20 Li atoms penetrate NCM
- Wad inflated: more migration → lower E_int → larger Wad
- Li6 > Li5.4 ranking emerges from migration count, NOT vacancy anchor

### Rigid Wad is gap-dependent and Madelung-dominated (v12-v14)
- v12 fixed gap=2.5 happened to match paper exp ranking — coincidental
- v13 Z-scan: W_max at gap=1.5 gives OPPOSITE ranking
- v14 equilibrium gap 1.2-1.6 Å (varies by comp): W_eq ranking ANTI-correlates with paper (R=-0.76)
- Energy descriptor at slab level dominated by composition-driven Madelung sum
- xy-shift CV<1% (v15): registry-insensitive — confirmed Madelung-dominated

### Bond density (geometric) IS robust descriptor (v14-v15)
- Li-O density per Å² at gap_eq: R=+0.82 (positive correlation with paper exp)
- Cl-O density: R=-0.91 (anion-anion repulsion penalty)
- Composite (Li-O − α·Cl-O): R≈+0.91
- v15: 36 registries CV 6.1% — bond density is intrinsic to atomic structure
- v14 single R1 vs v15 mean of 36: Pearson R agrees within 0.02 — not artifact

### Mechanism narrative (under validation)
- **Vacancy chemical anchor**: Li5.4 vacancy positions surface Li closer to NCM-O
  → high Li-O density → high adhesion
- **Cl-saturation passivation (modelC)**: 17 Cl-O contacts at surface
  → anion-anion repulsion → predicts low adhesion
- **Br role threshold**: Br < 0.7/fu buried in bulk; Br ≥ 0.8/fu surface-exposed
  → comp3 (Br=0.6) sweet spot; comp4/5 Br-O penalty

## Validation suite design (v16-v22)

| Test | Purpose | Method | Time |
|---|---|---|---|
| v16 | Cutoff sensitivity | Vary Li-O 2.5-3.5, Cl-O 3.0-4.0, Br-O 3.2-4.3 Å | 1 min |
| v17 | Gap window sensitivity | Vary 3.0-6.0 Å for "near-interface" definition | 1 min |
| v18 | Per-Li atom decomposition | Identify "anchor Li" (nearest_O < 3.0 Å) per comp | 1 min |
| v19 | Phase 1 cross-validation | Compare v15 metric with phase1_summary.json W_max | 30 sec |
| v20 | Visualization xyz | Save 6 xyz files for VESTA inspection | 30 sec |
| v21 | Composite descriptor optimization | Grid search (α, β) for Li-O − α·Cl-O − β·Br-O | 30 sec |
| v22 | **Relaxed bond count** | Limited LBFGS (max 50 steps) at gap_eq, count bonds | 5 min |

## Relax vs rigid bond count — methodological choice

User's question: "if descriptor is bonds, isn't relaxation more realistic?"

**Two types of relaxation**:
- **Type (a)**: Local atom adjustment 0.1-0.5 Å to find optimal bonding positions
  → desired effect for realistic interface
- **Type (b)**: Long-range migration 3+ Å into NCM bulk
  → solid-solution formation, NOT adhesion
  → observed in v9-v11 with LBFGS 200-300 steps

**v22 strategy**: Limited LBFGS (max 50 steps, fmax 0.05) + tight FixAtoms
- Cap migration window
- Track RMS displacement
- If RMS > 1.5 Å, flag as migration
- Compare bond count post-relaxation with v15 rigid

**If v22 gives same ranking as v15** → descriptor robust to relaxation strategy
**If different** → discuss in paper #2 method section

## Concerns to address

1. **n=5 small** for Pearson R — uncertainty ~±0.2
2. **modelC** predicted lowest Wad but no experimental measurement (paper hypothetical)
3. **MLIP energy fundamentally limited** at slab geometry for our system
4. **Different equilibrium gap per comp** (1.2-1.6 Å) — possibly need gap < 1.0 scan
5. **v5 paper #1 R²=0.999** was user-curated, NOT independent validation

## Paper #2 narrative — current candidate

> "Atomic-level MLIP energy descriptors (W_eq, fixed-gap Wad) at SE/NCM
> interfaces do not correlate with experimental adhesion measurements
> (R=-0.76, anti-correlated). However, geometric bond density descriptors
> at the equilibrium gap reproduce experimental ranking: Li-O attractive
> contacts (R=+0.82) and Cl-O repulsive contacts (R=-0.91), with composite
> (Li-O − α·Cl-O) achieving R=+0.91. The vacancy chemical anchor mechanism
> hypothesized from macroscopic measurements manifests geometrically:
> vacancy positions surface Li closer to NCM-O while suppressing Cl exposure.
> This indicates that interface chemistry — specifically the density of
> cation-anion contacts — is the macroscopically observable signal,
> while total interface energy is dominated by composition-dependent
> Madelung sums that obscure interface-specific chemistry."

## Files

- `필독/adhesion/phase2a_v9_cleavage.py` (paper #1 broken)
- `필독/adhesion/phase2a_v10_sandwich.py` (Camacho-Forero, failed)
- `필독/adhesion/phase2a_v10b_sandwich_se_fixed.py` (modified Camacho-Forero, failed)
- `필독/adhesion/phase2a_v11_haruyama_single.py` (Haruyama+LBFGS, failed)
- `필독/adhesion/phase2a_v12_rigid_haruyama.py` (rigid, current best baseline)
- `필독/adhesion/phase2a_v13_validation.py` (Z-scan + dense xy + bond decomp)
- `필독/adhesion/phase2a_v14_full_validation.py` (sanity + eq gap + composite)
- `필독/adhesion/phase2a_v15_bond_robustness.py` (36 reg robustness ✓)
- `필독/adhesion/phase2a_v16to22_full_suite.py` (comprehensive validation, ready)

## References used

- Haruyama 2014 — `필독/literature/haruyama2014.md`
- Komatsu 2022 — `필독/literature/komatsu2022.md`
- Camacho-Forero 2020 — `필독/literature/camacho_forero_2020.md`
- Enaldiev 2021 — `필독/literature/enaldiev2021.md` (low utility, just figure ref)

#paper2 #adhesion #v9-v22 #session-2026-05-07 #method-iteration #honest-narrative
