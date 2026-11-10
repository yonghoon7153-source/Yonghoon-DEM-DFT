"""Pure synthetic S0 envelope/bytes contract; no filesystem or engine access.

권고안 전제(Q-S0-1): the complete revalidated R-a boundary and six objects.
권고안 전제(Q-S0-2): canonical UTF-8 bytes with declared synthetic mappings.
Byte equality never qualifies hidden history, a real restart or actual T12.
"""
import base64
import binascii
import hashlib
import json
import math

from dem_gen2_live_contract import diagnose_live_ra


ASSUMPTIONS = ('Q-S0-1', 'Q-S0-2')
ROLES = ('atom', 'pair', 'wall', 'mesh', 'restart', 'state')
ATOM_COLUMNS = ('id', 'type', 'x', 'y', 'z', 'radius', 'mass', 'vx', 'vy', 'vz',
                'omegax', 'omegay', 'omegaz', 'fx', 'fy', 'fz')
ATOM_UNITS = ('identity', 'type_identity', 'length', 'length', 'length', 'length',
              'mass', 'velocity', 'velocity', 'velocity', 'angular_velocity',
              'angular_velocity', 'angular_velocity', 'force', 'force', 'force')
PAIR_COLUMNS = tuple('c_cpl[%d]' % i for i in range(1, 27))
WALL_U_COLUMNS = ('mesh', 'tri', 'id', 'fnx', 'fny', 'fnz')
WALL_R_COLUMNS = WALL_U_COLUMNS + ('delta_max', 'shear_x', 'shear_y', 'shear_z')
MAX_PAYLOAD_BYTES = 65536
MAX_ARCHIVE_BYTES = 1048576
MAX_ATOMS = 256
MAX_CONTACT_ROWS = 1024
_CONTRACT = frozenset(('schema', 'purpose', 's0_id', 'assumptions',
    'boundary_sha256', 'pair_reference', 'wall_reference'))
_REFERENCE = frozenset(('schema', 'mapping_id', 'source_pin', 'scope', 'profile',
    'columns', 'units', 'meanings', 'overlap_semantics', 'hidden_history_qualified'))
_ENVELOPE = frozenset(('schema', 'purpose', 's0_id', 'boundary_candidate', 'objects'))
_OBJECT = frozenset(('role', 'format_revision', 'boundary_sha256', 'step',
    'mesh_id', 'wall_id', 'history_id', 'inventory_id', 'generation_ordinal',
    'parent_sha256', 'media_type', 'columns', 'units', 'semantic_mapping_sha256',
    'payload_base64', 'payload_bytes', 'payload_sha256'))
_WRAPPER = frozenset(('schema', 'body', 'body_bytes', 'body_sha256'))


class _Missing(ValueError):
    pass


def _fields(value, keys):
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ValueError('EXACT_DICTIONARY_REQUIRED')
    if not keys.issubset(value):
        raise _Missing('REQUIRED_FIELDS_NOT_COMPUTED')
    if set(value) != keys:
        raise ValueError('UNDECLARED_FIELDS')
    return value


def _constant(value, expected):
    if type(value) is not str or value != expected:
        raise ValueError('UNSUPPORTED_DECLARATION')


def _token(value):
    if (type(value) is not str or not 1 <= len(value) <= 128
            or value[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in value)):
        raise ValueError('EXACT_SYNTHETIC_TOKEN_REQUIRED')
    return value


def _integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('EXACT_INTEGER_REQUIRED')
    return value


def _number(value, positive=False):
    if type(value) not in (int, float):
        raise ValueError('FINITE_BUILTIN_NUMBER_REQUIRED')
    try:
        finite = math.isfinite(value)
    except (OverflowError, ValueError):
        finite = False
    if not finite or (positive and value <= 0):
        raise ValueError('FINITE_BUILTIN_NUMBER_REQUIRED')
    return value


def _digest(value, length=64):
    if type(value) is not str or len(value) != length or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('FIXED_LOWERCASE_DIGEST_REQUIRED')
    return value


def canonical_bytes(value):
    """Exact built-in JSON only; no conversion methods or object hooks."""
    def inspect(item, active, depth):
        if depth > 64:
            raise ValueError('JSON_DEPTH_LIMIT')
        kind = type(item)
        if kind in (type(None), bool, int):
            return
        if kind is str:
            # Reject lone surrogates before producing UTF-8.
            try:
                item.encode('utf-8')
            except UnicodeError:
                raise ValueError('INVALID_UTF8_STRING') from None
            return
        if kind is float:
            if not math.isfinite(item):
                raise ValueError('NONFINITE_JSON')
            return
        if kind not in (dict, list):
            raise ValueError('EXACT_BUILTIN_JSON_REQUIRED')
        if id(item) in active:
            raise ValueError('CYCLIC_JSON')
        active = active | {id(item)}
        if kind is dict:
            for key, member in item.items():
                if type(key) is not str:
                    raise ValueError('EXACT_STRING_KEY_REQUIRED')
                inspect(key, active, depth + 1)
                inspect(member, active, depth + 1)
        else:
            for member in item:
                inspect(member, active, depth + 1)
    inspect(value, set(), 0)
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def sha256_bytes(value):
    if type(value) is not bytes:
        raise ValueError('EXACT_BYTES_REQUIRED')
    return hashlib.sha256(value).hexdigest()


