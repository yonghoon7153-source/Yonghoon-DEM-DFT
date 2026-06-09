# constrained ESW Cl-content scan — Gil-González Fig 1a reproduced with our cells

**Date 2026-06-09. Run on gabia, MP GGA_GGA+U hull, LiS4 / SCl3 / Li5PS4Cl2 excluded.**
Tool: `tools/oxidation/constrained_esw.py` (strain-explicit Fitzhugh leading order).
Output: `gabia:/data/work/repo/constrained_esw_cl_scan.json`.

## Goal

After the comp1 vs modelc pair-test closed Axis 2 ("Cl-rich widens more under constriction") with our cells, the natural next test is the **full Cl-content sweep** that Gil-González (Energy Storage Mater. 2022, Fig 1a) ran experimentally + computationally for K_eff = 0 / 10 / 20 GPa. If our `constrained_esw.py` is right, we should see:

1. flat window at 0 GPa (~1.7–2.4 V) across Cl content;
2. monotone widening with Cl as K_eff increases;
3. a turn-over at Cl ≈ 2.0 where their orthorhombic LPSCl2.0 phase appears.

## Composition series

| Label | Composition | V_SE (Å³/fu, used) | Notes |
|---|---|---|---|
| LPSCl0.5 | Li6.5PS5.5Cl0.5 | 264.5 | Cl-poor, approximate vol |
| LPSCl1.0 | Li6PS5Cl | 254.16 | comp1, our EOS V0/4 |
| LPSCl1.5 | Li5.5PS4.5Cl1.5 | 245.0 | Gil-González reference, approximate vol |
| **modelc** | **Li5.4PS4.4Cl1.6** | **243.29** | our modelc, EOS V0/5 |
| LPSCl2.0 | Li5PS4Cl2 | 233.0 | Cl-rich limit, approximate vol |

`V_SE` for the in-between compositions uses MP-averaged volumes (Cl smaller than S → cell shrinks with Cl). The leading-order edge shift only uses `DeltaV` of the *decomposition*, so the V_SE column mostly affects ε_RXN diagnostic, not the edge prediction.

## Headline results

### Oxidation onset reaction strain (the key quantity)

`ε_RXN = ΔV_products(solids) / V_SE` at the K_eff = 0 oxidation onset. **Monotone with Cl on the Cl-rich side.**

| | Cl/fu | n_e | ΔV (Å³) | **ε_RXN** | onset reaction at K_eff=0 |
|---|---|---|---|---|---|
| LPSCl0.5 | 0.5 | 3.0 | −22.7 | **−0.086** | → 0.5 LiCl + 1.5 S + Li3PS4 + 3 Li |
| LPSCl1.0 (comp1) | 1.0 | 2.0 | −9.2 | −0.036 | → 1.0 LiCl + 1.0 S + Li3PS4 + 2 Li |
| LPSCl1.5 | 1.5 | 1.0 | +3.2 | **+0.013** | → 1.5 LiCl + 0.5 S + Li3PS4 + 1 Li |
| **modelc** | 1.6 | 0.8 | +5.5 | **+0.023** | → 1.6 LiCl + 0.4 S + Li3PS4 + 0.8 Li |
| LPSCl2.0 | 2.0 | 3.0 | −4.4 | **−0.019** | → 2.0 LiCl + 0.5 S + 0.5 P2S7 + 3 Li |

Two qualitative jumps:

1. **Sign flip at Cl ≈ 1.3–1.5:** below this the oxidation decomposition is denser than the SE (electrons released drag the Li to the anode and the solid residue is just S+LiCl+Li3PS4 packed tighter than the parent); above this the bulky LiCl product dominates and the residue expands. Once ε_RXN > 0, mechanical constriction stabilises the SE → anodic limit rises.
2. **Path change at Cl = 2.0:** the system loses Li6PS5Cl-style decomposition entirely. The new path goes to P2S7 (a denser P–S polymer) + 2 LiCl + extra S, which has a denser product set than the half-LiCl LPSCl1.5 route. ε_RXN drops back to slightly negative. This corresponds to the orthorhombic LPSCl2.0 phase Gil-González discusses (their Fig 1a Cl=2 sits in a different structural family).

### Windows vs K_eff

K_eff = 0 GPa is essentially flat across Cl (1.01–1.14 V wide, all anchored at the same 1.24 V reduction edge and ~2.26 V oxidation edge). This is the "no constriction" baseline and **reproduces Gil-González's flat 0 GPa curve in Fig 1a**.

K_eff = 10 GPa widens everything; widening is monotone with Cl up to 1.6:

| | LPSCl0.5 | LPSCl1.0 | LPSCl1.5 | modelc | LPSCl2.0 |
|---|---|---|---|---|---|
| width (V) | 1.05 | 1.34 | 1.91 | **2.16** | 1.87 |

K_eff = 20 GPa amplifies the effect strongly:

