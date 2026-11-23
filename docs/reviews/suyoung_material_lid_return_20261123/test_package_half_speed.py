"""Verify the operator package against the actual pinned block; use a stub commit, never a solver."""
import argparse
import base64
import importlib.util
import io
from pathlib import Path
import re
import sys
import tarfile
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("package_half_speed", Path(__file__).with_name("package_half_speed.py"))
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


def extract(raw):
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as reader:
        members = reader.getmembers()
        assert len({m.name for m in members}) == len(members) and all(m.isfile() for m in members)
        return {m.name: reader.extractfile(m).read() for m in members}


def embedded(block, marker):
    header, tail = block.split(b"<<'" + marker + b"'\n", 1)
    payload, footer = tail.split(b'\n' + marker + b'\n', 1)
    archive = base64.b64decode(b''.join(payload.splitlines()), validate=True)
    assert package.digest(archive).encode('ascii') in footer
    return header, extract(archive), footer


class OperatorBlockTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pin = 'abcd' * 10
        self.runner = Path(__file__).with_name('run_half_speed.sh').read_bytes()
        driver = b'raise SystemExit("package test stub")\n'
        self.tree = {package.FOLDER + 'half_speed.py': driver, package.FOLDER + 'run_half_speed.sh': self.runner}
        self.git_calls = []

    def git(self, args):
        self.git_calls.append(args)
        if 'rev-parse' in args:
            self.assertEqual(args[-1], 'demo^{commit}')
            return (self.pin + '\n').encode('ascii')
        self.assertEqual(['show', self.pin], [args[-2], args[-1].split(':', 1)[0]])
        return self.tree[args[-1].split(':', 1)[1]]

    def build(self, output):
        with patch.object(package.subprocess, 'check_output', side_effect=self.git), \
             patch.object(package.subprocess, 'run') as ancestor:
            result = package.build(self.root, PREVIOUS, output, 'demo')
        self.assertEqual(ancestor.call_args.args[0][-4:], ['merge-base', '--is-ancestor', package.BASE, self.pin])
        self.assertTrue(ancestor.call_args.kwargs['check'])
        return result

    def test_frozen_sources_and_reproducible_block(self):
        path, digest, _ = self.build(self.root / 'release')
        self.assertEqual(path.name, 'PASTE_SUYOUNG_HALF_SPEED_abcdabcdabcd_1123.txt')
        self.assertEqual(path.with_suffix('.txt.sha256').read_bytes(), f'{digest}  {path.name}\n'.encode('ascii'))
        data = path.read_bytes()
        self.assertEqual(package.digest(data), digest)
        header, files, footer = embedded(data, b'HALF_SPEED_SOURCES')
        self.assertIn(b'[[ $# -eq 3', header)
        self.assertIn(b'GO_SUYOUNG_HALF_SPEED_ONCE', header)
        self.assertIn(b'run_half_speed.sh "$1" "$prior" "$baseline"', footer)
        _, previous, _ = embedded(PREVIOUS.read_bytes(), b'MATERIAL_LID_SOURCES')
        self.assertEqual(files.pop('SOURCE_SHA256SUMS'), package.manifest(files))
        self.assertEqual(files.pop('RELEASE'), (self.pin + '\n').encode('ascii'))
        for name, contents in self.tree.items():
            self.assertEqual(files.pop(name), contents)
        self.assertEqual(files, {'history/' + name: contents for name, contents in previous.items()})
        self.assertEqual(files['history/RELEASE'].decode().strip(), package.BASE)
        self.assertIn('history/history/RELEASE', files)
        self.assertEqual(self.build(self.root / 'release')[0].read_bytes(), data)
        self.assertEqual(self.build(self.root / 'another')[0].read_bytes(), data)

    def test_modified_source_block_and_source_archive_rejected(self):
        changed = self.root / 'altered.txt'
        changed.write_bytes(PREVIOUS.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'operator block'):
            package.previous_sources(changed)
        with patch.object(package, 'ARCHIVE_SHA', '0' * 64), self.assertRaisesRegex(ValueError, 'source archive'):
            package.previous_sources(PREVIOUS)

    def test_existing_different_output_preserved(self):
        path, _, _ = self.build(self.root)
        path.write_bytes(b'existing user file')
        with self.assertRaises(FileExistsError):
            self.build(self.root)
        self.assertEqual(path.read_bytes(), b'existing user file')

    def test_once_mode_and_measurement_contract(self):
        runner = self.runner.decode('ascii')
        for literal in ('--prior "$prior" --baseline "$baseline"', 'F12_STEPS=1138', 'F24_STEPS=2276',
                        'F12_BUDGET_SECONDS=900', 'F24_BUDGET_SECONDS=1800', 'WATCHDOG_GRACE_SECONDS=30',
                        '12) watchdog=930', '24) watchdog=1830', 'RETRIES=0', 'taskset -c "$cpu"',
                        'OPENBLAS_NUM_THREADS=1', 'OMP_NUM_THREADS=1', 'for cells in 12 24',
                        'suyoung_half_speed_result.tar.gz', 'HALF_SPEED_PREFIX_READBACK_COMPLETE'):
            self.assertIn(literal, runner)
        for name in ('prior', 'baseline'):
            self.assertRegex(runner, re.compile('^' + name + '_hash=[0-9a-f]{64}$', re.M))
            self.assertIn('$(sha256sum < "$' + name + '")', runner)
        positions = [runner.index(text) for text in ('"${app[@]}" check', '== CHECK_ONLY', 'mkdir -- "$once"',
                    'trap finish EXIT', '"${app[@]}" arm', '"${app[@]}" summary')]
        self.assertEqual(sorted(positions), positions)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('previous_block', type=Path)
    PREVIOUS = parser.parse_args().previous_block.resolve()
    unittest.main(argv=[sys.argv[0]], verbosity=2)
