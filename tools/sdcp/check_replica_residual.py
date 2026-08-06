#!/usr/bin/env python3
"""check_replica_residual.py — 1x1 이완 좌표를 1x4 로 복제해도 되나 (UMA, 몇 분).

왜 필요한가
  `make_slab_relax.py --harvest` 는 1x1 셀에서 이완한 좌표를 그대로 1x4 로 복제한다.
  1x1 주기는 **모든 복제 단위가 똑같이 움직이도록 강제**하므로, 실제 표면이 주기를 깨는
  재구성을 원한다면 복제본은 진짜 최소가 아니다. 그걸 QE 로 확인하면 또 며칠이다.

⚠⚠ **v1(2026-08-06)의 두 오류를 여기 남긴다 — 같은 함정을 다시 밟지 않기 위해.**

  ① **고정 원자를 안 걸렀다.** 슬랩은 아래 층을 `if_pos 0 0 0` 으로 얼려 벌크 자리에
     묶어 둔다. 그 원자들은 **애초에 이완되지 않았으므로 잔여력이 큰 게 설계대로**다.
     v1 은 전 원자의 max 를 보고 1.08 eV/A 라며 '재구성 신호' 판정을 냈는데, 그 1.08 은
     **얼려둔 기판**의 것이었다(자유층은 0.18/0.30). `_sdcp_maxcomp` 이 이미 못박아 둔
     함정을 새 도구에서 그대로 밟았다. → **자유 원자만 본다.**

  ② **'복제 단위 간 힘 편차' 는 판별력이 없다.** 정확한 4x 복제본은 모든 복제 단위의
     환경이 대칭적으로 동일하므로, 단일점 힘은 **대칭에 의해 반드시 같다** — 대칭 깨진
     상태가 더 낮든 말든 0 이 나온다. v1 은 그 0.0000 을 '인공 구속 없음' 의 증거로 읽었다.
     → 재구성 경향은 **대칭을 깨보고 되돌아오는지**로 본다(아래 --probe).

무엇을 보나
  A) **자유층 잔여력** — 복제본에서 자유 원자의 max|F|.
     ⚠ 이건 '복제가 타당한가' 의 **간접** 지표다. UMA 는 DFT+U(6.2)를 모르므로
       0.2 eV/A 급 불일치는 모델 차이만으로도 난다. 큰 값 = 확실한 경고, 작은 값 = 경고 없음.
  B) **대칭 깨짐 탐침 (--probe)** — 원자를 무작위로 살짝(기본 0.03 A) 흔든 뒤 UMA 로
     이완시켜, 복제 단위들이 **원래대로 되모이는지 / 갈라지는지** 본다. 이게 직접 증거다.
       · 되모인다(편차 작다)  → 1x1 주기가 진짜 최소. 복제 타당.
       · 갈라진다(편차 크다)  → 재구성을 원한다. 1x4 를 직접 이완해야 한다.

  python3 tools/sdcp/check_replica_residual.py \\
      --struct db/structures/linio2_104_sym_1x4L4_relaxed.vasp \\
      --relax-in /data/work/runs/sdcp_v2/slab_relax/relax.in --probe
"""
import argparse
import sys

import numpy as np
from ase.io import read


def free_mask_from_relax_in(in_path, n_unit, n_rep):
    """1x1 relax.in 의 if_pos → 1x4 복제본의 자유 마스크.

    ⚠ ase.repeat 는 **블록 순서**(unit0 전체 → unit1 전체 …)로 쌓는다. 마스크도 그 순서로 tile.
    """
    flags, on, n = [], False, 0
    for line in open(in_path, errors="ignore"):
        if line.lstrip().startswith("ATOMIC_POSITIONS"):
            on, n = True, 0
            continue
        if on:
            f = line.split()
            if len(f) < 4:
                break
            n += 1
            flags.append(not (len(f) >= 7 and f[4] == "0" and f[5] == "0" and f[6] == "0"))
    if len(flags) != n_unit:
        sys.exit(f"⛔ relax.in 의 원자 {len(flags)}개 != 1x1 단위 {n_unit}개")
    return np.tile(np.array(flags, bool), n_rep)


def layers_of(z, tol=0.35):
    order = np.argsort(z)
    out, cur = [], [order[0]]
    for k in order[1:]:
        if z[k] - z[cur[-1]] <= tol:
            cur.append(k)
        else:
            out.append(cur); cur = [k]
    out.append(cur)
    return out


