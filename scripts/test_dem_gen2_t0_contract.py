"""Synthetic packet tests only; no binary, actual T0 receipt or host reader."""
import copy
import math
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
q = types.ModuleType('dem_gen2_qualification')
q.__file__ = str(source_dir / 'dem_gen2_qualification.py')
exec(compile(Path(q.__file__).read_bytes(), q.__file__, 'exec'), q.__dict__)
sys.modules['dem_gen2_qualification'] = q
t0 = types.ModuleType('dem_gen2_t0_contract')
t0.__file__ = str(source_dir / 'dem_gen2_t0_contract.py')
exec(compile(Path(t0.__file__).read_bytes(), t0.__file__, 'exec'), t0.__dict__)


def fixture(sign=1):
    """Q-T0-1/2 recommendation assumptions; all labels and values are synthetic."""
    identity = dict(build_alias='synthetic_build', producer_pin='a'*40,
                    qualification_pin='b'*40, deck_sha256='c'*64,
                    fixture_sha256='d'*64, unit_mapping_id='GEN2_MPA_DECK_STRESS_0P001_V1',
                    run_id='synthetic_run', attempt_id='synthetic_attempt',
                    mesh_id='top_mesh', reaction_component='z')
    plan = dict(schema='DEM_GEN2_T0_SYNTHETIC_CONTRACT_V1', purpose='SYNTHETIC_PREPARATION',
                protocol='P2', identity=identity,
                fixture=dict(particle_count=20, compression_sign=sign, pressure_mpa=2.,
                             area_deck_m2=.001, declared_target_force_deck=2.),
                first_sample_id=11, sample_stride=2)
    cases = [dict(identity=copy.deepcopy(identity), kind=kind, sample_id=11+2*i,
                  raw_reaction=sign*force, normalized_force=force)
             for i, (kind, force) in enumerate((('compression_positive', 3.),
                 ('opposite_polarity_negative', -3.), ('zero_control', 0.)))]
    return plan, cases


