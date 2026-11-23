"""Recompute the signed F12/F24 prefix balances from two original TARs, using only the standard library."""
import argparse
import csv
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path


BALANCE_HASH = "1f680f4f255910bb2c93ce7e2edea004c89b4177fb3a4b8af93bd59edeab209e"
PRIOR_HASH = "c1506ea6fb6f16181fe36e85e76043101380b75c9cf435b2811a5b53b761d673"
PIN = "0c4eb97d447f9afa984303425e1c5ab221ae9cec"
PRIOR_PIN = "e8e2f2535aa12b9fb089d714e1325d862cb1161b"
MARKS = {12: (465, 569), 24: (930, 1138)}
DT = {12: 0.001497578010986372, 24: 0.000748789005493186}
DIAMETER = 0.1
WIDTH = math.sqrt(49 * math.pi * (DIAMETER / 2) ** 2 / 0.78)
REFERENCE = 0.6636991102836952
JCOLS = tuple(
    stage + "_" + group
    for stage in ("floor", "lid", "contact", "grid_change", "particle_change")
    for group in ("all", "bottom_row")
)
TRACE = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
WALL = ("step", "displacement_code", "top_gap_before", "floor_gap_before", "native_floor_impulse", *JCOLS)


def verify(condition, context):
    if not condition:
        raise ValueError(context)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_archive(path, expected):
    data = path.read_bytes()
    verify(digest(data) == expected, "archive SHA-256: " + path.name)
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as container:
        for member in container:
            if member.isdir():
                continue
            verify(member.isfile() and member.name not in files, "unexpected member " + member.name)
            files[member.name] = container.extractfile(member).read()
    return files


def numeric_rows(data, columns):
    rows = csv.DictReader(io.StringIO(data.decode("ascii"), newline=""))
    verify(tuple(rows.fieldnames) == columns, "CSV header")
    out = []
    for row in rows:
        verify(tuple(row) == columns, "CSV extra column")
        decoded = {key: int(v) if key == "step" else float(v) for key, v in row.items()}
        verify(all(math.isfinite(v) for v in decoded.values()), "non-finite CSV")
        out.append(decoded)
    return out


def summed(rows):
    return {key: math.fsum(row[key] for row in rows) for key in JCOLS}


def scaled(terms, factor):
    return {key: value * factor for key, value in terms.items()}


def differences(a, b):
    return {key: value - b[key] for key, value in a.items()}


def residuals(wall, trace, dt):
    result = {
        "floor_vs_native_J": abs(wall["native_floor_impulse"] - wall["floor_all"]),
        "all_floor_outside_bottom_row_J": abs(wall["floor_all"] - wall["floor_bottom_row"]),
        "bottom_row_lid_J": abs(wall["lid_bottom_row"]),
        "interbody_global_J": abs(wall["contact_all"]),
        "reconstructed_pressure_MPa": abs(
            wall["native_floor_impulse"] / (WIDTH * dt) * 10 - 10 * trace["bottom_pressure_E"]
        ),
    }
    for group in ("all", "bottom_row"):
        demand = math.fsum(wall[stage + "_" + group] for stage in ("floor", "lid", "contact"))
        result["grid_vs_demand_" + group + "_J"] = abs(wall["grid_change_" + group] - demand)
        result["particles_vs_grid_" + group + "_J"] = abs(wall["particle_change_" + group] - wall["grid_change_" + group])
    return result


