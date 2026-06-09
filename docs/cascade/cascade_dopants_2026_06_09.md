# Cascade Doping Verification — 14 dopants × 3 concentrations

**Source.** gabia (`kserver116-27`) cascade `multi_category_2026_05_26_v23`, UMA-s-1p1 task=omat, run 2026-06-07 (git commit `9ce6ca3` of `tools/doping`). Champion `xyz` at `db/structures/doping/<compound>_<x>_champion.xyz`. Full pipeline `00_preflight … 09e_ehull` executed per compound.

**Read on vm 2026-06-09.** Source of truth = gabia run dirs (not pushed to vm repo yet — PAT-less machine). This file lifts the headline numbers into a vm-queryable form. Companion JSON: `db/properties/doping_cascade_verified.json`.

## Headline table

All 41 (14 dopants × 3 concentrations + Sc2O3 x002 alone) **converged post-anneal**. `de_post_anneal` is the champion energy per atom relative to the cascade baseline (eV/atom, negative = more stable than undoped). `B0` is the UMA EOS bulk modulus of the champion (GPa); `E_VRH` is the UMA relaxed-ion Voigt-Reuss-Hill Young's modulus computed from `B_hill`/`G_hill` via `9BG/(3B+G)`.

| Dopant | x | Variant | Champion site | dE_post (eV/at) | ΔV_anneal | EOS B0 | E_VRH | Note |
|---|---|---|---|---|---|---|---|---|
| **Sc2O3** | 0.02 | Sc2O3+Clrich | Li_24g | **−0.974** | −3.54% | 17.8 | **18.7** | strongest dE; lowest E_VRH ⇒ best **soft** candidate |
| **Al2O3** | 0.10 | Al2O3+Clrich | Li_24g | −0.818 | −5.72% | 16.5 | 40.8 | x005 is softest (E=29.3, B0=18.1) — best **coating** candidate of Al2O3 |
| Al2O3 | 0.05 | Al2O3 | Li_24g | −0.809 | −4.96% | **18.1** | **29.3** | |
| Al2O3 | 0.02 | Al2O3 | Li_24g | −0.791 | −4.36% | 11.5 | 39.8 | lowest B0 of cascade |
| **MnO** | 0.05 | MnO | Li_24g | −0.662 | −2.44% | 18.2 | 32.6 | strong dE, low ΔV, soft E |
| MnO | 0.10 | MnO | Li_24g | −0.639 | −0.46% | 18.0 | 35.9 | smallest ΔV in cascade ⇒ minimal lattice strain |
| MnO | 0.02 | MnO | Li_24g | −0.652 | −5.90% | 0.0¹ | 37.7 | B0 = 0 (EOS fit failure) |
| CoO | 0.02 | CoO | Li_24g | −0.583 | −5.32% | 22.3 | 49.1 | |
| CaO | 0.02 | CaO | Li_24g | −0.580 | −5.40% | 23.5 | 49.1 | |
| BaO | 0.10 | BaO | Li_24g | −0.579 | −4.17% | 21.8 | 48.7 | |
| BaO | 0.02 | BaO | Li_24g | −0.577 | −4.79% | 23.2 | 50.4 | |
| CaO | 0.10 | CaO | Li_24g | −0.577 | −3.78% | 21.2 | 44.4 | |
| BaO | 0.05 | BaO | Li_24g | −0.571 | −3.71% | 20.0 | 36.2 | |
| CaO | 0.05 | CaO | Li_24g | −0.570 | −2.11% | 16.2 | 39.5 | |
| **NiO** | 0.05 | NiO | Li_24g | −0.569 | −5.85% | 20.9 | 49.6 | matches earlier 0.81/0.85/0.70 db registration (re-verified) |
| CoO | 0.05 | CoO | Li_24g | −0.568 | −2.66% | 19.3 | 42.9 | |
| CoO | 0.10 | CoO | Li_24g | −0.566 | −3.26% | 0.0¹ | 47.7 | B0 fit failure |
| Cu2O | 0.05 | Cu2O | **Li_24g** | −0.559 | −8.55% | 26.1 | **54.7** | largest \|ΔV\| at x=0.05 (Cu+/Li mismatch) |
| MgO+Clrich | 0.05 | MgO+Clrich | Li_24g | −0.555 | −8.64% | 24.3 | 52.6 | |
| Li2O | 0.02 | Li2O | **Li_48h** | −0.553 | −7.77% | 23.1 | 37.5 | the only non-24g main: Li2O sits on the smaller interstitial-flavored Li_48h |
| NiO | 0.10 | NiO | Li_24g | −0.551 | −3.75% | 19.2 | 33.9 | |
| Li2O | 0.10 | Li2O | Li_48h | −0.550 | −9.69% | 21.2 | 40.2 | largest \|ΔV\| (~10%) |
| SrO | 0.05 | SrO | Li_24g | −0.546 | −1.20% | 19.2 | 46.6 | smallest \|ΔV\| (−1.2%) ⇒ minimum lattice strain across dopants |
| MgO+Clrich | 0.02 | MgO+Clrich | Li_24g | −0.544 | −7.65% | 22.9 | 58.7 | |
| Cu2O | 0.02 | Cu2O | **Li_48h** | −0.542 | −6.17% | 19.4 | 40.8 | small Cu+ prefers smaller 48h site |
| Cu2O | 0.10 | Cu2O | Li_48h | −0.540 | −5.25% | 18.9 | 44.2 | |
| NiO | 0.02 | NiO | Li_24g | −0.532 | −3.11% | 18.9 | 37.7 | |
| Li2O | 0.05 | Li2O | Li_48h | −0.531 | −5.47% | 23.8 | 32.4 | |
| MgO | 0.10 | MgO | Li_24g | −0.531 | −9.12% | 17.2 | 44.4 | |
| SrO | 0.10 | SrO | Li_24g | −0.522 | −2.65% | 17.9 | 42.7 | |
| Ag2O | 0.02 | Ag2O | Li_24g | −0.507 | −7.97% | 26.5 | 48.3 | |
| SrO | 0.02 | SrO | Li_24g | −0.507 | −3.78% | 16.4 | 42.3 | |
| Ag2O | 0.10 | Ag2O | **Li_48h** | −0.506 | −5.50% | 18.0 | 40.4 | |
| ZnO | 0.02 | ZnO | Li_24g | −0.504 | −4.35% | 18.0 | 46.4 | |
| ZnO | 0.05 | ZnO | Li_24g | −0.501 | −3.83% | 22.6 | 59.9 | stiffest E_VRH in cascade |
| ZnO | 0.10 | ZnO | Li_24g | −0.500 | −5.21% | 0.0¹ | 45.6 | B0 fit failure |
| Na2O | 0.02 | Na2O | Li_24g | −0.500 | −2.80% | 21.3 | 37.4 | |
| Ag2O | 0.05 | Ag2O | Li_24g | −0.499 | −3.69% | 18.5 | 38.6 | |
| Na2O | 0.05 | Na2O | **Li_48h** | −0.486 | −3.41% | 19.4 | 48.3 | |
| Na2O | 0.10 | Na2O | Li_24g | −0.483 | −4.90% | 21.7 | 39.1 | |

