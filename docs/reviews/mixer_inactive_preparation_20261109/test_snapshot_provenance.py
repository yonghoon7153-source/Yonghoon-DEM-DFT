#!/usr/bin/env python3
"""Harmless synthetic source/cache fixtures; no scientific modules are imported."""
import argparse
import hashlib
import importlib
import importlib.util
import io
import json
import marshal
from pathlib import Path
import sys
import unittest
from unittest import mock


def run(verifier_path, work):
    if work.exists():
        raise ValueError('new evidence directory required')
    work.mkdir(parents=True)
    spec = importlib.util.spec_from_file_location('verifier_under_test', verifier_path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    denied = verifier.install_boundary([work])
    executed_marker = []
    observations = []
    source = b"VALUE = 'verified-source'\n"
    module_name = '_fixed_source_provenance_probe'
    relative = 'scripts/' + module_name + '.py'
    original_is_symlink = Path.is_symlink

    class SourceProvenance(unittest.TestCase):
        def fixture(self, cache=False):
            root = work / self._testMethodName
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(source)
            rows = [dict(path=relative, bytes=len(source), sha256=hashlib.sha256(source).hexdigest(),
                         git_blob=hashlib.sha1(b'blob ' + str(len(source)).encode() + b'\0' + source).hexdigest())]
            if cache:
                cache_path = Path(importlib.util.cache_from_source(str(path)))
                cache_path.parent.mkdir(parents=True)
                marker = compile("raise RuntimeError('UNVERIFIED_CACHE_MARKER')\n", str(path), 'exec')
                # PEP 552 unchecked-hash pyc: harmless marker proves -B is not a read prohibition.
                cache_path.write_bytes(importlib.util.MAGIC_NUMBER + (1).to_bytes(4, 'little')
                                       + bytes(8) + marshal.dumps(marker))
            return root, rows

        def imported_value(self, root, raws):
            finder = None
            inserted = str(root / 'scripts')
            if hasattr(verifier, 'VerifiedSourceFinder'):
                finder = verifier.VerifiedSourceFinder(root, raws, [module_name])
                sys.meta_path.insert(0, finder)
            else:
                # Exact standard import mechanism used by the preserved pre-fix verifier.
                sys.path.insert(0, inserted)
            try:
                try:
                    module = importlib.import_module(module_name)
                except RuntimeError as exc:
                    if str(exc) == 'UNVERIFIED_CACHE_MARKER':
                        executed_marker.append(self._testMethodName)
                        self.fail('unverified cache marker executed despite unchanged source bytes')
                    raise
                self.assertEqual(module.__file__, str(root / relative))
                return module.VALUE
            finally:
                sys.modules.pop(module_name, None)
                if finder is not None:
                    sys.meta_path.remove(finder)
                else:
                    sys.path.remove(inserted)
                sys.path_importer_cache.pop(inserted, None)

        def test_exact_snapshot_and_source_positive(self):
            root, rows = self.fixture()
            raws = verifier.snapshot_bytes(root, rows)
            self.assertEqual(self.imported_value(root, raws), 'verified-source')

        def test_extra_module_rejected_before_import(self):
            root, rows = self.fixture()
            (root / 'scripts/extra_probe.py').write_text("raise RuntimeError('EXTRA_MARKER')\n")
            with self.assertRaisesRegex(ValueError, 'snapshot.*graph'):
                verifier.snapshot_bytes(root, rows)

        def test_cache_rejected_before_import(self):
            root, rows = self.fixture(cache=True)
            with self.assertRaisesRegex(ValueError, 'snapshot.*graph'):
                verifier.snapshot_bytes(root, rows)

        def test_verified_source_cannot_be_replaced_by_bytecode(self):
            root, rows = self.fixture(cache=True)
            # Deliberately bypass the independent closed-graph guard to exercise the loader layer.
            raws = {relative: (root / relative).read_bytes()}
            verifier.check_snapshot(raws, rows)
            self.assertEqual(self.imported_value(root, raws), 'verified-source')

        def test_symlink_ancestor_rejected(self):
            root, rows = self.fixture()
            # Portable link-signal fixture; no actual symlink/junction is created.
            with mock.patch.object(Path, 'is_symlink', lambda path: path == root.parent or original_is_symlink(path)):
                with self.assertRaisesRegex(ValueError, 'link'):
                    verifier.snapshot_bytes(root, rows)

    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(SourceProvenance))
    output = stream.getvalue()
    print(output, end='')
    report = dict(schema='inactive_snapshot_provenance_fixture/1', methods=result.testsRun,
        failures=len(result.failures), errors=len(result.errors), rc=0 if result.wasSuccessful() else 1,
        verifier_sha256=hashlib.sha256(verifier_path.read_bytes()).hexdigest(),
        test_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        unchecked_cache_marker_executed=executed_marker,
        audit_synthetic_denial_probes=denied, actual_process_or_socket_calls=0,
        scientific_modules_imported=False, actual_symlinks_created=False,
        link_fixture_scope='Mocked ancestor link signal; not real OS junction qualification',
        actual_values_read=False, operational_activation=False, whole_gate='HOLD')
    assert denied == ['subprocess.Popen', 'socket.connect']
    (work / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (work / 'test.log').write_text(output, encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return report['rc']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verifier', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.verifier.resolve(), args.work.absolute()))
