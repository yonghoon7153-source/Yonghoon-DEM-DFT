#!/usr/bin/env python3
"""Reproduce the independent review's unchanged 12-case restore/UB probe.

This wrapper adds portable kit selection, provenance and explicit assertions.
The probe inputs and CLI calls remain in independent_restore_probe_original.py.
This is implementer reproduction, not a new independent review.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
from evidence_support import hashes, mirror, paths, provenance, save


def main():
    a = paths(__doc__)
    prov = provenance(a)
    work, _ = mirror(a)
    probe = Path(__file__).with_name('independent_restore_probe_original.py')
    prov['independent_probe_sha256'] = hashlib.sha256(probe.read_bytes()).hexdigest()
    command = [sys.executable, str(probe), '--repo', str(work), '--out', str(a.out / 'probe')]
    pr = subprocess.run(command, capture_output=True, text=True, timeout=600)
    (a.out / 'probe.log').write_text(pr.stdout + pr.stderr)
    raw = a.out / 'probe/restore_probe.json'
    rows = json.loads(raw.read_text()) if raw.exists() else []
    expected = {
        'baseline': ('RESTORED', 'PASS', 'PASS', 0),
        'nan_box': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'short_box': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'no_bounds': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'bad_atoms_header': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'g2c_wrong_step': ('VALUE_MISMATCH', 'PASS', 'FAIL', 2),
        'missing_c26': ('UNCONFIRMED', 'PASS', 'NOT_COMPUTED', 2),
        'g2_duplicate_id': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'g2_nan': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'g2_extra_short_row': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'g2_both_wrong_step': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
        'g2_numeric_equal_token': ('VALUE_MISMATCH', 'FAIL', 'PASS', 2),
    }
    checks = []
    for r in rows:
        observed = (r['status'], r['G2']['status'], r['G2c']['status'], r['restore_rc'])
        want = expected.get(r['case'])
        logs = [(a.out / 'probe' / r['case'] / n).read_text() for n in ('cli.log', 'gate.log')]
        passed = want is not None and observed == want and r['gate_rc'] == want[3] and not any('Traceback (most recent call last)' in t for t in logs)
        checks.append({'case': r['case'], 'observed': observed, 'expected': want, 'gate_rc': r['gate_rc'], 'passed': passed})
        print(f'{r["case"]}: {r["status"]} restore_rc={r["restore_rc"]} gate_rc={r["gate_rc"]} expected={passed}', flush=True)
    complete = len(rows) == len(expected) and {r['case'] for r in rows} == set(expected)
    unchanged = hashes(a.kit) == prov['source_sha256']
    passed = pr.returncode == 0 and complete and unchanged and all(r['passed'] for r in checks)
    save(a.out / 'results.json', {'provenance': prov, 'probe_command': command, 'probe_rc': pr.returncode,
                               'source_unchanged': unchanged, 'complete': complete, 'cases': checks, 'passed': passed})
    shutil.rmtree(work)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
