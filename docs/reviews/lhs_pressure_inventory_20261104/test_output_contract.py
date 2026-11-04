"""Synthetic output contract probes; never invoke inventory against host paths."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TARGET = Path(os.environ.get('LPI_COMMAND', str(Path(__file__).resolve().parent / 'pressure_inventory.sh')))
PREFIX = '{"probe'

# Execute the real entrypoint in a disposable process. Only identity/inventory
# and stdout are substituted; process shutdown remains real.
CHILD = r'''
import os, sys
source = open(sys.argv[1], encoding='utf-8').read()
code = source.split("-c '\n", 1)[1].rsplit("\n' \"$@\"", 1)[0]
cut = code.rfind('\nif __name__ == "__main__":')
assert cut >= 0
ns = {'__name__': 'synthetic_inventory'}
exec(compile(code[:cut], '<inventory-definitions>', 'exec'), ns)
mode = sys.argv[2]
ns['runtime_identity'] = lambda: None
ns['identity_allowed'] = lambda *args: True
def inventory(*args):
    if mode == 'compute':
        raise OSError('PRIVATE_ERROR_PAYLOAD')
    if mode == 'serialize':
        return {'rc': 0, 'bad': object()}
    return {'schema': 'lhs_pressure_inventory/v1', 'status': 'INVENTORY_COMPLETE', 'rc': 0}
ns['inventory'] = inventory
class Sink:
    def __init__(self):
        self.calls = 0
        self.flushes = 0
        self.buffered = b''
    def write(self, value):
        self.calls += 1
        if mode == 'persistent' or (mode == 'first' and self.calls == 1):
            raise OSError('PRIVATE_WRITE_PAYLOAD')
        if mode == 'prefix' and self.calls == 1:
            os.write(1, b'{"probe')
            raise OSError('PRIVATE_PARTIAL_PAYLOAD')
        if mode == 'short' and self.calls == 1:
            os.write(1, b'{"probe')
            return 7
        if mode in ('flush', 'buffered'):
            self.buffered += value.encode()
            return len(value)
        os.write(1, value.encode())
        return len(value)
    def flush(self):
        self.flushes += 1
        if mode == 'buffered':
            os.write(1, self.buffered)
            self.buffered = b''
        if mode == 'flush':
            # A failed flush may already have emitted a prefix. A later flush
            # would retry buffered data: the production exit must prevent it.
            if self.flushes == 1:
                os.write(1, b'{"probe')
                raise OSError('PRIVATE_FLUSH_PAYLOAD')
            os.write(1, b'REFLUSH_FORBIDDEN' + self.buffered)
            raise OSError('PRIVATE_REFLUSH_PAYLOAD')
sys.stdout = Sink()
sys.argv = [sys.argv[1], 'ibb']
ns['__name__'] = '__main__'
exec(compile(code[cut:], '<actual-inventory-entry>', 'exec'), ns)
'''


class OutputContract(unittest.TestCase):
    def child(self, mode):
        return subprocess.run([sys.executable, '-I', '-B', '-c', CHILD, str(TARGET), mode],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)

    def test_normal_exactly_one_json_and_zero(self):
        p = self.child('normal')
        self.assertEqual(p.returncode, 0, p.stderr)
        obj = json.loads(p.stdout)
        self.assertEqual((obj['status'], obj['rc']), ('INVENTORY_COMPLETE', 0))
        self.assertEqual(p.stderr, b'')

    def test_computation_error_one_failure_json(self):
        p = self.child('compute')
        self.assertNotEqual(p.returncode, 0)
        obj = json.loads(p.stdout)
        self.assertEqual((obj['status'], obj['rc']), ('NOT_ESTABLISHED', 2))
        self.assertNotIn(b'PRIVATE_', p.stdout)

    def test_serialization_error_one_failure_json(self):
        p = self.child('serialize')
        self.assertNotEqual(p.returncode, 0)
        obj = json.loads(p.stdout)
        self.assertEqual((obj['status'], obj['rc']), ('NOT_ESTABLISHED', 2))
        self.assertNotIn(b'PRIVATE_', p.stdout)

    def test_buffered_success_flushes_before_exit(self):
        p = self.child('buffered')
        self.assertEqual(p.returncode, 0, p.stderr)
        obj = json.loads(p.stdout)
        self.assertEqual((obj['status'], obj['rc']), ('INVENTORY_COMPLETE', 0))
        self.assertEqual(p.stderr, b'')

    def test_first_write_failure_no_second_output(self):
        p = self.child('first')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, b'')

    def test_partial_write_no_second_output(self):
        p = self.child('prefix')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, PREFIX.encode())

    def test_persistent_failure_nonzero_no_output(self):
        p = self.child('persistent')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, b'')

    def test_short_write_rejected_without_retry(self):
        p = self.child('short')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, PREFIX.encode())

    def test_flush_failure_no_shutdown_reflush(self):
        p = self.child('flush')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, PREFIX.encode())

    def fake_interpreter(self, ending, partial=False):
        # Only the shell wrapper runs. Its python3 resolves to this fake shell
        # executable, so embedded Python and fixed research roots are untouched.
        with tempfile.TemporaryDirectory(prefix='lpi-output-contract-') as folder:
            path = Path(folder)/'python3'
            payload = "printf '%s' '{\"probe'\n" if partial else ''
            path.write_text('#!/bin/sh\n' + payload + ending + '\n')
            path.chmod(0o755)
            env = dict(os.environ, PATH=folder)
            return subprocess.run(['/bin/sh', str(TARGET), 'ibb'], env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)

    def test_shell_start_rc2_no_fallback(self):
        p = self.fake_interpreter('exit 2')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, b'')

    def test_shell_start_other_error_no_fallback(self):
        p = self.fake_interpreter('exit 7')
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, b'')

    def test_shell_partial_error_no_fallback(self):
        p = self.fake_interpreter('exit 7', partial=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, PREFIX.encode())

    def test_shell_signal_partial_no_fallback(self):
        p = self.fake_interpreter('kill -TERM $$', partial=True)
        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(p.stdout, PREFIX.encode())


if __name__ == '__main__':
    unittest.main(verbosity=2)
