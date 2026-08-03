#!/usr/bin/env python3
"""build_linio2_slab.py — LiNiO2(104) 슬랩을 처음부터 다시 짓는다 + **결합길이 게이트**.

왜 새로 짓나 (2026-08-03)
  기존 기준 슬랩(`reference_dft_v2/scf_u62.in` 및 거기서 추출한 db/structures/*.vasp)은
  **Li24Ni24O48 산화물인데 2.5 A 미만 원자쌍이 0개**였다. Ni-O 최단 3.667 A, Li-Ni 7.095 A,
  같은 면적의 (104) 층에 원자가 1/3 만 있다. ASE 로 독립 판독해도 동일 → 파싱 문제가 아니라
  구조가 깨진 것. 그 위에서 두 달치 Phase-A/Phase-B/표면 MD 가 돌았다.

⚠⚠ **왜 두 달간 안 걸렸나 — 이 파일의 존재 이유**
  기존 검증(`extract_scf_slab.py`)은 "Ni z-층이 4개씩 6밴드인가"만 봤다. 그건 **대리 지표**라
  깨진 구조도 통과한다. 물리적 **불변량은 결합길이**다: 어떤 산화물이든 양이온-음이온
  결합이 1.8-2.2 A 에 반드시 있다. 그래서 이 스크립트는
  **게이트를 통과하지 못하면 파일을 아예 쓰지 않는다.** 경고만 찍고 넘어가지 않는다.

  python3 tools/sdcp/build_linio2_slab.py --layers 6 --vacuum 10 --supercell 4 1 \
      --out db/structures/linio2_104_rebuilt
"""
import argparse
import sys

import numpy as np
from ase import Atoms
from ase.build import surface
from ase.io import write
from ase.neighborlist import neighbor_list

# LiNiO2, R-3m (alpha-NaFeO2 형). 육방정 설정.
A_HEX, C_HEX = 2.878, 14.19
# 문헌 결합길이 — 게이트의 기준. NiO6 가 LiO6 보다 작다.
REF = {("Ni", "O"): 1.97, ("Li", "O"): 2.11}
TOL = 0.15                      # +-15 %


def build_bulk(z_o):
    """3a Li (0,0,0) · 3b Ni (0,0,1/2) · 6c O (0,0,+-z). R-centering 3중."""
    cell = [[A_HEX, 0, 0], [-A_HEX / 2, A_HEX * np.sqrt(3) / 2, 0], [0, 0, C_HEX]]
    sym, frac = [], []
    for d in [(0, 0, 0), (1 / 3, 2 / 3, 2 / 3), (2 / 3, 1 / 3, 1 / 3)]:
        sym += ["Li", "Ni", "O", "O"]
        frac += [d, (d[0], d[1], d[2] + 0.5),
                 (d[0], d[1], d[2] + z_o), (d[0], d[1], d[2] - z_o)]
    return Atoms(sym, scaled_positions=np.array(frac) % 1.0, cell=cell, pbc=True)


def pair_min(at, A, B):
    s = at.get_chemical_symbols()
    ia = [i for i, x in enumerate(s) if x == A]
    ib = [i for i, x in enumerate(s) if x == B]
    if not ia or not ib:
        return None
    d = at.get_all_distances(mic=True)[np.ix_(ia, ib)]
    if A == B:
        d = np.where(d < 1e-8, np.inf, d)
    return float(d.min())


def solve_z():
    """O 의 z 자유도를 문헌 Ni-O 1.97 A 에 맞춘다 (구조를 손으로 안 믿는다)."""
    best = None
    for z in np.linspace(0.20, 0.30, 2001):
        err = abs(pair_min(build_bulk(z), "Ni", "O") - REF[("Ni", "O")])
        if best is None or err < best[1]:
            best = (z, err)
    return best[0]


