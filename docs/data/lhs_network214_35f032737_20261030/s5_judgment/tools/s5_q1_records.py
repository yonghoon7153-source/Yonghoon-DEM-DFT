#!/usr/bin/env python3
"""Q1 — H0 이온 σ 의 v1.2 → B7 변화: 받은 기록만으로 원인을 어디까지 가를 수 있나 (읽기 전용 · 새 계산 = 기록끼리의 산술뿐).

원천 (셋 다 읽기만):
  · v1.2 값 = 커밋된 τ 원천 묶음 (docs/data/lhs_network194_11fcf91e8/handover_v12_20261006/net194_tau_sources_20261006.tar.gz) 을 빈 폴더에 푼 것 —
    케이스마다 network_conductivity_dual.json (hertzian: sigma_full · sigma_bulk_net · sigma_constr_net · n_nodes · percolating_fraction ·
    n_bottom · n_top · boundary_rule · boundary_band_frac)
  · v1.2 입력 지문 = 커밋된 docs/data/lhs_network194_11fcf91e8/merged/<ds>/status.json (원 덤프 sha256 · type_map · contact_scan)
  · B7 = 받은 194 묶음 — reread.json (가지 표 값 · 증서 풀이 방법 · row_cells 의 띠 규칙 · 띠 비율) · merged/<ds>/status.json
판정 재료:
  ① 입력 같음 — 원 덤프 sha256 (atom · contact · mesh · deck) · type_map · contact_scan 이 두 배치에서 같은가.
  ② 띠 같음 — 이온 Hertz 띠 규칙 · 띠 비율이 같은가 (v1.2 dual ↔ B7 row_cells).
  ③ 풀이 경로 — v1.2 옛 모듈 = 관통 노드 N + 2 > 30000 이면 CG (scipy 1.18.1 에서 옛 `tol=` 인자가 없어 `atol=1e-8` · 기본 rtol 1e-5 로 내려감) · 아니면 spsolve.
     N ≈ n_nodes × percolating_fraction (4 자리 반올림 → 근사).  B7 = 증서의 method.
  ④ 저장 해상도 — σ_ratio 는 소수 8 자리로 저장된다 (두 배치 모두).  두 반올림 값의 차 k 칸이면 참 차 ∈ ((k−1)·1e-8, (k+1)·1e-8) — k ≤ 1 이면
     기록으로는 크기를 못 가른다.
  ⑤ 가지 동조 — 전극 변경은 FULL · CF · 협착-only 세 가지의 경계층을 같이 바꾼다.  협착만 바뀌면 CF 가 가만있고 bulk 만 바뀌면 협착-only 가 가만있다.
  ⑥ 띠 · 망 크기와의 관계 — 순위 상관 · log–log 적합 (원인 확정이 아니라 일관성).
사용: python3 -I s5_q1_records.py --repo <리포> --root194 <풀어 둔 B7 194 뿌리> --v12src <풀어 둔 v1.2 τ 원천> --out <폴더>
"""
import argparse
import csv
import json
import math
import os

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
ap.add_argument('--v12src', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
UNIT = 1e-8
BR = (('full', 'sigma_full'), ('bulk_only', 'sigma_bulk_net'), ('constriction_only', 'sigma_constr_net'))
OLD_CG_N = 30000          # 옛 모듈: total_nodes = N + 2 > 30000 → CG


def num(x):
    """인계 칸은 글자다 (row_cells) — 유한 실수면 float · 아니면 None."""
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return float(x) if math.isfinite(x) else None
    try:
        v = float(str(x).strip())
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def jload(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def status_map(path):
    s = jload(path)
    cs = s['cases']
    if isinstance(cs, dict):
        return cs
    return {c['case']: c for c in cs}


v12_status, b7_status = {}, {}
for ds in ('lhs', 'lhsx'):
    v12_status.update(status_map(os.path.join(a.repo, 'docs/data/lhs_network194_11fcf91e8/merged', ds, 'status.json')))
    b7_status.update(status_map(os.path.join(a.root194, 'merged', ds, 'status.json')))

rr = jload(os.path.join(a.root194, 'reread.json'))
rows = []
for c in rr['cases']:
    k, ds = c['case'], c['cohort']
    h = jload(os.path.join(a.v12src, 'cases', k, 'work', 'results', k, 'network_conductivity_dual.json'))['hertzian']
    t = c['table']['hertz']
    rc = c.get('row_cells') or {}
    sv, sb = v12_status.get(k) or {}, b7_status.get(k) or {}
    n_nodes, pf = h.get('n_nodes'), h.get('percolating_fraction')
    n_perc = (n_nodes * pf) if isinstance(n_nodes, (int, float)) and isinstance(pf, (int, float)) else None
    r = dict(dataset=ds, case=k,
             same_raw_sha=(bool(sv.get('sha')) and sv.get('sha') == sb.get('sha')),
             same_type_map=(sv.get('type_map') == sb.get('type_map')),
             same_contact_scan=(sv.get('contact_scan') == sb.get('contact_scan')),
             band_rule_v12=h.get('boundary_rule'), band_rule_b7=rc.get('ion_net_band_rule_hertz'),
             band_frac_v12=num(h.get('boundary_band_frac')), band_frac_b7=num(rc.get('ion_net_band_frac_hertz')),
             n_nodes=n_nodes, n_perc_approx=(round(n_perc) if n_perc is not None else None),
             v12_solver=(None if n_perc is None else ('cg_rtol1e-5' if n_perc + 2 > OLD_CG_N else 'spsolve')),
             v12_solver_borderline=(n_perc is not None and abs(n_perc + 2 - OLD_CG_N) <= 0.00005 * n_nodes + 1),
             b7_method_full=((t['full'].get('cert') or {}).get('method')),
             n_bottom=h.get('n_bottom'), n_top=h.get('n_top'), n_edges=h.get('n_edges'),
             status_b7=t['full'].get('status'))
    r['band_frac_absdiff'] = (abs(r['band_frac_v12'] - r['band_frac_b7'])
                              if r['band_frac_v12'] is not None and r['band_frac_b7'] is not None else None)
    #  띠 비율 같음 = 규칙 글자 같음 ∧ 비율 차 ≤ 1e-12 (B7 칸은 글자로 옮겨 적힌 값 — 같은 float 이면 차 0)
    r['same_band'] = (r['band_rule_v12'] == r['band_rule_b7'] and r['band_frac_absdiff'] is not None and r['band_frac_absdiff'] <= 1e-12)
    for br, key in BR:
        new, old = t[br].get('value'), h.get(key)
        okb = isinstance(new, (int, float)) and isinstance(old, (int, float)) and new != 0 and old != 0
        r[f'ok_{br}'] = okb
        r[f'v12_{br}'], r[f'b7_{br}'] = old, new
        if not okb:
            r[f'd_{br}'] = r[f'u_{br}'] = r[f'units_{br}'] = r[f'units_off_{br}'] = None
            continue
        m = max(abs(new), abs(old))
        r[f'd_{br}'] = (new - old) / m                      # 상대 변화 (저장값끼리)
        r[f'u_{br}'] = UNIT / m                             # 한 칸의 상대 크기
        r[f'units_{br}'] = round((new - old) / UNIT)
        r[f'units_off_{br}'] = abs((new - old) / UNIT - round((new - old) / UNIT))
    rows.append(r)


def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    rk = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for t_ in range(i, j + 1):
            rk[o[t_]] = (i + j) / 2.0
        i = j + 1
    return rk


def spearman(x, y):
    rx, ry = rank(x), rank(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((p - mx) * (q - my) for p, q in zip(rx, ry))
    sxx = math.sqrt(sum((p - mx) ** 2 for p in rx))
    syy = math.sqrt(sum((q - my) ** 2 for q in ry))
    return sxy / (sxx * syy) if sxx and syy else None


def q(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(p * (len(v) - 1) + 0.5))] if v else None


def summ(v):
    return dict(n=len(v), min=min(v), p05=q(v, .05), p50=q(v, .5), p95=q(v, .95), max=max(v)) if v else dict(n=0)


res = {'schema': 's5_q1_records/v2', 'n_rows': len(rows)}
full = [r for r in rows if r['ok_full']]
res['n_full_comparable'] = len(full)
res['n_full_comparable_by_dataset'] = {ds: sum(1 for r in full if r['dataset'] == ds) for ds in ('lhs', 'lhsx')}
res['n_bulk_only_missing_v12_among_full'] = sum(1 for r in full if not r['ok_bulk_only'])
# ① ② 입력 · 띠 같음 (194 전부)
res['inputs'] = dict(same_raw_sha=sum(r['same_raw_sha'] for r in rows), same_type_map=sum(r['same_type_map'] for r in rows),
                     same_contact_scan=sum(r['same_contact_scan'] for r in rows), of=len(rows))
res['bands_full_comparable'] = dict(same_band=sum(r['same_band'] for r in full), of=len(full),
                                    differ=[(r['case'], r['band_rule_v12'], r['band_rule_b7'], r['band_frac_v12'], r['band_frac_b7'])
                                            for r in full if not r['same_band']])
# ③ 풀이 경로
res['v12_solver_full_comparable'] = {s: sum(1 for r in full if r['v12_solver'] == s) for s in ('spsolve', 'cg_rtol1e-5')}
res['v12_solver_borderline'] = [r['case'] for r in full if r['v12_solver_borderline']]
res['b7_method_full_comparable'] = {m: sum(1 for r in full if r['b7_method_full'] == m) for m in sorted({str(r['b7_method_full']) for r in full})}
# ④ 저장 해상도
res['storage_grid_max_offset'] = max(r[f'units_off_{br}'] for r in rows for br, _ in BR if r[f'ok_{br}'])
res['full_resolution_limited'] = [(r['case'], r['units_full'], r['d_full'], r['u_full']) for r in full if abs(r['units_full']) <= 1]
res['full_sign'] = dict(up=sum(1 for r in full if r['units_full'] > 0), same=sum(1 for r in full if r['units_full'] == 0),
                        down=sum(1 for r in full if r['units_full'] < 0))
# ⑤ 가지 동조 — 세 가지 모두 3 칸 이상 움직인 행
res3 = [r for r in rows if all(r[f'ok_{br}'] and abs(r[f'units_{br}']) >= 3 for br, _ in BR)]
rat_cf = [r['d_bulk_only'] / r['d_full'] for r in res3]
rat_cn = [r['d_constriction_only'] / r['d_full'] for r in res3]
res['branch_coherence'] = dict(n_rows_all_three_resolved=len(res3),
                               sign_all_same=sum(1 for r in res3 if (r['d_full'] > 0) == (r['d_bulk_only'] > 0) == (r['d_constriction_only'] > 0)),
                               cf_over_full=summ(rat_cf), constr_over_full=summ(rat_cn))
# 협착-only 대 FULL (CF 가 v1.2 에 없는 lhsx 29 행 포함 · 두 가지 3 칸 이상)
res2 = [r for r in full if r['ok_constriction_only'] and abs(r['units_full']) >= 3 and abs(r['units_constriction_only']) >= 3]
res['constr_over_full_all'] = summ([r['d_constriction_only'] / r['d_full'] for r in res2])
# ⑥ 순위 상관 · log–log (FULL 3 칸 이상 · 양수)
fr = [r for r in full if abs(r['units_full']) >= 3 and r['d_full'] > 0]
dfl = [r['d_full'] for r in fr]
feats = {'band_frac': [r['band_frac_b7'] for r in fr], 'sigma_full_b7': [r['b7_full'] for r in fr],
         'n_bottom': [r['n_bottom'] for r in fr], 'n_top': [r['n_top'] for r in fr],
         '1/min(n_bottom,n_top)': [1.0 / min(r['n_bottom'], r['n_top']) for r in fr],
         'n_nodes': [r['n_nodes'] for r in fr], 'n_edges': [r['n_edges'] for r in fr]}
res['spearman_d_full_vs'] = dict(n=len(fr), **{kk: spearman(dfl, v) for kk, v in feats.items()})
X = [math.log(r['band_frac_b7']) for r in fr]
Y = [math.log(r['d_full']) for r in fr]
mx, my = sum(X) / len(X), sum(Y) / len(Y)
sl = sum((x - mx) * (y - my) for x, y in zip(X, Y)) / sum((x - mx) ** 2 for x in X)
ic = my - sl * mx
resid = [y - (ic + sl * x) for x, y in zip(X, Y)]
sd = math.sqrt(sum(e * e for e in resid) / (len(resid) - 2))
r2 = 1 - sum(e * e for e in resid) / sum((y - my) ** 2 for y in Y)
res['loglog_d_full_vs_band_frac'] = dict(n=len(fr), slope=sl, intercept=ic, r2=r2, resid_sd=sd)
pick = {r['case']: r for r in rows}


def z_of(k):
    r = pick[k]
    if r not in fr:
        return None
    e = math.log(r['d_full']) - (ic + sl * math.log(r['band_frac_b7']))
    return dict(resid=e, z=e / sd, predicted_d_full=math.exp(ic + sl * math.log(r['band_frac_b7'])),
                rank_by_resid_desc=1 + sorted(resid, reverse=True).index(min(resid, key=lambda v: abs(v - e))))


lx = [r for r in full if r['dataset'] == 'lhsx']
res['lhsx_026'] = dict(row={kk: pick['lhsx_026'][kk] for kk in ('band_frac_b7', 'n_bottom', 'n_top', 'n_nodes', 'v12_solver', 'b7_method_full',
                                                                  'd_full', 'units_full', 'd_bulk_only', 'units_bulk_only',
                                                                  'd_constriction_only', 'units_constriction_only', 'same_raw_sha', 'same_band')},
                       rank_d_full_in_lhsx=1 + sorted([r['d_full'] for r in lx], reverse=True).index(pick['lhsx_026']['d_full']),
                       rank_band_frac_in_lhsx=1 + sorted([r['band_frac_b7'] for r in lx], reverse=True).index(pick['lhsx_026']['band_frac_b7']),
                       n_lhsx=len(lx), loglog=z_of('lhsx_026'))
# lhs00_123 — 저장 해상도 구간 + 같은 침대의 다른 가지 구간 (+ 다른 행의 가지 비 범위를 빌린 추정)
r = pick['lhs00_123']


def interval(rr_, br):
    k_, m_ = rr_[f'units_{br}'], max(abs(rr_[f'v12_{br}']), abs(rr_[f'b7_{br}']))
    return (max(k_ - 1, 0) * UNIT / m_, (k_ + 1) * UNIT / m_)


iv_f, iv_cf, iv_cn = interval(r, 'full'), interval(r, 'bulk_only'), interval(r, 'constriction_only')
cf_rng = (res['branch_coherence']['cf_over_full']['min'], res['branch_coherence']['cf_over_full']['max'])
cn_rng = (res['constr_over_full_all']['min'], res['constr_over_full_all']['max'])
res['lhs00_123'] = dict(row={kk: r[kk] for kk in ('band_frac_b7', 'n_bottom', 'n_top', 'n_nodes', 'v12_solver', 'b7_method_full',
                                                  'v12_full', 'b7_full', 'units_full', 'v12_bulk_only', 'b7_bulk_only', 'units_bulk_only',
                                                  'v12_constriction_only', 'b7_constriction_only', 'units_constriction_only',
                                                  'same_raw_sha', 'same_band')},
                        full_interval_from_storage=iv_f, cf_interval=iv_cf, constr_interval=iv_cn,
                        inferred_full_from_cf=(iv_cf[0] / cf_rng[1], iv_cf[1] / cf_rng[0]),
                        inferred_full_from_constr=(0.0, iv_cn[1] / cn_rng[0]),
                        loglog_predicted_d_full=math.exp(ic + sl * math.log(r['band_frac_b7'])),
                        note='추정 = 다른 행의 가지 비 범위 · 띠 적합을 이 침대에 빌린 것 — 측정 아님')
res['top6_d_full'] = [(x['case'], x['d_full'], x['units_full'], x['band_frac_b7']) for x in sorted(full, key=lambda x: -x['d_full'])[:6]]
cgr = [x['d_full'] for x in full if x['v12_solver'] == 'cg_rtol1e-5']
spr = [x['d_full'] for x in full if x['v12_solver'] == 'spsolve']
res['d_full_by_v12_solver'] = dict(cg=summ(cgr), spsolve=summ(spr))

os.makedirs(a.out, exist_ok=True)
#  TSV = 상대 차 · 저장 칸 · 띠 · 풀이 경로만 — σ 값 칸 (v12_* · b7_*) 은 싣지 않는다 (진단 기록 · 인계표 대용이 되지 않게 · tau_status_by_case.tsv 와 같은 규칙)
cols = [c for c in rows[0] if not (c.startswith('v12_full') or c.startswith('v12_bulk') or c.startswith('v12_constr') or c.startswith('b7_full')
                                   or c.startswith('b7_bulk') or c.startswith('b7_constr'))]
with open(os.path.join(a.out, 'q1_electrode_by_case.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter='\t', lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    for x in sorted(rows, key=lambda x: (x['dataset'], x['case'])):
        w.writerow(x)
with open(os.path.join(a.out, 'q1_records_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
