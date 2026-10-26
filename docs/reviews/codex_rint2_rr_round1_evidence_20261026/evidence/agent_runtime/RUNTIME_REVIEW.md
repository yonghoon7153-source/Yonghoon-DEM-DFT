# Runtime and certificate review, 2026-10-26

Review pin: 9bec6b7646374daed0d3edbb9647f9f46d302750. Comparison baseline: 0b3012460fb8e8b7d53484b0efe399e2dc506aec. Source snapshot verified by the parent review against the pinned Git blobs. No production-source or Git changes.

## Recommendation

- **RCA2-08: CLOSED against its stated minimum fix.** Both final energy sums, and the ledger tolerance overflow that could disable comparison, now fail closed. The original reproducer and separate U-only/W-only overflow cases return structured failure.
- **SELF-132: CLOSED for the identified Python 3.8 compatibility defects.** Dictionary assembly preserves contents/order, the nextafter fallback gives the same relevant binary64 values, and the child-interpreter shim preserves the venv interpreter path.
- **SELF-133: CLOSED for the R solver's real float64 inputs.** The fallback implements the modern CG iteration and stopping rule. This is not a claim that it reproduces every public SciPy API behavior.
- **C5: ACCEPT the Python 3.8 compatibility gate.** 3.8.20 versus kgy's 3.8.10 is not a defect under the accepted Python minor-version contract. It is compatibility evidence, not proof of host-wide bit identity or a substitute for the recorded production environment. Do not require an exact Python patch merely to close these two fixes.
- No finding here blocks S0 stage 1 or small numerical probes. Production permission remains governed by the separate B/C and final-pin requirements.

## What was run independently

All fresh runs used Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3 on Windows, with OPENBLAS/OMP/MKL threads set to 1. This review did **not** freshly rerun CPython 3.8 or 3.11. The submitted 3.8.20 / NumPy 1.24.4 / SciPy 1.10.1 eleven-suite gate log and 3.11.17 environment file were inspected as supplied evidence.

| Check | Result |
|---|---|
| Forced 3.8 nextafter branch, native math.nextafter reference | 200,169 boundary/random pairs; 0 mismatches, signed zero checked; NaNs compared as NaNs |
| Directed division, exact Fraction oracle | 4,950 finite positive input pairs; 0 violations of lower/upper enclosure |
| Fallback CG versus installed modern SciPy, real float64 SPD | 144 cases; solution bytes, info and callback count identical |
| Full resident test_step3_conv_cert | 30/30 PASS |
| Resident T24 | 8/8 PASS, including 20 complete ordinary certificate dictionaries identical to historical 49a1af626 |
| Extra diagnostic overflow stress | Nonblocking residual warning described below |

For resident tests, only historical-source loading in the test harness was redirected to fetched files because this snapshot has no Git history. Pinned production modules were imported unmodified. The full convergence suite includes K1, K4, K4b-K4d and seal checks.

Reproduce from this directory with the bundled Python executable, flags -X utf8 -B, and these scripts:

- probe_runtime.py -> probe_runtime.json / probe_runtime.log
- run_targeted_tests.py -> targeted_tests.log
- probe_diagnostic_overflow.py -> diagnostic_overflow.json / diagnostic_overflow.log

The bootstrap only supplies local dependency paths and review scratch paths.

## Source reasoning

### Overflow closure

scripts/step3_conv_cert.py:491 now uses _fsum_bound for final U; :568 does the same for W. The helper at :240-253 catches OverflowError/ValueError. Nonfinite totals are rejected at :493-495 and :570-572. The ledger intermediate checks at :343-357 reject nonfinite row/plate/tolerance values, so an infinite tolerance cannot silently accept a hidden ground term. plate_currents at :119-123 suppresses overflow warnings while its nonfinite result still fails the certificate checks.

Observed results:

| Fixture | Result |
|---|---|
| 5 independent nodes, gb=gt=8e307, phi=.5 | ledger overflow; NOT_CERTIFIABLE, ok=False, bounds absent, 0 warnings |
| 10 nodes, gb=gt=4e307, phi=.5 | final U overflow; same structured failure |
| 5 nodes, gb=gt=3e307, phi=1 | final W overflow; same structured failure |
| 1 node, L=1.6e308, gb=gt=4e307, phi=.25 | hidden-ground ledger comparison overflow rejected |

