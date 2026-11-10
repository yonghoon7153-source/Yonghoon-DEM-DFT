"""Pure synthetic case matrix; never an actual qualification receipt reader.

권고안 전제(Q-QUAL-A/B): fixed case denominator, original P2/S0/LIVE input
revalidation, declared checkpoint lineage and an exact physical-time pair.
Byte/label consistency does not authenticate execution or hidden history.
"""
from fractions import Fraction
import hashlib
import json

from dem_gen2_p2_contract import validate_p2_contract, diagnose_p2_separation
from dem_gen2_s0_contract import canonical_bytes


P2_CONTRACT_PIN = 'c571a27119ace92ca34d3d6f2b61135219a3f1b4'
S0_CONTRACT_PIN = 'f4647f2b7c218a6df7def3292c092273f9d4e35f'
_SOURCE = {'evidence_kind', 'p2_contract_pin', 's0_contract_pin', 'producer_pin',
           'consumer_definition_pin', 'qualification_definition_id'}
_PLAN = {'schema', 'purpose', 'evidence_kind', 'assumptions', 'plan_id', 'revision',
         'source_manifest', 'cases', 'attempts', 'time_pair'}
_CASE = {'case_id', 'role', 'expected_attempt_id', 'expected_grid_choice',
         'expected_run_id', 'expected_definition_id', 'expected_plan_sha256',
         'expected_s0_sha256', 'expected_status', 'expected_reason'}
_ATTEMPT = {'attempt_id', 'case_id', 'parent_attempt_id', 'parent_checkpoint_sha256',
            'parent_checkpoint_step', 'checkpoint_sha256', 'checkpoint_step',
            'stage', 'start_step', 'planned_end_step', 'dt_seconds', 'terminal_state'}
_PACKET = {'case_id', 'source_manifest', 'p2_plan', 's0_bytes', 'p2_context', 'trace'}
_CONTEXT = {'schema', 'p2_contract_pin', 'expected_source_manifest',
            'expected_plan_sha256', 'freeze_ordinal', 'first_observation_ordinal'}


def _fields(value, fields):
    if (type(value) is not dict or any(type(key) is not str for key in value)
            or set(value) != fields):
        raise ValueError('EXACT_FIELDS_REQUIRED')
    return value


def _one(value, choices):
    if type(value) is not str or value not in choices:
        raise ValueError('UNSUPPORTED_DECLARATION')
    return value


def _token(value):
    if (type(value) is not str or not 1 <= len(value) <= 128
            or value[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in value)):
        raise ValueError('EXACT_SYNTHETIC_TOKEN_REQUIRED')
    return value


def _integer(value, minimum=0):
    if type(value) is not int or not minimum <= value <= 10**9:
        raise ValueError('EXACT_BOUNDED_INTEGER_REQUIRED')
    return value


def _digest(value, length=64):
    if type(value) is not str or len(value) != length or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('EXACT_LOWERCASE_DIGEST_REQUIRED')
    return value


def _rat(value):
    if type(value) is not list or len(value) != 2:
        raise ValueError('EXACT_RATIONAL_REQUIRED')
    return Fraction(_integer(value[0], 1), _integer(value[1], 1))


def _source(value):
    _fields(value, _SOURCE)
    _one(value['evidence_kind'], ('SYNTHETIC_SOURCE_DECLARATIONS',))
    _one(value['p2_contract_pin'], (P2_CONTRACT_PIN,))
    _one(value['s0_contract_pin'], (S0_CONTRACT_PIN,))
    for key in ('producer_pin', 'consumer_definition_pin'):
        _digest(value[key], 40)
    _token(value['qualification_definition_id'])
    return value


