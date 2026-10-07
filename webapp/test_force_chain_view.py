#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 3D 뷰어 — Force Chain (메인 겹쳐 그리기 + 그림 창 "Force Chain View") (2026-10-07).

1저자 보고 그림 — 옛 판은 force_chains.json 의 가장 센 5000 개를 노랑 → 빨강으로 칠하고 굵기 · 불투명도를 (fn − 최소)/(최대 − 최소) 로
정했다 → 극단 접촉 하나가 축을 다 차지해 나머지가 전부 옅은 노랑 (PNG = 거의 다 옅은 노랑 · 빨간 토막 하나).

  python3 webapp/test_force_chain_view.py      # 종료코드 0 = PASS

[U] 조작판 배선 — DEM 조작판 "Force Chain" 아래 범례 · 조작 칸 (fc-panel) · "Force Chain View" 단추 (data-action forceChainView · All Paths View 옆) ·
    wireControls 가 체크박스를 forceChainToggle 로 · 단추를 showForceChainView 로 · MPM 조작판엔 없음.
[F] 순수 함수 (viewer3d.js 를 잘라 node 로) — 접촉 쌍 묶음 (AM–AM · AM–SE · SE–SE · 기타) · 가장 센 N 개 고르기 (안정 · 쓸 수 없는 행 셈) ·
    백분위 (numpy linear 와 같은 값) · 굵기 = 5–95 백분위로 자른 상대 힘 (극단 하나가 나머지를 지우지 않는다 — 옛 최소–최대와 대조) ·
    묶음별 수 · 힘 합 몫 (합 100 · 표시 소수 한 자리도 합 100.0) · 주기 경계를 넘는 접촉 = 면에서 잘라 반대 면 (상자를 가로지르는 관 없음 · 길이 = 최소상 거리) ·
    색 (접촉 쌍 = 검증한 3 색 · 힘 모드 = 옛 노랑 → 빨강 · 밝기 단조) · 범례 문구 (고르기 규칙 · 수 · 몫 · ⚠ fn 절대값 · 단위 없음) · PNG 이름.
[R] 메인 겹쳐 그리기 (THREE 껍데기) — 체크박스 → 자료 한 번만 불러 그림 · 묶음마다 InstancedMesh (색 = 묶음 색 · 굵기 = 상대 힘 · 불투명도 한 값) ·
    묶음 끄기 = 다시 짓지 않고 숨김 · 색 모드 · 수 바꾸기 = 다시 짓기 · 끄기 · 다시 켜기.
[M] 그림 창 (Force Chain View) — 맥락 SE · AM (불투명도 막대) · 상자 · 바닥 격자 · 관 전부 상자 안 · PNG (투명 · 4× · 축 글자 숨김 · 잘림 없게 맞춤 ·
    찍은 뒤 시점 그대로) · 범례 넣기 (합성) · 범례 PNG 따로 · 창 상태는 창 안에서만 (메인 옵션 그대로).
[C] 범례 PNG · 범례 넣은 합성 (canvas 껍데기) — 묶음 이름 · 수 · 몫 글자 · 견본 색 · fn 값 · µN 없음.
[X] 변이 — 최소–최대 굵기 · 힘 색 기본 · 접기 생략 · 몫 정규화 빠짐 · 범례에 fn 값 · PNG 맞춤 끔 → 해당 시험이 FAIL 한다 (판별력).
⚠ force_chains.json 의 fn 표기는 같은 리포 힘 분포와 scale 배 다르다 (analyze_contacts.py L956 = fn × 1e6/scale² ↔ dem_analysis_core.py L1102 = F/scale [N]) —
  이 보기는 fn 을 상대 크기로만 쓴다 (화면 · PNG 어디에도 절대값 · 단위를 적지 않는다).  시험이 그것을 강제한다.
⚠ node 가 없으면 건너뛰지 않고 FAIL 한다 (규칙 K).
"""
import json
import math
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(ROOT, 'scripts', 'check_all.sh')

sys.path.insert(0, HERE)
from test_closed_param_labels import js_fn, run_node   # noqa: E402
import test_tau_paths_view as TPV                        # noqa: E402  (같은 THREE · DOM 껍데기 · 파이썬 투영)

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


# ══════════════════════════════════════════════════════════════════════════════
#  합성 force_chains.json — 상자 x · y [0, 20) µm (주기) · z [0, 10] · p1 · p2 = three 좌표 (x, z, y) · fn = 상대 크기
# ══════════════════════════════════════════════════════════════════════════════
BOX = {'x_min': 0, 'x_max': 20, 'y_min': 0, 'y_max': 20, 'z_min': 0, 'z_max': 10}
TYPES = (['AM_P-AM_P'] * 9 + ['AM_P-AM_S'] * 5 + ['AM_S-AM_S'] * 3 + ['AM_P-SE'] * 12 + ['AM_S-SE'] * 10 + ['SE-SE'] * 15
         + ['?-SE'] * 2 + ['AM_P-T3'])
GROUP_OF = {'AM_P-AM_P': 'amam', 'AM_P-AM_S': 'amam', 'AM_S-AM_S': 'amam', 'AM_P-SE': 'amse', 'AM_S-SE': 'amse', 'SE-SE': 'sese',
            '?-SE': 'other', 'AM_P-T3': 'other'}


def _mk_chains():
    out = []
    for i, t in enumerate(TYPES):
        x, y, z = (i * 7.3) % 20, (i * 3.1) % 20, 0.5 + (i * 1.7) % 9
        dx, dy, dz = 0.6 + (i % 3) * 0.3, -0.4 + (i % 4) * 0.25, 0.3 + (i % 5) * 0.2
        x2 = min(19.9, max(0.1, x + dx))
        y2 = min(19.9, max(0.1, y + dy))
        out.append({'p1': [round(x, 3), round(z, 3), round(y, 3)], 'p2': [round(x2, 3), round(z + dz, 3), round(y2, 3)],
                    'fn': round(1.0 + (i * 37 % 50) / 10.0 + 0.001 * (1 + i % 9), 3), 'type': t})
    #  주기 경계를 넘는 접촉 셋 — x 면 · y 면 · 모서리 (원자 중심은 셀 안 · 최소상 거리 1 µm 남짓)
    out.append({'p1': [0.4, 3.0, 6.0], 'p2': [19.7, 3.4, 6.2], 'fn': 4.113, 'type': 'SE-SE'})
    out.append({'p1': [8.0, 5.0, 19.8], 'p2': [8.3, 5.2, 0.3], 'fn': 4.227, 'type': 'AM_P-SE'})
    out.append({'p1': [19.6, 7.0, 19.7], 'p2': [0.3, 7.3, 0.2], 'fn': 4.331, 'type': 'AM_P-AM_P'})
    #  극단 하나 (나머지 최대의 약 160 배) — 옛 최소–최대 굵기를 무너뜨린 꼴
    out.append({'p1': [10.0, 2.0, 10.0], 'p2': [10.8, 2.5, 10.4], 'fn': 987.654, 'type': 'SE-SE'})
    #  쓸 수 없는 행 — p2 없음 · fn 숫자 아님 · 좌표 NaN
    out.append({'p1': [1, 1, 1], 'fn': 2.0, 'type': 'SE-SE'})
    out.append({'p1': [1, 1, 1], 'p2': [1.5, 1, 1], 'fn': 'x', 'type': 'SE-SE'})
    out.append({'p1': [1, 1, None], 'p2': [1.5, 1, 1], 'fn': 2.5, 'type': 'SE-SE'})
    return out


CHAINS = _mk_chains()
N_BAD = 3
VALID = [c for c in CHAINS if isinstance(c.get('p2'), list) and isinstance(c.get('fn'), (int, float))
         and all(isinstance(v, (int, float)) for v in c['p1'] + c['p2'])]
SE_PARTS = [{'id': 1000 + i, 'type': 'SE', 'x': (i * 2.3) % 20, 'y': (i * 5.7) % 20, 'z': 0.5 + (i * 0.9) % 9, 'r': 0.5} for i in range(40)]
SE_PARTS.append({'id': 1999, 'type': 'SE', 'x': 20.3, 'y': -0.2, 'z': 3.0, 'r': 0.5})            # 덤프가 셀 밖에 둔 중심 (접어 그림)
AM_PARTS = [{'id': 2000, 'type': 'AM_P', 'x': 10, 'y': 10, 'z': 5, 'r': 3}, {'id': 2001, 'type': 'AM_S', 'x': 3, 'y': 15, 'z': 2, 'r': 1}]
FN_STRINGS = sorted({f'{c["fn"]:.3f}' for c in VALID} | {'987.65', '987.7'})     # 저장 fn (소수 셋째 자리가 0 아님 — 수 · 몫 글자와 겹치지 않는 꼴)
UNIT_RE = re.compile(r'µN|μN|\buN\b|mN|\bnN\b|\bN\)', re.I)


def ref_select(chains, n):
    """가장 센 n 개 — fn 내림차순 · 같으면 먼저 나온 것 (안정) · n 0 = 전부"""
    v = [(i, c) for i, c in enumerate(chains) if c in VALID]
    v.sort(key=lambda x: (-x[1]['fn'], x[0]))
    v = [c for _i, c in v]
    return v if not n or n >= len(v) else v[:n]


def ref_pct(vals, q):
    """numpy.percentile (linear) 과 같은 식"""
    a = sorted(vals)
    if not a:
        return float('nan')
    pos = (len(a) - 1) * q / 100.0
    lo, hi = math.floor(pos), math.ceil(pos)
    return a[lo] + (a[hi] - a[lo]) * (pos - lo)


def min_image_len(c, L=20.0):
    x1, z1, y1 = c['p1']
    x2, z2, y2 = c['p2']
    dx, dy = x2 - x1, y2 - y1
    dx -= L * round(dx / L)
    dy -= L * round(dy / L)
    return math.sqrt(dx * dx + dy * dy + (z2 - z1) ** 2)


FC_FNS = ('fcGroupOf', 'fcSelect', 'fcPercentile', 'fcScale', 'fcThickT', 'fcStats', 'fcSegments', 'fcForceHex', 'fcColorHex', 'fcBaseRadius',
          'fcLegendHtml', 'fcLegendSpec', 'fcPngName')
FC_RENDER = ('fcOpt', 'buildForceChainGroup', 'renderForceChains', '_teardownForceChains', '_fcWire', 'forceChainToggle', 'fcLoad')
FC_WINDOW = ('showForceChainView', 'figFrameGroup', 'figContextMeshes', 'figCapturePNG', 'figPngNote')
FC_DRAW = ('fcLegendPNG', 'fcCompositePNG', 'fcDrawLegend')
TAU_HELP = ('tauPathsFoldPieces', 'tauPathsWrapParticles', 'tauPathsFrustumFit')


def need(js, names):
    """js_fn 으로 잘라 낸다 — `async function` 이면 async 를 붙여 둔다 (js_fn 은 'function 이름(' 부터 자른다 → await 가 문법 오류가 된다)"""
    out, miss = [], []
    for n in names:
        try:
            f = js_fn(js, n)
            i = js.index(f'function {n}(')
            out.append(('async ' + f) if js[max(0, i - 6):i] == 'async ' else f)
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


def consts(js):
    """FC_DEF · COL (객체 상수) — 없으면 빈 글"""
    out, miss = [], []
    for n in ('COL', 'FC_DEF'):
        try:
            i = js.index(f'const {n} = {{')
            from test_closed_param_labels import _balanced
            out.append(f'const {n} = ' + _balanced(js, js.index('{', i)) + ';')
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


def data_js():
    return ('const CH = ' + json.dumps(CHAINS) + ';\nconst BOX = ' + json.dumps(BOX) + ';\nconst SEP = ' + json.dumps(SE_PARTS)
            + ';\nconst AMP = ' + json.dumps(AM_PARTS) + ';\n')


# ══════════════════════════════════════════════════════════════════════════════
#  [U] 조작판 배선
# ══════════════════════════════════════════════════════════════════════════════
def section_ui(js):
    print('[U] 조작판 배선')
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    dem = bc[bc.find('Mesh (plate)'):] if 'Mesh (plate)' in bc else ''
    mpm = bc[:bc.find('Mesh (plate)')] if 'Mesh (plate)' in bc else bc
    i_fc, i_ap = dem.find('id="force-chain-toggle"'), dem.find('data-action="tauPathsView"')
    chk('U1 DEM 조작판 — Force Chain 체크박스 바로 아래 범례 · 조작 칸 (id fc-panel · 처음엔 숨김)',
        re.search(r'id="force-chain-toggle".{0,200}?<div id="fc-panel" style="display:none', dem, re.S) is not None, dem[i_fc:i_fc + 300])
    chk('U2 "Force Chain View" 단추 (data-action forceChainView · All Paths View 바로 뒤) · MPM 조작판엔 없음',
        re.search(r'<button data-action="forceChainView"[^>]*>Force Chain View</button>', dem) is not None
        and 0 <= i_ap < dem.find('data-action="forceChainView"') and 'forceChainView' not in mpm)
    try:
        wc = js_fn(js, 'wireControls')
    except (ValueError, AssertionError):
        wc = ''
    chk("U3 wireControls — 체크박스 change → forceChainToggle(state, 켬, 아직 켬?) (불러오는 사이 끄면 그리지 않는다) · action 'forceChainView' → showForceChainView(state)",
        re.search(r"fcToggle\.addEventListener\('change', \(\) => forceChainToggle\(state, fcToggle\.checked, \(\) => fcToggle\.checked\)\)", wc) is not None
        and re.search(r"action === 'forceChainView'\)\s*\{\s*showForceChainView\(state\);", wc) is not None)
    chk('U4 옛 그리기 (TubeGeometry 하나씩 · 불투명도 = 힘) 는 없다', 'opacity: 0.15 + t * 0.85' not in wc and 'TubeGeometry(curve' not in wc)


# ══════════════════════════════════════════════════════════════════════════════
#  [F] 순수 함수
# ══════════════════════════════════════════════════════════════════════════════
F_RUN = r"""
const OUT = {};
OUT.def = FC_DEF;
OUT.groupOf = Object.fromEntries(['AM_P-AM_P', 'AM_P-AM_S', 'AM_S-AM_S', 'AM_P-SE', 'AM_S-SE', 'SE-SE', '?-SE', 'AM_P-T3', 'SE', '', null, 'AM_S-AM_P-SE']
  .map(t => [String(t), fcGroupOf(t)]));
