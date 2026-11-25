#!/usr/bin/env python3
"""make_eos_inputs.py — Nd 자리 비교 Q1 · G3 고정셀 + EOS 1 단계: 부피 격자 입력 (두 모델 최저 셀 × 부피 6 점)

  카드: db/properties/ndo_lpscl16_site_stability_estimand_2026_10_14.json §4 G3 (개정 2026-10-15 · 결과 전) · §6 계산 설정
  설계 (결과 전): eos_plan.json (같은 폴더) — 사용자 2026-10-16 '2로해' (설계안 + GPU 자리 ② kgy · cascade 와 같이)
  대상: Q1 단일점 판독 (db/properties/ndo_site_dft_q1_readout_2026_10_16.json) 의 모델별 최저 MP_07 · MLi_04

무엇을 쓰나 (tools/doping/run_force_check_scf.sh 가 읽는 꼴 = <out>/<이름>_x<XXX>/scf.in)
  · 셀 = 1저자 Rietveld 정수화 셀 (db/inputs/ndo_site_2026_10_14/candidates/<종류>/<이름>.xyz 의 셀 —
    6.928 × 6.928 × 34.640 Å · 세 각 60° · 1175.66 Å³) 을 부피 비 x 의 세제곱근으로 **등방 스케일** (모양 고정 · vc-relax 안 씀)
  · 원자 = UMA 이완 구조 (db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15/structures/<이름>.xyz — Q1 단일점과 같은 원본) 의
    **분율 좌표 그대로** (UMA 가 바꾼 셀 모양 — MP_07 은 c 가 +5 % — 을 Rietveld 모양으로 되돌린다)
  · calculation 'relax' (이온만 · BFGS) · forc_conv_thr 1.0d-3 · etot_conv_thr 1.0d-5 · nstep 200 · &CELL 블록 없음
  · 전자 설정 · PP · k (2 2 1 — G4 탐침으로 확인) = 카드 §6 — Q1 의 make_inputs.card_settings · check_input 을 그대로 쓴다
  · prefix 는 Q1 과 같은 이름 (점마다 폴더 · ./tmp 가 따로라 겹치지 않는다)

검사 (하나라도 어긋나면 아무것도 안 쓰고 멈춘다 · 종료 1)
  · Rietveld 셀 = 6.928 · 6.928 · 34.640 Å · 60 · 60 · 60° (허용 1e-3) · 두 후보의 원본 셀이 같다
  · 원자 수 · 조성 = Q1 판독 모델 화학식 (MP Cl8Li31Nd2O3P3S19 66 · MLi Cl8Li21Nd2O3P5S19 58)
  · 격자에 1.04 가 있다 (바닥 확인의 기준점 · eos_plan.json)
  · 점마다 부피 = x × V_Rietveld (상대 1e-9) · 각 60° (1e-6) · check_input (카드 §6 · PP · nosym · nspin 없음 · k)
  · **Q1 단일점 입력 (db/inputs/ndo_site_dft_2026_10_15/<이름>/scf.in) 에서 정해진 곳만 바뀌었다** —
    calculation · etot/forc 문턱 · CELL_PARAMETERS 3 줄 · &IONS 블록 추가. 좌표 · PP · 전자 설정 · k 줄은 바이트가 같아야 한다

⛔ 이 도구가 못 하는 것
  · 계산하지 않는다 · ΔG 를 내지 않는다 (site_dg.py 몫) · 2 단계 (--fit) · 3 단계 (--v0) 는 eos_plan.json 의 결과 전 규칙을 그대로 옮긴 것이다
    (2026-10-17 결과 전 커밋 — 끝점 연장 · BM3 · 바닥 확인 x 1.04 · 0.3 Å · V₀ 1 % 보류 · 시작 좌표 = V₀ 에 가장 가까운 점)
  · 격자가 바닥을 감싸는지 모른다 (끝점 연장 규칙은 eos_plan.json — 결과 뒤 같은 생성기 --extra 로)
  · 이완이 다른 바닥으로 가는지 모른다 (바닥 확인은 2 단계)

  python3 make_eos_inputs.py --selftest
  python3 make_eos_inputs.py --out <폴더>                 # 기본 격자 0.98 … 1.08 (eos_plan.json)
  python3 make_eos_inputs.py --out <폴더> --extra 0.96    # 끝점 연장 (eos_plan.json 규칙이 발동했을 때만)
  python3 make_eos_inputs.py --fit <점 폴더> --json <맞춤.json>               # 2 단계 (12 점 끝난 뒤)
  python3 make_eos_inputs.py --v0 <맞춤.json> --run <점 폴더> --out <root_v0>  # 3 단계 V₀ relax 입력
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "db/inputs/ndo_site_dft_2026_10_15"))
import make_inputs as MI  # noqa: E402  (카드 §6 설정 · 대조 함수 · tools/doping 경로)

PLAN = HERE / "eos_plan.json"
CARD = MI.CARD
UMA = MI.UMA
CAND = REPO / "db/inputs/ndo_site_2026_10_14/candidates"
Q1 = REPO / "db/inputs/ndo_site_dft_2026_10_15"
TARGETS = (("MLi", "MLi_04", "Cl8Li21Nd2O3P5S19", 58), ("MP", "MP_07", "Cl8Li31Nd2O3P3S19", 66))
RIETVELD_CELLPAR = (6.928, 6.928, 34.640, 60.0, 60.0, 60.0)
FORC, ETOT = "1.0d-3", "1.0d-5"
IONS = "&IONS\n    ion_dynamics = 'bfgs'\n/\n"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def plan_grid(plan=PLAN):
    g = json.loads(Path(plan).read_text())["격자"]["x"]
    return [float(x) for x in g]


def tag(name, x):
    return f"{name}_x{int(round(x * 100)):03d}"


def comp_of(atoms):
    return "".join(f"{e}{c}" for e, c in sorted(Counter(atoms.get_chemical_symbols()).items()))


def cell_block(text):
    m = re.search(r"CELL_PARAMETERS angstrom\n((?:.*\n){3})", text)
    return m.group(0) if m else None


def expected_from_q1(q1_text, new_text):
    """Q1 단일점 입력에 '바뀌어도 되는 것' 만 적용한 글 — 새 입력과 바이트가 같아야 한다."""
    t = q1_text.replace("    calculation = 'scf'\n", "    calculation = 'relax'\n", 1)
    t = t.replace("    etot_conv_thr = 1.0d-6\n", f"    etot_conv_thr = {ETOT}\n", 1)
    t = t.replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {FORC}\n", 1)
    old_c, new_c = cell_block(q1_text), cell_block(new_text)
    if old_c is None or new_c is None:
        return None
    t = t.replace(old_c, new_c, 1)
    i = t.find("&ELECTRONS")
    j = t.find("\n/\n", i)
    return None if i < 0 or j < 0 else t[:j + 3] + IONS + t[j + 3:]


def build(out=None, write=True, xs=None, card_path=CARD, uma=UMA, cand=CAND, q1=Q1, gen=None):
    from ase.io import read
    if gen is None:
        from generate_dft_inputs import generate_pwin as gen
    xs = plan_grid() if xs is None else [float(x) for x in xs]
    card = json.loads(Path(card_path).read_text())
    cfg = MI.card_settings(card)
    pdir = cfg["pseudo_dir"]
    bad, texts, man = [], {}, {"점": {}}
    if not out and write:
        raise SystemExit("⛔ --out 이 필요하다")
    if 1.04 not in [round(x, 6) for x in xs] and xs == plan_grid():
        bad.append("격자에 1.04 (바닥 확인 기준점) 가 없다")
    hosts = {}
    for kind, name, formula, nat in TARGETS:
        hp = Path(cand) / kind / f"{name}.xyz"
        host = read(hp)
        cp = host.cell.cellpar()
        if not np.allclose(cp, RIETVELD_CELLPAR, atol=1e-3):
            bad.append(f"{name} Rietveld 셀 {np.round(cp, 4).tolist()} ≠ {list(RIETVELD_CELLPAR)}")
        hosts[name] = host.cell.array.copy()
        src = Path(uma) / "structures" / f"{name}.xyz"
        at = read(src)
        if comp_of(at) != formula or len(at) != nat:
            bad.append(f"{name} 조성 {comp_of(at)} ({len(at)} 원자) ≠ Q1 {formula} ({nat})")
        q1_in = Path(q1) / name / "scf.in"
        q1_text = q1_in.read_text()
        frac = at.get_scaled_positions(wrap=True)
        H = hosts[name]
        VR = abs(np.linalg.det(H))
        for x in xs:
            a2 = at.copy()
            a2.set_cell(H * x ** (1.0 / 3.0), scale_atoms=False)
            a2.set_scaled_positions(frac)
            try:
                t = gen(a2, name, cfg["ecutwfc"], cfg["ecutrho"], cfg["kpoints"], pseudo_dir=pdir,
                        pp_names=cfg["pp"], calculation="relax", nosym=True,
                        smearing=cfg["smearing"], degauss=cfg["degauss"],
                        conv_thr=cfg["conv_thr"], mixing_beta=cfg["mixing_beta"])
            except ValueError as ex:
                bad.append(f"{tag(name, x)}: {ex}")
                continue
            n_cell = len(re.findall(r"^&CELL\n(?:.*\n)*?/\n", t, re.M))
            t = re.sub(r"^&CELL\n(?:.*\n)*?/\n", "", t, flags=re.M)
            t = t.replace("    etot_conv_thr = 1.0d-6\n", f"    etot_conv_thr = {ETOT}\n", 1)
            t = t.replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {FORC}\n", 1)
            tg = tag(name, x)
            if n_cell != 1 or "&CELL" in t:
                bad.append(f"{tg}: &CELL 블록을 정확히 하나 지우지 못했다 ({n_cell})")
            for key, val in (("etot_conv_thr", ETOT), ("forc_conv_thr", FORC)):
                if re.findall(rf"^\s*{key}\s*=\s*(\S+)", t, re.M) != [val]:
                    bad.append(f"{tg}: {key} ≠ {val}")
            if t.count(IONS) != 1:
                bad.append(f"{tg}: &IONS bfgs 블록이 하나가 아니다")
            bad += [f"{tg}: {b}" for b in MI.check_input(t, cfg, pdir, "relax", nat, cfg["kpoints"])]
            cb = cell_block(t)
            M = np.array([[float(v) for v in ln.split()] for ln in cb.splitlines()[1:4]]) if cb else None
            if M is None or abs(abs(np.linalg.det(M)) / (x * VR) - 1) > 1e-9:
                bad.append(f"{tg}: 부피가 x × V_Rietveld 가 아니다")
            else:
                ang = [np.degrees(np.arccos(np.dot(M[i], M[j]) / np.linalg.norm(M[i]) / np.linalg.norm(M[j])))
                       for i, j in ((1, 2), (0, 2), (0, 1))]
                if not np.allclose(ang, 60.0, atol=1e-6):
                    bad.append(f"{tg}: 각이 60° 가 아니다 {np.round(ang, 6).tolist()}")
            exp = expected_from_q1(q1_text, t)
            if exp is None or exp != t:
                bad.append(f"{tg}: Q1 단일점 입력에서 정해진 곳 (calculation · 문턱 · CELL · &IONS) 밖이 바뀌었다")
            texts[tg] = t
            man["점"][tg] = {"이름": name, "종류": kind, "x": x, "V_A3": round(x * VR, 6),
                            "셀_길이_A": [round(float(v), 6) for v in np.linalg.norm(H * x ** (1 / 3), axis=1)],
                            "원자": nat, "조성": formula}
    if bad:
        raise SystemExit("⛔ 입력을 쓰지 않았다 —\n   " + "\n   ".join(bad))
    man.update({"카드": str(Path(card_path).relative_to(REPO)) if Path(card_path).is_relative_to(REPO) else str(card_path),
                "카드_sha256": sha256(card_path), "설계": "db/inputs/ndo_site_eos_2026_10_16/eos_plan.json",
                "설계_sha256": sha256(PLAN), "설정_카드_6": cfg, "격자_x": xs,
                "relax": {"forc_conv_thr": FORC, "etot_conv_thr": ETOT, "nstep": 200, "ion_dynamics": "bfgs", "CELL": "없음"},
                "생성_함수": "tools/doping/generate_dft_inputs.py::generate_pwin (+ &CELL 제거 · 문턱 두 줄)",
                "생성_함수_sha256": sha256(REPO / "tools/doping/generate_dft_inputs.py"),
                "출처": {name: {"UMA_구조": f"db/raw/ndo_site_2026_10_14/uma_rietveld_2026_10_15/structures/{name}.xyz",
                                "UMA_구조_sha256": sha256(Path(uma) / "structures" / f"{name}.xyz"),
                                "Rietveld_셀": f"db/inputs/ndo_site_2026_10_14/candidates/{kind}/{name}.xyz",
                                "Rietveld_셀_sha256": sha256(Path(cand) / kind / f"{name}.xyz"),
                                "Q1_입력_sha256": sha256(Path(q1) / name / "scf.in")}
                         for kind, name, _, _ in TARGETS}})
    for tg, t in texts.items():
        man["점"][tg]["입력_sha256"] = hashlib.sha256(t.encode()).hexdigest()
    if write:
        o = Path(out)
        for tg, t in texts.items():
            (o / tg).mkdir(parents=True, exist_ok=True)
            (o / tg / "scf.in").write_text(t)
        mp = o / ("inputs_manifest.json" if xs == plan_grid() else f"inputs_manifest_extra_{'_'.join(tag('x', x)[2:] for x in xs)}.json")
        mp.write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    return man, texts


# ─────────────── 2 단계 맞춤 · 3 단계 V₀ 입력 — eos_plan.json 의 결과 전 규칙 그대로 (결과 전 커밋) ───────────────
RY_EV, BOHR_A = 13.605693122994, 0.529177210903
BASIN_REF_X, BASIN_FLAG_A, V0_SPLIT_REL, E_V0_NOTE_EV, V_FIXED_REL = 1.04, 0.3, 0.01, 0.005, 1e-6
EXTEND = {0.98: 0.96, 1.08: 1.10}        # 끝점 연장 — 한 번만 · 그 바깥은 사용자


def fc_ok(out_text, in_text):
    """tools/doping/run_force_check_scf.sh 의 _fc_ok 와 같다 (relax · tstress): JOB DONE · SCF 수렴 · 힘 · (tstress) 응력 · 'bfgs converged in'."""
    if not all(k in out_text for k in ("JOB DONE", "convergence has been achieved", "Forces acting on atoms")):
        return False
    if re.search(r"tstress *= *\.true\.", in_text, re.I) and not re.search(r"total +stress", out_text):
        return False
    if re.search(r"calculation *= *'(vc-)?relax'", in_text, re.I) and "bfgs converged in" not in out_text:
        return False
    return True


def read_point(d):
    """점 폴더 (scf.in · scf.out) → 완료 · 마지막 '!' 에너지 · 출력 셀 부피 · 입력 부피 · 이완 분율 좌표 (ASE espresso-out 마지막 구조)."""
    d = Path(d)
    rec = {"dir": d.name}
    try:
        tin, tout = (d / "scf.in").read_text(), (d / "scf.out").read_text(errors="replace")
    except OSError as ex:
        return {**rec, "ok": False, "why": f"파일 없음 ({ex.__class__.__name__})"}
    rec["ok"] = fc_ok(tout, tin)
    if not rec["ok"]:
        return {**rec, "why": "미완료 (러너 _fc_ok 와 같은 판정)"}
    e = re.findall(r"^!\s+total energy\s+=\s+(\S+)\s+Ry", tout, re.M)
    vo = re.findall(r"unit-cell volume\s+=\s+(\S+)\s+\(a\.u\.\)\^3", tout)
    cb = cell_block(tin)
    if not e or not vo or cb is None:
        return {**rec, "ok": False, "why": "에너지·부피·입력 셀을 못 읽었다"}
    M = np.array([[float(v) for v in ln.split()] for ln in cb.splitlines()[1:4]])
    from ase.io import read
    at = read(str(d / "scf.out"), format="espresso-out", index=-1)
    rec.update({"E_Ry": float(e[-1]), "E_eV": float(e[-1]) * RY_EV, "V_out_A3": float(vo[-1]) * BOHR_A ** 3, "V_in_A3": abs(float(np.linalg.det(M))),
                "frac": at.get_scaled_positions(wrap=False), "cell": at.cell.array.copy(), "symbols": at.get_chemical_symbols()})
    return rec


def basin_dev(frac, ref_frac, ref_cell):
    """분율 좌표 최소 이미지 차를 기준 셀 (x 1.04) 에서 Å 로 — 원자 평균 (lpsocl 선례)."""
    df = frac - ref_frac
    df -= np.round(df)
    return float(np.linalg.norm(df @ ref_cell, axis=1).mean())


def bm3(V, E):
    from ase.eos import EquationOfState
    eos = EquationOfState(np.asarray(V, float), np.asarray(E, float), eos="birchmurnaghan")
    v0, e0, B = eos.fit()
    res = np.asarray(E, float) - eos.func(np.asarray(V, float), *eos.eos_parameters)
    return {"V0_A3": float(v0), "E0_eV": float(e0), "B0_GPa": float(B) * 160.21766208, "rms_meV": float(np.sqrt(np.mean(res ** 2)) * 1000), "n": len(V)}


def fit_cell(points, grid=None):
    """한 셀의 점들 (read_point 결과 · x 키) → 상태 · 맞춤 · 다음 할 일. 규칙은 eos_plan.json 2단계 그대로 — 결과를 보고 바꾸지 않는다."""
    grid = grid or plan_grid()
    have = {round(p["x"], 2): p for p in points}
    miss = [x for x in grid if round(x, 2) not in have]
    bad = [p["dir"] for p in points if not p.get("ok")]
    if miss or bad:
        return {"status": "미완료", "missing_x": miss, "failed": bad,
                "next": "실패 점은 같은 입력으로 한 번 다시 · 두 번 실패면 사용자 (빼고 맞추지 않는다)"}
    fixed = [p["dir"] for p in points if abs(p["V_out_A3"] / p["V_in_A3"] - 1) > V_FIXED_REL]
    if fixed:
        return {"status": "멈춤", "why": f"출력 셀 부피가 입력과 다르다 (고정셀이 아니다) {fixed}"}
    xs = sorted(have)
    xmin = min(xs, key=lambda x: have[x]["E_eV"])
    tab = [{"x": x, "V_A3": have[x]["V_out_A3"], "E_eV": have[x]["E_eV"]} for x in xs]
    if xmin == xs[0] or xmin == xs[-1]:
        ext = EXTEND.get(xmin)
        if ext is not None and round(ext, 2) not in have:
            return {"status": "끝점 연장", "E_min_x": xmin, "extend_x": ext, "points": tab,
                    "next": f"make_eos_inputs.py --extra {ext} (두 셀 함께 · 한 번만) → 그 점을 돌린 뒤 다시 맞춘다"}
        return {"status": "사용자", "E_min_x": xmin, "points": tab, "why": "끝점 연장 뒤에도 최저점이 끝 — 더 바꾸지 않는다 (eos_plan.json)"}
    if len(xs) < 4:
        return {"status": "멈춤", "why": "4 점 미만"}
    ref = have.get(round(BASIN_REF_X, 2))
    for t in tab:
        t["basin_dev_A"] = basin_dev(have[t["x"]]["frac"], ref["frac"], ref["cell"])
        t["basin_flag"] = t["basin_dev_A"] > BASIN_FLAG_A
    fit = bm3([t["V_A3"] for t in tab], [t["E_eV"] for t in tab])
    flagged = [t["x"] for t in tab if t["basin_flag"]]
    rec = {"status": "V0_relax", "points": tab, "fit_all": fit, "basin_ref_x": BASIN_REF_X, "basin_flag_A": BASIN_FLAG_A, "flagged_x": flagged}
    if flagged:
        keep = [t for t in tab if not t["basin_flag"]]
        if len(keep) < 4:
            return {**rec, "status": "사용자", "why": f"바닥 확인 표시 {flagged} — 남은 점 4 미만이라 둘째 맞춤을 못 한다 (판정 보류)"}
        f2 = bm3([t["V_A3"] for t in keep], [t["E_eV"] for t in keep])
        rec["fit_no_flagged"] = f2
        if abs(f2["V0_A3"] / fit["V0_A3"] - 1) > V0_SPLIT_REL:
            return {**rec, "status": "사용자", "why": f"표시 점을 뺀 맞춤의 V₀ 가 {100 * abs(f2['V0_A3'] / fit['V0_A3'] - 1):.2f} % 다르다 (> 1 %) — 판정 보류"}
    near = min(xs, key=lambda x: abs(have[x]["V_out_A3"] - fit["V0_A3"]))
    rec.update({"V0_start_from_x": near, "x0": fit["V0_A3"] / have[near]["V_in_A3"] * near,
                "next": "make_eos_inputs.py --v0 <이 파일> --run <점 폴더> --out <root_v0> → V₀ relax → site_dg.py --qe <root_v0> --expect 1 --top 1 --thresholds Nd=0.10"})
    return rec


def fit_all(run_dir):
    """run_dir/<이름>_x<XXX>/ (scf.in · scf.out) → 두 셀 맞춤 · 전체 상태. 출력에 W 같은 값은 없다 (Nd 자리 에너지)."""
    out = {"schema": "ndo_site_eos_fit/v1", "plan": "db/inputs/ndo_site_eos_2026_10_16/eos_plan.json", "plan_sha256": sha256(PLAN),
           "tool_sha256": sha256(Path(__file__)), "cells": {}}
    for kind, name, formula, nat in TARGETS:
        pts = []
        for d in sorted(Path(run_dir).glob(f"{name}_x[0-9][0-9][0-9]")):
            p = read_point(d)
            p["x"] = int(d.name[-3:]) / 100.0
            if p.get("ok") and len(p.get("symbols", [])) != nat:
                p.update(ok=False, why=f"원자 수 {len(p['symbols'])} ≠ {nat}")
            pts.append(p)
        out["cells"][name] = fit_cell(pts)
    st = [c["status"] for c in out["cells"].values()]
    out["status"] = "V0_relax" if all(x == "V0_relax" for x in st) else ("끝점 연장" if "끝점 연장" in st and not ({"사용자", "멈춤"} & set(st)) else
                                                                       ("미완료" if "미완료" in st and not ({"사용자", "멈춤"} & set(st)) else "사용자"))
    return out


def v0_inputs(fit, run_dir, out=None, write=True, card_path=CARD, cand=CAND, q1=Q1, gen=None):
    """3 단계 — V₀ 셀 (Rietveld × (V₀/V_ref)^(1/3)) · 시작 좌표 = V₀ 에 가장 가까운 격자점의 이완 분율 좌표 · 같은 relax 설정.
    대조: Q1 단일점 입력에서 calculation · 문턱 · CELL · &IONS · **좌표 줄** 만 바뀌었다 (좌표는 이완 결과라 바뀐다)."""
    from ase.io import read
    if gen is None:
        from generate_dft_inputs import generate_pwin as gen
    if fit.get("status") != "V0_relax":
        raise SystemExit(f"⛔ 맞춤 상태 {fit.get('status')} — V₀ 입력을 만들지 않는다")
    cfg = MI.card_settings(json.loads(Path(card_path).read_text()))
    bad, texts, man = [], {}, {"셀": {}}
    for kind, name, formula, nat in TARGETS:
        c = fit["cells"][name]
        H = read(Path(cand) / kind / f"{name}.xyz").cell.array.copy()
        VR = abs(np.linalg.det(H))
        x0 = c["fit_all"]["V0_A3"] / VR
        src = read_point(Path(run_dir) / tag(name, c["V0_start_from_x"]))
        if not src.get("ok"):
            bad.append(f"{name}: 시작 점 {tag(name, c['V0_start_from_x'])} 을 못 읽었다"); continue
        at = read(Path(UMA) / "structures" / f"{name}.xyz")
        if src["symbols"] != at.get_chemical_symbols():
            bad.append(f"{name}: 시작 점 원자 순서가 원본과 다르다"); continue
        a2 = at.copy(); a2.set_cell(H * x0 ** (1.0 / 3.0), scale_atoms=False); a2.set_scaled_positions(src["frac"])
        t = gen(a2, name, cfg["ecutwfc"], cfg["ecutrho"], cfg["kpoints"], pseudo_dir=cfg["pseudo_dir"], pp_names=cfg["pp"], calculation="relax", nosym=True,
                smearing=cfg["smearing"], degauss=cfg["degauss"], conv_thr=cfg["conv_thr"], mixing_beta=cfg["mixing_beta"])
        t = re.sub(r"^&CELL\n(?:.*\n)*?/\n", "", t, flags=re.M)
        t = t.replace("    etot_conv_thr = 1.0d-6\n", f"    etot_conv_thr = {ETOT}\n", 1).replace("    forc_conv_thr = 1.0d-4\n", f"    forc_conv_thr = {FORC}\n", 1)
        bad += [f"{name}: {b}" for b in MI.check_input(t, cfg, cfg["pseudo_dir"], "relax", nat, cfg["kpoints"])]
        q1t = (Path(q1) / name / "scf.in").read_text()
        pos = lambda u: re.search(r"ATOMIC_POSITIONS crystal\n.*?(?=K_POINTS)", u, re.S)
        q1x = q1t.replace(pos(q1t).group(0), pos(t).group(0), 1)
        exp = expected_from_q1(q1x, t)
        if exp is None or exp != t:
            bad.append(f"{name}: Q1 단일점 입력에서 정해진 곳 (calculation · 문턱 · CELL · &IONS · 좌표) 밖이 바뀌었다")
        cb = cell_block(t); M = np.array([[float(v) for v in ln.split()] for ln in cb.splitlines()[1:4]])
        if abs(abs(np.linalg.det(M)) / c["fit_all"]["V0_A3"] - 1) > 1e-9:
            bad.append(f"{name}: 부피 ≠ V₀")
        texts[name] = t
        man["셀"][name] = {"x0": x0, "V0_A3": c["fit_all"]["V0_A3"], "start_from": tag(name, c["V0_start_from_x"]), "입력_sha256": hashlib.sha256(t.encode()).hexdigest()}
    if bad:
        raise SystemExit("⛔ V₀ 입력을 쓰지 않았다 —\n   " + "\n   ".join(bad))
    man.update({"fit_sha256": fit.get("_sha256"), "rule": "eos_plan.json 3단계 — E(V₀) 는 이 relax 의 에너지 (BM3 E₀ 아님) · 차 > 5 meV 면 기록·표시"})
    if write:
        o = Path(out)
        for n, t in texts.items():
            (o / n).mkdir(parents=True, exist_ok=True); (o / n / "scf.in").write_text(t)
        (o / "v0_inputs_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=2) + "\n")
    return man, texts


def _selftest():
    import copy
    import shutil
    import tempfile
    ok = []

    def chk(c, m):
        ok.append(bool(c))
        print(("  ✓ " if c else "  ✗ ") + m)

    def must_stop(fn, m, needle):
        try:
            fn()
        except SystemExit as ex:
            chk(needle in str(ex), m + f" — {str(ex).splitlines()[-1].strip()[:90]}")
            return
        chk(False, m + " → 멈추지 않았다")

    man, texts = build(write=False)
    chk(len(texts) == 12 and sorted({m["이름"] for m in man["점"].values()}) == ["MLi_04", "MP_07"], f"입력 12 개 (2 셀 × 6 부피) — {len(texts)}")
    chk([m["x"] for m in man["점"].values() if m["이름"] == "MP_07"] == [0.98, 1.0, 1.02, 1.04, 1.06, 1.08], "격자 0.98 … 1.08 (eos_plan.json)")
    chk(all("calculation = 'relax'" in t and "&CELL" not in t and t.count(IONS) == 1 for t in texts.values()), "전부 relax · &CELL 없음 · &IONS bfgs 하나")
    chk(all(abs(m["V_A3"] / (m["x"] * 1175.662) - 1) < 1e-5 for m in man["점"].values()), "부피 = x × 1175.66 Å³")
    keys = "ecutwfc|ecutrho|occupations|smearing|degauss|nosym|conv_thr|mixing_mode|mixing_beta|electron_maxstep|diagonalization|nspin"
    sig = lambda t: tuple(sorted(re.sub(r"\s", "", x) for x in re.findall(rf"^ *(?:{keys}) *=.*$", t, re.M)))  # noqa: E731
    q1sig = sig((Q1 / "MP_07" / "scf.in").read_text())
    chk(all(sig(t) == q1sig for t in texts.values()), "러너 설정 균일성 키가 12 개 모두 Q1 단일점과 같다")
    t0 = texts["MP_07_x104"]
    pos_new = re.search(r"ATOMIC_POSITIONS crystal\n(.*?)K_POINTS", t0, re.S).group(1)
    pos_q1 = re.search(r"ATOMIC_POSITIONS crystal\n(.*?)K_POINTS", (Q1 / "MP_07" / "scf.in").read_text(), re.S).group(1)
    chk(pos_new == pos_q1, "좌표 줄이 Q1 단일점 입력과 바이트가 같다 (분율 좌표 그대로)")
    # ── 음성 ──
    tmp = Path(tempfile.mkdtemp())
    try:
        c2 = tmp / "cand"
        shutil.copytree(CAND, c2)
        from ase.io import read, write as awrite
        a = read(c2 / "MP" / "MP_07.xyz")
        cp = a.cell.cellpar()
        cp[5] = 59.0
        a.set_cell(cp, scale_atoms=True)
        awrite(c2 / "MP" / "MP_07.xyz", a)
        must_stop(lambda: build(write=False, cand=c2), "[음성] Rietveld 셀 각이 59° 면 멈춘다", "Rietveld 셀")
        u2 = tmp / "uma"
        (u2 / "structures").mkdir(parents=True)
        for f in (UMA / "structures").glob("*.xyz"):
            (u2 / "structures" / f.name).write_bytes(f.read_bytes())
        (u2 / "structures" / "MLi_04.xyz").write_bytes((UMA / "structures" / "MP_07.xyz").read_bytes())
        must_stop(lambda: build(write=False, uma=u2), "[음성] MLi_04 자리에 MP_07 구조가 끼면 (조성 다름) 멈춘다", "조성")
        q2 = tmp / "q1"
        shutil.copytree(Q1, q2)
        p = q2 / "MP_07" / "scf.in"
        lines = p.read_text().splitlines(keepends=True)
        k = next(i for i, ln in enumerate(lines) if ln.startswith("ATOMIC_POSITIONS"))
        lines[k + 1] = lines[k + 1].replace("0.", "0.1", 1)
        p.write_text("".join(lines))
        must_stop(lambda: build(write=False, q1=q2), "[음성] Q1 입력과 좌표 한 줄이 다르면 멈춘다", "Q1 단일점 입력에서")
        import generate_dft_inputs as g
        orig = g.generate_pwin
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **{**k, "degauss": 0.02})),
                  "[음성] 생성 함수가 degauss 를 바꾸면 멈춘다", "degauss")
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **k).replace("&CELL\n", "&CELL \n")),
                  "[음성] &CELL 블록을 못 지우면 멈춘다", "&CELL")
        must_stop(lambda: build(write=False, gen=lambda *a, **k: orig(*a, **{**k, "calculation": "vc-relax"})),
                  "[음성] 생성 결과가 vc-relax 면 멈춘다", "calculation")
        cardp = tmp / "card.json"
        cj = json.loads(CARD.read_text())
        cj2 = copy.deepcopy(cj)
        cj2["6_규약_대조"]["계산_설정"]["K_POINTS"] = "automatic 3 3 1 0 0 0"
        cardp.write_text(json.dumps(cj2, ensure_ascii=False))
        must_stop(lambda: build(write=False, card_path=cardp), "[음성] 카드 k 가 Q1 과 달라지면 (Q1 입력과 어긋남) 멈춘다", "Q1 단일점 입력에서")
        m3, t3 = build(write=False, xs=[0.96])
        chk(sorted(t3) == ["MLi_04_x096", "MP_07_x096"], "--extra 0.96 은 두 셀 끝점 하나씩만 만든다")
        # ── 2 단계 맞춤 (결과 전 규칙) ──
        ok_out = "convergence has been achieved\nForces acting on atoms\n     total   stress\n     bfgs converged in   3 scf cycles\nJOB DONE.\n"
        rin = "calculation = 'relax'\ntstress = .true.\n"
        chk(fc_ok(ok_out, rin) and not fc_ok(ok_out.replace("bfgs converged in", "x"), rin) and not fc_ok(ok_out.replace("total   stress", "x"), rin)
            and fc_ok(ok_out.replace("total   stress", "x"), "calculation = 'relax'\n") and not fc_ok(ok_out.replace("JOB DONE", "x"), rin),
            "fc_ok = 러너 _fc_ok (JOB DONE · SCF · 힘 · tstress 면 응력 · relax 면 bfgs converged in)")
        rp = tmp / "real"; rp.mkdir()
        src = REPO / "db/raw/wad_cc_graphite_2026_09_28/stage1/CC_S33_AB_relax"
        (rp / "scf.in").write_text((src / "pw.in").read_text()); (rp / "scf.out").write_text((src / "pw.out").read_text())
        pr = read_point(rp)
        chk(pr["ok"] and abs(pr["V_out_A3"] / pr["V_in_A3"] - 1) < 1e-6 and abs(pr["E_Ry"] + 221.43988647) < 1e-8 and pr["frac"].shape == (12, 3),
            f"실물 QE relax 출력 읽기 (WAD-CC S33 AB) — 완료 · '!' 에너지 · 부피 입력=출력 · 분율 좌표 12 ({pr.get('V_out_A3')})")
        from ase.eos import birchmurnaghan
        VR = 1175.662
        rng = np.random.default_rng(0)
        base_frac = rng.random((10, 3)); Href = np.eye(3) * (1.04 * VR) ** (1 / 3)

        def synth(v0x, xs=(0.98, 1.0, 1.02, 1.04, 1.06, 1.08), shift=None, drop=None, fail=None, vbad=None):
            pts = []
            for x in xs:
                if drop is not None and abs(x - drop) < 1e-9:
                    continue
                V = x * VR
                E = birchmurnaghan(V, -100.0, 0.25, 4.5, v0x * VR)
                f = base_frac.copy()
                if shift and abs(x - shift[0]) < 1e-9:
                    f[:, 0] += shift[1] / Href[0, 0]
                pts.append({"dir": tag("T", x), "x": x, "ok": not (fail is not None and abs(x - fail) < 1e-9), "E_eV": E, "V_out_A3": V * (1.01 if vbad == x else 1.0),
                            "V_in_A3": V, "frac": f, "cell": Href, "symbols": ["X"] * 10})
            return pts
        c1 = fit_cell(synth(1.035))
        chk(c1["status"] == "V0_relax" and abs(c1["fit_all"]["V0_A3"] / (1.035 * VR) - 1) < 1e-6 and c1["V0_start_from_x"] == 1.04 and not c1["flagged_x"],
            f"맞춤: BM3 합성 곡선 V₀ 1.035 V_R 복원 · 시작 점 = 가장 가까운 1.04 · 표시 없음 ({c1.get('fit_all', {}).get('V0_A3')})")
        c2 = fit_cell(synth(0.95))
        chk(c2["status"] == "끝점 연장" and c2["extend_x"] == 0.96, "끝점: 최저점이 0.98 이면 0.96 연장 (한 번)")
        c3 = fit_cell(synth(0.90, xs=(0.96, 0.98, 1.0, 1.02, 1.04, 1.06, 1.08)))
        chk(c3["status"] == "사용자", "⛔음성 끝점: 연장 뒤에도 최저점이 끝 (0.96) → 사용자 (더 바꾸지 않는다)")
        c3b = fit_cell(synth(1.12))
        chk(c3b["status"] == "끝점 연장" and c3b["extend_x"] == 1.10, "끝점: 최저점이 1.08 이면 1.10 연장")
        chk(fit_cell(synth(1.035, drop=1.02))["status"] == "미완료" and fit_cell(synth(1.035, fail=1.06))["status"] == "미완료",
            "⛔음성 미완료: 점이 빠지거나 실패면 맞추지 않는다 (빼고 맞추지 않는다)")
        chk(fit_cell(synth(1.035, vbad=1.0))["status"] == "멈춤", "⛔음성 고정셀: 출력 부피 ≠ 입력 부피 → 멈춤")
        c4 = fit_cell(synth(1.035, shift=(1.08, 0.5)))
        chk(c4["flagged_x"] == [1.08] and "fit_no_flagged" in c4 and c4["status"] in ("V0_relax", "사용자"), f"바닥 확인: 0.5 Å 옮긴 점 (> 0.3) 표시 · 둘째 맞춤 기록 ({c4['status']})")
        pts5 = synth(1.035, shift=(1.06, 0.5)); [p.update(E_eV=p["E_eV"] - 0.5) for p in pts5 if abs(p["x"] - 1.06) < 1e-9]
        c5 = fit_cell(pts5)
        chk(c5["status"] == "사용자" and "1 %" in c5.get("why", ""), f"⛔음성 바닥 확인: 표시 점이 V₀ 를 1 % 넘게 끌면 판정 보류 → 사용자 ({c5.get('why', c5['status'])})")
        fa = fit_all(tmp)
        chk(fa["status"] == "사용자" or fa["status"] == "미완료", f"fit_all: 점 폴더가 없으면 맞추지 않는다 ({fa['status']})")
        try:
            v0_inputs({"status": "미완료"}, tmp, write=False); vb = False
        except SystemExit as ex:
            vb = "V₀ 입력을 만들지 않는다" in str(ex)
        chk(vb, "⛔음성 V₀ 입력: 맞춤 상태가 V0_relax 가 아니면 만들지 않는다")
        from ase.io import read as _rd
        fake_fit = {"status": "V0_relax", "cells": {}}
        for kind, name, formula, nat in TARGETS:
            fake_fit["cells"][name] = {"fit_all": {"V0_A3": 1.031 * VR}, "V0_start_from_x": 1.04}
        G = globals(); orig_rp = G["read_point"]          # 시작 점 읽기만 대역 (UMA 원본 분율 좌표) — v0_inputs 의 나머지 경로는 그대로
        G["read_point"] = lambda d: {"ok": True, "frac": _rd(UMA / "structures" / f"{Path(d).name.rsplit('_x', 1)[0]}.xyz").get_scaled_positions(wrap=True),
                                     "symbols": _rd(UMA / "structures" / f"{Path(d).name.rsplit('_x', 1)[0]}.xyz").get_chemical_symbols()}
        try:
            mv, tv = v0_inputs(fake_fit, tmp, write=False)
        finally:
            G["read_point"] = orig_rp
        Mv = np.array([[float(v) for v in ln.split()] for ln in cell_block(tv["MP_07"]).splitlines()[1:4]])
        chk(sorted(tv) == ["MLi_04", "MP_07"] and abs(abs(np.linalg.det(Mv)) / (1.031 * VR) - 1) < 1e-9 and "calculation = 'relax'" in tv["MP_07"]
            and "&CELL" not in tv["MP_07"] and tv["MP_07"].count(IONS) == 1,
            "V₀ 입력: 두 셀 · 부피 = V₀ · relax · &CELL 없음 · &IONS 하나 · Q1 입력과 정해진 곳 (좌표 포함) 만 다름")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"selftest: {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--extra", nargs="+", type=float, help="끝점 연장 (eos_plan.json 규칙이 발동했을 때만)")
    ap.add_argument("--fit", metavar="RUN_DIR", help="2 단계: 점 폴더들 (<이름>_x<XXX>/scf.in·scf.out) → BM3 · 바닥 확인 · 끝점 연장 판정 → --json")
    ap.add_argument("--json", help="--fit 결과 JSON")
    ap.add_argument("--v0", metavar="FIT_JSON", help="3 단계: 맞춤 결과 → V₀ relax 입력 (--run 점 폴더 · --out)")
    ap.add_argument("--run", help="--v0 와 함께: 점 폴더 (시작 좌표)")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.fit:
        f = fit_all(a.fit)
        txt = json.dumps(f, ensure_ascii=False, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
        if a.json:
            Path(a.json).write_text(txt + "\n")
        for n, c in f["cells"].items():
            fa = c.get("fit_all") or {}
            print(f"  {n}: {c['status']}" + (f" · V₀ {fa['V0_A3']:.2f} Å³ (x {fa['V0_A3'] / 1175.662:.4f}) · B₀ {fa['B0_GPa']:.1f} GPa · rms {fa['rms_meV']:.2f} meV · 표시 {c['flagged_x']}" if fa else "")
                  + (f" · {c.get('why') or c.get('next') or ''}"))
        print(f"  전체 {f['status']}" + (f" → {a.json}" if a.json else ""))
        return 0 if f["status"] == "V0_relax" else 3
    if a.v0:
        if not (a.run and a.out):
            ap.error("--v0 에는 --run · --out")
        f = json.loads(Path(a.v0).read_text()); f["_sha256"] = sha256(a.v0)
        man, texts = v0_inputs(f, a.run, a.out)
        for n, m in man["셀"].items():
            print(f"  {n}: x0 {m['x0']:.4f} · V₀ {m['V0_A3']:.2f} Å³ · 시작 {m['start_from']} → {a.out}/{n}/scf.in")
        return 0
    man, texts = build(a.out, xs=a.extra)
    print(f"입력 {len(texts)} 개 → {a.out}")
    for tg, m in man["점"].items():
        print(f"  {tg}  x {m['x']:.2f}  V {m['V_A3']:.3f} Å³  셀 {m['셀_길이_A']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