def replica_spread(at, k, sel=None):
    """복제 단위별 좌표를 겹쳐 놓고 **같은 자리끼리** 벌어진 정도(A)."""
    n = len(at) // k
    p = at.get_positions().reshape(k, n, 3).copy()
    b = at.cell.array[1] / k                     # 복제 축 = b (make_slab_relax 규약)
    for j in range(k):
        p[j] -= b * j                            # 각 복제본을 원점으로 되돌린다
    d = p.max(axis=0) - p.min(axis=0)            # (n,3)
    if sel is not None:
        d = d[sel[:n]]
    return float(np.linalg.norm(d, axis=1).max()) if len(d) else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", default="db/structures/linio2_104_sym_1x4L4_relaxed.vasp")
    ap.add_argument("--relax-in", help="1x1 relax.in — if_pos 로 자유 원자를 가른다 (강력 권장)")
    ap.add_argument("--free-z-min", type=float,
                    help="relax.in 이 없을 때 대안: 이 z 이상을 자유로 본다 (A)")
    ap.add_argument("--unit-cells", type=int, default=4)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--model", default="uma-s-1p1")
    ap.add_argument("--task", default="omat")
    ap.add_argument("--warn", type=float, default=0.05)
    ap.add_argument("--fail", type=float, default=0.15)
    ap.add_argument("--probe", action="store_true",
                    help="★ 대칭 깨짐 탐침 — 흔든 뒤 UMA 이완시켜 복제가 갈라지나 본다")
    ap.add_argument("--amp", type=float, default=0.03, help="탐침 진폭 (A)")
    ap.add_argument("--fmax", type=float, default=0.02, help="탐침 이완 수렴 (eV/A)")
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    at = read(a.struct); at.set_pbc(True)
    k = a.unit_cells
    n_unit = len(at) // k
    print(f"구조 {a.struct} — {len(at)}원자 · 셀 {at.cell.lengths().round(3)} · 복제 {k}x")

    # ── 자유 원자 마스크 (① 의 교훈) ───────────────────────────────────────
    if a.relax_in:
        free = free_mask_from_relax_in(a.relax_in, n_unit, k)
        src = f"relax.in if_pos ({a.relax_in})"
    elif a.free_z_min is not None:
        free = at.positions[:, 2] >= a.free_z_min
        src = f"z >= {a.free_z_min} A"
    else:
        sys.exit("⛔ --relax-in (권장) 또는 --free-z-min 이 필요하다.\n"
                 "   고정 원자는 애초에 이완되지 않아 잔여력이 크다 — 안 걸르면 판정이 통째로 틀어진다.")
    print(f"자유 원자 {int(free.sum())}/{len(at)}  (출처: {src})")

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    def mk():
        return FAIRChemCalculator(
            pretrained_mlip.get_predict_unit(a.model, device=a.device), task_name=a.task)
    at.calc = mk()

    # ── A) 자유층 잔여력 ───────────────────────────────────────────────────
    mag = np.linalg.norm(at.get_forces(), axis=1)
    fmax_free = mag[free].max()
    print(f"\nA) 자유 원자 최대 |F| = {fmax_free:.4f} eV/Å (평균 {mag[free].mean():.4f})"
          f"   ※ 고정 원자 최대 {mag[~free].max():.4f} — **판정 대상 아님**")
    z = at.positions[:, 2]
    print("   층별 (자유/고정 구분)")
    for L in layers_of(z):
        L = np.array(L)
        nf = int(free[L].sum())
        tag = "자유" if nf == len(L) else ("고정" if nf == 0 else f"혼합 {nf}/{len(L)}")
        m = mag[L[free[L]]].max() if nf else mag[L].max()
        flag = "  " if (nf == 0 or m <= a.warn) else ("⛔" if m > a.fail else "⚠ ")
        print(f"   {flag} z≈{z[L].mean():6.2f} Å  {len(L):3d}원자 [{tag:>7s}]  max|F| {m:.4f}")
    print(f"   ⚠ UMA 는 DFT+U(6.2)를 모른다 — 0.2 eV/Å 급 불일치는 모델 차이만으로도 난다. "
          "이 값은 **간접** 지표다.")

    # ── B) 대칭 깨짐 탐침 (② 의 교훈) ─────────────────────────────────────
    if not a.probe:
        print("\nB) 대칭 깨짐 탐침 생략 — ⚠ **A 만으로는 재구성 여부를 못 가른다.**")
        print("   정확한 복제본은 대칭 때문에 복제 단위 간 힘이 **반드시** 같아서, 그 일치는")
        print("   증거가 되지 못한다. --probe 를 붙여 흔든 뒤 되모이는지 볼 것.")
        return 0

    from ase.constraints import FixAtoms
    from ase.optimize import FIRE
    rng = np.random.default_rng(a.seed)
    pr = at.copy()
    pr.set_constraint(FixAtoms(mask=~free))
    d0 = replica_spread(pr, k, free)
    pr.positions[free] += rng.normal(0, a.amp, (int(free.sum()), 3))
    d1 = replica_spread(pr, k, free)
    pr.calc = mk()
    print(f"\nB) 대칭 깨짐 탐침 — 진폭 {a.amp} Å 로 흔들고 UMA 이완 (fmax {a.fmax}, 최대 {a.steps}스텝)")
    print(f"   복제 단위 간 좌표 편차: 원본 {d0:.4f} Å → 흔든 뒤 {d1:.4f} Å")
    opt = FIRE(pr, logfile=None)
    opt.run(fmax=a.fmax, steps=a.steps)
    d2 = replica_spread(pr, k, free)
    conv = np.linalg.norm(pr.get_forces()[free], axis=1).max()
    print(f"   이완 {opt.get_number_of_steps()}스텝 후 편차 {d2:.4f} Å "
          f"(자유 max|F| {conv:.4f} eV/Å)")

    print("\n판정")
    if opt.get_number_of_steps() >= a.steps:
        print(f"   ⚠ 탐침 이완이 {a.steps}스텝 안에 안 끝났다 — --steps 를 올리고 다시 볼 것. 판정 보류.")
    elif d2 <= max(d0, 1e-3) * 3 or d2 < 0.02:
        print(f"   ✅ **되모였다** ({d1:.3f} → {d2:.3f} Å) — 흔들어도 1x1 주기로 돌아온다.")
        print("      1x1 이완이 인공 구속을 걸지 않았다는 **직접 증거**다. 복제본을 그대로 쓴다.")
        print(f"      ⚠ UMA 판정이다. A 의 자유층 잔여력({fmax_free:.3f})은 DFT+U 로 재보기 전엔"
              " 참고값이다.")
    else:
        print(f"   ⛔ **갈라졌다** ({d1:.3f} → {d2:.3f} Å) — 복제 단위가 서로 다른 자리로 간다.")
        print("      1x1 주기가 재구성을 막고 있었다는 뜻이다 → **1x4 를 직접 이완**해야 한다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
