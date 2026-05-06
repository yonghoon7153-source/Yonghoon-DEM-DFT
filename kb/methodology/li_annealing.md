# Li Annealing — Thermal Li Sublattice Re-optimization

## Purpose
Re-optimize Li positions after halogen substitution without disturbing the
PS₄ framework or halogen placement. This is the key improvement of Pipeline v2 over v1.

## Why It's Needed

The two-stage disorder problem:
1. **Halogen disorder**: 4a/4c S/Cl/Br placement → 56-70 configs → enumerable
2. **Li disorder**: 48h site half-occupancy → C(48,24)=12 billion → NOT enumerable

Pipeline v1 uses Rietveld Li positions (optimized for original composition, not Br-substituted).
Pipeline v2 adds Li annealing to find the optimal Li arrangement for each halogen config.

## Protocol

1. From halogen screening, take top 5 Li configurations
2. MLIP MD at **500K** for 50-100 ps (Langevin thermostat, dt=2fs)
3. After MD, MLIP relax (FIRE optimizer)
4. Compare energies → select champion

## Temperature Selection: 500K

| Species | Ea (eV) | kT at 500K | Behavior |
|---------|---------|------------|----------|
| Li⁺ | ~0.2 | 0.043 | Active hopping ✅ |
| S²⁻ | ~3.5 (P-S) | 0.043 | Vibration only ✅ |
| Cl⁻/Br⁻ | ~1.0 | 0.043 | Frozen ✅ |

- **<500K**: Li hopping too slow, stuck in local minima
- **500K**: Optimal — Li freely explores, framework preserved
- **800K+**: Cl⁻/Br⁻ start hopping → halogen enumeration invalidated ⚠️
- **1500K+**: PS₄ framework can break ⚠️

## Key Finding: Ranking Reversal

comp1 (Li₆PS₅Cl) results:

| Config | Screening Energy (eV) | Screening Rank | Annealing Energy (eV) | Annealing Rank |
|--------|----------------------|----------------|----------------------|----------------|
| #0 | -217.468 | 1 | -217.533 | **1** |
| #1 | -217.283 | 2 | -216.953 | **5** ↓ |
| #8 | -217.200 | 3 | -217.030 | **3** |
| #15 | -217.175 | 4 | -217.042 | **2** ↑ |
| #9 | -217.131 | 5 | -217.013 | **4** |

**Interpretation:** 0K relaxation (screening) finds local minima. Thermal annealing
explores deeper basins. A config with high screening energy may sit near a deep basin
that 0K relaxation cannot reach.

## Energy Landscape: Two Distinct Types

### Type 1 — Rough landscape (comp1, Li₆PS₅Cl)
- Li spread: **1162 meV** across 20 random configs
- Different random placements → very different energies
- Annealing gain: 65 meV (modest — screening already finds good basin)
- **Meaning:** Where you put Li matters a lot, but 0K relax can partially find it

### Type 2 — Flat with hidden valley (Model C, Li₅.₄PS₄.₄Cl₁.₆)
- Li spread: **0.1 meV** across 20 random configs (!!!)
- All random placements → nearly identical energies (shallow local minima)
- Annealing gain: **114 meV** (massive — hidden deep basin inaccessible to 0K relax)
- **Meaning:** Where you put Li barely matters for energy, BUT the true optimum is hidden behind barriers

```
Type 1 (comp1):                    Type 2 (Model C):
Energy                              Energy
  ↑   ╱╲                              ↑
  |  ╱  ╲   ╱╲                        |  ━━━━━━━━━━━━━━━  ← all random Li here
  | ╱    ╲ ╱  ╲  ╱╲                   |                     (0.1 meV spread)
  |╱      ╲    ╲╱  ╲                  |          ╲  ╱
  |        1162 meV spread             |           ╲╱  ← -114 meV (annealing only)
  └──────────────────→                 └──────────────────→
   Li config                            Li config
```

## Impact on Downstream Properties (CONFIRMED)

| Composition | Family | Li Spread | Annealing Gain | B₀ Δ(v1→v2) | Interpretation |
|-------------|--------|-----------|----------------|-------------|----------------|
| comp1 | Li₆ | 1162 meV | 65 meV | **0.3 GPa** | v1 ≈ v2, annealing optional |
| Model C | Li₅.₄ | 0.1 meV | 114 meV | **1.7 GPa** | v2 essential, hidden basin |

### Key Findings

1. **Li₆ (no vacancy): v1 sufficient.** Rough landscape but 0K relax still finds
   reasonable basins. v1→v2 = 0.3 GPa (DFT confirmed: 26.2→26.5).

2. **Li₅.₄ (vacancy): v2 essential.** Flat landscape deceives — all random placements
   look equivalent, but a -114 meV deep basin exists. v1→v2 = 1.7 GPa (MLIP; DFT pending).

3. **Annealing is the key differentiator.** Not Li screening (which shows 0.1 meV flat
   landscape), but thermal annealing (which escapes shallow minima to find deep basin).

