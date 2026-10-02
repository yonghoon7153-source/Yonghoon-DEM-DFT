#!/usr/bin/env python3
"""agc_graphite.py — WAD-AgC: Ag(111)|흑연(0001) 고정기하 W_sep (DEM P1b · 인터레이어 안쪽 계면) · 사전등록 카드 `PREREG`.

왜: 무음극 셀 LPSCl | Ag–C (Ag + 덴카블랙) | VGCF 의 인터레이어 **안쪽** 계면 = Ag 입자 | 탄소. A′ V2 (Ag(111)|그래핀 단층) 값에는
    '그래핀 단층은 흑연 두께 수렴 대체물이 아니다' 라벨이 붙어 있다. 같은 옆 셀 · 같은 QE 설정 · 같은 제약으로 탄소를 **흑연 3층(ABA)** 으로
    바꿔 다시 잰다 (탄소 두께 점검 4층 · V2 입력을 이 기계에서 다시 돌리는 기계 대조 포함).
왜 새 파일인가: cc_graphite.py 는 C|C 카드 하나에 결박돼 있다 (MODELS·문턱·PREREG 가 그 카드의 값 결속 시험에 걸려 있다). 기판(Ag)·고정 규칙·
    registry 정의·대조(V2)·기계(kgy) 가 달라 같은 파일에 두면 두 카드가 한 상수 블록을 공유한다. 기하·QE 작성기·집계 함수는 그대로 import 한다
    (build_aprime_interfaces · build_aprime_s3 · collect_aprime_s4 · cc_graphite · se_sym_slab).

    python3 tools/wad/agc_graphite.py --registry_scan [--n_c 3]                 # 1/6 격자 이동의 대칭 동치류 (카드 §2 registry 선택 근거)
    python3 tools/wad/agc_graphite.py --stage1 --out db/inputs/wad_agc_graphite_2026_10_02/stage1
    python3 tools/wad/agc_graphite.py --stage2 --stage1_dir <stage1> --relax_raw <1단계 RUN> --out <stage2>
    python3 tools/wad/agc_graphite.py --verify_stage2 <kgy 의 stage2> --stage1_dir <stage1> --relax_raw <1단계 RUN>   # 결정성 대조
    python3 tools/wad/agc_graphite.py --collect --stage1_dir <stage1> --stage2_dir <stage2> --raw1 <1단계 RUN> --raw2 <2단계 RUN> \
            [--fallback_raw <β 0.1 대체 RUN>] [--atm] [--out result.json]
    python3 tools/wad/agc_graphite.py --selftest

모델 (카드 §2): Ag(111) (√3×√3)R30° 4층 (12 Ag · a_Ag = A_AG_PBE_D3 · 아래 2층 고정 · 위 2층 자유) + 흑연 2×2 · ABA (Bernal) · N_C 층
  (층당 C 8 · Ag 격자에 맞춰 +1.078 % · C 는 z 만) — V2 와 같은 옆 셀 · 같은 제약 · 같은 registry 매개(접촉층 C0 의 Ag 윗면 원시격자 분수 이동).
  AGC_N3_{top_fcc, top_hcp, hollow_fcc, s01} · AGC_N4_top_fcc (탄소 두께 점검) · CTRL_V2_top_fcc_dft_{bound,far} (기계 대조 — V2 2단계 입력 그대로)
⛔ registry: V2 의 넷(top_fcc · top_hcp · bridge · hollow_fcc)은 대칭으로 **둘**뿐이었다 — bridge ≡ top_fcc (병진 동치 · V2 W 16 자리 같음) ·
  top_hcp ≡ hollow_fcc (거울 동치 · 3e-6 J/m² 차). 흑연(ABA)에서는 2층이 거울을 깨서 top_hcp 와 hollow_fcc 가 갈린다.
  ⇒ 넷 = V2 이름 셋 + 1/6 격자에서 사전순으로 처음 나오는 비등가 이동 s01 = (0, 1/6). `registry_equivalences` 가 ASE
  SymmetryEquivalenceCheck 로 쌍별 비등가를 확인하고, 등가 쌍이 섞이면 1단계를 만들지 않는다.
QE = V2 와 같음 (`build_aprime_s3.qe_input` 그대로 · Ag 가 있어 mv 0.01): 52/520 · PBE+D3(BJ) 2체 · nspin 1 · local-TF 0.3 · 쌍극자 개정 2 ·
  k 6×6×1 (V2 와 같은 값 — 같은 k 끼리 비교) · relax etot 1e-5 · forc 1e-3 · bfgs · nstep 200.
끝점: far 직접·영상 ≥ 10 Å (V2 교훈 — 8 Å 에서 G3 FAIL) · far8 (같은 셀 · 직접 8 Å) 은 V2 의 8 Å 값과 비교하는 정보.
SCF 미수렴 대비 (결과 전): 2단계 잡마다 β 0.1 판을 같이 만든다 (`fallback/qe`) — 원 잡이 SCF 미수렴일 때만 한 번 · 그래도 미수렴이면 INCOMPLETE.
⛔ 못 하는 것: 에너지를 계산하지 않는다 (집계만) · 결과를 보고 문턱·표본을 바꾸지 않는다 · 비정합(회전) 계면을 계산하지 않는다 (2×2 정합 셀) ·
   실물 Ag 입자·덴카블랙의 결함·작용기·곡률을 모른다 (이상 Ag(111) · 이상 흑연 기저면) · Ag 표면 재구성은 안 본다 · E(d) 는 강체 분리
   (이완 없음) 라 DEM 박리 곡선의 근사 입력일 뿐이다 · 흑연 블록의 다른 Bernal 방향(ACA)은 표본 밖이다.
"""
import argparse
import datetime as _dt
import hashlib
import itertools
import json
import math
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import se_sym_slab as S                    # noqa: E402
import build_aprime_interfaces as B        # noqa: E402
import build_aprime_s3 as B3               # noqa: E402
import collect_aprime_s4 as C4             # noqa: E402
import cc_graphite as CC                   # noqa: E402

SlabError = S.SlabError
REPO = S.REPO
PREREG = "db/properties/wad_agc_graphite_prereg_2026_10_02.json"

# ── 카드 값 (결과 뒤 바꾸지 않는다 · selftest ⑩ 이 카드 code_binding 과 대조한다) ──
A_AG, A_C = B.A_AG_PBE_D3, B.A_C_PBE_D3
N_AG = 4
N_C, N_C_THICK = 3, 4
D0_INIT, DC_INIT = 3.30, CC.D_INIT          # 시작 간격 — 이완이 정한다 (V2 이완 d₀ ≈ 3.30 · 흑연 3.35)
GAP, GAP_INFO = 10.0, 8.0
KPTS, KPTS_G4 = (6, 6, 1), (9, 9, 1)        # 9 = 3 의 배수 (그래핀 K 점 포함) · 간격 0.162 Å⁻¹ ≤ 0.20
ECUT, ECUT_HI = (52.0, 520.0), (70.0, 700.0)
DEGAUSS, DEGAUSS_HALF = 0.01, 0.005
BETA, BETA_FALLBACK = 0.3, 0.1
ED_SHIFTS = tuple(B3.ED_SHIFTS)             # (-0.3, 0.3, 0.6) — V2 와 같은 국소 최소 점검
ED_EXTRA = (1.0, 1.5, 2.0, 3.0, 4.5)        # 강체 분리 곡선 (DEM 이 요청한 E(d) 의 근사 · 정보)
REGISTRIES = {"top_fcc": (0.0, 0.0), "top_hcp": (1.0 / 3.0, 2.0 / 3.0), "hollow_fcc": (2.0 / 3.0, 1.0 / 3.0), "s01": (0.0, 1.0 / 6.0)}
REP = "top_fcc"                             # E(d) · G3 · G4 · 두께 대상 (V2 의 G3 대표와 같은 이름)
G1_DW, G3_DW, G4_DW, THICK_DW = 0.002, 0.01, 0.01, 0.02
SPACING_OK, D0_OK, FLAT_TOL, STACK_TOL = (3.0, 4.2), (2.8, 4.2), 0.05, 0.05
N_C_PER_LAYER = 8
CTRL_SRC = "db/inputs/wad_aprime_s4_v2_stage2_2026_09_26/V2_top_fcc"
CTRL_JOBS = ("V2_top_fcc_dft_bound", "V2_top_fcc_dft_far")
CTRL_REF = ("db/raw/wad_aprime_s4_v2s2_2026_09_26/collect_aprime_s4_2026_09_26.json", "V2_top_fcc")
CTRL_V100_RAW = "db/raw/wad_aprime_s4_v2s2_2026_09_26/V2_top_fcc"
V2_SAME_NAME = {"top_fcc": "V2_top_fcc", "top_hcp": "V2_top_hcp", "hollow_fcc": "V2_hollow_fcc"}
MACHINE = "kgy RTX3090 24 GB (run_sese_gpu.sh · PWX·PSEUDO_DIR env · li2s v2 UMA 와 GPU 공유)"
SPEED_DAYS_ASK = 7.0                        # 첫 이완 실측으로 낸 총 견적이 이보다 길면 사용자에게 다시 묻는다 (카드 §9 · 실행 설정)
PP_EL = ("Ag", "C")
RY_EV, EV_J, A2_M2 = C4.RY_EV, C4.EV_J, C4.A2_M2


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def model_name(n_c, reg):
    return f"AGC_N{n_c}_{reg}"


REP_NAME = model_name(N_C, REP)
THICK_NAME = model_name(N_C_THICK, REP)


