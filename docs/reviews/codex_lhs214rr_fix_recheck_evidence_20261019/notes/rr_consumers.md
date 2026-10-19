# R01 / R04 consumer-chain independent review

Scope: pinned source `77d8fd44545c33cd10ab18fc250c7ad3023833ea`, immutable snapshot supplied by parent. Read `source/AGENTS.md`, submitted request, and 10-17 report before work. No source edits, Git actions, production DEM/214 or WSL runs. Small synthetic resistor fixtures only. Outputs below are under `evidence/rr_consumers/`; all new probe files have prefix `probes/rr_consumers`.

## Conclusion

R01 old H0 resurrection is closed at the real record/stop/reread/load gates. R01 submitted real-chain section passes all nine L0/L1/L2 × H0/Physics/H12 mutants, including actual fresh builds, generation gate, batch gate, and isolated source reread. R04 is closed for numeric ionic FULL/CF/constriction branches; an additional four independent full-consumer mutants reject through both publication candidate paths, record/stop, reread, actual `load_tau_results`, fresh build and actual release checker batch gate. No new production-code defect found in this consumer scope.

Do not state that submitted R01 is 27/27 on this Windows environment. Unchanged test yields 23/26, rc1, because its hard-coded 21-node exact-ULP boundary fixture solves on this platform below the intended threshold and raises `KeyError: q_withheld`; details below. Numeric agent owns the independent strict-boundary adjudication.

## Source path and exact lines

- Producer uses `G_eff * T_um / A_um2` (`network_conductivity.py:1435`); FULL strict `> FULL_Q_GUARD_MAX` at `:1471`; CF/constriction strict literal `> 1.5` labels at `:1478`; thermal follows its own parallel-bound branch at `:1469`.
- Published ionic certificate reconstructs q with matching division/multiplication order, using `_geometry_TA`: `tau_flux.py:796`; R01 strict guard `:807`; R04 expected tuple from reconstructed q `:817`–`:823`. It does not rely on `q_withheld`, rounding, or stored q for the policy comparison.
- `certificate_binding_problems` dispatches all three ionic branches `tau_flux.py:1007`–`:1023`; technical-invalid input is rejected separately by consumers, not certified by an empty binding-problem list.
- Per-mode binding becomes whole-record generation invalid: `tau_flux.py:1101`–`:1103`, `:1119`; all present mode τ values become NOT_COMPUTED through `:1332`, `:1368`–`:1372`.
- Actual candidate checks use stop for network-stop path `webapp/app.py:3713` and record check in both paths `:3723`–`:3730`. `pipeline_service.py:1215` runs generation contract for dual, legacy+physics and mode-file copies; stop ⑨ calls shared contract `:1133`.
- `g2_network_reread.py:492`–`:503`: K2 shared generation/certificate contract, K4 original stop. `lhs_design_dataset.py:2080`–`:2082`: P4 generation rejection; `:2099`–`:2103`: original stop recheck.
- Fresh `build_v13`: generation gate `lhs_release_build.py:2261`, original source reread `:2297`; batch gate `:1545`/`:1573`. Existing `check_v13` reuses batch-gate checker at `:2576`; it does not freshly reread source.

## Original probes and fresh baseline

`rr_consumers_run.py chain` executes original 10-15 probe bytes SHA256 `804de03d58902862f74006afaf1e24dfed97a42a254d02b86a4cc98797de243a`, changing only evidence/temp assignment and rebinding `__file__` to the new review. The five producer fixtures are freshly generated. Original helper SHA and exact path substitutions are retained in JSON; old evidence was not reused as producer output or overwritten.

- All five cases publish `done`; all K1–K7 checks pass.
- H0 model-limit cases at L0/L1/L2 retain primary-target HOLD. ml_physics and ml_el do not gain that H0 HOLD.
- Compared with the 10-17 original result, after normalizing actual run IDs and review/evidence paths, the only difference is `handover.report.tau_flux_sha256` (expected code change). No numerical/verdict normalization was applied.
- Actual `load_tau_results` and `build_handover` run on all five fresh cases.
- Fresh unmutated ml_physics selected row passes actual build with `dry_run=False`, `diagnostic=False`: 27 files, `warnings=[]`, `tau_reread=performed`; actual `check_v13=[]`. Selected H0 f=0.79535562, τ²=5.52989078649587, τ=2.351571981993294. This verifies a normal H0 numerical target coexists with legitimate diagnostic over-conduction and withheld Physics.
- Limits: one selected genuine producer row; remaining 213 rows and audit/batch records are submitted synthetic release fixtures. Original 52-column comparison function runs unchanged and selected row uses original `load_tau_results` anew per build. Not a real 214-run approval.

