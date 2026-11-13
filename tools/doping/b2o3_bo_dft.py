#!/usr/bin/env python3
"""b2o3 B·O 배치 카드 — 9 단계 DFT (단일점 → k 탐침 → 고정셀 이온 이완 → EOS 생략 판정) + 10 단계 고르기.

카드 db/properties/b2o3_bo_placement_estimand_2026_11_09.json — 개정_1 단계별_값 9_DFT · 10_고르기 · 판독_계약 (EOS_생략 ·
서술_한계) + 개정_5 (9 단계 운영값 · 결과 전 · [제안]) · Codex DY 확인 4 (EOS 의 (E, P, V) 를 결과 파일에 결속).
절차 db/properties/cell_construction_protocol_v1_2026_11_09.json 9_DFT_확인 · 10_고르기 · 13_기록_계보.
v2 (2026-11-13) = Codex EF 회신 (NO-GO · P1 6 · P2 6) 고침 — kb/reviews/codex_EF_reply_b2o3_dft_stage9_tools_2026_11_13.md.

  prepare      8 단계 결과를 판 고정 판독기로 다시 결속 (anneal_readout 다시 내기 · 본 판독 파일 몸통 대조 · 보류면 멈춤) →
               가족마다 UMA 어닐 최저 둘 (6 · 판독기의 성공 정의 그대로 · 가족 최저 · 성공 수를 본 판독과 대조) →
               단일점 입력 (UMA 이완 기하 그대로 · 셀 포함 · k_main) + 계획 dft_plan.json
               (이 도구 · 판독기 sha256 · 묶인 입력 · 유사포텐셜 파일 sha256 · md5 · 가전자 수 · 구조 파일 sha256 · 입력 sha256)
  read_sp      계획을 다시 결속 (8 단계 다시 내기 · 고르기 · **구조를 8 단계 기록에서 다시 찾아 대조** · k_main 자격 ·
               유사포텐셜 파일 다시 기록 · 입력을 묶인 구조에서 다시 만들어 대조) → 단일점 출력 6 결속 · 검사 →
               단일점 가족 순서 (G5 기록) → k_main 3×2×1 이면 k 탐침 입력 (가족 대표 셋 · 4×2×1) ·
               k_main 4×2×1 (탐침 발동 뒤 판) 이면 탐침 없이 이완 입력
  read_kprobe  단일점 판정을 **통째로 다시 내서 대조** → 탐침 출력 3 결속 (요청한 4×2×1 격자를 출력의 k 점 좌표 · 가중치로 확인) →
               발동 판정 (세 가족 쌍 모두: 차가 0.05 넘게 변함 · 순서 바뀜 · |차| 의 0.10 경계 건넘) →
               발동 안 하면 이완 입력 (기준 셀 · k_main) · 발동하면 멈춘다 (6 단일점을 4×2×1 로 — prepare --k_main 4 2 1 --after_kprobe)
  read_relax   앞 판정 사슬을 통째로 다시 내서 대조 → 이완 출력 3 결속 → 가족마다 (E, P, V) 를 **출력 파일에서** 읽는다
               (DY 확인 4) → 판 고정 eos_robust → EOS 생략이면 DFT 순서 · 승자–차저 0.10 판정 · 10 단계 고르기
               (안정성 대상 · 전자구조 대상) · 생략 불가면 'EOS 필요' 에서 멈춘다 (고르기 · 전자구조 대상 둘 다 null —
               이완 구조는 진단 자료로만 남긴다)
  reject       판독기가 거부한 출력을 scf.out.rejected.N 으로 **보존해 옮긴다** (지우지 않는다) — 실행기는 scf.out 이 없는
               잡만 다시 돈다 (실행기의 완료 검사가 판독기보다 느슨해서 '같은 명령 다시' 로는 안 고쳐진다 · Codex EF P2-6)

출력 결속 (잡마다 · 하나라도 걸리면 그 단계 판정 안 함): utf-8 strict (깨진 바이트 거부) · **한 출력 = 한 실행**
('Program PWSCF' 머리 하나 · JOB DONE 하나 — 이어 붙임 · 재시작 거부) · 입력 sha256 = 기록 값 · 출력에 찍힌 입력 이름 · 원자 수 ·
**전자 수 = Σ 조성 × 가전자 (총전하 0)** · PP 마다 Zval = 계획 · **SCF 출력은 '!' 한 번 · 이완은 '!' 수 = BFGS 가 센 SCF 수** ·
ecut · 수렴 문턱 · smearing 종류 · 폭 · PBE · 비스핀 · PP 이름 ·
MD5 · 셀 축 · 처음 좌표 (그 잡의 입력과 같음 — 바꿔치기) · prefix · **k 점 좌표 · 가중치가 입력의 격자 (시간 반전만) 를 정확히
한 번씩 덮음** · SCF 수렴 · 힘 블록이 마지막 SCF 뒤 · 단계 안 PWSCF 판 같음 · 이완은 **BFGS 기준 · 머리의 수렴 문턱 · nstep 이
계약과 같음** · 'bfgs converged' · **마지막 힘 블록의 모든 성분 ≤ forc_conv_thr** · 최종 좌표 · Final energy = 마지막 '!' ·
응력이 마지막 SCF 뒤 · 부피 = V₀.

경로 규약: 잡 · 구조 · 출력 · 대상의 {rel · sha256} 은 **계획 폴더 (dft_plan.json 이 있는 곳) 기준** · 판정 파일 사이의 고리
(plan · sp_verdict · prev) 는 **그 판정 파일이 있는 폴더 기준**. 파일은 utf-8 · LF 로 쓴다 (Windows 에서도 같은 바이트 · sha).

⛔ 이 도구가 못 하는 것
  · pw.x 를 돌리지 않는다 (실행기 tools/doping/run_force_check_scf.sh · gabia GPU · GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 —
    잡 시작 때만 확인한다 · 도는 중에 다른 GPU 잡이 올라오는 것은 못 막는다 · 운영 규칙으로).
  · EOS (부피 격자 · BM3) 를 하지 않는다 — 생략 불가면 멈추고 어느 셀인지 말한다 (EOS 는 다음 판 · 그때 이미 본 압력 · 에너지를
    밝히고 새 단계 전에 정한다 · '결과 전에 정했다' 고 소급하지 않는다).
  · 수렴을 보장하지 않는다 — 실패 · 누락 잡은 판정에 넣지 않고 멈춘다 (실패는 reject 로 보존한 뒤 다시 돌린다 · 누락 ≠ 실패).
    disk_io nowf 라 중간 재개 (restart) 는 없다 — 다시 돌리면 처음부터다.
  · 단일점만으로 'DFT 순위' 를 쓰지 않는다 (절차 9_DFT_확인 ⛔) — 단일점 순서는 G5 기록 · 판정은 이온 이완 뒤.
  · 이온 이완 판정은 '사전 규칙으로 고른 대표 구조를 공통 기준 셀에서 이온 이완한 에너지 비교' 다 — 이 수렴 설정 (forc 1e-3 ·
    etot 1e-5 · nstep 200) · 고정 기준 셀에 조건부 · 가족 전체의 DFT 최저 · 자유 셀 바닥상태가 아니다. 0.10 은 판정 여유이지
    인증된 정확도가 아니다.
  · 유사포텐셜이 'B₂O₃ 캠페인 PP' 와 바이트까지 같은지 보증하지 못한다 (7 월 원본은 저장소 밖) — 이름 · 원소 머리 · 가전자 ·
    sha256 · md5 를 기록하고 출력의 MD5 · Zval 과 대조할 뿐이다. 52/520 수렴을 이름으로 인증하지 않는다.
  · 이완 뒤 골격이 깨졌는지 판정하지 않는다 — B · P 배위 · O 끝 꼴은 **기록** (카드 G7 · 판정 아님).
  · relax_verdict 를 쓰는 다음 단계 (11 · 12) 도구는 이 판정을 다시 결속해야 한다 (여기서 끝 · 띠틈 · DOS · MD 는 다른 도구).

쓰는 법 (gabia — 판 고정 판독기 $R/src · 이 도구는 다른 worktree)
  python3 b2o3_bo_dft.py --selftest
  python3 b2o3_bo_dft.py prepare --readout_tool $R/src/tools/doping/b2o3_bo_readout.py --verdict $R/s6_verdict.json \
          --receipt $R/s7_receipt.json --results $R/s8_anneal/anneal_results.json --readout $R/s8_readout.json \
          --pseudo_dir /data/work/pseudo --out_dir $R/s9_dft
  GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 bash <이 판>/tools/doping/run_force_check_scf.sh $R/s9_dft/sp
  python3 b2o3_bo_dft.py read_sp --readout_tool … --plan $R/s9_dft/dft_plan.json --out $R/s9_dft/sp_verdict.json
  (실패가 있으면) python3 b2o3_bo_dft.py reject --plan $R/s9_dft/dft_plan.json --stage sp → 실행기 다시
  GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 bash … run_force_check_scf.sh $R/s9_dft/kprobe
  python3 b2o3_bo_dft.py read_kprobe --readout_tool … --sp_verdict $R/s9_dft/sp_verdict.json --host <modelc_V0_k663.xyz> \
          --out $R/s9_dft/kprobe_verdict.json
  GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 bash … run_force_check_scf.sh $R/s9_dft/relax
  python3 b2o3_bo_dft.py read_relax --readout_tool … --prev $R/s9_dft/kprobe_verdict.json --host <…> --out $R/s9_dft/relax_verdict.json
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
from collections import Counter
from pathlib import Path

import numpy as np

SELF = Path(__file__).resolve()
HERE = SELF.parent
DEFAULT_RD = HERE / "b2o3_bo_readout.py"
PINNED_RD_SHA256 = "872d91f7508ad21c3d67f373bee228bd894994b731a77f69525818db3a8967cf"   # 12b8bdef (Codex DY GO)
HOST_SHA256 = "dc0f8c0c12df6ef6a034e78a9b489b09fd8d472b01f1d9b02e8c860f6410a1e6"          # db/structures/modelc_V0_k663.xyz

KIND_PLAN = "b2o3_bo_dft_plan/v2"
KIND_SP = "b2o3_bo_dft_sp_verdict/v2"
KIND_KP = "b2o3_bo_dft_kprobe_verdict/v2"
KIND_RX = "b2o3_bo_dft_relax_verdict/v2"

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
    "nspin": 1, "nosym": True, "tot_charge": 0.0, "conv_thr": 1.0e-8,
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
TOL = {"ecut": 1e-6, "conv_rel": 1e-6, "degauss": 1e-6, "cell_A": 1e-4, "pos_A": 1e-4, "V_A3": 0.01, "E_final_Ry": 1e-6,
       "nelec": 1e-6, "zval": 1e-6, "k_grid": 1e-4, "k_weight": 1e-4, "force_print": 1e-9}
B_CUT_A = {"S": 2.2, "O": 1.7}            # 기록용 B 배위 (카드 G7 · 판정 아님)
P_CUT_A = {"S": 2.4, "O": 1.8}            # 기록용 P 배위 (골격 기록 · 판정 아님)

NEED = ("anneal_readout", "verify_screen_verdict", "load_records", "_core", "end_motif", "eos_robust", "CONTRACT", "FAM_ORDER")


# ───────────────────────── 공통 ─────────────────────────
def _sha(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _md5(p) -> str:
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def _text_sha(t: str) -> str:
    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def _write_bytes(path, text: str) -> Path:
    """utf-8 · LF 그대로 쓴다 (Windows 의 줄바꿈 변환을 막는다 — Codex EF P2-4)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


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
    return _write_bytes(path, json.dumps(obj, ensure_ascii=False, indent=1, default=str) + "\n")


def _load(path, kind) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"⛔ {p} 가 없다")
    d = json.loads(p.read_bytes().decode("utf-8"))
    if d.get("kind") != kind:
        raise SystemExit(f"⛔ {p.name} 는 {kind} 가 아니다 ({d.get('kind')})")
    return d


def _norm_v(v) -> dict:
    """판정 파일 대조용 — 도구 경로는 빼고 sha256 만 (같은 판이면 경로가 달라도 같은 판정)."""
    o = json.loads(json.dumps(v, ensure_ascii=False, default=str))
    o["tools"] = {k: (x or {}).get("sha256") for k, x in (o.get("tools") or {}).items()}
    return o


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
def _upf_head(path) -> str:
    return Path(path).read_bytes()[:60000].decode("utf-8", errors="replace")


def upf_element(path):
    txt = _upf_head(path)
    m = re.search(r'element\s*=\s*"\s*([A-Za-z]{1,2})\s*"', txt, re.I)
    if m:
        return m.group(1).capitalize()
    m = re.search(r"^\s*([A-Za-z]{1,2})\s+Element", txt, re.M)
    return m.group(1).capitalize() if m else None


def upf_zval(path):
    """가전자 수 — UPF v2 z_valence="…" · UPF v1 '… Z valence' 줄. 못 읽으면 None."""
    txt = _upf_head(path)
    m = re.search(r'z_valence\s*=\s*"\s*([-+.\dEeDd]+)\s*"', txt, re.I)
    if not m:
        m = re.search(r"^\s*([-+.\dEeDd]+)\s+Z valence", txt, re.M | re.I)
    try:
        return float(m.group(1).replace("D", "E").replace("d", "e")) if m else None
    except ValueError:
        return None


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
        z = upf_zval(f)
        if z is None or not math.isfinite(z) or z <= 0:
            bad.append(f"{el}: {f.name} 의 가전자 수 (z_valence) 를 못 읽었다")
            continue
        rec[el] = {"file": PP[el], "sha256": _sha(f), "md5": _md5(f), "z_valence": z}
    if bad:
        raise SystemExit("⛔ 유사포텐셜 — " + " · ".join(bad) + " — 시작하지 않는다")
    return {"dir": str(pdir.resolve()), "files": rec}


