#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DEM 3D 뷰어 — Tortuosity 후보 경로 여럿 (View Mode `tau_paths`) + 그림 창 (All Paths View · PNG) (2026-10-07).

1저자 보고 그림 요청 (긴급) — 옛 판은 "Percolating Path" 체크박스 + < > 로 저장된 경로를 **하나씩**만 그렸다 ("Path Only View" 도 하나).
se_clusters.json 의 관통 클러스터마다 저장된 후보 경로 (최대 30 · 낮은 τ 10 · 평균 근처 10 · 높은 τ 10 — scripts/analyze_contacts.py)
를 3D 모델 안에 **한 번에** 그리고 (τ 색 · 가장 작은 τ = 금색 · 굵게 · SE 흐리게 · AM 흐리게) 슬라이드용 PNG 로 받는다.

  python3 webapp/test_tau_paths_view.py      # 종료코드 0 = PASS

[U] 조작판 배선 — DEM View Mode "Tortuosity 후보 경로 (여럿 · τ 색)" (MPM 엔 없음) · applyViewMode 의 걷기 · 분기 · "All Paths View" 단추 ·
    Percolating Path 조작 안 "▦ 이 클러스터의 모든 후보 경로" 단추.
[F] 순수 함수 (viewer3d.js 를 잘라 node 로) — 고르기 (범위 · τ 작은 N · 금색 = 가장 작은 τ) · 색 램프 (한 색상 · 밝음 → 어두움 = τ 작음 → 큼 ·
    단조) · 경로 조각 (주기 경계를 넘는 홉 = 양쪽 면에 반 토막 · 펼침 · 모르는 id 에서 끊음 — 파이썬 기준 구현과 좌표까지 같다) ·
    길이 ÷ Δz = 저장된 τ (범례가 말하는 정의가 참) · 컬러바 눈금 · 컬러바 스펙 (영문 · 수송 tortuosity 아님) · 범례 문구 · exportColorbarPNG 의 colorFn.
[R] 그리기 (THREE 껍데기) — 모든 경로의 관 (원기둥 수 = 그릴 홉 수) · 경로마다 τ 색 · 금색 경로 굵게 · 상자를 가로지르는 긴 관 없음 ·
    SE · AM 흐림 · 판 · 한 경로 관 숨김 · 걷기 되돌림 · 조작 (범위 · N · 불투명도는 다시 짓지 않음 · 굵기 · 끝점 · 컬러바 · 그림 창).
[M] 그림 창 (All Paths View) — 경로 관 · SE 맥락 · 정보 줄 · PNG 다운로드 (투명 · 4× · 파일 이름 · 컬러바 넣기 선택) · 컬러바 PNG.
[C] 컬러바 넣은 PNG 합성 (Image · canvas 껍데기) — 그림 옆 세로 막대 (위 = 큰 τ) · 눈금 · 제목.
[D] /3d-data 가 se_clusters.json 의 경로를 그대로 싣는다 (대조 — 옛 판도 통과 · 뷰어 입력이 있다는 확인).
⚠ node 가 없으면 건너뛰지 않고 FAIL 한다 (돌지 않는 검사는 없는 것과 같다 — 규칙 K).
"""
import json
import math
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIEWER_JS = os.path.join(HERE, 'static', 'js', 'viewer3d.js')
CHECK_ALL = os.path.join(ROOT, 'scripts', 'check_all.sh')

sys.path.insert(0, HERE)
from test_closed_param_labels import js_fn, js_const, run_node   # noqa: E402  (렌더된 JS 를 잘라 node 로 — 같은 도구)

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


def fns(src, names):
    out, miss = [], []
    for n in names:
        try:
            out.append(js_fn(src, n))
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


def consts(src, names):
    out, miss = [], []
    for n in names:
        try:
            out.append(js_const(src, n))
        except (ValueError, AssertionError):
            miss.append(n)
    return '\n'.join(out), miss


def line_consts(src, pattern):
    """한 줄 상수 (배열 · 문자열) — `^const TAUP_… = …;$`"""
    return re.findall(pattern, src, re.M)


# ══════════════════════════════════════════════════════════════════════════════
#  합성 침대 — 상자 x · y [0, 20) µm (주기) · z [0, 10] · SE 중심 (µm)
# ══════════════════════════════════════════════════════════════════════════════
BOX = {'x_min': 0, 'x_max': 20, 'y_min': 0, 'y_max': 20, 'z_min': 0, 'z_max': 10}
P = {1: (5, 5, 0.5), 2: (5.5, 5, 4), 3: (6, 5, 9.5), 4: (4, 5, 3), 5: (4.5, 6, 6),
     6: (19.6, 10, 0.6), 7: (0.4, 10, 3.0), 8: (1.0, 10.5, 6.0), 9: (1.2, 10.2, 9.4),          # x 주기 경계를 넘는 홉 6 → 7
     10: (19.7, 19.6, 0.7), 11: (0.3, 0.5, 2.5), 12: (0.8, 1.0, 5.0), 13: (1.1, 1.3, 9.3),     # 모서리 (x · y) 를 넘는 홉 10 → 11
     14: (15, 15, 0.5), 15: (15, 15.5, 5), 16: (15, 16.5, 9.5), 17: (16, 15, 3), 18: (16.5, 16, 7),
     19: (1, 1, 5), 20: (1.5, 1, 5.5)}


def ref_tau(ids, L=20.0):
    """analyze_contacts.py 와 같은 식 — 홉마다 dx = min(|Δx|, L − |Δx|) (y 같음) · τ = Σ 홉 길이 / |z_끝 − z_처음| (소수 둘째 자리)"""
    s = 0.0
    for a, b in zip(ids, ids[1:]):
        dx = abs(P[a][0] - P[b][0]); dy = abs(P[a][1] - P[b][1]); dz = P[a][2] - P[b][2]
        dx = min(dx, L - dx); dy = min(dy, L - dy)
        s += math.sqrt(dx * dx + dy * dy + dz * dz)
    zd = abs(P[ids[-1]][2] - P[ids[0]][2])
    return round(s / zd, 2), round(s, 1), round(zd, 1)


def mk_path(ids, cat):
    t, pl, zd = ref_tau(ids)
    return {'ids': ids, 'tortuosity': t, 'path_length': pl, 'z_distance': zd, 'category': cat}


PATHS0 = [mk_path([1, 2, 3], 'best'), mk_path([1, 4, 5, 3], 'mean'), mk_path([6, 7, 8, 9], 'mean'),
          mk_path([10, 11, 12, 13], 'worst')]
PATHS2 = [mk_path([14, 15, 16], 'best'), mk_path([14, 17, 18, 16], 'worst')]
CLUSTERS = [
    {'ids': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 'size': 13, 'percolating': True, 'path': PATHS0[0], 'paths': PATHS0},
    {'ids': [19, 20], 'size': 2, 'percolating': False, 'path': None},
    {'ids': [14, 15, 16, 17, 18], 'size': 5, 'percolating': True, 'path': PATHS2[0], 'paths': PATHS2},
]
PARTICLES = [{'id': i, 'type': 'SE', 'x': x, 'y': y, 'z': z, 'r': 0.5} for i, (x, y, z) in P.items()]
PARTICLES += [{'id': 101, 'type': 'AM_P', 'x': 10, 'y': 10, 'z': 5, 'r': 3}, {'id': 102, 'type': 'AM_S', 'x': 3, 'y': 15, 'z': 2, 'r': 1}]


def ref_pieces(ids, unwrap=False, L=(20.0, 20.0), idx=None):
    """기준 구현 (파이썬) — 홉 = 최소상 변위 (x · y 주기).  unwrap False: 넘는 홉은 a → a + d/2 · b − d/2 → b 두 조각 ·
    True: 첫 자리에서 변위를 이어 붙인 한 조각 · 모르는 id 에서 끊는다 (점 하나뿐인 조각은 버림)."""
    idx = P if idx is None else idx
    pieces, cur, prev_raw, prev_draw = [], None, None, None
    n_wrap = n_miss = 0
    for i in ids:
        if i not in idx:
            n_miss += 1
            if cur and len(cur) >= 2:
                pieces.append(cur)
            cur = prev_raw = prev_draw = None
            continue
        x, y, z = idx[i]
        if prev_raw is None:
            cur = [[x, y, z]]
            prev_raw, prev_draw = (x, y, z), [x, y, z]
            continue
        dxr, dyr = x - prev_raw[0], y - prev_raw[1]
        dx = dxr - L[0] * round(dxr / L[0])
        dy = dyr - L[1] * round(dyr / L[1])
        d = (dx, dy, z - prev_raw[2])
        wrapped = abs(dx - dxr) > 1e-9 or abs(dy - dyr) > 1e-9
        if unwrap:
            q = [prev_draw[0] + d[0], prev_draw[1] + d[1], prev_draw[2] + d[2]]
            cur.append(q)
            prev_draw = q
            n_wrap += wrapped
        elif wrapped:
            n_wrap += 1
            cur.append([prev_raw[0] + d[0] / 2, prev_raw[1] + d[1] / 2, prev_raw[2] + d[2] / 2])
            pieces.append(cur)
            cur = [[x - d[0] / 2, y - d[1] / 2, z - d[2] / 2], [x, y, z]]
            prev_draw = [x, y, z]
        else:
            cur.append([x, y, z])
            prev_draw = [x, y, z]
        prev_raw = (x, y, z)
    if cur and len(cur) >= 2:
        pieces.append(cur)
    return pieces, n_wrap, n_miss


def close_pieces(a, b, tol=1e-9):
    if len(a) != len(b):
        return False
    for pa, pb in zip(a, b):
        if len(pa) != len(pb):
            return False
        for qa, qb in zip(pa, pb):
            if any(abs(u - v) > tol for u, v in zip(qa, qb)):
                return False
    return True


def lum(h):
    """상대 휘도 (sRGB → 선형)"""
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (h >> 16) & 255, (h >> 8) & 255, h & 255
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


# ══════════════════════════════════════════════════════════════════════════════
#  [U] 조작판 배선
# ══════════════════════════════════════════════════════════════════════════════
def section_ui(js):
    print('[U] 조작판 배선')
    try:
        bc = js_fn(js, 'buildControls')
    except (ValueError, AssertionError):
        bc = ''
    sels = re.findall(r'<select id="view-mode".*?</select>', bc, re.S)
    mpm_sel, dem_sel = (sels + ['', ''])[:2]
    m = re.search(r'<option value="tau_paths">([^<]*)</option>', dem_sel)
    chk(f'U1 DEM View Mode 에 "Tortuosity 후보 경로 (여럿 …)" (value tau_paths) · MPM 엔 없음 ({m.group(1) if m else None})',
        len(sels) == 2 and m is not None and 'Tortuosity 후보 경로' in m.group(1) and '여럿' in m.group(1) and 'tau_paths' not in mpm_sel)
    try:
        av = js_fn(js, 'applyViewMode')
    except (ValueError, AssertionError):
        av = ''
    i_def = av.find("if (!mode || mode === 'default')")
    i_td = av.find('_teardownTauPaths(state)')
    chk('U2 모드를 바꾸면 후보 경로 관을 걷는다 (applyViewMode 앞머리 · default 분기보다 먼저 _teardownTauPaths)',
        0 <= i_td < i_def, f'teardown @{i_td} · default @{i_def}')
    chk("U2b applyViewMode 의 tau_paths 분기가 renderTauPaths 를 부른다",
        re.search(r"if \(mode === 'tau_paths'\) \{\s*renderTauPaths\(state\);\s*return;\s*\}", av) is not None)
    dem_part = bc[bc.find('Mesh (plate)'):] if 'Mesh (plate)' in bc else ''
    chk('U3 DEM 조작판에 "All Paths View" 단추 (data-action tauPathsView · Path Only View 옆)',
        re.search(r'<button data-action="tauPathsView"[^>]*>All Paths View</button>', dem_part) is not None
        and dem_part.find('data-action="pathOnly"') < dem_part.find('data-action="tauPathsView"'))
    try:
        wc = js_fn(js, 'wireControls')
    except (ValueError, AssertionError):
        wc = ''
    chk("U3b wireControls — action 'tauPathsView' → showTauPathsView(state)",
        re.search(r"action === 'tauPathsView'\)\s*\{\s*showTauPathsView\(state\);", wc) is not None)
    i_pc, i_fc = bc.find('id="path-controls"'), bc.find('id="force-chain-toggle"')
    pc = bc[i_pc:i_fc] if 0 <= i_pc < i_fc else ''
    chk('U4 Percolating Path 조작 (path-controls · Force Chain 앞) 안에 "모든 후보 경로" 단추 (id path-all)',
        re.search(r'<button id="path-all"[^>]*>[^<]*모든 후보 경로[^<]*</button>', pc) is not None)
    try:
        ie = js_fn(js, 'initElectrodeViewer')
    except (ValueError, AssertionError):
        ie = ''
    chk("U4b 그 단추 = tauPathsShowCluster(state, state.currentClusterIdx) (화면에서 고른 클러스터)",
        "querySelector('#path-all')" in ie
        and re.search(r'tauPathsShowCluster\(state,\s*state\.currentClusterIdx\)', ie) is not None)


# ══════════════════════════════════════════════════════════════════════════════
#  [F] 순수 함수
# ══════════════════════════════════════════════════════════════════════════════
PURE_FNS = ('tauPathsCollect', 'tauPathT', 'tauPathColor', 'tauPathPieces', 'tauPathsTicks', 'tauPathsColorbarSpec',
            'tauPathsLegendHtml', 'tauPathsPngName')
LINE_CONST_RE = r'^const TAUP_(?:RAMP|TOPS|DEF_TXT|SAMPLE_TXT) = [^\n]*;$'

F_RUN = r"""
const OUT = {};
const idIndex = {}; PARTS.forEach(p => { idIndex[p.id] = p; });
OUT.ramp = TAUP_RAMP.slice();
OUT.tops = TAUP_TOPS.slice();
const sig = c => ({ n: c.paths.length, taus: c.paths.map(p => p.tau), cis: c.paths.map(p => p.ci), pis: c.paths.map(p => p.pi),
                    lo: c.lo, hi: c.hi, best: c.best ? [c.best.ci, c.best.pi, c.best.tau] : null, nAvail: c.nAvail,
                    nClusters: c.nClusters, nSkipped: c.nSkipped, perc: (c.percClusters || []).map(q => [q.ci, q.size, q.n]) });
