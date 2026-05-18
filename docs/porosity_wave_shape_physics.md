# Porosity Wave-Shape Physics Decomposition

**Generated:** 2026-05-13
**Source:** `predict_porosity_strict_physics.py` model with 1 experimental anchor
(ε_pure_SE = 10% at 300 MPa, user's lab measurement)
**Validated against:** 82 DEM cases (4 campaigns), see `all_dem_porosity.csv`

## Wave-shape origin — two competing densification mechanisms

The non-monotonic porosity curve ε(AM wt%) is the superposition of two
published physics that dominate at opposite ends of the composition axis:

```
ε(AM_wt) =  ε_RCP(f_se, λ)                          ← packing physics
          − Δ_plastic_max · f_se · p_se(f_se) / KC   ← plastic physics
```

The transition between the two is governed by stress-bearing
percolation `p_se = σ(8·(f_se − f_perc))` with `f_perc = 0.65`
(Storåkers 2000 / Bouvard 2000 / Jacobs 2009 / Henkes 2005 /
Liu & Yin 2025 consensus).

## Region-by-region decomposition

| AM wt% | Behavior          | Responsible physics                                    | Key reference |
|--------|-------------------|---------------------------------------------------------|---------------|
| 100→90 | 36% → 23% rapid drop | Bouvard binary packing: small particles begin Furnas-filling AM voids | Bouvard 2004 |
| 90→80  | Furnas valley ~17% | Bimodal/trimodal binary RCP minimum                    | McGeary 1961, Bouvard+McGeary curve |
| 80→60  | Flat / mild rise   | Packing past optimum + plastic still inactive (f_se < f_perc = 0.65) | Furnas-Westman 1930 + Liu&Yin 2025 |
| 60→30  | 17% → 13% gradual drop | Stress-bearing percolation activates → plastic begins | Storåkers-Fleck-McMeeking 2000, Jacobs 2009 |
| 30→0   | 13% → 10% gentle slope | Heckel plastic compaction (Tabor σ_y = H/3)         | Heckel 1961, Tabor 1948 |

## Why "wave" not "monotonic"

Two physics dominate at opposite ends:

- **Packing physics (Bouvard):** AM-rich side benefits most (Furnas valley)
- **Plastic physics (Heckel + stress percolation):** SE-rich side benefits
  most (soft phase compaction)

Since each is dominant in a different composition range, the model
naturally produces a non-monotonic curve with a *Furnas valley near
AM≈80 wt%* and a *plastic decline below AM≈30 wt%*.  The flat plateau
between (AM 30–80%) is where neither mechanism is fully active.

The sigmoidal transition arises from the percolation switch
`p_se(f_se)` turning on near f_se ≈ 0.55–0.65 (AM ≈ 30–40 wt%).

## Validation against 82 DEM cases (regime summary)

| Panel (in `porosity_4panel.png`) | N  | Regime                                  | Result |
|----------------------------------|----|------------------------------------------|--------|
| ① MAIN bulk thick-film          | 14 | bimodal AM, λ≥4, ε≥8                    | mean Δ = −2.27%, σ = 0.86%, RMSE = 2.42%, **\|Δ\|<5%: 100%** |
| ② thick-film out-of-regime       | 15 | mono-AM or λ<4                           | mean Δ = −7.23%, σ = 5.01% — Bouvard low-λ limit + mono-AM mismatch |
| ③ thin-film 1 mAh                | 33 | cell ≈ D_AM_P, wall confinement         | mean Δ = +0.20%, σ = 5.84% — *unbiased mean*, scatter is wall-effect |
| ④ particulate (mono-AM)          | 20 | monomodal AM by construction            | mean Δ = −8.53%, σ = 6.16% — includes DEM high-overlap artifacts |

## Deviation cause table — what each panel deviation means

| Panel | Cause              | Nature                                          | Fix (and overfit risk)                                  |
|-------|--------------------|-------------------------------------------------|---------------------------------------------------------|
| ①     | parameter conservativeness | small bias within published-value uncertainty | tuning α_KC or f_perc → **overfit risk** |
| ②     | Bouvard low-λ extrapolation + mono-AM | outside Bouvard 2004 calibration | Yu-Standish 1996 multimodal RCP → **principled extension** |
| ③     | wall confinement   | different physics (geometry, not bulk packing) | thin-film wall-effect term → **separate model** |
| ④     | low-λ + mono-AM + DEM artifact | partly outside model domain, partly non-physical | declare applicability domain; no fix for high-overlap artifacts |

**Conclusion:** trying to fix all four panels with a single model is
**overfitting** — each deviation has a distinct physical origin.  The
honest publication strategy is to (a) validate the model rigorously in
Panel ①, (b) explain Panels ②–④ deviations as out-of-regime by
documented physics, and (c) cite Yu-Standish 1996 multimodal RCP and
wall-effect models as principled future work.

## Code & data references

- Model:           `scripts/predict_porosity_strict_physics.py`
- Validation:      `scripts/validate_porosity_all_cases.py`
- Per-campaign:    `scripts/plot_porosity_per_campaign.py`
- 4-panel figure:  `scripts/plot_porosity_4panel.py`
- Main figure:     `scripts/plot_porosity_main_figure.py`
- 82-case CSV:     `all_dem_porosity.csv`
- Yu-Standish att.: `scripts/predict_porosity_yu_standish.py` (deferred future work)
