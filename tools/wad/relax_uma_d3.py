#!/usr/bin/env python3
"""relax_uma_d3.py — A′ S2: 결합 기하를 UMA(omat · **default** 모드) + D3(BJ · 2체) 로 이완한다 (마스크·측방 제약 · 셀 고정).

    python3 tools/wad/relax_uma_d3.py --model_dir <S2/V3_s_outer/A> [--out <dir>] [--device cuda] [--d3 auto] [--fmax 0.02] [--steps 3000]
    python3 tools/wad/relax_uma_d3.py --model_dir <…> --preflight_only        # 마스크·sha·정책 검사만 (계산 0)
    python3 tools/wad/relax_uma_d3.py --selftest                                # EMT 로 제약 역학·기록·음성 경로
    python3 tools/wad/relax_uma_d3.py --w_from <모델> --relax_dir <이완> --out <w.json>   # SE 쌍 카드 §2: 이완본 → 끝점 10·12 Å → W_UMA+D3 · ATM · G3
    python3 tools/wad/relax_uma_d3.py --collect <run_dir> --out <collect.json>            # SE 쌍 카드 §4·§5: sha 사슬 · G1 · G2 · G3 · registry 합쳐짐 · 헤드라인

입력 = 빌더(`build_aprime_interfaces.py`)가 만든 폴더: bound.extxyz + meta.json (fixed_idx · lateral_fixed_idx · registry · sha256).
  ① 파일 sha 가 meta 와 같아야 한다 (손댄 좌표 거부) ② 시작 전 `se_sym_slab.interface_check(init, init, …)` 로 마스크가 정책 집합과 같은지 본다
  ③ FixAtoms(fixed) + FixedLine(lateral · z 방향) · 셀 고정 · FIRE (또는 BFGS) · fmax 0.02 eV/Å
  ④ 끝나면 `interface_check(init, relaxed)` → interface_check.json (깃발이 있으면 rc 2 · 파일은 남긴다)
  ⑤ relax_meta.json 에 결박값 기록: fairchem.core · torch · ase 버전 · 체크포인트 경로+sha256 · 추론 모드(default) · D3 구현·매개변수 · 스텝·벽시계 · 수렴.

GPU 공유 안전장치 (2026-10-01 · SE 쌍 UMA 카드 · gabia 에서 li2s MD 옆):
  --gpu_start_max_mib M  : GPU 합계 ≤ M 이 될 때까지 기다렸다 시작 (못 읽으면 시작 안 함 · --gpu_wait_s 넘으면 종료 4)
  --gpu_kill_total_mib K : 감시 스레드 — 합계 > K 면 **이 프로세스만** 끝낸다 (종료 3 · gpu_guard.json · 세 번 연속 못 읽어도)
  --vram_cap_mib C       : torch.cuda.set_per_process_memory_fraction — 넘으면 이 프로세스가 OOM (CUDA 컨텍스트는 상한 밖)
  --mem_probe            : 힘 한 번만 계산하고 최대 메모리를 mem_probe.json 에 (이완·에너지 기록 없음)
  ⚠ 감시는 표본(기본 2 s)이다 — 표본 간격보다 빠른 급등은 못 막는다. 남의 잡(li2s·탄성)을 멈추거나 늦추지 않는다.

⛔ 못 하는 것: **이완 모드는** W 를 내지 않는다 (W 는 --w_from · 이완 에너지는 원출력 로그에만 — 결과표·W·후보 선택·게이트 조정에 쓰지 않는다 · 카드 v5 S3 전 예외 규칙) ·
  turbo 모드는 받지 않는다 (카드 결박 = default) · 3체 D3 를 켜지 않는다 · 셀을 풀지 않는다.
"""
import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys
import threading
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S  # noqa: E402

