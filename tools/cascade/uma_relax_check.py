#!/usr/bin/env python3
"""uma_relax_check.py — **DFT 로 이완된 구조를 UMA 로 다시 이완**시켜 부피가 얼마나 움직이나.

왜 (2026-08-19, 1저자 질문 "우리 b2o3 dft 는 어떻게 살아남았나")
  cascade 부피 게이트가 plain B₂O₃ 를 30/30 탈락시켰는데, 우리 DFT 구조
  `b2o3_relaxV0.cif` 가 **같은 치환**(P 10→8, S 44→41, Li 54→58, +B₂O₃)인데
  부피가 원자당 −2.0 % 밖에 안 움직였다. cascade MLIP 은 |ΔV| 중앙 29.1 % 다.

  같은 치환, 15배 차이. 원인 후보 셋 중 둘을 이 시험이 가른다:
    · UMA 도 DFT 근처(≈0 %)에서 멈춘다  → **출발 셀**이 부풀려져 있었다 (게이트 재검토)
    · UMA 가 크게 무너뜨린다(−20 % 대) → **엔진** 문제 (UMA 가 이 조성에서 과붕괴)

  ⚠ 남는 후보 (a) 농도 는 이 시험으로 못 가른다 — 우리 DFT 는 cascade 의 절반 농도다.
    가르려면 같은 농도의 셀을 따로 만들어야 한다.

이 도구가 **못 하는 것**
  · DFT 를 돌리지 않는다. 입력 구조의 DFT 이완은 이미 끝난 것을 쓴다.
  · 대조군(host)을 자동으로 고르지 않는다 — `--structs` 로 같이 준다.
  · 에너지를 비교하지 않는다. UMA 와 DFT 는 기준계가 달라 절대에너지 비교 금지.

⚠ gabia 에서 **pw.x 와 동시 실행 금지** (VRAM 47/48 GB 사례). 스크립트가 먼저 막는다.

  python3 tools/cascade/uma_relax_check.py --selftest
  python3 tools/cascade/uma_relax_check.py \
      --structs db/structures/b2o3_relaxV0.cif db/structures/modelC_DFT_EOS_V0.cif
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "db" / "properties" / "uma_relax_check.json"
#: cascade 스크린과 같은 조건으로 맞춘다 (파이프라인 표 02: UMA relax 1500 steps)
FMAX = 0.05
STEPS = 1500


def guard_gpu():
    """pw.x 가 돌고 있으면 멈춘다 — 같이 띄우면 VRAM 이 터진다 (CLAUDE.md 규약)."""
    try:
        r = subprocess.run(["pgrep", "-f", "[p]w.x"], capture_output=True, text=True)
        if r.stdout.strip():
            raise SystemExit("⛔ pw.x 가 돌고 있다 — UMA 와 동시 실행 금지 (VRAM). 끝나고 실행할 것")
    except FileNotFoundError:
        pass


def relax(path, device="cuda"):
    from ase.io import read
    from ase.optimize import FIRE
    from ase.filters import FrechetCellFilter
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    a = read(path)
    v0, n = a.get_volume(), len(a)
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    a.calc = FAIRChemCalculator(pred, task_name="omat")
    t0 = time.time()
    opt = FIRE(FrechetCellFilter(a), logfile=None)
    opt.run(fmax=FMAX, steps=STEPS)
    v1 = a.get_volume()
    return {"file": str(path), "natoms": n,
            "V0_A3": round(v0, 2), "V1_A3": round(v1, 2),
            "dV_pct": round(100.0 * (v1 / v0 - 1.0), 2),
            "V_per_atom_before": round(v0 / n, 3), "V_per_atom_after": round(v1 / n, 3),
            "steps": int(opt.get_number_of_steps()), "converged": bool(opt.converged()),
            "seconds": round(time.time() - t0, 1)}


def selftest():
    ok = True

    def chk(c, m):
        nonlocal ok
        print(("  ✓ " if c else "  ✗ ") + m)
        ok &= bool(c)

    for f in ("db/structures/b2o3_relaxV0.cif", "db/structures/modelC_DFT_EOS_V0.cif"):
        chk((ROOT / f).exists(), f"[전제] {f} 가 있다")
    try:
        from ase.io import read
        a = read(ROOT / "db" / "structures" / "b2o3_relaxV0.cif")
        chk(len(a) == 128, f"[양성] b2o3 가 128원자 (얻은 것 {len(a)})")
        sym = a.get_chemical_symbols()
        chk(sym.count("P") == 8 and sym.count("B") == 2,
            f"[양성] P 8 · B 2 — cascade plain 과 같은 치환 (P{sym.count('P')} B{sym.count('B')})")
        m = read(ROOT / "db" / "structures" / "modelC_DFT_EOS_V0.cif")
        chk(m.get_chemical_symbols().count("P") == 5,
            "[양성] modelC host 는 P 5 — 2× 하면 10, b2o3 의 8 보다 둘 많다")
    except ImportError:
        print("  ⚠ ase 없음 — 구조 시험 건너뜀")
    # 음성 — pw.x 가 돌면 막아야 한다 (여기선 안 도니 통과해야 정상)
    try:
        guard_gpu(); chk(True, "[음성] pw.x 가 없으면 guard 가 통과시킨다")
    except SystemExit:
        chk(False, "[음성] pw.x 가 없는데 guard 가 막았다")
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structs", nargs="+", default=[
        "db/structures/b2o3_relaxV0.cif", "db/structures/modelC_DFT_EOS_V0.cif"])
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--out", default=str(OUT))
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()
    guard_gpu()
    rows = []
    for s in a.structs:
        p = s if os.path.isabs(s) else str(ROOT / s)
        print(f"── {s}")
        r = relax(p, a.device)
        rows.append(r)
        print(f"   V {r['V0_A3']} → {r['V1_A3']} Å³   **ΔV {r['dV_pct']:+.2f} %**   "
              f"({r['steps']} steps, {'수렴' if r['converged'] else '미수렴'}, {r['seconds']:.0f}s)")
    Path(a.out).write_text(json.dumps({
        "what": "UMA-s-1p1(omat) re-relaxation of DFT-relaxed structures. "
                "Question: does UMA collapse the cell that DFT kept?",
        "settings": {"fmax": FMAX, "max_steps": STEPS,
                     "filter": "FrechetCellFilter (cell + positions)"},
        "how_to_read": [
            "dV_pct ~ 0  -> UMA agrees with DFT; the cascade's 29 % came from the "
            "INFLATED STARTING CELL, not from the material. Volume gate needs review.",
            "dV_pct ~ -20 % -> UMA over-collapses this composition. Engine problem.",
            "NOT settled by this test: concentration (our DFT cell is half the "
            "cascade concentration).",
        ],
        "results": rows,
    }, ensure_ascii=False, indent=2))
    print(f"\n→ {a.out}")


if __name__ == "__main__":
    main()