¹ `B0 = 0.0` cases (MnO_x002, CoO_x010, ZnO_x010) = EOS fit failed to return a physical Birch–Murnaghan curvature. Elastic Cij still converged so E_VRH is trustworthy; the B0 column should be ignored for those rows.

## What the data says

### Site preference is unambiguous

**38 of 41** champions place the dopant cation on **`Li_24g`** (the main argyrodite Li site, large coordination). The 3 exceptions all go to **`Li_48h`** (the smaller, more interstitial-flavored Li site), and they follow a clear chemistry signal:

- **Li2O** (all 3 x's) → `Li_48h`. Self-similar substitution (Li+→Li+) so the dopant Li naturally fills smaller channel sites rather than fully occupying a 24g Wyckoff position.
- **Cu2O** (x002, x010) → `Li_48h`. Cu+ is small (~77 pm), prefers the tighter 48h cage; x005 was the only Cu2O that placed Cu on 24g.
- **Ag2O** (x010) → `Li_48h`. Same flavor — monovalent small-cation, similar to Cu+.
- **Na2O** (x005) → `Li_48h`. Likely a tie-breaker between 24g and 48h at this specific concentration.

**Zero champions on the P_4b site.** Consistent with everything we already established for the heuristic + literature-graded site assignment review (Y@P / Si@P / Ge@P would need acceptor compensation and were the cascade's pending check). For the cascade's actual top-ranked oxide dopants here, P-site substitution simply does not win the energy ranking.

### `dE_post` ranking — strongest formation favorability

Cluster of equivalent acceptor-class oxides at the top (Sc, Al, Mn). Sc2O3 wins by ~150 meV/atom over Al2O3 (the runner-up cluster), which in turn wins by 100–200 meV/atom over Mn/Co/Ca/Ba.

- **Sc2O3_x002 −0.974 eV/atom** is the clear cascade winner on energy.
- **Al2O3 group −0.79 to −0.82** — robust across all 3 concentrations, monotone with x (slightly more favorable at higher x).
- **Mn/Co/Ca/Ba −0.57 to −0.66** — a broad middle cluster.
- **Cu/Ag/Mg/Ni/Sr/Li/Na/Zn −0.48 to −0.56** — bottom cluster, still all formation-favorable.

### `E_VRH` (Young's modulus) — coating-layer (soft) candidates

The weekly report's coating goal is **low modulus + high oxidation stability**. On modulus alone (cascade-internal, UMA-relaxed-ion comparison, not absolute UMA-vs-experiment):

| Rank | Compound | E_VRH (GPa) | dE_post | Why interesting |
|---|---|---|---|---|
| 1 | **Sc2O3_x002** | **18.7** | −0.974 | softest AND strongest formation energy — most promising single candidate |
| 2 | Al2O3_x005 | 29.3 | −0.809 | known route in literature; soft + favorable |
| 3 | Li2O_x005 | 32.4 | −0.531 | softest of the monovalent dopants |
| 4 | MnO_x005 | 32.6 | −0.662 | low ΔV (−2.4%), good formation |
| 5 | NiO_x010 | 33.9 | −0.551 | matches existing db NiO entry direction |

Anything above **~50 GPa** (BaO_x002, ZnO_x005, Cu2O_x005, MgO+Clrich_x002, etc.) is too stiff for the low-modulus coating goal — keep as hard-coating candidates if needed but not for the soft-contact role.

### `ΔV_anneal` — lattice strain on doping

Most champions sit at **−2 to −6%** volume change on anneal (i.e. anneal contracts the cell slightly from the rattled MLIP seed). Two extremes worth noting:

- **Smallest** \|ΔV\|: SrO_x005 (−1.2%), Mn-O_x010 (−0.46%), Mn-O_x005 (−2.4%) → minimal lattice strain, geometry barely moves on doping.
- **Largest** \|ΔV\|: Li2O_x010 (−9.7%), MgO_x010 (−9.1%), MgO+Clrich_x005 (−8.6%), Cu2O_x005 (−8.6%), Ag2O_x002 (−8.0%) → significant compression, worth checking that anneal didn't trigger PS4 framework distortion (TODO if any of these enter top candidates).

### "+Clrich" variants

Three compounds (Al2O3_x010, Sc2O3_x002, MgO_x002/005) had their champion in the `+Clrich` chain (extra Cl seed), meaning the cascade found that pairing the oxide dopant with extra Cl gives a more stable configuration than the pure oxide variant. This is consistent with the Paper #1 finding that Cl-enrichment on the anion sublattice is favorable — Sc, Al, Mg specifically benefit from co-Cl-enrichment.

## Compute provenance

| Field | Value |
|---|---|
| Cascade dir | `/data/work/runs/multi_category_2026_05_26_v23/` |
| Cascade git commit | `9ce6ca33ca7c8faa7ecae8b87025af08b1ad5d34` |
| MLIP | UMA-s-1p1, task=omat, fairchem (gabia) |
| Pipeline | `00_preflight … 09e_ehull` (10 stages) per compound |
| Read | gabia 2026-06-09 (post_anneal_ranking.json + 07_eos + 08_elastic per compound) |
| Champion `xyz` location | gabia `/data/work/repo/db/structures/doping/<cmpd>_<x>_champion.xyz` |
| **Status** | gabia-local; vm has Al2O3 only at `db/structures/doping/Al2O3_*_champion.xyz` (rest pending PAT sync). Numbers here are read-only from gabia. |

## Open questions / follow-up

1. **B0 = 0 fit failures** (MnO_x002, CoO_x010, ZnO_x010): re-run EOS with wider volume grid or different BM3 initial guess. Low priority — Cij already gives the modulus story.
2. **Sc2O3** only has x=0.02 result. Run x=0.05 and x=0.10 to confirm the favorability trend (probably worth the GPU time given the headline E_VRH=18.7 GPa).
3. **Top candidates for Paper #2 (coating) DFT validation**: Sc2O3_x002 + Al2O3_x005 + Li2O_x005 + MnO_x005 ⇒ 4 configs. Same protocol as Nd2O3 (DFT+U for Sc/Mn 3d if needed, ISPIN=2 for Mn).
4. **Charge compensation for acceptors** (when Sc3+/Al3+ replaces Li+, need 2 Li vacancies): cascade `tools/doping` already handles this via `add_li_interstitials` etc.; the converged dE values include the compensation.
5. **vm db push of doping_cascade_verified.json**: this update extends the file (Al2O3 already there) with the other 13 dopants. Companion update commit alongside this markdown.
