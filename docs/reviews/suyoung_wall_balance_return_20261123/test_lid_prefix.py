"""Manufactured trace, native-driver stub and receipt checks. No field calculation."""
import csv
from contextlib import contextmanager, redirect_stdout
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


source = Path(__file__).with_name("lid_prefix.py")
if not source.is_file():
    source = Path(os.environ["SUYOUNG_LID_PREFIX"])
spec = importlib.util.spec_from_file_location("tested_lid_prefix", source)
lid = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lid)

TRACE = ("step", "time_code", "height", "bottom_pressure_E", "phi_m")
DT = {12: .125, 24: .0625}
STEPS = {12: 2, 24: 4}
ANCHORS = {12: (1, 2), 24: (2, 4)}
IDENTITY = {"release": "synthetic", "baseline_sha256": "fixture"}


def csv_bytes(columns, items):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, columns, lineterminator="\r\n")
    writer.writeheader()
    writer.writerows(items)
    return stream.getvalue().encode("ascii")


def trace(cells, pressures):
    return [{
        "step": i, "time_code": i * DT[cells], "height": 1. - i * DT[cells] * .5,
        "bottom_pressure_E": p, "phi_m": .5 / (1. - i * DT[cells] * .5),
    } for i, p in enumerate(pressures)]


def fixture(cells):
    n = STEPS[cells]
    pressures = [0.] + [0. if i == 1 else .02 for i in range(1, n + 1)]
    native = trace(cells, pressures)
    walls = []
    for i in range(1, n + 1):
        down = .125 if i == 1 else 0.
        walls.append(dict(step=i, floor_impulse=pressures[i] * DT[cells], lid_downward_impulse=down,
                          lid_signed_impulse=-down, top_gap_before=.005, top_gap_after=0.,
                          floor_gap_after=0., lid_grid_impulse_error=0.))
    floor = dict(steps=n, floor_passes=2*n, positive_passes=n-1, accumulated_impulse=sum(row["floor_impulse"] for row in walls),
                 max_grid_impulse_error=0., max_g2p_momentum_error=0., max_penetration=0., disk_boundary_vertices=256)
    upper = dict(steps=n, lid_passes=2*n, positive_passes=1, accumulated_downward_impulse=.125,
                 max_grid_impulse_error=0., max_penetration=0., max_clock_error=0.)
    return native, walls, floor, upper


def write_json(path, value):
    path.write_text(json.dumps(value), encoding="ascii")


