"""R2: exercise the real workbook loader and Objective on synthetic NE/PE edits.

Everything created is under a temporary directory. The reviewed checkout is
read only. No original battery data or MATLAB source is needed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                        / "work/harness-r2-target/bms-balancing")
    args = parser.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify

    with tempfile.TemporaryDirectory(prefix="bms-r2-consumed-axis-") as name:
        root = Path(name)
        subprocess.run([sys.executable, str(args.target / "matlab/tests/gen_synth_xlsx.py"),
                        str(root)], check=True, capture_output=True, text=True)
        original = verify.build(root, "GITT", "200", "Li", w_dqdv=1.0, scale_seed=0)
        file = root / "data/half_cell/GITT/200.xlsx"
        frame = pd.read_excel(file)
        old_ne = frame["NE_voltage"].copy()
        bump = np.sin(np.pi * frame["NE_capacity"].to_numpy())
        frame["NE_voltage"] = old_ne + 0.03577 * bump
        frame.to_excel(file, index=False)
        changed = verify.build(root, "GITT", "200", "Li", w_dqdv=1.0, scale_seed=0)
        grid = np.linspace(0.02, 0.98, 400)
        observed = float(np.max(np.abs(changed.half.E_NE(grid) - original.half.E_NE(grid))))
        # Match the request's 35.77 mV intervention exactly on its comparison grid.
        frame["NE_voltage"] = old_ne + (0.03577 / observed) * 0.03577 * bump
        frame.to_excel(file, index=False)
        changed = verify.build(root, "GITT", "200", "Li", w_dqdv=1.0, scale_seed=0)

        def terms(obj):
            return np.array([[obj(p), obj.rmse_pocv(p), obj.rmse_dvdq(p),
                              obj.rmse_dqdv(p, False), obj.rmse_dqdv(p, True)]
                             for p in np.asarray(verify.DD_EVAL_P)])

        before, after = terms(original), terms(changed)
        assert np.array_equal(before, after)
        assert original.scales == changed.scales
        ne_difference_mv = float(np.max(np.abs(changed.half.E_NE(grid)
                                             - original.half.E_NE(grid))) * 1000)
        assert abs(ne_difference_mv - 35.77) < 1e-9

        # Control: an edit to the actually consumed PE column reaches the objective.
        frame["PE_voltage"] += 0.02
        frame.to_excel(file, index=False)
        pe_changed = verify.build(root, "GITT", "200", "Li", w_dqdv=1.0, scale_seed=0)
        pe_difference = float(np.max(np.abs(terms(pe_changed)[:, 1] - before[:, 1])))
        assert pe_difference > 1e-6

        result = {
            "measured_NE_change_mV": ne_difference_mv,
            "NE_capacity_change_percent": 0.0,
            "parameter_points": len(verify.DD_EVAL_P),
            "terms_per_point": 5,
            "NE_change_max_objective_or_rmse_difference": float(np.max(np.abs(after-before))),
            "NE_change_scales_identical": original.scales == changed.scales,
            "PE_positive_control_shift_mV": 20.0,
            "PE_positive_control_max_rmse_pocv_difference_V": pe_difference,
        }
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
