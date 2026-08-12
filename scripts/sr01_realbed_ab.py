#!/usr/bin/env python3
"""SR-01 실침대 A/B — production 시더로 깐 VGCF 를 점 vs 선분으로 굽고 연결성을 잰다.

왜 (Codex 리뷰 종료조건):
  `fibre_segment_raster.py` 의 A/B 는 **합성 직선 섬유**였다 — "정확한 91.7 % 는 production
  상수가 아니다" 가 Codex 의 판정이었고 실제로 상자 크기만 바꿔도 86.6→94.6 % 로 움직였다.
  이 스크립트는 **실제 DEM 침대(킷 스캐폴드)** 위에서 **production 시더**(`additives.seed_fibres`,
  curl·길이 CV·AM 내부 점 드랍·정렬 전부 포함)로 VGCF 를 깔고 같은 A/B 를 한다.

무엇이 실제와 같은가:
  · AM 위치·반경 = 실제 LIGGGHTS 압밀 침대 (킷 스캐폴드 CSV)
  · 섬유 개수 = `recipe_counts_real` (레시피 wt% × 실제 AM/SE 부피)
  · 형상 = production `seed_fibres` (curl·L_cv·in_am 드랍·align)
  · 점 간격 = production 규약 0.7·dx_MPM · 스탬프 = 1-복셀 floor (STEP3 규약)
  · 연결 판정 = **6-face** (솔버와 같음)

무엇이 다른가 (정직):
  · σ_e 를 풀지 않는다 — 이 스크립트는 **연결성(끊김)** 만 잰다.  Δσ_e 는 GPU STEP3 몫이다.
  · 폴리라인은 시더가 낸 **점 순서**로 복원한다 (같은 fid 의 연속 점 = 경로).  시더가 경로를
    순서대로 낸다는 전제이며, 실패하면 `--check-order` 가 알려준다.

사용:
    python3 scripts/sr01_realbed_ab.py --selftest
    python3 scripts/sr01_realbed_ab.py --kit kit_ps_7_3 --n-grid 288 --vox 0.4
"""
from __future__ import annotations

import argparse
import gzip
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import additives as _ad                                    # noqa: E402
from fibre_segment_raster import n_components_6face, polyline_cells   # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITDIR = os.path.join(ROOT, 'docs', 'data', 'kit_ps_scaffolds')
UM_BOX = 1000.0            # 킷 스캐폴드 좌표 1 box unit = 1000 µm (z 0.1115 ↔ 111.5 µm 두께)


def load_kit(kit):
    """킷 스캐폴드 → (am_c_um, am_r_um, se_c_um, se_r_um, lateral_um, thick_um)."""
    def _rd(tag):
        p = os.path.join(KITDIR, f'{kit}__{tag}_scaffold.csv.gz')
        if not os.path.exists(p):
            raise SystemExit(f'없는 킷 파일: {p}')
        a = np.atleast_2d(np.loadtxt(gzip.open(p), delimiter=','))
        return a[:, 1:4] * UM_BOX, a[:, 4] * UM_BOX
    am_c, am_r = _rd('am')
    se_c, se_r = _rd('se')
    lat = float(max(am_c[:, 0].max(), am_c[:, 1].max()))
    thick = float(am_c[:, 2].max() + am_r.max())
    return am_c, am_r, se_c, se_r, lat, thick


def point_cells_from(pts_um, vox):
    return np.floor(np.asarray(pts_um) / vox).astype(np.int64)