4. **comp3/4/5 (Li₅.₄ + Br) likely need v2 too.** If pure Cl shows 1.7 GPa shift,
   Br-containing compositions may show equal or larger shifts (Br breaks symmetry →
   more complex landscape).

### Physical Interpretation

Why is Model C's landscape flat but comp1's is rough?

- **Model C (Li₅.₄, Cl only):** Pure Cl cage is highly symmetric. All 48h Li sites
  are nearly equivalent by symmetry → random Li placement barely changes energy.
  But the GLOBAL optimum requires specific Li-vacancy ordering that maximizes
  Cl coordination → only accessible via thermal exploration.

- **comp1 (Li₆, Cl only):** ALL 48h sites occupied (no vacancy). Different
  arrangements create different Li-Li repulsion patterns → large energy variation.
  But the best arrangement is findable by 0K relax because the energy gradient
  points toward it.

**Paradox:** Low Li screening spread does NOT mean Li ordering is unimportant.
It means 0K methods cannot distinguish configurations, making annealing MORE
(not less) important.

## comp4 v2 Finding: Thermal Degeneracy of Li Ordering (2026-05-06)

### Quantitative observation (Stage 2 LBFGS)

20 random Li configs × LBFGS for comp4 v2 (best halogen ordering) shows extreme degeneracy:

```
Li10: -255.4668    Li15: -255.4665
Li11: -255.4672    Li16: -255.4675  ← rank0 (best)
Li12: -255.4666    Li17: -255.4665
Li13: -255.4664    Li18: -255.4665
Li14: -255.4665    Li19: -255.4666

Spread: 1.1 meV across all configs
500K kT = 43 meV  →  kT/spread ≈ 40×
```

All Li orderings are **thermally degenerate** at 500K — they fall within a single
thermal basin.

### Stage 3 anneal: stochastic outcome

```
rank0 (Li16 start)  Stage2 LBFGS = -255.4675  →  anneal = -255.4791  Δ = -12 meV  ✓
rank1 (Li6  start)  Stage2 LBFGS ≈ -255.466?  →  anneal = -255.4626  Δ = +4 meV   ✗
```

rank1 anneal landed HIGHER than its Stage 2 LBFGS minimum — thermal MD escaped the
starting basin without finding a deeper one. With kT >> basin depth, anneal outcome
is stochastic.

### Reframing: anneal is ensemble sampling, not minimum search

For Li5.4 systems:
- **❌ Wrong**: "anneal finds the lowest-energy Li ordering"
- **✓ Right**: "anneal generates a naturally-relaxed Li distribution snapshot from the
  thermally accessible ensemble"

What top-N selection + anneal actually does:

```
Stage 1 (random Li):           작위적 placement
   ↓ LBFGS
Stage 2 (top-N LBFGS minima):  artificial 0K minima (thermally degenerate)
   ↓ 500K MD anneal + quench
Stage 3 (anneal output):       작위성 제거된 ensemble representative
```

### Why P/S/halogen ranking IS meaningful, but Li ranking is NOT

```
Sublattice         | Energy spread | Treatment
-------------------|---------------|---------------------------------
P (4b)             | fully ordered | structurally fixed
S (PS₄, 16e)       | fully ordered | structurally fixed
Free anion (4a/4d) | ~50-150 meV   | enthalpy-driven enumeration ✓
Li (48h)           | < 2 meV       | thermally averaged ensemble ✓
```

P/S/halogen disorder → different basins separated by enthalpy → ranking matters.
Li disorder → degenerate basins within thermal energy → ranking is noise.

### Implications for paper #1 C44 problem

The 47% C44 spread across Li orderings (paper #1) is the same phenomenon viewed
through mechanical observables:

- Energy spread:  1 meV (negligible)
- C44 spread:    12.7 GPa (47%)

→ Same Li configurations with indistinguishable E produce wildly different elastic
constants. The Li ordering itself is thermodynamically meaningless (kT >> ΔE), so
**any single-snapshot Cij is an artifact** — only ensemble averages have physical meaning.

This is the same logic that motivates 600K MD snapshot averaging in paper #1.

### Methodology framing for papers

Suggested SI text:

> "P/S/halogen ordering is enthalpy-driven and screened by 0K LBFGS energy
> ranking. The Li/vacancy sublattice, by contrast, is thermally averaged: 20
> random configurations × LBFGS for comp4 (Li5.4) span only 1.1 meV, far below
> 500K kT (43 meV). Stage 3 anneal therefore does not seek a ground state but
> generates a naturally-relaxed Li distribution from the thermally accessible
> ensemble. Ranking among top-5 anneal outputs is dominated by stochastic MD
> noise (~16 meV) and should not be used to select a single 'champion'; instead,
> any anneal output serves as a representative sample for downstream
> property calculation."

## References
- [pustorino2025] Systematic Li structure sampling in LPSCl
- [ayadi2024] AIMD Li short-range order, temperature homogenization
