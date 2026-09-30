#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""닫힌 파라미터 그룹 보기 · 대체 표지 회귀 — 웹앱 ②-b (LHS-24 (e)(f)(g) · 1저자 비준 09-30 밤 · J20-l).

  python3 webapp/test_closed_param_groupview.py      # 종료코드 0 = PASS

  [E] (e) 그룹 비교 표의 최고값 강조: '낮을수록 좋음' 이름 집합이 표의 열 이름과 **같은 철자**여야 한다
      (옛 집합에 porosity union · overlap · CN std 가 없고, 'Vulnerable' 은 표 열 'AM Vulnerable' 과 철자가 달라
      조용히 '높을수록 좋음' 으로 강조됐다) · 집합에 표에 없는 이름이 남지 않는다 · AM–AM CN std 열 (J20-j) 이 표에 있다
  [F] (f) 등급 엔진 · 3D 뷰어가 physics 값이 없어 Hertz 계열 (c_cpl[22]) 값으로 바꿀 때 **표지**를 단다
      (두 값 ≈ 2.7 배 · 같은 라벨로 조용히 섞이던 것) — 대체가 없으면 표지도 없다
  [G] (g) 그룹 그림 체크박스의 모든 값이 그림 목록에 있다 (porosity_union · overlap_fraction_pct → '[SKIP] Unknown' 이던 것) ·
      두 그림은 값이 없는 케이스를 0 으로 그리지 않는다
