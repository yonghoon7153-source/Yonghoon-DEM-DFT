#!/usr/bin/env python3
"""contact_map.py — 흡착 복합체에서 **분자와 표면이 실제로 닿아 있나**를 잰다.

왜 필요한가 (2026-08-06 1저자 질문: "실제로 Li이랑 결합이 있는거야?")
  VESTA 가 분자–슬랩 사이에 선을 안 긋는 것은 **근거가 아니다**. VESTA 의 결합 탐색은
  기본 쌍 목록·거리 컷오프에 의존하고, Li–O 는 기본 목록에 없는 경우가 많다.
  "선이 없다" ≠ "결합이 없다". 그래서 거리를 직접 재고, 기준과 대 놓고 비교한다.

무엇을 재나
  · 분자 원자 ↔ 슬랩 원자 최단거리 상위 N쌍 (PBC 최소이미지)
  · 원소별 최단: Li · Ni · O(슬랩) 각각 — "Li 랑 붙었나"가 이 줄로 답이 된다
  · 각 쌍을 **공유결합 반지름 합**과 비교해 접촉/결합/비접촉을 판정
  · ⚠ 판정은 거리일 뿐이다. 결합 여부의 최종 근거는 전자구조(ICOHP/Bader)이지
    거리가 아니다 — 여기서는 "결합이 있을 수 있는 거리인가"까지만 말한다.

  python3 tools/sdcp/contact_map.py \
      /data/work/runs/sdcp_v2/phaseB/poses_export/phaseB_doped_*.vasp --nslab 192
  python3 tools/sdcp/contact_map.py <복합체.xyz> --nslab 192 --slab <슬랩.vasp>
"""
import argparse
import sys

import numpy as np
from ase.data import atomic_numbers, covalent_radii
from ase.io import read

