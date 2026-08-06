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

SUPPORTED_ANIONS = {"S", "Cl", "O"}          # bvse_standalone.py 의 BV 표와 일치해야 한다
OUT = "db/properties/sei_bvse.json"


def to_p1_cif(vasp, cif):
    """ASE 로 P1 CIF 를 쓴다 — bvse_standalone 은 대칭연산을 안 펼친다."""
    from ase.io import read, write
    at = read(vasp)
    write(cif, at, format="cif")
    return at


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default="db/structures/sei_*.vasp")
    ap.add_argument("--grid", type=int, default=32)
    ap.add_argument("--work", default="/data/work/runs/sei_bvse")
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)

    files = sorted(glob.glob(a.pattern))
    if not files:
        sys.exit(f"⛔ {a.pattern} 에 구조가 없다 — fetch_sei_structures.py --get 먼저")

    res = {}
    for f in files:
        tag = os.path.basename(f)[len("sei_"):-len(".vasp")]
        cif = os.path.join(a.work, tag + ".cif")
        at = to_p1_cif(f, cif)
        anions = {s for s in at.get_chemical_symbols() if s != "Li"}
        missing = anions - SUPPORTED_ANIONS
        print(f"\n═══ {tag}  ({len(at)}원자 · 음이온 {'+'.join(sorted(anions))}) ═══")
        if missing:
            # ⚠ 결합가 파라미터가 없는 원소가 섞이면 BVS 합이 그 원소를 통째로 무시한다.
            #   조용히 틀린 지도를 그리느니 건너뛴다.
            print(f"  ⏭  건너뜀 — 결합가 파라미터 없음: {'+'.join(sorted(missing))}")
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
        d.update({"status": "ok", "nsites": len(at), "anions": sorted(anions),
                  "grid": a.grid, "cif": cif})
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
    print(f"{'상':26s} {'상태':8s} {'침투장벽(프록시)':>18s}  음이온")
    for k, v in res.items():
        b = v.get("percolation_barrier_eV", v.get("barrier_eV"))
        print(f"{k:26s} {v['status']:8s} "
              f"{(f'{b:.3f}' if isinstance(b, (int, float)) else '—'):>18s}  "
              f"{'+'.join(v.get('anions', []))}")
    print(f"\n→ {OUT}")
    print("⚠ 이 숫자는 **순위용**이다. 논문 본문의 barrier 는 NEB 값으로 쓴다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
