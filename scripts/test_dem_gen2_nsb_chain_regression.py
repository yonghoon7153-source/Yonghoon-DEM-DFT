"""NSB-C01/C02 expected-correct regressions, written before candidate edits.

Only existing invented fixtures are loaded from explicitly copied dependencies.
The first three cases adapt the received review assertions, never its top-level
writer/runner. A process/network audit must already be installed by the runner.
"""
import copy
import math
from pathlib import Path
import types
import unittest


source_dir = Path(__file__).parent
fixtures = types.ModuleType('fixed_synthetic_matrix_fixture')
fixtures.__file__ = str(source_dir / 'test_dem_gen2_qualification_matrix.py')
exec(compile(Path(fixtures.__file__).read_bytes(), fixtures.__file__, 'exec'), fixtures.__dict__)
p2_fixture = fixtures.p2_fixture_module
p2 = p2_fixture.p2
matrix = fixtures.matrix


def post_rows(trace):
    return [row for row in trace if row.get('phase') == 'POST']


def set_post_height(trace, value):
    for row in post_rows(trace):
        for sample in row['samples']:
            sample['surface_height'] = value


def negative_packet(packets):
    return next(packet for packet in packets if packet['case_id'] == 'partial_control')


def rebind_packet_plan(plan, packets, context, packet):
    """Coherent synthetic setup before the expected outcome, not an operating seal."""
    p2_fixture.refreeze(packet['p2_plan'], packet['p2_context'])
    digest = packet['p2_context']['expected_plan_sha256']
    for row in packet['trace']:
        row['plan_sha256'] = digest
    case = next(case for case in plan['cases'] if case['case_id'] == packet['case_id'])
    case['expected_plan_sha256'] = digest
    fixtures.refreeze(plan, context)


