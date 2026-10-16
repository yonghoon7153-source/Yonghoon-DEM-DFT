#!/usr/bin/env python3
"""build_aprime_s3.py — A′ S3 패키지: S2 이완 좌표 → 끝점(bound·far) 재구성 · 파생 표본 · G3/G4 셀 · QE 입력 · sha 계보 (카드 v5 §0 S3).

    python3 tools/wad/build_aprime_s3.py --s3 --relax db/raw/wad_aprime_s2_relax_2026_09_25 --geom db/inputs/wad_aprime_s2_geometries_2026_09_25 --out db/inputs/wad_aprime_s3_2026_09_25
    python3 tools/wad/build_aprime_s3.py --v2_ed <V2 relax pw.out> --model_dir <S3/V2_top_fcc> --out <dir>   # 2단계: DFT 이완 좌표 → E(d)·far·G3·G4 입력
    python3 tools/wad/build_aprime_s3.py --seal_p2s --out <dir>   # P2′ (외주 2차 카드): 이완 부모 둘 → 끝점 · p05 · G3 · D3 만 예측 (80 % 규칙) · sha — VASP 잡 행렬은 묶음 빌더 몫
    python3 tools/wad/build_aprime_s3.py --selftest

규칙 (전부 카드 v5 에 봉인된 것을 코드로 옮김 · 결과 보고 바꾸지 않는다):
  · 상태: interface_check 깃발 0 + 수렴 → S3 후보 / 깃발 ≥ 1 → INCOMPLETE (세고 제외 · 교체 없음 · 소견만 기록)
  · 끝점: `build_aprime_interfaces.make_endpoints` (직접·영상 ≥ 8 Å · 같은 c · 쌍극자 구간 셀 위끝) — 이완 좌표에 다시 적용
  · 표본 ⑤: V5 S 바깥 registry A 의 이완 결합 기하에서 흡착층(Ag) +0.5 Å 강체 인장 → 자기 bound · far 는 같은 c 면 ① 과 같은 파일(sha 로 대조)
  · V2: 결합 기하는 **QE relax** (Ag 아래 2층 if_pos 0 0 0 · 그래핀 x·y 고정 if_pos 0 0 1 · PBE+D3) — 2단계(`--v2_ed`)에서 이완 출력의
    최종 좌표로 E(d) = d₀−0.3 · d₀+0.3 · d₀+0.6 · far 와 G3/G4 입력을 만든다 (규칙은 지금 봉인 · 좌표 sha 는 그때 부록)
  · G3 (대표점: V4_s_outer_A · V5_s_outer_A · V2_top_fcc(2단계)): (i) c+2 Å · 흡착층 그대로 → far 직접 8 / 영상 10 (ii) c+2 · 흡착층 +2 → 10 / 8 ·
    bound 는 c+2 셀에서 1 개 (i·ii 공통) · 기록할 것 ΔE_far · ΔE_bound · ΔW
  · G4 (같은 대표점): ecut 70/700 · k 한 단계 촘촘 · smearing ½ — 각각 두 끝점
  · 프로브 (S3 전 예외 ③): 분리 셀 · scf · ecut 70/700 · electron_maxstep 2 · 대표점 + V5 전부
  · QE: 52/520 Ry · PBE+D3(BJ 2체) · Ag 포함 = mv 0.01 · SE 만 = gaussian 0.005 · nspin 1 · tefield/dipfield edir 3 eamp 0 · disk_io medium
⛔ 못 하는 것: 계산·판정을 하지 않는다 · 이완 좌표를 고치지 않는다 (sha 가 relax_meta 와 다르면 거부) · V2 2단계 좌표는 이완 출력이 있어야 만든다.
"""
import argparse
import datetime as _dt
import glob
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S                    # noqa: E402
import build_aprime_interfaces as B        # noqa: E402
from relax_uma_d3 import ROLES             # noqa: E402

SlabError = S.SlabError
REPO = S.REPO
PP = dict(S.QE_PP)
PP.update({"Ag": (107.8682, "Ag_ONCV_PBE-1.0.oncvpsp.upf"), "C": (12.011, "C.pbe-n-kjpaw_psl.1.0.0.UPF"), "H": (1.008, "H.pbe-rrkjus_psl.1.0.0.UPF")})
PP_SHA = dict(S.PP_SHA256)
PP_SHA.update({"Ag_ONCV_PBE-1.0.oncvpsp.upf": "0494aa5927b754b42d3e72535636f215b4658e9b437e639dbc09674c36c8059a",
               "C.pbe-n-kjpaw_psl.1.0.0.UPF": "9900d1efd50b9848e31849f39094b33348486b400ee51e0f3922f716137cf3d7",
               "H.pbe-rrkjus_psl.1.0.0.UPF": "27f8a7e87851d59a2698237d6ab4578d62950640f4f175781b015a0ce731f962"})
ORDER = ("Li", "P", "S", "Cl", "Ag", "C", "H")
KPTS = {"V2": (6, 6, 1), "V3": (3, 3, 1), "V4": (3, 3, 1), "V5": (3, 2, 1)}
MACHINE = {"V2": "V100 (≈3 GB)", "V3": "gabia (≈42 GB · 프로브 뒤)", "V4": "gabia (≈37 GB · 프로브 뒤)", "V5": "RESOURCE_BLOCKED (예상 ≈246 GB) — 프로브로 확정"}
G3_REPS = {"V4": "V4_s_outer_A", "V5": "V5_s_outer_A", "V2": "V2_top_fcc"}
ED_SHIFTS = (-0.3, 0.3, 0.6)
CARD = "db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json"


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def qe_input(atoms, prefix, kpts, pseudo_dir, calc="scf", dip=None, fixed=(), lateral=(), ecut=(52.0, 520.0), electron_maxstep=200, d3=True):
    """A′ 용 pw.in — se_sym_slab.qe_input 의 규약(52/520 · D3 2체 명시 · local-TF · disk_io medium) + Ag·C·H · 쌍극자 · if_pos 제약."""
    syms = atoms.get_chemical_symbols()
    els = [e for e in ORDER if e in syms]
    missing = sorted(set(syms) - set(ORDER))
    if missing:
        raise SlabError(f"PP 가 없는 원소 {missing}")
    has_ag = "Ag" in els
    L = ["&CONTROL", f"  calculation = '{calc}'", f"  prefix = '{prefix}'", "  outdir = './tmp'", f"  pseudo_dir = '{pseudo_dir}'",
         "  tprnfor = .true.", "  disk_io = 'medium'"]
    if dip:
        L += ["  tefield = .true.", "  dipfield = .true."]
    if calc == "relax":
        L += ["  etot_conv_thr = 1.0d-5", "  forc_conv_thr = 1.0d-3", "  nstep = 200"]
    L += ["/", "&SYSTEM", "  ibrav = 0", f"  nat = {len(atoms)}", f"  ntyp = {len(els)}", f"  ecutwfc = {ecut[0]}", f"  ecutrho = {ecut[1]}",
          "  occupations = 'smearing'", f"  smearing = '{'mv' if has_ag else 'gaussian'}'", f"  degauss = {0.01 if has_ag else 0.005}", "  nspin = 1"]
    if dip:
        L += ["  edir = 3", "  eamp = 0.0d0", f"  emaxpos = {dip['emaxpos']:.5f}", f"  eopreg = {dip['eopreg']:.5f}"]
    if d3:
        L += ["  vdw_corr = 'grimme-d3'", "  dftd3_version = 4", "  dftd3_threebody = .false."]
    else:
        L += ["  vdw_corr = 'none'"]
    L += ["/", "&ELECTRONS", "  conv_thr = 1.0d-8", "  mixing_beta = 0.3", f"  electron_maxstep = {electron_maxstep}", "  mixing_mode = 'local-TF'", "/"]
    if calc == "relax":
        L += ["&IONS", "  ion_dynamics = 'bfgs'", "/"]
    L += ["", "ATOMIC_SPECIES"]
    for e in els:
        L.append(f"  {e:2s} {PP[e][0]:9.4f}  {PP[e][1]}")
    L += ["", "CELL_PARAMETERS angstrom"]
    for v in atoms.cell.array:
        L.append("  %16.10f %16.10f %16.10f" % tuple(v))
    L += ["", "ATOMIC_POSITIONS angstrom"]
    fx, lt = set(int(i) for i in fixed), set(int(i) for i in lateral)
    for i, (s, p) in enumerate(zip(syms, atoms.get_positions())):
        flag = ""
        if calc == "relax":
            flag = "  0 0 0" if i in fx else ("  0 0 1" if i in lt else "  1 1 1")
        L.append(f"  {s:2s} %16.10f %16.10f %16.10f" % tuple(p) + flag)
    L += ["", "K_POINTS automatic", "  %d %d %d 0 0 0" % tuple(kpts), ""]
    return "\n".join(L)


