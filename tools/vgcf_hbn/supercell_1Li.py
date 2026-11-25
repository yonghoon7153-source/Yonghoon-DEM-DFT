#!/usr/bin/env python3
"""supercell_1Li.py — 큐브(완화 좌표) -> 면내 nx×ny 슈퍼셀, Li는 딱 1개 (넓은 시트 그림용).

VESTA Boundary는 Li도 n^2개로 복제됨 -> 이건 시트(B/N/C)만 타일링하고 Li 1개만 남겨 중앙 배치.
슬래브라 면내(a1,a2)만 확장, z(진공)는 그대로. 완화 dimple 보존(면내 랩만, Li는 랩 제외).
Li와 그 dimple은 같은 면내 위치라 같은 shift를 받아 중앙에서 정렬됨.

  python3 supercell_1Li.py Li_on_hbn_2L_cdd.cube --nx 3 --ny 3
  -> Li_on_hbn_2L_cdd_3x3_1Li.vasp / .xyz  (VESTA에서 바로 열림, Boundary 불필요)
"""
import argparse, os
import numpy as np

BOHR = 0.529177210903
ZSYM = {3: "Li", 5: "B", 6: "C", 7: "N", 8: "O", 15: "P", 16: "S", 17: "Cl", 35: "Br"}


def read_cube_header(path):
    with open(path) as f:
        f.readline(); f.readline()
        nat, *o = f.readline().split(); nat = int(nat); origin = np.array(o, float)
        vecs, ns = [], []
        for _ in range(3):
            n, *v = f.readline().split(); ns.append(int(n)); vecs.append([float(x) for x in v])
        vecs = np.array(vecs); ns = np.array(ns)
        at = []
        for _ in range(nat):
            z, q, x, y, zc = f.readline().split(); at.append((int(z), float(x), float(y), float(zc)))
    return (vecs.T * ns).T, origin, at          # cell(Bohr), origin(Bohr), atoms(Bohr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cube")
    ap.add_argument("--nx", type=int, default=3)
    ap.add_argument("--ny", type=int, default=3)
    ap.add_argument("--no-center", action="store_true", help="Li 중앙정렬/랩 끔 (Li가 모서리)")
    a = ap.parse_args()

    cell_b, origin_b, at = read_cube_header(a.cube)
    A = cell_b * BOHR; a1, a2, a3 = A[0], A[1], A[2]
    sym = [ZSYM.get(z, "X") for z, _, _, _ in at]
    P = np.array([(np.array([x, y, zc]) - origin_b) * BOHR for _, x, y, zc in at])
    li = [i for i, s in enumerate(sym) if s == "Li"]
    if not li:
        raise SystemExit("Li 없음 — 이 큐브엔 Li가 없어")
    if len(li) > 1:
        print(f"주의: Li {len(li)}개 발견 -> 첫 개만 유지")
    li = li[0]; sheet = [i for i in range(len(sym)) if i != li]

    B = np.array([a1 * a.nx, a2 * a.ny, a3])     # 면내만 확장
    osym, opos = [], []
    for i in range(a.nx):
        for j in range(a.ny):
            sh = i * a1 + j * a2
            for k in sheet:
                osym.append(sym[k]); opos.append(P[k] + sh)
    osym.append("Li"); opos.append(P[li].copy())  # Li는 항상 마지막(=opos[-1])
    opos = np.array(opos)

    if not a.no_center:                           # Li를 박스 면내 중앙으로 + 시트 면내 랩(Li 제외)
        c = 0.5 * (B[0] + B[1]); d = c - opos[-1]; d[2] = 0.0
        opos = opos + d
        M = np.array([B[0][:2], B[1][:2]]); Mi = np.linalg.inv(M)
        for t in range(len(opos) - 1):            # 마지막(Li)은 랩 안 함
            fr = opos[t, :2] @ Mi; fr -= np.floor(fr); opos[t, :2] = fr @ M

    els = sorted(set(osym), key=lambda s: (s == "Li", s))   # Li 맨 뒤
    idx = [i for e in els for i in range(len(osym)) if osym[i] == e]
    osym = [osym[i] for i in idx]; opos = opos[idx]
    cnt = [osym.count(e) for e in els]

    base = os.path.splitext(a.cube)[0] + f"_{a.nx}x{a.ny}_1Li"
    with open(base + ".vasp", "w") as f:
        f.write(f"{os.path.basename(base)}  (nx{a.nx} ny{a.ny}, 1 Li on wide sheet)\n1.0\n")
        for v in B:
            f.write(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}\n")
        f.write("  " + "  ".join(els) + "\n  " + "  ".join(map(str, cnt)) + "\nCartesian\n")
        for p in opos:
            f.write(f"  {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}\n")
    with open(base + ".xyz", "w") as f:
        f.write(f"{len(osym)}\n{os.path.basename(base)}\n")
        for s, p in zip(osym, opos):
            f.write(f"{s:2s} {p[0]:14.8f} {p[1]:14.8f} {p[2]:14.8f}\n")
    print(f"-> {base}.vasp / .xyz   ({len(osym)} atoms = {dict(zip(els, cnt))})")
    print(f"   cell {np.linalg.norm(B, axis=1).round(2)} A | Li 1개(중앙), 시트 {a.nx}x{a.ny} 타일")


if __name__ == "__main__":
    main()
