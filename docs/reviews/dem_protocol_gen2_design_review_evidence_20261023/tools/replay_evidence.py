#!/usr/bin/env python3
"""Replay the preserved probes against source-pin blobs, without checkout changes.

The temporary source directory has no .git and is not a checkout/worktree. Git is
used only to read objects from --repo. Outputs must be a new directory. This is
an evidence replay, not a new independent review or a whole-repository gate.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    bundle = Path(__file__).resolve().parent.parent
    tools = bundle / 'tools'
    author, independent = bundle / 'author', bundle / 'independent'
    source_manifest = json.loads((author / 'source-manifest.json').read_text())
    pin = source_manifest['source_pin']
    if out.exists():
        raise SystemExit('Output already exists; choose a new directory to preserve evidence')
    out.mkdir(parents=True)
    snapshot = out / 'source-pin'
    snapshot.mkdir()
    records = source_manifest['sources'] + source_manifest['sealed32']
    expected = {row['path']: row['sha256'] for row in records}
    paths = sorted(set(expected) | {'scripts/run_network_194_parallel.py'})
    materialized = []
    for path in paths:
        relative = PurePosixPath(path)
        if relative.is_absolute() or '..' in relative.parts or '\\' in path:
            raise ValueError(f'Unsafe manifest path: {path!r}')
        data = subprocess.check_output(['git', '-C', str(repo), 'show', f'{pin}:{path}'])
        digest = hashlib.sha256(data).hexdigest()
        if path in expected and digest != expected[path]:
            raise ValueError(f'Source-pin hash mismatch: {path}')
        target = snapshot.joinpath(*relative.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        materialized.append({'path': path, 'bytes': len(data), 'sha256': digest})
    (out / 'materialized-source-manifest.json').write_text(
        json.dumps({'source_pin': pin, 'files': materialized}, indent=2) + '\n')

    runs = []

    def run(name, script, arguments, stdout_name):
        command = [sys.executable, '-I', '-B', str(script), *map(str, arguments)]
        with (out / stdout_name).open('wb') as stdout, (out / f'{name}.stderr.txt').open('wb') as stderr:
            result = subprocess.run(command, stdout=stdout, stderr=stderr)
        runs.append({'name': name, 'script': script.name, 'rc': result.returncode})
        if result.returncode:
            raise SystemExit(f'{name} failed rc={result.returncode}; see preserved stderr')

    run('author-arithmetic', tools / 'probe_design_arithmetic.py', [], 'arithmetic-results.json')
    run('legacy-pressure', tools / 'mv_pressure_arithmetic.py', [], 'legacy-pressure-results.json')
    run('independent-arithmetic', tools / 'probe_independent_portable.py',
        ['--repo', snapshot, '--git-repo', repo,
         '--request', author / 'codex_dem_protocol_gen2_design_request_20261023_draft.md',
         '--out', out / 'independent-results.json'], 'independent-arithmetic.stdout.txt')
    run('repo-mc', tools / 'probe_repo_mc.py',
        ['--repo', snapshot, '--out', out / 'repo-mc-results.json'], 'repo-mc.stdout.txt')

    def read(path):
        return json.loads(path.read_text())

    observed, original = read(out / 'independent-results.json'), read(independent / 'results.json')
    comparisons = {
        'author_arithmetic_json_equal': read(out / 'arithmetic-results.json') == read(author / 'arithmetic-results.json'),
        'legacy_pressure_json_equal': read(out / 'legacy-pressure-results.json') == read(author / 'legacy-pressure-results.json'),
        'independent_checks_equal': observed['checks'] == original['checks'],
        'independent_source_hashes_equal': observed['source_files'] == original['source_files'],
        'independent_literature_equal': observed['literature'] == original['literature'],
        'independent_request_hash_equal': observed['request_sha256'] == original['request_sha256'],
        'mc_witness_json_equal': read(out / 'repo-mc-results.json') == read(independent / 'repo-mc-results.json'),
    }
    summary = {
        'scope': 'Preserved-probe replay against source-pin blobs; no new independent review or full gate',
        'source_pin': pin, 'python': sys.version, 'materialized_files': len(materialized),
        'runs': runs, 'comparisons': comparisons,
        'all_compared_fields_equal': all(comparisons.values()),
        'limitations': ['Current ULPR/final worktree equivalence is not tested.',
                        'MC seeds are counterexample witnesses, not a measured coverage estimate.',
                        'No DEM, LIGGGHTS, GPU, scheduler, external GO or measurement is performed.'],
    }
    (out / 'replay-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    if not all(comparisons.values()):
        raise SystemExit('Replay differs in compared fields; inspect replay-summary.json')
    print(json.dumps({'runs_rc0': len(runs), 'compared_fields_equal': len(comparisons),
                      'materialized_files': len(materialized)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
