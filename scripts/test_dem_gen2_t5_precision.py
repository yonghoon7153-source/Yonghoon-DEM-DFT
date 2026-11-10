"""NSB-F01 expected-correct synthetic numeric boundary regressions.

No geometry estimator, physical values, host, or qualification is exercised.
The received two counterexamples are asserted as correct behavior, not expected
failures. Integer hand oracles below do not use the implementation's arithmetic.
"""
from copy import deepcopy
import json
import math
from pathlib import Path
import types
import unittest

_fixture_path = Path(__file__).with_name('test_dem_gen2_t5_contract.py')
_fixture_module = types.ModuleType('unchanged_t5_fixture')
_fixture_module.__file__ = str(_fixture_path)
exec(compile(_fixture_path.read_bytes(), str(_fixture_path), 'exec'),
     _fixture_module.__dict__)
t5 = _fixture_module.t5
N = 2 ** 53


def cell_fixture(truth, values, intervals=None, *, quantity='VOLUME',
                 budget=.1, mode='ABS'):
    plan, rows = _fixture_module.fixture(quantity)
    case = plan['cases'][0]
    estimand = plan['estimands'][0]['id']
    case['oracles'][estimand] = truth
    plan['error_policy'] = dict(mode=mode, budget=budget)
    for row in rows:
        if row['case_id'] == case['id'] and row['estimand_id'] == estimand:
            i = int(row['repetition_id'].split('_')[-1]) - 1
            row['value'] = values[i]
            row['interval'] = list(intervals[i] if intervals else
                                   (values[i], values[i]))
    return plan, rows


