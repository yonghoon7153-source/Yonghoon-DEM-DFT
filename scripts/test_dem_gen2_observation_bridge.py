"""Synthetic observation identity/diagnostic bridge; no physical qualification."""
import copy
from collections import UserDict
import math
from pathlib import Path
import types
import unittest

source = Path(__file__).with_name('dem_gen2_qualification.py')
q = types.ModuleType('g2_observation_source')
q.__file__ = str(source)
exec(compile(source.read_bytes(), str(source), 'exec'), q.__dict__)

ACCEPTED = {'SYNTHETIC_STATIC', 'SYNTHETIC_STAGE_CANDIDATE'}


def fixture(planned=4, delay=1):
    """All constants are arbitrary synthetic inputs, NOT selected Q2 values."""
    contract = dict(schema='SYNTHETIC_OBSERVATION_BRIDGE_V1',
        purpose='SYNTHETIC_PREPARATION', run_id='fixture-run', bed_id='fixture-bed',
        arm_id='fixture-arm', attempt_id='fixture-attempt', definition_id='fixture-definition',
        unit_system_id='SYNTHETIC_TICKS_AND_SCALARS', source_stage='servo',
        requested_boundary='SERVO_TO_RELAXATION', first_step=10, first_sample_id=100,
        first_tick=200, tick_stride=3, planned_samples=planned,
        expected_end_step=10+(planned-1)*2, expected_end_tick=200+(planned-1)*3,
        delay_samples=delay)
    rules = dict(samples_per_window=2, sample_stride=2, max_ke=.001,
        max_drift_fraction=.001, expected_inventory='synthetic-inventory',
        observation_contract=contract)
    rows = []
    for i in range(planned):
        row = dict(step=10+i*2, force=100., ke=0., residual=0., damping=0., inertia=0.,
                   escaped=0, inventory='synthetic-inventory', contacts_complete=True,
                   stage='servo', boundary_id='SERVO_TO_RELAXATION',
                   sample_id=100+i, time_tick=200+i*3, window_index=i//2)
        row.update({key: contract[key] for key in
                    ('run_id', 'bed_id', 'arm_id', 'attempt_id', 'definition_id', 'unit_system_id')})
        rows.append(row)
    return rows, 100., rules


class ObservationBridge(unittest.TestCase):
    def rejected(self, rows, target, rules):
        result = q.static_guard(rows, target, rules)
        self.assertNotIn(result['status'], ACCEPTED, result)
        return result

    def test_01_complete_trace_is_only_a_diagnostic_candidate(self):
        result = q.static_guard(*fixture())
        self.assertEqual(result['status'], 'SYNTHETIC_STAGE_CANDIDATE')
        self.assertEqual(result.get('candidate_stage'), 'relaxation')
        self.assertEqual(result.get('first_window_hit_sample'), 103)

    def test_02_existing_scalar_only_contract_is_preserved(self):
        rows, target, rules = fixture()
        del rules['observation_contract']
        self.assertEqual(q.static_guard(rows, target, rules),
                         dict(status='SYNTHETIC_STATIC', physical_ready=False))

    def test_03_wrong_run_bed_arm_attempt_definition_or_units(self):
        for key in ('run_id', 'bed_id', 'arm_id', 'attempt_id', 'definition_id', 'unit_system_id'):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                rows[-1][key] = 'other-fixture'
                self.rejected(rows, target, rules)

    def test_04_missing_observation_metadata(self):
        for key in ('run_id', 'stage', 'sample_id', 'time_tick', 'window_index', 'boundary_id'):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                del rows[-1][key]
                self.rejected(rows, target, rules)

    def test_05_metadata_requires_exact_builtin_types(self):
        class Token(str):
            pass
        for key, value in (('run_id', Token('fixture-run')), ('sample_id', True),
                           ('time_tick', 209.), ('window_index', True)):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                rows[-1][key] = value
                self.rejected(rows, target, rules)

    def test_06_stage_substitution(self):
        rows, target, rules = fixture()
        rows[-1]['stage'] = 'relaxation'
        self.rejected(rows, target, rules)

    def test_07_boundary_substitution(self):
        rows, target, rules = fixture()
        rows[-1]['boundary_id'] = 'RELAXATION_TO_S0'
        self.rejected(rows, target, rules)

    def test_08_duplicate_sample(self):
        rows, target, rules = fixture()
        rows[-1]['sample_id'] = rows[-2]['sample_id']
        self.rejected(rows, target, rules)

    def test_09_sample_gap(self):
        rows, target, rules = fixture()
        rows[-1]['sample_id'] += 1
        self.rejected(rows, target, rules)

    def test_10_stale_tick(self):
        rows, target, rules = fixture()
        rows[-1]['time_tick'] = rows[-2]['time_tick']
        self.rejected(rows, target, rules)

    def test_11_tick_gap(self):
        rows, target, rules = fixture()
        rows[-1]['time_tick'] += 1
        self.rejected(rows, target, rules)

    def test_12_window_membership_is_bound_to_samples(self):
        rows, target, rules = fixture()
        rows[-1]['window_index'] = 0
        self.rejected(rows, target, rules)

    def test_13_step_gap_still_refused(self):
        rows, target, rules = fixture()
        rows[-1]['step'] += 1
        self.rejected(rows, target, rules)

    def test_14_contiguous_but_wrong_expected_boundary_time(self):
        for key in ('step', 'sample_id', 'time_tick'):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                for row in rows:
                    row[key] += 20
                self.rejected(rows, target, rules)

    def test_15_missing_window_is_incomplete(self):
        rows, target, rules = fixture()
        result = self.rejected(rows[:-1], target, rules)
        self.assertEqual(result['status'], 'INCOMPLETE')

    def test_16_extra_budget_rows_are_not_silently_truncated(self):
        rows, target, rules = fixture()
        result = self.rejected(rows+[dict(rows[-1])], target, rules)
        self.assertEqual(result['status'], 'REJECTED')

    def test_17_first_window_hit_before_budget_is_not_completion(self):
        rows, target, rules = fixture(8)
        result = self.rejected(rows[:4], target, rules)
        self.assertEqual(result['status'], 'INCOMPLETE')
        self.assertEqual(result.get('first_window_hit_sample'), 103)

    def test_18_first_hit_then_late_instability(self):
        rows, target, rules = fixture(8)
        rows[-1]['force'] = 120.
        result = self.rejected(rows, target, rules)
        self.assertEqual(result['status'], 'NOT_CONVERGED')
        self.assertEqual(result.get('first_window_hit_sample'), 103)

    def test_19_pending_queue_values_cannot_be_hidden_by_stable_tail(self):
        rows, target, rules = fixture(8, delay=6)
        rows[1]['force'] = 120.
        result = self.rejected(rows, target, rules)
        self.assertEqual(result['status'], 'NOT_CONVERGED')
        self.assertEqual(result.get('reason'), 'PENDING_SAMPLES_UNSTABLE')

    def test_20_delay_needing_unprovided_history_is_refused(self):
        rows, target, rules = fixture()
        rules['observation_contract']['delay_samples'] = 4
        self.rejected(rows, target, rules)

    def test_21_transient_then_complete_stable_budget(self):
        rows, target, rules = fixture(8, delay=1)
        rows[0]['force'] = 120.
        result = q.static_guard(rows, target, rules)
        self.assertEqual(result['status'], 'SYNTHETIC_STAGE_CANDIDATE')
        self.assertEqual(result.get('first_window_hit_sample'), 104)

    def test_22_incomplete_or_lost_inventory_anywhere_in_trace(self):
        for key, value in (('contacts_complete', False), ('escaped', 1),
                           ('inventory', 'changed')):
            with self.subTest(key=key):
                rows, target, rules = fixture(8)
                rows[0][key] = value
                result = self.rejected(rows, target, rules)
                self.assertEqual(result['status'], 'REJECTED')

    def test_23_nonfinite_scalars_are_not_dropped(self):
        for key in ('force', 'ke', 'residual', 'damping', 'inertia'):
            with self.subTest(key=key):
                rows, target, rules = fixture(8)
                rows[0][key] = math.nan
                result = self.rejected(rows, target, rules)
                self.assertEqual(result['status'], 'REJECTED')

    def test_24_context_missing_unknown_or_wrong_schema(self):
        for change in ('missing', 'extra', 'schema', 'purpose', 'stage', 'boundary', 'not_mapping'):
            with self.subTest(change=change):
                rows, target, rules = fixture()
                c = rules['observation_contract']
                if change == 'missing':
                    del c['run_id']
                elif change == 'extra':
                    c['pending_queue_ok'] = True
                elif change == 'not_mapping':
                    rules['observation_contract'] = None
                else:
                    key = dict(schema='schema', purpose='purpose', stage='source_stage',
                               boundary='requested_boundary')[change]
                    c[key] = 'OTHER'
                self.rejected(rows, target, rules)

    def test_25_public_bridge_never_falls_back_when_context_is_missing(self):
        rows, target, rules = fixture()
        del rules['observation_contract']
        # The explicitly reported baseline is the old scalar guard. Its actual
        # acceptance, not a missing-module exception, exposes the new scope gap.
        entry = getattr(q, 'observation_bridge', q.static_guard)
        self.assertNotIn(entry(rows, target, rules)['status'], ACCEPTED)

    def test_26_extra_observation_fields_are_not_self_certification(self):
        rows, target, rules = fixture()
        rows[-1]['pending_queue_ok'] = True
        self.rejected(rows, target, rules)

    def test_27_inputs_are_never_mutated(self):
        for good in (True, False):
            args = fixture()
            if not good:
                args[0][-1]['run_id'] = 'wrong'
            before = copy.deepcopy(args)
            q.static_guard(*args)
            self.assertEqual(args, before)

    def test_28_plan_integer_and_end_anchor_contract(self):
        for key, value in (('first_step', True), ('tick_stride', 0), ('delay_samples', -1),
                           ('planned_samples', 4.), ('expected_end_step', 17),
                           ('expected_end_tick', 210), ('first_sample_id', 0)):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                rules['observation_contract'][key] = value
                self.rejected(rows, target, rules)

    def test_29_existing_scalar_negatives_remain_refused(self):
        for key, value in (('force', 102.), ('ke', 1.), ('residual', 2.),
                           ('damping', 1.), ('inertia', 1.)):
            with self.subTest(key=key):
                rows, target, rules = fixture()
                rows[-1][key] = value
                self.rejected(rows, target, rules)

    def test_30_no_result_grants_any_operational_authority(self):
        rows, target, rules = fixture()
        for supplied in (rows, rows[:-1], [{**r, 'run_id': 'wrong'} for r in rows]):
            result = q.static_guard(supplied, target, rules)
            for key in ('physical_ready', 'execution_go', 'transition_authorized', 'gate_write'):
                self.assertIs(result.get(key), False, key)
            self.assertEqual(result.get('research_results'), 0)
            self.assertEqual(result.get('scope'), 'SYNTHETIC_SERVO_TO_RELAXATION_ONLY')

    def test_31_explicit_context_cannot_fall_back_through_dict_subclass(self):
        class Rules(dict):
            pass
        class HiddenMembership(dict):
            def __contains__(self, key):
                return False
        for kind in (Rules, HiddenMembership, UserDict):
            with self.subTest(kind=kind.__name__):
                rows, target, rules = fixture()
                rows[-1]['run_id'] = 'wrong-run'
                self.rejected(rows, target, kind(rules))

    def test_32_rules_support_is_explicitly_exact_dict_even_without_context(self):
        class Rules(dict):
            pass
        for kind in (Rules, UserDict):
            with self.subTest(kind=kind.__name__):
                rows, target, rules = fixture()
                del rules['observation_contract']
                self.rejected(rows, target, kind(rules))


if __name__ == '__main__':
    unittest.main()
