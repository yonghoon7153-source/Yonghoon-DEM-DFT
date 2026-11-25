"""Tests written before the thin driver (reg1 contact mini · reg2-a unloading schedule).

Every MPM call in this file is a truncated schedule of a few steps (wiring checks).  No
registered arm is run to completion, and no number produced here is a physics result.
The registered numbers below are transcribed from the two registration drafts; a separate
test checks that the drafts still carry the same text.
"""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import shutil
import tempfile
from types import ModuleType
import unittest
from unittest import mock

import numpy as np


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REG1 = HERE.parent / "reg1_contact_mini_20261125.md"
REG2 = HERE.parent / "reg2_unloading_sf_20261125.md"
README = HERE.parent / "README.md"
_CACHE = {}


def drv():
    if "drv" not in _CACHE:
        spec = importlib.util.spec_from_file_location("suyoung_registration_driver_under_test", HERE / "driver.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _CACHE["drv"] = module
    return _CACHE["drv"]


def eng():
    if "eng" not in _CACHE:
        _CACHE["eng"] = drv().Engine(REPO)
    return _CACHE["eng"]


def arm(name):
    return {a.name: a for a in drv().all_arms()}[name]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def make_arm(geometry, contact, cells, material="P", load_div=1, unload_div=None):
    reg = "reg2" if geometry == "BED" else "reg1"
    return drv().Arm(reg=reg, name=f"TEST-{geometry}-{contact}-{material}-{cells:02d}", geometry=geometry,
                     contact=contact, material=material, cells=cells, load_div=load_div, unload_div=unload_div)


def exec_pinned(relative, name):
    path = REPO / relative
    raw = path.read_bytes()
    assert sha(raw) == drv().SOURCES[relative], relative
    module = ModuleType(name)
    module.__file__ = str(path)
    exec(compile(raw, str(path), "exec"), module.__dict__)
    return module


def trace_rows(folder):
    with (folder / "trace.csv").open(newline="", encoding="ascii") as stream:
        return list(csv.reader(stream))


CELLS1 = (8, 16, 24, 32, 48)
CELLS2 = (12, 16, 24, 36)
# reg1 §3 arm table (registration order): geometry, contact, materials, speed divisor,
# steps 8 -> 48 cells, per-arm limit seconds 8 -> 48 cells.
REG1_TABLE = (
    ("G1", "PLATE", ("P",), 1, (454, 908, 1361, 1815, 2722), (600, 600, 600, 600, 600)),
    ("G1", "PLATE", ("P", "E"), 4, (1815, 3630, 5444, 7259, 10888), (600, 600, 600, 600, 1380)),
    ("G2", "S", ("P",), 1, (908, 1815, 2722, 3630, 5444), (600, 600, 600, 600, 1440)),
    ("G2", "F2", ("P",), 1, (908, 1815, 2722, 3630, 5444), (600, 600, 600, 600, 1140)),
    ("G2", "S", ("P", "E"), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 1080, 2040, 5640)),
    ("G2", "F2", ("P", "E"), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 960, 1680, 4380)),
    ("G2", "F1", ("P",), 4, (3630, 7259, 10888, 14517, 21775), (600, 600, 960, 1680, 4380)),
)
REG1_TEXT = ("454 · 908 · 1,361 · 1,815 · 2,722", "1,815 · 3,630 · 5,444 · 7,259 · 10,888",
             "908 · 1,815 · 2,722 · 3,630 · 5,444", "3,630 · 7,259 · 10,888 · 14,517 · 21,775",
             "600 · 600 · 600 · 600 · 1,380", "600 · 600 · 600 · 600 · 1,440",
             "600 · 600 · 600 · 600 · 1,140", "600 · 600 · 1,080 · 2,040 · 5,640",
             "600 · 600 · 960 · 1,680 · 4,380", "197 · 797 · 1,793 · 3,209 · 7,213",
             "CPU 3.3–4.8 h", "**1.7–2.4 h**", "CPU 상한 4.2 h")
POINTS_PER_DISK = (197, 797, 1793, 3209, 7213)
# reg2 §3-5 per-arm limits in hours.
REG2_LIMIT_H = {("S", 36): 10, ("F2", 36): 6.5, ("C1", 36): 6.5, ("S", 24): 3, ("F2", 24): 2, ("C1", 24): 2,
                ("S", 16): 1, ("F2", 16): 1, ("C1", 16): 1, ("S", 12): .5, ("F2", 12): .5, ("C1", 12): .5}
REG2_REPORT_LIMIT_H = {"S": 6, "F2": 4}
REG2_TEXT = ("S36 10 h · F36 · C1-36 6.5 h · S24 3 h · F24 · C1-24 2 h · 16 칸 1 h · 12 칸 0.5 h · 보고 팔 S24 6 h · F24 4 h",
             "36 칸 18,633 걸음", "0.57672", "12 팔 CPU 16.0 h", "**약 8.1 h**", "벽시계 약 +2.4 h")
