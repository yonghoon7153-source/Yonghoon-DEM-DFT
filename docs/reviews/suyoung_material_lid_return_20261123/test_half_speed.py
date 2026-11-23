"""Manufactured clocks, observations and a stub driver; no compression is run."""
import csv
from contextlib import contextmanager
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


here = Path(__file__).resolve()
half = load("half_speed_tested", here.with_name("half_speed.py"))
default = here.parents[3] / half.PREVIOUS_READER
near = here.parent / "history" / half.PREVIOUS_READER
native = load("native_tested", os.environ.get("HALF_SPEED_NATIVE", near if near.is_file() else default))
DT = {12: .125, 24: .0625}
OLD = {12: 2, 24: 4}
HALF = {12: 4, 24: 8}
OLD_MARKS = {12:(1,2), 24:(2,4)}
NEW_MARKS = {12:(2,4), 24:(4,8)}


def series(n, speed, p):
    rows = []
    for i, pressure in enumerate(p):
        t = i*DT[n]
        h = 1.-t*speed
        rows.append(dict(step=str(i), time_code=str(t), height=str(h), bottom_pressure_E=str(pressure), phi_m=str(.5/h)))
    return rows


def raw(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, rows[0].keys(), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("ascii")


class Protocol(unittest.TestCase):
    def setUp(self):
        for module, field, value in ((native, "STEPS", OLD), (native, "SAMPLE_STEPS", OLD_MARKS),
                                     (half, "STEPS", HALF), (half, "MARKS", NEW_MARKS)):
            p = patch.object(module, field, value)
            p.start()
            self.addCleanup(p.stop)

    def test_preserves_dt_and_matches_every_original_displacement(self):
        a = series(12, .5, [0.]*3)
        b = series(12, .25, [0.]*5)
        self.assertEqual(half.validate_trace(native, raw(a), raw(b), 12, 1., .25, DT[12]), b)
        for k, wrong, i in (("time_code", ".13", 1), ("height",".25",3), ("phi_m",".33",2),
                            ("bottom_pressure_E","-1",1), ("bottom_pressure_E",".1",0), ("step","5",4)):
            with self.subTest(k=k), self.assertRaises(ValueError):
                bad = [dict(row) for row in b]
                bad[i][k] = wrong
                half.validate_trace(native, raw(a), raw(bad), 12, 1., .25, DT[12])
        with self.assertRaises(ValueError):
            half.validate_trace(native, raw(a), raw(b[:-1]), 12, 1., .25, DT[12])

    def test_native_union_and_shared_knots_keep_odd_original_f24(self):
        orig = {n:series(n,.5,[0.]*(OLD[n]+1)) for n in OLD}
        slow = {12:series(12,.25,[0.,.3,0.,0.,0.]), 24:series(24,.25,[0.,1.,0.,0.,0.,0.,0.,0.,0.])}
        result = half.compare_speeds(native, orig, slow, 1.)
        entire = result["half_native_2277"]
        shared = result["half_on_original_1139"]
        self.assertEqual((entire["samples"], shared["samples"]), (9,5))
        self.assertEqual(entire["peak"]["step_F24"], 1)
        self.assertAlmostEqual(entire["peak"]["signed_gap_MPa"], -8.5)
        self.assertEqual(shared["peak"]["step_F24_original"], 1)
        self.assertEqual(shared["peak"]["step_F12_half"], 1)
        self.assertEqual(shared["peak"]["signed_gap_MPa"], 3.)
        self.assertEqual(result["same_displacement_gap_change"]["max_pointwise_absolute_change"]["half_minus_original_gap_MPa"],3.)
        self.assertEqual([v["step_F24_half"] for v in shared["anchors"]], [4,8])

    def test_mass_weighted_velocity_and_residual(self):
        class Sample:
            def __call__(self, x, v, *rest):
                self.last_step = dict(step=1, floor_impulse=.625, lid_signed_impulse=-.125)
                return x, np.array([[0.,.5],[0.,.5]]), None, None, .1
        records = []
        call = half.ObservedAdvance(Sample(), records.append)
        call(None, np.array([[0.,-.5],[0.,.5]]), None, None, None, np.array([.5,1.5]), 10, .1, 1.)
        self.assertEqual(records[0], dict(step=1, particle_Py_before=.5, particle_Py_after=1., particle_delta_Py=.5,
                                         wall_signed_J=.5, residual_J=0.))
        for before, after in ((.5, .8), (float("nan"), 1.)):
            with self.assertRaises(ValueError):
                half.momentum_row(1, before, after, dict(step=1, floor_impulse=.625, lid_signed_impulse=-.125))

    def test_ratios_and_direct_delta_on_shared_time_window(self):
        walls = {n:[dict(floor_impulse=2., lid_signed_impulse=-1.) for _ in range(HALF[n])] for n in HALF}
        motions = {n:[dict(particle_Py_before=i, particle_Py_after=i+1) for i in range(HALF[n])] for n in HALF}
        walls[12][1] = dict(floor_impulse=1., lid_signed_impulse=0.)
        first = half.fixed_windows(walls, motions, NEW_MARKS, 1., DT)[0]
        self.assertIsNone(first["F12_native"]["floor_over_abs_lid"])
        self.assertEqual(first["F24_native"]["floor_over_abs_lid"], 2.)
        self.assertEqual(first["F24_same_duration_two_steps"]["direct_delta_Py_J"], 2.)
        self.assertEqual(first["F12_minus_F24_same_duration"]["direct_delta_Py_equivalent_MPa"], -80.)
        self.assertIsNone(half.fixed_windows(walls, {}, NEW_MARKS, 1., DT)[0]["F12_native"]["direct_delta_Py_J"])

    def test_native_arm_wrapper_restores_speed_and_binds_direct_table(self):
        solver = SimpleNamespace(WALL_SPEED=.5, WIDTH=1., LO=.125)
        seed = (np.zeros((1,2)), np.array([0]), np.ones(1))
        ctx = SimpleNamespace(solver=solver, kernel=SimpleNamespace(project_contacts=lambda friction: None))
        @contextmanager
        def bind(context, initial, project):
            context.seed, context.project = initial, project
            yield
        fine = SimpleNamespace(DT=DT, initial=lambda ctx,n:seed, bind_driver=bind,
                               write_json=lambda path,obj:path.write_text(json.dumps(obj),encoding="ascii"))
        ctx.floor = None
        class Zero:
            def __call__(self, x, v, *args):
                ctx.project(.5)
                step = self.audit["steps"] + 1
                self.audit.update(steps=step, floor_passes=2*step)
                self.lid_audit.update(steps=step, lid_passes=2*step)
                self.last_step = dict(step=step, floor_impulse=0., lid_downward_impulse=0., lid_signed_impulse=0.,
                                      top_gap_before=.1, top_gap_after=.1, floor_gap_after=.1, lid_grid_impulse_error=0.)
                return x, v, None, None, 0.
        def make(*args, **kwargs):
            self.assertEqual(solver.WALL_SPEED,.25)
            op = Zero()
            op.audit = dict(steps=0,floor_passes=0,positive_passes=0,accumulated_impulse=0.,max_penetration=0.,
                            max_grid_impulse_error=0.,max_g2p_momentum_error=0.)
            op.lid_audit = dict(steps=0,lid_passes=0,positive_passes=0,accumulated_downward_impulse=0.,
                                max_clock_error=0.,max_grid_impulse_error=0.,max_penetration=0.)
            return op
        def driver(label, n, budget, dest, advance):
            self.assertEqual(budget,900)
            x, ids, mass = ctx.seed(n)
            dest.mkdir()
            (dest/"trace.csv").write_bytes(raw(series(n,solver.WALL_SPEED,[0.]*(HALF[n]+1))))
            v = np.zeros_like(x)
            for i in range(1,HALF[n]+2):
                h = solver.WIDTH-i*DT[n]*solver.WALL_SPEED
                x,v,_,_,_ = advance(x,v,None,None,ids,mass,10*n,DT[n],solver.LO+h)
        ctx.driver = SimpleNamespace(run_arm=driver)
        prior = {12:raw(series(12,.5,[0.]*3))}
        identity = dict(half_wall_speed=.25)
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder)/"F12"
            half.run_arm(native,fine,ctx,SimpleNamespace(make_advance=make),prior,identity,12,dest)
            self.assertEqual(solver.WALL_SPEED,.5)
            self.assertEqual(native.STEPS,OLD)
            rows,walls,motion,rec=half.read_half_arm(native,fine,ctx,identity,12,dest,prior[12])
            self.assertEqual((len(rows),len(walls),len(motion)),(5,4,4))
            self.assertEqual(json.loads((dest/"half_speed_receipt.json").read_bytes()),rec)
            path = dest/"particle_momentum.csv"
            data = native.rows(path.read_bytes())
            data[1]["particle_Py_before"]="1"
            path.write_bytes(raw(data))
            with self.assertRaisesRegex(ValueError,"continuity"):
                half.read_half_arm(native,fine,ctx,identity,12,dest,prior[12])


if __name__ == "__main__":
    unittest.main()
