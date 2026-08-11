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


def lin_fit(t, y, lo, hi):
    """[lo,hi] 에서 MSD = c + m·t 를 자유 절편으로 맞춘다. (m, c, R²) 또는 None.

    ★★ 2026-08-11 — **이 절편이 β 게이트의 정체다.**
      고체 MSD 는 어느 계든 `MSD(t) = C + 6Dt` 꼴이다 (C = 케이지 진폭 + ballistic 잔재).
      C > 0 이면 log-log 기울기 β 는 **자동으로 1 아래**로 내려간다 — 확산이 아니어서가
      아니라 절편이 있어서다. 실측(db/properties/msd_3sys_200ps_origin.csv):

        계·온도              절편 c    c/MSD@50    β      비고
        B2O3 600 K           1.704 Å²   5.1 %     0.806
        LPSCl1.6 600 K       2.336      7.6 %     0.868
        **LPSOCl 600 K**     4.035     18.2 %     0.615   ← 게이트 탈락
        LPSCl1.6 1000 K      1.952      1.4 %     0.924

      β 가 c/MSD@50 에 거의 단조로 붙어 있고, **탈락한 곡선들의 직선 적합 R² 가
      0.971–0.996** 이다 — MSD 가 직선이 아니어서 탈락한 게 아니다.
      β=0.76 을 만드는 데 필요한 절편은 항상 창끝 MSD 의 ~7.4 % 다(크기 무관).

      ⇒ **게이트 β<0.8 은 사실상 "절편이 창끝 MSD 의 ~6 % 를 넘는가" 를 재고 있다.**
        그건 물리 판정이 아니라 **암묵적 표본 크기 요구**다. 그리고 D 는 이미
        **자유 절편 직선 맞춤**의 기울기에서 나오므로 절편에 영향받지 않는다.

      판별법: 창을 뒤로 밀면서 절편을 본다.
        · 절편이 **상수**·기울기 불변·β 가 1 로 올라감 → 케이지 절편. **D 인용 가능**
        · 절편이 **커지고** 기울기가 떨어지며 β 가 모든 창에서 그대로 → 진짜 sub-diffusion
    """
    pts = [(a, b) for a, b in zip(t, y) if lo <= a <= hi]
    if len(pts) < 3:
        return None
    n = len(pts)
    sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    den = n * sxx - sx * sx
    if abs(den) < 1e-30:
        return None
    m = (n * sxy - sx * sy) / den
    c = (sy - m * sx) / n
    ybar = sy / n
    ss = sum((c + m * x - yy) ** 2 for x, yy in pts)
    st = sum((yy - ybar) ** 2 for _, yy in pts)
    return m, c, (1.0 - ss / st if st > 1e-30 else float("nan"))


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

    # ⚠⚠ 2026-08-11 — `recursive=True` 가 빠져 있었다. 그러면 `**` 가 재귀가 아니라
    #   **한 단계**로만 동작해서, 캠페인이 실제로 쓰는 경로
    #   `<계>/T700_s2/d0.00_cfg0/T700/msd.json` (두 단계 깊이)를 하나도 못 찾는다.
    #   run_arrhenius_6pt.sh 가 '다음 단계'로 찍어 주는 명령이 바로 그 글롭이었고,
    #   msd_refit_window.py 는 recursive=True 라 같은 글롭으로 21개를 찾았다 —
    #   **도구마다 다른 답**이 나온 게 이 한 줄이다.
    files = sorted(_glob.glob(os.path.expanduser(a.glob), recursive=True))
    if not files:
        # 0개를 '파일 없음'으로만 끝내면 글롭 버그와 정말로 안 돈 것을 구분 못 한다.
        loose = sorted(_glob.glob(os.path.expanduser(a.glob).split("**")[0] + "**/msd.json",
                                  recursive=True)) if "**" in a.glob else []
        msg = [f"파일 없음: {a.glob}"]
        if loose:
            msg.append(f"⚠ 같은 뿌리 아래 msd.json 은 {len(loose)}개 있다 — 글롭 패턴을 볼 것:")
            msg += [f"    {p}" for p in loose[:3]]
        raise SystemExit("\n".join(msg))
    lo, hi = a.window

    def case_label(path, width=34):
        """⚠ 2026-08-11 — 옛 라벨은 `[-3:-1]` 이라 전부 `d0.00_cfg0/T700` 로 찍혔다.
        어느 계(modelc/lpsocl/b2o3)의 어느 시드인지가 **표에서 사라져** 탈락 8건이
        어디 것인지 읽을 수가 없었다. 정보 없는 조각(d*_cfg*, 마지막 T* 중복)을 버린다."""
        import re as _re
        parts = path.split(os.sep)[:-1]                     # msd.json 제외
        drop = _re.compile(r"^d\d+\.\d+_cfg\d+$")
        keep = [p for p in parts[-4:] if not drop.match(p)]
        if len(keep) >= 2 and keep[-1].lstrip("T").isdigit() \
                and keep[-1].lstrip("T") in keep[-2]:
            keep = keep[:-1]                                # T700_s2/T700 → T700_s2
        lab = "/".join(keep)
        return lab[-width:] if len(lab) > width else lab

    # ── 계·온도별 MSD 앙상블 평균 ─────────────────────────────────────────
    avg_curves = {}
    if a.average:
        # ⛔⛔ 2026-08-11 — 옛 코드는 **온도로만** 묶었다(`byT[T_K]`). 캠페인 글롭이
        #   세 계를 한꺼번에 덮으므로 T700 에 modelc·lpsocl·b2o3 가 **같이 평균**됐다.
        #   서로 다른 물질의 MSD 곡선을 평균한 것이라 그 값은 아무 뜻이 없다.
        #   (한 계씩 글롭할 때만 우연히 맞았다.) → (계, T) 로 묶는다.
        # ⚠ 시간 격자가 같아야 평균이 의미 있다. 다르면 짧은 쪽에 맞춰 자른다.
        byST = {}
        for f in files:
            d = json.load(open(f))
            t, y = d.get("times_ps"), d.get("msd_Li_A2")
            if not t or not y:
                continue
            lab = case_label(f)
            sysname = lab.split("/")[0] if "/" in lab else lab   # 계 이름
            byST.setdefault((sysname, int(d.get("T_K", 0))), []).append((t, y, f))
        print(f"계·온도별 MSD 앙상블 평균 (창 {lo}–{hi} ps)")
        print(f"{'계':12s} {'T (K)':>7s} {'n_runs':>7s} {'beta':>6s} {'c [Å²]':>8s} "
              f"{'MSD@hi':>9s}  판정")
        for key in sorted(byST):
            sysname, T = key
            runs = byST[key]
            n = min(len(t) for t, _, _ in runs)
            tt = runs[0][0][:n]
            yy = [sum(r[1][i] for r in runs) / len(runs) for i in range(n)]
            avg_curves[f"{sysname}/T{T}_AVG{len(runs)}"] = (tt, yy)
            b = loglog_slope(tt, yy, lo, hi)
            lf = lin_fit(tt, yy, lo, hi)
            m = max((v for u, v in zip(tt, yy) if u <= hi), default=float("nan"))
            ok = b is not None and BETA_OK[0] <= b <= BETA_OK[1] and m >= MSD_MIN_A2
            print(f"{sysname:12s} {T:7d} {len(runs):7d} "
                  f"{b if b is None else round(b, 2):>6} "
                  + (f"{lf[1]:8.2f}" if lf else f"{'—':>8s}")
                  + f" {m:9.1f}  {'✓ 확산' if ok else '⛔ 여전히 비확산'}")
        print("  ⚠ 평균이 살아나도 **개별 런은 여전히 못 쓴다** — config 산포를 평균 뒤에")
        print("    다시 낼 수 없으므로, 오차막대는 다른 방법(블록 평균 등)으로 내야 한다.")
        print("  ★ --scan 을 같이 주면 **이 평균 곡선으로** 창 스캔을 돈다 — 늦은 창의")
        print("    통계가 √n 배 좋아져서 c 판별(케이지 vs sub-diffusion)이 실제로 가능해진다.")
        print()

    print(f"창 {lo}–{hi} ps · β=1 확산 · β<{BETA_OK[0]} 케이지 · "
          f"창끝 MSD < {MSD_MIN_A2} Å² 면 통계 부족")
    # ⚠⚠ β<0.8 을 곧바로 '케이지' 로 읽지 말 것 — **창끝 MSD 를 같이 본다.**
    #   2026-08-11 귀무분포 검정(tools/ionic/beta_null_test.py): 케이지가 0 인 이상
    #   브라운 운동을 Li 27개·200 ps 로 재면 창 2–50 에서 β = 1.01 (5–95% 0.86–1.14),
    #   0.8 미만이 **1.0%** 뿐이다. 즉 이 창의 β<0.8 은 표본 부족이 아니라 진짜다.
    #   반면 늦은 창(50–200)에서는 이상 계도 10%가 0.8 아래로 떨어진다 — 그 창의
    #   β 로 '구제' 판정을 하면 안 된다. 창마다 게이트의 신뢰도가 다르다.
    print(f"{'case':34s} {'D(cm2/s)':>10s} {'beta':>6s} {'MSD@hi':>8s}  판정")
    bad = []
    for f in files:
        d = json.load(open(f))
        t, y = d.get("times_ps"), d.get("msd_Li_A2")
        D = d.get("D_Li_cm2_s")
        tag = case_label(f)
        # ⚠ P1-6 — D 가 null 인 msd.json 하나만 있어도 옛 코드는 TypeError 로 죽어
        #   **전수 게이트가 통째로** 날아갔다 (MD 가 중간에 죽으면 실제로 생긴다).
        _f = (lambda v, sp: "—".rjust(len(sp.format(0)))
              if v is None or v != v else sp.format(v))
        if not t or not y:
            print(f"{tag:34s} {_f(D, '{:10.3e}')} {'—':>6s} {'—':>8s}  ⚠ MSD 배열 없음")
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
        # ★ --average 를 같이 주면 **평균 곡선**으로 돈다. 늦은 창이 살아나는 유일한
        #   공짜 수단이다 (개별 런은 lag 이 길어지면 유효 표본이 몇 개 안 남아 붕괴한다).
        scan_items = ([(k, t, y) for k, (t, y) in sorted(avg_curves.items())]
                      if avg_curves else None)
        print("\n창 스캔 — β 가 1 에 가까워지는 창이 있으면 재계산 없이 구제된다"
              + ("  **[시드 평균 곡선]**" if scan_items else ""))
        head = " ".join(f"{lo}-{hi}".rjust(8) for lo, hi in WINS)
        print(f"{'case':34s} {head}   tmax")
        print(f"{'':34s} " + " ".join(f"{'c=' + w:>8s}" for w in [])
              + "  (아래 줄: 각 창의 **절편 c [Å²]** — 상수면 케이지, 커지면 sub-diffusion)")
        def _spearman(v):
            vv = [x for x in v if x is not None]
            if len(vv) < 4:
                return 0.0
            import statistics as _st
            r = sorted(range(len(vv)), key=lambda i: vv[i])
            rank = [0.0] * len(vv)
            for pos, i in enumerate(r):
                rank[i] = float(pos)
            x = [float(i) for i in range(len(vv))]
            mx, mr = _st.mean(x), _st.mean(rank)
            num = sum((a - mx) * (b - mr) for a, b in zip(x, rank))
            den = (sum((a - mx) ** 2 for a in x) * sum((b - mr) ** 2 for b in rank)) ** 0.5
            return num / den if den > 1e-30 else 0.0

        trends = []
        for _it in (scan_items if scan_items else files):
            if scan_items:
                tag, t, y = _it
            else:
                d = json.load(open(_it))
                t, y = d.get("times_ps"), d.get("msd_Li_A2")
                if not t or not y:
                    continue
                tag = case_label(_it)
            cells, ints, slps = [], [], []
            for lo, hi in WINS:
                b = loglog_slope(t, y, lo, hi)
                cells.append("   —".rjust(8) if b is None else f"{b:8.2f}")
                lf = lin_fit(t, y, lo, hi)
                ints.append("   —".rjust(8) if lf is None else f"{lf[1]:8.2f}")
                slps.append("   —".rjust(8) if lf is None else f"{lf[0]:8.3f}")
            print(f"{tag:34s} {' '.join(cells)}   {max(t):.0f}")
            print(f"{'  └ c [Å²]':34s} {' '.join(ints)}")
            print(f"{'  └ m [Å²/ps]':34s} {' '.join(slps)}")
            # ── 추세 통계 (⚠⚠ 2026-08-11 재검토로 **자동 판정 → 진단 제안** 격하) ──
            #   MC 4000회 재검토 실측이 초판 규칙을 죽였다:
            #   · 중첩창 6개의 유효 표본은 n_eff ≈ 3.2 (corr(2-50,10-50)=+0.97) —
            #     Spearman 임계 ±0.6 은 iid 귀무에서도 한쪽당 9% 짜리다.
            #   · 오분류율 8~13%. 특히 'sub-diffusion' 판정은 **느린 전이(D 는 존재,
            #     창만 이르다) 대비 동전(47~50%)** — 처방이 정반대인 세 번째 모형을
            #     초판이 아예 몰랐다 (제거 vs 창 이동).
            #   · 초판 CAGE 분기는 c 를 아예 안 봤다 — 자기 문서("c 행이 가른다")와 모순.
            #     lpsocl/T600 이 c=−4.85(비물리)로 CAGE 를 받은 게 그 구멍이다.
            #   확정은 **MTO 곡선**으로만 한다. 아래는 제안이지 판정이 아니다.
            bv0 = [loglog_slope(t, y, lo, hi) for lo, hi in WINS]
            lfv = [lin_fit(t, y, lo, hi) for lo, hi in WINS]
            triples = [(w, b, lf) for w, b, lf in zip(WINS, bv0, lfv)
                       if b is not None and lf is not None]
            # 비물리 창(절편 c<0)은 추세에서 **버린다** — 순위 매길 대상이 아니다
            valid = [(w, b, lf) for w, b, lf in triples if lf[1] >= 0]
            n_drop = len(triples) - len(valid)
            if len(valid) >= 4:
                bv = [b for _w, b, _l in valid]
                mv = [l[0] for _w, _b, l in valid]
                cv = [l[1] for _w, _b, l in valid]
                tb, tm, tc = _spearman(bv), _spearman(mv), _spearman(cv)
                dm = 100.0 * (mv[-1] - mv[0]) / mv[0] if mv[0] else float("nan")
                # ★ 잔차 검정 — 재검토가 찾은 **실제로 갈리는 통계**. 각 창의 (c,m) 직선이
                #   함의하는 log-log 기울기 β_imp 와 관측 β 의 최대 편차. cage 면 전 창
                #   일치한다 (modelc/700 실측 |Δβ|≤0.025 · cage joint p=0.935).
                dbmax = 0.0
                for (lo_, hi_), b, (m_, c_, _r2) in valid:
                    xx = [x for x in t if lo_ <= x <= hi_ and x > 0]
                    yy = [c_ + m_ * x for x in xx]
                    bi = loglog_slope(xx, yy, lo_, hi_)
                    if bi is not None:
                        dbmax = max(dbmax, abs(b - bi))
                cage_like = tb > 0.6 and abs(dm) < 15 and dbmax <= 0.05
                sub_like = abs(tb) < 0.45 and tm < -0.6 and tc > 0.6
                if cage_like and not sub_like:
                    v = f"케이지 절편 **시사** (잔차 |Δβ|max {dbmax:.3f} ≤ 0.05)"
                elif sub_like and not cage_like:
                    v = "sub-diffusion **또는 느린 전이** — 요약값으로 구분 불가(동전)"
                else:
                    v = "판별 불가"
                trends.append((tag[:26], tb, dm, tm, tc, dbmax, n_drop, v))
        print("  ⚠ 창을 늦추면 통계 점수는 줄어든다 — β 가 1 이어도 창 안 데이터가")
        print("    너무 적으면(점 3개 미만) '—' 로 나온다. tmax 가 창보다 작아도 마찬가지.")
        # ★★ 2026-08-11 — 눈으로 읽지 말고 **추세로 판정**한다. 실측에서 이 판정이
        #   β 게이트와 **반대로** 나오는 사례가 나왔다 (아래 trend_verdict 주석 참조).
        if trends:
            print()
            print("  ═══ 추세 **제안** (자동 판정 아님 — 2026-08-11 재검토로 격하) ═══")
            print(f"  {'case':26s} {'β추세':>6s} {'m변화%':>7s} {'m추세':>6s} {'c추세':>6s} "
                  f"{'|Δβ|max':>8s} {'제외창':>5s}  제안")
            for tag, tb, dm, tm, tc, dbm, nd_, v in trends:
                print(f"  {tag:26s} {tb:+6.2f} {dm:+7.1f} {tm:+6.2f} {tc:+6.2f} "
                      f"{dbm:8.3f} {nd_:5d}  {v}")
            print()
            print("  ⚠ 이 표는 **제안**이다 — MC 재검토 실측: 오분류 8~13%, 중첩창 n_eff≈3.2,")
            print("    'sub-diffusion' 제안은 느린 전이(D 존재·창만 이르다) 대비 **동전**이다.")
            print("    느린 전이면 처방이 정반대다: 점 제거가 아니라 **창 이동/연장**.")
            print("  · 케이지 시사의 실근거는 Spearman 이 아니라 **잔차 검정**(|Δβ|max ≤ 0.05)이다.")
            print("  ⛔ 아레니우스에서 점을 넣고 빼는 결정은 이 표로 하지 않는다 —")
            print("    ① MTO 곡선으로 재판정 ② 그래도 애매하면 **세 계 같은 온도 집합** 유지가")
            print("    점 제거보다 우선한다 (비대칭 가감은 Ea 비교를 통째로 깨뜨린다).")
        print()
        print("  ★ c 행은 β 보다 정보가 많지만 **만능이 아니다** (2026-08-11 재검토 반영):")
        print("    · cage vs 멱함수는 가르지만, 멱함수 vs **느린 전이**는 요약값으로 못 가른다.")
        print("    · 단일 시간원점의 sd(c)는 iid-OLS 표준오차의 10~40배다 — c 의 창간 요동을")
        print("      과해석하지 말 것. 확정은 MTO 곡선으로.")
        print("     · c 가 창 따라 **거의 상수** + m 도 상수 + β 만 1 로 올라감")
        print("       → 케이지 절편이다. MSD = c + 6Dt 로 이미 직선이고 **D 는 인용 가능**하다.")
        print("         (D 는 자유 절편 맞춤의 **기울기**에서 나오므로 c 에 오염되지 않는다.)")
        print("     · c 가 창 따라 **커지고** m 이 **떨어지며** β 가 모든 창에서 그대로")
        print("       → 진짜 sub-diffusion 이다. 그때만 D 인용 금지가 맞다.")
        print("     ⚠ R² 로는 둘을 못 가른다 — 두 모형 다 0.99 를 넘는다. c 를 볼 것.")

    print()
    if bad:
        # ⚠⚠ 2026-08-11 문구 정정 — "확산 영역이 아니다" 는 **β 가 말할 수 있는 것보다 세다**.
        #   β<0.8 은 (a) 진짜 sub-diffusion 이거나 (b) MSD 절편이 창끝의 ~6% 를 넘은 것이다.
        #   둘을 가르는 건 --scan 의 **c 행**이지 β 값이 아니다.
        print(f"⚠ **{len(bad)}/{len(files)} 개가 선언한 창에서 Fickian scaling 을 입증하지 못했다.**")
        for tag, v in bad:
            print(f"   {tag}: {v}")
        print("   ⛔ 여기서 곧바로 'D 인용 금지' 로 가지 말 것 — **--scan 의 c 행을 먼저 본다**:")
        print("     · c 가 창 따라 상수면 케이지 절편이다. D 는 자유 절편 맞춤의 기울기라 무사하다.")
        print("     · c 가 창 따라 커지면 그때가 진짜 sub-diffusion 이고 D 인용 금지가 맞다.")
        print("   처방: ① --scan 으로 c 판별 ② 표본(이온 수·시간원점)을 늘린다 "
              "③ 그래도 c 가 크면 그 온도를 Arrhenius 에서 뺀다")
        print("   ⚠ ③ 은 캠페인 규약(600/800/1000 3점)의 예외다 — 근거를 db 에 남길 것.")
    else:
        print(f"✅ {len(files)}개 전부 확산 영역 — D/Ea 인용 가능.")


if __name__ == "__main__":
    main()
