#!/usr/bin/env python3
"""build_round2_vasp_package.py — W_ad 외주 2차 VASP 묶음 (탄소 P2′ · C–C · 은 a4) · 러너 재시도 사다리 · 반송 검사 · 집계.

    python3 tools/wad/build_round2_vasp_package.py --selftest
    python3 tools/wad/build_round2_vasp_package.py --build --seal <P2′ 봉인 폴더> --out <묶음 폴더>
    python3 tools/wad/build_round2_vasp_package.py --check --out <묶음> --ret <반송 run 폴더> --manifest_sha256 <고정값>

근거: 카드 db/properties/wad_p2small_vasp_card_2026_10_15.json (D-2026-10-15-wad-p2small-vasp-card · 선택 2 + 80 % 발동 규칙 ·
  단계 누적 상한 1.5 배 · 전자 스텝 ≥ 1 뒤 충돌 = 실행 실패) · 개정 4 db/properties/wad_aprime_pilot_prereg_v5_amendment_4_e70_rerun_2026_10_15.json
  (D-2026-10-15-wad-aprime-v5-e70-a4-rerun · 은 a4 두 단계 · 러너·검사기 공통 SCF 판정 계약).

왜 새 파일인가: build_v5_vasp_package.py 는 V5 반송 재검사·재집계가 저장본과 바이트 일치로 묶여 있고 (4050264) 상수·러너가
  V5 18 잡에 맞춰져 있다. 여기서는 그 파서·검사 함수 (parse_outcar · oszicar_last · parse_incar_strict · dipol_z · check_dip_clear ·
  d3_ref_eV · pack 절차) 를 **가져다 쓰고** 탄소 잡 행렬 · 재시도 사다리 · 단계 상한 · 탄소 검사·집계만 더한다.
  은 a4 의 채택 (V5 G4 e70) 은 개정 4 대로 V5 검사기 쪽에서 한다 — 이 묶음은 a4 입력을 만들고 돌릴 뿐이다.

⛔ 이 도구가 못 하는 것: VASP 를 돌리지 않는다 · 구조를 만들지 않는다 (P2′ 봉인 · WAD-CC 봉인 · V5 묶음의 sha 로 결박만) ·
   러너의 SCF 판정은 OSZICAR·OUTCAR 기록만 본다 (전자밀도 · 해의 유일성은 모른다) · WAVECAR 읽기 확인 문구는 파일럿 원문으로 확정한다
   (그 전에는 ISTART·ICHARG 되울림 + 'WAVECAR not read' 부재 + ⓑ 원본·복사본·끝 sha = 그 ⓐ 의 기록 WAVECAR sha 로만 본다 ·
   문구 regex 는 파일럿에서 읽은 ⓑ 전부에 맞고 새로 시작한 시도에 안 맞고 grep -E 와 python 이 시도마다 같은 답일 때만 봉인한다 —
   파일럿에 없던 출력 꼴 (다른 노드 · 다른 실패 경로 · 로캘) 에서도 두 엔진이 같은 답이라는 보증은 없다) · optB88 설정 되울림 줄 형식도 파일럿으로 확정한다 ·
   vdW 커널 읽기 문구 (kernel_read_regex) 를 봉인하기 전에는 optB88 수렴 시도도 KERNEL_UNVERIFIED 다 · 커널 부재·재생성 표지는 넓은 낱말 목록이라
   5.4.4 실물 긍정 문구에 걸리면 거짓 경보다 (파일럿 원문으로 다시 정한다).
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_v5_vasp_package as V   # noqa: E402

PkgError = V.PkgError
_sha, _sha_text, _write, fin = V._sha, V._sha_text, V._write, V.fin
REPO = os.path.dirname(os.path.dirname(HERE))

CARD = "db/properties/wad_p2small_vasp_card_2026_10_15.json"
AMEND4 = "db/properties/wad_aprime_pilot_prereg_v5_amendment_4_e70_rerun_2026_10_15.json"
DECISIONS = ("D-2026-10-15-wad-p2small-vasp-card", "D-2026-10-15-wad-aprime-v5-e70-a4-rerun")
SPECIES_ORDER = ("Li", "P", "S", "Cl", "Ag", "C")
POTCAR_MAP = {**V.POTCAR_MAP, "C": "C"}
PP_EXPECTED_TITEL = {**V.PP_EXPECTED_TITEL, "C": "PAW_PBE C 08Apr2002"}   # 카드: 업체 보유본으로 확인 · 파일럿 뒤 탄소 등록부 봉인
ZVAL = {**V.ZVAL, "C": 4.0}
ENCUT, ENCUT_G4 = 520.0, 650.0
SIGMA_C, SIGMA_C_HALF = 0.05, 0.025                  # 카드 §3 탄소 점유 규약 — Gaussian ISMEAR 0 (은 쪽 MP1 0.136 은 소급하지 않는다)
K_BASE, K_DENSE, K_CC = (3, 2, 1), (6, 2, 1), (18, 18, 1)
EDIFF = 1e-6
NELM_RUNG = {"0": 200, "r1A": 200, "r1B": 300, "r2B": 300, "a4A": 200, "a4B": 300}
OPTB88 = (("GGA", "BO"), ("PARAM1", "0.1833333333"), ("PARAM2", "0.22"), ("AGGAC", "0.0"), ("LUSE_VDW", ".TRUE."),
          ("ZAB_VDW", "-0.8491"), ("IVDW", "0"))      # 카드 §2 ② (VASP 5.4.4 · IVDW_NL 없음 · D3 줄은 뺀다)
D3_TAGS = ("IVDW", "VDW_S6", "VDW_S8", "VDW_A1", "VDW_A2", "VDW_RADIUS", "VDW_CNRADIUS")
#: 사다리 단마다 기본 INCAR (단 0) 에 대한 **의미상 차이** — 빌더가 만든 뒤 parse_incar_strict 로 다시 대조한다 (그 밖의 차이 = 빌드 실패)
RUNG_DIFF = {"r1A": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE."},
             "r1B": {"ISTART": "1", "ICHARG": "0", "AMIN": "0.01", "NELM": "300"},
             "r2B": {"ISTART": "1", "ICHARG": "0", "AMIX": "0.1", "BMIX": "0.01", "AMIN": "0.01", "NELM": "300"},
             "a4A": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE."},
             "a4B": {"ISTART": "1", "ICHARG": "0", "AMIN": "0.01", "NELM": "300"}}
#: 단계표 (카드 §4c · 선택 2) — 기대 = 장부 기반 노드-시간 · 상한 = 1.5 배 (24 h 미만 단계는 24 h) · 전체 상한 = 기대 합 720 × 1.5
STAGE_EXPECT_H = {"P": 78.0, "1": 113.0, "2": 391.0, "3": 136.0, "4": 2.0}
STAGE_CAP_H = {k: max(24.0, round(1.5 * v)) for k, v in STAGE_EXPECT_H.items()}
TOTAL_CAP_H = 1.5 * sum(STAGE_EXPECT_H.values())
A4_JOB = "V5_s_outer_A_G4_e70_far_a4"
A4_SRC = "V5_s_outer_A_G4_e70_far"
V5_PKG = "db/inputs/wad_aprime_v5_vasp_2026_09_27"
V5_MANIFEST_SHA256 = "8118bbc023d6699cd7cd1b6e6afd32872e0699af70b412e15b89365e556ee2f1"
WADCC_PKG = "db/raw/wad_cc_graphite_2026_09_28/stage2_pkg"
CC_PAIR = ("CC_S33_AB_dft_bound", "CC_S33_AB_dft_far")
RETURN_ALLOWED = V.RETURN_ALLOWED + ("WAVECAR.info", "warn.log", "infra_abort.json")
RETURN_FORBIDDEN = V.RETURN_FORBIDDEN + ("vdw_kernel.bindat",)


# ───────────────────────── 입력 만들기 ─────────────────────────
def poscar_text(atoms, comment):
    """V.poscar_text 와 같은 꼴 — 종 순서에 C 를 더한다 (Li P S Cl Ag C)."""
    sym = atoms.get_chemical_symbols()
    unknown = sorted(set(sym) - set(SPECIES_ORDER))
    if unknown:
        raise PkgError(f"POSCAR: 모르는 원소 {unknown}")
    order = [i for sp in SPECIES_ORDER for i, s in enumerate(sym) if s == sp]
    present = [sp for sp in SPECIES_ORDER if sp in sym]
    c = atoms.cell.array; p = atoms.get_positions()
    L = [comment, "1.0"] + ["  " + " ".join(f"{x:16.10f}" for x in c[k]) for k in range(3)]
    L += ["  " + " ".join(present), "  " + " ".join(str(sym.count(sp)) for sp in present), "Cartesian"]
    L += ["  " + " ".join(f"{x:16.10f}" for x in p[i]) for i in order]
    return "\n".join(L) + "\n", order, present


def kpoints_text(k):
    return f"Gamma-centred mesh (W_ad round2)\n0\nGamma\n{k[0]} {k[1]} {k[2]}\n0 0 0\n"


def incar_base(job, encut, sigma, dz, method):
    """단 0 INCAR — V5 봉인 틀 그대로 + 탄소 점유 규약 (ISMEAR 0 · SIGMA) · optB88 이면 GGA = BO 와 vdW-DF 줄 (D3 줄 없음)."""
    if method not in ("pbed3", "optb88"):
        raise PkgError(f"모르는 방법 {method}")
    L = [f"SYSTEM = W_ad round2 {job} (single point)", "GGA = PE" if method == "pbed3" else "GGA = BO", "PREC = Accurate",
         f"ENCUT = {encut:.1f}", "EDIFF = 1E-6", f"NELM = {NELM_RUNG['0']}", "NELMIN = 6", "ALGO = Normal",
         "ISPIN = 1", "ISMEAR = 0", f"SIGMA = {sigma:.4f}", "LASPH = .TRUE.", "LREAL = .FALSE.", "ISYM = 0", "IBRION = -1", "NSW = 0"]
    if method == "pbed3":
        d = V.D3_PARAMS
        L += ["IVDW = 12", f"VDW_S6 = {d['s6']}", f"VDW_S8 = {d['s8']}", f"VDW_A1 = {d['a1']}", f"VDW_A2 = {d['a2']}",
              f"VDW_RADIUS = {V.VDW_RADIUS_A}", f"VDW_CNRADIUS = {V.VDW_CNRADIUS_A}"]
    else:
        L += [f"{k} = {v}" for k, v in OPTB88 if k != "GGA"]
    L += ["LDIPOL = .TRUE.", "IDIPOL = 3", f"DIPOL = 0.5 0.5 {dz:.6f}", "LWAVE = .FALSE.", "LCHARG = .FALSE."]
    return "\n".join(L) + "\n"


def rung_text(base, rung):
    """단 0 (또는 봉인 V5) INCAR 텍스트 → 사다리 단 INCAR. 있는 줄은 값만 바꾸고 없는 태그는 끝에 붙인다 (순서 결정적)."""
    want = RUNG_DIFF[rung]
    lines, seen = [], set()
    for ln in base.splitlines():
        k = ln.split("=", 1)[0].strip().upper() if "=" in ln else None
        if k in want:
            lines.append(f"{k} = {want[k]}"); seen.add(k)
        else:
            lines.append(ln)
    lines += [f"{k} = {v}" for k, v in want.items() if k not in seen]
    return "\n".join(lines) + "\n"


def semantic_diff(a_text, b_text):
    """두 INCAR 의 VASP 의미상 차이 {태그: (a, b)} — 문법 오류면 PkgError."""
    a, ea = V.parse_incar_strict(a_text)
    b, eb = V.parse_incar_strict(b_text)
    if ea or eb:
        raise PkgError(f"INCAR 문법 {ea or eb}")
    return {k: (a.get(k), b.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k) and k != "SYSTEM"}


def estimate(atoms, encut, kp):
    sym = atoms.get_chemical_symbols(); n = len(sym)
    nel = sum(ZVAL[s] for s in sym); nb = int(math.ceil(nel / 2 + n / 2))
    Vol = abs(float(atoms.get_volume())); kmax = math.sqrt(encut / V.HB2M)
    npw = Vol * kmax ** 3 / (6 * math.pi ** 2)
    nk_full = kp[0] * kp[1] * kp[2]; nk_irr = (nk_full + 1) // 2 + (1 if nk_full % 2 == 0 else 0)
    return {"NIONS": n, "NELECT": nel, "NBANDS_default": nb, "NPW_per_k": int(npw), "ENCUT_eV": encut, "nk_full": nk_full, "nk_irr_est": nk_irr,
            "wfc_only_GB_all_k": round(nb * npw * 16 * nk_irr / 1e9, 1), "⚠": "파동함수 몫 대략치 — peak RSS 아님 · 환원 k 는 IBZKPT 로 확인"}


def job_matrix():
    """카드 표본 계획 (선택 2) 의 잡 23 + 은 a4 1 = 24 — (이름, 단계, 종류, 방법, 구조 출처, 구조 이름, k, ENCUT, SIGMA, 사다리)."""
    J = []
    add = lambda *a: J.append(dict(zip(("dir", "stage", "kind", "method", "src", "structure", "kpts", "encut", "sigma", "ladder"), a)))
    for s, st in (("S_A_bound", "P"), ("S_A_far", "P"), ("Li_A_bound", "1"), ("Li_A_far", "1"), ("S_A_p05_bound", "1"), ("Li_A_p05_bound", "1")):
        add(f"P2S_{s}", st, "sample", "pbed3", "seal", s, K_BASE, ENCUT, SIGMA_C, "carbon")
    for s in ("S_A_G3_c2_bound", "S_A_G3_c2_far_i", "S_A_G3_c2_far_ii"):
        add(f"P2S_{s}", "2", "g3", "pbed3", "seal", s, K_BASE, ENCUT, SIGMA_C, "carbon")
    for tag, k, e, sg in (("k62", K_DENSE, ENCUT, SIGMA_C), ("k62s2", K_DENSE, ENCUT, SIGMA_C_HALF), ("e650", K_BASE, ENCUT_G4, SIGMA_C)):
        for ep in ("bound", "far"):
            add(f"P2S_S_A_G4_{tag}_{ep}", "2", "g4", "pbed3", "seal", f"S_A_{ep}", k, e, sg, "carbon")
    for t in ("S_A", "Li_A"):
        for ep in ("bound", "far"):
            add(f"P2S_{t}_optB88_{ep}", "3", "optb88", "optb88", "seal", f"{t}_{ep}", K_BASE, ENCUT, SIGMA_C, "carbon")
    for m, st in (("optB88", "P"), ("pbed3", "4")):
        for ep, cs in zip(("bound", "far"), CC_PAIR):
            add(f"CC_S33_AB_{m}_{ep}", st, "cc", "optb88" if m == "optB88" else "pbed3", "wadcc", cs, K_CC, ENCUT, SIGMA_C, "carbon")
    add(A4_JOB, "P", "a4", "v5", "v5", A4_SRC, (3, 2, 1), ENCUT_G4, V.SIGMA_BASE, "a4")
    return J


def _decision_state(did, ledger=None):
    d = json.load(open(ledger or os.path.join(REPO, "db", "governance", "decisions.json"), encoding="utf-8"))
    rows = [e for e in (d["decisions"] if isinstance(d, dict) else d) if e.get("id") == did]
    return rows[0].get("decision_state") if rows else None


def _manifest_lines(path):
    out = {}
    for ln in open(path, encoding="utf-8").read().splitlines():
        if ln.strip():
            h, p = ln.split("  ", 1)
            out[p] = h
    return out


def build(seal_dir, out, v5_pkg=None, wadcc_pkg=None, ledger=None):
    """봉인 구조 (P2′ 봉인 · WAD-CC stage2 · V5 묶음 sha) → 묶음 폴더. 구조를 새로 만들지 않는다 — sha 가 하나라도 다르면 만들지 않는다."""
    from ase.io import read
    for did in DECISIONS:
        st = _decision_state(did, ledger)
        if st != "active":
            raise PkgError(f"{did} 가 원장에서 active 가 아니다 ({st}) — 묶음을 만들지 않는다")
    v5_pkg = v5_pkg or os.path.join(REPO, V5_PKG)
    wadcc_pkg = wadcc_pkg or os.path.join(REPO, WADCC_PKG)
    smp = os.path.join(seal_dir, "p2s_seal_manifest.json")
    seal = json.load(open(smp, encoding="utf-8"))
    if seal.get("schema") != "p2s_seal/v1":
        raise PkgError(f"P2′ 봉인 schema {seal.get('schema')!r}")
    if _sha(os.path.join(v5_pkg, "MANIFEST.sha256")) != V5_MANIFEST_SHA256:
        raise PkgError("V5 묶음 MANIFEST sha 가 고정값과 다르다 — a4 입력을 만들지 않는다")
    v5man = _manifest_lines(os.path.join(v5_pkg, "MANIFEST.sha256"))
    v5jobs = {j["dir"]: j for j in json.load(open(os.path.join(v5_pkg, "jobs.json"), encoding="utf-8"))["jobs"]}
    ccm = json.load(open(os.path.join(wadcc_pkg, "cc_stage2_manifest.json"), encoding="utf-8"))
    ccj = {j["dir"]: j for j in ccm["jobs"]}
    dipset = {"S_A_bound": "S_A", "S_A_far": "S_A", "S_A_p05_bound": "S_A", "Li_A_bound": "Li_A", "Li_A_far": "Li_A", "Li_A_p05_bound": "Li_A",
              "S_A_G3_c2_bound": "S_A_G3", "S_A_G3_c2_far_i": "S_A_G3", "S_A_G3_c2_far_ii": "S_A_G3"}
    os.makedirs(os.path.join(out, "jobs"), exist_ok=True)
    jobs, d3c = [], {}
    for m in job_matrix():
        d = os.path.join(out, "jobs", m["dir"]); os.makedirs(d, exist_ok=True)
        rec = {k: m[k] for k in ("dir", "stage", "kind", "method", "ladder")}
        rec["structure"], rec["structure_src"] = m["structure"], m["src"]
        if m["src"] == "v5":
            src = os.path.join(v5_pkg, "jobs", A4_SRC)
            files = {}
            for f in ("POSCAR", "KPOINTS", "POTCAR.spec"):
                t = open(os.path.join(src, f), encoding="utf-8").read()
                if _sha_text(t) != v5man.get(f"jobs/{A4_SRC}/{f}"):
                    raise PkgError(f"V5 {A4_SRC}/{f} sha 가 V5 MANIFEST 와 다르다")
                files[f] = t
            base = open(os.path.join(src, "INCAR"), encoding="utf-8").read()
            if _sha_text(base) != v5man.get(f"jobs/{A4_SRC}/INCAR"):
                raise PkgError(f"V5 {A4_SRC}/INCAR sha 가 V5 MANIFEST 와 다르다")
            vj = v5jobs[A4_SRC]
            for r in ("a4A", "a4B"):
                files[f"INCAR.{r}"] = rung_text(base, r)
            rec.update({k: vj[k] for k in ("nions", "composition", "nelect_expected", "potcar_spec", "pp_expected_titel", "zval_expected", "encut", "sigma",
                                           "kpts", "cell_A", "dipol_z", "area_A2", "structure_sha256", "d3_2body_eV_ref")})
            rec.update({"ismear": 1, "v5_source": {"pkg": V5_PKG, "job": A4_SRC, "manifest_sha256": V5_MANIFEST_SHA256,
                                                   "files_sha256": {f: v5man[f"jobs/{A4_SRC}/{f}"] for f in ("POSCAR", "KPOINTS", "POTCAR.spec", "INCAR")}}})
            base_for_diff = base
        else:
            if m["src"] == "seal":
                sp = os.path.join(seal_dir, "structures", f"{m['structure']}.extxyz")
                want = seal["structures_sha256"].get(m["structure"])
                dip = seal["sets"][dipset[m["structure"]]]["dipfield"]
            else:
                sp = os.path.join(wadcc_pkg, "structures", f"{m['structure']}.extxyz")
                want = ccm["structures_sha256"].get(m["structure"])
                dip = ccj[m["structure"]]["dip"]
            if not want or _sha(sp) != want:
                raise PkgError(f"{m['dir']}: 구조 {m['structure']} sha 가 봉인과 다르다")
            at = read(sp)
            emx, eop = dip["emaxpos"], dip["eopreg"]
            clear = V.check_dip_clear(at, emx, eop); dz = V.dipol_z(emx, eop)
            pos, order, present = poscar_text(at, f"W_ad round2 {m['dir']} | src {m['structure']} sha {want[:16]}")
            base = incar_base(m["dir"], m["encut"], m["sigma"], dz, m["method"])
            files = {"POSCAR": pos, "KPOINTS": kpoints_text(m["kpts"]), "POTCAR.spec": "\n".join(POTCAR_MAP[s] for s in present) + "\n", "INCAR": base}
            for r in ("r1A", "r1B", "r2B"):
                files[f"INCAR.{r}"] = rung_text(base, r)
            sym = at.get_chemical_symbols(); c = at.cell.array
            rec.update({"structure_sha256": want, "nions": len(sym), "composition": {s: sym.count(s) for s in present},
                        "nelect_expected": sum(ZVAL[s] for s in sym), "potcar_spec": [POTCAR_MAP[s] for s in present],
                        "pp_expected_titel": [PP_EXPECTED_TITEL[s] for s in present], "zval_expected": [ZVAL[s] for s in present],
                        "encut": m["encut"], "sigma": m["sigma"], "ismear": 0, "kpts": list(m["kpts"]),
                        "cell_A": [round(float(x), 4) for x in at.cell.lengths()], "dipol_z": round(dz, 6), "dip": {"emaxpos": emx, "eopreg": eop},
                        "dip_min_clearance_A": clear, "poscar_order_to_original_index": order,
                        "area_A2": round(float(abs(c[0][0] * c[1][1] - c[0][1] * c[1][0])), 6), "estimate": estimate(at, m["encut"], m["kpts"])})
            if m["method"] == "pbed3":
                key = m["structure"]
                if key not in d3c:
                    d3c[key] = V.d3_ref_eV(at)
                rec["d3_2body_eV_ref"] = d3c[key]
            base_for_diff = base
        rungs = ("a4A", "a4B") if m["ladder"] == "a4" else ("0", "r1A", "r1B", "r2B")
        for r in rungs:
            if r == "0":
                continue
            got = {k: v[1] for k, v in semantic_diff(base_for_diff, files[f"INCAR.{r}"]).items()}
            if got != RUNG_DIFF[r]:
                raise PkgError(f"{m['dir']} INCAR.{r}: 의미상 차이 {got} ≠ 선언 {RUNG_DIFF[r]}")
        for n, t in files.items():
            _write(os.path.join(d, n), t)
        rec["rungs"] = {r: {"incar": "INCAR" if r == "0" else f"INCAR.{r}", "nelm": NELM_RUNG[r]} for r in rungs}
        rec["files_sha256"] = {n: _sha_text(t) for n, t in files.items()}
        jobs.append(rec)
    stages = {s: [j["dir"] for j in jobs if j["stage"] == s] for s in STAGE_EXPECT_H}
    _write(os.path.join(out, "STAGES.tsv"), "".join(f"{s}\t{STAGE_CAP_H[s]:g}\t{' '.join(stages[s])}\n" for s in STAGE_EXPECT_H) + f"TOTAL\t{TOTAL_CAP_H:g}\t-\n")
    _write(os.path.join(out, "JOBS.txt"), "\n".join(j["dir"] for j in jobs) + "\n")
    _write(os.path.join(out, "run_all.sh"), run_all_text()); os.chmod(os.path.join(out, "run_all.sh"), 0o755)
    meta = {"schema": "wad_round2_vasp_package/v1", "card": CARD, "amendment_4": AMEND4, "decisions": list(DECISIONS),
            "status": "준비본 v1 — Codex CZ 묶음 리뷰 전 · 발송 전",
            "tool_sha256": _sha(os.path.abspath(__file__)), "v5_tool_sha256": _sha(os.path.abspath(V.__file__)),
            "sources": {"p2s_seal_manifest_sha256": _sha(smp), "wadcc_manifest_sha256": _sha(os.path.join(wadcc_pkg, "cc_stage2_manifest.json")),
                        "v5_manifest_sha256": V5_MANIFEST_SHA256},
            "settings": {"species_order": SPECIES_ORDER, "potcar": POTCAR_MAP, "pp_expected_titel": PP_EXPECTED_TITEL, "zval": ZVAL,
                         "encut": ENCUT, "encut_g4": ENCUT_G4, "sigma": SIGMA_C, "sigma_half": SIGMA_C_HALF, "ismear": 0, "ediff": EDIFF,
                         "kpts": {"base": K_BASE, "dense": K_DENSE, "cc": K_CC}, "d3": V.D3_PARAMS,
                         "d3_cutoffs_A": {"VDW_RADIUS": V.VDW_RADIUS_A, "VDW_CNRADIUS": V.VDW_CNRADIUS_A}, "optb88": dict(OPTB88),
                         "nelm_by_rung": NELM_RUNG, "rung_diff": RUNG_DIFF, "return_allowed": RETURN_ALLOWED, "return_forbidden": RETURN_FORBIDDEN},
            "stages": {s: {"jobs": stages[s], "expect_ledger_h": STAGE_EXPECT_H[s], "cap_h": STAGE_CAP_H[s]} for s in STAGE_EXPECT_H},
            "total_cap_h": TOTAL_CAP_H, "jobs": jobs}
    _write(os.path.join(out, "jobs.json"), json.dumps(meta, ensure_ascii=False, indent=1, allow_nan=False))
    lines = []
    for root, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(root, f); r = os.path.relpath(p, out).replace(os.sep, "/")
            if r in ("MANIFEST.sha256", "README.md") or r.startswith(("run/", "run_aborted/")):
                continue
            lines.append(f"{_sha(p)}  {r}")
    _write(os.path.join(out, "MANIFEST.sha256"), "\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    msha = _sha(os.path.join(out, "MANIFEST.sha256"))
    _write(os.path.join(out, "README.md"), _readme(meta, msha))
    return meta, msha


# ───────────────────────── 러너 (업체 쪽 · bash · python 가정 없음) ─────────────────────────
RUN_ALL = r'''#!/usr/bin/env bash
# =============================================================================
# run_all.sh (W_ad round2 v1) — 탄소 P2′ 23 잡 + 은 a4 1 잡 · 단계 (P 파일럿 → 1 → 2 → 3 → 4) · 탄소 잡마다 사전등록 재시도 사다리
#   (단 0 → r1 ⓐ+ⓑ → r2 ⓑ) · 은 a4 = 두 단계 한 번 · SCF 판정 = OSZICAR 마지막 전자 반복행 (검사기와 같은 계약 · OUTCAR 문구로 판정하지 않는다)
#   필수: VASP_CMD · POTCAR_DIR (PAW_PBE: <POTCAR_DIR>/{Li_sv,P,S,Cl,Ag,C}/POTCAR) · optB88 잡이 있으면 VDW_KERNEL (vdw_kernel.bindat 경로)
#   STAGES (기본 "P" = 파일럿 5 잡) — P 밖 단계는 RELEASE_FILE + RELEASE_SHA256 (파일럿 반송 뒤 우리가 보낸다) 이 맞아야만 돈다
#   선택: PERF_TAGS_FILE (한 줄에 대입 하나 · NCORE/NPAR/KPAR/NSIM 양의 정수 · LPLANE/LSCALU/LSCALAPACK .TRUE./.FALSE.) · JOBS (단계 안 일부만)
#         PACK_ONLY=1 (계산 없이 포장만) · WATCH_S (경보 점검 간격 초 · 기본 60)
#   0 스텝 인프라 중단 기록 (전자 반복행 0 · 스케줄러 기록이 있을 때만 · 잡마다 2 회):
#     bash run_all.sh --infra-abort <잡> <단 0|r1A|r1B|r2B|a4A|a4B> <스케줄러 잡 id> <취소 UTC> <사유…>   → 그 시도를 run_aborted/ 로 옮긴다 · 다시 돌리면 같은 단부터
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · 시도 폴더가 이미 있으면 덮어쓰지 않습니다 (이어 돌리기는 기록을 다시 판정해 다음 단을 정합니다)
#   종료: 0 고른 잡 전부 값 있음 · 1 값 없는 잡 있음 (묶음 만듦 — 실패도 기록) · 2 패키지·환경·인자 오류 (아무것도 안 돎) · 4 포장 실패 (PACK_ONLY=1 로 다시)
#         5 단계·전체 누적 상한 (다음 잡 안 띄움 · 묶음 만듦 · 1저자 결정) · 6 공통 환경 고장 (VASP 빌드 · PP · vdW 커널 — 전체 정지 · 묶음 만듦)
#   보내는 것: 종료 0·1·5·6 뒤 `sha256sum -c round2_return.tgz.sha256` 까지 통과한 쌍. 종료 4 면 PACK_ONLY=1 → 종료 0 + 같은 확인 뒤.
#   지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk (mawk/gawk)
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='@RET_ALLOW@'
RET_FORBID='@RET_FORBID@'
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
utc(){ date -u +%FT%TZ; }
mkdir -p run
log(){ echo "$*"; echo "$(utc) $*" >> run/env.txt; }
clean(){ printf '%s' "$1" | tr -d '"\\\r\n\t' ; }
cap_num(){ [[ "$1" =~ ^[0-9]+(\.[0-9]+)?$ ]] && awk -v x="$1" 'BEGIN { exit !(x + 0 > 0) }'; }   # 상한 값 = 유한한 양수 (nan · inf · 음수 · 0 거부)
incar_val(){ awk -v T="$2" 'BEGIN{T=toupper(T)} { sub(/[#!].*/, ""); n=split($0, st, ";"); for (i=1; i<=n; i++) { s=st[i]; p=index(s, "="); if (!p) continue;
  k=substr(s, 1, p-1); v=substr(s, p+1); gsub(/[ \t]/, "", k); gsub(/^[ \t]+|[ \t]+$/, "", v); if (toupper(k)==T) val=v } } END { if (val!="") print val }' "$1" 2>/dev/null; }

# ── 판정 계약 (검사기 judge_text 와 같다 · 순서까지) → "상태 행수 dE deps 사유" ──
#  ① 행 0 → SCF_UNVERIFIED  ② 스텝 번호 1,2,…,N 아님 · 이온 요약(F=) 뒤 행 → SCF_UNVERIFIED  ③ N > NELM(이 시도의 INCAR) → SCF_UNVERIFIED
#  ④ 확정 모순은 rc 보다 먼저 (CZ Q-CZ-1): OUTCAR 실행 머리줄 ≥ 2 → SCF_UNVERIFIED · OUTCAR 가 끝까지 쓰였는데 머리줄 ≠ 1 또는
#     마지막 전자 반복 번호 k ≠ N → SCF_UNVERIFIED · 안 끝났는데 k > N + 1 (판정 근거 OSZICAR 가 두 스텝 이상 모자람) → SCF_UNVERIFIED
#     (안 끝난 OUTCAR 의 k 없음 · k ≤ N + 1 은 잘림·스텝 도중 충돌 = 결측이라 ⑤ 로 간다)
#  ⑤ rc ≠ 0 · 미종료 → RUN_FAILED  ⑥ 마지막 dE·d eps 가 유한수가 아님 → SCF_UNVERIFIED  ⑦ |dE| ≤ EDIFF 그리고 |d eps| ≤ EDIFF → OK · 아니면 SCF_NOT_CONVERGED
judge(){
  local d=$1 rc term nrun nelm ediff oit
  rc=$(grep -o '"rc": *-\{0,1\}[0-9]*' "$d/attempt.json" 2>/dev/null | head -1 | grep -o -- '-\{0,1\}[0-9]*$'); rc=${rc:-${2:-NA}}
  term=0; grep -aq "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  nrun=$(grep -acE '^[[:space:]]*vasp\.[0-9]' "$d/OUTCAR" 2>/dev/null); nrun=${nrun:-0}
  nelm=$(incar_val "$d/INCAR" NELM); ediff=$(incar_val "$d/INCAR" EDIFF)
  oit=$(grep -aoE 'Iteration +[0-9]+\( *[0-9]+\)' "$d/OUTCAR" 2>/dev/null | tail -1 | sed -E 's/.*\( *([0-9]+)\)/\1/')
  cat "$d/OSZICAR" 2>/dev/null | awk -v rc="$rc" -v term="$term" -v nrun="$nrun" -v nelm="${nelm:-NA}" -v ediff="${ediff:-NA}" -v oit="${oit:-NA}" '
    function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
    function finite(s,  t) { if (!isnum(s)) return 0; t = sprintf("%g", s + 0); return (t !~ /inf|nan/) }
    /^[ \t]*[0-9]+[ \t]+F=/ { ion = 1; next }
    /^[ \t]*(DAV|RMM|CG|SDA):/ { n++; k = $2; if (bad == "") { if (ion) bad = "rows_after_ion_summary"; else if (k !~ /^[0-9]+$/ || k + 0 != n) bad = "step_numbering" }
                                 de = (NF >= 5) ? $4 : ""; dp = (NF >= 5) ? $5 : ""; next }
    END { o = n + 0
      if (o == 0) { print "SCF_UNVERIFIED 0 NA NA no_rows"; exit }
      if (bad != "") { print "SCF_UNVERIFIED", o, "NA", "NA", bad; exit }
      if (nelm !~ /^[0-9]+$/) { print "SCF_UNVERIFIED", o, "NA", "NA", "nelm_unknown"; exit }
      if (o > nelm + 0) { print "SCF_UNVERIFIED", o, "NA", "NA", "n_gt_nelm"; exit }
      if (nrun + 0 >= 2) { print "SCF_UNVERIFIED", o, "NA", "NA", "run_blocks"; exit }
      if (term == 1) {
        if (nrun + 0 != 1) { print "SCF_UNVERIFIED", o, "NA", "NA", "run_blocks"; exit }
        if (oit != o) { print "SCF_UNVERIFIED", o, "NA", "NA", "outcar_oszicar_mismatch"; exit }
      } else if (oit ~ /^[0-9]+$/ && oit + 0 > o + 1) { print "SCF_UNVERIFIED", o, "NA", "NA", "outcar_oszicar_mismatch"; exit }
      if (rc != "0" || term != 1) { print "RUN_FAILED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "rc_or_not_terminated"; exit }
      if (!finite(de) || !finite(dp)) { print "SCF_UNVERIFIED", o, (de == "" ? "NA" : de), (dp == "" ? "NA" : dp), "nonfinite"; exit }
      if (!finite(ediff)) { print "SCF_UNVERIFIED", o, de, dp, "ediff_unknown"; exit }
      a = de + 0; b = dp + 0; if (a < 0) a = -a; if (b < 0) b = -b
      if (a <= ediff + 0 && b <= ediff + 0) print "OK", o, de, dp, "-"; else print "SCF_NOT_CONVERGED", o, de, dp, "-" }'
}

# ── 조기 경보 (120 스텝 뒤 20 스텝마다 · 경보 ≠ 중단) ──
alarms(){ awk 'function isnum(s) { return s ~ /^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$/ }
  function ab(x) { return x < 0 ? -x : x }
  /^[ \t]*(DAV|RMM|CG|SDA):/ { n++; e[n] = $4; p[n] = $5 }
  END { out = ""; if (n == 0) { print "0 -"; exit }
    if (!isnum(e[n]) || !isnum(p[n])) out = out "nonfinite,"
    for (q = 1; q <= 2; q++) { last = (q == 1) ? e[n] : p[n]; stall = (isnum(last) && ab(last + 0) > 1e-4)
      if (n >= 80) { m1 = -1; m2 = -1
        for (i = n - 39; i <= n; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m1 < 0 || v < m1) m1 = v } }
        for (i = n - 79; i <= n - 40; i++) { v = (q == 1) ? e[i] : p[i]; if (isnum(v)) { v = ab(v + 0); if (m2 < 0 || v < m2) m2 = v } }
        if (m1 >= 0 && m2 >= 0 && m1 >= m2) stall = 1 }
      if (stall) out = out ((q == 1) ? "dE_stall," : "deps_stall,") }
    print n, (out == "" ? "-" : out) }' "$1/OSZICAR" 2>/dev/null; }
watch_scf(){
  local d=$1 tag=$2 last=100 o n a
  while [ -f "$d/.running" ]; do
    sleep "${WATCH_S:-60}"
    [ -f "$d/OSZICAR" ] || continue
    o=$(alarms "$d"); n=${o%% *}; a=${o#* }
    case "$n" in ''|*[!0-9]*) continue;; esac
    if [ "$n" -ge 120 ] && [ "$n" -ge $((last + 20)) ]; then
      last=$((n - n % 20))
      if [ "$a" != "-" ]; then echo "$(utc) $tag step $n $a" >> "$d/warn.log"; log "⚠ 경보 $tag 스텝 $n: $a (중단 아님 · NELM 까지 돈다)"; fi
    fi
  done
}

# ── 포장 (허용 목록 · 단계마다 성공 확인 · V5 v6 절차) ──
pack_fail(){ echo "⛔ 포장: $1"; rm -f round2_return.tgz.part round2_return.tgz.sha256.part; return 1; }
pack(){
  local T=round2_return.tmp g hh n_mg n_so n_li f
  rm -rf "$T" round2_return.tgz.part round2_return.tgz.sha256.part round2_return.list; mkdir "$T" || return 1
  find run run_aborted -mindepth 2 -maxdepth 3 -type f > "$T/found" 2> /dev/null; g=$?
  [ -d run_aborted ] || g=0
  [ "$g" = 0 ] || { pack_fail "run/ 열거 실패"; return 1; }
  grep -E "^(run|run_aborted)/[^/]+/(stageA/)?($RET_ALLOW)$" "$T/found" > "$T/allowed"; g=$?
  [ "$g" -le 1 ] || { pack_fail "허용 목록 필터 오류 ($g)"; return 1; }
  LC_ALL=C sort "$T/allowed" > "$T/sorted" || { pack_fail "정렬 실패"; return 1; }
  : > "$T/mgmt" || { pack_fail "관리 목록 초기화 실패"; return 1; }
  n_mg=0
  for f in run/env.txt run/status.tsv run/infra_aborts.tsv; do
    [ -f "$f" ] || continue
    n_mg=$((n_mg + 1)); echo "$f" >> "$T/mgmt" || { pack_fail "관리 목록 쓰기 실패 ($f)"; return 1; }
  done
  echo MANIFEST.sha256 > round2_return.list || { pack_fail "목록 쓰기 실패 (MANIFEST.sha256)"; return 1; }
  cat "$T/mgmt" "$T/sorted" >> round2_return.list || { pack_fail "목록 쓰기 실패"; return 1; }
  n_so=$(wc -l < "$T/sorted") && n_li=$(wc -l < round2_return.list) || { pack_fail "목록 검증 준비 실패"; return 1; }
  [ "$n_li" -eq $((1 + n_mg + n_so)) ] || { pack_fail "목록 줄 수가 맞지 않는다 ($n_li ≠ 1+$n_mg+$n_so)"; return 1; }
  grep -qxF MANIFEST.sha256 round2_return.list || { pack_fail "목록에 MANIFEST.sha256 이 없다"; return 1; }
  tar czf round2_return.tgz.part -T round2_return.list || { pack_fail "tar 실패"; return 1; }
  tar tzf round2_return.tgz.part > "$T/members" || { pack_fail "묶음 구성원 열람 실패 — 검사할 수 없으면 보내지 않는다"; return 1; }
  grep -E "(^|/)($RET_FORBID)$" "$T/members" > "$T/forbidden"; g=$?
  if [ "$g" -eq 0 ]; then pack_fail "반송 묶음에 금지 파일이 들어갔다 — 보내지 않는다: $(tr '\n' ' ' < "$T/forbidden")"; return 1
  elif [ "$g" -ne 1 ]; then pack_fail "구성원 검사 오류 ($g)"; return 1; fi
  LC_ALL=C sort "$T/members" > "$T/members.sorted" && LC_ALL=C sort round2_return.list > "$T/list.sorted" || { pack_fail "구성원 대조 준비 실패"; return 1; }
  cmp -s "$T/members.sorted" "$T/list.sorted" || { pack_fail "묶음 구성원이 목록과 다르다 — 보내지 않는다"; return 1; }
  sha256sum round2_return.tgz.part > "$T/sha" || { pack_fail "sha256 계산 실패"; return 1; }
  hh=$(cut -d' ' -f1 < "$T/sha") || { pack_fail "sha256 읽기 실패"; return 1; }
  [[ "$hh" =~ ^[0-9a-fA-F]{64}$ ]] || { pack_fail "sha256 형식 이상 ($hh)"; return 1; }
  printf '%s  round2_return.tgz\n' "$hh" > round2_return.tgz.sha256.part || { pack_fail "sha 쓰기 실패"; return 1; }
  mv -f round2_return.tgz.part round2_return.tgz && mv -f round2_return.tgz.sha256.part round2_return.tgz.sha256 || { pack_fail "승격(mv) 실패 — sha256sum -c 로 확인"; return 1; }
  rm -rf "$T" || echo "⚠ 진단 폴더 정리 실패 — 묶음은 승격됐다"
  return 0
}
finish(){ # $1 종료 코드 — 포장하고 끝낸다 (포장 실패면 4)
  if ! pack; then echo "⛔ 반송 포장 실패 — 계산 결과는 run/ 에 그대로 있다. 다시 돌리지 말고 PACK_ONLY=1 bash run_all.sh 로 포장만"; exit 4; fi
  case "$1" in
    0) echo "✅ 끝 — round2_return.tgz 와 .sha256 을 보내 주세요";;
    1) echo "⚠ 값 없는 잡이 있다 — 그대로 반송해 주세요 (실패도 기록입니다)";;
    5) echo "⏸ 누적 상한 — 다음 잡을 띄우지 않았다. 반송해 주시고 1저자 결정을 기다려 주세요";;
    6) echo "⛔ 공통 환경 고장 — 전체 정지. 반송해 주시고 연락 주세요";;
  esac
  exit "$1"
}

# ── 단계 · 잡 표 ──
declare -A STAGE_OF CAP_H
STAGE_LIST=""
while IFS=$'\t' read -r s c js; do
  [ -n "$s" ] || continue
  if [ "$s" = TOTAL ]; then TOTAL_CAP=$c; continue; fi
  STAGE_LIST="$STAGE_LIST $s"; CAP_H[$s]=$c
  for j in $js; do STAGE_OF[$j]=$s; done
done < STAGES.tsv
ladder_of(){ case "$1" in @A4_JOB@) echo a4;; *) echo carbon;; esac; }
is_optb88(){ grep -qx 'GGA = BO' "jobs/$1/INCAR" 2>/dev/null || grep -qx 'GGA = BO' "jobs/$1/INCAR.a4A" 2>/dev/null; }

# ── 0 스텝 인프라 중단 기록 ──
if [ "${1:-}" = "--infra-abort" ]; then
  [ $# -ge 6 ] || { echo "⛔ 쓰는 법: --infra-abort <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유…>"; exit 2; }
  job=$2; rung=$3; sid=$(clean "$4"); when=$(clean "$5"); shift 5; why=$(clean "$*")
  [ -n "${STAGE_OF[$job]:-}" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  case "$rung" in 0) src=run/$job;; r1A) src=run/${job}_r1/stageA;; r1B) src=run/${job}_r1;; r2B) src=run/${job}_r2;; a4A) src=run/${job}_a4/stageA;; a4B) src=run/${job}_a4;;
    *) echo "⛔ 모르는 단 $rung"; exit 2;; esac
  [ -d "$src" ] || { echo "⛔ $src 가 없다"; exit 2; }
  n=$(grep -acE '^[[:space:]]*(DAV|RMM|CG|SDA):' "$src/OSZICAR" 2>/dev/null); n=${n:-0}
  [ "$n" = 0 ] || { echo "⛔ 전자 반복행 $n 개 — 0 스텝 중단이 아니다 (실행 실패는 사다리가 다룬다)"; exit 2; }
  [ -n "$sid" ] && [ -n "$when" ] && [ -n "$why" ] || { echo "⛔ 스케줄러 잡 id · 취소 시각 · 사유가 다 있어야 한다"; exit 2; }
  k=$(awk -F'\t' -v j="$job" '$2 == j' run/infra_aborts.tsv 2>/dev/null | wc -l); k=${k:-0}
  [ "$k" -lt 2 ] || { echo "⛔ $job 0 스텝 중단 기록이 이미 2 회 — 상한 (1저자에게 알린다)"; exit 2; }
  mkdir -p run_aborted; dst=run_aborted/${job}_${rung}_$((k + 1))
  mkdir "$dst" || exit 2
  shopt -s dotglob nullglob
  if [ "$rung" = r1B ] || [ "$rung" = a4B ]; then
    [ -d "$src/.b" ] || { echo "⛔ $src 에 ⓑ 가 시작된 흔적(.b)이 없다"; exit 2; }
    for f in "$src"/*; do [ "$(basename "$f")" = stageA ] && continue; mv "$f" "$dst/" || exit 2; done
  else
    for f in "$src"/*; do mv "$f" "$dst/" || exit 2; done; rmdir "$src" || exit 2
  fi
  shopt -u dotglob nullglob
  rm -f "$dst/POTCAR" "$dst/WAVECAR" "$dst/CHGCAR" "$dst/CHG" "$dst/vasprun.xml" "$dst/vdw_kernel.bindat" "$dst/.running"
  w=${WALL_S:-NA}
  printf '{"job": "%s", "rung": "%s", "sched_job_id": "%s", "cancel_utc": "%s", "reason": "%s", "wall_s": "%s", "recorded_utc": "%s"}\n' \
    "$job" "$rung" "$sid" "$when" "$why" "$w" "$(utc)" > "$dst/infra_abort.json"
  [ -f run/infra_aborts.tsv ] || printf "recorded_utc\tjob\trung\tsched_job_id\tcancel_utc\twall_s\treason\n" > run/infra_aborts.tsv
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$(utc)" "$job" "$rung" "$sid" "$when" "$w" "$why" >> run/infra_aborts.tsv
  echo "✓ $src → $dst (0 스텝 인프라 중단 $((k + 1))/2) — 다시 돌리면 같은 단부터"; exit 0
fi

if [ "${PACK_ONLY:-0}" = 1 ]; then
  echo "pack_only $(utc)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 로 다시"; exit 4
fi

# ── 단계 · 해제 파일 ──
STAGES=${STAGES:-P}
REL_STAGES=" "; REL_TOTAL=""; REL_VER=""; REL_KERNEL=""; RESTART_RE=""; KERNEL_RE=""
declare -A REL_SP
for s in $STAGES; do [ -n "${CAP_H[$s]:-}" ] || { echo "⛔ 모르는 단계 $s"; exit 2; }; done
need_rel=0; for s in $STAGES; do [ "$s" = P ] || need_rel=1; done
if [ "$need_rel" = 1 ]; then
  [ -n "${RELEASE_FILE:-}" ] && [ -f "$RELEASE_FILE" ] && [ -n "${RELEASE_SHA256:-}" ] || { echo "⛔ P 밖 단계는 RELEASE_FILE · RELEASE_SHA256 이 필요하다 (파일럿 반송 뒤 받는다)"; exit 2; }
  [ "$(h "$RELEASE_FILE")" = "$RELEASE_SHA256" ] || { echo "⛔ 해제 파일 sha 가 RELEASE_SHA256 과 다르다"; exit 2; }
  while IFS=$'\t' read -r k a b; do
    case "$k" in
      stages) REL_STAGES=" $a ";;
      cap_h) cap_num "$b" || { echo "⛔ 해제 파일의 단계 $a 상한 '$b' 가 유한한 양수가 아니다"; exit 2; }; CAP_H[$a]=$b;;
      total_cap_h) cap_num "$a" || { echo "⛔ 해제 파일의 전체 상한 '$a' 가 유한한 양수가 아니다"; exit 2; }; REL_TOTAL=$a;;
      vasp_version) REL_VER=$a;;
      species_sha256) REL_SP[$a]=$b;;
      kernel_sha256) REL_KERNEL=$a;;
      restart_read_regex) RESTART_RE=$a;;
      kernel_read_regex) KERNEL_RE=$a;;           # 기록만 (커널 읽기 판정은 검사기)
    esac
  done < "$RELEASE_FILE"
  for s in $STAGES; do [ "$s" = P ] && continue; case "$REL_STAGES" in *" $s "*) ;; *) echo "⛔ 해제 파일이 단계 $s 를 풀지 않았다"; exit 2;; esac; done
  [ -n "$REL_VER" ] && [ -n "$REL_KERNEL" ] && [ "${#REL_SP[@]}" -ge 6 ] || { echo "⛔ 해제 파일에 vasp_version · kernel_sha256 · species_sha256 (6 종) 이 다 있어야 한다"; exit 2; }
  [ -n "$REL_TOTAL" ] && TOTAL_CAP=$REL_TOTAL
fi
SEL=""
for s in $STAGES; do for j in $(awk -F'\t' -v s="$s" '$1 == s {print $3}' STAGES.tsv); do SEL="$SEL $j"; done; done
if [ -n "${JOBS:-}" ]; then
  for j in $JOBS; do case " $SEL " in *" $j "*) ;; *) echo "⛔ $j 는 고른 단계(STAGES=$STAGES)에 없다"; exit 2;; esac; done
  SEL=$JOBS
fi
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 64 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
need_k=0; for j in $SEL; do is_optb88 "$j" && need_k=1; done
if [ "$need_k" = 1 ]; then
  [ -n "${VDW_KERNEL:-}" ] && [ -s "$VDW_KERNEL" ] && [ -r "$VDW_KERNEL" ] || { log "⛔ optB88 잡이 있는데 VDW_KERNEL (vdw_kernel.bindat) 이 없다 — 공통 환경 고장 · 전체 정지"; finish 6; }
  KSHA=$(h "$VDW_KERNEL"); KSIZE=$(stat -c %s "$VDW_KERNEL")
  if [ -n "$REL_KERNEL" ] && [ "$KSHA" != "$REL_KERNEL" ]; then log "⛔ vdW 커널 sha $KSHA ≠ 봉인 $REL_KERNEL — 공통 환경 고장 · 전체 정지"; finish 6; fi
fi
PERF_LINES=""
if [ -n "${PERF_TAGS_FILE:-}" ]; then
  { [ -f "$PERF_TAGS_FILE" ] && [ -r "$PERF_TAGS_FILE" ]; } || { echo "⛔ PERF_TAGS_FILE 을 읽을 수 없다: $PERF_TAGS_FILE"; exit 2; }
  bad=0; seen=" "
  while IFS= read -r ln || [ -n "$ln" ]; do
    t=$(printf '%s' "$ln" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    case "$t" in ''|'#'*|'!'*) continue;; esac
    case "$t" in *';'*|*'\'*|*'#'*|*'!'*) echo "⛔ 성능 파일: 세미콜론·역슬래시·줄 끝 주석 금지 — $t"; bad=1; continue;; esac
    if printf '%s' "$t" | grep -Eq '^(NCORE|NPAR|KPAR|NSIM)[[:space:]]*=[[:space:]]*[1-9][0-9]*$'; then :
    elif printf '%s' "$t" | grep -Eqi '^(LPLANE|LSCALU|LSCALAPACK)[[:space:]]*=[[:space:]]*\.?(TRUE|FALSE|T|F)\.?$'; then :
    else echo "⛔ 성능 파일: 허용 밖 줄 — $t"; bad=1; continue; fi
    tag=$(printf '%s' "${t%%=*}" | tr -d '[:space:]' | tr '[:lower:]' '[:upper:]')
    case "$seen" in *" $tag "*) echo "⛔ 성능 파일: $tag 중복"; bad=1; continue;; esac
    seen="$seen$tag "; PERF_LINES="$PERF_LINES$t"$'\n'
  done < "$PERF_TAGS_FILE"
  [ "$bad" = 0 ] || exit 2
fi
{ echo "date_utc $(utc)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR"; echo "STAGES $STAGES"
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(h MANIFEST.sha256)"
  [ "$need_k" = 1 ] && echo "VDW_KERNEL $VDW_KERNEL sha256 $KSHA size $KSIZE"
  [ "$need_rel" = 1 ] && echo "RELEASE $RELEASE_FILE sha256 $RELEASE_SHA256"
  [ -n "$KERNEL_RE" ] && echo "KERNEL_READ_RE $KERNEL_RE"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\trung\tstage\trc\tstatus\tn_elec\tdE\tdeps\twhy\twall_s\n" > run/status.tsv

# ── 누적 벽시계 (attempt.json t_start→t_end · 0 스텝 중단 포함) ──
wall_s_of(){ # $1 단계 (ALL = 전체)
  local f j w s tot=0 d
  for f in $(find run run_aborted -name attempt.json 2>/dev/null) $(find run_aborted -name infra_abort.json 2>/dev/null); do
    d=$(dirname "$f")
    if [ "$(basename "$f")" = infra_abort.json ]; then
      [ -f "$d/attempt.json" ] && continue
      w=$(grep -o '"wall_s": "[0-9]*"' "$f" | grep -o '[0-9]*'); w=${w:-0}
    else
      w=$(awk '{ if (match($0, /"t_start": [0-9]+/)) a = substr($0, RSTART + 11, RLENGTH - 11); if (match($0, /"t_end": [0-9]+/)) b = substr($0, RSTART + 9, RLENGTH - 9) } END { print (b != "" && a != "") ? b - a : 0 }' "$f")
    fi
    j=$(grep -o '"job": "[^"]*"' "$f" | head -1 | sed 's/"job": "//; s/"$//')
    s=${STAGE_OF[$j]:-?}
    if [ "$1" = ALL ] || [ "$1" = "$s" ]; then tot=$((tot + w)); fi
  done
  echo "$tot"
}
cap_ok(){ # $1 잡 → 0 이면 띄워도 된다 (단계 · 전체 상한)
  local s=${STAGE_OF[$1]} ws wt
  ws=$(wall_s_of "$s"); wt=$(wall_s_of ALL)
  awk -v w="$ws" -v c="${CAP_H[$s]}" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ 단계 $s 누적 $((ws / 3600)) h > 상한 ${CAP_H[$s]} h — $1 을 띄우지 않는다"; return 1; }
  awk -v w="$wt" -v c="$TOTAL_CAP" 'BEGIN { exit !(w <= c * 3600) }' || { log "⏸ 전체 누적 $((wt / 3600)) h > 상한 $TOTAL_CAP h — $1 을 띄우지 않는다"; return 1; }
  return 0
}
pp_ok(){ # $1 잡 — 해제 뒤에는 PP 종별 sha 가 봉인과 같아야 한다
  local p
  [ "$need_rel" = 1 ] || return 0
  while read -r p; do [ -n "$p" ] || continue
    [ "$(h "$POTCAR_DIR/$p/POTCAR")" = "${REL_SP[$p]:-x}" ] || { log "⛔ POTCAR $p sha 가 봉인과 다르다 — 공통 환경 고장 · 전체 정지"; return 1; }
  done < "jobs/$1/POTCAR.spec"
}
ver_of(){ grep -am1 -E '^[[:space:]]*vasp\.[0-9]' "$1/OUTCAR" 2>/dev/null | tr -s '[:space:]' ' ' | sed 's/^ //; s/ $//'; }

# ── WAVECAR 머리 (VASP 5.x: 첫 레코드 RECL·NSPIN·RTAG · 둘째 레코드 NKPTS·NBANDS·ENCUT) ──
wav_head(){ local f=$1 r
  r=$(od -A n -t f8 -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%.0f ", $i }'); set -- $r
  [ $# -eq 3 ] && [ "$1" -gt 0 ] 2>/dev/null || { echo "NA NA NA NA NA NA"; return; }
  echo "$1 $2 $3 $(od -A n -t f8 -j "$1" -N 24 "$f" 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) printf "%s ", ($i == int($i) ? sprintf("%.0f", $i) : sprintf("%.4f", $i)) }')"
}
out_num(){ if [ "$2" = ENCUT ]; then grep -aoE "ENCUT *= *[0-9.]+ eV" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+ eV$' | grep -oE '^[0-9.]+';
  else grep -aoE "$2 *= *[0-9.]+" "$1/OUTCAR" 2>/dev/null | tail -1 | grep -oE '[0-9.]+$'; fi; }

# ── 한 시도 ──
run_one(){ # $1 잡 · $2 단 · $3 시도 폴더 · $4 INCAR 이름 · $5 WAVECAR 원본 (B 단만) → 0 돌림 · 3 준비 실패 · 6 공통 환경 고장
  #   A·단 0·r2 는 폴더를 mkdir 로 차지한다 · r1B·a4B 는 ⓐ 가 든 시도 폴더 안에서 `.b` 를 mkdir 로 차지한다 (둘 다 원자적 · 덮어쓰지 않는다)
  local job=$1 rung=$2 d=$3 inc=$4 wsrc=${5:-} rid t0 t1 rc j wsha="" wcp="" wend hd istart icharg nr pr hon ksha="" ver
  pp_ok "$job" || return 6        # 모든 VASP 실행 직전 · 폴더를 차지하기 전 (이어 돌린 ⓑ 포함 — CZ Q-CZ-3)
  case "$rung" in
    r1B|a4B) mkdir "$d/.b" 2>/dev/null || { echo "⛔ $d/.b 가 이미 있다 — ⓑ 를 덮어쓰지 않는다"; return 3; };;
    *) mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; };;
  esac
  { cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/" && cp "jobs/$job/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; rm -f "$d/POTCAR"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$job/POTCAR.spec"
  grep -aE "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  if grep -qx 'GGA = BO' "$d/INCAR"; then
    cp "$VDW_KERNEL" "$d/vdw_kernel.bindat" || return 6
    ksha=$(h "$d/vdw_kernel.bindat"); [ "$ksha" = "$KSHA" ] || { log "⛔ 복사한 vdW 커널 sha 불일치 — 공통 환경 고장"; return 6; }
  fi
  if [ -n "$wsrc" ]; then
    cp "$wsrc" "$d/WAVECAR" || return 3
    wsha=$(h "$wsrc"); wcp=$(h "$d/WAVECAR")
  fi
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s)
  touch "$d/.running"; watch_scf "$d" "$job/$rung" & local wpid=$!
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
  rm -f "$d/.running"; kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
  ver=$(clean "$(ver_of "$d")")
  case "$rung" in
    r1A|a4A)
      hd=$(wav_head "$d/WAVECAR")
      printf '{"sha256": "%s", "size": %s, "head": "%s", "outcar": {"NKPTS": "%s", "NBANDS": "%s", "ENCUT": "%s"}}\n' "$(h "$d/WAVECAR")" "$(stat -c %s "$d/WAVECAR" 2>/dev/null || echo 0)" \
        "$hd" "$(out_num "$d" NKPTS)" "$(out_num "$d" NBANDS)" "$(out_num "$d" ENCUT)" > "$d/WAVECAR.info";;
    r1B|r2B|a4B)
      wend=$(h "$d/WAVECAR")
      # Startparameter 줄만 ('ISTART = n  job :' · 'ICHARG = n  charge:') — INCAR 를 되울리는 빌드에서 입력값을 실제값으로 읽지 않게 (마지막 줄)
      istart=$(grep -aE '^[[:space:]]*ISTART *= *[0-9]+[[:space:]]+job' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ISTART *= *[0-9]+' | grep -oE '[0-9]+$')
      icharg=$(grep -aE '^[[:space:]]*ICHARG *= *[0-9]+[[:space:]]+charge' "$d/OUTCAR" 2>/dev/null | tail -1 | grep -oE 'ICHARG *= *[0-9]+' | grep -oE '[0-9]+$')
      nr=0; grep -aq "WAVECAR not read" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && nr=1
      pr=NA; if [ -n "$RESTART_RE" ]; then pr=0; grep -aqE "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null && pr=1; fi
      hon=0; [ "$istart" = 1 ] && [ "$icharg" = 0 ] && [ "$nr" = 0 ] && [ "$pr" != 0 ] && [ -n "$wsha" ] && [ "$wsha" = "$wcp" ] && [ "$wcp" = "$wend" ] && hon=1
      printf '{"src_sha256": "%s", "copied_sha256": "%s", "end_sha256": "%s", "istart": "%s", "icharg": "%s", "not_read_phrase": %s, "positive_regex_match": "%s", "honoured": %s}\n' \
        "$wsha" "$wcp" "$wend" "${istart:-NA}" "${icharg:-NA}" "$nr" "$pr" "$hon" > "$d/WAVECAR.info";;
  esac
  printf '{"job": "%s", "attempt": "%s", "stage": "%s", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "vasp_version": "%s", "kernel_sha256": "%s", "perf": "%s", "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s", "WAVECAR.info": "%s"}}\n' \
    "$job" "$rung" "${STAGE_OF[$job]}" "$rid" "$rc" "$t0" "$t1" "$ver" "$ksha" "$(printf '%s' "$PERF_LINES" | tr '\n' ';')" \
    "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" "$(h "$d/WAVECAR.info")" > "$d/attempt.json"
  j=$(judge "$d"); set -- $j
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "$rung" "${STAGE_OF[$job]}" "$rc" "$1" "$2" "$3" "$4" "$5" "$((t1 - t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml" "$d/vdw_kernel.bindat"
  case "$rung" in r1A|a4A) ;; *) rm -f "$d/WAVECAR";; esac      # ⓐ WAVECAR 는 그 잡 사다리가 끝날 때까지 둔다 (반송 안 함 · sha·크기·머리만)
  if [ "$need_rel" = 1 ] && [ -n "$ver" ] && [ "$ver" != "$REL_VER" ]; then log "⛔ $job/$rung VASP 빌드 '$ver' ≠ 봉인 — 공통 환경 고장 · 전체 정지"; return 6; fi
  return 0
}
wsha(){ grep -o "\"$2\": \"[0-9a-f]*\"" "$1" 2>/dev/null | head -1 | grep -o '[0-9a-f]\{64\}'; }   # WAVECAR.info 의 sha 필드 하나 ($1 파일 · $2 키)
stat_of(){ # 시도 폴더 · 단 → 상태 (B 단은 재시작 확인을 먼저 · 기록 없으면 INCOMPLETE_ATTEMPT)
  #   재시작 확인 = 검사기와 같다: 기록 honoured · ⓑ src = copied = end = 그 ⓐ 의 기록 sha (r1B·a4B ← 같은 폴더 stageA · r2B ← r1 의 stageA)
  #   · 해제 파일에 재시작 regex 가 있으면 원문 (stdout.log · OUTCAR) 을 다시 본다 — 이어 돌리기 · 손댄 기록에서도 검사기와 같은 답
  local d=$1 j a s
  [ -f "$d/attempt.json" ] || { echo INCOMPLETE_ATTEMPT; return; }
  case "$2" in r1B|r2B|a4B)
    case "$2" in r2B) a=${d%_r2}_r1/stageA;; *) a=$d/stageA;; esac
    s=$(wsha "$a/WAVECAR.info" sha256)
    { grep -q '"honoured": 1' "$d/WAVECAR.info" 2>/dev/null && [ -n "$s" ] && [ "$(wsha "$d/WAVECAR.info" src_sha256)" = "$s" ] \
      && [ "$(wsha "$d/WAVECAR.info" copied_sha256)" = "$s" ] && [ "$(wsha "$d/WAVECAR.info" end_sha256)" = "$s" ] \
      && { [ -z "$RESTART_RE" ] || grep -aqE "$RESTART_RE" "$d/stdout.log" "$d/OUTCAR" 2>/dev/null; }; } || { echo RESTART_NOT_HONOURED; return; };;
  esac
  j=$(judge "$d"); echo "${j%% *}"
}
elig_A(){ # ⓐ 자격 (ⓑ 를 띄우기 전 — ① 정상 종료·유한 상태 ② 유효 WAVECAR: 머리 = ⓐ OUTCAR 원문 NKPTS·NBANDS·ENCUT · WAVECAR.info 의 OUTCAR 사본 = 원문
  #         (검사기 a_eligible 과 같다) ③ 기록 sha = 지금 WAVECAR · 복사본 sha 는 run_one 이 ⓑ 기록에 남기고 재시작 확인이 본다)
  local d=$1 s r c k
  s=$(stat_of "$d" A)
  case "$s" in OK|SCF_NOT_CONVERGED) ;; *) echo "ⓐ 상태 $s (정상 종료·유한 상태 아님)"; return 1;; esac
  [ -s "$d/WAVECAR" ] || { echo "ⓐ WAVECAR 없음·빈 파일"; return 1; }
  for k in NKPTS NBANDS ENCUT; do
    c=$(grep -o "\"$k\": \"[^\"]*\"" "$d/WAVECAR.info" 2>/dev/null | head -1 | sed 's/.*: "//; s/"$//')
    [ -n "$c" ] && [ "$c" = "$(out_num "$d" "$k")" ] || { echo "ⓐ WAVECAR.info 의 OUTCAR 사본 $k '$c' ≠ ⓐ OUTCAR 원문 '$(out_num "$d" "$k")'"; return 1; }
  done
  r=$(awk '{ if (match($0, /"head": "[^"]*"/)) print substr($0, RSTART + 9, RLENGTH - 10) }' "$d/WAVECAR.info"); set -- $r
  [ $# -ge 6 ] && [ "$4" = "$(out_num "$d" NKPTS)" ] && [ "$5" = "$(out_num "$d" NBANDS)" ] && \
    awk -v a="$6" -v b="$(out_num "$d" ENCUT)" 'BEGIN { exit !(b != "" && (a - b < 0.05) && (b - a < 0.05)) }' || { echo "ⓐ WAVECAR 머리 ($r) ≠ OUTCAR NKPTS/NBANDS/ENCUT"; return 1; }
  [ "$(h "$d/WAVECAR")" = "$(wsha "$d/WAVECAR.info" sha256)" ] || { echo "ⓐ WAVECAR 가 기록 뒤 바뀌었다"; return 1; }
  return 0
}
two_stage(){ # $1 잡 · $2 시도 폴더 · $3 ⓐ 단 · $4 ⓑ 단 → FINAL · 반환 0 OK · 1 값 없음/다음 단 후보 · 6 공통 환경 고장
  local job=$1 d=$2 ra=$3 rb=$4 r why
  if [ ! -d "$d/stageA" ]; then run_one "$job" "$ra" "$d/stageA" "INCAR.$ra"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }; fi
  [ -f "$d/stageA/attempt.json" ] || { FINAL=INCOMPLETE_ATTEMPT; return 1; }
  if [ ! -d "$d/.b" ]; then
    why=$(elig_A "$d/stageA") || { FINAL=STAGE_A_INELIGIBLE; log "$job $rb: ⓐ 자격 미달 — $why · ⓑ 를 띄우지 않는다"; return 1; }
    run_one "$job" "$rb" "$d" "INCAR.$rb" "$d/stageA/WAVECAR"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }
  fi
  FINAL=$(stat_of "$d" "$rb")
  [ "$FINAL" = OK ]
}

# ── 사다리 ──
FINAL=""
drop_wav(){ # $1 ⓐ 폴더 — ⓐ WAVECAR 는 그 잡이 **끝난** 상태에서만 지운다. 0 스텝 중단 기록 뒤 이어 돌리기 · 1저자 검토 (재시작 미이행 → 다음 단) 가
  #           ⓐ 를 다시 계산하지 않고 쓸 수 있게 미확인·재시작 미이행·기록 없음·준비 실패에서는 남긴다 (반송은 안 한다)
  case "$FINAL" in INCOMPLETE_ATTEMPT|RESTART_NOT_HONOURED|SCF_UNVERIFIED|PREP_FAILED) log "… $1/WAVECAR 를 남긴다 ($FINAL — 검토·이어 돌리기용)";; *) rm -f "$1/WAVECAR";; esac
}
ladder(){ # $1 잡 → FINAL = 마지막 상태 · 반환 0 값 있음 · 1 값 없음 · 5 상한 · 6 공통 환경 고장
  local job=$1 s r
  if [ "$(ladder_of "$job")" = a4 ]; then
    if [ ! -d "run/${job}_a4" ]; then cap_ok "$job" || return 5; pp_ok "$job" || return 6; mkdir "run/${job}_a4" || { FINAL=PREP_FAILED; return 1; }; fi
    two_stage "$job" "run/${job}_a4" a4A a4B; r=$?; [ "$r" = 6 ] && return 6      # a4 는 한 번 (사다리 아님)
    drop_wav "run/${job}_a4/stageA"; return "$r"
  fi
  if [ ! -d "run/$job" ]; then cap_ok "$job" || return 5; pp_ok "$job" || return 6; run_one "$job" 0 "run/$job" INCAR; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }; fi
  s=$(stat_of "run/$job" 0)
  case "$s" in OK) FINAL=OK; return 0;; SCF_NOT_CONVERGED|RUN_FAILED) ;; *) FINAL=$s; return 1;; esac
  if [ ! -d "run/${job}_r1" ]; then pp_ok "$job" || return 6; mkdir "run/${job}_r1" || { FINAL=PREP_FAILED; return 1; }; fi
  two_stage "$job" "run/${job}_r1" r1A r1B; r=$?
  [ "$r" = 6 ] && return 6
  if [ "$r" = 0 ]; then drop_wav "run/${job}_r1/stageA"; return 0; fi
  case "$FINAL" in SCF_NOT_CONVERGED|RUN_FAILED) ;; *) drop_wav "run/${job}_r1/stageA"; return 1;; esac      # 미확인·자격 미달·재시작 미이행 = 자동 승격 없음
  if [ ! -d "run/${job}_r2" ]; then
    pp_ok "$job" || return 6
    [ -s "run/${job}_r1/stageA/WAVECAR" ] && elig_A "run/${job}_r1/stageA" > /dev/null || { FINAL=STAGE_A_INELIGIBLE; log "$job r2: r1 의 자격 있는 ⓐ WAVECAR 가 없다 — r2 를 띄우지 않는다"; return 1; }
    run_one "$job" r2B "run/${job}_r2" INCAR.r2B "run/${job}_r1/stageA/WAVECAR"; r=$?; [ "$r" = 6 ] && return 6; [ "$r" = 0 ] || { FINAL=PREP_FAILED; return 1; }
  fi
  FINAL=$(stat_of "run/${job}_r2" r2B); drop_wav "run/${job}_r1/stageA"
  [ "$FINAL" = OK ] && return 0 || return 1
}

rc_all=0
log "════ W_ad round2 · 단계 $STAGES · 잡 $(echo $SEL | wc -w) ════"
for job in $SEL; do
  [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }
  ladder "$job"; r=$?
  case "$r" in
    0) log "✓ $job ($FINAL)";;
    1) log "✗ $job 값 없음 ($FINAL)"; rc_all=1;;
    5) finish 5;;
    6) finish 6;;
  esac
done
finish "$rc_all"
'''


def run_all_text():
    return (RUN_ALL.replace("@RET_ALLOW@", "|".join(re.escape(x) for x in RETURN_ALLOWED))
            .replace("@RET_FORBID@", "|".join(re.escape(x) for x in RETURN_FORBIDDEN)).replace("@A4_JOB@", A4_JOB))


# ───────────────────────── 판정 계약 (러너 judge() 와 같은 규칙·같은 순서) ─────────────────────────
_NUM = re.compile(r"^[-+]?([0-9]+\.?[0-9]*|\.[0-9]+)([eE][-+]?[0-9]+)?$")
_ROW = re.compile(r"^[ \t]*(DAV|RMM|CG|SDA):")
_ION = re.compile(r"^[ \t]*[0-9]+[ \t]+F=")
STATUS_PROMOTE = ("SCF_NOT_CONVERGED", "RUN_FAILED")          # 다음 단 자격 (탄소 사다리) — 이 둘뿐


def _num(tok):
    """러너 awk 의 finite() 와 같다 — 정규식 (부호 · 소수 · e 지수) 통과 + 유한."""
    if tok is None or not _NUM.match(tok):
        return None
    x = float(tok)
    return x if math.isfinite(x) else None


def incar_val(text, tag):
    """러너 incar_val() 와 같다 — #·! 뒤 주석 · ';' 문장 구분 · 같은 태그면 마지막 값 · 키 공백 제거 · 값 앞뒤 공백 제거."""
    val = None
    for ln in text.splitlines():
        ln = re.split(r"[#!]", ln, maxsplit=1)[0]
        for st in ln.split(";"):
            if "=" not in st:
                continue
            k, v = st.split("=", 1)
            if re.sub(r"[ \t]", "", k).upper() == tag.upper():
                v = v.strip(" \t")
                if v != "":
                    val = v
    return val