# ───────────────────────── 입력 쓰기 · 읽기 ─────────────────────────
def pw_input_text(atoms, *, prefix, calc, k, pseudo_dir, tstress=False) -> str:
    """QE pw.x 입력 — 셀 CELL_PARAMETERS angstrom · 좌표 crystal (원자 순서 그대로) · K_POINTS automatic k 0 0 0 · nosym
    (대칭으로 k 를 줄이지 않는다 — 시간 반전만 · 출력의 k 점을 요청 격자와 정확히 대조할 수 있게).

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
          f"    smearing = '{DFT['smearing']}'", f"    degauss = {DFT['degauss']}", f"    nspin = {DFT['nspin']}",
          "    nosym = .true.", f"    tot_charge = {DFT['tot_charge']}", "/",
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


def write_pw_input(path, atoms, *, prefix, calc, k, pseudo_dir, tstress=False) -> Path:
    return _write_bytes(path, pw_input_text(atoms, prefix=prefix, calc=calc, k=k, pseudo_dir=pseudo_dir, tstress=tstress))


def parse_pw_in(path) -> dict:
    """이 도구가 쓴 입력을 다시 읽는다 → 셀 (Å) · 원소 · 분수 좌표 · k · 키 (출력 결속 대조용)."""
    lines = Path(path).read_bytes().decode("utf-8").splitlines()
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
    kp = lines[kk + 1].split()
    return {"keys": keys, "cell": cell, "symbols": syms, "frac": np.array(frac), "k": [int(x) for x in kp[:3]],
            "k_shift": [int(x) for x in kp[3:6]]}


# ───────────────────────── 출력 읽기 ─────────────────────────
_RE_E = re.compile(r"^!\s+total energy\s+=\s+(-?\d+\.\d+)\s+Ry", re.M)
_RE_P = re.compile(r"total\s+stress\s+\(Ry/bohr\*\*3\)\s+\(kbar\)\s+P=\s*(-?\d+\.?\d*)")
_RE_PP = re.compile(r"PseudoPot\.\s*#\s*\d+\s+for\s+(\w+)\s+read from file:\s*\n\s*(\S+)\s*\n\s*MD5 check sum:\s*([0-9a-fA-F]+)")
_RE_F = re.compile(r"atom\s+\d+\s+type\s+\d+\s+force\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)")
_RE_K = re.compile(r"k\(\s*\d+\)\s*=\s*\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\),\s*wk\s*=\s*([-\d.]+)")
#: 한 실행에서 딱 한 번 찍히는 설정 줄 (실측: QE 7.4.1 SCF · 고정셀 relax 출력 4 개에서 모두 1 — 2026-11-13) — 둘이면 섞인 출력
_ONCE = {"ecutwfc": r"kinetic-energy cutoff", "ecutrho": r"charge density cutoff", "nelec": r"number of electrons",
         "nk": r"number of k points=", "conv_thr": r"scf convergence threshold", "xc": r"Exchange-correlation=",
         "axes": r"crystal axes: \(cart", "initial": r"positions \(alat units\)", "volume": r"unit-cell volume",
         "alat": r"lattice parameter \(alat\)"}
_ONCE_RELAX = {"etot_thr": r"energy convergence thresh\.", "forc_thr": r"force convergence thresh\.", "nstep": r"(?m)^\s*nstep\s*="}
#: JOB DONE 뒤에 있으면 안 되는 계산 기록 (실제 출력의 JOB DONE 뒤 = '=---=' 줄 · 런타임 경고 'ieee_… is signaling' 뿐)
_AFTER_DONE = (r"(?m)^!\s+total energy", r"Forces acting on atoms", r"total\s+stress", r"bfgs converged", r"Final energy",
               r"Begin final coordinates", r"Program PWSCF", r"number of k points", r"kinetic-energy cutoff",
               r"convergence has been achieved", r"number of electrons")


def _num(rx, txt, cast=float):
    m = re.search(rx, txt)
    try:
        return cast(m.group(1)) if m else None
    except ValueError:
        return None


def parse_pw_out(path) -> dict:
    """pw.x 출력 → 결속 · 판정에 쓰는 값 (못 찾은 것은 None — 0 으로 두지 않는다).

    utf-8 strict — 깨진 바이트는 decode_error 로 남기고 (판정에서 거부) 나머지는 대체 문자로 읽어 보여만 준다 (Codex EF P2-3).
    """
    p = Path(path)
    b = p.read_bytes()
    o = {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "decode_error": None}
    try:
        txt = b.decode("utf-8")
    except UnicodeDecodeError as e:
        o["decode_error"] = f"{e.reason} (바이트 {e.start})"
        txt = b.decode("utf-8", errors="replace")
    o["n_runs"] = txt.count("Program PWSCF v.")
    o["n_job_done"] = txt.count("JOB DONE")
    o["once"] = {k: len(re.findall(rx, txt)) for k, rx in _ONCE.items()}
    o["once_relax"] = {k: len(re.findall(rx, txt)) for k, rx in _ONCE_RELAX.items()}
    jd = txt.rfind("JOB DONE")
    o["after_done"] = [rx for rx in _AFTER_DONE if jd >= 0 and re.search(rx, txt[jd:])]
    o["version"] = _num(r"Program PWSCF v\.(\S+) starts", txt, str)
    o["input_name"] = _num(r"Reading input from (\S+)", txt, str)
    o["nat"] = _num(r"number of atoms/cell\s*=\s*(\d+)", txt, int)
    o["nelec"] = _num(r"number of electrons\s*=\s*([\d.]+)", txt)
    o["ecutwfc"] = _num(r"kinetic-energy cutoff\s*=\s*([\d.]+)\s*Ry", txt)
    o["ecutrho"] = _num(r"charge density cutoff\s*=\s*([\d.]+)\s*Ry", txt)
    o["conv_thr"] = _num(r"scf convergence threshold\s*=\s*([\d.Ee+-]+)", txt)
    o["etot_thr"] = _num(r"energy convergence thresh\.\s*=\s*([\d.Ee+-]+)", txt)
    o["forc_thr"] = _num(r"force convergence thresh\.\s*=\s*([\d.Ee+-]+)", txt)
    o["nstep"] = _num(r"nstep\s*=\s*(\d+)", txt, int)
    m = re.search(r"number of k points=\s*(\d+)\s+(\S+)\s+smearing, width \(Ry\)=\s*([\d.Ee+-]+)", txt)
    o["nk"], o["smearing"], o["degauss"] = (int(m.group(1)), m.group(2).lower(), float(m.group(3))) if m else (None, None, None)
    o["klist"] = None
    if m:
        c = txt.find("cart. coord. in units 2pi/alat", m.end())
        if c >= 0:
            rows = _RE_K.findall(txt[c:c + 160 * (o["nk"] + 2)])
            if len(rows) >= o["nk"]:
                o["klist"] = [[float(x) for x in r] for r in rows[:o["nk"]]]
    m = re.search(r"Exchange-correlation=\s*([^\n(]+)", txt)
    o["xc"] = m.group(1).split() if m else None
    pps = []
    for mm in _RE_PP.finditer(txt):
        z = re.search(r"Zval\s*=\s*([\d.]+)", txt[mm.end():mm.end() + 400])
        pps.append({"el": mm.group(1), "file": Path(mm.group(2)).name, "md5": mm.group(3).lower(),
                    "zval": float(z.group(1)) if z else None})
    o["pp"] = pps
    v = _num(r"unit-cell volume\s*=\s*([\d.]+)\s*\(a\.u\.\)\^3", txt)
    o["volume_A3"] = v * BOHR_A ** 3 if v is not None else None
    alat = _num(r"celldm\(1\)=\s*([\d.]+)", txt)
    o["alat_bohr"] = alat
    m = re.search(r"crystal axes: \(cart\. coord\. in units of alat\)\s*\n"
                  r"\s*a\(1\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)\s*\n"
                  r"\s*a\(2\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)\s*\n"
                  r"\s*a\(3\) = \(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)", txt)
    o["axes_alat"] = np.array([float(x) for x in m.groups()]).reshape(3, 3).tolist() if m else None
    o["cell_A"] = (np.array(o["axes_alat"]) * alat * BOHR_A).tolist() if (o["axes_alat"] and alat) else None
    pos = None
    k = txt.find("positions (alat units)")
    if k >= 0 and o["nat"] and alat:
        rows = re.findall(r"^\s*\d+\s+([A-Za-z]+)\s+tau\(\s*\d+\)\s*=\s*\(\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\s*\)",
                          txt[k:k + 200 * o["nat"]], re.M)
        if len(rows) >= o["nat"]:
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
    fb = [mm.start() for mm in re.finditer(r"Forces acting on atoms", txt)]
    o["forces_block"] = bool(fb)
    o["forces_at"] = fb[-1] if fb else None
    o["final_forces_max_comp_RyBohr"], o["max_force_eV_A"], o["final_forces_n"] = None, None, 0
    if fb and o["nat"]:
        F = _RE_F.findall(txt[fb[-1]:fb[-1] + 130 * (o["nat"] + 6)])
        o["final_forces_n"] = min(len(F), o["nat"])
        if len(F) >= o["nat"]:
            arr = np.array(F[:o["nat"]], float)
            o["final_forces_max_comp_RyBohr"] = float(np.abs(arr).max())
            o["max_force_eV_A"] = float(np.linalg.norm(arr, axis=1).max()) * RYBOHR_EVA
    Ps = [(mm.start(), float(mm.group(1))) for mm in _RE_P.finditer(txt)]
    o["P_kbar"] = Ps[-1][1] if Ps else None
    o["P_at"] = Ps[-1][0] if Ps else None
    o["spin_polarized"] = ("SPIN UP" in txt) or ("Starting magnetic structure" in txt)
    m = re.search(r"bfgs converged in\s+(\d+)\s+scf cycles and\s+(\d+)\s+bfgs steps", txt)
    o["bfgs"] = {"scf_cycles": int(m.group(1)), "steps": int(m.group(2))} if m else None
    m = re.search(r"\(criteria: energy <\s*([\d.Ee+-]+)\s*Ry, force <\s*([\d.Ee+-]+)\s*Ry/Bohr\)", txt)
    o["bfgs_criteria"] = [float(m.group(1)), float(m.group(2))] if m else None
    o["final_E_Ry"] = _num(r"Final energy\s+=\s+(-?\d+\.\d+)\s+Ry", txt)
    fin = None
    bb, ee = txt.rfind("Begin final coordinates"), txt.rfind("End final coordinates")
    if 0 <= bb < ee:
        blk = txt[bb:ee]
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


def kmesh_problems(o, mesh) -> list:
    """출력의 k 점 (2π/alat 직교 좌표 · 가중치) 이 요청한 Γ 포함 MP 격자 (shift 0) 를 정확히 한 번씩 덮는가 (Codex EF P1-3).

    분수 좌표 = k · a_i (a_i = 출력의 결정 축 · alat 단위). ① 모든 점이 격자 위 (1e-4 — 다른 격자의 출력은 여기서 걸린다) →
    ② 점마다 중복도 m = w·N/2 가 1 (그 점만) 또는 2 (k 와 −k — 시간 반전) → ③ 덮은 점들이 격자 전체를 정확히 한 번씩 ·
    가중치 합 2. nosym 이라 다른 대칭 축소는 없다 (있으면 거부 — 큰 소리).
    ⛔ 점 수가 '더 크다' 로 판정하지 않는다 — 3×2×1 출력은 4×2×1 격자를 덮지 못해 여기서 걸린다.
    """
    kl, ax = o.get("klist"), o.get("axes_alat")
    n = [int(x) for x in mesh]
    if not kl or ax is None:
        return [f"k 점 목록 · 결정 축을 못 읽었다 (요청 격자 {n} 를 확인할 수 없다)"]
    N = n[0] * n[1] * n[2]
    A = np.asarray(ax, float)
    pts, off = [], []
    for kx, ky, kz, w in kl:
        f = A @ np.array([kx, ky, kz])
        x = f * np.array(n, float)
        if np.abs(x - np.round(x)).max() > TOL["k_grid"]:
            off.append(np.round(f, 5).tolist())
            continue
        pts.append((tuple(int(round(v)) % ni for v, ni in zip(x, n)), w))
    if off:
        return [f"요청 격자 {n}: k 점 {len(off)}/{len(kl)} 개가 격자 위에 없다 (예: 분수 {off[0]}) — 다른 k 격자의 출력"]
    cover = Counter()
    wsum = 0.0
    for g, w in pts:
        gm = tuple((-x) % ni for x, ni in zip(g, n))
        m = w * N / 2.0
        if abs(m - round(m)) > TOL["k_weight"] or int(round(m)) not in (1, 2):
            return [f"요청 격자 {n}: k 점 {g} 가중치 {w} — 시간 반전만이면 2/{N} 또는 4/{N} 이어야 한다"]
        if int(round(m)) == 2 and g == gm:
            return [f"요청 격자 {n}: k 점 {g} 는 −k 와 같은데 가중치가 둘 몫이다 (대칭 축소 — nosym 이 아니다)"]
        for s_ in ({g} if int(round(m)) == 1 else {g, gm}):
            cover[s_] += 1
        wsum += w
    full = set(itertools.product(range(n[0]), range(n[1]), range(n[2])))
    if set(cover) != full or any(c != 1 for c in cover.values()) or abs(wsum - 2.0) > TOL["k_weight"] * N:
        return [f"요청 격자 {n}: k 점들이 {N} 점을 정확히 한 번씩 덮지 않는다 (덮음 {len(cover)} · 가중치 합 {wsum:.4f})"]
    return []


def out_problems(o, inp, *, stage, pp, V0=None) -> list:
    """출력 하나가 그 입력 (같은 폴더의 scf.in) · 계획한 설정의 **한 실행**의 완료 결과인가 → 문제 목록 (빈 목록 = 통과)."""
    q = []
    if o["decode_error"]:
        q.append(f"출력 바이트 손상 (utf-8 아님 · {o['decode_error']})")
    if o["n_runs"] != 1:
        q.append(f"한 출력에 실행이 {o['n_runs']} 개 (이어 붙임 · 재시작) — 한 실행의 출력만 받는다")
    if o["n_job_done"] != 1 or not o["job_done"]:
        q.append(f"JOB DONE {o['n_job_done']} 번 (한 번이어야 한다 · 안 끝났거나 섞였다)")
    many = {k: c for k, c in o["once"].items() if c != 1}
    if many:
        q.append(f"설정 줄이 한 번씩이 아니다 {many} (한 실행의 출력이 아니다 · 머리 없이 붙인 조각)")
    if o["after_done"]:
        q.append(f"JOB DONE 뒤에 계산 기록 {o['after_done'][:2]} (이어 붙임 — JOB DONE 은 마지막 실행의 끝이어야 한다)")
    if o["E_Ry"] is None:
        q.append("'!' 총에너지 없음")
    elif stage != "relax" and o["n_scf"] != 1:
        q.append(f"SCF 출력에 '!' 총에너지가 {o['n_scf']} 개 (한 번이어야 — 섞인 · 끼워 넣은 조각)")
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
    if sorted(got) != present or len(o["pp"]) != len(present):
        q.append(f"유사포텐셜 원소 {sorted(got)} ≠ {present}")
    for el in present:
        d, pl = got.get(el), pp.get(el) or {}
        if d and (d["file"] != PP[el] or d["md5"] != pl.get("md5")):
            q.append(f"유사포텐셜 {el}: {d['file']} · md5 {d['md5'][:8]} ≠ 계획 {PP[el]} · {str(pl.get('md5'))[:8]}")
        if d and (d["zval"] is None or pl.get("z_valence") is None or abs(d["zval"] - pl["z_valence"]) > TOL["zval"]):
            q.append(f"유사포텐셜 {el}: Zval {d['zval']} ≠ 계획 {pl.get('z_valence')}")
    zs = {el: (pp.get(el) or {}).get("z_valence") for el in present}
    if any(z is None for z in zs.values()):
        q.append("계획에 가전자 수 (z_valence) 가 없다 — 기대 전자 수를 못 낸다")
    else:
        cnt = Counter(inp["symbols"])
        expect = sum(cnt[el] * zs[el] for el in present) - DFT["tot_charge"]
        if o["nelec"] is None or abs(o["nelec"] - expect) > TOL["nelec"]:
            q.append(f"전자 수 {o['nelec']} ≠ 기대 {expect:g} (조성 × 가전자 · 총전하 {DFT['tot_charge']:g}) — 다른 전하 상태 · 다른 PP")
    cin = np.asarray(inp["cell"], float)
    if o["cell_A"] is None or np.abs(np.asarray(o["cell_A"]) - cin).max() > TOL["cell_A"]:
        q.append("출력의 셀 축이 입력 셀과 다르다")
    ini = o["initial"]
    if ini is None:
        q.append("출력의 처음 좌표 블록을 못 읽었다")
    elif ini["symbols"] != list(inp["symbols"]):
        q.append("출력의 처음 원소 순서가 입력과 다르다")
    elif np.abs(np.asarray(ini["cart_A"]) - np.asarray(inp["frac"], float) @ cin).max() > TOL["pos_A"]:
        q.append("출력의 처음 좌표가 입력 좌표와 다르다 (다른 잡의 출력?)")
    if o["prefixes"] and o["prefixes"] != [inp["keys"].get("prefix")]:
        q.append(f"출력의 prefix {o['prefixes']} ≠ 입력 {inp['keys'].get('prefix')}")
    if inp.get("k_shift") != [0, 0, 0]:
        q.append(f"입력 k shift {inp.get('k_shift')} ≠ 0 0 0")
    q += kmesh_problems(o, inp["k"])
    if (not o["forces_block"] or o["forces_at"] is None or o["E_last_at"] is None or o["forces_at"] < o["E_last_at"]
            or o["final_forces_max_comp_RyBohr"] is None):
        q.append("힘 블록이 마지막 SCF 뒤에 없다 (또는 원자 수만큼 못 읽었다)")
    if stage == "relax":
        R = DFT["relax"]
        many = {k: c for k, c in o["once_relax"].items() if c != 1}
        if many:
            q.append(f"이완 설정 줄이 한 번씩이 아니다 {many}")
        c = o["bfgs_criteria"]
        if (c is None or abs(c[0] / R["etot_conv_thr"] - 1) > TOL["conv_rel"]
                or abs(c[1] / R["forc_conv_thr"] - 1) > TOL["conv_rel"]):
            q.append(f"BFGS 기준 {c} ≠ 계약 [{R['etot_conv_thr']}, {R['forc_conv_thr']}] (느슨한 기준의 수렴을 받지 않는다)")
        if (o["etot_thr"] is None or abs(o["etot_thr"] / R["etot_conv_thr"] - 1) > TOL["conv_rel"]
                or o["forc_thr"] is None or abs(o["forc_thr"] / R["forc_conv_thr"] - 1) > TOL["conv_rel"]):
            q.append(f"출력 머리의 이완 문턱 ({o['etot_thr']}, {o['forc_thr']}) ≠ 계약")
        if o["nstep"] != R["nstep"]:
            q.append(f"nstep {o['nstep']} ≠ {R['nstep']}")
        fm = o["final_forces_max_comp_RyBohr"]
        if fm is not None and fm > R["forc_conv_thr"] + TOL["force_print"]:
            q.append(f"마지막 힘 성분 최대 {fm:.2e} Ry/Bohr > forc_conv_thr {R['forc_conv_thr']} (모든 성분 기준)")
        if o["bfgs"] is None:
            q.append("'bfgs converged' 없음 (nstep 소진 · 미수렴)")
        elif o["n_scf"] != o["bfgs"]["scf_cycles"]:
            q.append(f"'!' 총에너지 {o['n_scf']} 개 ≠ BFGS 가 센 SCF {o['bfgs']['scf_cycles']} 번 (끼워 넣은 · 빠진 조각)")
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


def _job_dirs(plan_dir, stage, job):
    d = Path(plan_dir) / stage / job
    return d, d / "scf.in", d / "scf.out"


def read_stage_outputs(plan_dir, jobs, *, stage, pp, V0=None):
    """단계 잡 전부 → {잡: 출력 dict} · 누락 · 실패를 모아 멈춘다 (누락 ≠ 실패 · 둘 다 판정에 안 넣는다)."""
    outs, missing, bad = {}, [], []
    for j in jobs:
        d, fin, fout = _job_dirs(plan_dir, stage, j["job"])
        if not fin.is_file() or _sha(fin) != j["input_sha256"]:
            bad.append(f"{j['job']}: 입력 scf.in 이 기록 뒤 바뀌었다 · 없다 (sha256)")
            continue
        if not fout.is_file():
            missing.append(j["job"])
            continue
        o = parse_pw_out(fout)
        q = out_problems(o, parse_pw_in(fin), stage=stage, pp=pp, V0=V0)
        if q:
            bad.append(f"{j['job']}: " + " · ".join(q[:3]))
        outs[j["job"]] = o
    if missing:
        raise SystemExit(f"⛔ {stage} 출력 누락 {len(missing)} 건 ({missing}) — 누락은 실패가 아니다 · 다 돌린 뒤 판독한다")
    if bad:
        raise SystemExit(f"⛔ {stage} 출력 결속 · 검사 실패 {len(bad)} 건 — 판독하지 않는다:\n  " + "\n  ".join(bad)
                         + f"\n  → 실패 출력을 보존해 옮긴 뒤 (b2o3_bo_dft.py reject … --stage {stage}) 같은 실행기로 다시 돌린다")
    vers = {o["version"] for o in outs.values()}
    if len(vers) != 1:
        raise SystemExit(f"⛔ {stage} 출력의 PWSCF 판이 갈린다 {sorted(vers, key=str)}")
    return outs


def reject_outputs(plan_dir, jobs, *, stage, pp, V0=None) -> list:
    """검사에 걸린 출력을 scf.out.rejected.N 으로 옮긴다 (지우지 않는다) → [(잡, 새 이름, 이유)] · 입력이 바뀐 잡은 손대지 않는다."""
    moved = []
    for j in jobs:
        d, fin, fout = _job_dirs(plan_dir, stage, j["job"])
        if not fout.is_file():
            continue
        if not fin.is_file() or _sha(fin) != j["input_sha256"]:
            moved.append((j["job"], None, ["입력이 기록과 달라 손대지 않았다"]))
            continue
        q = out_problems(parse_pw_out(fout), parse_pw_in(fin), stage=stage, pp=pp, V0=V0)
        if not q:
            continue
        n = 1
        while (d / f"scf.out.rejected.{n}").exists():
            n += 1
        dest = d / f"scf.out.rejected.{n}"
        fout.rename(dest)
        moved.append((j["job"], dest.name, q[:3]))
    return moved


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


def stage10(succ, eos, raw, res_dir, base):
    """10 단계 고르기 — DFT 승자–차저 ≥ 0.10 이면 이긴 가족의 UMA 어닐 최저 셋 · 아니면 가족마다 UMA 어닐 최저 하나.

    구조 경로는 계획 폴더 기준 {rel · sha256} (Codex EF P2-2) — 8 단계 결과 기록의 sha256 과 같아야 한다.
    """
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
        e = ((raw.get(s["name"]) or {}).get("outputs") or {}).get("post_relax") or {}
        p = (Path(res_dir) / e.get("rel", "")).resolve()
        if not e.get("sha256") or not p.is_file() or _sha(p) != e["sha256"]:
            raise SystemExit(f"⛔ 안정성 대상 {s['name']} 의 post_relax 가 8 단계 기록과 결속되지 않는다")
        s["post_relax"] = _entry(p, base)
    return {"rule": rule, "stability_targets": pick, "rel_base": "계획 폴더 (dft_plan.json 이 있는 곳)"}


# ───────────────────────── k 판 자격 (prepare · 다시 결속 공통 — Codex EF P1-2) ─────────────────────────
def _k_main_check(RD, k_main, after_entry, base, results_sha):
    """k_main 3×2×1 = 탐침 발동 판정 없음 · k_main 4×2×1 = 같은 8 단계 결과에서 나온 **발동한** 탐침 판정이 있고
    그 판정을 출력에서 다시 내도 발동이어야 한다. 그 밖의 k 는 없다."""
    k_main = list(k_main)
    if k_main == DFT["k_main"]:
        if after_entry:
            raise SystemExit("⛔ k_main 3×2×1 판에 탐침 판정 (after_kprobe) 이 붙어 있다 — 섞인 계획")
        return None
    if k_main != DFT["k_probe"]:
        raise SystemExit(f"⛔ k_main {k_main} — {DFT['k_main']} (기본) 또는 {DFT['k_probe']} (탐침 발동 뒤) 만")
    if not after_entry:
        raise SystemExit("⛔ k_main 4×2×1 은 탐침 발동 판정 (after_kprobe) 이 있을 때만 — 결과 전 규칙 (DU P1-5)")
    kp_path = _bound(after_entry, base, "탐침 발동 판정")
    kv = _load(kp_path, KIND_KP)
    if not kv.get("triggered"):
        raise SystemExit("⛔ after_kprobe 판정이 발동이 아니다 — 4×2×1 다시 계산의 근거가 없다")
    if (kv.get("stage8") or {}).get("anneal_results_sha256") != results_sha:
        raise SystemExit("⛔ after_kprobe 판정이 다른 8 단계 결과에서 나왔다")
    _rebind_kp(RD, kp_path, None)                # 발동 판정을 출력에서 다시 낸다 (손댄 '발동' 은 근거가 아니다)
    return kp_path


# ───────────────────────── 명령 ─────────────────────────
def prepare(RD, verdict, receipt, results, readout, pseudo_dir, out_dir, k_main=None, after_kprobe=None):
    out_dir = Path(out_dir)
    k_main = list(k_main or DFT["k_main"])
    if k_main not in (DFT["k_main"], DFT["k_probe"]):
        raise SystemExit(f"⛔ k_main {k_main} — {DFT['k_main']} (기본) 또는 {DFT['k_probe']} (탐침 발동 뒤) 만")
    if k_main == DFT["k_probe"] and not after_kprobe:
        raise SystemExit("⛔ k_main 4×2×1 은 탐침 발동 판정 (--after_kprobe) 이 있을 때만 — 결과 전 규칙 (DU P1-5)")
    if (out_dir / "dft_plan.json").exists():
        raise SystemExit(f"⛔ {out_dir}/dft_plan.json 가 이미 있다 — 덮지 않는다 (새 폴더)")
    A100, succ, raw, res_dir = stage8(RD, verdict, receipt, results, readout)
    after_entry = _entry(after_kprobe, out_dir) if after_kprobe else None
    _k_main_check(RD, k_main, after_entry, out_dir, _sha(results))
    ps = pseudo_record(pseudo_dir)
    jobs, texts = [], {}
    for s in select_sp(succ):
        p, a = _struct(RD, raw, res_dir, s["name"])
        job = _job("sp", s)
        t = pw_input_text(a, prefix=job, calc="scf", k=k_main, pseudo_dir=ps["dir"])
        texts[job] = t
        jobs.append({"job": job, "family": s["family"], "i": s["i"], "name": s["name"], "rank": s["rank"],
                     "E_uma_eV": s["E"], "structure": _entry(p, out_dir), "input_sha256": _text_sha(t),
                     "uma_record": coord_record(RD, a)})
    _write_jobs(out_dir, "sp", texts)
    plan = {"kind": KIND_PLAN, "card": "db/properties/b2o3_bo_placement_estimand_2026_11_09.json#개정_1 9_DFT · 개정_5",
            "tools": _tools(RD),
            "inputs": {"screen_verdict": _entry(verdict, out_dir), "pilot_receipt": _entry(receipt, out_dir),
                       "anneal_results": _entry(results, out_dir), "anneal_readout": _entry(readout, out_dir)},
            "after_kprobe": after_entry,
            "stage8": {"order": A100.get("order"), "winner": A100.get("winner"), "decision": A100.get("decision"),
                       "gap_eV": A100.get("winner_runner_up_gap_eV")},
            "contract": DFT, "pseudo": ps, "k_main": k_main, "jobs_sp": jobs,
            "rel_base": "잡 · 구조 · 입력의 rel 은 이 계획 폴더 기준"}
    _dump(plan, out_dir / "dft_plan.json")
    return plan


def _pp(plan):
    return plan["pseudo"]["files"]


def _rebind_plan(RD, plan_path):
    """계획을 다시 결속 — 도구 · 판독기 같음 · 계약 같음 · 묶인 입력 sha · 8 단계 다시 내기 · k 판 자격 · 고르기 다시 ·
    **구조를 8 단계 기록에서 다시 찾아 계획과 대조** · 유사포텐셜을 다시 기록해 대조 · 입력을 묶인 구조에서 다시 만들어 대조."""
    pp_ = Path(plan_path).resolve()
    plan = _load(pp_, KIND_PLAN)
    _same_tools(RD, plan, "계획")
    base = pp_.parent
    if plan.get("contract") != json.loads(json.dumps(DFT)):
        raise SystemExit("⛔ 계획의 계약 (contract) 이 이 도구의 값과 다르다")
    ins = {k: _bound(plan["inputs"].get(k), base, k) for k in ("screen_verdict", "pilot_receipt", "anneal_results",
                                                               "anneal_readout")}
    A100, succ, raw, res_dir = stage8(RD, ins["screen_verdict"], ins["pilot_receipt"], ins["anneal_results"],
                                      ins["anneal_readout"])
    _k_main_check(RD, plan.get("k_main") or [], plan.get("after_kprobe"), base, plan["inputs"]["anneal_results"]["sha256"])
    sel = select_sp(succ)
    want = [(s["family"], s["i"], s["name"], s["rank"]) for s in sel]
    got = [(j["family"], j["i"], j["name"], j["rank"]) for j in plan["jobs_sp"]]
    if want != got:
        raise SystemExit(f"⛔ 계획의 단일점 대상이 다시 고른 것과 다르다 ({got} ≠ {want}) — 손댄 계획은 쓰지 않는다")
    for j in plan["jobs_sp"]:
        p, _ = _struct(RD, raw, res_dir, j["name"])
        if _entry(p, base) != j["structure"]:
            raise SystemExit(f"⛔ {j['job']}: 계획의 구조가 8 단계 기록의 {j['name']} post_relax 와 다르다 (경로 · sha256)")
    if pseudo_record(plan["pseudo"]["dir"]) != plan["pseudo"]:
        raise SystemExit("⛔ 유사포텐셜 기록이 지금 파일과 다르다 (계획 뒤 바뀌었다) — 판독하지 않는다")
    exp = _expected_sp(plan, base)
    for j in plan["jobs_sp"]:
        if _text_sha(exp[j["job"]]) != j["input_sha256"]:
            raise SystemExit(f"⛔ {j['job']}: 계획의 입력 sha256 이 묶인 구조에서 다시 만든 입력과 다르다")
    return plan, base, A100, succ, raw, res_dir


def _expected_sp(plan, base):
    from ase.io import read
    out = {}
    for j in plan["jobs_sp"]:
        a = read(str(_bound(j["structure"], base, f"{j['job']} 구조")))
        out[j["job"]] = pw_input_text(a, prefix=j["job"], calc="scf", k=plan["k_main"], pseudo_dir=plan["pseudo"]["dir"])
    return out


def _expected_kprobe(plan, base, reps):
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
    from ase.io import read
    if host is None:
        raise SystemExit("⛔ 이완 입력을 만들거나 대조하려면 --host (modelc_V0_k663.xyz) 가 필요하다")
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
    """잡 입력을 쓴다 — 이미 있으면 같은 바이트일 때만 둔다 (다르면 멈춤 · 덮지 않는다)."""
    for job, t in texts.items():
        f = Path(base) / stage / job / "scf.in"
        if f.exists():
            if f.read_bytes() != t.encode("utf-8"):
                raise SystemExit(f"⛔ {f} 가 이미 있고 다시 만든 입력과 다르다 — 덮지 않는다")
            continue
        _write_bytes(f, t)


def _sp_rows(plan, base, outs):
    rows = []
    for j in plan["jobs_sp"]:
        o = outs[j["job"]]
        rows.append({"job": j["job"], "family": j["family"], "i": j["i"], "name": j["name"], "rank": j["rank"],
                     "E_eV": o["E_Ry"] * RY_EV, "max_force_eV_A": o["max_force_eV_A"], "nk": o["nk"],
                     "output": _entry(o["path"], base), "wall": o["wall"], "gpu": o["gpu"]})
    rep = {}
    for F in FAM:
        rep[F] = sorted((r for r in rows if r["family"] == F), key=lambda r: (r["E_eV"], r["i"]))[0]
    return rows, rep


def _build_sp_verdict(RD, plan, base, plan_path, vdir, host):
    """단일점 판정 (파일은 안 쓴다) → (판정, 다음 단계 이름, 다음 잡 입력 텍스트, 가족 대표 잡)."""
    outs = read_stage_outputs(base, plan["jobs_sp"], stage="sp", pp=_pp(plan))
    rows, rep = _sp_rows(plan, base, outs)
    order, gap, dec = family_order({F: rep[F]["E_eV"] for F in FAM})
    uma = plan["stage8"]["order"]
    v = {"kind": KIND_SP, "tools": _tools(RD), "plan": _entry(plan_path, vdir),
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
        v["next"] = "run_force_check_scf.sh <계획 폴더>/kprobe → read_kprobe"
        return v, "kprobe", texts, reps
    v["jobs_relax"], texts, v["reference_cell"] = _expected_relax(plan, base, reps, host)
    v["next"] = "run_force_check_scf.sh <계획 폴더>/relax → read_relax --prev <이 파일>"
    return v, "relax", texts, reps


def read_sp(RD, plan_path, out, host=None):
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    plan, base, A100, succ, raw, res_dir = _rebind_plan(RD, plan_path)
    v, stage, texts, _ = _build_sp_verdict(RD, plan, base, Path(plan_path).resolve(), Path(out).resolve().parent, host)
    _write_jobs(base, stage, texts)
    _dump(v, out)
    return v


def _rebind_sp(RD, sp_path, host=None):
    """단일점 판정을 **통째로** 다시 낸다 (계획 · 8 단계 · 단일점 출력 · 다음 잡 입력) → 저장된 판정과 같아야 (Codex EF P2-1)."""
    sp_path = Path(sp_path).resolve()
    v = _load(sp_path, KIND_SP)
    _same_tools(RD, v, "단일점 판정")
    plan_path = _bound(v["plan"], sp_path.parent, "계획")
    plan, base, A100, succ, raw, res_dir = _rebind_plan(RD, plan_path)
    v_new, _, _, reps = _build_sp_verdict(RD, plan, base, plan_path, sp_path.parent, host)
    if _norm_v(v_new) != _norm_v(v):
        raise SystemExit("⛔ 단일점 판정이 계획 · 출력에서 다시 낸 판정과 다르다 (행 · 대표 · 순서 · 문장 · 다음 잡 중 하나) — "
                         "바뀐 판정은 쓰지 않는다")
    return v, plan, base, A100, succ, raw, res_dir, reps


def _kprobe_core(v, plan, base):
    outs = read_stage_outputs(base, v["jobs_kprobe"], stage="kprobe", pp=_pp(plan))
    E1 = {F: next(r["E_eV"] for r in v["rows"] if r["job"] == v["representatives"][F]) for F in FAM}
    E2 = {j["family"]: outs[j["job"]]["E_Ry"] * RY_EV for j in v["jobs_kprobe"]}
    why = kprobe_trigger(E1, E2)
    pairs = {f"{G}-{F}": {"k_main": E1[G] - E1[F], "k_probe": E2[G] - E2[F], "change": (E2[G] - E2[F]) - (E1[G] - E1[F])}
             for F, G in itertools.combinations(FAM, 2)}
    return outs, why, pairs


def _build_kp_verdict(RD, v, plan, base, reps, sp_path, vdir, host, core=None):
    outs, why, pairs = core or _kprobe_core(v, plan, base)
    kv = {"kind": KIND_KP, "tools": _tools(RD), "sp_verdict": _entry(sp_path, vdir),
          "stage8": {"anneal_results_sha256": plan["inputs"]["anneal_results"]["sha256"]},
          "k_main": plan["k_main"], "k_probe": DFT["k_probe"], "pairs": pairs,
          "outputs": {j["job"]: _entry(outs[j["job"]]["path"], base) for j in v["jobs_kprobe"]},
          "nk": {"k_main": v["rows"][0]["nk"], "k_probe": next(iter(outs.values()))["nk"]},
          "triggered": bool(why), "why": why}
    texts = {}
    if why:
        kv["next"] = ("⛔ 발동 — 6 단일점을 4×2×1 로 다시 (새 폴더: prepare --k_main 4 2 1 --after_kprobe <이 파일>) · "
                      "안 할 거면 사용자 명시 결정으로 닫는다 (결정 원장 · 이유 · 한계)")
    else:
        kv["jobs_relax"], texts, kv["reference_cell"] = _expected_relax(plan, base, reps, host)
        kv["next"] = "run_force_check_scf.sh <계획 폴더>/relax → read_relax --prev <이 파일>"
    return kv, texts


def read_kprobe(RD, sp_path, out, host):
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    sp_path = Path(sp_path).resolve()
    v, plan, base, A100, succ, raw, res_dir, reps = _rebind_sp(RD, sp_path)
    if plan["k_main"] != DFT["k_main"]:
        raise SystemExit("⛔ 이 단일점 판정에는 k 탐침이 없다 (k_main 4×2×1 판) — read_relax 로 간다")
    kv, texts = _build_kp_verdict(RD, v, plan, base, reps, sp_path, Path(out).resolve().parent, host)
    _write_jobs(base, "relax", texts)
    _dump(kv, out)
    return kv


def _rebind_kp(RD, kp_path, host):
    """탐침 판정을 다시 낸다 — 먼저 발동 판정 · 쌍만 (host 없이도) · 그다음 판정 통째로 (출력 sha · k 점 수 · 이완 잡)."""
    kp_path = Path(kp_path).resolve()
    kv = _load(kp_path, KIND_KP)
    _same_tools(RD, kv, "탐침 판정")
    sp_path = _bound(kv["sp_verdict"], kp_path.parent, "단일점 판정")
    v, plan, base, A100, succ, raw, res_dir, reps = _rebind_sp(RD, sp_path)
    core = _kprobe_core(v, plan, base)
    _, why, pairs = core
    if bool(why) != bool(kv.get("triggered")) or why != kv.get("why") or json.loads(json.dumps(pairs)) != kv.get("pairs"):
        raise SystemExit("⛔ 탐침 판정이 출력에서 다시 낸 발동 판정과 다르다 — 바뀐 판정은 쓰지 않는다")
    if why or host is not None:
        kv_new, _ = _build_kp_verdict(RD, v, plan, base, reps, sp_path, kp_path.parent, host, core=core)
        if _norm_v(kv_new) != _norm_v(kv):
            raise SystemExit("⛔ 탐침 판정이 다시 낸 판정과 다르다 (출력 sha · k 점 수 · 이완 잡 · 기준 셀 중 하나) — 쓰지 않는다")
    return kv, v, plan, base, A100, succ, raw, res_dir


def read_relax(RD, prev_path, out, host):
    from ase import Atoms
    if Path(out).exists():
        raise SystemExit(f"⛔ {out} 가 이미 있다 — 덮지 않는다")
    prev_path = Path(prev_path).resolve()
    kind = json.loads(prev_path.read_bytes().decode("utf-8")).get("kind")
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
    outs = read_stage_outputs(base, jobs, stage="relax", pp=_pp(plan), V0=V0)
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
                     "bfgs": o["bfgs"], "final_force_max_comp_RyBohr": o["final_forces_max_comp_RyBohr"],
                     "output": _entry(o["path"], base), "wall": o["wall"]})
    eos = RD.eos_robust(fam)
    if eos["baseline_order"] != family_order({F: fam[F][0] for F in FAM})[0]:
        raise SystemExit("⛔ 판 고정 eos_robust 의 기준 순서가 이 도구의 순서와 다르다")
    gaps = [c["gap"] for c in eos["corners"]]
    rv = {"kind": KIND_RX, "tools": _tools(RD), "prev": _entry(prev_path, Path(out).resolve().parent),
          "k_main": plan["k_main"], "reference_cell": cell_rec, "rows": rows,
          "eos_input": {F: {"E_eV": fam[F][0], "P_GPa": fam[F][1], "V_A3": fam[F][2],
                            "output": next(r["output"] for r in rows if r["family"] == F)} for F in FAM},
          "eos": eos, "corrected_gap_range_eV": [min(gaps), max(gaps)], "relaxed": relaxed,
          "scope": ("사전 규칙으로 고른 가족 대표 구조를 공통 기준 셀 (host 모양 · V₀) 에서 이온 이완한 에너지 비교 — "
                    "이 수렴 설정 (forc 1e-3 Ry/Bohr · etot 1e-5 Ry · nstep 200) 조건부 · 가족 전체 DFT 최저 · 자유 셀 바닥상태 아님 · "
                    "0.10 eV 는 판정 여유 (인증된 정확도 아님)"),
          "rel_base": "rows · relaxed · 대상의 rel 은 계획 폴더 기준 · prev 는 이 판정 폴더 기준"}
    if eos["skip_eos"]:
        d = eos["baseline_decision"]
        rv["decision"] = (f"DFT 이온 이완 (고정 기준 셀 · 보정 전) 최저 {d['lowest']} · 승자–차저 {eos['baseline_gap']:.3f} "
                          + ("≥" if d["gap_ge_margin"] else "<") + f" {d['margin']} — 압력 보정 범위 전체에서 순서 · 판정 그대로 (EOS 생략)")
        rv["stage10"] = stage10(succ, eos, raw, res_dir, base)
        rv["electronic_targets"] = [{"family": F, **relaxed[F]["file"], "parent_structure": relaxed[F]["parent_structure"]}
                                    for F in FAM]
    else:
        why = [f"{F}: |P| {abs(fam[F][1]):.2f} > {DFT['P_max_GPa']} GPa" for F in FAM if abs(fam[F][1]) > DFT["P_max_GPa"]]
        if not eos["robust_independent_B"]:
            why.append("B 조합 중 순서 · 0.10 판정이 바뀌는 것이 있다")
        rv["decision"] = "EOS 필요 — " + " · ".join(why) + " (고르기 안 함 · 그 셀만 EOS — 다음 판)"
        rv["stage10"] = None
        rv["electronic_targets"] = None          # Codex EF P1-6 — EOS 보류면 실행 대상 없음 (이완 구조는 relaxed 에 진단 자료로만)
        rv["relaxed_note"] = "EOS 보류 — relaxed 는 진단 자료 · 안정성 · 전자구조 실행 대상이 아니다"
    _dump(rv, out)
    return rv


def write_relaxed(path, atoms) -> Path:
    """이완 끝 구조 (extxyz · LF) — 이미 있으면 같은 바이트일 때만 둔다 (다르면 멈춤 · 앞 판정의 구조를 덮지 않는다)."""
    from ase.io import write
    import io
    buf = io.StringIO()
    write(buf, atoms, format="extxyz")
    p = Path(path)
    if p.exists() and p.read_bytes() != buf.getvalue().encode("utf-8"):
        raise SystemExit(f"⛔ {p} 가 이미 있고 이번 이완 출력에서 만든 구조와 다르다 — 덮지 않는다 (앞 판정 · 출력을 먼저 확인)")
    return _write_bytes(p, buf.getvalue())


# ───────────────────────── reject 의 잡 목록 ─────────────────────────
def _jobs_for_reject(plan_path, stage, verdict=None):
    """reject 대상 잡 — sp 는 계획에서 · kprobe · relax 는 그 잡 목록을 가진 판정 파일에서 (판정 → 계획 고리가 이 계획이어야)."""
    plan_path = Path(plan_path).resolve()
    plan = _load(plan_path, KIND_PLAN)
    if ((plan.get("tools") or {}).get("dft_tool") or {}).get("sha256") != _tool_fp()["sha256"]:
        raise SystemExit("⛔ 이 도구 sha256 이 계획을 만든 판과 다르다 — 같은 판으로만 거부 · 판독한다")
    if stage == "sp":
        return plan, plan["jobs_sp"]
    if not verdict:
        raise SystemExit("⛔ --stage kprobe · relax 는 잡 목록이 든 판정 파일 (--verdict) 이 필요하다")
    vp = Path(verdict).resolve()
    d = json.loads(vp.read_bytes().decode("utf-8"))
    key = {"kprobe": "jobs_kprobe", "relax": "jobs_relax"}[stage]
    if not d.get(key):
        raise SystemExit(f"⛔ {vp.name} 에 {key} 가 없다")
    p, cur = vp, d
    if cur.get("kind") == KIND_KP:
        p = _bound(cur.get("sp_verdict"), p.parent, "단일점 판정")
        cur = _load(p, KIND_SP)
    if cur.get("kind") != KIND_SP:
        raise SystemExit(f"⛔ {vp.name} 는 단일점 · 탐침 판정이 아니다 ({d.get('kind')})")
    if _bound(cur.get("plan"), p.parent, "계획") != plan_path:
        raise SystemExit("⛔ 판정 파일이 이 계획에서 나온 것이 아니다 — 남의 잡을 옮기지 않는다")
    return plan, d[key]


# ───────────────────────── selftest ─────────────────────────
ZV_TEST = {"Li": 3.0, "B": 3.0, "O": 6.0, "P": 5.0, "S": 6.0, "Cl": 7.0}


def _kpts_tr(mesh):
    """selftest — Γ 포함 MP 격자 (shift 0) 를 시간 반전으로만 줄인 [(분수 좌표, 가중치)] — QE nosym 출력과 같은 꼴 (가중치 합 2)."""
    n = [int(x) for x in mesh]
    N = n[0] * n[1] * n[2]
    seen, out = set(), []
    for g in itertools.product(range(n[0]), range(n[1]), range(n[2])):
        if g in seen:
            continue
        gm = tuple((-x) % ni for x, ni in zip(g, n))
        seen |= {g, gm}
        out.append((np.array(g, float) / np.array(n, float), (2.0 if g == gm else 4.0) / N))
    return out


def _fake_out(inp_path, *, E_list, stage="sp", pp=None, mesh=None, kpts=None, ecut=52.0, conv="1.0E-08",
              smear="Gaussian", width="0.0100", xc="SLA  PW   PBX  PBC", job_done=True, not_conv=False, spin=False,
              shift_pos=0.0, P_kbar=None, P_before_last=False, bfgs=True, final_E=None, final=True, version="7.4.1",
              input_name="scf.in", vol_override=None, drop_forces=False, prefix=None, final_symbols=None, nelec=None,
              zval_over=None, crit=("1.0E-05", "1.0E-03"), hdr_thr=("1.0E-05", "1.0E-03"), nstep=200, force_last=None,
              append_run=None, tail_junk=None, axes_eps=0.0, bfgs_cycles=None):
    """이 도구가 읽는 줄만 QE 7.4.1 꼴로 흉내 낸 출력 (줄 모양은 db/raw 의 실제 7.4.1 출력 — li2s_neb_cellconv ·
    ndo_site_eos (nosym relax) — 으로 맞췄다). k 점은 입력 격자 (또는 mesh · kpts) 를 시간 반전으로만 줄여 2π/alat 직교 좌표로 찍는다."""
    inp = parse_pw_in(inp_path)
    cell = inp["cell"]
    alat = float(np.linalg.norm(cell[0])) / BOHR_A
    A = cell / (alat * BOHR_A)
    cart = inp["frac"] @ cell
    vol = (vol_override if vol_override is not None else abs(np.linalg.det(cell))) / BOHR_A ** 3
    pre = prefix or inp["keys"]["prefix"]
    pp = pp or {}
    present = [e for e in SPECIES if e in set(inp["symbols"])]
    zv = {el: (zval_over or {}).get(el, (pp.get(el) or {}).get("z_valence", ZV_TEST[el])) for el in present}
    ne = sum(inp["symbols"].count(el) * (pp.get(el) or {}).get("z_valence", ZV_TEST[el]) for el in present)
    ne = ne if nelec is None else nelec
    L = [f"     Program PWSCF v.{version} starts on 13Nov2026 at 23:50:33 ", "",
         f"     Reading input from {input_name}", "",
         f"     lattice parameter (alat)  =      {alat:.4f}  a.u.",
         f"     unit-cell volume          =    {vol:.4f} (a.u.)^3",
         f"     number of atoms/cell      =           {len(inp['symbols'])}"]
    if ne != "missing":
        L.append(f"     number of electrons       =       {ne:.2f}")
    L += [f"     kinetic-energy cutoff     =      {ecut:.4f}  Ry",
          f"     charge density cutoff     =     {DFT['ecutrho']:.4f}  Ry",
          f"     scf convergence threshold =      {conv}"]
    if stage == "relax":
        L += [f"     energy convergence thresh.=      {hdr_thr[0]}", f"     force convergence thresh. =      {hdr_thr[1]}"]
    L += [f"     Exchange-correlation=  {xc}", "                           (   1   4   3   4   0   0   0)"]
    if stage == "relax":
        L.append(f"     nstep                     =          {nstep}")
    L += ["", "     GPU acceleration is ACTIVE.  1 visible GPUs per MPI rank", "",
          f"     celldm(1)=  {alat:.6f}  celldm(2)=   0.000000  celldm(3)=   0.000000", "",
          "     crystal axes: (cart. coord. in units of alat)"]
    Ap = A.copy()
    Ap[2, 2] += axes_eps                      # 셀 축만 다른 출력 (selftest)
    for n, row in enumerate(Ap, 1):
        L.append(f"               a({n}) = (  {row[0]:.6f}  {row[1]:.6f}  {row[2]:.6f} )  ")
    L.append("")
    for n, el in enumerate(present, 1):
        L += [f"     PseudoPot. # {n} for {el:<2} read from file:", f"     /data/work/pseudo/{PP[el]}",
              f"     MD5 check sum: {(pp.get(el) or {}).get('md5', '0' * 32)}",
              f"     Pseudo is Ultrasoft, Zval = {zv[el]:4.1f}", ""]
    if spin:
        L.append("     Starting magnetic structure ")
    L += ["   Cartesian axes", "", "     site n.     atom                  positions (alat units)"]
    for n, (s, x) in enumerate(zip(inp["symbols"], cart), 1):
        t = (x + shift_pos) / (alat * BOHR_A)
        L.append(f"        {n}           {s}  tau(   {n}) = (   {t[0]:.7f}   {t[1]:.7f}   {t[2]:.7f}  )")
    kl = kpts if kpts is not None else _kpts_tr(mesh or inp["k"])
    Ainv_T = np.linalg.inv(A).T
    L += ["", f"     number of k points=     {len(kl)}  {smear} smearing, width (Ry)=  {width}",
          "                       cart. coord. in units 2pi/alat"]
    for n, (f, w) in enumerate(kl, 1):
        k = np.asarray(f, float) @ Ainv_T
        L.append(f"        k({n:5d}) = ( {k[0]:11.7f} {k[1]:11.7f} {k[2]:11.7f}), wk = {w:11.7f}")
    L.append("")

    def scf_block(E, with_p, last):
        b = ["     convergence NOT achieved after 200 iterations: stopping" if not_conv else
             "     convergence has been achieved in  12 iterations", "",
             f"!    total energy              =    {E / RY_EV:.8f} Ry", ""]
        if not drop_forces:
            b += ["     Forces acting on atoms (cartesian axes, Ry/au):", ""]
            for n in range(1, len(inp["symbols"]) + 1):
                fx = force_last if (last and n == 1 and force_last is not None) else 0.0001
                b.append(f"     atom {n:4d} type  1   force = {fx:14.8f}    0.00020000   -0.00030000")
            b += ["     Total force =     0.001144     Total SCF correction =     0.000012", ""]
        if with_p and P_kbar is not None:
            b += [f"          total   stress  (Ry/bohr**3)                   (kbar)     P=      {P_kbar:8.2f}",
                  "   0.00001392   0.00000588  -0.00001346            2.05        0.87       -1.98", ""]
        return b
    for n, E in enumerate(E_list):
        last = n == len(E_list) - 1
        L += scf_block(E, (last and not P_before_last) or (P_before_last and n == len(E_list) - 2), last)
    if stage == "relax":
        if bfgs:
            nc = len(E_list) if bfgs_cycles is None else bfgs_cycles
            L += [f"     bfgs converged in  {nc} scf cycles and  {nc - 1} bfgs steps",
                  f"     (criteria: energy <  {crit[0]} Ry, force <  {crit[1]} Ry/Bohr)", "",
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
    L += ["=------------------------------------------------------------------------------=",
          "Warning: ieee_invalid is signaling", "Warning: ieee_divide_by_zero is signaling"]
    txt = "\n".join(L) + "\n"
    if tail_junk:
        txt += tail_junk
    if append_run is not None:
        txt += append_run
    return txt


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


def _write_fake_pp(pdir, el, *, z=None, elem=None, extra=""):
    """UPF 머리 가짜 — GBRV (Li · S · Cl) 는 UPF v1 줄 꼴 · psl (B · O · P) 는 v2 속성 꼴 (실제 파일 머리와 같은 꼴)."""
    z = ZV_TEST[el] if z is None else z
    e = elem or el
    if el in ("Li", "S", "Cl"):
        t = ("<PP_INFO>\n</PP_INFO>\n<PP_HEADER>\n   0                   Version Number\n"
             f"  {e:<2}                   Element\n   US                  Ultrasoft pseudopotential\n"
             "    T                  Nonlinear Core Correction\n SLA  PW   PBX  PBC    PBE  Exchange-Correlation functional\n"
             f"    {z:.11f}      Z valence\n</PP_HEADER>\n")
    else:
        t = (f'<UPF version="2.0.1">\n<PP_HEADER generated="x" element="{e:>2}" pseudo_type="PAW" '
             f'z_valence="{z:.15E}" />\n')
    (Path(pdir) / PP[el]).write_bytes((t + extra).encode("utf-8"))


def _selftest() -> int:
    import shutil
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
            if kw in str(ex):
                return True
            print(f"     (다른 이유로 멈춤: {str(ex)[:160]})")
            return False
        except Exception as ex:                       # 거부가 아니라 터진 것 — 빨간불
            print(f"     (터짐: {type(ex).__name__}: {ex})")
            return False
        return False

    real = load_rd()
    check_rd(real, pinned=False)
    chk(real.__dft_sha256__ == PINNED_RD_SHA256 or True, f"[정보] 이 저장소 판독기 sha256 {real.__dft_sha256__[:12]}…")
    host = HERE.parent.parent / "db" / "structures" / "modelc_V0_k663.xyz"
    chk(host.is_file() and _sha(host) == HOST_SHA256, "[양성] host modelc_V0_k663.xyz sha256 = 카드 값")

    # ── k 격자 검사 단위 시험 (EF P1-3) ──
    Ax = np.diag([1.0, 2.0, 1.27])
    Ainv_T = np.linalg.inv(Ax).T

    def ko(lst):
        return {"klist": [list(np.asarray(f, float) @ Ainv_T) + [w] for f, w in lst], "axes_alat": Ax.tolist()}

    chk(kmesh_problems(ko(_kpts_tr([3, 2, 1])), [3, 2, 1]) == [] and len(_kpts_tr([3, 2, 1])) == 4
        and len(_kpts_tr([4, 2, 1])) == 6, "[양성] k 격자 — 3×2×1 (시간 반전만 · 4 점) · 4×2×1 (6 점) 이 요청 격자를 정확히 덮음")
    full = [(np.array(g, float) / [3, 2, 1], 2.0 / 6) for g in itertools.product(range(3), range(2), range(1))]
    chk(kmesh_problems(ko(full), [3, 2, 1]) == [], "[양성] k 격자 — 줄이지 않은 목록 (noinv 꼴 · 6 점) 도 정확히 덮으면 통과")
    chk(any("위에 없다" in w for w in kmesh_problems(ko(_kpts_tr([3, 2, 1])), [4, 2, 1])),
        "[음성] k 격자 — 3×2×1 출력을 4×2×1 요청으로 읽으면 거부 (점이 격자 밖)")
    chk(any("위에 없다" in w for w in kmesh_problems(ko(_kpts_tr([4, 2, 1])), [3, 2, 1])),
        "[음성] k 격자 — 4×2×1 출력을 3×2×1 요청으로 읽으면 거부")
    sh = [((np.array(g, float) + 0.5) / [3, 2, 1], 2.0 / 6) for g in itertools.product(range(3), range(2), range(1))]
    chk(any("위에 없다" in w for w in kmesh_problems(ko(sh), [3, 2, 1])), "[음성] k 격자 — 반 칸 밀린 (shift) 격자는 거부")
    chk(any("정확히 한 번씩" in w for w in kmesh_problems(ko(_kpts_tr([3, 2, 1])[:-1]), [3, 2, 1])),
        "[음성] k 격자 — 점 하나 빠지면 거부")
    bw = [(f, (w if i else w * 1.5)) for i, (f, w) in enumerate(_kpts_tr([3, 2, 1]))]
    chk(any("이어야 한다" in w for w in kmesh_problems(ko(bw), [3, 2, 1])),
        "[음성] k 격자 — 가중치가 격자 몫 (2/N · 4/N) 이 아니면 거부")
    bw2 = [(f, (w * 1.25 if i == 1 else w)) for i, (f, w) in enumerate(_kpts_tr([3, 2, 1]))]
    chk(any("이어야 한다" in w for w in kmesh_problems(ko(bw2), [3, 2, 1])),
        "[음성] k 격자 — 짝 점의 가중치가 5/6 (몫 2.5) 이면 거부 (반올림으로 짝 몫이 되지 않는다)")
    sy = [(f, w) for f, w in _kpts_tr([4, 2, 1]) if not np.allclose(f, [0.5, 0, 0])]
    sy[0] = (sy[0][0], 4.0 / 8)
    chk(any("−k 와 같은데" in w for w in kmesh_problems(ko(sy), [4, 2, 1])),
        "[음성] k 격자 — 대칭으로 줄인 목록 (자기 짝 점에 둘 몫 가중치) 은 거부 (nosym 이어야)")
    chk(any("−k 와 같은데" in w or "정확히" in w for w in
            kmesh_problems(ko([(np.array(g, float) / 2, 0.5) for g in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]]), [4, 2, 1])),
        "[음성] k 격자 — 더 성긴 격자 (2×2×1) 의 점이 4×2×1 위에 있어도 덮음 · 가중치로 거부")
    chk(kmesh_problems({"klist": None, "axes_alat": None}, [3, 2, 1]) != [], "[음성] k 점 목록을 못 읽으면 거부")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # ── 유사포텐셜 가짜 (원소 머리 · 가전자) ──
        pdir = td / "pseudo"
        pdir.mkdir()
        for el in PP:
            _write_fake_pp(pdir, el)
        ps = pseudo_record(pdir)
        chk(sorted(ps["files"]) == sorted(SPECIES) and {el: d["z_valence"] for el, d in ps["files"].items()} == ZV_TEST,
            "[양성] 유사포텐셜 여섯 · 원소 머리 · 가전자 (UPF v1 줄 · v2 속성) · sha256 · md5 기록")
        _write_fake_pp(pdir, "B", elem="Al")
        chk(refuses("원소 머리", pseudo_record, pdir), "[음성] 유사포텐셜 원소 머리가 다르면 멈춘다")
        _write_fake_pp(pdir, "B")
        (pdir / PP["S"]).write_bytes((pdir / PP["S"]).read_bytes().replace(b"Z valence", b"Z valenc"))
        chk(refuses("가전자 수", pseudo_record, pdir), "[음성] 가전자 수를 못 읽으면 멈춘다 (기대 전자 수를 못 낸다)")
        _write_fake_pp(pdir, "S")
        os.remove(pdir / PP["Cl"])
        chk(refuses("없음", pseudo_record, pdir), "[음성] 유사포텐셜 파일이 없으면 멈춘다")
        _write_fake_pp(pdir, "Cl")
        ps = pseudo_record(pdir)
        PPR = ps["files"]

        # ── 128 원자 가짜 구조 (host 1×2×5 + 조성) ──
        h = read(str(host)).repeat((1, 2, 1))
        rng = np.random.default_rng(7)
        sy_ = h.get_chemical_symbols()
        iP = [i for i, s in enumerate(sy_) if s == "P"][:2]
        iS = [i for i, s in enumerate(sy_) if s == "S"][:3]
        for i in iP:
            sy_[i] = "B"
        for i in iS:
            sy_[i] = "O"
        frac = list(h.get_scaled_positions())
        sy_ += ["Li"] * 4
        frac += [list(rng.random(3)) for _ in range(4)]
        base_atoms = Atoms(sy_, scaled_positions=np.array(frac), cell=h.cell, pbc=True)
        chk(len(base_atoms) == 128 and dict(sorted(Counter(sy_).items())) == DFT["composition"],
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
                sh_ = _sha(d / "post_relax.xyz")
                plan8.append({"name": name, "rank": rank, "family": F, "start": {"sha256": "x"}})
                recs[name] = {"ok": True, "E": E, "atoms": a}
                raw.append({"name": name, "outputs": {"post_relax": {"rel": f"{name}/post_relax.xyz", "sha256": sh_}}})
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
        V, RC, RO = td / "verdict.json", td / "receipt.json", ro

        # ── prepare ──
        out = td / "s9"
        plan = prepare(RD, V, RC, res, RO, pdir, out)
        P = out / "dft_plan.json"
        jn = [j["job"] for j in plan["jobs_sp"]]
        chk(len(jn) == 6 and [j["family"] for j in plan["jobs_sp"]] == ["F_B", "F_B", "F_P", "F_P", "F_free", "F_free"]
            and plan["jobs_sp"][0]["name"].startswith("cfg0003") and plan["jobs_sp"][1]["name"].startswith("cfg0005"),
            f"[양성] prepare — 가족마다 UMA 최저 둘 (6) · 순서 {jn[:2]}")
        pin = parse_pw_in(out / "sp" / jn[0] / "scf.in")
        a0 = read(str(rdir / plan["jobs_sp"][0]["name"] / "post_relax.xyz"))
        chk(np.abs(pin["cell"] - a0.cell.array).max() < 1e-8 and np.abs(pin["frac"] @ pin["cell"] - a0.positions).max() < 1e-7
            and pin["symbols"] == a0.get_chemical_symbols() and pin["k"] == [3, 2, 1] and pin["k_shift"] == [0, 0, 0]
            and pin["keys"]["ecutwfc"] == "52.0" and pin["keys"]["conv_thr"] == "1.0d-8" and pin["keys"]["smearing"] == "gaussian"
            and pin["keys"]["nosym"] == ".true." and pin["keys"]["tot_charge"] == "0.0",
            "[양성] 단일점 입력 = UMA 이완 기하 그대로 (셀 · 좌표 · 원자 순서) · k 3×2×1 · 52/520 · 1.0d-8 · gaussian · nosym · 총전하 0")
        chk(plan["jobs_sp"][0]["structure"]["rel"] == os.path.relpath(rdir / plan["jobs_sp"][0]["name"] / "post_relax.xyz", out)
            and plan["rel_base"].startswith("잡"), "[양성] 계획의 구조 경로 = 계획 폴더 기준 (rel_base 명시)")
        chk(refuses("이미 있다", prepare, RD, V, RC, res, RO, pdir, out), "[음성] 계획이 있는 폴더에 다시 prepare → 덮지 않는다")
        A_bad = json.loads(json.dumps(A100))
        A_bad["hold_reasons"] = ["F_free: G1 실패"]
        ro2 = td / "ro_hold.json"
        ro2.write_text(json.dumps(A_bad))
        chk(refuses("보류", prepare, _FakeRD(real, A_bad, plan8, recs, res), V, RC, res, ro2, pdir, td / "s9_hold"),
            "[음성] 8 단계 본 판독이 보류면 DFT 대상을 고르지 않는다")
        A_mm = json.loads(json.dumps(A100))
        A_mm["families"]["F_P"]["min"]["name"] = "cfg9999"
        ro3 = td / "ro_mm.json"
        ro3.write_text(json.dumps(A_mm))
        chk(refuses("성공 목록", prepare, _FakeRD(real, A_mm, plan8, recs, res), V, RC, res, ro3, pdir, td / "s9_mm"),
            "[음성] 성공 목록의 최저가 본 판독과 다르면 멈춘다 (성공 정의가 갈림)")
        ro4 = td / "ro_edit.json"
        ro4.write_text(json.dumps({**A100, "winner": "F_P"}))
        chk(refuses("다시 낸 본 판독", prepare, RD, V, RC, res, ro4, pdir, td / "s9_e"), "[음성] 본 판독 파일을 손대면 (승자 바꿈) 멈춘다")
        chk(refuses("탐침 발동 판정", prepare, RD, V, RC, res, RO, pdir, td / "s9_k", k_main=[4, 2, 1]),
            "[음성] k_main 4×2×1 은 탐침 발동 판정 없이는 안 된다 (prepare)")
        chk(refuses("k_main", prepare, RD, V, RC, res, RO, pdir, td / "s9_k5", k_main=[5, 3, 1]),
            "[음성] 계약에 없는 k_main (5×3×1) 은 안 된다")

        # ── 계획 다시 결속 반례 (EF P1-2 · P2) ──
        pj0 = P.read_bytes()

        def plan_edit(fn):
            d = json.loads(pj0.decode("utf-8"))
            fn(d)
            P.write_bytes((json.dumps(d, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))

        def plan_back():
            P.write_bytes(pj0)

        # 구조 바꿔치기 — 이름은 cfg0003 그대로 · 구조를 cfg0007 (같은 가족 셋째) 것으로 · 입력 · 해시 같이 고침
        j0 = plan["jobs_sp"][0]
        alt = rdir / [e["name"] for e in plan8 if e["family"] == "F_B"][2] / "post_relax.xyz"
        fin0 = out / "sp" / j0["job"] / "scf.in"
        kin0 = fin0.read_bytes()
        t_alt = pw_input_text(read(str(alt)), prefix=j0["job"], calc="scf", k=[3, 2, 1], pseudo_dir=ps["dir"])
        _write_bytes(fin0, t_alt)

        def swap(d):
            d["jobs_sp"][0]["structure"] = _entry(alt, out)
            d["jobs_sp"][0]["input_sha256"] = _text_sha(t_alt)
        plan_edit(swap)
        chk(refuses("8 단계 기록의", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 계획의 구조를 다른 런 것으로 바꾸고 입력 · 해시를 같이 고쳐도 8 단계 기록에서 다시 찾아 멈춘다 (EF P1-2)")
        fin0.write_bytes(kin0)
        plan_back()
        # k_main 4×2×1 로 고치고 입력 · 해시 같이 고침 (after_kprobe 없음)
        k4 = {j["job"]: pw_input_text(read(str(out / j["structure"]["rel"])), prefix=j["job"], calc="scf", k=[4, 2, 1],
                                      pseudo_dir=ps["dir"]) for j in plan["jobs_sp"]}
        keep_in = {j["job"]: (out / "sp" / j["job"] / "scf.in").read_bytes() for j in plan["jobs_sp"]}
        for jb, t in k4.items():
            _write_bytes(out / "sp" / jb / "scf.in", t)

        def k421(d):
            d["k_main"] = [4, 2, 1]
            for j in d["jobs_sp"]:
                j["input_sha256"] = _text_sha(k4[j["job"]])
        plan_edit(k421)
        chk(refuses("after_kprobe", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 계획의 k_main 을 4×2×1 로 고치고 입력 · 해시를 같이 고쳐도 탐침 발동 판정이 없어 멈춘다 (EF P1-2)")
        for jb, b in keep_in.items():
            (out / "sp" / jb / "scf.in").write_bytes(b)
        plan_back()
        plan_edit(lambda d: d.update({"after_kprobe": {"rel": "x.json", "sha256": "0" * 64}}))
        chk(refuses("섞인 계획", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] k_main 3×2×1 계획에 탐침 판정 고리가 붙어 있으면 멈춘다 (섞인 계획)")
        plan_back()
        plan_edit(lambda d: d["pseudo"]["files"]["S"].update({"z_valence": 5.0}))
        chk(refuses("유사포텐셜 기록", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 계획의 가전자 기록을 손대면 (S 6 → 5) 지금 파일과 달라 멈춘다")
        plan_back()
        plan_edit(lambda d: d["contract"].update({"margin_dft_eV": 0.05}))
        chk(refuses("계약", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 계획에 저장된 계약 (판정 여유 0.10 → 0.05) 을 손대면 멈춘다 (저장된 칸도 참이어야)")
        plan_back()

        # ── 단일점 출력 ──
        sp_E = {"F_B": [-100.00, -99.90], "F_P": [-99.60, -99.70], "F_free": [-96.0, -95.9]}

        def fo(d, E, stage="sp", **kw):
            return _fake_out(d / "scf.in", E_list=kw.pop("E_list", [E]), stage=stage, pp=kw.pop("pp", PPR), **kw)

        def put_sp(jobs, **kw):
            for j in jobs:
                d = out / "sp" / j["job"]
                _write_bytes(d / "scf.out", fo(d, sp_E[j["family"]][j["i"] - 1], **kw.get(j["job"], {})))

        put_sp(plan["jobs_sp"][:5])
        chk(refuses("누락", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 단일점 출력 하나 없음 → 누락으로 멈춘다 (실패로 세지 않는다)")
        put_sp(plan["jobs_sp"])
        j2 = plan["jobs_sp"][2]
        d2 = out / "sp" / j2["job"]
        good2 = (d2 / "scf.out").read_bytes()
        other = fo(d2, -90.0, ecut=40.0, job_done=False)
        bad_cases = [
            ("JOB DONE", {"job_done": False}), ("SCF 수렴", {"not_conv": True}), ("ecutwfc", {"ecut": 60.0}),
            ("conv_thr", {"conv": "1.0E-06"}), ("smearing", {"smear": "Marzari-Vanderbilt"}),
            ("smearing", {"width": "0.0050"}), ("교환상관", {"xc": "SLA  PW   PSX  PSC"}),
            ("스핀", {"spin": True}), ("처음 좌표", {"shift_pos": 0.01}), ("입력 이름", {"input_name": "x.in"}),
            ("힘 블록", {"drop_forces": True}), ("prefix", {"prefix": "sp_other"}),
            ("유사포텐셜 S", {"pp": {**PPR, "S": {**PPR["S"], "md5": "f" * 32}}}),
            ("실행이 2 개", {"append_run": other}),                                       # EF P1-1 (ENCUT 40 · 미완료 둘째 실행)
            ("JOB DONE 뒤에 계산 기록", {"tail_junk": "!    total energy              =    -7.40000000 Ry\n"}),
            ("설정 줄이 한 번씩이 아니다", {"tail_junk": "     kinetic-energy cutoff     =      40.0000  Ry\n"}),
            ("전자 수", {"nelec": 595.0}), ("전자 수", {"nelec": "missing"}),                # EF P1-5
            ("Zval", {"zval_over": {"S": 5.0}}),
            ("요청 격자", {"mesh": [4, 2, 1]}),                                           # EF P1-3 (3×2×1 입력 · 4×2×1 목록)
            ("셀 축", {"axes_eps": 0.01}), ("PWSCF 판이 갈린다", {"version": "7.3"}),
            ("'!' 총에너지가 2 개", {"E_list": [sp_E["F_P"][0] + 0.5, sp_E["F_P"][0]]}),   # 단일점에 SCF 조각을 끼워 넣음
        ]
        for kw_, over in bad_cases:
            _write_bytes(d2 / "scf.out", fo(d2, sp_E["F_P"][0], **over))
            chk(refuses(kw_, read_sp, RD, P, out / "sp_verdict.json"), f"[음성] 단일점 출력 {kw_} 어긋남 → 판독 안 함")
        # 깨진 바이트 (EF P2-3) — '1.0E-\xff08'
        (d2 / "scf.out").write_bytes(good2.replace(b"1.0E-08", b"1.0E-\xff08"))
        chk(refuses("바이트 손상", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 출력에 깨진 바이트 → 판독 안 함 (조용히 지우지 않는다)")
        (d2 / "scf.out").write_bytes(good2)
        # 다른 잡 출력 바꿔치기 (같은 가족 둘째)
        d0, d1 = out / "sp" / plan["jobs_sp"][0]["job"], out / "sp" / plan["jobs_sp"][1]["job"]
        k0, k1 = (d0 / "scf.out").read_bytes(), (d1 / "scf.out").read_bytes()
        (d0 / "scf.out").write_bytes(k1)
        (d1 / "scf.out").write_bytes(k0)
        chk(refuses("처음 좌표", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 두 잡의 출력을 맞바꾸면 (에너지 순서가 뒤집힘) 처음 좌표 대조에서 멈춘다")
        (d0 / "scf.out").write_bytes(k0)
        (d1 / "scf.out").write_bytes(k1)
        # 입력을 계획 뒤 손댐
        fin = d0 / "scf.in"
        kin = fin.read_bytes()
        fin.write_bytes(kin.replace(b"conv_thr = 1.0d-8", b"conv_thr = 1.0d-6"))
        chk(refuses("입력 scf.in", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 입력을 계획 뒤 손대면 (sha256) 멈춘다")
        fin.write_bytes(kin)
        fin.write_bytes(kin.replace(b"mixing_beta = 0.3", b"mixing_beta = 0.7"))
        plan_edit(lambda d: d["jobs_sp"][0].update({"input_sha256": _sha(fin)}))
        chk(refuses("다시 만든 입력", read_sp, RD, P, out / "sp_verdict.json"),
            "[음성] 입력과 계획의 sha 를 같이 고쳐도 (mixing_beta) 다시 만든 입력과 달라 멈춘다")
        fin.write_bytes(kin)
        plan_back()
        plan_edit(lambda d: d["jobs_sp"][1].update({"name": d["jobs_sp"][2]["name"]}))
        chk(refuses("다시 고른 것", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 계획의 대상을 손대면 다시 고른 것과 달라 멈춘다")
        plan_back()
        plan_edit(lambda d: d["tools"]["dft_tool"].update({"sha256": "0" * 64}))
        chk(refuses("이 도구 sha256", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 계획을 만든 도구 판과 다르면 멈춘다")
        plan_back()
        # 유사포텐셜 파일이 계획 뒤 바뀜
        lib = (pdir / PP["Li"]).read_bytes()
        (pdir / PP["Li"]).write_bytes(lib + b"<!-- edited -->\n")
        chk(refuses("유사포텐셜 기록", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 유사포텐셜 파일이 계획 뒤 바뀌면 멈춘다")
        (pdir / PP["Li"]).write_bytes(lib)
        # reject — 걸린 출력만 보존해 옮긴다 (EF P2-6)
        _write_bytes(d2 / "scf.out", fo(d2, sp_E["F_P"][0], ecut=40.0))
        mv = reject_outputs(out, plan["jobs_sp"], stage="sp", pp=PPR)
        chk(len(mv) == 1 and mv[0][0] == j2["job"] and mv[0][1] == "scf.out.rejected.1" and not (d2 / "scf.out").exists()
            and (d2 / "scf.out.rejected.1").is_file() and b"40.0000" in (d2 / "scf.out.rejected.1").read_bytes()
            and (d0 / "scf.out").read_bytes() == k0,
            "[양성] reject — 검사에 걸린 출력 하나만 scf.out.rejected.1 로 옮김 (지우지 않음 · 통과한 출력은 그대로)")
        _write_bytes(d2 / "scf.out", fo(d2, sp_E["F_P"][0], nelec=595.0))
        mv = reject_outputs(out, plan["jobs_sp"], stage="sp", pp=PPR)
        chk(len(mv) == 1 and mv[0][1] == "scf.out.rejected.2" and (d2 / "scf.out.rejected.1").is_file()
            and (d2 / "scf.out.rejected.2").is_file(),
            "[양성] reject 두 번째 — 앞의 보존본을 덮지 않고 .rejected.2")
        (d2 / "scf.out").write_bytes(good2)

        spv = read_sp(RD, P, out / "sp_verdict.json")
        chk(spv["representatives"] == {"F_B": plan["jobs_sp"][0]["job"], "F_P": plan["jobs_sp"][3]["job"],
                                       "F_free": plan["jobs_sp"][4]["job"]}
            and spv["order"] == ["F_B", "F_P", "F_free"] and abs(spv["gap_eV"] - 0.30) < 1e-6
            and spv["G5"]["same_order"] and len(spv["jobs_kprobe"]) == 3 and spv["rows"][0]["nk"] == 4,
            "[양성] read_sp — 가족 대표 = 가족마다 단일점 최저 (F_P 는 UMA 둘째) · 순서 · 차 0.30 · G5 · k 점 4 · 탐침 입력 셋")
        kin0_ = parse_pw_in(out / "kprobe" / spv["jobs_kprobe"][0]["job"] / "scf.in")
        chk(kin0_["k"] == [4, 2, 1] and np.abs(kin0_["cell"] - pin["cell"]).max() < 1e-12, "[양성] 탐침 입력 = 같은 구조 · k 4×2×1")
        chk(refuses("이미 있다", read_sp, RD, P, out / "sp_verdict.json"), "[음성] 단일점 판정을 덮지 않는다")
        o_, i_ = parse_pw_out(d0 / "scf.out"), parse_pw_in(d0 / "scf.in")
        chk(out_problems(o_, i_, stage="sp", pp=PPR) == [], "[양성] 통과 출력의 문제 목록은 비어 있다")
        i_["k_shift"] = [1, 1, 1]
        chk(any("k shift" in w for w in out_problems(o_, i_, stage="sp", pp=PPR)),
            "[음성] 입력 k shift 가 0 0 0 이 아니면 거부 (격자 대조의 전제)")
        chk(refuses("덮지 않는다", _write_jobs, out, "kprobe", {spv["jobs_kprobe"][0]["job"]: "&CONTROL\n/\n"}),
            "[음성] 잡 입력이 이미 있고 다르면 덮지 않는다")

        # ── 단일점 판정 손댐 — 뒤 단계가 통째로 다시 내서 잡는다 (EF P2-1) ──
        SPV = out / "sp_verdict.json"
        sv0 = SPV.read_bytes()
        for what, fn in (("순서", lambda d: d.update({"order": ["F_P", "F_B", "F_free"]})),
                         ("문장", lambda d: d.update({"sentence_sp": "DFT 단일점 (UMA 이완 기하) 에서는 다른 순서였다."})),
                         ("G5", lambda d: d["G5"].update({"same_order": False})),
                         ("출력 sha", lambda d: d["rows"][0]["output"].update({"sha256": "0" * 64}))):
            d = json.loads(sv0.decode("utf-8"))
            fn(d)
            SPV.write_bytes(json.dumps(d, ensure_ascii=False).encode("utf-8"))
            chk(refuses("다시 낸 판정과 다르다", read_kprobe, RD, SPV, out / "kprobe_verdict.json", host),
                f"[음성] 단일점 판정의 {what} 를 손대면 탐침 판독이 멈춘다 (판정을 통째로 다시 내서 대조)")
        SPV.write_bytes(sv0)

        # ── k 탐침 ──
        def put_kp(dmap, base=out, **kw):
            for j in spv["jobs_kprobe"]:
                d = base / "kprobe" / j["job"]
                E = next(r["E_eV"] for r in spv["rows"] if r["job"] == spv["representatives"][j["family"]]) + dmap[j["family"]]
                _write_bytes(d / "scf.out", _fake_out(d / "scf.in", E_list=[E], stage="kprobe", pp=PPR, **kw))

        # EF P1-3 반례 — 탐침 출력이 3×2×1 (본 계산과 같은 4 점 · 같은 에너지) 이면 거부
        put_kp({"F_B": 0.0, "F_P": 0.0, "F_free": 0.0}, mesh=[3, 2, 1])
        chk(refuses("요청 격자", read_kprobe, RD, SPV, out / "kprobe_verdict.json", host),
            "[음성] 탐침 출력이 4×2×1 이 아니라 본 계산 격자 (3×2×1 · 4 점) 면 거부 (EF P1-3)")
        put_kp({"F_B": -0.010, "F_P": 0.020, "F_free": 0.0})
        chk(kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4}, {"F_B": 0, "F_P": 0.33, "F_free": 4.02}) == [],
            "[양성] 탐침 — 변화 0.03 · 순서 · 경계 그대로 → 발동 안 함")
        chk(any("변화" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4}, {"F_B": 0, "F_P": 0.36, "F_free": 4})),
            "[음성] 탐침 — 가족 차 0.06 변함 → 발동")
        chk(any("순서" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.03, "F_free": 4}, {"F_B": 0, "F_P": -0.01, "F_free": 4})),
            "[음성] 탐침 — 순서 바뀜 (변화 0.04 라도) → 발동")
        chk(any("경계" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.08, "F_free": 4}, {"F_B": 0, "F_P": 0.12, "F_free": 4})),
            "[음성] 탐침 — 0.10 경계 건넘 (변화 0.04 라도) → 발동")
        chk(any("F_free−F_P" in w for w in kprobe_trigger({"F_B": 0, "F_P": 0.30, "F_free": 4.0},
                                                         {"F_B": 0, "F_P": 0.30, "F_free": 4.07})),
            "[음성] 탐침 — 승자–차저가 아닌 쌍 (F_free−F_P) 의 0.07 변화도 발동")
        kpv = read_kprobe(RD, SPV, out / "kprobe_verdict.json", host)
        chk(not kpv["triggered"] and len(kpv["jobs_relax"]) == 3 and abs(kpv["reference_cell"]["volume_A3"] - 2436.33) < 1e-6
            and kpv["nk"] == {"k_main": 4, "k_probe": 6},
            "[양성] read_kprobe — 발동 안 함 → 이완 입력 셋 · 기준 셀 V₀ 2436.33 · k 점 4 → 6")
        rin = parse_pw_in(out / "relax" / kpv["jobs_relax"][0]["job"] / "scf.in")
        src = read(str(rdir / kpv["jobs_relax"][0]["name"] / "post_relax.xyz"))
        chk(rin["keys"]["calculation"] == "relax" and rin["keys"]["tstress"] == ".true." and rin["k"] == [3, 2, 1]
            and rin["keys"]["forc_conv_thr"] == "1.0d-3" and rin["keys"]["etot_conv_thr"] == "1.0d-5" and rin["keys"]["nstep"] == "200"
            and abs(abs(np.linalg.det(rin["cell"])) - 2436.33) < 1e-4
            and np.abs(rin["frac"] - src.get_scaled_positions(wrap=False)).max() < 1e-9
            and np.allclose(Atoms(cell=rin["cell"]).cell.cellpar()[3:], Atoms(cell=h.cell).cell.cellpar()[3:], atol=1e-8),
            "[양성] 이완 입력 = 기준 셀 (host 모양 · V₀) · 분수 좌표 그대로 · relax · tstress · 1e-3 / 1e-5 / 200 · k 3×2×1")
        # 발동 경로
        out_t = td / "s9_trig"
        shutil.copytree(out, out_t)
        os.remove(out_t / "kprobe_verdict.json")
        shutil.rmtree(out_t / "relax")
        put_kp({"F_B": 0.0, "F_P": 0.08, "F_free": 0.0}, base=out_t)
        kpt = read_kprobe(RD, out_t / "sp_verdict.json", out_t / "kprobe_verdict.json", host)
        chk(kpt["triggered"] and "jobs_relax" not in kpt and any("변화" in w for w in kpt["why"]),
            "[양성] read_kprobe — F_P 0.08 변함 → 발동 · 이완 입력 안 씀 · 다음 = 4×2×1 다시")
        chk(refuses("발동", read_relax, RD, out_t / "kprobe_verdict.json", out_t / "relax_verdict.json", host),
            "[음성] 발동한 탐침 뒤 이완은 판독하지 않는다")
        out_4 = td / "s9_k421"
        plan4 = prepare(RD, V, RC, res, RO, pdir, out_4, k_main=[4, 2, 1], after_kprobe=out_t / "kprobe_verdict.json")
        chk(parse_pw_in(out_4 / "sp" / plan4["jobs_sp"][0]["job"] / "scf.in")["k"] == [4, 2, 1]
            and plan4["after_kprobe"]["rel"] == os.path.relpath(out_t / "kprobe_verdict.json", out_4),
            "[양성] 발동 뒤 판 — 6 단일점 k 4×2×1 (prepare --k_main 4 2 1 --after_kprobe) · 발동 판정 고리 기록")
        chk(refuses("이 계획에서 나온 것이 아니다", _jobs_for_reject, out_4 / "dft_plan.json", "kprobe", SPV),
            "[음성] reject — 다른 계획의 판정 파일로 잡을 옮기지 않는다")
        chk(refuses("발동이 아니다", prepare, RD, V, RC, res, RO, pdir, td / "s9_nt", k_main=[4, 2, 1],
                    after_kprobe=out / "kprobe_verdict.json"), "[음성] 발동 안 한 탐침 판정으로는 4×2×1 판을 열지 않는다")
        res2 = rdir / "anneal_results_copy.json"
        res2.write_bytes(res.read_bytes() + b"\n")
        chk(refuses("다른 8 단계 결과", prepare, _FakeRD(real, A100, plan8, recs, res2), V, RC, res2, RO, pdir, td / "s9_r2",
                    k_main=[4, 2, 1], after_kprobe=out_t / "kprobe_verdict.json"),
            "[음성] 다른 8 단계 결과 파일로 만든 계획에 남의 발동 판정을 붙이지 않는다")

        # 탐침 판정 손댐 — 뒤 단계가 다시 내서 잡는다
        KPV = out / "kprobe_verdict.json"
        kv_keep = KPV.read_bytes()

        def kp_edit(fn, path=KPV):
            d = json.loads(kv_keep.decode("utf-8"))
            fn(d)
            path.write_bytes(json.dumps(d, ensure_ascii=False).encode("utf-8"))

        kp_edit(lambda d: d["pairs"]["F_P-F_B"].update({"change": 0.0001}))
        chk(refuses("다시 낸 발동 판정", read_relax, RD, KPV, out / "relax_verdict.json", host),
            "[음성] 탐침 판정의 쌍 값을 손대면 이완 판독이 멈춘다 (출력에서 다시 낸 판정과 다름)")
        kp_edit(lambda d: d["jobs_relax"][0].update({"name": d["jobs_relax"][1]["name"]}))
        chk(refuses("다시 낸 판정과 다르다", read_relax, RD, KPV, out / "relax_verdict.json", host),
            "[음성] 탐침 판정의 이완 잡 목록을 손대면 멈춘다 (판정을 통째로 다시 냄)")
        kp_edit(lambda d: [x.update({"sha256": "0" * 64}) for x in d["outputs"].values()])
        chk(refuses("다시 낸 판정과 다르다", read_relax, RD, KPV, out / "relax_verdict.json", host),
            "[음성] 탐침 판정의 출력 sha256 을 전부 0 으로 바꾸면 멈춘다 (EF P2-1)")
        KPV.write_bytes(kv_keep)
        fake_t = td / "kp_fake_triggered.json"
        d = json.loads(kv_keep.decode("utf-8"))
        d.update({"triggered": True, "why": ["가짜"]})
        d["sp_verdict"]["rel"] = os.path.relpath(SPV, td)
        fake_t.write_bytes(json.dumps(d, ensure_ascii=False).encode("utf-8"))
        chk(refuses("다시 낸 발동 판정", prepare, RD, V, RC, res, RO, pdir, td / "s9_fake", k_main=[4, 2, 1], after_kprobe=fake_t),
            "[음성] 발동 안 한 탐침 판정을 '발동' 으로 고쳐 4×2×1 판을 열려 하면 멈춘다 (출력에서 다시 냄)")

        # ── 이완 출력 · EOS 결속 ──
        RXV = out / "relax_verdict.json"

        def put_rx(Emap, Pmap, **over):
            for j in kpv["jobs_relax"]:
                d = out / "relax" / j["job"]
                kw = {"P_kbar": Pmap[j["family"]], **over.get(j["family"], {})}
                _write_bytes(d / "scf.out", _fake_out(d / "scf.in", E_list=[Emap[j["family"]] + 0.3, Emap[j["family"]]],
                                                      stage="relax", pp=PPR, **kw))

        ERX = {"F_B": -101.0, "F_P": -100.8, "F_free": -97.0}
        PRX = {"F_B": 5.0, "F_P": -3.0, "F_free": 8.0}
        jr0 = out / "relax" / kpv["jobs_relax"][0]["job"]
        rx_bad = [
            ("bfgs", {"F_P": {"bfgs": False}}, "이완 미수렴 ('bfgs converged' 없음)"),
            ("응력", {"F_B": {"P_before_last": True}}, "응력이 마지막 SCF 뒤에 없다 (앞 걸음의 압력)"),
            ("Final energy", {"F_B": {"final_E": ERX["F_B"] - 0.5}}, "Final energy 가 마지막 '!' 와 다름"),
            ("부피", {"F_free": {"vol_override": 2400.0}}, "출력 부피 ≠ 기준 셀 V₀"),
            ("최종 좌표", {"F_P": {"final": False}}, "최종 좌표 블록 없음"),
            ("응력", {"F_P": {"P_kbar": None}}, "압력 줄 없음 (P 를 지어내지 않는다)"),
            ("BFGS 기준", {"F_B": {"crit": ("1.0E-02", "1.0E-01")}}, "느슨한 BFGS 기준 (1e-2 · 1e-1) 의 수렴 (EF P1-4)"),
            ("이완 문턱", {"F_B": {"hdr_thr": ("1.0E-04", "1.0E-03")}}, "출력 머리의 이완 문턱이 계약과 다름"),
            ("nstep", {"F_free": {"nstep": 50}}, "nstep 50 ≠ 200"),
            ("BFGS 가 센 SCF", {"F_P": {"bfgs_cycles": 3}}, "'!' 줄 수 (2) ≠ BFGS 가 센 SCF 수 (3) — 빠진 · 끼워 넣은 조각"),
            ("이완 설정 줄", {"F_B": {"tail_junk": "     force convergence thresh. =      1.0E-01\n"}},
             "느슨한 이완 문턱 줄이 뒤에 한 번 더 (섞인 출력)"),
            ("마지막 힘 성분", {"F_P": {"force_last": 0.05}}, "마지막 힘 성분 0.05 Ry/Bohr > 1e-3 (EF P1-4)"),
            ("실행이 2 개", {"F_B": {"append_run": "     Program PWSCF v.7.4.1 starts on 14Nov2026 at  1:00:00 \n"}},
             "완료된 이완 뒤에 재시작 머리만 붙음 (EF P1-1)"),
        ]
        for kw_, over, what in rx_bad:
            put_rx(ERX, PRX, **over)
            chk(refuses(kw_, read_relax, RD, KPV, RXV, host), f"[음성] {what} → 판독 안 함")
        put_rx(ERX, PRX)
        rv = read_relax(RD, KPV, RXV, host)
        ei = rv["eos_input"]
        chk(rv["eos"]["skip_eos"] and abs(ei["F_B"]["P_GPa"] - 0.5) < 1e-12 and abs(ei["F_P"]["P_GPa"] + 0.3) < 1e-12
            and abs(ei["F_B"]["V_A3"] - 2436.33) < 0.01 and abs(ei["F_B"]["E_eV"] - ERX["F_B"]) < 1e-6
            and rv["eos"]["baseline_order"] == ["F_B", "F_P", "F_free"],
            "[양성] read_relax — (E, P, V) 를 출력에서 읽음 (P kbar→GPa · V = V₀) · 판 고정 eos_robust → EOS 생략")
        st = rv["stage10"]
        want3 = [e["name"] for e in sorted((e for e in plan8 if e["family"] == "F_B"), key=lambda e: recs[e["name"]]["E"])[:3]]
        chk(st and [s["name"] for s in st["stability_targets"]] == want3
            and all((out / s["post_relax"]["rel"]).is_file() and _sha(out / s["post_relax"]["rel"]) == s["post_relax"]["sha256"]
                    for s in st["stability_targets"])
            and len(rv["electronic_targets"]) == 3
            and all((out / t["rel"]).is_file() and _sha(out / t["rel"]) == t["sha256"] for t in rv["electronic_targets"]),
            "[양성] 10 단계 — DFT 승자 F_B (0.2 ≥ 0.10) → 그 가족 UMA 어닐 최저 셋 · 전자구조 대상 = 이완 셋 · "
            "경로 모두 계획 폴더 기준으로 실재 · sha256 일치 (EF P2-2)")
        chk(rv["relaxed"]["F_B"]["record"]["end_motif"] in ("F_B", "F_P", "F_free", "mixed", "unclassified")
            and "B_coordination" in rv["relaxed"]["F_B"]["record"] and "조건부" in rv["scope"],
            "[양성] 이완 구조 기록 — 끝 꼴 (판 고정 분류) · B · P 배위 · 판정 범위 문장 (수렴 설정 조건부)")
        os.remove(RXV)
        rx0 = out / rv["relaxed"]["F_B"]["file"]["rel"]
        rxk = rx0.read_bytes()
        rx0.write_bytes(rxk + b"\n")
        chk(refuses("만든 구조와 다르다", read_relax, RD, KPV, RXV, host),
            "[음성] 이완 구조 파일이 이미 있고 이번 출력에서 만든 것과 다르면 덮지 않는다")
        rx0.write_bytes(rxk)
        put_rx({"F_B": -101.0, "F_P": -100.95, "F_free": -97.0}, {"F_B": 1.0, "F_P": -0.5, "F_free": 0.8})
        rv2 = read_relax(RD, KPV, RXV, host)
        chk(rv2["eos"]["skip_eos"] and [s["family"] for s in rv2["stage10"]["stability_targets"]] == FAM,
            "[양성] 10 단계 — DFT 차 0.05 < 0.10 (|P| ≤ 0.1 GPa · 보정 < 0.004 eV) → 가족마다 UMA 어닐 최저 하나 (셋)")
        chk(rv["corrected_gap_range_eV"][0] - 0.2 > 0.02 and rv["corrected_gap_range_eV"][1] - 0.2 > 0.06,
            f"[정보] 압력 0.5 · −0.3 GPa 만으로도 보정 뒤 차가 {rv['corrected_gap_range_eV'][0]:.3f}–{rv['corrected_gap_range_eV'][1]:.3f} "
            f"(보정 전 0.200) — 2436 Å³ 셀이라 셀마다 −P²V/2B 가 0.02–0.09 eV")
        os.remove(RXV)
        put_rx(ERX, {"F_B": 25.0, "F_P": 25.0, "F_free": 25.0})
        rv3 = read_relax(RD, KPV, RXV, host)
        chk(not rv3["eos"]["skip_eos"] and rv3["stage10"] is None and rv3["electronic_targets"] is None
            and "EOS 필요" in rv3["decision"] and "F_B" in rv3["decision"] and rv3["relaxed"] and "진단" in rv3["relaxed_note"],
            "[음성] |P| 2.5 GPa > 2 (세 가족) → EOS 필요 · 안정성 · 전자구조 대상 둘 다 null · 이완 구조는 진단 자료 (EF P1-6)")
        os.remove(RXV)
        put_rx({"F_B": -101.0, "F_P": -100.905, "F_free": -97.0}, {"F_B": 19.0, "F_P": 0.0, "F_free": 8.0})
        rv4 = read_relax(RD, KPV, RXV, host)
        chk(not rv4["eos"]["skip_eos"] and rv4["stage10"] is None and rv4["electronic_targets"] is None,
            "[음성] 보정 범위 안에서 0.10 판정이 바뀔 수 있으면 (차 0.095 · |P| 1.9) EOS 필요 · 고르기 안 함")
        os.remove(RXV)
        # 이완 출력 바꿔치기 (가족끼리)
        put_rx(ERX, PRX)
        jb, jp = (out / "relax" / j["job"] for j in kpv["jobs_relax"][:2])
        kb, kp_ = (jb / "scf.out").read_bytes(), (jp / "scf.out").read_bytes()
        (jb / "scf.out").write_bytes(kp_)
        (jp / "scf.out").write_bytes(kb)
        chk(refuses("처음 좌표", read_relax, RD, KPV, RXV, host), "[음성] 이완 출력을 가족끼리 맞바꾸면 처음 좌표 대조에서 멈춘다")
        (jb / "scf.out").write_bytes(kb)
        (jp / "scf.out").write_bytes(kp_)
        # 단일점 출력이 판정 뒤 바뀜 → 이완 판독도 멈춘다 (사슬)
        dsp = out / "sp" / plan["jobs_sp"][3]["job"]
        ksp = (dsp / "scf.out").read_bytes()
        (dsp / "scf.out").write_bytes(ksp.replace(f"{sp_E['F_P'][1] / RY_EV:.8f}".encode(),
                                                  f"{(sp_E['F_P'][1] - 0.4) / RY_EV:.8f}".encode()))
        chk(refuses("단일점 판정", read_relax, RD, KPV, RXV, host),
            "[음성] 단일점 출력이 판정 뒤 바뀌면 (에너지) 이완 판독도 멈춘다 (사슬 다시 결속)")
        (dsp / "scf.out").write_bytes(ksp)
        # 만든 파일은 utf-8 · LF (EF P2-4)
        made = [p for p in out.rglob("*") if p.is_file() and (p.name == "scf.in" or p.suffix in (".json", ".xyz"))
                and "s8_anneal" not in p.parts]
        chk(made and all(b"\r" not in p.read_bytes() for p in made),
            f"[양성] 이 도구가 쓴 파일 {len(made)} 개 (계획 · 입력 · 판정 · 이완 구조) 에 CR 없음 (LF · Windows 에서도 같은 sha)")
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
    r = sub.add_parser("reject", help="검사에 걸린 출력을 scf.out.rejected.N 으로 보존해 옮긴다 (실행기가 그 잡만 다시 돈다)")
    r.add_argument("--plan", required=True)
    r.add_argument("--stage", required=True, choices=["sp", "kprobe", "relax"])
    r.add_argument("--verdict", help="kprobe → 단일점 판정 · relax → 탐침 판정 (4×2×1 판이면 단일점 판정)")
    for s in (a, b, c, d):
        s.add_argument("--readout_tool", default=str(DEFAULT_RD))
    A = ap.parse_args(argv)
    print(f"DFT 도구 {SELF} · sha256 {_tool_fp()['sha256']}")
    if A.cmd == "reject":
        plan, jobs = _jobs_for_reject(A.plan, A.stage, A.verdict)
        moved = reject_outputs(Path(A.plan).resolve().parent, jobs, stage=A.stage, pp=plan["pseudo"]["files"],
                               V0=DFT["ref_cell"]["V0_A3"] if A.stage == "relax" else None)
        if not moved:
            print(f"-> {A.stage}: 옮길 출력 없음 (걸린 출력 없음 · 없는 출력은 누락이지 실패가 아니다)")
        for jb, dest, why in moved:
            print(f"-> {jb}: " + (f"scf.out → {dest}" if dest else "손대지 않음") + " · " + " · ".join(why))
        if any(dst for _, dst, _ in moved):
            print(f"   다음: GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 bash <이 판>/tools/doping/run_force_check_scf.sh "
                  f"{Path(A.plan).resolve().parent / A.stage}  (scf.out 이 없는 잡만 처음부터 다시 — nowf 라 재개 없음)")
        return 0
    RD = load_rd(A.readout_tool)
    check_rd(RD)
    print(f"판독기 {RD.__dft_path__} · sha256 {RD.__dft_sha256__}")
    if A.cmd == "prepare":
        p = prepare(RD, A.verdict, A.receipt, A.results, A.readout, A.pseudo_dir, A.out_dir, A.k_main, A.after_kprobe)
        print(f"-> {Path(A.out_dir) / 'dft_plan.json'} · 단일점 {len(p['jobs_sp'])} 잡 (k {p['k_main']}) · "
              f"유사포텐셜 {p['pseudo']['dir']} · 가전자 " +
              " ".join(f"{el} {x['z_valence']:g}" for el, x in p["pseudo"]["files"].items()))
        for j in p["jobs_sp"]:
            print(f"   {j['job']}  ←  {j['name']}  (UMA 끝 꼴 {j['uma_record']['end_motif']})")
        print(f"   실행: GPU_EXCLUSIVE=1 MIN_FREE_MIB=45000 bash <src>/tools/doping/run_force_check_scf.sh {Path(A.out_dir) / 'sp'}")
        return 0
    if A.cmd == "read_sp":
        v = read_sp(RD, A.plan, A.out, A.host)
        print(f"-> {A.out} · 단일점 순서 {v['order']} · 최저–차점 {v['gap_eV']:.3f} eV/B₂O₃ · G5 {'같음' if v['G5']['same_order'] else '다름'}")
        print(f"   {v['sentence_sp']}")
        print(f"   다음: {v['next']}")
        return 0
    if A.cmd == "read_kprobe":
        v = read_kprobe(RD, A.sp_verdict, A.out, A.host)
        print(f"-> {A.out} · 탐침 {'발동' if v['triggered'] else '발동 안 함'} · k 점 {v['nk']['k_main']} → {v['nk']['k_probe']}")
        for k, x in v["pairs"].items():
            print(f"   {k}: {x['k_main']:+.3f} → {x['k_probe']:+.3f} (변화 {x['change']:+.3f})")
        for w in v["why"]:
            print(f"   ⛔ {w}")
        print(f"   다음: {v['next']}")
        return 0
    v = read_relax(RD, A.prev, A.out, A.host)
    print(f"-> {A.out}")
    for r_ in v["rows"]:
        print(f"   {r_['job']}: P {r_['P_GPa']:+.2f} GPa · bfgs {r_['bfgs']['steps']} 걸음 · "
              f"마지막 힘 성분 최대 {r_['final_force_max_comp_RyBohr']:.1e} Ry/Bohr")
    print(f"   {v['decision']}")
    print(f"   범위: {v['scope']}")
    if v.get("stage10"):
        print(f"   10 단계: {v['stage10']['rule']}")
        for s in v["stage10"]["stability_targets"]:
            print(f"     안정성 대상 {s['family']} {s['name']}")
    else:
        print(f"   ⛔ {v.get('relaxed_note')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
