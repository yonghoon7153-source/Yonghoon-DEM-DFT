"""S1-O own static text/Decimal/JSON artifact builder; never imports received code.
This program writes design documents only. No synthetic validation or native calls.
"""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
S0 = ROOT / "reference/s0"
for directory in (ROOT / "contracts", ROOT / "notes", ROOT / "analysis"):
    directory.mkdir(exist_ok=True)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write_json(name, obj):
    path = ROOT / name
    if path.exists():
        raise RuntimeError("NO_OVERWRITE:" + name)
    path.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

old = (S0 / "sources/Normal480Candidate.java.txt").read_bytes()
candidate = (S0 / "candidate/MicroshortS1RestCandidate.java.inactive.txt").read_bytes()
sparse_tokens = (S0 / "candidate/REQUESTED_TIMES_S1_3600.txt").read_text(encoding="utf-8").split()
old_lists = re.findall(r'm\.study\("std1"\)\.feature\("time"\)\.set\("tlist","([^"]+)"\)', old.decode("utf-8"))
if len(old_lists) != 1:
    raise RuntimeError("STATIC_SOURCE_TLIST_COUNT")
dense_tokens = [t for t in old_lists[0].split() if Decimal(t) <= Decimal(120)]
prefix_tokens = [t for t in sparse_tokens if Decimal(t) <= Decimal(120)]
if (len(dense_tokens), len(prefix_tokens), len(sparse_tokens)) != (1337, 255, 401):
    raise RuntimeError("STATIC_REQUEST_COUNT")
if not set(map(Decimal, prefix_tokens)) <= set(map(Decimal, dense_tokens)):
    raise RuntimeError("STATIC_SPARSE_NOT_SUBSET")
for seq in (dense_tokens, prefix_tokens, sparse_tokens):
    if any(Decimal(a) >= Decimal(b) for a, b in zip(seq, seq[1:])):
        raise RuntimeError("STATIC_REQUEST_ORDER")

CAP_OLD = "if(t<0.1[s],0.000125[s],0.1[s])"
CAP_NEW = "if(t<0.1[s],0.000125[s],if(t<5[s],0.1[s],if(t<30[s],0.5[s],if(t<300[s],5[s],30[s]))))"
CAP_HALF = "if(t<0.1[s],0.0000625[s],if(t<5[s],0.05[s],if(t<30[s],0.25[s],if(t<300[s],2.5[s],15[s]))))"
common = {
    "fresh": True, "window_s": ["0", "120"], "sigma_S_m": "1.7e-6",
    "i_app_A_m2": "0", "initialization_contract": "INITIALIZATION.json",
    "initial_composition": {"xN": "0.445", "xP": "derived_from_fixed_inventory_not_independent_literal", "ce_mol_m3": "1200"},
    "rtol_Time": "1e-6", "study_rtol_string": "1e-5",
    "initialstepbdf_s": "1e-5", "maxstepconstraintbdf": "expr", "maxstepbdf_inactive_slot_s": "0.1",
    "tstepsbdf": "strict", "tstepsstore": 1, "eventout": "on", "stop_storage": "stepbefore_stepafter",
    "physical_elements_N_sep_P": [120, 60, 120], "particle_N_P": [320, 320],
    "full_dependent_fields": "UNCHANGED_FROM_S0", "profile_coordinates_per_electrode": 241,
    "compile_max": 1, "batch_max": 1, "runAll_max": 1, "retry_max": 0,
    "activation": "INACTIVE_DESIGN_ONLY", "approved": False, "usable": False,
}
variants = []
for ident, request_key, tout, cap, axis in [
    ("P0", "dense_0_120", "tsteps", CAP_OLD, "fresh_high_sigma_reference"),
    ("P1", "dense_0_120", "tlist", CAP_OLD, "storage_only_vs_P0"),
    ("P2", "sparse_0_120", "tlist", CAP_OLD, "requested_times_only_vs_P1"),
    ("P3", "sparse_0_120", "tlist", CAP_NEW, "cap_only_vs_P2"),
]:
    variants.append({"variant_id": ident, "request_vector": request_key, "tout": tout,
                     "maxstepexpressionbdf": cap, "changed_axis": axis, "shared": common})