README_PREFIXES = {"scripts/dem_suyoung_sf2d_dev.py": "6e807323", "scripts/suyoung_u6_first_dev.py": "5db0f1bd",
                   "scripts/suyoung_multicontact_dev.py": "acf5c061", "scripts/suyoung_u6b_dev.py": "50f1a3ae",
                   "docs/reviews/suyoung_floor_contact_20261123/material_floor.py": "4b64bcfe"}


class PinTests(unittest.TestCase):
    def test_pins_are_the_readme_sources_and_the_current_bytes(self):
        pins = drv().SOURCES
        readme = README.read_text(encoding="utf-8")
        for path, prefix in README_PREFIXES.items():
            self.assertTrue(pins[path].startswith(prefix), path)
            self.assertIn(f"`{path}` {prefix}", readme)
        for path, pin in pins.items():
            self.assertEqual(sha((REPO / path).read_bytes()), pin, path)

    def test_byte_pin_mismatch_is_refused(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for path in drv().SOURCES:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / path, root / path)
            drv().Engine(root)
            for path in ("docs/reviews/suyoung_floor_contact_20261123/material_floor.py",
                         "scripts/dem_suyoung_sf2d_dev.py"):
                original = (root / path).read_bytes()
                (root / path).write_bytes(original + b"\n")
                with self.assertRaises(ValueError) as caught:
                    drv().Engine(root)
                self.assertIn(path, str(caught.exception))
                (root / path).write_bytes(original)
            (root / "scripts/suyoung_multicontact_dev.py").unlink()
            with self.assertRaises((ValueError, FileNotFoundError)):
                drv().Engine(root)


class PlanTests(unittest.TestCase):
    def test_reg1_fifty_arms_steps_and_limits(self):
        arms = drv().reg1_arms()
        self.assertEqual(len(arms), 50)
        self.assertEqual(len({a.name for a in arms}), 50)
        expected = {}
        for geometry, contact, materials, div, steps, limits in REG1_TABLE:
            for material in materials:
                for cells, n, limit in zip(CELLS1, steps, limits, strict=True):
                    expected[(geometry, contact, material, div, cells)] = (n, limit)
        self.assertEqual(len(expected), 50)
        seen = {}
        for a in arms:
            p = eng().plan(a)
            seen[(a.geometry, a.contact, a.material, a.load_div, a.cells)] = (p["steps"], p["limit_s"])
            disks = 1 if a.geometry == "G1" else 2
            self.assertEqual(p["points"], disks * POINTS_PER_DISK[CELLS1.index(a.cells)], a.name)
            self.assertEqual(p["grid"], 10 * a.cells)
        self.assertEqual(seen, expected)
        longest = max(arms, key=lambda a: eng().plan(a)["limit_s"])
        self.assertEqual(eng().plan(longest)["limit_s"], 5640)
        self.assertEqual({a.name for a in arms if eng().plan(a)["limit_s"] == 5640},
                         {"R1-G2-S-P-V4-48", "R1-G2-S-E-V4-48"})

    def test_reg1_speeds_and_section7_totals(self):
        v0 = eng().plan(arm("R1-G1-PLATE-P-V0-08"))
        v4 = eng().plan(arm("R1-G1-PLATE-P-V4-08"))
        self.assertEqual(round(v0["v_over_cP"], 5), .01025)
        self.assertEqual(round(v4["v_over_cP"], 5), .00256)
        totals = drv().plan_totals(eng(), drv().reg1_arms())
        self.assertEqual((round(totals["cpu_low_h"], 1), round(totals["cpu_high_h"], 1)), (3.3, 4.8))
        self.assertEqual((round(totals["wall2_low_h"], 1), round(totals["wall2_high_h"], 1)), (1.7, 2.4))
        no24 = drv().plan_totals(eng(), [a for a in drv().reg1_arms() if a.cells != 24])
        self.assertEqual(round(no24["cpu_high_h"], 1), 4.2)

    def test_reg2_arms_limits_and_steps(self):
        arms = drv().reg2_arms()
        self.assertEqual(len(arms), 14)
        main = [a for a in arms if a.unload_div == 1]
        report = [a for a in arms if a.unload_div == 4]
        self.assertEqual(len(main), 12)
        self.assertEqual(sorted((a.contact, a.cells) for a in report), [("F2", 24), ("S", 24)])
        for a in main:
            self.assertEqual(eng().plan(a)["limit_s"], REG2_LIMIT_H[(a.contact, a.cells)] * 3600, a.name)
        for a in report:
            self.assertEqual(eng().plan(a)["limit_s"], REG2_REPORT_LIMIT_H[a.contact] * 3600, a.name)
        p36 = eng().plan(arm("R2-BED-S-P-V0-36"))
        self.assertEqual(p36["steps"], 18633)
        self.assertEqual(round(p36["height_at_stop_nominal"], 5), .57672)
        totals = drv().plan_totals(eng(), main)
        self.assertEqual(round(totals["cpu_high_h"], 1), 16.0)
        self.assertEqual(round(totals["wall2_high_h"], 1), 8.1)
        both = drv().plan_totals(eng(), arms)
        self.assertEqual(round(both["wall2_high_h"] - totals["wall2_high_h"], 1), 2.4)

    def test_registration_text_still_carries_the_transcribed_numbers(self):
        text1 = REG1.read_text(encoding="utf-8")
        text2 = REG2.read_text(encoding="utf-8")
        for snippet in REG1_TEXT:
            self.assertIn(snippet, text1)
        for snippet in REG2_TEXT:
            self.assertIn(snippet, text2)

    def test_check_only_matches_registration_without_an_mpm_step(self):
        out = io.StringIO()
        with mock.patch.object(drv().ArmRunner, "step", side_effect=AssertionError("MPM step in CHECK_ONLY")), \
                contextlib.redirect_stdout(out):
            rc = drv().main(["CHECK_ONLY", "--root", str(REPO)])
        text = out.getvalue()
        self.assertEqual(rc, 0, text)
        self.assertIn("PLAN_MATCHES_REGISTRATION reg1 50/50 reg2 14/14", text)
        self.assertIn("MPM_STEPS 0", text)
        self.assertIn("R1-G2-S-P-V4-48", text)
        self.assertIn("CHECK_ONLY_OK", text)

    def test_check_only_refuses_a_changed_source(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            for path in drv().SOURCES:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPO / path, root / path)
            target = root / "docs/reviews/suyoung_u6a_gates_20261123/gap_kernel.py"
            target.write_bytes(target.read_bytes() + b"# changed\n")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = drv().main(["CHECK_ONLY", "--root", str(root)])
            self.assertEqual(rc, 1)
            self.assertIn("SOURCE_PIN_MISMATCH", out.getvalue())


