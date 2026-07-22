#!/usr/bin/env python3
"""reflow 갭 분해: ledger-Hertz vs ledger-voxel vs MPM-voxel — "reflow=재유동" 반증 재현.

적대리뷰(물리·통계, 2026-07-22)가 지적: A-3의 reflow=0.34 를 "SE plastic 재유동"으로 라벨했으나,
ledger는 **Hertz 접촉면적**(Σ R·ov, 연속)으로, MPM은 **voxel-coverage**(이진 인접, ~0.13µm 격자)로
접촉손실을 재 — 서로 다른 지표.  SC 표면은 34nm(¼ voxel 미만)만 후퇴 → voxel은 거의 불감, Hertz는
선형 감소.  이 도구는 같은 강체 기하를 **두 지표 모두로** 재서 갭을 분해:
  ledger-Hertz(30%) → ledger-voxel(강체) = 지표+area법칙 차이 (재유동 아님)
  ledger-voxel(강체) → MPM-voxel = 재평형/재유동 (진짜 MPM-only 몫)
real_14 결과: 30.0 → 16.8 → 19.4 %  = 지표 +13.2%p (지배) / 재평형 −2.6%p (미미, 부호도 반대).
⇒ reflow=0.34 는 대부분 지표/법칙 아티팩트.  (물리 Finding 4: ov0~92nm=SE 반경 18% = 소성 →
elastic πRδ area 자체가 과대; production Stage-E capped area가 이래서 존재.)

사용:
  python3 scripts/metric_split_check.py --am-scaffold docs/data/real14_am_scaffold.csv \
      --se-scaffold docs/data/real14_se_scaffold.csv --mpm-loss 19.4 [--n-grid 256] [--sc-dv 0.051]
"""
import argparse
import importlib.util
import os
import sys

import numpy as np


def _ledger():
    s = importlib.util.spec_from_file_location('_L', os.path.join(os.path.dirname(__file__), 'cycle_contact_ledger.py'))
    L = importlib.util.module_from_spec(s)
    _a = sys.argv
    sys.argv = ['_L']
    s.loader.exec_module(L)
    sys.argv = _a
    return L


def _atoms(am_path, se_path):
    def rd(p):
        return [ln.strip().split(',') for ln in open(p) if ln.strip() and not ln.startswith('#')]
    typ = []
    xyz = []
    rad = []
    for r in rd(am_path):
        typ.append(int(float(r[0])))
        xyz.append([float(r[1]) * 1000, float(r[2]) * 1000, float(r[3]) * 1000])
        rad.append(float(r[4]) * 1000)
    for r in rd(se_path):
        typ.append(3)
        xyz.append([float(r[1]) * 1000, float(r[2]) * 1000, float(r[3]) * 1000])
        rad.append(float(r[4]) * 1000)
    return np.array(typ), np.array(xyz, float), np.array(rad, float)


def hertz_loss(L, typ, xyz, rad, sc_dv):
    """ledger 규약: SC-SE Hertz 접촉면적(Σ R·ov) 손실 % (강체, sc_dv 수축)."""
    ci, cj, d, ov0 = L.build_contacts(xyz, rad)
    is_am = (typ[ci] == 1) | (typ[ci] == 2)
    is_am_j = (typ[cj] == 1) | (typ[cj] == 2)
    sc_se = ((typ[ci] == 2) & (typ[cj] == 3)) | ((typ[cj] == 2) & (typ[ci] == 3))
    Rstar = rad[ci] * rad[cj] / (rad[ci] + rad[cj])
    eps = sc_dv / 3.0                                          # ΔV(부피) → 반경 ε ≈ ΔV/3
    move = np.where(is_am, rad[ci] * eps, 0.0) + np.where(is_am_j, rad[cj] * eps, 0.0)
    A0 = Rstar * ov0
    Ach = Rstar * np.maximum(0.0, ov0 - move)
    return 100.0 * (1.0 - Ach[sc_se].sum() / max(A0[sc_se].sum(), 1e-30)), float(np.mean(ov0[sc_se]) * 1000.0)


