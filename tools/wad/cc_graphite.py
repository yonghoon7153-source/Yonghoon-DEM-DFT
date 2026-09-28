#!/usr/bin/env python3
"""cc_graphite.py — WAD-CC 흑연 층간(C|C) W_sep: 1단계(제약 이완) 입력 · 2단계(끝점·E(d)·G3·G4) 입력 · 집계 (사전등록 카드 `PREREG`).

왜: 무음극 셀 LPSCl | Ag–C (Ag + Denka Black) | VGCF 에서 DEM 이 쓰는 탄소–탄소 접촉 — 덴카–덴카 · 덴카–VGCF · VGCF–VGCF — 은
    DFT 에서 셋 다 **흑연 기저면(0001) | 기저면** 접촉이고, 서로 다른 입자라 면내 회전이 임의다(= 비정합). V2(Ag(111)|그래핀)와
    **같은** PBE+D3(BJ) 2체 · 같은 QE 설정으로 W 를 잰다. 흑연은 실험 앵커가 있어 (Wang 2015 Nat. Commun. 6, 7853 —
    litdb `wang2015_graphite_cleavage_energy`) 우리 D3(BJ) 설정의 대조 계산을 겸한다.

    python3 tools/wad/cc_graphite.py --stage1 --out db/inputs/wad_cc_graphite_2026_09_28/stage1
    python3 tools/wad/cc_graphite.py --stage2 --stage1_dir <stage1> --relax_raw <1단계 RUN> --out <stage2>
    python3 tools/wad/cc_graphite.py --collect --stage2_dir <stage2> --raw <2단계 RUN> [--atm] [--out result.json]
    python3 tools/wad/cc_graphite.py --selftest

모델 (1×1 육방 셀 · a = A_C_PBE_D3 2.46604 Å (09-25 선행 배치 PBE+D3 그래핀) · 층당 C 2 · 초기 층간 3.35 Å):
  S33_{AB,SP,AA}   6층 흑연을 3|3 에서 가른다 — 두꺼운|두꺼운 (입자–입자 접촉 · Wang CE 와 같은 기하)
  M41_{AB,SP,AA}   4층 흑연 위 그래핀 1장 — V2(Ag 위 그래핀 1장)와 같은 기하 → V2 와 같은-기하 비
  S44_AB · M61_AB  두께 점검 (S33_AB · M41_AB 대비 |ΔW| ≤ 0.02)
  M41_AB_V2a       V2 의 그래핀 격자 a_Ag·√3/(2√2) = 2.49263 Å (+1.078 %) — 변형 영향 (정보)
registry = 계면 한 쌍의 면내 어긋남 u (60° 분수좌표 대각선 (s, s)): AA s = 0 · AB = 아래 블록의 ABAB 를 잇는 s (Bernal) ·
  SP s = ½ (AB↔BA 안장점). 블록 안은 항상 Bernal. 판정은 **좌표에서 다시** 한다 (`stacking_label` — 원자 표지와 무관:
  위층 두 원자의 아래층 최근접 면내 거리 AA [0, 0] · AB [0, a/√3] · SP [a/(2√3), a/(2√3)]).
비정합(임의 회전 입자 접촉) 추정 = GSFE 평균 (Wang 2015 의 σ0 와 같은 정의 · 이완 없는 강체 비정합):
  1성(星) W_inc = (2·W_AB + W_AA)/3 · 2성 W_inc = (W_AA + 3·W_SP)/4 (AB 무관) · σ0 = W_AB − W_inc(2성) ·
  1성 일관성 비 r = (W_AB − W_SP)/(W_AB − W_AA) (1성이면 1/9). **정보량** — 판정 아님.
QE = V2 와 같음 (`build_aprime_s3.qe_input` 그대로 쓰고 smearing 두 줄만 바꾼다): 52/520 · PBE+D3(BJ) 2체 (version 4 ·
  threebody .false.) · **mv 0.01** (Ag 가 없어도 V2 와 맞춘다 — 원 함수는 Ag 없으면 gaussian 0.005) · nspin 1 ·
  쌍극자(개정 2 · 진공 중앙 · 양쪽 핵 ≥ 4 Å) · k 18×18×1 (0.163 Å⁻¹ ≤ 0.20) · relax = 맨 아래층 고정 · 나머지 z 만.
끝점: far 직접·영상 간격 ≥ 10 Å (V2 교훈 — 8 Å 에서 G3 FAIL) · far8(같은 셀 · 직접 8 Å)은 정보.
⛔ 못 하는 것: 에너지를 계산하지 않는다(집계만) · 결과를 보고 문턱·표본을 바꾸지 않는다 · 비정합 계면을 직접 계산하지 않는다
   (푸리에 추정) · 덴카블랙의 모서리·결함·산소 작용기·곡률은 모른다(이상 기저면만) · 바인더는 다루지 않는다.
"""
import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S                    # noqa: E402
import build_aprime_interfaces as B        # noqa: E402
import build_aprime_s3 as B3               # noqa: E402
import collect_aprime_s4 as C4             # noqa: E402

SlabError = S.SlabError
REPO = S.REPO
PREREG = "db/properties/wad_cc_graphite_prereg_2026_09_28.json"

A_C = B.A_C_PBE_D3
A_C_V2 = B.A_AG_PBE_D3 / math.sqrt(2.0) * math.sqrt(3.0) / 2.0   # V2: 그래핀 2×2 on Ag(111)(√3×√3)R30° 의 그래핀 격자
D_INIT = 3.35
GAP, GAP_INFO = 10.0, 8.0
KPTS, KPTS_DENSE = (18, 18, 1), (24, 24, 1)
ECUT, ECUT_HI = (52.0, 520.0), (70.0, 700.0)
SMEAR, DEGAUSS, DEGAUSS_HALF = "mv", 0.01, 0.005
ED_SHIFTS = B3.ED_SHIFTS
MACHINE = "V100 (run_sese_gpu.sh · V2 와 같은 pw.x 912d8c8f)"
PP_C = B3.PP["C"][1]

GEOM = {"S33": (3, 3), "M41": (4, 1), "S44": (4, 4), "M61": (6, 1)}
MODELS = (("S33", "AB", "base"), ("S33", "SP", "base"), ("S33", "AA", "base"),
          ("M41", "AB", "base"), ("M41", "SP", "base"), ("M41", "AA", "base"),
          ("S44", "AB", "base"), ("M61", "AB", "base"), ("M41", "AB", "V2a"))
LATTICE = {"base": A_C, "V2a": A_C_V2}
REPS = ("CC_S33_AB", "CC_M41_AB")          # E(d) · far8 · G3 · G4 대상 (사전등록)

# 판정 문턱 — 사전등록 카드와 같은 값 (결과 뒤 바꾸지 않는다 · 카드 값 결속 시험이 selftest 에 있다)
BAND = (0.31, 0.47)                        # S33_AB 운영 허용대 (Codex 파일럿 허용오차 · 측정 불확도 아님)
G3_DW, G4_DW, THICK_DW = 0.01, 0.01, 0.02
SPACING_OK = (3.0, 4.2)                    # 이완 뒤 층간 [Å] — 밖이면 INCOMPLETE (세고 제외 · 교체 없음)
FLAT_TOL = 0.05                            # 한 층 안 z 폭 [Å]
WANG = {"CE_incommensurate_J_m2": (0.37, 0.01), "CE_ideal_AB_J_m2": (0.39, 0.02), "sigma0_J_m2": (0.022, 0.005),
        "src": "Wang et al., Nat. Commun. 6, 7853 (2015) — litdb wang2015_graphite_cleavage_energy (초록 · 본문 식 G(0) = G + σ0)"}
