"""Checks against observed copies and independently specified byte totals."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('copy_budget', Path(__file__).with_name('copy_budget.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class CopyBudgetTests(unittest.TestCase):
    def test_success_has_three_simultaneous_state_roots(self):
        r = m.observe_attempt()
        self.assertEqual(r['status'], 'COMPLETED_SYNTHETIC')
        self.assertEqual([x['live_state_roots'] for x in r['copy_events']], [2, 3])
        self.assertEqual([x['source_is_committed'] for x in r['copy_events']], [True, False])
        self.assertTrue(all(x['parent_still_current'] for x in r['copy_events']))
        self.assertTrue(r['committed_trial_and_detached_return'])

    def test_rod_success_uses_same_publication_boundary(self):
        r = m.observe_attempt(rods=True)
        self.assertEqual(len(r['copy_events']), 2)
        self.assertEqual(max(x['live_state_roots'] for x in r['copy_events']), 3)
        self.assertTrue(r['committed_trial_and_detached_return'])

    def test_all_registered_failures_never_make_return_copy(self):
        for site in m.MODEL.PLAIN_SITES + m.MODEL.ROD_SITES:
            with self.subTest(site=site):
                r = m.observe_attempt(rods=True, fail_at=site)
                self.assertEqual(r['status'], 'INJECTED_FAILURE')
                self.assertEqual(len(r['copy_events']), 1)
                self.assertEqual(r['copy_events'][0]['live_state_roots'], 2)
                self.assertTrue(r['parent_unchanged'])
                self.assertFalse(r['committed_trial_and_detached_return'])

    def test_instrumentation_is_restored(self):
        original = m.MODEL.deepcopy
        m.observe_attempt()
        self.assertIs(m.MODEL.deepcopy, original)
        m.observe_attempt(fail_at='p2g')
        self.assertIs(m.MODEL.deepcopy, original)
        with self.assertRaises(ValueError):
            m.observe_attempt(fail_at='unknown')
        self.assertIs(m.MODEL.deepcopy, original)

    def test_report_excludes_object_addresses_and_memory_claims(self):
        r = m.observe_attempt()
        self.assertFalse(r['actual_memory_measured'])
        self.assertFalse(r['physical_solver_imported'])
        self.assertFalse(r['execution_go'])
        text = json.dumps(r)
        self.assertNotIn('object_id', text)
        self.assertNotIn('0x', text)

    def test_three_reservations_exceed_seventeen_bytes(self):
        r = m.MEMORY.account(m.declared_plan(6, 17))['pools']['planned_arrays']
        self.assertEqual(r['peak_bytes'], 18)
        self.assertEqual(r['headroom_bytes'], -1)
        self.assertTrue(r['over_budget'])

    def test_retained_snapshot_is_a_fourth_reservation(self):
        r = m.MEMORY.account(m.declared_plan(6, 23, retained_copies=1))['pools']['planned_arrays']
        self.assertEqual(r['peak_bytes'], 24)
        self.assertTrue(r['over_budget'])

    def test_missing_return_copy_changes_budget_conclusion(self):
        complete = m.declared_plan(6, 17)
        incomplete = deepcopy(complete)
        incomplete['allocations'] = [a for a in incomplete['allocations'] if a['id'] != 'returned']
        full = m.MEMORY.account(complete)['pools']['planned_arrays']
        partial = m.MEMORY.account(incomplete)['pools']['planned_arrays']
        self.assertEqual((full['peak_bytes'], partial['peak_bytes']), (18, 12))
        self.assertTrue(full['over_budget'])
        self.assertFalse(partial['over_budget'])

    def test_exact_large_reservation(self):
        size = 2**53 + 1
        r = m.MEMORY.account(m.declared_plan(size, 3 * size - 1))['pools']['planned_arrays']
        self.assertEqual(r['peak_bytes'], 3 * size)
        self.assertEqual(r['headroom_bytes'], -1)

    def test_plan_types_rejected(self):
        for bad in (True, 1.0, '1', None, -1):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                m.declared_plan(bad, 100)
            with self.subTest(budget=bad), self.assertRaises(ValueError):
                m.declared_plan(6, bad)
            with self.subTest(copies=bad), self.assertRaises(ValueError):
                m.declared_plan(6, 100, retained_copies=bad)
        with self.assertRaises(ValueError):
            m.declared_plan(0, 100)

    def test_dependency_identity_checked_before_loading(self):
        path = m.HERE.parent / 'dem_trial_isolation_20261114/trial_model.py'
        with self.assertRaisesRegex(ValueError, 'identity'):
            m.checked_module(path, '0' * 64, 'must_not_load')


if __name__ == '__main__':
    unittest.main(verbosity=2)
