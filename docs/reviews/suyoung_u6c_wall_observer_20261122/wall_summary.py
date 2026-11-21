"""Decompose the retained native F8/F16 pressure gap into two wall calls."""
import argparse
from bisect import bisect_left
import csv
import hashlib
import io
import json
import math
from pathlib import Path


TRACE = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
WALL = ("step", "plate_displacement_code", "lid_code", "first_top_row",
        "bottom_J_pre", "bottom_J_post", "top_J_down_pre", "top_J_down_post",
        "floor_positive_mass_entries_pre", "floor_positive_mass_entries_post",
        "top_positive_mass_entries_pre", "top_positive_mass_entries_post", "bottom_pressure_E")
EXPECTED = {8:"03f3bc2c106aa466f1ccc2b774e0b768f2a902792006609680faa53038434cdf",
            16:"5475cc87df297533002afb621cbdac06c0319ca40eb65ddf40322ae6c018b0de"}
SOURCES = {
    "suyoung_u6b_dev.py":"50f1a3aec71b750105852dfec281fc7ca9b84f5d4a594ee8fcc10073d4dba762",
    "suyoung_u6_first_dev.py":"5db0f1bda90c824a23479401b7744cf8d31fc64f373441abca692dce6717bda5",
    "dem_suyoung_sf2d_dev.py":"6e8073230f14142f3f802e1fed316bea22610502a98292e2ef794a123ea7e5f4",
}
COMPONENTS = ("total", "pre", "post")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def rows(data, columns):
    reader = csv.DictReader(io.StringIO(data.decode("ascii"), newline=""))
    require(tuple(reader.fieldnames or ()) == columns, "CSV_COLUMNS")
    records = list(reader)
    require(all(None not in r and None not in r.values() for r in records), "CSV_COLUMNS")
    return records


def read_arm(folder, cells, observer_sha):
    result_data = (folder / "result.json").read_bytes()
    obs_data = (folder / "observer.json").read_bytes()
    trace_data = (folder / "trace.csv").read_bytes()
    side_data = (folder / "wall.csv").read_bytes()
    result, obs = json.loads(result_data), json.loads(obs_data)
    trace_sha = sha(trace_data)
    require(obs["status"] == "DEVELOPMENT_WALL_READBACK" and obs["eligible_development_readback"] is True
            and obs["u6_qualified"] is False and result["status"] == "TARGET_BRACKETED", "INELIGIBLE_ARM")
    require(obs["arm"] == result["arm"] == "F" and obs["cells"] == result["cells"] == cells
            and obs["setting"] == result["setting"] == 1 and obs["label"] == result["label"] == "DEVELOPMENT_ONLY"
            and result["protocol"] == "U6b-setting1-bottom-loading-v1" and result["origin"] == "new", "ARM_BINDING")
    require(obs["expected_trace_sha256"] == obs["trace_sha256"] == result["trace_sha256"] == trace_sha
            == EXPECTED[cells] and obs["wall_sha256"] == sha(side_data) and obs["result_sha256"] == sha(result_data),
            "FILE_BINDING")
    require(obs["observer_sha256"] == observer_sha and obs["original_source_sha256"] == SOURCES and
            result["source_sha256"] == {k:v for k,v in SOURCES.items() if k != "suyoung_u6b_dev.py"},
            "SOURCE_BINDING")
    dt, width, E = obs["dt"], obs["width"], obs["E_MPa"]
    require(E == 10. and math.isfinite(dt) and dt > 0 and math.isfinite(width) and width > 0, "NORMALIZATION")
    trace, side = rows(trace_data, TRACE), rows(side_data, WALL)
    require(len(trace) == len(side)+1 and len(side) == result["steps"] == obs["steps"] > 0, "STEP_COUNT")
    initial = trace[0]
    require(initial["step"]=="0" and float(initial["height"]) == width and
            float(initial["time_code"]) == float(initial["bottom_pressure_E"]) == 0., "INITIAL_STATE")
    samples = [(0.,0.,0.,0.)]  # Native unloaded origin. No step-zero projection was observed.
    for i, (t, s) in enumerate(zip(trace[1:], side), 1):
        u = width - float(t["height"])
        p = float(t["bottom_pressure_E"])
        pre, post = float(s["bottom_J_pre"]), float(s["bottom_J_post"])
        require(t["step"] == s["step"] == str(i) and float(t["time_code"]) == dt*i and
                u == float(s["plate_displacement_code"]) and math.isfinite(u) and u > samples[-1][0],
                "STEP_OR_DISPLACEMENT")
        require(all(math.isfinite(j) and j >= 0 for j in (pre,post,float(s["top_J_down_pre"]),
                                                          float(s["top_J_down_post"]))) and
                math.isfinite(float(s["lid_code"])) and all(s[key].isascii() and s[key].isdigit()
                for key in ("first_top_row", *WALL[8:12])), "INVALID_WALL_RECORD")
        require(p == float(s["bottom_pressure_E"]) == (pre + post)/(dt*width) and math.isfinite(p),
                "NATIVE_REACTION_MISMATCH")
        converted = (u, E*p, E*(pre/(dt*width)), E*(post/(dt*width)))
        require(all(math.isfinite(v) for v in converted), "NONFINITE_PRESSURE")
        samples.append(converted)
    return samples, {"trace_sha256":trace_sha, "wall_sha256":obs["wall_sha256"],
                     "observer_receipt_sha256":sha(obs_data), "result_sha256":obs["result_sha256"],
                     "observed_steps":len(side), "curve_knots_with_initial_state":len(samples),
                     "dt":dt, "width":width, "E_MPa":E}


