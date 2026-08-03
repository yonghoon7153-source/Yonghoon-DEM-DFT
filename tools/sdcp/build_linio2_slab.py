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

  python3 tools/sdcp/build_linio2_slab.py --layers 4 --vacuum 14 --supercell 1 2 \
      --out db/structures/linio2_104_rebuilt

셀 크기 고르기 (문헌 감각)
  (104) 의 **원시** 2D 셀은 2.878 x 5.781 A = 16.64 A^2, 층당 4원자(LiNiO2 1 화학식)로 아주 작다.
  문헌의 NCM/LiNiO2(104) 흡착 계산이 가벼운 이유가 이것이다 — 보통 원시셀 1-6개를 쓴다.
  ⚠ ase.build.surface 에 12원자 육방정 셀을 주면 ASE 는 R-centering 이 만드는 면내 병진
    [-4/3,-2/3,1/3](5.781 A)을 못 보고 **원시셀의 3배**(2.878 x 18.272, 층당 12원자)를 낸다.
    원하는 면적은 반복 수로 전부 도달하므로 그대로 쓰되, 아래 표의 기준이 그 3배 셀임을 기억할 것.

    반복   층   원자수   표면적       비고
    1x1    4     48     49.9 A^2    작은 분자 / 깨끗한 표면 에너지
    1x2    4     96     99.8        **깨진 원본과 같은 원자수, 진짜 구조**
    1x2    6    144     99.8        두꺼운 슬랩
    1x3    4    144    149.7
    2x2    4    192    199.6        깨진 원본과 **같은 면적**(측면 이미지 거리 보존)
