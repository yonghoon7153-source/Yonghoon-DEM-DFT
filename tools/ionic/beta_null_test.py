#!/usr/bin/env python3
"""beta_null_test.py — β 게이트의 **귀무분포**를 잰다: "완벽히 확산하는 계도 β<0.8 이 나오나?"

왜 필요한가 (2026-08-11)
  `msd_diffusive_check.py` 는 β<0.80 을 '케이지'로 부른다. 그런데 그 β 는 **단일
  시간원점** MSD 에서 잰 값이고, 표본은 이온 n_Li 개뿐이다. 표본이 적으면 **진짜
  확산하는 궤적도** β 가 크게 흔들린다 — 그럼 게이트가 물리가 아니라 잡음을 재게 된다.

  실측 계기: arrhenius_6pt 21런 중 8개가 '케이지'로 탈락했는데, 그 8개의
  **창끝 MSD 가 24–138 Å²** 였다. 900 K 에서 MSD 138 Å²(RMS ~12 Å, 격자 여러 칸)면
  물리적으로 케이지일 수 없다. 즉 게이트가 오작동한다는 신호다.

이 도구가 하는 일
  같은 (n_Li, 프레임 수, dt, D) 로 **이상적인 브라운 운동**을 만들어 같은 추정기로
  β 를 잰다. 물리적 케이지는 0이고 통계 잡음만 있는 계다. 그 β 분포가
    · 0.8 아래를 자주 밟으면 → **게이트 임계가 틀렸다** (거짓 탈락)
    · 1 근처에 몰려 있으면  → 실측 β<0.8 은 진짜 케이지다
  둘 중 하나로 갈린다. 어느 쪽이든 답이 나온다.

⚠ 이건 MD 를 대신하지 않는다. **게이트를 검정**할 뿐이다.

  python3 tools/ionic/beta_null_test.py --n_li 27 --n_frames 2000 --dt_ps 0.1
  python3 tools/ionic/beta_null_test.py --from_msd ~/work/runs/.../msd.json
  python3 tools/ionic/beta_null_test.py --hop_sweep --csv db/properties/beta_gate_null_vs_hops_origin.csv

이 도구가 못 하는 것
  · MD 를 대신하지 못한다 — 게이트(추정기)를 검정할 뿐이다.
  · 진짜 sub-diffusion 을 만들지 못한다 — 귀무는 전부 Fickian+케이지다. 그래서
    "게이트가 잡음을 잰다" 는 말할 수 있어도 "실측 β 낮음 = 잡음" 은 단정 못 한다.
  · --hop_sweep 의 n_hop 은 MSD/d_hop² 환산(상한 추정)이다 — 되돌아오는 홉을
    세지 않으므로 실제 이벤트 수보다 낙관적이다 (hops_per_ion.py 와 같은 한계).
"""
import argparse
import json
import math
import os
import sys

import numpy as np

WINDOWS = [(2.0, 50.0), (10.0, 50.0), (25.0, 100.0), (50.0, 200.0)]


def beta_of(t, y, lo, hi):
    """log-log 기울기 — msd_diffusive_check.py 와 같은 정의."""
    m = [(a, b) for a, b in zip(t, y) if lo <= a <= hi and a > 0 and b > 0]
    if len(m) < 3:
        return None
    lx = np.log([p[0] for p in m]); ly = np.log([p[1] for p in m])
    return float(np.polyfit(lx, ly, 1)[0])