def _report(status, reason, planned=0, received=0, rows=None, missing=None,
            lineage='NOT_COMPUTED', time_pair='NOT_COMPUTED'):
    rows = [] if rows is None else rows
    return dict(status=status, reason=reason,
        planned_cases=planned, received_cases=received, checked_cases=len(rows),
        matched_expectations=sum(row['meets_expectation'] for row in rows),
        missing_case_ids=[] if missing is None else missing, case_results=rows,
        lineage_status=lineage, dt_pair_status=time_pair, actual_binary_identity=None,
        actual_qualification='NOT_RUN', actual_T0='NOT_RUN', actual_T2='NOT_RUN',
        actual_T5='NOT_RUN', actual_T10='NOT_RUN', actual_T11='NOT_RUN',
        actual_T12='NOT_RUN', actual_T13='NOT_RUN', actual_S0=None,
        physical_ready=False, execution_go=False, transition_authorized=False,
        gate_write=False, operational_seal_modified=False, registration_complete=False,
        source_authenticated=False, hidden_history_qualified=False,
        review_status='NOT_RECEIVED', research_results=0,
        assumptions=['Q-QUAL-A', 'Q-QUAL-B'], whole_status='HOLD')


def _prepare(plan, context):
    # Exact built-in JSON validation precedes supplied-value comparisons.
    plan_bytes = canonical_bytes(plan)
    canonical_bytes(context)
    _fields(context, _CONTEXT)
    _one(context['schema'], ('FROZEN_SYNTHETIC_QUALIFICATION_CONTEXT_V1',))
    _one(context['p2_contract_pin'], (P2_CONTRACT_PIN,))
    source = _source(context['expected_source_manifest'])
    if (_integer(context['freeze_ordinal']) >= _integer(context['first_observation_ordinal'])
            or _digest(context['expected_plan_sha256']) != hashlib.sha256(plan_bytes).hexdigest()):
        raise ValueError('FROZEN_PLAN_OR_DECLARED_ORDER_MISMATCH')
    _fields(plan, _PLAN)
    for key, choice in (('schema', 'DEM_GEN2_QUALIFICATION_MATRIX_V1'),
            ('purpose', 'SYNTHETIC_PREPARATION'), ('evidence_kind', 'SYNTHETIC_CASE_MATRIX')):
        _one(plan[key], (choice,))
    _token(plan['plan_id'])
    _integer(plan['revision'], 1)
    if (type(plan['assumptions']) is not list or any(type(x) is not str for x in plan['assumptions'])
            or plan['assumptions'] != ['Q-QUAL-A', 'Q-QUAL-B']):
        raise ValueError('ASSUMPTIONS_REQUIRED')
    if _source(plan['source_manifest']) != source:
        raise ValueError('EXTERNAL_SOURCE_MANIFEST_MISMATCH')
    if type(plan['cases']) is not list or not 2 <= len(plan['cases']) <= 128:
        raise ValueError('FIXED_BOUNDED_CASE_LIST_REQUIRED')
    cases = {}
    for case in plan['cases']:
        _fields(case, _CASE)
        case_id = _token(case['case_id'])
        if case_id in cases:
            raise ValueError('DUPLICATE_PLANNED_CASE')
        role = _one(case['role'], ('POSITIVE', 'EXPECTED_NEGATIVE'))
        for key in ('expected_attempt_id', 'expected_run_id', 'expected_definition_id'):
            _token(case[key])
        _one(case['expected_grid_choice'], ('coarse', 'half'))
        for key in ('expected_plan_sha256', 'expected_s0_sha256'):
            _digest(case[key])
        expected = ('SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE', 'SYNTHETIC_SEQUENCE_AND_TOY_LIMITS_ONLY')
        if role == 'EXPECTED_NEGATIVE':
            expected = ('INCOMPLETE', 'SEPARATION_OR_POST_BUDGET_INCOMPLETE')
        _one(case['expected_status'], (expected[0],))
        _one(case['expected_reason'], (expected[1],))
        cases[case_id] = case
    if type(plan['attempts']) is not list or len(plan['attempts']) != len(cases):
        raise ValueError('ONE_DECLARED_ATTEMPT_PER_CASE_REQUIRED')
    attempts, by_case = {}, {}
    for attempt in plan['attempts']:
        _fields(attempt, _ATTEMPT)
        attempt_id, case_id = _token(attempt['attempt_id']), _token(attempt['case_id'])
        if attempt_id in attempts or case_id in by_case or case_id not in cases:
            raise ValueError('DUPLICATE_OR_UNPLANNED_ATTEMPT')
        if cases[case_id]['expected_attempt_id'] != attempt_id:
            raise ValueError('CASE_ATTEMPT_IDENTITY_MISMATCH')
        _one(attempt['stage'], ('RA_END',))
        _one(attempt['terminal_state'], ('DECLARED_COMPLETE', 'DECLARED_PARTIAL', 'DECLARED_FAILED'))
        _digest(attempt['checkpoint_sha256'])
        for key in ('checkpoint_step', 'start_step', 'planned_end_step'):
            _integer(attempt[key], 1)
        if attempt['checkpoint_step'] != attempt['start_step'] or attempt['planned_end_step'] <= attempt['start_step']:
            raise ValueError('CHECKPOINT_START_OR_END_MISMATCH')
        _rat(attempt['dt_seconds'])
        if attempt['parent_attempt_id'] is None:
            if attempt['parent_checkpoint_sha256'] is not None or attempt['parent_checkpoint_step'] is not None:
                raise ValueError('ROOT_ATTEMPT_HAS_PARENT_FIELDS')
        else:
            _token(attempt['parent_attempt_id'])
            _digest(attempt['parent_checkpoint_sha256'])
            _integer(attempt['parent_checkpoint_step'], 1)
        attempts[attempt_id], by_case[case_id] = attempt, attempt
    for attempt_id, attempt in attempts.items():
        parent_id = attempt['parent_attempt_id']
        if parent_id is not None:
            if parent_id not in attempts:
                raise ValueError('UNKNOWN_RESTART_PARENT')
            parent = attempts[parent_id]
            if (attempt['parent_checkpoint_sha256'] != parent['checkpoint_sha256']
                    or attempt['checkpoint_sha256'] != parent['checkpoint_sha256']
                    or attempt['parent_checkpoint_step'] != parent['checkpoint_step']
                    or attempt['start_step'] != parent['checkpoint_step']
                    or _rat(attempt['dt_seconds']) != _rat(parent['dt_seconds'])):
                raise ValueError('RESTART_PARENT_CHECKPOINT_MISMATCH')
        seen, current = set(), attempt_id
        while current is not None:
            if current in seen:
                raise ValueError('CYCLIC_RESTART_ATTEMPTS')
            seen.add(current)
            current = attempts[current]['parent_attempt_id']
    pair = _fields(plan['time_pair'], {'coarse_case_id', 'half_case_id', 'start_seconds',
        'end_seconds', 'window_seconds', 'initial_state'})
    for key, grid in (('coarse_case_id', 'coarse'), ('half_case_id', 'half')):
        case_id = _token(pair[key])
        if case_id not in cases or cases[case_id]['role'] != 'POSITIVE' or cases[case_id]['expected_grid_choice'] != grid:
            raise ValueError('EXPLICIT_COARSE_HALF_POSITIVE_PAIR_REQUIRED')
    if pair['coarse_case_id'] == pair['half_case_id']:
        raise ValueError('DISTINCT_TIME_PAIR_CASES_REQUIRED')
    for key in ('start_seconds', 'end_seconds', 'window_seconds'):
        _rat(pair[key])
    if _rat(pair['end_seconds']) <= _rat(pair['start_seconds']):
        raise ValueError('POSITIVE_COMPARISON_DURATION_REQUIRED')
    initial = _fields(pair['initial_state'], {'scope', 'atom_payload_sha256',
        'mesh_payload_sha256', 'restart_payload_sha256', 'history_id'})
    _one(initial['scope'], ('ATOM_MESH_RESTART_DECLARED_BYTES_V1',))
    for key in ('atom_payload_sha256', 'mesh_payload_sha256', 'restart_payload_sha256'):
        _digest(initial[key])
    _token(initial['history_id'])
    return cases, by_case, source