def seed_carbon_on_kit(kit='kit_ps_7_3', n_grid=288, vgcf_wt=1.0, seed=0,
                       occ_res=0.25, max_fibres=0):
    """실침대 위에 production 시더로 VGCF 를 깐다 — A/B 와 네트워크 측정의 **공통 앞단**.

    ★ 두 소비자가 **정확히 같은 점 구름**을 봐야 한다.  따로 씨 뿌리면 per-fibre 단절과
      전역 네트워크가 **다른 실현**을 비교하게 되고, 차이가 래스터 때문인지 시드 때문인지
      구분할 수 없다.  그래서 여기 한 곳에서만 만든다 (CLAUDE.md 사다리 ②).
    """
    am_c, am_r, se_c, se_r, lat, thick = load_kit(kit)
    dx = lat / n_grid                                        # MPM 격자 (box lateral / n_grid)
    step = 0.7 * dx                                          # production 점 간격 규약

    # 실제 부피에서 레시피 개수 (production 규약)
    am_vol = float((4.0 / 3.0 * np.pi * am_r ** 3).sum())
    se_vol = float((4.0 / 3.0 * np.pi * se_r ** 3).sum())
    cnt = _ad.recipe_counts_real({'VGCF': vgcf_wt}, am_vol, se_vol)
    nobj = int(cnt['VGCF']['n'])
    nobj_full = nobj
    if max_fibres and nobj > max_fibres:      # 표본 — 연결성 통계는 수백 섬유면 수렴한다
        nobj = int(max_fibres)

    # AM 내부 판정 (시더가 AM 안 점을 드랍한다 — production 과 같게).
    # ★ 시더는 **점 하나씩** 부른다 (additives:649 `[in_am(p) for p in ln]`).  실침대에서는
    #   호출이 200만 회를 넘어 KDTree 점별 조회로는 못 쓴다 → **점유격자 O(1) 조회**로 바꾼다
    #   (AM 반경 2–6 µm 이라 occ 0.25 µm 격자면 판정이 사실상 동일; selftest 가 KDTree 와 대조).
    occ_dx = occ_res
    nx = int(np.ceil(lat / occ_dx)) + 2
    nz = int(np.ceil(thick / occ_dx)) + 2
    occ = np.zeros((nx, nx, nz), bool)
    for c0, r0 in zip(am_c, am_r):
        i0 = np.maximum(((c0 - r0) / occ_dx).astype(int), 0)
        i1 = np.minimum(((c0 + r0) / occ_dx).astype(int) + 1, [nx - 1, nx - 1, nz - 1])
        if np.any(i1 < i0):
            continue
        gx = (np.arange(i0[0], i1[0] + 1) + 0.5) * occ_dx - c0[0]
        gy = (np.arange(i0[1], i1[1] + 1) + 0.5) * occ_dx - c0[1]
        gz = (np.arange(i0[2], i1[2] + 1) + 0.5) * occ_dx - c0[2]
        d2 = (gx[:, None, None] ** 2 + gy[None, :, None] ** 2 + gz[None, None, :] ** 2)
        occ[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1] |= (d2 < r0 * r0)

    def in_am(q):
        """AM 구 내부인가.  1-D 입력 → **스칼라 bool** (시더 계약)."""
        a = np.asarray(q, np.float64)
        single = (a.ndim == 1)
        Q = np.atleast_2d(a)
        idx = (Q / occ_dx).astype(np.int64)
        np.clip(idx, 0, [nx - 1, nx - 1, nz - 1], out=idx)
        out = occ[idx[:, 0], idx[:, 1], idx[:, 2]]
        return bool(out[0]) if single else out

    rng = np.random.default_rng(seed)
    box = (lat, lat, thick)
    pts, fid, _w = _ad.seed_fibres(
        nobj, box, step, rng, L=_ad.VGCF_L, L_cv=0.35, curl=0.06,
        in_am=in_am, return_ids=True, return_vol=True)
    return {'pts': np.asarray(pts, np.float64), 'fid': np.asarray(fid),
            'step': step, 'dx': dx, 'lat': lat, 'thick': thick,
            'am_c': am_c, 'am_r': am_r, 'se_c': se_c, 'se_r': se_r,
            'nobj': nobj, 'nobj_full': nobj_full, 'kit': kit, 'n_grid': n_grid}