def synth(n_li, n_frames, dt_ps, D_cm2_s, rng, cage_A2=0.0, tau_ps=1.0):
    """3D 브라운 운동 + (선택) 케이지 진동 → 단일 시간원점 MSD.

    ⛔⛔ 2026-08-11 자체검토 P0 — **초판은 cage_A2 = 0 만 돌렸고, 그 모형은 β<0.8 을
      구조적으로 만들 수 없다.** 모든 이온을 t=0 에 정확히 원점에 두므로 MSD 절편이
      항등적으로 0 이기 때문이다. 실제 고체 MSD 는 어느 계든

          MSD(t) = C + 6Dt        (C = 케이지 진폭 + ballistic 잔재)

      이고, C > 0 이면 log-log 기울기 β 는 **자동으로 1 아래**로 내려간다.
      즉 초판의 "1.0 %" 는 **케이지가 없는 계의 거짓탈락률**이지 우리 계의 것이 아니다.

      cage 를 넣고 잰 값 (Li 27 · 200 ps · 창 2–50 · 장시간 D 는 입력값과 **정확히 일치**):

        C ≈ 0 Å²  → β 중앙값 1.006 · P(β<0.8) = 1.1 %
        C ≈ 2 Å²  → 0.844 · **27.7 %**
        C ≈ 4 Å²  → 0.745 · **74.0 %**
        C ≈ 6 Å²  → 0.668 · **98.0 %**

      우리 db 의 실측 절편(db/properties/msd_3sys_200ps_origin.csv)은 1.7–4.0 Å² 다.
      ⇒ **"진짜 확산 + 정상적인 케이지 진동" 만으로 8/21 탈락(38 %)이 나온다.**

    ⚠ 그러므로 이 도구의 결론은 "β<0.8 이면 sub-diffusion" 이 아니라
      **"β<0.8 은 절편이 창끝 MSD 의 ~6 % 를 넘었다는 뜻"** 이다. 둘을 가르는 건
      `msd_diffusive_check.py --scan` 의 **c 행**이지 β 값이 아니다.
    """
    # D [cm²/s] → Å²/ps :  1 cm²/s = 1e16 Å² / 1e12 ps = 1e4 Å²/ps
    D_a2_ps = D_cm2_s * 1e4
    sigma = math.sqrt(2.0 * D_a2_ps * dt_ps)          # 축당 스텝 표준편차
    steps = rng.normal(0.0, sigma, size=(n_frames - 1, n_li, 3))
    pos = np.concatenate([np.zeros((1, n_li, 3)), np.cumsum(steps, axis=0)], axis=0)
    if cage_A2 > 0:
        # OU 케이지 — 장시간 D 를 **안 바꾸는** 정상 과정. 축당 분산 cage_A2/3.
        a = math.exp(-dt_ps / tau_ps)
        sd_u = math.sqrt(cage_A2 / 3.0)
        u = np.empty((n_frames, n_li, 3))
        u[0] = rng.normal(0.0, sd_u, size=(n_li, 3))
        drv = rng.normal(0.0, sd_u * math.sqrt(1 - a * a), size=(n_frames - 1, n_li, 3))
        for k in range(1, n_frames):
            u[k] = a * u[k - 1] + drv[k - 1]
        pos = pos + u - u[0]          # t=0 에서 0 이 되도록 (절편은 상관 감쇠로 생긴다)
    msd = (pos ** 2).sum(-1).mean(-1)                  # 원점 = 첫 프레임 (단일 시간원점)
    t = np.arange(n_frames) * dt_ps
    return t, msd


def ideal_beta(n_hop, cage_A2, tau_ps=1.0, prod_ps=200.0, d_hop=3.0,
               lo=2.0, hi=50.0, dt_ps=0.1):
    """잡음 0 인 이상 곡선 MSD(t)=2·cage_A2·(1−e^{−t/τ})+6Dt 의 창내 log-log 기울기.

    n_hop 은 hops_per_ion.py 규약(= MSD@prod / d_hop², 상한 추정)으로 D 를 역산한다.
    OU 케이지의 장시간 절편은 2·cage_A2 다 (분산 감쇠 항등식) — cage_A2 가 아니라.
    """
    if n_hop <= 0:
        raise ValueError(f"n_hop 은 양수여야 한다: {n_hop}")
    D_a2ps = n_hop * d_hop ** 2 / (6.0 * prod_ps)          # MSD@prod = n_hop·d_hop²
    t = np.arange(dt_ps, hi + dt_ps, dt_ps)
    y = 2.0 * cage_A2 * (1.0 - np.exp(-t / tau_ps)) + 6.0 * D_a2ps * t
    return beta_of(t, y, lo, hi), D_a2ps * 1e-4            # (β_det, D[cm²/s])


