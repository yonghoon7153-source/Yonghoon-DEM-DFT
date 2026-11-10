"""Offline contract: complete synthetic channels and independent R-a diagnosis.

권고안 전제(Q-LIVE-1): exact same-frame channels, explicit synthetic units.
권고안 전제(Q-LIVE-2): full servo budget followed by an independent fixed-plate
R-a budget. Existing scalar thresholds remain synthetic, not registration.
No live reader, filesystem writes, engine command, operational seal or GO.
"""
import copy
from fractions import Fraction
import math

from dem_gen2_qualification import integer, number, observation_bridge, static_guard
from dem_gen2_t11_contract import canonical_sha256, validate_t11_plan


ASSUMPTIONS = ('Q-LIVE-1', 'Q-LIVE-2')
IDENTITY_KEYS = ('run_id', 'bed_id', 'arm_id', 'attempt_id', 'definition_id', 'unit_system_id')
SCALAR_PROFILE = 'EXISTING_SYNTHETIC_STATIC_GUARD_V1'
UNITS = {
    'reaction': 'TOY_DECK_REACTION_AREA_PRESSURE_V1',
    'energy': 'TOY_DECK_TRANSLATIONAL_ROTATIONAL_ENERGY_V1',
    'force_balance': 'TOY_DECK_FORCE_VECTOR_V1',
    'torque_balance': 'TOY_DECK_TORQUE_VECTOR_V1',
    'plate': 'TOY_DECK_POSITION_VELOCITY_V1',
    'contacts': 'EXACT_CONTACT_COUNT_V1',
    'inventory': 'TOY_ID_TYPE_RADIUS_MASS_V1',
}
_PLAN = set(('schema', 'purpose', 'protocol', 'assumptions', 't11_plan', 't11_context',
    'case_id', 'grid_choice', 'scalar_profile', 'scalar_limits', 'extra_limits',
    'inventory_id', 'reference_inventory', 'plate_reference', 'ra_window_count'))
_STAMP = set(IDENTITY_KEYS) | {'stage', 'step', 'sample_id', 'time_tick', 'window_index'}
_PLATE = {'position', 'velocity', 'mesh_id', 'wall_id', 'history_id'}
_EXTRA = {'max_rotational_ke', 'max_torque_residual', 'max_torque_damping', 'max_torque_inertia'}


class _Missing(ValueError):
    pass


def _fields(value, fields):
    if (type(value) is not dict or any(type(key) is not str for key in value)
            or set(value) != fields):
        raise ValueError('EXACT_FIELDS_REQUIRED')
    return value


def _constant(value, expected):
    if type(value) is not str or value != expected:
        raise ValueError('UNSUPPORTED_DECLARATION')


def _token(value):
    if (type(value) is not str or not 1 <= len(value) <= 128
            or any(not 32 < ord(c) < 127 for c in value)):
        raise ValueError('BOUNDED_ASCII_TOKEN_REQUIRED')
    return value


def _vector(value):
    if type(value) is not list or len(value) != 3:
        raise ValueError('EXACT_THREE_VECTOR_REQUIRED')
    return [number(v) for v in value]


def _norm(value):
    return number(math.hypot(*_vector(value)), nonnegative=True)


def _inventory(value):
    if type(value) is not list or not value:
        raise ValueError('EXPLICIT_NONEMPTY_INVENTORY_REQUIRED')
    result = {}
    for particle in value:
        _fields(particle, {'id', 'type', 'radius', 'mass'})
        ident = integer(particle['id'], 1)
        if ident in result:
            raise ValueError('DUPLICATE_INVENTORY_ID')
        result[ident] = (integer(particle['type'], 1),
            number(particle['radius'], positive=True), number(particle['mass'], positive=True))
    return result


def _plate(value):
    _fields(value, _PLATE)
    _vector(value['position'])
    _vector(value['velocity'])
    for key in ('mesh_id', 'wall_id', 'history_id'):
        _token(value[key])


