#!/usr/bin/env python3
"""llm_fitting_lpsocl_bm.py — LPSOCl DFT-EOS harvest: Birch-Murnaghan fit + basin check.

Pipeline v2, Step 7: after the KISTI chain writes ALL_DONE (7/7 volumes with
JOB DONE), fit E(V) to 3rd-order Birch-Murnaghan -> V0, B0, B0'; and verify all
volumes stayed in the SAME ionic basin (a volume that basin-hopped during its
fixed-cell relax poisons the fit -> flagged, refit without it).

  conda activate uma
  python3 llm_fitting_lpsocl_bm.py --base /scratch/x3430a02/kgy/lpsocl_eos
  # 부분 수확(미완 볼륨 건너뜀): --allow_partial

Outputs under --base: eos_fit_results.json, eos_EV.csv, prints the verdict.
"""
import argparse
import json
import re
import numpy as np

RY2EV = 13.605693122994
EVA3_2_GPA = 160.21766208
VOLS = ["v094", "v096", "v098", "v100", "v102", "v104", "v106"]


def parse_relax(path):
    """relax.out -> (E_final_Ry, cell(3x3 A), frac(final) Nx3, converged?, done?)"""
    txt = open(path, errors="ignore").read()
    done = "JOB DONE" in txt
    conv = "bfgs converged" in txt
    Es = re.findall(r"^!\s+total energy\s+=\s+([-\d.]+)\s+Ry", txt, re.M)
    E = float(Es[-1]) if Es else None
    lines = txt.splitlines()
    nat = None
    for l in lines:
        m = re.search(r"number of atoms/cell\s+=\s+(\d+)", l)
        if m:
            nat = int(m.group(1)); break
    # cell: fixed-cell relax -> read the input echo "crystal axes" (alat units) + alat
    alat = None
    for l in lines:
        m = re.search(r"lattice parameter \(alat\)\s+=\s+([\d.]+)\s+a.u.", l)
        if m:
            alat = float(m.group(1)) * 0.529177210903; break
    cell = None
    for i, l in enumerate(lines):
        if "crystal axes: (cart. coord. in units of alat)" in l:
            cell = np.array([[float(x) for x in re.findall(r"[-\d.]+", lines[i + k])[1:4]]
                             for k in (1, 2, 3)]) * alat
            break
    # last ATOMIC_POSITIONS (crystal) block
    idx = [i for i, l in enumerate(lines) if l.strip().startswith("ATOMIC_POSITIONS")]
    frac = None
    if idx and nat:
        blk = lines[idx[-1] + 1: idx[-1] + 1 + nat]
        try:
            frac = np.array([[float(x) for x in b.split()[1:4]] for b in blk])
        except (ValueError, IndexError):
            frac = None
    return E, cell, frac, conv, done


