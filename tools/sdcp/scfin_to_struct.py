#!/usr/bin/env python3
"""scfin_to_struct.py — QE scf.in → xyz + POSCAR 페어 + 흡착/주기이미지 거리 점검.

계산에 **실제로 들어간** 기하를 그대로 꺼낸다. Phase-A 스캔 xyz 가 아니라 scf.in 을
읽는 이유: 스캔 셀은 c=40 Å 인데 파이프라인이 슬랩 셀(c=28.79 Å)로 다시 앉히기
때문에, 눈으로 봐야 하는 건 **재배치 후**의 기하다.

⚠ 2026-07-17 에 doped 결합에너지를 철회한 원인이 이 지점이었다 — 분자가 수직으로 서서
  티오펜 S 가 **주기이미지 슬랩의 O 와 1.506 Å**(결합거리)이었고, 그러면 E_bind 가
  한 표면이 아니라 두 표면 몫이 된다. 그래서 이 도구는 구조만 뽑는 게 아니라
  **① 분자↔슬랩 접촉거리(자기 셀)** 와 **② 이웃 셀 26개에 대한 최소 원자간 거리**를
  같이 찍는다. ①이 없으면 흡착이 아니고, ②가 작으면 단일표면 값이 아니다.

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


def image_check(cell, labels, pos):
    """이웃 셀 26개에 대한 최소 원자간 거리. 자기 셀(0,0,0)은 뺀다."""
    worst, per_shift = None, {}
    for sh in itertools.product((-1, 0, 1), repeat=3):
        if sh == (0, 0, 0):
            continue
        t = np.array(sh) @ cell
        d = np.linalg.norm(pos[:, None, :] - (pos[None, :, :] + t), axis=-1)
        i, j = np.unravel_index(np.argmin(d), d.shape)
        rec = (d[i, j], labels[i], labels[j], sh)
        per_shift[sh] = rec
        if worst is None or rec[0] < worst[0]:
            worst = rec
    return worst, per_shift


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scf_in", required=True, nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--tag", default=None, help="출력 접두어 (기본: 상위 디렉터리명)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for path in a.scf_in:
        tag = a.tag or os.path.basename(os.path.dirname(os.path.abspath(path)))
        cell, labels0, pos0 = read_scf_in(path)
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

        print(f"\n══ {tag}  (nat {len(elems)}) ══")
        print(f"  cell  a {np.linalg.norm(cell[0]):.3f}  b {np.linalg.norm(cell[1]):.3f}"
              f"  c {c_len:.3f} A     z-span {span:.3f} → 수직 진공 {c_len - span:.3f} A")
        print(f"  xyz 와 vasp 는 **같은 원자 순서·같은 좌표** ({'+'.join(f'{e}{c}' for e, c in zip(order, counts))})")

        # ── ① 흡착하고 있나 (자기 셀 안, 분자↔슬랩) ──────────────────────────
        mol = split_molecule(elems, pos)
        if mol.any() and (~mol).any():
            dms = np.linalg.norm(pos[mol][:, None, :] - pos[~mol][None, :, :], axis=-1)
            i, j = np.unravel_index(np.argmin(dms), dms.shape)
            mi = np.flatnonzero(mol)[i]; si = np.flatnonzero(~mol)[j]
            print(f"  ① 분자({mol.sum()}원자) ↔ 슬랩({(~mol).sum()}원자) 최근접 "
                  f"{dms[i, j]:.3f} A  ({labels[mi]}↔{labels[si]})")
            if dms[i, j] > 4.0:
                print("     ⛔ 4 A 초과 — 접촉이 아니다. 이건 흡착 자세가 아니라 떠 있는 것이다.")
            elif dms[i, j] > 3.2:
                print("     ⚠ 물리흡착 경계 — 화학결합 없음. 의도한 자세인지 확인할 것.")
            else:
                print("     ✓ 접촉 (결합/근접 흡착)")

        # ── ② 주기이미지와 붙어 있나 ────────────────────────────────────────
        worst, per_shift = image_check(cell, labels, pos)
        print(f"  ② 이웃셀 통틀어 최소 원자간 거리 {worst[0]:.3f} A "
              f"({worst[1]}↔{worst[2]}, shift {worst[3]})")
        for sh, lab in (((0, 0, 1), "c 축 위 (샌드위치 위험)"),
                        ((1, 0, 0), "a 축 옆 (분자-분자 피복)"),
                        ((0, 1, 0), "b 축 옆 (분자-분자 피복)")):
            r = per_shift[sh]
            print(f"     {lab:26s} {r[0]:7.3f} A  ({r[1]}↔{r[2]})")
        # ⚠ 판정선은 물리다: 결합거리(~1.5-2.2 A)면 그 자세는 못 쓴다.
        if worst[0] < 2.5:
            print("     ⛔ 결합거리 — 이미지 샌드위치. 이 자세의 E_bind 는 단일표면 값이 아니다.")
        elif worst[0] < 3.5:
            print("     ⚠ vdW 접촉 — E_bind 에 이미지 상호작용이 섞인다. 셀을 키울 것.")
        else:
            print("     ✓ 이미지 분리 확보 (2026-07-17 철회 사유 없음)")
        print(f"  → {a.out}/{tag}.xyz + {tag}.vasp")


if __name__ == "__main__":
    main()
