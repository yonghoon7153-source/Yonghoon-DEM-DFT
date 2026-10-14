# RRM/N9 and T2 adversarial review notes

Pinned source: `1087a9b2f4a93aa6a3b0debc698a14fffa13488d`, read-only snapshot under `rint_g2_impl_review_20261014/source`. No source changes, simulations, production runs, WSL, or Git writes performed. Only small offline geometry calculations and existing small FV fixtures.

Evidence: `../evidence/rrm_probe.json`; reproduction: `../probes/rrm_probe.py`. Runtime: Windows Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3. The supplied ladder used Linux Python 3.11.15/NumPy 2.4.6/SciPy 1.17.1, so the 45-degree floating-point tie allocations are not bit-identical. The newly identified boundary error is also reproduced at 15 and 30 degrees with no ties.

## Confirmed findings

### P2: Tilted MMS skips the film on crossed boundary half-cells

Location: `scripts/rint_t2_dev.py:190-192` (context 185-192). The boundary assembly always uses `gb = 2*sig[cell]*h`, then evaluates the piecewise exact potential at the boundary face. If the cell center and face center are on opposite sides of u=0, that half-cell contains both materials and a membrane. The current assembly connects directly across the potential jump with pure bulk conductance. This occurs with the existing default ladder, so no mutation is required.

Actual maxima from instrumenting the existing `mms_solve` function:

| Axis law fixture | Maximum error | Cell | Cell u | Boundary u | Tie cells |
|---|---:|---|---:|---:|---:|
| theta 15, n=64 | 0.5376755856049966 | (23,63) | -0.001439240068191933 | +0.001795997995589549 | 0 |
| theta 30, n=16 | 0.5038084526638738 | (3,15) | -0.01471143170299749 | +0.01028856829700253 | 0 |
| theta 45, n=128 | 0.44429102168588724 | (0,127) | -1.11e-16 | +0.004419417382415913 | 128 |

The probe's `boundary_control` changes only the crossed boundary couplings in the already assembled matrix and RHS. Interior faces, the exact boundary potential, and the exact error target remain unchanged. Let `d1+d2=h/2` be the exact distances to the planar interface, computed by linear interpolation of u. Replace the bulk-only coupling by

`g_boundary = h^2 / (d1/sigma_cell + d2/sigma_boundary + 1e4*rface_candidate)`.

The candidate film ASR is the same L1 or axis law already used by the harness. This is a diagnostic control, not a claim that the full tilted scheme is now validated.

| Fixture | Original L2 | Boundary control L2 | Original max | Boundary control max |
|---|---:|---:|---:|---:|
| 15 deg, n64, axis | 0.01306318860 | 0.0004495112904 | 0.5376755856 | 0.006475555385 |
| 30 deg, n16, axis | 0.04096008793 | 0.003087791839 | 0.5038084527 | 0.01633704071 |
| 45 deg, n128, axis | 0.003835149728 | 0.0009205293577 | 0.4442910217 | 0.005660516619 |
| 45 deg, n128, plane shifted 0.001 um, axis | 0.003883094200 | 0.0009823643239 | 0.4439262878 | 0.004030350534 |
| 15 deg, n64, L1 | 0.01282826063 | 0.001406042364 | 0.5324747283 | 0.02030409571 |

The shifted 45-degree case has zero tie cells; it still has the 0.44 error. Even excluding tied cells from the original 45-degree error norm leaves maximum non-tie error 0.11724899629513752. Therefore the README's `docs/data/rint_t2_dev_20261013/README.md:53-55` claim that the plateau is a point/tie assignment limitation is not an adequate diagnosis. Boundary film omission accounts for the large spikes and plateau. Ordinary nonmonotonic stair-step error and tie policy remain separate questions. Fix boundary interface treatment and update this diagnosis before using these ladders to choose D11 or seal D12-V. The existing axis-aligned exact tests are unaffected and did not exercise this branch.

### P2: RRM checker accepts NaN film resistances and the wrapper then solves a bypass

Location: `scripts/rint_rrm_reference.py:318-321`, especially comparison at 320. The test `abs(rface-want)>tolerance` is false for NaN. Replacing the 67 film-row `rface` entries in clean fixture A by NaN, preserving cut rows, and refreshing the row fingerprint yields `rrm_check == []`. `rrm_require` and `rrm_solve` accept it. The production face function at `scripts/step3_sigma.py:354-356` treats NaN as `r>0 == False`, preserving bulk conductance on those faces.

- Clean RRM sigma: 0.003334457143882423 S/cm.
- NaN film rows, same outside cuts: 0.0037299595666211234 S/cm.
- Result reports `unconverged=False`, residual 6.2089744354216986e-15.