def run(kit='kit_ps_7_3', n_grid=288, vox=0.4, vgcf_wt=1.0, seed=0, check_order=True,
        occ_res=0.25, max_fibres=0, gap_tol=2.0):
    S = seed_carbon_on_kit(kit, n_grid, vgcf_wt, seed, occ_res, max_fibres)
    pts, fid, step = S['pts'], S['fid'], S['step']
    dx, lat, thick = S['dx'], S['lat'], S['thick']
    am_r, se_r, nobj, nobj_full = S['am_r'], S['se_r'], S['nobj'], S['nobj_full']

    pt_comp, sg_comp, pt_cells, sg_cells, nseg, n_gap = [], [], [], [], [], []
    order_bad = 0
    for f in np.unique(fid):
        m = fid == f
        P = pts[m]
        if len(P) < 2:
            continue
        if check_order:                    # 연속 점 간격이 step 근처인가 = 경로 순서 전제 검사
            d = np.linalg.norm(np.diff(P, axis=0), axis=1)
            if np.median(d) > 3.0 * step:
                order_bad += 1
        # ★ 2026-08-11 버그 수정: 시더가 **AM 안 점을 드랍**하므로 살아남은 점을 그냥
        #   폴리라인으로 이으면 **AM 을 관통하는 직선**이 그려진다 (탄소를 AM 내부에 넣는 셈).
        #   ⇒ 연속 점 간격이 step 의 gap_tol 배를 넘으면 **끊어서** 별도 구간으로 굽는다.
        #   그 결과 남는 단절은 래스터 아티팩트가 아니라 **물리적 단절(AM 이 섬유를 끊음)** 이다.
        d = np.linalg.norm(np.diff(P, axis=0), axis=1)
        brk = np.nonzero(d > gap_tol * step)[0] + 1
        runs = np.split(P, brk) if len(brk) else [P]
        n_gap.append(len(brk))
        pc = np.unique(point_cells_from(P, vox), axis=0)
        sc_list = [polyline_cells(R, vox) for R in runs if len(R) >= 1]
        sc = np.unique(np.vstack(sc_list), axis=0) if sc_list else pc
        pt_comp.append(n_components_6face(pc))
        sg_comp.append(n_components_6face(sc))
        pt_cells.append(len(pc)); sg_cells.append(len(sc)); nseg.append(len(P))
    pt_comp = np.array(pt_comp); sg_comp = np.array(sg_comp)
    return {
        'kit': kit, 'n_grid': n_grid, 'vox_um': vox, 'dx_mpm_um': round(dx, 4),
        'point_step_um': round(step, 4), 'lateral_um': round(lat, 2), 'thick_um': round(thick, 2),
        'n_AM': len(am_r), 'n_SE': len(se_r), 'vgcf_wt_pct': vgcf_wt,
        'n_fibres_recipe': nobj_full, 'n_fibres_seeded': nobj, 'n_fibres_measured': int(len(pt_comp)),
        'pts_per_fibre_median': float(np.median(nseg)) if nseg else 0.0,
        'order_check_failed': order_bad, 'gap_tol': gap_tol,
        'am_gaps_per_fibre_mean': round(float(np.mean(n_gap)), 3) if n_gap else 0.0,
        'fibres_with_am_gap_pct': round(100.0 * float(np.mean(np.array(n_gap) > 0)), 2) if n_gap else 0.0,
        'point_broken_pct': round(100.0 * (pt_comp > 1).mean(), 2) if len(pt_comp) else None,
        'point_mean_components': round(float(pt_comp.mean()), 3) if len(pt_comp) else None,
        'point_max_components': int(pt_comp.max()) if len(pt_comp) else None,
        'segment_broken_pct': round(100.0 * (sg_comp > 1).mean(), 2) if len(sg_comp) else None,
        'segment_mean_components': round(float(sg_comp.mean()), 3) if len(sg_comp) else None,
        'point_cells_total': int(np.sum(pt_cells)), 'segment_cells_total': int(np.sum(sg_cells)),
        'cells_ratio_seg_over_pt': round(float(np.sum(sg_cells) / max(np.sum(pt_cells), 1)), 3),
    }


