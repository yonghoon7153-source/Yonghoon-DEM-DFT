#!/usr/bin/env python3
"""Check inactive LHS12 document rules against invented boundary cases only.

This is not a production classifier, data reader, approval, or scientific test.
Reads definition.json and synthetic_boundary_cases.json; its own source bytes
are read only for identity hashing. No project imports, subprocesses, network,
original logs, ZIPs, or historical scripts.
Historical ambiguity is modeled from quoted document conditions, not executed
against any existing product classifier. Use --write-result for the fixed local
static_check_results.json output; otherwise print the same JSON to stdout.
"""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
DEFINITION = HERE.parent / 'lhs_n_preaccess_definition_draft_20261106' / 'definition.json'
CASES = HERE / 'synthetic_boundary_cases.json'
RESULT = HERE / 'static_check_results.json'
AXES = ['prior_overlap', 'dependent_lineage', 'relevant_outcome_exposure']


def need(condition, message):
    if not condition:
        raise ValueError(message)


def strict_pairs(pairs):
    value = {}
    for key, item in pairs:
        need(key not in value, 'duplicate JSON key')
        value[key] = item
    return value


def reject_constant(_):
    raise ValueError('nonfinite JSON constant')


def load(path):
    raw = path.read_bytes()
    return json.loads(raw.decode('utf-8'), object_pairs_hook=strict_pairs,
                      parse_constant=reject_constant), hashlib.sha256(raw).hexdigest()


def validate_policy(document, cases):
    expected_boundary = {
        'status': 'DRAFT_NOT_REGISTERED', 'author_ratification': 'PENDING',
        'external_review': 'PARTIAL_ACCEPTED_CLARIFICATION_RECHECK_PENDING',
        'whole_gate': 'HOLD', 'measured_rows': 0, 'rows': [], 'cohort_members': [],
        'frozen_pairs': [], 'execution_authorized': False,
        'value_access_authorized': False, 'active_registration_changed': False,
        'new_reader_provided': False,
    }
    for key, expected in expected_boundary.items():
        need(document.get(key) == expected, 'inactive boundary changed: ' + key)
    need(document['actual_template']['status'] == 'NOT_COLLECTED', 'actual template status changed')
    need(document['actual_template']['cohort_evidence_flags'] == dict.fromkeys(AXES),
         'actual cohort facts must stay uncollected')
    for key, value in document['actual_template'].items():
        if key not in ('status', 'cohort_evidence_flags'):
            need(value is None, 'actual template populated: ' + key)
    need(cases['all_cases_are_invented'] is True and cases['research_observations'] == 0
         and cases['actual_case_ids_used'] is False, 'synthetic scope required')
    cohort = document['cohort_rule']
    need(cohort['status'] == 'INACTIVE_RECOMMENDATION_REQUIRES_Q1_RATIFICATION', 'Q1 inactive')
    need(cohort['axes'] == AXES, 'cohort axes changed')
    need(cohort['axis_values'] == {
        'true': 'confirmed affirmative fact',
        'false': 'documented verified negative; not absence of a record',
        'null': 'unknown; never coerce to false'}, 'tri-state meanings changed')
    need(cohort['exclusive_priority'] == [
        {'when': 'any_axis_true', 'primary_cohort': 'EXPOSED_CONTEXT'},
        {'when': 'no_axis_true_and_any_axis_unknown', 'primary_cohort': 'UNRESOLVED_CONTEXT'},
        {'when': 'all_axes_verified_false', 'primary_cohort': 'PROSPECTIVE_CANDIDATE'}],
        'cohort exclusive priority changed')
    for key in ('preserve_all_axis_evidence', 'preserve_unknown_axes_even_if_exposed',
                'primary_cohort_counts_disjoint', 'secondary_flag_counts_are_not_primary_cohort_counts'):
        need(cohort[key] is True, 'cohort preservation changed: ' + key)
    need(cohort['prospective_is_independence_certification'] is False, 'prospective is not certification')
    direction = document['aggregate_direction_rule']
    need(direction['status'] == 'INACTIVE_RECOMMENDATION_REQUIRES_Q2_RATIFICATION', 'Q2 inactive')
    expected_strings = {
        'scope': 'predeclared same cohort, stratum and contrast type; not all candidates pooled',
        'evaluated_set': 'E: evaluable prespecified fixed pairs with finite established contrasts',
        'zero_N_set': 'Z: pairs in E with delta_N == 0',
        'direction_set': 'D: pairs in E with delta_N != 0',
        'partition': 'E is disjoint union of Z and D',
    }
    for key, expected in expected_strings.items():
        need(direction[key] == expected, 'direction scope changed: ' + key)
    need(direction['empty_direction_set'] == {
        'arithmetic_direction': 'NOT_IDENTIFIABLE',
        'reason_if_E_empty': 'NO_EVALUABLE_PAIRS',
        'evaluation_status_if_E_empty': 'NOT_ESTABLISHED',
        'reason_if_E_nonempty': 'NO_NONZERO_N_CONTRAST'}, 'empty direction policy changed')
    need(direction['nonempty_direction_cases'] == [
        {'when': 'all_products_negative', 'arithmetic_direction': 'DIRECTION_CONSISTENT'},
        {'when': 'all_products_positive', 'arithmetic_direction': 'DIRECTION_OPPOSITE'},
        {'when': 'otherwise_including_delta_P_zero', 'arithmetic_direction': 'DIRECTION_MIXED_OR_TIED'}],
        'nonempty direction branches changed')
    for key in ('empty_set_checked_before_all', 'preserve_all_evaluated_rows',
                'independent_N_effect_status_separate', 'sign_resolution_separate'):
        need(direction[key] is True, 'direction preservation changed: ' + key)
    for key in ('zero_N_is_aggregate_tie', 'post_outcome_rematching'):
        need(direction[key] is False, 'direction exclusion rule changed: ' + key)
    need(direction['report_counts_and_ids'] == ['planned', 'evaluable', 'unevaluable', 'zero_N', 'direction'],
         'denominator IDs required')
    need(direction['count_identities'] == ['planned = evaluable + unevaluable', 'evaluable = zero_N + direction'],
         'denominator identities changed')
    need(document['pairing']['post_outcome_rematching'] is False
         and document['pairing']['observed_outcome_matching'] is False, 'pairing restrictions changed')


