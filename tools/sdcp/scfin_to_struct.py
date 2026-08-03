#!/usr/bin/env python3
"""scfin_to_struct.py — QE scf.in → xyz + POSCAR 페어 + 흡착/주기이미지 거리 점검.

계산에 **실제로 들어간** 기하를 그대로 꺼낸다. Phase-A 스캔 xyz 가 아니라 scf.in 을
읽는 이유: 스캔 셀은 c=40 Å 인데 파이프라인이 슬랩 셀(c=28.79 Å)로 다시 앉히기
때문에, 눈으로 봐야 하는 건 **재배치 후**의 기하다.

⚠ 2026-07-17 에 doped 결합에너지를 철회한 원인이 이 지점이었다 — 분자가 수직으로 서서
  티오펜 S 가 **c 를 넘은 이미지 슬랩의 O 와 1.506 Å**(결합거리)이었고, 그러면 E_bind 가
  한 표면이 아니라 두 표면 몫이 된다. 그래서 구조만 뽑지 않고 거리를 같이 찍는다.

⚠⚠ **거리를 층으로 갈라야 한다. 안 가르면 두 방향으로 다 틀린다 (2026-08-03, 실제로 다 틀림).**
  ① 흡착 접촉  sh_z == 0 (자기 셀 포함) — 슬랩은 면내로 **연속된 하나의 표면**이다.
     분자가 셀 모서리에 앉으면 진짜 결합상대가 shift (1,1,0) 에 있다. 자기 셀만 재면
     그 결합(1.887 Å)을 놓치고 6.348 Å 을 보고 "떠 있다"고 오판한다.
  ② 진공 너머  sh_z != 0 — 여기만 **인공 두 번째 표면**이다. 샌드위치 판정은 이 층에서만.
  ③ 면내 피복  sh_z == 0, 분자↔분자 — 분자가 옆 셀 자기 자신과 닿으면 피복률이 과하다.
  [참고] 슬랩↔슬랩 면내(Ni–O 1.94 Å, Ni–Ni 2.88 Å)는 **결정 그 자체**다. 판정에 넣지 마라.

⚠⚠ **xyz 와 vasp 는 반드시 같은 원자 순서로 쓴다 (2026-08-03).** POSCAR 는 같은 원소가
  연속해야 하는데 복합체는 O 가 슬랩과 분자 양쪽에 흩어져 있어 재정렬이 불가피하다.
  예전 판은 vasp 만 재정렬해서 두 파일의 원자 순서가 달랐고, 뷰어에서 서로 다른
  구조처럼 보였다(실측 제보). 순서를 한 번만 정하고 두 파일에 똑같이 쓴다.

  cd ~/Yonghoon-DEM-DFT
  python3 tools/sdcp/scfin_to_struct.py --scf_in .../complex_doped/scf.in --out ~/sdcp_poses

관례(CLAUDE.md): 구조 배포는 **xyz + POSCAR(.vasp) 페어**. xyz 는 격자가 없으므로
VESTA 에서 Boundary 타일링을 하려면 .vasp 쪽을 연다.
"""
import argparse
import itertools
import os
import re

import numpy as np

# 공유결합 반지름 (Å, Cordero 2008). 분자/슬랩 분할용 연결성 판정에만 쓴다.
RCOV = {"H": 0.31, "Li": 1.28, "B": 0.84, "C": 0.76, "N": 0.71, "O": 0.66,
        "F": 0.57, "P": 1.07, "S": 1.05, "Cl": 1.02, "Ni": 1.24}
BOND_SCALE = 1.25
# 분자 씨앗: 슬랩(LiNiO2)에 없는 원소만 고른다. O 는 양쪽에 다 있으므로 씨앗이 못 된다
# — 연결성으로 흡수시킨다.
MOL_SEED = ("C", "H", "S", "N", "F", "P", "B", "Cl")


