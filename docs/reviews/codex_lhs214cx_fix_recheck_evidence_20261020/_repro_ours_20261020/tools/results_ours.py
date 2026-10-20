"""Collect our reproduction outputs into one comparison JSON (read only).

usage: python3 -I results_ours.py <repro_dir> <bundle_root> <out_json>
"""
import json
import platform
import sys
from pathlib import Path


def j(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))


def main():
    rp, bx, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    import numpy
    import scipy
    env = dict(platform=platform.platform(), python=sys.version.split()[0], numpy=numpy.__version__,
               scipy=scipy.__version__, markdown_it='not installed', threads='OMP/OpenBLAS/MKL/NumExpr = 1',
               cpu='4 vCPU container')
    cx = bx / 'evidence'
    res = dict(environment_ours=env, environment_codex='Windows 11 build 26200 · Python 3.12.14 · NumPy 2.5.3 · SciPy 1.16.3 · markdown-it-py 3.0.0',
               rows=[])

    def row(item, codex, ours, verdict, note=''):
        res['rows'].append(dict(item=item, codex=codex, ours=ours, verdict=verdict, note=note))

    cb = j(rp / 'out/current_boundary.json')
    row('boundary test 34713ac96 (unmodified)', '40/40 rc0 (9.33 s)',
        f"{cb['stdout_tail'][-1]} rc{cb['returncode']} ({cb['seconds']} s)", 'same')
    bb = j(rp / 'out/baseline_boundary.json')
    row('boundary test 685c2bbdb (unmodified source, run in our tree)', '23/29 rc1 (Windows original)',
        f"{bb['stdout_tail'][-1]} rc{bb['returncode']}", 'differs (environment)',
        'E0-E4 + E-prime all pass here; Windows collapses E-prime into one FAIL (29 vs 30 checks)')
    rs = j(rp / 'out/current_receipt_selftest.json')
    row('receipt selftest 34713ac96 (no adapter)', '109/122 rc1 original · 122/122 with adapter',
        f"{rs['stdout_tail'][-1]} rc{rs['returncode']} ({rs['seconds']} s)", 'differs (environment)',
        'the 13 Windows failures (S7 family, S11d2, S11f2, S12a2, S12c2) pass here: system dist-packages scipy is visible to the python -I generation child')
    ar = j(rp / 'out/actual_receipt_ours.json')
    row('actual supp20 registration receipt', 'rc1 · only D1 · values equal old/new',
        f"rc{ar['rc']} · bad {[c['id'] for c in ar['checks'] if not c['ok']]}", 'same',
        'checks + registration values equal all four Codex receipts')
    for mode in ('core', 'axis', 'mutants', 'failclosed'):
        o, c = j(rp / f's02_probe/{mode}.json'), j(cx / f's02/{mode}.json')
        diff = [x['name'] for x, y in zip(o['checks'], c['checks']) if x['ok'] != y['ok']]
        row(f'S02 probe {mode}', f"{c['summary']['passed']}/{c['summary']['total']}",
            f"{o['summary']['passed']}/{o['summary']['total']}",
            'same' if not diff else 'differs (environment)', '; '.join(diff))
    row('S02 probe sweep (start area ±200 ULP, 401)', '401/401 · second axis 251 · max 9 ULP · max 19 tries',
        'not run', 'not reproduced (time, brief)',
        'our container figure from the 10-19 S02 fix evidence: 401/401 · 278 · 14 ULP')
    core = j(rp / 's02_probe/core.json')
    for lab, s in core['starts'].items():
        se = s['search']
        res.setdefault('search_ours', {})[lab] = dict(
            start_area=s['start_area'], one_axis_missing=sorted(s['one_axis']['problems']),
            success_area=se.get('area'), k=se.get('k'), tries=len(se.get('tried', [])),
            boundary=dict((k, dict(box_y=r['by'], raw_q=r['raw'], status=r['status'], stored_q=r['stored_q'],
                                   I_bottom=r['I_bottom'])) for k, r in s['records'].items()))
    mu = j(rp / 's02_probe/mutants.json')
    res['mutants_ours'] = {m['label']: dict(failed_E=m['failed'], e5_failed=m['e5']['failed']) for m in mu['mutations']}
    s6 = j(rp / 's06_nooracle.json')
    res['s06_nooracle'] = {k: {kk: vv for kk, vv in v.items() if kk not in ('rows',)} for k, v in s6['parts'].items()}
    res['s06_nooracle']['B_matrix_8736'].pop('receipts12', None)
    res['s06_nooracle']['receipts12'] = {k: v for k, v in s6['parts']['B_matrix_8736']['receipts12'].items() if k != 'rows'}
    res['scope_ours'] = j(rp / 'scope_ours.json')
    res['tree_cmp'] = j(rp / 'tree_cmp.json')
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    for r in res['rows']:
        print(r['verdict'], '|', r['item'], '|', r['codex'], '|', r['ours'], '|', r['note'][:150])


if __name__ == '__main__':
    main()
