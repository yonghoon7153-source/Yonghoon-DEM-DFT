"""Expected-correct checks for a synthetic state-transition model, not MPM."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('trial_model', Path(__file__).with_name('trial_model.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def seed():
    return {
        'step': 7, 'time_ticks': 70, 'wall_z': 41, 'wall_vel': -2,
        'points': [
            dict(point_id=7, particle_id=2, x=11, v=13, C=17, F=19, dg_acc=23, eps_acc=29),
            dict(point_id=8, particle_id=2, x=31, v=37, C=41, F=43, dg_acc=47, eps_acc=53),
            dict(point_id=9, particle_id=3, x=11, v=59, C=61, F=67, dg_acc=71, eps_acc=73),
        ],
        'profiles': [100, 200, 300, 400], 'host': [500, 600, 700, 800],
    }


def expected(state, rods=False):
    """Hand-specified arithmetic oracle; does not call the model's stages."""
    out = deepcopy(state)
    for p in out['points']:
        p['x'] += 8 if rods else 1
        p['v'] += 13 if rods else 2
        p['C'] += 3
        p['F'] += 4
        p['dg_acc'] += 5
        p['eps_acc'] += 6
    out['profiles'] = [state['profiles'][0] + 3, state['profiles'][1] + 5,
                       state['profiles'][2] + 7, state['profiles'][3] + 11]
    out['host'] = [state['host'][0] + 13, state['host'][1] + 17,
                   state['host'][2] + 19, state['host'][3] + 23]
    out['step'] += 1
    out['time_ticks'] += 10
    return out


PLAIN = ('trial_created', 'p2g', 'g2p_first', 'g2p_done', 'host_first', 'host_done', 'before_commit')
ROD = PLAIN + ('rod_first', 'rod_positions', 'rod_velocity_first', 'rod_done')


