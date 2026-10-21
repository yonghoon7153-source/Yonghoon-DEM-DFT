# planned edits after the pre-fix run (hardening round)

step3_conv_cert.py
1. _plate_input_problem: phi dtype kind 'f' (1-D) · plate g dtype kind in 'fiu' (bool/str/object refused)
2. _ledger: L dtype kind in 'fiu' · b dtype kind in 'fiu' · gb/gt dtype kind in 'fiu' (before astype)
   symmetry: relative _SYM_TOL = 1e-12 (duplicate-summation-order rounding k·u << 1e-12)
   row sums: tol_row = _LEDGER_TOL * (nnz_row + k_bot + k_top + 8) * (ar + pl)   (anchor "    if (np.abs(rs - pl) > " kept once)
   b: tol_b = _LEDGER_TOL * (k_bot + 8) * (|b| + bb)
3. target_bracket: np.errstate(over/invalid ignore) around flows/terms; flows non-finite -> problem (NOT_CERTIFIABLE);
   after the push: c/cb/ct/d2/a2 non-finite -> problem.  Anchors kept: "u1, e1 = _fsum_bound(c * dphi)",
   "    if _tree:\n        acc = d.copy()", "    if _defect_term:\n", "hi = (U + e1 + e2 + e3) * (1.0 + 8.0 * _UNIT)"
4. target_judge: exact Fraction comparison: tau = Fraction(repr(float(tol))) (1e-4 -> 1/10^4)
   fw = FH - FL ; fe = max(FH - FG, FG - FL) ; lim = tau * FG
   "    if fw > lim:" (width) · "elif fe > lim:" (error bound) · else pass.  float w, e kept for the record.

test_step3_target_cert.py
5. T18 baseline: run the same check functions unmutated first; a mutant is "detected" only if an expected check that
   passed in the baseline fails under the mutant.
6. docstring: T15-T18.
