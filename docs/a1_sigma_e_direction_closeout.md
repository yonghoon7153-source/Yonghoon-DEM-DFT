# A1 — σ_e composition-direction (σ_S/σ_P endpoints): CLOSE-OUT (2026-06-30)

Resolves audit ⚠#11 (`docs/stage2_model_audit_vs_literature.md`): the σ_e form's
single-vs-poly endpoint conductivities σ_S / σ_P were **mis-attributed** and
carried a possibly material-specific **sign assumption**. A1 is now closed.

## What was wrong
- The values **σ_S = 10, σ_P = 5 mS/cm** were cited as "**Trevisanello 2021**".
  Trevisanello 2021 measured Li⁺ chemical diffusion / BET surface area / R_ct —
  **NOT electronic σ_e**. So the *source* was wrong.
- The code comments also **swapped the poly/single labels** (σ_S called
  "polycrystalline", σ_P "single-crystal"). By the form's own convention σ_S is the
  AM_S endpoint (p=0, small **single**-crystal) and σ_P the AM_P endpoint (p=1, large
  **poly**crystalline).
- The single>poly *direction* is **material-specific** (undoped NCM811 vs W-doped
  NCWA), which was not stated.

## What is right (the fix — comment/label only, ZERO numerical change)
- **σ_S / σ_P are CORPUS-FIT endpoints, not a Trevisanello measurement.** The live
  fit gives σ_S ≈ 9.13 / σ_P ≈ 4.14 (ratio 2.21); we round to **10 / 5 (ratio 2.00)**
  — ΔLOOCV = −0.0004 vs live (essentially identical) with 2 fewer DOF. The 2× ratio
  is **data-validated**: locking ratio = 1 costs LOOCV **−0.10**. So the values are
  empirically correct for our material and need no change.
- **Direction is GB physics for undoped NCM811**: AM_S (single-crystal) has no
  internal grain boundaries → higher intrinsic σ_e than large polycrystalline AM_P.
  So σ_S > σ_P is correct *for NCM811* (our material). The NCM(r) factor
  `1/(1+(r/2)^1.5)` is the same GB direction (Trevisanello-*spirit*), with β/r0
  **corpus-fit** — not a Trevisanello σ_e formula.
- **σ_S / σ_P are exposed as MATERIAL INPUTS** (`--sigma-S` / `--sigma-P`,
  generate_comparison_plots.py). The locked defaults (10/5) are the validated NCM811
  values; for a different CAM the user overrides them. E.g. **W-doped NCWA
  (#266 Oh 2026) shows poly 13.7 ≫ single 2.45** → for that material set
  `--sigma-S < --sigma-P` (poly>single). The form is material-agnostic; only the
  default is NCM811-specific.

## Proof the fit is unchanged
The A1 commit (`29375b2`) touched **only** comments, docstrings, plot titles/labels,
CLI help, and the PLOT_REGISTRY text. Filtered diff of executable lines = **empty**;
`_SIGMA_S_LOCKED=10.0`, `_SIGMA_P_LOCKED=5.0`, `NCM_AM_REF_R=2.0`,
`NCM_AM_GB_EXPONENT=1.5` are **byte-identical**. ⇒ the σ_e form is numerically
identical → **LOOCV unchanged (0.9531, Stage 22.5)**. No re-fit needed.

Optional sanity check on a machine with the corpus + sklearn (confirms 0.9531):
```bash
python3 scripts/electronic_ablation_full.py     # prints the Stage 22.5 LOOCV
# or the dashboard global-fit summary in generate_comparison_plots.py
```

## Phase-3 readiness
A1 was the "Phase-3 prerequisite". It is satisfied: the σ_e form is sound, its
endpoint assumption (σ_S>σ_P for NCM811) is now **explicit, data-validated, and
material-overridable** — not a hidden mis-attributed lock. Phase-3 predictor can
consume the σ_e form as-is.

## ✅ A1 CLOSED
- Attribution fixed (corpus-fit, not Trevisanello) ✓
- poly/single label swap fixed ✓
- values data-validated (ratio 2.0; live≈locked) ✓
- exposed as material INPUT (NCM811 default; override for NCWA/NCA) ✓
- LOOCV provably unchanged (comment-only edits) ✓
No numerical change was warranted; the only error was the citation/label, now
corrected. The deeper "move NCM(r) to the diffusion/dead-AM channel" idea (audit
recommendation 3) is an optional future refactor, NOT required for A1 closure.
