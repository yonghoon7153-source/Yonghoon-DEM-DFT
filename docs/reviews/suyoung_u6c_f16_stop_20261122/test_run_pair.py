"""Development runner checks. The integration loop is replaced by a one-row fixture."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
spec = importlib.util.spec_from_file_location("three_body_pair", HERE / "run_pair.py")
pair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pair)


class PairTests(unittest.TestCase):
    def test_match_includes_last_complete_sample_and_line_endings(self):
        previous = b"col\r\n0\r\n1\r\n"
        self.assertTrue(pair.prefix_matches(previous, previous + b"2\r\n"))
        for current in (previous, previous[:-3], b"col\n0\n1\n2\n",
                        b"col\r\n0\r\n9\r\n2\r\n"):
            self.assertFalse(pair.prefix_matches(previous, current))

    def test_preservation_gates(self):
        with self.assertRaisesRegex(ValueError, "F8_TRACE_CHANGED"):
            pair.check_history(8, b"a\n", b"b\n")
        with self.assertRaisesRegex(ValueError, "F16_PREFIX_CHANGED_OR_NOT_EXTENDED"):
            pair.check_history(16, b"a\n", b"b\nc\n")
        pair.check_history(8, b"a\n", b"a\n")
        pair.check_history(16, b"a\n", b"a\nb\n")

    def test_nonoriginal_field_rejected(self):
        for cells in (8, 16):
            modules = pair.load_sources(REPO)
            driver = modules["driver"]
            solver = driver.fixed_solver()
            x, ids, volume = solver.seed(cells)
            state = pair.seed_hashes(x, ids, volume, cells)
            with self.assertRaisesRegex(ValueError, "ORIGINAL_FIELD_SELECTOR"):
                pair.select_fields(lambda a, i: i[::-1], cells, "F", ids, state)

    def test_same_candidate_and_native_receipt(self):
        for cells in (8, 16):
            with self.subTest(cells=cells), tempfile.TemporaryDirectory() as temp:
                mods = pair.load_sources(REPO)
                driver = mods["driver"]
                out = Path(temp) / ("F" + str(cells))

                def fake(arm, n, budget, path):
                    solver = driver.fixed_solver()
                    x, ids, volume = solver.seed(n)
                    driver.field_ids(arm, ids)
                    solver.project_contacts(np.array([0, 1]), np.zeros(2, dtype=int),
                                            np.ones(2), np.array([[0., 0.], [1., 0.]]),
                                            np.zeros((2, 2)), np.array([[0., 0.], [1., 0.]]), .5)
                    path.mkdir()
                    t = driver.step_size(solver, n)
                    w = solver.WIDTH
                    h = w - t * solver.WALL_SPEED
                    data = (f"step,time_code,height,bottom_pressure_E,phi_m\n"
                            f"0,0,{w},0,{volume.sum()/w**2}\n1,{t},{h},0.12,{volume.sum()/(w*h)}\n")
                    (path / "trace.csv").write_bytes(data.encode())
                    value = dict(arm=arm, cells=n, steps=1, points_count=len(x), setting=1,
                                 label="DEVELOPMENT_ONLY", status="TARGET_BRACKETED", origin="new",
                                 protocol=driver.PROTOCOL, budget_s=budget, elapsed_s=0.0,
                                 source_sha256=driver.SOURCE, trace_sha256=driver.digest(path / "trace.csv"))
                    driver.write_json(path / "result.json", value)
                    return value

                with patch.object(pair, "load_sources", return_value=mods), patch.object(driver, "run_arm", side_effect=fake):
                    self.assertEqual(pair.run_arm(REPO, cells, out), 0)
                trace, curve, receipt = pair.read_arm(mods, cells, out)
                self.assertEqual((len(curve), receipt["cells"], receipt["kernel_sha256"]), (2, cells, pair.KERNEL))
                self.assertFalse(receipt["u6_qualified"])
                with self.assertRaises(FileExistsError):
                    pair.run_arm(REPO, cells, out)
                receipt["kernel_sha256"] = "0" * 64
                (out / "candidate.json").write_text(json.dumps(receipt), encoding="ascii")
                with self.assertRaisesRegex(ValueError, "ARM_RECEIPT"):
                    pair.read_arm(mods, cells, out)

    def test_reference_geometry_and_timing(self):
        mods = pair.load_sources(REPO)
        for cells in (8, 16):
            pair.setup_geometry(mods["driver"], mods["driver"].fixed_solver(), cells)


if __name__ == "__main__":
    unittest.main()
