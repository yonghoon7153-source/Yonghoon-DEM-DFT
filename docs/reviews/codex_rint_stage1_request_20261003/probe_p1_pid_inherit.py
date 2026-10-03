#!/usr/bin/env python3
"""Codex 요청 탐침 P1 — 첨가제 복셀이 AM 입자 번호(pid)를 물려받는다 (① r_int 자기리뷰 P1-1 · 독립 재현).

자기리뷰 원 탐침(p8b_neck.py)은 본 세션 scratchpad 에만 있어 리포에 없다.  여기서는 **형상을 따로 짜서**
같은 결함 부류를 재현한다 — 수치는 원 탐침과 다르다 (형상이 다르므로).

  (a) 합성: VGCF 한 가닥 (기둥 하나) 이 pid 0/1/2 를 지닌다 → 표에 VGCF|VGCF 를 주면 같은 가닥 안에
      가짜 계면 2 면 · σ_e 붕괴 · 결과의 `interface` 원장에 실물처럼 기록된다.  pid 를 −1 로 두면 0 면.
  (b) 생산 경로: `rasterize` (AM 두 구 접촉 + VGCF 점열) — 첨가제 스탬프가 sid 만 바꾸고 pid 를 남기는지,
      그리고 가짜 VGCF|VGCF 면이 실제 생산 래스터에서 생기는지 센다 (솔브 없이 면만).
  (c) pid 를 읽는 다른 소비처: `per_particle_current` 는 pid ≥ 0 인 **모든** 복셀을 더한다 —
      AM 자리를 덮어쓴 VGCF 복셀의 전류가 그 AM 입자 몫에 들어가는지 (계면 항 OFF 에서도).

실행: 리포 뿌리에서 `python3 docs/reviews/codex_rint_stage1_request_20261003/probe_p1_pid_inherit.py`
코드 고정: scripts/step3_sigma.py = 구현 커밋 5e0efdb8d 와 같은 파일 (그 뒤 변경 없음).
"""
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import step3_sigma as s3  # noqa: E402

SIG_E = s3.electronic_sigma_table(0.010, 0.005, 100.0, 1.0, 0.25)   # AM_S · AM_P · VGCF · SuperP · SDCP [S/cm]


def fake_vgcf_faces(sid, pid, periodic_xy=False):
    """sid==3 양쪽 · pid 둘 다 ≥ 0 · pid 다름 — face_rint 가 VGCF|VGCF 표에서 r 를 거는 면 수."""
    n = 0
    for ax in range(3):
        a = [slice(None)] * 3; b = [slice(None)] * 3
        a[ax] = slice(None, -1); b[ax] = slice(1, None)
        sa, sb = sid[tuple(a)], sid[tuple(b)]
        pa, pb = pid[tuple(a)], pid[tuple(b)]
        n += int(((sa == 3) & (sb == 3) & (pa >= 0) & (pb >= 0) & (pa != pb)).sum())
    return n


def part_a():
    print('== (a) 합성: VGCF 한 가닥 · pid 0/1/2 (첨가제가 AM 세 입자 자리를 덮었다고 가정)')
    vox = 0.2
    sid = np.zeros((3, 3, 12), np.int8)
    sid[1, 1, :] = 3                                   # 가닥 하나 = 유일한 관통 경로
    kw = dict(z_bot_um=0.0, z_top_um=12 * vox)
    pid = np.full(sid.shape, -1, np.int32)
    pid[1, 1, 0:4], pid[1, 1, 4:8], pid[1, 1, 8:12] = 0, 1, 2
    r0 = s3.solve_sigma_z(sid, SIG_E, vox, **kw)
    for r in (1e-4, 1e-2):
        rr = s3.solve_sigma_z(sid, SIG_E, vox, rint={(3, 3): r}, pid=pid, **kw)
        rn = s3.solve_sigma_z(sid, SIG_E, vox, rint={(3, 3): r}, pid=np.full(sid.shape, -1, np.int32), **kw)
        print(f'  r = {r:g} Ω·cm²: σ_e OFF {r0["sigma_eff"]:.6g} → pid 상속 {rr["sigma_eff"]:.6g} '
              f'({100 * (rr["sigma_eff"] / r0["sigma_eff"] - 1):+.2f} %) · 원장 faces_by_pair = '
              f'{rr["interface"]["faces_by_pair"]} · pid −1 이면 σ_e {rn["sigma_eff"]:.6g} · 면 '
              f'{rn["interface"]["n_faces_rint"]}')