def _report(status, reason, servo=None, boundary=None):
    return dict(status=status, reason=reason, boundary_candidate=boundary,
        servo_diagnostic=servo, physical_ready=False, execution_go=False,
        transition_authorized=False, gate_write=False, operational_seal_modified=False,
        registration_complete=False, source_authenticated=False,
        actual_T0='NOT_RUN', actual_T11='NOT_RUN', actual_T12='NOT_RUN',
        actual_build_identity=None, actual_compression_sign=None, research_results=0,
        assumptions=list(ASSUMPTIONS), evidence_kind='SYNTHETIC_ONLY', whole_status='HOLD')


def _prepare(plan):
    # Check the entire input before comparisons, copying or hashing can encounter
    # a supplied object subclass. This hashes JSON data only, not a source proof.
    plan_hash = canonical_sha256(plan)
    _fields(plan, _PLAN)
    for key, expected in (('schema', 'DEM_GEN2_LIVE_RA_SYNTHETIC_PLAN_V1'),
            ('purpose', 'SYNTHETIC_PREPARATION'), ('protocol', 'P2'),
            ('scalar_profile', SCALAR_PROFILE)):
        _constant(plan[key], expected)
    if type(plan['assumptions']) is not list or plan['assumptions'] != list(ASSUMPTIONS):
        raise ValueError('ASSUMPTIONS_REQUIRED')
    for item in plan['assumptions']:
        if type(item) is not str:
            raise ValueError('EXACT_ASSUMPTION_TOKENS_REQUIRED')
    t11 = validate_t11_plan(plan['t11_plan'], plan['t11_context'])
    if t11['status'] != 'DRAFT_CONTRACT_VALID':
        raise ValueError('T11_SYNTHETIC_PLAN_REJECTED')
    compiled = t11['compiled']
    grid_choice = plan['grid_choice']
    if type(grid_choice) is not str or grid_choice not in ('coarse', 'half'):
        raise ValueError('EXPLICIT_T11_GRID_REQUIRED')
    grid = compiled[grid_choice + '_grid']
    case_id = _token(plan['case_id'])
    cases = [item for item in plan['t11_plan']['cases'] if item['case_id'] == case_id]
    compiled_cases = [item for item in compiled['cases'] if item['case_id'] == case_id]
    if len(cases) != 1 or len(compiled_cases) != 1:
        raise ValueError('DECLARED_T11_CASE_REQUIRED')
    # The trace target is supplied by the selected case, not its model's errors.
    target_pair = cases[0]['target_force']
    target = number(float(Fraction(*target_pair)), positive=True)
    scalar = _fields(plan['scalar_limits'], {'max_translational_ke', 'max_drift_fraction'})
    number(scalar['max_translational_ke'], positive=True)
    number(scalar['max_drift_fraction'], nonnegative=True)
    if plan['extra_limits'] is None:
        raise _Missing('EXTRA_CHANNEL_TOY_LIMITS_UNSELECTED')
    extra = _fields(plan['extra_limits'], _EXTRA)
    for value in extra.values():
        number(value, nonnegative=True)
    inventory = _inventory(plan['reference_inventory'])
    inventory_id = _token(plan['inventory_id'])
    reference = plan['plate_reference']
    _plate(reference)
    if reference['velocity'] != [0, 0, 0]:
        raise ValueError('RA_REFERENCE_MUST_BE_FIXED')
    ra_windows = integer(plan['ra_window_count'], 2)
    t0_plan = plan['t11_context']['t0_plan']
    if reference['mesh_id'] != t0_plan['identity']['mesh_id']:
        raise ValueError('T0_MESH_DECLARATION_MISMATCH')
    identity = {key: plan['t11_plan']['identity'][key] for key in IDENTITY_KEYS[:-1]}
    identity['unit_system_id'] = plan['t11_plan']['identity']['unit_mapping_id']
    source = copy.deepcopy(t0_plan['identity'])
    source.update(t0_packet_sha256=compiled['t0_packet_sha256'],
        t11_plan_sha256=compiled['plan_sha256'], case_id=case_id, grid_choice=grid_choice)
    contract = dict(identity, schema='SYNTHETIC_OBSERVATION_BRIDGE_V1',
        purpose='SYNTHETIC_PREPARATION', source_stage='servo',
        requested_boundary='SERVO_TO_RELAXATION', first_step=grid['first_step'],
        first_sample_id=grid['first_sample_id'], first_tick=grid['first_control_tick'],
        tick_stride=grid['control_tick_stride'], planned_samples=grid['budget_ticks'],
        expected_end_step=grid['end_step'], expected_end_tick=grid['end_control_tick'],
        delay_samples=compiled_cases[0]['delay_ticks'])
    rules = dict(samples_per_window=grid['window_ticks'], sample_stride=grid['step_stride'],
        max_ke=scalar['max_translational_ke'], max_drift_fraction=scalar['max_drift_fraction'],
        expected_inventory=inventory_id, observation_contract=contract)
    return dict(plan_hash=plan_hash, source=source, identity=identity, grid=grid,
        rules=rules, target=target, inventory=inventory, extra=extra,
        compression_sign=t0_plan['fixture']['compression_sign'],
        area=t0_plan['fixture']['area_deck_m2'], reference=reference,
        ra_samples=ra_windows*grid['window_ticks'])


