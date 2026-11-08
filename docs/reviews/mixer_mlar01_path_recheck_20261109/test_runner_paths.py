"""Synthetic runner-path regressions; invoked only by the audited mock harness."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import shlex
import tempfile
import unittest

PRISTINE = None
FIXTURES = None
OBSERVATIONS = []
BINDINGS = ('python', 'job_start', 'stdout', 'stderr')
BAD_CHARACTERS = (('SPACE', ' '), ('LF', '\n'), ('TAB', '\t'), ('VT', '\v'),
                  ('FF', '\f'), ('CR', '\r'), ('NUL', '\x00'), ('DEL', '\x7f'),
                  ('NBSP', '\u00a0'), ('LINE_SEPARATOR', '\u2028'))


def normal_config():
    # Pure synthetic POSIX tokens, never opened or executed.
    prefix = '/' + 'synthetic-mlar01'
    return {'runner_bindings': {**{key: prefix + '/' + key for key in BINDINGS},
                               'walltime': '1-00:00:00'}}


class RunnerPaths(unittest.TestCase):
    def test_normal_pristine_runner_bytes(self):
        config = normal_config()
        spec = config['runner_bindings']
        approval = 'synthetic-approval.json'
        expected = '\n'.join([
            '#!/usr/bin/env bash', '#SBATCH --partition=cpu', '#SBATCH --qos=cpu-60',
            '#SBATCH --nodes=1', '#SBATCH --ntasks=20', '#SBATCH --cpus-per-task=1',
            '#SBATCH --no-requeue', '#SBATCH --time=1-00:00:00',
            '#SBATCH --output=' + spec['stdout'], '#SBATCH --error=' + spec['stderr'],
            'set -euo pipefail', 'exec ' + ' '.join(shlex.quote(x) for x in
                (spec['python'], spec['job_start'], str(Path(approval).resolve())))]) + '\n'
        actual = PRISTINE['canonical_runner'](config, approval)
        self.assertEqual(actual.encode('utf-8'), expected.encode('utf-8'))
        OBSERVATIONS.append({'case': 'normal_pristine_runner', 'exact_expected_bytes': True,
                             'sha256': hashlib.sha256(actual.encode('utf-8')).hexdigest()})

    def test_pristine_rejects_whitespace_and_c0_del_before_generation(self):
        for key in BINDINGS:
            for name, char in BAD_CHARACTERS:
                with self.subTest(binding=key, character=name):
                    config = normal_config()
                    config['runner_bindings'][key] += char + '--array=0-7'
                    error = None
                    try:
                        PRISTINE['canonical_runner'](config, 'synthetic-approval.json')
                    except ValueError as exc:
                        error = str(exc)
                    OBSERVATIONS.append({'case': 'pristine_character_guard', 'binding': key,
                                         'character': name, 'rejected': error is not None,
                                         'reason': error})
                    self.assertEqual(error, 'runner binding ' + key)

    def test_normal_full_flow_calls_fake_scheduler_once(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = FIXTURES.Fixture(directory)
            config, approval, _, _ = fixture.make()
            with contextlib.redirect_stdout(io.StringIO()):
                fixture.submit(approval)
            self.assertEqual(len(fixture.calls), 1)
            argv, _ = fixture.calls[0]
            self.assertEqual(argv[0], 'sbatch')
            self.assertFalse(any(x.startswith(('--array', '-a')) for x in argv[1:]))
            receipt = json.loads((Path(config['case_dir']) / 'submission.receipt.json').read_bytes())
            self.assertEqual(receipt['state'], 'SUBMITTED')
            OBSERVATIONS.append({'case': 'normal_full_flow', 'fake_sbatch_calls': 1,
                                 'receipt_state': receipt['state']})

    def test_prestaged_tab_vt_ff_refused_before_fake_scheduler(self):
        # Stage an adversarial runner without asking the fixed generator to create
        # it. This checks main's revalidation in addition to the generation guard.
        for key in ('stdout', 'stderr'):
            for name, char in (('TAB', '\t'), ('VT', '\v'), ('FF', '\f')):
                with self.subTest(binding=key, character=name), tempfile.TemporaryDirectory() as directory:
                    fixture = FIXTURES.Fixture(directory)
                    config, approval, _, put = fixture.make()
                    prior = config['runner_bindings'][key]
                    config['runner_bindings'][key] += char + '--array=0-7'
                    runner = Path(config['runner']['path']).read_text(encoding='utf-8')
                    directive = '#SBATCH --' + ('output=' if key == 'stdout' else 'error=')
                    self.assertEqual(runner.count(directive + prior + '\n'), 1)
                    runner = runner.replace(directive + prior + '\n',
                                            directive + config['runner_bindings'][key] + '\n')
                    config['runner'] = put('runner', runner)
                    approval.write_text(json.dumps(config), encoding='utf-8')
                    error = None
                    with contextlib.redirect_stdout(io.StringIO()):
                        try:
                            fixture.submit(approval)
                        except ValueError as exc:
                            error = str(exc)
                    OBSERVATIONS.append({'case': 'prestaged_injection', 'binding': key,
                                         'character': name, 'rejected': error is not None,
                                         'reason': error, 'fake_sbatch_calls': len(fixture.calls)})
                    self.assertEqual(error, 'runner binding ' + key)
                    self.assertEqual(fixture.calls, [])
                    self.assertFalse((Path(directory) / 'admission').exists())
                    self.assertFalse((Path(config['case_dir']) / 'submission.claim.json').exists())


if __name__ == '__main__':
    raise SystemExit('Use run_mock_checks.py; a process/network audit hook and sealed fixture are required.')
