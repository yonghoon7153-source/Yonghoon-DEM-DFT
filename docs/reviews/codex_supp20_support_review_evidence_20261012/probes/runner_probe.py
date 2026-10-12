"""Read-only runner review: isolated registration, preflight, and detail contracts.

No solver, worker, simulation, or production batch is run. Only the generation
probe is replaced in preflight, because that probe would run a small solver.
All fixtures are under a disposable temporary directory outside source/.
"""
from pathlib import Path
import ast
import copy
import hashlib
import json
import os
import sys
import tempfile
from unittest.mock import patch

REVIEW = Path(__file__).resolve().parents[1]
SOURCE = REVIEW / "source"
WORKSPACE = REVIEW.parent
for path in (WORKSPACE / "lhs_coverage_review_20260930/deps",
             WORKSPACE / "gen2_network_reverify3_20261007/deps",
             SOURCE / "webapp", SOURCE / "scripts"):
    sys.path.insert(0, str(path))
sys.dont_write_bytecode = True
import run_network_194_parallel as runner
import g2_network_reread as reread


def caught(fn):
    try:
        value = fn()
        return {"error": None, "value": value}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


def followups(plan, root):
    lines = []
    man = {"plan": plan, "git": {"sha": "a" * 40, "short": "a" * 9},
           "code_hashes": runner.code_hashes(), runner.GEN_KEY: "g2"}
    runner.print_followups(root, man, out=lambda *a, **k: lines.append(" ".join(map(str, a))))
    return next(line for line in lines if line.startswith("python3 scripts/g2_network_reread.py"))


def detail_record(pairs):
    pairs = sorted(pairs)
    summary = {"expected_n": len(pairs), "read_n": len(pairs), "set_equal": True,
               "missing": [], "extra": []}
    meta = [{"name": k, "ok": True} for k in reread.LAUNCHER_META_IDS]
    meta += [{"name": f"{k} {cohort}", "ok": True}
             for cohort in sorted({h for c, h in pairs}) for k in reread.LAUNCHER_COHORT_META_IDS]
    next(m for m in meta if m["name"] == "M3").update(summary)
    return dict(expected_set="supp20", n_fail=0, meta=meta, **summary,
                cases=[dict(case=c, cohort=h, checks=[dict(name=k, ok=True) for k in reread.CASE_CHECK_IDS])
                       for c, h in pairs])


def function_ast(path, names):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {n.name: ast.dump(n, include_attributes=False) for n in tree.body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in names}


