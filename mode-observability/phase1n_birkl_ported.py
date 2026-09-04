#!/usr/bin/env python3
"""Phase 1n — Birkl 식 (7)–(12) 가 막힌 것이 **구조인가 규약인가**. 전수로 가른다.

## 무엇이 남아 있었나

Phase 1f 가 Birkl 식 (7)–(12) 를 우리 좌표로 옮기려다 막혔다 — pristine 에서
식 (12) 에 **근이 없다**. 그리고 원인을 "두 `x` 정규화 사이 환산 부재" 로 적고
참고문헌 [33] 을 요청했다.

**그런데 1f 는 이미 `build_reference_interps("grid", …)` 를 썼다** — 곧 **셀-창**
정규화다 (Phase 1j 가 나중에 세운 바로 그 좌표계). 그러므로 "환산이 없어서" 는
정확한 진단이 아니었다. 남는 후보는 **방향 규약**이다:

- 우리 `s_NE` 는 **방전방향 정렬**이다 (`s=0` 이 만충, `s=1` 이 만방).
- Birkl 의 `x_NE` 는 **리튬화 분율**이라 방전에서 **감소**한다.
- **둘은 반대로 달린다.** 1f 는 Birkl 의 `x_NE` 를 우리 보간자에 그대로 먹였다.

증거: 1f 가 식 (11) 의 근으로 `Δx_EoC = 0.119891` 을 얻었는데, 그것은
`x_NE,EoC = 0.12` 라는 뜻이다. **만충에서 음극은 거의 가득 차 있어야 한다**
(리튬화 분율 ≈ 1). 0.12 는 축이 뒤집혔을 때 나오는 값이다.

## 이 스크립트가 하는 일 — 규약 전수

계수를 지어내지 않는다. **전사된 식은 그대로 두고**, 자연스러운 규약 선택지를
**전부 열거해** 어느 것이 pristine 에서 자기무모순인지 본다:

| 축 | 선택지 |
|---|---|
| PE 방향 | 전사대로 · 뒤집기 (`x → 1 − x`) |
| NE 방향 | 전사대로 · 뒤집기 |
| 식 (8) 의 `+1` | 전사대로 (8 에만) · (10) 으로 옮김 · 양쪽 · 없음 |

**2 × 2 × 4 = 16 가지.** 합격 기준은 셋 다:
1. 식 (11)·(12) 가 `Δx ∈ [−1.5, 1.5]` 안에 **근을 가진다**
2. 두 전극의 창 `[x_EoC, x_EoD]` 가 **`[0,1]` 안**에 있다
3. 두 창의 **폭이 0.1 이상** (퇴화하지 않는다)

`[해석]` **어느 것도 통과 못 하면** 막힌 것은 규약이 아니라 **식의 구조**이고,
1f 의 발견이 (진단은 틀렸어도) **더 강해진다.**
**정확히 하나가 통과하면** 그것이 전사와 어디가 다른지가 곧 답이다.

## 통과하면 그 다음 — Birkl 의 장부로 스펙트럼을 잰다

Birkl 은 **모드 3개 + 새 미지수 2개(`Δx_EoC, Δx_EoD`)를 도입하고 등식 2개가 그
둘을 잡는** 구조다. 이것은 Phase 1e(우리 창 4개에 제약을 **더한** 것)와도
Phase 1i(우리 모드 3개를 **제약한** 것)와도 **다른 장부**다. 통과하면 그
매개화의 3-모드 Jacobian 스펙트럼을 우리 자유 창 모델과 나란히 놓는다.

출력: results/phase1n/{variants.csv, spectrum.csv} + stdout. **CSV 가 정본이다.**
"""
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
DD = HERE.parent / "degradation-degeneracy"
sys.path.insert(0, str(DD))

from src.fitting import (  # noqa: E402
    build_reference_interps, extract_reference, modes_to_params, reconstruct)

CURVES = DD / "results" / "grid_curves_v4" / "curves.parquet"
OUT = HERE / "results" / "phase1n"
H = 0.02
LO, HI = 0.02, 0.98
MODES = ["LLI", "LAM_PE", "LAM_NE"]
ONES = np.ones(3) / np.sqrt(3.0)
SPAN = 1.5                      # Δx 탐색 구간 (전사판보다 넓게 — 근을 놓치지 않게)
MIN_W = 0.10                    # 창 폭 하한 (퇴화 판정)


