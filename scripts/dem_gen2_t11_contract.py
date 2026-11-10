"""Pure synthetic T11 plan consistency; no readers, oracle runs or authority.

권고안 전제(Q-T11-01): exact rational physical time and integer ticks.
권고안 전제(Q-T11-02): explicit finite cases, including unstable controls.
권고안 전제(Q-T11-03): error clip = actuator limit / proportional gain.
권고안 전제(Q-T11-04): frozen synthetic bytes and declared event ordering.
Hashes and ordinals are consistency checks, not evidence authentication.
"""
from fractions import Fraction
import hashlib
import json
import math

from dem_gen2_t0_contract import validate_t0_contract


T0_CONTRACT_PIN = 'c5ebaa71298691020313e272b39c0a80b51cdc4d'
ASSUMPTIONS = ('Q-T11-01', 'Q-T11-02', 'Q-T11-03', 'Q-T11-04')
_PLAN = frozenset(('schema', 'purpose', 'protocol', 'plan_id', 'revision',
    'assumptions', 'range_claim', 'identity', 't0_binding', 'units', 'time', 'cases'))
_IDENTITY = frozenset(('run_id', 'bed_id', 'arm_id', 'attempt_id', 'definition_id',
                       'unit_mapping_id'))
_T0 = frozenset(('contract_pin', 'packet_sha256', 'compression_sign',
                 'reaction_component', 'compression_velocity_sign'))
_UNITS = frozenset(('force_id', 'length_id', 'physical_time_id', 'deck_time_id',
                    'physical_seconds_per_deck_time'))
_TIME = frozenset(('dt_deck', 'dt_half_deck', 'control_period_seconds',
                   'window_seconds', 'budget_seconds'))
_CASE = frozenset(('case_id', 'K_force_per_length', 'kp',
    'vmax_length_per_second', 'target_force', 'u_limit', 'delay_seconds',
    'oracle_tolerance', 'oracle_divergence'))
_CONTEXT = frozenset(('schema', 'expected_plan_sha256', 'expected_t0_packet_sha256',
    't0_contract_pin', 't0_plan', 't0_controls', 'freeze_ordinal',
    'first_observation_ordinal'))


def _dictionary(value, keys):
    if (type(value) is not dict or any(type(key) is not str for key in value)
            or set(value) != keys):
        raise ValueError('EXACT_FIELDS_REQUIRED')
    return value


def _constant(value, expected):
    if type(value) is not str or value != expected:
        raise ValueError('UNSUPPORTED_DECLARATION')


def _token(value):
    if (type(value) is not str or not 1 <= len(value) <= 128
            or value[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in value)):
        raise ValueError('SYNTHETIC_ALIAS_REQUIRED')
    return value


def _integer(value, minimum):
    if type(value) is not int or value < minimum:
        raise ValueError('EXACT_INTEGER_REQUIRED')
    return value


def _digest(value):
    if type(value) is not str or len(value) != 64 or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('SHA256_REQUIRED')
    return value


def _rational(value, allow_zero=False):
    if (type(value) is not list or len(value) != 2
            or type(value[0]) is not int or type(value[1]) is not int
            or value[1] <= 0 or value[0] < (0 if allow_zero else 1)):
        raise ValueError('EXACT_RATIONAL_REQUIRED')
    return Fraction(value[0], value[1])


def _pair(value):
    return [value.numerator, value.denominator]


def _exact_count(value, minimum):
    if value.denominator != 1 or value.numerator < minimum:
        raise ValueError('NONINTEGER_OR_SHORT_TIME_GRID')
    return value.numerator


def _oracle_float(value):
    try:
        result = float(value)
    except (OverflowError, ValueError):
        raise ValueError('ORACLE_FLOAT_UNREPRESENTABLE') from None
    if not math.isfinite(result) or result <= 0:
        raise ValueError('ORACLE_FLOAT_UNREPRESENTABLE')
    return result


def canonical_sha256(value):
    """Hash exact built-in JSON data without invoking object conversion hooks.

Finite built-in floats are supported for the already declared T0 packet.
T11 numeric fields themselves have the narrower exact-rational schema.
This is byte identity under this convention, not canonical mathematical value.
"""
    def inspect(item, ancestors, depth):
        if depth > 64:
            raise ValueError('JSON_DEPTH_LIMIT')
        kind = type(item)
        if kind in (type(None), bool, int, str):
            return
        if kind is float:
            if not math.isfinite(item):
                raise ValueError('NONFINITE_JSON')
            return
        if kind not in (dict, list):
            raise ValueError('BUILTIN_JSON_REQUIRED')
        if id(item) in ancestors:
            raise ValueError('CYCLIC_JSON')
        ancestors = ancestors | {id(item)}
        if kind is dict:
            for key, member in item.items():
                if type(key) is not str:
                    raise ValueError('EXACT_STRING_KEYS_REQUIRED')
                inspect(member, ancestors, depth + 1)
        else:
            for member in item:
                inspect(member, ancestors, depth + 1)
    inspect(value, set(), 0)
    payload = json.dumps(value, sort_keys=True, ensure_ascii=True,
                         separators=(',', ':'), allow_nan=False).encode('ascii')
    return hashlib.sha256(payload).hexdigest()