class IsolationTests(unittest.TestCase):
    def test_success_without_rods(self):
        original = seed()
        store = m.TrialModel(original)
        self.assertEqual(store.attempt(), expected(original))
        self.assertEqual(store.snapshot(), expected(original))

    def test_success_with_rods(self):
        original = seed()
        self.assertEqual(m.TrialModel(original).attempt(rods=True), expected(original, True))

    def test_all_plain_failure_sites_and_explicit_retry(self):
        for site in PLAIN:
            with self.subTest(site=site):
                original = seed()
                store = m.TrialModel(original)
                with self.assertRaisesRegex(m.InjectedFailure, '^' + site + '$'):
                    store.attempt(fail_at=site)
                self.assertEqual(store.snapshot(), original)
                self.assertEqual(store.attempt(), expected(original))

    def test_all_rod_failure_sites_and_explicit_retry(self):
        for site in ROD:
            with self.subTest(site=site):
                original = seed()
                store = m.TrialModel(original)
                with self.assertRaises(m.InjectedFailure):
                    store.attempt(rods=True, fail_at=site)
                self.assertEqual(store.snapshot(), original)
                self.assertEqual(store.attempt(rods=True), expected(original, True))

    def test_previous_success_is_not_erased_on_later_failure(self):
        for site in ROD:
            with self.subTest(site=site):
                store = m.TrialModel(seed())
                store.attempt(rods=True)
                prefix = expected(seed(), True)
                with self.assertRaises(m.InjectedFailure):
                    store.attempt(rods=True, fail_at=site)
                self.assertEqual(store.snapshot(), prefix)
                self.assertEqual(store.attempt(rods=True), expected(prefix, True))

    def test_partial_point_update_keeps_all_six_fields(self):
        original = seed()
        store = m.TrialModel(original)
        with self.assertRaises(m.InjectedFailure):
            store.attempt(fail_at='g2p_first')
        for before, after in zip(original['points'], store.snapshot()['points']):
            for field in ('x', 'v', 'C', 'F', 'dg_acc', 'eps_acc'):
                self.assertEqual(after[field], before[field], field)

    def test_partial_host_update_is_not_published(self):
        store = m.TrialModel(seed())
        with self.assertRaises(m.InjectedFailure):
            store.attempt(fail_at='host_first')
        self.assertEqual(store.snapshot()['host'], [500, 600, 700, 800])
        self.assertEqual(store.snapshot()['step'], 7)
        self.assertEqual(store.snapshot()['time_ticks'], 70)

    def test_profile_prefix_known_answer(self):
        original = seed()
        original['profiles'] = [2, 2, 2, 2]
        store = m.TrialModel(original)
        with self.assertRaises(m.InjectedFailure):
            store.attempt(fail_at='p2g')
        self.assertEqual(store.snapshot()['profiles'], [2, 2, 2, 2])
        self.assertEqual(store.attempt()['profiles'], [5, 7, 9, 13])

    def test_returned_snapshots_are_detached(self):
        store = m.TrialModel(seed())
        snap = store.snapshot()
        snap['points'][0]['x'] = -99
        snap['profiles'][0] = -99
        self.assertEqual(store.snapshot(), seed())
        result = store.attempt()
        result['points'][0]['F'] = -99
        result['host'][0] = -99
        self.assertEqual(store.snapshot(), expected(seed()))

    def test_constructor_detaches_caller(self):
        original = seed()
        store = m.TrialModel(original)
        original['points'][0]['C'] = -99
        original['profiles'][0] = -99
        self.assertEqual(store.snapshot(), seed())

    def test_motion_and_wall_do_not_restart_on_failure(self):
        original = seed()
        store = m.TrialModel(original)
        with self.assertRaises(m.InjectedFailure):
            store.attempt(rods=True, fail_at='rod_positions')
        self.assertEqual(store.snapshot(), original)
        result = store.attempt(rods=True)
        self.assertEqual((result['wall_z'], result['wall_vel']), (41, -2))
        self.assertEqual(result['points'][0]['v'], 26)
        self.assertEqual(result['points'][0]['C'], 20)

    def test_point_and_particle_identity_preserved(self):
        result = m.TrialModel(seed()).attempt(rods=True)
        self.assertEqual([(p['point_id'], p['particle_id']) for p in result['points']],
                         [(7, 2), (8, 2), (9, 3)])
        self.assertEqual(len(result['points']), 3)

    def test_unknown_and_disabled_injection_rejected(self):
        for site in ('unknown', 'rod_done', ''):
            with self.subTest(site=site):
                store = m.TrialModel(seed())
                with self.assertRaises(ValueError):
                    store.attempt(fail_at=site)
                self.assertEqual(store.snapshot(), seed())

    def test_control_types_rejected_before_change(self):
        for kwargs in ({'rods': 1}, {'rods': 'yes'}, {'fail_at': 1}, {'fail_at': True}):
            with self.subTest(kwargs=kwargs):
                store = m.TrialModel(seed())
                with self.assertRaises(ValueError):
                    store.attempt(**kwargs)
                self.assertEqual(store.snapshot(), seed())

    def test_empty_and_malformed_state_rejected(self):
        bads = [{}, seed(), seed(), seed(), seed(), seed()]
        bads[1]['points'] = []
        bads[2]['points'][1]['point_id'] = 7
        bads[3]['profiles'] = [0]
        del bads[4]['points'][0]['F']
        bads[5]['step'] = -1
        for bad in bads:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    m.TrialModel(bad)

    def test_exact_integer_sentinels_and_bool_rejection(self):
        original = seed()
        original['profiles'][0] = 2**53 + 1
        self.assertEqual(m.TrialModel(original).attempt()['profiles'][0], 2**53 + 4)
        for bad in (True, 1.0, '1', None):
            original['points'][0]['F'] = bad
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                m.TrialModel(original)


if __name__ == '__main__':
    unittest.main(verbosity=2)
