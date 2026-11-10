"""Exact synthetic T11 plans and tiny existing-oracle probes.

All numbers/aliases are synthetic Q-T11 recommendation assumptions. No real
T0, bed, logs, binary, registration, host reader or operating permissions.
"""
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
for name in ('dem_gen2_qualification', 'dem_gen2_t0_contract', 'dem_gen2_t11_contract'):
    module = types.ModuleType(name)
    module.__file__ = str(source_dir / (name + '.py'))
    exec(compile(Path(module.__file__).read_bytes(), module.__file__, 'exec'), module.__dict__)
    sys.modules[name] = module
q = sys.modules['dem_gen2_qualification']
t0 = sys.modules['dem_gen2_t0_contract']
t11 = sys.modules['dem_gen2_t11_contract']
PIN = 'c5ebaa71298691020313e272b39c0a80b51cdc4d'
ASSUMPTIONS = ['Q-T11-01', 'Q-T11-02', 'Q-T11-03', 'Q-T11-04']


def independent_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(',', ':'), allow_nan=False).encode('ascii')).hexdigest()


def t0_fixture(sign=1):
    identity = dict(build_alias='synthetic_build', producer_pin='a'*40,
        qualification_pin='b'*40, deck_sha256='c'*64, fixture_sha256='d'*64,
        unit_mapping_id='GEN2_MPA_DECK_STRESS_0P001_V1', run_id='synthetic_run',
        attempt_id='synthetic_attempt', mesh_id='top_mesh', reaction_component='z')
    plan = dict(schema='DEM_GEN2_T0_SYNTHETIC_CONTRACT_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', identity=identity, fixture=dict(particle_count=20,
        compression_sign=sign, pressure_mpa=2., area_deck_m2=.001,
        declared_target_force_deck=2.), first_sample_id=11, sample_stride=2)
    controls = [dict(identity=copy.deepcopy(identity), kind=kind, sample_id=11+2*i,
        raw_reaction=sign*force, normalized_force=force)
        for i, (kind, force) in enumerate((('compression_positive', 3.),
        ('opposite_polarity_negative', -3.), ('zero_control', 0.)))]
    return plan, controls


def fixture(sign=1):
    base, controls = t0_fixture(sign)
    packet_sha = independent_hash(dict(synthetic_plan=base, synthetic_controls=controls))
    plan = dict(schema='DEM_GEN2_T11_SYNTHETIC_PLAN_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', plan_id='toy_t11_A1', revision=1, assumptions=list(ASSUMPTIONS),
        range_claim='EXPLICIT_CASE_LIST_ONLY', identity=dict(run_id='synthetic_run',
        bed_id='synthetic_bed', arm_id='synthetic_arm', attempt_id='synthetic_attempt',
        definition_id='synthetic_definition', unit_mapping_id='GEN2_MPA_DECK_STRESS_0P001_V1'),
        t0_binding=dict(contract_pin=PIN, packet_sha256=packet_sha, compression_sign=sign,
            reaction_component='z', compression_velocity_sign=-1),
        units=dict(force_id='GEN2_DECK_FORCE', length_id='GEN2_DECK_LENGTH',
            physical_time_id='s', deck_time_id='GEN2_DECK_TIME',
            physical_seconds_per_deck_time=[1, 1]),
        time=dict(dt_deck=[1, 8], dt_half_deck=[1, 16], control_period_seconds=[1, 1],
            window_seconds=[2, 1], budget_seconds=[8, 1]),
        cases=[dict(case_id='toy_stable', K_force_per_length=[1, 2], kp=[1, 1],
            vmax_length_per_second=[1, 1], target_force=[1, 1], u_limit=[1, 1],
            delay_seconds=[0, 1], oracle_tolerance=[1, 16], oracle_divergence=[10, 1])])
    context = dict(schema='DEM_GEN2_T11_FROZEN_SYNTHETIC_CONTEXT_V1',
        expected_plan_sha256=independent_hash(plan), expected_t0_packet_sha256=packet_sha,
        t0_contract_pin=PIN, t0_plan=base, t0_controls=controls, freeze_ordinal=10,
        first_observation_ordinal=11)
    return plan, context


def refreeze(plan, context):
    """Only fixture setup before its synthetic observations; no real sealing."""
    context['expected_plan_sha256'] = independent_hash(plan)


