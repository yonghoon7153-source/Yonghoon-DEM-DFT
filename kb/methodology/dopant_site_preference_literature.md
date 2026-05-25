# Dopant Site Preference — Literature-Grounded Assignments

> **v4.5.24 LITERATURE-PREFERRED policy** (reviewer-bound). For each
> dopant documented here, the cascade restricts substitution to these
> literature-supported Wyckoff sites, dropping radius-only placements
> with no literature backing (e.g. O→Cl_4d, Sn⁴⁺→Li removed).
> Undocumented elements fall back to the Shannon-radius+charge filter.
>
> Source: `tools/doping/site_preference.py::LITERATURE_SITES`.
> Host sites: Li_24g/Li_48h (Li⁺), P_4b (P⁵⁺, PS4 center),
> S_16e (PS4-bonded S²⁻), S_4a (free S²⁻/Li2S-like), Cl_4d (halide).

## Li-site cations (substitute Li⁺, aliovalent → Li vacancy compensation)

| Dopant | charge | radius(Å) | predicted site(s) | reason / reference |
|---|---|---|---|---|
| Cu | +1 | 0.77 | Li_24g, Li_48h | Cu⁺→Li isovalent |
| Na | +1 | 1.02 | Li_24g, Li_48h | Na→Li isovalent (common) |
| Ag | +1 | 1.15 | Li_24g, Li_48h | Nature Comm 2025 Ag-exsolution argyrodite |
| Ni | +2 | 0.69 | Li_24g | Ni²⁺ → Li site (NMC parent, DOPANT_DB) |
| Mg | +2 | 0.72 | Li_24g | Mg²⁺→Li aliovalent (common) |
| Zn | +2 | 0.74 | Li_24g | Zn²⁺→Li; Sundar 2025 ZnO coating |
| Co | +2 | 0.745 | Li_24g | Co²⁺ → Li site (NMC parent, DOPANT_DB) |
| Mn | +2 | 0.83 | Li_24g | Mn²⁺ CN6 → Li site (DOPANT_DB) |
| Ca | +2 | 1.0 | Li_24g | Li5.35Ca0.1PS4.5Cl1.55, 10.2 mS/cm |
| Sr | +2 | 1.18 | Li_24g | Sr²⁺→Li (larger alkaline earth) |
| Ba | +2 | 1.35 | Li_24g | PMC 11106650 mechanochemical Li6-aBa_a/2PS5Cl (borderline radius) |
| Al | +3 | 0.535 | Li_24g, P_4b | Li5.4Al0.1PS4.7Cl1.3 7.29mS/cm (Li-site); Al³⁺ also P-acceptor (amphoteric) |
| Cr | +3 | 0.615 | Li_24g | Cr³⁺ CN6 → Li site (DOPANT_DB) |
| Ga | +3 | 0.62 | Li_24g | Ga³⁺→Li aliovalent |
| Fe | +3 | 0.645 | Li_24g | Fe³⁺ CN6 → Li site (DOPANT_DB) |
| Sc | +3 | 0.745 | Li_24g | Sc³⁺→Li aliovalent |
| In | +3 | 0.8 | Li_24g | In³⁺→Li aliovalent |
| Lu | +3 | 0.861 | Li_24g | Lu³⁺→Li RE (smallest Ln) |
| Yb | +3 | 0.868 | Li_24g | Yb³⁺→Li RE |
| Tm | +3 | 0.88 | Li_24g | Tm³⁺→Li RE |
| Er | +3 | 0.89 | Li_24g | Er³⁺→Li RE |
| Y | +3 | 0.9 | Li_24g | mechanochemical Y-doped LPSCl |
| Ho | +3 | 0.901 | Li_24g | Ho³⁺→Li RE |
| Dy | +3 | 0.912 | Li_24g | Dy³⁺→Li RE |
| Tb | +3 | 0.923 | Li_24g | Tb³⁺→Li RE |
| Gd | +3 | 0.938 | Li_24g | Gd³⁺→Li RE oxide |
| Eu | +3 | 0.947 | Li_24g | Eu³⁺→Li RE |
| Sm | +3 | 0.958 | Li_24g | Sm³⁺→Li RE oxide |
| Nd | +3 | 0.983 | Li_24g | Nd³⁺→Li; paper#2 Nd2O3 case study |
| Pr | +3 | 0.99 | Li_24g | Pr³⁺→Li RE |
| Bi | +3 | 1.03 | Li_24g | Bi³⁺→Li (Bi2S3/Bi2O3 SE doping) |
| La | +3 | 1.032 | Li_24g | La³⁺→Li; Sundar 2025 / paper#2 RE oxide |
| Ce | +4 | 0.87 | Li_24g, P_4b | Ce⁴⁺ (CeO2) — Li or P depending on valence |

