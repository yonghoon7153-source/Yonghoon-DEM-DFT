"""Replay the registered U6(a) endpoint from the author's four native F curves."""

import argparse
import csv
import hashlib
import io
import json
import math
import tarfile
from pathlib import Path


RELEASE = "eb3d7cc5520e46cc8ce50f2c821c9de1c99b7112"
ARCHIVE = "suyoung_u6a_setting2_result.tar.gz"
ARCHIVE_HASH = "882c078ba22efab1699773b1c657996933aa2b87b34c8058c62a6a5860f8a0af"
SCREEN_HASH = "711488b61bf077172335d60de019ca06f7004de4a118f8c15d70268c84b6758c"
SOURCE_HASH = "7d698c085e250be40fd7d2bfdad7ae84233ddaa847bed4939d69d0ac343834b3"
RULE_HASH = "512fa5cbad8319cf0cff0ef2f800ad5cb00f91cdf8ce806ee6768fd3742dac7c"
TARGET_E = 0.12  # The native pressure is in units of 10 MPa.
BAND = 0.005
CELLS = (8, 12, 16, 24)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def arm_readback(files, summary, cells, clock):
    prefix = f"run/F{cells}/"
    receipt = json.loads(files[prefix + "target_receipt.json"])
    raw = files[prefix + "trace.csv"]
    result_raw = files[prefix + "result.json"]
    observation_raw = files[prefix + "observation.json"]
    result = json.loads(result_raw)
    obs = json.loads(observation_raw)
    require(receipt == summary["arms"][str(cells)], "summary/arm receipt mismatch")
    require(receipt["trace_sha256"] == result["trace_sha256"] == digest(raw) and
            receipt["observation_sha256"] == digest(observation_raw) and
            receipt["result_sha256"] == digest(result_raw), "native files/receipt mismatch")
    require(result["cells"] == obs["cells"] == receipt["cells"] == cells and
            obs["identity"]["release"] == receipt["release"] == RELEASE and
            result["arm"] == "F" and result["setting"] == 2 and
            result["status"] == receipt["status"] == "TARGET_BRACKETED" and
            obs["gap"]["cell_size_gap_correction"] is True and
            obs["gap"]["distance_based_contact_detection"] is False and
            obs["interbody_calls"] == obs["gap"]["calls"] == result["steps"], "arm identity/setting mismatch")
    rows = list(csv.DictReader(io.StringIO(raw.decode("ascii"))))
    steps = result["steps"]
    require(len(rows) == steps + 1 and steps > 0, "incomplete trace")
    height = [float(row["height"]) for row in rows]
    pressure = [float(row["bottom_pressure_E"]) for row in rows]
    area_per_width = height[0] * float(rows[0]["phi_m"])
    for i, row in enumerate(rows):
        require(int(row["step"]) == i and math.isfinite(height[i]) and height[i] > 0 and
                math.isfinite(pressure[i]) and
                math.isclose(float(row["phi_m"]) * height[i], area_per_width, rel_tol=1e-12),
                "invalid sample or changing reference area")
    require(all(p < TARGET_E for p in pressure[:-1]) and pressure[-1] >= TARGET_E,
            "first target crossing must end the trace")
    lower, upper = pressure[-2:]
    target_height = height[-2] + (height[-1] - height[-2]) * (TARGET_E - lower) / (upper - lower)
    phi = area_per_width / target_height
    require(math.isclose(phi, receipt["phi_m"], rel_tol=2e-14) and
            receipt["bracket_steps"] == [steps-1, steps] and
            all(math.isclose(10*p, q, rel_tol=1e-14) for p, q in
                zip((lower, upper), receipt["bracket_pressure_MPa"], strict=True)), "interpolation mismatch")
    require(clock["process_rc"] == "0" and clock["watchdog_status"] == "none" and
            0 <= result["elapsed_s"] == receipt["elapsed_seconds"] <= result["budget_s"], "arm timing mismatch")
    return dict(phi_m_at_target=phi, height_at_target=target_height, reference_area=area_per_width*height[0],
                box_area_at_target=height[0]*target_height, pressure_bracket_MPa=[10*lower,10*upper],
                step_bracket=[steps-1,steps], elapsed_seconds=result["elapsed_s"],
                operator_elapsed_seconds=int(clock["elapsed_s"]), budget_seconds=result["budget_s"],
                max_floor_penetration_code=obs["floor"]["max_penetration"], trace_sha256=digest(raw))