class GeometryTests(unittest.TestCase):
    def constants(self):
        c = eng().const
        return c.D, c.LO, c.W7, c.GP

    def test_one_disk_geometry(self):
        d, lo, w7, gp = self.constants()
        g = eng().geometry(arm("R1-G1-PLATE-P-V0-08"))
        self.assertEqual(g["centers"].shape, (1, 2))
        cx, cy = g["centers"][0]
        self.assertEqual(cx, .5)
        self.assertAlmostEqual(cy - d / 2 - lo, gp, delta=1e-15)
        self.assertAlmostEqual(lo + g["h0"] - (cy + d / 2), gp, delta=1e-15)
        self.assertEqual(g["h0"], w7)
        self.assertAlmostEqual(g["u_geo"], 2 * gp, delta=1e-17)
        self.assertAlmostEqual(g["u_end"], .2 * d + 2 * gp, delta=1e-17)
        self.assertAlmostEqual(g["lo"], .15, delta=1e-15)
        self.assertAlmostEqual(g["lo"] + g["width"], .85, delta=1e-15)
        self.assertAlmostEqual(cx - g["lo"], 3.5 * d, delta=1e-12)
        self.assertEqual(g["upper"], 0)
        runner = drv().ArmRunner(eng(), arm("R1-G1-PLATE-P-V0-08"))
        self.assertEqual(len(runner.ids), 197)
        self.assertTrue(np.all(runner.ids == 0) and np.all(runner.fields == 0))
        self.assertLessEqual(float(np.max(np.hypot(*(runner.x - g["centers"][0]).T))), d / 2 + 1e-15)
        self.assertEqual(len(runner.boundary.owners), 256)
        self.assertTrue(np.all(runner.boundary.groups == 0))

    def test_two_disk_geometry(self):
        d, lo, w7, gp = self.constants()
        g = eng().geometry(arm("R1-G2-F2-P-V0-08"))
        (x0, y0), (x1, y1) = g["centers"]
        self.assertEqual((x0, x1), (.5, .5))
        self.assertAlmostEqual(y0 - d / 2 - lo, gp, delta=1e-15)
        self.assertAlmostEqual((y1 - d / 2) - (y0 + d / 2), 2 * gp, delta=1e-15)
        self.assertAlmostEqual(lo + g["h0"] - (y1 + d / 2), gp, delta=1e-15)
        self.assertEqual(g["h0"], 2 * w7)
        self.assertAlmostEqual(g["u_geo"], 4 * gp, delta=1e-17)
        self.assertAlmostEqual(g["u_end"], 2 * (.2 * d + 2 * gp), delta=1e-17)
        self.assertEqual(g["upper"], 1)
        f = drv().ArmRunner(eng(), arm("R1-G2-F2-P-V0-08"))
        s = drv().ArmRunner(eng(), arm("R1-G2-S-P-V0-08"))
        self.assertEqual(np.bincount(f.ids).tolist(), [197, 197])
        self.assertTrue(np.array_equal(f.fields, f.ids) and np.all(s.fields == 0))
        self.assertTrue(np.array_equal(f.boundary.groups, np.repeat(np.arange(2), 256)))
        self.assertTrue(np.all(s.boundary.groups == 0))
        self.assertTrue(np.array_equal(f.boundary.owners, s.boundary.owners))
        lower, upper = f.x[f.ids == 0], f.x[f.ids == 1]
        self.assertGreaterEqual(float(upper[:, 1].min() - lower[:, 1].max()), 2 * gp - 1e-15)

    def test_seed_rewrite_equals_native_bed_seed(self):
        c = eng().const
        centers = drv().bed_seed_centers(c.LO, c.BED_WIDTH)
        for cells in (8, 12, 16):
            mine = drv().seed_disks(cells, centers, c.D)
            native = eng().solver.seed(cells)
            for a, b in zip(mine, native, strict=True):
                self.assertEqual(a.dtype.kind, b.dtype.kind)
                self.assertEqual(a.tobytes(), b.tobytes(), cells)

    def test_disk_boundary_rewrite_equals_original_on_49_disks(self):
        c = eng().const
        relative = "docs/reviews/suyoung_floor_contact_20261123/material_floor.py"
        floor = exec_pinned(relative, "test_original_floor")
        raw = (REPO / relative).read_bytes()
        guard = b"cells not in (8, 12, 16, 24) or not"
        self.assertEqual(raw.count(guard), 1)
        relaxed = ModuleType("test_guard_relaxed_floor")
        relaxed.__file__ = str(REPO / relative)
        exec(compile(raw.replace(guard, b"cells not in (8, 12, 16, 24, 36) or not"), relaxed.__file__, "exec"),
             relaxed.__dict__)
        centers = drv().bed_boundary_centers(c.LO, c.BED_WIDTH)
        for cells, original in ((8, floor), (12, floor), (16, floor), (24, floor), (36, relaxed)):
            x, ids, _ = eng().solver.seed(cells)
            reference = original.disk_boundary(eng().solver, x, ids, cells)
            mine = drv().disk_boundary(floor, c.D, x, ids, centers)
            for key in ("owners", "positions", "groups"):
                self.assertEqual(getattr(mine, key).tobytes(), getattr(reference, key).tobytes(), (cells, key))


