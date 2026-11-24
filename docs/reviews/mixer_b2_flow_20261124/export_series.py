"""Export measured frame-level observations and sensitivity summaries for the report."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np


def describe(values):
    finite = [v for v in values if v is not None]
    if not finite:
        return {"frames": 0, "median": None, "q25": None, "q75": None}
    lower, median, upper = (float(v) for v in np.quantile(finite, [.25, .5, .75]))
    return {"frames": len(finite), "median": median, "q25": lower, "q75": upper}


def export(records_path, report_dir):
    records = [json.loads(line) for line in records_path.read_text(encoding="utf-8").splitlines()]
    second = [r for r in records if r["phase"] == "TURN_1_TO_2"]
    if len(records) != 201 or len(second) != 100:
        raise ValueError("Expected the complete B2-U development readback")
    cols = ("index", "step", "turns", "phase", "theta_signed_deg", "theta_abs_deg", "delta_over_R",
            "delta_mm", "layer_status", "surface_rms_over_R", "center_slip_fraction")
    with (report_dir / "flow_by_frame.csv").open("w", encoding="ascii", newline="") as out:
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(cols)
        for r in records:
            writer.writerow([r["frame_index"], r["step"], r["turns_since_rotation"], r["phase"],
                             r["theta_signed_deg"], r["theta_deg"], r["delta_over_R"],
                             None if r["delta_m"] is None else 1000 * r["delta_m"], r["layer_status"],
                             r["surface_rms_over_R"], r["wall_frame_kinematics"]["azimuthal_slip_fraction"]])
    sensitivity = {
        "window": "1 <= completed turns < 2", "frames": len(second),
        "layer_status_counts": dict(Counter(r["layer_status"] for r in second)),
        "thickness_by_relative_speed_cutoff": {
            str(c): describe(v["delta_over_R"] for r in second for v in r["layer_sensitivity"] if v["cutoff"] == c)
            for c in (.025, .05, .10)},
        "absolute_angle_by_surface_quantile": {
            q: describe(None if r["surface_q_sensitivity_deg"][q] is None else abs(r["surface_q_sensitivity_deg"][q])
                        for r in second) for q in ("0.985", "0.99", "0.995")},
        "surface_rms_over_R": describe(r["surface_rms_over_R"] for r in second),
        "steady_window_is_independent_seeds": False}
    (report_dir / "sensitivity.json").write_bytes((json.dumps(sensitivity, indent=2) + "\n").encode())


if __name__ == "__main__":
    export(Path(sys.argv[1]), Path(sys.argv[2]))