OUT.colAll = sig(tauPathsCollect(CL, { scope: 'all', top: 0 }));
OUT.colDef = sig(tauPathsCollect(CL, {}));
OUT.col2 = sig(tauPathsCollect(CL, { scope: '2', top: 0 }));
OUT.colTop3 = sig(tauPathsCollect(CL, { scope: 'all', top: 3 }));
OUT.colBad = sig(tauPathsCollect(CL, { scope: '1', top: 0 }));
OUT.colNone = sig(tauPathsCollect([], { scope: 'all' }));
{ const cl = JSON.parse(JSON.stringify(CL));
  cl[0].paths.push({ ids: [1], tortuosity: 1.0 }, { ids: [1, 2], tortuosity: 'x' }, { ids: null, tortuosity: 1.2 });
  OUT.colSkip = sig(tauPathsCollect(cl, { scope: 'all' })); }
{ const cl = [{ ids: [1, 2, 3], size: 3, percolating: true, path: CL[0].paths[0] }];      // 옛 형식 — paths 없이 path 하나
  OUT.colLegacy = sig(tauPathsCollect(cl, { scope: 'all' })); }
{ const cl = JSON.parse(JSON.stringify(CL)); cl[2].paths[0].tortuosity = CL[0].paths[0].tortuosity;   // 동률 — 먼저 나온 것
  OUT.colTie = sig(tauPathsCollect(cl, { scope: 'all' })); }
OUT.T = [tauPathT(1, 1, 2), tauPathT(2, 1, 2), tauPathT(1.5, 1, 2), tauPathT(0, 1, 2), tauPathT(9, 1, 2), tauPathT(1.3, 1.3, 1.3)];
OUT.cols = Array.from({ length: 21 }, (_, i) => tauPathColor(i / 20));
OUT.colEnds = [tauPathColor(-1), tauPathColor(2), tauPathColor(NaN)];
OUT.pieces = {};
for (const [k, ids] of Object.entries(PIDS)) {
  for (const uw of [false, true]) {
    const r = tauPathPieces(ids, idIndex, BOX, uw);
    OUT.pieces[k + (uw ? '_u' : '')] = { pieces: r.pieces, nWrap: r.nWrap, nMissing: r.nMissing, nHops: r.nHops, L: r.lengthUm, dz: r.dzUm };
  }
}
OUT.ticks = [[1.35, 2.08], [1.0, 1.1], [1.2, 4.0], [1.01, 1.02], [1.5, 1.5], [1.05, 3.97]].map(([a, b]) => tauPathsTicks(a, b));
const colA = tauPathsCollect(CL, { scope: 'all', top: 0 });
OUT.spec = (() => { const s = tauPathsColorbarSpec(colA); return { title: s.title, sub: s.sub, short: s.short, ticks: s.ticks,
  fn: [0, 0.5, 1].map(t => s.colorFn ? s.colorFn(t) : null), same: [0, 0.37, 1].every(t => s.colorFn && s.colorFn(t) === tauPathColor(t)) }; })();
OUT.leg = tauPathsLegendHtml(colA, { nSeg: 18, nWrap: 2, nMissing: 0 }, { scope: 'all', top: 0, seOpacity: 0.08, amOpacity: 0.12, width: 1, ends: false });
OUT.legMiss = tauPathsLegendHtml(colA, { nSeg: 18, nWrap: 0, nMissing: 3 }, { scope: 'all', top: 0 });
OUT.legNone = tauPathsLegendHtml(tauPathsCollect([], {}), null, { scope: 'all', top: 0 });
OUT.png = [tauPathsPngName(colA), tauPathsPngName(tauPathsCollect(CL, { scope: '2' }))];
console.log(JSON.stringify(OUT));
"""

# exportColorbarPNG — 캔버스 껍데기로 막대 칸의 색을 적는다
CB_SHIM = r"""
'use strict';
const CB = { rects: [], texts: [], downloads: [] };
function mkCtx() { return { font: '', fillStyle: '', strokeStyle: '', lineWidth: 1, textAlign: '', textBaseline: '',
  fillRect(x, y, w, h) { CB.rects.push([this.fillStyle, x, y, w, h]); }, strokeRect() {}, fillText(t) { CB.texts.push(String(t)); },
  measureText(t) { const px = parseFloat(String(this.font).replace(/^[^0-9]*/, '')) || 10; return { width: String(t).length * px * 0.5 }; },
  beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, save() {}, restore() {}, translate() {}, rotate() {}, drawImage() {} }; }
const document = { createElement(tag) { if (tag === 'canvas') { const c = { width: 0, height: 0, _ctx: mkCtx(),
                     getContext() { return this._ctx; }, toDataURL() { return 'data:image/png;base64,QQ=='; } }; return c; }
                   return { tag, click() { CB.downloads.push(this.download); }, remove() {} }; },
                   body: { appendChild() {} } };
"""

CB_RUN = r"""
const OUT = {};
const bars = () => CB.rects.filter(r => r[3] === 1.5);
CB.rects = [];
exportColorbarPNG({ colorFn: tauPathColor, title: 'Geometric tortuosity τ', ticks: [{ p: 0, label: '1.35' }, { p: 1, label: '2.08' }] }, 'colorbar_tau_paths.png');
{ const b = bars(); OUT.tau = { n: b.length, first: b.length ? b[0][0] : null, last: b.length ? b[b.length - 1][0] : null,
        want: ['#' + tauPathColor(0).toString(16).padStart(6, '0'), '#' + tauPathColor(1).toString(16).padStart(6, '0')],
        dl: CB.downloads.slice(-1)[0], texts: CB.texts.slice() }; }
CB.rects = []; CB.texts = [];
exportColorbarPNG({ map: 'jet', gamma: 1.6, title: 'x', left: '0', right: 'high' }, 'colorbar_jet.png');
{ const b = bars(); OUT.jet = { first: b.length ? b[0][0] : null, last: b.length ? b[b.length - 1][0] : null,
        want: ['#' + jetColor(0).toString(16).padStart(6, '0'), '#' + jetColor(1).toString(16).padStart(6, '0')] }; }
