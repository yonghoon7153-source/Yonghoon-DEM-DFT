#!/usr/bin/env python3
"""msd_refit_window.py — 이미 돈 MD 를 **재계산 없이** 다른 적합 창으로 다시 맞춘다.

왜 만들었나 (1저자 질문 2026-08-03: "fit 을 2-50 까지만 하는 게 맞아?")
  msd.json 은 `D_Li_cm2_s` 스칼라뿐 아니라 **times_ps / msd_Li_A2 시계열 전체**를 담고 있다.
  즉 `--fit_window_ps` 는 **저장된 D 값만** 정하고, 창을 바꾸는 데 MD 재실행이 필요 없다.
  → 54 런(6점 아레니우스)을 창 결정 때문에 붙잡아 둘 이유가 없다. 먼저 돌리고 나중에 재적합한다.

이 도구가 하는 일
  1) 각 msd.json 을 여러 창에서 재적합 → 기울기·beta·D
  2) 창을 **beta 로 고르는** 정책(--policy beta)과 고정 창(--policy fixed)을 비교
  3) 같은 계 안에서 온도별 D 를 모아 **Ea 가 창에 따라 얼마나 흔들리는지** 계산

⚠⚠ **창을 바꾸면 Ea 가 바뀐다 — 그게 이 도구의 요점이다.** 200 ps 실데이터에서
  LPSOCl 은 2-50 창 Ea 0.339 eV 인데 20-200 창에서 0.097 eV 가 나온다(-242 meV).
  우리가 주장하는 도핑 효과(LPSOCl 이 modelc 보다 +90 meV)보다 **창 효과가 더 크다**.
  따라서 창은 "관례" 가 아니라 **명시적으로 고르고 근거를 적어야 하는 선택**이다.

⚠⚠ **창을 늦춘다고 항상 좋아지는 게 아니다.** 같은 데이터에서 LPSOCl 은
  800 K 후반 기울기(0.53-0.79)가 **600 K 후반 기울기(0.92-1.11)보다 작다** — 물리적으로 불가능.
  아레니우스 R^2 가 0.13 까지 떨어진다. 후반 창이 '진실' 이 아니라 **통계가 없는** 것이다.
  근본 원인은 창이 아니라 **단일 시간원점 MSD** 다 (아래 --mto 참조).

  python3 tools/ionic/msd_refit_window.py --glob '~/work/runs/lpsocl_md/ladder/**/msd.json'
  python3 tools/ionic/msd_refit_window.py --glob '...' --policy beta --csv db/properties/msd_window_scan.csv
"""
import argparse
import glob as _glob
import json
import math
import os
import re

BETA_OK = (0.80, 1.20)
MSD_MIN_A2 = 3.0            # msd_diffusive_check.py 와 같은 게이트
CAMPAIGN_WIN = (2.0, 50.0)  # 캠페인 규약 창 (CLAUDE.md)
KB_EV = 8.617333262e-5


# ── 기본 통계 (numpy 없이 — 서버마다 env 가 달라서 의존성을 줄인다) ──────────
def _fit(xs, ys):
    """최소제곱 1차. (slope, intercept, R^2). 점 3개 미만이면 None."""
    n = len(xs)
    if n < 3:
        return None
    sx = sum(xs); sy = sum(ys)
    sxx = sum(v * v for v in xs); sxy = sum(a * b for a, b in zip(xs, ys))
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    m = (n * sxy - sx * sy) / den
    b = (sy - m * sx) / n
    ybar = sy / n
    ss = sum((b + m * x - y) ** 2 for x, y in zip(xs, ys))
    st = sum((y - ybar) ** 2 for y in ys)
    return m, b, (1.0 - ss / st if st > 1e-30 else float("nan"))


def slope_beta(t, y, lo, hi):
    """[lo,hi] ps 에서 (선형 기울기 A^2/ps, log-log 기울기 beta, 창끝 MSD).

    ⚠ beta 는 **시간 범위가 좁으면 못 믿는다.** 100-200 ps 는 2배 구간(0.3 decade)이라
      beta 의 표본오차가 크다. 그래서 아래 pick_window 는 최소 span 을 요구한다.
    """
    lin = [(a, b) for a, b in zip(t, y) if lo <= a <= hi]
    if len(lin) < 3:
        return None, None, None
    f = _fit([p[0] for p in lin], [p[1] for p in lin])
    lg = [(math.log(a), math.log(b)) for a, b in lin if a > 0 and b > 0]
    g = _fit([p[0] for p in lg], [p[1] for p in lg]) if len(lg) >= 3 else None
    return (f[0] if f else None), (g[0] if g else None), lin[-1][1]


