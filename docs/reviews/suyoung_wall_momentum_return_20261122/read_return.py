"""Re-read the author's fixed lower-wall return and localize its stress contribution."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


RESULT = "bd50c34c882866a39c5a94a511b855017cff3c5921437e60151074ed473bf77b"
SCREEN = "b5c01b2222260ac21b82b385439dec6fa4ddf4c368db77a8fae5e03c2da673df"
HISTORY = "0d415250759821b9db816e6a13d43ca190e983a7389914c5c3357b697399a5ae"
SOURCE = "5f2e87b77aa02ce02854cd2903e2562044ab4527a293c34a292fe14c6f7c8888"
WIDTH = 0.7024180763115129


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def members(path, expected):
    require(digest(path.read_bytes()) == expected, "archive identity " + path.name)
    files = {}
    with tarfile.open(path, "r:gz") as archive:
        for member in archive.getmembers():
            parts = member.name.split("/")
            require(not any(p in ("", ".", "..") for p in parts)
                    and ":" not in member.name and "\\" not in member.name, "member path")
            if member.isdir():
                continue
            require(member.isreg() and member.name not in files, "member type or duplicate")
            files[member.name] = archive.extractfile(member).read()
    return files


def spatial_sample(record, dt):
    mask = record["mask"]
    grid = mask["grid"]
    # y = 0.15 is an actual row at both resolutions.
    require(grid * 3 % 20 == 0, "shared wall row")
    field_stride = (grid + 1) ** 2
    factor = -10.0 / (WIDTH * dt)
    entries = list(zip(mask["keys"], mask["stress"], strict=True))
    wall_entries = [(key, value) for key, value in entries if key % (grid + 1) == grid * 3 // 20]
    fields = sorted({key // field_stride for key, _ in entries})
    return {
        "wall_row_count": len(wall_entries),
        "stress_MPa": math.fsum(value for _, value in entries) * factor,
        "wall_row_stress_MPa": math.fsum(value for _, value in wall_entries) * factor,
        "stress_by_id_MPa": {
            field: math.fsum(value for key, value in entries if key // field_stride == field) * factor
            for field in fields
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--return-dir", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    source = members(args.source, SOURCE)
    history = members(args.history, HISTORY)
    result = members(args.return_dir / "suyoung_wall_momentum_result.tar.gz", RESULT)
    screen = (args.return_dir / "screen.txt").read_bytes()
    require(digest(screen) == SCREEN, "outer screen")
    require((args.return_dir / "SHA256SUMS").read_text().splitlines() == [
        RESULT + "  suyoung_wall_momentum_result.tar.gz", SCREEN + "  screen.txt"], "outer manifest")
    require(source["SOURCE_SHA256SUMS"] == result["run/SOURCE_SHA256SUMS"], "source list")
    for line in source["SHA256SUMS"].decode().splitlines():
        expected, name = line.split("  ", 1)
        require(expected == digest(source[name]), "source " + name)
    for n in (8, 16):
        for name in ("trace.csv", "wall_observations.json", "prefix_receipt.json"):
            key = f"run/F{n}/{name}"
            require(result[key] == history[key], "historical bytes " + key)
    # The archived 'read' subcommand consumes arrays only. The 'arm' entry point is never invoked.
    with tempfile.TemporaryDirectory() as folder:
        scratch = Path(folder)
        for files, root in ((result, scratch), (source, scratch / "src")):
            for name, data in files.items():
                path = root / name
                path.parent.mkdir(exist_ok=True, parents=True)
                path.write_bytes(data)
        reader = scratch / "src/docs/reviews/suyoung_wall_momentum_20261122/observe_momentum.py"
        replay = scratch / "replay.json"
        subprocess.run([sys.executable, "-I", "-X", "utf8", "-B", str(reader), "read",
                        "--repo", str(scratch / "src"), "--prior", str(args.history.resolve()),
                        "--run", str(scratch / "run"), "--out", str(replay)], check=True)
        require(replay.read_bytes() == result["run/summary.json"], "summary bytes")

    summary = json.loads(result["run/summary.json"])
    spatial = {}
    dt_by_arm = {}
    for cells in (8, 16):
        dt = json.loads(result[f"run/F{cells}/prefix_receipt.json"])["dt"]
        dt_by_arm[cells] = dt
        for record in json.loads(result[f"run/F{cells}/momentum.json"]):
            spatial[cells, record["step"]] = spatial_sample(record, dt)
    pairs = []
    for row in summary["paired"]:
        coarse, fine = row["steps"]
        a, b = spatial[8, coarse], spatial[16, fine]
        delta = row["signed_pre_delta_MPa"]
        stress_gap = delta["stress"]
        require(abs((a["stress_MPa"] - b["stress_MPa"]) - stress_gap) < 1e-12, "stress gap")
        require(a["stress_by_id_MPa"].keys() == b["stress_by_id_MPa"].keys(), "field membership")
        by_id = {i: x - b["stress_by_id_MPa"][i] for i, x in a["stress_by_id_MPa"].items()}
        row_gap = a["wall_row_stress_MPa"] - b["wall_row_stress_MPa"]
        require(abs(math.fsum(by_id.values()) - stress_gap) < 1e-12, "field sum")
        mass_rates = []
        speeds = []
        for cells, step in ((8, coarse), (16, fine)):
            pre = summary["samples"][str(cells)][str(step)]["pre"]
            mass_rates.append(pre["M"] / dt_by_arm[cells])
            speeds.append(pre["mean_down"])
        mass_contribution = (10 / WIDTH) * (mass_rates[0] - mass_rates[1]) * math.fsum(speeds) / 2
        speed_contribution = (10 / WIDTH) * (speeds[0] - speeds[1]) * math.fsum(mass_rates) / 2
        require(abs(mass_contribution + speed_contribution - math.fsum(delta.values())) < 1e-12,
                "symmetric mass and speed split")
        pairs.append({
            "steps": row["steps"], "pre_delta_MPa": delta,
            "pre_gap_MPa": math.fsum(delta.values()), "total_gap_MPa": row["native_total_delta_MPa"],
            "second_wall_gap_MPa": row["signed_post_delta_MPa"],
            "symmetric_mass_rate_MPa": mass_contribution, "symmetric_mean_speed_MPa": speed_contribution,
            "mass_share_of_pre_gap": mass_contribution / math.fsum(delta.values()),
            "speed_share_of_pre_gap": speed_contribution / math.fsum(delta.values()),
            "stress_share_of_pre_gap": stress_gap / math.fsum(delta.values()),
            "dominance_ratio": row["description"]["dominance_ratio"],
            "cancellation_ratio": row["description"]["cancellation_ratio"],
            "common_wall_row_y": 0.15, "row_counts": [a["wall_row_count"], b["wall_row_count"]],
            "stress_gap_on_wall_row_MPa": row_gap, "wall_row_share_of_stress_gap": row_gap / stress_gap,
            "stress_gap_by_field_MPa": by_id,
            "largest_field_share_of_stress_gap": max(by_id.values()) / stress_gap,
        })
    report = {
        "development_only": True, "qualification": "HOLD", "stage3": "HOLD",
        "return_sha256": RESULT, "screen_sha256": SCREEN, "prior_sha256": HISTORY,
        "frozen_source_tar_sha256": SOURCE, "replayed_summary_sha256": digest(result["run/summary.json"]),
        "byte_identical_to_history": ["trace.csv", "wall_observations.json", "prefix_receipt.json"],
        "F8_prefix_steps": 270, "F16_prefix_steps": 540, "first_crossing": summary["first_crossing"],
        "prespecified_direction": summary["descriptive_direction"], "pairs": pairs,
        "posthoc_localization": "common wall row and original field IDs",
    }
    with args.out.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        handle.write("\n")
    print("MOMENTUM_RETURN_VERIFIED", report["prespecified_direction"])


if __name__ == "__main__":
    main()
