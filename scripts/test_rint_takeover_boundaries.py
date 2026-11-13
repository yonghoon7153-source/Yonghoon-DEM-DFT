"""Small synthetic Q12/audit regressions. No solver, shell, GPU, or real inputs."""
import ast
import copy
import json
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
import uuid
from unittest import mock

import numpy as np
from scipy import sparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import cjunc_asm_compare as AC
if os.name == 'posix':
    import cjunc_store as CS
else:
    # The store import requires POSIX statvfs. Exercise these exact pure I/O
    # definitions on Windows without replacing any filesystem safety guard.
    CS = types.ModuleType('audit_functions_only')
    CS.__dict__.update(os=os, json=json, AUDIT_PREFIX='cjstore_audit_')
    source = ast.parse((ROOT / 'scripts/cjunc_store.py').read_text(encoding='utf8'))
    selected = [n for n in source.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))
                and n.name in ('audit_path', 'write_audit', 'AuditSupersessionError')]
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<exact audit definitions>', 'exec'), CS.__dict__)


def fixture():
    return {'L': sparse.csr_matrix([[2., -1.], [-1., 2.]]),
            'b': np.array([0., 1.]), 'n_dof': 2,
            'Ab': np.array([0]), 'gb': np.array([1.]),
            'At': np.array([1]), 'gt': np.array([1.])}


class AssemblyBoundaryTests(unittest.TestCase):
    def rejected(self, record):
        result = AC.compare_assembly(record, copy.deepcopy(record))
        self.assertFalse(result['comparable'])
        self.assertIsNone(result['bytes_equal'])
        self.assertEqual(result['claims'], [])

    def test_positive_and_changed_rhs(self):
        a = AC.assembly_record(fixture(), 'a' * 64, [0, 1])
        self.assertTrue(AC.compare_assembly(a, copy.deepcopy(a))['bytes_equal'])
        b = fixture(); b['b'][1] = 2.
        result = AC.compare_assembly(a, AC.assembly_record(b, 'a' * 64, [0, 1]))
        self.assertTrue(result['graph_equal'])
        self.assertFalse(result['bytes_equal'])

    def test_missing_or_invalid_generated_arrays(self):
        for field in ('b', 'Ab', 'gb', 'At', 'gt'):
            for value in (None, np.array([object()]), np.array([np.nan]), np.array([np.inf])):
                with self.subTest(field=field, value=repr(value)):
                    asm = fixture(); asm[field] = value
                    self.rejected(AC.assembly_record(asm, 'a' * 64, [0, 1]))
        asm = fixture(); del asm['b']
        self.rejected(AC.assembly_record(asm, 'a' * 64, [0, 1]))

    def test_generated_shapes_and_counts(self):
        for field, value in [('b', np.array([1.])), ('gb', np.array([])),
                             ('Ab', np.array([2])), ('n_dof', True), ('n_dof', 2.9)]:
            with self.subTest(field=field):
                asm = fixture(); asm[field] = value
                self.rejected(AC.assembly_record(asm, 'a' * 64, [0, 1]))

    def test_ids_validated_before_conversion(self):
        for ids in ([0.9, 1.9], [0, 0], [0], [False, 1], ['0', '1'],
                    [0, 2**100], [-1, 1], np.array([0., 1.])):
            with self.subTest(ids=repr(ids)):
                self.rejected(AC.assembly_record(fixture(), 'a' * 64, ids))

    def test_serialized_required_fields(self):
        good = AC.assembly_record(fixture(), 'a' * 64, [0, 1])
        for path in [('rhs',), ('csr', 'data'), ('csr', 'indices'), ('csr', 'indptr'),
                     ('dof', 'Ab'), ('dof', 'gb'), ('dof', 'At'), ('dof', 'gt')]:
            with self.subTest(path=path):
                bad = copy.deepcopy(good); at = bad
                for name in path[:-1]: at = at[name]
                at[path[-1]] = None
                self.rejected(bad)

    def test_serialized_number_and_descriptor_boundaries(self):
        good = AC.assembly_record(fixture(), 'a' * 64, [0, 1])
        for value in (True, '２', 2.9, float('nan'), float('inf'), 10**100, 0, -1):
            with self.subTest(value=repr(value)):
                bad = copy.deepcopy(good); bad['dof']['n'] = value
                self.rejected(bad)
        for key, value in [('dtype', '|O'), ('shape', [1]), ('sha256', 'bad')]:
            with self.subTest(key=key):
                bad = copy.deepcopy(good); bad['rhs'][key] = value
                self.rejected(bad)
        bad = copy.deepcopy(good); bad['complete'] = 'yes'
        self.rejected(bad)


class AuditBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='audit_boundary_')
        self.addCleanup(self.temp.cleanup)
        self.arm = str(Path(self.temp.name) / 'p2_SYNTHETIC.json')
        self.path = Path(CS.audit_path(self.arm))
        CS.write_audit(self.arm, {'status': 'hit', 'key': 'a' * 64})
        self.old = self.path.read_bytes()

    def preserved(self):
        return [p for p in self.path.parent.iterdir()
                if p.is_file() and p.name != self.path.name and p.read_bytes() == self.old]

    def test_part_write_failure_cannot_reuse_old_audit(self):
        real_open = open
        def fail_part(path, *args, **kwargs):
            if str(path).endswith('.part'): raise OSError('synthetic write failure')
            return real_open(path, *args, **kwargs)
        with mock.patch.object(CS, 'open', fail_part, create=True):
            with self.assertRaises(OSError): CS.write_audit(self.arm, {'status': 'built_write_failed'})
        self.assertFalse(self.path.exists())
        self.assertEqual(len(self.preserved()), 1)

    def test_record_construction_failure_cannot_reuse_old_audit(self):
        def failure(): raise OSError('synthetic runtime-record failure')
        with self.assertRaises(OSError): CS.write_audit(self.arm, failure)
        self.assertFalse(self.path.exists())
        self.assertEqual(len(self.preserved()), 1)

    def test_success_preserves_previous_bytes(self):
        CS.write_audit(self.arm, {'status': 'built_written'})
        self.assertEqual(json.loads(self.path.read_text())['status'], 'built_written')
        self.assertEqual(len(self.preserved()), 1)

    def test_supersession_failure_is_distinct(self):
        with mock.patch.object(CS.os, 'rename', side_effect=OSError('synthetic archive failure')):
            with self.assertRaises(Exception) as caught:
                CS.write_audit(self.arm, {'status': 'built_written'})
        self.assertEqual(type(caught.exception).__name__, 'AuditSupersessionError')
        self.assertEqual(self.path.read_bytes(), self.old)

    def test_supersession_setup_failures_are_distinct(self):
        for target, name in ((uuid, 'uuid4'), (CS.os, 'lstat')):
            with self.subTest(name=name):
                with mock.patch.object(target, name, side_effect=OSError('synthetic pre-rename failure')):
                    with self.assertRaises(Exception) as caught:
                        CS.write_audit(self.arm, {'status': 'built_written'})
                self.assertEqual(type(caught.exception).__name__, 'AuditSupersessionError')
                self.assertEqual(self.path.read_bytes(), self.old)

    def test_payload_propagates_supersession_and_builds_lazily(self):
        tree = ast.parse((ROOT / 'scripts/mpm_webapp_payload.py').read_text(encoding='utf8'))
        tries = [n for n in ast.walk(tree) if isinstance(n, ast.Try)
                 and any(isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute)
                         and c.func.attr == 'write_audit' for c in ast.walk(ast.Module(body=n.body, type_ignores=[])))]
        node = min(tries, key=lambda x: x.end_lineno - x.lineno)
        class AuditSupersessionError(OSError): pass
        def fail(*args): raise AuditSupersessionError('synthetic archive failure')
        calls = []
        stub = types.SimpleNamespace(AuditSupersessionError=AuditSupersessionError, write_audit=fail,
                                     audit_record=lambda *a, **k: calls.append(1))
        namespace = {'_cjs': stub, 'a': types.SimpleNamespace(out=self.arm, _cj_store='synthetic'),
                     '_cj_prep': {'store': {}}}
        with self.assertRaises(AuditSupersessionError):
            exec(compile(ast.Module(body=[node], type_ignores=[]), '<payload audit try>', 'exec'), namespace)
        self.assertEqual(calls, [])

    def test_runner_moves_audit_only_when_store_enabled(self):
        source = (ROOT / 'scripts/sdcp_gain_vox015_8arm.sh').read_text(encoding='utf8')
        start = source.index('  CJA="$(dirname "$FRESH")')
        block = source[start:source.index('  return 0', start)]
        self.assertIn('if [ -n "$CJS_FLAG" ] && [ -f "$CJA" ]; then', block)


if __name__ == '__main__':
    unittest.main()