def document_direction(rule, pairs):
    """Interpret only the checked document predicates on invented integer contrasts."""
    original = copy.deepcopy(pairs)
    need(len({p['pair_id'] for p in pairs}) == len(pairs), 'duplicate synthetic pair ID')
    for pair in pairs:
        need(pair['pair_id'].startswith('SYN-'), 'only synthetic pair IDs accepted')
        need(type(pair['evaluable']) is bool, 'evaluable must be boolean')
        if pair['evaluable']:
            need(type(pair['delta_N']) is int and type(pair['delta_P']) is int,
                 'only invented finite integer contrasts accepted')
        else:
            need(pair['delta_N'] is None and pair['delta_P'] is None and pair.get('reason'),
                 'unevaluable synthetic row must retain nulls and reason')
    evaluated = [p for p in pairs if p['evaluable']]
    zero = [p for p in evaluated if p['delta_N'] == 0]
    direction = [p for p in evaluated if p['delta_N'] != 0]
    # Empty D is handled before all(); never authorize vacuous positive/negative tags.
    if not direction:
        candidates = [rule['empty_direction_set']['arithmetic_direction']]
        reason_key = 'reason_if_E_empty' if not evaluated else 'reason_if_E_nonempty'
        reason = rule['empty_direction_set'][reason_key]
        evaluation_status = rule['empty_direction_set']['evaluation_status_if_E_empty'] if not evaluated else None
    else:
        products = [p['delta_N'] * p['delta_P'] for p in direction]
        negative = all(v < 0 for v in products)
        positive = all(v > 0 for v in products)
        predicates = {'all_products_negative': negative, 'all_products_positive': positive,
                      'otherwise_including_delta_P_zero': not negative and not positive}
        candidates = [b['arithmetic_direction'] for b in rule['nonempty_direction_cases'] if predicates[b['when']]]
        reason, evaluation_status = None, None
    need(len(candidates) == 1, 'direction classification not exclusive')
    ids = {
        'planned': [p['pair_id'] for p in pairs],
        'evaluable': [p['pair_id'] for p in evaluated],
        'unevaluable': [p['pair_id'] for p in pairs if not p['evaluable']],
        'zero_N': [p['pair_id'] for p in zero],
        'direction': [p['pair_id'] for p in direction],
    }
    counts = {key: len(value) for key, value in ids.items()}
    need(counts['planned'] == counts['evaluable'] + counts['unevaluable'], 'planned denominator lost')
    need(counts['evaluable'] == counts['zero_N'] + counts['direction'], 'evaluated denominator lost')
    need(not set(ids['zero_N']) & set(ids['direction']), 'Z and D overlap')
    need(set(ids['evaluable']) == set(ids['zero_N']) | set(ids['direction']), 'Z and D do not partition E')
    need(set(ids['planned']) == set(ids['evaluable']) | set(ids['unevaluable']), 'planned IDs lost')
    need(pairs == original, 'input rows changed or rematched')
    return {'arithmetic_direction': candidates[0], 'reason': reason,
            'evaluation_status': evaluation_status, 'counts': counts, 'ids': ids,
            'preserved_rows': copy.deepcopy(pairs), 'exclusive_status_count': len(candidates)}


