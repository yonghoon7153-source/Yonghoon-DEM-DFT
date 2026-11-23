"""Small synthetic checks for the same-floor F12/F24 handoff; no time integration."""
import csv
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from types import SimpleNamespace as NS
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fine", HERE / "fine_floor.py")
fine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fine)
REFERENCE = Path(os.environ.get("SUYOUNG_FULL_REFERENCE", HERE.parent / "suyoung_floor_full_20261123"))
compare = fine.load(REFERENCE / "full_compare.py")


def sample(cells, pressures, *, terminal="TARGET_BRACKETED", speed=1.):
    dt = fine.DT[cells]
    buf = io.StringIO(newline="")
    writer = csv.writer(buf)
    writer.writerow(compare.COLUMNS)
    for i, p in enumerate(pressures):
        t = i*dt
        height = 1. - t*speed
        writer.writerow((i, t, height, p, .78/height))
    trace = buf.getvalue().encode("ascii")
    result = dict(arm="F", cells=cells, setting=1, label="DEVELOPMENT_ONLY", origin="new",
                  status=terminal, source_sha256={"solver": "a"}, protocol="u6", points_count=fine.POINTS[cells],
                  budget_s=fine.BUDGET[cells], trace_sha256=fine.sha(trace), elapsed_s=.2, steps=i)
    audit = dict(accumulated_impulse=sum(pressures)*dt, positive_passes=sum(p>0 for p in pressures),
                 steps=i, floor_passes=2*i, disk_boundary_vertices=256, max_grid_impulse_error=0.,
                 max_g2p_momentum_error=0., max_penetration=0.)
    return trace, json.dumps(result).encode(), audit


def context(speed=1.):
    return NS(compare=compare, solver=NS(WIDTH=1., WALL_SPEED=speed), identity={"release": "test"},
              driver=NS(SOURCE={"solver": "a"}, PROTOCOL="u6"))


