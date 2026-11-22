"""Re-read the fixed stress probe and locate each signed contribution on the wall."""
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
helper = HERE.parent / "suyoung_wall_momentum_return_20261122/read_return.py"
spec = importlib.util.spec_from_file_location("momentum_return", helper)
previous = importlib.util.module_from_spec(spec)
spec.loader.exec_module(previous)
PROBE = "fcf9fd337d57c77cb9b4f751a6b938ce60a1d9010e438026ac10ffa762104cfd"
SCREEN = "2cecf47170306fd1098cd78a050e85be275c53e87b90f9ecab87f4f12aae19b2"
SOURCE = "d7a225450f97ea7432cb4ee8d8791b0deaa33de0c51903192e1a2c9632b43179"
COLUMNS = ("yy", "yx", "unit_yy", "unit_yx")
IDENTICAL = ("momentum.json", "momentum_receipt.json", "wall_observations.json", "trace.csv", "prefix_receipt.json")


def totals(columns, indices):
    return {c: math.fsum(columns[c][i] for i in indices) for c in COLUMNS}


def localize(arm, n):
    rows = {}
    g = 10 * n
    for record in json.loads(arm):
        columns = record["projection"]
        keys = columns["keys"]
        plane = [i for i, key in enumerate(keys) if 20 * (key % (g + 1)) == 3 * g]
        field_ids = [key // (g + 1) ** 2 for key in keys]
        rows[record["step"]] = {
            "all": totals(columns, range(len(keys))),
            "plane": totals(columns, plane),
            "plane_keys": len(plane),
            "mask_keys": len(keys),
            "abs_yx_sum_MPa": math.fsum(abs(v) for v in columns["yx"]),
            "fields": {f: totals(columns, [i for i, v in enumerate(field_ids) if v == f])
                       for f in sorted(set(field_ids))},
        }
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("return-dir", "momentum", "prior", "source", "out"):
        parser.add_argument("--" + key, type=Path, required=True)
    args = parser.parse_args()
    result = previous.members(args.return_dir / "suyoung_wall_stress_probe_result.tar.gz", PROBE)
    source = previous.members(args.source, SOURCE)
    momentum = previous.members(args.momentum, previous.RESULT)
    previous.require(previous.digest(args.prior.read_bytes()) == previous.HISTORY, "prior")
    previous.require(previous.digest((args.return_dir / "screen.txt").read_bytes()) == SCREEN, "screen")
    previous.require((args.return_dir / "SHA256SUMS").read_text().splitlines() ==
                     [PROBE + "  suyoung_wall_stress_probe_result.tar.gz", SCREEN + "  screen.txt"], "manifest")
    previous.require(result["run/SOURCE_SHA256SUMS"] == source["SOURCE_SHA256SUMS"], "source manifest")
    for line in source["SHA256SUMS"].decode().splitlines():
        digest, key = line.split("  ", 1)
        previous.require(hashlib.sha256(source[key]).hexdigest() == digest, "source " + key)
    for n in (8, 16):
        for name in IDENTICAL:
            key = f"run/F{n}/{name}"
            previous.require(result[key] == momentum[key], "historical bytes " + key)

    with tempfile.TemporaryDirectory() as directory:
        scratch = Path(directory)
        for files, dest in ((source, scratch / "source"), (result, scratch)):
            for name, data in files.items():
                out = dest / name
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
        repo = scratch / "source"
        reader = repo / "docs/reviews/suyoung_wall_stress_probe_20261122/probe.py"
        replay = scratch / "reread.json"
        subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(reader), "read",
                        "--repo", str(repo), "--momentum", str(args.momentum.resolve()),
                        "--prior", str(args.prior.resolve()), "--run", str(scratch / "run"),
                        "--out", str(replay)], check=True)
        previous.require(replay.read_bytes() == result["run/summary.json"], "fixed reader replay")

    summary = json.loads(result["run/summary.json"])
    arms = {n: localize(result[f"run/F{n}/probe.json"], n) for n in (8, 16)}
    pairs = []
    for pair in summary["paired"]:
        i, j = pair["steps"]
        coarse, fine = arms[8][i], arms[16][j]
        delta = {k: coarse["all"][k] - fine["all"][k] for k in COLUMNS}
        previous.require(delta == pair["delta_F8_minus_F16"], "signed native sums")
        previous.require(coarse["fields"].keys() == fine["fields"].keys(), "same fields")
        row_gap = {k: coarse["plane"][k] - fine["plane"][k] for k in COLUMNS}
        by_field = {f: {k: coarse["fields"][f][k] - fine["fields"][f][k] for k in ("yy", "unit_yy")}
                    for f in coarse["fields"]}
        for k in ("yy", "unit_yy"):
            previous.require(math.isclose(math.fsum(v[k] for v in by_field.values()), delta[k], abs_tol=1e-12),
                             "field sum")
        pairs.append({"steps": [i, j], "u": pair["u"], "signed_delta_MPa": delta, "F8": coarse, "F16": fine,
                      "normal_pressure_ratio": coarse["all"]["yy"] / fine["all"]["yy"],
                      "uniform_compression_response_ratio": coarse["all"]["unit_yy"] / fine["all"]["unit_yy"],
                      "plane_delta_MPa": row_gap, "plane_share_native_yy": row_gap["yy"] / delta["yy"],
                      "plane_share_uniform_yy": row_gap["unit_yy"] / delta["unit_yy"],
                      "delta_by_original_field": by_field})
    report = {"scope": "development, two observed native common displacements", "return_sha256": PROBE,
              "summary_sha256": previous.digest(result["run/summary.json"]), "source_tar_sha256": SOURCE,
              "prior_momentum_sha256": previous.RESULT, "prior_prefix_sha256": previous.HISTORY,
              "identical_to_previous_by_arm": IDENTICAL, "pairs": pairs, "u6c": "HOLD", "stage3": "HOLD"}
    with args.out.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")
    print("STRESS_RETURN_VERIFIED")


if __name__ == "__main__":
    main()
