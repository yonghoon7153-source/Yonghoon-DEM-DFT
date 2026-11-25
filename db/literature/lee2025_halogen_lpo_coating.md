# Lee et al. 2025 — Halogen-programmed Li3PO4 coating (LPOFCl)

**Citation**: Lee, J.; Moon, H.; Lee, J.; Kim, Y.; Kim, G.; Kim, B.; Yoo, J.; Kang, M.
*Halogen-programmed Li3PO4 coating for self-adaptive and durable interfaces in sulfide-based all-solid-state batteries.*
Chem. Eng. J. **530**, 173574 (2026). DOI: 10.1016/j.cej.2026.173574.

## System
- Coating material: **LPOFCl** = halogen-co-substituted Li3PO4 with F⁻ + Cl⁻ replacing O in PO4³⁻
- Synthesis: co-precipitation (LiOH·H₂O + NH₄F + NH₄Cl + H₃PO4, O:F:Cl = 1:0.05:0.05), 550 °C 3 h in O₂
- Layer thickness: ~3 nm conformal on NCM811
- SSE pair: **LPSCl (Li₆PS₅Cl)**

## DFT methodology (VASP)
| Setting | Value |
|---|---|
| Code | VASP, PAW |
| XC | GGA-PBE |
| Cutoff | 500 eV plane-wave |
| Electronic conv | 1e-6 eV |
| Force conv | 0.01 eV/Å |
| K-grid | Γ-centered MP, 0.5 Å⁻¹ (coarse) |
| Smearing | Methfessel-Paxton, width 0.2 eV |
| Halogen model | Replace 1 O in PO4³⁻ → F or Cl, relax (charge-neutral) |
| NEB | 12 images + spring 5 eV/Å² (residual forces <0.01 eV/Å) |

## Key DFT results
- **Li⁺ migration barrier**: 0.62 eV (pristine LPO) → **0.41 eV (LPOFCl)** ≈ 34 % reduction
- Lattice volume expansion: ΔV/V ≈ 0.6 % (slight)
- Three cooperative effects:
  1. Electrostatic potential modulation by F⁻/Cl⁻ substitution (asymmetric, polarization gradient)
  2. Enhanced Li⁺ polarizability (Cl⁻ larger ionic radius broadens potential well)
  3. Weakened Li–O bonding due to F⁻-induced charge redistribution
- **Interfacial free energy ΔG** (LPSCl vs coating):
  - Pristine LPSCl ↔ LPO: −18.61 eV
  - **LPSCl ↔ LPOFCl: −27.71 eV** (much more thermodynamically favorable)

## Relevance to paper #1 / #2
- **Halogen substitution analogy**: F⁻ + Cl⁻ co-sub in Li3PO4 lattice = analogous to our Cl/Br mixing in argyrodite. Both yield (a) lattice distortion, (b) electrostatic field gradient, (c) reduced Li migration barrier.
- **Migration barrier reduction mechanism**: same physical picture (polarizability + soft Li-X bonds) we cite for Cl/Br modulation.
- **F⁻/Cl⁻ co-substitution synergy** > single halogen — supports our argument that mixed-halogen optimization outperforms pure Cl or pure Br.
- **Numerical baseline**: 0.41 eV LPOFCl migration barrier vs ~0.2–0.3 eV argyrodite barrier — argyrodite is far more conductive, but the qualitative trend (halogen mix lowers barrier) is consistent.

## Methodology contrast with our work
| Aspect | Lee 2025 (Coating) | Our paper (Argyrodite) |
|---|---|---|
| Code | VASP | Quantum ESPRESSO |
| XC | PBE | PBE (SSSP_1.3.0) |
| K-grid | 0.5 Å⁻¹ (coarse) | 2×2×2 EOS, 6×6×3 post-proc |
| Cutoff | 500 eV | ecutwfc=52 Ry (~708 eV) |
| Methodology | Static + NEB | EOS scan + elastic + finite-strain |

## Tagged for citation in
- Introduction: halogen substitution for Li transport enhancement
- Discussion: interfacial coating engineering (paper #2 narrative)
- Methods: NEB / activation barrier comparison

**Verified**: read pages 1–5, 11–17 directly (2026-05-22 session).