def read_arm(new, prior, cells):
    arm = f"F{cells}"
    path = "run/" + arm + "/"
    receipt = json.loads(new[path + "balance_receipt.json"])
    old_receipt = json.loads(prior[path + "fine_receipt.json"])
    verify(json.loads(new["run/summary.json"])["arms"][str(cells)] == receipt, "returned summary vs receipt")
    verify(json.loads(prior["run/summary.json"])["arms"][arm] == old_receipt, "prior summary vs receipt")
    dt = DT[cells]
    last = MARKS[cells][-1]
    native, old, impulses = new[path + "trace.csv"], prior[path + "trace.csv"], new[path + "wall_impulses.csv"]
    verify(receipt["release"] == PIN and old_receipt["release"] == PRIOR_PIN, "arm release")
    verify(receipt["previous_tar_sha256"] == PRIOR_HASH and old_receipt["reached_target"], "prior identity and status")
    verify(old_receipt["result_sha256"] == digest(prior[path + "result.json"]), "prior result binding")
    verify(receipt["trace_sha256"] == digest(native) and receipt["observer_table_sha256"] == digest(impulses), "raw receipt binding")
    verify(receipt["steps"] == last and receipt["dt"] == dt and receipt["width"] == WIDTH, "native inputs")
    verify(len(old.splitlines()) == old_receipt["native_steps"] + 2 and digest(old) == old_receipt["trace_sha256"], "prior full trace")
    verify(native == b"".join(old.splitlines(keepends=True)[:last + 2]), "prior byte-for-byte prefix")
    traces = numeric_rows(native, TRACE)
    rows = numeric_rows(impulses, WALL)
    verify(len(rows) == last and len(traces) == last + 1, "prefix length")
    verify(traces[0]["height"] == WIDTH and traces[0]["time_code"] == traces[0]["step"] == 0, "initial trace")
    maxima = {}
    for i, row in enumerate(rows, 1):
        sample = traces[i]
        verify(row["step"] == sample["step"] == i and sample["time_code"] == i * dt, "native time/steps")
        verify(row["displacement_code"] == WIDTH - sample["height"], "native displacement")
        verify(row["lid_all"] <= 0 and row["native_floor_impulse"] >= 0, "wall directions on material")
        for key, value in residuals(row, sample, dt).items():
            maxima[key] = max(maxima.get(key, 0), value)
    verify(max(maxima.values()) <= 2e-12, "momentum/pressure closure")
    gap = [r for r in rows if r["top_gap_before"] > 1e-12 and r["lid_all"] < 0]
    first_lid = next(r for r in rows if r["lid_all"] < 0)
    first_floor = next(r for r in rows if r["native_floor_impulse"] > 0)
    gap_sum = math.fsum(row["lid_all"] for row in gap)
    totals = summed(rows)
    verify(first_lid == receipt["first_lid_down_impulse"] and first_floor == receipt["first_floor_up_impulse"], "first impulses")
    verify(len(gap) == receipt["steps_with_lid_impulse_and_positive_material_gap"] and
           gap_sum == receipt["cumulative_lid_impulse_with_positive_material_gap"], "gap receipt")
    verify(all(totals[k] == receipt["signed_impulse_sums"][k] for k in JCOLS), "signed cumulative receipt")
    verify([rows[s - 1] for s in MARKS[cells]] == receipt["snapshots"], "snapshot receipt")
    step_ids = [r["step"] for r in gap]
    intervals = []
    for step in step_ids:
        if intervals and step == intervals[-1][1] + 1:
            intervals[-1][1] = step
        else:
            intervals.append([step, step])
    summary = {
        "dt_code": dt, "projected_steps": last, "identical_previous_native_prefix_data_rows_including_initial": last + 1,
        "full_trace_sha256": digest(old), "native_prefix_sha256": digest(native), "observer_table_sha256": digest(impulses),
        "first_lid_down_step": first_lid["step"], "first_floor_up_step": first_floor["step"],
        "first_lid_impulse_code": first_lid["lid_all"], "first_top_gap_D": first_lid["top_gap_before"] / DIAMETER,
        "steps_with_downward_lid_during_positive_gap": len(gap), "positive_gap_step_intervals": intervals,
        "downward_lid_during_positive_gap_J": gap_sum, "positive_gap_fraction_of_downward_lid_pct": 100 * gap_sum / totals["lid_all"],
        "maximum_absolute_step_residuals": maxima,
    }
    return traces, rows, summary


def snapshot(traces, rows, cells, step):
    row = rows[step - 1]
    dt = DT[cells]
    clock = traces[step]["time_code"]
    factor = 10 / (WIDTH * dt)
    observed = {k: row[k] for k in JCOLS}
    accumulated = summed(rows[:step])
    return {
        "step": step, "time_code": clock, "plate_displacement_D": row["displacement_code"] / DIAMETER,
        "top_gap_before_D": row["top_gap_before"] / DIAMETER, "floor_gap_before_D": row["floor_gap_before"] / DIAMETER,
        "native_floor_pressure_MPa": traces[step]["bottom_pressure_E"] * 10,
        "single_step_signed_J": observed, "single_step_signed_equivalent_MPa": scaled(observed, factor),
        "signed_J_since_initial": accumulated,
        "time_average_signed_equivalent_MPa_since_initial": scaled(accumulated, 10 / (WIDTH * clock)),
    }


