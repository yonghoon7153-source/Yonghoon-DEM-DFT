# R4 gamma/shape independent subreview

Target `39a5fe06215710b16e9b42bf3dc3c04c63cb8663`, `bms-balancing/`. Read `reviews/R4_REQUEST.md` fully. No target edits or private data access.

**One reproducible P1 remains.** The new `gamma_headroom` calculation passes the finite-grid tests below, and R3's low-ratio and illegal-excursion examples now behave correctly. However a separate `(c)` branch still makes the same universal model-rejection and LAM-leakage claims. This prevents accepting the assertion that the script now reports only descriptive magnitudes on all paths.

Run from the review workspace, with target dependencies installed:

```bash
python outputs/harness_r4_shape_repros.py --target /absolute/path/to/bms-balancing
```

Executed on the target with Python 3.12.3: **rc 0**. The script's assertions require both corrected controls and the remaining counterexample to behave as reported. It uses the actual `Blend` and `ne_shape.main()` with synthetic measurement and fitted-pair inputs, not a new optimizer result.

## S1 [P1] The separate broad-residual branch still rejects every gamma although the same run exhibits an exact valid gamma

Locations: `scripts/ne_shape.py:319-322`; the claim that all diagnostic paths are descriptive is `FINDINGS.md:1308-1309`. Existing regression coverage: `tests/test_review_findings.py:1934-1950`.

Construct measured pristine and aged NE curves with the unmodified target Blend at gamma 0.15 and 0.5. Supply full-cell fitted target gamma 0.0. PE and capacities are equal. The fitted pair is input to the diagnostic; the counterexample does not claim that an optimizer chose it during this test.

Actual output and independently recomputed values:

```text
measured pristine gamma                 0.15
true measured target gamma              0.5
supplied selected target gamma          0.0
error at the legal true gamma 0.5        0.0 V
measured change                         62.44361590442882 mV
selected-pair change                    26.24999362069963 mV
(b)/(a)                                 0.4203791410938752
selected-fit residual >50mV             68.0% of the 400-point x grid
new headroom witness                    gamma=0.5, delta=+0.35
new witness amplitude                   62.44361590442882 mV
```

The repaired ratio logic takes its middle branch and prints only a descriptive comparison. The new `(d)` logic actually provides the legal witness. Then the separate `(c)` branch prints:

```text
모양이 아니다.** γ 를 어떻게 고르든 남고, a_NE·b_NE 가
흡수한다 = LAM_NE·LLI 에 계통 편향.
```

Thus this is not the already-fixed R3 low-ratio path, a failed fixture, or a missed global optimization. The same run presents gamma 0.5, and direct evaluation at that gamma gives **exactly zero shape error**. The universal claim is false on that input. In addition, a residual at the selected gamma cannot establish which parameters would absorb it.

Why the current test stays green: its old selected pair 0.15→0.16 with truth 0.45 yields only **18%** of x points over 50mV, so `(c)`'s `>30%` branch does not execute. Its source checks search only for `모델 부적합` and `상자 안`; the retained wording contains neither string. This is another branch, not a change in threshold needed to resurrect the old one.

Minimum closure: remove the universal gamma rejection and parameter-causation statements from `(c)` as well. It may report the fraction/max/RMS residual **at the selected gamma**. Add the exact-family broad-residual case so the test covers `(c)` above and below 30%, and require semantic consistency with an exhibited exact fit rather than a blacklist of two phrases.

## Corrected paths that survived reproduction

- R3's exact-family low-ratio case (reference 0.15, selected 0.16, true 0.45): ratio `0.03295993760467304`, no universal rejection, valid witness gamma 0.45. R3's original path is closed.
- R3's 100mV-offset amplitude example (reference 0.25, selected 0.26): finite-grid maximum `45.20971840251814mV`, witness `None`, legal headroom `[-0.25,+0.25]`. The old unconditional “inside the box” assertion is gone. `(c)` still runs in this example, but S1 uses an exact-family counterexample where its conclusion is definitely wrong.
- `gamma_headroom` agrees with an independently computed reduction over the same 501 gamma values and 400 x coordinates. For a known legal continuous witness gamma 0.45025, it returns 0.451 as the nearest **sampled** witness, as its docstring promises.
- The committed three rows' legal deltas agree with saved reference gamma, witnesses lie inside `[0,0.5]`, and saved witness deltas agree at CSV precision. The published 86.006744mV and private-data witness amplitudes were not recomputed from unavailable literature curves; this is a stated verification boundary, not a new finding.

## Finite-grid scope and the new `(d)` interpretation

Positive and negative statements have different strengths. A sampled legal gamma can witness an amplitude on the stated x grid. `witness=None` establishes only that no sampled gamma passed the criterion. Neither the nearest sampled witness nor a sampled maximum is automatically the nearest continuous witness or a global continuous-family bound.

The code docstring, CSV sidecar, and table say **grid-based**; these are appropriate. The main paragraph also says “이 격자에서는” before describing 300_0009. I do **not** count the finite scan itself as a newly demonstrated target defect. A smooth toy function, explicitly not actual `Blend`, is included only to illustrate scope: a 100mV bump centered at gamma 0.2505 can be missed by a 0.001-spaced scan. It is not evidence that the private-data 86.01mV result reverses.

For unambiguous design handoff, preserve the full wording even in summaries: **“with the selected reference gamma fixed, no gamma on the 501-point grid reaches the measured normalized amplitude on the 400-point x grid.”** `FINDINGS.md:1297-1298` and `WORKING_STATE.md:33-34` shorten this to “gamma alone cannot reach it/no witness”; adding the grid scope there prevents a future reader from treating a finite scan as a family exclusion proof.

To make a continuous exclusion claim later, validate the relevant monotonicity/envelope properties of the actual component curves or compute a certified upper bound. The fact that the largest sampled value occurs at an endpoint is not, by itself, that certificate. Shape agreement still needs an alignment and residual criterion; the current amplitude witnesses should not be relabeled shape fits.

The recorded nearest witnesses are negative deltas for 100 and 200. That shows the direction of the **chosen nearest grid witness**, not that all possible witnesses must be negative. Also `FINDINGS.md:1293` says the selected changes differ in both magnitude and direction; state 100's selected delta is also negative (`-0.001759`), so only state 200 reverses direction. This is a small wording correction, not an additional P1.

## Answer relevant to the revised GO objective

The corrected amplitude ratio, fixed-reference grid results, and conditional 97-row arithmetic can populate an **observations** column, with their qualifications. They do not establish which new electrode family should be selected. S1 must be corrected before accepting the claim that all program outputs have been reduced to observations. After that, no additional private-data measurement is required merely to draft a requirements document that separates observations, competing hypotheses, discrimination tests, and adoption criteria.