# ─────────────────────────────── 기하 ───────────────────────────────
def _assemble(n_c, f1, f2, a_ag=A_AG, a_c=A_C, d0=D0_INIT, dc=DC_INIT, n_ag=N_AG, bern_sign=1.0):
    """Ag(111)√3 n_ag 층 + 흑연 2×2 n_c 층 (ABA) — 접촉층 C0 = Ag 윗면 기준 원자 t0 + f1·p1 + f2·p2 (V2 와 같은 매개).
    → (Atoms (c = 0 · 끝점 전), 변형률 %). 2층 = 1층 + bern_sign·(⅙, ⅙) 셀 분수 (= 그래핀 원시 (⅓, ⅓)) · 3층 = 1층."""
    from ase import Atoms
    if n_c < 1:
        raise SlabError("흑연 층 수 ≥ 1")
    sub = B.ag111_root_slab(a_ag, n_ag)
    C = sub.cell.array.copy()
    xy_c, strain = B.graphene_2x2_in_cell(C, a_c)
    B._strain_guard([strain], "AgC 흑연 on Ag(111)√3")
    t0, p1, p2 = B._top_layer_primitive(sub)
    z_top = float(sub.get_positions()[:, 2].max())
    base = xy_c - xy_c[0] + sub.get_positions()[t0, :2] + f1 * p1 + f2 * p2
    bern = bern_sign * (C[0, :2] + C[1, :2]) / 6.0
    pos = []
    for k in range(n_c):
        xy = base + (bern if k % 2 else 0.0)
        pos += [[x, y, z_top + d0 + k * dc] for x, y in xy]
    at = sub + Atoms("C" * len(pos), positions=pos)
    at.set_cell(C); at.set_pbc((True, True, False))
    return at, strain


def stacking_2x2(at, lower, upper, a_prim, tol=STACK_TOL):
    """두 탄소층의 적층 (좌표에서 · 원자 표지와 무관). 위층 원자마다 아래층 최근접 면내 거리 → AB = 절반 0 · 절반 a/√3 · AA = 전부 0."""
    x = at.get_positions(); C = at.cell.array
    dm = sorted(min(d for i in lower for d, _na, _nb, _v in B._images_inplane(x[j] - x[i], C)) for j in upper)
    n = len(dm)
    n0 = sum(1 for v in dm if v < tol)
    nb = sum(1 for v in dm if abs(v - a_prim / math.sqrt(3.0)) < tol)
    if n0 == n:
        return "AA"
    if n % 2 == 0 and n0 == n // 2 and nb == n // 2:
        return "AB"
    return "other"


def carbon_report(at, is_c):
    """탄소층 · 층간 · 평탄도 · 블록 안 적층 · Ag–C 직접 간격 d₀ (전부 좌표에서)."""
    idx = np.where(is_c)[0]
    L = [[int(idx[i]) for i in l] for l in CC.layers(at[idx])]
    z = at.get_positions()[:, 2]
    zc = [float(np.mean(z[l])) for l in L]
    a_prim = float(np.linalg.norm(at.cell.array[0])) / 2.0
    ag = np.where(~np.asarray(is_c))[0]
    return {"n_layers": len(L), "atoms_per_layer": [len(l) for l in L], "layer_z_A": [round(v, 4) for v in zc],
            "spacings_A": [round(zc[k + 1] - zc[k], 4) for k in range(len(zc) - 1)],
            "flatness_A": [round(float(z[l].max() - z[l].min()), 4) for l in L],
            "internal": [stacking_2x2(at, L[k], L[k + 1], a_prim) for k in range(len(L) - 1)],
            "d0_A": round(float(z[idx].min() - z[ag].max()), 4), "a_graphene_prim_A": round(a_prim, 6), "layers": L}


def build_model(n_c, reg, gap=GAP):
    """→ (이름, bound, far, is_c, meta). 끝점 = V2 와 같은 `make_endpoints` (쌍극자 개정 2) · 고정 = far_half(Ag) · 측방 = C 전부."""
    if reg not in REGISTRIES:
        raise SlabError(f"registry {reg} — {list(REGISTRIES)} 만")
    f1, f2 = REGISTRIES[reg]
    bound, strain = _assemble(n_c, f1, f2)
    is_c = np.array([s == "C" for s in bound.get_chemical_symbols()])
    b, f, em = B.make_endpoints(bound, is_c, gap)
    rep = carbon_report(b, is_c)
    if rep["n_layers"] != n_c or any(n != N_C_PER_LAYER for n in rep["atoms_per_layer"]):
        raise SlabError(f"{model_name(n_c, reg)}: 탄소층 구성 {rep['atoms_per_layer']}")
    if any(s != "AB" for s in rep["internal"]):
        raise SlabError(f"{model_name(n_c, reg)}: 좌표 판정 블록 안 적층 {rep['internal']} — 설계(ABA)와 다르다")
    fixed = S.fixed_mask_policy(b, ads_elements=("C",), substrate_elements=("Ag",))
    lateral = [int(i) for i in np.where(is_c)[0]]
    chk = S.interface_check(b, f, ads_elements=("C",), substrate_elements=("Ag",), fixed_idx=fixed, lateral_fixed_idx=lateral)
    name = model_name(n_c, reg)
    meta = {"model": name, "n_C_layers": n_c, "registry": reg, "shift_frac_primitive": [f1, f2], "a_Ag_A": A_AG, "a_C_A": A_C,
            "graphite_strain_pct": round(strain, 3), "n_Ag": int((~is_c).sum()), "n_C": int(is_c.sum()), "n_C_contact_layer": N_C_PER_LAYER,
            "area_A2": round(float(np.linalg.norm(np.cross(b.cell.array[0], b.cell.array[1]))), 6),
            "fixed_idx": fixed, "lateral_fixed_idx": lateral, "c_mask": [bool(v) for v in is_c], "carbon": {k: v for k, v in rep.items() if k != "layers"},
            "endpoints": em, "interface_check_flags": chk["flags"], "d0_init_A": D0_INIT, "dc_init_A": DC_INIT}
    return name, b, f, is_c, meta


# ─────────────────────────────── registry 대칭 ───────────────────────────────
def _compare_atoms(n_c, f1, f2):
    at, _ = _assemble(n_c, f1, f2)
    C = at.cell.array.copy(); C[2] = [0.0, 0.0, 45.0]
    at.set_cell(C); at.set_pbc(True); at.wrap()        # 진공이 커서 3D 주기로 비교해도 z 영상은 섞이지 않는다
    return at


def _comparator():
    from ase.utils.structure_comparator import SymmetryEquivalenceCheck
    return SymmetryEquivalenceCheck(angle_tol=1.0, ltol=0.05, stol=0.05, vol_tol=0.1, scale_volume=False, to_primitive=False)


def registry_equivalences(n_c, shifts):
    """shifts = {이름: (f1, f2)} → 대칭 등가(회전·거울·병진 포함 · ASE SymmetryEquivalenceCheck) 인 쌍 목록. 비면 전부 비등가."""
    comp = _comparator()
    at = {k: _compare_atoms(n_c, *v) for k, v in shifts.items()}
    return [[a, b] for a, b in itertools.combinations(list(shifts), 2) if comp.compare(at[a], at[b])]


def registry_scan(n_c=N_C, grid=6):
    """V2 이름 넷 + (i/grid, j/grid) 이동 → 대칭 동치류 (나온 순서대로). 카드 §2 의 registry 선택 근거 (결과 전)."""
    cands = [("top_fcc", (0.0, 0.0)), ("top_hcp", (1 / 3, 2 / 3)), ("bridge", (0.5, 0.0)), ("hollow_fcc", (2 / 3, 1 / 3))]
    cands += [(f"g{i}{j}", (i / grid, j / grid)) for i in range(grid) for j in range(grid)]
    comp = _comparator()
    classes = []
    for name, (f1, f2) in cands:
        at = _compare_atoms(n_c, f1, f2)
        for c in classes:
            if comp.compare(at, c["atoms"]):
                c["members"].append(name); break
        else:
            classes.append({"rep": name, "shift": [f1, f2], "atoms": at, "members": [name]})
    return [{k: v for k, v in c.items() if k != "atoms"} for c in classes]


# ─────────────────────────────── 묶음 ───────────────────────────────
def _replace_once(text, old, new, what):
    if text.count(old) != 1:
        raise SlabError(f"{what}: '{old.strip()}' 줄이 정확히 하나가 아니다 ({text.count(old)}) — 치환하지 않는다")
    return text.replace(old, new)


class AgcPack:
    """구조 파일 · pw.in · qe/jobs.json (run_sese_gpu.sh 의 IN = <out>/qe)."""
    def __init__(self, out, pseudo_dir, what):
        self.out, self.pseudo_dir, self.what = out, pseudo_dir, what
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

    def _write(self, name, text, rec):
        d = os.path.join(self.out, "qe", name); os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "pw.in")
        open(p, "w").write(text)
        rec["pw_in_sha256"] = _sha(p)
        self.jobs.append(rec)
        return p

    def add_job(self, name, atoms, model, calc="scf", kind="scf", dip=None, fixed=(), lateral=(), ecut=ECUT, kpts=KPTS,
                degauss=DEGAUSS, beta=BETA, tags=None):
        t = B3.qe_input(atoms, name, kpts, self.pseudo_dir, calc, dip, fixed, lateral, ecut, 200, d3=True)
        if degauss != DEGAUSS:
            t = _replace_once(t, f"  degauss = {DEGAUSS}\n", f"  degauss = {degauss}\n", name)
        if beta != BETA:
            t = _replace_once(t, f"  mixing_beta = {BETA}\n", f"  mixing_beta = {beta}\n", name)
        rec = {"dir": name, "kind": kind, "calc": calc, "model": model, "nat": len(atoms), "kpts": list(kpts), "ecutwfc": ecut[0], "ecutrho": ecut[1],
               "smearing": "mv", "degauss": degauss, "mixing_beta": beta, "electron_maxstep": 200, "d3": "PBE+D3(BJ) 2체", "dip": dip,
               "structure": (tags or {}).get("structure"), "tags": tags or {}, "machine": MACHINE}
        return self._write(name, t, rec)

    def add_copy(self, name, src, kind, model, tags=None):
        """다른 묶음의 pw.in 을 **바이트 그대로** (기계 대조용 — 러너가 바꾸는 pseudo_dir 줄 말고는 같은 입력)."""
        t = open(src).read()
        rec = {"dir": name, "kind": kind, "calc": "scf", "model": model, "source_pw_in": os.path.relpath(src, REPO), "source_sha256": _sha(src),
               "tags": tags or {}, "machine": MACHINE}
        p = self._write(name, t, rec)
        if rec["pw_in_sha256"] != rec["source_sha256"]:
            raise SlabError(f"{name}: 복사본 sha 가 원본과 다르다")
        return p

    def write_jobs(self, extra=None):
        doc = {"schema": "qe_input_set/v1", "what": self.what, "prereg": PREREG,
               "settings": {"pp": {e: B3.PP[e][1] for e in PP_EL}, "pp_sha256": {B3.PP[e][1]: B3.PP_SHA[B3.PP[e][1]] for e in PP_EL},
                            "pseudo_dir_note": "러너가 PSEUDO_DIR 로 바꾼다 (실행 폴더 복사본에서만)"},
               "jobs": self.jobs}
        doc.update(extra or {})
        p = os.path.join(self.out, "qe", "jobs.json")
        json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
        return p


