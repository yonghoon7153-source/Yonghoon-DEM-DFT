#!/usr/bin/env python3
"""build_v5_vasp_package.py — A′ V5 (LPSCl|Ag(111) 작은 주기 계면) **VASP 외주 패키지** · 반송 검사 · W/G3/G4/G5 집계. (v2 · Codex CE 반영)

왜 있나 (2026-09-27 · 1저자 "v5 관련해서 vasp 용으로 외주건으로 한번 만들어보고 codex 리뷰 받자 · 될지는 모르지만 준비는 해둬볼게")
  V5 는 우리 GPU 한 장(48 GB)에 안 들어가 RESOURCE_BLOCKED 였다 (QE CPU 추정 89–109 GB @70 Ry · 축소 변형도 61–80 GB).
  외주(큰 CPU 노드의 VASP)라면 들어간다. 이 도구는 **봉인된 S3v2 패키지를 입력으로 읽어** V5 18 잡을 VASP 로 옮긴다 —
  구조를 새로 만들지 않는다 (좌표는 S3v2 구조 파일 sha 로 결박 · 다르면 만들지 않는다).
왜 새 파일인가: QE 입력을 만든 `build_aprime_s3.py` 는 S3/S3v2 봉인에 파일 sha 로 결박돼 있다. 여기는 봉인 산출물만 읽는 번역기다.

v2 (Codex CE NO-GO 반영 · 2026-09-27) — 리뷰어가 재현한 통과 경로를 전부 막았다
  P0-1 성능 태그 = **제한 문법** (한 줄 한 대입 · `;` `\\` 금지 · 태그 중복 금지 · 태그별 값 타입) — 러너와 검사기가 같은 규칙
  P0-2 시도 폴더는 **새로만** (있으면 거부) · 성공 = rc 0 ∧ 종료 ∧ 수렴 ∧ OUTCAR 실행 1 개 · `attempt.json` 에 실행 ID·rc·입출력 sha 결박
       (실행 뒤 생기거나 바뀌거나 없어진 파일 → ATTEMPT_MISMATCH) · OUTCAR 복수 실행 MULTIPLE_RUNS
       · **실제 해석된 설정 되울림** (ENCUT·ISMEAR·SIGMA·ISPIN·NIONS·NELECT·IVDW·LDIPOL·IDIPOL·DIPOL · EFIELD ≠ 0 금지) 대조 — 못 읽으면 통과가 아니라 미검증
  P0-3 POTCAR: 종별 **전체 TITEL(날짜 포함)·ZVAL** 기대값 (PBE_54) · 조립본 sha + 종별 sha 반송 필수 · OUTCAR 의 TITEL 과 대조
       · **잡 사이 종별 sha 와 조립본 sha 일치** (18 잡 종 순서 동일) · 파일럿 뒤 봉인 등록부(`--seal_pp`: 종별·조립본 sha · VASP 버전 줄)와 대조
  P0-4 G5: UMA 입력 **출처 대조** (uma-s-1p1 · 체크포인트 sha 전체 · omat · default · fairchem 2.19.0/2.21.0(교차대조 등가)) · 구조 sha·원자 수·pbc · 중복 이름 거부 · **유한값만** · JSON allow_nan=False
  P1-1 `--check/--collect/--seal_pp` 입구에서 **외부 고정 MANIFEST sha** 와 목록 전 파일 대조 (기대 INCAR/r1·jobs.json 을 승인본에 결박)
  P1-2 결측 = 미검증 (NIONS·NELECT·D3 기대값·Edisp) · **종료코드 규약** (아래) · 진단 JSON 은 실패해도 쓴다 (승인본 오류면 오류 JSON)
  P1-3 r1 은 첫 시도가 **실행됐고 실행 실패·미종료·미수렴** 일 때만 · 첫 시도 없는 r1 · 무결성·PP·설정 위반은 승격 안 함
  P1-4 D3 검사 둘로 분리: ① Edisp 1 % = **큰 오설정 탐지용** (감쇠·3체·계수) · ② **오차 예산** (결과 전 제안 · 1저자 비준 대상):
       표본 쌍 차이 |ΔD3_VASP − ΔD3_ref| ≤ 0.005 J/m² (넘으면 그 표본 총 W 에 인용 금지 라벨 · W_PBE·G5 Δ 는 D3 가 상쇄돼 영향 없음)
       G3 차이의 차이 ≤ 0.001 J/m² (넘으면 G3 = INCOMPLETE (D3 예산))
       배분 = 기존 문턱의 고정 비율 — G3 문턱 0.01 의 10 % · G5 표본 문턱 0.10 의 5 %. V2 실측 QE↔s-dftd3 (쌍 0.0025 · 차이의 차이 0.0001) 은
       달성 가능성 참고일 뿐 근거가 아니다. 기준값(ref) = VASP 내장 D3 기본 절단(공식 문서 VDW_RADIUS 50.2 Å · VDW_CNRADIUS 21.17 Å)에 맞춘 s-dftd3 2체.
       INCAR 에 두 절단을 **명시**해 버전별 기본값 변화를 막는다.
  P1-5 G3 예측 산술 정정 (0.0095396 + 0.0004 = 0.0099396 < 0.01 — 경계선이지 FAIL 예측 아님) → 개정 3 v2 에 기록
  Q4 버전: VASP 버전 = OUTCAR 첫 줄 · 전 잡 같은 빌드 (VERSION_INCONSISTENT) · 등록부와 다르면 VERSION_MISMATCH.
       VDW_S6 사용자 조정은 문서상 6.6.0 부터 — s6 = 1.0 이 PBE 기본값과 같아 값은 같지만, "명시 태그가 다 적용됐다" 는 버전 확인 뒤에만 말한다.
  Q2·Q3 정보 열 (게이트 아님): 표본별 −TS 항 차 (J/m²) · NGZF · OUTCAR 'min pos' 줄 (쌍극자 cut 위치 파일럿 수동 확인용)
  3c 채택안: G5 에 `raw_error_criteria_met` · `usage_eligible` 별도 필드 · 총 W G3 FAIL 이면 "INCOMPLETE (G3 FAIL · 오차표만)"
  3b′ (원안 폐기 · 제한된 잔차 진단으로만): G3 세 구조의 UMA 에너지가 오면 δΔ = δW_PBE − δW_UMA 를 **기록** (문턱 없음 · 비준 전 판정 아님)
  기타: 파일 쓰기 LF 고정 (Windows 에서 selftest 해시가 갈리던 문제) · README 평면파 최대의 ENCUT 표기 · 16 GB 는 파동함수 몫이지 peak RSS 아님
        · 최대 실행 36 회 · 파일럿 2 잡(① bound·far) 재사용 규칙 · README 에 잡별 NELECT·셀

종료코드 (CLI)
  --check   : 0 전 잡 OK · 3 OK 아닌 잡 있음 · 2 승인본(MANIFEST)·사용법 오류
  --collect : 2 승인본·사용법 오류 · 3 OK 아닌 잡 있음(무결성) · 0 G5 PASS · 10 G5 FAIL · 11 G5 INCOMPLETE/BLOCKED · 12 UMA 없음(G5 미평가 · 잡은 전부 OK)
  --build · --seal_pp : 0 성공 · 2 실패

⛔ 이 도구가 못 하는 것
  · POTCAR 파일을 만들거나 내용을 검사하지 못한다 (VASP 라이선스 — 업체 보유분) · 반송된 TITEL/ZVAL 줄 · 종별·조립본 sha 만 본다.
  · **PBE_54 인지 내용 해시로 보증하지 못한다** (공개 기준 해시가 없다) — TITEL 날짜 · 업체 진술 · 파일럿 봉인 뒤 일관성만 본다.
  · 업체가 모든 산출물을 일관되게 위조하면 못 잡는다 — 목표는 실수(재사용·교체·오설정)를 잡는 것이다.
  · VASP 값을 QE 값(V2·V4)과 한 표에서 빼거나 섞지 않는다 — 다른 비교군이다.
  · OUTCAR 문구는 버전마다 조금 다르다 — 설정 되울림·Edisp 줄을 못 읽으면 **미검증**으로 막는다 (파일럿이 파서를 확인한다).
    IVDW·DIPOL 되울림은 INCAR 에코 줄에서 읽힐 수 있다 (해석값과 같다는 보증은 파일럿 OUTCAR 수동 확인).
  · 전자밀도·평균전위로 쌍극자 불연속 위치를 확인하지 않는다 — 핵 여유 4 Å 와 DIPOL 식만 본다 ('min pos'·NGZF 는 기록만).
  · UMA 에너지를 계산하지 않는다 (`relax_uma_d3.py --energies` JSON 을 받는다) · 결과를 보고 표본·문턱·분모를 바꾸지 않는다.
  · 업체 기계의 시간·peak 메모리를 보장하지 않는다 — README 추정은 평면파·밴드 수에서 낸 대략값이다.

사용
  python3 tools/wad/build_v5_vasp_package.py --build --pkg db/inputs/wad_aprime_s3v2_2026_09_26 --out <패키지>
  python3 tools/wad/build_v5_vasp_package.py --check   --out <패키지> --manifest_sha256 <고정값> --ret <반송> [--pp_registry R --pp_registry_sha256 H] [--json J]
  python3 tools/wad/build_v5_vasp_package.py --seal_pp --out <패키지> --manifest_sha256 <고정값> --ret <파일럿 반송> --json pp_registry.json
  python3 tools/wad/build_v5_vasp_package.py --collect --out <패키지> --manifest_sha256 <고정값> --ret <반송> [--uma uma.json] [--pp_registry …] [--json J]
  python3 tools/wad/build_v5_vasp_package.py --selftest
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

SPECIES_ORDER = ("Li", "P", "S", "Cl", "Ag")
POTCAR_MAP = {"Li": "Li_sv", "P": "P", "S": "S", "Cl": "Cl", "Ag": "Ag"}
ZVAL = {"Li": 3.0, "P": 5.0, "S": 6.0, "Cl": 7.0, "Ag": 11.0}
PP_EXPECTED_TITEL = {"Li": "PAW_PBE Li_sv 10Sep2004", "P": "PAW_PBE P 06Sep2000", "S": "PAW_PBE S 06Sep2000",
                     "Cl": "PAW_PBE Cl 06Sep2000", "Ag": "PAW_PBE Ag 02Apr2005"}     # PBE_54 (Materials Project 목록) — 파일럿이 확인 · 다르면 등록 전 멈춘다
PP_SET = "PBE_54"
ENCUT_BASE, ENCUT_G4E = 520.0, 650.0
SIGMA_BASE = 0.136                                                  # eV = QE degauss 0.01 Ry
KP_G4K = (4, 3, 1)
D3_PARAMS = {"s6": 1.0, "s8": 0.7875, "a1": 0.4289, "a2": 4.4407}
VDW_RADIUS_A, VDW_CNRADIUS_A = 50.2, 21.17                          # VASP 내장 D3 기본 절단 (공식 문서) — INCAR 에 명시해 고정
BOHR = 0.529177210903
PERF_INT = ("NCORE", "NPAR", "KPAR", "NSIM")
PERF_BOOL = ("LPLANE", "LSCALU", "LSCALAPACK")
PERF_TAGS = PERF_INT + PERF_BOOL
RESCUE = {"AMIX": "0.1", "BMIX": "0.01", "NELM": "300"}
R1_ELIGIBLE = ("EXECUTION_FAILED", "NOT_TERMINATED", "SCF_NOT_CONVERGED")
DIP_MIN_CLEAR_A = 4.0
D3_REL_TOL = 0.01                                                   # Edisp vs ref — 큰 오설정 탐지용 (오차 예산 아님)
D3_PAIR_BUDGET, D3_G3_BUDGET = 0.005, 0.001                         # J/m² — G5 표본 문턱의 5 % · G3 문턱의 10 % (결과 전 제안 · 1저자 비준 대상)
SIGMA_ECHO_TOL, DIPOL_ECHO_TOL = 0.005, 0.005                       # OUTCAR 되울림은 소수 2 자리로 찍힌다
G3_DW, G4_DW, G5_PER, G5_MEAN = 0.01, 0.02, 0.10, 0.05
G5_SAMPLES = {"①": ("V5_s_outer_A_bound", "V5_s_outer_A_far"), "②": ("V5_s_outer_B_bound", "V5_s_outer_B_far"),
              "③": ("V5_li_outer_A_bound", "V5_li_outer_A_far"), "④": ("V5_li_outer_B_bound", "V5_li_outer_B_far"),
              "⑤": ("V5_s_outer_A_p05_bound", "V5_s_outer_A_far")}
G5_GROUPS = {"s_outer": ("①", "②", "⑤"), "li_outer": ("③", "④")}
G3_JOBS = ("V5_s_outer_A_G3_c2_bound", "V5_s_outer_A_G3_c2_far_i", "V5_s_outer_A_G3_c2_far_ii")
UMA_REQ = {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default",
           "checkpoint_sha256": "07068e9c76702ca173d13155095f2117c1b327ec228557e64cd2709c777b824a",
           "fairchem_allowed": ("2.19.0", "2.21.0")}                # 2.21.0 = wad_aprime_s4_uma_env_xcheck_2026_09_26 (|Δ| ≤ 0.005 meV 등가)
PILOT_JOBS = ("V5_s_outer_A_bound", "V5_s_outer_A_far")
EV_J, A2_M2 = 1.602176634e-19, 1e-20
HB2M = 3.80998212                                                   # ħ²/2mₑ [eV·Å²]
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class PkgError(Exception):
    pass


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _sha_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


def _write(path, text):
    """LF 고정 쓰기 — Windows 기본 CRLF 로 쓰면 기록해 둔 해시와 갈린다 (CE 리뷰어 실측)."""
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def fin(x):
    """유한한 실수만 통과 (bool · None · NaN · ±Inf · 문자열 → None)."""
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    return float(x) if math.isfinite(x) else None


# ───────────────────────── 입력 만들기 ─────────────────────────
def poscar_text(atoms, comment):
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


def parse_poscar_cart(text):
    ln = text.splitlines()
    cell = [[float(x) for x in ln[k].split()] for k in (2, 3, 4)]
    sp = ln[5].split(); nn = [int(x) for x in ln[6].split()]
    pos = [[float(x) for x in l.split()[:3]] for l in ln[8:8 + sum(nn)]]
    return sp, nn, cell, pos


def dipol_z(emaxpos, eopreg):
    """QE 톱니 불연속 구간 중심 → VASP DIPOL_z. VASP 보정의 불연속은 DIPOL ± ½ 에 놓인다 (CE Q3 확인) → 중심 − ½ (mod 1)."""
    return (emaxpos + 0.5 * eopreg - 0.5) % 1.0


def check_dip_clear(atoms, emaxpos, eopreg, min_clear=DIP_MIN_CLEAR_A):
    c = float(atoms.cell.array[2, 2]); lo, hi = emaxpos * c, (emaxpos + eopreg) * c
    worst = min(min(abs(z + s * c - lo), abs(z + s * c - hi)) if not (lo <= z + s * c <= hi) else 0.0
                for z in atoms.get_positions()[:, 2] for s in (-1, 0, 1))
    if worst < min_clear - 1e-3:      # emaxpos·eopreg 는 dip_region 이 소수 5 자리로 반올림 → c ≤ 40 Å 에서 재계산 오차 ≤ 2e-4 Å
        raise PkgError(f"쌍극자 구간 [{lo:.3f}, {hi:.3f}] Å 에서 가장 가까운 핵까지 {worst:.3f} Å < {min_clear} Å")
    return round(worst, 3)


def incar_text(job, encut, sigma, dz, rescue=False):
    L = [f"SYSTEM = A-prime V5 {job} (single point){' - pre-registered retry r1' if rescue else ''}",
         "GGA = PE", "PREC = Accurate", f"ENCUT = {encut:.1f}", "EDIFF = 1E-6",
         f"NELM = {RESCUE['NELM'] if rescue else 200}", "NELMIN = 6", "ALGO = Normal",
         "ISPIN = 1", "ISMEAR = 1", f"SIGMA = {sigma:.4f}", "LASPH = .TRUE.", "LREAL = .FALSE.", "ISYM = 0",
         "IBRION = -1", "NSW = 0",
         "IVDW = 12", f"VDW_S6 = {D3_PARAMS['s6']}", f"VDW_S8 = {D3_PARAMS['s8']}", f"VDW_A1 = {D3_PARAMS['a1']}", f"VDW_A2 = {D3_PARAMS['a2']}",
         f"VDW_RADIUS = {VDW_RADIUS_A}", f"VDW_CNRADIUS = {VDW_CNRADIUS_A}",
         "LDIPOL = .TRUE.", "IDIPOL = 3", f"DIPOL = 0.5 0.5 {dz:.6f}",
         "LWAVE = .FALSE.", "LCHARG = .FALSE."]
    if rescue:
        L += [f"AMIX = {RESCUE['AMIX']}", f"BMIX = {RESCUE['BMIX']}"]
    return "\n".join(L) + "\n"


def kpoints_text(k):
    return f"Gamma-centred mesh (A-prime V5)\n0\nGamma\n{k[0]} {k[1]} {k[2]}\n0 0 0\n"


def parse_incar_strict(text):
    """VASP 의미대로 읽는다: `#`·`!` 뒤 주석 · **`;` 는 문장 구분** · `\\` 줄 이음은 거부 · 같은 태그 두 번이면 오류.
    반환 (dict, 오류 목록). 오류가 하나라도 있으면 검사기는 INPUT_MODIFIED 로 본다."""
    d, errs = {}, []
    for raw in text.splitlines():
        ln = re.split(r"[#!]", raw, maxsplit=1)[0]
        if "\\" in ln:
            errs.append(f"줄 이음(\\) 금지: {raw.strip()}"); continue
        for st in ln.split(";"):
            st = st.strip()
            if not st:
                continue
            if "=" not in st:
                errs.append(f"대입 아님: {st}"); continue
            k, v = st.split("=", 1); k = k.strip().upper(); v = " ".join(v.split())
            if not re.fullmatch(r"[A-Z][A-Z0-9_]*", k):
                errs.append(f"태그 이름 이상: {k}"); continue
            if k in d:
                errs.append(f"태그 중복: {k}"); continue
            d[k] = v
    return d, errs


def perf_value_ok(tag, val):
    if tag in PERF_INT:
        return re.fullmatch(r"[1-9][0-9]*", val) is not None
    if tag in PERF_BOOL:
        return re.fullmatch(r"\.?(TRUE|FALSE|T|F)\.?", val.upper()) is not None
    return False


def estimate(atoms, encut, kp):
    """대략 규모 — NELECT · 기본 NBANDS · 평면파 수 · **파동함수 몫** 메모리 (peak RSS 아님 · FFT·투영자·작업 배열·MPI 복제 제외)."""
    sym = atoms.get_chemical_symbols(); n = len(sym)
    nel = sum(ZVAL[s] for s in sym); nb = int(math.ceil(nel / 2 + n / 2))
    V = abs(float(atoms.get_volume())); kmax = math.sqrt(encut / HB2M)
    npw = V * kmax ** 3 / (6 * math.pi ** 2)
    nk_full = kp[0] * kp[1] * kp[2]; nk_irr = (nk_full + 1) // 2 + (1 if nk_full % 2 == 0 else 0)
    return {"NIONS": n, "NELECT": nel, "NBANDS_default": nb, "NPW_per_k": int(npw), "ENCUT_eV": encut, "nk_full": nk_full, "nk_irr_est": nk_irr,
            "wfc_only_GB_all_k": round(nb * npw * 16 * nk_irr / 1e9, 1), "⚠": "파동함수 몫 대략치 — peak RSS 아님 · 환원 k 는 IBZKPT 로 확인"}


def d3_ref_eV(atoms):
    """s-dftd3 2체 D3(BJ) · VASP 기본 절단(VDW_RADIUS 50.2 Å · VDW_CNRADIUS 21.17 Å)에 맞춤 [eV]. dftd3 가 없으면 PkgError (기대값 없는 패키지는 만들지 않는다)."""
    try:
        import numpy as np
        from dftd3.interface import RationalDampingParam, DispersionModel
    except Exception as e:
        raise PkgError(f"simple-dftd3 가 없다 — D3 기대값 없이 패키지를 만들지 않는다 ({e})")
    m = DispersionModel(atoms.get_atomic_numbers(), atoms.get_positions() / BOHR, atoms.cell.array / BOHR, np.array([True, True, True]))
    m.set_realspace_cutoff(VDW_RADIUS_A / BOHR, 40.0, VDW_CNRADIUS_A / BOHR)
    return float(m.get_dispersion(RationalDampingParam(**D3_PARAMS, s9=0.0), grad=False)["energy"]) * 27.211386245988


RUN_ALL = r'''#!/usr/bin/env bash
# =============================================================================
# run_all.sh (v2) — A′ V5 VASP 단일점 18 잡 · 잡마다 사전등록 재시도 INCAR.r1 최대 1 회 (최대 36 실행)
#   필수: VASP_CMD (예: "mpirun -np 128 vasp_std") · POTCAR_DIR (PAW_PBE 폴더: <POTCAR_DIR>/Li_sv/POTCAR · P · S · Cl · Ag)
#   선택: PERF_TAGS_FILE — 한 줄에 대입 하나만 · 허용 NCORE/NPAR/KPAR/NSIM (양의 정수) · LPLANE/LSCALU/LSCALAPACK (.TRUE./.FALSE.)
#         세미콜론·역슬래시·중복 태그·줄 끝 주석 금지 (VASP 는 ';' 뒤를 다른 설정으로 읽는다)
#         JOBS="잡1 잡2" (일부만 — 파일럿: JOBS="V5_s_outer_A_bound V5_s_outer_A_far")
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · ⛔ POTCAR 는 반송하지 않습니다 (TITEL/ZVAL 줄 · sha256 만)
#   ⛔ 시도 폴더(run/<잡>, run/<잡>_r1)가 이미 있으면 그 잡은 돌지 않습니다 — 지난 출력 재사용 방지. 다시 돌리려면 run/ 을 옮기세요.
#   종료코드: 0 전 잡 성공 · 1 일부 실패 (그래도 반송 묶음은 만든다 — 실패도 기록) · 2 패키지·성능 파일 오류 (아무것도 안 돈다)
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 128 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
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
JOBS=${JOBS:-$(cat JOBS.txt)}
for job in $JOBS; do [ -d "jobs/$job" ] || { echo "⛔ 모르는 잡 $job"; exit 2; }; done
mkdir -p run
{ echo "date_utc $(date -u +%FT%TZ)"; echo "host $(hostname 2>/dev/null)"; echo "VASP_CMD $VASP_CMD"; echo "POTCAR_DIR $POTCAR_DIR";
  echo "PERF_TAGS $(printf '%s' "$PERF_LINES" | tr '\n' ';')"; echo "MANIFEST_sha256 $(sha256sum MANIFEST.sha256 | cut -d' ' -f1)"; } >> run/env.txt
[ -f run/status.tsv ] || printf "job\tattempt\trc\tterminated\tconverged\tn_runs\tn_elec_steps\tTOTEN_eV\twall_s\n" > run/status.tsv
h(){ sha256sum "$1" 2>/dev/null | cut -d' ' -f1; }
run_one(){  # $1 잡 · $2 시도(0|r1) · $3 INCAR 파일 → 0 성공 · 1 실행했으나 실패 (재시도 대상) · 3 준비 실패 (재시도 아님)
  local job=$1 att=$2 inc=$3 d; d=run/$job; [ "$att" = r1 ] && d=run/${job}_r1
  [ -e "$d" ] && { echo "⛔ $d 가 이미 있다 — 덮어쓰지 않는다"; return 3; }
  mkdir -p "$d" || return 3
  { cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/" && cp "jobs/$job/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; return 3; }
    cat "$POTCAR_DIR/$p/POTCAR" >> "$d/POTCAR"; printf "%s %s\n" "$p" "$(h "$POTCAR_DIR/$p/POTCAR")" >> "$d/POTCAR.species.sha256"
  done < "jobs/$job/POTCAR.spec"
  grep -E "TITEL|ZVAL|VRHFIN|LEXCH" "$d/POTCAR" > "$d/POTCAR.titel"; h "$d/POTCAR" > "$d/POTCAR.sha256"
  local rid t0 t1 rc term conv nrun nel E
  rid="$(date -u +%Y%m%dT%H%M%S)-$$-$RANDOM"; t0=$(date +%s)
  (cd "$d" && $VASP_CMD > stdout.log 2>&1); rc=$?; t1=$(date +%s)
  term=0; grep -q "General timing and accounting" "$d/OUTCAR" 2>/dev/null && term=1
  conv=0; grep -q "aborting loop because EDIFF is reached" "$d/OUTCAR" 2>/dev/null && conv=1
  grep -q "EDIFF was not reached" "$d/OUTCAR" 2>/dev/null && conv=0
  nrun=$(grep -cE '^[[:space:]]*vasp\.[0-9]' "$d/OUTCAR" 2>/dev/null); nrun=${nrun:-0}
  nel=$(grep -cE "^(DAV|RMM|CG|SDA):" "$d/OSZICAR" 2>/dev/null); nel=${nel:-0}
  E=$(grep "free  energy   TOTEN" "$d/OUTCAR" 2>/dev/null | tail -1 | awk '{print $5}')
  printf '{"job": "%s", "attempt": "%s", "run_id": "%s", "rc": %d, "t_start": %d, "t_end": %d, "sha256": {"INCAR": "%s", "POSCAR": "%s", "KPOINTS": "%s", "POTCAR": "%s", "OUTCAR": "%s", "OSZICAR": "%s"}}\n' \
    "$job" "$att" "$rid" "$rc" "$t0" "$t1" "$(h "$d/INCAR")" "$(h "$d/POSCAR")" "$(h "$d/KPOINTS")" "$(cat "$d/POTCAR.sha256")" "$(h "$d/OUTCAR")" "$(h "$d/OSZICAR")" > "$d/attempt.json"
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$job" "$att" "$rc" "$term" "$conv" "$nrun" "$nel" "${E:-NA}" "$((t1-t0))" >> run/status.tsv
  rm -f "$d/POTCAR" "$d/WAVECAR" "$d/CHGCAR" "$d/CHG" "$d/vasprun.xml"
  [ "$rc" = 0 ] && [ "$term" = 1 ] && [ "$conv" = 1 ] && [ "$nrun" = 1 ] && return 0
  return 1
}
fail=0
for job in $JOBS; do
  run_one "$job" 0 INCAR; s=$?
  if [ "$s" = 0 ]; then echo "✓ $job"
  elif [ "$s" = 1 ]; then
    echo "… $job 실행 실패·미종료·미수렴 → 사전등록 재시도 1 회 (INCAR.r1: AMIX 0.1 · BMIX 0.01 · NELM 300)"
    if run_one "$job" r1 INCAR.r1; then echo "✓ $job (r1)"; else echo "⛔ $job r1 도 실패 — 값 없음 (다른 설정으로 더 돌리지 않는다)"; fail=1; fi
  else echo "⛔ $job 준비 실패 (기존 폴더 · 입력 · POTCAR) — 재시도 대상 아님"; fail=1; fi
done
tar czf V5_vasp_return.tgz run MANIFEST.sha256 && sha256sum V5_vasp_return.tgz > V5_vasp_return.tgz.sha256
if [ "$fail" = 0 ]; then echo "✅ 끝 — V5_vasp_return.tgz 와 .sha256 을 보내 주세요"; else echo "⚠ 일부 잡 실패 — 그대로 반송해 주세요 (실패도 기록입니다)"; fi
exit "$fail"
'''


def _readme(jobs, est, pkg_sha):
    rows = "\n".join(f"| `{j['dir']}` | {j['role']} | {j['nions']} | {j['nelect_expected']:.0f} | {'×'.join(f'{x:.3f}' for x in j['cell_A'])} | "
                     f"{j['encut']:.0f} | {'×'.join(map(str, j['kpts']))} | {j['sigma']:.3f} |" for j in jobs)
    pp = " · ".join(f"{POTCAR_MAP[s]} (`{PP_EXPECTED_TITEL[s]}`)" for s in SPECIES_ORDER)
    return f"""# A′ V5 — VASP 단일점 외주 패키지 v2 (LPSCl | Ag(111) 작은 주기 계면)

