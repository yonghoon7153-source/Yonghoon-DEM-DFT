"""Worked-example checker only. Not a solver, runtime guard or receipt adopter."""
from pathlib import Path
import copy
import hashlib
import json

STATE_KEYS = {'step', 'time_tick', 'identity', 'mass_volume', 'position_velocity',
              'deformation_stress_plastic', 'rigid_state',
              'boundary_contact_history', 'rng', 'phase'}
PHYSICS = ['constitutive', 'boundary', 'contact', 'g2p']


def diagnose(r, omit=None):
    """Diagnose this finite synthetic schema, without changing any input."""
    errors = []

    def require(condition, reason):
        if not condition and reason != omit:
            errors.append(reason)

    # Integer/token examples deliberately do not accept physical arrays/floats.
    for name in ['parent_version', 'parent_seen', 'attempt', 'previous_attempt',
                 'max_attempts', 'target_step', 'target_tick', 'field_capacity',
                 'required_fields', 'reported_peak', 'budget', 'published']:
        if type(r.get(name)) is not int or r[name] < 0:
            return ['invalid_example_schema']
    for name in ['collision', 'grid_empty', 'trial_empty']:
        if type(r.get(name)) is not bool:
            return ['invalid_example_schema']
    for name in ['before', 'after']:
        s = r.get(name)
        if type(s) is not dict or set(s) != STATE_KEYS:
            return ['invalid_example_schema']
        if any(type(s[k]) is not int or s[k] < 0 for k in ['step', 'time_tick']):
            return ['invalid_example_schema']
        if any(type(s[k]) is not str or not s[k] for k in STATE_KEYS - {'step', 'time_tick'}):
            return ['invalid_example_schema']
    mem = r.get('live_bytes')
    if type(mem) is not dict or set(mem) != {'old', 'new', 'rollback'}:
        return ['invalid_example_schema']
    if any(type(v) is not int or v < 0 for v in mem.values()):
        return ['invalid_example_schema']
    if r.get('required_physics') != PHYSICS:
        return ['invalid_example_schema']
    done = r.get('completed_physics')
    if type(done) is not list or any(type(x) is not str for x in done):
        return ['invalid_example_schema']
    require(len(done) == len(set(done)) and set(done) <= set(PHYSICS), 'physics_record')
    require(r['target_step'] == r['before']['step'] + 1 and
            r['target_tick'] > r['before']['time_tick'], 'target')
    require(r['max_attempts'] >= 1 and 1 <= r['attempt'] <= r['max_attempts'], 'attempt_budget')
    action = r.get('action')
    if action not in {'DISCARD', 'TECH_FAIL', 'RETRY', 'COMMIT'}:
        return ['invalid_example_schema']
    # All memory groups in this toy record are distinct, simultaneously live.
    require(r['reported_peak'] == sum(mem.values()), 'peak_accounting')
    if action != 'TECH_FAIL':
        require(r['required_fields'] <= r['field_capacity'], 'capacity')
        require(sum(mem.values()) <= r['budget'], 'memory_budget')
    else:
        reasons = {'CAPACITY': r['required_fields'] > r['field_capacity'],
                   'MEMORY': sum(mem.values()) > r['budget'],
                   'RETRIES': r['attempt'] == r['max_attempts']}
        require(r.get('failure_reason') in reasons and reasons.get(r.get('failure_reason')) is True,
                'unsubstantiated_failure')
    if action in {'DISCARD', 'TECH_FAIL', 'RETRY'}:
        require(r['before'] == r['after'], 'rollback_state_changed')
        require(r['grid_empty'] and r['trial_empty'], 'trial_not_cleared')
        require(r['published'] == 0, 'premature_publication')
    if action == 'DISCARD':
        require(r['collision'], 'discard_reason')
    if action == 'RETRY':
        require(r['attempt'] == r['previous_attempt'] + 1, 'retry_order')
        require(not r['collision'], 'unresolved_collision')
    if action == 'COMMIT':
        require(not r['collision'], 'unresolved_collision')
        require(r['parent_seen'] == r['parent_version'], 'parent_changed')
        require(done == PHYSICS, 'physics_incomplete')
        require(r['after']['step'] == r['target_step'] and
                r['after']['time_tick'] == r['target_tick'], 'commit_time')
        require(all(r['after'][k] == r['before'][k] for k in ['identity', 'mass_volume']),
                'conserved_identity')
        require(r['published'] == 1, 'publication_count')
    return errors


def main():
    p = Path(__file__).with_name('transaction_examples.json')
    data = p.read_bytes()
    cases = json.loads(data)['cases']
    observations = []
    for item in cases:
        r = item['record']
        original = copy.deepcopy(r)
        errors = diagnose(r)
        assert (not errors) == item['expected_valid'], (r['id'], errors)
        if not item['expected_valid']:
            assert item['expected_reason'] in errors, (r['id'], errors)
        assert r == original
        observations.append(dict(id=r['id'], accepted=not errors, reasons=errors))

    # Erasing each state group must be observed, not merely clearing the grid.
    state_changes = []
    base = cases[0]['record']
    for k in sorted(STATE_KEYS):
        mutant = copy.deepcopy(base)
        mutant['after'][k] = (mutant['after'][k] + 1 if type(mutant['after'][k]) is int
                              else mutant['after'][k] + ':changed')
        assert 'rollback_state_changed' in diagnose(mutant), k
        state_changes.append(k)

    # These are explicit weakened reference-checker variants, not old solver code.
    guard_checks = []
    for item in cases[4:]:
        r = copy.deepcopy(item['record'])
        if r['id'] == 'TX08_PEAK_MAX_ONLY':
            # Isolate the stated accounting guard from independent budget failure.
            r['budget'] = 10
        reason = item['expected_reason']
        assert reason in diagnose(r)
        assert diagnose(r, omit=reason) == [], (r['id'], diagnose(r, omit=reason))
        guard_checks.append(dict(case=r['id'], removed_guard=reason, false_accept_detected=True))
    schema_count = 0
    for value in [True, 1.0, float('nan'), float('inf'), '2', None, -1]:
        r = copy.deepcopy(base); r['attempt'] = value
        assert diagnose(r) == ['invalid_example_schema']
        schema_count += 1
    output = dict(scope='Finite synthetic record examples; not production TX qualification',
        fixture_sha256=hashlib.sha256(data).hexdigest(),
        observations=observations, valid_records=4, invalid_records=8,
        rollback_field_observations=state_changes,
        weakened_guard_observations=guard_checks, schema_observations=schema_count,
        solver_executed=False, production_TX_tests_executed=False, overall='HOLD')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
