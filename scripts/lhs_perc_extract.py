#!/usr/bin/env python3
"""AM 접촉 그래프의 z-퍼콜레이션 판정 — LHS 확장의 **1차 관측량** `perc_i`.

    python3 scripts/lhs_perc_extract.py --dump post_lhs00_000/atom_2425000.liggghts \\
                                        --n-types 3 --case lhs00_000
    python3 scripts/lhs_perc_extract.py --batch post_root --n-types-from design.csv
    python3 scripts/lhs_perc_extract.py --selftest

사전등록 `docs/reviews/lhs_extension_prereg_v2_20260829.md` §4-1 이 규약을 적고, 같은 절이
**"아직 구현으로 봉인되지 않은 것"** 다섯 개를 이름으로 남겼다.  이 파일이 그 봉인이다 —
Codex R11 B1: *"추출기와 경계 fixture 를 결과 전에 커밋해야 이 규약이 실재한다."*

═══ 봉인되는 규약 ═══

**① 그래프**.  노드 = AM 입자.  간선 = **표면 간극 ≤ 0** 인 쌍, 즉
`d_ij ≤ r_i + r_j`.  tolerance 는 **정확히 0** 이고 등호는 **접촉으로** 센다
(부동소수 여유를 두지 않는다 — 두면 그 여유가 새 자유도가 된다).

**② AM_P ↔ AM_S 간선은 허용한다.**  전자 backbone 은 AM **상(phase)** 이지 크기 계급이
아니다.  기존 코퍼스의 `f_perc_x_AM` 도 AM 을 한 상으로 본다.  ⇒ 3-type 침대에서 type 1·2
는 **한 노드 집합**이다.

**③ 경계**.  x·y **주기** (minimum image, 상자 길이는 덤프의 `ITEM: BOX BOUNDS` 에서
읽는다) · z **개방** (감싸지 않는다).  덤프 헤더의 경계 플래그가 `pp pp ff` 계열이 아니면
**거부한다** — 규약과 파일이 어긋난 채로 숫자를 내지 않는다.

**④ 슬래브 기준면** = **고체 전체(AM ∪ SE)의 z 범위**:
`z_lo = min(z_i − r_i)` · `z_hi = max(z_i + r_i)`, 두 극값 모두 **모든** 입자에 대해.
슬래브 두께 `t = r_AM,max` (그 침대 AM 반지름의 최댓값).
아래 슬래브 = `z_i − r_i ≤ z_lo + t` · 위 슬래브 = `z_i + r_i ≥ z_hi − t`.
둘 중 하나라도 **비면 `perc = 0`** (사전등록 그대로).

  ⚠ 왜 AM 만의 범위를 쓰지 않나 — 그러면 AM 이 희박한 침대일수록 슬래브가 **있는 AM 위로
  움츠러들어** 판정이 쉬워진다.  즉 문턱 근처에서 1차 관측량이 **가설 방향으로 편향**된다.
  ⚠ 왜 상자 경계(`zlo/zhi`)를 쓰지 않나 — LIGGGHTS 상자는 플래튼 행정을 담느라 압밀된
  침대보다 훨씬 높다.  그 안에서는 어떤 침대도 위 슬래브에 닿지 않는다.

**⑤ 좌표·반지름 출처** = 그 런의 **마지막** 압밀 후 원자 덤프
(`post_*/atom_<최대 step>.liggghts`) 의 `x y z radius type` 열.  파생 CSV 나 metrics JSON
을 읽지 않는다 — 중간 산물은 규약이 다시 개입할 자리다.

**⑥ 상 사상**.  `--n-types` 는 **필수**다.  자동 추론을 **거부**하는 이유: 3-type 침대의
AM_P 가 우연히 0개면 존재 type 이 둘이라 2-type 으로 보이고, 그때 type 2(AM_S)가 SE 로
오사상돼 **AM 전체가 사라진다**.  fail-closed 로 막는다.
  · `--n-types 2` → {1: AM, 2: SE}
  · `--n-types 3` → {1: AM_P, 2: AM_S, 3: SE}
파일에 선언 밖 type 이 있으면 거부한다.

═══ σ_e 는 여기 없다 ═══

`perc_i` 는 **이 그래프 하나로만** 정한다 (사전등록 §4-1, Codex R11 B1).  σ_e 영점 규칙은
secondary diagnostic 이라 **다른 도구**가 낸다.  이 스크립트는 σ_e 를 읽지도 않는다 —
읽으면 둘이 갈릴 때 사후에 고를 여지가 생긴다.

═══ 부수 산출 ═══

`phi_AM_solid_measured` = `ΣV_AM / (ΣV_AM + ΣV_SE)` — 설계 CSV 의 `phi_AM`
(= `2000w/(4800−2800w)`, w = AM 질량분율) 과 **같은 정의**라 대조할 수 있다.
⚠ 적합에 쓰는 φ 는 사전등록이 정한 설계값이다.  이 측정값은 **대조용**이고, 어긋나면
그 사실을 보고한다 (사후에 어느 쪽을 쓸지 고르지 않는다).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

import numpy as np

CHI2_1DOF_95 = 3.841458820694124  # (fitter 와 공유하지 않는다 — 여기선 안 쓴다)

#: 상 사상.  ⑥ 참조 — 자동 추론은 거부한다.
TYPE_MAP = {
    2: {1: 'AM', 2: 'SE'},
    3: {1: 'AM_P', 2: 'AM_S', 3: 'SE'},
}

#: ② AM 으로 보는 라벨.  AM_P 와 AM_S 는 **한 노드 집합**이다.
AM_LABELS = frozenset({'AM', 'AM_P', 'AM_S'})

#: ③ 요구하는 경계 플래그 (x, y, z).
REQUIRED_BC = ('pp', 'pp', 'ff')


class BedRefusal(RuntimeError):
    """규약과 파일이 어긋났다 — 숫자를 내지 않고 멈춘다."""


# ──────────────────────────────────────────────────────────────────────────────
# 덤프 읽기
# ──────────────────────────────────────────────────────────────────────────────
def read_atom_dump(path):
    """마지막 프레임의 `x y z radius type` + 상자 경계·플래그를 돌려준다.

    ⚠ 여러 프레임이 있으면 **마지막** 것을 쓴다 (⑤: 압밀 후 상태).
    """
    with open(path, 'r', encoding='utf-8', errors='replace') as fh:
        lines = fh.read().splitlines()

    frames = [i for i, ln in enumerate(lines) if ln.startswith('ITEM: TIMESTEP')]
    if not frames:
        raise BedRefusal(f'{path}: `ITEM: TIMESTEP` 이 없다 — LIGGGHTS 원자 덤프가 아니다')
    start = frames[-1]

    box_lo, box_hi, bc = [], [], None
    headers, rows = None, []
    i = start
    while i < len(lines):
        ln = lines[i].strip()
        if ln.startswith('ITEM: BOX BOUNDS'):
            flags = ln.replace('ITEM: BOX BOUNDS', '').strip().split()
            # `xy xz yz pp pp pp` 처럼 tilt 접두가 붙을 수 있다 → 뒤 3개만 본다.
            bc = tuple(flags[-3:]) if len(flags) >= 3 else None
            for k in range(3):
                parts = lines[i + 1 + k].split()
                box_lo.append(float(parts[0]))
                box_hi.append(float(parts[1]))
            i += 4
            continue
        if ln.startswith('ITEM: ATOMS'):
            headers = ln.replace('ITEM: ATOMS', '').strip().split()
            i += 1
            while i < len(lines) and not lines[i].startswith('ITEM:'):
                vals = lines[i].split()
                if len(vals) == len(headers):
                    rows.append(vals)
                i += 1
            continue
        i += 1

    if headers is None:
        raise BedRefusal(f'{path}: `ITEM: ATOMS` 이 없다')
    if len(box_lo) != 3:
        raise BedRefusal(f'{path}: `ITEM: BOX BOUNDS` 를 못 읽었다 — 주기 상자 길이가 없으면 '
                         'minimum image 를 규약대로 못 쓴다')
    need = ('x', 'y', 'z', 'radius', 'type')
    missing = [c for c in need if c not in headers]
    if missing:
        raise BedRefusal(f'{path}: 열 부재 {missing} (있는 열: {headers})')
    if not rows:
        raise BedRefusal(f'{path}: 마지막 프레임에 입자가 0개다')

    idx = {c: headers.index(c) for c in need}
    arr = np.asarray(rows, dtype=object)
    out = {c: np.asarray([float(r[idx[c]]) for r in rows], dtype=np.float64) for c in need}
    out['type'] = out['type'].astype(np.int64)
    del arr
    return out, np.asarray(box_lo), np.asarray(box_hi), bc


def check_boundary_flags(bc, allow_any):
    if allow_any:
        return f'경계 플래그 검사 우회 (--allow-any-bc): {bc}'
    if bc is None:
        raise BedRefusal('BOX BOUNDS 에 경계 플래그가 없다 — 규약(③ pp pp ff)을 확인할 수 없다')
    if tuple(bc) != REQUIRED_BC:
        raise BedRefusal(f'경계 플래그 {tuple(bc)} 가 규약 {REQUIRED_BC} 와 다르다.  '
                         '규약과 파일이 어긋난 채로 판정하지 않는다')
    return f'경계 플래그 {tuple(bc)} = 규약'


# ──────────────────────────────────────────────────────────────────────────────
# 그래프
# ──────────────────────────────────────────────────────────────────────────────
def _pairs_within(xyz, radii, lx, ly, z_pad):
    """`d_ij <= r_i + r_j` 인 쌍 (i<j).  xy 주기 · z 개방.

    xy 는 cKDTree 의 `boxsize` 로 감싸고, z 는 **감싸지 않게** 하려고 실제 두께보다 훨씬 큰
    가상 주기를 준 뒤 좌표를 그 안 가운데로 옮긴다 (감쌈 거리가 두께보다 크므로 절대 안 만난다).
    반지름이 두 계급이면 `r_i + r_j` 가 쌍마다 달라 **계급별로** 질의한다 — 전역 최대
    cutoff 를 쓰면 후보가 폭증한다.
    """
    from scipy.spatial import cKDTree

    n = len(radii)
    if n < 2:
        return np.empty((0, 2), dtype=np.int64)

    z = xyz[:, 2].copy()
    zspan = float(z.max() - z.min()) if n else 0.0
    zbig = 3.0 * (zspan + 2.0 * float(radii.max()) + z_pad + 1.0)
    pts = np.empty_like(xyz)
    pts[:, 0] = np.mod(xyz[:, 0], lx)
    pts[:, 1] = np.mod(xyz[:, 1], ly)
    pts[:, 2] = z - z.min() + zbig / 3.0
    boxsize = np.array([lx, ly, zbig])

    # 반지름 계급 (부동소수 잡음 제거).
    key = np.round(radii, 12)
    classes = np.unique(key)
    groups = [np.flatnonzero(key == c) for c in classes]
    trees = [cKDTree(pts[g], boxsize=boxsize) for g in groups]

    out = []
    for a in range(len(groups)):
        for b in range(a, len(groups)):
            cut = float(classes[a] + classes[b])
            if a == b:
                pr = trees[a].query_pairs(r=cut, output_type='ndarray')
                if len(pr):
                    out.append(np.column_stack([groups[a][pr[:, 0]], groups[a][pr[:, 1]]]))
            else:
                nb = trees[a].query_ball_tree(trees[b], r=cut)
                ii, jj = [], []
                for li, lst in enumerate(nb):
                    for lj in lst:
                        ii.append(groups[a][li])
                        jj.append(groups[b][lj])
                if ii:
                    out.append(np.column_stack([np.asarray(ii), np.asarray(jj)]))
    if not out:
        return np.empty((0, 2), dtype=np.int64)
    pairs = np.vstack(out)

    # 정확한 재검사 — KD-tree 의 cutoff 는 계급 최대치라 계급 안에서도 느슨할 수 있다.
    d = pts[pairs[:, 0]] - pts[pairs[:, 1]]
    d[:, 0] -= lx * np.round(d[:, 0] / lx)
    d[:, 1] -= ly * np.round(d[:, 1] / ly)
    dist = np.sqrt((d ** 2).sum(axis=1))
    keep = dist <= (radii[pairs[:, 0]] + radii[pairs[:, 1]])   # ① 등호는 접촉
    pairs = pairs[keep]
    lo = np.minimum(pairs[:, 0], pairs[:, 1])
    hi = np.maximum(pairs[:, 0], pairs[:, 1])
    pairs = np.unique(np.column_stack([lo, hi]), axis=0)
    return pairs


def percolation(atoms, box_lo, box_hi, n_types):
    """규약 ①~⑥ 대로 `perc` 를 낸다.  → dict"""
    tmap = TYPE_MAP.get(int(n_types))
    if tmap is None:
        raise BedRefusal(f'--n-types {n_types} 는 규약에 없다 (2 또는 3)')
    seen = set(np.unique(atoms['type']).tolist())
    unknown = sorted(seen - set(tmap))
    if unknown:
        raise BedRefusal(f'선언 밖 type {unknown} 이 덤프에 있다 (--n-types {n_types} → {tmap})')

    lab = np.array([tmap[int(t)] for t in atoms['type']])
    is_am = np.isin(lab, list(AM_LABELS))
    r_all = atoms['radius']
    z_all = atoms['z']

    # ④ 기준면 — **고체 전체**
    z_lo = float((z_all - r_all).min())
    z_hi = float((z_all + r_all).max())

    if not is_am.any():
        return dict(perc=0, refusal=None, n_AM=0, reason='AM 입자가 0개',
                    z_lo=z_lo, z_hi=z_hi, slab_t=None, r_AM_max=None,
                    n_edges=0, n_components=0, n_bottom=0, n_top=0,
                    phi_AM_solid_measured=0.0)

    idx = np.flatnonzero(is_am)
    xyz = np.column_stack([atoms['x'][idx], atoms['y'][idx], atoms['z'][idx]])
    rad = r_all[idx]
    slab_t = float(rad.max())                                   # ④ t = r_AM,max

    lx = float(box_hi[0] - box_lo[0])
    ly = float(box_hi[1] - box_lo[1])
    if not (lx > 0 and ly > 0):
        raise BedRefusal(f'상자 가로 길이가 비정상 (lx={lx}, ly={ly})')

    bottom = (xyz[:, 2] - rad) <= (z_lo + slab_t)
    top = (xyz[:, 2] + rad) >= (z_hi - slab_t)

    vol = (4.0 / 3.0) * math.pi * r_all ** 3
    v_am = float(vol[is_am].sum())
    v_se = float(vol[~is_am].sum())
    phi = v_am / (v_am + v_se) if (v_am + v_se) > 0 else float('nan')

    base = dict(z_lo=z_lo, z_hi=z_hi, slab_t=slab_t, r_AM_max=slab_t,
                n_AM=int(len(idx)), n_bottom=int(bottom.sum()), n_top=int(top.sum()),
                phi_AM_solid_measured=phi, refusal=None)

    # 사전등록: "그 층에 입자가 없으면 미퍼콜"
    if not bottom.any() or not top.any():
        base.update(perc=0, n_edges=0, n_components=int(len(idx)),
                    reason='슬래브가 비었다 (아래 %d · 위 %d)' % (bottom.sum(), top.sum()))
        return base

    pairs = _pairs_within(xyz, rad, lx, ly, z_pad=slab_t)

    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    n = len(idx)
    if len(pairs):
        data = np.ones(len(pairs))
        adj = coo_matrix((data, (pairs[:, 0], pairs[:, 1])), shape=(n, n))
        adj = adj + adj.T
    else:
        adj = coo_matrix((n, n))
    ncomp, comp = connected_components(adj, directed=False)

    bot_c = set(comp[bottom].tolist())
    top_c = set(comp[top].tolist())
    hit = sorted(bot_c & top_c)

    base.update(perc=int(bool(hit)), n_edges=int(len(pairs)), n_components=int(ncomp),
                reason=('연결성분 %s 가 두 슬래브를 잇는다' % hit) if hit
                       else '두 슬래브를 잇는 연결성분이 없다')
    return base


# ──────────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────────
def latest_dump(post_dir):
    """`atom_<step>.liggghts` 중 **step 이 최대**인 것 (⑤).  사전순이 아니다."""
    best, best_step = None, -1
    for name in os.listdir(post_dir):
        if not (name.startswith('atom_') and name.endswith('.liggghts')):
            continue
        try:
            step = int(name[len('atom_'):-len('.liggghts')])
        except ValueError:
            continue
        if step > best_step:
            best, best_step = name, step
    if best is None:
        raise BedRefusal(f'{post_dir}: `atom_<step>.liggghts` 가 없다')
    return os.path.join(post_dir, best), best_step


def run_one(dump, n_types, case, allow_any_bc):
    atoms, blo, bhi, bc = read_atom_dump(dump)
    note = check_boundary_flags(bc, allow_any_bc)
    out = percolation(atoms, blo, bhi, n_types)
    out.update(case=case, dump=os.path.abspath(dump), n_types=int(n_types),
               n_particles=int(len(atoms['type'])), bc_note=note,
               box_lx=float(bhi[0] - blo[0]), box_ly=float(bhi[1] - blo[1]))
    return out


# ──────────────────────────────────────────────────────────────────────────────
# selftest — 경계 fixture 포함 (Codex R11 B1: "결과 전에 커밋")
# ──────────────────────────────────────────────────────────────────────────────
def _fixture(rows, lx=10.0, ly=10.0, zlo=-5.0, zhi=25.0, bc='pp pp ff'):
    """rows = [(type, x, y, z, r), ...] → 덤프 문자열."""
    head = ['ITEM: TIMESTEP', '0', 'ITEM: NUMBER OF ATOMS', str(len(rows)),
            f'ITEM: BOX BOUNDS {bc}',
            f'0.0 {lx}', f'0.0 {ly}', f'{zlo} {zhi}',
            'ITEM: ATOMS id type x y z radius']
    for k, (t, x, y, z, r) in enumerate(rows, 1):
        head.append(f'{k} {t} {x!r} {y!r} {z!r} {r!r}')
    return '\n'.join(head) + '\n'


def _run_fixture(tmp, rows, n_types=2, **kw):
    path = os.path.join(tmp, 'atom_100.liggghts')
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(_fixture(rows, **kw))
    return run_one(path, n_types, 'fx', allow_any_bc=False)


def selftest():
    import tempfile
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}')

    with tempfile.TemporaryDirectory() as tmp:
        # ── 1. 관통하는 AM 기둥 → perc = 1 ─────────────────────────────────
        # r = 1, 중심 z = 0,2,4,...,20 → 표면이 정확히 맞닿는다 (간극 = 0).
        col = [(1, 5.0, 5.0, float(2 * k), 1.0) for k in range(11)]
        r1 = _run_fixture(tmp, col)
        chk('1 관통 기둥 perc=1', r1['perc'] == 1, r1['reason'])
        chk('1 간선 10개 (등호가 접촉)', r1['n_edges'] == 10, str(r1['n_edges']))
        chk('1 z_lo/-1 · z_hi/21', abs(r1['z_lo'] + 1) < 1e-12 and abs(r1['z_hi'] - 21) < 1e-12)

        # ── 2. 한 알을 빼면 끊긴다 → perc = 0 (음성 경로) ───────────────────
        cut = col[:5] + col[6:]
        r2 = _run_fixture(tmp, cut)
        chk('2 한 알 제거 perc=0', r2['perc'] == 0, r2['reason'])
        chk('2 성분이 둘 이상', r2['n_components'] >= 2, str(r2['n_components']))

        # ── 3. 경계 fixture — 간극이 정확히 0 이면 접촉, 조금이라도 벌어지면 아니다 ──
        eps = 1e-9
        r3a = _run_fixture(tmp, [(1, 5.0, 5.0, 0.0, 1.0), (1, 5.0, 5.0, 2.0, 1.0)])
        r3b = _run_fixture(tmp, [(1, 5.0, 5.0, 0.0, 1.0), (1, 5.0, 5.0, 2.0 + eps, 1.0)])
        chk('3 간극 0 = 접촉', r3a['n_edges'] == 1, str(r3a['n_edges']))
        chk('3 간극 +1e-9 = 비접촉', r3b['n_edges'] == 0, str(r3b['n_edges']))

        # ── 4. xy minimum image — 상자를 가로질러 닿는다 ────────────────────
        # x = 0.4 와 x = 9.7, Lx = 10 → 감싼 거리 0.7 ≤ r_i + r_j = 1.0
        r4 = _run_fixture(tmp, [(1, 0.4, 5.0, 5.0, 0.5), (1, 9.7, 5.0, 5.0, 0.5)])
        chk('4 xy 주기 간선 있음', r4['n_edges'] == 1, str(r4['n_edges']))
        # 같은 배치를 y 로 크게 벌리면 없어야 한다 (minimum image 가 만능이 아님을 확인)
        r4b = _run_fixture(tmp, [(1, 0.4, 1.0, 5.0, 0.5), (1, 9.7, 5.0, 5.0, 0.5)])
        chk('4 멀면 간선 없음', r4b['n_edges'] == 0, str(r4b['n_edges']))

        # ── 5. z 는 감싸지 않는다 (③ 음성 경로) ─────────────────────────────
        # 아래 끝과 위 끝의 두 알만.  z 를 감싸면 붙어 perc=1 이 되어 버린다.
        r5 = _run_fixture(tmp, [(1, 5.0, 5.0, 0.0, 1.0), (1, 5.0, 5.0, 20.0, 1.0)])
        chk('5 z 미감쌈 → perc=0', r5['perc'] == 0, r5['reason'])
        chk('5 z 미감쌈 → 간선 0', r5['n_edges'] == 0, str(r5['n_edges']))

        # ── 6. 슬래브가 비면 미퍼콜 ────────────────────────────────────────
        # SE 가 위아래로 튀어나와 기준면을 정하고, AM 은 가운데만 있다.
        mid = [(1, 5.0, 5.0, float(8 + 2 * k), 1.0) for k in range(3)]
        se = [(2, 2.0, 2.0, 0.0, 1.0), (2, 2.0, 2.0, 20.0, 1.0)]
        r6 = _run_fixture(tmp, mid + se)
        chk('6 슬래브 빔 → perc=0', r6['perc'] == 0, r6['reason'])
        chk('6 위 슬래브 0개', r6['n_top'] == 0, str(r6['n_top']))
        chk('6 기준면은 SE 를 포함', abs(r6['z_lo'] + 1) < 1e-12 and abs(r6['z_hi'] - 21) < 1e-12)

        # ── 7. ④ 의 이유 — AM 만의 범위였다면 6번이 perc=1 이 됐을 것 ────────
        r7 = _run_fixture(tmp, mid)          # SE 없이 같은 AM 만
        chk('7 AM 만이면 같은 AM 이 perc=1', r7['perc'] == 1, r7['reason'])

        # ── 8. AM_P ↔ AM_S 간선 허용 (②) ──────────────────────────────────
        # ⚠ SE 알은 AM 범위 **안**에 둔다 — 밖에 두면 기준면이 늘어나 위 슬래브가 비고,
        #    그 이른 반환 때문에 간선을 세기도 전에 끝난다 (이 픽스처 자신이 그 함정에 빠졌다).
        mixed = [(1, 5.0, 5.0, 0.0, 2.0), (2, 5.0, 5.0, 2.5, 0.5),
                 (1, 5.0, 5.0, 5.0, 2.0), (3, 1.0, 1.0, 3.0, 0.5)]
        r8 = _run_fixture(tmp, mixed, n_types=3)
        chk('8 AM_P-AM_S 간선', r8['n_edges'] == 2, str(r8['n_edges']))
        chk('8 SE 는 노드 아님', r8['n_AM'] == 3, str(r8['n_AM']))
        chk('8 큰↔작은 사슬로 관통', r8['perc'] == 1, r8['reason'])

        # ── 9. 상 사상 fail-closed ────────────────────────────────────────
        try:
            _run_fixture(tmp, [(1, 5.0, 5.0, 0.0, 1.0), (3, 5.0, 5.0, 3.0, 1.0)], n_types=2)
            chk('9 선언 밖 type 거부', False, '거부하지 않았다')
        except BedRefusal:
            chk('9 선언 밖 type 거부', True)

        # ── 10. 경계 플래그 fail-closed (③) ───────────────────────────────
        try:
            _run_fixture(tmp, col, bc='pp pp pp')
            chk('10 경계 플래그 거부', False, '거부하지 않았다')
        except BedRefusal:
            chk('10 경계 플래그 거부', True)

        # ── 11. φ 측정값 = 질량분율 정의와 같은 축 ──────────────────────────
        # AM r=1 4개, SE r=1 4개 → V_AM/(V_AM+V_SE) = 0.5
        half = [(1, 1.0 + k, 1.0, 5.0, 1.0) for k in range(4)] + \
               [(2, 1.0 + k, 4.0, 5.0, 1.0) for k in range(4)]
        r11 = _run_fixture(tmp, half)
        chk('11 phi 측정 0.5', abs(r11['phi_AM_solid_measured'] - 0.5) < 1e-12,
            str(r11['phi_AM_solid_measured']))

        # ── 12. 마지막 프레임을 쓴다 (⑤) ───────────────────────────────────
        two = _fixture([(1, 5.0, 5.0, 0.0, 1.0)]) + _fixture(col)
        p12 = os.path.join(tmp, 'atom_200.liggghts')
        with open(p12, 'w', encoding='utf-8') as fh:
            fh.write(two)
        r12 = run_one(p12, 2, 'fx', allow_any_bc=False)
        chk('12 마지막 프레임', r12['n_particles'] == len(col) and r12['perc'] == 1,
            str(r12['n_particles']))

        # ── 13. latest_dump 는 step 최대 (사전순 아님) ─────────────────────
        for nm in ('atom_9.liggghts', 'atom_100.liggghts', 'atom_2425000.liggghts'):
            open(os.path.join(tmp, nm), 'a', encoding='utf-8').close()
        got, step = latest_dump(tmp)
        chk('13 최대 step 선택', step == 2425000, f'{got} step={step}')

        # ── 14. 결정성 ────────────────────────────────────────────────────
        a = _run_fixture(tmp, col)
        b = _run_fixture(tmp, col)
        chk('14 결정성', (a['perc'], a['n_edges'], a['n_components'])
                        == (b['perc'], b['n_edges'], b['n_components']))

    print(f'lhs_perc_extract selftest: {ok}/{ok + len(bad)} PASS')
    for b in bad:
        print('  ✗', b)
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='AM 접촉 그래프의 z-퍼콜레이션 판정 (사전등록 v2 §4-1 규약 봉인)')
    ap.add_argument('--dump', help='압밀 후 원자 덤프 하나')
    ap.add_argument('--post-dir', help='디렉터리 — step 이 가장 큰 atom_*.liggghts 를 고른다')
    ap.add_argument('--n-types', type=int, choices=(2, 3),
                    help='2 = mono {1:AM, 2:SE} · 3 = bimodal {1:AM_P, 2:AM_S, 3:SE}.  '
                         '자동 추론은 거부한다 (docstring 규약 6)')
    ap.add_argument('--case', default=None, help='케이스 이름 (기본: 디렉터리 이름)')
    ap.add_argument('--allow-any-bc', action='store_true',
                    help='경계 플래그 검사를 우회한다 — 진단 전용, 생산 금지')
    ap.add_argument('--out', help='결과 JSON 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.dump and not a.post_dir:
        ap.error('--dump 또는 --post-dir 이 필요하다')
    if a.n_types is None:
        ap.error('--n-types 는 필수다 (fail-closed — docstring 규약 6)')

    if a.post_dir:
        dump, _step = latest_dump(a.post_dir)
        case = a.case or os.path.basename(os.path.normpath(a.post_dir))
    else:
        dump = a.dump
        case = a.case or os.path.basename(os.path.dirname(os.path.abspath(dump)))

    out = run_one(dump, a.n_types, case, a.allow_any_bc)
    txt = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)
    print(txt)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(txt + '\n')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BedRefusal as exc:
        print(f'⛔ 거부: {exc}', file=sys.stderr)
        sys.exit(2)