def compare_prefix(coarse, fine):
    # Confirm the fine grid contains the complete native displacement union; only odd steps require interpolation.
    verify(len(fine) == 2 * len(coarse) - 1, "native grid nesting")
    first = None
    peak = None
    for j, sample in enumerate(fine):
        left = coarse[j // 2]
        pressure = left["bottom_pressure_E"]
        if j % 2:
            right = coarse[j // 2 + 1]
            fraction = (sample["height"] - left["height"]) / (right["height"] - left["height"])
            verify(0 < fraction < 1, "interpolation bounds")
            pressure += fraction * (right["bottom_pressure_E"] - pressure)
        else:
            verify(sample["height"] == left["height"] and sample["time_code"] == left["time_code"], "native knot mismatch")
        gap = 10 * (pressure - sample["bottom_pressure_E"])
        record = {"F24_step": j, "F12_step_if_native": None if j % 2 else j // 2,
                  "displacement_D": (WIDTH - sample["height"]) / DIAMETER,
                  "F12_minus_F24_MPa": gap, "absolute_percent_fixed_reference": 100 * abs(gap) / REFERENCE}
        if first is None and abs(gap) > .05 * REFERENCE:
            first = record
        if peak is None or abs(gap) > abs(peak["F12_minus_F24_MPa"]):
            peak = record
    verify(first is not None and tuple(r["F24_step"] for r in (first, peak)) == MARKS[24], "landmarks vs native pressure union")
    return {"union_points": len(fine), "fixed_reference_MPa": REFERENCE, "threshold_MPa": .05 * REFERENCE,
            "first_above_5_pct": first, "maximum_in_observed_prefix": peak}


def evaluate(balance, prior):
    new, old = read_archive(balance, BALANCE_HASH), read_archive(prior, PRIOR_HASH)
    for source, pin in ((new, PIN), (old, PRIOR_PIN)):
        verify(source["run/RELEASE"].decode("ascii").strip() == pin, "run release identity")
        verify(source["run/screen.txt"].splitlines()[-1] == b"COMMAND_RC=0", "terminal status")
    data = {n: read_arm(new, old, n) for n in MARKS}
    comparisons = []
    for i, coarse_step in enumerate(MARKS[12]):
        snap = {n: snapshot(*data[n][:2], n, MARKS[n][i]) for n in MARKS}
        verify(snap[12]["time_code"] == snap[24]["time_code"] and
               snap[12]["plate_displacement_D"] == snap[24]["plate_displacement_D"], "matched native endpoint")
        delta = differences(snap[12]["single_step_signed_equivalent_MPa"], snap[24]["single_step_signed_equivalent_MPa"])
        end = 2 * coarse_step
        fine_two = scaled(summed(data[24][1][end-2:end]), 10 / (WIDTH * DT[12]))
        delta_same_window = differences(snap[12]["single_step_signed_equivalent_MPa"], fine_two)
        comparisons.append({
            "snapshots": {"F12": snap[12], "F24": snap[24]},
            "F12_minus_F24_native_endpoint_equivalent_MPa": delta,
            "F12_minus_F24_since_initial_signed_J": differences(snap[12]["signed_J_since_initial"], snap[24]["signed_J_since_initial"]),
            "identical_step_window": {"F12_steps": [coarse_step], "F24_steps": [end - 1, end],
                                      "F24_interval_average_signed_equivalent_MPa": fine_two,
                                      "F12_minus_F24_interval_average_signed_equivalent_MPa": delta_same_window},
        })
    return {
        "balance_return_sha256": BALANCE_HASH, "previous_full_fine_return_sha256": PRIOR_HASH,
        "release": PIN, "prior_release": PRIOR_PIN, "width_code": WIDTH, "diameter_code": DIAMETER,
        "sign": "Positive is upward impulse on material. Only the floor equivalent is the reported bottom pressure.",
        "per_step_conversion": "10 * J / (width * native dt) MPa. J is in native impulse units.",
        "bottom_row_initial_body_ids": list(range(0, 49, 7)),
        "gaps": "At step entry: commanded lid position minus maximum tracked material surface y, and minimum surface y minus floor. Positive-gap threshold is 1e-12 code length.",
        "native_pressure_union": compare_prefix(data[12][0], data[24][0]),
        "arms": {f"F{n}": data[n][2] for n in MARKS}, "matched_comparisons": comparisons,
    }


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("balance_return", type=Path)
    cli.add_argument("prior_full_fine_return", type=Path)
    cli.add_argument("--out", type=Path)
    args = cli.parse_args()
    report = json.dumps(evaluate(args.balance_return, args.prior_full_fine_return), indent=2, allow_nan=False) + "\n"
    if args.out:
        args.out.write_bytes(report.encode("utf-8"))
    else:
        print(report, end="")
