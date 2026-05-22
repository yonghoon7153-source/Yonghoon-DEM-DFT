# Fadillah et al. 2025 — Molecular surface engineering of LPSClBr (= our comp2)

**Citation**: Fadillah, L.; Braks, L.; Oh, J.; Liu, M.; Türk, H.; Tisi, D.; Mensi, M.; Ceriotti, M.; Choi, J. W.; Coskun, A.
*Molecular Surface Engineering of Sulfide Electrolytes with Enhanced Humidity Tolerance for Robust Lithium Metal All-Solid-State Batteries.*
Adv. Mater. **2025**, e15013. DOI: 10.1002/adma.202515013.

## System
- **LPSClBr = Li₆PS₅Cl₀.₅Br₀.₅** ← matches our **comp2** family exactly
- Coating: octadecyl phosphonic acid (OPA) or lithiated form (Li-OPA), single-step wet-mix
- Coating amount: 2 wt% optimal
- Target: stabilize both anode (Li metal) + cathode (NCM811) interfaces

## Computational methodology
- ML potential: **PET (Point Edge Transformer)** trained on **MAD (Massive Atomic Diversity)** universal dataset
- Simplified surface: LPSCl(100) Cl-terminated (Br migrates to bulk per Monte Carlo — relevant insight!)
- OPA modeled with 5-carbon alkyl chain (instead of 18-carbon) for efficiency
- DFT (unspecified package) confirms adsorption energies

## Key results
- **Adsorption energies (DFT)**:
  - OPA-H on LPSCl(100): E_ad = **3.856 eV**
  - Li-OPA on LPSCl(100): E_ad = **5.174 eV** (stronger anchoring)
- **Surface halogen ordering (MC)**: Cl preferentially at surface, **Br migrates to bulk** even if initially placed at surface (=relevant for our halogen partitioning narrative!)
- LPSClBr ionic conductivity: 5.7 mS/cm pristine, retained 92% after 24h dry-room exposure with Li-OPA coating

## Electrochemistry
- Critical current density: 0.8 → 2.4 mA/cm² with Li-OPA coating
- 400 h Li plate/strip at 1.0 mAh/cm²
- NMC811 full cell: 160 mAh/g at 0.3C, 99.7% CE, 85% retention 100 cycles

## Relevance to paper #1 / #2
- **Direct comp2 citation source**: LPSClBr at exactly Cl₀.₅Br₀.₅ stoichiometry — matches our comp2 (Li₆PS₅Cl₀.₅Br₀.₅).
- **Halogen partitioning insight**: MC simulations show Cl prefers (100) surface, Br migrates to bulk.
  → Supports our argument that Cl vs Br site preference matters for mechanical/electrochemical properties.
  → Could be cited for the "halogen-position-dependent stability" discussion in paper #2.
- **DFT adsorption energy reference values**: useful for paper #2 coating/interface energetics calibration.
- **ML potential approach** (PET/MAD): alternative to our UMA — worth contrasting in supplementary methods.

## Methodology contrast with our work
| Aspect | Fadillah 2025 | Our paper |
|---|---|---|
| ML potential | PET trained on MAD | UMA-s-1p1 |
| LPSClBr DFT | Unspecified, surface (100) only | QE PBE EOS + elastic, 5 f.u. cell |
| Halogen modeling | MC for site ordering | Enumerate then UMA screen |
| Composition | Comp2 only (Cl0.5Br0.5) | All comp1–5 + modelC |
| Property focus | Surface stability, coating | Bulk mechanical (B0, E, Cij) |

**Verified**: read pages 1–6 directly (2026-05-22 session).
