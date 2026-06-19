# LPSCl vs LPSCl1.6 — ionic conductivity, NEB-free geometric descriptors

**Question:** Express the comp1 (LPSCl) vs modelc (LPSCl1.6) Li⁺ transport difference the way
argyrodite papers do (doublet / intra-cage / inter-cage), WITHOUT running NEB.

**Two literature routes:**
- **NEB barriers** (Ma et al., *J. Mater. Chem. A* 2024, 12, 27011): explicit CI-NEB for
  intra-cage (0.873→0.496 eV) and inter-cage (0.976→0.592 eV) jumps. Note their DFT barriers
  are ~3× their own experimental Ea (0.29→0.25 eV) → trend only, not quantitative.
- **Geometric descriptors** (Taklu et al., *Nano Energy* 2021, 90, 106542): DFT-optimised
  geometry → 48h–48h Li–Li distances + 24g doublet bridge + S/Cl anion site disorder, tied
  qualitatively to Ea. NO barrier calculation. ← **route taken here** (we already have
  optimised structures + AIMD Ea).

## Method
`tools/ionic/cage_jump_descriptors.py` (numpy-only, full-MIC). Free anions (= cage centres) =
S not bonded to P (>2.3 Å) + all Cl. Each Li assigned to nearest cage centre; intra-cage =
Li–Li within a cage, inter-cage = across cages. Structures: `comp1_V0_k444.xyz` (cubic 4 f.u.),
`modelc_V0_k663.xyz` (rhombohedral, Cl-rich).

## Results

| descriptor | comp1 (LPSCl) | modelc (LPSCl1.6) |
|---|---|---|
| formula | Li24 P4 S20 Cl4 | Li27 P5 S22 Cl8 |
| free-anion centres | 4 S + 4 Cl | 2 S + 8 Cl |
| **cage-centre Cl fraction** | 0.50 | **0.80** |
| Li in S-cages / Cl-cages | 24 / 0 | 12 / 15 |
| **Li fraction on Cl sites** | 0.00 | **0.556** |
| occupied cages | 4 | 8 |
| Li per occupied cage | [6,6,6,6] | [6,6,4,2,2,1,3,3] |
| Li–Li NN median (Å) | 2.77 | 3.13 |
| **AIMD Ea (quantitative)** | **0.253 eV** | **0.223 eV** |

(AIMD from `docs/figures/slide09_arrhenius/arrhenius_fit_origin.csv`;
CSV: `docs/figures/ionic_cage/cage_descriptors_comp1_modelc.csv`.)

## Mechanism (the story)
1. **Anion site disorder ↑** — modelc cage centres are 80 % Cl (comp1 50 %), with one Cl on the
   4d (normally free-S) antisite → larger S/Cl site disorder.
2. **Li delocalisation ↑ (key signal)** — in comp1 all 24 Li localise in 4 free-S cages (6 each;
   the 4a Cl have no mobile-Li cage). In modelc 55.6 % of Li spread onto Cl-coordinated sites and
   the number of occupied cages doubles (4→8) → more accessible Li sites + a flatter energy
   landscape.
3. ⇒ this lowers the AIMD Ea (0.253→0.223 eV) and raises σ. This is exactly the Zeier
   "anion site disorder → Li delocalisation → σ↑" picture, and Taklu's "more migration
   sites / Li bridging" — reproduced for LPSCl→LPSCl1.6 without NEB.

## Honest caveats
- **Lead with anion-disorder + Li-delocalisation**, not raw distances. The intra/inter Li–Li
  distances are noisy in these ordered (fully Li-occupied) approximants — e.g. the inter-cage
  "window" came out 3.12→2.86 Å (confounded by the changed cage assignment), so it is NOT
  reported as a result.
- Taklu's specific "doublet distance shrinks" claim does NOT transfer here (our doublets are
  similar, 2.62 vs 2.73 Å). **Our mechanism is disorder-driven delocalisation, not bond
  contraction.**
- For a clean Fig-2d-style distance plot, extract Li–Li / jump statistics from the **AIMD
  trajectory** (samples the real mobile-Li distribution) rather than the static structure.
- Single-Li NEB (if ever run) would overestimate the absolute Ea ~3× (cf. Ma et al.); the
  quantitative number stays the **AIMD Ea**.