class T5PrecisionTests(unittest.TestCase):
    def complete_cell(self, plan, rows):
        report = t5.audit_t5_coverage(plan, rows)
        self.assertEqual(report['status'], 'SYNTHETIC_BOOKKEEPING_COMPLETE')
        for key in ('physical_ready', 'execution_go', 'gate_write'):
            self.assertIs(report[key], False)
        self.assertEqual(report['qualification'], 'NOT_RUN')
        self.assertEqual(report['registration_status'], 'DRAFT_UNREGISTERED')
        self.assertEqual(report['research_results'], 0)
        return report['cells'][0]

    def test_01_received_reversed_integer_interval_rejected(self):
        plan, rows = _fixture_module.fixture()
        rows[0]['interval'] = [N + 1, N]
        self.assertEqual(t5.audit_t5_coverage(plan, rows)['status'], 'REJECTED')

    def test_02_received_singleton_misses_oracle_by_one(self):
        plan, rows = cell_fixture(N + 1, [N] * 4)
        cell = self.complete_cell(plan, rows)
        self.assertEqual((cell['covered'], cell['planned']), (0, 4))
        self.assertEqual(cell['conservative_coverage'], 0)
        self.assertEqual((cell['mean_bias'], cell['max_abs_error'], cell['rmse']),
                         (-1, 1, 1))
        self.assertIs(cell['declared_toy_coverage_target_met'], False)
        self.assertIs(cell['declared_toy_bias_budget_met'], False)

    def test_03_mixed_and_negative_reversed_intervals_rejected(self):
        for endpoints in ([N + 1, float(N)], [-N, -N - 1],
                          [float(-N), -N - 1]):
            with self.subTest(endpoints=endpoints):
                plan, rows = _fixture_module.fixture()
                rows[0]['interval'] = endpoints
                self.assertEqual(t5.audit_t5_coverage(plan, rows)['status'],
                                 'REJECTED')

    def test_04_mixed_integer_float_subtraction_keeps_unit_error(self):
        for truth, value, signed_error in ((N + 1, float(N), -1),
                                           (float(N), N + 1, 1)):
            with self.subTest(truth=truth, value=value):
                plan, rows = cell_fixture(truth, [value] * 4)
                cell = self.complete_cell(plan, rows)
                self.assertEqual(cell['covered'], 0)
                self.assertEqual(cell['mean_bias'], signed_error)
                self.assertEqual(cell['max_abs_error'], 1)
                self.assertEqual(cell['rmse'], 1)
                self.assertIs(cell['declared_toy_bias_budget_met'], False)

    def test_05_negative_porosity_is_not_rounded_or_clamped(self):
        plan, rows = cell_fixture(-N - 1, [-N] * 4, quantity='POROSITY')
        cell = self.complete_cell(plan, rows)
        self.assertEqual(cell['oracle'], -N - 1)
        self.assertEqual((cell['covered'], cell['mean_bias']), (0, 1))
        self.assertIs(cell['declared_toy_bias_budget_met'], False)

    def test_06_neighbor_and_huge_exact_singletons_remain_valid(self):
        for truth in (N - 1, N, N + 1, 10 ** 400):
            with self.subTest(truth=truth):
                plan, rows = cell_fixture(truth, [truth] * 4, budget=0)
                cell = self.complete_cell(plan, rows)
                self.assertEqual(cell['oracle'], truth)
                self.assertEqual((cell['covered'], cell['mean_bias'],
                                  cell['max_abs_error'], cell['rmse']),
                                 (4, 0, 0, 0))
                self.assertIs(cell['declared_toy_bias_budget_met'], True)

    def test_07_exact_mean_above_integer_budget_is_not_rounded_to_tie(self):
        plan, rows = cell_fixture(0, [N, N, N, N + 1], budget=N)
        cell = self.complete_cell(plan, rows)
        self.assertIs(cell['declared_toy_bias_budget_met'], False)
        self.assertIn('mean_bias_exact_ratio', cell)
        self.assertEqual(cell['mean_bias_exact_ratio'], [4 * N + 1, 4])
        self.assertEqual(cell['effective_bias_budget_exact_ratio'], [N, 1])

    def test_08_exact_signed_mean_at_and_above_budget(self):
        for values, accepted in (([-N] * 4, True),
                                  ([-N, -N, -N, -N - 1], False)):
            with self.subTest(accepted=accepted):
                plan, rows = cell_fixture(0, values, quantity='POROSITY',
                                          budget=float(N))
                cell = self.complete_cell(plan, rows)
                self.assertIs(cell['declared_toy_bias_budget_met'], accepted)

    def test_09_relative_budget_product_keeps_half_unit_boundary(self):
        truth = 2 * N - 1
        # 0.5 * truth = N - 0.5 exactly. Error N exceeds it; N - 1 does not.
        for error, accepted in ((N - 1, True), (N, False)):
            with self.subTest(error=error):
                plan, rows = cell_fixture(truth, [truth + error] * 4,
                                          budget=.5, mode='REL')
                cell = self.complete_cell(plan, rows)
                self.assertEqual(cell['mean_bias'], error)
                self.assertIs(cell['declared_toy_bias_budget_met'], accepted)
                self.assertIn('effective_bias_budget_exact_ratio', cell)
                self.assertEqual(cell['effective_bias_budget_exact_ratio'],
                                 [2 * N - 1, 2])

    def test_10_large_opposite_errors_cancel_without_losing_max_error(self):
        error = N + 1
        plan, rows = cell_fixture(0, [-error, error, -error, error],
                                  quantity='POROSITY', budget=0)
        cell = self.complete_cell(plan, rows)
        self.assertEqual(cell['mean_bias'], 0)
        self.assertEqual(cell['max_abs_error'], error)
        self.assertIs(cell['declared_toy_bias_budget_met'], True)
        self.assertTrue(math.isfinite(cell['rmse']))
        self.assertEqual(cell['rmse'], float(error))

    def test_11_unrepresentable_rmse_display_is_rejected(self):
        plan, rows = cell_fixture(0, [10 ** 400] * 4)
        report = t5.audit_t5_coverage(plan, rows)
        self.assertEqual(report['status'], 'REJECTED')
        self.assertIs(report['physical_ready'], False)
        self.assertIs(report['execution_go'], False)

    def test_12_float_binary_values_keep_their_original_meaning(self):
        # Binary float 0.4 - 0.3 is strictly greater than binary float 0.1.
        plan, rows = cell_fixture(.3, [.4] * 4, budget=.1)
        cell = self.complete_cell(plan, rows)
        self.assertEqual(cell['mean_bias'], .4 - .3)
        self.assertEqual(cell['max_abs_error'], .4 - .3)
        self.assertIs(cell['declared_toy_bias_budget_met'], False)

    def test_13_numeric_subclasses_and_bool_rejected_without_hooks(self):
        calls = []

        class IntChild(int):
            def __float__(self):
                calls.append('float-int-child')
                raise AssertionError('conversion hook must not run')

        class FloatChild(float):
            def __float__(self):
                calls.append('float-float-child')
                raise AssertionError('conversion hook must not run')

        for value in (True, IntChild(N + 1), FloatChild(1.0)):
            for location in ('oracle', 'row', 'endpoint', 'budget'):
                with self.subTest(type=type(value).__name__, location=location):
                    plan, rows = _fixture_module.fixture()
                    if location == 'oracle':
                        plan['cases'][0]['oracles']['sphere_full'] = value
                    elif location == 'row':
                        rows[0]['value'] = value
                    elif location == 'endpoint':
                        rows[0]['interval'][0] = value
                    else:
                        plan['error_policy']['budget'] = value
                    self.assertEqual(t5.audit_t5_coverage(plan, rows)['status'],
                                     'REJECTED')
        self.assertEqual(calls, [])

    def test_14_exact_diagnostics_are_json_data_and_inputs_unchanged(self):
        plan, rows = cell_fixture(N + 1, [float(N)] * 4)
        saved = deepcopy((plan, rows))
        report = t5.audit_t5_coverage(plan, rows)
        self.assertEqual(report['status'], 'SYNTHETIC_BOOKKEEPING_COMPLETE')
        cell = report['cells'][0]
        self.assertIn('mean_bias_exact_ratio', cell)
        self.assertEqual(cell['mean_bias_exact_ratio'], [-1, 1])
        self.assertEqual(cell['max_abs_error_exact_ratio'], [1, 1])
        restored = json.loads(json.dumps(report, allow_nan=False))
        self.assertEqual(restored, report)
        self.assertEqual((plan, rows), saved)

    def test_15_nonzero_derived_float_underflow_is_rejected(self):
        # The exact mean is 2**-1076, below the least positive binary64.
        smallest = math.ulp(0.0)
        plan, rows = cell_fixture(0, [smallest, 0, 0, 0], budget=0)
        report = t5.audit_t5_coverage(plan, rows)
        self.assertEqual(report['status'], 'REJECTED')
        self.assertIs(report['execution_go'], False)

    def test_16_small_representable_float_diagnostics_remain_valid(self):
        plan, rows = cell_fixture(0, [1e-300] * 4, budget=1e-300)
        cell = self.complete_cell(plan, rows)
        self.assertEqual(cell['mean_bias'], 1e-300)
        self.assertEqual(cell['max_abs_error'], 1e-300)
        self.assertEqual(cell['rmse'], 1e-300)
        self.assertIs(cell['declared_toy_bias_budget_met'], True)
