# Numeric lane — independent L214R recheck, 2026-10-17

Code pin: `60ba39e224aff48a030dccfe750342f3bf9db61f`; comparison base:
`6cb2569569ec74b7f5a96e0ef19494e872da5272`. Both are manifest-backed file trees,
not Git checkouts. Production source was not edited. Only review probes, evidence,
and temporary fixture files were written. No real specimen / LHS214 / WSL run.
Tiny 3-node and 21-node synthetic circuit calls are isolated review probes.

## Result

L214R-01 A/B and L214R-05–10 close their stated counterexamples. The advertised
four numeric suites reproduce exactly. There is one additional **P2** gate gap:
an authentic above-limit FULL numerical proof can be relabeled as computed and
its withheld scalar restored; the consumer then publishes that forbidden FULL
value and loses the independent H0 model-limit flag. The producer's own guard is
correct. This is consumer contract enforcement on a mutated record, not evidence
that the real 214 results contain such a record.

## P2 candidate NUM-NEW01: computed FULL bypasses the fixed q > 1.5 guard

Relevant source locations:

- `scripts/tau_flux.py:743`, especially `:787–810`: reconstructs positive finite q
  and matches the rounded reported values, but does not reject a FULL q above
  `network_conductivity.FULL_Q_GUARD_MAX`.
- `scripts/tau_flux.py:399–414`: `full_model_limit_flag` returns False immediately
  for a reported computed record, even when its proof reconstructs q > 1.5.
- `scripts/network_conductivity.py:1471`: genuine producer withholds FULL when
  raw q > 1.5. This behavior is correct and unchanged.
- `scripts/lhs_release_build.py:693`: the H0 release HOLD only receives the status
  and flag produced upstream; the mutated record yields OK / False.

Independent fixture: 21-node SE-only series network, box 0.7 × 0.7, thickness 20,
each contact area 0.5 and delta 0.2. Actual production function's H0 proof has
`q_withheld=1.6231747351909995`. The untouched control returns
NOT_COMPUTED/full_over_conduction, H0 flag True, and the primary release HOLD.

Exact mutation to the H0 record (no other mode is altered):

| Slot | Replacement |
|---|---|
| sigma_full | round(q_withheld, 8) = 1.62317474 |
| sigma_full_mScm | round(q_withheld * sigma_grain_S_cm * 1000, 6) = 4.869524 |
| sigma_full_status | computed |
| sigma_full_reason | null |
| ionic_status | computed |
| ionic_status_reason | null |
| solve_certificate_full.status | computed |
| solve_certificate_full.reason | null |

All certificate numerical fields, electrode currents, geometry, method,
convergence/attempt records, and q_withheld/q_guard_max/guard_policy/sum_g remain
unaltered. Thus no new numerical solution is forged; the same certified solution
is incorrectly admitted across a known output-policy boundary. Keeping the
certificate's original over_conduction status correctly rejects the record;
changing its two labels exposes the missing q-based check.

Observed after mutation:

- `ion_record_problem` = None.
- `certificate_binding_problems` = [].
- `network_generation_contract` = g2, problems [].
- Both `network_content_verdict` and `network_record_verdict` = `(True, 'ok…')`.
- `ion_columns`: H0 OK, f = 1.62317474, tau2 = 5.52989076841878,
  full_model_limit_hertz = False.
- After ordinary `_cell` string serialization, `v13_primary_model_limit_problems`
  = [] (untouched control returns the H0 HOLD). This checks the actual release
  primary-model-limit gate, not an entire release package build.

Evidence: `evidence/numeric_adversarial.json`, object `restored_primary_H0`.
Before/after dual and mode files: `tmp/numeric_h0_before/` and
`tmp/numeric_h0_after/`. The JSON also contains a Physics example with q
2.593468501694396, admitted as OK with f 2.5934685.

Boundary evidence (`full_guard_rounding_boundary`) shows genuine raw q values
1.4999999999999998, 1.5, and 1.5000000000000002 all store q=1.5. The last one is
correctly withheld by the producer but passes `_cert_published_problem` after
the two label changes. Minimum repair should check the reconstructed raw q for
the FULL ionic branch using the existing strict `>` policy. Checking only rounded
`sigma_full > 1.5` would leave that edge case open. CF / constriction-only
model_over_conduction must retain their intentional published-value behavior.

