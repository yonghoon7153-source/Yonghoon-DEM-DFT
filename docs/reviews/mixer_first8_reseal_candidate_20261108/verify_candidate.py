#!/usr/bin/env python3
"""Bounded offline static compatibility evidence; never an operational seal/GO.

Reads fixed local Git objects without lazy fetch. Writes only a new caller-chosen
evidence directory, exports pinned scripts there, then generates text decks in
memory. No simulator, scheduler, remote host or research outcomes are accessed.
"""
import argparse
import copy
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ACCEPTED = '69b6bec7ac20343dd884f8d5fa63e8bf45e7df97'
RECEIPT = 'e6000405b7625acf8c2c0a393571b116479e0e97'
OLD = '527e244e4ebd6f0cb04c6cfb2ff5f3a52fb01996'
LAUNCH = 'docs/reviews/mixer_first8_launch_preparation_20261106'
FOLDER = 'docs/reviews/mixer_first8_reseal_candidate_20261108'
CHANGED = 'scripts/mixer_deck_readback.py'


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def git(repo, *args):
    env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(
        ['git', '--no-lazy-fetch', '-c', 'core.fsmonitor=false', '-C', str(repo), *args],
        env=env, timeout=30)


def blob(repo, pin, path):
    return git(repo, 'show', pin + ':' + path)


