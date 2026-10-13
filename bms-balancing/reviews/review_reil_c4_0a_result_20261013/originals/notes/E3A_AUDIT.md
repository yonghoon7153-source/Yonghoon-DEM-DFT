# E3a independent static audit

Frozen repository: `yonghoon7153-source/Yonghoon-DEM-DFT` at `c542e056b33d25100bc0519ce492c98d3bcce172`.

Read local captures of `reil_c4_e3a.py`, relevant `reil_c5_pilot.py`, `reil_c4_monitor.py`, tests and C4 approval v2. Read preserved `util_LFP.py.txt` and `NOTEBOOK_SOURCE_EXCERPTS.json` through GitHub at this ref. No Python, imports, tests, optimizer runs, notebooks or research data were executed/opened. Line numbers below refer to the local frozen source captures.

## Findings

### E3A-P2-01: C4 array validation is self-consistency, not binding to the accepted C6 arrays

- Location: `bms-balancing/scripts/reil_c4_e3a.py:401-405` (function at 387-406); invoked by `dryrun` at 462.
- `check_arrays` hashes every local artifact against its local manifest (398), checks `ARRAYS.json.c6_manifest_sha256` against the caller's trusted C6 digest (402), and checks each local metadata `npy_sha256` against the local manifest (404). It never compares the local arrays against the authenticated C6 manifest's file entries or an externally pinned expected C4 manifest digest. Its returned C4 manifest digest is computed, not verified.
- Static failure scenario: change one valid NPY array, update its `npy_sha256` in `ARRAYS.json`, and regenerate the local manifest (including the modified metadata hash), while keeping the old `c6_manifest_sha256` string. Every implemented predicate passes although the array no longer matches the accepted C6 array. Even the metadata's old `c6_npy_sha256`, raw hashes and shapes can remain stale without rejection.
- Impact: a new `dryrun` can claim successful array-seal comparison and save a new plan referencing an unaccepted array bundle. This is an existing verification gate in C4-0a, not merely an unimplemented C4-E caller responsibility. It does not establish that the submitted frozen arrays are wrong; the parent review independently compares those actual artifacts.
- Minimal correction: accept the actual C6 seal path, verify its MANIFEST bytes against the caller's pinned digest, then compare all four local NPY hashes to the authenticated C6 manifest entries. Alternatively require and verify an externally supplied accepted C4 MANIFEST digest. Comparing another field inside the same untrusted `ARRAYS.json` alone is insufficient.
- Relevant regression, when separately authorized: alter an array and refresh the local manifest/metadata while retaining the accepted C6 label; validation must reject it. Do not run now.

### E3A-P2-02: the worker discards structural-error partial counters

- Primary location: `bms-balancing/scripts/reil_c4_monitor.py:160-162`.
- E3a producer: `bms-balancing/scripts/reil_c4_e3a.py:273-275`; `Structural` stores `partial` at monitor 28-30.
- Static failure scenario: objective evaluations have already observed nonfinite selected objectives and out-of-domain points, then a later objective raises a structural exception (for example an escaping MemoryError). E3a attaches the task identifiers and all `st` counters to `Structural.partial`, but `worker_loop` emits only `s.info` and a timestamp. `supervise` returns that event unchanged. Shared progress retains only `n_eval` (monitor 153-154,299); the other counters are lost.
- Impact: the failed E3a call's partial diagnostic evidence is unavailable after the global stop, despite the wrapper explicitly preparing it. Do not describe this as losing the entire evaluation count: shared progress can retain that count. X/F/G were not returned, so losing X/F/G is not the issue.
- Minimal correction: serialize `s.partial` into the structural event (as a separately named partial record); preserve the global-stop state and do not mark a failed call successful. A synthetic worker-level check should assert that the partial payload reaches the supervisor when future testing is authorized.

## E3a call behavior accepted on static evidence

- Direct call at E3a 271 is the preserved notebook call with `pop_size=50`. Cases at 43 agree with excerpt cell 3. Algorithm metadata at 100-112 matches util 564-591 and 682-701: GA 20 seeds 0-19, population 50, 100 generations; NSGA2 population 50, 100 generations, seed 1; NSGA3 das-dennis(4,8), 165 reference directions/population, 100 generations, seed 1. The separate util `run_nsga` 150-generation path is not used.
- `n_eval` is incremented before the utility objective (247), including attempts that raise. It does not fabricate a strict optimizer budget: expected counts are documented arithmetic only. Nonfinite selected/all-four counters (259-261) count returned objective arrays; an objective exception is recorded separately instead of treating missing values as a finite result.
- Domain labels intercept the existing single `dVdQ_hc` call (241-244), then use exactly the utility's endpoint-excluded `q[argmin(abs(q)):argmax(q)]` interval (151-158). Empty slices are recorded as unknown; `_tally` runs even if the later utility objective raises (255-258). No extra objective or halfcell computation is introduced. Counts mean evaluations containing at least one experimental Q point outside an interval, not counts of individual points.
- X/F/G preserve returned data and distinguish None from a reported value (290-303); `G_status` distinguishes missing and not returned. The recomputed violation is `max(0,d_N-d_P+1e-4)`, matching util's constraint. Exact residuals use each float's exact rational value with decimal registration bounds. `success_reported` is separated from `success_is_evidence=False`.
- Origin classification walks inward to outward across traceback frames (130-148). An error in `_n_out`, count conversion or another E3a/monitor/C5 wrapper frame is structural even when an outer utility frame exists. An escaping utility or its called-library error is local unless its type is in the explicit structural list. This matches the stated ownership rule. Library origin here describes the owning call path, not a guarantee that a library/environment fault is scientifically local.
- Deepcopy at 233 is semantically justified for numerical objectives: preserved util objective 157-236 reads `Q_exp_interp`, `dVdQ_exp_interp`, `V_exp_interp` and writes different `Vf_sim`, `Q_sim`, `Vf_sim_4Cap`, `Q_sim_max`, `dVdQ_sim` keys. Halfcell arrays are read, not mutated. Notebook excerpt cell 8 shares one Model among cases, but those added output keys do not feed subsequent objective values. Base-model and halfcell digests are compared before and after (232,279).
- Case-major instead of cell-major ordering is numerically justified for independent calls using the same frozen environment and inputs: utility minimizers receive explicit seeds for every GA and NSGA run. It does not establish bitwise equivalence of elapsed timing or change what the notebook saves in its mutated Model objects; those are outside the numerical result claim.

## Disclosed, nonblocking evidence limitations

- Test 349-364 accepts either a returned NSGA2 result or a utility-local error after at least one objective attempt. Pytest's captured passing output is not preserved in the submitted log according to the result request. Therefore `26 passed` establishes this test's branch-tolerant call contract, not a completed 5,000-evaluation NSGA2 run or a returned Pareto front. No rerun is warranted without new authorization. On the next separately authorized run, persist the structured outcome and evaluation count as an artifact.
- Tests 340-346 exercise utility ValueError and MemoryError but do not directly inject a wrapper-origin error. The static classifier rule is sound; additional origin-specific test coverage would be useful without claiming the current suite proved every origin branch.
- Any exception swallowed internally by preserved utility code (for example its broad except around peak scoring) cannot be classified by this wrapper. This is inherited utility behavior, not a newly introduced wrapper defect.

Overall E3a call recording, objective selection, explicit-seed ordering and deepcopy rationale are acceptable on the inspected static paths. The two findings above concern the implemented artifact-validation and structural-diagnostic handoff paths and should not be obscured by the passing synthetic suite.