def read_extxyz(path):
    """Phase-A 가 ASE 로 쓴 pose xyz. 2번째 줄 Lattice="..." 에 셀이 들어 있다.

    ⚠ 원본 자세를 그대로 볼 수 있어야 한다 — scf.in 쪽 수치가 이상할 때
      '스캔이 그렇게 낸 것'인지 'phaseB 가 망친 것'인지 가르는 유일한 대조군이다.
    """
    with open(path, errors="ignore") as f:
        lines = f.read().splitlines()
    nat = int(lines[0].split()[0])
    m = re.search(r'Lattice="([^"]+)"', lines[1])
    if not m:
        raise SystemExit(f"⛔ {path} 2번째 줄에 Lattice=\"...\" 가 없다 — 셀 없는 순수 xyz 는 못 쓴다")
    cell = np.array([float(x) for x in m.group(1).split()]).reshape(3, 3)
    labels, pos = [], []
    for ln in lines[2:2 + nat]:
        v = ln.split()
        labels.append(v[0]); pos.append([float(x) for x in v[1:4]])
    return cell, labels, np.array(pos)


def read_any(path):
    return read_extxyz(path) if path.lower().endswith((".xyz", ".extxyz")) else read_scf_in(path)


def read_scf_in(path):
    """CELL_PARAMETERS angstrom / ATOMIC_POSITIONS angstrom 만 읽는다 (이 생성기의 형식)."""
    with open(path, errors="ignore") as f:
        lines = f.read().splitlines()
    cell, labels, pos = [], [], []
    mode = None
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        head = s.split()[0].upper()
        if head == "CELL_PARAMETERS":
            if "angstrom" not in s.lower():
                raise SystemExit(f"⛔ CELL_PARAMETERS 단위가 angstrom 이 아니다: {s}")
            mode = "cell"; continue
        if head == "ATOMIC_POSITIONS":
            if "angstrom" not in s.lower():
                raise SystemExit(f"⛔ ATOMIC_POSITIONS 단위가 angstrom 이 아니다: {s}")
            mode = "pos"; continue
        if head in ("K_POINTS", "ATOMIC_SPECIES", "HUBBARD") or s.startswith("&"):
            mode = None; continue
        if mode == "cell":
            v = s.split()
            if len(v) == 3:
                cell.append([float(x) for x in v])
            if len(cell) == 3:
                mode = None
        elif mode == "pos":
            v = s.split()
            if len(v) >= 4:
                labels.append(v[0]); pos.append([float(x) for x in v[1:4]])
            else:
                mode = None
    if len(cell) != 3 or not labels:
        raise SystemExit(f"⛔ {path} 에서 셀/좌표를 못 읽었다")
    return np.array(cell), labels, np.array(pos)


# ⚠ QE 라벨은 자기/U 를 나누려고 원소 뒤에 숫자를 붙인다 (Ni1, Ni2). 뷰어에 넘길
#   .xyz/.vasp 에는 **원소 기호**가 가야 하므로 뒤 숫자를 뗀다.
def element(label):
    m = re.match(r"^([A-Z][a-z]?)", label)
    if not m:
        raise SystemExit(f"⛔ 라벨에서 원소를 못 읽었다: {label}")
    return m.group(1)


def group_by_species(elems, labels, pos):
    """POSCAR 규격(같은 원소 연속)에 맞게 한 번만 재정렬하고, 그 순서를 xyz 에도 쓴다."""
    uniq = sorted(set(elems), key=elems.index)          # 첫 등장 순서 유지
    idx = [i for e in uniq for i, x in enumerate(elems) if x == e]
    return ([elems[i] for i in idx], [labels[i] for i in idx], pos[np.array(idx)],
            uniq, [elems.count(e) for e in uniq])


def split_molecule(elems, pos):
    """C/H/S 씨앗에서 공유결합 반지름으로 자라며 분자를 집는다. 나머지가 슬랩."""
    n = len(elems)
    r = np.array([RCOV.get(e, 1.0) for e in elems])
    d = np.linalg.norm(pos[:, None, :] - pos[None, :, :], axis=-1)
    bond = d < BOND_SCALE * (r[:, None] + r[None, :])
    np.fill_diagonal(bond, False)
    mol = np.array([e in MOL_SEED for e in elems])
    while True:                                          # 씨앗에 붙은 O 까지 흡수
        grown = mol | (bond & mol[None, :]).any(axis=1)
        if (grown == mol).all():
            return mol
        mol = grown