def gate(at, label):
    """⚠ 통과 못 하면 **예외를 던진다**. 경고만 찍고 파일을 쓰면 이 사고가 재발한다."""
    s = at.get_chemical_symbols()
    d = at.get_all_distances(mic=True)
    np.fill_diagonal(d, np.inf)
    ok, lines = True, [f"── 결합길이 게이트: {label} (nat {len(at)}, {at.symbols.formula})"]
    gmin = float(d.min())
    lines.append(f"   전체 최단 원자간 거리 {gmin:.3f} A")
    if gmin > 2.5:
        ok = False
        lines.append("   ⛔ 2.5 A 미만 원자쌍이 하나도 없다 — 산화물일 수 없다")
    for (A, B), ref in REF.items():
        got = pair_min(at, A, B)
        if got is None:
            continue
        good = abs(got - ref) <= TOL * ref
        ok &= good
        lines.append(f"   {A}-{B} 최단 {got:.3f} A  (기준 {ref} +-{TOL:.0%}) "
                     f"{'OK' if good else '⛔'}")
    # 배위수 — 결합길이만 맞고 **개수**가 틀린 경우를 잡는다.
    # ⚠ get_all_distances 로 세면 안 된다: 쌍당 최소이미지 **하나**만 주므로, 같은 O 사이트의
    #   다른 주기이미지가 이웃인 경우를 통째로 놓친다(12원자 셀에서 Ni CN 이 6 대신 2로 나왔다).
    #   neighbor_list 는 이미지를 전부 펼치므로 이게 유일하게 맞는 방법이다.
    ii, jj = neighbor_list("ij", at, 2.4)
    cn = [int(sum(1 for k, x in zip(ii, jj) if k == i and s[x] == "O"))
          for i, x in enumerate(s) if x == "Ni"]
    lines.append(f"   Ni 의 O 배위수: 최소 {min(cn)} / 최대 {max(cn)} (벌크 6, 표면 4-5)")
    if max(cn) != 6:
        ok = False
        lines.append("   ⛔ 6배위 Ni 가 하나도 없다 — 내부 층이 없거나 구조가 깨졌다")
    print("\n".join(lines))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", type=int, default=6)
    ap.add_argument("--vacuum", type=float, default=10.0)
    # ⚠ ASE 의 (104) 표면 셀은 a=18.272 · b=2.878 로 나온다. 원본 셀(11.512 x 18.272)에
    #   맞추려면 **b 를 4배** 해야 한다 (1 x 4). 축을 헷갈리면 a 가 73 A 로 튄다(실측).
    ap.add_argument("--supercell", type=int, nargs=2, default=[1, 4],
                    help="면내 반복. 1 4 = 18.272 x 11.512 A (원본과 같은 면적)")
    ap.add_argument("--out", required=True, help="확장자 없는 출력 접두어")
    a = ap.parse_args()

    z_o = solve_z()
    bulk_ = build_bulk(z_o)
    print(f"O z 자유도 = {z_o:.4f} (Ni-O 를 문헌 1.97 A 에 맞춰 역산)")
    if not gate(bulk_, "bulk LiNiO2"):
        sys.exit("⛔ 벌크가 게이트를 통과 못 했다 — 슬랩을 자를 이유가 없다")

    sl = surface(bulk_, (1, 0, 4), layers=a.layers, vacuum=a.vacuum / 2)
    sl = sl.repeat((a.supercell[0], a.supercell[1], 1))
    sl.set_pbc(True)
    print(f"\n(104) 슬랩: 면내 |a|={np.linalg.norm(sl.cell[0]):.3f} "
          f"|b|={np.linalg.norm(sl.cell[1]):.3f} c={np.linalg.norm(sl.cell[2]):.3f} A")
    if not gate(sl, "LiNiO2(104) slab"):
        sys.exit("⛔ 슬랩이 게이트를 통과 못 했다 — **파일을 쓰지 않는다**")

    write(f"{a.out}.vasp", sl, format="vasp", direct=False)
    write(f"{a.out}.xyz", sl)
    print(f"\n✓ 게이트 통과 → {a.out}.vasp + .xyz")


if __name__ == "__main__":
    main()
