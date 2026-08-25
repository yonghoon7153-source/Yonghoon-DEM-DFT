#!/usr/bin/env python3
"""펠릿 RVE σ 측정기 — D13 이온 보정의 실행 도구 (G2, 2026-08-25).

실행 계약: `docs/reviews/sdcp_ion_calib_prereg_20260825.md` (런 전 등록 — 표적·합격선은
그 문서가 정본이고 이 스크립트는 **측정기**다: σ 입력을 받아 σ_eff 를 돌려줄 뿐,
합격/기각을 판정하지 않는다).

무엇을 만드나 — 이 논문 Figure 2 의 펠릿(9:1 wt LPSCl:binder)을 복셀 RVE 로:
  · SE 매트릭스(sid 6)가 상자를 가득 채우고, binder 구(PTFE→sid 7 / SDCP→sid 5)를
    RSA(비겹침 순차 배치, x/y 주기)로 **스탬프-부피 기준** 참 vol% 까지 놓는다.
    wt→vol 은 리포 밀도 규약 (LPSCl 2.00 · PTFE 2.20 · SDCP 1.30 g/cm³):
    9:1 wt → PTFE 9.17 vol% · SDCP 14.60 vol% (prereg §1 산술과 selftest 가 대조).
  · PTFE 차단 노브(원장 ②)는 `step3_sigma.apply_ptfe_blocking` — **전극과 같은 함수**
    (사본 금지, R5-CX-09 규약) — 를 periodic_xy=True 로 부른다.
  · 솔브·σ 표도 생산 함수 그대로: `solve_sigma_z` + `ionic_sigma_table` /
    `electronic_sigma_table(sigma_se=…)` (④ 전용 훅, 기본 0 = 생산 불변).

이온/전자 **같은 sid 격자** → `input_digest` 가 정의상 동일 (음성 대조 §6-2 는 이 값의
기록으로 증명한다).  T2(z-스패닝 부재)용으로 binder 상의 연결성분(6-면, x/y wrap 포함)
크기 분포와 스패닝 여부를 기록한다.

v1 한계 (기록):
  · binder 구 지름은 **모델 파라미터**다 (--binder-d-um 필수; 실측 입도 없음 — §F1
    미지값은 스윕으로 다룬다).
  · z 는 비주기(플레이트) — z 경계를 걸친 구는 잘린다 (스탬프-부피 기준 목표라 vol% 는
    정확히 유지된다).
  · RSA 는 평형 배치가 아니다 (실물 혼합 무작위성의 프록시).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step3_sigma as s3                                    # noqa: E402

RHO = {'se': 2.00, 'ptfe': 2.20, 'sdcp': 1.30}              # g/cm³ — 리포 밀도 규약 (D13)
BINDER_SID = {'ptfe': 7, 'sdcp': 5}


def wt_to_vol(wt_binder, rho_se, rho_binder):
    """9:1 같은 질량비 → binder 부피분율.  prereg §1 의 산술과 같은 식."""
    v_se = (1.0 - wt_binder) / rho_se
    v_b = wt_binder / rho_binder
    return v_b / (v_se + v_b)


def _min_image_xy(d, box):
    """x/y 만 최소상 (z 는 비주기 플레이트)."""
    d = d.copy()
    for k in (0, 1):
        d[..., k] -= box * np.round(d[..., k] / box)
    return d


def build_rve(binder, vol_target, box_um, vox, d_um, seed, max_try=200000):
    """SE 매트릭스 + binder RSA 구.  목표는 **스탬프-부피 분율** (격자 기준 참 vol%).

    반환 (sid, centers, stamped_frac)."""
    n = int(round(box_um / vox))
    sid = np.full((n, n, n), 6, np.int8)
    if binder == 'none' or vol_target <= 0.0:
        return sid, np.zeros((0, 3)), 0.0
    bsid = BINDER_SID[binder]
    rng = np.random.default_rng(seed)
    r = d_um / 2.0
    ax = (np.arange(n) + 0.5) * vox
    centers = []
    n_cells = sid.size
    tries = 0
    while (sid == bsid).sum() / n_cells < vol_target:
        tries += 1
        if tries > max_try:
            raise RuntimeError(f'RSA 포화: {tries} 회에 vol {vol_target:.4f} 미달 '
                               f'(현재 {(sid == bsid).sum() / n_cells:.4f}) — box/d 재검토')
        c = rng.uniform(0.0, box_um, 3)
        if centers:
            dd = _min_image_xy(np.asarray(centers) - c, box_um)
            if (np.einsum('ij,ij->i', dd, dd) < (2 * r) ** 2).any():
                continue                                    # 비겹침 (표면 접촉까지 허용)
        # 스탬프 — x/y 주기 이미지 포함 (경계를 걸친 구가 반대편에 이어진다)
        for sx in (-box_um, 0.0, box_um):
            for sy in (-box_um, 0.0, box_um):
                cc = c + np.array([sx, sy, 0.0])
                i0 = np.maximum(0, np.floor((cc - r) / vox).astype(int))
                i1 = np.minimum(n - 1, np.ceil((cc + r) / vox).astype(int))
                if (i1 < i0).any():
                    continue
                gx, gy, gz = np.meshgrid(ax[i0[0]:i1[0] + 1], ax[i0[1]:i1[1] + 1],
                                         ax[i0[2]:i1[2] + 1], indexing='ij')
                m = (gx - cc[0]) ** 2 + (gy - cc[1]) ** 2 + (gz - cc[2]) ** 2 <= r * r
                sub = sid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
                sub[m] = bsid
        centers.append(c)
    return sid, np.asarray(centers), float((sid == bsid).sum() / n_cells)


def spanning_z(mask, wrap_xy=True):
    """binder 상의 z-스패닝 성분 검사 (T2) + 성분 크기 분포.

    6-면 연결 label 뒤 x/y wrap 면에서 맞닿는 label 을 union-find 로 합친다 —
    wrap 을 안 합치면 연결을 **과소**평가해 T2(비퍼콜 주장)가 거저 통과한다."""
    from scipy.ndimage import label
    lab, nl = label(mask)
    if nl == 0:
        return False, []
    parent = list(range(nl + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    if wrap_xy:
        for lo, hi in ((lab[0, :, :], lab[-1, :, :]), (lab[:, 0, :], lab[:, -1, :])):
            both = (lo > 0) & (hi > 0)
            for a, b in set(zip(lo[both].tolist(), hi[both].tolist())):
                union(a, b)
    root = np.array([find(i) for i in range(nl + 1)])
    lab = root[lab]
    ids, sizes = np.unique(lab[lab > 0], return_counts=True)
    z0 = set(np.unique(lab[:, :, 0])) - {0}
    z1 = set(np.unique(lab[:, :, -1])) - {0}
    spans = bool(z0 & z1)
    return spans, sorted((int(x) for x in sizes), reverse=True)


def measure(sid, vox, box_um, a):
    """이온·전자 두 솔브 (같은 격자 = 같은 digest)."""
    dig = hashlib.sha256(sid.tobytes() + np.int64(sid.shape).tobytes()
                         + np.float64([vox]).tobytes()).hexdigest()[:16]
    t_i = s3.ionic_sigma_table(a.sigma_ion_sdcp, a.sigma_ion_se)
    t_e = s3.electronic_sigma_table(0.0, 0.0, 0.0, 0.0, a.sigma_e_sdcp,
                                    sigma_se=a.sigma_e_se)
    kw = dict(z_top_um=box_um, z_bot_um=0.0, periodic_xy=True)
    r_i = s3.solve_sigma_z(sid, t_i, vox, **kw)
    r_e = s3.solve_sigma_z(sid, t_e, vox, **kw)
    return dig, r_i, r_e


def run(a):
    vol = 0.0 if a.binder == 'none' else wt_to_vol(a.wt_binder, RHO['se'], a.rho_binder)
    rows = []
    for k in range(a.seeds):
        seed = a.seed + k
        sid, cen, frac = build_rve(a.binder, vol, a.box_um, a.vox, a.binder_d_um, seed)
        n_blk = s3.apply_ptfe_blocking(sid, a.vox, a.ptfe_block_um, periodic_xy=True)
        dig, r_i, r_e = measure(sid, a.vox, a.box_um, a)
        spans, sizes = (spanning_z(sid == BINDER_SID[a.binder])
                        if a.binder != 'none' else (False, []))
        brug = a.sigma_ion_se * (1.0 - vol) ** 1.5
        row = {
            'seed': seed, 'binder': a.binder, 'wt_binder': a.wt_binder,
            'rho_binder_g_cm3': (a.rho_binder if a.binder != 'none' else None),
            'vol_target': vol, 'vol_stamped': frac, 'n_spheres': int(len(cen)),
            'binder_d_um': (a.binder_d_um if a.binder != 'none' else None),
            'box_um': a.box_um, 'vox_um': a.vox,
            'ptfe_block_um': a.ptfe_block_um, 'n_blocked_cells': n_blk,
            'input_digest': dig,                            # 이온=전자 같은 격자 (§6-2)
            'sigma_ion_se_S_cm': a.sigma_ion_se, 'sigma_ion_sdcp_S_cm': a.sigma_ion_sdcp,
            'sigma_e_se_S_cm': a.sigma_e_se, 'sigma_e_sdcp_S_cm': a.sigma_e_sdcp,
            'sigma_ion_eff_S_cm': r_i['sigma_eff'], 'sigma_e_eff_S_cm': r_e['sigma_eff'],
            'sigma_ion_eff_mS_cm': r_i['sigma_eff'] * 1e3,
            'formation_factor_ion': (r_i['sigma_eff'] / a.sigma_ion_se
                                     if a.sigma_ion_se > 0 else None),
            'bruggeman_dilution_mS_cm': brug * 1e3,         # §6-1 기록 관측량 (게이트 아님)
            'ion_unconverged': bool(r_i.get('unconverged')),
            'e_unconverged': bool(r_e.get('unconverged')),
            'binder_spans_z': spans, 'binder_component_sizes_top5': sizes[:5],
            'binder_n_components': len(sizes),
        }
        rows.append(row)
        print(f"  seed {seed}: σ_ion {row['sigma_ion_eff_mS_cm']:.4f} mS/cm "
              f"(F={row['formation_factor_ion'] if row['formation_factor_ion'] is None else round(row['formation_factor_ion'], 4)}) · "
              f"σ_e {row['sigma_e_eff_S_cm']:.4e} S/cm · binder {frac * 100:.2f} vol% "
              f"({len(cen)} 구) · blocked {n_blk} · spans_z={spans}", flush=True)
    #  ⚠ dict-union `|` 금지 — kgy dem-venv 는 Python 3.8 이다 (실측 TypeError, 2026-08-25)
    out = {'arm': {**vars(a), 'out': None}, 'rows': rows}
    if len(rows) > 1:
        li = np.log10([r['sigma_ion_eff_S_cm'] for r in rows if r['sigma_ion_eff_S_cm'] > 0])
        le = np.log10([r['sigma_e_eff_S_cm'] for r in rows if r['sigma_e_eff_S_cm'] > 0])
        out['agg'] = {
            'sigma_ion_eff_mS_cm_mean': float(np.mean([r['sigma_ion_eff_mS_cm'] for r in rows])),
            'log10_ion_se': (float(np.std(li, ddof=1) / np.sqrt(len(li))) if len(li) > 1 else None),
            'log10_e_se': (float(np.std(le, ddof=1) / np.sqrt(len(le))) if len(le) > 1 else None),
            'any_spans_z': bool(any(r['binder_spans_z'] for r in rows)),
        }
        print(f"  ── {len(rows)} 시드: ⟨σ_ion⟩ {out['agg']['sigma_ion_eff_mS_cm_mean']:.4f} mS/cm · "
              f"SE(log10) ion {out['agg']['log10_ion_se']} / e {out['agg']['log10_e_se']} · "
              f"spans_z(any) {out['agg']['any_spans_z']}", flush=True)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print(f"  → {a.out}")
    return out


def _selftest():
    ok = True

    def chk(name, c):
        nonlocal ok
        ok &= bool(c)
        print(('  PASS  ' if c else '  FAIL  ') + name)

    # 1) wt→vol 산술 = prereg §1 (9.17 / 14.60 vol%)
    chk('1) wt→vol: PTFE 9:1 → 9.17 vol%',
        abs(wt_to_vol(0.10, 2.00, 2.20) - 0.0917) < 5e-4)
    chk('2) wt→vol: SDCP 9:1 → 14.60 vol%',
        abs(wt_to_vol(0.10, 2.00, 1.30) - 0.1460) < 5e-4)

    # 3) neat 균일 매트릭스 → F = 1 (정확)
    sid = np.full((8, 8, 12), 6, np.int8)
    r = s3.solve_sigma_z(sid, s3.ionic_sigma_table(0.0, 3.0e-3), 0.25,
                         z_top_um=3.0, z_bot_um=0.0, periodic_xy=True)
    chk(f'3) neat 균일: F = {r["sigma_eff"] / 3.0e-3:.6f} (1.0)',
        abs(r['sigma_eff'] / 3.0e-3 - 1.0) < 1e-4)

    # 4) RSA — 비겹침(주기 최소상) + 스탬프-부피가 목표 이상 + 재현성(같은 시드 = 같은 격자)
    sidA, cenA, frA = build_rve('sdcp', 0.146, 6.0, 0.2, 1.5, seed=7)
    sidB, _, _ = build_rve('sdcp', 0.146, 6.0, 0.2, 1.5, seed=7)
    sidC, _, _ = build_rve('sdcp', 0.146, 6.0, 0.2, 1.5, seed=8)
    if len(cenA) > 1:
        dd = _min_image_xy(cenA[None, :, :] - cenA[:, None, :], 6.0)
        pd = np.sqrt(np.einsum('ijk,ijk->ij', dd, dd))
        np.fill_diagonal(pd, 1e9)
        chk(f'4) RSA 비겹침: min 쌍거리 {pd.min():.3f} ≥ d 1.5', pd.min() >= 1.5 - 1e-9)
    chk(f'5) 스탬프-부피 목표 도달: {frA * 100:.2f} ≥ 14.60 vol%', frA >= 0.146)
    chk('6) 같은 시드 → 같은 격자 · 다른 시드 → 다른 격자',
        bool((sidA == sidB).all()) and not bool((sidA == sidC).all()))

    # 7) 방향: binder 가 σ 를 깎는다 (희석) — Bruggeman 은 기록 관측량 (게이트 아님, §6-1)
    ri = s3.solve_sigma_z(sidA, s3.ionic_sigma_table(0.0, 3.0e-3), 0.2,
                          z_top_um=6.0, z_bot_um=0.0, periodic_xy=True)
    chk(f'7) 희석 방향: σ {ri["sigma_eff"] * 1e3:.3f} < neat 3.0 mS/cm',
        0.0 < ri['sigma_eff'] < 3.0e-3)

    # 8) z-스패닝 검출기 — wrap 을 통해서만 이어지는 성분을 놓치지 않는다
    m = np.zeros((6, 4, 8), bool)
    m[0, 1, 0:4] = True                                     # x=0 기둥 (아래 절반)
    m[-1, 1, 3:8] = True                                    # x=끝 기둥 (위 절반, z=3 겹침)
    sp_w, sz_w = spanning_z(m, wrap_xy=True)
    sp_n, _ = spanning_z(m, wrap_xy=False)
    chk('8) 스패닝: wrap 이어야 z-관통 (wrap True / no-wrap False)', sp_w and not sp_n)
    chk(f'9) 성분 크기 분포 기록: {sz_w}', sz_w == [9])

    # 10) PTFE 차단이 펠릿 경로에서도 발화 + 이온 σ 추가 하락 (전극과 같은 공유 함수)
    sidP, _, _ = build_rve('ptfe', 0.0917, 6.0, 0.2, 1.5, seed=11)
    sidP2 = sidP.copy()
    nb = s3.apply_ptfe_blocking(sidP2, 0.2, 0.21, periodic_xy=True)
    r0 = s3.solve_sigma_z(sidP, s3.ionic_sigma_table(0.0, 3.0e-3), 0.2,
                          z_top_um=6.0, z_bot_um=0.0, periodic_xy=True)
    r1 = s3.solve_sigma_z(sidP2, s3.ionic_sigma_table(0.0, 3.0e-3), 0.2,
                          z_top_um=6.0, z_bot_um=0.0, periodic_xy=True)
    chk(f'10) 차단 {nb} 셀 → σ_ion {r0["sigma_eff"] * 1e3:.3f} → {r1["sigma_eff"] * 1e3:.3f} 하락',
        nb > 0 and r1['sigma_eff'] < r0['sigma_eff'])

    # 11) 전자 훅 sigma_se: 기본 0 이면 neat 전자 σ = 0, 훅을 주면 유한
    re0 = s3.solve_sigma_z(np.full((6, 6, 8), 6, np.int8),
                           s3.electronic_sigma_table(0, 0, 0, 0, 0), 0.25,
                           z_top_um=2.0, z_bot_um=0.0, periodic_xy=True)
    re1 = s3.solve_sigma_z(np.full((6, 6, 8), 6, np.int8),
                           s3.electronic_sigma_table(0, 0, 0, 0, 0, sigma_se=3e-8), 0.25,
                           z_top_um=2.0, z_bot_um=0.0, periodic_xy=True)
    chk(f'11) 전자 훅: 기본 σ_e=0 (생산 불변) · sigma_se=3e-8 → {re1["sigma_eff"]:.2e}',
        re0['sigma_eff'] == 0.0 and abs(re1['sigma_eff'] / 3e-8 - 1.0) < 1e-4)

    print(f'pellet_rve_sigma selftest: {"PASS" if ok else "FAIL"}')
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--binder', choices=('none', 'ptfe', 'sdcp'), default='none')
    ap.add_argument('--wt-binder', type=float, default=0.10, help='binder 질량분율 (9:1 = 0.10)')
    ap.add_argument('--rho-binder', type=float, default=None,
                    help='binder 밀도 g/cm³ (기본: PTFE 2.20 / SDCP 1.30 — ρ_SDCP 감도는 '
                         '1.1/1.7 로 override, prereg §4)')
    ap.add_argument('--binder-d-um', type=float, default=None,
                    help='binder 구 지름 µm — **모델 파라미터** (실측 입도 없음, §F1: 스윕)')
    ap.add_argument('--box-um', type=float, default=18.0)
    ap.add_argument('--vox', type=float, default=0.12)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--seeds', type=int, default=1, help='시드 반복 (prereg: ≥4)')
    ap.add_argument('--ptfe-block-um', type=float, default=0.0,
                    help='원장 ② 노브 — step3_sigma.apply_ptfe_blocking (전극과 같은 함수)')
    ap.add_argument('--sigma-ion-se', type=float, default=3.0e-3, help='S/cm (① 보정 대상)')
    ap.add_argument('--sigma-ion-sdcp', type=float, default=0.0, help='S/cm (③ — 기대 ≈불활성)')
    ap.add_argument('--sigma-e-se', type=float, default=0.0, help='S/cm (④ — neat 전자 정규화)')
    ap.add_argument('--sigma-e-sdcp', type=float, default=0.0, help='S/cm (⑥ — σ_SDCP=250 대체 후보)')
    ap.add_argument('--out', default=None, help='JSON 출력 경로')
    a = ap.parse_args(argv)
    if a.selftest:
        return _selftest()
    if a.binder != 'none':
        if a.binder_d_um is None:
            ap.error('--binder-d-um 필수 (모델 파라미터 — §F1: 값을 지어내지 않는다)')
        if a.rho_binder is None:
            a.rho_binder = RHO[a.binder]
    if a.ptfe_block_um > 0 and a.binder != 'ptfe':
        ap.error('--ptfe-block-um 은 --binder ptfe 에서만 뜻이 있다 (그 외 침대엔 no-op '
                 '— 실수로 준 것일 가능성이 높아 fail-closed)')
    run(a)
    return 0


if __name__ == '__main__':
    sys.exit(main())
