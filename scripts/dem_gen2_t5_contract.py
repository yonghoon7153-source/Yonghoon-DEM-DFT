"""Pure-data synthetic T5 declarations and planned-denominator bookkeeping.

권고안 전제(Q-T5-01..05): no physical estimator or CI generator is implemented.
Caller-supplied plan consistency is checked; external preregistration is not.
"""
from fractions import Fraction
import math


_PLAN_KEYS = frozenset(('schema', 'purpose', 'identity', 'quantity', 'output_unit',
    'cases', 'estimands', 'sample_sizes', 'seeds', 'dependence',
    'interval_definition', 'error_policy', 'family', 'missing_policy', 'retry_policy'))
_IDENTITY_KEYS = frozenset(('plan_id', 'revision', 'producer_pin', 'operator_pin',
    'oracle_pin', 'interval_method_pin', 'frame_id', 'inventory_id', 'unit_system_id'))
_ROW_KEYS = frozenset(('identity', 'case_id', 'estimand_id', 'n', 'repetition_id',
    'seed', 'oracle_id', 'output_unit', 'status', 'value', 'interval', 'failure_code'))
_KINDS = frozenset(('two_separate', 'two_tangent', 'two_overlap',
                    'three_coincident', 'wall_half'))
_PAIRS = frozenset((op, region) for op in ('sphere', 'union')
                   for region in ('full', 'interior'))
_MAX_TRIALS = 16384


def _dict(value, keys):
    # Check key types before set construction, hashing, equality, or lookup.
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise ValueError('exact built-in mapping and string keys required')
    if set(value) != keys:
        raise ValueError('unexpected mapping keys')
    return value


def _list(value, minimum, maximum):
    if type(value) is not list or not minimum <= len(value) <= maximum:
        raise ValueError('bounded exact built-in list required')
    return value


def _int(value, minimum=0, maximum=1000000000):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError('bounded exact built-in integer required')
    return value


def _number(value, nonnegative=False):
    if type(value) not in (int, float):
        raise ValueError('built-in finite number required')
    result = float(value)
    if not math.isfinite(result) or (nonnegative and result < 0):
        raise ValueError('invalid finite number')
    return result


def _token(value):
    if type(value) is not str or not 1 <= len(value) <= 128:
        raise ValueError('bounded token required')
    if not value.isascii() or not value[0].isalpha():
        raise ValueError('ASCII token required')
    if any(not (c.isalnum() or c in '_-') for c in value):
        raise ValueError('invalid token')
    return value


def _one(value, allowed):
    if type(value) is not str or value not in allowed:
        raise ValueError('unsupported declaration')
    return value


def _ratio(value, strict=False):
    _list(value, 2, 2)
    numerator, denominator = (_int(x, 1) for x in value)
    if numerator > denominator or (strict and numerator == denominator):
        raise ValueError('invalid probability ratio')
    return Fraction(numerator, denominator)


def _identity(value):
    _dict(value, _IDENTITY_KEYS)
    for key, item in value.items():
        if key == 'revision':
            _int(item, 1)
        elif key.endswith('_pin'):
            if (type(item) is not str or len(item) != 40
                    or any(c not in '0123456789abcdef' for c in item)):
                raise ValueError('full lowercase Git pin required')
        else:
            _token(item)
    return dict(value)


def _report(status, reason, normalized=None, cells=None, missing_keys=None):
    return dict(status=status, reason=reason, physical_ready=False,
        execution_go=False, gate_write=False, qualification='NOT_RUN',
        registration_status='DRAFT_UNREGISTERED', research_results=0,
        interval_generation_qualification='NOT_QUALIFIED',
        true_coverage_inference='NOT_QUALIFIED', pbc_qualification='NOT_QUALIFIED',
        external_preregistration_verification='NOT_PERFORMED',
        validation_scope='CALLER_SUPPLIED_PLAN_INTERNAL_CONSISTENCY_ONLY',
        pbc_requirement=normalized['pbc_requirement'] if normalized else 'UNKNOWN',
        planned_cells=len(normalized['cells']) if normalized else 0,
        planned_trials=normalized['planned_trials'] if normalized else 0,
        cells=cells if cells is not None else [],
        missing_keys=missing_keys if missing_keys is not None else [],
        assumptions=['Q-T5-01', 'Q-T5-02', 'Q-T5-03', 'Q-T5-04', 'Q-T5-05'])


