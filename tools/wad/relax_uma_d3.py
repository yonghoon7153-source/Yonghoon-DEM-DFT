#!/usr/bin/env python3
"""relax_uma_d3.py — A′ S2: 결합 기하를 UMA(omat · **default** 모드) + D3(BJ · 2체) 로 이완한다 (마스크·측방 제약 · 셀 고정).

    python3 tools/wad/relax_uma_d3.py --model_dir <S2/V3_s_outer/A> [--out <dir>] [--device cuda] [--d3 auto] [--fmax 0.02] [--steps 3000]
    python3 tools/wad/relax_uma_d3.py --model_dir <…> --preflight_only        # 마스크·sha·정책 검사만 (계산 0)
    python3 tools/wad/relax_uma_d3.py --selftest                                # EMT 로 제약 역학·기록·음성 경로

입력 = 빌더(`build_aprime_interfaces.py`)가 만든 폴더: bound.extxyz + meta.json (fixed_idx · lateral_fixed_idx · registry · sha256).
  ① 파일 sha 가 meta 와 같아야 한다 (손댄 좌표 거부) ② 시작 전 `se_sym_slab.interface_check(init, init, …)` 로 마스크가 정책 집합과 같은지 본다
  ③ FixAtoms(fixed) + FixedLine(lateral · z 방향) · 셀 고정 · FIRE (또는 BFGS) · fmax 0.02 eV/Å
  ④ 끝나면 `interface_check(init, relaxed)` → interface_check.json (깃발이 있으면 rc 2 · 파일은 남긴다)
  ⑤ relax_meta.json 에 결박값 기록: fairchem.core · torch · ase 버전 · 체크포인트 경로+sha256 · 추론 모드(default) · D3 구현·매개변수 · 스텝·벽시계 · 수렴.

⛔ 못 하는 것: W 를 내지 않는다 (에너지는 원출력 로그에만 — 결과표·W·후보 선택·게이트 조정에 쓰지 않는다 · 카드 v5 S3 전 예외 규칙) ·
  turbo 모드는 받지 않는다 (카드 결박 = default) · 3체 D3 를 켜지 않는다 · 셀을 풀지 않는다.
"""
import argparse
import glob
import hashlib
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S  # noqa: E402