def _decode_json(data, limit):
    if type(data) is not bytes or not 0 < len(data) <= limit:
        raise ValueError('SYNTHETIC_BYTE_BUDGET_OR_TYPE')
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def constant(_):
        raise ValueError('NONSTANDARD_JSON_CONSTANT')
    try:
        value = json.loads(data.decode('utf-8'), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, json.JSONDecodeError):
        raise ValueError('INVALID_UTF8_JSON') from None
    if canonical_bytes(value) != data:
        raise ValueError('NONCANONICAL_JSON_BYTES')
    return value


def _list_equal(value, expected):
    if type(value) is not list or any(type(item) is not str for item in value):
        raise ValueError('EXACT_COLUMN_OR_UNIT_LIST_REQUIRED')
    if value != list(expected):
        raise _Missing('REQUIRED_COLUMN_MAPPING_NOT_COMPUTED')


def _reference(value, role):
    _fields(value, _REFERENCE)
    _constant(value['schema'], 'SYNTHETIC_S0_MAPPING_REFERENCE_V1')
    _constant(value['scope'], 'DECLARED_SYNTHETIC_MAPPING_ONLY')
    _token(value['mapping_id'])
    _digest(value['source_pin'], 40)
    if type(value['hidden_history_qualified']) is not bool or value['hidden_history_qualified'] is not False:
        raise ValueError('HIDDEN_HISTORY_QUALIFICATION_NOT_SUPPORTED')
    if role == 'pair':
        _constant(value['profile'], 'PAIR26')
        _constant(value['overlap_semantics'], 'CURRENT_OVERLAP_ONLY')
        columns = PAIR_COLUMNS
    else:
        if type(value['profile']) is not str or value['profile'] not in ('WALL_U', 'WALL_R'):
            raise ValueError('EXPLICIT_WALL_PROFILE_REQUIRED')
        _constant(value['overlap_semantics'], 'DECLARED_OBSERVABLES_NOT_HIDDEN_HISTORY_PROOF')
        columns = WALL_U_COLUMNS if value['profile'] == 'WALL_U' else WALL_R_COLUMNS
    _list_equal(value['columns'], columns)
    for key in ('units', 'meanings'):
        values = value[key]
        if type(values) is not list or len(values) != len(columns):
            raise _Missing('EXPLICIT_SEMANTIC_MAPPING_NOT_COMPUTED')
        for item in values:
            _token(item)
    if role == 'pair' and value['meanings'][22] != 'current_overlap':
        raise ValueError('CURRENT_OVERLAP_IS_NOT_HIDDEN_HISTORY')
    return value