"""
import argparse
import sys

import numpy as np
from ase import Atoms
from ase.build import surface
from ase.io import write
from ase.neighborlist import neighbor_list
from collections import Counter

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


def planes(at, tol=0.3):
    """z 로 원자를 (104) 면 단위로 묶는다."""
    order = np.argsort(at.positions[:, 2])
    s = at.get_chemical_symbols()
    g = [[order[0]]]
    for k in order[1:]:
        if at.positions[k, 2] - at.positions[g[-1][-1], 2] > tol:
            g.append([])
        g[-1].append(k)
    return [(float(at.positions[q, 2].mean()), dict(Counter(s[i] for i in q))) for q in g]


def ni_cn(at, cut=2.4):
    """Ni 별 O 배위수. neighbor_list 로 주기이미지까지 편다."""
    ii, jj = neighbor_list("ij", at, cut)
    s = at.get_chemical_symbols()
    return {i: sum(1 for k, x in zip(ii, jj) if k == i and s[x] == "O")
            for i, x in enumerate(s) if x == "Ni"}


def find_shift(z_o, layers, vacuum):
    """bulk 를 c 방향으로 얼마나 밀고 잘라야 **대칭·정본 종단**이 나오나.

    ⚠⚠ **shift 0 으로 자르면 안 된다 (2026-08-03, 설계 리뷰가 잡아냄).** 완전한 (104) 면
      하나가 셀 경계에서 쪼개져서 위는 **순수 O3 면**, 아래는 Li3Ni3O3 이 된다. 비대칭이고,
      더 나쁘게 자세 스캔은 z 최대면 위에 분자를 얹으므로 **Ni 없는 산소면에 흡착**시킨다 —
      (104) 의 정본 표면(5배위 Ni 노출)이 아니다. Ni 3개는 배위수 3까지 떨어진다.
      **결합길이 게이트는 이걸 통과시킨다** — 결합길이는 다 정상이라서. 원래 사고와 같은 패턴.
    """
    best = None
    for sh in np.linspace(0, 1, 65)[:-1]:
        bb = build_bulk(z_o)
        f = bb.get_scaled_positions(); f[:, 2] = (f[:, 2] + sh) % 1.0
        bb.set_scaled_positions(f)
        sl = surface(bb, (1, 0, 4), layers=layers, vacuum=vacuum / 2)
        P = planes(sl)
        if len(P) < 2 or P[0][1] != P[-1][1]:
            continue
        cn = sorted(ni_cn(sl).values())
        if not cn or min(cn) < 5 or max(cn) != 6:
            continue
        # 표면 Ni 가 정확히 CN 5, 내부가 6 인 것 중 면이 가장 많은(=온전한) 것
        score = (len(P), -abs(sh - 0.0625))
        if best is None or score > best[0]:
            best = (score, float(sh), P, cn)
    if best is None:
        sys.exit("⛔ 어떤 z-shift 로도 대칭 (104) 종단이 안 나온다 — layers 를 바꿔 볼 것")
    return best[1], best[2], best[3]


def gate(at, label, is_slab=True):
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
    lines.append(f"   Ni 의 O 배위수: 최소 {min(cn)} / 최대 {max(cn)} (벌크 6, 표면 5)")
    if max(cn) != 6:
        ok = False
        lines.append("   ⛔ 6배위 Ni 가 하나도 없다 — 내부 층이 없거나 구조가 깨졌다")
    # ⚠⚠ 아래 세 검사가 2026-08-03 에 추가된 것이다. 결합길이만 보는 게이트는
    #   "윗면이 순수 O3 인 비대칭 슬랩"을 **통과시켰다** — 결합길이는 다 정상이니까.
    #   분자가 붙는 면이 뭔지가 결합에너지를 결정하므로 여기서 막아야 한다.
    if is_slab and min(cn) < 5:
        ok = False
        lines.append(f"   ⛔ 배위수 {min(cn)} 인 Ni 가 있다 — 종단이 정본 (104)(표면 CN 5)이 아니다")
    if not is_slab:
        print("\n".join(lines))
        return ok
    P = planes(at)
    top, bot = P[-1][1], P[0][1]
    same = (top == bot)
    lines.append(f"   종단면  아래 {bot}  /  위 {top}  {'일치' if same else '⛔ 불일치'}")
    if not same:
        ok = False
        lines.append("   ⛔ 비대칭 슬랩 — 분자가 붙는 윗면이 아랫면과 다른 화학종이다")
    if "Ni" not in top:
        ok = False
        lines.append("   ⛔ 윗면에 Ni 가 없다 — 흡착 자리(5배위 Ni)가 노출돼 있지 않다")
    lines.append(f"   (104) 면 {len(P)}장 · 두께 {at.positions[:, 2].max() - at.positions[:, 2].min():.2f} A")
    print("\n".join(lines))
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layers", type=int, default=6)
    # ⚠ 진공은 **분자 꼭대기 → 다음 슬랩 바닥 15 A** 가 기준이다 (디폴 보정 톱니파가
#   밀도 없는 구간에 앉아야 한다). 여기 값은 맨 슬랩용이고 복합체는 더 필요하다.
    ap.add_argument("--vacuum", type=float, default=20.0)
    # ⚠ ASE 의 (104) 표면 셀은 a=18.272 · b=2.878 로 나온다. 원본 셀(11.512 x 18.272)에
    #   맞추려면 **b 를 4배** 해야 한다 (1 x 4). 축을 헷갈리면 a 가 73 A 로 튄다(실측).
    ap.add_argument("--supercell", type=int, nargs=2, default=[1, 4],
                    help="면내 반복 (ASE (104) 셀 2.878 x 18.272 = 49.9 A^2, 층당 12원자 기준)")
    ap.add_argument("--out", required=True, help="확장자 없는 출력 접두어")
    a = ap.parse_args()

    z_o = solve_z()
    bulk_ = build_bulk(z_o)
    print(f"O z 자유도 = {z_o:.4f} (Ni-O 를 문헌 1.97 A 에 맞춰 역산)")
    if not gate(bulk_, "bulk LiNiO2", is_slab=False):
        sys.exit("⛔ 벌크가 게이트를 통과 못 했다 — 슬랩을 자를 이유가 없다")

    sh, P0, cn0 = find_shift(z_o, a.layers, a.vacuum)
    print(f"\nz-shift = {sh:.4f} c 로 자른다 (대칭 종단 + 표면 Ni CN 5)")
    print(f"   완전한 (104) 면 {len(P0)}장, 종단 조성 {P0[0][1]}, Ni CN {sorted(set(cn0))}")
    bb = build_bulk(z_o)
    f = bb.get_scaled_positions(); f[:, 2] = (f[:, 2] + sh) % 1.0
    bb.set_scaled_positions(f)
    sl = surface(bb, (1, 0, 4), layers=a.layers, vacuum=a.vacuum / 2)
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
