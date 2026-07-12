#!/usr/bin/env python3
"""uma_hydroxyl_screen.py — SDCP SO3H | HYDROXYLATED LiNiO2(104): H-bond screen (UMA).

질문 (문헌 화해): 깨끗한 격자 O와는 수소결합 전구체가 없었다(6배향 스크린 음성).
그럼 실표면처럼 수산화(OH)된 표면에서는 SO3H가 수소결합을 하는가?

모델: 깨끗한 DFT 슬랩(전체 동결) 위에 해리수 n개(OH@표면양이온 + H@격자O; 전하중성)를
패치로 흡착·이완 → 그 패치 위에 중성 v7c를 (i) 산성 O-H가 아래(OH_down),
(ii) 설포네이트가 아래(sulfonate_down)로 놓고 UMA 이완 → 판정:
  · H-BOND     : 산성 H ··· (수산기O 또는 격자O) <= 2.2 A
  · ACTIVATED  : 산성 O-H > 1.05 A (늘어남)
  · TRANSFERRED: 산성 O-H > 1.30 A + 새 O-H < 1.10 A  ← UMA는 전하분리를 못 다루므로
                 이 이벤트는 "후보"일 뿐, 반드시 DFT로 재검할 것.

  conda activate uma; export HF_HUB_OFFLINE=1
  python3 uma_hydroxyl_screen.py --slab slab_clean.xyz --moldir <dir with sdcp_v7c_neutral.xyz> \
      --out hydroxyl_screen --nwater 3
기본 device=cuda: 3090에서 pw.x(~19GB) 옆 잔여 ~5GB에 UMA-S가 공존 가능. CUDA OOM이
나면 UMA만 죽고 pw.x는 무사하니 --device cpu로 재실행하면 됨 (계산 결과는 동일).
"""
import argparse
import os
import numpy as np

from ase import Atoms
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator


def hcount(mol, i, cut=1.25):
    d = mol.get_all_distances()
    return sum(1 for j, s in enumerate(mol.get_chemical_symbols())
               if s == "H" and j != i and d[i, j] < cut)


def find_groups(mol):
    sym = mol.get_chemical_symbols()
    d = mol.get_all_distances()
    Ss = [i for i, s in enumerate(sym) if s == "S"
          and sum(1 for j, t in enumerate(sym) if t == "O" and d[i, j] < 1.8) >= 3]
    assert len(Ss) == 1, "sulfonate S not unique"
    sS = Ss[0]
    sO = [j for j, t in enumerate(sym) if t == "O" and d[sS, j] < 1.8]
    aH = None
    for j in sO:                                   # 산성 H: 설포네이트 O에 붙은 H
        for k, t in enumerate(sym):
            if t == "H" and d[j, k] < 1.15:
                aH, aO = k, j
    assert aH is not None, "acidic H not found (neutral xyz 맞나?)"
    return sS, sO, aO, aH


def orient(mol, target_vec):
    m = mol.copy()
    com = m.get_center_of_mass()
    v = target_vec / np.linalg.norm(target_vec)
    zm = np.array([0.0, 0.0, -1.0])
    axis = np.cross(v, zm)
    if np.linalg.norm(axis) < 1e-8:
        if v[2] > 0:
            m.rotate(180, "x", center=com)
        return m
    ang = np.degrees(np.arccos(np.clip(np.dot(v, zm), -1, 1)))
    m.rotate(ang, axis / np.linalg.norm(axis), center=com)
    return m


