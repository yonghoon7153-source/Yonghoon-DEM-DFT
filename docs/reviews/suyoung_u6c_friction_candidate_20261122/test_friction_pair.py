"""Native-step four-curve and opt-in control tests using synthetic values only."""
import importlib.util
import json
import math
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("friction_pair", HERE/"friction_pair.py")
pair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pair)


def curve(samples):
    return pair.dt.Curve(tuple(float(i) for i in range(len(samples))), tuple(samples))


class FourCurves(unittest.TestCase):
    def test_if_kernel_changes_the_entire_response_identically_it_is_still_reported(self):
        old = curve([0, 1, 2])
        new = curve([0, 2, 4])
        result = pair.compare(old, old, new, new, 2.)
        self.assertTrue(result["candidate_numerical_comparison"]["exact_samples_and_same_stop"])
        stat = result["all_four_common"]["original_kernel_change"]
        self.assertEqual(stat["candidate_minus_historical_MPa"], 2.)
        self.assertEqual(result["all_four_common"]["fixed_points"][0]["status"], "REACHED")
        short = pair.dt.Curve((0., .02), (0., 1.))
        self.assertTrue(all(x["pressures_MPa"] is None for x in
                            pair.compare(short, short, short, short, .5)["all_four_common"]["fixed_points"]))

    def test_old_and_new_maxima_compared_only_on_same_support(self):
        result = pair.compare(curve([0, 3, 9, 10]), curve([0, 2, 4]),
                              curve([0, 1, 4]), curve([0, 2]), 2.)
        same = result["all_four_common"]
        self.assertEqual(same["samples"], 2)
        self.assertEqual(same["old"]["first_worst"]["original_minus_reversed_MPa"], 1.)
        self.assertEqual(same["candidate"]["first_worst"]["original_minus_reversed_MPa"], -1.)
        self.assertEqual(same["decrease_in_max_abs_MPa"], 0.)
        self.assertEqual(result["historical_pair"]["max_abs_MPa"], 5.)
        self.assertIsNone(result["candidate_pair"]["at_fixed_anchor"])

    def test_compare_signed_change_at_each_extremum(self):
        result = pair.compare(curve([0, 8, 8]), curve([0, 6, 8]),
                              curve([0, 7, 8]), curve([0, 7, 11]), 2.)
        same = result["all_four_common"]
        self.assertEqual(same["decrease_in_max_abs_MPa"], -1.)
        self.assertEqual(same["at_old_worst"]["candidate_original_minus_reversed_MPa"], 0.)
        self.assertEqual(same["at_candidate_worst"]["old_original_minus_reversed_MPa"], 0.)

    def test_float_roundoff_comparison_and_bit_equality_are_separate(self):
        old, new = curve([0, 1, 2]), curve([0, 1, 2 + 4e-15])
        eq = pair.compare(old, old, old, new, 2.)["candidate_numerical_comparison"]
        self.assertFalse(eq["exact_samples_and_same_stop"])
        self.assertTrue(eq["within_diagnostic_tolerance_and_same_stop"])
        self.assertIsNone(eq["qualification_threshold"])

    def test_equal_prefix_different_end_ineligible_for_full_equivalence(self):
        old, new = curve([0, 1, 2]), curve([0, 1])
        eq = pair.compare(old, old, old, new, 2.)["candidate_numerical_comparison"]
        self.assertEqual(eq["max_abs_on_pair_common_MPa"], 0.)
        self.assertFalse(eq["within_diagnostic_tolerance_and_same_stop"])

    def test_step_grid_must_match(self):
        a = curve([0, 1])
        b = pair.dt.Curve((0., .9), (0., 1.))
        with self.assertRaisesRegex(ValueError, "NATIVE_GRID_MISMATCH"):
            pair.compare(a, b, a, a, 1.)

    def test_wrong_mapping_and_wrong_candidate_calls_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "MAPPING"):
            pair.geometry("wrong")
        with self.assertRaisesRegex(ValueError, "PROJECTOR_CALL_COUNT"):
            pair.check_calls(0, 3)
        with self.assertRaisesRegex(ValueError, "PROJECTOR_CALL_COUNT"):
            pair.check_calls(2, 3)
        pair.check_calls(3, 3)


