# Dopant site preference (antisite-swap, all-UMA) — 81-system screen

Method: `tools/doping/site_preference_swap.py` — same-composition M@P vs M@Li position
swap, both relaxed (UMA-s-1p1), ΔE = E(M@P) − E(M@Li). ΔE<0 → framework P site;
ΔE>0 → Li site. 81 systems (27 dopant oxides × 3 concentrations), 78 ok + 3 Li2O skip.
Per-element aggregate: `docs/figures/site_preference/site_pref_by_element.csv`.

## Headline
**Determinant = ability to be a framework former (small + high valence), not pure size.**
- **Tetravalent group-14 (Si⁴⁺, Ge⁴⁺, Sn⁴⁺) → P framework** (mean dE −0.96 eV; the ONLY
  clear P-preferrers). They substitute P⁵⁺ in the PS₄ tetrahedron.
- **Large di/tri-valent (alkaline-earth Ca/Sr/Ba, rare-earth La/Nd/Sm/Gd/Y, Na, Ag, late-TM)
  → Li site** (mean +1.57 eV for r>0.9 Å). Too large / wrong valence for the tetrahedron.
- **B, Al = borderline / flip** (mean ≈ 0–0.3). B (r 0.27) is small enough for P but B³⁺
  prefers B–O (borate) → competes between framework-P and Li/O region.
- Pearson r(ionic radius, mean dE) = **0.67** — a real but noisy size trend (valence breaks it:
  group-14 +4 are P-preferrers despite Sn being mid-size).

## Answers to the live questions
- **B@P (PI's DFT setup)**: DEFENSIBLE but borderline. B prefers P at x005/x010 (dE −0.41/−0.21)
  yet flips to Li at x002 (+0.76). B genuinely competes between framework-P and borate(Li/O).
  → Running B@P is valid; do NOT claim "B clearly prefers P" — it is one of two motifs.
- **Nd → Li (robust)**: dE +0.33/+0.92/+2.42 across x002/005/010, all Li, mean +1.22.
  Confirms the Nd@Li / Li-channel-blocking picture (consistent with σ↓ vs modelc).
- **Y vs Nd — NOT a site difference**: Y also → Li (dE +0.47/+2.31/+2.51, mean +1.76), even
  more strongly than Nd. So the earlier "Y@P (ionic↑) vs Nd@Li (ionic↓) is a site effect"
  hypothesis is **NOT supported** here — both prefer Li. Whatever drives the Y-paper's ionic
  gain is not a clean site-preference difference from Nd in this screen.

## Honest method caveats
- **Large scatter / concentration flips**: the same element can flip P↔Li across x (Al, B, Cr,
  Ni, Sn-x005, Ge-x010). The antisite-swap ΔE is sensitive to the specific champion config and
  to which P/Li is chosen for the swap → treat as a **coarse, semi-quantitative screen**, not a
  precise per-element verdict. Robust conclusions are the **extremes** (group-14 → P; large
  RE/alkaline-earth → Li); the middle (B/Al/TM) is ambiguous.
- **Non-converged M@P** (conv=n: Al2O3_x002, Ag2O_x002/x010): big-cation-on-P is intrinsically
  high-strain and may not reach fmax → those dE are upper bounds (sign still trustworthy for
  large cations).
- Same-composition swap includes the displaced-host (P↔Li) antisite penalty — intrinsic to a
  fixed-composition comparison; the SIGN and cross-element ranking are the usable signal.
- Li2O/Li-led "dopants" skipped (anion-on-chalcogen, cation P-vs-Li N/A).

## Takeaway for the paper
A clean, defensible statement: **"Tetravalent group-14 dopants enter the P (framework) site;
larger di/tri-valent cations — including all rare earths and alkaline earths — occupy the Li
site and thus impede the Li sublattice."** B is a borderline framework/borate case; Nd robustly
takes the Li site (channel-blocking). Y behaves like Nd (Li), so the Y↑/Nd↓ ionic contrast is
not explained by site preference alone.