def hydroxylate(slab, n):
    """해리수 n개: 패치(셀 중앙 근처) 양이온 위 OH + 인근 격자 O 위 H. 반환: (atoms, patch_xy)."""
    sym = slab.get_chemical_symbols()
    pos = slab.positions
    ztop = pos[:, 2].max()
    surf = [i for i in range(len(slab)) if pos[i, 2] > ztop - 1.4]
    cats = [i for i in surf if sym[i] in ("Li", "Ni")]
    oxs = [i for i in surf if sym[i] == "O"]
    assert cats and oxs, "surface sites not found"
    cc = slab.cell.array[0] * 0.5 + slab.cell.array[1] * 0.5
    c0 = min(cats, key=lambda i: np.hypot(*(pos[i, :2] - cc[:2])))
    picked = [c0]
    for i in sorted(cats, key=lambda i: np.linalg.norm(pos[i, :2] - pos[c0, :2])):
        if len(picked) >= n:
            break
        if i not in picked and 2.0 < np.linalg.norm(pos[i, :2] - pos[c0, :2]) < 7.0:
            picked.append(i)
    used_o = set()
    ads = Atoms()
    for c in picked[:n]:
        po = pos[c] + [0.0, 0.0, 1.90]                        # OH의 O
        ads += Atoms("O", positions=[po])
        ads += Atoms("H", positions=[po + [0.60, 0.0, 0.78]])  # O-H 0.98, 기울임
        cand = [o for o in oxs if o not in used_o and np.linalg.norm(pos[o] - pos[c]) < 3.8]
        if cand:
            o = min(cand, key=lambda o: np.linalg.norm(pos[o] - pos[c]))
            used_o.add(o)
            ads += Atoms("H", positions=[pos[o] + [0.0, 0.0, 0.98]])  # 해리 H
    patch_xy = np.mean([pos[c, :2] for c in picked[:n]], axis=0)
    return ads, patch_xy


