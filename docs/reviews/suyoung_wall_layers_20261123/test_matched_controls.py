"""Synthetic checks for the two matched grid-80 prefixes. No loading arm is run."""
import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import numpy as np


def load():
    path = Path(__file__).with_name("matched_controls.py")
    spec = importlib.util.spec_from_file_location("matched_controls_test_subject", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Controls(unittest.TestCase):
    def setUp(self):
        self.m = load()

    def trace(self, dt, last=540, pressure=0.002):
        h = self.m.WIDTH
        v = self.m.SPEED
        lines = [",".join(self.m.COLUMNS)]
        for i in range(last+1):
            t = i * dt
            lines.append(f"{i},{t},{h-t*v},{pressure if i else 0.0},{.78*h/(h-t*v)}")
        return ("\n".join(lines)+"\n").encode()

    def test_fixed_clock_and_mpa(self):
        self.assertEqual(self.m.parse_trace(self.trace(self.m.DT), self.m.DT, 540)[-1], .02)

    def test_reject_partial_and_wrong_clock(self):
        for data in (self.trace(self.m.DT, 539), self.trace(2*self.m.DT)):
            with self.subTest(), self.assertRaises(ValueError):
                self.m.parse_trace(data, self.m.DT, 540)

    def test_reject_early_target_and_nonfinite(self):
        for p in (.12, float("nan"), -.01):
            with self.subTest(p=p), self.assertRaises(ValueError):
                self.m.parse_trace(self.trace(self.m.DT, pressure=p), self.m.DT, 540)

    def test_same_displacement_signed_bridge(self):
        def seq(scale, last=540):
            return [s*scale for s in range(last+1)]
        r = self.m.bridge(seq(.002, 270), seq(.0009), seq(.0007), seq(.00055))
        endpoint = r["samples"][-1]
        for k,v in {"dt_MPa":.054, "seed_MPa":.108, "grid_MPa":.081, "native_gap_MPa":.243}.items():
            self.assertAlmostEqual(endpoint[k],v)
        self.assertEqual([r["samples"][k] for k in (269,270)],r["primary"])
        self.assertEqual(r["peaks"]["dt_MPa"]["coarse_step"],270)
        self.assertFalse(r["u6_qualified"])
        self.assertFalse(r["stage3_go"])
        self.assertEqual(r["registered_fine_peak_MPa"], .6636991102836952)

    def test_signed_cancellation_and_first_tied_max(self):
        coarse=[0.0]*271
        fine=[0.0]*541
        a=fine.copy()
        a[2]=a[4]=.1
        r=self.m.bridge(coarse,a,fine,fine)
        self.assertEqual(r["peaks"]["dt_MPa"]["coarse_step"],1)
        self.assertEqual(r["samples"][1]["dt_MPa"], -.1)
        self.assertEqual(r["samples"][1]["seed_MPa"], .1)
        self.assertEqual(r["samples"][1]["native_gap_MPa"], 0.)

    def test_bridge_requires_all_rows(self):
        with self.assertRaises(ValueError):
            self.m.bridge([0.]*270,[0.]*541,[0.]*541,[0.]*541)

    def test_receipt_binds_trace_and_seed_role(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            data=self.trace(self.m.DT)
            (p/"trace.csv").write_bytes(data)
            original=self.m.receipt(8,data)
            self.m.write(p/"receipt.json",original)
            self.assertEqual(len(self.m.control_read(p,8)),541)
            with self.assertRaises(ValueError):
                self.m.control_read(p,16)
            (p/"trace.csv").write_bytes(data.replace(b"0.002,",b"0.003,",1))
            with self.assertRaises(ValueError):
                self.m.control_read(p,8)

    def test_outputs_exclusive(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"s.json"
            self.m.write(p,{"x":0})
            with self.assertRaises(FileExistsError):
                self.m.write(p,{"x":1})
            self.assertEqual(json.loads(p.read_bytes()),{"x":0})

    def mock_arm(self, folder, stop=None):
        m = self.m
        initial = (np.zeros((2,2)), np.array([0,1]), np.ones(2))
        solver = SimpleNamespace(LO=.15, seed=lambda n: initial, project_contacts=None)
        kernel = SimpleNamespace(project_contacts=lambda *args: None)
        kernel_calls = 0
        def fake_native(*args):
            nonlocal kernel_calls
            kernel_calls += 1
            if stop == "contact" and kernel_calls == 25:
                raise ArithmeticError("synthetic contact stop")
            solver.project_contacts(.5)
        solver.advance = fake_native
        def fake_loop(mode, cells, budget, out, *, advance):
            self.assertEqual((mode,cells,budget),("F",8,600))
            self.assertEqual(driver.step_size(solver, cells), m.DT)
            x,ids,volume = solver.seed(cells)
            out.mkdir()
            raw = self.trace(m.DT)
            for i in range(1,542):
                if i == 26 and stop == "target":
                    return {"status":"TARGET_BRACKETED"}
                if i == 26 and stop == "clock":
                    return {"status":"TIME_LIMIT"}
                if i == 541:
                    (out/"trace.csv").write_bytes(raw)
                advance(x, x, np.zeros((2,2,2)), np.ones((2,2,2)),
                        ids, volume, 80, m.DT, solver.LO+(m.WIDTH-m.DT*i*m.SPEED))
            self.fail("advanced beyond registered step 540")
        driver = SimpleNamespace(field_ids=lambda mode, ids:ids, fixed_solver=lambda:solver,
                                 step_size=lambda *args:2*m.DT,run_arm=fake_loop)
        with patch.object(m,"engine",return_value=(driver,solver,kernel)), patch.object(
                m,"seed_arrays",return_value=initial) as seeds:
            rc=m.run_arm(Path("."),16,folder)
            seeds.assert_called_once_with(solver,16)
        return rc,kernel_calls

    def test_fine_seed_coarse_grid_fine_dt_and_exact_stop(self):
        with tempfile.TemporaryDirectory() as td:
            folder=Path(td)/"seed16"
            self.assertEqual(self.mock_arm(folder),(0,540))
            self.assertEqual(len(self.m.control_read(folder,16)),541)
            self.assertFalse((folder/"failed_incoming.npz").exists())

    def test_contact_target_or_time_stop_cannot_emit_complete_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            for stop in ("contact","target","clock"):
                folder=Path(td)/stop
                with self.subTest(stop=stop):
                    self.assertEqual(self.mock_arm(folder,stop),(4,25))
                    self.assertTrue((folder/"incomplete.json").is_file())
                    self.assertFalse((folder/"receipt.json").exists())
                    captured=folder/"failed_incoming.npz"
                    self.assertEqual(captured.is_file(),stop=="contact")
                    if stop=="contact":
                        failure=json.loads((folder/"incomplete.json").read_bytes())["failed_advance"]
                        self.assertEqual(failure["incoming_sha256"],self.m.sha(captured.read_bytes()))
                        with np.load(captured,allow_pickle=False) as z:
                            self.assertEqual((int(z["attempted_step"]),int(z["grid"])),(25,80))
                            self.assertTrue(np.array_equal(z["ids"],[0,1]))


if __name__=="__main__":
    unittest.main()