SlabError = S.SlabError
D3_PARAMS = {"functional": "PBE", "damping": "BJ", "s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407, "three_body": False}
ROLES = {"V2": (("Ag",), ("C",)), "V3": (S.SE_ELEMENTS, ("Ag",)), "V4": (S.SE_ELEMENTS, ("C", "H")), "V5": (S.SE_ELEMENTS, ("Ag",)),
         "P1": (S.SE_ELEMENTS, ("Ag",)), "P2": (S.SE_ELEMENTS, ("C",))}      # P1·P2 = SE 쌍 전체 계면 (build_full)


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _gpu_total_mib():
    """GPU 0 사용량 합계 (MiB) · 못 읽으면 None. 시험에서는 WAD_NVSMI 가 명령을 바꾼다."""
    cmd = os.environ.get("WAD_NVSMI", "nvidia-smi")
    try:
        r = subprocess.run([cmd, "--query-gpu=memory.used", "--format=csv,noheader,nounits", "-i", "0"],
                           capture_output=True, text=True, timeout=20)
        return int(r.stdout.strip().splitlines()[0].strip())
    except Exception:  # noqa: BLE001
        return None


def gpu_start_gate(start_max, wait_s, poll=None):
    """합계 ≤ start_max 가 될 때까지 기다린다 → {ok, last_MiB, waited_s, reason}. 못 읽으면 시작하지 않는다 (fail-closed)."""
    poll = float(os.environ.get("WAD_GUARD_POLL", "30")) if poll is None else poll
    t0 = time.time()
    while True:
        u = _gpu_total_mib()
        w = round(time.time() - t0, 1)
        if u is None:
            return {"ok": False, "last_MiB": None, "waited_s": w, "reason": "nvidia-smi 를 못 읽었다 — 시작하지 않는다 (fail-closed)"}
        if u <= start_max:
            return {"ok": True, "last_MiB": u, "waited_s": w, "reason": f"합계 {u} ≤ {start_max}"}
        if time.time() - t0 >= wait_s:
            return {"ok": False, "last_MiB": u, "waited_s": w, "reason": f"합계 {u} > {start_max} 가 {wait_s}s 계속 — 시작하지 않는다"}
        print(f"  대기 — GPU 합계 {u} > {start_max} MiB", flush=True)
        time.sleep(poll)


def start_gpu_watchdog(kill_total, out_dir, sample=None):
    """감시 스레드 — 합계 > kill_total 이면 **이 프로세스만** 끝낸다 (os._exit(3) · gpu_guard.json). 세 번 연속 못 읽어도 끝낸다."""
    sample = float(os.environ.get("WAD_GUARD_SAMPLE", "2")) if sample is None else sample

    def _abort(reason, u):
        try:
            os.makedirs(out_dir, exist_ok=True)
            json.dump({"killed_by": "gpu_watchdog", "reason": reason, "total_MiB": u, "kill_total_MiB": kill_total,
                       "at": time.strftime("%Y-%m-%d %H:%M:%S")}, open(os.path.join(out_dir, "gpu_guard.json"), "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
        finally:
            print(f"⛔ GPU 감시: {reason} — 이 프로세스만 멈춘다 (종료 3)", flush=True)
            os._exit(3)

    def loop():
        miss = 0
        while True:
            u = _gpu_total_mib()
            if u is None:
                miss += 1
                if miss >= 3:
                    _abort("nvidia-smi 를 세 번 연속 못 읽었다 (fail-closed)", None)
            else:
                miss = 0
                if u > kill_total:
                    _abort(f"GPU 합계 {u} > {kill_total} MiB", u)
            time.sleep(sample)

    th = threading.Thread(target=loop, daemon=True)
    th.start()
    return th


def _peak_mem():
    try:
        import torch
        if torch.cuda.is_available():
            return {"max_reserved_MiB": round(torch.cuda.max_memory_reserved() / 2 ** 20), "max_allocated_MiB": round(torch.cuda.max_memory_allocated() / 2 ** 20)}
    except Exception:  # noqa: BLE001
        pass
    return None


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
        raise SlabError(f"meta.model = {model!r} — {'·'.join(ROLES)} 중 하나여야 한다")
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


def make_calc(kind, device, d3_kind, vram_cap_mib=None):
    info = {"calc": kind, "device": device}
    if kind == "emt":
        from ase.calculators.emt import EMT
        base = EMT(); info["emt"] = "ase EMT (시험용 · 물리 아님)"
        if vram_cap_mib:
            info["vram_cap"] = "해당 없음 (EMT)"
    elif kind == "uma":
        import fairchem.core as fc
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        import torch
        if vram_cap_mib and str(device).startswith("cuda") and torch.cuda.is_available():
            tot = torch.cuda.get_device_properties(0).total_memory / 2 ** 20
            frac = min(1.0, float(vram_cap_mib) / tot)
            torch.cuda.set_per_process_memory_fraction(frac, 0)
            info["vram_cap"] = {"cap_MiB": vram_cap_mib, "device_total_MiB": round(tot), "fraction": round(frac, 4),
                                "⚠": "CUDA 컨텍스트(수백 MiB)는 이 상한 밖이다"}
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


def relax(model_dir, out, calc_kind="uma", device="cuda", d3_kind="auto", fmax=0.02, steps=3000, optimizer="fire", preflight_only=False,
          vram_cap_mib=None, gpu_kill_total_mib=None, gpu_start_max_mib=None, gpu_wait_s=3600, mem_probe=False):
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
    guard = {"vram_cap_MiB": vram_cap_mib, "gpu_kill_total_MiB": gpu_kill_total_mib, "gpu_start_max_MiB": gpu_start_max_mib}
    if gpu_start_max_mib is not None:
        g = gpu_start_gate(gpu_start_max_mib, gpu_wait_s)
        guard["start_gate"] = g
        if not g["ok"]:
            rec["gpu_guard"] = guard
            json.dump(rec, open(os.path.join(out, "gate_refused.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
            print(f"⛔ 시작 문턱: {g['reason']}", flush=True)
            return rec, 4
    if gpu_kill_total_mib is not None:
        start_gpu_watchdog(gpu_kill_total_mib, out)
        guard["watchdog"] = f"on (합계 > {gpu_kill_total_mib} MiB 면 이 프로세스만 종료 3)"
    rec["gpu_guard"] = guard
    calc, cinfo = make_calc(calc_kind, device, d3_kind, vram_cap_mib)
    atoms.calc = calc
    rec["calculator"] = cinfo
    t0 = time.time()
    if mem_probe:
        atoms.get_forces()
        rec["mem_probe"] = {"peak": _peak_mem(), "gpu_total_after_MiB": _gpu_total_mib(), "n_atoms": len(atoms), "wall_s": round(time.time() - t0, 1),
                            "⛔": "힘 한 번 — 이완·에너지 기록 없음 (메모리만 잰다)"}
        json.dump(rec, open(os.path.join(out, "mem_probe.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        return rec, 0
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
    rec["peak_mem"] = _peak_mem()
    rec.update({"calculator_pbc": [True, True, True], "calculator_pbc_why": "UMA 는 균일 pbc 만 받는다 · z 영상 간격 ≥ 8 Å > UMA 컷오프 6 Å · QE 와 같은 3축 관례",
                "steps_taken": int(opt.get_number_of_steps()), "converged_fmax": converged, "fmax_free_final_eV_A": round(fmax_free, 5), "wall_s": round(wall, 1),
                "relaxed_sha256": _sha(rp), "disp_max_A": chk["disp_max_A"], "disp_rms_A": chk["disp_rms_A"], "interface_check_flags": chk["flags"],
                "energies_raw_log_only": {"E_init_eV": e0, "E_final_eV": e1, "⛔": "원출력 기록용 — 결과표·W·후보 선택·게이트 조정에 쓰지 않는다 (카드 v5 S3 전 예외 규칙)"}})
    json.dump(rec, open(os.path.join(out, "relax_meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return rec, (0 if (converged and not chk["flags"]) else 2)


EV_A2_TO_J_M2 = 16.02176634          # eV/Å² → J/m²
D3BJ_PBE_SDFTD3 = {"s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407, "alp": 14.0}   # cc_graphite.D3BJ_PBE 와 같다 (ATM 열)
HARTREE_EV, BOHR_A = 27.211386245988, 0.529177210903
G3_TOL_J_M2 = 0.01                   # SE 쌍 카드 4 G3 (10 → 12 Å)


def _atm_delta(b, f):
    """같은 기하에서 E_D3(s9=1) − E_D3(s9=0) 의 끝점 차 (eV) — WAD-CC atm_column 과 같은 방법 · 없으면 None."""
    try:
        from dftd3.interface import DispersionModel, RationalDampingParam
    except ImportError:
        return None

    def e_d3(at, s9):
        mdl = DispersionModel(at.get_atomic_numbers(), at.get_positions() / BOHR_A, at.cell.array / BOHR_A, periodic=np.array([True, True, True]))
        return mdl.get_dispersion(RationalDampingParam(s9=s9, **D3BJ_PBE_SDFTD3), grad=False)["energy"] * HARTREE_EV
    return (e_d3(f, 1.0) - e_d3(f, 0.0)) - (e_d3(b, 1.0) - e_d3(b, 0.0))


def w_endpoints(model_dir, relax_dir, gaps=(10.0, 12.0), calc_kind="uma", device="cuda", d3_kind="auto", vram_cap_mib=None,
                gpu_kill_total_mib=None, gpu_start_max_mib=None, gpu_wait_s=3600, out_dir=None):
    """SE 쌍 카드 §2: 이완된 결합 기하 → make_endpoints(gap) 로 bound′·far → E = E_UMA + E_D3(2체) → W = ΔE/A (J/m²) · ATM 열 · G3.

    ① 모델 폴더의 meta·bound sha (load_model) ② relax_meta 의 init_sha256 = 이 모델 · relaxed_sha256 = 파일 (다른 모델의 이완본·손댄 좌표 거부)
    ③ 끝점은 **이완본에서** 새로 만든다 (빌더의 초기 far 를 쓰지 않는다) ④ 계산기 pbc 3축 (이완과 같은 관례).
    ⛔ 못 하는 것: DFT 가 아니다 · registry 평균·헤드라인은 --collect · 라벨 문장은 결과 기록 몫 · 이완이 미수렴이면 값을 내되 '미수렴' 을 같이 적는다 (G1 판정은 기록에서).
    """
    from ase.io import read
    init, meta, sub_el, ads_el, fixed, lateral, init_sha = load_model(model_dir)
    rp = os.path.join(relax_dir, "relaxed.extxyz"); mp = os.path.join(relax_dir, "relax_meta.json")
    if not (os.path.isfile(rp) and os.path.isfile(mp)):
        raise SlabError(f"이완 산출물이 없다 — {relax_dir} (relaxed.extxyz · relax_meta.json)")
    rm = json.load(open(mp, encoding="utf-8"))
    if rm.get("init_sha256") != init_sha:
        raise SlabError(f"relax_meta 의 init_sha256 가 이 모델과 다르다 — 다른 모델의 이완본? ({str(rm.get('init_sha256'))[:16]} ≠ {init_sha[:16]})")
    if rm.get("relaxed_sha256") != _sha(rp):
        raise SlabError("relaxed.extxyz sha256 가 relax_meta 와 다르다 (손댄 좌표?)")
    if calc_kind == "uma" and d3_kind == "none":
        raise SlabError("UMA 본 계산에서 --d3 none 은 허용되지 않는다 (카드: UMA+D3)")
    relaxed = read(rp); relaxed.set_pbc((True, True, False))
    is_ads = np.array([s in ads_el for s in relaxed.get_chemical_symbols()])
    out_dir = out_dir or relax_dir
    guard = {"vram_cap_MiB": vram_cap_mib, "gpu_kill_total_MiB": gpu_kill_total_mib, "gpu_start_max_MiB": gpu_start_max_mib}
    if gpu_start_max_mib is not None:
        g = gpu_start_gate(gpu_start_max_mib, gpu_wait_s); guard["start_gate"] = g
        if not g["ok"]:
            raise SlabError(f"시작 문턱: {g['reason']}")
    if gpu_kill_total_mib is not None:
        start_gpu_watchdog(gpu_kill_total_mib, out_dir); guard["watchdog"] = "on"
    calc, cinfo = make_calc(calc_kind, device, d3_kind, vram_cap_mib)
    A = float(np.linalg.norm(np.cross(relaxed.cell.array[0], relaxed.cell.array[1])))
    rows = {}
    for gap in gaps:
        b, f, em = __import__("build_aprime_interfaces").make_endpoints(relaxed, is_ads, float(gap))
        e = {}
        for k, at in (("bound", b), ("far", f)):
            x = at.copy(); x.set_pbc((True, True, True)); x.calc = calc
            e[k] = float(x.get_potential_energy())
        datm = _atm_delta(b.copy(), f.copy())
        rows[f"{float(gap):g}"] = {"E_bound_eV": e["bound"], "E_far_eV": e["far"], "W_2body_J_m2": (e["far"] - e["bound"]) / A * EV_A2_TO_J_M2,
                                  "dW_ATM_J_m2": None if datm is None else datm / A * EV_A2_TO_J_M2,
                                  "ATM_status": "simple-dftd3 · E(s9=1) − E(s9=0) · 3D 주기" if datm is not None else "simple-dftd3 python 없음 — ATM 미계산 (0 아님)",
                                  "endpoint": em}
    keys = list(rows)
    g3 = None
    if len(keys) >= 2:
        dW = abs(rows[keys[-1]]["W_2body_J_m2"] - rows[keys[0]]["W_2body_J_m2"])
        g3 = {"from_to_A": [keys[0], keys[-1]], "abs_dW_J_m2": dW, "tol_J_m2": G3_TOL_J_M2, "status": "PASS" if dW <= G3_TOL_J_M2 else "FAIL",
              "⚠": "카드 G3 판정 대상 = P1·P2 의 S 바깥 A — 나머지는 정보"}
    rec = {"schema": "wad_uma_w/v1", "model": meta.get("model"), "term": meta.get("term"), "registry": meta.get("registry"), "model_dir": os.path.abspath(model_dir),
           "relax_dir": os.path.abspath(relax_dir), "init_sha256": init_sha, "relaxed_sha256": rm.get("relaxed_sha256"), "n_atoms": len(relaxed),
           "n_ads": int(is_ads.sum()), "area_A2": A, "relax": {k: rm.get(k) for k in ("converged_fmax", "steps_taken", "fmax_free_final_eV_A", "interface_check_flags", "disp_max_A")},
           "gaps": rows, "G3": g3, "gpu_guard": guard, "calculator": cinfo,
           "definition": "W_sep = [E(far) − E(bound′)]/A · E = E_UMA(default · omat) + E_D3(BJ 2체) · 끝점 = 이완 결합 기하에서 make_endpoints(gap) · 계면 1 개"}
    return rec


G3_REPS = {"P1": ("s_outer", "A"), "P2": ("s_outer", "A")}      # SE 쌍 카드 §4 G3 판정 대상 (나머지는 정보)


def collect(run_dir, fmax_target=0.02, max_steps=3000):
    """SE 쌍 카드 §4·§5 집계 — run_dir/models/<계_종결>/<A|B>/ · relax/<계_종결>/<A|B>/ · w/<계_종결>_<A|B>.json 에서
    무결성 (sha 사슬: bound · meta · relax_meta · W / relaxed · relax_meta · W) · G1 (fmax ≤ 0.02 · 스텝 ≤ 3000) · G2 (깃발 0) ·
    G3 (대표 = P1·P2 S 바깥 A · 10 → 12 Å |ΔW| ≤ 0.01) · registry 합쳐짐 (이완 뒤 접촉층 거리 < 0.2 Å · build_aprime_interfaces.registry_distance) ·
    종결별 헤드라인 (유효 registry 의 평균 · [min, max] · 2체 · ATM 열 따로 · 12 Å 는 정보).
    ⛔ 못 하는 것: 라벨 문장·DEM 문구를 만들지 않는다 (결과 기록 몫) · G5 (V5 VASP 비교) 는 외주가 와야 한다 ·
      INCOMPLETE 를 다른 표본으로 바꾸지 않는다 (세고 뺀다) · 빠진 파일·끊긴 sha 는 건너뛰지 않고 거부한다.
    """
    import build_aprime_interfaces as B
    from ase.io import read
    samples = {}
    for mp in sorted(glob.glob(os.path.join(run_dir, "models", "*", "*", "meta.json"))):
        mdir = os.path.dirname(mp)
        key, reg = os.path.basename(os.path.dirname(mdir)), os.path.basename(mdir)
        meta = json.load(open(mp, encoding="utf-8"))
        kind, term = meta.get("model"), meta.get("term")
        if kind not in G3_REPS or key != f"{kind}_{term}" or reg != meta.get("registry"):
            raise SlabError(f"collect: 폴더 이름과 meta 가 다르다 — {mdir} (model {kind} · term {term} · registry {meta.get('registry')})")
        rdir = os.path.join(run_dir, "relax", key, reg)
        wp = os.path.join(run_dir, "w", f"{key}_{reg}.json")
        paths = {"bound": os.path.join(mdir, "bound.extxyz"), "relaxed": os.path.join(rdir, "relaxed.extxyz"), "relax_meta": os.path.join(rdir, "relax_meta.json"), "w": wp}
        for p in paths.values():
            if not os.path.isfile(p):
                raise SlabError(f"collect: 없다 — {p} (빠진 표본을 조용히 건너뛰지 않는다)")
        rm = json.load(open(paths["relax_meta"], encoding="utf-8"))
        w = json.load(open(wp, encoding="utf-8"))
        s_init, s_rel = _sha(paths["bound"]), _sha(paths["relaxed"])
        if not (s_init == meta["sha256"]["bound"] == rm.get("init_sha256") == w.get("init_sha256")):
            raise SlabError(f"collect: {key}/{reg} 초기 sha 사슬이 끊겼다 (bound · meta · relax_meta · W)")
        if not (s_rel == rm.get("relaxed_sha256") == w.get("relaxed_sha256")):
            raise SlabError(f"collect: {key}/{reg} 이완본 sha 사슬이 끊겼다 (relaxed · relax_meta · W)")
        f = rm.get("fmax_free_final_eV_A")               # 0.0 도 유효하다 — `or` 로 채우지 않는다
        n = rm.get("steps_taken")
        g1 = bool(rm.get("converged_fmax")) and f is not None and f <= fmax_target and n is not None and n <= max_steps
        flags = rm.get("interface_check_flags")
        g2 = flags == []                                   # None (기록 없음) 은 통과가 아니다
        g = w.get("gaps", {})
        if "10" not in g:
            raise SlabError(f"collect: {key}/{reg} W 에 10 Å 끝점이 없다 (헤드라인 간격)")
        g12 = g.get("12", {})
        samples[(kind, term, reg)] = {
            "model": kind, "term": term, "registry": reg, "G1": g1, "G2": g2, "valid": bool(g1 and g2),
            "steps": n, "fmax_final_eV_A": f, "interface_check_flags": flags,
            "W2_10_J_m2": g["10"]["W_2body_J_m2"], "dW_ATM_10_J_m2": g["10"].get("dW_ATM_J_m2"),
            "W2_12_J_m2": g12.get("W_2body_J_m2"), "dW_ATM_12_J_m2": g12.get("dW_ATM_J_m2"),
            "G3_abs_dW_J_m2": (w.get("G3") or {}).get("abs_dW_J_m2"),
            "E_bound_10_eV": g["10"].get("E_bound_eV"), "E_far_10_eV": g["10"].get("E_far_eV"), "area_A2": w.get("area_A2"),
            "n_atoms": w.get("n_atoms"), "n_ads": w.get("n_ads"), "wall_s": rm.get("wall_s"), "peak_mem": rm.get("peak_mem"),
            "sha256": {"bound": s_init, "relaxed": s_rel}, "_paths": paths, "_ads": meta.get("ads_element")}
    if not samples:
        raise SlabError(f"collect: {run_dir}/models 아래에 P1·P2 모델이 없다")
    g3 = {}
    for kind, (t, r) in G3_REPS.items():
        if not any(k[0] == kind for k in samples):
            continue
        s = samples.get((kind, t, r))
        if s is None or not s["valid"] or s["G3_abs_dW_J_m2"] is None:
            g3[kind] = {"sample": f"{kind}_{t}_{r}", "status": "INCOMPLETE", "why": "대표 표본이 없거나 G1·G2 미통과이거나 12 Å 끝점이 없다"}
        else:
            ok = s["G3_abs_dW_J_m2"] <= G3_TOL_J_M2
            g3[kind] = {"sample": f"{kind}_{t}_{r}", "abs_dW_J_m2": s["G3_abs_dW_J_m2"], "tol_J_m2": G3_TOL_J_M2, "status": "PASS" if ok else "FAIL",
                        "label": None if ok else f"끝점 미수렴 (+{s['G3_abs_dW_J_m2']:.3f} J/m² · 10 → 12 Å) — 헤드라인은 10 Å 그대로"}
    reg_out, head = {}, {}
    for kind, term in sorted({(k[0], k[1]) for k in samples}):
        a, b = samples.get((kind, term, "A")), samples.get((kind, term, "B"))
        rd = None
        if a and b:
            rd = B.registry_distance(kind, read(a["_paths"]["bound"]), read(b["_paths"]["bound"]), read(a["_paths"]["relaxed"]), read(b["_paths"]["relaxed"]), a["_ads"])
            reg_out[f"{kind}_{term}"] = rd
        val = [s for s in (a, b) if s and s["valid"]]
        inc = [s["registry"] for s in (a, b) if s and not s["valid"]]
        h = {"n_registry_valid": len(val), "INCOMPLETE": inc, "G3_label": (g3.get(kind) or {}).get("label")}
        if val:
            w10 = [s["W2_10_J_m2"] for s in val]
            atm = [s["dW_ATM_10_J_m2"] for s in val]
            w12 = [s["W2_12_J_m2"] for s in val]
            h.update({"W2_10_mean_J_m2": float(np.mean(w10)), "W2_10_min_max_J_m2": [float(min(w10)), float(max(w10))],
                      "dW_ATM_10_mean_J_m2": None if any(x is None for x in atm) else float(np.mean(atm)),
                      "W2_12_mean_J_m2_info": None if any(x is None for x in w12) else float(np.mean(w12)),
                      "by_registry_W2_10_J_m2": {s["registry"]: s["W2_10_J_m2"] for s in val}})
        merged = bool(rd and rd["merged"] and len(val) == 2)
        h["registry_merged"] = merged
        h["n_registry_distinct"] = 1 if merged else len(val)
        h["note"] = ("합쳐짐 — 이완 뒤 두 registry 가 같은 자리 (카드 §4: 하나로 보고)" if merged else
                     ("registry 하나만 유효 (INCOMPLETE " + ",".join(inc) + ")" if len(val) == 1 else
                      ("유효 표본 없음" if not val else "두 registry 따로 — 평균 · [min, max]")))
        head[f"{kind}_{term}"] = h
    out_s = []
    for k in sorted(samples):
        s = {kk: vv for kk, vv in samples[k].items() if not kk.startswith("_")}
        out_s.append(s)
    return {"schema": "wad_se_pairs_collect/v1", "run_dir": os.path.relpath(os.path.abspath(run_dir), S.REPO) if os.path.abspath(run_dir).startswith(S.REPO + os.sep) else os.path.abspath(run_dir), "n_samples": len(samples),
            "G1_pass": sum(s["G1"] for s in samples.values()), "G2_pass": sum(s["G2"] for s in samples.values()),
            "G3": g3, "registry": reg_out, "headline_by_term": head, "samples": out_s,
            "rules": {"fmax_eV_A": fmax_target, "max_steps": max_steps, "G3_tol_J_m2": G3_TOL_J_M2, "G3_reps": {k: "_".join(v) for k, v in G3_REPS.items()},
                      "merge_tol_A": B.MERGE_TOL_A, "headline": "종결별 · 유효 registry 평균 · [min, max] · 2체 D3 · 10 Å · ATM 열 따로 (카드 §1·§5)"}}


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
        # ── GPU 공유 안전장치 (2026-10-01) — 가짜 nvidia-smi 가 파일의 숫자를 찍는다 ──
        gv = os.path.join(T, "gpuval"); fake = os.path.join(T, "fake-nvidia-smi")
        open(fake, "w").write(f"#!/bin/sh\ncat {gv}\n"); os.chmod(fake, 0o755)
        env0 = {k: os.environ.get(k) for k in ("WAD_NVSMI", "WAD_GUARD_POLL", "WAD_GUARD_SAMPLE")}
        os.environ.update({"WAD_NVSMI": fake, "WAD_GUARD_POLL": "0.1", "WAD_GUARD_SAMPLE": "0.1"})
        try:
            open(gv, "w").write("3000\n")
            rec, rc = relax(md, os.path.join(md, "g1"), calc_kind="emt", d3_kind="none", fmax=0.05, steps=5, gpu_start_max_mib=12000, gpu_wait_s=2)
            ck("시작 문턱: 합계 3000 ≤ 12000 → 바로 시작 (이완 산출물 있음)", rec["gpu_guard"]["start_gate"]["ok"] and os.path.isfile(os.path.join(md, "g1", "relaxed.extxyz")), rec.get("gpu_guard"))
            open(gv, "w").write("43000\n")
            rec, rc = relax(md, os.path.join(md, "g2"), calc_kind="emt", d3_kind="none", fmax=0.05, steps=5, gpu_start_max_mib=12000, gpu_wait_s=1)
            ck("⛔음성 시작 문턱: 합계 43000 > 12000 가 대기 상한 넘게 → 종료 4 · 이완 안 함", rc == 4 and os.path.isfile(os.path.join(md, "g2", "gate_refused.json"))
               and not os.path.exists(os.path.join(md, "g2", "relaxed.extxyz")), (rc, rec.get("gpu_guard")))
            os.environ["WAD_NVSMI"] = os.path.join(T, "없는-nvidia-smi")
            rec, rc = relax(md, os.path.join(md, "g3"), calc_kind="emt", d3_kind="none", fmax=0.05, steps=5, gpu_start_max_mib=12000, gpu_wait_s=1)
            ck("⛔음성 시작 문턱: nvidia-smi 를 못 읽으면 시작하지 않는다 (fail-closed · 종료 4)", rc == 4 and "못 읽었다" in rec["gpu_guard"]["start_gate"]["reason"], rec.get("gpu_guard"))
            os.environ["WAD_NVSMI"] = fake
            open(gv, "w").write("43000\n")
            import threading as _th
            _th.Timer(0.5, lambda: open(gv, "w").write("3000\n")).start()
            rec, rc = relax(md, os.path.join(md, "g4"), calc_kind="emt", d3_kind="none", fmax=0.05, steps=5, gpu_start_max_mib=12000, gpu_wait_s=10)
            ck("시작 문턱: 43000 → 0.5 s 뒤 3000 이면 기다렸다가 시작", rec["gpu_guard"]["start_gate"]["ok"] and rec["gpu_guard"]["start_gate"]["waited_s"] >= 0.3, rec["gpu_guard"]["start_gate"])
            envs = dict(os.environ)
            open(gv, "w").write("47000\n")
            r = subprocess.run([sys.executable, __file__, "--model_dir", md, "--out", os.path.join(md, "g5"), "--calc", "emt", "--d3", "none",
                                "--steps", "200000", "--fmax", "1e-9", "--gpu_kill_total_mib", "45500"], capture_output=True, text=True, env=envs, timeout=120)
            ck("⛔음성 감시: 합계 47000 > 45500 → 이 프로세스만 종료 3 · gpu_guard.json", r.returncode == 3 and os.path.isfile(os.path.join(md, "g5", "gpu_guard.json")), (r.returncode, r.stdout[-200:]))
            open(gv, "w").write("3000\n")
            r = subprocess.run([sys.executable, __file__, "--model_dir", md, "--out", os.path.join(md, "g6"), "--calc", "emt", "--d3", "none",
                                "--steps", "30", "--fmax", "0.05", "--gpu_kill_total_mib", "45500"], capture_output=True, text=True, env=envs, timeout=120)
            ck("감시: 합계 3000 이면 끝까지 돈다 (종료 3 아님 · gpu_guard.json 없음)", r.returncode in (0, 2) and not os.path.exists(os.path.join(md, "g6", "gpu_guard.json")), (r.returncode, r.stdout[-200:]))
            rec, rc = relax(md, os.path.join(md, "g7"), calc_kind="emt", d3_kind="none", mem_probe=True, vram_cap_mib=1800)
            ck("mem_probe: 힘 한 번 · mem_probe.json · 이완 산출물 없음 · EMT 는 상한 '해당 없음'", rc == 0 and os.path.isfile(os.path.join(md, "g7", "mem_probe.json"))
               and not os.path.exists(os.path.join(md, "g7", "relaxed.extxyz")) and rec["calculator"].get("vram_cap") == "해당 없음 (EMT)", rec.get("calculator"))
        finally:
            for k, v in env0.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        # ── W 단계 (--w_from · SE 쌍 카드 §2) — EMT 로 흐름만 · 음성: 다른 모델의 이완본 · 손댄 이완 좌표 · UMA+d3 none ──
        wr = w_endpoints(md, os.path.join(md, "relax"), gaps=(8.0, 10.0), calc_kind="emt", d3_kind="none")
        ck("W 단계: 끝점 둘 (8·10 Å) · W 유한 · 넓이 > 0 · G3 계산됨 · far 간격 ≥ gap", set(wr["gaps"]) == {"8", "10"} and all(np.isfinite(v["W_2body_J_m2"]) for v in wr["gaps"].values())
           and wr["area_A2"] > 0 and wr["G3"] is not None and wr["gaps"]["10"]["endpoint"]["far_gap_direct_image_A"][0] >= 10 - 1e-6, {k: v["W_2body_J_m2"] for k, v in wr["gaps"].items()})
        ck("W 단계: W = (E_far − E_bound)/A × 16.0218 (부호·단위 검산)", all(abs(v["W_2body_J_m2"] - (v["E_far_eV"] - v["E_bound_eV"]) / wr["area_A2"] * 16.02176634) < 1e-9
           for v in wr["gaps"].values()))
        ck("W 단계: ATM 은 계산되거나 '미계산 (0 아님)' — 0 으로 채우지 않는다", all((v["dW_ATM_J_m2"] is not None) or ("미계산" in v["ATM_status"]) for v in wr["gaps"].values()))
        try:
            w_endpoints(md, os.path.join(md, "g6"), gaps=(8.0,), calc_kind="emt", d3_kind="none")          # g6 = 같은 모델 · 정상 이완본 (위 감시 시험)
            m_ok = True
        except SlabError:
            m_ok = False
        ck("W 단계: 같은 모델의 다른 이완 폴더(g6)도 받는다", m_ok)
        B.write_models(os.path.join(T, "V2b"), {"hollow_fcc": B.build_v2(d0=2.0)["hollow_fcc"]})
        try:
            w_endpoints(os.path.join(T, "V2b", "hollow_fcc"), os.path.join(md, "relax"), gaps=(8.0,), calc_kind="emt", d3_kind="none"); bad = False
        except SlabError as e:
            bad = "다른 모델" in str(e)
        ck("⛔음성 W 단계: 다른 모델의 이완본을 주면 거부 (init_sha256 불일치)", bad)
        rp = os.path.join(md, "relax", "relaxed.extxyz"); keep = open(rp).read(); open(rp, "w").write(keep + "\n")
        try:
            w_endpoints(md, os.path.join(md, "relax"), gaps=(8.0,), calc_kind="emt", d3_kind="none"); bad = False
        except SlabError as e:
            bad = "손댄" in str(e)
        ck("⛔음성 W 단계: 이완 좌표를 손대면 거부 (relaxed_sha256 불일치)", bad)
        open(rp, "w").write(keep)
        try:
            w_endpoints(md, os.path.join(md, "relax"), gaps=(8.0,), calc_kind="uma", d3_kind="none"); bad = False
        except SlabError as e:
            bad = "d3" in str(e).lower()
        ck("⛔음성 W 단계: UMA + --d3 none → 거부", bad)
        # ── P1 · P2 (SE 쌍 전체 계면) 도 이 도구가 받는다 — 사전 점검만 (계산 0) ──
        for kind, term in (("P1", "s_outer"), ("P2", "li_outer")):
            B.write_models(os.path.join(T, kind), {"A": B.build_full(kind, term)["A"]})
            try:
                recp, rcp = relax(os.path.join(T, kind, "A"), os.path.join(T, kind, "A", "pre"), calc_kind="emt", d3_kind="none", preflight_only=True)
                okp = rcp == 0 and recp["preflight"]["mask_matches_policy"] and not recp["preflight"]["flags"]; infop = recp.get("preflight")
            except SlabError as e:
                okp, infop = False, str(e)
            ck(f"{kind} {term}: 사전 점검 통과 (마스크 = 정책 · 깃발 0)", okp, infop)
        # ── --collect (SE 쌍 카드 §4·§5 집계) — 가짜 이완·W 로 논리만 · 음성: fmax · 깃발 · G3 · sha · 빠진 W · 합쳐짐 ──
        import shutil
        from ase.io import write as awrite
        RD = os.path.join(T, "run")
        pm = B.build_full("P2", "s_outer")
        B.write_models(os.path.join(RD, "models", "P2_s_outer"), {"A": pm["A"], "B": pm["B"]})

        def fake(reg, w10, g3v=0.005, fmx=0.015, flg=(), relaxed=None):
            md_ = os.path.join(RD, "models", "P2_s_outer", reg); rd_ = os.path.join(RD, "relax", "P2_s_outer", reg); os.makedirs(rd_, exist_ok=True)
            rp_ = os.path.join(rd_, "relaxed.extxyz")
            if relaxed is None:
                shutil.copy(os.path.join(md_, "bound.extxyz"), rp_)
            else:
                awrite(rp_, relaxed)
            si, sr = _sha(os.path.join(md_, "bound.extxyz")), _sha(rp_)
            json.dump({"init_sha256": si, "relaxed_sha256": sr, "converged_fmax": fmx <= 0.02, "steps_taken": 10, "fmax_free_final_eV_A": fmx,
                       "interface_check_flags": list(flg), "wall_s": 1.0}, open(os.path.join(rd_, "relax_meta.json"), "w"))
            os.makedirs(os.path.join(RD, "w"), exist_ok=True)
            json.dump({"init_sha256": si, "relaxed_sha256": sr, "area_A2": 300.0,
                       "gaps": {"10": {"W_2body_J_m2": w10, "dW_ATM_J_m2": -0.04, "E_bound_eV": -1.0, "E_far_eV": 0.0}, "12": {"W_2body_J_m2": w10 + g3v, "dW_ATM_J_m2": -0.041}},
                       "G3": {"abs_dW_J_m2": g3v}}, open(os.path.join(RD, "w", f"P2_s_outer_{reg}.json"), "w"))
        fake("A", 0.21); fake("B", 0.22)
        c = collect(RD); h = c["headline_by_term"]["P2_s_outer"]
        ck("collect: G1·G2 2/2 · G3 PASS · registry 따로 (1.31 Å) · 평균 0.215 · [0.21, 0.22] · ATM −0.04",
           c["G1_pass"] == 2 and c["G2_pass"] == 2 and c["G3"]["P2"]["status"] == "PASS" and not h["registry_merged"] and h["n_registry_distinct"] == 2
           and abs(h["W2_10_mean_J_m2"] - 0.215) < 1e-12 and h["W2_10_min_max_J_m2"] == [0.21, 0.22] and abs(h["dW_ATM_10_mean_J_m2"] + 0.04) < 1e-12
           and abs(c["registry"]["P2_s_outer"]["final_A"] - 1.307) < 0.01, (h, c["G3"]))
        ck("collect: P1 표본이 없으면 P1 G3 는 안 나온다 (없는 대표를 PASS 로 쓰지 않는다)", "P1" not in c["G3"], c["G3"])
        fake("B", 0.22, fmx=0.0)
        ck("collect: fmax 0.0 은 유효 (`or` 함정 아님) → G1 통과", collect(RD)["G1_pass"] == 2)
        fake("B", 0.22, fmx=0.03)
        h = collect(RD)["headline_by_term"]["P2_s_outer"]
        ck("⛔음성 collect: B fmax 0.03 → INCOMPLETE · 헤드라인 = A 하나 · 교체 없음", h["INCOMPLETE"] == ["B"] and h["n_registry_valid"] == 1 and h["W2_10_mean_J_m2"] == 0.21, h)
        fake("B", 0.22, flg=("PS4_broken",))
        h = collect(RD)["headline_by_term"]["P2_s_outer"]
        ck("⛔음성 collect: B 깃발 → INCOMPLETE (G2)", h["INCOMPLETE"] == ["B"] and h["n_registry_valid"] == 1, h)
        fake("B", 0.22); fake("A", 0.21, g3v=0.02)
        c = collect(RD); h = c["headline_by_term"]["P2_s_outer"]
        ck("⛔음성 collect: 대표 G3 0.02 > 0.01 → FAIL · 라벨 '끝점 미수렴' · 헤드라인은 10 Å 그대로",
           c["G3"]["P2"]["status"] == "FAIL" and "끝점 미수렴" in (h["G3_label"] or "") and abs(h["W2_10_mean_J_m2"] - 0.215) < 1e-12, c["G3"])
        fake("A", 0.21)
        bas = B.ads_lattice("P2", pm["A"]["bound"].cell.array); y = pm["A"]["bound"].copy(); py_ = y.get_positions()
        mk = np.array([q == "C" for q in y.get_chemical_symbols()]); py_[mk, :2] += bas[0]; y.set_positions(py_)
        fake("B", 0.21, relaxed=y)
        h = collect(RD)["headline_by_term"]["P2_s_outer"]
        ck("collect: B 이완본이 A 와 같은 자리 (격자 이동) → 합쳐짐 · 서로 다른 registry 1 개", h["registry_merged"] and h["n_registry_distinct"] == 1, h)
        fake("B", 0.22)
        rp = os.path.join(RD, "relax", "P2_s_outer", "B", "relaxed.extxyz"); keep = open(rp).read(); open(rp, "w").write(keep + "\n")
        try:
            collect(RD); bad = False
        except SlabError as e:
            bad = "sha 사슬" in str(e)
        ck("⛔음성 collect: 이완본을 손대면 거부 (sha 사슬)", bad)
        open(rp, "w").write(keep)
        wb = os.path.join(RD, "w", "P2_s_outer_B.json"); os.rename(wb, wb + ".x")
        try:
            collect(RD); bad = False
        except SlabError as e:
            bad = "없다" in str(e)
        ck("⛔음성 collect: W 기록이 빠지면 건너뛰지 않고 거부", bad)
        os.rename(wb + ".x", wb)
        ck("collect: 복구 뒤 다시 통과", collect(RD)["G1_pass"] == 2)
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
    ap.add_argument("--vram_cap_mib", type=float, default=None, help="이 프로세스 GPU 메모리 상한 (torch · 컨텍스트 제외)")
    ap.add_argument("--gpu_kill_total_mib", type=int, default=None, help="GPU 합계가 이 값을 넘으면 이 프로세스만 종료 3")
    ap.add_argument("--gpu_start_max_mib", type=int, default=None, help="GPU 합계가 이 값 이하일 때만 시작 (못 읽으면 시작 안 함)")
    ap.add_argument("--gpu_wait_s", type=int, default=3600, help="시작 문턱 대기 상한 (넘으면 종료 4)")
    ap.add_argument("--mem_probe", action="store_true", help="힘 한 번 계산하고 최대 메모리만 기록 (이완 없음)")
    ap.add_argument("--w_from", metavar="MODEL_DIR", help="W 단계 (SE 쌍 카드 §2): 이 모델의 이완본(--relax_dir)에서 끝점을 만들어 W_UMA+D3 · ATM · G3 → --out")
    ap.add_argument("--relax_dir", help="--w_from 과 함께: relaxed.extxyz · relax_meta.json 이 있는 폴더")
    ap.add_argument("--gaps", type=float, nargs="+", default=[10.0, 12.0], help="--w_from 끝점 간격 (Å) · 기본 10 12 (G3)")
    ap.add_argument("--collect", metavar="RUN_DIR", help="SE 쌍 카드 §4·§5 집계: RUN_DIR/{models,relax,w} → sha 사슬 · G1 · G2 · G3 · registry 합쳐짐 · 종결별 헤드라인 (→ --out JSON)")
    ap.add_argument("--d3_energy", metavar="STRUCT", help="S3 전 예외 ② D3 결박 검사용: 이 구조의 외부 D3 에너지만 찍는다 (eV · Ry · 구현·버전)")
    ap.add_argument("--energies", metavar="STRUCT", nargs="+", help="S4 집계용: 구조들의 **UMA 단일점 에너지(D3 없음 · default 모드 · 3축 pbc)** 를 JSON 으로 (개정 1: D3 항은 QE 출력에서). --out 에 쓴다")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.collect:
        rec = collect(a.collect)
        if a.out:
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            open(a.out, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1, default=float) + "\n")
        fmt = lambda v, d=4: "—" if v is None else f"{v:.{d}f}"
        print(f"collect: 표본 {rec['n_samples']} · G1 {rec['G1_pass']}/{rec['n_samples']} · G2 {rec['G2_pass']}/{rec['n_samples']} · G3 "
              + " · ".join(f"{k} {v['status']}" for k, v in rec["G3"].items()))
        for k, h in rec["headline_by_term"].items():
            r = rec["registry"].get(k, {})
            mm = h.get("W2_10_min_max_J_m2") or [None, None]
            print(f"  {k}: W2(10 Å) {fmt(h.get('W2_10_mean_J_m2'))} [{fmt(mm[0])}, {fmt(mm[1])}] · ATM {fmt(h.get('dW_ATM_10_mean_J_m2'))} · "
                  f"registry {r.get('init_A', '—')} → {r.get('final_A', '—')} Å ({'합쳐짐' if h['registry_merged'] else '따로'}) · 유효 {h['n_registry_valid']}"
                  + (f" · INCOMPLETE {h['INCOMPLETE']}" if h["INCOMPLETE"] else "") + (f" · {h['G3_label']}" if h.get("G3_label") else ""))
        if a.out:
            print(f"→ {a.out}")
        return 0
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
        # ⛔ 키는 고유해야 한다 — 2026-09-26 실측: S2 의 relaxed.extxyz 4 개(폴더만 다름)를 파일명으로 키를 잡아 셋을 덮어썼다.
        #   파일명이 겹치면 "<상위폴더>/<파일명>" 으로, 그래도 겹치면 실행을 거부한다 (조용히 덮어쓰지 않는다).
        bases = [os.path.splitext(os.path.basename(p))[0] for p in a.energies]
        keys = [b if bases.count(b) == 1 else f"{os.path.basename(os.path.dirname(os.path.abspath(p)))}/{b}" for p, b in zip(a.energies, bases)]
        if len(set(keys)) != len(keys):
            raise SystemExit(f"⛔ --energies 구조 이름이 겹친다 (상위폴더까지 같음): {keys}")
        for p, key in zip(a.energies, keys):
            at = read(p); at.set_pbc((True, True, True)); at.calc = base
            rows[key] = {"struct": os.path.abspath(p), "sha256": _sha(p), "n_atoms": len(at), "formula": at.get_chemical_formula(),
                         "E_UMA_eV": float(at.get_potential_energy()), "pbc": [True, True, True]}
        rec = {"schema": "uma_energies/v1", "what": "UMA 단일점 에너지 (D3 없음) — W_UMA 용 · D3 항은 QE 출력에서 (개정 1)", "calculator": {k: v for k, v in info.items() if k != "d3"},
               "energies": rows}
        txt = json.dumps(rec, ensure_ascii=False, indent=1, default=float)
        if a.out:
            open(a.out, "w", encoding="utf-8").write(txt + "\n"); print(f"-> {a.out}")
        print(txt if not a.out else json.dumps({k: v["E_UMA_eV"] for k, v in rows.items()}, ensure_ascii=False))
        return 0
    if a.w_from:
        if not (a.relax_dir and a.out):
            ap.error("--w_from 에는 --relax_dir · --out 이 필요하다")
        rec = w_endpoints(a.w_from, a.relax_dir, a.gaps, a.calc, a.device, a.d3, a.vram_cap_mib, a.gpu_kill_total_mib, a.gpu_start_max_mib, a.gpu_wait_s,
                          out_dir=os.path.dirname(os.path.abspath(a.out)))
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(json.dumps(rec, ensure_ascii=False, indent=1, default=float) + "\n")
        g = rec["gaps"]; k0 = next(iter(g))
        print(f"W {rec['model']} {rec['term']} {rec['registry']} · 수렴 {rec['relax']['converged_fmax']} · 깃발 {len(rec['relax']['interface_check_flags'] or [])} · "
              + " · ".join(f"{k} Å W2 {v['W_2body_J_m2']:.4f}" + ("" if v['dW_ATM_J_m2'] is None else f" ATM {v['dW_ATM_J_m2']:+.4f}") for k, v in g.items())
              + (f" · G3 |ΔW| {rec['G3']['abs_dW_J_m2']:.4f} {rec['G3']['status']}" if rec["G3"] else "") + f" → {a.out}")
        return 0
    if not a.model_dir:
        ap.error("--model_dir 이 필요하다")
    out = a.out or os.path.join(a.model_dir, "relax")
    rec, rc = relax(a.model_dir, out, a.calc, a.device, a.d3, a.fmax, a.steps, a.optimizer, a.preflight_only,
                    a.vram_cap_mib, a.gpu_kill_total_mib, a.gpu_start_max_mib, a.gpu_wait_s, a.mem_probe)
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
