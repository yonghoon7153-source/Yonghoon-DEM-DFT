#!/usr/bin/env python3
"""SDCP **점-스탬프 교란**을 GPU 없이 잰다 — 목표 B 의 조건 ③(기전 분리)를 선점한다.

★ 무엇을 묻나 (CL-25):
  생산 STEP3 는 SDCP 를 **입자당 셀 하나**로 찍는다 (`seed_sdcp` singles = 입자당 점 1개,
  `step3_sigma` 첨가제 경로 = `np.floor` 셀 하나).  그러면 한 입자가 **vox³** 을 차지해
  참부피 π/6·(0.3)³ = 0.014137 µm³ 의 **4.53× (vox 0.4) · 1.91 (0.3) · 1.11 (0.25)** 가 된다.
  ⇒ "격자를 조이면 DBE 이득이 준다" 가 **SDCP 가 홀쭉해져서**일 수 있다 — 그러면 이득의
  기전이 물리(혼합전도 SDCP)가 아니라 **스탬프 인공물**이다.  원고의 헤드라인이 걸린 지점.

★ 어떻게 GPU 없이 되나:
  `step3_sigma.solve_sigma_z` 가 sid 배열을 직접 받는다.  같은 SDCP 중심 좌표를
  **① 참 구(Ø0.30 µm)로 래스터** vs **② 생산 점-스탬프** 두 규약으로 각각 굽고, 나머지
  (AM·SE·격자·origin)를 **완전히 고정**한 채 σ_e 만 비교한다.  차이는 정의상 스탬프 것뿐이다.

★ 이 시험이 실침대와 다른 점 (넘겨짚지 말 것):
  · 침대가 다르다 — 킷 스캐폴드의 AM/SE + **합성 SDCP 배치**다 (실제 seed_sdcp 배치 아님).
  · 그래서 나오는 것은 **기전의 크기와 부호**이지 실침대 보정계수가 아니다.
  · 실침대 값은 여전히 GPU 원장(상별 `count(sid)·vox³` vs 레시피)이 필요하다.

사용:
  python3 scripts/sdcp_stamp_confound.py --vox 0.4 0.3 0.25 0.2 0.15
  python3 scripts/sdcp_stamp_confound.py --selftest
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from step3_sigma import solve_sigma_z                            # noqa: E402
from step3_transport_resolution import (SDCP_D_UM, SID_AM, SID_SDCP, SID_SE,  # noqa: E402
                                        SIGMA_E_AM, SIGMA_E_SDCP,
                                        rasterize_spheres, sdcp_point_cells)


def build(vox, origin, length_um, am, se, sdcp_c, mode, lattice_shift=None):
    """sid 격자.  `mode` = 'sphere'(참 구) | 'point'(생산 점-스탬프) | 'none'.

    ⚠ origin 앙상블은 `origin`(물리 crop 창)이 아니라 `lattice_shift`(격자 위상)로 한다
      — Codex CDX-R2-01.  crop 을 움직이면 팔마다 SDCP/SE 표본이 달라져 위상 효과와
      표본 효과가 섞인다.
    """
    sh = np.zeros(3) if lattice_shift is None else np.asarray(lattice_shift, float)
    sid = rasterize_spheres(vox, origin, length_um, [(se[0], se[1], SID_SE),
                                                     (am[0], am[1], SID_AM)],
                            lattice_shift=sh)
    #  ★★ 2026-08-18 (심층 리뷰 ② B1) — **축별** 크기로 클립한다.
    #    옛 판은 `n = sid.shape[0]` 하나로 세 축을 전부 클립했다.  `rasterize_spheres` 는
    #    **이동한 축만** +1 셀을 주므로(step3_transport_resolution.py:79) sh=(h,0,0) 이면
    #    격자가 (134, 133, 133) 인데 y·z 를 134 로 클립해 **범위 밖 인덱스가 통과**한다.
    #    재현: `--len-um 20 --vox 0.15`, sh=(0.075,0,0) →
    #      IndexError: index 133 is out of bounds for axis 1 with size 133
    #    ⇒ CL-31 이 "진행중" 이라 적어둔 vox 0.2/0.15 팔은 **오늘 그대로 죽는다**.
    #    (docstring 기본 `--len-um 12` 는 12/0.15=80 이 정수라 우연히 안 죽어 selftest 가 놓쳤다.)
    n3 = np.array(sid.shape)
    if mode == 'sphere':
        #  ★★ 생산 게이트 미러 (리뷰 ② B2) — 옛 판에는 **게이트가 없었다**.
        #    셀-중심-in-구 래스터는 d/vox 가 작으면 입자를 통째로 잃는다.  실측(입자 5,659):
        #      vox 0.4  d/vox 0.75 → 셀0 입자 **78.7 %** (부피/참 0.961 — 총 부피는 멀쩡해 보인다)
        #      vox 0.3  1.00 → **47.8 %** (0.991) · vox 0.25 1.20 → **19.3 %** (1.006)
        #      vox 0.2  1.50 →   1.0 % (1.000) · vox 0.15 2.00 → **0.0 %** (0.979)
        #    ⇒ 총 부피비가 1 근처라 **눈에 안 띈다** — 살아남은 입자가 정확히 1 셀씩 먹어
        #      상쇄하기 때문이다.  그러나 공간 분포는 "입자의 78 % 를 무작위로 지운 것" 이다.
        #    생산(step3_sigma.py:286)이 fail-closed 로 막는 영역을 여기서만 열어두면
        #      두 도구가 **다른 것을 재고도 같은 이름으로 보고**하게 된다.
        if len(sdcp_c) and SDCP_D_UM / vox < 2.0:
            raise ValueError(
                f'구 스탬프 d/vox = {SDCP_D_UM / vox:.2f} < 2 거부 (생산 게이트와 동일).  '
                f'이 격자에서는 입자의 상당수가 셀 0 개가 된다 — 총 부피비는 1 근처라 '
                f'멀쩡해 보이지만 공간 분포가 틀린다.  vox ≤ {SDCP_D_UM / 2:.3f} µm 를 쓸 것')
        r = np.full(len(sdcp_c), SDCP_D_UM / 2.0)
        add = rasterize_spheres(vox, origin, length_um, [(sdcp_c, r, SID_SDCP)],
                                lattice_shift=sh)
        sid[add == SID_SDCP] = SID_SDCP
    elif mode == 'point':
        #  격자 위상 이동 = 셀 경계가 −s 만큼 밀린 것과 같다 → floor((p−origin+s)/vox)
        #  ⚠ 사전 창(`rel < length_um + sh`)은 지웠다 — 축별 클립이 유일한 판정자여야
        #    구 경로(rasterize_spheres 도 n3 로 클립)와 **같은 입자 집합**이 된다.
        rel = np.asarray(sdcp_c, float) - np.asarray(origin, float) + sh
        ijk = np.floor(rel / vox).astype(int)
        ijk = ijk[((ijk >= 0) & (ijk < n3)).all(1)]
        if len(ijk):
            sid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = SID_SDCP
    return sid


def run(am, se, sdcp_c, base_origin, length_um, voxes, n_origin=8):
    sig = np.zeros(9)
    sig[SID_AM] = SIGMA_E_AM
    sig[SID_SDCP] = SIGMA_E_SDCP                                 # SE·기공 = 전자 절연
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    rows = []
    for vox in voxes:
        import itertools as _it
        shifts = [np.array(t) for t in _it.product((0.0, vox / 2.0), repeat=3)][:n_origin]
        res, gate = {}, None
        for mode in ('none', 'sphere', 'point'):
            vals, vol, unc = [], [], []
            try:
                for sh in shifts:
                    sid = build(vox, base_origin, length_um, am, se, sdcp_c, mode,
                                lattice_shift=sh)
                    r_ = solve_sigma_z(sid, sig, vox, area_um2=length_um * length_um)
                    vals.append(float(r_['sigma_eff']))
                    vol.append(float((sid == SID_SDCP).sum()) * vox ** 3)
                    #  ★ 미수렴을 **버리지 않는다** (리뷰 ② H2) — 옆 도구
                    #    `step3_transport_resolution.py:117` 는 이미 이것을 읽는데 여기만 빠졌다.
                    unc.append(bool(r_.get('unconverged'))
                               or int(r_.get('cg_info', 0) or 0) != 0)
            except ValueError as _e:                       # 구 게이트 (d/vox < 2)
                gate = str(_e)
                res[mode] = None
                continue
            res[mode] = {'sig': np.array(vals), 'vol': float(np.mean(vol)) if vol else 0.0,
                         'unconverged': bool(any(unc))}
        row = {
            'vox': float(vox),
            'sdcp_d_per_dx': float(f'{SDCP_D_UM / vox:.3f}'),
            'sphere_gate_rejected': gate,
            'unconverged_any': bool(any(v['unconverged'] for v in res.values() if v)),
        }
        for mode in ('none', 'sphere', 'point'):
            v = res.get(mode)
            row[f'sigma_e_{mode}'] = float(f'{v["sig"].mean():.6g}') if v else None
            #  ★ origin 폭을 **세 팔 모두** 보고한다 (리뷰 ② H5) — 옛 판은 point 만 봐서
            #    "구 팔이 격자에 안정" 을 이 도구로 검증할 수 없었다.
            row[f'origin_spread_{mode}_pct'] = float(
                f'{(v["sig"].max() / max(v["sig"].min(), 1e-30) - 1) * 100:.3g}') if v else None
            if mode != 'none':
                row[f'vol_{mode}_um3'] = float(f'{v["vol"]:.4g}') if v else None
                row[f'vol_{mode}_over_true'] = float(
                    f'{v["vol"] / (len(sdcp_c) * V_true):.3f}') if v else None
        #  ★ 이득은 **쌍대응**으로 — 같은 origin 끼리 나눈 뒤 평균/SE (리뷰 ② H4).
        #    옛 판은 ratio-of-means 를 4자리로 인용했는데 불확실도가 없었다.  실침대
        #    캠페인(CL-33/34)은 이미 쌍대응 SE 를 정본으로 못박았다 — 같은 규율을 여기에도.
        b = res.get('none')
        for mode in ('sphere', 'point'):
            v = res.get(mode)
            if not (b and v):
                row[f'gain_{mode}_pct'], row[f'gain_{mode}_se_pct_pt'] = None, None
                continue
            g = (v['sig'] / np.maximum(b['sig'], 1e-30) - 1.0) * 100.0
            row[f'gain_{mode}_pct'] = float(f'{g.mean():.4g}')
            row[f'gain_{mode}_se_pct_pt'] = float(
                f'{g.std(ddof=1) / np.sqrt(len(g)):.3g}') if len(g) > 1 else None
        rows.append(row)
    return rows


def _selftest():
    ok, fail = 0, []

    def chk(n, c):
        nonlocal ok
        (ok := ok + 1) if c else fail.append(n)
        print(('  PASS  ' if c else '  FAIL  ') + n)

    # ① 점-스탬프 부피 = 입자수 × vox³ (정의) — 그리고 참부피 대비 배수가 산술과 맞다
    c = np.array([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0], [3.0, 3.0, 3.0]])
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    for vox, want in ((0.4, 4.53), (0.3, 1.91), (0.25, 1.11)):
        n = int(round(4.0 / vox))
        ijk = sdcp_point_cells(c, vox, (0, 0, 0), 4.0, n)
        got = len(ijk) * vox ** 3 / (len(c) * V_true)
        chk(f'① 점-스탬프 vox {vox}: 참부피의 {got:.2f}배 (산술 {want})', abs(got - want) < 0.02)
    # ② ★ 점-스탬프 부피는 vox 0.24 근처에서 **우연히 정확**해지고 그 아래로는 과소가 된다
    #    (vox³ = π/6·d³ 인 지점).  ⇒ 0.4 → 0.25 스윕은 "수렴" 과 "부피가 정답을 통과하는 것"
    #    이 섞여 있고, 그 아래에서는 **부호가 뒤집힌다** = 판별 검사가 된다.
    xover = SDCP_D_UM * (np.pi / 6.0) ** (1.0 / 3.0)
    chk(f'② 점-스탬프 부피가 정확해지는 vox = {xover:.4f} µm (생산 0.25 바로 옆)',
        abs(xover - 0.2418) < 1e-3)
    for vox, want in ((0.4, 4.53), (0.15, 0.239)):
        got = vox ** 3 / V_true
        chk(f'②b vox {vox} 에서 점/참 = {got:.3f} ({"과대" if got > 1 else "**과소**"})',
            abs(got - want) < 0.01)
    # ③ ★ 서브복셀 구는 래스터에서 **통째로 사라진다** — 그래서 점-스탬프가 쓰인 것이고,
    #    두 규약 다 vox 0.4 에서는 틀린다 (하나는 87 % 소실, 하나는 4.53× 과대).
    gap = 1.0
    g0 = np.arange(0.5, 4.0, gap)
    C = np.stack(np.meshgrid(g0, g0, g0, indexing='ij'), -1).reshape(-1, 3) + 0.137
    R = np.full(len(C), SDCP_D_UM / 2.0)
    lost = {}
    for vox in (0.4, 0.15):
        n = int(round(4.5 / vox)); gg = (np.arange(n) + 0.5) * vox
        lost[vox] = sum(1 for p in C if ((np.array([gg[np.abs(gg - p[k]).argmin()]
                                                    for k in range(3)]) - p) ** 2).sum()
                        > (SDCP_D_UM / 2) ** 2) / len(C)
    chk(f'③ vox 0.4 에서 구 래스터는 입자의 {lost[0.4]:.0%} 를 잃는다 (서브복셀)',
        lost[0.4] > 0.7)
    chk(f'③b vox 0.15 (Ø/dx = 2) 에서는 아무도 안 잃는다 ({lost[0.15]:.0%})', lost[0.15] == 0.0)
    _ = R

    # ── ④ **재현 회귀** (심층 리뷰 ② B1) — `build()` 를 실제로 부른다.
    #    옛 selftest 는 build() 를 한 번도 호출하지 않아 이 결함을 원리적으로 못 잡았다.
    #    L/vox 가 정수가 아니고 한 축만 이동하면 축별 격자 크기가 갈리는데 옛 판은
    #    `sid.shape[0]` 하나로 세 축을 클립해 범위 밖 인덱스를 통과시켰다.
    rng = np.random.default_rng(0)
    L, VOX = 20.0, 0.15                                  # 20/0.15 = 133.33 (비정수)
    o = np.zeros(3)
    _am = (rng.uniform(0, L, (12, 3)), np.full(12, 2.0))
    _se = (rng.uniform(0, L, (60, 3)), np.full(60, 0.5))
    _c = rng.uniform(0, L, (4000, 3))
    _sids = {}
    try:
        for _s in ([0., 0., 0.], [VOX / 2, 0., 0.], [0., VOX / 2, 0.], [0., 0., VOX / 2]):
            _sids[tuple(_s)] = build(VOX, o, L, _am, _se, _c, 'point',
                                     lattice_shift=np.array(_s))
        chk('④ build(point) 가 비정수 L/vox × 한-축 이동에서 IndexError 를 안 낸다', True)
    except IndexError as _e:
        chk(f'④ build(point) IndexError: {_e}', False)
    #  ④b 축별 격자 크기가 실제로 갈린다 (그래야 ④ 가 의미 있는 회귀다)
    chk('④b sh=(h,0,0) 에서 격자가 (134,133,133) 로 갈린다',
        _sids.get((VOX / 2, 0., 0.), np.zeros((1, 1, 1))).shape == (134, 133, 133))
    #  ④c 점 팔의 SDCP **표본**이 팔마다 흔들리지 않는다 (CDX-R2-01 재발 방지)
    _cnt = {k: int((v == SID_SDCP).sum()) for k, v in _sids.items()}
    chk(f'④c 네 팔의 점-스탬프 SDCP 셀 수 산포 ≤ 0.5 % ({sorted(_cnt.values())})',
        (max(_cnt.values()) - min(_cnt.values())) <= 0.005 * max(_cnt.values()))

    # ── ⑤ **재현 회귀** (리뷰 ② B2) — 구 팔이 생산 게이트를 가진다.
    #    실측: vox 0.4 에서 입자의 78.7 % 가 셀 0 개인데 **총 부피비는 0.961** 이라
    #    눈에 안 띈다 (살아남은 입자가 1 셀씩 먹어 상쇄).  ⇒ 부피비로는 못 잡는다.
    _rej = False
    try:
        build(0.4, o, L, _am, _se, _c, 'sphere')
    except ValueError:
        _rej = True
    chk('⑤ 구 팔이 vox 0.4 (d/vox 0.75) 를 거부한다 (생산 게이트 미러)', _rej)
    _ok15 = False
    try:
        build(0.15, o, L, _am, _se, _c[:200], 'sphere'); _ok15 = True
    except ValueError:
        pass
    chk('⑤b vox 0.15 (d/vox = 2.0) 는 통과한다', _ok15)
    print(f'\nsdcp_stamp_confound selftest: {ok}/{ok + len(fail)} PASS'
          + (f'   FAILED: {fail}' if fail else ''))
    return 1 if fail else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--kit', default='kit_ps_7_3')
    ap.add_argument('--len-um', type=float, default=12.0)
    ap.add_argument('--vox', type=float, nargs='+', default=[0.4, 0.3, 0.25, 0.2, 0.15])
    ap.add_argument('--sdcp-vol-pct', type=float, default=0.5,
                    help='RVE 부피 대비 SDCP 부피 %% (레시피가 아니라 **통제 변수**)')
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--out', default='')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())

    from sr01_realbed_ab import load_kit                          # noqa: E402
    am_c, am_r, se_c, se_r, lat, thick = load_kit(a.kit)
    base = np.array([lat / 2 - a.len_um / 2, lat / 2 - a.len_um / 2, thick / 2 - a.len_um / 2])
    V_true = np.pi / 6.0 * SDCP_D_UM ** 3
    n_sdcp = int(round(a.sdcp_vol_pct / 100.0 * a.len_um ** 3 / V_true))
    rng = np.random.default_rng(a.seed)
    sdcp_c = base + rng.uniform(0, a.len_um, size=(n_sdcp, 3))
    print(f'{a.kit} · RVE {a.len_um} µm³ · SDCP Ø{SDCP_D_UM} µm × {n_sdcp:,} '
          f'({a.sdcp_vol_pct} vol%, 균일 랜덤 배치 = **통제 변수**)')
    print('σ_e: AM 0.010 · SDCP 250 S/cm · SE/기공 전자절연\n')
    rows = run((am_c, am_r), (se_c, se_r), sdcp_c, base, a.len_um, a.vox)
    print(f'{"vox":>6} {"Ø/dx":>6} {"부피 점/참":>10} {"σ_e AM만":>11} {"σ_e +구":>11} '
          f'{"σ_e +점":>11} {"이득 구%±SE":>15} {"이득 점%±SE":>15}')
    for r in rows:
        def _g(k):
            v, s = r.get(f'gain_{k}_pct'), r.get(f'gain_{k}_se_pct_pt')
            return '  (게이트 거부)' if v is None else f'{v:>8.2f} ± {s if s else 0:<4.2f}'
        _sp = r['sigma_e_sphere']
        print(f'{r["vox"]:>6} {r["sdcp_d_per_dx"]:>6.2f} {r["vol_point_over_true"]:>10.2f} '
              f'{r["sigma_e_none"]:>11.5g} '
              f'{("%11.5g" % _sp) if _sp is not None else "          —"} '
              f'{r["sigma_e_point"]:>11.5g} {_g("sphere"):>15} {_g("point"):>15}')
        if r['sphere_gate_rejected']:
            print(f'        ⚠ 구 팔 거부: {r["sphere_gate_rejected"][:88]}')
        if r['unconverged_any']:
            print('        ⚠⚠ 미수렴 팔이 있다 — 이 행의 σ 를 인용하지 말 것')
    print('\n⚠ 이득은 **쌍대응**(같은 origin 끼리 나눈 뒤 평균)이고 ± 는 8팔 표준오차다.  '
          '\n⚠ 이 RVE 에는 VGCF 도 AM-AM 브리지도 없다 — 실침대와 같은 망이 아니다 (CL-31 캐비엇).')
    if a.out:
        json.dump({'kit': a.kit, 'len_um': a.len_um, 'n_sdcp': n_sdcp,
                   'sdcp_vol_pct': a.sdcp_vol_pct, 'rows': rows},
                  open(a.out, 'w'), ensure_ascii=False, indent=1)
        print(f'\n  → {a.out}')
