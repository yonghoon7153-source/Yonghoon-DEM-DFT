#!/usr/bin/env python3
"""Reproduce the v3 mixer audit from sources_mixing only (Python stdlib).

Run: python notes/audit_mixing.py [--save]
--save writes only evidence/mixing_repro.json. No simulations or figures run.
Slide comparison targets below are the values inspected in the submitted v3.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources_mixing"
PIN = "a0439bdf8156236f454bd3f8b5bf4d044e127039"
FINAL = "docs/data/mixer_final10_20260930/"
BO = "docs/data/mixer_highbo_devbo_prelim_20261003/"
U = "docs/data/mixer_highbo_devu_prelim_20261006/"
FINAL_RUNS = [
    "LA_s32452843", "L0_s32452843", "LA_s49979687", "LA_s67867967",
    "LB1_s32452843", "LB2_s32452843", "LB3_s32452843",
    "LC_s32452843", "LC_s49979687", "LC_s67867967",
]
DEV_PATHS = [
    BO + "devbo_c16x4.json", U + "devu_c16x4.json",
    BO + "devbo_c12x3.json", U + "devu_c12x3.json",
    BO + "devbo_c8x2.json", U + "devu_c8x2.json",
]


def total(values):
    # Explicit accumulation also matches the earlier JavaScript calculation.
    result = 0.0
    for value in values:
        result += value
    return result


def average(values):
    return total(values) / len(values)


def sample_sd(values):
    m = average(values)
    return math.sqrt(total([(x - m) ** 2 for x in values]) / (len(values) - 1))


def frame_check(run):
    final_bin = run["planned"]["final_bin"]
    rows = [r for r in run["rows"] if math.floor(r["rev"]) == final_bin]
    values = [(run["S0"] - r["s2"]) / (run["S0"] - run["SR"]) for r in rows]
    assert len(rows) == run["planned"]["expected"]
    m = average(values)
    assert abs(m - run["planned"]["M_final"]) < 1e-12
    assert abs(sample_sd(values) - run["planned"]["M_final_sd"]) < 1e-12
    return {
        "run": run["provenance"]["run"]["name"], "n": len(rows),
        "mean_from_s2": m, "sd_from_s2": sample_sd(values),
        "mean_minus_planned": m - run["planned"]["M_final"],
        "max_abs_row_formula_error": max(abs(x - r["M"]) for x, r in zip(values, rows)),
    }


def audit():
    hashes = {}

    def read(path):
        raw = (SOURCE / path).read_bytes()
        hashes[path] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw)

    proof = {
        "pin": PIN,
        "source_level": "saved reader JSON, not reconstructed from simulation dumps",
        "mix1": [], "mix2": [], "mix3": [],
    }
    final_by_name = {}
    for name in FINAL_RUNS:
        path = FINAL + name + "_c16x4.json"
        runs = read(path)
        assert len(runs) == 1
        r = runs[0]
        final_by_name[name] = r
        proof["mix1"].append({
            "path": path, "S0": r["S0"], "SR": r["SR"], "planned": r["planned"],
            "frame_recalculation": [frame_check(r)],
        })
    development = {}
    for path in DEV_PATHS:
        runs = read(path)
        comparator = runs[0]["planned"]["M_final"]
        assert runs[0]["provenance"]["run"]["name"] == "LC_ref_r2_s32452843"
        data = []
        for r in runs:
            name = r["provenance"]["run"]["name"]
            row = {
                "run": name, "S0": r["S0"], "SR": r["SR"], "planned": r["planned"],
                "delta_from_LC": comparator - r["planned"]["M_final"],
            }
            data.append(row)
            development[(path, name)] = row
        proof["mix2"].append({
            "path": path, "runs": data, "frame_recalculation": [frame_check(r) for r in runs],
        })
    path = U + "devu_contact.json"
    for r in read(path)["runs"]:
        if not r.get("bin", {}).get("mean"):
            continue
        frames, mean = r["bin"]["frames"], r["bin"]["mean"]
        assert len(frames) == 100
        row = {
            "path": path, "run": r["run"], "frames": len(frames),
            "mean_saved": mean["se_frac_in_clusters"],
            "mean_recomputed": average([f["s1_se_clusters"]["se_frac_in_clusters"] for f in frames]),
            "lo_saved": mean["lo.se_frac_in_clusters"],
            "hi_saved": mean["hi.se_frac_in_clusters"],
            "lo_recomputed": average([f["resolution"]["lo"]["se_frac_in_clusters"] for f in frames]),
            "hi_recomputed": average([f["resolution"]["hi"]["se_frac_in_clusters"] for f in frames]),
        }
        for key in ("mean", "lo", "hi"):
            assert abs(row[key + "_saved"] - row[key + "_recomputed"]) < 1e-12
        proof["mix3"].append(row)

    verdict = read(FINAL + "verdict_20260930.json")
    contrasts = {}
    for grid in ("16x4", "12x3", "8x2"):
        differences = []
        for seed in (32452843, 49979687, 67867967):
            if grid == "16x4":
                d = (final_by_name[f"LC_s{seed}"]["planned"]["M_final"]
                     - final_by_name[f"LA_s{seed}"]["planned"]["M_final"])
            else:
                # Full coarser-grid frames were not fetched; use saved readouts.
                d = verdict["runs"][f"LC_s{seed}|{grid}"]["M"] - verdict["runs"][f"LA_s{seed}|{grid}"]["M"]
            differences.append(d)
        m, se = average(differences), sample_sd(differences) / math.sqrt(3)
        contrasts[grid] = {"d": differences, "mean": m, "se": se, "absolute_mean_leq_SE": abs(m) <= se}
        assert abs(m - verdict["main"][grid]["Delta"]) < 1e-12
        assert abs(se - verdict["main"][grid]["SE"]) < 1e-12
    proof["mix1_contrasts"] = contrasts
    proof["mix3_comparison_margins"] = [
        {"run": r["run"], "lower_minus_comparator_upper": r["lo_recomputed"] - proof["mix3"][0]["hi_recomputed"]}
        for r in proof["mix3"][1:]
    ]
    proof["thermodynamic_arithmetic"] = {
        "SE_SE_to_large_NCM_equal_gamma": (4.8 / 2) * 9 ** 2,
        "SE_SE_to_small_NCM_equal_gamma": (4.8 / 2) * 4 ** 2,
        "SE_large_NCM_to_SE_SE_equal_W": 1.8,
        "large_threshold": 1 / 1.8 ** 2, "small_threshold": 1 / 1.6 ** 2,
        "deltaW_identity": "2 gamma_A + 2 gamma_S - 4 sqrt(gamma_A gamma_S) = 2 (sqrt(gamma_A)-sqrt(gamma_S))^2; W in J/m²; equal-area comparison",
    }
    targets = [
        ("F_mix2: NCM Bo384, 12x3", development[(BO + "devbo_c12x3.json", "LHx10_ref_r2_s32452843")]["delta_from_LC"], 0.928),
        ("F_mix2: all-pair CED x14.42, 16x4", development[(U + "devu_c16x4.json", "LU637_ref_r2_s32452843")]["delta_from_LC"], 0.866),
        ("F_mix3: low-cohesion comparator", proof["mix3"][0]["mean_recomputed"], 0.401),
    ]
    proof["rounding_discrepancies"] = [
        {"element": label, "recomputed": value, "three_decimal_rounding": round(value, 3),
         "submitted_v3_value": submitted, "differs": round(value, 3) != submitted}
        for label, value, submitted in targets
    ]
    assert all(r["differs"] for r in proof["rounding_discrepancies"])
    assert len(proof["mix1"]) == 10
    assert sum(len(x["frame_recalculation"]) for x in proof["mix2"]) == 21
    assert len(proof["mix3"]) == 3
    proof["counts"] = {"final_run_grid_readouts": 10, "development_run_grid_readouts": 21,
                       "cluster_runs": 3, "cluster_frames_per_run": 100}
    proof["source_sha256"] = hashes
    return proof


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    result = audit()
    encoded = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.save:
        output = ROOT / "evidence" / "mixing_repro.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
        print(json.dumps({"saved": str(output), **result["counts"],
                          "rounding_discrepancies": result["rounding_discrepancies"]}, ensure_ascii=True))
    else:
        print(encoded, end="")
