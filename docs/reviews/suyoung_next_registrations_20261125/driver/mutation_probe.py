"""Mutation probe for test_driver.py: break the driver in memory and check that the named tests fail.

    python3 -I -X utf8 -B docs/reviews/suyoung_next_registrations_20261125/driver/mutation_probe.py

Nothing is written; every mutation patches a fresh in-memory copy of driver.py.  Each line
reports how many of the selected tests fail (all of them should).
"""
import importlib.util
import io
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(mutate, tests):
    t = load("probe_tests", HERE / "test_driver.py")
    d = load("probe_driver", HERE / "driver.py")
    mutate(d)
    t._CACHE.clear()
    t._CACHE["drv"] = d
    suite = unittest.TestSuite()
    for name in tests:
        cls, method = name.split(".")
        suite.addTest(getattr(t, cls)(method))
    result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
    return len(result.failures) + len(result.errors), result.testsRun


def unload_labelled_load(d):
    original = d.Engine.schedule
    d.Engine.schedule = lambda self, *a, **k: [(s, "LOAD", h, w) for s, _, h, w in original(self, *a, **k)]


def perturbing_observer(d):
    original = d.ArmRunner.install_observers

    def install(self):
        original(self)
        inner = self.floor._other_walls

        def nudged(solver, xy, gv, lid):
            inner(solver, xy, gv, lid)
            gv[:, 0] *= 1. + 2.**-50
        nudged.__wrapped__ = inner.__wrapped__
        self.floor._other_walls = nudged
    d.ArmRunner.install_observers = install


def seed_style_outline(d):
    d.bed_boundary_centers = d.bed_seed_centers


def short_limit(d):
    original = d.Engine._plan

    def plan(self, arm):
        p = original(self, arm)
        if p["reg"] == "reg1" and p["limit_s"] > 600:
            p["limit_s"] -= 60
        return p
    d.Engine._plan = plan


def early_stop(d):
    d.PHI_STOP = .949


def no_reversal(d):
    original = d.Engine.schedule
    d.Engine.schedule = lambda self, *a, **k: [(s, p, h, abs(w)) for s, p, h, w in original(self, *a, **k)]


def c1_keeps_friction(d):
    original = d.ArmRunner.contact

    def contact(self, ids, nodes, mass, grad, gv, centers, friction):
        if self.arm.contact == "C1":
            self.projector.project(self.boundary, self.dt, ids, nodes, mass, grad, gv, centers, friction)
            return None
        return original(self, ids, nodes, mass, grad, gv, centers, friction)
    d.ArmRunner.contact = contact


def flipped_top(d):
    original = d.ArmRunner.record

    def record(self, k, phase, height, pressure):
        self.observer.dv = [-x for x in self.observer.dv]
        return original(self, k, phase, height, pressure)
    d.ArmRunner.record = record


def plastic_e(d):
    d.elastic_material = lambda solver: solver.load_material()


def unmerged_s(d):
    original = d.ArmRunner.__init__

    def init(self, engine, arm, observe=True):
        merge = engine.s2.merge_surface_fields
        engine.s2.merge_surface_fields = lambda boundary, ids: None
        try:
            original(self, engine, arm, observe)
        finally:
            engine.s2.merge_surface_fields = merge
    d.ArmRunner.__init__ = init


CASES = (
    ("unload rows labelled LOAD", unload_labelled_load, ["RunTests.test_bed_run_records_the_press_stop_and_reversal"]),
    ("observer nudges the x velocity by 2^-50", perturbing_observer,
     ["KernelIdentityTests.test_observers_do_not_change_the_physics",
      "KernelIdentityTests.test_bed_loading_rows_equal_the_native_loop"]),
    ("outline uses the seed centre expression", seed_style_outline,
     ["GeometryTests.test_disk_boundary_rewrite_equals_original_on_49_disks"]),
    ("reg1 limit 60 s shorter above 600 s", short_limit,
     ["PlanTests.test_reg1_fifty_arms_steps_and_limits",
      "PlanTests.test_check_only_matches_registration_without_an_mpm_step"]),
    ("Φ_m stop at 0.949", early_stop,
     ["ScheduleTests.test_reg2_schedule_press_stop_reverse", "PlanTests.test_reg2_arms_limits_and_steps"]),
    ("plate not reversed", no_reversal,
     ["ScheduleTests.test_reg2_schedule_press_stop_reverse", "ScheduleTests.test_reversal_reaches_the_plate_operator"]),
    ("C1 keeps friction 0.5", c1_keeps_friction,
     ["KernelIdentityTests.test_c1_differs_from_f2_only_in_the_friction_argument"]),
    ("top impulse sign flipped", flipped_top,
     ["RunTests.test_truncated_run_records_monitors_first_force_and_receipt"]),
    ("E arm keeps the yield", plastic_e,
     ["KernelIdentityTests.test_elastic_material_turns_off_the_return_mapping_only"]),
    ("S outline not merged", unmerged_s,
     ["GeometryTests.test_two_disk_geometry", "KernelIdentityTests.test_bed_loading_rows_equal_the_native_loop"]),
)


def main():
    missed = 0
    for label, mutate, tests in CASES:
        failed, ran = run(mutate, tests)
        missed += failed != ran
        print(f"{label}: {failed}/{ran} selected tests fail")
    print("MUTATIONS_ALL_CAUGHT" if not missed else f"MUTATIONS_MISSED {missed}")
    return 0 if not missed else 1


if __name__ == "__main__":
    sys.exit(main())