def main():
    if not CURVES.exists():
        sys.exit(f"곡선 파일이 없다: {CURVES}")

    df = pd.read_parquet(CURVES, columns=[
        "cond_id", "lli", "lam_pe", "lam_ne", "noise", "q_mah",
        "x_norm", "v_pe", "v_ne", "v_full"])
    d0 = df[df.noise == 0]
    ref = extract_reference(d0)
    xa = ref.x_norm.to_numpy(float)
    xs = xa[(xa >= LO) & (xa <= HI)]
    q0 = float(ref.q_mah.iloc[0])
    grid_ref = {"x": xa, "pe": ref.v_pe.to_numpy(float), "ne": ref.v_ne.to_numpy(float)}
    f_pe0, f_ne0 = build_reference_interps("grid", grid_ref)
    v_ref = ref.v_full.to_numpy(float)
    E_high, E_low = float(v_ref[0]), float(v_ref[-1])
    print(f"컷오프 상수 (reference 자신의 양 끝)  E_high {E_high:.4f} V · "
          f"E_low {E_low:.4f} V")
    print(f"reference {len(xa)}점 · 관측 {len(xs)}점 · q0 {q0:.2f} mAh\n")

    def variant(flip_pe, flip_ne, one_where):
        """규약 하나를 고르면 (stoich, f_pe, f_ne) 를 돌려준다."""
        fpe = (lambda u: f_pe0(1.0 - np.asarray(u))) if flip_pe else f_pe0
        fne = (lambda u: f_ne0(1.0 - np.asarray(u))) if flip_ne else f_ne0
        one_pe = 1.0 if one_where in ("8", "both") else 0.0
        one_ne = 1.0 if one_where in ("10", "both") else 0.0

        def stoich(lli, lam_pe, lam_ne, dxc, dxd):
            return (dxc / (1 - lam_pe),                                    # (7)
                    (dxd + one_pe - lli + lam_pe) / (1 - lam_pe),          # (8)
                    (dxc + lli - lam_ne) / (1 - lam_ne),                   # (9)
                    (dxd + one_ne) / (1 - lam_ne))                         # (10)
        return stoich, fpe, fne

    def solve(stoich, fpe, fne, lli, lam_pe, lam_ne):
        """식 (11)(12) 를 각각 1차원으로 푼다 (두 식이 분리된다)."""
        def g_c(dx):
            p, _, n, _ = stoich(lli, lam_pe, lam_ne, dx, 0.0)
            return E_high - (float(fpe(p)) - float(fne(n)))
        def g_d(dx):
            _, p, _, n = stoich(lli, lam_pe, lam_ne, 0.0, dx)
            return E_low - (float(fpe(p)) - float(fne(n)))
        out = []
        for g in (g_c, g_d):
            gr = np.linspace(-SPAN, SPAN, 601)
            vals = np.array([g(t) for t in gr])
            sign = np.where(np.diff(np.sign(vals)) != 0)[0]
            if len(sign) == 0:
                return None
            i = sign[0]
            out.append(brentq(g, gr[i], gr[i + 1], xtol=1e-12))
        return tuple(out)

    # ── ① 규약 16가지 전수 ────────────────────────────────────────────────
    print("── ① 규약 전수 (pristine 자기무모순 검사) ──")
    print(f"   {'PE':>4}{'NE':>4}{'+1 위치':>9}   {'근':>4}  "
          f"{'PE 창 [EoC,EoD]':>22}{'NE 창':>22}  판정")
    rows, passing = [], []
    for flip_pe, flip_ne, one_where in itertools.product(
            [False, True], [False, True], ["8", "10", "both", "none"]):
        stoich, fpe, fne = variant(flip_pe, flip_ne, one_where)
        dx = solve(stoich, fpe, fne, 0.0, 0.0, 0.0)
        tag_pe = "뒤집" if flip_pe else "전사"
        tag_ne = "뒤집" if flip_ne else "전사"
        if dx is None:
            print(f"   {tag_pe:>4}{tag_ne:>4}{one_where:>9}   {'없음':>4}"
                  f"{'':>22}{'':>22}  ✗ 근 없음")
            rows.append({"flip_pe": flip_pe, "flip_ne": flip_ne,
                         "one_where": one_where, "verdict": "no-root"})
            continue
        pc, pd_, nc, nd = stoich(0.0, 0.0, 0.0, *dx)
        wp, wn = pd_ - pc, nd - nc
        inside = all(-1e-9 <= t <= 1 + 1e-9 for t in (pc, pd_, nc, nd))
        wide = abs(wp) >= MIN_W and abs(wn) >= MIN_W
        ok = inside and wide
        why = "✓ 통과" if ok else ("✗ 창이 [0,1] 밖" if not inside else "✗ 창 퇴화")
        print(f"   {tag_pe:>4}{tag_ne:>4}{one_where:>9}   {'있음':>4}"
              f"  [{pc:+.3f},{pd_:+.3f}] w={wp:+.3f}"
              f"  [{nc:+.3f},{nd:+.3f}] w={wn:+.3f}  {why}")
        rows.append({"flip_pe": flip_pe, "flip_ne": flip_ne, "one_where": one_where,
                     "dx_eoc": dx[0], "dx_eod": dx[1],
                     "x_pe_eoc": pc, "x_pe_eod": pd_, "x_ne_eoc": nc, "x_ne_eod": nd,
                     "w_pe": wp, "w_ne": wn, "verdict": "pass" if ok else why})
        if ok:
            passing.append((flip_pe, flip_ne, one_where, dx))

    OUT.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT / "variants.csv", index=False)
    print(f"\n   → 통과 {len(passing)} / 16")

    if not passing:
        print("\n**어느 규약도 통과하지 못한다.**")
        print("`[해석]` 막힌 것은 규약이 아니라 **식의 구조**다. Phase 1f 의")
        print("발견은 (진단이 '환산 부재' 로 틀렸어도) **더 강해진다** — 참고문헌")
        print("[33] 이 채워야 할 것은 환산이 아니라 **식 자체의 빠진 층**이다.")
        print(f"\n산출물: {OUT}/  (variants.csv)")
        return

    # ── ② 통과한 규약으로 3-파라미터 스펙트럼 ─────────────────────────────
    print("\n── ② 통과 규약으로 Birkl 3-파라미터 판의 스펙트럼 ──")
    print("   (Birkl 장부 = 모드 3 + 미지수 2, 등식 2 가 그 둘을 잡는다 —")
    print("    Phase 1e·1i 와 **다른 장부**다)\n")

    uniq = d0[["cond_id", "lli", "lam_pe", "lam_ne", "q_mah"]].drop_duplicates()

    def q_of(l, p, n):
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        return None if r.empty else float(r.q_mah.iloc[0])

    def sim_curve(l, p, n):
        """격자의 **실제 PyBaMM 시뮬** 곡선 — 두 매개화의 공통 심판."""
        r = uniq[np.isclose(uniq.lli, l) & np.isclose(uniq.lam_pe, p)
                 & np.isclose(uniq.lam_ne, n)]
        if r.empty:
            return None
        g = d0[d0.cond_id == r.cond_id.iloc[0]].sort_values("x_norm")
        return np.interp(xs, g.x_norm.to_numpy(float), g.v_full.to_numpy(float))

    srows = []
    keep = None          # ③ 심판에 넘길 대표 Birkl 변종 (J, 이름)
    for flip_pe, flip_ne, one_where, _ in passing:
        stoich, fpe, fne = variant(flip_pe, flip_ne, one_where)

        def curve_birkl(l, p, n):
            dx = solve(stoich, fpe, fne, l, p, n)
            if dx is None:
                return None
            pc, pd_, nc, nd = stoich(l, p, n, *dx)
            wp, wn = pd_ - pc, nd - nc
            if abs(wp) < 1e-6 or abs(wn) < 1e-6:
                return None
            a_pe, a_ne = 1.0 / wp, 1.0 / wn
            par = np.array([a_pe, -pc * a_pe, a_ne, -nc * a_ne])
            _, _, full = reconstruct(par, fpe, fne, xs)
            return full

        base = curve_birkl(0, 0, 0)
        if base is None:
            print(f"   [{flip_pe},{flip_ne},{one_where}] base 실패")
            continue

        # ★ 이식 검산 — **모드를 움직였을 때 시뮬 참값을 따라가는가.**
        #   pristine 에서만 보면 창이 정확히 [0,1] 이라 재구성이 곧 reference 라
        #   **항등식**이고 판별력이 없다 (실측 0.00 mV). 진짜 시험은 축 조건이다.
        errs = []
        for a in [(H, 0, 0), (0, H, 0), (0, 0, H)]:
            vt = sim_curve(*a)
            vb = curve_birkl(*a)
            if vt is None or vb is None:
                continue
            m = np.isfinite(vt) & np.isfinite(vb)
            errs.append(float(np.abs(vb[m] - vt[m]).mean() * 1e3))
        dvv = np.array(errs) if errs else np.array([np.nan])
        gate = np.isfinite(dvv).all() and dvv.mean() < 60.0
        cols = []
        for a in [(H, 0, 0), (0, H, 0), (0, 0, H)]:
            c = curve_birkl(*a)
            if c is None:
                cols = None
                break
            cols.append((c - base) / H)
        if cols is None:
            print(f"   [{flip_pe},{flip_ne},{one_where}] 축 조건에서 근 소실")
            continue
        J_full = np.column_stack(cols)
        ok = np.isfinite(J_full).all(axis=1) & np.isfinite(base)
        J = J_full[ok]
        w, V = np.linalg.eigh(J.T @ J)
        sv = np.sqrt(np.maximum(w, 0.0))
        u = V[:, 0] / np.linalg.norm(V[:, 0])
        u = -u if u.sum() < 0 else u
        ang = float(np.degrees(np.arccos(np.clip(abs(u @ ONES), -1, 1))))
        tag = f"PE {'뒤집' if flip_pe else '전사'} · NE {'뒤집' if flip_ne else '전사'} · +1 {one_where}"
        cond = (sv[-1] / sv[0]) if sv[0] > 1e-12 else float("inf")
        print(f"   {tag}")
        print(f"      ★ 이식 검산: pristine 재구성 vs 실제 곡선  평균 {dvv.mean():7.2f} mV"
              f" · 최대 {dvv.max():7.2f} mV   {'✓ 이 셀이다' if gate else '✗ **이 셀이 아니다** — 아래 스펙트럼 무효'}")
        print(f"      특이값 {np.round(sv, 4)}   조건수 {cond:.2f}")
        print(f"      u_min {np.round(u, 5)}   ∠(1,1,1) = **{ang:.2f}°**   유효 {J.shape[0]}점")
        # ③ 대표 선정: 이식 검산을 통과하고 퇴화(σ_min = 0)하지 않은 것 중 최선
        if gate and sv[0] > 1e-12 and (keep is None or dvv.mean() < keep[2]):
            keep = (J_full, tag, float(dvv.mean()))
        srows.append({"variant": tag, "cond": float(cond),
                      "recon_mae_mV": float(dvv.mean()),
                      "recon_max_mV": float(dvv.max()),
                      "port_valid": bool(gate),
                      "angle_deg": ang, "n_points": int(J.shape[0]),
                      **{f"sv{i+1}": float(sv[i]) for i in range(3)},
                      **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)}})

    # 대조 — 우리 자유 창 모델 (같은 관측·같은 스텝)
    def curve_ours(l, p, n):
        q = q_of(l, p, n)
        if q is None:
            return None
        _, _, full = reconstruct(modes_to_params(p, n, l, q / q0), f_pe0, f_ne0, xs)
        return full

    b0 = curve_ours(0, 0, 0)
    Jo_full = np.column_stack([(curve_ours(*a) - b0) / H
                               for a in [(H, 0, 0), (0, H, 0), (0, 0, H)]])
    ok = np.isfinite(Jo_full).all(axis=1) & np.isfinite(b0)
    Jo = Jo_full[ok]
    w, V = np.linalg.eigh(Jo.T @ Jo)
    sv = np.sqrt(np.maximum(w, 0.0))
    u = V[:, 0] / np.linalg.norm(V[:, 0]); u = -u if u.sum() < 0 else u
    ango = float(np.degrees(np.arccos(np.clip(abs(u @ ONES), -1, 1))))
    # 같은 심판으로 우리 모델도 잰다 (공정한 맞대결)
    eo = []
    for a in [(H, 0, 0), (0, H, 0), (0, 0, H)]:
        vt, vb = sim_curve(*a), curve_ours(*a)
        if vt is None or vb is None:
            continue
        m = np.isfinite(vt) & np.isfinite(vb)
        eo.append(float(np.abs(vb[m] - vt[m]).mean() * 1e3))
    eo = np.array(eo)
    print(f"\n   [대조] 우리 자유 창 모델 (`modes_to_params`)")
    print(f"      ★ 같은 검산: 시뮬 참값 추종  평균 {eo.mean():7.2f} mV"
          f" · 최대 {eo.max():7.2f} mV")
    print(f"      특이값 {np.round(sv, 4)}   조건수 {sv[-1]/sv[0]:.2f}"
          f"   ∠(1,1,1) = {ango:.2f}°")
    srows.append({"variant": "[대조] 우리 자유 창 모델", "cond": float(sv[-1] / sv[0]),
                  "recon_mae_mV": float(eo.mean()), "recon_max_mV": float(eo.max()),
                  "port_valid": True,
                  "angle_deg": ango, "n_points": int(Jo.shape[0]),
                  **{f"sv{i+1}": float(sv[i]) for i in range(3)},
                  **{f"u_min_{m}": u[i] for i, m in enumerate(MODES)}})

    # ── ③ 심판 — **시뮬 Jacobian 자신**과 대조한다 ────────────────────────
    #   두 매개화가 곡선은 비슷하게 맞추는데 null 방향이 76° 어긋난다.
    #   어느 쪽이 우리 셀의 실제 국소 기하인가는 **곡선이 아니라 도함수**가 정한다.
    vb0 = sim_curve(0, 0, 0)
    Js_full = np.column_stack([(sim_curve(*a) - vb0) / H
                               for a in [(H, 0, 0), (0, H, 0), (0, 0, H)]])
    # 세 Jacobian 을 **같은 관측점 집합** 위에서 비교한다. 앞에서부터 잘라 빼면
    # 그 차이는 기하가 아니라 잘림이다 (첫 실행에서 282 vs 288 로 걸렸다).
    common = np.isfinite(Js_full).all(axis=1) & np.isfinite(Jo_full).all(axis=1)
    if keep is not None:
        common &= np.isfinite(keep[0]).all(axis=1)
    Js = Js_full[common]
    ws, Vs = np.linalg.eigh(Js.T @ Js)
    us = Vs[:, 0] / np.linalg.norm(Vs[:, 0]); us = -us if us.sum() < 0 else us
    svs = np.sqrt(np.maximum(ws, 0.0))
    print("\n── ③ 심판: 격자의 **실제 시뮬 Jacobian** (Phase 1c 와 같은 것) ──")
    print(f"   공통 관측점 {int(common.sum())} / {len(common)} — 세 Jacobian 을 "
          f"같은 점 위에서 비교한다")
    print(f"   특이값 {np.round(svs, 4)}   조건수 {svs[-1]/svs[0]:.2f}")
    print(f"   u_min {np.round(us, 5)}   ∠(1,1,1) = **{float(np.degrees(np.arccos(np.clip(abs(us@ONES),-1,1)))):.2f}°**")
    # ★ 자기점검 — 검산 게이트가 실제로 판별력이 있었나.
    #   축 조건 하나가 pristine 에서 움직이는 크기(= 미분되는 신호 자체)를 잰다.
    sig = float(np.abs(Js * H).mean() * 1e3)
    gerr = [eo.mean()] + ([keep[2]] if keep is not None else [])
    print(f"\n   ★ 신호 크기: 축 한 걸음(Δ={H})이 곡선을 움직이는 평균 {sig:.2f} mV.")
    print(f"      ② 의 이식 검산 오차 {min(gerr):.2f}~{max(gerr):.2f} mV 는 이 신호의 "
          f"{min(gerr)/sig:.1f}~{max(gerr)/sig:.1f} 배 —")
    print(f"      곧 게이트 60 mV 는 너무 느슨했고 '✓ 이 셀이다' 는 **약한 주장**이다.")
    print(f"\n   {'매개화':<34}{'열 상대오차':>12}{'최적배율 c':>11}"
          f"{'c 뒤 잔차':>10}{'∠(u_min, 시뮬 u_min)':>22}")
    jrows = []
    cands = []
    if keep is None:
        print("   (Birkl 쪽 대표 없음 — 이식 검산 통과 + 비퇴화 변종이 하나도 없다)")
    else:
        cands.append((f"Birkl 이식 [{keep[1]}]", keep[0][common]))
    cands.append(("우리 자유 창 모델", Jo_full[common]))
    for tag, Jm in cands:
        rel = float(np.linalg.norm(Jm - Js) / np.linalg.norm(Js))
        # 크기와 모양을 가른다: 두 해석 모델 모두 응답이 과대하다. 최적 스칼라
        # 배율 c 를 빼고 남는 잔차가 **모양**의 오차다.
        c = float((Jm * Js).sum() / (Jm * Jm).sum())
        rel_c = float(np.linalg.norm(c * Jm - Js) / np.linalg.norm(Js))
        wm, Vm = np.linalg.eigh(Jm.T @ Jm)
        um = Vm[:, 0] / np.linalg.norm(Vm[:, 0]); um = -um if um.sum() < 0 else um
        a_s = float(np.degrees(np.arccos(np.clip(abs(um @ us), -1, 1))))
        print(f"   {tag:<34}{100*rel:>11.1f}%{c:>11.3f}{100*rel_c:>9.1f}%{a_s:>21.2f}°")
        jrows.append({"variant": tag, "jacobian_rel_err": rel,
                      "best_scale_c": c, "rel_err_after_scale": rel_c,
                      "angle_to_sim_umin_deg": a_s, "n_points": int(len(Jm))})
    # ── ④ c < 0 은 어디서 오나 — 열별로 가른다 ────────────────────────────
    #   전체 c 가 음수라는 것은 두 행렬이 **반대로** 움직인다는 뜻이다.
    #   축별로 봐야 그것이 한 열의 문제인지 전면적인지 알 수 있다.
    print(f"\n── ④ 열별 진단 (전체 c 가 음수인 이유) ──")
    print(f"   {'축':>8}{'‖시뮬열‖':>11}{'‖모델열‖':>11}{'cos':>9}   매개화")
    crows = []
    for tag, Jm in cands:
        for i, m in enumerate(MODES):
            cs, cm = Js[:, i], Jm[:, i]
            cos = float(cs @ cm / (np.linalg.norm(cs) * np.linalg.norm(cm)))
            print(f"   {m:>8}{np.linalg.norm(cs):>11.3f}{np.linalg.norm(cm):>11.3f}"
                  f"{cos:>9.3f}   {tag}")
            crows.append({"variant": tag, "mode": m, "sim_col_norm": float(np.linalg.norm(cs)),
                          "model_col_norm": float(np.linalg.norm(cm)), "cos": cos})
    pd.DataFrame(crows).to_csv(OUT / "columns.csv", index=False)
    cdf = pd.DataFrame(crows)
    print()
    for tag, _ in cands:
        g = cdf[cdf.variant == tag]
        best = g.loc[g.cos.idxmax()]
        nneg = int((g.cos < 0).sum())
        print(f"   {tag}: 최선 열 {best['mode']} cos {best.cos:+.3f} · 음수 열 {nneg}/3")
    print("\n   `[해석]` 어느 쪽도 세 열을 다 맞히지 못한다. 그러므로 ③ 이 지지하는")
    print("   것은 'u_min 이 (1,1,1) 근방인가' 라는 **이분법뿐**이고, 각도의 정확한")
    print("   값이나 열 오차의 순위는 이 실험으로 주장할 수 없다.")

    pd.DataFrame(jrows).to_csv(OUT / "arbiter.csv", index=False)

    pd.DataFrame(srows).to_csv(OUT / "spectrum.csv", index=False)
    print(f"\n산출물: {OUT}/  (variants.csv · spectrum.csv · arbiter.csv · columns.csv)")


if __name__ == "__main__":
    main()