def judge_text(osz, out, incar, rc):
    """→ (상태, 행수, dE 토큰, d eps 토큰, 사유) — 러너 judge() 의 awk 와 같은 규칙·같은 순서 (selftest 가 같은 탐침 집합으로 대조).

    확정 모순은 rc 보다 먼저 거부한다 (CZ Q-CZ-1 · 2026-10-22): 실행 머리줄 ≥ 2 · 끝까지 쓰인 OUTCAR 의 머리줄 ≠ 1 또는 마지막 반복 번호 ≠ N ·
    안 끝난 OUTCAR 의 반복 번호 > N + 1. 안 끝난 OUTCAR 의 번호 없음 · ≤ N + 1 은 결측 (잘림 · 스텝 도중 충돌) 이라 RUN_FAILED 를 허용한다
    (비준 정책 '전자 스텝 ≥ 1 뒤 충돌 = 실행 실패' 유지 · 판정 근거 파일 OSZICAR 쪽 결측은 봐주지 않는다)."""
    n, ion, bad, de, dp = 0, False, "", "", ""
    for ln in (osz or "").splitlines():
        if _ION.match(ln):
            ion = True
            continue
        if _ROW.match(ln):
            n += 1
            t = ln.split()
            k = t[1] if len(t) > 1 else ""
            if not bad:
                if ion:
                    bad = "rows_after_ion_summary"
                elif not (re.fullmatch(r"[0-9]+", k) and int(k) == n):
                    bad = "step_numbering"
            de, dp = (t[3], t[4]) if len(t) >= 5 else ("", "")
    out = out or ""
    term = "General timing and accounting" in out
    nrun = len(re.findall(r"(?m)^[ \t\r\f\v]*vasp\.[0-9]", out))
    it = re.findall(r"Iteration +[0-9]+\( *([0-9]+)\)", out)
    oit = int(it[-1]) if it else None
    nelm, ediff = incar_val(incar or "", "NELM"), incar_val(incar or "", "EDIFF")
    na = lambda x: x if x != "" else "NA"
    if n == 0:
        return "SCF_UNVERIFIED", 0, "NA", "NA", "no_rows"
    if bad:
        return "SCF_UNVERIFIED", n, "NA", "NA", bad
    if not (nelm and re.fullmatch(r"[0-9]+", nelm)):
        return "SCF_UNVERIFIED", n, "NA", "NA", "nelm_unknown"
    if n > int(nelm):
        return "SCF_UNVERIFIED", n, "NA", "NA", "n_gt_nelm"
    if nrun >= 2:
        return "SCF_UNVERIFIED", n, "NA", "NA", "run_blocks"
    if term:
        if nrun != 1:
            return "SCF_UNVERIFIED", n, "NA", "NA", "run_blocks"
        if oit != n:
            return "SCF_UNVERIFIED", n, "NA", "NA", "outcar_oszicar_mismatch"
    elif oit is not None and oit > n + 1:
        return "SCF_UNVERIFIED", n, "NA", "NA", "outcar_oszicar_mismatch"
    if rc != 0 or not term:
        return "RUN_FAILED", n, na(de), na(dp), "rc_or_not_terminated"
    a, b = _num(de), _num(dp)
    if a is None or b is None:
        return "SCF_UNVERIFIED", n, na(de), na(dp), "nonfinite"
    e = _num(ediff)
    if e is None:
        return "SCF_UNVERIFIED", n, de, dp, "ediff_unknown"
    return ("OK" if abs(a) <= e and abs(b) <= e else "SCF_NOT_CONVERGED"), n, de, dp, "-"