policy = {
    "kind": "S1O_P0_P3_POLICY_CONTRACT", "status": "OFFLINE_PROPOSED_NOT_TESTED",
    "approved": False, "usable": False, "native_ready": False,
    "source_sha256": digest(candidate), "source_path": "reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt",
    "priority": "S0_REPORT_and_DECISION_final_definition_over_agent_note_alternatives",
    "request_vectors": {
        "dense_0_120": {"count": 1337, "tokens_s": dense_tokens, "source": "reference/s0/sources/Normal480Candidate.java.txt:tlist prefix <=120"},
        "sparse_0_120": {"count": 255, "tokens_s": prefix_tokens, "source": "reference/s0/candidate/REQUESTED_TIMES_S1_3600.txt:prefix <=120"},
        "sparse_0_3600": {"count": 401, "tokens_s": sparse_tokens, "source": "reference/s0/candidate/REQUESTED_TIMES_S1_3600.txt"}},
    "variants": variants,
    "literal_patch_table_from_S0": [
        {"target": "T_END_SECONDS", "source": "3600.0", "all_P": "120.0"},
        {"target": "SIGMA_S1_S_M", "source": "1.7e-7", "all_P": "1.7e-6"},
        {"target": "study std1/time tlist", "source": "sparse_0_3600", "replacement": "variant.request_vector exact token string"},
        {"target": "Time.tout", "source": "tlist", "replacement": "variant.tout"},
        {"target": "MAXSTEP_S1", "source": CAP_NEW, "replacement": "variant.maxstepexpressionbdf"},
        {"target": "run/output/purpose identifiers and logger claimed settings", "replacement": "must follow variant_id and be listed in future source diff; no physical replacement"}],
    "comparisons": [{"reference": a, "candidate": b, "only_changed_axis": axis,
                     "expected_common_request_vector": "sparse_0_120", "expected_count": 255}
                    for a, b, axis in [("P0", "P1", "storage"), ("P1", "P2", "requests"), ("P2", "P3", "cap")]],
    "consumer_contract": {
        "inputs": ["run/source/settings/native completion/evidence/ownership/resource records for both runs", "boundary1/4 scalar tables", "N/P profile tables", "Li and guard tables", "native accepted-step time list", "stored time list", "units and coordinate/domain contracts"],
        "outputs": ["each native_completion", "each evidence_validity", "comparison_coverage", "policy_comparison", "axis_scope", "request_missing/duplicates", "actual_intersection", "actual_compared_times", "max_values_and_locations", "budget_and_cleanup"],
        "own_requests_required": "P0/P1 each1337 and P2/P3 each255 before normal120 completion; full255 comparison plus each own request coverage",
        "time_interpolation": "FORBIDDEN; tlist/strict readback alone is not proof; exact requested times must appear as accepted-step endpoints or mark interpolation evidence OPEN",
        "stored_count": "NOT_FIXED; P0 all accepted, P1-3 requested plus permitted event/guard states retained separately",
        "profile_grid": {"N": {"count": 241, "domain": 1, "coordinate_um": ["0", "52"]}, "P": {"count": 241, "domain": 3, "coordinate_um": ["77", "121"]}, "comparison": "same exact input coordinate identifiers; not nearest-neighbor"},
        "limits": {"max_abs_delta_terminal_V": "0.001", "max_abs_delta_surface_x": "0.0001", "each_total_Li_relative_drift": "0.000001", "pair_total_Li_relative_difference_to_initial_inventory": "0.000001", "each_voltage_identity_residual_V": "1e-8"},
        "nonbinding_weak_signal_diagnostic": {"max_deltaV_design_goal_V": "1e-5", "endpoint_drift_discrepancy_design_goal_V": "1e-5", "effect": "miss does not change compatibility limit; weak-signal inference remains INCONCLUSIVE unless K supports it"},
        "stop_result": "guard termination/fatal/missing/invalid/numeric incompatibility halts next policy run; do not relabel normal120 complete; no retry",
        "native_success_not_comparison_pass": True,
        "no_empty_t0_only_pass": True,
    },
    "P_max_run_count": 4, "actual_executed": 0,
    "late_cap_gap": {"P_validated_window_s": ["0", "120"], "after_300_s": "UNQUALIFIED_BY_P", "closure": "K_CAP matched baseline and half-cap nearzero/high full0-3600 below, distinct M/N approvals; no hidden P4 or optional +2 run", "late_slope_window_s": ["2700", "3600"], "short_late_window_can_substitute": False},
    "implementation_scope": "JSON describes exact variants; source materialization/adapter completion still requires declared source diff, validation and separate native approval. No Java API compatibility claimed."
}
write_json("contracts/POLICY_VARIANTS.json", policy)

