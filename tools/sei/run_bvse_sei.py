#!/usr/bin/env python3
"""run_bvse_sei.py — SEI 분해상들의 Li BVSE 지도·침투장벽을 한 번에 돌린다.

⚠⚠ 이 값은 **"Li migration barrier (eV)" 로 인용하면 안 된다.** BVSE 는 결합가 합이
  이상값(Li⁺ = 1.0)에서 벗어나는 정도를 에너지처럼 그린 **정적 기하 프록시**이지
  안장점 에너지가 아니다. 쓰임은 **상 사이의 상대 순위**와 **채널이 뚫려 있나** 뿐이다.
  절대 barrier 는 DFT NEB 으로만 낸다 (Li₂S · Li₃P · Li₃PO₄).

⚠ Li–P 결합가 파라미터가 없다 — `bvse_standalone.py` 의 표는 S·Cl·O 뿐이다.
  **Li₃P 는 BVSE 를 건너뛴다.** softBV 의 Li–P R₀ 를 출처와 함께 확보하기 전에는
  기억으로 채워 넣지 않는다. (Li₃P 는 어차피 NEB 3종에 들어 있다.)

  python3 tools/sei/run_bvse_sei.py
  python3 tools/sei/run_bvse_sei.py --grid 40      # 더 촘촘히 (기본 32)
"""
import argparse
import glob
import json
import os
import subprocess
import sys

SUPPORTED_ANIONS = {"S", "Cl", "O"}   # bvse_standalone.py 의 BV 표와 일치해야 한다
# ⚠ "Li 가 아닌 원소 = 음이온" 은 틀렸다 (2026-08-06). Li3PO4 의 P 는 PO4 중심의 **양이온**,
#   LiNdO2 의 Nd 도 양이온이다. 실제 규칙: S/Cl/O 가 있으면 그것이 음이온이고 나머지는
#   골격 양이온이다(우리 단순 BVSE 는 Li-음이온 항만 쓴다). S/Cl/O 가 하나도 없으면
#   그때는 다른 원소(P 등)가 음이온이고, 파라미터가 없으므로 건너뛴다.
# ⚠⚠ 그리고 **작은 셀은 주기 이미지 합산이 모자란다.** 실측(2026-08-06): Li2O 3.29 Å 셀에서
#   Li-site BVS 가 0.227 로 나왔는데 손계산 기대값은 ~0.95 다(이웃을 1/4 만 셌다).
#   → 셀을 MIN_L 이상으로 확장한 뒤 돌리고, BVS(Li) 가 1.0 에서 크게 벗어나면 경고한다.
MIN_L = 12.0                          # Å — 이보다 짧은 축은 슈퍼셀로 늘린다
BVS_LO, BVS_HI = 0.7, 1.4             # Li-site BVS 정상 범위 (이상값 1.0)
OUT = "db/properties/sei_bvse.json"


