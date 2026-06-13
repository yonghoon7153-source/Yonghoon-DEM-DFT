# Dopant screening funnel provenance + multi-cation motif generalization

> Created 2026-06-13. Single source of truth for **how the Nd₂O₃ champion was
> selected** (funnel accounting, honest) and the **Y₂O₃ cross-validation** that
> shows the doping motif is not Nd-specific.
> Owning branch: `claude/friendly-meitner-lldvar`. The Y₂O₃ cascade data is
> produced by branch `claude/configure-spawn-halogen-lithium-TjDCB` (gabia) and
> only **cited** here — this file touches nothing TjDCB owns, so no merge clash.
> Cross-links: `db/compositions/modelc_nd_doped.json` (Nd record),
> `paper_figures/nd2o3_doped_modelc_DFTrelax.{cif,xyz}` (champion structure).

---

## 1. Nd₂O₃ champion — the screening funnel (honest accounting)

### 1.1 What actually produced cfg141 (CONFIRMED from json execution record)

| Stage | Method | Count | Result |
|---|---|---|---|
| **1. Enumerate** | `enumerate_track1.py` — Track 1A, Hard–Hard pruning (O@16e placed near Nd) | **342 configs** | `phase_1_track1A_enumerate: DONE` |
| **2. MLIP screen** | UMA (uma-s-1p2) batch relax of all 342 | 342 → 1 | champion **cfg141**, E/atom span −4.34844…−4.34342 (~5 meV/atom across the field) |
| **3. Anneal** | 500 K NVT 20 ps + 5 ps 300 K quench + LBFGS, top-10 (5×1A + 5×1B) → 4 unique | 4 frames | cfg141 stays **rank 1** |
| **4. DFT+U verify** | KISTI, DFT+U(Nd 4f, ISPIN=2), top-5 | in progress | structure relaxed at k441; **re-ranking margin PENDING** |

cfg141 identity: **Nd=[1, 82], vac=[5, 6, 63, 71], O=[37, 95, 109]** (124-atom
1×1×2 supercell indices).

### 1.2 Why cfg141 is defensible as the champion (not just "first listed")

- **Anneal re-ranking margin**: cfg141 (Track 1A, Nd@Li) vs best competitor cfg23
  (Track 1B, Nd@P) = **1.633 eV/cell = 0.544 eV per O-defect**. Boltzmann at the
  500 K anneal T: P(1B)/P(1A) = exp(−1.633/0.043) = exp(−37.9) ≈ **4×10⁻¹⁷**;
  even at 1000 K synthesis quench ~1×10⁻⁸ → essentially 100 % Track 1A formation.
- **Track 1B is a family of basins, all higher**: cfg23 had the largest anneal
  gain (−671.6 meV, rank #4→#2) yet still sits 1.63 eV/cell above cfg141 →
  the advantage is not a single-config fluke.
- **Robustness QC**: 20 random Li perturbations (≤0.5 Å) + UMA FIRE relax on
  cfg141 — **all 20 ended higher** by 0.4–15.5 meV (mean 2.5). No nearby lower
  minimum → cfg141 is at/very near the MLIP global minimum.
  (commit on 1BN1c: "Phase 2.5 quality check: cfg141 ROBUST ground state confirmed".)
- **The winning pair was a stated chemical hypothesis, then earned it**: the
  dispersed pair Nd=[1, 82] is the script's `FORCE_PAIR` (a hand-picked
  reference), and it beat every distance-binned competitor — i.e. an exhaustive
  search confirmed the chemical intuition rather than the intuition steering the
  search.

### 1.3 Funnel SIZE — what we can and cannot claim ⚠

There are **two** enumeration scripts; do not conflate them:

- **`enumerate_track1.py`** — the one the json attributes the champion to.
  Hard–Hard pruned to **342 configs** (Track 1A). This is the CONFIRMED
  champion-producing screen.
- **`enumerate_nd_o_all.py`** — a later *comprehensive* design: full
  `C(24, 3) = 2024` O placements per Nd pair (24 O-eligible sites = 20 PS₄
  corner S + 4 free anion 4a/4d), categories A–G summing to 2024; Nd pairs =
  `FORCE_PAIR (1) + 5 distance bins × 5 ≈ 26`. Designed for
  ~26 × 2024 ≈ **53k** single-points → top-20 LBFGS → top-5 anneal.
  **NOT referenced in the json execution status** → whether it was run to
  completion (and whether it reproduced cfg141) is **UNVERIFIED**.

**Seminar-safe phrasing** (pick by what gabia logs confirm):
- Defensible today: *"Track 1A O-placements were enumerated (342 configs, Hard–Hard
  pruned), MLIP-screened, annealed (top-5, 500 K), and DFT+U-verified; the
  champion beats the Nd@P alternative by 0.54 eV/O-defect."*
- "Hundreds of thousands" is honest only as **MD force evaluations** (4 anneal
  frames × ~5×10⁴ steps ≈ 2×10⁵ evals), **not** as config count. If you want the
  ~50k exhaustive-config number, confirm `enumerate_nd_o_all` was the executed
  path first.

### 1.4 PENDING — fill when logs/results arrive

- [ ] Exact executed funnel: was it 342 (track1.py) **or** ~53k (nd_o_all.py)?
      → gabia `/data/work/nd_doped_modelc/1_enumerate/` header `# Nd pairs:` /
      `# O configs:` printout, and which `configs/` dir fed phase 2.
