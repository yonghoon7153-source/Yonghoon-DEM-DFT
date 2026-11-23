"""Offline readback of two frozen author returns. Uses only Python's standard library."""
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


CURRENT = "cd9b0e6b9ce31719716b3ae4b9f97734a7a4ba3614c7de7bd3d93d44f3be83e6"
HALF = "ddcf2fd738430c40246d177d1e1dea73de24883c07218e4f07c0dcf6de90f863"
PIN = "9638542795ed98edf8b1c9ac52d88c3a0e2f8f3b"
HALF_PIN = "ba0e2bb980a4f098aee6ee526d069ed2d2446151"
SCREEN = "4717cea65deecf413d714e25ccad7c302575b373d05b3657670db474e3af3c08"
REFERENCE = 0.6636991102836952
LAYERS = ("lower", "middle", "upper")
FIELDS = (*LAYERS, "whole", "floor", "lid_signed")
STEPS = {12: 555, 24: 1110}


def require(condition, name):
    if not condition:
        raise ValueError(name)


def hash_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def archive(path, expected):
    data = path.read_bytes()
    require(hash_bytes(data) == expected, "return SHA256")
    files = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as source:
        for member in source:
            if member.isdir():
                continue
            require(member.isfile() and member.name.startswith("run/") and member.name not in files, "tar members")
            files[member.name] = source.extractfile(member).read()
    return files


def table(data):
    return list(csv.DictReader(io.StringIO(data.decode("ascii"), newline="")))


def close(a, b, key, tol=2e-12):
    require(math.isfinite(a) and math.isfinite(b) and math.isclose(a, b, rel_tol=tol, abs_tol=tol), key)


def check_prefix(short, long, count):
    rows = long.splitlines(keepends=True)
    require(len(rows) >= count + 1 and short == b"".join(rows[:count + 1]), "changed historical CSV prefix")


def scope(files, pin, status):
    summary = json.loads(files["run/summary.json"])
    screen = files["run/screen.txt"].splitlines()
    require(files["run/RELEASE"] == (pin + "\n").encode() and summary["release"] == pin
            and summary["source_sha256"] == hash_bytes(files["run/SOURCE_SHA256SUMS"]), "release/manifest")
    require(summary["label"] == "DEVELOPMENT_ONLY" and summary["status"] == status and
            all(summary[k] is False for k in ("u6_qualified", "stage3_go", "three_dimensional_go")), "scope")
    require(screen[-1] == b"COMMAND_RC=0" and {b"F12_RC=0", b"F24_RC=0"} <= set(screen), "incomplete run")
    return summary


def check_arm(n, files, old, summary, prev):
    end = STEPS[n]
    key = f"run/F{n}/"
    receipt = json.loads(files[key + "layer_receipt.json"])
    old_receipt = json.loads(old[key + "half_speed_receipt.json"])
    require(receipt == summary["arms"][str(n)] and receipt["release"] == PIN and
            receipt["steps"] == end and receipt["cell_count"] == n and
            old_receipt == prev["arms"][str(n)] and old_receipt["release"] == HALF_PIN, "arm receipts")
    for name, new_key, old_key, data_rows in (("trace.csv", "trace_sha256", "trace_sha256", end+1),
                                               ("wall_steps.csv", "wall_sha256", "wall_csv_sha256", end)):
        old_csv, current_csv = old[key + name], files[key + name]
        require(hash_bytes(current_csv) == receipt[new_key] and hash_bytes(old_csv) == old_receipt[old_key], name)
        check_prefix(current_csv, old_csv, data_rows)
    material = files[key + "layer_steps.csv"]
    motion = old[key + "particle_momentum.csv"]
    require(hash_bytes(material) == receipt["layer_sha256"] and
            hash_bytes(motion) == old_receipt["particle_momentum_sha256"], "momentum tables")
    layers, walls = table(material), table(files[key + "wall_steps.csv"])
    prior, trace = table(motion)[:end], table(files[key + "trace.csv"])
    require(len(layers) == len(walls) == len(prior) == end == len(trace)-1, "row counts")
    dt, width = float(trace[1]["time_code"]), float(trace[0]["height"])
    require(dt == old_receipt["native_dt"] and dt > 0 and width > 0, "geometry and time")
    require(trace[0]["step"] == "0" and float(trace[0]["time_code"]) == float(trace[0]["bottom_pressure_E"]) == 0, "initial row")
    previous = {k: 0.0 for k in (*LAYERS, "whole")}
    records = []
    max_layer_residual = max_wall_residual = 0.0
    for step, (row, w, p, t) in enumerate(zip(layers, walls, prior, trace[1:], strict=True), 1):
        require(all(r["step"] == str(step) for r in (row, w, p, t)), "step numbers")
        before = {k: float(row[k+"_before"]) for k in previous}
        after = {k: float(row[k+"_after"]) for k in previous}
        require(before == previous and all(math.isfinite(v) for v in after.values()), "momentum continuity")
        impulses = {k: after[k]-before[k] for k in previous}
        require(all(impulses[k] == float(row[k+"_delta"]) for k in impulses), "layer deltas")
        require(before["whole"] == float(p["particle_Py_before"]) and after["whole"] == float(p["particle_Py_after"])
                and impulses["whole"] == float(p["particle_delta_Py"]), "previous direct particle momentum")
        impulses.update(floor=float(w["floor_impulse"]), lid_signed=float(w["lid_signed_impulse"]))
        require(impulses["floor"] == float(row["floor_J"]) >= 0 and
                impulses["lid_signed"] == float(row["lid_signed_J"]) <= 0, "signed plate impulses")
        net = math.fsum((impulses["floor"], impulses["lid_signed"]))
        require(net == float(row["wall_signed_J"]) == float(p["wall_signed_J"]), "previous wall total")
        for values in (before, after, impulses):
            close(math.fsum(values[k] for k in LAYERS), values["whole"], "layer sum")
        close(net, impulses["whole"], "wall sum")
        close(10*impulses["floor"]/(width*dt), 10*float(t["bottom_pressure_E"]), "trace pressure")
        require(float(t["time_code"]) == dt*step, "clock")
        max_layer_residual = max(max_layer_residual, abs(math.fsum(impulses[k] for k in LAYERS)-impulses["whole"]))
        max_wall_residual = max(max_wall_residual, abs(net-impulses["whole"]))
        records.append(impulses)
        previous = after
    return dict(records=records, trace=trace, dt=dt, width=width, layer_spec=receipt["layer_spec"],
                max_layer_sum_residual_J=max_layer_residual, max_wall_sum_residual_J=max_wall_residual)


