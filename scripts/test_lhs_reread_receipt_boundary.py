"""Synthetic L214K-05 contract tests; exact AST functions, no sealed imports.

The runner must install its audit policy before this
module is loaded. All IO below is confined to TemporaryDirectory fixtures.
"""
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from types import SimpleNamespace
import unittest


ROOT = Path(os.environ.get('LHS_BOUNDARY_SOURCE_ROOT', Path(__file__).resolve().parents[1]))
SOURCE = ROOT / 'scripts/g2_network_reread.py'


def source_functions(names, namespace):
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'), filename=str(SOURCE))
    chosen = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    if {n.name for n in chosen} != set(names):
        raise AssertionError('missing selected source function')
    # No module body, imports, _mods implementation, or sealed dependencies.
    module = ast.Module(body=chosen, type_ignores=[])
    exec(compile(module, str(SOURCE), 'exec'), namespace)
    for key in ('SCHEMA', 'IDENTITY_KEYS'):
        matches = [n.value for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == key for t in n.targets)]
        if len(matches) != 1:
            raise AssertionError('missing source declaration: ' + key)
        namespace[key] = ast.literal_eval(matches[0])
    return namespace


class RereadReceiptBoundary(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='lhs_k05_synthetic_')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fail_case = None
        self.fail_at = None
        self.exception = RuntimeError
        self.seen = []
        self.args = SimpleNamespace(selftest=False, expect_generation='g2',
            launcher_root=None, expect_set=None, expect_case=None, smoke_root=None,
            case_dir=[], json=str(self.root / 'receipt.json'))
        self.tf = SimpleNamespace(MODES=('hertz',), ROW_GENERATION_COL='ion_net_generation',
            MODEL_LIMIT_REASON='full_over_conduction',
            network_generation_contract=lambda dual: {'generation': 'g2', 'problems': []},
            generation_contract_text=lambda con: 'synthetic contract',
            case_row=self.case_row, row_generation_problems=self.row_problems,
            column_names=lambda: ('ion_net_generation', 'ion_net_status_hertz'),
            _cell=lambda value: str(value))
        self.ps = SimpleNamespace(PROVENANCE_GENERATION_KEYS=('synthetic_generation',),
            read_network_provenance=lambda path: {
                'provenance_state': 'valid', 'solver_status': 'success',
                'network_run_id': 'run_' + Path(path).name, 'synthetic_generation': 'g2'},
            provenance_generation_problem=lambda *args: [],
            network_stop_verdict=lambda *args: (True, 'synthetic stop'))
        self.ns = dict(Path=Path, tempfile=tempfile, shutil=shutil, json=json, sys=sys,
            _read_json=self.read_json, _k7_problems=lambda *args: [],
            branch_table=lambda *args: {'hertz': {'full': {'status': 'computed', 'reason': '', 'value': 1}}},
            _parse=lambda argv: self.args,
            summarize=lambda reports, meta: sum(not c['ok'] for r in reports for c in r['checks'])
                + sum(not c['ok'] for c in meta))
        source_functions({'reread_case', 'run_smoke_or_dirs', '_cells_match', 'main'}, self.ns)
        self.ns['_mods'] = lambda: (self.ps, self.tf,
            SimpleNamespace(load_webapp=lambda path: {}), SimpleNamespace())
        self.ns['synth_batch'] = lambda cd, lwb, tmp: (Path(cd), tmp)
        self.ns['handover_gate'] = lambda cd, *args: (True, 'synthetic handover', {
            Path(cd).name: {'ion_net_generation': 'g2', 'ion_net_status_hertz': 'OK'}})

    def read_json(self, path):
        if path.name == 'full_metrics.json':
            rid = 'run_' + path.parent.name
            return {'network_solver_status': 'success', 'network_run_id': rid,
                    'active_network_run_id': rid}
        if path.name == 'network_conductivity_dual.json':
            return {'fixture': 'SYNTHETIC_ONLY'}
        raise AssertionError('unexpected project data read')

    def case_row(self, path):
        name = Path(path).name
        self.seen.append(name)
        if name == self.fail_case and self.fail_at == 'case_row':
            raise self.exception('SYNTHETIC_CONSUMER_REFUSAL')
        return {'ion_net_generation': 'g2', 'ion_net_status_hertz': 'OK',
                'ion_net_status_reason_hertz': '', '_fixture_case': name}

    def row_problems(self, row):
        if row['_fixture_case'] == self.fail_case and self.fail_at == 'row_generation_problems':
            raise self.exception('SYNTHETIC_GENERATION_REFUSAL')
        return 'g2', []

    def invoke(self, names):
        self.args.case_dir = [str(self.root / name) for name in names]
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = self.ns['main']([])
        return rc, json.loads(Path(self.args.json).read_text(encoding='utf-8'))

    def test_01_normal_single_and_multiple_case_receipts(self):
        for names in (['normal'], ['normal_a', 'normal_b']):
            rc, receipt = self.invoke(names)
            self.assertEqual(rc, 0)
            self.assertEqual(receipt['n_fail'], 0)
            self.assertEqual([r['case'] for r in receipt['cases']], names)
            self.assertEqual(receipt['expected_generation'], 'g2')
            self.assertEqual([r['run_id'] for r in receipt['cases']], ['run_' + n for n in names])
            self.assertTrue(all(c['ok'] for r in receipt['cases'] for c in r['checks']))

    def test_02_case_consumer_exception_is_a_failed_case_not_an_escape(self):
        self.fail_case = 'bad'
        for point in ('case_row', 'row_generation_problems'):
            for error in (ValueError, OverflowError, RuntimeError):
                with self.subTest(point=point, error=error.__name__):
                    self.fail_at, self.exception = point, error
                    result = self.ns['reread_case'](self.root / 'bad', 'g2', self.ps, self.tf)
                    self.assertEqual(result['case'], 'bad')
                    self.assertEqual(result['run_id'], 'run_bad')
                    self.assertEqual(result['folder'], str(self.root / 'bad'))
                    failed = [c for c in result['checks'] if not c['ok']]
                    self.assertTrue(failed)
                    self.assertTrue(any(c['name'].startswith('K5') for c in failed))
                    self.assertTrue(any(error.__name__ in c['detail'] for c in failed))
                    self.assertFalse(result.get('row_cells'))

    def test_03_new_failure_replaces_old_success_receipt(self):
        rc, old = self.invoke(['old_success'])
        self.assertEqual(rc, 0)
        old_bytes = Path(self.args.json).read_bytes()
        for point in ('case_row', 'row_generation_problems'):
            with self.subTest(point=point):
                self.fail_at, self.fail_case = point, 'current_failure'
                rc, new = self.invoke(['current_failure'])
                self.assertEqual(rc, 1)
                self.assertGreater(new['n_fail'], 0)
                self.assertEqual([r['case'] for r in new['cases']], ['current_failure'])
                self.assertNotEqual(Path(self.args.json).read_bytes(), old_bytes)
                self.assertNotEqual(new, old)

    def test_04_failed_first_middle_last_never_discard_other_cases(self):
        for failed_index in range(3):
            names = ['first', 'middle', 'last']
            self.fail_at, self.fail_case = 'case_row', names[failed_index]
            with self.subTest(failed_index=failed_index):
                rc, receipt = self.invoke(names)
                self.assertEqual(rc, 1)
                self.assertEqual([r['case'] for r in receipt['cases']], names)
                for row in receipt['cases']:
                    self.assertEqual(all(c['ok'] for c in row['checks']), row['case'] != self.fail_case)

    def test_05_current_failed_check_before_consumer_remains_failed(self):
        self.ps.network_stop_verdict = lambda *args: (False, 'synthetic prior stop failure')
        rc, receipt = self.invoke(['normal'])
        self.assertEqual(rc, 1)
        self.assertGreater(receipt['n_fail'], 0)
        self.assertTrue(any(c['name'].startswith('K4') and not c['ok']
                            for c in receipt['cases'][0]['checks']))

    def test_06_interrupt_is_not_downgraded_to_a_regular_consumer_failure(self):
        self.fail_at, self.fail_case, self.exception = 'case_row', 'interrupted', KeyboardInterrupt
        with self.assertRaises(KeyboardInterrupt):
            self.ns['reread_case'](self.root / 'interrupted', 'g2', self.ps, self.tf)


if __name__ == '__main__':
    unittest.main()