def write_xyz(path, elems, pos, comment):
    with open(path, "w") as f:
        f.write(f"{len(elems)}\n{comment}\n")
        for e, p in zip(elems, pos):
            f.write(f"{e:<3s} {p[0]:16.8f} {p[1]:16.8f} {p[2]:16.8f}\n")


def write_poscar(path, cell, order, counts, pos, comment):
    with open(path, "w") as f:
        f.write(comment.replace("\n", " ") + "\n1.0\n")
        for v in cell:
            f.write(f"  {v[0]:18.12f} {v[1]:18.12f} {v[2]:18.12f}\n")
        f.write("  " + "  ".join(order) + "\n")
        f.write("  " + "  ".join(str(c) for c in counts) + "\n")
        f.write("Cartesian\n")
        for p in pos:
            f.write(f"  {p[0]:18.12f} {p[1]:18.12f} {p[2]:18.12f}\n")



# ═══ VESTA 프리셋 ═══════════════════════════════════════════════════════════
# 사용자의 기존 SDCP 분자 .vesta (ORCA 판) 양식을 그대로 승계한다 — C/S/O/H 의
# 반지름·색이 같아야 분자 그림끼리 나란히 놓을 수 있다. 여기에 슬랩 원소만 더한다.
#   (radius, R,G,B, R2,G2,B2)   뒤 3색은 VESTA 보조색
VSTYLE = {
    "C":  (0.35,  76,  76,  76, 128,  73,  41),
    "S":  (0.48, 255, 250,   0, 255, 250,   0),
    "O":  (0.38, 254,   3,   0, 254,   3,   0),
    "H":  (0.20, 255, 255, 255, 255, 204, 204),
    "Li": (0.42,  70, 175,  90,  70, 175,  90),
    "Ni": (0.46,  40,  90, 200,  40,  90, 200),
}
# ⚠ **반지름은 셀 크기에 맞춰 키워야 한다 (2026-08-03 실측).** 위 값은 ~10 A 분자용이라
#   11.5 x 18.3 x 28.8 A 결정 셀에 그대로 쓰면 화면의 1% 짜리 **점**이 된다. 비율은
#   분자 .vesta 와 같게 두고 전체를 상수배 한다 → 분자 그림과 상대 크기가 유지된다.
RAD_SCALE_DEFAULT = 1.7
# ⚠ scf.in 은 Ni1/Ni2 (AFM 부격자)를 라벨로 구분해 들고 있다. .vasp/.xyz 로 나갈 때는
#   원소 Ni 로 뭉개지지만 **.vesta 는 site 단위 색을 쓰므로 부격자를 살릴 수 있다** —
#   NiO6 팔면체가 파랑/회색으로 갈리면 반강자성 배치가 그림에서 바로 읽힌다.
# ⚠ **흰 배경에 옅은 회색을 쓰면 원자가 사라진다 (실측: Ni 절반이 안 보였다).**
#   AFM 쌍은 파랑/보라로 — 둘 다 흰 배경에서 진하고, O(빨강)·S(노랑)·Li(초록)와 안 겹친다.
NI_SUB = {"Ni1": (40, 90, 200), "Ni2": (150, 60, 170)}
# (A1, A2, max_len, show_polyhedra)
VBONDS = [("Ni", "O", 2.40, 1),   # NiO6 팔면체 + 분자 O 와의 흡착결합(1.89 A)도 여기서 그려진다
          ("Li", "O", 2.60, 0),
          ("C", "C", 1.70, 0), ("C", "H", 1.15, 0), ("C", "O", 1.65, 0),
          ("C", "S", 1.95, 0), ("S", "O", 1.80, 0), ("O", "H", 1.10, 0)]