"""
import csv
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = os.path.join(ROOT, 'scripts')
sys.path.insert(0, HERE)
sys.path.insert(0, SCRIPTS)

_ok, _fail = 0, []


def chk(name, cond, extra=''):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}' + (f' — {extra}' if extra else ''))
    return bool(cond)


def section_e():
    print('[E] 그룹 표 최고값 강조 — 낮을수록 좋음 집합 ↔ 표 열 이름')
    import app as A
    keys = getattr(A, 'GROUP_DISPLAY_KEYS', None)
    lower = getattr(A, 'GROUP_LOWER_BETTER', None)
    best = getattr(A, '_group_best_marks', None)
    if not chk('E0 GROUP_DISPLAY_KEYS · GROUP_LOWER_BETTER · _group_best_marks 가 모듈 수준에 있다',
               keys is not None and lower is not None and callable(best)):
        return
    labels = [k[0] for k in keys]
    by_key = {k[2]: k[0] for k in keys}
    for key in ('porosity', 'porosity_union', 'overlap_fraction_pct', 'thickness_um', 'se_se_cn_std',
                'am_am_cn_std', 'am_vulnerable_pct', 'tortuosity_mean', 'stress_cv'):
        lab = by_key.get(key)
        chk(f'E1 {key} 열이 표에 있고 낮을수록 좋음으로 판정', lab is not None and lab in lower,
            f'label={lab!r}')
    dead = sorted(set(lower) - set(labels))
    chk('E2 낮을수록 좋음 집합에 표에 없는 이름이 없다 (철자가 어긋나면 조용히 반대로 강조된다)', not dead,
        f'표에 없는 이름 {dead}')
    for key in ('se_se_cn', 'percolation_pct', 'coverage_AM_P_mean'):
        lab = by_key.get(key)
        chk(f'E3 {key} 는 높을수록 좋음 (집합 밖)', lab is not None and lab not in lower, f'label={lab!r}')
    lab_u, lab_cn = by_key.get('porosity_union'), by_key.get('se_se_cn')
    rows = [{lab_u: '12.5', lab_cn: '3.1'}, {lab_u: '10.2', lab_cn: '4.0'}, {lab_u: '-', lab_cn: '2.0'}]
    marks = best(rows, [(lab_u, '', 'porosity_union'), (lab_cn, '', 'se_se_cn')])
    chk('E4 ε_union 가장 낮은 행 (10.2) 이 강조 · 값 없는 행은 후보 아님', (lab_u, 1) in marks and (lab_u, 0) not in marks,
        f'marks={sorted(marks)}')
    chk('E5 SE–SE CN 가장 높은 행 (4.0) 이 강조', (lab_cn, 1) in marks and (lab_cn, 2) not in marks,
        f'marks={sorted(marks)}')
    same_rows = [{lab_u: '5.0'}, {lab_u: '5.0'}]
    chk('E6 모든 값이 같으면 강조 없음', not best(same_rows, [(lab_u, '', 'porosity_union')]))


def section_f():
    print('[F] physics → Hertz 대체 표지 — 등급 엔진 · 3D 뷰어')
    import grade_engine as GE
    ax = next((a for a in GE.AXES if a.get('key') == 'coverage_AM_P_mean_physics'), None)
    if not chk('F0 등급 축 coverage_AM_P_mean_physics (대체 coverage_AM_P_mean) 가 있다',
               ax is not None and ax.get('fallback_key') == 'coverage_AM_P_mean'):
        return
    r_fb = GE._grade_axis(ax, {'coverage_AM_P_mean': 20.0}, [])
    note = r_fb.get('fallback_note') or ''
    chk('F1 physics 없음 → Hertz 값으로 채울 때 fallback_note 에 "Hertz" 표지', 'Hertz' in note, f'note={note!r}')
    chk('F2 같은 표지가 basis (툴팁 · 보고서) 에도 들어간다', 'Hertz' in (r_fb.get('basis') or ''),
        f'basis={r_fb.get("basis")!r}')
    chk('F3 source_key = 실제로 읽은 키 (coverage_AM_P_mean)', r_fb.get('source_key') == 'coverage_AM_P_mean',
        f'source_key={r_fb.get("source_key")!r}')
    chk('F4 값은 그대로 (대체값 20.0 — 계산 불변)', r_fb.get('value') == 20.0, f'value={r_fb.get("value")!r}')
    r_ok = GE._grade_axis(ax, {'coverage_AM_P_mean_physics': 54.0, 'coverage_AM_P_mean': 20.0}, [])
    chk('F5 physics 가 있으면 표지 없음 · source_key = physics 키',
        not r_ok.get('fallback_note') and r_ok.get('source_key') == 'coverage_AM_P_mean_physics',
        f'note={r_ok.get("fallback_note")!r} src={r_ok.get("source_key")!r}')
    ax_b3 = next((a for a in GE.AXES if a.get('key') == 'coverage_AM_mean_physics_rough'), None)
    if ax_b3 is not None:
        r_b3 = GE._grade_axis(ax_b3, {'coverage_AM_mean_physics': 40.0}, [])
        nb = r_b3.get('fallback_note') or ''
        chk('F6 physics → physics 대체 (B3 없음) 는 표지를 달되 "Hertz" 라 부르지 않는다',
            bool(nb) and 'Hertz' not in nb and 'coverage_AM_mean_physics' in nb, f'note={nb!r}')
    import viewer3d_data as VD
    col_fn = getattr(VD, 'coverage_map_column', None)
    if chk('F7 viewer3d_data.coverage_map_column 이 있다 (뷰어가 읽은 열을 알린다)', callable(col_fn)):
        with tempfile.TemporaryDirectory() as td:
            p_h = os.path.join(td, 'h.csv')
            with open(p_h, 'w', newline='') as fh:
                w = csv.writer(fh); w.writerow(['am_id', 'coverage_hertzian_pct']); w.writerow([1, 30.0])
            p_b = os.path.join(td, 'b.csv')
            with open(p_b, 'w', newline='') as fh:
                w = csv.writer(fh); w.writerow(['am_id', 'coverage_hertzian_pct', 'coverage_physics_pct'])
                w.writerow([1, 30.0, 70.0])
            chk('F8 physics 열 없음 → coverage_hertzian_pct', col_fn(p_h) == 'coverage_hertzian_pct', repr(col_fn(p_h)))
            chk('F9 둘 다 있으면 coverage_physics_pct', col_fn(p_b) == 'coverage_physics_pct', repr(col_fn(p_b)))
            chk('F10 파일 없음 → None', col_fn(os.path.join(td, 'none.csv')) is None)
            chk('F11 build_coverage_map 값은 그대로 (physics 우선 · 없으면 hertz)',
                VD.build_coverage_map(p_b) == {1: 70.0} and VD.build_coverage_map(p_h) == {1: 30.0})
    asrc = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
    chk("F12 app.py 가 aux['coverage_per_am_source'] 를 싣는다",
        re.search(r"aux\[['\"]coverage_per_am_source['\"]\]\s*=", asrc) is not None)
    js = open(os.path.join(HERE, 'static', 'js', 'viewer3d.js'), encoding='utf-8').read()
    chk('F13 3D 뷰어 피복 범례가 coverage_per_am_source 로 Hertz 대체를 표시한다',
        'coverage_per_am_source' in js and 'Hertz 계열 대체' in js)
    sh = open(os.path.join(HERE, 'templates', 'single.html'), encoding='utf-8').read()
    chk('F14 등급 표 라벨 칸이 fallback_note 를 표시한다', 'fallback_note' in sh)


def section_g():
    print('[G] 그룹 그림 체크박스 ↔ 그림 목록')
    import generate_comparison_plots as G
    html = open(os.path.join(HERE, 'templates', 'group.html'), encoding='utf-8').read()
    vals = sorted(set(re.findall(r'class="plot-checkbox"[^>]*>\s*<input type="checkbox" value="([^"]+)"', html)))
    chk('G0 그림 체크박스를 찾았다', len(vals) >= 30, f'n={len(vals)}')
    special = {'four_panel'}
    missing = [v for v in vals if v not in G.PLOT_REGISTRY and v not in special]
    chk('G1 모든 체크박스 값이 그림 목록에 있다 ([SKIP] Unknown 없음)', not missing, f'없음 {missing}')
    for key in ('porosity_union', 'overlap_fraction_pct'):
        e = G.PLOT_REGISTRY.get(key)
        if not chk(f'G2 {key} 그림 등록', e is not None and callable(e.get('func'))):
            continue
        with tempfile.TemporaryDirectory() as td:
            old = getattr(G, 'OUTPUT_DIR', None)
            try:
                if hasattr(G, 'OUTPUT_DIR'):
                    G.OUTPUT_DIR = td
                data = [{key: 12.0}, {}, {key: 10.0}]
                pts = G._metric_points(data, key)
                chk(f'G3 {key}: 값 없는 케이스는 점을 찍지 않는다 (0 으로 그리지 않음)',
                    pts == [(0, 12.0), (2, 10.0)], repr(pts))
            finally:
                if hasattr(G, 'OUTPUT_DIR'):
                    G.OUTPUT_DIR = old


def main():
    for fn in (section_e, section_f, section_g):
        try:
            fn()
        except Exception as e:  # 한 절의 예외가 다른 절을 가리지 않게
            import traceback
            traceback.print_exc()
            _fail.append(f'{fn.__name__} 예외 {type(e).__name__}: {e}')
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        for f in _fail:
            print('  -', f)
        sys.exit(1)


if __name__ == '__main__':
    main()
