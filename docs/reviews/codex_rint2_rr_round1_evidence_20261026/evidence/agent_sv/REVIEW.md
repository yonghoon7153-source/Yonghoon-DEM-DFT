# SV certificate / topology read-only re-review

- Pin: `9bec6b7646374daed0d3edbb9647f9f46d302750`; baseline: `0b3012460fb8e8b7d53484b0efe399e2dc506aec`.
- Date: 2026-10-26. CPU-only small synthetic circuits. No production-source or Git changes; no DEM/GPU/S0/registered R campaigns.
- Runtime: bundled Python 3.12.14, NumPy 2.5.3, SciPy 1.16.3, BLAS threads 1. Actual versions are recorded in `probe_actual_results.json`. This is independent evidence in a different runtime, not reproduction of the author's 3.11/3.8 environment claim.

## Closure decisions

| Finding / claim | Decision | Evidence / limitation |
|---|---|---|
| RCA2-01 | **CLOSED — original minimum** | Original perturbed-first-solve counterexample now yields nominal 10.291249475344962 < threshold 10.291251705345072 < certificate lower 10.29125393534377 and `SV_DEPENDENT`. Actual producer, certificates, projection, `ca_ext_record_ok`, `sv_assess`; no manually fabricated interval. Independent Fraction oracle: 25,100 quotient pairs, zero violations, including 3,077 overflows and 3,181 subnormal/zero results. |
| RCA2-04 | **PARTIAL** | Original F3 cases are repaired: missing endpoint certificate, foreign certificate, unregistered bracket/cut/kind rules, count 10^400 and inconsistent removed component count all rejected by actual `ca_ext_record_ok`. Expanded same-run endpoint identity is not complete: disclosed k=0 limitation below now has a harmful concrete circuit, with every count unchanged. X6 remains open as explicitly deferred. |
| RCA2-06 F4 | **CLOSED — original minimum** | Unmodified QD4 resident test runs correct two-component case (six cells removed, upper infinity), and first-component-only memory mutant (three cells, upper ratio2) fails intended assertions. At test threshold2.5 correct `SV_UNCHECKED`, mutant clear. This is resident coverage repair, not newly discovered production miscalculation. |
| RCA2-06 F6 | **CLOSED — original minimum** | Real producer census0/actual1 and census1/actual2 failures pass `ca_ext_record_ok`, remain `SV_UNCHECKED`, and preserve `unsplit_census_mismatch` in reason. Unchanged resident SM function:37 PASS/0 FAIL. |
| RCA-06 | **CLOSED — original explicitly stated minimum** | Prior partial-note's only remaining closure condition was RCA2-01 verification, now satisfied. Integrated SV-record correctness remains partial under RCA2-04; do not conflate that with keeping the original P1 open indefinitely. |
| A′ C1 / A″ topology substitution claim | **PARTIAL** | k>0 original main-to-end swaps rejected; honest FLOAT, UFLOAT and contracted PAR records accepted. Counts do not identify a weighted graph when parallel multiplicity changes. |
| A′ C2 directional rounding | **CLOSED within tested arithmetic contract** | Exact-rational enclosure and optimal adjacent-float checks; QD6 resident knife tests pass. |
| A′ C5 kind/rule | **CLOSED — name contract** | Unregistered names rejected. This verifies names, not reconstruction of the cutting semantics. |

## P2 — harmful realization of the already disclosed k=0 limitation

This is **not a new regression class**, not evidence that an honest producer miscalculates, and not a production/default-threshold result. It supplies the concrete harmful circuit that request §8 and preattack2 had not found.

**Location:** `scripts/ca_ext_svcf.py:641–647` accepts a main certificate as the lower-end certificate when k=0 and the four topology counts agree; `scripts/carbon_junction.py:2162–2191` counts removed *unique pairs*, ignoring a removed parallel edge while another survives; `scripts/carbon_junction.py:2387–2404` supplies that k. `scripts/rint_r_chain.py:1441–1446` only adds equality of the copied *main* certificate with the run's main certificate; that equality remains true here. Acceptance reaches actual `scripts/run_contract.py:749–760`.

**Small actual geometry:** begin with resident PAR (`test_carbon_junction.py:4389–4392`), c=1; prepend `(0.5,1.5,9.5)` to the third polyline. This extends its dangling left branch to the upper electrode. Raster→registry→plan→solve→certificates use unchanged production functions. Honest record:

| Quantity | Main | Cut |
|---|---:|---:|
| Actual positive edge multiplicity |22|21|
| Unique edge pairs |21|21|
| DOF / bottom / top couplings |23 / 2 / 2|23 / 2 / 2|
| G |19.95024875621891|19.615384615384567|
| Certificate topology tuple |[21,23,2,2]|[21,23,2,2]|

`n_sv_faces_cut=1`, `n_reach_pairs_cut=0`, unsplit census=0. Honest certified ratio is `[1.0170715052189403,1.0170715052190658]`. A separate exact Fraction elimination of the captured assembled matrices gives ratio **1.0170715052190031**, inside the interval.