def bridge_fixture(plan, compiled):
    """Synthetic force rows chosen separately, never inferred from oracle error."""
    grid, case = compiled['coarse_grid'], compiled['cases'][0]
    contract = dict(schema='SYNTHETIC_OBSERVATION_BRIDGE_V1', purpose='SYNTHETIC_PREPARATION',
        run_id=plan['identity']['run_id'], bed_id=plan['identity']['bed_id'],
        arm_id=plan['identity']['arm_id'], attempt_id=plan['identity']['attempt_id'],
        definition_id=plan['identity']['definition_id'], unit_system_id='SYNTHETIC_TICKS_AND_SCALARS',
        source_stage='servo', requested_boundary='SERVO_TO_RELAXATION',
        first_step=grid['first_step'], first_sample_id=grid['first_sample_id'],
        first_tick=grid['first_control_tick'], tick_stride=grid['control_tick_stride'],
        planned_samples=grid['budget_ticks'], expected_end_step=grid['end_step'],
        expected_end_tick=grid['end_control_tick'], delay_samples=case['delay_ticks'])
    rules = dict(samples_per_window=grid['window_ticks'], sample_stride=grid['step_stride'],
        max_ke=.001, max_drift_fraction=.001, expected_inventory='synthetic_inventory',
        observation_contract=contract)
    rows = []
    for i in range(grid['budget_ticks']):
        row = dict(step=grid['first_step']+i*grid['step_stride'], force=100., ke=0.,
            residual=0., damping=0., inertia=0., escaped=0, inventory='synthetic_inventory',
            contacts_complete=True, stage='servo', boundary_id='SERVO_TO_RELAXATION',
            sample_id=1+i, time_tick=1+i, window_index=i//grid['window_ticks'])
        row.update({key: contract[key] for key in ('run_id', 'bed_id', 'arm_id',
                    'attempt_id', 'definition_id', 'unit_system_id')})
        rows.append(row)
    return rows, 100., rules


class T11Contract(unittest.TestCase):
    def authority_off(self, result):
        for key in ('registration_complete', 'physical_ready', 'execution_go',
                    'gate_write', 'operational_seal_modified'):
            self.assertIs(result[key], False)
        self.assertEqual(result['actual_T0'], 'NOT_RUN')
        self.assertIsNone(result['actual_compression_sign'])
        self.assertIsNone(result['actual_build_identity'])
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['whole_status'], 'HOLD')
        self.assertEqual(result['assumptions'], ASSUMPTIONS)

    def valid(self, plan, context):
        result = t11.validate_t11_plan(plan, context)
        self.assertEqual(result['status'], 'DRAFT_CONTRACT_VALID', result)
        self.authority_off(result)
        return result['compiled']

    def rejected(self, plan, context):
        result = t11.validate_t11_plan(plan, context)
        self.assertEqual(result['status'], 'REJECTED', result)
        self.authority_off(result)
        self.assertIsNone(result['compiled'])
        return result

    def test_01_exact_grid_and_dt_half_keep_physical_end_and_control_ticks(self):
        compiled = self.valid(*fixture())
        coarse, half = compiled['coarse_grid'], compiled['half_grid']
        self.assertEqual((coarse['control_steps'], coarse['window_ticks'], coarse['budget_ticks']), (8, 2, 8))
        self.assertEqual((coarse['first_step'], coarse['end_step']), (8, 64))
        self.assertEqual((half['control_steps'], half['first_step'], half['end_step']), (16, 16, 128))
        for grid in (coarse, half):
            self.assertEqual(grid['end_control_tick'], 8)
            self.assertEqual(Fraction(*grid['dt_seconds'])*grid['end_step'], Fraction(8))
            self.assertEqual(grid['physical_end_seconds'], [8, 1])
        self.assertEqual(compiled['model_results'], 'NOT_RUN')

    def test_02_physical_time_scale_is_not_deck_dt(self):
        plan, context = fixture()
        plan['units']['physical_seconds_per_deck_time'] = [2, 1]
        refreeze(plan, context)
        grid = self.valid(plan, context)['coarse_grid']
        self.assertEqual((grid['dt_seconds'], grid['control_steps'], grid['end_step']), ([1,4], 4, 32))

    def test_03_noninteger_control_grid_is_never_rounded(self):
        plan, context = fixture()
        plan['time'].update(dt_deck=[1,10], dt_half_deck=[1,20], control_period_seconds=[1,3])
        refreeze(plan, context)
        self.rejected(plan, context)

    def test_04_incomplete_or_short_windows_are_rejected(self):
        for key, value in (('window_seconds', [5,2]), ('budget_seconds', [5,1]),
                           ('budget_seconds', [2,1]), ('window_seconds', [1,1])):
            plan, context = fixture()
            plan['time'][key] = value
            refreeze(plan, context)
            with self.subTest(key=key, value=value): self.rejected(plan, context)

    def test_05_independently_integer_grid_is_not_a_dt_half_pair(self):
        plan, context = fixture()
        plan['time']['dt_half_deck'] = [1,32]
        refreeze(plan, context)
        self.rejected(plan, context)

    def test_06_delay_must_be_exact_ticks_inside_declared_budget(self):
        for value in ([1,2], [8,1], [9,1]):
            plan, context = fixture()
            plan['cases'][0]['delay_seconds'] = value
            refreeze(plan, context)
            with self.subTest(value=value): self.rejected(plan, context)

    def test_07_stable_toy_matches_independent_geometric_recurrence(self):
        case = self.valid(*fixture())['cases'][0]
        self.assertEqual(case['exact_a'], [1,2])
        self.assertEqual(case['exact_error_clip'], [1,1])
        result = q.servo_probe(**case['oracle_args'])
        self.assertEqual(result['errors'], [float(Fraction(1, 2**n)) for n in range(9)])
        self.assertEqual(result['first_window_hit'], 7)
        self.assertEqual(result['steps_observed'], 8)
        self.assertTrue(result['complete_budget'])
        self.assertEqual(result['status'], 'SYNTHETIC_CONVERGED')
        self.assertIs(result['physical_ready'], False)

    def test_08_nondamping_and_diverging_cases_are_valid_negative_plans(self):
        for stiffness, gain, budget, expected in (([2,1], [1,1], 8, 'NOT_CONVERGED'),
                ([176,5], [1,16], 16, 'UNSTABLE')):
            plan, context = fixture()
            plan['cases'][0].update(K_force_per_length=stiffness, kp=gain)
            plan['time']['budget_seconds'] = [budget,1]
            refreeze(plan, context)
            case = self.valid(plan, context)['cases'][0]
            result = q.servo_probe(**case['oracle_args'])
            with self.subTest(expected=expected):
                self.assertEqual(result['status'], expected)
                self.assertIs(result['physical_ready'], False)

    def test_09_actuator_saturation_maps_to_error_clip_not_same_a(self):
        plan, context = fixture()
        plan['cases'][0].update(K_force_per_length=[1,20000], kp=[10000,1])
        refreeze(plan, context)
        case = self.valid(plan, context)['cases'][0]
        self.assertEqual(case['exact_a'], [1,2])
        self.assertEqual(case['exact_error_clip'], [1,10000])
        result = q.servo_probe(**case['oracle_args'])
        self.assertEqual(result['status'], 'NOT_CONVERGED')
        self.assertGreater(result['errors'][-1], .99)

    def test_10_existing_delayed_counterexample_does_not_stop_at_first_hit(self):
        plan, context = fixture()
        plan['cases'][0].update(K_force_per_length=[5,8], kp=[1,10],
            delay_seconds=[32,1], oracle_tolerance=[1,8])
        plan['time']['budget_seconds'] = [1000,1]
        refreeze(plan, context)
        case = self.valid(plan, context)['cases'][0]
        self.assertEqual((case['exact_a'], case['exact_error_clip']), ([1,16], [10,1]))
        result = q.servo_probe(**case['oracle_args'])
        self.assertEqual(result['first_window_hit'], 17)
        self.assertEqual(result['steps_observed'], 402)
        self.assertEqual(result['status'], 'UNSTABLE')
        self.assertFalse(result['complete_budget'])

    def test_11_compiled_bridge_grid_preserves_pending_and_complete_budget_guard(self):
        plan, context = fixture()
        plan['time']['budget_seconds'] = [6,1]
        plan['cases'][0]['delay_seconds'] = [4,1]
        refreeze(plan, context)
        compiled = self.valid(plan, context)
        rows, target, rules = bridge_fixture(plan, compiled)
        self.assertEqual(q.observation_bridge(rows, target, rules)['status'], 'SYNTHETIC_STAGE_CANDIDATE')
        self.assertEqual(q.observation_bridge(rows[:-1], target, rules)['status'], 'INCOMPLETE')
        rows[1]['force'] = 120.
        result = q.observation_bridge(rows, target, rules)
        self.assertEqual(result['status'], 'NOT_CONVERGED')
        self.assertEqual(result['reason'], 'PENDING_SAMPLES_UNSTABLE')
        for key in ('physical_ready', 'execution_go', 'transition_authorized', 'gate_write'):
            self.assertIs(result[key], False)

    def test_12_t0_complete_packet_is_revalidated_not_its_status_string(self):
        plan, context = fixture()
        self.assertEqual(t0.validate_t0_contract(context['t0_plan'], context['t0_controls'])['status'],
                         'SYNTHETIC_T0_CONTRACT_CONSISTENT')
        context['t0_controls'][1]['normalized_force'] = 3.
        packet_sha = independent_hash(dict(synthetic_plan=context['t0_plan'], synthetic_controls=context['t0_controls']))
        context['expected_t0_packet_sha256'] = packet_sha
        plan['t0_binding']['packet_sha256'] = packet_sha
        refreeze(plan, context)
        self.assertEqual(self.rejected(plan, context)['reason'], 'T0_SYNTHETIC_PACKET_REJECTED')
        plan, context = fixture()
        context['t0_controls'] = {'status': 'SYNTHETIC_T0_CONTRACT_CONSISTENT'}
        self.rejected(plan, context)

    def test_13_changed_t0_bytes_cannot_reuse_old_packet_digest(self):
        plan, context = fixture()
        for row in context['t0_controls']:
            row['raw_reaction'] *= 2
            row['normalized_force'] *= 2
        self.assertEqual(self.rejected(plan, context)['reason'], 'T0_FROZEN_BYTES_MISMATCH')

    def test_14_t0_binding_pin_sign_axis_and_units_are_not_free_labels(self):
        for location, key, value in (('t0_binding', 'contract_pin', 'e'*40),
            ('t0_binding', 'compression_sign', -1), ('t0_binding', 'reaction_component', 'x'),
            ('t0_binding', 'compression_velocity_sign', 1), ('units', 'force_id', 'N'),
            ('units', 'length_id', 'm'), ('units', 'physical_time_id', 'ms'),
            ('identity', 'run_id', 'other_run'), ('identity', 'attempt_id', 'other_attempt'),
            ('identity', 'unit_mapping_id', 'another_mapping')):
            plan, context = fixture()
            plan[location][key] = value
            refreeze(plan, context)
            with self.subTest(location=location, key=key): self.rejected(plan, context)
        compiled = self.valid(*fixture(-1))
        self.assertEqual(compiled['t0_checked_controls'], 3)

    def test_15_post_freeze_changes_reject_even_individually_valid_plans(self):
        for kind in ('gain', 'time', 'identity', 'revision', 'extra_case'):
            plan, context = fixture()
            if kind == 'gain': plan['cases'][0]['kp'] = [2,1]
            elif kind == 'time': plan['time']['budget_seconds'] = [12,1]
            elif kind == 'identity': plan['identity']['bed_id'] = 'other_bed'
            elif kind == 'revision': plan['revision'] += 1
            else:
                plan['cases'].append(copy.deepcopy(plan['cases'][0]))
                plan['cases'][-1]['case_id'] = 'second_case'
            with self.subTest(kind=kind):
                self.assertEqual(self.rejected(plan, context)['reason'], 'PLAN_FROZEN_BYTES_MISMATCH')

    def test_16_declared_order_cannot_be_late_or_boolean(self):
        for freeze, observed in ((11,11), (12,11), (True,11), (10,False), (-1,11)):
            plan, context = fixture()
            context.update(freeze_ordinal=freeze, first_observation_ordinal=observed)
            with self.subTest(freeze=freeze, observed=observed): self.rejected(plan, context)

    def test_17_range_and_case_set_preserve_negative_cases(self):
        plan, context = fixture()
        plan['cases'].append(dict(plan['cases'][0], case_id='toy_negative', K_force_per_length=[2,1]))
        refreeze(plan, context)
        self.assertEqual(self.valid(plan, context)['checked_cases'], 2)
        for kind in ('empty', 'duplicate', 'continuous_claim'):
            bad, frozen = fixture()
            if kind == 'empty': bad['cases'] = []
            elif kind == 'duplicate': bad['cases'].append(copy.deepcopy(bad['cases'][0]))
            else: bad['range_claim'] = 'ALL_REAL_BEDS_STABLE'
            refreeze(bad, frozen)
            with self.subTest(kind=kind): self.rejected(bad, frozen)

    def test_18_exact_rationals_and_domain_are_narrow(self):
        for value in ([True,1], [1,False], [1,0], [1,-1], [0,1], [-1,1], 0.5, '1/2', [1], [1.,2]):
            plan, context = fixture()
            plan['cases'][0]['K_force_per_length'] = value
            refreeze(plan, context)
            with self.subTest(value=repr(value)): self.rejected(plan, context)
        for key, value in (('u_limit', [2,1]), ('oracle_tolerance', [1,1]), ('oracle_divergence', [1,1])):
            plan, context = fixture()
            plan['cases'][0][key] = value
            refreeze(plan, context)
            with self.subTest(key=key): self.rejected(plan, context)

    def test_19_rational_float_overflow_underflow_and_domain_collapse_reject(self):
        cases = (('K_force_per_length', [10**400,1]), ('K_force_per_length', [1,10**400]),
                 ('kp', [1,10**400]), ('oracle_tolerance', [1,10**400]),
                 ('oracle_tolerance', [10**30-1,10**30]), ('oracle_divergence', [10**30+1,10**30]))
        for key, value in cases:
            plan, context = fixture()
            plan['cases'][0][key] = value
            refreeze(plan, context)
            with self.subTest(key=key, numerator_digits=len(str(value[0]))): self.rejected(plan, context)

    def test_20_unknown_missing_and_actual_authority_fields_are_refused(self):
        for location in ('plan', 'identity', 't0_binding', 'units', 'time', 'case', 'context'):
            for change in ('missing', 'extra'):
                plan, context = fixture()
                obj = {'plan': plan, 'identity': plan['identity'], 't0_binding': plan['t0_binding'],
                       'units': plan['units'], 'time': plan['time'], 'case': plan['cases'][0], 'context': context}[location]
                if change == 'missing': del obj[next(iter(obj))]
                else: obj['execution_go'] = True
                refreeze(plan, context)
                with self.subTest(location=location, change=change): self.rejected(plan, context)
        plan, context = fixture()
        plan['purpose'] = 'ACTUAL_QUALIFICATION'
        refreeze(plan, context)
        self.rejected(plan, context)

    def test_21_subclasses_are_rejected_without_conversion_hooks(self):
        calls = []
        class TrapDict(dict):
            def __getitem__(self, key): calls.append('getitem'); raise AssertionError('hook')
            def items(self): calls.append('items'); raise AssertionError('hook')
        class TrapList(list):
            def __iter__(self): calls.append('iter'); raise AssertionError('hook')
        class TrapInt(int):
            def __int__(self): calls.append('int'); raise AssertionError('hook')
        class TrapString(str):
            def __str__(self): calls.append('str'); raise AssertionError('hook')
        for location in ('plan', 'context', 'case_list', 'rational', 'integer', 'string', 't0_plan'):
            plan, context = fixture()
            if location == 'plan': plan = TrapDict(plan)
            elif location == 'context': context = TrapDict(context)
            elif location == 'case_list': plan['cases'] = TrapList(plan['cases'])
            elif location == 'rational': plan['cases'][0]['kp'] = TrapList([1,1])
            elif location == 'integer': plan['cases'][0]['kp'] = [TrapInt(1),1]
            elif location == 'string': plan['plan_id'] = TrapString('toy_t11_A1')
            else: context['t0_plan'] = TrapDict(context['t0_plan'])
            with self.subTest(location=location): self.rejected(plan, context)
        self.assertEqual(calls, [])

    def test_22_inputs_unchanged_and_no_partial_compile_on_late_case_failure(self):
        for bad in (False, True):
            plan, context = fixture()
            if bad:
                plan['cases'].append(dict(plan['cases'][0], case_id='bad_later_case', delay_seconds=[8,1]))
                refreeze(plan, context)
            before = copy.deepcopy((plan, context))
            if bad: self.rejected(plan, context)
            else: self.valid(plan, context)
            self.assertEqual((plan, context), before)

    def test_23_hash_convention_matches_independent_bytes_not_equivalent_fractions(self):
        plan, context = fixture()
        self.assertEqual(t11.canonical_sha256(plan), independent_hash(plan))
        plan['cases'][0]['K_force_per_length'] = [2,4]
        self.assertEqual(self.rejected(plan, context)['reason'], 'PLAN_FROZEN_BYTES_MISMATCH')
        refreeze(plan, context)
        self.assertEqual(self.valid(plan, context)['cases'][0]['exact_a'], [1,2])

    def test_24_validator_does_not_execute_the_existing_oracle(self):
        original = q.servo_probe
        def forbidden(*args, **kwargs):
            raise AssertionError('validator executed a model')
        q.servo_probe = forbidden
        try:
            self.assertEqual(self.valid(*fixture())['cases'][0]['model_result'], 'NOT_RUN')
        finally:
            q.servo_probe = original


if __name__ == '__main__':
    unittest.main()