def evaluate(directory):
    raw = (directory/ARCHIVE).read_bytes()
    screen = (directory/"screen.txt").read_bytes()
    lines = (directory/"SHA256SUMS").read_text(encoding="ascii").splitlines()
    require(sorted(lines) == sorted([f"{ARCHIVE_HASH}  {ARCHIVE}", f"{SCREEN_HASH}  screen.txt"]) and
            digest(raw) == ARCHIVE_HASH and digest(screen) == SCREEN_HASH, "external return SHA256")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        members = archive.getmembers()
        require(len({m.name for m in members}) == len(members) and all(m.isfile() or m.isdir() for m in members),
                "unexpected or duplicate archive entry")
        files = {m.name: archive.extractfile(m).read() for m in members if m.isfile()}
    require(files["run/screen.txt"] == screen and files["run/RELEASE"].decode("ascii").strip() == RELEASE and
            digest(files["run/SOURCE_SHA256SUMS"]) == SOURCE_HASH, "pinned run/source identity")
    summary = json.loads(files["run/summary.json"])
    require(summary["gate"] == "U6(a)" and summary["release"] == RELEASE and
            summary["source_manifest_sha256"] == SOURCE_HASH and summary["registered_reader_sha256"] == RULE_HASH and
            summary["label"] == "DEVELOPMENT_ONLY" and summary["setting"] == 2 and
            summary["gap_correction"] is True and summary["distance_filter"] is False and
            all(summary[key] is False for key in ("u6_qualified", "stage3_go", "three_dimensional_go")),
            "gate provenance or downstream status mismatch")
    clocks = list(csv.DictReader(io.StringIO(files["run/arm_status.tsv"].decode("ascii")), delimiter="\t"))
    require(tuple(int(row["grid"]) for row in clocks) == CELLS and b"AUTOMATIC_RETRIES=0" in screen.splitlines(),
            "wrong grids or retry contract")
    arms = {n: arm_readback(files, summary, n, clock) for n, clock in zip(CELLS, clocks, strict=True)}
    delta = abs(arms[12]["phi_m_at_target"] - arms[16]["phi_m_at_target"])
    passed = delta <= BAND
    assessment = "PASS" if passed else "FAIL"
    require(math.isclose(delta, summary["absolute_delta"], abs_tol=2e-14, rel_tol=0) and
            summary["assessment"] == assessment and summary["selected_setting"] == (2 if passed else None) and
            summary["threshold"] == BAND and summary["timeouts_this_return"] == 0, "gate summary mismatch")
    return dict(label=summary["label"], setting=2, gate="U6(a)", grid_cells=[12,16], arms=arms,
                status=assessment, absolute_delta=delta, threshold=BAND, margin=BAND-delta,
                selected_setting=summary["selected_setting"], release=RELEASE,
                source_manifest_sha256=SOURCE_HASH, registered_reader_sha256=RULE_HASH,
                return_tar_sha256=ARCHIVE_HASH, screen_sha256=SCREEN_HASH, registered_target_MPa=10*TARGET_E,
                new_model_runs=0, timeouts_this_return=0, automatic_retries=0,
                seconds_total=sum(a["elapsed_seconds"] for a in arms.values()),
                operator_seconds_total=sum(a["operator_elapsed_seconds"] for a in arms.values()),
                u6_qualified=False, stage3_go=False, three_dimensional_go=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("return_directory", type=Path)
    parser.add_argument("--output", type=Path, help="write a new JSON receipt, otherwise print it")
    args = parser.parse_args()
    output = json.dumps(evaluate(args.return_directory), indent=2, allow_nan=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="ascii", newline="\n") as stream:
            stream.write(output)
    else:
        print(output, end="")