Now replace only the lower-end certificate with this same run's main certificate, update its G/nominal ratio and recomputed interval consistently, and mirror the upper alias (no upper solve exists). **No `n_*` count and no census field changes.** Both honest and edited manifests pass actual `run_contract.ca_ext_record_ok` `(True,None)`. At legal illustrative threshold **1.01**, `sv_assess` changes **`SV_DEPENDENT` → `[]`**. The read_run main-certificate comparison keys remain equal to the real main certificate.

The pin has **no numeric registered/default SV threshold**: `rint_r_chain.py:837–839` accepts a finite number >=1, and require_plan_numbers rejects null; the registration defers the author's choice until after review/before DBE. At t=2 this particular honest circuit already clears. Do not report it as a failure at a production threshold.

**Consumer boundary:** the actual full ca_ext consumer and decision function were invoked; the full filesystem/registration `read_run` pipeline was not. Its main-certificate comparison was checked on unchanged actual main certificates, rather than claiming the unrelated gates were exercised.

**Minimum direction:** bind each endpoint certificate to its assembled **weighted graph**, including multiplicity or canonical summed conductances, retained DOF identity, and electrode couplings, and compare against an expected endpoint identity from outside the editable SV record. Here raw multiplicity22→21 and weighted digests differ even though topology tuples agree. An internally editable digest alone does not protect coordinated forgery. B's proposed external S0 census binding by itself cannot catch this example, since every census/cut-count field is unchanged. Do not require `G_cut != G_full`: deleting an equipotential edge can honestly leave terminal G unchanged.

Artifacts: `probe_actual.py`, `probe_actual_results.json`, `k0_honest_manifest.json`, `k0_swapped_manifest.json`, `k0_actual_evidence.json`, `k0_actual_main_result.json`, `probe_weighted.py`, `k0_assembled_systems.json`, `weighted_graph_results.json`. Manifest hashes are in the result JSON; a final SHA256 inventory is alongside this review.

## Disclosed deferred issues independently reproduced

- **X6 P2:** five actual fixtures (QD2-3, QDX, RAIL5, QD2-1, QD4). Remove upper and consistently set both SV-record and evidence-census unsplit count to0: **5/5 actual ca_ext consumer accepts, `SV_UNCHECKED`→clear**. Without census edit,5/5 reject. Location `ca_ext_svcf.py:688–709`, especially701–707: compares copies within the record, not outside-record evidence.
- **X3 P3:** QDX lower certificate←upper, G and ratio correspondingly changed, cut counts unchanged: consumer accepts; t=2 `SV_UNCHECKED`→`SV_DEPENDENT`. Conservative direction, distinct from false clear.
- **X5 P3:** both ends topology-zero fixture accepts eight malformed lower k values (bools, -1,1.0,string,None,2^63,10^6). Location `ca_ext_svcf.py:601–605`: early return when neither end is computed. No decision effect in that route.
- **Honest FLOAT handling:** actual FLOAT, UFLOAT and original PAR c=1 all pass full ca_ext consumer and honestly clear at t=2. Do not revert to requiring changed counts whenever raw edges were deleted.

These record-edit limitations do not invalidate untouched developmental S0 stage1 or SBE iteration/cost probes. They must remain explicit before any registered R interpretation. No evidence here requires blocking the reading of S0 stage1 output. For C7, these probes use real producer-generated census, I_bot and fingerprints, satisfying the updated schema; the entire old geometry suite was **not** replayed and old-schema rejection is not counted as closure.

## Reproduction and verification

From PowerShell in the review root:

```powershell
& ./evidence/agent_sv/run_all.ps1
```

The runner uses the requested bundled Python with `-X utf8 -B`, cached NumPy/SciPy paths, and isolated temp. Direct new probes take a few seconds each. It also invokes:

```text
python -X utf8 -B repo/scripts/test_carbon_junction.py --only QD2,QD3,QD4,QD5,QD6,QD7
python -X utf8 -B repo/scripts/test_ca_ext_b6.py --only S --skip-payload
```

- QD2–7: **126/126 PASS**, `resident_qd.log`. Includes F4 memory mutation, numerical knife cases, topology swaps and80 honest motifs (floating and c=1 cases).
- Direct unchanged SM helper: **37 PASS /0 FAIL**, `resident_sm.log`; complete consumer scaffold, actual producer subcases preserved.
- Targeted B6 S: **254 PASS /0 FAIL**, `resident_b6_s.log`, after the root reviewer fetched the historical cohort JSON/receipt inputs at the pin. Payload subgroup is deliberately skipped.
- Independent exact quotient oracle: **25,100 pairs;0 failures**, `rounding.json`.
- Independent actual producer/consumer and exact weighted-system probes: all assertions pass. `deferred_and_f6_results.json` preserves outcomes and reasons.

No inference of general production correctness follows from these counts. Known record identity limitations are preserved rather than treated as negative-test success.


