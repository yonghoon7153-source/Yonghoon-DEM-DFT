# Figure caption — porosity_v4_paper_figure.png

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