console.log(JSON.stringify(OUT));
"""


def section_pure(js):
    print('[F] 순수 함수 (node)')
    if not shutil.which('node'):
        chk('F0 node 필요 (뷰어 함수를 실제로 돌린다)', False, 'node 미설치')
        return
    src, miss = fns(js, PURE_FNS)
    lc = line_consts(js, LINE_CONST_RE)
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    if not chk('F0 viewer3d.js 에서 ' + ' · '.join(PURE_FNS) + ' · TAUP_RAMP · TAUP_TOPS · TAUP_DEF_TXT · TAUP_SAMPLE_TXT 를 잘라 냈다',
               not miss and not miss_c and len(lc) == 4, f'없음 {miss + miss_c} · 한 줄 상수 {len(lc)}'):
        return
    pids = {'straight': [1, 2, 3], 'xwrap': [6, 7, 8, 9], 'corner': [10, 11, 12, 13], 'missing': [1, 2, 999, 4, 5, 3],
            'missEnd': [1, 2, 999], 'single': [1]}
    script = ('"use strict";\n' + cs + '\n' + '\n'.join(lc) + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
              + ';\nconst PARTS = ' + json.dumps(PARTICLES) + ';\nconst BOX = ' + json.dumps(BOX)
              + ';\nconst PIDS = ' + json.dumps(pids) + ';\n' + F_RUN)
    res = run_node(script)
    if not chk('F0b node 실행', res is not None):
        return

    # ── 고르기 ──
    taus0 = [p['tortuosity'] for p in PATHS0]
    taus2 = [p['tortuosity'] for p in PATHS2]
    all_t = sorted(taus0 + taus2)
    ca = res['colAll']
    chk(f'F1 범위 "모든 관통 클러스터" = 관통 클러스터 두 개 (0 · 2) 의 저장 경로 전부 {len(all_t)} 개 · τ 오름차순 · 비관통 (1) 은 없다',
        ca['n'] == 6 and ca['taus'] == all_t and set(ca['cis']) == {0, 2} and ca['nClusters'] == 2 and ca['nAvail'] == 6, repr(ca))
    chk(f'F1b τ 범위 = 고른 경로의 최소 · 최대 ({ca["lo"]} – {ca["hi"]}) · 금색 = 가장 작은 τ (클러스터 0 · 경로 0 · τ {taus0[0]})',
        ca['lo'] == min(all_t) and ca['hi'] == max(all_t) and ca['best'] == [0, 0, taus0[0]], repr(ca))
    chk('F1c 범위 목록 = 관통 클러스터마다 (번호 · SE 수 · 저장 경로 수) — 고르기 단추에 쓴다',
        ca['perc'] == [[0, 13, 4], [2, 5, 2]], repr(ca['perc']))
    chk('F1d 옵션 없음 = 모든 관통 클러스터 · 경로 전부 (기본)', res['colDef']['taus'] == all_t, repr(res['colDef']))
    c2 = res['col2']
    chk(f'F2 범위 "클러스터 #2" = 그 클러스터 경로 {len(taus2)} 개 · 금색 = 그 안의 가장 작은 τ',
        c2['n'] == 2 and set(c2['cis']) == {2} and c2['taus'] == sorted(taus2) and c2['best'] == [2, 0, taus2[0]]
        and c2['perc'] == [[0, 13, 4], [2, 5, 2]], repr(c2))
    t3 = res['colTop3']
    chk(f'F3 τ 작은 3 개 = 전체에서 τ 가장 작은 셋 ({t3["taus"]} = {all_t[:3]})', t3['taus'] == all_t[:3] and t3['n'] == 3
        and t3['nAvail'] == 6, repr(t3))
    chk('F3b 비관통 클러스터를 고르면 0 개 · 범위 없음 (null) · 고를 수 있는 관통 클러스터 목록은 그대로',
        res['colBad']['n'] == 0 and res['colBad']['lo'] is None and res['colBad']['best'] is None and len(res['colBad']['perc']) == 2,
        repr(res['colBad']))
    chk('F3c 클러스터가 없으면 0 개', res['colNone']['n'] == 0 and res['colNone']['perc'] == [], repr(res['colNone']))
    chk('F3d 쓸 수 없는 경로 (id 하나 · τ 숫자 아님 · ids 없음) 는 빼고 센다 (nSkipped 3)',
        res['colSkip']['n'] == 6 and res['colSkip']['nSkipped'] == 3, repr(res['colSkip']))
    chk('F3e 옛 형식 (paths 없이 path 하나) 도 그 경로 하나로', res['colLegacy']['n'] == 1, repr(res['colLegacy']))
    chk('F3f τ 동률이면 먼저 나온 경로가 금색 (안정 정렬)', res['colTie']['best'][:2] == [0, 0], repr(res['colTie']))

    # ── 색 ──
    T = res['T']
    chk(f'F4 색 축 t = (τ − 최소)/(최대 − 최소) · [0, 1] 로 자른다 · 범위가 한 점이면 0.5 {T}',
        [round(x, 9) for x in T] == [0.0, 1.0, 0.5, 0.0, 1.0, 0.5])
    ramp = res['ramp']
    cols = res['cols']
    chk('F5 색 램프 = 한 색상 (파랑) 순차 · 끝 = 램프 끝 (밝음 #86b6ef → 어두움 #0d366b) · 기준 팔레트 단계 250…700',
        cols[0] == 0x86b6ef and cols[-1] == 0x0d366b and ramp[0] == 0x86b6ef and ramp[-1] == 0x0d366b and len(ramp) >= 6,
        f'{[hex(c) for c in (cols[0], cols[-1])]} · 램프 {len(ramp)}')
    lums = [lum(c) for c in cols]
    chk('F5b 휘도가 τ 를 따라 엄격히 줄어든다 (큰 τ = 더 어둡게 — 21 점)', all(b < a for a, b in zip(lums, lums[1:])),
        repr([round(x, 4) for x in lums]))
    chk('F5c 파랑 계열 — 모든 점에서 B > G > R (금색 강조와 섞이지 않는다)',
        all(((c & 255) > ((c >> 8) & 255) > ((c >> 16) & 255)) for c in cols), repr([hex(c) for c in cols[::5]]))
    chk('F5d 범위 밖 · NaN 은 끝 색 (밝은 끝 · 어두운 끝 · 밝은 끝)', res['colEnds'] == [0x86b6ef, 0x0d366b, 0x86b6ef], repr(res['colEnds']))

    # ── 경로 조각 ──
    pcs = res['pieces']
    for k, ids in pids.items():
        for uw in (False, True):
            key = k + ('_u' if uw else '')
            got = pcs[key]
            want, wwrap, wmiss = ref_pieces(ids, unwrap=uw)
            chk(f'F6 {key}: 조각 좌표 = 파이썬 기준 구현 ({len(want)} 조각 · 주기 넘음 {wwrap} · 모르는 id {wmiss})',
                close_pieces(got['pieces'], want) and got['nWrap'] == wwrap and got['nMissing'] == wmiss,
                f"{got['pieces']} vs {want} · wrap {got['nWrap']} · miss {got['nMissing']}")
    xw = pcs['xwrap']['pieces']
    chk('F6b 주기 경계를 넘는 홉 = 반 토막 둘 — 첫 조각은 x = 20 (상자 면) 에서 끝나고 다음 조각은 x = 0 에서 시작 (상자를 가로지르는 긴 관 없음)',
        len(xw) == 2 and abs(xw[0][-1][0] - 20.0) < 1e-9 and abs(xw[1][0][0] - 0.0) < 1e-9
        and all(abs(a[0] - b[0]) < 10 for pc in xw for a, b in zip(pc, pc[1:])), repr(xw))
    cu = pcs['corner_u']['pieces']
    chk('F6c 펼침 (unwrap) = 한 조각 · 홉이 이어진다 (x 19.7 → 20.3 · y 19.6 → 20.5)',
        len(cu) == 1 and abs(cu[0][1][0] - 20.3) < 1e-9 and abs(cu[0][1][1] - 20.5) < 1e-9, repr(cu))
    chk('F6d 모르는 id 에서 관을 끊는다 (이어 그리지 않는다) · 점 하나만 남은 조각은 버린다',
        len(pcs['missing']['pieces']) == 2 and pcs['missing']['nMissing'] == 1 and len(pcs['missEnd']['pieces']) == 1
        and pcs['single']['pieces'] == [], repr({k: pcs[k]['pieces'] for k in ('missing', 'missEnd', 'single')}))
    bad = []
    for p in PATHS0 + PATHS2:
        k = {(1, 2, 3): 'straight', (6, 7, 8, 9): 'xwrap', (10, 11, 12, 13): 'corner'}.get(tuple(p['ids']))
        if not k:
            continue
        g = pcs[k]
        if not (abs(g['L'] - p['path_length']) < 0.05 + 1e-9 and abs(g['dz'] - p['z_distance']) < 0.05 + 1e-9
                and round(g['L'] / g['dz'], 2) == p['tortuosity']):
            bad.append((k, g['L'], g['dz'], p))
    chk('F7 경로 길이 (최소상 홉 합) ÷ 양 끝 z 거리 = 저장된 τ (analyze_contacts.py 의 식) — 범례 · 컬러바가 말하는 정의가 참',
        not bad, repr(bad))
    chk('F7b 펼침 · 반 토막 어느 쪽이든 길이 · 홉 수는 같다 (그림만 다르다)',
        all(abs(pcs[k]['L'] - pcs[k + '_u']['L']) < 1e-9 and pcs[k]['nHops'] == pcs[k + '_u']['nHops']
            for k in ('straight', 'xwrap', 'corner')))

    # ── 눈금 · 스펙 ──
    tk = res['ticks']
    ok_t, why = True, []
    for (lo, hi), t in zip([(1.35, 2.08), (1.0, 1.1), (1.2, 4.0), (1.01, 1.02), (1.5, 1.5), (1.05, 3.97)], tk):
        labs = [x['label'] for x in t]
        ps = [x['p'] for x in t]
        if lo == hi:
            ok_t &= len(t) == 1 and labs == ['1.50']
            continue
        cond = (labs[0] == f'{lo:.2f}' and labs[-1] == f'{hi:.2f}' and 2 <= len(t) <= 5 and ps[0] == 0 and ps[-1] == 1
                and all(b - a >= 0.15 - 1e-12 for a, b in zip(ps, ps[1:]))
                and all(not re.search(r'\.\d*0$', s) for s in labs[1:-1]))
        if not cond:
            why.append((lo, hi, labs, ps))
        ok_t &= cond
    chk('F8 컬러바 눈금 — 끝 = 실제 최소 · 최대 (소수 둘째) · 모두 5 개 이하 (7–8 개는 많다) · 서로 0.15 이상 · 안쪽은 1·2·5 간격 · 꼬리 0 없음',
        ok_t, repr(why or tk))
    chk(f'F8b real_14 범위 (1.35 – 2.08) 눈금 = {[x["label"] for x in tk[0]]}', [x['label'] for x in tk[0]] == ['1.35', '1.5', '2.08'])
    sp = res['spec']
    chk('F9 컬러바 스펙 — 색 함수 = 관 색 (tauPathColor) · 영문 제목 (Geometric tortuosity · path length / Δz) · 눈금',
        sp['same'] is True and 'Geometric tortuosity' in sp['title'] and 'path length / Δz' in sp['title']
        and sp['ticks'] and sp['ticks'][0]['label'] == f'{min(all_t):.2f}' and sp['ticks'][-1]['label'] == f'{max(all_t):.2f}',
        repr(sp)[:300])
    chk('F9b 컬러바 부제 — τ_Dij 와 같은 정의 · 수송 tortuosity 아님 · 경로 수 · 금색 = 가장 작은 τ (그림 캡션 오기 방지)',
        'τ_Dij' in sp['sub'] and 'not the transport tortuosity' in sp['sub'] and '6 stored candidate paths' in sp['sub']
        and 'gold = lowest τ' in sp['sub'] and sp['short'] and 'Δz' in sp['short'], sp['sub'])

    # ── 범례 ──
    leg = res['leg']
    plain = re.sub(r'<[^>]+>', '', leg)
    chk('F10 범례 — τ 정의 한 줄 (SE 중심 길이 ÷ 양 끝 z 거리 · 표의 τ_Dij 와 같은 정의 · 수송 tortuosity 아님 · tortuosity_SE_wall 과 다름)',
        all(w in plain for w in ('양 끝 z 거리', '표의 τ_Dij 와 같은 정의', '수송 tortuosity 아님', 'tortuosity_SE_wall')), plain[:500])
    chk('F10b 범례 — 표본이라는 것 (클러스터마다 최대 30 · 낮은 τ 10 · 평균 근처 10 · 높은 τ 10 · τ 분포의 대표 표본 아님)',
        all(w in plain for w in ('최대 30', '낮은 τ 10', '평균 근처 10', '높은 τ 10', '대표 표본이 아니다')), plain[:700])
    chk(f'F10c 범례 — 경로 수 · 클러스터 수 · τ 범위 ({min(all_t):.2f} – {max(all_t):.2f}) · 금색 = 가장 작은 τ',
        '경로 6 개' in plain and '관통 클러스터 2 개' in plain and f'τ {min(all_t):.2f} – {max(all_t):.2f}' in plain
        and '금색' in plain and '가장 작은 τ' in plain, plain[:500])
    chk('F10d 범례 컬러바 = 같은 램프의 CSS 그라디언트 (밝음 → 어두움)',
        'linear-gradient' in leg and '#86b6ef' in leg and '#0d366b' in leg)
    chk('F10e 범례 — 주기 경계를 넘는 홉 수 (반 토막) · 모르는 id 경고 (있을 때만)',
        '주기 경계를 넘는 홉 2 개' in plain and '반 토막' in plain and '⚠' not in plain
        and '모르는 id 3 개' in re.sub(r'<[^>]+>', '', res['legMiss']))
    ids_need = ('taup-scope', 'taup-top', 'taup-se-op', 'taup-am-op', 'taup-width', 'taup-ends', 'taup-cbar', 'taup-modal')
    chk('F10f 범례 조작 — 범위 · τ 작은 N · SE 불투명도 · AM 불투명도 · 관 굵기 · 끝점 · 컬러바 ⬇ · 그림 창',
        all(f'id="{i}"' in leg for i in ids_need), repr([i for i in ids_need if f'id="{i}"' not in leg]))
    chk('F10g 범위 고르기 = 모든 관통 클러스터 + 클러스터마다 (번호 · SE 수 · 경로 수)',
        re.search(r'<option value="all" selected>모든 관통 클러스터</option>', leg) is not None
        and '클러스터 #0 (13 SE · 4 경로)' in leg and '클러스터 #2 (5 SE · 2 경로)' in leg)
    chk('F10h N 고르기 = 경로 전부 · τ 작은 5 · 10 · 20', res['tops'] == [0, 5, 10, 20]
        and all(f'τ 작은 {n} 개' in leg for n in (5, 10, 20)) and '경로 전부' in leg)
    chk('F10i 범례 — Screenshot 에는 범례 · 컬러바가 안 들어간다 · 컬러바는 따로 · 그림 창 PNG',
        'Screenshot' in plain and '컬러바 ⬇' in plain and '그림 창' in plain)
    chk('F10j 경로가 없으면 그렇다고 말한다 (관통 클러스터 · se_clusters.json 경로 없음)',
        '저장된 후보 경로 없음' in re.sub(r'<[^>]+>', '', res['legNone']))
    chk(f'F11 PNG 파일 이름 = tau_paths_n<경로 수>_tau<최소>-<최대>.png ({res["png"]})',
        res['png'] == [f'tau_paths_n6_tau{min(all_t):.2f}-{max(all_t):.2f}.png',
                       f'tau_paths_n2_tau{min(taus2):.2f}-{max(taus2):.2f}.png'])

    # ── exportColorbarPNG 의 colorFn ──
    src_cb, miss_cb = fns(js, ('exportColorbarPNG', 'fitTextLines', 'jetColor', 'coolwarmColor', 'tauPathColor'))
    if not chk('F12 exportColorbarPNG · fitTextLines · jetColor · coolwarmColor 를 잘라 냈다', not miss_cb, repr(miss_cb)):
        return
    lc_ramp = line_consts(js, r'^const TAUP_RAMP = [^\n]*;$')
    cb = run_node(CB_SHIM + '\n'.join(lc_ramp) + '\n' + src_cb + '\n' + CB_RUN)
    if not chk('F12b node 실행 (exportColorbarPNG)', cb is not None):
        return
    t = cb['tau']
    chk(f'F12c 컬러바 PNG — spec.colorFn 이 있으면 그 색으로 막대를 칠한다 (첫 칸 {t["first"]} · 끝 칸 {t["last"]} = {t["want"]}) · 파일 이름',
        t['n'] > 100 and [t['first'], t['last']] == t['want'] and t['dl'] == 'colorbar_tau_paths.png', repr(t)[:300])
    j = cb['jet']
    chk('F12d 대조 — colorFn 없는 옛 스펙 (jet) 은 그대로 jet 색', [j['first'], j['last']] == j['want'], repr(j))


# ══════════════════════════════════════════════════════════════════════════════
#  [R] 그리기 (THREE 껍데기)
# ══════════════════════════════════════════════════════════════════════════════
R_SHIM = r"""
'use strict';
const LOG = { legends: [], cbar: [], modal: 0, clip: 0, dispatched: [], applied: [] };
class V3 { constructor(x = 0, y = 0, z = 0) { this.x = x; this.y = y; this.z = z; }
  set(x, y, z) { this.x = x; this.y = y; this.z = z; return this; } copy(v) { this.x = v.x; this.y = v.y; this.z = v.z; return this; }
  clone() { return new V3(this.x, this.y, this.z); } subVectors(a, b) { this.x = a.x - b.x; this.y = a.y - b.y; this.z = a.z - b.z; return this; }
  addVectors(a, b) { this.x = a.x + b.x; this.y = a.y + b.y; this.z = a.z + b.z; return this; }
  sub(v) { this.x -= v.x; this.y -= v.y; this.z -= v.z; return this; } add(v) { this.x += v.x; this.y += v.y; this.z += v.z; return this; }
  multiplyScalar(s) { this.x *= s; this.y *= s; this.z *= s; return this; } divideScalar(s) { this.x /= s; this.y /= s; this.z /= s; return this; }
  length() { return Math.hypot(this.x, this.y, this.z); } normalize() { const l = this.length() || 1; return this.divideScalar(l); }
  addScaledVector(v, s) { this.x += v.x * s; this.y += v.y * s; this.z += v.z * s; return this; }
  distanceTo(v) { return Math.hypot(this.x - v.x, this.y - v.y, this.z - v.z); } }
