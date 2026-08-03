#!/usr/bin/env python3
"""md_temperature_feasibility.py — "그 온도에서 MD 를 돌 수 있나" 를 우리 실측으로 계산한다.

1저자 요청(2026-08-03): 600/800/1000 K 말고 500/700/900 K 도 되나? 300 K 는 왜 안 되나?

⚠ 답은 "된다/안 된다" 가 아니라 **얼마나 돌아야 하나** 다. 온도가 낮아지면 Li 가 덜 뛰고,
  MSD 가 확산 영역에 들어가는 데 걸리는 시간이 아레니우스로 **지수적으로** 늘어난다.
  그래서 각 온도에 대해 **필요 prod 시간**을 계산해 실행 가능 여부를 판정한다.

계산 근거 (전부 우리 db 실측):
  D(T) = D(T_ref) * exp(-Ea/kB * (1/T - 1/T_ref))       아레니우스
  MSD  = 6 D t                                           3차원 확산
  t_min = MSD_gate / (6 D(T))                            게이트(3 A^2) 도달 시간

⚠⚠ **t_min 은 하한이지 충분조건이 아니다.** 우리 확산영역 게이트는 MSD 크기 말고
  **beta = d log MSD / d log t 가 0.8-1.2** 인지도 본다. beta 는 '뛴 횟수' 의 문제라
  MSD 만 채워도 통과 못 할 수 있다 — 실제로 comp1 은 600 K 에서 MSD 는 충분한데
  beta 0.17-0.79 로 전부 탈락했다(kb/results/mlip_md_diffusive_gate_2026_08_01.md).
  그래서 아래 표의 판정은 **t_min 의 10배**를 실무 기준으로 쓴다.

  python3 tools/ionic/md_temperature_feasibility.py
  python3 tools/ionic/md_temperature_feasibility.py --csv db/properties/md_temperature_feasibility.csv
"""
import argparse
import csv
import math

KB = 8.617333262e-5        # eV/K
MSD_GATE = 3.0             # A^2 — tools/ionic/msd_diffusive_check.py 의 MSD_MIN_A2
SAFETY = 10                # beta 까지 통과하려면 t_min 만으로는 부족하다(위 주석)

# ── 우리 db 실측 앵커 ────────────────────────────────────────────────────
#   Ea 는 멀티시드 3-T 적합, D 는 600 K 시드평균. 출처를 각 항목에 적는다.
SYS = {
    "LPSCl1.6 (modelc)": {
        "Ea": 0.197, "Ea_err": 0.032, "D600": 1.041e-5 / 1.0,   # 아래 note 참조
        "src": "db/properties/b2o3_md_arrhenius.json (3-seed x 3-T) · "
               "D600 은 b2o3 와 같은 프로토콜의 modelc 값 사용",
        "note": "⚠ li_transport.json 헤드라인은 Ea 0.2235(단일시드 계열). 멀티시드 0.197±0.032 를 쓴다.",
    },
    "LPSOCl (+O)": {
        "Ea": 0.287, "Ea_err": 0.024, "D600": 6.2705e-6,
        "src": "db/properties/lpsocl_md_arrhenius.json (4-seed x 3-T, D_600_mean)",
        "note": None,
    },
    "B2O3-doped": {
        "Ea": 0.199, "Ea_err": 0.034, "D600": 1.041e-5,
        "src": "db/properties/b2o3_md_arrhenius.json (3-seed x 3-T reseed, D_600_mean)",
        "note": None,
    },
}
T_REF = 600.0
TEMPS = [300, 400, 500, 600, 700, 800, 900, 1000]


def D_at(T, Ea, D600):
    return D600 * math.exp(-Ea / KB * (1.0 / T - 1.0 / T_REF))


def t_min_ps(T, Ea, D600):
    """MSD 게이트(3 A^2) 도달에 필요한 시간 [ps]. D 는 cm^2/s → A^2/ps 로 환산."""
    D = D_at(T, Ea, D600) * 1e16 * 1e-12        # cm^2/s → A^2/ps
    return MSD_GATE / (6.0 * D)


def verdict(t_need_ps):
    """실무 판정. 우리 표준 prod 는 200 ps, 연장판이 1600 ps."""
    if t_need_ps <= 200:
        return "✅ 표준 200 ps 로 가능"
    if t_need_ps <= 1600:
        return "🔶 연장 필요 (1600 ps 판)"
    if t_need_ps <= 20000:
        return "⚠ 20 ns 급 — 셀 확대 병행 필수"
    return "⛔ 직접 MD 불가"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="Origin-ready CSV 로도 저장")
    a = ap.parse_args()

    rows = []
    for name, s in SYS.items():
        print(f"\n══ {name}   Ea = {s['Ea']:.3f} ± {s['Ea_err']:.3f} eV · "
              f"D(600 K) = {s['D600']:.3e} cm²/s")
        print(f"   출처: {s['src']}")
        if s["note"]:
            print(f"   {s['note']}")
        print(f"   {'T(K)':>6} {'D (cm²/s)':>12} {'MSD 3 Å² 도달':>14} "
              f"{'실무 필요(×10)':>16}  판정")
        for T in TEMPS:
            D = D_at(T, s["Ea"], s["D600"])
            tm = t_min_ps(T, s["Ea"], s["D600"])
            need = tm * SAFETY
            unit = (f"{need:,.0f} ps" if need < 1e4 else
                    f"{need/1000:,.1f} ns" if need < 1e7 else f"{need/1e6:,.1f} µs")
            print(f"   {T:>6} {D:>12.3e} {tm:>11.1f} ps {unit:>16}  {verdict(need)}")
            rows.append({"system": name, "T_K": T, "Ea_eV": s["Ea"],
                         "D_cm2_s": f"{D:.4e}", "t_MSD3_ps": f"{tm:.2f}",
                         "t_practical_ps": f"{need:.1f}", "verdict": verdict(need)})

    print("\n" + "─" * 78)
    print("판정 기준: 표준 prod 200 ps · 연장판 1600 ps · 실무 필요 = MSD 도달시간 × 10")
    print("⚠ ×10 인 이유: MSD 크기를 채워도 beta(=d log MSD/d log t) 가 0.8 미만이면")
    print("   케이지 진동이라 D 를 못 쓴다. comp1 은 600 K 에서 MSD 는 충분한데")
    print("   beta 0.17-0.79 로 전부 탈락했다 — 시간이 아니라 **뛴 횟수**의 문제다.")

    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8-sig") as f:
            f.write("# MD temperature feasibility — required production time per temperature.\n")
            f.write("# t_MSD3 = MSD_gate(3 A^2)/(6D); t_practical = 10x (beta gate margin).\n")
            f.write("# D(T) from measured Ea and D(600 K); see tools/ionic/md_temperature_feasibility.py\n")
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader(); w.writerows(rows)
        print(f"\n→ {a.csv}")


if __name__ == "__main__":
    main()