def part_b():
    print('== (b) 생산 경로 rasterize: AM_S 두 구 접촉 (R 1.0 µm · 겹침 δ 0.02 µm) + VGCF 점열')
    R, d = 1.0, 1.98
    am_c = np.array([[1.5, 1.5, 1.5], [1.5 + d, 1.5, 1.5]])
    am_r = np.array([R, R]); am_t = np.array([2, 2])          # 2 = AM_S (LIGGGHTS 규약)
    xc = 1.5 + d / 2.0                                        # 접촉면 x
    hi = (1.5 + d + 1.5, 3.0, 3.0)
    for vox in (0.2, 0.1):
        rows = []
        for label, pts in (
            ('목을 y 로 가로지름 (x = 접촉면)', np.c_[np.full(281, xc), np.linspace(0.1, 2.9, 281), np.full(281, 1.5)]),
            ('목을 y 로 가로지름 (x = 접촉면 − ½vox)', np.c_[np.full(281, xc - vox / 2), np.linspace(0.1, 2.9, 281), np.full(281, 1.5)]),
            ('목을 z 로 가로지름 (x = 접촉면 + ½vox)', np.c_[np.full(281, xc + vox / 2), np.full(281, 1.5), np.linspace(0.1, 2.9, 281)]),
            ('두 구 윗면을 x 로 (z = 꼭대기 − ½vox)', np.c_[np.linspace(0.6, hi[0] - 0.6, 401), np.full(401, 1.5), np.full(401, 1.5 + R - vox / 2)]),
        ):
            aph = np.full(len(pts), 2)                          # 2 → sid 3 (VGCF)
            sid, pid = s3.rasterize(am_c, am_r, am_t, pts, aph, (0.0, 0.0, 0.0), hi, vox)
            v = sid == 3
            pids = sorted(set(pid[v].tolist()) - {-1})
            rows.append((label, int(v.sum()), int((v & (pid >= 0)).sum()), pids, fake_vgcf_faces(sid, pid)))
        print(f'  vox {vox}:')
        for label, nv, npid, pids, nf in rows:
            print(f'    {label}: VGCF 복셀 {nv} · 그 중 pid ≥ 0 {npid} · pid 종류 {pids} · 가짜 VGCF|VGCF 면 {nf}')


def part_c():
    print('== (c) per_particle_current: AM 자리를 덮은 VGCF 복셀의 전류가 AM 입자 몫에 들어가는가 (계면 항 OFF)')
    vox = 0.2
    sid = np.ones((6, 6, 10), np.int8)                      # AM_S 기둥 블록
    pid = np.zeros(sid.shape, np.int32); pid[:, :, 5:] = 1  # 아래 입자 0 · 위 입자 1
    sid[2:4, 2:4, 1:4] = 3                                  # 입자 0 안에 VGCF 4×3 셀 (sid 만 바뀜 · pid 0 유지)
    kw = dict(z_bot_um=0.0, z_top_um=10 * vox)
    res = s3.solve_sigma_z(sid, SIG_E, vox, return_field=True, **kw)
    je_inh = s3.per_particle_current(res, sid, pid, SIG_E, 2)
    pid_fix = pid.copy(); pid_fix[sid == 3] = -1
    je_fix = s3.per_particle_current(res, sid, pid_fix, SIG_E, 2)
    print(f'  입자별 |J_z| 대리값 — pid 상속 {je_inh.round(6).tolist()} · VGCF 복셀 pid −1 {je_fix.round(6).tolist()} '
          f'· 입자 0 비 {je_inh[0] / je_fix[0]:.3f}')


if __name__ == '__main__':
    part_a()
    part_b()
    part_c()