class T0Contract(unittest.TestCase):
    def assert_blocked(self, plan, cases):
        result = t0.validate_t0_contract(plan, cases)
        self.assertEqual(result['status'], 'REJECTED')
        self.assert_authority_off(result)
        return result

    def assert_authority_off(self, result):
        self.assertEqual(result['actual_T0'], 'NOT_RUN')
        self.assertIsNone(result['actual_build_identity'])
        self.assertIsNone(result['actual_compression_sign'])
        self.assertEqual(result['binary_syntax'], 'NOT_RUN')
        for key in ('physical_ready', 'execution_go', 'gate_write', 'operational_seal_modified'):
            self.assertIs(result[key], False)
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['evidence_kind'], 'SYNTHETIC_ONLY')
        self.assertEqual(result['assumptions'], ['Q-T0-1', 'Q-T0-2'])

    def test_01_complete_packet_is_only_synthetic_consistency(self):
        result = t0.validate_t0_contract(*fixture())
        self.assertEqual(result['status'], 'SYNTHETIC_T0_CONTRACT_CONSISTENT')
        self.assertEqual(result['checked_cases'], 3)
        self.assertEqual(result['target_force_deck'], 2.)
        self.assertEqual([x['classification'] for x in result['observations']],
                         ['COMPRESSION_POSITIVE', 'OPPOSITE_SIGN_DETECTED', 'ZERO_NONDETERMINING'])
        self.assert_authority_off(result)

    def test_02_both_declared_signs_preserve_raw_same_sample(self):
        for sign in (-1, 1):
            plan, cases = fixture(sign)
            result = t0.validate_t0_contract(plan, cases)
            with self.subTest(sign=sign):
                self.assertEqual(result['status'], 'SYNTHETIC_T0_CONTRACT_CONSISTENT')
                self.assertEqual([x['raw_reaction'] for x in result['observations']],
                                 [x['raw_reaction'] for x in cases])
                self.assertEqual([x['normalized_force'] for x in result['observations']], [3., -3., 0.])

    def test_03_identity_switch_with_unchanged_numbers_is_rejected(self):
        replacements = dict(build_alias='another_build', producer_pin='e'*40,
            qualification_pin='f'*40, deck_sha256='a'*64, fixture_sha256='b'*64,
            unit_mapping_id='another_units', run_id='another_run', attempt_id='another_attempt',
            mesh_id='another_mesh', reaction_component='x')
        for key, value in replacements.items():
            plan, cases = fixture()
            cases[1]['identity'][key] = value
            with self.subTest(key=key): self.assert_blocked(plan, cases)

    def test_04_unknown_unit_mapping_is_not_self_certifying(self):
        plan, cases = fixture()
        plan['identity']['unit_mapping_id'] = 'UNREGISTERED_UNIT_MAPPING'
        for row in cases: row['identity']['unit_mapping_id'] = 'UNREGISTERED_UNIT_MAPPING'
        self.assert_blocked(plan, cases)

    def test_05_target_arithmetic_is_bound_to_declared_mapping(self):
        for field, value in (('declared_target_force_deck', 2000.), ('pressure_mpa', 2000.), ('area_deck_m2', 1.)):
            plan, cases = fixture()
            plan['fixture'][field] = value
            with self.subTest(field=field): self.assert_blocked(plan, cases)

    def test_06_changed_synthetic_target_can_be_consistent_without_real_qualification(self):
        plan, cases = fixture()
        plan['fixture'].update(pressure_mpa=4., area_deck_m2=.002, declared_target_force_deck=8.)
        result = t0.validate_t0_contract(plan, cases)
        self.assertEqual(result['status'], 'SYNTHETIC_T0_CONTRACT_CONSISTENT')
        self.assertEqual(result['target_force_deck'], 8.)
        self.assert_authority_off(result)

    def test_07_missing_duplicate_gap_and_reordered_samples(self):
        for mutation in ('missing', 'extra', 'duplicate', 'gap', 'reorder'):
            plan, cases = fixture()
            if mutation == 'missing': cases.pop()
            elif mutation == 'extra': cases.append(copy.deepcopy(cases[-1]))
            elif mutation == 'duplicate': cases[1]['sample_id'] = cases[0]['sample_id']
            elif mutation == 'gap': cases[1]['sample_id'] += 1
            else: cases[0], cases[1] = cases[1], cases[0]
            with self.subTest(mutation=mutation): self.assert_blocked(plan, cases)

    def test_08_sample_anchors_require_exact_integers(self):
        for where, key in (('plan', 'first_sample_id'), ('plan', 'sample_stride'), ('row', 'sample_id')):
            for value in (True, 1., '1', 0, -1):
                plan, cases = fixture()
                (plan if where == 'plan' else cases[0])[key] = value
                with self.subTest(where=where, key=key, value=repr(value)): self.assert_blocked(plan, cases)

    def test_09_role_contract_cannot_be_relabeled_or_self_reported(self):
        for mutation in ('wrong_role', 'duplicate_role', 'expected_accept', 'all_zero'):
            plan, cases = fixture()
            if mutation == 'wrong_role': cases[0]['kind'] = 'zero_control'
            elif mutation == 'duplicate_role': cases[1]['kind'] = cases[0]['kind']
            elif mutation == 'expected_accept': cases[1]['expected_accept'] = True
            else:
                for row in cases: row.update(raw_reaction=0., normalized_force=0.)
            with self.subTest(mutation=mutation): self.assert_blocked(plan, cases)

    def test_10_same_sample_signed_normalization_not_absolute_value(self):
        for index, value in ((0, -3.), (1, 3.), (2, 1.)):
            plan, cases = fixture()
            cases[index]['normalized_force'] = value
            with self.subTest(index=index): self.assert_blocked(plan, cases)

    def test_11_raw_scalar_nonfinite_or_nonbuiltin_values_are_rejected(self):
        for key in ('raw_reaction', 'normalized_force'):
            for value in (float('nan'), float('inf'), -float('inf'), True, '3', 10**1000):
                plan, cases = fixture()
                cases[0][key] = value
                with self.subTest(key=key, kind=type(value).__name__): self.assert_blocked(plan, cases)

    def test_12_fixture_numeric_contract_rejects_invalid_and_overflow(self):
        for key in ('pressure_mpa', 'area_deck_m2', 'declared_target_force_deck'):
            for value in (0., -1., float('nan'), float('inf'), True, '2', 10**1000):
                plan, cases = fixture()
                plan['fixture'][key] = value
                with self.subTest(key=key, kind=type(value).__name__): self.assert_blocked(plan, cases)
        plan, cases = fixture()
        plan['fixture'].update(pressure_mpa=1e308, area_deck_m2=1e308)
        self.assert_blocked(plan, cases)

    def test_13_declared_sign_and_fixture_size_are_explicit(self):
        for key, values in (('compression_sign', (None, True, 0, 1., '1', 2)),
                            ('particle_count', (None, True, 20., '20', 1, 21))):
            for value in values:
                plan, cases = fixture()
                plan['fixture'][key] = value
                with self.subTest(key=key, value=repr(value)): self.assert_blocked(plan, cases)

    def test_14_identity_format_rejects_empty_paths_and_wrong_digest_shape(self):
        for key, values in (('build_alias', ('', 'has space', '../path', 'x'*129)),
                            ('producer_pin', ('abc', 'g'*40, 'A'*40)),
                            ('fixture_sha256', ('f'*40, 'g'*64, 'F'*64))):
            for value in values:
                plan, cases = fixture()
                plan['identity'][key] = value
                with self.subTest(key=key, value=value): self.assert_blocked(plan, cases)

    def test_15_mesh_axis_contract_is_fixed_not_renamed(self):
        for key, value in (('mesh_id', 'other_mesh'), ('reaction_component', 'x')):
            plan, cases = fixture()
            plan['identity'][key] = value
            for row in cases: row['identity'][key] = value
            with self.subTest(key=key): self.assert_blocked(plan, cases)

    def test_16_missing_unknown_fields_and_actual_receipts_are_rejected(self):
        for location in ('plan', 'identity', 'fixture', 'case', 'case_identity'):
            for mutation in ('missing', 'extra'):
                plan, cases = fixture()
                obj = {'plan': plan, 'identity': plan['identity'], 'fixture': plan['fixture'],
                       'case': cases[0], 'case_identity': cases[0]['identity']}[location]
                if mutation == 'missing': del obj[next(iter(obj))]
                else: obj['actual_receipt'] = 'NOT_ALLOWED'
                with self.subTest(location=location, mutation=mutation): self.assert_blocked(plan, cases)
        for key, value in (('purpose', 'PRODUCTION'), ('protocol', 'P1'), ('schema', 'UNKNOWN')):
            plan, cases = fixture()
            plan[key] = value
            with self.subTest(key=key): self.assert_blocked(plan, cases)

    def test_17_nonbuiltin_containers_and_scalar_subclasses_do_not_call_hooks(self):
        calls = []
        class TrapDict(dict):
            def __getitem__(self, key): calls.append('getitem'); raise AssertionError('hook called')
            def __contains__(self, key): calls.append('contains'); raise AssertionError('hook called')
        class TrapList(list):
            def __iter__(self): calls.append('iter'); raise AssertionError('hook called')
        class TrapFloat(float):
            def __float__(self): calls.append('float'); raise AssertionError('hook called')
        class TrapString(str):
            def __str__(self): calls.append('str'); raise AssertionError('hook called')
        class TrapInt(int):
            def __int__(self): calls.append('int'); raise AssertionError('hook called')
        for location in ('plan', 'identity', 'fixture', 'cases', 'case', 'case_identity', 'number', 'string', 'integer'):
            plan, cases = fixture()
            if location == 'plan': plan = TrapDict(plan)
            elif location == 'identity': plan['identity'] = TrapDict(plan['identity'])
            elif location == 'fixture': plan['fixture'] = TrapDict(plan['fixture'])
            elif location == 'cases': cases = TrapList(cases)
            elif location == 'case': cases[0] = TrapDict(cases[0])
            elif location == 'case_identity': cases[0]['identity'] = TrapDict(cases[0]['identity'])
            elif location == 'number': cases[0]['raw_reaction'] = TrapFloat(3.)
            elif location == 'string': plan['identity']['build_alias'] = TrapString('synthetic_build')
            else: plan['first_sample_id'] = TrapInt(11)
            with self.subTest(location=location): self.assert_blocked(plan, cases)
        self.assertEqual(calls, [])

    def test_18_inputs_are_unchanged_on_consistent_and_rejected_packets(self):
        for bad in (False, True):
            plan, cases = fixture()
            if bad: cases[-1]['identity']['attempt_id'] = 'wrong_attempt'
            before = copy.deepcopy((plan, cases))
            t0.validate_t0_contract(plan, cases)
            with self.subTest(bad=bad): self.assertEqual((plan, cases), before)

    def test_19_exact_shifted_sample_plan_is_supported(self):
        plan, cases = fixture()
        plan.update(first_sample_id=101, sample_stride=4)
        for index, row in enumerate(cases): row['sample_id'] = 101+4*index
        result = t0.validate_t0_contract(plan, cases)
        self.assertEqual(result['status'], 'SYNTHETIC_T0_CONTRACT_CONSISTENT')
        self.assertEqual([x['sample_id'] for x in result['observations']], [101,105,109])

    def test_20_invalid_packets_return_no_partial_consistency(self):
        plan, cases = fixture()
        cases[-1]['identity']['run_id'] = 'other_run'
        result = self.assert_blocked(plan, cases)
        self.assertEqual(result['observations'], [])
        self.assertEqual(result['checked_cases'], 0)
        self.assertIsNone(result['target_force_deck'])


if __name__ == '__main__':
    unittest.main()
