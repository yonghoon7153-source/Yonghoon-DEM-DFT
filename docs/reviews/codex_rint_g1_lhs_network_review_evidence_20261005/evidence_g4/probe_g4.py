"""Read-only production-function audit. Only outputs under evidence_g4 are written."""
import contextlib
import copy
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
OUT = ROOT / 'evidence_g4'
sys.path.insert(0, str(SOURCE / 'scripts'))
import lhs_design_dataset as lhs

CAPTURE = {}


def profile(frame, event, arg):
    if event == 'return' and frame.f_code is lhs._selftest.__code__:
        CAPTURE.update(frame.f_locals)


def full_handover(name, mutate=None, groups='f1,fracture,area', reviewed=True, design_mutate=None):
    w = CAPTURE['_wa11']()
    h = CAPTURE['_hq10']()
    d = copy.deepcopy(CAPTURE['_dq11'])
    if mutate:
        mutate(w)
    if design_mutate:
        design_mutate(d)
    try:
        rows, cols, rep = lhs.build_handover(d, h, webapp=w, webapp_groups=groups, wa_reviewed_only=reviewed)
        result = dict(name=name, accepted=True,
                      output={r['case_id']: {k: v for k, v in r.items()
                              if lhs.wa_group_f1(k) or lhs.wa_group_frac(k) or lhs.wa_group_area(k)
                              or k.startswith('area_')} for r in rows},
                      gate_counts={k: v for k, v in rep.items() if k.startswith('wa_')}, columns=cols)
    except Exception as error:
        result = dict(name=name, accepted=False, exception=type(error).__name__, reason=str(error))
    print(f'{name}: accepted={result["accepted"]}' + (' ' + result.get('reason', '')[:180]), flush=True)
    return result