Evidence: `chain_provenance.json`, `consumers_probe.json`, `consumers_handover_rows.json`, `baseline.json`, `summary.json`, retained fixture/release folders.

## R01 exact old resurrection capture

`rr_consumers_run.py resurrection` executes old 10-17 `consumer_h0_resurrection.py` bytes unchanged. Only imported helper source/evidence/temp paths are rebound. Wrapper catches its now-expected early refusal and saves the live report; no verdict expression or mutant changed.

- Raw q=1.6231747351909995, numerical certificate unchanged=True, old 10-leaf resurrection and consistent copies/projection.
- Content=True is still expected: channel/content is not a complete numerical acceptance gate. Record=False; stop=False (⑦ and ⑨); τ generation invalid and all three τ values blank.
- Actual `load_tau_results` raises `FillRefusal` at P4 with raw q, strict threshold, policy `full_single_phase_q_gt_1p5/v1` and R01 reason.
- Independent post-refusal `reread_case` fails K2, K3, K4, K5, K6; K1 still passes published identity.
- Original probe stops before handover/build because it assumed load acceptance. Output does not exist; do not misdescribe this particular run as an independently completed build rejection. Submitted B section provides actual nine build rejections.

Evidence: `resurrection_capture.json`, retained original helper working directory and `run.log`.

## R04 independent additional mutants

`rr_consumers_independent.py` mutates fresh baseline source only, then restores scratch source/gate byte-for-byte in `finally`. All numbers remain unchanged. Four variants:

1. H0 CF q=3.926990816987246, model_over_conduction→computed with both status/reason tuples.
2. Physics constriction-only q=7.6373127569770105, same label reversal.
3. H12 CF q=3.599741582238307, only branch+certificate reason changed to None.
4. H0 FULL q=0.7953556202435896, only branch+certificate reason changed to q_gt_1p5.

All four: content=True; record=False; stop=False; actual `_network_projection` + `_network_candidate_checks` general path rejects at record gate and stop path rejects at stop gate; all three τ mode values blank; P4 refuses with R04 reason. Fresh build with unchanged old passing gate is refused by real source reread. Fresh build with actual failing reread detail is refused by batch gate (K2 present). No output folders created. Restoration leaves original check `[]`.

`rr_consumers_check_gate.py` separately installs actual H0-CF failing reread details and calls actual `check_v13`: it detects changed gate SHA and K2–K6 failure details, then returns `[]` after exact gate restoration. When original gate/handovers/release are unchanged but current source alone is changed, existing `check_v13=[]`, as explicitly documented in prior review. That is unchanged scope, not a fresh-source certification.

Evidence: `independent_r04.json`, `independent_r04_stdout.log`, `actual_gate_check.json`, `summary.json`.

## Submitted tests and boundary limitation

Both submitted test files were read before execution and executed unchanged with isolated TEMP, UTF-8, no bytecode and four numerical thread-count variables set to 1. These overlapped numeric agent once due to message timing; no further duplicate unchanged suites were run.

- R04: rc0, 12/12. Original 12 beds × three modes accepted; 51 + 21 label flips and all reason mutants reject. CF/constriction boundary tests pass, including q=1.5 and nextafter(1.5,+∞).
- R01: rc1, 23/26 (not 27/27). R, C and B all pass, including all nine consumer/build variants. E1 gets raw next/eq/prev `1.4999999999999962`, `1.4999999999999958`, `1.4999999999999956`, so E3 gets computed instead of withheld and E4 setup raises KeyError. Later E5 is skipped by that section exception. This is a nonportable fixture expectation, not evidence that the guard misclassified the q actually solved. Coordinate numeric agent's independent boundary proof before final closure wording.

Evidence: `submitted_suites.json`, `test_l214r_r01_restored_full.py.log`, `test_l214r_r04_cf_label.py.log`.

## Policy answers / limitations

Whole-record rejection for R04 is consistent with the already-approved atomic generation/certificate contract: a producer-inconsistent label means that assembled run cannot be treated as valid. It is intentionally conservative: an unrelated mathematically valid H0 number is blanked with the contradictory run. It is not a new physical q cap on CF/constriction values; original correctly labeled over-conduction values remain accepted. Thus P3 interpretation-label defect severity and whole-record integrity rejection are not contradictory.

No consumer evidence requires expanding this ionic τ review to electronic FULL or electronic/thermal CF label policies. Those are outside the selected consumer and thermal follows a different branch policy. Carry them as explicit separate-scope limitations; do not state that all channels' publication labels/numbers have now been certified. Normal-case evidence supports the tested cases, not every possible input.

The code correction does not ratify registration, reseal fingerprints, approve B7 pins, authorize a fresh ROOT/214 run, or clear independent S3 HOLD.
