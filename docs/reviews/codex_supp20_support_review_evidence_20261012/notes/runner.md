# Runner / reread independent review

Review pin: `b429c3c1df0956d2721861d89cc29a2d56f2b581`; baseline: `3cedd40a5911d0606bf33ed2085d5cb93c4db2e0`.

Scope: `scripts/run_network_194_parallel.py`, `scripts/g2_network_reread.py`, and supplementary registration. Source files were not edited. The supplied source tree is an exported snapshot, not a Git checkout; attempted Git identity/status checks therefore returned “not a git repository.” Pin provenance belongs to `evidence/pin_receipt.json`. Probe: `probes/runner_probe.py`; observations: `evidence/runner_probe.json`.

## Result

No new blocking defect in the changed runner/reread code was established. The actual default plan is still exactly 194 cases in `lhs,lhsx`, identifies as `production194`, and requires observation. Its ID digest is `a04282d7275bd8f92b0afb4ac8b045f72f3867ccebbb7813b530b3901fd7b3bf`; code fingerprint is `e8b2496b9c2ecf6edad8c6b52d32a2514c96dd54c9a20823c300639249ecae71`.

The actual pinned snapshot cannot yet establish `supp20`: the expected harvest directory is absent and both runner registration and reread registration raise `LaunchError` with `n 0`. With a synthetic registered 20-file harvest, the shared observation predicate and preflight reject observation disabled, allow it enabled, and print `--expect-set supp20` in followups.

## P2 operational gap, already disclosed: production intent is lost when registration cannot be established

Locations: `scripts/run_network_194_parallel.py:1016`–`1022` (swallows registration failure), `:1035`–`1039` (observation requirement only for a recognized set), `:1749`–`1750` (wrong full-cohort count merely warns), `:2309`–`2311` (followup falls back to explicit cases). Audit uses the same observation predicate at `:2654`.

Reproduction: leave default supplementary registration absent as at this pin, supply a temporary 20-case harvest through the supported `--lhss-harvest`/`--lhss-cohort` override, and build the plan. The ID digest is exactly the registered supplementary digest, but `registered_production_set` and `production_observation_problem(observe_imports=False)` both return `None`. Isolated preflight returns an empty `stop` list. Printed reread followup contains 20 `--expect-case` options. The same plan with a valid registered harvest is recognized and stopped for observation disabled. Once registration exists, a 19/21/wrong-ID/thick-substituted plan is likewise treated as unregistered; 20-to-20 substitution has no count warning.

Consequence: a generic preflight success or generated explicit-case reread command is not proof of supplementary production eligibility. The generated expectation is selected from the same plan, not independently from `supp20`. The request discloses the registration-unavailable observation gap, and the full-cohort/partial-plan policy predates this change for production194. This is not a newly proved release false-green, and it need not block the documented exact registered launch after the missing inputs are committed and verified.

Action: require positive `registered_id_set('supp20')` resolution, exact registered plan membership, and `--expect-set supp20` at launch signoff. Optional code hardening: an explicit production-set mode should fail closed on unavailable/mismatched registration and always retain the selected set for followups. Keep partial/pilot runs an explicit separate intent. At minimum qualify registration §3's unconditional “observation mandatory” wording with its registration prerequisite.

## Count, ID, and expectation binding

- Synthetic registration rejects 19 cases, 21 cases, same-count replacement, thick-case addition, and thick-case replacement.
- Detailed reread contract accepts its well-formed 20-case contract fixture and rejects missing cases with unchanged summary, same-count replacement, duplicate rows, wrong cohort, thick replacement, false checks under `n_fail=0`, empty check lists, integer `1` in place of boolean `True`, and passing the supplementary detail to the production194 expected set.
- The set recognizer itself collapses duplicate queue entries, but `plan_problems` rejects the duplicate; this is not a false-green path.
- AST comparison against the prior review snapshot confirms unchanged `registered_id_set`, `build_plan`, `cohort_specs`, `preflight`, `print_followups`, `plan_input_digest`, `registered_expected`, `explicit_expected`, `run_launcher`, `launcher_detail_problems`, and `launcher_identity`. Reread production changes in the submitted diff are documentation/help additions; its supplementary test exercises existing generic logic.

## Q5 / Q6 advice

The runner changes do not weaken the tested existing 194 behavior. However, the old GO applies to its original pin; this review's evidence is for the new pin and does not supply the missing supplementary data or release evidence.

For two-batch launch: commit r3 harvest/cohort/union artifacts; record the `1e09f661d` reharvest provenance and r2 keywise comparison; verify exactly `lhss_001` through `lhss_020` with no `lhst_*`; fill and ratify the registration; independently resolve both registered sets and compare each dry-run ID, raw-table, and cohort TSV fingerprint to its registration; run the required final-pin WSL preflight/smoke checks on a clean tree; use observation on both batches, separate fresh roots, and the explicit registered reread set for each. Launch/deployment authorization and post-run gates remain separate.

Important Q6 distinction: `registered_id_set` at `:990`–`1006` compares count, cohort composition, and ID digest only. It never reads the raw-table/cohort fingerprints written in registration §2. `plan_input_digest` at `:1219`–`1233` computes those values; printing them is not an automated comparison against the ratified document. The probe changes a raw SHA and cohort TSV while keeping filenames fixed: supplementary registration still succeeds, ID digest remains equal, and the raw-table/cohort digests change. This is expected separation of responsibilities, not a claimed new integrity bug.

A filled document plus a generic “preflight PASS” therefore is insufficient evidence by itself. The final evidence needs the actual matching digests and successful registered-set resolution. If only the planned data/registration are added, a narrow final input-receipt check is sufficient; no reason was found in this scope to repeat a broad code review. Since real r3 artifacts are absent here, this review cannot perform or pre-approve that receipt check. Any new code changes or unexplained r2/r3 differences expand that final check.

## Limits

No solver, physical simulation, worker, or production batch was run. Preflight's generation solver was replaced with a declared passing fixture solely to isolate the registration/observation branch. `--allow-missing-raw` permitted synthetic fixture raw-file absence; all other real static preflight code ran. These `stop=[]` results are not end-to-end launch approval. Reread detail fixtures were handcrafted structural records, not claimed successful network publications. Audit CLI and release gates were not independently rerun in this subreview. Parent review owns provided selftests and release review.