class NSBChainRegression(unittest.TestCase):
    def no_authority(self, result):
        for key in ('physical_ready', 'execution_go', 'transition_authorized', 'gate_write',
                    'operational_seal_modified', 'registration_complete', 'source_authenticated',
                    'hidden_history_qualified'):
            self.assertIs(result[key], False)
        self.assertEqual(result['research_results'], 0)
        self.assertEqual(result['whole_status'], 'HOLD')

    def p2_result(self, args, status, reason=None):
        before = copy.deepcopy(args)
        result = p2.diagnose_p2_separation(*args)
        self.assertEqual(result['status'], status, result)
        if reason is not None:
            self.assertEqual(result['reason'], reason)
        self.assertEqual(args, before)
        self.no_authority(result)
        return result

    def matrix_result(self, args, status):
        before = copy.deepcopy(args)
        result = matrix.validate_qualification_matrix(*args)
        self.assertEqual(result['status'], status, result)
        self.assertEqual(args, before)
        self.no_authority(result)
        self.assertEqual(result['actual_qualification'], 'NOT_RUN')
        self.assertEqual(result['review_status'], 'NOT_RECEIVED')
        return result

    def test_received_surface_integer_drift_is_not_rounded_to_zero(self):
        args = p2_fixture.fixture()
        set_post_height(args[3], 2**53)
        post_rows(args[3])[-1]['samples'][-1]['surface_height'] += 1
        self.p2_result(args, 'NOT_CONVERGED', 'TOY_SURFACE_DRIFT_BUDGET_EXCEEDED')

    def test_received_integer_ke_above_exact_rational_limit_does_not_pass(self):
        plan, archive, context, trace = p2_fixture.fixture()
        plan['params']['max_ke'] = [2**53, 1]
        p2_fixture.refreeze(plan, context)
        for row in trace:
            row['plan_sha256'] = context['expected_plan_sha256']
        trace[-1]['samples'][-1]['ke'] = 2**53 + 1
        self.p2_result((plan, archive, context, trace), 'NOT_CONVERGED', 'TOY_KE_BUDGET_EXCEEDED')

    def test_received_empty_trace_is_not_expected_post_budget_negative(self):
        args = fixtures.fixture()
        negative_packet(args[1])['trace'] = []
        self.matrix_result(args, 'REJECTED')

    def test_large_constant_heights_and_exact_ke_limit_are_positive(self):
        for height in (2**53, 2**53 + 1, -(2**53 + 1)):
            with self.subTest(height=height):
                plan, archive, context, trace = p2_fixture.fixture()
                set_post_height(trace, height)
                plan['params']['max_ke'] = [2**53, 1]
                p2_fixture.refreeze(plan, context)
                for row in trace:
                    row['plan_sha256'] = context['expected_plan_sha256']
                    for sample in row.get('samples', []):
                        sample['ke'] = 2**53
                self.p2_result((plan, archive, context, trace), 'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE')

    def test_precision_failure_propagates_through_coherent_matrix_packets(self):
        for kind in ('surface', 'ke'):
            with self.subTest(kind=kind):
                args = fixtures.fixture()
                packet = next(p for p in args[1] if p['case_id'] == 'coarse_complete')
                if kind == 'surface':
                    set_post_height(packet['trace'], 2**53)
                    post_rows(packet['trace'])[-1]['samples'][-1]['surface_height'] += 1
                else:
                    packet['p2_plan']['params']['max_ke'] = [2**53, 1]
                    packet['trace'][-1]['samples'][-1]['ke'] = 2**53 + 1
                    rebind_packet_plan(*args, packet)
                self.matrix_result(args, 'REJECTED')

    def test_contact_zero_and_clear_only_traces_do_not_witness_post_shortage(self):
        for prefix, label in ((1, 'contact_only'), (3, 'two_zero_without_clear'), (4, 'clear_without_post')):
            with self.subTest(stage=label):
                args = fixtures.fixture()
                packet = negative_packet(args[1])
                packet['trace'] = packet['trace'][:prefix]
                self.matrix_result(args, 'REJECTED')

    def test_complete_one_two_three_post_windows_keep_explicit_shortage_diagnostics(self):
        for complete_post in (1, 2, 3):
            with self.subTest(complete_post=complete_post):
                args = fixtures.fixture()
                packet = negative_packet(args[1])
                packet['trace'] = packet['trace'][:4 + complete_post]
                result = self.matrix_result(args, 'SYNTHETIC_MATRIX_CONSISTENT')
                row = next(row for row in result['case_results'] if row['case_id'] == 'partial_control')
                self.assertTrue(row['meets_expectation'])
                self.assertFalse(row['synthetic_case_complete'])
                self.assertEqual(row.get('negative_scope'), 'POST_SHORTAGE_AFTER_SEPARATION_AND_CLEAR')
                self.assertEqual(row.get('checked_post_windows'), complete_post)
                self.assertEqual(row.get('missing_post_windows'), 4 - complete_post)

    def test_negative_planned_end_is_bound_to_clear_plus_four_windows(self):
        for declared_end in (192, 224):
            with self.subTest(declared_end=declared_end):
                args = fixtures.fixture()
                attempt = next(a for a in args[0]['attempts'] if a['case_id'] == 'partial_control')
                attempt['planned_end_step'] = declared_end
                fixtures.refreeze(args[0], args[2])
                self.matrix_result(args, 'REJECTED')

    def test_missing_step_samples_or_post_contacts_are_not_expected_shortage(self):
        for kind in ('missing_sample', 'contact_reappeared'):
            with self.subTest(kind=kind):
                args = fixtures.fixture()
                packet = negative_packet(args[1])
                if kind == 'missing_sample':
                    packet['trace'][-1]['samples'].pop()
                else:
                    packet['trace'][-1]['samples'][0]['contact_count'] = 1
                self.matrix_result(args, 'REJECTED')

    def test_builtin_float_boundary_keeps_binary_float_semantics(self):
        for value, expected in ((0.125, 'SYNTHETIC_POST_DIAGNOSTIC_CANDIDATE'),
                                (math.nextafter(0.125, math.inf), 'NOT_CONVERGED')):
            with self.subTest(value=value):
                plan, archive, context, trace = p2_fixture.fixture()
                plan['params']['max_ke'] = [1, 8]
                p2_fixture.refreeze(plan, context)
                for row in trace:
                    row['plan_sha256'] = context['expected_plan_sha256']
                trace[-1]['samples'][-1]['ke'] = value
                self.p2_result((plan, archive, context, trace), expected)

    def test_numeric_subclasses_are_refused_without_conversion_hooks(self):
        calls = []
        class HookInt(int):
            def __float__(self): calls.append('float'); raise AssertionError('hook must not run')
        class HookFloat(float):
            def __float__(self): calls.append('float'); raise AssertionError('hook must not run')
        for value in (HookInt(2**53 + 1), HookFloat(0.0), True):
            args = p2_fixture.fixture()
            args[3][-1]['samples'][-1]['ke'] = value
            result = p2.diagnose_p2_separation(*args)
            self.assertEqual(result['status'], 'REJECTED')
            self.no_authority(result)
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
