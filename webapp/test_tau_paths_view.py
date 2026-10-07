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

★ 10-07 2판 (1저자 "이거 여러개 갱신해서 나올 수 있게 해주고 png 다운로드 할때는 박스 안에서 모두 있게") — 그림 창만 (메인 View Mode 그대로):
[P] 순수 함수 — 고르기 (τ 작은 순 · 무작위 = seed 고정 mulberry32 · 갱신 = 다른 집합이 나오는 다음 seed · 경로 전부면 다른 조합 없음) ·
    창 고르기 묶음 (금색 = τ 작은 순 = 범위의 가장 작은 τ · 무작위 = 이 그림 안에서 가장 작은 τ) · 컬러바 스펙 · PNG 이름 (_rand<seed>) ·
    접기 (넘는 홉 = 면에서 정확히 잘라 반대 면 · 모서리 · 파이썬 기준 구현과 좌표까지 같다 · 길이 그대로) · 셀 맞춤 (밖 길이 최소 · 동률이면
    여유 ≥ 0.05 L 중 원래 셀에 가장 가까운 자리 — 파이썬 기준 구현과 같은 답) · 맥락 입자 접기 · PNG 맞춤 (시선 방향으로 뒤로 · NDC 를 파이썬이
    따로 계산) · 정보 줄 문구.
[W] 그림 창 (THREE 껍데기 · 조작을 실제로 누른다) — 고르기 조작 · 경로 수 · ↻ 갱신 (그 자리에서 · 집합이 바뀐다) · 머리 수 · 정보 줄 · 컬러바 ·
    합성 · PNG 이름이 함께 바뀐다 · 주기 경계 셋 (셀 옮김 = 상자 · 격자 · 축 글자 · 맥락 입자가 그 셀 · 점 전부 상자 안 · 'fold' = 원래 셀 ·
    면에서 자름 · 'unwrap' = 옛 펼침) · 셀보다 넓은 경로 = 면에서 잘라 상자 안 · PNG 맞춤 (가까운 시점에서도 상자 · 경로 · 끝점이 다 들어간다 ·
    찍은 뒤 시점 그대로) · 창은 메인 옵션을 고치지 않는다.
[X] 변이 — 셀 옮김 끔 · 접기 = 반 토막 · 무작위가 seed 무시 · PNG 맞춤 끔 · 셀 맞춤 뒤 접기 생략 → 위 시험이 각각 FAIL 한다 (판별력).
    M1c · M1d · M4 = 요청대로 바뀐 기본 ('cell') · 조작 (주기 펼침 체크박스 → 주기 경계 고르기) 에 맞춰 고친 옛 시험.
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


# 2판 그림 창 도우미 — 옛 절 (F · R · M · C) 은 있으면 함께 싣고 (없으면 옛 판 그대로 돈다) · 새 절 (P · W · X) 은 반드시 있어야 한다
VIEW_FNS = ('tauPathsRng', 'tauPathsPick', 'tauPathsRefreshSeed', 'tauPathsViewCol', 'tauPathsCellFit', 'tauPathsFoldPieces',
            'tauPathsWrapParticles', 'tauPathsFrustumFit', 'tauPathsViewInfoHtml',
            'figFrameGroup', 'figContextMeshes', 'figCapturePNG', 'figPngNote')      # 그림 창 공용 (Force Chain View 와 같은 상자 · 맥락 · PNG 맞춤)
VIEW_CONSTS = ('TAUP_VIEW_DEF',)


def view_src(src):
    """있는 것만 — (JS 소스, 없는 이름 목록)"""
    f, miss_f = fns(src, VIEW_FNS)
    c, miss_c = consts(src, VIEW_CONSTS)
    return c + '\n' + f, miss_f + miss_c


# ══════════════════════════════════════════════════════════════════════════════
#  합성 침대 — 상자 x · y [0, 20) µm (주기) · z [0, 10] · SE 중심 (µm)
# ══════════════════════════════════════════════════════════════════════════════
BOX = {'x_min': 0, 'x_max': 20, 'y_min': 0, 'y_max': 20, 'z_min': 0, 'z_max': 10}
P = {1: (5, 5, 0.5), 2: (5.5, 5, 4), 3: (6, 5, 9.5), 4: (4, 5, 3), 5: (4.5, 6, 6),
     6: (19.6, 10, 0.6), 7: (0.4, 10, 3.0), 8: (1.0, 10.5, 6.0), 9: (1.2, 10.2, 9.4),          # x 주기 경계를 넘는 홉 6 → 7
     10: (19.7, 19.6, 0.7), 11: (0.3, 0.5, 2.5), 12: (0.8, 1.0, 5.0), 13: (1.1, 1.3, 9.3),     # 모서리 (x · y) 를 넘는 홉 10 → 11
     14: (15, 15, 0.5), 15: (15, 15.5, 5), 16: (15, 16.5, 9.5), 17: (16, 15, 3), 18: (16.5, 16, 7),
     19: (1, 1, 5), 20: (1.5, 1, 5.5)}


def ref_tau(ids, L=20.0, pos=None):
    """analyze_contacts.py 와 같은 식 — 홉마다 dx = min(|Δx|, L − |Δx|) (y 같음) · τ = Σ 홉 길이 / |z_끝 − z_처음| (소수 둘째 자리)"""
    pos = P if pos is None else pos
    s = 0.0
    for a, b in zip(ids, ids[1:]):
        dx = abs(pos[a][0] - pos[b][0]); dy = abs(pos[a][1] - pos[b][1]); dz = pos[a][2] - pos[b][2]
        dx = min(dx, L - dx); dy = min(dy, L - dy)
        s += math.sqrt(dx * dx + dy * dy + dz * dz)
    zd = abs(pos[ids[-1]][2] - pos[ids[0]][2])
    return round(s / zd, 2), round(s, 1), round(zd, 1)


def mk_path(ids, cat, pos=None):
    t, pl, zd = ref_tau(ids, pos=pos)
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

# 셀보다 넓은 경로 (2판 · 셀 맞춤 뒤에도 접어야 하는 경우) — x 홉마다 최소상 +6 µm · 이어 그리면 x 2 → 38 (폭 36 > 상자 20) · y 3 → 6
P_WIDE = {31: (2, 3, 0.5), 32: (8, 3.5, 2.0), 33: (14, 4, 3.5), 34: (0, 4.5, 5.0), 35: (6, 5, 6.5), 36: (12, 5.5, 8.0), 37: (18, 6, 9.5)}
PATH_WIDE = mk_path([31, 32, 33, 34, 35, 36, 37], 'best', P_WIDE)
CL_WIDE = [{'ids': list(P_WIDE), 'size': len(P_WIDE), 'percolating': True, 'path': PATH_WIDE, 'paths': [PATH_WIDE]}]
PARTS_WIDE = [{'id': i, 'type': 'SE', 'x': x, 'y': y, 'z': z, 'r': 0.5} for i, (x, y, z) in P_WIDE.items()]


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


# ── 2판 기준 구현 (파이썬) ─────────────────────────────────────────────────────────
VIEW_GRID, VIEW_CLEAR, VIEW_MARGIN = 360, 0.05, 0.04          # 뷰어 TAUP_VIEW_DEF 와 같아야 한다 (P0b 가 대조)


def ref_fold(pieces, x0, y0, Lx, Ly, eps=1e-9):
    """접기 기준 — 홉이 면 (x = x0 + m·Lx · y = y0 + n·Ly) 을 넘는 매개 t 에서 자르고 토막마다 가운데 점의 상 (floor) 만큼 옮긴다 ·
    상이 바뀌면 새 조각 (면에서 자른 곳 하나) · 닫힌 셀로 붙임.  반환 (조각, 자른 곳 수)."""
    out, ncut = [], 0
    for pc in pieces:
        if len(pc) < 2:
            continue
        cur, ck = None, None
        for a, b in zip(pc, pc[1:]):
            ts = [0.0, 1.0]
            for ax, o, L in ((0, x0, Lx), (1, y0, Ly)):
                if not L > 0:
                    continue
                d = b[ax] - a[ax]
                if d == 0:
                    continue
                ka, kb = math.floor((a[ax] - o) / L), math.floor((b[ax] - o) / L)
                for m in range(min(ka, kb) + 1, max(ka, kb) + 1):
                    t = (o + m * L - a[ax]) / d
                    if eps < t < 1 - eps:
                        ts.append(t)
            ts.sort()

            def at(t):
                return [a[i] + (b[i] - a[i]) * t for i in range(3)]
            for t0, t1 in zip(ts, ts[1:]):
                if not t1 - t0 > eps:
                    continue
                pm = at((t0 + t1) / 2)
                kx = math.floor((pm[0] - x0) / Lx) if Lx > 0 else 0
                ky = math.floor((pm[1] - y0) / Ly) if Ly > 0 else 0

                def put(q):
                    return [min(x0 + Lx, max(x0, q[0] - kx * Lx)), min(y0 + Ly, max(y0, q[1] - ky * Ly)), q[2]]
                if cur is None or (kx, ky) != ck:
                    if cur is not None:
                        if len(cur) >= 2:
                            out.append(cur)
                        ncut += 1
                    cur, ck = [put(at(t0))], (kx, ky)
                cur.append(put(at(t1)))
        if cur is not None and len(cur) >= 2:
            out.append(cur)
    return out, ncut


def plen(pieces):
    return sum(math.dist(a, b) for pc in pieces for a, b in zip(pc, pc[1:]))


def ref_cell_axis(paths_pieces, a, lo0, L, G=VIEW_GRID, clear_frac=VIEW_CLEAR):
    """셀 맞춤 기준 (한 축) — 최소화 = 셀 [lo0 + s, lo0 + s + L) 밖 경로 길이 합 (경로마다 정수 상 · 가운데가 셀에 드는 상 · 못 들면 그 둘레 셋 중 최소) ·
    동률 → 여유 ≥ clear_frac·L 인 자리 중 원래 셀에 가장 가까운 것 (원 둘레 거리 · 먼저 나온 것) · 없으면 여유 최대.  반환 (s ∈ (−L/2, L/2], 밖, 밖 @0, 여유)."""
    P_ = []
    for pieces in paths_pieces:
        us, segs = [], []
        for pc in pieces:
            for i, q in enumerate(pc):
                us.append(q[a] - lo0)
                if i + 1 < len(pc):
                    segs.append((q[a] - lo0, pc[i + 1][a] - lo0, math.dist(q, pc[i + 1])))
        if us:
            P_.append((min(us), max(us), segs))

    def out_len(segs, c):
        o = 0.0
        for ua, ub, ln in segs:
            va, d = ua + c, ub - ua
            if not abs(d) > 1e-12:
                o += 0.0 if 0 <= va <= L else ln
                continue
            t0, t1 = sorted((-va / d, (L - va) / d))
            o += ln * (1 - max(0.0, min(1.0, t1) - max(0.0, t0)))
        return o
    cand = []
    for g in range(G):
        s = g * L / G
        out, clear = 0.0, math.inf
        for lo, hi, segs in P_:
            k = -math.floor(((lo + hi) / 2 - s) / L)
            l2, h2 = lo + k * L - s, hi + k * L - s
            if l2 >= 0 and h2 <= L:
                clear = min(clear, min(l2, L - h2))
            else:
                out += min(out_len(segs, (k + j) * L - s) for j in (-1, 0, 1))
                clear = min(clear, 0.0)
        cand.append((s, out, clear, min(s, L - s)))
    omin = min(c[1] for c in cand)
    tol = 1e-9 * (1 + max(c[1] for c in cand))
    tie = [c for c in cand if c[1] <= omin + tol]
    ok = [c for c in tie if c[2] >= clear_frac * L]
    if ok:
        pick = min(ok, key=lambda c: c[3])                    # 같은 거리면 먼저 나온 것 (min 은 첫 최소)
    else:
        pick = tie[0]
        for c in tie[1:]:
            if c[2] > pick[2] + 1e-12 or (abs(c[2] - pick[2]) <= 1e-12 and c[3] < pick[3]):
                pick = c
    s = pick[0] - L if pick[0] > L / 2 else pick[0]
    return s, pick[1], cand[0][1], pick[2]


