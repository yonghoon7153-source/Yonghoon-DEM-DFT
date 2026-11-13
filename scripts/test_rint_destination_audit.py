"""RTR-01: exact shell publication fragment, synthetic files and AST consumer.

No full runner, solver, signals, field access, or research payload qualification.
The fresh-arm check is an explicit assumption here. RINT_AUDIT_BASH selects Bash;
RINT_AUDIT_SOURCE_ROOT optionally selects a fixed before/mutant source copy.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(os.environ.get('RINT_AUDIT_SOURCE_ROOT', Path(__file__).resolve().parents[1]))
SHELL = (ROOT / 'scripts/sdcp_gain_vox015_8arm.sh').read_text(encoding='utf-8')
START = SHELL.index('\n  fi\n', SHELL.index('echo "     원본을 남겨 둔다: $FRESH"')) + len('\n  fi\n')
PUBLISH = SHELL[START:SHELL.index('\n  return 0', START) + len('\n  return 0')]
SKIP_START = SHELL.index('  if [ -s "$OUT" ]; then')
SKIP = SHELL[SKIP_START:SHELL.index('\n  # 이 vox', SKIP_START)]
BASH = os.environ.get('RINT_AUDIT_BASH') or shutil.which('bash')


def definitions(file, names, namespace):
    tree = ast.parse((ROOT / 'scripts' / file).read_text(encoding='utf-8'))
    nodes = [n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), file, 'exec'), namespace)
    return namespace


CS = definitions('cjunc_store.py', {'audit_path', 'write_audit', 'AuditSupersessionError'},
                 {'os': os, 'json': json, 'AUDIT_PREFIX': 'cjstore_audit_'})
RC = definitions('rint_r_chain.py', {'cjunc_store_arm_audit'},
                 {'Path': Path, 'json': json, 'CJUNC_AUDIT_PREFIX': 'cjstore_audit_',
                  'CJUNC_AUDIT_ARM_KEYS': ('arm', 'status', 'key', 'store_file', 'file_sha256', 'why', 'problem')})


def audit(status, key):
    return {'schema': 'cjstore-audit-v1', 'status': status, 'key': key * 64,
            'file': 'cjreg_' + key * 64 + '.npz', 'file_sha256': 'c' * 64,
            'why': None, 'runtime': {'scope': 'synthetic'}}


class DestinationAuditTests(unittest.TestCase):
    def setUp(self):
        if not BASH:
            self.fail('Bash is required; this suite does not claim a skipped PASS')
        self.temp = tempfile.TemporaryDirectory(prefix='rtr01_')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'run').mkdir(); (self.root / 'out').mkdir()
        self.fresh = self.root / 'run/p2_synthetic.json'
        self.out = self.root / 'out/p2_synthetic.json'
        self.src_audit = self.fresh.with_name('cjstore_audit_' + self.fresh.name)
        self.dst_audit = self.out.with_name('cjstore_audit_' + self.out.name)
        self.fresh.write_bytes(b'{"attempt":"new","qualified_stub":true}\n')
        self.out.write_bytes(b'{"attempt":"old"}\n')
        self.old = json.dumps(audit('hit', 'a'), sort_keys=True).encode()
        self.dst_audit.write_bytes(self.old)

    def publish(self, setup='', store=True, skip=False):
        script = ('set -u\nFRESH=run/p2_synthetic.json\nOUT=out/p2_synthetic.json\n'
                  'OUTDIR=out\nTAG=synthetic\nSCR=unused\nFIBRE_STAMP=unused\n'
                  'CJS_FLAG=' + ('synthetic' if store else "''") + '\n' + setup + '\n'
                  'publish() {\n' + (SKIP + '\n' if skip else '') + PUBLISH + '\n}\npublish\n')
        (self.root / 'publish.sh').write_text(script, encoding='utf-8', newline='\n')
        return subprocess.run([BASH, '--noprofile', '--norc', 'publish.sh'], cwd=self.root,
                              capture_output=True, text=True, encoding='utf-8', timeout=20)

    def row(self):
        return RC['cjunc_store_arm_audit'](self.root / 'out', [self.out.name])[0]

    def archived(self):
        return [p for p in (self.root / 'out').rglob('*')
                if p.is_file() and p != self.dst_audit and p.read_bytes() == self.old]

    def assert_missing_new(self):
        self.assertEqual(json.loads(self.out.read_text())['attempt'], 'new')
        self.assertEqual(self.row()['problem'], 'missing')
        self.assertIsNone(self.row()['status'])
        self.assertEqual(len(self.archived()), 1)

    def test_missing_new_audit_is_missing_not_old_success(self):
        self.assertEqual(self.publish().returncode, 0)
        self.assert_missing_new()

    def test_audit_builder_failure_is_missing_not_old_success(self):
        def fail(): raise OSError('synthetic builder failure')
        with self.assertRaises(OSError): CS['write_audit'](str(self.fresh), fail)
        self.assertEqual(self.publish().returncode, 0)
        self.assert_missing_new()

    def test_audit_move_failure_is_missing_not_old_success(self):
        CS['write_audit'](str(self.fresh), audit('built_written', 'b'))
        result = self.publish('mv() { case "$1" in run/cjstore_audit_*) return 1;; *) command mv "$@";; esac; }')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(self.src_audit.is_file())
        self.assert_missing_new()

    def test_normal_publish_preserves_old_and_reads_new(self):
        CS['write_audit'](str(self.fresh), audit('built_written', 'b'))
        new = self.src_audit.read_bytes()
        self.assertEqual(self.publish().returncode, 0)
        self.assertEqual(self.dst_audit.read_bytes(), new)
        self.assertEqual(self.row()['key'], 'b' * 64)
        self.assertIsNone(self.row()['problem'])
        self.assertEqual(len(self.archived()), 1)

    def test_retirement_failure_stops_arm_publication(self):
        old_arm = self.out.read_bytes()
        result = self.publish('mv() { case "$*" in *out/cjstore_audit_*) return 1;; *) command mv "$@";; esac; }')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.out.read_bytes(), old_arm)
        self.assertEqual(self.dst_audit.read_bytes(), self.old)
        self.assertTrue(self.fresh.is_file())

    def test_archive_allocation_failure_stops_arm_publication(self):
        old_arm = self.out.read_bytes()
        self.assertNotEqual(self.publish('mktemp() { return 1; }').returncode, 0)
        self.assertEqual(self.out.read_bytes(), old_arm)
        self.assertEqual(self.dst_audit.read_bytes(), self.old)
        self.assertTrue(self.fresh.is_file())

    def test_valid_skip_preserves_existing_audit(self):
        old_arm = self.out.read_bytes()
        result = self.publish('python3() { return 0; }\nmv() { return 99; }\nmktemp() { return 99; }', skip=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn('SKIP', result.stdout)
        self.assertEqual(self.out.read_bytes(), old_arm)
        self.assertEqual(self.dst_audit.read_bytes(), self.old)
        self.assertTrue(self.fresh.is_file())
        self.assertEqual(self.archived(), [])

    def test_store_off_preserves_existing_sidecars_and_no_aggregation(self):
        CS['write_audit'](str(self.fresh), audit('built_written', 'b'))
        self.assertEqual(self.publish(store=False).returncode, 0)
        self.assertEqual(self.dst_audit.read_bytes(), self.old)
        self.assertTrue(self.src_audit.exists())
        tree = ast.parse((ROOT / 'scripts/rint_r_chain.py').read_text(encoding='utf-8'))
        runner = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Runner')
        method = next(n for n in runner.body if isinstance(n, ast.FunctionDef) and n.name == '_store_audit')
        ns = {'cjunc_store_arm_audit': lambda *a: self.fail('store-off aggregation')}
        exec(compile(ast.Module(body=[method], type_ignores=[]), '<exact store-off method>', 'exec'), ns)
        obj = type('Fixture', (), {'cjunc_store': None, 'store_audit': []})()
        ns['_store_audit'](obj, 'synthetic', self.root / 'out', [{'file': self.out.name}])
        self.assertEqual(obj.store_audit, [])

    def test_repeated_retirement_never_overwrites_history(self):
        for _ in range(2):
            self.dst_audit.write_bytes(self.old)
            self.fresh.write_bytes(b'{"attempt":"new"}')
            self.assertEqual(self.publish().returncode, 0)
        self.assertEqual(len(self.archived()), 2)
        self.assertEqual(self.row()['problem'], 'missing')

    def test_arm_move_failure_cannot_publish_audit_as_new(self):
        CS['write_audit'](str(self.fresh), audit('built_written', 'b'))
        old_arm = self.out.read_bytes()
        result = self.publish('mv() { case "$1" in run/p2_*) return 1;; *) command mv "$@";; esac; }')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.out.read_bytes(), old_arm)
        self.assertEqual(self.row()['problem'], 'missing')
        self.assertTrue(self.src_audit.exists())
        self.assertEqual(len(self.archived()), 1)


if __name__ == '__main__':
    unittest.main()
