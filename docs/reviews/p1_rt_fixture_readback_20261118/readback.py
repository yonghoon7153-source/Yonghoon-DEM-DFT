"""Read fixed fixture files in their original location and emit a separate decision."""
import hashlib
import json
from pathlib import Path
import re
import sys


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_inputs(work, expected):
    for name, wanted in expected.items():
        path = work / name
        if path.resolve(strict=True) != path or not path.is_file():
            raise ValueError('unexpected input path: ' + name)
        if digest(path.read_bytes()) != wanted:
            raise ValueError('input digest differs: ' + name)


def inspect(site, evidence, reader, release):
    root = site.resolve(strict=True)
    work = root / 'work'
    run = work / 'fixture'
    if (root / 'SOURCE_PIN').read_text().strip() != evidence['source_pin']:
        raise ValueError('wrong source pin')
    submitted = (root / 'submission.txt').read_text().strip()
    if re.fullmatch(re.escape(evidence['job']) + r'(?:;[^;\s]+)?', submitted) is None:
        raise ValueError('wrong submission receipt')
    verify_inputs(work, evidence['files'])
    manifest = (run / 'run_manifest.txt').read_text().splitlines()
    if [v for v in manifest if v.startswith('job_id=')] != ['job_id=' + evidence['job']]:
        raise ValueError('wrong job in fixture manifest')
    original = json.loads((run / 'rt_grammar_verdict.json').read_bytes())
    mod = {'__name__': 'pinned_development_reader'}
    exec(compile(reader, '<readback-reader>', 'exec'), mod)
    current = mod['evaluate_fixture'](run)
    verify_inputs(work, evidence['files'])
    checks = current['checks']
    passed = (current['status'] == 'PASS' and current['exit_code'] == 0
              and len(checks) == 20 and all(x is True for x in checks.values()))
    return dict(schema='rt_fixture_original_path_readback/1', job=evidence['job'],
                source_pin=evidence['source_pin'], readback_pin=release,
                reader_sha256=digest(reader), original_verdict=original['status'],
                original_reader_rc=original['exit_code'], original_checks=original['checks'],
                inputs_verified_before_after=len(evidence['files']),
                checks=checks, numeric_status=current['numeric']['status'],
                binding_status=current['binding']['status'], reader_rc=current['exit_code'],
                status='PASS' if passed else 'FAIL', physical_qualification=False)


def main(evidence, reader, release):
    expected = evidence['source_pin']
    root = Path.home() / ('rt_fixture_np6_1118_' + expected[:12])
    try:
        result = inspect(root, evidence, reader, release)
    except (OSError, ValueError, KeyError, UnicodeError) as error:
        print(json.dumps(dict(status='READBACK_INCOMPLETE', job=evidence['job'],
                              error=str(error), readback_pin=release)))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return 0 if result['status'] == 'PASS' else 2
