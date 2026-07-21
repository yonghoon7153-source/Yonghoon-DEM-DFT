#!/usr/bin/env python3
"""comp_phonon_uma.py — champion V0가 진짜 국소 최소인지 UMA Γ-진동으로 스크린.

동기 (2026-07-21): comp2는 comp4와 같은 50:50 혼합 할라이드 — adhesion 캠페인에서
comp4 champion이 단일-프레임 셀 압축 artifact(4%)로 판명된 리스크 클래스라,
comp2 champion V0의 동적 안정성(허수 모드 유무)을 확인한다.

프로토콜 (스크린 레벨 — UMA 기준의 최소 여부):
  1. V0에서 UMA 힘 fmax 보고 (DFT-V0와 UMA 최소의 어긋남 크기)
  2. 셀 고정 gentle relax (fmax 0.02) → V0 대비 MIC-RMSD 보고
     (RMSD가 크면 = UMA가 다른 분지로 이동 = 그 자체가 적신호)
  3. UMA-최소에서 유한차분 Γ 진동 (ASE Vibrations, delta 0.01 A, 6N 중심차분)
  4. 판정: 음향 3개(|ω|<20i cm-1 노이즈 허용) 외 허수 모드 있으면 SOFT
     → DFT ph.x(Γ, NC 80/320) 에스컬레이션 권고. 없으면 STABLE.

gabia (uma env, GPU는 pbrefine 점유 → --device cpu):
  tmux new -s c2phon -d '/data/apps/miniforge3/envs/uma/bin/python3 \
      tools/electronic/comp_phonon_uma.py --device cpu \
      --out /data/work/runs/comp2_phonon > /data/work/runs/comp2_phonon.log 2>&1'
"""
import argparse
import json
import os
import time

import numpy as np
from ase.io import read, write
from ase.optimize import BFGS
from ase.vibrations import Vibrations