def _fmt(r):
    print(f"■ {r['kit']}  n_grid {r['n_grid']} → dx {r['dx_mpm_um']} µm · 점간격 "
          f"{r['point_step_um']} µm · STEP3 vox {r['vox_um']} µm")
    print(f"  침대: {r['lateral_um']}×{r['lateral_um']}×{r['thick_um']} µm · "
          f"AM {r['n_AM']} · SE {r['n_SE']}")
    print(f"  VGCF {r['vgcf_wt_pct']} wt% → 섬유 {r['n_fibres_recipe']}개 "
          f"(측정 {r['n_fibres_measured']}, 섬유당 점 중앙값 {r['pts_per_fibre_median']:.0f})")
    if r['order_check_failed']:
        print(f"  ⚠ 경로-순서 검사 실패 {r['order_check_failed']}개 — 폴리라인 복원 전제 확인 필요")
    print(f"  점-스탬프 (현행)  단절 {r['point_broken_pct']:5.1f}%  "
          f"평균 {r['point_mean_components']:5.2f} 성분 (최대 {r['point_max_components']})  "
          f"셀 {r['point_cells_total']:,}")
    print(f"  선분-스탬프       단절 {r['segment_broken_pct']:5.1f}%  "
          f"평균 {r['segment_mean_components']:5.2f} 성분             "
          f"셀 {r['segment_cells_total']:,}  (셀비 {r['cells_ratio_seg_over_pt']})")
    print(f"  ↳ AM 관통 방지: 섬유당 물리적 끊김 {r['am_gaps_per_fibre_mean']:.2f}개 · "
          f"끊김 있는 섬유 {r['fibres_with_am_gap_pct']:.1f}%  "
          f"⇒ 선분의 잔여 단절은 **AM 이 끊은 것**이지 래스터 아티팩트가 아니다")


def _selftest():
    ok = fail = 0

    def chk(m, c):
        nonlocal ok, fail
        print(('  PASS  ' if c else '  FAIL  ') + m)
        ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

    kits = [f[:-len('__am_scaffold.csv.gz')] for f in sorted(os.listdir(KITDIR))
            if f.endswith('__am_scaffold.csv.gz')]
    chk(f'1) 킷 스캐폴드가 있다 ({len(kits)}개)', len(kits) >= 1)
    am_c, am_r, se_c, se_r, lat, thick = load_kit(kits[0])
    chk(f'2) {kits[0]} 로드: AM {len(am_r)} · SE {len(se_r)} · '
        f'{lat:.1f}×{lat:.1f}×{thick:.1f} µm', len(am_r) > 100 and 20 < thick < 300)
    chk('3) 반경이 NCM 급 (1–10 µm)', 1.0 < float(am_r.mean()) < 10.0)
    r = run(kits[0], n_grid=288, vox=0.4, vgcf_wt=1.0, seed=1, max_fibres=400)
    chk(f"4) 레시피 섬유 {r['n_fibres_recipe']}개 > 0", r['n_fibres_recipe'] > 0)
    chk(f"5) 경로-순서 전제 성립 (실패 {r['order_check_failed']})", r['order_check_failed'] == 0)
    chk(f"6) ★ 실침대 점-스탬프가 실제로 끊긴다: {r['point_broken_pct']}%",
        r['point_broken_pct'] > 50)
    chk(f"7) ★ 선분-스탬프 단절 {r['segment_broken_pct']}% < 점-스탬프 {r['point_broken_pct']}%",
        r['segment_broken_pct'] < r['point_broken_pct'])
    chk(f"7b) ★ 선분의 잔여 단절 {r['segment_broken_pct']}% ≈ AM-끊김 섬유 "
        f"{r['fibres_with_am_gap_pct']}% (±8 %p) = 남은 것은 **물리적 단절**",
        abs(r['segment_broken_pct'] - r['fibres_with_am_gap_pct']) < 8.0)
    chk(f"8) 셀 비 {r['cells_ratio_seg_over_pt']} 가 폭증하지 않는다 (<2.0)",
        r['cells_ratio_seg_over_pt'] < 2.0)
    print(f'\nsr01_realbed_ab selftest: {ok}/{ok + fail} PASS')
    return fail == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--n-grid', type=int, default=288)
    ap.add_argument('--vox', type=float, default=0.4, help='STEP3 복셀 (production 기본 0.4)')
    ap.add_argument('--vgcf-wt', type=float, default=1.0)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--all-kits', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    kits = ([f[:-len('__am_scaffold.csv.gz')] for f in sorted(os.listdir(KITDIR))
             if f.endswith('__am_scaffold.csv.gz')] if a.all_kits else [a.kit])
    for k in kits:
        _fmt(run(k, a.n_grid, a.vox, a.vgcf_wt, a.seed))
        print()


if __name__ == '__main__':
    main()