const sel = fcSelect(CH, 0), sel10 = fcSelect(CH, 10), sel30 = fcSelect(CH, 30);
const key = c => c.type + '@' + c.fn + '@' + c.p1.join(',');
OUT.sel = { n: sel.drawn.length, nAll: sel.nAll, nBad: sel.nBad, keys: sel.drawn.map(key) };
OUT.sel10 = sel10.drawn.map(key); OUT.sel30n = sel30.drawn.length;
{ const tie = [{ p1: [0, 0, 0], p2: [1, 0, 0], fn: 5, type: 'SE-SE' }, { p1: [2, 0, 0], p2: [3, 0, 0], fn: 5, type: 'AM_P-SE' }, { p1: [4, 0, 0], p2: [5, 0, 0], fn: 7, type: 'SE-SE' }];
  OUT.tie = fcSelect(tie, 2).drawn.map(c => c.type + c.fn); }
OUT.pct = [[1, 2, 3, 4], [5], [3, 1, 2], [10, 20, 30, 40, 50, 60]].map(a => [5, 25, 50, 95, 100].map(q => fcPercentile(a.slice().sort((x, y) => x - y), q)));
const sc = fcScale(sel.drawn);
OUT.scale = sc;
OUT.t = sel.drawn.map(c => fcThickT(c.fn, sc.lo, sc.hi));
OUT.tFlat = [fcThickT(3, 2, 2), fcThickT(1, 2, 5), fcThickT(9, 2, 5), fcThickT(3.5, 2, 5)];
const fns = sel.drawn.map(c => c.fn), mx = Math.max(...fns), mn = Math.min(...fns);
OUT.tOld = fns.map(f => (f - mn) / (mx - mn));
const st = fcStats(sel.drawn);
OUT.stats = st;
OUT.stats10 = fcStats(sel10.drawn);
OUT.statsEmpty = fcStats([]);
const sg = fcSegments(sel.drawn, BOX);
OUT.seg = { segs: sg.segs.map(s => ({ k: s.k, pieces: s.pieces, nCut: s.nCut })), nWrap: sg.nWrap, nCut: sg.nCut };
OUT.force = Array.from({ length: 21 }, (_, i) => fcForceHex(i / 20));
OUT.colors = ['amam', 'amse', 'sese', 'other'].map(g => fcColorHex('group', g, 0.3));
OUT.colorsForce = [0, 0.5, 1].map(t => fcColorHex('force', 'amam', t));
OUT.r0 = [fcBaseRadius(BOX), fcBaseRadius({ x_min: 0, x_max: 50, y_min: 0, y_max: 40 }), fcBaseRadius({})];
const OPT = { color: 'group', n: 0, show: { amam: true, amse: true, sese: true, other: true }, width: 1 };
OUT.legDark = fcLegendHtml(st, sel, OPT, { nWrap: sg.nWrap, nCut: sg.nCut }, false);
OUT.legLight = fcLegendHtml(st, sel, Object.assign({}, OPT, { color: 'force' }), { nWrap: sg.nWrap, nCut: sg.nCut }, true);
OUT.legEmpty = fcLegendHtml(fcStats([]), fcSelect([], 0), OPT, null, false);
OUT.spec = fcLegendSpec(st, sel, OPT);
OUT.specForce = fcLegendSpec(st, sel, Object.assign({}, OPT, { color: 'force' }));
{ const d1 = sel.drawn.slice(1), s1 = { drawn: d1, nAll: sel.nAll, nBad: sel.nBad };      // 극단 하나를 뺀 집합 — 쏠림 경고가 없어야 한다
  OUT.legNoTop = fcLegendHtml(fcStats(d1), s1, OPT, null, false); OUT.specNoTop = fcLegendSpec(fcStats(d1), s1, OPT); OUT.topShare = st.topShare; OUT.topKey = st.topKey; }
OUT.png = [fcPngName(st, sel, OPT), fcPngName(st, sel10, Object.assign({}, OPT, { color: 'force' })),
           fcPngName(st, sel, Object.assign({}, OPT, { show: { amam: true, amse: false, sese: true, other: false } }))];
