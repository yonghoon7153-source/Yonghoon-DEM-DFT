#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""④b Love–Weber 입자 응력 — 웹앱 같은 묶음 (J20-s · 1저자 비준 10-04 · 원장 LHS-29 · J20-l 코드 → 웹앱 순차).

옛 열 (`stress_cv` · `stress_ratio_<상>`) = LIGGGHTS stress/atom (접촉 virial 50/50 분할) · 대각 성분 — 값 · 키는 그대로, **이름표만** 정정.
새 열 (`stress_cv_lw` · `stress_ratio_<상>_lw` · `_nowall` · 벽 비율 · 상태) 을 케이스 표 · 그룹 표 · 그룹 그림 · 보고서 · 툴팁에.
등급 축 (기계적 안정성 = stress_cv) 은 **바꾸지 않는다** — 바뀌는 등급값 보고 뒤 (②b TAU-03 과 같은 절차).

  A  케이스 표 (transform → tier1 → Stage E → ASR → 정규화 → 논문 라벨 — 케이스 라우트와 같은 체인)
     A1 옛 세대 CSV (옛 네 줄만) + LW 키 있는 metrics → LW 줄 (값) · 벽 제외 · 벽 비율 · 상태 OK 가 옛 줄 뒤에 선다
     A2 LW 키 없는 옛 케이스 → LW 줄 '—' (0 으로 안 채움) · 상태 = NOT_COMPUTED (재분석 전)
     A3 상태 FAILED → 값 줄 '—' · 상태 줄에 사유
     A4 새 세대 CSV (analyze_contacts 가 LW 줄을 이미 씀) → 중복 없음
     A5 논문 라벨: 옛 줄 = 'stress/atom' · '50/50' · 'diagonal' 표기 · 새 줄 = 'Love–Weber' · 머리 = 두 규약
  B  single.html 툴팁 · 별칭 (PAPER_TO_ORIG) — 옛 툴팁에 50/50 · 대각 · LHS-29 · 새 줄마다 툴팁 · 새 논문 라벨 → 원 라벨
  C  그룹 표 — LW 열 · '낮을수록 좋음' 철자 = 열 이름 · group.html 툴팁
  D  보고서 (Physics Derivations) — 옛 줄 이름표 · 상 비 키 = stress_ratio_<상> (옛 판은 없는 키 sigma_AM_P_ratio 를 읽어 안 보였다) · LW 줄
  E  등급 엔진 — stress_cv 축 값은 stress_cv 만 본다 (LW 키를 넣어도 같은 값) · 설명에 규약 한정어
  F  그룹 그림 — LW 값 없는 케이스는 0 으로 그리지 않는다 · 두 규약 같이 (옛 = 점선)
  G  표 재생성 (rebuild_tables_from_metrics) — LW 키 있으면 줄 · 없으면 줄 없음

  python3 webapp/test_stress_lw_labels.py
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
    return cond


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


LW_CV = 'Stress CV — Love–Weber (%)'
LW_R = {p: f'σ_{p}/σ_mean — Love–Weber' for p in ('AM_P', 'AM_S', 'SE')}
LW_CVN = 'Stress CV — Love–Weber · 벽 접촉 제외 (%)'
LW_RN = {p: f'σ_{p}/σ_mean — Love–Weber · 벽 접촉 제외' for p in ('AM_P', 'AM_S', 'SE')}
LW_WALL = '벽 접촉 입자 (%) — 바닥 · 판'
LW_ST = 'Love–Weber 상태 (④b · LHS-29)'
OLD = ['Stress CV(%)', 'σ_AM_P/σ_mean', 'σ_AM_S/σ_mean', 'σ_SE/σ_mean']
NEW = [LW_CV, LW_R['AM_P'], LW_R['AM_S'], LW_R['SE'], LW_CVN, LW_RN['AM_P'], LW_RN['AM_S'], LW_RN['SE'], LW_WALL, LW_ST]

MET_LW = {'stress_cv': 213.1, 'stress_ratio_AM_P': 0.884, 'stress_ratio_AM_S': 1.085, 'stress_ratio_SE': 0.999,
          'stress_lw_status': 'OK', 'stress_lw_definition': 'love_weber_branch_full_tensor_v1',
          'stress_cv_lw': 120.7, 'stress_ratio_AM_P_lw': 2.737, 'stress_ratio_AM_S_lw': 2.341, 'stress_ratio_SE_lw': 0.981,
          'stress_cv_lw_nowall': 122.9, 'stress_ratio_AM_P_lw_nowall': 3.016, 'stress_ratio_AM_S_lw_nowall': 2.446,
          'stress_ratio_SE_lw_nowall': 0.982, 'stress_lw_wall_frac_AM_P': 0.417, 'stress_lw_wall_frac_AM_S': 0.200,
          'stress_lw_wall_frac_SE': 0.098, 'stress_lw_n_wall_floor': 2214, 'stress_lw_n_wall_plate': 1104,
          'stress_lw_plate_flag': 'mesh', 'stress_lw_wall_scope': 'floor_zplane0+mesh_plate (x·y periodic assumed)'}