def hop_sweep(a):
    """n_hop 축으로 귀무분포 스윕 — "홉이 몇 개면 β 게이트를 믿을 수 있나".

    각 n_hop(200 ps 기준)에서: 이상곡선 β_det + MC 분포(중앙값·5–95%·P(β<gate)·
    5% 분위수 β_crit). β_crit 이 곧 "이 홉 수에서 거짓탈락 5% 를 주는 문턱"이다.
    """
    rng = np.random.default_rng(a.seed)
    lo, hi = 2.0, 50.0                                     # 캠페인 규약 창 고정
    prod_ps = (a.n_frames - 1) * a.dt_ps
    grid = [1.0, 2.0, 3.0, 5.0, 8.4, 10.0, 13.9, 20.0, 30.0]  # 8.4/13.9 = 우리 실측 계
    print(f"홉 스윕 — 절편 2·cage = {2*a.cage_A2:.1f} Å² (실측: modelc 2.3 / b2o3 1.7 / "
          f"lpsocl 4.0) · Li {a.n_li} · {prod_ps:.0f} ps · 창 {lo:g}–{hi:g} · {a.trials}회/점")
    print(f"⚠ 모든 행이 **진짜 Fickian** 이다 — β<{a.gate} 는 전부 거짓탈락이다.\n")
    hdr = (f"{'n_hop@200ps':>11s} {'D [cm²/s]':>10s} {'c/MSD@50':>9s} {'β_det':>6s} "
           f"{'β 중앙값':>8s} {'β 5–95%':>12s} {f'P(β<{a.gate})':>10s} {'β_crit5%':>9s}")
    print(hdr)
    rows = []
    for nh in grid:
        b_det, D_cm2 = ideal_beta(nh, a.cage_A2, a.tau_ps, prod_ps, lo=lo, hi=hi,
                                  dt_ps=a.dt_ps)
        c_eff = 2.0 * a.cage_A2
        msd50 = 6.0 * D_cm2 * 1e4 * hi + c_eff
        bs = []
        for _ in range(a.trials):
            t, y = synth(a.n_li, a.n_frames, a.dt_ps, D_cm2, rng,
                         cage_A2=a.cage_A2, tau_ps=a.tau_ps)
            b = beta_of(t, y, lo, hi)
            if b is not None:
                bs.append(b)
        bs = np.array(bs)
        p_fail = float((bs < a.gate).mean())
        crit5 = float(np.percentile(bs, 5))
        rows.append({"n_hop_200ps": nh, "D_cm2_s": D_cm2,
                     "c_over_msd50_pct": 100 * c_eff / msd50,
                     "beta_deterministic": round(b_det, 3),
                     "beta_median": round(float(np.median(bs)), 3),
                     "beta_p5": round(float(np.percentile(bs, 5)), 3),
                     "beta_p95": round(float(np.percentile(bs, 95)), 3),
                     "false_fail_pct": round(100 * p_fail, 1),
                     "beta_crit_5pct": round(crit5, 3)})
        print(f"{nh:11.1f} {D_cm2:10.2e} {100*c_eff/msd50:8.1f}% {b_det:6.2f} "
              f"{np.median(bs):8.2f} {f'{np.percentile(bs,5):.2f}–{np.percentile(bs,95):.2f}':>12s} "
              f"{100*p_fail:9.1f}% {crit5:9.2f}")
    # 게이트 0.8 이 건전해지는 최소 홉 수 (거짓탈락 <5%)
    sound = [r for r in rows if r["false_fail_pct"] < 5.0]
    print()
    if sound:
        print(f"→ **β≥{a.gate} 게이트가 건전한(거짓탈락<5%) 최소 홉 수: "
              f"n_hop ≈ {sound[0]['n_hop_200ps']:g}** (이 절편 크기 기준)")
    else:
        print(f"→ ⛔ 이 절편({2*a.cage_A2:.1f} Å²)에서는 어떤 홉 수에서도 β≥{a.gate} "
              f"게이트가 5% 기준을 못 넘는다 — 문턱을 β_crit5% 열에서 다시 골라야 한다")
    print("   실측 대조: modelc 600 K (홉 13.9, β 0.87) · b2o3 600 K (13.9, 0.81) · "
          "lpsocl 600 K (8.4, 0.61)")
    if a.csv:
        import csv as _csv
        with open(a.csv, "w", newline="") as f:
            f.write(f"# beta gate null distribution vs hop count. window {lo:g}-{hi:g} ps, "
                    f"n_Li {a.n_li}, prod {prod_ps:.0f} ps, cage intercept {2*a.cage_A2:.1f} A^2, "
                    f"{a.trials} trials, seed {a.seed}. All rows are TRUE Fickian - "
                    f"false_fail_pct is the false-rejection rate of the beta>={a.gate} gate.\n")
            f.write("# n_hop convention = MSD(prod)/d_hop^2, d_hop 3 A (hops_per_ion.py). "
                    "beta_crit_5pct = 5th percentile of null beta = threshold giving 5% false fail.\n")
            w = _csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"CSV → {a.csv}")
    return 0


