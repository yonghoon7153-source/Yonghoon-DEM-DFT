"""Mutation probe for test_reg1_block.py: break one rule in a copy of the block and check the named tests fail.

    python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/reg1_block/mutation_probe.py [--only TEXT]

Each mutation edits a copy of one block file (reg1_reader.py, reg1_queue.py or run.sh).  The copies of
the two Python files are written to a temporary folder and loaded from there for the in-process tests,
and the packages the shell tests build read the mutated bytes through a patched `read_repo`.  Nothing
in the repository is written.  Each line reports how many of the selected tests fail (all should).
"""
import argparse
import importlib.util
import io
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

HERE = Path(__file__).resolve().parent
BLOCK_REL = "docs/reviews/suyoung_next_registrations_20261125/reg1_block/"
RULE, ARM, SUM, DEC, QUE, UNP, CHK, E2E = ("ReaderRuleTests.", "ReaderArmTests.", "ReaderSummaryTests.",
                                          "DecisionTests.", "QueueTests.", "UnpackTests.", "CheckOnlyTests.",
                                          "EndToEndTests.")
MUTATIONS = [
    ("J1 judges 8-16 in place of 24-48", "reg1_reader.py",
     'state = ctx.force.aggregate({first: pairs["16_32"], second: pairs["24_48"]})',
     'state = ctx.force.aggregate({first: pairs["16_32"], second: pairs["8_16"]})',
     [RULE + "test_j1_verdict_uses_only_judged_pairs_with_force_rule_combination"]),
    ("J1 exceedance demoted to hold", "reg1_reader.py",
     'return {"WITHIN": "CONVERGED"}.get(state, state)',
     'return {"WITHIN": "CONVERGED", "EXCEEDS": "HOLD"}.get(state, state)',
     [RULE + "test_j1_verdict_uses_only_judged_pairs_with_force_rule_combination"]),
    ("J1 coarse and fine swapped", "reg1_reader.py",
     'return dict(base, **ctx.force.compare(coarse["curve"], fine["curve"]))',
     'return dict(base, **ctx.force.compare(fine["curve"], coarse["curve"]))',
     [RULE + "test_j1_pair_is_the_u6c_force_rule", RULE + "test_j1_exact_five_percent_boundary"]),
    ("J2 limit 1/10", "reg1_reader.py",
     "exceeds = ctx.force.exceeds(float(numerator), float(denominator))",
     "exceeds = 10 * numerator > denominator",
     [RULE + "test_j2_exact_boundary_and_zero"]),
    ("J2 denominator from the top plate", "reg1_reader.py",
     "denominator = max((abs(b) for _, b in forces), default=0.)",
     "denominator = max((abs(t) for t, _ in forces), default=0.)",
     [RULE + "test_j2_exact_boundary_and_zero"]),
    ("J3 one-disk curve read at u", "reg1_reader.py",
     "[(2. * u, sigma) for u, sigma in g1[\"curve\"]]",
     "[(u, sigma) for u, sigma in g1[\"curve\"]]",
     [RULE + "test_j3_maps_u_to_half_and_judges_32_and_48"]),
    ("J3 judged at 48 only", "reg1_reader.py",
     "judged = [cells[str(n)] for n in J3_CELLS]",
     'judged = [cells["48"], cells["48"]]',
     [RULE + "test_j3_maps_u_to_half_and_judges_32_and_48"]),
    ("J3 J2 holds called technical", "reg1_reader.py",
     'return "HOLD", "J2" if kinds and all(k == "J2" for k in kinds) else "TECHNICAL"',
     'return "HOLD", "TECHNICAL"',
     [RULE + "test_j3_maps_u_to_half_and_judges_32_and_48"]),
    ("first force at or above the floor", "reg1_reader.py",
     "if k and sigma > threshold:", "if k and sigma >= threshold:",
     [RULE + "test_first_force_is_strictly_above_the_noise_floor"]),
    ("lateral watch on one-disk arms too", "reg1_reader.py",
     'watch = arm.geometry == "G2"', "watch = True",
     [ARM + "test_lateral_offset_holds_two_disks_only"]),
    ("lateral limit doubled", "reg1_reader.py",
     "if abs(v) > d.LATERAL_LIMIT_D), None)", "if abs(v) > 2 * d.LATERAL_LIMIT_D), None)",
     [ARM + "test_lateral_offset_holds_two_disks_only"]),
    ("one side-wall hit allowed", "reg1_reader.py",
     "if side > 0:", "if side > 1:",
     [ARM + "test_side_wall_and_penetration_are_held"]),
    ("penetration limit made exclusive", "reg1_reader.py",
     "if penetration > d.PENETRATION_LIMIT:", "if penetration >= d.PENETRATION_LIMIT:",
     [ARM + "test_side_wall_and_penetration_are_held"]),
    ("non-finite values ignored", "reg1_reader.py",
     '    if nonfinite:\n        violations.append("NONFINITE")\n', "",
     [ARM + "test_nonfinite_is_held"]),
    ("schedule check dropped", "reg1_reader.py",
     'reasons.append("SCHEDULE")', "pass",
     [ARM + "test_record_mismatches_are_held"]),
    ("trace hash check dropped", "reg1_reader.py",
     'reasons.append("TRACE_SHA")', "pass",
     [ARM + "test_record_mismatches_are_held"]),
    ("source identity check dropped", "reg1_reader.py",
     'if result.get("sources") != e.source_record():', "if False:",
     [ARM + "test_block_errors_from_one_arm"]),
    ("worker rc 2 not a block error", "reg1_reader.py",
     "if rc in (1, 2):", "if rc in (1,):",
     [ARM + "test_block_errors_from_one_arm"]),
    ("J4 strain without the gap", "reg1_reader.py",
     'u = rec["u_geo"] + eps * ctx.engine.const.D', "u = eps * ctx.engine.const.D",
     [ARM + "test_j4_and_j5_on_small_arms"]),
    ("J5 sigma_yy sign kept", "reg1_reader.py",
     "[-p[2] for p in points]", "[p[2] for p in points]",
     [ARM + "test_j4_and_j5_on_small_arms"]),
    ("three-valued rows collapsed to two", "reg1_reader.py",
     "return True if verdict == true else False if verdict == false else None",
     "return True if verdict == true else False",
     [DEC + "test_precedence_and_three_valued_rows"]),
    ("last TRUE row wins", "reg1_reader.py",
     'decided = next((r for r in rows if r["value"] is True), None)',
     'decided = next((r for r in reversed(rows) if r["value"] is True), None)',
     [DEC + "test_precedence_and_three_valued_rows"]),
    ("row 7 reads the V0 plate verdict", "reg1_reader.py",
     '7: _and(conv[g1v4], contacts["S"]["v4_exceeds"], contacts["F2"]["v4_exceeds"])}',
     '7: _and(conv[g1v0], contacts["S"]["v4_exceeds"], contacts["F2"]["v4_exceeds"])}',
     [DEC + "test_precedence_and_three_valued_rows"]),
    ("gap flag needs F1 to exceed", "reg1_reader.py",
     'gap = _and(conv["G2-F1-P-V4"], exc["G2-F2-P-V4"])', 'gap = _and(exc["G2-F1-P-V4"], exc["G2-F2-P-V4"])',
     [DEC + "test_gap_flag"]),
    ("solver refusal removed", "reg1_reader.py",
     "    driver.run_arm = refuse\n", "",
     [SUM + "test_reader_never_runs_the_solver"]),
    ("distinct physical cores unchecked", "reg1_reader.py",
     " and len({tuple(v) for v in cores.values()}) == 2)", ")",
     [SUM + "test_technical_incomplete_cases"]),
    ("environment identity unchecked", "reg1_reader.py",
     'if (env.get("python"), env.get("numpy")) != tuple(target_environment):', "if False:",
     [SUM + "test_technical_incomplete_cases"]),
    ("replay accepts any archived summary", "reg1_reader.py",
     'Q.require(archived == summary, "ARCHIVED_SUMMARY_MISMATCH")', "pass",
     [SUM + "test_summary_cli_and_replay"]),
    ("first force from a trace with non-finite values", "reg1_reader.py",
     "    if not nonfinite:\n        first = first_force(", "    if True:\n        first = first_force(",
     [ARM + "test_nonfinite_displacement_does_not_break_the_summary"]),
    ("report values not made JSON-safe", "reg1_reader.py",
     "return value if math.isfinite(value) else None", "return value",
     [ARM + "test_nonfinite_displacement_does_not_break_the_summary"]),
    ("a closed screen stops the queue", "reg1_queue.py",
     "    except OSError:\n        pass", "    except OSError:\n        raise",
     [QUE + "test_a_closed_screen_does_not_lose_the_execution_record"]),
    ("queue shortest first", "reg1_queue.py",
     'jobs.sort(key=lambda j: (-j["est_high_s"], j["arm"]))', 'jobs.sort(key=lambda j: (j["est_high_s"], j["arm"]))',
     [QUE + "test_queue_follows_the_driver_plan_longest_first"]),
    ("grace 60 s", "reg1_queue.py", "GRACE_S = 30", "GRACE_S = 60",
     [QUE + "test_queue_follows_the_driver_plan_longest_first"]),
    ("a failed arm is started again", "reg1_queue.py",
     "                elif rc is not None:\n                    finished(cpu, rc, False)\n",
     "                elif rc is not None:\n                    finished(cpu, rc, False)\n"
     "                    if rc and not job.get(\"again\"):\n                        pending.append(dict(job, again=True))\n",
     [QUE + "test_each_arm_once_on_two_cores_and_a_failure_does_not_stop_the_rest"]),
    ("same physical core allowed", "reg1_queue.py",
     "require(len(cpus) == 2 and cpus[0] != cpus[1] and list(cores[cpus[0]]) != list(cores[cpus[1]]),",
     "require(len(cpus) == 2,",
     [QUE + "test_same_physical_core_is_refused"]),
    ("no kill after limit plus grace", "reg1_queue.py",
     'if rc is None and time.monotonic() - mono > job["limit_s"] + grace_s:', "if False:",
     [QUE + "test_limit_plus_grace_kills_and_the_queue_goes_on"]),
    ("unpack ignores the command rc", "reg1_queue.py",
     'require(last == b"COMMAND_RC=0", "incomplete return: " + last.decode("ascii", "replace"))', "pass",
     [UNP + "test_bad_returns"]),
    ("CHECK_ONLY does not stop before the reservation", "run.sh",
     "if [[ $mode == CHECK_ONLY ]]; then echo CONTACT_MINI_CHECK_ONLY_OK; exit 0; fi\n", "",
     [CHK + "test_check_only_passes_with_plan_seeds_and_reader_self_check"]),
    ("block CHECK_ONLY token same as the driver's", "run.sh",
     "echo CONTACT_MINI_CHECK_ONLY_OK; exit 0", "echo CHECK_ONLY_OK; exit 0",
     [CHK + "test_check_only_passes_with_plan_seeds_and_reader_self_check"]),
    ("reservation reused", "run.sh",
     'mkdir -- "$once" || { echo "ALREADY_RESERVED $once"; exit 2; }', 'mkdir -p -- "$once"',
     [E2E + "test_second_go_is_already_reserved"]),
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(mutation, base):
    name, target, old, new, tests = mutation
    folder = Path(tempfile.mkdtemp(prefix="reg1_block_mutation_"))
    try:
        for file in ("reg1_reader.py", "reg1_queue.py", "run.sh"):
            shutil.copy(HERE / file, folder / file)
        text = (folder / target).read_text("utf-8")
        assert text.count(old) == 1, f"{name}: mutation anchor not unique ({text.count(old)})"
        (folder / target).write_text(text.replace(old, new), "utf-8")
        if target == "run.sh":
            subprocess.run(["bash", "-n", str(folder / target)], check=True)
        t = load("reg1_probe_tests", HERE / "test_reg1_block.py")
        original_read = t.read_repo

        def read_repo(relative):
            if relative.startswith(BLOCK_REL) and (folder / relative[len(BLOCK_REL):]).is_file():
                return (folder / relative[len(BLOCK_REL):]).read_bytes()
            return original_read(relative)
        t.read_repo = read_repo
        t._CACHE["reg1_queue"] = load("reg1_probe_queue", folder / "reg1_queue.py")
        t._CACHE["reg1_reader"] = load("reg1_probe_reader", folder / "reg1_reader.py")
        if base is not None:
            t._CACHE["base"] = base
        suite = unittest.TestSuite()
        for test in tests:
            cls, method = test.split(".")
            suite.addTest(getattr(t, cls)(method))
        result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
        failed = len(result.failures) + len(result.errors)
        return failed, result.testsRun
    finally:
        shutil.rmtree(folder, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--only", help="run the mutations whose name contains this text")
    args = parser.parse_args()
    t = load("reg1_probe_base", HERE / "test_reg1_block.py")
    base = t.base_run()
    # Control: the same copy-and-load path with no change keeps every selected fast test passing.
    fast = sorted({test for m in MUTATIONS for test in m[4] if not test.startswith((E2E, CHK))}
                  - {QUE + "test_limit_plus_grace_kills_and_the_queue_goes_on"})
    failed, ran = run(("control (no change)", "reg1_reader.py", "LABEL = ", "LABEL = ", fast), base)
    print(f"CONTROL {ran - failed}/{ran} passing without a mutation", flush=True)
    if failed:
        return 1
    caught = total = 0
    for mutation in MUTATIONS:
        if args.only and args.only not in mutation[0]:
            continue
        start = time.monotonic()
        failed, ran = run(mutation, base)
        total += 1
        caught += failed == ran and ran > 0
        print(f"{'CAUGHT ' if failed == ran and ran > 0 else 'MISSED '} {failed}/{ran} failing  {mutation[0]}"
              f"  ({time.monotonic() - start:.0f} s)", flush=True)
    print("MUTATIONS_ALL_CAUGHT" if caught == total else f"MUTATIONS_MISSED {total - caught}", f"{caught}/{total}")
    return 0 if caught == total else 1


if __name__ == "__main__":
    sys.exit(main())
