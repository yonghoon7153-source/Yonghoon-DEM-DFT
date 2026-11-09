"""Small synthetic checks only; not registered T5/T11 or research results."""
import math
from decimal import Decimal, localcontext
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

    def test_contact_area_exchange_at_extreme_radius_ratio(self):
        # The small sphere is centered on the large sphere's surface. Its
        # circle area differs from pi below one binary64 ULP in these cases.
        for large in (1e8, 1e308):
            for r, s in ((large, 1.), (1., large)):
                with self.subTest(r=r, s=s):
                    self.assertAlmostEqual(q.contact_area(r, s, large), math.pi,
                                           delta=4 * math.ulp(math.pi))
        self.assertEqual(q.contact_area(1e8, 1, 1e8), q.contact_area(1, 1e8, 1e8))

    def test_contact_area_scale_tangent_and_representability(self):
        for scale in (1e-100, 1., 1e100):
            with self.subTest(scale=scale):
                self.assertAlmostEqual(q.contact_area(2*scale, scale, 2*scale)/(scale*scale),
                                       15 * math.pi / 16, places=14)
        for distance in (math.nextafter(1., math.inf), math.nextafter(3., 0.)):
            # Independent high-precision small-sphere plane construction.
            with localcontext() as context:
                context.prec = 100
                d = Decimal.from_float(distance)
                x = (d*d + 1 - 4)/(2*d)
                expected = float(Decimal.from_float(math.pi) * (1-x*x))
            for r, s in ((2., 1.), (1., 2.)):
                with self.subTest(distance=distance, r=r):
                    self.assertAlmostEqual(q.contact_area(r, s, distance), expected,
                                           delta=8 * math.ulp(expected))
        self.assertEqual(q.contact_area(2, 1, 3), 0)
        self.assertEqual(q.contact_area(2, 1, math.nextafter(3., math.inf)), 0)
        with self.assertRaises(ValueError):
            q.contact_area(2, 1, 1)
        for scale in (1e-200, 1e200):
            with self.subTest(unrepresentable_scale=scale), self.assertRaises(ValueError):
                q.contact_area(scale, scale, scale)


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

    def test_delayed_transient_hit_does_not_end_observation(self):
        for a, delay, tolerance, budget, first_hit, divergence_step in (
                (1/256, 512, 1/128, 10000, 257, 6440),
                (1/16, 32, 1/8, 1000, 17, 402)):
            with self.subTest(delay=delay):
                result = q.servo_probe(a, delay=delay, tolerance=tolerance, budget=budget)
                self.assertEqual(result['status'], 'UNSTABLE')
                self.assertEqual(len(result['errors']) - 1, divergence_step)
                self.assertEqual(result['first_window_hit'], first_hit)
                self.assertFalse(result['complete_budget'])
                self.assertFalse(result['physical_ready'])

    def test_stable_probe_observes_the_full_declared_budget(self):
        result = q.servo_probe(.5, budget=100)
        self.assertEqual(result['status'], 'SYNTHETIC_CONVERGED')
        self.assertEqual(len(result['errors']), 101)
        self.assertEqual(result['first_window_hit'], 23)
        self.assertTrue(result['complete_budget'])
        self.assertTrue(result['delay_queue_within_tolerance'])
        self.assertTrue(result['tail_within_tolerance'])
        self.assertEqual(result['stability_scope'], 'DECLARED_SYNTHETIC_BUDGET_ONLY')

    def test_pending_delay_queue_prevents_budget_end_convergence(self):
        result = q.servo_probe(1/256, delay=512, tolerance=1/128, budget=257)
        self.assertEqual(result['status'], 'NOT_CONVERGED')
        self.assertEqual(len(result['errors']), 258)
        self.assertEqual(result['first_window_hit'], 257)
        self.assertTrue(result['complete_budget'])
        self.assertTrue(result['tail_within_tolerance'])
        self.assertFalse(result['delay_queue_within_tolerance'])

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

    def test_plane_penetration_is_invariant_under_large_translation(self):
        expected = {1: dict(type=1, radius=1., mass=1.)}
        for origin in (0., 1e16, -1e16):
            for offset in (0., -10.):
                particle = dict(id=1, type=1, radius=1., mass=1., x=0., y=0., z=origin+offset)
                for limit in (0., .5, 1.):
                    with self.subTest(origin=origin, offset=offset, limit=limit):
                        result = q.inventory_guard([particle], expected, origin-10., origin, limit)
                        self.assertEqual(result['status'], 'SYNTHETIC_CONSERVED' if limit == 1 else 'REJECTED')
                        if limit == 1:
                            self.assertEqual(result['surface_cut_count'], 1)
                particle['z'] = origin - 4.
                result = q.inventory_guard([particle], expected, origin-10., origin, 0.)
                self.assertEqual(result['status'], 'SYNTHETIC_CONSERVED')
                self.assertEqual(result['surface_cut_count'], 0)

    def test_surface_penetration_smaller_than_coordinate_addition_ulp(self):
        radius = math.nextafter(1., math.inf)
        particle = dict(id=1, type=1, radius=radius, mass=1., x=0., y=0., z=1.)
        expected = {1: dict(type=1, radius=radius, mass=1.)}
        self.assertEqual(q.inventory_guard([particle], expected, -10., 2., 0.)['status'], 'REJECTED')
        result = q.inventory_guard([particle], expected, -10., 2., math.ulp(1.))
        self.assertEqual(result['status'], 'SYNTHETIC_CONSERVED')
        self.assertEqual(result['surface_cut_count'], 1)


if __name__ == '__main__':
    unittest.main()