def _stamp(prepared, index, stage):
    grid = prepared['grid']
    offset = 0 if stage == 'servo' else grid['budget_ticks']
    return dict(prepared['identity'], stage=stage,
        step=grid['first_step']+(offset+index)*grid['step_stride'],
        sample_id=grid['first_sample_id']+offset+index,
        time_tick=grid['first_control_tick']+(offset+index)*grid['control_tick_stride'],
        window_index=index//grid['window_ticks'])


def _frame(frame, prepared, index, stage):
    _fields(frame, {'source_identity', 'stamp', 'channels'})
    source = _fields(frame['source_identity'], set(prepared['source']))
    if source != prepared['source']:
        raise ValueError('SOURCE_DECLARATION_MISMATCH')
    stamp = _fields(frame['stamp'], _STAMP)
    for key in IDENTITY_KEYS + ('stage',):
        _token(stamp[key])
    for key in ('step', 'sample_id'):
        integer(stamp[key], 1)
    for key in ('time_tick', 'window_index'):
        integer(stamp[key])
    if stamp != _stamp(prepared, index, stage):
        raise ValueError('FRAME_IDENTITY_OR_GRID_MISMATCH')
    channels = frame['channels']
    if type(channels) is not dict or any(type(key) is not str for key in channels):
        raise ValueError('EXACT_CHANNEL_MAP_REQUIRED')
    if not set(UNITS).issubset(channels):
        raise _Missing('REQUIRED_CHANNEL_NOT_COMPUTED')
    if set(channels) != set(UNITS):
        raise ValueError('UNDECLARED_CHANNEL')
    values = {}
    for name, unit_id in UNITS.items():
        channel = _fields(channels[name], {'stamp', 'unit_id', 'complete', 'values'})
        _fields(channel['stamp'], _STAMP)
        # Each channel's stamp gets its own exact-type validation: bool/1 and
        # 1.0/1 must not pass only because Python considers them equal.
        for key in IDENTITY_KEYS + ('stage',):
            _token(channel['stamp'][key])
        for key in ('step', 'sample_id'):
            integer(channel['stamp'][key], 1)
        for key in ('time_tick', 'window_index'):
            integer(channel['stamp'][key])
        if channel['stamp'] != stamp:
            raise ValueError('MIXED_CHANNEL_FRAME')
        _constant(channel['unit_id'], unit_id)
        if channel['complete'] is False or channel['complete'] is None:
            raise _Missing('CHANNEL_INCOMPLETE')
        if channel['complete'] is not True:
            raise ValueError('EXACT_COMPLETENESS_FLAG_REQUIRED')
        values[name] = channel['values']
    reaction = _fields(values['reaction'], {'raw_reaction', 'compression_sign',
        'normalized_force', 'area_deck_m2', 'pressure_deck'})
    raw = number(reaction['raw_reaction'])
    sign = reaction['compression_sign']
    if type(sign) is not int or sign != prepared['compression_sign']:
        raise ValueError('DECLARED_POLARITY_MISMATCH')
    force = number(reaction['normalized_force'], nonnegative=True)
    area = number(reaction['area_deck_m2'], positive=True)
    pressure = number(reaction['pressure_deck'], nonnegative=True)
    if force != number(sign*raw) or area != prepared['area'] or pressure != number(force/area):
        raise ValueError('REACTION_SAME_SAMPLE_ARITHMETIC_MISMATCH')
    energy = values['energy']
    if type(energy) is dict and 'rotational_ke' not in energy:
        raise _Missing('ROTATIONAL_KE_NOT_COMPUTED')
    _fields(energy, {'translational_ke', 'rotational_ke'})
    ke = number(energy['translational_ke'], nonnegative=True)
    number(energy['rotational_ke'], nonnegative=True)
    for name in ('force_balance', 'torque_balance'):
        required_balance = {'residual', 'gravity', 'damping', 'inertia'}
        if type(values[name]) is dict and not required_balance.issubset(values[name]):
            raise _Missing('BALANCE_COMPONENT_NOT_COMPUTED')
        balance = _fields(values[name], required_balance)
        for vector in balance.values():
            _vector(vector)
    plate = values['plate']
    _plate(plate)
    for key in ('mesh_id', 'wall_id', 'history_id'):
        if plate[key] != prepared['reference'][key]:
            raise ValueError('PLATE_OR_HISTORY_DECLARATION_CHANGED')
    if stage == 'relaxation' and plate != prepared['reference']:
        raise ValueError('RA_PLATE_NOT_FIXED')
    contacts = _fields(values['contacts'], {'count'})
    if contacts['count'] is None:
        raise _Missing('CONTACT_COUNT_NOT_COMPUTED')
    integer(contacts['count'])
    inv = _fields(values['inventory'], {'particles', 'escaped'})
    if integer(inv['escaped']) != 0 or _inventory(inv['particles']) != prepared['inventory']:
        raise ValueError('FULL_REFERENCE_INVENTORY_MISMATCH')
    scalar = dict(stamp, force=force, ke=ke,
        residual=_norm(values['force_balance']['residual']),
        damping=_norm(values['force_balance']['damping']),
        inertia=_norm(values['force_balance']['inertia']), escaped=0,
        inventory=prepared['rules']['expected_inventory'], contacts_complete=True,
        boundary_id='SERVO_TO_RELAXATION' if stage == 'servo' else 'RA_END')
    return scalar, values


def _extra_stable(values, limits):
    return (values['energy']['rotational_ke'] <= limits['max_rotational_ke']
        and _norm(values['torque_balance']['residual']) <= limits['max_torque_residual']
        and _norm(values['torque_balance']['damping']) <= limits['max_torque_damping']
        and _norm(values['torque_balance']['inertia']) <= limits['max_torque_inertia'])


def diagnose_live_ra(plan, servo_frames, ra_frames):
    """Revalidate original synthetic T11 inputs and complete channel traces.

The selected T11 plan supplies a grid and a case target, not observations or
registration. Existing observation_bridge remains the sole servo diagnostic.
R-a independently checks its complete declared budget and terminal two windows.
Returned hashes bind synthetic data bytes only. No actual S0 is produced.
"""
    servo = None
    try:
        prepared = _prepare(plan)
        for frames in (servo_frames, ra_frames):
            if type(frames) is not list:
                raise ValueError('EXACT_TRACE_LIST_REQUIRED')
            canonical_sha256(frames)
        grid = prepared['grid']
        if len(servo_frames) > grid['budget_ticks'] or len(ra_frames) > prepared['ra_samples']:
            raise ValueError('EXTRA_OBSERVATIONS_OUTSIDE_PLAN')
        servo_pairs = [_frame(frame, prepared, i, 'servo') for i, frame in enumerate(servo_frames)]
        servo_rows = [pair[0] for pair in servo_pairs]
        servo = observation_bridge(servo_rows, prepared['target'], prepared['rules'])
        if servo['status'] != 'SYNTHETIC_STAGE_CANDIDATE':
            return _report(servo['status'], 'SERVO_' + servo['reason'], servo)
        width = 2*grid['window_ticks']
        delay_width = prepared['rules']['observation_contract']['delay_samples']+1
        checked_servo = servo_pairs[-max(width, delay_width):]
        if any(not _extra_stable(pair[1], prepared['extra']) for pair in checked_servo):
            return _report('NOT_CONVERGED', 'SERVO_EXTRA_CHANNEL_TAIL_UNSTABLE', servo)
        # Servo's last plate position declares where the independently fixed
        # R-a plate begins. Stopping its velocity is not an engine command here.
        if servo_pairs[-1][1]['plate']['position'] != prepared['reference']['position']:
            raise ValueError('SERVO_TO_RA_PLATE_POSITION_MISMATCH')
        ra_pairs = [_frame(frame, prepared, i, 'relaxation') for i, frame in enumerate(ra_frames)]
        if len(ra_pairs) != prepared['ra_samples']:
            return _report('INCOMPLETE', 'RA_DECLARED_BUDGET_NOT_OBSERVED', servo)
        scalar_rules = {key: value for key, value in prepared['rules'].items()
                        if key != 'observation_contract'}
        ra_static = static_guard([pair[0] for pair in ra_pairs[-width:]],
            prepared['target'], scalar_rules)
        if ra_static['status'] != 'SYNTHETIC_STATIC':
            return _report('NOT_CONVERGED', 'RA_TERMINAL_SCALAR_WINDOWS_UNSTABLE', servo)
        if any(not _extra_stable(pair[1], prepared['extra']) for pair in ra_pairs[-width:]):
            return _report('NOT_CONVERGED', 'RA_TERMINAL_EXTRA_CHANNEL_WINDOWS_UNSTABLE', servo)
        end = ra_frames[-1]['stamp']
        boundary = dict(schema='SYNTHETIC_RA_BOUNDARY_CANDIDATE_V1', stage='relaxation',
            boundary_id='RA_END', identity=copy.deepcopy(prepared['identity']),
            source_identity=copy.deepcopy(prepared['source']), end_step=end['step'],
            end_sample_id=end['sample_id'], end_tick=end['time_tick'],
            end_window_index=end['window_index'], plate=copy.deepcopy(prepared['reference']),
            inventory_id=plan['inventory_id'], reference_inventory=copy.deepcopy(plan['reference_inventory']),
            plan_sha256=prepared['plan_hash'], servo_trace_sha256=canonical_sha256(servo_frames),
            ra_trace_sha256=canonical_sha256(ra_frames), end_frame_sha256=canonical_sha256(ra_frames[-1]))
        return _report('SYNTHETIC_RA_END_CANDIDATE', 'SYNTHETIC_DIAGNOSTIC_ONLY', servo, boundary)
    except _Missing as error:
        return _report('NOT_COMPUTED', error.args[0], servo)
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as error:
        reason = error.args[0] if type(error) is ValueError and error.args and type(error.args[0]) is str else 'INVALID_SYNTHETIC_INPUT'
        return _report('REJECTED', reason, servo)