def voxel_loss(typ, xyz, rad, sc_scale, ng, box_um=50.0):
    """MPM식 voxel-coverage(AM_S 표면 voxel 중 SE 인접 분율) 손실 % (강체, SC ×sc_scale, SE 고정)."""
    dx = box_um / ng
    lo = xyz.min(0) - 1.0

    def raster(sel, rscale):
        m = np.zeros((ng, ng, ng), bool)
        for i in sel:
            c = xyz[i] - lo
            r = rad[i] * rscale
            i0 = np.maximum(((c - r) / dx).astype(int), 0)
            i1 = np.minimum(((c + r) / dx).astype(int) + 1, ng)
            if np.any(i1 <= i0):
                continue
            gx = np.arange(i0[0], i1[0])
            gy = np.arange(i0[1], i1[1])
            gz = np.arange(i0[2], i1[2])
            X, Y, Z = np.meshgrid((gx + .5) * dx, (gy + .5) * dx, (gz + .5) * dx, indexing='ij')
            ins = ((X - c[0]) ** 2 + (Y - c[1]) ** 2 + (Z - c[2]) ** 2) <= r * r
            ii, jj, kk = np.nonzero(ins)
            m[gx[ii], gy[jj], gz[kk]] = True
        return m

    def cov(sc_s):
        amS = raster(np.where(typ == 2)[0], sc_s)
        se = raster(np.where(typ == 3)[0], 1.0)
        se &= ~amS
        surf = np.zeros_like(amS)
        adj = np.zeros_like(amS)
        for ax in range(3):
            for s in (1, -1):
                surf |= (np.roll(amS, s, ax) == False)
                adj |= np.roll(se, s, ax)
        surf &= amS
        return 100.0 * (surf & adj).sum() / max(surf.sum(), 1)

    c0 = cov(1.0)
    c1 = cov(sc_scale)
    return 100.0 * (1.0 - c1 / c0), c0, c1


def main(argv):
    ap = argparse.ArgumentParser(description='reflow 갭 분해 (지표 vs 재유동 반증)')
    ap.add_argument('--am-scaffold', required=True)
    ap.add_argument('--se-scaffold', required=True)
    ap.add_argument('--mpm-loss', type=float, required=True, help='MPM voxel-coverage SC 손실 % (앵커 실측)')
    ap.add_argument('--sc-dv', type=float, default=0.051, help='SC 부피 ΔV (기본 0.051 = Kondrakov)')
    ap.add_argument('--n-grid', type=int, default=256, help='voxel 격자 (384=MPM와 동일, 256=빠름)')
    a = ap.parse_args(argv)
    L = _ledger()
    typ, xyz, rad = _atoms(a.am_scaffold, a.se_scaffold)
    hl, ov_nm = hertz_loss(L, typ, xyz, rad, a.sc_dv)
    sc_scale = (1.0 - a.sc_dv) ** (1.0 / 3.0)
    vl, c0, c1 = voxel_loss(typ, xyz, rad, sc_scale, a.n_grid)
    dx_nm = 50.0 / a.n_grid * 1000
    move_nm = 2.0 * (a.sc_dv / 3.0) * 1000
    print('=' * 76)
    print(f'reflow 갭 분해 (SC ΔV −{a.sc_dv*100:.1f}%, 이동 {move_nm:.0f}nm, ov0 평균 {ov_nm:.0f}nm)')
    print(f'  voxel {dx_nm:.0f}nm (이동 = {move_nm/dx_nm:.2f} voxel; n_grid={a.n_grid})')
    print('-' * 76)
    print(f'  ledger Hertz-area 손실  = {hl:5.1f}%   (Σ R·ov, 연속, elastic 법칙)')
    print(f'  ledger RIGID voxel 손실 = {vl:5.1f}%   (MPM식 인접, 강체 = 재유동 없음)')
    print(f'  MPM voxel 손실          = {a.mpm_loss:5.1f}%   (재평형, 재유동 포함) [앵커 실측]')
    print('-' * 76)
    print(f'  지표+area법칙 (Hertz→voxel, 강체): {hl-vl:+5.1f}%p   ← 재유동 아님')
    print(f'  재평형/재유동 (voxel, 강체→MPM):  {vl-a.mpm_loss:+5.1f}%p   ← 진짜 MPM-only 몫')
    dom = '지표/법칙' if abs(hl - vl) > abs(vl - a.mpm_loss) else '재유동'
    print(f'  ⇒ 지배항 = {dom}.  같은(voxel) 지표선 ledger 강체({vl:.1f}%) ≈ MPM({a.mpm_loss:.1f}%) '
          f'= Δ{abs(vl-a.mpm_loss):.1f}%p (reflow 불필요)')
    print(f'  ⇒ "reflow={1-a.mpm_loss/max(hl,1e-9):.2f} = SE 재유동"은 오귀속; 대부분 Hertz↔voxel 지표차.')
    print('=' * 76)


if __name__ == '__main__':
    main(sys.argv[1:])
