#!/usr/bin/env python3
"""Generator seed regressions: text generation only, never a DEM launch.

Added before the generator fix. Positive hashes are pre-fix UTF-8 deck bytes;
consumer R01 checks remain independent and do not grant execution permission.
"""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_mixer_deck as gen
import mixer_deck_readback as rb
from test_mixer_d2_consumers import fixture


POSITIVE_HASHES = {
    (3, 2147483647, False): '636680f04264ccf471ad753ccc30eb75e1be93a937f0c15f38d937b81c396ba4',
    (3, 2147483629, True): '8d9e963a2b13735a8aeb87484c690b4702ad327e4686709538ea19faeab47f3d',
    (2, 2147483647, False): 'cc0a6a58c55bae69f3d59abdf48aa9b2a6f7419968284227ab1fa20cf76188fd',
    (2, 2147483629, True): '7343af40cc1787f4f5f897211dcd00c3621260aca59308718dbb2b3a32f0d56b',
}
PHASES = (('AM_P', 'AM_S', 'SE'), ('AM_P', 'SE'))
GENERATOR = Path(gen.__file__).resolve()
D2_ARGS = ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3',
           '--gm-bo-se', '0.73', '--dens-gen', 'lab20261014',
           '--stiffen-se', '20', '--hold-bo-pairwise']


def cli(out, seed, options):
    return subprocess.run([sys.executable, '-I', '-B', '-X', 'utf8', str(GENERATOR),
                           '--out', str(out), '--n-total', '100000', '--cgf', '151.4',
                           '--revolutions', '2', '--seed', str(seed)] + options,
                          capture_output=True, text=True, encoding='utf-8', timeout=30)


class GeneratorInsertionSeedBounds(unittest.TestCase):
    def test_api_rejects_noncanonical_seed_before_emitting_text(self):
        for value in (True, False, 3.0, 32452843.5, '+32452843', '032452843',
                      '32_452_843', '\uff13\uff12\uff14\uff15\uff12\uff18\uff14\uff13',
                      ' 32452843', '32452843 ', '3.0', '', None):
            with self.subTest(seed=value):
                with self.assertRaisesRegex(SystemExit, 'ASCII positive integer'):
                    fixture(seed=value, layered=False)

    def test_api_checks_range_before_primality(self):
        for value, reason in ((0, 'ASCII positive integer'), (-1, 'ASCII positive integer'),
                              (1, 'not prime'), (4, 'not prime'),
                              (2147483648, 'outside 1..2147483647'),
                              (2147483659, 'outside 1..2147483647')):
            with self.subTest(seed=value):
                with self.assertRaisesRegex(SystemExit, reason):
                    fixture(seed=value, layered=False)

    def test_layered_derived_seed_overflow_is_rejected(self):
        for phases in PHASES:
            with self.subTest(phases=phases):
                with self.assertRaisesRegex(SystemExit, 'insB seed.*outside 1..2147483647'):
                    fixture(seed=2147483647, phases=phases)

    def test_boundary_positive_bytes_and_consumer_acceptance(self):
        for phases in PHASES:
            for seed, layered in ((2147483647, False), (2147483629, True)):
                with self.subTest(phases=phases, seed=seed):
                    text, meta, _ = fixture(seed=seed, layered=layered, phases=phases)
                    self.assertEqual(hashlib.sha256(text.encode('utf-8')).hexdigest(),
                                     POSITIVE_HASHES[len(phases), seed, layered])
                    report = rb.read_d2(text, meta)
                    self.assertEqual(report['verdict'], 'PASS', report)
                    self.assertFalse(report['execution_authorized'])

    def test_cli_integer_normalization_keeps_canonical_output(self):
        for seed in ('+32452843', '032452843', '32_452_843',
                     '\uff13\uff12\uff14\uff15\uff12\uff18\uff14\uff13', ' 32452843'):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as temp:
                out = Path(temp) / 'not-created'
                result = cli(out, seed, ['--arm', 'E1'])
                self.assertEqual(result.returncode, 0, result.stderr)
                text = (out / 'in.mixer').read_text(encoding='utf-8')
                actual = [line.split()[5] for line in text.splitlines()
                          if line.startswith('fix ') and ' insert/pack seed ' in line]
                self.assertEqual(actual, ['32452843'])

    def test_cli_seed_failures_preserve_existing_output(self):
        for seed, options, reason in ((2147483648, D2_ARGS, 'outside 1..2147483647'),
                                      (2147483659, D2_ARGS, 'outside 1..2147483647'),
                                      (4, D2_ARGS, 'not prime'),
                                      (2147483647, D2_ARGS, 'insB seed')):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as temp:
                out = Path(temp) / 'existing'
                out.mkdir()
                sentinel = out / 'in.mixer'
                sentinel.write_bytes(b'pre-existing synthetic marker\n')
                result = cli(out, seed, options)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(reason, result.stderr)
                self.assertEqual(sentinel.read_bytes(), b'pre-existing synthetic marker\n')
                self.assertEqual(sorted(p.name for p in out.iterdir()), ['in.mixer'])

    def test_all_arms_failure_does_not_publish_partial_decks(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'not-created'
            result = cli(out, 2147483647, ['--all-arms'])
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('insB seed', result.stderr)
            self.assertFalse(out.exists())

    def test_cli_boundary_positives_keep_exact_insert_seeds(self):
        for seed, options, expected in ((2147483647, ['--arm', 'E1'], ['2147483647']),
                                        (2147483629, D2_ARGS, ['2147483629', '2147483647'])):
            with self.subTest(seed=seed), tempfile.TemporaryDirectory() as temp:
                out = Path(temp) / 'deck'
                result = cli(out, seed, options)
                self.assertEqual(result.returncode, 0, result.stderr)
                text = (out / 'in.mixer').read_text(encoding='utf-8')
                actual = [line.split()[5] for line in text.splitlines()
                          if line.startswith('fix ') and ' insert/pack seed ' in line]
                self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