def _packet(packet, case, attempt, source):
    _fields(packet, _PACKET)
    # Archive bytes occupy one explicit slot; all other data has the narrower
    # exact JSON contract, checked before calling existing dependency functions.
    canonical_bytes({key: value for key, value in packet.items() if key != 's0_bytes'})
    if type(packet['s0_bytes']) is not bytes or not 0 < len(packet['s0_bytes']) <= 1048576:
        raise ValueError('EXACT_BOUNDED_S0_BYTES_REQUIRED')
    if _source(packet['source_manifest']) != source:
        raise ValueError('PACKET_SOURCE_MANIFEST_MISMATCH')
    p2_plan, context = packet['p2_plan'], packet['p2_context']
    checked = validate_p2_contract(p2_plan, packet['s0_bytes'], context)
    if checked['status'] != 'SYNTHETIC_P2_CONTRACT_CONSISTENT':
        raise ValueError('ORIGINAL_P2_S0_LIVE_INPUT_REJECTED')
    if (p2_plan['header']['producer_pin'] != source['producer_pin']
            or p2_plan['header']['consumer_definition_pin'] != source['consumer_definition_pin']):
        raise ValueError('P2_SOURCE_DECLARATION_MISMATCH')
    for expected, actual in (('expected_attempt_id', 'attempt_id'),
                            ('expected_run_id', 'run_id'), ('expected_definition_id', 'definition_id')):
        if case[expected] != p2_plan['identity'][actual]:
            raise ValueError('CASE_P2_IDENTITY_MISMATCH')
    compiled = checked['compiled']
    if (case['expected_grid_choice'] != p2_plan['params']['time']['grid_choice']
            or case['expected_plan_sha256'] != compiled['plan_sha256']
            or case['expected_s0_sha256'] != compiled['s0_sha256']):
        raise ValueError('CASE_P2_PLAN_OR_S0_BINDING_MISMATCH')
    # These exact bytes have just passed P2 -> decode_s0 -> LIVE revalidation.
    # Reading the already validated JSON body does not authenticate its source.
    envelope = json.loads(packet['s0_bytes'].decode('utf-8'))['body']
    objects = {obj['role']: obj for obj in envelope['objects']}
    boundary = envelope['boundary_candidate']
    if (attempt['checkpoint_sha256'] != objects['restart']['payload_sha256']
            or attempt['checkpoint_step'] != boundary['end_step']
            or attempt['start_step'] != boundary['end_step']
            or _rat(attempt['dt_seconds']) != _rat(compiled['selected_dt_seconds'])):
        raise ValueError('ATTEMPT_S0_CHECKPOINT_OR_TIME_MISMATCH')
    observed = diagnose_p2_separation(p2_plan, packet['s0_bytes'], context, packet['trace'])
    if observed['status'] not in ('SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE', 'INCOMPLETE'):
        raise ValueError('P2_TRACE_FAILURE_IS_NOT_EXPECTED_PARTIAL')
    if observed['status'] == 'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE':
        if observed['post_end']['step'] != attempt['planned_end_step']:
            raise ValueError('DECLARED_ATTEMPT_END_MISMATCH')
    else:
        windows = [row for row in packet['trace'] if row['kind'] == 'WINDOW']
        if windows and windows[-1]['end_step'] > attempt['planned_end_step']:
            raise ValueError('PARTIAL_TRACE_EXCEEDS_PLANNED_END')
    expected = (observed['status'] == case['expected_status'] and observed['reason'] == case['expected_reason'])
    if case['role'] == 'EXPECTED_NEGATIVE' and not expected:
        raise ValueError('EXPECTED_NEGATIVE_MISMATCH')
    # A complete P2 toy diagnostic does not erase a declared failed attempt.
    complete = (observed['status'] == 'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE'
                and attempt['terminal_state'] == 'DECLARED_COMPLETE')
    meets = expected and (complete if case['role'] == 'POSITIVE'
                         else attempt['terminal_state'] == 'DECLARED_PARTIAL')
    row = dict(case_id=case['case_id'], role=case['role'], observed_status=observed['status'],
        observed_reason=observed['reason'], meets_expectation=meets,
        attempt_terminal_state=attempt['terminal_state'], synthetic_case_complete=complete)
    return row, dict(objects=objects, boundary=boundary, p2_plan=p2_plan, compiled=compiled)


