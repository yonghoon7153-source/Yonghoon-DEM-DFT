#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lhsx 64 확장 설계 CSV → 130 인계 스키마의 설계행 (J20-c · 1저자 09-29 밤 "64 도 진행하자").

    python3 scripts/lhsx_design_adapter.py --design docs/data/lhs_ext_design_v2_20260829.csv \\
        --union docs/data/lhs_union_20260927/lhsx64_union.tsv --out docs/data/lhsx_design_adapted_20260929.csv
    python3 scripts/lhsx_design_adapter.py --selftest

왜 필요한가: `lhs_design_dataset.build_handover` 는 설계행의 열을 그대로 싣는다.  lhsx 설계 (`id · pdd_SE · w_AM_P · w_AM_S · rP_um …`) 는
130 설계 (`case_id · am_pct · d_am_p_um …`) 와 이름 · 규약이 달라 그대로 넣으면 같은 뜻의 값이 다른 열에 흩어진다.

★ 변환은 **생성 코드에서 읽은 정의**로만 한다 (추정 금지):
  · 질량분율 `w_AM_P · w_AM_S · pdd_SE` (합 1 · `lhs_ext_materialize` 머리말: particledistribution/discrete plain = 질량분율) →
    `am_pct = 100·(1 − pdd_SE)` (130 의 am_pct 도 중량 %) · `ps_frac = w_AM_P/(w_AM_P + w_AM_S)` (AM 중 P 몫 · 밀도 같아 질량 = 부피).
  · mono 는 **P 열 = 일반 AM 자리** 규약 (`lhs_ext_materialize` 머리말 · R14): `mono_AM_P` → d_am_p = 2·rP · ps 1 / `mono_AM_S` → d_am_s = 2·rP · ps 0.
  · 입자 수 추정 = `lhs_ext_design.n_spheres` (같은 함수 · V_INS · volfrac) 로 상별 재계산 — CSV 의 `n_AM_est · n_SE_est` 와 **일치해야** 한다 (왕복 검사).
  · 압력 300 MPa · E_SE 1.35 GPa · 상자 50 µm 는 **템플릿 덱 (lhs00_000 · lhs00_110) 상속** — `render()` 는 반지름 · 가중 · volfrac · seed · 이름만 치환한다
    (그 파일 grep: pressure · youngs 0 건).  상자 50 은 union TSV 의 `lx_um` 로 64/64 확인한다.
  · 130 전용 추정 열 (loading · thickness_est · phi_*_est · sv_inv · rve_min/recommended · thick_over · finite_size_flag · se_percolation_est) 은 하중 기반
    두께 규약이 lhsx (volfrac 기반) 에 없어 **넣지 않는다** — 열 사전에 사유를 적는다.  실측 열 (수확 · union) 이 그 자리를 대신한다.
