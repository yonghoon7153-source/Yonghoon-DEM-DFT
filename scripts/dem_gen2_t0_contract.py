"""Offline synthetic T0 packet consistency; no readers or operating authority.

권고안 전제(Q-T0-1): exact identity packet and three fixed control roles.
권고안 전제(Q-T0-2): declared unit arithmetic only; actual qualification unknown.
Labels and hashes are compared, never authenticated as real execution evidence.
The 20-particle declaration is a fixture plan, not a run of twenty particles.
"""
from dem_gen2_qualification import integer, number, target_force


_IDENTITY = frozenset(('build_alias', 'producer_pin', 'qualification_pin',
    'deck_sha256', 'fixture_sha256', 'unit_mapping_id', 'run_id', 'attempt_id',
    'mesh_id', 'reaction_component'))
_PLAN = frozenset(('schema', 'purpose', 'protocol', 'identity', 'fixture',
                  'first_sample_id', 'sample_stride'))
_FIXTURE = frozenset(('particle_count', 'compression_sign', 'pressure_mpa',
                     'area_deck_m2', 'declared_target_force_deck'))
_CASE = frozenset(('identity', 'kind', 'sample_id', 'raw_reaction', 'normalized_force'))
_ROLES = ('compression_positive', 'opposite_polarity_negative', 'zero_control')
_CLASSES = ('COMPRESSION_POSITIVE', 'OPPOSITE_SIGN_DETECTED', 'ZERO_NONDETERMINING')


def _exact_dict(value, keys):
    if type(value) is not dict or any(type(k) is not str for k in value) or set(value) != keys:
        raise ValueError('exact complete dictionary required')
    return value


def _token(value):
    if (type(value) is not str or not 1 <= len(value) <= 128
            or value[0] not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
            or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-' for c in value)):
        raise ValueError('bounded synthetic alias required')
    return value


def _digest(value, length):
    if type(value) is not str or len(value) != length or any(c not in '0123456789abcdef' for c in value):
        raise ValueError('fixed lowercase digest required')


def _identity(value):
    _exact_dict(value, _IDENTITY)
    for key in ('producer_pin', 'qualification_pin'):
        _digest(value[key], 40)
    for key in ('deck_sha256', 'fixture_sha256'):
        _digest(value[key], 64)
    for key in _IDENTITY - {'producer_pin', 'qualification_pin', 'deck_sha256', 'fixture_sha256'}:
        _token(value[key])
    return value


def _constant(value, expected):
    if type(value) is not str or value != expected:
        raise ValueError('supported synthetic declaration required')


def validate_t0_contract(plan, cases):
    """Validate an all-or-nothing synthetic declaration and its three controls.

No sign is inferred from data. The caller declares a synthetic sign; opposite
polarity is a required negative control, and zero is explicitly non-determining.
The target-force arithmetic is the existing producer mapping, not an observed
pressure or an assertion that a target pressure was reached. Equality is exact
for the declared built-in numeric representation, not a physical tolerance.
"""
    def report(status, reason, observations=None, target=None):
        observations = [] if observations is None else observations
        return dict(status=status, reason=reason, observations=observations,
                target_force_deck=target, checked_cases=len(observations), actual_T0='NOT_RUN',
                actual_build_identity=None, actual_compression_sign=None,
                binary_syntax='NOT_RUN', physical_ready=False, execution_go=False,
                gate_write=False, operational_seal_modified=False, research_results=0,
                assumptions=['Q-T0-1', 'Q-T0-2'], evidence_kind='SYNTHETIC_ONLY')

    try:
        _exact_dict(plan, _PLAN)
        _constant(plan['schema'], 'DEM_GEN2_T0_SYNTHETIC_CONTRACT_V1')
        _constant(plan['purpose'], 'SYNTHETIC_PREPARATION')
        _constant(plan['protocol'], 'P2')
        identity = _identity(plan['identity'])
        _constant(identity['unit_mapping_id'], 'GEN2_MPA_DECK_STRESS_0P001_V1')
        _constant(identity['mesh_id'], 'top_mesh')
        _constant(identity['reaction_component'], 'z')
        specification = _exact_dict(plan['fixture'], _FIXTURE)
        if type(specification['particle_count']) is not int or specification['particle_count'] != 20:
            raise ValueError('declared twenty-particle fixture required')
        sign = specification['compression_sign']
        if type(sign) is not int or sign not in (-1, 1):
            raise ValueError('exact declared polarity required')
        target = target_force(specification['pressure_mpa'], specification['area_deck_m2'])
        declared_target = number(specification['declared_target_force_deck'], positive=True)
        if declared_target != target:
            raise ValueError('declared target does not match fixed unit mapping')
        first = integer(plan['first_sample_id'], 1)
        stride = integer(plan['sample_stride'], 1)
    except (KeyError, ValueError, TypeError):
        return report('REJECTED', 'INVALID_SYNTHETIC_PLAN')

    observations = []
    try:
        if type(cases) is not list or len(cases) != 3:
            raise ValueError('exact three-control list required')
        for index, case in enumerate(cases):
            _exact_dict(case, _CASE)
            if _identity(case['identity']) != identity:
                raise ValueError('control identity differs from declared plan')
            _constant(case['kind'], _ROLES[index])
            sample = integer(case['sample_id'], 1)
            if sample != first + index * stride:
                raise ValueError('control sample does not match declared plan')
            raw = number(case['raw_reaction'])
            normalized = number(case['normalized_force'])
            if normalized != number(sign * raw):
                raise ValueError('normalization must use the same signed sample')
            if ((index == 0 and normalized <= 0) or (index == 1 and normalized >= 0)
                    or (index == 2 and normalized != 0)):
                raise ValueError('control role predicate failed')
            observations.append(dict(sample_id=sample, kind=_ROLES[index], raw_reaction=raw,
                                     normalized_force=normalized, classification=_CLASSES[index]))
    except (KeyError, ValueError, TypeError):
        return report('REJECTED', 'INVALID_SYNTHETIC_CONTROLS')
    return report('SYNTHETIC_T0_CONTRACT_CONSISTENT', 'DIAGNOSTIC_ONLY', observations, target)
