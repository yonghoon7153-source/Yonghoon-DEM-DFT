#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""194 인계 v1.2 다시 읽기 검산 (Codex 4차 §8-4) — 읽기 전용 · 계산 없음 (τ 는 원천 파일이 있으면 tau_flux 로 독립 재계산).

  python3 reread_v12.py --handover-dir <WSL 묶음을 푼 handover/> [--seal-audit <seal_audit.tsv>] [--tau-sources <τ 원천 묶음을 푼 ROOT>] --out reread.json

⛔ **자동 배포 관문이 아니다** — 검산 도구다 (Codex 5차 `docs/reviews/codex_review_rglr3_reverify_20261006.md` §6 QV1).  PASS 는 "이 표가 커밋된
   배치 증거 · 옛 인계 · 봉인 감사와 이 검사 범위에서 맞는다" 까지이고, 다음 납품본을 자동 승인하지 않는다 (배포는 사람이 판정 · 독립 대조와 함께).
   반례 회귀 = `scripts/test_reread_v12.py` (RGLR4-01 · 02 — 복사본 변조가 비영 종료 · 원본 PASS 유지).

대조 원천 (리포 커밋본): 배치 증거 `docs/data/lhs_network194_11fcf91e8/merged/<c>/{metrics_flat.csv,status.json}` ·
옛 인계 (d1ec42fba 접촉 배치) `docs/data/{lhs,lhsx}_handover_20261001.csv` · 퍼콜 감사 `docs/data/lhs_perc_audit_20261001/*_d1ec42fba/perc_audit.tsv` ·
봉인 지문 · 등록 큐 `manifest.json` (code_hashes · plan.queue).
검사 (코호트마다):
  C1 행 집합 = metrics_flat 케이스 = 130 · 64 · 중복 없음
  C2 LW 열 없음 · 제외 노트에 LW = frame_unverified
  C3 열 사전 ↔ 표 열 (양쪽 같은 집합 · 뜻 빈칸 없음)
  C4 회귀 — 옛 인계와 공통 열 값 (문자열 같음 · 부동소수 상대 1e-12 안 = close · 그 밖 = diff) · 새 열 · 빠진 열 · 행 짝 (양쪽 같은 케이스 집합).
     ★ RGLR4-01 (Codex 5차 · 10-06): diff 칸 · 빠진 열 · 짝 없는 행 = **실패** (옛 판은 기록만 하고 PASS · rc 0 — 한 칸 99 변조도 통과).
     의도된 변화는 `C4_ALLOWED` (세대별 허용 목록 · 열마다 기대 diff 칸 수 · 기대 탈락 열 — 이 파일 안 상수 = 커밋이 봉인) 에 적은 것만 통과 ·
     기대 칸 수와 다르면 실패.  v1.2 세대 = 빈 목록 (옛 인계와 공통 24,440 + 12,160 칸 차이 0 · 탈락 0).
  C5 τ 묶음 — 모드별 상태 수 · NOT_COMPUTED 0 · OK/MBCB 값 = metrics_flat 로 다시 계산한 φ_mc / (σ_ratio · L_gap / L_mc) ·
     tau = √tau2 · OK ⇒ ≥ 1 · MBCB ⇒ < 1 · NOT_PERCOLATING ⇒ f = 0 · tau2 빈칸 · 비관통 집합 = 망 valid_zero = 퍼콜 감사 ·
     BAND_FALLBACK ⇒ 값 빈칸 · 띠 L1/L2 · 공통 메타 (σ₀ 3.0 · φ basis · L basis) · basis_check ok
  C6 τ 출처 부록 — 행 = 케이스 (행 수 = 표 행 수 · 케이스 중복 0 · 같은 집합 — RGLR4-02 의 C6 몫) · network_run_id = 배치 status.json ·
     tau_flux sha256 = 봉인 · 같은 세대 검사 목록 전부 · basis 문구
  C7 (선택 · --tau-sources) 원천 sha256 = 출처 부록 · tau_flux.ion_columns 독립 재계산 = 표 τ 칸 (전부)
  C8 (선택 · --seal-audit) 봉인 감사 — ★ RGLR4-02 (Codex 5차): 줄 수 · 판정 문자열만 세던 옛 판은 lhsx_064 행을 lhs00_000 중복으로 바꿔도
     PASS 였다.  이제 = 행 수 194 · 케이스 중복 0 · 케이스 집합 = 인계표 두 코호트 집합 = 등록 manifest plan.queue 집합 · 코호트 = 큐의 코호트 ·
     판정 SEALED / SEALED_LEGACY · merged same · record_status = 병합 기록 (merged/<코호트>/status.json) 의 상태 (done · partial) ·
     record_sha256 = 그 병합 기록의 정규 JSON sha256 (`run_network_194_parallel._rec_sha` 와 같은 직렬화 — 정렬 키 · 구분자 , :) — 하나라도 어긋나면 실패.
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
#: ★ RGLR4-01 — C4 세대별 허용 목록 (의도된 변화만).  diff_cols = {열: 기대 diff 칸 수} · dropped_cols = [기대 탈락 열].
#:   v1.2 (10-06) = 빈 목록 — 옛 인계 (10-01 d1ec42fba) 와 공통 칸 차이 0 · 탈락 0 이 기대값이다.  바꾸려면 이 상수를 커밋으로 고친다 (커밋 = 봉인 ·
#:   사유를 옆 주석에) — 실행 인자로 넓히지 않는다.
C4_ALLOWED = {'lhs': {'diff_cols': {}, 'dropped_cols': []}, 'lhsx': {'diff_cols': {}, 'dropped_cols': []}}
#: C8 판정 · 병합 기록 상태 허용값
C8_VERDICTS_OK = ('SEALED', 'SEALED_LEGACY')
C8_RECORD_STATUS_OK = ('done', 'partial')
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