SlabError = S.SlabError
D3_PARAMS = {"functional": "PBE", "damping": "BJ", "s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407, "three_body": False}
ROLES = {"V2": (("Ag",), ("C",)), "V3": (S.SE_ELEMENTS, ("Ag",)), "V4": (S.SE_ELEMENTS, ("C", "H")), "V5": (S.SE_ELEMENTS, ("Ag",))}


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load_model(model_dir):
    from ase.io import read
    meta = json.load(open(os.path.join(model_dir, "meta.json"), encoding="utf-8"))
    bp = os.path.join(model_dir, "bound.extxyz")
    got = _sha(bp)
    want = meta.get("sha256", {}).get("bound")
    if want and got != want:
        raise SlabError(f"bound.extxyz sha256 가 meta 와 다르다 (손댄 좌표?) — {got[:16]} ≠ {want[:16]}")
    init = read(bp)
    init.set_pbc((True, True, False))
    model = meta.get("model")
    if model not in ROLES:
        raise SlabError(f"meta.model = {model!r} — V2·V3·V4·V5 중 하나여야 한다")
    sub_el, ads_el = ROLES[model]
    fixed = meta.get("fixed_idx")
    lateral = meta.get("lateral_fixed_idx", [])
    if fixed is None:
        raise SlabError("meta 에 fixed_idx 가 없다 — 빌더 산출물이 아니다")
    return init, meta, sub_el, ads_el, fixed, lateral, got


def preflight(init, sub_el, ads_el, fixed, lateral):
    """마스크가 정책 집합과 같고 · 흡착면·유한성 등이 초기 구조에서 성립하는지 (init↔init 는 변위 0 이라 제약 검사는 통과해야 한다)."""
    r = S.interface_check(init, init.copy(), ads_elements=ads_el, substrate_elements=sub_el, fixed_idx=fixed, lateral_fixed_idx=lateral)
    if r["flags"]:
        raise SlabError("사전 점검 실패 — " + " | ".join(r["flags"]))
    return r


def make_calc(kind, device, d3_kind):
    info = {"calc": kind, "device": device}
    if kind == "emt":
        from ase.calculators.emt import EMT
        base = EMT(); info["emt"] = "ase EMT (시험용 · 물리 아님)"
    elif kind == "uma":
        import fairchem.core as fc
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        import torch
        pu = pretrained_mlip.get_predict_unit("uma-s-1p1", device=device, inference_settings="default")
        base = FAIRChemCalculator(pu, task_name="omat")
        info.update({"fairchem.core": getattr(fc, "__version__", "?"), "torch": torch.__version__, "cuda": torch.version.cuda,
                     "model": "uma-s-1p1", "task": "omat", "inference_settings": "default"})
        ck = sorted(glob.glob(os.path.expanduser("~/.cache/fairchem/models--facebook--UMA/**/uma-s-1p1.pt"), recursive=True)
                    + glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--facebook--UMA/**/uma-s-1p1.pt"), recursive=True))
        info["checkpoint"] = [{"path": os.path.realpath(c), "sha256": _sha(c), "MB": round(os.path.getsize(c) / 2 ** 20)} for c in ck] or "⚠ 체크포인트 파일을 못 찾았다 — 결박 불가"
    else:
        raise SlabError(f"모르는 계산기 {kind}")
    if d3_kind == "none":
        info["d3"] = "없음 (시험용) — UMA 본 실행에서는 허용되지 않는다"
        return base, info
    d3 = None
    tried = []
    for k in ((["dftd3", "torch_dftd", "dftd3_cli"]) if d3_kind == "auto" else [d3_kind]):
        try:
            if k == "dftd3":
                import dftd3
                from dftd3.ase import DFTD3
                d3 = DFTD3(method="PBE", damping="d3bj"); info["d3"] = {"impl": "simple-dftd3 (python)", "version": getattr(dftd3, "__version__", "?"), "method": "PBE", "damping": "d3bj (2체)"}
            elif k == "torch_dftd":
                import torch, torch_dftd
                from torch_dftd.torch_dftd3_calc import TorchDFTD3Calculator
                d3 = TorchDFTD3Calculator(xc="pbe", damping="bj", abc=False, device=device if torch.cuda.is_available() and device == "cuda" else "cpu", dtype=torch.float64)
                info["d3"] = {"impl": "torch-dftd", "version": getattr(torch_dftd, "__version__", "?"), "xc": "pbe", "damping": "bj", "abc": False}
            elif k == "dftd3_cli":
                from ase.calculators.dftd3 import DFTD3 as DFTD3CLI
                d3 = DFTD3CLI(xc="pbe", damping="bj", abc=False); info["d3"] = {"impl": "dftd3 CLI (ase.calculators.dftd3)", "xc": "pbe", "damping": "bj", "abc": False}
            break
        except Exception as e:  # noqa: BLE001
            tried.append(f"{k}: {type(e).__name__}: {e}")
            d3 = None
    if d3 is None:
        raise SlabError("D3 구현을 못 찾았다 — " + " / ".join(tried) + " — UMA 본 실행에는 D3(BJ 2체)가 필수다 (카드 결박)")
    info["d3"]["params_expected"] = D3_PARAMS
    from ase.calculators.mixing import SumCalculator
    return SumCalculator([base, d3]), info


def relax(model_dir, out, calc_kind="uma", device="cuda", d3_kind="auto", fmax=0.02, steps=3000, optimizer="fire", preflight_only=False):
    from ase.constraints import FixAtoms, FixedLine
    from ase.io import write
    import ase
    init, meta, sub_el, ads_el, fixed, lateral, init_sha = load_model(model_dir)
    pre = preflight(init, sub_el, ads_el, fixed, lateral)
    os.makedirs(out, exist_ok=True)
    rec = {"model_dir": os.path.abspath(model_dir), "model": meta.get("model"), "registry": meta.get("registry"), "term": meta.get("term"),
           "init_sha256": init_sha, "n_atoms": len(init), "fixed_n": len(fixed), "lateral_n": len(lateral), "preflight": {"flags": pre["flags"], "mask_matches_policy": pre["mask_matches_policy"]},
           "ase": ase.__version__, "fmax_target_eV_A": fmax, "max_steps": steps, "optimizer": optimizer, "cell_fixed": True}
    if preflight_only:
        rec["preflight_only"] = True
        json.dump(rec, open(os.path.join(out, "preflight.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        return rec, 0
    if calc_kind == "uma" and d3_kind == "none":
        raise SlabError("UMA 본 실행에서 --d3 none 은 허용되지 않는다 (카드 결박: PBE+D3 대조는 UMA+D3)")
    atoms = init.copy()
    # ⛔ 2026-09-25 gabia 실측: fairchem UMA 계산기는 축마다 다른 pbc(T,T,F) 를 거부한다 (MixedPBCError).
    #   계산기에 넘기는 동안만 **3축 주기**로 둔다 — 끝점 규칙으로 z 영상 간격이 ≥ 8 Å(빌더 기본 9 Å) 라 UMA 컷오프(6 Å)를 넘고,
    #   QE 참조도 3축 주기라 D3 의 z-영상 합도 그쪽과 같은 관례다. 저장·구조 검사는 슬랩 관례(T,T,F) 그대로.
    atoms.set_pbc((True, True, True))
    cons = [FixAtoms(indices=list(fixed))]
    if lateral:
        cons.append(FixedLine(indices=list(lateral), direction=[0, 0, 1]))
    atoms.set_constraint(cons)
    calc, cinfo = make_calc(calc_kind, device, d3_kind)
    atoms.calc = calc
    rec["calculator"] = cinfo
    t0 = time.time()
    e0 = float(atoms.get_potential_energy())
    Opt = {"fire": __import__("ase.optimize", fromlist=["FIRE"]).FIRE, "bfgs": __import__("ase.optimize", fromlist=["BFGS"]).BFGS}[optimizer]
    opt = Opt(atoms, logfile=os.path.join(out, "opt.log"), trajectory=os.path.join(out, "opt.traj"))
    converged = bool(opt.run(fmax=fmax, steps=steps))
    f = atoms.get_forces()
    free = np.ones(len(atoms), bool); free[list(fixed)] = False
    fz = f.copy()
    if lateral:
        fz[list(lateral), :2] = 0.0                      # 측방 제약 원자는 z 성분만 자유
    fmax_free = float(np.linalg.norm(fz[free], axis=1).max()) if free.any() else 0.0
    e1 = float(atoms.get_potential_energy())
    wall = time.time() - t0
    atoms.set_constraint()                               # 저장은 제약 없이 (좌표만)
    atoms.calc = None
    atoms.set_pbc((True, True, False))                   # 저장은 슬랩 관례로
    rp = os.path.join(out, "relaxed.extxyz")
    write(rp, atoms)
    chk = S.interface_check(init, atoms, ads_elements=ads_el, substrate_elements=sub_el, fixed_idx=fixed, lateral_fixed_idx=lateral)
    json.dump(chk, open(os.path.join(out, "interface_check.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    rec.update({"calculator_pbc": [True, True, True], "calculator_pbc_why": "UMA 는 균일 pbc 만 받는다 · z 영상 간격 ≥ 8 Å > UMA 컷오프 6 Å · QE 와 같은 3축 관례",
                "steps_taken": int(opt.get_number_of_steps()), "converged_fmax": converged, "fmax_free_final_eV_A": round(fmax_free, 5), "wall_s": round(wall, 1),
                "relaxed_sha256": _sha(rp), "disp_max_A": chk["disp_max_A"], "disp_rms_A": chk["disp_rms_A"], "interface_check_flags": chk["flags"],
                "energies_raw_log_only": {"E_init_eV": e0, "E_final_eV": e1, "⛔": "원출력 기록용 — 결과표·W·후보 선택·게이트 조정에 쓰지 않는다 (카드 v5 S3 전 예외 규칙)"}})
    json.dump(rec, open(os.path.join(out, "relax_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return rec, (0 if (converged and not chk["flags"]) else 2)


def _selftest():
    import tempfile, subprocess
    sys.path.insert(0, HERE)
    import build_aprime_interfaces as B
    n_ok = n_bad = 0

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")
    with tempfile.TemporaryDirectory() as T:
        # d0 를 2.0 Å 로 눌러 EMT 에서 C 층에 z 힘이 생기게 한다 (3.3 Å 에서는 EMT 힘이 0 에 가까워 스텝이 안 돈다)
        man = B.write_models(os.path.join(T, "V2"), {"top_fcc": B.build_v2(d0=2.0)["top_fcc"]})
        md = os.path.join(T, "V2", "top_fcc")
        rec, rc = relax(md, os.path.join(md, "relax"), calc_kind="emt", d3_kind="none", fmax=0.05, steps=25)
        from ase.io import read
        rel = read(os.path.join(md, "relax", "relaxed.extxyz"))
        x0, x1 = read(os.path.join(md, "bound.extxyz")).get_positions(), rel.get_positions()
        meta = json.load(open(os.path.join(md, "meta.json")))
        fx, lat = meta["fixed_idx"], meta["lateral_fixed_idx"]
        ck("selftest(EMT): 고정 원자 변위 0", np.abs(x1[fx] - x0[fx]).max() < 1e-9, np.abs(x1[fx] - x0[fx]).max())
        ck("selftest(EMT): 측방 제약 원자 면내 변위 0 · z 는 움직임", np.abs(x1[lat][:, :2] - x0[lat][:, :2]).max() < 1e-9 and np.abs(x1[lat][:, 2] - x0[lat][:, 2]).max() > 1e-6, (np.abs(x1[lat][:, :2] - x0[lat][:, :2]).max(), np.abs(x1[lat][:, 2] - x0[lat][:, 2]).max()))
        ck("selftest: 계산기 pbc 는 3축 주기로 기록 · 저장은 (T,T,F)", rec.get("calculator_pbc") == [True, True, True] and list(rel.get_pbc()) == [True, True, False], (rec.get("calculator_pbc"), list(rel.get_pbc())))
        ck("selftest(EMT): 산출 파일 셋 + interface_check 깃발 0 + 기록 필드", all(os.path.isfile(os.path.join(md, "relax", f)) for f in ("relaxed.extxyz", "relax_meta.json", "interface_check.json", "opt.log"))
           and not rec["interface_check_flags"] and rec["steps_taken"] >= 1 and "energies_raw_log_only" in rec and rec["preflight"]["mask_matches_policy"], rec.get("interface_check_flags"))
        # 사전 점검만
        rec2, rc2 = relax(md, os.path.join(md, "pre"), calc_kind="emt", d3_kind="none", preflight_only=True)
        ck("preflight_only: 계산 없이 preflight.json 만", rc2 == 0 and os.path.isfile(os.path.join(md, "pre", "preflight.json")) and not os.path.exists(os.path.join(md, "pre", "relaxed.extxyz")))
        # ⛔ 음성 ① 좌표 손댐 → sha 불일치 → 거부
        bp = os.path.join(md, "bound.extxyz"); s = open(bp).read(); open(bp, "w").write(s.replace("Ag", "Ag", 1) + "\n")
        try:
            relax(md, os.path.join(md, "x"), calc_kind="emt", d3_kind="none", preflight_only=True); bad = False
        except SlabError as e:
            bad = "sha256" in str(e)
        ck("⛔음성: bound.extxyz 를 손대면 sha 불일치로 거부", bad)
        open(bp, "w").write(s)
        # ⛔ 음성 ② meta 의 측방 마스크를 부분집합으로 → 사전 점검 실패
        m2 = json.load(open(os.path.join(md, "meta.json"))); m2["lateral_fixed_idx"] = m2["lateral_fixed_idx"][1:]
        json.dump(m2, open(os.path.join(md, "meta.json"), "w"), default=float)
        try:
            relax(md, os.path.join(md, "y"), calc_kind="emt", d3_kind="none", preflight_only=True); bad = False
        except SlabError as e:
            bad = "사전 점검" in str(e) and "흡착층 전체" in str(e)
        ck("⛔음성: meta 측방 마스크 부분집합 → 사전 점검에서 거부", bad)
        json.dump(meta, open(os.path.join(md, "meta.json"), "w"), default=float)
        # ⛔ 음성 ③ 고정 마스크 빠짐 (meta 에서 fixed_idx 제거)
        m3 = dict(meta); m3.pop("fixed_idx")
        json.dump(m3, open(os.path.join(md, "meta.json"), "w"), default=float)
        try:
            relax(md, os.path.join(md, "z"), calc_kind="emt", d3_kind="none", preflight_only=True); bad = False
        except SlabError as e:
            bad = "fixed_idx" in str(e)
        ck("⛔음성: meta 에 fixed_idx 없음 → 거부", bad)
        json.dump(meta, open(os.path.join(md, "meta.json"), "w"), default=float)
        # ⛔ 음성 ④ UMA 본 실행에 --d3 none 금지 (계산기 만들기 전에 막힌다)
        try:
            relax(md, os.path.join(md, "w"), calc_kind="uma", d3_kind="none"); bad = False
        except SlabError as e:
            bad = "D3" in str(e) or "d3" in str(e)
        ck("⛔음성: UMA + --d3 none → 거부 (카드 결박)", bad)
        # ⛔ 음성 ⑤ CLI 에 turbo 없음
        r = subprocess.run([sys.executable, __file__, "--model_dir", md, "--mode", "turbo"], capture_output=True, text=True)
        ck("⛔음성: CLI --mode turbo → 인자 오류 (default 만)", r.returncode != 0)
    print(f"{'✅' if n_bad == 0 else '⛔'} relax_uma_d3 selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--model_dir")
    ap.add_argument("--out")
    ap.add_argument("--calc", choices=["uma", "emt"], default="uma")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--mode", choices=["default"], default="default", help="UMA 추론 모드 — 카드 결박으로 default 만")
    ap.add_argument("--d3", choices=["auto", "dftd3", "torch_dftd", "dftd3_cli", "none"], default="auto")
    ap.add_argument("--fmax", type=float, default=0.02)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--optimizer", choices=["fire", "bfgs"], default="fire")
    ap.add_argument("--preflight_only", action="store_true")
    ap.add_argument("--d3_energy", metavar="STRUCT", help="S3 전 예외 ② D3 결박 검사용: 이 구조의 외부 D3 에너지만 찍는다 (eV · Ry · 구현·버전)")
    ap.add_argument("--energies", metavar="STRUCT", nargs="+", help="S4 집계용: 구조들의 **UMA 단일점 에너지(D3 없음 · default 모드 · 3축 pbc)** 를 JSON 으로 (개정 1: D3 항은 QE 출력에서). --out 에 쓴다")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.d3_energy:
        from ase.io import read
        at = read(a.d3_energy); at.set_pbc((True, True, True))   # QE 와 같은 3축 주기 (결박 검사는 같은 관례여야 한다)
        calc, info = make_calc("emt", a.device, a.d3)          # EMT 는 자리만 — D3 항만 따로 읽는다
        d3 = calc.mixer.calcs[1] if hasattr(calc, "mixer") else calc.calcs[1]
        at.calc = d3
        e = float(at.get_potential_energy())
        print(json.dumps({"struct": os.path.abspath(a.d3_energy), "sha256": _sha(a.d3_energy), "n_atoms": len(at), "pbc": [True, True, True], "E_D3_eV": e, "E_D3_Ry": e / 13.605693122994, "d3": info["d3"],
                          "⛔": "QE 의 'DFT-D3 Dispersion' 줄과 대조하는 용도 — 총 에너지·W 에 쓰지 않는다"}, ensure_ascii=False, indent=1, default=float))
        return 0
    if a.energies:
        from ase.io import read
        calc, info = make_calc(a.calc, a.device, "none")
        base = calc.mixer.calcs[0] if hasattr(calc, "mixer") else (calc.calcs[0] if hasattr(calc, "calcs") else calc)
        rows = {}
        for p in a.energies:
            at = read(p); at.set_pbc((True, True, True)); at.calc = base
            rows[os.path.splitext(os.path.basename(p))[0]] = {"struct": os.path.abspath(p), "sha256": _sha(p), "n_atoms": len(at), "formula": at.get_chemical_formula(),
                                                              "E_UMA_eV": float(at.get_potential_energy()), "pbc": [True, True, True]}
        rec = {"schema": "uma_energies/v1", "what": "UMA 단일점 에너지 (D3 없음) — W_UMA 용 · D3 항은 QE 출력에서 (개정 1)", "calculator": {k: v for k, v in info.items() if k != "d3"},
               "energies": rows}
        txt = json.dumps(rec, ensure_ascii=False, indent=1, default=float)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(txt + "\n"); print(f"-> {a.out}")
        print(txt if not a.out else json.dumps({k: v["E_UMA_eV"] for k, v in rows.items()}, ensure_ascii=False))
        return 0
    if not a.model_dir:
        ap.error("--model_dir 이 필요하다")
    out = a.out or os.path.join(a.model_dir, "relax")
    rec, rc = relax(a.model_dir, out, a.calc, a.device, a.d3, a.fmax, a.steps, a.optimizer, a.preflight_only)
    print(json.dumps({k: rec[k] for k in rec if k not in ("calculator",)}, ensure_ascii=False, indent=1, default=float))
    if "calculator" in rec:
        print("계산기:", json.dumps(rec["calculator"], ensure_ascii=False, default=float)[:600])
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
