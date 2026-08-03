#!/usr/bin/env python3
"""scfin_to_struct.py — QE scf.in → xyz + POSCAR 페어 + 주기이미지 간격 점검.

계산에 **실제로 들어간** 기하를 그대로 꺼낸다. Phase-A 스캔 xyz 가 아니라 scf.in 을
읽는 이유: 스캔 셀은 c=40 Å 인데 파이프라인이 슬랩 셀(c=28.79 Å)로 다시 앉히기
때문에, 눈으로 봐야 하는 건 **재배치 후**의 기하다.

⚠ 2026-07-17 에 doped 결합에너지를 철회한 원인이 바로 이 지점이었다 — 분자가 수직으로
  서서 티오펜 S 가 **주기이미지 슬랩의 O 와 1.506 Å**(결합거리)이었고, 그러면
  E_bind 가 한 표면이 아니라 두 표면 몫이 된다. 그래서 이 도구는 구조만 뽑는 게 아니라
  **모든 이웃 셀(26개)에 대한 최소 원자간 거리**를 같이 찍는다. 그 숫자를 안 보고
  자세를 채택하지 않는다.

  cd ~/Yonghoon-DEM-DFT
  python3 tools/sdcp/scfin_to_struct.py \
      --scf_in /data/work/runs/.../complex_doped/scf.in --out ~/sdcp_poses

관례(CLAUDE.md): 구조 배포는 **xyz + POSCAR(.vasp) 페어**. xyz 는 격자가 없으므로
VESTA 에서 Boundary 타일링을 하려면 .vasp 쪽을 연다.
"""
import argparse
import itertools
import os
import re

import numpy as np


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


# ⚠ QE 라벨은 자기장/U 를 나누려고 원소 뒤에 숫자를 붙인다 (Ni1, Ni2). 뷰어에 넘길
#   .xyz/.vasp 에는 **원소 기호**가 가야 하므로 뒤 숫자를 뗀다.
def element(label):
    m = re.match(r"^([A-Z][a-z]?)", label)
    if not m:
        raise SystemExit(f"⛔ 라벨에서 원소를 못 읽었다: {label}")
    return m.group(1)


def write_xyz(path, elems, pos, comment):
    with open(path, "w") as f:
        f.write(f"{len(elems)}\n{comment}\n")
        for e, p in zip(elems, pos):
            f.write(f"{e:<3s} {p[0]:16.8f} {p[1]:16.8f} {p[2]:16.8f}\n")


def write_poscar(path, cell, elems, pos, comment):
    order, counts = [], []
    for e in elems:                      # 등장 순서 유지 (원자 순서를 안 흔든다)
        if not order or order[-1] != e:
            if e in order:               # 같은 원소가 떨어져 나오면 POSCAR 규격이 깨진다
                order, counts = None, None
                break
            order.append(e); counts.append(1)
        else:
            counts[-1] += 1
    if order is None:                    # → 원소별로 묶어서 다시 만든다
        uniq = sorted(set(elems), key=lambda x: elems.index(x))
        idx = [i for e in uniq for i, x in enumerate(elems) if x == e]
        elems = [elems[i] for i in idx]; pos = pos[idx]
        order = uniq; counts = [elems.count(e) for e in uniq]
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
    worst = None
    per_shift = {}
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
    ap.add_argument("--tag", default=None, help="출력 파일 접두어 (기본: 상위 디렉터리명)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    for path in a.scf_in:
        tag = a.tag or os.path.basename(os.path.dirname(os.path.abspath(path)))
        cell, labels, pos = read_scf_in(path)
        elems = [element(x) for x in labels]
        c_len = np.linalg.norm(cell[2])
        span = pos[:, 2].max() - pos[:, 2].min()
        comment = (f"{tag} | nat={len(elems)} | cell a={np.linalg.norm(cell[0]):.3f} "
                   f"b={np.linalg.norm(cell[1]):.3f} c={c_len:.3f} A | "
                   f"z-span={span:.3f} A | vertical vacuum={c_len - span:.3f} A | "
                   f"UNRELAXED single-point geometry from {os.path.abspath(path)}")
        write_xyz(os.path.join(a.out, f"{tag}.xyz"), elems, pos, comment)
        write_poscar(os.path.join(a.out, f"{tag}.vasp"), cell, elems, pos, comment)

        worst, per_shift = image_check(cell, labels, pos)
        print(f"\n══ {tag}  (nat {len(elems)}) ══")
        print(f"  cell  a {np.linalg.norm(cell[0]):.3f}  b {np.linalg.norm(cell[1]):.3f}"
              f"  c {c_len:.3f} A")
        print(f"  z-span {span:.3f} A  →  수직 진공 {c_len - span:.3f} A")
        print(f"  ⚑ 모든 이웃셀 통틀어 최소 원자간 거리 "
              f"{worst[0]:.3f} A  ({worst[1]}↔{worst[2]}, shift {worst[3]})")
        for sh, lab in ((( 0, 0, 1), "c 축 위 (샌드위치 위험 방향)"),
                        ((1, 0, 0), "a 축 옆 (분자-분자 피복률)"),
                        ((0, 1, 0), "b 축 옆 (분자-분자 피복률)")):
            r = per_shift[sh]
            print(f"    {lab:28s} {r[0]:7.3f} A  ({r[1]}↔{r[2]})")
        # ⚠ 판정선은 물리다: 결합거리(~1.5-2.2 A)에 들어가면 그 자세는 못 쓴다.
        #   3 A 미만이면 vdW 접촉이라 결합에너지에 섞인다 → 재설계.
        if worst[0] < 2.5:
            print("  ⛔ 결합거리다 — 이미지 샌드위치. 이 자세로 낸 E_bind 는 단일표면 값이 아니다.")
        elif worst[0] < 3.5:
            print("  ⚠ vdW 접촉 영역 — E_bind 에 이미지 상호작용이 섞인다. 셀을 키울 것.")
        else:
            print("  ✓ 이미지 분리 확보 (2026-07-17 철회 사유 없음)")
        print(f"  → {a.out}/{tag}.xyz + {tag}.vasp")


if __name__ == "__main__":
    main()
