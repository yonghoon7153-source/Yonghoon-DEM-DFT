"""Expected-correct tests for a synthetic planning calculator, not DEM runs."""
import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('memory_plan', Path(__file__).with_name('memory_liveness.py'))
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def allocation(name, size, start=0, end=4, pool='host', used=1):
    return dict(id=name, pool=pool, reserved_bytes=size, used_bytes=used, start=start, end=end)


def plan(*allocations):
    return dict(schema='synthetic_memory_liveness/1', units='B',
                pools={'host': {'budget_bytes': 20}}, allocations=list(allocations), views=[])


class MemoryLivenessTests(unittest.TestCase):
    def test_overlap_old_new_rollback(self):
        p = plan(allocation('old', 3, 0, 4), allocation('new', 4, 2, 6), allocation('rollback', 2, 0, 6))
        out = model.account(p)['pools']['host']
        self.assertEqual(out['peak_bytes'], 9)
        self.assertEqual(out['timeline'], [[0, 5], [2, 9], [4, 6], [6, 0]])

    def test_half_open_boundary(self):
        out = model.account(plan(allocation('a', 3, 0, 2), allocation('b', 5, 2, 4)))
        self.assertEqual(out['pools']['host']['peak_bytes'], 5)
        self.assertEqual(out['pools']['host']['timeline'], [[0, 3], [2, 5], [4, 0]])

    def test_aliases_do_not_allocate(self):
        p = plan(allocation('owner', 8))
        p['views'] = [dict(id='left', owner='owner', start=1, end=3, offset_bytes=0, nbytes=4),
                      dict(id='right', owner='owner', start=1, end=3, offset_bytes=4, nbytes=4)]
        self.assertEqual(model.account(p)['pools']['host']['peak_bytes'], 8)

    def test_int_above_float_precision(self):
        p = plan(allocation('big', 2**53), allocation('one', 1))
        p['pools']['host']['budget_bytes'] = 2**53
        out = model.account(p)['pools']['host']
        self.assertEqual(out['peak_bytes'], 2**53 + 1)
        self.assertEqual(out['headroom_bytes'], -1)
        self.assertTrue(out['over_budget'])

    def test_distinct_pools(self):
        p = plan(allocation('h', 8), allocation('d', 9, pool='device'))
        p['pools']['device'] = {'budget_bytes': 8}
        out = model.account(p)
        self.assertEqual(out['pools']['host']['peak_bytes'], 8)
        self.assertEqual(out['pools']['device']['peak_bytes'], 9)
        self.assertFalse(out['pools']['host']['over_budget'])
        self.assertTrue(out['pools']['device']['over_budget'])
        self.assertNotIn('combined_peak_bytes', out)

    def test_reserved_not_used(self):
        out = model.account(plan(allocation('a', 16, used=2)))
        self.assertEqual(out['pools']['host']['peak_bytes'], 16)

    def test_budget_equality_then_one_byte_less(self):
        p = plan(allocation('a', 8));p['pools']['host']['budget_bytes'] = 8
        self.assertFalse(model.account(p)['pools']['host']['over_budget'])
        p['pools']['host']['budget_bytes'] = 7
        self.assertTrue(model.account(p)['pools']['host']['over_budget'])

    def test_input_permutation(self):
        p = plan(allocation('a', 3, 0, 2), allocation('b', 5, 1, 3), allocation('c', 2, 2, 4))
        expected = model.account(p);p['allocations'].reverse()
        self.assertEqual(model.account(p), expected)

    def test_input_not_modified(self):
        p = plan(allocation('a', 3));before = copy.deepcopy(p)
        model.account(p);self.assertEqual(p, before)
        p['allocations'][0]['reserved_bytes'] = None;before = copy.deepcopy(p)
        with self.assertRaises(ValueError):model.account(p)
        self.assertEqual(p, before)

    def test_numeric_types_before_conversion(self):
        for value in [True, 1.0, float('nan'), float('inf'), '1', '\uff11', None, -1]:
            with self.subTest(value=repr(value)):
                p = plan(allocation('a', 3));p['allocations'][0]['reserved_bytes'] = value
                with self.assertRaises(ValueError):model.account(p)

    def test_duplicate_allocation_id(self):
        with self.assertRaises(ValueError):model.account(plan(allocation('a', 3), allocation('a', 4)))

    def test_view_needs_known_owner(self):
        p = plan(allocation('a', 3));p['views'] = [dict(id='v', owner='absent', start=0, end=1, offset_bytes=0, nbytes=1)]
        with self.assertRaises(ValueError):model.account(p)

    def test_view_cannot_outlive_owner(self):
        for start,end in [(0,3),(2,5)]:
            with self.subTest(start=start,end=end):
                p = plan(allocation('a', 3, 1, 4));p['views'] = [dict(id='v', owner='a', start=start, end=end, offset_bytes=0, nbytes=1)]
                with self.assertRaises(ValueError):model.account(p)

    def test_view_bounds_and_duplicate_ids(self):
        p = plan(allocation('a', 3));v = dict(id='v', owner='a', start=0, end=1, offset_bytes=2, nbytes=2)
        p['views'] = [v]
        with self.assertRaises(ValueError):model.account(p)
        v['offset_bytes'] = 0;p['views'] = [v, copy.deepcopy(v)]
        with self.assertRaises(ValueError):model.account(p)
        p['views'] = [dict(v,id='a')]
        with self.assertRaises(ValueError):model.account(p)

    def test_view_may_not_override_pool(self):
        p = plan(allocation('a', 3));p['views'] = [dict(id='v', owner='a', pool='device', start=0, end=1, offset_bytes=0, nbytes=1)]
        with self.assertRaises(ValueError):model.account(p)

    def test_interval_and_reservation_bounds(self):
        for changes in [dict(start=2,end=2),dict(start=3,end=2),dict(start=-1),
                        dict(reserved_bytes=0),dict(used_bytes=4)]:
            with self.subTest(changes=changes):
                p = plan(allocation('a', 3));p['allocations'][0].update(changes)
                with self.assertRaises(ValueError):model.account(p)

    def test_unknown_or_missing_field(self):
        p = plan(allocation('a', 3));p['extra'] = 0
        with self.assertRaises(ValueError):model.account(p)
        del p['extra'];del p['allocations'][0]['used_bytes']
        with self.assertRaises(ValueError):model.account(p)

    def test_empty_plan_and_unresolved_budget(self):
        with self.assertRaises(ValueError):model.account(plan())
        p = plan(allocation('a', 3));p['pools']['host']['budget_bytes'] = None
        with self.assertRaises(ValueError):model.account(p)

    def test_units_and_unknown_pool(self):
        p = plan(allocation('a', 3));p['units'] = 'GiB'
        with self.assertRaises(ValueError):model.account(p)
        p['units'] = 'B';p['allocations'][0]['pool'] = 'device'
        with self.assertRaises(ValueError):model.account(p)

    def test_no_go_or_resource_adoption(self):
        out = model.account(plan(allocation('a', 3)))
        self.assertEqual(out['status'], 'SYNTHETIC_ARITHMETIC_ONLY')
        self.assertFalse(out['actual_resource_qualification'])
        self.assertFalse(out['execution_go'])


if __name__ == '__main__':
    unittest.main()