def _plan(plan):
    _dict(plan, _PLAN_KEYS)
    _one(plan['schema'], ('DEM_GEN2_T5_SYNTHETIC_CONTRACT_V1',))
    _one(plan['purpose'], ('SYNTHETIC_PREPARATION',))
    identity = _identity(plan['identity'])
    quantity = _one(plan['quantity'], ('VOLUME', 'POROSITY'))
    unit = 'SYNTHETIC_LENGTH_CUBED' if quantity == 'VOLUME' else 'FRACTION'
    _one(plan['output_unit'], (unit,))
    estimands = {}
    pairs, regions = set(), {}
    pbc_required = False
    for item in _list(plan['estimands'], 4, 4):
        _dict(item, {'id', 'operator', 'region', 'roi_id', 'denominator_id',
                     'clipping_id', 'pbc_policy'})
        name = _token(item['id'])
        op = _one(item['operator'], ('sphere', 'union'))
        region = _one(item['region'], ('full', 'interior'))
        for key in ('roi_id', 'denominator_id', 'clipping_id'):
            _token(item[key])
        pbc = _one(item['pbc_policy'], ('NONE', 'XY_PERIODIC'))
        definition = tuple(item[k] for k in ('roi_id', 'denominator_id',
                                            'clipping_id', 'pbc_policy'))
        if name in estimands or (op, region) in pairs:
            raise ValueError('duplicate estimand')
        if region in regions and regions[region] != definition:
            raise ValueError('operator region declarations disagree')
        regions[region] = definition
        estimands[name] = dict(item)
        pairs.add((op, region))
        pbc_required = pbc_required or pbc == 'XY_PERIODIC'
    if pairs != _PAIRS:
        raise ValueError('incomplete estimand set')
    cases, kinds = {}, set()
    for item in _list(plan['cases'], 5, 16):
        _dict(item, {'id', 'fixture_kind', 'oracle_id', 'oracles'})
        name = _token(item['id'])
        kind = _one(item['fixture_kind'], _KINDS)
        oracle_id = _token(item['oracle_id'])
        _dict(item['oracles'], set(estimands))
        oracles = {key: _number(value, quantity == 'VOLUME')
                   for key, value in item['oracles'].items()}
        if name in cases:
            raise ValueError('duplicate case')
        cases[name] = dict(oracle_id=oracle_id, oracles=oracles)
        kinds.add(kind)
    if kinds != _KINDS:
        raise ValueError('required analytic case declaration missing')
    sizes = [_int(n, 2) for n in _list(plan['sample_sizes'], 1, 16)]
    if any(a >= b for a, b in zip(sizes, sizes[1:])):
        raise ValueError('sample ladder must increase strictly')
    seeds, seed_values, groups = {}, set(), set()
    for item in _list(plan['seeds'], 2, 128):
        _dict(item, {'repetition_id', 'seed', 'dependence_group'})
        repetition = _token(item['repetition_id'])
        seed = _int(item['seed'], 1)
        group = _token(item['dependence_group'])
        if repetition in seeds or seed in seed_values or group in groups:
            raise ValueError('repetition, seed, and group must be unique')
        seeds[repetition] = seed
        seed_values.add(seed)
        groups.add(group)
    _one(plan['dependence'], ('INDEPENDENT_WITHIN_CELL_SHARED_ACROSS_CELLS',))
    interval = _dict(plan['interval_definition'], {'method_id', 'nominal_level',
        'coverage_target', 'evaluation', 'uncertainty'})
    _token(interval['method_id'])
    _ratio(interval['nominal_level'], strict=True)
    coverage_target = _ratio(interval['coverage_target'])
    _one(interval['evaluation'], ('PLANNED_DENOMINATOR_ONLY',))
    _one(interval['uncertainty'], ('NOT_QUALIFIED',))
    error = _dict(plan['error_policy'], {'mode', 'budget'})
    mode = _one(error['mode'], ('ABS', 'REL'))
    budget = _number(error['budget'], nonnegative=True)
    if mode == 'REL' and any(value == 0 for c in cases.values()
                             for value in c['oracles'].values()):
        raise ValueError('relative budget is undefined for zero oracle')
    cells = [(case, estimand, n) for case in cases for estimand in estimands for n in sizes]
    expected_cells = set(cells)
    planned_trials = len(cells) * len(seeds)
    if planned_trials > _MAX_TRIALS:
        raise ValueError('synthetic contract capacity exceeded')
    family = _dict(plan['family'], {'alpha_family', 'cells'})
    family_alpha = _ratio(family['alpha_family'])
    family_keys, alpha_total = set(), Fraction(0)
    for item in _list(family['cells'], 1, _MAX_TRIALS):
        _dict(item, {'case_id', 'estimand_id', 'n', 'alpha'})
        key = (_token(item['case_id']), _token(item['estimand_id']), _int(item['n'], 2))
        if key in family_keys:
            raise ValueError('duplicate family cell')
        family_keys.add(key)
        alpha_total += _ratio(item['alpha'])
    if family_keys != expected_cells or alpha_total > family_alpha:
        raise ValueError('family manifest or alpha budget mismatch')
    _one(plan['missing_policy'], ('COUNT_IN_PLANNED_AND_HOLD',))
    _one(plan['retry_policy'], ('NONE',))
    return dict(identity=identity, quantity=quantity, output_unit=unit,
        cases=cases, seeds=seeds, cells=cells, expected_cells=expected_cells,
        planned_trials=planned_trials, coverage_target=coverage_target,
        error_mode=mode, error_budget=budget,
        pbc_requirement='REQUIRED_UNQUALIFIED' if pbc_required else 'NONE_DECLARED')


