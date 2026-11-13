#!/usr/bin/env python3
"""SELF-170: execute the three source canary expressions, never the reader.

AST extraction deliberately avoids engine, gate, file permission and result-data
dependencies. This is a focused selftest regression, not the full blind suite.
Optional source argument supports an unchanged before-copy and mutation checks.
"""
import ast
import datetime
from pathlib import Path
import sys
import types
import unittest


SOURCE = Path(sys.argv.pop(1)) if len(sys.argv) > 1 else Path(__file__).with_name('mixer_smoke_blind.py')
TREE = ast.parse(SOURCE.read_bytes())
SELF = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'selftest')
FUNCS = {n.name: n for n in SELF.body if isinstance(n, ast.FunctionDef)}
ENV = {}
if '_canary_present' in FUNCS:
    exec(compile(ast.Module(body=[FUNCS['_canary_present']], type_ignores=[]), '<source-helper>', 'exec'), ENV)


def expression(name, target):
    assignment = next(n for n in ast.walk(FUNCS[name]) if isinstance(n, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == target for t in n.targets))
    if name == '_t15':
        return compile(ast.Expression(assignment.value), '<source-t15>', 'eval')
    # Extract only the no-canary condition, leaving the real selftest unchanged.
    candidates = []
    for n in ast.walk(assignment.value):
        old = isinstance(n, ast.Compare) and isinstance(n.left, ast.JoinedStr) and any(isinstance(op, ast.NotIn) for op in n.ops)
        new = (isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.Not)
               and isinstance(n.operand, ast.Call) and isinstance(n.operand.func, ast.Name)
               and n.operand.func.id == '_canary_present')
        if old or new:
            candidates.append(n)
    if len(candidates) != 1:
        raise AssertionError('source canary condition missing or ambiguous')
    return compile(ast.Expression(candidates[0]), '<source-condition>', 'eval')


C15 = expression('_t15', 'leaked')
C16 = expression('_t16', 'res')
C23 = expression('_t24', 'ok_self')


def leaks(text, shown='', needle='0.9643'):
    env = dict(ENV, canary={needle}, text=text, shown=shown)
    return bool(eval(C15, env))


def no_leak16(text):
    return eval(C16, dict(ENV, st={'delta3': 0.3929}, s2=text))


def no_leak23(text, shown=''):
    return eval(C23, dict(ENV, LC_REF=[0.9643], _Ma=lambda x: x, text=text, s2=shown))


class CanaryRegression(unittest.TestCase):
    def test_iso_timestamp_is_not_value(self):
        self.assertFalse(leaks('2026-11-12T17:35:10.964312Z'))

    def test_filename_timestamp_is_not_value(self):
        self.assertFalse(leaks('interim_full_20261112T173510.964312Z.json'))

    def test_json_value_is_leak(self):
        self.assertTrue(leaks('{"M": 0.9643}'))

    def test_negative_value_is_leak(self):
        self.assertTrue(leaks('delta=-0.3929', needle='0.3929'))

    def test_repr_prefix_is_leak(self):
        self.assertTrue(leaks('value=0.964285714', needle='0.96428'))

    def test_literal_point_not_regex_wildcard(self):
        self.assertFalse(leaks('value=0x9643'))

    def test_later_real_leak_after_timestamp(self):
        self.assertTrue(leaks('time=10.964312Z; M=0.9643'))
        self.assertTrue(leaks('time=10.964312Z', 'M=0.9643'))

    def test_boundaries_remain_conservative(self):
        for prefix in ('', ' ', '\t', '\n', '"', '-', '=', 'NaN ', 'inf ', '９'):
            with self.subTest(prefix=repr(prefix)):
                self.assertTrue(leaks(prefix + '0.9643'))
        for prefix in '0123456789':
            with self.subTest(prefix=prefix):
                self.assertFalse(leaks(prefix + '0.9643'))
        self.assertFalse(leaks(''))

    def test_second_read_condition(self):
        self.assertTrue(no_leak16('time=10.392912Z'))
        self.assertFalse(no_leak16('delta=-0.3929'))

    def test_projection_failure_condition(self):
        self.assertTrue(no_leak23('time=10.964312Z'))
        self.assertFalse(no_leak23('M=0.9643'))
        self.assertFalse(no_leak23('time=10.964312Z', 'M=0.9643'))

    def test_fixed_clock_source_copy(self):
        class Frozen(datetime.datetime):
            @classmethod
            def now(cls, tz=None):
                return cls(2026, 11, 12, 17, 35, 10, 964312, tzinfo=tz)
        now_node = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == '_now')
        env = {'datetime': types.SimpleNamespace(datetime=Frozen, timezone=datetime.timezone)}
        exec(compile(ast.Module(body=[now_node], type_ignores=[]), '<fixed-clock-source>', 'exec'), env)
        stamp = env['_now']()
        self.assertEqual(stamp, '2026-11-12T17:35:10.964312Z')
        self.assertFalse(leaks(stamp))
        self.assertTrue(no_leak23(stamp))
        self.assertTrue(no_leak16(stamp.replace('964312', '392912')))
        self.assertTrue(leaks(stamp + '; M=0.9643'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
