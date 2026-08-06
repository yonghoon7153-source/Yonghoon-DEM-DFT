#!/usr/bin/env python3
"""extraction_probe.py — "neutral 은 Li 를 안 뽑는다" 를 **강한 형태로** 시험한다.

왜 필요한가 (2026-08-06)
  재스캔에서 doped 는 108 자세 중 9개가 Li 추출로 갔고 neutral 은 108/108 에서 안 갔다.
  ⚠ 그런데 "108개 출발점에서 못 찾았다"는 **"그 상태가 없다"가 아니다.** 심사에서
  정확히 이 지점을 찌른다. 탐색 실패와 상태 부재는 다른 얘기다.

  강한 시험: **doped 의 추출 기하를 그대로 두고 분자만 neutral 로 바꿔** 이완한다.
    · Li 가 격자로 되돌아가면 → neutral 은 추출 상태를 **유지조차 못 한다**. 주장이 세진다.
    · Li 가 그대로 있으면    → 추출 상태는 neutral 에도 **존재**하고 UMA 가 출발점에서
      못 갔을 뿐이다. 그러면 "neutral 은 안 뽑는다" 를 "UMA 는 neutral 의 추출 경로를
      찾지 못했다" 로 **약하게 다시 써야 한다.**
  어느 쪽이 나와도 논문이 정확해진다.

어떻게 neutral 을 만드나
  doped 는 술폰산에서 H 하나를 잃은 종이다(S–O 3개가 1.48 Å 로 균등). 되돌리려면
  그 세 O 중 하나에 H 를 0.99 Å 로 붙인다. **표면 Li 에 배위하지 않은 O** 를 고른다 —
  배위한 O 에 붙이면 인위적으로 배위를 깨는 셈이라 시험이 오염된다.
  ⚠ 이건 근사적 구성이다. 논문에 쓸 때 "doped 추출 기하에 양성자를 되돌려 얻은 구조"
    라고 그대로 밝힐 것. 진짜 neutral 최소가 아니다.

  python3 tools/sdcp/extraction_probe.py            # 기본 경로
  python3 tools/sdcp/extraction_probe.py --dry      # 구조만 만들고 이완은 안 함
"""
import argparse
import os
import sys

import numpy as np
from ase import Atoms
from ase.io import read, write

DEF_SCAN = "/data/work/runs/sdcp_v2/phaseA_top1free"
DEF_EXTR = "doped_sulfonate_down_r180_g20"      # 추출 챔피언 (Li 2.35 Å 이동)
DEF_SLAB = "/data/work/runs/sdcp_v2/slabref_085/slab_ref_relaxed.xyz"
OH = 0.99                                        # Å — 술폰산 O–H


def add_proton(at, nslab):
    """술폰산 O 중 **표면 Li 에 배위하지 않은** 것에 H 를 붙여 doped → neutral 로."""
    sym = at.get_chemical_symbols()
    mol = list(range(nslab, len(at)))
    li = [i for i in range(nslab) if sym[i] == "Li"]
    s_idx = [i for i in mol if sym[i] == "S"]
    if not s_idx:
        raise SystemExit("⛔ 분자에 S 가 없다")
    # 술폰산 S = O 를 3개 이상 달고 있는 S
    best, best_os = None, []
    for s in s_idx:
        os_ = [i for i in mol if sym[i] == "O"
               and at.get_distance(s, i, mic=True) < 1.8]
        if len(os_) > len(best_os):
            best, best_os = s, os_
    if len(best_os) < 3:
        raise SystemExit(f"⛔ 술폰산 S 를 못 찾았다 (S{best} 의 O {len(best_os)}개)")

    # 각 O 의 '표면 Li 최단거리' — 먼 O 가 배위에 안 쓰인 O 다
    dli = {o: min(at.get_distance(o, l, mic=True) for l in li) for o in best_os}
    tgt = max(dli, key=lambda o: dli[o])
    print(f"  술폰산 S{best} · O {best_os}")
    for o in best_os:
        print(f"    O{o} → 표면 Li 최단 {dli[o]:.2f} Å" + ("   ← 여기에 H" if o == tgt else ""))

    # H 방향: S→O 를 연장하고 표면에서 멀어지는 쪽으로 살짝 기울인다
    v = at.positions[tgt] - at.positions[best]
    v /= np.linalg.norm(v)
    v = v + np.array([0, 0, 0.5])          # 표면 반대(+z) 쪽으로
    v /= np.linalg.norm(v)
    h = at.positions[tgt] + OH * v
    out = at + Atoms("H", positions=[h])
    out.set_cell(at.cell); out.set_pbc(True)
    # ⚠ 새 H 가 다른 원자와 겹치면 시험이 무의미하다
    d = min(np.linalg.norm(out.positions[-1] - out.positions[i])
            for i in range(len(out) - 1))
    print(f"  H 배치: O{tgt} 에서 {OH} Å · 다른 원자와 최단 {d:.2f} Å")
    if d < 0.8:
        raise SystemExit("⛔ 새 H 가 다른 원자와 겹친다 — 방향을 바꿔야 한다")
    return out, tgt


