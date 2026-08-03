#!/usr/bin/env python3
"""phaseA_v7c_orient_scan.py — SDCP v7c | LiNiO2(104) binding: MLIP pose scan.

Spec = sdcp master §2.2: consistent references (shared E_slab, same-setting molecule
ref), orientations sulfonate-down / ether-O-down / chelation (pincer), doped =
neutral radical geometry [M-H]. UMA oc20 (omat verified worse for this system).

리뷰 반영 (2026-08-03, kb/reports/sdcp_review_action_plan_2026_08_03.md):
  · §1-1  측면 위치가 셀 중심 한 곳뿐이었다 → **--grid 3 3** 격자 스캔이 기본.
          (104) 면에는 Ni-top / Li-top / O-top / bridge 가 다 있다 — 한 점만 보면
          "최적 자세"가 사실은 "셀 중심에서의 최적"이 된다.
  · §2-10 FIRE().run() 의 수렴 bool 을 버려서 **미수렴 자세가 챔피언이 될 수 있었다**
          → converged 열을 CSV 에 기록하고 랭킹에서 미수렴을 제외한다.
  · §5-5  --freeze_frac 기본 0.5 → **1.0**. DFT 로 이완한 기판을 UMA 가 재구성하면
          E(복합체)와 E(슬랩)의 슬랩 좌표가 어긋나 그 차이가 E_bind 에 남는다.
          슬랩을 통째로 얼려야 Phase-B 의 좌표일치 assert 를 통과한다.

  conda activate uma
  python3 phaseA_v7c_orient_scan.py --slab db/structures/linio2_104_sym_1x4L4_relaxed.vasp \
      --moldir <...>/inputs/sdcp_v7c --out <...>/phaseA_v2
Outputs: phaseA_v7c_results.csv + relaxed complex xyz per case + log prints.
E_bind = E(complex) - E(slab) - E(molecule)   [negative = binding]

⚠ UMA 절대 E_bind 는 인용 금지(§7 인용 규율) — 자세 **랭킹**만 쓰고, 상위 3-5 자세를
  전부 Phase-B DFT+U 로 재채점한다(챔피언 하나만 믿지 않는다).
"""
import argparse
import os
import numpy as np

from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE


def hcount(mol, i, cut=1.25):
    d = mol.get_all_distances()
    return sum(1 for j, s in enumerate(mol.get_chemical_symbols())
               if s == "H" and j != i and d[i, j] < cut)


def find_groups(mol):
    """indices: sulfonate O's, sulfonate S, ether O (both C neighbors are sp3 CH2/CH)."""
    sym = mol.get_chemical_symbols()
    d = mol.get_all_distances()
    Ss = [i for i, s in enumerate(sym) if s == "S"
          and sum(1 for j, t in enumerate(sym) if t == "O" and d[i, j] < 1.8) >= 3]
    assert len(Ss) == 1, "sulfonate S not unique"
    sS = Ss[0]
    sO = [j for j, t in enumerate(sym) if t == "O" and d[sS, j] < 1.8]
    eth = None
    for i, s in enumerate(sym):
        if s != "O" or i in sO:
            continue
        Cn = [j for j, t in enumerate(sym) if t == "C" and d[i, j] < 1.65]
        if len(Cn) == 2 and all(hcount(mol, c) >= 1 for c in Cn):
            eth = i
            break
    assert eth is not None, "ether O not found"
    return sS, sO, eth


def orient(mol, target_vec):
    """rigid-rotate molecule so target_vec (from COM) points along -z."""
    m = mol.copy()
    com = m.get_center_of_mass()
    v = target_vec / np.linalg.norm(target_vec)
    zm = np.array([0.0, 0.0, -1.0])
    axis = np.cross(v, zm)
    if np.linalg.norm(axis) < 1e-8:
        if v[2] > 0:                      # pointing +z: flip about x
            m.rotate(180, "x", center=com)
        return m
    ang = np.degrees(np.arccos(np.clip(np.dot(v, zm), -1, 1)))
    m.rotate(ang, axis / np.linalg.norm(axis), center=com)
    return m