def _read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def far_diag(out_text, area):
    """far 끝점 진단 (카드 §3 · 정보) — 마지막 dipolmoment z · 쌍극 보정 에너지 · E-fermi · ΔV = 180.95 × p_z / A (V)."""
    pz = V._last(r"dipolmoment\s+\S+\s+\S+\s+(\S+)\s+electrons", out_text)
    ec = V._last(r"dipol\+quadrupol energy correction\s+(\S+)", out_text)
    ef = V._last(r"E-fermi\s*:\s*(\S+)", out_text)
    p = V._tok_float(pz)
    return {"p_z_eA": p, "dipole_energy_correction_eV": V._tok_float(ec), "E_fermi_eV": V._tok_float(ef),
            "dV_step_V": (180.95 * p / area) if (p is not None and area) else None,
            "potential_step_lines": re.findall(r"(?m)^.*(?:potential step|step in potential|vacuum level).*$", out_text)[-3:]}


OPTB88_ECHO = {"PARAM1": (r"PARAM1\s*=\s*(\S+)", 0.1833333333, 1e-3), "PARAM2": (r"PARAM2\s*=\s*(\S+)", 0.22, 1e-3),
               "ZAB_VDW": (r"(?i)Zab_vdW\s*=\s*(\S+)", -0.8491, 1e-3), "AGGAC": (r"AGGAC\s*=\s*(\S+)", 0.0, 1e-4)}
# vdW 커널 상태 (CZ Q-CZ-5) — 준비 (복사본 sha · 등록부 대조) · 읽기 (등록부 kernel_read_regex) · 부재 · 재생성을 가른다
KERNEL_LINE_RE = re.compile(r"(?i)vdw.*kernel|kernel.*vdw")          # vdW 커널을 말하는 줄 — ⚠ 카드 §2.4 의 (?i)kernel|vdw_kernel 에서 좁혔다:
#                                                                     MPI·OS 경고 ('kernel module … not loaded') 가 커널 부재로 잡혀 전체 정지가 되는 오탐
KERNEL_REGEN_RE = re.compile(r"(?i)\b(recalc\w*|regenerat\w*|generat\w*|comput\w*|writ\w*)\b")   # 재생성 표지
KERNEL_BAD_RE = re.compile(r"(?i)\b(not|no|error|cannot|unable|fail\w*|missing|differ\w*)\b")      # 부정 표지


# ───────────────────────── 반송 검사 (시도 하나) ─────────────────────────
RUNG_DIR = {"0": "{job}", "r1A": "{job}_r1/stageA", "r1B": "{job}_r1", "r2B": "{job}_r2", "a4A": "{job}_a4/stageA", "a4B": "{job}_a4"}
OUTCAR_DIMS = (("NKPTS", r"NKPTS *= *([0-9.]+)"), ("NBANDS", r"NBANDS *= *([0-9.]+)"), ("ENCUT", r"ENCUT *= *([0-9.]+) eV"))   # 러너 out_num() 과 같은 패턴 · 마지막 값
RESTART_RX_CHARS = re.compile(r"^[A-Za-z0-9 _:.,=()|*+?^$/-]+$")   # 재시작 긍정 문구 regex — grep -E (러너) 와 python re (검사기) 에서 뜻이 같은 글자만


def outcar_dims(text):
    """ⓐ OUTCAR 원문 → NKPTS · NBANDS · ENCUT (문자열 · 없으면 None). WAVECAR.info 안의 `outcar` 사본은 러너가 같은 파일에서 베낀 것이라 근거가 아니다 (CZ Q-CZ-2 ③)."""
    return {k: (re.findall(p, text) or [None])[-1] for k, p in OUTCAR_DIMS}


def _read_raw(p):
    """줄바꿈을 바꾸지 않고 읽는다 — \\r 를 줄 끝으로 보지 않아 grep 과 줄 나눔이 같다 (_read 는 \\r · \\r\\n 을 \\n 으로 바꾼다)."""
    try:
        return open(p, encoding="utf-8", errors="replace", newline="").read()
    except OSError:
        return None


def restart_evidence(attdir, out_text=None):
    """시도 하나의 재시작 원문 증거 — OUTCAR Startparameter 줄 (입력 되울림 제외 · 마지막 줄) 의 ISTART · ICHARG · 'WAVECAR not read' ·
    regex 를 찾을 원문 (stdout.log + OUTCAR · 줄바꿈 그대로 — 러너 grep 과 같은 줄)."""
    if out_text is None:
        out_text = _read(os.path.join(attdir, "OUTCAR")) or ""
    ro, rs = (_read_raw(os.path.join(attdir, f)) or "" for f in ("OUTCAR", "stdout.log"))
    body = V._strip_incar_echo(out_text)[0] if out_text else ""
    return {"istart": V._last(r"^\s*ISTART\s*=\s*(\d+)\s+job", body), "icharg": V._last(r"^\s*ICHARG\s*=\s*(\d+)\s+charge", body),
            "not_read_phrase": "WAVECAR not read" in ro or "WAVECAR not read" in rs, "text": rs + "\n" + ro}


def _raw_text(attdir):
    """stdout.log + OUTCAR 원문 (줄바꿈 그대로) — 등록부 문구 regex 를 찾는 곳."""
    return (_read_raw(os.path.join(attdir, "stdout.log")) or "") + "\n" + (_read_raw(os.path.join(attdir, "OUTCAR")) or "")


def kernel_state(text):
    """원문 → (상태, 줄): vdW 커널을 말하는 줄에 재생성 표지가 있으면 "regenerated" · 부정 표지면 "not_read" · 그런 줄이 없으면 (None, None).
    ⚠ 표지는 넓다 — 업체 5.4.4 의 실제 긍정 문구에 'calculating' 같은 말이 있으면 거짓 경보다. 파일럿 원문을 보고 다시 정한다 (검사기만 바뀌고 묶음은 안 바뀐다)."""
    for ln in text.splitlines():
        if KERNEL_LINE_RE.search(ln):
            if KERNEL_REGEN_RE.search(ln):
                return "regenerated", ln.strip()
            if KERNEL_BAD_RE.search(ln):
                return "not_read", ln.strip()
    return None, None


def restart_regex_problems(rx):
    """재시작 긍정 문구 regex 가 러너 (grep -E · 줄 단위) 와 검사기 (python re.M) 에서 같은 뜻인지 — 문제 목록 (비면 통과).
    ⚠ 카드 §2.2 는 [ ] \\ 도 허용했는데 괄호 안 역슬래시 ([\\]]) · \\d · [[:space:]] 는 두 엔진에서 뜻이 갈려 뺐다 (구절 하나를 찾는 데는 필요 없다).
    빈 문자열에 맞는 regex (a* · |x · ^) 는 무엇에나 맞아서 구별을 못 한다."""
    if not RESTART_RX_CHARS.match(rx or ""):
        return ["허용 밖 글자 (괄호 표현 [ ] · 역슬래시 · 중괄호 · 탭 등)"]
    bad = []
    if "(?" in rx:
        bad.append("'(?' — 파이썬 확장 (ERE 에 없다)")
    try:
        if re.search(rx, "") is not None:
            bad.append("빈 문자열에 맞는다 (무엇에나 맞는다)")
    except re.error as e:
        bad.append(f"파이썬 컴파일 실패 ({e})")
    return bad


def audit_r2(o, job, rung):
    """OUTCAR 해석값 (입력 에코 제외) 대조 → (없는 키, 모순 목록, 근거). ⓐ 단은 퍼텐셜 보정을 끈 단이라 DIPOL 근거가 없어도 된다."""
    s = o["settings"]
    a_rung = rung in ("r1A", "a4A")
    exp = {"NIONS": job["nions"], "NELECT": job["nelect_expected"], "ENCUT": job["encut"], "ISMEAR": job["ismear"], "SIGMA": job["sigma"],
           "ISPIN": 1, "LDIPOL": "F" if a_rung else "T", "IDIPOL": 3}
    if job["method"] in ("pbed3", "v5"):
        exp.update({"IVDW": 12, "VDW_S6": V.D3_PARAMS["s6"], "VDW_S8": V.D3_PARAMS["s8"], "VDW_A1": V.D3_PARAMS["a1"], "VDW_A2": V.D3_PARAMS["a2"],
                    "VDW_RADIUS": V.VDW_RADIUS_A, "VDW_CNRADIUS": V.VDW_CNRADIUS_A})
    missing, bad = [], []
    for k, e in exp.items():
        v = s.get(k)
        if v is None:
            missing.append(k); continue
        if k == "SIGMA":
            ok = abs(v - e) <= V.SIGMA_ECHO_TOL + 1e-9
        elif k in ("ENCUT", "NELECT"):
            ok = abs(v - e) <= 0.05
        elif k in ("VDW_S6", "VDW_S8", "VDW_A1", "VDW_A2"):
            ok = abs(v - e) <= V.D3_PARAM_TOL + 1e-12
        elif k in ("VDW_RADIUS", "VDW_CNRADIUS"):
            ok = abs(v - e) <= V.D3_RADIUS_TOL + 1e-12
        else:
            ok = v == e
        if not ok:
            bad.append(f"{k} {v} ≠ {e}")
    text = o.get("_body", "")
    if job["method"] == "optb88":
        iv = s.get("IVDW")
        if iv not in (None, 0):
            bad.append(f"IVDW {iv} ≠ 0 (optB88 에 D3 가 켜졌다)")
        for k, (pat, e, tol) in OPTB88_ECHO.items():
            v = V._tok_float(V._last(pat, text))
            if v is None:
                missing.append(k)
            elif abs(v - e) > tol:
                bad.append(f"{k} {v} ≠ {e}")
        if not re.search(r"(?i)LUSE_VDW\s*=\s*(T|\.TRUE\.)", text):
            missing.append("LUSE_VDW")
    gga, eg = V._last(r"^\s*GGA\s*=\s*(\S+)\s+GGA type", text), ("BO" if job["method"] == "optb88" else "PE")   # 실제 교환함수 (5.4.4 꼴 '   GGA     =    PE    GGA type')
    if gga is None:
        missing.append("GGA")
    elif gga.upper() != eg:
        bad.append(f"GGA {gga} ≠ {eg} (실제 교환함수)")
    nelm = V._tok_float(V._last(r"^\s*NELM\s*=\s*(\d+)", text))
    if nelm is None:
        missing.append("NELM")
    elif int(nelm) != NELM_RUNG[rung]:
        bad.append(f"NELM {int(nelm)} ≠ {NELM_RUNG[rung]}")
    if rung in ("r1B", "r2B", "a4B"):
        # ISTART·ICHARG 되울림은 설정 모순이 아니라 재시작 확인 (check_attempt → RESTART_NOT_HONOURED) 에서 본다
        amin = V._tok_float(V._last(r"^\s*AMIN\s*=\s*(\S+)", text))
        if amin is None:
            missing.append("AMIN")
        elif abs(amin - 0.01) > 1e-4:
            bad.append(f"AMIN {amin} ≠ 0.01")
    if rung == "r2B":
        m = re.findall(r"(?m)^\s*AMIX\s*=\s*(\S+);\s*BMIX\s*=\s*(\S+)", text)
        if not m:
            missing.append("AMIX/BMIX")
        elif abs(float(m[-1][0].rstrip(";")) - 0.1) > 1e-3 or abs(float(m[-1][1]) - 0.01) > 1e-4:
            bad.append(f"AMIX/BMIX {m[-1]} ≠ 0.1/0.01")
    got, dbad = V.dipol_evidence(o, job["dipol_z"])
    bad += dbad
    if not got and not dbad and not a_rung:
        missing.append("DIPOL")
    if s.get("EFIELD") is not None and abs(s["EFIELD"]) > 1e-12:
        bad.append(f"EFIELD {s['EFIELD']} (외부장 금지)")
    return missing, bad, {"DIPOL": got}