V2_REF = ("db/raw/wad_aprime_s4_v2s2_2026_09_26/collect_aprime_s4_2026_09_26.json", "V2_top_fcc")
D3BJ_PBE = {"s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407, "alp": 14.0}   # V2 ATM 열과 같은 값 (S1 결박값)
RY_EV, EV_J, A2_M2 = C4.RY_EV, C4.EV_J, C4.A2_M2
HARTREE_EV, BOHR_A = 27.211386245988, 0.529177210903


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ─────────────────────────────── 기하 ───────────────────────────────
def _cell(a, c):
    return np.array([[a, 0.0, 0.0], [a / 2.0, a * math.sqrt(3.0) / 2.0, 0.0], [0.0, 0.0, c]])


def layer_offsets(n_sub, n_top, reg):
    """층별 면내 어긋남 s (분수좌표 (s, s)). 아래 블록 ABAB… · 계면 = reg · 위 블록 안은 Bernal."""
    if n_sub < 2 or n_top < 1:
        raise SlabError("기판 ≥ 2층 (Bernal 방향을 정하려면) · 위 ≥ 1층")
    if reg not in ("AB", "SP", "AA"):
        raise SlabError(f"registry {reg} — AB · SP · AA 만")
    sub = [(i % 2) / 3.0 for i in range(n_sub)]
    step = sub[-2] - sub[-1]
    u1 = sub[-1] + {"AB": step, "AA": 0.0, "SP": 0.5}[reg]
    top = [u1 - (step if k % 2 else 0.0) for k in range(n_top)]
    return sub, top


def graphite_stack(n_sub, n_top, reg, a=A_C, d=D_INIT):
    """(원자, is_top) — 층당 C 2 (기저 (0,0)·(⅓,⅓) + 층 어긋남) · 층 j 는 z = j·d."""
    from ase import Atoms
    sub, top = layer_offsets(n_sub, n_top, reg)
    C = _cell(a, (n_sub + n_top) * d + 20.0)
    fr, z, top_mask = [], [], []
    for j, o in enumerate(sub + top):
        for b in (0.0, 1.0 / 3.0):
            f = np.mod(np.array([o + b, o + b]), 1.0)
            f[np.isclose(f, 1.0)] = 0.0
            fr.append(f); z.append(j * d); top_mask.append(j >= n_sub)
    xy = np.array(fr) @ C[:2, :2]
    at = Atoms("C" * len(z), positions=np.column_stack([xy, z]), cell=C, pbc=(True, True, False))
    return at, np.array(top_mask)


def layers(at, tol=0.3):
    """z 로 층을 묶는다 (아래→위) · 각 층 = 원자 인덱스 목록."""
    z = at.get_positions()[:, 2]
    order = np.argsort(z, kind="stable")
    out, cur = [], [int(order[0])]
    for i in order[1:]:
        if z[i] - z[cur[-1]] < tol:
            cur.append(int(i))
        else:
            out.append(sorted(cur)); cur = [int(i)]
    out.append(sorted(cur))
    return out


def stacking_label(at, lower, upper, tol=0.05):
    """두 층의 적층 — 원자 표지와 무관한 판정 (위층 원자마다 아래층 최근접 면내 거리, 정렬)."""
    x = at.get_positions(); C = at.cell.array
    a = float(np.linalg.norm(C[0]))
    dm = sorted(min(d for i in lower for d, _na, _nb, _v in B._images_inplane(x[j] - x[i], C)) for j in upper)
    ref = {"AA": [0.0, 0.0], "AB": [0.0, a / math.sqrt(3.0)], "SP": [a / (2.0 * math.sqrt(3.0))] * 2}
    for k, v in ref.items():
        if len(dm) == 2 and all(abs(p - q) < tol for p, q in zip(dm, v)):
            return k
    return "other"


def stack_report(at, n_sub):
    """층 · 층간 · 평탄도 · 계면 적층 · 블록 안 적층 (전부 좌표에서)."""
    L = layers(at)
    z = at.get_positions()[:, 2]
    zc = [float(np.mean(z[l])) for l in L]
    return {"n_layers": len(L), "atoms_per_layer": [len(l) for l in L], "layer_z_A": [round(v, 4) for v in zc],
            "spacings_A": [round(zc[k + 1] - zc[k], 4) for k in range(len(zc) - 1)],
            "flatness_A": [round(float(z[l].max() - z[l].min()), 4) for l in L],
            "interface": stacking_label(at, L[n_sub - 1], L[n_sub]) if len(L) > n_sub else None,
            "internal": [stacking_label(at, L[k], L[k + 1]) for k in range(len(L) - 1) if k != n_sub - 1]}


def model_name(geom, reg, lat):
    return f"CC_{geom}_{reg}" + ("" if lat == "base" else f"_{lat}")


def build_model(geom, reg, lat="base", gap=GAP):
    """→ (이름, bound, far, is_top, meta). 끝점은 V2 와 같은 `make_endpoints` (쌍극자 개정 2 포함)."""
    n_sub, n_top = GEOM[geom]
    a = LATTICE[lat]
    at, is_top = graphite_stack(n_sub, n_top, reg, a)
    b, f, em = B.make_endpoints(at, is_top, gap)
    rep = stack_report(b, n_sub)
    if rep["n_layers"] != n_sub + n_top or any(n != 2 for n in rep["atoms_per_layer"]):
        raise SlabError(f"{geom}_{reg}: 층 구성 {rep['atoms_per_layer']}")
    if rep["interface"] != reg or any(s != "AB" for s in rep["internal"]):
        raise SlabError(f"{geom}_{reg}: 좌표 판정 계면 {rep['interface']} · 블록 안 {rep['internal']} — 설계와 다르다")
    L = layers(b)
    fixed = list(L[0])
    lateral = [i for i in range(len(b)) if i not in fixed]
    name = model_name(geom, reg, lat)
    meta = {"model": name, "geometry": geom, "registry": reg, "lattice": lat, "a_A": round(a, 8),
            "strain_vs_A_C_pct": round(100.0 * (a / A_C - 1.0), 4), "n_sub_layers": n_sub, "n_top_layers": n_top,
            "n_atoms": len(b), "n_C_contact_layer": 2, "area_A2": round(float(np.linalg.norm(np.cross(b.cell.array[0], b.cell.array[1]))), 6),
            "fixed_idx": fixed, "lateral_fixed_idx": lateral, "stack": rep, "endpoints": em, "d_init_A": D_INIT}
    return name, b, f, is_top, meta


# ─────────────────────────────── QE 입력 ───────────────────────────────
def qe_input_cc(atoms, prefix, kpts, pseudo_dir, calc="scf", dip=None, fixed=(), lateral=(), ecut=ECUT, degauss=DEGAUSS):
    """V2 와 같은 작성기(`build_aprime_s3.qe_input`) → smearing 두 줄만 mv · degauss 로 (Ag 가 없어 gaussian 0.005 가 나오는 줄)."""
    t = B3.qe_input(atoms, prefix, kpts, pseudo_dir, calc, dip, fixed, lateral, ecut, 200, d3=True)
    s_old, d_old = "  smearing = 'gaussian'\n", "  degauss = 0.005\n"
    if t.count(s_old) != 1 or t.count(d_old) != 1:
        raise SlabError("원 작성기의 Ag-없음 smearing 줄이 예상과 다르다 (gaussian · 0.005 각 1줄) — 치환하지 않는다")
    return t.replace(s_old, f"  smearing = '{SMEAR}'\n").replace(d_old, f"  degauss = {degauss}\n")


class CCPack:
    """구조 파일 · pw.in · qe/jobs.json (run_sese_gpu.sh 의 IN = <out>/qe)."""
    def __init__(self, out, pseudo_dir):
        self.out, self.pseudo_dir = out, pseudo_dir
        self.jobs, self.struct = [], {}
        os.makedirs(os.path.join(out, "qe"), exist_ok=True)

    def add_struct(self, name, atoms):
        from ase.io import write
        d = os.path.join(self.out, "structures"); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, f"{name}.extxyz")
        a = atoms.copy(); a.set_pbc((True, True, False)); a.calc = None
        write(p, a)
        self.struct[name] = _sha(p)
        return p

    def add_job(self, name, atoms, model, calc="scf", kind="scf", dip=None, fixed=(), lateral=(), ecut=ECUT, kpts=KPTS, degauss=DEGAUSS, tags=None):
        d = os.path.join(self.out, "qe", name); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "pw.in")
        open(p, "w").write(qe_input_cc(atoms, name, kpts, self.pseudo_dir, calc, dip, fixed, lateral, ecut, degauss))
        self.jobs.append({"dir": name, "kind": kind, "calc": calc, "model": model, "nat": len(atoms), "kpts": list(kpts), "ecutwfc": ecut[0], "ecutrho": ecut[1],
                          "smearing": SMEAR, "degauss": degauss, "electron_maxstep": 200, "d3": "PBE+D3(BJ) 2체", "dip": dip, "pw_in_sha256": _sha(p),
                          "structure": (tags or {}).get("structure"), "tags": tags or {}, "machine": MACHINE})
        return p

    def write_jobs(self, what, extra=None):
        doc = {"schema": "qe_input_set/v1", "what": what, "prereg": PREREG,
               "settings": {"pp": {"C": PP_C}, "pp_sha256": {PP_C: B3.PP_SHA[PP_C]}, "pseudo_dir_note": "러너가 PSEUDO_DIR 로 바꾼다"},
               "jobs": self.jobs}
        doc.update(extra or {})
        p = os.path.join(self.out, "qe", "jobs.json")
        json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        return p