def selftest():
    """새 경로(ideal_beta/hop_sweep 수식)만 검정한다 — MC 본체는 통계 도구라 제외."""
    bad = 0
    # 양성: 절편 0 이면 이상곡선 β = 1 정확히
    b, D = ideal_beta(10.0, 0.0)
    if abs(b - 1.0) > 1e-6:
        print(f"FAIL: cage 0 인데 β_det={b}"); bad += 1
    # 양성: D 역산 — n_hop 10 · 200 ps · d_hop 3 → MSD@200 = 90 Å² → D = 7.5e-6 cm²/s
    if abs(D - 90.0 / (6 * 200.0) * 1e-4) > 1e-12:
        print(f"FAIL: D 역산 {D}"); bad += 1
    # 양성: 절편이 커지면 β_det 는 단조 감소
    b1, _ = ideal_beta(5.0, 1.0)
    b2, _ = ideal_beta(5.0, 3.0)
    if not (b2 < b1 < 1.0):
        print(f"FAIL: 절편 단조성 {b1} {b2}"); bad += 1
    # 양성: 홉이 많아지면 β_det → 1 (절편 고정)
    b3, _ = ideal_beta(100.0, 1.0)
    if not (b3 > b1):
        print(f"FAIL: 홉 단조성 {b1} {b3}"); bad += 1
    # 음성: n_hop ≤ 0 은 거부해야 한다
    try:
        ideal_beta(0.0, 1.0)
        print("FAIL: n_hop 0 이 통과했다"); bad += 1
    except ValueError:
        pass
    # 음성: 절편이 지배하면 β_det 가 0.8 아래로 떨어져야 한다 (게이트가 실제로 반응하는지)
    b4, _ = ideal_beta(1.0, 2.0)      # 홉 1 · 절편 4 Å² → c/MSD@50 ≈ 64%
    if not (b4 < 0.8):
        print(f"FAIL: 절편 지배인데 β_det={b4} ≥ 0.8"); bad += 1
    print(f"selftest {'PASS' if not bad else 'FAIL'} — {6 - bad} ok, {bad} bad")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_li", type=int, default=27, help="확산 이온 수 (MSD 를 평균할 표본)")
    ap.add_argument("--n_frames", type=int, default=2000, help="prod 프레임 수 (200 ps / 0.1 ps)")
    ap.add_argument("--dt_ps", type=float, default=0.1, help="프레임 간격 = save_fs/1000")
    ap.add_argument("--D", type=float, default=1.5e-5, help="참 D [cm²/s]")
    ap.add_argument("--trials", type=int, default=2000,
                    help="⚠ 1% 꼬리를 재려면 400 회는 부족하다 (MC 오차 ±0.5%)")
    ap.add_argument("--cage_A2", type=float, default=2.0,
                    help="케이지 진폭 <u²> [Å²] — **기본 2.0**. 0 으로 두면 절편 없는 "
                         "비현실적 귀무가 된다 (우리 db 실측 절편 1.7–4.0 Å²)")
    ap.add_argument("--tau_ps", type=float, default=1.0, help="케이지 상관시간")
    ap.add_argument("--gate", type=float, default=0.80, help="검정할 게이트 임계")
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--from_msd", help="실제 msd.json 에서 n_Li·프레임·dt·D 를 읽어 맞춘다")
    ap.add_argument("--hop_sweep", action="store_true",
                    help="n_hop 축 스윕 — '홉 몇 개부터 β 게이트를 믿을 수 있나' 표")
    ap.add_argument("--csv", help="--hop_sweep 결과를 Origin-ready CSV 로 저장")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        sys.exit(selftest())
    if a.hop_sweep:
        sys.exit(hop_sweep(a))

    if a.from_msd:
        d = json.load(open(os.path.expanduser(a.from_msd)))
        t = d.get("times_ps") or []
        if len(t) < 2:
            sys.exit(f"⛔ times_ps 가 없다: {a.from_msd}")
        a.n_frames, a.dt_ps = len(t), float(t[1] - t[0])
        if d.get("n_Li"):
            a.n_li = int(d["n_Li"])
        if d.get("D_Li_cm2_s"):
            a.D = float(d["D_Li_cm2_s"])
        print(f"실측에서 맞춤: {a.from_msd}")

    rng = np.random.default_rng(a.seed)
    print(f"브라운 운동 + 케이지 <u²>={a.cage_A2} Å² (τ {a.tau_ps} ps) — Li {a.n_li}개 · 프레임 {a.n_frames} (dt {a.dt_ps} ps, "
          f"총 {(a.n_frames - 1) * a.dt_ps:.0f} ps) · 참 D {a.D:.3e} cm²/s · {a.trials}회")
    print("⚠ 이 계는 **장시간 D 가 입력값과 정확히 같다** = 진짜 Fickian 이다.\n   여기서 β<게이트 가 나오는 건 sub-diffusion 이 아니라 **절편** 때문이다.\n")

    print(f"{'창 [ps]':>12s} {'β 중앙값':>9s} {'β 5–95%':>16s} "
          f"{f'β<{a.gate} 비율':>12s}  판정")
    worst = 0.0
    for lo, hi in WINDOWS:
        bs = []
        for _ in range(a.trials):
            t, y = synth(a.n_li, a.n_frames, a.dt_ps, a.D, rng,
                         cage_A2=a.cage_A2, tau_ps=a.tau_ps)
            b = beta_of(t, y, lo, hi)
            if b is not None:
                bs.append(b)
        if not bs:
            continue
        bs = np.array(bs)
        frac = float((bs < a.gate).mean())
        worst = max(worst, frac)
        verdict = ("✓ 게이트 건전 (거짓탈락 <5%)" if frac < 0.05 else
                   "⚠ 거짓탈락 무시 못 함" if frac < 0.20 else
                   "⛔ **게이트가 잡음을 재고 있다**")
        print(f"{f'{lo:g}–{hi:g}':>12s} {np.median(bs):9.3f} "
              f"{f'{np.percentile(bs, 5):.2f}–{np.percentile(bs, 95):.2f}':>16s} "
              f"{frac * 100:11.1f}%  {verdict}")

    print()
    if worst >= 0.20:
        print(f"⛔ **결론: β<{a.gate} 를 '케이지'로 읽으면 안 된다.** 케이지가 0 인 계에서도 "
              f"최대 {worst * 100:.0f}% 가 탈락한다.")
        print("   → 탈락 사유를 β 단독으로 쓰지 말고 **창끝 MSD 와 같이** 볼 것. "
              "MSD 가 크면(수십 Å²) 확산은 이미 일어난 것이고 β 는 추정기 잡음이다.")
        print("   → 근본 처방은 시간 연장이 아니라 **표본 늘리기**(다중 시간원점 or 셀 확대)다.")
    elif worst >= 0.05:
        print(f"⚠ 거짓탈락률 최대 {worst * 100:.0f}% — 경계선 β(0.75–0.80)는 단독 판정 근거로 "
              f"약하다. MSD 크기를 같이 볼 것.")
    else:
        print(f"✓ 거짓탈락률 최대 {worst * 100:.1f}% — 이 표본 크기에서 β 게이트는 건전하다. "
              f"실측 β<{a.gate} 는 진짜 케이지로 읽어도 된다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