sigmas = [("Z", "1e-20"), ("L", "1.7e-8"), ("M", "1.7e-7"), ("H", "1.7e-6")]
axes = [
    {"axis_id": "RTOL", "only_change": "Time.rtol", "baseline": "1e-6", "candidate": "1e-7", "must_not_change": ["Study rtol string", "scaled/factor", "initialstep", "cap", "mesh", "storage"]},
    {"axis_id": "CAP", "only_change": "Time.maxstepexpressionbdf", "baseline": CAP_NEW, "candidate": CAP_HALF, "must_not_change": ["rtol", "initialstep", "mesh", "requests", "storage"]},
    {"axis_id": "PARTICLE", "only_change": "pce1/pin1.Nel and pce2/pin1.Nel", "baseline": [320, 320], "candidate": [640, 640], "must_not_change": ["physical mesh", "rtol", "cap", "requests", "storage"]},
    {"axis_id": "PHYSICAL", "only_change": "mesh1/edg1/dis1..3.numelem", "baseline": [120, 60, 120], "candidate": [240, 120, 240], "must_not_change": ["particle mesh", "rtol", "cap", "requests", "storage"]},
]
budgets = {"status": "UNAPPROVED_PLANNING_CEILING_REQUIRES_PILOT_COST_AND_RESOURCE_REVIEW", "preflight_s": 300, "compile_batch_s": 7200, "owned_cleanup_s": 120, "analysis_s": 600, "preservation_s": 180, "local_delivery_s": 600, "overall_s": 9000, "output_growth_GiB_proposed": 6, "start_disk_free_GiB_proposed": 16, "resource_binding": "RESOURCE_CONTRACT.json; S0 numbers do not override future stricter contract or measured cumulative reservation"}
runs = []
for code, sigma in sigmas:
    runs.append({"run_id": "M_BASE_" + code, "phase": "M", "axis": "BASE", "sigma_S_m": sigma, "fresh_window_s": ["0", "3600"], "request_count": 401, "budget": budgets, "reuse": "same one baseline used by all four axes; no extra baseline solves"})
for axis in axes:
    for code, sigma in sigmas:
        runs.append({"run_id": "N_" + axis["axis_id"] + "_" + code, "phase": "N", "axis": axis["axis_id"], "sigma_S_m": sigma, "fresh_window_s": ["0", "3600"], "request_count": 401, "budget": budgets})
pairs = []
for axis in axes:
    for code, sigma in sigmas[1:]:
        pairs.append({"finite_sigma_S_m": sigma, "axis": axis["axis_id"], "base_pair": ["M_BASE_Z", "M_BASE_" + code], "control_pair": ["N_" + axis["axis_id"] + "_Z", "N_" + axis["axis_id"] + "_" + code]})
