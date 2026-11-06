"""Synthetic-only diagnostic regression; never invokes a real inventory CLI."""
import json
import pathlib
import tempfile
import types
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve().parent


def load():
    source = (HERE / 'pressure_inventory.sh').read_text()
    code = source.split("exec python3 -I -B -c '\n", 1)[1].rsplit("\n' \"$@\"", 1)[0]
    module = types.ModuleType('synthetic_inventory')
    exec(compile(code, 'sealed_inventory', 'exec'), module.__dict__)
    return module


def diagnostic(report):
    # Only fixed identifiers/enums from synthetic fixtures; never exception text.
    return {key: report[key] for key in ('status', 'rc', 'roots', 'cases')}


class AncestorDiagnostics(unittest.TestCase):
    def test_ancestor_metadata_refusal_keeps_diagnostics_and_log_bytes(self):
        m = load()
        with tempfile.TemporaryDirectory(prefix='a01-synthetic-') as tmp:
            shared = pathlib.Path(tmp) / 'shared'
            root = shared / 'local'
            root.mkdir(parents=True)
            files = []
            for _, case in m.plan('wsl'):
                directory = root / case
                directory.mkdir()
                for name in ('log.liggghts', 'log.txt'):
                    path = directory / name
                    path.write_bytes(b'')
                    files.append(path)
            before = [p.read_bytes() for p in files]
            baseline = m.inventory('wsl', {'local': root})
            self.assertEqual(baseline['rc'], 0, diagnostic(baseline))
            original = m.os.open
            mutations = []

            def inject(path, flags, *args, **kwargs):
                if path == 'shared':
                    first = shared.stat()
                    sibling = shared / 'unrelated'
                    sibling.mkdir()
                    sibling.rmdir()
                    last = shared.stat()
                    mutations.append((m.stamp(first), m.stamp(last)))
                return original(path, flags, *args, **kwargs)

            with mock.patch.object(m.os, 'open', side_effect=inject):
                refused = m.inventory('wsl', {'local': root})
            details = diagnostic(refused)
            self.assertEqual(len(mutations), 1)
            self.assertNotEqual(*mutations[0], msg='filesystem did not expose injected metadata change')
            self.assertEqual(refused['rc'], 2, details)
            self.assertEqual(refused['roots'], {'local': 'CHANGED'}, details)
            self.assertEqual(refused['counted_cases'], 0, details)
            self.assertEqual(len(details['cases']), 30)
            self.assertTrue(all(r['status'] == 'NOT_ESTABLISHED' and r['reason'] == 'CHANGED'
                                for r in details['cases']), details)
            self.assertEqual(before, [p.read_bytes() for p in files])
            print(json.dumps({'scope': 'synthetic only', 'historical_cause_proven': False,
                              'baseline_rc': baseline['rc'], 'refusal': details}, sort_keys=True))


if __name__ == '__main__':
    unittest.main(verbosity=2)
