#!/usr/bin/env python3
"""cube_to_vesta_cdd.py — CDD Gaussian cube -> .vesta 페어 (이중 등가면: 노랑 축적 / 청록 결핍).

VESTA에서 열면 Liu2022 (f)(g) 양식: 노랑=전자 축적(받개), 청록=결핍(Li+).
cube 헤더에서 셀·원자를 읽어 .vesta 생성 (ASCII+CRLF, cube를 IMPORT_DENSITY로 참조).
.vesta는 밀도를 품지 않고 cube를 가리키므로 둘을 같은 폴더에 둘 것.

  python3 cube_to_vesta_cdd.py Li_on_hbn_2L_cdd.cube [--iso 0.003]
  -> Li_on_hbn_2L_cdd.vesta  (같은 폴더, cube 파일명 참조)
"""
import argparse, os
import numpy as np

BOHR = 0.529177210903
ZSYM = {3: "Li", 5: "B", 6: "C", 7: "N", 8: "O", 15: "P", 16: "S", 17: "Cl", 35: "Br", 53: "I"}
# VESTA 표준 원소색 (elements.ini) + 공유결합 반지름 → VASP 열었을 때와 동일한 외형
COL = {"Li": ("1.2800", "204 128 255 204 128 255"), "B": ("0.8400", "255 181 181 255 181 181"),
       "C": ("0.7600", "128 128 128 90 90 90"),     "N": ("0.7100", " 48  80 248  48  80 248"),
       "O": ("0.6600", "255  13  13 254 3 0"),       "P": ("1.0600", "255 128  0 204 191 224"),
       "S": ("1.0500", "255 255  48 255 250 0"),     "Cl": ("1.0200", " 31 240  31 49 252 2"),
       "Br": ("1.2000", "166  41  41 200 60 60"),     "I": ("1.3900", "148   0 148 130 0 130")}

# argyrodite 결합/다면체 — P중심 PS4·PO4 사면체는 polyhedra(poly=1), Li–음이온 배위는 stick(poly=0)
# max 거리는 argyrodite 표준 결합상한 (Å); poly=1이면 그 중심원자로 다면체 렌더
BONDPAIRS = [
    ("P", "S", 2.35, 1), ("P", "O", 1.95, 1),
    ("Li", "S", 3.00, 0), ("Li", "Cl", 3.10, 0), ("Li", "Br", 3.25, 0),
    ("Li", "I", 3.40, 0), ("Li", "O", 2.70, 0),
]


def make_sbond(syms):
    """등장 원소에 맞는 SBOND 섹션. VESTA 필드: id A B min max search(0) boundary(1)
    show_polyhedra search_by(0) style(1=stick) radius width R G B."""
    s = set(syms); out = []; n = 0
    for A, B, mx, poly in BONDPAIRS:
        if A in s and B in s:
            n += 1
            out.append(f"  {n}  {A:>3s}  {B:>3s}    0.00000  {mx:8.5f}  0  1  {poly}  0  1  0.000  0.000 127 127 127")
    out.append("  0 0 0 0")
    return "\n".join(out)


