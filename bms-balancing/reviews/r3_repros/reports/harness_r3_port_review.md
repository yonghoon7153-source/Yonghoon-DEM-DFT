# R3 — port comparison and profile validation subreview

Target: `a432d239c72c44a780be56679b8d9c1b9aaf3dc0` on
`claude/bms-alpha-beta-verify`; HEAD adds only the request above code/document
commit `f5d9aafd2c2a3f40287f365ee37cb55753d6e36e`. Scope: `bms-balancing/`.

R3's GO means a defensible basis for designing our new model, not permission to
send a review to the retired code provider. The findings below concern the
numerical validation foundation; no live external system or private data was
used and target files were not modified.

## Executed evidence

```sh
/home/yonghoon71/ddvenv/bin/python /mnt/c/Users/Administrator/Documents/Codex/2026-08-24/claude-14-gate-code-review-9qkx05-2/outputs/harness_r3_port_repros.py
```

Observed rc `0`: all valid controls and discrepancy assertions passed. The
script uses synthetic numeric CSVs, truthful synthetic optimizer results,
temporary outputs, the actual public Python command dispatcher, and extracted
unchanged `run_states.sh` helpers. It never needs original MATLAB/xlsx data.

### The newly committed 192-value evidence does check arithmetically

I independently parsed each MATLAB `.csv` and the captured full-precision Python
output at the beginning of the matching `.txt`. All four pairs have 16 anchors,
8 matching parameter rows, and 4 matching metric columns. Direct recomputation,
without trusting the verdict text, gives:

| MATLAB artifact | maximum RMSE relative difference |
|---|---:|
| `dd_eval_300_Li_r2.csv` | 4.042289976866168e-12 |
| `dd_eval_pristine_Kunz_r2.csv` | 2.5354636469008477e-12 |
| `dd_eval_pristine_Li_005c_r2.csv` | 3.2797605797850125e-12 |
| `dd_eval_pristine_Li_r2.csv` | 2.6849350033632538e-12 |

This corroborates the arithmetic of the supplied output pairs. It does not
independently rerun MATLAB, bind the private input/source provenance, prove
equivalence outside the sampled inputs, or close the disclosed U1' weighted
function uncertainty. The comparison defects below do not show that these four
particular pairs are numerically wrong.

## P1-P1: R2-01 completeness and finite checks stop before anchors and parameter identity

Locations: `bms_balancing/verify.py:656`, `:659`, `:693`, `:701`.
Reproduction: `comparator_probes()` cases `missing_anchor`, `nan_anchor`, and
`nan_parameter`.

The corrected RMSE cases now work: deleting a row gives `incomplete`, NaN in an
RMSE gives `incomplete`, and a changed finite RMSE gives `model_mismatch`. But:

| New input variation | Actual result |
|---|---|
| Remove expected `E_PE_0p5` anchor | `status=complete`, no problems, "앵커 15개와 rmse 32개 … 전부 일치" |
| Set `E_PE_0p5` anchor to NaN | `status=complete`, no problems, "앵커 16개와 rmse 32개 … 전부 일치" |
| Set one parameter row's `a_PE` to NaN | `status=complete`, 32/32 metrics compared, "전부 일치" |

The new expected/compared counts cover only metrics. Missing anchors merely
print a notice; their finite status is never checked. `max(abs(...)) > tol`
also does not reject NaN in the parameter vector, so the required same-input
relationship is undefined while the result remains complete.

This is a remaining boundary of R2-01, not a repeat of its now-fixed RMSE NaN
case. Minimum correction: validate the complete declared anchor schema and all
five parameter coordinates before comparisons. Missing legacy anchors must
produce a partial result; nonfinite anchors/parameters must make the result
invalid or incomplete. Count/check expected anchors as well as metrics.

## P1-P2: R2-02 still infers producer precision from incidental numeric values

Locations: `bms_balancing/verify.py:538`, `:571`.
Reproduction: `comparator_probes()` case `all_short_g17_column`.

The previous cross-column `1.5` counterexample is fixed. However, a legitimate
`%.17g` file whose pOCV column consists of exact `0.125` values contains no token
with 15 significant digits. The comparator assigns the entire column `atol=.001`.
Let Python differ in one cell:

```text
MATLAB CSV (%.17g): 0.125
Python:            0.1259765625
absolute difference: 0.0009765625 = 1/1024
relative difference (Python denominator): 0.007751937984496124
result: status=complete, worst_rel=0, "전부 일치"
```

Both values are exactly representable dyadics. This is not binary rounding or a
low-precision export. The CSV is full precision; its particular numbers happen
to be short. Knowing that one long token proves precision does not mean absence
of a long token proves limited precision.

Minimum correction: encode or explicitly select the output format/version.
Known `.17g` output uses full-precision comparison regardless of token length.
Unknown-format legacy files need an explicitly uncertain/partial interpretation
rather than value-dependent confidence. Add a full column of exact short tokens
to regression coverage. This does not establish an error in the four committed
recompare files, which contain long full-precision tokens.

## P1-P3: comparison's structured failure is dropped at the production command boundary

Locations: `bms_balancing/verify.py:625`, `:1213`, `:1217`.
Reproduction: `cli_and_stale_profile()` launches a subprocess through
`verify.main(['eval', ..., '--compare', csv])` with an otherwise valid synthetic
objective and a deliberately different finite CSV metric.

Observed stdout:

```text
판정: 앵커는 전부 맞는데 rmse 가 갈린다 (최대 상대차 5.85e+02)
```

Observed process exit code: **0**. `_compare_dd_eval()` now returns
`status='model_mismatch'`, but `cmd_eval()` ignores that return and itself returns
None. The real `main()` returns None, so `sys.exit(main())` signals success.

Minimum correction: propagate a validated comparison outcome to CLI exit codes;
complete supported agreement returns 0, mismatch/invalid input returns nonzero,
and partial results require explicit policy. Add a process-level regression,
not just direct helper assertions. This is the unimplemented production-exit
part of R2-01's minimum condition, not a claim that the current human-readable
mismatch line is hidden.

## P1-P4: the new all-failed profile path silently reuses an old artifact

Locations: `bms_balancing/verify.py:1012` through `:1019`;
`scripts/run_states.sh:59`, `:89`, `:144`, `:150`.
Regression blind spot: `tests/test_review_findings.py:1425` uses an output path
that does not already exist.

The direct R2-03 fix works: failed optimizer points are no longer stored as new
successful rows. Its new all-failed branch returns normally without writing
`--out`. If a previous CSV already occupies `--out`, it remains there.

The reproduction creates a valid old profile CSV, forces all four profile
optimizer calls to fail, and invokes the exact unchanged `run` and
`check_artifact` helpers extracted from `run_states.sh` around that command.
Actual results:

```text
profile log: γ=0 and γ=.5 both report all starts failed
profile log: "저장할 행이 없다 (모든 γ 가 실패) ... 를 쓰지 않는다"
old CSV: byte-for-byte unchanged
run_states helper: "OK (1 초) → .../profile.csv"
run_states helper exit code: 0
```

Thus a failed rerun is counted as a successful current run because the validator
checks existence/nonempty CSV rows rather than whether this invocation produced
the artifact. The normal script then reaches `&& write_meta` at line 150,
which can attach fresh provenance to the stale file; that last consequence is
from the inspected control flow, not claimed as executed in this probe.

Minimum correction: write each attempt to a fresh private output and publish it
only after validating that attempt's result. An all-failed run must return
nonzero or an explicit incomplete result that the wrapper refuses to publish.
Retaining an old useful artifact is fine, but it must not be reported or stamped
as the product of the new attempt. Add an existing-output rerun regression.

## Closure recommendation

R2-01 is partially fixed (finite RMSE coverage works; anchor/parameter coverage
and CLI failure propagation remain open). R2-02 is partially fixed (cross-column
tolerance leakage works; producer precision is still inferred unsafely).
R2-03's result-filtering is fixed, and the acknowledged old-profile convergence
limit is honest; the new stale-output acceptance path needs closure.

The 192-point arithmetic should be retained as sampled agreement evidence. These
remaining implementation gaps should be corrected before treating the harness's
future success states as a reliable basis for new-model design experiments.