These directly satisfy findings.json:12809-12812, whose minimum requested protection is final U/W summation plus the permanent 5-node regression.

### Compatibility and semantics

- scripts/ptfe_face_alpha.py:240-244 replaces dict union with unpacking. Its original scalar-key insertion order and separate copied dia_classes dictionary are preserved.
- scripts/ca_ext_svcf.py:751-766 calls the identical math.nextafter function when available; otherwise explicit binary64 stepping handles positive/negative normals, subnormals, signed zero and infinities. The fallback's NaN arithmetic is irrelevant to _div_dir's finite-positive domain.
- scripts/ca_ext_svcf.py:769-786 uses exact Fraction comparison before stepping. An overflowing upper bound represented by None and lower bound saturated at maximum finite float remain conservative bounds; C6's representation choice is not a defect.
- scripts/test_ca_ext_runner.py:689 and test_rint_r_chain_e2e.py:462 use abspath(sys.executable), preserving the selected venv path instead of resolving its symlink to the base interpreter.
- scripts/step3_sigma.py:117 selects the native function by the rtol parameter; :602 calls that one symbol. A modern environment therefore retains the original SciPy implementation.
- _cg_v112 at :73-112 matches the iteration, initial residual, relative/absolute tolerance normalization, callback placement and iteration-exhaustion semantics in official SciPy v1.12.0 and v1.17.1 for the supplied real float64 data and explicit preconditioner. Production vectors/matrices are assembled as float64, e.g. :2183 onward, and x0 is normalized at :551.

Official comparison sources:
[1.12.0 implementation](https://github.com/scipy/scipy/blob/v1.12.0/scipy/sparse/linalg/_isolve/iterative.py#L355-L400) and [1.17.1 implementation](https://github.com/scipy/scipy/blob/v1.17.1/scipy/sparse/linalg/_isolve/iterative.py#L356-L400).

The fallback is narrower than the public SciPy interface: it forces float64, does not implement complex dot products or full make_system validation, and does not separately reject negative atol. Those are outside the R calls reviewed here; calling it universally API-equivalent would be too broad. It does not promise cross-version or cross-BLAS bit equality.

### Environment gate

scripts/check_kgy_py38.sh:15-25 compares Python (major, minor), and exact NumPy/SciPy versions; :26 records the full Python version. setup_kgy_py38.sh:6-9 obtains a 3.8 interpreter and pins the numerical packages. check_all.sh:277 includes the gate. This matches Q9 revision 4 at q9_predict_units_design.md:204-205 and the pre-solve contract at :66.

The supplied kgy_py38.log records all 11 suites passed with Python 3.8.20 / NumPy 1.24.4 / SciPy 1.10.1. The request expressly records the actual kgy 3.8.10 difference and pending remaining package inventory. Full host identity, GPU behavior, raster fingerprints across machines, and final-pin S0 are separate obligations; none is proven by this gate, and none requires pretending that 3.8.20 is 3.8.10.

## Nonblocking residual robustness observation

scripts/step3_conv_cert.py:509 still computes the diagnostic raw KCL norm with an unguarded NumPy sum. This line is unchanged from baseline :494. Three independent nodes with gb=8e307, gt=1 and phi=.2 have finite inputs and finite U=1.5360000000000001e308, yet sum(abs(d)) overflows:

- target_kcl_raw=inf, warning “overflow encountered in reduce”;
- target_lo=0, target_hi=1.5360000000000033e308;
- certify returns status=POSITIVE_SOLVED but ok=False, pass_b=False, pass_c=False, pass_d=False;
- promoting warnings to errors raises RuntimeWarning at :509.

This does not produce a certified wrong value, is outside registered physical magnitudes, and does not reopen the specific final-U/W defect. It prevents a universal claim that every finite-input intermediate overflow is warning-free or always returns NOT_CERTIFIABLE. If tracked, this merits a nonblocking P3 diagnostic-robustness item: guard/suppress this diagnostic sum or narrow that universal wording. Evidence is diagnostic_overflow.json.

