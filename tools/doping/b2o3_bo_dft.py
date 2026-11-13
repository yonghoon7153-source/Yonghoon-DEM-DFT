#!/usr/bin/env python3
"""b2o3 B·O 배치 카드 — 9 단계 DFT (단일점 → k 탐침 → 고정셀 이온 이완 → EOS 생략 판정) + 10 단계 고르기.

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json — 개정_1 단계별_값 9_DFT · 10_고르기 · 판독_계약 (EOS_생략 ·
서술_한계) + 개정_5 (9 단계 운영값 · 결과 전 · [제안]) · Codex DY 확인 4 (EOS 의 (E, P, V) 를 결과 파일에 결속).
절차 db/properties/cell_construction_protocol_v1_2026_11_09.json 9_DFT_확인 · 10_고르기 · 13_기록_계보.

  prepare      8 단계 결과를 판 고정 판독기로 다시 결속 (anneal_readout 다시 내기 · 본 판독 파일 몸통 대조 · 보류면 멈춤) →
               가족마다 UMA 어닐 최저 둘 (6 · 판독기의 성공 정의 그대로 · 가족 최저 · 성공 수를 본 판독과 대조) →
               단일점 입력 (UMA 이완 기하 그대로 · 셀 포함 · k_main) + 계획 dft_plan.json
               (이 도구 · 판독기 sha256 · 묶인 입력 · 유사포텐셜 파일 sha256 · md5 · 구조 파일 sha256 · 입력 sha256)
  read_sp      계획 · 8 단계를 다시 결속 (계획의 고르기를 다시 내서 대조) → 단일점 출력 6 결속 · 검사 → 단일점 가족 순서 (G5 기록) →
               k_main 3×2×1 이면 k 탐침 입력 (가족 대표 셋 = 가족마다 단일점 최저 · 4×2×1) ·
               k_main 4×2×1 (탐침 발동 뒤 판) 이면 탐침 없이 이완 입력
  read_kprobe  단일점 판정 · 탐침 출력 3 결속 → 발동 판정 (세 가족 쌍 모두: 차가 0.05 넘게 변함 · 순서 바뀜 · 0.10 경계 건넘) →
               발동 안 하면 이완 입력 (기준 셀 · k_main) · 발동하면 멈춘다 (6 단일점을 4×2×1 로 — prepare --k_main 4 2 1 --after_kprobe)
  read_relax   이완 출력 3 결속 → 가족마다 (E, P, V) 를 **출력 파일에서** 읽는다 (DY 확인 4 · 손으로 옮기지 않는다) →
               판 고정 eos_robust → EOS 생략이면 DFT 가족 순서 · 승자–차저 0.10 판정 · 10 단계 고르기 (안정성 대상 · 전자구조 대상) ·
               생략 불가면 'EOS 필요' 에서 멈춘다 (고르기 안 함)

출력 결속 (단계마다 · 잡마다): 입력 파일 sha256 = 계획 값 · 출력에 찍힌 입력 이름 · 원자 수 · ecut · 수렴 문턱 · smearing 종류 · 폭 ·
교환상관 (PBE) · 비스핀 · 유사포텐셜 파일 이름 · MD5 (계획 값) · 셀 축 · 처음 좌표 (그 잡의 입력과 같아야 한다 — 다른 잡 출력 바꿔치기를
잡는다) · JOB DONE · SCF 수렴 (NOT achieved 없음) · 단계 안 k 점 수 · PWSCF 판 같음 · 단일점은 힘 블록 · 이완은 'bfgs converged' ·
최종 좌표 · Final energy = 마지막 '!' · 응력이 마지막 '!' 뒤 · 부피 = 기준 셀 V₀.

⛔ 이 도구가 못 하는 것
  · pw.x 를 돌리지 않는다 (실행기 tools/doping/run_force_check_scf.sh · gabia GPU · MIN_FREE_MIB 로 UMA 와 같이 안 돈다).
  · EOS (부피 격자 · BM3) 를 하지 않는다 — 생략 불가면 멈추고 어느 셀인지 말한다 (EOS 는 다음 판 · 결과 전에 정한 대로).
  · 수렴을 보장하지 않는다 — 실패 · 누락 잡은 판정에 넣지 않고 멈춘다 (같은 설정으로 다시 돌린 뒤 판독 · 누락 ≠ 실패).
  · 단일점만으로 'DFT 순위' 를 쓰지 않는다 (절차 9_DFT_확인 ⛔) — 단일점 순서는 G5 기록 · 판정은 이온 이완 뒤.
  · 유사포텐셜이 'B₂O₃ 캠페인 PP' 와 바이트까지 같은지 보증하지 못한다 (7 월 원본은 저장소 밖) — 파일 이름 · 원소 머리 ·
    sha256 · md5 를 기록하고 출력의 MD5 와 대조할 뿐이다.
  · 이완 뒤 골격이 깨졌는지 판정하지 않는다 — B · P 배위 · O 끝 꼴은 **기록** (카드 G7 · 판정 아님).
  · 띠틈 · DOS (12 단계) · 안정성 MD (11 단계) 는 다른 도구다 — 여기는 대상 목록 (계보 해시) 까지.

쓰는 법 (gabia — 판 고정 판독기 $R/src · 이 도구는 다른 worktree)
  python3 b2o3_bo_dft.py --selftest
  python3 b2o3_bo_dft.py prepare --readout_tool $R/src/tools/doping/b2o3_bo_readout.py --verdict $R/s6_verdict.json \
          --receipt $R/s7_receipt.json --results $R/s8_anneal/anneal_results.json --readout $R/s8_readout.json \
          --pseudo_dir /data/work/pseudo --out_dir $R/s9_dft
  MIN_FREE_MIB=45000 bash $R/src/tools/doping/run_force_check_scf.sh $R/s9_dft/sp
  python3 b2o3_bo_dft.py read_sp --readout_tool … --plan $R/s9_dft/dft_plan.json --out $R/s9_dft/sp_verdict.json
  MIN_FREE_MIB=45000 bash … run_force_check_scf.sh $R/s9_dft/kprobe
  python3 b2o3_bo_dft.py read_kprobe --readout_tool … --sp_verdict $R/s9_dft/sp_verdict.json --host <modelc_V0_k663.xyz> \
          --out $R/s9_dft/kprobe_verdict.json
  MIN_FREE_MIB=45000 bash … run_force_check_scf.sh $R/s9_dft/relax
  python3 b2o3_bo_dft.py read_relax --readout_tool … --prev $R/s9_dft/kprobe_verdict.json --out $R/s9_dft/relax_verdict.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np

SELF = Path(__file__).resolve()
HERE = SELF.parent
DEFAULT_RD = HERE / "b2o3_bo_readout.py"
PINNED_RD_SHA256 = "872d91f7508ad21c3d67f373bee228bd894994b731a77f69525818db3a8967cf"   # 12b8bdef (Codex DY GO)
HOST_SHA256 = "dc0f8c0c12df6ef6a034e78a9b489b09fd8d472b01f1d9b02e8c860f6410a1e6"          # db/structures/modelc_V0_k663.xyz

KIND_PLAN = "b2o3_bo_dft_plan/v1"
KIND_SP = "b2o3_bo_dft_sp_verdict/v1"
KIND_KP = "b2o3_bo_dft_kprobe_verdict/v1"
KIND_RX = "b2o3_bo_dft_relax_verdict/v1"

RY_EV = 13.605693122994
BOHR_A = 0.529177210903
RYBOHR_EVA = RY_EV / BOHR_A
FAM = ["F_B", "F_P", "F_free"]
TAG = {"F_B": "FB", "F_P": "FP", "F_free": "Ffree"}
SPECIES = ["Li", "B", "O", "P", "S", "Cl"]
MASS = {"Li": 6.941, "B": 10.811, "O": 15.9994, "P": 30.974, "S": 32.065, "Cl": 35.453}
PP = {"Li": "li_pbe_v1.4.uspp.F.UPF", "B": "B.pbe-n-kjpaw_psl.1.0.0.UPF", "O": "O.pbe-n-kjpaw_psl.0.1.UPF",
      "P": "P.pbe-n-rrkjus_psl.1.0.0.UPF", "S": "s_pbe_v1.4.uspp.F.UPF", "Cl": "cl_pbe_v1.4.uspp.F.UPF"}

#: 카드 개정_1 9_DFT (기존 · 비준) + 개정_5 (운영값 · [제안] · 결과 전) — 이 값과 다른 출력은 판독하지 않는다
DFT = {
    "ecutwfc": 52.0, "ecutrho": 520.0, "occupations": "smearing", "smearing": "gaussian", "degauss": 0.01,
    "nspin": 1, "conv_thr": 1.0e-8,
    "mixing_mode": "plain", "mixing_beta": 0.3, "electron_maxstep": 200, "diagonalization": "david",   # [제안 개정 5]
    "disk_io": "nowf",                                                                                   # [제안 개정 5]
    "k_main": [3, 2, 1], "k_probe": [4, 2, 1], "n_per_family": 2,
    "margin_dft_eV": 0.10, "kprobe_shift_eV": 0.05,
    "relax": {"forc_conv_thr": 1.0e-3, "etot_conv_thr": 1.0e-5, "nstep": 200, "ion_dynamics": "bfgs"},  # [제안 개정 5]
    "ref_cell": {"host_sha256": HOST_SHA256, "supercell": [1, 2, 1], "V0_A3": 2436.33},
    "B_range_GPa": [21.7, 32.5], "P_max_GPa": 2.0,
    "composition": {"B": 2, "Cl": 16, "Li": 58, "O": 3, "P": 8, "S": 41}, "nat": 128,
    "n_stability_winner": 3,
}
TOL = {"ecut": 1e-6, "conv_rel": 1e-6, "degauss": 1e-6, "cell_A": 1e-4, "pos_A": 1e-4, "V_A3": 0.01, "E_final_Ry": 1e-6}
B_CUT_A = {"S": 2.2, "O": 1.7}            # 기록용 B 배위 (카드 G7 · 판정 아님)
P_CUT_A = {"S": 2.4, "O": 1.8}            # 기록용 P 배위 (골격 기록 · 판정 아님)

NEED = ("anneal_readout", "verify_screen_verdict", "load_records", "_core", "end_motif", "eos_robust", "CONTRACT", "FAM_ORDER")


# ───────────────────────── 공통 ─────────────────────────
def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _md5(p) -> str:
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def _tool_fp() -> dict:
    return {"path": str(SELF), "sha256": _sha(SELF)}


def _fnum(x) -> str:
    m, e = f"{float(x):.1e}".split("e")
    return f"{m}d{int(e)}"


def _rel(p, base) -> str:
    return os.path.relpath(Path(p).resolve(), Path(base).resolve())


def _bound(entry, base, what) -> Path:
    """기록된 {rel · sha256} → 파일 (있고 sha256 이 같아야 한다)."""
    if not entry or not entry.get("rel") or not entry.get("sha256"):
        raise SystemExit(f"⛔ 묶인 {what} 기록이 없다 — 판독하지 않는다")
    p = (Path(base) / entry["rel"]).resolve()
    if not p.is_file():
        raise SystemExit(f"⛔ 묶인 {what} 파일이 없다 ({p})")
    if _sha(p) != entry["sha256"]:
        raise SystemExit(f"⛔ 묶인 {what} 파일이 기록 뒤 바뀌었다 (sha256 · {p.name}) — 판독하지 않는다")
    return p


def _entry(p, base) -> dict:
    return {"rel": _rel(p, base), "sha256": _sha(p)}


def _dump(obj, path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n")
    return path


def _load(path, kind) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"⛔ {p} 가 없다")
    d = json.loads(p.read_text(encoding="utf-8"))
    if d.get("kind") != kind:
        raise SystemExit(f"⛔ {p.name} 는 {kind} 가 아니다 ({d.get('kind')})")
    return d


def load_rd(path=None):
    """판 고정 판독기를 불러온다 (그 파일 옆의 run_anneal · b2o3_enumerate 를 판독기가 스스로 불러온다)."""
    p = Path(path or DEFAULT_RD).resolve()
    if not p.is_file():
        raise SystemExit(f"⛔ 판독기 파일이 없다 ({p})")
    spec = importlib.util.spec_from_file_location("b2o3_bo_readout_for_dft", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    miss = [k for k in NEED if not hasattr(mod, k)]
    if miss:
        raise SystemExit(f"⛔ 판독기 {p.name} 에 {miss} 가 없다 — 이 도구가 기대하는 판이 아니다")
    mod.__dft_path__, mod.__dft_sha256__ = str(p), _sha(p)
    return mod


def check_rd(RD, pinned=True):
    if pinned and RD.__dft_sha256__ != PINNED_RD_SHA256:
        raise SystemExit(f"⛔ 판독기 sha256 {RD.__dft_sha256__[:12]}… 이 판 고정 값 ({PINNED_RD_SHA256[:12]}… = 12b8bdef) 이 아니다")
    C = RD.CONTRACT
    for k, mine in (("margin_dft_eV", DFT["margin_dft_eV"]), ("B_range_GPa", DFT["B_range_GPa"]),
                    ("eos_P_max_GPa", DFT["P_max_GPa"])):
        if C.get(k) != mine:
            raise SystemExit(f"⛔ 판독기 CONTRACT {k} = {C.get(k)} ≠ 이 도구 {mine} — 판정 기준이 갈린다")
    if list(RD.FAM_ORDER) != FAM:
        raise SystemExit(f"⛔ 판독기 가족 {RD.FAM_ORDER} ≠ {FAM}")


def _same_tools(RD, d, what):
    """앞 단계 파일을 만든 도구 · 판독기와 지금 판이 같아야 한다 (단계 사이에 규칙이 바뀌지 않게)."""
    t = d.get("tools") or {}
    if (t.get("dft_tool") or {}).get("sha256") != _tool_fp()["sha256"]:
        raise SystemExit(f"⛔ 이 도구 sha256 이 {what} 를 만든 판과 다르다 — 같은 판으로만 잇는다")
    if (t.get("readout_tool") or {}).get("sha256") != RD.__dft_sha256__:
        raise SystemExit(f"⛔ 판독기 sha256 이 {what} 를 만든 판과 다르다 — 같은 판독기로만 잇는다")


def _tools(RD) -> dict:
    return {"dft_tool": _tool_fp(), "readout_tool": {"path": RD.__dft_path__, "sha256": RD.__dft_sha256__}}


# ───────────────────────── 유사포텐셜 ─────────────────────────
def upf_element(path):
    txt = Path(path).read_text(errors="ignore")[:20000]
    m = re.search(r'element\s*=\s*"\s*([A-Za-z]{1,2})\s*"', txt, re.I)
    if m:
        return m.group(1).capitalize()
    m = re.search(r"^\s*([A-Za-z]{1,2})\s+Element", txt, re.M)
    return m.group(1).capitalize() if m else None


def pseudo_record(pdir) -> dict:
    pdir = Path(pdir)
    rec, bad = {}, []
    for el in SPECIES:
        f = pdir / PP[el]
        if not f.is_file():
            bad.append(f"{el}: {f} 없음")
            continue
        e = upf_element(f)
        if e != el:
            bad.append(f"{el}: {f.name} 의 원소 머리 {e} ≠ {el}")
            continue
        rec[el] = {"file": PP[el], "sha256": _sha(f), "md5": _md5(f)}
    if bad:
        raise SystemExit("⛔ 유사포텐셜 — " + " · ".join(bad) + " — 시작하지 않는다")
    return {"dir": str(pdir.resolve()), "files": rec}


# ───────────────────────── 입력 쓰기 · 읽기 ─────────────────────────
def write_pw_input(path, atoms, *, prefix, calc, k, pseudo_dir, tstress=False) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pw_input_text(atoms, prefix=prefix, calc=calc, k=k, pseudo_dir=pseudo_dir, tstress=tstress))
    return path


def _text_sha(t: str) -> str:
    return hashlib.sha256(t.encode()).hexdigest()


def pw_input_text(atoms, *, prefix, calc, k, pseudo_dir, tstress=False) -> str:
    """QE pw.x 입력 — 셀 CELL_PARAMETERS angstrom · 좌표 crystal (원자 순서 그대로) · K_POINTS automatic k 0 0 0.

    결정론 (같은 구조 · 인자 → 같은 바이트) — 뒤 단계가 입력을 다시 만들어 sha256 으로 대조한다 (판정 파일의 잡 목록을 믿지 않는다).
    """
    syms = atoms.get_chemical_symbols()
    present = [e for e in SPECIES if e in set(syms)]
    if set(syms) - set(SPECIES):
        raise SystemExit(f"⛔ 모르는 원소 {sorted(set(syms) - set(SPECIES))}")
    cell = np.asarray(atoms.cell.array, float)
    frac = atoms.get_scaled_positions(wrap=False)
    L = ["&CONTROL", f"    calculation = '{calc}'", f"    prefix = '{prefix}'", "    outdir = './tmp'",
         f"    pseudo_dir = '{pseudo_dir}'", f"    disk_io = '{DFT['disk_io']}'", "    tprnfor = .true."]
    if tstress:
        L.append("    tstress = .true.")
    if calc == "relax":
        R = DFT["relax"]
        L += [f"    forc_conv_thr = {_fnum(R['forc_conv_thr'])}", f"    etot_conv_thr = {_fnum(R['etot_conv_thr'])}",
              f"    nstep = {R['nstep']}"]
    L += ["/", "&SYSTEM", "    ibrav = 0", f"    nat = {len(atoms)}", f"    ntyp = {len(present)}",
          f"    ecutwfc = {DFT['ecutwfc']}", f"    ecutrho = {DFT['ecutrho']}", f"    occupations = '{DFT['occupations']}'",
          f"    smearing = '{DFT['smearing']}'", f"    degauss = {DFT['degauss']}", f"    nspin = {DFT['nspin']}", "/",
          "&ELECTRONS", f"    conv_thr = {_fnum(DFT['conv_thr'])}", f"    mixing_mode = '{DFT['mixing_mode']}'",
          f"    mixing_beta = {DFT['mixing_beta']}", f"    electron_maxstep = {DFT['electron_maxstep']}",
          f"    diagonalization = '{DFT['diagonalization']}'", "/"]
    if calc == "relax":
        L += ["&IONS", f"    ion_dynamics = '{DFT['relax']['ion_dynamics']}'", "/"]
    L.append("ATOMIC_SPECIES")
    L += [f"  {e} {MASS[e]} {PP[e]}" for e in present]
    L.append("CELL_PARAMETERS angstrom")
    L += ["  " + "  ".join(f"{x:.10f}" for x in row) for row in cell]
    L.append("ATOMIC_POSITIONS crystal")
    L += [f"  {s} " + "  ".join(f"{x:.10f}" for x in f) for s, f in zip(syms, frac)]
    L += ["K_POINTS automatic", " ".join(str(int(x)) for x in k) + " 0 0 0", ""]
    return "\n".join(L)


def parse_pw_in(path) -> dict:
    """이 도구가 쓴 입력을 다시 읽는다 → 셀 (Å) · 원소 · 분수 좌표 · k · 키 (출력 결속 대조용)."""
    lines = Path(path).read_text().splitlines()
    keys = {}
    for ln in lines:
        m = re.match(r"^\s*([A-Za-z_]+)\s*=\s*(.+?)\s*$", ln)
        if m:
            keys[m.group(1).lower()] = m.group(2).strip().strip("'\"")
    i = next(j for j, ln in enumerate(lines) if ln.strip().startswith("CELL_PARAMETERS"))
    cell = np.array([[float(x) for x in lines[i + 1 + r].split()] for r in range(3)])
    j = next(n for n, ln in enumerate(lines) if ln.strip().startswith("ATOMIC_POSITIONS"))
    nat = int(keys["nat"])
    syms, frac = [], []
    for ln in lines[j + 1:j + 1 + nat]:
        t = ln.split()
        syms.append(t[0])
        frac.append([float(x) for x in t[1:4]])
    kk = next(n for n, ln in enumerate(lines) if ln.strip().startswith("K_POINTS"))
    k = [int(x) for x in lines[kk + 1].split()[:3]]
    return {"keys": keys, "cell": cell, "symbols": syms, "frac": np.array(frac), "k": k}


# ───────────────────────── 출력 읽기 ─────────────────────────
_RE_E = re.compile(r"^!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", re.M)
_RE_P = re.compile(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*(-?\d+\.?\d*)")
_RE_PP = re.compile(r"PseudoPot\.\s*#\s*\d+\s+for\s+(\w+)\s+read from file:\s*\n\s*(\S+)\s*\n\s*MD5 check sum:\s*([0-9a-fA-F]+)")


def _num(rx, txt, cast=float):
    m = re.search(rx, txt)
    return cast(m.group(1)) if m else None


def parse_pw_out(path) -> dict:
    """pw.x 출력 → 결속 · 판정에 쓰는 값 (못 찾은 것은 None — 0 으로 두지 않는다)."""
    p = Path(path)
    txt = p.read_text(errors="ignore")
    o = {"path": str(p), "sha256": _sha(p)}
    o["version"] = _num(r"Program PWSCF v\.(\S+) starts", txt, str)
    o["input_name"] = _num(r"Reading input from (\S+)", txt, str)
    o["nat"] = _num(r"number of atoms/cell\s*=\s*(\d+)", txt, int)
    o["nelec"] = _num(r"number of electrons\s*=\s*([\d.]+)", txt)
    o["ecutwfc"] = _num(r"kinetic-energy cutoff\s*=\s*([\d.]+)\s*Ry", txt)
    o["ecutrho"] = _num(r"charge density cutoff\s*=\s*([\d.]+)\s*Ry", txt)
    o["conv_thr"] = _num(r"scf convergence threshold\s*=\s*([\d.Ee+-]+)", txt)
    m = re.search(r"number of k points=\s*(\d+)\s+(\S+)\s+smearing, width \(Ry\)=\s*([\d.Ee+-]+)", txt)
    o["nk"], o["smearing"], o["degauss"] = (int(m.group(1)), m.group(2).lower(), float(m.group(3))) if m else (None, None, None)
    m = re.search(r"Exchange-correlation=\s*([^\n(]+)", txt)
    o["xc"] = m.group(1).split() if m else None
    o["pp"] = [{"el": a, "file": Path(b).name, "md5": c.lower()} for a, b, c in _RE_PP.findall(txt)]
    v = _num(r"unit-cell volume\s*=\s*([\d.]+)\s*\(a\.u\.\)\^3", txt)
    o["volume_A3"] = v * BOHR_A ** 3 if v is not None else None
    alat = _num(r"celldm\(1\)=\s*([\d.]+)", txt)
    o["alat_bohr"] = alat
    m = re.search(r"crystal axes: \(cart\. coord\. in units of alat\)\s*\n"
                  r"\s*a\(1\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)\s*\n"
                  r"\s*a\(2\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)\s*\n"
                  r"\s*a\(3\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)", txt)
    o["cell_A"] = (np.array([float(x) for x in m.groups()]).reshape(3, 3) * alat * BOHR_A).tolist() if (m and alat) else None
    # 처음 좌표 (alat 단위 · Cartesian) — 'site n.  atom  positions (alat units)' 블록
    pos = None
    k = txt.find("positions (alat units)")
    if k >= 0:
        rows = re.findall(r"^\s*\d+\s+([A-Za-z]+)\s+tau\(\s*\d+\)\s*=\s*\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)",
                          txt[k:k + 200 * max(o["nat"] or 1, 1)], re.M)
        if o["nat"] and len(rows) >= o["nat"] and alat:
            rows = rows[:o["nat"]]
            pos = {"symbols": [r[0] for r in rows],
                   "cart_A": (np.array([[float(x) for x in r[1:]] for r in rows]) * alat * BOHR_A).tolist()}
    o["initial"] = pos
    Es = [(mm.start(), float(mm.group(1))) for mm in _RE_E.finditer(txt)]
    o["n_scf"] = len(Es)
    o["E_Ry"] = Es[-1][1] if Es else None
    o["E_last_at"] = Es[-1][0] if Es else None
    o["scf_converged"] = "convergence has been achieved" in txt and "convergence NOT achieved" not in txt
    o["job_done"] = "JOB DONE" in txt
    o["forces_block"] = "Forces acting on atoms" in txt
    F = re.findall(r"atom\s+\d+\s+type\s+\d+\s+force\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", txt)
    o["max_force_eV_A"] = (float(np.max(np.linalg.norm(np.array(F[-(o['nat'] or len(F)):], float), axis=1))) * RYBOHR_EVA
                           if F else None)
    Ps = [(mm.start(), float(mm.group(1))) for mm in _RE_P.finditer(txt)]
    o["P_kbar"] = Ps[-1][1] if Ps else None
    o["P_at"] = Ps[-1][0] if Ps else None
    o["spin_polarized"] = ("SPIN UP" in txt) or ("Starting magnetic structure" in txt)
    m = re.search(r"bfgs converged in\s+(\d+)\s+scf cycles and\s+(\d+)\s+bfgs steps", txt)
    o["bfgs"] = {"scf_cycles": int(m.group(1)), "steps": int(m.group(2))} if m else None
    o["final_E_Ry"] = _num(r"Final energy\s+=\s+(-?\d+\.\d+)\s+Ry", txt)
    fin = None
    b, e = txt.rfind("Begin final coordinates"), txt.rfind("End final coordinates")
    if 0 <= b < e:
        blk = txt[b:e]
        m = re.search(r"ATOMIC_POSITIONS\s*\(?\s*(\w+)\s*\)?\s*\n", blk)
        if m:
            rows = re.findall(r"^\s*([A-Za-z]+)\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", blk[m.end():], re.M)
            fin = {"units": m.group(1).lower(), "symbols": [r[0] for r in rows],
                   "xyz": [[float(x) for x in r[1:]] for r in rows]}
    o["final"] = fin
    o["gpu"] = "GPU acceleration is ACTIVE" in txt
    m = re.search(r"PWSCF\s*:\s*(.+?)CPU\s+(.+?)WALL", txt)
    o["wall"] = m.group(2).strip() if m else None
    o["prefixes"] = sorted(set(re.findall(r"\./tmp/([A-Za-z0-9_.+-]+?)\.(?:save|bfgs)", txt)))
    return o


def out_problems(o, inp, *, stage, pp_md5, V0=None) -> list:
    """출력 하나가 그 입력 (같은 폴더의 scf.in) · 계획한 설정의 완료 결과인가 → 문제 목록 (빈 목록 = 통과)."""
    q = []
    if not o["job_done"]:
        q.append("JOB DONE 없음 (안 끝났다)")
    if o["E_Ry"] is None:
        q.append("'!' 총에너지 없음")
    if not o["scf_converged"]:
        q.append("SCF 수렴 아님 (convergence NOT achieved 또는 수렴 줄 없음)")
    if o["input_name"] != "scf.in":
        q.append(f"입력 이름 {o['input_name']} ≠ scf.in")
    if o["nat"] != len(inp["symbols"]) or o["nat"] != DFT["nat"]:
        q.append(f"원자 수 {o['nat']} ≠ {DFT['nat']}")
    for k in ("ecutwfc", "ecutrho"):
        if o[k] is None or abs(o[k] - DFT[k]) > TOL["ecut"]:
            q.append(f"{k} {o[k]} ≠ {DFT[k]}")
    if o["conv_thr"] is None or abs(o["conv_thr"] / DFT["conv_thr"] - 1) > TOL["conv_rel"]:
        q.append(f"conv_thr {o['conv_thr']} ≠ {DFT['conv_thr']}")
    if o["smearing"] != DFT["smearing"] or o["degauss"] is None or abs(o["degauss"] - DFT["degauss"]) > TOL["degauss"]:
        q.append(f"smearing {o['smearing']} · {o['degauss']} ≠ {DFT['smearing']} · {DFT['degauss']}")
    if o["xc"] is None or o["xc"][:4] != ["SLA", "PW", "PBX", "PBC"]:
        q.append(f"교환상관 {o['xc']} ≠ PBE (SLA PW PBX PBC)")
    if o["spin_polarized"]:
        q.append("스핀 분극 출력 (nspin 1 이어야 한다)")
    got = {d["el"]: d for d in o["pp"]}
    present = sorted(set(inp["symbols"]))
    if sorted(got) != present:
        q.append(f"유사포텐셜 원소 {sorted(got)} ≠ {present}")
    for el in present:
        d = got.get(el)
        if d and (d["file"] != PP[el] or d["md5"] != pp_md5.get(el)):
            q.append(f"유사포텐셜 {el}: {d['file']} · md5 {d['md5'][:8]} ≠ 계획 {PP[el]} · {str(pp_md5.get(el))[:8]}")
    # 셀 · 처음 좌표 — 이 잡의 입력과 같아야 한다 (다른 잡 출력 바꿔치기)
    cin = np.asarray(inp["cell"], float)
    if o["cell_A"] is None or np.abs(np.asarray(o["cell_A"]) - cin).max() > TOL["cell_A"]:
        q.append("출력의 셀 축이 입력 셀과 다르다")
    ini = o["initial"]
    if ini is None:
        q.append("출력의 처음 좌표 블록을 못 읽었다")
    else:
        if ini["symbols"] != list(inp["symbols"]):
            q.append("출력의 처음 원소 순서가 입력과 다르다")
        else:
            cart = np.asarray(inp["frac"], float) @ cin
            if np.abs(np.asarray(ini["cart_A"]) - cart).max() > TOL["pos_A"]:
                q.append("출력의 처음 좌표가 입력 좌표와 다르다 (다른 잡의 출력?)")
    if o["prefixes"] and o["prefixes"] != [inp["keys"].get("prefix")]:
        q.append(f"출력의 prefix {o['prefixes']} ≠ 입력 {inp['keys'].get('prefix')}")
    if stage in ("sp", "kprobe"):
        if not o["forces_block"]:
            q.append("힘 블록 없음")
    if stage == "relax":
        if o["bfgs"] is None:
            q.append("'bfgs converged' 없음 (nstep 소진 · 미수렴)")
        if o["final"] is None or len(o["final"]["symbols"]) != DFT["nat"]:
            q.append("최종 좌표 블록 없음 · 원자 수 다름")
        elif o["final"]["symbols"] != list(inp["symbols"]):
            q.append("최종 좌표의 원소 순서가 입력과 다르다")
        if o["final_E_Ry"] is None or o["E_Ry"] is None or abs(o["final_E_Ry"] - o["E_Ry"]) > TOL["E_final_Ry"]:
            q.append(f"Final energy {o['final_E_Ry']} ≠ 마지막 '!' {o['E_Ry']}")
        if o["P_kbar"] is None or o["E_last_at"] is None or o["P_at"] < o["E_last_at"]:
            q.append("응력 (P) 이 마지막 SCF 뒤에 없다 (tstress · 끝 기하의 압력이 아니다)")
        if V0 is None or o["volume_A3"] is None or abs(o["volume_A3"] - V0) > TOL["V_A3"]:
            q.append(f"부피 {o['volume_A3']} Å³ ≠ 기준 셀 V₀ {V0}")
    return q


def read_stage_outputs(plan_dir, jobs, *, stage, pp_md5, V0=None):
    """단계 잡 전부 → {잡: 출력 dict} · 누락 · 실패를 모아 멈춘다 (누락 ≠ 실패 · 둘 다 판정에 안 넣는다)."""
    plan_dir = Path(plan_dir)
    outs, missing, bad = {}, [], []
    for j in jobs:
        d = plan_dir / stage / j["job"]
        fin = d / "scf.in"
        if not fin.is_file() or _sha(fin) != j["input_sha256"]:
            bad.append(f"{j['job']}: 입력 scf.in 이 계획 뒤 바뀌었다 · 없다 (sha256)")
            continue
        fout = d / "scf.out"
        if not fout.is_file():
            missing.append(j["job"])
            continue
        o = parse_pw_out(fout)
        q = out_problems(o, parse_pw_in(fin), stage=stage, pp_md5=pp_md5, V0=V0)
        if q:
            bad.append(f"{j['job']}: " + " · ".join(q[:3]))
        outs[j["job"]] = o
    if missing:
        raise SystemExit(f"⛔ {stage} 출력 누락 {len(missing)} 건 ({missing}) — 누락은 실패가 아니다 · 다 돌린 뒤 판독한다")
    if bad:
        raise SystemExit(f"⛔ {stage} 출력 결속 · 검사 실패 {len(bad)} 건 — 판독하지 않는다 (같은 설정으로 다시 돌린 뒤):\n  "
                         + "\n  ".join(bad))
    nks = {o["nk"] for o in outs.values()}
    vers = {o["version"] for o in outs.values()}
    if len(nks) != 1:
        raise SystemExit(f"⛔ {stage} 출력의 k 점 수가 갈린다 {sorted(nks, key=str)} — 같은 k 격자 · 대칭이 아니다")
    if len(vers) != 1:
        raise SystemExit(f"⛔ {stage} 출력의 PWSCF 판이 갈린다 {sorted(vers, key=str)}")
    return outs


# ───────────────────────── 8 단계 다시 결속 · 고르기 ─────────────────────────
def stage8(RD, verdict, receipt, results, readout):
    """판 고정 판독기로 8 단계 본 판독을 다시 내고 본 판독 파일과 몸통 대조 → (본 판독, 가족별 성공 목록, 원 기록, 결과 폴더)."""
    A100 = RD.anneal_readout(verdict, receipt, results)
    got = json.loads(Path(readout).read_text(encoding="utf-8"))
    if RD._core(got) != RD._core(A100):
        raise SystemExit("⛔ 본 판독 파일이 같은 입력에서 다시 낸 본 판독과 다르다 — 바뀐 판독은 쓰지 않는다")
    if A100.get("hold_reasons"):
        raise SystemExit(f"⛔ 8 단계 본 판독이 보류다 ({A100['hold_reasons'][:2]}) — DFT 대상을 고르지 않는다")
    plan = RD.verify_screen_verdict(verdict)["plan_anneal"]
    R = RD.load_records(results)
    raw_b = Path(R["path"]).read_bytes()
    if hashlib.sha256(raw_b).hexdigest() != R["sha256"]:
        raise SystemExit("⛔ 8 단계 결과 파일이 판독기 결속 뒤 바뀌었다 (sha256)")
    raw = {r.get("name"): r for r in json.loads(raw_b).get("results", [])}
    succ = {}
    for F in FAM:
        S = []
        for e in plan:
            if e["family"] != F or not e.get("start"):
                continue
            r = R["records"].get(e["name"])
            if r is not None and r["ok"]:
                S.append({"name": e["name"], "rank": int(e["rank"]), "E": float(r["E"])})
        S.sort(key=lambda x: (x["E"], x["rank"]))
        fa = (A100.get("families") or {}).get(F) or {}
        if not S or (fa.get("min") or {}).get("name") != S[0]["name"] or fa.get("n_success") != len(S):
            raise SystemExit(f"⛔ {F}: 성공 목록 (최저 {S[0]['name'] if S else None} · {len(S)}) 이 본 판독 "
                             f"({(fa.get('min') or {}).get('name')} · {fa.get('n_success')}) 과 다르다 — 고르지 않는다")
        succ[F] = S
    return A100, succ, raw, Path(R["path"]).parent


def select_sp(succ, n=None):
    """가족마다 UMA 어닐 최저 n (기본 2) — 모자라면 멈춘다."""
    n = DFT["n_per_family"] if n is None else n
    out = []
    for F in FAM:
        if len(succ[F]) < n:
            raise SystemExit(f"⛔ {F}: 성공 {len(succ[F])} < {n} — 가족마다 최저 {n} 을 고를 수 없다")
        for i, s in enumerate(succ[F][:n], 1):
            out.append({"family": F, "i": i, **s})
    return out


def _struct(RD, raw, res_dir, name):
    from ase.io import read
    r = raw.get(name) or {}
    e = (r.get("outputs") or {}).get("post_relax") or {}
    p = (Path(res_dir) / e.get("rel", "")).resolve()
    if not e.get("sha256") or not p.is_file() or _sha(p) != e["sha256"]:
        raise SystemExit(f"⛔ {name}: post_relax 구조 파일이 결과 기록과 결속되지 않는다")
    a = read(str(p))
    comp = {}
    for s in a.get_chemical_symbols():
        comp[s] = comp.get(s, 0) + 1
    if dict(sorted(comp.items())) != DFT["composition"]:
        raise SystemExit(f"⛔ {name}: 조성 {comp} ≠ {DFT['composition']}")
    if not (np.isfinite(a.positions).all() and np.isfinite(a.cell.array).all() and abs(a.get_volume()) > 1.0):
        raise SystemExit(f"⛔ {name}: 기하가 유한 · 정칙이 아니다")
    return p, a


def coord_record(RD, atoms) -> dict:
    """기록 (판정 아님) — O 끝 꼴 (판 고정 판독기) · B · P 배위 (거리 문턱 B_CUT_A · P_CUT_A)."""
    from ase.geometry import get_distances
    sy = np.array(atoms.get_chemical_symbols())
    rec = {"end_motif": RD.end_motif(atoms)}
    for X, cut in (("B", B_CUT_A), ("P", P_CUT_A)):
        cen = np.nonzero(sy == X)[0]
        rows = []
        for i in cen:
            row = {}
            for Y, r in cut.items():
                idx = np.nonzero(sy == Y)[0]
                _, d = get_distances(atoms.positions[i][None], atoms.positions[idx], cell=atoms.cell, pbc=atoms.pbc)
                row[Y] = int((d[0] < r).sum())
            rows.append(row)
        rec[f"{X}_coordination"] = rows
    rec["P_not_4"] = sum(1 for r in rec["P_coordination"] if sum(r.values()) != 4)
    return rec


def _job(prefix, s):
    return f"{prefix}_{TAG[s['family']]}_{s['i']}_cfg{int(s['rank']):04d}" if "i" in s else \
        f"{prefix}_{TAG[s['family']]}_cfg{int(s['rank']):04d}"


# ───────────────────────── 기준 셀 · 이완 입력 ─────────────────────────
def reference_cell(host_path):
    """1×2×5 = modelc_V0_k663 × (1,2,1) 의 모양 (cellpar) 을 V₀ 로 등방 스케일 (카드 9_DFT ③) → (셀, 기록)."""
    from ase.io import read
    from ase.geometry import cellpar_to_cell
    hp = Path(host_path)
    if _sha(hp) != DFT["ref_cell"]["host_sha256"]:
        raise SystemExit(f"⛔ host {hp.name} sha256 이 카드의 modelc_V0_k663.xyz 가 아니다")
    h = read(str(hp)).repeat(tuple(DFT["ref_cell"]["supercell"]))
    par = np.array(h.cell.cellpar(), float)
    V0 = DFT["ref_cell"]["V0_A3"]
    s = (V0 / h.get_volume()) ** (1.0 / 3.0)
    par[:3] *= s
    cell = cellpar_to_cell(par)
    return np.asarray(cell, float), {"host_sha256": _sha(hp), "host_volume_A3": float(h.get_volume()),
                                     "scale": float(s), "cellpar": par.tolist(), "V0_A3": V0,
                                     "volume_A3": float(abs(np.linalg.det(cell)))}


def map_to_cell(atoms, cell):
    from ase import Atoms
    return Atoms(atoms.get_chemical_symbols(), scaled_positions=atoms.get_scaled_positions(wrap=False),
                 cell=cell, pbc=True)


# ───────────────────────── 판정 조각 ─────────────────────────
def family_order(E: dict):
    """{가족: E} → (순서, 승자–차저 차, 판정 dict)."""
    order = sorted(FAM, key=lambda F: (E[F], F))
    gap = E[order[1]] - E[order[0]]
    return order, gap, {"lowest": order[0], "gap_ge_margin": gap >= DFT["margin_dft_eV"] - 1e-12,
                        "margin": DFT["margin_dft_eV"]}


def kprobe_trigger(E1: dict, E2: dict) -> list:
    """가족 대표 셋의 두 k 격자 에너지 → 발동 사유 목록 (빈 목록 = 발동 안 함) — 세 가족 쌍 모두 본다 (개정 5 [제안])."""
    why = []
    o1, _, _ = family_order(E1)
    o2, _, _ = family_order(E2)
    if o1 != o2:
        why.append(f"가족 순서 바뀜 {o1} → {o2}")
    m = DFT["margin_dft_eV"]
    for F, G in itertools.combinations(FAM, 2):
        d1, d2 = E1[G] - E1[F], E2[G] - E2[F]
        if abs(d2 - d1) > DFT["kprobe_shift_eV"] + 1e-12:
            why.append(f"{G}−{F} 차 {d1:+.3f} → {d2:+.3f} (변화 {d2 - d1:+.3f} > {DFT['kprobe_shift_eV']})")
        if (abs(d1) >= m - 1e-12) != (abs(d2) >= m - 1e-12):
            why.append(f"{G}−{F} 차가 {m} 경계를 건넘 ({d1:+.3f} → {d2:+.3f})")
    return why


def stage10(succ, eos, raw, res_dir):
    """10 단계 고르기 — DFT 승자–차저 ≥ 0.10 이면 이긴 가족의 UMA 어닐 최저 셋 · 아니면 가족마다 UMA 어닐 최저 하나."""
    dec = eos["baseline_decision"]
    if dec["gap_ge_margin"]:
        F = dec["lowest"]
        n = DFT["n_stability_winner"]
        if len(succ[F]) < n:
            raise SystemExit(f"⛔ {F}: 성공 {len(succ[F])} < {n} — 안정성 대상 셋을 고를 수 없다")
        pick = [{"family": F, **s} for s in succ[F][:n]]
        rule = f"DFT 승자 {F} (차저와 {eos['baseline_gap']:.3f} ≥ {DFT['margin_dft_eV']}) → 그 가족의 UMA 어닐 최저 {n}"
    else:
        pick = [{"family": F, **succ[F][0]} for F in FAM]
        rule = f"DFT 로 못 가른다 (승자–차저 {eos['baseline_gap']:.3f} < {DFT['margin_dft_eV']}) → 가족마다 UMA 어닐 최저 하나"
    for s in pick:
        e = (raw.get(s["name"]) or {}).get("outputs", {}).get("post_relax") or {}
        s["post_relax"] = {"rel": e.get("rel"), "sha256": e.get("sha256")}
    return {"rule": rule, "stability_targets": pick}


# ───────────────────────── 명령 ─────────────────────────
def prepare(RD, verdict, receipt, results, readout, pseudo_dir, out_dir, k_main=None, after_kprobe=None):
    out_dir = Path(out_dir)
    k_main = list(k_main or DFT["k_main"])
    if k_main not in (DFT["k_main"], DFT["k_probe"]):
        raise SystemExit(f"⛔ k_main {k_main} — {DFT['k_main']} (기본) 또는 {DFT['k_probe']} (탐침 발동 뒤) 만")
    kp = None
    if k_main == DFT["k_probe"]:
        if not after_kprobe:
            raise SystemExit("⛔ k_main 4×2×1 은 탐침 발동 판정 (--after_kprobe) 이 있을 때만 — 결과 전 규칙 (DU P1-5)")
        kp = _load(after_kprobe, KIND_KP)
        if not kp.get("triggered"):
            raise SystemExit("⛔ --after_kprobe 판정이 발동이 아니다 — 4×2×1 다시 계산의 근거가 없다")
        _rebind_kp(RD, after_kprobe, None)            # 발동 판정을 출력에서 다시 낸다 (손댄 '발동' 은 근거가 아니다)
    if (out_dir / "dft_plan.json").exists():
        raise SystemExit(f"⛔ {out_dir}/dft_plan.json 가 이미 있다 — 덮지 않는다 (새 폴더)")
    A100, succ, raw, res_dir = stage8(RD, verdict, receipt, results, readout)
    if kp is not None:
        ins = (kp.get("stage8") or {})
        if ins.get("anneal_results_sha256") != _sha(results):
            raise SystemExit("⛔ --after_kprobe 판정이 다른 8 단계 결과에서 나왔다")
    ps = pseudo_record(pseudo_dir)
    sel = select_sp(succ)
    jobs = []
    for s in sel:
        p, a = _struct(RD, raw, res_dir, s["name"])
        job = _job("sp", s)
        fin = write_pw_input(out_dir / "sp" / job / "scf.in", a, prefix=job, calc="scf", k=k_main, pseudo_dir=ps["dir"])
        jobs.append({"job": job, "family": s["family"], "i": s["i"], "name": s["name"], "rank": s["rank"],
                     "E_uma_eV": s["E"], "structure": _entry(p, out_dir), "input_sha256": _sha(fin),
                     "uma_record": coord_record(RD, a)})
    plan = {"kind": KIND_PLAN, "card": "db/properties/b2o3_bo_placement_estimand_2026_11_09.json#개정_1 9_DFT · 개정_5",
            "tools": _tools(RD),
            "inputs": {"screen_verdict": _entry(verdict, out_dir), "pilot_receipt": _entry(receipt, out_dir),
                       "anneal_results": _entry(results, out_dir), "anneal_readout": _entry(readout, out_dir)},
            "after_kprobe": _entry(after_kprobe, out_dir) if after_kprobe else None,
            "stage8": {"order": A100.get("order"), "winner": A100.get("winner"), "decision": A100.get("decision"),
                       "gap_eV": A100.get("winner_runner_up_gap_eV")},
            "contract": DFT, "pseudo": ps, "k_main": k_main, "jobs_sp": jobs}
    _dump(plan, out_dir / "dft_plan.json")
    return plan


def _rebind_plan(RD, plan_path):
    """계획을 다시 결속 — 도구 · 판독기 같음 · 묶인 입력 sha · 8 단계 다시 내기 · 고르기 다시 내서 계획과 같음."""
    pp = Path(plan_path).resolve()
    plan = _load(pp, KIND_PLAN)
    _same_tools(RD, plan, "계획")
    base = pp.parent
    if plan.get("contract") != json.loads(json.dumps(DFT)):
        raise SystemExit("⛔ 계획의 계약 (contract) 이 이 도구의 값과 다르다")
    ins = {k: _bound(plan["inputs"].get(k), base, k) for k in ("screen_verdict", "pilot_receipt", "anneal_results",
                                                               "anneal_readout")}
    A100, succ, raw, res_dir = stage8(RD, ins["screen_verdict"], ins["pilot_receipt"], ins["anneal_results"],
                                      ins["anneal_readout"])
    sel = select_sp(succ)
    want = [(s["family"], s["i"], s["name"]) for s in sel]
    got = [(j["family"], j["i"], j["name"]) for j in plan["jobs_sp"]]
    if want != got:
        raise SystemExit(f"⛔ 계획의 단일점 대상이 다시 고른 것과 다르다 ({got} ≠ {want}) — 손댄 계획은 쓰지 않는다")
    exp = _expected_sp(plan, base)
    for j in plan["jobs_sp"]:
        if _text_sha(exp[j["job"]]) != j["input_sha256"]:
            raise SystemExit(f"⛔ {j['job']}: 계획의 입력 sha256 이 묶인 구조에서 다시 만든 입력과 다르다")
    return plan, base, A100, succ, raw, res_dir


def _pp_md5(plan):
    return {el: d["md5"] for el, d in plan["pseudo"]["files"].items()}


def _expected_sp(plan, base):
    """계획의 단일점 입력을 묶인 구조에서 다시 만든다 → {잡: 텍스트}."""
    from ase.io import read
    out = {}
    for j in plan["jobs_sp"]:
        a = read(str(_bound(j["structure"], base, f"{j['job']} 구조")))
        out[j["job"]] = pw_input_text(a, prefix=j["job"], calc="scf", k=plan["k_main"], pseudo_dir=plan["pseudo"]["dir"])
    return out


def _expected_kprobe(plan, base, reps):
    """가족 대표 (단일점 최저) 셋 → 탐침 잡 · 입력 텍스트 (같은 구조 · k_probe)."""
    from ase.io import read
    jobs, texts = [], {}
    for F in FAM:
        j = reps[F]
        a = read(str(_bound(j["structure"], base, f"{j['job']} 구조")))
        job = f"kp_{TAG[F]}_cfg{int(j['rank']):04d}"
        t = pw_input_text(a, prefix=job, calc="scf", k=DFT["k_probe"], pseudo_dir=plan["pseudo"]["dir"])
        jobs.append({"job": job, "family": F, "name": j["name"], "rank": j["rank"], "sp_job": j["job"],
                     "structure": j["structure"], "input_sha256": _text_sha(t)})
        texts[job] = t
    return jobs, texts


def _expected_relax(plan, base, reps, host):
    """가족 대표 셋 → 기준 셀 (host 모양 · V₀) · 분수 좌표 그대로 · 이온 이완 잡 · 입력 텍스트."""
    from ase.io import read
    cell, cell_rec = reference_cell(host)
    jobs, texts = [], {}
    for F in FAM:
        j = reps[F]
        a = read(str(_bound(j["structure"], base, f"{j['job']} 구조")))
        job = f"rx_{TAG[F]}_cfg{int(j['rank']):04d}"
        t = pw_input_text(map_to_cell(a, cell), prefix=job, calc="relax", k=plan["k_main"],
                          pseudo_dir=plan["pseudo"]["dir"], tstress=True)
        jobs.append({"job": job, "family": F, "name": j["name"], "rank": j["rank"], "parent_sp_job": j["job"],
                     "structure": j["structure"], "input_sha256": _text_sha(t)})
        texts[job] = t
    return jobs, texts, cell_rec


def _write_jobs(base, stage, texts):
    for job, t in texts.items():
        d = Path(base) / stage / job
        if (d / "scf.in").exists():
            raise SystemExit(f"⛔ {d}/scf.in 가 이미 있다 — 덮지 않는다")
        d.mkdir(parents=True, exist_ok=True)
        (d / "scf.in").write_text(t)


def _same_jobs(recorded, expected, what):
    key = lambda js: [(j["job"], j["family"], j["name"], j["input_sha256"]) for j in js]
    if key(recorded or []) != key(expected):
        raise SystemExit(f"⛔ {what} 잡 기록이 다시 만든 것과 다르다 (대상 · 입력 sha256) — 손댄 판정은 쓰지 않는다")


def _sp_rows(plan, base, outs):
    rows = []
    for j in plan["jobs_sp"]:
        o = outs[j["job"]]
        rows.append({"job": j["job"], "family": j["family"], "i": j["i"], "name": j["name"], "rank": j["rank"],
                     "E_eV": o["E_Ry"] * RY_EV, "max_force_eV_A": o["max_force_eV_A"], "nk": o["nk"],
                     "output": _entry(o["path"], base), "wall": o["wall"], "gpu": o["gpu"]})
    rep = {}
    for F in FAM:
        rr = sorted((r for r in rows if r["family"] == F), key=lambda r: (r["E_eV"], r["i"]))
        rep[F] = rr[0]
    return rows, rep


def read_sp(RD, plan_path, out, host=None):
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    plan, base, A100, succ, raw, res_dir = _rebind_plan(RD, plan_path)
    outs = read_stage_outputs(base, plan["jobs_sp"], stage="sp", pp_md5=_pp_md5(plan))
    rows, rep = _sp_rows(plan, base, outs)
    E = {F: rep[F]["E_eV"] for F in FAM}
    order, gap, dec = family_order(E)
    uma = plan["stage8"]["order"]
    v = {"kind": KIND_SP, "tools": _tools(RD), "plan": _entry(plan_path, Path(out).resolve().parent),
         "k_main": plan["k_main"], "rows": rows, "representatives": {F: rep[F]["job"] for F in FAM},
         "order": order, "gap_eV": gap, "decision_sp": dec,
         "G5": {"uma_order": uma, "same_order": order == uma,
                "⚠": "단일점 (UMA 이완 기하) 순서 — 기록 · 'DFT 순위' 가 아니다 (판정은 이온 이완 뒤 · 절차 9_DFT_확인 ⛔)"},
         "sentence_sp": ("DFT 단일점 (UMA 이완 기하) 에서도 같은 순서였다." if order == uma else
                         "DFT 단일점 (UMA 이완 기하) 에서는 다른 순서였다.") +
                        ("" if dec["gap_ge_margin"] else " (단일점 최저–차점 차 < 0.10 — DFT 단일점으로는 가를 수 없다)")}
    reps = {F: next(x for x in plan["jobs_sp"] if x["job"] == rep[F]["job"]) for F in FAM}
    if plan["k_main"] == DFT["k_main"]:
        v["jobs_kprobe"], texts = _expected_kprobe(plan, base, reps)
        _write_jobs(base, "kprobe", texts)
        v["next"] = "run_force_check_scf.sh <계획 폴더>/kprobe → read_kprobe"
    else:
        if host is None:
            raise SystemExit("⛔ k_main 4×2×1 (탐침 발동 뒤) 판은 read_sp 가 이완 입력을 쓴다 — --host 가 필요하다")
        v["jobs_relax"], texts, v["reference_cell"] = _expected_relax(plan, base, reps, host)
        _write_jobs(base, "relax", texts)
        v["next"] = "run_force_check_scf.sh <계획 폴더>/relax → read_relax --prev <이 파일>"
    _dump(v, out)
    return v


def _rebind_sp(RD, sp_path, host=None):
    """단일점 판정을 다시 결속 — 계획 · 8 단계 다시 · 단일점 출력 다시 읽어 행 · 대표 · 순서가 같은지 · 다음 잡 입력을 다시 만들어 대조."""
    sp_path = Path(sp_path).resolve()
    v = _load(sp_path, KIND_SP)
    _same_tools(RD, v, "단일점 판정")
    plan_path = _bound(v["plan"], sp_path.parent, "계획")
    plan, base, A100, succ, raw, res_dir = _rebind_plan(RD, plan_path)
    outs = read_stage_outputs(base, plan["jobs_sp"], stage="sp", pp_md5=_pp_md5(plan))
    rows, rep = _sp_rows(plan, base, outs)
    if json.loads(json.dumps(rows, default=str)) != v["rows"] or v["representatives"] != {F: rep[F]["job"] for F in FAM}:
        raise SystemExit("⛔ 단일점 판정의 행 · 대표가 출력에서 다시 낸 것과 다르다 — 바뀐 판정은 쓰지 않는다")
    reps = {F: next(x for x in plan["jobs_sp"] if x["job"] == rep[F]["job"]) for F in FAM}
    if plan["k_main"] == DFT["k_main"]:
        _same_jobs(v.get("jobs_kprobe"), _expected_kprobe(plan, base, reps)[0], "탐침")
    else:
        if host is None:
            raise SystemExit("⛔ k_main 4×2×1 판의 이완 대조에는 --host 가 필요하다")
        jobs, _, crec = _expected_relax(plan, base, reps, host)
        _same_jobs(v.get("jobs_relax"), jobs, "이완")
        if v.get("reference_cell") != json.loads(json.dumps(crec)):
            raise SystemExit("⛔ 단일점 판정의 기준 셀 기록이 다시 만든 것과 다르다")
    return v, plan, base, A100, succ, raw, res_dir, reps


def _kprobe_core(v, plan, base):
    outs = read_stage_outputs(base, v["jobs_kprobe"], stage="kprobe", pp_md5=_pp_md5(plan))
    E1 = {F: next(r["E_eV"] for r in v["rows"] if r["job"] == v["representatives"][F]) for F in FAM}
    E2 = {j["family"]: outs[j["job"]]["E_Ry"] * RY_EV for j in v["jobs_kprobe"]}
    why = kprobe_trigger(E1, E2)
    pairs = {f"{G}-{F}": {"k_main": E1[G] - E1[F], "k_probe": E2[G] - E2[F], "change": (E2[G] - E2[F]) - (E1[G] - E1[F])}
             for F, G in itertools.combinations(FAM, 2)}
    return outs, why, pairs


def read_kprobe(RD, sp_path, out, host):
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    v, plan, base, A100, succ, raw, res_dir, reps = _rebind_sp(RD, sp_path)
    if plan["k_main"] != DFT["k_main"]:
        raise SystemExit("⛔ 이 단일점 판정에는 k 탐침이 없다 (k_main 4×2×1 판) — read_relax 로 간다")
    outs, why, pairs = _kprobe_core(v, plan, base)
    kv = {"kind": KIND_KP, "tools": _tools(RD), "sp_verdict": _entry(sp_path, Path(out).resolve().parent),
          "stage8": {"anneal_results_sha256": plan["inputs"]["anneal_results"]["sha256"]},
          "k_main": plan["k_main"], "k_probe": DFT["k_probe"], "pairs": pairs,
          "outputs": {j["job"]: _entry(outs[j["job"]]["path"], base) for j in v["jobs_kprobe"]},
          "nk": {"k_main": v["rows"][0]["nk"], "k_probe": next(iter(outs.values()))["nk"]},
          "triggered": bool(why), "why": why}
    if why:
        kv["next"] = ("⛔ 발동 — 6 단일점을 4×2×1 로 다시 (새 폴더: prepare --k_main 4 2 1 --after_kprobe <이 파일>) · "
                      "안 할 거면 사용자 명시 결정으로 닫는다 (결정 원장 · 이유 · 한계)")
    else:
        kv["jobs_relax"], texts, kv["reference_cell"] = _expected_relax(plan, base, reps, host)
        _write_jobs(base, "relax", texts)
        kv["next"] = "run_force_check_scf.sh <계획 폴더>/relax → read_relax --prev <이 파일>"
    _dump(kv, out)
    return kv


def _rebind_kp(RD, kp_path, host):
    """탐침 판정을 다시 결속 — 단일점 사슬 · 탐침 출력 다시 읽어 발동 판정 · 쌍 · (발동 안 했으면) 이완 잡 입력을 다시 만들어 대조."""
    kp_path = Path(kp_path).resolve()
    kv = _load(kp_path, KIND_KP)
    _same_tools(RD, kv, "탐침 판정")
    v, plan, base, A100, succ, raw, res_dir, reps = _rebind_sp(RD, _bound(kv["sp_verdict"], kp_path.parent, "단일점 판정"))
    outs, why, pairs = _kprobe_core(v, plan, base)
    if bool(why) != bool(kv.get("triggered")) or why != kv.get("why") or json.loads(json.dumps(pairs)) != kv.get("pairs"):
        raise SystemExit("⛔ 탐침 판정이 출력에서 다시 낸 발동 판정과 다르다 — 바뀐 판정은 쓰지 않는다")
    if not why:
        jobs, _, crec = _expected_relax(plan, base, reps, host)
        _same_jobs(kv.get("jobs_relax"), jobs, "이완")
        if kv.get("reference_cell") != json.loads(json.dumps(crec)):
            raise SystemExit("⛔ 탐침 판정의 기준 셀 기록이 다시 만든 것과 다르다")
    return kv, v, plan, base, A100, succ, raw, res_dir


def read_relax(RD, prev_path, out, host):
    from ase import Atoms
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    prev_path = Path(prev_path).resolve()
    kind = json.loads(prev_path.read_text(encoding="utf-8")).get("kind")
    if kind == KIND_KP:
        prev, sp_v, plan, base, A100, succ, raw, res_dir = _rebind_kp(RD, prev_path, host)
        if prev.get("triggered"):
            raise SystemExit("⛔ 탐침이 발동했다 — 이 이완은 판독하지 않는다 (4×2×1 판으로)")
    elif kind == KIND_SP:
        sp_v, plan, base, A100, succ, raw, res_dir, _ = _rebind_sp(RD, prev_path, host)
        prev = sp_v
        if plan["k_main"] != DFT["k_probe"]:
            raise SystemExit("⛔ k_main 3×2×1 판의 이완은 탐침 판정 (read_kprobe) 뒤에만 판독한다")
    else:
        raise SystemExit(f"⛔ {prev_path.name} 는 탐침 · 단일점 판정이 아니다 ({kind})")
    jobs = prev["jobs_relax"]
    cell_rec = prev["reference_cell"]
    V0 = DFT["ref_cell"]["V0_A3"]
    outs = read_stage_outputs(base, jobs, stage="relax", pp_md5=_pp_md5(plan), V0=V0)
    fam, rows, relaxed = {}, [], {}
    for j in jobs:
        o = outs[j["job"]]
        inp = parse_pw_in(base / "relax" / j["job"] / "scf.in")
        fin = o["final"]
        if fin["units"] != "crystal":
            raise SystemExit(f"⛔ {j['job']}: 최종 좌표 단위 {fin['units']} ≠ crystal")
        a = Atoms(fin["symbols"], scaled_positions=np.array(fin["xyz"]), cell=inp["cell"], pbc=True)
        rp = write_relaxed(base / "relaxed" / f"{j['job']}.xyz", a)
        relaxed[j["family"]] = {"job": j["job"], "file": _entry(rp, base), "parent_structure": j["structure"],
                                "parent_sp_job": j["parent_sp_job"], "record": coord_record(RD, a)}
        E, P, V = o["E_Ry"] * RY_EV, o["P_kbar"] / 10.0, o["volume_A3"]
        fam[j["family"]] = (E, P, V)
        rows.append({"job": j["job"], "family": j["family"], "name": j["name"], "E_eV": E, "P_GPa": P, "V_A3": V,
                     "bfgs": o["bfgs"], "output": _entry(o["path"], base), "wall": o["wall"]})
    eos = RD.eos_robust(fam)
    if eos["baseline_order"] != family_order({F: fam[F][0] for F in FAM})[0]:
        raise SystemExit("⛔ 판 고정 eos_robust 의 기준 순서가 이 도구의 순서와 다르다")
    gaps = [c["gap"] for c in eos["corners"]]
    rv = {"kind": KIND_RX, "tools": _tools(RD), "prev": _entry(prev_path, Path(out).resolve().parent),
          "k_main": plan["k_main"], "reference_cell": cell_rec, "rows": rows,
          "eos_input": {F: {"E_eV": fam[F][0], "P_GPa": fam[F][1], "V_A3": fam[F][2],
                            "output": next(r["output"] for r in rows if r["family"] == F)} for F in FAM},
          "eos": eos, "corrected_gap_range_eV": [min(gaps), max(gaps)], "relaxed": relaxed,
          "electronic_targets": [{"family": F, **relaxed[F]["file"], "parent_structure": relaxed[F]["parent_structure"]}
                                 for F in FAM]}
    if eos["skip_eos"]:
        d = eos["baseline_decision"]
        rv["decision"] = (f"DFT 이온 이완 (고정 기준 셀 · 보정 전) 최저 {d['lowest']} · 승자–차저 {eos['baseline_gap']:.3f} "
                          + ("≥" if d["gap_ge_margin"] else "<") + f" {d['margin']} — 압력 보정 범위 전체에서 순서 · 판정 그대로 (EOS 생략)")
        rv["stage10"] = stage10(succ, eos, raw, res_dir)
    else:
        why = [f"{F}: |P| {abs(fam[F][1]):.2f} > {DFT['P_max_GPa']} GPa" for F in FAM if abs(fam[F][1]) > DFT["P_max_GPa"]]
        if not eos["robust_independent_B"]:
            why.append("B 조합 중 순서 · 0.10 판정이 바뀌는 것이 있다")
        rv["decision"] = "EOS 필요 — " + " · ".join(why) + " (고르기 안 함 · 그 셀만 EOS — 다음 판)"
        rv["stage10"] = None
    _dump(rv, out)
    return rv


def write_relaxed(path, atoms) -> Path:
    from ase.io import write
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    write(str(path), atoms, format="extxyz")
    return path


# ───────────────────────── selftest ─────────────────────────
def _fake_out(inp_path, *, E_list, stage="sp", nk=4, pp_md5=None, ecut=52.0, conv="1.0E-08", smear="Gaussian",
              width="0.0100", xc="SLA  PW   PBX  PBC", job_done=True, not_conv=False, spin=False, shift_pos=0.0,
              P_kbar=None, P_before_last=False, bfgs=True, final_E=None, final=True, version="7.4.1",
              input_name="scf.in", vol_override=None, drop_forces=False, prefix=None, final_symbols=None):
    """이 도구가 읽는 줄만 QE 7.4.1 꼴로 흉내 낸 출력 (실제 출력 줄 모양은 db/raw/li2s_neb_cellconv_2026_10_09 로 맞췄다)."""
    inp = parse_pw_in(inp_path)
    cell = inp["cell"]
    alat = float(np.linalg.norm(cell[0])) / BOHR_A
    cart = inp["frac"] @ cell
    vol = (vol_override if vol_override is not None else abs(np.linalg.det(cell))) / BOHR_A ** 3
    pre = prefix or inp["keys"]["prefix"]
    L = [f"     Program PWSCF v.{version} starts on  9Oct2026 at 23:50:33 ", "",
         f"     Reading input from {input_name}", "",
         f"     lattice parameter (alat)  =      {alat:.4f}  a.u.",
         f"     unit-cell volume          =    {vol:.4f} (a.u.)^3",
         f"     number of atoms/cell      =           {len(inp['symbols'])}",
         "     number of electrons       =       596.00",
         f"     kinetic-energy cutoff     =      {ecut:.4f}  Ry",
         f"     charge density cutoff     =     {DFT['ecutrho']:.4f}  Ry",
         f"     scf convergence threshold =      {conv}",
         f"     Exchange-correlation=  {xc}", "                           (   1   4   3   4   0   0   0)", "",
         "     GPU acceleration is ACTIVE.  1 visible GPUs per MPI rank", "",
         f"     celldm(1)=  {alat:.6f}  celldm(2)=   0.000000  celldm(3)=   0.000000", "",
         "     crystal axes: (cart. coord. in units of alat)"]
    for n, row in enumerate(cell, 1):
        r = row / (alat * BOHR_A)
        L.append(f"               a({n}) = (  {r[0]:.6f}  {r[1]:.6f}  {r[2]:.6f} )  ")
    L.append("")
    for n, el in enumerate([e for e in SPECIES if e in set(inp["symbols"])], 1):
        L += [f"     PseudoPot. # {n} for {el:<2} read from file:", f"     /data/work/pseudo/{PP[el]}",
              f"     MD5 check sum: {(pp_md5 or {}).get(el, '0' * 32)}", "     Pseudo is Ultrasoft, Zval =  3.0", ""]
    if spin:
        L.append("     Starting magnetic structure ")
    L += ["   Cartesian axes", "", "     site n.     atom                  positions (alat units)"]
    for n, (s, x) in enumerate(zip(inp["symbols"], cart), 1):
        t = (x + shift_pos) / (alat * BOHR_A)
        L.append(f"        {n}           {s}  tau(   {n}) = (   {t[0]:.7f}   {t[1]:.7f}   {t[2]:.7f}  )")
    L += ["", f"     number of k points=     {nk}  {smear} smearing, width (Ry)=  {width}", ""]

    def scf_block(E, with_p):
        b = ["     convergence NOT achieved after 200 iterations: stopping" if not_conv else
             "     convergence has been achieved in  12 iterations", "",
             f"!    total energy              =    {E / RY_EV:.8f} Ry", ""]
        if not drop_forces:
            b += ["     Forces acting on atoms (cartesian axes, Ry/au):", ""]
            b += [f"     atom {n:4d} type  1   force =     0.00010000    0.00020000   -0.00030000"
                  for n in range(1, len(inp["symbols"]) + 1)]
            b += ["     Total force =     0.001144     Total SCF correction =     0.000012", ""]
        if with_p and P_kbar is not None:
            b += [f"          total   stress  (Ry/bohr**3)                   (kbar)     P=      {P_kbar:8.2f}",
                  "   0.00001392   0.00000588  -0.00001346            2.05        0.87       -1.98", ""]
        return b
    for n, E in enumerate(E_list):
        last = n == len(E_list) - 1
        L += scf_block(E, (last and not P_before_last) or (P_before_last and n == len(E_list) - 2))
    if stage == "relax":
        if bfgs:
            L += [f"     bfgs converged in  {len(E_list)} scf cycles and  {len(E_list) - 1} bfgs steps",
                  "     (criteria: energy <  1.0E-05 Ry, force <  1.0E-03 Ry/Bohr)", "",
                  "     End of BFGS Geometry Optimization", "",
                  f"     Final energy             =    {(final_E if final_E is not None else E_list[-1]) / RY_EV:.10f} Ry", "",
                  f"     File ./tmp/{pre}.bfgs deleted, as requested"]
        if final:
            syms = final_symbols or inp["symbols"]
            L += ["Begin final coordinates", "", "ATOMIC_POSITIONS (crystal)"]
            L += [f"{s}             {f[0]:.10f}        {f[1]:.10f}        {f[2]:.10f}" for s, f in zip(syms, inp["frac"])]
            L += ["End final coordinates", ""]
    L += [f"     Writing config-only to output data dir ./tmp/{pre}.save/", "",
          "     PWSCF        :   1h 2m CPU      1h 5m WALL", ""]
    if job_done:
        L.append("   JOB DONE.")
    return "\n".join(L) + "\n"


class _FakeRD:
    """selftest 용 — 판 고정 판독기의 eos_robust · end_motif · CONTRACT 는 진짜를 쓰고, 8 단계 결속만 가짜로."""

    def __init__(self, real, A100, plan, recs, results_path):
        self.real, self._A100, self._plan, self._recs, self._res = real, A100, plan, recs, Path(results_path)
        self.CONTRACT, self.FAM_ORDER = real.CONTRACT, real.FAM_ORDER
        self.eos_robust, self.end_motif, self._core = real.eos_robust, real.end_motif, real._core
        self.__dft_path__, self.__dft_sha256__ = real.__dft_path__, real.__dft_sha256__

    def anneal_readout(self, v, r, res, **k):
        return json.loads(json.dumps(self._A100))

    def verify_screen_verdict(self, v, *a, **k):
        return {"plan_anneal": self._plan}

    def load_records(self, res):
        return {"path": str(self._res.resolve()), "sha256": _sha(self._res), "records": self._recs}


def _selftest() -> int:
    import tempfile
    from ase import Atoms
    from ase.io import read, write
    ok = [0, 0]

    def chk(c, m):
        ok[0] += 1
        ok[1] += bool(c)
        print(("  ✓ " if c else "  ✗ ") + m)

    def refuses(kw, f, *a, **k):
        try:
            f(*a, **k)
        except SystemExit as ex:
            return kw in str(ex)
        except Exception as ex:                       # 거부가 아니라 터진 것 — 빨간불
            print(f"     (터짐: {type(ex).__name__}: {ex})")
            return False
        return False

    real = load_rd()
    check_rd(real, pinned=False)
    chk(real.__dft_sha256__ == PINNED_RD_SHA256 or True, f"[정보] 이 저장소 판독기 sha256 {real.__dft_sha256__[:12]}…")
    host = HERE.parent.parent / "db" / "structures" / "modelc_V0_k663.xyz"
    chk(host.is_file() and _sha(host) == HOST_SHA256, "[양성] host modelc_V0_k663.xyz sha256 = 카드 값")
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # ── 유사포텐셜 가짜 (원소 머리) ──
        pdir = td / "pseudo"
        pdir.mkdir()
        for el, f in PP.items():
            (pdir / f).write_text(f'<UPF version="2.0.1">\n<PP_HEADER element="{el}" pseudo_type="US"/>\n')
        ps = pseudo_record(pdir)
        md5 = {el: d["md5"] for el, d in ps["files"].items()}
        chk(sorted(ps["files"]) == sorted(SPECIES), "[양성] 유사포텐셜 여섯 · 원소 머리 · sha256 · md5 기록")
        (pdir / PP["B"]).write_text('<PP_HEADER element="Al"/>\n')
        chk(refuses("원소 머리", pseudo_record, pdir), "[음성] 유사포텐셜 원소 머리가 다르면 멈춘다")
        (pdir / PP["B"]).write_text(f'<PP_HEADER element="B" pseudo_type="PAW"/>\n')
        os.remove(pdir / PP["Cl"])
        chk(refuses("없음", pseudo_record, pdir), "[음성] 유사포텐셜 파일이 없으면 멈춘다")
        (pdir / PP["Cl"]).write_text('<PP_HEADER element="Cl"/>\n')
        ps = pseudo_record(pdir)
        md5 = {el: d["md5"] for el, d in ps["files"].items()}

        # ── 128 원자 가짜 구조 (host 1×2×5 + 조성) ──
        h = read(str(host)).repeat((1, 2, 1))
        rng = np.random.default_rng(7)
        sy = h.get_chemical_symbols()
        # host Li108→ 1×2×5 는 Li54 P10 S44 Cl16 (124) — 조성 맞추기: P 둘 → B · S 셋 → O · Li 4 더
        iP = [i for i, s in enumerate(sy) if s == "P"][:2]
        iS = [i for i, s in enumerate(sy) if s == "S"][:3]
        for i in iP:
            sy[i] = "B"
        for i in iS:
            sy[i] = "O"
        frac = list(h.get_scaled_positions())
        sy += ["Li"] * 4
        frac += [list(rng.random(3)) for _ in range(4)]
        base_atoms = Atoms(sy, scaled_positions=np.array(frac), cell=h.cell, pbc=True)
        chk(len(base_atoms) == 128 and dict(sorted({s: sy.count(s) for s in set(sy)}.items())) == DFT["composition"],
            "[양성] 시험 구조 128 원자 · 카드 조성")

        def variant(seed, scale=1.0):
            a = base_atoms.copy()
            a.set_cell(np.asarray(a.cell.array) * scale, scale_atoms=True)
            a.positions += np.random.default_rng(seed).normal(0, 0.02, a.positions.shape)
            return a

        # ── 8 단계 가짜 결과 (가족마다 4 런) ──
        rdir = td / "s8_anneal"
        rdir.mkdir()
        plan8, recs, raw = [], {}, []
        Es = {"F_B": [-10.0, -9.95, -9.5, -9.4], "F_P": [-9.48, -9.40, -9.3, -9.2], "F_free": [-6.3, -6.0, -5.9, -5.8]}
        motif = {"F_B": "bo4", "F_P": "distributed", "F_free": "free_s"}
        n = 0
        for F in FAM:
            for k, E in enumerate(Es[F]):
                rank = 3 + 2 * k + FAM.index(F)
                name = f"cfg{rank:04d}_E-0.000_O-{motif[F]}"
                d = rdir / name
                d.mkdir()
                a = variant(n, 0.995 + 0.002 * k)
                n += 1
                write(str(d / "post_relax.xyz"), a, format="extxyz")
                sh = _sha(d / "post_relax.xyz")
                plan8.append({"name": name, "rank": rank, "family": F, "start": {"sha256": "x"}})
                recs[name] = {"ok": True, "E": E, "atoms": a}
                raw.append({"name": name, "outputs": {"post_relax": {"rel": f"{name}/post_relax.xyz", "sha256": sh}}})
        res = rdir / "anneal_results.json"
        res.write_text(json.dumps({"results": raw}))
        A100 = {"order": ["F_B", "F_P", "F_free"], "winner": "F_B", "decision": "승자 F_B (차저 F_P 와 0.520 ≥ 0.2)",
                "winner_runner_up_gap_eV": 0.52, "hold_reasons": None,
                "families": {F: {"n_success": 4, "min": {"name": min((e for e in plan8 if e["family"] == F),
                                                                      key=lambda e: recs[e["name"]]["E"])["name"]}}
                             for F in FAM}}
        for nm in ("verdict.json", "receipt.json"):
            (td / nm).write_text("{}")
        ro = td / "s8_readout.json"
        ro.write_text(json.dumps(A100))
        RD = _FakeRD(real, A100, plan8, recs, res)

        # ── prepare ──
        out = td / "s9"
        plan = prepare(RD, td / "verdict.json", td / "receipt.json", res, ro, pdir, out)
        jn = [j["job"] for j in plan["jobs_sp"]]
        chk(len(jn) == 6 and [j["family"] for j in plan["jobs_sp"]] == ["F_B", "F_B", "F_P", "F_P", "F_free", "F_free"]
            and plan["jobs_sp"][0]["name"].startswith("cfg0003") and plan["jobs_sp"][1]["name"].startswith("cfg0005"),
            f"[양성] prepare — 가족마다 UMA 최저 둘 (6) · 순서 {jn[:2]}")
        pin = parse_pw_in(out / "sp" / jn[0] / "scf.in")
        a0 = read(str(rdir / plan["jobs_sp"][0]["name"] / "post_relax.xyz"))
        chk(np.abs(pin["cell"] - a0.cell.array).max() < 1e-8 and np.abs(pin["frac"] @ pin["cell"] - a0.positions).max() < 1e-7
            and pin["symbols"] == a0.get_chemical_symbols() and pin["k"] == [3, 2, 1]
            and pin["keys"]["ecutwfc"] == "52.0" and pin["keys"]["conv_thr"] == "1.0d-8" and pin["keys"]["smearing"] == "gaussian",
            "[양성] 단일점 입력 = UMA 이완 기하 그대로 (셀 · 좌표 · 원자 순서) · k 3×2×1 · 52/520 · 1.0d-8 · gaussian")
        chk(refuses("이미 있다", prepare, RD, td / "verdict.json", td / "receipt.json", res, ro, pdir, out),
            "[음성] 계획이 있는 폴더에 다시 prepare → 덮지 않는다")
        A_bad = json.loads(json.dumps(A100))
        A_bad["hold_reasons"] = ["F_free: G1 실패"]
        ro2 = td / "ro_hold.json"
        ro2.write_text(json.dumps(A_bad))
        chk(refuses("보류", prepare, _FakeRD(real, A_bad, plan8, recs, res), td / "verdict.json", td / "receipt.json", res,
                    ro2, pdir, td / "s9_hold"), "[음성] 8 단계 본 판독이 보류면 DFT 대상을 고르지 않는다")
        A_mm = json.loads(json.dumps(A100))
        A_mm["families"]["F_P"]["min"]["name"] = "cfg9999"
        ro3 = td / "ro_mm.json"
        ro3.write_text(json.dumps(A_mm))
        chk(refuses("성공 목록", prepare, _FakeRD(real, A_mm, plan8, recs, res), td / "verdict.json", td / "receipt.json",
                    res, ro3, pdir, td / "s9_mm"), "[음성] 성공 목록의 최저가 본 판독과 다르면 멈춘다 (성공 정의가 갈림)")
        ro4 = td / "ro_edit.json"
        ro4.write_text(json.dumps({**A100, "winner": "F_P"}))
        chk(refuses("다시 낸 본 판독", prepare, RD, td / "verdict.json", td / "receipt.json", res, ro4, pdir, td / "s9_e"),
            "[음성] 본 판독 파일을 손대면 (승자 바꿈) 멈춘다")
        chk(refuses("탐침 발동 판정", prepare, RD, td / "verdict.json", td / "receipt.json", res, ro, pdir, td / "s9_k",
                    k_main=[4, 2, 1]), "[음성] k_main 4×2×1 은 탐침 발동 판정 없이는 안 된다")

        # ── 단일점 출력 ──
        sp_E = {"F_B": [-100.00, -99.90], "F_P": [-99.60, -99.70], "F_free": [-96.0, -95.9]}

        def put_sp(stage, jobs, Emap, **kw):
            for j in jobs:
                d = out / stage / j["job"]
                E = Emap(j)
                (d / "scf.out").write_text(_fake_out(d / "scf.in", E_list=[E + 0.5, E], stage="sp",
                                                     pp_md5=md5, **kw.get(j["job"], {})))

        put_sp("sp", plan["jobs_sp"][:5], lambda j: sp_E[j["family"]][j["i"] - 1])
        chk(refuses("누락", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 단일점 출력 하나 없음 → 누락으로 멈춘다 (실패로 세지 않는다)")
        put_sp("sp", plan["jobs_sp"], lambda j: sp_E[j["family"]][j["i"] - 1])
        # 음성: 잡마다 하나씩 깨고 되돌린다
        bad_cases = [("JOB DONE", {"job_done": False}), ("SCF 수렴", {"not_conv": True}), ("ecutwfc", {"ecut": 60.0}),
                     ("conv_thr", {"conv": "1.0E-06"}), ("smearing", {"smear": "Marzari-Vanderbilt"}),
                     ("smearing", {"width": "0.0050"}), ("교환상관", {"xc": "SLA  PW   PSX  PSC"}),
                     ("스핀", {"spin": True}), ("처음 좌표", {"shift_pos": 0.01}), ("입력 이름", {"input_name": "x.in"}),
                     ("힘 블록", {"drop_forces": True}), ("prefix", {"prefix": "sp_other"}),
                     ("유사포텐셜", {"pp_md5": {**md5, "S": "f" * 32}})]
        j0 = plan["jobs_sp"][2]
        for kw_, over in bad_cases:
            d = out / "sp" / j0["job"]
            keep = (d / "scf.out").read_text()
            (d / "scf.out").write_text(_fake_out(d / "scf.in", E_list=[-99.1, sp_E["F_P"][0]], stage="sp",
                                                 pp_md5=over.pop("pp_md5", md5), **over))
            chk(refuses(kw_, read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
                f"[음성] 단일점 출력 {kw_} 어긋남 → 판독 안 함")
            (d / "scf.out").write_text(keep)
        # 다른 잡 출력 바꿔치기 (같은 가족 둘째)
        d1, d2 = out / "sp" / plan["jobs_sp"][0]["job"], out / "sp" / plan["jobs_sp"][1]["job"]
        k1, k2 = (d1 / "scf.out").read_text(), (d2 / "scf.out").read_text()
        (d1 / "scf.out").write_text(k2)
        (d2 / "scf.out").write_text(k1)
        chk(refuses("처음 좌표", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 두 잡의 출력을 맞바꾸면 (에너지 순서가 뒤집힘) 처음 좌표 대조에서 멈춘다")
        (d1 / "scf.out").write_text(k1)
        (d2 / "scf.out").write_text(k2)
        # k 점 수 갈림
        keep = (d1 / "scf.out").read_text()
        (d1 / "scf.out").write_text(_fake_out(d1 / "scf.in", E_list=[-99.5, -100.0], stage="sp", pp_md5=md5, nk=6))
        chk(refuses("k 점 수", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 단계 안 k 점 수가 갈리면 멈춘다")
        (d1 / "scf.out").write_text(keep)
        # 입력을 계획 뒤 손댐
        fin = d1 / "scf.in"
        kin = fin.read_text()
        fin.write_text(kin.replace("conv_thr = 1.0d-8", "conv_thr = 1.0d-6"))
        chk(refuses("입력 scf.in", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 입력을 계획 뒤 손대면 (sha256) 멈춘다")
        fin.write_text(kin)
        # 입력 · 계획 sha 를 같이 고침 (출력 검사가 안 보는 키 — mixing_beta) → 묶인 구조에서 다시 만든 입력과 달라 멈춘다
        kin = fin.read_text()
        fin.write_text(kin.replace("mixing_beta = 0.3", "mixing_beta = 0.7"))
        pj0 = (out / "dft_plan.json").read_text()
        pjm = json.loads(pj0)
        pjm["jobs_sp"][0]["input_sha256"] = _sha(fin)
        (out / "dft_plan.json").write_text(json.dumps(pjm, ensure_ascii=False, indent=1) + "\n")
        chk(refuses("다시 만든 입력", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 입력과 계획의 sha 를 같이 고쳐도 (mixing_beta) 다시 만든 입력과 달라 멈춘다")
        fin.write_text(kin)
        (out / "dft_plan.json").write_text(pj0)
        # 계획 손댐 — 대상 바꿈
        pj = json.loads((out / "dft_plan.json").read_text())
        pj2 = json.loads(json.dumps(pj))
        pj2["jobs_sp"][1]["name"] = pj2["jobs_sp"][2]["name"]
        (out / "dft_plan.json").write_text(json.dumps(pj2))
        chk(refuses("다시 고른 것", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 계획의 대상을 손대면 다시 고른 것과 달라 멈춘다")
        (out / "dft_plan.json").write_text(json.dumps(pj, ensure_ascii=False, indent=1) + "\n")
        # 도구 판 다름
        pj3 = json.loads(json.dumps(pj))
        pj3["tools"]["dft_tool"]["sha256"] = "0" * 64
        (out / "dft_plan.json").write_text(json.dumps(pj3))
        chk(refuses("이 도구 sha256", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 계획을 만든 도구 판과 다르면 멈춘다")
        (out / "dft_plan.json").write_text(json.dumps(pj, ensure_ascii=False, indent=1) + "\n")

        spv = read_sp(RD, out / "dft_plan.json", out / "sp_verdict.json")
        chk(spv["representatives"] == {"F_B": plan["jobs_sp"][0]["job"], "F_P": plan["jobs_sp"][3]["job"],
                                       "F_free": plan["jobs_sp"][4]["job"]}
            and spv["order"] == ["F_B", "F_P", "F_free"] and abs(spv["gap_eV"] - 0.30) < 1e-6
            and spv["G5"]["same_order"] and len(spv["jobs_kprobe"]) == 3,
            "[양성] read_sp — 가족 대표 = 가족마다 단일점 최저 (F_P 는 UMA 둘째) · 순서 · 차 0.30 · G5 · 탐침 입력 셋")
        kin0 = parse_pw_in(out / "kprobe" / spv["jobs_kprobe"][0]["job"] / "scf.in")
        chk(kin0["k"] == [4, 2, 1] and np.abs(kin0["cell"] - pin["cell"]).max() < 1e-12,
            "[양성] 탐침 입력 = 같은 구조 · k 4×2×1")
        chk(refuses("이미 있다", read_sp, RD, out / "dft_plan.json", out / "sp_verdict.json"),
            "[음성] 단일점 판정을 덮지 않는다")

        # ── k 탐침 ──
        def put_kp(dmap):
            for j in spv["jobs_kprobe"]:
                d = out / "kprobe" / j["job"]
                E = next(r["E_eV"] for r in spv["rows"] if r["job"] == spv["representatives"][j["family"]]) + dmap[j["family"]]
                (d / "scf.out").write_text(_fake_out(d / "scf.in", E_list=[E + 0.4, E], stage="kprobe", pp_md5=md5, nk=6))

        put_kp({"F_B": -0.010, "F_P": 0.020, "F_free": 0.0})
        chk(kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4}, {"F_B": 0, "F_P": 0.33, "F_free": 4.02}) == [],
            "[양성] 탐침 — 변화 0.03 · 순서 · 경계 그대로 → 발동 안 함")
        chk(any("변화" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4},
                                                  {"F_B": 0, "F_P": 0.36, "F_free": 4})),
            "[음성] 탐침 — 가족 차 0.06 변함 → 발동")
        chk(any("순서" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.03, "F_free": 4},
                                                  {"F_B": 0, "F_P": -0.01, "F_free": 4})),
            "[음성] 탐침 — 순서 바뀜 (변화 0.04 라도) → 발동")
        chk(any("경계" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.08, "F_free": 4},
                                                  {"F_B": 0, "F_P": 0.12, "F_free": 4})),
            "[음성] 탐침 — 0.10 경계 건넘 (변화 0.04 라도) → 발동")
        chk(any("F_free−F_P" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4.0},
                                                         {"F_B": 0, "F_P": 0.30, "F_free": 4.07})),
            "[음성] 탐침 — 승자–차저가 아닌 쌍 (F_free−F_P) 의 0.07 변화도 발동")
        kpv = read_kprobe(RD, out / "sp_verdict.json", out / "kprobe_verdict.json", host)
        chk(not kpv["triggered"] and len(kpv["jobs_relax"]) == 3 and abs(kpv["reference_cell"]["volume_A3"] - 2436.33) < 1e-6,
            "[양성] read_kprobe — 발동 안 함 → 이완 입력 셋 · 기준 셀 V₀ 2436.33")
        rin = parse_pw_in(out / "relax" / kpv["jobs_relax"][0]["job"] / "scf.in")
        src = read(str(rdir / kpv["jobs_relax"][0]["name"] / "post_relax.xyz"))
        chk(rin["keys"]["calculation"] == "relax" and rin["keys"]["tstress"] == ".true." and rin["k"] == [3, 2, 1]
            and abs(abs(np.linalg.det(rin["cell"])) - 2436.33) < 1e-4
            and np.abs(rin["frac"] - src.get_scaled_positions(wrap=False)).max() < 1e-9
            and np.allclose(Atoms(cell=rin["cell"]).cell.cellpar()[3:], Atoms(cell=h.cell).cell.cellpar()[3:], atol=1e-8),
            "[양성] 이완 입력 = 기준 셀 (host 모양 · V₀) · 분수 좌표 그대로 · relax · tstress · k 3×2×1")
        # 발동 경로
        out_t = td / "s9_trig"
        import shutil
        shutil.copytree(out, out_t)
        for f in ("kprobe_verdict.json",):
            os.remove(out_t / f)
        shutil.rmtree(out_t / "relax")
        for j in spv["jobs_kprobe"]:
            d = out_t / "kprobe" / j["job"]
            E = next(r["E_eV"] for r in spv["rows"] if r["job"] == spv["representatives"][j["family"]])
            E += {"F_B": 0.0, "F_P": 0.08, "F_free": 0.0}[j["family"]]
            (d / "scf.out").write_text(_fake_out(d / "scf.in", E_list=[E + 0.4, E], stage="kprobe", pp_md5=md5, nk=6))
        # 복사본의 계획 · 판정은 같은 상대 경로라 그대로 결속된다
        kpt = read_kprobe(RD, out_t / "sp_verdict.json", out_t / "kprobe_verdict.json", host)
        chk(kpt["triggered"] and "jobs_relax" not in kpt and any("변화" in w for w in kpt["why"]),
            "[양성] read_kprobe — F_P 0.08 변함 → 발동 · 이완 입력 안 씀 · 다음 = 4×2×1 다시")
        chk(refuses("발동", read_relax, RD, out_t / "kprobe_verdict.json", out_t / "relax_verdict.json", host),
            "[음성] 발동한 탐침 뒤 이완은 판독하지 않는다")
        out_4 = td / "s9_k421"
        plan4 = prepare(RD, td / "verdict.json", td / "receipt.json", res, ro, pdir, out_4, k_main=[4, 2, 1],
                        after_kprobe=out_t / "kprobe_verdict.json")
        chk(parse_pw_in(out_4 / "sp" / plan4["jobs_sp"][0]["job"] / "scf.in")["k"] == [4, 2, 1],
            "[양성] 발동 뒤 판 — 6 단일점 k 4×2×1 (prepare --k_main 4 2 1 --after_kprobe)")

        # 판정 파일 손댐 — 뒤 단계가 다시 내서 잡는다
        kv_keep = (out / "kprobe_verdict.json").read_text()
        kvx = json.loads(kv_keep)
        kvx["pairs"]["F_P-F_B"]["change"] = 0.0001
        (out / "kprobe_verdict.json").write_text(json.dumps(kvx))
        chk(refuses("다시 낸 발동 판정", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 탐침 판정의 쌍 값을 손대면 이완 판독이 멈춘다 (출력에서 다시 낸 판정과 다름)")
        kvx = json.loads(kv_keep)
        kvx["jobs_relax"][0]["name"] = kvx["jobs_relax"][1]["name"]
        (out / "kprobe_verdict.json").write_text(json.dumps(kvx))
        chk(refuses("이완 잡 기록", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 탐침 판정의 이완 잡 목록을 손대면 (다시 만든 입력과 다름) 멈춘다")
        (out / "kprobe_verdict.json").write_text(kv_keep)
        fake_t = td / "kp_fake_triggered.json"
        kvx = json.loads(kv_keep)
        kvx.update({"triggered": True, "why": ["가짜"]})
        kvx["sp_verdict"]["rel"] = os.path.relpath(out / "sp_verdict.json", td)
        fake_t.write_text(json.dumps(kvx))
        chk(refuses("다시 낸 발동 판정", prepare, RD, td / "verdict.json", td / "receipt.json", res, ro, pdir, td / "s9_fake",
                    k_main=[4, 2, 1], after_kprobe=fake_t),
            "[음성] 발동 안 한 탐침 판정을 '발동' 으로 고쳐 4×2×1 판을 열려 하면 멈춘다 (출력에서 다시 냄)")

        # ── 이완 출력 · EOS 결속 ──
        def put_rx(Emap, Pmap, **over):
            for j in kpv["jobs_relax"]:
                d = out / "relax" / j["job"]
                kw = {"P_kbar": Pmap[j["family"]], **over.get(j["family"], {})}
                (d / "scf.out").write_text(_fake_out(d / "scf.in", E_list=[Emap[j["family"]] + 0.3, Emap[j["family"]]],
                                                     stage="relax", pp_md5=md5, **kw))

        ERX = {"F_B": -101.0, "F_P": -100.8, "F_free": -97.0}
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_P={"bfgs": False})
        chk(refuses("bfgs", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 이완 미수렴 ('bfgs converged' 없음) → 판독 안 함")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_B={"P_before_last": True})
        chk(refuses("응력", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 응력이 마지막 SCF 뒤에 없다 (앞 걸음의 압력) → 판독 안 함")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_B={"final_E": ERX["F_B"] - 0.5})
        chk(refuses("Final energy", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] Final energy 가 마지막 '!' 와 다르면 판독 안 함")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_free={"vol_override": 2400.0})
        chk(refuses("부피", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 출력 부피 ≠ 기준 셀 V₀ → 판독 안 함")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_P={"final": False})
        chk(refuses("최종 좌표", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 최종 좌표 블록이 없으면 판독 안 함")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}, F_P={"P_kbar": None})
        chk(refuses("응력", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 압력 줄이 없으면 판독 안 함 (P 를 지어내지 않는다)")
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0})
        rv = read_relax(RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host)
        ei = rv["eos_input"]
        chk(rv["eos"]["skip_eos"] and abs(ei["F_B"]["P_GPa"] - 0.5) < 1e-12 and abs(ei["F_P"]["P_GPa"] + 0.3) < 1e-12
            and abs(ei["F_B"]["V_A3"] - 2436.33) < 0.01 and abs(ei["F_B"]["E_eV"] - ERX["F_B"]) < 1e-6
            and rv["eos"]["baseline_order"] == ["F_B", "F_P", "F_free"],
            "[양성] read_relax — (E, P, V) 를 출력에서 읽음 (P kbar→GPa · V = V₀) · 판 고정 eos_robust → EOS 생략")
        st = rv["stage10"]
        chk(st and [s["name"] for s in st["stability_targets"]] == [s["name"] for s in sorted(
            (e for e in plan8 if e["family"] == "F_B"), key=lambda e: recs[e["name"]]["E"])[:3]]
            and len(rv["electronic_targets"]) == 3 and all(Path(out / t["rel"]).is_file() for t in rv["electronic_targets"]),
            "[양성] 10 단계 — DFT 승자 F_B (0.2 ≥ 0.10) → 그 가족 UMA 어닐 최저 셋 · 전자구조 대상 = 이완 셋 (파일 · 부모 해시)")
        chk(rv["relaxed"]["F_B"]["record"]["end_motif"] in ("F_B", "F_P", "F_free", "mixed", "unclassified")
            and "B_coordination" in rv["relaxed"]["F_B"]["record"], "[양성] 이완 구조 기록 — 끝 꼴 (판 고정 분류) · B · P 배위")
        os.remove(out / "relax_verdict.json")
        put_rx({"F_B": -101.0, "F_P": -100.95, "F_free": -97.0}, {"F_B": 1.0, "F_P": -0.5, "F_free": 0.8})
        rv2 = read_relax(RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host)
        chk(rv2["eos"]["skip_eos"] and [s["family"] for s in rv2["stage10"]["stability_targets"]] == FAM,
            "[양성] 10 단계 — DFT 차 0.05 < 0.10 (|P| ≤ 0.1 GPa · 보정 < 0.004 eV) → 가족마다 UMA 어닐 최저 하나 (셋)")
        chk(rv["corrected_gap_range_eV"][0] - 0.2 > 0.02 and rv["corrected_gap_range_eV"][1] - 0.2 > 0.06,
            f"[정보] 압력 0.5 · −0.3 GPa 만으로도 보정 뒤 차가 {rv['corrected_gap_range_eV'][0]:.3f}–{rv['corrected_gap_range_eV'][1]:.3f} "
            f"(보정 전 0.200) — 2436 Å³ 셀이라 셀마다 −P²V/2B 가 0.02–0.09 eV")
        os.remove(out / "relax_verdict.json")
        put_rx(ERX, {"F_B": 25.0, "F_P": -3.0, "F_free": 8.0})
        rv3 = read_relax(RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host)
        chk(not rv3["eos"]["skip_eos"] and rv3["stage10"] is None and "EOS 필요" in rv3["decision"] and "F_B" in rv3["decision"],
            "[음성] |P| 2.5 GPa > 2 → EOS 필요 · 고르기 안 함 · 어느 셀인지 말한다")
        os.remove(out / "relax_verdict.json")
        put_rx({"F_B": -101.0, "F_P": -100.905, "F_free": -97.0}, {"F_B": 19.0, "F_P": 0.0, "F_free": 8.0})
        rv4 = read_relax(RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host)
        chk(not rv4["eos"]["skip_eos"] and rv4["stage10"] is None,
            "[음성] 보정 범위 안에서 0.10 판정이 바뀔 수 있으면 (차 0.095 · |P| 1.9) EOS 필요 · 고르기 안 함")
        os.remove(out / "relax_verdict.json")
        # 이완 출력 바꿔치기 (가족끼리)
        put_rx(ERX, {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0})
        jb, jp = (out / "relax" / j["job"] for j in kpv["jobs_relax"][:2])
        kb, kp_ = (jb / "scf.out").read_text(), (jp / "scf.out").read_text()
        (jb / "scf.out").write_text(kp_)
        (jp / "scf.out").write_text(kb)
        chk(refuses("처음 좌표", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 이완 출력을 가족끼리 맞바꾸면 처음 좌표 대조에서 멈춘다")
        (jb / "scf.out").write_text(kb)
        (jp / "scf.out").write_text(kp_)
        # 단일점 출력이 판정 뒤 바뀜 → 이완 판독도 멈춘다 (사슬)
        dsp = out / "sp" / plan["jobs_sp"][3]["job"]
        ksp = (dsp / "scf.out").read_text()
        (dsp / "scf.out").write_text(ksp.replace(f"{sp_E['F_P'][1] / RY_EV:.8f}", f"{(sp_E['F_P'][1] - 0.4) / RY_EV:.8f}"))
        chk(refuses("단일점 판정", read_relax, RD, out / "kprobe_verdict.json", out / "relax_verdict.json", host),
            "[음성] 단일점 출력이 판정 뒤 바뀌면 (에너지) 이완 판독도 멈춘다 (사슬 다시 결속)")
        (dsp / "scf.out").write_text(ksp)
        # 기준 셀: host 가 다르면 멈춘다
        bad_host = td / "host_bad.xyz"
        bad_host.write_text(host.read_text().replace("Cl", "Br", 1))
        chk(refuses("host", reference_cell, bad_host), "[음성] host 파일이 카드 sha256 이 아니면 기준 셀을 만들지 않는다")
        c, crec = reference_cell(host)
        chk(abs(crec["volume_A3"] - 2436.33) < 1e-6 and abs(crec["scale"] - (2436.33 / crec["host_volume_A3"]) ** (1 / 3)) < 1e-12,
            f"[양성] 기준 셀 — host 1×2×5 V {crec['host_volume_A3']:.3f} → 등방 스케일 {crec['scale']:.6f} → V₀ 2436.33")
    print(f"selftest: {ok[1]}/{ok[0]}")
    return 0 if ok[0] == ok[1] else 1


# ───────────────────────── CLI ─────────────────────────
def main(argv=None):
    if argv is None and "--selftest" in sys.argv[1:]:
        return _selftest()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("prepare")
    for k in ("verdict", "receipt", "results", "readout", "pseudo_dir", "out_dir"):
        a.add_argument(f"--{k}", required=True)
    a.add_argument("--k_main", type=int, nargs=3)
    a.add_argument("--after_kprobe")
    b = sub.add_parser("read_sp")
    b.add_argument("--plan", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--host", help="k_main 4×2×1 판에서만 (이완 입력의 기준 셀)")
    c = sub.add_parser("read_kprobe")
    c.add_argument("--sp_verdict", required=True)
    c.add_argument("--host", required=True)
    c.add_argument("--out", required=True)
    d = sub.add_parser("read_relax")
    d.add_argument("--prev", required=True, help="탐침 판정 (k_main 3×2×1) 또는 단일점 판정 (k_main 4×2×1)")
    d.add_argument("--host", required=True, help="기준 셀을 다시 만들어 이완 입력을 대조한다 (modelc_V0_k663.xyz)")
    d.add_argument("--out", required=True)
    for s in (a, b, c, d):
        s.add_argument("--readout_tool", default=str(DEFAULT_RD))
    A = ap.parse_args(argv)
    RD = load_rd(A.readout_tool)
    check_rd(RD)
    print(f"DFT 도구 {SELF} · sha256 {_tool_fp()['sha256']}")
    print(f"판독기 {RD.__dft_path__} · sha256 {RD.__dft_sha256__}")
    if A.cmd == "prepare":
        p = prepare(RD, A.verdict, A.receipt, A.results, A.readout, A.pseudo_dir, A.out_dir, A.k_main, A.after_kprobe)
        print(f"-> {Path(A.out_dir) / 'dft_plan.json'} · 단일점 {len(p['jobs_sp'])} 잡 (k {p['k_main']}) · "
              f"유사포텐셜 {p['pseudo']['dir']}")
        for j in p["jobs_sp"]:
            print(f"   {j['job']}  ←  {j['name']}  (UMA 끝 꼴 {j['uma_record']['end_motif']})")
        print(f"   실행: MIN_FREE_MIB=45000 bash <src>/tools/doping/run_force_check_scf.sh {Path(A.out_dir) / 'sp'}")
        return 0
    if A.cmd == "read_sp":
        v = read_sp(RD, A.plan, A.out, A.host)
        print(f"-> {A.out} · 단일점 순서 {v['order']} · 최저–차점 {v['gap_eV']:.3f} eV/B₂O₃ · G5 {'같음' if v['G5']['same_order'] else '다름'}")
        print(f"   {v['sentence_sp']}")
        print(f"   다음: {v['next']}")
        return 0
    if A.cmd == "read_kprobe":
        v = read_kprobe(RD, A.sp_verdict, A.out, A.host)
        print(f"-> {A.out} · 탐침 {'발동' if v['triggered'] else '발동 안 함'}")
        for k, x in v["pairs"].items():
            print(f"   {k}: {x['k_main']:+.3f} → {x['k_probe']:+.3f} (변화 {x['change']:+.3f})")
        for w in v["why"]:
            print(f"   ⛔ {w}")
        print(f"   다음: {v['next']}")
        return 0
    v = read_relax(RD, A.prev, A.out, A.host)
    print(f"-> {A.out}")
    for r in v["rows"]:
        print(f"   {r['job']}: P {r['P_GPa']:+.2f} GPa · bfgs {r['bfgs']['steps']} 걸음")
    print(f"   {v['decision']}")
    if v.get("stage10"):
        print(f"   10 단계: {v['stage10']['rule']}")
        for s in v["stage10"]["stability_targets"]:
            print(f"     안정성 대상 {s['family']} {s['name']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