K = {
    "kind": "S1O_PREREGISTERED_MATCHED_NUMERICAL_CONTROL_DESIGN", "approved": False, "usable": False, "native_ready": False,
    "freeze_rule": "Freeze exact axis choices/values/sigmas/windows/interpretation and dedup keys after P cost review but before viewing any M ladder result. This full four-axis draft is recommended; no result-dependent selection of favorable sigma or axis.",
    "baseline": {"policy_variant": "P3 extended only to3600 via exact sparse_0_3600", "rtol": "1e-6", "cap": CAP_NEW, "physical_N_sep_P": [120, 60, 120], "particle_N_P": [320, 320], "initialstep_s": "1e-5", "tout": "tlist", "strict": True, "requested_count": 401},
    "axes": axes, "sigmas_S_m": [s for _, s in sigmas], "run_inventory": runs, "matched_pairs": pairs,
    "run_counts": {"policy_P": 4, "main_M_base": 4, "controls_N": 16, "unique_full3600": 20, "total_P_M_N": 24, "all_proposed_not_approved": True, "maximum_COMSOL_solves_per_run": 1, "maximum_compile_per_run": 1, "maximum_batch_per_run": 1, "automatic_retry": 0},
    "sequence": [
        {"step": 1, "runs": ["P0", "P1", "P2", "P3"], "pause": "each policy result accepted before next; P only120s"},
        {"step": 2, "action": "review pilot measured cost, close resource/API blockers, freeze K/source variants/counts/budgets before M, separate approvals"},
        {"step": 3, "runs": ["M_BASE_Z", "M_BASE_H", "N_CAP_Z", "N_CAP_H"], "pause": "review full3600 same-sigma cap and late2700-3600 evidence before remaining ladder; these four already counted in M4/N16, not extraP"},
        {"step": 4, "runs": ["M_BASE_L", "M_BASE_M"], "pause": "separate per-run approval; do not tune sigma based on high result"},
        {"step": 5, "runs": [r["run_id"] for r in runs if r["run_id"].startswith("N_") and r["run_id"] not in ["N_CAP_Z", "N_CAP_H"]], "pause": "same pre-frozen twelve remaining non-CAP and two low/midCAP controls; bounded individually"}
    ],
    "dedup_key": ["sigma", "initialization/source and material/physics hashes", "axis settings", "request list and storage", "time window", "required output/evidence schema", "engines/policy/resource contract"],
    "dedup_rule": "M_BASE_Z shared by all3finite and4axes; each N_AXIS_Z shared by3finite only within same axis. P3_120 cannot replace M_BASE_H_3600. Previous NORMAL480/rtol30/B-min have different initial/protocol and cannot be K baselines. A run is reused only if complete key identical and required data complete.",
    "observation": {
        "terminal_voltage_V": "phis_boundary4 - phis_boundary1",
        "D_sigma_V": "(V_Z(t)-V_Z(0))-(V_sigma(t)-V_sigma(0)); positive is extra finite-sigma terminal voltage drop",
        "S_sigma_V_per_h": "(D_sigma(3600)-D_sigma(2700))*3600/900",
        "E_D_V": "max_axis abs(D_axis(3600)-D_BASE(3600)) using matching Z at each axis",
        "E_S_V_per_h": "max_axis abs(S_axis-S_BASE) using matching Z at each axis",
        "delta_D_V": "0.001", "delta_S_V_per_h": "0.001", "multiplier": 5,
        "classification": {"DISTINGUISHABLE_AT_REST": "valid+Kcomplete+resolved_current_inventory_signs; D>max(deltaD,5ED) AND S>max(deltaS,5ES)", "NOT_DISTINGUISHABLE_WITHIN_T": "valid+Kcomplete; abs(D)<=deltaD AND abs(S)<=deltaS AND 5ED<=deltaD AND 5ES<=deltaS; unresolved nearzero sign recorded not strict-positive failure", "INCONCLUSIVE": "all other cases; no change of thresholds after seeing outputs"},
        "meaning": "observed sensitivity over this registered K, not rigorous discretization-error bound or experimental detectability; no full-convergence PASS"
    },
    "late_cap_evidence": {"required_windows_s": [["300", "3600"], ["2700", "3600"]], "record": ["accepted-step sequence", "actual dt min/max/count by0-.1/.1-5/5-30/30-300/300-2700/2700-3600", "rejected step/Tfail/NLfail with log definitions", "cap readback for baseline and control", "stored and requested times independently"], "inactive_cap": "If actual dt never reaches restrictive half-cap, report cap non-binding/limited exercise; matching settings alone does not prove stronger integration. Retain observed D/S difference but leave blanket late-cap qualification OPEN unless independent time-resolution evidence supports it.", "no_short_substitute": True},
    "cost_reduction": {"before_M_only": "drop an axis or sigma control only by explicit revised fixed scope, same-sigma Z retained; record exactly missing K; no silently filled ED/ES=0", "after_M": "budget stop/abandon preserves existing data; full registered classification remains INCONCLUSIVE for incomplete affected sigma", "minimum_lean_example": {"runs": ["M_BASE_Z", "M_BASE_H", "N_CAP_Z", "N_CAP_H"], "new_total_including_P": 8, "what_can_be_said": "high sigma cap-only contrast over3600", "what_remains": "all three final ladder classifications under four-axisK INCONCLUSIVE; weak/mid and rtol/space untested"}},
    "nominal_ceiling_arithmetic": {"P4_plus_M4_N16_at9000_s": 216000, "hours": 60, "20_full3600_at9000_s": 180000, "not_a_blanket_approval_or_forecast": True},
    "status": "DRAFT_FIXED_COUNTS_AND_AXES__PILOT_COST_AND_USER_SCOPE_DECISION_PENDING"
}
write_json("contracts/K_DESIGN.json", K)

