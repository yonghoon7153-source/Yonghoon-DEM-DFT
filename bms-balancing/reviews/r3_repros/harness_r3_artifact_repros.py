"""R3 numeric artifact audit: independently compare recorded values and test C21.

All mutations are to temporary copies of numeric review fixtures. No reviewed
source, original measurement, or remote state is changed.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
from unittest.mock import patch

import numpy as np


def load_tests(target):
    spec = importlib.util.spec_from_file_location("r3_review_tests", target / "tests/test_review_findings.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stored_pairs(target, verify):
    rows = []
    for path in sorted((target / "out/recompare").glob("dd_eval_*_r2.csv")):
        ma, mr, mh = verify.read_dd_eval_csv(path)
        pa, pr, ph = verify.read_dd_eval_csv(path.with_suffix(".txt"))
        assert len(ma) == len(pa) == 16
        assert len(mr) == len(pr) == 8 and mh == ph
        matlab, python = np.array(mr), np.array(pr)
        assert np.isfinite(matlab).all() and np.isfinite(python).all()
        assert np.array_equal(matlab[:, :5], python[:, :5])
        metric_diff = np.abs(matlab[:, 5:] - python[:, 5:]) / np.maximum(np.abs(python[:, 5:]), 1e-30)
        anchor_diff = max(abs(ma[key]-pa[key])/max(abs(pa[key]), 1e-30) for key in pa)
        assert metric_diff.max() < 1e-9 and anchor_diff < 1e-9
        rows.append({"file": path.name, "anchors_checked": len(ma), "metrics_checked": int(metric_diff.size),
                     "max_anchor_relative_difference": anchor_diff,
                     "max_metric_relative_difference": float(metric_diff.max())})
    assert len(rows) == 4
    return rows


def c21_unbound_numbers(target, tests, verify):
    with tempfile.TemporaryDirectory(prefix="harness-r3-c21-") as name:
        root = Path(name)
        shutil.copytree(target / "out/recompare", root / "out/recompare")
        shutil.copyfile(target / "FINDINGS.md", root / "FINDINGS.md")
        check = tests.test_section_1_8_192_values_are_backed_by_committed_recompare_artifacts
        with patch.object(tests, "ROOT", root):
            check()
            file = root / "out/recompare/dd_eval_pristine_Li_r2.csv"
            before = file.read_text(encoding="utf-8")
            lines = before.splitlines()
            header_index = next(i for i, line in enumerate(lines) if line.startswith("a_PE,"))
            record = lines[header_index + 1].split(",")
            original = float(record[5])
            record[5] = "9.0"
            lines[header_index + 1] = ",".join(record)
            file.write_text("\n".join(lines) + "\n", encoding="utf-8")
            check()  # The current test passes despite the changed numeric evidence.
            _, python_rows, _ = verify.read_dd_eval_csv(file.with_suffix(".txt"))
            actual_python = float(python_rows[0][5])
            assert abs(9.0 - actual_python) > 8
            # Positive control: the same test does reject changed verdict wording.
            transcript = file.with_suffix(".txt")
            text = transcript.read_text(encoding="utf-8")
            transcript.write_text(text.replace("앵커 16개가 전부 맞고", "검증 결과 없음"), encoding="utf-8")
            caught = False
            try:
                check()
            except AssertionError:
                caught = True
            assert caught
            return {"valid_original_passed": True, "csv_only_change_still_passed": True,
                    "original_rmse": original, "altered_csv_rmse": 9.0,
                    "unchanged_transcript_python_rmse": actual_python,
                    "actual_relative_difference": abs(9.0-actual_python)/abs(actual_python),
                    "verdict_wording_positive_control_rejected": caught}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, default=Path(__file__).resolve().parents[1]
                        / "work/harness-r3-target/bms-balancing")
    args = parser.parse_args()
    sys.path.insert(0, str(args.target))
    from bms_balancing import verify
    tests = load_tests(args.target)
    result = {"stored_192_values_independent_recalculation": stored_pairs(args.target, verify),
              "C21_regression_does_not_bind_csv_values_to_transcript": c21_unbound_numbers(args.target, tests, verify)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