> 상태: **준비본 (실행 미정)** · Codex CE NO-GO 반영판 · 재리뷰 전 · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` **proposed**
> 원본: 봉인 S3v2 패키지 (구조 파일 sha 결박) · 이 패키지 MANIFEST.sha256 의 sha256 = `{pkg_sha}` (보낼 때 메일 본문에 적는다 — 반송 검사가 이 값으로 승인본을 확인한다)

## 무엇을 하나
PBE+D3(BJ) **단일점(SCF) 18 개** — 이완 없음. 좌표는 이미 정해져 있습니다 (POSCAR 그대로).

| 잡 | 역할 | NIONS | NELECT | 셀 a×b×c (Å) | ENCUT (eV) | k (Γ) | SIGMA (eV) |
|---|---|---|---|---|---|---|---|
{rows}

## 돌리는 법
1. **파일럿 2 잡 먼저** (표본 ① 두 끝점 · 반송해 주세요): `JOBS="V5_s_outer_A_bound V5_s_outer_A_far" VASP_CMD="mpirun -np <N> vasp_std" POTCAR_DIR=<PAW_PBE> bash run_all.sh`
   — 파일럿 전에 VASP 버전·PP 세트·설정·파서·실패 규칙은 고정돼 있습니다. 파일럿의 W 값을 보고 설정을 바꾸지 않습니다.
2. 확인 연락을 받으면 **나머지 16 잡**: `JOBS="<16 잡>" ... bash run_all.sh` (파일럿 두 잡은 이 패키지 sha 그대로라면 **재사용** — 다시 돌리지 않습니다).
   파일럿 뒤에 VASP 입력이 바뀌어야 하면 새 패키지 버전이 나가고, 파일럿은 구판 진단으로만 남습니다.
3. 성능 태그는 `PERF_TAGS_FILE=perf.txt` 로만 — **한 줄에 대입 하나**, 허용: NCORE NPAR KPAR NSIM (양의 정수) · LPLANE LSCALU LSCALAPACK (.TRUE./.FALSE.).
   세미콜론(;) · 역슬래시(\\) · 같은 태그 두 번 · 줄 끝 주석은 거부됩니다. **INCAR·POSCAR·KPOINTS 는 고치지 마세요.**
4. 시도 폴더 `run/<잡>` 이 이미 있으면 러너가 그 잡을 **돌리지 않습니다** (지난 출력 재사용 방지). 다시 돌리려면 `run/` 을 통째로 옮기세요.
5. 한 잡이 실행 실패·미종료·미수렴이면 러너가 미리 정한 재시도(INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300)를 **한 번만** 합니다.
   그래도 안 되면 그 잡은 비워 둡니다 — 다른 설정으로 더 돌리지 마세요. 실행 상한 = 18 × 2 = **36 회** (파일럿 재사용 시).

## VASP 버전 · POTCAR — 이 조합으로 고정
- **VASP**: 파일럿과 본 배치가 **같은 빌드**여야 합니다 (OUTCAR 첫 줄로 확인 · 다르면 그 배치는 쓰지 않습니다). 버전·빌드를 `run/env.txt` 에 적어 주세요.
  INCAR 의 VDW_S6 는 문서상 VASP 6.6.0 부터 사용자 조정이 되지만, 값 1.0 은 PBE 기본값과 같습니다 (구버전이어도 같은 값).
- **POTCAR** {PP_SET}: {pp}.
  파일럿에서 TITEL(날짜 포함)·종별·조립본 sha256 을 확인해 **등록부로 봉인**하고, 이후 모든 잡이 그 등록부와 같아야 합니다. 다른 PP 트리로 바꾸지 마세요.
  POTCAR 파일은 **보내지 마세요** — 러너가 TITEL/ZVAL/LEXCH 줄 · 종별 sha256 · 조립본 sha256 만 남깁니다.

## 돌려받을 것
`V5_vasp_return.tgz` + `.sha256` (러너가 만듭니다): 시도마다 OUTCAR · OSZICAR · INCAR(실행본) · KPOINTS · POSCAR · POTCAR.titel · POTCAR.sha256 · POTCAR.species.sha256 · attempt.json · stdout.log
· `run/status.tsv` · `run/env.txt`. VASP 버전·빌드·컴파일러·노드/코어 수·**잡별 peak RSS·벽시계** 를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.
실패한 잡도 폴더째 보내 주세요 (실패도 기록입니다).

## 규모 (대략 · 우리 추정 — 견적은 파일럿 벽시계·peak RSS 로)
NIONS 176–200 · NELECT {est['nel_min']:.0f}–{est['nel_max']:.0f} · 기본 NBANDS ~{est['nb_max']} · 평면파 최대 ~{est['npw_520']:,}/k (ENCUT 520) · ~{est['npw_650']:,}/k (ENCUT 650 · G4 변형 2 잡)
· 파동함수 몫만 ~{est['wfc_max']} GB (k 합 · **peak RSS 아님** — FFT·투영자·작업 배열·MPI 복제는 따로) · 환원 k 추정 Γ3×2×1 ≈ 4 · Γ4×3×1 ≈ 7 (IBZKPT 로 확인).
비스핀 · 금속(Ag) 슬랩 · 진공 포함 · LREAL=F · 실행 최대 36 회. KPAR 는 실제 k 수·메모리·노드 배치에 맞춰 업체가 고릅니다.

## English summary
18 single-point PBE+D3(BJ) SCF runs (no relaxation) on fixed geometries. PAW_PBE {PP_SET} Li_sv/P/S/Cl/Ag (TITELs above; sealed after the pilot);
the pilot and the main batch must use the same VASP build. ENCUT 520 eV (650 eV for two G4 jobs); ISMEAR 1, SIGMA 0.136 eV; IVDW 12 with explicit
PBE-BJ parameters and explicit VDW_RADIUS/VDW_CNRADIUS; dipole correction along z (LDIPOL, IDIPOL 3, DIPOL given). Run the two pilot jobs first and
return them. Do not edit INCAR/POSCAR/KPOINTS (performance tags only via PERF_TAGS_FILE, one assignment per line, no ';'); existing attempt folders
are never overwritten; one pre-registered retry per job (max 36 runs); do not send POTCAR files. Please report VASP version/build and per-job peak RSS and wall time.
"""


def build(pkg, out):
    from ase.io import read
    qe = json.load(open(os.path.join(pkg, "qe", "jobs.json"), encoding="utf-8"))
    man_path = os.path.join(pkg, "s3_manifest.json"); man = json.load(open(man_path, encoding="utf-8"))
    if qe.get("s3_manifest_sha256") != _sha(man_path):
        raise PkgError("S3 manifest sha 가 qe/jobs.json 에 적힌 값과 다르다 — 봉인 패키지가 아니다")
    ssha = man["structures_sha256"]
    v5 = [j for j in qe["jobs"] if j.get("model") == "V5" and j.get("kind") != "probe"]
    if len(v5) != 18:
        raise PkgError(f"V5 잡이 18 개가 아니다 ({len(v5)}) — 카드 표본(5 표본 · G3 3 · G4 6)과 다르다")
    os.makedirs(os.path.join(out, "jobs"), exist_ok=True)
    jobs, cache, d3c = [], {}, {}
    for j in v5:
        st = j["structure"]; sp = os.path.join(pkg, "structures", f"{st}.extxyz")
        if st not in ssha or _sha(sp) != ssha[st]:
            raise PkgError(f"{j['dir']}: 구조 {st} 의 sha 가 봉인 manifest 와 다르다")
        at = cache.setdefault(st, read(sp))
        tags = j.get("tags") or {}; g4 = tags.get("G4", "") or ""
        g4t = g4.replace("G4_", "").rsplit("_", 1)[0] if g4 else ""
        encut = ENCUT_G4E if g4t == "e70" else ENCUT_BASE
        sigma = SIGMA_BASE / 2 if (g4t == "s05" or tags.get("degauss_halved")) else SIGMA_BASE
        kp = tuple(j["kpts"])
        if g4t == "k1" and kp != KP_G4K:
            raise PkgError(f"{j['dir']}: G4 k1 인데 k 가 {kp}")
        emx, eop = j["dip"]["emaxpos"], j["dip"]["eopreg"]
        clear = check_dip_clear(at, emx, eop); dz = dipol_z(emx, eop)
        d = os.path.join(out, "jobs", j["dir"]); os.makedirs(d, exist_ok=True)
        pos, order, present = poscar_text(at, f"A-prime V5 {j['dir']} | src {st} sha {ssha[st][:16]}")
        files = {"POSCAR": pos, "INCAR": incar_text(j["dir"], encut, sigma, dz), "INCAR.r1": incar_text(j["dir"], encut, sigma, dz, rescue=True),
                 "KPOINTS": kpoints_text(kp), "POTCAR.spec": "\n".join(POTCAR_MAP[s] for s in present) + "\n"}
        for n, t in files.items():
            _write(os.path.join(d, n), t)
        role = {"scf": "표본 끝점", "g3": "G3 끝점 검사 (c+2)",
                "g4": f"G4 수치 검사 ({ {'e70': 'ENCUT 650', 'k1': 'k 4×3×1', 's05': 'SIGMA ½'}.get(g4t, g4t) })"}[j["kind"]]
        sym = at.get_chemical_symbols()
        if st not in d3c:
            d3c[st] = d3_ref_eV(at)
        c = at.cell.array
        jobs.append({"dir": j["dir"], "kind": j["kind"], "role": role, "structure": st, "structure_sha256": ssha[st], "nions": len(sym),
                     "composition": {s: sym.count(s) for s in present}, "nelect_expected": sum(ZVAL[s] for s in sym),
                     "potcar_spec": [POTCAR_MAP[s] for s in present], "pp_expected_titel": [PP_EXPECTED_TITEL[s] for s in present],
                     "zval_expected": [ZVAL[s] for s in present], "encut": encut, "sigma": sigma, "kpts": list(kp),
                     "cell_A": [round(float(x), 4) for x in at.cell.lengths()],
                     "dipol_z": round(dz, 6), "qe_dip": {"emaxpos": emx, "eopreg": eop}, "dip_min_clearance_A": clear,
                     "poscar_order_to_original_index": order, "area_A2": round(float(abs(c[0][0] * c[1][1] - c[0][1] * c[1][0])), 6),
                     "files_sha256": {n: _sha_text(t) for n, t in files.items()}, "d3_2body_eV_ref": d3c[st],
                     "estimate": estimate(at, encut, kp), "qe_job_pw_in_sha256": j.get("pw_in_sha256")})
    E = [x["estimate"] for x in jobs]
    est = {"nel_min": min(e["NELECT"] for e in E), "nel_max": max(e["NELECT"] for e in E), "nb_max": max(e["NBANDS_default"] for e in E),
           "npw_520": max(e["NPW_per_k"] for e in E if e["ENCUT_eV"] == ENCUT_BASE), "npw_650": max((e["NPW_per_k"] for e in E if e["ENCUT_eV"] == ENCUT_G4E), default=0),
           "wfc_max": max(e["wfc_only_GB_all_k"] for e in E), "max_runs": 2 * len(jobs)}
    _write(os.path.join(out, "run_all.sh"), RUN_ALL); os.chmod(os.path.join(out, "run_all.sh"), 0o755)
    _write(os.path.join(out, "JOBS.txt"), "\n".join(x["dir"] for x in jobs) + "\n")
    meta = {"schema": "aprime_v5_vasp_package/v2", "date": "2026-09-27", "status": "준비본 v2 (Codex CE NO-GO 반영 · 재리뷰 전 · 결정 proposed · 실행 미정)",
            "source_package": pkg, "source_s3_manifest_sha256": qe["s3_manifest_sha256"], "source_seal": "db/properties/wad_aprime_s3v2_seal_2026_09_26.json",
            "card": "db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json", "amendment": "db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json",
            "tool_sha256": _sha(os.path.abspath(__file__)),
            "settings": {"potcar": POTCAR_MAP, "pp_set": PP_SET, "pp_expected_titel": PP_EXPECTED_TITEL, "zval": ZVAL, "encut": ENCUT_BASE, "encut_g4e": ENCUT_G4E,
                         "sigma": SIGMA_BASE, "d3": D3_PARAMS, "d3_cutoffs_A": {"VDW_RADIUS": VDW_RADIUS_A, "VDW_CNRADIUS": VDW_CNRADIUS_A},
                         "d3_ref": "simple-dftd3 2체 · VASP 절단에 맞춤", "perf_tags_int": PERF_INT, "perf_tags_bool": PERF_BOOL, "rescue": RESCUE,
                         "r1_eligible": R1_ELIGIBLE, "d3_gross_rel_tol": D3_REL_TOL, "d3_pair_budget_J_m2": D3_PAIR_BUDGET, "d3_g3_budget_J_m2": D3_G3_BUDGET,
                         "uma_required": UMA_REQ, "pilot_jobs": PILOT_JOBS},
            "G5_samples": {k: list(v) for k, v in G5_SAMPLES.items()}, "G5_groups": {k: list(v) for k, v in G5_GROUPS.items()}, "estimate": est, "jobs": jobs}
    _write(os.path.join(out, "jobs.json"), json.dumps(meta, ensure_ascii=False, indent=1, allow_nan=False))
    lines = []
    for root, _, fs in os.walk(out):
        for f in sorted(fs):
            p = os.path.join(root, f); r = os.path.relpath(p, out).replace(os.sep, "/")
            if r in ("MANIFEST.sha256", "README.md") or r.startswith("run/"):
                continue
            lines.append(f"{_sha(p)}  {r}")
    _write(os.path.join(out, "MANIFEST.sha256"), "\n".join(sorted(lines, key=lambda s: s.split("  ", 1)[1])) + "\n")
    msha = _sha(os.path.join(out, "MANIFEST.sha256"))
    _write(os.path.join(out, "README.md"), _readme(jobs, est, msha))
    return meta, msha


# ───────────────────────── 승인본 대조 (P1-1) ─────────────────────────
def verify_manifest(out, expected_sha256):
    """외부에 고정한 MANIFEST sha 와 그 목록의 모든 파일을 대조한다. 어긋나면 PkgError (검사·집계를 시작하지 않는다)."""
    if not expected_sha256 or not HEX64.match(str(expected_sha256).lower()):
        raise PkgError("--manifest_sha256 (외부에 고정한 64자리 hex) 가 필요하다")
    mp = os.path.join(out, "MANIFEST.sha256")
    if not os.path.isfile(mp) or _sha(mp) != expected_sha256.lower():
        raise PkgError("MANIFEST.sha256 가 고정값과 다르다 — 승인본이 아니다")
    listed = []
    for ln in open(mp, encoding="utf-8").read().splitlines():
        if not ln.strip():
            continue
        h, rel = ln.split("  ", 1)
        p = os.path.join(out, rel)
        if not os.path.isfile(p) or _sha(p) != h:
            raise PkgError(f"승인본 파일이 MANIFEST 와 다르다: {rel}")
        listed.append(rel)
    if "jobs.json" not in listed:
        raise PkgError("MANIFEST 에 jobs.json 이 없다")
    return len(listed)


def return_manifest_info(ret, pinned):
    """반송 묶음에 들어 있는 MANIFEST.sha256 (러너가 실행 때 쓴 것) 이 고정값과 같은가 — 정보 (입력 대조가 이미 결박한다)."""
    p = os.path.join(ret, "MANIFEST.sha256")
    return {"present": os.path.isfile(p), "matches_pinned": (_sha(p) == str(pinned).lower()) if os.path.isfile(p) else None}


# ───────────────────────── 반송 검사 ─────────────────────────
_HEADER = re.compile(r"^\s*(vasp\.\d.*)$", re.M)


def _last(pat, text, flags=re.M):
    m = re.findall(pat, text, flags)
    return m[-1] if m else None


def parse_outcar(text):
    heads = _HEADER.findall(text)
    r = {"n_runs": len(heads), "version": " ".join(heads[0].split()) if heads else None,
         "terminated": "General timing and accounting" in text,
         "converged": ("aborting loop because EDIFF is reached" in text) and ("EDIFF was not reached" not in text)}
    def num(pat):
        v = _last(pat, text)
        return fin(float(v)) if v is not None else None
    r["TOTEN_eV"] = num(r"free\s+energy\s+TOTEN\s*=\s*(-?\d+\.\d+)")
    r["E_sigma0_eV"] = num(r"energy\(sigma->0\)\s*=\s*(-?\d+\.\d+)")
    r["E_noentropy_eV"] = num(r"energy\s+without\s+entropy\s*=\s*(-?\d+\.\d+)")
    r["Edisp_eV"] = num(r"Edisp\s*(?:\(eV\))?\s*[:=]\s*(-?\d+\.\d+)")
    s = {}
    v = _last(r"NIONS\s*=\s*(\d+)", text); s["NIONS"] = int(v) if v else None
    s["NELECT"] = num(r"NELECT\s*=\s*(-?\d+\.?\d*)")
    s["ENCUT"] = num(r"^\s*ENCUT\s*=\s*([\d.]+)\s*eV")
    v = re.findall(r"ISMEAR\s*=\s*(-?\d+)\s*;\s*SIGMA\s*=\s*([\d.]+)", text)
    s["ISMEAR"], s["SIGMA"] = (int(v[-1][0]), float(v[-1][1])) if v else (None, None)
    v = _last(r"^\s*ISPIN\s*=\s*(\d+)", text); s["ISPIN"] = int(v) if v else None
    v = _last(r"^\s*IVDW\s*=\s*(\d+)", text); s["IVDW"] = int(v) if v else None
    v = _last(r"^\s*LDIPOL\s*=\s*(\S+)", text); s["LDIPOL"] = (v.strip(".").upper()[:1] if v else None)
    v = _last(r"^\s*IDIPOL\s*=\s*(\d+)", text); s["IDIPOL"] = int(v) if v else None
    v = re.findall(r"^\s*DIPOL\s*=\s*([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)", text, re.M); s["DIPOL_z"] = float(v[-1][2]) if v else None
    s["EFIELD"] = num(r"^\s*EFIELD\s*=\s*([-+\d.Ee]+)")
    r["settings"] = s
    r["outcar_titel"] = list(dict.fromkeys(" ".join(x.split()) for x in re.findall(r"TITEL\s*=\s*(.+)", text)))
    v = _last(r"NGZF\s*=\s*(\d+)", text); r["NGZF"] = int(v) if v else None
    r["dipole_minpos_lines"] = [" ".join(x.split()) for x in re.findall(r"^.*min pos.*$", text, re.M)[-2:]]
    return r


def parse_titel(text):
    return [" ".join(x.split()) for x in re.findall(r"TITEL\s*=\s*(.+)", text)], [float(x) for x in re.findall(r"ZVAL\s*=\s*(-?\d+\.?\d*)", text)]


def audit_settings(s, job):
    """OUTCAR 되울림(실제 해석된 값) 대조 → (없는 키, 다른 키)."""
    exp = {"NIONS": job["nions"], "NELECT": job["nelect_expected"], "ENCUT": job["encut"], "ISMEAR": 1, "SIGMA": job["sigma"], "ISPIN": 1,
           "IVDW": 12, "LDIPOL": "T", "IDIPOL": 3, "DIPOL_z": job["dipol_z"]}
    missing = [k for k in exp if s.get(k) is None]
    bad = []
    for k, e in exp.items():
        v = s.get(k)
        if v is None:
            continue
        if k == "SIGMA":
            ok = abs(v - e) <= SIGMA_ECHO_TOL + 1e-9
        elif k == "DIPOL_z":
            dz = abs(v - e) % 1.0; ok = min(dz, 1 - dz) <= DIPOL_ECHO_TOL + 1e-9
        elif k in ("ENCUT", "NELECT"):
            ok = abs(v - e) <= 0.05
        else:
            ok = v == e
        if not ok:
            bad.append(f"{k} {v} ≠ {e}")
    if s.get("EFIELD") is not None and abs(s["EFIELD"]) > 1e-12:
        bad.append(f"EFIELD {s['EFIELD']} (외부장 금지)")
    return missing, bad


def _spec_key(job):
    return ",".join(job["potcar_spec"])


def check_job(job, pkgdir, attdir, attempt="0", pp_registry=None):
    """한 시도 폴더 → 상태 dict. OK 가 아니면 값은 판정에 안 쓴다.
    순서: 실행 기록 결박 → 입력 무결성 → rc → OUTCAR 구조 → 종료·수렴 → POTCAR → 버전 → 설정 되울림 → 에너지 → D3."""
    r = {"dir": os.path.basename(attdir), "attempt": attempt}
    if not os.path.isdir(attdir):
        r["status"] = "MISSING"; r["missing"] = ["(폴더)"]; return r
    miss = [f for f in ("INCAR", "KPOINTS", "POSCAR", "attempt.json") if not os.path.isfile(os.path.join(attdir, f))]
    if miss:
        r["status"] = "MISSING"; r["missing"] = miss; return r
    try:
        a = json.load(open(os.path.join(attdir, "attempt.json"), encoding="utf-8"))
    except Exception as e:
        r["status"] = "ATTEMPT_MISMATCH"; r["why"] = f"attempt.json 읽기 실패 {e}"; return r
    if not isinstance(a, dict) or a.get("job") != job["dir"] or str(a.get("attempt")) != str(attempt) or not isinstance(a.get("sha256"), dict):
        r["status"] = "ATTEMPT_MISMATCH"; r["why"] = f"attempt.json 의 잡/시도 {a.get('job') if isinstance(a, dict) else a}"; return r
    for f in ("INCAR", "POSCAR", "KPOINTS", "OUTCAR", "OSZICAR"):
        p = os.path.join(attdir, f)
        if (a["sha256"].get(f) or "") != (_sha(p) if os.path.isfile(p) else ""):
            r["status"] = "ATTEMPT_MISMATCH"; r["why"] = f"{f} 가 실행 기록(attempt.json)과 다르다 — 실행 뒤 바뀌었거나 생겼거나 없어진 파일"; return r
    rc = a.get("rc")
    if isinstance(rc, bool) or not isinstance(rc, int):
        r["status"] = "ATTEMPT_MISMATCH"; r["why"] = f"rc 형식 {rc!r}"; return r
    r["run_id"] = a.get("run_id"); r["rc"] = rc
    for f in ("POSCAR", "KPOINTS"):
        if _sha(os.path.join(attdir, f)) != job["files_sha256"][f]:
            r["status"] = "INPUT_MODIFIED"; r["why"] = f; return r
    ours, e0 = parse_incar_strict(open(os.path.join(pkgdir, "jobs", job["dir"], "INCAR.r1" if attempt == "r1" else "INCAR"), encoding="utf-8").read())
    ran, e1 = parse_incar_strict(open(os.path.join(attdir, "INCAR"), encoding="utf-8", errors="replace").read())
    extra = {k: v for k, v in ran.items() if k not in ours}
    badperf = [k for k, v in extra.items() if k not in PERF_TAGS or not perf_value_ok(k, v)]
    diff = [k for k in ours if ran.get(k) != ours[k]]
    if e0 or e1 or badperf or diff:
        r["status"] = "INPUT_MODIFIED"; r["why"] = f"INCAR 문법 {e1[:3]} · 다른 태그 {diff} · 허용 밖·형식 이상 추가 {badperf}"; return r
    op = os.path.join(attdir, "OUTCAR")
    o = parse_outcar(open(op, encoding="utf-8", errors="replace").read()) if os.path.isfile(op) else None
    if o:
        r.update({k: v for k, v in o.items() if k != "settings"}); r["settings"] = o["settings"]
    if o and o["n_runs"] > 1:
        r["status"] = "MULTIPLE_RUNS"; r["why"] = f"OUTCAR 실행 머리줄 {o['n_runs']} 개 (정적 단일점은 1 개)"; return r
    if rc != 0:
        r["status"] = "EXECUTION_FAILED"; r["why"] = f"rc {rc}"; return r
    if o is None or not os.path.isfile(os.path.join(attdir, "OSZICAR")):
        r["status"] = "NOT_TERMINATED"; r["why"] = "rc 0 인데 OUTCAR/OSZICAR 없음"; return r
    if o["n_runs"] == 0:
        r["status"] = "OUTCAR_UNPARSEABLE"; r["why"] = "OUTCAR 에 실행 머리줄이 없다"; return r
    if not o["terminated"]:
        r["status"] = "NOT_TERMINATED"; return r
    if not o["converged"]:
        r["status"] = "SCF_NOT_CONVERGED"; return r
    tp, sp_, spp = (os.path.join(attdir, f) for f in ("POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"))
    if not all(os.path.isfile(x) for x in (tp, sp_, spp)):
        r["status"] = "POTCAR_UNVERIFIED"; r["why"] = "POTCAR.titel · POTCAR.sha256 · POTCAR.species.sha256 중 없음"; return r
    psha = open(sp_, encoding="utf-8").read().strip().lower()
    sps = [l.split() for l in open(spp, encoding="utf-8").read().splitlines() if l.strip()]
    if not HEX64.match(psha) or psha != str(a["sha256"].get("POTCAR", "")).lower() or len(sps) != len(job["potcar_spec"]) \
            or any(len(x) != 2 or not HEX64.match(x[1].lower()) for x in sps) or [x[0] for x in sps] != job["potcar_spec"]:
        r["status"] = "POTCAR_UNVERIFIED"; r["why"] = "POTCAR sha 형식·순서·실행 기록 불일치"; return r
    titel, zv = parse_titel(open(tp, encoding="utf-8", errors="replace").read())
    exp_t = [pp_registry["titel"][p] for p in job["potcar_spec"]] if pp_registry else job["pp_expected_titel"]
    if titel != exp_t or [round(x, 3) for x in zv] != [round(x, 3) for x in job["zval_expected"]] or o["outcar_titel"] != titel:
        r["status"] = "POTCAR_MISMATCH"; r["why"] = f"TITEL {titel} (기대 {exp_t}) · ZVAL {zv} · OUTCAR TITEL {o['outcar_titel']}"; return r
    r["potcar_species_sha256"] = {x[0]: x[1].lower() for x in sps}; r["potcar_sha256"] = psha
    if pp_registry:
        if any(pp_registry["species_sha256"].get(k) != v for k, v in r["potcar_species_sha256"].items()):
            r["status"] = "POTCAR_MISMATCH"; r["why"] = "봉인 등록부의 종별 sha 와 다르다"; return r
        want = (pp_registry.get("assembled_sha256") or {}).get(_spec_key(job))
        if want is not None and want != psha:
            r["status"] = "POTCAR_MISMATCH"; r["why"] = "봉인 등록부의 조립본 sha 와 다르다"; return r
        if pp_registry.get("vasp_version") is not None and o["version"] != pp_registry["vasp_version"]:
            r["status"] = "VERSION_MISMATCH"; r["why"] = f"VASP {o['version']!r} ≠ 등록부 {pp_registry['vasp_version']!r}"; return r
    missing, bad = audit_settings(o["settings"], job)
    if any(k in missing for k in ("NIONS", "NELECT")):
        r["status"] = "SYSTEM_UNVERIFIED"; r["why"] = f"OUTCAR 에 {missing} 없음"; return r
    if bad:
        r["status"] = "SETTINGS_MISMATCH"; r["why"] = "; ".join(bad); return r
    if missing:
        r["status"] = "SETTINGS_UNVERIFIED"; r["why"] = f"OUTCAR 되울림을 못 읽음: {missing} (파일럿으로 파서 확인)"; return r
    if o["TOTEN_eV"] is None or o["E_sigma0_eV"] is None:
        r["status"] = "ENERGY_UNPARSEABLE"; return r
    ref = fin(job.get("d3_2body_eV_ref"))
    if ref is None or o["Edisp_eV"] is None:
        r["status"] = "D3_UNVERIFIED"; r["why"] = "D3 기대값 또는 Edisp 없음"; return r
    if abs(o["Edisp_eV"] - ref) > D3_REL_TOL * abs(ref):
        r["status"] = "D3_MISMATCH"; r["why"] = f"Edisp {o['Edisp_eV']:.4f} vs ref {ref:.4f} eV (>1 % — 감쇠·3체·계수 오설정 의심)"; return r
    r["status"] = "OK"; return r


def check(out, ret, manifest_sha256, pp_registry=None):
    verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    J = {j["dir"]: j for j in meta["jobs"]}
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    res = {}
    for job in meta["jobs"]:
        bdir, rdir = os.path.join(run, job["dir"]), os.path.join(run, job["dir"] + "_r1")
        base = check_job(job, out, bdir, "0", pp_registry)
        if base["status"] in R1_ELIGIBLE and os.path.isdir(rdir):
            r1 = check_job(job, out, rdir, "r1", pp_registry)
            res[job["dir"]] = {**r1, "first_attempt": base["status"]} if r1["status"] == "OK" else {**base, "r1": r1["status"]}
        elif os.path.isdir(rdir):
            res[job["dir"]] = {**base, "r1_ignored": f"첫 시도 상태 {base['status']} 는 재시도 자격이 아니다 (사전등록: 실행 실패·미종료·미수렴만)"}
        else:
            res[job["dir"]] = base
    # 잡 사이 일관성 — 한 비교군 안의 계산이 같은 PP 데이터셋·같은 VASP 빌드인가 (어긋나면 어느 쪽이 맞는지 모르므로 전부 막는다)
    by_sp, by_spec, vers = {}, {}, set()
    for n, r in res.items():
        for sp, h in (r.get("potcar_species_sha256") or {}).items():
            by_sp.setdefault(sp, set()).add(h)
        if r.get("potcar_sha256"):
            by_spec.setdefault(_spec_key(J[n]), set()).add(r["potcar_sha256"])
        if r.get("version"):
            vers.add(r["version"])
    incons = sorted(sp for sp, hs in by_sp.items() if len(hs) > 1) + sorted(f"조립본[{k}]" for k, hs in by_spec.items() if len(hs) > 1)
    for n, r in res.items():
        if r["status"] != "OK":
            continue
        if incons:
            r["status"] = "POTCAR_INCONSISTENT"; r["why"] = f"잡 사이 POTCAR sha 가 갈린다: {incons}"
        elif len(vers) > 1:
            r["status"] = "VERSION_INCONSISTENT"; r["why"] = f"잡 사이 VASP 버전 줄이 갈린다: {sorted(vers)}"
    return meta, res


def check_exit(res):
    return 0 if res and all(v["status"] == "OK" for v in res.values()) else 3


def seal_pp(out, ret, manifest_sha256):
    """파일럿 반송(OK 인 잡)에서 종별 TITEL·sha · 조립본 sha · VASP 버전 줄을 뽑아 등록부를 만든다. 파일럿 잡이 OK 가 아니면 만들지 않는다."""
    meta, res = check(out, ret, manifest_sha256)
    ok = {n: r for n, r in res.items() if r["status"] == "OK"}
    miss = [p for p in PILOT_JOBS if p not in ok]
    if miss:
        raise PkgError(f"파일럿 잡이 OK 가 아니다: {[(p, res[p]['status']) for p in miss]} — 등록부를 만들지 않는다")
    J = {j["dir"]: j for j in meta["jobs"]}
    sp_sha, titel, asm, vers = {}, {}, {}, set()
    for n in PILOT_JOBS:
        for p, t in zip(J[n]["potcar_spec"], J[n]["pp_expected_titel"]):
            h = ok[n]["potcar_species_sha256"][p]
            if sp_sha.setdefault(p, h) != h:
                raise PkgError(f"파일럿 두 잡의 {p} sha 가 다르다")
            titel[p] = t
        if asm.setdefault(_spec_key(J[n]), ok[n]["potcar_sha256"]) != ok[n]["potcar_sha256"]:
            raise PkgError("파일럿 두 잡의 조립본 sha 가 다르다")
        vers.add(ok[n]["version"])
    if len(vers) != 1:
        raise PkgError(f"파일럿 두 잡의 VASP 버전 줄이 다르다: {sorted(vers)}")
    return {"schema": "aprime_v5_pp_registry/v2", "pp_set": PP_SET, "titel": titel, "species_sha256": sp_sha, "assembled_sha256": asm,
            "vasp_version": vers.pop(), "from_pilot": {n: ok[n].get("run_id") for n in PILOT_JOBS}, "package_manifest_sha256": manifest_sha256,
            "⛔": "이 등록부를 봉인(커밋·해시 기록)한 뒤 나머지 16 잡을 받는다 — 이후 모든 잡이 같아야 한다"}


def load_pp_registry(path, sha):
    if not path:
        return None
    if not sha or not HEX64.match(sha.lower()) or _sha(path) != sha.lower():
        raise PkgError("PP 등록부 sha 가 고정값과 다르다")
    return json.load(open(path, encoding="utf-8"))


# ───────────────────────── UMA 입력 (P0-4) ─────────────────────────
def load_uma(uma, meta, names):
    """uma_energies/v1 → ({이름: E_eV}, 오류 목록). 출처(S1)·구조(S3)·유한성 중 하나라도 어긋나면 오류로 남긴다 (조용히 버리지 않는다)."""
    errs, E = [], {}
    if not isinstance(uma, dict) or uma.get("schema") != "uma_energies/v1":
        return {}, ["schema 가 uma_energies/v1 이 아니다"]
    c = uma.get("calculator") or {}
    for k in ("model", "task", "inference_settings"):
        if c.get(k) != UMA_REQ[k]:
            errs.append(f"calculator.{k} = {c.get(k)!r} (결박 {UMA_REQ[k]!r})")
    ck = c.get("checkpoint")
    if not (isinstance(ck, list) and any(isinstance(x, dict) and x.get("sha256") == UMA_REQ["checkpoint_sha256"] for x in ck)):
        errs.append("체크포인트 sha256 이 S1 결박값과 다르다")
    if c.get("fairchem.core") not in UMA_REQ["fairchem_allowed"]:
        errs.append(f"fairchem.core {c.get('fairchem.core')!r} ∉ {UMA_REQ['fairchem_allowed']}")
    J = {j["structure"]: j for j in meta["jobs"]}
    rows = {}
    for k, v in (uma.get("energies") or {}).items():
        b = str(k).split("/")[-1]
        if b in rows:
            errs.append(f"이름 중복: {b}")
        rows[b] = v
    for n in names:
        v = rows.get(n)
        if not isinstance(v, dict):
            errs.append(f"{n}: UMA 에너지 없음"); continue
        j = J.get(n)
        if j is None:
            errs.append(f"{n}: 패키지에 없는 구조"); continue
        if v.get("sha256") != j["structure_sha256"]:
            errs.append(f"{n}: 구조 sha 가 S3v2 와 다르다")
        if v.get("n_atoms") != j["nions"]:
            errs.append(f"{n}: 원자 수 {v.get('n_atoms')} ≠ {j['nions']}")
        if v.get("pbc") != [True, True, True]:
            errs.append(f"{n}: pbc {v.get('pbc')} (3축 주기여야 한다)")
        e = fin(v.get("E_UMA_eV"))
        if e is None:
            errs.append(f"{n}: E_UMA_eV 가 유한한 수가 아니다 ({v.get('E_UMA_eV')!r})")
        else:
            E[n] = e
    return E, errs


# ───────────────────────── 집계 ─────────────────────────
def collect(out, ret, manifest_sha256, uma=None, pp_registry=None):
    meta, res = check(out, ret, manifest_sha256, pp_registry)
    J = {j["dir"]: j for j in meta["jobs"]}
    ok = lambda n: res.get(n, {}).get("status") == "OK"
    def dA(b, f, vals):
        if b not in vals or f not in vals:
            return None
        x = fin(vals[f] - vals[b]) if (fin(vals[f]) is not None and fin(vals[b]) is not None) else None
        return None if x is None else x * EV_J / (J[b]["area_A2"] * A2_M2)
    V = lambda key: {n: r[key] for n, r in res.items() if r["status"] == "OK" and fin(r.get(key)) is not None}
    F, S0, ED, NE = V("TOTEN_eV"), V("E_sigma0_eV"), V("Edisp_eV"), V("E_noentropy_eV")
    REF = {n: j["d3_2body_eV_ref"] for n, j in J.items() if fin(j.get("d3_2body_eV_ref")) is not None}
    smp = {}
    for k, (b, f) in G5_SAMPLES.items():
        w, wd, wne = dA(b, f, F), dA(b, f, ED), dA(b, f, NE)
        dref = dA(b, f, REF) if (ok(b) and ok(f)) else None
        pair = (wd - dref) if (wd is not None and dref is not None) else None
        over = (abs(pair) > D3_PAIR_BUDGET) if pair is not None else None
        smp[k] = {"bound": b, "far": f, "W_J_m2": w, "W_sigma0_J_m2": dA(b, f, S0), "dD3_J_m2": wd, "W_PBE_J_m2": (w - wd) if (w is not None and wd is not None) else None,
                  "mTS_term_J_m2": (w - wne) if (w is not None and wne is not None) else None,
                  "dD3_ref_J_m2": dref, "d3_pair_err_J_m2": pair, "d3_pair_over_budget": over,
                  "W_label": "⛔ D3 쌍 오차 예산 초과 — 총 W 를 PBE+D3(BJ) 값으로 인용 금지 (W_PBE·G5 Δ 는 영향 없음)" if over else None}
    base, bd3, bref = smp["①"]["W_J_m2"], smp["①"]["dD3_J_m2"], smp["①"]["dD3_ref_J_m2"]
    g3 = {"threshold": G3_DW, "d3_g3_budget": D3_G3_BUDGET}
    for tag, far in (("i", G3_JOBS[1]), ("ii", G3_JOBS[2])):
        b = G3_JOBS[0]
        Wx, Dx = dA(b, far, F), dA(b, far, ED)
        Rx = dA(b, far, REF) if (ok(b) and ok(far)) else None
        g3[f"dW_{tag}"] = (Wx - base) if (Wx is not None and base is not None) else None
        g3[f"d3_diffdiff_{tag}"] = ((Dx - bd3) - (Rx - bref)) if None not in (Dx, bd3, Rx, bref) else None
    if None in (g3["dW_i"], g3["dW_ii"], g3["d3_diffdiff_i"], g3["d3_diffdiff_ii"]):
        g3["status"] = "INCOMPLETE"
    elif max(abs(g3["d3_diffdiff_i"]), abs(g3["d3_diffdiff_ii"])) > D3_G3_BUDGET:
        g3["status"] = "INCOMPLETE (D3 차이의 차이 예산 초과)"
    else:
        g3["status"] = "PASS" if max(abs(g3["dW_i"]), abs(g3["dW_ii"])) <= G3_DW else "FAIL"
    g4 = {}
    for tag, lab in (("e70", "ENCUT 650"), ("k1", "k 4×3×1"), ("s05", "SIGMA ½")):
        Wx = dA(f"V5_s_outer_A_G4_{tag}_bound", f"V5_s_outer_A_G4_{tag}_far", F)
        dw = (Wx - base) if (Wx is not None and base is not None) else None
        g4[tag] = {"variant": lab, "W": Wx, "dW": dw, "status": "INCOMPLETE" if dw is None else ("PASS" if abs(dw) <= G4_DW else "FAIL")}
    st4 = {v["status"] for v in g4.values()}
    g4["status"] = "INCOMPLETE" if "INCOMPLETE" in st4 else ("FAIL" if "FAIL" in st4 else "PASS")
    rec = {"schema": "aprime_v5_vasp_collect/v2", "manifest_sha256": manifest_sha256, "return_bundle": return_manifest_info(ret, manifest_sha256),
           "energy_convention": "W = MP1 σ 0.136 eV 에서의 TOTEN(자유에너지) 차 / A — 0 K 점착에너지·실제 전자온도 자유에너지라 부르지 않는다 (CE Q2) · E(σ→0)·−TS 항 차 병기",
           "samples": smp, "G3": g3, "G4": g4, "jobs": res, "jobs_not_ok": sorted(n for n, v in res.items() if v["status"] != "OK"),
           "⛔": "VASP 비교군 — QE V2·V4 값과 빼거나 섞지 않는다"}
    if uma is not None:
        need = sorted({n for v in G5_SAMPLES.values() for n in v})
        E, errs = load_uma(uma, meta, need)
        keys = {str(k).split("/")[-1] for k in ((uma.get("energies") or {}) if isinstance(uma, dict) else {})}
        EG3, errs3 = load_uma(uma, meta, list(G3_JOBS)) if all(g in keys for g in G3_JOBS) else ({}, ["G3 세 구조 UMA 없음"])
        d = {}
        for k, s in smp.items():
            wu = dA(s["bound"], s["far"], E) if not errs else None
            d[k] = fin(s["W_J_m2"] - (wu + s["dD3_J_m2"])) if None not in (s["W_J_m2"], wu, s["dD3_J_m2"]) else None
        gm = {g: (sum(d[x] for x in m) / len(m) if all(d[x] is not None for x in m) else None) for g, m in G5_GROUPS.items()}
        complete = all(v is not None for v in d.values())
        raw_ok = complete and all(abs(v) <= G5_PER for v in d.values()) and all(abs(m) <= G5_MEAN for m in gm.values())
        g5 = {"Delta_J_m2": d, "group_mean": gm, "per_sample_max": G5_PER, "group_mean_max": G5_MEAN, "uma_errors": errs,
              "overall_mean_info": (sum(d.values()) / 5 if complete else None), "raw_error_criteria_met": raw_ok if complete else None,
              "usage_eligible": bool(raw_ok and not errs and g3["status"] == "PASS" and g4["status"] == "PASS"),
              "note": "①·⑤ 는 far 를 공유 — 독립 5 회 검증이 아니다 · ±0.10/±0.05 를 새 계면의 신뢰구간으로 옮기지 않는다 · PASS ≠ DEM 전달 승인 (카드 DEM 합의 별도)"}
        if errs:
            g5["status"] = "BLOCKED (UMA 입력 출처·값 검사 실패)"
        elif not complete:
            g5["status"] = "INCOMPLETE (분모 5 고정 · 교체 금지)"
        elif not raw_ok:
            g5["status"] = "FAIL"
        elif g3["status"] != "PASS" or g4["status"] != "PASS":
            g5["status"] = f"INCOMPLETE (G3 {g3['status']} · G4 {g4['status']} — 오차표만)"
        else:
            g5["status"] = "PASS"
        if EG3 and not errs3 and d.get("①") is not None:
            dg = {}
            for tag, far in (("i", G3_JOBS[1]), ("ii", G3_JOBS[2])):
                Wx, Dx, Ux = dA(G3_JOBS[0], far, F), dA(G3_JOBS[0], far, ED), dA(G3_JOBS[0], far, EG3)
                dg[tag] = fin((Wx - (Ux + Dx)) - d["①"]) if None not in (Wx, Ux, Dx) else None
            g5["residual_endpoint_diag_3b_prime"] = {"dDelta_J_m2": dg, "⚠": "진단 기록 (3b′ · 비준 전 · 판정 아님) — δΔ = δW_PBE − δW_UMA"}
        rec["G5"] = g5
    return rec


def collect_exit(rec):
    if rec["jobs_not_ok"]:
        return 3
    g5 = rec.get("G5")
    if g5 is None:
        return 12
    s = g5["status"]
    return 0 if s == "PASS" else (10 if s == "FAIL" else 11)


# ───────────────────────── selftest ─────────────────────────
DEFAULT_FAKE_VERSION = "vasp.6.4.2 20Jul23 (build Nov  1 2023) complex"


def _fake_outcar(job, E, Ed, *, conv=True, term=True, edisp=True, extra_run=False, encut=None, drop=(), efield=None, titel_override=None,
                 version=DEFAULT_FAKE_VERSION):
    t = [f" {version}"]
    for tt in (titel_override or job["pp_expected_titel"]):
        t += [f"   POTCAR:    {tt}", f"   TITEL  = {tt}"]
    echo = {"NIONS": f"   number of dos      NEDOS =    301   number of ions     NIONS = {job['nions']:6d}",
            "NELECT": f"   NELECT = {job['nelect_expected']:12.4f}    total number of electrons",
            "ENCUT": f"   ENCUT  = {encut if encut is not None else job['encut']:7.1f} eV  38.22 Ry    6.18 a.u.",
            "SIGMA": f"   ISMEAR =     1;   SIGMA  = {job['sigma']:7.2f}  broadening in eV -4-tet -1-fermi 0-gaus",
            "ISPIN": "   ISPIN  =      1    spin polarized calculation?", "IVDW": "   IVDW   =     12",
            "LDIPOL": "   LDIPOL =      T    correct potential (dipole corrections)", "IDIPOL": "   IDIPOL =      3    1-x, 2-y, 3-z, 4-all directions",
            "DIPOL": f"   DIPOL  =   0.5000  0.5000  {job['dipol_z']:.4f}"}
    t += [v for k, v in echo.items() if k not in drop]
    if efield is not None:
        t.append(f"   EFIELD = {efield}")
    if edisp:
        t.append(f"  Edisp (eV):  {Ed:12.5f}")
    t.append(" ------------------------ aborting loop because EDIFF is reached ----------------------------------------" if conv
             else " ------------------------ aborting loop EDIFF was not reached (unconverged)  ----------------------------")
    t += [f"  free  energy   TOTEN  =  {E:18.8f} eV", f"  energy  without entropy=  {E + 0.01:18.8f}  energy(sigma->0) =  {E + 0.005:18.8f}"]
    if term:
        t.append(" General timing and accounting informations for this job:")
    if extra_run:
        t += [f" {version}", "   NIONS =      9", f"  free  energy   TOTEN  =  {E + 1.0:18.8f} eV"]
    return "\n".join(t) + "\n"


FAKE_VASP = r'''
import os, re, sys, json
sys.path.insert(0, os.environ["FAKE_TOOLDIR"])
import build_v5_vasp_package as B
mode = os.environ.get("FAKE_MODE", "ok")
inc, _ = B.parse_incar_strict(open("INCAR").read())
job = re.search(r"V5 (\S+) \(single point\)", inc["SYSTEM"]).group(1)
sp, nn, cell, pos = B.parse_poscar_cart(open("POSCAR").read())
titel, zv = B.parse_titel(open("POTCAR").read())
ref = {j["dir"]: j for j in json.load(open(os.path.join(os.environ["FAKE_PKG"], "jobs.json")))["jobs"]}[job]["d3_2body_eV_ref"]
fj = {"nions": sum(nn), "nelect_expected": sum(z * n for z, n in zip(zv, nn)), "encut": float(inc["ENCUT"]), "sigma": float(inc["SIGMA"]),
      "dipol_z": float(inc["DIPOL"].split()[2]), "pp_expected_titel": titel}
conv = not (mode == "noconv_unless_amix" and "AMIX" not in inc)
B._write("OUTCAR", B._fake_outcar(fj, -1000.0 - 0.01 * len(job), ref, conv=conv, term=(mode != "noterm")))
B._write("OSZICAR", "DAV:   1\n" * 10)
sys.exit(1 if mode == "rc1" else 0)
'''


def _selftest():
    import shutil
    import subprocess
    import tempfile
    import numpy as np
    from ase import Atoms
    from ase.io import write
    ok = bad = 0
    def ck(c, m):
        nonlocal ok, bad
        if c:
            ok += 1
        else:
            bad += 1; print("  ✗", m)
    # ① 순수 함수
    at = Atoms("AgLiSAgClP", positions=[[0, 0, 1], [1, 0, 5], [2, 0, 6], [0, 1, 2], [3, 0, 7], [4, 0, 8]], cell=[10, 10, 30], pbc=True)
    txt, order, present = poscar_text(at, "t"); sp, nn, cell, pos = parse_poscar_cart(txt)
    ck(sp == ["Li", "P", "S", "Cl", "Ag"] and nn == [1, 1, 1, 1, 2] and all(np.allclose(pos[k], at.positions[order[k]]) for k in range(len(order))), "POSCAR 종 순서 · 대응표")
    try:
        poscar_text(Atoms("Fe", positions=[[0, 0, 0]], cell=[5, 5, 5]), "x"); ck(False, "⛔음성 모르는 원소 Fe")
    except PkgError:
        ck(True, "")
    ck(abs(dipol_z(0.85963, 0.03119) - 0.375225) < 1e-6, "DIPOL_z = 중심 − ½")
    ck(abs(check_dip_clear(Atoms("Ag2", positions=[[0, 0, 5.0], [0, 0, 22.0]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119) - 5.558) < 1e-2
       and abs(check_dip_clear(Atoms("Ag2", positions=[[0, 0, 1.0], [0, 0, 20.0]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119) - 4.5) < 1e-2, "쌍극자 여유 (위 원자 · 바닥 위 영상)")
    for z1, z2 in ((1.0, 26.0), (32.058 - 1.5, 10.0)):
        try:
            check_dip_clear(Atoms("Ag2", positions=[[0, 0, z1], [0, 0, z2]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119); ck(False, "⛔음성 쌍극자 여유 부족 통과")
        except PkgError:
            ck(True, "")
    i0, e0 = parse_incar_strict(incar_text("x", 520, 0.136, 0.3752))
    ck(not e0 and i0["VDW_RADIUS"] == "50.2" and i0["VDW_CNRADIUS"] == "21.17" and i0["IVDW"] == "12" and i0["DIPOL"] == "0.5 0.5 0.375200" and "AMIX" not in i0,
       "INCAR: D3 절단 명시 · IVDW · DIPOL · 혼합 태그 없음")
    d, e = parse_incar_strict("NCORE = 1 ; EFIELD = 0.01\n")
    ck(not e and d == {"NCORE": "1", "EFIELD": "0.01"}, f"INCAR 파서: ';' 는 문장 구분 (VASP 의미) — {d} {e}")
    ck(bool(parse_incar_strict("ENCUT = 520\nENCUT = 400\n")[1]) and bool(parse_incar_strict("NCORE = 1 \\\n")[1]), "⛔음성 INCAR 파서: 중복 태그 · 줄 이음 → 오류")
    ck(perf_value_ok("NCORE", "16") and not perf_value_ok("NCORE", "two") and not perf_value_ok("NCORE", "0") and perf_value_ok("LPLANE", ".TRUE.")
       and not perf_value_ok("LPLANE", "yes") and not perf_value_ok("EFIELD", "0"), "성능 태그 값 타입")
    ck(fin(float("nan")) is None and fin(float("inf")) is None and fin(True) is None and fin("1.0") is None and fin(2) == 2.0, "fin: NaN·Inf·bool·str 거부")
    po = parse_outcar(" vasp.6.4.2 x\n   TITEL  = A\n   TITEL  = B\n   TITEL  = A\n")
    ck(po["outcar_titel"] == ["A", "B"] and po["version"] == "vasp.6.4.2 x" and po["n_runs"] == 1, "OUTCAR TITEL 반복 인쇄 → 순서 보존 중복 제거 · 버전 줄 전체")
    # ② 합성 S3v2 패키지 → build() 로 실제 경로 시험 (D3 가 1 % 문턱이 시험 이동보다 크도록 Ag 3 층 슬랩을 붙인다)
    with tempfile.TemporaryDirectory() as T:
        s3 = os.path.join(T, "s3"); os.makedirs(os.path.join(s3, "structures")); os.makedirs(os.path.join(s3, "qe"))
        names_struct = sorted({n for v in G5_SAMPLES.values() for n in v} | set(G3_JOBS))
        slab = [[0.5 + ix * 3.35, 0.5 + iy * 2.873, 20.0 + iz * 2.4] for ix in range(3) for iy in range(7) for iz in range(3)]
        dip = lambda c: {"emaxpos": round(14.0 / c, 5), "eopreg": round(1.0 / c, 5)}
        ssha = {}
        for n in names_struct:
            c = 42.0 if "G3" in n else 40.0
            z_ad = 7.0 if ("far" in n) else (5.0 if "p05" in n else 4.5)
            a = Atoms("LiPSClAg" + "Ag" * len(slab), positions=[[1, 1, 1.0], [3, 3, 2.0], [5, 5, 3.0], [7, 7, 3.6], [2, 6, z_ad + (1.0 if "far_ii" in n else 0.0)]] + slab,
                      cell=[10.055, 20.11, c], pbc=True)
            p = os.path.join(s3, "structures", f"{n}.extxyz"); write(p, a, format="extxyz"); ssha[n] = _sha(p)
        mp = os.path.join(s3, "s3_manifest.json"); _write(mp, json.dumps({"structures_sha256": ssha}))
        qj = []
        for n in names_struct:
            qj.append({"dir": n, "model": "V5", "kind": "g3" if "G3" in n else "scf", "structure": n, "kpts": [3, 2, 1],
                       "dip": dip(42.0 if "G3" in n else 40.0), "tags": {}, "pw_in_sha256": "0" * 64})
        for t4 in ("e70", "k1", "s05"):
            for e_ in ("bound", "far"):
                qj.append({"dir": f"V5_s_outer_A_G4_{t4}_{e_}", "model": "V5", "kind": "g4", "structure": f"V5_s_outer_A_{e_}", "kpts": [4, 3, 1] if t4 == "k1" else [3, 2, 1],
                           "dip": dip(40.0), "tags": {"G4": f"G4_{t4}_{e_}", **({"degauss_halved": True} if t4 == "s05" else {})}, "pw_in_sha256": "0" * 64})
        qj.append({"dir": "probe_x", "model": "V5", "kind": "probe", "structure": "V5_s_outer_A_far", "kpts": [3, 2, 1], "dip": dip(40.0)})
        _write(os.path.join(s3, "qe", "jobs.json"), json.dumps({"s3_manifest_sha256": _sha(mp), "jobs": qj}))
        out = os.path.join(T, "pkg")
        meta, msha = build(s3, out)
        J = {j["dir"]: j for j in meta["jobs"]}
        ck(len(meta["jobs"]) == 18 and J["V5_s_outer_A_G4_e70_bound"]["encut"] == 650 and J["V5_s_outer_A_G4_s05_far"]["sigma"] == 0.068
           and J["V5_s_outer_A_G4_k1_far"]["kpts"] == [4, 3, 1] and all(fin(j["d3_2body_eV_ref"]) is not None for j in meta["jobs"]), "build: 18 잡 · G4 변형 · D3 기대값 전부")
        ck(min(abs(j["d3_2body_eV_ref"]) for j in meta["jobs"]) > 12.0, "합성 구조 |D3| > 12 eV (1 % 문턱 > 시험 이동 0.10 eV — 예산 시험이 1 % 검사에 가리지 않게)")
        ck(verify_manifest(out, msha) > 90, "승인본 대조 통과 (정상 · 파일 90 개 넘게)")
        with open(os.path.join(out, "MANIFEST.sha256"), "rb") as fh:
            ck(b"\r\n" not in fh.read(), "LF 고정 (CRLF 없음)")
        ret = os.path.join(T, "ret"); run = os.path.join(ret, "run")
        A = J["V5_s_outer_A_bound"]["area_A2"]; dE = lambda Wv: Wv * A * A2_M2 / EV_J
        REF = {n: J[n]["d3_2body_eV_ref"] for n in J}
        E = {n: -1000.0 for n in J}
        for k, (b, f) in G5_SAMPLES.items():
            E[f] = E[b] + dE(0.60 if k == "③" else 0.50)
        E["V5_s_outer_A_far"] = E["V5_s_outer_A_bound"] + dE(0.50); E["V5_s_outer_A_p05_bound"] = E["V5_s_outer_A_far"] - dE(0.45)
        for x, w in (("far_i", 0.505), ("far_ii", 0.509)):
            E[f"V5_s_outer_A_G3_c2_{x}"] = E["V5_s_outer_A_G3_c2_bound"] + dE(w)
        for t4, w in (("e70", 0.51), ("k1", 0.49), ("s05", 0.50)):
            E[f"V5_s_outer_A_G4_{t4}_far"] = E[f"V5_s_outer_A_G4_{t4}_bound"] + dE(w)
        ED = {n: REF[n] for n in J}
        SPSHA = {p: hashlib.sha256(p.encode()).hexdigest() for p in POTCAR_MAP.values()}
        def mk(n, att="0", *, outcar=None, incar_extra="", incar=None, rc=0, titel=None, spsha=None, psha_override=None, drop=(), no_out=False, tamper_after=None, **kw):
            j = J[n]; d = os.path.join(run, n if att == "0" else n + "_r1"); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
            src = os.path.join(out, "jobs", n)
            for f in ("POSCAR", "KPOINTS"):
                shutil.copy(os.path.join(src, f), d)
            _write(os.path.join(d, "INCAR"), incar if incar is not None else open(os.path.join(src, "INCAR.r1" if att == "r1" else "INCAR")).read() + incar_extra)
            if not no_out:
                _write(os.path.join(d, "OSZICAR"), "DAV:   1\n" * 20)
                _write(os.path.join(d, "OUTCAR"), outcar if outcar is not None else _fake_outcar(j, E[n], ED[n], **kw))
            sp_ = spsha or SPSHA
            _write(os.path.join(d, "POTCAR.titel"), "".join(f"   TITEL  = {t}\n   POMASS = 1; ZVAL   = {z:8.3f}    mass and valenz\n   LEXCH  = PE\n"
                                                           for t, z in zip(titel or j["pp_expected_titel"], j["zval_expected"])))
            _write(os.path.join(d, "POTCAR.species.sha256"), "".join(f"{p} {sp_[p]}\n" for p in j["potcar_spec"]))
            psha = psha_override or hashlib.sha256("".join(sp_[p] for p in j["potcar_spec"]).encode()).hexdigest()
            _write(os.path.join(d, "POTCAR.sha256"), psha + "\n")
            shas = {f: (_sha(os.path.join(d, f)) if os.path.isfile(os.path.join(d, f)) else "") for f in ("INCAR", "POSCAR", "KPOINTS", "OUTCAR", "OSZICAR")}
            _write(os.path.join(d, "attempt.json"), json.dumps({"job": n, "attempt": att, "run_id": f"rid-{n}-{att}", "rc": rc, "sha256": {**shas, "POTCAR": psha}}))
            for f in drop:
                os.remove(os.path.join(d, f))
            if tamper_after:
                tamper_after(d)
            return d
        def st(n, reg=None):
            return check(out, ret, msha, reg)[1][n]["status"]
        for n in J:
            mk(n, incar_extra="NCORE = 16\nKPAR = 2\nLPLANE = .TRUE.\n")
        _, res = check(out, ret, msha)
        ck(all(v["status"] == "OK" for v in res.values()) and check_exit(res) == 0,
           f"정상 대조군: 18 잡 OK (성능 태그 3 개 허용) — {[(n, v['status'], v.get('why')) for n, v in res.items() if v['status'] != 'OK'][:3]}")
        uma = {"schema": "uma_energies/v1", "calculator": {"model": "uma-s-1p1", "task": "omat", "inference_settings": "default", "fairchem.core": "2.21.0",
               "checkpoint": [{"sha256": UMA_REQ["checkpoint_sha256"]}]}, "energies": {}}
        dD3 = {k: (REF[f] - REF[b]) * EV_J / (A * A2_M2) for k, (b, f) in G5_SAMPLES.items()}
        want = {"①": 0.01, "②": 0.01, "③": 0.02, "④": 0.01}
        row = lambda n, e: {"sha256": J[n]["structure_sha256"], "n_atoms": J[n]["nions"], "pbc": [True, True, True], "E_UMA_eV": e}
        for k, (b, f) in G5_SAMPLES.items():
            if k == "⑤":
                continue
            w = 0.60 if k == "③" else 0.50
            uma["energies"][b] = row(b, 0.0); uma["energies"][f] = row(f, dE(w - dD3[k] - want[k]))
        uma["energies"]["V5_s_outer_A_p05_bound"] = row("V5_s_outer_A_p05_bound", uma["energies"]["V5_s_outer_A_far"]["E_UMA_eV"] - dE(0.45 - dD3["⑤"]))
        rc_ = collect(out, ret, msha, uma)
        ck(rc_["G3"]["status"] == "PASS" and rc_["G4"]["status"] == "PASS" and rc_["G5"]["status"] == "PASS" and collect_exit(rc_) == 0
           and abs(rc_["G5"]["Delta_J_m2"]["①"] - 0.01) < 1e-6 and rc_["G5"]["usage_eligible"] is True and rc_["G5"]["raw_error_criteria_met"] is True
           and rc_["samples"]["①"]["mTS_term_J_m2"] is not None and abs(rc_["samples"]["①"]["mTS_term_J_m2"]) < 1e-9,
           f"정상 대조군: G3·G4·G5 PASS · 종료 0 · −TS 항 차 기록 — {rc_['G3']['status']} {rc_['G4']['status']} {rc_['G5']['status']} {rc_['G5']['Delta_J_m2']}")
        json.dumps(rc_, allow_nan=False)
        # ③ P0-1 성능 태그 우회
        F_ = "V5_s_outer_A_far"
        mk(F_, incar_extra="NCORE = 1 ; EFIELD = 0.01\n")
        ck(st(F_) == "INPUT_MODIFIED", "⛔음성 P0-1 'NCORE = 1 ; EFIELD = 0.01' → INPUT_MODIFIED")
        for extra, why in (("NCORE = 1 ; ENCUT = 400\n", "세미콜론 ENCUT"), ("NCORE = 16\nNCORE = 8\n", "중복"), ("KPAR = two\n", "타입"),
                           ("NCORE = 16 \\\n", "줄 이음"), ("NWRITE = 0\n", "허용 밖")):
            mk(F_, incar_extra=extra)
            ck(st(F_) == "INPUT_MODIFIED", f"⛔음성 P0-1 성능 태그 {why} → INPUT_MODIFIED")
        # ④ P0-2 지난 출력 · 복수 실행 · 설정 되울림
        mk(F_, rc=1)
        ck(st(F_) == "EXECUTION_FAILED", "⛔음성 P0-2 rc=1 (OUTCAR 는 정상이어도) → EXECUTION_FAILED")
        mk(F_, tamper_after=lambda d: _write(os.path.join(d, "OUTCAR"), open(os.path.join(d, "OUTCAR")).read() + " \n"))
        ck(st(F_) == "ATTEMPT_MISMATCH", "⛔음성 P0-2 실행 뒤 OUTCAR 교체 → ATTEMPT_MISMATCH")
        good_outcar = _fake_outcar(J[F_], E[F_], ED[F_])
        mk(F_, rc=1, no_out=True, tamper_after=lambda d: (_write(os.path.join(d, "OUTCAR"), good_outcar), _write(os.path.join(d, "OSZICAR"), "DAV: 1\n")))
        ck(st(F_) == "ATTEMPT_MISMATCH", "⛔음성 P0-2 실패한 실행(OUTCAR 없음) 뒤에 지난 정상 OUTCAR 를 넣음 → ATTEMPT_MISMATCH")
        mk(F_, extra_run=True)
        ck(st(F_) == "MULTIPLE_RUNS", "⛔음성 P0-2 두 번째 미완결 실행 붙임 → MULTIPLE_RUNS")
        mk(F_, encut=400.0)
        ck(st(F_) == "SETTINGS_MISMATCH", "⛔음성 P0-2 OUTCAR ENCUT 400 (INCAR 520) → SETTINGS_MISMATCH")
        mk(F_, efield=0.01)
        ck(st(F_) == "SETTINGS_MISMATCH", "⛔음성 OUTCAR EFIELD ≠ 0 → SETTINGS_MISMATCH")
        mk(F_, drop=("attempt.json",))
        ck(st(F_) == "MISSING", "⛔음성 attempt.json 없음 → MISSING")
        mk(F_, tamper_after=lambda d: _write(os.path.join(d, "attempt.json"), json.dumps({**json.load(open(os.path.join(d, "attempt.json"))), "rc": "0"})))
        ck(st(F_) == "ATTEMPT_MISMATCH", "⛔음성 attempt.json rc 가 문자열 → ATTEMPT_MISMATCH")
        for key in ("IVDW", "DIPOL", "SIGMA", "ENCUT"):
            mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], drop=(key,)))
            ck(st(F_) == "SETTINGS_UNVERIFIED", f"⛔음성 되울림 {key} 못 읽음 → SETTINGS_UNVERIFIED (통과 아님)")
        # ⑤ P0-3 POTCAR · 버전
        mk(F_, drop=("POTCAR.sha256",))
        ck(st(F_) == "POTCAR_UNVERIFIED", "⛔음성 P0-3 POTCAR.sha256 삭제 → POTCAR_UNVERIFIED")
        mk(F_, titel=[t.replace("02Apr2005", "06Sep2000") for t in J[F_]["pp_expected_titel"]])
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 P0-3 TITEL 날짜 다름 → POTCAR_MISMATCH")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=[t.replace("Ag 02Apr2005", "Ag_pv 06Sep2000") for t in J[F_]["pp_expected_titel"]]))
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 P0-3 OUTCAR TITEL ≠ POTCAR.titel → POTCAR_MISMATCH")
        mk(F_)
        mk("V5_s_outer_A_bound", spsha={**SPSHA, "Ag": "f" * 64})
        rs = check(out, ret, msha)[1]
        ck(rs[F_]["status"] == "POTCAR_INCONSISTENT" and check_exit(rs) == 3, "⛔음성 P0-3 bound 만 다른 Ag sha → POTCAR_INCONSISTENT · 종료 3")
        mk("V5_s_outer_A_bound", psha_override="a" * 64)
        ck(st(F_) == "POTCAR_INCONSISTENT", "⛔음성 P0-3 종별 sha 는 같고 조립본 sha 만 다름 → POTCAR_INCONSISTENT")
        mk("V5_s_outer_A_bound")
        reg = {"titel": {POTCAR_MAP[s]: PP_EXPECTED_TITEL[s] for s in SPECIES_ORDER}, "species_sha256": {**SPSHA, "Ag": "e" * 64}}
        ck(st(F_, reg) == "POTCAR_MISMATCH", "⛔음성 봉인 등록부와 다른 종별 sha → POTCAR_MISMATCH")
        mk("V5_s_outer_B_far", version="vasp.6.3.0 16May22 (build Jun 1 2022) complex")
        ck(st(F_) == "VERSION_INCONSISTENT", "⛔음성 잡 하나만 다른 VASP 빌드 → 전 배치 VERSION_INCONSISTENT")
        mk("V5_s_outer_B_far")
        reg_ok = seal_pp(out, ret, msha)
        ck(st(F_, {**reg_ok, "vasp_version": "vasp.6.5.1 other"}) == "VERSION_MISMATCH", "⛔음성 등록부와 다른 VASP 버전 → VERSION_MISMATCH")
        ck(st(F_, reg_ok) == "OK" and st(F_, {**reg_ok, "assembled_sha256": {_spec_key(J[F_]): "b" * 64}}) == "POTCAR_MISMATCH",
           "등록부 대조: 봉인값이면 OK · 조립본 sha 다르면 POTCAR_MISMATCH")
        # ⑥ P0-4 UMA
        u_nan = json.loads(json.dumps(uma))
        for v in u_nan["energies"].values():
            v["E_UMA_eV"] = float("nan")
        rr = collect(out, ret, msha, u_nan)
        ck(rr["G5"]["status"].startswith("BLOCKED") and collect_exit(rr) == 11 and rr["G5"]["usage_eligible"] is False, f"⛔음성 P0-4 UMA 전부 NaN → BLOCKED (PASS 아님) — {rr['G5']['status']}")
        json.dumps(rr, allow_nan=False)
        for mut, why in ((lambda u: u["calculator"].update({"checkpoint": [{"sha256": "0" * 64}]}), "체크포인트 sha"),
                         (lambda u: u["calculator"].update({"task": "omol"}), "task"), (lambda u: u["calculator"].update({"fairchem.core": "1.0.0"}), "버전"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"sha256": "1" * 64}), "구조 sha"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"pbc": [True, True, False]}), "pbc"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"E_UMA_eV": True}), "bool 에너지"),
                         (lambda u: u["energies"].update({"x/V5_s_outer_B_far": dict(u["energies"]["V5_s_outer_B_far"])}), "이름 중복")):
            u = json.loads(json.dumps(uma)); mut(u)
            ck(collect(out, ret, msha, u)["G5"]["status"].startswith("BLOCKED"), f"⛔음성 P0-4 UMA {why} 틀림 → BLOCKED")
        # ⑦ P1-1 승인본
        inc = os.path.join(out, "jobs", F_, "INCAR"); orig = open(inc).read()
        _write(inc, orig.replace("ENCUT = 520.0", "ENCUT = 400.0")); mk(F_, incar=orig.replace("ENCUT = 520.0", "ENCUT = 400.0"))
        try:
            check(out, ret, msha); ck(False, "⛔음성 P1-1 기대·반송 INCAR 동시 변조를 통과시켰다")
        except PkgError:
            ck(True, "")
        _write(inc, orig); mk(F_)
        try:
            check(out, ret, "0" * 64); ck(False, "⛔음성 P1-1 틀린 고정값 통과")
        except PkgError:
            ck(True, "")
        jobs_path = os.path.join(out, "jobs.json"); keep = open(jobs_path).read()
        jj = json.loads(keep); jj["jobs"][0]["d3_2body_eV_ref"] = None; _write(jobs_path, json.dumps(jj))
        try:
            check(out, ret, msha); ck(False, "⛔음성 D3 기대값 None 으로 바꾼 jobs.json 이 승인본 대조를 통과")
        except PkgError:
            ck(True, "")
        _write(jobs_path, keep)
        # ⑧ P1-2 결측 · 종료코드
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], drop=("NELECT",)))
        ck(st(F_) == "SYSTEM_UNVERIFIED", "⛔음성 P1-2 NELECT 줄 없음 → SYSTEM_UNVERIFIED")
        mk(F_, edisp=False)
        ck(st(F_) == "D3_UNVERIFIED", "⛔음성 Edisp 없음 → D3_UNVERIFIED")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_] * 1.05))
        ck(st(F_) == "D3_MISMATCH", "⛔음성 Edisp 5 % 차 → D3_MISMATCH")
        mk(F_)
        empty = os.path.join(T, "empty"); os.makedirs(empty)
        ck(check_exit(check(out, empty, msha)[1]) == 3, "⛔음성 P1-2 빈 반송 → 종료코드 3 (0 아님)")
        # ⑨ P1-3 r1 자격
        B_ = "V5_s_outer_B_far"
        def break_poscar(d):
            _write(os.path.join(d, "POSCAR"), "x\n")
            aj = json.load(open(os.path.join(d, "attempt.json"))); aj["sha256"]["POSCAR"] = _sha(os.path.join(d, "POSCAR"))
            _write(os.path.join(d, "attempt.json"), json.dumps(aj))
        mk(B_, tamper_after=break_poscar); mk(B_, "r1")
        r9 = check(out, ret, msha)[1][B_]
        ck(r9["status"] == "INPUT_MODIFIED" and "r1_ignored" in r9, f"⛔음성 P1-3 첫 시도 INPUT_MODIFIED + 정상 r1 → 승격 안 함 — {r9['status']}")
        shutil.rmtree(os.path.join(run, B_))
        ck(st(B_) == "MISSING", "⛔음성 P1-3 첫 시도 없는 r1 → 채택 안 함 (MISSING)")
        mk(B_, conv=False)
        r9c = check(out, ret, msha)[1][B_]
        ck(r9c["status"] == "OK" and r9c["attempt"] == "r1" and r9c["first_attempt"] == "SCF_NOT_CONVERGED", "r1 채택: 첫 시도 미수렴 + 사전등록 r1 정상 · 첫 상태 보존")
        mk(B_, rc=1, no_out=True)
        r9d = check(out, ret, msha)[1][B_]
        ck(r9d["status"] == "OK" and r9d["first_attempt"] == "EXECUTION_FAILED", f"r1 채택: 첫 시도가 OUTCAR 도 없이 rc 1 로 죽음 → EXECUTION_FAILED 는 자격 — {r9d.get('first_attempt')}")
        mk(B_, rc=0, no_out=True)
        r9e = check(out, ret, msha)[1][B_]
        ck(r9e["status"] == "OK" and r9e["first_attempt"] == "NOT_TERMINATED", f"r1 채택: rc 0 인데 OUTCAR 없음 → NOT_TERMINATED — {r9e.get('first_attempt')}")
        shutil.rmtree(os.path.join(run, B_ + "_r1")); mk(B_)
        # ⑩ P1-4 D3 예산
        G_ = G3_JOBS[2]
        mk(G_, outcar=_fake_outcar(J[G_], E[G_] + dE(0.0015), ED[G_] + dE(0.0015)))     # 실물처럼 TOTEN 에도 같은 D3 오차가 들어간다
        r10 = collect(out, ret, msha, uma)
        ck(r10["G3"]["status"].startswith("INCOMPLETE (D3") and r10["G5"]["status"].startswith("INCOMPLETE (G3") and r10["G5"]["usage_eligible"] is False,
           f"⛔음성 P1-4 G3 차이의 차이 0.0015 > 0.001 → G3 INCOMPLETE (D3) → G5 오차표만 — {r10['G3']['status']} / {r10['G5']['status']}")
        mk(G_)
        mk(B_, outcar=_fake_outcar(J[B_], E[B_] + dE(0.008), ED[B_] + dE(0.008)))       # TOTEN = E_PBE + Edisp → 같은 오차가 W 와 ΔD3 양쪽에
        r11 = collect(out, ret, msha, uma)
        ck(r11["samples"]["②"]["d3_pair_over_budget"] is True and abs(r11["samples"]["②"]["d3_pair_err_J_m2"] - 0.008) < 1e-6 and r11["samples"]["②"]["W_label"]
           and r11["samples"]["①"]["W_label"] is None and r11["G5"]["Delta_J_m2"]["②"] is not None and abs(r11["G5"]["Delta_J_m2"]["②"] - 0.01) < 1e-6,
           f"⛔음성 P1-4 표본 ② 쌍 오차 0.008 > 0.005 → 인용 금지 라벨 · G5 Δ 는 불변 (D3 상쇄) — {r11['samples']['②'].get('d3_pair_err_J_m2')}")
        mk(B_)
        # ⑪ 3c · FAIL · 누락 · 미평가
        E_bak = E[G_]; E[G_] = E[G3_JOBS[0]] + dE(0.512); mk(G_)
        r12 = collect(out, ret, msha, uma)
        ck(r12["G3"]["status"] == "FAIL" and r12["G5"]["status"] == "INCOMPLETE (G3 FAIL · G4 PASS — 오차표만)" and r12["G5"]["raw_error_criteria_met"] is True
           and r12["G5"]["usage_eligible"] is False and collect_exit(r12) == 11, f"3c: G3 FAIL → 'INCOMPLETE (G3 FAIL · 오차표만)' · 원시 기준 충족 · 사용 자격 없음 — {r12['G5']['status']}")
        E[G_] = E_bak; mk(G_)
        u3 = json.loads(json.dumps(uma)); u3["energies"]["V5_li_outer_A_far"]["E_UMA_eV"] -= dE(0.15)
        r13 = collect(out, ret, msha, u3)
        ck(r13["G5"]["status"] == "FAIL" and collect_exit(r13) == 10, f"⛔음성 표본 ③ |Δ| 0.17 → FAIL (종료 10) — {r13['G5']['status']}")
        os.remove(os.path.join(run, "V5_li_outer_B_bound", "OUTCAR"))
        r14 = collect(out, ret, msha, uma)
        ck(collect_exit(r14) == 3 and r14["G5"]["status"].startswith("INCOMPLETE (분모"), f"⛔음성 표본 누락 → 종료 3 · INCOMPLETE (분모 5) — {r14['G5']['status']}")
        mk("V5_li_outer_B_bound")
        ck(collect_exit(collect(out, ret, msha, None)) == 12, "UMA 없음 → 종료 12 (G5 미평가)")
        # ⑫ 3b′ 진단 (G3 세 구조 UMA 가 있을 때만 · 판정 아님)
        u4 = json.loads(json.dumps(uma))
        for g in G3_JOBS:
            u4["energies"][g] = row(g, 0.0)
        u4["energies"][G_]["E_UMA_eV"] = dE(0.509 - (REF[G_] - REF[G3_JOBS[0]]) * EV_J / (A * A2_M2) - 0.01 - 0.03)
        r15 = collect(out, ret, msha, u4)
        dg = r15["G5"].get("residual_endpoint_diag_3b_prime", {}).get("dDelta_J_m2", {})
        ck(dg.get("ii") is not None and abs(dg["ii"] - 0.03) < 1e-6 and r15["G5"]["status"] == "PASS", f"3b′: δΔ(ii) = +0.03 기록 · 판정 불변 — {dg} {r15['G5']['status']}")
        # ⑬ seal_pp
        regd = seal_pp(out, ret, msha)
        ck(regd["species_sha256"] == SPSHA and regd["titel"]["Ag"] == PP_EXPECTED_TITEL["Ag"] and regd["vasp_version"] == " ".join(DEFAULT_FAKE_VERSION.split())
           and len(regd["assembled_sha256"]) == 1, "seal_pp: 파일럿 두 잡에서 종별·조립본 sha · TITEL · VASP 버전 등록부")
        mk(F_, rc=1)
        try:
            seal_pp(out, ret, msha); ck(False, "⛔음성 파일럿이 OK 가 아닌데 등록부를 만들었다")
        except PkgError:
            ck(True, "")
        mk(F_)
        # ⑭ 배포 러너 실제 실행 (가짜 VASP · bash) — 러너와 검사기가 같은 규칙을 쓰는지
        if not all(shutil.which(x) for x in ("bash", "sha256sum", "tar")):
            print("  ⚠ SKIP 러너 실행 시험 (bash · sha256sum · tar 중 없음) — 통과로 세지 않는다")
        else:
            fake = os.path.join(T, "fake_vasp.py"); _write(fake, FAKE_VASP)
            potdir = os.path.join(T, "potcars")
            for s in SPECIES_ORDER:
                os.makedirs(os.path.join(potdir, POTCAR_MAP[s]))
                _write(os.path.join(potdir, POTCAR_MAP[s], "POTCAR"), f"  {PP_EXPECTED_TITEL[s]}\n   VRHFIN ={s}: test\n   LEXCH  = PE\n"
                       f"   TITEL  = {PP_EXPECTED_TITEL[s]}\n   POMASS =    1.000; ZVAL   =   {ZVAL[s]:7.3f}    mass and valenz\n")
            perf = os.path.join(T, "perf.txt"); _write(perf, "NCORE = 4\nKPAR = 1\n")
            badperf = os.path.join(T, "perf_bad.txt"); _write(badperf, "NCORE = 1 ; EFIELD = 0.01\n")
            def run_pkg(tag, vasp_cmd, mode="ok", perf_file=perf, fresh=True):
                w = os.path.join(T, f"w_{tag}")
                if fresh:
                    shutil.copytree(out, w)
                env = {**os.environ, "VASP_CMD": vasp_cmd, "POTCAR_DIR": potdir, "JOBS": " ".join(PILOT_JOBS), "FAKE_TOOLDIR": HERE, "FAKE_PKG": out, "FAKE_MODE": mode}
                if perf_file is not None:
                    env["PERF_TAGS_FILE"] = perf_file
                p = subprocess.run(["bash", os.path.join(w, "run_all.sh")], env=env, capture_output=True, text=True, timeout=300)
                return w, p.returncode, p.stdout + p.stderr
            py = f"{sys.executable} {fake}"
            w, rcode, log = run_pkg("ok", py)
            rs = check(out, w, msha)[1]
            ck(rcode == 0 and all(rs[p]["status"] == "OK" for p in PILOT_JOBS) and check_exit(rs) == 3 and os.path.isfile(os.path.join(w, "V5_vasp_return.tgz")),
               f"러너 실행: 파일럿 2 잡 성공 · 검사 OK (나머지 16 잡 MISSING → 종료 3) — rc {rcode} {[(p, rs[p]['status'], rs[p].get('why')) for p in PILOT_JOBS]} {log[-300:]}")
            ck(return_manifest_info(w, msha) == {"present": True, "matches_pinned": True}, "반송 묶음의 MANIFEST = 고정값")
            _, rcode2, log2 = run_pkg("ok", py, fresh=False)
            rs2 = check(out, w, msha)[1]
            ck(rcode2 == 1 and "이미 있다" in log2 and all(rs2[p]["status"] == "OK" for p in PILOT_JOBS), f"⛔음성 러너 재실행: 기존 시도 폴더 거부 · 종료 1 · 앞 결과 보존 — rc {rcode2}")
            w3, rcode3, _ = run_pkg("false", "false")
            rs3 = check(out, w3, msha)[1]
            ck(rcode3 == 1 and all(rs3[p]["status"] == "EXECUTION_FAILED" and rs3[p].get("r1") == "EXECUTION_FAILED" for p in PILOT_JOBS),
               f"⛔음성 러너 VASP_CMD=false → 종료 1 · EXECUTION_FAILED (r1 도) — rc {rcode3} {[(p, rs3[p]['status'], rs3[p].get('r1')) for p in PILOT_JOBS]}")
            w4, rcode4, log4 = run_pkg("badperf", py, perf_file=badperf)
            ck(rcode4 == 2 and not any(os.path.isdir(os.path.join(w4, "run", p)) for p in PILOT_JOBS), f"⛔음성 러너 성능 파일 'NCORE = 1 ; EFIELD = 0.01' → 종료 2 · 아무것도 안 돎 — rc {rcode4}")
            w5, rcode5, _ = run_pkg("noperf", py, perf_file=os.path.join(T, "없는_파일.txt"))
            ck(rcode5 == 2, f"⛔음성 러너 읽을 수 없는 성능 파일 → 종료 2 — rc {rcode5}")
            w6, rcode6, _ = run_pkg("rescue", py, mode="noconv_unless_amix")
            rs6 = check(out, w6, msha)[1]
            ck(rcode6 == 0 and all(rs6[p]["status"] == "OK" and rs6[p]["attempt"] == "r1" and rs6[p]["first_attempt"] == "SCF_NOT_CONVERGED" for p in PILOT_JOBS),
               f"러너 r1: 첫 시도 미수렴 → 사전등록 재시도 성공 · 검사 OK(r1) — rc {rcode6} {[(p, rs6[p]['status'], rs6[p].get('first_attempt')) for p in PILOT_JOBS]}")
            w7, rcode7, _ = run_pkg("rc1", py, mode="rc1")
            rs7 = check(out, w7, msha)[1]
            ck(rcode7 == 1 and all(rs7[p]["status"] == "EXECUTION_FAILED" for p in PILOT_JOBS), f"⛔음성 러너 정상 OUTCAR 인데 rc 1 → 종료 1 · EXECUTION_FAILED — rc {rcode7}")
    print(f"{'✅' if not bad else '⛔'} build_v5_vasp_package selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for f in ("--build", "--check", "--collect", "--seal_pp", "--selftest"):
        ap.add_argument(f, action="store_true")
    ap.add_argument("--pkg", default="db/inputs/wad_aprime_s3v2_2026_09_26"); ap.add_argument("--out"); ap.add_argument("--ret"); ap.add_argument("--uma")
    ap.add_argument("--json"); ap.add_argument("--manifest_sha256"); ap.add_argument("--pp_registry"); ap.add_argument("--pp_registry_sha256")
    a = ap.parse_args()
    if a.selftest:
        return _selftest()
    try:
        if a.build:
            meta, msha = build(a.pkg, a.out)
            print(f"✅ {len(meta['jobs'])} 잡 → {a.out} · MANIFEST.sha256 sha256 {msha}")
            print(f"   규모: {meta['estimate']}")
            return 0
        if not (a.out and a.ret):
            ap.error("--out 과 --ret 가 필요하다")
        reg = load_pp_registry(a.pp_registry, a.pp_registry_sha256)
        if a.seal_pp:
            r = seal_pp(a.out, a.ret, a.manifest_sha256)
            if a.json:
                _write(a.json, json.dumps(r, ensure_ascii=False, indent=1, allow_nan=False) + "\n")
            print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
        if a.collect:
            uma = json.load(open(a.uma, encoding="utf-8")) if a.uma else None
            rec = collect(a.out, a.ret, a.manifest_sha256, uma, reg)
            for k, s in rec["samples"].items():
                print(f"  {k} W {s['W_J_m2']} · W_PBE {s['W_PBE_J_m2']} · ΔD3 {s['dD3_J_m2']} · D3 쌍 오차 {s['d3_pair_err_J_m2']}{' · ' + s['W_label'] if s['W_label'] else ''}")
            print(f"  G3 {rec['G3']['status']} · G4 {rec['G4']['status']}{' · G5 ' + rec['G5']['status'] if 'G5' in rec else ''} · 미완 {rec['jobs_not_ok']}")
            if a.json:
                _write(a.json, json.dumps(rec, ensure_ascii=False, indent=1, allow_nan=False) + "\n")
            return collect_exit(rec)
        if a.check:
            _, res = check(a.out, a.ret, a.manifest_sha256, reg)
            for n, r in res.items():
                print(f"  {n:34s} {r['status']}{(' · ' + str(r.get('why'))) if r.get('why') else ''}")
            print(f"  반송 묶음 MANIFEST: {return_manifest_info(a.ret, a.manifest_sha256)}")
            if a.json:
                _write(a.json, json.dumps(res, ensure_ascii=False, indent=1, allow_nan=False) + "\n")
            return check_exit(res)
    except PkgError as e:
        print(f"⛔ {e}")
        if a.json and not a.build:
            _write(a.json, json.dumps({"error": str(e), "exit": 2}, ensure_ascii=False) + "\n")
        return 2
    ap.error("--build · --check · --collect · --seal_pp · --selftest 중 하나")


if __name__ == "__main__":
    sys.exit(main())
