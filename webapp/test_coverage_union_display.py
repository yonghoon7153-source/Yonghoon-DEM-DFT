#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Physics 피복 ⑥ 합집합 cap — 웹앱 같은 묶음 (J20-l · C2-⑥ 1저자 비준 10-06 · LHS-25).

  python3 webapp/test_coverage_union_display.py      # 종료코드 0 = PASS

생산자 (`coverage_physics_vs_hertzian.union_coverage_bed`) 가 새 키 `coverage_<상>_mean_physics_union` 을 쓴다.  웹앱은 같은 이름 · 한정어로:
  [N] 케이스 망 요약 — Coverage 행의 Physics 열 = **합집합** 값 (행 이름에 '합집합 · 겹침 한 번 · AM–AM 가림 제외 · 세대 2 면적') ·
      바로 아래 legacy 합-클립 줄 (옛 Physics v1 값 · 100 % 포화 표지) · 옛 케이스 (새 키 없음) = '—' (0 · legacy · Hertz 복사 아님) ·
      빈칸 침대 = '—' + 사유 줄 · mono (Coverage AM) 도 같다
  [T] 툴팁 (렌더된 single.html 의 lookupTip 을 node 로) — 정의 · N · 표면 소비자 · legacy 줄 포화 · 역맵 일치
  [G] 그룹 비교 — 합집합 열 둘 · 열 툴팁 · mono 매핑 · 빈칸 = '— (빈칸)' (None 이 'None' 으로 보이지 않게 · 최고값 후보 아님)
  [R] MD 보고서 · 그룹 보고서 · AI 프롬프트 표 — 같은 키 · 같은 한정어
  [F] 그룹 그림 — 체크박스 · 그림 목록 · 값 없는 케이스는 점을 안 찍는다
  [P] 등급 쉬운 설명 — 등급 축은 아직 옛 합-클립 (LHS-25 ② 미결) 이라고 적는다
★ 시험 먼저 — 옛 웹앱 (a0a24c538) 은 Coverage 행 Physics 열에 legacy 합-클립을 그대로 싣고 합집합 키를 모른다.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

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


NET_CSV = ('지표,값\n── 구조 ──,\nPorosity(%),15.63\n── 계면 ──,\nAM-SE Total(μm²),1234.5\nSE-SE Total(μm²),2345.6\n'
           'Coverage AM_P(%),18.4\nCoverage AM_S(%),18.3\n── 이온경로: 연결성 ──,\nSE-SE CN mean,4.75\n')
NET_CSV_MONO = ('지표,값\n── 구조 ──,\nPorosity(%),15.63\n── 계면 ──,\nAM-SE Total(μm²),1234.5\nSE-SE Total(μm²),2345.6\n'
                'Coverage AM(%),7.9\n── 이온경로: 연결성 ──,\nSE-SE CN mean,4.75\n')
LEG = {'coverage_AM_P_mean': 18.4, 'coverage_AM_S_mean': 18.3, 'coverage_AM_P_mean_physics': 48.286,
       'coverage_AM_S_mean_physics': 51.798, 'coverage_AM_mean_physics': 51.522}
UNION = {'coverage_AM_P_mean_physics_union': 39.718, 'coverage_AM_P_std_physics_union': 14.2,
         'coverage_AM_S_mean_physics_union': 43.518, 'coverage_AM_S_std_physics_union': 20.1,
         'coverage_AM_mean_physics_union': 43.218, 'coverage_status_physics_union': 'ok',
         'coverage_rule_physics_union': 'union_caps_g2_surface', 'coverage_n_fib_physics_union': 6000,
         'coverage_diag_physics_union': {'n_am': 457}}
BLANK = {'coverage_AM_P_mean_physics_union': None, 'coverage_AM_P_std_physics_union': None,
         'coverage_AM_S_mean_physics_union': None, 'coverage_AM_S_std_physics_union': None,
         'coverage_AM_mean_physics_union': None,
         'coverage_status_physics_union': 'blank: 2 접촉을 거부했다 — 첫 사례 31–29241: ValueError: ligg_area < 0',
         'coverage_rule_physics_union': 'union_caps_g2_surface', 'coverage_n_fib_physics_union': 6000,
         'coverage_diag_physics_union': {'n_am': 104}}


