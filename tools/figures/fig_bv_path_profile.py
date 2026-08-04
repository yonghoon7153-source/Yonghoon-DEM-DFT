#!/usr/bin/env python3
"""fig_bv_path_profile.py — BV 에너지 지형의 **침투 경로 프로파일** (reaction coordinate vs eV).

문헌(softBV/BVlain 계열 발표자료·Y-치환 argyrodite 논문)의 "Energy vs Reaction Coordinate"
그림을 우리 구조로 재현한다.

방법 — **bvlain 의 침투 관례를 그대로 따른다** (안 맞추면 장벽이 어긋난다, 1차 시도 실측):
  · 연결성 = **26-이웃** (generate_binary_structure(3,3) — 면+모서리+꼭짓점)
  · 침투 판정 = 에너지 문턱 t 의 부분집합 {E-aboveMin < t} 를 라벨링해서
    어떤 성분이 자기 주기 이미지(v ↔ v+격자벡터)와 이어지는가 (축별 이분탐색)
  · 프로파일 = 그 축의 문턱 t* 아래 영역 안에서, wrap 을 실증하는 복셀쌍 사이
    **최단 기하 경로**(26-이웃 Dijkstra, 셀 기하 반영) 를 따라 E(s) 를 그린다

⚠⚠ 정답 검증 내장: 축별 문턱을 정렬하면 bvlain 자신의 percolation_barriers
  (E_1D ≤ E_2D ≤ E_3D) 와 일치해야 한다 (1차 구현이 6-이웃/전역최소-고정이라 0.074 eV
  어긋나 게이트에 걸렸고, 관례를 맞춘 것이 이 판이다). 0.03 eV 넘게 어긋나면 그림을
  내지 않고 죽는다.

⚠ 이 프로파일은 **빈 격자 BV 프록시**다 (kb/concepts/bvse.md §8-9). 절대 스케일은
  그럴듯하지만 가족 내 σ/Ea 순위는 MD 가 판정한다 — 그림 각주에 그대로 박는다.

  python3 tools/figures/fig_bv_path_profile.py                  # comp1+modelc 2패널 + CSV
  python3 tools/figures/fig_bv_path_profile.py --systems comp1 modelc lpsocl b2o3
"""
import argparse
import heapq
import itertools
import os
import sys

import numpy as np
from scipy.ndimage import label as nd_label
from scipy.ndimage import generate_binary_structure

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from tools.figures.house_style import INK, MUT, SYS, apply_axes  # noqa: E402

# 표시명은 사용자 지정 관례 (2026-08-04): LPSCl · LPSCl1.6 · LPSOCl1.6 · B2O3@LPSCl1.6
SYSTEMS = {
    "comp1":  ("db/structures/comp1_V0_k444.cif",  "LPSCl"),
    "modelc": ("db/structures/modelc_V0_k663.xyz", "LPSCl1.6"),
    "lpsocl": ("db/structures/lpsocl_relaxV0.xyz", "LPSOCl1.6"),
    "b2o3":   ("db/structures/b2o3_relaxV0.xyz",   "B2O3@LPSCl1.6"),
}
MD_EA = {"comp1": "0.253", "modelc": "0.197±0.032", "lpsocl": "0.287±0.024", "b2o3": "0.199±0.034"}
RES, RCUT, K = 0.25, 10.0, 100
STRUCT26 = generate_binary_structure(3, 3)          # bvlain 과 동일 (26-이웃)


def _tile2(E):
    """bvlain 방식 2x2x2 타일 (침투 판정용)."""
    return np.tile(E, (2, 2, 2))


