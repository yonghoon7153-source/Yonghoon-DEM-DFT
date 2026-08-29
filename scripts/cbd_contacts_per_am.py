#!/usr/bin/env python3
"""AM 입자당 전도성-첨가제(CBD) 접촉 수 — Table S3 의 `Median CBD contacts per AM`.

    python3 scripts/cbd_contacts_per_am.py --bed <run_dir> --scaffold am_scaffold.csv
    python3 scripts/cbd_contacts_per_am.py --selftest

★ 왜 이 스크립트가 필요한가.  침대는 **MPM 물질점 구름**으로 저장돼 있다 (침대당 ≈ 1.9 GB):
`phase.npy` 는 점당 상 라벨(int8), `fibre.npy` 는 점당 개체 id, `se_dump.npy` 는 점당 좌표
(3 × float32).  상 라벨은 *"이 점은 VGCF"* 만 알고 *"몇 번 AM 입자"* 는 모른다 — AM 개체
정보는 런 디렉터리 **밖의** `am_scaffold.csv` (AM 1,271개) 에 있다.
⇒ 둘을 합쳐야 **입자별** 접촉 수가 나온다.

세는 방법 (규약을 여기 못박는다 — 나중에 바꾸면 값이 바뀐다):

  · **접촉** = AM 구 **표면 바깥** `band_um` (기본 0.15 µm = σ_e 격자 한 복셀 폭) 껍질 안에
    있는 첨가제 물질점.
  · **접촉 수** = 그 점들이 속한 **서로 다른 첨가제 개체(object)의 개수**.
    ⚠ 점 개수가 아니다 — 굵은 섬유 하나가 점을 여럿 차지해도 접촉 1 이다.
  · **CBD 구성**: 기본은 **전도성** 첨가제만 = VGCF(2) + SDCP(5).  PTFE(4)는 절연이라
    기본에서 뺀다.  `--include-ptfe` 로 넣을 수 있다 — v6 의 433/517 이 어느 구성인지
    모르므로 **두 구성을 다 내고** 어느 쪽이 v6 과 맞는지 보고한다.

좌표 프레임 (2026-08-29 실측으로 확정):
  `se_dump` 는 MPM **정규화** 좌표다.  실좌표로 되돌리는 사상은 **기록된 양에서 유도**한다 —
    · 축척 = `um_box_um` (= 54.3478 µm/unit).  ⚠ `lateral_box × 1000` (= 50) **아니다**
    · 가로 origin = `(1 − lateral_box·1000/um_box_um)/2` = 0.04 — 50 µm 침대가 54.35 µm
      도메인 **가운데** 놓여 있다 (50/54.3478 = 0.92003, 관측 x 범위 0.0400–0.9602 와 일치)
    · z origin = `wall_z − thickness_um/축척` = 0.04995
  두 독립 확인: 두께 `(1.3846−0.05)×54.3478 = 72.533` (기록 **72.534**) ·
  가로 폭 `(0.9602−0.0400)×54.3478 = 50.011` (**50**).
  ⚠ 초판은 `×50, origin 0` 이라 **양 축 다 8 % 작았고**, 그래서 전부 흩어졌다.
  `am_scaffold` 는 이미 실좌표다 (AM 반지름 0.0025 = 2.5 µm).
  ⚠⚠ **이 배선을 접촉으로 검증하지 않는다** — 접촉이 생길 때까지 변환을 맞추면 그 변환이
  답을 만든다.  대신 **독립 성질**로 검사한다: AM 은 MPM 에서 얼어붙은 장애물이므로
  그 구 **안에는 물질점이 없어야** 하고, 변환이 틀리면 그 비율이 AM 부피분율(≈46 %) 근처로
  튄다.  `inside_frac` 이 그 검사이고 초과하면 **거부한다**.
  ★ 이 검사가 유효한 이유: 상 코드 전수를 세니 **AM 상이 없다** (SE 97.23 % · VGCF 2.42 % ·
  PTFE 0.35 %) — AM 은 격자 마스크이지 물질점이 아니다.  ⇒ *"첨가제가 AM 을 배제하지 않고
  시딩됐다"* 라는 대안 설명이 배제되고, 높은 `inside_frac` 은 변환 오류만을 뜻한다.

⚠⚠ **이 값은 규약 의존이다.**  band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.
그래서 산출물에 규약을 함께 적고, 원고에는 규약과 함께 인용한다.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

PHASE = {'VGCF': 2, 'PTFE': 4, 'SDCP': 5}
CONDUCTIVE = ('VGCF', 'SDCP')
#  프레임 검증을 **표면이 아니라 깊은 안쪽**에서 한다 — 배제 경계가 ≈ 0.5 µm 흐리다.
DEEP_FRAC = 0.8


def _load_scaffold(path):
    """AM 중심·반지름을 **시뮬 단위 그대로** 읽는다 (변환은 호출자가).

    파일 첫 줄이 `# type,x,y,z,r  # AM scaffold ...` 형태라 표준 DictReader 로는 열 이름이
    `'# type'` 이 된다.  ⇒ 주석 표지와 꼬리 주석을 벗겨서 읽는다.
    """
    import csv
    rows, header = [], None
    with open(path, newline='', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            if header is None:
                head = line.lstrip('#').strip()
                head = head.split('#')[0].strip()          # 꼬리 주석 제거
                header = [c.strip().lower() for c in head.split(',')]
                continue
            if line.startswith('#'):
                continue
            rows.append(dict(zip(header, next(csv.reader([line])))))
    if header is None:
        raise SystemExit(f'am_scaffold 가 비었다: {path}')

    def pick(*names):
        for n in names:
            if n in header:
                return n
        raise SystemExit(f'am_scaffold 에 {names} 중 어느 열도 없다: {header}')
    cx, cy, cz = pick('x', 'x_um'), pick('y', 'y_um'), pick('z', 'z_um')
    cr = pick('r', 'radius', 'r_um', 'radius_um')
    ct = 'type' if 'type' in header else None
    xs = [float(r[cx]) for r in rows]
    ys = [float(r[cy]) for r in rows]
    zs = [float(r[cz]) for r in rows]
    rr = [float(r[cr]) for r in rows]
    tt = [int(float(r[ct])) for r in rows] if ct else [0] * len(rows)
    return xs, ys, zs, rr, tt


def count_contacts(bed_dir, scaffold, band_um=0.15, include_ptfe=False,
                   max_am=None, um_per_unit=1000.0, se_scale=None,
                   inside_tol=0.02):
    """AM 입자별 접촉 **개체** 수.

    ⚠ 침대는 **복셀 격자가 아니라 MPM 물질점 구름**이다 (2026-08-29 실측):
    `mpm_metrics.n_pts` = `phase.npy` 길이이고 `se_dump.npy` 는 그 3배 float32 = **좌표**다.
    (초판은 `n_grid²·nz` 격자로 읽으려다 fail-closed 검사에 걸렸다 — 2.55배 안 맞았다.)
    ⇒ 접촉을 격자가 아니라 **기하**로 직접 잰다.

    `um_per_unit`: scaffold·se_dump 의 길이 단위 → µm.  기본 1000 은 데이터가 정한다 —
    scaffold 의 AM 반지름 0.0025 가 NCM811 의 2.5 µm 이고 상자 0.05 가 50 µm 다.
    함수가 그 정합성을 **검사**한다.
    """
    import numpy as np
    from scipy.spatial import cKDTree

    meta = json.load(open(os.path.join(bed_dir, 'mpm_metrics.json'), encoding='utf-8'))
    n_pts = int(meta['n_pts'])
    phase = np.load(os.path.join(bed_dir, 'phase.npy'), mmap_mode='r')
    if phase.size != n_pts:
        raise SystemExit(f'phase.npy 길이 {phase.size} != mpm_metrics.n_pts {n_pts}')
    pos = np.load(os.path.join(bed_dir, 'se_dump.npy'), mmap_mode='r')
    if pos.size != 3 * n_pts:
        raise SystemExit(f'se_dump.npy 원소 {pos.size} != 3·n_pts {3*n_pts} — '
                         f'좌표 배열이 아니다')
    pos = pos.reshape(n_pts, 3)
    fid = np.load(os.path.join(bed_dir, 'fibre.npy'), mmap_mode='r')
    if fid.size != n_pts:
        raise SystemExit(f'fibre.npy 길이 {fid.size} != n_pts {n_pts}')

    #  ── 상 개수를 매니페스트와 대조한다 (배열이 서로 같은 색인인지 fail-closed)
    ph = np.asarray(phase)
    counts = {k: int((ph == c).sum()) for k, c in PHASE.items()}
    add = meta.get('additives', {})
    for k in ('VGCF', 'PTFE', 'SDCP'):
        if k in add and 'n_points' in add[k]:
            want = int(add[k]['n_points'])
            if counts[k] != want:
                raise SystemExit(f'{k}: phase.npy 가 {counts[k]:,} 점인데 '
                                 f'metrics 는 {want:,} — 배열 색인이 다르다')

    kinds = list(CONDUCTIVE) + (['PTFE'] if include_ptfe else [])
    sel = np.isin(ph, [PHASE[k] for k in kinds])
    idx = np.flatnonzero(sel)
    if idx.size == 0:
        raise SystemExit(f'{kinds} 상의 점이 하나도 없다')
    #  ── 좌표 프레임.  `se_dump` 는 MPM **정규화** 좌표다 (도메인 ≈ [0,1], 플래튼이
    #     `wall_z`).  실좌표로 되돌리려면 `lateral_box` 를 곱한다.  scaffold 는 이미 실좌표다.
    #     ⚠ 이 배선은 아래 `inside_frac` 검사가 **접촉과 무관하게** 검증한다.
    #  ⚠⚠ 초판은 `× lateral_box × 1000` (= ×50, offset 0) 이었고 **양 축 다 8 % 작았다**
    #     — 그래서 첨가제가 AM 에 대해 흩어져 `inside_frac` 이 48 % 로 나왔다.
    #     정확한 사상은 **기록된 양에서 유도**한다 (접촉에 맞추지 않는다):
    #       · 축척 = `um_box_um` (µm / 정규화 단위)
    #       · 가로 offset = 침대가 도메인 **가운데** 놓인 여백.  50/54.3478 = 0.92003 이고
    #         관측 x 범위가 0.0400–0.9602 로 정확히 그것이다
    #       · z offset = `wall_z − thickness_um/축척`  ⇒ 두께가 기록값으로 되돌아온다
    scale_um = float(meta.get('um_box_um') or 0.0)
    if scale_um <= 0:
        raise SystemExit('mpm_metrics 에 um_box_um 이 없다 — 좌표 축척을 유도할 수 없다')
    L_dem_um = float(meta.get('lateral_box', 0.05)) * um_per_unit
    off_xy = (1.0 - L_dem_um / scale_um) / 2.0
    off_z = float(meta['wall_z']) - float(meta['thickness_um']) / scale_um
    if se_scale is not None:                      # 수동 override (진단 전용)
        scale_um, off_xy, off_z = se_scale * um_per_unit, 0.0, 0.0
    origin = np.array([off_xy, off_xy, off_z])
    apos = (np.asarray(pos[idx], dtype=np.float64) - origin) * scale_um
    aid = np.asarray(fid[idx])

    xs, ys, zs, rs, tt = _load_scaffold(scaffold)
    if max_am:
        xs, ys, zs, rs, tt = (v[:max_am] for v in (xs, ys, zs, rs, tt))
    rs_um = [r * um_per_unit for r in rs]
    if not (0.1 <= min(rs_um) and max(rs_um) <= 20.0):
        raise SystemExit(f'AM 반지름이 {min(rs_um):.3g}–{max(rs_um):.3g} µm 로 나온다 — '
                         f'um_per_unit={um_per_unit} 이 틀렸다')

    #  ── 좌표계가 같은가.  scaffold 는 DEM 좌표, se_dump 는 **MPM 압밀 후** 좌표라
    #     프레임이 다를 수 있다 (`dilate_z` · `um_box_um` ≠ `lateral_box`×1000).
    #     프레임이 어긋나면 결과가 "전부 0" 으로 나오는데, 그것은 **측정값이 아니라 실패**다.
    ampos = np.array([[x, y, z] for x, y, z in zip(xs, ys, zs)]) * um_per_unit
    rng_add = (apos.min(axis=0), apos.max(axis=0))
    rng_am = (ampos.min(axis=0), ampos.max(axis=0))

    #  ── 경계 규약: `periodic_xy + z_open` (metrics `coverage_boundary`).
    #     AM 구가 상자를 넘어간다 (실측 x −2.4 … 52.4 µm) ⇒ 감아서 세지 않으면 경계
    #     입자의 접촉을 놓친다.  cKDTree 주기 상자는 **모든 좌표가 ≥ 0** 이어야 하므로
    #     z 를 양쪽 같은 양만큼 밀어 올린다 (거리 불변).
    apos[:, 0] %= L_dem_um
    apos[:, 1] %= L_dem_um
    ampos[:, 0] %= L_dem_um
    ampos[:, 1] %= L_dem_um
    z0 = min(apos[:, 2].min(), ampos[:, 2].min()) - 1.0
    apos[:, 2] -= z0
    ampos[:, 2] -= z0
    zbox = max(apos[:, 2].max(), ampos[:, 2].max()) + 10.0
    tree = cKDTree(apos, boxsize=[L_dem_um, L_dem_um, zbox])

    #  ★ 프레임 검증 — **접촉과 무관하다.**  AM 은 MPM 에서 격자 마스크라 그 **깊은
    #    안쪽**에는 물질점이 없어야 한다.  변환이 틀리면 무작위로 섞여 AM 부피분율
    #    (≈ 0.46) 근처가 나온다.
    #  ⚠⚠ **표면이 아니라 `DEEP_FRAC × r` 안쪽을 본다.**  실측 반경 밀도(2026-08-29):
    #      d/r < 0.8 에서 **0.001**, 0.8–1.0 에서 0.07 → 0.52, 표면 바로 밖 1.34.
    #      배제는 실재하지만 경계가 **≈ 0.5 µm 흐리다** (격자 셀 0.207 µm · 압밀 중 이동).
    #      초판은 `d < r` 로 봐서 그 전이층 9.5 % 를 "변환 오류" 로 잘못 읽었다 —
    #      날카로운 경계를 가정한 검사가 흐린 경계를 만난 것이다.
    inside = set()
    for c, r in zip(ampos, rs_um):
        inside.update(tree.query_ball_point(c, DEEP_FRAC * r))
    inside_frac = len(inside) / float(apos.shape[0])
    if max_am is None and inside_frac > inside_tol:
        raise SystemExit(
            f'첨가제 점의 {inside_frac:.1%} 가 AM 구 **깊은 안쪽**(d < {DEEP_FRAC}·r)에 '
            f'있다 (허용 {inside_tol:.0%}).\n'
            '  AM 은 격자 마스크라 거기 물질점이 없어야 한다 ⇒ 좌표 변환이 틀렸다.\n'
            f'  현재 축척 {scale_um:.4f} µm/unit · origin {origin.round(5).tolist()}\n'
            '  ⚠ 접촉이 생길 때까지 변환을 맞추지 말 것 — 그 변환이 답을 만든다.')

    #  ★ 반경 밀도 프로파일 — 배제가 어디까지 실재하고 경계가 얼마나 흐린지 남긴다.
    #    이것이 `band_um` 규약을 읽는 근거이고, 값이 규약 의존임을 보이는 자리다.
    prof_edges = [0.0, 0.4, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6]   # d / r
    prof = [0] * (len(prof_edges) - 1)
    rmax = max(rs_um)
    for c, r in zip(ampos, rs_um):
        nb = tree.query_ball_point(c, prof_edges[-1] * r)   # ⚠ `idx` 를 덮지 않는다
        if not nb:
            continue
        dd = np.linalg.norm(apos[nb] - c, axis=1) / r
        for j in range(len(prof)):
            prof[j] += int(((dd >= prof_edges[j]) & (dd < prof_edges[j + 1])).sum())
    shell = [(prof_edges[j + 1] ** 3 - prof_edges[j] ** 3) for j in range(len(prof))]
    tot = sum(s_ * 1.0 for s_ in shell)
    bulk = (prof[-1] / shell[-1]) if shell[-1] and prof[-1] else 1.0
    radial = {f'{prof_edges[j]:.1f}-{prof_edges[j+1]:.1f}':
              round((prof[j] / shell[j]) / bulk, 4) if shell[j] and bulk else None
              for j in range(len(prof))}

    out = []
    for c, r in zip(ampos, rs_um):
        near = tree.query_ball_point(c, r + band_um)
        if not near:
            out.append(0)
            continue
        near = np.asarray(near)
        d = np.linalg.norm(apos[near] - c, axis=1)
        keep = near[d >= r]                     # 구 **표면 바깥** 껍질만
        out.append(int(np.unique(aid[keep]).size) if keep.size else 0)

    if out and max(out) == 0:
        ax = lambda t: ' · '.join(f'{a:8.3f}–{b:<8.3f}' for a, b in zip(*t))  # noqa: E731
        raise SystemExit(
            'AM 전부가 접촉 0 이다 — 이것은 측정값이 아니라 **좌표계 불일치**다.\n'
            f'  첨가제 점 (se_dump, MPM 압밀 후) x·y·z 범위 [µm]:\n    {ax(rng_add)}\n'
            f'  AM   (am_scaffold, DEM 좌표)     x·y·z 범위 [µm]:\n    {ax(rng_am)}\n'
            '  ⇒ 두 범위가 겹치지 않거나 축척이 다르면 프레임이 다른 것이다.\n'
            '     mpm_metrics 의 `dilate_z` · `um_box_um` · `wall_z` 를 확인할 것.\n'
            '  ⚠ 자동 보정하지 않는다 — 어떤 변환인지 확정하기 전에 맞추면 그 변환이\n'
            '     결과를 만든다.')

    return out, dict(band_um=band_um, kinds=kinds, n_am=len(out),
                     scale_um_per_unit=scale_um, origin_norm=origin.tolist(),
                     inside_frac=round(inside_frac, 6), deep_frac=DEEP_FRAC,
                     radial_density_norm=radial, boundary='periodic_xy+z_open',
                     range_additive_um=[rng_add[0].tolist(), rng_add[1].tolist()],
                     range_am_um=[rng_am[0].tolist(), rng_am[1].tolist()],
                     um_per_unit=um_per_unit, n_pts=n_pts,
                     n_additive_points=int(idx.size),
                     phase_counts=counts, representation='mpm_material_points')


def summarise(counts):
    import statistics as st
    s = sorted(counts)
    return dict(n=len(s), median=st.median(s), mean=round(st.fmean(s), 2),
                p10=s[len(s) // 10], p90=s[-max(1, len(s) // 10)],
                min=s[0], max=s[-1], zero=sum(1 for v in s if v == 0))


# =========================================================================
def selftest() -> int:
    fails = []

    def chk(name, cond, detail=''):
        (print(f'  ok   {name}') if cond
         else (fails.append(name), print(f'  FAIL {name} {detail}')))

    print('cbd_contacts selftest')
    try:
        import numpy as np
        from scipy.spatial import cKDTree                  # noqa: F401
    except ImportError as e:
        print(f'  {e} — 수치 검사 생략'); return 0
    import tempfile

    #  합성 침대 = **물질점 구름** (실제 형식).  시뮬 단위, 1 unit = 1000 µm.
    U = 1000.0
    cx = cy = cz = 0.016                       # 16 µm
    r_sim = 0.0025                             # 2.5 µm
    band = 0.15                                # µm

    LB, UBOX, WALL, THK = 0.05, 54.3478, 1.3846, 72.534   # 실제 metrics 와 같은 형태
    _sc = UBOX
    _oxy = (1.0 - LB * U / UBOX) / 2.0
    _oz = WALL - THK / UBOX

    def shell_pt(dist_um, k):
        """중심에서 dist_um 떨어진 점을 **se_dump 의 정규화 좌표로** 돌려준다.

        실제 파일이 그 프레임이므로 픽스처도 그래야 변환 배선이 시험된다.
        ⚠ 초판 픽스처는 scaffold 와 같은 프레임이라 변환을 아예 안 태웠고, 그다음 판은
        `×lateral_box` 라는 **틀린** 사상을 태웠다 — 둘 다 실제 결함을 못 잡았다."""
        import math
        a = 0.7 * k
        p = [cx * U + dist_um * math.cos(a), cy * U + dist_um * math.sin(a), cz * U]
        return [p[0] / _sc + _oxy, p[1] / _sc + _oxy, p[2] / _sc + _oz]

    with tempfile.TemporaryDirectory() as td:
        P, F, X = [], [], []

        def add(ph, oid, xyz):
            P.append(PHASE[ph]); F.append(float(oid)); X.append(xyz)
        #  VGCF 개체 3개 — 하나는 **점 5개** (개체 수 ≠ 점 수 검사)
        #  ⚠ 표면(r = 2.5 µm)에 **정확히** 놓지 않는다 — 부동소수로 안/밖이 갈려
        #    `inside_frac` 이 흔들린다.  실침대는 점이 많아 한 점이 좌우하지 않지만
        #    픽스처는 69점이라 한 점이 1.4 %p 다.
        for j in range(5):
            add('VGCF', 11, shell_pt(2.52 + 0.02 * j, j))
        add('VGCF', 12, shell_pt(2.6, 7))
        add('VGCF', 13, shell_pt(2.55, 9))
        #  PTFE 개체 하나 — 기본에서 빠져야 한다
        add('PTFE', 99, shell_pt(2.58, 11))
        #  껍질 밖.  기본 band(0.15)에는 안 들어오고 넓히면 들어와야 한다
        add('VGCF', 77, shell_pt(3.4, 13))
        #  AM 안쪽 첨가제 — 표면 **바깥** 껍질만 세므로 빠져야 한다
        add('VGCF', 55, shell_pt(1.2, 15))
        #  ★ 첨가제 패딩 — 모든 AM 밖 멀리 (band 검사 최대 1.2 µm 껍질 밖).
        #    ⚠ 없으면 위의 **의도적 내부 점 1개**가 첨가제의 11 % 가 되어 `inside_frac`
        #    검사에 걸린다.  실침대는 첨가제가 188만 점이라 그런 일이 없다 —
        #    픽스처가 그 비율을 흉내내야 검사를 제대로 시험한다.
        for j in range(60):
            add('VGCF', 88, shell_pt(10.0 + 0.01 * j, j))
        #  패딩 (SE, 상 코드에 없음)
        for j in range(20):
            P.append(9); F.append(0.0); X.append([0.5 + 1e-4 * j, 0.5, 0.5])

        n_pts = len(P)
        np.save(os.path.join(td, 'phase.npy'), np.array(P, dtype=np.int8))
        np.save(os.path.join(td, 'fibre.npy'), np.array(F, dtype=np.float32))
        np.save(os.path.join(td, 'se_dump.npy'),
                np.array(X, dtype=np.float32).ravel())
        meta = dict(n_pts=n_pts, lateral_box=LB, um_box_um=UBOX,
                    wall_z=WALL, thickness_um=THK, additives=dict(
            VGCF=dict(n_points=sum(1 for p in P if p == PHASE['VGCF'])),
            PTFE=dict(n_points=sum(1 for p in P if p == PHASE['PTFE']))))
        json.dump(meta, open(os.path.join(td, 'mpm_metrics.json'), 'w'))

        sc = os.path.join(td, 'am.csv')
        with open(sc, 'w', encoding='utf-8') as fh:
            fh.write('# type,x,y,z,r  # AM scaffold (AM_P=1,AM_S=2) — fixture\n')
            fh.write(f'2,{cx:.6f},{cy:.6f},{cz:.6f},{r_sim:.6f}\n')

        cnt, info = count_contacts(td, sc, band_um=band)
        chk('전도성 개체 3개 (점 7개 → 개체 3)', cnt == [3], str(cnt))
        chk('AM 표면 **안쪽** 점은 안 센다', 55 not in [11, 12, 13] and cnt == [3])
        chk('PTFE 는 기본에서 빠진다', 'PTFE' not in info['kinds'])
        chk('물질점 표현으로 읽는다',
            info['representation'] == 'mpm_material_points')

        cnt2, _ = count_contacts(td, sc, band_um=band, include_ptfe=True)
        chk('--include-ptfe 면 4개', cnt2 == [4], str(cnt2))

        cnt3, _ = count_contacts(td, sc, band_um=1.2)
        chk('band 를 넓히면 먼 개체가 들어온다', cnt3 == [4], str(cnt3))

        #  ── fail-closed 검사 셋
        json.dump(dict(n_pts=n_pts + 1, lateral_box=LB, um_box_um=UBOX, wall_z=WALL,
                       thickness_um=THK, additives=meta['additives']),
                  open(os.path.join(td, 'mpm_metrics.json'), 'w'))
        try:
            count_contacts(td, sc, band_um=band)
            chk('n_pts 불일치를 잡는다', False, '예외가 안 났다')
        except SystemExit:
            chk('n_pts 불일치를 잡는다 (fail-closed)', True)

        bad = dict(meta); bad['additives'] = dict(VGCF=dict(n_points=999))  # noqa
        json.dump(bad, open(os.path.join(td, 'mpm_metrics.json'), 'w'))
        try:
            count_contacts(td, sc, band_um=band)
            chk('상 개수 불일치를 잡는다', False, '예외가 안 났다')
        except SystemExit:
            chk('상 개수 불일치를 잡는다 (배열 색인이 다르면 멈춘다)', True)

        json.dump(meta, open(os.path.join(td, 'mpm_metrics.json'), 'w'))
        try:
            count_contacts(td, sc, band_um=band, um_per_unit=1.0)
            chk('단위 스케일 오류를 잡는다', False, '예외가 안 났다')
        except SystemExit:
            chk('단위 스케일 오류를 잡는다 (AM 반지름이 비현실적)', True)

        #  주석 머리글이 붙은 scaffold 를 읽는가
        xs, ys, zs, rr, tt = _load_scaffold(sc)
        chk('scaffold: 주석 머리글을 벗겨 읽는다',
            len(xs) == 1 and abs(rr[0] - r_sim) < 1e-12 and tt == [2],
            f'{xs} {rr} {tt}')

    s = summarise([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    chk('summarise: 중앙값·0 개수', s['median'] == 4.5 and s['zero'] == 1, str(s))
    print(f'\n{len(fails)} failure(s)')
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--bed', help='침대 런 디렉터리 (phase·fibre·se_dump·mpm_metrics)')
    ap.add_argument('--scaffold', help='am_scaffold.csv')
    ap.add_argument('--band-um', type=float, default=0.15,
                    help='접촉 판정 껍질 두께 (µm).  기본 0.15 = σ_e 격자 한 복셀')
    ap.add_argument('--se-scale', type=float,
                    help='se_dump 정규화 좌표 → 실좌표 배율 (기본 metrics.lateral_box)')
    ap.add_argument('--um-per-unit', type=float, default=1000.0,
                    help='scaffold·se_dump 길이 단위 → µm (기본 1000; 함수가 검사한다)')
    ap.add_argument('--include-ptfe', action='store_true',
                    help='(참고) 기본 실행은 두 구성을 다 낸다')
    ap.add_argument('--max-am', type=int, help='앞 N 개만 (시험용)')
    ap.add_argument('--out', help='결과 JSON')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.bed and a.scaffold):
        ap.error('--bed 와 --scaffold 가 필요하다')

    res, info = {}, None
    for inc in (False, True):
        cnt, info = count_contacts(a.bed, a.scaffold, band_um=a.band_um,
                                   include_ptfe=inc, max_am=a.max_am,
                                   um_per_unit=a.um_per_unit, se_scale=a.se_scale)
        tag = 'conductive+PTFE' if inc else 'conductive only (VGCF+SDCP)'
        res[tag] = dict(summary=summarise(cnt), convention=info, counts=cnt)
        s = res[tag]['summary']
        print(f'── {tag}')
        print(f'   median {s["median"]}  mean {s["mean"]}  p10–p90 {s["p10"]}–{s["p90"]}  '
              f'min–max {s["min"]}–{s["max"]}  접촉 0 인 AM {s["zero"]}/{s["n"]}')
    print(f'\n규약: band {a.band_um} µm · 접촉 = 서로 다른 **개체** 수 (점 수 아님) · '
          f'AM 표면 바깥 껍질만')
    print(f'   물질점 {info["n_pts"]:,} 중 첨가제 {info["n_additive_points"]:,} · '
          f'상별 점수 {info["phase_counts"]}')
    print(f'   프레임: {info["scale_um_per_unit"]:.4f} µm/unit · origin '
          f'{[round(v,5) for v in info["origin_norm"]]} · AM 구 **안**에 든 첨가제 점 '
          f'{info["inside_frac"]:.2%}  (d < {info["deep_frac"]}·r, AM 은 격자 마스크 ⇒ ≈0)')
    print('   반경 밀도 (d/r, bulk=1): ' + ' · '.join(
        f'{k} {v}' for k, v in info['radial_density_norm'].items()))
    print('⚠ 이 값은 규약 의존이다 — band 폭·개체 정의·PTFE 포함 여부가 각각 값을 바꾼다.')
    if a.out:
        json.dump(res, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'wrote {a.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
