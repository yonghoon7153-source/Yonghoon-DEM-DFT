#!/usr/bin/env python3
"""Phase 1l — 팽창(부피) 축은 `(1,1,1)` 축퇴를 깨는가. **모형 없이** 판정한다.

## 왜 이 계산인가

Mohtat 2019 의 처방은 이 계보에서 유일하게 **"제약을 걸어라" 가 아니라 "센서를
하나 더 달아라"** 다 — 전압에 **셀 팽창(μm)** 을 둘째 채널로 더한다.
Phase 1e·1h·1i 가 제약 처방을 우리 격자에서 세 각도로 기각했으므로,
**이 계보에서 아직 기각되지 않은 처방은 그의 것 하나뿐**이다 (통합 논지 Gap 8).

## 막힌 자리 — 그리고 그것을 우회하는 법

`Chen2020_composite` 에는 **전극 팽창 파라미터가 없다** (실측: `partial molar
volume` 은 SEI 것뿐이고 `Cell thermal expansion coefficient` 는 열팽창이다).
그러므로 Mohtat 식 팽창 채널을 **우리 셀로 교정할 수 없다.**

**그런데 교정 없이도 판정할 수 있다.** Mohtat 식 (39) 계열의 팽창 모형은 전부

```
Δt(x) = n_c · Σᵢ tᵢ⁰ ξᵢ · (전극 i 의 화학량론 변화)
```

즉 **전극 화학량론의 고정 선형범함수**다. 계수 `(n_c, tᵢ⁰, ξᵢ)` 가 무엇이든
**gradient 는 화학량론 궤적의 Jacobian 을 통과한다.** 그러므로:

> 화학량론 궤적 `[y(x), z(x)]` 의 Jacobian 이 `(1,1,1)` 을 못 보면,
> **그 형태의 팽창 모형은 계수가 무엇이든 못 본다.**

이것은 한 모형의 답이 아니라 **모형 족(族) 전체에 대한 답**이라 더 강하다.

## 화학량론은 어디서 오나 — 시뮬 참값에서

격자 parquet 의 `v_pe`·`v_ne` (전극별 전위)를 봉인된 평형 OCP 표로 **역보간**해
`y(x_norm)`·`z(x_norm)` 을 얻는다. `modes_to_params` 도 창 대수도 안 쓴다 —
그래서 Phase 1k 가 붙인 `'paper'` 규약 경고가 **여기엔 안 걸린다.**

⚠ 격자 곡선은 0.05 C 유한 전류라 `v_pe` 에 과전압이 섞여 있다. 그래서 얻는 것은
**겉보기 화학량론**이다. Phase 1j 가 그 과전압을 18.7 mV 로 쟀다 — 아래 경계 참조.

출력: results/phase1l/{angles.csv, augmented.csv} + stdout. **CSV 가 정본이다.**
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
HCDIR = DD / ".cache" / "halfcell"
OUT = HERE / "results" / "phase1l"

H = 0.02
LO, HI = 0.02, 0.98
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)
OPS = [("pristine", 0.00, 0.00, 0.00), ("22p 근방", 0.16, 0.12, 0.12)]


def ang(u, v):
    c = abs(float(u @ v)) / (np.linalg.norm(u) * np.linalg.norm(v))
    return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))


def umin(J):
    w, V = np.linalg.eigh(J.T @ J)
    u = V[:, 0] / np.linalg.norm(V[:, 0])
    return (-u if u.sum() < 0 else u), np.sqrt(np.maximum(w, 0.0))


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}")

    from src.io import source_digest
    now = source_digest()
    meta = yaml.safe_load(sorted(HCDIR.glob("*.meta.yaml"))[0].read_text(encoding="utf-8"))
    if str(meta.get("source_digest")) != now:
        sys.exit(f"평형 OCP 캐시 봉인 불일치 ({meta.get('source_digest')} ≠ {now})")
    hc = json.loads(sorted(HCDIR.glob("*_ocp_*.json"))[0].read_text())
    print(f"봉인 확인 source_digest {now} ✓")

    # 역보간표 — OCP 는 단조여야 한다. 확인하고 쓴다.
    y_t = np.asarray(hc["y_pe"], float); u_p = np.asarray(hc["u_pe"], float)
    z_t = np.asarray(hc["z_ne"], float); u_n = np.asarray(hc["u_ne"], float)
    for nm, xx, uu in (("PE", y_t, u_p), ("NE", z_t, u_n)):
        d = np.diff(uu)
        mono = np.all(d < 0) or np.all(d > 0)
        print(f"   {nm} OCP 단조성 {'✓' if mono else '✗ 비단조 — 역보간 불가'}"
              f"   (u {uu.min():.3f}~{uu.max():.3f} V)")
        if not mono:
            sys.exit(f"{nm} OCP 가 단조가 아니다 — 역보간을 거부한다")
    # interp 는 증가 격자를 요구한다
    op = np.argsort(u_p); on = np.argsort(u_n)
    up_s, yp_s = u_p[op], y_t[op]
    un_s, zn_s = u_n[on], z_t[on]

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "x_norm",
        "v_pe", "v_ne", "v_full"])
    d0 = df[df.noise == 0]
    key = {}
    for c, g in d0.groupby("cond_id", sort=False):
        key[(round(g.lli.iloc[0], 4), round(g.lam_pe.iloc[0], 4),
             round(g.lam_ne.iloc[0], 4))] = c
    ref = d0[d0.cond_id == next(iter(key.values()))].sort_values("x_norm")
    xa = ref.x_norm.to_numpy(float)
    xs = xa[(xa >= LO) & (xa <= HI)]
    cache = {}

    def traj(k):
        """조건 k → (V_full, y(x), z(x)) 를 공통 x 격자에서."""
        if k not in key:
            return None
        if k not in cache:
            g = d0[d0.cond_id == key[k]].sort_values("x_norm")
            gx = g.x_norm.to_numpy(float)
            v = np.interp(xs, gx, g.v_full.to_numpy(float))
            vp = np.interp(xs, gx, g.v_pe.to_numpy(float))
            vn = np.interp(xs, gx, g.v_ne.to_numpy(float))
            cache[k] = (v, np.interp(vp, up_s, yp_s), np.interp(vn, un_s, zn_s))
        return cache[k]

    def rk(l, p, n):
        return (round(l, 4), round(p, 4), round(n, 4))

    rows, arows = [], []
    for label, l0, p0, n0 in OPS:
        base = traj(rk(l0, p0, n0))
        axes = [(l0 + H, p0, n0), (l0, p0 + H, n0), (l0, p0, n0 + H)]
        if base is None or any(traj(rk(*a)) is None for a in axes):
            print(f"[건너뜀] {label}")
            continue
        cols = [traj(rk(*a)) for a in axes]

        J_v = np.column_stack([(c[0] - base[0]) / H for c in cols])          # 전압
        J_y = np.column_stack([(c[1] - base[1]) / H for c in cols])          # PE 화학량론
        J_z = np.column_stack([(c[2] - base[2]) / H for c in cols])          # NE 화학량론
        J_s = np.vstack([J_y, J_z])                                          # 화학량론 궤적

        print(f"\n══ {label} (LLI {l0} · LAM_PE {p0} · LAM_NE {n0}) ══  {len(xs)}점")
        for nm, JJ, unit in (("전압 U_full(x)", J_v, "V/단위"),
                             ("PE 화학량론 y(x)", J_y, "1/단위"),
                             ("NE 화학량론 z(x)", J_z, "1/단위"),
                             ("★ 화학량론 궤적 [y;z]", J_s, "1/단위")):
            u, sv = umin(JJ)
            a = ang(u, ONES)
            print(f"   {nm:<22} 열 노름 {np.round(np.linalg.norm(JJ, axis=0), 4)} {unit}")
            print(f"   {'':<22} u_min {np.round(u, 5)}"
                  f"   ∠(1,1,1) = **{a:6.2f}°**   조건수 {sv[-1]/sv[0]:7.2f}")
            rows.append({"op": label, "observable": nm, "angle_deg": a,
                         "cond": float(sv[-1] / sv[0]),
                         **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)},
                         **{f"col_norm_{m}": float(np.linalg.norm(JJ[:, i]))
                            for i, m in enumerate(MODES)}})

        # ── 전압에 화학량론 채널을 **더하면** 최소 감도가 오르나 ──────────
        # 팽창은 [y;z] 의 고정 선형범함수이므로, [y;z] 를 통째로 더한 것이
        # **어떤 팽창 모형보다도 후하다** (상계). 그래도 안 오르면 결론이 난다.
        sv_v = np.linalg.svd(J_v, compute_uv=False)
        # 스케일 맞추기 — 두 채널의 열 노름을 같은 크기로 (가중은 자의적이므로
        # "가장 후한" 쪽으로 준다: 화학량론 채널을 전압 채널과 같은 노름으로)
        sc = np.linalg.norm(J_v) / np.linalg.norm(J_s)
        sv_a = np.linalg.svd(np.vstack([J_v, sc * J_s]), compute_uv=False)
        gain = 100 * (sv_a[-1] / sv_v[-1] - 1)
        print(f"   ── 전압 + 화학량론(동일 가중, **상계**) ──")
        print(f"      σ_min {sv_v[-1]:.4f} → {sv_a[-1]:.4f}   ({gain:+.1f} %)"
              f"   조건수 {sv_v[0]/sv_v[-1]:.2f} → {sv_a[0]/sv_a[-1]:.2f}")
        arows.append({"op": label, "mix": "상계 ([y;z] 통째)",
                      "sigma_min_voltage": float(sv_v[-1]),
                      "sigma_min_augmented": float(sv_a[-1]),
                      "gain_pct": float(gain),
                      "cond_voltage": float(sv_v[0] / sv_v[-1]),
                      "cond_augmented": float(sv_a[0] / sv_a[-1])})

        # ── 실제 팽창은 **스칼라** 다: E(x) = cosθ·y(x) + sinθ·z(x) ──────────
        #   계수 (n_c, tᵢ⁰, ξᵢ) 를 모르므로 **섞는 비를 훑는다.** 물리적으로는
        #   Gr+Si 음극의 팽창이 NMC 양극보다 훨씬 크므로 θ → 90° 쪽이 현실이다
        #   (Si 는 리튬화에서 ~300 %, 흑연 ~10 %, NMC 는 수 % 수준).
        print(f"   ── 스칼라 팽창 E = cosθ·y + sinθ·z 를 훑는다 (θ=90° = 순수 NE) ──")
        print(f"      {'θ':>5}{'∠(u_min(E),(1,1,1))':>22}{'σ_min 이득':>12}")
        for th_deg in (0, 30, 45, 60, 75, 90):
            th = np.radians(th_deg)
            J_E = np.cos(th) * J_y + np.sin(th) * J_z
            uE, svE = umin(J_E)
            aE = ang(uE, ONES)
            scE = np.linalg.norm(J_v) / np.linalg.norm(J_E)
            svE_a = np.linalg.svd(np.vstack([J_v, scE * J_E]), compute_uv=False)
            gE = 100 * (svE_a[-1] / sv_v[-1] - 1)
            star = "  ← 물리적으로 현실 쪽" if th_deg == 90 else ""
            print(f"      {th_deg:>4}°{aE:>21.2f}°{gE:>+11.1f} %{star}")
            arows.append({"op": label, "mix": f"θ={th_deg}°",
                          "angle_E_deg": aE,
                          "sigma_min_voltage": float(sv_v[-1]),
                          "sigma_min_augmented": float(svE_a[-1]),
                          "gain_pct": float(gE),
                          "cond_augmented": float(svE_a[0] / svE_a[-1])})

        # `(1,1,1)` 이 각 채널에 실제로 보이나 — 방향 미분의 크기
        print(f"   ── `(1,1,1)` 방향 미분의 크기 (최대 특이값 대비) ──")
        for nm, JJ in (("전압", J_v), ("y (PE)", J_y), ("z (NE)", J_z)):
            s_ = np.linalg.svd(JJ, compute_uv=False)
            r_ = np.linalg.norm(JJ @ ONES)
            print(f"      {nm:<8} ‖J·(1,1,1)/√3‖ = {r_:8.4f}"
                  f"   최대 대비 {r_/s_[0]:.4f}   최소 대비 {r_/s_[-1]:7.2f} 배")

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "angles.csv", index=False)
    pd.DataFrame(arows).to_csv(OUT / "augmented.csv", index=False)
    print(f"\n산출물: {OUT}/  (angles.csv · augmented.csv)")


if __name__ == "__main__":
    main()