## P-site cations (substitute P⁵⁺ in PS4 tetrahedron)

| Dopant | charge | radius(Å) | predicted site(s) | reason / reference |
|---|---|---|---|---|
| B | +3 | 0.11 | P_4b | Lee 2025 CEJ: B³⁺ PO4-cluster (P-site acceptor) |
| Si | +4 | 0.4 | P_4b | Si⁴⁺→P acceptor (LGPS family) |
| Ge | +4 | 0.53 | P_4b | Ge⁴⁺→P (LGPS family) |
| Ti | +4 | 0.605 | P_4b | Ti⁴⁺→P acceptor |
| Sn | +4 | 0.69 | P_4b | MDPI Materials 16(7),2751 (2023) Sn-substituted LPSCl |
| Hf | +4 | 0.71 | P_4b | Hf⁴⁺→P (5d analogue of Zr) |
| Zr | +4 | 0.72 | P_4b | Zr⁴⁺→P acceptor |
| As | +5 | 0.46 | P_4b | As⁵⁺→P isovalent |
| V | +5 | 0.54 | P_4b | V⁵⁺→P isovalent |
| Sb | +5 | 0.6 | P_4b | Sb⁵⁺→P isovalent (common) |
| Nb | +5 | 0.64 | P_4b | Nb⁵⁺→P isovalent |
| Ta | +5 | 0.64 | P_4b | Ta⁵⁺→P (5d analogue of Nb) |
| Mo | +6 | 0.41 | P_4b | Mo⁶⁺ thiophosphate donor (DOPANT_DB) |
| W | +6 | 0.42 | P_4b | W⁶⁺ thiophosphate donor (DOPANT_DB) |
| Re | +7 | 0.53 | P_4b | Re⁷⁺ high-valence P substitution (DOPANT_DB) |

## Anions → S²⁻ sublattice (PS4 or free S)

| Dopant | charge | radius(Å) | predicted site(s) | reason / reference |
|---|---|---|---|---|
| N | -3 | 1.46 | S_16e | N³⁻ → PS4 S (aliovalent nitride doping) |
| O | -2 | 1.4 | S_16e, S_4a | ACS AMI 2021 oxysulfide Li6PS5-xClOx (best=S_16e, PS4-bonded) |
| Se | -2 | 1.98 | S_16e, S_4a | Se→S isovalent (chalcogen swap) |
| Te | -2 | 2.21 | S_16e, S_4a | Te→S isovalent (chalcogen swap) |

## Anions → Cl⁻ halide sublattice

| Dopant | charge | radius(Å) | predicted site(s) | reason / reference |
|---|---|---|---|---|
| F | -1 | 1.33 | Cl_4d | ACS AMI 2022 F-doped argyrodite (F→Cl⁻ halide site) |
| Cl | -1 | 1.81 | Cl_4d, S_4a | Adeli 2019 halogen-rich (Cl on 4d + free S_4a anion) |
| Br | -1 | 1.96 | Cl_4d, S_4a | halogen mixing Li6PS5(Cl,Br) (comp2 family) |
| I | -1 | 2.2 | Cl_4d | I-F dual-doped JPCC 2023 |

## Undocumented — radius/charge filter fallback

이 원소들은 LITERATURE_SITES에 없어 Shannon-radius+charge 필터로만 site 결정:

| Dopant | charge | radius(Å) | radius-filter site(s) |
|---|---|---|---|
| K | +1 | 1.38 | (none) |
| H | +1 | -0.04 | P_4b |

## Policy rationale (for reviewer)

- **Why literature-preferred?** The Shannon-radius cutoff (RADIUS_TOL)
  is a necessary but not sufficient filter: it admits sign-correct,
  size-tolerable but chemically unreported placements (O on the Cl⁻
  site, Sn⁴⁺ on the Li⁺ site). Restricting documented dopants to their
  literature sites removes these, so every screened (compound, site)
  pair is defensible and UMA compute is not spent on implausible cells.
- **Charge-sign rule** (cation↔cation, anion↔anion) is always enforced,
  even for literature sites.
- **Amphoteric cases** (Al³⁺, Ce⁴⁺) list both Li and P sites — both are
  literature-reported and let UMA energy decide the winner.
- **Fallback**: undocumented elements keep the radius filter, so adding
  a new dopant still works without a LITERATURE_SITES entry.