def li_state(at, ref, nslab, tag):
    """추출된 Li 가 아직 나와 있나 — 맨 슬랩 대비 변위로 판정."""
    sym = at.get_chemical_symbols()
    d = np.linalg.norm(at.positions[:nslab] - ref.positions[:nslab], axis=1)
    i = int(np.argmax(d))
    mol = list(range(nslab, len(at)))
    dm = min(at.get_distance(i, m, mic=True) for m in mol)
    print(f"  [{tag}] 최대 변위 원자 {sym[i]}{i} = {d[i]:.2f} Å · 분자까지 {dm:.2f} Å · "
          f"0.5 Å 초과 {int((d > 0.5).sum())}개")
    return d[i], sym[i], dm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", default=DEF_SCAN)
    ap.add_argument("--pose", default=DEF_EXTR)
    ap.add_argument("--slabref", default=DEF_SLAB)
    ap.add_argument("--nslab", type=int, default=192)
    ap.add_argument("--freeze_frac", type=float, default=0.85)
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--out", default="/data/work/runs/sdcp_v2/extraction_probe")
    ap.add_argument("--dry", action="store_true", help="구조만 만들고 이완 안 함")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    src = os.path.join(a.scan, f"complex_{a.pose}.xyz")
    at = read(src)
    ref = read(a.slabref)
    at.set_cell(ref.cell); at.set_pbc(True)
    print(f"출발 기하: {src}  ({len(at)} 원자)")
    li_state(at, ref, a.nslab, "출발(doped 추출)")

    print("\n① doped → neutral 로 양성자 되돌리기")
    neu, o_h = add_proton(at, a.nslab)
    write(os.path.join(a.out, "start_neutral_from_doped_extr.xyz"), neu)
    write(os.path.join(a.out, "start_doped_extr.xyz"), at)
    if a.dry:
        print("\n--dry — 구조만 저장했다. 이완은 안 했다.")
        return 0

    from ase.constraints import FixAtoms
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    from ase.optimize import FIRE
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                              task_name="oc20")

    zs = ref.positions[:, 2]
    zcut = zs.min() + a.freeze_frac * (zs.max() - zs.min())
    fix = FixAtoms(indices=[i for i in range(a.nslab) if ref.positions[i, 2] < zcut])
    print(f"\n구속: freeze_frac {a.freeze_frac} → 슬랩 {a.nslab - len(fix.index)}원자 자유 "
          f"+ 분자 전부 자유 (재스캔과 동일)")

    print("\n② 이완 — 대조군(doped 추출 그대로)")
    ctl = at.copy(); ctl.set_constraint(fix); ctl.calc = calc
    ok_c = bool(FIRE(ctl, logfile=None).run(fmax=a.fmax, steps=a.steps))
    write(os.path.join(a.out, "relaxed_doped_extr.xyz"), ctl)
    dc, sc, dmc = li_state(ctl, ref, a.nslab, f"doped 이완 (수렴 {ok_c})")

    print("\n③ 이완 — ★ 시험군(같은 자리, neutral 분자)")
    tst = neu.copy(); tst.set_constraint(fix); tst.calc = calc
    ok_t = bool(FIRE(tst, logfile=None).run(fmax=a.fmax, steps=a.steps))
    write(os.path.join(a.out, "relaxed_neutral_from_doped_extr.xyz"), tst)
    dt, st, dmt = li_state(tst, ref, a.nslab, f"neutral 이완 (수렴 {ok_t})")

    print("\n" + "─" * 72)
    print("★ 판정")
    if not (ok_c and ok_t):
        print("  ⚠ 이완이 수렴하지 않았다 — --steps 를 늘려 다시 볼 것. 아래는 잠정.")
    print(f"  doped   추출 Li 변위 {dc:.2f} Å  (분자까지 {dmc:.2f} Å)")
    print(f"  neutral 추출 Li 변위 {dt:.2f} Å  (분자까지 {dmt:.2f} Å)")
    if dt < 0.5:
        print("\n  ✅ **neutral 에서는 Li 가 격자로 되돌아갔다.**")
        print("     → 추출 상태를 유지조차 못 한다. '중성 종은 Li 를 뽑지 않는다' 가")
        print("        탐색 실패가 아니라 **상태 부재**로 강해진다.")
    elif dt > 1.5:
        print("\n  ⛔ **neutral 도 추출 상태를 유지한다.**")
        print("     → 그 상태는 neutral 에도 **존재**하고 UMA 가 108 출발점에서 못 갔을 뿐이다.")
        print("        주장을 'UMA 는 neutral 의 추출 경로를 찾지 못했다' 로 **약하게** 다시 쓸 것.")
        print("        (열역학적 부재가 아니라 **경로/장벽** 문제라는 뜻이므로 NEB 이 필요해진다.)")
    else:
        print("\n  ⚠ 중간값이다 — 완전히 되돌아가지도, 유지하지도 않았다.")
        print("     이 한 번으로 결론 내지 말 것. 다른 추출 자세로도 반복해 볼 것.")
    print("\n  ⚠ 이 시험은 **doped 추출 기하에 양성자를 되돌려 만든 구조**다. 진짜 neutral")
    print("     최소가 아니므로, 논문에 쓸 때 구성 방법을 그대로 밝힐 것.")
    print(f"  ⚠ UMA 는 전하분리를 판정할 수 없다 — 최종 결론은 DFT 로만 낸다.")
    print(f"\n  산출물 → {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
