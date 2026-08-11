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
    a = ap.parse_args()

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