class ScheduleTests(unittest.TestCase):
    def test_reg1_schedule_is_a_monotone_press(self):
        a = arm("R1-G2-S-P-V4-16")
        p, g = eng().plan(a), eng().geometry(a)
        rows = eng().schedule(a, 1.)
        self.assertEqual(len(rows), p["steps"])
        speed = p["load_speed"]
        for k, (step, phase, height, wall) in enumerate(rows, 1):
            self.assertEqual((step, phase, wall), (k, "LOAD", speed))
            self.assertEqual(height, g["h0"] - p["dt"] * k * speed)
        self.assertGreaterEqual(g["h0"] - rows[-1][2], g["u_end"])
        self.assertLess(g["h0"] - rows[-2][2], g["u_end"])

    def check_unloading(self, a, unload_speed):
        p = eng().plan(a)
        x, ids, volume = eng().solver.seed(a.cells)
        total = float(volume.sum())
        width = eng().const.BED_WIDTH
        rows = eng().schedule(a, total)
        n_load = sum(r[1] == "LOAD" for r in rows)
        self.assertEqual([r[1] for r in rows], ["LOAD"] * n_load + ["UNLOAD"] * (len(rows) - n_load))
        self.assertEqual(len(rows), p["steps"])
        self.assertEqual(n_load, p["n_load"])
        self.assertEqual([r[0] for r in rows], list(range(1, len(rows) + 1)))
        dt, v0 = p["dt"], p["load_speed"]
        for k in range(1, n_load + 1):
            self.assertEqual(rows[k - 1][2], width - dt * k * v0)
            self.assertEqual(rows[k - 1][3], v0)
        phi = [total / (width * r[2]) for r in rows[:n_load]]
        self.assertGreaterEqual(phi[-1], .95)
        self.assertTrue(all(value < .95 for value in phi[:-1]))
        h_u = rows[n_load - 1][2]
        for m, r in enumerate(rows[n_load:], 1):
            self.assertEqual(r[2], h_u + dt * m * unload_speed)
            self.assertEqual(r[3], -unload_speed)
        self.assertGreaterEqual(rows[-1][2] - h_u, .06)
        self.assertLess(rows[-2][2] - h_u, .06)
        self.assertEqual(len(rows) - n_load, math.ceil(.06 / (unload_speed * dt)))

    def test_reg2_schedule_press_stop_reverse(self):
        a = arm("R2-BED-S-P-V0-12")
        self.check_unloading(a, eng().plan(a)["load_speed"])

    def test_reg2_report_arm_unloads_at_quarter_speed(self):
        a = arm("R2-BED-F2-P-U4-24")
        p = eng().plan(a)
        self.assertEqual(p["unload_speed"], p["load_speed"] / 4)
        self.check_unloading(a, p["unload_speed"])

    def test_reversal_reaches_the_plate_operator(self):
        a = make_arm("BED", "S", 8, unload_div=1)
        runner = drv().ArmRunner(eng(), a)
        rows = eng().schedule(a, runner.total, n_load=3, n_unload=3)
        self.assertEqual([r[1] for r in rows], ["LOAD"] * 3 + ["UNLOAD"] * 3)
        for row in rows:
            runner.step(*row)
        v0 = eng().plan(a)["load_speed"]
        self.assertEqual(runner.observer.wall_speeds, [v0] * 6 + [-v0] * 6)
        lids = runner.observer.lids
        self.assertEqual(lids[::2], [eng().const.LO + r[2] for r in rows])
        self.assertTrue(lids[4] < lids[6] < lids[8] < lids[10])