class PrefixTests(unittest.TestCase):
    def setUp(self):
        for obj, value in ((lid.STEPS, STEPS), (lid.SAMPLE_STEPS, ANCHORS)):
            guard = patch.dict(obj, value)
            guard.start()
            self.addCleanup(guard.stop)
        self.fine = SimpleNamespace(DT=DT, write_json=write_json)
        self.ctx = SimpleNamespace(solver=SimpleNamespace(WIDTH=1., LO=.125, WALL_SPEED=.5))

    def receipt(self, cells, native, walls, floor, upper):
        return lid.receipt(self.fine, self.ctx, IDENTITY, cells, csv_bytes(TRACE, native),
                           csv_bytes(lid.WALL_COLUMNS, walls), floor, upper)

    def test_paired_accepts_pressure_only_and_matches_native_text(self):
        reference = trace(12, [0., .1, .2])
        changed = trace(12, [0., .25, 0.])
        a = csv_bytes(TRACE, reference)
        self.assertEqual(lid.paired_trace(a, csv_bytes(TRACE, changed), 12)[1]["bottom_pressure_E"], "0.25")
        for field, val, idx in [("time_code", "0.1250", 1), ("height", ".9", 2), ("phi_m", "0.6", 1),
                                ("step", 3, 2), ("bottom_pressure_E", .01, 0),
                                ("bottom_pressure_E", -1, 1), ("bottom_pressure_E", "nan", 2)]:
            bad = [dict(row) for row in changed]
            bad[idx][field] = val
            with self.subTest(field=field, val=val), self.assertRaises(ValueError):
                lid.paired_trace(a, csv_bytes(TRACE, bad), 12)
        with self.assertRaises(ValueError):
            lid.paired_trace(a, csv_bytes(TRACE, changed[:-1]), 12)

    def test_union_interpolates_signed_odd_knot_with_fixed_threshold(self):
        traces = {12: trace(12, [0, .01, .02]), 24: trace(24, [0, .005, .00669, .033, .02])}
        result = lid.compare(traces, 1.)
        self.assertEqual(result["samples"], 5)
        self.assertEqual(result["first_above"]["step_F24"], 3)
        self.assertEqual(result["peak"]["step_F24"], 3)
        self.assertAlmostEqual(result["peak"]["F12_MPa"], .15)
        self.assertAlmostEqual(result["peak"]["F24_MPa"], .33)
        self.assertAlmostEqual(result["peak"]["signed_gap_MPa"], -.18)
        self.assertAlmostEqual(result["fixed_reference_percent"], 100 * .18 / .6636991102836952)
        self.assertEqual([r["step_F24"] for r in result["anchors"]], [2, 4])
        for index, bad in ((1, traces[12][0]["height"]), (2, .91)):
            broken = {12: traces[12], 24: [dict(r) for r in traces[24]]}
            broken[24][index]["height"] = bad
            with self.subTest(index=index), self.assertRaises(ValueError):
                lid.compare(broken, 1.)
        equal = {n: trace(n, [0.] * (STEPS[n]+1)) for n in STEPS}
        self.assertIsNone(lid.compare(equal, 1.)["first_above"])

    def test_receipt_binds_native_and_wall_bytes(self):
        native, walls, floor, upper = fixture(12)
        report = self.receipt(12, native, walls, floor, upper)
        self.assertEqual((report["steps"], report["first_lid_down_step"], report["first_positive_step"]), (2, 1, 2))
        self.assertEqual(report["trace_sha256"], hashlib.sha256(csv_bytes(TRACE, native)).hexdigest())
        self.assertEqual(report["wall_csv_sha256"], hashlib.sha256(csv_bytes(lid.WALL_COLUMNS, walls)).hexdigest())
        self.assertFalse(report["u6_qualified"] or report["stage3_go"])

    def test_rejects_malformed_wall_rows_and_aggregate_receipts(self):
        native, walls, floor, upper = fixture(12)
        for field, value in (("step", 3), ("top_gap_after", -3e-12), ("floor_gap_after", -3e-12),
                             ("lid_signed_impulse", .125), ("floor_impulse", .01), ("lid_grid_impulse_error", 3e-12),
                             ("top_gap_before", float("nan"))):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.receipt(12, native, [{**walls[0], field: value}, walls[1]], floor, upper)
        for field, value in (("accumulated_downward_impulse", .25), ("positive_passes", 5), ("lid_passes", 3),
                             ("max_clock_error", 3e-12), ("max_penetration", -1.)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.receipt(12, native, walls, floor, {**upper, field: value})
        for field, value in (("floor_passes", 3), ("accumulated_impulse", .25), ("max_penetration", 3e-12)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.receipt(12, native, walls, {**floor, field: value}, upper)
        with self.assertRaises(ValueError):
            self.receipt(12, native, walls[:-1], floor, upper)

    def test_summary_counters_and_measured_maxima_must_match(self):
        native, walls, floor, upper = fixture(12)
        for field, value in (("positive_passes", .5), ("positive_passes", 0), ("positive_passes", 3),
                             ("max_grid_impulse_error", 1e-12), ("max_penetration", 1e-12)):
            with self.subTest(plate="upper", field=field, value=value), self.assertRaises(ValueError):
                self.receipt(12, native, walls, floor, {**upper, field: value})
        for field, value in (("positive_passes", .5), ("positive_passes", 0), ("positive_passes", 3),
                             ("max_penetration", 1e-12), ("max_grid_impulse_error", float("nan"))):
            with self.subTest(plate="lower", field=field, value=value), self.assertRaises(ValueError):
                self.receipt(12, native, walls, {**floor, field: value}, upper)

    def test_summary_rereads_receipt_and_flags_tampered_wall_bytes(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            run = root / "run"
            run.mkdir()
            for name in ("RELEASE", "SOURCE_SHA256SUMS"):
                for directory in (root, run):
                    (directory / name).write_bytes(b"fixture\n")
            prior = {}
            for n in STEPS:
                arm = run / f"F{n}"
                arm.mkdir()
                native, walls, floor, upper = fixture(n)
                prior[n] = csv_bytes(TRACE, trace(n, [0.] * (STEPS[n] + 1)))
                (arm / "trace.csv").write_bytes(csv_bytes(TRACE, native))
                (arm / "wall_steps.csv").write_bytes(csv_bytes(lid.WALL_COLUMNS, walls))
                write_json(arm / "candidate_receipt.json", self.receipt(n, native, walls, floor, upper))
            argv = ["lid_prefix.py", "summary", "--root", str(root), "--prior", str(root / "prior"), "--run", str(run)]
            with patch.object(sys, "argv", argv), patch.object(lid, "setup", return_value=(self.fine, self.ctx, None, prior, IDENTITY)):
                with redirect_stdout(io.StringIO()):
                    lid.main()
                result = json.loads((run / "summary.json").read_bytes())
                self.assertEqual(result["status"], "MATCHED_PREFIX_COMPLETE")
                self.assertEqual(result["old_grid_lid"]["peak"]["signed_gap_MPa"], 0)
                self.assertGreater(result["new_material_lid"]["fixed_reference_percent"], 0)
                self.assertFalse(result["three_dimensional_go"])
                path = run / "F24" / "wall_steps.csv"
                path.write_bytes(path.read_bytes().replace(b"0.005,", b"0.0050,", 1))
                with self.assertRaisesRegex(ValueError, "receipt mismatch"):
                    lid.main()

    def test_native_driver_stub_obeys_one_seed_and_one_contact_per_step(self):
        # Exercise the normal arm wrapper, including its extra call to stop at the last saved sample.
        cells = 12
        native, walls, floor, upper = fixture(cells)
        initial = tuple(object() for _ in range(3))
        calls = []
        fake_solver = self.ctx.solver
        self.ctx.floor = object()
        self.ctx.kernel = SimpleNamespace(project_contacts=lambda friction: calls.append(("contact", friction)))
        self.fine.initial = lambda ctx, n: initial

        @contextmanager
        def bind(ctx, seed, project):
            ctx.seed, ctx.project = seed, project
            yield

        self.fine.bind_driver = bind

        def make_advance(solver, n, *, floor_module):
            self.assertIs(solver, fake_solver)
            self.assertEqual(n, cells)
            self.assertIs(floor_module, self.ctx.floor)

            def advance(*args):
                self.ctx.project(.5)
                advance.last_step = walls[len(calls)-1]

            advance.audit, advance.lid_audit = floor, upper
            return advance

        def run(label, n, budget, path, *, advance):
            self.assertEqual((label, n, budget), ("F", cells, lid.BUDGET[cells]))
            self.assertIs(self.ctx.seed(n), initial)
            path.mkdir()
            (path / "trace.csv").write_bytes(csv_bytes(TRACE, native))
            for i in (1, 2, 3):
                h = 1. - DT[n] * i * fake_solver.WALL_SPEED
                advance(None, None, None, None, initial[1], initial[2], 10*n, DT[n], fake_solver.LO+h)
            self.fail("arm did not stop before a third step")

        self.ctx.driver = SimpleNamespace(run_arm=run)
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / "F12"
            lid.run_arm(self.fine, self.ctx, SimpleNamespace(make_advance=make_advance),
                        {cells: csv_bytes(TRACE, native)}, IDENTITY, cells, dest)
            self.assertEqual(calls, [("contact", .5), ("contact", .5)])
            self.assertEqual(json.loads((dest / "candidate_receipt.json").read_bytes())["steps"], 2)
            self.assertEqual((dest / "wall_steps.csv").read_text().splitlines()[0], ",".join(lid.WALL_COLUMNS))


if __name__ == "__main__":
    unittest.main()
