#!/usr/bin/env python3
"""hops_per_ion.py — "이 온도에서 beta 가 설 수 있나"를 **홉 수**로 예측한다.

1저자 질문(2026-08-04): 저온에서 beta 가 낮게 나오는 게 현실적인가, 아니면 이상한가?

핵심 통찰 — **beta 는 시간이 아니라 홉 수를 잰다.**
  이온당 홉 수  n_hop = MSD / d_hop^2 = 6 D t / d_hop^2
  (d_hop = 이웃 Li 자리 간격 ~3 A. argyrodite 케이지 내/간 도약의 대표 길이)

  n_hop >= 10   확산 통계 충분  (beta ~ 1 기대)
  3 <= n_hop <10 경계          (beta 가 시드마다 흔들린다)
  n_hop < 3     홉 부족        (beta 가 낮게 나오는 게 **정상** — 측정 실패지 물리 아님)

⚠⚠ **이 예측이 우리 v2 게이트 결과를 그대로 맞춘다 (2026-08-04 실측 대조).**
  600 K · 200 ps 에서 n_hop = modelc 13.9 / b2o3 13.9 / **LPSOCl 8.4**
  실측 beta   =            0.87 ✓      0.81 ✓        **0.61 ⛔**
  → LPSOCl 600 K 탈락은 사고가 아니라 **예측 가능했던 통계 부족**이다.
    (LPSOCl 은 Ea 가 높아 같은 온도에서 D 가 작다 → 같은 200 ps 에 홉이 40% 적다)

⚠ 2026-09-11 정정 — 이건 **유효(독립) 홉 수** f·n 이지 상한이 아니다. 되돌아오는 홉이 있으면 같은 MSD 를
  내는 데 더 많은 이벤트가 필요하다 → MSD/d² 는 이벤트 수의 **하한**이다 (실측 f ≈ 0.7,
  db/properties/lpsocl_box331_c2b_hops_2026_09_11.json). '통계 충분' 판정에 맞는 양은 이 유효 홉 수라
  경계선 N_OK/N_EDGE 는 그대로 둔다.
  ⛔ 2026-09-07 정정 — 옛 판은 그 근거로 **"Haven 비 H_R 0.3–0.7 < 1 (litdb dyre2004)"**
    을 인용했다. 그 범위는 **문헌 소환값이고 우리 것이 아니며**, li_transport.json 이
    그것으로 우리 σ 를 되재는 것을 명시적으로 금지했다. 우리 궤적에서 직접 잰 값은
    **H_R = 0.84 ± 0.06** (db/properties/haven_ratio_measured_2026_09_07.json ·
    6 계온도 · b2o3 1200 K 제외). 그 파일은 `citable: false` — **방향 판정용**이라
    이 도구의 경계선을 그 숫자로 되재지 않는다. 상관운동이 있다는 방향만 살아 있고,
    "0.3–0.7 만큼 보수적으로" 라는 **크기 주장은 철회**다.
  (같은 날 부호도 뒤집혔다: H_R ≡ D*/D_σ 이므로 σ_NE = H_R·σ_true — H_R<1 이면
   NE 는 **과소**다. run_md_sigma.py 의 '나누기 2 = 상한' 지시가 그 오류였다.)

  python3 tools/ionic/hops_per_ion.py
  python3 tools/ionic/hops_per_ion.py --prod_ps 1600 --csv db/properties/hops_per_ion.csv

⛔ 이 도구가 못 하는 것
  · 궤적을 안 읽는다. 위 SYS 표의 Ea·D(600 K) **앵커에서 외삽**할 뿐이라, 앵커가
    철회되면 이 표도 같이 철회된다. 홉을 실제로 세는 것은 tools/ionic/aimd_jump_stats.py 다.
  · d_hop = 3 Å 은 argyrodite 대표값 하나다 — 계마다 다르고, n_hop 은 d_hop² 에 반비례한다.
  · β 를 예측하지 않는다. "홉이 몇 개면 β 가 설 수 있나" 의 **필요조건**만 본다.
"""
import argparse
import csv
import math

KB = 8.617333262e-5
D_HOP = 3.0          # A — 이웃 Li 자리 간격 (argyrodite 대표 홉 길이)
N_OK, N_EDGE = 10.0, 3.0

# 앵커: 우리 db 멀티시드 실측 (md_temperature_feasibility.py 와 같은 출처)
SYS = {
    "LPSCl1.6 (modelc)": {"Ea": 0.197, "D600": 1.041e-5,
                          "src": "b2o3_md_arrhenius.json 3-seed x 3-T"},
    "LPSOCl1.6":         {"Ea": 0.287, "D600": 6.2705e-6,
                          "src": "lpsocl_md_arrhenius.json 4-seed x 3-T"},
    # ⛔ 2026-08-24 — Ea 0.199 (전구간 600–1000 K 단일적합) 는 철회됐다. 아레니우스가
    #   800 K 위에서 굽어(600→800 0.222 / 800→1000 0.077) 하나의 직선이 성립하지 않는다.
    #   이 도구는 **저온(300–500 K) 외삽**에 쓰므로 저온 구간값을 써야 한다. 굽은 곡선을
    #   평균낸 0.199 를 쓰면 저온을 실제보다 **쉽게** 본다(홉이 더 많이 일어난다고 센다).
    #   0.2241 = 3시드 구간적합 평균 (±0.0606). 근거: b2o3_md_arrhenius.json
    #   segment_extrapolation_2026_08_24 · kb/results/b2o3_arrhenius_curvature_2026_08_23.md
    "B2O3@LPSCl1.6":     {"Ea": 0.2241, "D600": 1.041e-5,
                          "src": "b2o3_md_arrhenius.json 구간적합 600→800 (3시드, ±0.061)"},
}
T_REF = 600.0
TEMPS = [1000, 900, 800, 700, 600, 500, 400, 300]