The consumers lane subsequently confirmed the full real stop → reread → P0–P4 →
handover → build_v13/check_v13 chain in `evidence/consumer_h0_resurrection.json`.
The minimal mutation above is rejected by stop contract ④ because its power-share
field still carries the genuine withheld status. Restoring the same-fixture
thermal H0 power share (0.797464) / computed status and the ordinary full_metrics
and batch projections lets the full chain pass: 27 files, warnings [], reread
performed, check_v13 []. Currents, geometry, attempts and guard diagnostics remain
unchanged. See that lane's evidence for its exact additional edits and commands.

## Existing fixes and independent checks

| Original item | Closure in this lane | Source anchor |
|---|---|---|
| L214R-01 A | Closed: finite T/A and reconstructed q; overflow scale/int become rejection | network_conductivity.py:954, :1075, :1085 |
| L214R-01 B | Closed: final accepted attempt must satisfy the same numeric and method rules | network_conductivity.py:981, :1007 |
| L214R-05 | Closed: published proof's geometry, q and dimensional σ comparisons reject nonfinite arithmetic | tau_flux.py:721, :787, :802 |
| L214R-06 | Closed: all three published ionic branches bind adopted attempt | tau_flux.py:758; network_conductivity.py:1007 |
| L214R-07 | Closed: record dimensional identity rejects nonfinite product/difference/tolerance | tau_flux.py:272 |
| L214R-08 | Closed for stated big JSON integer cases; N5 remains separately declared | tau_flux.py:174, :189, :827 |
| L214R-09 | Closed: value-state f/tau2/tau finite-positive check | tau_flux.py:1364, :1371, :1373 |
| L214R-10 | Closed: recalculated temperature reference/factor and comparisons checked before equality | tau_flux.py:895, :908 |

The new H0 guard counterexample is a separate policy-consistency issue; it does
not reopen the fixed finite-arithmetic or adopted-attempt counterexamples.

| Check | Result |
|---|---|
| test_l214r01_certificate.py | 112/112, rc 0 |
| test_l214r05_published_certificate.py | 184/184, rc 0 |
| test_l214r06_same_class.py | 306/306, rc 0 |
| test_l214r09_same_class.py | 96/96, rc 0 |
| Adapted previous independent numeric probe | 38 solver cases, 14 certificate mutations, 5 records, rc 0 |
| Earlier independent residual/conservation/error/Krylov/geometry overflow counterexamples | rejected as intended |
| Solver ladder bytes, base vs final | identical |
| Normal synthetic producer records, two modes, base vs final | full previous fields bit-identical |
| Fresh adopted-attempt sweep | 252 mutations, zero accepted, zero exceptions |
| Fresh ledger extreme/type sweep | 36 cases, zero exceptions or invalid values in OK/MBCB rows |

The adoption sweep independently mutates currents, residuals, conservation,
Krylov info, error, outcome and method for both modes and each of the three
published ionic branches. The ledger sweep includes 5e-324, 1e-310, 1e-200,
1e-100, 1, 1e100, 1e200, 1e308, 10**400, NaN, inf, and bool. It checks that any
OK/MBCB row's f, f_gap, tau2 and tau are finite positive numbers.

`numeric_runner.py` reuses the previous `l214_numeric.py` by an explicitly
documented in-memory adapter. Changes are ROOT/pin/base and the old-base
four-field exclusion (those fields already exist in the new base, so compare
the complete record). All original numeric probes remain unchanged. Exact
original/derived hashes and replacement strings are in
`evidence/numeric_probe_adapter.json`. This is an adapted rerun, not a claim of
byte-for-byte unchanged execution.

Packaging: the exact original probe bytes are also bundled as
`probes/numeric_l214_original.py.b64`, SHA-256
`c77e316e6a1b1555f9f9135912c9bd397d2213d03b1628f4bcf6166a62f7493d`.
The runner verifies this hash whether it reads the prior sibling probe or falls
back to the bundle when the sibling is absent. `--verify-bundle` confirmed valid
syntax and identical normalized input text through the fallback loader without
rerunning the numeric work; see `evidence/numeric_bundle_verification.json`.

