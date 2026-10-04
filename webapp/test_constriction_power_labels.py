#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""④a 협착 저항 전력 몫 — 웹앱 같은 묶음 (J20-s · 1저자 비준 10-04 · LHS-30 · J20-l).

옛 행 'Constriction 비율(%)' = 1 − mean_edge[R_bulk/R_total] (접촉별 비가중 평균 · L2-08) — 값 · 조회 키 그대로, **이름표만** 정정.
새 행 = constriction_power_share_ion_{hertz,physics} × 100 (같은 FULL 해의 Σ I²R_c / Σ I²R_total).  등급 축은 그대로 (보고 뒤).

  A  케이스 표 (케이스 라우트와 같은 체인) — 옛 행 뒤에 새 행 · H/P 값 · 값 없으면 '—' (0 으로 안 채움) · 상태 (not_computed) 표시
  B  논문 라벨 · single.html 툴팁 · 별칭 — 옛 행 = '비가중' · 'L2-08' · 'not a power share' · 새 행 = 'I²R'
  C  그룹 표 — 'Constriction (비가중)' · 'Constriction I²R' 열 · 낮을수록 좋음 철자 = 열 이름 · group.html 툴팁
  D  보고서 — 옛 줄 이름표 · 새 줄 (constriction_power_share_ion_hertz)
  E  등급 엔진 — 협착 축 값 불변 (새 키를 넣어도) · 설명에 새 열 · 전환 보류 표기
  F  app.py 옛 주석 ("σ_ionic moves while σ_bulk stays fixed") 정정 — 모드 차이 = 접촉 면적 → R_c

  python3 webapp/test_constriction_power_labels.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
_ok, _fail = 0, []


def chk(name, cond, why=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f'  ({why})' if why else ''))


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


OLD = 'Constriction 비율(%)'
NEW = 'Constriction 전력 몫 (I²R · %)'
BASE = {'sigma_full_mScm': 0.12, 'sigma_full_mScm_physics': 0.30, 'bulk_resistance_fraction': 0.2337,
        'bulk_resistance_fraction_physics': 0.2177, 'phi_se': 0.30, 'sigma_bulk_net_mScm': 0.5}
LW = dict(BASE, constriction_power_share_ion_hertz=0.7861, constriction_power_share_ion_hertz_status='computed',
          constriction_power_share_ion_physics=0.8277, constriction_power_share_ion_physics_status='computed')