def write_vesta(path, cell, labels, elems, pos, title, scale=RAD_SCALE_DEFAULT):
    """CRYSTAL 형식 .vesta. 좌표는 **분율**이어야 한다 (MOLECULE 판은 Cartesian).

    ⚠ CLAUDE.md: .vesta 는 **ASCII 전용 + CRLF**. 비ASCII 한 글자가 파싱을 깨뜨린 전례가
      있으므로 이 함수가 쓰는 문자열에는 한글·em-dash 를 절대 넣지 않는다.
    """
    a, b, c = (np.linalg.norm(v) for v in cell)
    ang = lambda u, v: np.degrees(np.arccos(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))))
    al, be, ga = ang(cell[1], cell[2]), ang(cell[0], cell[2]), ang(cell[0], cell[1])
    frac = pos @ np.linalg.inv(cell)

    # 사이트 라벨: 참조 .vesta 와 같은 **영숫자만** 쓴다 (밑줄/비ASCII 는 파싱 위험).
    #   AFM 부격자는 색으로도 갈리지만 라벨에도 남긴다 — NiA = spin up, NiB = spin down.
    seen, site_lab = {}, []
    for e, lb in zip(elems, labels):
        stem = {"Ni1": "NiA", "Ni2": "NiB"}.get(lb, e)
        seen[stem] = seen.get(stem, 0) + 1
        site_lab.append(f"{stem}{seen[stem]}")

    L = ["#VESTA_FORMAT_VERSION 3.5.4", "", "", "CRYSTAL", "", "TITLE",
         title.encode("ascii", "replace").decode("ascii"), "", "GROUP", "1 1 P 1  ", "SYMOP",
         " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1   1",
         " -1.0 -1.0 -1.0  0 0 0  0 0 0  0 0 0", "TRANM 0",
         " 0.000000  0.000000  0.000000  1  0  0   0  1  0   0  0  1", "LTRANSL", " -1",
         " 0.000000  0.000000  0.000000  0.000000  0.000000  0.000000", "LORIENT",
         " -1   0   0   0   0",
         " 1.000000  0.000000  0.000000  1.000000  0.000000  0.000000",
         " 0.000000  0.000000  1.000000  0.000000  0.000000  1.000000", "LMATRIX",
         " 1.000000  0.000000  0.000000  0.000000", " 0.000000  1.000000  0.000000  0.000000",
         " 0.000000  0.000000  1.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
         " 0.000000  0.000000  0.000000", "CELLP",
         f"  {a:9.6f}  {b:9.6f}  {c:9.6f}  {al:9.6f}  {be:9.6f}  {ga:9.6f}",
         "  0.000000   0.000000   0.000000   0.000000   0.000000   0.000000", "STRUC"]
    for i, (e, sl, f) in enumerate(zip(elems, site_lab, frac), 1):
        L.append(f"  {i:3d}  {e:<2s}  {sl:>10s}  1.0000  {f[0]:10.6f} {f[1]:10.6f} "
                 f"{f[2]:10.6f}    1        -")
        L.append("                            0.000000   0.000000   0.000000  0.00")
    L += ["  0 0 0 0 0 0 0", "THERI 1"]
    for i, sl in enumerate(site_lab, 1):
        L.append(f"  {i:3d} {sl:>10s} -0.000000")
    L += ["  0 0 0", "SHAPE",
          "  0       0       0       0   0.000000  0   192   192   192   192", "BOUND",
          "       0        1         0        1         0        1", "  0   0   0   0  0",
          "SBOND"]
    present = set(elems)
    n = 0
    for a1, a2, mx, poly in VBONDS:
        if a1 not in present or a2 not in present:
            continue
        n += 1
        # ⚠ 플래그는 **사용자의 기존 .vesta 와 한 글자도 다르지 않게** `0 1 1 0 1` 로 둔다.
        #   그 파일이 정상 렌더되는 known-good 조합이다. 여기를 임의로 0 으로 바꿨더니
        #   결합이 안 그려졌다(실측) — 이 5개 정수의 의미를 추측으로 건드리지 않는다.
        #   boundary_mode(2번째)=1 이라 **셀 경계를 넘는 결합**도 그려진다. 이 계의
        #   흡착결합이 실제로 shift (1,1,0) 이므로 이게 0 이면 분자가 떠 보인다.
        L.append(f"  {n}  {a1:>5s} {a2:>5s}    0.00000  {mx:9.5f}  0  1  1  0  1  "
                 f"{0.110 * scale:.3f}  0.000 127 127 127")
    L += ["  0 0 0 0", "SITET"]
    for i, (e, lb, sl) in enumerate(zip(elems, labels, site_lab), 1):
        rad, r1, g1, b1, r2, g2, b2 = VSTYLE.get(e, (0.40, 160, 160, 160, 160, 160, 160))
        rad *= scale
        if lb in NI_SUB:
            r1, g1, b1 = NI_SUB[lb]; r2, g2, b2 = r1, g1, b1
        L.append(f"  {i:3d} {sl:>10s}  {rad:.4f} {r1:3d} {g1:3d} {b1:3d} "
                 f"{r2:3d} {g2:3d} {b2:3d}  50  0")
    L += ["  0 0 0 0 0 0", "VECTR", " 0 0 0 0 0", "VECTT", " 0 0 0 0 0", "SPLAN",
          "  0   0   0   0", "LBLAT", " -1", "LBLSP", " -1", "DLATM", " -1", "DLBND", " -1",
          "DLPLY", " -1", "PLN2D", "  0   0   0   0", "ATOMT"]
    for k, e in enumerate(sorted(present, key=lambda x: list(elems).index(x)), 1):
        rad, r1, g1, b1, r2, g2, b2 = VSTYLE.get(e, (0.40, 160, 160, 160, 160, 160, 160))
        rad *= scale
        L.append(f"  {k}  {e:>9s}  {rad:.4f} {r1:3d} {g1:3d} {b1:3d} {r2:3d} {g2:3d} {b2:3d}  50")
    # SCENE: c 축을 화면 위로 세운 측면 시점 (슬랩은 위에서 보면 층이 안 보인다)
    L += ["  0 0 0 0 0 0", "SCENE",
          " 1.000000  0.000000  0.000000  0.000000", " 0.000000  0.000000  1.000000  0.000000",
          " 0.000000 -1.000000  0.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
          "  0.000   0.000", "  0.000", "  1.000", "HBOND 0 2", "", "STYLE",
          "DISPF 37749698", "MODEL   0  1  0", "SURFS   0  1  1", "SECTS  32  1",
          "FORMS   0  1", "ATOMS   0  0  1", "BONDS   1", "POLYS   1", "VECTS 1.000000",
          "FORMP", "  1  1.0   0   0   0", "ATOMP", " 24  24   0  50  2.0   0", "BONDP",
          f"  1  16  {0.110 * scale:.3f}  0.000 127 127 127", "POLYP", "  50 1  0.030 150 150 150",
          "ISURF", "  0   0   0   0", "TEX3P", "  1         -INF         -INF", "SECTP",
          "  1  5.00000E-01  5.00000E-01  0.00000E+00  0.00000E+00  0.00000E+00  0.00000E+00",
          "CONTR", " 0.1 -1 1 1 10 -1 2 5", " 2 1 2 1", "   0   0   0", "   0   0   0",
          "   0   0   0", "   0   0   0", "HKLPP", " 192 1  1.000 255   0 255", "UCOLP",
          "   0   0  1.000   0   0   0", "COMPS 0", "LABEL 1    12  1.000 0", "PROJT 0  0.962",
          "BKGRC", " 255 255 255", "DPTHQ 0 -0.5000  3.5000", "LIGHT0 1"]
    ident = [" 1.000000  0.000000  0.000000  0.000000", " 0.000000  1.000000  0.000000  0.000000",
             " 0.000000  0.000000  1.000000  0.000000", " 0.000000  0.000000  0.000000  1.000000",
             " 0.000000  0.000000 20.000000  0.000000", " 0.000000  0.000000 -1.000000"]
    L += ident + ["  26  26  26 255", " 179 179 179 255", " 255 255 255 255"]
    for k in (1, 2, 3):
        L += [f"LIGHT{k}"] + ident + ["   0   0   0   0"] * 3
    L += ["SECCL 0", "", "TEXCL 0", "", "ATOMM", " 204 204 204 255", "  25.600", "BONDM",
          " 255 255 255 255", " 128.000", "POLYM", " 255 255 255 255", " 128.000", "SURFM",
          "   0   0   0 255", " 128.000", "FORMM", " 100 100 100 255", "  44.800", "HKLPM",
          " 255 255 255 255", " 128.000", ""]
    body = "\n".join(L)
    assert body.isascii(), "non-ASCII leaked into .vesta"
    with open(path, "w", encoding="ascii", newline="\r\n") as f:
        f.write(body)


