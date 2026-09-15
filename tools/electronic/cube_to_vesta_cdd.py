#!/usr/bin/env python3
"""cube_to_vesta_cdd.py — cube/POSCAR -> .vesta (CDD 이중 등가면 또는 순수 구조).

VESTA에서 열면 Liu2022 (f)(g) 양식: 노랑=전자 축적(받개), 청록=결핍(Li+).
cube 헤더에서 셀·원자를 읽어 .vesta 생성 (ASCII+CRLF, cube를 IMPORT_DENSITY로 참조).
.vesta는 밀도를 품지 않고 cube를 가리키므로 둘을 같은 폴더에 둘 것.

  python3 cube_to_vesta_cdd.py Li_on_hbn_2L_cdd.cube [--iso 0.003]
  -> Li_on_hbn_2L_cdd.vesta  (같은 폴더, cube 파일명 참조)

  python3 cube_to_vesta_cdd.py --poscar static/POSCAR --out x.vesta
  -> 밀도 없는 **구조 전용** vesta (VASP POSCAR/CONTCAR 직접 읽기)

⛔ 이 도구가 **못 하는 것**
  · 원소색·결합상한은 **표시용 관례**다. 물리 판정에 쓰지 않는다 (결합 유무를 이 그림으로
    주장하지 않는다). 표에 없는 원소는 회색 구로 떨어지고 결합이 안 그려진다.
  · POSCAR 의 Selective dynamics(T/F)를 **표시하지 않는다** — 고정/자유 원자가 그림에서
    구분되지 않는다. 고정층을 보이려면 별도 색칠이 필요하다.
  · 자기 모멘트·전하를 안 그린다. 밀도는 cube 경로로만 들어간다.
"""
import argparse, os
from pathlib import Path
import numpy as np

BOHR = 0.529177210903
ZSYM = {1: "H", 3: "Li", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 15: "P", 16: "S", 17: "Cl",
        28: "Ni", 35: "Br", 53: "I"}
# VESTA 표준 원소색 (elements.ini) + 공유결합 반지름 → VASP 열었을 때와 동일한 외형
COL = {"Li": ("1.2800", "204 128 255 204 128 255"), "B": ("0.8400", "255 181 181 255 181 181"),
       "C": ("0.7600", "128 128 128 90 90 90"),     "N": ("0.7100", " 48  80 248  48  80 248"),
       "O": ("0.6600", "255  13  13 254 3 0"),       "P": ("1.0600", "255 128  0 204 191 224"),
       "S": ("1.0500", "255 255  48 255 250 0"),     "Cl": ("1.0200", " 31 240  31 49 252 2"),
       "Br": ("1.2000", "166  41  41 200 60 60"),     "I": ("1.3900", "148   0 148 130 0 130"),
       "H": ("0.4600", "255 204 204 255 204 204"),   "F": ("0.5700", "176 185 230 176 185 230"),
       "Ni": ("1.2400", "183 187 189  61  80 191")}

