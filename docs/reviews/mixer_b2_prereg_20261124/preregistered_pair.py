"""Read B2 endpoint fractions offline after normal return, W9 and archive verification."""
import argparse
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path


U_SHA = "128d0c0dc67ead931dbc4a68ccf5c1508e7d02bcacc1db3f921010ba72dee2c2"
C_PIN = "92b185b70c12d3962340d02f915df8e37c987ea2"
C_META = "18f2e3cb3d83e6402a128acd2d0172813505fd34f1b8d17aa4067569728535eb"
C_DECK = "d36d199388243ccd630cbd346cbcdb6f37bf8bb92ae9c8f4e73e2e98597a6a3e"
CASE = "PRECAL_R1_B2_C"
STEPS = [32976*i for i in range(134, 234)]
T0 = 32976*34
METRICS = (("s1_se_clusters", "se_frac_in_clusters", -1),
           ("s2_am_se_attach", "se_attached_any_frac", 1))


def require(ok, label):
    if not ok:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fractions(block, counts):
    rows = block["frames"]
    require(block["status"] == "OK" and block["n"] == len(rows) == 100 and block["bin"] == 1
            and block["steps"] == [r["step"] for r in rows] == STEPS, "wrong native frame window")
    denominator = counts["observed_by_type"]["3"]
    require(type(denominator) is int and denominator > 0, "invalid SE count")
    result = {}
    for group, metric, _ in METRICS:
        total = 0
        for row in rows:
            require(row["n"]["SE"] == denominator, "SE count differs across native frames")
            value = row[group][metric]
            require(type(value) in (float, int) and math.isfinite(value) and 0 <= value <= 1,
                    "missing or invalid native fraction")
            count = round(value * denominator)
            require(count / denominator == value, "fraction differs from native integer-count ratio")
            if metric == "se_frac_in_clusters":
                require(count == denominator - row[group]["hist_components"]["1"], "singleton count mismatch")
            total += count
        mean = Fraction(total, 100*denominator)
        require(math.isclose(float(mean), block["mean"][metric], rel_tol=1e-14, abs_tol=1e-15),
                "observer mean differs from 100 native frames")
        result[metric] = mean
    return result


def receipt_fields(record):
    job = "369734"
    require(record["case"] == CASE and record["role"] == "C" and record["release_pin"] == C_PIN and
            record["job_id"] == record["job_end_id"] == record["scheduler"]["job_id"] == job,
            "wrong arm, release or job")
    require(record["scheduler"]["state"] == "COMPLETED" and record["scheduler"]["exit_code"] == "0:0"
            and type(record["runner_rc"]) is int and record["runner_rc"] == 0 and
            record["return_ready"] is True and record["exact_frame_names"] is True and
            record["frame_count"] == 234 and record["post_runtime_matches"] is True and
            record["post_runtime_error"] is None and record["w9"] == "LIVE_TERMINAL_MATCH",
            "terminal completion and W9 required")


def paired(u, c):
    pv = c["provenance"]
    require(c["case_id"] == pv["binding"]["case_id"] == CASE and c["status"] == "OK" and
            pv["binding"]["seed"] == 32452843 and pv["binding"]["role"] == "C", "wrong C native observation")
    require(u["case"] == "PRECAL_R1_B2_U" and u["job"] == "368758", "wrong U observation")
    modules = {Path(v["path"].replace("\\", "/")).name: v["sha256"] for v in pv["module_sha256"].values()}
    require(len(modules) == len(pv["module_sha256"]) == 9 and modules == u["source_sha256"], "observer modules")
    require(len(pv["reference_frames"]) == 1 and
            all(pv["reference_frames"][0][k] == u["e0_frame"][k] for k in ("step","sha256")), "E0 reference")
    native_inputs = pv["input_sha256"]
    paths = [Path(row["path"].replace("\\", "/")) for row in pv["frames"]]
    require(len({p.parent for p in paths}) == 1 and paths[0].parent.name == "post", "native dump directory")
    run = paths[0].parent.parent
    inputs = {Path(k.replace("\\", "/")): v for k, v in native_inputs.items()}
    require(inputs[run/"deck_meta.json"] == C_META and inputs[run/"in.mixer"] == C_DECK, "C seed/deck bytes")
    for fs in (pv["frames"], u["frames"]):
        require([f["step"] for f in fs] == [T0, *STEPS] and
                all(re.fullmatch(r"[0-9a-f]{64}", f["sha256"]) for f in fs), "native provenance window")
    require(all(p.name == f"mix_{f['step']}.liggghts" and inputs[p] == f["sha256"]
                for p,f in zip(paths, pv["frames"])), "C native frame provenance")
    a, b = [fractions(obj["contact"]["bin"], obj["counts"]) for obj in (u, c)]
    results = {}
    for _,metric,expected in METRICS:
        delta = b[metric] - a[metric]
        results[metric] = dict(U_percent=float(100*a[metric]), C_percent=float(100*b[metric]),
                               C_minus_U_percentage_points=float(100*delta), exact_fraction_delta=str(delta),
                               sign="zero" if not delta else "positive" if delta > 0 else "negative",
                               predicted_direction_observed=expected*delta > 0)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for arg in ("u_observer", "c_native_observer", "c_return_json", "new_output"):
        parser.add_argument(arg, type=Path)
    args = parser.parse_args()
    u, c, receipt = [p.read_bytes() for p in (args.u_observer, args.c_native_observer, args.c_return_json)]
    require(sha(u) == U_SHA, "original verified U observation required")
    receipt_fields(json.loads(receipt))
    results = paired(json.loads(u), json.loads(c))
    output = dict(label="DEVELOPMENT_ONLY", scope="paired contact arithmetic, 1 seed, 100 time samples",
                  archive_and_W9_evidence="verified separately before using this reader", seed=32452843,
                  sha256=dict(u=sha(u), c=sha(c), c_return=sha(receipt)), metrics=results,
                  both_directions_observed=all(r["predicted_direction_observed"] for r in results.values()))
    with args.new_output.open("x", encoding="utf8", newline="\n") as stream:
        json.dump(output, stream, indent=2, allow_nan=False)
        stream.write("\n")


if __name__ == "__main__":
    main()
