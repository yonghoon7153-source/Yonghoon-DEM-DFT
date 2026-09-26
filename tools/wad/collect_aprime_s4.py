#!/usr/bin/env python3
"""collect_aprime_s4.py — A′ S4 집계: V2 2단계 QE 출력 → W_sep · E(d) · G3 · G4 · (UMA 대조).

카드 v5 (`db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json` · 개정 1·2) 의 식을 그대로 옮긴다:
  · W_sep = [E(far) − E(bound)] / (n_if · A)   · E = QE `!` 자유에너지 F · E_int = F − (−TS) 병기 · n_if = 1 · A = 변형된 실제 셀 면적
  · 보고: J/m² + eV/C (그래핀 C 원자당)
  · E(d): d₀−0.3 · d₀ · d₀+0.3 · d₀+0.6 · far 의 상대 에너지 (meV · meV/C) — d₀ 가 격자 안 국소 최소인지 (기록 · 문턱 없음)
  · G3 (대표점): c+2 셀에서 bound 1 · far (i) 그대로 · far (ii) +2 → ΔE_bound · ΔE_far · ΔW 각각 기록 · |ΔW| ≤ 0.01 J/m² **그리고** 조각 |ΔE| ≤ 5 meV
  · G4 (대표점): e70/700 · k+1 · smearing ½ 각각 두 끝점 → |ΔW| ≤ 0.02 J/m² (조각 ≤ 10 meV — ⚠ e70 조각은 절대 에너지가 ecut 에 비변분이라
    기록만 하고 문턱은 k·smearing 조각에만 건다: 이 해석은 1저자 확인 대상으로 결과 기록에 적는다)
  · UMA (개정 1): W_UMA+D3 := W_UMA + [E_D3,QE(far) − E_D3,QE(bound)]/A · Δ = W_PBE+D3 − W_UMA+D3 (= W_PBE − W_UMA) — V2 는 대상군 P1′ 이 아니라
    G5 판정이 아니다. 참고로 0.10/0.05 와 나란히 찍기만 한다.

입력 무결성: 실행 폴더의 pw.in 은 러너가 pseudo_dir 만 바꾼다 → 그 줄을 뺀 본문이 패키지 pw.in 과 같아야 유효 (다르면 그 잡은 INVALID · 0 으로 안 그린다).
완료 판정: se_sym_slab.parse_pw (JOB DONE · convergence has been achieved · D3 줄 · 마지막 실행).

⛔ 이 도구가 못 하는 것: 판정 문구를 만들지 않는다(문턱과 값을 나란히 놓는다) · 실패·누락 잡을 0 으로 채우지 않는다 · UMA 에너지를 직접 계산하지
   않는다(`relax_uma_d3.py --energies` 의 JSON 을 받는다) · 결과를 보고 표본·문턱을 바꾸지 않는다.

사용
  python3 tools/wad/collect_aprime_s4.py --stage2 db/inputs/wad_aprime_s4_v2_stage2_2026_09_26 --raw db/raw/wad_aprime_s4_v2s2_2026_09_26 [--uma uma.json] --out result.json
  python3 tools/wad/collect_aprime_s4.py --selftest
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S  # noqa: E402

RY_EV = 13.605693122994
RY_J = 2.1798723611e-18
EV_J = 1.602176634e-19
A2_M2 = 1e-20
G3_DW_MAX, G3_DE_MEV = 0.01, 5.0
G4_DW_MAX, G4_DE_MEV = 0.02, 10.0
G5_REF = {"per_sample": 0.10, "mean": 0.05}


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _norm_in(text):
    """러너가 바꾸는 pseudo_dir 줄만 뺀 입력 본문 (무결성 대조용)."""
    return "\n".join(ln for ln in text.splitlines() if not ln.strip().startswith("pseudo_dir"))


def area_A2(extxyz):
    from ase.io import read
    import numpy as np
    c = read(extxyz).cell.array
    return float(np.linalg.norm(np.cross(c[0], c[1])))


def w_j_m2(dE_ry, A):
    return dE_ry * RY_J / (A * A2_M2)


def read_job(raw_dir, pkg_dir, job):
    """한 잡 → {status, F_Ry, D3_Ry, mTS_Ry, E_int_Ry, E_pbe_Ry, input_match}. 없으면 status 만 (값 없음 ≠ 0)."""
    out = os.path.join(raw_dir, job, "pw.out"); pin_run = os.path.join(raw_dir, job, "pw.in"); pin_pkg = os.path.join(pkg_dir, "qe", job, "pw.in")
    r = {"job": job}
    if not os.path.isfile(out):
        r["status"] = "MISSING"; return r
    if os.path.isfile(pin_run) and os.path.isfile(pin_pkg):
        r["input_match"] = _norm_in(open(pin_run, errors="ignore").read()) == _norm_in(open(pin_pkg, errors="ignore").read())
    else:
        r["input_match"] = None
    if r["input_match"] is False:
        r["status"] = "INVALID_INPUT_MISMATCH"; return r
    try:
        e = S.parse_pw(out, "scf", True)
    except S.SlabError as ex:
        r["status"] = "FAILED"; r["why"] = str(ex); return r
    r.update({"status": "OK", "F_Ry": e["E_tot_Ry"], "D3_Ry": e["E_d3_Ry"], "mTS_Ry": e["mTS_Ry"], "E_pbe_Ry": e["E_pbe_Ry"],
              "E_int_Ry": (e["E_tot_Ry"] - e["mTS_Ry"]) if e["mTS_Ry"] is not None else None, "nat": e["nat"], "pw_out_sha256": _sha(out)})
    return r


def _w(jb, jf, A, key="F_Ry"):
    if not (jb and jf and jb.get("status") == "OK" and jf.get("status") == "OK") or jb.get(key) is None or jf.get(key) is None:
        return None
    return w_j_m2(jf[key] - jb[key], A)


def collect_registry(stage2_dir, raw_dir, name, uma=None, supp_dir=None):
    pkg = os.path.join(stage2_dir, name)
    man = json.load(open(os.path.join(pkg, "s3_v2_stage2_manifest.json"), encoding="utf-8"))
    jobs = {j["dir"]: j for j in man["jobs"]}
    A = area_A2(os.path.join(pkg, "structures", f"{name}_dft_bound.extxyz"))
    n_C = None
    from ase.io import read
    n_C = sum(1 for s in read(os.path.join(pkg, "structures", f"{name}_dft_bound.extxyz")).get_chemical_symbols() if s == "C")
    J = {j: read_job(os.path.join(raw_dir, name), pkg, j) for j in jobs}
    # 보조 잡 (부록 정오): supp/<name>/jobs.json 의 잡이 tags.substitutes = X 를 달고 있고 X 가 OK 가 아니면, 보조 잡이 OK 일 때만 대체한다.
    #   원 잡의 상태는 지우지 않고 `original` 에 남긴다 (조용한 교체 금지). 보조 잡도 실패면 원 잡 상태 그대로.
    if supp_dir and os.path.isfile(os.path.join(supp_dir, name, "jobs.json")):
        spkg = os.path.join(supp_dir, name)
        for sj in json.load(open(os.path.join(spkg, "jobs.json"), encoding="utf-8")).get("jobs", []):
            X = (sj.get("tags") or {}).get("substitutes")
            if not X or X not in J:
                continue
            sub = read_job(os.path.join(raw_dir, name), spkg, sj["dir"])
            J[X]["supplement"] = {"job": sj["dir"], "status": sub["status"], "changed": (sj.get("tags") or {}).get("changed")}
            if J[X]["status"] != "OK" and sub["status"] == "OK":
                J[X] = {**sub, "job": X, "substituted_by": sj["dir"], "changed": (sj.get("tags") or {}).get("changed"), "original": {k: v for k, v in J[X].items() if k != "supplement"}}
    b, f = J.get(f"{name}_dft_bound"), J.get(f"{name}_dft_far")
    rec = {"registry": name, "d0_A": man["d0_A"], "area_A2": round(A, 4), "n_C": n_C, "n_if": 1, "jobs": J,
           "W_PBE_D3_J_m2": _w(b, f, A, "F_Ry"), "W_PBE_D3_Eint_J_m2": _w(b, f, A, "E_int_Ry"), "W_PBE_J_m2": _w(b, f, A, "E_pbe_Ry"),
           "dD3_QE_J_m2": _w(b, f, A, "D3_Ry")}
    if rec["W_PBE_D3_J_m2"] is not None:
        dE_ev = (f["F_Ry"] - b["F_Ry"]) * RY_EV
        rec["W_PBE_D3_eV_per_C"] = dE_ev / n_C if n_C else None
        rec["W_PBE_D3_meV_per_cell"] = dE_ev * 1000
    # E(d)
    ed = {}
    if b and b.get("status") == "OK":
        for tag, s in (("Ed_m03", -0.3), ("Ed_p03", 0.3), ("Ed_p06", 0.6)):
            j = J.get(f"{name}_{tag}")
            ed[f"d0{s:+.1f}"] = {"d_A": round(man["d0_A"] + s, 4), "dE_meV": (j["F_Ry"] - b["F_Ry"]) * RY_EV * 1000 if j and j.get("status") == "OK" else None,
                                 "status": j["status"] if j else "MISSING"}
        if f and f.get("status") == "OK":
            ed["far"] = {"d_A": "≥ 8", "dE_meV": (f["F_Ry"] - b["F_Ry"]) * RY_EV * 1000, "status": "OK"}
        vals = [ed[k]["dE_meV"] for k in ("d0-0.3", "d0+0.3") if ed.get(k, {}).get("dE_meV") is not None]
        rec["E_d_local_min_in_grid"] = (all(v > 0 for v in vals) if len(vals) == 2 else None)
        if len(vals) == 2:
            em, ep = ed["d0-0.3"]["dE_meV"], ed["d0+0.3"]["dE_meV"]
            curv = (em + ep) / (0.3 ** 2)                       # meV/Å² (E0 = 0)
            rec["E_d_parabola"] = {"curvature_meV_A2": curv, "min_offset_A": (-0.3 * (ep - em) / (2 * (em + ep))) if (em + ep) else None,
                                   "⚠": "3 점 포물선 — 진단용 (카드 문턱 없음)"}
    rec["E_d"] = ed
    # G3
    g3b, g3i, g3ii = J.get(f"{name}_G3_c2_bound"), J.get(f"{name}_G3_c2_far_i"), J.get(f"{name}_G3_c2_far_ii")
    if g3b is not None:
        base = rec["W_PBE_D3_J_m2"]
        Wi, Wii = _w(g3b, g3i, A), _w(g3b, g3ii, A)
        de = lambda x, y: (x["F_Ry"] - y["F_Ry"]) * RY_EV * 1000 if (x and y and x.get("status") == "OK" and y.get("status") == "OK") else None
        g3 = {"dE_bound_meV": de(g3b, b), "dE_far_i_meV": de(g3i, f), "dE_far_ii_meV": de(g3ii, f),
              "W_i_J_m2": Wi, "W_ii_J_m2": Wii, "dW_i_J_m2": (Wi - base) if (Wi is not None and base is not None) else None,
              "dW_ii_J_m2": (Wii - base) if (Wii is not None and base is not None) else None, "threshold": {"|dW|<=": G3_DW_MAX, "|dE|<=meV": G3_DE_MEV}}
        pieces = [g3["dE_bound_meV"], g3["dE_far_i_meV"], g3["dE_far_ii_meV"]]; dws = [g3["dW_i_J_m2"], g3["dW_ii_J_m2"]]
        if any(v is None for v in pieces + dws):
            g3["status"] = "INCOMPLETE"
        else:
            g3["status"] = "PASS" if all(abs(v) <= G3_DW_MAX for v in dws) and all(abs(v) <= G3_DE_MEV for v in pieces) else "FAIL"
        rec["G3"] = g3
    # G4
    g4 = {}
    for tag, piece_gate in (("e70", False), ("k1", True), ("s05", True)):
        jb, jf = J.get(f"{name}_G4_{tag}_bound"), J.get(f"{name}_G4_{tag}_far")
        if jb is None:
            continue
        base = rec["W_PBE_D3_J_m2"]; Wx = _w(jb, jf, A)
        de = lambda x, y: (x["F_Ry"] - y["F_Ry"]) * RY_EV * 1000 if (x and y and x.get("status") == "OK" and y.get("status") == "OK") else None
        r4 = {"W_J_m2": Wx, "dW_J_m2": (Wx - base) if (Wx is not None and base is not None) else None, "dE_bound_meV": de(jb, b), "dE_far_meV": de(jf, f),
              "piece_gate_applied": piece_gate, "threshold": {"|dW|<=": G4_DW_MAX, "|dE|<=meV": G4_DE_MEV if piece_gate else "기록만 (ecut 비변분)"}}
        if r4["dW_J_m2"] is None or (piece_gate and (r4["dE_bound_meV"] is None or r4["dE_far_meV"] is None)):
            r4["status"] = "INCOMPLETE"
        else:
            ok = abs(r4["dW_J_m2"]) <= G4_DW_MAX and (not piece_gate or (abs(r4["dE_bound_meV"]) <= G4_DE_MEV and abs(r4["dE_far_meV"]) <= G4_DE_MEV))
            r4["status"] = "PASS" if ok else "FAIL"
        g4[tag] = r4
    if g4:
        st = {v["status"] for v in g4.values()}
        g4["status"] = "INCOMPLETE" if "INCOMPLETE" in st else ("FAIL" if "FAIL" in st else "PASS")
        rec["G4"] = g4
    # UMA (개정 1)
    if uma:
        eb, ef = uma.get(f"{name}_dft_bound"), uma.get(f"{name}_dft_far")
        if eb is not None and ef is not None and rec["dD3_QE_J_m2"] is not None:
            W_uma = (ef - eb) * EV_J / (A * A2_M2)
            rec["UMA"] = {"E_bound_eV": eb, "E_far_eV": ef, "W_UMA_J_m2": W_uma, "W_UMA_plus_QE_D3_J_m2": W_uma + rec["dD3_QE_J_m2"],
                          "Delta_J_m2": rec["W_PBE_D3_J_m2"] - (W_uma + rec["dD3_QE_J_m2"]),
                          "identity_check_W_PBE_minus_W_UMA": rec["W_PBE_J_m2"] - W_uma,
                          "⚠": "V2 는 대상군 P1′ 이 아니다 — G5 판정 아님 · 0.10/0.05 는 참고 눈금"}
        else:
            rec["UMA"] = {"status": "UMA 에너지 없음 (relax_uma_d3.py --energies)"} if not (eb is not None and ef is not None) else {"status": "QE D3 항 없음"}
    return rec


def collect(stage2_dir, raw_dir, uma_json=None, supp_dir=None):
    uma = None
    if uma_json:
        u = json.load(open(uma_json, encoding="utf-8"))
        uma = {k: v["E_UMA_eV"] for k, v in u.get("energies", {}).items()}
    regs = sorted(d for d in os.listdir(stage2_dir) if d.startswith("V2_") and os.path.isdir(os.path.join(stage2_dir, d)))
    out = {"schema": "aprime_s4_v2_collect/v1", "stage2": stage2_dir, "raw": raw_dir, "uma_json": uma_json, "supp": supp_dir, "registries": {}}
    for n in regs:
        out["registries"][n] = collect_registry(stage2_dir, raw_dir, n, uma, supp_dir)
    Ws = [r["W_PBE_D3_J_m2"] for r in out["registries"].values() if r["W_PBE_D3_J_m2"] is not None]
    out["summary"] = {"n_registry": len(regs), "n_W": len(Ws), "W_PBE_D3_J_m2": {n: r["W_PBE_D3_J_m2"] for n, r in out["registries"].items()},
                      "W_range_J_m2": [min(Ws), max(Ws)] if Ws else None, "W_mean_J_m2": (sum(Ws) / len(Ws)) if Ws else None,
                      "G3": {n: r["G3"]["status"] for n, r in out["registries"].items() if "G3" in r}, "G4": {n: r["G4"]["status"] for n, r in out["registries"].items() if "G4" in r},
                      "Delta_UMA_J_m2": {n: r["UMA"].get("Delta_J_m2") for n, r in out["registries"].items() if isinstance(r.get("UMA"), dict) and "Delta_J_m2" in r["UMA"]},
                      "G5_ref_scale": G5_REF, "jobs_not_ok": {n: [j for j, v in r["jobs"].items() if v["status"] != "OK"] for n, r in out["registries"].items()},
                      "substituted": {n: {j: v["substituted_by"] for j, v in r["jobs"].items() if v.get("substituted_by")} for n, r in out["registries"].items()}}
    return out


def _print(out):
    print(f"{'registry':14s} {'d0':>6s} {'W F':>8s} {'W Eint':>8s} {'W PBE':>8s} {'dD3':>7s} {'eV/C':>7s}  E(d-0.3) E(d+0.3) E(d+0.6) [meV]  G3    G4     Δ_UMA")
    for n, r in out["registries"].items():
        f = lambda x, w=8, p=4: (f"{x:{w}.{p}f}" if isinstance(x, (int, float)) else f"{'—':>{w}s}")
        ed = r.get("E_d", {}); g = lambda k: ed.get(k, {}).get("dE_meV")
        print(f"{n:14s} {r['d0_A']:6.3f} {f(r['W_PBE_D3_J_m2'])} {f(r['W_PBE_D3_Eint_J_m2'])} {f(r['W_PBE_J_m2'])} {f(r['dD3_QE_J_m2'],7)} {f(r.get('W_PBE_D3_eV_per_C'),7)}  "
              f"{f(g('d0-0.3'),8,1)} {f(g('d0+0.3'),8,1)} {f(g('d0+0.6'),8,1)}        {r.get('G3',{}).get('status','—'):5s} {r.get('G4',{}).get('status','—'):6s} {f(r.get('UMA',{}).get('Delta_J_m2') if isinstance(r.get('UMA'),dict) else None,7)}")
    s = out["summary"]
    print(f"W 범위 {s['W_range_J_m2']} · 평균 {s['W_mean_J_m2']} · 미완 잡 {s['jobs_not_ok']}")
    for n, r in out["registries"].items():
        if "G3" in r:
            g = r["G3"]; print(f"  G3 {n}: ΔE_bound {g['dE_bound_meV']} · ΔE_far(i) {g['dE_far_i_meV']} · ΔE_far(ii) {g['dE_far_ii_meV']} meV · ΔW(i) {g['dW_i_J_m2']} · ΔW(ii) {g['dW_ii_J_m2']} → {g['status']}")
        if "G4" in r:
            for t in ("e70", "k1", "s05"):
                if t in r["G4"]:
                    g = r["G4"][t]; print(f"  G4 {n} {t}: ΔW {g['dW_J_m2']} · ΔE_bound {g['dE_bound_meV']} · ΔE_far {g['dE_far_meV']} meV → {g['status']}")


# ───────────────────────── selftest ─────────────────────────
def _fake_out(path, F, d3, ts=-0.0005, nat=20):
    open(path, "w").write(f"     Program PWSCF v.7.4.1 starts\n     number of atoms/cell      =           {nat}\n     convergence has been achieved in   9 iterations\n"
                          f"!    total energy              =  {F:16.8f} Ry\n     smearing contrib. (-TS)   =  {ts:16.8f} Ry\n     DFT-D3 Dispersion         =  {d3:16.8f} Ry\n     JOB DONE.\n")


def _selftest():
    import tempfile
    from ase import Atoms
    from ase.io import write
    ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    with tempfile.TemporaryDirectory() as T:
        st, raw = os.path.join(T, "s2"), os.path.join(T, "raw"); name = "V2_x"
        pkg = os.path.join(st, name); os.makedirs(os.path.join(pkg, "structures")); os.makedirs(os.path.join(pkg, "qe"))
        at = Atoms("Ag12C8", positions=[[0, 0, i * 0.5] for i in range(20)], cell=[[5, 0, 0], [2.5, 4.330127, 0], [0, 0, 24]], pbc=True)
        write(os.path.join(pkg, "structures", f"{name}_dft_bound.extxyz"), at, format="extxyz")
        A = 5 * 4.330127
        F0 = -1000.0; W_true = 0.30  # J/m² → ΔF
        dF = W_true * A * A2_M2 / RY_J
        jobs = ["dft_bound", "dft_far", "Ed_m03", "Ed_p03", "Ed_p06", "G3_c2_bound", "G3_c2_far_i", "G3_c2_far_ii", "G4_e70_bound", "G4_e70_far", "G4_k1_bound", "G4_k1_far", "G4_s05_bound", "G4_s05_far"]
        E = {"dft_bound": (F0, -0.50), "dft_far": (F0 + dF, -0.40), "Ed_m03": (F0 + 0.002, -0.55), "Ed_p03": (F0 + 0.001, -0.47), "Ed_p06": (F0 + 0.003, -0.45),
             "G3_c2_bound": (F0 + 1e-5, -0.50), "G3_c2_far_i": (F0 + dF + 1e-5, -0.40), "G3_c2_far_ii": (F0 + dF + 2e-5, -0.40),
             "G4_e70_bound": (F0 - 0.05, -0.50), "G4_e70_far": (F0 - 0.05 + dF + 1e-4, -0.40), "G4_k1_bound": (F0 + 1e-4, -0.50), "G4_k1_far": (F0 + dF + 1e-4, -0.40),
             "G4_s05_bound": (F0 + 2e-4, -0.50), "G4_s05_far": (F0 + dF + 2e-4, -0.40)}
        man = {"model": name, "d0_A": 3.3, "jobs": [{"dir": f"{name}_{j}", "kind": "scf"} for j in jobs]}
        json.dump(man, open(os.path.join(pkg, "s3_v2_stage2_manifest.json"), "w"))
        for j in jobs:
            d = os.path.join(pkg, "qe", f"{name}_{j}"); os.makedirs(d); open(os.path.join(d, "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/data/work/pseudo'\n  prefix='x'\n/\n")
            r = os.path.join(raw, name, f"{name}_{j}"); os.makedirs(r); open(os.path.join(r, "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/home/ubuntu/wad4l/pseudo_kgy'\n  prefix='x'\n/\n")
            _fake_out(os.path.join(r, "pw.out"), *E[j])
        out = collect(st, raw)
        r = out["registries"][name]
        ck(abs(r["W_PBE_D3_J_m2"] - W_true) < 1e-6 and abs(r["area_A2"] - A) < 1e-3 and r["n_C"] == 8, f"W = ΔF/A 로 0.30 J/m² 복원 · 면적 · n_C — {r['W_PBE_D3_J_m2']}")
        ck(abs(r["dD3_QE_J_m2"] - w_j_m2(0.10, A)) < 1e-6 and abs(r["W_PBE_J_m2"] - (W_true - w_j_m2(0.10, A))) < 1e-6, "ΔD3 · W_PBE = W − ΔD3 (개정 1 항 분리)")
        ck(r["E_d_local_min_in_grid"] is True and abs(r["E_d"]["d0-0.3"]["dE_meV"] - 0.002 * RY_EV * 1000) < 1e-6, "E(d): d₀ 가 격자 안 국소 최소 · 상대 에너지 meV")
        ck(r["G3"]["status"] == "PASS" and abs(r["G3"]["dE_bound_meV"] - 1e-5 * RY_EV * 1000) < 1e-9, f"G3 PASS (조각 0.136 meV · ΔW ~0) — {r['G3']['status']}")
        ck(r["G4"]["status"] == "PASS" and r["G4"]["e70"]["piece_gate_applied"] is False and r["G4"]["k1"]["piece_gate_applied"] is True, "G4 PASS · e70 조각 문턱 미적용 표기")
        ck(all(v["input_match"] is True for v in r["jobs"].values()), "입력 무결성: pseudo_dir 만 다른 pw.in 은 일치로 본다")
        uma_json = os.path.join(T, "uma.json")
        json.dump({"energies": {f"{name}_dft_bound": {"E_UMA_eV": -100.0}, f"{name}_dft_far": {"E_UMA_eV": -100.0 + (W_true - w_j_m2(0.10, A) + 0.05) * A * A2_M2 / EV_J}}}, open(uma_json, "w"))
        o2 = collect(st, raw, uma_json); u = o2["registries"][name]["UMA"]
        ck(abs(u["Delta_J_m2"] + 0.05) < 1e-6 and abs(u["identity_check_W_PBE_minus_W_UMA"] - u["Delta_J_m2"]) < 1e-6, f"UMA: W_UMA+QE-D3 · Δ = W_PBE − W_UMA (개정 1 항등식) — {u['Delta_J_m2']}")
        # ⛔ 음성 1: far 를 0.02 Ry 올리면 G3 FAIL (ΔW · 조각 둘 다)
        _fake_out(os.path.join(raw, name, f"{name}_G3_c2_far_i", "pw.out"), F0 + dF + 0.02, -0.40)
        o3 = collect(st, raw); ck(o3["registries"][name]["G3"]["status"] == "FAIL", "⛔음성 G3: far(i) +0.02 Ry → FAIL")
        # ⛔ 음성 2: pw.out 삭제 → MISSING · W None (0 아님)
        os.remove(os.path.join(raw, name, f"{name}_dft_far", "pw.out"))
        o4 = collect(st, raw); r4 = o4["registries"][name]
        ck(r4["jobs"][f"{name}_dft_far"]["status"] == "MISSING" and r4["W_PBE_D3_J_m2"] is None and o4["summary"]["W_mean_J_m2"] is None, "⛔음성 누락: far 없음 → MISSING · W None · 평균 None")
        # ⛔ 음성 3: 실행 입력이 패키지와 다르면 INVALID
        _fake_out(os.path.join(raw, name, f"{name}_dft_far", "pw.out"), F0 + dF, -0.40)
        open(os.path.join(raw, name, f"{name}_dft_far", "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/x'\n  prefix='y'\n/\n")
        o5 = collect(st, raw); ck(o5["registries"][name]["jobs"][f"{name}_dft_far"]["status"] == "INVALID_INPUT_MISMATCH" and o5["registries"][name]["W_PBE_D3_J_m2"] is None, "⛔음성 입력 불일치: prefix 가 다르면 INVALID · W None")
        # 보조 잡 대체 (부록 정오 1): k1_far 를 미수렴으로 만들고 supp 의 k1_far_b01 이 OK 면 대체 · 원 상태 보존
        _fake_out(os.path.join(raw, name, f"{name}_dft_far", "pw.out"), F0 + dF, -0.40)
        open(os.path.join(raw, name, f"{name}_dft_far", "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/x'\n  prefix='x'\n/\n")
        open(os.path.join(raw, name, f"{name}_G4_k1_far", "pw.out"), "w").write("     Program PWSCF\n     convergence NOT achieved\n!    total energy = -1.0 Ry\n     DFT-D3 Dispersion = -0.1 Ry\n     JOB DONE.\n")
        supp = os.path.join(T, "supp", name); os.makedirs(os.path.join(supp, "qe", f"{name}_G4_k1_far_b01")); 
        open(os.path.join(supp, "qe", f"{name}_G4_k1_far_b01", "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/p'\n  prefix='b01'\n  mixing_beta = 0.1\n/\n")
        json.dump({"jobs": [{"dir": f"{name}_G4_k1_far_b01", "tags": {"substitutes": f"{name}_G4_k1_far", "changed": "mixing_beta 0.3 → 0.1"}}]}, open(os.path.join(supp, "jobs.json"), "w"))
        rb = os.path.join(raw, name, f"{name}_G4_k1_far_b01"); os.makedirs(rb); open(os.path.join(rb, "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/q'\n  prefix='b01'\n  mixing_beta = 0.1\n/\n")
        _fake_out(os.path.join(rb, "pw.out"), F0 + dF + 1e-4, -0.40)
        o7 = collect(st, raw, None, os.path.join(T, "supp")); r7 = o7["registries"][name]
        ck(r7["jobs"][f"{name}_G4_k1_far"].get("substituted_by") == f"{name}_G4_k1_far_b01" and r7["jobs"][f"{name}_G4_k1_far"]["original"]["status"] == "FAILED" and r7["G4"]["k1"]["status"] == "PASS"
           and o7["summary"]["substituted"][name] == {f"{name}_G4_k1_far": f"{name}_G4_k1_far_b01"}, "보조 잡 대체: 원 FAILED 보존 · b01 로 G4 k1 PASS · summary 에 대체 기록")
        o7n = collect(st, raw, None); ck(o7n["registries"][name]["G4"]["k1"]["status"] == "INCOMPLETE", "⛔음성 supp 없이는 대체 안 함 → k1 INCOMPLETE")
        open(os.path.join(rb, "pw.out"), "w").write("     Program PWSCF\n     convergence NOT achieved\n!    total energy = -1.0 Ry\n     DFT-D3 Dispersion = -0.1 Ry\n     JOB DONE.\n")
        o7f = collect(st, raw, None, os.path.join(T, "supp")); ck(o7f["registries"][name]["jobs"][f"{name}_G4_k1_far"]["status"] == "FAILED" and not o7f["registries"][name]["jobs"][f"{name}_G4_k1_far"].get("substituted_by"), "⛔음성 보조 잡도 실패면 대체 안 함 (원 FAILED 그대로)")
        _fake_out(os.path.join(raw, name, f"{name}_G4_k1_far", "pw.out"), *E["G4_k1_far"])
        # ⛔ 음성 4: 미수렴 출력 → FAILED
        open(os.path.join(raw, name, f"{name}_dft_far", "pw.in"), "w").write("&CONTROL\n  pseudo_dir = '/x'\n  prefix='x'\n/\n")
        open(os.path.join(raw, name, f"{name}_dft_far", "pw.out"), "w").write("     Program PWSCF\n     convergence NOT achieved\n!    total energy = -1.0 Ry\n     DFT-D3 Dispersion = -0.1 Ry\n     JOB DONE.\n")
        o6 = collect(st, raw); ck(o6["registries"][name]["jobs"][f"{name}_dft_far"]["status"] == "FAILED", "⛔음성 미수렴: convergence NOT achieved → FAILED")
    print(f"{'✅' if not bad else '⛔'} collect_aprime_s4 selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--stage2"); ap.add_argument("--raw"); ap.add_argument("--uma"); ap.add_argument("--supp", help="보조 잡 패키지 (부록 정오 · tags.substitutes)"); ap.add_argument("--out"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if not (a.stage2 and a.raw):
        ap.error("--stage2 와 --raw 가 필요하다")
    out = collect(a.stage2, a.raw, a.uma, a.supp)
    _print(out)
    if a.out:
        json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float); open(a.out, "a").write("\n"); print(f"-> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