Scope: this is a development-validator fault, not a demonstrated default producer failure. The ordinary `rrm_plan` with the finite supplied fixture does not create NaN. Refreshing row fingerprints after a controlled fault is the repository's explicit N9 test convention, allowing the checker to test semantic correctness independently of E5. Add explicit finite/nonnegative row validation before numeric comparison; do not broaden this finding into a production-security claim.

Related validator weakness (optional separate finding or hardening note): `rrm_check` trusts mutable recipe fields and skips excluded contacts without checking the claimed prior rejection. Remove all 85 outside cut rows as the supplied N9 mutant does; alone this is rejected. Changing only `record.iface_rrm.resolve_k` from 4 to 5 makes `rrm_check` skip the contact at lines 295-302 and return []; setting `record.iface_r_type_ohm_cm2={}` instead also makes the film set empty. Both pass `rrm_solve`, giving sigma 0.0040840140889134725 S/cm, `unconverged=False`. Normal planner calls with those inputs would reject. This needs recipe binding or fail-closed eligibility revalidation if N9 is advertised as an independent plan validator. It requires an additional metadata fault beyond the current row-only negative tests.

### P3: RRM retains unlabeled CNC totals in its ordinary returned record

Location: `scripts/rint_rrm_reference.py:235-244`. After replacing CNC rows, `rec=dict(base['record'])` and the subsequent updates leave `iface_contact_ledger`, `iface_carbon_cover`, and uniform `rface_c` data describing the CNC plan. The RRM-specific nested record is correct, but generic consumers receive contradictory counts/totals without a label that those fields describe the discarded CNC plan.

- Clean fixture A actual rows: 67 film, 85 cut. `record.iface_contact_ledger.film_faces.active=152`, `cut_faces=0`.
- A legitimate half-carbon variant of fixture A has actual rows 37 film, 42 cut and RRM conductance 2.7535056597827278e-6 S. Inherited `film_G_S_total.remove_area=2.612935414333538e-6`, `renormalize=5.027420037705035e-6` S. The RRM `contacts[0].film_G_S` correctly gives 2.753505659782727e-6 S.

Recompute RRM-specific standard diagnostics or clearly move the CNC-only fields into a labeled comparison record. This does not change the correctly assembled clean RRM solve.

## Positive checks and question answers

- Q1: The restricted axis-aligned RRM mechanism matches the v3 definition, subject to validator and reporting corrections above. Independently integrated 1000 randomized circle/rectangle intersections using numerical quadrature; maximum absolute difference divided by a^2 was 1.73102875081053e-13. Unequal-radius mixed-material fixture B rotated onto x, y and z gave identical `a=0.44374348899298655`, sum weights 0.6186056185197304 um^2, coverage 1.0000000000000004, zero rejections and zero checker violations. Fixture A area/weights and the supplied N9 bypass sigma independently reproduce. Off-axis faces are explicitly assigned zero weight and cut; tilted contacts reject. Caller-provided k and the development-only label correctly avoid inventing D12-V. These mechanism checks do not certify RRM discretization error or independence as a reference.
- Q1 N9 scope: Keeping the RRM guard in `rrm_solve` and production code unaware of RRM is consistent with trial-only architecture; the direct production solver accepting the supplied N9 mutant is already disclosed and is not a new finding. All RRM harness calls must use the wrapper, and its checker needs the above corrections.
- Q2: No new evidence requires reconstructing the neck before any T3-B experiment. Cut is the contract's declared recommended default and reconstruction is an alternative, not a required second implementation. D17 confirmation still remains with the author. Before calling T3-B differences certified CNC bias, freeze this selected RRM and check its own error against separate analytic/MMS/frozen geometry, as v3.1 section 6 requires.
- Q8: Exact algebra/manufactured-field checks and the aligned exact discrete solve can legitimately pass/fail as mechanism tests before D12-V. Our independent theta0, beta3, n16 solve had max error 8.881784197001252e-16 and L2 2.723647616275778e-16. Tilt ladders remain development output. D12-V should specify origin/tie treatment, but tie exclusion or origin shift is not a substitute for repairing the boundary defect. T2-1 full acceptance still needs its independently specified flux/energy observables, origin and 3D coverage; current harness only returns potential norms and film-face count.
- Q10: No prohibited pre-D12-V validation PASS was found in the inspected RRM/T2 labels or outputs: they explicitly say development/not verification and forbid later relabeling. Exact mechanism PASS is appropriately distinguished. The claimed first-execution history is a provenance claim, not something source inspection alone can independently certify. The boundary defect invalidates the supplied causal diagnosis, not the permission to run development experiments.

## Reproduction

From the user workspace root in PowerShell:

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
$env:TEMP=(Resolve-Path rint_g2_impl_review_20261014/tmp).Path
& 'C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' rint_g2_impl_review_20261014/probes/rrm_probe.py
```

The script imports only the pinned snapshot, plus the already installed science dependencies. It emits JSON. The saved evidence was created directly from the successful command's JSON output. No target source or test file was patched.