def validate_candidate(candidate, expected):
    need(candidate.get('schema') == 'first8_inactive_reseal_candidate/1', 'candidate schema')
    need(candidate.get('status') == 'INACTIVE_PENDING_EXTERNAL_REVIEW', 'candidate status')
    need(candidate.get('whole_gate') == 'HOLD', 'whole HOLD')
    for key in ('execution_authorized', 'operational_activation', 'registration_changed'):
        need(candidate.get(key) is False, key)
    need(candidate.get('research_results') == 0, 'research result count')
    need(candidate.get('validation_source_pin') == ACCEPTED, 'accepted validation pin')
    need(candidate.get('original_asset_generation_pin') == OLD, 'original asset provenance')
    need(candidate.get('original_launch_seal_path') == LAUNCH + '/source_seal.json', 'old seal path')
    rows = candidate.get('files')
    need(type(rows) is list and len(rows) == len(expected), 'complete dependency count')
    need(all(type(row) is dict and set(row) == {'path', 'sha256'} for row in rows), 'dependency fields')
    need(len({row['path'] for row in rows}) == len(rows), 'unique dependency paths')
    need({row['path']: row['sha256'] for row in rows} == expected, 'dependency hash binding')
    need('source_pin' not in candidate and 'allowed_submissions' not in candidate,
         'candidate is not a launch seal or approval artifact')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True, help='must not exist')
    args = ap.parse_args()
    repo = args.repo.resolve(strict=True)
    output = args.output.absolute()
    need(not output.exists(), 'output already exists; preserve earlier evidence')
    candidate_path = repo / FOLDER / 'candidate_seal.json'
    candidate_raw = candidate_path.read_bytes()
    candidate = json.loads(candidate_raw)
    old_raw = blob(repo, RECEIPT, LAUNCH + '/source_seal.json')
    old = json.loads(old_raw)
    need(old['source_pin'] == OLD, 'old seal provenance')
    expected, sources, delta = {}, {}, []
    for entry in old['files']:
        path = entry['path']
        before, after = blob(repo, OLD, path), blob(repo, ACCEPTED, path)
        need(sha(before) == entry['sha256'], 'old sealed hash: ' + path)
        need(blob(repo, RECEIPT, path) == after, 'receipt code drift: ' + path)
        sources[path] = after
        expected[path] = sha(after)
        delta.append(dict(path=path, original_sha256=sha(before), accepted_sha256=sha(after),
                          byte_identical=before == after,
                          accepted_git_blob=git(repo, 'rev-parse', ACCEPTED + ':' + path).decode().strip()))
    need(len(expected) == 12, 'bounded closure must have twelve entries')
    need([row['path'] for row in delta if not row['byte_identical']] == [CHANGED], 'only accepted readback changed')
    validate_candidate(candidate, expected)

    negatives = []
    for label in ('missing_dependency', 'hash_drift', 'activation', 'launch_schema'):
        bad = copy.deepcopy(candidate)
        if label == 'missing_dependency': bad['files'].pop()
        elif label == 'hash_drift': bad['files'][0]['sha256'] = '0' * 64
        elif label == 'activation': bad['operational_activation'] = True
        else: bad['source_pin'] = ACCEPTED
        try:
            validate_candidate(bad, expected)
        except ValueError as exc:
            negatives.append(dict(case=label, rejected=True, reason=str(exc)))
        else:
            raise ValueError('negative not rejected: ' + label)

    # Original launch package remains byte-for-byte at the preserved receipt pin.
    original_paths = git(repo, 'ls-tree', '-r', '--name-only', RECEIPT, '--', LAUNCH).decode().splitlines()
    launch_hashes = {}
    for path in original_paths:
        raw = blob(repo, RECEIPT, path)
        need((repo / path).read_bytes() == raw, 'original launch package modified: ' + path)
        launch_hashes[path] = sha(raw)
    driver = blob(repo, RECEIPT, LAUNCH + '/submit_one.py.txt').decode()
    need("Path(__file__).resolve().parent/'source_seal.json'" in driver, 'driver no longer binds sibling seal')
    need("c.get('source_pin')==seal['source_pin']" in driver, 'driver source pin guard')
    need(OLD != ACCEPTED, 'old pin remains different')
    operational = dict(method='static source inspection only; driver not imported or invoked',
                       driver_source_pin=OLD, candidate_validation_pin=ACCEPTED,
                       candidate_has_launch_source_pin=False, operational_activation=False,
                       driver_still_reads_original_sibling_seal=True,
                       changed_pin_would_fail_existing_equality_guard=True,
                       submission_invocations=0, mpi_invocations=0)

    manifest_raw = blob(repo, RECEIPT, LAUNCH + '/static_asset_manifest.json')
    manifest = json.loads(manifest_raw)
    need(manifest['source_pin'] == OLD, 'asset generation provenance')
    assets = {}
    for entry in manifest['files']:
        path = entry['path']
        need(path.startswith('planned_assets/') and '..' not in Path(path).parts, 'bounded asset path')
        need(path not in assets, 'duplicate asset path')
        raw = blob(repo, RECEIPT, LAUNCH + '/' + path)
        need(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], 'asset manifest: ' + path)
        need((repo / LAUNCH / path).read_bytes() == raw, 'asset worktree bytes: ' + path)
        assets[path] = raw
    need(len(assets) == 40, 'forty planned assets required')

    output.mkdir(parents=True, exist_ok=False)
    export = output / 'pinned_source'
    for path, raw in sources.items():
        target = export / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    # Load exactly the accepted files. This verifier is run as a fresh process.
    modules = [Path(path).stem for path in sources if path.endswith('.py')]
    need(not any(name in sys.modules for name in modules), 'scientific module already imported')
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(export / 'scripts'))
    prep = importlib.import_module('mixer_precal_prepare')
    cases = []
    for case_id in prep.CASE_IDS:
        stem = 'planned_assets/' + case_id + '/'
        old_deck = assets[stem + 'in.mixer']
        old_meta = json.loads(assets[stem + 'deck_meta.json'])
        fresh = prep.prepare_case(case_id)
        need(fresh['deck'] == old_deck, 'fresh deck differs: ' + case_id)
        need(prep._json_exact(fresh['meta']) == prep._json_exact(old_meta), 'typed metadata differs: ' + case_id)
        binding = prep.validate_case(case_id, old_deck, old_meta)
        need(binding['execution_authorized'] is False and binding['registered'] is None, 'binding is not GO')
        cases.append(dict(case_id=case_id, regenerated_deck_bytes_equal=True,
                          regenerated_metadata_type_sensitive_equal=True, binding=binding,
                          observed_atoms=None))
    pairs = []
    for level in (1, 2, 3):
        u, c = ('planned_assets/PRECAL_R1_B%d_%s/' % (level, role) for role in ('U', 'C'))
        result = prep.diff.diff_d2_decks(assets[u + 'in.mixer'], assets[c + 'in.mixer'],
                                        json.loads(assets[u + 'deck_meta.json']), json.loads(assets[c + 'deck_meta.json']))
        need(result['verdict'] == 'PASS' and result['execution_authorized'] is False, 'pair ' + str(level))
        pairs.append(dict(pair='R1_B%d' % level, verdict=result['verdict'], failures=result['failures']))
    for name in modules:
        if name in sys.modules:
            need(Path(sys.modules[name].__file__).resolve() == (export / 'scripts' / (name + '.py')).resolve(),
                 'module path differs: ' + name)
    for path, raw in sources.items():
        need((export / path).read_bytes() == raw, 'export changed during validation: ' + path)
    for path, digest in launch_hashes.items():
        need(sha((repo / path).read_bytes()) == digest, 'launch file changed during validation: ' + path)
    need(candidate_path.read_bytes() == candidate_raw, 'candidate changed during validation')
    report = dict(scope='inactive source-reseal candidate; static text/metadata compatibility only',
                  validation_source_pin=ACCEPTED, original_asset_generation_pin=OLD, receipt_pin=RECEIPT,
                  candidate_sha256=sha(candidate_raw), python=platform.python_version(),
                  python_executable=sys.executable, python_executable_sha256=sha(Path(sys.executable).read_bytes()),
                  dependency_comparison=delta, source_entries=len(delta),
                  original_launch_files_preserved=launch_hashes, planned_asset_files_verified=len(assets),
                  old_asset_manifest_sha256=sha(manifest_raw), cases=cases, pairs=pairs,
                  candidate_negative_probes=negatives, operational_boundary=operational,
                  registered=None, execution_authorized=False, operational_activation=False,
                  research_results=0, whole_gate='HOLD', independent_review='PENDING',
                  limitations=['same-source generation oracle is not independent physics validation',
                               'STL bytes only, no independent geometry validation',
                               'planned N100000 is not an actual particle/simulator result',
                               'no observer output, real log, binary/MPI, scheduler or host qualification',
                               'MLA external recheck and author decisions remain separate'])
    (output / 'verification.json').write_bytes(encode(report))
    print(json.dumps(dict(source_entries=len(delta), changed_sources=[CHANGED],
                          preserved_launch_files=len(launch_hashes), asset_files=len(assets),
                          cases=len(cases), pairs=len(pairs), negative_probes=len(negatives),
                          whole_gate='HOLD', operational_activation=False)))


if __name__ == '__main__':
    main()