def main():
    report = {"pin": "b429c3c1df0956d2721861d89cc29a2d56f2b581",
              "limits": ["Temporary synthetic harvest names and digest fields only; no physical values tested.",
                         "Preflight generation solver replaced with a declared passing fixture; no complete launch validation claimed.",
                         "Detail records are handcrafted contract fixtures, not published network evidence.",
                         "No audit CLI or solver runs; observation audit conclusion follows its shared predicate."]}
    args = runner._parse(["run", "--root", str(REVIEW / "tmp" / "never_started")])
    actual = runner.build_plan(args.cohorts.split(","), runner.cohort_specs(args))
    p194 = runner.registered_id_set("production194")
    ids = [f"lhss_{i:03d}" for i in range(1, 21)]
    pairs = frozenset((case, "lhss") for case in ids)
    report["actual_checkout"] = {
        "default_cohorts": args.cohorts, "default_queue_n": len(actual["queue"]),
        "default_registered_set": runner.registered_production_set(actual),
        "production194_ids_sha256": runner.ids_digest(p194["pairs"]),
        "production194_no_observation_problem": runner.production_observation_problem(dict(plan=actual, observe_imports=False)),
        "supp20_registered_lookup": caught(lambda: len(runner.registered_id_set("supp20")["pairs"])),
        "supp20_reread_expected": caught(lambda: len(reread.registered_expected("supp20")["pairs"])),
        "code_fp": runner.code_fp(runner.code_hashes()),
    }
    (REVIEW / "tmp").mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="runner_probe_", dir=REVIEW / "tmp") as td:
        tmp = Path(td)

        def harvest(name, case_ids):
            h = tmp / name
            h.mkdir()
            for case in case_ids:
                raw = {k: {"sha256": hashlib.sha256(f"{case}:{k}".encode()).hexdigest()}
                       for k in ("atom", "contact", "mesh", "deck")}
                (h / f"{case}.json").write_text(json.dumps({"raw": raw, "contact_scan": {"n_rows_last": 1}}), encoding="utf-8")
            (h / "_cohort.tsv").write_text("case\tatom_file\tcontact_file\tdeck\n", encoding="utf-8")
            return dict(runner.COHORT_SPECS["lhss"], harvest=str(h), cohort=str(h / "_cohort.tsv"))

        good_spec = harvest("good20", ids)
        custom_specs = dict(runner.COHORT_SPECS, lhss=good_spec)
        plan = runner.build_plan(["lhss"], custom_specs)
        gp = dict(generation="g2", g2_name="g2", error="", problems=[])
        args = runner._parse(["run", "--root", str(tmp / "no_launch"), "--cohorts", "lhss", "--dry-run",
                              "--lhss-harvest", good_spec["harvest"], "--lhss-cohort", good_spec["cohort"],
                              "--allow-missing-raw"])

        def inspect(plan_):
            with patch.object(runner, "derive_generation", return_value=gp):
                pf = runner.preflight(args, plan_, tmp / "no_launch", None)
            return {"queue_n": len(plan_["queue"]), "registered_set": runner.registered_production_set(plan_),
                    "observation_problem": runner.production_observation_problem(dict(plan=plan_, observe_imports=args.observe_imports)),
                    "preflight_stop": pf["stop"], "preflight_warn": pf["warn"],
                    "ids_sha256": pf["input_digest"]["ids_sha256"],
                    "reread_command": followups(plan_, tmp / "no_launch")}

        report["unavailable_registration_exact20_external_override"] = inspect(plan)
        report["registered_fixtures"] = {}
        with patch.object(runner, "COHORT_SPECS", custom_specs):
            report["registered_fixtures"]["exact20"] = inspect(plan)
            with patch.object(args, "observe_imports", True):
                report["registered_fixtures"]["exact20_observation_enabled"] = inspect(plan)
            for name, cases in {
                "missing19": ids[:-1], "extra21": ids + ["lhss_021"],
                "substituted20": ids[:-1] + ["lhss_099"],
                "thick_added21": ids + ["lhst_036_6m"],
                "thick_substituted20": ids[:-1] + ["lhst_036_6m"],
            }.items():
                spec = harvest(name, cases)
                bad_plan = runner.build_plan(["lhss"], dict(custom_specs, lhss=spec))
                row = inspect(bad_plan)
                with patch.object(runner, "COHORT_SPECS", dict(custom_specs, lhss=spec)):
                    row["bad_registration_lookup"] = caught(lambda: len(runner.registered_id_set("supp20")["pairs"]))
                report["registered_fixtures"][name] = row
            combined = dict(plan, cohorts=actual["cohorts"] + plan["cohorts"], queue=actual["queue"] + plan["queue"])
            report["registered_fixtures"]["combined214"] = {
                "registered_set": runner.registered_production_set(combined),
                "observation_problem": runner.production_observation_problem(dict(plan=combined, observe_imports=False))}
            duplicate = dict(plan, queue=plan["queue"] + [plan["queue"][0]])
            report["duplicate_queue"] = {"registered_set": runner.registered_production_set(duplicate),
                                          "plan_problems": runner.plan_problems(duplicate)}
            wrong_cohort = copy.deepcopy(plan)
            wrong_cohort["queue"][-1]["cohort"] = "lhs"
            report["wrong_cohort"] = {"registered_set": runner.registered_production_set(wrong_cohort),
                                      "plan_problems": runner.plan_problems(wrong_cohort)}
            before = runner.plan_input_digest(plan)
            raw_file = Path(good_spec["harvest"]) / "lhss_001.json"
            fixture = json.loads(raw_file.read_text(encoding="utf-8"))
            fixture["raw"]["atom"]["sha256"] = "0" * 64
            raw_file.write_text(json.dumps(fixture), encoding="utf-8")
            cohort_file = Path(good_spec["cohort"])
            cohort_file.write_text(cohort_file.read_text(encoding="utf-8") + "lhss_001\tchanged.atom\tchanged.contact\tchanged.deck\n", encoding="utf-8")
            after = runner.plan_input_digest(plan)
            report["registration_checks_ids_only"] = {
                "registered_set_after_raw_and_cohort_change": runner.registered_production_set(plan),
                "ids_sha_unchanged": before["ids_sha256"] == after["ids_sha256"],
                "raw_table_sha_changed": before["raw_sha256_table_sha256"] != after["raw_sha256_table_sha256"],
                "cohort_sha_changed": before["cohort_tsv_sha256"] != after["cohort_tsv_sha256"],
            }

        rec = detail_record(pairs)
        variants = {"positive": rec}
        x = copy.deepcopy(rec); x["cases"].pop(); variants["missing19_kept_summary20"] = x
        x = copy.deepcopy(rec); x["cases"][-1]["case"] = "lhss_099"; variants["substitution_same20"] = x
        x = copy.deepcopy(rec); x["cases"].append(copy.deepcopy(x["cases"][0])); variants["duplicate21"] = x
        x = copy.deepcopy(rec); x["cases"][-1]["case"] = "lhst_036_6m"; variants["thick_substitution20"] = x
        x = copy.deepcopy(rec); x["cases"][-1]["cohort"] = "lhs"; variants["wrong_cohort20"] = x
        x = copy.deepcopy(rec); x["cases"][0]["checks"][0]["ok"] = False; variants["false_check_summary0"] = x
        x = copy.deepcopy(rec); x["cases"][0]["checks"] = []; variants["empty_checks"] = x
        x = copy.deepcopy(rec); x["cases"][0]["checks"][0]["ok"] = 1; variants["integer_true"] = x
        report["detail_contract"] = {name: reread.launcher_detail_problems(value, pairs) for name, value in variants.items()}
        report["detail_contract"]["same20_wrong_expected194"] = reread.launcher_detail_problems(rec, p194["pairs"])

    baseline = REVIEW / "baseline/scripts"
    if baseline.is_dir():
        report["unchanged_ast_from_previous_review"] = {}
        for file, names in {
            "run_network_194_parallel.py": ["registered_id_set", "build_plan", "cohort_specs", "preflight", "print_followups", "plan_input_digest"],
            "g2_network_reread.py": ["registered_expected", "explicit_expected", "run_launcher", "launcher_detail_problems", "launcher_identity"]
        }.items():
            old = function_ast(baseline / file, names)
            new = function_ast(SOURCE / "scripts" / file, names)
            report["unchanged_ast_from_previous_review"][file] = {name: old.get(name) == new.get(name) for name in names}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
