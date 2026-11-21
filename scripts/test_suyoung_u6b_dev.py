"""Synthetic regressions for the U6(b) development comparison."""
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
DRIVER = HERE / "suyoung_u6b_dev.py"


class DevelopmentTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(DRIVER.is_file(), "U6(b) driver is absent")
        spec = importlib.util.spec_from_file_location("dev_u6b", DRIVER)
        self.dev = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.dev)
        work = tempfile.TemporaryDirectory()
        self.addCleanup(work.cleanup)
        self.root = Path(work.name)

    def test_read_on_compression_path(self):
        rows = self.dev.pressures_at_targets([(0.78, 0.0), (.90, .5), (.95, 1.2)])
        self.assertAlmostEqual(rows["0.90"]["pressure_MPa"], .5)
        self.assertAlmostEqual(rows["0.95"]["pressure_MPa"], 1.2)
        self.assertEqual(rows["0.84"]["state"], "VALUE")

    def test_first_cap_on_same_step(self):
        rows = self.dev.pressures_at_targets([(.78, 0), (.90, .4), (.97, 3.)])
        self.assertEqual(rows["0.90"]["state"], "VALUE")
        self.assertEqual(rows["0.95"], {"state": "NOT_REACHED", "pressure_MPa": None})

    def test_post_cap_row_rejected(self):
        with self.assertRaises(ValueError):
            self.dev.pressures_at_targets([(.78, 0), (.82, 1.25), (.90, .5)])

    def test_no_log_of_noise_including_zero(self):
        rows = self.dev.pressures_at_targets([(.78, 0), (.84, 0), (.90, .008), (.95, .009)])
        self.assertEqual([v["state"] for v in rows.values()], ["NOISE", "NOISE", "VALUE"])

    def test_reject_reversed_or_nonfinite_points(self):
        for point in ((.77, .5), (.81, float("nan")), (.8, -1.)):
            with self.subTest(point=point), self.assertRaises(ValueError):
                self.dev.pressures_at_targets([(.78, 0), point])

    def test_A_with_sign_change_on_witness(self):
        got = self.dev.arm_rule([.02, 0., .04, .07])
        self.assertEqual(got["rule"], "A")
        self.assertTrue(got["suspect_asymptotic"])
        self.assertAlmostEqual(got["interval"][1], .18)

    def test_B_zero_witness_and_no_monotone_drift(self):
        self.assertEqual(self.dev.arm_rule([0., 0., .004, .005])["rule"], "B")
        self.assertEqual(self.dev.arm_rule([-.001, 0., .004, .005])["rule"], "UNCONVERGED")

    def test_large_witness_excluded_from_B(self):
        got = self.dev.arm_rule([1., 0., .005, .004])
        self.assertEqual(got["rule"], "B")
        self.assertTrue(got["bias_signal"])
        self.assertAlmostEqual(got["interval"][0], .004-.02-3*.005)

    def test_bias_and_noise_are_distinct(self):
        raw = self.dev.arm_rule([0., .12, .135, .119])
        self.assertTrue(raw["bias_signal"])
        self.assertTrue(raw["noise_signal"])
        raw = self.dev.arm_rule([0., .03, .045, .055])
        self.assertFalse(raw["bias_signal"])

    def test_S_and_F_field_identities(self):
        import numpy as np
        ids = np.array([3, 7, 7])
        self.assertEqual(self.dev.field_ids("F", ids).tolist(), [3, 7, 7])
        self.assertEqual(self.dev.field_ids("S", ids).tolist(), [0, 0, 0])
        self.assertEqual(ids.tolist(), [3, 7, 7])

    def test_arm_with_synthetic_advance_and_no_overwrite(self):
        import numpy as np
        calls = []
        def synthetic(x, v, affine, elastic, fields, volume, grid, dt, lid):
            calls.append((set(fields.tolist()), grid))
            return x, v, affine, elastic, .15
        for arm, expected in (("S", {0}), ("F", set(range(49)))):
            out = self.root / arm
            item = self.dev.run_arm(arm, 8, 15, out, advance=synthetic)
            self.assertEqual(item["status"], "TARGET_BRACKETED")
            self.assertEqual(calls[-1], (expected, 80))
            self.assertIs(self.dev.read_run(out, arm, 8)["points"]["0.84"]["pressure_MPa"], None)
            with self.assertRaises(FileExistsError):
                self.dev.run_arm(arm, 8, 15, out, advance=synthetic)

    def test_deadline_before_first_step(self):
        with patch.object(self.dev.time, "monotonic", side_effect=[0, 6, 7]):
            row = self.dev.run_arm("S", 8, 5, self.root/"S8", advance=lambda *args: self.fail("over time"))
        self.assertEqual(row["status"], "TIME_LIMIT")
        with self.assertRaises(ValueError):
            self.dev.read_run(self.root/"S8", "S", 8)

    def test_reject_incorrect_historical_trace(self):
        src = self.root/"fake.csv"
        src.write_text("synthetic trace", encoding="ascii")
        with self.assertRaises(ValueError):
            self.dev.import_trace(12, src, self.root/"F12")
        self.assertFalse((self.root/"F12").exists())

    def test_tampered_or_relabelled_trace_rejected(self):
        out = self.root/"S8"
        self.dev.run_arm("S", 8, 10, out, advance=lambda x,v,a,e,*other:(x,v,a,e,.2))
        with self.assertRaises(ValueError):
            self.dev.read_run(out, "F", 8)
        path = out/"trace.csv"
        path.write_bytes(path.read_bytes()+b"\n")
        with self.assertRaises(ValueError):
            self.dev.read_run(out, "S", 8)

    def test_summary_requires_all_arms_for_common_points(self):
        values = {}
        for arm in ("S","F"):
            for cells in (8,12,16,24):
                values[(arm,cells)] = self.dev.pressures_at_targets([(.78,0),(.96,.50 if arm=="S" else .25)])
        out = self.dev.compare(values)
        self.assertEqual(out["status"], "DEVELOPMENT_READBACK")
        bounds = out["targets"]["0.90"]["ln_S_over_F_interval_report_only"]
        self.assertAlmostEqual(bounds[0], math.log(2.)-.04)
        self.assertAlmostEqual(bounds[1], math.log(2.)+.04)
        self.assertFalse(out["u6_qualified"])
        with self.assertRaises(ValueError):
            self.dev.compare(dict(list(values.items())[:-1]))

    def test_no_reachable_common_target_and_no_extrapolation(self):
        values = {(a,c): self.dev.pressures_at_targets([(.78,0),(.82,1.2)]) for a in ("S","F") for c in (8,12,16,24)}
        got = self.dev.compare(values)
        self.assertEqual(got["status"], "NO_COMMON_TARGET")
        for point in got["targets"].values():
            self.assertIsNone(point["ln_S_over_F_interval_report_only"])

    def test_noise_kept_and_no_ratio_available(self):
        values = {(a,c): self.dev.pressures_at_targets([(.78,0),(.96,.004)]) for a in ("S","F") for c in (8,12,16,24)}
        got = self.dev.compare(values)
        self.assertEqual(got["status"], "NO_ABOVE_NOISE_SET")
        self.assertIsNone(got["targets"]["0.84"]["ln_S_over_F_interval_report_only"])

    def test_one_noise_arm_has_one_sided_ratio_and_no_bias(self):
        cases = {(a,c): self.dev.pressures_at_targets([(.78,0),(.96,.6 if a=="S" else .004)]) for a in ("S","F") for c in (8,12,16,24)}
        item = self.dev.compare(cases)["targets"]["0.90"]
        ratio = item["ln_S_over_F_interval_report_only"]
        self.assertIsInstance(ratio, list, "expected one-sided interval")
        self.assertAlmostEqual(ratio[0], item["arms"]["S"]["resolution"]["interval"][0]-math.log(.008))
        self.assertIsNone(ratio[1])

    def test_partial_panel_saved_when_an_arm_is_missing(self):
        path = self.root/"partial.json"
        self.assertEqual(self.dev.main(["summarize","--runs",str(self.root),"--out",str(path)]), 4)
        restored = json.loads(path.read_bytes())
        self.assertEqual(restored["status"], "INCOMPLETE_INPUT")
        self.assertEqual(len(restored["unavailable"]), 8)
        self.assertIsNone(restored["targets"]["0.84"]["ln_S_over_F_interval_report_only"])
        self.assertIsNone(restored["targets"]["0.84"]["arms"]["S"]["resolution"])

if __name__ == "__main__":
    unittest.main()
