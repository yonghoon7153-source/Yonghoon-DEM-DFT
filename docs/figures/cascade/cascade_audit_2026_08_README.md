# Cascade Codex audit artifacts — pinned 9abe5105

These files support the audit-only Cascade figures and the axis-specific gate-presence table.

## Provenance

- Frozen source commit: `9abe5105cacafa22ab3e185f09e2a4c37118b9a9`
- Generator: `tools/figures/plot_cascade_audit_2026_08.py`
- Intended use: audit/status display only; never a current leaderboard, Pareto set, transport ranking, or pair prediction.

## Included

- `cascade_audit_gate_completeness.csv`
- Five audit figures and their five companion CSVs:
  campaign status, G3 phase-set sensitivity, historical G4 deconstruction,
  post-hoc interface axes, and ML validation.
- The pinned, fail-closed figure generator.

## Merge cautions

1. Do **not** merge the local Codex manifest wholesale into the newer `922332c0` manifest.
   The newer Na2S regeneration changed `cascade_v23_ranked_v2.csv`, so its hash differs.
2. The G3 phase-set labels in the companion CSV identify the analytical included/excluded
   sensitivity cases. They are not original row-level provenance: the recovered GP rows did
   not record `phase_set_id`, MP entry IDs, or an MP snapshot hash.
3. `cascade_audit_gate_completeness.csv` distinguishes record presence from approved
   comparability. In particular, G3 has 90 onset records but zero method-complete comparisons.
4. Missing values remain missing; they must never be converted to gate failures.

