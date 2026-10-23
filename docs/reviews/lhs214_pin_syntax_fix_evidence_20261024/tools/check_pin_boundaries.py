#!/usr/bin/env python3
"""Assert six receipt SHA boundaries using the existing synthetic selftest fixture.

Runs no production batch. The fixture's source pin is synthetic, not a B7 approval.
Use a new --out directory; the repository is read as the source of all checks.
"""
import argparse
import contextlib
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    repo = args.repo.expanduser().resolve(strict=True)
    out = args.out.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=False)
    sys.path.insert(0, str(repo / 'scripts'))
    import supp20_input_receipt as receipt
    import run_network_194_parallel as runner

    original = runner.preflight_receipt_checks
    results = {}
    expected = {
        'normal': [],
        'trailing_LF': ['P7', 'P10'],
        'trailing_CRLF': ['P7', 'P10'],
        'wrong_last_digit': ['P10'],
        'trailing_space': ['P7', 'P10'],
        'trailing_NUL': ['P7', 'P10'],
    }

    def wrapped(path, *a, **kw):
        initial = original(path, *a, **kw)
        if results or not initial.get('checks') or not all(c['ok'] for c in initial['checks']):
            return initial
        p = Path(path)
        before = p.read_bytes()
        rec = json.loads(before)
        pin = rec['git']['sha']
        assert len(pin) == 40
        cases = {
            'normal': pin,
            'trailing_LF': pin + '\n',
            'trailing_CRLF': pin + '\r\n',
            'wrong_last_digit': pin[:-1] + ('0' if pin[-1] != '0' else '1'),
            'trailing_space': pin + ' ',
            'trailing_NUL': pin + '\x00',
        }
        (out / 'synthetic_preflight.log').write_bytes(Path(initial['log']['path']).read_bytes())
        try:
            for name, value in cases.items():
                rec['git']['sha'] = value
                p.write_text(json.dumps(rec), encoding='utf-8')
                actual = original(p, expect_set='supp20', approved_sha=pin)
                bad = [c['id'] for c in actual['checks'] if not c['ok']]
                results[name] = {
                    'git_sha': value,
                    'approved_sha': pin,
                    'expected_bad': expected[name],
                    'actual_bad': bad,
                    'ok': bad == expected[name],
                    'checks': actual['checks'],
                }
        finally:
            p.write_bytes(before)
        return initial

    runner.preflight_receipt_checks = wrapped
    try:
        with (out / 'receipt_selftest.log').open('w', encoding='utf-8') as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                receipt_rc = receipt._selftest()
    finally:
        runner.preflight_receipt_checks = original
    assert set(results) == set(expected), 'The existing positive fixture was not observed.'
    (out / 'boundaries.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    failed = [name for name, value in results.items() if not value['ok']]
    summary = {
        'scope': 'Local synthetic preflight and launch regressions; not WSL, B7, external GO, or a production run.',
        'runner_sha256': hashlib.sha256((repo / 'scripts/run_network_194_parallel.py').read_bytes()).hexdigest(),
        'receipt_sha256': hashlib.sha256((repo / 'scripts/supp20_input_receipt.py').read_bytes()).hexdigest(),
        'code_fp': runner.code_fp(runner.code_hashes()),
        'code_files': len(runner.CODE_FILES),
        'receipt_selftest_rc': receipt_rc,
        'receipt_selftest_last_line': (out / 'receipt_selftest.log').read_text(encoding='utf-8').splitlines()[-1],
        'boundary_cases': len(results),
        'failed_boundaries': failed,
        'test_rc': int(receipt_rc != 0 or bool(failed)),
    }
    (out / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary['test_rc']


if __name__ == '__main__':
    raise SystemExit(main())
