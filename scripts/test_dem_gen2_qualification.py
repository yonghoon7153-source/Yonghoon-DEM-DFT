"""Small synthetic checks only; not registered T5/T11 or research results."""
import math
from pathlib import Path
import types
import unittest

source = Path(__file__).with_name('dem_gen2_qualification.py')
q = types.ModuleType('g2q')
q.__file__ = str(source)
exec(compile(source.read_bytes(), str(source), 'exec'), q.__dict__)


class Geometry(unittest.TestCase):
    def test_sphere_lens_analytic(self):
        self.assertAlmostEqual(q.sphere_lens(1, 1, 1), 5 * math.pi / 12)
        self.assertEqual(q.sphere_lens(1, 1, 2), 0)
        self.assertAlmostEqual(q.sphere_lens(2, 1, 0), 4 * math.pi / 3)

    def test_contact_area_is_geometric_not_mechanical(self):
        self.assertAlmostEqual(q.contact_area(1, 1, 1), .75 * math.pi)
        self.assertEqual(q.contact_area(1, 1, 2), 0)
        with self.assertRaises(ValueError):
            q.contact_area(2, 1, .5)

    def test_wall_half_sphere(self):
        self.assertAlmostEqual(q.sphere_below_plane(1, 0), 2 * math.pi / 3)
        self.assertEqual(q.sphere_below_plane(1, -2), 0)
        self.assertAlmostEqual(q.sphere_below_plane(1, 2), 4 * math.pi / 3)

    def test_union_three_coincident_not_pair_subtraction(self):
        one = [(0., 0., 0., 1.)]
        a = q.union_mc(one, (-1, 1, -1, 1, -1, 1), 6000, 17)
        b = q.union_mc(one * 3, (-1, 1, -1, 1, -1, 1), 6000, 17)
        self.assertEqual(a, b)
        self.assertLess(abs(a['volume'] - 4 * math.pi / 3), .2)

    def test_union_wall_clip_and_reproducibility(self):
        a = q.union_mc([(0, 0, 0, 1)], (-1, 1, -1, 1, -1, 0), 6000, 19)
        self.assertLess(abs(a['volume'] - 2 * math.pi / 3), .15)
        self.assertEqual(a, q.union_mc([(0, 0, 0, 1)], (-1, 1, -1, 1, -1, 0), 6000, 19))

    def test_interval_edges_and_coverage_denominator(self):
        lo, hi = q.wilson(0, 100, 1.96)
        self.assertEqual(lo, 0)
        self.assertGreater(hi, 0)
        c = q.coverage([(0, 1), None, (.6, .9)], .5)
        self.assertEqual(c, {'covered': 1, 'planned': 3, 'missing': 1, 'coverage': 1/3})
        with self.assertRaises(ValueError):
            q.coverage([], .5)

    def test_invalid_geometry_or_seed(self):
        for bad in (0, -1, math.nan, math.inf, True):
            with self.assertRaises(ValueError):
                q.sphere_lens(bad, 1, 1)
        for n, seed in ((0, 1), (5.5, 1), (5, True)):
            with self.assertRaises(ValueError):
                q.union_mc([(0, 0, 0, 1)], (-1, 1, -1, 1, -1, 1), n, seed)

    def test_large_finite_scale_and_overflow_refusal(self):
        self.assertAlmostEqual(q.sphere_lens(1e100, 1e100, 1e100)/1e300, 5*math.pi/12)
        self.assertAlmostEqual(q.sphere_lens(1e-100, 1e-100, 1e-100)/1e-300, 5*math.pi/12)
        self.assertAlmostEqual(q.sphere_lens(1e308, 1, 0), 4*math.pi/3)
        with self.assertRaises(ValueError):
            q.sphere_lens(1e200, 1e200, 1e200)
        with self.assertRaises(ValueError):
            q.wilson(1, 2, 1e308)


