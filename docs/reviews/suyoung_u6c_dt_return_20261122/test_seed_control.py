from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seed_control as sc


class SeedControlTests(unittest.TestCase):
    def setUp(self):
        curve = sc.dt.Curve
        self.half = curve((0., 1., 2.), (0., 5., 4.))
        self.fine = curve((0., 1., 2.), (0., 1., 3.))
        self.dense = curve((0., .5, 1., 2.), (0., .5, 6., 4.))

    def test_same_location_signed_cancellation(self):
        comparison = sc.compare(self.half, self.fine, self.dense, 1.)
        anchor = comparison["at_original_anchor"]
        self.assertEqual(anchor["u"], 1.)
        self.assertEqual(anchor["gaps_MPa"], dict(zip(sc.GAPS, (4., -1., 5.))))
        self.assertEqual(anchor, comparison["largest_residual_on_common_support"])
        self.assertEqual(comparison["common_knots"], 4)

    def test_short_trace_marks_fixed_location_unavailable(self):
        short = sc.dt.Curve((0., .5), (0., .5))
        comparison = sc.compare(self.half, self.fine, short, 1.)
        self.assertIsNone(comparison["at_original_anchor"])
        self.assertEqual(comparison["anchor_status"], "NOT_REACHED")
        largest = comparison["largest_residual_on_common_support"]
        self.assertEqual(largest["u"], .5)
        self.assertEqual(largest["gaps_MPa"], dict(zip(sc.GAPS, (2., 2., 0.))))

    def test_fixed_location_can_differ_from_common_peak(self):
        comparison = sc.compare(self.half, self.fine, self.dense, 2.)
        self.assertEqual(comparison["at_original_anchor"]["u"], 2.)
        self.assertEqual(comparison["largest_residual_on_common_support"]["u"], 1.)

    def test_original_arrays_and_grid_routing(self):
        original_arrays = (object(), object(), object())
        seed_calls = []

        def seed(cells):
            seed_calls.append(cells)
            return original_arrays

        solver = SimpleNamespace(seed=seed)
        factory = lambda: solver
        timestep = lambda solver, cells: 1 / cells
        driver = SimpleNamespace(fixed_solver=factory, step_size=timestep)

        def run(arm, cells, budget, out):
            self.assertEqual((arm, cells), ("F", 8))
            s = driver.fixed_solver()
            self.assertEqual(driver.step_size(s, cells), 1/16)
            self.assertIs(s.seed(cells), original_arrays)
            return {"status": "TIME_LIMIT"}

        driver.run_arm = run
        with patch.object(sc, "verify_seed", return_value={"checked":True}) as verify:
            result, seed = sc.integrate(driver, 8., Path("unused"))
        verify.assert_called_once_with(original_arrays)
        self.assertEqual(seed_calls, [16])
        self.assertEqual(result["status"], "TIME_LIMIT")
        self.assertEqual(seed, {"checked":True})
        self.assertIs(driver.fixed_solver, factory)
        self.assertIs(driver.step_size, timestep)
        self.assertEqual(solver.seed.__name__, "seed")

    def test_failure_restores_source_and_no_retry(self):
        solver = SimpleNamespace(seed=lambda cells: (1, 2, 3))
        saved_seed = solver.seed
        factory = lambda: solver
        driver = SimpleNamespace(fixed_solver=factory, step_size=lambda s, c: 1/c)
        called = []

        def stop(*args):
            called.append(True)
            raise ValueError("partial")

        driver.run_arm = stop
        with self.assertRaisesRegex(ValueError, "partial"):
            sc.integrate(driver, 1., Path("unused"))
        self.assertEqual(called, [True])
        self.assertIs(solver.seed, saved_seed)
        self.assertIs(driver.fixed_solver, factory)

    def test_wrong_seed_is_refused(self):
        import numpy as np
        arbitrary = np.zeros((sc.NPOINTS, 2)), np.zeros(sc.NPOINTS, dtype='int64'), np.ones(sc.NPOINTS)
        with self.assertRaisesRegex(ValueError, "SEED_HASH"):
            sc.verify_seed(arbitrary)
        with self.assertRaisesRegex(ValueError, "SEED_SHAPE"):
            sc.verify_seed((arbitrary[0][:-1], *arbitrary[1:]))

    def test_frozen_seed_hashes_match_scalar_geometry(self):
        from math import pi, sqrt
        import numpy as np
        width = sqrt(49*pi*.05**2/.78)
        # Multiplication by the fixed binary64 spacing reproduces the seed contract.
        spacing = .5/160
        offsets = [(a*spacing,b*spacing) for a in range(-16,17) for b in range(-16,17)
                   if (a*spacing)*(a*spacing)+(b*spacing)*(b*spacing) <= .05**2]
        xy = np.array([(.15+(i+.5)*width/7+x,.15+(j+.5)*width/7+y)
                       for i in range(7) for j in range(7) for x,y in offsets])
        ids = np.repeat(np.arange(49, dtype="<i8"), len(offsets))
        vol = np.full(len(ids), pi*.05**2/len(offsets))
        self.assertEqual(sc.verify_seed((xy,ids,vol)),sc.SEED)

    def test_complete_record_and_separate_tamper_failures(self):
        import json
        import math
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            width, dt = 1., .001
            h = width-dt*sc.dt.SPEED
            area = 49*math.pi*.05**2
            content = (",".join(sc.dt.COLUMNS)+"\n"+f"0,0,{width},0,{area/width**2}\n"
                       +f"1,{dt},{h},.12,{area/(width*h)}\n").encode()
            (folder/"trace.csv").write_bytes(content)
            native = {"status":"TARGET_BRACKETED","arm":"F","cells":8,"origin":"new","points_count":sc.NPOINTS,
                      "setting":1,"protocol":sc.dt.NATIVE,"label":"DEVELOPMENT_ONLY","trace_sha256":sc.dt.sha(content),
                      "source_sha256":{k:v for k,v in sc.dt.SOURCE.items() if k != "suyoung_u6b_dev.py"},"steps":1}
            sc.dt.write_json(folder/"result.json", native)
            receipt = {"protocol":sc.PROTOCOL,"label":"DEVELOPMENT_ONLY","arm":"F","status":native["status"],
                       "grid_cells_per_diameter":8,"seed_cells_per_diameter":16,"dt_cells_per_diameter":16,
                       "source_sha256":sc.dt.SOURCE,"initial_seed_sha256":sc.SEED,"u6_qualified":False,
                       "reader_sha256":sc.dt.sha(Path(sc.__file__).read_bytes()),"trace_sha256":sc.dt.sha(content),
                       "native_result_sha256":sc.dt.sha((folder/"result.json").read_bytes())}
            ref = {"width":width, "dt":dt, "points_count":sc.NPOINTS}
            receipts = (receipt, dict(receipt, initial_seed_sha256={}), dict(receipt, grid_cells_per_diameter=16),
                        dict(receipt,native_result_sha256="stale"))
            for i,r in enumerate(receipts):
                (folder/"seed_control.json").write_text(json.dumps(r),encoding="ascii")
                if i == 0:
                    curve, digest = sc.dense_curve(folder, ref)
                    self.assertEqual((curve.p, digest), ((0.,1.2), sc.dt.sha(content)))
                else:
                    with self.assertRaisesRegex(ValueError, "CONTROL_BINDING"):
                        sc.dense_curve(folder, ref)

    def test_missing_return_produces_only_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            out = folder/"summary"
            self.assertEqual(sc.read_command(folder/"w", folder/"h", folder/"d", out), 4)
            import json
            result = json.loads(out.read_bytes())
            self.assertEqual(result["status"], "INCOMPLETE")
            self.assertFalse(result["u6_qualified"])
            self.assertNotIn("comparison", result)
            with self.assertRaises(FileExistsError):
                sc.read_command(folder/"w", folder/"h", folder/"d", out)


if __name__ == "__main__":
    unittest.main()