def _time_pair(pair, cases, by_case, checked):
    coarse_id, half_id = pair['coarse_case_id'], pair['half_case_id']
    if coarse_id not in checked or half_id not in checked:
        return 'NOT_COMPUTED'
    coarse_dt, half_dt = (_rat(by_case[key]['dt_seconds']) for key in (coarse_id, half_id))
    if half_dt*2 != coarse_dt:
        raise ValueError('NOT_AN_EXACT_DT_HALF_PAIR')
    for key in (coarse_id, half_id):
        attempt, packet = by_case[key], checked[key]
        dt = _rat(attempt['dt_seconds'])
        if (dt*attempt['start_step'] != _rat(pair['start_seconds'])
                or dt*attempt['planned_end_step'] != _rat(pair['end_seconds'])
                or _rat(packet['p2_plan']['params']['time']['window_seconds']) != _rat(pair['window_seconds'])):
            raise ValueError('EXACT_SAME_PHYSICAL_TIME_REQUIRED')
        initial = pair['initial_state']
        for role in ('atom', 'mesh', 'restart'):
            if packet['objects'][role]['payload_sha256'] != initial[role+'_payload_sha256']:
                raise ValueError('DECLARED_INITIAL_STATE_BYTES_MISMATCH')
        if packet['boundary']['plate']['history_id'] != initial['history_id']:
            raise ValueError('INITIAL_HISTORY_DECLARATION_MISMATCH')
    return 'SYNTHETIC_TIME_PAIR_CONSISTENT'


