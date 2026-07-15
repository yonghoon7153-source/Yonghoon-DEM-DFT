# E_SE calibration — 2mAh_real_9 (실험 2mAh_9 대응)

**Question:** Which SE Young's modulus (E_SE) best represents cold-pressed
LPSCl (bulk 24 GPa) in the DEM compaction of cathode `input_2mAh_real_9`
(bimodal, AM:SE = 82:18, P:S = 7:3, 300 MPa target)?

Candidates compared: **E_SE = 1.35 / 1.5 / 2.0 GPa.**
Data: `docs/data/esse_calibration_2mAh_real_9.csv` (all values measured from
raw LIGGGHTS atom+contact dumps; transport cross-checked against webapp).

## Measured table

| E_SE | seed | ε_sphere | ε_union | overlap% | ⟨δ⟩µm | T µm | SE perc% | AM perc% / f_AM^cc | σ_ionic H/P | σ_e StageE | κ StageE |
|------|------|------|------|------|------|------|------|------|------|------|------|
| **1.35** | 78401 | 13.47 | 14.98 | 1.75 | 0.0739 | 33.98 | 99.3 | 69.6 / 71.3 ⚠ | 0.168/0.108 | 1.056 | 7.52 |
| 1.5 | S_a | 12.64 | 14.22 | 1.81 | 0.0757 | 33.60 | — | — | — | — | — |
| 1.5 | 58573 (S2) | 13.19 | 14.64 | 1.66 | 0.0723 | 33.85 | 99.2 | 79.0 / 82.1 | 0.180/0.114 | 1.087 | 7.71 |
| 1.5 | 58661 (S3) | 12.47 | 14.01 | 1.76 | 0.0748 | 33.58 | 99.4 | 75.0 / 77.5 ⚠ | 0.203/0.127 | 1.062 | 8.11 |
| **1.5** | **mean±std** | **12.77±0.31** | **14.29** | **1.74** | **0.0743** | 33.68 | 99.3 | 77.0 / 79.8 | 0.19/0.121 | 1.075 | 7.91 |
| 2.0 | d9c8cebf | 15.01 | 16.18 | 1.38 | 0.0660 | 34.60 | — | — | — | — | — |

ε_sphere-sum = webapp "Porosity" (production calibration metric); verified
to match exactly (1.35→13.47, S2→13.19, S3→12.47). ⚠ = AM electronic
network <80% (dead-AM warning).

## Findings

1. **Mechanics identical for 1.35 and 1.5.** overlap (1.75 vs 1.74 avg) and
   ⟨δ⟩ (0.0739 vs 0.0743 avg) are the same — 1.35's values land in the
   middle of the 1.5 three-seed band. Same plastic-deformation regime;
   changing E_SE 1.35↔1.5 does not change compaction mechanics.

2. **σ_ionic tracks porosity, not E.** Across seeds, lower porosity → higher
   σ_ionic monotonically (ε 13.47/13.19/12.47 → σ_ionic_P 0.108/0.114/0.127).
   The conductivity spread is density(seed)-driven, not E-driven.

3. **Porosity is non-monotonic in E:** 1.5 (12.77%) < 1.35 (13.47%) <
   2.0 (15.01%). The 1.35–1.5 gap (+0.70%p, ~2.3σ of the 1.5 seed std) is a
   packing offset (1.35 plate stopped 0.3µm higher), not an E effect —
   confirmed by identical overlap. 1.35 is a single seed (no replicate).

4. **Dead-AM warning is seed-borderline, not 1.35-specific.** f_AM^cc:
   1.35=71%, S3=77.5% (also <80% ⚠), S2=82%. The 82:18 / no-conductive-
   additive design sits on the 80% boundary regardless of E. StageE σ_e
   (1.056–1.087) and κ (7.5–8.1) are effectively constant — the AM-network
   spread washes out after Stage-E correction.

5. **Only 2.0 is a distinct regime:** overlap 1.38 (−21% vs 1.5), ⟨δ⟩ 0.066
   (−11%), ε +2.2%p. Stiffer SE deforms less → more porous.

## Decision

**Keep E_SE = 1.35 GPa.** It is physically identical to 1.5 (structure,
mechanics, transport all within seed noise), matches the experimental/production
porosity (~13.5%), and preserves production continuity. 1.5 is an equally
valid twin; 2.0 is rejected (too stiff). Both 1.35 and 1.5 lie within the
literature range for cold-pressed LPSCl effective modulus (~1–2 GPa, ~12–18×
softer than 24 GPa bulk via grain-boundary sliding + residual porosity).

## Cronau overlap gap — RESOLVED (SE-only validation, 2026-06-06)

The composite SE overlap (1.75%) looked far below the Cronau plastic floor
(5–10%).  Two **pure-SE** runs at the same E_SE = 1.35 GPa (SE bears the full
300 MPa load; the SE-SE lens volume is then EXACT, no AM approximation)
settle the question:

| SE-only case | N | T µm | ε_sphere | ε_union | overlap% | ⟨δ⟩ (% of d) |
|------|------|------|------|------|------|------|
| SE 20 vol% | 40,250 | 8.24 | −2.34 | 10.08 | **12.13** | 11.2 |
| SE 25 wt%  | 58,633 | 12.31 | +0.23 | 11.64 | **11.44** | 10.8 |

→ Pure SE at 1.35 GPa gives **11–12% overlap (⟨δ⟩ ≈ 11% of diameter)** —
at/above the Cronau 5–10% floor.  **The 1.35 GPa SE material model reproduces
the Cronau plastic floor.**  The composite's low 1.75% is therefore correct
**AM load-shielding** — the rigid 140 GPa AM skeleton carries the 300 MPa, so
the SE between AM grains is only lightly compressed.  The 1.75% ↔ 12% contrast
is a quantitative measure of that shielding, not a model defect.

Practical note: dense SE-only states give a **negative / near-zero
ε_sphere-sum** (V_sphere > V_box overlap artifact) — use ε_union for those.

_Saved 2026-06-06 (cloud session). Source raw dumps: upload 01f30198
(1.35 + 1.5 S2/S3), b8c56a96 (1.5 S_a), d9c8cebf (2.0)._
