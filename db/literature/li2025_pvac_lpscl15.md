# Li et al. 2025 — PVAC@LPSCl/LPSCl1.5 composite electrolyte film

**Citation**: Li, X.; Guo, Y.; Wang, Y.; Liu, J.; Wu, Z.; Wang, D.
*Physicochemical Dual-Force-Driven PVAC@LPSCl Composite Electrolyte Film for High-Performance All-Solid-State Batteries.*
Adv. Funct. Mater. **2025**, e12635. DOI: 10.1002/adfm.202512635.

## System
- Polymer binder: **PVAC** (polyvinyl acetate, ester-functional non-polar polymer)
- Argyrodite: **LPSCl** (Li₆PS₅Cl, x=0) and **LPSCl1.5** (Li₅.₅PS₄.₅Cl₁.₅, x=0.5)
  - LPSCl1.5 = **close to our modelC (Li₅.₄PS₄.₄Cl₁.₆) but not identical** (their Li5.5 vs ours Li5.4)
- Film: 50 μm thick PVAC@LPSCl1.5 composite (7 wt% PVAC, 93 wt% S-LPSCl1.5)

## DFT methodology (per Supporting Information)
- Code: **VASP + PAW**
- XC: **PBE-GGA**
- Cutoff: **400 eV** (low — surface adsorption only)
- K-points: **single Γ point** (no Brillouin sampling — surface slab only valid)
- All atoms fully relaxed (force convergence not given in excerpt)
- Charge density difference + adsorption energy calculations on LPSCl (001) surface
- **Limitation**: settings adequate for binder-surface adsorption energy but NOT for bulk EOS/elastic/conductivity calculations
- Tensile test: HR30 Discovery Hybrid Rheometer-DMA (TA Instruments)

## Key DFT-derived data — adsorption energies on LPSCl(001)
| Binder | ΔE_ads (eV) |
|---|---|
| PVDF | −1.76 (strongest, but incompatible solvent) |
| **PVAC** | **−0.90** (chosen, ester carbonyl Li-O coordination, bond ≈1.93 Å) |
| PEO | −0.77 |
| PEVA | −0.64 |
| SBR / NBR | −0.34 |
| SBS | −0.12 |
| PIB | −0.05 |

## Material data — LPSCl1.5 (close to modelC)
- Ionic conductivity (S-LPSCl1.5 pristine): **2.01 × 10⁻³ S/cm** (this is the "B-LPSCl1.5" / "S-LPSCl1.5" labeled curve)
- E-LPSCl1.5 (film with 7% PVAC binder): 2.80 mS/cm
- Tensile strength of film: **1.2 MPa** (very soft, ductile)
- Yield + ultimate stress 1.0 / 1.2 MPa
- Air stability (H₂S evolution rate): 2× lower with PVAC vs naked LPSCl1.5
- Bulk LPSCl ionic conductivity (ref): 0.84 mS/cm at RT

## Electrochemistry
- CCD: 1.59 mA/cm² (B-LPSCl1.5/Li) → **3.18 mA/cm²** (E-LPSCl1.5)
- Li symm 1000 h at 1.27 mA/cm², 12 mV polarization
- NMC811 full cell: 87.3% retention 200 cycles at 0.5C

## Relevance to paper #1 / #2
- **LPSCl1.5 ≈ our modelC**: their Li₅.₅PS₄.₅Cl₁.₅ vs our Li₅.₄PS₄.₄Cl₁.₆ — same Cl-rich halogen substitution family (Adeli 2019 framework). Their conductivity (2.0 mS/cm pristine) is a useful benchmark.
- **Mechanical contrast**: their composite film 1.2 MPa tensile strength = very soft (binder-dominated). Our modelC bulk B0 = 21.7 GPa is a different regime (rigid sintered pellet). Could cite for "binder-vs-bulk" mechanical comparison.
- **DFT-guided binder selection** as methodology — could mirror for B2O3-doping paper #2 if exploring coating layer + binder synergy.
- **Critical insight**: Cl-rich substitution improves both lattice deformability AND conductivity — supports our paper #1 narrative about Cl/Br halogen tuning.

## Methodology contrast with our work
| Aspect | Li 2025 (PVAC) | Our paper |
|---|---|---|
| Composition | LPSCl (x=0), LPSCl1.5 (x=0.5) | comp1-5 + modelC family |
| Property | Adsorption energy on (001) | Bulk B0, E, Cij + adhesion |
| Layer focus | Polymer-electrolyte interface | Bulk + SE/NCM interface |
| Conductivity | Reported 0.84 → 2.01 mS/cm | Not measured (mechanical focus) |

**Verified**: read pages 1–6 directly (2026-05-22 session).