bytes_per_state = (Decimal(7315279360) - Decimal(4261090658)) / (Decimal(5740) - Decimal(3340))
intercept = Decimal(4261090658) - bytes_per_state * Decimal(3340)
cost = {
    "kind": "S1O_PILOT_COST_OBSERVATION_AND_REBUDGET_DESIGN", "approved": False, "native_ready": False,
    "historical_record_scope": "source-ledger quoted observations, not new measurements; charging nearzero olddense differs from finite-sigma rest",
    "historical": [
        {"run": "NORMAL120", "compile_batch_s": "2650.203", "overall_s": "2794.536", "stored_states": 2140, "mph_bytes": 2734001003},
        {"run": "NORMAL240", "compile_batch_s": "4059.516", "overall_s": "4269.865", "stored_states": 3340, "mph_bytes": 4261090658},
        {"run": "NORMAL480", "compile_batch_s": "6500.453", "overall_s": "6829.015", "solver_s": "2457", "stored_states": 5740, "mph_bytes": 7315279360},
        {"run": "BMIN150_particle640", "overall_s": "4471.8936425", "stored_states": 2447, "mph_bytes": 6162301981}],
    "historical_evidence": "reference/s0/notes/COST_AND_DESIGN.md:16-29 and source SPEC lines cited there",
    "separate_clocks": ["compile wall", "batch wall", "initialization wall if observable", "Time solver wall from labeled native log", "post-solve save/export wall when instrumented otherwise residual unclassified", "analysis wall", "packaging wall", "parent total"],
    "never_add_nested_clocks": True,
    "pilot_records": ["variant/settings/source identity", "actual core request and separately observed process CPU", "fresh/consistent initialization outcome", "accepted step count and dt distribution by capsegment", "Tfail/NLfail rejected records separately", "native wall and CPU where available", "stored/requested/full-field counts", "MPH size and all output footprint", "CSV/stdout/base64 bytes", "sampled working-set and private commit maxima", "OS process/job peak counter availability and aggregation scope", "available physical/commit/disk minima", "postprocessor and package wall/size", "monitor/drop/sample gaps and resource stop outcome"],
    "sampled_peak_caveat": "sampled_max != OS peak != enforced hard cap; counters absent/unreadable give UNKNOWN and no resource-sufficiency PASS",
    "proposed_per_run_limits": budgets,
    "rebudget_formula": {
        "calibration": "from P record per-phase C_compile,C_init,c_step (native step/solver record), c_store (save/export residual only if separated), c_analysis,c_pack; if phases cannot separate leave them unresolved instead of fake fit",
        "n_step_scenario": "use accepted counts by capsegment, strict requests, initial transients; S0 cap integral lower bound1063 is lower bound only, not forecast; use1x/3x/10x work factors as sensitivity scenarios, not probability intervals",
        "native_scenario_s": "C_compile + C_init + f_step*c_step*N_est + c_store*S_est + C_batch_other ; no double counting nested solver/batch times",
        "candidate_native_limit_s": "ceil(1.5*max(validated_applicable_scenarios_native) + 300) rounded up to60s; compare with explicit7200 proposal and seek revised approval if greater; neverautoextend",
        "candidate_overall_limit_s": "approved_native + separately budgeted preflight/cleanup/analysis/preservation/delivery with final-record margin; each phase budget remains independently binding",
        "analysis_pack": "scale measured bytes/rows throughput with2x margin andfixedstartup, separately from native; absentmeasurement OPEN",
        "disk": "planned persistent previous outputs + worst candidate MPH/CSV/stdout/raw/fullbase64 + temporary and package coexistence + cleanup/log reserve; require free>=sum_reserved+margin before newrun; no deletion of oldMPH to fit",
        "RAM_commit": "use sameconfigurationpilot measuredcounter scope and conservative margin; extrapolating mesh640/600 or sigma/late regime remains UNKNOWN; if safeheadroom cannot be defended no nativeGO",
        "recalibration": "after first complete full3600 high/Z pair, update only future cost approvals, not Kselection/physics thresholds; if cap active or NLfail changes treat mappinguncertain"
    },
    "storage_scenario": {"normal240_480_incremental_bytes_per_state": str(bytes_per_state), "intercept_bytes": str(intercept), "401_state_MPH_bytes_scenario": str(intercept + bytes_per_state * Decimal(401)), "particle640_401_state_scenario_bytes": str(Decimal(6162301981) / Decimal(2447) * Decimal(401)), "same_fields_encoding_assumption": True, "not_RAM_or_disk_cap_or_completion_guarantee": True, "all401profiles_rows": 401*241*2},
    "ocv_predictions": [
        {"sigma_S_m": "1.7e-8", "one_hour_equilibrium_mean_composition_OCV_drop_mV": "0.096248"},
        {"sigma_S_m": "1.7e-7", "one_hour_equilibrium_mean_composition_OCV_drop_mV": "0.962366"},
        {"sigma_S_m": "1.7e-6", "one_hour_equilibrium_mean_composition_OCV_drop_mV": "9.503694"}],
    "prediction_comparison": {"mean_OCV": "same fixed OCP functions at electrode particle-volume/length-weighted averagex: U_P(xavgP,T)-U_N(xavgN,T); not arithmetic meanofsurfaceextrema orterminalV", "columns": ["S0 analytic OCVdrop", "computed mean-composition OCVdrop", "terminal selfdrop", "paired terminalD", "initial terminal offset", "late S and K ED/ES", "reaction/diffusion/nonuniformity interpretation unresolved"], "forbidden": "no sigma/OCP/initialstate retuning to hitprediction; disagreement is evidence, notautomaticretry; no empirical R-to-sigma inversion"},
    "three_unjudgeable_paths": [
        {"path": "same tlist name but interpolated/missing accepted times or discarded guard state", "blocker": "exact requested/stored/native-step evidence and perrun ownrequests coverage, noempty/t0 PASS"},
        {"path": "finiteσ CDI changes inventory or initial potential jump counted as self-discharge", "blocker": "threephase initialization and sameinitialinventory limits; retain algebraic potentialoffset and use paired increments"},
        {"path": "P120 accepted then claim late2700-3600 or weakσ resolution without matchedZ control", "blocker": "fixed20run K with same-axisZ and full3600cap; missingcoverage=>INCONCLUSIVE, noEDzero default"}],
    "limits_of_budget": "P/M/N caps are unapproved proposals; fullK nominal60h wall+outputs substantial. User may stop afterP, or approve reducedregisteredquestion with INCONCLUSIVE residual, notautomaticexecution."
}
write_json("contracts/COST_MODEL.json", cost)