def _labels_周期(mask):
    """26-이웃 라벨 + 바깥 경계 넘어 같은 성분 병합 (bvlain _apply_pbc 상당, union-find)."""
    lab, nfeat = nd_label(mask, structure=STRUCT26)
    parent = list(range(nfeat + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for axis in range(3):
        f_hi = np.take(lab, -1, axis=axis)
        f_lo = np.take(lab, 0, axis=axis)
        both = (f_hi > 0) & (f_lo > 0)
        for a, b in set(zip(f_hi[both].ravel(), f_lo[both].ravel())):
            union(int(a), int(b))
    flat = np.array([find(i) for i in range(nfeat + 1)])
    return flat[lab]


# 7가지 감김(winding) 병진 — bvlain _cross_boundary 의 {0,1}³ 병진과 동일.
#   침투는 순수 축(100/010/001)만이 아니라 **대각 감김**(110/011/…)으로도 성립한다 —
#   1차 구현이 순수 축만 봐서 comp1 E_1D 를 0.26 으로 놓쳤다(정답 0.195 = 대각).
T7 = [t for t in itertools.product((0, 1), repeat=3) if t != (0, 0, 0)]


def _slices_for(T, N):
    lo = [slice(0, N[d]) if T[d] else slice(None) for d in range(3)]
    hi = [slice(N[d], 2 * N[d]) if T[d] else slice(None) for d in range(3)]
    return tuple(lo), tuple(hi)


def wrapsets(E, t):
    """문턱 t 에서, 감김 T 마다 그 T 로 자기 이미지와 이어지는 성분 라벨 집합."""
    lab = _labels_周期(_tile2(E) < t)
    N = E.shape
    out = {}
    for T in T7:
        lo, hi = _slices_for(T, N)
        a, b = lab[lo], lab[hi]
        m = (a > 0) & (a == b)
        out[T] = set(np.unique(a[m]).tolist()) if m.any() else set()
    return lab, out


def dmax_at(E, t):
    """bvlain 의 d (성분이 도달하는 {0,1}³ 병진 개수, 자기 자신 포함) 최댓값."""
    _, ws = wrapsets(E, t)
    cnt = {}
    for T, labs in ws.items():
        for l in labs:
            cnt[l] = cnt.get(l, 0) + 1
    return 1 + (max(cnt.values()) if cnt else 0)


def perc_threshold(E, need_d, tol=2e-3):
    """d ≥ need_d 가 처음 성립하는 문턱 (이분탐색). bvlain: 1D d≥2 · 2D d≥4 · 3D d=8."""
    lo, hi = 0.0, float(E.max())
    if dmax_at(E, hi) < need_d:
        return None
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if dmax_at(E, mid) >= need_d:
            hi = mid
        else:
            lo = mid
    return hi


def wrap_witness(E, t):
    """t 에서 성립하는 감김 중 하나를 골라 (T, 시작복셀 v). v 는 E 최소 증인."""
    lab, ws = wrapsets(E, t)
    N = E.shape
    best = None
    for T in T7:
        if not ws[T]:
            continue
        lo, hi = _slices_for(T, N)
        a, b = lab[lo], lab[hi]
        ok = (a > 0) & (a == b)
        if not ok.any():
            continue
        tiledE = _tile2(E)[lo]
        idxs = np.argwhere(ok)
        vals = tiledE[ok]
        k = int(np.argmin(vals))
        v = tuple(int(x) % N[d] for d, x in enumerate(idxs[k]))
        if best is None or vals[k] < best[0]:
            best = (float(vals[k]), T, v)
    return (best[1], best[2]) if best else (None, None)


OFFS26 = [o for o in itertools.product((-1, 0, 1), repeat=3) if o != (0, 0, 0)]


def dijkstra_valley(E2, start, target, open_axes, cap, cell, N):
    """{E < cap} 안에서 **에너지 선적분 ∫E ds 최소** 경로 (26-이웃).

    ⚠ 순수 최단거리로 하면 경로가 천장(cap) 바로 밑을 직선으로 질러가서 프로파일에
      인공 평탄 구간이 생긴다 (LPSOCl 1차 시도 실측). 문헌 그림들은 골짜기를 따라
      우물-안장-우물을 오가는 모양 — 선적분 최소가 그걸 재현한다.
      +0.02 eV 오프셋은 E=0 분지에서 무한 배회를 막는 길이 벌점.
    open_axes 는 2배 확장(랩 없음), 나머지 PBC.
    """
    sh = E2.shape
    step = [cell[d] / N[d] for d in range(3)]
    slen = {o: float(np.linalg.norm(o[0] * step[0] + o[1] * step[1] + o[2] * step[2]))
            for o in OFFS26}
    ok = E2 < cap + 1e-12
    dist = np.full(sh, np.inf)
    dist[start] = 0.0
    prev = {}
    pq = [(0.0, start)]
    while pq:
        dcur, u = heapq.heappop(pq)
        if u == target:
            path = [u]
            while path[-1] != start:
                path.append(prev[path[-1]])
            return path[::-1]
        if dcur > dist[u]:
            continue
        eu = E2[u]
        for o in OFFS26:
            v = [u[0] + o[0], u[1] + o[1], u[2] + o[2]]
            bad = False
            for d in range(3):
                if d in open_axes:
                    if not (0 <= v[d] < sh[d]):
                        bad = True
                        break
                else:
                    v[d] %= sh[d]
            if bad:
                continue
            v = tuple(v)
            if not ok[v]:
                continue
            nd = dcur + slen[o] * (0.5 * (eu + E2[v]) + 0.02)
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return None


def profile_for(name, path_cif):
    from bvlain import Lain
    calc = Lain(verbose=False)
    calc.read_file(path_cif)
    E = calc.bvse_distribution(mobile_ion="Li1+", r_cut=RCUT, resolution=RES, k=K)
    E = E - E.min()
    cell = calc.atoms.cell.array

    # ⚠ **배열축 ↔ 격자벡터 대응 가드 (2026-08-04).** 4계 실측으로는 perm=[0,1,2]
    #   (bvlain 이 배열축 i = 격자 a_i 로 reshape 한다) — 그래도 mesh_ 로 매번 확인한다.
    #   bvlain 판올림으로 순서가 바뀌면 비스듬한 셀에서 반응좌표·감김 라벨이 소리 없이
    #   틀어지기 때문. ⚠ 교훈 하나 더: 이 가드를 만들게 한 "버그"는 사실 검산 스크립트가
    #   **cif 왕복 프레임(표준 방향)과 원본 xyz 프레임을 섞은 것**이었다 — 좌표 검산은
    #   반드시 calc.atoms (bvlain 프레임) 하나로 통일할 것.
    coords = calc.mesh_.reshape(E.shape + (3,))
    perm = []
    for ax in range(3):
        step = np.zeros(3); step[ax] = 1
        d = coords[tuple(step.astype(int))] - coords[0, 0, 0]
        perm.append(int(np.argmax(np.abs(d))))
    if sorted(perm) != [0, 1, 2]:
        raise SystemExit(f"⛔ {name}: mesh_ 축 대응을 못 정했다 (perm={perm})")
    if perm != [0, 1, 2]:
        E = np.transpose(E, np.argsort(perm))       # 배열축 i ↔ 격자 a_i 로 정렬
        print(f"    (bvlain 배열축 재배열: perm {perm} → 정렬)")
    perc = calc.percolation_barriers(encut=5.0)
    ref = sorted(float(perc[k]) for k in ("E_1D", "E_2D", "E_3D"))

    N = E.shape
    mine = [perc_threshold(E, need) for need in (2, 4, 8)]     # 1D · 2D · 3D
    for lab_, t in zip(("1D", "2D", "3D"), mine):
        print(f"    E_{lab_} = {t:.4f} eV" if t is not None else f"    E_{lab_}: 침투 없음")

    err = max(abs(m - r) for m, r in zip([t for t in mine if t is not None], ref))
    print(f"    검증: mine {[round(v, 3) for v in mine if v is not None]} vs "
          f"bvlain {[round(v, 3) for v in ref]} (최대 오차 {err:.3f} eV)")
    if err > 0.03:
        raise SystemExit(f"⛔ {name}: 경로 추출이 bvlain 침투장벽과 {err:.3f} eV 어긋난다 — "
                         "그림을 내지 않는다. (연결성/라벨 관례 재점검)")

    t = mine[0]                                                 # 1D 침투 = "the transport path"
    T, v = wrap_witness(E, t)
    if v is None:
        raise SystemExit(f"⛔ {name}: 문턱 {t:.3f} 에서 wrap 증인이 없다 (모순)")
    open_axes = {d for d in range(3) if T[d]}
    E2 = E
    for d in sorted(open_axes):
        E2 = np.concatenate([E2, E2], axis=d)
    start = tuple(v)
    tgt = tuple(v[d] + (N[d] if T[d] else 0) for d in range(3))
    path = dijkstra_valley(E2, start, tgt, open_axes, t, cell, N)
    if path is None:
        raise SystemExit(f"⛔ {name}: cap={t:.3f} 에서 경로가 안 이어진다 (모순)")
    # ⚠⚠ **반응좌표는 랩을 풀고 재야 한다 (2026-08-05 수정).**
    #   dijkstra 는 주기축에서 `v[d] %= sh[d]` 로 감싼다. 그 인덱스를 그대로
    #   데카르트로 바꿔 거리를 누적하면, 셀을 넘는 한 걸음이 **셀 한 변만큼의
    #   가짜 점프**로 잡힌다 — 프로파일엔 그 구간이 '평탄 구간'처럼 그려진다.
    #   실측(수정 전): comp1 9.80 Å 점프 2개(전체 길이의 42%), lpsocl 6.68 Å 2개(58%).
    #   → LPSOCl 패널의 긴 평탄대는 물리(넓은 통로)가 아니라 이 아티팩트였다.
    #   고침: 이웃 간 인덱스 차를 {-1,0,1} 로 되돌린 뒤(26-이웃이므로 그게 참값)
    #   그 차분만 데카르트로 환산해 누적한다. E 값·E_perc·순위는 영향 없다
    #   (같은 voxel 을 지나므로) — 바뀌는 건 x축과 경로 길이뿐이다.
    #
    # ⚠ metric (2026-08-05 리뷰 ISSUE-1 반영): bvlain `_mesh` 는 linspace(0,1,N)
    #   **양끝 포함**이라 물리 voxel 간격은 cell/(N-1) 이고, 인덱스 0 과 N-1 은
    #   **같은 평면**이다 (실측 max|E[0]-E[-1]| ~ 1e-11). 따라서
    #   (i) 일반 스텝 = cell/(N-1), (ii) 경계를 넘거나 복제 이음새를 지나는 스텝은
    #   물리적으로 0 Å. cell/N 로 나누면 길이가 계별 +0.1 ~ -4.2% 틀어진다(lpsocl 최대).
    #   dijkstra 가중치(slen)는 인덱스-metric 그대로 둔다 — 경로 '선택'에만 관여하고
    #   E_perc·프로파일 E 와 무관 (comp1 은 등방 N 이라 선택 불변).
    idx = np.array(path, int)
    phys = np.empty_like(idx)
    for d_ax in range(3):
        n_ax = N[d_ax]
        if d_ax in open_axes:               # 2배 확장축: 복제 이음새(N-1 ≡ N) = 같은 평면
            phys[:, d_ax] = (idx[:, d_ax] // n_ax) * (n_ax - 1) + idx[:, d_ax] % n_ax
        else:                               # 주기축: 유일 평면 수 = N-1 (0 ≡ N-1)
            phys[:, d_ax] = idx[:, d_ax] % (n_ax - 1)
    dif = np.diff(phys, axis=0)
    for d_ax in range(3):
        if d_ax not in open_axes:           # 주기축 MIC (주기 = N-1)
            m = N[d_ax] - 1
            dif[:, d_ax] = (dif[:, d_ax] + m // 2) % m - m // 2
    if np.abs(dif).max() > 1:
        raise SystemExit(f"⛔ {name}: 랩 해제 후에도 |Δindex|>1 — 경로가 26-이웃이 아니다")
    step_cart = (dif / (np.array(N) - 1.0)) @ cell
    d = np.concatenate([[0.0], np.cumsum(np.linalg.norm(step_cart, axis=1))])
    e = np.array([E2[tuple(p)] for p in path])
    wind = "[" + "".join(str(x) for x in T) + "]"
    print(f"    경로: winding {wind} · {len(path)}점 · 길이 {d[-1]:.1f} A · max {e.max():.4f} eV")
    return {"axis": wind, "d": d, "e": e, "E_perc": float(t),
            "ref": {k: float(perc[k]) for k in perc}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", nargs="+", default=["comp1", "modelc"],
                    help="그림 패널 (CSV 는 여기 나온 계 전부)")
    ap.add_argument("--out_png", default="docs/figures/bv_path_profile.png")
    ap.add_argument("--out_csv", default="db/properties/bv_path_profile_origin.csv")
    a = ap.parse_args()

    res = {}
    for s in a.systems:
        print(f"── {s} ({SYSTEMS[s][1]})")
        res[s] = profile_for(s, SYSTEMS[s][0])

    # ── Origin CSV (계마다 d/E 열쌍, 길이 다르면 빈칸) ───────────────────────
    os.makedirs(os.path.dirname(a.out_csv), exist_ok=True)
    nmax = max(len(r["d"]) for r in res.values())
    with open(a.out_csv, "w", newline="", encoding="utf-8-sig") as f:
        f.write('"# BV-EL (bvlain, Morse softBV, eV aboveMin) percolation-path profile: '
                'per-axis percolation threshold (26-connectivity, bvlain convention), '
                'then min-energy-line-integral path under that ceiling."\n')
        f.write('"# EMPTY-LATTICE PROXY: absolute scale plausible, family sigma/Ea ranking is '
                'decided by MD (kb/concepts/bvse.md sec 8-9)."\n')
        f.write('"# 2026-08-05 FIX(2): reaction coordinate is PBC-unwrapped AND uses the bvlain '
                'mesh metric (endpoint-inclusive grid: spacing cell/(N-1); boundary/seam-crossing '
                'steps are 0 A - same physical plane). Pre-fix fake plateaus: comp1 2x9.80 A = 42% '
                'of plotted length, lpsocl 2x6.68 A = 58% (jump = |lattice vector| x (N-1)/N, '
                'independently verified). E_perc / E values / rankings unchanged by both fixes."\n')
        for s, r in res.items():
            f.write(f'"# {s}: axis {r["axis"]}, E_perc {r["E_perc"]:.4f} eV; '
                    f'bvlain E_1D/2D/3D {r["ref"]["E_1D"]:.3f}/{r["ref"]["E_2D"]:.3f}/'
                    f'{r["ref"]["E_3D"]:.3f} eV; MD Ea {MD_EA[s]} eV"\n')
        cols = []
        for s in res:
            cols += [f"{s}_d_A", f"{s}_E_eV"]
        f.write(",".join(cols) + "\n")
        for i in range(nmax):
            row = []
            for s in res:
                r = res[s]
                row += ([f"{r['d'][i]:.3f}", f"{r['e'][i]:.4f}"] if i < len(r["d"]) else ["", ""])
            f.write(",".join(row) + "\n")
    print(f"→ {a.out_csv}")

    # ── 그림 (문헌 스타일: 패널당 한 계, 같은 y축, max barrier 주석) ─────────
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(res)
    fig, axs = plt.subplots(1, n, figsize=(5.4 * n, 3.9), sharey=True)
    axs = np.atleast_1d(axs)
    ymax = max(r["e"].max() for r in res.values()) * 1.35
    for axp, (s, r) in zip(axs, res.items()):
        c = SYS.get(s, INK)
        axp.plot(r["d"], r["e"], "-", color=c, lw=1.6, marker="o", ms=2.2, mfc=c, mec="none")
        axp.axhline(r["E_perc"], ls="--", lw=1.0, color=INK, alpha=0.55)
        axp.text(0.98, r["E_perc"] + 0.02 * ymax,
                 f"$E_{{perc}}$({r['axis']}) = {r['E_perc']:.3f} eV",
                 ha="right", va="bottom", fontsize=10.5, color=INK,
                 transform=axp.get_yaxis_transform())
        axp.text(0.02, 0.965, f"{SYSTEMS[s][1]}   (MD $E_a$ {MD_EA[s]} eV)",
                 ha="left", va="top", fontsize=10.5, color=MUT, transform=axp.transAxes)
        axp.set_ylim(0, ymax)
        axp.set_xlim(0, r["d"][-1])
        apply_axes(axp, xlabel="Reaction coordinate (Å)",
                   ylabel="Energy (eV)" if axp is axs[0] else None)
    fig.suptitle("BV-EL percolation-path profiles (empty-lattice proxy — ranking by MD)",
                 fontsize=11.5, color=MUT, y=0.99)
    fig.tight_layout()
    os.makedirs(os.path.dirname(a.out_png), exist_ok=True)
    fig.savefig(a.out_png, dpi=300)
    print(f"→ {a.out_png}")


if __name__ == "__main__":
    main()