def pick_window(t, y, t_hi, min_span, beta_ok, lo_grid):
    """beta 로 창 **시작점**을 고른다. 끝점은 t_hi 고정(궤적 전체 또는 지정값).

    정책: "남은 궤적 전체에 대한 log-log 기울기가 0.8-1.2 안에 들어오는
          **가장 이른 시각**부터 적합한다."
    자유 파라미터가 하나(beta 범위)뿐이고, 원고에 한 문장으로 적을 수 있다.

    ⚠ 못 고르면 None 을 준다 — **아무 창이나 골라 주지 않는다.** 확산 영역이 없다는
      판정 자체가 결과다(comp1 600 K 사례).
    """
    for lo in lo_grid:
        if t_hi / max(lo, 1e-9) < min_span:
            break
        s, b, mend = slope_beta(t, y, lo, t_hi)
        if b is None or s is None:
            continue
        if beta_ok[0] <= b <= beta_ok[1] and s > 0:
            return lo, s, b, mend
    return None


def sysname(path):
    """경로에서 계 이름을 뽑는다. 못 뽑으면 부모 디렉토리 이름."""
    p = os.path.normpath(path)
    for key in ("lpsocl", "modelc", "b2o3", "comp1", "comp2", "lpscl"):
        if key in p.lower():
            return key
    return os.path.basename(os.path.dirname(os.path.dirname(p)))