def grid_points(cell, nx, ny):
    """면내 격자 목표점 (Cartesian xy). (i+0.5)/n 분율 — n 이 홀수면 셀 중심 포함."""
    pts = []
    for i in range(nx):
        for j in range(ny):
            f = np.array([(i + 0.5) / nx, (j + 0.5) / ny, 0.0])
            pts.append(((i, j), (f @ cell)[:2]))
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slab", required=True)
    ap.add_argument("--moldir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--gap", type=float, default=2.4, help="lowest mol atom above slab top (A)")
    ap.add_argument("--cz", type=float, default=0.0,
                    help="override slab c-axis (A) so standing poses are image-clean "
                         "(0=keep file cell; ~40 for the tall SDCP molecule; fixes the v1 "
                         "image-sandwich where a standing pose touched the vertical image)")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--freeze_frac", type=float, default=1.0,
                    help="fix slab atoms with z below this fraction of the slab thickness. "
                         "기본 1.0 = 슬랩 전체 고정 (DFT-이완 기판을 UMA 가 재구성하지 "
                         "못하게 — Phase-B 좌표일치 assert 의 전제). 0.5 등은 진단용.")
    ap.add_argument("--grid", type=int, nargs=2, default=[3, 3], metavar=("NX", "NY"),
                    help="면내 배치 격자 (기본 3 3). 1 1 = 옛 동작(셀 중심 한 점).")
    ap.add_argument("--rots", type=int, nargs="+", default=[0, 90, 180, 270],
                    help="분자 z-회전 각도들")
    ap.add_argument("--tags", nargs="+", default=["neutral", "doped"],
                    help="스캔할 종 (moldir 의 sdcp_v7c_<tag>.xyz)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    # fairchem 은 인자 파싱 뒤에 import — GPU/uma 없는 곳에서도 --help 와 모듈 시험이 되게
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                              task_name="oc20")

    # ---- shared slab reference ----
    slab0 = read(a.slab)
    if a.cz > 0:                                    # extend vacuum so standing poses are image-clean
        cell = slab0.cell.array.copy(); cell[2, 2] = a.cz
        slab0.set_cell(cell); slab0.pbc = True
        print(f"c-axis -> {a.cz} A (vacuum above slab {a.cz - slab0.positions[:, 2].max():.1f} A)", flush=True)
    area = float(np.linalg.norm(np.cross(slab0.cell.array[0], slab0.cell.array[1])))
    if area < 1.0:                                  # a bare .xyz has NO cell -> degenerate -> garbage energies
        raise SystemExit(f"SLAB CELL DEGENERATE (in-plane area {area:.2f} A^2). Use a .vasp/.cif slab WITH a "
                         f"cell, NOT a bare .xyz.\ncell=\n{slab0.cell.array}")
    zs = slab0.positions[:, 2]
    if a.freeze_frac >= 1.0:
        fix = FixAtoms(indices=list(range(len(slab0))))     # freeze whole slab
    else:
        print(f"⚠ freeze_frac {a.freeze_frac} < 1.0 — 슬랩 일부가 UMA 로 움직인다. "
              "이 산출물은 Phase-B 좌표일치 assert 를 통과하지 못한다 (진단 전용).", flush=True)
        zcut = zs.min() + a.freeze_frac * (zs.max() - zs.min())
        fix = FixAtoms(indices=[i for i in range(len(slab0)) if slab0.positions[i, 2] < zcut])
    slab = slab0.copy()
    slab.set_constraint(fix)
    slab.calc = calc
    conv_slab = bool(FIRE(slab, logfile=None).run(fmax=a.fmax, steps=200))
    if a.freeze_frac >= 1.0 and not np.allclose(slab.positions, slab0.positions, atol=1e-8):
        raise SystemExit("⛔ 전체 고정인데 슬랩 좌표가 움직였다 — constraint 가 안 걸렸다")
    E_slab = slab.get_potential_energy()
    ztop = slab.positions[:, 2].max()
    print(f"E_slab = {E_slab:.4f} eV  (top z={ztop:.2f}, "
          f"{'frozen' if a.freeze_frac >= 1.0 else f'FIRE converged={conv_slab}'})", flush=True)

    pts = grid_points(slab.cell.array, a.grid[0], a.grid[1])
    rows = []
    for tag in a.tags:
        mol0 = read(os.path.join(a.moldir, f"sdcp_v7c_{tag}.xyz"))
        # gas reference (same setting; UMA has no charge/mult knob -> geometry-level ref)
        g = mol0.copy()
        g.center(vacuum=10.0)
        g.calc = calc
        conv_mol = bool(FIRE(g, logfile=None).run(fmax=a.fmax, steps=300))
        E_mol = g.get_potential_energy()
        print(f"[{tag}] E_mol = {E_mol:.4f} eV  (converged={conv_mol})", flush=True)
        if not conv_mol:
            print(f"  ⚠ {tag} 기체 참조가 미수렴 — 이 종의 모든 E_bind 가 오염된다. "
                  "steps 를 늘려 다시 돌 것.", flush=True)

        sS, sO, eth = find_groups(mol0)
        com = mol0.get_center_of_mass()
        heads = {
            "sulfonate_down": mol0.positions[sO].mean(axis=0) - com,
            "etherO_down":    mol0.positions[eth] - com,
            "chelation":      0.5 * (mol0.positions[sO].mean(axis=0) + mol0.positions[eth]) - com,
        }
        n_pose = len(heads) * len(a.rots) * len(pts)
        print(f"[{tag}] {len(heads)} orient x {len(a.rots)} rot x {len(pts)} grid = {n_pose} poses", flush=True)
        for oname, vec in heads.items():
            for rot in a.rots:
                for (gi, gj), xy in pts:
                    m = orient(mol0, vec)
                    m.rotate(rot, "z", center=m.get_center_of_mass())
                    m.positions[:, :2] += xy - m.get_center_of_mass()[:2]
                    m.positions[:, 2] += (ztop + a.gap) - m.positions[:, 2].min()
                    comp = slab.copy() + m
                    comp.set_constraint(fix)
                    comp.calc = calc
                    # ⚠ 수렴 bool 을 버리면 미수렴 자세가 랭킹에 올라 챔피언이 될 수 있다 (§2-10)
                    conv = bool(FIRE(comp, logfile=None).run(fmax=a.fmax, steps=a.steps))
                    E = comp.get_potential_energy()
                    eb = E - E_slab - E_mol
                    label = f"{tag}_{oname}_r{rot}_g{gi}{gj}"
                    write(os.path.join(a.out, f"complex_{label}.xyz"), comp)
                    rows.append((label, E, eb, conv))
                    print(f"  {label:40s} E_bind = {eb:+.3f} eV  {'' if conv else '⚠ NOT CONVERGED'}",
                          flush=True)

    with open(os.path.join(a.out, "phaseA_v7c_results.csv"), "w") as f:
        f.write("label,E_complex_eV,E_bind_eV,converged\n")
        for label, E, eb, conv in rows:
            f.write(f"{label},{E:.4f},{eb:.4f},{int(conv)}\n")
        f.write(f"# E_slab={E_slab:.4f} (shared); refs: gas-phase UMA relax per molecule; oc20\n")
        f.write("# converged=0 rows are EXCLUDED from ranking; rerun with more --steps if a low\n")
        f.write("# E_bind pose failed to converge. UMA absolute E_bind: ranking only, never quote.\n")

    ok = [r for r in rows if r[3]]
    bad = len(rows) - len(ok)
    best = sorted(ok, key=lambda r: r[2])
    print(f"\n=== ranking (converged only — {len(ok)}/{len(rows)}"
          + (f", {bad} unconverged EXCLUDED" if bad else "") + ") ===")
    for label, E, eb, _ in best[:8]:
        print(f"  {eb:+.3f} eV  {label}")
    print("→ 상위 3-5 자세를 **전부** Phase-B DFT+U 로 재채점한다 (챔피언 하나만 믿지 않는다)")
    print(f"saved: {a.out}/phaseA_v7c_results.csv")


if __name__ == "__main__":
    main()