class FinePair(unittest.TestCase):
    def test_native_clocks_and_point_counts(self):
        self.assertEqual(fine.DT[12], 2*fine.DT[24])
        self.assertEqual((fine.POINTS[12], fine.POINTS[24]), (21609, 87857))
        self.assertNotEqual(fine.SEEDS[12], fine.SEEDS[24])
        for cells in (12, 24):
            trace, result, audit = sample(cells, (0., 0., .09, .12))
            info = fine.receipt(context(), cells, trace, result, audit)
            self.assertEqual(info["first_positive_step"], 2)
            self.assertEqual(info["positive_native_samples"], 2)
            self.assertEqual(info["geometry_sha256"], list(fine.SEEDS[cells]))
            self.assertTrue(info["reached_target"])
            self.assertFalse(info["u6_qualified"])

    def test_arm_or_point_substitution_and_stale_hash(self):
        trace, raw, audit = sample(12, (0., .12))
        for overrides in ({"cells": 24}, {"points_count": fine.POINTS[24]}, {"origin": "historical"},
                          {"trace_sha256": "other"}, {"setting": 2}, {"budget_s": 14400}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                fine.receipt(context(), 12, trace, json.dumps(dict(json.loads(raw), **overrides)).encode(), audit)

    def test_false_terminal_and_timeout(self):
        for p, terminal in (((0., .09), "TARGET_BRACKETED"), ((0., .09), "TIME_LIMIT"),
                            ((0., .12, .13), "TARGET_BRACKETED"), ((0., .09), "GEOMETRY_LIMIT")):
            with self.subTest(p=p, terminal=terminal), self.assertRaises(ValueError):
                fine.receipt(context(), 24, *sample(24, p, terminal=terminal))

    def test_geometry_with_no_reaction(self):
        speed = .1/fine.DT[24]
        rec = fine.receipt(context(speed), 24, *sample(24, [0., 0., 0.], terminal="GEOMETRY_LIMIT", speed=speed))
        self.assertIsNone(rec["first_positive_step"])
        self.assertFalse(rec["reached_target"])

    def test_momentum_closure_and_penetration(self):
        trace, result, audit = sample(12, (0., .06, .12))
        for overrides in ({"accumulated_impulse": .1}, {"floor_passes":0}, {"max_penetration": 1e-6},
                          {"positive_passes":0}):
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                fine.receipt(context(), 12, trace, result, dict(audit, **overrides))

    def make_return(self, run):
        for cells, p in ((12, (0., 0., .12)), (24, (0., .04, .01, .05, .12))):
            trace, result, audit = sample(cells, p)
            rec = fine.receipt(context(), cells, trace, result, audit)
            sub = run / f"F{cells}"
            sub.mkdir()
            (sub / "trace.csv").write_bytes(trace)
            (sub / "result.json").write_bytes(result)
            fine.write_json(sub / "fine_receipt.json", rec)

    def test_compare_uses_native_union_right_labels_and_preserves_coarse_failure(self):
        with tempfile.TemporaryDirectory() as root:
            run = Path(root)
            self.make_return(run)
            prior = dict(fixed_reference_comparison="EXCEEDS", fixed_reference_ratio=.8)
            out = fine.summarize(context(), prior, run)
            self.assertEqual(out["previous_F8_F16"], prior)
            ratio = out["comparison"]
            self.assertEqual(ratio["pair"], "F12_F24")
            self.assertEqual(set(ratio["arms"]), {"F12","F24"})
            self.assertEqual(ratio["common"]["samples"], 5)
            self.assertAlmostEqual(ratio["common"]["max_abs_difference_MPa"], .4)
            self.assertTrue(ratio["common"]["first_worst"]["F24_native"])
            self.assertFalse(ratio["common"]["first_worst"]["F12_native"])
            self.assertEqual(ratio["fine_peak_on_common_support_MPa"], 1.2)
            self.assertEqual(ratio["fixed_reference_MPa"], compare.FIXED_REFERENCE_MPA)
            self.assertFalse(out["u6_qualified"] or out["stage3_go"] or out["three_dimensional_go"])

    def test_incomplete_arm_or_modified_receipt_cannot_enter_summary(self):
        with tempfile.TemporaryDirectory() as root:
            run = Path(root)
            self.make_return(run)
            incomplete = run / "F24/incomplete.json"
            incomplete.write_text("{}")
            with self.assertRaises(ValueError):
                fine.summarize(context(), {}, run)
            incomplete.unlink()
            receipt = run / "F12/fine_receipt.json"
            r = json.loads(receipt.read_bytes())
            r["trace_sha256"] = "x"
            receipt.write_text(json.dumps(r))
            with self.assertRaises(ValueError):
                fine.summarize(context(), {}, run)

    def test_solver_binding_restores_state_after_exception(self):
        solver, driver = NS(seed="first", project_contacts="second"), NS(fixed_solver="third")
        with self.assertRaises(RuntimeError):
            with fine.bind_driver(NS(solver=solver, driver=driver), object(), object()):
                self.assertIs(driver.fixed_solver(), solver)
                raise RuntimeError("test")
        self.assertEqual((solver.seed,solver.project_contacts,driver.fixed_solver),("first","second","third"))

    def test_native_driver_orchestration_with_manufactured_pressure(self):
        # Simulate the driver's exact call arguments without computing any physical field.
        cells = 12
        trace, result, audit = sample(cells, (0., .01, .12))
        ctx = context()
        ctx.solver.LO = .15
        ctx.solver.seed, ctx.solver.project_contacts, ctx.driver.fixed_solver = "seed", "project", "solver"
        ctx.kernel = NS(project_contacts=lambda *args: None)
        def step(*args):
            ctx.solver.project_contacts(None, .5)
            return ()
        class Stepper:
            def __call__(self, *args):
                return step(*args)
        stepper = Stepper()
        stepper.audit = audit
        ctx.floor = NS(make_advance=lambda solver, count: stepper)
        arrays = (object(), object(), object())
        def driver(arm, n, budget, dest, *, advance):
            self.assertIs(ctx.driver.fixed_solver(), ctx.solver)
            self.assertEqual((arm, n, budget), ("F", cells, fine.BUDGET[cells]))
            x, ids, vol = ctx.solver.seed(cells)
            for i in (1, 2):
                h = ctx.solver.WIDTH - i*fine.DT[cells]*ctx.solver.WALL_SPEED
                advance(x, None, None, None, ids, vol, 10*cells, fine.DT[cells], ctx.solver.LO+h)
            dest.mkdir()
            (dest / "trace.csv").write_bytes(trace)
            (dest / "result.json").write_bytes(result)
            return json.loads(result)
        ctx.driver.run_arm = driver
        with tempfile.TemporaryDirectory() as root, patch.object(fine, "initial", return_value=arrays):
            dest = Path(root) / "F12"
            fine.run_arm(ctx, cells, dest)
            self.assertTrue(json.loads((dest / "fine_receipt.json").read_bytes())["reached_target"])
            self.assertFalse((dest / "incomplete.json").exists())
            with self.assertRaisesRegex(ValueError, "existing arm"):
                fine.run_arm(ctx, cells, dest)
        self.assertEqual((ctx.solver.seed, ctx.solver.project_contacts, ctx.driver.fixed_solver),
                         ("seed", "project", "solver"))


if __name__ == "__main__":
    unittest.main()