def check_attempt(job, pkgdir, attdir, rung, registry=None, a_ref=None):
    """한 시도 폴더 → 상태 dict (V5 check_job 순서: 실행 기록 결박 → 입력 무결성 → 있는 증거의 모순 → 판정 계약 → 재시작 → 완결성).
    ⓑ 단 (r1B · r2B · a4B) 은 a_ref (그 ⓑ 가 읽은 ⓐ 의 검사 기록) 를 꼭 받는다 — ⓑ 원본 sha 가 그 ⓐ 의 기록된 WAVECAR sha 여야 한다 (없으면 재시작 미이행).
    등록부에 restart_read_regex 가 있으면 ⓑ 원문 (OUTCAR + stdout.log) 에서 다시 찾는다 (러너의 honoured 를 믿지 않는다)."""
    r = {"dir": os.path.relpath(attdir, os.path.dirname(os.path.dirname(attdir))) if attdir else None, "rung": rung}

    def done(status, why=None, **kw):
        r["status"] = status
        if why:
            r["why"] = why
        r.update(kw)
        return r
    if not os.path.isdir(attdir):
        return done("MISSING")
    if not os.path.isfile(os.path.join(attdir, "attempt.json")):
        return done("INCOMPLETE_ATTEMPT", "attempt.json 없음 — 끝나지 않은 시도 (0 스텝 중단이면 업체 기록 · 아니면 1저자)")
    try:
        a = json.load(open(os.path.join(attdir, "attempt.json"), encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return done("ATTEMPT_MISMATCH", f"attempt.json 읽기 실패 {e}")
    if not isinstance(a, dict) or a.get("job") != job["dir"] or str(a.get("attempt")) != rung or a.get("stage") != job["stage"] or not isinstance(a.get("sha256"), dict):
        return done("ATTEMPT_MISMATCH", "attempt.json 의 잡·단·단계·sha 형식")
    rid, t0, t1, rc = a.get("run_id"), a.get("t_start"), a.get("t_end"), a.get("rc")
    isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
    if not (isinstance(rid, str) and V.RUN_ID_RE.match(rid)) or not (isint(t0) and isint(t1) and t1 >= t0) or not isint(rc):
        return done("ATTEMPT_MISMATCH", f"실행 기록 형식 (run_id {rid!r} · t {t0!r}→{t1!r} · rc {rc!r})")
    files = ("INCAR", "POSCAR", "KPOINTS", "OUTCAR", "OSZICAR") + (("WAVECAR.info",) if rung != "0" else ())
    for f in files:
        p = os.path.join(attdir, f)
        if (a["sha256"].get(f) or "") != (_sha(p) if os.path.isfile(p) else ""):
            return done("ATTEMPT_MISMATCH", f"{f} 가 실행 기록(attempt.json)과 다르다")
    r.update({"run_id": rid, "rc": rc, "wall_s": t1 - t0, "attempt_json_sha256": _sha(os.path.join(attdir, "attempt.json")),
              "outcar_sha256": str(a["sha256"].get("OUTCAR") or ""), "kernel_sha256": a.get("kernel_sha256") or None})
    for f in ("POSCAR", "KPOINTS"):
        if _sha(os.path.join(attdir, f)) != job["files_sha256"][f]:
            return done("INPUT_MODIFIED", f)
    inc_name = job["rungs"][rung]["incar"]
    ours, e0 = V.parse_incar_strict(open(os.path.join(pkgdir, "jobs", job["dir"], inc_name), encoding="utf-8").read())
    incar_text = open(os.path.join(attdir, "INCAR"), encoding="utf-8", errors="replace").read()
    ran, e1 = V.parse_incar_strict(incar_text)
    extra = {k: v for k, v in ran.items() if k not in ours}
    badperf = [k for k, v in extra.items() if k not in V.PERF_TAGS or not V.perf_value_ok(k, v)]
    diff = [k for k in ours if ran.get(k) != ours[k]]
    if e0 or e1 or badperf or diff:
        return done("INPUT_MODIFIED", f"INCAR 문법 {e1[:3]} · 다른 태그 {diff} · 허용 밖 추가 {badperf}")
    out_text = _read(os.path.join(attdir, "OUTCAR")) or ""
    o = V.parse_outcar(out_text) if out_text else None
    if o:
        o["_body"] = V._strip_incar_echo(out_text)[0]
        r.update({k: v for k, v in o.items() if k not in ("settings", "_body")}); r["settings"] = o["settings"]
    # ── ① 있는 증거의 모순 (POTCAR · 버전 · 설정 · D3 · 커널) ──
    tp, sp_, spp = (os.path.join(attdir, f) for f in ("POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"))
    if not all(os.path.isfile(x) for x in (tp, sp_, spp)):
        return done("POTCAR_UNVERIFIED", "POTCAR 기록 (titel · sha256 · species.sha256) 결측")
    psha = open(sp_, encoding="utf-8").read().strip().lower()
    sps = [l.split() for l in open(spp, encoding="utf-8").read().splitlines() if l.strip()]
    if not V.HEX64.match(psha) or psha != str(a["sha256"].get("POTCAR", "")).lower() or [x[0] for x in sps] != job["potcar_spec"] \
            or any(len(x) != 2 or not V.HEX64.match(x[1].lower()) for x in sps):
        return done("POTCAR_UNVERIFIED", "POTCAR sha 형식·순서·실행 기록 불일치")
    r["potcar_species_sha256"] = {x[0]: x[1].lower() for x in sps}; r["potcar_sha256"] = psha
    conflicts = []
    titel, zv = V.parse_titel(open(tp, encoding="utf-8", errors="replace").read())
    exp_t = [registry["titel"][p] for p in job["potcar_spec"]] if registry else job["pp_expected_titel"]
    if titel != exp_t or [round(x, 3) for x in zv] != [round(x, 3) for x in job["zval_expected"]]:
        conflicts.append(("POTCAR_MISMATCH", f"POTCAR.titel {titel} · ZVAL {zv} (기대 {exp_t})"))
    ot = o["outcar_titel"] if o else []
    if ot and ot != titel and not (len(ot) < len(titel) and titel[:len(ot)] == ot):
        conflicts.append(("POTCAR_MISMATCH", f"OUTCAR TITEL {ot} ≠ POTCAR.titel {titel}"))
    if registry:
        if any(registry["species_sha256"].get(k) != v for k, v in r["potcar_species_sha256"].items()):
            conflicts.append(("POTCAR_MISMATCH", "봉인 등록부의 종별 sha 와 다르다"))
        if o and o["version"] and o["version"] != registry["vasp_version"]:
            conflicts.append(("VERSION_MISMATCH", f"VASP {o['version']!r} ≠ 등록부"))
        if job["method"] == "optb88" and r["kernel_sha256"] != registry.get("kernel_sha256"):
            conflicts.append(("KERNEL_MISMATCH", f"vdW 커널 sha {r['kernel_sha256']} ≠ 등록부"))
    if job["method"] == "optb88":
        ktext = _raw_text(attdir)
        kst, kln = kernel_state(ktext)
        krx = (registry or {}).get("kernel_read_regex") or ""
        r["kernel_state"] = kst or ("read" if krx and not restart_regex_problems(krx) and re.search(krx, ktext, re.M) else "unconfirmed")
        if kst:
            conflicts.append(("KERNEL_NOT_READ", f"vdW 커널 {kst} — {kln[:120]!r} (커널 줄에 부재·재생성 표지)"))
    missing, bad, src = audit_r2(o, job, rung) if o else ([], [], {})
    if bad:
        conflicts.append(("SETTINGS_MISMATCH", "; ".join(bad)))
    ref = fin(job.get("d3_2body_eV_ref"))
    if o and ref is not None and o["Edisp_eV"] is not None and abs(o["Edisp_eV"] - ref) > V.D3_REL_TOL * abs(ref):
        conflicts.append(("D3_MISMATCH", f"Edisp {o['Edisp_eV']:.4f} vs ref {ref:.4f} eV (>1 %)"))
    if conflicts:
        return done(conflicts[0][0], conflicts[0][1], conflicts=[f"{s_}: {w}" for s_, w in conflicts])
    # ── ② 판정 계약 (러너와 같다) ──
    st, n, de, dp, why = judge_text(_read(os.path.join(attdir, "OSZICAR")), out_text, incar_text, rc)
    r["judge"] = {"status": st, "n_elec_steps": n, "dE": de, "d_eps": dp, "why": why}
    if rung in ("r1A", "a4A"):
        wi = _read(os.path.join(attdir, "WAVECAR.info"))
        try:
            w = json.loads(wi) if wi else None
        except ValueError:
            w = None
        r["wavecar"] = w
        r["outcar_dims"] = outcar_dims(out_text)
    if rung in ("r1B", "r2B", "a4B"):
        wi = _read(os.path.join(attdir, "WAVECAR.info"))
        try:
            w = json.loads(wi) if wi else None
        except ValueError:
            w = None
        ev = restart_evidence(attdir, out_text)
        ist, ich, notread = ev["istart"], ev["icharg"], ev["not_read_phrase"]
        a_sha = str(((a_ref or {}).get("wavecar") or {}).get("sha256") or "")
        rx = (registry or {}).get("restart_read_regex") or ""
        rxbad = restart_regex_problems(rx) if rx else []
        pos = (not rxbad and re.search(rx, ev["text"], re.M) is not None) if rx else None
        r["restart"] = {"record": w, "outcar_istart": ist, "outcar_icharg": ich, "not_read_phrase": notread, "a_wavecar_sha256": a_sha or None,
                        "positive_regex": rx or None, "positive_regex_match": pos}
        if not (isinstance(w, dict) and w.get("honoured") == 1 and w.get("istart") == "1" and w.get("icharg") == "0" and w.get("not_read_phrase") == 0
                and ist == "1" and ich == "0" and not notread
                and V.HEX64.match(str(w.get("src_sha256", ""))) and w.get("src_sha256") == w.get("copied_sha256") == w.get("end_sha256")):
            return done("RESTART_NOT_HONOURED", f"ⓑ 가 ⓐ WAVECAR 를 읽었다고 확인할 수 없다 (OUTCAR ISTART {ist} · ICHARG {ich} · 'WAVECAR not read' {notread} · sha 셋) — "
                        "자동 채택·승격 없음 · 1저자 검토")
        if not (V.HEX64.match(a_sha) and w.get("src_sha256") == a_sha):
            return done("RESTART_NOT_HONOURED", f"ⓑ 원본이 이 ⓐ 의 WAVECAR 가 아니다 (ⓐ 기록 sha {a_sha or '없음'} · ⓑ src/copied/end {w.get('src_sha256')}) — "
                        "자동 채택·승격 없음 · 1저자 검토")
        if rx and not pos:
            return done("RESTART_NOT_HONOURED", (f"등록부 재시작 regex 형식 {rxbad}" if rxbad else f"등록부의 재시작 긍정 문구 /{rx}/ 가 ⓑ OUTCAR·stdout.log 원문에 없다")
                        + " — 자동 채택·승격 없음 · 1저자 검토")
    if st != "OK":
        return done(st, f"판정 계약 {why} (행 {n} · dE {de} · d eps {dp})")
    # ── ③ 완결성 (OK 만) ──
    r["settings_sources"] = src
    if job["method"] == "optb88" and r.get("kernel_state") != "read":
        krx = (registry or {}).get("kernel_read_regex") or ""
        return done("KERNEL_UNVERIFIED", f"등록부 커널 읽기 문구 /{krx}/ 가 OUTCAR·stdout 원문에 없다" if krx else
                    "vdW 커널 읽기 확인 미완 — 파일럿 원문으로 확정한 문구 (등록부 kernel_read_regex) 가 아직 없다 (CZ: 확정 전에는 읽었다고 하지 않는다)")
    if not o or not o["outcar_titel"] or len(o["outcar_titel"]) < len(titel):
        return done("POTCAR_UNVERIFIED", "성공한 실행인데 OUTCAR TITEL 이 없거나 앞부분만 있다")
    if any(k in missing for k in ("NIONS", "NELECT")):
        return done("SYSTEM_UNVERIFIED", f"OUTCAR 에 {missing} 없음")
    if missing:
        return done("SETTINGS_UNVERIFIED", f"해석값을 못 읽음: {missing} (파일럿 원문으로 파서 확인)")
    if o["TOTEN_eV"] is None or o["E_sigma0_eV"] is None:
        return done("ENERGY_UNPARSEABLE", "마지막 FREE ENERGIE 구획의 TOTEN·E(σ→0) 가 없다")
    if job["method"] != "optb88" and (ref is None or o["Edisp_eV"] is None):
        return done("D3_UNVERIFIED", "D3 기대값 또는 Edisp 없음")
    return done("OK")


ENV_CLASS = ("VERSION_MISMATCH", "POTCAR_MISMATCH", "KERNEL_MISMATCH", "KERNEL_NOT_READ")   # 환경 등급 — 어느 시도에서 나오든 전체 정지 (CZ Q-CZ-3 · Q-CZ-5)
ENV_SPLIT = ("VERSION_INCONSISTENT", "POTCAR_INCONSISTENT", "KERNEL_INCONSISTENT")     # 시도 사이 갈림 — 어느 쪽이 맞는지 모르므로 전부 막는다
COMMON_ENV = ENV_CLASS + ENV_SPLIT
INTEGRITY = ("ATTEMPT_MISMATCH", "INPUT_MODIFIED", "POTCAR_UNVERIFIED", "INCOMPLETE_ATTEMPT", "MISSING")   # 무결성 실패 (파일럿 결박 대조보다 먼저 이름 붙는다)
A_TOLERATED = ("SETTINGS_UNVERIFIED", "ENERGY_UNPARSEABLE", "D3_UNVERIFIED", "KERNEL_UNVERIFIED")   # ⓐ (WAVECAR 만 만드는 단) 에서는 자격을 막지 않는 결측
SEAL_PASS = ("OK", "SCF_NOT_CONVERGED", "RUN_FAILED", "SCF_UNVERIFIED", "RESTART_NOT_HONOURED",   # 봉인을 막지 않는 시도 상태 (정상 · 물리 실패 ·
             "KERNEL_UNVERIFIED")                                                                  #  등록부가 커널 문구를 정하기 전의 optB88 수렴 시도)
LADDER_RUNGS = {"carbon": ("0", "r1A", "r1B", "r2B"), "a4": ("a4A", "a4B")}
RA_OF = {"r1B": "r1A", "r2B": "r1A", "a4B": "a4A"}       # ⓑ 단 → 그 ⓑ 가 읽은 ⓐ 단 (r2 는 r1 의 ⓐ WAVECAR 를 쓴다)
AB_RE = re.compile(r"^(.+)_(0|r1A|r1B|r2B|a4A|a4B)_([0-9]+)$")   # run_aborted/<잡>_<단>_<k> (러너 --infra-abort)


def a_eligible(ra):
    """ⓐ 자격 (ⓑ 를 띄우기 전 셋 중 기록으로 볼 수 있는 둘 — ① 정상 종료·유한 상태 ② WAVECAR 0 보다 크고 머리 = ⓐ OUTCAR NKPTS·NBANDS·ENCUT).
    ② 의 OUTCAR 값은 check_attempt 가 반송된 ⓐ OUTCAR 원문에서 다시 읽은 `outcar_dims` 다 — WAVECAR.info 의 `outcar` 사본은 그것과 같아야 할 뿐 근거가 아니다 (러너 elig_A 와 같다)."""
    j = ra.get("judge") or {}
    if ra.get("status") not in ("OK", "SCF_NOT_CONVERGED") and j.get("status") not in ("OK", "SCF_NOT_CONVERGED"):
        return False, f"ⓐ 상태 {ra.get('status')} / 판정 {j.get('status')}"
    if ra.get("status") not in ("OK", "SCF_NOT_CONVERGED") + A_TOLERATED:
        return False, f"ⓐ 무결성·설정 {ra.get('status')}"
    w = ra.get("wavecar") or {}
    hd = str(w.get("head", "")).split()
    dims = ra.get("outcar_dims") or {}
    if any(dims.get(k) is None for k, _ in OUTCAR_DIMS):
        return False, f"ⓐ OUTCAR 원문에서 NKPTS·NBANDS·ENCUT 를 못 읽었다 {dims}"
    oc = w.get("outcar") if isinstance(w.get("outcar"), dict) else {}
    if any(oc.get(k) != dims[k] for k, _ in OUTCAR_DIMS):
        return False, f"WAVECAR.info 의 OUTCAR 사본 {oc} 이 실물 ⓐ OUTCAR {dims} 와 다르다"
    try:
        ok = (int(w.get("size", 0)) > 0 and len(hd) >= 6 and hd[3] == dims["NKPTS"] and hd[4] == dims["NBANDS"]
              and abs(float(hd[5]) - float(dims["ENCUT"])) < 0.05)
    except (TypeError, ValueError):
        ok = False
    return (True, "-") if ok else (False, f"WAVECAR 머리 {hd[3:6]} · 크기 {w.get('size')} ≠ ⓐ OUTCAR {dims}")


def _started(d):
    """시도가 시작됐나 — run_one 은 폴더를 차지한 뒤 맨 먼저 INCAR 를 놓고 끝에 attempt.json 을 쓴다 (r1B · a4B 의 폴더는 ⓐ 의 부모라 폴더만으로는 모른다)."""
    return os.path.isfile(os.path.join(d, "attempt.json")) or os.path.isfile(os.path.join(d, "INCAR"))


def env_audit(attempts):
    """[(꼬리표, 검사 기록)] → [(꼬리표, 등급, 사유)] (비면 깨끗하다) — CZ Q-CZ-3: 채택 시도만이 아니라 모든 시도를 본다.
    ① 시도마다 환경 등급 모순 — status 와 conflicts 목록 둘 다 (check_attempt 는 첫 모순만 status 로 올린다)
    ② 시도 사이 VASP 버전 · PP 종별 sha · vdW 커널 sha 갈림.
    ⚠ 못 하는 것: 무결성 검사에서 먼저 멈춘 시도 (ATTEMPT_MISMATCH 등) 는 버전·PP 를 읽지 않아 ② 에 안 들어간다 — 그 시도는 무결성으로 따로 막힌다."""
    out, by = [], {"VERSION_INCONSISTENT": {}, "POTCAR_INCONSISTENT": {}, "KERNEL_INCONSISTENT": {}}
    for tag, r in attempts:
        seen = set()
        for c in [f"{r.get('status')}: {r.get('why', '')}"] + list(r.get("conflicts") or []):
            k, _, w = c.partition(":")
            if k in ENV_CLASS and k not in seen:
                seen.add(k); out.append((tag, k, w.strip()))
        for sp, hh in (r.get("potcar_species_sha256") or {}).items():
            by["POTCAR_INCONSISTENT"].setdefault(f"POTCAR {sp}", {}).setdefault(hh, []).append(tag)
        if r.get("version"):
            by["VERSION_INCONSISTENT"].setdefault("VASP 버전", {}).setdefault(r["version"], []).append(tag)
        if r.get("kernel_sha256"):
            by["KERNEL_INCONSISTENT"].setdefault("vdW 커널 sha", {}).setdefault(r["kernel_sha256"], []).append(tag)
    for cls, keys in by.items():
        for key, vals in sorted(keys.items()):
            if len(vals) > 1:
                out.append(("시도 사이", cls, f"{key} 가 갈린다 — " + " · ".join(f"{v[:40]} ← {sorted(ts)[:4]}" for v, ts in sorted(vals.items()))))
    return out


def aborted_attempts(J, pkgdir, ret, registry=None):
    """0 스텝 인프라 중단으로 run_aborted/ 에 옮긴 시도 중 attempt.json 이 있는 것 → [(꼬리표, 검사 기록)] — 환경 감사에만 쓴다 (사다리 · 값에는 안 쓴다)."""
    base = ret if os.path.isdir(os.path.join(ret, "run")) else os.path.dirname(os.path.abspath(ret))
    ab, found = os.path.join(base, "run_aborted"), []
    for name in (sorted(os.listdir(ab)) if os.path.isdir(ab) else []):
        m, d = AB_RE.match(name), os.path.join(ab, name)
        if m and m.group(1) in J and os.path.isfile(os.path.join(d, "attempt.json")):
            found.append((f"{m.group(1)}/{m.group(2)}@aborted{m.group(3)}", check_attempt(J[m.group(1)], pkgdir, d, m.group(2), registry)))
    return found


def resolve_job(job, pkgdir, run, registry=None):
    """잡 하나의 사다리 → 채택 결과 (+ 이력 · 모든 시도 `attempts`). 탄소: 단 0 → (미수렴·실행 실패면) r1 ⓐ+ⓑ → (그래도면) r2 ⓑ · a4: ⓐ+ⓑ 한 번.
    OK = 그 잡의 모든 시도가 무결성 · 환경 · 결박 검사를 통과했고 채택 시도가 수렴했다 (V5 adopt_a4 가 이 OK 를 그대로 믿는다 — CZ Q-CZ-8):
    · 환경 등급 모순 · 시도 사이 갈림은 어느 시도에서 나오든 (사다리가 안 지나간 단도) 최종 상태를 덮는다 (원래 값은 adopted_status · 단은 env_in)
    · 등록부가 있으면 파일럿 잡의 반송 시도 집합 · 단마다 run_id · attempt.json · OUTCAR sha 가 봉인과 같아야 한다 (아니면 PILOT_BINDING_MISMATCH ·
      시도 자체가 무결성 실패면 그 이름이 먼저다)."""
    P = lambda rung: os.path.join(run, RUNG_DIR[rung].format(job=job["dir"]))
    seen = {}

    def chk(rung):
        if rung not in seen:
            ref = chk(RA_OF[rung]) if rung in RA_OF else None
            seen[rung] = check_attempt(job, pkgdir, P(rung), rung, registry, a_ref=ref)
        return seen[rung]
    res = _walk(job, chk)
    att = {k: chk(k) for k in LADDER_RUNGS[job["ladder"]] if _started(P(k))}
    res["attempts"] = att
    orig = res["status"]
    if registry and job["dir"] in PILOT_JOBS and orig not in INTEGRITY:
        exp = ((registry.get("from_pilot") or {}).get(job["dir"]), (registry.get("from_pilot_sha256") or {}).get(job["dir"]))
        got = ({k: a.get("run_id") for k, a in att.items()},
               {k: {"attempt.json": a.get("attempt_json_sha256"), "OUTCAR": a.get("outcar_sha256")} for k, a in att.items()})
        if got != exp:
            res.update(status="PILOT_BINDING_MISMATCH", why=f"파일럿 반송 시도가 봉인과 다르다 — 단·run_id 반송 {got[0]} · 봉인 {exp[0]} (attempt.json · OUTCAR sha 도 대조)")
    env = env_audit(list(att.items()))
    if env:
        res.update(status=env[0][1], why=f"환경 감사 — {env[0][0]}: {env[0][2]}", env_in=[list(e) for e in env])
    if res["status"] != orig:
        res["adopted_status"] = orig
    return res


def _walk(job, chk):
    """사다리 채택 규칙 (CZ 전과 같다) — chk(단) 은 그 단의 검사 기록 (ⓑ 는 자기 ⓐ 기록에 결박돼 있다)."""
    hist = {}
    if job["ladder"] == "a4":
        ra = chk("a4A"); hist["a4A"] = ra["status"]
        if ra["status"] == "MISSING":
            return {"status": "MISSING", "history": hist}
        ok, why = a_eligible(ra)
        if not ok:
            return {"status": "STAGE_A_INELIGIBLE", "why": why, "history": hist, "stageA": ra}
        rb = chk("a4B"); hist["a4B"] = rb["status"]
        return {**rb, "history": hist, "stageA": ra}
    r0 = chk("0"); hist["0"] = r0["status"]
    if r0["status"] == "OK" or r0["status"] not in STATUS_PROMOTE:
        return {**r0, "history": hist}
    last = r0
    for ra_name, rb_name in (("r1A", "r1B"), (None, "r2B")):
        if ra_name:
            ra = chk(ra_name); hist[ra_name] = ra["status"]
            if ra["status"] == "MISSING":
                return {**last, "history": hist, "ladder_note": "다음 단 시도 없음"}
            ok, why = a_eligible(ra)
            if not ok:
                return {"status": "STAGE_A_INELIGIBLE", "why": why, "history": hist}
        rb = chk(rb_name); hist[rb_name] = rb["status"]     # r1B · r2B 둘 다 r1 ⓐ 에 결박 (RA_OF)
        if rb["status"] == "MISSING":
            return {**last, "history": hist, "ladder_note": "다음 단 시도 없음"}
        if rb["status"] == "OK" or rb["status"] not in STATUS_PROMOTE:
            return {**rb, "history": hist}
        last = rb
    return {**last, "history": hist}


# ───────────────────────── 집계 (카드 §2 · §4 · §4d) ─────────────────────────
G3_DW = G4_DW = 0.01                  # 카드 G3·G4 (탄소) — 은 쪽 0.02 의 절반
TRIG_DW = 0.8 * 0.01                  # 선택 2 발동 규칙 (PASS 인데 |ΔW| > 0.008 → Li_A/PBE 에 더하거나 1저자가 닫는다)
G5C_PER, G5C_BIAS = 0.03, 0.02        # 카드 G5_C — 표본 |Δ_C| · 종결별 signed bias |mean Δ_C|
DELTA_PCT_LABEL = 20.0                # δ 라벨 — 백분율 > 20 % 면 '함수 선택 (XC+vdW) 민감'
SIG_PZ, SIG_PBE = 0.02, 0.001         # far 전하이동 신호 ⓐ |Δp_z| e·Å · ⓑ G3 (ii) PBE 몫 J/m² (우리 제안 · CZ 확인 대상)
SAMPLES = {"S_A": ("P2S_S_A_bound", "P2S_S_A_far"), "S_A_p05": ("P2S_S_A_p05_bound", "P2S_S_A_far"),
           "Li_A": ("P2S_Li_A_bound", "P2S_Li_A_far"), "Li_A_p05": ("P2S_Li_A_p05_bound", "P2S_Li_A_far")}
GROUPS = {"s_outer": ("S_A", "S_A_p05"), "li_outer": ("Li_A", "Li_A_p05")}
G3_PAIRS = {"i": ("P2S_S_A_G3_c2_bound", "P2S_S_A_G3_c2_far_i"), "ii": ("P2S_S_A_G3_c2_bound", "P2S_S_A_G3_c2_far_ii")}
G4_PAIRS = {"k62": ("P2S_S_A_G4_k62_bound", "P2S_S_A_G4_k62_far"), "k62s2": ("P2S_S_A_G4_k62s2_bound", "P2S_S_A_G4_k62s2_far"),
            "e650": ("P2S_S_A_G4_e650_bound", "P2S_S_A_G4_e650_far")}
G4_STEPS = (("k", "k62", None, "Γ6×2 σ − Γ3×2 σ"), ("sigma", "k62s2", "k62", "Γ6×2 σ/2 − Γ6×2 σ"), ("encut", "e650", None, "ENCUT 650 − 520 (Γ3×2 σ)"))
DELTA_PAIRS = {"S_A": ("P2S_S_A_optB88_bound", "P2S_S_A_optB88_far"), "Li_A": ("P2S_Li_A_optB88_bound", "P2S_Li_A_optB88_far")}
CC_PAIRS = {"pbed3": ("CC_S33_AB_pbed3_bound", "CC_S33_AB_pbed3_far"), "optb88": ("CC_S33_AB_optB88_bound", "CC_S33_AB_optB88_far")}
UMA_NAMES = ("S_A_bound", "S_A_far", "S_A_p05_bound", "Li_A_bound", "Li_A_far", "Li_A_p05_bound")
UMA_G3 = ("S_A_G3_c2_bound", "S_A_G3_c2_far_i", "S_A_G3_c2_far_ii")
def collect(out, ret, manifest_sha256, uma=None, registry=None):
    """반송 → 잡별 채택 결과 · W · Δ_C · G3 · G4 · G5_C · δ · ②′ · far 진단 · 신호 · 80 % 발동 · 질문별 실패 전파. 판정은 카드 문턱 그대로."""
    V.verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    J = {j["dir"]: j for j in meta["jobs"]}
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    res = {n: resolve_job(j, out, run, registry) for n, j in J.items()}
    # 전역 환경 감사 (CZ Q-CZ-3) — 모든 잡의 모든 시도 (채택 시도만이 아니다) + 0 스텝 중단으로 옮긴 시도. 하나라도 걸리면 공통 환경 고장 (전체 정지 · 종료 6)
    genv = env_audit([(f"{n}/{k}", a) for n, r in res.items() for k, a in (r.get("attempts") or {}).items()] + aborted_attempts(J, out, ret, registry))
    for n, r in res.items():
        if r["status"] == "OK" and genv:
            r.update(adopted_status="OK", status=genv[0][1], why=f"전역 환경 감사 — {genv[0][0]}: {genv[0][2]}")
    common = [f"{t} {c}: {w}"[:300] for t, c, w in genv]
    ok = lambda n: res.get(n, {}).get("status") == "OK"
    E = lambda n, k="TOTEN_eV": fin(res[n].get(k)) if ok(n) else None

    def W(b, f, k="TOTEN_eV"):
        eb, ef = E(b, k), E(f, k)
        return None if eb is None or ef is None else (ef - eb) * V.EV_J / (J[b]["area_A2"] * V.A2_M2)
    dref = lambda b, f: (J[f]["d3_2body_eV_ref"] - J[b]["d3_2body_eV_ref"]) * V.EV_J / (J[b]["area_A2"] * V.A2_M2)
    rec = {"schema": "wad_round2_collect/v1", "manifest_sha256": manifest_sha256, "card": CARD,
           "pp_registry": "검증됨" if registry else "없음 — 파일럿 단계 집계 (G5_C BLOCKED)",
           "energy_convention": "W = [TOTEN(far) − TOTEN(bound)]/A — Gaussian σ 0.05 eV TOTEN (탄소 규약) · 0 K 점착에너지·전자 자유에너지로 부르지 않는다",
           "common_environment_failure": common or None}
    # 표본 W (탄소 PBE+D3)
    smp = {}
    for k, (b, f) in SAMPLES.items():
        w, wd = W(b, f), W(b, f, "Edisp_eV")
        smp[k] = {"bound": b, "far": f, "W_J_m2": w, "W_sigma0_J_m2": W(b, f, "E_sigma0_eV"), "W_E0_noentropy_J_m2": W(b, f, "E_noentropy_eV"),
                  "dD3_VASP_J_m2": wd, "W_PBE_J_m2": (w - wd) if None not in (w, wd) else None, "dD3_ref_J_m2": dref(b, f),
                  "status": {"bound": res[b]["status"], "far": res[f]["status"]}}
    base = smp["S_A"]
    # G3 (S_A · PBE+D3)
    g3 = {"threshold": G3_DW, "d3_g3_budget": V.D3_G3_BUDGET}
    for tag, (b, f) in G3_PAIRS.items():
        wx, dx = W(b, f), W(b, f, "Edisp_eV")
        g3[f"dW_{tag}"] = (wx - base["W_J_m2"]) if None not in (wx, base["W_J_m2"]) else None
        g3[f"dD3_{tag}"] = (dx - base["dD3_VASP_J_m2"]) if None not in (dx, base["dD3_VASP_J_m2"]) else None
        g3[f"d3_diffdiff_{tag}"] = (g3[f"dD3_{tag}"] - (dref(b, f) - base["dD3_ref_J_m2"])) if g3[f"dD3_{tag}"] is not None else None
    if None in (g3["dW_i"], g3["dW_ii"], g3["d3_diffdiff_i"], g3["d3_diffdiff_ii"]):
        g3["status"] = "INCOMPLETE"
    elif max(abs(g3["d3_diffdiff_i"]), abs(g3["d3_diffdiff_ii"])) > V.D3_G3_BUDGET:
        g3["status"] = "INCOMPLETE (D3 차이의 차이 예산 초과)"
    else:
        g3["status"] = "PASS" if max(abs(g3["dW_i"]), abs(g3["dW_ii"])) <= G3_DW else "FAIL"
    # G4 (S_A · 같은 기하 → Edisp 같아야 한다)
    b0, f0 = SAMPLES["S_A"]
    g4 = {}
    Wv = {t: W(*p) for t, p in G4_PAIRS.items()}
    Wv[None] = base["W_J_m2"]
    for step, t, ref_t, lab in G4_STEPS:
        b, f = G4_PAIRS[t]
        dd = {ep: (E(x, "Edisp_eV") - E(x0, "Edisp_eV")) if None not in (E(x, "Edisp_eV"), E(x0, "Edisp_eV")) else None for ep, x, x0 in (("bound", b, b0), ("far", f, f0))}
        dw = (Wv[t] - Wv[ref_t]) if None not in (Wv[t], Wv[ref_t]) else None
        if dw is None or None in dd.values():
            st = "INCOMPLETE"
        elif max(abs(v) for v in dd.values()) > V.D3_SAME_GEOM_TOL_EV:
            st = f"INCOMPLETE (D3 불일치 — 같은 기하 Edisp 차 > {V.D3_SAME_GEOM_TOL_EV:g} eV)"
        else:
            st = "PASS" if abs(dw) <= G4_DW else "FAIL"
        g4[step] = {"variant": lab, "dW": dw, "d3_same_geom_diff_eV": dd, "status": st}
    st4 = [v["status"] for v in g4.values()]
    g4["status"] = "FAIL" if "FAIL" in st4 else ("INCOMPLETE" if any(x.startswith("INCOMPLETE") for x in st4) else "PASS")
    g4["info_total_k62s2_minus_base"] = (Wv["k62s2"] - Wv[None]) if None not in (Wv["k62s2"], Wv[None]) else None
    # 선택 2 발동 규칙 (결과 전 · 판정을 바꾸지 않는다)
    trig = [f"G3 {t} |ΔW| {abs(g3[f'dW_{t}']):.4f}" for t in ("i", "ii") if g3["status"] == "PASS" and abs(g3[f"dW_{t}"]) > TRIG_DW]
    trig += [f"G4 {s} |ΔW| {abs(v['dW']):.4f}" for s, v in g4.items() if isinstance(v, dict) and v.get("status") == "PASS" and abs(v["dW"]) > TRIG_DW]
    rec["trigger_80pct"] = {"triggered": bool(trig), "checks": trig, "rule": "PASS 했지만 |ΔW| > 0.008 J/m² — 그 검사를 Li_A/PBE 에 더하거나 1저자가 명시 결정으로 닫는다 (자동 실행 아님)"}
    # G5_C
    g5 = {"per_sample": G5C_PER, "bias": G5C_BIAS}
    uE, uerr = ({}, ["UMA 입력 없음"]) if uma is None else V.load_uma(uma, meta, list(UMA_NAMES))
    uG3, uerr3 = ({}, ["UMA 입력 없음"]) if uma is None else V.load_uma(uma, meta, list(UMA_G3))     # 3b′ 진단용 (정보 · 없으면 진단만 빠진다)
    dlt = {}
    for k, (b, f) in SAMPLES.items():
        sb, sf = J[b]["structure"], J[f]["structure"]
        wu = (uE[sf] - uE[sb]) * V.EV_J / (J[b]["area_A2"] * V.A2_M2) if (sb in uE and sf in uE) else None
        s = smp[k]
        dlt[k] = (s["W_J_m2"] - (wu + s["dD3_VASP_J_m2"])) if None not in (s["W_J_m2"], wu, s["dD3_VASP_J_m2"]) else None
        s.update({"W_UMA_J_m2": wu, "Delta_C_J_m2": dlt[k], "W_UMA_D3ref_J_m2": (wu + s["dD3_ref_J_m2"]) if wu is not None else None,
                  "dD3_VASP_minus_ref_J_m2": (s["dD3_VASP_J_m2"] - s["dD3_ref_J_m2"]) if s["dD3_VASP_J_m2"] is not None else None})
    by_t = {t: [dlt[k] for k in ks] for t, ks in GROUPS.items()}
    g5["signed_bias"] = {t: (sum(v) / len(v)) if None not in v else None for t, v in by_t.items()}
    g5["MAE_info"] = {t: (sum(abs(x) for x in v) / len(v)) if None not in v else None for t, v in by_t.items()}
    allv = list(dlt.values())
    g5["MAE_info"]["all"] = (sum(abs(x) for x in allv) / len(allv)) if None not in allv else None
    g5["dp05_minus_dA_info"] = {t: (dlt[ks[1]] - dlt[ks[0]]) if None not in (dlt[ks[0]], dlt[ks[1]]) else None for t, ks in GROUPS.items()}
    raw_ok = (None not in allv and all(abs(x) <= G5C_PER for x in allv) and all(abs(b_) <= G5C_BIAS for b_ in g5["signed_bias"].values()))
    if common:
        g5["status"] = f"BLOCKED (공통 환경 고장 {len(common)} 건 — {common[0][:120]})"
    elif uerr:
        g5["status"] = f"BLOCKED (UMA 입력: {uerr[:3]})"
    elif registry is None:
        g5["status"] = "BLOCKED (PP 등록부 없음 — 파일럿 단계)"
    elif None in allv:
        g5["status"] = f"INCOMPLETE (분모 4 중 {sum(x is not None for x in allv)} 유효)"
    elif g3["status"] != "PASS" or g4["status"] != "PASS":
        g5["status"] = f"INCOMPLETE (G3 {g3['status']} · G4 {g4['status']} — 오차표만 · 원시 기준 {'충족' if raw_ok else '미충족'})"
    else:
        g5["status"] = "PASS" if raw_ok else "FAIL"
    g5["raw_criteria_met"] = raw_ok
    g5["labels"] = ["VASP PAW · 코드가 P2 예측과 다르다", "Gaussian σ 0.05 eV TOTEN 규약", "S_A/PBE 대표 점검 — Li_A·optB88 수치 민감도 미검증 (선택 2)"]
    if g4.get("sigma", {}).get("status") != "PASS":
        g5["labels"].append("σ 확인 (G4 σ 단계 PASS) 전 — Δ_C 전부를 UMA 모델 오차로 읽지 않는다")
    if uG3 and not uerr3 and dlt["S_A"] is not None:
        g5["diag_3b_prime_info"] = {}
        for tag, (b, f) in G3_PAIRS.items():
            sb, sf = J[b]["structure"], J[f]["structure"]
            wu = (uG3[sf] - uG3[sb]) * V.EV_J / (J[b]["area_A2"] * V.A2_M2)
            wx, dx = W(b, f), W(b, f, "Edisp_eV")
            g5["diag_3b_prime_info"][tag] = ((wx - (wu + dx)) - dlt["S_A"]) if None not in (wx, dx) else None
    rec.update({"samples": smp, "G3": g3, "G4": g4, "G5_C": g5})
    # δ_XC+vdW (정보 · 라벨 규칙)
    reg_max = max([abs(g3[f"dW_{t}"]) for t in ("i", "ii") if g3.get(f"dW_{t}") is not None]
                  + [abs(v["dW"]) for v in g4.values() if isinstance(v, dict) and v.get("dW") is not None] or [0.0])
    dd = {}
    for k, (b, f) in DELTA_PAIRS.items():
        wo, wr = W(b, f), smp[k]["W_J_m2"]
        s_ = max(0.01, reg_max if k == "S_A" else 0.0)
        x = {"W_optB88_J_m2": wo, "W_ref_PBE_D3_J_m2": wr, "delta_J_m2": (wo - wr) if None not in (wo, wr) else None, "s_J_m2": s_,
             "status": {"bound": res[b]["status"], "far": res[f]["status"]}}
        if x["delta_J_m2"] is None:
            x["label"] = "δ 미완료 (G5_C 와 무관 · §4d)"
        elif wr > 0 and abs(wr) >= 10 * s_:
            x["pct"] = 100 * abs(x["delta_J_m2"]) / abs(wr)
            x["label"] = "함수 선택 (XC+vdW) 민감" if x["pct"] > DELTA_PCT_LABEL else "백분율 표기 가능"
        else:
            x["label"] = "절대 차이만 (해석 보류)"
        dd[k] = x
    rec["delta_XC_vdW"] = dd
    # ②′ C–C (정보 · 실험 값은 나란히만)
    cc = {m: {"W_J_m2": W(*p), "status": {"bound": res[p[0]]["status"], "far": res[p[1]]["status"]}} for m, p in CC_PAIRS.items()}
    cc["optb88_minus_pbed3_J_m2"] = (cc["optb88"]["W_J_m2"] - cc["pbed3"]["W_J_m2"]) if None not in (cc["optb88"]["W_J_m2"], cc["pbed3"]["W_J_m2"]) else None
    cc["⛔"] = "같은 VASP 안의 두 방법 차이만 — 실험 흑연 값으로 판정·보정하지 않는다 · LPSCl–C 방향을 정하지 않는다 · QE 값과 섞지 않는다"
    rec["CC_control"] = cc
    # far 진단 + 전하이동 신호 (정보 · 판정 아님)
    fd = {}
    for n, j in J.items():
        if not (n.endswith("_far") or "_far_" in n or n == A4_JOB):
            continue
        hist = res[n].get("history") or {}
        rung = "a4B" if j["ladder"] == "a4" else next((k for k in ("r2B", "r1B", "0") if hist.get(k) == "OK"), "0")   # 채택 시도 (없으면 단 0)
        t = _read(os.path.join(run, RUNG_DIR[rung].format(job=n), "OUTCAR"))
        fd[n] = far_diag(t, j["area_A2"]) if t else None
    rec["far_diagnostics"] = fd
    sig = []
    pa, pb = (fd.get("P2S_S_A_far") or {}).get("p_z_eA"), (fd.get("P2S_S_A_G3_c2_far_ii") or {}).get("p_z_eA")
    if None not in (pa, pb) and abs(pb - pa) >= SIG_PZ:
        sig.append(f"ⓐ |Δp_z| {abs(pb - pa):.3f} e·Å ≥ {SIG_PZ} (S_A far ↔ G3 far_ii)")
    if None not in (g3.get("dW_ii"), g3.get("dD3_ii")) and abs(g3["dW_ii"] - g3["dD3_ii"]) >= SIG_PBE:
        sig.append(f"ⓑ G3 (ii) PBE 몫 |ΔW − ΔD3| {abs(g3['dW_ii'] - g3['dD3_ii']):.4f} ≥ {SIG_PBE} J/m²")
    rec["charge_transfer_signals"] = {"signals": sig, "label": "분리 끝점의 전자 상태 미확인" if sig else None,
                                      "rule": "신호가 있으면 라벨 제한 · 계속할지는 1저자 (판정 상태는 바꾸지 않는다) · ⓒ 파일럿 S_A far 진단은 1저자가 본다"}
    if sig:
        g5["labels"].append("분리 끝점의 전자 상태 미확인")
    # 질문별 실패 전파 (§4d)
    q = {"G5_C": [n for n in set(sum(SAMPLES.values(), ()) + sum(G3_PAIRS.values(), ()) + sum(G4_PAIRS.values(), ())) if not ok(n)],
         "delta_XC_vdW": [n for n in sum(DELTA_PAIRS.values(), ()) if not ok(n)],
         "CC_control": [n for n in sum(CC_PAIRS.values(), ()) if not ok(n)], "silver_a4": [A4_JOB] if not ok(A4_JOB) else []}
    rec["failure_propagation"] = {k: sorted(v) for k, v in q.items()}
    rec["failure_propagation"]["rule"] = "물리적 수렴 실패는 그 질문에만 · 공통 환경 고장 (VASP 빌드 · PP · vdW 커널) 만 전체 정지 · 은 a4 실패는 은 G4 에만"
    rec["jobs"] = res
    rec["jobs_not_ok"] = sorted(n for n, r in res.items() if r["status"] != "OK")
    return rec


def collect_exit(rec):
    if rec.get("common_environment_failure"):
        return 6
    g = rec["G5_C"]["status"]
    return 0 if g == "PASS" else (10 if g == "FAIL" else 3)


# ───────────────────────── 파일럿 뒤: 등록부 봉인 · 해제 파일 ─────────────────────────
REG_SCHEMA = "wad_round2_pp_registry/v2"      # v2 (CZ Q-CZ-3): 파일럿 결박 = 모든 시도 {잡: {단: run_id}} · 봉인 전 모든 시도의 환경 감사
PILOT_JOBS = ("P2S_S_A_bound", "P2S_S_A_far", "CC_S33_AB_optB88_bound", "CC_S33_AB_optB88_far", A4_JOB)
V5_REGISTRY = "db/raw/wad_aprime_v5_vasp_2026_09_27/pp_registry_2026_10_05.json"


def _restart_regex_check(rx, run, J):
    """봉인 전 재시작 긍정 문구 regex 확인 (카드 §2.2 · CZ Q-CZ-2 ②) — 파일럿 시도 원문 (OUTCAR + stdout.log) 에서
    ⓐ WAVECAR 를 읽은 ⓑ (Startparameter ISTART 1 · 'WAVECAR not read' 없음) 에는 전부 맞고, 새로 시작한 시도 (ISTART 0 — 단 0 · ⓐ 단 · 되돌아간 ⓑ)
    에는 하나도 안 맞고, 러너 (grep -E) 와 검사기 (python re.M) 가 시도마다 같은 답이어야 한다. 아니면 PkgError (봉인 안 함).
    ⚠ 못 하는 것: 파일럿에 없던 출력 꼴 (다른 노드 · 다른 실패 경로) 에서도 같은 답이라는 보증은 없다 — 그래서 문구는 고정 구절 하나로 좁힌다."""
    bad = restart_regex_problems(rx)
    if bad:
        raise PkgError(f"재시작 regex {rx!r} 형식 — {bad} · 봉인하지 않는다")
    read, not_read, unknown, split = [], [], [], []
    for n in PILOT_JOBS:
        for rung in (("a4A", "a4B") if J[n]["ladder"] == "a4" else ("0", "r1A", "r1B", "r2B")):
            d = os.path.join(run, RUNG_DIR[rung].format(job=n))
            if not os.path.isfile(os.path.join(d, "attempt.json")):
                continue
            ev = restart_evidence(d)
            py = re.search(rx, ev["text"], re.M) is not None
            files = [os.path.join(d, f) for f in ("stdout.log", "OUTCAR") if os.path.isfile(os.path.join(d, f))]
            g = subprocess.run(["grep", "-aqE", "--", rx, *files], capture_output=True).returncode if files else 1
            if g not in (0, 1):
                raise PkgError(f"재시작 regex {rx!r}: grep -E 오류 (종료 {g}) — 봉인하지 않는다")
            tag = f"{n}/{rung}"
            if py != (g == 0):
                split.append(tag)
            if rung in ("r1B", "r2B", "a4B") and ev["istart"] == "1" and not ev["not_read_phrase"]:
                read.append((tag, py))
            elif ev["istart"] == "0" or ev["not_read_phrase"]:
                not_read.append((tag, py))
            else:
                unknown.append(tag)
    miss, hit = [t for t, m in read if not m], [t for t, m in not_read if m]
    why = ([f"두 엔진 갈림 {split}"] if split else []) + ([] if read else ["파일럿에 ⓐ WAVECAR 를 읽은 ⓑ 가 없다"]) \
        + ([f"읽은 ⓑ {len(read)} 중 안 맞음 {miss}"] if miss else []) + ([f"새로 시작한 시도에 맞음 {hit}"] if hit else [])
    if why:
        raise PkgError(f"재시작 regex {rx!r} 를 파일럿 원문으로 확인하지 못했다 — {' · '.join(why)} · 봉인하지 않는다 (regex 없이 봉인하거나 1저자)")
    return {"regex": rx, "read": [t for t, _ in read], "not_read": [t for t, _ in not_read], "unknown": unknown}


def _kernel_regex_check(rx, run, J):
    """봉인 전 커널 읽기 문구 확인 (카드 §2.4 · CZ Q-CZ-5) — 파일럿 optB88 시도 중 전자 스텝이 있는 것 (커널은 첫 전자 스텝 전에 읽는다) 의
    원문에 전부 맞고, optB88 이 아닌 시도 (커널을 안 읽는다) 에는 하나도 안 맞아야 한다 · 글자 제한은 재시작 문구와 같다.
    같은 원문의 부정·재생성 줄은 check_attempt 의 KERNEL_NOT_READ (환경 등급) 가 봉인을 막는다."""
    bad = restart_regex_problems(rx)
    if bad:
        raise PkgError(f"커널 regex {rx!r} 형식 — {bad} · 봉인하지 않는다")
    pos, neg = [], []
    for n in PILOT_JOBS:
        for rung in LADDER_RUNGS[J[n]["ladder"]]:
            d = os.path.join(run, RUNG_DIR[rung].format(job=n))
            if not os.path.isfile(os.path.join(d, "attempt.json")):
                continue
            hit = re.search(rx, _raw_text(d), re.M) is not None
            if J[n]["method"] == "optb88":
                if any(_ROW.match(l) for l in (_read(os.path.join(d, "OSZICAR")) or "").splitlines()):
                    pos.append((f"{n}/{rung}", hit))
            else:
                neg.append((f"{n}/{rung}", hit))
    miss, hits = [t for t, h in pos if not h], [t for t, h in neg if h]
    why = ([] if pos else ["파일럿 optB88 시도 (전자 스텝 ≥ 1) 가 없다"]) + ([f"optB88 시도 중 안 맞음 {miss}"] if miss else []) \
        + ([f"optB88 아닌 시도에 맞음 {hits}"] if hits else [])
    if why:
        raise PkgError(f"커널 regex {rx!r} 를 파일럿 원문으로 확인하지 못했다 — {' · '.join(why)} · 봉인하지 않는다 (regex 없이 봉인하면 optB88 은 KERNEL_UNVERIFIED 로 남는다)")
    return {"regex": rx, "optb88": [t for t, _ in pos], "not_optb88": [t for t, _ in neg]}


def seal_registry(out, ret, manifest_sha256, restart_read_regex="", v5_registry=None, kernel_read_regex=""):
    """파일럿 반송 → 탄소 등록부 (C 추가 · vdW 커널 신원 · VASP 빌드 · 파일럿 run_id). 은 a4 와 같은 빌드·같은 PP 여야 한다 (V5 등록부 대조).
    모든 시도를 본다 (CZ Q-CZ-3 — 채택 시도만 보면 a4A 만 다른 빌드여도 봉인됐다):
    ⛔ 무결성 실패 · 환경 등급 · 시도 사이 갈림 · 그 밖 모순·결측은 봉인하지 않는다 (자동 교체 없음 · 1저자) ·
    물리 실패 (실행 실패 · 미수렴 · SCF 미확인 · 재시작 미이행 · 그래서 생긴 ⓐ 자격 미달) 는 봉인을 막지 않는다 · 파일럿 잡마다 완결된 시도가 하나 이상.
    결박 = 모든 시도 {잡: {단: run_id}} · {잡: {단: {attempt.json · OUTCAR sha}}} (resolve_job 이 등록부로 대조한다)."""
    V.verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    J = {j["dir"]: j for j in meta["jobs"]}
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    v5 = json.load(open(v5_registry or os.path.join(REPO, V5_REGISTRY), encoding="utf-8"))
    every, titel, fp, fps = [], {}, {}, {}
    for n in PILOT_JOBS:
        att = resolve_job(J[n], out, run, None).get("attempts") or {}
        bad = {k: f"{a['status']} {a.get('why', '')}"[:200] for k, a in att.items()
               if not (a["status"] in SEAL_PASS or (k in ("r1A", "a4A") and a["status"] in A_TOLERATED))}
        if bad:
            raise PkgError(f"파일럿 {n}: {bad} — 봉인하지 않는다 (무결성·환경·모순·결측은 1저자 · 물리 실패만 통과)")
        if not att:
            raise PkgError(f"파일럿 {n}: 완결된 시도 (attempt.json) 가 없다 — 봉인하지 않는다")
        every += [(f"{n}/{k}", a) for k, a in att.items()]
        fp[n] = {k: a.get("run_id") for k, a in att.items()}
        fps[n] = {k: {"attempt.json": a.get("attempt_json_sha256"), "OUTCAR": a.get("outcar_sha256")} for k, a in att.items()}
        for k in att:
            tp = os.path.join(run, RUNG_DIR[k].format(job=n), "POTCAR.titel")
            if os.path.isfile(tp):
                for spec, t in zip(J[n]["potcar_spec"], V.parse_titel(open(tp, encoding="utf-8", errors="replace").read())[0]):
                    titel[spec] = t
    every += [x for x in aborted_attempts(J, out, ret) if x[0].split("/")[0] in PILOT_JOBS]
    env = env_audit(every)
    if env:
        raise PkgError(f"파일럿 환경 감사 {[' '.join(e)[:160] for e in env[:3]]} — 봉인하지 않는다 (공통 환경 고장 · 1저자)")
    sp, vers, ks = {}, set(), set()
    for _, a in every:
        for k, hh in (a.get("potcar_species_sha256") or {}).items():
            sp.setdefault(k, set()).add(hh)
        if a.get("version"):
            vers.add(a["version"])
        if a.get("kernel_sha256"):
            ks.add(a["kernel_sha256"])
    bad = [k for k, v in sp.items() if len(v) > 1] + (["VASP 버전 갈림"] if len(vers) != 1 else []) + (["커널 sha 갈림·없음"] if len(ks) != 1 else [])
    if set(sp) != set(POTCAR_MAP.values()):
        bad.append(f"종 {sorted(sp)} ≠ {sorted(POTCAR_MAP.values())}")
    if bad:
        raise PkgError(f"파일럿 공통 환경 불일치 {bad} — 봉인하지 않는다")
    sps = {k: next(iter(v)) for k, v in sp.items()}
    ver = next(iter(vers))
    if ver != v5["vasp_version"] or any(sps[k] != v5["species_sha256"][k] for k in v5["species_sha256"]):
        raise PkgError("VASP 빌드 또는 PP 가 V5 등록부와 다르다 — 은 a4 는 같은 빌드·같은 PP 여야 한다 (개정 4) · 봉인하지 않는다")
    kern = next(iter(ks))
    rx_check = _restart_regex_check(restart_read_regex, run, J) if restart_read_regex else None
    kx_check = _kernel_regex_check(kernel_read_regex, run, J) if kernel_read_regex else None
    return {"schema": REG_SCHEMA, "pp_set": V.PP_SET, "titel": titel, "species_sha256": sps, "vasp_version": ver,
            "kernel_sha256": kern, "package_manifest_sha256": manifest_sha256, "from_pilot": fp, "from_pilot_sha256": fps,
            "restart_read_regex": restart_read_regex, "restart_read_check": rx_check, "kernel_read_regex": kernel_read_regex, "kernel_read_check": kx_check, "v5_registry_sha256": _sha(v5_registry or os.path.join(REPO, V5_REGISTRY)),
            "⛔": "이 등록부를 봉인 (커밋·해시) 한 뒤 해제 파일을 보낸다 — 이후 모든 잡이 같아야 한다 (공통 환경 고장 = 전체 정지)"}


def release_text(reg, stages, caps_h, total_cap_h, release_id):
    """해제 파일 (TSV) — 러너가 sha 로 확인한다. 상한은 파일럿 실측으로 다시 낸 값 (1저자 확인) · 유한한 양수만 (nan · inf · 음수 · 0 거부 — CZ Q-CZ-3)."""
    pos = lambda x: (isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x > 0
                     and re.fullmatch(r"[0-9]+(\.[0-9]+)?", f"{x:g}") is not None)      # 러너 cap_num 과 같은 표기 (1e+06 꼴이면 러너가 거부한다)
    for s in stages:
        if s not in STAGE_EXPECT_H or s == "P":
            raise PkgError(f"해제할 수 없는 단계 {s}")
        if s not in caps_h:
            raise PkgError(f"단계 {s} 상한이 없다")
        if not pos(caps_h[s]):
            raise PkgError(f"단계 {s} 상한 {caps_h[s]!r} — 유한한 양수가 아니다")
    if not pos(total_cap_h):
        raise PkgError(f"전체 상한 {total_cap_h!r} — 유한한 양수가 아니다")
    L = [f"release\t{release_id}", f"stages\t{' '.join(stages)}"] + [f"cap_h\t{s}\t{caps_h[s]:g}" for s in stages]
    L += [f"total_cap_h\t{total_cap_h:g}", f"vasp_version\t{reg['vasp_version']}", f"kernel_sha256\t{reg['kernel_sha256']}"]
    L += [f"species_sha256\t{k}\t{v}" for k, v in sorted(reg["species_sha256"].items())]
    if reg.get("restart_read_regex"):
        L.append(f"restart_read_regex\t{reg['restart_read_regex']}")
    if reg.get("kernel_read_regex"):
        L.append(f"kernel_read_regex\t{reg['kernel_read_regex']}")      # 러너는 기록만 (판정은 검사기)
    return "\n".join(L) + "\n"


def _readme(meta, pkg_sha):
    rows = "\n".join(f"| {j['stage']} | `{j['dir']}` | {j['kind']} | {j['method']} | {j['nions']} | {j['encut']:.0f} | {'×'.join(map(str, j['kpts']))} | "
                     f"{j['sigma']:.3f} | {'0 → r1 ⓐ+ⓑ → r2 ⓑ' if j['ladder'] == 'carbon' else 'ⓐ+ⓑ 한 번'} |" for j in meta["jobs"])
    caps = " · ".join(f"{s} {meta['stages'][s]['cap_h']:g} h" for s in meta["stages"])
    return f"""# W_ad 외주 2차 — VASP 단일점 묶음 (LPSCl | 흑연 작은 모델 · C–C 대조 · 은 a4)

> 상태: **준비본 v1 — Codex CZ 묶음 리뷰 전 · 발송 전** · 결정 `D-2026-10-15-wad-p2small-vasp-card` · `D-2026-10-15-wad-aprime-v5-e70-a4-rerun` (active)
> 이 묶음 MANIFEST.sha256 의 sha256 = `{pkg_sha}` (보낼 때 메일 본문에 적는다 — 반송 검사가 이 값으로 승인본을 확인한다)

## 무엇을 하나
단일점 (SCF) 24 잡 — 이완 없음. 좌표는 정해져 있습니다 (POSCAR 그대로). 단계마다 돌립니다.

| 단계 | 잡 | 종류 | 방법 | NIONS | ENCUT | k (Γ) | SIGMA | 재시도 |
|---|---|---|---|---|---|---|---|---|
{rows}

## 돌리는 법
1. **파일럿 (단계 P · 5 잡) 먼저**: `VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> VDW_KERNEL=<vdw_kernel.bindat> bash run_all.sh`
   (STAGES 기본값 = P). 끝나면 `round2_return.tgz` + `.sha256` 을 보내 주세요 — 우리가 파일럿을 검사해 **등록부를 봉인**하고 **해제 파일**을 보냅니다.
2. 해제 파일을 받으면: `STAGES="1 2 3 4" RELEASE_FILE=<받은 파일> RELEASE_SHA256=<메일의 sha256> VASP_CMD=… POTCAR_DIR=… VDW_KERNEL=… bash run_all.sh`
   — 파일럿 잡은 다시 돌지 않습니다 (시도 폴더가 있으면 기록을 다시 판정만 합니다).
3. **재시도는 러너가 미리 정한 대로만** 합니다 (탄소 잡: 단 0 → r1 ⓐ (쌍극 퍼텐셜 보정 끔 · WAVECAR 남김) → r1 ⓑ (보정 켬 · ⓐ WAVECAR 에서 · AMIN 0.01) →
   r2 ⓑ (혼합 AMIX 0.1 · BMIX 0.01 · AMIN 0.01 · 같은 ⓐ WAVECAR) / 은 a4: ⓐ+ⓑ 한 번). 다음 단은 **확인된 미수렴 · 실행 실패**일 때만입니다.
   그 밖 (SCF 미확인 · ⓐ 자격 미달 · 재시작 미이행) 은 멈추고 기록만 남깁니다 — **다른 설정으로 더 돌리지 마세요.**
4. **ⓐ 의 WAVECAR 는 지우지 마세요** — 러너가 그 잡이 끝날 때 지웁니다 (반송하지 않습니다 · sha·크기·머리만 기록).
5. 0 스텝 인프라 중단 (스케줄러 취소 등으로 전자 반복 0 회) 이면: `bash run_all.sh --infra-abort <잡> <단> <스케줄러 잡 id> <취소 UTC> <사유>` 로 기록한 뒤
   다시 돌려 주세요 (잡마다 2 회까지 · 그 벽시계도 상한 장부에 들어갑니다 · 시간을 알면 `WALL_S=<초>` 를 앞에 붙여 주세요).
6. **누적 상한**: 단계마다 {caps} · 전체 {meta['total_cap_h']:g} h (한 노드 벽시계 합 · 파일럿 뒤에는 해제 파일의 값). 넘으면 러너가 다음 잡을 띄우지 않고 멈춥니다 (종료 5) —
   돌던 잡은 끝까지 돕니다. 반송해 주시고 결정을 기다려 주세요.
7. **공통 환경 고장 = 전체 정지** (종료 6): VASP 빌드 · POTCAR · vdW 커널 파일이 파일럿에서 봉인한 것과 다르거나, optB88 잡에 커널이 없을 때.
   POTCAR 는 VASP 를 띄울 때마다 (끊긴 뒤 이어 돌릴 때도) 다시 확인합니다. 해제 파일의 상한 값이 양수가 아니면 시작하지 않습니다 (종료 2).
8. 성능 태그는 `PERF_TAGS_FILE` 로만 (V5 와 같은 규칙) — **INCAR · POSCAR · KPOINTS 는 고치지 마세요.** ⓐ·ⓑ 는 같은 랭크·NCORE·KPAR 로 돌려야 합니다 (NBANDS 가 같아야 WAVECAR 를 읽는다).
9. 반송 묶음은 러너가 허용 목록만 담습니다 (POTCAR 본문 · WAVECAR · CHGCAR · vdw_kernel.bindat 는 넣지 않습니다). 포장이 실패하면 (종료 4) `PACK_ONLY=1 bash run_all.sh`.
   보내는 것: 종료 0 · 1 · 5 · 6 뒤 `sha256sum -c round2_return.tgz.sha256` 까지 통과한 쌍.
10. 지원 환경: Linux · bash ≥ 4 · GNU coreutils (find sort grep cmp sha256sum od stat) · GNU tar · awk.

## VASP · POTCAR · vdW 커널
- **VASP**: V5 와 같은 빌드 (vasp.5.4.4.18Apr17-6-g9f103f2a35) — 은 a4 는 반드시 같은 빌드·같은 PP 여야 합니다.
- **POTCAR** PBE_54: Li_sv · P · S · Cl · Ag (V5 와 같은 파일) + **C** (`PAW_PBE C 08Apr2002` 예상 — 보유본으로 확인 · 파일럿 뒤 봉인).
- **optB88-vdW**: `vdw_kernel.bindat` (VASP 5.4.4 배포본) 경로를 `VDW_KERNEL` 로 주세요. 러너가 sha256 · 크기를 기록합니다 (파일럿 뒤 봉인).

## 돌려받을 것
`round2_return.tgz` + `.sha256` — 시도마다 {' · '.join(RETURN_ALLOWED)} (있는 것만) · `run/status.tsv` · `run/env.txt` · `run/infra_aborts.tsv` · `MANIFEST.sha256`.
VASP 빌드 · 노드/코어 · **잡별 peak RSS · 벽시계** 를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.

## English summary
24 single-point SCF runs (no relaxation) on fixed geometries, in stages: P (pilot: 5 jobs) first, then 1–4 only after we send a release file.
Carbon jobs: Gaussian ISMEAR 0, SIGMA 0.05 eV (0.025 eV for one check), ENCUT 520 eV (650 eV for one check), PBE+D3(BJ) with explicit parameters, or
optB88-vdW (GGA = BO, PARAM1/PARAM2, AGGAC 0, LUSE_VDW, Zab_vdW, IVDW 0; needs vdw_kernel.bindat via VDW_KERNEL). Dipole correction along z.
The runner applies a pre-registered retry ladder automatically (rung 0 → r1 stage A without dipole potential correction, then stage B restarting from that
WAVECAR with AMIN 0.01 → r2 stage B with AMIX 0.1/BMIX 0.01/AMIN 0.01); the silver a4 job is a single two-stage run. Convergence is judged from the last
electronic row of OSZICAR (|dE| and |d eps| ≤ EDIFF), never from OUTCAR wording. Please do not edit INCAR/POSCAR/KPOINTS, do not delete stage-A WAVECARs,
and do not rerun anything by hand; record zero-step infrastructure aborts with --infra-abort. Cumulative wall-time caps stop the runner (exit 5);
a VASP build, POTCAR or vdW-kernel change stops everything (exit 6). Return the round2_return.tgz pair after `sha256sum -c`.
"""


# ───────────────────────── 시험 (가짜 VASP) ─────────────────────────
FAKE_VASP = r"""
import os, sys, json, re, struct, time
plan = json.load(open(os.environ["FAKE_PLAN"])) if os.environ.get("FAKE_PLAN") else {}
pkg = json.load(open(os.path.join(os.environ["FAKE_PKG"], "jobs.json")))
J = {j["dir"]: j for j in pkg["jobs"]}
def iv(t, k):
    v = None
    for ln in t.splitlines():
        ln = re.split(r"[#!]", ln, maxsplit=1)[0]
        for st in ln.split(";"):
            if "=" in st and st.split("=", 1)[0].strip().upper() == k:
                v = st.split("=", 1)[1].strip()
    return v
inc = open("INCAR").read()
m = re.search(r"(?:W_ad round2|A-prime V5) (\S+) \(single point\)", inc)
job = m.group(1) if m else "?"
if job == "V5_s_outer_A_G4_e70_far":
    job = "V5_s_outer_A_G4_e70_far_a4"
cwd = os.getcwd(); base = os.path.basename(cwd); par = os.path.basename(os.path.dirname(cwd))
if base == "stageA":
    rung = "a4A" if par.endswith("_a4") else "r1A"
elif base.endswith("_r1"):
    rung = "r1B"
elif base.endswith("_r2"):
    rung = "r2B"
elif base.endswith("_a4"):
    rung = "a4B"
else:
    rung = "0"
beh = plan.get(f"{job}/{rung}", plan.get(f"*/{rung}", "conv"))
j = J[job]; st = j["structure"]
nelm = int(iv(inc, "NELM") or 60); lwave = (iv(inc, "LWAVE") or "").upper().strip(".") in ("TRUE", "T")
ldip = (iv(inc, "LDIPOL") or "").upper().strip(".") in ("TRUE", "T"); gga = iv(inc, "GGA") or "PE"
ist_in = int(iv(inc, "ISTART") or 0); ich_in = int(iv(inc, "ICHARG") or 2)
ist = 1 if (ist_in == 1 and os.path.isfile("WAVECAR") and beh not in ("ignore_wavecar", "istart0_quiet", "istart0_only")) else 0
ich = ich_in if ist == 1 else 2
if beh == "istart0_only":
    ich = 0                      # 시험용: ICHARG 는 0 인데 ISTART 만 0 (각 조건이 따로 잡는지)
if beh == "icharg2_only":
    ich = 2                      # 시험용: ISTART 는 1 인데 ICHARG 만 2
version = os.environ.get("FAKE_VERSION", "vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex")
if beh == "otherver":                            # CZ Q-CZ-3 재현: 이 시도만 다른 VASP 빌드 (나머지는 conv 와 같다)
    version = "vasp.6.4.2 other build (this attempt only)"
pot = open("POTCAR").read()
titel = re.findall(r"TITEL\s*=\s*(.+)", pot); zv = [float(x) for x in re.findall(r"ZVAL\s*=\s*(-?\d+\.?\d*)", pot)]
pl = open("POSCAR").read().splitlines(); nn = [int(x) for x in pl[6].split()]
nel = sum(z * n for z, n in zip(zv, nn)); nions = sum(nn)
E = json.load(open(os.environ["FAKE_ENERGY"])) if os.environ.get("FAKE_ENERGY") else {}
key = f"{st}|{j['method']}|{j['kind']}"
d3s = {x["structure"]: x["d3_2body_eV_ref"] for x in pkg["jobs"] if "d3_2body_eV_ref" in x}
Et = E.get(job, E.get(st, -1000.0)) + d3s.get(st, 0.0)          # 총에너지 = 표의 '전자' 값 + 같은 기하의 D3 (optB88 도 같은 기준 위에 표 값으로 차이를 준다)
Ed = (j.get("d3_2body_eV_ref") + E.get(f"edisp_shift|{job}", 0.0)) if j["method"] != "optb88" else None
pz = E.get(f"pz|{job}", 0.10)
rows, rc, term = [], 0, True
if beh in ("conv", "otherver"):
    rows = [(i, 1e-3 / i, 1e-4 / i) for i in range(1, 25)] + [(25, -3.1e-8, -1.2e-8)]
elif beh in ("noconv", "badwav", "nowav"):
    rows = [(i, 2.2e-3, -3.2e-5) for i in range(1, nelm + 1)]
elif beh == "conv_badwav":
    rows = [(i, 1e-3 / i, 1e-4 / i) for i in range(1, 25)] + [(25, -3.1e-8, -1.2e-8)]
elif beh in ("crash", "crash_tworuns"):
    rows, rc, term = [(i, 1e-2, 1e-3) for i in range(1, 8)], 1, False
elif beh == "nan":
    rows = [(i, 1e-3, 1e-4) for i in range(1, 20)] + [(20, "NaN", "NaN")]
elif beh == "zero":
    rows, rc, term = [], 1, False
elif beh == "step0":
    rows = [(0, 1e-3, 1e-4)] + [(i, 1e-3, 1e-4) for i in range(2, 10)] + [(10, -1e-8, -1e-8)]
elif beh in ("ignore_wavecar", "istart0_quiet", "istart0_only", "icharg2_only"):
    rows = [(i, 1e-3 / i, 1e-4 / i) for i in range(1, 25)] + [(25, -3.1e-8, -1.2e-8)]
elif beh == "slow":
    rows = [(i, 2e-3, 2e-5) for i in range(1, 161)]
def fmt(x):
    return x if isinstance(x, str) else f"{x: .5E}"
osz = open("OSZICAR", "w")
for k, (i, de, dp) in enumerate(rows):
    osz.write(f"DAV: {i:4d}   {Et + 0.001 * (len(rows) - k):.12E}   {fmt(de)}   {fmt(dp)}  9016   0.341E-03  0.267E-01\n"); osz.flush()
    if beh == "slow":
        time.sleep(0.01 if k < 130 else 0.05)
if term and rows:
    osz.write(f"   1 F= {Et:.8E} E0= {Et:.8E}  d E =0.1E+00\n")
osz.close()
out = [f" {version}", " ", " executed on             LinuxIFC date 2026.10.20  00:00:00", "", " INCAR:"] + [f"   {x}" for x in inc.splitlines()]
if beh == "crash_tworuns":                       # CZ Q-CZ-1 재현 ①: 같은 버전의 실행 머리줄이 둘 (두 실행이 한 OUTCAR 에)
    out = [f" {version}", " executed on             LinuxIFC date 2026.10.19  23:00:00"] + out
out += [f" POTCAR:    {t}" for t in titel] + [f"   TITEL  = {t}" for t in titel]
nb = 512
out += [" Dimension of arrays:", f"   k-points           NKPTS =      4   k-points in BZ     NKDIM =      4   number of bands    NBANDS=    {nb}",
        f"   number of dos      NEDOS =    301   number of ions     NIONS = {nions:6d}", "   dimension x,y,z NGXF=   100 NGYF=   200 NGZF=   400", "",
        " Startparameter for this run:", f"   NWRITE =      2    write-flag & timer", f"   ISTART =      {ist}    job   : 0-new  1-cont  2-samecut",
        f"   ICHARG =      {ich}    charge: 1-file 2-atom 10-const", "   ISPIN  =      1    spin polarized calculation?",
        f"   ENCUT  = {float(iv(inc, 'ENCUT')):7.1f} eV  38.22 Ry    6.18 a.u.", f"   NELM   =    {nelm};   NELMIN=  6; NELMDL= -5     # of ELM steps",
        f"   NELECT = {nel:12.4f}    total number of electrons", f"   ISMEAR =     {int(iv(inc, 'ISMEAR'))};   SIGMA  = {float(iv(inc, 'SIGMA')):7.2f}  broadening in eV -4-tet -1-fermi 0-gaus",
        f"     AMIX     = {float(iv(inc, 'AMIX') or 0.4):6.2f};   BMIX     = {float(iv(inc, 'BMIX') or 1.0):5.2f}", f"     AMIN     = {float(iv(inc, 'AMIN') or 0.1):6.2f}",
        f"   LDIPOL =      {'T' if ldip else 'F'}    correct potential (dipole corrections)", "   IDIPOL =      3    1-x, 2-y, 3-z, 4-all directions"]
out.append(f"   GGA     =    {gga}    GGA type")             # 5.4.4 실물 꼴 (V5 반송 OUTCAR — PE)
if gga == "BO":
    out += ["   PARAM1  =  0.1833", "   PARAM2  =  0.2200", "   Zab_vdW = -0.8491", "   AGGAC   =  0.0000", "   LUSE_VDW =      T"]
    if os.path.isfile("vdw_kernel.bindat"):
        out.append(" vdW kernel read from vdw_kernel.bindat")
dz = float(iv(inc, "DIPOL").split()[2])
for (i, de, dp) in rows:
    out.append(f"--------------------------------------- Iteration      1( {i:3d})  ---------------------------------------")
    if ldip:
        out += [" DIPCOR: dipole corrections for dipol", f" direction  3 min pos {round(((dz + 0.5) % 1.0) * 400) % 400:5d},"]
    out += [f" dipolmoment           0.000000      0.000000      {pz:.6f} electrons x Angstroem", " dipol+quadrupol energy correction           -0.000107 eV"]
if beh == "two_blocks":
    pass
if rows and term:
    out.append(" E-fermi :   0.9032     XC(G=0):  -6.3203     alpha+bet : -6.2429")
    if Ed is not None:
        out += ["         DFTD3 V3.0 Rev 1        ", " IVDW         = 12", " VDW_S6       = 1.0000", " VDW_S8       = 0.7875", " VDW_A1       = 0.4289",
                " VDW_A2       = 4.4407", " VDW_RADIUS   = 50.2000 A", " VDW_CNRADIUS = 21.1700 A", f" Edisp (eV)  {Ed:.5f}"]
    out += ["  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)", "  ---------------------------------------------------", f"  free  energy   TOTEN  =  {Et:18.8f} eV", "",
            f"  energy  without entropy=  {Et + 0.01:18.8f}  energy(sigma->0) =  {Et + 0.005:18.8f}",
            " General timing and accounting informations for this job:"]
open("OUTCAR", "w").write("\n".join(out) + "\n")
so = [" running on   64 total cores", f" {version}"]
if ist == 0 and beh not in ("istart0_quiet", "istart0_only"):
    so.append(" WAVECAR not read")
if ist == 1:
    so.append(" reading WAVECAR")                # 재시작 긍정 문구 (시험용 — 업체 5.4.4 의 실제 문구는 파일럿 원문으로 확정)
open("stdout.log", "w").write("\n".join(so) + "\n")
if lwave and beh != "nowav" and rows:
    recl = 64
    nbw = nb + (1 if beh in ("badwav", "conv_badwav") else 0)
    rec1 = struct.pack("3d", recl, 1, 45200).ljust(recl, b"\0")
    rec2 = struct.pack("3d", 4, nbw, float(iv(inc, "ENCUT"))).ljust(recl, b"\0")
    open("WAVECAR", "wb").write(rec1 + rec2 + os.urandom(256))
for f in ("CHGCAR", "CHG", "vasprun.xml"):
    open(f, "w").write("FAKE DO_NOT_SHIP\n")
sys.exit(rc)
"""


def _selftest():
    import shutil
    import subprocess
    import tempfile
    from ase.io import read, write
    import numpy as np
    n_ok = n_bad = 0

    def ck(name, cond, info=""):
        nonlocal n_ok, n_bad
        if cond:
            n_ok += 1
        else:
            n_bad += 1
            print(f"  ✗ {name} {str(info)[:400]}")
    sys.path.insert(0, HERE)
    import build_aprime_s3 as S3
    T = tempfile.mkdtemp(prefix="r2_")
    try:
        # ── 0. 가짜 P2′ 봉인 (레포 초기 구조 · 흑연 +0.1 Å) ──
        pgeom = os.path.join(REPO, "db", "inputs", "wad_p2small_geometries_2026_10_17")
        R0 = os.path.join(T, "relax")
        for name, sub, term in S3.P2S_SAMPLES:
            d = os.path.join(R0, sub); os.makedirs(d)
            at = read(os.path.join(pgeom, sub, "bound.extxyz")); x = at.get_positions(); x[S3._ads_mask(at, "P2S"), 2] += 0.1; at.set_positions(x)
            write(os.path.join(d, "relaxed.extxyz"), at)
            gm = json.load(open(os.path.join(pgeom, sub, "meta.json"), encoding="utf-8"))
            json.dump({"model": "P2S", "term": term, "registry": "A", "init_sha256": gm["sha256"]["bound"], "relaxed_sha256": _sha(os.path.join(d, "relaxed.extxyz")),
                       "converged_fmax": True, "fmax_free_final_eV_A": 0.015, "steps_taken": 300, "interface_check_flags": [], "disp_max_A": 0.1,
                       "calculator": {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default", "fairchem.core": "2.21.0",
                                      "checkpoint": [{"sha256": V.UMA_REQ["checkpoint_sha256"]}], "d3": {"impl": "simple-dftd3 (python)", "version": "1.6.0"}}},
                      open(os.path.join(d, "relax_meta.json"), "w"))
            json.dump({"flags": []}, open(os.path.join(d, "interface_check.json"), "w"))
        SEAL = os.path.join(T, "seal")
        sm = S3.seal_p2s(R0, pgeom, SEAL, date="2026-10-17")
        # ── 1. 묶음 ──
        PKG = os.path.join(T, "pkg")
        meta, msha = build(SEAL, PKG)
        J = {j["dir"]: j for j in meta["jobs"]}
        ck("묶음: 잡 24 (탄소 21 · C–C 4 중 PBE 2 + optB88 2 · 은 a4 1) · 단계 P 5 · 1 4 · 2 9 · 3 4 · 4 2",
           len(J) == 24 and [len(meta["stages"][s]["jobs"]) for s in "P1234"] == [5, 4, 9, 4, 2], [len(meta["stages"][s]["jobs"]) for s in "P1234"])
        ck("묶음: 단계 상한 = 1.5 × 장부 기대 (P 117 · 1 170 · 2 586 · 3 204 · 4 24) · 전체 1,080", [meta["stages"][s]["cap_h"] for s in "P1234"] == [117, 170, 586, 204, 24]
           and meta["total_cap_h"] == 1080, [meta["stages"][s]["cap_h"] for s in "P1234"])
        rd = lambda j, f: open(os.path.join(PKG, "jobs", j, f), encoding="utf-8").read()
        okd = all({k: v[1] for k, v in semantic_diff(rd(n, "INCAR"), rd(n, f"INCAR.{r}")).items()} == RUNG_DIFF[r]
                  for n in J if J[n]["ladder"] == "carbon" for r in ("r1A", "r1B", "r2B"))
        ck("묶음: 탄소 사다리 INCAR 의미상 차이 = 선언 (r1A LDIPOL F·LWAVE T · r1B ISTART 1·ICHARG 0·AMIN 0.01·NELM 300 · r2B + AMIX 0.1·BMIX 0.01)", okd)
        card_vals = {"r1A": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE."}, "r1B": {"ISTART": "1", "ICHARG": "0", "AMIN": "0.01", "NELM": "300"},
                     "r2B": {"ISTART": "1", "ICHARG": "0", "AMIX": "0.1", "BMIX": "0.01", "AMIN": "0.01", "NELM": "300"},
                     "a4A": {"LDIPOL": ".FALSE.", "LWAVE": ".TRUE."}, "a4B": {"ISTART": "1", "ICHARG": "0", "AMIN": "0.01", "NELM": "300"}}
        ck("카드 값 (리터럴 대조 — 순환 아님): 사다리 단 차이 · NELM 0/r1A 200 · r1B/r2B 300 · a4 200/300 · σ 0.05/0.025 · ENCUT 520/650 · k Γ3×2/Γ6×2/Γ18×18",
           RUNG_DIFF == card_vals and NELM_RUNG == {"0": 200, "r1A": 200, "r1B": 300, "r2B": 300, "a4A": 200, "a4B": 300} and (SIGMA_C, SIGMA_C_HALF) == (0.05, 0.025)
           and (ENCUT, ENCUT_G4) == (520.0, 650.0) and (K_BASE, K_DENSE, K_CC) == ((3, 2, 1), (6, 2, 1), (18, 18, 1)) and dict(OPTB88) == {"GGA": "BO", "PARAM1": "0.1833333333",
           "PARAM2": "0.22", "AGGAC": "0.0", "LUSE_VDW": ".TRUE.", "ZAB_VDW": "-0.8491", "IVDW": "0"} and (G5C_PER, G5C_BIAS, G3_DW, G4_DW, TRIG_DW) == (0.03, 0.02, 0.01, 0.01, 0.008))
        v5i = open(os.path.join(REPO, V5_PKG, "jobs", A4_SRC, "INCAR"), encoding="utf-8").read()
        ck("묶음: 은 a4 ⓐ·ⓑ INCAR = V5 봉인 INCAR + 개정 4 차이만 · POSCAR·KPOINTS = V5 파일", all({k: v[1] for k, v in semantic_diff(v5i, rd(A4_JOB, f"INCAR.{r}")).items()} == RUNG_DIFF[r] for r in ("a4A", "a4B"))
           and _sha_text(rd(A4_JOB, "POSCAR")) == J[A4_JOB]["v5_source"]["files_sha256"]["POSCAR"])
        pi = V.parse_incar_strict(rd("P2S_S_A_bound", "INCAR"))[0]; oi = V.parse_incar_strict(rd("P2S_S_A_optB88_bound", "INCAR"))[0]
        ck("묶음: 탄소 점유 ISMEAR 0 · SIGMA 0.05 · PBE+D3 줄 · optB88 은 GGA BO·PARAM·LUSE_VDW·ZAB · IVDW 0 · D3 계수 줄 없음",
           pi["ISMEAR"] == "0" and pi["SIGMA"] == "0.0500" and pi["IVDW"] == "12" and oi["GGA"] == "BO" and oi["IVDW"] == "0" and oi["LUSE_VDW"] == ".TRUE."
           and not any(k in oi for k in D3_TAGS[1:]) and oi["ZAB_VDW"] == "-0.8491", (pi.get("SIGMA"), oi))
        g4 = {t: V.parse_incar_strict(rd(f"P2S_S_A_G4_{t}_bound", "INCAR"))[0] for t in ("k62", "k62s2", "e650")}
        ck("묶음: G4 — Γ6×2 · σ/2 0.025 · ENCUT 650 · 나머지 같다 · C–C Γ 18×18×1", rd("P2S_S_A_G4_k62_bound", "KPOINTS").splitlines()[3] == "6 2 1"
           and g4["k62s2"]["SIGMA"] == "0.0250" and g4["e650"]["ENCUT"] == "650.0" and rd("CC_S33_AB_pbed3_far", "KPOINTS").splitlines()[3] == "18 18 1")
        ck("묶음: 같은 기하 잡의 D3 기대값이 같다 (S_A bound · G4 셋) · optB88 은 D3 기대값 없음",
           len({J[n]["d3_2body_eV_ref"] for n in ("P2S_S_A_bound", "P2S_S_A_G4_k62_bound", "P2S_S_A_G4_k62s2_bound", "P2S_S_A_G4_e650_bound")}) == 1
           and "d3_2body_eV_ref" not in J["P2S_S_A_optB88_bound"])
        dzs = V.dipol_z(sm["sets"]["S_A"]["dipfield"]["emaxpos"], sm["sets"]["S_A"]["dipfield"]["eopreg"])
        ck("묶음: DIPOL = 봉인 집합의 쌍극 구간 (S_A) · POSCAR 종 줄에 C", abs(J["P2S_S_A_p05_bound"]["dipol_z"] - round(dzs, 6)) < 1e-9 and "C" in rd("P2S_S_A_bound", "POSCAR").splitlines()[5].split())
        m2, msha2 = build(SEAL, os.path.join(T, "pkg2"))
        ck("결정성: 두 번 만들면 MANIFEST sha 가 같다", msha2 == msha, (msha, msha2))
        bad_seal = os.path.join(T, "seal_bad"); shutil.copytree(SEAL, bad_seal)
        open(os.path.join(bad_seal, "structures", "S_A_far.extxyz"), "a").write(" \n")
        try:
            build(bad_seal, os.path.join(T, "pkg_bad")); bad = False
        except PkgError as e:
            bad = "sha" in str(e)
        ck("⛔음성 묶음: 봉인 구조를 손대면 만들지 않는다", bad)
        led = os.path.join(T, "ledger.json"); json.dump({"decisions": [{"id": DECISIONS[0], "decision_state": "active"}, {"id": DECISIONS[1], "decision_state": "proposed"}]}, open(led, "w"))
        try:
            build(SEAL, os.path.join(T, "pkg_bad2"), ledger=led); bad = False
        except PkgError as e:
            bad = "active" in str(e)
        ck("⛔음성 묶음: 결정이 active 가 아니면 만들지 않는다", bad)
        # ── 2. 판정 계약 교차 (러너 awk ↔ 파이썬 · 같은 탐침) ──
        runner = run_all_text()
        fn = "\n".join(re.findall(r"(?ms)^(incar_val\(\)\{.*?\n\}|judge\(\)\{.*?\n\})\n", runner + "\n"))
        if "judge(){" not in fn:
            fn = runner[runner.index("incar_val(){"):runner.index("\n}\n", runner.index("judge(){")) + 3]
        jt = os.path.join(T, "judge.sh"); open(jt, "w").write("set -u\n" + fn[fn.index("incar_val(){"):] + '\njudge "$1" "$2"\n')
        row = lambda i, de, dp: f"DAV: {i:4d}   -0.67E+03   {de}   {dp}  9016   0.341E-03\n"
        okrows = "".join(row(i, "-0.1E-02", "-0.1E-03") for i in range(1, 25)) + row(25, "-0.31E-07", "-0.12E-07")
        out_ok = lambda n, extra="": f" vasp.5.4.4 x\n{extra}" + "".join(f" Iteration      1( {i:3d})\n" for i in range(1, n + 1)) + " General timing and accounting\n"
        noterm = lambda k: " vasp.5.4.4 x\n" + "".join(f" Iteration      1( {i:3d})\n" for i in range(1, k + 1))          # 안 끝난 OUTCAR (마지막 반복 번호 k)
        inc = "NELM = 30\nEDIFF = 1E-6\n"
        probes = {"ok": (okrows, out_ok(25), inc, 0), "noconv": (okrows.replace("-0.31E-07", "0.22E-02"), out_ok(25), inc, 0),
                  "deps_only": (okrows.replace("-0.12E-07", "0.2E-05"), out_ok(25), inc, 0),
                  "edge_eq": (okrows.replace("-0.31E-07", "0.1E-05").replace("-0.12E-07", "-1E-6"), out_ok(25), inc, 0),
                  "nan": (okrows.replace("-0.31E-07", "NaN"), out_ok(25), inc, 0), "inf": (okrows.replace("-0.31E-07", "1E+400"), out_ok(25), inc, 0),
                  "stars": (okrows.replace("-0.31E-07", "*******"), out_ok(25), inc, 0), "four_fields": (okrows.rsplit("DAV", 1)[0] + "DAV:   25   -0.67E+03   -0.3E-07\n", out_ok(25), inc, 0),
                  "step0": (row(0, "1E-3", "1E-4") + okrows.split("\n", 1)[1], out_ok(25), inc, 0),
                  "skip": (okrows.replace("DAV:    7", "DAV:    8", 1), out_ok(25), inc, 0),
                  "two_blocks": (okrows + "   1 F= -.1E+04 E0= -.1E+04 d E =0.1E+00\n" + row(1, "1E-3", "1E-4"), out_ok(25), inc, 0),
                  "after_ion": (okrows + "   1 F= -.1E+04 E0= -.1E+04 d E =0.1E+00\n", out_ok(25), inc, 0),
                  "no_rows": ("", out_ok(0), inc, 0), "gt_nelm": (okrows, out_ok(25), "NELM = 20\nEDIFF = 1E-6\n", 0),
                  "rc1": (okrows, out_ok(25), inc, 1), "not_term": (okrows, " vasp.5.4.4 x\n" + "".join(f" Iteration      1( {i:3d})\n" for i in range(1, 26)), inc, 0),
                  "rc1_nan": (okrows.replace("-0.31E-07", "NaN"), out_ok(25), inc, 1), "two_runs": (okrows, out_ok(25, " vasp.5.4.4 y\n"), inc, 0),
                  "it_mismatch": (okrows, out_ok(24), inc, 0), "no_ediff": (okrows, out_ok(25), "NELM = 30\n", 0), "no_nelm": (okrows, out_ok(25), "EDIFF = 1E-6\n", 0),
                  "nelm_semicolon": (okrows, out_ok(25), "NELM = 30; EDIFF = 1E-6 # c\n", 0), "dup_nelm_last": (okrows, out_ok(25), "NELM = 10\nNELM = 30\nEDIFF = 1E-6\n", 0),
                  "rc1_gt_nelm": (okrows, out_ok(25), "NELM = 20\nEDIFF = 1E-6\n", 1), "rc1_step0": (row(0, "1E-3", "1E-4") + okrows.split("\n", 1)[1], out_ok(25), inc, 1),
                  "rc1_no_rows": ("", " vasp.5.4.4 x\n", inc, 1),
                  # R1 (CZ Q-CZ-1) — 확정 모순은 rc 보다 먼저 · 안 끝난 OUTCAR 의 결측은 실행 실패
                  "rc1_two_runs": (okrows, out_ok(25, " vasp.5.4.4 y\n"), inc, 1), "rc1_it_mismatch_term": (okrows, out_ok(24), inc, 1),
                  "crash_midstep": (okrows, noterm(26), inc, 1), "crash_outcar_short": (okrows, noterm(20), inc, 1),
                  "crash_no_iter": (okrows, " vasp.5.4.4 x\n", inc, 1), "crash_no_header": (okrows, "", inc, 1),
                  "crash_outcar_ahead": (okrows, noterm(28), inc, 1), "noterm_two_runs": (okrows, " vasp.5.4.4 y\n" + noterm(25), inc, 1),
                  "term_no_header": (okrows, out_ok(25).replace(" vasp.5.4.4 x\n", ""), inc, 1), "rc0_noterm_midstep": (okrows, noterm(26), inc, 0)}
        agree, seen = True, {}
        for name, (osz, out, ic, rc) in probes.items():
            d = os.path.join(T, "probe", name); os.makedirs(d)
            open(os.path.join(d, "OSZICAR"), "w").write(osz); open(os.path.join(d, "OUTCAR"), "w").write(out); open(os.path.join(d, "INCAR"), "w").write(ic)
            sh = subprocess.run(["bash", jt, d, str(rc)], capture_output=True, text=True).stdout.split()
            py = [str(x) for x in judge_text(osz, out, ic, rc)]
            seen[name] = (sh, py)
            if sh != py:
                agree = False
        ck(f"판정 계약: 러너 awk = 파이썬 (탐침 {len(probes)} · 상태·행수·dE·d eps·사유 전부)", agree, {k: v for k, v in seen.items() if v[0] != v[1]})
        want = {"ok": "OK", "noconv": "SCF_NOT_CONVERGED", "deps_only": "SCF_NOT_CONVERGED", "edge_eq": "OK", "nan": "SCF_UNVERIFIED", "inf": "SCF_UNVERIFIED",
                "stars": "SCF_UNVERIFIED", "four_fields": "SCF_UNVERIFIED", "step0": "SCF_UNVERIFIED", "skip": "SCF_UNVERIFIED", "two_blocks": "SCF_UNVERIFIED",
                "after_ion": "OK", "no_rows": "SCF_UNVERIFIED", "gt_nelm": "SCF_UNVERIFIED", "rc1": "RUN_FAILED", "not_term": "RUN_FAILED", "rc1_nan": "RUN_FAILED",
                "two_runs": "SCF_UNVERIFIED", "it_mismatch": "SCF_UNVERIFIED", "no_ediff": "SCF_UNVERIFIED", "no_nelm": "SCF_UNVERIFIED", "nelm_semicolon": "OK", "dup_nelm_last": "OK",
                "rc1_gt_nelm": "SCF_UNVERIFIED", "rc1_step0": "SCF_UNVERIFIED", "rc1_no_rows": "SCF_UNVERIFIED",
                "rc1_two_runs": "SCF_UNVERIFIED", "rc1_it_mismatch_term": "SCF_UNVERIFIED", "crash_midstep": "RUN_FAILED", "crash_outcar_short": "RUN_FAILED",
                "crash_no_iter": "RUN_FAILED", "crash_no_header": "RUN_FAILED", "crash_outcar_ahead": "SCF_UNVERIFIED", "noterm_two_runs": "SCF_UNVERIFIED",
                "term_no_header": "SCF_UNVERIFIED", "rc0_noterm_midstep": "RUN_FAILED"}
        ck("판정 계약: 기대 상태 (NaN·Inf·별표·스텝 0·건너뜀·블록 둘·행 없음·NELM 초과 = 미확인 · rc 1/미종료 = 실행 실패 · 경계 = EDIFF 이하 수렴)",
           all(seen[k][1][0] == v for k, v in want.items()), {k: seen[k][1][0] for k, v in want.items() if seen[k][1][0] != v})
        v5same = all(((lambda r: ("SCF_UNVERIFIED" if r[3] else ("OK" if abs(r[1]) <= 1e-6 and abs(r[2]) <= 1e-6 else "SCF_NOT_CONVERGED")))(V.oszicar_last(probes[k][0]))) == want[k]
                     for k in ("ok", "noconv", "deps_only", "nan", "inf", "stars", "step0", "skip", "two_blocks", "no_rows"))
        ck("판정 계약: V5 검사기 계약 (4050264 · oszicar_last) 과 같은 탐침에서 같은 판정", v5same)
        ck("⛔음성 판정 계약: 'OUTCAR 문구 수렴' 이 아니라 OSZICAR 로 — NELM 소진 (EDIFF is reached 줄이 있어도) = 미수렴",
           judge_text(okrows.replace("-0.31E-07", "0.22E-02"), out_ok(25, " aborting loop because EDIFF is reached\n"), inc, 0)[0] == "SCF_NOT_CONVERGED")
        # ── 3. 러너 (가짜 VASP · 파일럿) ──
        POT = os.path.join(T, "pot")
        for sp_, t in ((POTCAR_MAP[e], PP_EXPECTED_TITEL[e]) for e in SPECIES_ORDER):
            os.makedirs(os.path.join(POT, sp_), exist_ok=True)
            open(os.path.join(POT, sp_, "POTCAR"), "w").write(f"   VRHFIN =X: s p\n   TITEL  = {t}\n   POMASS =   1.000; ZVAL   = {ZVAL[[e for e in SPECIES_ORDER if POTCAR_MAP[e] == sp_][0]]:8.3f}    mass and valenz\n")
        KER = os.path.join(T, "vdw_kernel.bindat"); open(KER, "wb").write(b"KERNEL" * 100)
        FV = os.path.join(T, "fake_vasp.py"); open(FV, "w").write(FAKE_VASP)
        en = {}
        for st_, e in (("S_A_bound", -2000.0), ("S_A_far", -1999.0), ("S_A_p05_bound", -1999.9), ("Li_A_bound", -1800.0), ("Li_A_far", -1799.2), ("Li_A_p05_bound", -1799.9),
                       ("S_A_G3_c2_bound", -2000.0), ("S_A_G3_c2_far_i", -1999.0), ("S_A_G3_c2_far_ii", -1999.0), ("CC_S33_AB_dft_bound", -100.0), ("CC_S33_AB_dft_far", -99.5)):
            en[st_] = e
        for n, j in J.items():
            if j["method"] == "optb88" and j["structure"].endswith("far"):
                en[n] = en[j["structure"]] + 0.1
        en["pz|P2S_S_A_far"] = 0.50; en["pz|P2S_S_A_G3_c2_far_ii"] = 0.505
        EF = os.path.join(T, "energy.json"); json.dump(en, open(EF, "w"))

        def runner_env(pkg, plan, **kw):
            pf = os.path.join(T, f"plan_{abs(hash(json.dumps(plan, sort_keys=True)))}.json"); json.dump(plan, open(pf, "w"))
            env = dict(os.environ, VASP_CMD=f"{sys.executable} {FV}", POTCAR_DIR=POT, VDW_KERNEL=KER, FAKE_PLAN=pf, FAKE_PKG=pkg, FAKE_ENERGY=EF, WATCH_S="1")
            env.update({k: str(v) for k, v in kw.items() if v is not None})
            for k in [k for k, v in kw.items() if v is None]:
                env.pop(k, None)
            return env

        def run_r(pkg, plan, args=(), **kw):
            r = subprocess.run(["bash", os.path.join(pkg, "run_all.sh"), *args], capture_output=True, text=True, env=runner_env(pkg, plan, **kw), timeout=600)
            return r.returncode, r.stdout + r.stderr
        plan_p = {"P2S_S_A_bound/0": "noconv", "P2S_S_A_bound/r1A": "noconv", "P2S_S_A_bound/r1B": "conv",
                  "P2S_S_A_far/0": "crash", "P2S_S_A_far/r1A": "noconv", "P2S_S_A_far/r1B": "noconv", "P2S_S_A_far/r2B": "conv",
                  "CC_S33_AB_optB88_far/0": "nan", f"{A4_JOB}/a4B": "ignore_wavecar"}
        rc, log_ = run_r(PKG, plan_p)
        st = {}
        for ln in open(os.path.join(PKG, "run", "status.tsv")).read().splitlines()[1:]:
            t = ln.split("\t"); st[(t[0], t[1])] = t[4]
        ck("러너 파일럿: 종료 1 (값 없는 잡 있음) · 사다리 — S_A bound 0 미수렴 → r1 ⓐ+ⓑ 수렴 · far 실행 실패 → r1 ⓑ 미수렴 → r2 ⓑ 수렴",
           rc == 1 and st.get(("P2S_S_A_bound", "0")) == "SCF_NOT_CONVERGED" and st.get(("P2S_S_A_bound", "r1B")) == "OK" and ("P2S_S_A_bound", "r2B") not in st
           and st.get(("P2S_S_A_far", "0")) == "RUN_FAILED" and st.get(("P2S_S_A_far", "r1B")) == "SCF_NOT_CONVERGED" and st.get(("P2S_S_A_far", "r2B")) == "OK", (rc, st, log_[-600:]))
        ck("러너 파일럿: NaN = SCF 미확인 → 승격 없음 (r1 없음) · a4 ⓑ 가 WAVECAR 를 안 읽음 → 재시작 미이행",
           st.get(("CC_S33_AB_optB88_far", "0")) == "SCF_UNVERIFIED" and not os.path.isdir(os.path.join(PKG, "run", "CC_S33_AB_optB88_far_r1"))
           and "RESTART_NOT_HONOURED" in log_, log_[-800:])
        ck("러너 파일럿: ⓐ WAVECAR — 채택(OK) 뒤 지움 · 재시작 미이행이면 남김 (검토용) · ⓑ 복사본은 지움",
           not os.path.exists(os.path.join(PKG, "run", "P2S_S_A_bound_r1", "stageA", "WAVECAR")) and os.path.exists(os.path.join(PKG, "run", f"{A4_JOB}_a4", "stageA", "WAVECAR"))
           and not os.path.exists(os.path.join(PKG, "run", "P2S_S_A_bound_r1", "WAVECAR")))
        mem = subprocess.run(["tar", "tzf", os.path.join(PKG, "round2_return.tgz")], capture_output=True, text=True).stdout.split()
        ck("러너 포장: sha 확인 통과 · WAVECAR·POTCAR·CHGCAR·커널 없음 · stageA 의 attempt.json·WAVECAR.info 있음",
           subprocess.run(["sha256sum", "-c", "round2_return.tgz.sha256"], cwd=PKG, capture_output=True).returncode == 0
           and not any(re.search(r"(^|/)(WAVECAR|POTCAR|CHGCAR|CHG|vasprun\.xml|vdw_kernel\.bindat)$", m_) for m_ in mem)
           and "run/P2S_S_A_bound_r1/stageA/attempt.json" in mem and "run/P2S_S_A_bound_r1/stageA/WAVECAR.info" in mem, [m_ for m_ in mem if "WAVECAR" in m_][:6])
        res = {n: resolve_job(J[n], PKG, os.path.join(PKG, "run")) for n in PILOT_JOBS}
        ck("검사기 = 러너 (파일럿): S_A bound OK@r1 · far OK@r2 · C–C optB88 bound 수렴이지만 등록부 전이라 KERNEL_UNVERIFIED (R4) · far SCF 미확인 · a4 재시작 미이행",
           res["P2S_S_A_bound"]["status"] == "OK" and res["P2S_S_A_bound"]["history"].get("r1B") == "OK" and res["P2S_S_A_far"]["history"].get("r2B") == "OK"
           and res["P2S_S_A_far"]["status"] == "OK" and res["CC_S33_AB_optB88_bound"]["status"] == "KERNEL_UNVERIFIED"
           and res["CC_S33_AB_optB88_bound"].get("judge", {}).get("status") == "OK" and res["CC_S33_AB_optB88_far"]["status"] == "SCF_UNVERIFIED"
           and res[A4_JOB]["status"] == "RESTART_NOT_HONOURED", {n: (r["status"], r.get("history"), r.get("why")) for n, r in res.items()})
        nst = len(open(os.path.join(PKG, "run", "status.tsv")).read().splitlines())
        rc2, _ = run_r(PKG, plan_p)
        ck("러너 이어 돌리기: 끝난 시도는 다시 돌지 않는다 (status.tsv 줄 수 같음) · 같은 종료 1", rc2 == 1 and len(open(os.path.join(PKG, "run", "status.tsv")).read().splitlines()) == nst)
        # ── 4. 등록부 · 해제 · 본 단계 ──
        v5r = os.path.join(T, "v5reg.json")
        json.dump({"vasp_version": "vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex",
                   "species_sha256": {p_: _sha(os.path.join(POT, p_, "POTCAR")) for p_ in ("Li_sv", "P", "S", "Cl", "Ag")}}, open(v5r, "w"))
        KREG = "vdW kernel read from"                    # 가짜 VASP 의 커널 읽기 문구 (실물 문구는 파일럿 원문으로 정한다)
        reg = seal_registry(PKG, PKG, msha, v5_registry=v5r, kernel_read_regex=KREG)
        ck("등록부: 6 종 (C 포함) · 커널 sha · VASP 빌드 · 파일럿 run_id 5", set(reg["species_sha256"]) == set(POTCAR_MAP.values()) and reg["kernel_sha256"] == _sha(KER)
           and len(reg["from_pilot"]) == 5, reg["from_pilot"])
        bad_v5 = os.path.join(T, "v5bad.json"); json.dump({"vasp_version": "vasp.6.4.2 other", "species_sha256": {}}, open(bad_v5, "w"))
        try:
            seal_registry(PKG, PKG, msha, v5_registry=bad_v5); bad = False
        except PkgError as e:
            bad = "V5" in str(e)
        ck("⛔음성 등록부: VASP 빌드가 V5 와 다르면 봉인하지 않는다 (은 a4 = 같은 빌드·같은 PP)", bad)
        # R2 (CZ Q-CZ-2 ②) — 재시작 긍정 문구 regex 는 파일럿 ⓑ 원문으로 확인한 것만 봉인한다
        regp = seal_registry(PKG, PKG, msha, restart_read_regex="reading WAVECAR", v5_registry=v5r)
        rcx = regp.get("restart_read_check") or {}
        ck("등록부 regex: 파일럿에서 ⓐ WAVECAR 를 읽은 ⓑ 셋 (S_A bound r1B · far r1B · far r2B) 에 맞고 새로 시작한 시도 여덟 (단 0 넷 · ⓐ 셋 · 되돌아간 a4B) 에는 안 맞는다 → 봉인",
           regp["restart_read_regex"] == "reading WAVECAR" and sorted(rcx.get("read", [])) == ["P2S_S_A_bound/r1B", "P2S_S_A_far/r1B", "P2S_S_A_far/r2B"]
           and len(rcx.get("not_read", [])) == 8 and f"{A4_JOB}/a4B" in rcx["not_read"] and not rcx.get("unknown"), rcx)
        for rx_, lab_, why_ in (("NO SUCH PHRASE", "읽은 ⓑ 원문에 없다", "안 맞음"), ("WAVECAR", "새로 시작한 시도에도 맞는다 — 구별 못 함", "새로 시작한 시도에 맞음"),
                                ("(reading WAVECAR)?", "빈 문자열에도 맞는다", "빈 문자열"), ("(?i)READING wavecar", "(? 파이썬 확장", "(?"),
                                (r"reading\sWAVECAR", "역슬래시 — \\s 는 ERE 와 뜻이 갈린다", "허용 밖 글자"), ("[[:alpha:]]eading WAVECAR", "괄호 표현 — POSIX 클래스", "허용 밖 글자"),
                                ("reading WAVECAR{1}", "중괄호", "허용 밖 글자"), ("reading( WAVECAR", "파이썬 컴파일 실패", "컴파일")):
            try:
                seal_registry(PKG, PKG, msha, restart_read_regex=rx_, v5_registry=v5r); msg_ = "(봉인됨)"
            except PkgError as e:
                msg_ = str(e)
            ck(f"⛔음성 등록부 regex ({lab_}): 봉인하지 않는다 · 사유 '{why_}'", "regex" in msg_ and why_ in msg_, msg_)
        tcr = os.path.join(T, "tz_cr"); shutil.copytree(PKG, tcr, ignore=shutil.ignore_patterns("round2_return*"))
        open(os.path.join(tcr, "run", "P2S_S_A_bound_r1", "stdout.log"), "w", newline="").write(" running on   64 total cores\r reading WAVECAR\n")
        try:
            seal_registry(tcr, tcr, msha, restart_read_regex="^ reading WAVECAR", v5_registry=v5r); msg_ = "(봉인됨)"
        except PkgError as e:
            msg_ = str(e)
        ck("⛔음성 등록부 regex (stdout 에 \\r 로 붙은 줄): grep 처럼 한 줄로 읽어 '안 맞음' (두 엔진 갈림 아님 — 검사기는 줄바꿈을 바꾸지 않고 읽는다)",
           "안 맞음" in msg_ and "갈림" not in msg_, msg_)
        import types
        real_sp = globals()["subprocess"]
        globals()["subprocess"] = types.SimpleNamespace(run=lambda *a_, **k_: types.SimpleNamespace(returncode=1))      # grep 이 늘 '안 맞음' 이라고 답하는 가짜
        try:
            seal_registry(PKG, PKG, msha, restart_read_regex="reading WAVECAR", v5_registry=v5r); msg_ = "(봉인됨)"
        except PkgError as e:
            msg_ = str(e)
        finally:
            globals()["subprocess"] = real_sp
        ck("⛔음성 등록부 regex (러너 grep 과 검사기 파이썬이 다른 답 — 가짜 grep): 봉인하지 않는다 · 사유 '두 엔진 갈림'", "두 엔진 갈림" in msg_, msg_)
        rf = os.path.join(T, "release.tsv")
        _write(rf, release_text(reg, ["1", "2", "3", "4"], {"1": 170, "2": 586, "3": 204, "4": 24}, 1080, "R2-REL-TEST"))
        rc3, log3 = run_r(PKG, {}, (), STAGES="1 2 3 4")
        ck("⛔음성 해제: P 밖 단계를 해제 파일 없이 → 종료 2 (아무것도 안 돎)", rc3 == 2 and not os.path.isdir(os.path.join(PKG, "run", "P2S_Li_A_bound")), log3[-200:])
        rc4, log4 = run_r(PKG, {}, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256="0" * 64)
        ck("⛔음성 해제: sha 가 다르면 종료 2", rc4 == 2, log4[-200:])
        plan_m = {"P2S_Li_A_bound/0": "zero", "P2S_S_A_G3_c2_far_i/0": "noconv", "P2S_S_A_G3_c2_far_i/r1A": "badwav", "P2S_Li_A_optB88_far/0": "step0"}
        rc5, log5 = run_r(PKG, plan_m, (), STAGES="1 2 3 4", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf))
        res5 = {n: resolve_job(J[n], PKG, os.path.join(PKG, "run"), reg) for n in J if J[n]["stage"] != "P"}
        ck("러너 본 단계: 종료 1 · 0 스텝 = 미확인 · ⓐ WAVECAR 머리 불일치 = ⓐ 자격 미달 (ⓑ 없음) · 스텝 0 = 미확인 · 나머지 OK",
           rc5 == 1 and res5["P2S_Li_A_bound"]["status"] == "SCF_UNVERIFIED" and res5["P2S_S_A_G3_c2_far_i"]["status"] == "STAGE_A_INELIGIBLE"
           and not os.path.isdir(os.path.join(PKG, "run", "P2S_S_A_G3_c2_far_i_r1", ".b")) and res5["P2S_Li_A_optB88_far"]["status"] == "SCF_UNVERIFIED"
           and sum(r["status"] == "OK" for r in res5.values()) == 16, ({n: r["status"] for n, r in res5.items() if r["status"] != "OK"}, log5[-500:]))
        rcA, logA = run_r(PKG, {}, ("--infra-abort", "P2S_S_A_G3_c2_far_i", "0", "SGE-1", "2026-10-20T00:00Z", "test"))
        ck("⛔음성 0 스텝 기록: 전자 반복행이 있는 시도는 거부 (실행 실패는 사다리 몫)", rcA == 2 and "0 스텝 중단이 아니다" in logA, logA[-200:])
        rcB, logB = run_r(PKG, {}, ("--infra-abort", "P2S_Li_A_bound", "0", "SGE-2", "2026-10-20T01:00Z", "node", "lost"), WALL_S="120")
        rc6, _ = run_r(PKG, {}, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf), JOBS="P2S_Li_A_bound")
        ck("0 스텝 기록 → 같은 단을 다시 돈다 → OK · run_aborted 에 보존 · 장부 tsv",
           rcB == 0 and rc6 == 0 and resolve_job(J["P2S_Li_A_bound"], PKG, os.path.join(PKG, "run"), reg)["status"] == "OK"
           and os.path.isfile(os.path.join(PKG, "run_aborted", "P2S_Li_A_bound_0_1", "infra_abort.json")) and os.path.isfile(os.path.join(PKG, "run", "infra_aborts.tsv")), (rcB, logB[-200:], rc6))
        # ── 5. 공통 환경 고장 · 상한 ──
        def fresh(name):
            d = os.path.join(T, name); shutil.copytree(PKG, d, ignore=shutil.ignore_patterns("run", "run_aborted", "round2_return*")); return d
        p1 = fresh("pk_nok")
        rc7, log7 = run_r(p1, {}, (), VDW_KERNEL=None)
        ck("⛔음성 공통 환경: optB88 잡이 있는데 커널 없음 → 종료 6 (전체 정지 · 묶음은 만듦)", rc7 == 6 and os.path.isfile(os.path.join(p1, "round2_return.tgz")), log7[-200:])
        p2 = fresh("pk_ver"); shutil.copytree(os.path.join(PKG, "run"), os.path.join(p2, "run"))
        shutil.rmtree(os.path.join(p2, "run", "P2S_Li_A_far")); [shutil.rmtree(x, ignore_errors=True) for x in (os.path.join(p2, "run", "P2S_Li_A_far_r1"),)]
        rc8, log8 = run_r(p2, {}, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf), JOBS="P2S_Li_A_far", FAKE_VERSION="vasp.6.4.2 other build")
        ck("⛔음성 공통 환경: VASP 빌드가 봉인과 다르면 → 종료 6", rc8 == 6 and "VASP 빌드" in log8, log8[-300:])
        p3 = fresh("pk_pp"); shutil.copytree(os.path.join(PKG, "run"), os.path.join(p3, "run")); shutil.rmtree(os.path.join(p3, "run", "P2S_Li_A_far"))
        pot2 = os.path.join(T, "pot2"); shutil.copytree(POT, pot2); open(os.path.join(pot2, "C", "POTCAR"), "a").write("   EXTRA\n")
        rc9, log9 = run_r(p3, {}, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf), JOBS="P2S_Li_A_far", POTCAR_DIR=pot2)
        ck("⛔음성 공통 환경: POTCAR 종별 sha 가 봉인과 다르면 → 종료 6 (띄우기 전)", rc9 == 6 and not os.path.isdir(os.path.join(p3, "run", "P2S_Li_A_far")), log9[-300:])
        rfk = os.path.join(T, "release_badk.tsv"); _write(rfk, release_text({**reg, "kernel_sha256": "f" * 64}, ["3"], {"3": 204}, 1080, "R2-BADK"))
        p4 = fresh("pk_ker")
        rc10, log10 = run_r(p4, {}, (), STAGES="3", RELEASE_FILE=rfk, RELEASE_SHA256=_sha(rfk))
        ck("⛔음성 공통 환경: vdW 커널 sha 가 봉인과 다르면 → 종료 6", rc10 == 6 and "커널" in log10, log10[-300:])
        p5 = fresh("pk_cap"); os.makedirs(os.path.join(p5, "run_aborted", "P2S_S_A_bound_0_1"))
        json.dump({"job": "P2S_S_A_bound", "rung": "0", "wall_s": str(118 * 3600)}, open(os.path.join(p5, "run_aborted", "P2S_S_A_bound_0_1", "infra_abort.json"), "w"))
        rc11, log11 = run_r(p5, {})
        ck("⛔음성 상한: 단계 P 누적 (0 스텝 중단 벽시계 118 h > 117 h) → 다음 잡 안 띄움 · 종료 5 · 묶음 만듦",
           rc11 == 5 and not os.path.isdir(os.path.join(p5, "run", "P2S_S_A_bound")) and os.path.isfile(os.path.join(p5, "round2_return.tgz")), log11[-300:])
        p6 = fresh("pk_watch")
        rc12, log12 = run_r(p6, {"P2S_S_A_bound/0": "slow"}, (), JOBS="P2S_S_A_bound")
        wl = _read(os.path.join(p6, "run", "P2S_S_A_bound", "warn.log")) or ""
        for beh_, lab_ in (("istart0_quiet", "문구 없이 ISTART 0 · ICHARG 2"), ("istart0_only", "ISTART 만 0 (ICHARG 0 · 문구 없음)"), ("icharg2_only", "ICHARG 만 2 (ISTART 1 · 문구 없음)")):
            p6b = fresh(f"pk_{beh_}")
            rc12b, log12b = run_r(p6b, {"P2S_S_A_bound/0": "noconv", "P2S_S_A_bound/r1A": "noconv", "P2S_S_A_bound/r1B": beh_}, (), JOBS="P2S_S_A_bound")
            ck(f"⛔음성 재시작 ({lab_}): 러너·검사기 둘 다 재시작 미이행 · r2 로 승격 안 함",
               rc12b == 1 and "RESTART_NOT_HONOURED" in log12b and not os.path.isdir(os.path.join(p6b, "run", "P2S_S_A_bound_r2"))
               and resolve_job(J["P2S_S_A_bound"], p6b, os.path.join(p6b, "run"))["status"] == "RESTART_NOT_HONOURED", log12b[-300:])
        ck("조기 경보: 120 스텝 뒤 |dE| 정체 → warn.log · env.txt (중단 아님 — 끝까지 돈다)", "dE_stall" in wl and os.path.isfile(os.path.join(p6, "run", "P2S_S_A_bound", "attempt.json")), (wl, log12[-300:]))
        # R1 끝에서 끝 (CZ Q-CZ-1 재현 ①) — 단 0 = 전자행 7 · rc 1 · 같은 버전 실행 머리줄 둘
        pR = fresh("pk_tworuns")
        rcR, logR = run_r(pR, {"P2S_S_A_bound/0": "crash_tworuns"}, (), JOBS="P2S_S_A_bound")
        stR = {}
        for ln in open(os.path.join(pR, "run", "status.tsv")).read().splitlines()[1:]:
            t_ = ln.split("\t"); stR[(t_[0], t_[1])] = t_[4]
        resR = resolve_job(J["P2S_S_A_bound"], pR, os.path.join(pR, "run"))
        ck("⛔음성 R1 끝에서 끝 (CZ 재현 ①): 단 0 전자행 7 · rc 1 · 머리줄 둘 → 러너 SCF_UNVERIFIED · r1 안 띄움 · 검사기도 단 0 에서 멈춤",
           rcR == 1 and stR.get(("P2S_S_A_bound", "0")) == "SCF_UNVERIFIED" and not os.path.isdir(os.path.join(pR, "run", "P2S_S_A_bound_r1"))
           and resR["status"] == "SCF_UNVERIFIED" and resR["history"] == {"0": "SCF_UNVERIFIED"}, (rcR, stR, resR.get("history"), logR[-300:]))
        if not os.path.isdir(os.path.join(pR, "run", "P2S_S_A_bound_r1")):                                                  # (러너가 r1 을 띄웠으면 위 시험이 이미 ✗)
            shutil.copytree(os.path.join(PKG, "run", "P2S_S_A_bound_r1"), os.path.join(pR, "run", "P2S_S_A_bound_r1"))   # CZ 사슬: 정상 r1 반송을 붙인다
        resR2 = resolve_job(J["P2S_S_A_bound"], pR, os.path.join(pR, "run"))
        ck("⛔음성 R1 (CZ 사슬 '0: RUN_FAILED → r1A OK → r1B OK → 최종 OK'): 정상 r1 을 붙여도 검사기는 단 0 SCF_UNVERIFIED 에서 멈춘다",
           resR2["status"] == "SCF_UNVERIFIED" and "r1B" not in resR2["history"], (resR2["status"], resR2.get("history")))
        # ── 6. 집계 (깨끗한 반송 · 가짜 UMA) ──
        p7 = fresh("pk_clean")
        rcc, logc = run_r(p7, {})
        reg7 = seal_registry(p7, p7, msha, v5_registry=v5r, kernel_read_regex=KREG)
        rf7 = os.path.join(T, "release7.tsv"); _write(rf7, release_text(reg7, ["1", "2", "3", "4"], {"1": 170, "2": 586, "3": 204, "4": 24}, 1080, "R2-7"))
        rcc2, logc2 = run_r(p7, {}, (), STAGES="1 2 3 4", RELEASE_FILE=rf7, RELEASE_SHA256=_sha(rf7))
        ck("깨끗한 반송: 파일럿 0 · 본 단계 0 (24 잡 OK)", rcc == 0 and rcc2 == 0, (logc[-300:], logc2[-300:]))
        A = J["P2S_S_A_bound"]["area_A2"]
        uma = {"schema": "uma_energies/v1", "calculator": {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default", "fairchem.core": "2.21.0",
                                                           "checkpoint": [{"sha256": V.UMA_REQ["checkpoint_sha256"]}]}, "energies": {}}
        for n in UMA_NAMES + UMA_G3:
            j = next(x for x in meta["jobs"] if x["structure"] == n and x["method"] == "pbed3")
            uma["energies"][n] = {"sha256": j["structure_sha256"], "n_atoms": j["nions"], "pbc": [True, True, True], "E_UMA_eV": en[n] + 0.001}          # UMA (D3 없음) = 가짜 표의 전자 값
        r7 = collect(p7, p7, msha, uma, reg7)
        ck("집계 (깨끗): G3 PASS · G4 PASS · G5_C PASS · 80 % 발동 없음 · 실패 전파 비어 있음",
           r7["G3"]["status"] == "PASS" and r7["G4"]["status"] == "PASS" and r7["G5_C"]["status"] == "PASS" and not r7["trigger_80pct"]["triggered"]
           and not any(r7["failure_propagation"][k] for k in ("G5_C", "delta_XC_vdW", "CC_control", "silver_a4")), (r7["G3"]["status"], r7["G4"]["status"], r7["G5_C"]["status"]))
        ck("집계: Δ_C = W_VASP − (W_UMA + ΔD3_VASP) (가짜 값에서 0 · |Δ| < 1e-6 — Edisp 인쇄 5 자리) · δ = W_optB88 − W_PBE (0.1 eV/A) · C–C 두 방법 차이",
           all(abs(r7["samples"][k]["Delta_C_J_m2"]) < 1e-6 for k in SAMPLES) and abs(r7["delta_XC_vdW"]["S_A"]["delta_J_m2"] - 0.1 * V.EV_J / (A * V.A2_M2)) < 1e-9
           and r7["CC_control"]["optb88_minus_pbed3_J_m2"] is not None, {k: r7["samples"][k]["Delta_C_J_m2"] for k in SAMPLES})
        dS = r7["delta_XC_vdW"]["S_A"]; wr_, s__ = dS["W_ref_PBE_D3_J_m2"], dS["s_J_m2"]
        rule = ("백분율" if (wr_ > 0 and abs(wr_) >= 10 * s__) else "절대 차이만")
        ck(f"δ 라벨 규칙: W_ref {wr_:.4f} · s {s__:.4f} → {rule} (10 s 조건 · s ≥ 0.01) · 백분율이면 20 % 문턱 라벨", (rule == "절대 차이만" and dS["label"] == "절대 차이만 (해석 보류)" and "pct" not in dS)
           or (rule == "백분율" and "pct" in dS and dS["label"] == ("함수 선택 (XC+vdW) 민감" if dS["pct"] > 20 else "백분율 표기 가능")), dS)
        ck("집계: far 진단 (p_z · 쌍극 보정 · E-fermi · ΔV) · 신호 ⓐ 없음 (|Δp_z| 0.005 < 0.02)", r7["far_diagnostics"]["P2S_S_A_far"]["p_z_eA"] == 0.5
           and r7["far_diagnostics"]["P2S_S_A_far"]["E_fermi_eV"] == 0.9032 and not r7["charge_transfer_signals"]["signals"], r7["charge_transfer_signals"])
        r7b = collect(p7, p7, msha, None, reg7)
        r7c = collect(p7, p7, msha, uma, None)
        ck("⛔음성 집계: UMA 없음 → G5_C BLOCKED · 등록부 없음 → BLOCKED (파일럿 단계)", r7b["G5_C"]["status"].startswith("BLOCKED (UMA") and r7c["G5_C"]["status"].startswith("BLOCKED (PP"),
           (r7b["G5_C"]["status"], r7c["G5_C"]["status"]))
        u2 = json.loads(json.dumps(uma)); u2["energies"]["Li_A_far"]["E_UMA_eV"] += 0.7
        r7d = collect(p7, p7, msha, u2, reg7)
        ck("⛔음성 집계: Li_A 표본 UMA 가 0.7 eV 어긋나면 G5_C FAIL (표본 0.03 · 편향 0.02) · 종료 10", r7d["G5_C"]["status"] == "FAIL" and collect_exit(r7d) == 10,
           (r7d["G5_C"]["status"], r7d["G5_C"]["signed_bias"]))
        u3 = json.loads(json.dumps(uma)); u3["calculator"]["checkpoint"] = [{"sha256": "0" * 64}]
        ck("⛔음성 집계: UMA 체크포인트 결박이 다르면 BLOCKED", collect(p7, p7, msha, u3, reg7)["G5_C"]["status"].startswith("BLOCKED (UMA"))
        Jd = {x["structure"]: x["d3_2body_eV_ref"] for x in meta["jobs"] if "d3_2body_eV_ref" in x}
        dD3ii = ((Jd["S_A_G3_c2_far_ii"] - Jd["S_A_G3_c2_bound"]) - (Jd["S_A_far"] - Jd["S_A_bound"])) * V.EV_J / (A * V.A2_M2)
        en2 = dict(en); en2["S_A_G3_c2_far_ii"] = en["S_A_G3_c2_far_ii"] + (0.0085 - dD3ii) * A * V.A2_M2 / V.EV_J; en2["pz|P2S_S_A_G3_c2_far_ii"] = 0.53
        en2["edisp_shift|P2S_S_A_G4_k62_far"] = 2e-4
        dD3Li = (Jd["Li_A_far"] - Jd["Li_A_bound"])                                   # eV — Li_A 의 W_ref 를 0.05 J/m² (< 10 s = 0.1) 로 맞춘다
        en2["Li_A_far"] = en["Li_A_bound"] + 0.05 * A * V.A2_M2 / V.EV_J - dD3Li; en2["P2S_Li_A_optB88_far"] = en2["Li_A_far"] + 0.1
        json.dump(en2, open(EF, "w"))
        p8 = fresh("pk_trig")
        run_r(p8, {}); reg8 = seal_registry(p8, p8, msha, v5_registry=v5r, kernel_read_regex=KREG)
        rf8 = os.path.join(T, "release8.tsv"); _write(rf8, release_text(reg8, ["1", "2", "3", "4"], {"1": 170, "2": 586, "3": 204, "4": 24}, 1080, "R2-8"))
        run_r(p8, {}, (), STAGES="1 2 3 4", RELEASE_FILE=rf8, RELEASE_SHA256=_sha(rf8))
        r8 = collect(p8, p8, msha, uma, reg8)
        ck("80 % 발동: G3 (ii) PASS 인데 |ΔW| 0.0085 > 0.008 → 발동 기록 (판정은 그대로 PASS) · 신호 ⓐ |Δp_z| 0.03 · ⓑ PBE 몫 → 라벨",
           r8["G3"]["status"] == "PASS" and r8["trigger_80pct"]["triggered"] and any("G3 ii" in x for x in r8["trigger_80pct"]["checks"])
           and len(r8["charge_transfer_signals"]["signals"]) == 2 and "분리 끝점의 전자 상태 미확인" in r8["G5_C"]["labels"], (r8["trigger_80pct"], r8["charge_transfer_signals"]))
        dL = r8["delta_XC_vdW"]["Li_A"]
        ck("δ 라벨: W_ref 0.05 < 10 s (0.1) → 백분율 없이 '절대 차이만 (해석 보류)'", abs(dL["W_ref_PBE_D3_J_m2"] - 0.05) < 1e-4 and dL["label"] == "절대 차이만 (해석 보류)"
           and "pct" not in dL, dL)
        ck("⛔음성 G4: 같은 기하인데 Edisp 가 2e-4 eV 다르면 그 단계 INCOMPLETE (D3 불일치) → G4 INCOMPLETE → G5_C 오차표만",
           r8["G4"]["k"]["status"].startswith("INCOMPLETE (D3") and r8["G4"]["status"] == "INCOMPLETE" and r8["G5_C"]["status"].startswith("INCOMPLETE (G3"), (r8["G4"]["k"], r8["G5_C"]["status"]))
        json.dump(en, open(EF, "w"))
        r5c = collect(PKG, PKG, msha, uma, reg)
        ck("실패 전파: G3 far_i ⓐ 자격 미달 → G3 INCOMPLETE → G5_C 'INCOMPLETE (오차표만)' · optB88 Li_A far 미확인 → δ Li_A 만 미완료 · C–C far 미확인 → ②′ 만",
           r5c["G3"]["status"] == "INCOMPLETE" and r5c["G5_C"]["status"].startswith("INCOMPLETE (G3") and r5c["delta_XC_vdW"]["Li_A"]["label"].startswith("δ 미완료")
           and r5c["delta_XC_vdW"]["S_A"]["delta_J_m2"] is not None and "CC_S33_AB_optB88_far" in r5c["failure_propagation"]["CC_control"]
           and r5c["failure_propagation"]["silver_a4"] == [A4_JOB], (r5c["G3"]["status"], r5c["G5_C"]["status"], r5c["failure_propagation"]))
        # ── 7. 검사기 음성 (손댄 반송) ──
        tam = os.path.join(T, "tam"); shutil.copytree(p7, tam)
        ib = os.path.join(tam, "run", "P2S_S_A_bound", "INCAR"); open(ib, "a").write("ALGO = Fast\n")
        ck("⛔음성 검사기: 실행 뒤 INCAR 를 고치면 ATTEMPT_MISMATCH", resolve_job(J["P2S_S_A_bound"], tam, os.path.join(tam, "run"), reg7)["status"] == "ATTEMPT_MISMATCH")
        tam2 = os.path.join(T, "tam2"); shutil.copytree(p7, tam2)
        aj = os.path.join(tam2, "run", "CC_S33_AB_optB88_bound", "attempt.json"); a_ = json.load(open(aj)); a_["kernel_sha256"] = "e" * 64; json.dump(a_, open(aj, "w"))
        ck("⛔음성 검사기: 커널 sha 가 등록부와 다르면 KERNEL_MISMATCH (공통 환경 고장 → 집계 종료 6)",
           resolve_job(J["CC_S33_AB_optB88_bound"], tam2, os.path.join(tam2, "run"), reg7)["status"] == "KERNEL_MISMATCH" and collect_exit(collect(tam2, tam2, msha, uma, reg7)) == 6)
        tam3 = os.path.join(T, "tam3"); shutil.copytree(PKG, tam3)
        wi = os.path.join(tam3, "run", "P2S_S_A_bound_r1", "WAVECAR.info"); w_ = json.load(open(wi)); w_["copied_sha256"] = "d" * 64; open(wi, "w").write(json.dumps(w_) + "\n")
        aj = os.path.join(tam3, "run", "P2S_S_A_bound_r1", "attempt.json"); a_ = json.load(open(aj)); a_["sha256"]["WAVECAR.info"] = _sha(wi); json.dump(a_, open(aj, "w"))
        ck("⛔음성 검사기: ⓑ 복사본 sha ≠ ⓐ sha → 재시작 미이행 (수렴했어도 자동 채택 안 함)",
           resolve_job(J["P2S_S_A_bound"], tam3, os.path.join(tam3, "run"))["status"] == "RESTART_NOT_HONOURED")
        # R2 (CZ Q-CZ-2) — ⓐ→ⓑ 결박 · ⓐ 머리 = 실제 OUTCAR · 재시작 문구 (재현 셋 + 양성 · 러너 이어 돌리기도 같은 답)
        def edit_info(att, fn):                       # WAVECAR.info 를 고치고 attempt.json 의 sha 를 맞춘다 (기록끼리는 일관된 위조)
            wi_ = os.path.join(att, "WAVECAR.info"); w__ = json.load(open(wi_)); fn(w__); open(wi_, "w").write(json.dumps(w__) + "\n")
            aj_ = os.path.join(att, "attempt.json"); a__ = json.load(open(aj_)); a__["sha256"]["WAVECAR.info"] = _sha(wi_); json.dump(a__, open(aj_, "w"))
        other = lambda w: w.update(src_sha256="c" * 64, copied_sha256="c" * 64, end_sha256="c" * 64)
        tz1 = os.path.join(T, "tz1"); shutil.copytree(PKG, tz1)
        edit_info(os.path.join(tz1, "run", "P2S_S_A_bound_r1"), other)
        rz1 = resolve_job(J["P2S_S_A_bound"], tz1, os.path.join(tz1, "run"))
        rcz1, logz1 = run_r(tz1, {}, (), JOBS="P2S_S_A_bound")
        ck("⛔음성 R2 (CZ 재현 ①): ⓑ src/copied/end 를 다른 같은 sha 로 (ⓐ 그대로 · 기록 sha 맞춤) → 검사기 재시작 미이행 · 러너 이어 돌리기도 같은 답 (r2 안 띄움)",
           rz1["status"] == "RESTART_NOT_HONOURED" and "이 ⓐ 의 WAVECAR 가 아니다" in rz1.get("why", "") and rcz1 == 1 and "RESTART_NOT_HONOURED" in logz1
           and not os.path.isdir(os.path.join(tz1, "run", "P2S_S_A_bound_r2")), (rz1["status"], rz1.get("why"), rcz1, logz1[-300:]))
        tz2 = os.path.join(T, "tz2"); shutil.copytree(PKG, tz2)
        edit_info(os.path.join(tz2, "run", "P2S_S_A_far_r2"), other)
        rz2 = resolve_job(J["P2S_S_A_far"], tz2, os.path.join(tz2, "run"))
        rcz2, logz2 = run_r(tz2, {}, (), JOBS="P2S_S_A_far")
        ck("⛔음성 R2: r2 ⓑ 도 r1 ⓐ WAVECAR 에 결박 (r2 src/copied/end 를 다른 같은 sha 로) → 검사기·러너 재시작 미이행 (손 안 댄 r2 는 파일럿 시험에서 OK)",
           rz2["status"] == "RESTART_NOT_HONOURED" and rz2["history"].get("r2B") == "RESTART_NOT_HONOURED" and rcz2 == 1 and "RESTART_NOT_HONOURED" in logz2,
           (rz2["status"], rz2.get("history"), rcz2, logz2[-300:]))
        rz8 = check_attempt(J["P2S_S_A_bound"], PKG, os.path.join(PKG, "run", "P2S_S_A_bound_r1"), "r1B")
        ck("⛔음성 R2: ⓑ 를 ⓐ 검사 기록 없이 검사하면 재시작 미이행 (결박할 ⓐ 가 없다)", rz8["status"] == "RESTART_NOT_HONOURED", (rz8["status"], rz8.get("why")))
        rz3 = resolve_job(J[A4_JOB], p7, os.path.join(p7, "run"), {**reg7, "restart_read_regex": "NO SUCH PHRASE"})
        ck("⛔음성 R2 (CZ 재현 ②): 등록부 restart_read_regex 가 원문에 없는 문구 → 재시작 미이행 (러너 honoured 를 믿지 않고 원문을 다시 본다)",
           rz3["status"] == "RESTART_NOT_HONOURED" and "NO SUCH PHRASE" in rz3.get("why", ""), (rz3["status"], rz3.get("why")))
        pz = os.path.join(T, "pk_rx"); shutil.copytree(p7, pz)
        for x_ in ("P2S_Li_A_far", "P2S_Li_A_far_r1", "P2S_Li_A_far_r2"):
            shutil.rmtree(os.path.join(pz, "run", x_), ignore_errors=True)
        regz = seal_registry(pz, pz, msha, restart_read_regex="reading WAVECAR", v5_registry=v5r)
        rfz = os.path.join(T, "release_rx.tsv"); _write(rfz, release_text(regz, ["1"], {"1": 170}, 1080, "R2-RX"))
        plan_z = {"P2S_Li_A_far/0": "noconv", "P2S_Li_A_far/r1A": "noconv", "P2S_Li_A_far/r1B": "conv"}
        rcz4, logz4 = run_r(pz, plan_z, (), STAGES="1", RELEASE_FILE=rfz, RELEASE_SHA256=_sha(rfz), JOBS="P2S_Li_A_far")
        rz4 = resolve_job(J["P2S_Li_A_far"], pz, os.path.join(pz, "run"), regz)
        wz4 = json.load(open(os.path.join(pz, "run", "P2S_Li_A_far_r1", "WAVECAR.info")))
        ck("R2 양성: 파일럿 원문으로 봉인한 regex ('reading WAVECAR') 해제 파일 → 러너 ⓑ 긍정 문구 맞음 · OK · 검사기도 OK@r1B",
           rcz4 == 0 and wz4.get("positive_regex_match") == "1" and rz4["status"] == "OK" and rz4["history"].get("r1B") == "OK", (rcz4, wz4, rz4["status"], rz4.get("why"), logz4[-300:]))
        rfz2 = os.path.join(T, "release_rx2.tsv"); _write(rfz2, release_text({**regz, "restart_read_regex": "NO SUCH PHRASE"}, ["1"], {"1": 170}, 1080, "R2-RX2"))
        rcz5, logz5 = run_r(pz, plan_z, (), STAGES="1", RELEASE_FILE=rfz2, RELEASE_SHA256=_sha(rfz2), JOBS="P2S_Li_A_far")
        rz5 = resolve_job(J["P2S_Li_A_far"], pz, os.path.join(pz, "run"), {**regz, "restart_read_regex": "NO SUCH PHRASE"})
        ck("⛔음성 R2 (이어 돌리기 · 같은 ⓑ 기록을 원문에 없는 문구 regex 해제 파일로): 러너 stat_of 도 원문을 다시 봐서 재시작 미이행 · r2 안 띄움 · 검사기도",
           rcz5 == 1 and "RESTART_NOT_HONOURED" in logz5 and not os.path.isdir(os.path.join(pz, "run", "P2S_Li_A_far_r2")) and rz5["status"] == "RESTART_NOT_HONOURED",
           (rcz5, logz5[-300:], rz5["status"]))
        tz6 = os.path.join(T, "tz6"); shutil.copytree(PKG, tz6)

        def nb999(w):
            hd_ = w["head"].split(); hd_[4] = "999"; w["head"] = " ".join(hd_); w["outcar"]["NBANDS"] = "999"
        edit_info(os.path.join(tz6, "run", "P2S_S_A_bound_r1", "stageA"), nb999)
        rz6 = resolve_job(J["P2S_S_A_bound"], tz6, os.path.join(tz6, "run"))
        ck("⛔음성 R2 (CZ 재현 ③): ⓐ WAVECAR.info 머리·OUTCAR 사본 NBANDS 를 둘 다 999 로 (기록 sha 맞춤 · 실물 OUTCAR 512) → ⓐ 자격 미달",
           rz6["status"] == "STAGE_A_INELIGIBLE", (rz6["status"], rz6.get("why")))
        tz7 = os.path.join(T, "tz7"); shutil.copytree(PKG, tz7)
        a4d = os.path.join(tz7, "run", f"{A4_JOB}_a4")
        for x_ in os.listdir(a4d):                                     # ⓑ 를 띄우기 전에 끊긴 상태 (ⓐ 와 그 WAVECAR 만 남긴다)
            if x_ != "stageA":
                p_ = os.path.join(a4d, x_); shutil.rmtree(p_) if os.path.isdir(p_) else os.remove(p_)
        edit_info(os.path.join(a4d, "stageA"), lambda w: w["outcar"].update(NBANDS="999"))
        rz7 = resolve_job(J[A4_JOB], tz7, os.path.join(tz7, "run"))
        rcz7, logz7 = run_r(tz7, {}, (), JOBS=A4_JOB)
        ck("⛔음성 R2: ⓐ WAVECAR.info 의 OUTCAR 사본만 999 (머리 = 실물 512) → 검사기 ⓐ 자격 미달 · 러너 이어 돌리기도 ⓑ 를 안 띄운다",
           rz7["status"] == "STAGE_A_INELIGIBLE" and "사본" in rz7.get("why", "") and rcz7 == 1 and not os.path.isdir(os.path.join(a4d, ".b")) and "자격 미달" in logz7,
           (rz7["status"], rz7.get("why"), rcz7, logz7[-300:]))
        # R3 (CZ Q-CZ-3) — 모든 시도의 환경 감사 · 질문별 실패 · 파일럿 결박 · 재개 ⓑ 의 PP · 상한 값
        ea = env_audit([("x/0", {"status": "SETTINGS_MISMATCH", "why": "a", "conflicts": ["SETTINGS_MISMATCH: a", "VERSION_MISMATCH: b"]}),
                        ("y/0", {"status": "OK", "version": "v1"}), ("z/0", {"status": "OK", "version": "v1"})])
        ck("R3 환경 감사 계약: status 가 다른 모순이어도 conflicts 안의 환경 등급을 잡는다 · 같은 버전 둘은 갈림이 아니다", [e[1] for e in ea] == ["VERSION_MISMATCH"], ea)
        def seal_msg(pk):
            try:
                return seal_registry(pk, pk, msha, v5_registry=v5r), "-"
            except PkgError as e:
                return None, str(e)
        pv = fresh("pk_a4ver")
        rcv, logv = run_r(pv, {f"{A4_JOB}/a4A": "otherver"})
        regv, msgv = seal_msg(pv)
        ck("⛔음성 R3 (CZ 재현 P0): 파일럿 a4A 만 다른 VASP 빌드 (a4B 정상 · 러너 종료 0) → 봉인하지 않는다 (최종 a4B 만 보면 봉인됐다)",
           rcv == 0 and regv is None and "VERSION" in msgv, (rcv, msgv, logv[-200:]))
        pvf = os.path.join(T, "pk_a4ver_full"); shutil.copytree(p7, pvf)
        shutil.rmtree(os.path.join(pvf, "run", f"{A4_JOB}_a4")); shutil.copytree(os.path.join(pv, "run", f"{A4_JOB}_a4"), os.path.join(pvf, "run", f"{A4_JOB}_a4"))
        rv = resolve_job(J[A4_JOB], pvf, os.path.join(pvf, "run"), reg7)
        cv = collect(pvf, pvf, msha, uma, reg7)
        ck("⛔음성 R3 (CZ 재현 P0): 등록부로 보면 a4 는 VERSION_MISMATCH (ⓐ 자격 미달 안에 묻히지 않는다 · 원래 값은 adopted_status) · 집계 공통 환경 고장 → G5_C BLOCKED · 종료 6",
           rv["status"] == "VERSION_MISMATCH" and rv.get("adopted_status") == "STAGE_A_INELIGIBLE" and bool(cv["common_environment_failure"])
           and cv["G5_C"]["status"].startswith("BLOCKED (공통 환경") and collect_exit(cv) == 6, (rv["status"], rv.get("adopted_status"), cv["common_environment_failure"], cv["G5_C"]["status"]))
        pc = fresh("pk_a4crash")
        rcc_, logc_ = run_r(pc, {f"{A4_JOB}/a4A": "crash"})
        regc, msgc = seal_msg(pc)
        ck("R3 (CZ 반대 방향): 파일럿 a4A 가 정상 환경에서 전자행을 남기고 충돌 (물리 실패 · 최종 ⓐ 자격 미달) → 탄소 등록부는 봉인된다 (v2 · a4 결박 = a4A 실행 하나)",
           regc is not None and regc["schema"] == "wad_round2_pp_registry/v2" and isinstance(regc["from_pilot"].get(A4_JOB), dict) and set(regc["from_pilot"][A4_JOB]) == {"a4A"}
           and set((regc["from_pilot_sha256"].get("P2S_S_A_bound") or {}).get("0") or {}) == {"attempt.json", "OUTCAR"}, (msgc, (regc or {}).get("from_pilot"), logc_[-200:]))
        tsx = os.path.join(T, "tz_extra"); shutil.copytree(PKG, tsx, ignore=shutil.ignore_patterns("round2_return*"))
        shutil.copytree(os.path.join(tsx, "run", "P2S_S_A_far_r2"), os.path.join(tsx, "run", "P2S_S_A_bound_r2"))
        regx, msgx = seal_msg(tsx)
        ck("⛔음성 R3: 사다리가 안 지나간 파일럿 시도도 본다 (S_A bound 는 r1 에서 OK 인데 남의 기록이 든 r2 폴더) → 봉인하지 않는다",
           regx is None and "ATTEMPT_MISMATCH" in msgx and "r2B" in msgx, msgx)
        tbl = os.path.join(T, "tbl"); shutil.copytree(p7, tbl)
        shutil.copytree(os.path.join(PKG, "run", "P2S_S_A_G3_c2_far_i_r1"), os.path.join(tbl, "run", "P2S_S_A_G3_c2_far_i_r1"))
        oc_ = os.path.join(tbl, "run", "P2S_S_A_G3_c2_far_i_r1", "stageA", "OUTCAR"); t_ = open(oc_).read(); open(oc_, "w").write(t_.replace(" vasp.5.4.4.18Apr17", " vasp.5.4.4.OTHER", 1))
        swapped_bl = "vasp.5.4.4.OTHER" in open(oc_).read() and "General timing" in open(oc_).read()
        aj_ = os.path.join(os.path.dirname(oc_), "attempt.json"); a__ = json.load(open(aj_)); a__["sha256"]["OUTCAR"] = _sha(oc_); json.dump(a__, open(aj_, "w"))
        rbl = resolve_job(J["P2S_S_A_G3_c2_far_i"], tbl, os.path.join(tbl, "run"))
        ck("⛔음성 R3: 단 0 이 OK 여도 사다리 밖 시도 (r1 ⓐ) 의 VASP 빌드가 다르면 VERSION_INCONSISTENT (등록부 없이도 · 시도 사이 갈림)",
           swapped_bl and rbl["status"] == "VERSION_INCONSISTENT" and rbl.get("adopted_status") == "OK" and set(rbl.get("attempts", {})) == {"0", "r1A"},
           (swapped_bl, rbl["status"], rbl.get("why"), list(rbl.get("attempts", {}))))
        tab = os.path.join(T, "tab"); shutil.copytree(p7, tab)
        abd = os.path.join(tab, "run_aborted", "P2S_Li_A_far_0_1"); shutil.copytree(os.path.join(tab, "run", "P2S_Li_A_far"), abd)
        oc_ = os.path.join(abd, "OUTCAR"); t_ = open(oc_).read(); open(oc_, "w").write(t_.replace(" vasp.5.4.4.18Apr17", " vasp.5.4.4.OTHER", 1))
        swapped_ab = "vasp.5.4.4.OTHER" in open(oc_).read() and "General timing" in open(oc_).read()
        aj_ = os.path.join(abd, "attempt.json"); a__ = json.load(open(aj_)); a__["sha256"]["OUTCAR"] = _sha(oc_); json.dump(a__, open(aj_, "w"))
        cab = collect(tab, tab, msha, uma, reg7)
        ck("⛔음성 R3: 0 스텝 중단으로 옮긴 시도 (run_aborted) 도 환경 감사 — 다른 VASP 빌드면 공통 환경 고장 · 종료 6",
           swapped_ab and bool(cab["common_environment_failure"]) and collect_exit(cab) == 6 and any("aborted" in x for x in cab["common_environment_failure"]),
           (swapped_ab, cab["common_environment_failure"]))
        tb = os.path.join(T, "tb"); shutil.copytree(p7, tb)
        aj_ = os.path.join(tb, "run", "P2S_S_A_bound", "attempt.json"); a__ = json.load(open(aj_)); a__["run_id"] = "20261020T000000-1-1"; json.dump(a__, open(aj_, "w"))
        rb1 = resolve_job(J["P2S_S_A_bound"], tb, os.path.join(tb, "run"), reg7)
        rgf = os.path.join(T, "reg7.json"); _write(rgf, json.dumps(reg7, ensure_ascii=False, indent=1) + "\n")
        cli = subprocess.run([sys.executable, "-I", os.path.abspath(__file__), "--check", "--out", tb, "--ret", tb, "--manifest_sha256", msha,
                              "--registry", rgf, "--registry_sha256", _sha(rgf)], capture_output=True, text=True)
        ck("⛔음성 R3 (CZ 재현 P1 · 파일럿 결박): 봉인 뒤 파일럿 run_id 를 바꾸면 PILOT_BINDING_MISMATCH · CLI --check 종료 3 (지금까지는 OK)",
           rb1["status"] == "PILOT_BINDING_MISMATCH" and rb1.get("adopted_status") == "OK" and cli.returncode == 3 and "PILOT_BINDING_MISMATCH" in cli.stdout,
           (rb1["status"], cli.returncode, cli.stdout[-300:], cli.stderr[-300:]))
        tb2 = os.path.join(T, "tb2"); shutil.copytree(p7, tb2)
        oc_ = os.path.join(tb2, "run", "CC_S33_AB_optB88_far", "OUTCAR"); open(oc_, "a").write(" \n")
        aj_ = os.path.join(tb2, "run", "CC_S33_AB_optB88_far", "attempt.json"); a__ = json.load(open(aj_)); a__["sha256"]["OUTCAR"] = _sha(oc_); json.dump(a__, open(aj_, "w"))
        rb2 = resolve_job(J["CC_S33_AB_optB88_far"], tb2, os.path.join(tb2, "run"), reg7)
        ck("⛔음성 R3 (파일럿 결박): 봉인 뒤 파일럿 OUTCAR 를 바꾸고 실행 기록 sha 를 맞춰도 PILOT_BINDING_MISMATCH", rb2["status"] == "PILOT_BINDING_MISMATCH"
           and rb2.get("adopted_status") == "OK", (rb2["status"], rb2.get("why")))
        tb3 = os.path.join(T, "tb3"); shutil.copytree(p7, tb3)
        shutil.copytree(os.path.join(PKG, "run", "P2S_S_A_bound_r1"), os.path.join(tb3, "run", "P2S_S_A_bound_r1"))
        rb3 = resolve_job(J["P2S_S_A_bound"], tb3, os.path.join(tb3, "run"), reg7)
        ck("⛔음성 R3 (파일럿 결박): 봉인에 없던 시도 (r1) 가 반송에 더 있으면 PILOT_BINDING_MISMATCH", rb3["status"] == "PILOT_BINDING_MISMATCH", (rb3["status"], rb3.get("why")))
        pq = fresh("pk_ppres")
        plan_q = {"P2S_Li_A_far/0": "noconv", "P2S_Li_A_far/r1A": "noconv", "P2S_Li_A_far/r1B": "ignore_wavecar"}
        rcq, logq = run_r(pq, plan_q, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf), JOBS="P2S_Li_A_far")
        r1d = os.path.join(pq, "run", "P2S_Li_A_far_r1")
        kept = os.path.isfile(os.path.join(r1d, "stageA", "WAVECAR"))
        for x_ in os.listdir(r1d):                                       # ⓑ 만 지운다 → 'ⓐ 끝 · ⓑ 전'
            if x_ != "stageA":
                p_ = os.path.join(r1d, x_); shutil.rmtree(p_) if os.path.isdir(p_) else os.remove(p_)
        rcq2, logq2 = run_r(pq, plan_q, (), STAGES="1", RELEASE_FILE=rf, RELEASE_SHA256=_sha(rf), JOBS="P2S_Li_A_far", POTCAR_DIR=pot2)
        ck("⛔음성 R3 (CZ P1 · 재개 ⓑ 의 PP): ⓐ 끝 · ⓑ 전에서 C POTCAR 를 바꾼 POTCAR_DIR 로 이어 돌리면 → 종료 6 · ⓑ 안 뜸 (.b 없음)",
           rcq == 1 and kept and rcq2 == 6 and not os.path.isdir(os.path.join(r1d, ".b")), (rcq, kept, rcq2, logq2[-300:]))
        bad_caps = []
        for v_ in (float("nan"), float("inf"), -1.0, 0.0, 1e7):
            for which in ("stage", "total"):
                try:
                    release_text(reg, ["1"], {"1": v_ if which == "stage" else 170}, v_ if which == "total" else 1080, "R3-CAP"); bad_caps.append((v_, which))
                except PkgError:
                    pass
        ck("⛔음성 R3 상한 값: release_text 가 nan · inf · 음수 · 0 · 러너가 못 읽는 표기 (1e+07) 상한 (단계·전체) 을 거부한다", not bad_caps, bad_caps)
        good_rel = release_text(reg, ["1"], {"1": 170}, 1080, "R3-NAN")
        for lab_, old_, new_ in (("단계 cap_h nan", "cap_h\t1\t170", "cap_h\t1\tnan"), ("전체 total_cap_h -5", "total_cap_h\t1080", "total_cap_h\t-5"),
                                 ("단계 cap_h 0", "cap_h\t1\t170", "cap_h\t1\t0")):
            rfn = os.path.join(T, f"release_{abs(hash(lab_))}.tsv"); _write(rfn, good_rel.replace(old_, new_))
            pn = fresh(f"pk_cap_{abs(hash(lab_))}")
            rcn, logn = run_r(pn, {}, (), STAGES="1", RELEASE_FILE=rfn, RELEASE_SHA256=_sha(rfn), JOBS="P2S_Li_A_far")
            ck(f"⛔음성 R3 상한 값: 러너가 해제 파일의 {lab_} 를 받으면 종료 2 (아무것도 안 돎)", new_ in open(rfn).read() and rcn == 2
               and not os.path.isdir(os.path.join(pn, "run", "P2S_Li_A_far")), (rcn, logn[-200:]))
        # R4 (CZ Q-CZ-5) — optB88: 실제 교환함수 · 커널 읽기 / 부재 / 재생성
        def outcar_edit(att, old_, new_):                # OUTCAR 한 곳을 바꾸고 실행 기록 sha 를 맞춘다 → 바뀌었는지
            oc_ = os.path.join(att, "OUTCAR"); t_ = open(oc_).read()
            if old_ not in t_:
                return False
            open(oc_, "w").write(t_.replace(old_, new_, 1))
            aj_ = os.path.join(att, "attempt.json"); a__ = json.load(open(aj_)); a__["sha256"]["OUTCAR"] = _sha(oc_); json.dump(a__, open(aj_, "w"))
            return True
        OB = "P2S_S_A_optB88_bound"                     # 파일럿 밖 optB88 잡 (파일럿 결박 대조 없이 설정·커널 감사만 본다)
        r40 = resolve_job(J[OB], p7, os.path.join(p7, "run"), reg7)
        ck("R4 양성: 커널 읽기 문구를 파일럿 원문으로 봉인한 등록부 → optB88 OK (GGA BO 확인 · 커널 상태 read)", r40["status"] == "OK" and r40.get("kernel_state") == "read",
           (r40["status"], r40.get("why"), r40.get("kernel_state")))
        t41 = os.path.join(T, "t41"); shutil.copytree(p7, t41)
        sw = outcar_edit(os.path.join(t41, "run", OB), "GGA     =    BO    GGA type", "GGA     =    PE    GGA type")
        r41 = resolve_job(J[OB], t41, os.path.join(t41, "run"), reg7)
        ck("⛔음성 R4 (CZ 재현 ①): optB88 OUTCAR 해석값 GGA = BO → PE → SETTINGS_MISMATCH (지금까지는 OK)", sw and r41["status"] == "SETTINGS_MISMATCH" and "GGA" in r41.get("why", ""),
           (sw, r41["status"], r41.get("why")))
        t42 = os.path.join(T, "t42"); shutil.copytree(p7, t42)
        sw = outcar_edit(os.path.join(t42, "run", OB), "   GGA     =    BO    GGA type\n", "")
        r42 = resolve_job(J[OB], t42, os.path.join(t42, "run"), reg7)
        ck("⛔음성 R4 (CZ 재현 ②): 해석 GGA 줄을 지우면 SETTINGS_UNVERIFIED (형식 못 읽음 = 미검증)", sw and r42["status"] == "SETTINGS_UNVERIFIED" and "GGA" in r42.get("why", ""),
           (sw, r42["status"], r42.get("why")))
        for lab_, new_, st_ in (("CZ 재현 ③ 'ERROR: vdw_kernel.bindat not read'", " ERROR: vdw_kernel.bindat not read", "not_read"),
                                ("CZ 재현 ④ 'kernel differs, recalculating vdW kernel'", " kernel differs, recalculating vdW kernel", "regenerated")):
            tk = os.path.join(T, f"t4k_{st_}"); shutil.copytree(p7, tk)
            sw = outcar_edit(os.path.join(tk, "run", OB), " vdW kernel read from vdw_kernel.bindat", new_)
            rk = resolve_job(J[OB], tk, os.path.join(tk, "run"), reg7)
            ck(f"⛔음성 R4 ({lab_}): KERNEL_NOT_READ ({st_}) · 환경 등급이라 집계 공통 환경 고장 · 종료 6 (지금까지는 OK)",
               sw and rk["status"] == "KERNEL_NOT_READ" and rk.get("kernel_state") == st_ and collect_exit(collect(tk, tk, msha, uma, reg7)) == 6,
               (sw, rk["status"], rk.get("kernel_state"), rk.get("why")))
        tks = os.path.join(T, "t4seal"); shutil.copytree(PKG, tks, ignore=shutil.ignore_patterns("round2_return*"))
        sw = outcar_edit(os.path.join(tks, "run", "CC_S33_AB_optB88_bound"), " vdW kernel read from vdw_kernel.bindat", " ERROR: vdw_kernel.bindat not read")
        try:
            seal_registry(tks, tks, msha, v5_registry=v5r, kernel_read_regex=KREG); msg_ = "(봉인됨)"
        except PkgError as e:
            msg_ = str(e)
        ck("⛔음성 R4: 파일럿 optB88 시도에 커널 부재 줄이 있으면 봉인하지 않는다 (KERNEL_NOT_READ)", sw and "KERNEL_NOT_READ" in msg_, (sw, msg_))
        tfp = os.path.join(T, "t4fp"); shutil.copytree(p7, tfp)
        open(os.path.join(tfp, "run", OB, "stdout.log"), "a").write(" WARNING: kernel module ib_uverbs not loaded (no RDMA) - falling back to TCP\n")
        rfp = resolve_job(J[OB], tfp, os.path.join(tfp, "run"), reg7)
        ck("R4 오탐 방지: MPI·OS 의 'kernel … not' 줄은 vdW 커널 줄이 아니다 → OK 그대로 (카드 §2.4 의 넓은 꼴 (?i)kernel 을 vdW 를 같이 말하는 줄로 좁혔다)",
           rfp["status"] == "OK", (rfp["status"], rfp.get("why")))
        r46 = [resolve_job(J[OB], p7, os.path.join(p7, "run"), rg_)["status"] for rg_ in (None, {**reg7, "kernel_read_regex": ""}, {**reg7, "kernel_read_regex": "NO SUCH KERNEL PHRASE"})]
        ck("⛔음성 R4: 등록부 없음 · 등록부에 커널 문구 없음 · 원문에 없는 문구 → optB88 수렴 시도도 KERNEL_UNVERIFIED", r46 == ["KERNEL_UNVERIFIED"] * 3, r46)
        kchk = reg.get("kernel_read_check") or {}
        ck("등록부 커널 문구: 파일럿 optB88 두 잡 (전자 스텝 ≥ 1) 에 맞고 optB88 아닌 시도에는 안 맞는다 → 봉인 · 해제 파일에 한 줄 · 러너가 env.txt 에 기록",
           reg.get("kernel_read_regex") == KREG and sorted(kchk.get("optb88", [])) == ["CC_S33_AB_optB88_bound/0", "CC_S33_AB_optB88_far/0"] and len(kchk.get("not_optb88", [])) >= 5
           and f"kernel_read_regex\t{KREG}" in release_text(reg, ["1"], {"1": 170}, 1080, "R4") and f"KERNEL_READ_RE {KREG}" in open(os.path.join(p7, "run", "env.txt")).read(), kchk)
        for rx_, why_ in (("NO SUCH KERNEL PHRASE", "안 맞음"), ("read", "optB88 아닌 시도에 맞음"), ("(?i)vdw kernel", "(?")):
            try:
                seal_registry(PKG, PKG, msha, v5_registry=v5r, kernel_read_regex=rx_); msg_ = "(봉인됨)"
            except PkgError as e:
                msg_ = str(e)
            ck(f"⛔음성 등록부 커널 문구 {rx_!r}: 봉인하지 않는다 · 사유 '{why_}'", "커널" in msg_ and why_ in msg_, msg_)
    finally:
        if os.environ.get("R2_SELFTEST_KEEP") == "1":
            print(f"  (시험 폴더 남김: {T})")
        else:
            shutil.rmtree(T, ignore_errors=True)
    print(f"{'✅' if n_bad == 0 else '⛔'} build_round2_vasp_package selftest {n_ok}/{n_ok + n_bad} 통과")
    return 0 if n_bad == 0 else 1


