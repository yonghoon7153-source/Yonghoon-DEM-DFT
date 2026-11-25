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
        "note": "⚠ li_transport.json 헤드라인은 Ea 0.2235(단일시드 계열). 멀티시드 0.197±0.032 를 쓴다. "
                "⚠⚠ 2026-08-24 — modelc 도 **102 meV 굽는다**(b2o3 145 meV 와 같은 방향). "
                "b2o3 처럼 구간값으로 바꿔야 하는데 modelc 600 K 가 아직 단일시드라 "
                "시드별 구간적합을 못 한다. gabia 3시드 런이 끝나면 이 앵커도 갱신할 것.",
    },
    "LPSOCl (+O)": {
        "Ea": 0.287, "Ea_err": 0.024, "D600": 6.2705e-6,
        "src": "db/properties/lpsocl_md_arrhenius.json (4-seed x 3-T, D_600_mean)",
        "note": None,
    },
    # ⛔ 2026-08-24 — 옛 앵커 Ea 0.199 ± 0.034 (600–1000 K 전구간 단일적합) 는 철회됐다.
    #   800 K 위에서 굽는다 (600→800 0.222 / 800→1000 0.077, 145 meV). 이 표는 **저온**
    #   MD 소요시간을 예측하므로 저온 구간값을 쓴다 — 평균낸 0.199 는 저온을 실제보다
    #   쉽게(짧게) 보이게 한다. 오차막대도 0.034 → 0.061 로 커진다(시드별 적합).
    "B2O3-doped": {
        "Ea": 0.2241, "Ea_err": 0.0606, "D600": 1.041e-5,
        "src": "db/properties/b2o3_md_arrhenius.json segment_extrapolation_2026_08_24 "
               "(600→800 K 구간, 3시드 각각 적합, D_600_mean)",
        "note": "⛔ 전구간 단일 Ea 는 이 계에 없다. 800→1000 은 0.077 eV 로 갈린다.",
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



# ── 처리량 스케일링 (2026-08-26 신설) ────────────────────────────────────────
def cmd_scaling(a):
    """**셀을 키우면 실제로 몇 배 느려지나** 를 잰다. → 표 + JSON

    왜 필요한가:
      open_items #1·#2 가 *"200 ps 가 부족하다 → 셀 확대 또는 시간 연장"* 에서 멈춰 있다.
      그런데 **셀을 9배로 키우면 9배 느려지는지 우리는 모른다.**
      `park2024_sevennet_parallel_gnn_md` `Fig. S1` 이 보인 것: GNN-MD 는 **원자 수가 적으면
      GPU 가 논다.** 62원자는 그 저이용 구간 한복판일 가능성이 크다 — 그렇다면 248·558원자로
      키워도 **벽시계는 9배가 아니라 훨씬 덜 는다.**

    ⛔ 이 도구가 못 하는 것
      · 물리를 안 본다. **속도만** 잰다 (MSD·β 는 별개다).
      · 짧은 구간(기본 20 스텝)의 속도라 **장시간 평균이 아니다** — 캐시·열 상태가 다르다.
      · 다른 작업이 같은 GPU 를 쓰면 값이 오염된다. 실행 전 `nvidia-smi` 를 볼 것.
    """
    import json as _j, pathlib as _pl, time
    import numpy as np
    from ase.io import read as _read
    from ase.md.langevin import Langevin
    from ase import units
    from fairchem.core import pretrained_mlip, FAIRChemCalculator

    at0 = _read(a.struct)
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=a.device)
    rows = []
    print(f"  기준 구조 {a.struct} · {len(at0)}원자 · 스텝 {a.steps} · dt {a.dt} fs\n")
    for rep in a.reps:
        n = [int(x) for x in rep.split("x")]
        at = at0.repeat(n)
        at.calc = FAIRChemCalculator(pred, task_name="omat")
        dyn = Langevin(at, a.dt * units.fs, temperature_K=a.temp,
                       friction=0.02 / units.fs)
        dyn.run(3)                                   # 워밍업 — 첫 호출은 컴파일·할당이 섞인다
        t0 = time.perf_counter()
        dyn.run(a.steps)
        el = time.perf_counter() - t0
        ps = a.steps * a.dt / 1000.0
        rate = ps / el * 86400.0                      # ps/day
        rows.append({"rep": rep, "n_atoms": len(at), "elapsed_s": round(el, 2),
                     "ps_per_day": round(rate, 1),
                     "atom_ps_per_day": round(rate * len(at), 1)})
        print(f"   {rep:>7}  {len(at):>5}원자  {el:6.2f} s/{a.steps}스텝  "
              f"→ {rate:8.1f} ps/day   {rate*len(at):.3e} atom·ps/day")
    if len(rows) >= 2:
        b = rows[0]
        print(f"\n  ── 기준({b['rep']}, {b['n_atoms']}원자) 대비 ──")
        for r in rows[1:]:
            fa = r["n_atoms"] / b["n_atoms"]
            ft = b["ps_per_day"] / r["ps_per_day"] if r["ps_per_day"] else float("inf")
            eff = fa / ft if ft else 0
            tag = ("✅ GPU 가 놀고 있었다 — 키워도 거의 안 느려진다" if ft < fa * 0.4 else
                   "🔶 부분 이득" if ft < fa * 0.8 else "⛔ 원자수만큼 느려진다")
            print(f"   {r['rep']:>7}  원자 ×{fa:.0f}  **벽시계 ×{ft:.1f}**  "
                  f"(원자당 처리량 ×{eff:.2f})  {tag}")
        print(f"\n  ⛔ 속도만 잰 것이다. 그 셀에서 물리가 맞는지는 별개다 "
              f"(make_md_supercell.py 의 두 기준을 볼 것).")
    if a.out:
        _pl.Path(a.out).write_text(_j.dumps(
            {"struct": a.struct, "device": a.device, "steps": a.steps, "dt_fs": a.dt,
             "temperature_K": a.temp, "rows": rows,
             "⛔_do_not": "속도만이다. MSD·β·유한크기 판정과 섞지 말 것"},
            ensure_ascii=False, indent=2))
        print(f"\n✓ → {a.out}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", help="Origin-ready CSV 로도 저장")
    ap.add_argument("--scaling", action="store_true",
                    help="**처리량 스케일링 측정 모드** — 셀을 키우며 벽시계를 잰다")
    ap.add_argument("--struct", help="--scaling: 기준 구조")
    ap.add_argument("--reps", nargs="+", default=["1x1x1", "2x2x1", "3x3x1"],
                    help="--scaling: 시험할 배수 (기본 1x1x1 2x2x1 3x3x1)")
    ap.add_argument("--steps", type=int, default=20, help="--scaling: 측정 스텝 수")
    ap.add_argument("--dt", type=float, default=2.0, help="--scaling: dt (fs)")
    ap.add_argument("--temp", type=float, default=600.0, help="--scaling: 온도 K")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out", help="--scaling: JSON 출력")
    a = ap.parse_args()

    if a.scaling:
        if not a.struct:
            import sys as _s
            _s.exit("⛔ --scaling 에는 --struct 가 필요하다 "
                    "(예: --struct db/structures/modelc_v3_62atom_V0.cif)")
        return cmd_scaling(a)

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
    import sys as _sys
    _sys.exit(main() or 0)
