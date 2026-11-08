"""Own checked harness: copy-only fixtures; no actual subprocess or network.

The candidate launch folder comes from --repo; all twelve original dependencies
come from --sealed-snapshot and must match the unchanged source_seal. Neither
input is edited. Fresh --work stores raw logs and copies outside the repository.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

LAUNCH = Path('docs/reviews/mixer_first8_launch_preparation_20261106')
BLOCKED = []


def audit(event, args):
    if event.startswith(('subprocess.', 'socket.', 'os.spawn', 'os.exec')) or event in {
            'os.system', 'os.posix_spawn', 'os.startfile', 'pty.spawn'}:
        BLOCKED.append(event)
        raise AssertionError('External process/network forbidden in mocks: ' + event)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--sealed-snapshot', required=True, type=Path)
    parser.add_argument('--work', required=True, type=Path)
    parser.add_argument('--phase', required=True, choices=('before', 'after'))
    parser.add_argument('--submit-source', type=Path, help='Optional preserved before-fix bytes for replay')
    parser.add_argument('--existing', action='store_true', help='Also run unchanged 10/8/14 suites')
    args = parser.parse_args()
    sys.addaudithook(audit)  # Before loading any project code.
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)
    scratch = work / 'snapshot'
    launch = scratch / LAUNCH
    shutil.copytree(args.repo / LAUNCH, launch)
    if args.submit_source:
        (launch / 'submit_one.py.txt').write_bytes(args.submit_source.read_bytes())
    seal = json.loads((launch / 'source_seal.json').read_bytes())
    dependencies = []
    for item in seal['files']:
        relative = Path(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        source = args.sealed_snapshot / relative
        assert source.is_file() and not source.is_symlink()
        data = source.read_bytes()
        assert sha(data) == item['sha256'], 'Pinned dependency mismatch: ' + item['path']
        target = scratch / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        dependencies.append({'path': item['path'], 'sha256': sha(data), 'bytes': len(data)})
    assert len(dependencies) == 12
    assets = json.loads((launch / 'static_asset_manifest.json').read_bytes())
    for item in assets['files']:
        assert sha((launch / item['path']).read_bytes()) == item['sha256']
    assert len(assets['files']) == 40
    submit = launch / 'submit_one.py.txt'
    original = submit.read_bytes()
    (work / 'submit_source.py.txt').write_bytes(original)
    pristine = {'__file__': str(submit), '__name__': 'mlar01_pristine_only'}
    exec(compile(original, str(submit), 'exec'), pristine)
    # Retain the actual guard in pristine tests. Windows full-flow checks need
    # only this path syntax adapter, confined to the copied file.
    needle = b'spec[k].startswith("/")'
    assert original.count(needle) == 1
    adapted = original.replace(needle, b'Path(spec[k]).is_absolute()') if os.name == 'nt' else original
    submit.write_bytes(adapted)
    temporary = work / 'tmp'
    temporary.mkdir()
    tempfile.tempdir = str(temporary)
    fixture = load('mlar01_fixture', launch / 'test_mla_boundaries.py')
    new = load('mlar01_path_tests', Path(__file__).with_name('test_runner_paths.py'))
    new.PRISTINE = pristine
    new.FIXTURES = fixture
    modules = [('test_runner_paths', new)]
    if args.existing:
        modules.extend((name, load(name, launch / (name + '.py'))) for name in
                       ('test_submit_draft', 'test_job_start_draft', 'test_mla_boundaries'))
    results = []
    clean_env = {key: value for key, value in os.environ.items()
                 if not key.startswith(('SBATCH_', 'SLURM_', 'SALLOC_', 'SRUN_'))}
    capacity = types.SimpleNamespace(f_bavail=10**12, f_frsize=1, f_favail=10**9)
    with patch.dict(os.environ, clean_env, clear=True), patch.object(os, 'statvfs',
            lambda _: capacity, create=True):
        for name, module in modules:
            log = io.StringIO()
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                result = unittest.TextTestRunner(stream=log, verbosity=2).run(
                    unittest.defaultTestLoader.loadTestsFromModule(module))
            (work / (name + '.log')).write_text(log.getvalue(), encoding='utf-8', newline='\n')
            results.append({'suite': name, 'methods': result.testsRun, 'failures': len(result.failures),
                            'errors': len(result.errors), 'skipped': len(result.skipped),
                            'success': result.wasSuccessful()})
    summary = {
        'phase': args.phase, 'python': sys.version.split()[0], 'platform': sys.platform,
        'harness_sha256': sha(Path(__file__).read_bytes()),
        'path_tests_sha256': sha(Path(__file__).with_name('test_runner_paths.py').read_bytes()),
        'submit_source_sha256': sha(original), 'scratch_adapted_submit_sha256': sha(adapted),
        'pristine_guard_tested': True,
        'windows_full_flow_path_syntax_adapter': os.name == 'nt',
        'capacity_adapter': 'fixed synthetic bytes/inodes only',
        'source_pin': seal['source_pin'], 'source_seal_sha256': sha((launch / 'source_seal.json').read_bytes()),
        'static_asset_manifest_sha256': sha((launch / 'static_asset_manifest.json').read_bytes()),
        'sealed_dependencies': dependencies, 'static_assets_checked': len(assets['files']),
        'job_start_sha256': sha((launch / 'job_start.py.txt').read_bytes()),
        'suites': results, 'boundary_observations': new.OBSERVATIONS,
        'blocked_external_attempts': BLOCKED,
        'actual_scheduler_submissions': 0, 'actual_mpi_calls': 0, 'actual_research_results': 0,
        'operational_seal_changed': False, 'whole_gate': 'HOLD',
        'success': all(item['success'] for item in results) and not BLOCKED}
    (work / 'results.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False) + '\n',
                                     encoding='utf-8', newline='\n')
    print(json.dumps({'phase': args.phase, 'suites': results,
                      'blocked_external_attempts': BLOCKED, 'success': summary['success']}))
    return 0 if summary['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