def document_cohort(rule, axes):
    original = copy.deepcopy(axes)
    need(set(axes) == set(AXES), 'wrong synthetic cohort axes')
    need(all(type(value) is bool or value is None for value in axes.values()), 'tri-state axes required')
    positive = any(value is True for value in axes.values())
    unknown = any(value is None for value in axes.values())
    predicates = {'any_axis_true': positive,
                  'no_axis_true_and_any_axis_unknown': not positive and unknown,
                  'all_axes_verified_false': all(value is False for value in axes.values())}
    candidates = [b['primary_cohort'] for b in rule['exclusive_priority'] if predicates[b['when']]]
    need(len(candidates) == 1, 'cohort classification not exclusive')
    need(axes == original, 'cohort evidence changed')
    return {'primary_cohort': candidates[0], 'preserved_axes': copy.deepcopy(axes),
            'unknown_axes': [key for key in AXES if axes[key] is None],
            'confirmed_axes': [key for key in AXES if axes[key] is True],
            'exclusive_status_count': len(candidates)}


def check(document, cases):
    validate_policy(document, cases)
    direction_rule, cohort_rule = document['aggregate_direction_rule'], document['cohort_rule']
    named_direction = []
    direction_lookup = {}
    for case in cases['direction_cases']:
        need(case['case_id'] not in direction_lookup, 'duplicate direction case ID')
        direction_lookup[case['case_id']] = case
        actual = document_direction(direction_rule, case['pairs'])
        need(all(actual[key] == expected for key, expected in case['expected'].items()),
             'named direction expectation failed: ' + case['case_id'])
        named_direction.append({'case_id': case['case_id'], 'status': 'PASS', **actual})
    named_cohort, cohort_lookup = [], {}
    for case in cases['cohort_cases']:
        need(case['case_id'] not in cohort_lookup, 'duplicate cohort case ID')
        cohort_lookup[case['case_id']] = case
        actual = document_cohort(cohort_rule, case['axes'])
        need(actual['primary_cohort'] == case['expected'], 'named cohort expectation failed: ' + case['case_id'])
        named_cohort.append({'case_id': case['case_id'], 'status': 'PASS', **actual})
    history = cases['historical_overlap_models']
    need(history['interpretation_only'] is True and history['not_an_existing_classifier_execution'] is True,
         'historical model scope changed')
    old_direction = direction_lookup[history['direction']['case_id']]['pairs']
    old_e = [p for p in old_direction if p['evaluable']]
    old_d = [p for p in old_e if p['delta_N'] != 0]
    need(old_d, 'historical primary counterexample must not depend on empty all')
    old_direction_matches = []
    if all(p['delta_N'] * p['delta_P'] < 0 for p in old_d):
        old_direction_matches.append('DIRECTION_CONSISTENT')
    if any(p['delta_N'] * p['delta_P'] == 0 for p in old_e):
        old_direction_matches.append('DIRECTION_MIXED_OR_TIED')
    need(old_direction_matches == history['direction']['expected_simultaneously_true'], 'old direction overlap not reproduced')
    old_axes = cohort_lookup[history['cohort']['case_id']]['axes']
    old_cohort_matches = []
    if any(value is True for value in old_axes.values()):
        old_cohort_matches.append('EXPOSED_CONTEXT')
    if any(value is None for value in old_axes.values()):
        old_cohort_matches.append('UNRESOLVED_CONTEXT')
    need(old_cohort_matches == history['cohort']['expected_simultaneously_true'], 'old cohort overlap not reproduced')
    enum = cases['enumeration']
    need(enum['cohort_axis_states'] == [True, False, None] and enum['cohort_axis_count'] == 3,
         'cohort enumeration changed')
    need(enum['delta_N_domain'] == [-1, 0, 1] and enum['delta_P_domain'] == [-1, 0, 1]
         and enum['ordered_pair_counts'] == [0, 1, 2], 'direction enumeration changed')
    cohort_table, cohort_totals = [], {}
    for values in itertools.product(enum['cohort_axis_states'], repeat=len(AXES)):
        actual = document_cohort(cohort_rule, dict(zip(AXES, values)))
        cohort_table.append(actual)
        label = actual['primary_cohort']
        cohort_totals[label] = cohort_totals.get(label, 0) + 1
    need(len(cohort_table) == enum['expected_cohort_combinations'] == 27, 'cohort enumeration incomplete')
    need(cohort_totals == {'EXPOSED_CONTEXT': 19, 'UNRESOLVED_CONTEXT': 7, 'PROSPECTIVE_CANDIDATE': 1},
         'cohort partition totals changed')
    domain = list(itertools.product(enum['delta_N_domain'], enum['delta_P_domain']))
    direction_total, direction_totals = 0, {}
    for size in enum['ordered_pair_counts']:
        for contrast in itertools.product(domain, repeat=size):
            pairs = [{'pair_id': 'SYN-ENUM-' + str(index), 'evaluable': True,
                      'delta_N': dn, 'delta_P': dp} for index, (dn, dp) in enumerate(contrast)]
            actual = document_direction(direction_rule, pairs)
            # A second sign-set characterization checks the predicate interpretation.
            products = {dn * dp for dn, dp in contrast if dn != 0}
            expected = ('NOT_IDENTIFIABLE' if not products else
                        'DIRECTION_CONSISTENT' if products == {-1} else
                        'DIRECTION_OPPOSITE' if products == {1} else 'DIRECTION_MIXED_OR_TIED')
            need(actual['arithmetic_direction'] == expected, 'enumerated direction differs from sign-set characterization')
            direction_total += 1
            direction_totals[expected] = direction_totals.get(expected, 0) + 1
    need(direction_total == enum['expected_direction_combinations'] == 91, 'direction enumeration incomplete')
    need(direction_totals == {'NOT_IDENTIFIABLE': 13, 'DIRECTION_CONSISTENT': 18,
                             'DIRECTION_OPPOSITE': 18, 'DIRECTION_MIXED_OR_TIED': 42},
         'direction partition totals changed')
    return {
        'inactive_policy_and_empty_actual_records': 'PASS',
        'historical_overlap_models': {
            'LHS12-01': {'status': 'REPRODUCED_DOCUMENT_INTERPRETATION_OVERLAP', 'simultaneously_true': old_direction_matches,
                         'revised_status': document_direction(direction_rule, old_direction)['arithmetic_direction']},
            'LHS12-02': {'status': 'REPRODUCED_DOCUMENT_INTERPRETATION_OVERLAP', 'simultaneously_true': old_cohort_matches,
                         'revised_status': document_cohort(cohort_rule, old_axes)['primary_cohort']},
            'no_product_classifier_failure_claimed': True,
        },
        'named_direction_cases': named_direction, 'named_cohort_cases': named_cohort,
        'cohort_enumeration': {'cases': len(cohort_table), 'primary_counts': cohort_totals,
                               'all_exclusive': True, 'all_evidence_preserved': True, 'truth_table': cohort_table},
        'direction_enumeration': {'cases': direction_total, 'ordered_pair_counts': [0, 1, 2],
                                  'contrast_domain': [-1, 0, 1], 'status_counts': direction_totals,
                                  'all_exclusive': True, 'all_denominators_and_rows_preserved': True,
                                  'sign_set_cross_check': 'PASS'},
        'counts_are_synthetic_checks_not_research_observations': True,
        'scientific_or_execution_qualification_established': False,
    }