def window(arm, step, count):
    require(1 <= count <= step <= len(arm["records"]), "window bounds")
    samples = arm["records"][step-count:step]
    factor = 10/(arm["width"] * arm["dt"] * count)
    return {k: math.fsum(row[k] for row in samples) * factor for k in FIELDS}


def differences(a, b):
    return {k: a[k]-b[k] for k in FIELDS}


def inspect(depth_tar, half_tar):
    files, old = archive(depth_tar, CURRENT), archive(half_tar, HALF)
    new, prev = scope(files, PIN, "DEPTH_PREFIX_COMPLETE"), scope(old, HALF_PIN, "HALF_SPEED_PREFIX_COMPLETE")
    require(hash_bytes(files["run/screen.txt"]) == SCREEN and new["model_release"] == HALF_PIN and
            new["half_return_sha256"] == HALF and new["half_speed"] == prev["half_wall_speed"] and
            new["balance_return_sha256"] == prev["baseline_sha256"] and
            new["material_return_sha256"] == prev["original_speed_material_lid_sha256"] and
            prev["reference_MPa"] == REFERENCE, "reference lineage")
    a, b = (check_arm(n, files, old, new, prev) for n in (12,24))
    require(a["width"] == b["width"] and a["dt"] == 2*b["dt"], "grid domains/clocks")
    series, anchors = [], []
    saved = {tuple(item["steps_F12_F24"]): item for item in new["observations"]}
    require(set(saved) == {(481,962),(555,1110)}, "registered windows")
    for i in range(1, STEPS[12]+1):
        j = 2*i
        left, right = a["trace"][i], b["trace"][j]
        require(left["height"] == right["height"] and left["time_code"] == right["time_code"], "unmatched displacement/time")
        record = dict(F12_step=i, F24_step=j, displacement_D=(a["width"]-float(left["height"]))/.1, time_code=float(left["time_code"]))
        arms = [window(a,i,1), window(b,j,1), window(b,j,2)]
        gaps = [differences(arms[0], item) for item in arms[1:]]
        for tag, gap in zip(("native","equal_duration"), gaps, strict=True):
            close(gap["whole"], math.fsum(gap[k] for k in LAYERS), "matched layer balance")
            close(gap["whole"], gap["floor"]+gap["lid_signed"], "matched wall balance")
            for k in FIELDS:
                record[f"{tag}_{k}_MPa"] = gap[k]
        series.append(record)
        if (i,j) in saved:
            grouped = dict(zip(("F12","F24","F24_equal_duration","F12_minus_F24","F12_minus_F24_equal_duration"), [*arms,*gaps], strict=True))
            for key, window_data in grouped.items():
                for k, value in window_data.items():
                    saved_key = k + ("_delta_MPa" if k in (*LAYERS, "whole") else "_MPa")
                    close(value, saved[i,j][key][saved_key], "anchor summary "+key+" "+k)
            anchors.append(dict(F12_step=i, F24_step=j, displacement_D=record["displacement_D"], time_code=record["time_code"], **grouped))
    first = next(r for r in series if abs(r["native_floor_MPa"]) > .05*REFERENCE)
    peak = max(series, key=lambda r: abs(r["native_floor_MPa"]))
    require(first["F12_step"] == 481 and peak["F12_step"] == 555, "anchors vs direct floor readings")
    report = dict(status="DEVELOPMENT_ONLY", U6c="HOLD", stage3="HOLD", three_dimensional="HOLD",
                  release=PIN, return_sha256=CURRENT, half_return_sha256=HALF, screen_sha256=SCREEN,
                  fixed_denominator_MPa=REFERENCE, common_measured_windows=len(series),
                  first_common_crossing_pct=100*abs(first["native_floor_MPa"])/REFERENCE,
                  max_common_prefix_pct=100*abs(peak["native_floor_MPa"])/REFERENCE,
                  units="Layer and whole values are signed upward changes in vertical momentum per time and width in MPa equivalents.",
                  layer_convention="Material-point membership is set by initial height relative to the initial plate gap.",
                  arms={str(n):{k:arm[k] for k in ("dt","width","layer_spec","max_layer_sum_residual_J","max_wall_sum_residual_J")}
                        for n,arm in ((12,a),(24,b))}, anchors=anchors)
    return report, series


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    for name in ("depth_tar","half_tar","output_dir"):
        cli.add_argument(name, type=Path)
    args = cli.parse_args()
    result, series = inspect(args.depth_tar, args.half_tar)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir/"depth_readback.json").write_bytes((json.dumps(result,indent=2,allow_nan=False)+"\n").encode())
    with (args.output_dir/"depth_common.csv").open("w", encoding="ascii", newline="") as output:
        writer = csv.DictWriter(output,series[0],lineterminator="\n")
        writer.writeheader()
        writer.writerows(series)
    print("DEPTH_ARCHIVES_AND_MEASURED_WINDOWS_OK", len(series))


if __name__ == "__main__":
    main()