def validate_qualification_matrix(plan, packets, frozen_context):
    """Evaluate every declared synthetic case without granting real readiness.

The two supported case roles are a complete P2 toy trace and the specifically
expected incomplete post-budget control. No actual binary/history/restart
receipt is authenticated or accepted. Lineage compares declarations and opaque
checkpoint bytes, not engine restoration. Missing cases keep their denominator.
"""
    planned, received, rows = 0, 0, []
    try:
        cases, attempts, source = _prepare(plan, frozen_context)
        planned = len(cases)
        if type(packets) is not list or len(packets) > 128:
            raise ValueError('EXACT_BOUNDED_PACKET_LIST_REQUIRED')
        received = len(packets)
        packet_map = {}
        for packet in packets:
            _fields(packet, _PACKET)
            case_id = _token(packet['case_id'])
            if case_id in packet_map or case_id not in cases:
                raise ValueError('DUPLICATE_OR_UNPLANNED_PACKET')
            packet_map[case_id] = packet
        missing = [key for key in cases if key not in packet_map]
        checked = {}
        for case_id, case in cases.items():
            if case_id in packet_map:
                row, prepared = _packet(packet_map[case_id], case, attempts[case_id], source)
                rows.append(row)
                checked[case_id] = prepared
        time_status = _time_pair(plan['time_pair'], cases, attempts, checked)
        lineage = 'NOT_COMPUTED' if missing else 'SYNTHETIC_LINEAGE_CONSISTENT'
        if missing or any(not row['meets_expectation'] for row in rows):
            return _report('INCOMPLETE', 'FIXED_CASE_MATRIX_NOT_COMPLETE', planned,
                received, rows, missing, lineage, time_status)
        return _report('SYNTHETIC_MATRIX_CONSISTENT', 'DECLARATIONS_AND_SYNTHETIC_CASES_ONLY',
            planned, received, rows, missing, lineage, time_status)
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as error:
        reason = error.args[0] if type(error) is ValueError and error.args and type(error.args[0]) is str else 'INVALID_SYNTHETIC_MATRIX'
        return _report('REJECTED', reason, planned, received)
