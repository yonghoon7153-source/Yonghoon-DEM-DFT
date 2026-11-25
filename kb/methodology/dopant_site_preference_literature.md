# Dopant Site Preference — Literature-Anchored Heuristic Assignments (v4.5.26)

> **NOT pure literature-grounded** — это literature-ANCHORED heuristic:
> **cited 14** (concrete paper/DOI) · **standard 15** (textbook isovalent/aliovalent) · **analogy 24** (chemical analogy + caveat).
> Paper must report this confidence distribution so reviewers judge reliability themselves (reviewer round-2).
>
> **Policy**: documented dopants RESTRICTED to listed sites (radius-only spurious sites dropped); charge-sign always enforced; undocumented → radius/charge fallback.
> **Site assignment basis**: ionic radius + charge-sign + HSAB hard/soft-acid heuristic, literature-anchored where available.
> Source: `tools/doping/site_preference.py::LITERATURE_SITES`. Two review rounds (2026-05-19).

## Confidence-tier usage caveat (reviewer round-2)

- **cited/standard** dopants: site assignment defensible, use directly.
- **analogy** dopants (RE 11, 3d-TM 5, Zr/Hf, W/Mo/Re/N/Sr/Sc...): heuristic.
  Report Layer-2 results for these SEPARATELY (do not pool with cited).