class Q { constructor() { this.b = null; } setFromUnitVectors(a, b) { this.b = [b.x, b.y, b.z]; return this; } }
class M4 { compose(p, q, s) { this.p = [p.x, p.y, p.z]; this.q = q && q.b ? q.b.slice() : null; this.s = [s.x, s.y, s.z]; return this; } }
class Color { constructor(v) { this.v = v; } setHex(h) { this.v = h; return this; } getHex() { return this.v; } }
class Mat { constructor(o) { Object.assign(this, o || {}); this.userData = {}; } dispose() { this.disposed = true; } }
class Geo { constructor(...a) { this.args = a; } dispose() { this.disposed = true; } }
class InstancedMesh { constructor(g, m, n) { this.geometry = g; this.material = m; this.count = n; this.isInstancedMesh = true;
    this.mats = new Array(n); this.cols = new Array(n); this.instanceMatrix = { needsUpdate: false }; this.instanceColor = null;
    this.userData = {}; this.visible = true; }
  setMatrixAt(i, m) { this.mats[i] = { p: m.p.slice(), q: m.q ? m.q.slice() : null, s: m.s.slice() }; }
  setColorAt(i, c) { if (!this.instanceColor) this.instanceColor = { needsUpdate: false }; this.cols[i] = c.v; }
  dispose() { this.disposed = true; } }
class Group { constructor() { this.children = []; this.userData = {}; this.visible = true; }
  add(o) { this.children.push(o); return this; } remove(o) { this.children = this.children.filter(c => c !== o); }
  traverse(f) { f(this); this.children.forEach(c => (c.traverse ? c.traverse(f) : f(c))); } }
const THREE = { Vector3: V3, Quaternion: Q, Matrix4: M4, Color, InstancedMesh, Group,
  CylinderGeometry: Geo, SphereGeometry: Geo, MeshPhongMaterial: Mat, MeshLambertMaterial: Mat, MeshBasicMaterial: Mat,
  FrontSide: 0, DoubleSide: 2 };
class Event { constructor(t) { this.type = t; } }
let ELS = {};
function mkEl(id) { return { id, value: '', checked: false, textContent: '', innerHTML: '', style: {}, ls: [],
  addEventListener(type, fn) { this.ls.push([type, fn]); }, dispatchEvent(ev) { LOG.dispatched.push([this.id, ev.type, this.value]); } }; }