"""
from __future__ import annotations

import argparse
import csv
import math
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lhs_ext_design as XD                                   # noqa: E402  — n_spheres · phi_am_of_pdd_se (정본)

TEMPLATE_FIXED = {'pressure_MPa': 300.0, 'e_se_gpa': 1.35, 'rve_um': 50.0}   # lhs00_000 · lhs00_110 템플릿 값 = 130 설계 FIXED 와 같다
OMITTED = {
    'loading_mAh_cm2': 'lhsx 설계는 하중이 아니라 volfrac (삽입 부피분율) 로 두께가 정해진다 — 130 의 하중 열 없음',
    'thickness_est_um': '130 의 하중 기반 추정 규약이 lhsx 에 없다 — 실측 두께 열 (thickness_*_um) 을 쓸 것',
    'phi_am_est': '130 의 EPS_TYPICAL 추정 — lhsx 는 SE-rich 라 그 전형 공극률이 맞지 않는다 · 실측 phi_am 을 쓸 것',
    'phi_se_est': '같은 이유 · 실측 phi_se 를 쓸 것',
    'se_percolation_est_meanfield': '130 의 phi_se_est 기반 평균장 추정 — lhsx 에는 만들지 않는다 (실측 percolation_pct 가 ② 에서 온다)',
    'sv_inv_um': '130 의 φ 추정 기반 Sauter 역수 — 추정 φ 가 없어 만들지 않는다',
    'rve_min_um': '130 의 n_am_p 추정 기반 — 만들지 않는다 (rve_over_d_am_max 는 실측 상자 50 으로 계산)',
    'rve_recommended_um': '같은 이유',
    'thick_over_d_am_max': '추정 두께가 없다 — 실측 두께 / d_am_max 는 소비자가 계산',
    'finite_size_flag': '추정 두께 · n_am_p 추정이 없어 만들지 않는다',
}
COLS = ['case_id', 'block', 'd_am_p_um', 'd_am_s_um', 'ps_frac', 'ps_label', 'd_se_um', 'am_pct', 'rve_um', 'pressure_MPa', 'e_se_gpa',
        'd_am_max_um', 'r_AM_P_um', 'r_AM_S_um', 'r_SE_um', 'size_ratio_P_over_S', 'size_ratio_AM_over_SE',
        'n_am_p_est', 'n_am_s_est', 'n_se_est', 'n_total_est', 'rve_over_d_am_max',
        'lhsx_stratum', 'lhsx_ntype', 'lhsx_kind', 'lhsx_pdd_SE', 'lhsx_w_AM_P', 'lhsx_w_AM_S', 'lhsx_rSE_lo_um', 'lhsx_rSE_truncated',
        'lhsx_volfrac', 'lhsx_phi_AM_solid', 'lhsx_lhs_cell', 'lhsx_seed']


class AdapterRefusal(RuntimeError):
    pass


def _f(x):
    return float(x) if x not in (None, '') else float('nan')


def adapt_row(r: dict) -> dict:
    kind, nt = r['kind'], int(r['ntype'])
    wP, wS, wSE = _f(r['w_AM_P']), _f(r['w_AM_S']), _f(r['pdd_SE'])
    if abs(wP + wS + wSE - 1.0) > 2e-6:                     # CSV 가중 6 자리 반올림 셋 → 최대 1.5e-6 (실측 lhsx_002 0.999999)
        raise AdapterRefusal(f'{r["id"]}: 질량분율 합 {wP + wS + wSE!r} ≠ 1')
    rP, rS, rSE = _f(r['rP_um']), _f(r['rS_um']), _f(r['rSE_um'])
    volfrac = _f(r['volfrac'])
    phi_am = XD.phi_am_of_pdd_se(wSE)                       # 고체 기준 AM 부피분율 (정본 함수)
    if abs(phi_am - _f(r['phi_AM'])) > 1e-6:
        raise AdapterRefusal(f'{r["id"]}: phi_AM 재계산 {phi_am!r} ≠ CSV {r["phi_AM"]}')
    phi_se = 1.0 - phi_am
    if kind == 'bimodal':
        if nt != 3 or not (rS == rS):
            raise AdapterRefusal(f'{r["id"]}: bimodal 인데 ntype {nt} · rS {r["rS_um"]!r}')
        ps = wP / (wP + wS)
        dP, dS = 2 * rP, 2 * rS
        n_p = XD.n_spheres(phi_am * ps, rP, volfrac)
        n_s = XD.n_spheres(phi_am * (1 - ps), rS, volfrac)
    elif kind in ('mono_AM_P', 'mono_AM_S'):
        if nt != 2 or wS != 0.0 or (rS == rS):
            raise AdapterRefusal(f'{r["id"]}: {kind} 인데 ntype {nt} · w_AM_S {r["w_AM_S"]!r} · rS {r["rS_um"]!r} (P 열 = 일반 AM 자리 규약 위반)')
        ps = 1.0 if kind == 'mono_AM_P' else 0.0
        dP, dS = (2 * rP, float('nan')) if ps == 1.0 else (float('nan'), 2 * rP)
        n_all = XD.n_spheres(phi_am, rP, volfrac)
        n_p, n_s = (n_all, 0.0) if ps == 1.0 else (0.0, n_all)
    else:
        raise AdapterRefusal(f'{r["id"]}: 모르는 kind {kind!r}')
    n_se = XD.n_spheres(phi_se, rSE, volfrac)
    #  왕복 검사 — CSV 가 적은 추정 개수와 같은 함수로 같은 값이 나와야 한다.  허용 폭 = CSV 반지름이 4 자리로 반올림된 몫
    #  (n ∝ r⁻³ ⇒ Δn = 3·n·(5e-5/r)) + 1 (개수 반올림).  실측: lhsx_001 SE 56118.0 vs CSV 56120 (r 0.564 → 폭 ≈ 15).
    def _tol(n, rr):
        return 3.0 * n * (5e-5 / rr) + 1.0
    tol_am = (_tol(n_p, rP) + _tol(n_s, rS)) if kind == 'bimodal' else _tol(n_p + n_s, rP)
    if abs((n_p + n_s) - int(r['n_AM_est'])) > tol_am or abs(n_se - int(r['n_SE_est'])) > _tol(n_se, rSE):
        raise AdapterRefusal(f'{r["id"]}: 입자 수 재계산 AM {n_p + n_s:.1f} · SE {n_se:.1f} ≠ CSV {r["n_AM_est"]} · {r["n_SE_est"]} (허용 {tol_am:.1f} · {_tol(n_se, rSE):.1f})')
    d_max = max(x for x in (dP, dS) if x == x)
    d_am_eff = dP if ps == 1.0 else dS if ps == 0.0 else max(dP, dS)   # 130 의 size_ratio_AM_over_SE 는 d_am_max/d_se 가 아니라 예시상 d_P/d_SE (11/2 = 5.5) — 최대 AM 지름
    o = dict(case_id=r['id'], block=kind, d_am_p_um=dP, d_am_s_um=dS, ps_frac=ps,
             ps_label=f'{int(round(10 * ps))}:{10 - int(round(10 * ps))}', d_se_um=2 * rSE, am_pct=100.0 * (1.0 - wSE),
             rve_um=TEMPLATE_FIXED['rve_um'], pressure_MPa=TEMPLATE_FIXED['pressure_MPa'], e_se_gpa=TEMPLATE_FIXED['e_se_gpa'],
             d_am_max_um=d_max, r_AM_P_um=rP if dP == dP else float('nan'), r_AM_S_um=(rS if kind == 'bimodal' else (rP if ps == 0.0 else float('nan'))),
             r_SE_um=rSE, size_ratio_P_over_S=(dP / dS if (dP == dP and dS == dS) else float('nan')), size_ratio_AM_over_SE=d_am_eff / (2 * rSE),
             n_am_p_est=n_p, n_am_s_est=n_s, n_se_est=n_se, n_total_est=n_p + n_s + n_se, rve_over_d_am_max=TEMPLATE_FIXED['rve_um'] / d_max,
             lhsx_stratum=r['stratum'], lhsx_ntype=nt, lhsx_kind=kind, lhsx_pdd_SE=wSE, lhsx_w_AM_P=wP, lhsx_w_AM_S=wS,
             lhsx_rSE_lo_um=r['rSE_lo_um'], lhsx_rSE_truncated=r['rSE_truncated'], lhsx_volfrac=volfrac, lhsx_phi_AM_solid=phi_am,
             lhsx_lhs_cell=r['lhs_cell'], lhsx_seed=r['seed'])
    if not (0.0 < o['am_pct'] < 100.0 and 0.0 <= ps <= 1.0):
        raise AdapterRefusal(f'{r["id"]}: am_pct {o["am_pct"]} · ps {ps} 범위 밖')
    return o


def adapt(design_path: str, union_path: str | None) -> list[dict]:
    with open(design_path, encoding='utf-8-sig', newline='') as fh:
        rows = list(csv.DictReader(fh))
    if len({r['id'] for r in rows}) != len(rows):
        raise AdapterRefusal('id 중복')
    out = [adapt_row(r) for r in rows]
    if union_path:
        with open(union_path, encoding='utf-8', newline='') as fh:
            u = {r['case']: r for r in csv.DictReader(fh, delimiter='\t')}
        miss = [o['case_id'] for o in out if o['case_id'] not in u]
        if miss:
            raise AdapterRefusal(f'union 에 없는 설계행 {miss[:5]}')
        bad = [o['case_id'] for o in out if abs(float(u[o['case_id']]['lx_um']) - TEMPLATE_FIXED['rve_um']) > 1e-9]
        if bad:
            raise AdapterRefusal(f'상자 ≠ 50 µm: {bad[:5]} — 템플릿 상속 가정이 깨졌다')
    return out


def write(out_rows, path):
    with open(path, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, COLS, lineterminator='\n')
        w.writeheader()
        for o in out_rows:
            w.writerow({k: ('' if (isinstance(v, float) and v != v) else (repr(v) if isinstance(v, float) else v)) for k, v in o.items()})


def selftest() -> int:
    ok, bad = 0, []

    def chk(name, cond):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(name)
    #  실물 64 (리포 안) — 왕복 검사가 전부 서는가
    rows = adapt('docs/data/lhs_ext_design_v2_20260829.csv', 'docs/data/lhs_union_20260927/lhsx64_union.tsv')
    chk('① 64 행 · id 유일', len(rows) == 64 and len({r['case_id'] for r in rows}) == 64)
    kinds = {r['block'] for r in rows}
    chk('② kind 셋 (bimodal · mono_AM_P · mono_AM_S)', kinds == {'bimodal', 'mono_AM_P', 'mono_AM_S'})
    chk('③ mono_AM_S 는 d_am_p 빈칸 · ps 0 · r_AM_S = rP (P 열 = AM 자리)',
        all((r['d_am_p_um'] != r['d_am_p_um']) and r['ps_frac'] == 0.0 and r['r_AM_S_um'] == r['d_am_s_um'] / 2 for r in rows if r['block'] == 'mono_AM_S'))
    chk('④ mono_AM_P 는 d_am_s 빈칸 · ps 1', all((r['d_am_s_um'] != r['d_am_s_um']) and r['ps_frac'] == 1.0 for r in rows if r['block'] == 'mono_AM_P'))
    chk('⑤ am_pct = 100·(1 − pdd_SE) · SE-rich 영역 (am_pct 30–70)', all(abs(r['am_pct'] - 100 * (1 - r['lhsx_pdd_SE'])) < 1e-9 and 30 <= r['am_pct'] <= 70 for r in rows))
    chk('⑥ n_total_est = 상별 합', all(abs(r['n_total_est'] - (r['n_am_p_est'] + r['n_am_s_est'] + r['n_se_est'])) < 1e-6 for r in rows))
    #  반례 — 질량분율 합 ≠ 1 · phi_AM 불일치 · mono 규약 위반 · 입자 수 불일치 · 상자 ≠ 50
    base = dict(id='x', stratum='0', ntype='3', kind='bimodal', pdd_SE='0.4', w_AM_P='0.3', w_AM_S='0.3', rP_um='3.0', rS_um='1.5', rSE_um='0.7',
                rSE_lo_um='0.5', rSE_truncated='0', volfrac='0.25', phi_AM='', n_AM_est='', n_SE_est='', n_total_est='', lhs_cell='', seed='1')
    phi = XD.phi_am_of_pdd_se(0.4)
    base['phi_AM'] = repr(phi)
    nP = XD.n_spheres(phi * 0.5, 3.0, 0.25); nS = XD.n_spheres(phi * 0.5, 1.5, 0.25); nSE = XD.n_spheres(1 - phi, 0.7, 0.25)
    base.update(n_AM_est=str(int(round(nP + nS))), n_SE_est=str(int(round(nSE))))
    chk('⑦ 정상 합성 행 통과', adapt_row(dict(base))['ps_frac'] == 0.5)

    def refuses(**kw):
        try:
            adapt_row(dict(base, **kw))
            return False
        except AdapterRefusal:
            return True
    chk('★⑧ 질량분율 합 ≠ 1 거부', refuses(w_AM_S='0.31'))
    chk('★⑨ phi_AM 불일치 거부', refuses(phi_AM=repr(phi + 1e-3)))
    chk('★⑩ 입자 수 불일치 거부 (같은 함수 왕복 · 반올림 폭 밖)', refuses(n_SE_est=str(int(round(nSE * 1.01)))) and not refuses(n_SE_est=str(int(round(nSE)) + 1)))
    chk('★⑪ mono 인데 w_AM_S ≠ 0 거부', refuses(kind='mono_AM_P', ntype='2', rS_um='', w_AM_S='0.1', w_AM_P='0.5'))
    chk('★⑫ 모르는 kind 거부', refuses(kind='trimodal'))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'u.tsv')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('case\tlx_um\n' + '\n'.join(f'{r["case_id"]}\t{"49.0" if i == 0 else "50.0"}' for i, r in enumerate(rows)) + '\n')
        try:
            adapt('docs/data/lhs_ext_design_v2_20260829.csv', p)
            chk('★⑬ 상자 ≠ 50 거부', False)
        except AdapterRefusal:
            chk('★⑬ 상자 ≠ 50 거부', True)
        q = os.path.join(td, 'a.csv')
        write(rows, q)
        with open(q, encoding='utf-8', newline='') as fh:
            back = list(csv.DictReader(fh))
        chk('⑭ CSV 왕복 — 64 행 · 열 = COLS · 빈칸 = NaN', len(back) == 64 and list(back[0].keys()) == COLS
            and sum(1 for b in back if b['d_am_p_um'] == '') == sum(1 for r in rows if r['block'] == 'mono_AM_S'))
    print(f'lhsx_design_adapter selftest: {ok}/{ok + len(bad)}' + ('' if not bad else '  ✗ ' + ' | '.join(bad)))
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--design', default='docs/data/lhs_ext_design_v2_20260829.csv')
    ap.add_argument('--union', default='docs/data/lhs_union_20260927/lhsx64_union.tsv', help='상자 50 µm 확인용 (lx_um) · "" 이면 생략')
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    rows = adapt(a.design, a.union or None)
    if a.out:
        write(rows, a.out)
        print(f'→ {a.out}  {len(rows)} 행 × {len(COLS)} 열  (넣지 않은 130 추정 열 {len(OMITTED)}: {", ".join(OMITTED)})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
