#!/usr/bin/env python3
"""msd_diffusive_check.py — MSD 가 **진짜 확산 영역**인지 판정한다 (인용 게이트).

왜 필요한가
  D 는 MSD 를 `fit_window_ps` 에서 직선 맞춤해 얻는데, 그 창이 확산 영역이 아니면
  **케이지 진동·드리프트를 확산으로 오독**한다. 실측 두 건:
    · comp2 disorder d=0.5 — 600 K D 가 1.4~2.3e-05 cm²/s (comp1 의 1000 K 값과 동급),
      D(1000)/D(600) 가 1.98~5.6 밖에 안 됨 (0.276 eV 면 8.5 배 기대)
    · comp1 seed3 — D(600) 1.36e-06 ≈ D(800) 1.37e-06 (비 1.007). 물리적으로 불가능.
  둘 다 "Ea 를 냈다"까지는 갔지만 **그 Ea 를 인용하면 안 되는** 상태였다.

판정
  log-log 기울기 β = d(log MSD)/d(log t) 를 창 안에서 잰다.
    β ≈ 1.0        확산 (Fickian) — 인용 가능
    β < 0.8        아직 케이지/천이 — **인용 금지**, 창을 늦추거나 prod 를 늘려라
    β > 1.2        드리프트/탄도 — 질량중심 표류 의심

⚠ β 만으로는 부족하다. **MSD 절대 크기**도 본다: 창 끝의 MSD 가 이웃 Li–Li 거리²
  (~3 Å² 정도) 보다 작으면 이온이 자기 자리를 못 벗어난 것이라 β 가 1 이어도 통계가 없다.

  python3 tools/ionic/msd_diffusive_check.py --glob '~/work/runs/comp2_disorder_relaxed/d*_cfg*/T*/msd.json'
  python3 tools/ionic/msd_diffusive_check.py --glob '~/work/runs/comp1_seeds/s*/d*_cfg*/T*/msd.json'
"""
import argparse
import glob as _glob
import json
import math
import os

BETA_OK = (0.80, 1.20)
MSD_MIN_A2 = 3.0            # 창 끝 MSD 하한 — 이보다 작으면 자리 이탈을 못 한 것