def to_p1_cif(vasp, cif, min_l=MIN_L):
    """ASE 로 P1 CIF 를 쓴다. 짧은 축은 **슈퍼셀로 늘린다**.

    ⚠ bvse_standalone 은 대칭연산을 안 펼치는 자체 파서이고, 주기 이미지 합산 범위가
      아지로다이트(~10 Å)에 맞춰져 있다. 3~5 Å 셀을 그대로 넣으면 이웃을 덜 세서
      BVS 가 통째로 작아지고 장벽이 엉뚱해진다(실측: LiCl 17.3).
    """
    import numpy as np
    from ase.io import read, write
    at = read(vasp)
    L = at.cell.lengths()
    rep = tuple(max(1, int(np.ceil(min_l / x))) for x in L)
    if rep != (1, 1, 1):
        at = at.repeat(rep)
    write(cif, at, format="cif")
    return at, rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="db/structures/sei_*.vasp")
    ap.add_argument("--grid", type=int, default=32)
    ap.add_argument("--work", default="/data/work/runs/sei_bvse")
    ap.add_argument("--min_l", type=float, default=MIN_L,
                    help="이보다 짧은 셀 축은 슈퍼셀로 늘린다 [Å]")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)

    files = sorted(glob.glob(a.pattern))
    if not files:
        sys.exit(f"⛔ {a.pattern} 에 구조가 없다 — fetch_sei_structures.py --get 먼저")

    res = {}
    for f in files:
        tag = os.path.basename(f)[len("sei_"):-len(".vasp")]
        cif = os.path.join(a.work, tag + ".cif")
        at, rep = to_p1_cif(f, cif, a.min_l)
        els = set(at.get_chemical_symbols())
        anions = els & SUPPORTED_ANIONS
        cations = sorted(els - anions - {"Li"})
        print(f"\n═══ {tag}  ({len(at)}원자, 슈퍼셀 {rep[0]}×{rep[1]}×{rep[2]} · "
              f"음이온 {'+'.join(sorted(anions)) or '없음'}"
              + (f" · 골격 양이온 {'+'.join(cations)}" if cations else "") + ") ═══")
        if "Li" not in els:
            print("  ⏭  건너뜀 — **Li 가 없다.** Li 이동 BVSE 자체가 정의되지 않는다.")
            res[tag] = {"status": "skipped", "reason": "no Li in compound",
                        "nsites": len(at)}
            continue
        missing = els - anions - {"Li"} - set(cations) if False else (
            set() if anions else (els - {"Li"}))
        if missing:
            # ⚠ 결합가 파라미터가 없는 원소가 섞이면 BVS 합이 그 원소를 통째로 무시한다.
            #   조용히 틀린 지도를 그리느니 건너뛴다.
            print(f"  ⏭  건너뜀 — 음이온이 S/Cl/O 가 아니다: {'+'.join(sorted(missing))} "
                  f"(Li-{'/'.join(sorted(missing))} 결합가 파라미터 미확보)")
            print(f"     (bvse_standalone.py 의 BV 표는 S·Cl·O 뿐. 출처 있는 R0 를 확보하기 전엔")
            print(f"      기억으로 채우지 않는다. 이 상은 DFT NEB 으로만 판정한다.)")
            res[tag] = {"status": "skipped", "reason": f"no BV params for {sorted(missing)}",
                        "nsites": len(at), "anions": sorted(anions)}
            continue

        pre = os.path.join(a.work, tag)
        cmd = [sys.executable, "tools/comp1_v3/bvse_standalone.py", cif,
               "--grid", str(a.grid), "--prefix", pre]
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout.strip()[-800:] or r.stderr.strip()[-600:])
        js = pre + "_bvse_summary.json"
        if r.returncode or not os.path.isfile(js):
            res[tag] = {"status": "failed", "stderr": r.stderr.strip()[-400:]}
            continue
        d = json.load(open(js))
        bvs = d.get("Li_site_BVS_mean")
        ok_bvs = bvs is not None and BVS_LO <= bvs <= BVS_HI
        if not ok_bvs:
            print(f"  ⚠⚠ Li-site BVS = {bvs} — 정상 범위({BVS_LO}–{BVS_HI})를 벗어났다.")
            print(f"     Li⁺ 의 결합가 합은 1.0 근처여야 한다. 이웃 합산이 모자라거나")
            print(f"     R0 가 이 화학에 안 맞는다는 뜻이므로 **이 값은 쓰면 안 된다.**")
        d.update({"status": "ok" if ok_bvs else "suspect", "nsites": len(at),
                  "anions": sorted(anions), "framework_cations": cations,
                  "supercell": list(rep), "grid": a.grid, "cif": cif,
                  "bvs_sanity": "ok" if ok_bvs else f"BVS {bvs} outside {BVS_LO}-{BVS_HI}"})
        res[tag] = d

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({
        "property": "sei_bvse",
        "warning": ("BVSE 는 정적 기하 프록시다. **eV 단위 migration barrier 로 인용 금지** — "
                    "상 사이 상대 순위와 채널 개통 판정에만 쓴다. 절대 barrier 는 DFT NEB."),
        "bv_params": "softBV Li-X R0: S 2.105 / Cl 2.249 / O 1.466, b=0.37 (Li-P 미확보)",
        "results": res,
    }, open(OUT, "w"), ensure_ascii=False, indent=2)

    print("\n" + "═" * 70)
    print(f"{'상':26s} {'상태':8s} {'프록시 장벽':>12s} {'BVS(Li)':>9s}  음이온")
    for k, v in res.items():
        b = v.get("Li_migration_barrier_BVSE")
        s_ = v.get("Li_site_BVS_mean")
        print(f"{k:26s} {v['status']:8s} "
              f"{(f'{b:.3f}' if isinstance(b, (int, float)) else '—'):>12s} "
              f"{(f'{s_:.3f}' if isinstance(s_, (int, float)) else '—'):>9s}  "
              f"{'+'.join(v.get('anions', []))}")
    print(f"\n→ {OUT}")
    print("⚠ 이 숫자는 **순위용**이다. 논문 본문의 barrier 는 NEB 값으로 쓴다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