def bm3(V, E0, V0, B0, Bp):
    x = (V0 / V) ** (2.0 / 3.0)
    return E0 + 9 * V0 * B0 / 16.0 * ((x - 1) ** 3 * Bp + (x - 1) ** 2 * (6 - 4 * x))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--ref", default="v100", help="basin-check reference volume")
    ap.add_argument("--rmsd_flag", type=float, default=0.30,
                    help="mean |disp| (A, MIC) above this vs ref = basin hop flag")
    ap.add_argument("--allow_partial", action="store_true")
    a = ap.parse_args()

    data = {}
    for v in VOLS:
        try:
            E, cell, frac, conv, done = parse_relax(f"{a.base}/{v}/relax.out")
        except FileNotFoundError:
            print(f"  {v}: relax.out 없음 — skip"); continue
        if not done:
            print(f"  {v}: JOB DONE 없음 (미완) — skip"); continue
        V = abs(np.linalg.det(cell))
        data[v] = dict(E_Ry=E, V_A3=V, cell=cell, frac=frac, conv=conv)
        print(f"  {v}: E={E:.6f} Ry  V={V:.2f} A^3  bfgs={'수렴' if conv else 'MAXSTEP?'}")
    if len(data) < (4 if a.allow_partial else 7):
        raise SystemExit(f"수확 가능 볼륨 {len(data)}개 — "
                         + ("--allow_partial로도 4개 미만이면 피팅 불가" if a.allow_partial
                            else "7/7 필요 (부분 피팅은 --allow_partial)"))

    # ---- basin check: mean MIC displacement (A) vs ref volume, in ref cell metric ----
    ref = a.ref if a.ref in data else sorted(data)[len(data) // 2]
    f0 = data[ref]["frac"]; c0 = data[ref]["cell"]
    flags = {}
    for v, d in data.items():
        if d["frac"] is None or f0 is None or len(d["frac"]) != len(f0):
            flags[v] = None; continue
        df = d["frac"] - f0
        df -= np.round(df)                      # MIC in fractional space
        disp = np.linalg.norm(df @ c0, axis=1)  # -> A (ref-cell metric)
        flags[v] = float(disp.mean())
    print(f"\nbasin check (vs {ref}, mean MIC disp A): " +
          "  ".join(f"{v}:{(m if m is None else round(m,3))}" for v, m in flags.items()))
    hoppers = [v for v, m in flags.items() if m is not None and m > a.rmsd_flag]
    if hoppers:
        print(f"  !! basin-hop 의심 (> {a.rmsd_flag} A): {hoppers} — 1차 피팅에서 제외")

    # ---- BM fit (scipy) ----
    from scipy.optimize import curve_fit
    use = [v for v in data if v not in hoppers]
    Vv = np.array([data[v]["V_A3"] for v in use])
    Ev = np.array([data[v]["E_Ry"] for v in use]) * RY2EV
    order = np.argsort(Vv); Vv, Ev = Vv[order], Ev[order]
    p0 = [Ev.min(), Vv[np.argmin(Ev)], 0.15, 4.0]     # B0 ~ 24 GPa = 0.15 eV/A^3
    popt, pcov = curve_fit(bm3, Vv, Ev, p0=p0, maxfev=20000)
    perr = np.sqrt(np.diag(pcov))
    E0, V0, B0, Bp = popt
    res_meV = (Ev - bm3(Vv, *popt)) * 1000
    print(f"\n=== Birch-Murnaghan (3rd) — {len(use)} 볼륨 ===")
    print(f"  V0 = {V0:.2f} ± {perr[1]:.2f} A^3")
    print(f"  B0 = {B0*EVA3_2_GPA:.2f} ± {perr[2]*EVA3_2_GPA:.2f} GPa")
    print(f"  B' = {Bp:.2f} ± {perr[3]:.2f}")
    print(f"  잔차: max |{np.abs(res_meV).max():.2f}| meV  (점별: "
          + " ".join(f"{r:+.1f}" for r in res_meV) + ")")

    with open(f"{a.base}/eos_EV.csv", "w") as f:
        f.write("volume_label,V_A3,E_Ry,E_eV,used_in_fit,basin_mean_disp_A\n")
        for v in sorted(data):
            d = data[v]
            f.write(f"{v},{d['V_A3']:.4f},{d['E_Ry']:.8f},{d['E_Ry']*RY2EV:.6f},"
                    f"{v in use},{flags.get(v)}\n")
    out = dict(V0_A3=V0, V0_err=perr[1], B0_GPa=B0 * EVA3_2_GPA,
               B0_err_GPa=perr[2] * EVA3_2_GPA, Bprime=Bp, Bprime_err=perr[3],
               E0_eV=E0, residuals_meV=res_meV.tolist(), used=use,
               basin_hoppers=hoppers, basin_ref=ref,
               basin_mean_disp_A={k: vv for k, vv in flags.items()})
    with open(f"{a.base}/eos_fit_results.json", "w") as f:
        json.dump(out, f, indent=1)
    print(f"\nsaved: {a.base}/eos_fit_results.json + eos_EV.csv")
    print("다음 단계(pipeline v2): V0 셀로 Step 8 (성질 계산) — B0는 무도핑 21.7 /"
          " B2O3 24.5 GPa와 비교해 O-도핑 강성 효과 판정.")


if __name__ == "__main__":
    main()