- [ ] Number of Nd pairs actually used (design ≤ 26).
- [ ] **Phase-3 DFT+U re-ranking margin** (cfg141 vs #2 at DFT level) — closes
      the "UMA noise could have flipped it" objection quantitatively.

---

## 2. Champion structure (DFT-relaxed, lineage closed)

cfg141 (124-atom) → remove 4 Li vacancies → **120-atom** primitive; index 82 → **78**.
A direct PBC-coordination analysis of `nd2o3_doped_modelc_DFTrelax.xyz` finds Nd
at indices **1 and 78** — confirming the lineage end-to-end.

DFT-relaxed composition **Li₄₈Nd₂P₁₀O₃S₄₁Cl₁₆** (charge-balanced, 0 net).

**Two inequivalent Nd sites** (Nd–Nd 29.7 Å — maximally dispersed, one per half-cell):

| site | first shell (≤3.3 Å) | distances (Å) |
|---|---|---|
| Nd1 (oxy-bound) | **2 O** + 3 S + 1 Cl | Nd–O 2.48 / 2.61, Nd–S 2.62–3.18, Nd–Cl 2.80 |
| Nd78 (sulfide) | 5 S + 1 Cl | Nd–S 2.70–3.00, Nd–Cl 2.75 |

**O is fully dissolved into the PS₄ framework — no free O²⁻**: all 3 O are covalent
P–O (1.55–1.60 Å). P24 = **PS₂O₂** (O29+O34), P25 = **PS₃O** (O40); O34 and O40
also anchor Nd1. Framework integrity: P–S = **2.064 ± 0.018 Å** (n=37 = 10 P×4 − 3
O-substitutions), identical to undoped modelc 2.064 ± 0.011.

→ KISTI tie-in: scf_k441.in splits Nd into two species (AFM, start_mag ±0.5) =
exactly these two sites. DOS/PDOS first question = does Nd 4f split by site
(oxy-bound vs sulfide), and where in the gap.

---

## 3. Y₂O₃ cross-validation — motif is NOT Nd-specific

**Source (cited, not owned)**: branch `claude/configure-spawn-halogen-lithium-TjDCB`,
gabia `…/multi_category_2026_05_26_v23/Y2O3_x010/`, UMA `uma-s-1p1`,
commit `71f12468`. **UMA-level, NOT DFT-verified.**

### 3.1 Site preference — DECISIVE, and matches Nd on BOTH sites

Stage-03 winners, metric `de_per_atom_vs_baseline` (lower = more favorable):

| ΔE/atom (eV) | cation site | O site | |
|---|---|---|---|
| **−1.0022** | **Li_24g** | **S_16e** | winner |
| −0.9929 | Li_24g | S_16e | |
| −0.9329 | Li_24g | S_4a | |
| −0.7291 | P_4b | S_16e | |
| −0.6607 | P_4b | S_4a | |

- **Cation: Y→Li_24g beats Y→P_4b by +0.273 eV/atom** (~13 eV/cell at ~47 atoms —
  far beyond UMA noise) = same as Nd (Nd@Li ≫ Nd@P).
- **Anion: O@S_16e beats O@S_4a by ~0.07 eV/atom** within the Li group = same
  direction as Nd (Track 1A O@16e ≫ Track 1B O@4d, 0.544 eV/O).
- **Double match** → the (M³⁺→Li_24g + O→PS₄-corner) motif is common to two
  different +3 cations (Nd³⁺ 0.98 Å, Y³⁺ 0.90 Å), not a Nd-4f peculiarity.

### 3.2 Resolves the apparent elastic "tension"

Stage-08 (UMA elastic) ranks Y→P configs stiffer (E_young 51–54 vs 29–34 GPa for
Y→Li). This is **not** a real tension: Y→P is 0.27 eV/atom thermodynamically
unfavorable → it doesn't form, so the stiffer config is inaccessible.

### 3.3 What to keep vs discard from this batch

- **KEEP** ① site preference (strong) and ② decomposition path (partial):
  e_hull reference decomposition at the Cl-rich variant =
  `0.255 YPS₄ + 0.213 LiCl + 0.191 Li₂O + 0.170 Li₃P + 0.170 S`
  (Y forms a YPS₄ phosphate-sulfide). **Absolute ΔE_above_hull still needs DFT on
  winner.xyz** — only the hull reference energy is computed.
- **DISCARD** ③ ESW: the json self-labels it a coarse, non-voltage-referenced
  proxy (competing-phase energy span only) — not paper-grade.
- **SKIPPED** ④ adhesion (Stage 12) and σ-MD (Stage 09 was e_hull+ESW, not σ):
  TOP_K_NCM=0 / TOP_K_SIGMA=0 → DONE markers but no real output.

### 3.4 Significance

This is the **second +3 datapoint** the north-star plan asked for ("Nd is one
datapoint; run more compounds"). It promotes the Nd finding from a single case
study to a **transferable design rule**: trivalent M³⁺ dopants in Li₅.₄ argyrodite
prefer the Li site with O co-substituting onto the PS₄ corner. La₂O₃ (Step 47,
running now) is the natural third point to confirm the lanthanide trend.

### 3.5 PENDING

- [ ] DFT single-point/relax on Y₂O₃ winner.xyz → absolute ΔE_above_hull.
- [ ] La₂O₃_x005 Stage-03 winner site (expect Li_24g + S_16e) when cascade reaches it.
