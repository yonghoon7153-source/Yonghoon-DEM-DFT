"""Operator tests use one synthetic particle or archived bytes, never the production disk packing."""
import csv
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import importlib.util
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("floor_operator_test_subject", HERE / "floor_operator.py")
op = importlib.util.module_from_spec(spec)
spec.loader.exec_module(op)


class FloorOperator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(os.environ.get("SUYOUNG_SOURCE_ROOT", HERE.parents[2]))
        cls.root = root
        cls.m = op.module(Path(os.environ.get("SUYOUNG_NATIVE_PROTOCOL", root / op.MATCHED)))
        physics = Path(os.environ.get("SUYOUNG_CANDIDATE_MODULE", HERE / "material_floor.py"))
        cls.physics = op.module(physics)

    def toy_arm(self, folder, cells, *, stop=None, one=False, source=None):
        # Keep the real historical loop/clock, real new advance and both real floor projections.
        # Only the seeding and optional artificial second-pass kick substitute a tiny test body.
        m = self.m
        driver, solver, kernel = m.engine(self.root)
        x = np.array([[.4, solver.LO + (.001 if one else .18)]])
        fields = np.array([0], dtype=np.int64)
        volume = np.array([.78*m.WIDTH**2])
        initial = x, fields, volume
        boundary = self.physics.MaterialBoundary([0], [[.4, solver.LO if one else x[0, 1]]])
        seen = []
        def factory(s, n):
            seen.append((s, n))
            return self.physics.make_advance(s, n, boundary=boundary)
        if one or stop:
            def kick(ids, node, mass, grad, gv, centers, friction):
                if stop == "failure":
                    raise ArithmeticError("synthetic fault")
                gv[:,1] -= .1 if stop == "target" else 1e-6
            kernel.project_contacts = kick
        parts = (m, source or {"release":"synthetic"}, driver, solver, kernel, SimpleNamespace(make_advance=factory))
        saved = (solver.seed, solver.project_contacts, driver.fixed_solver)
        with patch.object(m, "seed_arrays", return_value=initial), patch.dict(op.END, {cells:1} if one else {}):
            rc = op.arm(parts, cells, folder)
        self.assertEqual(saved, (solver.seed, solver.project_contacts, driver.fixed_solver))
        self.assertEqual(seen, [(solver, cells)])
        return rc

    def test_full_two_native_schedules_on_stationary_synthetic_point(self):
        with tempfile.TemporaryDirectory() as td:
            for cells, steps in op.END.items():
                folder = Path(td) / f"F{cells}"
                self.assertEqual(self.toy_arm(folder, cells), 0)
                rec = json.loads((folder / "receipt.json").read_bytes())
                self.assertEqual((rec["grid"], rec["dt"], rec["steps"], rec["interbody_calls"]),
                                 (10*cells, op.dt_for(self.m,cells), steps, steps))
                self.assertEqual(rec["floor_audit"]["floor_passes"], 2*steps)
                self.assertEqual(rec["floor_audit"]["positive_passes"], 0)

    def test_actual_after_interbody_floor_pass_reaches_native_pressure_csv(self):
        with tempfile.TemporaryDirectory() as td:
            for cells in op.END:
                folder = Path(td) / f"F{cells}"
                self.assertEqual(self.toy_arm(folder, cells, one=True), 0)
                rec = json.loads((folder / "receipt.json").read_bytes())
                self.assertEqual(rec["floor_audit"]["positive_passes"], 1)
                self.assertGreater(rec["floor_audit"]["accumulated_impulse"], 0.)
                self.assertGreater(self.m.parse_trace((folder/"trace.csv").read_bytes(), rec["dt"],1)[-1], 0.)

    def test_early_cap_and_interbody_failure_stay_incomplete(self):
        with tempfile.TemporaryDirectory() as td:
            for reason in ("target","failure"):
                folder = Path(td) / reason
                self.assertEqual(self.toy_arm(folder, 8, stop=reason, one=True), 4)
                self.assertTrue((folder/"incomplete.json").exists())
                self.assertFalse((folder/"receipt.json").exists())

    def test_original_binds_whole_archive_and_both_receipts(self):
        prior = os.environ.get("SUYOUNG_CROSS_RETURN")
        if not prior:
            self.skipTest("Set SUYOUNG_CROSS_RETURN to the registered cross archive")
        old = op.original(self.m, Path(prior))
        for cells in op.END:
            self.assertEqual(op.sha(old[cells]["cross_receipt.json"]), op.CROSS_RECEIPT[cells])
        with tempfile.TemporaryDirectory() as td:
            bad = Path(td)/"altered.tar.gz"
            bad.write_bytes(Path(prior).read_bytes() + b"x")
            with self.assertRaisesRegex(ValueError, "CROSS_ARCHIVE_HASH"):
                op.original(self.m,bad)

    def test_old_union_crossing_539_and_shared_540(self):
        prior = os.environ.get("SUYOUNG_CROSS_RETURN")
        if not prior:
            self.skipTest("Set SUYOUNG_CROSS_RETURN to the registered cross archive")
        old = op.original(self.m, Path(prior))
        p = [self.m.parse_trace(old[n]["trace.csv"], op.dt_for(self.m,n), steps) for n, steps in op.END.items()]
        summary = op.gap_summary(self.m,*p)
        first = summary["native_union"]["first_above_5pct"]
        self.assertEqual(first["fine_step"],539)
        self.assertTrue(first["coarse_interpolated"])
        self.assertAlmostEqual(first["signed_gap_MPa"],.03359937103298061,places=15)
        self.assertEqual(summary["shared_native"]["first_above_5pct"]["fine_step"],540)

    def test_readback_and_weekly_csv_refuse_trace_or_receipt_changes(self):
        prior = os.environ.get("SUYOUNG_CROSS_RETURN")
        if not prior:
            self.skipTest("Set SUYOUNG_CROSS_RETURN to the registered cross archive")
        old = op.original(self.m, Path(prior))
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            for n in op.END:
                orig = run/"original"/f"F{n}"
                orig.mkdir(parents=True)
                for name, data in old[n].items():
                    (orig/name).write_bytes(data)
                (run/"candidate").mkdir(exist_ok=True)
                self.assertEqual(self.toy_arm(run/"candidate"/f"F{n}", n),0)
            parts = (self.m, {"release":"synthetic"})
            summary = op.summarize(parts, old, run, write_outputs=True)
            self.assertTrue(summary["candidate_zero_throughout"])
            self.assertFalse(summary["qualification_computed"])
            raw = (run/"pressure_displacement.csv").read_bytes()
            rows = list(csv.DictReader(io.StringIO(raw.decode())))
            self.assertEqual(len(rows),1624)
            self.assertEqual(summary["pressure_displacement_sha256"],op.sha(raw))
            self.assertEqual({(r["wall_model"], r["cells"]) for r in rows},
                             {(m,str(n)) for m in op.MODELS for n in op.END})
            for path in (run/"candidate/F16/trace.csv", run/"original/F8/prefix_receipt.json",
                         run/"candidate/F8/receipt.json", run/"pressure_displacement.csv"):
                before = path.read_bytes()
                path.write_bytes(before.replace(b"synthetic", b"altered") if path.name == "receipt.json"
                                 else before+b"X")
                with self.subTest(path=path), self.assertRaises(ValueError):
                    op.summarize(parts,old,run,write_outputs=False)
                path.write_bytes(before)


if __name__ == "__main__":
    unittest.main()
