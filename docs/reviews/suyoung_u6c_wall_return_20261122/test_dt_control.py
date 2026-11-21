import dataclasses
import json
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dt_control as ctl


class ControlTests(unittest.TestCase):
    def setUp(self):
        self.c = ctl.Curve((0., 1., 2.), (0., 4., 5.))
        self.f = ctl.Curve((0., 1., 2., 3.), (0., 1., 3., 6.))
        self.h = ctl.Curve((0., .5, 1.5, 2.5), (0., 1., 3., 5.))

    def test_signed_anchored_identity(self):
        report = ctl.compare(self.c, self.f, self.h)
        self.assertEqual(report["prior_peak_gap_u"], 1.)
        self.assertEqual(report["at_prior_peak"]["signed_gaps_MPa"], {
            "original_F8_minus_F16":3., "F8_minus_F8_half_dt":2.,
            "F8_half_dt_minus_F16":1.})
        self.assertEqual(report["common_end_u"], 2.)
        self.assertEqual(report["common_knots"], 5)

    def test_early_stop_does_not_extrapolate(self):
        short = ctl.Curve((0., .5), (0., 1.))
        report = ctl.compare(self.c, self.f, short)
        self.assertIsNone(report["at_prior_peak"])
        self.assertEqual(report["prior_peak_coverage"], "NOT_REACHED")
        self.assertEqual(report["common_end_u"], .5)
        self.assertEqual(report["common_knots"], 2)
        overlap = report["at_largest_original_gap_on_common_support"]
        self.assertEqual(overlap["u"], .5)
        self.assertEqual(overlap["signed_gaps_MPa"], {
            "original_F8_minus_F16":1.5, "F8_minus_F8_half_dt":1.,
            "F8_half_dt_minus_F16":.5})
        self.assertEqual(report["prior_peak_gap_u"], 1.)

    def test_cancellation_at_anchor(self):
        high = dataclasses.replace(self.h, p=(0., 3., 7., 8.))
        gaps = ctl.compare(self.c, self.f, high)["at_prior_peak"]["signed_gaps_MPa"]
        self.assertLess(gaps["F8_minus_F8_half_dt"], 0.)
        self.assertEqual(gaps["F8_half_dt_minus_F16"], 4.)

    def test_extrema_are_taken_over_all_three_native_knot_sets(self):
        spike = ctl.Curve((0., .5, 2.), (0., 16., 4.))
        result = ctl.compare(self.c, self.f, spike)["common_max_abs_gap_MPa"]
        self.assertEqual(result["F8_half_dt_minus_F16"], 15.5)
        self.assertEqual(result["F8_minus_F8_half_dt"], 14.)

    def test_invalid_trace_and_late_target(self):
        from math import pi
        width, dt, speed = 1., .1, .2
        def sample(press):
            lines = [",".join(ctl.COLUMNS)]
            for i, p in enumerate(press):
                h = width - dt*i*speed
                lines.append(f"{i},{i*dt},{h},{p},{49*pi*.05**2/(width*h)}")
            return ("\n".join(lines)+"\n").encode()
        self.assertEqual(ctl.parse_curve(sample([0., .03, .12]), 2, dt, width, speed).p[-1], 1.2)
        for bad in (sample([0., .2, .22]), sample([0., .02, .04]), sample([0., float("nan"), .15])):
            with self.assertRaises(ValueError):
                ctl.parse_curve(bad, 2, dt, width, speed)

    def test_time_step_restored_on_failure(self):
        solver = SimpleNamespace()
        def original_dt(s, c):
            return 2./c
        def run(arm, cells, budget, out):
            self.assertEqual((arm, cells), ("F", 8))
            self.assertEqual(driver.step_size(solver, cells), original_dt(solver, 16))
            raise RuntimeError("test")
        driver = SimpleNamespace(step_size=original_dt, run_arm=run)
        with self.assertRaises(RuntimeError):
            ctl.integrate(driver, 2, Path("unused"))
        self.assertIs(driver.step_size, original_dt)

    def test_timeout_is_partial_and_no_retry(self):
        calls = []
        def run(arm, cells, budget, out):
            calls.append((arm, cells, budget))
            return {"status":"TIME_LIMIT"}
        driver = SimpleNamespace(step_size=lambda s,c: 2./c, run_arm=run)
        self.assertEqual(ctl.integrate(driver, 1, Path("unused"))["status"], "TIME_LIMIT")
        self.assertEqual(calls, [("F",8,1)])
        with self.assertRaisesRegex(ValueError, "INCOMPLETE"):
            ctl.check_native({"status":"TIME_LIMIT"}, {}, b"", 1)

    def test_missing_inputs_yield_partial_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            out = path / "summary.json"
            self.assertEqual(ctl.read_command(path/"missing.tar.gz", path/"partial", out), 4)
            report = json.loads(out.read_bytes())
            self.assertEqual(report["status"], "INCOMPLETE")
            self.assertFalse(report["u6_qualified"])
            self.assertNotIn("comparison", report)
            with self.assertRaises(FileExistsError):
                ctl.read_command(path/"missing.tar.gz", path/"partial", out)

    def make_synthetic_arm(self, arm):
        from math import pi
        # Invented same-step traces, not a solver run.
        width, dt, n = 1., .5, 2
        def trace(press):
            rows = [",".join(ctl.COLUMNS)]
            for i, p in enumerate(press):
                h = width-dt*i*ctl.SPEED
                rows.append(f"{i},{i*dt},{h},{p},{49*pi*.05**2/(width*h)}")
            return ("\n".join(rows)+"\n").encode()
        fine = ctl.parse_curve(trace([0.,.025,.13]), n, dt, width, ctl.SPEED)
        coarse = ctl.Curve((0., fine.u[-1]), (0., 1.9))
        data = trace([0.,.04,.125])
        (arm/"trace.csv").write_bytes(data)
        digest = ctl.sha(data)
        result = {"protocol":ctl.NATIVE,"label":"DEVELOPMENT_ONLY","setting":1,"arm":"F",
                  "cells":8,"origin":"new","points_count":48,"steps":n,"status":"TARGET_BRACKETED",
                  "trace_sha256":digest,"source_sha256":{k:v for k,v in ctl.SOURCE.items() if k!="suyoung_u6b_dev.py"}}
        ctl.write_json(arm/"result.json",result)
        receipt = {"protocol":ctl.CONTROL,"label":"DEVELOPMENT_ONLY","arm":"F","cells":8,
                   "native_dt_multiplier":.5,"status":"TARGET_BRACKETED","only_changed_parameter":"time_step",
                   "u6_qualified":False,"source_sha256":ctl.SOURCE,"tool_sha256":ctl.sha(Path(ctl.__file__).read_bytes()),
                   "trace_sha256":digest,"native_result_sha256":ctl.sha((arm/"result.json").read_bytes())}
        ctl.write_json(arm/"dt_control.json",receipt)
        historical = ctl.compare(coarse,fine,fine)
        return {8:coarse,16:fine}, {8:{"points_count":48,"width":width},16:{"dt":dt}}, {
            "at_first_worst_total_gap":{"u":historical["prior_peak_gap_u"]},
            "maximum_absolute_total_gap_MPa":historical["prior_peak_gap_MPa"]}

    def test_complete_synthetic_read_and_no_promotion(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            old = self.make_synthetic_arm(path)
            with patch.object(ctl,"load_prior",return_value=old):
                self.assertEqual(ctl.read_command(path/"prior",path,path/"summary"),0)
            result = json.loads((path/"summary").read_bytes())
            self.assertEqual(result["status"], "DEVELOPMENT_DT_SENSITIVITY")
            self.assertEqual(result["comparison"]["prior_peak_coverage"], "REACHED")
            self.assertFalse(result["stage3_go"] or result["u6_qualified"])

    def test_tampered_trace_blocked_before_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            old = self.make_synthetic_arm(path)
            with (path/"trace.csv").open("ab") as stream:
                stream.write(b"\n")
            with patch.object(ctl,"load_prior",return_value=old):
                self.assertEqual(ctl.read_command(path/"prior",path,path/"summary"),4)
            result = json.loads((path/"summary").read_bytes())
            self.assertEqual(result["issue"], "CONTROL_TRACE_BINDING")
            self.assertNotIn("comparison", result)


if __name__ == "__main__":
    unittest.main()