def at(curve, axis, u):
    j = bisect_left(axis, u)
    if j < len(axis) and axis[j] == u:
        return curve[j][1:], [j,j]
    require(0 < j < len(axis), "OUTSIDE_COMMON_SUPPORT")
    s = (u-axis[j-1]) / (axis[j]-axis[j-1])
    return tuple(a + (b-a)*s for a,b in zip(curve[j-1][1:],curve[j][1:])), [j-1,j]


def decompose(coarse, fine):
    caxis, faxis = ([r[0] for r in curve] for curve in (coarse,fine))
    end = min(caxis[-1],faxis[-1])
    knots = sorted({u for axis in (caxis,faxis) for u in axis if u <= end})
    worst = None
    largest = -1.
    max_residual = 0.
    for u in knots:
        cv, csteps = at(coarse,caxis,u)
        fv, fsteps = at(fine,faxis,u)
        gap = tuple(c-f for c,f in zip(cv,fv))
        residual = abs(gap[0]-(gap[1]+gap[2]))
        # Component conversion, interpolation and subtraction are binary64
        # operations. Bound their closure in the scale of the original signals.
        require(residual <= 16 * math.ulp(max(abs(v) for v in (*cv,*fv))), "COMPONENTS_DO_NOT_CLOSE")
        max_residual = max(max_residual,residual)
        if abs(gap[0]) > largest:
            largest = abs(gap[0])
            worst = {"u":u, "coarse_native_step_bracket":csteps, "fine_native_step_bracket":fsteps,
                     "coarse_MPa":dict(zip(COMPONENTS,cv)), "fine_MPa":dict(zip(COMPONENTS,fv)),
                     "coarse_minus_fine_MPa":dict(zip(COMPONENTS,gap))}
    return {"common_start_u":0., "common_end_u":end, "union_knots":len(knots),
            "maximum_absolute_total_gap_MPa":largest, "at_first_worst_total_gap":worst,
            "max_component_sum_roundoff_MPa":max_residual}


def summarize(runs, observer_sha):
    report = {"status":"INCOMPLETE", "label":"DEVELOPMENT_WALL_DIAGNOSTIC", "u6_qualified":False,
              "stage3_go":False, "observer_sha256":observer_sha, "arms":{}, "issues":{}}
    data = {}
    for cells in (8,16):
        key = f"F{cells}"
        try:
            data[cells], report["arms"][key] = read_arm(runs/key, cells, observer_sha)
        except FileNotFoundError:
            report["issues"][key] = "MISSING_RETURN_FILE"
        except (ArithmeticError, KeyError, OSError, TypeError, ValueError, csv.Error) as exc:
            report["issues"][key] = "INVALID_RETURN_" + type(exc).__name__
    if not report["issues"]:
        try:
            report["decomposition"] = decompose(data[8],data[16])
            report["status"] = "DEVELOPMENT_WALL_DECOMPOSED"
        except (ArithmeticError, ValueError) as exc:
            report["issues"]["pair"] = str(exc)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    report = summarize(args.runs, sha(Path(__file__).with_name("observe.py").read_bytes()))
    with args.out.open("x",encoding="ascii",newline="\n") as out:
        json.dump(report,out,sort_keys=True,indent=2,allow_nan=False)
        out.write("\n")
    print(report["status"])
    return 0 if report["status"]=="DEVELOPMENT_WALL_DECOMPOSED" else 4


if __name__ == "__main__":
    raise SystemExit(main())
