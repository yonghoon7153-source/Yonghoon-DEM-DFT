#!/usr/bin/env python3
"""vasp_to_cif.py — POSCAR/VASP → 최소 CIF (P1).

왜 필요한가: `voronoi_volume_disorder.py` 와 `b2o3_all_bond_lengths.py` 가 **CIF 만 읽는다**.
LPSOCl 은 .vasp/.xyz 만 있어서 그대로는 못 돌린다.

⚠ 대칭을 찾지 않는다. **P1 로 그대로 옮긴다** — relax 후 구조는 이상적 대칭이 이미 깨져 있고,
   대칭을 억지로 부여하면 우리가 재려는 **site disorder 자체를 지워버린다**
   (Voronoi std(V) 가 disorder 지표라는 게 이 파이프라인의 전제다).

  python3 tools/comp1_v3/vasp_to_cif.py in.vasp out.cif
"""
import math
import sys

import numpy as np


def read_poscar(fn):
    L = open(fn).read().splitlines()
    scale = float(L[1].split()[0])
    A = np.array([[float(x) for x in L[i].split()[:3]] for i in (2, 3, 4)]) * scale
    sp = L[5].split()
    cnt = [int(x) for x in L[6].split()]
    mode = L[7].strip().lower()
    if mode.startswith("s"):          # Selective dynamics
        mode = L[8].strip().lower()
        k = 9
    else:
        k = 8
    direct = mode.startswith("d")
    sym, pos = [], []
    for s, n in zip(sp, cnt):
        for _ in range(n):
            v = [float(x) for x in L[k].split()[:3]]
            pos.append(v)
            sym.append(s)
            k += 1
    P = np.array(pos)
    if not direct:                    # Cartesian → fractional
        P = P @ np.linalg.inv(A)
    return A, P % 1.0, sym


def cell_params(A):
    a, b, c = (np.linalg.norm(A[i]) for i in range(3))
    ang = lambda u, v: math.degrees(math.acos(
        float(np.dot(u, v)) / (np.linalg.norm(u) * np.linalg.norm(v))))
    return a, b, c, ang(A[1], A[2]), ang(A[0], A[2]), ang(A[0], A[1])


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, dst = sys.argv[1], sys.argv[2]
    A, frac, sym = read_poscar(src)
    a, b, c, al, be, ga = cell_params(A)
    cnt = {}
    # ⚠ **컬럼 순서·개수를 db/structures/b2o3_relaxV0.cif 와 정확히 맞춘다.**
    #   voronoi_volume_disorder.py 는 줄에서 **마지막 3개 소수**를 좌표로 집고,
    #   b2o3_all_bond_lengths.py 는 **t[1] 을 원소기호, t[2:5] 를 좌표**로 읽는다.
    #   → occupancy 열을 붙이면 좌표가 한 칸 밀려 **조용히 틀린 값**이 나오고
    #     (실제로 겪음: Voronoi 합이 셀부피 대비 +2.6%),
    #     label 을 먼저 안 쓰면 원소기호가 'Li1' 로 읽혀 **모든 결합 탐색이 0건**이 된다.
    #   occupancy 는 넣지 않는다. 형식: `Li1   Li  x y z`
    lines = [
        f"# generated from {src} by tools/comp1_v3/vasp_to_cif.py",
        "# P1 — 대칭을 찾지 않는다 (site disorder 를 지우지 않기 위해)",
        "# 컬럼 순서는 b2o3_relaxV0.cif 와 동일 (occupancy 열 없음 — 파서가 좌표를 밀린다)",
        f"data_{__import__('os').path.basename(src).rsplit('.',1)[0]}",
        f"_cell_length_a    {a:.6f}", f"_cell_length_b    {b:.6f}", f"_cell_length_c    {c:.6f}",
        f"_cell_angle_alpha {al:.6f}", f"_cell_angle_beta  {be:.6f}",
        f"_cell_angle_gamma {ga:.6f}",
        "_space_group_name_H-M_alt 'P 1'", "_space_group_IT_number 1",
        "", "loop_", " _atom_site_label", " _atom_site_type_symbol",
        " _atom_site_fract_x", " _atom_site_fract_y", " _atom_site_fract_z",
    ]
    for sy, f in zip(sym, frac):
        cnt[sy] = cnt.get(sy, 0) + 1
        lines.append(f"{sy}{cnt[sy]}".ljust(6)
                     + f"{sy} {f[0]:.6f} {f[1]:.6f} {f[2]:.6f}")
    open(dst, "w").write("\n".join(lines) + "\n")
    print(f"{src} → {dst}   {len(sym)} atoms  "
          f"a,b,c = {a:.4f},{b:.4f},{c:.4f}  α,β,γ = {al:.2f},{be:.2f},{ga:.2f}")


if __name__ == "__main__":
    main()