def mic_rmsd(a, b):
    d = a.get_positions() - b.get_positions()
    f = d @ np.linalg.inv(a.cell.array)
    f -= np.round(f)
    d = f @ a.cell.array
    return float(np.sqrt((d ** 2).sum(axis=1).mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structure", default="db/structures/comp2_V0.cif")
    ap.add_argument("--label", default="comp2")
    ap.add_argument("--out", default="./phonon_out")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--fmax_relax", type=float, default=0.005)
    ap.add_argument("--delta", type=float, default=0.01)
    ap.add_argument("--imag_tol_cm1", type=float, default=20.0)
    ap.add_argument("--follow", type=int, default=1,
                    help="가장 깊은 허수 모드 N개를 ±변위-이완 추적 (진짜 안장점 판별)")
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    os.chdir(a.out)

    repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    spath = a.structure if os.path.isabs(a.structure) else os.path.join(repo, a.structure)
    at0 = read(spath)
    print(f"[{a.label}] {spath}  nat={len(at0)}  cell={np.diag(at0.cell.array).round(3)}", flush=True)

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(a.uma_model, device=a.device)
    calc = FAIRChemCalculator(predictor, task_name=a.uma_task)

    # 1) UMA 힘 @ V0
    at = at0.copy(); at.calc = calc
    f0 = float(np.abs(at.get_forces()).max())
    e0 = float(at.get_potential_energy())
    print(f"[1] UMA fmax @ V0 = {f0:.4f} eV/A   E = {e0:.4f} eV", flush=True)

    # 2) gentle relax (cell fixed)
    t = time.time()
    BFGS(at, logfile="relax.log").run(fmax=a.fmax_relax, steps=300)
    rmsd = mic_rmsd(at, at0)
    fr = float(np.abs(at.get_forces()).max())
    print(f"[2] relax done ({time.time()-t:.0f}s)  fmax={fr:.4f}  MIC-RMSD vs V0 = {rmsd:.4f} A"
          f"  {'⚠ 분지 이동 의심(>0.2)' if rmsd > 0.2 else '(같은 분지)'}", flush=True)

    # 3) FD Γ vibrations (캐시 이름에 기하 해시 — 재이완 후 stale 캐시 방지)
    t = time.time()
    ghash = abs(hash(at.get_positions().tobytes())) % 100000
    vib = Vibrations(at, delta=a.delta, name=f"vib_{a.label}_{ghash}")
    vib.run()
    freqs = vib.get_frequencies()          # complex array, cm^-1
    print(f"[3] vibrations done ({time.time()-t:.0f}s)  n_modes={len(freqs)}", flush=True)

    # 4) 판정: 허수 모드 = ASE가 복소수로 반환 (imag part = |ω| cm-1)
    vals = [(-abs(f.imag) if abs(f.imag) > 1e-6 else f.real) for f in freqs]
    order = np.argsort(vals)
    vals_s = [vals[i] for i in order]
    n_imag = sum(1 for v in vals_s if v < -a.imag_tol_cm1)
    lowest = ", ".join(f"{v:+.1f}" for v in vals_s[:12])
    print(f"[4] lowest 12 modes (cm-1, 음수=허수): {lowest}")
    verdict = "STABLE" if n_imag == 0 else f"SOFT ({n_imag} imaginary > {a.imag_tol_cm1}i)"
    print(f"    음향 허용치 {a.imag_tol_cm1}i cm-1 밖 허수 모드: {n_imag}개  →  VERDICT: {verdict}", flush=True)

    # 5) 모드 성분: 허수/최저 모드를 어느 원소가 흔드는가 (Li 지배 = 얕은 케이지 = 무죄 후보)
    syms = np.array(at.get_chemical_symbols())
    char = []
    print("[5] mode character (원소별 |변위|^2 비율):")
    for rank in range(min(8, len(order))):
        i = int(order[rank])
        m = vib.get_mode(i)                      # (nat, 3)
        w = (m ** 2).sum(axis=1); w /= w.sum()
        frac = {s: round(float(w[syms == s].sum()), 3) for s in ("Li", "P", "S", "Cl", "Br") if (syms == s).any()}
        char.append({"freq_cm1": round(vals[i], 1), "species_frac": frac})
        print(f"    {vals[i]:+8.1f} cm-1  " + "  ".join(f"{k} {v:.0%}" for k, v in frac.items()), flush=True)

    # 6) 변위-이완 추적: 가장 깊은 허수 모드 ± 따라가면 더 낮은 최소가 있는가
    follow = []
    E_min = float(at.get_potential_energy())
    for rank in range(min(a.follow, len(order))):
        i = int(order[rank])
        if vals[i] > -a.imag_tol_cm1:
            break
        m = vib.get_mode(i); m = m / np.linalg.norm(m)
        best = None
        for sgn in (+1, -1):
            at2 = at.copy(); at2.positions += sgn * 0.25 * m; at2.calc = calc
            BFGS(at2, logfile=None).run(fmax=0.01, steps=150)
            dE = float(at2.get_potential_energy()) - E_min
            rm = mic_rmsd(at2, at)
            fn = f"{a.label}_followmin_m{rank}_{'p' if sgn > 0 else 'n'}.xyz"
            write(fn, at2)
            follow.append({"mode_cm1": round(vals[i], 1), "dir": sgn, "dE_meV": round(dE * 1e3, 2),
                           "rmsd_A": round(rm, 4), "file": fn})
            if best is None or dE < best[0]:
                best = (dE, fn)
            print(f"[6] follow {vals[i]:+.1f} cm-1 dir {sgn:+d}: ΔE = {dE*1e3:+.2f} meV, RMSD {rm:.4f} A"
                  f"  → {fn}  {'(진짜 안장 — 더 낮은 최소)' if dE < -1e-3 else '(유의미한 하강 없음)'}", flush=True)
        if best and best[0] < -1e-3:
            write(f"{a.label}_followmin_best.xyz", read(best[1]))
            print(f"[6] best lower minimum: {best[1]} (ΔE {best[0]*1e3:+.1f} meV) → {a.label}_followmin_best.xyz", flush=True)

    out = {
        "label": a.label, "structure": os.path.basename(spath), "nat": len(at0),
        "method": f"UMA {a.uma_model}/{a.uma_task} FD Gamma vibrations, delta {a.delta} A, "
                  f"cell-fixed pre-relax fmax {a.fmax_relax}",
        "uma_fmax_at_V0_eVA": round(f0, 4), "relax_rmsd_vs_V0_A": round(rmsd, 4),
        "lowest_modes_cm1": [round(v, 1) for v in vals_s[:20]],
        "n_imaginary_beyond_tol": n_imag, "imag_tol_cm1": a.imag_tol_cm1,
        "verdict": verdict,
        "mode_character": char,
        "mode_follow": follow,
        "note": "UMA-level screen: STABLE = UMA 최소에서 동적 안정. SOFT면 DFT ph.x(Gamma) 확인 필요. "
                "RMSD>0.2 A면 UMA가 V0 분지를 벗어난 것 — 판정 자체를 재고.",
    }
    with open(f"{a.label}_phonon_uma.json", "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print(f">> {a.out}/{a.label}_phonon_uma.json — 붙여주면 db 등록 + 다음 단계(스위트/ph.x) 판정", flush=True)


if __name__ == "__main__":
    main()