def _dd(dip):
    return {"emaxpos": dip["emaxpos"], "eopreg": dip["eopreg"]}


def _code_sha():
    return {os.path.relpath(os.path.join(HERE, f), REPO): _sha(os.path.join(HERE, f))
            for f in ("agc_graphite.py", "cc_graphite.py", "build_aprime_interfaces.py", "build_aprime_s3.py", "collect_aprime_s4.py", "se_sym_slab.py")}


def _models_stage1():
    return [(N_C, reg) for reg in REGISTRIES] + [(N_C_THICK, REP)]


# ─────────────────────────────── 1단계 ───────────────────────────────
def stage1(out, pseudo_dir="/data/work/pseudo", date=None, check_registry=True):
    """기계 대조 2 (V2 입력 그대로) → 제약 이완 5 (N3 × registry 4 · N4 대표). 등가 registry 가 섞이면 만들지 않는다."""
    eq = registry_equivalences(N_C, REGISTRIES) if check_registry else None
    if eq:
        raise SlabError(f"registry 대칭 등가 쌍 {eq} — 서로 비등가인 넷이어야 한다 (09-23 계획 · 카드 §2)")
    P = AgcPack(out, pseudo_dir, "WAD-AgC 1단계 — 기계 대조 2 (V2 입력 그대로) · Ag(111)|흑연 제약 이완 5")
    src = os.path.join(REPO, CTRL_SRC)
    for j in CTRL_JOBS:
        P.add_copy(f"CTRL_{j}", os.path.join(src, "qe", j, "pw.in"), "ctrl", "CTRL_V2",
                   tags={"G1": "기계 대조 — V100 의 같은 입력과 W 비교", "ref": f"{CTRL_REF[0]} · {CTRL_REF[1]}"})
    models = {}
    for n_c, reg in _models_stage1():
        name, b, f, is_c, meta = build_model(n_c, reg)
        P.add_struct(f"{name}_init_bound", b); P.add_struct(f"{name}_init_far", f)
        P.add_job(f"{name}_relax", b, name, calc="relax", kind="relax", dip=_dd(meta["endpoints"]["dipfield"]), fixed=meta["fixed_idx"],
                  lateral=meta["lateral_fixed_idx"], tags={"structure": f"{name}_init_bound", "stage": "1 · 제약 이완 (Ag 아래 2층 고정 · 위 2층 자유 · C 는 z 만)"})
        models[name] = meta
    man = {"schema": "agc_graphite_stage1/v1", "date": date or _dt.date.today().isoformat(), "prereg": PREREG, "code_sha256": _code_sha(),
           "constants": {"A_AG": A_AG, "A_C": A_C, "N_AG": N_AG, "N_C": N_C, "N_C_THICK": N_C_THICK, "D0_INIT": D0_INIT, "DC_INIT": DC_INIT,
                         "GAP": GAP, "KPTS": KPTS, "ECUT": ECUT, "DEGAUSS": DEGAUSS, "REGISTRIES": REGISTRIES, "REP": REP},
           "registry_check": {"pairs_equivalent": eq, "method": "ASE SymmetryEquivalenceCheck (angle 1° · ltol·stol 0.05) · N_C 층 구조"},
           "ctrl": {"source": CTRL_SRC, "jobs": list(CTRL_JOBS), "ref": list(CTRL_REF)},
           "models": models, "structures_sha256": P.struct, "jobs": P.jobs}
    json.dump(man, open(os.path.join(out, "agc_stage1_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    P.write_jobs({"stage1_manifest_sha256": _sha(os.path.join(out, "agc_stage1_manifest.json"))})
    return man


# ─────────────────────────────── 2단계 ───────────────────────────────
def _relax_ok(pw):
    """마지막 실행 bfgs converged (P0) 이면 None · 아니면 사유 (없음·미수렴·실패)."""
    if not os.path.isfile(pw):
        return "이완 출력 없음"
    try:
        S.parse_pw(pw, "relax", True)
    except SlabError as ex:
        return f"이완 미완료·실패: {ex}"
    return None


def stage2(stage1_dir, relax_raw, out, pseudo_dir="/data/work/pseudo", date=None):
    from ase.io import read
    man1 = json.load(open(os.path.join(stage1_dir, "agc_stage1_manifest.json"), encoding="utf-8"))
    P = AgcPack(out, pseudo_dir, "WAD-AgC 2단계 — 끝점 · far8 · E(d) · G3 · G4 · 두께")
    PF = AgcPack(os.path.join(out, "fallback"), pseudo_dir, "WAD-AgC 2단계 대체 — β 0.1 (원 잡이 SCF 미수렴일 때만 · 한 번)")
    models, status = {}, {}
    for name, m in man1["models"].items():
        sp = os.path.join(stage1_dir, "structures", f"{name}_init_bound.extxyz")
        if _sha(sp) != man1["structures_sha256"][f"{name}_init_bound"]:
            raise SlabError(f"{name}: 1단계 구조 sha 가 manifest 와 다르다")
        init = read(sp); init.set_pbc((True, True, False))
        pw = os.path.join(relax_raw, f"{name}_relax", "pw.out")
        why = _relax_ok(pw)
        if why:
            status[name] = "INCOMPLETE"; models[name] = {"flags": [why], "처리": "세고 제외 · 교체 없음 · 2단계 입력 없음"}
            continue
        at = CC.relaxed_from_pw(pw, init)
        x0, x1 = init.get_positions(), at.get_positions()
        is_c = np.array(m["c_mask"])
        dxy_c = float(np.abs(x1[is_c, :2] - x0[is_c, :2]).max())
        d_fix = float(np.abs(x1[m["fixed_idx"]] - x0[m["fixed_idx"]]).max())
        if dxy_c > 1e-4 or d_fix > 1e-4:
            raise SlabError(f"{name}: 제약 위반 — C 면내 이동 {dxy_c:.2e} Å · 고정 Ag 이동 {d_fix:.2e} Å (둘 다 0 이어야 · 입력·러너를 본다)")
        rep = carbon_report(at, is_c)
        flags = []
        if rep["n_layers"] != m["n_C_layers"] or any(n != N_C_PER_LAYER for n in rep["atoms_per_layer"]):
            flags.append(f"탄소층 {rep['atoms_per_layer']}")
        if any(not (SPACING_OK[0] <= s <= SPACING_OK[1]) for s in rep["spacings_A"]):
            flags.append(f"흑연 층간 {rep['spacings_A']} 가 {SPACING_OK} 밖")
        if any(fl > FLAT_TOL for fl in rep["flatness_A"]):
            flags.append(f"탄소층 평탄도 {rep['flatness_A']} > {FLAT_TOL}")
        if any(s != "AB" for s in rep["internal"]):
            flags.append(f"블록 안 적층 {rep['internal']}")
        if not (D0_OK[0] <= rep["d0_A"] <= D0_OK[1]):
            flags.append(f"Ag–C 간격 d₀ {rep['d0_A']} 가 {D0_OK} 밖")
        chk = S.interface_check(init, at, ads_elements=("C",), substrate_elements=("Ag",), fixed_idx=m["fixed_idx"], lateral_fixed_idx=m["lateral_fixed_idx"])
        flags += [f"interface_check: {fl}" for fl in chk["flags"]]
        rec = {"relax_pw_out_sha256": _sha(pw), "carbon_relaxed": {k: v for k, v in rep.items() if k != "layers"}, "flags": flags,
               "max_dxy_C_A": dxy_c, **{k: m[k] for k in ("n_C_layers", "registry", "n_C_contact_layer")}}
        if flags:
            status[name] = "INCOMPLETE"; rec["처리"] = "세고 제외 · 교체 없음 · 2단계 입력 없음"; models[name] = rec
            continue
        status[name] = "OK"
        b, f, em = B.make_endpoints(at, is_c, GAP)
        d0, dd = em["d0_A"], _dd(em["dipfield"])
        todo = []                                           # (이름, 원자, kind, kw, tags) — 원 잡 · β 0.1 대체 잡에 똑같이
        P.add_struct(f"{name}_dft_bound", b); P.add_struct(f"{name}_dft_far", f)
        todo += [(f"{name}_dft_bound", b, "scf", {"dip": dd}, {"structure": f"{name}_dft_bound", "endpoint": "bound", "d0_A": d0}),
                 (f"{name}_dft_far", f, "scf", {"dip": dd}, {"structure": f"{name}_dft_far", "endpoint": "far", "gap_A": GAP})]
        if m["n_C_layers"] == N_C:
            f8 = B3._rigid_shift(b, is_c, GAP_INFO - d0)
            if B.dip_region([b, f, f8])["region_A"] != em["dipfield"]["region_A"]:
                raise SlabError(f"{name}: far8 이 쌍극자 구간 집합을 바꾼다")
            P.add_struct(f"{name}_far8", f8)
            todo.append((f"{name}_far8", f8, "info", {"dip": dd}, {"structure": f"{name}_far8", "info": "직접 8 Å (같은 셀) — V2 8 Å 값과 비교"}))
        if name == REP_NAME:
            for s in ED_SHIFTS + ED_EXTRA:
                tag = f"{name}_Ed_{'m' if s < 0 else 'p'}{abs(s):.1f}".replace(".", "")
                a2 = B3._rigid_shift(b, is_c, s)
                if B.dip_region([b, f, a2])["region_A"] != em["dipfield"]["region_A"]:
                    raise SlabError(f"{tag}: E(d) 점이 쌍극자 구간 집합을 바꾼다")
                P.add_struct(tag, a2)
                todo.append((tag, a2, "ed", {"dip": dd}, {"structure": tag, "E(d)": f"d0{s:+.1f}", "d_A": round(d0 + s, 4)}))
            b2, f2i = B3._c_plus(b, 2.0), B3._c_plus(f, 2.0)
            f2ii = B3._rigid_shift(f2i, is_c, 2.0)
            d2 = B.dip_region([b2, f2i, f2ii])
            for tag, a2 in (("G3_c2_bound", b2), ("G3_c2_far_i", f2i), ("G3_c2_far_ii", f2ii)):
                P.add_struct(f"{name}_{tag}", a2)
                todo.append((f"{name}_{tag}", a2, "g3", {"dip": _dd(d2)}, {"structure": f"{name}_{tag}", "G3": tag}))
            for ep, a2 in (("bound", b), ("far", f)):
                todo += [(f"{name}_G4_e70_{ep}", a2, "g4", {"dip": dd, "ecut": ECUT_HI}, {"structure": f"{name}_dft_{ep}", "G4": f"e70_{ep}"}),
                         (f"{name}_G4_k9_{ep}", a2, "g4", {"dip": dd, "kpts": KPTS_G4}, {"structure": f"{name}_dft_{ep}", "G4": f"k9_{ep}"}),
                         (f"{name}_G4_s05_{ep}", a2, "g4", {"dip": dd, "degauss": DEGAUSS_HALF}, {"structure": f"{name}_dft_{ep}", "G4": f"s05_{ep}"})]
            rec["G3_dip_region_A"] = d2["region_A"]
        for jn, a2, kind, kw, tags in todo:
            P.add_job(jn, a2, name, kind=kind, tags=tags, **kw)
            PF.add_job(f"{jn}_b01", a2, name, kind=kind, beta=BETA_FALLBACK, tags={**tags, "substitutes": jn,
                       "rule": "원 잡이 SCF 미수렴일 때만 한 번 (카드 §4 · 결과 전) · 그래도 미수렴이면 INCOMPLETE"}, **kw)
        rec.update({"d0_A": d0, "endpoints": em})
        models[name] = rec
    man = {"schema": "agc_graphite_stage2/v1", "date": date or _dt.date.today().isoformat(), "prereg": PREREG, "code_sha256": _code_sha(),
           "stage1_manifest_sha256": _sha(os.path.join(stage1_dir, "agc_stage1_manifest.json")), "relax_raw": relax_raw,
           "status": status, "n_ok": sum(1 for v in status.values() if v == "OK"), "n_incomplete": sum(1 for v in status.values() if v == "INCOMPLETE"),
           "models": models, "structures_sha256": P.struct, "jobs": P.jobs, "fallback_jobs": PF.jobs}
    json.dump(man, open(os.path.join(out, "agc_stage2_manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
    ms = _sha(os.path.join(out, "agc_stage2_manifest.json"))
    P.write_jobs({"stage2_manifest_sha256": ms}); PF.write_jobs({"stage2_manifest_sha256": ms})
    return man


def verify_stage2(stage1_dir, relax_raw, pkg_dir):
    """다른 기계에서 만든 2단계 패키지 ↔ 같은 이완 출력으로 **여기서 다시 만든** 것 (원 잡 + 대체 잡).
    같아야 하는 것: 잡 목록 · pw.in sha (manifest 와 디스크) · 구조 좌표·셀 (1e-8 Å) · 모델 상태. 구조 파일 sha 는 비교하지 않는다 (ASE 판 머리글)."""
    import tempfile
    from ase.io import read
    theirs = json.load(open(os.path.join(pkg_dir, "agc_stage2_manifest.json"), encoding="utf-8"))
    with tempfile.TemporaryDirectory() as T:
        ours = stage2(stage1_dir, relax_raw, T, date=theirs.get("date"))
        res = {}
        for key, sub in (("jobs", ""), ("fallback_jobs", "fallback")):
            a = {j["dir"]: j["pw_in_sha256"] for j in theirs[key]}
            b = {j["dir"]: j["pw_in_sha256"] for j in ours[key]}
            disk = {d: (_sha(os.path.join(pkg_dir, sub, "qe", d, "pw.in")) if os.path.isfile(os.path.join(pkg_dir, sub, "qe", d, "pw.in")) else None) for d in a}
            res[key] = {"same_list": sorted(a) == sorted(b), "pw_in_sha_mismatch": sorted(d for d in a if a[d] != b.get(d)),
                        "disk_vs_manifest_mismatch": sorted(d for d in a if disk[d] != a[d])}
        geo = []
        for k in sorted(set(theirs["structures_sha256"]) | set(ours["structures_sha256"])):
            pa, pb = os.path.join(pkg_dir, "structures", f"{k}.extxyz"), os.path.join(T, "structures", f"{k}.extxyz")
            if not (os.path.isfile(pa) and os.path.isfile(pb)):
                geo.append(k); continue
            x, y = read(pa), read(pb)
            if len(x) != len(y) or not np.allclose(x.cell.array, y.cell.array, atol=1e-8) or not np.allclose(x.get_positions(), y.get_positions(), atol=1e-8):
                geo.append(k)
    res.update({"structure_geometry_mismatch": geo, "status_same": theirs["status"] == ours["status"], "code_sha_same_info": theirs.get("code_sha256") == ours.get("code_sha256")})
    res["pass"] = bool(all(v["same_list"] and not v["pw_in_sha_mismatch"] and not v["disk_vs_manifest_mismatch"] for v in (res["jobs"], res["fallback_jobs"]))
                       and not geo and res["status_same"])
    return res


# ─────────────────────────────── 집계 ───────────────────────────────
def _read_with_fallback(raw2, stage2_dir, job, fb_raw, fb_dirs):
    """원 잡 → OK 면 그대로. 아니면 β 0.1 대체 잡(있고 OK 일 때만)으로 — 원 상태는 `original` 에 남긴다 (조용한 교체 금지)."""
    r = C4.read_job(raw2, stage2_dir, job)
    if r.get("status") == "OK" or not fb_raw or f"{job}_b01" not in fb_dirs:
        return r
    s = C4.read_job(fb_raw, os.path.join(stage2_dir, "fallback"), f"{job}_b01")
    if s.get("status") == "OK":
        s["substituted_for"] = job; s["original"] = {k: r.get(k) for k in ("status", "why")}
        return s
    r["fallback"] = {k: s.get(k) for k in ("status", "why")}
    return r


def _tsv_wall(raw, job):
    p = os.path.join(raw, "jobs_run.tsv")
    if not os.path.isfile(p):
        return None
    rows = [ln.rstrip("\n").split("\t") for ln in open(p, encoding="utf-8")]
    hit = [r for r in rows[1:] if r and r[0] == job and len(r) > 3 and r[2] == "1"]
    return int(hit[-1][3]) if hit else None


def ctrl_check(stage1_dir, raw1):
    """G1 — V2_top_fcc 2단계 입력을 이 기계에서 다시 돌린 W ↔ V100 W. |ΔW| ≤ G1_DW → PASS. 벽시계 비 = 속도 정보."""
    J = {j: C4.read_job(raw1, stage1_dir, f"CTRL_{j}") for j in CTRL_JOBS}
    A = C4.area_A2(os.path.join(REPO, CTRL_SRC, "structures", f"{CTRL_JOBS[0]}.extxyz"))
    Wk = C4._w(J[CTRL_JOBS[0]], J[CTRL_JOBS[1]], A)
    ref = json.load(open(os.path.join(REPO, CTRL_REF[0]), encoding="utf-8"))["registries"][CTRL_REF[1]]["W_PBE_D3_J_m2"]
    d = (Wk - ref) if Wk is not None else None
    out = {"W_here_J_m2": Wk, "W_V100_J_m2": ref, "dW_J_m2": d, "threshold_abs_dW": G1_DW,
           "status": "INCOMPLETE" if d is None else ("PASS" if abs(d) <= G1_DW else "FAIL"),
           "FAIL 이면": "P1b 헤드라인 보류 (MACHINE_MISMATCH) — 원인(바이너리·PP·D3 구현) 확인 전 V2·WAD-CC 와 같은 표에 안 놓는다"}
    dF, speed = {}, {}
    for j in CTRL_JOBS:
        v = os.path.join(REPO, CTRL_V100_RAW, j, "pw.out")
        if J[j].get("status") == "OK" and os.path.isfile(v):
            try:
                dF[j] = (J[j]["F_Ry"] - S.parse_pw(v, "scf", True)["E_tot_Ry"]) * RY_EV * 1000
            except SlabError:
                dF[j] = None
        here = _tsv_wall(raw1, f"CTRL_{j}"); v100 = _tsv_wall(os.path.join(REPO, CTRL_V100_RAW), j)
        speed[j] = {"wall_here_s": here, "wall_V100_s": v100, "ratio": (here / v100) if (here and v100) else None}
    out["dF_vs_V100_meV_info"] = dF
    out["speed_info"] = speed
    return out


def _ed_curve(ed_rows, area):
    """강체 E(d) → 이웃 점 사이 기울기 = 견인력 σ = d(ΔE/A)/dd (GPa · 1 J/m²/Å = 10 GPa). 정보 — 이완 없음."""
    pts = sorted((r["d_A"], r["dE_meV"]) for r in ed_rows if r.get("dE_meV") is not None)
    tr = []
    for (d1, e1), (d2, e2) in zip(pts, pts[1:]):
        w = (e2 - e1) * 1e-3 * EV_J / (area * A2_M2)
        tr.append({"d_mid_A": round(0.5 * (d1 + d2), 4), "traction_GPa": w / (d2 - d1) * 10.0})
    mx = max(tr, key=lambda t: t["traction_GPa"]) if tr else None
    return {"points_d_A_dE_meV": [[round(d, 4), e] for d, e in pts], "traction": tr, "max_traction_info": mx,
            "⚠": "강체 분리 (위 블록만 +z · 이완 없음) · 2체 D3 · 2×2 정합 셀 — DEM 박리 곡선의 근사 입력 (정보 · 판정 아님)"}


def collect(stage1_dir, stage2_dir, raw1, raw2, fallback_raw=None, atm=False):
    man1 = json.load(open(os.path.join(stage1_dir, "agc_stage1_manifest.json"), encoding="utf-8"))
    man2 = json.load(open(os.path.join(stage2_dir, "agc_stage2_manifest.json"), encoding="utf-8"))
    fb_dirs = {j["dir"] for j in man2.get("fallback_jobs", [])}
    J = {j["dir"]: _read_with_fallback(raw2, stage2_dir, j["dir"], fallback_raw, fb_dirs) for j in man2["jobs"]}
    ok = lambda x: bool(x) and x.get("status") == "OK"
    rows = {}
    for name in man1["models"]:
        if man2["status"].get(name) != "OK":
            rows[name] = {"status": man2["status"].get(name, "MISSING"), "flags": man2["models"].get(name, {}).get("flags")}
            continue
        m = man2["models"][name]
        A = C4.area_A2(os.path.join(stage2_dir, "structures", f"{name}_dft_bound.extxyz"))
        b, f = J.get(f"{name}_dft_bound"), J.get(f"{name}_dft_far")
        W = C4._w(b, f, A)
        r = {"status": "OK" if W is not None else "INCOMPLETE", "n_C_layers": m["n_C_layers"], "registry": m["registry"], "d0_A": m["d0_A"], "area_A2": round(A, 6),
             "W_PBE_D3_J_m2": W, "W_PBE_D3_Eint_J_m2": C4._w(b, f, A, "E_int_Ry"), "W_PBE_J_m2": C4._w(b, f, A, "E_pbe_Ry"), "dD3_QE_J_m2": C4._w(b, f, A, "D3_Ry"),
             "W_meV_per_C_contact": ((f["F_Ry"] - b["F_Ry"]) * RY_EV * 1000 / m["n_C_contact_layer"]) if W is not None else None,
             "substituted": sorted(k for k in (f"{name}_dft_bound", f"{name}_dft_far") if (J.get(k) or {}).get("substituted_for"))}
        if m["n_C_layers"] == N_C:
            W8 = C4._w(b, J.get(f"{name}_far8"), A)
            r["far8_info"] = {"W_8A_J_m2": W8, "dW_8to10_J_m2": (W - W8) if (W is not None and W8 is not None) else None}
        if name == REP_NAME:
            de = lambda x, y: (x["F_Ry"] - y["F_Ry"]) * RY_EV * 1000 if (ok(x) and ok(y)) else None
            ed = []
            for s in ED_SHIFTS + ED_EXTRA:
                tag = f"{name}_Ed_{'m' if s < 0 else 'p'}{abs(s):.1f}".replace(".", "")
                ed.append({"shift_A": s, "d_A": round(m["d0_A"] + s, 4), "dE_meV": de(J.get(tag), b)})
            near = [e["dE_meV"] for e in ed if e["shift_A"] in (-0.3, 0.3)]
            r["E_d"] = ed
            r["E_d_local_min_in_grid"] = (all(v > 0 for v in near) if None not in near else None)
            far_pt = [{"shift_A": None, "d_A": round(m["d0_A"] + (GAP - m["d0_A"]), 4), "dE_meV": de(f, b)}]
            r["E_d_curve_info"] = _ed_curve([{"d_A": m["d0_A"], "dE_meV": 0.0 if ok(b) else None}] + ed + far_pt, A)
            g3b, g3i, g3ii = J.get(f"{name}_G3_c2_bound"), J.get(f"{name}_G3_c2_far_i"), J.get(f"{name}_G3_c2_far_ii")
            Wi, Wii = C4._w(g3b, g3i, A), C4._w(g3b, g3ii, A)
            dws = [(Wi - W) if (Wi is not None and W is not None) else None, (Wii - W) if (Wii is not None and W is not None) else None]
            g3 = {"W_i_J_m2": Wi, "W_ii_J_m2": Wii, "dW_i_J_m2": dws[0], "dW_ii_J_m2": dws[1], "threshold_abs_dW": G3_DW}
            g3["status"] = "INCOMPLETE" if None in dws else ("PASS" if all(abs(v) <= G3_DW for v in dws) else "FAIL")
            r["G3"] = g3
            g4 = {}
            for tag in ("e70", "k9", "s05"):
                jb, jf = J.get(f"{name}_G4_{tag}_bound"), J.get(f"{name}_G4_{tag}_far")
                Wx = C4._w(jb, jf, A)
                d = (Wx - W) if (Wx is not None and W is not None) else None
                g4[tag] = {"W_J_m2": Wx, "dW_J_m2": d, "threshold_abs_dW": G4_DW, "status": "INCOMPLETE" if d is None else ("PASS" if abs(d) <= G4_DW else "FAIL"),
                           "substituted": [k for k, v in ((f"{name}_G4_{tag}_bound", jb), (f"{name}_G4_{tag}_far", jf)) if (v or {}).get("substituted_for")]}
            st = {v["status"] for v in g4.values()}
            g4["status"] = "INCOMPLETE" if "INCOMPLETE" in st else ("FAIL" if "FAIL" in st else "PASS")
            r["G4"] = g4
        rows[name] = r
    Wof = lambda n: (rows.get(n) or {}).get("W_PBE_D3_J_m2")
    a, c = Wof(REP_NAME), Wof(THICK_NAME)
    dth = (c - a) if (a is not None and c is not None) else None
    thick = {"pair": f"{THICK_NAME} − {REP_NAME}", "dW_J_m2": dth, "threshold_abs_dW": THICK_DW,
             "status": "INCOMPLETE" if dth is None else ("PASS" if abs(dth) <= THICK_DW else "FAIL")}
    g1 = ctrl_check(stage1_dir, raw1)
    n3 = [model_name(N_C, r) for r in REGISTRIES]
    vals = [Wof(n) for n in n3 if Wof(n) is not None]
    head = {"what": f"Ag(111)|흑연(0001) {N_C}층 · W_sep (끝점 {GAP:g} Å · PBE+D3(BJ) 2체) · registry 평균 [min, max]",
            "n_ok": len(vals), "n_registry": len(n3), "incomplete": [n for n in n3 if Wof(n) is None],
            "mean_J_m2": (sum(vals) / len(vals)) if vals else None, "range_J_m2": [min(vals), max(vals)] if vals else None,
            "status": "HELD (MACHINE_MISMATCH — G1 FAIL)" if g1["status"] == "FAIL" else ("OK" if vals else "INCOMPLETE")}
    labels = ["이상 Ag(111) · 이상 흑연 기저면 · 2×2 정합 셀 (비정합 아님) · 흑연 +1.078 % 변형 (Ag 격자) · ABA 한 방향",
              "PBE+D3(BJ) 2체 조건부 (ATM 은 별도 열) · DFT 국소 이완 d₀ 의 고정기하 분리일"]
    for k, gname in (("G1", g1["status"]), ("G3", (rows.get(REP_NAME) or {}).get("G3", {}).get("status")),
                     ("G4", (rows.get(REP_NAME) or {}).get("G4", {}).get("status")), ("두께", thick["status"])):
        if gname != "PASS":
            labels.append(f"{k} {gname or 'INCOMPLETE'}")
    v2 = {}
    p = os.path.join(REPO, CTRL_REF[0])
    if os.path.isfile(p):
        g = json.load(open(p, encoding="utf-8"))["registries"]
        for reg, v2n in V2_SAME_NAME.items():
            w8 = (rows.get(model_name(N_C, reg)) or {}).get("far8_info", {}).get("W_8A_J_m2")
            vv = (g.get(v2n) or {}).get("W_PBE_D3_J_m2")
            v2[reg] = {"W_P1b_8A_J_m2": w8, "W_V2_8A_J_m2": vv, "dW_graphite_minus_graphene_J_m2": (w8 - vv) if (w8 is not None and vv is not None) else None}
        wii = (g.get("V2_top_fcc") or {}).get("G3", {}).get("W_ii_J_m2")
        v2["top_fcc_10A"] = {"W_P1b_10A_J_m2": a, "W_V2_10A_J_m2": wii, "dW_J_m2": (a - wii) if (a is not None and wii is not None) else None}
        v2["⚠"] = ("같은 옆 셀·같은 QE·같은 제약 — 다른 것은 탄소 두께(1 → 3층) · 셀 c(영상 간격 V2 9 Å · 여기 ≥ 10 Å)·기계. "
                   "V2 의 bridge ≡ top_fcc · top_hcp ≡ hollow_fcc (대칭 동치) 라 V2 는 registry 둘이다.")
    out = {"schema": "agc_graphite_collect/v1", "stage1": stage1_dir, "stage2": stage2_dir, "raw1": raw1, "raw2": raw2, "fallback_raw": fallback_raw,
           "prereg": PREREG, "rows": rows, "headline": head, "labels": labels,
           "gates": {"G0_relax": man2["status"], "G1_machine": g1, "G3": (rows.get(REP_NAME) or {}).get("G3", {}).get("status"),
                     "G4": (rows.get(REP_NAME) or {}).get("G4", {}).get("status"), "thickness": thick},
           "info": {"vs_V2": v2}, "jobs_not_ok": sorted(j for j, v in J.items() if v.get("status") != "OK"),
           "substituted": sorted(j for j, v in J.items() if v.get("substituted_for"))}
    if atm:
        at = CC.atm_column(stage2_dir, [n for n in rows if rows[n].get("status") == "OK"])
        out["info"]["ATM"] = at
        if "rows" in at:
            d = [at["rows"][n]["dW_ATM_J_m2"] for n in n3 if at["rows"].get(n)]
            out["headline"]["ATM_column_mean_dW_J_m2"] = (sum(d) / len(d)) if d else None
    return out


def _print(o):
    f = lambda x, p=4: (f"{x:.{p}f}" if isinstance(x, (int, float)) else "—")
    print(f"{'model':22s} {'d0':>6s} {'W':>8s} {'W_Eint':>8s} {'W_PBE':>8s} {'ΔD3':>7s} {'meV/C':>7s}")
    for n, r in o["rows"].items():
        if "d0_A" not in r:
            print(f"{n:22s} {r.get('status')} {r.get('flags')}"); continue
        print(f"{n:22s} {r['d0_A']:6.3f} {f(r['W_PBE_D3_J_m2']):>8s} {f(r['W_PBE_D3_Eint_J_m2']):>8s} {f(r['W_PBE_J_m2']):>8s} {f(r['dD3_QE_J_m2']):>7s} {f(r['W_meV_per_C_contact'], 1):>7s}")
    g = o["gates"]
    print(f"G1 기계 대조 {g['G1_machine']['status']} (ΔW {f(g['G1_machine']['dW_J_m2'], 5)}) · G3 {g['G3']} · G4 {g['G4']} · 두께 {g['thickness']['status']} · 헤드라인 {o['headline']['status']}")
    print(f"미완 잡 {o['jobs_not_ok']} · 대체 {o['substituted']}")


# ─────────────────────────────── selftest ───────────────────────────────
def _fake_relax_out(path, at, dz=None, dxy=None, fail=False):
    """합성 relax 출력 — dz/dxy = {인덱스: 값}. 원자 기호는 at 그대로."""
    x = at.get_positions().copy()
    for i, v in (dz or {}).items():
        x[i, 2] += v
    for i, v in (dxy or {}).items():
        x[i, 0] += v
    L = ["     Program PWSCF v.7.4.1 starts", f"     number of atoms/cell      =           {len(at)}", "     convergence has been achieved in  10 iterations",
         "!    total energy              =   -900.00000000 Ry", "     DFT-D3 Dispersion         =   -0.05000000 Ry",
         ("     bfgs failed after 200 scf cycles and 199 bfgs steps, convergence not achieved" if fail else "     bfgs converged in   6 scf cycles and   5 bfgs steps"),
         "Begin final coordinates", "", "ATOMIC_POSITIONS (angstrom)"]
    L += [f"{s:2s} {p[0]:16.10f} {p[1]:16.10f} {p[2]:16.10f}" for s, p in zip(at.get_chemical_symbols(), x)]
    L += ["End final coordinates", "     convergence has been achieved in   8 iterations", "!    total energy              =   -900.00100000 Ry",
          "     DFT-D3 Dispersion         =   -0.05000000 Ry", "   JOB DONE."]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write("\n".join(L) + "\n")


def _w_to_dry(W, A):
    return W * A * A2_M2 / C4.RY_J


def _selftest():
    import re
    import tempfile
    from ase.io import read
    n_ok = n_bad = 0
    TOL = 1e-6

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {info}")
    # ① 빌더 — N3 registry 넷 · N4
    built = {}
    for n_c, reg in _models_stage1():
        name, b, f, is_c, m = build_model(n_c, reg)
        built[name] = (b, f, is_c, m)
        em = m["endpoints"]
        ck(f"{name}: Ag 12 · C {8 * n_c} · 변형 +1.078 % · 고정 6 · 측방 {8 * n_c} · 블록 안 AB · 깃발 0",
           m["n_Ag"] == 12 and m["n_C"] == 8 * n_c and abs(m["graphite_strain_pct"] - 1.078) < 0.01 and len(m["fixed_idx"]) == 6
           and len(m["lateral_fixed_idx"]) == 8 * n_c and set(m["carbon"]["internal"]) == {"AB"} and not m["interface_check_flags"], m["carbon"])
        ck(f"{name}: far 직접·영상 ≥ 10 · 쌍극자 여유 ≥ 4/4", em["far_gap_direct_image_A"][0] >= GAP - 1e-6 and em["far_gap_direct_image_A"][1] >= GAP - 1e-6
           and em["dipfield"]["clearance_A"]["to_top_atom"] >= 4 - 1e-6 and em["dipfield"]["clearance_A"]["to_substrate_bottom_image"] >= 4 - 1e-6, em)
    b, f, is_c, m = built[REP_NAME]
    L = [l for l in CC.layers(b[np.where(is_c)[0]])]
    ck("ABA: 1층과 3층이 같은 xy (Bernal)", np.allclose(np.sort(b[np.where(is_c)[0]].get_positions()[L[0], :2], axis=0),
                                             np.sort(b[np.where(is_c)[0]].get_positions()[L[2], :2], axis=0)))
    ck("V2 와 같은 옆 셀 · 같은 접촉층 C 좌표 (N3 top_fcc 의 1층 = V2 top_fcc 의 그래핀 · z 제외)",
       np.allclose(np.sort(b.get_positions()[np.where(is_c)[0][:8], :2], axis=0), np.sort(B.build_v2()["top_fcc"]["bound"].get_positions()[12:, :2], axis=0), atol=1e-8))
    # ② 적층 판정 — 좌표가 설계값을 되풀이하지 않는다
    ci = np.where(is_c)[0]; Lg = [[int(ci[i]) for i in l] for l in L]
    a_prim = float(np.linalg.norm(b.cell.array[0])) / 2.0
    lab = {}
    for k, fr in (("aa", -1.0), ("half", 0.5), ("ab2", 1.0)):
        bb = b.copy(); y = bb.get_positions(); y[Lg[1], :2] += fr * (b.cell.array[0, :2] + b.cell.array[1, :2]) / 6.0; bb.set_positions(y)
        lab[k] = stacking_2x2(bb, Lg[0], Lg[1], a_prim)
    ck("적층 판정: 2층을 −(⅙,⅙) 옮기면 AA · +½(⅙,⅙) 는 other · +(⅙,⅙) 더 (= ⅓,⅓ 셀분수 → 원시 (⅔,⅔)) 는 AB (반대 Bernal)",
       lab == {"aa": "AA", "half": "other", "ab2": "AB"}, lab)
    old = _assemble.__defaults__
    try:
        _assemble.__defaults__ = old[:-1] + (0.0,)          # bern_sign 0 → AA 블록
        build_model(N_C, REP); bad = False
    except SlabError as ex:
        bad = "설계(ABA)와 다르다" in str(ex)
    finally:
        _assemble.__defaults__ = old
    ck("⛔음성 빌더: 블록 안 적층이 AB 가 아니면 거부 (bern 0 → AA)", bad)
    try:
        _assemble(N_C, 0.0, 0.0, a_c=2.35); bad = False
    except SlabError:
        bad = True
    ck("⛔음성: 흑연 격자 2.35 Å → 변형률 > 3 % → 거부 (결정 7 재개 규칙)", bad)
    try:
        build_model(N_C, "bridge"); bad = False
    except SlabError:
        bad = True
    ck("⛔음성: 카드에 없는 registry 이름 → 거부", bad)
    # ③ registry 대칭 — 카드 넷은 비등가 · V2 의 등가 쌍은 잡힌다
    ck("카드 registry 넷 (N3): 쌍별 비등가", registry_equivalences(N_C, REGISTRIES) == [], registry_equivalences(N_C, REGISTRIES))
    eqv2 = registry_equivalences(1, {"top_fcc": (0.0, 0.0), "top_hcp": (1 / 3, 2 / 3), "bridge": (0.5, 0.0), "hollow_fcc": (2 / 3, 1 / 3)})
    ck("⛔음성 V2 (그래핀 1층): bridge ≡ top_fcc · top_hcp ≡ hollow_fcc 를 잡는다 (V2 W 16 자리 같음과 일치)",
       sorted(map(sorted, eqv2)) == [["bridge", "top_fcc"], ["hollow_fcc", "top_hcp"]], eqv2)
    ck("흑연 3층에서는 top_hcp ≠ hollow_fcc (2층이 거울을 깬다)", registry_equivalences(N_C, {"top_hcp": (1 / 3, 2 / 3), "hollow_fcc": (2 / 3, 1 / 3)}) == [])
    RG = dict(REGISTRIES)
    try:
        REGISTRIES["bridge"] = (0.5, 0.0)
        with tempfile.TemporaryDirectory() as T:
            stage1(T, date="2026-10-02"); bad = False
    except SlabError as ex:
        bad = "등가" in str(ex)
    finally:
        REGISTRIES.clear(); REGISTRIES.update(RG)
    ck("⛔음성 1단계: 등가 registry(bridge ≡ top_fcc)가 섞이면 만들지 않는다", bad)
    with tempfile.TemporaryDirectory() as T:
        s1 = os.path.join(T, "s1")
        m1 = stage1(s1, date="2026-10-02")
        m1b = stage1(os.path.join(T, "s1b"), date="2026-10-02", check_registry=False)
        ck("1단계: 모델 5 · 잡 7 (대조 2 → 이완 5 순서) · 결정성 (두 번 빌드 sha 같음)",
           len(m1["models"]) == 5 and [j["kind"] for j in m1["jobs"]] == ["ctrl", "ctrl"] + ["relax"] * 5
           and [j["pw_in_sha256"] for j in m1["jobs"]] == [j["pw_in_sha256"] for j in m1b["jobs"]] and m1["structures_sha256"] == m1b["structures_sha256"])
        src = os.path.join(REPO, CTRL_SRC, "qe", CTRL_JOBS[0], "pw.in")
        ck("기계 대조 입력 = V2 2단계 입력 바이트 그대로", _sha(os.path.join(s1, "qe", f"CTRL_{CTRL_JOBS[0]}", "pw.in")) == _sha(src))
        r = open(os.path.join(s1, "qe", f"{REP_NAME}_relax", "pw.in")).read()
        ck("이완 입력 N3: '0 0 0' 6 · '0 0 1' 24 · '1 1 1' 6 · relax · k 6 6 1 · mv 0.01 · D3 2체 · 쌍극자 · 52/520",
           r.count("  0 0 0") == 6 and r.count("  0 0 1") == 24 and r.count("  1 1 1") == 6 and "calculation = 'relax'" in r and "  6 6 1 0 0 0" in r
           and "smearing = 'mv'" in r and "degauss = 0.01\n" in r and "dftd3_threebody = .false." in r and "dipfield = .true." in r and "ecutwfc = 52.0" in r)
        keys = ("ecutwfc", "ecutrho", "occupations", "smearing", "degauss", "nspin", "vdw_corr", "dftd3_version", "dftd3_threebody", "conv_thr", "mixing_beta",
                "mixing_mode", "electron_maxstep", "tefield", "dipfield", "edir", "eamp", "disk_io", "tprnfor", "ibrav")
        kv = lambda t: {k: v.strip() for k, v in re.findall(r"^\s*(\w+)\s*=\s*(.+)$", t, re.M) if k in keys}
        mine = B3.qe_input(read(os.path.join(s1, "structures", f"{REP_NAME}_init_bound.extxyz")), "x", KPTS, "/p", dip=_dd(m1["models"][REP_NAME]["endpoints"]["dipfield"]))
        ck("V2 와 같은 설정: 20 키 전부 같은 값 (V2_top_fcc_dft_bound 와)", kv(open(src).read()) == kv(mine) and len(kv(mine)) == len(keys))
        jj = json.load(open(os.path.join(s1, "qe", "jobs.json"), encoding="utf-8"))
        ck("jobs.json: 러너 형식 · PP 해시 Ag·C · 디스크 sha = 기록", all({"dir", "calc", "kind", "pw_in_sha256"} <= set(j) for j in jj["jobs"])
           and jj["settings"]["pp_sha256"] == {B3.PP[e][1]: B3.PP_SHA[B3.PP[e][1]] for e in PP_EL}
           and all(_sha(os.path.join(s1, "qe", j["dir"], "pw.in")) == j["pw_in_sha256"] for j in jj["jobs"]))
        # ④ 2단계 — 합성 이완 (C 블록 z +0.02 · Ag 위층 그대로)
        raw1 = os.path.join(T, "run1")
        for name, mm in m1["models"].items():
            init = read(os.path.join(s1, "structures", f"{name}_init_bound.extxyz"))
            _fake_relax_out(os.path.join(raw1, f"{name}_relax", "pw.out"), init, dz={i: 0.02 for i in np.where(mm["c_mask"])[0]})
        s2 = os.path.join(T, "s2")
        m2 = stage2(s1, raw1, s2, date="2026-10-02")
        n_rep = 2 + 1 + len(ED_SHIFTS) + len(ED_EXTRA) + 3 + 6
        ck(f"2단계: OK 5 · 잡 = N3 3 × 3 + 대표 {n_rep} + N4 2 = {9 + n_rep + 2} · 대체 잡 같은 수 (β 0.1 · substitutes)",
           m2["n_ok"] == 5 and len(m2["jobs"]) == 9 + n_rep + 2 and len(m2["fallback_jobs"]) == len(m2["jobs"])
           and all(j["tags"].get("substitutes") == j["dir"][:-4] and j["mixing_beta"] == BETA_FALLBACK for j in m2["fallback_jobs"]), (len(m2["jobs"]), m2["status"]))
        fb = open(os.path.join(s2, "fallback", "qe", f"{REP_NAME}_dft_bound_b01", "pw.in")).read()
        pr = open(os.path.join(s2, "qe", f"{REP_NAME}_dft_bound", "pw.in")).read()
        ck("대체 잡 = 원 잡과 β 한 줄만 다르다", [l for l in fb.splitlines() if l not in pr.splitlines()] == ["  mixing_beta = 0.1", "  prefix = '" + f"{REP_NAME}_dft_bound_b01" + "'"]
           or sorted(set(fb.splitlines()) ^ set(pr.splitlines())) == sorted(["  mixing_beta = 0.1", "  mixing_beta = 0.3", f"  prefix = '{REP_NAME}_dft_bound_b01'", f"  prefix = '{REP_NAME}_dft_bound'"]))
        s05 = open(os.path.join(s2, "qe", f"{REP_NAME}_G4_s05_far", "pw.in")).read(); k9 = open(os.path.join(s2, "qe", f"{REP_NAME}_G4_k9_far", "pw.in")).read()
        ck("G4: s05 = degauss 0.005 · k9 = 9 9 1 · e70 = 70/700", "degauss = 0.005\n" in s05 and "  9 9 1 0 0 0" in k9
           and "ecutwfc = 70.0" in open(os.path.join(s2, "qe", f"{REP_NAME}_G4_e70_far", "pw.in")).read())
        bb = read(os.path.join(s2, "structures", f"{REP_NAME}_dft_bound.extxyz")); ff = read(os.path.join(s2, "structures", f"{REP_NAME}_dft_far.extxyz"))
        icm = np.array(m1["models"][REP_NAME]["c_mask"])
        ck("끝점: far = C 블록만 +z (직접 10 Å) · Ag 그대로", abs(float(ff.get_positions()[icm, 2].min() - ff.get_positions()[~icm, 2].max()) - GAP) < 1e-6
           and np.allclose(bb.get_positions()[~icm], ff.get_positions()[~icm]))
        m2b = stage2(s1, raw1, os.path.join(T, "s2b"), date="2026-10-02")
        ck("2단계 결정성 (두 번 sha 같음 · 대체 포함)", [j["pw_in_sha256"] for j in m2["jobs"] + m2["fallback_jobs"]] == [j["pw_in_sha256"] for j in m2b["jobs"] + m2b["fallback_jobs"]])
        ck("verify_stage2: 같은 이완 출력이면 pass", verify_stage2(s1, raw1, s2)["pass"])
        p = os.path.join(s2, "qe", f"{REP_NAME}_dft_far", "pw.in"); t = open(p).read(); open(p, "w").write(t.replace("conv_thr = 1.0d-8", "conv_thr = 1.0d-6"))
        v = verify_stage2(s1, raw1, s2)
        ck("⛔음성 verify: 디스크 pw.in 을 고치면 잡힌다", not v["pass"] and f"{REP_NAME}_dft_far" in v["jobs"]["disk_vs_manifest_mismatch"], v["jobs"])
        open(p, "w").write(t)
        # 음성 — 제약 위반 · 이완 실패 · 층간 깃발
        raw_bad = os.path.join(T, "run_bad"); shutil.copytree(raw1, raw_bad)
        init = read(os.path.join(s1, "structures", f"{REP_NAME}_init_bound.extxyz"))
        _fake_relax_out(os.path.join(raw_bad, f"{REP_NAME}_relax", "pw.out"), init, dxy={int(np.where(icm)[0][0]): 0.01})
        try:
            stage2(s1, raw_bad, os.path.join(T, "s2x")); bad = False
        except SlabError as ex:
            bad = "제약 위반" in str(ex)
        ck("⛔음성 2단계: C 면내 이동 (제약 위반) → 거부", bad)
        _fake_relax_out(os.path.join(raw_bad, f"{REP_NAME}_relax", "pw.out"), init, fail=True)
        mx = stage2(s1, raw_bad, os.path.join(T, "s2y"))
        ck("⛔음성 2단계: 이완 실패(bfgs failed) → 그 모델 INCOMPLETE (세고 제외) · 나머지 OK", mx["status"][REP_NAME] == "INCOMPLETE" and mx["n_ok"] == 4, mx["status"])
        Lc = carbon_report(init, icm)["layers"]
        _fake_relax_out(os.path.join(raw_bad, f"{REP_NAME}_relax", "pw.out"), init, dz={i: 1.2 for i in Lc[2]})
        mx = stage2(s1, raw_bad, os.path.join(T, "s2z"))
        ck("⛔음성 2단계: 흑연 층간 4.55 Å (밖) → INCOMPLETE 깃발", mx["status"][REP_NAME] == "INCOMPLETE" and any("층간" in fl for fl in mx["models"][REP_NAME]["flags"]), mx["models"][REP_NAME].get("flags"))
        # ⑤ 집계 — 합성 SCF 출력
        raw2 = os.path.join(T, "run2"); fbr = os.path.join(T, "run2fb")
        Wd = {model_name(N_C, "top_fcc"): 0.47, model_name(N_C, "top_hcp"): 0.46, model_name(N_C, "hollow_fcc"): 0.465, model_name(N_C, "s01"): 0.468, THICK_NAME: 0.485}
        for j in m2["jobs"]:
            nm = j["model"]; A = C4.area_A2(os.path.join(s2, "structures", f"{nm}_dft_bound.extxyz"))
            base = -2000.0
            if j["dir"].endswith("_dft_far"):
                F = base + _w_to_dry(Wd[nm], A)
            elif j["dir"].endswith("_far8"):
                F = base + _w_to_dry(Wd[nm] - 0.012, A)
            elif "_Ed_" in j["dir"]:
                s = float(j["tags"]["E(d)"][2:]); F = base + _w_to_dry(Wd[nm] * min(1.0, abs(s) / 6.7), A)
            elif "G3_c2_bound" in j["dir"]:
                F = base
            elif "G3_c2_far_i" in j["dir"] and not j["dir"].endswith("_ii"):
                F = base + _w_to_dry(Wd[nm] + 0.004, A)
            elif "G3_c2_far_ii" in j["dir"]:
                F = base + _w_to_dry(Wd[nm] + 0.015, A)               # G3 (ii) FAIL 로 설계
            elif "_G4_" in j["dir"]:
                F = base + (_w_to_dry(Wd[nm] + 0.003, A) if j["dir"].endswith("_far") else 0.0)
            else:
                F = base
            if j["dir"] == f"{REP_NAME}_G4_k9_far":
                continue                                               # 원 잡 없음 → 대체 잡으로
            d = os.path.join(raw2, j["dir"]); os.makedirs(d)
            shutil.copy(os.path.join(s2, "qe", j["dir"], "pw.in"), os.path.join(d, "pw.in"))
            C4._fake_out(os.path.join(d, "pw.out"), F, -0.1, nat=j["nat"])
        d = os.path.join(fbr, f"{REP_NAME}_G4_k9_far_b01"); os.makedirs(d)
        shutil.copy(os.path.join(s2, "fallback", "qe", f"{REP_NAME}_G4_k9_far_b01", "pw.in"), os.path.join(d, "pw.in"))
        A_rep = C4.area_A2(os.path.join(s2, "structures", f"{REP_NAME}_dft_bound.extxyz"))
        C4._fake_out(os.path.join(d, "pw.out"), -2000.0 + _w_to_dry(Wd[REP_NAME] + 0.003, A_rep), -0.1, nat=44 - 8)
        # 기계 대조 — V100 W 와 +0.001 (PASS)
        ref = json.load(open(os.path.join(REPO, CTRL_REF[0]), encoding="utf-8"))["registries"][CTRL_REF[1]]["W_PBE_D3_J_m2"]
        Ac = C4.area_A2(os.path.join(REPO, CTRL_SRC, "structures", f"{CTRL_JOBS[0]}.extxyz"))
        for j, F in ((CTRL_JOBS[0], -1500.0), (CTRL_JOBS[1], -1500.0 + _w_to_dry(ref + 0.001, Ac))):
            d = os.path.join(raw1, f"CTRL_{j}"); os.makedirs(d, exist_ok=True)
            shutil.copy(os.path.join(s1, "qe", f"CTRL_{j}", "pw.in"), os.path.join(d, "pw.in"))
            C4._fake_out(os.path.join(d, "pw.out"), F, -0.1, nat=20)
        o = collect(s1, s2, raw1, raw2, fallback_raw=fbr)
        rr = o["rows"]
        ck("집계: W 설계값 재현 (N3 넷 · N4)", all(abs(rr[n]["W_PBE_D3_J_m2"] - w) < TOL for n, w in Wd.items()), {n: rr[n].get("W_PBE_D3_J_m2") for n in Wd})
        ck("헤드라인: N3 평균 · [min, max] · n 4 · OK", abs(o["headline"]["mean_J_m2"] - (0.47 + 0.46 + 0.465 + 0.468) / 4) < TOL
           and o["headline"]["range_J_m2"] == [rr[model_name(N_C, "top_hcp")]["W_PBE_D3_J_m2"], rr[REP_NAME]["W_PBE_D3_J_m2"]] and o["headline"]["n_ok"] == 4 and o["headline"]["status"] == "OK", o["headline"])
        ck("G1 기계 대조 +0.001 → PASS", o["gates"]["G1_machine"]["status"] == "PASS" and abs(o["gates"]["G1_machine"]["dW_J_m2"] - 0.001) < TOL, o["gates"]["G1_machine"])
        ck("G3: (i) +0.004 PASS 쪽 · (ii) +0.015 → FAIL · 라벨에 'G3 FAIL'", o["gates"]["G3"] == "FAIL" and "G3 FAIL" in o["labels"], (o["gates"]["G3"], o["labels"]))
        ck("G4: 원 k9_far 없음 → β 0.1 대체로 채움 · 기록 · +0.003 PASS", o["gates"]["G4"] == "PASS" and f"{REP_NAME}_G4_k9_far" in o["substituted"]
           and rr[REP_NAME]["G4"]["k9"]["substituted"] == [f"{REP_NAME}_G4_k9_far"], (o["gates"]["G4"], o["substituted"]))
        ck("두께: N4 − N3 = +0.015 ≤ 0.02 → PASS", o["gates"]["thickness"]["status"] == "PASS" and abs(o["gates"]["thickness"]["dW_J_m2"] - 0.015) < TOL)
        ck("far8 정보: 10 − 8 Å = +0.012 · V2 대비 칸 있음", abs(rr[REP_NAME]["far8_info"]["dW_8to10_J_m2"] - 0.012) < TOL and "top_fcc" in o["info"]["vs_V2"]
           and o["info"]["vs_V2"]["top_fcc"]["W_V2_8A_J_m2"] is not None)
        cur = rr[REP_NAME]["E_d_curve_info"]
        ck("E(d): 국소 최소 (±0.3 둘 다 양수) · 점 10 (d₀ + 8 + far) · 견인력 9 · 최대값 있음",
           rr[REP_NAME]["E_d_local_min_in_grid"] is True and len(cur["points_d_A_dE_meV"]) == 10 and len(cur["traction"]) == 9 and cur["max_traction_info"] is not None, cur)
        o2 = collect(s1, s2, raw1, raw2, fallback_raw=None)
        ck("⛔음성 집계: 대체 RUN 을 안 주면 k9 는 INCOMPLETE (0 으로 안 채운다) · G4 INCOMPLETE", o2["gates"]["G4"] == "INCOMPLETE"
           and o2["rows"][REP_NAME]["G4"]["k9"]["W_J_m2"] is None and "G4 INCOMPLETE" in o2["labels"], o2["gates"]["G4"])
        shutil.rmtree(os.path.join(raw2, f"{THICK_NAME}_dft_far"))
        o3 = collect(s1, s2, raw1, raw2, fallback_raw=fbr)
        ck("⛔음성 집계: N4 far 없음 → 두께 INCOMPLETE (W None · 0 아님)", o3["gates"]["thickness"]["status"] == "INCOMPLETE" and o3["rows"][THICK_NAME]["W_PBE_D3_J_m2"] is None)
        C4._fake_out(os.path.join(raw1, f"CTRL_{CTRL_JOBS[1]}", "pw.out"), -1500.0 + _w_to_dry(ref + 0.003, Ac), -0.1, nat=20)
        o4 = collect(s1, s2, raw1, raw2, fallback_raw=fbr)
        ck("⛔음성 G1: +0.003 > 0.002 → FAIL · 헤드라인 HELD", o4["gates"]["G1_machine"]["status"] == "FAIL" and o4["headline"]["status"].startswith("HELD"), o4["headline"]["status"])
    # ⑥ 카드 결속
    p = os.path.join(REPO, PREREG)
    if os.path.isfile(p):
        cb = json.load(open(p, encoding="utf-8"))["code_binding"]
        mine = {"REGISTRIES": {k: [round(v[0], 12), round(v[1], 12)] for k, v in REGISTRIES.items()}, "REP": REP, "N_C": N_C, "N_C_THICK": N_C_THICK, "N_AG": N_AG,
                "GAP": GAP, "KPTS": list(KPTS), "KPTS_G4": list(KPTS_G4), "ECUT": list(ECUT), "ECUT_HI": list(ECUT_HI), "DEGAUSS": [DEGAUSS, DEGAUSS_HALF],
                "BETA": [BETA, BETA_FALLBACK], "ED_SHIFTS": list(ED_SHIFTS), "ED_EXTRA": list(ED_EXTRA), "G1_DW": G1_DW, "G3_DW": G3_DW, "G4_DW": G4_DW,
                "THICK_DW": THICK_DW, "SPACING_OK": list(SPACING_OK), "D0_OK": list(D0_OK), "FLAT_TOL": FLAT_TOL}
        theirs = {k: cb.get(k) for k in mine}
        if "REGISTRIES" in cb:
            theirs["REGISTRIES"] = {k: [round(v[0], 12), round(v[1], 12)] for k, v in cb["REGISTRIES"].items()}
        ck("카드 결속: code_binding 값 = 코드 상수 (전부)", mine == theirs, {k: (mine[k], theirs.get(k)) for k in mine if mine[k] != theirs.get(k)})
    else:
        ck("카드가 repo 에 있다", False, p)
    print(f"agc_graphite selftest: {n_ok} 통과 · {n_bad} 실패 " + ("✅" if n_bad == 0 else "❌"))
    return n_bad == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--registry_scan", action="store_true")
    ap.add_argument("--n_c", type=int, default=N_C)
    ap.add_argument("--stage1", action="store_true")
    ap.add_argument("--stage2", action="store_true")
    ap.add_argument("--verify_stage2", default=None)
    ap.add_argument("--collect", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--stage1_dir", default=None)
    ap.add_argument("--stage2_dir", default=None)
    ap.add_argument("--relax_raw", default=None)
    ap.add_argument("--raw1", default=None)
    ap.add_argument("--raw2", default=None)
    ap.add_argument("--fallback_raw", default=None)
    ap.add_argument("--atm", action="store_true")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.registry_scan:
        cl = registry_scan(a.n_c)
        print(f"N_C={a.n_c}: 대칭 동치류 {len(cl)} 개 (V2 이름 넷 + 1/6 격자 36 점)")
        for c in cl:
            print(f"  {c['rep']:11s} {str([round(v, 4) for v in c['shift']]):18s} ← {c['members']}")
        return
    if a.stage1:
        m = stage1(a.out, a.pseudo_dir)
        print(f"1단계: 모델 {len(m['models'])} · 잡 {len(m['jobs'])} → {a.out}/qe/jobs.json · registry 등가 쌍 {m['registry_check']['pairs_equivalent']}")
        return
    if a.stage2:
        m = stage2(a.stage1_dir, a.relax_raw, a.out, a.pseudo_dir)
        print(f"2단계: OK {m['n_ok']} · INCOMPLETE {m['n_incomplete']} · 잡 {len(m['jobs'])} (+ 대체 {len(m['fallback_jobs'])}) → {a.out}/qe/jobs.json")
        for n, s in m["status"].items():
            if s != "OK":
                print(f"  {n}: {s} {m['models'][n].get('flags')}")
        return
    if a.verify_stage2:
        r = verify_stage2(a.stage1_dir, a.relax_raw, a.verify_stage2)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        sys.exit(0 if r["pass"] else 1)
    if a.collect:
        o = collect(a.stage1_dir, a.stage2_dir, a.raw1, a.raw2, a.fallback_raw, a.atm)
        _print(o)
        if a.out:
            json.dump(o, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
            print(f"→ {a.out}")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