def loglog_slope(t, y, lo, hi):
    """[lo,hi] ps 구간의 log-log 기울기. 점이 3개 미만이면 None."""
    pts = [(math.log(a), math.log(b)) for a, b in zip(t, y)
           if lo <= a <= hi and a > 0 and b > 0]
    if len(pts) < 3:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    return (n * sxy - sx * sy) / den if abs(den) > 1e-30 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True, help="msd.json 글롭 (따옴표로 감쌀 것)")
    ap.add_argument("--window", type=float, nargs=2, default=[2.0, 50.0],
                    help="D 를 맞춘 창 (기본 2 50 — 캠페인 규약)")
    ap.add_argument("--average", action="store_true",
                    help="같은 온도의 파일들 **MSD 곡선을 먼저 평균**한 뒤 β 를 잰다. "
                         "독립 시드/config 는 같은 계의 다른 초기속도라 MSD 앙상블 평균이 "
                         "정당하다 — 홉이 적어 자기평균이 안 되는 궤적을 **재계산 없이** "
                         "살리는 유일한 수단.")
    ap.add_argument("--scan", action="store_true",
                    help="여러 창에서 β 를 재서 **어디서부터 확산이 되는지** 찾는다. "
                         "케이지 판정이 나왔을 때 '재계산 없이 구제 가능한가'를 가른다.")
    a = ap.parse_args()

    files = sorted(_glob.glob(os.path.expanduser(a.glob)))
    if not files:
        raise SystemExit(f"파일 없음: {a.glob}")
    lo, hi = a.window

    # ── 온도별 MSD 앙상블 평균 ────────────────────────────────────────────
    if a.average:
        # ⚠ 시간 격자가 같아야 평균이 의미 있다. 다르면 짧은 쪽에 맞춰 자른다.
        byT = {}
        for f in files:
            d = json.load(open(f))
            t, y = d.get("times_ps"), d.get("msd_Li_A2")
            if not t or not y:
                continue
            byT.setdefault(int(d.get("T_K", 0)), []).append((t, y, f))
        print(f"온도별 MSD 앙상블 평균 (창 {lo}–{hi} ps)")
        print(f"{'T (K)':>7s} {'n_runs':>7s} {'beta':>6s} {'MSD@hi':>9s}  판정")
        for T in sorted(byT):
            runs = byT[T]
            n = min(len(t) for t, _, _ in runs)
            tt = runs[0][0][:n]
            yy = [sum(r[1][i] for r in runs) / len(runs) for i in range(n)]
            b = loglog_slope(tt, yy, lo, hi)
            m = max((v for u, v in zip(tt, yy) if u <= hi), default=float("nan"))
            ok = b is not None and BETA_OK[0] <= b <= BETA_OK[1] and m >= MSD_MIN_A2
            print(f"{T:7d} {len(runs):7d} {b if b is None else round(b,2):>6} "
                  f"{m:9.1f}  {'✓ 확산' if ok else '⛔ 여전히 비확산'}")
        print("  ⚠ 평균이 살아나도 **개별 런은 여전히 못 쓴다** — config 산포를 평균 뒤에")
        print("    다시 낼 수 없으므로, 오차막대는 다른 방법(블록 평균 등)으로 내야 한다.")
        print()
    print(f"창 {lo}–{hi} ps · β=1 확산 · β<{BETA_OK[0]} 케이지 · "
          f"창끝 MSD < {MSD_MIN_A2} Å² 면 통계 부족")
    print(f"{'case':34s} {'D(cm2/s)':>10s} {'beta':>6s} {'MSD@hi':>8s}  판정")
    bad = []
    for f in files:
        d = json.load(open(f))
        t, y = d.get("times_ps"), d.get("msd_Li_A2")
        D = d.get("D_Li_cm2_s")
        tag = "/".join(f.split(os.sep)[-3:-1])
        if not t or not y:
            print(f"{tag:34s} {D:10.3e} {'—':>6s} {'—':>8s}  ⚠ MSD 배열 없음")
            continue
        b = loglog_slope(t, y, lo, hi)
        msd_hi = max((v for u, v in zip(t, y) if u <= hi), default=float("nan"))
        marks = []
        if b is None:
            marks.append("β 못 잼")
        elif b < BETA_OK[0]:
            marks.append(f"⛔ 케이지(β={b:.2f})")
        elif b > BETA_OK[1]:
            marks.append(f"⚠ 드리프트(β={b:.2f})")
        if msd_hi < MSD_MIN_A2:
            marks.append(f"⛔ 통계부족(MSD {msd_hi:.1f} Å²)")
        verdict = " · ".join(marks) if marks else "✓ 확산"
        if marks:
            bad.append((tag, verdict))
        _f = lambda v, sp: "—".rjust(len(sp.format(0))) if v is None or v != v else sp.format(v)
        print(f"{tag:34s} {_f(D, '{:10.3e}')} {_f(b, '{:6.2f}')} "
              f"{_f(msd_hi, '{:8.1f}')}  {verdict}")

    # ── 창 스캔: 재계산 없이 구제 가능한가 ────────────────────────────────
    if a.scan:
        # ⚠ MSD 는 짧은 시간에서 원래 sub-diffusive 다(케이지 안 진동). 늦은 창에서
        #   β 가 1 로 올라가면 **MD 를 다시 돌 필요 없이 창만 바꾸면 된다.**
        #   끝까지 β<1 이면 그건 궤적이 짧은 것이라 prod 연장 말고는 답이 없다.
        # ⚠⚠ **창 목록이 궤적 길이를 따라가야 한다 (2026-08-03).** 이 목록은 200 ps prod
        #   기준으로 굳어 있어서 최대 창이 100-200 ps 였다. 1600 ps 런이 들어와도 뒤쪽
        #   1400 ps 를 **아예 안 본다** — 연장한 이유가 늦은 창에서 확산 영역을 보려는
        #   것인데 그 창이 목록에 없으면 3일치 GPU 가 그냥 버려진다.
        #   → 궤적 tmax 에 맞춰 늦은 창을 자동으로 덧붙인다 (짧은 창은 대조용으로 유지).
        tmax_all = 0.0
        for f in files:
            try:
                tt = json.load(open(f)).get("times_ps") or []
                tmax_all = max(tmax_all, max(tt) if tt else 0.0)
            except Exception:
                pass
        WINS = [(2, 50), (10, 50), (25, 100), (50, 150), (50, 200), (100, 200)]
        for frac_lo, frac_hi in ((0.10, 0.50), (0.25, 0.75), (0.50, 1.00)):
            lo, hi = round(tmax_all * frac_lo), round(tmax_all * frac_hi)
            if hi > 200 and hi - lo >= 50 and (lo, hi) not in WINS:
                WINS.append((lo, hi))
        if tmax_all > 250:
            print(f"(궤적 tmax {tmax_all:.0f} ps → 늦은 창 자동 추가: "
                  f"{', '.join(f'{l}-{h}' for l, h in WINS[6:])})")
        print("\n창 스캔 — β 가 1 에 가까워지는 창이 있으면 재계산 없이 구제된다")
        head = " ".join(f"{lo}-{hi}".rjust(8) for lo, hi in WINS)
        print(f"{'case':34s} {head}   tmax")
        for f in files:
            d = json.load(open(f))
            t, y = d.get("times_ps"), d.get("msd_Li_A2")
            if not t or not y:
                continue
            tag = "/".join(f.split(os.sep)[-3:-1])
            cells = []
            for lo, hi in WINS:
                b = loglog_slope(t, y, lo, hi)
                cells.append("   —" .rjust(8) if b is None else f"{b:8.2f}")
            print(f"{tag:34s} {' '.join(cells)}   {max(t):.0f}")
        print("  ⚠ 창을 늦추면 통계 점수는 줄어든다 — β 가 1 이어도 창 안 데이터가")
        print("    너무 적으면(점 3개 미만) '—' 로 나온다. tmax 가 창보다 작아도 마찬가지.")

    print()
    if bad:
        print(f"⛔ **{len(bad)}/{len(files)} 개가 확산 영역이 아니다 — 그 D 와 그걸 쓴 Ea 는 인용 금지.**")
        for tag, v in bad:
            print(f"   {tag}: {v}")
        print("   처방: ① 창을 늦춘다(예: 10–50 ps) ② prod 를 늘린다 ③ 그 온도를 Arrhenius 에서 뺀다")
        print("   ⚠ ③ 은 캠페인 규약(600/800/1000 3점)의 예외다 — 근거를 db 에 남길 것.")
    else:
        print(f"✅ {len(files)}개 전부 확산 영역 — D/Ea 인용 가능.")


if __name__ == "__main__":
    main()