def main():
    import app as webapp

    def render(metrics, csv_net):
        data = [['Porosity(%)', 15.0], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
        if csv_net:
            data = [['Porosity(%)', 15.0], ['── Network Solver (Hertzian DEM-native) ──', ''], ['σ_ionic (mS/cm)', 0.12],
                    [OLD, round((1 - metrics['bulk_resistance_fraction']) * 100, 1)], ['── 응력 ──', ''], ['Stress CV(%)', 40.0]]
        tbl = {'network_summary': {'columns': ['지표', '값'], 'data': [list(r) for r in data]}}
        mm = dict(metrics)
        webapp.transform_network_summary_4col(tbl, mm, {})
        webapp.inject_tier1_patch_rows(tbl, mm)
        webapp.inject_stage_e_rows(tbl, mm)
        webapp.inject_cell_asr_rows(tbl, mm, {})
        webapp.normalize_network_summary_layout(tbl, mm)
        raw = [list(r) for r in tbl['network_summary']['data']]
        webapp.apply_paper_labels(tbl)
        return raw, [list(r) for r in tbl['network_summary']['data']]

    def row(rows, label):
        return next((r for r in rows if isinstance(r, list) and r and str(r[0]).strip() == label), None)

    print('A  케이스 표')
    for nm, csv_net in (('Step 4', False), ('Step 4b', True)):
        raw, paper = render(LW, csv_net)
        lab = [str(r[0]).strip() for r in raw if r]
        r_new, r_old = row(raw, NEW), row(raw, OLD)
        chk(f'A1 [{nm}] 새 행 = 78.6 (H) · 82.8 (P) · 옛 행 바로 뒤 · 한 번',
            r_new is not None and r_new[1] == 78.6 and r_new[2] == 82.8 and lab.count(NEW) == 1
            and r_old is not None and lab.index(NEW) == lab.index(OLD) + 1, repr((r_old, r_new)))
        chk(f'A1b [{nm}] 옛 행 값 그대로 (76.6 · 78.2)', r_old is not None and r_old[1] == 76.6 and r_old[2] == 78.2, repr(r_old))
        raw0, _ = render(BASE, csv_net)
        r0 = row(raw0, NEW)
        chk(f'A2 [{nm}] 새 키 없는 옛 케이스 → 새 행 "—" (0 으로 안 채움)', r0 is not None and r0[1] == '—' and r0[2] == '—', repr(r0))
    m3 = dict(BASE, constriction_power_share_ion_hertz=None, constriction_power_share_ion_hertz_status='not_computed (no percolating FULL solution)')
    raw3, _ = render(m3, False)
    r3 = row(raw3, NEW)
    chk('A3 상태 not_computed → "—" (H) · physics 키도 없으면 "—"', r3 is not None and r3[1] == '—' and r3[2] == '—', repr(r3))
    m4 = dict(LW)
    m4.pop('constriction_power_share_ion_physics')
    raw4, _ = render(m4, False)
    r4 = row(raw4, NEW)
    chk('A4 physics 값 없음 → physics 칸 "—" (Hertz 값을 복사하지 않는다 — TAU-21 과 같은 규칙)', r4 is not None and r4[1] == 78.6 and r4[2] == '—', repr(r4))

    print('B  라벨 · 툴팁')
    PL = webapp._PAPER_LABEL_MAP
    chk('B1 옛 행 논문 라벨 = 비가중 · L2-08 · not a power share', OLD in PL and 'unweighted' in PL[OLD] and 'L2-08' in PL[OLD]
        and 'not a power share' in PL[OLD], PL.get(OLD))
    chk('B2 새 행 논문 라벨 = I²R · same FULL solution', NEW in PL and 'I²R' in PL[NEW] and 'FULL' in PL[NEW], PL.get(NEW))
    html = _read('webapp/templates/single.html')
    chk('B3 별칭 표 — 두 논문 라벨 → 원 라벨', f"'{PL.get(OLD)}': '{OLD}'" in html and f"'{PL.get(NEW)}': '{NEW}'" in html)
    chk('B4 옛 논문 라벨 (Constriction-resistance fraction (%)) 별칭 키 없음', "'Constriction-resistance fraction (%)'" not in html)
    i = html.find(f"'{NEW}': {{")
    chk('B5 새 행 툴팁 — Σ I²R_c / Σ I²R_total · 관통 간선 · 가상 전극 제외 · 반례 8.18', i >= 0 and all(
        w in html[i:i + 1400] for w in ('I²R_c', '관통', '가상 전극', '8.18')), html[i:i + 200] if i >= 0 else '')

    print('C  그룹 표')
    gk = {lab_: key for lab_, _u, key, _g in webapp.GROUP_DISPLAY_KEYS}
    chk('C1 그룹 열 — Constriction (비가중) = _constriction_pct · Constriction I²R = _constriction_power_pct',
        gk.get('Constriction (비가중)') == '_constriction_pct' and gk.get('Constriction I²R') == '_constriction_power_pct', repr([k for k in gk if 'Constr' in k]))
    chk('C2 낮을수록 좋음 = 열 이름 철자 (두 열)', {'Constriction (비가중)', 'Constriction I²R'} <= webapp.GROUP_LOWER_BETTER
        and 'Constriction' not in webapp.GROUP_LOWER_BETTER)
    src = _read('webapp/app.py')
    chk('C3 그룹 로드 유도 — _constriction_power_pct = constriction_power_share_ion_hertz × 100',
        "metrics['_constriction_power_pct']" in src and 'constriction_power_share_ion_hertz' in src[src.find("metrics['_constriction_power_pct']") - 400:src.find("metrics['_constriction_power_pct']") + 200])
    ghtml = _read('webapp/templates/group.html')
    chk('C4 group.html 툴팁 — 두 열 이름', "'Constriction (비가중)':" in ghtml and "'Constriction I²R':" in ghtml)

    print('D  보고서')
    ir = src.find("if metrics.get('bulk_resistance_fraction') is not None:\n            L.append(")
    blk = src[ir:ir + 900] if ir >= 0 else ''
    chk('D1 보고서 — 옛 줄 "비가중" 이름표 · 새 줄 constriction_power_share_ion_hertz', '비가중' in blk and 'constriction_power_share_ion_hertz' in blk, blk[:300])

    print('E  등급 엔진')
    import grade_engine as G
    lab_c = next(ax['label'] for ax in G.AXES if ax.get('key') == '__constriction_R_fraction_pct')   # axis_values = {이름표: 값}
    a0 = G.axis_values(dict(BASE)).get(lab_c)
    a1 = G.axis_values(dict(LW)).get(lab_c)
    chk('E1 협착 축 값 불변 — 새 키를 넣어도 같다 (전환은 등급값 보고 뒤) · 값 = (1 − bf_physics) × 100',
        a0 is not None and a0 == a1 and abs(a0 - (1 - BASE['bulk_resistance_fraction_physics']) * 100) < 1e-9, repr((a0, a1)))
    gsrc = _read('scripts/grade_engine.py')
    i = gsrc.find("'key': '__constriction_R_fraction_pct'")
    chk('E2 협착 축 설명 — 새 열 이름 · 전환 보류', i >= 0 and 'constriction_power_share_ion_hertz' in gsrc[i:i + 1200])

    print('F  옛 주석')
    chk('F1 "σ_ionic moves while σ_bulk stays fixed" 주석 없음 · 모드 차이 = 접촉 면적 → R_c', 'σ_ionic moves while σ_bulk stays fixed' not in src
        and '접촉 면적' in src[src.find("bf_h = metrics.get('bulk_resistance_fraction')") - 600:src.find("bf_h = metrics.get('bulk_resistance_fraction')")])

    print(f'\n{_ok}/{_ok + len(_fail)} PASS' + ('' if not _fail else '  — FAIL: ' + ' · '.join(_fail)))
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())
