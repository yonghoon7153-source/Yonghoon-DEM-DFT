#!/usr/bin/env python3
"""Local-only promisor regression for the pinned T12 loader (not physical T12).

Copies exact commit/tree/six-blob objects from --repo into disposable object
repositories. Only file transport to an empty local remote is allowed. The
optional guard mutation deliberately demonstrates an actual local lazy fetch.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from unittest import mock
import zlib


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def isolated_env():
    # A managed checkout may use alternates or Git discovery/config overrides.
    # None may leak into the deliberately incomplete test object databases.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_ALLOW_PROTOCOL='file', GIT_TERMINAL_PROMPT='0')
    return env


def objects_digest(repo):
    return {str(p.relative_to(repo)): digest(p.read_bytes())
            for p in sorted((repo / '.git/objects').rglob('*')) if p.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1],
                        help='Read-only repository containing the exact pinned objects')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1],
                        help='Root containing the runner and its evidence JSON')
    parser.add_argument('--output', type=Path, required=True, help='New scratch directory')
    parser.add_argument('--check-guard-mutation', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    script = args.source.resolve() / 'scripts/test_dem_gen2_t12_consumer_contract.py'
    spec = importlib.util.spec_from_file_location('t12_fixture', script)
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    evidence = args.source.resolve() / fixture.EVIDENCE
    manifest = json.loads((evidence / 'source-manifest.json').read_text())
    original = json.loads((evidence / 'fixture-results.json').read_text())
    env = isolated_env()
    tmp = out / 'tmp'
    tmp.mkdir()
    env.update(TMPDIR=str(tmp), TEMP=str(tmp), TMP=str(tmp))

    def git(*argv, source=False):
        # Source reads retain the managed object selectors, always prohibit fetch.
        e = dict(os.environ if source else env, GIT_NO_LAZY_FETCH='1')
        return subprocess.check_output(['git', '--no-lazy-fetch', *argv], env=e)

    version = git('--version').decode().strip()
    seed = out / 'complete'
    git('-c', 'init.templateDir=', 'init', '--quiet', str(seed))
    remote = out / 'empty-remote.git'
    git('-c', 'init.templateDir=', 'init', '--bare', '--quiet', str(remote))
    objects = []
    revisions = [('commit', fixture.PIN), ('tree', fixture.PIN + '^{tree}')]
    revisions += [('tree', fixture.PIN + ':' + path)
                  for path in ('docs', 'docs/data', fixture.PREFIX.rstrip('/'))]
    revisions += [('blob', fixture.PIN + ':' + fixture.PREFIX + name)
                  for name in sorted(fixture.FILES)]
    for kind, revision in revisions:
        oid = git('-C', str(args.repo), 'rev-parse', '--verify', revision,
                  source=True).decode().strip()
        raw = git('-C', str(args.repo), 'cat-file', kind, oid, source=True)
        encoded = kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw
        assert hashlib.sha1(encoded).hexdigest() == oid
        path = seed / '.git/objects' / oid[:2] / oid[2:]
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(zlib.compress(encoded))
        objects.append({'kind': kind, 'revision': revision, 'oid': oid,
                        'sha256': digest(raw)})
    for name, value in [('core.repositoryformatversion', '1'),
                        ('extensions.partialclone', 'origin'),
                        ('remote.origin.url', str(remote)),
                        ('remote.origin.promisor', 'true'),
                        ('remote.origin.partialclonefilter', 'blob:none')]:
        git('-C', str(seed), 'config', name, value)

    def run(label, missing=None, runner=script):
        case = out / label
        case.mkdir()
        repo = case / 'repo'
        shutil.copytree(seed, repo)
        if missing:
            oid = next(o['oid'] for o in objects if o['revision'] == missing)
            (repo / '.git/objects' / oid[:2] / oid[2:]).unlink()
        before = objects_digest(repo)
        trace = case / 'trace.jsonl'
        child_env = dict(env, GIT_NO_LAZY_FETCH='0', GIT_TRACE2_EVENT=str(trace))
        command = [sys.executable, '-I', '-X', 'utf8', '-B', str(runner), '--repo', str(repo)]
        result = subprocess.run(command, capture_output=True, env=child_env, timeout=60)
        (case / 'stdout.json').write_bytes(result.stdout)
        (case / 'stderr.txt').write_bytes(result.stderr)
        events = [json.loads(line) for line in trace.read_text().splitlines()] if trace.exists() else []
        fetches = [e for e in events if e.get('event') == 'child_start' and 'fetch' in e.get('argv', [])]
        reads = [e['argv'] for e in events if e.get('event') == 'start' and 'show' in e.get('argv', [])]
        guarded_reads = bool(reads) and all('--no-lazy-fetch' in command for command in reads)
        row = {'case': label, 'returncode': result.returncode, 'fetch_processes': len(fetches),
               'parent_GIT_NO_LAZY_FETCH': '0', 'transport': 'file only; empty local bare remote',
               'git_show_reads': len(reads), 'all_reads_explicitly_guarded': guarded_reads,
               'objects_unchanged': before == objects_digest(repo), 'missing_revision': missing,
               'trace': str(trace.relative_to(out)), 'trace_sha256': digest(trace.read_bytes()) if trace.exists() else None}
        if missing:
            row['pass'] = result.returncode == 2 and not fetches and row['objects_unchanged'] and guarded_reads
        else:
            receipt = json.loads(result.stdout) if result.returncode == 0 else {}
            row['case_count'] = receipt.get('case_count')
            row['pass'] = (result.returncode == 0 and not fetches and row['objects_unchanged'] and guarded_reads
                           and {command[-1] for command in reads} == {fixture.PIN + ':' + fixture.PREFIX + n for n in fixture.FILES}
                           and len(reads) == 6
                           and receipt.get('status') == 'PASS' and receipt.get('case_count') == receipt.get('passed') == 52
                           and receipt.get('cases') == original['cases']
                           and receipt.get('source_sha256') == manifest['files_sha256'] == original['source_sha256']
                           and receipt.get('physical_ready') is False and receipt.get('physical_T12') == 'NOT_RUN')
        return row

    rows = [run('complete-six-blobs'), run('missing-commit', fixture.PIN),
            run('missing-root-tree', fixture.PIN + '^{tree}'),
            run('missing-kit-tree', fixture.PIN + ':' + fixture.PREFIX.rstrip('/')),
            run('missing-blob', fixture.PIN + ':' + fixture.PREFIX + 'ul_gates.py')]
    compatibility = {'kind': 'mocked unsupported-option response; not a real old Git execution'}
    dest = out / 'unsupported-option'
    dest.mkdir()
    with mock.patch.dict(os.environ, {'GIT_NO_LAZY_FETCH': '0'}), mock.patch.object(
            fixture.subprocess, 'run', return_value=subprocess.CompletedProcess(
                ['git'], 129, stdout=b'', stderr=b'unknown option: --no-lazy-fetch')) as child:
        try:
            fixture.snapshot(seed, manifest, dest)
        except ValueError:
            rejected = True
        else:
            rejected = False
        call = child.call_args
        compatibility['pass'] = bool(rejected and child.call_count == 1 and not list(dest.iterdir())
                                     and '--no-lazy-fetch' in call.args[0]
                                     and call.kwargs.get('env', {}).get('GIT_NO_LAZY_FETCH') == '1')
    mutation = None
    if args.check_guard_mutation:
        mutated = out / 'guard-removed'
        for name in (Path('scripts/test_dem_gen2_t12_consumer_contract.py'),
                     Path(fixture.EVIDENCE) / 'source-manifest.json',
                     Path(fixture.EVIDENCE) / 'p1-consumer-contract.json'):
            target = mutated / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(args.source / name, target)
        runner = mutated / 'scripts/test_dem_gen2_t12_consumer_contract.py'
        text = runner.read_text()
        assert text.count('"git", "--no-lazy-fetch", "-C"') == 1
        assert text.count('dict(os.environ, GIT_NO_LAZY_FETCH="1")') == 1
        text = text.replace('"git", "--no-lazy-fetch", "-C"', '"git", "-C"')
        text = text.replace('dict(os.environ, GIT_NO_LAZY_FETCH="1")', 'dict(os.environ)')
        runner.write_text(text)
        mutation = run('guard-removal-local-fetch', fixture.PIN + ':' + fixture.PREFIX + 'ul_gates.py', runner)
        mutation['detected'] = mutation['returncode'] == 2 and mutation['fetch_processes'] > 0
        mutation['pass'] = mutation['detected']
    passed = all(row['pass'] for row in rows) and compatibility['pass'] and (mutation is None or mutation['detected'])
    report = {'status': 'PASS' if passed else 'FAIL', 'git_version': version,
              'runner_sha256': digest(script.read_bytes()), 'harness_sha256': digest(Path(__file__).read_bytes()),
              'consumer_pin': fixture.PIN, 'objects': objects, 'cases': rows,
              'compatibility_guard': compatibility, 'guard_removal_mutation': mutation,
              'physical_ready': False, 'physical_T12': 'NOT_RUN'}
    (out / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'git_version': version,
                      'cases': [{k: c[k] for k in ('case', 'returncode', 'fetch_processes', 'pass')} for c in rows],
                      'compatibility_guard_pass': compatibility['pass'],
                      'mutation_detected': None if mutation is None else mutation['detected']}, indent=2))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
