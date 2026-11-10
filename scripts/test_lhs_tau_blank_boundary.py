"""L214K-08 synthetic row tests; source AST only, no tau_flux import."""
import ast
import math
import os
from pathlib import Path
import re
import unittest


ROOT = Path(os.environ.get('LHS_BOUNDARY_SOURCE_ROOT', Path(__file__).resolve().parents[1]))
SOURCE = ROOT / 'scripts/lhs_release_build.py'


def load_checker():
    tree = ast.parse(SOURCE.read_text(encoding='utf-8'), filename=str(SOURCE))
    functions = {'_v13_num', 'v13_blank_reason', 'v13_blank_problems'}
    constants = {'KEY', '_V13_TAU_VALUE_RE', '_V13_TAU_REASON_RE', '_V13_VALUE_STATUSES',
                 '_V13_NONPERC_COLS', '_V13_FRAC_RE'}
    nodes = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in functions:
            nodes.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in constants
                                                  for t in node.targets):
            nodes.append(node)
    if {n.name for n in nodes if isinstance(n, ast.FunctionDef)} != functions:
        raise AssertionError('selected release functions missing')
    ns = dict(math=math, re=re, ReleaseError=type('SyntheticReleaseError', (ValueError,), {}),
        _v13_phases=lambda col: None,
        _v13_is_model_limit=lambda row, mode: row.get('ion_net_status_reason_' + mode) == 'full_over_conduction')
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SOURCE), 'exec'), ns)
    if not constants.issubset(ns):
        raise AssertionError('selected release declarations missing')
    return ns


class TauBlankBoundary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns = load_checker()

    def check(self, mode='hertz', status='OK', f='0.25', tau2='4', tau='2', reason=''):
        row = {self.ns['KEY']: 'synthetic_case', 'ion_net_status_' + mode: status,
               'f_ion_' + mode: f, 'tau2_ion_' + mode: tau2, 'tau_ion_' + mode: tau,
               'ion_net_status_reason_' + mode: reason}
        cols = [self.ns['KEY'], 'f_ion_' + mode, 'tau2_ion_' + mode, 'tau_ion_' + mode,
                'ion_net_status_reason_' + mode]
        return self.ns['v13_blank_problems']([row], cols)

    def test_01_finite_positive_tau_values_preserve_every_mode_and_status(self):
        for mode in ('hertz', 'hertz_h12', 'physics'):
            for status in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
                for tau2, tau in (('4', '2'), ('0.25', '0.5'), ('1e-200', '1e-100')):
                    with self.subTest(mode=mode, status=status, tau2=tau2):
                        self.assertEqual(self.check(mode, status, tau2=tau2, tau=tau), [])

    def test_02_tau2_and_tau_are_independently_finite_and_positive(self):
        for mode in ('hertz', 'hertz_h12', 'physics'):
            for status in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
                for field in ('tau2', 'tau'):
                    for bad in ('inf', '-inf', 'nan', '-1', '0', 'not_a_number'):
                        with self.subTest(mode=mode, status=status, field=field, bad=bad):
                            self.assertTrue(self.check(mode, status, **{field: bad}))

    def test_03_existing_f_status_guard_is_preserved(self):
        for status in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
            for value in ('0', '-1', 'inf', 'nan', 'bad'):
                with self.subTest(status=status, value=value):
                    self.assertTrue(self.check(status=status, f=value))
        self.assertTrue(self.check(status='NOT_PERCOLATING', f='1', tau2='', tau=''))

    def test_04_nonpercolating_uses_blank_tau_not_literal_infinity(self):
        for mode in ('hertz', 'hertz_h12', 'physics'):
            self.assertEqual(self.check(mode, 'NOT_PERCOLATING', f='0', tau2='', tau=''), [])
            self.assertTrue(self.check(mode, 'NOT_PERCOLATING', f='0', tau2='inf', tau=''))
            self.assertTrue(self.check(mode, 'NOT_PERCOLATING', f='0', tau2='', tau='inf'))

    def test_05_notcomputed_and_model_limit_blank_policies_are_preserved(self):
        for reason in ('invalid_input: synthetic conversion refusal', 'full_over_conduction'):
            self.assertEqual(self.check(status='NOT_COMPUTED', f='', tau2='', tau='', reason=reason), [])
            self.assertTrue(self.check(status='NOT_COMPUTED', f='', tau2='4', tau='', reason=reason))
        self.assertEqual(self.check(status='BAND_FALLBACK', f='', tau2='', tau=''), [])

    def test_06_absent_tau_under_value_status_is_not_fabricated(self):
        self.assertTrue(self.check(tau2=''))
        self.assertTrue(self.check(tau=''))
        # Empty reason is expected for OK, not a fabricated diagnostic string.
        self.assertTrue(self.check(reason='made_up_reason'))


if __name__ == '__main__':
    unittest.main()