def _guard(label, fn):
    try:
        fn()
    except Exception as e:                                       # noqa: BLE001 — 옛 코드 = 없는 이름 · 키도 FAIL 로 센다
        import traceback
        traceback.print_exc()
        chk(f'{label} — 예외 {type(e).__name__}: {e}', False)


def make_case(root, name, metrics, net=NET_CSV):
    rd = os.path.join(root, 'results', name)
    os.makedirs(rd, exist_ok=True)
    with open(os.path.join(rd, 'network_summary.csv'), 'w', encoding='utf-8') as f:
        f.write(net)
    m = dict({'porosity': 15.63, 'thickness_um': 30.28, 'plate_z_source': 'mesh', 'se_se_cn': 4.75}, **metrics)
    with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False)
    cd = os.path.join(root, 'uploads', name)
    os.makedirs(cd, exist_ok=True)
    with open(os.path.join(cd, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump({'name': name, 'mode': 'bimodal', 'scale': 1000}, f)
    return rd


def rows_of(A, rd, name):
    tables, metrics, ip = A._load_case_tables(rd, {'id': name, 'name': name})
    return tables, metrics, ip, tables['network_summary']['data']


def find(rows, needle):
    return [i for i, r in enumerate(rows) if isinstance(r[0], str) and needle in r[0]]


def _balanced(src, i):
    depth, j, n = 0, i, len(src)
    while j < n:
        ch = src[j]
        if ch in '\'"`':
            q = ch
            j += 1
            while j < n and src[j] != q:
                j += 2 if src[j] == '\\' else 1
        elif src.startswith('//', j):
            j = src.index('\n', j)
            continue
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return src[i:j + 1]
        j += 1
    raise AssertionError('중괄호 짝 없음')


def js_const(src, name):
    i = src.index(f'const {name} = {{')
    return f'const {name} = ' + _balanced(src, src.index('{', i)) + ';'


def js_fn(src, name):
    i = src.index(f'function {name}(')
    return src[i:src.index('{', i)] + _balanced(src, src.index('{', i))


def tips_via_node(html, queries):
    parts = [js_const(html, 'METRIC_TIPS'), js_const(html, 'PAPER_TO_ORIG')]
    if 'function tabTip(' in html:
        parts.append(js_fn(html, 'tabTip'))
    parts.append(js_fn(html, 'lookupTip'))
    script = '\n'.join(parts) + ('\nconst Q = ' + json.dumps(queries, ensure_ascii=False) + ';\n'
                                 'console.log(JSON.stringify(Q.map(q => { const t = lookupTip(q, null, "network_summary"); '
                                 'return t ? [t.title, t.formula, t.desc, t.meaning].join(" ") : null; })));\n')
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script)
        p = f.name
    try:
        r = subprocess.run(['node', p], capture_output=True, text=True, timeout=60)
        if r.returncode:
            print('    node stderr:', (r.stderr or '')[-400:])
            return None
        return json.loads(r.stdout.strip().splitlines()[-1])
    finally:
        os.unlink(p)


def main():
    tmp = tempfile.mkdtemp(prefix='union_web_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
        import app as A

        print('[N] 케이스 망 요약 — Coverage 행')
        rd = make_case(tmp, 'ucase', dict(LEG, **UNION))
        tables, metrics, ip, rows = rows_of(A, rd, 'ucase')
        iP, iS = find(rows, 'cov_AM_P'), find(rows, 'cov_AM_S')
        ok_rows = len(iP) == 1 and len(iS) == 1
        chk('N0 Coverage AM_P · AM_S 행이 하나씩 (paper 라벨)', ok_rows, repr([r[0] for r in rows]))
        if ok_rows:
            rP, rS = rows[iP[0]], rows[iS[0]]
            chk('N1 ★ Physics 열 = 합집합 값 (39.7 · 43.5) · legacy 합-클립 (48.3 · 51.8) 이 아니다',
                str(rP[2]) == '39.7' and str(rS[2]) == '43.5', f'{rP} · {rS}')
            chk('N1b 행 이름 = 합집합 · 겹침 한 번 · AM–AM 가림 제외 · 세대 2 면적 (Physics 열의 정의)',
                all(x in rP[0] for x in ('합집합', '겹침 한 번', 'AM–AM 가림 제외', '세대 2 면적')), rP[0])
            chk('N1c Hertz 열 그대로 (18.4) · Δ = Hertz ↔ 합집합', str(rP[1]) == '18.4' and rP[3] == A._pct_delta(18.4, 39.718),
                f'{rP[1]} · {rP[3]}')
            lp, ls = rows[iP[0] + 1], rows[iS[0] + 1]
            chk('N2 ★ 바로 아래 legacy 합-클립 줄 — Physics 열 = 옛 값 (48.3 · 51.8) · Hertz 열 — · 이름에 legacy · 합-클립 · 포화',
                str(lp[2]) == '48.3' and str(ls[2]) == '51.8' and lp[1] == '—'
                and all(x in lp[0] for x in ('legacy', '합-클립', '포화')), f'{lp} · {ls}')
        rd2 = make_case(tmp, 'oldcase', dict(LEG))
        _t2, _m2, _ip2, rows2 = rows_of(A, rd2, 'oldcase')
        iP2 = find(rows2, 'cov_AM_P')
        if chk('N3 옛 케이스에도 Coverage AM_P 행이 있다', len(iP2) == 1):
            r2, l2 = rows2[iP2[0]], rows2[iP2[0] + 1]
            chk('N3b ★ 옛 케이스 (합집합 키 없음) → Physics 열 "—" (0 · legacy 48.3 · Hertz 복사 18.4 아님) · legacy 줄 = 48.3',
                r2[2] == '—' and str(l2[2]) == '48.3' and 'legacy' in l2[0], f'{r2} · {l2}')
        rd3 = make_case(tmp, 'blankcase', dict(LEG, **BLANK))
        _t3, _m3, _ip3, rows3 = rows_of(A, rd3, 'blankcase')
        iP3 = find(rows3, 'cov_AM_P')
        st = [r for r in rows3 if isinstance(r[0], str) and '합집합 상태' in r[0]]
        chk('N4 ★ 빈칸 침대 → Physics 열 "—" + 사유 줄 (ligg_area < 0 · 첫 사례) · 0 이 아니다',
            len(iP3) == 1 and rows3[iP3[0]][2] == '—' and len(st) == 1 and 'ligg_area < 0' in str(st[0][2]),
            repr(st))
        st_ok = [r for r in rows if isinstance(r[0], str) and '합집합 상태' in r[0]]
        chk('N4b 정상 침대에는 상태 줄이 없다', not st_ok)
        rd4 = make_case(tmp, 'monocase', {'coverage_AM_mean': 7.9, 'coverage_AM_mean_physics': 18.324,
                                          'coverage_AM_mean_physics_union': 15.984, 'coverage_status_physics_union': 'ok'},
                        net=NET_CSV_MONO)
        _t4, _m4, _ip4, rows4 = rows_of(A, rd4, 'monocase')
        i4 = find(rows4, 'cov_AM (')
        chk('N5 mono (Coverage AM) — Physics 열 = 합집합 16.0 · legacy 줄 18.3',
            len(i4) == 1 and str(rows4[i4[0]][2]) == '16.0' and str(rows4[i4[0] + 1][2]) == '18.3',
            repr([rows4[i] for i in i4] + ([rows4[i4[0] + 1]] if i4 else [])))

        print('[T] 툴팁 (렌더된 JS 를 node 로)')
        from jinja2 import ChainableUndefined
        _old = A.app.jinja_env.undefined
        A.app.jinja_env.undefined = ChainableUndefined
        try:
            with A.app.app_context(), A.app.test_request_context('/'):
                html = A.render_template('single.html', case={'id': 'ucase', 'name': 'ucase', 'mode': 'bimodal', 'scale': 1000},
                                         figures=[], report='', tables=tables, metrics=metrics, input_params=ip,
                                         archive_path=None, mpm_metrics={}, trust_card=None, lv=A._page_lv('single'))
        finally:
            A.app.jinja_env.undefined = _old
        if not shutil.which('node'):
            chk('node 필요 (툴팁 조회를 실제로 돈다)', False, 'node 미설치')
        else:
            _st3 = [r[0] for r in rows3 if '합집합 상태' in str(r[0])]
            q = [rows[iP[0]][0], rows[iP[0] + 1][0], _st3[0]] if (ok_rows and _st3) else []
            res = tips_via_node(html, q) if q else None
            if chk('T0 node 실행', res is not None):
                t_main, t_leg, t_st = res
                chk('T1 ★ Coverage 행 툴팁 = 합집합 cap 정의 (Fibonacci N 6000 · 표면 소비자 film_area_g2 · AM–AM 가림 · 겹침 한 번) + '
                    'Hertz 열 식 그대로',
                    t_main is not None and all(x in t_main for x in ('합집합', '6000', "consumer='surface'", 'AM–AM', '겹침 한 번',
                                                                    'min(100', '4πr² − ΣA(AM–AM)')), (t_main or '')[:200])
                chk('T2 legacy 줄 툴팁 = 접촉 면적 합 · 100 % 포화 · LHS-25 · 등급 축이 아직 이 값', t_leg is not None
                    and all(x in t_leg for x in ('포화', 'LHS-25', '등급')), (t_leg or '')[:200])
                chk('T3 상태 줄 툴팁 (빈칸 사유를 읽는 법)', t_st is not None and '빈칸' in t_st, (t_st or '')[:120])
        paper = A._PAPER_LABEL_MAP
        pto = js_const(html, 'PAPER_TO_ORIG')
        chk('T4 _PAPER_LABEL_MAP 의 Coverage 세 라벨이 PAPER_TO_ORIG 에 같은 철자로 있다 (역맵)',
            all(f"'{paper[k]}'" in pto for k in ('Coverage AM_P(%)', 'Coverage AM_S(%)', 'Coverage AM(%)')))

        _guard('[G]', lambda: section_g(A, gh_path=os.path.join(HERE, 'templates', 'group.html')))
        _guard('[R]', lambda: section_r(A))
        _guard('[F]', lambda: section_f(os.path.join(HERE, 'templates', 'group.html')))
        _guard('[P]', lambda: section_p(A))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f'\n{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


def section_g(A, gh_path):
        print('[G] 그룹 비교')
        keys = {k[2]: k[0] for k in A.GROUP_DISPLAY_KEYS}
        lp_, ls_ = keys.get('coverage_AM_P_mean_physics_union'), keys.get('coverage_AM_S_mean_physics_union')
        chk('G1 그룹 표 열 = 합집합 P · S (높을수록 좋음 — 낮을수록 집합 밖)', lp_ is not None and ls_ is not None
            and '합집합' in lp_ and lp_ not in A.GROUP_LOWER_BETTER, f'{lp_} · {ls_}')
        gh = open(gh_path, encoding='utf-8').read()
        chk('G2 그룹 열 툴팁 (COL_TIPS) — 합집합 · legacy 와 다른 양', bool(lp_) and f"'{lp_}'" in gh and f"'{ls_}'" in gh
            and '합집합' in gh)
        cells = getattr(A, '_group_union_coverage_cells', None)
        if chk('G3 그룹 칸 도우미 _group_union_coverage_cells 가 있다 · group() 이 부른다', callable(cells)
               and '_group_union_coverage_cells(metrics)' in open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()):
            mono = cells({'ps_ratio': '10:0', 'coverage_AM_mean_physics_union': 15.984, 'coverage_status_physics_union': 'ok'})
            mono_s = cells({'ps_ratio': '0:10', 'coverage_AM_mean_physics_union': 12.0, 'coverage_status_physics_union': 'ok'})
            blank = cells(dict(BLANK))
            old = cells(dict(LEG))
            chk('G4 mono → P (10:0) · S (0:10) 열로 · 빈칸 → "— (빈칸)" (None 이 "None" 으로 보이지 않게) · 옛 케이스 = 키 없음 ("-")',
                mono.get('coverage_AM_P_mean_physics_union') == 15.984 and 'coverage_AM_S_mean_physics_union' not in mono
                and mono_s.get('coverage_AM_S_mean_physics_union') == 12.0
                and str(blank.get('coverage_AM_P_mean_physics_union', '')).startswith('—')
                and 'coverage_AM_P_mean_physics_union' not in old,
                repr((mono, blank.get('coverage_AM_P_mean_physics_union'))))
            best = A._group_best_marks([{lp_: '— (빈칸)'}, {lp_: '40.1'}, {lp_: '30.0'}], [(lp_, '(%)', 'x')])
            chk('G5 "— (빈칸)" 칸은 최고값 후보가 아니다 (40.1 강조)', (lp_, 1) in best and (lp_, 0) not in best, repr(best))


def section_r(A):
        print('[R] MD 보고서 · 그룹 보고서 · AI 프롬프트')
        c = A.app.test_client()
        r = c.get('/results/ucase/report')
        md = r.get_data(as_text=True)
        chk('R1 케이스 MD 보고서 = 같은 Coverage 행 (합집합 라벨 · 39.7) + legacy 줄', r.status_code == 200 and '합집합' in md
            and '39.7' in md and '합-클립' in md, str(r.status_code))
        asrc = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
        chk('R2 그룹 보고서 · AI 프롬프트 표에 합집합 열 (같은 키 · 같은 한정어) 둘씩',
            asrc.count("'coverage_AM_P_mean_physics_union')") >= 2 and asrc.count("'coverage_AM_S_mean_physics_union')") >= 2)


def section_f(gh_path):
        print('[F] 그룹 그림')
        gh = open(gh_path, encoding='utf-8').read()
        import generate_comparison_plots as G
        chk('F1 그림 목록 coverage_AM_mean_physics_union · 체크박스', 'coverage_AM_mean_physics_union' in G.PLOT_REGISTRY
            and 'value="coverage_AM_mean_physics_union"' in gh)
        if 'coverage_AM_mean_physics_union' in G.PLOT_REGISTRY:
            pts = G._metric_points([{'coverage_AM_mean_physics_union': 43.2}, {}, {'coverage_AM_mean_physics_union': None}],
                                   'coverage_AM_mean_physics_union')
            chk('F2 값 없는 · None 케이스는 점을 안 찍는다 (0 으로 채우지 않는다)', pts == [(0, 43.2)], repr(pts))
            d = G.PLOT_REGISTRY['coverage_AM_mean_physics_union'].get('description', '')
            chk('F3 그림 설명 = 합집합 · 세대 2 · legacy 와 다른 양', '합집합' in d and '세대 2' in d, d[:120])


def section_p(A):
        js = open(os.path.join(HERE, 'static', 'js', 'viewer3d.js'), encoding='utf-8').read()
        chk('V1 3D 뷰어 피복 범례 (입자별 legacy 값) = 합-클립이라 적고 케이스 표 Physics 열 (합집합) 과 다른 값임을 알린다',
            'Physics v1 합-클립' in js and '합집합 cap' in js)
        print('[P] 등급 쉬운 설명')
        for key in ('coverage_AM_P_mean_physics', 'coverage_AM_S_mean_physics'):
            t = A._GRADE_PLAIN.get(key, '')
            chk(f'P1 {key} — 등급 축은 아직 옛 합-클립 · 케이스 표 Physics 열은 합집합 (LHS-25)',
                '합집합' in t and 'LHS-25' in t and '100 %' in t and '포화' in t, t[:160])


if __name__ == '__main__':
    sys.exit(main())
