"""Unexecuted staging suite. Every value and identity is an invented fixture.

권고안 전제(Q-LIVE-1/2). Copy exact dependency sources into an isolated test
directory and install the agreed process/network audit guard before executing.
No test here reads research data, invokes a DEM engine or creates operating GO.
"""
import copy
import hashlib
import json
from pathlib import Path
import sys
import types
import unittest

source_dir = Path(__file__).parent
for name in ('dem_gen2_qualification', 'dem_gen2_t0_contract',
             'dem_gen2_t11_contract', 'dem_gen2_live_contract'):
    module = types.ModuleType(name)
    module.__file__ = str(source_dir / (name + '.py'))
    exec(compile(Path(module.__file__).read_bytes(), module.__file__, 'exec'), module.__dict__)
    sys.modules[name] = module
live = sys.modules['dem_gen2_live_contract']


def independent_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=True,
        separators=(',', ':'), allow_nan=False).encode('ascii')).hexdigest()


def fixture(sign=1, grid_choice='coarse', delay=0):
    """Hand-built complete two-particle toy trace, not T0's 20-particle claim.

The T0 controls and T11 grid are declared independently. No model output is
converted into force, torque or energy. The trace has eight servo samples and
four independent R-a samples; all are literal synthetic measurements.
"""
    t0_identity = dict(build_alias='synthetic_build', producer_pin='a'*40,
        qualification_pin='b'*40, deck_sha256='c'*64, fixture_sha256='d'*64,
        unit_mapping_id='GEN2_MPA_DECK_STRESS_0P001_V1', run_id='synthetic_run',
        attempt_id='synthetic_attempt', mesh_id='top_mesh', reaction_component='z')
    t0_plan = dict(schema='DEM_GEN2_T0_SYNTHETIC_CONTRACT_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', identity=t0_identity, fixture=dict(particle_count=20,
            compression_sign=sign, pressure_mpa=2., area_deck_m2=.001,
            declared_target_force_deck=2.), first_sample_id=11, sample_stride=2)
    controls = [dict(identity=copy.deepcopy(t0_identity), kind=kind, sample_id=11+2*i,
        raw_reaction=sign*force, normalized_force=force)
        for i, (kind, force) in enumerate((('compression_positive', 3.),
        ('opposite_polarity_negative', -3.), ('zero_control', 0.)))]
    packet_hash = independent_hash(dict(synthetic_plan=t0_plan, synthetic_controls=controls))
    identity = dict(run_id='synthetic_run', bed_id='synthetic_bed', arm_id='synthetic_arm',
        attempt_id='synthetic_attempt', definition_id='synthetic_definition',
        unit_mapping_id='GEN2_MPA_DECK_STRESS_0P001_V1')
    t11 = dict(schema='DEM_GEN2_T11_SYNTHETIC_PLAN_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', plan_id='toy_live_grid', revision=1,
        assumptions=['Q-T11-01', 'Q-T11-02', 'Q-T11-03', 'Q-T11-04'],
        range_claim='EXPLICIT_CASE_LIST_ONLY', identity=identity,
        t0_binding=dict(contract_pin='c5ebaa71298691020313e272b39c0a80b51cdc4d',
            packet_sha256=packet_hash, compression_sign=sign, reaction_component='z',
            compression_velocity_sign=-1),
        units=dict(force_id='GEN2_DECK_FORCE', length_id='GEN2_DECK_LENGTH',
            physical_time_id='s', deck_time_id='GEN2_DECK_TIME',
            physical_seconds_per_deck_time=[1, 1]),
        time=dict(dt_deck=[1, 8], dt_half_deck=[1, 16], control_period_seconds=[1, 1],
            window_seconds=[2, 1], budget_seconds=[8, 1]),
        cases=[dict(case_id='toy_live_case', K_force_per_length=[1, 1], kp=[1, 1],
            vmax_length_per_second=[1, 1], target_force=[2, 1], u_limit=[1, 1],
            delay_seconds=[delay, 1], oracle_tolerance=[1, 16], oracle_divergence=[10, 1])])
    context = dict(schema='DEM_GEN2_T11_FROZEN_SYNTHETIC_CONTEXT_V1',
        expected_plan_sha256=independent_hash(t11), expected_t0_packet_sha256=packet_hash,
        t0_contract_pin='c5ebaa71298691020313e272b39c0a80b51cdc4d',
        t0_plan=t0_plan, t0_controls=controls, freeze_ordinal=10, first_observation_ordinal=11)
    particles = [dict(id=1, type=1, radius=.5, mass=1.), dict(id=2, type=2, radius=.25, mass=2.)]
    plate = dict(position=[0., 0., 10.], velocity=[0., 0., 0.],
        mesh_id='top_mesh', wall_id='synthetic_wall', history_id='synthetic_history')
    plan = dict(schema='DEM_GEN2_LIVE_RA_SYNTHETIC_PLAN_V1', purpose='SYNTHETIC_PREPARATION',
        protocol='P2', assumptions=['Q-LIVE-1', 'Q-LIVE-2'], t11_plan=t11,
        t11_context=context, case_id='toy_live_case', grid_choice=grid_choice,
        scalar_profile='EXISTING_SYNTHETIC_STATIC_GUARD_V1',
        scalar_limits=dict(max_translational_ke=.001, max_drift_fraction=.001),
        extra_limits=dict(max_rotational_ke=.001, max_torque_residual=.01,
            max_torque_damping=.001, max_torque_inertia=.001),
        inventory_id='synthetic_inventory', reference_inventory=particles,
        plate_reference=plate, ra_window_count=2)
    source = copy.deepcopy(t0_identity)
    source.update(t0_packet_sha256=packet_hash, t11_plan_sha256=independent_hash(t11),
        case_id='toy_live_case', grid_choice=grid_choice)
    stamp_identity = {key: identity[key] for key in ('run_id', 'bed_id', 'arm_id', 'attempt_id', 'definition_id')}
    stamp_identity['unit_system_id'] = identity['unit_mapping_id']
    unit_ids = dict(reaction='TOY_DECK_REACTION_AREA_PRESSURE_V1',
        energy='TOY_DECK_TRANSLATIONAL_ROTATIONAL_ENERGY_V1',
        force_balance='TOY_DECK_FORCE_VECTOR_V1', torque_balance='TOY_DECK_TORQUE_VECTOR_V1',
        plate='TOY_DECK_POSITION_VELOCITY_V1', contacts='EXACT_CONTACT_COUNT_V1',
        inventory='TOY_ID_TYPE_RADIUS_MASS_V1')
    traces = []
    stride = 8 if grid_choice == 'coarse' else 16
    for stage, offset, count in (('servo', 0, 8), ('relaxation', 8, 4)):
        frames = []
        for i in range(count):
            stamp = dict(stamp_identity, stage=stage, step=(offset+i+1)*stride,
                sample_id=offset+i+1, time_tick=offset+i+1, window_index=i//2)
            balance = dict(residual=[0., 0., 0.], gravity=[0., 0., -1.],
                           damping=[0., 0., 0.], inertia=[0., 0., 0.])
            values = dict(reaction=dict(raw_reaction=sign*2., compression_sign=sign,
                normalized_force=2., area_deck_m2=.001, pressure_deck=2000.),
                energy=dict(translational_ke=0., rotational_ke=0.),
                force_balance=copy.deepcopy(balance), torque_balance=copy.deepcopy(balance),
                plate=copy.deepcopy(plate), contacts=dict(count=2),
                inventory=dict(particles=copy.deepcopy(particles), escaped=0))
            channels = {name: dict(stamp=copy.deepcopy(stamp), unit_id=unit_ids[name],
                complete=True, values=value) for name, value in values.items()}
            frames.append(dict(source_identity=copy.deepcopy(source), stamp=stamp, channels=channels))
        traces.append(frames)
    return plan, traces[0], traces[1]


def set_force(frame, value):
    reaction = frame['channels']['reaction']['values']
    reaction.update(raw_reaction=reaction['compression_sign']*value,
        normalized_force=value, pressure_deck=value/reaction['area_deck_m2'])


class LiveContract(unittest.TestCase):
    def authority_off(self, result):
        for key in ('physical_ready', 'execution_go', 'transition_authorized', 'gate_write',
                    'operational_seal_modified', 'registration_complete', 'source_authenticated'):
            self.assertIs(result[key], False)
        for key in ('actual_T0', 'actual_T11', 'actual_T12'):
            self.assertEqual(result[key], 'NOT_RUN')
        self.assertIsNone(result['actual_build_identity'])
        self.assertIsNone(result['actual_compression_sign'])
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['whole_status'], 'HOLD')
        self.assertEqual(result['assumptions'], ['Q-LIVE-1', 'Q-LIVE-2'])

    def check(self, args, status, reason=None):
        result = live.diagnose_live_ra(*args)
        self.assertEqual(result['status'], status, result)
        self.authority_off(result)
        if reason is not None: self.assertEqual(result['reason'], reason, result)
        if status != 'SYNTHETIC_RA_END_CANDIDATE': self.assertIsNone(result['boundary_candidate'])
        return result

    def test_01_complete_two_stages_yield_only_bound_diagnostic(self):
        args = fixture()
        result = self.check(args, 'SYNTHETIC_RA_END_CANDIDATE')
        boundary = result['boundary_candidate']
        self.assertEqual((boundary['end_step'], boundary['end_sample_id'], boundary['end_tick'],
            boundary['end_window_index']), (96, 12, 12, 1))
        self.assertEqual(boundary['stage'], 'relaxation')
        self.assertEqual(boundary['boundary_id'], 'RA_END')
        self.assertEqual(boundary['plan_sha256'], independent_hash(args[0]))
        self.assertEqual(boundary['servo_trace_sha256'], independent_hash(args[1]))
        self.assertEqual(boundary['ra_trace_sha256'], independent_hash(args[2]))
        self.assertEqual(boundary['end_frame_sha256'], independent_hash(args[2][-1]))
        self.assertEqual(boundary['reference_inventory'], args[0]['reference_inventory'])
        self.assertEqual(result['servo_diagnostic']['first_window_hit_sample'], 4)

    def test_02_declared_signs_and_exact_dt_half_grid(self):
        for sign in (-1, 1):
            for grid in ('coarse', 'half'):
                with self.subTest(sign=sign, grid=grid):
                    result = self.check(fixture(sign, grid), 'SYNTHETIC_RA_END_CANDIDATE')
                    expected = 96 if grid == 'coarse' else 192
                    self.assertEqual(result['boundary_candidate']['end_step'], expected)
                    self.assertEqual(result['boundary_candidate']['end_tick'], 12)

    def test_03_input_is_unchanged_and_returned_candidate_detached(self):
        args = fixture()
        before = copy.deepcopy(args)
        result = self.check(args, 'SYNTHETIC_RA_END_CANDIDATE')
        result['boundary_candidate']['plate']['position'][2] = -5
        result['boundary_candidate']['reference_inventory'][0]['mass'] = -5
        self.assertEqual(args, before)

    def test_04_missing_channels_cannot_be_filled_by_scalar_success(self):
        for name in ('torque_balance', 'force_balance', 'energy', 'contacts', 'inventory'):
            args = fixture()
            del args[1][1]['channels'][name]
            with self.subTest(channel=name):
                self.check(args, 'NOT_COMPUTED', 'REQUIRED_CHANNEL_NOT_COMPUTED')

    def test_05_missing_rotational_energy_and_incomplete_contacts(self):
        args = fixture()
        del args[1][1]['channels']['energy']['values']['rotational_ke']
        self.check(args, 'NOT_COMPUTED', 'ROTATIONAL_KE_NOT_COMPUTED')
        for value in (False, None):
            args = fixture()
            args[2][0]['channels']['contacts']['complete'] = value
            with self.subTest(marker=value): self.check(args, 'NOT_COMPUTED', 'CHANNEL_INCOMPLETE')
        args = fixture()
        args[2][0]['channels']['contacts']['values']['count'] = None
        self.check(args, 'NOT_COMPUTED', 'CONTACT_COUNT_NOT_COMPUTED')

    def test_06_every_channel_requires_the_same_frame_identity(self):
        changes = dict(step=99, sample_id=99, time_tick=99, window_index=99,
            stage='relaxation', run_id='other_run', attempt_id='other_attempt')
        for key, value in changes.items():
            args = fixture()
            args[1][0]['channels']['torque_balance']['stamp'][key] = value
            with self.subTest(key=key): self.check(args, 'REJECTED', 'MIXED_CHANNEL_FRAME')

    def test_07_integer_stamps_cannot_use_bool_or_float_equality(self):
        for value in (True, 1.):
            args = fixture()
            args[1][0]['channels']['energy']['stamp']['sample_id'] = value
            with self.subTest(value=value): self.check(args, 'REJECTED')
        args = fixture()
        args[1][0]['channels']['energy']['complete'] = 1
        self.check(args, 'REJECTED', 'EXACT_COMPLETENESS_FLAG_REQUIRED')

    def test_08_source_and_units_are_bound_on_every_frame(self):
        args = fixture()
        args[1][1]['source_identity']['deck_sha256'] = 'e'*64
        self.check(args, 'REJECTED', 'SOURCE_DECLARATION_MISMATCH')
        args = fixture()
        args[2][1]['channels']['torque_balance']['unit_id'] = 'UNREGISTERED_TORQUE'
        self.check(args, 'REJECTED', 'UNSUPPORTED_DECLARATION')

    def test_09_full_inventory_cannot_be_replaced_by_count(self):
        for key, value in (('id', 3), ('type', 3), ('mass', 9.), ('radius', .125)):
            args = fixture()
            args[2][1]['channels']['inventory']['values']['particles'][0][key] = value
            with self.subTest(key=key): self.check(args, 'REJECTED', 'FULL_REFERENCE_INVENTORY_MISMATCH')
        for mutation in ('missing', 'duplicate', 'escaped'):
            args = fixture()
            value = args[1][0]['channels']['inventory']['values']
            if mutation == 'missing': value['particles'].pop()
            elif mutation == 'duplicate': value['particles'][1] = copy.deepcopy(value['particles'][0])
            else: value['escaped'] = 1
            with self.subTest(mutation=mutation): self.check(args, 'REJECTED')

    def test_10_force_and_torque_channels_are_separate_and_complete(self):
        args = fixture()
        del args[1][0]['channels']['force_balance']['values']['gravity']
        self.check(args, 'NOT_COMPUTED', 'BALANCE_COMPONENT_NOT_COMPUTED')
        args = fixture()
        args[2][-1]['channels']['force_balance']['values']['damping'] = [.1, 0., 0.]
        self.check(args, 'NOT_CONVERGED', 'RA_TERMINAL_SCALAR_WINDOWS_UNSTABLE')

    def test_11_additional_channels_are_independently_bounded(self):
        for stage in (1, 2):
            for name, key, value in (('energy', 'rotational_ke', .1),
                    ('torque_balance', 'residual', [.1, 0., 0.]),
                    ('torque_balance', 'damping', [.1, 0., 0.]),
                    ('torque_balance', 'inertia', [.1, 0., 0.])):
                args = fixture()
                args[stage][-1]['channels'][name]['values'][key] = value
                with self.subTest(stage=stage, key=key): self.check(args, 'NOT_CONVERGED')

    def test_12_first_hit_does_not_complete_declared_servo_budget(self):
        plan, servo, unused = fixture()
        result = self.check((plan, servo[:4], []), 'INCOMPLETE', 'SERVO_DECLARED_BUDGET_NOT_OBSERVED')
        self.assertEqual(result['servo_diagnostic']['first_window_hit_sample'], 4)

    def test_13_late_scalar_failure_preserves_first_hit_without_candidate(self):
        args = fixture()
        set_force(args[1][-1], 2.1)
        result = self.check(args, 'NOT_CONVERGED', 'SERVO_TERMINAL_WINDOWS_UNSTABLE')
        self.assertEqual(result['servo_diagnostic']['first_window_hit_sample'], 4)

    def test_14_pending_scalar_and_extra_channels_are_not_discarded(self):
        args = fixture(delay=6)
        set_force(args[1][1], 2.1)
        self.check(args, 'NOT_CONVERGED', 'SERVO_PENDING_SAMPLES_UNSTABLE')
        args = fixture(delay=6)
        args[1][1]['channels']['energy']['values']['rotational_ke'] = .1
        self.check(args, 'NOT_CONVERGED', 'SERVO_EXTRA_CHANNEL_TAIL_UNSTABLE')

    def test_15_servo_success_cannot_substitute_for_independent_ra_budget(self):
        for count in (0, 1, 3):
            plan, servo, ra = fixture()
            with self.subTest(count=count):
                self.check((plan, servo, ra[:count]), 'INCOMPLETE', 'RA_DECLARED_BUDGET_NOT_OBSERVED')
        args = fixture()
        args[0]['ra_window_count'] = 3
        self.check(args, 'INCOMPLETE', 'RA_DECLARED_BUDGET_NOT_OBSERVED')

    def test_16_ra_plate_must_be_fixed_through_every_observation(self):
        for key, value in (('position', [0., 0., 10.1]), ('velocity', [0., 0., .1])):
            args = fixture()
            args[2][0]['channels']['plate']['values'][key] = value
            with self.subTest(key=key): self.check(args, 'REJECTED', 'RA_PLATE_NOT_FIXED')
        args = fixture()
        args[1][-1]['channels']['plate']['values']['position'][2] = 10.1
        self.check(args, 'REJECTED', 'SERVO_TO_RA_PLATE_POSITION_MISMATCH')

    def test_17_same_mesh_wall_history_declarations_are_required(self):
        for key in ('mesh_id', 'wall_id', 'history_id'):
            args = fixture()
            args[2][0]['channels']['plate']['values'][key] = 'other_history'
            with self.subTest(key=key): self.check(args, 'REJECTED', 'PLATE_OR_HISTORY_DECLARATION_CHANGED')

    def test_18_ra_time_stage_and_window_cannot_be_relabelled(self):
        for key, value in (('step', 64), ('stage', 'servo'), ('window_index', 4)):
            args = fixture()
            args[2][0]['stamp'][key] = value
            for channel in args[2][0]['channels'].values(): channel['stamp'][key] = value
            with self.subTest(key=key): self.check(args, 'REJECTED', 'FRAME_IDENTITY_OR_GRID_MISMATCH')

    def test_19_full_t11_input_is_revalidated_not_a_status_receipt(self):
        args = fixture()
        args[0]['t11_context']['expected_plan_sha256'] = 'e'*64
        self.check(args, 'REJECTED', 'T11_SYNTHETIC_PLAN_REJECTED')
        args = fixture()
        args[0]['t11_context'] = dict(status='DRAFT_CONTRACT_VALID', physical_ready=True)
        self.check(args, 'REJECTED', 'T11_SYNTHETIC_PLAN_REJECTED')

    def test_20_new_limits_cannot_relax_existing_scalar_profile(self):
        args = fixture()
        args[0]['scalar_limits']['max_force_fraction'] = .5
        self.check(args, 'REJECTED', 'EXACT_FIELDS_REQUIRED')
        args = fixture()
        args[0]['scalar_profile'] = 'REGISTERED_LOOSE_BOUNDS'
        self.check(args, 'REJECTED', 'UNSUPPORTED_DECLARATION')
        args = fixture()
        args[0]['extra_limits'] = None
        self.check(args, 'NOT_COMPUTED', 'EXTRA_CHANNEL_TOY_LIMITS_UNSELECTED')

    def test_21_old_scalar_window_mean_still_applies(self):
        args = fixture()
        for frame in args[2]: set_force(frame, 2.012)
        self.check(args, 'NOT_CONVERGED', 'RA_TERMINAL_SCALAR_WINDOWS_UNSTABLE')

    def test_22_reaction_uses_same_sample_and_declared_polarity(self):
        args = fixture()
        args[1][0]['channels']['reaction']['values']['raw_reaction'] = -2.
        self.check(args, 'REJECTED', 'REACTION_SAME_SAMPLE_ARITHMETIC_MISMATCH')
        args = fixture()
        args[2][0]['channels']['reaction']['values']['pressure_deck'] = 2.
        self.check(args, 'REJECTED', 'REACTION_SAME_SAMPLE_ARITHMETIC_MISMATCH')

    def test_23_nonfinite_and_unsupported_types_do_not_run_hooks(self):
        calls = []
        class HookNumber(float):
            def __float__(self): calls.append('float'); raise AssertionError('hook')
            def __eq__(self, other): calls.append('eq'); raise AssertionError('hook')
        for value in (True, float('nan'), float('inf'), HookNumber(0.)):
            args = fixture()
            args[1][0]['channels']['energy']['values']['rotational_ke'] = value
            with self.subTest(kind=type(value).__name__): self.check(args, 'REJECTED')
        self.assertEqual(calls, [])

    def test_24_extra_reordered_and_gap_observations_are_not_selected_away(self):
        for mutation in ('extra', 'reorder', 'gap'):
            args = fixture()
            if mutation == 'extra': args[1].append(copy.deepcopy(args[1][-1]))
            elif mutation == 'reorder': args[1][0], args[1][1] = args[1][1], args[1][0]
            else: del args[1][1]
            with self.subTest(mutation=mutation): self.check(args, 'REJECTED')

    def test_25_trace_bytes_remain_boundary_evidence_not_source_authentication(self):
        args = fixture()
        before = self.check(args, 'SYNTHETIC_RA_END_CANDIDATE')['boundary_candidate']
        args[2][-1]['channels']['contacts']['values']['count'] = 3
        after = self.check(args, 'SYNTHETIC_RA_END_CANDIDATE')['boundary_candidate']
        self.assertNotEqual(before['end_frame_sha256'], after['end_frame_sha256'])
        self.assertNotEqual(before['ra_trace_sha256'], after['ra_trace_sha256'])
        self.assertEqual(before['plan_sha256'], after['plan_sha256'])


if __name__ == '__main__':
    unittest.main()