# 참고 거리 — 산화물/유기 계면에서 흔히 인용되는 범위 (판정 보조용, 컷오프가 아니다)
REF = {
    "Li-O": (1.90, 2.20, "Li⁺–O 배위 (LiNiO₂ 벌크 Li–O ≈ 2.0–2.1 Å)"),
    "Ni-O": (1.85, 2.15, "Ni–O 팔면체"),
    "O-O":  (2.60, 3.20, "O···O 수소결합/van der Waals 접촉"),
    "O-H":  (1.60, 2.20, "O···H 수소결합"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("complex", help="복합체 구조 (.vasp 권장 — 격자가 있어야 PBC)")
    ap.add_argument("--nslab", type=int, default=192,
                    help="앞에서부터 슬랩 원자 수 (나머지가 분자). Phase-B 규약 = 192")
    ap.add_argument("--slab", default=None,
                    help="복합체가 .xyz 라 격자가 없을 때 셀을 빌려올 파일")
    ap.add_argument("--top", type=int, default=12, help="최단거리 상위 몇 쌍")
    ap.add_argument("--contact", type=float, default=1.25,
                    help="접촉 판정 = d < contact × (공유반지름 합). 1.25 는 관례적 여유")
    a = ap.parse_args()

    at = read(a.complex)
    if at.cell.rank < 3:
        if not a.slab:
            sys.exit("⛔ 격자가 없다 — --slab 으로 셀을 주거나 .vasp 를 써라 "
                     "(PBC 없이 잰 거리는 옆 이미지를 놓친다)")
        at.set_cell(read(a.slab).cell)
    at.set_pbc(True)

    n = len(at)
    if not (0 < a.nslab < n):
        sys.exit(f"⛔ --nslab {a.nslab} 이 원자수 {n} 과 안 맞는다")
    sym = at.get_chemical_symbols()
    slab_i = list(range(a.nslab))
    mol_i = list(range(a.nslab, n))

    print(f"구조 {a.complex}")
    print(f"  원자 {n} = 슬랩 {len(slab_i)} + 분자 {len(mol_i)}   "
          f"셀 c={at.cell.array[2][2]:.3f} Å")
    print(f"  분자 조성 {''.join(sorted(set(sym[i] for i in mol_i)))} · "
          f"분자 z 범위 {at.positions[mol_i, 2].min():.2f}–{at.positions[mol_i, 2].max():.2f} Å · "
          f"슬랩 top {at.positions[slab_i, 2].max():.2f} Å")
    print("─" * 74)

    # PBC 최소이미지 거리 — 전 쌍. 6-7천 쌍이라 통째로 돌려도 된다.
    pairs = []
    for m in mol_i:
        d = at.get_distances(m, slab_i, mic=True)
        for k, s in enumerate(slab_i):
            pairs.append((d[k], m, s))
    pairs.sort()

    def rcov(i, j):
        return (covalent_radii[atomic_numbers[sym[i]]]
                + covalent_radii[atomic_numbers[sym[j]]])

    print(f"① 최단거리 상위 {a.top}쌍  (분자원자 ↔ 슬랩원자)")
    for d, m, s in pairs[:a.top]:
        r = rcov(m, s)
        ratio = d / r
        key = "-".join(sorted((sym[m], sym[s])))
        lo, hi, note = REF.get(key, (None, None, ""))
        # ⚠ Li–O 는 이온결합이라 공유반지름 합이 기준으로 부적절하다(항상 '멀다'로 읽힌다).
        #   참고범위가 있는 쌍은 그 범위를 우선 적용한다.
        if lo is not None:
            tag = ("★ 배위 거리" if d <= hi else
                   "· 접촉" if d <= hi * 1.25 else "  (떨어짐)")
        else:
            tag = ("★ 결합 거리" if ratio < 1.0 else
                   "· 접촉" if ratio < a.contact else "  (떨어짐)")
        print(f"   {sym[m]:>2s}{m:<4d} ↔ {sym[s]:>2s}{s:<4d}  d={d:5.2f} Å  "
              f"(Σr_cov {r:4.2f}, d/Σr {ratio:4.2f})  {tag}"
              + (f"   ← {note}" if note else ""))

    print("\n② 슬랩 원소별 최단 — **'Li 랑 붙었나'는 이 줄이 답한다**")
    verdict_li = None
    for el in ("Li", "Ni", "O"):
        cand = [p for p in pairs if sym[p[2]] == el]
        if not cand:
            print(f"   {el:2s} : 슬랩에 없음"); continue
        d, m, s = cand[0]
        r = rcov(m, s)
        lo, hi, _ = REF.get("-".join(sorted((sym[m], el))), (None, None, ""))
        near = d <= (hi * 1.25 if hi else a.contact * r)
        state = ("★ 배위/결합 거리" if d <= (hi if hi else r) else
                 "· 접촉" if near else "  떨어짐")
        print(f"   {el:2s} : {d:5.2f} Å  ({sym[m]}{m} ↔ {el}{s}, "
              + (f"기준 {lo:.2f}–{hi:.2f}" if hi else f"Σr_cov {r:4.2f}") + f")  {state}")
        if el == "Li":
            verdict_li = (d, sym[m], near)

    print("\n③ 판정")
    dmin = pairs[0][0]
    if dmin > 3.5:
        print(f"   ⛔ 최단 접촉이 {dmin:.2f} Å — **어떤 화학결합도 아니다.**")
        print("      이 자세의 E_ads 는 사실상 **분산력(vdW)** 뿐이다. 그러면 Δ 도 "
              "'어느 쪽이 더 잘 분산상호작용하나'를 재는 것이고, D3 보정 파라미터에 "
              "그대로 의존한다 — 논문에서 '결합' 이라고 쓰면 안 된다.")
    elif dmin > 2.6:
        print(f"   · 최단 {dmin:.2f} Å — 물리흡착(physisorption) 영역. 수소결합/vdW 접촉.")
        print("      '화학결합(chemisorption)' 이라고 부르려면 전하이동 근거가 따로 필요하다.")
    else:
        print(f"   ★ 최단 {dmin:.2f} Å — 화학결합이 있을 수 있는 거리다.")
        print("      ⚠ 단, **거리는 결합의 증거가 아니다.** Löwdin/Bader 전하나 ICOHP 로 "
              "확인해야 '결합' 이라고 쓸 수 있다.")
    if verdict_li:
        d, other, close = verdict_li
        print(f"   Li 에 대해서는: 최단 {d:.2f} Å ({other}···Li) — "
              + ("**배위로 볼 만하다**" if close else "**결합이라 부를 거리가 아니다**"))
    print("\n   ⚠ 이건 **초기 자세**다 (Phase-B 는 single-point SCF — 좌표가 안 바뀐다).")
    print("      즉 여기서 안 닿아 있으면 계산이 끝나도 안 닿아 있다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