const document = { getElementById(id) { return ELS[id] || (ELS[id] = mkEl(id)); }, querySelector() { return null; } };
function fire(id, type) { (ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).forEach(l => l[1]({ type, target: ELS[id] })); }
function nListen(id, type) { return (ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).length; }
//  범례를 새로 쓰면 그 안의 요소는 새 요소다 (옛 듣개가 남지 않는다 — 실제 DOM 처럼)
function setLegend(state, html) { LOG.legends.push(html); (html.match(/id="([^"]+)"/g) || []).forEach(m => { delete ELS[m.slice(4, -1)]; });
  (html.match(/<(?:select|input)[^>]*id="([^"]+)"[^>]*>/g) || []).forEach(tag => {
    const id = /id="([^"]+)"/.exec(tag)[1], v = /value="([^"]*)"/.exec(tag), el = document.getElementById(id);
    if (v) el.value = v[1]; el.checked = / checked/.test(tag); }); }
function exportColorbarPNG(spec, name) { LOG.cbar.push([spec && spec.title, name, spec && spec.ticks]); }
function showTauPathsView(state) { LOG.modal++; }
function applyViewMode(state, mode) { LOG.applied.push(mode); }
"""

R_RUN = r"""
const OUT = { err: null };
try {
  const idIndex = {}; PARTS.forEach(p => { idIndex[p.id] = p; });
  const se = PARTS.filter(p => p.type === 'SE'), amp = PARTS.filter(p => p.type === 'AM_P'), ams = PARTS.filter(p => p.type === 'AM_S');
  function pm(ps, base, opa, tr) { return { visible: true, userData: { particles: ps, baseColor: base }, recolored: 0,
    setColorAt() { this.recolored++; }, instanceColor: { needsUpdate: false },
    material: { opacity: opa, transparent: tr, depthWrite: !tr, userData: {}, needsUpdate: false } }; }
  const scene = new Group();
  const pathGroup = new Group();
  const state = { scene, data: { particles: PARTS, box: BOX, clusters: { clusters: CL } }, idIndex,
                  meshes: { AM_P: pm(amp, 0x222222, 1, false), AM_S: pm(ams, 0x888888, 1, false), SE: pm(se, 0xf5e6a3, 0.85, true),
                            MESH: { visible: true, material: { opacity: 0.55 } } },
                  pathGroup, applyClip() { LOG.clip++; }, viewMode: 'tau_paths' };
  const meshes = () => { const g = state.tauPathsGroup; const out = {}; if (!g) return out;
    g.traverse(o => { if (o.isInstancedMesh) (out[o.userData.kind] = out[o.userData.kind] || []).push(o); }); return out; };
  const summary = () => { const m = meshes(), one = k => (m[k] || [])[0] || null;
    const seg = one('seg'), segB = one('segBest'), jt = one('joint'), jtB = one('jointBest'), ends = one('ends');
    const perPath = {};
    if (seg) seg.instPath = seg.userData.instPath;
    [seg, segB].forEach(mm => { if (!mm) return; mm.userData.instPath.forEach((k, i) => {
      (perPath[k] = perPath[k] || { cols: new Set(), n: 0, r: new Set(), maxLen: 0 });
      perPath[k].cols.add(mm.cols[i]); perPath[k].n++; perPath[k].r.add(+mm.mats[i].s[0].toFixed(6));
      perPath[k].maxLen = Math.max(perPath[k].maxLen, mm.mats[i].s[1]); }); });
    const pp = {}; Object.keys(perPath).forEach(k => { pp[k] = { cols: [...perPath[k].cols], n: perPath[k].n, r: [...perPath[k].r], maxLen: perPath[k].maxLen }; });
    return { kinds: Object.keys(m).sort(), nSeg: seg ? seg.count : 0, nSegBest: segB ? segB.count : 0, nJoint: jt ? jt.count : 0,
             nJointBest: jtB ? jtB.count : 0, nEnds: ends ? ends.count : 0,
             endCols: ends ? [...new Set(ends.cols)] : [], perPath: pp,
             bestEmissive: segB ? segB.material.emissive : null, bestCols: segB ? [...new Set(segB.cols)] : [],
             frustum: Object.values(m).flat().every(o => o.frustumCulled === false),
             deco: Object.values(m).flat().some(o => o.userData.isDecoration),
             firstSeg: seg ? seg.mats[0] : null, inScene: scene.children.includes(state.tauPathsGroup),
             paths: state._tauPathsLast ? state._tauPathsLast.col.paths.map(p => [p.ci, p.pi, p.tau]) : null }; };
  const matOf = t => { const m = state.meshes[t]; return { opacity: m.material.opacity, transparent: m.material.transparent,
                                                         depthWrite: m.material.depthWrite, visible: m.visible, recolored: m.recolored }; };
  renderTauPaths(state);
  OUT.r1 = summary();
  OUT.r1.legend = LOG.legends[LOG.legends.length - 1] || '';
  OUT.r1.se = matOf('SE'); OUT.r1.am = matOf('AM_P'); OUT.r1.ams = matOf('AM_S');
  OUT.r1.plate = state.meshes.MESH.visible; OUT.r1.pathGroupVisible = pathGroup.visible; OUT.r1.clip = LOG.clip;
  OUT.r1.opt = Object.assign({}, state._tauPathsOpt);
  //  다시 그려도 묶음은 하나 · 옛 묶음 해제
  const g1 = state.tauPathsGroup;
  renderTauPaths(state);
  OUT.again = { nGroups: scene.children.filter(c => c.userData && c.userData.isTauPaths).length,
                oldDisposed: (() => { let d = true; g1.traverse(o => { if (o.isInstancedMesh && !o.disposed) d = false; }); return d; })() };
  //  조작 — 범위 · N
  ELS['taup-scope'].value = '2'; fire('taup-scope', 'change');
  OUT.scope2 = summary();
  ELS['taup-scope'].value = 'all'; fire('taup-scope', 'change');
  ELS['taup-top'].value = '3'; fire('taup-top', 'change');
  OUT.top3 = summary();
  ELS['taup-top'].value = '0'; fire('taup-top', 'change');
  //  불투명도 막대 — 관 묶음을 다시 짓지 않는다
  { const g0 = state.tauPathsGroup;
    ELS['taup-se-op'].value = '30'; fire('taup-se-op', 'input');
    ELS['taup-am-op'].value = '0'; fire('taup-am-op', 'input');
    OUT.opac = { same: state.tauPathsGroup === g0, se: matOf('SE'), am: matOf('AM_P'), seVal: (ELS['taup-se-op-val'] || {}).textContent };
    ELS['taup-am-op'].value = '12'; fire('taup-am-op', 'input'); ELS['taup-se-op'].value = '8'; fire('taup-se-op', 'input'); }
  //  굵기 · 끝점 — 관만 다시 짓고 범례는 다시 쓰지 않는다 (끄는 막대 요소가 바뀌면 손에서 빠진다)
  const nLeg0 = LOG.legends.length, wEl = ELS['taup-width'];
  ELS['taup-width'].value = '200'; fire('taup-width', 'input');
  OUT.wide = summary();
  OUT.wide.sameSlider = ELS['taup-width'] === wEl; OUT.wide.val = (ELS['taup-width-val'] || {}).textContent;
  ELS['taup-width'].value = '100'; fire('taup-width', 'input');
  ELS['taup-ends'].checked = true; fire('taup-ends', 'change');
  OUT.ends = summary();
  ELS['taup-ends'].checked = false; fire('taup-ends', 'change');
  OUT.wide.legendsDuring = LOG.legends.length - nLeg0;
  //  컬러바 · 그림 창
  fire('taup-cbar', 'click'); fire('taup-modal', 'click');
  OUT.cbar = LOG.cbar.slice(); OUT.modal = LOG.modal;
  OUT.listen = { scope: nListen('taup-scope', 'change'), top: nListen('taup-top', 'change') };
  //  AM 을 숨긴 채 (불투명도 0) 모드를 떠나도 걷기가 보임을 되돌린다
  ELS['taup-am-op'].value = '0'; fire('taup-am-op', 'input');
  OUT.amHiddenBeforeLeave = state.meshes.AM_P.visible;
  //  다른 모드로 — 사건이 그림을 만들지 않는다
  state.viewMode = 'default';
  ELS['taup-scope'].value = '2'; fire('taup-scope', 'change');
  OUT.otherModeGroup = !!state.tauPathsGroup && state.tauPathsGroup !== null;
  //  걷기
  _teardownTauPaths(state);
  OUT.td = { group: state.tauPathsGroup, inScene: scene.children.filter(c => c.userData && c.userData.isTauPaths).length,
             se: matOf('SE'), am: matOf('AM_P'), pathGroupVisible: pathGroup.visible };
  //  Percolating Path 의 "모든 후보 경로" 단추 — 화면의 클러스터 · View Mode 를 바꾼다
  ELS = {}; LOG.dispatched = [];
  const sel = document.getElementById('view-mode'); sel.value = 'default';
  tauPathsShowCluster(state, 2);
  OUT.show = { scope: state._tauPathsOpt.scope, top: state._tauPathsOpt.top, sel: sel.value, dispatched: LOG.dispatched.slice() };
  tauPathsShowCluster(state, null);
  OUT.showNull = { scope: state._tauPathsOpt.scope };
  //  없는 클러스터를 고른 채로 그리면 모든 관통 클러스터로 (빈 그림 대신)
  state.viewMode = 'tau_paths'; state._tauPathsOpt.scope = '7';
  renderTauPaths(state);
  OUT.badScope = { scope: state._tauPathsOpt.scope, n: summary().paths ? summary().paths.length : 0 };
  //  경로가 없는 케이스 — 관 없음 · 범례가 말한다
  const st2 = { scene: new Group(), data: { particles: PARTS, box: BOX, clusters: {} }, idIndex, meshes: {}, applyClip() {}, viewMode: 'tau_paths' };
  renderTauPaths(st2);
  OUT.none = { group: st2.tauPathsGroup || null, legend: LOG.legends[LOG.legends.length - 1] };
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
"""

RENDER_FNS = PURE_FNS + ('buildTauPathsGroup', 'tauPathsBaseRadius', 'tauPathsOpt', 'renderTauPaths', '_teardownTauPaths',
                         '_tauPathsFade', '_tauPathsWire', 'tauPathsShowCluster')


def section_render(js):
    print('[R] 그리기 (THREE 껍데기)')
    if not shutil.which('node'):
        chk('R0 node 필요', False, 'node 미설치')
        return
    src, miss = fns(js, RENDER_FNS)
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    lc = line_consts(js, LINE_CONST_RE)
    if not chk('R0 그리기 함수 (buildTauPathsGroup · renderTauPaths · _teardownTauPaths · _tauPathsFade · _tauPathsWire · '
               'tauPathsShowCluster) · TAUP_DEFAULT_OPT 를 잘라 냈다', not miss and not miss_c and len(lc) == 4,
               f'없음 {miss + miss_c}'):
        return
    rr = run_node(R_SHIM + cs + '\n' + '\n'.join(lc) + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
                  + ';\nconst PARTS = ' + json.dumps(PARTICLES) + ';\nconst BOX = ' + json.dumps(BOX) + ';\n' + R_RUN)
    if not chk('R0b node 실행 (renderTauPaths)', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:900]):
        return
    allp = sorted([(0, i, p['tortuosity']) for i, p in enumerate(PATHS0)] + [(2, i, p['tortuosity']) for i, p in enumerate(PATHS2)],
                  key=lambda x: x[2])
    # 기대 원기둥 수 = 홉마다 1 (주기 넘음 = 2) · 금색 = τ 가장 작은 경로
    def nseg(ids):
        pcs, _, _ = ref_pieces(ids)
        return sum(len(pc) - 1 for pc in pcs)

    def npts(ids):
        pcs, _, _ = ref_pieces(ids)
        return sum(len(pc) for pc in pcs)
    path_ids = {(0, i): p['ids'] for i, p in enumerate(PATHS0)}
    path_ids.update({(2, i): p['ids'] for i, p in enumerate(PATHS2)})
    best = allp[0]
    want_seg = sum(nseg(path_ids[(c, i)]) for c, i, _ in allp if (c, i) != best[:2])
    want_best = nseg(path_ids[best[:2]])
    r1 = rr['r1']
    chk(f'R1 모든 후보 경로 {len(allp)} 개를 한 번에 — 원기둥 = 그릴 홉 수 (보통 {want_seg} + 금색 {want_best} · 주기 넘음은 반 토막 둘)',
        r1['paths'] == [list(x) for x in allp] and r1['nSeg'] == want_seg and r1['nSegBest'] == want_best
        and len(r1['perPath']) == len(allp), repr({k: r1[k] for k in ('nSeg', 'nSegBest', 'paths')}))
    chk('R1b 관 이음매 (구) = 조각 점마다 — 굽은 자리가 끊겨 보이지 않는다',
        r1['nJoint'] == sum(npts(path_ids[(c, i)]) for c, i, _ in allp if (c, i) != best[:2])
        and r1['nJointBest'] == npts(path_ids[best[:2]]), repr({k: r1[k] for k in ('nJoint', 'nJointBest')}))
    lo, hi = allp[0][2], allp[-1][2]
    # 경로 k (= 고른 순서) 마다 색 하나 · τ 순 휘도 감소
    pp = r1['perPath']
    order = sorted(pp, key=lambda k: int(k))
    one_col = all(len(pp[k]['cols']) == 1 for k in pp)
    chk('R2 경로마다 한 색 (경로 안의 원기둥은 같은 색)', one_col, repr(pp)[:300])
    nonbest = [k for k in order if int(k) != 0]
    lums = [lum(pp[k]['cols'][0]) for k in nonbest]
    taus_nb = [allp[int(k)][2] for k in nonbest]
    cols_nb = [pp[k]['cols'][0] for k in nonbest]
    ok_ord = taus_nb == sorted(taus_nb) and all((lb < la) if tb > ta else (cb == ca)
                                                  for ta, tb, la, lb, ca, cb in zip(taus_nb, taus_nb[1:], lums, lums[1:], cols_nb, cols_nb[1:]))
    chk(f'R2b 색 순서가 τ 를 따른다 — τ {taus_nb} 순으로 휘도 감소 (큰 τ = 어둡게 · 같은 τ = 같은 색)',
        ok_ord, repr([round(x, 4) for x in lums]))
    want_cols = []
    for k in nonbest:
        t = (allp[int(k)][2] - lo) / (hi - lo)
        want_cols.append(t)
    chk('R2c 경로 색 = tauPathColor((τ − 최소)/(최대 − 최소)) — 끝 경로 (가장 큰 τ) = 램프의 어두운 끝 #0d366b',
        cols_nb[-1] == 0x0d366b and abs(want_cols[-1] - 1.0) < 1e-12, repr([hex(c) for c in cols_nb]))
    chk(f'R3 가장 작은 τ ({best[2]} · 클러스터 #{best[0]}) = 금색 (COL.PATH) · 빛남 · 보통 관보다 굵게 (1.8 배)',
        r1['bestCols'] == [0xffd700] and r1['bestEmissive'] == 0xffd700 and pp['0']['r'] and pp[nonbest[0]]['r']
        and abs(pp['0']['r'][0] / pp[nonbest[0]]['r'][0] - 1.8) < 1e-6, repr({'best': pp.get('0'), 'nb': pp.get(nonbest[0])}))
    chk('R3b 보통 관 굵기 = 상자 폭 × 0.0045 (20 µm 상자 → 0.09 µm) · 경로마다 같다',
        all(pp[k]['r'] == [0.09] for k in nonbest), repr({k: pp[k]['r'] for k in nonbest}))
    chk('R4 상자를 가로지르는 긴 관이 없다 — 가장 긴 원기둥 < 상자 반폭 (주기 넘음 = 양쪽 면 반 토막)',
        max(pp[k]['maxLen'] for k in pp) < 10, repr({k: round(pp[k]['maxLen'], 3) for k in pp}))
    fs = r1['firstSeg']
    chk('R4b 원기둥 위치 = data (x, y, z) → three (x, z, y) · 중점 · 길이 = 홉 길이',
        fs is not None and len(fs['p']) == 3 and fs['s'][1] > 0, repr(fs))
    chk('R5 SE 흐리게 (불투명도 0.08 · 깊이 쓰기 끔 · 본래 색으로 다시 칠함) · AM 흐리게 (0.12) · 판 메시 숨김 · 한 경로 관 숨김',
        r1['se']['opacity'] == 0.08 and r1['se']['depthWrite'] is False and r1['se']['transparent'] is True and r1['se']['recolored'] > 0
        and r1['am']['opacity'] == 0.12 and r1['am']['depthWrite'] is False and r1['ams']['opacity'] == 0.12
        and r1['plate'] is False and r1['pathGroupVisible'] is False, repr({k: r1[k] for k in ('se', 'am', 'plate', 'pathGroupVisible')}))
    chk('R5b 단면 뷰 다시 적용 (applyClip) · PNG 에서 빠지는 장식이 아님 · 시야 밖 잘림 끔 · 장면에 붙음',
        r1['clip'] >= 1 and r1['deco'] is False and r1['frustum'] is True and r1['inScene'] is True, repr({k: r1[k] for k in ('clip', 'deco', 'frustum')}))
    chk('R5c 기본 옵션 = 모든 관통 클러스터 · 경로 전부 · SE 0.08 · AM 0.12 · 굵기 1 · 끝점 끔',
        r1['opt'] == {'scope': 'all', 'top': 0, 'seOpacity': 0.08, 'amOpacity': 0.12, 'width': 1, 'ends': False}, repr(r1['opt']))
    chk('R5d 범례가 붙는다 (정의 문구 포함)', '표의 τ_Dij 와 같은 정의' in re.sub(r'<[^>]+>', '', r1['legend']))
    ag = rr['again']
    chk('R6 다시 그려도 관 묶음은 하나 · 옛 묶음 GPU 자원 해제', ag['nGroups'] == 1 and ag['oldDisposed'] is True, repr(ag))
    s2 = rr['scope2']
    chk('R7 범위 → 클러스터 #2 = 그 경로 둘만', s2['paths'] is not None and [p[0] for p in s2['paths']] == [2, 2], repr(s2['paths']))
    t3 = rr['top3']
    chk('R7b τ 작은 3 개 = 전체 τ 가장 작은 셋만', t3['paths'] == [list(x) for x in allp[:3]], repr(t3['paths']))
    op = rr['opac']
    chk('R8 SE · AM 불투명도 막대 = 재질만 바꾼다 (관 묶음 그대로) · AM 0 = 숨김 · 값 표시',
        op['same'] is True and op['se']['opacity'] == 0.3 and op['am']['visible'] is False and op['seVal'] == '0.30', repr(op))
    wd = rr['wide']
    chk('R9 관 굵기 막대 (2 배) = 다시 짓는다 · 보통 관 0.18 µm · 값 표시 2.0×',
        all(wd['perPath'][k]['r'] == [0.18] for k in wd['perPath'] if k != '0') and wd['val'] == '2.0×',
        repr({k: wd['perPath'][k]['r'] for k in wd['perPath']}))
    chk('R9b 굵기 막대 · 끝점은 관만 다시 짓는다 — 범례를 다시 쓰지 않아 끄는 막대가 손에서 빠지지 않는다',
        wd['sameSlider'] is True and wd['legendsDuring'] == 0, repr({k: wd[k] for k in ('sameSlider', 'legendsDuring')}))
    en = rr['ends']
    chk(f'R10 끝점 켬 = 경로마다 바닥 (청록) · 위 (빨강) 구 둘 ({en["nEnds"]} = 2 × {len(allp)})',
        en['nEnds'] == 2 * len(allp) and sorted(en['endCols']) == sorted([0x22d3ee, 0xf87171]), repr({k: en[k] for k in ('nEnds', 'endCols')}))
    cb = rr['cbar']
    chk('R11 컬러바 ⬇ = exportColorbarPNG(tauPathsColorbarSpec(…), "colorbar_tau_paths.png") · 그림 창 단추 = showTauPathsView',
        len(cb) == 1 and 'Geometric tortuosity' in (cb[0][0] or '') and cb[0][1] == 'colorbar_tau_paths.png' and rr['modal'] == 1, repr(cb))
    chk('R11b 조작 듣개는 범례마다 한 번 (다시 그려도 쌓이지 않는다)', rr['listen'] == {'scope': 1, 'top': 1}, repr(rr['listen']))
    td = rr['td']
    chk('R12 걷기 = 관 묶음 제거 · SE · AM 재질 되돌림 (처음 값 · AM 을 숨긴 채 떠나도 다시 보임) · 한 경로 관 다시 보임',
        rr['amHiddenBeforeLeave'] is False
        and td['group'] is None and td['inScene'] == 0 and (td['se']['opacity'], td['se']['transparent'], td['se']['depthWrite']) == (0.85, True, False)
        and (td['am']['opacity'], td['am']['transparent'], td['am']['depthWrite'], td['am']['visible']) == (1, False, True, True)
        and td['pathGroupVisible'] is True, repr(td))
    sh = rr['show']
    chk('R13 "모든 후보 경로" 단추 = 화면의 클러스터로 범위를 정하고 View Mode 를 tau_paths 로 바꾼다 (change 사건)',
        sh['scope'] == '2' and sh['sel'] == 'tau_paths' and ['view-mode', 'change', 'tau_paths'] in sh['dispatched'], repr(sh))
    chk('R13b 고른 클러스터가 없으면 모든 관통 클러스터', rr['showNull']['scope'] == 'all', repr(rr['showNull']))
    chk('R13c 없는 클러스터 번호가 남아 있으면 모든 관통 클러스터로 그린다 (빈 그림 대신)',
        rr['badScope']['scope'] == 'all' and rr['badScope']['n'] == len(allp), repr(rr['badScope']))
    nn = rr['none']
    chk('R14 저장 경로가 없는 케이스 — 관 없음 · 범례가 그렇다고 말한다',
        nn['group'] is None and '저장된 후보 경로 없음' in re.sub(r'<[^>]+>', '', nn['legend'] or ''), repr(nn)[:300])


# ══════════════════════════════════════════════════════════════════════════════
#  [M] 그림 창 (All Paths View)
# ══════════════════════════════════════════════════════════════════════════════
M_SHIM = R_SHIM.replace("function showTauPathsView(state) { LOG.modal++; }\n", "") + r"""
LOG.scenes = []; LOG.overlay = null; LOG.alerts = []; LOG.saves = []; LOG.captures = []; LOG.composite = []; LOG.cbarExports = [];
class Scene extends Group { constructor() { super(); this.background = 'bg0'; LOG.scenes.push(this); } }
class Obj3 extends Group { constructor() { super(); this.position = new V3(); } }
THREE.Scene = Scene; THREE.PerspectiveCamera = class extends Obj3 {}; THREE.AmbientLight = class extends Obj3 {};
THREE.DirectionalLight = class extends Obj3 {}; THREE.GridHelper = class extends Obj3 {};
THREE.LineSegments = class extends Obj3 { constructor(g, m) { super(); this.geometry = g; this.material = m; } };
THREE.BoxGeometry = Geo; THREE.EdgesGeometry = Geo; THREE.LineBasicMaterial = Mat;
THREE.WebGLRenderer = class { constructor(o) { this.opts = o; this.domElement = mkEl('canvas'); this._clear = [0xf5f5f5, 1]; }
  setPixelRatio() {} setSize() {} setClearColor(c, a) { this._clear = [c, a]; } getClearColor(c) { return c; } getClearAlpha() { return this._clear[1]; }
  render() {} dispose() { this.disposed = true; } };
class OrbitControls { constructor() { this.target = new V3(); } update() {} addEventListener() {} }
const window = { devicePixelRatio: 1 };
function requestAnimationFrame() { return 1; }
function cancelAnimationFrame() {}
function alert(m) { LOG.alerts.push(String(m)); }
function addAxisLabels(scene) { const s = new Obj3(); s.userData.isAxisLabel = true; s.userData.isDecoration = true; scene.add(s); }
function createInstancedSpheres(ps, seg, color, opacity, transparent) { if (!ps || !ps.length) return null;
  const m = new Obj3(); m.material = new Mat({ opacity, transparent, depthWrite: !transparent, color }); m.userData.particles = ps; return m; }
function captureHighRes(r, s, c, scale) { const hiddenAxis = []; s.traverse(o => { if (o.userData && o.userData.isAxisLabel) hiddenAxis.push(o.visible); });
  LOG.captures.push({ alpha: r._clear[1], bg: s.background, scale, axisVisible: hiddenAxis }); return 'data:image/png;base64,SHOT'; }
async function saveWithDialog(url, name, btn, label) { LOG.saves.push([url, name, label]); }
function tauPathsCompositePNG(url, spec) { LOG.composite.push([url, spec && spec.short]); return Promise.resolve('data:image/png;base64,COMP'); }
document.body = { appendChild(o) { LOG.overlay = o; } };
document.createElement = (tag) => { const e = mkEl(tag); e.className = ''; e.clientWidth = 760; e.clientHeight = 520;
  e.appendChild = function (c) { (this.children = this.children || []).push(c); return c; }; e.remove = function () { this.removed = true; };
  e.querySelector = function () { return mkEl('q'); }; return e; };
const _gid = document.getElementById;
document.getElementById = function (id) { const e = _gid.call(document, id); e.clientWidth = e.clientWidth || 760; e.clientHeight = e.clientHeight || 520;
  e.appendChild = e.appendChild || function (c) { return c; }; e.style = e.style || {}; return e; };
exportColorbarPNG = function (spec, name) { LOG.cbarExports.push([spec && spec.title, name]); };
"""

M_RUN = r"""
(async () => {
const OUT = { err: null };
try {
  const idIndex = {}; PARTS.forEach(p => { idIndex[p.id] = p; });
  const se = PARTS.filter(p => p.type === 'SE');
  const state = { data: { particles: PARTS, box: BOX, clusters: { clusters: CL } }, idIndex, seParticles: se,
                  amPParticles: PARTS.filter(p => p.type === 'AM_P'), amSParticles: PARTS.filter(p => p.type === 'AM_S'),
                  amParticles: PARTS.filter(p => p.type !== 'SE') };
  showTauPathsView(state);
  const sc = LOG.scenes[LOG.scenes.length - 1];
  const inst = {}; if (sc) sc.traverse(o => { if (o.isInstancedMesh) inst[o.userData.kind] = (inst[o.userData.kind] || 0) + o.count; });
  let seCtx = null, amCtx = 0, bbox = false; if (sc) sc.traverse(o => { if (o.userData && o.userData.isSEContext) seCtx = o.material.opacity;
    if (o.userData && o.userData.isAMContext) amCtx++; if (o.userData && o.userData.isBbox) bbox = true; });
  OUT.open = { overlay: !!LOG.overlay, html: LOG.overlay ? LOG.overlay.innerHTML : '', inst, seCtx, amCtx, bbox, alerts: LOG.alerts.slice() };
  //  PNG — 투명 · 4× · 축 글자 숨김 · 파일 이름
  const fireAsync = (id, type) => Promise.all((ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).map(l => l[1]({ type, target: ELS[id] })));
  await fireAsync('taup-png-btn', 'click');
  OUT.png1 = { saves: LOG.saves.slice(), captures: LOG.captures.slice(), composite: LOG.composite.slice(), bgAfter: sc ? sc.background : null };
  //  컬러바 넣기 켬 → 합성한 PNG 를 저장
  ELS['taup-m-cbar-in'].checked = true;
  await fireAsync('taup-png-btn', 'click');
  OUT.png2 = { saves: LOG.saves.slice(), composite: LOG.composite.slice() };
  //  컬러바 PNG 단추
  fire('taup-cbar-btn', 'click');
  OUT.cbar = LOG.cbarExports.slice();
  //  펼침 켬 → 관을 다시 짓는다 (펼친 경로는 한 조각 — 반 토막 없음)
  ELS['taup-m-unwrap'].checked = true; fire('taup-m-unwrap', 'change');
  const inst2 = {}; sc.traverse(o => { if (o.isInstancedMesh) inst2[o.userData.kind] = (inst2[o.userData.kind] || 0) + o.count; });
  OUT.unwrap = inst2;
  //  경로가 없는 케이스 — 창을 열지 않고 안내만
  LOG.overlay = null; LOG.alerts = [];
  showTauPathsView({ data: { particles: PARTS, box: BOX, clusters: {} }, idIndex, seParticles: se });
  OUT.none = { overlay: !!LOG.overlay, alerts: LOG.alerts.slice() };
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
})();
"""


def section_modal(js):
    print('[M] 그림 창 (All Paths View)')
    if not shutil.which('node'):
        chk('M0 node 필요', False, 'node 미설치')
        return
    src, miss = fns(js, RENDER_FNS + ('showTauPathsView',))
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    lc = line_consts(js, LINE_CONST_RE)
    if not chk('M0 showTauPathsView 를 잘라 냈다', not miss and not miss_c and len(lc) == 4, f'없음 {miss + miss_c}'):
        return
    rr = run_node(M_SHIM + cs + '\n' + '\n'.join(lc) + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
                  + ';\nconst PARTS = ' + json.dumps(PARTICLES) + ';\nconst BOX = ' + json.dumps(BOX) + ';\n' + M_RUN)
    if not chk('M0b node 실행 (showTauPathsView)', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:900]):
        return
    allp = sorted([p['tortuosity'] for p in PATHS0 + PATHS2])
    o = rr['open']
    html = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', o['html']))
    chk(f'M1 창이 열린다 — 정보 줄 = 경로 6 개 · 관통 클러스터 2 개 · τ {allp[0]:.2f} – {allp[-1]:.2f} · 금색 = 가장 작은 τ',
        o['overlay'] and not o['alerts'] and '경로 6 개' in html and '관통 클러스터 2 개' in html
        and f'τ {allp[0]:.2f} – {allp[-1]:.2f}' in html and '금색' in html, html[:400])
    chk('M1b 창에도 τ 정의 · 표본 문구 (표의 τ_Dij 와 같은 정의 · 수송 tortuosity 아님 · tortuosity_SE_wall · 최대 30)',
        all(w in html for w in ('표의 τ_Dij 와 같은 정의', '수송 tortuosity 아님', 'tortuosity_SE_wall', '최대 30')), html[:900])
    chk('M1c 창의 장면 = 메인과 같은 관 (보통 + 금색 원기둥 · 이음매) · SE 맥락 (불투명도 0.08 · 메인 막대 값) · AM 맥락 · 상자 테두리',
        o['inst'].get('seg', 0) + o['inst'].get('segBest', 0) == 18 and o['inst'].get('segBest', 0) == 2
        and o['inst'].get('joint', 0) > 0 and o['seCtx'] == 0.08 and o['amCtx'] >= 1 and o['bbox'], repr(o))
    ids_need = ('taup-png-btn', 'taup-cbar-btn', 'taup-m-se', 'taup-m-se-op', 'taup-m-am', 'taup-m-unwrap', 'taup-m-ends', 'taup-m-cbar-in')
    chk('M1d 창 조작 — PNG 다운로드 · 컬러바 PNG · SE 맥락 (켬 · 불투명도) · AM · 주기 펼침 · 끝점 · 컬러바 넣기',
        all(f'id="{i}"' in o['html'] for i in ids_need), repr([i for i in ids_need if f'id="{i}"' not in o['html']]))
    chk('M1e "컬러바 넣기" 는 기본 꺼짐 (랩 원칙: 범례 · 주석은 그림 밖 · 편집 가능하게 — docs/report_making_principles.md §2)',
        re.search(r'<input type="checkbox" id="taup-m-cbar-in"(?![^>]*checked)[^>]*>', o['html']) is not None
        and ('report_making_principles' in o['html'] or '범례는 그림 밖' in html))
    p1 = rr['png1']
    want_name = f'tau_paths_n6_tau{allp[0]:.2f}-{allp[-1]:.2f}.png'
    chk(f'M2 PNG 다운로드 = 투명 배경 (지우기 알파 0 · 배경 없음) · 4× · 축 글자 숨김 · 이름 {want_name}',
        len(p1['captures']) == 1 and p1['captures'][0]['alpha'] == 0 and p1['captures'][0]['bg'] is None
        and p1['captures'][0]['scale'] == 4 and p1['captures'][0]['axisVisible'] and not any(p1['captures'][0]['axisVisible'])
        and p1['saves'] and p1['saves'][0][0] == 'data:image/png;base64,SHOT' and p1['saves'][0][1] == want_name
        and not p1['composite'] and p1['bgAfter'] == 'bg0', repr(p1)[:600])
    p2 = rr['png2']
    chk('M2b 컬러바 넣기 켬 = 찍은 그림 + 컬러바 합성본을 저장 (tauPathsCompositePNG)',
        len(p2['composite']) == 1 and p2['composite'][0][0] == 'data:image/png;base64,SHOT' and 'Δz' in (p2['composite'][0][1] or '')
        and p2['saves'][-1][0] == 'data:image/png;base64,COMP' and p2['saves'][-1][1] == want_name, repr(p2)[:500])
    chk('M3 컬러바 PNG 단추 = 따로 받는 컬러바 (exportColorbarPNG · colorbar_tau_paths.png)',
        rr['cbar'] and 'Geometric tortuosity' in (rr['cbar'][0][0] or '') and rr['cbar'][0][1] == 'colorbar_tau_paths.png', repr(rr['cbar']))
    uw = rr['unwrap']
    chk('M4 주기 펼침 켬 = 관을 다시 짓는다 — 넘는 홉도 하나로 (원기둥 18 → 16 · 반 토막 없음)',
        uw.get('seg', 0) + uw.get('segBest', 0) == 16, repr(uw))
    nn = rr['none']
    chk('M5 저장 경로가 없으면 창을 열지 않고 안내만', nn['overlay'] is False and nn['alerts'], repr(nn))


# ══════════════════════════════════════════════════════════════════════════════
#  [C] 컬러바 넣은 PNG 합성
# ══════════════════════════════════════════════════════════════════════════════
C_SHIM = r"""
'use strict';
const LOG = { draws: [], rects: [], texts: [], canvases: [] };
function mkCtx() { return { font: '', fillStyle: '', strokeStyle: '', lineWidth: 1, textAlign: '', textBaseline: '',
  drawImage(img, x, y) { LOG.draws.push([img.src, x, y]); }, fillRect(x, y, w, h) { LOG.rects.push([this.fillStyle, x, y, w, h]); },
  strokeRect() {}, fillText(t, x, y) { LOG.texts.push([String(t), this.font]); }, measureText(t) { return { width: String(t).length * 10 }; },
  beginPath() {}, moveTo() {}, lineTo() {}, stroke() {}, save() {}, restore() {}, translate() {}, rotate() {} }; }
const document = { createElement(tag) { const c = { width: 0, height: 0, _ctx: mkCtx(), getContext() { return this._ctx; },
                     toDataURL() { return 'data:image/png;base64,OUT:' + this.width + 'x' + this.height; } }; LOG.canvases.push(c); return c; } };
class Image { constructor() { this.width = 2800; this.height = 2000; this._src = ''; }
  set src(v) { this._src = v; setTimeout(() => this.onload && this.onload(), 0); } get src() { return this._src; } }
"""

C_RUN = r"""
(async () => {
  const OUT = { err: null };
  try {
    const col = tauPathsCollect(CL, { scope: 'all', top: 0 });
    const spec = tauPathsColorbarSpec(col);
    const url = await tauPathsCompositePNG('data:image/png;base64,SHOT', spec);
    const c = LOG.canvases[LOG.canvases.length - 1];
    const bar = LOG.rects.filter(r => r[1] > 2800);
    const ys = bar.map(r => r[2]);
    const top = bar.length ? bar[ys.indexOf(Math.min(...ys))][0] : null, bot = bar.length ? bar[ys.indexOf(Math.max(...ys))][0] : null;
    OUT.c = { url, w: c.width, h: c.height, draws: LOG.draws, nBar: bar.length, top, bot,
              want: ['#' + tauPathColor(1).toString(16).padStart(6, '0'), '#' + tauPathColor(0).toString(16).padStart(6, '0')],
              texts: LOG.texts.map(t => t[0]), fonts: [...new Set(LOG.texts.map(t => t[1]))], ticks: spec.ticks.map(t => t.label) };
  } catch (e) { OUT.err = String(e && e.stack || e); }
  console.log(JSON.stringify(OUT));
})();
"""


def section_composite(js):
    print('[C] 컬러바 넣은 PNG 합성')
    if not shutil.which('node'):
        chk('C0 node 필요', False, 'node 미설치')
        return
    src, miss = fns(js, PURE_FNS + ('tauPathsCompositePNG',))
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    lc = line_consts(js, LINE_CONST_RE)
    if not chk('C0 tauPathsCompositePNG 를 잘라 냈다', not miss and not miss_c and len(lc) == 4, f'없음 {miss + miss_c}'):
        return
    rr = run_node(C_SHIM + cs + '\n' + '\n'.join(lc) + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS) + ';\n' + C_RUN)
    if not chk('C0b node 실행', rr is not None and rr.get('err') is None, repr(rr and rr.get('err'))[:600]):
        return
    c = rr['c']
    chk(f'C1 합성본 = 찍은 그림 (2800×2000) 을 (0, 0) 에 그대로 + 오른쪽에 컬러바 칸 (폭 {c["w"]} > 2800 · 높이 같음)',
        c['draws'] == [['data:image/png;base64,SHOT', 0, 0]] and c['w'] > 2800 and c['h'] == 2000
        and c['url'] == f'data:image/png;base64,OUT:{c["w"]}x{c["h"]}', repr({k: c[k] for k in ('w', 'h', 'draws', 'url')}))
    chk(f'C2 세로 막대 — 위 = 큰 τ (어두운 끝 {c["want"][0]}) · 아래 = 작은 τ (밝은 끝 {c["want"][1]}) · 그림 칸에는 칠하지 않는다',
        c['nBar'] > 100 and [c['top'], c['bot']] == c['want'], repr({k: c[k] for k in ('nBar', 'top', 'bot')}))
    chk(f'C3 눈금 라벨 = 컬러바 스펙 눈금 ({c["ticks"]}) · 제목 = 짧은 영문 (Geometric τ · path length / Δz)',
        all(t in c['texts'] for t in c['ticks']) and any('Δz' in t and 'Geometric' in t for t in c['texts']), repr(c['texts']))


# ══════════════════════════════════════════════════════════════════════════════
#  [D] /3d-data 가 se_clusters.json 의 경로를 싣는다 (대조)
# ══════════════════════════════════════════════════════════════════════════════
def section_data():
    print('[D] /3d-data — 저장된 후보 경로가 뷰어 입력에 있다 (대조)')
    tmp = tempfile.mkdtemp(prefix='taupaths_')
    try:
        up, rs = os.path.join(tmp, 'uploads'), os.path.join(tmp, 'results')
        os.makedirs(up)
        os.makedirs(rs)
        os.environ['WEBAPP_UPLOAD_FOLDER'], os.environ['WEBAPP_RESULTS_FOLDER'] = up, rs
        import app as webapp
        webapp.app.config['UPLOAD_FOLDER'], webapp.app.config['RESULTS_FOLDER'] = up, rs
        cid = '261007_000001_taupaths'
        os.makedirs(os.path.join(up, cid))
        with open(os.path.join(up, cid, 'meta.json'), 'w') as f:
            json.dump({'name': cid, 'mode': 'standard', 'type_map': '1:AM_P,2:AM_S,3:SE', 'scale': 1000, 'status': 'done'}, f)
        rd = webapp.get_results_dir(cid)
        os.makedirs(rd, exist_ok=True)
        tmap = {'AM_P': 1, 'AM_S': 2, 'SE': 3}
        with open(os.path.join(rd, 'atoms.csv'), 'w') as f:
            f.write('id,type,x,y,z,radius\n')
            for p in PARTICLES:
                f.write(f"{p['id']},{tmap[p['type']]},{p['x'] / 1000},{p['y'] / 1000},{p['z'] / 1000},{p['r'] / 1000}\n")
        with open(os.path.join(rd, 'se_clusters.json'), 'w') as f:
            json.dump({'clusters': CLUSTERS, 'se_cluster_map': {}}, f)
        with open(os.path.join(rd, 'input_params.json'), 'w') as f:
            json.dump({'box_x': 0.02, 'box_y': 0.02}, f)
        c = webapp.app.test_client()
        r = c.get(f'/results/{cid}/3d-data')
        j = r.get_json(silent=True) or {}
        cl = ((j.get('clusters') or {}).get('clusters')) or []
        n = sum(len(x.get('paths') or []) for x in cl if x.get('percolating'))
        chk(f'D1 /3d-data 200 · 클러스터 {len(cl)} 개 · 관통 클러스터 저장 경로 {n} 개 (ids · τ 그대로) · 상자 20 µm',
            r.status_code == 200 and n == 6 and cl[0]['paths'][2]['ids'] == [6, 7, 8, 9]
            and cl[0]['paths'][2]['tortuosity'] == PATHS0[2]['tortuosity'] and j.get('box', {}).get('x_max') == 20.0,
            f'{r.status_code} · {n}')
        pids = {p['id'] for p in j.get('particles') or []}
        chk('D2 경로의 SE id 가 전부 입자 목록에 있다 (뷰어 idIndex 로 찾는다)',
            all(i in pids for x in cl for pth in (x.get('paths') or []) for i in pth['ids']))
    except Exception as e:                                       # noqa: BLE001
        chk('D 절 실행', False, f'{type(e).__name__}: {e}')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def section_registration():
    print('[REG] check_all 배선')
    s = open(CHECK_ALL, encoding='utf-8').read()
    chk('REG scripts/check_all.sh 가 이 시험을 돈다', 'webapp/test_tau_paths_view.py' in s)


def main():
    js = open(VIEWER_JS, encoding='utf-8').read()
    section_ui(js)
    section_pure(js)
    section_render(js)
    section_modal(js)
    section_composite(js)
    section_data()
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