summary = {
    "kind": "OWN_STATIC_ARITHMETIC_AND_SOURCE_TOKEN_EXTRACTION_ONLY",
    "candidate_sha256": digest(candidate), "normal480_source_sha256": digest(old),
    "request_counts": {"dense120": len(dense_tokens), "sparse120": len(prefix_tokens), "sparse3600": len(sparse_tokens)},
    "prefix_is_subset": True, "request_monotonic_unique": True,
    "proposed_unique_runs": {"P": 4, "M": 4, "N": 16, "total": 24},
    "proposed_max_wall_9000_each_s": 24*9000,
    "candidate_import_execution": 0, "synthetic_tests": 0, "COMSOL": 0, "JVM": 0,
    "created": [{"path": n, "bytes": (ROOT/n).stat().st_size, "sha256": digest((ROOT/n).read_bytes())} for n in ["contracts/POLICY_VARIANTS.json", "contracts/K_DESIGN.json", "contracts/COST_MODEL.json"]],
    "prior_static_read_diagnostic": "tool329cd5 rg exited1 because contracts directory didnotyetexist; read-only discovery, no candidate/test/native execution"
}
write_json("analysis/POLICY_DESIGN_STATIC_OUTPUT.json", summary)
print(json.dumps(summary, ensure_ascii=False))