def _grid(dt, control_period, window, budget):
    control_steps = _exact_count(control_period / dt, 1)
    window_ticks = _exact_count(window / control_period, 2)
    budget_ticks = _exact_count(budget / control_period, 2 * window_ticks)
    if budget_ticks % window_ticks:
        raise ValueError('INCOMPLETE_END_WINDOW')
    return dict(dt_seconds=_pair(dt), control_steps=control_steps,
        window_ticks=window_ticks, budget_ticks=budget_ticks, first_step=control_steps,
        first_sample_id=1, first_control_tick=1, step_stride=control_steps,
        sample_stride=1, control_tick_stride=1, end_step=control_steps * budget_ticks,
        end_control_tick=budget_ticks, terminal_window_ticks=2 * window_ticks,
        physical_end_seconds=_pair(control_steps * budget_ticks * dt))


def validate_t11_plan(plan, frozen_context):
    """Compile only an exactly frozen synthetic T11 plan, all-or-nothing.

The returned oracle arguments can be used by an explicitly separate synthetic
test of existing servo_probe. This function never executes that probe. A valid
plan may intentionally be unstable. No stage transition or actual GO follows.
"""
    def report(status, reason, compiled=None):
        return dict(status=status, reason=reason, compiled=compiled,
            actual_T0='NOT_RUN', actual_compression_sign=None,
            actual_build_identity=None, registration_complete=False,
            physical_ready=False, execution_go=False, gate_write=False,
            operational_seal_modified=False, research_results=0,
            assumptions=list(ASSUMPTIONS), evidence_kind='SYNTHETIC_ONLY',
            whole_status='HOLD')

    try:
        _dictionary(frozen_context, _CONTEXT)
        _constant(frozen_context['schema'], 'DEM_GEN2_T11_FROZEN_SYNTHETIC_CONTEXT_V1')
        _constant(frozen_context['t0_contract_pin'], T0_CONTRACT_PIN)
        expected_plan = _digest(frozen_context['expected_plan_sha256'])
        expected_t0 = _digest(frozen_context['expected_t0_packet_sha256'])
        freeze = _integer(frozen_context['freeze_ordinal'], 0)
        observed = _integer(frozen_context['first_observation_ordinal'], 0)
        if freeze >= observed:
            raise ValueError('PLAN_NOT_BEFORE_DECLARED_OBSERVATION')

        # Revalidate complete original T0 inputs; do not accept a status receipt.
        t0_plan, controls = frozen_context['t0_plan'], frozen_context['t0_controls']
        t0_result = validate_t0_contract(t0_plan, controls)
        if t0_result['status'] != 'SYNTHETIC_T0_CONTRACT_CONSISTENT':
            raise ValueError('T0_SYNTHETIC_PACKET_REJECTED')
        t0_digest = canonical_sha256(dict(synthetic_plan=t0_plan, synthetic_controls=controls))
        if t0_digest != expected_t0:
            raise ValueError('T0_FROZEN_BYTES_MISMATCH')

        _dictionary(plan, _PLAN)
        for key, expected in (('schema', 'DEM_GEN2_T11_SYNTHETIC_PLAN_V1'),
                ('purpose', 'SYNTHETIC_PREPARATION'), ('protocol', 'P2'),
                ('range_claim', 'EXPLICIT_CASE_LIST_ONLY')):
            _constant(plan[key], expected)
        _token(plan['plan_id'])
        _integer(plan['revision'], 1)
        assumptions = plan['assumptions']
        if (type(assumptions) is not list or len(assumptions) != len(ASSUMPTIONS)
                or any(type(v) is not str for v in assumptions)
                or assumptions != list(ASSUMPTIONS)):
            raise ValueError('ASSUMPTIONS_REQUIRED')
        identity = _dictionary(plan['identity'], _IDENTITY)
        for value in identity.values():
            _token(value)
        for key in ('run_id', 'attempt_id', 'unit_mapping_id'):
            if identity[key] != t0_plan['identity'][key]:
                raise ValueError('T0_IDENTITY_MISMATCH')
        binding = _dictionary(plan['t0_binding'], _T0)
        _constant(binding['contract_pin'], T0_CONTRACT_PIN)
        if _digest(binding['packet_sha256']) != t0_digest:
            raise ValueError('T0_BINDING_MISMATCH')
        if (type(binding['compression_sign']) is not int
                or binding['compression_sign'] != t0_plan['fixture']['compression_sign']):
            raise ValueError('T0_POLARITY_MISMATCH')
        _constant(binding['reaction_component'], t0_plan['identity']['reaction_component'])
        if type(binding['compression_velocity_sign']) is not int or binding['compression_velocity_sign'] != -1:
            raise ValueError('UNSUPPORTED_COMPRESSION_DIRECTION')
        units = _dictionary(plan['units'], _UNITS)
        for key, expected in (('force_id', 'GEN2_DECK_FORCE'), ('length_id', 'GEN2_DECK_LENGTH'),
                ('physical_time_id', 's'), ('deck_time_id', 'GEN2_DECK_TIME')):
            _constant(units[key], expected)
        scale = _rational(units['physical_seconds_per_deck_time'])
        times = _dictionary(plan['time'], _TIME)
        dt = _rational(times['dt_deck']) * scale
        dt_half = _rational(times['dt_half_deck']) * scale
        if dt_half * 2 != dt:
            raise ValueError('NOT_EXACT_DT_HALF_PAIR')
        period = _rational(times['control_period_seconds'])
        window = _rational(times['window_seconds'])
        budget = _rational(times['budget_seconds'])
        coarse, half = _grid(dt, period, window, budget), _grid(dt_half, period, window, budget)

        cases = plan['cases']
        if type(cases) is not list or not cases:
            raise ValueError('EXPLICIT_CASES_REQUIRED')
        case_ids, compiled_cases = set(), []
        for case in cases:
            _dictionary(case, _CASE)
            case_id = _token(case['case_id'])
            if case_id in case_ids:
                raise ValueError('DUPLICATE_CASE_ID')
            case_ids.add(case_id)
            stiffness = _rational(case['K_force_per_length'])
            gain = _rational(case['kp'])
            velocity = _rational(case['vmax_length_per_second'])
            target = _rational(case['target_force'])
            limit = _rational(case['u_limit'])
            delay_time = _rational(case['delay_seconds'], allow_zero=True)
            tolerance = _rational(case['oracle_tolerance'])
            divergence = _rational(case['oracle_divergence'])
            if limit > 1 or tolerance >= 1 or divergence <= 1:
                raise ValueError('UNSUPPORTED_ORACLE_DOMAIN')
            delay = _exact_count(delay_time / period, 0)
            if delay >= coarse['budget_ticks']:
                raise ValueError('DELAY_OUTSIDE_DECLARED_BUDGET')
            a = stiffness * gain * velocity * period / target
            saturation = limit / gain
            oracle_args = dict(a=_oracle_float(a), delay=delay,
                saturation=_oracle_float(saturation), budget=coarse['budget_ticks'],
                tolerance=_oracle_float(tolerance), divergence=_oracle_float(divergence),
                consecutive=2 * coarse['window_ticks'])
            if oracle_args['tolerance'] >= 1 or oracle_args['divergence'] <= 1:
                raise ValueError('ORACLE_FLOAT_DOMAIN_COLLAPSED')
            compiled_cases.append(dict(case_id=case_id, exact_a=_pair(a),
                exact_error_clip=_pair(saturation), delay_ticks=delay,
                oracle_args=oracle_args, model_result='NOT_RUN'))

        plan_digest = canonical_sha256(plan)
        if plan_digest != expected_plan:
            raise ValueError('PLAN_FROZEN_BYTES_MISMATCH')
        compiled = dict(plan_sha256=plan_digest, t0_packet_sha256=t0_digest,
            t0_contract_pin=T0_CONTRACT_PIN, coarse_grid=coarse, half_grid=half,
            cases=compiled_cases, checked_cases=len(compiled_cases),
            t0_checked_controls=t0_result['checked_cases'],
            range_claim='EXPLICIT_CASE_LIST_ONLY', model_results='NOT_RUN')
        return report('DRAFT_CONTRACT_VALID', 'SYNTHETIC_CONSISTENCY_ONLY', compiled)
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as error:
        # Error messages originate here/T0/stdlib, never format supplied objects.
        reason = error.args[0] if type(error) is ValueError and error.args and type(error.args[0]) is str else 'INVALID_SYNTHETIC_PLAN'
        return report('REJECTED', reason)
