#!/usr/bin/env python3
"""Build A then B in a NEW copy; never submit or replace a deployed folder.

The input package is fixed by an external tar SHA256 and PACKAGE_MANIFEST.json.
The historical IN verifier runs before the F8 replacement, not afterwards.
SELF-170 is supplemental: it is not silently added to the historical 12-file seal.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import time

IN = 'docs/reviews/mixer_inactive_preparation_20261109'
F8 = 'docs/reviews/mixer_first8_launch_preparation_20261106'
OBSERVER = 'scripts/mixer_precal_observe.py'
SMOKE = 'scripts/mixer_smoke_blind.py'
CASES = tuple('PRECAL_R1_B%d_%s' % (b, r) for b in (1, 2, 3) for r in ('U', 'C')) + ('PRECAL_N0', 'PRECAL_E0')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def safe_output(source, output):
    for token in (str(source), str(output)):
        require(not token.startswith(('\\\\?\\', '\\\\.\\')), 'namespace path unsupported')
    for p in (source, output):
        for q in (p, *p.parents):
            require(not q.is_symlink(), 'linked path unsupported')
    source, output = source.resolve(strict=True), output.resolve()
    require(not output.exists(), 'output must be new; no retry over previous evidence')
    require(source != output and source not in output.parents and output not in source.parents,
            'source and output must be disjoint')
    return source, output


def package_check(root):
    manifest = json.loads((root / 'PACKAGE_MANIFEST.json').read_bytes())
    require(re.fullmatch('[0-9a-f]{40}', manifest['source_pin']) is not None, 'full source pin required')
    rows = manifest['files']
    names = [r['path'] for r in rows]
    require(len(names) == len(set(names)), 'duplicate package member')
    for r in rows:
        p = PurePosixPath(r['path'])
        require(not p.is_absolute() and '..' not in p.parts and '\\' not in r['path'], 'unsafe member')
        f = root / p
        require(f.is_file() and not f.is_symlink(), 'missing or linked source')
        raw = f.read_bytes()
        require(len(raw) == r['bytes'] and sha(raw) == r['sha256'], 'source hash mismatch: ' + r['path'])
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual == set(names) | {'PACKAGE_MANIFEST.json'}, 'extra/missing package files')
    require(not any(p.is_symlink() for p in root.rglob('*')), 'linked package entry')
    return manifest


def update_inventory(source, inventory):
    result = copy.deepcopy(inventory)
    changed = []
    rows = result['source_dependencies'] + result['launch_snapshot'] + [result['preparation_test']]
    require(len(rows) == 86 and len({r['path'] for r in rows}) == 86, 'historical inventory size')
    for row in rows:
        raw = (source / row['path']).read_bytes()
        if sha(raw) != row['sha256']:
            require(row['path'] == OBSERVER, 'unapproved inventory drift: ' + row['path'])
            changed.append(row['path'])
            row.update(bytes=len(raw), sha256=sha(raw),
                       git_blob=hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest())
    require(changed == [OBSERVER], 'expected original observer inventory transition')
    return result


def stage_a(source, out):
    inv = update_inventory(source, json.loads((source / IN / 'source_inventory.json').read_bytes()))
    tool = out / 'A/tool'
    put(tool / 'source_inventory.json', encode(inv))
    put(tool / 'verify_inactive.py', (source / IN / 'verify_inactive.py').read_bytes())
    for row in inv['source_dependencies'] + inv['launch_snapshot'] + [inv['preparation_test']]:
        put(out / 'A/snapshot' / row['path'], (source / row['path']).read_bytes())
    return inv


def stage_b(source, candidate, target, pin):
    require(not target.exists(), 'B output must be new')
    shutil.copytree(source, target)
    # The delivery manifest remains a historical input record, not a seal of B.
    (target / 'PACKAGE_MANIFEST.json').rename(target / 'INPUT_PACKAGE_MANIFEST.json')
    f8 = target / F8
    assets = json.loads((f8 / 'static_asset_manifest.json').read_bytes())
    original_pin = assets['source_pin']
    cm = json.loads((candidate / 'candidate_asset_manifest.json').read_bytes())
    require(cm['original_asset_generation_pin'] == original_pin, 'asset generation provenance')
    sums = (f8 / 'planned_assets/SHA256SUMS').read_text(encoding='utf-8').splitlines()
    for cid in CASES:
        for name in ('in.mixer', 'Drum.stl', 'Front.stl', 'Back.stl'):
            require((candidate / 'candidate_assets' / cid / name).read_bytes() ==
                    (f8 / 'planned_assets' / cid / name).read_bytes(), 'deck/STL changed')
        rel = 'planned_assets/' + cid + '/deck_meta.json'
        raw = (candidate / 'candidate_assets' / cid / 'deck_meta.json').read_bytes()
        rows = [r for r in assets['files'] if r['path'] == rel]
        require(len(rows) == 1, 'one metadata manifest row')
        rows[0].update(bytes=len(raw), sha256=sha(raw))
        put(f8 / rel, raw)
        hits = [i for i, s in enumerate(sums) if s.endswith('  ' + cid + '/deck_meta.json')]
        require(len(hits) == 1, 'one metadata checksum row')
        sums[hits[0]] = sha(raw) + '  ' + cid + '/deck_meta.json'
    assets['metadata_generation_source_pin'] = cm['metadata_generation_source_pin']
    require(assets['source_pin'] == original_pin, 'original generation pin preserved')
    put(f8 / 'static_asset_manifest.json', encode(assets))
    put(f8 / 'planned_assets/SHA256SUMS', ('\n'.join(sums) + '\n').encode())
    seal = json.loads((f8 / 'source_seal.json').read_bytes())
    require(len(seal['files']) == 12, 'bounded seal remains twelve dependencies')
    seal['source_pin'] = pin
    for row in seal['files']:
        row['sha256'] = sha((source / row['path']).read_bytes())
    put(f8 / 'source_seal.json', encode(seal))
    package = json.loads((source / 'PACKAGE_MANIFEST.json').read_bytes())
    tool_rows = [r for r in package['files'] if r['path'].startswith('scripts/')]
    require(any(r['path'] == SMOKE for r in tool_rows), 'SELF-170 source must be bound')
    put(f8 / 'e0_runtime_tool_identity.json', encode(dict(
        schema='e0_reseal_runtime_source_identity/1', source_pin=pin, files=tool_rows,
        relation='Supplemental exact tool identity; historical source_seal still has twelve rows',
        deployment_performed=False, submission_authorized=False)))
    return target


def verify_b(target):
    f8 = target / F8
    manifest = json.loads((f8 / 'static_asset_manifest.json').read_bytes())
    require(len(manifest['files']) == 40, 'forty assets')
    for row in manifest['files']:
        raw = (f8 / row['path']).read_bytes()
        require(sha(raw) == row['sha256'] and len(raw) == row['bytes'], 'asset integrity')
    lines = (f8 / 'planned_assets/SHA256SUMS').read_text().splitlines()
    require(len(lines) == 40, 'forty checksums')
    for line in lines:
        digest, rel = line.split('  ', 1)
        require(sha((f8 / 'planned_assets' / rel).read_bytes()) == digest, 'asset checksum')
    for filename in ('source_seal.json', 'e0_runtime_tool_identity.json'):
        for row in json.loads((f8 / filename).read_bytes())['files']:
            require(sha((target / row['path']).read_bytes()) == row['sha256'], 'tool drift')
    return {'assets': 40, 'checksums': 40, 'bounded_dependencies': 12}


def invoke(source, out, label, args, expected=0):
    log = out / 'checks' / (label + '.log')
    log.parent.mkdir(exist_ok=True)
    start = time.monotonic()
    with log.open('wb') as f:
        cp = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', *map(str, args)],
                            cwd=source, stdout=f, stderr=subprocess.STDOUT, timeout=600)
    record = dict(label=label, rc=cp.returncode, expected_rc=expected,
                  seconds=round(time.monotonic() - start, 3), log_sha256=sha(log.read_bytes()))
    require(cp.returncode == expected, 'check failed: ' + label + '; see retained log')
    return record


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--mode', choices=('assemble', 'linux-checks'), default='linux-checks')
    a = ap.parse_args(argv)
    require(a.mode != 'linux-checks' or sys.platform.startswith('linux'), 'Linux checks require Linux')
    source, out = safe_output(a.source, a.output)
    package = package_check(source)
    if a.mode == 'linux-checks':
        require(not package.get('working_tree_overrides'), 'fixed committed input required for Linux run')
    out.mkdir()
    records = []
    summary = dict(source_pin=package['source_pin'], status='INCOMPLETE', deployment_performed=False,
                   submission_authorized=False, research_results=0, checks=records)
    try:
        stage_a(source, out)
        verifier = out / 'A/tool/verify_inactive.py'
        candidate = out / 'A/candidate'
        for mode in ('build', 'verify', 'old', 'preparation-tests'):
            records.append(invoke(source, out, 'A_' + mode, [verifier, '--mode', mode,
                '--snapshot', out / 'A/snapshot', '--candidate', candidate,
                '--evidence', out / ('A/evidence_' + mode)], 1 if mode == 'old' else 0))
            report = json.loads((out / ('A/evidence_' + mode) / 'report.json').read_bytes())
            if mode == 'old':
                require(report.get('methods') == 1 and report.get('failures') == 8 and report.get('errors') == 0,
                        'old metadata must fail in exactly eight subcases')
            if mode == 'preparation-tests':
                require(report.get('methods') == 14 and report.get('failures') == 0 and report.get('errors') == 0,
                        'preparation fourteen')
        target = stage_b(source, candidate, out / 'B', package['source_pin'])
        summary['B_integrity'] = verify_b(target)
        records.append(invoke(target, out, 'B_validate8', [target / 'scripts/mixer_e0_reseal_bundle.py',
                              '--validate-assets', target]))
        if a.mode == 'linux-checks':
            suites = [('self170', 'scripts/test_mixer_self170_canaries.py', []),
                      ('smoke_blind', SMOKE, ['--selftest']),
                      ('observer', 'scripts/test_mixer_precal_observe.py', [])]
            suites += [(n, F8 + '/' + p, []) for n, p in (
                ('submit10', 'test_submit_draft.py'), ('boundaries14', 'test_mla_boundaries.py'),
                ('jobstart8', 'test_job_start_draft.py'), ('prepare_only1', 'test_prepare_only.py'))]
            for label, script, args in suites:
                records.append(invoke(target, out, label, [target / script, *args]))
        require(package_check(source) == package, 'input package changed')
        verify_b(target)
        summary.update(status='AB_READY_FOR_AUTHOR_REVIEW' if a.mode == 'linux-checks' else 'ASSEMBLED_LINUX_CHECKS_NOT_RUN',
                       metadata_cases=8, unchanged_decks=8, unchanged_stls=24,
                       linux_checks_completed=a.mode == 'linux-checks',
                       IN_record_scope='A only, pre-reseal; do not rerun IN against B')
    finally:
        put(out / 'RECEIPT.json', encode(summary))
    print(json.dumps({k:v for k,v in summary.items() if k != 'checks'}, ensure_ascii=False))
    return 0


def validate_assets(target):
    sys.path.insert(0, str(target / 'scripts'))
    import mixer_precal_prepare as prep
    passed = []
    for cid in CASES:
        p = target / F8 / 'planned_assets' / cid
        prep.validate_case(cid, (p / 'in.mixer').read_bytes(), json.loads((p / 'deck_meta.json').read_bytes()))
        passed.append(cid)
    # The old E0 metadata must fail with the current generator.
    # Original metadata is recorded separately in the A snapshot, not guessed from paths.
    old = target.parent / 'A/snapshot' / F8 / 'planned_assets/PRECAL_E0/deck_meta.json'
    try:
        p = target / F8 / 'planned_assets/PRECAL_E0'
        prep.validate_case('PRECAL_E0', (p / 'in.mixer').read_bytes(), json.loads(old.read_bytes()))
    except ValueError:
        pass
    else:
        raise ValueError('old E0 metadata unexpectedly accepted')
    print(json.dumps(dict(validate_case_pass=passed, old_e0_metadata_rejected=True)))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--validate-assets':
        validate_assets(Path(sys.argv[2]).resolve())
    else:
        raise SystemExit(main())