def _payload(obj):
    encoded = obj['payload_base64']
    if type(encoded) is not str or len(encoded) > 4*((MAX_PAYLOAD_BYTES+2)//3):
        raise ValueError('SYNTHETIC_PAYLOAD_BUDGET_OR_TYPE')
    try:
        data = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        raise ValueError('INVALID_BASE64') from None
    if base64.b64encode(data).decode('ascii') != encoded:
        raise ValueError('NONCANONICAL_BASE64')
    if not 0 < len(data) <= MAX_PAYLOAD_BYTES:
        raise ValueError('SYNTHETIC_PAYLOAD_BUDGET')
    if _integer(obj['payload_bytes'], 1) != len(data):
        raise ValueError('PAYLOAD_LENGTH_MISMATCH')
    if _digest(obj['payload_sha256']) != sha256_bytes(data):
        raise ValueError('PAYLOAD_DIGEST_MISMATCH')
    return data


def _inventory(reference):
    if type(reference) is not list or not 0 < len(reference) <= MAX_ATOMS:
        raise ValueError('SYNTHETIC_INVENTORY_BUDGET_OR_TYPE')
    inventory = {}
    for row in reference:
        _fields(row, {'id', 'type', 'radius', 'mass'})
        identity = _integer(row['id'], 1)
        if identity in inventory:
            raise ValueError('DUPLICATE_REFERENCE_ID')
        inventory[identity] = (_integer(row['type'], 1), _number(row['radius'], True), _number(row['mass'], True))
    return inventory


def _typed_rows(data, role, width):
    payload = _decode_json(data, MAX_PAYLOAD_BYTES)
    _fields(payload, {'schema', 'rows'})
    _constant(payload['schema'], 'SYNTHETIC_S0_' + role.upper() + '_PAYLOAD_V1')
    rows = payload['rows']
    limit = MAX_ATOMS if role == 'atom' else MAX_CONTACT_ROWS
    if type(rows) is not list or len(rows) > limit:
        raise ValueError('SYNTHETIC_ROW_BUDGET_OR_TYPE')
    for row in rows:
        if type(row) is not list or len(row) != width:
            raise _Missing('REQUIRED_ROW_COLUMNS_NOT_COMPUTED')
        for number in row:
            _number(number)
    return rows


def validate_s0_envelope(contract, envelope, live_plan, servo_frames, ra_frames):
    """Compare six objects to the complete revalidated synthetic LIVE boundary."""
    def report(status, reason, checked=0):
        return dict(status=status, reason=reason, checked_objects=checked,
            physical_ready=False, execution_go=False, transition_authorized=False,
            gate_write=False, operational_seal_modified=False, registration_complete=False,
            source_authenticated=False, hidden_history_qualified=False,
            actual_T0='NOT_RUN', actual_T11='NOT_RUN', actual_T12='NOT_RUN',
            actual_S0=None, research_results=0, assumptions=list(ASSUMPTIONS),
            evidence_kind='SYNTHETIC_ONLY', whole_status='HOLD')
    try:
        # Check built-in data before any comparison can invoke supplied hooks.
        canonical_bytes(contract)
        envelope_bytes = canonical_bytes(envelope)
        if len(envelope_bytes) > MAX_ARCHIVE_BYTES:
            raise ValueError('SYNTHETIC_ARCHIVE_BUDGET')
        _fields(contract, _CONTRACT)
        _constant(contract['schema'], 'SYNTHETIC_S0_CONTRACT_V1')
        _constant(contract['purpose'], 'SYNTHETIC_PREPARATION')
        s0_id = _token(contract['s0_id'])
        _list_equal(contract['assumptions'], ASSUMPTIONS)
        expected_boundary = _digest(contract['boundary_sha256'])
        pair_reference = _reference(contract['pair_reference'], 'pair')
        wall_reference = _reference(contract['wall_reference'], 'wall')

        live = diagnose_live_ra(live_plan, servo_frames, ra_frames)
        if live['status'] != 'SYNTHETIC_RA_END_CANDIDATE':
            return report('NOT_COMPUTED', 'LIVE_RA_BOUNDARY_NOT_AVAILABLE')
        boundary = live['boundary_candidate']
        boundary_bytes = canonical_bytes(boundary)
        boundary_hash = sha256_bytes(boundary_bytes)
        if boundary_hash != expected_boundary:
            raise ValueError('FROZEN_BOUNDARY_MISMATCH')
        _fields(envelope, _ENVELOPE)
        _constant(envelope['schema'], 'SYNTHETIC_S0_ENVELOPE_V1')
        _constant(envelope['purpose'], 'SYNTHETIC_PREPARATION')
        _constant(envelope['s0_id'], s0_id)
        if canonical_bytes(envelope['boundary_candidate']) != boundary_bytes:
            raise ValueError('COMPLETE_BOUNDARY_MISMATCH')
        inventory = _inventory(boundary['reference_inventory'])
        objects = envelope['objects']
        if type(objects) is not list or len(objects) != len(ROLES):
            raise _Missing('EXACT_SIX_OBJECTS_REQUIRED')
        parent_hash = boundary_hash
        for ordinal, (role, obj) in enumerate(zip(ROLES, objects)):
            _fields(obj, _OBJECT)
            _constant(obj['role'], role)
            if type(obj['format_revision']) is not int or obj['format_revision'] != 1:
                raise ValueError('UNSUPPORTED_FORMAT_REVISION')
            if _digest(obj['boundary_sha256']) != boundary_hash:
                raise ValueError('OBJECT_BOUNDARY_MISMATCH')
            if _integer(obj['step'], 1) != boundary['end_step']:
                raise ValueError('OBJECT_END_STEP_MISMATCH')
            for key in ('mesh_id', 'wall_id', 'history_id'):
                _constant(obj[key], boundary['plate'][key])
            _constant(obj['inventory_id'], boundary['inventory_id'])
            if _integer(obj['generation_ordinal']) != ordinal or _digest(obj['parent_sha256']) != parent_hash:
                raise ValueError('OBJECT_GENERATION_CHAIN_MISMATCH')
            data = _payload(obj)
            if role == 'atom':
                _constant(obj['media_type'], 'application/json')
                _list_equal(obj['columns'], ATOM_COLUMNS)
                _list_equal(obj['units'], ATOM_UNITS)
                atom_reference = dict(schema='SYNTHETIC_ATOM16_MAPPING_V1', columns=list(ATOM_COLUMNS), units=list(ATOM_UNITS))
                if _digest(obj['semantic_mapping_sha256']) != sha256_bytes(canonical_bytes(atom_reference)):
                    raise ValueError('ATOM_MAPPING_MISMATCH')
                rows = _typed_rows(data, role, len(ATOM_COLUMNS))
                found = {}
                for row in rows:
                    identity = _integer(row[0], 1)
                    if identity in found:
                        raise ValueError('DUPLICATE_ATOM_ID')
                    found[identity] = (_integer(row[1], 1), _number(row[5], True), _number(row[6], True))
                if found != inventory:
                    raise ValueError('ATOM_REFERENCE_INVENTORY_MISMATCH')
            elif role in ('pair', 'wall'):
                reference = pair_reference if role == 'pair' else wall_reference
                _constant(obj['media_type'], 'application/json')
                _list_equal(obj['columns'], reference['columns'])
                _list_equal(obj['units'], reference['units'])
                if _digest(obj['semantic_mapping_sha256']) != sha256_bytes(canonical_bytes(reference)):
                    raise ValueError('DECLARED_MAPPING_MISMATCH')
                rows = _typed_rows(data, role, len(reference['columns']))
                if role == 'wall':
                    for row in rows:
                        _integer(row[0], 0)
                        _integer(row[1], 0)
                        if _integer(row[2], 1) not in inventory:
                            raise ValueError('WALL_PARTICLE_OUTSIDE_INVENTORY')
            else:
                _constant(obj['media_type'], 'application/octet-stream')
                _list_equal(obj['columns'], ())
                _list_equal(obj['units'], ())
                opaque_reference = dict(schema='OPAQUE_SYNTHETIC_BYTES_ONLY', role=role)
                if _digest(obj['semantic_mapping_sha256']) != sha256_bytes(canonical_bytes(opaque_reference)):
                    raise ValueError('OPAQUE_MAPPING_MISMATCH')
            parent_hash = sha256_bytes(canonical_bytes(obj))
        return report('SYNTHETIC_S0_CONSISTENT', 'DECLARATION_AND_BYTE_IDENTITY_ONLY', len(ROLES))
    except _Missing as error:
        return report('NOT_COMPUTED', error.args[0])
    except (KeyError, TypeError, ValueError, OverflowError, RecursionError) as error:
        reason = error.args[0] if type(error) is ValueError and error.args and type(error.args[0]) is str else 'INVALID_SYNTHETIC_INPUT'
        return report('REJECTED', reason)


def serialize_s0(contract, envelope, live_plan, servo_frames, ra_frames):
    """Return canonical bytes only after complete validation; never write a file."""
    result = validate_s0_envelope(contract, envelope, live_plan, servo_frames, ra_frames)
    if result['status'] != 'SYNTHETIC_S0_CONSISTENT':
        raise ValueError(result['reason'])
    body = canonical_bytes(envelope)
    wrapper = dict(schema='SYNTHETIC_S0_ARCHIVE_V1', body=envelope,
                   body_bytes=len(body), body_sha256=sha256_bytes(body))
    data = canonical_bytes(wrapper)
    if len(data) > MAX_ARCHIVE_BYTES:
        raise ValueError('SYNTHETIC_ARCHIVE_BUDGET')
    return data


def decode_s0(data, contract, live_plan, servo_frames, ra_frames):
    """Decode canonical bytes and revalidate full original LIVE inputs again."""
    try:
        wrapper = _decode_json(data, MAX_ARCHIVE_BYTES)
        _fields(wrapper, _WRAPPER)
        _constant(wrapper['schema'], 'SYNTHETIC_S0_ARCHIVE_V1')
        body = canonical_bytes(wrapper['body'])
        if _integer(wrapper['body_bytes'], 1) != len(body) or _digest(wrapper['body_sha256']) != sha256_bytes(body):
            raise ValueError('ARCHIVE_BODY_IDENTITY_MISMATCH')
        envelope = wrapper['body']
        result = validate_s0_envelope(contract, envelope, live_plan, servo_frames, ra_frames)
        if result['status'] != 'SYNTHETIC_S0_CONSISTENT':
            raise ValueError(result['reason'])
        return envelope
    except (KeyError, TypeError, OverflowError, RecursionError):
        raise ValueError('INVALID_SYNTHETIC_ARCHIVE') from None