def pair_min(cell, labels, pos, sel_a, sel_b, layer, same=False):
    """sel_a ↔ sel_b 최소 거리. `layer` 로 어떤 이미지를 볼지 고른다.

    ⚠⚠ **이 함수의 layer 분리가 이 도구의 전부다. 두 번 틀렸다 (2026-08-03).**

      1차 오판 — 전 원자쌍을 훑어 슬랩의 면내 격자 결합(Ni–O 1.94 Å, Ni–Ni 2.88 Å)을
        '이미지 샌드위치'로 찍었다. 슬랩은 a·b 로 주기적인 결정이라 그 결합은 정상이다.
      2차 오판 — 반대로 흡착거리를 **자기 셀 안에서만** 재서, 셀 모서리 근처에 앉은
        분자의 진짜 결합상대(shift (1,1,0) 의 Ni, 1.887 Å)를 놓치고 6.348 Å 을 보고
        "떠 있다"고 판정했다. 슬랩은 면내로 **연속된 하나의 표면**이다.

      물리적으로 옳은 분리는 이것뿐이다:
        layer='surface' (sh_z == 0, 자기 셀 포함) → **진짜 표면**. 흡착 접촉거리.
        layer='vacuum'  (sh_z != 0)              → **진공 너머의 인공 두 번째 표면**.
                                                    2026-07-17 샌드위치 철회의 그 축.
    """
    ia, ib = np.flatnonzero(sel_a), np.flatnonzero(sel_b)
    if not len(ia) or not len(ib):
        return None
    best = None
    for sh in itertools.product((-1, 0, 1), repeat=3):
        if layer == "surface" and sh[2] != 0:
            continue
        if layer == "vacuum" and sh[2] == 0:
            continue
        # ⚠ 같은 집합끼리 비교할 때 (0,0,0) 은 **분자 내부 결합**(C–H 1.08 Å 등)을 집는다.
        #   대각선만 지우는 걸로는 부족하다 — 그 shift 자체를 빼야 이미지 접촉만 남는다.
        if same and sh == (0, 0, 0):
            continue
        d = np.linalg.norm(pos[ia][:, None, :]
                           - (pos[ib][None, :, :] + np.array(sh) @ cell), axis=-1)
        i, j = np.unravel_index(np.argmin(d), d.shape)
        rec = (d[i, j], labels[ia[i]], labels[ib[j]], sh)
        if best is None or rec[0] < best[0]:
            best = rec
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf_in", required=True, nargs="+",
                    help="QE scf.in 또는 Phase-A pose .xyz (확장자로 자동 판별)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default=None, help="출력 접두어 (기본: 상위 디렉터리명)")
    ap.add_argument("--vesta_scale", type=float, default=RAD_SCALE_DEFAULT,
                    help="VESTA 원자 반지름 배율. 셀이 크면 키운다 (기본 1.7)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for path in a.scf_in:
        tag = a.tag or (os.path.splitext(os.path.basename(path))[0]
                        if path.lower().endswith((".xyz", ".extxyz"))
                        else os.path.basename(os.path.dirname(os.path.abspath(path))))
        cell, labels0, pos0 = read_any(path)
        elems0 = [element(x) for x in labels0]
        elems, labels, pos, order, counts = group_by_species(elems0, labels0, pos0)

        c_len = np.linalg.norm(cell[2])
        span = pos[:, 2].max() - pos[:, 2].min()
        comment = (f"{tag} | nat={len(elems)} | cell a={np.linalg.norm(cell[0]):.3f} "
                   f"b={np.linalg.norm(cell[1]):.3f} c={c_len:.3f} A | "
                   f"z-span={span:.3f} A | vertical vacuum={c_len - span:.3f} A | "
                   f"UNRELAXED single-point geometry from {os.path.abspath(path)}")
        write_xyz(os.path.join(a.out, f"{tag}.xyz"), elems, pos, comment)
        write_poscar(os.path.join(a.out, f"{tag}.vasp"), cell, order, counts, pos, comment)
        write_vesta(os.path.join(a.out, f"{tag}.vesta"), cell, labels, elems, pos,
                    f"{tag} (nat {len(elems)}) - unrelaxed single-point geometry, "
                    f"NiO6 polyhedra + AFM sublattice colors (NiA blue / NiB purple)",
                    scale=a.vesta_scale)

        print(f"\n══ {tag}  (nat {len(elems)}) ══")
        print(f"  cell  a {np.linalg.norm(cell[0]):.3f}  b {np.linalg.norm(cell[1]):.3f}"
              f"  c {c_len:.3f} A     z-span {span:.3f} → 수직 진공 {c_len - span:.3f} A")
        print(f"  xyz 와 vasp 는 **같은 원자 순서·같은 좌표** ({'+'.join(f'{e}{c}' for e, c in zip(order, counts))})")

        mol = split_molecule(elems, pos)
        if not (mol.any() and (~mol).any()):
            print("  (단일 조각 — 분자/슬랩 분할 없음)")
            print(f"  → {a.out}/{tag}.xyz + .vasp + .vesta")
            continue

        # ── ⓪ z 단면: 슬랩 위에 얹혀 있는 게 맞나 ───────────────────────────
        zs, zm = pos[~mol][:, 2], pos[mol][:, 2]
        print(f"  ⓪ z 범위  슬랩 [{zs.min():6.2f}, {zs.max():6.2f}]   "
              f"분자 [{zm.min():6.2f}, {zm.max():6.2f}]  (A)")

        # ── ① 흡착 접촉 — **면내 주기를 포함한** 진짜 표면과의 거리 ──────────
        ads = pair_min(cell, labels, pos, mol, ~mol, "surface")
        print(f"  ① 흡착 접촉  분자({mol.sum()}) ↔ 표면({(~mol).sum()})  "
              f"{ads[0]:.3f} A  ({ads[1]}↔{ads[2]}, shift {ads[3]})")
        print("     (슬랩은 면내로 연속된 하나의 표면 — shift 가 (±1,±1,0) 이어도 같은 표면이다)")
        if ads[0] < 2.5:
            print("     ✓ 화학흡착 (결합거리)")
        elif ads[0] < 3.2:
            print("     ✓ 근접 접촉")
        elif ads[0] < 4.0:
            print("     ⚠ 물리흡착 경계 — 화학결합 없음")
        else:
            print("     ⛔ 4 A 초과 — 접촉이 아니다. 흡착 자세가 아니라 떠 있는 것이다.")

        # ── ② 진공 너머 = 인공 두 번째 표면 (2026-07-17 철회의 그 축) ────────
        vac_s = pair_min(cell, labels, pos, mol, ~mol, "vacuum")
        vac_m = pair_min(cell, labels, pos, mol, mol, "vacuum", same=True)
        print(f"  ② 진공 너머 (c 를 넘는 이미지만)  분자↔슬랩 {vac_s[0]:.3f} A "
              f"(shift {vac_s[3]})  ·  분자↔분자 {vac_m[0]:.3f} A")
        img = min(vac_s[0], vac_m[0])
        if img < 2.5:
            print("     ⛔ 결합거리 — 이미지 샌드위치. 이 자세의 E_bind 는 단일표면 값이 아니다.")
        elif img < 3.5:
            print("     ⚠ vdW 접촉 — E_bind 에 이미지 상호작용이 섞인다. 진공을 키울 것.")
        else:
            print("     ✓ 진공 분리 확보 (2026-07-17 철회 사유 없음)")

        # ── ③ 면내 피복 — 분자끼리 옆 셀에서 닿나 ───────────────────────────
        lat = pair_min(cell, labels, pos, mol, mol, "surface", same=True)
        print(f"  ③ 면내 피복  분자 ↔ 옆 셀 분자 {lat[0]:.3f} A "
              f"({lat[1]}↔{lat[2]}, shift {lat[3]})"
              f"{'  ⚠ 3.5 A 미만 — 피복률이 너무 높다' if lat[0] < 3.5 else ''}")
        ss = pair_min(cell, labels, pos, ~mol, ~mol, "surface", same=True)
        print(f"     [참고] 슬랩 ↔ 옆 셀 슬랩 {ss[0]:.3f} A ({ss[1]}↔{ss[2]}) = 격자 결합, 정상")
        print(f"  → {a.out}/{tag}.xyz + .vasp + .vesta")


if __name__ == "__main__":
    main()