def ref_cell_fit(paths_pieces, box=BOX):
    sx = ref_cell_axis(paths_pieces, 0, box['x_min'], box['x_max'] - box['x_min'])
    sy = ref_cell_axis(paths_pieces, 1, box['y_min'], box['y_max'] - box['y_min'])
    return sx, sy


def _sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _cross(a, b):
    return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]


def _unit(a):
    n = math.sqrt(_dot(a, a))
    return [a[0] / n, a[1] / n, a[2] / n]


def ndc_max(cam, target, pts):
    """핀홀 투영 (three.js lookAt + PerspectiveCamera 와 같은 축) — 점마다 max(|x_ndc|, |y_ndc|) 의 최대 · 카메라 앞 (깊이 > near) 이 아니면 inf"""
    f = _unit(_sub(target, cam['pos']))
    r = _unit(_cross(f, cam['up']))
    u = _cross(r, f)
    T, A = math.tan(math.radians(cam['fov']) / 2), cam['aspect']
    worst = 0.0
    for p in pts:
        v = _sub(p, cam['pos'])
        z = _dot(v, f)
        if not z > cam['near']:
            return math.inf
        worst = max(worst, abs(_dot(v, r)) / (z * T * A), abs(_dot(v, u)) / (z * T))
    return worst


def um_txt(v):
    """정보 줄의 셀 옮김 표기 (−1.44 µm · 0 µm · +2.00 µm)"""
    return '0 µm' if abs(v) < 0.005 else ('+' if v > 0 else '−') + f'{abs(v):.2f} µm'


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
    vsrc, _vmiss = view_src(js)                                  # 2판 도우미 — 있으면 함께 (메인 그리기는 쓰지 않는다)
    rr = run_node(R_SHIM + cs + '\n' + '\n'.join(lc) + '\n' + vsrc + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
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
LOG.cams = []; LOG.ctrls = [];
class Scene extends Group { constructor() { super(); this.background = 'bg0'; LOG.scenes.push(this); } }
class Obj3 extends Group { constructor() { super(); this.position = new V3(); } }
THREE.Scene = Scene; THREE.AmbientLight = class extends Obj3 {};
//  카메라 = 시야각 · 화면비 · near · far · up (PNG 맞춤이 읽는다) · 행렬 갱신 횟수만 센다
THREE.PerspectiveCamera = class extends Obj3 { constructor(fov, aspect, near, far) { super(); this.fov = fov; this.aspect = aspect; this.near = near;
  this.far = far; this.up = new V3(0, 1, 0); this.nProj = 0; this.nWorld = 0; LOG.cams.push(this); }
  updateProjectionMatrix() { this.nProj++; } updateMatrixWorld() { this.nWorld++; } };
THREE.DirectionalLight = class extends Obj3 {}; THREE.GridHelper = class extends Obj3 {};
THREE.LineSegments = class extends Obj3 { constructor(g, m) { super(); this.geometry = g; this.material = m; } };
THREE.BoxGeometry = Geo; THREE.EdgesGeometry = Geo; THREE.LineBasicMaterial = Mat;
THREE.WebGLRenderer = class { constructor(o) { this.opts = o; this.domElement = mkEl('canvas'); this._clear = [0xf5f5f5, 1]; }
  setPixelRatio() {} setSize() {} setClearColor(c, a) { this._clear = [c, a]; } getClearColor(c) { return c; } getClearAlpha() { return this._clear[1]; }
  render() {} dispose() { this.disposed = true; } };
class OrbitControls { constructor(cam) { this.object = cam; this.target = new V3(); this.nUpdate = 0; LOG.ctrls.push(this); }
  update() { this.nUpdate++; } addEventListener() {} }
const window = { devicePixelRatio: 1 };
function requestAnimationFrame() { return 1; }
function cancelAnimationFrame() {}
function alert(m) { LOG.alerts.push(String(m)); }
function addAxisLabels(scene, box) { const s = new Obj3(); s.userData.isAxisLabel = true; s.userData.isDecoration = true; s.userData.box = box ? Object.assign({}, box) : null;
  scene.add(s); }
function createInstancedSpheres(ps, seg, color, opacity, transparent) { if (!ps || !ps.length) return null;
  const m = new Obj3(); m.material = new Mat({ opacity, transparent, depthWrite: !transparent, color }); m.userData.particles = ps; return m; }
//  그려진 내용 (three 좌표) — 상자 꼭짓점 (보일 때) · 관 원기둥 양 끝 · 이음매 · 끝점.  맥락 입자 · 바닥 격자는 넣지 않는다 (PNG 맞춤 대상 밖)
function contentPts(sc) { const pts = [];
  sc.traverse(o => {
    if (o.userData && o.userData.isBbox && o.visible) { const a = (o.geometry && o.geometry.args && o.geometry.args[0] && o.geometry.args[0].args) || [0, 0, 0];
      for (const i of [-1, 1]) for (const j of [-1, 1]) for (const k of [-1, 1]) pts.push([o.position.x + i * a[0] / 2, o.position.y + j * a[1] / 2, o.position.z + k * a[2] / 2]); }
    if (o.isInstancedMesh) { const kd = o.userData.kind; o.mats.forEach(m => {
      if (kd === 'seg' || kd === 'segBest') { const h = m.s[1] / 2, d = m.q || [0, 1, 0];
        pts.push([m.p[0] - d[0] * h, m.p[1] - d[1] * h, m.p[2] - d[2] * h], [m.p[0] + d[0] * h, m.p[1] + d[1] * h, m.p[2] + d[2] * h]); }
      else pts.push(m.p.slice()); }); } });
  return pts; }
//  장면 요약 — 관 (종류별 수 · 경로 번호별 이음매 차례) · 끝점 · 원기둥 양 끝 · 상자 · 격자 · 축 글자 상자 · 맥락 입자 (data 좌표 · id)
function snapScene(sc) { const r = { kinds: {}, joints: [], ends: [], segEnds: [], segLen: 0, paths: [], bbox: null, grid: null, labels: [], se: null, am: [] };
  const ks = new Set();
  sc.traverse(o => {
    if (o.isInstancedMesh) { const kd = o.userData.kind; r.kinds[kd] = (r.kinds[kd] || 0) + o.count;
      o.mats.forEach((m, i) => { const k = (o.userData.instPath || [])[i]; ks.add(k);
        if (kd === 'seg' || kd === 'segBest') { const h = m.s[1] / 2, d = m.q || [0, 1, 0]; r.segLen += m.s[1];
          r.segEnds.push([m.p[0] - d[0] * h, m.p[1] - d[1] * h, m.p[2] - d[2] * h], [m.p[0] + d[0] * h, m.p[1] + d[1] * h, m.p[2] + d[2] * h]); }
        else if (kd === 'ends') r.ends.push([k].concat(m.p));
        else r.joints.push([k, kd === 'jointBest' ? 1 : 0].concat(m.p)); }); }
    const u = o.userData || {};
    if (u.isBbox) { const a = (o.geometry && o.geometry.args && o.geometry.args[0] && o.geometry.args[0].args) || null;
      r.bbox = { c: [o.position.x, o.position.y, o.position.z], size: a, visible: o.visible !== false }; }
    if (u.isGrid) r.grid = [o.position.x, o.position.y, o.position.z];
    if (u.isAxisLabel) r.labels.push(u.box);
    if (u.isSEContext) r.se = (u.particles || []).map(p => [p.id, p.x, p.y, p.z]);
    if (u.isAMContext) r.am.push((u.particles || []).map(p => [p.id, p.x, p.y, p.z])); });
  r.paths = [...ks].filter(k => k != null).sort((a, b) => a - b);
  return r; }
function captureHighRes(r, s, c, scale) { const hiddenAxis = []; s.traverse(o => { if (o.userData && o.userData.isAxisLabel) hiddenAxis.push(o.visible); });
  const t = LOG.ctrls[LOG.ctrls.length - 1];
  LOG.captures.push({ alpha: r._clear[1], bg: s.background, scale, axisVisible: hiddenAxis,
    cam: { pos: [c.position.x, c.position.y, c.position.z], up: c.up ? [c.up.x, c.up.y, c.up.z] : [0, 1, 0], fov: c.fov, aspect: c.aspect, near: c.near, far: c.far },
    target: t ? [t.target.x, t.target.y, t.target.z] : null, content: contentPts(s) });
  return 'data:image/png;base64,SHOT'; }
async function saveWithDialog(url, name, btn, label) { LOG.saves.push([url, name, label]); }
function tauPathsCompositePNG(url, spec) { LOG.composite.push([url, spec && spec.short, spec && spec.sub]); return Promise.resolve('data:image/png;base64,COMP'); }
document.body = { appendChild(o) { LOG.overlay = o; } };
document.createElement = (tag) => { const e = mkEl(tag); e.className = ''; e.clientWidth = 760; e.clientHeight = 520;
  e.appendChild = function (c) { (this.children = this.children || []).push(c); return c; }; e.remove = function () { this.removed = true; };
  e.querySelector = function () { return mkEl('q'); }; return e; };
const _gid = document.getElementById;
document.getElementById = function (id) { const e = _gid.call(document, id); e.clientWidth = e.clientWidth || 760; e.clientHeight = e.clientHeight || 520;
  e.appendChild = e.appendChild || function (c) { return c; }; e.style = e.style || {}; return e; };
exportColorbarPNG = function (spec, name) { LOG.cbarExports.push([spec && spec.title, name, spec && spec.sub]); };
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
  //  주기 경계 = 이어 그림 (옛 "주기 펼침" 켬) → 관을 다시 짓는다 (펼친 경로는 한 조각 — 상자 밖 허용)
  //  (요소는 getElementById 로 — 옛 판 창에는 이 조작이 없어 사건이 아무것도 안 한다 · 실행은 멈추지 않는다)
  document.getElementById('taup-m-bound').value = 'unwrap'; fire('taup-m-bound', 'change');
  { const s = snapScene(sc); OUT.unwrap = Object.assign({}, s.kinds, { maxX: Math.max(...s.joints.map(j => j[2])), maxY: Math.max(...s.joints.map(j => j[4])) }); }
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
    vsrc, _vmiss = view_src(js)                                  # 2판 도우미 — 있으면 함께 (없으면 옛 창 그대로 돈다)
    if not chk('M0 showTauPathsView 를 잘라 냈다', not miss and not miss_c and len(lc) == 4, f'없음 {miss + miss_c}'):
        return
    rr = run_node(M_SHIM + cs + '\n' + '\n'.join(lc) + '\n' + vsrc + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
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
    # ★ 2판 — 창의 기본 주기 경계 = 'cell' (경로마다 이어 그린 뒤 셀 자리를 옮김) → 이 침대는 반 토막 없이 원기둥 = 홉 수 16 (옛 판 = 반 토막 18)
    chk('M1c 창의 장면 (기본 주기 경계 = 셀 옮김) = 경로마다 이어 그린 관 (보통 + 금색 원기둥 16 = 홉 수 · 금색 2 · 반 토막 없음) · 이음매 · '
        'SE 맥락 (불투명도 0.08 · 메인 막대 값) · AM 맥락 · 상자 테두리',
        o['inst'].get('seg', 0) + o['inst'].get('segBest', 0) == 16 and o['inst'].get('segBest', 0) == 2
        and o['inst'].get('joint', 0) > 0 and o['seCtx'] == 0.08 and o['amCtx'] >= 1 and o['bbox'], repr(o))
    ids_need = ('taup-png-btn', 'taup-cbar-btn', 'taup-m-se', 'taup-m-se-op', 'taup-m-am', 'taup-m-bound', 'taup-m-ends', 'taup-m-cbar-in')
    chk('M1d 창 조작 — PNG 다운로드 · 컬러바 PNG · SE 맥락 (켬 · 불투명도) · AM · 주기 경계 (고르기 — 옛 "주기 펼침" 체크박스는 없다) · 끝점 · 컬러바 넣기',
        all(f'id="{i}"' in o['html'] for i in ids_need) and 'id="taup-m-unwrap"' not in o['html'],
        repr([i for i in ids_need if f'id="{i}"' not in o['html']]))
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
    chk('M4 주기 경계 = 이어 그림 (옛 "주기 펼침") = 관을 다시 짓는다 — 넘는 홉도 하나로 (원기둥 16 · 반 토막 없음) · 상자 밖으로 나간다 (허용 · x 또는 y > 20)',
        uw.get('seg', 0) + uw.get('segBest', 0) == 16 and max(uw.get('maxX', 0), uw.get('maxY', 0)) > 20 + 1e-6, repr(uw))
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
#  [P] 2판 순수 함수 — 고르기 · 갱신 · 창 고르기 묶음 · 접기 · 셀 맞춤 · 입자 접기 · PNG 맞춤 · 정보 줄
# ══════════════════════════════════════════════════════════════════════════════
FIDS = {'straight': [1, 2, 3], 'b1': [1, 4, 5, 3], 'xwrap': [6, 7, 8, 9], 'corner': [10, 11, 12, 13], 'c2a': [14, 15, 16], 'c2b': [14, 17, 18, 16]}
CELLS = {'c0': (0.0, 0.0), 'cs': (-1.4444444444444446, -1.4444444444444446), 'c2': (2.0, 0.0)}
#  접기 가장자리 — 면에 닿고 돌아감 (자르지 않음) · 정확한 모서리 (x · y 를 같은 t 에) · 면 위 꼭짓점에서 넘어감 · 왼쪽으로 넘음 · 비주기 축 (L 0)
EDGE = [{'pieces': [[[5, 5, 0], [20, 5, 1], [15, 5, 2]]], 'cell': {'x0': 0, 'y0': 0, 'Lx': 20, 'Ly': 20},
         'want': [[[5, 5, 0], [20, 5, 1], [15, 5, 2]]], 'cut': 0},
        {'pieces': [[[19, 19, 0], [21, 21, 1]]], 'cell': {'x0': 0, 'y0': 0, 'Lx': 20, 'Ly': 20},
         'want': [[[19, 19, 0], [20, 20, 0.5]], [[0, 0, 0.5], [1, 1, 1]]], 'cut': 1},
        {'pieces': [[[15, 5, 0], [20, 5, 1], [25, 5, 2]]], 'cell': {'x0': 0, 'y0': 0, 'Lx': 20, 'Ly': 20},
         'want': [[[15, 5, 0], [20, 5, 1]], [[0, 5, 1], [5, 5, 2]]], 'cut': 1},
        {'pieces': [[[1, 5, 0], [-1, 5, 1]]], 'cell': {'x0': 0, 'y0': 0, 'Lx': 20, 'Ly': 20},
         'want': [[[1, 5, 0], [0, 5, 0.5]], [[20, 5, 0.5], [19, 5, 1]]], 'cut': 1},
        {'pieces': [[[1, 5, 0], [25, 5, 1]]], 'cell': {'x0': 0, 'y0': 0, 'Lx': 0, 'Ly': 20},
         'want': [[[1, 5, 0], [25, 5, 1]]], 'cut': 0}]
BOXC = [[x, y, z] for x in (0, 20) for y in (0, 10) for z in (0, 20)]          # three 좌표 (x, z_data, y_data) 상자 꼭짓점


def _rand_sets(n_sets=6, seed=20261007):
    """셀 맞춤 무작위 대조 — 경로 묶음 (이어 그린 조각) · 걸음 폭이 묶음마다 다르다 (셀보다 넓은 경로 포함) · 홉의 일부는 x 또는 y 가 그대로 (점 무게) ·
    한 경로는 조각 둘 (모르는 id 에서 끊긴 꼴)"""
    import random
    rg = random.Random(seed)
    out = []
    for si in range(n_sets):
        step = (1.0, 2.5, 4.0, 6.0, 9.0, 3.0)[si % 6]
        ps = []
        for _p in range(rg.randint(4, 14)):
            x, y, z = rg.uniform(0, 20), rg.uniform(0, 20), 0.5
            pc = [[x, y, z]]
            for _h in range(rg.randint(3, 25)):
                x += 0.0 if rg.random() < 0.15 else rg.uniform(-step, step)
                y += 0.0 if rg.random() < 0.15 else rg.uniform(-step, step)
                z += rg.uniform(0.2, 1.0)
                pc.append([x, y, z])
            pieces = [pc] if len(pc) < 6 or rg.random() < 0.8 else [pc[:3], pc[4:]]
            ps.append(pieces)
        out.append(ps)
    return out


RAND_SETS = _rand_sets()
FF = [{'cam': {'pos': [10.5, 5.5, 10.5], 'up': [0, 1, 0], 'fov': 50, 'aspect': 760 / 520, 'near': 0.1}, 'target': [10, 5, 10], 'pts': BOXC, 'margin': 0.04},
      {'cam': {'pos': [210, 155, 210], 'up': [0, 1, 0], 'fov': 50, 'aspect': 760 / 520, 'near': 0.1}, 'target': [10, 5, 10], 'pts': BOXC, 'margin': 0.04},
      {'cam': {'pos': [0, 0, 10], 'up': [0, 1, 0], 'fov': 50, 'aspect': 1.5, 'near': 0.1}, 'target': [0, 0, 0], 'pts': [[0, 0, 20], [1, 1, 0]], 'margin': 0.04},
      {'cam': {'pos': [0, 30, 0], 'up': [0, 1, 0], 'fov': 50, 'aspect': 1.5, 'near': 0.1}, 'target': [0, 0, 0], 'pts': [[-20, 0, -20], [20, 0, 20]], 'margin': 0.04}]

P_RUN = r"""
const OUT = {};
const idIndex = {}; PARTS.forEach(p => { idIndex[p.id] = p; });
const idW = {}; PARTS_W.forEach(p => { idW[p.id] = p; });
OUT.def = TAUP_VIEW_DEF;
const full = tauPathsCollect(CL, { scope: 'all', top: 0 });
const key = ps => ps.map(p => p.ci + ':' + p.pi);
OUT.full = key(full.paths); OUT.fullTau = full.paths.map(p => p.tau);
const pk = (n, m, s) => { const r = tauPathsPick(full.paths, n, m, s); return { keys: key(r.paths), taus: r.paths.map(p => p.tau), all: r.all, mode: r.mode, seed: r.seed }; };
OUT.pickTau3 = pk(3, 'tau', 7);
OUT.pickR3a = pk(3, 'rand', 4); OUT.pickR3b = pk(3, 'rand', 4);
OUT.pickSeeds = Array.from({ length: 200 }, (_, i) => key(tauPathsPick(full.paths, 3, 'rand', i + 1).paths).join(','));
OUT.pickAll0 = pk(0, 'rand', 5); OUT.pickAll30 = pk(30, 'rand', 5); OUT.pickAll6 = pk(6, 'tau', 5);
{ const r = tauPathsRng(9), r2 = tauPathsRng(9), a = [], b = []; for (let i = 0; i < 50; i++) { a.push(r()); b.push(r2()); } OUT.rng = { a, b }; }
{ const cur = tauPathsPick(full.paths, 3, 'rand', 4);
  const r = tauPathsRefreshSeed(full.paths, 3, 4, cur.paths);
  OUT.refresh = { seed: r.seed, changed: r.changed, before: key(cur.paths), after: key(tauPathsPick(full.paths, 3, 'rand', r.seed).paths) };
  const ra = tauPathsRefreshSeed(full.paths, 0, 4, full.paths);
  OUT.refreshAll = { seed: ra.seed, changed: ra.changed };
  const t3 = tauPathsPick(full.paths, 3, 'tau', 1).paths, rt = tauPathsRefreshSeed(full.paths, 3, 1, t3);
  OUT.refreshFromTau = { seed: rt.seed, changed: rt.changed, before: key(t3), after: key(tauPathsPick(full.paths, 3, 'rand', rt.seed).paths) }; }
const vc = ws => { const c = tauPathsViewCol(CL, ws);
  return { keys: key(c.paths), n: c.paths.length, lo: c.lo, hi: c.hi, best: c.best ? [c.best.ci, c.best.pi, c.best.tau] : null, scope: c.scope,
    nScope: c.nScope, nAvail: c.nAvail, scopeBest: c.scopeBest ? [c.scopeBest.ci, c.scopeBest.pi, c.scopeBest.tau] : null, bestIsScopeMin: c.bestIsScopeMin,
    mode: c.mode, want: c.want, seed: c.seed, all: c.all, nClusters: c.nClusters, perc: (c.percClusters || []).map(q => [q.ci, q.size, q.n]),
    spec: tauPathsColorbarSpec(c).sub, png: tauPathsPngName(c),
    infoCell: tauPathsViewInfoHtml(c, { bound: 'cell', fit: { sx: -1.4444444444444446, sy: -1.4444444444444446 }, st: { nCut: 0, nCutPaths: 0 } }),
    infoCell0: tauPathsViewInfoHtml(c, { bound: 'cell', fit: { sx: 0, sy: 0 }, st: { nCut: 0, nCutPaths: 0 } }),
    infoCellWide: tauPathsViewInfoHtml(c, { bound: 'cell', fit: { sx: 2, sy: 0 }, st: { nCut: 1, nCutPaths: 1 } }),
    infoFold: tauPathsViewInfoHtml(c, { bound: 'fold', fit: null, st: { nCut: 3, nCutPaths: 2 } }),
    infoUnwrap: tauPathsViewInfoHtml(c, { bound: 'unwrap', fit: null, st: { nCut: 0, nCutPaths: 0 } }) }; };
OUT.vTau3 = vc({ scope: 'all', n: 3, mode: 'tau', seed: 1 });
OUT.vAll = vc({ scope: 'all', n: 0, mode: 'tau', seed: 1 });
OUT.vAllRand = vc({ scope: 'all', n: 0, mode: 'rand', seed: 3 });
OUT.vBad = vc({ scope: '7', n: 0, mode: 'tau', seed: 1 });
OUT.v2 = vc({ scope: '2', n: 5, mode: 'rand', seed: 1 });
{ let s = 1; for (; s < 500; s++) { const c = tauPathsViewCol(CL, { scope: 'all', n: 3, mode: 'rand', seed: s }); if (c.paths[0].tau > c.scopeBest.tau) break; }
  OUT.seedNoMin = s; OUT.vRandNoMin = vc({ scope: 'all', n: 3, mode: 'rand', seed: s }); }
{ let s = 1; for (; s < 500; s++) { const c = tauPathsViewCol(CL, { scope: 'all', n: 3, mode: 'rand', seed: s }); if (c.paths[0].tau === c.scopeBest.tau) break; }
  OUT.seedMin = s; OUT.vRandMin = vc({ scope: 'all', n: 3, mode: 'rand', seed: s }); }
OUT.unw = {};
for (const [k, ids] of Object.entries(FIDS)) OUT.unw[k] = tauPathPieces(ids, idIndex, BOX, true).pieces;
OUT.unw.wide = tauPathPieces(WIDE_IDS, idW, BOX, true).pieces;
OUT.fold = {};
for (const [k, pcs] of Object.entries(OUT.unw)) for (const [ck, c] of Object.entries(CELLS)) {
  const r = tauPathsFoldPieces(pcs, { x0: c[0], y0: c[1], Lx: 20, Ly: 20 }); OUT.fold[k + '@' + ck] = { pieces: r.pieces, nCut: r.nCut }; }
OUT.foldEdge = EDGE.map(e => tauPathsFoldPieces(e.pieces, e.cell));
const fitOf = (paths, idx) => tauPathsCellFit(paths.map(p => tauPathPieces(p.ids, idx, BOX, true).pieces), BOX);
OUT.fitAll = fitOf(full.paths, idIndex);
OUT.fit2 = fitOf(tauPathsCollect(CL, { scope: '2', top: 0 }).paths, idIndex);
OUT.fitWide = fitOf(tauPathsCollect(CL_W, { scope: 'all', top: 0 }).paths, idW);
OUT.fitNone = tauPathsCellFit([], BOX);
OUT.fitRand = RS.map(ps => tauPathsCellFit(ps, BOX));
{ const c = { x0: OUT.fitAll.x0, y0: OUT.fitAll.y0, Lx: 20, Ly: 20 };
  const w = tauPathsWrapParticles(PARTS, c);
  OUT.wrap = { pts: w.map(p => [p.id, p.x, p.y, p.z]), same: w.map((p, i) => p === PARTS[i]) };
  OUT.wrap0Same = tauPathsWrapParticles(PARTS, { x0: 0, y0: 0, Lx: 20, Ly: 20 }) === PARTS;
  const extra = PARTS.concat([{ id: 900, type: 'SE', x: 20.3, y: -0.2, z: 1, r: 0.5 }]);
  OUT.wrapOut = tauPathsWrapParticles(extra, { x0: 0, y0: 0, Lx: 20, Ly: 20 }).map(p => [p.id, p.x, p.y, p.z]);
  OUT.wrapOrig = [extra[extra.length - 1].x, extra[extra.length - 1].y]; }
OUT.ff = FF.map(q => tauPathsFrustumFit(q.cam, q.target, q.pts, q.margin));
console.log(JSON.stringify(OUT));
"""


def _close(a, b, tol=1e-12):
    return all(abs(u - v) <= tol for u, v in zip(a, b)) and len(a) == len(b)


def _pieces_close(a, b, tol=1e-12):
    return len(a) == len(b) and all(len(pa) == len(pb) and all(_close(qa, qb, tol) for qa, qb in zip(pa, pb)) for pa, pb in zip(a, b))


def _plain(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', h or ''))


def section_view_pure(js):
    print('[P] 2판 순수 함수 — 고르기 · 갱신 · 접기 · 셀 맞춤 · 입자 접기 · PNG 맞춤 · 정보 줄 (node)')
    if not shutil.which('node'):
        chk('P0 node 필요', False, 'node 미설치')
        return
    src, miss = fns(js, PURE_FNS)
    vsrc, vmiss = view_src(js)
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    lc = line_consts(js, LINE_CONST_RE)
    if not chk('P0 viewer3d.js 에서 ' + ' · '.join(VIEW_FNS) + ' · TAUP_VIEW_DEF 를 잘라 냈다',
               not miss and not vmiss and not miss_c and len(lc) == 4, f'없음 {miss + vmiss + miss_c}'):
        return
    script = ('"use strict";\n' + cs + '\n' + '\n'.join(lc) + '\n' + vsrc + '\n' + src + '\nconst CL = ' + json.dumps(CLUSTERS)
              + ';\nconst PARTS = ' + json.dumps(PARTICLES) + ';\nconst BOX = ' + json.dumps(BOX) + ';\nconst CL_W = ' + json.dumps(CL_WIDE)
              + ';\nconst PARTS_W = ' + json.dumps(PARTS_WIDE) + ';\nconst WIDE_IDS = ' + json.dumps(PATH_WIDE['ids'])
              + ';\nconst FIDS = ' + json.dumps(FIDS) + ';\nconst CELLS = ' + json.dumps(CELLS) + ';\nconst EDGE = ' + json.dumps(EDGE)
              + ';\nconst FF = ' + json.dumps(FF) + ';\nconst RS = ' + json.dumps(RAND_SETS) + ';\n' + P_RUN)
    res = run_node(script)
    if not chk('P0b node 실행', res is not None):
        return
    d = res['def']
    chk('P0c 그림 창 기본 TAUP_VIEW_DEF — 경로 수 [5 · 10 · 15 · 20 · 30 · 0 = 전부] · 주기 경계 셋 (cell · fold · unwrap · 이름) · 격자 360 · 여유 0.05 L · NDC 여백 0.04 '
        '(파이썬 기준 구현과 같은 값)',
        d.get('ns') == [5, 10, 15, 20, 30, 0] and [b[0] for b in d.get('bounds', [])] == ['cell', 'fold', 'unwrap']
        and d['bounds'][0][1] == '상자 안 · 단위 셀을 경로에 맞춰 옮김 (이어 그림)' and d['bounds'][1][1] == '상자 안 · 원래 셀 (넘는 홉은 면에서 잘라 반대 면)'
        and d['bounds'][2][1] == '이어 그림 · 상자 밖 허용'
        and (d.get('grid'), d.get('clear'), d.get('margin')) == (VIEW_GRID, VIEW_CLEAR, VIEW_MARGIN), repr(d))

    # ── 고르기 ──
    full, ftau = res['full'], res['fullTau']
    t3 = res['pickTau3']
    chk(f'P1 τ 작은 순 3 개 = τ 가장 작은 셋 ({t3["taus"]}) · 경로 전부 아님 · seed 없음 (지금 판 그대로)',
        t3['keys'] == full[:3] and t3['all'] is False and t3['mode'] == 'tau' and t3['seed'] is None, repr(t3))
    a, b = res['pickR3a'], res['pickR3b']
    chk(f'P2 무작위 3 개 — 같은 seed = 같은 집합 ({a["keys"]}) · τ 오름차순 · 저장 경로에서만 · seed 를 돌려준다',
        a == b and len(a['keys']) == 3 and a['taus'] == sorted(a['taus']) and set(a['keys']) <= set(full) and a['mode'] == 'rand'
        and a['seed'] == 4 and a['all'] is False, repr(a))
    seeds = res['pickSeeds']
    seen = set(k for s in seeds for k in s.split(','))
    chk(f'P2b seed 를 바꾸면 집합이 바뀐다 — seed 1…200 에서 서로 다른 집합 {len(set(seeds))} 개 (C(6,3) = 20 중 ≥ 10) · 경로 6 개가 다 한 번은 뽑힌다',
        len(set(seeds)) >= 10 and seen == set(full), f'{len(set(seeds))} · {sorted(seen)}')
    chk('P2c 경로 수 0 (= 전부) · 고를 수 있는 수 이상 (30 · 6) = 경로 전부 (무작위를 골라도 τ 순 같은 집합 · seed 없음 · 다른 조합 없음)',
        all(res[k]['all'] is True and res[k]['keys'] == full and res[k]['mode'] == 'tau' and res[k]['seed'] is None
            for k in ('pickAll0', 'pickAll30', 'pickAll6')), repr({k: res[k] for k in ('pickAll0', 'pickAll30')}))
    rg = res['rng']
    chk('P2d 난수 (mulberry32) — 같은 seed = 같은 수열 · [0, 1) · 고르게 흩어짐 (50 개 중 서로 다른 값 ≥ 45)',
        rg['a'] == rg['b'] and all(0 <= x < 1 for x in rg['a']) and len(set(rg['a'])) >= 45, repr(rg['a'][:5]))
    rf, ra, rt = res['refresh'], res['refreshAll'], res['refreshFromTau']
    chk(f'P3 ↻ 갱신 = 지금 보이는 집합과 다른 집합이 나오는 다음 seed (4 → {rf["seed"]}) · 경로 전부면 다른 조합 없음 (seed + 1 · changed 거짓) · '
        f'τ 작은 순에서 눌러도 다른 집합 ({rt["seed"]})',
        rf['changed'] is True and rf['seed'] > 4 and rf['after'] != rf['before'] and len(rf['after']) == 3
        and ra == {'seed': 5, 'changed': False} and rt['changed'] is True and rt['after'] != rt['before'], repr((rf, ra, rt)))

    # ── 창 고르기 묶음 ──
    v3 = res['vTau3']
    chk(f'P4 창 고르기 (τ 작은 순 3) — 경로 3 개 · τ {v3["lo"]} – {v3["hi"]} · 금색 = 범위의 가장 작은 τ ({ftau[0]}) · 범위 6 개 · 경로 전부 아님',
        v3['keys'] == full[:3] and v3['best'] is not None and v3['best'][2] == ftau[0] and v3['bestIsScopeMin'] is True
        and (v3['lo'], v3['hi']) == (ftau[0], ftau[2]) and v3['nScope'] == 6 and v3['mode'] == 'tau' and v3['all'] is False
        and v3['seed'] is None and v3['scope'] == 'all', repr(v3))
    vn, sn = res['vRandNoMin'], res['seedNoMin']
    chk(f'P4b 무작위 (seed {sn} — 범위의 가장 작은 τ 가 빠진 집합) — 금색 = 이 그림 안에서 가장 작은 τ ({vn["best"]}) · 범위 최소 ({ftau[0]}) 와 다르다고 표시',
        sn < 500 and vn['mode'] == 'rand' and vn['seed'] == sn and vn['best'] is not None and vn['best'][2] == vn['lo'] and vn['lo'] > ftau[0]
        and vn['bestIsScopeMin'] is False and vn['scopeBest'][2] == ftau[0] and vn['keys'][0] == f'{vn["best"][0]}:{vn["best"][1]}', repr(vn))
    gold_rand = _plain(vn['infoCell0'])
    chk('P4c 무작위 정보 줄 — "금색 = 이 그림 안에서 가장 작은 τ" · 범위 전체의 가장 작은 τ 는 이 그림에 없다 (값과 함께) · 무작위 · seed',
        '금색 = 이 그림 안에서 가장 작은 τ' in gold_rand and f'범위 전체의 가장 작은 τ {ftau[0]:.2f} 는 이 그림에 없다' in gold_rand
        and f'무작위 · seed {sn}' in gold_rand and '경로 3 개 (범위의 6 개 중 무작위' in gold_rand, gold_rand)
    vm = res['vRandMin']
    chk(f'P4d 무작위 집합에 범위 최소가 들면 (seed {res["seedMin"]}) "범위 전체의 가장 작은 τ 와 같다"',
        vm['bestIsScopeMin'] is True and vm['best'][2] == ftau[0] and '범위 전체의 가장 작은 τ 와 같다' in _plain(vm['infoCell0']), repr(vm)[:300])
    va = res['vAllRand']
    chk('P4e 경로 수 = 전부 + 무작위 = 경로 전부 (다른 조합 없음) — 실제 고르기 = τ 순 · 원한 고르기 = 무작위 · seed 없음 · PNG 이름에 _rand 없음',
        va['all'] is True and va['mode'] == 'tau' and va['want'] == 'rand' and va['seed'] is None and '_rand' not in va['png']
        and va['keys'] == full and '다른 조합 없음' in _plain(va['infoCell0']), repr(va)[:300])
    chk('P4f 없는 범위 (클러스터 #7) = 모든 관통 클러스터 (창 안에서만) · 범위 #2 = 그 경로 둘 (경로 수 5 ≥ 2 = 전부) · 범위 목록은 그대로',
        res['vBad']['scope'] == 'all' and res['vBad']['n'] == 6 and res['v2']['scope'] == '2' and res['v2']['n'] == 2 and res['v2']['all'] is True
        and res['v2']['perc'] == [[0, 13, 4], [2, 5, 2]], repr((res['vBad']['scope'], res['v2']['scope'], res['v2']['n'])))
    chk(f'P5 컬러바 부제 = 고른 집합 — 무작위 "3 of 6 stored candidate paths (random subset, seed {sn}) · gold = lowest τ in this figure" · '
        'τ 작은 순 "3 lowest-τ of 6" · 전부 "6 stored candidate paths" · 셋 다 수송 tortuosity 아님',
        f'3 of 6 stored candidate paths (random subset, seed {sn})' in vn['spec'] and 'gold = lowest τ in this figure' in vn['spec']
        and '3 lowest-τ of 6 stored candidate paths' in v3['spec'] and 'gold = lowest τ.' in v3['spec']
        and '6 stored candidate paths; gold = lowest τ.' in res['vAll']['spec']
        and all('not the transport tortuosity' in x['spec'] for x in (vn, v3, res['vAll'])), repr((vn['spec'], v3['spec']))[:600])
    chk(f'P5b PNG 이름 — 무작위 = …_rand{sn}.png (이어 받아도 덮어쓰지 않게) · τ 작은 순 · 전부 = 옛 이름 그대로',
        vn['png'] == f'tau_paths_n3_tau{vn["lo"]:.2f}-{vn["hi"]:.2f}_rand{sn}.png'
        and v3['png'] == f'tau_paths_n3_tau{ftau[0]:.2f}-{ftau[2]:.2f}.png' and res['vAll']['png'] == f'tau_paths_n6_tau{ftau[0]:.2f}-{ftau[-1]:.2f}.png',
        repr((vn['png'], v3['png'], res['vAll']['png'])))

    # ── 접기 ──
    unw = res['unw']
    ref_unw = {k: ref_pieces(ids, unwrap=True)[0] for k, ids in FIDS.items()}
    ref_unw['wide'] = ref_pieces(PATH_WIDE['ids'], unwrap=True, idx=P_WIDE)[0]
    chk('P6 이어 그린 조각 (tauPathPieces unwrap) = 파이썬 기준 (접기의 입력)', all(_pieces_close(unw[k], ref_unw[k], 1e-12) for k in ref_unw),
        repr({k: unw[k] for k in ('xwrap', 'wide')})[:300])
    bad_ref, bad_prop = [], []
    for k, pcs in ref_unw.items():
        for ck, (x0, y0) in CELLS.items():
            got = res['fold'][f'{k}@{ck}']
            want, wcut = ref_fold(pcs, x0, y0, 20.0, 20.0)
            if not (_pieces_close(got['pieces'], want, 1e-12) and got['nCut'] == wcut):
                bad_ref.append((k, ck, got, want, wcut))
            pts = [q for pc in got['pieces'] for q in pc]
            ok_in = all(x0 <= q[0] <= x0 + 20 and y0 <= q[1] <= y0 + 20 for q in pts)
            ok_len = abs(plen(got['pieces']) - plen(pcs)) <= 1e-12 * max(1.0, plen(pcs))
            ok_join = True
            for pa, pb in zip(got['pieces'], got['pieces'][1:]):          # 이웃 조각 = 같은 점의 다른 상 (격자 벡터만큼) · 그 점은 면 위
                e, s_ = pa[-1], pb[0]
                dx, dy = e[0] - s_[0], e[1] - s_[1]
                lat = abs(dx - 20 * round(dx / 20)) < 1e-9 and abs(dy - 20 * round(dy / 20)) < 1e-9 and (round(dx / 20), round(dy / 20)) != (0, 0)
                face = min(abs(e[0] - x0), abs(e[0] - x0 - 20), abs(e[1] - y0), abs(e[1] - y0 - 20)) < 1e-9
                ok_join &= lat and face and abs(e[2] - s_[2]) < 1e-12
            if not (ok_in and ok_len and ok_join):
                bad_prop.append((k, ck, ok_in, ok_len, ok_join))
    chk('P6b 접기 = 파이썬 기준 구현 (조각 좌표 1e-12 · 자른 곳 수) — 경로 6 + 넓은 경로 × 셀 셋 (원래 · 옮긴 −1.44 · +2)', not bad_ref, repr(bad_ref)[:600])
    chk('P6c 접기 성질 — 모든 점이 닫힌 셀 안 · 길이 합 그대로 (자르기만) · 이웃 조각 = 같은 점의 다른 상 (격자 벡터) 이고 그 점은 면 위 (반 토막 · 긴 관 없음)',
        not bad_prop, repr(bad_prop)[:400])
    fx, fc = res['fold']['xwrap@c0'], res['fold']['corner@c0']
    chk('P6d 원래 셀 — x 면을 넘는 홉 = 두 조각 (x = 20 에서 끝 · x = 0 에서 시작) · 모서리 홉 = 세 조각 (x · y 면 차례로 · 자른 곳 2) · y > 20 인 점 없음',
        len(fx['pieces']) == 2 and abs(fx['pieces'][0][-1][0] - 20) < 1e-9 and abs(fx['pieces'][1][0][0]) < 1e-9 and fx['nCut'] == 1
        and len(fc['pieces']) == 3 and fc['nCut'] == 2 and abs(fc['pieces'][1][0][1]) < 1e-9 and abs(fc['pieces'][1][-1][0] - 20) < 1e-9
        and max(q[1] for pc in fc['pieces'] for q in pc) <= 20, repr((fx, fc))[:500])
    fw = res['fold']['wide@c2']
    chk('P6e 셀보다 넓은 경로 (x 폭 36) 를 셀 [2, 22) 에 = 두 조각 (x = 22 에서 잘라 x = 2 에서 잇는다) · 길이 그대로',
        len(fw['pieces']) == 2 and fw['nCut'] == 1 and abs(fw['pieces'][0][-1][0] - 22) < 1e-9 and abs(fw['pieces'][1][0][0] - 2) < 1e-9,
        repr(fw)[:400])
    edge_bad = [(i, g, e['want'], e['cut']) for i, (g, e) in enumerate(zip(res['foldEdge'], EDGE))
                if not (_pieces_close(g['pieces'], e['want'], 1e-9) and g['nCut'] == e['cut'])]
    chk('P6f 접기 가장자리 — 면에 닿고 돌아감 = 자르지 않음 · 정확한 모서리 (x · y 같은 t) = 한 번만 자름 · 면 위 꼭짓점에서 넘어감 = 그 점에서 · '
        '왼쪽으로 넘음 · 비주기 축 (L 0) 은 접지 않음', not edge_bad, repr(edge_bad)[:600])

    # ── 셀 맞춤 ──
    fa = res['fitAll']
    all_pcs = [ref_unw[k] for k in FIDS]
    (rsx, ro, ro0, rcl), (rsy, so, so0, scl) = ref_cell_fit(all_pcs)
    chk(f'P7 셀 맞춤 (경로 6) = 파이썬 기준 구현 — 옮김 ({fa["sx"]:.4f}, {fa["sy"]:.4f}) = ({rsx:.4f}, {rsy:.4f}) · 그 자리 밖 길이 0 · 옮기지 않으면 밖 길이 > 0 '
        f'(x {fa["outX0"]:.3f} · y {fa["outY0"]:.3f} µm) · 면 여유 ≥ 0.05 L',
        abs(fa['sx'] - rsx) < 1e-12 and abs(fa['sy'] - rsy) < 1e-12 and fa['outX'] <= 1e-9 and fa['outY'] <= 1e-9
        and fa['outX0'] > 0.01 and fa['outY0'] > 0.01 and abs(fa['outX0'] - ro0) < 1e-9 and abs(fa['outY0'] - so0) < 1e-9
        and fa['clearX'] >= VIEW_CLEAR * 20 and fa['clearY'] >= VIEW_CLEAR * 20 and abs(fa['x0'] - fa['sx']) < 1e-12 and fa['Lx'] == 20,
        repr(fa))
    ncut_fit = sum(ref_fold(pc, fa['x0'], fa['y0'], 20.0, 20.0)[1] for pc in all_pcs)
    chk('P7b 맞춘 셀에서는 접어도 자를 곳이 없다 (경로 6 개 모두 한 조각 — 셀 옮김이 목적을 이룬다 · 원래 셀은 3 곳)',
        ncut_fit == 0 and sum(ref_fold(pc, 0.0, 0.0, 20.0, 20.0)[1] for pc in all_pcs) == 3, f'{ncut_fit}')
    f2_ = res['fit2']
    chk('P7c 원래 셀에 여유 있게 다 들어가면 옮기지 않는다 (범위 #2 → 0 · 0)', f2_['sx'] == 0 and f2_['sy'] == 0 and f2_['outX'] == 0, repr(f2_))
    fw_ = res['fitWide']
    (wsx, wo, _wo0, _wcl), (wsy, _yo, _yo0, _ycl) = ref_cell_fit([ref_unw['wide']])
    chk(f'P7d 셀보다 넓은 경로 — 기준 구현과 같은 자리 (x +{fw_["sx"]:.2f} · y {fw_["sy"]:.2f}) · 밖 길이가 남는다 (접어야 한다) · 넓은 경로 1 개로 센다',
        abs(fw_['sx'] - wsx) < 1e-12 and abs(fw_['sy'] - wsy) < 1e-12 and fw_['outX'] > 1 and abs(fw_['outX'] - wo) < 1e-9 and fw_['nWideX'] == 1
        and fw_['nWideY'] == 0, repr(fw_))
    fn = res['fitNone']
    chk('P7e 경로가 없으면 옮기지 않는다', fn['sx'] == 0 and fn['sy'] == 0 and fn['outX'] == 0, repr(fn))
    bad_r, n_wide, n_shift = [], 0, 0
    for i, (ps, got) in enumerate(zip(RAND_SETS, res['fitRand'])):
        (rx, rox, rox0, _cx), (ry, roy, roy0, _cy) = ref_cell_fit(ps)
        tol = 1e-9 * (1 + rox0 + roy0)
        if not (abs(got['sx'] - rx) < 1e-12 and abs(got['sy'] - ry) < 1e-12 and abs(got['outX'] - rox) < tol and abs(got['outY'] - roy) < tol
                and abs(got['outX0'] - rox0) < tol and abs(got['outY0'] - roy0) < tol):
            bad_r.append((i, (got['sx'], got['sy'], got['outX'], got['outX0']), (rx, ry, rox, rox0)))
        n_wide += got['nWideX'] + got['nWideY']
        n_shift += (abs(got['sx']) > 0) + (abs(got['sy']) > 0)
    chk(f'P7f 무작위 대조 {len(RAND_SETS)} 묶음 (걸음 폭 1–9 µm · 셀보다 넓은 경로 {n_wide} · 좌표가 그대로인 홉 = 점 무게 · 끊긴 조각) — 뷰어 (누적 길이 표 · 이분 탐색) '
        f'= 파이썬 기준 (홉마다 자르기) : 자리 · 밖 길이 · 옮기지 않을 때 밖 길이 (옮긴 축 {n_shift})',
        not bad_r and n_wide > 0 and n_shift > 0, repr(bad_r)[:600])

    # ── 맥락 입자 접기 ──
    wp = res['wrap']
    x0, y0 = fa['x0'], fa['y0']
    orig = {p['id']: p for p in PARTICLES}
    ok_w = all(x0 <= x < x0 + 20 and y0 <= y < y0 + 20 and z == orig[i]['z'] for i, x, y, z in wp['pts'])
    ok_same = all(s == (x0 <= orig[i]['x'] < x0 + 20 and y0 <= orig[i]['y'] < y0 + 20) for (i, _x, _y, _z), s in zip(wp['pts'], wp['same']))
    ok_img = all(abs((x - orig[i]['x']) / 20 - round((x - orig[i]['x']) / 20)) < 1e-9 and abs((y - orig[i]['y']) / 20 - round((y - orig[i]['y']) / 20)) < 1e-9
                 for i, x, y, _z in wp['pts'])
    chk('P8 맥락 입자를 맞춘 셀 안으로 — x · y 가 반열린 셀 [x0, x0 + L) 안 · 원래 자리와 격자 벡터만큼 차이 · z 그대로 · 셀 안이던 입자는 같은 객체',
        ok_w and ok_same and ok_img and len(wp['pts']) == len(PARTICLES), repr(wp['pts'][:4]))
    wo_ = {i: (x, y) for i, x, y, _z in res['wrapOut']}
    chk('P8b 원래 셀 · 모두 안 = 같은 배열 (다시 짓지 않는다) · 셀 밖 중심 (20.3, −0.2) → (0.3, 19.8) · 원본 입자는 고치지 않는다',
        res['wrap0Same'] is True and abs(wo_[900][0] - 0.3) < 1e-9 and abs(wo_[900][1] - 19.8) < 1e-9 and res['wrapOrig'] == [20.3, -0.2],
        repr((res['wrap0Same'], wo_.get(900), res['wrapOrig'])))

    # ── PNG 맞춤 ──
    ff = res['ff']
    bad_ff = []
    m = VIEW_MARGIN
    c0 = FF[0]
    new0 = dict(c0['cam'], pos=ff[0]['pos'])
    n_before = ndc_max(c0['cam'], c0['target'], c0['pts'])
    n_after = ndc_max(new0, c0['target'], c0['pts'])
    d_old, d_new = _sub(c0['cam']['pos'], c0['target']), _sub(ff[0]['pos'], c0['target'])
    cosang = _dot(d_old, d_new) / math.sqrt(_dot(d_old, d_old) * _dot(d_new, d_new))
    if not (ff[0]['moved'] and n_before > 1 and n_after <= 1 - m + 1e-9 and n_after >= 1 - m - 1e-6 and cosang > 1 - 1e-12
            and abs(math.sqrt(_dot(d_new, d_new)) - ff[0]['dist']) < 1e-9 and ff[0]['dist'] > ff[0]['dist0']):
        bad_ff.append(('close', ff[0], n_before, n_after, cosang))
    chk(f'P9 PNG 맞춤 — 상자 안 가까운 시점 (꼭짓점이 뒤 · 화면 밖 = NDC {n_before}) → 시선 방향으로만 뒤로 ({ff[0]["dist0"]:.2f} → {ff[0]["dist"]:.2f}) · '
        f'파이썬 투영으로 모든 꼭짓점 |NDC| ≤ 1 − {m} (가장 바깥 = {n_after:.6f} · 딱 맞게)', not bad_ff, repr(bad_ff)[:500])
    c3 = FF[2]
    n3_ = ndc_max(dict(c3['cam'], pos=ff[2]['pos']), c3['target'], c3['pts'])
    chk('P9b 이미 다 보이면 움직이지 않는다 (당기지도 않는다) · 카메라 뒤의 점 → 앞으로 들도록 뒤로 · 위에서 똑바로 내려다봐도 (up ∥ 시선) 유한한 답',
        ff[1]['moved'] is False and ff[1]['pos'] == FF[1]['cam']['pos'] and ff[2]['moved'] is True and n3_ <= 1 - m + 1e-9
        and all(math.isfinite(v) for v in ff[3]['pos']) and ff[3]['dist'] >= ff[3]['dist0'], repr((ff[1], ff[2], ff[3]))[:500])

    # ── 정보 줄 ──
    pa_ = _plain(res['vAll']['infoCell'])
    chk('P10 정보 줄 (셀 옮김) — 경로 6 개 (범위의 경로 전부 · 다른 조합 없음) · "x·y 주기 단위 셀을 −1.44 µm · −1.44 µm 옮겨 그림 (같은 침대 · 같은 크기 — '
        '주기 경계라 동등)"',
        '경로 6 개 (범위의 경로 전부 · 다른 조합 없음)' in pa_
        and 'x·y 주기 단위 셀을 −1.44 µm · −1.44 µm 옮겨 그림 (같은 침대 · 같은 크기 — 주기 경계라 동등)' in pa_, pa_)
    chk('P10b 옮김 0 이면 셀 옮김 문구 없음 · 넓은 경로 = "셀에 다 담기지 않는 경로 1 개 = 면에서 잘라 반대 면으로" · +2.00 µm · 0 µm',
        '옮겨 그림' not in _plain(res['vAll']['infoCell0'])
        and '셀에 다 담기지 않는 경로 1 개 = 면에서 잘라 반대 면으로 이음 (1 곳 · 상자 안)' in _plain(res['vAll']['infoCellWide'])
        and 'x·y 주기 단위 셀을 +2.00 µm · 0 µm 옮겨 그림' in _plain(res['vAll']['infoCellWide']), _plain(res['vAll']['infoCellWide']))
    starts = {p['ids'][0] for p in PATHS0 + PATHS2}
    ends_ = {p['ids'][-1] for p in PATHS0 + PATHS2}
    t3_ids = [ids for _t, ids in sorted((p['tortuosity'], p['ids']) for p in PATHS0 + PATHS2)[:3]]
    chk(f'P10d 정보 줄 — 출발 (바닥) SE · 도착 (위) SE 의 서로 다른 수 (경로가 바닥 몇 점으로 모여 보이는 까닭 = 저장 표본 · 갱신이 바꾸지 못한다) — '
        f'전부 {len(starts)} → {len(ends_)} · τ 작은 셋 {len({i[0] for i in t3_ids})} → {len({i[-1] for i in t3_ids})}',
        f'출발 (바닥) SE {len(starts)} 개 → 도착 (위) SE {len(ends_)} 개' in pa_
        and f'출발 (바닥) SE {len({i[0] for i in t3_ids})} 개 → 도착 (위) SE {len({i[-1] for i in t3_ids})} 개' in _plain(v3['infoCell0']),
        pa_)
    pf, pu = _plain(res['vAll']['infoFold']), _plain(res['vAll']['infoUnwrap'])
    chk('P10c 원래 셀 (fold) = "주기 경계를 넘는 경로 2 개 = 면에서 잘라 반대 면으로 이음 (3 곳 · 상자 안)" · 이어 그림 = 상자 밖 안내 · τ 작은 순 = 금색 = 가장 작은 τ',
        '주기 경계를 넘는 경로 2 개 = 면에서 잘라 반대 면으로 이음 (3 곳 · 상자 안)' in pf and '상자 밖' in pu
        and '범위의 6 개 중 τ 작은 순' in _plain(v3['infoCell0']) and f'금색 = 가장 작은 τ ({ftau[0]:.2f} · 클러스터 #0)' in _plain(v3['infoCell0']),
        repr((pf, pu))[:500])


# ══════════════════════════════════════════════════════════════════════════════
#  [W] 2판 그림 창 — 조작을 실제로 누른다 (THREE 껍데기)
# ══════════════════════════════════════════════════════════════════════════════
W_RUN = r"""
(async () => {
const OUT = { err: null, snaps: {} };
try {
  const E = id => document.getElementById(id);
  const mkState = (cl, parts, opt) => { const idIndex = {}; parts.forEach(p => { idIndex[p.id] = p; });
    return { data: { particles: parts, box: BOX, clusters: { clusters: cl } }, idIndex,
             seParticles: parts.filter(p => p.type === 'SE'), amPParticles: parts.filter(p => p.type === 'AM_P'),
             amSParticles: parts.filter(p => p.type === 'AM_S'), amParticles: parts.filter(p => p.type !== 'SE'), _tauPathsOpt: Object.assign({}, opt) }; };
  const fireAsync = (id, type) => Promise.all((ELS[id] ? ELS[id].ls : []).filter(l => l[0] === type).map(l => l[1]({ type, target: ELS[id] })));
  const camOf = () => { const c = LOG.cams[LOG.cams.length - 1], t = LOG.ctrls[LOG.ctrls.length - 1];
    return { pos: [c.position.x, c.position.y, c.position.z], target: [t.target.x, t.target.y, t.target.z], up: [c.up.x, c.up.y, c.up.z],
             fov: c.fov, aspect: c.aspect, near: c.near }; };
  const snap = k => { OUT.snaps[k] = Object.assign(snapScene(LOG.scenes[LOG.scenes.length - 1]),
    { title: E('taup-m-title').textContent || '', info: E('taup-m-info').innerHTML || '', cam: camOf(), pick: E('taup-m-pick').value,
      scopeVal: E('taup-m-scope').value, nSaves: LOG.saves.length }); };
  const OPT0 = { scope: 'all', top: 0, seOpacity: 0.08, amOpacity: 0.12, width: 1, ends: true };
  const st = mkState(CL, PARTS, OPT0);
  showTauPathsView(st);
  OUT.html = LOG.overlay ? LOG.overlay.innerHTML : '';
  snap('open');
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 0 — 기본 시점
  const c = LOG.cams[LOG.cams.length - 1], t = LOG.ctrls[LOG.ctrls.length - 1];
  const p0 = c.position.clone();
  c.position.set(t.target.x + 2, t.target.y + 1.5, t.target.z + 2);                // 상자 안 가까운 시점 — 내용이 화면 밖
  OUT.closeCam = camOf();
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 1 — 맞춤 켬 (기본)
  OUT.afterClose = camOf();
  OUT.pngNote = E('taup-m-png-note').textContent || '';
  E('taup-m-fit').checked = false; fire('taup-m-fit', 'change');
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 2 — 맞춤 끔
  OUT.pngNoteOff = E('taup-m-png-note').textContent || '';
  E('taup-m-fit').checked = true; fire('taup-m-fit', 'change');
  c.position.copy(p0);
  E('taup-m-n').value = '3'; fire('taup-m-n', 'change'); snap('n3');
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 3 — τ 작은 3
  fire('taup-m-refresh', 'click'); snap('r1');
  E('taup-m-cbar-in').checked = true;
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 4 — 갱신 1 · 컬러바 넣기
  E('taup-m-cbar-in').checked = false;
  fire('taup-cbar-btn', 'click');
  fire('taup-m-refresh', 'click'); snap('r2');
  await fireAsync('taup-png-btn', 'click');                                       // 찍기 5 — 갱신 2
  E('taup-m-pick').value = 'tau'; fire('taup-m-pick', 'change'); snap('tau3');
  E('taup-m-scope').value = '2'; fire('taup-m-scope', 'change'); snap('scope2');
  E('taup-m-scope').value = 'all'; fire('taup-m-scope', 'change');
  E('taup-m-n').value = '0'; fire('taup-m-n', 'change'); snap('all');
  E('taup-m-bound').value = 'fold'; fire('taup-m-bound', 'change'); snap('fold');
  E('taup-m-bound').value = 'unwrap'; fire('taup-m-bound', 'change'); snap('unwrap');
  E('taup-m-bound').value = 'cell'; fire('taup-m-bound', 'change'); snap('cell2');
  E('taup-m-frame').checked = false; fire('taup-m-frame', 'change'); snap('noframe');
  E('taup-m-frame').checked = true; fire('taup-m-frame', 'change');
  OUT.optAfter = JSON.stringify(st._tauPathsOpt); OUT.optBefore = JSON.stringify(OPT0);
  OUT.saves = LOG.saves.map(s => s[1]); OUT.captures = LOG.captures.slice(); OUT.composite = LOG.composite.slice(); OUT.cbar = LOG.cbarExports.slice();
  //  없는 범위 (#7) 로 연 창 — 모든 관통 클러스터로 그리되 메인 옵션은 그대로
  const st2 = mkState(CL, PARTS, Object.assign({}, OPT0, { scope: '7' }));
  showTauPathsView(st2); snap('bad'); OUT.badOpt = st2._tauPathsOpt.scope;
  //  셀보다 넓은 경로 — 셀을 옮겨도 다 못 담는다 → 면에서 잘라 상자 안
  const st3 = mkState(CL_W, PARTS_W, OPT0);
  showTauPathsView(st3); snap('wide');
} catch (e) { OUT.err = String(e && e.stack || e); }
console.log(JSON.stringify(OUT));
})();
"""


def _decode(snap, pos_tol=1e-6):
    """그려진 경로 되읽기 (접어 자르지 않은 그림에서) — 경로 번호별 이음매 차례 → 맥락 SE (그린 셀로 접힌 자리) 의 id 차례 · 못 찾으면 None"""
    se = snap.get('se') or []
    by_k = {}
    for j in snap.get('joints') or []:
        by_k.setdefault(j[0], []).append((j[2], j[4], j[3]))              # three (x, y, z) → data (x, y_data = three z, z_data = three y)
    out = []
    for k in sorted(by_k):
        ids = []
        for x, y, z in by_k[k]:
            hit = [s[0] for s in se if abs(s[1] - x) < pos_tol and abs(s[2] - y) < pos_tol and abs(s[3] - z) < pos_tol]
            if len(hit) != 1:
                return None
            ids.append(hit[0])
        out.append(tuple(ids))
    return out


def _pts_data(snap):
    """그려진 점 전부 (data 좌표) — 이음매 · 끝점 · 원기둥 양 끝"""
    pts = [(j[2], j[4], j[3]) for j in snap.get('joints') or []]
    pts += [(e[1], e[3], e[2]) for e in snap.get('ends') or []]
    pts += [(p[0], p[2], p[1]) for p in snap.get('segEnds') or []]
    return pts


def _inside(pts, x0, y0, L=20.0, tol=1e-9):
    return all(x0 - tol <= x <= x0 + L + tol and y0 - tol <= y <= y0 + L + tol for x, y, _z in pts)


def _nseg(s):
    return s['kinds'].get('seg', 0) + s['kinds'].get('segBest', 0)


def _njoint(s):
    return s['kinds'].get('joint', 0) + s['kinds'].get('jointBest', 0)


def w_eval(res):
    """W 절 판정 — 이름 → (참 · 거짓, 덧말).  X 절 (변이) 이 같은 판정을 다시 쓴다."""
    R = {}
    S, html = res['snaps'], res.get('html') or ''
    taus = sorted([(p['tortuosity'], 0, i) for i, p in enumerate(PATHS0)] + [(p['tortuosity'], 2, i) for i, p in enumerate(PATHS2)])
    ids_of = {(0, i): tuple(p['ids']) for i, p in enumerate(PATHS0)}
    ids_of.update({(2, i): tuple(p['ids']) for i, p in enumerate(PATHS2)})
    all_ids = set(ids_of.values())
    tau3 = {ids_of[(c, i)] for _t, c, i in taus[:3]}
    unw = [ref_pieces(list(ids_of[(c, i)]), unwrap=True)[0] for _t, c, i in taus]
    (rsx, *_), (rsy, *_) = ref_cell_fit(unw)
    total_len = sum(plen(p) for p in unw)
    #  W1 — 조작
    opt_scope = re.search(r'<select id="taup-m-scope"[^>]*>(.*?)</select>', html, re.S)
    opt_n = re.search(r'<select id="taup-m-n"[^>]*>(.*?)</select>', html, re.S)
    opt_pick = re.search(r'<select id="taup-m-pick"[^>]*>(.*?)</select>', html, re.S)
    opt_bound = re.search(r'<select id="taup-m-bound"[^>]*>(.*?)</select>', html, re.S)
    ops = lambda m: re.findall(r'<option value="([^"]*)"( selected)?>([^<]*)</option>', m.group(1)) if m else []
    sc_, n_, pk_, bd_ = ops(opt_scope), ops(opt_n), ops(opt_pick), ops(opt_bound)
    R['W1 창 조작 — 범위 (모든 관통 클러스터 + 클러스터마다 · 메인 범례와 같은 이름) · 경로 수 [5 · 10 · 15 · 20 · 30 · 전부] (처음 = 메인 값 · 전부) · '
      '고르기 [τ 작은 순 · 무작위] · ↻ 갱신 (다른 경로) · 주기 경계 셋 (셀 옮김 기본) · PNG 잘림 없게 맞춤 (기본 켬)'] = (
        [(v, s_, t) for v, s_, t in sc_] == [('all', ' selected', '모든 관통 클러스터'), ('0', '', '클러스터 #0 (13 SE · 4 경로)'), ('2', '', '클러스터 #2 (5 SE · 2 경로)')]
        and [v for v, _s, _t in n_] == ['5', '10', '15', '20', '30', '0'] and [t for _v, s_, t in n_ if s_] == ['전부']
        and [(v, t) for v, _s, t in pk_] == [('tau', 'τ 작은 순'), ('rand', '무작위')] and [v for v, s_, _t in pk_ if s_] == ['tau']
        and [v for v, _s, _t in bd_] == ['cell', 'fold', 'unwrap'] and [v for v, s_, _t in bd_ if s_] == ['cell']
        and re.search(r'<button id="taup-m-refresh"[^>]*>↻ 갱신 \(다른 경로\)</button>', html) is not None
        and re.search(r'<input type="checkbox" id="taup-m-fit" checked>\s*PNG 잘림 없게 맞춤', html) is not None
        and 'id="taup-m-unwrap"' not in html, repr((sc_, n_, pk_, bd_))[:400])
    #  W2 — 기본 = 셀 옮김
    o = S['open']
    x0 = o['bbox']['c'][0] - 10 if o.get('bbox') else None
    y0 = o['bbox']['c'][2] - 10 if o.get('bbox') else None
    lab = (o.get('labels') or [None])[0] or {}
    R[f'W2 기본 (셀 옮김) — 상자 · 격자 · 축 글자 = 맞춘 셀 (x {um_txt(rsx)} · y {um_txt(rsy)} · 파이썬 기준과 같다) · 그린 점 (이음매 · 끝점 · 원기둥 양 끝) 전부 그 상자 안 · '
      '면에서 자른 곳 없음 (원기둥 16 · 이음매 22 · 끝점 12)'] = (
        x0 is not None and abs(x0 - rsx) < 1e-9 and abs(y0 - rsy) < 1e-9 and abs(rsx) > 0.5 and abs(rsy) > 0.5
        and o['bbox']['size'] == [20, 10, 20] and o['grid'] is not None and abs(o['grid'][0] - (rsx + 10)) < 1e-9 and abs(o['grid'][2] - (rsy + 10)) < 1e-9
        and abs(lab.get('x_min', 1e9) - rsx) < 1e-9 and abs(lab.get('y_max', 1e9) - (rsy + 20)) < 1e-9
        and _inside(_pts_data(o), rsx, rsy) and _nseg(o) == 16 and _njoint(o) == 22 and len(o['ends']) == 12,
        repr({'x0': x0, 'y0': y0, 'ref': (rsx, rsy), 'kinds': o['kinds'], 'lab': lab})[:400])
    pi_ = _plain(o['info'])
    R['W2b 정보 줄이 셀 옮김을 말한다 — "x·y 주기 단위 셀을 … µm · … µm 옮겨 그림 (같은 침대 · 같은 크기 — 주기 경계라 동등)" (값 = 그린 셀)'] = (
        f'x·y 주기 단위 셀을 {um_txt(rsx)} · {um_txt(rsy)} 옮겨 그림 (같은 침대 · 같은 크기 — 주기 경계라 동등)' in pi_
        and '경로 6 개 (범위의 경로 전부 · 다른 조합 없음)' in pi_, pi_)
    se_ = o.get('se') or []
    dec = _decode(o)
    R['W2c 맥락 SE = 그 셀 안으로 접힌 자리 (반열린 셀) · 경로 이음매 = 접힌 SE 중심 그대로 (관이 입자를 꿴다) · 그려진 경로 = 저장 경로 6 개'] = (
        len(se_) == len(P) and all(rsx <= s[1] < rsx + 20 and rsy <= s[2] < rsy + 20 for s in se_)
        and dec is not None and set(dec) == all_ids and len(dec) == 6, repr(dec)[:300])
    R['W2d 시점 = 그린 셀 기준 (주시점 = 상자 가운데 — 셀을 옮긴 만큼 시점도 옮겨 상자가 창에서 제자리)'] = (
        _close(o['cam']['target'], [rsx + 10, 5, rsy + 10], 1e-9), repr(o['cam']))
    #  W3 — PNG 맞춤
    cap = res.get('captures') or []
    m = VIEW_MARGIN
    ok3 = len(cap) >= 3
    if ok3:
        c0_, c1_, c2_ = cap[0], cap[1], cap[2]
        n0 = ndc_max(c0_['cam'], c0_['target'], c0_['content'])
        nb = ndc_max(dict(res['closeCam']), res['closeCam']['target'], c1_['content'])
        n1 = ndc_max(c1_['cam'], c1_['target'], c1_['content'])
        n2 = ndc_max(c2_['cam'], c2_['target'], c2_['content'])
        d_old = _sub(res['closeCam']['pos'], res['closeCam']['target'])
        d_new = _sub(c1_['cam']['pos'], c1_['target'])
        cosang = _dot(d_old, d_new) / math.sqrt(_dot(d_old, d_old) * _dot(d_new, d_new))
        R['W3a PNG (기본 시점) — 상자 꼭짓점 · 경로 · 끝점이 모두 화면 안 (|NDC| ≤ 1 − 0.04 · 파이썬 투영)'] = (n0 <= 1 - m + 1e-9, f'{n0}')
        R['W3b PNG 맞춤 — 상자 안 가까운 시점 (내용이 화면 밖) 에서 눌러도 시선 방향으로만 뒤로 물러나 찍는다 → 모두 화면 안 (|NDC| ≤ 1 − 0.04) · '
          '찍은 뒤 시점 그대로 · 안내 ("배 멀리서")'] = (
            nb > 1 and n1 <= 1 - m + 1e-9 and cosang > 1 - 1e-9 and math.sqrt(_dot(d_new, d_new)) > math.sqrt(_dot(d_old, d_old))
            and _close(c1_['target'], res['closeCam']['target'], 0) and res['afterClose']['pos'] == res['closeCam']['pos']
            and '배 멀리서' in (res.get('pngNote') or ''), f'before {nb} · capture {n1} · cos {cosang} · note {res.get("pngNote")!r}')
        R['W3c "PNG 잘림 없게 맞춤" 끔 = 화면 시점 그대로 찍는다 (같은 가까운 시점 → 잘린다 · 안내가 그렇다고 말한다)'] = (
            c2_['cam']['pos'] == res['closeCam']['pos'] and n2 > 1 and '맞춤 끔' in (res.get('pngNoteOff') or ''), f'{n2} · {res.get("pngNoteOff")!r}')
    else:
        for k in ('W3a PNG (기본 시점) — 상자 꼭짓점 · 경로 · 끝점이 모두 화면 안 (|NDC| ≤ 1 − 0.04 · 파이썬 투영)',
                  'W3b PNG 맞춤 — 상자 안 가까운 시점 (내용이 화면 밖) 에서 눌러도 시선 방향으로만 뒤로 물러나 찍는다 → 모두 화면 안 (|NDC| ≤ 1 − 0.04) · '
                  '찍은 뒤 시점 그대로 · 안내 ("배 멀리서")',
                  'W3c "PNG 잘림 없게 맞춤" 끔 = 화면 시점 그대로 찍는다 (같은 가까운 시점 → 잘린다 · 안내가 그렇다고 말한다)'):
            R[k] = (False, f'찍기 {len(cap)} 번')
    #  W4 — 경로 수 3 (τ 작은 순)
    n3 = S['n3']
    d3 = _decode(n3)
    saves = res.get('saves') or []
    lo3, hi3 = taus[0][0], taus[2][0]
    R[f'W4 경로 수 3 (창 안에서 · 다시 열지 않고) — 그려진 경로 = τ 작은 셋 · 머리 "3 개" · 정보 줄 "경로 3 개 (범위의 6 개 중 τ 작은 순)" · τ {lo3:.2f} – {hi3:.2f} · '
      'PNG 이름 n3 (무작위 표지 없음)'] = (
        d3 is not None and set(d3) == tau3 and '— 3 개' in n3['title'] and '경로 3 개 (범위의 6 개 중 τ 작은 순)' in _plain(n3['info'])
        and f'τ {lo3:.2f} – {hi3:.2f}' in _plain(n3['info']) and len(saves) > 3 and saves[3] == f'tau_paths_n3_tau{lo3:.2f}-{hi3:.2f}.png',
        repr((d3, n3['title'], _plain(n3['info'])[:200], saves[3:4])))
    #  W5 — 갱신
    r1, r2 = S['r1'], S['r2']
    d1, d2 = _decode(r1), _decode(r2)
    m1 = re.search(r'무작위 · seed (\d+)', _plain(r1['info']))
    m2 = re.search(r'무작위 · seed (\d+)', _plain(r2['info']))
    s1, s2 = (int(m1.group(1)) if m1 else None), (int(m2.group(1)) if m2 else None)
    comp = res.get('composite') or []
    cb = res.get('cbar') or []
    R['W5 ↻ 갱신 1 (τ 작은 순에서) = 고르기가 무작위로 · 다른 세 경로 (그 자리에서) · 머리 "3 개" · 정보 줄 seed · 금색 = 이 그림 안에서 가장 작은 τ · '
      'PNG 이름 _rand<seed> · 컬러바 넣은 합성본 = 그 집합의 스펙'] = (
        r1['pick'] == 'rand' and d1 is not None and len(d1) == 3 and set(d1) <= all_ids and set(d1) != set(d3 or ()) and s1 is not None
        and '— 3 개' in r1['title'] and '금색 = 이 그림 안에서 가장 작은 τ' in _plain(r1['info'])
        and len(saves) > 4 and saves[4].startswith('tau_paths_n3_tau') and saves[4].endswith(f'_rand{s1}.png')
        and len(comp) >= 1 and f'3 of 6 stored candidate paths (random subset, seed {s1})' in (comp[-1][2] or ''),
        repr((r1['pick'], d1, s1, saves[4:5], comp[-1:]))[:500])
    R['W5b ↻ 갱신 2 = 또 다른 집합 · 다른 seed · 다른 PNG 이름 (덮어쓰지 않는다) · 컬러바 PNG 단추도 그때의 집합 스펙'] = (
        d2 is not None and len(d2) == 3 and d1 is not None and set(d2) != set(d1) and s2 is not None and s1 is not None and s2 != s1
        and len(saves) > 5 and saves[5].endswith(f'_rand{s2}.png') and saves[5] != saves[4]
        and len(cb) >= 1 and f'seed {s1}' in (cb[-1][2] or ''), repr((d1, d2, s1, s2, saves[4:6], cb[-1:]))[:500])
    t3s = S['tau3']
    R['W5c 고르기 = τ 작은 순 으로 되돌리면 τ 작은 세 경로 · 정보 줄 "τ 작은 순"'] = (
        _decode(t3s) is not None and set(_decode(t3s)) == tau3 and '범위의 6 개 중 τ 작은 순' in _plain(t3s['info']), _plain(t3s['info'])[:200])
    #  W6 — 범위 #2
    s2_ = S['scope2']
    ds2 = _decode(s2_)
    R['W6 범위 = 클러스터 #2 → 그 경로 둘 (경로 수 3 ≥ 2 = 경로 전부 · 다른 조합 없음) · 머리 "2 개" · 그 둘은 원래 셀에 여유 있게 들어가 셀을 옮기지 않는다 (상자 = 원래 자리)'] = (
        ds2 is not None and set(ds2) == {ids_of[(2, 0)], ids_of[(2, 1)]} and '— 2 개' in s2_['title']
        and '범위의 경로 전부 · 다른 조합 없음' in _plain(s2_['info']) and '옮겨 그림' not in _plain(s2_['info'])
        and s2_['bbox'] is not None and _close(s2_['bbox']['c'], [10, 5, 10], 1e-9) and s2_['scopeVal'] == '2', repr((ds2, s2_['title'], s2_.get('bbox'))))
    #  W7 — 원래 셀 · 면에서 자름
    f_ = S['fold']
    pts_f = _pts_data(f_)
    xs, ys = [p[0] for p in pts_f], [p[1] for p in pts_f]
    R['W7 주기 경계 = 원래 셀 (fold) — 점 전부 원래 상자 [0, 20]² 안 (반 토막이 밖으로 나오지 않는다) · 넘는 홉 = 면에서 정확히 잘라 반대 면 (자른 곳 3 → 원기둥 19 · 이음매 28) · '
      '면 위 점 (x 0 · 20 · y 0 · 20) · 상자 · 시점 = 원래 자리 · 정보 줄 "면에서 잘라 반대 면"'] = (
        _inside(pts_f, 0.0, 0.0) and _nseg(f_) == 19 and _njoint(f_) == 28
        and min(abs(x - 20) for x in xs) < 1e-9 and min(abs(x) for x in xs) < 1e-9 and min(abs(y) for y in ys) < 1e-9 and min(abs(y - 20) for y in ys) < 1e-9
        and f_['bbox'] is not None and _close(f_['bbox']['c'], [10, 5, 10], 1e-9) and _close(f_['cam']['target'], [10, 5, 10], 1e-9)
        and '면에서 잘라 반대 면으로 이음 (3 곳 · 상자 안)' in _plain(f_['info']),
        repr({'kinds': f_['kinds'], 'max_y': max(ys) if ys else None, 'bbox': f_.get('bbox')})[:400])
    u_ = S['unwrap']
    pts_u = _pts_data(u_)
    R['W8 주기 경계 = 이어 그림 (옛 펼침) — 원기둥 16 · 상자 밖으로 나간다 (허용) · 정보 줄이 그렇다고 말한다 · 상자 = 원래 자리'] = (
        _nseg(u_) == 16 and max(max(p[0], p[1]) for p in pts_u) > 20 + 1e-6 and '상자 밖' in _plain(u_['info'])
        and u_['bbox'] is not None and _close(u_['bbox']['c'], [10, 5, 10], 1e-9), repr(u_['kinds']))
    lens = {k: S[k]['segLen'] for k in ('all', 'fold', 'unwrap', 'cell2')}
    taus_txt = {k: re.search(r'τ (\d\.\d\d) – (\d\.\d\d)', _plain(S[k]['info'])) for k in lens}
    R[f'W9 그림만 다르다 — 그린 관 길이 합 (셀 옮김 · 원래 셀 · 이어 그림) = 저장 경로 길이 합 ({total_len:.4f} µm) · τ 범위 문구 같다'] = (
        all(abs(v - total_len) < 1e-9 * total_len for v in lens.values()) and all(taus_txt.values())
        and len({(t.group(1), t.group(2)) for t in taus_txt.values()}) == 1, repr(lens))
    c2s = S['cell2']
    R['W9b 다시 셀 옮김 = 처음과 같은 셀 · 같은 관 · 같은 시점'] = (
        c2s['bbox'] is not None and o['bbox'] is not None and _close(c2s['bbox']['c'], o['bbox']['c'], 1e-9) and c2s['kinds'] == o['kinds']
        and _close(c2s['cam']['target'], o['cam']['target'], 1e-9), repr((c2s.get('bbox'), o.get('bbox'))))
    nf = S['noframe']
    R['W9c 상자 · 바닥 격자 끔 = 상자 안 보임 (PNG 맞춤도 상자 꼭짓점을 빼고 셈)'] = (nf['bbox'] is not None and nf['bbox']['visible'] is False, repr(nf.get('bbox')))
    #  W10 — 창 상태는 창 안에서만
    bd = _decode(S['bad'])
    R['W10 창은 메인 옵션 객체를 고치지 않는다 (조작 전부 뒤 그대로) · 없는 범위 (#7) 로 열어도 창 안에서만 모든 관통 클러스터 (메인 옵션 #7 그대로)'] = (
        res.get('optAfter') == res.get('optBefore') and res.get('badOpt') == '7' and bd is not None and set(bd) == all_ids,
        repr((res.get('optAfter'), res.get('badOpt'))))
    #  W11 — 셀보다 넓은 경로
    w = S['wide']
    (wsx, *_), (wsy, *_) = ref_cell_fit([ref_pieces(PATH_WIDE['ids'], unwrap=True, idx=P_WIDE)[0]])
    wl = plen(ref_pieces(PATH_WIDE['ids'], unwrap=True, idx=P_WIDE)[0])
    R[f'W11 셀보다 넓은 경로 (x 폭 36 > 20) — 셀 (x {um_txt(wsx)} · y {um_txt(wsy)}) 을 맞춰도 다 못 담아 면에서 잘라 반대 면 (자른 곳 1 → 원기둥 7 · 이음매 9) · '
      '점 전부 그 상자 안 · 길이 그대로 · 정보 줄 "셀에 다 담기지 않는 경로 1 개"'] = (
        w['bbox'] is not None and abs(w['bbox']['c'][0] - 10 - wsx) < 1e-9 and abs(w['bbox']['c'][2] - 10 - wsy) < 1e-9
        and _inside(_pts_data(w), wsx, wsy) and _nseg(w) == 7 and _njoint(w) == 9 and abs(w['segLen'] - wl) < 1e-9 * wl
        and '셀에 다 담기지 않는 경로 1 개 = 면에서 잘라 반대 면으로 이음 (1 곳 · 상자 안)' in _plain(w['info'])
        and f'x·y 주기 단위 셀을 {um_txt(wsx)} · {um_txt(wsy)} 옮겨 그림' in _plain(w['info']),
        repr({'bbox': w.get('bbox'), 'kinds': w['kinds'], 'info': _plain(w['info'])[-200:]}))
    return R


def run_window(js_src_override=None, js=None):
    """W 장면을 돌린다 — js_src_override = 변이한 뷰어 소스 묶음 (X 절) · 없으면 viewer3d.js 에서 잘라 쓴다"""
    if js_src_override is None:
        src, miss = fns(js, RENDER_FNS + ('showTauPathsView',))
        vsrc, _vm = view_src(js)
        cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
        lc = line_consts(js, LINE_CONST_RE)
        if miss or miss_c or len(lc) != 4:
            return None, f'없음 {miss + miss_c}'
        body = cs + '\n' + '\n'.join(lc) + '\n' + vsrc + '\n' + src
    else:
        body = js_src_override
    rr = run_node(M_SHIM + body + '\nconst CL = ' + json.dumps(CLUSTERS) + ';\nconst PARTS = ' + json.dumps(PARTICLES)
                  + ';\nconst BOX = ' + json.dumps(BOX) + ';\nconst CL_W = ' + json.dumps(CL_WIDE) + ';\nconst PARTS_W = ' + json.dumps(PARTS_WIDE)
                  + ';\n' + W_RUN)
    return rr, (rr.get('err') if rr else 'node 실패')


def section_view_window(js):
    print('[W] 2판 그림 창 — 고르기 · 갱신 · 주기 경계 · PNG 맞춤 (조작을 실제로 누른다)')
    if not shutil.which('node'):
        chk('W0 node 필요', False, 'node 미설치')
        return
    rr, err = run_window(js=js)
    if not chk('W0 node 실행 (showTauPathsView · 조작 사건 · PNG 셋 · 창 셋)', rr is not None and rr.get('err') is None, repr(err)[:900]):
        return
    for name, (ok, extra) in w_eval(rr).items():
        chk(name, ok, extra)


# ══════════════════════════════════════════════════════════════════════════════
#  [X] 변이 — 위 시험이 결함을 잡는가 (판별력)
# ══════════════════════════════════════════════════════════════════════════════
#  (이름, 바꿀 자리 [(옛 글자, 새 글자)], FAIL 해야 할 W 시험 머리)
MUTANTS = [
    ('X1 셀 옮김 끔 (셀 맞춤이 늘 0 을 돌려줌)', [('const s = pick.s > L / 2 ? pick.s - L : pick.s;', 'const s = 0;')], ('W2 ', 'W2b ')),
    ('X2 접기 = 옛 반 토막 (면에서 자르지 않고 최소상 변위의 절반)', [('!!(o.unwrap || o.cell)', '!!o.unwrap'), ('if (o.cell) {', 'if (false) {')], ('W7 ',)),
    ('X3 무작위가 seed 를 무시 (늘 같은 수열)', [('const rnd = tauPathsRng(sd);', 'const rnd = tauPathsRng(1);')], ('W5b ',)),
    ('X4 PNG 맞춤 끔 (화면 시점 그대로 찍음 — 공용 figCapturePNG)', [('if (wantFit) {', 'if (false) {')], ('W3b ',)),
    ('X5 셀 맞춤 뒤 접기 생략 (이어 그린 조각 그대로)', [('pieces = fp.pieces;', '')], ('W11 ', 'W2 ')),
]


def mutate(src, pairs):
    """변이 — (옛 글자, 새 글자) 를 차례로 한 번씩.  자리가 없으면 None (변이 검사가 조용히 통과하지 않게 FAIL 로)"""
    for old, new in pairs:
        if old not in src:
            return None
        src = src.replace(old, new, 1)
    return src


def section_view_mutation(js):
    print('[X] 변이 — 시험의 판별력 (변이한 뷰어에서 해당 W 시험이 FAIL 해야 한다)')
    if not shutil.which('node'):
        chk('X0 node 필요', False, 'node 미설치')
        return
    src, miss = fns(js, RENDER_FNS + ('showTauPathsView',))
    vsrc, vmiss = view_src(js)
    cs, miss_c = consts(js, ('COL', 'TAUP_DEFAULT_OPT'))
    lc = line_consts(js, LINE_CONST_RE)
    if not chk('X0 2판 그림 창 도우미가 있다 (변이 대상)', not miss and not vmiss and not miss_c and len(lc) == 4, f'없음 {miss + vmiss + miss_c}'):
        return
    body = cs + '\n' + '\n'.join(lc) + '\n' + vsrc + '\n' + src
    for name, pairs, targets in MUTANTS:
        mb = mutate(body, pairs)
        if mb is None:
            chk(f'{name} → 변이 자리를 찾지 못했다 (코드가 바뀌었으면 변이도 고칠 것)', False, repr([p[0] for p in pairs]))
            continue
        rr, err = run_window(js_src_override=mb)
        if rr is None or rr.get('err'):
            chk(f'{name} → 변이한 뷰어가 멈추지 않고 돈다 (그림이 틀려야지 죽으면 안 된다)', False, repr(err)[:400])
            continue
        ev = w_eval(rr)
        hit = {k.split(' ')[0]: ok for k, (ok, _x) in ev.items() if any(k.startswith(t) for t in targets)}
        n_other = sum(1 for k, (ok, _x) in ev.items() if not ok and k.split(' ')[0] not in hit)
        chk(f'{name} → {" · ".join(t.strip() for t in targets)} 가 FAIL 한다 ({hit} · 다른 W 시험 FAIL {n_other})',
            len(hit) == len(targets) and not any(hit.values()))


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
    section_view_pure(js)
    section_view_window(js)
    section_view_mutation(js)
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