def run():
    meta = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=sys.version,
                numpy=np.__version__, platform=platform.platform(),
                sha256={str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in [SOURCE / 'scripts/lhs_design_dataset.py', SOURCE / 'webapp/test_s567_labels.py']})
    if '--fixtures-only' in sys.argv:
        raise SystemExit('Use the stored fixture JSON for later replays; this first harness captures the unmodified selftest.')
    log = io.StringIO()
    start = time.perf_counter()
    sys.setprofile(profile)
    try:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            rc = lhs._selftest()
    except Exception:
        rc = 99
        traceback.print_exc(file=log)
    finally:
        sys.setprofile(None)
    meta['selftest'] = dict(exit=rc, seconds=time.perf_counter()-start)
    (OUT / 'lhs_selftest.stdout.txt').write_text(log.getvalue(), encoding='utf-8')
    print('lhs_selftest', meta['selftest'], log.getvalue().splitlines()[-1:], flush=True)
    start = time.perf_counter()
    r = subprocess.run([sys.executable, '-u', str(SOURCE / 'webapp/test_s567_labels.py')],
                       cwd=SOURCE, capture_output=True, text=True, encoding='utf-8', errors='replace')
    meta['labels'] = dict(exit=r.returncode, seconds=time.perf_counter()-start)
    (OUT / 'labels.stdout.txt').write_text(r.stdout, encoding='utf-8')
    (OUT / 'labels.stderr.txt').write_text(r.stderr, encoding='utf-8')
    print('labels', meta['labels'], r.stdout.splitlines()[-1:], flush=True)
    (OUT / 'metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
    if '_wa11' not in CAPTURE:
        raise RuntimeError('Selftest did not reach G4 fixture definitions')
    fixtures = dict(design=CAPTURE['_dq11'], harvest=CAPTURE['_hq10'](), webapp=CAPTURE['_wa11']())
    (OUT / 'baseline_fixture.json').write_text(json.dumps(fixtures, ensure_ascii=False, indent=2), encoding='utf-8')
    results = []
    def add(name, mut=None, **kw):
        results.append(full_handover(name, mut, **kw))
    def update(case='q1', **fields):
        return lambda w: w['rows'][case].update(fields)
    def remove(*keys, case='q1'):
        return lambda w: [w['rows'][case].pop(k, None) for k in keys]
    add('baseline_all_groups', groups='contact,percolation,f1,fracture,area')
    add('baseline_g4_groups')
    add('network_stage_contact_groups', lambda w: w.update(stop_after='network'))
    add('fraction_pct_nan', update(frac_intact_force_pct='nan'))
    add('fracture_index_nan', update(fracture_index_force='nan'))
    add('area_positive_count_nan_mean', update(area_AM_S_AM_S_mean='nan'))
    add('area_nan_total', update(area_AM_S_AM_S_total='nan', am_am_total_area='nan', am_am_mean_area='nan'))
    add('f1_h_infinity', update(se_se_cn_aug_h_spread_sim='inf'))
    add('f1_std_negative', update(se_se_cn_aug_std='-1'))
    add('f1_std_missing', remove('se_se_cn_aug_std'))
    add('f1_missing_cn', remove('se_se_cn'), groups='f1')
    def f1_missing_cn_corrupt_aug(w):
        w['rows']['q1'].pop('se_se_cn')
        w['rows']['q1']['se_se_cn_aug'] = '-999'
    add('f1_missing_cn_corrupt_aug', f1_missing_cn_corrupt_aug, groups='f1')
    add('fracture_missing_am_total', remove('am_am_n_contacts'), groups='fracture')
    add('area_missing_percolation', remove('percolation_pct'), groups='area')
    def area_missing_pp_corrupt_eap(w):
        w['rows']['q2'].pop('percolation_pct')
        w['rows']['q2']['se_se_cn_eff_area_perc'] = '0.4'
    add('area_missing_pp_corrupt_eap', area_missing_pp_corrupt_eap, groups='area')
    add('area_missing_global_eff', remove('se_se_cn_eff_area'), groups='area')
    add('area_perc_nan', update(se_se_cn_eff_area_perc='nan'), groups='area')
    add('area_perc_negative', update(se_se_cn_eff_area_perc='-1'), groups='area')
    add('area_missing_am_total', remove('am_am_total_area'), groups='area')
    add('area_missing_am_mean', remove('am_am_mean_area'), groups='area')
    def absent_zero_count_with_positive_mean(w):
        q = w['rows']['q2']
        q.pop('area_AM_P_AM_P_n', None)
        q['area_AM_P_AM_P_mean'] = '0.01'
    add('missing_pair_count_positive_mean', absent_zero_count_with_positive_mean,
        groups='contact,percolation,f1,fracture,area')
    def absent_all_pair_keys(w):
        q = w['rows']['q2']
        for k in ('area_AM_P_AM_P_n', 'area_AM_P_AM_P_mean', 'area_AM_P_AM_P_total'):
            q.pop(k, None)
    add('zero_pair_all_keys_missing', absent_all_pair_keys)
    add('explicit_zero_pair_mean_zero', update('q2', area_AM_P_AM_P_mean='0'))
    add('explicit_zero_pair_mean_positive', update('q2', area_AM_P_AM_P_mean='0.01'))
    # Physical admissibility is separate from the rounding interval.
    add('pct_negative_inside_tolerance', update(frac_pulverization_force_pct='-0.004'))
    add('fi_negative_inside_tolerance', update('q2', **dict(CAPTURE['_frf']([22,0,0,0,0]), fracture_index_force='-0.00004')))
    p_exact = 600/11
    fi_exact = 1/11
    for delta in (0.004999, 0.005, 0.005001):
        add(f'pct_boundary_{delta}', update(frac_intact_force_pct=repr(p_exact+delta)))
    for delta in (4.999e-5, 5e-5, 5.001e-5):
        add(f'fi_boundary_{delta}', update(fracture_index_force=repr(fi_exact+delta)))
    # Existing zero-pair policy positive controls and exclusions with all census rows approved.
    add('exclusion_even_unreviewed', reviewed=False, groups='contact,percolation,f1,fracture,area')
    excluded = {k: lhs.wa_excluded(k) for k in CAPTURE['_wa11']()['verdict'] if lhs.wa_excluded(k)}
    report = dict(results=results, excluded=excluded, note='Synthetic actual-function probes; not raw 194-case corroboration.')
    (OUT / 'probe_results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    console = io.StringIO()
    try:
        with contextlib.redirect_stdout(console):
            run()
    finally:
        transcript = console.getvalue()
        (OUT / 'probe.stdout.txt').write_text(transcript, encoding='utf-8')
        print(transcript, end='')
