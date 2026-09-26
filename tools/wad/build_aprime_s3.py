#!/usr/bin/env python3
"""build_aprime_s3.py — A′ S3 패키지: S2 이완 좌표 → 끝점(bound·far) 재구성 · 파생 표본 · G3/G4 셀 · QE 입력 · sha 계보 (카드 v5 §0 S3).

    python3 tools/wad/build_aprime_s3.py --s3 --relax db/raw/wad_aprime_s2_relax_2026_09_25 --geom db/inputs/wad_aprime_s2_geometries_2026_09_25 --out db/inputs/wad_aprime_s3_2026_09_25
    python3 tools/wad/build_aprime_s3.py --v2_ed <V2 relax pw.out> --model_dir <S3/V2_top_fcc> --out <dir>   # 2단계: DFT 이완 좌표 → E(d)·far·G3·G4 입력
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
            open(p, "w").write(open(p).read().replace("degauss = 0.01\n", "degauss = 0.005\n")); P.jobs[-1]["pw_in_sha256"] = _sha(p); P.jobs[-1]["tags"]["degauss_halved"] = True
    add = {"schema": "aprime_s3_v2_stage2/v1", "model": name, "pw_out_sha256": _sha(pw_out), "d0_A": round(d0, 4), "endpoints": em, "structures_sha256": P.struct, "jobs": P.jobs,
           "rule": "카드 v5 V2: d₀ = 제약 아래 DFT 국소 이완 간격 · E(d) = d₀−0.3 · +0.3 · +0.6 · far (≥ 8/8) · G3 (i)(ii) · G4 (e70 · k 7×7×1 · smearing ½)"}
    json.dump(add, open(os.path.join(out, "s3_v2_stage2_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    json.dump({"schema": "qe_input_set/v1", "what": f"A′ V2 2단계 ({name})", "settings": {"pp": {e: PP[e][1] for e in ORDER}, "pp_sha256": {PP[e][1]: PP_SHA[PP[e][1]] for e in ORDER}}, "jobs": P.jobs},
              open(os.path.join(out, "jobs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    return add


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
        d0_expect = float(b0.get_positions()[ads, 2].min() - b0.get_positions()[~ads, 2].max()) - 0.2
        ck("V2 2단계: d₀ = (S3 bound 간격 − 0.2) · E(d) 3 · far · G3 3 · G4 6 · sha 기록", abs(add["d0_A"] - d0_expect) < 1e-3 and sum(1 for j in add["jobs"] if "Ed_" in j["dir"]) == 3 and sum(1 for j in add["jobs"] if j["kind"] == "g3") == 3 and sum(1 for j in add["jobs"] if j["kind"] == "g4") == 6, (add["d0_A"], len(add["jobs"])))
        # ⛔ 음성: 이완 실패 출력 → 거부
        open(po, "w").write("\n".join(lines).replace("bfgs converged in  12", "bfgs failed after 200 scf cycles and 199 bfgs steps, convergence not achieved") + "\n")
        try:
            v2_stage2(po, os.path.join(T, "a", "V2_top_fcc"), os.path.join(T, "v2s2b"), os.path.join(T, "a", "s3_manifest.json")); bad = False
        except SlabError:
            bad = True
        ck("⛔음성: V2 이완 실패 출력 → 2단계 거부 (P0)", bad)
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
    if a.v2_ed:
        if not (a.model_dir and a.out):
            ap.error("--v2_ed 에는 --model_dir 와 --out 이 필요하다")
        add = v2_stage2(a.v2_ed, a.model_dir, a.out, a.s3_manifest, a.pseudo_dir)
        print(json.dumps({k: add[k] for k in ("model", "d0_A", "pw_out_sha256")}, ensure_ascii=False, indent=1)); print(f"→ {a.out}/jobs.json ({len(add['jobs'])} 잡)")
        return 0
    ap.error("--selftest · --s3 · --v2_ed 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
