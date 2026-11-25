#!/usr/bin/env python3
"""build_li_interface.py — electrolyte | Li-metal interface slab for MLIP-MD.

Builds a coherent (lateral-commensurate) SE|Li slab: reorients the electrolyte so
its a,b lattice vectors lie in the xy-plane, flattens c to an orthogonal slab axis
(vacuum), then fills a Li-metal reservoir (bcc, tiled & cropped to the a,b footprint)
on top with a small initial gap. Bottom SE layers are FixAtoms-frozen to mimic bulk.

Purpose: watch (with UMA MLIP MD, NO DFT) whether Li reduces the SE at the interface
-> P-S bond breaking, Li2S/Li3P (and, for b2o3, metallic LiB) formation. Confirms /
quantifies the *thermodynamic* prediction (b2o3 worse at bare Li metal via LiB) with
actual *dynamics/morphology* that the equilibrium calc could not give.

Runs on kgy (uma env has ASE). Output = interface_<label>_Li.xyz + a geometry report.

  python3 tools/oxidation/build_li_interface.py \
    --electrolyte db/structures/modelc_V0_k663.xyz --label modelc \
    --li_thickness 14 --out interface_modelc_Li.xyz

--sandwich 판 (2026-11-17 · [혁주] MD-0 · 카드 db/properties/hyeokju_lzo_md_card_2026_11_16.json ⏩_개정_1):
  슬랩 (면내 a·b · c 는 z 축) 위 틈에 조성 블록을 **무작위로** 놓아 주기 샌드위치 (진공 없음 · 계면 둘) 를 만든다.
    c = 슬랩 두께 + 틈 + 블록 두께 + 틈 · 블록 두께 = (블록 질량 / 밀도) / 면적
    원자마다 [슬랩 위 + 틈, + 블록 두께) 에서 무작위 자리를 뽑고, 최종 셀의 3D 최소상 거리로 모든 원자와
    --min_dist 이상이면 받는다 · 못 놓으면 **거부한다** (원자를 빼거나 거리를 줄이지 않는다)
  산출: <out>.xyz (extxyz) + <out>.vasp (VESTA 규율: xyz + POSCAR 쌍) + <out>_freeze.json (슬랩 인덱스 = 담금질 동안 고정)
        + <out>_manifest.json (조성 · 두께 · c · 밀도 · 실제 최소 거리 · 시드 · 슬랩 sha256)
    python3 tools/oxidation/build_li_interface.py --sandwich <slab.vasp> --block "Li:32,Zr:16,O:48" \
        --block_density 4.0 --gap 2.0 --min_dist 1.6 --seed 20261117 --out <이름>
  ⛔ --sandwich 가 못 하는 것: 블록 구조를 만들지 않는다 (무작위 배치일 뿐 — 녹였다 식히는 것은 run_li_interface_md.py) ·
     슬랩 a·b 가 면내가 아니거나 c 가 z 축이 아니면 거부한다 (기울어진 셀을 돌려 맞추지 않는다) · 슬랩 원자끼리의
     거리는 안 본다 (슬랩은 빌더가 검증했다) · 밀도가 물리적으로 맞는지 모른다 (카드가 정한다)
  python3 tools/oxidation/build_li_interface.py --selftest
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np
from ase import Atoms
from ase.io import read, write
from ase.geometry.cell import cellpar_to_cell
from ase.constraints import FixAtoms

A_LI = 3.51            # bcc Li lattice const (A)  -> n_Li = 2/a^3 = 0.0463 /A^3


def reorient_ab_inplane(atoms):
    """Pure rotation to standard orientation: a||x, b in xy-plane (b_z=0), c tilted.
    Structure unchanged (fractional coords preserved)."""
    frac = atoms.get_scaled_positions(wrap=True)
    atoms.set_cell(cellpar_to_cell(atoms.cell.cellpar()), scale_atoms=False)
    atoms.set_scaled_positions(frac)
    return atoms


def fill_li_bcc(a_vec, b_vec, z0, z1):
    """Tile bcc Li over the xy bounding box, keep atoms with a,b-fractional in [0,1)
    and z in [z0,z1). a_vec,b_vec are in the xy-plane after reorientation."""
    a2d = np.array([a_vec[:2], b_vec[:2]])          # rows = a_xy, b_xy
    Minv = np.linalg.inv(a2d.T)                     # cols of a2d.T = a,b
    corners = np.array([[0, 0], a_vec[:2], b_vec[:2], a_vec[:2] + b_vec[:2]])
    (xmin, ymin), (xmax, ymax) = corners.min(0) - A_LI, corners.max(0) + A_LI
    basis = [(0, 0, 0), (0.5, 0.5, 0.5)]
    pos = []
    for i in range(int(np.floor(xmin / A_LI)) - 1, int(np.ceil(xmax / A_LI)) + 2):
        for j in range(int(np.floor(ymin / A_LI)) - 1, int(np.ceil(ymax / A_LI)) + 2):
            for k in range(int(np.floor(z0 / A_LI)) - 1, int(np.ceil(z1 / A_LI)) + 2):
                for bx, by, bz in basis:
                    x, y, z = (i + bx) * A_LI, (j + by) * A_LI, (k + bz) * A_LI
                    if not (z0 <= z < z1):
                        continue
                    f1, f2 = Minv @ np.array([x, y])
                    if 0 <= f1 < 1 and 0 <= f2 < 1:
                        pos.append([x, y, z])
    return np.array(pos)


AMU_PER_A3_TO_GCC = 1.66053906660          # 1 amu/Å³ = 1.66054 g/cm³


def parse_counts(s):
    """'Li:32,Zr:16,O:48' → {'Li': 32, ...} · 원소 기호 · 양의 정수가 아니면 ValueError."""
    from ase.data import atomic_numbers
    out = {}
    for tok in str(s).split(","):
        p = [x.strip() for x in tok.split(":")]
        if len(p) != 2 or p[0] not in atomic_numbers or not p[1].isdigit() or int(p[1]) <= 0 or p[0] in out:
            raise ValueError(f"⛔ 블록 조성 조각을 못 읽었다: {tok!r} (원소:양의 정수 · 원소는 한 번씩)")
        out[p[0]] = int(p[1])
    return out


def build_sandwich(slab, counts, density_gcc, gap=2.0, min_dist=1.6, seed=20261117, max_tries=20000):
    """슬랩 + 무작위 블록 주기 샌드위치 → (atoms, manifest). 못 놓으면 ValueError (원자를 빼지 않는다)."""
    from ase.data import atomic_masses, atomic_numbers
    from ase.geometry import get_distances
    cell = np.asarray(slab.cell.array, float)
    if np.abs(cell[0, 2]) > 1e-6 or np.abs(cell[1, 2]) > 1e-6 or np.abs(cell[2, :2]).max() > 1e-6:
        raise ValueError("⛔ 슬랩 셀의 a·b 가 면내 (z 성분 0) 이고 c 가 z 축이어야 한다 — 기울어진 셀은 돌려 맞추지 않는다")
    if density_gcc <= 0 or gap < 0 or min_dist <= 0:
        raise ValueError("⛔ 밀도 · 최소 거리는 양수 · 틈은 0 이상이어야 한다")
    a_vec, b_vec = cell[0], cell[1]
    area = float(np.linalg.norm(np.cross(a_vec, b_vec)))
    pos_s = slab.get_positions().copy()
    pos_s[:, 2] -= pos_s[:, 2].min()
    t_s = float(pos_s[:, 2].max())
    mass = sum(n * atomic_masses[atomic_numbers[el]] for el, n in counts.items())
    t_b = float(mass * AMU_PER_A3_TO_GCC / density_gcc / area)
    c = t_s + gap + t_b + gap
    new_cell = np.array([a_vec, b_vec, [0.0, 0.0, c]])
    rng = np.random.default_rng(seed)
    syms = [el for el, n in counts.items() for _ in range(n)]
    syms = [syms[i] for i in rng.permutation(len(syms))]
    placed = [p for p in pos_s]
    z0 = t_s + gap
    for el in syms:
        for _ in range(max_tries):
            u, v, w = rng.random(3)
            p = u * a_vec + v * b_vec + np.array([0.0, 0.0, z0 + w * t_b])
            _, d = get_distances(p[None, :], np.array(placed), cell=new_cell, pbc=True)
            if d.min() >= min_dist:
                placed.append(p)
                break
        else:
            raise ValueError(f"⛔ {el} 를 놓을 자리를 {max_tries} 번 만에 못 찾았다 ({len(placed) - len(slab)}/{len(syms)} 놓음) — "
                             "밀도 · 최소 거리 · 틈을 카드에서 다시 정한다 (원자를 빼지 않는다)")
    out = Atoms(symbols=list(slab.get_chemical_symbols()) + syms, positions=np.array(placed), cell=new_cell, pbc=True)
    nb = len(syms)
    _, D = get_distances(out.positions[len(slab):], out.positions, cell=new_cell, pbc=True)
    for i in range(nb):
        D[i, len(slab) + i] = np.inf
    dmin = float(D.min())
    if dmin < min_dist - 1e-9:
        raise ValueError(f"⛔ 블록 원자 최소 거리 {dmin:.3f} Å < {min_dist} — 배치 검사 실패")
    zb = out.positions[len(slab):, 2]
    man = {"n_slab": len(slab), "n_block": nb, "n_total": len(out), "formula": out.get_chemical_formula(),
           "block_counts": counts, "block_density_gcc": density_gcc, "block_mass_amu": round(mass, 4),
           "area_A2": round(area, 4), "t_slab_A": round(t_s, 4), "t_block_A": round(t_b, 4), "gap_A": gap,
           "c_A": round(c, 4), "min_dist_A": min_dist, "min_dist_block_achieved_A": round(dmin, 4),
           "block_z_range_A": [round(float(zb.min()), 4), round(float(zb.max()), 4)], "seed": seed,
           "freeze_idx": list(range(len(slab))),
           "⚠": "블록은 무작위 배치다 — 구조가 아니다. 녹였다 식히는 것은 run_li_interface_md.py --schedule"}
    return out, man


def selftest():
    res = []

    def chk(name, cond):
        res.append(bool(cond)); print(("  ✓ " if cond else "  ✗ ") + name)

    def refused(fn, why=""):
        """ValueError 로 거부했고, 이유 글귀 (why) 가 있으면 그 글귀까지 맞아야 참 — 다른 곳의 오류로 '거부' 를 세지 않는다."""
        try:
            fn()
        except ValueError as e:
            return why in str(e)
        return False

    g = np.mgrid[0:3, 0:3, 0:2].reshape(3, -1).T * 3.0
    slab = Atoms(["Li"] * len(g), positions=g + [0.5, 0.5, 1.0], cell=[9.0, 9.0, 6.0], pbc=True)
    cnt = parse_counts("Zr:4,O:8")
    out, man = build_sandwich(slab, cnt, 4.0, gap=2.0, min_dist=1.6, seed=1)
    chk("양성: 조성 = 슬랩 + 블록", man["n_total"] == len(slab) + 12 and out.get_chemical_symbols().count("Zr") == 4)
    chk("양성: c = 슬랩 두께 + 틈 + 블록 두께 + 틈", abs(man["c_A"] - (man["t_slab_A"] + 4.0 + man["t_block_A"])) < 1e-3)
    from ase.data import atomic_masses, atomic_numbers
    m = 4 * atomic_masses[atomic_numbers["Zr"]] + 8 * atomic_masses[atomic_numbers["O"]]
    chk("양성: 블록 두께 = 질량 / 밀도 / 면적", abs(man["t_block_A"] - m * 1.66053906660 / 4.0 / 81.0) < 1e-3)
    chk("양성: 블록 원자는 [슬랩 위 + 틈, + 블록 두께) 안", man["block_z_range_A"][0] >= man["t_slab_A"] + 2.0 - 1e-9
        and man["block_z_range_A"][1] < man["t_slab_A"] + 2.0 + man["t_block_A"] + 1e-9)
    chk("양성: 실제 최소 거리 ≥ min_dist (주기 최소상)", man["min_dist_block_achieved_A"] >= 1.6)
    chk("양성: 고정 목록 = 슬랩 인덱스", man["freeze_idx"] == list(range(len(slab))))
    # 빌더가 잰 값이 아니라 **따로** 잰다 — 틈 0 으로 위쪽 주기상 (다음 칸 슬랩 바닥) 바로 밑까지 블록을 채운다
    o0, m0 = build_sandwich(slab, parse_counts("Zr:6,O:12"), 4.0, gap=0.0, min_dist=1.8, seed=3)
    Dm = o0.get_all_distances(mic=True)[len(slab):]
    for i in range(Dm.shape[0]):
        Dm[i, len(slab) + i] = np.inf
    chk("양성: 틈 0 에서도 블록 원자 – 모든 원자 (주기상 포함) 최소 거리 ≥ 1.8 Å (ASE mic 로 따로 잼)", float(Dm.min()) >= 1.8 - 1e-9)
    out2, _ = build_sandwich(slab, cnt, 4.0, gap=2.0, min_dist=1.6, seed=1)
    out3, _ = build_sandwich(slab, cnt, 4.0, gap=2.0, min_dist=1.6, seed=2)
    chk("양성: 같은 시드 → 같은 배치 · ⛔음성: 다른 시드 → 다른 배치",
        np.allclose(out.positions, out2.positions) and not np.allclose(out.positions, out3.positions))
    chk("⛔음성: 못 놓는 거리 (min_dist 4 Å) → '놓을 자리' 로 거부 (원자를 빼지 않는다)",
        refused(lambda: build_sandwich(slab, cnt, 4.0, gap=2.0, min_dist=4.0, seed=1, max_tries=300), "놓을 자리를"))
    tilt = slab.copy(); tilt.set_cell([[9.0, 0, 0], [0, 9.0, 0], [1.0, 0, 6.0]])
    chk("⛔음성: c 가 z 축이 아니면 거부", refused(lambda: build_sandwich(tilt, cnt, 4.0), "z 축"))
    chk("⛔음성: 블록 조성 못 읽음 (원소 아님 · 0 · 중복) → 거부",
        refused(lambda: parse_counts("Xx:3")) and refused(lambda: parse_counts("Zr:0"))
        and refused(lambda: parse_counts("Zr:2,Zr:1")) and refused(lambda: parse_counts("Zr2")))
    chk("⛔음성: 밀도 0 → 거부", refused(lambda: build_sandwich(slab, cnt, 0.0)))
    # 주기 최소상: 블록 맨 위 원자와 다음 칸 슬랩 바닥 사이도 거리 검사에 들어가는가 (틈 0 · 거리 크게 → 거부되어야 한다)
    chk("⛔음성: 틈 0 이면 위쪽 주기상 (다음 칸 슬랩) 과도 거리를 잰다 → 촘촘하면 거부",
        refused(lambda: build_sandwich(slab, parse_counts("Zr:60"), 9.0, gap=0.0, min_dist=2.5, seed=1, max_tries=300)))
    n_bad = len(res) - sum(res)
    print(f"selftest: {sum(res)} 통과 / {n_bad} 실패")
    return 0 if n_bad == 0 else 1


def main_sandwich(a):
    slab = read(a.sandwich)
    counts = parse_counts(a.block)
    out, man = build_sandwich(slab, counts, a.block_density, gap=a.gap_sandwich, min_dist=a.min_dist, seed=a.seed)
    base = a.out or "sandwich"
    base = base[:-4] if base.endswith(".xyz") else base
    write(base + ".xyz", out, format="extxyz")
    write(base + ".vasp", out, format="vasp", direct=True, sort=False)
    with open(base + "_freeze.json", "w", encoding="utf-8") as f:
        json.dump({"freeze_idx": man["freeze_idx"], "why": "슬랩 원자 — 블록을 녹였다 식히는 동안 고정"}, f)
    man["slab"] = {"path": a.sandwich, "sha256": hashlib.sha256(open(a.sandwich, "rb").read()).hexdigest(),
                   "formula": slab.get_chemical_formula()}
    man["files"] = [base + ".xyz", base + ".vasp", base + "_freeze.json"]
    with open(base + "_manifest.json", "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
    print(f"✓ {man['formula']} · {man['n_total']} 원자 (슬랩 {man['n_slab']} + 블록 {man['n_block']}) · c {man['c_A']:.2f} Å · "
          f"블록 {man['t_block_A']:.2f} Å · 최소 거리 {man['min_dist_block_achieved_A']:.2f} Å → {base}.xyz · .vasp · _freeze.json · _manifest.json")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sandwich", help="슬랩 구조 파일 (.vasp) → 슬랩 + 무작위 블록 주기 샌드위치")
    ap.add_argument("--block", help="--sandwich 블록 조성 (예 Li:32,Zr:16,O:48)")
    ap.add_argument("--block_density", type=float, default=4.0, help="--sandwich 블록 밀도 [g/cm³]")
    ap.add_argument("--gap_sandwich", type=float, default=2.0, help="--sandwich 계면 틈 [Å] (두 계면 같다)")
    ap.add_argument("--min_dist", type=float, default=1.6, help="--sandwich 블록 원자 최소 거리 [Å]")
    ap.add_argument("--seed", type=int, default=20261117, help="--sandwich 배치 시드")
    ap.add_argument("--electrolyte")
    ap.add_argument("--label")
    ap.add_argument("--li_thickness", type=float, default=14.0, help="Li reservoir thickness (A)")
    ap.add_argument("--gap", type=float, default=2.2, help="initial SE-Li gap (A)")
    ap.add_argument("--vac_bottom", type=float, default=2.0)
    ap.add_argument("--vac_top", type=float, default=12.0)
    ap.add_argument("--fix_bottom", type=float, default=6.0, help="freeze SE atoms within this many A of the bottom")
    ap.add_argument("--supercell", type=int, nargs=2, default=[1, 1], help="lateral repeat of SE (a b) before building")
    ap.add_argument("--roll_c", type=float, default=0.0,
                    help="roll SE along c (fractional, periodic) BEFORE cleaving -> selects which layer sits at the exposed top (e.g. 0.51 exposes B in b2o3_relaxV0)")
    ap.add_argument("--shift_ab", type=float, nargs=2, default=[0.0, 0.0],
                    help="lateral fractional shift (registry scan vs the Li slab)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.sandwich:
        if not a.block:
            ap.error("--sandwich 는 --block 이 필요하다")
        return main_sandwich(a)
    if not (a.electrolyte and a.label):
        ap.error("--electrolyte 와 --label 이 필요하다 (또는 --sandwich · --selftest)")

    se = read(a.electrolyte)
    if a.supercell != [1, 1]:
        se = se.repeat((a.supercell[0], a.supercell[1], 1))
    if a.roll_c or any(a.shift_ab):
        f = se.get_scaled_positions()
        f[:, 2] = (f[:, 2] + a.roll_c) % 1.0
        f[:, 0] = (f[:, 0] + a.shift_ab[0]) % 1.0
        f[:, 1] = (f[:, 1] + a.shift_ab[1]) % 1.0
        se.set_scaled_positions(f)
    se = reorient_ab_inplane(se)
    se.positions[:, 2] += a.vac_bottom - se.positions[:, 2].min()     # sit SE at z=vac_bottom
    zmax = se.positions[:, 2].max()
    ssym = np.array(se.get_chemical_symbols())
    for el in ("B", "O", "P"):                       # who is actually at the Li contact?
        if (ssym == el).any():
            dep = np.sort(zmax - se.positions[ssym == el, 2])
            print(f"  {el} depth below exposed top (A): {np.round(dep, 1)}"
                  + ("   <-- SURFACE-EXPOSED" if dep[0] < 3.0 else ""))
    a_vec, b_vec = se.cell[0], se.cell[1]

    z0, z1 = zmax + a.gap, zmax + a.gap + a.li_thickness
    li_pos = fill_li_bcc(a_vec, b_vec, z0, z1)
    Ztot = z1 + a.vac_top

    combined = se + Atoms(["Li"] * len(li_pos), positions=li_pos)
    combined.set_cell(np.array([a_vec, b_vec, [0, 0, Ztot]]))
    combined.pbc = [True, True, True]
    zc = combined.positions[:, 2]
    mask = [(i < len(se)) and (zc[i] < a.vac_bottom + a.fix_bottom) for i in range(len(combined))]
    combined.set_constraint(FixAtoms(mask=mask))

    out = a.out or f"interface_{a.label}_Li.xyz"
    write(out, combined)

    area = np.linalg.norm(np.cross(a_vec, b_vec))
    dens = len(li_pos) / (area * a.li_thickness)
    print(f"[{a.label}] SE={len(se)}  Li={len(li_pos)}  total={len(combined)}  fixed_bottom={sum(mask)}")
    print(f"  lateral |a|={np.linalg.norm(a_vec):.3f} |b|={np.linalg.norm(b_vec):.3f}  area={area:.1f} A^2")
    print(f"  SE z-span={zmax - a.vac_bottom:.1f} A | Li {z0:.1f}-{z1:.1f} A (thick {a.li_thickness}) | cell Z={Ztot:.1f}")
    print(f"  Li number density={dens:.4f}/A^3  (bulk bcc target 0.0463; relax/MD will settle it)")
    print(f"  -> {out}   [VESTA it: SE slab at bottom (frozen layer), Li reservoir on top, vacuum above]")
    if abs(dens - 0.0463) / 0.0463 > 0.15:
        print(f"  !! Li density off by >15% from bulk — check li_thickness / cropping.")


if __name__ == "__main__":
    sys.exit(main())
