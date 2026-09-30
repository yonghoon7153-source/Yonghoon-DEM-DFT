#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""닫힌 파라미터 표시 회귀 — 웹앱 ① (1저자 비준 09-30 밤 · J20-l "코드 → 웹앱 순차 반영").

  python3 webapp/test_closed_param_labels.py      # 종료코드 0 = PASS

웹앱이 **코드의 정의와 같은 이름 · 한정어**로 보여 주는가를 본다 (값 계산은 건드리지 않는다).
가짜 케이스 하나로 `_load_case_tables` (케이스 페이지 · MD 보고서가 같이 쓰는 표) 를 실제로 돌리고
`single.html` 을 렌더한 뒤, 툴팁 조회 (`lookupTip`) 는 node 로 **렌더된 JS 를 그대로** 실행한다.

  [N] 네트워크 표 — 열 머리 = Hertz 계열 (LIGGGHTS c_cpl[22] 기하 교차 원판 · 이름만 Hertz) · Physics 계열 v1
      · 공극률 두 줄 나란히 (ε_sphere 구 부피 합 · ε_union 쌍 렌즈) · 두께 = 판 간격 · φ_SE 한정어 · AM–AM CN std 행
  [B] 머리 배지 — ε_sphere · ε_union 라벨 · 두께의 plate_z_source (판 메시 / ⚠ 최고 입자 중심 추정)
  [T] 툴팁 — 라벨 → 툴팁 역맵 전수 일치 · 코드와 다른 옛 서술 (A^Tabor / Σ4πR² · "Hertz 접촉역학 기반" ·
      z_max − z_min · "문헌 비교용") 제거 · 접촉 요약 · 배위수 탭의 행이 파괴 표 툴팁을 빌려 쓰지 않는다
  [G] 그룹 비교 — 닫힌 열마다 툴팁 · 같은 정의
  [R] MD 보고서 — 같은 라벨

⚠ 실측 근거 (웹앱 ε_union 이 정확 union 의 상한이 **아니다**): `docs/data/lhs_union_20260927/` 194/194 건에서
   웹앱 쌍 렌즈 union < 몬테카를로 정확 union (중앙 −0.64 %p · lhsx −0.75 %p) — 벽 밖으로 나간 구 부피를
   빼지 않기 때문이다.  벽 밖을 빼면 정확 union 과 중앙 0.001 %p.  그래서 라벨이 "상한" 이라 쓰면 거짓이다.
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
SINGLE_HTML = os.path.join(HERE, 'templates', 'single.html')
GROUP_HTML = os.path.join(HERE, 'templates', 'group.html')

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


# ── 가짜 케이스 (DEM 없이) ─────────────────────────────────────────────────────
NET_CSV = (
    '지표,값\n'
    '── 구조 ──,\n'
    'Porosity(%),15.63\n'
    '전극두께(μm),30.28\n'
    '── 계면 ──,\n'
    'AM-SE Total(μm²),1234.5\n'
    'SE-SE Total(μm²),2345.6\n'
    'Coverage AM_P(%),18.2\n'
    'Coverage AM_S(%),19.1\n'
    '── 이온경로: 연결성 ──,\n'
    'SE-SE CN mean,4.75\n'
    'SE-SE CN std,1.9\n'
    '── 이온전도 ──,\n'
    'SE Volume Fraction,0.254\n'
)
CONTACT_CSV = (
    '접촉유형,접촉수,접촉면적_mean(μm²),접촉면적_total(μm²)\n'
    'AM_P-AM_P,12,0.5,6.0\n'
    'AM_P-SE,300,1.2,360.0\n'
    'AM_S-SE,500,1.0,500.0\n'
    'SE-SE,2000,1.1,2200.0\n'
    'AM전체-SE,800,1.075,860.0\n'
    'All,2812,1.09,3066.0\n'
)
COORD_CSV = (
    '입자유형,입자수,배위수_mean,배위수_std,배위수_min,배위수_max\n'
    'AM_P,36,20.1,3.2,10,30\n'
    'AM_S,421,8.1,2.0,2,15\n'
    'SE,32832,5.2,1.9,0,12\n'
)
METRICS = {
    'porosity': 15.63, 'porosity_union': 18.42, 'overlap_fraction_pct': 3.31,
    'thickness_um': 30.28, 'plate_z_source': 'mesh', 'phi_se': 0.254,
    'se_se_cn': 4.75, 'se_se_cn_std': 1.9,
    #  am_am_n_contacts 는 실제 full_metrics.json 에서 **문자열**이다 (numpy int64 → json default=str) — ② 에서 고친다
    'am_am_cn': 3.1, 'am_am_cn_std': 1.42, 'am_am_n_contacts': '412',
    'coverage_AM_P_mean': 18.2, 'coverage_AM_P_mean_physics': 48.3,
    'coverage_AM_S_mean': 19.1, 'coverage_AM_S_mean_physics': 51.8,
}