def _ads_mask(atoms, model):
    sub_el, ads_el = ROLES[model]
    return np.array([s in ads_el for s in atoms.get_chemical_symbols()])


def _rigid_shift(atoms, is_ads, dz):
    a = atoms.copy(); x = a.get_positions(); x[is_ads, 2] += dz; a.set_positions(x)
    return a


def _c_plus(atoms, dc):
    a = atoms.copy(); C = a.cell.array.copy(); C[2, 2] += dc; a.set_cell(C)
    return a


def _dip_for(structs):
    """G3 변형 집합(c+2 · bound · far (i)(ii)) 에 **같은** 쌍극자 구간 — 개정 2 규칙 (집합의 진공 중앙 · 양쪽 핵 ≥ 4 Å)."""
    return B.dip_region(structs)


class Pack:
    """S3 산출물 묶음 — 구조 파일 · pw.in · jobs · manifest."""
    def __init__(self, out, pseudo_dir):
        self.out, self.pseudo_dir = out, pseudo_dir
        self.jobs, self.struct = [], {}
        os.makedirs(out, exist_ok=True)

    def add_struct(self, name, atoms):
        from ase.io import write
        d = os.path.join(self.out, "structures"); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, f"{name}.extxyz")
        a = atoms.copy(); a.set_pbc((True, True, False)); a.calc = None
        write(p, a)
        self.struct[name] = _sha(p)
        return p

    def add_job(self, name, atoms, model, calc="scf", dip=None, fixed=(), lateral=(), ecut=(52.0, 520.0), kpts=None, electron_maxstep=200, kind="scf", tags=None, machine=None):
        d = os.path.join(self.out, "qe", name); os.makedirs(d, exist_ok=True)
        k = kpts or KPTS[model]
        txt = qe_input(atoms, name, k, self.pseudo_dir, calc, dip, fixed, lateral, ecut, electron_maxstep, d3=True)
        p = os.path.join(d, "pw.in"); open(p, "w").write(txt)
        self.jobs.append({"dir": name, "kind": kind, "calc": calc, "model": model, "nat": len(atoms), "kpts": list(k), "ecutwfc": ecut[0], "ecutrho": ecut[1],
                          "electron_maxstep": electron_maxstep, "d3": True, "dip": dip, "pw_in_sha256": _sha(p), "structure": tags.get("structure") if tags else None,
                          "tags": tags or {}, "machine": machine or MACHINE[model]})
        return p


def load_relaxed(relax_dir, name):
    from ase.io import read
    d = os.path.join(relax_dir, name)
    meta = json.load(open(os.path.join(d, "relax_meta.json"), encoding="utf-8"))
    chk = json.load(open(os.path.join(d, "interface_check.json"), encoding="utf-8"))
    p = os.path.join(d, "relaxed.extxyz")
    if _sha(p) != meta["relaxed_sha256"]:
        raise SlabError(f"{name}: relaxed.extxyz sha 가 relax_meta 와 다르다 — 손댄 좌표")
    at = read(p); at.set_pbc((True, True, False))
    return at, meta, chk, {"relaxed_sha256": meta["relaxed_sha256"], "relax_meta_sha256": _sha(os.path.join(d, "relax_meta.json")),
                            "interface_check_sha256": _sha(os.path.join(d, "interface_check.json")), "init_sha256": meta["init_sha256"]}


