#!/usr/bin/env python3
"""export_phaseB_poses.py — Phase-B 에 들어간 **초기 자세**를 배포용으로 뽑는다.

왜 필요한가
  Phase-B 는 며칠 걸리는데, 그동안 "지금 무슨 구조를 계산하고 있나" 를 눈으로 볼 방법이
  없다. Phase-A 산출물은 `.xyz` 뿐이라 **격자가 없어** VESTA 에서 타일링이 안 된다.

⚠ CLAUDE.md 규율 — 구조 배포는 **xyz + POSCAR(.vasp) 페어**다.
  xyz 는 격자가 없으므로 Boundary 타일링은 .vasp 로 봐야 한다.
  그리고 셀은 **Phase-B 가 실제로 쓰는 c-shrink 셀**을 쓴다 — Phase-A 의 원본 셀이 아니다.
  (그래야 화면에서 보는 것과 계산하는 것이 같다.)

  python3 tools/sdcp/export_phaseB_poses.py                 # 기본 경로
  python3 tools/sdcp/export_phaseB_poses.py --out ~/poses   # 다른 곳에
"""
import argparse
import os
import sys

from ase.io import read, write

DEF_SCAN = "/data/work/runs/sdcp_v2/phaseA"
DEF_PB = "/data/work/runs/sdcp_v2/phaseB"
POSES = {
    "doped": "doped_sulfonate_down_r90_g22",
    "neutral": "neutral_sulfonate_down_r180_g01",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default=DEF_SCAN)
    ap.add_argument("--phaseb", default=DEF_PB)
    ap.add_argument("--out", default=os.path.join(DEF_PB, "poses_export"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    cshrink = os.path.join(a.phaseb, "slab_cshrink.vasp")
    cell = None
    if os.path.isfile(cshrink):
        cell = read(cshrink).cell.array.copy()
        print(f"셀 출처: {cshrink}  (c = {cell[2][2]:.3f} Å — Phase-B 가 실제로 쓰는 셀)")
    else:
        print(f"⚠ {cshrink} 가 아직 없다 — Phase-A 슬랩 셀로 대체한다.")
        print("   ⚠ 그러면 화면의 진공 두께가 실제 계산과 다르다.")

    n = 0
    for tag, label in POSES.items():
        src = os.path.join(a.scan, f"complex_{label}.xyz")
        if not os.path.isfile(src):
            print(f"⛔ 없음: {src}")
            continue
        at = read(src)
        if cell is None:
            sl = os.path.join(os.path.dirname(__file__), "..", "..",
                              "db/structures/linio2_104_sym_1x4L4_relaxed.vasp")
            cell = read(sl).cell.array.copy()
        at.set_cell(cell)
        at.set_pbc(True)
        base = os.path.join(a.out, f"phaseB_{tag}_{label}")
        write(base + ".vasp", at, format="vasp", direct=False)
        write(base + ".xyz", at)
        zmol = at.positions[-1, 2]
        print(f"✓ {tag:8s} {label}")
        print(f"    {base}.vasp  +  .xyz   ({len(at)} 원자)")
        n += 1

    if n:
        print("\n⚠ VESTA 에서: **.vasp 로 열어야** Boundary 타일링이 된다(xyz 는 격자가 없다).")
        print("⚠ 이건 **초기 자세**다 — Phase-B 는 SCF(single-point)라 좌표가 안 바뀐다.")
        print("   즉 이 구조가 곧 계산 대상이고, 최종 구조이기도 하다.")
    return 0 if n else 1


if __name__ == "__main__":
    sys.exit(main())
