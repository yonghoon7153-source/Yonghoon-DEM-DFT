#!/usr/bin/env python3
"""Run final kit baselines and ten dump/restore mutations with full selftests.

Source files are never edited. A mutant is killed only by an anticipated
behavioral test failure, with no exception-shaped failures or unrelated tests.
"""
import re
import shutil
import subprocess
import sys
import time
from evidence_support import hashes, mirror, paths, provenance, save


def main():
    a = paths(__doc__)
    prov = provenance(a)
    work, kit = mirror(a)
    texts = {n: (kit / n).read_text() for n in ('ul_gates.py', 'ul_reader.py')}
    # Each tuple gives the one production edit and the allowed failed-test names.
    jobs = [
        ('box_finite', 'ul_gates.py', 'elif any(not math.isfinite(v) for axis in box for v in axis):', 'elif False:',
         r'C6 .*axis[012]_end[01]_(?:nan|-?inf)|C7 .*box_nonfinite'),
        ('box_order', 'ul_gates.py', 'elif any(lo >= hi for lo, hi in box):', 'elif False:',
         r'C6 .*reversed_bound|C6 .*zero_width|C7 .*box_reversed|C7 .*box_zero_width'),
        ('box_two_values', 'ul_gates.py', 'any(len(ln.split()) != 2 for ln in bounds)', 'False',
         r'C6 .*extra_bound|C7 .*box_extra'),
        ('exact_header_names', 'ul_gates.py',
         "if lines[kb].split()[:3] != ['ITEM:', 'BOX', 'BOUNDS'] or lines[kh].split()[:2] != head.split():", 'if False:',
         r'C[67] .*(?:box|atom|entries)_header_prefix'),
        ('g2_header_guard', 'ul_gates.py', "header_problems = _dump_header_problems(d, 'custom', lines)", 'header_problems = []',
         r'C6 ULPR-03 G2 (?:test|orig|both) '),
        ('g2c_header_guard', 'ul_gates.py', "header_problems = _dump_header_problems(d, 'local')", 'header_problems = []',
         r'C7 G2c (?:test|orig|both) (?:box_|entries_header_prefix)'),
        ('g2c_same_step', 'ul_gates.py',
         "if dt['step'] != do['step'] or (expected_step is not None and dt['step'] != expected_step):",
         "if False or (expected_step is not None and dt['step'] != expected_step):", r'C7 G2c (?:test|orig) 다른 TIMESTEP'),
        ('g2c_expected_step', 'ul_gates.py',
         "if dt['step'] != do['step'] or (expected_step is not None and dt['step'] != expected_step):",
         "if dt['step'] != do['step']:", r'C7 G2c 양쪽 같은 S0 \+ 1'),
        ('restore_g2c_expected_binding', 'ul_reader.py', 'ul_gates.g2c_compare(g2c, orig_con, expected_step=s0)',
         'ul_gates.g2c_compare(g2c, orig_con)', r'R35 G2c 시점 결합 g2c_both_wrong_step'),
        ('gravity_g2c_expected_binding', 'ul_reader.py', "f'contact_{rm}.dump'), expected_step=rm)",
         "f'contact_{rm}.dump'))", r'R16 중력 팔과 출처 G2c 머리가 같은 R_M \+ 1'),
    ]
    results = []

    def run(name, filename, candidate, allowed=None):
        for n, txt in texts.items():
            (kit / n).write_text(txt)
        (kit / filename).write_text(candidate)
        for cache in kit.rglob('__pycache__'):
            shutil.rmtree(cache)
        command = [sys.executable, '-B', '-I', str(kit / filename), '--selftest']
        began = time.monotonic()
        pr = subprocess.run(command, capture_output=True, text=True, timeout=600)
        log = pr.stdout + pr.stderr
        (a.out / (name + '.log')).write_text(log)
        failures = [line for line in log.splitlines() if line.startswith('  ✗ ')]
        exception_failures = [line for line in failures if re.search(r'\b(?:\w*Error|\w*Exception):', line)]
        unexpected = [line for line in failures if allowed is not None and not re.search(allowed, line)]
        clean = 'Traceback (most recent call last)' not in log and not exception_failures
        if allowed is None:
            passed = pr.returncode == 0 and not failures and 'selftest: PASS (0 실패)' in log and clean
        else:
            passed = pr.returncode == 1 and bool(failures) and not unexpected and clean and 'selftest: FAIL (' in log
        result = {'name': name, 'file': filename, 'command': command, 'rc': pr.returncode,
                  'checks': log.count('  ✓ ') + len(failures), 'failures': failures,
                  'allowed_failure_pattern': allowed, 'unexpected_failures': unexpected,
                  'exception_failures': exception_failures, 'passed': passed,
                  'seconds': round(time.monotonic() - began, 3)}
        results.append(result)
        print(f'{name}: rc={pr.returncode} checks={result["checks"]} failed={len(failures)} expected={passed}', flush=True)

    for filename in texts:
        run('baseline-' + filename[:-3], filename, texts[filename])
    if not all(r['passed'] for r in results):
        save(a.out / 'results.json', {'provenance': prov, 'runs': results, 'passed': False})
        return 1
    for name, filename, old, new, pattern in jobs:
        if texts[filename].count(old) != 1:
            raise RuntimeError(f'{name}: expected one mutation anchor, got {texts[filename].count(old)}')
        run(name, filename, texts[filename].replace(old, new, 1), pattern)
    unchanged = hashes(a.kit) == prov['source_sha256']
    passed = unchanged and all(r['passed'] for r in results)
    save(a.out / 'results.json', {'provenance': prov, 'source_unchanged': unchanged, 'runs': results, 'passed': passed})
    # Preserve source, logs, edits and hashes; discard only this runner's scratch mirror.
    shutil.rmtree(work)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
