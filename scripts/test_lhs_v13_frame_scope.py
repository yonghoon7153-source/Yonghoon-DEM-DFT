"""Check the release README with an empty synthetic table and fit."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lhs_release_build as release


def synthetic_context(stage):
    model = {
        "params": {"a": 0, "alpha": 0, "beta": 0}, "se": {}, "by_dataset": {},
        "r2": None, "loocv_r2": None, "resid_sd": None,
    }
    fit = {
        "target": "synthetic", "phi_eff": "synthetic", "n_fit": 0,
        "n_fit_by_dataset": {}, "excluded": {}, "caveats": [],
        "constants": {key: 0 for key in ("phi_c_P", "phi_c_S", "delta",
                                          "r_cut_um", "gate_exponent")},
        "fits": {"locked": model, "free": model},
    }
    return {
        "date": "fixture", "dry_run": False, "pre": "", "stage": stage,
        "fit": {"summary": fit}, "datasets": ["lhs"], "hrows": {"lhs": []},
        "gens": {"lhs": "g2"}, "hand": {"lhs": ["synthetic.csv"]},
        "manifest": {}, "codex_verdict": "fixture", "tau_reread": "fixture",
        "press_ok": False, "missing": {}, "tables": {"lhs": ([], [])},
        "by_ds": {"lhs": ([], [])}, "h12": False, "warnings": [],
    }


class FrameScopeTests(unittest.TestCase):
    def setUp(self):
        with tempfile.TemporaryDirectory() as empty_stage:
            self.readme = release._v13_readme(synthetic_context(empty_stage))

    def test_reader_sees_frame_and_intended_use_before_tables(self):
        intro = self.readme.split("## 외부 검토", 1)[0]
        self.assertTrue("탈압 전 값" in intro and "모델 내부 ML 기술자" in intro)

    def test_copyable_ml_prompt_stands_alone(self):
        prompt = self.readme.split("## 9.", 1)[1].split("## 10.", 1)[0]
        self.assertTrue("탈압 전" in prompt and "모델 내부 ML 기술자" in prompt)


if __name__ == "__main__":
    unittest.main()
