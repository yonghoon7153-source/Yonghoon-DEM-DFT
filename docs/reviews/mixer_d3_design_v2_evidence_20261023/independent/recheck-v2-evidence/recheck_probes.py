#!/usr/bin/env python3
"""Small independent semantic probes for D3 revision 1 (not production tests)."""
import itertools
import json

C, I, U = 'compatible', 'incompatible', 'unassessed'


def candidate(row):
    if not row:
        raise ValueError('A required validation-item list must not be empty')
    if U in row:
        return U
    return C if all(x == C for x in row) else I


def aggregate(table):
    if not table:
        return 'not-applicable'
    states = [candidate(row) for row in table]
    if U in states:
        return 'incomplete'
    if all(x == C for x in states):
        return 'all-compatible'
    if all(x == I for x in states):
        return 'none-compatible'
    return 'mixed'


def main():
    checks = []

    def record(name, passed, detail):
        checks.append({'name': name, 'pass': bool(passed), 'detail': detail})

    # I01: finite-grid absence is still compatible with an unsampled exact solution.
    f = lambda b: (b - 1.5)**2
    supported = [b for b in (1, 2) if abs(f(b)) <= .01]
    record('I01_empty_grid_scope', not supported and f(1.5) == 0,
           {'finite_supported': supported, 'unsampled_exact_solution': 1.5})

    # I02: exhaustive two-candidate/two-required-item status tables.
    counts = {k: 0 for k in ('all-compatible', 'mixed', 'none-compatible', 'incomplete')}
    false_success = []
    for cells in itertools.product((C, I, U), repeat=4):
        table = (cells[:2], cells[2:])
        state = aggregate(table)
        counts[state] += 1
        if (state == 'all-compatible') != all(x == C for x in cells):
            false_success.append({'table': table, 'state': state})
    record('I02_exhaustive_status_tables', not false_success and sum(counts.values()) == 81,
           {'tables': sum(counts.values()), 'aggregate_counts': counts, 'false_success': false_success})
    record('I02_partial_failure', aggregate(((C, C), (I, C))) == 'mixed',
           {'table': ((C, C), (I, C)), 'aggregate': aggregate(((C, C), (I, C)))})
    incomplete = ((I, U), (C, C))
    record('I02_known_failure_preserved_under_incomplete', aggregate(incomplete) == 'incomplete'
           and incomplete[0][0] == I,
           {'table_retained': incomplete, 'aggregate': aggregate(incomplete)})
    record('I02_empty_S_not_success', aggregate(()) == 'not-applicable',
           {'S': [], 'aggregate': aggregate(())})

    # I03: order is per access unit. A common key cannot provide the stated order.
    c1_seal, cal_release, c2_seal, val_release = 10, 11, 20, 21
    record('I03_per_unit_release', cal_release > c1_seal and val_release > c2_seal
           and not cal_release > c2_seal,
           {'C1_seal': c1_seal, 'calibration_release': cal_release, 'C2_seal': c2_seal,
            'validation_release': val_release, 'common_release_at_11_would_violate_validation_order': True,
            'times_are_synthetic_order_indices': True})

    # I04: abstract IDs test the rule; no source authentication of actual seed numbers.
    reserved = {'reserved_a', 'reserved_b', 'reserved_c'}
    dev = {'dev_a'}
    calibration = {'cal_a'}
    validation = {'val_a'}
    record('I04_reserved_intersection', not ((dev | calibration | validation) & reserved)
           and bool((dev | calibration | validation | {'reserved_b'}) & reserved),
           {'clean_intersection': sorted((dev | calibration | validation) & reserved),
            'reused_intersection': sorted((dev | calibration | validation | {'reserved_b'}) & reserved),
            'actual_reserved_numeric_ID_provenance': 'not_checked_in_this_input_scope'})

    result = {'scope': 'Independent synthetic semantics; no production implementation, measurement, or execution approval',
              'checks': checks, 'summary': {'passed': sum(c['pass'] for c in checks), 'total': len(checks)}}
    print(json.dumps(result, indent=2))
    return 0 if all(c['pass'] for c in checks) else 1


if __name__ == '__main__':
    raise SystemExit(main())