def rec_sha(rec):
    """병합 케이스 기록의 정규 JSON sha256 — `scripts/run_network_194_parallel._rec_sha` 와 같은 직렬화 (정렬 키 · ensure_ascii False · 구분자 , :).
    ⚠ 사본이다 (검산기는 리포 밖 묶음에서도 돈다) — 같은 직렬화인지는 baseline (커밋된 감사표 194 행 일치) 이 지킨다."""
    if not isinstance(rec, dict):
        return None
    return hashlib.sha256(json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')).hexdigest()


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
    res['case_ids'] = ids                                   # C8 (봉인 감사 ↔ 인계표 집합) 가 쓴다
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
    # C4 회귀 — ★ RGLR4-01: diff 칸 · 빠진 열 · 짝 없는 행은 실패 (허용 목록 C4_ALLOWED 에 기대값으로 적은 것만 통과)
    prev_rows = read_csv(PREV[coh])
    prev = {r['case_id']: r for r in prev_rows}
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
    dropped = [c for c in pcols if c not in cols]
    allow = C4_ALLOWED.get(coh) or {}
    a_diff, a_drop = dict(allow.get('diff_cols') or {}), list(allow.get('dropped_cols') or [])
    c4_prob = []
    for c, e in sorted(diffs.items()):
        if c not in a_diff:
            c4_prob.append(f'diff {c} {e["n"]} 칸 (허용 목록 밖) 예 {e["ex"][:1]}')
        elif a_diff[c] != e['n']:
            c4_prob.append(f'diff {c} {e["n"]} 칸 ≠ 허용 목록 기대 {a_diff[c]} 칸')
    for c, n_ in sorted(a_diff.items()):
        if c not in diffs:
            c4_prob.append(f'허용 목록의 diff {c} (기대 {n_} 칸) 가 실제로 없다 — 허용 목록이 낡았다')
    for c in dropped:
        if c not in a_drop:
            c4_prob.append(f'탈락 열 {c} (허용 목록 밖)')
    for c in a_drop:
        if c not in dropped:
            c4_prob.append(f'허용 목록의 탈락 열 {c} 가 실제로는 있다 — 허용 목록이 낡았다')
    t_ids, p_ids = [r['case_id'] for r in tab], [r['case_id'] for r in prev_rows]
    if len(p_ids) != len(set(p_ids)):
        c4_prob.append(f'옛 인계에 케이스 중복 {len(p_ids) - len(set(p_ids))}')
    if set(t_ids) != set(p_ids):
        c4_prob.append(f'짝 없는 행 — 표에만 {sorted(set(t_ids) - set(p_ids))[:5]} · 옛 인계에만 {sorted(set(p_ids) - set(t_ids))[:5]}')
    res['C4_regression'] = {'common_cols': len(common), 'cells': tally, 'diff_cols': diffs,
                            'new_cols': [c for c in cols if c not in pcols], 'dropped_cols': dropped,
                            'allowed': {'diff_cols': a_diff, 'dropped_cols': a_drop}, 'problems': c4_prob[:20], 'n_problems': len(c4_prob)}
    if c4_prob:
        F.append(f'C4 회귀 ({len(c4_prob)}: {c4_prob[0]})')
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
    p_cases = [r.get('case') for r in prov]
    n_dup_p = len(p_cases) - len(set(p_cases))
    res['C6_provenance'] = {'n': len(prov), 'n_table': len(ids), 'n_dup': n_dup_p, 'set_eq_table': set(p_cases) == set(ids),
                            'bad': pb[:20], 'n_bad': len(pb), 'tau_flux_seal': tf_seal}
    #  ★ RGLR4-02 (C6 몫) — 같은 집합 검사만으로는 중복 행 (덧붙임) 을 못 본다 → 행 수 = 표 행 수 · 케이스 중복 0 도 요구
    if pb or not res['C6_provenance']['set_eq_table'] or n_dup_p or len(prov) != len(ids):
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


def seal_audit_check(path, out):
    """C8 — 봉인 감사표 ↔ 인계표 · 등록 manifest 큐 · 병합 기록 (★ RGLR4-02).  반환 dict (problems 가 비면 통과)."""
    rows = read_csv(path, '\t')
    head = list(rows[0].keys()) if rows else []
    vk = next((k for k in head if k.lower() in ('verdict', '판정')), None)
    prob = []
    need = ('case', 'cohort', 'record_status', 'merged', 'record_sha256')
    miss_h = [k for k in need if k not in head] + ([] if vk else ['verdict'])
    if miss_h:
        prob.append(f'감사표 머리에 없는 열 {miss_h}')
    cases = [r.get('case') for r in rows]
    n_exp = sum(EXPECT_N.values())
    if len(rows) != n_exp:
        prob.append(f'행 수 {len(rows)} ≠ {n_exp}')
    dups = sorted({c for c in cases if cases.count(c) > 1})
    if dups:
        prob.append(f'케이스 중복 {dups[:5]}')
    tab_ids = {c: coh for coh in ('lhs', 'lhsx') for c in ((out.get(coh) or {}).get('case_ids') or [])}
    try:
        man = json.load(open(os.path.join(BATCH, 'manifest.json'), encoding='utf-8'))
        queue = {e['case']: e['cohort'] for e in ((man.get('plan') or {}).get('queue') or [])}
    except (OSError, ValueError, KeyError, TypeError) as e:
        queue = {}
        prob.append(f'등록 manifest plan.queue 를 못 읽었다 ({type(e).__name__})')
    if set(cases) != set(tab_ids):
        prob.append(f'감사표 집합 ≠ 인계표 집합 — 감사표에만 {sorted(set(cases) - set(tab_ids))[:5]} · 인계표에만 {sorted(set(tab_ids) - set(cases))[:5]}')
    if queue and set(cases) != set(queue):
        prob.append(f'감사표 집합 ≠ 등록 큐 — 감사표에만 {sorted(set(cases) - set(queue))[:5]} · 큐에만 {sorted(set(queue) - set(cases))[:5]}')
    merged = {}
    for coh in ('lhs', 'lhsx'):
        try:
            merged[coh] = json.load(open(os.path.join(BATCH, 'merged', coh, 'status.json'), encoding='utf-8')).get('cases') or {}
        except (OSError, ValueError) as e:
            merged[coh] = {}
            prob.append(f'병합 기록 merged/{coh}/status.json 을 못 읽었다 ({type(e).__name__})')
    cnt, mcnt, n_sha = {}, {}, 0
    for r in rows:
        c, coh = r.get('case'), r.get('cohort')
        cnt[r.get(vk)] = cnt.get(r.get(vk), 0) + 1
        mcnt[r.get('merged')] = mcnt.get(r.get('merged'), 0) + 1
        if r.get(vk) not in C8_VERDICTS_OK:
            prob.append(f'{c}: 판정 {r.get(vk)!r} ∉ {C8_VERDICTS_OK}')
        if r.get('merged') != 'same':
            prob.append(f'{c}: merged {r.get("merged")!r} ≠ same')
        want_coh = queue.get(c) or tab_ids.get(c)
        if coh != want_coh or (c in tab_ids and coh != tab_ids[c]):
            prob.append(f'{c}: 코호트 {coh!r} ≠ 등록 큐 · 인계표 {want_coh!r}')
        rec = (merged.get(want_coh) or {}).get(c)
        if not isinstance(rec, dict):
            prob.append(f'{c}: 병합 기록 (merged/{want_coh}) 에 케이스가 없다')
            continue
        if r.get('record_status') not in C8_RECORD_STATUS_OK or r.get('record_status') != rec.get('status'):
            prob.append(f'{c}: record_status {r.get("record_status")!r} ≠ 병합 기록 상태 {rec.get("status")!r} (허용 {C8_RECORD_STATUS_OK})')
        if r.get('record_sha256') != rec_sha(rec):
            prob.append(f'{c}: record_sha256 ≠ 병합 기록 정규 JSON sha256')
        else:
            n_sha += 1
    return {'n': len(rows), 'n_unique': len(set(cases)), 'verdicts': cnt, 'merged': mcnt, 'record_sha_match': n_sha,
            'queue_n': len(queue), 'problems': prob[:30], 'n_problems': len(prob)}


def main(argv=None):
    ap = argparse.ArgumentParser(description='194 인계 v1.2 다시 읽기 검산 (읽기 전용 · 검산 도구 — 자동 배포 관문이 아니다)')
    ap.add_argument('--handover-dir', required=True)
    ap.add_argument('--seal-audit', default='')
    ap.add_argument('--tau-sources', default='', help='τ 원천 묶음을 푼 ROOT (cases/<c>/work/results/<run>/…)')
    ap.add_argument('--out', default='')
    a = ap.parse_args(argv)
    out = {'repo': REPO, 'batch': BATCH}
    for coh in ('lhs', 'lhsx'):
        cohort(coh, a.handover_dir, a.tau_sources or None, out)
    if a.seal_audit:
        out['C8_seal_audit'] = c8 = seal_audit_check(a.seal_audit, out)
        if c8['problems']:
            out.setdefault('fail_global', []).append(f'C8 봉인 감사 ({len(c8["problems"])}: {c8["problems"][0]})')
    else:
        out['C8_seal_audit'] = {'skipped': True, 'note': '--seal-audit 없음 — 봉인 증거를 대조하지 않았다 (PASS 가 봉인을 말하지 않는다)'}
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
    c8 = out.get('C8_seal_audit') or {}
    print('[C8] ' + ('건너뜀 (--seal-audit 없음 — 봉인 증거 미대조)' if c8.get('skipped') else
                     f"{c8.get('n')} 행 · 고유 {c8.get('n_unique')} · 등록 큐 {c8.get('queue_n')} · 판정 {c8.get('verdicts')} · merged {c8.get('merged')} · "
                     f"record sha 일치 {c8.get('record_sha_match')} · 문제 {c8.get('n_problems')}"))
    print('verdict', out['verdict'], fails, '— 검산 도구 결과 (자동 배포 관문 아님)')
    return 0 if not fails else 1


if __name__ == '__main__':
    raise SystemExit(main())