| | LPSCl0.5 | LPSCl1.0 | LPSCl1.5 | **modelc** | LPSCl2.0 |
|---|---|---|---|---|---|
| reduction (V) | 0.23 | 0.02 | −0.15 | **−0.18** | −0.40 |
| oxidation (V) | 1.31 | 1.68 | 2.66 | **3.11** | 2.20 |
| width (V) | 1.09 | 1.66 | 2.81 | **3.30** | 2.60 |
| Δ vs 0 GPa width | +0.07 | +0.66 | +1.79 | **+2.28** | +1.46 |

Reading top-to-bottom on the oxidation row at K_eff = 20 GPa: anodic limit drops with Cl on the Cl-poor side (Cl<1) and **rises sharply** on the Cl-rich side (Cl 1.5, 1.6), then partially reverses at Cl = 2.0 — i.e. **modelc (Cl=1.6) sits at the apparent optimum** of the constriction-induced oxidation limit.

### Comparison to Gil-González Fig 1a

Their Fig 1a curve shows window-width vs Cl content with three lines for K_eff = 0 / 10 / 20 GPa. Qualitative match:

| Feature | Their Fig 1a | Our calc |
|---|---|---|
| 0 GPa: window flat across Cl | yes | **yes (1.01–1.14 V)** |
| 10–20 GPa: Cl-rich widens more | yes | **yes, monotone Cl=0.5→1.6** |
| Cl=2.0 not the maximum (different phase) | yes (LPSCl2.0 = C2mm orthorhombic) | **yes (different decomp path → ε_RXN drops back, width 2.6 < 2.8 of LPSCl1.5)** |
| Anodic limit at K=20 GPa, Cl=1.5 | ≈ 4.3 V (their value) | **2.66 V (ours, leading-order)** |

The absolute oxidation voltages differ by ~1.5 V because our leading-order shift uses K_eff = effective bulk modulus directly while Gil-González does the full Lagrange re-minimisation that lets the product set itself reorganise at higher K_eff (their products become SCl4 + Li2PS3 + S at K=20). The **slopes / orderings / qualitative trends agree**, which is what we set out to reproduce.

## What this tells us about modelc

modelc (Cl = 1.6) sits **inside the "Cl-rich sweet spot"** Gil-González identified:

- 0 GPa onset identical to comp1 (no advantage if no constriction)
- under constriction the Cl-rich oxidation products (bulky 1.6 LiCl) carry the highest ε_RXN of the series → anodic limit rises the most → window widens the most (3.30 V at 20 GPa)
- Cl = 2.0 is past the sweet spot because the decomposition path itself changes to P2S7-bearing chemistry, which is denser and doesn't gain as much from constriction.

So Paper #1 can quote: **"At realistic cell pressures (10–38 MPa formation → tens of GPa local K_eff at particle contacts), modelc's Cl-rich composition sits at the constriction-induced oxidation-stability optimum of the LPSCl_x family, reproducing the trend Gil-González et al. (Energy Storage Mater. 2022, Fig 1a) identified."**

## Limits / caveats

- **Leading-order edge shift only.** φ_ox += K_eff·ΔV / n_e, φ_red −= K_eff·ΔV_red / n_e. This is exact at small K_eff·ΔV; at K_eff = 20 GPa it underestimates Gil-González's full Lagrange result because we don't re-minimise the product set itself at K > 0. A second-order pass (re-build the augmented hull at each K_eff and re-extract the onset reactions) is the obvious next refinement.
- **V_SE for non-MP compositions.** LPSCl0.5/1.5/2.0 don't have MP entries; we used approximate volumes. The trend is robust; absolute values would tighten with EOS V0 from our own DFT.
- **Phase set exclusions.** Following Gil-González SI, we drop LiS4 (mp-995393), SCl3 (mp-1186934), Li5PS4Cl2 (mp-1040450). This shifts our LPSCl1.0 anodic onset from 2.14 V (LiS4 included) to 2.26 V (excluded), matching their 2.40 V better.
- **Reference at K_eff = 0** is the chemical convex hull; we keep elemental Li **un-augmented** so the V vs Li/Li+ reference is a fixed anode reservoir (cathode-side constriction only).

## Open follow-ups

1. **Full Lagrange re-min** at each K_eff (rebuild augmented hull with `+K_eff·V_i` on every solid phase, take `get_element_profile` again). Would close the absolute-voltage gap to Gil-González. Code-wise, an existing earlier version of `constrained_esw.py` (the one we discarded for the strain-explicit rewrite) already builds the augmented hull; can be hybridised.
2. **DFT EOS V0 for LPSCl0.5 / 1.5 / 2.0** so V_SE isn't approximated. Optional; not on the critical path.
3. **Plot.** A clean `width vs Cl` plot with 3 lines for K_eff = 0 / 10 / 20 reproduces Gil-González Fig 1a directly; one figure for the seminar.
