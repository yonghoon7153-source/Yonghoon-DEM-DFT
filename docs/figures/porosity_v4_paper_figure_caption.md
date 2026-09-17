# Figure caption — porosity_v4_paper_figure.png

> ⛔⛔ **이 캡션의 케이스 수 `82` 는 틀렸다 — 실제 코퍼스는 `80` 이다** (2026-09-17, 원장
> `GAP3-FIG` 확장).  생성기 `plot_porosity_v4_journal.py` 가 그 수를 **리터럴로 적고**
> 있었다 (`:291` · `:502` · 이 캡션 템플릿 3곳).  실측: 자매 `plot_porosity_v4_paper.py`
> 와 로더가 **공백 말고는 동일**하고 거기서 `N_all=80 · N_trust=74` 가 나온다.
>
> ⚠ **소스는 고쳤지만 이 파일과 그림은 아직 재생성되지 않았다.**  생성기가 `sklearn` 을
> 요구하는데 클라우드 컨테이너에 없다 (CLAUDE.md).  ⇒ **WSL 에서 한 번 돌려야 한다**:
> `python3 scripts/plot_porosity_v4_journal.py`  (그림 `porosity_v4_paper_figure.png` +
> 이 캡션이 함께 갱신되고, 이 표지는 그때 지운다.)
>
> ⚠ 아래 본문의 **RMSE·R² 는 생성기가 계산한 값**이라 리터럴이 아니다 — 다만 그때의
> 코퍼스 값이므로 재생성 후 바뀔 수 있다.  `82` 만이 확정된 오류다.


**2D porosity surface ε(f_AM, λ_eff) for the 82-case DEM corpus, fitted with
the v4 physics model.**
(a) Predicted porosity surface as a function of AM weight fraction f_AM and
effective AM-to-SE size ratio λ_eff = r_AM,eff / r_SE.  Colour: model
prediction; markers: 82 DEM-measured porosities (same colour scale); white
dashed line: AM-percolation onset f_perc(λ) separating the matrix-dominant
regime (low λ, AM forms a load-bearing skeleton with SE bridging gaps) from
the Furnas regime (high λ, small SE particles fill voids between large AM
particles).  Six outlier groups (A1, A2, B, C, D, E) are circled in red — see
(f).  (b) Predicted vs measured porosity for all 82 cases with 95 % bootstrap
prediction bands (gray error bars).  Outliers are excluded from the trust
RMSE.  R² = 0.674, RMSE = 2.27 %p (trust = 1.70), and
5-fold cross-validated RMSE = 2.93 %p.  (c) Residual histogram of
the v4 physics model (blue) vs a Gradient Boosting Regressor evaluated by
5-fold cross-validation (red, RMSE = 1.84 %p on the trust set).
The two distributions overlap within the ±2 %p band, indicating that the
physics model has reached the data noise floor.  (d) 1D slices ε(f_AM) at
λ ∈ {2, 3, 5, 7, 10, 13} with bootstrap 95 % bands, illustrating how the
sin-wave shape of the paper §5 model emerges from the 2D surface: amplitude
and phase track λ continuously.  (e) Term decomposition of the prediction at
λ = 7, stacked from the RCP baseline ε_RCP = 36 % downward: blue =
Δε_Furnas (small SE filling AM voids), purple = Δε_Matrix (SE bridging an
AM-percolating skeleton), orange = Δε_plastic (Heckel plastic densification).
Inset: regime weights w_F(f_AM) and w_M(f_AM) — the sigmoid switch sets the
sin-wave envelope.  (f) Per-case residuals coloured by campaign; outlier
groups (A: single-layer AM_P with D_P/thickness > 0.5; B,E: trimodal deep
packing; C: AM_S-rich thick cell; D: half-stiffness particulate variant)
self-cluster outside the ±2 %p ML noise band, supporting the physical
interpretation that v4 fails only where its assumptions break.

v4 uses 6 physical-principle groups with 23 parameters total; bootstrap
parameter uncertainties are reported in Table S1.