MET_OLD = {k: MET_LW[k] for k in ('stress_cv', 'stress_ratio_AM_P', 'stress_ratio_AM_S', 'stress_ratio_SE')}


def main():
    import app as webapp

    def render(metrics, extra_rows=()):
        data = [['Porosity(%)', 15.0], ['── 응력 ──', ''], ['Stress CV(%)', metrics.get('stress_cv', 40.0)],
                ['σ_AM_P/σ_mean', metrics.get('stress_ratio_AM_P', 1.0)], ['σ_AM_S/σ_mean', metrics.get('stress_ratio_AM_S', 1.0)],
                ['σ_SE/σ_mean', metrics.get('stress_ratio_SE', 1.0)]] + [list(r) for r in extra_rows]
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

    def num(x):
        try:
            return float(str(x))
        except (TypeError, ValueError):
            return None

    print('A  케이스 표')
    raw, paper = render(MET_LW)
    lab = [str(r[0]).strip() for r in raw if r]
    chk('A1a 옛 세대 CSV + LW 키 → 새 줄 10 개 전부 · 각 한 번', all(lab.count(n) == 1 for n in NEW), repr([n for n in NEW if lab.count(n) != 1]))
    chk('A1b 값 = metrics (반올림 1 · 3 자리) — CV 120.7 · AM_P 2.737 · 벽 제외 AM_P 3.016',
        num((row(raw, LW_CV) or [None, None])[1]) == 120.7 and num((row(raw, LW_R['AM_P']) or [None, None])[1]) == 2.737
        and num((row(raw, LW_RN['AM_P']) or [None, None])[1]) == 3.016, repr([row(raw, LW_CV), row(raw, LW_R['AM_P'])]))
    w = row(raw, LW_WALL)
    chk('A1c 벽 비율 줄 = "AM_P 41.7 · AM_S 20.0 · SE 9.8"', w is not None and w[1] == 'AM_P 41.7 · AM_S 20.0 · SE 9.8', repr(w))
    st = row(raw, LW_ST)
    chk('A1d 상태 줄 = OK', st is not None and str(st[1]).startswith('OK'), repr(st))
    io = [lab.index(n) for n in OLD + NEW if n in lab]
    chk('A1e 순서 — 옛 네 줄 → LW 열 줄 (정규화 정렬 표 그대로)', io == sorted(io) and len(io) == 14, repr(io))
    raw2, _ = render(MET_OLD)
    vals2 = {n: row(raw2, n) for n in NEW}
    chk('A2 LW 키 없는 옛 케이스 → 값 줄 "—" (0 으로 안 채움)',
        all(r is not None and r[1] == '—' and r[2] == '—' for n, r in vals2.items() if n not in (LW_ST,)), repr(vals2))
    st2 = row(raw2, LW_ST)
    chk('A2b 상태 = NOT_COMPUTED (재분석 전 케이스 — 접촉 단계 재실행)', st2 is not None and 'NOT_COMPUTED' in str(st2[1]) and '재분석' in str(st2[1]), repr(st2))
    m3 = dict(MET_OLD, stress_lw_status='FAILED (virial_mismatch: 0.33 > 0.01)')
    raw3, _ = render(m3)
    st3 = row(raw3, LW_ST)
    chk('A3 FAILED → 값 줄 "—" · 상태 줄에 사유', st3 is not None and 'virial_mismatch' in str(st3[1])
        and (row(raw3, LW_CV) or [0, 0])[1] == '—', repr(st3))
    extra = [[LW_CV, 120.7], [LW_R['AM_P'], 2.737], [LW_R['SE'], 0.981], [LW_CVN, 122.9], [LW_WALL, 'AM_P 41.7 · AM_S 20.0 · SE 9.8']]
    raw4, _ = render(MET_LW, extra)
    lab4 = [str(r[0]).strip() for r in raw4 if r]
    chk('A4 새 세대 CSV (LW 줄을 이미 씀) → 중복 없음', all(lab4.count(n) == 1 for n in NEW), repr([(n, lab4.count(n)) for n in NEW]))
    PL, PS = webapp._PAPER_LABEL_MAP, webapp._PAPER_SECTION_MAP
    chk('A5a 옛 네 줄 논문 라벨 = "stress/atom" · "50/50" · 대각 (diagonal) 표기',
        all(k in PL and 'stress/atom' in PL[k] and '50/50' in PL[k] and 'diagonal' in PL[k] for k in OLD), repr([PL.get(k) for k in OLD]))
    chk('A5b 새 줄 논문 라벨 = "Love–Weber" (상태 · 벽 비율 줄 포함)', all(k in PL and 'Love–Weber' in PL[k] or (k == LW_WALL and k in PL) for k in NEW),
        repr([k for k in NEW if k not in PL]))
    chk('A5c 응력 머리 = 두 규약 표기 (stress/atom 50/50 · Love–Weber)', 'stress/atom' in PS.get('── 응력 ──', '') and 'Love–Weber' in PS.get('── 응력 ──', ''),
        PS.get('── 응력 ──'))
    chk('A5d 논문 라벨 적용 뒤에도 옛 값 그대로 (213.1 · 0.884)', any(r and r[0] == PL['Stress CV(%)'] and num(r[1]) == 213.1 for r in paper)
        and any(r and r[0] == PL['σ_AM_P/σ_mean'] and num(r[1]) == 0.884 for r in paper))
    src = _read('webapp/app.py')
    ci = src.find('_CANONICAL_ROW_ORDER = [')
    canon = src[ci:src.find(']', src.find("'ASR_thermal", ci))]
    chk('A6 정렬 표 — σ_SE/σ_mean 뒤에 LW 줄 순서대로', all(f"'{n}'" in canon for n in NEW)
        and canon.find("'σ_SE/σ_mean'") < canon.find(f"'{LW_CV}'") < canon.find(f"'{LW_ST}'"))

    print('B  single.html 툴팁 · 별칭')
    html = _read('webapp/templates/single.html')
    i0 = html.find("'Stress CV(%)': {")
    old_tip = html[i0:html.find('},', html.find("'σ_SE/σ_mean': {", i0)) + 2] if i0 >= 0 else ''
    chk('B1 옛 툴팁 넷 — "50/50" · "대각" · "LHS-29" 표기', old_tip.count('50/50') >= 4 and '대각' in old_tip and 'LHS-29' in old_tip, old_tip[:200])
    chk('B2 새 줄마다 툴팁', all(f"'{n}': {{" in html for n in NEW), repr([n for n in NEW if f"'{n}': {{" not in html]))
    chk('B3 별칭 표 — 새 논문 라벨 → 원 라벨 (옛 줄 넷 + 새 줄 전부)', all(n in PL and f"'{PL[n]}': '{n}'" in html for n in OLD + NEW),
        repr([n for n in OLD + NEW if n not in PL or f"'{PL[n]}': '{n}'" not in html]))
    chk('B4 옛 논문 라벨 (규약 표기 없던 것) 별칭 키 없음',
        "'von-Mises stress ratio, ⟨σ_VM⟩_AM_P / ⟨σ_VM⟩_all'" not in html
        and "'Particle-stress coefficient of variation, CV(σ_VM) (%)'" not in html)
    i1 = html.find(f"'{LW_CV}': {{")
    chk('B5 LW CV 툴팁 = 접촉점 (branch) · 전체 텐서 · 벽 접촉 · 등급 축은 옛 규약', i1 >= 0 and all(
        w_ in html[i1:i1 + 1600] for w_ in ('접촉점', '전체 텐서', '벽', '등급')), html[i1:i1 + 300] if i1 >= 0 else '')

    print('C  그룹 표')
    gk = {lab_: key for lab_, _u, key, _g in webapp.GROUP_DISPLAY_KEYS}
    chk('C1 그룹 표 LW 열 — Stress CV LW · σ_<상>/σ_mean LW · Stress CV LW (벽 제외)',
        gk.get('Stress CV LW') == 'stress_cv_lw' and gk.get('σ_AM_P/σ_mean LW') == 'stress_ratio_AM_P_lw'
        and gk.get('σ_SE/σ_mean LW') == 'stress_ratio_SE_lw' and gk.get('Stress CV LW (벽 제외)') == 'stress_cv_lw_nowall', repr(gk))
    chk('C1b 옛 열 이름에 규약 표기 (50/50)', 'Stress CV (50/50)' in gk and gk['Stress CV (50/50)'] == 'stress_cv', repr([k for k in gk if 'Stress' in k]))
    chk('C2 낮을수록 좋음 = 열 이름과 같은 철자 (옛 · 새 CV)', {'Stress CV (50/50)', 'Stress CV LW', 'Stress CV LW (벽 제외)'} <= webapp.GROUP_LOWER_BETTER
        and all(n in gk for n in webapp.GROUP_LOWER_BETTER if 'Stress' in n), repr(sorted(n for n in webapp.GROUP_LOWER_BETTER if 'Stress' in n)))
    ghtml = _read('webapp/templates/group.html')
    chk('C3 group.html 툴팁 — 새 열 · 옛 열 이름', all(f"'{n}':" in ghtml for n in ('Stress CV (50/50)', 'Stress CV LW', 'σ_AM_P/σ_mean LW', 'Stress CV LW (벽 제외)')))

    print('D  보고서')
    ir = src.find("        if metrics.get('stress_cv'):\n")
    ir = ir if ir >= 0 and src.find('### Electronic / Thermal / Mechanical') < ir else -1
    blk = src[ir:ir + 2600] if ir >= 0 else ''
    chk('D1 보고서 상 비 키 = stress_ratio_<상> (옛 판은 없는 키 목록 [sigma_AM_P_ratio, …] 을 읽었다)',
        "['sigma_AM_P_ratio', 'sigma_AM_S_ratio', 'sigma_SE_ratio']" not in src and "metrics.get(f'stress_ratio_{ph}')" in blk, blk[:300])
    chk('D2 보고서 — 옛 줄 이름표 50/50 · LW 줄 (stress_cv_lw)', '50/50' in blk and 'stress_cv_lw' in blk and 'Love–Weber' in blk, blk[:400])

    print('E  등급 엔진')
    import grade_engine as G
    lab_s = next(ax['label'] for ax in G.AXES if ax.get('key') == '__sigma_vm_cv_pct')      # axis_values = {이름표: 값}
    v0 = G.axis_values(dict(MET_OLD)).get(lab_s)
    v1 = G.axis_values(dict(MET_OLD, **{k: v for k, v in MET_LW.items() if 'lw' in k})).get(lab_s)
    chk('E1 등급 축 값 불변 — LW 키를 더해도 같은 값 = 옛 stress_cv (213.1) · 전환은 등급값 보고 뒤',
        v0 is not None and v0 == v1 == MET_OLD['stress_cv'], repr((v0, v1)))
    gsrc = _read('scripts/grade_engine.py')
    chk('E2 등급 축 설명 — 50/50 분할 · LHS-29 한정어', '50/50' in gsrc and 'LHS-29' in gsrc)
    chk('E3 쉬운 툴팁 __sigma_vm_cv_pct — 옛 규약 · Love–Weber 전환 보류 표기',
        '50/50' in src[src.find("'__sigma_vm_cv_pct':"):src.find("'__sigma_vm_cv_pct':") + 500])

    print('F  그룹 그림')
    import matplotlib
    matplotlib.use('Agg')
    import generate_comparison_plots as GP
    data = [dict(MET_LW), dict(MET_OLD), dict(MET_LW, stress_cv_lw=100.0)]
    ax = GP.plot_stress_cv(data, ['a', 'b', 'c'], ax=matplotlib.pyplot.subplots()[1])
    ys = [list(l.get_ydata()) for l in ax.get_lines()]
    lw_line = [y for y in ys if 120.7 in [round(v, 1) for v in y if v == v]]
    chk('F1 Stress CV 그림 — LW 선은 값 있는 케이스만 (0 없음)', lw_line and all(v != 0 for v in lw_line[0]) and len(lw_line[0]) == 2, repr(ys))
    chk('F1b 옛 규약 선 (50/50) 도 같이 — 선 둘', len(ax.get_lines()) >= 2 and any(l.get_linestyle() in ('--', 'dashed') for l in ax.get_lines()))
    ax2 = GP.plot_stress_ratio(data, ['a', 'b', 'c'], ax=matplotlib.pyplot.subplots()[1])
    zero_lines = [list(l.get_ydata()) for l in ax2.get_lines() if any(v == 0 for v in l.get_ydata())]
    chk('F2 Stress Ratio 그림 — 0 으로 그린 점 없음 (LW 없는 케이스 빠짐)', not zero_lines, repr(zero_lines))

    print('G  표 재생성')
    import rebuild_tables_from_metrics as RB
    rows = RB.network_summary(dict(MET_LW))
    labs = [r['지표'] for r in rows]
    chk('G1 LW 키 있으면 줄 (CV · 비 · 벽 제외)', LW_CV in labs and LW_R['AM_P'] in labs and LW_CVN in labs, repr(labs))
    rows0 = RB.network_summary(dict(MET_OLD))
    chk('G2 LW 키 없으면 줄 없음 (만들지 않는다)', not any('Love–Weber' in r['지표'] for r in rows0))

    print(f'\n{_ok}/{_ok + len(_fail)} PASS' + ('' if not _fail else '  — FAIL: ' + ' · '.join(_fail)))
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())