# argyrodite 결합/다면체 — P중심 PS4·PO4 사면체는 polyhedra(poly=1), Li–음이온 배위는 stick(poly=0)
# max 거리는 argyrodite 표준 결합상한 (Å); poly=1이면 그 중심원자로 다면체 렌더
BONDPAIRS = [
    ("P", "S", 2.35, 1), ("P", "O", 1.95, 1),
    ("Li", "S", 3.00, 0), ("Li", "Cl", 3.10, 0), ("Li", "Br", 3.25, 0),
    ("Li", "I", 3.40, 0), ("Li", "O", 2.70, 0),
    # SDCP/PTFE 조각 + 층상 산화물 슬랩 (표시용 상한 — 물리 판정 근거 아님)
    ("Ni", "O", 2.45, 1), ("C", "C", 1.75, 0), ("C", "F", 1.65, 0), ("C", "H", 1.25, 0),
    ("C", "O", 1.60, 0), ("C", "S", 1.95, 0), ("S", "O", 1.75, 0), ("O", "H", 1.25, 0),
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


def read_poscar(path):
    """VASP POSCAR/CONTCAR → (cell Å, [(기호, frac3)]).  못 읽으면 ValueError.

    ⛔ 원소 기호 줄(6행)이 없는 **VASP4 형식은 받지 않는다** — 기호를 POTCAR 에서
      추측하면 조용히 틀린 그림이 나온다. 기호가 없으면 시작하지 않는다.
    """
    L = Path(path).read_text(encoding="utf-8", errors="ignore").split("\n")
    scale = float(L[1].split()[0])
    cell = np.array([[float(x) for x in L[i].split()[:3]] for i in (2, 3, 4)]) * scale
    syms = L[5].split()
    if not syms or syms[0][0].isdigit():
        raise ValueError(f"{path}: 6행이 원소 기호가 아니다 (VASP4 형식은 안 받는다)")
    cnts = [int(x) for x in L[6].split()]
    i = 7
    if L[i].strip()[:1].upper() == "S":          # Selective dynamics
        i += 1
    direct = L[i].strip()[:1].upper() in ("D", "F")
    i += 1
    out = []
    for s, n in zip(syms, cnts):
        for _ in range(n):
            # ⛔ 잘린 파일에서 `L[i].split()[:3]` 는 **빈 배열**을 만들고 개수 검사를 통과한다.
            #   좌표가 없는 원자가 조용히 생긴다 — 성분 3개를 여기서 강제한다 (selftest 로 잡음).
            tok = L[i].split() if i < len(L) else []
            if len(tok) < 3:
                raise ValueError(f"{path}: {i+1}행에 좌표 3성분이 없다 (원자 {len(out)+1}/{sum(cnts)})")
            xyz = np.array([float(x) for x in tok[:3]]); i += 1
            out.append((s, xyz if direct else xyz @ np.linalg.inv(cell)))
    if len(out) != sum(cnts):
        raise ValueError(f"{path}: 좌표 {len(out)} ≠ 선언 {sum(cnts)}")
    return cell, out


def _selftest():
    """양성 + **음성** 경로. 음성만이 이 리더가 뭘 막는지 보증한다."""
    import tempfile
    bad, n = [], [0]

    def chk(c, m):
        n[0] += 1
        print(("  ✓ " if c else "  ✗ ") + m)
        if not c:
            bad.append(m)

    P5 = ("cmt\n1.0\n4.0 0.0 0.0\n0.0 4.0 0.0\n0.0 0.0 4.0\nLi O\n1 2\nDirect\n"
          "0.0 0.0 0.0\n0.5 0.0 0.0\n0.0 0.5 0.0\n")
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d/"P").write_text(P5, encoding="utf-8")
        cell, at = read_poscar(d/"P")
        chk(len(at) == 3 and [s for s, _ in at] == ["Li", "O", "O"], "양성: 기호·개수대로 펼친다")
        chk(abs(cell[0][0] - 4.0) < 1e-9, "양성: scale 을 곱한 셀을 돌려준다")
        chk(abs(at[1][1][0] - 0.5) < 1e-9, "양성: Direct 좌표를 그대로 쓴다")

        # Selective dynamics 줄을 건너뛴다
        (d/"S").write_text(P5.replace("Direct", "Selective dynamics\nDirect")
                           .replace("0.0 0.0 0.0\n0.5", "0.0 0.0 0.0 F F F\n0.5"), encoding="utf-8")
        chk(len(read_poscar(d/"S")[1]) == 3, "양성: Selective dynamics 줄을 건너뛴다")

        # Cartesian → frac 변환
        (d/"C").write_text("cmt\n1.0\n4.0 0.0 0.0\n0.0 4.0 0.0\n0.0 0.0 4.0\nLi\n1\n"
                           "Cartesian\n2.0 0.0 0.0\n", encoding="utf-8")
        chk(abs(read_poscar(d/"C")[1][0][1][0] - 0.5) < 1e-9,
            "양성: Cartesian 을 분율로 바꾼다 (그대로 쓰지 않는다)")

        # ⛔ VASP4 (기호 줄 없음) 는 거부
        (d/"V4").write_text(P5.replace("Li O\n", ""), encoding="utf-8")
        try:
            read_poscar(d/"V4"); ok = False
        except ValueError:
            ok = True
        chk(ok, "⛔음성: 기호 줄 없는 VASP4 를 거부한다 (POTCAR 로 추측하지 않는다)")

        # ⛔ 좌표가 모자라면 거부
        (d/"Short").write_text(P5.rsplit("\n", 2)[0] + "\n", encoding="utf-8")
        try:
            read_poscar(d/"Short"); ok = False
        except (ValueError, IndexError):
            ok = True
        chk(ok, "⛔음성: 선언 개수보다 좌표가 적으면 거부한다 (조용히 자르지 않는다)")

    chk("Ni" in COL and "F" in COL and "H" in COL, "양성: Ni·F·H 가 원소표에 있다")
    chk(any(a == "Ni" and b == "O" and poly == 1 for a, b, _, poly in BONDPAIRS),
        "양성: Ni–O 가 다면체(poly=1)로 등록돼 있다")
    print(f"selftest {n[0] - len(bad)}/{n[0]} · " + ("FAIL: " + "; ".join(bad) if bad else "PASS"))
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cube", nargs="?")
    ap.add_argument("--poscar", help="VASP POSCAR/CONTCAR 에서 구조 전용 vesta 를 만든다")
    ap.add_argument("--out", help="출력 .vesta 경로 (--poscar 와 함께)")
    ap.add_argument("--title", help="VESTA TITLE 줄")
    ap.add_argument("--iso", type=float, default=0.0, help="등가면 절대값 (0=자동 ~max/3)")
    ap.add_argument("--maxabs", type=float, default=0.0, help="cube 최대|Δρ| (자동iso용; 로그의 range로)")
    ap.add_argument("--structure-only", action="store_true", help="밀도/등가면 빼고 순수 구조 vesta")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(_selftest())
    if bool(a.poscar) == bool(a.cube):
        ap.error("cube 하나 또는 --poscar 하나를 준다 (둘 다/둘 없음 안 된다)")
    if a.poscar:
        a.structure_only = True                      # 밀도가 없다
        cell, plist = read_poscar(a.poscar)
        cell_b = cell / BOHR
        atoms = [(s, f) for s, f in plist]           # (기호, frac)
    else:
        cell_b, origin_b, atoms_z, vecs, ns = read_cube_header(a.cube)
        cell = cell_b * BOHR
        inv0 = np.linalg.inv(cell_b)
        atoms = [(ZSYM.get(z, "X"), (np.array([x, y, zc]) - origin_b) @ inv0)
                 for z, x, y, zc in atoms_z]
    L = np.linalg.norm(cell, axis=1)
    ang = lambda u, v: np.degrees(np.arccos(np.dot(u, v) / (np.linalg.norm(u)*np.linalg.norm(v))))
    al, be, ga = ang(cell[1], cell[2]), ang(cell[0], cell[2]), ang(cell[0], cell[1])
    iso = a.iso if a.iso > 0 else (a.maxabs/3 if a.maxabs > 0 else 0.003)

    # 원자 (분율 좌표) — cube/POSCAR 어느 쪽이든 위에서 (기호, frac) 로 맞춰 왔다
    from collections import Counter
    cnt = Counter(); struc = []; sitet = []; theri = []; atomt = {}
    for i, (s, fr) in enumerate(atoms, 1):
        cnt[s] += 1; lb = f"{s}{cnt[s]}"
        struc.append(f"{i:3d} {s:>2s} {lb:>8s}  1.0000 {fr[0]:11.6f} {fr[1]:11.6f} {fr[2]:11.6f}    1        -")
        struc.append("                            0.000000   0.000000   0.000000  0.00")
        r, c = COL.get(s, ("0.5", "150 150 150 150 150 150")); sitet.append(f"{i:3d} {lb:>8s}  {r} {c}  50  0")
        theri.append(f"{i:3d} {lb:>8s}  0.000000"); atomt[s] = (r, c)
    cube_name = os.path.basename(a.cube) if a.cube else os.path.basename(a.poscar)
    atomt_lines = "\n".join(f"  {j+1} {s:>2s}  {COL.get(s,('0.5','150 150 150 150 150 150'))[0]} "
                            f"{COL.get(s,('0.5','150 150 150 150 150 150'))[1]}  50" for j, s in enumerate(atomt))

    dens = "" if a.structure_only else f"\nIMPORT_DENSITY 1\n+1.000000 {cube_name}\n"
    isurf = "" if a.structure_only else (
        f"ISURF\n  1   0  {iso:.5f} 255 255   0 127 255\n"
        f"  2   0  {-iso:.5f}   0 255 255 127 255\n  0   0   0   0\n")
    ttl = a.title or (f"{cube_name} structure only" if a.structure_only
                      else f"{cube_name} CDD (yellow=accumulation / cyan=depletion)")
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
    outp = a.out or (os.path.splitext(a.cube or a.poscar)[0]
                     + ("_structure.vesta" if a.structure_only else ".vesta"))
    assert all(ord(ch) < 128 for ch in v), "non-ASCII"
    open(outp, "w", newline="").write(v.replace("\n", "\r\n"))
    tag = "구조 only" if a.structure_only else f"iso ±{iso:.4f}"
    print(f"-> {outp}  ({tag}, {len(atoms)} atoms)")
    print(f"   cell {L.round(2)} A  {len(atoms)} atoms  (cube와 같은 폴더에 둘 것)")


if __name__ == "__main__":
    main()