class Adapter(unittest.TestCase):
    def test_only_field_ids_and_hook_change_and_restore_even_after_failure(self):
        step = .00625
        width = math.sqrt(49*math.pi*.05**2/.78)
        offsets = [(i*step,j*step) for i in range(-8,9) for j in range(-8,9)
                   if (i*step)**2+(j*step)**2 <= .05**2]
        centers = [(.15+(i+.5)*width/7,.15+(j+.5)*width/7) for i in range(7) for j in range(7)]
        positions = np.array([(a+x,b+y) for a,b in centers for x,y in offsets])
        ids = np.repeat(np.arange(49,dtype=np.int64),len(offsets))
        volume = np.full(len(ids),math.pi*.05**2/len(offsets))
        def base_seed(cells):
            self.assertEqual(cells, 8)
            return positions, ids, volume
        def old_projector(*args):
            raise AssertionError("Historical contact unexpectedly invoked")
        solver = SimpleNamespace(seed=base_seed, project_contacts=old_projector)
        factory = lambda: solver
        for mapping in ("ORIGINAL","REVERSED"):
            for failure in (False, True):
                def synthetic_projection(*args):
                    self.assertEqual(args, (1,2,3,4,5,6,.5))
                    if failure:
                        raise ArithmeticError("fixture residual")
                def run_arm(arm, cells, budget, out):
                    self.assertEqual((arm,cells,budget), ("F",8,17))
                    current = driver.fixed_solver()
                    x, fields, vol = current.seed(8)
                    self.assertIs(x, positions)
                    self.assertIs(vol, volume)
                    np.testing.assert_array_equal(fields, ids if mapping == "ORIGINAL" else 48-ids)
                    current.project_contacts(1,2,3,4,5,6,.5)
                    return {"steps":1}
                driver = SimpleNamespace(fixed_solver=factory, run_arm=run_arm)
                candidate = SimpleNamespace(project_contacts=synthetic_projection)
                if failure:
                    with self.assertRaisesRegex(RuntimeError, f"F8 {mapping}, step 1"):
                        pair.integrate(driver, candidate, mapping, 17, Path("unused"))
                else:
                    result, observed, calls = pair.integrate(driver, candidate, mapping, 17, Path("unused"))
                    self.assertEqual((result["steps"],observed,calls), (1,pair.geometry(mapping),1))
                self.assertIs(solver.project_contacts, old_projector)
                self.assertIs(solver.seed, base_seed)
                self.assertIs(driver.fixed_solver, factory)

    def test_bound_receipt_rejects_wrong_arm_changed_kernel_and_altered_trace(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            kernel = folder/pair.KERNEL
            kernel.write_bytes(b"synthetic candidate")
            width, dt = .71, .02
            lines = [",".join(pair.dt.COLUMNS)]
            for i, p in enumerate((0.,.03,.13)):
                h = width-dt*i*pair.dt.SPEED
                lines.append(f"{i},{dt*i},{h},{p},{49*math.pi*.05**2/(width*h)}")
            raw = ("\n".join(lines)+"\n").encode()
            trace = folder/"trace.csv"
            trace.write_bytes(raw)
            native = dict(status="TARGET_BRACKETED",protocol=pair.dt.NATIVE, arm="F",cells=8, origin="new",
                          label="DEVELOPMENT_ONLY",setting=1,points_count=9653,steps=2,trace_sha256=pair.dt.sha(raw),
                          source_sha256={k:v for k,v in pair.dt.SOURCE.items() if k != "suyoung_u6b_dev.py"})
            pair.dt.write_json(folder/"result.json",native)
            item = pair.receipt(folder, "ORIGINAL", native, folder, 2, pair.geometry("ORIGINAL"))
            pair.dt.write_json(folder/"candidate.json",item)
            ref = dict(dt=dt, width=width, points_count=9653)
            self.assertEqual(pair.read_candidate(folder,folder,"ORIGINAL",ref)[0].p[-1],1.3)
            with self.assertRaisesRegex(ValueError,"CANDIDATE_RECEIPT_BINDING"):
                pair.read_candidate(folder,folder,"REVERSED",ref)
            kernel.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError,"CANDIDATE_RECEIPT_BINDING"):
                pair.read_candidate(folder,folder,"ORIGINAL",ref)
            trace.write_bytes(raw+b"\n")
            with self.assertRaisesRegex(ValueError,"TRACE_BINDING"):
                pair.read_candidate(folder,folder,"ORIGINAL",ref)

    def test_damaged_historical_archive_returns_incomplete_without_comparison(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            bad = folder/"old.tar.gz"
            bad.write_bytes(b"bad")
            out = folder/"partial.json"
            args = SimpleNamespace(out=out, wall=bad)
            self.assertEqual(pair.read(args),4)
            report = json.loads(out.read_bytes())
            self.assertIs(report["u6_qualified"],False)
            self.assertEqual(report["status"],"INCOMPLETE")
            self.assertNotIn("comparison",report)


if __name__ == "__main__":
    unittest.main()