def main():
    need(sys.argv[1:] in ([], ['--write-result']), 'supported option: --write-result only')
    result = {'schema': 'lhs12_document_static_check/v1', 'scope': 'INACTIVE_DOCUMENT_RULES_ONLY',
              'project_modules_imported': False, 'scientific_data_read': False,
              'research_observations': 0, 'policy_activation': False, 'author_ratification': 'PENDING',
              'external_recheck_completed_by_this_script': False, 'external_closure_claimed': False,
              'execution_authorized': False, 'value_access_authorized': False, 'whole_gate': 'HOLD'}
    try:
        document, document_sha = load(DEFINITION)
        cases, cases_sha = load(CASES)
        result['input_sha256'] = {
            'docs/reviews/lhs_n_preaccess_definition_draft_20261106/definition.json': document_sha,
            'docs/reviews/lhs12_clarification_recheck_20261108/synthetic_boundary_cases.json': cases_sha,
            'docs/reviews/lhs12_clarification_recheck_20261108/check_static_cases.py': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        }
        result['checks'] = check(document, cases)
        result['status'] = 'PASS'
    except (KeyError, TypeError, ValueError) as exc:
        result['status'] = 'FAIL'
        result['failure'] = str(exc)
    except OSError:
        result['status'] = 'FAIL'
        result['failure'] = 'allowed document input or checker identity could not be read'
    rendered = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    if sys.argv[1:] == ['--write-result']:
        RESULT.write_text(rendered, encoding='utf-8', newline='\n')
        print(json.dumps({'status': result['status'], 'output': 'static_check_results.json',
                          'research_observations': 0, 'whole_gate': 'HOLD'}))
    else:
        print(rendered, end='')
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