- **3d TM (Cr,Mn,Fe,Co,Ni)**: lattice substitution unconfirmed — separate
  sulfide phase (FeS/CoS/NiS) may be more stable. Li_24g is a heuristic
  restriction (blocks radius's spurious P_4b), NOT a confirmed placement.
- **radius-fallback (B,Ce,Bi)**: no literature claim; B³⁺→P_4b geometric only.

## Open items (paper-text, do not block batch)

- **As/Sb valence**: LITERATURE_SITES has +5 only; As2S3/Sb2S3 precursors are
  +3 → Li-vacancy count may be off (MLIP relaxation compensates site). P1.
- **DOI verify**: Ba (PMC 11106650), Ag (Nature Comm 2025), F (2022 vs 2024).

## Li-site cations

| Dopant | q | r(Å) | site(s) | conf | reason/ref |
|---|---|---|---|---|---|
| Cu | +1 | 0.77 | Li_24g, Li_48h | standard | Cu⁺→Li⁺ isovalent |
| Na | +1 | 1.02 | Li_24g, Li_48h | standard | Na⁺→Li⁺ isovalent (standard) |
| Ag | +1 | 1.15 | Li_24g, Li_48h | cited | Nature Comm 2025 Ag-exsolution argyrodite (verify DOI) |
| Ni | +2 | 0.69 | Li_24g | analogy | Ni²⁺→Li (heuristic; NiS phase-separation risk) |
| Mg | +2 | 0.72 | Li_24g | standard | Mg²⁺→Li aliovalent (standard) |
| Zn | +2 | 0.74 | Li_24g | cited | Zn²⁺→Li; Sundar 2025 ZnO coating |
| Co | +2 | 0.745 | Li_24g | analogy | Co²⁺→Li (heuristic; CoS phase-separation risk) |
| Mn | +2 | 0.83 | Li_24g | analogy | Mn²⁺→Li (heuristic; lattice sub. unconfirmed) |
| Ca | +2 | 1.0 | Li_24g | cited | Li5.35Ca0.1PS4.5Cl1.55, 10.2 mS/cm (specific composition) |
| Sr | +2 | 1.18 | Li_24g | analogy | Sr²⁺→Li by Ca analogue (larger alkaline earth) |
| Ba | +2 | 1.35 | Li_24g | cited | PMC 11106650 mechanochemical Li6-aBa_a/2PS5Cl (radius borderline) |
| Al | +3 | 0.535 | Li_24g | cited | Li5.4Al0.1PS4.7Cl1.3 7.29mS/cm (PMC9783369, Li-site aliovalent) |
| Cr | +3 | 0.615 | Li_24g | analogy | Cr³⁺→Li (heuristic; lattice sub. unconfirmed, may phase-separate) |
| Ga | +3 | 0.62 | Li_24g | standard | Ga³⁺→Li aliovalent (group-13) |
| Fe | +3 | 0.645 | Li_24g | analogy | Fe³⁺→Li (heuristic; FeS phase-separation risk) |
| Sc | +3 | 0.745 | Li_24g | analogy | Sc³⁺→Li aliovalent (Y analogue) |
| In | +3 | 0.8 | Li_24g | standard | In³⁺→Li aliovalent (too large for P-site) |
| Lu | +3 | 0.861 | Li_24g | analogy | Lu³⁺→Li by RE analogy (smallest Ln) |
| Yb | +3 | 0.868 | Li_24g | analogy | Yb³⁺→Li by RE analogy |
| Tm | +3 | 0.88 | Li_24g | analogy | Tm³⁺→Li by RE analogy |
| Er | +3 | 0.89 | Li_24g | analogy | Er³⁺→Li by RE analogy |
| Y | +3 | 0.9 | Li_24g | cited | mechanochemical Y-doped LPSCl |
| Ho | +3 | 0.901 | Li_24g | analogy | Ho³⁺→Li by RE analogy |
| Dy | +3 | 0.912 | Li_24g | analogy | Dy³⁺→Li by RE analogy |
| Tb | +3 | 0.923 | Li_24g | analogy | Tb³⁺→Li by RE analogy |
| Gd | +3 | 0.938 | Li_24g | analogy | Gd³⁺→Li by RE analogy |
| Eu | +3 | 0.947 | Li_24g | analogy | Eu³⁺→Li by RE analogy |
| Sm | +3 | 0.958 | Li_24g | analogy | Sm³⁺→Li by RE analogy (Nd/La anchored) |
| Nd | +3 | 0.983 | Li_24g | cited | Nd³⁺→Li; paper#2 Nd2O3 case study (anchor) |
| Pr | +3 | 0.99 | Li_24g | analogy | Pr³⁺→Li by RE analogy |
| La | +3 | 1.032 | Li_24g | cited | La³⁺→Li; Sundar 2025 / paper#2 RE oxide |

## P-site cations (PS4 center)

| Dopant | q | r(Å) | site(s) | conf | reason/ref |
|---|---|---|---|---|---|
| Si | +4 | 0.4 | P_4b | cited | ScienceDirect S0013468621017217 Si substitution on P-site argyrodite |
| Ge | +4 | 0.53 | P_4b | standard | Ge⁴⁺→P isovalent analogue (LGPS is Ge-structural, not LPSCl Ge-doping cited) |
| Ti | +4 | 0.605 | P_4b | standard | Ti⁴⁺→P acceptor (group-14/-4 analogue) |
| Sn | +4 | 0.69 | P_4b | cited | MDPI Materials 16(7) 2751 (2023) DOI 10.3390/ma16072751: P→Sn, Sn–S bond |
| Hf | +4 | 0.71 | P_4b, Li_24g | analogy | Hf⁴⁺ amphoteric: charge→P, radius(0.71≈Li)→Li (heuristic; 5d analogue of Zr) |
| Zr | +4 | 0.72 | P_4b, Li_24g | analogy | Zr⁴⁺ amphoteric: charge→P, radius(0.72≈Li 0.76)→Li (heuristic) |
| As | +5 | 0.46 | P_4b | standard | As⁵⁺→P⁵⁺ isovalent (standard) |
| V | +5 | 0.54 | P_4b | standard | V⁵⁺→P⁵⁺ isovalent |
| Sb | +5 | 0.6 | P_4b | standard | Sb⁵⁺→P⁵⁺ isovalent (standard thiophosphate) |
| Nb | +5 | 0.64 | P_4b | standard | Nb⁵⁺→P⁵⁺ isovalent |
| Ta | +5 | 0.64 | P_4b | standard | Ta⁵⁺→P⁵⁺ isovalent (5d analogue of Nb) |
| Mo | +6 | 0.41 | P_4b | analogy | Mo⁶⁺→P donor by analogy to MoS3 additions; weak direct LPSCl ref |
| W | +6 | 0.42 | P_4b | analogy | W⁶⁺→P donor by analogy to WS3 thiophosphate-glass additions; weak direct LPSCl ref |
| Re | +7 | 0.53 | P_4b | analogy | Re⁷⁺→P donor (heuristic; very high charge, large Δq compensation) |

## Anions → S²⁻

| Dopant | q | r(Å) | site(s) | conf | reason/ref |
|---|---|---|---|---|---|
| N | -3 | 1.46 | S_16e | analogy | N³⁻→PS4 S by analogy to LiPON N→O; NO direct LPSCl report (Li3N batch) |
| O | -2 | 1.4 | S_16e, S_4a | cited | Lee 2025 (ScienceDirect S2405829725000790): site-selective O at Wyckoff 16e of PS4; S_4a secondary |
| Se | -2 | 1.98 | S_16e, S_4a | standard | Se→S isovalent chalcogen substitution (standard) |
| Te | -2 | 2.21 | S_16e, S_4a | standard | Te→S isovalent chalcogen substitution (standard) |

## Anions → Cl⁻ halide

| Dopant | q | r(Å) | site(s) | conf | reason/ref |
|---|---|---|---|---|---|
| F | -1 | 1.33 | Cl_4d | cited | ACS AMI 2024 16(24) 31341 fluorine-like / LiF-doped argyrodite (F→Cl⁻ 4d) |
| Cl | -1 | 1.81 | Cl_4d, S_4a | cited | Adeli 2019 Angew halogen-rich Li6PS5Cl1+x (Cl 4d + free S_4a) |
| Br | -1 | 1.96 | Cl_4d, S_4a | cited | Kraft 2017 JACS halogen mixing Li6PS5(Cl,Br) (comp2 family) |
| I | -1 | 2.2 | Cl_4d | standard | I→Cl⁻ halide-site substitution (larger halide) |

## Undocumented → radius/charge fallback (heuristic, no literature claim)

| Dopant | q | r(Å) | radius site(s) |
|---|---|---|---|
| K | +1 | 1.38 | (none) |
| H | +1 | -0.04 | P_4b |
| Bi | +3 | 1.03 | Li_24g, Li_48h |
| B | +3 | 0.11 | P_4b |
| Ce | +4 | 0.87 | Li_24g, Li_48h |
