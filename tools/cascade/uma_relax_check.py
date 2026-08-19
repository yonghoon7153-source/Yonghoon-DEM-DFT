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


#: 같은 GPU 를 쓰는 QE 바이너리. ⚠ `neb.x` 를 빠뜨리면 SEI NEB 와 부딪친다
#: (2026-08-19 — 앞 판이 pw.x 만 봐서 cc333 neb.x 를 못 봤다).
QE_BINS = ("pw.x", "neb.x", "cp.x", "ph.x")


def running_qe():
    """지금 도는 QE 프로세스 이름 목록. 없으면 빈 리스트."""
    out = []
    for b in QE_BINS:
        try:
            # ⛔ `pgrep -f` 는 **명령줄 전체**를 본다 — 커밋 메시지에 "pw.x" 라고 적기만 해도
            #   자기 셸이 걸린다 (2026-08-19 실측, selftest 가 잡았다). 프로세스 **이름**으로 본다.
            r = subprocess.run(["pgrep", "-x", b], capture_output=True, text=True)
            if r.stdout.strip():
                out.append(b)
        except FileNotFoundError:
            return []
    return out


def guard_gpu(allow_share=False):
    """QE 가 돌고 있으면 멈춘다 — 같이 띄우면 VRAM 이 터진다 (CLAUDE.md 규약).

    `allow_share=True` 는 **사용자가 명시로 허용했을 때만** 쓴다. 조용히 넘어가지 않고
    무엇과 같이 도는지 찍는다 (2026-08-19 1저자 승인: "같이 돌려도 될거야, oom 나면 stop").
    """
    busy = running_qe()
    if not busy:
        return
    if allow_share:
        print(f"⚠ QE 가 돌고 있다: {', '.join(busy)} — 사용자 허용으로 **같이** 실행한다. "
              f"OOM 나면 이쪽을 죽일 것 (nvidia-smi 로 여유 확인 권장)")
        return
    raise SystemExit(f"⛔ {', '.join(busy)} 가 돌고 있다 — UMA 와 동시 실행 금지 (VRAM). "
                     f"끝나고 실행하거나 --allow_gpu_share 를 줄 것")


def drop_li(atoms, n_drop, seed=0):
    """Li 를 n_drop 개 뺀다 (결정론적: 인덱스 순 균등 간격).

    왜 (2026-08-19): gabia 실측에서 UMA 가 **만석 Li₆** canonical 셀만 +32.7 % 부풀리고
    Li 결손계(modelC Li₅.₄, b2o3)는 안 부푼다. "만석 Li 부격자가 원인" 가설을 가르려면
    같은 셀에서 Li 만 빼 보면 된다. 전하 보상은 **안 한다** — UMA 는 전하를 모른다.
    """
    import numpy as np
    li = [i for i, s in enumerate(atoms.get_chemical_symbols()) if s == "Li"]
    if n_drop <= 0 or n_drop >= len(li):
        raise ValueError(f"Li {len(li)}개에서 {n_drop}개는 못 뺀다")
    step = len(li) / float(n_drop)
    take = {li[int(round(k * step)) % len(li)] for k in range(n_drop)}
    return atoms[[i for i in range(len(atoms)) if i not in take]]


def relax(path, device="cuda", n_drop_li=0):
    from ase.io import read
    from ase.optimize import FIRE
    from ase.filters import FrechetCellFilter
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    a = read(path)
    if n_drop_li:
        a = drop_li(a, n_drop_li)
    v0, n = a.get_volume(), len(a)
    pred = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device)
    a.calc = FAIRChemCalculator(pred, task_name="omat")
    t0 = time.time()
    opt = FIRE(FrechetCellFilter(a), logfile=None)
    opt.run(fmax=FMAX, steps=STEPS)
    v1 = a.get_volume()
    return {"file": str(path), "natoms": n, "n_drop_li": int(n_drop_li),
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
    # drop_li — 양성 + 음성
    try:
        from ase.io import read as _rd
        c = _rd(ROOT / "db" / "structures" / "comp1_V0_k444.cif")
        nli = c.get_chemical_symbols().count("Li")
        d = drop_li(c, 1)
        chk(len(d) == len(c) - 1 and d.get_chemical_symbols().count("Li") == nli - 1,
            f"[양성] drop_li(1) 이 Li 를 정확히 하나 뺀다 ({nli}→{d.get_chemical_symbols().count('Li')})")
        chk(drop_li(c, 3).get_chemical_symbols().count("P") == c.get_chemical_symbols().count("P"),
            "[양성] Li 만 빠지고 P 는 그대로다")
        a1 = drop_li(c, 2).get_positions(); a2 = drop_li(c, 2).get_positions()
        chk(a1.shape == a2.shape and (a1 == a2).all(), "[양성] 결정론적이다 (두 번 불러 같다)")
        for bad in (0, -1, nli, nli + 5):
            try:
                drop_li(c, bad); chk(False, f"[음성] drop_li({bad}) 를 막지 못했다")
            except ValueError:
                pass
        chk(True, "[음성] 0·음수·전체이상 Li 삭제는 ValueError 로 막는다")
    except ImportError:
        print("  ⚠ ase 없음 — drop_li 시험 건너뜀")
    # guard — 양성 + 음성
    chk("neb.x" in QE_BINS and "pw.x" in QE_BINS,
        "[양성] guard 가 neb.x 도 본다 (pw.x 만 보면 SEI NEB 를 놓친다)")
    try:
        guard_gpu(); chk(True, "[음성] QE 가 없으면 guard 가 통과시킨다")
    except SystemExit:
        chk(False, "[음성] QE 가 없는데 guard 가 막았다")
    # ★ 음성 — QE 가 돌면 **막아야** 한다. running_qe 를 가짜로 채워 확인한다.
    _real = globals()["running_qe"]
    try:
        globals()["running_qe"] = lambda: ["neb.x"]
        try:
            guard_gpu(); chk(False, "[음성] QE 가 도는데 guard 가 통과시켰다")
        except SystemExit:
            chk(True, "[음성] QE 가 돌면 guard 가 막는다")
        try:
            guard_gpu(allow_share=True); chk(True, "[양성] --allow_gpu_share 면 통과시킨다")
        except SystemExit:
            chk(False, "[양성] 허용했는데도 막았다")
    finally:
        globals()["running_qe"] = _real
    print("selftest PASS" if ok else "selftest FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structs", nargs="+", default=[
        "db/structures/b2o3_relaxV0.cif", "db/structures/modelC_DFT_EOS_V0.cif"])
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--drop_li", type=int, default=0,
                    help="이완 전에 Li 를 이만큼 뺀다 (만석-Li 가설 검증용)")
    ap.add_argument("--allow_gpu_share", action="store_true",
                    help="QE 가 돌아도 실행 (사용자 명시 허용 시에만)")
    ap.add_argument("--out", default=str(OUT))
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    a = ap.parse_args()
    guard_gpu(a.allow_gpu_share)
    rows = []
    for s in a.structs:
        p = s if os.path.isabs(s) else str(ROOT / s)
        print(f"── {s}")
        r = relax(p, a.device, a.drop_li)
        rows.append(r)
        print(f"   {('Li−%d  ' % a.drop_li) if a.drop_li else ''}"
              f"V {r['V0_A3']} → {r['V1_A3']} Å³   **ΔV {r['dV_pct']:+.2f} %**   "
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