console.log(JSON.stringify(OUT));
"""


def lum(h):
    return TPV.lum(h)


def section_pure(js):
    print('[F] 순수 함수 (node)')
    if not shutil.which('node'):
        chk('F0 node 필요', False, 'node 미설치')
        return None
    src, miss = need(js, FC_FNS + TAU_HELP)
    cs, miss_c = consts(js)
    if not chk('F0 viewer3d.js 에서 ' + ' · '.join(FC_FNS) + ' · FC_DEF 를 잘라 냈다', not miss and not miss_c, f'없음 {miss + miss_c}'):
        return None
    res = run_node('"use strict";\n' + cs + '\n' + src + '\n' + TPV.js_const(js, 'TAUP_VIEW_DEF') + '\n' + data_js() + F_RUN)
    if not chk('F0b node 실행', res is not None):
        return None
    d = res['def']
    gk = [g[0] for g in d.get('groups', [])]
    chk('F1 FC_DEF — 묶음 넷 (amam · amse · sese · other) · 색 = 검증한 3 색 (#2a78d6 · #eb6834 · #1baf7a — dataviz 기준 팔레트 1–3 칸 · 색각 이상 ΔE 9.2) + 기타 회색 · '
        '수 [500 · 1000 · 2000 · 5000 · 전부] (기본 5000) · 백분위 5 · 95 · 고르기 규칙 문구',
        gk == ['amam', 'amse', 'sese', 'other'] and [g[2] for g in d['groups']] == [0x2a78d6, 0xeb6834, 0x1baf7a, 0x898781]
        and [g[1] for g in d['groups']] == ['AM–AM', 'AM–SE', 'SE–SE', '기타'] and d.get('ns') == [500, 1000, 2000, 5000, 0]
        and d.get('nDefault') == 5000 and (d.get('pLo'), d.get('pHi')) == (5, 95)
        and d.get('rule') == '상위 10 % 접촉 (analyze_contacts) 중 가장 센 N 개 · 굵기 = 상대 힘 (5–95 백분위)', repr(d)[:400])
    go = res['groupOf']
    chk('F2 접촉 쌍 → 묶음 — AM_P · AM_S 끼리 = AM–AM · AM 과 SE = AM–SE · SE 끼리 = SE–SE · 모르는 이름 (? · T3) · 반쪽 · 셋 이상 = 기타',
        all(go[t] == g for t, g in GROUP_OF.items()) and go['SE'] == 'other' and go[''] == 'other' and go['null'] == 'other'
        and go['AM_S-AM_P-SE'] == 'other', repr(go))
    s = res['sel']
    want_all = ref_select(CHAINS, 0)
    key = lambda c: f"{c['type']}@{c['fn']:g}@{','.join(f'{v:g}' for v in c['p1'])}"
    chk(f'F3 가장 센 N 개 — 전부 = 쓸 수 있는 {len(VALID)} 개 (fn 내림차순) · 쓸 수 없는 행 {N_BAD} 개 (p2 없음 · fn 숫자 아님 · 좌표 NaN) 는 세고 뺀다 · '
        'N 10 = 앞 10 · N > 수 = 전부 · 같은 fn 이면 먼저 나온 것',
        s['n'] == len(VALID) and s['nAll'] == len(CHAINS) and s['nBad'] == N_BAD
        and [k.split('@')[0] for k in s['keys']] == [c['type'] for c in want_all]
        and [float(k.split('@')[1]) for k in s['keys']] == [c['fn'] for c in want_all]
        and len(res['sel10']) == 10 and [float(k.split('@')[1]) for k in res['sel10']] == [c['fn'] for c in want_all[:10]]
        and res['sel30n'] == 30 and res['tie'] == ['SE-SE7', 'SE-SE5'], repr(s)[:300])
    pct_bad = []
    for a, row in zip([[1, 2, 3, 4], [5], [3, 1, 2], [10, 20, 30, 40, 50, 60]], res['pct']):
        for q, v in zip([5, 25, 50, 95, 100], row):
            if abs(v - ref_pct(a, q)) > 1e-12:
                pct_bad.append((a, q, v, ref_pct(a, q)))
    chk('F4 백분위 = numpy linear 식 (q 5 · 25 · 50 · 95 · 100 · 한 값 · 섞인 순서)', not pct_bad, repr(pct_bad))
    fns = [c['fn'] for c in want_all]
    lo, hi = ref_pct(fns, 5), ref_pct(fns, 95)
    sc = res['scale']
    t = res['t']
    t_old = res['tOld']
    srt = sorted(t)
    med = srt[len(srt) // 2]
    chk(f'F5 굵기 축 = 고른 집합 fn 의 5 · 95 백분위 ({sc["lo"]:.3f} · {sc["hi"]:.3f}) 로 자른 상대 힘 — t ∈ [0, 1] · 아래 5 % = 0 · 위 5 % = 1',
        abs(sc['lo'] - lo) < 1e-12 and abs(sc['hi'] - hi) < 1e-12 and all(0 <= x <= 1 for x in t)
        and all((x == 0) == (f <= lo) for x, f in zip(t, fns)) and all((x == 1) == (f >= hi) for x, f in zip(t, fns)), repr(sc))
    frac_old = sum(1 for x in t_old if x < 0.05) / len(t_old)
    chk(f'F5b 극단 하나 (fn {max(fns):g} ≈ 나머지 최대의 {max(fns) / sorted(fns)[-2]:.0f} 배) 가 나머지를 지우지 않는다 — 옛 최소–최대: {frac_old:.0%} 가 t < 0.05 (거의 다 옅은 노랑) · '
        f'새 축: 가운데 경로 t = {med:.2f} · 사분위 폭 {srt[3 * len(srt) // 4] - srt[len(srt) // 4]:.2f}',
        frac_old >= 0.95 and 0.25 <= med <= 0.75 and srt[3 * len(srt) // 4] - srt[len(srt) // 4] >= 0.3, repr((frac_old, med)))
    chk('F5c 굵기 축이 한 점 (최소 = 최대) 이면 0.5 · 밖은 0 · 1 로 자른다', res['tFlat'] == [0.5, 0, 1, 0.5], repr(res['tFlat']))
    st = res['stats']
    by = {g['key']: g for g in st['groups']}
    want_n = {k: sum(1 for c in want_all if GROUP_OF[c['type']] == k) for k in ('amam', 'amse', 'sese', 'other')}
    want_s = {k: sum(c['fn'] for c in want_all if GROUP_OF[c['type']] == k) for k in want_n}
    tot = sum(want_s.values())
    chk(f'F6 묶음별 수 = {want_n} · 힘 합 몫 = 묶음 fn 합 / 전체 fn 합 × 100 (상대 · 단위 없음)',
        {k: by[k]['n'] for k in by} == want_n and all(abs(by[k]['share'] - 100 * want_s[k] / tot) < 1e-9 for k in want_n) and st['n'] == len(want_all),
        repr({k: (by[k]['n'], round(by[k]['share'], 3)) for k in by}))
    shown = [float(by[k]['shareTxt']) for k in by]
    chk(f'F6b 몫 합 = 100 (값 {sum(g["share"] for g in st["groups"]):.12f}) · 표시 (소수 한 자리 · 큰 나머지 반올림) 합도 정확히 100.0 ({by["amam"]["shareTxt"]} · '
        f'{by["amse"]["shareTxt"]} · {by["sese"]["shareTxt"]} · {by["other"]["shareTxt"]})',
        abs(sum(g['share'] for g in st['groups']) - 100) < 1e-9 and abs(sum(shown) - 100.0) < 1e-9
        and all(re.fullmatch(r'\d+\.\d', by[k]['shareTxt']) for k in by)
        and abs(sum(float(g['shareTxt']) for g in res['stats10']['groups']) - 100.0) < 1e-9, repr(shown))
    se_ = res['statsEmpty']
    chk('F6c 고른 접촉이 없으면 수 0 · 몫 0 (나눗셈 없음)', se_['n'] == 0 and all(g['n'] == 0 and g['share'] == 0 for g in se_['groups']), repr(se_))
    sg = res['seg']
    bad_in, bad_len, longest = [], [], 0.0
    for sseg, c in zip(sg['segs'], want_all):
        pts = [q for pc in sseg['pieces'] for q in pc]
        if not all(0 <= q[0] <= 20 and 0 <= q[1] <= 20 for q in pts):
            bad_in.append((c['p1'], c['p2'], sseg['pieces']))
        ln = sum(math.dist(a, b) for pc in sseg['pieces'] for a, b in zip(pc, pc[1:]))
        if abs(ln - min_image_len(c)) > 1e-9:
            bad_len.append((c['p1'], c['p2'], ln, min_image_len(c)))
        longest = max([longest] + [math.dist(a, b) for pc in sseg['pieces'] for a, b in zip(pc, pc[1:])])
    n_per = sum(1 for c in want_all if min_image_len(c) < math.dist(
        (c['p1'][0], c['p1'][2], c['p1'][1]), (c['p2'][0], c['p2'][2], c['p2'][1])) - 1e-9)
    chk(f'F7 상자 안 — 주기 경계를 넘는 접촉 {sg["nWrap"]} 개 (= 최소상이 단순 차와 다른 접촉 {n_per}) = 면에서 잘라 반대 면 (자른 곳 {sg["nCut"]}) · 점 전부 상자 [0, 20]² 안 · '
        f'그린 길이 = 최소상 거리 · 가장 긴 토막 {longest:.2f} µm < 상자 반폭 (상자를 가로지르는 관 없음)',
        sg['nWrap'] == n_per == 3 and sg['nCut'] == 4 and not bad_in and not bad_len and longest < 10, repr((bad_in, bad_len))[:500])
    fh = res['force']
    lums = [lum(h) for h in fh]
    chk('F8 색 — 접촉 쌍 = 묶음 색 (t 와 무관) · 힘 모드 = 옛 노랑 → 빨강 (HSL 0.15 → 0 · 밝기 0.85 → 0.40) · 휘도가 힘을 따라 줄어든다 (21 점)',
        res['colors'] == [0x2a78d6, 0xeb6834, 0x1baf7a, 0x898781] and all(b < a for a, b in zip(lums, lums[1:]))
        and res['colorsForce'] == [fh[0], fh[10], fh[20]] and fh[0] == 0xfff7b3 and fh[20] == 0xcc0000, repr([hex(h) for h in fh[::5]]))
    chk('F8b 관 굵기 기준 = 상자 x · y 중 긴 쪽 × 0.004 (20 µm → 0.08 · 50 µm → 0.2 · 상자 없음 → 0.2)',
        [round(v, 9) for v in res['r0']] == [0.08, 0.2, 0.2], repr(res['r0']))
    dark, light = res['legDark'], res['legLight']
    pd, pl = TPV._plain(dark), TPV._plain(light)
    rows_ok = all(f'{lab} {by[k]["n"]} 개 · 힘 합 {by[k]["shareTxt"]} %' in pd for k, lab in (('amam', 'AM–AM'), ('amse', 'AM–SE'), ('sese', 'SE–SE'), ('other', '기타')))
    chk('F9 범례 — 고르기 규칙 ("상위 10 % 접촉 (analyze_contacts) 중 가장 센 N 개 · 굵기 = 상대 힘 (5–95 백분위)") · 묶음마다 견본 색 · 이름 · 수 · 힘 합 몫 · 저장 수 · 쓸 수 없는 행 · '
        '주기 경계 접기 · 조작 (색 · 수 · 묶음 끄기 · 범례 PNG · 그림 창)',
        FC_RULE in pd and rows_ok and f'저장 {len(CHAINS)} 개 중' in pd and f'쓸 수 없는 행 {N_BAD} 개' in pd
        and '주기 경계를 넘는 접촉 3 개 = 면에서 잘라 반대 면' in pd
        and all(f'id="{i}"' in dark for i in ('fc-color', 'fc-n', 'fc-show-amam', 'fc-show-amse', 'fc-show-sese', 'fc-show-other', 'fc-legend-png', 'fc-view'))
        and all(f'#{c:06x}' in dark for c in (0x2a78d6, 0xeb6834, 0x1baf7a)), pd[:700])
    chk('F9b 범례 글자는 잉크 색 (견본만 묶음 색) — 묶음 색으로 칠한 글자 없음', not re.search(r'color:\s*#(2a78d6|eb6834|1baf7a)', dark + light, re.I), dark[:300])
    leaks = [s_ for s_ in FN_STRINGS if s_ in pd or s_ in pl] + [m.group(0) for m in UNIT_RE.finditer(pd + ' ' + pl)]
    chk(f'F9c 범례에 fn 절대값 · 힘 단위가 없다 (저장 fn {len(FN_STRINGS)} 꼴 · µN · mN · N) — 상대 크기만 (force_chains.json 의 fn 표기는 힘 분포와 scale 배 다르다)',
        not leaks and '상대' in pd, repr(leaks[:8]))
    chk('F9d 힘 색 모드 범례 = 옅음 → 진함 띠 ("약함" → "셈" · 상대) · 견본 색 대신 · 묶음 수 · 몫은 그대로 (그림 창 = 밝은 바탕 글자)',
        'linear-gradient' in light and '약함' in pl and '셈' in pl and 'AM–SE' in pl and '#1baf7a' not in light, pl[:400])
    chk('F9e 자료가 없으면 그렇다고 말한다 (force_chains.json — 접촉 분석 단계 산출물)', 'force_chains.json' in TPV._plain(res['legEmpty']), res['legEmpty'][:200])
    sp = res['spec']
    rows = sp.get('rows') or []
    chk('F10 범례 PNG 스펙 (영문) — 제목 = 가장 센 N 개 · 줄마다 색 · 이름 · 수 · 몫 (합 100) · 규칙 (relative only) · fn 값 · 단위 없음',
        [r['label'] for r in rows] == ['AM–AM', 'AM–SE', 'SE–SE', 'Other'] and [r['color'] for r in rows] == [0x2a78d6, 0xeb6834, 0x1baf7a, 0x898781]
        and [r['n'] for r in rows] == [by[k]['n'] for k in ('amam', 'amse', 'sese', 'other')]
        and abs(sum(float(r['share']) for r in rows) - 100.0) < 1e-9 and str(len(want_all)) in sp['title'] and 'strongest' in sp['title']
        and 'relative' in sp['note'] and not any(s_ in json.dumps(sp) for s_ in FN_STRINGS) and not UNIT_RE.search(json.dumps(sp, ensure_ascii=False)),
        repr(sp)[:500])
    spf = res['specForce']
    chk('F10b 힘 모드 스펙 = 띠 (색 함수 = 관 색 · weak → strong) · 줄 견본 없음 (색 = 힘)', spf.get('mode') == 'force' and spf.get('ramp') == [fh[0], fh[10], fh[20]]
        and all(r.get('color') is None for r in spf.get('rows') or [{}]), repr(spf)[:300])
    top_pct = 100 * max(fns) / sum(fns)
    top_lab = {'amam': 'AM–AM', 'amse': 'AM–SE', 'sese': 'SE–SE', 'other': '기타'}[GROUP_OF[want_all[0]['type']]]
    top_txt = str(math.floor(top_pct + 0.5))                          # JS toFixed(0) 와 같은 반올림 (절반은 올림)
    warn = f'가장 센 접촉 하나가 힘 합의 {top_txt} % ({top_lab})'
    chk(f'F9f 몫이 접촉 하나에 쏠리면 (≥ 25 %) 범례가 그렇다고 말한다 — "{warn}" (메인 · 그림 창 · 범례 PNG 영문) · 그 하나를 빼면 경고 없음 '
        '(몫 = 요청된 fn 합 그대로 · 굵기 축은 5–95 백분위라 영향 없음)',
        res.get('topShare') is not None and abs(res['topShare'] - top_pct) < 1e-9 and res.get('topKey') == GROUP_OF[want_all[0]['type']]
        and warn in pd and warn in pl and '가장 센 접촉 하나가' not in TPV._plain(res['legNoTop'])
        and f'the single strongest contact carries {top_txt} % of the summed force ({top_lab})' in res['spec']['note']
        and 'single strongest contact' not in res['specNoTop']['note'], repr((res.get('topShare'), top_pct, pd[-300:])))
    p1, p2, p3 = res['png']
    chk(f'F11 PNG 이름 — force_chains_top<N>_<pair|force>[_<보인 묶음>].png ({p1} · {p2} · {p3})',
        p1 == f'force_chains_top{len(want_all)}_pair.png' and p2 == 'force_chains_top10_force.png' and p3 == f'force_chains_top{len(want_all)}_pair_AMAM-SESE.png',
        repr(res['png']))
    return res


FC_RULE = '상위 10 % 접촉 (analyze_contacts) 중 가장 센 N 개 · 굵기 = 상대 힘 (5–95 백분위)'


# ══════════════════════════════════════════════════════════════════════════════
#  [R] 메인 겹쳐 그리기 (THREE 껍데기)
# ══════════════════════════════════════════════════════════════════════════════
R_RUN = r"""
(async () => {
const OUT = { err: null };
try {
  let nFetch = 0;
  globalThis.fetch = async (u) => { nFetch++; OUT.url = u; return { ok: true, json: async () => JSON.parse(JSON.stringify(CH)) }; };
  const scene = new Group();
  const state = { scene, dataUrl: '/results/demo/3d-data', data: { box: BOX }, viewMode: 'default' };
  const meshes = () => { const out = []; if (state.forceChainGroup) state.forceChainGroup.traverse(o => { if (o.isInstancedMesh) out.push(o); }); return out; };
  const summ = () => meshes().map(m => ({ g: m.userData.group, kind: m.userData.kind, n: m.count, visible: m.visible, cols: [...new Set(m.cols)],
    r: m.mats.map(x => x.s[0]), len: m.mats.map(x => x.s[1]), op: m.material.opacity, tr: !!m.material.transparent, mid: m.mats.map(x => x.p) }));
  await forceChainToggle(state, true);
  OUT.on = { s: summ(), panel: (ELS['fc-panel'] || {}).innerHTML || '', display: ((ELS['fc-panel'] || {}).style || {}).display, nFetch,
             inScene: scene.children.includes(state.forceChainGroup), opt: Object.assign({}, state._fcOpt) };
  //  묶음 끄기 — 다시 짓지 않고 숨김
  const g0 = state.forceChainGroup;
  ELS['fc-show-sese'].checked = false; fire('fc-show-sese', 'change');
  OUT.hide = { same: state.forceChainGroup === g0, s: summ() };
  ELS['fc-show-sese'].checked = true; fire('fc-show-sese', 'change');
  //  색 모드 = 힘 → 다시 짓기
  ELS['fc-color'].value = 'force'; fire('fc-color', 'change');
  OUT.force = { s: summ(), rebuilt: state.forceChainGroup !== g0, oldDisposed: (() => { let d = true; g0.traverse(o => { if (o.isInstancedMesh && !o.disposed) d = false; }); return d; })() };
  ELS['fc-color'].value = 'group'; fire('fc-color', 'change');
  //  수 = 10
  ELS['fc-n'].value = '10'; fire('fc-n', 'change');
  OUT.n10 = { s: summ(), panel: (ELS['fc-panel'] || {}).innerHTML || '' };
  ELS['fc-n'].value = '0'; fire('fc-n', 'change');
  //  끄기 · 다시 켜기 (다시 불러오지 않는다)
  await forceChainToggle(state, false);
  OUT.off = { visible: state.forceChainGroup ? state.forceChainGroup.visible : null, display: ((ELS['fc-panel'] || {}).style || {}).display };
  await forceChainToggle(state, true);
  OUT.again = { visible: state.forceChainGroup.visible, nFetch, display: ((ELS['fc-panel'] || {}).style || {}).display };
  OUT.legendPng = LOG.fcLegend.slice();
  fire('fc-legend-png', 'click'); fire('fc-view', 'click');
  OUT.legendPng = LOG.fcLegend.slice(); OUT.modal = LOG.fcModal;
  //  자료 없음
  globalThis.fetch = async () => ({ ok: true, json: async () => [] });
  const st2 = { scene: new Group(), dataUrl: '/results/none/3d-data', data: { box: BOX } };
  await forceChainToggle(st2, true);
  OUT.none = { group: st2.forceChainGroup ? st2.forceChainGroup.children.length : null, panel: (ELS['fc-panel'] || {}).innerHTML || '' };
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
})();
"""

R_EXTRA = r"""
LOG.fcLegend = []; LOG.fcModal = 0;
function fcLegendPNG(spec, name) { LOG.fcLegend.push([spec && spec.title, name]); }
function showForceChainView(state) { LOG.fcModal++; }
"""


def section_render(js):
    print('[R] 메인 겹쳐 그리기 (THREE 껍데기)')
    if not shutil.which('node'):
        chk('R0 node 필요', False, 'node 미설치')
        return
    src, miss = need(js, FC_FNS + FC_RENDER + TAU_HELP)
    cs, miss_c = consts(js)
    if not chk('R0 그리기 함수 (' + ' · '.join(FC_RENDER) + ') 를 잘라 냈다', not miss and not miss_c, f'없음 {miss + miss_c}'):
        return
    rr = run_node(TPV.R_SHIM + R_EXTRA + cs + '\n' + src + '\n' + TPV.js_const(js, 'TAUP_VIEW_DEF') + '\n' + data_js() + R_RUN)
    if not chk('R0b node 실행 (forceChainToggle · renderForceChains)', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:900]):
        return
    want_all = ref_select(CHAINS, 0)
    fns = [c['fn'] for c in want_all]
    lo, hi = ref_pct(fns, 5), ref_pct(fns, 95)
    on = rr['on']
    by = {m['g']: m for m in on['s']}
    n_pieces = {g: 0 for g in ('amam', 'amse', 'sese', 'other')}
    for c in want_all:
        per = min_image_len(c) < math.dist((c['p1'][0], c['p1'][2], c['p1'][1]), (c['p2'][0], c['p2'][2], c['p2'][1])) - 1e-9
        n_pieces[GROUP_OF[c['type']]] += 1 + (0 if not per else (2 if c['type'] == 'AM_P-AM_P' else 1))
    chk(f'R1 켜면 force-chains 를 한 번 불러 (주소 = 3d-data → force-chains) 묶음마다 InstancedMesh 하나 · 원기둥 = 접촉 (주기 경계에서 자른 토막 포함 {n_pieces})',
        on['nFetch'] == 1 and rr['url'] == '/results/demo/force-chains' and on['inScene'] is True
        and sorted(by) == ['amam', 'amse', 'other', 'sese'] and {g: by[g]['n'] for g in by} == n_pieces and all(m['kind'] == 'fcSeg' for m in on['s']),
        repr({g: by[g]['n'] for g in by}))
    chk('R2 색 = 묶음 색 (묶음 안 한 색) — AM–AM 파랑 · AM–SE 주황 · SE–SE 청록 · 기타 회색',
        by['amam']['cols'] == [0x2a78d6] and by['amse']['cols'] == [0xeb6834] and by['sese']['cols'] == [0x1baf7a] and by['other']['cols'] == [0x898781],
        repr({g: by[g]['cols'] for g in by}))
    chk('R3 불투명도 한 값 (힘으로 흐리지 않는다 — 모든 묶음 불투명 1 · 투명 끔)', all(m['op'] == 1 and m['tr'] is False for m in on['s']),
        repr([(m['g'], m['op'], m['tr']) for m in on['s']]))
    r_all = sorted(r for m in on['s'] for r in m['r'])
    r0 = 0.004 * 20
    chk(f'R4 굵기 = 상대 힘 (5–95 백분위 자름) — 반지름 {r_all[0]:.4f} … {r_all[-1]:.4f} µm = r0 × (0.35 … 2.0) · 가운데 반지름 {r_all[len(r_all) // 2]:.4f} (옛 최소–최대였다면 거의 다 가장 가늘다)',
        abs(r_all[0] - 0.35 * r0) < 1e-9 and abs(r_all[-1] - 2.0 * r0) < 1e-9 and 0.6 * r0 < r_all[len(r_all) // 2] < 1.8 * r0, repr(r_all[::10]))
    pn = TPV._plain(on['panel'])
    chk('R5 범례 칸이 보인다 (고르기 규칙 · 묶음 수 · 몫) · 옵션 기본 = 접촉 쌍 · 5000 · 묶음 다 켬 · 굵기 1',
        on['display'] == 'block' and FC_RULE in pn and 'AM–SE' in pn
        and on['opt'] == {'color': 'group', 'n': 5000, 'show': {'amam': True, 'amse': True, 'sese': True, 'other': True}, 'width': 1}, repr(on['opt']))
    hd = rr['hide']
    hv = {m['g']: m['visible'] for m in hd['s']}
    chk('R6 묶음 끄기 (SE–SE) = 다시 짓지 않고 그 InstancedMesh 만 숨김', hd['same'] is True and hv == {'amam': True, 'amse': True, 'sese': False, 'other': True}, repr(hv))
    fo = rr['force']
    cols_f = sorted({c for m in fo['s'] for c in m['cols']})
    chk('R7 색 모드 = 힘 → 다시 짓는다 (옛 묶음 GPU 자원 해제) · 색이 힘을 따른다 (여러 색 · 묶음 색 아님)',
        fo['rebuilt'] is True and fo['oldDisposed'] is True and len(cols_f) > 4 and 0x2a78d6 not in cols_f, repr([hex(c) for c in cols_f[:6]]))
    n10 = rr['n10']
    chk('R8 수 = 10 → 가장 센 10 개만 (원기둥 10 + 주기 토막) · 범례 수도 10',
        sum(m['n'] for m in n10['s']) >= 10 and sum(m['n'] for m in n10['s']) <= 13 and '가장 센 10 개' in TPV._plain(n10['panel']), repr([m['n'] for m in n10['s']]))
    chk('R9 끄기 = 숨김 · 범례 칸 숨김 · 다시 켜기 = 다시 불러오지 않고 보임', rr['off'] == {'visible': False, 'display': 'none'}
        and rr['again'] == {'visible': True, 'nFetch': 1, 'display': 'block'}, repr((rr['off'], rr['again'])))
    chk('R10 범례 PNG 단추 = fcLegendPNG (legend_force_chains.png) · 그림 창 단추 = showForceChainView',
        len(rr['legendPng']) == 1 and rr['legendPng'][0][1] == 'legend_force_chains.png' and rr['modal'] == 1, repr(rr['legendPng']))
    chk('R11 자료가 없으면 관 없음 · 범례가 그렇다고 말한다', rr['none']['group'] in (None, 0) and 'force_chains.json' in TPV._plain(rr['none']['panel']), repr(rr['none'])[:300])


# ══════════════════════════════════════════════════════════════════════════════
#  [M] 그림 창 (Force Chain View)
# ══════════════════════════════════════════════════════════════════════════════
M_EXTRA = r"""
LOG.fcLegend = []; LOG.fcComposite = [];
function fcLegendPNG(spec, name) { LOG.fcLegend.push([spec && spec.title, name, spec && spec.rows ? spec.rows.length : null]); }
function fcCompositePNG(url, spec) { LOG.fcComposite.push([url, spec && spec.title]); return Promise.resolve('data:image/png;base64,COMP'); }
//  원기둥 = 양 끝 (방향이 있는 인스턴스) · 구 = 가운데 — 접촉 관도 맞춤 대상 (모양으로 가른다)
function contentPts(sc) { const pts = [];
  sc.traverse(o => {
    if (o.userData && o.userData.isBbox && o.visible) { const a = (o.geometry && o.geometry.args && o.geometry.args[0] && o.geometry.args[0].args) || [0, 0, 0];
      for (const i of [-1, 1]) for (const j of [-1, 1]) for (const k of [-1, 1]) pts.push([o.position.x + i * a[0] / 2, o.position.y + j * a[1] / 2, o.position.z + k * a[2] / 2]); }
    if (o.isInstancedMesh && o.visible) o.mats.forEach(m => { if (m.q) { const h = m.s[1] / 2, d = m.q;
        pts.push([m.p[0] - d[0] * h, m.p[1] - d[1] * h, m.p[2] - d[2] * h], [m.p[0] + d[0] * h, m.p[1] + d[1] * h, m.p[2] + d[2] * h]); }
      else pts.push(m.p.slice()); }); });
  return pts; }
"""

M_RUN = r"""
(async () => {
const OUT = { err: null };
try {
  globalThis.fetch = async () => ({ ok: true, json: async () => JSON.parse(JSON.stringify(CH)) });
  const E = id => document.getElementById(id);
  const fireAsync = (id, type) => Promise.all((ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).map(l => l[1]({ type, target: ELS[id] })));
  const camOf = () => { const c = LOG.cams[LOG.cams.length - 1], t = LOG.ctrls[LOG.ctrls.length - 1];
    return { pos: [c.position.x, c.position.y, c.position.z], target: [t.target.x, t.target.y, t.target.z], up: [c.up.x, c.up.y, c.up.z], fov: c.fov, aspect: c.aspect, near: c.near }; };
  const sceneSum = () => { const sc = LOG.scenes[LOG.scenes.length - 1]; const r = { fc: [], ends: [], bbox: null, grid: null, se: null, am: 0, labels: 0 };
    sc.traverse(o => {
      if (o.isInstancedMesh && o.userData.kind === 'fcSeg') r.fc.push({ g: o.userData.group, n: o.count, visible: o.visible, cols: [...new Set(o.cols)], op: o.material.opacity });
      if (o.isInstancedMesh && o.userData.kind === 'fcSeg') o.mats.forEach(m => { const h = m.s[1] / 2, d = m.q || [0, 1, 0];
        r.ends.push([m.p[0] - d[0] * h, m.p[1] - d[1] * h, m.p[2] - d[2] * h], [m.p[0] + d[0] * h, m.p[1] + d[1] * h, m.p[2] + d[2] * h]); });
      const u = o.userData || {};
      if (u.isBbox) r.bbox = { c: [o.position.x, o.position.y, o.position.z], visible: o.visible };
      if (u.isGrid) r.grid = [o.position.x, o.position.y, o.position.z];
      if (u.isSEContext) r.se = { op: o.material.opacity, visible: o.visible, pts: (u.particles || []).map(p => [p.id, p.x, p.y, p.z]) };
      if (u.isAMContext) r.am++;
      if (u.isAxisLabel) r.labels++; });
    return r; };
  const OPT0 = { color: 'group', n: 5000, show: { amam: true, amse: true, sese: true, other: true }, width: 1 };
  const state = { dataUrl: '/results/demo/3d-data', data: { box: BOX }, seParticles: SEP, amPParticles: AMP.filter(p => p.type === 'AM_P'),
                  amSParticles: AMP.filter(p => p.type === 'AM_S'), _fcOpt: JSON.parse(JSON.stringify(OPT0)) };
  await showForceChainView(state);
  OUT.html = LOG.overlay ? LOG.overlay.innerHTML : '';
  OUT.open = Object.assign(sceneSum(), { title: (E('fcv-title').textContent || ''), info: (E('fcv-info').innerHTML || '') });
  //  PNG — 기본 시점
  await fireAsync('fcv-png-btn', 'click');
  //  가까운 시점 → 맞춤
  const c = LOG.cams[LOG.cams.length - 1], t = LOG.ctrls[LOG.ctrls.length - 1];
  const p0 = c.position.clone();
  c.position.set(t.target.x + 1.5, t.target.y + 1, t.target.z + 1.5);
  OUT.closeCam = camOf();
  await fireAsync('fcv-png-btn', 'click');
  OUT.afterClose = camOf();
  OUT.note = E('fcv-png-note').textContent || '';
  E('fcv-fit').checked = false; fire('fcv-fit', 'change');
  await fireAsync('fcv-png-btn', 'click');
  E('fcv-fit').checked = true; fire('fcv-fit', 'change');
  c.position.copy(p0);
  //  범례 넣기 → 합성
  E('fcv-legend-in').checked = true; fire('fcv-legend-in', 'change');
  await fireAsync('fcv-png-btn', 'click');
  E('fcv-legend-in').checked = false; fire('fcv-legend-in', 'change');
  fire('fcv-legend-btn', 'click');
  //  묶음 끄기 · 색 · 수 · 맥락 막대 · 상자
  E('fcv-show-amam').checked = false; fire('fcv-show-amam', 'change');
  OUT.hideAmam = sceneSum();
  await fireAsync('fcv-png-btn', 'click');
  E('fcv-show-amam').checked = true; fire('fcv-show-amam', 'change');
  E('fcv-color').value = 'force'; fire('fcv-color', 'change');
  OUT.force = Object.assign(sceneSum(), { info: E('fcv-info').innerHTML || '' });
  E('fcv-color').value = 'group'; fire('fcv-color', 'change');
  E('fcv-n').value = '10'; fire('fcv-n', 'change');
  OUT.n10 = Object.assign(sceneSum(), { title: E('fcv-title').textContent || '', info: E('fcv-info').innerHTML || '' });
  { const rad = () => { const r = []; LOG.scenes[LOG.scenes.length - 1].traverse(o => { if (o.isInstancedMesh && o.userData.kind === 'fcSeg') o.mats.forEach(m => r.push(m.s[0])); }); return r; };
    const r1 = rad(); E('fcv-width').value = '200'; fire('fcv-width', 'input'); const r2 = rad();
    OUT.width = { r1: r1.slice(0, 5), r2: r2.slice(0, 5), n1: r1.length, n2: r2.length, val: (E('fcv-width-val') || {}).textContent || '' };
    E('fcv-width').value = '100'; fire('fcv-width', 'input'); }
  E('fcv-se-op').value = '30'; fire('fcv-se-op', 'input');
  E('fcv-am').checked = false; fire('fcv-am', 'change');
  E('fcv-frame').checked = false; fire('fcv-frame', 'change');
  OUT.ctx = sceneSum();
  OUT.saves = LOG.saves.map(s => [s[0].slice(0, 30), s[1]]); OUT.captures = LOG.captures.slice(); OUT.comp = LOG.fcComposite.slice(); OUT.legend = LOG.fcLegend.slice();
  OUT.optAfter = JSON.stringify(state._fcOpt); OUT.optBefore = JSON.stringify(OPT0);
  //  자료 없음 — 창을 열지 않고 안내만
  LOG.overlay = null; LOG.alerts = [];
  globalThis.fetch = async () => ({ ok: true, json: async () => [] });
  await showForceChainView({ dataUrl: '/results/none/3d-data', data: { box: BOX } });
  OUT.none = { overlay: !!LOG.overlay, alerts: LOG.alerts.slice() };
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
})();
"""


def run_window(body):
    return run_node(TPV.M_SHIM + M_EXTRA + body + '\n' + data_js() + M_RUN)


def window_body(js):
    src, miss = need(js, FC_FNS + FC_RENDER + FC_WINDOW + TAU_HELP)
    cs, miss_c = consts(js)
    if miss or miss_c:
        return None, miss + miss_c
    return cs + '\n' + TPV.js_const(js, 'TAUP_VIEW_DEF') + '\n' + src, []


def m_eval(rr):
    """M 절 판정 — 이름 → (참 · 거짓, 덧말).  X 절이 같은 판정을 다시 쓴다."""
    R = {}
    html, o = rr.get('html') or '', rr['open']
    ids = ('fcv-color', 'fcv-n', 'fcv-show-amam', 'fcv-show-amse', 'fcv-show-sese', 'fcv-show-other', 'fcv-se', 'fcv-se-op', 'fcv-am', 'fcv-am-op',
           'fcv-frame', 'fcv-fit', 'fcv-legend-in', 'fcv-png-btn', 'fcv-legend-btn')
    R['M1 창 조작 — 색 (접촉 쌍 · 힘) · 수 · 묶음 끄기 · SE · AM 맥락 (불투명도) · 상자 · 바닥 격자 · PNG 잘림 없게 맞춤 (기본 켬) · 범례 넣기 (기본 끔) · PNG · 범례 PNG'] = (
        all(f'id="{i}"' in html for i in ids) and re.search(r'<input type="checkbox" id="fcv-fit" checked>', html) is not None
        and re.search(r'<input type="checkbox" id="fcv-legend-in"(?![^>]*checked)[^>]*>', html) is not None
        and re.search(r'<option value="group" selected>접촉 쌍</option>', html) is not None, repr([i for i in ids if f'id="{i}"' not in html]))
    pi = TPV._plain(o['info'])
    want_all = ref_select(CHAINS, 0)
    R['M2 창이 열린다 — 머리 = 접촉 수 · 정보 줄 = 고르기 규칙 · 묶음마다 수 · 힘 합 몫 · fn 절대값 · 단위 없음'] = (
        f'— {len(want_all)} 개' in o['title'] and FC_RULE in pi and 'AM–AM' in pi and '힘 합' in pi
        and not any(s_ in pi or s_ in html for s_ in FN_STRINGS) and not TPV_UNIT(pi + html), pi[:300])
    pts = [(p[0], p[2], p[1]) for p in o['ends']]
    longest = max((math.dist(a, b) for a, b in zip(o['ends'][::2], o['ends'][1::2])), default=0)
    R['M3 관 전부 상자 안 (주기 경계를 넘는 접촉 = 면에서 잘라 반대 면) · 가장 긴 토막 < 상자 반폭 · 묶음 색 · 불투명 1'] = (
        bool(pts) and all(-1e-9 <= x <= 20 + 1e-9 and -1e-9 <= y <= 20 + 1e-9 for x, y, _z in pts) and longest < 10
        and sorted(m['g'] for m in o['fc']) == ['amam', 'amse', 'other', 'sese'] and all(m['op'] == 1 for m in o['fc'])
        and {m['g']: m['cols'] for m in o['fc']}['amse'] == [0xeb6834], repr({'longest': longest, 'n': len(pts)}))
    se = o.get('se') or {}
    R['M4 맥락 SE (흐리게 0.08) · AM · 상자 · 바닥 격자 · 축 글자 · 셀 밖 SE 중심은 셀 안으로 접는다'] = (
        se.get('op') == 0.08 and o['am'] >= 1 and o['bbox'] is not None and _close(o['bbox']['c'], [10, 5, 10]) and o['grid'] is not None and o['labels'] >= 1
        and all(0 <= p[1] < 20 and 0 <= p[2] < 20 for p in se.get('pts') or [[0, -1, -1, 0]]), repr({k: o.get(k) for k in ('bbox', 'am', 'labels')}))
    cap = rr.get('captures') or []
    m = TPV.VIEW_MARGIN
    if len(cap) >= 3:
        n0 = TPV.ndc_max(cap[0]['cam'], cap[0]['target'], cap[0]['content'])
        nb = TPV.ndc_max(rr['closeCam'], rr['closeCam']['target'], cap[1]['content'])
        n1 = TPV.ndc_max(cap[1]['cam'], cap[1]['target'], cap[1]['content'])
        n2 = TPV.ndc_max(cap[2]['cam'], cap[2]['target'], cap[2]['content'])
        R['M5 PNG = 투명 (지우기 알파 0 · 배경 없음) · 4× · 축 글자 숨김 · 기본 시점에서 상자 · 관이 다 화면 안'] = (
            cap[0]['alpha'] == 0 and cap[0]['bg'] is None and cap[0]['scale'] == 4 and cap[0]['axisVisible'] and not any(cap[0]['axisVisible'])
            and n0 <= 1 - m + 1e-9, f'{n0}')
        R['M6 PNG 잘림 없게 맞춤 — 가까운 시점 (내용이 화면 밖) 에서도 시선 방향으로만 뒤로 → 상자 꼭짓점 · 관 양 끝이 |NDC| ≤ 1 − 0.04 · 찍은 뒤 시점 그대로 · 안내'] = (
            nb > 1 and n1 <= 1 - m + 1e-9 and rr['afterClose']['pos'] == rr['closeCam']['pos'] and '배 멀리서' in (rr.get('note') or ''),
            f'before {nb} · capture {n1} · note {rr.get("note")!r}')
        R['M6b 맞춤 끔 = 화면 시점 그대로 (잘린다)'] = (cap[2]['cam']['pos'] == rr['closeCam']['pos'] and n2 > 1, f'{n2}')
    else:
        for k in ('M5 PNG = 투명 (지우기 알파 0 · 배경 없음) · 4× · 축 글자 숨김 · 기본 시점에서 상자 · 관이 다 화면 안',
                  'M6 PNG 잘림 없게 맞춤 — 가까운 시점 (내용이 화면 밖) 에서도 시선 방향으로만 뒤로 → 상자 꼭짓점 · 관 양 끝이 |NDC| ≤ 1 − 0.04 · 찍은 뒤 시점 그대로 · 안내',
                  'M6b 맞춤 끔 = 화면 시점 그대로 (잘린다)'):
            R[k] = (False, f'찍기 {len(cap)}')
    saves = rr.get('saves') or []
    comp = rr.get('comp') or []
    leg = rr.get('legend') or []
    name_all = f'force_chains_top{len(want_all)}_pair.png'
    R[f'M7 PNG 이름 ({name_all}) · 범례 넣기 켬 = 합성본 저장 · 범례 PNG 단추 = 따로 (legend_force_chains.png · 줄 넷) · 묶음 끄면 이름에 보인 묶음'] = (
        len(saves) >= 5 and saves[0][1] == name_all and saves[3][0].startswith('data:image/png;base64,COMP') and len(comp) == 1
        and len(leg) == 1 and leg[0][1] == 'legend_force_chains.png' and leg[0][2] == 4
        and saves[4][1] == f'force_chains_top{len(want_all)}_pair_AMSE-SESE-OTHER.png', repr((saves, comp, leg))[:500])
    ha = {x['g']: x['visible'] for x in rr['hideAmam']['fc']}
    R['M8 묶음 끄기 (AM–AM) = 그 관만 숨김 · PNG 맞춤도 숨긴 관은 빼고 셈'] = (
        ha == {'amam': False, 'amse': True, 'sese': True, 'other': True}, repr(ha))
    fo = rr['force']
    cols = sorted({c for x in fo['fc'] for c in x['cols']})
    R['M9 색 = 힘 → 관 색이 힘을 따른다 (여러 색) · 정보 줄 = 약함 → 셈 띠'] = (
        len(cols) > 4 and 0x2a78d6 not in cols and '약함' in TPV._plain(fo['info']), repr([hex(c) for c in cols[:5]]))
    n10 = rr['n10']
    R['M10 수 = 10 → 머리 "10 개" · 관 10 개 (+ 주기 토막) · 정보 줄 "가장 센 10 개"'] = (
        '— 10 개' in n10['title'] and 10 <= sum(x['n'] for x in n10['fc']) <= 13 and '가장 센 10 개' in TPV._plain(n10['info']),
        repr((n10['title'], [x['n'] for x in n10['fc']])))
    cx = rr['ctx']
    R['M11 SE 불투명도 막대 · AM 끄기 · 상자 · 격자 끄기 — 창 안에서만 (메인 옵션 그대로)'] = (
        (cx.get('se') or {}).get('op') == 0.3 and cx['bbox'] is not None and cx['bbox']['visible'] is False
        and rr.get('optAfter') == rr.get('optBefore'), repr((cx.get('se', {}).get('op'), cx.get('bbox'), rr.get('optAfter'))))
    R['M12 자료가 없으면 창을 열지 않고 안내만'] = (rr['none']['overlay'] is False and len(rr['none']['alerts']) == 1, repr(rr['none']))
    wd = rr.get('width') or {}
    R['M13 관 굵기 막대 (창 안 · 0.5–3×) — 2× 면 반지름이 정확히 두 배 (같은 관 수 · 상대 힘 축 그대로) · 값 표시 2.0×'] = (
        bool(wd.get('r1')) and wd.get('n1') == wd.get('n2') and all(abs(b - 2 * a) < 1e-12 for a, b in zip(wd['r1'], wd['r2'])) and wd.get('val') == '2.0×'
        and 'id="fcv-width"' in html, repr(wd))
    return R


def _close(a, b, tol=1e-9):
    return len(a) == len(b) and all(abs(u - v) <= tol for u, v in zip(a, b))


def TPV_UNIT(s):
    return UNIT_RE.search(s) is not None


def section_modal(js):
    print('[M] 그림 창 (Force Chain View)')
    if not shutil.which('node'):
        chk('M0 node 필요', False, 'node 미설치')
        return
    body, miss = window_body(js)
    if not chk('M0 showForceChainView · 그림 창 공용 도우미 (figFrameGroup · figContextMeshes · figCapturePNG) 를 잘라 냈다', body is not None, f'없음 {miss}'):
        return
    rr = run_window(body)
    if not chk('M0b node 실행 (창 · 조작 · PNG 다섯)', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:900]):
        return
    for name, (ok, extra) in m_eval(rr).items():
        chk(name, ok, extra)


# ══════════════════════════════════════════════════════════════════════════════
#  [C] 범례 PNG · 범례 넣은 합성 (canvas 껍데기)
# ══════════════════════════════════════════════════════════════════════════════
C_SHIM = r"""
'use strict';
const LOG = { draws: [], rects: [], texts: [], canvases: [], downloads: [], strokes: [] };
function mkCtx() { return { font: '', fillStyle: '', strokeStyle: '', lineWidth: 1, textAlign: '', textBaseline: '', lineCap: '',
  drawImage(img, x, y) { LOG.draws.push([img.src, x, y]); }, fillRect(x, y, w, h) { LOG.rects.push([this.fillStyle, x, y, w, h]); },
  strokeRect() {}, fillText(t, x, y) { LOG.texts.push([String(t), this.font, this.fillStyle]); }, measureText(t) { const px = parseFloat(String(this.font).replace(/^[^0-9]*/, '')) || 10; return { width: String(t).length * px * 0.55 }; },
  beginPath() {}, moveTo() {}, lineTo() {}, stroke() { LOG.strokes.push([this.strokeStyle, this.lineWidth]); }, save() {}, restore() {}, translate() {}, rotate() {} }; }
const document = { createElement(tag) { if (tag === 'canvas') { const c = { width: 0, height: 0, _ctx: mkCtx(), getContext() { return this._ctx; },
                     toDataURL() { return 'data:image/png;base64,OUT:' + this.width + 'x' + this.height; } }; LOG.canvases.push(c); return c; }
                   return { tag, click() { LOG.downloads.push([this.download, this.href]); }, remove() {} }; },
                   body: { appendChild() {} } };
class Image { constructor() { this.width = 2800; this.height = 2000; this._src = ''; }
  set src(v) { this._src = v; setTimeout(() => this.onload && this.onload(), 0); } get src() { return this._src; } }
"""

C_RUN = r"""
(async () => {
  const OUT = { err: null };
  try {
    const sel = fcSelect(CH, 0), st = fcStats(sel.drawn);
    const OPT = { color: 'group', n: 0, show: { amam: true, amse: true, sese: true, other: true }, width: 1 };
    const spec = fcLegendSpec(st, sel, OPT);
    fcLegendPNG(spec, 'legend_force_chains.png');
    OUT.leg = { dl: LOG.downloads.slice(), texts: LOG.texts.map(t => t[0]), inks: [...new Set(LOG.texts.map(t => t[2]))], fills: [...new Set(LOG.rects.map(r => r[0]))],
                strokes: [...new Set(LOG.strokes.map(s => s[0]))], fonts: [...new Set(LOG.texts.map(t => t[1]))], canvas: LOG.canvases.map(c => [c.width, c.height]) };
    LOG.texts = []; LOG.rects = []; LOG.draws = []; LOG.strokes = [];
    const url = await fcCompositePNG('data:image/png;base64,SHOT', spec);
    const c = LOG.canvases[LOG.canvases.length - 1];
    OUT.comp = { url, w: c.width, h: c.height, draws: LOG.draws, texts: LOG.texts.map(t => t[0]), strokes: [...new Set(LOG.strokes.map(s => s[0]))],
                 fills: [...new Set(LOG.rects.map(r => r[0]))] };
    LOG.texts = []; LOG.rects = []; LOG.strokes = [];
    fcLegendPNG(fcLegendSpec(st, sel, Object.assign({}, OPT, { color: 'force' })), 'legend_force_chains.png');
    OUT.legForce = { texts: LOG.texts.map(t => t[0]), fills: LOG.rects.map(r => r[0]) };
  } catch (e) { OUT.err = String(e && e.stack || e); }
  console.log(JSON.stringify(OUT));
})();
"""


def section_draw(js):
    print('[C] 범례 PNG · 범례 넣은 합성')
    if not shutil.which('node'):
        chk('C0 node 필요', False, 'node 미설치')
        return
    src, miss = need(js, FC_FNS + FC_DRAW + TAU_HELP + ('fitTextLines',))
    cs, miss_c = consts(js)
    if not chk('C0 fcLegendPNG · fcCompositePNG · fcDrawLegend 를 잘라 냈다', not miss and not miss_c, f'없음 {miss + miss_c}'):
        return
    rr = run_node(C_SHIM + cs + '\n' + src + '\n' + TPV.js_const(js, 'TAUP_VIEW_DEF') + '\n' + data_js() + C_RUN)
    if not chk('C0b node 실행', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:600]):
        return
    lg = rr['leg']
    want_all = ref_select(CHAINS, 0)
    by_n = {k: sum(1 for c in want_all if GROUP_OF[c['type']] == k) for k in ('amam', 'amse', 'sese', 'other')}
    txt = ' | '.join(lg['texts'])
    swatch = {'#2a78d6', '#eb6834', '#1baf7a', '#898781'}
    chk('C1 범례 PNG = 흰 바탕 6× · 줄마다 견본 (묶음 색 선) · 이름 · 수 · 몫 (영문) · 글자 = 잉크 색 (묶음 색 글자 없음) · Arial · 파일 legend_force_chains.png',
        lg['dl'] and lg['dl'][-1][0] == 'legend_force_chains.png' and all(lab in txt for lab in ('AM–AM', 'AM–SE', 'SE–SE', 'Other'))
        and all(f'n = {by_n[k]}' in txt for k in by_n) and '% of summed force' in txt and swatch <= set(lg['strokes'])
        and not (set(lg['inks']) & swatch) and all('Arial' in f for f in lg['fonts']) and lg['canvas'][-1][0] >= 6 * 300, txt[:400])
    leaks = [s_ for s_ in FN_STRINGS if s_ in txt] + [m.group(0) for m in UNIT_RE.finditer(txt)]
    chk('C2 범례 PNG 에 fn 절대값 · 힘 단위가 없다 (relative only 문구는 있다)', not leaks and 'relative' in txt, repr(leaks))
    cp = rr['comp']
    chk('C3 범례 넣은 합성 = 찍은 그림 (2800×2000) 을 (0, 0) 에 그대로 + 오른쪽에 범례 (폭 > 2800 · 높이 같음 · 견본 넷 · 이름)',
        cp['draws'] == [['data:image/png;base64,SHOT', 0, 0]] and cp['w'] > 2800 and cp['h'] == 2000 and swatch <= set(cp['strokes'])
        and all(lab in ' '.join(cp['texts']) for lab in ('AM–AM', 'SE–SE')) and cp['url'] == f'data:image/png;base64,OUT:{cp["w"]}x{cp["h"]}',
        repr({k: cp[k] for k in ('w', 'h', 'draws')}))
    lf = rr['legForce']
    chk('C4 힘 색 모드 범례 PNG = 띠 (weak → strong · 관 색) · 줄 = 이름 · 수 · 몫 (견본 색 없음)',
        'weak' in ' '.join(lf['texts']) and 'strong' in ' '.join(lf['texts']) and len([f for f in lf['fills'] if f.startswith('#')]) > 50,
        repr(lf['texts'][:6]))


# ══════════════════════════════════════════════════════════════════════════════
#  [X] 변이 — 위 시험이 결함을 잡는가
# ══════════════════════════════════════════════════════════════════════════════
#  (이름, [(옛 글자, 새 글자)], 판정: 'pure' = F 절 다시 · 'win' = M 절 다시, FAIL 해야 할 시험 머리)
MUTANTS = [
    ('X1 굵기 = 옛 최소–최대 (5–95 백분위 대신)', [('const lo = fcPercentile(v, FC_DEF.pLo), hi = fcPercentile(v, FC_DEF.pHi);',
                                                'const lo = v[0], hi = v[v.length - 1];')], 'pure', ('F5 ', 'F5b ')),
    ('X2 기본 색 = 힘 (접촉 쌍 대신)', [("color: 'group', n: FC_DEF.nDefault", "color: 'force', n: FC_DEF.nDefault")], 'render', ('R2 ', 'R5 ')),
    ('X3 접기 생략 (p1 → p2 그대로 — 주기 접촉이 상자를 가로지른다)', [('const fp = tauPathsFoldPieces([[a, b]], cell);', 'const fp = { pieces: [[a, b0]], nCut: 0 };')],
     'pure', ('F7 ',)),
    ('X4 몫 정규화 빠짐 (fn 합 그대로)', [('share: tot > 0 ? 100 * g.sum / tot : 0', 'share: g.sum')], 'pure', ('F6 ', 'F6b ')),
    ('X5 범례에 fn 값 (가장 센 접촉의 fn)', [("'가장 센 ' + sel.drawn.length + ' 개'", "'가장 센 ' + sel.drawn.length + ' 개 (최대 fn ' + (sel.drawn.length ? sel.drawn[0].fn : 0) + ')'")],
     'pure', ('F9c ',)),
    ('X6 PNG 맞춤 끔', [('if (wantFit) {', 'if (false) {')], 'win', ('M6 ',)),
]


def mutate(src, pairs):
    for old, new in pairs:
        if old not in src:
            return None
        src = src.replace(old, new, 1)
    return src


def _pure_eval(js_mut, js):
    """변이 소스로 F 절을 다시 돌려 판정만 모은다 (chk 를 잠시 가로챈다)"""
    global _ok, _fail
    saved = (_ok, list(_fail))
    got = {}

    def grab(name, cond, extra=''):
        got[name.split(' ')[0]] = bool(cond)
        return bool(cond)
    g = globals()
    real = g['chk']
    g['chk'] = grab
    try:
        section_pure(js_mut)
    finally:
        g['chk'] = real
        _ok, _fail = saved[0], saved[1]
    return got


def _render_eval(js_mut):
    global _ok, _fail
    saved = (_ok, list(_fail))
    got = {}

    def grab(name, cond, extra=''):
        got[name.split(' ')[0]] = bool(cond)
        return bool(cond)
    g = globals()
    real = g['chk']
    g['chk'] = grab
    try:
        section_render(js_mut)
    finally:
        g['chk'] = real
        _ok, _fail = saved[0], saved[1]
    return got


def section_mutation(js):
    print('[X] 변이 — 시험의 판별력 (변이한 뷰어에서 해당 시험이 FAIL 해야 한다)')
    if not shutil.which('node'):
        chk('X0 node 필요', False, 'node 미설치')
        return
    body, miss = window_body(js)
    if not chk('X0 Force Chain 도우미가 있다 (변이 대상)', body is not None, f'없음 {miss}'):
        return
    for name, pairs, where, targets in MUTANTS:
        js_m = mutate(js, pairs)
        if js_m is None:
            chk(f'{name} → 변이 자리를 찾지 못했다 (코드가 바뀌었으면 변이도 고칠 것)', False, repr([p[0] for p in pairs]))
            continue
        if where == 'pure':
            got = _pure_eval(js_m, js)
        elif where == 'render':
            got = _render_eval(js_m)
        else:
            b2, _m = window_body(js_m)
            rr = run_window(b2) if b2 else None
            if rr is None or rr.get('err'):
                chk(f'{name} → 변이한 창이 멈추지 않고 돈다', False, repr(rr and rr.get('err'))[:300])
                continue
            got = {k.split(' ')[0]: ok for k, (ok, _x) in m_eval(rr).items()}
        hit = {t.strip(): got.get(t.strip()) for t in targets}
        chk(f'{name} → {" · ".join(hit)} 가 FAIL 한다 ({hit})', all(v is False for v in hit.values()), repr(got)[:300])


def section_registration():
    print('[REG] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    i_t, i_f = s.find('webapp/test_tau_paths_view.py'), s.find('webapp/test_force_chain_view.py')
    chk('REG scripts/check_all.sh 가 이 시험을 돈다 (tau_paths_view 바로 다음 줄)', 0 <= i_t < i_f and s[i_t:i_f].count('\n') == 1)


def main():
    js = open(VIEWER_JS, encoding='utf-8').read()
    section_ui(js)
    section_pure(js)
    section_render(js)
    section_modal(js)
    section_draw(js)
    section_mutation(js)
    section_registration()
    print()
    print(f'{_ok} PASS · {len(_fail)} FAIL')
    if _fail:
        print('FAIL — ' + ' | '.join(_fail))
        return 1
    print('ALL PASS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
