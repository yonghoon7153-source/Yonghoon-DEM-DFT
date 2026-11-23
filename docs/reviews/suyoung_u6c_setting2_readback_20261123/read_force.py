"""Apply the unchanged U6(c) item 6 force/displacement arithmetic to selected F curves."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


SOURCE_PIN = "c858862722bf6e5eb587ccbd54e1eef7dd59aa27"
RULE_DIR = "suyoung_u6c_force_rule_20261122"
RULE = RULE_DIR + "/rule.json"
ORIGINAL = RULE_DIR + "/force_rule.py"
NATIVE = "suyoung_floor_full_20261123/full_compare.py"
GATE = "suyoung_u6a_setting2_return_20261123/verify_setting2.py"
FILES = {
    RULE: "1736322b4b2f4cef384becd97099998668137c19272e504edd951b698502a8f4",
    ORIGINAL: "145b5fe6f456e8b66c2a8cc422ff88648c82d07c4420482f06bc6da7a5b1b6db",
    "suyoung_u6c_doubling_readback_20261122/doubling.py":
        "9d664ed38a70295b9bd04ecbf5dae4ffda663c5efbc348c30a77bf6b99fa1bda",
    NATIVE: "f3eb1aa342e97e5accd9619230b695e523d9113035937daf676b29c88b498d3a",
    GATE: "d2f203e23b56fbeb1609d02f249b9bd0099d1962b2720b5b635789c83be380e3",
}


def require(ok, label):
    if not ok:
        raise ValueError(label)


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verified_sources(repo, scratch):
    for relative, expected in FILES.items():
        name = "docs/reviews/" + relative
        # Use fixed Git blobs rather than working-tree bytes. This also supports sparse checkouts.
        content = subprocess.check_output(["git", "-c", "safe.directory=" + repo.as_posix(), "-C", str(repo),
                                           "show", SOURCE_PIN + ":" + name])
        require(hashlib.sha256(content).hexdigest() == expected, "source identity " + name)
        path = scratch/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def read(directory, source):
    gate, native, rule = (load(source/name) for name in (GATE, NATIVE, ORIGINAL))
    decision = gate.evaluate(directory)
    require(decision["selected_setting"] == 2 and decision["status"] == "PASS", "F setting selection")
    contract = json.loads((source/RULE).read_bytes())
    pairs, historical, arm_hashes = {}, {}, {}
    with tarfile.open(directory/gate.ARCHIVE, "r:gz") as archive:
        for n, f in contract["required_grid_pairs_cells_per_diameter"]:
            curves, raw, recs, widths = [], [], [], []
            for grid in (n, f):
                prefix = f"run/F{grid}/"
                trace = archive.extractfile(prefix + "trace.csv").read()
                receipt = json.load(archive.extractfile(prefix + "target_receipt.json"))
                width = float(next(csv.DictReader(io.StringIO(trace.decode("ascii"))))["height"])
                u, pressure = native.read_native(trace, width, receipt["wall_speed"], receipt["dt"], receipt["status"])
                curves.append(list(zip(u, pressure, strict=True)))
                raw.append(trace)
                recs.append(receipt)
                widths.append(width)
                arm_hashes[f"F{grid}"] = {k: receipt[k] for k in ("trace_sha256", "result_sha256", "observation_sha256")}
            require(widths[0] == widths[1] and recs[0]["wall_speed"] == recs[1]["wall_speed"] and
                    recs[0]["dt"] == 2*recs[1]["dt"], "initial geometry, loading or clocks")
            name = f"F{n}_F{f}"
            pairs[name] = candidate = rule.compare(*curves)
            cross = native.compare_pair(*raw, width=widths[0], speed=recs[0]["wall_speed"],
                                        dt8=recs[0]["dt"], dt16=recs[1]["dt"],
                                        terminal8=recs[0]["status"], terminal16=recs[1]["status"])
            common = cross["common"]
            require((candidate["union_knots"], candidate["max_abs_difference_MPa"], candidate["ratio"],
                     candidate["comparison"], candidate["exceeding_knots"]) ==
                    (common["samples"], common["max_abs_difference_MPa"], common["fine_peak_ratio"],
                     common["fine_peak_comparison"], common["fine_peak_exceeding_samples"]), "reader disagreement")
            historical[name] = dict(reference_MPa=cross["fixed_reference_MPa"],
                                    ratio=common["fixed_reference_ratio"],
                                    exceeding_knots=common["fixed_reference_exceeding_samples"])
    return dict(label="DEVELOPMENT_ONLY", force_item="U6(c) item 6", selected_setting=2,
                historical_rule_scope=contract["scope"], application="2026-11-23 author direction, selected setting",
                unchanged_rule_id=contract["id"], source_pin=SOURCE_PIN, registered_pairs=pairs,
                native_curve_comparison=rule.aggregate(pairs), historical_fixed_reference_only=historical,
                sources_sha256=FILES, F_evidence_sha256=arm_hashes, F_return_sha256=decision["return_tar_sha256"],
                F_screen_sha256=decision["screen_sha256"], other_seven_items="UNASSESSED",
                full_qualification_granted=False, stage3_go=False, three_dimensional_go=False, new_model_runs=0)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("return_directory", type=Path, help="original completed setting 2 F return")
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    p.add_argument("--output", type=Path, help="publish a new receipt; default is stdout")
    args = p.parse_args()
    with tempfile.TemporaryDirectory() as temp:
        source = Path(temp)
        verified_sources(args.repo.resolve(), source)
        value = read(args.return_directory, source)
    data = json.dumps(value, ensure_ascii=True, allow_nan=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8", newline="\n") as out:
            out.write(data)
    else:
        print(data, end="")