def _dd(dip):
    return {"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}


def _code_sha():
    return {os.path.relpath(os.path.join(HERE, f), REPO): _sha(os.path.join(HERE, f))
            for f in ("cc_graphite.py", "build_aprime_interfaces.py", "build_aprime_s3.py", "collect_aprime_s4.py", "se_sym_slab.py")}


# ─────────────────────────────── 1단계 ───────────────────────────────
def stage1(out, pseudo_dir="/data/work/pseudo", date=None):
    """이완 9 잡 (맨 아래층 '0 0 0' · 나머지 '0 0 1')."""
    P = CCPack(out, pseudo_dir)
    models = {}
    for geom, reg, lat in MODELS:
        name, b, f, is_top, meta = build_model(geom, reg, lat)
        P.add_struct(f"{name}_init_bound", b); P.add_struct(f"{name}_init_far", f)
        P.add_job(f"{name}_relax", b, name, calc="relax", kind="relax", dip=_dd(meta["endpoints"]["dipfield"]), fixed=meta["fixed_idx"],
                  lateral=meta["lateral_fixed_idx"], tags={"structure": f"{name}_init_bound", "stage": "1 · 제약 이완 (맨 아래층 고정 · 나머지 z 만)"})
        meta["top_mask"] = [bool(v) for v in is_top]
        models[name] = meta
    man = {"schema": "cc_graphite_stage1/v1", "date": date or _dt.date.today().isoformat(), "prereg": PREREG, "code_sha256": _code_sha(),
           "constants": {"A_C": A_C, "A_C_V2": A_C_V2, "D_INIT": D_INIT, "GAP": GAP, "KPTS": KPTS, "ECUT": ECUT, "SMEAR": SMEAR, "DEGAUSS": DEGAUSS},
           "models": models, "structures_sha256": P.struct, "jobs": P.jobs}
    json.dump(man, open(os.path.join(out, "cc_stage1_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    P.write_jobs("WAD-CC 1단계 — 흑연 C|C 제약 이완 9", {"stage1_manifest_sha256": _sha(os.path.join(out, "cc_stage1_manifest.json"))})
    return man


# ─────────────────────────────── 2단계 ───────────────────────────────
def relaxed_from_pw(pw_out, init):
    """이완 출력(마지막 실행 · bfgs converged — P0) → 최종 좌표 Atoms (셀 = 1단계 bound)."""
    from ase import Atoms
    S.parse_pw(pw_out, "relax", True)
    txt = open(pw_out, errors="ignore").read()
    k = txt.rfind("Program PWSCF")
    sym, x = S._read_positions_block(txt[k:] if k >= 0 else txt)
    if sym != init.get_chemical_symbols():
        raise SlabError(f"{pw_out}: 원자 순서·개수가 1단계 bound 와 다르다")
    return Atoms(sym, positions=x, cell=init.cell.array, pbc=(True, True, False))


def stage2(stage1_dir, relax_raw, out, pseudo_dir="/data/work/pseudo", date=None):
    from ase.io import read
    man1 = json.load(open(os.path.join(stage1_dir, "cc_stage1_manifest.json"), encoding="utf-8"))
    P = CCPack(out, pseudo_dir)
    models, status = {}, {}
    for name, m in man1["models"].items():
        init = read(os.path.join(stage1_dir, "structures", f"{name}_init_bound.extxyz"))
        if _sha(os.path.join(stage1_dir, "structures", f"{name}_init_bound.extxyz")) != man1["structures_sha256"][f"{name}_init_bound"]:
            raise SlabError(f"{name}: 1단계 구조 sha 가 manifest 와 다르다")
        pw = os.path.join(relax_raw, f"{name}_relax", "pw.out")
        at = relaxed_from_pw(pw, init)
        x0, x1 = init.get_positions(), at.get_positions()
        dxy = float(np.abs(x1[:, :2] - x0[:, :2]).max())
        dz_fixed = float(np.abs(x1[m["fixed_idx"], 2] - x0[m["fixed_idx"], 2]).max())
        if dxy > 1e-4 or dz_fixed > 1e-4:
            raise SlabError(f"{name}: 제약 위반 — 면내 이동 {dxy:.2e} Å · 고정층 z 이동 {dz_fixed:.2e} Å (둘 다 0 이어야)")
        is_top = np.array(m["top_mask"])
        rep = stack_report(at, m["n_sub_layers"])
        flags = []
        if rep["n_layers"] != m["n_sub_layers"] + m["n_top_layers"]:
            flags.append(f"층 수 {rep['n_layers']}")
        if any(not (SPACING_OK[0] <= s <= SPACING_OK[1]) for s in rep["spacings_A"]):
            flags.append(f"층간 {rep['spacings_A']} 가 {SPACING_OK} 밖")
        if any(fl > FLAT_TOL for fl in rep["flatness_A"]):
            flags.append(f"층 평탄도 {rep['flatness_A']} > {FLAT_TOL}")
        if rep["interface"] != m["registry"] or any(s != "AB" for s in rep["internal"]):
            flags.append(f"적층 {rep['interface']} / {rep['internal']}")
        rec = {"relax_pw_out_sha256": _sha(pw), "max_dxy_A": dxy, "stack_relaxed": rep, "flags": flags, **{k: m[k] for k in ("geometry", "registry", "lattice", "a_A", "n_sub_layers", "n_top_layers", "n_C_contact_layer")}}
        if flags:
            status[name] = "INCOMPLETE"; rec["처리"] = "세고 제외 · 교체 없음 · 2단계 입력 없음"; models[name] = rec
            continue
        status[name] = "OK"
        b, f, em = B.make_endpoints(at, is_top, GAP)
        d0 = em["d0_A"]
        dd = _dd(em["dipfield"])
        P.add_struct(f"{name}_dft_bound", b); P.add_struct(f"{name}_dft_far", f)
        P.add_job(f"{name}_dft_bound", b, name, dip=dd, tags={"structure": f"{name}_dft_bound", "endpoint": "bound", "d0_A": d0})
        P.add_job(f"{name}_dft_far", f, name, dip=dd, tags={"structure": f"{name}_dft_far", "endpoint": "far", "gap_A": GAP})
        if name in REPS:
            f8 = B3._rigid_shift(b, is_top, GAP_INFO - d0)
            if B.dip_region([b, f, f8])["region_A"] != em["dipfield"]["region_A"]:
                raise SlabError(f"{name}: far8 이 쌍극자 구간 집합을 바꾼다")
            P.add_struct(f"{name}_far8", f8)
            P.add_job(f"{name}_far8", f8, name, kind="info", dip=dd, tags={"structure": f"{name}_far8", "info": "직접 8 Å (같은 셀) — 8→10 꼬리 · V2 +0.0136 과 비교"})
            for s in ED_SHIFTS:
                tag = f"{name}_Ed_{'m' if s < 0 else 'p'}{abs(s):.1f}".replace(".", "")
                a2 = B3._rigid_shift(b, is_top, s)
                P.add_struct(tag, a2); P.add_job(tag, a2, name, kind="ed", dip=dd, tags={"structure": tag, "E(d)": f"d0{s:+.1f}"})
            b2, f2i = B3._c_plus(b, 2.0), B3._c_plus(f, 2.0)
            f2ii = B3._rigid_shift(f2i, is_top, 2.0)
            d2 = B.dip_region([b2, f2i, f2ii])
            for tag, a2 in (("G3_c2_bound", b2), ("G3_c2_far_i", f2i), ("G3_c2_far_ii", f2ii)):
                P.add_struct(f"{name}_{tag}", a2); P.add_job(f"{name}_{tag}", a2, name, kind="g3", dip=_dd(d2), tags={"structure": f"{name}_{tag}", "G3": tag})
            for ep, a2 in (("bound", b), ("far", f)):
                P.add_job(f"{name}_G4_e70_{ep}", a2, name, kind="g4", dip=dd, ecut=ECUT_HI, tags={"structure": f"{name}_dft_{ep}", "G4": f"e70_{ep}"})
                P.add_job(f"{name}_G4_k24_{ep}", a2, name, kind="g4", dip=dd, kpts=KPTS_DENSE, tags={"structure": f"{name}_dft_{ep}", "G4": f"k24_{ep}"})
                P.add_job(f"{name}_G4_s05_{ep}", a2, name, kind="g4", dip=dd, degauss=DEGAUSS_HALF, tags={"structure": f"{name}_dft_{ep}", "G4": f"s05_{ep}"})
            rec["G3_dip_region_A"] = d2["region_A"]
        rec.update({"d0_A": d0, "endpoints": em})
        models[name] = rec
    man = {"schema": "cc_graphite_stage2/v1", "date": date or _dt.date.today().isoformat(), "prereg": PREREG, "code_sha256": _code_sha(),
           "stage1_manifest_sha256": _sha(os.path.join(stage1_dir, "cc_stage1_manifest.json")), "relax_raw": relax_raw,
           "status": status, "n_ok": sum(1 for v in status.values() if v == "OK"), "n_incomplete": sum(1 for v in status.values() if v == "INCOMPLETE"),
           "models": models, "structures_sha256": P.struct, "jobs": P.jobs}
    json.dump(man, open(os.path.join(out, "cc_stage2_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    P.write_jobs("WAD-CC 2단계 — 끝점 · E(d) · far8 · G3 · G4", {"stage2_manifest_sha256": _sha(os.path.join(out, "cc_stage2_manifest.json"))})
    return man


# ─────────────────────────────── 집계 ───────────────────────────────
def w_inc(Wab, Wsp, Waa):
    """GSFE 평균 → 비정합 추정. 값이 하나라도 없으면 None (0 으로 채우지 않는다)."""
    if None in (Wab, Wsp, Waa):
        return None
    r = (Wab - Wsp) / (Wab - Waa) if abs(Wab - Waa) > 1e-12 else None
    two = (Waa + 3.0 * Wsp) / 4.0
    return {"W_inc_2star_J_m2": two, "W_inc_1star_J_m2": (2.0 * Wab + Waa) / 3.0, "sigma0_J_m2": Wab - two,
            "star_consistency_ratio": r, "star_consistency_ref": 1.0 / 9.0, "bracket_J_m2": [min(Waa, Wab), max(Waa, Wab)],
            "⚠": "강체 비정합 = GSFE 평균 (Wang 2015 σ0 정의) · 3 registry 푸리에 절단 추정 — 정보량"}


def atm_column(stage2_dir, names):
    """ΔW_ATM = 같은 기하에서 E_D3(s9=1) − E_D3(s9=0) 의 끝점 차 (simple-dftd3 · 3D 주기) — V2 ATM 열과 같은 방법. 없으면 None."""
    try:
        from dftd3.interface import DispersionModel, RationalDampingParam
    except ImportError:
        return {"status": "simple-dftd3 python 없음 — ATM 미계산 (0 아님)"}
    from ase.io import read

    def e_d3(at, s9):
        mdl = DispersionModel(at.get_atomic_numbers(), at.get_positions() / BOHR_A, at.cell.array / BOHR_A, periodic=np.array([True, True, True]))
        return mdl.get_dispersion(RationalDampingParam(s9=s9, **D3BJ_PBE), grad=False)["energy"] * HARTREE_EV
    out = {"method": "simple-dftd3 · PBE D3(BJ) " + json.dumps(D3BJ_PBE) + " · ATM = E(s9=1) − E(s9=0) · 3D 주기", "rows": {}}
    for n in names:
        pb = os.path.join(stage2_dir, "structures", f"{n}_dft_bound.extxyz"); pf = os.path.join(stage2_dir, "structures", f"{n}_dft_far.extxyz")
        if not (os.path.isfile(pb) and os.path.isfile(pf)):
            out["rows"][n] = None; continue
        b, f = read(pb), read(pf)
        A = float(np.linalg.norm(np.cross(b.cell.array[0], b.cell.array[1])))
        atm = (e_d3(f, 1.0) - e_d3(f, 0.0)) - (e_d3(b, 1.0) - e_d3(b, 0.0))
        two = e_d3(f, 0.0) - e_d3(b, 0.0)
        out["rows"][n] = {"dW_ATM_J_m2": atm * EV_J / (A * A2_M2), "dD3_2body_sdftd3_J_m2": two * EV_J / (A * A2_M2)}
    return out


def collect(stage2_dir, raw_dir, atm=False, v2_ref=V2_REF):
    man = json.load(open(os.path.join(stage2_dir, "cc_stage2_manifest.json"), encoding="utf-8"))
    jobs = {j["dir"]: j for j in man["jobs"]}
    J = {j: C4.read_job(raw_dir, stage2_dir, j) for j in jobs}
    ok = lambda x: bool(x) and x.get("status") == "OK"
    rows = {}
    for name, m in man["models"].items():
        if man["status"][name] != "OK":
            rows[name] = {"status": man["status"][name], "flags": m.get("flags")}
            continue
        A = C4.area_A2(os.path.join(stage2_dir, "structures", f"{name}_dft_bound.extxyz"))
        b, f = J.get(f"{name}_dft_bound"), J.get(f"{name}_dft_far")
        W = C4._w(b, f, A)
        r = {"status": "OK" if W is not None else "INCOMPLETE", "d0_A": m["d0_A"], "area_A2": round(A, 6), "a_A": m["a_A"],
             "W_PBE_D3_J_m2": W, "W_PBE_D3_Eint_J_m2": C4._w(b, f, A, "E_int_Ry"), "W_PBE_J_m2": C4._w(b, f, A, "E_pbe_Ry"), "dD3_QE_J_m2": C4._w(b, f, A, "D3_Ry"),
             "W_meV_per_C_contact": ((f["F_Ry"] - b["F_Ry"]) * RY_EV * 1000 / m["n_C_contact_layer"]) if W is not None else None}
        if name in REPS:
            de = lambda x, y: (x["F_Ry"] - y["F_Ry"]) * RY_EV * 1000 if (ok(x) and ok(y)) else None
            ed = {}
            for tag, s in (("Ed_m03", -0.3), ("Ed_p03", 0.3), ("Ed_p06", 0.6)):
                ed[f"d0{s:+.1f}"] = {"d_A": round(m["d0_A"] + s, 4), "dE_meV": de(J.get(f"{name}_{tag}"), b)}
            vals = [ed[k]["dE_meV"] for k in ("d0-0.3", "d0+0.3")]
            r["E_d"] = ed
            r["E_d_local_min_in_grid"] = (all(v > 0 for v in vals) if None not in vals else None)
            W8 = C4._w(b, J.get(f"{name}_far8"), A)
            r["far8_info"] = {"W_8A_J_m2": W8, "dW_8to10_J_m2": (W - W8) if (W is not None and W8 is not None) else None, "V2_ref_dW_8to10": 0.0136}
            g3b, g3i, g3ii = J.get(f"{name}_G3_c2_bound"), J.get(f"{name}_G3_c2_far_i"), J.get(f"{name}_G3_c2_far_ii")
            Wi, Wii = C4._w(g3b, g3i, A), C4._w(g3b, g3ii, A)
            dws = [(Wi - W) if (Wi is not None and W is not None) else None, (Wii - W) if (Wii is not None and W is not None) else None]
            g3 = {"W_i_J_m2": Wi, "W_ii_J_m2": Wii, "dW_i_J_m2": dws[0], "dW_ii_J_m2": dws[1], "threshold_abs_dW": G3_DW,
                  "endpoint_dE_meV": {"bound": de(g3b, b), "far_i": de(g3i, f), "far_ii": de(g3ii, f)}}
            g3["status"] = "INCOMPLETE" if None in dws else ("PASS" if all(abs(v) <= G3_DW for v in dws) else "FAIL")
            if dws[1] is not None:
                g3["tail_1_over_d2_info"] = {"W_inf_est_J_m2": W + dws[1] * (1 / 100.0) / (1 / 100.0 - 1 / 144.0),
                                             "⚠": "D3 꼬리를 1/d² 로 본 외삽 (10→12 Å 기울기) — 정보 · 판정 아님"}
            r["G3"] = g3
            g4 = {}
            for tag in ("e70", "k24", "s05"):
                Wx = C4._w(J.get(f"{name}_G4_{tag}_bound"), J.get(f"{name}_G4_{tag}_far"), A)
                d = (Wx - W) if (Wx is not None and W is not None) else None
                g4[tag] = {"W_J_m2": Wx, "dW_J_m2": d, "threshold_abs_dW": G4_DW, "status": "INCOMPLETE" if d is None else ("PASS" if abs(d) <= G4_DW else "FAIL")}
            st = {v["status"] for v in g4.values()}
            g4["status"] = "INCOMPLETE" if "INCOMPLETE" in st else ("FAIL" if "FAIL" in st else "PASS")
            r["G4"] = g4
        rows[name] = r
    Wof = lambda n: (rows.get(n) or {}).get("W_PBE_D3_J_m2")
    thick = {}
    for thin, thickm in (("CC_S33_AB", "CC_S44_AB"), ("CC_M41_AB", "CC_M61_AB")):
        a, c = Wof(thin), Wof(thickm)
        d = (c - a) if (a is not None and c is not None) else None
        thick[f"{thickm}−{thin}"] = {"dW_J_m2": d, "threshold_abs_dW": THICK_DW, "status": "INCOMPLETE" if d is None else ("PASS" if abs(d) <= THICK_DW else "FAIL")}
    reg = {g: w_inc(Wof(f"CC_{g}_AB"), Wof(f"CC_{g}_SP"), Wof(f"CC_{g}_AA")) for g in ("S33", "M41")}
    wab = Wof("CC_S33_AB")
    control = {"W_S33_AB_J_m2": wab, "band_J_m2": list(BAND),
               "status": "INCOMPLETE" if wab is None else ("IN_BAND" if BAND[0] <= wab <= BAND[1] else "OUT_OF_BAND"),
               "밖이면": "D3 계수를 만지지 않는다 — 원인 진단 (수치 설정 · 분산 모델 계통 편차를 따로)"}
    wang = {"ref": WANG, "W_S33_AB_minus_CE_AB": (wab - WANG["CE_ideal_AB_J_m2"][0]) if wab is not None else None}
    if reg["S33"]:
        wang["W_inc_S33_minus_CE_inc"] = reg["S33"]["W_inc_2star_J_m2"] - WANG["CE_incommensurate_J_m2"][0]
        wang["sigma0_S33_minus_Wang"] = reg["S33"]["sigma0_J_m2"] - WANG["sigma0_J_m2"][0]
    wang["⚠"] = "정보 — 값 대 값 합격 판정이 아니다 (판정은 S33_AB 운영 허용대 하나)"
    strain = {"dW_V2a_minus_base_J_m2": (Wof("CC_M41_AB_V2a") - Wof("CC_M41_AB")) if (Wof("CC_M41_AB_V2a") is not None and Wof("CC_M41_AB") is not None) else None,
              "a_V2a_A": A_C_V2, "a_base_A": A_C}
    v2 = None
    p = os.path.join(REPO, v2_ref[0])
    if os.path.isfile(p):
        g = json.load(open(p, encoding="utf-8"))["registries"][v2_ref[1]]
        v2w = g.get("G3", {}).get("W_ii_J_m2")
        mm = reg["M41"]["W_inc_2star_J_m2"] if reg["M41"] else None
        ss = reg["S33"]["W_inc_2star_J_m2"] if reg["S33"] else None
        v2 = {"V2_W_10A_J_m2": v2w, "src": f"{v2_ref[0]} · {v2_ref[1]} · G3 W_ii (직접 10 Å)",
              "ratio_V2_over_M41_inc": (v2w / mm) if (v2w and mm) else None, "ratio_V2_over_S33_inc": (v2w / ss) if (v2w and ss) else None,
              "⚠": "V2 는 G3 FAIL · k 축 미검증 라벨 · 그래핀 +1.078 % 변형 격자 — 비는 같은 PBE+D3(BJ) 2체 안에서만 뜻이 있다"}
    out = {"schema": "cc_graphite_collect/v1", "stage2": stage2_dir, "raw": raw_dir, "prereg": PREREG, "rows": rows,
           "gates": {"control_S33_AB": control, "G3": {n: rows[n]["G3"]["status"] for n in REPS if "G3" in rows.get(n, {})},
                     "G4": {n: rows[n]["G4"]["status"] for n in REPS if "G4" in rows.get(n, {})}, "thickness": thick},
           "info": {"registry_incommensurate": reg, "wang2015": wang, "strain_V2a": strain, "vs_V2": v2},
           "jobs_not_ok": sorted(j for j, v in J.items() if v["status"] != "OK")}
    if atm:
        out["info"]["ATM"] = atm_column(stage2_dir, [n for n in rows if rows[n].get("status") == "OK"])
    return out


def _print(o):
    f = lambda x, p=4: (f"{x:.{p}f}" if isinstance(x, (int, float)) else "—")
    print(f"{'model':16s} {'d0':>6s} {'W':>8s} {'W_Eint':>8s} {'W_PBE':>8s} {'ΔD3':>7s} {'meV/C':>7s}")
    for n, r in o["rows"].items():
        if r.get("status") not in ("OK", "INCOMPLETE") or "d0_A" not in r:
            print(f"{n:16s} {r.get('status')} {r.get('flags')}"); continue
        print(f"{n:16s} {r['d0_A']:6.3f} {f(r['W_PBE_D3_J_m2']):>8s} {f(r['W_PBE_D3_Eint_J_m2']):>8s} {f(r['W_PBE_J_m2']):>8s} {f(r['dD3_QE_J_m2']):>7s} {f(r['W_meV_per_C_contact'], 1):>7s}")
    g = o["gates"]
    print(f"대조 S33_AB {f(g['control_S33_AB']['W_S33_AB_J_m2'])} · 허용대 {g['control_S33_AB']['band_J_m2']} → {g['control_S33_AB']['status']}")
    print(f"G3 {g['G3']} · G4 {g['G4']} · 두께 { {k: v['status'] for k, v in g['thickness'].items()} }")
    for geo, v in o["info"]["registry_incommensurate"].items():
        if v:
            print(f"{geo}: W_inc 2성 {f(v['W_inc_2star_J_m2'])} · 1성 {f(v['W_inc_1star_J_m2'])} · σ0 {f(v['sigma0_J_m2'])} · 괄호 {[round(x, 4) for x in v['bracket_J_m2']]} · r {f(v['star_consistency_ratio'], 3)} (1/9 = 0.111)")
    print(f"미완 잡 {o['jobs_not_ok']}")


# ─────────────────────────────── selftest ───────────────────────────────
def _fake_relax_out(path, at, dz_top=0.0, top=None, fail=False, dxy=0.0):
    x = at.get_positions().copy()
    if top is not None:
        x[top, 2] += dz_top
    x[:, 0] += dxy
    L = ["     Program PWSCF v.7.4.1 starts", f"     number of atoms/cell      =           {len(at)}", "     convergence has been achieved in  10 iterations",
         "!    total energy              =   -300.00000000 Ry", "     DFT-D3 Dispersion         =   -0.05000000 Ry",
         ("     bfgs failed after 200 scf cycles and 199 bfgs steps, convergence not achieved" if fail else "     bfgs converged in   6 scf cycles and   5 bfgs steps"),
         "Begin final coordinates", "", "ATOMIC_POSITIONS (angstrom)"]
    L += [f"C  {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}" for p in x]
    L += ["End final coordinates", "     convergence has been achieved in   8 iterations", "!    total energy              =   -300.00100000 Ry",
          "     DFT-D3 Dispersion         =   -0.05000000 Ry", "   JOB DONE."]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(L) + "\n")


def _selftest():
    import re
    import shutil
    import tempfile
    from ase.io import read
    n_ok = n_bad = 0
    TOL = 1e-6                                 # J/m² — 합성 pw.out 이 F 를 8 자리로 찍는다 (5e-9 Ry ÷ 5.3 Å² ≈ 2e-7 J/m²)

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")
    # ① 적층 — 좌표 판정
    for geom, reg in (("S33", "AB"), ("S33", "SP"), ("S33", "AA"), ("M41", "AB"), ("M41", "SP"), ("M41", "AA"), ("S44", "AB"), ("M61", "AB")):
        name, b, f, is_top, m = build_model(geom, reg)
        ck(f"적층 {name}: 계면 {reg} · 블록 안 전부 AB · 층당 2", m["stack"]["interface"] == reg and set(m["stack"]["internal"]) == {"AB"} and set(m["stack"]["atoms_per_layer"]) == {2}, m["stack"])
    _, b, _, _, m = build_model("S33", "AB")
    L = layers(b); x = b.get_positions(); a = A_C
    ck("S33_AB = 완전한 Bernal: 층 j 와 j+2 가 같은 xy", all(np.allclose(np.sort(x[L[j], :2], axis=0), np.sort(x[L[j + 2], :2], axis=0)) for j in range(4)))
    ck("AB 판정 기준 거리 a/√3 = C–C 결합 1.4238 Å", abs(a / math.sqrt(3) - 1.42377) < 1e-4)
    ck("layer_offsets: SP 계면 어긋남 = ½ (대각선)", abs((layer_offsets(3, 3, "SP")[1][0] - layer_offsets(3, 3, "SP")[0][-1]) - 0.5) < 1e-12)
    # 좌표 판정이 설계값을 되풀이하지 않는다 — 위층을 손으로 옮기면 판정이 따라간다
    lab = {}
    for k, fr in (("12", 1 / 12), ("6", 1 / 6), ("23", 2 / 3), ("13", 1 / 3)):
        bb = b.copy(); y = bb.get_positions(); y[L[3], :2] += (b.cell.array[0, :2] + b.cell.array[1, :2]) * fr; bb.set_positions(y)
        lab[k] = stacking_label(bb, L[2], L[3])
    ck("좌표 판정이 설계값을 되풀이하지 않는다: AB 위층을 (s,s) 옮기면 ⅙ → SP · ⅔ → AA · ⅓ → AB(BA) · 1/12 → other", lab == {"12": "other", "6": "SP", "23": "AA", "13": "AB"}, lab)
    try:
        layer_offsets(3, 3, "AC"); bad = False
    except SlabError:
        bad = True
    ck("⛔음성: 없는 registry → SlabError", bad)
    lo0 = layer_offsets
    try:
        globals()["layer_offsets"] = lambda n_sub, n_top, reg: lo0(n_sub, n_top, "AA")   # 이름은 SP · 실제로는 AA 를 만든다
        build_model("S33", "SP"); bad = False
    except SlabError as ex:
        bad = "설계와 다르다" in str(ex)
    finally:
        globals()["layer_offsets"] = lo0
    ck("⛔음성 빌더: 좌표로 판정한 적층이 이름과 다르면 거부 (SP 라 부르고 AA 를 만들면)", bad)
    # ② 격자 · V2 연결
    ck("V2 그래핀 격자 = a_Ag·√3/(2√2) → 변형 +1.078 % (build_v2 와 같은 값)", abs(100 * (A_C_V2 / A_C - 1) - B.build_v2()["top_fcc"]["meta"]["graphene_strain_pct"]) < 2e-3, A_C_V2)
    # ③ 끝점 · 쌍극자
    for geom, reg, lat in MODELS:
        name, b, f, is_top, m = build_model(geom, reg, lat)
        em = m["endpoints"]
        if not (em["far_gap_direct_image_A"][0] >= GAP - 1e-6 and em["far_gap_direct_image_A"][1] >= GAP - 1e-6
                and em["dipfield"]["clearance_A"]["to_top_atom"] >= 4 - 1e-6 and em["dipfield"]["clearance_A"]["to_substrate_bottom_image"] >= 4 - 1e-6):
            ck(f"끝점 {name}: far ≥ 10/10 · 쌍극자 여유 ≥ 4/4", False, em); break
    else:
        ck("끝점 9 모델: far 직접·영상 ≥ 10 Å · 쌍극자 여유 ≥ 4/4 Å", True)
    with tempfile.TemporaryDirectory() as T:
        s1 = os.path.join(T, "s1")
        m1 = stage1(s1, date="2026-09-28")
        m1b = stage1(os.path.join(T, "s1b"), date="2026-09-28")
        ck("1단계: 9 모델 · 이완 9 잡 · 결정성 (두 번 빌드 sha 동일)", len(m1["models"]) == 9 and len(m1["jobs"]) == 9 and [j["pw_in_sha256"] for j in m1["jobs"]] == [j["pw_in_sha256"] for j in m1b["jobs"]] and m1["structures_sha256"] == m1b["structures_sha256"])
        r = open(os.path.join(s1, "qe", "CC_S33_AB_relax", "pw.in")).read()
        ck("1단계 입력 S33_AB: '0 0 0' 2 · '0 0 1' 10 · '1 1 1' 0 · relax · k 18 18 1", r.count("  0 0 0") == 2 and r.count("  0 0 1") == 10 and r.count("  1 1 1") == 0 and "calculation = 'relax'" in r and "  18 18 1 0 0 0" in r)
        ck("1단계 입력: mv 0.01 · D3(BJ) 2체 · dipfield · eamp 0 · 52/520", "smearing = 'mv'" in r and "degauss = 0.01\n" in r and "dftd3_version = 4" in r and "dftd3_threebody = .false." in r
           and "dipfield = .true." in r and "eamp = 0.0d0" in r and "ecutwfc = 52.0" in r and "ecutrho = 520.0" in r and "gaussian" not in r)
        # V2 와 같은 설정 — 실제 V2 2단계 입력과 설정 줄 대조 (Ag·원자 수·쌍극자 위치·prefix 제외)
        v2p = os.path.join(REPO, "db", "inputs", "wad_aprime_s4_v2_stage2_2026_09_26", "V2_top_fcc", "qe", "V2_top_fcc_dft_bound", "pw.in")
        if os.path.isfile(v2p):
            keys = ("ecutwfc", "ecutrho", "occupations", "smearing", "degauss", "nspin", "vdw_corr", "dftd3_version", "dftd3_threebody", "conv_thr", "mixing_beta",
                    "mixing_mode", "electron_maxstep", "tefield", "dipfield", "edir", "eamp", "disk_io", "tprnfor", "ibrav")
            kv = lambda t: {k: v.strip() for k, v in re.findall(r"^\s*(\w+)\s*=\s*(.+)$", t, re.M) if k in keys}
            cc_scf = qe_input_cc(read(os.path.join(s1, "structures", "CC_S33_AB_init_bound.extxyz")), "x", KPTS, "/p", dip=_dd(m1["models"]["CC_S33_AB"]["endpoints"]["dipfield"]))
            v2kv, cckv = kv(open(v2p).read()), kv(cc_scf)
            ck("V2 와 같은 설정: 20 개 키 전부 같은 값 (smearing mv · degauss 0.01 포함)", v2kv == cckv and len(cckv) == len(keys), {k: (v2kv.get(k), cckv.get(k)) for k in keys if v2kv.get(k) != cckv.get(k)})
        else:
            ck("V2 2단계 입력이 repo 에 있다", False, v2p)
        # 원 작성기가 바뀌면 조용히 치환하지 않는다
        orig = B3.qe_input
        try:
            B3.qe_input = lambda *a, **k: orig(*a, **k).replace("degauss = 0.005", "degauss = 0.004")
            qe_input_cc(read(os.path.join(s1, "structures", "CC_S33_AB_init_bound.extxyz")), "x", KPTS, "/p"); bad = False
        except SlabError:
            bad = True
        finally:
            B3.qe_input = orig
        ck("⛔음성: 원 작성기의 smearing 줄이 예상과 다르면 거부 (조용한 치환 없음)", bad)
        jj = json.load(open(os.path.join(s1, "qe", "jobs.json"), encoding="utf-8"))
        ck("jobs.json: 러너 형식 (dir·calc·kind·pw_in_sha256) · PP 해시 C · kind↔calc probe 불일치 0", all({"dir", "calc", "kind", "pw_in_sha256"} <= set(j) for j in jj["jobs"])
           and jj["settings"]["pp_sha256"] == {PP_C: B3.PP_SHA[PP_C]} and all((j["kind"] == "probe") == (j["calc"] == "probe") for j in jj["jobs"])
           and all(_sha(os.path.join(s1, "qe", j["dir"], "pw.in")) == j["pw_in_sha256"] for j in jj["jobs"]))
        # ④ 2단계 — 합성 이완 출력 (위 블록 z +0.05 Å)
        raw1 = os.path.join(T, "run1")
        for name, m in m1["models"].items():
            init = read(os.path.join(s1, "structures", f"{name}_init_bound.extxyz"))
            _fake_relax_out(os.path.join(raw1, f"{name}_relax", "pw.out"), init, 0.05, np.where(m["top_mask"])[0])
        s2 = os.path.join(T, "s2")
        m2 = stage2(s1, raw1, s2, date="2026-09-28")
        m2b = stage2(s1, raw1, os.path.join(T, "s2b"), date="2026-09-28")
        kinds = {}
        for j in m2["jobs"]:
            kinds[j["kind"]] = kinds.get(j["kind"], 0) + 1
        ck("2단계: OK 9 · 잡 44 (scf 18 · far8 2 · E(d) 6 · G3 6 · G4 12) · 결정성", m2["n_ok"] == 9 and len(m2["jobs"]) == 44 and kinds == {"scf": 18, "info": 2, "ed": 6, "g3": 6, "g4": 12}
           and [j["pw_in_sha256"] for j in m2["jobs"]] == [j["pw_in_sha256"] for j in m2b["jobs"]], kinds)
        ck("2단계: d₀ = 3.35 + 0.05 (이완 좌표에서 다시)", abs(m2["models"]["CC_S33_AB"]["d0_A"] - 3.40) < 1e-4 and abs(m2["models"]["CC_M41_SP"]["d0_A"] - 3.40) < 1e-4)
        e = m2["models"]["CC_S33_AB"]["endpoints"]
        ck("2단계 끝점: far 직접 10 · 영상 ≥ 10 · 쌍극자 여유 ≥ 4", abs(e["far_gap_direct_image_A"][0] - 10.0) < 1e-3 and e["far_gap_direct_image_A"][1] >= 10 - 1e-6 and e["dipfield"]["clearance_A"]["to_top_atom"] >= 4 - 1e-6)
        f8 = read(os.path.join(s2, "structures", "CC_S33_AB_far8.extxyz")); tm = np.array(m1["models"]["CC_S33_AB"]["top_mask"]); y = f8.get_positions()
        ck("far8: 같은 셀 · 직접 간격 8.000 Å", abs(float(y[tm, 2].min() - y[~tm, 2].max()) - 8.0) < 1e-6 and abs(f8.cell.array[2, 2] - e["c_A"]) < 1e-4)
        base = open(os.path.join(s2, "qe", "CC_S33_AB_dft_bound", "pw.in")).read()
        for tag, want in (("s05", ("degauss = 0.01\n", "degauss = 0.005\n")), ("k24", ("  18 18 1 0 0 0", "  24 24 1 0 0 0")), ("e70", ("ecutwfc = 52.0\n  ecutrho = 520.0", "ecutwfc = 70.0\n  ecutrho = 700.0"))):
            g = open(os.path.join(s2, "qe", f"CC_S33_AB_G4_{tag}_bound", "pw.in")).read()
            ck(f"G4 {tag}: base 와 한 곳만 다르다", g.replace(f"G4_{tag}_bound", "dft_bound").replace(want[1], want[0]) == base and want[1] in g)
        # ⑤ 2단계 음성
        bad1 = os.path.join(T, "run1_bad"); shutil.copytree(raw1, bad1)
        init = read(os.path.join(s1, "structures", "CC_S33_AA_init_bound.extxyz"))
        _fake_relax_out(os.path.join(bad1, "CC_S33_AA_relax", "pw.out"), init, 0.0, None, fail=True)
        try:
            stage2(s1, bad1, os.path.join(T, "x1")); bad = False
        except SlabError:
            bad = True
        ck("⛔음성 2단계: bfgs failed 출력 → 거부 (P0)", bad)
        _fake_relax_out(os.path.join(bad1, "CC_S33_AA_relax", "pw.out"), init, 0.0, None, dxy=0.01)
        try:
            stage2(s1, bad1, os.path.join(T, "x2")); bad = False
        except SlabError as ex:
            bad = "제약 위반" in str(ex)
        ck("⛔음성 2단계: 면내 이동 0.01 Å → 거부 (z 만 제약 위반)", bad)
        _fake_relax_out(os.path.join(bad1, "CC_S33_AA_relax", "pw.out"), init, 1.2, np.where(m1["models"]["CC_S33_AA"]["top_mask"])[0])
        mx = stage2(s1, bad1, os.path.join(T, "x3"))
        ck("⛔음성 2단계: 계면 층간 4.55 Å (> 4.2) → INCOMPLETE · 잡 없음 · 나머지는 그대로", mx["status"]["CC_S33_AA"] == "INCOMPLETE" and not any(j["model"] == "CC_S33_AA" for j in mx["jobs"]) and mx["n_ok"] == 8, mx["models"]["CC_S33_AA"].get("flags"))
        # ⑥ 집계 — 합성 에너지 (W 를 알고 넣는다)
        raw2 = os.path.join(T, "run2")
        W = {"CC_S33_AB": 0.400, "CC_S33_SP": 0.390, "CC_S33_AA": 0.350, "CC_M41_AB": 0.360, "CC_M41_SP": 0.352, "CC_M41_AA": 0.316, "CC_S44_AB": 0.405, "CC_M61_AB": 0.362, "CC_M41_AB_V2a": 0.350}
        F0 = -100.0

        def put(job, F, d3=-0.05, nat=12):
            d = os.path.join(raw2, job); os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(s2, "qe", job, "pw.in"), os.path.join(d, "pw.in"))
            C4._fake_out(os.path.join(d, "pw.out"), F, d3, nat=nat)
        for name in W:
            A = C4.area_A2(os.path.join(s2, "structures", f"{name}_dft_bound.extxyz"))
            dF = W[name] * A * A2_M2 / C4.RY_J
            put(f"{name}_dft_bound", F0); put(f"{name}_dft_far", F0 + dF, d3=-0.04)
            if name in REPS:
                put(f"{name}_far8", F0 + dF - 0.004 * A * A2_M2 / C4.RY_J)
                for tag, e_ in (("Ed_m03", 2e-3), ("Ed_p03", 1e-3), ("Ed_p06", 3e-3)):
                    put(f"{name}_{tag}", F0 + e_)
                put(f"{name}_G3_c2_bound", F0 + 1e-5); put(f"{name}_G3_c2_far_i", F0 + dF + 1e-5); put(f"{name}_G3_c2_far_ii", F0 + dF + 1e-5 + 0.002 * A * A2_M2 / C4.RY_J)
                for tag in ("e70", "k24", "s05"):
                    put(f"{name}_G4_{tag}_bound", F0 - 0.1); put(f"{name}_G4_{tag}_far", F0 - 0.1 + dF + 0.005 * A * A2_M2 / C4.RY_J)
        o = collect(s2, raw2)
        ck("집계: W 9 개 복원 (|오차| < 1e-6 · 합성 출력 8 자리 반올림)", all(abs(o["rows"][n]["W_PBE_D3_J_m2"] - W[n]) < TOL for n in W), {n: o["rows"][n]["W_PBE_D3_J_m2"] for n in W})
        ri = o["info"]["registry_incommensurate"]["S33"]
        ck("비정합: 2성 (0.35 + 3·0.39)/4 = 0.38 · 1성 (0.80 + 0.35)/3 = 0.38333 · σ0 0.02 · r 0.2", abs(ri["W_inc_2star_J_m2"] - 0.38) < TOL and abs(ri["W_inc_1star_J_m2"] - 1.15 / 3) < TOL
           and abs(ri["sigma0_J_m2"] - 0.02) < TOL and abs(ri["star_consistency_ratio"] - 0.2) < 1e-4 and np.allclose(ri["bracket_J_m2"], [0.35, 0.4], atol=TOL), ri)
        ck("비정합 1성 = 2성 (SP 가 1/9 규칙을 따르면)", abs(w_inc(0.4, 0.4 - 0.05 / 9, 0.35)["W_inc_1star_J_m2"] - w_inc(0.4, 0.4 - 0.05 / 9, 0.35)["W_inc_2star_J_m2"]) < 1e-12)
        g = o["gates"]
        ck("게이트: 대조 IN_BAND · G3 PASS ×2 · G4 PASS ×2 (ΔW 0.005 ≤ 0.01) · 두께 PASS ×2", g["control_S33_AB"]["status"] == "IN_BAND" and set(g["G3"].values()) == {"PASS"} and set(g["G4"].values()) == {"PASS"}
           and len(g["G3"]) == 2 and all(v["status"] == "PASS" for v in g["thickness"].values()), g)
        rr = o["rows"]["CC_S33_AB"]
        ck("far8 정보: 8→10 +0.004 · E(d) 국소 최소 · 1/d² 꼬리 외삽 = W + 3.273·ΔW(ii)", abs(rr["far8_info"]["dW_8to10_J_m2"] - 0.004) < TOL and rr["E_d_local_min_in_grid"] is True
           and abs(rr["G3"]["tail_1_over_d2_info"]["W_inf_est_J_m2"] - (0.4 + 0.002 * (1 / 100) / (1 / 100 - 1 / 144))) < 10 * TOL)
        ck("meV/C (접촉층 C 2): S33_AB 0.40 J/m² ≈ 65.7 meV/C", abs(rr["W_meV_per_C_contact"] - rr["W_PBE_D3_J_m2"] * rr["area_A2"] * A2_M2 / EV_J * 1000 / 2) < 1e-4 and abs(rr["W_meV_per_C_contact"] - 65.74) < 0.01, rr["W_meV_per_C_contact"])
        ck("Wang 정보: W_inc − 0.37 = +0.01 · σ0 − 0.022 = −0.002 · 판정 아님 표시", abs(o["info"]["wang2015"]["W_inc_S33_minus_CE_inc"] - 0.01) < TOL and abs(o["info"]["wang2015"]["sigma0_S33_minus_Wang"] + 0.002) < TOL and "판정" in o["info"]["wang2015"]["⚠"])
        v2 = o["info"]["vs_V2"]
        ck("V2 비: repo 의 V2 10 Å 값(0.4491) / M41 W_inc", v2 is not None and v2["V2_W_10A_J_m2"] is not None and abs(v2["V2_W_10A_J_m2"] - 0.4491) < 5e-4 and abs(v2["ratio_V2_over_M41_inc"] - v2["V2_W_10A_J_m2"] / o["info"]["registry_incommensurate"]["M41"]["W_inc_2star_J_m2"]) < 1e-12, v2)
        ck("변형 정보: V2a − base = −0.010", abs(o["info"]["strain_V2a"]["dW_V2a_minus_base_J_m2"] + 0.010) < TOL)
        # ⑦ 집계 음성
        A = C4.area_A2(os.path.join(s2, "structures", "CC_S33_AB_dft_bound.extxyz"))
        put("CC_S33_AB_G4_k24_far", F0 - 0.1 + 0.4 * A * A2_M2 / C4.RY_J + 0.012 * A * A2_M2 / C4.RY_J)
        o2 = collect(s2, raw2)
        ck("⛔음성 G4: k24 ΔW 0.012 → FAIL (C|C 문턱 0.01 · V2 의 0.02 아님)", o2["rows"]["CC_S33_AB"]["G4"]["k24"]["status"] == "FAIL" and o2["gates"]["G4"]["CC_S33_AB"] == "FAIL")
        put("CC_S33_AB_G4_k24_far", F0 - 0.1 + 0.4 * A * A2_M2 / C4.RY_J + 0.005 * A * A2_M2 / C4.RY_J)
        put("CC_M41_AB_G3_c2_far_ii", F0 + 1e-5 + (0.36 + 0.015) * C4.area_A2(os.path.join(s2, "structures", "CC_M41_AB_dft_bound.extxyz")) * A2_M2 / C4.RY_J)
        og = collect(s2, raw2)
        ck("⛔음성 G3: M41 직접 검사 ΔW +0.015 → FAIL (ii_direct 만) · S33 은 PASS 그대로", og["gates"]["G3"] == {"CC_S33_AB": "PASS", "CC_M41_AB": "FAIL"}
           and abs(og["rows"]["CC_M41_AB"]["G3"]["dW_ii_J_m2"] - 0.015) < TOL and abs(og["rows"]["CC_M41_AB"]["G3"]["dW_i_J_m2"]) < TOL, og["gates"]["G3"])
        put("CC_M41_AB_G3_c2_far_ii", F0 + 1e-5 + (0.36 + 0.002) * C4.area_A2(os.path.join(s2, "structures", "CC_M41_AB_dft_bound.extxyz")) * A2_M2 / C4.RY_J)
        put("CC_S33_AB_dft_far", F0 + 0.50 * A * A2_M2 / C4.RY_J, d3=-0.04)
        o3 = collect(s2, raw2)
        ck("⛔음성 대조: S33_AB 0.50 → OUT_OF_BAND · 두께 S44−S33 −0.095 → FAIL", o3["gates"]["control_S33_AB"]["status"] == "OUT_OF_BAND" and o3["gates"]["thickness"]["CC_S44_AB−CC_S33_AB"]["status"] == "FAIL")
        put("CC_S33_AB_dft_far", F0 + 0.40 * A * A2_M2 / C4.RY_J, d3=-0.04)
        os.remove(os.path.join(raw2, "CC_S33_SP_dft_far", "pw.out"))
        o4 = collect(s2, raw2)
        ck("⛔음성 누락: S33_SP far 없음 → W None · S33 비정합 None (0 아님) · 미완 목록", o4["rows"]["CC_S33_SP"]["W_PBE_D3_J_m2"] is None and o4["info"]["registry_incommensurate"]["S33"] is None
           and "CC_S33_SP_dft_far" in o4["jobs_not_ok"] and "W_inc_S33_minus_CE_inc" not in o4["info"]["wang2015"])
        put("CC_S33_SP_dft_far", F0 + 0.39 * A * A2_M2 / C4.RY_J, d3=-0.04)
        open(os.path.join(raw2, "CC_M41_AB_dft_bound", "pw.in"), "a").write("! 손댄 입력\n")
        o5 = collect(s2, raw2)
        ck("⛔음성 입력 불일치: 실행 pw.in 이 패키지와 다르면 INVALID · W None", o5["rows"]["CC_M41_AB"]["W_PBE_D3_J_m2"] is None and o5["rows"]["CC_M41_AB"]["status"] == "INCOMPLETE")
        # ⑧ ATM 열 (simple-dftd3 있으면 계산 · 없으면 None 문구)
        at = atm_column(s2, ["CC_S33_AB"])
        if "rows" in at:
            v = at["rows"]["CC_S33_AB"]
            ck("ATM: 값이 유한 · 2체 ΔD3 > 0 (분리하면 분산 에너지가 오른다)", v is not None and math.isfinite(v["dW_ATM_J_m2"]) and v["dD3_2body_sdftd3_J_m2"] > 0, v)
        else:
            ck("ATM: simple-dftd3 없으면 0 이 아니라 문구", "없음" in at.get("status", ""), at)
    # ⑨ 카드 결속 — 사전등록 카드가 있으면 문턱·모델·registry·설정이 코드와 같아야 한다
    card_p = os.path.join(REPO, PREREG)
    if os.path.isfile(card_p):
        c = json.load(open(card_p, encoding="utf-8"))["code_binding"]
        ck("카드 결속: 문턱 · 허용대 · 모델 · REPS · k · 간격 · smearing", c["BAND"] == list(BAND) and c["G3_DW"] == G3_DW and c["G4_DW"] == G4_DW and c["THICK_DW"] == THICK_DW
           and c["MODELS"] == [list(t) for t in MODELS] and c["REPS"] == list(REPS) and c["KPTS"] == list(KPTS) and c["KPTS_DENSE"] == list(KPTS_DENSE) and c["GAP"] == GAP
           and c["SMEAR"] == [SMEAR, DEGAUSS, DEGAUSS_HALF] and c["SPACING_OK"] == list(SPACING_OK) and c["FLAT_TOL"] == FLAT_TOL, c)
    print(f"{'✅' if n_bad == 0 else '⛔'} cc_graphite selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--stage1", action="store_true")
    ap.add_argument("--stage2", action="store_true")
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--stage1_dir"); ap.add_argument("--relax_raw"); ap.add_argument("--stage2_dir"); ap.add_argument("--raw")
    ap.add_argument("--atm", action="store_true", help="simple-dftd3 로 ATM 열 (정보)")
    ap.add_argument("--out"); ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.stage1:
        if not a.out:
            ap.error("--out")
        m = stage1(a.out, a.pseudo_dir)
        for n, v in m["models"].items():
            print(f"✓ {n}: 원자 {v['n_atoms']} · a {v['a_A']:.5f} · c {v['endpoints']['c_A']} Å · 계면 {v['stack']['interface']} · far {v['endpoints']['far_gap_direct_image_A']}")
        print(f"→ {a.out}/qe/jobs.json ({len(m['jobs'])} 잡)")
        return 0
    if a.stage2:
        if not (a.stage1_dir and a.relax_raw and a.out):
            ap.error("--stage1_dir · --relax_raw · --out")
        m = stage2(a.stage1_dir, a.relax_raw, a.out, a.pseudo_dir)
        print(json.dumps({"status": m["status"], "n_jobs": len(m["jobs"]), "d0_A": {n: v.get("d0_A") for n, v in m["models"].items()}}, ensure_ascii=False, indent=1))
        print(f"→ {a.out}/qe/jobs.json")
        return 0
    if a.collect:
        if not (a.stage2_dir and a.raw):
            ap.error("--stage2_dir · --raw")
        o = collect(a.stage2_dir, a.raw, a.atm)
        _print(o)
        if a.out:
            json.dump(o, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float); open(a.out, "a").write("\n"); print(f"-> {a.out}")
        return 0
    ap.error("--selftest · --stage1 · --stage2 · --collect 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SlabError as e:
        print(f"⛔ {e}")
        sys.exit(2)