def arrhenius(TD):
    """{T: D} → (Ea eV, R^2). 점 3개 미만이면 None."""
    pts = [(1.0 / T, math.log(D)) for T, D in sorted(TD.items()) if D and D > 0]
    if len(pts) < 3:
        return None
    f = _fit([p[0] for p in pts], [p[1] for p in pts])
    return (-f[0] * KB_EV, f[2]) if f else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="msd.json 글롭 (따옴표로 감쌀 것)")
    ap.add_argument("--policy", choices=["fixed", "beta", "both"], default="both")
    ap.add_argument("--fixed", type=float, nargs=2, default=list(CAMPAIGN_WIN),
                    help="고정 창 [ps] (기본 2 50 — 캠페인 규약)")
    ap.add_argument("--hi", default="traj",
                    help="beta 정책의 창 끝 [ps]. traj = 궤적 끝 (기본)")
    ap.add_argument("--beta", type=float, nargs=2, default=list(BETA_OK))
    ap.add_argument("--min_span", type=float, default=4.0,
                    help="창의 hi/lo 최소 비율. beta 를 좁은 구간에서 재면 못 믿는다(기본 4배).")
    ap.add_argument("--mto", action="store_true",
                    help="msd.json 에 msd_Li_A2_mto(다중 시간원점)가 있으면 그걸 쓴다")
    ap.add_argument("--csv", help="Origin-ready CSV 로도 저장")
    a = ap.parse_args()

    files = sorted(_glob.glob(os.path.expanduser(a.glob), recursive=True))
    if not files:
        raise SystemExit(f"⛔ 파일 없음: {a.glob}")

    key = "msd_Li_A2_mto" if a.mto else "msd_Li_A2"
    tkey = "times_ps_mto" if a.mto else "times_ps"
    lo_grid = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100]

    rows, byfixed, bypick = [], {}, {}
    print(f"창 재적합 — {len(files)}개 msd.json · MSD 종류 = "
          f"{'다중 시간원점(MTO)' if a.mto else '단일 시간원점'}")
    print(f"{'계':<9}{'T':>6}{'traj':>7} │{'고정창':>10}{'slope':>8}{'beta':>6}{'D':>11}"
          f" │{'beta선택창':>12}{'slope':>8}{'beta':>6}{'D':>11}{'비':>7}")

    for f in files:
        try:
            d = json.load(open(f))
        except Exception as e:
            print(f"  ⛔ {f} 읽기 실패: {e}")
            continue
        t, y = d.get(tkey), d.get(key)
        if not t or not y:
            print(f"  ⛔ {os.path.relpath(f)} — {key} 없음"
                  + ("  (--mto 는 새 런에만 있다)" if a.mto else ""))
            continue
        T = float(d.get("T_K", 0))
        sysn = sysname(f)
        seed = (re.findall(r"[/_]s(\d+)", f) or ["?"])[0]
        tmax = max(t)
        t_hi = tmax if a.hi == "traj" else float(a.hi)

        s0, b0, m0 = slope_beta(t, y, a.fixed[0], a.fixed[1])
        D0 = s0 / 6.0 * 1e-4 if s0 and s0 > 0 else None

        pk = pick_window(t, y, t_hi, a.min_span, tuple(a.beta), lo_grid)
        if pk:
            lo1, s1, b1, m1 = pk
            D1 = s1 / 6.0 * 1e-4
            wtxt, ratio = f"{lo1:g}-{t_hi:g}", (s1 / s0 if s0 else float("nan"))
        else:
            lo1 = s1 = b1 = m1 = D1 = None
            wtxt, ratio = "없음", float("nan")

        # ⚠ None/NaN 이 하나라도 있으면 서식이 죽는다. 판정 도구가 죽으면 그 사례의
        #   판정이 아예 안 남으므로, 값이 없을 때는 '-' 로 채우고 줄은 반드시 찍는다.
        def num(v, w, p):
            return f"{v:>{w}.{p}f}" if isinstance(v, (int, float)) and v == v else "-".rjust(w)
        sci = lambda v: f"{v:>11.3e}" if v else "-".rjust(11)
        wfix = f"{a.fixed[0]:g}-{a.fixed[1]:g}"
        rtxt = f"{ratio:>6.2f}x" if ratio == ratio else "-".rjust(7)
        print(f"{sysn:<9}{T:>6.0f}{tmax:>6.0f}p │{wfix:>10}"
              f"{num(s0, 8, 3)}{num(b0, 6, 2)}{sci(D0)} │{wtxt:>12}"
              f"{num(s1, 8, 3)}{num(b1, 6, 2)}{sci(D1)}{rtxt}")

        gate = ("확산" if (b0 and BETA_OK[0] <= b0 <= BETA_OK[1] and m0 and m0 >= MSD_MIN_A2)
                else "게이트탈락")
        rows.append({"file": os.path.relpath(f), "system": sysn, "T_K": int(T), "seed": seed,
                     "traj_ps": f"{tmax:.0f}",
                     "win_fixed": f"{a.fixed[0]:g}-{a.fixed[1]:g}",
                     "slope_fixed_A2_ps": f"{s0:.4f}" if s0 else "",
                     "beta_fixed": f"{b0:.3f}" if b0 else "",
                     "D_fixed_cm2_s": f"{D0:.4e}" if D0 else "",
                     "gate_fixed": gate,
                     "win_beta": wtxt,
                     "slope_beta_A2_ps": f"{s1:.4f}" if s1 else "",
                     "beta_beta": f"{b1:.3f}" if b1 else "",
                     "D_beta_cm2_s": f"{D1:.4e}" if D1 else "",
                     "ratio_beta_over_fixed": f"{ratio:.3f}" if ratio == ratio else ""})
        if D0:
            byfixed.setdefault(sysn, {}).setdefault(int(T), []).append(D0)
        if D1:
            bypick.setdefault(sysn, {}).setdefault(int(T), []).append(D1)

    # ── 창이 Ea 를 얼마나 흔드는가 ────────────────────────────────────────
    def mean(v):
        return sum(v) / len(v)

    print("\n" + "─" * 86)
    print("창이 Ea 를 얼마나 바꾸나 (같은 계의 온도별 D 를 시드평균한 뒤 아레니우스)")
    print(f"{'계':<10}{'창':>16}{'n_T':>5}{'Ea (eV)':>10}{'R^2':>8}   {'vs 고정창':>10}")
    for sysn in sorted(set(list(byfixed) + list(bypick))):
        base = None
        for tag, src in (("고정 " + f"{a.fixed[0]:g}-{a.fixed[1]:g}", byfixed),
                         ("beta 선택", bypick)):
            TD = {T: mean(v) for T, v in src.get(sysn, {}).items()}
            r = arrhenius(TD)
            if not r:
                print(f"{sysn:<10}{tag:>16}{len(TD):>5}{'점 3개 미만':>19}")
                continue
            Ea, r2 = r
            if base is None:
                base = Ea
            dd = (Ea - base) * 1000
            flag = "  ⚠ R^2 낮음 — 아레니우스가 안 선다" if r2 < 0.9 else ""
            print(f"{sysn:<10}{tag:>16}{len(TD):>5}{Ea:>10.3f}{r2:>8.3f}   "
                  f"{dd:>+7.0f} meV{flag}")

    print("\n⚠ 위 Ea 는 **이 글롭에 들어온 런만** 쓴 값이다. 헤드라인 Ea 는 여전히")
    print("  멀티시드 *_md_arrhenius.json 이 출처다. 이 표는 '창 민감도' 를 보는 용도다.")
    print("⚠ beta 선택창이 '없음' 인 점은 **어떤 창에서도 확산 영역이 아니다** 는 뜻이다.")
    print("  그런 점은 아레니우스에서 빼야 한다 — 창을 바꿔 구제하려 들면 안 된다.")

    if a.csv:
        import csv as _csv
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as fh:
            fh.write("# MSD fit-window sensitivity. slope in A^2/ps, D = slope/6 [cm2/s].\n")
            fh.write("# beta = d log MSD / d log t over the same window (0.8-1.2 = Fickian).\n")
            fh.write("# win_beta: earliest start whose beta over [start, traj_end] is Fickian; "
                     "'none' = no diffusive window exists.\n")
            w = _csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        print(f"\n→ {a.csv}")


if __name__ == "__main__":
    main()
