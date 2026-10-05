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
  R  RGL-06 (Codex 10-05 · 1저자 비준 "권고대로") — 이름 한정 · 상태 (같은 묶음 · J20-l)
     R1 상태 UNDEFINED (무하중 — CV · 비 0/0) → 값 줄 '—' · 상태 줄에 사유 (0 으로 안 채움)
     R2 상태 OK 인데 계약 v2 표지 없음 (10-05 이전 · 입력 검증 전 세대) → 상태 줄에 '입력 검증 전' · 재분석 권장 (값은 그대로)
     R3 논문 라벨 — LW 줄 = 입자 접촉력 기반 대칭 응력 (kinetic · 벽 · couple 미포함) · 벽 제외 = 선별 모집단 (벽 힘 복원 아님) ·
        상태 = 전역 virial 부호/척도 (프레임 대응 증명 아님) · 'full tensor' 표기 없음 (전체 동적 응력으로 읽히지 않게)
     R4 single.html 툴팁 — LW CV · 벽 제외 · 상태 줄의 한정어 · 덱 가정 미검증 · UNDEFINED · invalid_input
     R5 group.html 툴팁 · 보고서 · 그룹 그림 범례 — 같은 한정어
  V  LHS-33 (좁은 개정 · 1저자 비준 10-05 · Codex 재검증 Q7 · 같은 묶음 · J20-l) — 옛 σ_VM 네 열이 무효 · 미정의
     (stress_cv_status ≠ computed) 면 '—' + 사유 (0 · None 으로 안 보임) · 옛 세대 (상태 키 없음) · 정상은 그대로
     V1 케이스 표 — 값 줄 '—' · 상태 줄 (상태 — 사유) · 정상 · 옛 세대는 옛 줄 그대로 · 상태 줄 없음
     V2 정렬 표 · 논문 라벨 · single.html 툴팁 · 별칭 (PAPER_TO_ORIG)
     V3 그룹 표 — '— (짧은 사유)' 칸 (None 이 'None' 으로 보이지 않게) · 최고값 후보 아님 · group() 이 같은 도우미를 부른다
     V4 보고서 — 무효면 '—' + 사유 줄 · V5 등급 쉬운 툴팁 · 축 설명 · group.html 툴팁 · single.html 옛 줄 툴팁에 LHS-33

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
          'stress_lw_contract': 'love_weber_checks_v2',
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
    chk('B5 LW CV 툴팁 = 접촉점 (branch) · 9 성분 텐서 (대각만 아님 — RGL-06 뒤 "전체 텐서" 대신) · 벽 접촉 · 등급 축은 옛 규약',
        i1 >= 0 and all(w_ in html[i1:i1 + 1800] for w_ in ('접촉점', '9 성분', '벽', '등급')), html[i1:i1 + 300] if i1 >= 0 else '')

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

    print('R  RGL-06 이름 한정 · 상태')
    m_u = dict(MET_OLD, stress_lw_status='UNDEFINED (zero_load: max|F| = 0 — 평균 σ_VM = 0 → CV · 상 비 = 0/0 미정의 · 0 으로 채우지 않음)',
               stress_lw_contract='love_weber_checks_v2')
    raw_u, _ = render(m_u)
    st_u = row(raw_u, LW_ST)
    chk('R1 상태 UNDEFINED (무하중) → 값 줄 "—" · 상태 줄에 UNDEFINED · zero_load (0 으로 안 채움)',
        st_u is not None and 'UNDEFINED' in str(st_u[1]) and 'zero_load' in str(st_u[1])
        and all((row(raw_u, n) or [0, 0])[1] == '—' for n in NEW if n not in (LW_ST,)), repr(st_u))
    m_v1 = {k: v for k, v in MET_LW.items() if k != 'stress_lw_contract'}
    raw_v1, _ = render(m_v1)
    st_v1 = row(raw_v1, LW_ST)
    chk('R2 OK 인데 계약 v2 표지 없음 (10-05 이전 세대) → 상태 줄 "OK" 로 시작 · "입력 검증 전" · RGL-06 · 재분석 (값 줄은 그대로)',
        st_v1 is not None and str(st_v1[1]).startswith('OK') and '입력 검증 전' in str(st_v1[1]) and 'RGL-06' in str(st_v1[1])
        and '재분석' in str(st_v1[1]) and num((row(raw_v1, LW_CV) or [None, None])[1]) == 120.7, repr(st_v1))
    chk('R2b 계약 v2 표지가 있으면 상태 줄 = "OK" 그대로 (경고 없음)', st is not None and str(st[1]) == 'OK', repr(st))
    m_nw = {k: v for k, v in MET_LW.items() if '_nowall' not in k}
    m_nw['stress_lw_nowall_status'] = 'UNDEFINED (zero_mean_vm: 벽 안 닿은 입자의 평균 σ_VM = 0 → CV · 상 비 = 0/0 미정의)'
    raw_nw, _ = render(m_nw)
    st_nw = row(raw_nw, LW_ST)
    chk('R2c 전체 OK · 벽 제외 모집단 UNDEFINED → 벽 제외 값 줄 "—" · 상태 줄에 "벽 제외: UNDEFINED" (빈칸의 이유)',
        st_nw is not None and str(st_nw[1]).startswith('OK') and '벽 제외' in str(st_nw[1]) and 'UNDEFINED' in str(st_nw[1])
        and (row(raw_nw, LW_CVN) or [0, 0])[1] == '—' and num((row(raw_nw, LW_CV) or [None, None])[1]) == 120.7, repr(st_nw))
    plw = [PL.get(k, '') for k in (LW_CV, LW_R['AM_P'], LW_R['AM_S'], LW_R['SE'])]
    chk('R3a 논문 라벨 — LW CV · 상 비 = particle-contact (입자 접촉력) · CV 는 symmetric · kinetic · couple 미포함 표기',
        all('particle-contact' in p for p in plw) and 'symmetric' in plw[0] and 'kinetic' in plw[0] and 'couple' in plw[0], repr(plw))
    pnw = [PL.get(k, '') for k in (LW_CVN, LW_RN['AM_P'], LW_RN['AM_S'], LW_RN['SE'])]
    chk('R3b 논문 라벨 — 벽 제외 줄 = selected population (선별 모집단)', all('selected population' in p for p in pnw)
        and 'not restored' in pnw[0], repr(pnw))
    chk('R3c 논문 라벨 — 상태 줄 = global virial · not a frame-correspondence proof · 벽 비율 줄 = deck geometry not verified',
        'global' in PL.get(LW_ST, '') and 'not a frame' in PL.get(LW_ST, '') and 'not verified' in PL.get(LW_WALL, ''),
        repr((PL.get(LW_ST), PL.get(LW_WALL))))
    chk('R3d "full tensor" 표기 없음 (전체 동적 응력으로 읽히지 않게) · 응력 머리 = particle-contact-force',
        not any('full tensor' in PL.get(k, '') for k in NEW) and 'particle-contact' in PS.get('── 응력 ──', ''),
        repr([PL.get(k) for k in NEW if 'full tensor' in PL.get(k, '')]))

    def _tip(label, span=1800):
        i = html.find(f"'{label}': {{")
        return html[i:i + span] if i >= 0 else ''
    t_cv = _tip(LW_CV)
    t_cv = t_cv[:t_cv.find('\n  },') + 1] if '\n  },' in t_cv else t_cv
    chk('R4a LW CV 툴팁 — 입자 접촉력 기반 대칭 응력의 VM · kinetic · couple · 전체 동적 응력 아님 · 9 성분 · 전역 virial (프레임 대응 증명 아님)',
        all(w_ in t_cv for w_ in ('입자 접촉력', '대칭', 'kinetic', 'couple', '전체 동적 응력 아님', '9 성분', '전역', '프레임')), t_cv[:300])
    t_nw = [_tip(n) for n in (LW_CVN, LW_RN['AM_P'], LW_RN['AM_S'], LW_RN['SE'])]
    chk('R4b 벽 제외 툴팁 넷 — 선별 모집단 · 결측 벽 힘 복원 아님', all('선별 모집단' in t and '복원' in t for t in t_nw), repr([t[:120] for t in t_nw]))
    t_st = _tip(LW_ST)
    chk('R4c 상태 툴팁 — UNDEFINED · invalid_input · 전역 (프레임 대응 증명 아님) · 덱 가정 미검증 · 계약 v2',
        all(w_ in t_st for w_ in ('UNDEFINED', 'invalid_input', '전역', '프레임', '덱', '검증', 'love_weber_checks_v2')), t_st[:300])
    t_wl = _tip(LW_WALL)
    chk('R4d 벽 비율 툴팁 — 덱 가정 (바닥 z = 0 · 평면 mesh 판 · x·y 주기) 을 함수가 검증하지 않음',
        all(w_ in t_wl for w_ in ('z = 0', 'mesh', '주기', '검증')), t_wl[:300])
    gi = ghtml.find("'Stress CV LW':")
    g_cv = ghtml[gi:ghtml.find('\n', gi)] if gi >= 0 else ''
    gj = ghtml.find("'Stress CV LW (벽 제외)':")
    g_nw = ghtml[gj:ghtml.find('\n', gj)] if gj >= 0 else ''
    chk('R5a group.html — Stress CV LW 툴팁 = 입자 접촉력 · 대칭 · kinetic · couple 미포함 · (벽 제외) = 선별 모집단 · 복원 아님',
        all(w_ in g_cv for w_ in ('입자 접촉력', '대칭', 'kinetic', 'couple')) and '선별 모집단' in g_nw and '복원' in g_nw, repr((g_cv[:200], g_nw[:200])))
    chk('R5b 보고서 — LW 줄에 입자 접촉력 대칭 응력 VM 한정어 · 벽 제외 = 선별 모집단', '입자 접촉력' in blk and '선별 모집단' in blk, blk[:400])
    labs_f = ax.get_legend_handles_labels()[1]
    chk('R5c 그룹 그림 범례 — LW 선 = particle-contact (full tensor 표기 없음)', any('particle-contact' in l for l in labs_f)
        and not any('full tensor' in l for l in labs_f), repr(labs_f))

    print('V  LHS-33 옛 σ_VM 열 상태 (무효 · 미정의 = "—" + 사유)')
    SROW = 'Stress CV 상태 (50/50 · LHS-33)'
    m_bad = dict(MET_LW, stress_cv=None, stress_ratio_AM_P=None, stress_ratio_AM_S=None, stress_ratio_SE=None,
                 stress_cv_status='invalid_input', stress_cv_contract='v2-invalid-null',
                 stress_cv_reason='c_strs 비유한 · 숫자 아님 2 / 2 입자 (id 1, 2)')
    raw_b, paper_b = render(m_bad)
    vals_b = {n: row(raw_b, n) for n in OLD}
    chk('V1a ★ 무효 → 옛 네 값 줄 "—" (두 칸 모두 · None · 0 아님)',
        all(r is not None and r[1] == '—' and r[2] == '—' for r in vals_b.values()), repr(vals_b))
    sb = row(raw_b, SROW)
    chk('V1b ★ 상태 줄 = 상태 — 사유 (invalid_input · c_strs 비유한) · Δ 칸 빈칸 · 한 번만',
        sb is not None and 'invalid_input' in str(sb[1]) and 'c_strs 비유한' in str(sb[1]) and sb[3] == ''
        and [str(r[0]).strip() for r in raw_b if r].count(SROW) == 1, repr(sb))
    lab_b = [str(r[0]).strip() for r in raw_b if r]
    chk('V1c 상태 줄 자리 = 옛 네 줄 뒤 · LW 줄 앞 (정렬 표)', SROW in lab_b and lab_b.index('σ_SE/σ_mean') < lab_b.index(SROW) < lab_b.index(LW_CV),
        repr(lab_b[lab_b.index('Stress CV(%)') - 1:lab_b.index('Stress CV(%)') + 8] if 'Stress CV(%)' in lab_b else lab_b))
    m_u = {k: v for k, v in m_bad.items() if k not in ('stress_ratio_AM_P', 'stress_ratio_AM_S', 'stress_ratio_SE')}
    m_u.update(stress_cv_status='unavailable_no_c_strs', stress_cv_reason='c_strs 열 없음')
    raw_u2, _ = render(m_u)
    chk('V1d c_strs 없음 (unavailable_no_c_strs) → 값 줄 "—" · 상태 줄에 unavailable_no_c_strs',
        (row(raw_u2, 'Stress CV(%)') or [0, 0])[1] == '—' and 'unavailable_no_c_strs' in str((row(raw_u2, SROW) or ['', ''])[1]))
    m_ok = dict(MET_LW, stress_cv_status='computed', stress_cv_contract='v2-invalid-null')
    raw_o, _ = render(m_ok)
    chk('V1e 정상 (computed) → 옛 값 그대로 (213.1 · 0.884) · 상태 줄 없음', num((row(raw_o, 'Stress CV(%)') or [0, 0])[1]) == 213.1
        and num((row(raw_o, 'σ_AM_P/σ_mean') or [0, 0])[1]) == 0.884 and row(raw_o, SROW) is None)
    chk('V1f 옛 세대 (상태 키 없음) → 옛 값 그대로 · 상태 줄 없음 (역사 파일 불변)', row(raw, SROW) is None
        and num((row(raw, 'Stress CV(%)') or [0, 0])[1]) == 213.1)
    m_z = dict(MET_LW, stress_cv=0.0, stress_cv_status='undefined_zero_mean', stress_cv_reason='평균 σ_VM = 0')
    raw_z, _ = render(m_z)
    chk('V1g 상태가 미정의인데 저장된 0 → "—" (상태를 따른다 · 0 을 보이지 않는다)', (row(raw_z, 'Stress CV(%)') or [0, 0])[1] == '—')
    chk('V2a 정렬 표에 상태 줄 (σ_SE/σ_mean 뒤 · LW 앞)', f"'{SROW}'" in canon
        and canon.find("'σ_SE/σ_mean'") < canon.find(f"'{SROW}'") < canon.find(f"'{LW_CV}'"))
    chk('V2b 논문 라벨 — 상태 줄 = stress/atom 50/50 · invalid/undefined → blank (not 0) · LHS-33', 'LHS-33' in PL.get(SROW, '')
        and '50/50' in PL.get(SROW, '') and 'not 0' in PL.get(SROW, ''), PL.get(SROW))
    t_s = _tip(SROW)
    t_s = t_s[:t_s.find('\n  },') + 1] if '\n  },' in t_s else t_s
    chk('V2c single.html 툴팁 — 상태 넷 (computed · unavailable_no_c_strs · invalid_input · undefined_zero_mean) · 0 으로 안 채움 · 등급 안 매김 · '
        'v2-invalid-null', all(w_ in t_s for w_ in ('computed', 'unavailable_no_c_strs', 'invalid_input', 'undefined_zero_mean',
                                                   '0 으로', '등급', 'v2-invalid-null', 'LHS-33')), t_s[:300])
    chk('V2d 별칭 — 상태 줄 논문 라벨 → 원 라벨', SROW in PL and f"'{PL[SROW]}': '{SROW}'" in html)
    t_old = _tip('Stress CV(%)')
    chk('V2e 옛 줄 툴팁에 LHS-33 — 무효 · 미정의면 "—" (0 아님)', 'LHS-33' in t_old[:t_old.find('\n  },')] and '—' in t_old[:t_old.find('\n  },')])
    import metrics_json as MJ
    gc = getattr(MJ, 'stress_cv_group_cells', None)
    g_bad = gc(dict(m_bad)) if callable(gc) else {}
    chk('V3a ★ 그룹 칸 도우미 — 무효면 옛 네 열 = "— (입력 무효)" (None 이 "None" 으로 보이지 않게 · 0 아님)',
        callable(gc) and all(g_bad.get(k) == '— (입력 무효)' for k in ('stress_cv', 'stress_ratio_AM_P', 'stress_ratio_AM_S', 'stress_ratio_SE')),
        repr({k: g_bad.get(k) for k in ('stress_cv', 'stress_ratio_SE')}))
    g_ok = gc(dict(m_ok)) if callable(gc) else {}
    g_old = gc(dict(MET_OLD)) if callable(gc) else {}
    chk('V3b 정상 · 옛 세대 → 값 그대로 (213.1)', g_ok.get('stress_cv') == 213.1 and g_old.get('stress_cv') == 213.1)
    g_u = gc(dict(m_u)) if callable(gc) else {}
    chk('V3c c_strs 없음 · 상 비 키 없음 → stress_cv = "— (c_strs 없음)" · 없는 상 비 키는 만들지 않는다',
        g_u.get('stress_cv') == '— (c_strs 없음)' and 'stress_ratio_AM_P' not in g_u, repr(g_u.get('stress_cv')))
    lab_cv = next(l for l, _u, k, _g in webapp.GROUP_DISPLAY_KEYS if k == 'stress_cv')
    mk = webapp._group_best_marks([{lab_cv: '— (입력 무효)'}, {lab_cv: '150.0'}, {lab_cv: '120.0'}], [(lab_cv, '(%)', 'stress_cv')])
    chk('V3d "— (사유)" 칸은 최고값 후보 아님 (낮을수록 좋음 → 120 강조)', (lab_cv, 2) in mk and (lab_cv, 0) not in mk, repr(sorted(mk)))
    gi0 = src.find('def group():')
    chk('V3e group() 이 같은 도우미 (metrics_json.stress_cv_group_cells) 로 칸을 만든다', gi0 >= 0
        and 'stress_cv_group_cells' in src[gi0:src.find('\ndef ', gi0 + 10)])
    rl = getattr(MJ, 'stress_cv_report_line', None)
    line_b = rl(dict(m_bad)) if callable(rl) else None
    chk('V4a ★ 보고서 줄 도우미 — 무효면 "—" + 상태 — 사유 · LHS-33 · 정상 · 옛 세대면 None',
        callable(rl) and line_b and '—' in line_b and 'invalid_input' in line_b and 'LHS-33' in line_b
        and rl(dict(m_ok)) is None and rl(dict(MET_OLD)) is None, repr(line_b))
    si0 = src.find('def serve_report(')
    chk('V4b serve_report 가 같은 도우미 (stress_cv_report_line) 를 부르고 섹션 조건이 무효 상태도 본다', si0 >= 0
        and 'stress_cv_report_line' in src[si0:src.find('\ndef ', si0 + 10)] and "stress_cv_status" in src[si0:src.find('\ndef ', si0 + 10)])
    es = src[src.find("'__sigma_vm_cv_pct':"):src.find("'__sigma_vm_cv_pct':") + 700]
    chk('V5a 등급 쉬운 툴팁 — 무효 · 미정의는 등급 안 매김 (LHS-33)', 'LHS-33' in es and '등급' in es, es[:300])
    gax = next(ax_ for ax_ in G.AXES if ax_.get('key') == '__sigma_vm_cv_pct')
    chk('V5b 등급 축 설명 — LHS-33 · 무효 · 미정의 = 값 없음 (등급 안 매김)', 'LHS-33' in gax.get('meaning', ''), gax.get('meaning'))
    gs = ghtml.find("'Stress CV (50/50)':")
    g50 = ghtml[gs:ghtml.find('\n', gs)] if gs >= 0 else ''
    chk('V5c group.html 툴팁 — "— (사유)" 칸 · LHS-33', 'LHS-33' in g50 and '— (' in g50, g50[:200])

    print(f'\n{_ok}/{_ok + len(_fail)} PASS' + ('' if not _fail else '  — FAIL: ' + ' · '.join(_fail)))
    return 1 if _fail else 0


if __name__ == '__main__':
    sys.exit(main())
