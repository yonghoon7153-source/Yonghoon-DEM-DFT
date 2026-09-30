# Mixer high-Bo round 10 independent evidence

Review: `review.md` (Korean). Scope: submitted v2.6 Q1–Q4.
Repository source pin: `8e8474a68fa71216f3d4890b46a6cddb6380db66`.
Upstream LIGGGHTS source pin: `3d5c00f20519e6bb6eb6756f51f1ad36564e649d`.
Input archive SHA256: `397ea3a16ab56e1947707502e99a8253bc5ad6e9e240ac81d92c32cdd3ad00aa`.

## Reproduction

Use Python with NumPy and SciPy. This review used numpy 2.3.5 and scipy 1.16.3.

```bash
python audit_round10.py --selftests --lf-selftests
```

No DEM simulation, MPI or scheduler job is invoked. Synthetic fixtures are temporary directories under `evidence/`. Tests may invoke local text-only shell gate fixtures. On Windows, `selftest_lf.py` additionally emulates Linux text-file LF output for the tests; it does not edit submitted source or change assertions. POSIX 0600 file-permission tests are not certified on Windows.

## Evidence meaning

- `submitted/`: original extracted input, including preregistration, 14 decks and patch. No edits.
- `source/`: exact pinned source files needed for scoped analysis. `SOURCE_PINS.json` records Git blob identities. The original mixed/newline bytes of Back.stl are preserved.
- `audit_round10.py`: independent E*/CED/F0 arithmetic from deck commands, source/blob hashes, deck readback, MPI distribution algebra, normalization and contract counterexamples.
- `evidence/audit_results.json`: calculated results. The NaN / missing-report-values cases intentionally assert that the submitted implementation accepts these boundary cases; a corrected implementation should make those reproduction assertions fail until the audit is adapted to test closure.
- `evidence/*selftest*.log`: original selftest outputs; failures are retained, not discarded.
- `review_status.json`: scope and status summary, not a production approval record.

The producer/consumer gate counterexample stubs contact acquisition and S_R² acquisition while executing the real `e0_diag` and `verify_e0_record`. The separate finite-cloud example executes `cell_stats`. It does NOT claim that the small synthetic cloud passes the actual 100000-particle DEM contact contract. The soft-range counterexample calls the actual contact-status function.

Reported DEV7 maxima and counts are not independently measured here: actual dumps/logs/blind vault JSON are absent from the input archive. Forecast numbers are conditional calculations from reported input values.

No production code, ledger, Git state, remote jobs or simulation outputs were changed. This is not a full repository mirror and not a full `check_all` or launcher certification. Model choice, shell timing and test counts are not scientific evidence.
