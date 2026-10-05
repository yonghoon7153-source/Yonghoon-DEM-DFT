#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""194 인계 v1.2 다시 읽기 검산 (Codex 4차 §8-4) — 읽기 전용 · 계산 없음 (τ 는 원천 파일이 있으면 tau_flux 로 독립 재계산).

  python3 reread_v12.py --handover-dir <WSL 묶음을 푼 handover/> [--seal-audit <seal_audit.tsv>] [--tau-sources <τ 원천 묶음을 푼 ROOT>] --out reread.json

대조 원천 (리포 커밋본): 배치 증거 `docs/data/lhs_network194_11fcf91e8/merged/<c>/{metrics_flat.csv,status.json}` ·
옛 인계 (d1ec42fba 접촉 배치) `docs/data/{lhs,lhsx}_handover_20261001.csv` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/*_d1ec42fba/perc_audit.tsv` ·
봉인 지문 `manifest.json` code_hashes.
검사 (코호트마다):
  C1 행 집합 = metrics_flat 케이스 = 130 · 64 · 중복 없음
  C2 LW 열 없음 · 제외 노트에 LW = frame_unverified
  C3 열 사전 ↔ 표 열 (양쪽 같은 집합 · 뜻 빈칸 없음)
  C4 회귀 — 옛 인계와 공통 열 값 (문자열 같음 · 부동소수 상대 1e-12 안 · 그 밖 = 차이 열 목록) · 새 열 · 빠진 열
  C5 τ 묶음 — 모드별 상태 수 · NOT_COMPUTED 0 · OK/MBCB 값 = metrics_flat 로 다시 계산한 φ_mc / (σ_ratio · L_gap / L_mc) ·
     tau = √tau2 · OK ⇒ ≥ 1 · MBCB ⇒ < 1 · NOT_PERCOLATING ⇒ f = 0 · tau2 빈칸 · 비관통 집합 = 망 valid_zero = 퍼콜 감사 ·
     BAND_FALLBACK ⇒ 값 빈칸 · 띠 L1/L2 · 공통 메타 (σ₀ 3.0 · φ basis · L basis) · basis_check ok
  C6 τ 출처 부록 — 행 = 케이스 · network_run_id = 배치 status.json · tau_flux sha256 = 봉인 · 같은 세대 검사 목록 전부 · basis 문구
  C7 (선택 · --tau-sources) 원천 sha256 = 출처 부록 · tau_flux.ion_columns 독립 재계산 = 표 τ 칸 (전부)
  C8 (선택 · --seal-audit) 봉인 감사 = 194 전부 SEALED · SEALED_LEGACY (UNSEALED 0)
"""
import argparse
import csv
import glob
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..')) if 'docs' in HERE.split(os.sep) else os.environ.get('REPO', '/home/user/Yonghoon-DEM-DFT')
BATCH = os.path.join(REPO, 'docs', 'data', 'lhs_network194_11fcf91e8')
PREV = {'lhs': os.path.join(REPO, 'docs', 'data', 'lhs_handover_20261001.csv'),
        'lhsx': os.path.join(REPO, 'docs', 'data', 'lhsx_handover_20261001.csv')}
PERC = {'lhs': os.path.join(REPO, 'docs', 'data', 'lhs_perc_audit_20261001', 'lhs_20261001_d1ec42fba', 'perc_audit.tsv'),
        'lhsx': os.path.join(REPO, 'docs', 'data', 'lhs_perc_audit_20261001', 'lhsx_20261001_d1ec42fba', 'perc_audit.tsv')}
EXPECT_N = {'lhs': 130, 'lhsx': 64}
LW_RE = re.compile(r'stress_lw_.+|stress_cv_lw(_nowall)?|stress_ratio_.+_lw(_nowall)?')
MODES = ('hertz', 'physics')
DUAL = {'hertz': 'hertzian', 'physics': 'physics'}
CHECKS_FULL = 'P0_records;P1_run_id;P2_input_digest;P3_batch_tie;P4_stop_contract;P4_generation;P4_read_stable'
BASIS = 'current_files_no_publish_hash'
sys.path.insert(0, os.path.join(REPO, 'scripts'))


def num(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def read_csv(p, delim=','):
    with open(p, encoding='utf-8', newline='') as fh:
        return list(csv.DictReader(fh, delimiter=delim))


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rel(a, b):
    return 0.0 if a == b else abs(a - b) / max(abs(a), abs(b), 1e-300)


def same_cell(a, b, tol=1e-12):
    if a == b:
        return 'same'
    fa, fb = num(a), num(b)
    if fa is not None and fb is not None and rel(fa, fb) <= tol:
        return 'close'
    return 'diff'


def one(pattern):
    hits = sorted(glob.glob(pattern))
    return hits[-1] if hits else None


def cohort(coh, hdir, tau_root, out):
    res = {'cohort': coh, 'fail': []}
    F = res['fail']
    tab_p = one(os.path.join(hdir, f'{coh}_handover_v12_*[0-9].csv'))
    if not tab_p:
        F.append('인계표 파일 없음')
        out[coh] = res
        return
    base = tab_p[:-4]
    paths = {k: base + s for k, s in (('columns', '_columns.tsv'), ('prov', '_tau_provenance.tsv'), ('excluded', '_excluded.tsv'))}
    res['files'] = {'table': os.path.basename(tab_p), **{k: (os.path.basename(v) if os.path.exists(v) else None) for k, v in paths.items()},
                    'sha256': {os.path.basename(p): sha_file(p) for p in [tab_p, *paths.values()] if os.path.exists(p)}}
    tab = read_csv(tab_p)
    cols = list(tab[0].keys()) if tab else []
    res['shape'] = [len(tab), len(cols)]
    mf = {r['case']: r for r in read_csv(os.path.join(BATCH, 'merged', coh, 'metrics_flat.csv'))}
    st = json.load(open(os.path.join(BATCH, 'merged', coh, 'status.json'), encoding='utf-8'))['cases']
    # C1
    ids = [r['case_id'] for r in tab]
    c1 = {'n': len(ids), 'expect': EXPECT_N[coh], 'dups': len(ids) - len(set(ids)),
          'set_eq_metrics': set(ids) == set(mf), 'missing': sorted(set(mf) - set(ids))[:10], 'extra': sorted(set(ids) - set(mf))[:10]}
    res['C1_rows'] = c1
    if not (c1['n'] == c1['expect'] and c1['dups'] == 0 and c1['set_eq_metrics']):
        F.append('C1 행 집합')
    # C2
    lw_in = [c for c in cols if LW_RE.fullmatch(c)]
    exc = read_csv(paths['excluded'], '\t') if os.path.exists(paths['excluded']) else []
    exc_txt = json.dumps(exc, ensure_ascii=False)
    res['C2_lw'] = {'lw_cols_in_table': lw_in, 'excluded_rows': len(exc), 'frame_unverified_in_excluded': 'frame_unverified' in exc_txt}
    if lw_in or not res['C2_lw']['frame_unverified_in_excluded']:
        F.append('C2 LW')
    # C3
    d = read_csv(paths['columns'], '\t') if os.path.exists(paths['columns']) else []
    dcols = [r.get('column') for r in d]
    empty = [r.get('column') for r in d if not (r.get('meaning') or '').strip()]
    res['C3_dictionary'] = {'n': len(d), 'only_in_table': sorted(set(cols) - set(dcols))[:20], 'only_in_dict': sorted(set(dcols) - set(cols))[:20],
                            'empty_meaning': empty[:20]}
    if res['C3_dictionary']['only_in_table'] or res['C3_dictionary']['only_in_dict'] or empty:
        F.append('C3 열 사전')
    # C4 회귀
    prev = {r['case_id']: r for r in read_csv(PREV[coh])}
    pcols = list(next(iter(prev.values())).keys())
    common = [c for c in cols if c in pcols and c != 'case_id']
    tally, diffs = {'same': 0, 'close': 0, 'diff': 0}, {}
    for r in tab:
        p = prev.get(r['case_id'])
        if p is None:
            continue
        for c in common:
            k = same_cell(r[c], p[c])
            tally[k] += 1
            if k == 'diff':
                e = diffs.setdefault(c, {'n': 0, 'ex': []})
                e['n'] += 1
                if len(e['ex']) < 3:
                    e['ex'].append([r['case_id'], p[c], r[c]])
    res['C4_regression'] = {'common_cols': len(common), 'cells': tally, 'diff_cols': diffs,
                            'new_cols': [c for c in cols if c not in pcols], 'dropped_cols': [c for c in pcols if c not in cols]}
    # C5 τ
    pa = {r['case']: r for r in read_csv(PERC[coh], '\t') if r['case'].startswith('lhs')}
    nonperc_audit = {c for c, r in pa.items() if r['se_perc_webapp_dump'] != 'True'}
    t5 = {}
    for m in MODES:
        cnt, bad = {}, []
        for r in tab:
            s = r.get(f'ion_net_status_{m}', '')
            cnt[s] = cnt.get(s, 0) + 1
            f, fg, t2, t = (num(r.get(f'f_ion_{m}')), num(r.get(f'f_ion_{m}_gap')), num(r.get(f'tau2_ion_{m}')), num(r.get(f'tau_ion_{m}')))
            q = mf.get(r['case_id'], {})
            phi, Lg, Lm = num(q.get('phi_se_mass_conserving')), num(q.get('thickness_um')), num(q.get('thickness_mass_conserving_um'))
            sr = num(q.get(f'network_dual.{DUAL[m]}.sigma_full'))
            if s in ('OK', 'MODEL_BELOW_CONTINUUM_BOUND'):
                if None in (f, fg, t2, t, phi, Lg, Lm, sr):
                    bad.append([r['case_id'], s, 'value missing'])
                    continue
                f_re = sr * Lg / Lm
                t2_re = phi / f_re
                worst = max(rel(fg, sr), rel(f, f_re), rel(t2, t2_re), rel(t, math.sqrt(t2)))
                if worst > 1e-9:
                    bad.append([r['case_id'], s, f'recompute rel {worst:.3g}'])
                if (s == 'OK') != (t2 >= 1.0):
                    bad.append([r['case_id'], s, f'tau2 {t2} vs status'])
            elif s == 'NOT_PERCOLATING':
                if f != 0.0 or fg != 0.0 or r.get(f'tau2_ion_{m}', '') != '' or r.get(f'tau_ion_{m}', '') != '':
                    bad.append([r['case_id'], s, 'nonperc cells'])
                if q.get(f'network_dual.{DUAL[m]}.sigma_full_status') != 'valid_zero':
                    bad.append([r['case_id'], s, 'metrics status not valid_zero'])
            elif s == 'BAND_FALLBACK':
                if r.get(f'tau2_ion_{m}', '') != '' or r.get(f'ion_net_band_rule_{m}') not in ('L1', 'L2'):
                    bad.append([r['case_id'], s, 'band cells'])
            else:
                bad.append([r['case_id'], s, 'status not allowed in handover'])
            if r.get(f'ion_net_basis_check_{m}') != 'ok':
                bad.append([r['case_id'], s, f'basis_check {r.get(f"ion_net_basis_check_{m}")}'])
        np_tab = {r['case_id'] for r in tab if r.get(f'ion_net_status_{m}') == 'NOT_PERCOLATING'}
        np_mf = {c for c, q in mf.items() if q.get(f'network_dual.{DUAL[m]}.sigma_full_status') == 'valid_zero'}
        t5[m] = {'status_counts': cnt, 'not_computed': cnt.get('NOT_COMPUTED', 0), 'bad': bad[:20], 'n_bad': len(bad),
                 'nonperc_eq_metrics': np_tab == np_mf, 'nonperc_eq_perc_audit': np_tab == nonperc_audit, 'n_nonperc': len(np_tab)}
        if bad or cnt.get('NOT_COMPUTED', 0) or not (np_tab == np_mf == nonperc_audit):
            F.append(f'C5 τ {m}')
    shared = {k: sorted({r.get(k, '') for r in tab}) for k in ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis')}
    t5['shared'] = shared
    if shared['phi_basis'] != ['mass_conserving'] or shared['L_basis'] != ['L_mc'] or [num(x) for x in shared['ion_sigma0_mScm']] != [3.0]:
        F.append('C5 τ 공통 메타')
    res['C5_tau'] = t5
    # C6 출처 부록
    man = json.load(open(os.path.join(BATCH, 'manifest.json'), encoding='utf-8'))
    tf_seal = (man.get('code_hashes') or {}).get('scripts/tau_flux.py')
    prov = read_csv(paths['prov'], '\t') if os.path.exists(paths['prov']) else []
    pb = []
    for r in prov:
        c = r.get('case')
        if r.get('network_run_id') != (st.get(c) or {}).get('network_run_id'):
            pb.append([c, 'run_id'])
        if r.get('tau_flux_py_sha256') != tf_seal:
            pb.append([c, 'tau_flux sha'])
        if r.get('same_generation_checks') != CHECKS_FULL or r.get('same_generation_basis') != BASIS:
            pb.append([c, 'checks/basis'])
        if not r.get('atoms_csv_digest') or not r.get('contacts_csv_digest') or not r.get('dual_sha256') or not r.get('full_metrics_sha256'):
            pb.append([c, 'digest empty'])
    res['C6_provenance'] = {'n': len(prov), 'set_eq_table': {r.get('case') for r in prov} == set(ids), 'bad': pb[:20], 'n_bad': len(pb),
                            'tau_flux_seal': tf_seal}
    if pb or not res['C6_provenance']['set_eq_table']:
        F.append('C6 출처 부록')
    # C7 원천 독립 재계산
    if tau_root:
        import tau_flux
        cb, n_ok = [], 0
        provd = {r['case']: r for r in prov}
        tabd = {r['case_id']: r for r in tab}
        for c in ids:
            hits = glob.glob(os.path.join(tau_root, 'cases', c, 'work', 'results', '*', 'network_conductivity_dual.json'))
            if len(hits) != 1:
                cb.append([c, f'dual files {len(hits)}'])
                continue
            cdir = os.path.dirname(hits[0])
            fm_p = os.path.join(cdir, 'full_metrics.json')
            if sha_file(hits[0]) != provd.get(c, {}).get('dual_sha256') or sha_file(fm_p) != provd.get(c, {}).get('full_metrics_sha256'):
                cb.append([c, 'sha256 ≠ 출처 부록'])
            dual = json.load(open(hits[0], encoding='utf-8'))
            fm = json.load(open(fm_p, encoding='utf-8'))
            exp = tau_flux.ion_columns(dual, fm, fm.get('percolation_pct'))
            mism = [k for k, v in exp.items() if k in tabd[c] and same_cell(tau_flux._cell(v), tabd[c][k], tol=0) == 'diff']
            if mism:
                cb.append([c, f'cells {mism[:4]}'])
            else:
                n_ok += 1
        res['C7_sources'] = {'n_ok': n_ok, 'n_bad': len(cb), 'bad': cb[:20]}
        if cb:
            F.append('C7 원천 재계산')
    out[coh] = res


def main(argv=None):
    ap = argparse.ArgumentParser(description='194 인계 v1.2 다시 읽기 검산 (읽기 전용)')
    ap.add_argument('--handover-dir', required=True)
    ap.add_argument('--seal-audit', default='')
    ap.add_argument('--tau-sources', default='', help='τ 원천 묶음을 푼 ROOT (cases/<c>/work/results/<run>/…)')
    ap.add_argument('--out', default='')
    a = ap.parse_args(argv)
    out = {'repo': REPO, 'batch': BATCH}
    for coh in ('lhs', 'lhsx'):
        cohort(coh, a.handover_dir, a.tau_sources or None, out)
    if a.seal_audit:
        rows = read_csv(a.seal_audit, '\t')
        vk = next((k for k in (rows[0].keys() if rows else []) if k.lower() in ('verdict', '판정')), None)
        cnt = {}
        for r in rows:
            cnt[r.get(vk)] = cnt.get(r.get(vk), 0) + 1
        mcnt = {}
        for r in rows:
            mcnt[r.get('merged')] = mcnt.get(r.get('merged'), 0) + 1
        out['C8_seal_audit'] = {'n': len(rows), 'verdicts': cnt, 'merged': mcnt}
        if len(rows) != 194 or any(k not in ('SEALED', 'SEALED_LEGACY') for k in cnt) or set(mcnt) != {'same'}:
            out.setdefault('fail_global', []).append('C8 봉인 감사')
    fails = [f'{c}:{x}' for c in ('lhs', 'lhsx') for x in out[c]['fail']] + out.get('fail_global', [])
    out['verdict'] = 'PASS' if not fails else 'FAIL'
    out['fails'] = fails
    s = json.dumps(out, ensure_ascii=False, indent=1)
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(s + '\n')
    for c in ('lhs', 'lhsx'):
        r = out[c]
        print(f"[{c}] shape {r.get('shape')} · C1 {r.get('C1_rows', {}).get('set_eq_metrics')} · C4 cells {r.get('C4_regression', {}).get('cells')} "
              f"diff_cols {list((r.get('C4_regression') or {}).get('diff_cols', {}))[:8]} · "
              f"τ hertz {((r.get('C5_tau') or {}).get('hertz') or {}).get('status_counts')} · physics {((r.get('C5_tau') or {}).get('physics') or {}).get('status_counts')} · "
              f"prov {((r.get('C6_provenance') or {}).get('n'))} · fail {r['fail']}")
    print('verdict', out['verdict'], fails)
    return 0 if not fails else 1


if __name__ == '__main__':
    raise SystemExit(main())
