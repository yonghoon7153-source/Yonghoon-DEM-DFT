#!/usr/bin/env python3
"""Codex 요청 탐침 P2-1 — 계면 저항을 복셀 **면마다** 걸면 접촉 면적이 격자 산물이 된다 (독립 재현).

① 은 r [Ω·cm²] 를 계면 면 하나하나에 직렬로 넣는다 → 계면 전체의 컨덕턴스 = (면 수 × vox²)/r.
참 면적 A_true 와 면 수 × vox² 의 비가 형상 · 기울기 · 격자에 따라 변하면, 같은 r 가 다른 계면 컨덕턴스를 낸다.

  (a) 기울인 평면: 면 수 × vox² / 참 면적 → 기대 |cosθ| + |sinθ| (법선 L1 노름)
  (b) 구 표면: 면 수 × vox² / 4πR² → 기대 3/2 (방향 평균)
  (c) AM–AM 접촉 (rasterize · 브리지 기본 1.2·vox 와 고정 0.24 µm): pid 가 다른 AM 면 × vox² / 기하 교차 원판 πa²
  (d) AM_S 사슬의 vox 사다리: 같은 r 에서 σ(r)/σ(0) 가 격자를 따라 움직이는가 (계면 몫 비수렴)

실행: 리포 뿌리에서 `python3 docs/reviews/codex_rint_stage1_request_20261003/probe_p21_face_area.py`
코드 고정: scripts/step3_sigma.py = 구현 커밋 5e0efdb8d 와 같은 파일 (그 뒤 변경 없음).
"""
import math
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import step3_sigma as s3  # noqa: E402


def count_faces(mask_a, mask_b):
    """mask_a 셀과 mask_b 셀이 마주한 6-이웃 면 수 (비주기)."""
    n = 0
    for ax in range(3):
        a = [slice(None)] * 3; b = [slice(None)] * 3
        a[ax] = slice(None, -1); b[ax] = slice(1, None)
        n += int((mask_a[tuple(a)] & mask_b[tuple(b)]).sum() + (mask_b[tuple(a)] & mask_a[tuple(b)]).sum())
    return n


def part_a():
    print('== (a) 기울인 평면 (x–z 면에서 θ · 상자 400 × 4 × 400 셀 · vox 1)')
    nx, ny, nz = 400, 4, 400
    xc = np.arange(nx) + 0.5; zc = np.arange(nz) + 0.5
    for deg in (0, 15, 30, 45):
        t = math.tan(math.radians(deg))
        z0 = nz / 2 - t * nx / 2
        below = (zc[None, :] < (t * xc[:, None] + z0))           # (nx, nz)
        A = np.repeat(below[:, None, :], ny, axis=1)
        nf = count_faces(A, ~A)
        true_area = nx / math.cos(math.radians(deg)) * ny      # 평면이 x 전 구간을 지난다
        print(f'  θ {deg:2d}°: 면 수 비 {nf / true_area:.4f} · 기대 cosθ + sinθ = '
              f'{math.cos(math.radians(deg)) + math.sin(math.radians(deg)):.4f}')


def part_b():
    print('== (b) 구 표면 (R 2 µm): 면 수 × vox² / 4πR²')
    R = 2.0
    for vox in (0.4, 0.2, 0.1, 0.05):
        n = int(math.ceil(2 * R / vox)) + 4
        c = (n * vox) / 2
        g = (np.arange(n) + 0.5) * vox - c
        X, Y, Z = np.meshgrid(g, g, g, indexing='ij')
        inside = X * X + Y * Y + Z * Z <= R * R
        nf = count_faces(inside, ~inside)
        print(f'  vox {vox}: 비 {nf * vox * vox / (4 * math.pi * R * R):.4f}')


def am_pair_faces(sid, pid):
    am = (sid == 1) | (sid == 2)
    n = 0
    for ax in range(3):
        a = [slice(None)] * 3; b = [slice(None)] * 3
        a[ax] = slice(None, -1); b[ax] = slice(1, None)
        n += int((am[tuple(a)] & am[tuple(b)] & (pid[tuple(a)] >= 0) & (pid[tuple(b)] >= 0)
                  & (pid[tuple(a)] != pid[tuple(b)])).sum())
    return n


def part_c():
    print('== (c) AM_S 두 구 접촉 (R 2 µm · 겹침 δ 0.05 µm) — pid 가 다른 AM|AM 면 × vox² / πa² (기하 교차 원판)')
    R, delta = 2.0, 0.05
    d = 2 * R - delta
    a_geo = math.sqrt(R * R - (d / 2) ** 2)
    A_true = math.pi * a_geo ** 2
    print(f'  a = {a_geo:.4f} µm (a/R {a_geo / R:.3f}) · πa² = {A_true:.4f} µm²')
    am_c = np.array([[2.5, 2.5, 2.5], [2.5 + d, 2.5, 2.5]]); am_r = np.array([R, R]); am_t = np.array([2, 2])
    hi = (2.5 + d + 2.5, 5.0, 5.0)
    for bridge in (None, 0.24):
        cells = []
        for vox in (0.4, 0.2, 0.15, 0.1, 0.05):
            sid, pid = s3.rasterize(am_c, am_r, am_t, None, None, (0.0, 0.0, 0.0), hi, vox, bridge_um=bridge)
            nf = am_pair_faces(sid, pid)
            cells.append(f'vox {vox}: {nf} 면 · 비 {nf * vox * vox / A_true:.2f}')
        print(f'  브리지 {"기본 1.2·vox" if bridge is None else f"고정 {bridge} µm"}: ' + ' | '.join(cells))


def part_d():
    print('== (d) AM_S 사슬 4 구 (R 1 µm · δ 0.02 µm · z 방향) — r = 1e-3 Ω·cm² 를 pid 경계에, vox 사다리')
    R, delta, N = 1.0, 0.02, 4
    d = 2 * R - delta
    zs = R + d * np.arange(N)
    am_c = np.c_[np.full(N, 1.0), np.full(N, 1.0), zs]
    am_r = np.full(N, R); am_t = np.full(N, 2)
    top = float(zs[-1] + R)
    hi = (2.0, 2.0, top)
    a_geo = math.sqrt(R * R - (d / 2) ** 2)
    sig = s3.electronic_sigma_table(0.010, 0.005, 100.0, 1.0, 0.25)
    for bridge in (None, 0.24):
        cells = []
        for vox in (0.2, 0.1, 0.05):
            sid, pid = s3.rasterize(am_c, am_r, am_t, None, None, (0.0, 0.0, 0.0), hi, vox, bridge_um=bridge)
            kw = dict(z_bot_um=0.0, z_top_um=top)
            r0 = s3.solve_sigma_z(sid, sig, vox, **kw)
            r1 = s3.solve_sigma_z(sid, sig, vox, rint={(1, 1): 1e-3}, pid=pid, **kw)
            cells.append(f'vox {vox}: σ(r)/σ(0) {r1["sigma_eff"] / r0["sigma_eff"]:.4f} · 면 {r1["interface"]["n_faces_rint"]}')
        print(f'  브리지 {"기본 1.2·vox" if bridge is None else f"고정 {bridge} µm"}: ' + ' | '.join(cells))
    print(f'  참고: 기하 접촉 반지름 a = {a_geo:.4f} µm — 계면 3 곳이 참 면적 πa² 로 r 를 받는다면 σ(r)/σ(0) 는 격자와 무관해야 한다')


if __name__ == '__main__':
    part_a()
    part_b()
    part_c()
    part_d()