class Control(unittest.TestCase):
    def test_force_units_and_sign_saturation(self):
        self.assertEqual(q.target_force(300, .0025), 750)
        self.assertEqual(q.servo_velocity(0, 750, 30, .01), -.01)
        self.assertEqual(q.servo_velocity(1500, 750, 30, .01), .01)
        self.assertEqual(q.servo_velocity(750, 750, 30, .01), 0)

    def test_zero_error_large_gain_does_not_move(self):
        self.assertEqual(q.servo_velocity(1., 1., 1e308, 10.), 0.)
        self.assertEqual(q.servo_velocity(2., 1., 1e308, 10.), 10.)
        self.assertAlmostEqual(q.target_force(1e308, 1e-308), 1000.)
        with self.assertRaises(ValueError):
            q.target_force(1e200, 1e200)

    def test_linear_stable_and_nondecaying_and_unstable(self):
        self.assertEqual(q.servo_probe(.5)['status'], 'SYNTHETIC_CONVERGED')
        self.assertEqual(q.servo_probe(2)['status'], 'NOT_CONVERGED')
        self.assertEqual(q.servo_probe(2.2)['status'], 'UNSTABLE')
        self.assertEqual(q.servo_probe(1.5, delay=1)['status'], 'UNSTABLE')

    def test_budget_saturation_and_sign_guards(self):
        self.assertEqual(q.servo_probe(.5, budget=2)['status'], 'NOT_CONVERGED')
        self.assertEqual(q.servo_probe(.5, saturation=.0001)['status'], 'NOT_CONVERGED')
        for bad in (0, -1, math.nan, True):
            with self.assertRaises(ValueError):
                q.servo_probe(bad)

    def test_static_two_windows(self):
        rows = [dict(step=i, force=750., ke=1e-9, residual=0., damping=0., inertia=0.,
                     escaped=0, inventory='same', contacts_complete=True) for i in range(1, 9)]
        rules = dict(samples_per_window=4, sample_stride=1, max_ke=1e-6,
                     max_drift_fraction=.001, expected_inventory='same')
        self.assertEqual(q.static_guard(rows, 750, rules)['status'], 'SYNTHETIC_STATIC')
        for key, val in [('damping', 1.), ('inertia', 1.), ('residual', 8.), ('force', 760.),
                         ('ke', 1.), ('escaped', 1), ('inventory', 'different'),
                         ('contacts_complete', False), ('step', 99)]:
            copy = [dict(r) for r in rows]
            copy[-1][key] = val
            self.assertNotEqual(q.static_guard(copy, 750, rules)['status'], 'SYNTHETIC_STATIC', key)
        self.assertEqual(q.static_guard(rows[:-1], 750, rules)['status'], 'INCOMPLETE')
        with self.assertRaises(ValueError):
            q.static_guard(rows, 750, {**rules, 'max_ke': None})


class Conservation(unittest.TestCase):
    def fixture(self):
        particles = [dict(id=1, type=1, radius=.1, mass=1., x=0., y=0., z=.5)]
        inventory = {1: dict(type=1, radius=.1, mass=1.)}
        return particles, inventory

    def test_full_identity_and_center_crossing(self):
        particles, expected = self.fixture()
        self.assertEqual(q.inventory_guard(particles, expected, 0., 1., .02)['status'], 'SYNTHETIC_CONSERVED')
        for key, value in [('id', 2), ('type', 2), ('radius', .11), ('mass', 2),
                           ('z', 1.01), ('x', math.nan), ('id', True)]:
            p = [{**particles[0], key: value}]
            self.assertEqual(q.inventory_guard(p, expected, 0., 1., .02)['status'], 'REJECTED', key)
        for p in ([], particles*2):
            self.assertEqual(q.inventory_guard(p, expected, 0., 1., .02)['status'], 'REJECTED')

    def test_surface_clip_distinct_from_center_crossing(self):
        particles, expected = self.fixture()
        particles[0]['z'] = .91
        r = q.inventory_guard(particles, expected, 0., 1., .02)
        self.assertEqual(r['status'], 'SYNTHETIC_CONSERVED')
        self.assertEqual(r['surface_cut_count'], 1)
        particles[0]['z'] = .95
        self.assertEqual(q.inventory_guard(particles, expected, 0., 1., .02)['status'], 'REJECTED')
        with self.assertRaises(ValueError):
            q.inventory_guard(particles, expected, 0., 1., None)


if __name__ == '__main__':
    unittest.main()