def read_cube_header(path):
    with open(path) as f:
        f.readline(); f.readline()
        nat, *o = f.readline().split(); nat = int(nat); origin = np.array(o, float)
        vecs, ns = [], []
        for _ in range(3):
            n, *v = f.readline().split(); ns.append(int(n)); vecs.append([float(x) for x in v])
        vecs = np.array(vecs); ns = np.array(ns)
        atoms = []
        for _ in range(nat):
            z, q, x, y, zc = f.readline().split()
            atoms.append((int(z), float(x), float(y), float(zc)))
    cell = (vecs.T * ns).T          # 각 축 = n_i * v_i (Bohr)
    return cell, origin, atoms, vecs, ns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cube")
    ap.add_argument("--iso", type=float, default=0.0, help="등가면 절대값 (0=자동 ~max/3)")
    ap.add_argument("--maxabs", type=float, default=0.0, help="cube 최대|Δρ| (자동iso용; 로그의 range로)")
    ap.add_argument("--structure-only", action="store_true", help="밀도/등가면 빼고 순수 구조 vesta")
    a = ap.parse_args()
    cell_b, origin_b, atoms, vecs, ns = read_cube_header(a.cube)
    cell = cell_b * BOHR            # Angstrom
    L = np.linalg.norm(cell, axis=1)
    ang = lambda u, v: np.degrees(np.arccos(np.dot(u, v) / (np.linalg.norm(u)*np.linalg.norm(v))))
    al, be, ga = ang(cell[1], cell[2]), ang(cell[0], cell[2]), ang(cell[0], cell[1])
    iso = a.iso if a.iso > 0 else (a.maxabs/3 if a.maxabs > 0 else 0.003)

    # 원자 (분율 좌표, Bohr->frac via cell_b)
    inv = np.linalg.inv(cell_b)
    from collections import Counter
    cnt = Counter(); struc = []; sitet = []; theri = []; atomt = {}
    for i, (z, x, y, zc) in enumerate(atoms, 1):
        s = ZSYM.get(z, "X"); cnt[s] += 1; lb = f"{s}{cnt[s]}"
        fr = (np.array([x, y, zc]) - origin_b) @ inv
        struc.append(f"{i:3d} {s:>2s} {lb:>8s}  1.0000 {fr[0]:11.6f} {fr[1]:11.6f} {fr[2]:11.6f}    1        -")
        struc.append("                            0.000000   0.000000   0.000000  0.00")
        r, c = COL.get(s, ("0.5", "150 150 150 150 150 150")); sitet.append(f"{i:3d} {lb:>8s}  {r} {c}  50  0")
        theri.append(f"{i:3d} {lb:>8s}  0.000000"); atomt[s] = (r, c)
    cube_name = os.path.basename(a.cube)
    atomt_lines = "\n".join(f"  {j+1} {s:>2s}  {COL.get(s,('0.5','150 150 150 150 150 150'))[0]} "
                            f"{COL.get(s,('0.5','150 150 150 150 150 150'))[1]}  50" for j, s in enumerate(atomt))

    dens = "" if a.structure_only else f"\nIMPORT_DENSITY 1\n+1.000000 {cube_name}\n"
    isurf = "" if a.structure_only else (
        f"ISURF\n  1   0  {iso:.5f} 255 255   0 127 255\n"
        f"  2   0  {-iso:.5f}   0 255 255 127 255\n  0   0   0   0\n")
    ttl = f"{cube_name} structure only" if a.structure_only \
        else f"{cube_name} CDD (yellow=accumulation / cyan=depletion)"
    v = f"""#VESTA_FORMAT_VERSION 3.5.4

CRYSTAL

TITLE
{ttl}
{dens}
GROUP
1 1 P 1
CELLP
  {L[0]:.6f}   {L[1]:.6f}   {L[2]:.6f}  {al:.6f}  {be:.6f}  {ga:.6f}
  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
STRUC
{chr(10).join(struc)}
  0 0 0 0 0 0 0
THERI 1
{chr(10).join(theri)}
  0 0 0
SHAPE
  0       0       0       0   0.000000  0   192   192   192   192
BOUND
       0        1         0        1         0        1
  0   0   0   0  0
SBOND
{make_sbond(atomt)}
SITET
{chr(10).join(sitet)}
  0 0 0 0 0 0
ATOMT
{atomt_lines}
  0 0 0 0 0 0
STYLE
DISPF 37753794
MODEL   2  1  0
SURFS   0  1  1
SECTS  32  1
ATOMS   0  0  1
BONDS   1
POLYS   1
{isurf}BKGRC
 255 255 255
"""
    outp = os.path.splitext(a.cube)[0] + ("_structure.vesta" if a.structure_only else ".vesta")
    assert all(ord(ch) < 128 for ch in v), "non-ASCII"
    open(outp, "w", newline="").write(v.replace("\n", "\r\n"))
    tag = "구조 only" if a.structure_only else f"iso ±{iso:.4f}"
    print(f"-> {outp}  ({tag}, {len(atoms)} atoms)")
    print(f"   cell {L.round(2)} A  {len(atoms)} atoms  (cube와 같은 폴더에 둘 것)")


if __name__ == "__main__":
    main()