class KernelIdentityTests(unittest.TestCase):
    def test_sources_unchanged_and_only_declared_substitutions(self):
        f2 = drv().ArmRunner(eng(), arm("R1-G2-F2-P-V0-08"))
        f1 = drv().ArmRunner(eng(), arm("R1-G2-F1-P-V4-08"))
        for runner in (f2, f1):
            for row in eng().schedule(runner.arm, 1.)[:3]:
                runner.step(*row)
        for path, pin in drv().SOURCES.items():
            self.assertEqual(sha((REPO / path).read_bytes()), pin, path)
        fresh_floor = exec_pinned("docs/reviews/suyoung_floor_contact_20261123/material_floor.py", "fresh_floor")
        for name, obj in vars(fresh_floor).items():
            if isinstance(obj, type):
                for attr, member in vars(obj).items():
                    if callable(member) and hasattr(member, "__code__"):
                        self.assertEqual(getattr(f2.floor, name).__dict__[attr].__code__, member.__code__)
            elif callable(obj) and hasattr(obj, "__code__"):
                mine = getattr(f2.floor, name)
                if name == "_other_walls":
                    self.assertIsNot(mine, obj)
                    self.assertEqual(mine.__wrapped__.__code__, obj.__code__)
                else:
                    self.assertEqual(mine.__code__, obj.__code__, name)
        fresh_kernel = exec_pinned("scripts/suyoung_multicontact_dev.py", "fresh_kernel")
        material = exec_pinned("scripts/dem_suyoung_sf2d_dev.py", "fresh_material")
        for name, obj in vars(fresh_kernel).items():
            if callable(obj) and hasattr(obj, "__code__"):
                if name == "_pair_impulse":
                    self.assertEqual(f1.kernel._pair_impulse.__wrapped__.__code__, material.pair_impulse.__code__)
                else:
                    self.assertEqual(getattr(f1.kernel, name).__code__, obj.__code__, name)
        fresh_gap = eng().gap.GapProjector(fresh_kernel).derived
        for name, obj in vars(fresh_gap).items():
            if callable(obj) and hasattr(obj, "__code__"):
                mine = getattr(f2.projector.derived, name)
                if name == "_pair_impulse":
                    self.assertEqual(mine.__wrapped__.__code__, obj.__code__)
                else:
                    self.assertEqual(mine.__code__, obj.__code__, name)
        self.assertEqual(set(vars(f2.view)), {"model", "LO", "WIDTH", "WALL_SPEED", "DIAMETER", "project_contacts"})
        self.assertIs(f2.view.model, eng().solver.model)
        self.assertEqual((f2.view.LO, f2.view.DIAMETER), (eng().solver.LO, eng().solver.DIAMETER))
        self.assertEqual(f2.view.WIDTH, eng().geometry(f2.arm)["width"])
        bed = drv().ArmRunner(eng(), arm("R2-BED-C1-P-V0-12"))
        self.assertEqual(bed.view.WIDTH, eng().solver.WIDTH)
        self.assertEqual(bed.view.WALL_SPEED, eng().solver.WALL_SPEED)

    def test_elastic_material_turns_off_the_return_mapping_only(self):
        elastic = drv().ArmRunner(eng(), arm("R1-G1-PLATE-E-V4-08")).material
        plastic = eng().solver.model
        self.assertIsNot(elastic, plastic)
        for name, value in vars(plastic).items():
            if name.isupper():
                if name == "YIELD":
                    self.assertEqual(getattr(elastic, name), math.inf)
                else:
                    self.assertEqual(getattr(elastic, name), value, name)
            elif callable(value) and hasattr(value, "__code__"):
                self.assertEqual(getattr(elastic, name).__code__, value.__code__, name)
        trial = np.array([[[1.3, .1], [0., .7]]])
        self.assertFalse(np.allclose(plastic.plastic_project(trial), trial, rtol=1e-6, atol=0))
        np.testing.assert_allclose(elastic.plastic_project(trial), trial, rtol=1e-13, atol=1e-15)

    def test_observers_do_not_change_the_physics(self):
        # Windows reach past the first floor load (wiring fact at 8 cells), so floor, plate,
        # inter-disk contact and side walls all act inside the compared steps.
        for name, steps in (("R1-G2-F2-P-V0-08", 160), ("R1-G2-S-E-V4-08", 160), ("R1-G2-F1-P-V4-08", 160),
                            ("R1-G1-PLATE-P-V0-08", 60)):
            a = arm(name)
            watched = drv().ArmRunner(eng(), a, observe=True)
            plain = drv().ArmRunner(eng(), a, observe=False)
            floor_loaded = impulses = 0
            for row in eng().schedule(a, 1.)[:steps]:
                p1, record = watched.step(*row)
                p2, none = plain.step(*row)
                self.assertIsNone(none)
                self.assertEqual(p1, p2, (name, row[0]))
                floor_loaded += p1 > 0
                impulses += (record["interfield_normal_impulse"] or 0.) > 0
                self.assertEqual(isinstance(record["sigma_yy_avg_MPa"], float), a.geometry == "G1", name)
            self.assertGreater(floor_loaded, 0, name)
            if a.contact in ("F1", "F2"):
                self.assertGreater(impulses, 0, name)
            for key in ("x", "v", "affine", "elastic"):
                self.assertEqual(getattr(watched, key).tobytes(), getattr(plain, key).tobytes(), (name, key))

    def test_c1_differs_from_f2_only_in_the_friction_argument(self):
        seen = {}
        for contact in ("F2", "C1"):
            a = make_arm("G2", contact, 8)
            runner = drv().ArmRunner(eng(), a)
            calls = []
            original = runner.projector.project

            def spy(*args, _calls=calls, _original=original):
                _calls.append(args[-1])
                return _original(*args)
            runner.projector.project = spy
            for row in eng().schedule(a, 1.)[:5]:
                runner.step(*row)
            seen[contact] = calls
        self.assertEqual(seen["F2"], [.5] * 5)
        self.assertEqual(seen["C1"], [0.] * 5)

    def native_bed_trace(self, contact, cells, steps, dest):
        """Original setting-2 loop: u6b run_arm + material floor + S or F2 contact, stopped after `steps`."""
        u6b = exec_pinned("scripts/suyoung_u6b_dev.py", "native_u6b")
        solver = u6b.fixed_solver()
        floor = exec_pinned("docs/reviews/suyoung_floor_contact_20261123/material_floor.py", "native_floor")
        arrays = solver.seed(cells)
        dt = u6b.step_size(solver, cells)

        class Stop(Exception):
            pass

        if contact == "F2":
            kernel = exec_pinned("scripts/suyoung_multicontact_dev.py", "native_kernel")
            gap = exec_pinned("docs/reviews/suyoung_u6a_gates_20261123/gap_kernel.py", "native_gap")
            advance_floor = floor.make_advance(solver, cells)
            projector = gap.GapProjector(kernel)

            def project(*args):
                self.assertEqual(args[-1], .5)
                return projector.project(advance_floor.boundary, dt, *args)
            name = "F"
        else:
            s2 = exec_pinned("docs/reviews/suyoung_u6b_setting2_20261123/setting2_u6b.py", "native_s2")
            boundary = floor.disk_boundary(solver, arrays[0], arrays[1], cells)
            s2.merge_surface_fields(boundary, arrays[1])
            advance_floor = floor.make_advance(solver, cells, boundary=boundary)
            project = s2.single_field_contact
            name = "S"
        done, last = 0, None

        def advance(*args):
            nonlocal done, last
            if done == steps:
                raise Stop
            last = advance_floor(*args)
            done += 1
            return last
        saved = solver.seed, solver.project_contacts, u6b.fixed_solver
        solver.seed, solver.project_contacts, u6b.fixed_solver = (lambda n: arrays), project, (lambda: solver)
        try:
            u6b.run_arm(name, cells, 3600, dest, advance=advance)
        except Stop:
            pass
        finally:
            solver.seed, solver.project_contacts, u6b.fixed_solver = saved
        return trace_rows(dest), last[:4]

    def test_bed_loading_rows_equal_the_native_loop(self):
        # 8-cell bed (wiring fact): the floor first loads at step 261 (S) and 332 (F2), so these
        # windows compare floor, merged S outline, gap projector and plate together.
        with tempfile.TemporaryDirectory() as name:
            tmp = Path(name)
            for contact, steps in (("S", 270), ("F2", 340)):
                native, state = self.native_bed_trace(contact, 8, steps, tmp / ("native_" + contact))
                self.assertEqual(len(native), steps + 2)
                self.assertTrue(any(float(row[3]) > 0 for row in native[2:]), contact)
                a = make_arm("BED", contact, 8, unload_div=1)
                schedule = eng().schedule(a, float(eng().solver.seed(8)[2].sum()), n_load=steps, n_unload=0)
                result = drv().run_arm(eng(), a, tmp / ("mine_" + contact), schedule=schedule, kind="TEST")
                self.assertEqual(result["steps_done"], steps)
                mine = trace_rows(tmp / ("mine_" + contact))
                self.assertEqual([row[:5] for row in mine], native, contact)
                self.assertEqual(result["final_state_sha256"], drv().array_sha(*state), contact)