def validate_t5_plan(plan):
    """Validate declarations only; does not authenticate an external frozen plan."""
    try:
        normalized = _plan(plan)
    except (TypeError, ValueError, OverflowError):
        return _report('REJECTED', 'INVALID_SYNTHETIC_PLAN')
    return _report('SYNTHETIC_PLAN_VALID', 'DECLARATIONS_ONLY', normalized)


def audit_t5_coverage(plan, rows):
    """Count supplied intervals against declared oracles without generating CIs."""
    try:
        normalized = _plan(plan)
        received = {}
        for row in _list(rows, 0, _MAX_TRIALS):
            _dict(row, _ROW_KEYS)
            row_identity = _identity(row['identity'])
            if row_identity != normalized['identity']:
                raise ValueError('row identity mismatch')
            case, estimand = _token(row['case_id']), _token(row['estimand_id'])
            n, repetition = _int(row['n'], 2), _token(row['repetition_id'])
            seed, oracle_id = _int(row['seed'], 1), _token(row['oracle_id'])
            cell, key = (case, estimand, n), (case, estimand, n, repetition)
            if cell not in normalized['expected_cells'] or repetition not in normalized['seeds']:
                raise ValueError('row outside planned manifest')
            if (seed != normalized['seeds'][repetition]
                    or oracle_id != normalized['cases'][case]['oracle_id']):
                raise ValueError('row seed or oracle identity mismatch')
            _one(row['output_unit'], (normalized['output_unit'],))
            if key in received:
                raise ValueError('duplicate trial')
            status = _one(row['status'], ('VALID', 'FAILED', 'MISSING'))
            if status == 'VALID':
                value = _number(row['value'], normalized['quantity'] == 'VOLUME')
                endpoints = _list(row['interval'], 2, 2)
                lower, upper = (_number(x) for x in endpoints)
                if lower > upper or row['failure_code'] is not None:
                    raise ValueError('invalid valid-record payload')
                received[key] = (status, value, lower, upper)
            else:
                _token(row['failure_code'])
                if row['value'] is not None or row['interval'] is not None:
                    raise ValueError('failed or missing record contains values')
                received[key] = (status, None, None, None)
        cells, missing_keys = [], []
        for case, estimand, n in normalized['cells']:
            truth = normalized['cases'][case]['oracles'][estimand]
            valid = covered = missing = failed = 0
            deviations = []
            for repetition in normalized['seeds']:
                key = (case, estimand, n, repetition)
                record = received.get(key)
                if record is None or record[0] == 'MISSING':
                    missing += 1
                    missing_keys.append(list(key))
                elif record[0] == 'FAILED':
                    failed += 1
                else:
                    valid += 1
                    covered += record[2] <= truth <= record[3]
                    deviations.append(_number(record[1] - truth))
            planned = len(normalized['seeds'])
            mean_bias = _number(math.fsum(deviations) / valid) if valid else None
            max_abs = max(abs(d) for d in deviations) if valid else None
            rmse = _number(math.hypot(*deviations) / math.sqrt(valid)) if valid else None
            budget = normalized['error_budget']
            if normalized['error_mode'] == 'REL':
                budget = _number(budget * abs(truth), nonnegative=True)
            cells.append(dict(case_id=case, estimand_id=estimand, n=n,
                oracle=truth, output_unit=normalized['output_unit'], planned=planned,
                valid=valid, missing=missing, failed=failed, covered=covered,
                conservative_coverage=covered / planned,
                eligible_coverage_diagnostic=covered / valid if valid else None,
                mean_bias=mean_bias, max_abs_error=max_abs, rmse=rmse,
                declared_toy_coverage_target_met=Fraction(covered, planned) >= normalized['coverage_target'],
                declared_toy_bias_budget_met=abs(mean_bias) <= budget if valid else None))
        incomplete = any(c['missing'] or c['failed'] for c in cells)
    except (TypeError, ValueError, OverflowError):
        return _report('REJECTED', 'INVALID_SYNTHETIC_PLAN_OR_ROWS')
    return _report('INCOMPLETE' if incomplete else 'SYNTHETIC_BOOKKEEPING_COMPLETE',
                   'PLANNED_DENOMINATOR_ONLY', normalized, cells, missing_keys)
