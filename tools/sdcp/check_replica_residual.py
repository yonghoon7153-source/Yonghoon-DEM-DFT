#!/usr/bin/env python3
"""check_replica_residual.py — 1x1 이완 좌표를 1x4 로 복제했을 때 **인공 구속이 없었나**.

왜 필요한가
  `make_slab_relax.py --harvest` 는 1x1 셀에서 이완한 좌표를 그대로 1x4 로 복제한다.
  그런데 1x1 주기는 **모든 복제 단위가 똑같이 움직이도록 강제**한다. 실제 표면이
  주기를 깨는 재구성(예: 산소 이합체화, 지그재그)을 원한다면 1x1 이완은 그 자유도를
  애초에 안 준 것이고, 복제본은 **진짜 최소가 아니다**.
  판별은 간단하다 — 복제본에서 **잔여력**이 크면 주기를 깨고 싶어한다는 뜻이다.

  ⚠ QE 로 확인하면 또 몇 시간이다. UMA 단일점이면 몇 초에 같은 질문에 답한다.
    (절대 에너지가 아니라 **힘의 크기·분포**만 보므로 MLIP 로 충분하다.)

판정
  · 최대 |F| < 0.05 eV/A          → ✅ 복제 타당. 1x4 를 그대로 쓴다.
  · 0.05 – 0.15 eV/A              → ⚠ 경계. 어느 원자/층인지 보고 판단.
  · > 0.15 eV/A                   → ⛔ 재구성 신호. **1x4 를 직접 이완**해야 한다.

  ⚠⚠ **UMA 는 절대 판정자가 아니다.** 이 도구는 '주기를 깨고 싶어하는가' 라는
    **정성 질문**에만 쓴다. 힘의 절대값을 DFT 값처럼 인용하지 않는다.
  ⚠ 그리고 1x1 이완은 **DFT+U(U=6.2)** 로 했는데 UMA 는 그 U 를 모른다. 그래서
    "UMA 힘이 작다"는 "DFT 힘도 작다"의 증명이 아니다 — **큰 쪽이 나오면 확실한 경고**,
    작게 나오면 '경고 없음' 까지만.

  python3 tools/sdcp/check_replica_residual.py \\
      --struct db/structures/linio2_104_sym_1x4L4_relaxed.vasp
  python3 tools/sdcp/check_replica_residual.py --struct ... --unit-cells 4 --device cuda
"""
import argparse
import sys

import numpy as np
from ase.io import read


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", default="db/structures/linio2_104_sym_1x4L4_relaxed.vasp")
    ap.add_argument("--unit-cells", type=int, default=4,
                    help="복제 배수 (b 축). 복제 단위 간 힘 차이를 보려면 필요")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--warn", type=float, default=0.05, help="eV/A")
    ap.add_argument("--fail", type=float, default=0.15, help="eV/A")
    a = ap.parse_args()

    at = read(a.struct)
    at.set_pbc(True)
    print(f"구조 {a.struct} — {len(at)}원자 · 셀 {np.diag(at.cell.array).round(3)}")

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    at.calc = FAIRChemCalculator(
        pretrained_mlip.get_predict_unit(a.model, device=a.device), task_name=a.task)

    f = at.get_forces()
    mag = np.linalg.norm(f, axis=1)
    fmax = mag.max()
    print(f"\n최대 |F| = {fmax:.4f} eV/Å  ·  평균 {mag.mean():.4f}  "
          f"(UMA {a.model}/{a.task} — 정성 판정용)")

    # ── 어디가 큰가: z 층별 ────────────────────────────────────────────────
    z = at.positions[:, 2]
    order = np.argsort(z)
    layers, cur = [], [order[0]]
    for k in order[1:]:
        if z[k] - z[cur[-1]] <= 0.35:
            cur.append(k)
        else:
            layers.append(cur); cur = [k]
    layers.append(cur)
    print(f"\n층별 최대 |F| ({len(layers)}층, 같은 층 = Δz ≤ 0.35 Å)")
    for L in layers:
        zc = z[L].mean()
        m = mag[L].max()
        flag = "⛔" if m > a.fail else ("⚠" if m > a.warn else "  ")
        syms = "".join(sorted(set(at.get_chemical_symbols()[i] for i in L)))
        print(f"  {flag} z≈{zc:6.2f} Å  {len(L):3d}원자 ({syms:6s})  max|F| {m:.4f}")

    # ── ★ 복제 단위 사이가 갈리나 — 이게 '주기를 깨고 싶어한다' 의 직접 증거 ──
    # 복제본이면 같은 자리의 원자가 unit-cells 개씩 있고, 힘이 **똑같아야** 한다.
    # 갈리면 그 자리가 서로 다른 방향으로 가고 싶다는 뜻 = 재구성 요구.
    n = len(at)
    if a.unit_cells > 1 and n % a.unit_cells == 0:
        per = n // a.unit_cells
        blocks = mag.reshape(a.unit_cells, per) if _is_block_replica(at, a.unit_cells) \
            else None
        if blocks is None:
            blocks = np.array([mag[i::a.unit_cells] for i in range(a.unit_cells)])
        spread = blocks.max(axis=0) - blocks.min(axis=0)
        print(f"\n복제 단위 간 |F| 편차 — 최대 {spread.max():.4f} eV/Å "
              f"(평균 {spread.mean():.4f})")
        if spread.max() > a.warn:
            print("  ⛔ **복제 단위끼리 힘이 갈린다** = 같은 자리가 서로 다른 방향을 원한다.")
            print("     1x1 주기가 재구성을 막고 있었다는 직접 신호다 → 1x4 직접 이완.")
        else:
            print("  ✅ 복제 단위 간 차이 없음 — 1x1 주기가 인공 구속을 걸지 않았다.")

    # ── 종합 ───────────────────────────────────────────────────────────────
    print("\n판정")
    if fmax < a.warn:
        print(f"  ✅ 최대 |F| {fmax:.4f} < {a.warn} eV/Å — **복제 타당**. 1x4 를 그대로 쓴다.")
        print("     ⚠ 단 UMA 는 U=6.2 를 모른다 — '경고 없음' 까지이지 DFT 검증이 아니다.")
    elif fmax < a.fail:
        print(f"  ⚠ 최대 |F| {fmax:.4f} — 경계. 위 층별/복제편차를 보고 판단한다.")
        print("     표면 최상층만 크면 UMA 의 표면 기술 한계일 수 있다(내부층이 크면 진짜 문제).")
    else:
        print(f"  ⛔ 최대 |F| {fmax:.4f} > {a.fail} eV/Å — **재구성 신호**.")
        print("     1x4 를 직접 이완해야 한다. 복제본을 그대로 쓰면 잘못된 기준점이 된다.")
    return 0


def _is_block_replica(at, k):
    """ase 의 repeat 는 블록 순서로 쌓는다 — 그 가정이 맞는지 좌표로 확인."""
    n = len(at) // k
    s0 = at.get_chemical_symbols()[:n]
    return all(at.get_chemical_symbols()[i * n:(i + 1) * n] == s0 for i in range(k))


if __name__ == "__main__":
    sys.exit(main())