L214R-07 rejects nonfinite/underflowed reconstructed dimensional σ and finite
comparison arithmetic. L214R-08 converts 10**400 to a rejected non-number without
an exception in the covered consumers. L214R-09 guarantees finite positive
value-state f/tau2/tau. L214R-10 rejects nonfinite recalculated Arrhenius reference
and factor before comparisons. No new failure of those repairs was found.

## Design choices 1, 2, 3, 4, 9 and 10

1. Adopted-attempt Krylov/direct distinction matches the actual producer ladder.
   Prior failed attempts remain legal; only the final accepted attempt must agree.
2. Extreme scale now yields invalid_geometry rather than OverflowError. This is
   a fail-closed improvement and does not change the compared normal circuits.
3. 0b delegation is coherent **when callers use the documented conjunction**:
   `ion_record_problem` plus generation/certificate contract. `generation == g2`
   or `certificate_binding_problems == []` alone is not a record-validity verdict.
   Actual publication record checks and τ consumption apply 0b as well.
4. `channel_verdict` / content checks are status-level checks and are valid only
   as part of the composed publication contract. They do not certify σ numerics.
9. N4 is a real unvalidated channel boundary: changing Physics thermal σ_dim by
   ×10, or to NaN, leaves content and record checks True and ionic τ OK. The
   current ionic τ review can defer the declared σ_e/σ_th QV4 work, but no broader
   claim that all published conductivities are numerically certified is justified.
10. N5 goes beyond the request's NaN description: NaN, +inf, -inf, bool and a string
    are all treated like no numeric I_bottom on an unpublished CF branch; null
    is the ordinary control and 10**400 is now rejected. All accepted variants
    leave the valid ionic FULL τ unchanged. This is a P3 schema-consistency
    hardening item, not an observed bad FULL numerical value / GO blocker in this
    scope. Prefer explicitly null/absent I_bottom later, since production emits
    null, but keep the no-value branch distinction.

## Known items K1–K3

- K1 reproduced: `tau2_from_metrics({'phi_se': .3, 'sigma_full_mScm': 1e-310})`
  gives `(inf, 3.0)`; `tau2_value(1e308,3,1e-3)` gives inf. P3 display/getter
  hardening for this scope; do not say every τ API now guarantees finiteness.
- K2 reproduced with full_metrics temperature_provenance.sigma_ion_T_factor
  = 10**400: tau2_from_metrics raises OverflowError. The stop-contract call is
  inside its exception-to-rejection block (`pipeline_service.py:1071–1095`).
  P3 reason/availability hardening; not silent accepted g2 handoff.
- K3 reproduced using the genuine historical lhs00_001 nonpercolating dual
  record, changing both sigma_grain_S_cm to 1e306: both 0b checks pass,
  NOT_PERCOLATING f=0 remains, but ion_sigma0_mScm=inf. Source `_sigma0` at
  tau_flux.py:1253 lacks a finite check. Historical-reader metadata hardening
  (P3); current g2 production admission separately applies σ₀ convention checks.

No additional pre-GO blocker from K1–K3 is established for the explicitly bounded
g2 ionic handoff task. K4–K8 and release/publication details are assigned to other
lanes. Q5's normal-case comparisons support the tested normal cases; they cannot
establish that the corrected defects are the only behavior-changing or invalid
input cases, as NUM-NEW01 shows.

## Reproduction

From the workspace root, PowerShell (the scripts set TMP/TEMP to review/tmp and
OMP/OPENBLAS/MKL/NUMEXPR thread variables to 1; no bytecode writes):

```powershell
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'lhs214r_fix_recheck_20261017/probes/numeric_runner.py' --tests
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'lhs214r_fix_recheck_20261017/probes/numeric_runner.py'
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 -B 'lhs214r_fix_recheck_20261017/probes/numeric_adversarial.py'
```

Dependency roots are workspace/lhs_coverage_review_20260930/deps and
workspace/gen2_network_reverify3_20261007/deps. Logs and exact commands are saved
in `evidence/numeric_selftests.json`; detailed selftest logs use prefix numeric_.