class RunTests(unittest.TestCase):
    def test_smoke_runs_the_smallest_arm_for_wiring_only(self):
        with tempfile.TemporaryDirectory() as name:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                rc = drv().main(["SMOKE", "--root", str(REPO), "--out", str(Path(name) / "smoke")])
            self.assertEqual(rc, 0, out.getvalue())
            self.assertIn("SMOKE_RAN arm=R1-G1-PLATE-P-V0-08 steps=5", out.getvalue())
            self.assertIn("wiring only", out.getvalue())
            result = json.loads((Path(name) / "smoke" / "result.json").read_text())
            self.assertEqual((result["schedule_kind"], result["steps_done"], result["status"]),
                             ("SMOKE", 5, "COMPLETE"))
            self.assertIs(result["physics_result"], False)
            self.assertEqual(len(trace_rows(Path(name) / "smoke")), 7)

    def test_truncated_run_records_monitors_first_force_and_receipt(self):
        a = arm("R1-G2-F2-P-V0-08")
        with tempfile.TemporaryDirectory() as name:
            out = Path(name) / "arm"
            schedule = eng().schedule(a, 1.)[:60]
            result = drv().run_arm(eng(), a, out, schedule=schedule, kind="TEST")
            rows = trace_rows(out)
            self.assertEqual(tuple(rows[0]), drv().COLUMNS)
            self.assertEqual(len(rows), 62)
            self.assertEqual([int(r[0]) for r in rows[1:]], list(range(61)))
            g = eng().geometry(a)
            self.assertEqual(result["first_force"]["u_geo"], g["u_geo"])
            self.assertEqual(result["first_force"]["threshold_MPa"], .008)
            self.assertEqual(result["observer_calls"], dict(other_walls=120, contact=60))
            self.assertEqual(result["floor_audit"]["steps"], 60)
            receipt = json.loads((out / "receipt.json").read_text())
            self.assertEqual(receipt["trace_sha256"], result["trace_sha256"])
            self.assertEqual(receipt["trace_sha256"], sha((out / "trace.csv").read_bytes()))
            self.assertEqual(receipt["first_force_u_on"], result["first_force"]["u_on"])
            self.assertEqual(receipt["rows"], 61)
            monitors = result["monitors"]
            for key in ("max_abs_upper_dx_over_D", "side_wall_hits_total", "max_floor_penetration",
                        "max_abs_momentum_residual", "technical_hold_reasons"):
                self.assertIn(key, monitors)
            index = {k: i for i, k in enumerate(drv().COLUMNS)}
            momentum = max(abs(float(r[index["momentum_y"]])) for r in rows[2:])
            impulses = max(max(abs(float(r[index["bottom_force"]])), abs(float(r[index["top_force"]])))
                           for r in rows[2:]) * eng().plan(a)["dt"]
            self.assertGreater(max(momentum, impulses), 0.)
            self.assertLessEqual(monitors["max_abs_momentum_residual"], 1e-10 * max(momentum, impulses))
            self.assertEqual([p["pair"] for p in result["last_step_pairs"]], [[0, 1]])
            self.assertEqual(result["stage3_go"], False)
            self.assertEqual(result["three_dimensional_go"], False)

    def test_bed_run_records_the_press_stop_and_reversal(self):
        a = make_arm("BED", "S", 8, unload_div=1)
        rows = eng().schedule(a, float(eng().solver.seed(8)[2].sum()), n_load=3, n_unload=2)
        with tempfile.TemporaryDirectory() as name:
            out = Path(name) / "bed"
            result = drv().run_arm(eng(), a, out, schedule=rows, kind="TEST")
            u = result["unloading"]
            self.assertEqual((u["k_u"], u["h_u"], u["unload_steps_done"]), (3, rows[2][2], 2))
            self.assertEqual(u["unload_travel_done"], rows[4][2] - rows[2][2])
            self.assertEqual(u["unload_speed"], eng().const.V0)
            phase = drv().COLUMNS.index("phase")
            self.assertEqual([r[phase] for r in trace_rows(out)[1:]],
                             ["INITIAL", "LOAD", "LOAD", "LOAD", "UNLOAD", "UNLOAD"])
            receipt = json.loads((out / "receipt.json").read_text())
            self.assertEqual((receipt["load_steps_in_trace"], receipt["unload_steps_in_trace"]), (3, 2))
            self.assertIsNone(result["first_force"])
            self.assertIsNone(result["monitors"]["max_abs_upper_dx_over_D"])

    def test_time_limit_and_failure_paths(self):
        a = arm("R1-G1-PLATE-P-V0-08")
        with tempfile.TemporaryDirectory() as name:
            result = drv().run_arm(eng(), a, Path(name) / "late", schedule=eng().schedule(a, 1.)[:3],
                                   kind="TEST", limit_s=0.)
            self.assertEqual((result["status"], result["steps_done"]), ("TIME_LIMIT", 0))
            self.assertTrue((Path(name) / "late" / "result.json").is_file())
            calls = {"n": 0}
            original = drv().ArmRunner.step

            def failing(runner, *args, **kwargs):
                calls["n"] += 1
                if calls["n"] == 2:
                    raise ArithmeticError("injected")
                return original(runner, *args, **kwargs)
            with mock.patch.object(drv().ArmRunner, "step", failing):
                with self.assertRaises(ArithmeticError):
                    drv().run_arm(eng(), a, Path(name) / "fail", schedule=eng().schedule(a, 1.)[:3], kind="TEST")
            incomplete = json.loads((Path(name) / "fail" / "incomplete.json").read_text())
            self.assertEqual((incomplete["status"], incomplete["steps_done"]), ("INCOMPLETE", 1))
            self.assertIn("injected", incomplete["reason"])
            with self.assertRaises(FileExistsError):
                drv().run_arm(eng(), a, Path(name) / "fail", schedule=eng().schedule(a, 1.)[:1], kind="TEST")

    def test_cli_run_uses_registered_schedule_and_limit(self):
        with tempfile.TemporaryDirectory() as name:
            seen = {}

            def fake(engine, a, out, schedule=None, kind="RUN", limit_s=None, **kwargs):
                seen.update(arm=a.name, schedule=schedule, kind=kind, limit_s=limit_s, out=out)
                return {"status": seen.get("status", "COMPLETE")}
            with mock.patch.object(drv(), "run_arm", fake), contextlib.redirect_stdout(io.StringIO()):
                rc = drv().main(["RUN", "--root", str(REPO), "--arm", "R1-G2-S-E-V4-48",
                                 "--out", str(Path(name) / "a")])
            self.assertEqual(rc, 0)
            self.assertEqual((seen["arm"], seen["schedule"], seen["kind"], seen["limit_s"]),
                             ("R1-G2-S-E-V4-48", None, "RUN", None))

            def late(*args, **kwargs):
                return {"status": "TIME_LIMIT"}
            with mock.patch.object(drv(), "run_arm", late), contextlib.redirect_stdout(io.StringIO()):
                rc = drv().main(["RUN", "--root", str(REPO), "--arm", "R2-BED-C1-P-V0-12",
                                 "--out", str(Path(name) / "b")])
            self.assertEqual(rc, 3)

    def test_cli_usage_errors(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            drv().main(["BOGUS"])
        self.assertEqual(caught.exception.code, 2)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            drv().main(["RUN", "--out", "x"])
        self.assertEqual(caught.exception.code, 2)
        with tempfile.TemporaryDirectory() as name, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(drv().main(["RUN", "--root", str(REPO), "--arm", "R1-NOPE",
                                         "--out", str(Path(name) / "z")]), 2)

    def test_monitor_summary_flags_lateral_drift_and_side_walls(self):
        mini = drv().Monitors(mini=True)
        mini.update(1, dict(upper_dx_over_D=.004, side_wall_hits=0, floor_max_penetration=0.,
                            momentum_residual=1e-20))
        mini.update(2, dict(upper_dx_over_D=-.012, side_wall_hits=0, floor_max_penetration=1e-13,
                            momentum_residual=-2e-20))
        mini.update(3, dict(upper_dx_over_D=.001, side_wall_hits=2, floor_max_penetration=1e-13,
                            momentum_residual=0.))
        s = mini.summary()
        self.assertEqual((s["first_lateral_violation_step"], s["first_side_wall_step"]), (2, 3))
        self.assertEqual(s["max_abs_upper_dx_over_D"], .012)
        self.assertEqual(s["side_wall_hits_total"], 2)
        self.assertEqual(s["technical_hold_reasons"], ["LATERAL_OFFSET", "SIDE_WALL_CONTACT"])
        bed = drv().Monitors(mini=False)
        bed.update(1, dict(upper_dx_over_D=None, side_wall_hits=40, floor_max_penetration=0.,
                           momentum_residual=0.))
        self.assertEqual(bed.summary()["technical_hold_reasons"], [])


if __name__ == "__main__":
    unittest.main()