def make_case(root, name, plate_src):
    rd = os.path.join(root, 'results', name)
    os.makedirs(rd, exist_ok=True)
    for fn, body in (('network_summary.csv', NET_CSV), ('contact_summary.csv', CONTACT_CSV),
                     ('coordination_summary.csv', COORD_CSV)):
        with open(os.path.join(rd, fn), 'w', encoding='utf-8') as f:
            f.write(body)
    m = dict(METRICS, plate_z_source=plate_src)
    with open(os.path.join(rd, 'full_metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(m, f, ensure_ascii=False)
    cd = os.path.join(root, 'uploads', name)
    os.makedirs(cd, exist_ok=True)
    with open(os.path.join(cd, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump({'name': name, 'mode': 'bimodal', 'scale': 1000}, f)
    return rd


# ── JS 추출기 (문자열 · 주석 안의 중괄호를 건너뛴다) ─────────────────────────────
def _balanced(src, i):
    """src[i] == '{' 부터 짝이 맞는 '}' 까지."""
    assert src[i] == '{', src[i:i + 20]
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
        elif src.startswith('/*', j):
            j = src.index('*/', j) + 2
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


def run_node(script):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(script)
        p = f.name
    try:
        r = subprocess.run(['node', p], capture_output=True, text=True, timeout=60)
        if r.returncode:
            print('    node stderr:', (r.stderr or '')[-600:])
            return None
        return json.loads(r.stdout.strip().splitlines()[-1])
    finally:
        os.unlink(p)


def tips_via_node(html, queries):
    """렌더된 single.html 의 METRIC_TIPS · PAPER_TO_ORIG · tabTip · lookupTip 을 그대로 실행."""
    parts = [js_const(html, 'METRIC_TIPS'), js_const(html, 'PAPER_TO_ORIG')]
    if 'function tabTip(' in html:
        parts.append(js_fn(html, 'tabTip'))
    parts.append(js_fn(html, 'lookupTip'))
    script = '\n'.join(parts) + (
        '\nconst Q = ' + json.dumps(queries, ensure_ascii=False) + ';\n'
        'const out = Q.map(q => { const t = lookupTip(q[0], q[1], q[2]); '
        'return t ? {title: t.title, formula: t.formula, desc: t.desc, meaning: t.meaning} : null; });\n'
        'console.log(JSON.stringify({out: out, keys: Object.keys(METRIC_TIPS)}));\n')
    return run_node(script)


def txt(t):
    return ' '.join(str((t or {}).get(k) or '') for k in ('title', 'formula', 'desc', 'meaning'))


def main():
    tmp = tempfile.mkdtemp(prefix='closed_labels_')
    try:
        for k, v in (('WEBAPP_RESULTS_FOLDER', 'results'), ('WEBAPP_UPLOAD_FOLDER', 'uploads'),
                     ('WEBAPP_ARCHIVE_FOLDER', 'archive'), ('WEBAPP_MPM_LAB_FOLDER', 'mpm_lab')):
            os.environ[k] = os.path.join(tmp, v)
        sys.path.insert(0, HERE)
        sys.path.insert(0, os.path.join(ROOT, 'scripts'))
        import app as A
        rd = make_case(tmp, 'lcase', 'mesh')
        rd2 = make_case(tmp, 'lcase_est', 'estimated_center')

        tables, metrics, ip = A._load_case_tables(rd, {'id': 'lcase', 'name': 'lcase'})
        net = tables['network_summary']
        cols, rows = net['columns'], net['data']
        labels = [str(r[0]).strip() for r in rows]

        print('[N] 네트워크 표')
        chk('N1 열 머리 = Hertz 계열 (c_cpl[22] 기하 교차 원판)',
            str(cols[1]).startswith('Hertz 계열') and 'c_cpl[22]' in str(cols[1]), str(cols[1]))
        chk('N2 열 머리 = Physics 계열 v1', str(cols[2]).startswith('Physics 계열'), str(cols[2]))
        i_sp = [i for i, l in enumerate(labels) if 'ε_sphere' in l]
        chk('N3 공극률 행 = ε_sphere (구 부피 합) 하나', len(i_sp) == 1, repr(labels[:6]))
        if i_sp:
            i = i_sp[0]
            nxt = labels[i + 1] if i + 1 < len(labels) else ''
            chk('N4 바로 다음 행 = ε_union 쌍 렌즈 (나란히 · 강등 없음)',
                'ε_union' in nxt and 'pair-lens' in nxt, nxt)
            chk('N4b ε_union 라벨이 "overlap-corrected" · "upper bound" 라 하지 않는다',
                'overlap-corrected' not in nxt and 'upper bound' not in nxt, nxt)
            chk('N4c ε_union 값 = porosity_union (소수 1)',
                i + 1 < len(rows) and str(rows[i + 1][1]) == f"{METRICS['porosity_union']:.1f}")
            chk('N4d ε_sphere 값 = porosity (CSV 그대로)', str(rows[i][1]) == '15.63', str(rows[i][1]))
        th = [l for l in labels if l.startswith('Electrode thickness')]
        chk('N5 두께 = 판 간격 (plate gap)', len(th) == 1 and 'plate gap' in th[0], repr(th))
        ph = [l for l in labels if l.startswith('SE volume fraction')]
        chk('N6 φ_SE 한정어 = 구 부피 합 ÷ 판 간격', len(ph) == 1 and 'sphere volume' in ph[0], repr(ph))
        am_std = [r for r in rows if str(r[0]).strip() == 'AM-AM coordination number σ(z_AM-AM)']
        chk('N7 AM–AM CN std 행 (J20-j 세 열 중 표시 안 되던 것)',
            len(am_std) == 1 and str(am_std[0][1]) == '1.42', repr(am_std))
        sec = [l for l in labels if l.startswith('── 네트워크 솔버')]
        chk('N8 네트워크 솔버 절 머리에 "DEM native vs Tabor" 옛 표기 없음',
            all('Hertzian vs Physics' not in s for s in sec), repr(sec))

        print('[B] 머리 배지 · 렌더')
        from jinja2 import ChainableUndefined
        _old = A.app.jinja_env.undefined
        A.app.jinja_env.undefined = ChainableUndefined
        try:
            with A.app.app_context(), A.app.test_request_context('/'):
                html = A.render_template('single.html', case={'id': 'lcase', 'name': 'lcase', 'mode': 'bimodal', 'scale': 1000},
                                         figures=[], report='', tables=tables, metrics=metrics,
                                         input_params=ip, archive_path=None, mpm_metrics={},
                                         trust_card=None, lv=A._page_lv('single'))
                t2, m2, ip2 = A._load_case_tables(rd2, {'id': 'lcase_est', 'name': 'lcase_est'})
                html2 = A.render_template('single.html', case={'id': 'lcase_est', 'name': 'lcase_est', 'mode': 'bimodal', 'scale': 1000},
                                          figures=[], report='', tables=t2, metrics=m2,
                                          input_params=ip2, archive_path=None, mpm_metrics={},
                                          trust_card=None, lv=A._page_lv('single'))
        finally:
            A.app.jinja_env.undefined = _old
        for old in ('Hertzian (DEM native)', 'Physics (Tabor + volume)', 'overlap-corrected'):
            chk(f'B0 옛 표기 없음: {old!r}', old not in html)
        badge_th = re.search(r'<span class="badge"[^>]*title="([^"]*)"[^>]*>\s*두께[^<]*', html)
        chk('B1 두께 배지 = 판 간격 · 출처 mesh 표시',
            bool(badge_th) and '판 간격' in badge_th.group(0) and 'mesh' in badge_th.group(1),
            badge_th.group(0)[:200] if badge_th else 'no badge')
        badge_th2 = re.search(r'<span class="badge[^"]*"[^>]*title="([^"]*)"[^>]*>\s*두께[^<]*', html2)
        chk('B2 mesh 없는 케이스 = ⚠ 최고 입자 중심 추정 표시',
            bool(badge_th2) and '⚠' in badge_th2.group(0) and '입자 중심' in badge_th2.group(1),
            badge_th2.group(0)[:200] if badge_th2 else 'no badge')
        b_un = re.search(r'<span class="badge"[^>]*title="([^"]*)"[^>]*>\s*ε_union[^<]*', html)
        chk('B3 ε_union 배지 = 쌍 렌즈 · 벽 밖 미제거 (옛 "문헌 비교용" 없음)',
            bool(b_un) and '벽 밖' in b_un.group(1) and '문헌 비교용' not in b_un.group(1)
            and '쌍 렌즈' in b_un.group(0), b_un.group(0)[:200] if b_un else 'no badge')
        b_sp = re.search(r'<span class="badge"[^>]*title="([^"]*)"[^>]*>\s*(Porosity[^<]*)', html)
        chk('B4 공극률 배지 = ε_sphere 표기', bool(b_sp) and 'ε_sphere' in b_sp.group(2),
            b_sp.group(2) if b_sp else 'no badge')
        chk('B5 접촉 요약 · 배위수 행에 탭 문맥 (data-tab)',
            'data-metric="AM_P-AM_P" data-tab="contact_summary"' in html
            and 'data-metric="SE" data-tab="coordination_summary"' in html)

        print('[T] 툴팁 (렌더된 JS 를 node 로)')
        if not shutil.which('node'):
            chk('node 필요 (툴팁 조회를 실제로 돌린다)', False, 'node 미설치')
        else:
            paper = dict(A._PAPER_LABEL_MAP)
            q = [[l, None, 'network_summary'] for l in labels if l and not l.startswith('──')]
            q += [[p, None, 'network_summary'] for p in paper.values()]
            q += [[r, None, 'network_summary'] for r in paper]
            q += [['AM_P-AM_P', None, 'contact_summary'], ['All', None, 'contact_summary'],
                  ['SE', None, 'coordination_summary'], ['AM_P-AM_P', None, 'fracture_summary']]
            res = tips_via_node(html, q)
            chk('T0 node 실행', res is not None)
            if res is not None:
                got = {tuple(k): v for k, v in zip([tuple(x) for x in q], res['out'])}
                keys = set(res['keys'])

                def tip(lbl, tab='network_summary'):
                    return got.get((lbl, None, tab))
                # T1 — 역맵 전수: 원 라벨에 툴팁이 있으면 바뀐 라벨도 **같은** 툴팁을 찾는다
                drift = [(r, p) for r, p in paper.items()
                         if r.strip() in keys and (tip(p) or {}).get('title') != (tip(r) or {}).get('title')]
                chk('T1 라벨 → 툴팁 역맵 전수 일치 (_PAPER_LABEL_MAP ↔ PAPER_TO_ORIG)', not drift, repr(drift[:4]))
                sp = next((l for l in labels if 'ε_sphere' in l), '')
                un = next((l for l in labels if 'ε_union' in l), '')
                t_sp, t_un = tip(sp), tip(un)
                chk('T2 ε_sphere 툴팁 = 구 부피 합 · 겹친 부피 이중계상 · 인계는 정확 union',
                    '구 부피 합' in txt(t_sp) and '이중' in txt(t_sp)
                    and 'porosity_union_exact_pct' in txt(t_sp), txt(t_sp)[:160])
                chk('T3 ε_union 툴팁 있음 · 벽 밖 미제거 · 정확 union 보다 낮게 나온다 (실측)',
                    t_un is not None and '벽 밖' in txt(t_un) and '정확 union' in txt(t_un)
                    and '상한' not in (t_un or {}).get('title', ''), txt(t_un)[:160])
                ov = next((l for l in labels if l.startswith('Overlap fraction')), '')
                chk('T3b 겹침 비율 행에도 툴팁', bool(ov) and tip(ov) is not None, ov)
                t_th = tip(next((l for l in labels if l.startswith('Electrode thickness')), ''))
                chk('T4 두께 툴팁 = 판 간격 · mesh_info.json · 대체 규칙 (옛 z_max − z_min 없음)',
                    '판 간격' in txt(t_th) and 'mesh_info.json' in txt(t_th)
                    and 'z_max − z_min' not in txt(t_th), txt(t_th)[:160])
                t_ams = tip('AM-SE Total(μm²)')
                chk('T5 AM–SE 총 면적 = c_cpl[22] 기하 교차 원판 (옛 "Hertz 접촉역학 기반" 없음)',
                    'c_cpl[22]' in txt(t_ams) and 'Hertz 접촉역학' not in txt(t_ams), txt(t_ams)[:160])
                chk('T6 SE–SE 총 면적 = c_cpl[22]', 'c_cpl[22]' in txt(tip('SE-SE Total(μm²)')))
                for lb in ('Coverage AM_P(%)', 'Coverage AM_S(%)', 'Coverage AM(%)'):
                    t = tip(lb)
                    chk(f'T7 {lb} 식 = 입자별 min(100, …/(4πr² − ΣA(AM–AM))) · 두 열 = 두 계열',
                        'min(100' in txt(t) and '4πr² − ΣA(AM–AM)' in txt(t)
                        and 'A_AM-SE^Tabor' not in txt(t) and 'Hertz 계열' in txt(t)
                        and 'Physics 계열' in txt(t), txt(t)[:160])
                for lb in ('SE-SE CN mean', 'SE-SE CN std'):
                    chk(f'T8 {lb} = 입자–입자 접촉만 (벽 · 플래튼 안 셈)', '벽' in txt(tip(lb)), txt(tip(lb))[:120])
                chk('T8b SE–SE CN std = 모집단 σ', '모집단' in txt(tip('SE-SE CN std')))
                chk('T9 AM–AM CN std 툴팁 (모집단 σ)', '모집단' in txt(tip('AM-AM CN std')))
                chk('T10 φ_SE 툴팁 = 구 부피 합 ÷ 판 간격', '구 부피 합' in txt(tip('SE Volume Fraction'))
                    and '판 간격' in txt(tip('SE Volume Fraction')))
                t_cs = got.get(('AM_P-AM_P', None, 'contact_summary'))
                chk('T11 접촉 요약 AM_P-AM_P 행 ≠ 파괴 severe % 툴팁 · 덤프 행 수 · 없는 쌍 = 0',
                    t_cs is not None and 'severe' not in (t_cs or {}).get('title', '')
                    and '덤프' in txt(t_cs) and '0' in txt(t_cs), txt(t_cs)[:160])
                chk('T11b 접촉 요약 All 행 툴팁', got.get(('All', None, 'contact_summary')) is not None)
                t_co = got.get(('SE', None, 'coordination_summary'))
                chk('T12 배위수 탭 = 상 구분 없는 전체 배위수 (SE–SE CN 과 다른 양)',
                    t_co is not None and '전체' in txt(t_co) and 'SE–SE CN' in txt(t_co), txt(t_co)[:160])
                t_fr = got.get(('AM_P-AM_P', None, 'fracture_summary'))
                chk('T13 파괴 탭 AM_P-AM_P 는 종전 그대로 (severe %)', 'severe' in (t_fr or {}).get('title', ''))
                chk('T14 σ_ionic 툴팁의 면적 = c_cpl[22] (옛 "LIGGGHTS-reported Hertzian area" 없음)',
                    'LIGGGHTS-reported Hertzian area' not in html)

        print('[G] 그룹 비교')
        gsrc = open(GROUP_HTML, encoding='utf-8').read()
        if shutil.which('node'):
            cols_needed = ['φ_AM', 'φ_SE', 'Porosity', 'Porosity (union)', 'Overlap fraction', '두께',
                           'SE-SE CN', 'SE-SE CN std', 'SE-SE Total', 'Coverage P', 'Coverage S',
                           'AM-AM CN', 'AM-AM Mean Area', 'AM-AM N contacts']
            res = run_node(js_const(gsrc, 'COL_TIPS') + '\nconsole.log(JSON.stringify(COL_TIPS));\n')
            chk('G0 COL_TIPS 실행', res is not None)
            if res is not None:
                miss = [c for c in cols_needed if c not in res]
                chk('G1 닫힌 열마다 툴팁', not miss, repr(miss))
                cp = res.get('Coverage P', '') + res.get('Coverage S', '')
                chk('G2 Coverage P/S = Hertz 계열 · 입자별 min(100, …/(4πr² − ΣA(AM–AM)))',
                    'Hertz 계열' in cp and '4πr² − ΣA(AM–AM)' in cp and 'min(100' in cp, cp[:160])
                chk('G3 Porosity = 구 부피 합 · Porosity (union) = 쌍 렌즈 · 벽 밖',
                    '구 부피 합' in res.get('Porosity', '') and '벽 밖' in res.get('Porosity (union)', ''))
                chk('G4 두께 = 판 간격 (옛 z_max − z_min 없음)',
                    '판 간격' in res.get('두께', '') and 'z_max − z_min' not in res.get('두께', ''))
                chk('G5 AM-SE Total · SE-SE Total = c_cpl[22]',
                    'c_cpl[22]' in res.get('AM-SE Total', '') and 'c_cpl[22]' in res.get('SE-SE Total', ''))
                chk('G6 σ_brug/σ_grain 의 σ_grain 라벨 = 펠릿 (옛 "grain interior" 없음 · SELF-51)',
                    'grain interior' not in res.get('σ_brug/σ_grain', ''))
        chk('G7 유도 상자 cov_Hertz = c_cpl[22] (옛 "ELASTIC contact area" 없음)',
            'ELASTIC contact area' not in gsrc and 'cov_Hertz^½</b>: Holm 1967 constriction at c_cpl[22]' in gsrc)
        chk('G8 그룹 그림 체크박스 union 설명 (옛 "overlap-corrected; literature comparison" 없음)',
            'overlap-corrected; literature comparison' not in gsrc)

        print('[R] MD 보고서')
        c = A.app.test_client()
        r = c.get('/results/lcase/report')
        md = r.get_data(as_text=True)
        chk('R1 보고서 200', r.status_code == 200, str(r.status_code))
        chk('R2 보고서 = ε_sphere · ε_union 쌍 렌즈 라벨 (옛 overlap-corrected 없음)',
            'ε_sphere' in md and '쌍 렌즈' in md and 'overlap-corrected' not in md)
        chk('R3 보고서 두께 = 판 간격 · 출처', '판 간격' in md and 'mesh' in md)
        chk('R4 보고서 네트워크 표 열 머리 = Hertz 계열 · Physics 계열', 'Hertz 계열' in md and 'Physics 계열' in md)
        #  AI 분석 프롬프트 · 그룹 MD 보고서 (API 키 없이는 못 돌리므로 소스로) — 같은 한정어
        asrc = open(os.path.join(HERE, 'app.py'), encoding='utf-8').read()
        chk('R5 AI 분석 · 그룹 보고서 표 = ε_sphere · ε_union pair-lens · 판 간격 (옛 "Porosity union(%)" 없음)',
            "('Porosity union(%)'" not in asrc and "('Thickness(μm)'" not in asrc
            and asrc.count("('Porosity ε_union pair-lens(%)', 'porosity_union')") == 2)
        pu = A._GRADE_PLAIN.get('porosity_union', '')
        chk('R6 등급 설명 (쉽게 말하면) union = 쌍 렌즈 · 정확 union 보다 낮음 (옛 "문헌 비교용" 없음)',
            '문헌 비교용' not in pu and '쌍 렌즈' in pu and '정확한 union' in pu, pu[:120])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