def diagnose(comp, n_sub, aO_l, aH_l, ads_o_idx, lat_o_top):
    """산성 H의 수소결합/이동 판정. *_l 은 분자 내 로컬 인덱스."""
    p = comp.positions
    iH = n_sub + aH_l
    iO = n_sub + aO_l
    doh = np.linalg.norm(p[iH] - p[iO])
    dads = min((np.linalg.norm(p[iH] - p[j]) for j in ads_o_idx), default=9.9)
    dlat = min((np.linalg.norm(p[iH] - p[j]) for j in lat_o_top), default=9.9)
    v = []
    if doh > 1.30 and min(dads, dlat) < 1.10:
        v.append("TRANSFERRED?(DFT 재검 필수)")
    elif doh > 1.05:
        v.append("ACTIVATED")
    if min(dads, dlat) <= 2.20:
        v.append("H-BOND→" + ("adsOH" if dads <= dlat else "latticeO"))
    return doh, dads, dlat, ("+".join(v) if v else "none")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slab", required=True, help="slab_clean.xyz (DFT 기하, 전체 동결)")
    ap.add_argument("--moldir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nwater", type=int, default=3)
    ap.add_argument("--gap", type=float, default=2.2)
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=a.device),
                              task_name="oc20")

    slab = read(a.slab)
    n_slab = len(slab)
    fix = FixAtoms(indices=list(range(n_slab)))               # 슬랩 전체 동결 (클린-DFT 기판 프로토콜)
    ztop = slab.positions[:, 2].max()
    lat_o_top = [i for i in range(n_slab) if slab.get_chemical_symbols()[i] == "O"
                 and slab.positions[i, 2] > ztop - 1.4]

    # ---- gas H2O ref (수산화 흡착에너지 sanity용) ----
    h2o = Atoms("OHH", positions=[[0, 0, 0], [0.96, 0, 0], [-0.24, 0.93, 0]])
    h2o.center(vacuum=8)
    h2o.calc = calc
    FIRE(h2o, logfile=None).run(fmax=a.fmax, steps=200)
    E_h2o = h2o.get_potential_energy()

    # ---- bare frozen slab E ----
    s0 = slab.copy(); s0.set_constraint(fix); s0.calc = calc
    E_slab0 = s0.get_potential_energy()                       # 동결이라 single point와 동일

    # ---- hydroxylated slab (adsorbates만 이완) ----
    ads, patch_xy = hydroxylate(slab, a.nwater)
    sOH = slab.copy() + ads
    sOH.set_constraint(fix)
    sOH.calc = calc
    FIRE(sOH, logfile=None).run(fmax=a.fmax, steps=300)
    E_slabOH = sOH.get_potential_energy()
    n_sub = len(sOH)
    ads_o_idx = [n_slab + k for k, s in enumerate(ads.get_chemical_symbols()) if s == "O"]
    eads = (E_slabOH - E_slab0 - a.nwater * E_h2o) / a.nwater
    print(f"E_slabOH = {E_slabOH:.4f} eV | 해리수 흡착 {eads:+.3f} eV/H2O (음수=유리)", flush=True)
    write(os.path.join(a.out, "slab_hydroxylated.xyz"), sOH)

    # ---- molecule ref ----
    mol0 = read(os.path.join(a.moldir, "sdcp_v7c_neutral.xyz"))
    g = mol0.copy(); g.center(vacuum=10.0); g.calc = calc
    FIRE(g, logfile=None).run(fmax=a.fmax, steps=300)
    E_mol = g.get_potential_energy()
    print(f"E_mol(neutral) = {E_mol:.4f} eV", flush=True)

    sS, sO, aO, aH = find_groups(mol0)
    com = mol0.get_center_of_mass()
    heads = [("OHdown", mol0.positions[aH] - com, (0, 90, 180, 270)),
             ("sulfdown", mol0.positions[sO].mean(axis=0) - com, (0, 90))]

    rows = []
    zt2 = sOH.positions[:, 2].max()
    for hname, vec, rots in heads:
        for rot in rots:
            m = orient(mol0, vec)
            m.rotate(rot, "z", center=m.get_center_of_mass())
            m.positions[:, :2] += patch_xy - m.get_center_of_mass()[:2]   # 패치 위로
            m.positions[:, 2] += (zt2 + a.gap) - m.positions[:, 2].min()
            comp = sOH.copy() + m
            comp.set_constraint(fix)                                      # 원 슬랩만 동결
            comp.calc = calc
            FIRE(comp, logfile=None).run(fmax=a.fmax, steps=a.steps)
            E = comp.get_potential_energy()
            eb = E - E_slabOH - E_mol
            doh, dads, dlat, verdict = diagnose(comp, n_sub, aO, aH, ads_o_idx, lat_o_top)
            label = f"{hname}_r{rot}"
            write(os.path.join(a.out, f"complex_{label}.xyz"), comp)
            rows.append((label, eb, doh, dads, dlat, verdict))
            print(f"  {label:14s} E_bind {eb:+.3f} eV | O-H {doh:.3f} A | "
                  f"H..adsO {dads:.2f} | H..latO {dlat:.2f} | {verdict}", flush=True)

    with open(os.path.join(a.out, "hydroxyl_screen_results.csv"), "w") as f:
        f.write("label,E_bind_eV,acid_OH_A,H_to_adsO_A,H_to_latticeO_A,verdict\n")
        for r in rows:
            f.write(f"{r[0]},{r[1]:.4f},{r[2]:.3f},{r[3]:.2f},{r[4]:.2f},{r[5]}\n")
        f.write(f"# E_slabOH={E_slabOH:.4f}, E_mol={E_mol:.4f}, nwater={a.nwater}, "
                f"E_ads(H2O,diss)={eads:+.3f} eV; slab frozen, adsorbates+mol free; uma-s-1p1/oc20\n")
    print("\n=== 판정 요약 ===")
    hb = [r for r in rows if "H-BOND" in r[5]]
    print(f"수소결합 형성 {len(hb)}/{len(rows)} 배치"
          + (f" — 최단 H···O {min(min(r[3], r[4]) for r in hb):.2f} A" if hb else ""))
    print("깨끗면 스크린(6배향, 전구체 0)과 비교해 읽을 것; TRANSFERRED?는 반드시 DFT 재검.")
    print(f"saved: {a.out}/hydroxyl_screen_results.csv")


if __name__ == "__main__":
    main()