# ───────────────────────── CLI ─────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--seal", help="P2′ 봉인 폴더 (build_aprime_s3.py --seal_p2s 산출물)")
    ap.add_argument("--out", help="묶음 폴더")
    ap.add_argument("--ret", help="반송 run 폴더 (round2_return.tgz 을 푼 곳)")
    ap.add_argument("--manifest_sha256", help="보낸 묶음의 MANIFEST.sha256 sha256 (고정값)")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--seal_registry", metavar="OUT_JSON")
    ap.add_argument("--restart_read_regex", default="")
    ap.add_argument("--kernel_read_regex", default="", help="파일럿 원문으로 확정한 vdW 커널 읽기 문구 (없으면 optB88 은 KERNEL_UNVERIFIED)")
    ap.add_argument("--collect", metavar="OUT_JSON")
    ap.add_argument("--a4_result", metavar="OUT_JSON", help="은 a4 결과 (V5 검사기 --a4_result 입력 · 개정 4 채택은 V5 쪽에서)")
    ap.add_argument("--uma", help="uma_energies/v1 JSON (relax_uma_d3.py --energies)")
    ap.add_argument("--registry", help="봉인 등록부 JSON")
    ap.add_argument("--registry_sha256")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    if a.build:
        if not (a.seal and a.out):
            ap.error("--build 에는 --seal · --out")
        meta, msha = build(a.seal, a.out)
        print(f"✓ 묶음 {a.out} · 잡 {len(meta['jobs'])} · MANIFEST sha256 {msha}")
        return 0
    if not (a.out and a.ret and a.manifest_sha256):
        ap.error("--check · --seal_registry · --collect · --a4_result 에는 --out · --ret · --manifest_sha256")
    reg = None
    if a.registry:
        if not a.registry_sha256 or _sha(a.registry) != a.registry_sha256.lower():
            raise PkgError("등록부 sha 가 고정값과 다르다")
        reg = json.load(open(a.registry, encoding="utf-8"))
        if reg.get("schema") != REG_SCHEMA or reg.get("package_manifest_sha256") != a.manifest_sha256:
            raise PkgError("등록부 schema · 묶음 MANIFEST 가 맞지 않는다")
    if a.seal_registry:
        r = seal_registry(a.out, a.ret, a.manifest_sha256, a.restart_read_regex, kernel_read_regex=a.kernel_read_regex)
        _write(a.seal_registry, json.dumps(r, ensure_ascii=False, indent=1) + "\n")
        print(f"✓ 등록부 → {a.seal_registry} (sha256 {_sha(a.seal_registry)})")
        return 0
    if a.a4_result:
        V.verify_manifest(a.out, a.manifest_sha256)
        meta = json.load(open(os.path.join(a.out, "jobs.json"), encoding="utf-8"))
        run = os.path.join(a.ret, "run") if os.path.isdir(os.path.join(a.ret, "run")) else a.ret
        r = resolve_job({j["dir"]: j for j in meta["jobs"]}[A4_JOB], a.out, run, reg)
        _write(a.a4_result, json.dumps({"schema": "wad_round2_a4_result/v1", "job": A4_JOB, "package_manifest_sha256": a.manifest_sha256,
                                        "registry_sha256": a.registry_sha256, "result": r}, ensure_ascii=False, indent=1, default=float) + "\n")
        print(f"  a4 {r['status']} · 이력 {r.get('history')} → {a.a4_result} (sha256 {_sha(a.a4_result)})")
        return 0
    if a.check:
        V.verify_manifest(a.out, a.manifest_sha256)
        meta = json.load(open(os.path.join(a.out, "jobs.json"), encoding="utf-8"))
        run = os.path.join(a.ret, "run") if os.path.isdir(os.path.join(a.ret, "run")) else a.ret
        res = {j["dir"]: resolve_job(j, a.out, run, reg) for j in meta["jobs"]}
        for n, r in res.items():
            print(f"  {r['status']:<24s} {n}  {r.get('history')}")
        return 0 if all(r["status"] == "OK" for r in res.values()) else 3
    if a.collect:
        uma = json.load(open(a.uma, encoding="utf-8")) if a.uma else None
        rec = collect(a.out, a.ret, a.manifest_sha256, uma, reg)
        _write(a.collect, json.dumps(rec, ensure_ascii=False, indent=1, default=float) + "\n")
        print(f"  G3 {rec['G3']['status']} · G4 {rec['G4']['status']} · G5_C {rec['G5_C']['status']} · 80 % 발동 {rec['trigger_80pct']['triggered']} · "
              f"신호 {len(rec['charge_transfer_signals']['signals'])} · 미완 {rec['jobs_not_ok']} → {a.collect}")
        return collect_exit(rec)
    ap.error("--selftest · --build · --check · --seal_registry · --collect · --a4_result 중 하나")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PkgError as e:
        print(f"⛔ {e}")
        sys.exit(2)