# v2 실측 beta (2026-08-04, 멀티시드 앙상블 · 창 2-50 ps) — 예측 검증용
BETA_OBS = {("LPSCl1.6 (modelc)", 600): 0.87, ("LPSCl1.6 (modelc)", 800): 0.93,
            ("LPSCl1.6 (modelc)", 1000): 0.92,
            ("LPSOCl1.6", 600): 0.61, ("LPSOCl1.6", 800): 0.86, ("LPSOCl1.6", 1000): 1.02,
            ("B2O3@LPSCl1.6", 600): 0.81, ("B2O3@LPSCl1.6", 800): 0.83,
            ("B2O3@LPSCl1.6", 1000): 0.97}


def D_at(T, Ea, D600):
    return D600 * math.exp(-Ea / KB * (1.0 / T - 1.0 / T_REF))


def verdict(n):
    if n >= N_OK:
        return "확산 통계 충분"
    if n >= N_EDGE:
        return "경계 — 시드마다 흔들림"
    return "홉 부족 → beta 낮은 게 정상"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prod_ps", type=float, default=200.0, help="궤적 길이 [ps]")
    ap.add_argument("--d_hop", type=float, default=D_HOP, help="홉 거리 [A]")
    ap.add_argument("--csv", help="Origin-ready CSV 로도 저장")
    a = ap.parse_args()

    rows = []
    for name, s in SYS.items():
        print(f"\n══ {name}   Ea {s['Ea']:.3f} eV · D(600 K) {s['D600']:.3e} cm²/s"
              f"   [{s['src']}]")
        print(f"   {'T (K)':>6} {'D (cm²/s)':>12} {'MSD@%.0fps' % a.prod_ps:>12} "
              f"{'홉/이온':>8} {'실측 β':>8}  판정")
        for T in TEMPS:
            D = D_at(T, s["Ea"], s["D600"])
            msd = 6.0 * (D * 1e16 * 1e-12) * a.prod_ps        # A^2
            n = msd / a.d_hop ** 2
            b = BETA_OBS.get((name, T))
            bs = (f"{b:.2f}" + ("✓" if b >= 0.8 else "⛔")) if b else "—"
            print(f"   {T:>6} {D:>12.2e} {msd:>12.1f} {n:>8.1f} {bs:>8}  {verdict(n)}")
            rows.append({"system": name, "T_K": T, "prod_ps": f"{a.prod_ps:.0f}",
                         "D_cm2_s": f"{D:.4e}", "MSD_A2": f"{msd:.2f}",
                         "hops_per_ion": f"{n:.2f}", "beta_observed": b if b else "",
                         "verdict": verdict(n)})

    print("\n" + "─" * 78)
    print(f"기준: n_hop = 6Dt/d_hop²  (d_hop {a.d_hop} Å) · ≥{N_OK:.0f} 충분 · "
          f"{N_EDGE:.0f}–{N_OK:.0f} 경계 · <{N_EDGE:.0f} 부족")
    print("⚠ 이건 **유효(독립) 홉 수** f·n 이다 — 되돌아오는 홉은 MSD 를 줄이므로")
    print("  MSD/d² 는 실제 이벤트 수 n 의 **하한**이다(상한이 아니다 — 2026-09-11 정정).")
    print("  '통계가 충분한가' 에 맞는 양이 바로 이 유효 홉 수라 경계선은 그대로 읽는다.")
    print(f"  실측 f ≈ 0.7 (LPSOCl 3x3x1 400 ps: 궤적 계수 20-94 vs MSD/d² 15.5-68)")
    print("★ 검증: 600 K 예측(13.9/8.4/13.9)이 실측 β(0.87/0.61/0.81) 순서를 맞춘다 —")
    print("  LPSOCl 600 K 탈락은 Ea 가 높아 같은 시간에 홉이 40% 적었던 결과다.")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as f:
            f.write("# Hops per Li ion vs temperature: n_hop = 6*D*t / d_hop^2.\n")
            f.write("# D from measured multiseed Ea + D(600 K); d_hop = 3 A (Li-Li site spacing).\n")
            f.write("# UPPER BOUND: back-correlated hops are not counted, so the real hop\n")
            f.write("#   requirement is higher. Read thresholds conservatively.\n")
            f.write("# RETRACTED 2026-09-07: the previous header said '(Haven 0.3-0.7 < 1)'.\n")
            f.write("#   That range is a literature value, not ours, and li_transport.json\n")
            f.write("#   forbids rescaling our numbers with it. Our measured H_R = 0.84 +/- 0.06\n")
            f.write("#   (haven_ratio_measured_2026_09_07.json) is citable:false — a direction\n")
            f.write("#   diagnostic, so no magnitude claim is made here.\n")
            f.write("# beta_observed = v2 multiseed ensemble gate result (2026-08-04) where available.\n")
            # 앵커를 헤더에 적는다 — 이 표는 궤적이 아니라 Ea·D(600 K) 앵커에서 외삽한
            # 값이라, 앵커가 바뀌면 표 전체가 바뀐다 (2026-08-24 b2o3 Ea 0.199 → 0.2241
            # 구간적합 정정이 실제로 그랬다: 1000 K n_hop 64.7 → 78.6).
            for _n, _s in SYS.items():
                f.write(f"# ANCHOR {_n}: Ea={_s['Ea']} eV, D600={_s['D600']:.4e} cm2/s "
                        f"[{_s['src']}]\n")
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        print(f"\n→ {a.csv}")


if __name__ == "__main__":
    main()