def build_s3(relax_dir, geom_dir, out, pseudo_dir="/data/work/pseudo", gap=8.0, date=None):
    from ase.io import read
    date = date or _dt.date.today().isoformat()
    card = json.load(open(os.path.join(REPO, CARD), encoding="utf-8"))
    card_digest = card.get("ratification", {}).get("content_digest")
    if not card_digest:
        raise SlabError("카드 v5 가 봉인(content_digest)돼 있지 않다 — S3 는 S1 봉인 뒤에만")
    geom_man = json.load(open(os.path.join(geom_dir, "manifest.json"), encoding="utf-8"))
    P = Pack(out, pseudo_dir)
    names = sorted(d for d in os.listdir(relax_dir) if os.path.isdir(os.path.join(relax_dir, d)))
    status, findings, endpoints = {}, {}, {}
    cand = []
    for n in names:
        at, meta, chk, lin = load_relaxed(relax_dir, n)
        model = meta["model"]
        flags = meta["interface_check_flags"]
        if flags or not meta["converged_fmax"]:
            status[n] = "INCOMPLETE"
            findings[n] = {"flags": flags, "converged": meta["converged_fmax"], "disp_max_A": meta["disp_max_A"],
                           "소견": ("Ag₄ 사면체가 표면에서 열림 (Ag–Ag 결합 목록 ±15 % 밖)" if model == "V3" else
                                    "기판 원자가 첫 흡착층 평면 아래 1.5 Å 안 (비혼합 범위 이탈)" if any("비혼합" in f for f in flags) else "후검 깃발"),
                           "처리": "세고 제외 · 교체 없음 · S4 입력 만들지 않음 (카드 G2)", "lineage": lin}
            continue
        status[n] = "S3_CANDIDATE"
        cand.append((n, at, meta, chk, lin, model))
    sample5 = None
    for n, at, meta, chk, lin, model in cand:
        is_ads = _ads_mask(at, model)
        # 마스크는 S2 기하 폴더의 meta.json (최적화 전 기록) 에서 가져온다 — 러너 meta 는 개수만 적는다
        gm = _geom_meta(geom_dir, n, model)
        fixed, lateral = gm["fixed_idx"], gm.get("lateral_fixed_idx", [])
        b, f, em = B.make_endpoints(at, is_ads, gap)
        sb = P.add_struct(f"{n}_bound", b); sf = P.add_struct(f"{n}_far", f)
        dip = em["dipfield"]
        rec = {"model": model, "registry": meta.get("registry"), "term": meta.get("term"), "lineage": lin, "n_atoms": len(at), "fixed_idx": fixed, "lateral_fixed_idx": lateral,
               "endpoints": em, "bound_sha256": P.struct[f"{n}_bound"], "far_sha256": P.struct[f"{n}_far"], "kpts": list(KPTS[model]), "machine": MACHINE[model]}
        if model == "V2":
            # 1단계 = QE relax (제약) · 2단계는 --v2_ed
            P.add_job(f"{n}_relax", b, model, calc="relax", dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, fixed=fixed, lateral=lateral,
                      kind="relax", tags={"structure": f"{n}_bound", "stage": "S4-1 · 제약 DFT 이완 (Ag 아래 2층 고정 · 그래핀 x·y 고정) · 2단계 E(d) 는 --v2_ed"})
            rec["V2_stage2"] = "이완 출력(pw.out 최종 좌표)에서 --v2_ed 로 d₀ · E(d) (−0.3 · +0.3 · +0.6) · far · G3 · G4 입력 생성 (규칙 봉인 · 좌표 sha 는 부록)"
        else:
            P.add_job(f"{n}_bound", b, model, dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, tags={"structure": f"{n}_bound", "endpoint": "bound"})
            P.add_job(f"{n}_far", f, model, dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, tags={"structure": f"{n}_far", "endpoint": "far"})
            # 프로브 (S3 전 예외 ③ · scf · 70/700 · electron_maxstep 2 · 분리 셀)
            if model == "V5" or n == G3_REPS.get(model):
                P.add_job(f"probe_{n}_far_e70", f, model, dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, ecut=(70.0, 700.0), electron_maxstep=2, kind="probe",
                          tags={"structure": f"{n}_far", "⛔": "S3 전 예외 ③ — 원출력 보존 · 에너지 사용 금지 · CPU 추정 → GPU 허가 → 피크 실측"})
            # G3 · G4 (대표점)
            if n == G3_REPS.get(model):
                b2 = _c_plus(b, 2.0); f2i = _c_plus(f, 2.0); f2ii = _rigid_shift(_c_plus(f, 2.0), is_ads, 2.0)
                d2 = _dip_for([b2, f2i, f2ii])
                for tag, a2 in (("G3_c2_bound", b2), ("G3_c2_far_i", f2i), ("G3_c2_far_ii", f2ii)):
                    P.add_struct(f"{n}_{tag}", a2)
                    P.add_job(f"{n}_{tag}", a2, model, dip={"emaxpos": d2["emaxpos"], "eopreg": d2["eopreg"]}, kind="g3", tags={"structure": f"{n}_{tag}", "G3": tag})
                rec["G3"] = {"cells": "c+2 Å · bound 1 · far (i) 그대로 → 직접 8/영상 10 · far (ii) +2 → 10/8", "기록": "ΔE_far · ΔE_bound · ΔW (|ΔW| ≤ 0.01 · 조각 |ΔE| ≤ 5 meV)",
                             "far_gaps_check": {"i": _gaps(f2i, is_ads), "ii": _gaps(f2ii, is_ads)}, "dip_region_A": d2["region_A"]}
                k = KPTS[model]; k1 = (k[0] + 1, k[1] + 1, 1)
                for tag, a2, kw in (("G4_e70_bound", b, {"ecut": (70.0, 700.0)}), ("G4_e70_far", f, {"ecut": (70.0, 700.0)}),
                                    ("G4_k1_bound", b, {"kpts": k1}), ("G4_k1_far", f, {"kpts": k1})):
                    P.add_job(f"{n}_{tag}", a2, model, dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, kind="g4", tags={"structure": f"{n}_{'bound' if 'bound' in tag else 'far'}", "G4": tag}, **kw)
                # smearing ½ 는 입력 텍스트 치환으로 (작성기 인자 최소화)
                for ep, a2 in (("bound", b), ("far", f)):
                    p = P.add_job(f"{n}_G4_s05_{ep}", a2, model, dip={"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}, kind="g4", tags={"structure": f"{n}_{ep}", "G4": f"G4_s05_{ep}"})
                    t = open(p).read().replace("degauss = 0.01\n", "degauss = 0.005\n").replace("degauss = 0.005\n", "degauss = 0.0025\n", 1) if "Ag" not in at.get_chemical_symbols() else open(p).read().replace("degauss = 0.01\n", "degauss = 0.005\n")
                    open(p, "w").write(t); P.jobs[-1]["pw_in_sha256"] = _sha(p); P.jobs[-1]["tags"]["degauss_halved"] = True
                rec["G4"] = {"variants": ["e70/700", f"k {k1[0]}×{k1[1]}×1", "smearing ½"], "각각": "두 끝점 · |ΔW| ≤ 0.02 (조각 ≤ 10 meV)"}
        # 표본 ⑤ — V5 S 바깥 A 에서 +0.5 Å 인장
        if n == "V5_s_outer_A":
            b5 = _rigid_shift(at, is_ads, 0.5)
            bb5, ff5, em5 = B.make_endpoints(b5, is_ads, gap)
            P.add_struct("V5_s_outer_A_p05_bound", bb5); P.add_struct("V5_s_outer_A_p05_far", ff5)
            same_far = P.struct["V5_s_outer_A_p05_far"] == P.struct[f"{n}_far"]
            d5 = em5["dipfield"]
            P.add_job("V5_s_outer_A_p05_bound", bb5, model, dip={"emaxpos": d5["emaxpos"], "eopreg": d5["eopreg"]}, tags={"structure": "V5_s_outer_A_p05_bound", "endpoint": "bound", "sample": "⑤ (S·A +0.5 Å 인장)"})
            if not same_far:
                P.add_job("V5_s_outer_A_p05_far", ff5, model, dip={"emaxpos": d5["emaxpos"], "eopreg": d5["eopreg"]}, tags={"structure": "V5_s_outer_A_p05_far", "endpoint": "far", "sample": "⑤"})
            sample5 = {"from": n, "shift_A": 0.5, "bound_sha256": P.struct["V5_s_outer_A_p05_bound"], "far_sha256": P.struct["V5_s_outer_A_p05_far"], "far_same_as_sample1": same_far,
                       "endpoints": em5, "⚠": "표본 ①과 같은 registry — 독립 표본 주장 금지 (카드)"}
        endpoints[n] = rec
    idx = {"schema": "aprime_s3_package/v2", "date": date, "card": CARD, "card_content_digest": card_digest,
           "dipole_rule": "개정 2 (2026-09-26) — build_aprime_interfaces.dip_region: 집합(bound·far·G3 변형)의 진공 중앙 · 양쪽 핵 ≥ 4 Å · 폭 1 Å (v1 패키지의 '[c−1.5, c−0.5]' 는 기판 바닥 영상 1 Å 아래 → 비물리 힘 · 폐기)",
           "geometries_manifest_sha256": _sha(os.path.join(geom_dir, "manifest.json")), "relax_dir": relax_dir,
           "code_sha256": {os.path.relpath(__file__, REPO): _sha(__file__), "tools/wad/build_aprime_interfaces.py": _sha(os.path.join(HERE, "build_aprime_interfaces.py")),
                           "tools/wad/se_sym_slab.py": _sha(os.path.join(HERE, "se_sym_slab.py")), "tools/wad/relax_uma_d3.py": _sha(os.path.join(HERE, "relax_uma_d3.py"))},
           "status": status, "n_candidates": sum(1 for v in status.values() if v == "S3_CANDIDATE"), "n_incomplete": sum(1 for v in status.values() if v == "INCOMPLETE"),
           "incomplete_findings": findings, "endpoints": endpoints, "sample5": sample5,
           "G5_samples": {"①": "V5_s_outer_A", "②": "V5_s_outer_B", "③": "V5_li_outer_A", "④": "V5_li_outer_B", "⑤": "V5_s_outer_A_p05 (①과 상관)", "⚠": "V5 는 RESOURCE_BLOCKED (예상) — 프로브 뒤 (실측) 로 · 막히면 G5 NOT_TESTED"},
           "settings": {"ecutwfc": 52.0, "ecutrho": 520.0, "functional": "PBE + D3(BJ) 2체 (dftd3_version 4 · threebody .false.)", "smearing": "Ag 포함 mv 0.01 · SE 만 gaussian 0.005 · nspin 1",
                        "dipole": "tefield · dipfield · edir 3 · eamp 0 · 불연속 구간(emaxpos/eopreg) = 집합(bound·far·G3 변형)의 진공 중앙 · 양쪽 핵 ≥ 4 Å · 폭 1 Å (개정 2 · build_aprime_interfaces.dip_region 이 여유 검사 · 종전 '[c−1.5, c−0.5] Å' 는 기판 바닥 영상 1 Å 아래여서 폐기)", "kpts": {k: list(v) for k, v in KPTS.items()},
                        "pp": {e: PP[e][1] for e in ORDER}, "pp_sha256": {PP[e][1]: PP_SHA[PP[e][1]] for e in ORDER}, "pseudo_dir_note": "러너가 PSEUDO_DIR 로 바꾼다",
                        "W_energy": "`!` total energy (자유에너지 F) · E_int=F+TS 병기", "n_interfaces": 1, "area": "변형된 SE 셀 면적 (V2 는 Ag 셀 면적)"},
           "structures_sha256": P.struct, "jobs": P.jobs,
           "⛔": "S3 봉인 대상 = 이 manifest (좌표 sha · 끝점 · 마스크 · 계보). V2 2단계 좌표는 --v2_ed 부록. INCOMPLETE 3 은 S4 입력 없음 (세고 제외)."}
    json.dump(idx, open(os.path.join(out, "s3_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    json.dump({"schema": "qe_input_set/v1", "date": date, "what": "A′ S4 QE 입력 (S3 패키지 · 쌍극자 구간 개정 2) — run_sese_gpu.sh 호환", "decisions": card["decisions_이_카드가_따르는"],
               "settings": {"pp": {e: PP[e][1] for e in ORDER}, "pp_sha256": idx["settings"]["pp_sha256"], "pseudo_dir_note": "러너가 PSEUDO_DIR 로 바꾼다"},
               "s3_manifest_sha256": _sha(os.path.join(out, "s3_manifest.json")), "jobs": P.jobs}, open(os.path.join(out, "jobs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return idx


def _gaps(at, is_ads):
    y = at.get_positions()
    return [round(float(y[is_ads, 2].min() - y[~is_ads, 2].max()), 3), round(float(at.cell.array[2, 2] - (y[is_ads, 2].max() - y[~is_ads, 2].min())), 3)]


def _geom_meta(geom_dir, n, model):
    if model == "V2":
        fam, reg = "V2", n.split("_", 1)[1]
    else:
        fam, reg = n.rsplit("_", 1)
    return json.load(open(os.path.join(geom_dir, fam, reg, "meta.json"), encoding="utf-8"))


def v2_stage2(pw_out, model_dir, out, s3_manifest, pseudo_dir="/data/work/pseudo", gap=8.0):
    """V2 2단계 — QE relax 출력의 최종 좌표(마지막 실행 · bfgs converged) → d₀ · E(d) · far · G3 · G4 입력 + 부록 manifest."""
    from ase import Atoms
    txt = open(pw_out, errors="ignore").read()
    S.parse_pw(pw_out, "relax", True)                   # 완료·수렴·D3 줄 (P0 규칙)
    k = txt.rfind("Program PWSCF"); t = txt[k:] if k >= 0 else txt
    sym, x = S._read_positions_block(t)
    man = json.load(open(s3_manifest, encoding="utf-8"))
    name = os.path.basename(model_dir.rstrip("/"))
    rec = man["endpoints"][name]
    from ase.io import read
    b0 = read(os.path.join(os.path.dirname(s3_manifest), "structures", f"{name}_bound.extxyz"))
    if sym != b0.get_chemical_symbols():
        raise SlabError("이완 출력의 원자 순서가 S3 bound 와 다르다")
    at = Atoms(sym, positions=x, cell=b0.cell.array, pbc=(True, True, False))
    is_ads = _ads_mask(at, "V2")
    P = Pack(out, pseudo_dir)
    d0 = float(at.get_positions()[is_ads, 2].min() - at.get_positions()[~is_ads, 2].max())
    b, f, em = B.make_endpoints(at, is_ads, gap)
    P.add_struct(f"{name}_dft_bound", b); P.add_struct(f"{name}_dft_far", f)
    dip = em["dipfield"]; dd = {"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}
    P.add_job(f"{name}_dft_bound", b, "V2", dip=dd, tags={"structure": f"{name}_dft_bound", "endpoint": "bound", "d0_A": round(d0, 4)})
    P.add_job(f"{name}_dft_far", f, "V2", dip=dd, tags={"structure": f"{name}_dft_far", "endpoint": "far"})
    for s in ED_SHIFTS:
        a2 = _rigid_shift(b, is_ads, s); tag = f"{name}_Ed_{'m' if s < 0 else 'p'}{abs(s):.1f}".replace(".", "")
        P.add_struct(tag, a2); P.add_job(tag, a2, "V2", dip=dd, tags={"structure": tag, "E(d)": f"d0{s:+.1f}"})
    if name == G3_REPS["V2"]:
        b2 = _c_plus(b, 2.0); f2i = _c_plus(f, 2.0); f2ii = _rigid_shift(_c_plus(f, 2.0), is_ads, 2.0); d2 = _dip_for([b2, f2i, f2ii])
        for tag, a2 in (("G3_c2_bound", b2), ("G3_c2_far_i", f2i), ("G3_c2_far_ii", f2ii)):
            P.add_struct(f"{name}_{tag}", a2); P.add_job(f"{name}_{tag}", a2, "V2", dip={"emaxpos": d2["emaxpos"], "eopreg": d2["eopreg"]}, kind="g3", tags={"structure": f"{name}_{tag}", "G3": tag})
        k1 = (7, 7, 1)
        for tag, a2, kw in (("G4_e70_bound", b, {"ecut": (70.0, 700.0)}), ("G4_e70_far", f, {"ecut": (70.0, 700.0)}), ("G4_k1_bound", b, {"kpts": k1}), ("G4_k1_far", f, {"kpts": k1})):
            P.add_job(f"{name}_{tag}", a2, "V2", dip=dd, kind="g4", tags={"structure": f"{name}_dft_{'bound' if 'bound' in tag else 'far'}", "G4": tag}, **kw)
        for ep, a2 in (("bound", b), ("far", f)):
            p = P.add_job(f"{name}_G4_s05_{ep}", a2, "V2", dip=dd, kind="g4", tags={"structure": f"{name}_dft_{ep}", "G4": f"G4_s05_{ep}"})
            # ⛔ 2026-09-26 실측 결함: `open(p, "w").write(open(p).read()…)` 는 **쓰기용으로 먼저 열어 파일을 비운 뒤** 읽어 빈 파일을 썼다
            #   (V100 에서 s05 두 잡이 'could not find namelist &control' 로 3 초 rc 1). build_s3 처럼 **읽고 나서** 쓴다.
            t = open(p).read()
            if "degauss = 0.01\n" not in t:
                raise SlabError(f"{p}: degauss = 0.01 줄이 없다 — smearing ½ 치환 대상이 아니다")
            open(p, "w").write(t.replace("degauss = 0.01\n", "degauss = 0.005\n")); P.jobs[-1]["pw_in_sha256"] = _sha(p); P.jobs[-1]["tags"]["degauss_halved"] = True
    add = {"schema": "aprime_s3_v2_stage2/v1", "model": name, "pw_out_sha256": _sha(pw_out), "d0_A": round(d0, 4), "endpoints": em, "structures_sha256": P.struct, "jobs": P.jobs,
           "rule": "카드 v5 V2: d₀ = 제약 아래 DFT 국소 이완 간격 · E(d) = d₀−0.3 · +0.3 · +0.6 · far (≥ 8/8) · G3 (i)(ii) · G4 (e70 · k 7×7×1 · smearing ½)"}
    json.dump(add, open(os.path.join(out, "s3_v2_stage2_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    json.dump({"schema": "qe_input_set/v1", "what": f"A′ V2 2단계 ({name})", "settings": {"pp": {e: PP[e][1] for e in ORDER}, "pp_sha256": {PP[e][1]: PP_SHA[PP[e][1]] for e in ORDER}}, "jobs": P.jobs},
              open(os.path.join(out, "jobs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return add


# ─────────────── P2′ 작은 탄소 모델 봉인 (외주 2차 카드 wad_p2small_vasp_card_2026_10_15 · 빌드 ②) ───────────────
P2S_CARD = "db/properties/wad_p2small_vasp_card_2026_10_15.json"
P2S_DECISION = "D-2026-10-15-wad-p2small-vasp-card"
P2S_SAMPLES = (("S_A", "P2S_s_outer/A", "s_outer"), ("Li_A", "P2S_li_outer/A", "li_outer"))
P2S_FMAX, P2S_STEPS = 0.02, 3000            # 카드 G1 (부모 둘만 · S2 와 같다)
P2S_G3_DW, P2S_G3_TRIGGER = 0.01, 0.8       # 카드 G3 문턱 · '발송 전 D3 만 예측 80 % 규칙'
P2S_GAPS = (10.0, 12.0)                     # 기본 끝점 직접 간격 · 80 % 규칙이 발동하면 한 번만 +2 Å (모든 표본의 far 를 같이)
P2S_BIND = {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default", "checkpoint_sha16": "07068e9c76702ca1", "d3_impl": "simple-dftd3"}


def _decision_state(did, ledger=None):
    d = json.load(open(ledger or os.path.join(REPO, "db", "governance", "decisions.json"), encoding="utf-8"))
    rows = [e for e in (d["decisions"] if isinstance(d, dict) else d) if e.get("id") == did]
    return rows[0].get("decision_state") if rows else None


def p2s_d3_g3_prediction(b, f, b2, f2i, f2ii):
    """카드 '발송 전 D3 만 예측' — 외부 D3 2체 (build_v5_vasp_package.d3_ref_eV · simple-dftd3 · VASP 절단 · V5 jobs.json 의 d3_2body_eV_ref 와 같은 함수) 로
    ΔW_i = W_D3(c+2 bound, far_i) − W_D3(bound, far) · ΔW_ii = W_D3(c+2 bound, far_ii) − W_D3(bound, far) [J/m²] · W = (E_far − E_bound)/A.
    ⚠ D3 몫만이다 — PBE 몫은 모른다 (작다고 전체 변화가 작다는 뜻이 아니다 · 카드)."""
    import build_v5_vasp_package as V
    E = {k: V.d3_ref_eV(a) for k, a in (("bound", b), ("far", f), ("c2_bound", b2), ("c2_far_i", f2i), ("c2_far_ii", f2ii))}
    c = b.cell.array
    A = abs(float(c[0, 0] * c[1, 1] - c[0, 1] * c[1, 0]))
    W = lambda eb, ef: (ef - eb) * V.EV_J / (A * V.A2_M2)
    base = W(E["bound"], E["far"])
    di, dii = W(E["c2_bound"], E["c2_far_i"]) - base, W(E["c2_bound"], E["c2_far_ii"]) - base
    lim = P2S_G3_TRIGGER * P2S_G3_DW
    return {"E_D3_2body_eV": E, "area_A2": round(A, 6), "dW_D3_i_J_m2": di, "dW_D3_ii_J_m2": dii, "trigger_J_m2": lim,
            "triggered": bool(max(abs(di), abs(dii)) > lim), "d3_ref": "build_v5_vasp_package.d3_ref_eV (simple-dftd3 2체 · VASP 절단 50.2 / 21.17 Å · 3축 주기)"}


def _p2s_parent(relax_dir, geom_dir, rec_build, name, sub, term):
    """부모 하나 — 계보 (이완 시작 = 레포 초기 구조) · G1 · G2 · 계산기 결박. 하나라도 어긋나면 SlabError (교체 없음)."""
    at, meta, chk, lin = load_relaxed(relax_dir, sub)
    gm = json.load(open(os.path.join(geom_dir, sub, "meta.json"), encoding="utf-8"))
    want = rec_build["samples"][name]["sha256"]["bound"]
    if not (lin["init_sha256"] == gm["sha256"]["bound"] == want):
        raise SlabError(f"{name}: 계보 — 이완 시작 sha {lin['init_sha256'][:16]} 가 레포 초기 구조 {want[:16]} 와 다르다")
    if meta.get("model") != "P2S" or meta.get("term") != term or meta.get("registry") != "A":
        raise SlabError(f"{name}: relax_meta 의 모델·종결·registry 가 {('P2S', term, 'A')} 가 아니다 — {(meta.get('model'), meta.get('term'), meta.get('registry'))}")
    g1 = {"converged_fmax": meta.get("converged_fmax"), "fmax_free_final_eV_A": meta.get("fmax_free_final_eV_A"), "steps_taken": meta.get("steps_taken")}
    if not (g1["converged_fmax"] is True and isinstance(g1["fmax_free_final_eV_A"], (int, float)) and g1["fmax_free_final_eV_A"] <= P2S_FMAX
            and isinstance(g1["steps_taken"], int) and g1["steps_taken"] <= P2S_STEPS):
        raise SlabError(f"{name}: G1 미통과 {g1} (fmax ≤ {P2S_FMAX} · {P2S_STEPS} 스텝 안) — 봉인하지 않는다 (교체 없음 · 1저자 결정)")
    if meta.get("interface_check_flags") or chk.get("flags"):
        raise SlabError(f"{name}: G2 깃발 {meta.get('interface_check_flags') or chk.get('flags')} — 봉인하지 않는다 (교체 없음 · 1저자 결정)")
    c = meta.get("calculator") or {}
    ck = c.get("checkpoint")
    got = {"model": c.get("model"), "task": c.get("task"), "inference_settings": c.get("inference_settings"),
           "checkpoint_sha16": ck[0]["sha256"][:16] if isinstance(ck, list) and ck else None, "d3_impl": str((c.get("d3") or {}).get("impl", ""))}
    if any(got[k] != P2S_BIND[k] for k in ("model", "task", "inference_settings", "checkpoint_sha16")) or not got["d3_impl"].startswith(P2S_BIND["d3_impl"]):
        raise SlabError(f"{name}: 계산기 결박 불일치 {got} ≠ {P2S_BIND}")
    got.update({"fairchem.core": c.get("fairchem.core"), "d3_version": (c.get("d3") or {}).get("version")})
    return at, gm, {"lineage": lin, "G1": g1, "G2_flags": [], "binding": got, "disp_max_A": meta.get("disp_max_A")}


def seal_p2s(relax_dir, geom_dir, out, date=None, gaps=P2S_GAPS, ledger=None, predict=None):
    """P2′ 봉인 (카드 '만들 것' 3–4 단계) — 이완한 부모 둘 → 끝점 (make_endpoints) · p05 (비이완 강체 · far 공유) · S_A G3 세 구조 ·
    발송 전 D3 만 G3 예측 (80 % 규칙: 발동하면 끝점 설계를 한 번만 +2 Å · 그래도 발동하면 멈추고 1저자에게) · 구조 sha · 계보.

    산출: out/structures/<이름>.extxyz 9 개 + out/p2s_seal_manifest.json (structures_sha256 · 집합별 쌍극자 구간 · 표본 쌍 · G3 쌍 ·
      p05 변환 기록 · 부모 계보·G1·G2·결박 · D3 예측 · 코드 sha). VASP 잡 행렬 (설정·k·σ·함수) 은 여기서 정하지 않는다 — 묶음 빌더 몫.
    ⛔ 못 하는 것: 이완·DFT 없음 · G1/G2 를 못 넘은 부모를 고치거나 바꾸지 않는다 (봉인 거부) · D3 예측은 PBE 몫을 모른다.
    """
    st = _decision_state(P2S_DECISION, ledger)
    if st != "active":
        raise SlabError(f"{P2S_DECISION} 가 원장에서 active 가 아니다 ({st}) — 봉인하지 않는다")
    predict = predict or p2s_d3_g3_prediction
    date = date or _dt.date.today().isoformat()
    bp = os.path.join(geom_dir, "build_record.json")
    rec_build = json.load(open(bp, encoding="utf-8"))
    par = {name: _p2s_parent(relax_dir, geom_dir, rec_build, name, sub, term) for name, sub, term in P2S_SAMPLES}
    preds, chosen = [], None
    for gap in gaps:
        S_ = {}
        for name, (at, gm, info) in par.items():
            is_ads = _ads_mask(at, "P2S")
            b, f, em = B.make_endpoints(at, is_ads, gap)
            pr, prec = B.p05_probe(b, f, dz=B.P05_DZ_A, gap=gap, ads_elements=("C",), fixed_idx=gm["fixed_idx"])
            if prec.get("interface_check_flags"):
                raise SlabError(f"{name}_p05: G1p ③ interface_check 깃발 {prec['interface_check_flags']}")
            S_[name] = {"is_ads": is_ads, "bound": b, "far": f, "p05": pr, "p05_rec": prec, "endpoints": em,
                        "dip": B.dip_region([b, f, pr])}
        s = S_["S_A"]
        b2, f2i = _c_plus(s["bound"], 2.0), _c_plus(s["far"], 2.0)
        f2ii = _rigid_shift(f2i, s["is_ads"], 2.0)
        g3 = {"bound": b2, "far_i": f2i, "far_ii": f2ii, "dip": B.dip_region([b2, f2i, f2ii]),
              "gaps_direct_image_A": {"i": _gaps(f2i, s["is_ads"]), "ii": _gaps(f2ii, s["is_ads"])}}
        p = predict(s["bound"], s["far"], b2, f2i, f2ii)
        preds.append({"gap_A": gap, **p})
        if not p["triggered"]:
            chosen = (gap, S_, g3)
            break
    if chosen is None:
        os.makedirs(out, exist_ok=True)
        json.dump({"schema": "p2s_d3_g3_prediction/v1", "date": date, "predictions": preds, "⛔": "80 % 규칙이 끝점 설계 두 번 다 발동 — 봉인하지 않는다 · 1저자에게 묻는다 (카드)"},
                  open(os.path.join(out, "p2s_d3_g3_prediction_refused.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        raise SlabError(f"D3 만 G3 예측이 끝점 {list(gaps)} Å 모두에서 80 % 문턱 ({P2S_G3_TRIGGER * P2S_G3_DW:g} J/m²) 을 넘는다 — 멈추고 1저자에게 묻는다")
    gap, S_, g3 = chosen
    P = Pack(out, None)
    for name, s in S_.items():
        P.add_struct(f"{name}_bound", s["bound"]); P.add_struct(f"{name}_far", s["far"]); P.add_struct(f"{name}_p05_bound", s["p05"])
    for k in ("bound", "far_i", "far_ii"):
        P.add_struct(f"S_A_G3_c2_{k}", g3[k])
    from ase.io import read
    rd = lambda n: read(os.path.join(out, "structures", f"{n}.extxyz"))
    p05_file = {}
    for name, s in S_.items():
        rc = B.check_rigid_shift(rd(f"{name}_bound"), rd(f"{name}_p05_bound"), s["is_ads"], B.P05_DZ_A)
        if not rc["ok"]:
            raise SlabError(f"{name}_p05: 파일에서 다시 읽은 구조가 강체 이동 검사를 못 넘는다 {rc['violations']}")
        p05_file[name] = rc
    code = {os.path.relpath(p, REPO): _sha(p) for p in (os.path.abspath(__file__), os.path.join(HERE, "build_aprime_interfaces.py"), os.path.join(HERE, "se_sym_slab.py"),
                                                         os.path.join(HERE, "relax_uma_d3.py"), os.path.join(HERE, "build_v5_vasp_package.py"))}
    lite = lambda d: {"emaxpos": d["emaxpos"], "eopreg": d["eopreg"], "region_A": d["region_A"], "clearance_A": d["clearance_A"]}
    man = {"schema": "p2s_seal/v1", "date": date, "card": P2S_CARD, "decision": {"id": P2S_DECISION, "state_at_seal": st},
           "relax_dir": relax_dir, "geom_dir": geom_dir, "build_record_sha256": _sha(bp), "code_sha256": code,
           "endpoint_gap_A": gap, "gap_rule": f"기본 {gaps[0]} Å · 80 % 규칙 발동 시 한 번만 {gaps[-1]} Å (카드 '발송 전 D3 만 예측')",
           "d3_g3_prediction": preds,
           "structures_sha256": dict(P.struct),
           "sets": {**{name: {"structures": [f"{name}_bound", f"{name}_far", f"{name}_p05_bound"], "dipfield": lite(s["dip"]), "c_A": s["endpoints"]["c_A"]}
                       for name, s in S_.items()},
                    "S_A_G3": {"structures": ["S_A_G3_c2_bound", "S_A_G3_c2_far_i", "S_A_G3_c2_far_ii"], "dipfield": lite(g3["dip"]),
                               "c_A": round(float(g3["bound"].cell.array[2, 2]), 4), "far_gaps_direct_image_A": g3["gaps_direct_image_A"]}},
           "samples_W_pairs": {"S_A": ["S_A_bound", "S_A_far"], "S_A_p05": ["S_A_p05_bound", "S_A_far"],
                               "Li_A": ["Li_A_bound", "Li_A_far"], "Li_A_p05": ["Li_A_p05_bound", "Li_A_far"]},
           "G3_pairs": {"base": ["S_A_bound", "S_A_far"], "i": ["S_A_G3_c2_bound", "S_A_G3_c2_far_i"], "ii": ["S_A_G3_c2_bound", "S_A_G3_c2_far_ii"]},
           "parents": {name: {**info, "endpoints": {k: S_[name]["endpoints"][k] for k in ("c_A", "delta_A", "d0_A", "gap_rule_A", "bound_gap_direct_image_A", "far_gap_direct_image_A")},
                              "fixed_idx_n": len(gm["fixed_idx"]), "sealed_bound_sha256": P.struct[f"{name}_bound"], "sealed_far_sha256": P.struct[f"{name}_far"]}
                       for name, (at, gm, info) in par.items()},
           "p05": {name: {"parent_bound_sha256": P.struct[f"{name}_bound"], "probe_sha256": P.struct[f"{name}_p05_bound"], "far_shared_sha256": P.struct[f"{name}_far"],
                          "transform": s["p05_rec"]["transform"], "rigid_check_memory": s["p05_rec"]["rigid_check"], "rigid_check_files": p05_file[name],
                          "shared_far": s["p05_rec"]["shared_far"], "interface_check_flags": s["p05_rec"]["interface_check_flags"],
                          "gap_direct_image_A": s["p05_rec"]["gap_direct_image_A"]} for name, s in S_.items()},
           "⛔": "구조·계보·D3 몫 예측만 — UMA·VASP 에너지 없음 · 이 파일을 고치지 않는다 (다시 만들면 새 봉인)"}
    mp = os.path.join(out, "p2s_seal_manifest.json")
    open(mp, "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1, default=float) + "\n")
    man["manifest_sha256"] = _sha(mp)
    return man


def _selftest():
    import tempfile, re
    n_ok = n_bad = 0

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")
    relax = os.path.join(REPO, "db", "raw", "wad_aprime_s2_relax_2026_09_25"); geom = os.path.join(REPO, "db", "inputs", "wad_aprime_s2_geometries_2026_09_25")
    if not os.path.isdir(relax):
        ck("S2 이완 산출물이 repo 에 있다", False, relax); return 1
    with tempfile.TemporaryDirectory() as T:
        m1 = build_s3(relax, geom, os.path.join(T, "a"))
        m2 = build_s3(relax, geom, os.path.join(T, "b"))
        ck("S3: 후보 9 · INCOMPLETE 3", m1["n_candidates"] == 9 and m1["n_incomplete"] == 3, (m1["n_candidates"], m1["n_incomplete"]))
        ck("S3: INCOMPLETE = V3 ×2 + V4_li_outer_A · 소견 기록", set(m1["incomplete_findings"]) == {"V3_s_outer_A", "V3_li_outer_A", "V4_li_outer_A"} and all("소견" in v for v in m1["incomplete_findings"].values()))
        ck("S3: 결정성 — 두 번 빌드해도 구조 sha · 입력 sha 동일", m1["structures_sha256"] == m2["structures_sha256"] and [j["pw_in_sha256"] for j in m1["jobs"]] == [j["pw_in_sha256"] for j in m2["jobs"]])
        ep = m1["endpoints"]
        ck("S3: 모든 후보 far 간격 ≥ 8/8 · 쌍극자 구간 빈 공간", all(e["endpoints"]["far_gap_direct_image_A"][0] >= 8 and e["endpoints"]["far_gap_direct_image_A"][1] >= 8 and e["endpoints"]["dipfield"]["empty_in_both_endpoints"] for e in ep.values()))
        ck("S3: 표본 ⑤ 생성 · ①과 far 공유 여부 기록", m1["sample5"] is not None and "far_same_as_sample1" in m1["sample5"], m1["sample5"])
        g3 = ep["V5_s_outer_A"]["G3"]["far_gaps_check"]
        ck("S3: G3 (i) 8/10 · (ii) 10/8", abs(g3["i"][0] - 8) < 0.05 and abs(g3["i"][1] - 11) < 0.05 and abs(g3["ii"][0] - 10) < 0.05 and abs(g3["ii"][1] - 9) < 0.05, g3)
        kinds = {}
        for j in m1["jobs"]:
            kinds[j["kind"]] = kinds.get(j["kind"], 0) + 1
        ck("S3: 잡 종류 — relax(V2 4) · scf · probe · g3 · g4", kinds.get("relax") == 4 and kinds.get("probe", 0) >= 5 and kinds.get("g3", 0) == 6 and kinds.get("g4", 0) == 12, kinds)
        v2 = open(os.path.join(T, "a", "qe", "V2_top_fcc_relax", "pw.in")).read()
        ck("V2 relax 입력: Ag 6개 '0 0 0' · C 8개 '0 0 1' · 나머지 Ag '1 1 1' · D3 2체 · mv 0.01 · dipfield", v2.count("  0 0 0") == 6 and v2.count("  0 0 1") == 8 and v2.count("  1 1 1") == 6 and "dftd3_threebody = .false." in v2 and "smearing = 'mv'" in v2 and "dipfield = .true." in v2 and "eamp = 0.0d0" in v2, (v2.count("  0 0 0"), v2.count("  0 0 1"), v2.count("  1 1 1")))
        # 개정 2 (2026-09-26): 쌍극자 불연속 구간 = 진공 중앙 — 바닥 영상(c+0.5) 에서 4 Å · 폭 1 Å · 종전 0.93764 (= (c−1.5)/c) 아님
        em_ = float(re.search(r"emaxpos = ([0-9.]+)", v2).group(1)); eo_ = float(re.search(r"eopreg = ([0-9.]+)", v2).group(1)); c_ = ep["V2_top_fcc"]["endpoints"]["c_A"]
        ck("V2 relax 입력: 쌍극자 구간 [c−4.5, c−3.5] (바닥 영상 4 Å · 꼭대기(far) 4 Å) · 종전 [c−1.5, c−0.5] 아님", abs(em_ * c_ - (c_ - 4.5)) < 0.01 and abs(eo_ * c_ - 1.0) < 0.01 and abs(em_ - (c_ - 1.5) / c_) > 0.05, (em_, eo_, c_))
        ck("S3: 모든 후보 쌍극자 여유 ≥ 4/4 Å (dip_region 기록)", all(e["endpoints"]["dipfield"]["clearance_A"]["to_top_atom"] >= 4 - 1e-6 and e["endpoints"]["dipfield"]["clearance_A"]["to_substrate_bottom_image"] >= 4 - 1e-6 for e in ep.values()))
        g3d = ep["V5_s_outer_A"]["G3"]["dip_region_A"]; c5 = ep["V5_s_outer_A"]["endpoints"]["c_A"] + 2.0
        ck("G3 집합(c+2 · bound · far i·ii): 같은 구간 · far(ii) 꼭대기·바닥 영상 양쪽 4 Å", abs(g3d[1] - (c5 + 0.5 - 4.0)) < 0.01 and abs((g3d[1] - g3d[0]) - 1.0) < 0.01, (g3d, c5))
        v4 = open(os.path.join(T, "a", "qe", "V4_s_outer_A_bound", "pw.in")).read()
        ck("V4 입력: gaussian 0.005 · ntyp 6 (Li P S Cl C H) · nat 122 · k 3 3 1", "smearing = 'gaussian'" in v4 and "ntyp = 6" in v4 and "nat = 122" in v4 and "  3 3 1 0 0 0" in v4)
        pr = open(os.path.join(T, "a", "qe", "probe_V5_s_outer_A_far_e70", "pw.in")).read()
        ck("프로브 입력: scf · ecut 70/700 · electron_maxstep 2", "calculation = 'scf'" in pr and "ecutwfc = 70.0" in pr and "electron_maxstep = 2" in pr)
        # ⛔ 음성: 이완 좌표를 손대면 거부
        import shutil
        R2 = os.path.join(T, "relax"); shutil.copytree(relax, R2)
        p = os.path.join(R2, "V5_s_outer_A", "relaxed.extxyz"); open(p, "a").write("\n")
        try:
            build_s3(R2, geom, os.path.join(T, "c")); bad = False
        except SlabError as e:
            bad = "손댄" in str(e)
        ck("⛔음성: relaxed.extxyz 손댐 → 거부", bad)
        # V2 2단계 (합성 pw.out: S3 bound 좌표에 그래핀 z −0.2 Å)
        from ase.io import read
        b0 = read(os.path.join(T, "a", "structures", "V2_top_fcc_bound.extxyz")); x = b0.get_positions().copy(); ads = np.array([s == "C" for s in b0.get_chemical_symbols()]); x[ads, 2] -= 0.2
        lines = ["     Program PWSCF v.7.4.1 starts", "     convergence has been achieved in  10 iterations", "!    total energy              =   -300.00000000 Ry", "     DFT-D3 Dispersion         =   -0.50000000 Ry",
                 "     bfgs converged in  12 scf cycles and  11 bfgs steps", "Begin final coordinates", "", "ATOMIC_POSITIONS (angstrom)"]
        lines += [f"{s:2s} {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}" for s, p in zip(b0.get_chemical_symbols(), x)]
        lines += ["End final coordinates", "     convergence has been achieved in   8 iterations", "!    total energy              =   -300.00100000 Ry", "     DFT-D3 Dispersion         =   -0.50000000 Ry", "   JOB DONE."]
        po = os.path.join(T, "v2.out"); open(po, "w").write("\n".join(lines) + "\n")
        add = v2_stage2(po, os.path.join(T, "a", "V2_top_fcc"), os.path.join(T, "v2s2"), os.path.join(T, "a", "s3_manifest.json"))
        # ⛔ 2026-09-26: s05 입력이 빈 파일이었던 결함 — 내용 · degauss 0.005 · 그 외 base 와 동일 · 두 패키지(S3 · 2단계) 전수 비어 있음 0
        for ep in ("bound", "far"):
            s05 = open(os.path.join(T, "v2s2", "qe", f"V2_top_fcc_G4_s05_{ep}", "pw.in")).read(); base = open(os.path.join(T, "v2s2", "qe", f"V2_top_fcc_dft_{ep}", "pw.in")).read()
            ck(f"2단계 s05_{ep}: 비어 있지 않고 degauss 0.005 · 그 외 base 와 동일", len(s05) > 500 and "degauss = 0.005" in s05 and s05.replace("degauss = 0.005\n", "degauss = 0.01\n").replace(f"G4_s05_{ep}", f"dft_{ep}") == base, len(s05))
        empties = [q for q in glob.glob(os.path.join(T, "**", "pw.in"), recursive=True) if os.path.getsize(q) < 100]
        ck("두 패키지 전수: 빈 pw.in 0", not empties, empties)
        d0_expect = float(b0.get_positions()[ads, 2].min() - b0.get_positions()[~ads, 2].max()) - 0.2
        ck("V2 2단계: d₀ = (S3 bound 간격 − 0.2) · E(d) 3 · far · G3 3 · G4 6 · sha 기록", abs(add["d0_A"] - d0_expect) < 1e-3 and sum(1 for j in add["jobs"] if "Ed_" in j["dir"]) == 3 and sum(1 for j in add["jobs"] if j["kind"] == "g3") == 3 and sum(1 for j in add["jobs"] if j["kind"] == "g4") == 6, (add["d0_A"], len(add["jobs"])))
        # ⛔ 음성: 이완 실패 출력 → 거부
        open(po, "w").write("\n".join(lines).replace("bfgs converged in  12", "bfgs failed after 200 scf cycles and 199 bfgs steps, convergence not achieved") + "\n")
        try:
            v2_stage2(po, os.path.join(T, "a", "V2_top_fcc"), os.path.join(T, "v2s2b"), os.path.join(T, "a", "s3_manifest.json")); bad = False
        except SlabError:
            bad = True
        ck("⛔음성: V2 이완 실패 출력 → 2단계 거부 (P0)", bad)
    # ── P2′ 봉인 (외주 2차 카드) — 가짜 이완 산출물 = 레포 초기 구조에서 흑연을 +0.1 Å 옮긴 것 · 계산기 결박값은 카드 값 ──
    import shutil
    from ase.io import read, write
    pgeom = os.path.join(REPO, "db", "inputs", "wad_p2small_geometries_2026_10_17")
    with tempfile.TemporaryDirectory() as T:
        def fake_relax(root, mut=None):
            for name, sub, term in P2S_SAMPLES:
                d = os.path.join(root, sub); os.makedirs(d, exist_ok=True)
                at = read(os.path.join(pgeom, sub, "bound.extxyz")); x = at.get_positions(); x[_ads_mask(at, "P2S"), 2] += 0.1; at.set_positions(x)
                write(os.path.join(d, "relaxed.extxyz"), at)
                gm = json.load(open(os.path.join(pgeom, sub, "meta.json"), encoding="utf-8"))
                meta = {"model": "P2S", "term": term, "registry": "A", "init_sha256": gm["sha256"]["bound"], "relaxed_sha256": _sha(os.path.join(d, "relaxed.extxyz")),
                        "converged_fmax": True, "fmax_free_final_eV_A": 0.0151, "steps_taken": 321, "interface_check_flags": [], "disp_max_A": 0.1,
                        "calculator": {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default", "fairchem.core": "2.21.0",
                                       "checkpoint": [{"sha256": "07068e9c76702ca1" + "0" * 48}], "d3": {"impl": "simple-dftd3 (python)", "version": "1.6.0"}}}
                if mut:
                    mut(name, meta, d)
                json.dump(meta, open(os.path.join(d, "relax_meta.json"), "w", encoding="utf-8"))
                json.dump({"flags": []}, open(os.path.join(d, "interface_check.json"), "w", encoding="utf-8"))
            return root
        R0 = fake_relax(os.path.join(T, "r0"))
        sm = seal_p2s(R0, pgeom, os.path.join(T, "s0"), date="2026-10-17")
        S0 = os.path.join(T, "s0", "structures")
        names = sorted(n[:-7] for n in os.listdir(S0))
        ck("P2′ 봉인: 구조 9 (표본 4 + far 2 + G3 3) · sha = 파일", len(names) == 9 and all(_sha(os.path.join(S0, f"{n}.extxyz")) == sm["structures_sha256"][n] for n in names), names)
        ck("P2′ 봉인: p05 는 부모 far 를 공유 (표본 쌍) · 끝점 10 Å · D3 예측 기록 (유한)", sm["samples_W_pairs"]["S_A_p05"] == ["S_A_p05_bound", "S_A_far"]
           and sm["samples_W_pairs"]["Li_A_p05"] == ["Li_A_p05_bound", "Li_A_far"] and sm["endpoint_gap_A"] in P2S_GAPS
           and all(np.isfinite(p["dW_D3_i_J_m2"]) and np.isfinite(p["dW_D3_ii_J_m2"]) for p in sm["d3_g3_prediction"]), (sm["endpoint_gap_A"], sm["d3_g3_prediction"][-1]["triggered"]))
        isC = _ads_mask(read(os.path.join(S0, "S_A_bound.extxyz")), "P2S")
        rr = B.check_rigid_shift(read(os.path.join(S0, "S_A_bound.extxyz")), read(os.path.join(S0, "S_A_p05_bound.extxyz")), isC, 0.5)
        fb, fa = read(os.path.join(S0, "S_A_far.extxyz")), read(os.path.join(S0, "S_A_bound.extxyz"))
        ck("P2′ 봉인: 파일에서 p05 = 부모 bound 흡착층 +0.5 Å (G1p ①) · far 는 같은 셀", rr["ok"] and np.allclose(fb.cell.array, fa.cell.array), rr)
        g = sm["sets"]["S_A_G3"]["far_gaps_direct_image_A"]; gp = sm["endpoint_gap_A"]
        ck("P2′ 봉인: G3 (i) 직접 그대로 · 영상 +2 / (ii) 직접 +2 · 영상 그대로 · 셀 c+2",
           abs(g["i"][0] - gp) < 1e-3 and abs(g["i"][1] - (gp + 3)) < 1e-3 and abs(g["ii"][0] - (gp + 2)) < 1e-3 and abs(g["ii"][1] - (gp + 1)) < 1e-3
           and abs(sm["sets"]["S_A_G3"]["c_A"] - sm["sets"]["S_A"]["c_A"] - 2.0) < 1e-3, (g, sm["sets"]["S_A_G3"]["c_A"], sm["sets"]["S_A"]["c_A"]))
        ck("P2′ 봉인: 집합별 쌍극자 구간 (S_A·Li_A·G3) · 계보 (초기 sha = 레포) · 결박값 기록", all("emaxpos" in v["dipfield"] for v in sm["sets"].values())
           and all(sm["parents"][n]["lineage"]["init_sha256"] == json.load(open(os.path.join(pgeom, sub, "meta.json")))["sha256"]["bound"] for n, sub, _ in P2S_SAMPLES)
           and sm["parents"]["S_A"]["binding"]["checkpoint_sha16"] == "07068e9c76702ca1", sm["parents"]["S_A"]["binding"])
        gb, gc = read(os.path.join(S0, "S_A_G3_c2_bound.extxyz")), read(os.path.join(S0, "S_A_bound.extxyz"))
        ck("P2′ 봉인: G3 c+2 bound = 표본 S_A bound 좌표 그대로 (셀만 c+2) · D3 예측 문턱 0.008 J/m² (0.8 × 0.01)",
           np.array_equal(gb.get_positions(), gc.get_positions()) and abs(gb.cell.array[2, 2] - gc.cell.array[2, 2] - 2.0) < 1e-6
           and all(abs(p["trigger_J_m2"] - 0.008) < 1e-12 for p in sm["d3_g3_prediction"]), (gb.cell.array[2, 2], gc.cell.array[2, 2]))
        sm2 = seal_p2s(R0, pgeom, os.path.join(T, "s0b"), date="2026-10-17")
        ck("P2′ 봉인: 결정성 — 두 번 봉인해도 구조 sha 동일", sm2["structures_sha256"] == sm["structures_sha256"])
        cnt = {"n": 0}

        def pred_first(*a):
            cnt["n"] += 1
            p = p2s_d3_g3_prediction(*a); p["triggered"] = cnt["n"] == 1; return p
        sm3 = seal_p2s(R0, pgeom, os.path.join(T, "s3"), date="2026-10-17", predict=pred_first)
        f3, b3 = read(os.path.join(T, "s3", "structures", "S_A_far.extxyz")), read(os.path.join(T, "s3", "structures", "S_A_G3_c2_far_ii.extxyz"))
        i3 = _ads_mask(f3, "P2S")
        ck("80 % 규칙: 10 Å 에서 발동 → 12 Å 로 한 번 옮김 · 예측 둘 기록 · far 직접 12 · G3 (ii) 직접 14",
           sm3["endpoint_gap_A"] == 12.0 and len(sm3["d3_g3_prediction"]) == 2 and abs(_gaps(f3, i3)[0] - 12.0) < 1e-3 and abs(_gaps(b3, i3)[0] - 14.0) < 1e-3,
           (sm3["endpoint_gap_A"], _gaps(f3, i3), _gaps(b3, i3)))

        def pred_always(*a):
            p = p2s_d3_g3_prediction(*a); p["triggered"] = True; return p
        try:
            seal_p2s(R0, pgeom, os.path.join(T, "s4"), predict=pred_always); bad = False
        except SlabError as e:
            bad = "1저자" in str(e) and os.path.isfile(os.path.join(T, "s4", "p2s_d3_g3_prediction_refused.json")) and not os.path.isdir(os.path.join(T, "s4", "structures"))
        ck("⛔음성 80 % 규칙: 두 번 다 발동 → 봉인 거부 · 예측 기록만 · 구조 없음", bad)
        neg = (("relaxed.extxyz 를 손댐", lambda n, m, d: open(os.path.join(d, "relaxed.extxyz"), "a").write(" \n") if n == "Li_A" else None, "sha"),
               ("이완 시작 sha 가 레포 초기 구조가 아님", lambda n, m, d: m.update(init_sha256="0" * 64) if n == "S_A" else None, "계보"),
               ("G1 미수렴", lambda n, m, d: m.update(converged_fmax=False) if n == "Li_A" else None, "G1"),
               ("G1 3001 스텝", lambda n, m, d: m.update(steps_taken=3001) if n == "S_A" else None, "G1"),
               ("G1 fmax 0.021", lambda n, m, d: m.update(fmax_free_final_eV_A=0.021) if n == "S_A" else None, "G1"),
               ("G2 깃발", lambda n, m, d: m.update(interface_check_flags=["비혼합"]) if n == "Li_A" else None, "G2"),
               ("체크포인트 sha 다름", lambda n, m, d: m["calculator"].update(checkpoint=[{"sha256": "f" * 64}]) if n == "S_A" else None, "결박"),
               ("D3 구현 torch-dftd", lambda n, m, d: m["calculator"].update(d3={"impl": "torch-dftd"}) if n == "Li_A" else None, "결박"),
               ("turbo 모드", lambda n, m, d: m["calculator"].update(inference_settings="turbo") if n == "S_A" else None, "결박"),
               ("모델이 P2 (전체 계면)", lambda n, m, d: m.update(model="P2") if n == "S_A" else None, "모델"))
        for i, (lab, mut, key) in enumerate(neg):
            Rn = fake_relax(os.path.join(T, f"rn{i}"), mut)
            try:
                seal_p2s(Rn, pgeom, os.path.join(T, f"sn{i}")); bad = False
            except SlabError as e:
                bad = key in str(e) and not os.path.isdir(os.path.join(T, f"sn{i}", "structures"))
            ck(f"⛔음성 P2′ 봉인: {lab} → 거부 · 구조 안 씀", bad)
        orig_add = Pack.add_struct

        def bad_add(self, name, atoms):
            if name.endswith("_p05_bound"):
                atoms = atoms.copy(); x = atoms.get_positions(); x[_ads_mask(atoms, "P2S"), 0] += 1e-5; atoms.set_positions(x)
            return orig_add(self, name, atoms)
        Pack.add_struct = bad_add
        try:
            seal_p2s(R0, pgeom, os.path.join(T, "s6")); bad = False
        except SlabError as e:
            bad = "파일에서 다시 읽은" in str(e)
        finally:
            Pack.add_struct = orig_add
        ck("⛔음성 P2′ 봉인: 쓴 p05 파일이 메모리 탐침과 어긋나면 (흡착층 x 1e-5 Å) 거부 — 파일 왕복 검사", bad)
        led = os.path.join(T, "ledger.json")
        json.dump({"decisions": [{"id": P2S_DECISION, "decision_state": "proposed"}]}, open(led, "w"))
        try:
            seal_p2s(R0, pgeom, os.path.join(T, "s5"), ledger=led); bad = False
        except SlabError as e:
            bad = "active" in str(e)
        ck("⛔음성 P2′ 봉인: 카드 결정이 active 아님 → 거부", bad)
    print(f"{'✅' if n_bad == 0 else '⛔'} build_aprime_s3 selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--s3", action="store_true")
    ap.add_argument("--relax", default="db/raw/wad_aprime_s2_relax_2026_09_25")
    ap.add_argument("--geom", default="db/inputs/wad_aprime_s2_geometries_2026_09_25")
    ap.add_argument("--out")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--v2_ed", metavar="PW_OUT")
    ap.add_argument("--model_dir")
    ap.add_argument("--s3_manifest", default="db/inputs/wad_aprime_s3_2026_09_25/s3_manifest.json")
    ap.add_argument("--seal_p2s", action="store_true", help="P2′ 봉인 (외주 2차 카드 · 빌드 ②): 이완 부모 둘 → 끝점 · p05 · G3 · D3 만 예측 · sha")
    ap.add_argument("--p2s_relax", default="db/raw/wad_p2small_relax_2026_10_17/relax")
    ap.add_argument("--p2s_geom", default="db/inputs/wad_p2small_geometries_2026_10_17")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.s3:
        if not a.out:
            ap.error("--out 이 필요하다")
        m = build_s3(a.relax, a.geom, a.out, a.pseudo_dir)
        print(json.dumps({"n_candidates": m["n_candidates"], "n_incomplete": m["n_incomplete"], "incomplete": list(m["incomplete_findings"]), "n_jobs": len(m["jobs"]),
                          "jobs_by_kind": {k: sum(1 for j in m["jobs"] if j["kind"] == k) for k in ("relax", "scf", "probe", "g3", "g4")}}, ensure_ascii=False, indent=1))
        return 0
    if a.seal_p2s:
        if not a.out:
            ap.error("--out 이 필요하다")
        m = seal_p2s(a.p2s_relax, a.p2s_geom, a.out)
        print(json.dumps({"endpoint_gap_A": m["endpoint_gap_A"], "n_structures": len(m["structures_sha256"]),
                          "d3_g3_prediction": [{k: p[k] for k in ("gap_A", "dW_D3_i_J_m2", "dW_D3_ii_J_m2", "triggered")} for p in m["d3_g3_prediction"]],
                          "G1": {n: v["G1"] for n, v in m["parents"].items()}, "manifest_sha256": m["manifest_sha256"]}, ensure_ascii=False, indent=1, default=float))
        print(f"→ {a.out}/p2s_seal_manifest.json")
        return 0
    if a.v2_ed:
        if not (a.model_dir and a.out):
            ap.error("--v2_ed 에는 --model_dir 와 --out 이 필요하다")
        add = v2_stage2(a.v2_ed, a.model_dir, a.out, a.s3_manifest, a.pseudo_dir)
        print(json.dumps({k: add[k] for k in ("model", "d0_A", "pw_out_sha256")}, ensure_ascii=False, indent=1)); print(f"→ {a.out}/jobs.json ({len(add['jobs'])} 잡)")
        return 0
    ap.error("--selftest · --s3 · --v2_ed · --seal_p2s 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
