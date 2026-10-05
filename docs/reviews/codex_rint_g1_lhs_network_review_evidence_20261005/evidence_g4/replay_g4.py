"""Bounded read-only replay: hashes, exact CLI, then committed CSV G4 checks.

CSV checks use recorded producer n_SE and unrounded inp.r_SE, except lhs130
also compares n_SE against separately committed harvest phase_counts. This is
not a DEM-dump replay or a complete 194-row build_handover reproduction.
"""
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
OUT = ROOT / 'evidence_g4'
sys.path.insert(0, str(SOURCE / 'scripts'))
import lhs_design_dataset as lhs


def main():
    manifest = json.loads((OUT / 'acquisition_manifest.json').read_text(encoding='utf-8'))
    verification = []
    for item in manifest['files']:
        p = SOURCE / item['path']
        raw = p.read_bytes()
        actual = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        verification.append(dict(path=item['path'], expected=item['git_blob_sha1'], actual=actual,
                                 matches=actual == item['git_blob_sha1'], bytes=len(raw)))
    (OUT / 'acquisition_verified.json').write_text(json.dumps(verification, indent=2), encoding='utf-8')
    print('Git blob hashes:', sum(r['matches'] for r in verification), '/', len(verification))
    if not all(r['matches'] for r in verification):
        print(json.dumps([r for r in verification if not r['matches']], indent=2))
        return 2
    cli = []
    for name, args in [('selftest', ['scripts/lhs_design_dataset.py', '--selftest']),
                       ('labels', ['webapp/test_s567_labels.py'])]:
        t0 = time.perf_counter()
        p = subprocess.run([sys.executable, '-u', *args], cwd=SOURCE, capture_output=True,
                           text=True, encoding='utf-8')
        elapsed = time.perf_counter() - t0
        (OUT / (name + '.cli.stdout.txt')).write_text(p.stdout, encoding='utf-8')
        (OUT / (name + '.cli.stderr.txt')).write_text(p.stderr, encoding='utf-8')
        cli.append(dict(name=name, args=args, exit=p.returncode, seconds=elapsed))
        print(name, p.returncode, elapsed, p.stdout.splitlines()[-1:])
    (OUT / 'cli_metadata.json').write_text(json.dumps(cli, indent=2), encoding='utf-8')
    cohorts = []
    for prefix in ('lhs', 'lhsx'):
        path = SOURCE / 'docs/data' / f'{prefix}_webapp_contact_d1ec42fba/metrics_flat.csv'
        with path.open(encoding='utf-8-sig', newline='') as f:
            rawrows = list(csv.DictReader(f))
        counter = Counter()
        failures = []
        maxima = Counter()
        for row in rawrows:
            case = row['case']
            nse = int(row['n_SE'])
            rse = float(row['inp.r_SE']) * 1e6 / float(row['meta.scale'])
            h = {'phase_counts': {'SE': nse}}
            if prefix == 'lhs':
                h = json.loads((SOURCE / 'docs/data/lhs_descriptors_20260925' / (case + '.json')).read_text(encoding='utf-8'))
                counter['n_SE_matches_harvest'] += h['phase_counts']['SE'] == nse
            rep = Counter()
            try:
                normalized = lhs._wa_area_prep(case, row, rep)
                checks = (lhs._wa_f1_gates(case, normalized, h), lhs._wa_frac_gates(case, normalized),
                          lhs._wa_area_gates(case, normalized, h, {'r_SE_um': rse}, list(normalized)))
                if checks != (1, 1, 1):
                    failures.append(dict(case=case, skipped=checks))
                else:
                    counter['g4_gate_pass'] += 1
            except Exception as error:
                failures.append(dict(case=case, error=repr(error)))
            counter['nonpercolating'] += float(row['percolation_pct']) == 0
            nt = int(row['n_total_AM_AM_force'])
            counter['force_total_equals_contacts'] += nt == int(row['am_am_n_contacts'])
            for stage in lhs.FRAC_STAGES:
                maxima['frac_pct_abs_error'] = max(maxima['frac_pct_abs_error'], abs(float(row[f'frac_{stage}_force_pct']) - 100 * int(row[f'n_{stage}_force_AM_AM']) / nt))
            fi = (int(row['n_fragmentation_force_AM_AM']) + int(row['n_pulverization_force_AM_AM'])) / nt
            maxima['fracture_index_abs_error'] = max(maxima['fracture_index_abs_error'], abs(float(row['fracture_index_force']) - fi))
            expected = float(row['se_se_cn']) + 2 * int(row['se_se_cn_aug_n_extra']) / nse
            maxima['F1_relative_error'] = max(maxima['F1_relative_error'], abs(float(row['se_se_cn_aug']) - expected) / max(1, abs(expected)))
            expected = 2 * float(row['area_SE_SE_total']) / (nse * 4 * math.pi * rse * rse)
            maxima['A4_relative_error'] = max(maxima['A4_relative_error'], abs(float(row['se_se_cn_eff_area']) - expected) / abs(expected))
            for k, v in row.items():
                if lhs.wa_group_f1(k) or lhs.wa_group_frac(k) or lhs.wa_group_area(k):
                    if v not in (None, '') and not math.isfinite(float(v)):
                        counter['nonfinite_g4_values'] += 1
                if k.startswith('area_') and k.endswith('_n') and v not in (None, '') and float(v) == 0:
                    counter['explicit_zero_contact_pairs'] += 1
            counter.update(rep)
        cohorts.append(dict(cohort=prefix, rows=len(rawrows), counters=dict(counter), max_errors=dict(maxima), failures=failures))
    result = dict(commit=manifest['commit'], cohorts=cohorts,
                  scope='Committed metrics CSV consistency, not raw dump replay. lhs130 n_SE additionally checked against harvested JSON; lhsx64 n_SE from producer CSV. No whole-194 build_handover claim.')
    (OUT / 'committed_194_g4_checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))
    return int(any(r['failures'] for r in cohorts) or any(r['exit'] for r in cli))


if __name__ == '__main__':
    sys.exit(main())
