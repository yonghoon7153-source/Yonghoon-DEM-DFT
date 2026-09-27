#!/usr/bin/env python3
"""build_v5_vasp_package.py — A′ V5 (LPSCl|Ag(111) 작은 주기 계면) **VASP 외주 패키지** · 반송 검사 · W/G3/G4/G5 집계. (v5 · Codex CE·CF·CG·CI 반영)

왜 있나 (2026-09-27 · 1저자 "v5 관련해서 vasp 용으로 외주건으로 한번 만들어보고 codex 리뷰 받자 · 될지는 모르지만 준비는 해둬볼게")
  V5 는 우리 GPU 한 장(48 GB)에 안 들어가 RESOURCE_BLOCKED 였다 (QE CPU 추정 89–109 GB @70 Ry · 축소 변형도 61–80 GB).
  외주(큰 CPU 노드의 VASP)라면 들어간다. 이 도구는 **봉인된 S3v2 패키지를 입력으로 읽어** V5 18 잡을 VASP 로 옮긴다 —
  구조를 새로 만들지 않는다 (좌표는 S3v2 구조 파일 sha 로 결박 · 다르면 만들지 않는다).
왜 새 파일인가: QE 입력을 만든 `build_aprime_s3.py` 는 S3/S3v2 봉인에 파일 sha 로 결박돼 있다. 여기는 봉인 산출물만 읽는 번역기다.

v2 (Codex CE NO-GO 반영) — 성능 태그 제한 문법 · 시도 폴더 새로만 + attempt.json 결박 · 복수 실행 · 설정 되울림 · 전체 TITEL + 종별·조립본 sha
  · 버전 일치 · UMA 출처·유한성 · 외부 고정 MANIFEST 대조 · 결측=미검증 · 종료코드 · r1 자격 제한 · D3 두 층 (1 % 오설정 · 쌍 0.005 / G3 차이의 차이 0.001)
  · 3c 필드 · 3b′ 진단 · LF 고정 쓰기 (자세한 이력은 개정 3 문서)

v3 (Codex CF NO-GO 반영 · 2026-09-27)
  P0-1 **증거 먼저**: 있는 증거(POTCAR 기록 · OUTCAR TITEL · 버전 · 설정 되울림 · Edisp)가 기대값과 **모순**이면 rc·미종료·미수렴보다 먼저 막는다
       (모순 = 재시도 자격 없음 · `conflicts` 목록에 전부 적는다). 증거가 **없는** 것(일찍 죽어 OUTCAR 가 없음)은 모순이 아니다 — 정당한 r1 은 그대로.
       잡 사이 POTCAR·버전 일관성은 첫 시도·r1 **모든 시도**에서 모은다 (버려진 시도의 다른 PP 도 잡는다).
  P0-2 최종 집계(`--collect`)는 **봉인 PP 등록부 + 고정 sha 필수** (없으면 종료 2) · 파일럿 단계 집계는 `--pilot` 로만 (G5 = BLOCKED)
       · 등록부 **내용 검증** (schema · PBE_54 · 전 종 TITEL · 종별·조립본 sha · VASP 버전 줄 · 패키지 MANIFEST sha · 파일럿 두 잡 run_id) — 틀리면 시작 안 함
       · 검증한 등록부 sha 를 결과에 남긴다 · `usage_eligible` 에 등록부 검증 포함 · attempt.json 의 run_id·t_start·t_end 형식 필수
  P0-3 G4 변형은 표본 ① 과 **같은 기하**라 Edisp 가 같아야 한다 — 끝점마다 |ΔEdisp| ≤ 1e-4 eV (VASP 인쇄 5 자리) 가 아니면 그 변형 INCOMPLETE (D3 불일치)
  P1-1 에너지 = **마지막 레코드**의 토큰을 유한수로 해석 (NaN·Inf·별표·잘림이면 미검증 · 앞 값으로 돌아가지 않는다) · TOTEN·E(σ→0)·E(무엔트로피)는
       마지막 'FREE ENERGIE OF THE ION-ELECTRON SYSTEM' 구획 뒤의 레코드만 (VASP 는 SCF 단계 TOTEN 에 D3 를 안 넣고 최종 구획에만 넣는다 — 실물 확인)
  P1-2 Edisp 실물 형식 `Edisp (eV)  -28.80731` (VASP 5.4.4 · 콜론 없음) 지원 + **실물 OUTCAR 발췌 픽스처** (REAL_OUTCAR_544 · 저장소 원본과 줄 대조)
  P1-3 러너: 반송 압축·해시 실패 → **종료 4** · '✅ 끝' 금지 · 임시 파일 뒤 승격 · `PACK_ONLY=1` 로 계산 없이 포장만 재시도
  R2 해석값 출처: OUTCAR 의 **INCAR 에코 구획**(` INCAR:` ~ 첫 ` POTCAR:`)은 설정 판독에서 뺀다 · D3 매개변수(VDW_S6/S8/A1/A2/RADIUS/CNRADIUS)는
       DFTD3 구획의 해석값으로 대조 · DIPOL 은 (가) 해석값 줄 또는 (나) `direction 3 min pos` / NGZF 로 본 cut 위치 = (DIPOL_z + ½) mod 1 (±2 격자) —
       (나) 의 뜻은 실물로 확인했다 (VASP 5.4.4 SDCP C12 정적: INCAR DIPOL_z 0.4278 → min pos 520 / NGZF 560 = 0.9286 · 기대 0.9278). 둘 다 없으면 미검증.
  R4 G5 상태 순서: UMA 입력 BLOCKED → 등록부 BLOCKED → 분모 INCOMPLETE → G3/G4 비통과면 INCOMPLETE (원시 기준 결과를 문자열에 병기) → 원시 FAIL → PASS
  권고 반영: `total_w_citable`·`total_w_labels` 기계 필드 · 원자적 시도 폴더 생성(mkdir) · README 재실행 문구 (수동 재실행 = 새 승인 · 포장 재시도는 계산 없음)

v4 (Codex CG NO-GO 반영 · 2026-09-27)
  P1-1 러너 포장은 **허용 목록**으로만 — run/<잡>/{OUTCAR OSZICAR INCAR KPOINTS POSCAR IBZKPT POTCAR.titel POTCAR.sha256 POTCAR.species.sha256 attempt.json stdout.log}
       + run/status.tsv · run/env.txt · MANIFEST.sha256. 정상 실행 뒤의 삭제에 기대지 않는다 · 준비 실패·PACK_ONLY 도 같은 pack() · 묶음 구성원에
       POTCAR/WAVECAR/CHGCAR/CHG/vasprun.xml 이 있으면 보내지 않는다(종료 4) · 준비 실패 때 조립 중이던 POTCAR 도 지운다 ·
       검사기는 반송 폴더의 금지 파일을 `return_bundle.forbidden_files` 로 보고한다 (저장하지 말고 지우라고).
  P1-2 최종 검사·집계에서 **파일럿 두 잡의 채택 시도**(0 또는 정당한 r1)의 run_id 가 등록부 `from_pilot` 과 같아야 한다 · 같은 run_id 라도 attempt.json·OUTCAR sha 가
       봉인(`from_pilot_sha256` · 등록부 schema v3)과 다르면 막는다 → 상태 PILOT_NOT_SEALED (자동 교체 없음 · 재실행은 새 승인 대상).
  P1-3 미완료 시도(rc ≠ 0 · 미종료)의 OUTCAR TITEL 이 기대 목록의 **정상 접두**(같은 순서·같은 문자열로 앞부분만)이면 결측이지 모순이 아니다 (r1 자격 유지) ·
       다른 종·날짜·순서·추가 는 계속 모순(POTCAR_MISMATCH · r1 자격 없음) · 성공 시도의 접두만 은 미검증(POTCAR_UNVERIFIED · r1 자격 아님).
  권고 1 에너지·Edisp 는 '레코드 존재' 와 '값' 을 분리 — 값이 빈 마지막 레코드도 마지막 레코드다 (None → 미검증 · 앞 값 안 씀) · 값 패턴이 줄을 넘지 않는다.
  권고 2 반송 묶음·sha 둘 다 임시 파일로 완성한 뒤 승격 · sha 파일은 최종 이름으로 쓴다 (`sha256sum -c` 그대로 통과).
  권고 3 등록부에 봉인 당시 파일럿 attempt.json·OUTCAR sha 를 기록(`from_pilot_sha256`)하고 최종 검사에서 대조.

v5 (Codex CI NO-GO 반영 · 2026-09-27)
  P1   러너 `pack()` 이 목록 생성(find · 허용 필터 · sort · 목록 쓰기)·tar·구성원 열람(tar tzf)·금지 검사·구성원↔목록 대조·sha 의 **성공을 단계마다 확인**한다 —
       어느 하나라도 실패하면 1 을 돌려 러너는 **종료 4** · '✅' 없음 · 기존 tgz/sha 쌍 불변 (승격은 마지막 두 mv 뿐). 리뷰어 재현(BASH_ENV 로 find/sort 를 73 으로):
       v4 는 관리 파일 3 개만 담고 종료 0 이었다. grep 의 **정상 무매치(1)** 와 **오류(≥ 2)** 를 가른다 — 잡 파일이 하나도 없는 run/ 은 관리 파일만 포장해도 정상.
       tar tzf 열람 실패는 '금지 없음' 이 아니라 실패다. 묶음 구성원 집합 = 목록 집합이 아니면 실패 (tar 가 조용히 빠뜨리는 경우).
  S3   잘린 마지막 TITEL(앞 항목은 다 맞고 마지막 관측 문자열이 기대의 앞부분)은 새 상태 **TITEL_TRUNCATED** — 모순 확정이 아니라 **자동 확인 불가** · 통과·r1 자격 없음 ·
       원문 확인·새 승인으로만 해제 (POTCAR_MISMATCH 와 구분해 적는다).
  권고  개정 3 의 '도구는 기록만·게이트 아님' → 'cut 위치의 설정 일치 검사는 게이트 · 전자밀도 검증은 안 한다' 로 정리 · 결정 원장 제목·method_ref 의 v3/129 표기 정리 ·
       '어느 단계가 실패해도 옛 쌍 그대로' 는 '두 번째 mv 실패면 새 tgz + 옛 sha (종료 4 로 드러남)' 로 좁힘 · 발송은 종료 0 뒤 `sha256sum -c` 까지 통과한 쌍만.

종료코드 (CLI)
  --check   : 0 전 잡 OK · 3 OK 아닌 잡 있음 · 2 승인본(MANIFEST)·등록부·사용법 오류
  --collect : 2 승인본·등록부 없음/오류·사용법 · 3 OK 아닌 잡 있음(무결성) · 0 G5 PASS · 10 G5 FAIL · 11 G5 INCOMPLETE/BLOCKED · 12 UMA 없음(G5 미평가)
  --build · --seal_pp : 0 성공 · 2 실패
  run_all.sh : 0 전 잡 성공·포장 · 1 일부 잡 실패 (포장은 됨) · 2 패키지·성능 파일 오류 · 4 반송 포장 실패 (PACK_ONLY=1)

⛔ 이 도구가 못 하는 것
  · POTCAR 파일을 만들거나 내용을 검사하지 못한다 (VASP 라이선스 — 업체 보유분) · 반송된 TITEL/ZVAL 줄 · 종별·조립본 sha 만 본다.
  · **PBE_54 인지 내용 해시로 보증하지 못한다** (공개 기준 해시가 없다) — TITEL 날짜 · 업체 진술 · 파일럿 봉인 뒤 일관성만 본다.
    버전 줄 일치는 같은 버전/빌드 **표기**의 일치이지 바이너리 전체 동일성이 아니다.
  · 업체가 모든 산출물을 일관되게 위조하면 못 잡는다 — 목표는 실수(재사용·교체·오설정)를 잡는 것이다. run_id 도 위조 인증은 아니다.
  · VASP 값을 QE 값(V2·V4)과 한 표에서 빼거나 섞지 않는다 — 다른 비교군이다.
  · OUTCAR 문구는 버전마다 다를 수 있다 — 실물로 확인한 것은 VASP 5.4.4 한 건이다. 설정 되울림·Edisp·min pos 를 못 읽으면 **미검증**으로 막고,
    업체 버전 형식이 다르면 파일럿 원문으로 **파서만** 적응한다 (판정 규칙·문턱 불변 · 적응 내용은 기록).
  · 전자밀도·평균전위로 쌍극자 불연속을 확인하지 않는다 — 핵 여유 4 Å · DIPOL 식 · cut 위치(min pos)만 본다.
  · D3 예산(0.005 · 0.001 J/m²)은 **운영 예산**이지 통계적 신뢰구간이 아니다 · 예산 통과가 "기준 D3 대비 오차 0" 을 뜻하지 않는다.
  · UMA 에너지를 계산하지 않는다 (`relax_uma_d3.py --energies` JSON 을 받는다) · 결과를 보고 표본·문턱·분모를 바꾸지 않는다.
  · 업체 기계의 시간·peak 메모리를 보장하지 않는다 — README 추정은 평면파·밴드 수에서 낸 대략값이다.
  · 반송 묶음 허용 목록은 **파일 이름** 기준이다 — 허용 이름으로 바꿔 넣은 파일(예: POTCAR 본문을 stdout.log 로)은 못 거른다.
  · 봉인 파일럿 결속(run_id · attempt.json·OUTCAR sha)은 실수(다른 폴더 재실행 · 파일 교체)를 잡는 것이지 위조 방어가 아니다.

사용
  python3 tools/wad/build_v5_vasp_package.py --build --pkg db/inputs/wad_aprime_s3v2_2026_09_26 --out <패키지>
  python3 tools/wad/build_v5_vasp_package.py --check   --out <패키지> --manifest_sha256 <고정값> --ret <반송> [--pp_registry R --pp_registry_sha256 H] [--json J]
  python3 tools/wad/build_v5_vasp_package.py --seal_pp --out <패키지> --manifest_sha256 <고정값> --ret <파일럿 반송> --json pp_registry.json
  python3 tools/wad/build_v5_vasp_package.py --collect --out <패키지> --manifest_sha256 <고정값> --ret <반송> --uma uma.json --pp_registry R --pp_registry_sha256 H [--json J]
  python3 tools/wad/build_v5_vasp_package.py --collect --pilot --out … --ret …        # 파일럿 단계 (등록부 없이 · G5 BLOCKED)
  python3 tools/wad/build_v5_vasp_package.py --selftest
"""
import argparse
import gzip
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
D3_PAIR_BUDGET, D3_G3_BUDGET = 0.005, 0.001                         # J/m² — 운영 예산: G5 표본 문턱의 5 % · G3 문턱의 10 % (결과 전 제안 · 1저자 비준 대상)
D3_SAME_GEOM_TOL_EV = 1e-4                                          # 같은 기하(G4 변형 ↔ 표본 ①)의 Edisp 는 같아야 한다 — VASP 인쇄 5 자리
D3_PARAM_TOL, D3_RADIUS_TOL = 5e-4, 0.01                            # DFTD3 구획 인쇄 자릿수 (계수 4 자리 · 절단 Å 4 자리)
SIGMA_ECHO_TOL, DIPOL_ECHO_TOL = 0.005, 0.005                       # OUTCAR 되울림은 소수 2 · 4 자리로 찍힌다
DIPOL_CUT_GRID_TOL = 2                                              # min pos 로 본 cut 위치 허용 (NGZF 격자점)
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
REG_SCHEMA = "aprime_v5_pp_registry/v3"                              # v3 (CG): from_pilot_sha256 (봉인 당시 파일럿 attempt.json·OUTCAR sha) 필수
RETURN_ALLOWED = ("OUTCAR", "OSZICAR", "INCAR", "KPOINTS", "POSCAR", "IBZKPT", "POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256",
                  "attempt.json", "stdout.log")                     # run/<잡>/ 에서 반송 묶음에 담는 파일 (허용 목록 · CG P1-1) — 이 밖은 담지 않는다
RETURN_FORBIDDEN = ("POTCAR", "WAVECAR", "CHGCAR", "CHG", "vasprun.xml")   # 묶음에 있으면 안 되는 이름 — 러너는 보내지 않고(종료 4) 검사기는 보고한다
RUN_ID_RE = re.compile(r"^\d{8}T\d{6}-\d+-\d+$")                    # 러너 형식: UTC 시각 - PID - RANDOM
EV_J, A2_M2 = 1.602176634e-19, 1e-20
HB2M = 3.80998212                                                   # ħ²/2mₑ [eV·Å²]
HEX64 = re.compile(r"^[0-9a-f]{64}$")

# 실물 OUTCAR 발췌 (VASP 5.4.4 · 이 저장소의 우리 계산) — 파서 형식의 기준. selftest 가 원본 gz 와 줄 대조한다.
REAL_OUTCAR_544_SRC = "db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz"
REAL_OUTCAR_544_DIPOL_Z = 0.4278                                    # 같은 폴더 INCAR: DIPOL = 0.5 0.5 0.4278 · IVDW 11 · ENCUT 520
REAL_OUTCAR_544 = """ vasp.5.4.4.18Apr17-6-g9f103f2a35 (build Aug 19 2022 11:57:46) complex
 INCAR:
 POTCAR:    PAW_PBE Li_sv 10Sep2004
   TITEL  = PAW_PBE Li_sv 10Sep2004
 Dimension of arrays:
   number of dos      NEDOS =    301   number of ions     NIONS =    227
   dimension x,y,z NGXF=   280 NGYF=  180 NGZF=  560
   support grid    NGXF=   560 NGYF=  360 NGZF= 1120
 Startparameter for this run:
   ISPIN  =      2    spin polarized calculation?
   ENCUT  =  520.0 eV  38.22 Ry    6.18 a.u.  33.97 21.40 68.15*2*pi/ulx,y,z
   NELECT =    1596.0000    total number of electrons
   ISMEAR =     0;   SIGMA  =   0.05  broadening in eV -4-tet -1-fermi 0-gaus
   LDIPOL =      T    correct potential (dipole corrections)
   IDIPOL =      3    1-x, 2-y, 3-z, 4-all directions
 DIPCOR: dipole corrections for dipol
 direction  3 min pos   520,
  free energy    TOTEN  =     -1122.49048092 eV
------------------------ aborting loop because EDIFF is reached ----------------------------------------
         DFTD3 V3.0 Rev 1
 IVDW         = 11
 VDW_S6       =    1.0000
 VDW_S8       =    0.7220
 VDW_SR       =    1.2170
 VDW_RADIUS   =   50.2022 A
 VDW_CNRADIUS =   21.1671 A
 Edisp (eV)  -28.80731
  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)
  ---------------------------------------------------
  free  energy   TOTEN  =     -1151.29778848 eV
  energy  without entropy=    -1151.28677648  energy(sigma->0) =    -1151.29228248
 General timing and accounting informations for this job:
"""


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


def _tok_float(tok):
    """레코드의 수치 토큰 → 유한수 또는 None (NaN · Inf · 별표 · 잘림 · 빈 값)."""
    try:
        return fin(float(tok))
    except (TypeError, ValueError):
        return None


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
    """QE 톱니 불연속 구간 중심 → VASP DIPOL_z. VASP 보정의 불연속은 DIPOL ± ½ 에 놓인다 (CE Q3 확인 · 실물 min pos 확인) → 중심 − ½ (mod 1)."""
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
# run_all.sh (v5) — A′ V5 VASP 단일점 18 잡 · 잡마다 사전등록 재시도 INCAR.r1 최대 1 회 (최대 36 실행)
#   필수: VASP_CMD (예: "mpirun -np 128 vasp_std") · POTCAR_DIR (PAW_PBE 폴더: <POTCAR_DIR>/Li_sv/POTCAR · P · S · Cl · Ag)
#   선택: PERF_TAGS_FILE — 한 줄에 대입 하나만 · 허용 NCORE/NPAR/KPAR/NSIM (양의 정수) · LPLANE/LSCALU/LSCALAPACK (.TRUE./.FALSE.)
#         세미콜론·역슬래시·중복 태그·줄 끝 주석 금지 (VASP 는 ';' 뒤를 다른 설정으로 읽는다)
#         JOBS="잡1 잡2" (일부만 — 파일럿: JOBS="V5_s_outer_A_bound V5_s_outer_A_far")
#         PACK_ONLY=1 — 계산은 하지 않고 반송 묶음만 다시 만든다 (포장이 실패했을 때 · VASP_CMD·POTCAR_DIR 불필요)
#   ⛔ INCAR·POSCAR·KPOINTS 를 고치지 마세요 · ⛔ POTCAR 는 반송하지 않습니다 (TITEL/ZVAL 줄 · sha256 만) —
#      반송 묶음은 **허용 목록**(RET_ALLOW)의 파일만 담습니다. 준비 실패·중단·PACK_ONLY 에서도 POTCAR 본문·WAVECAR·CHGCAR 는 들어가지 않고,
#      혹시 들어가면 묶음을 만들지 않습니다 (종료 4).
#   ⛔ 시도 폴더(run/<잡>, run/<잡>_r1)가 이미 있으면 그 잡은 돌지 않습니다 (원자적 mkdir). 재시도 상한은 잡마다 사전등록 1 회 —
#      그 밖의 수동 재실행은 새 승인 없이는 하지 않습니다. 파일럿 두 잡은 봉인한 그 실행 그대로 최종 반송에 포함합니다 (다시 돌리지 않습니다).
#   종료코드: 0 전 잡 성공·포장 · 1 일부 잡 실패 (반송 묶음은 만든다 — 실패도 기록) · 2 패키지·성능 파일 오류 (아무것도 안 돈다)
#             4 반송 포장 실패 — 목록 생성·tar·구성원 열람·검사·sha 어느 단계든 (계산 결과는 run/ 에 그대로 · 기존 묶음 쌍도 그대로 — PACK_ONLY=1 로 포장만 다시)
#   ⛔ 보낼 것은 종료 0 뒤 `sha256sum -c V5_vasp_return.tgz.sha256` 까지 통과한 쌍만입니다.
# =============================================================================
set -u
HERE=$(cd "$(dirname "$0")" && pwd); cd "$HERE"
sha256sum -c --quiet MANIFEST.sha256 || { echo "⛔ 패키지 파일이 MANIFEST 와 다르다 — 실행하지 않는다"; exit 2; }
RET_ALLOW='@RET_ALLOW@'    # run/<잡>/ 아래에서 반송하는 파일 이름 (이 밖은 담지 않는다)
RET_FORBID='@RET_FORBID@'  # 묶음 구성원에 있으면 안 되는 이름 (POTCAR 본문 등) — 있으면 보내지 않는다
pack_fail(){ echo "⛔ 포장: $1"; rm -f V5_vasp_return.tgz.part V5_vasp_return.tgz.sha256.part; return 1; }   # 임시 묶음은 지운다 · 기존 tgz/sha 쌍과 진단용 V5_vasp_return.tmp/ 는 남긴다
pack(){  # 허용 목록으로 구성원을 모아 임시 파일에 쓰고, **단계마다 성공을 확인**한 뒤에야 둘 다 승격 (CI P1). 실패 = 1 · 기존 tgz/sha 쌍은 건드리지 않는다 (승격은 마지막 두 mv 뿐)
  local T=V5_vasp_return.tmp g h
  rm -rf "$T" V5_vasp_return.tgz.part V5_vasp_return.tgz.sha256.part V5_vasp_return.list; mkdir "$T" || return 1
  find run -mindepth 2 -maxdepth 2 -type f > "$T/found" || { pack_fail "run/ 열거 실패"; return 1; }
  grep -E "^run/[^/]+/($RET_ALLOW)$" "$T/found" > "$T/allowed"; g=$?
  [ "$g" -le 1 ] || { pack_fail "허용 목록 필터 오류 ($g)"; return 1; }     # 1 = 잡 파일이 하나도 없음 (정상 · 관리 파일만 포장) · 2 이상 = 오류
  LC_ALL=C sort "$T/allowed" > "$T/sorted" || { pack_fail "정렬 실패"; return 1; }
  : > "$T/mgmt"; for f in run/env.txt run/status.tsv; do [ -f "$f" ] && echo "$f" >> "$T/mgmt"; done
  { echo MANIFEST.sha256; cat "$T/mgmt" "$T/sorted"; } > V5_vasp_return.list || { pack_fail "목록 쓰기 실패"; return 1; }
  tar czf V5_vasp_return.tgz.part -T V5_vasp_return.list || { pack_fail "tar 실패"; return 1; }
  tar tzf V5_vasp_return.tgz.part > "$T/members" || { pack_fail "묶음 구성원 열람 실패 — 검사할 수 없으면 보내지 않는다"; return 1; }
  grep -E "(^|/)($RET_FORBID)$" "$T/members" > "$T/forbidden"; g=$?
  if [ "$g" -eq 0 ]; then pack_fail "반송 묶음에 금지 파일(POTCAR 본문 등)이 들어갔다 — 보내지 않는다: $(tr '\n' ' ' < "$T/forbidden")"; return 1
  elif [ "$g" -ne 1 ]; then pack_fail "구성원 검사 오류 ($g)"; return 1; fi
  LC_ALL=C sort "$T/members" > "$T/members.sorted" && LC_ALL=C sort V5_vasp_return.list > "$T/list.sorted" || { pack_fail "구성원 대조 준비 실패"; return 1; }
  cmp -s "$T/members.sorted" "$T/list.sorted" || { pack_fail "묶음 구성원이 목록과 다르다 — 보내지 않는다"; return 1; }
  h=$(sha256sum V5_vasp_return.tgz.part | cut -d' ' -f1); [ "${#h}" -eq 64 ] || { pack_fail "sha256 실패"; return 1; }
  printf '%s  V5_vasp_return.tgz\n' "$h" > V5_vasp_return.tgz.sha256.part || { pack_fail "sha 쓰기 실패"; return 1; }
  mv -f V5_vasp_return.tgz.part V5_vasp_return.tgz && mv -f V5_vasp_return.tgz.sha256.part V5_vasp_return.tgz.sha256 || { pack_fail "승격(mv) 실패 — 새 tgz + 옛 sha 가 남을 수 있다 · sha256sum -c 로 확인"; return 1; }
  rm -rf "$T"
}
if [ "${PACK_ONLY:-0}" = 1 ]; then
  [ -d run ] || { echo "⛔ run/ 이 없다 — 포장할 것이 없다"; exit 2; }
  echo "pack_only $(date -u +%FT%TZ)" >> run/env.txt
  if pack; then echo "✅ 포장만 다시 했다 — V5_vasp_return.tgz 와 .sha256 을 보내 주세요 (계산은 다시 돌리지 않았다)"; exit 0; fi
  echo "⛔ 포장 실패 — 디스크·권한을 확인한 뒤 PACK_ONLY=1 로 다시"; exit 4
fi
: "${VASP_CMD:?VASP_CMD 를 주세요 (예: mpirun -np 128 vasp_std)}"
: "${POTCAR_DIR:?POTCAR_DIR 를 주세요 (PAW_PBE 폴더)}"
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
  mkdir "$d" 2>/dev/null || { echo "⛔ $d 가 이미 있거나 만들 수 없다 — 덮어쓰지 않는다"; return 3; }
  { cp "jobs/$job/POSCAR" "jobs/$job/KPOINTS" "$d/" && cp "jobs/$job/$inc" "$d/INCAR"; } || return 3
  [ -n "$PERF_LINES" ] && printf '%s' "$PERF_LINES" >> "$d/INCAR"
  : > "$d/POTCAR"; : > "$d/POTCAR.species.sha256"
  while read -r p; do
    [ -n "$p" ] || continue
    [ -f "$POTCAR_DIR/$p/POTCAR" ] || { echo "⛔ POTCAR $p 없음"; rm -f "$d/POTCAR"; return 3; }   # 조립 중이던 부분 본문도 지운다
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
if ! pack; then echo "⛔ 반송 포장 실패 — 계산 결과는 run/ 에 그대로 있다. 다시 돌리지 말고 PACK_ONLY=1 bash run_all.sh 로 포장만 다시"; exit 4; fi
if [ "$fail" = 0 ]; then echo "✅ 끝 — V5_vasp_return.tgz 와 .sha256 을 보내 주세요"; else echo "⚠ 일부 잡 실패 — 그대로 반송해 주세요 (실패도 기록입니다)"; fi
exit "$fail"
'''


def run_all_text():
    """배포 run_all.sh 본문 — 허용/금지 파일 목록을 파이썬 상수에서 채운다 (검사기와 같은 목록)."""
    return RUN_ALL.replace("@RET_ALLOW@", "|".join(re.escape(x) for x in RETURN_ALLOWED)).replace("@RET_FORBID@", "|".join(re.escape(x) for x in RETURN_FORBIDDEN))


def _readme(jobs, est, pkg_sha):
    rows = "\n".join(f"| `{j['dir']}` | {j['role']} | {j['nions']} | {j['nelect_expected']:.0f} | {'×'.join(f'{x:.3f}' for x in j['cell_A'])} | "
                     f"{j['encut']:.0f} | {'×'.join(map(str, j['kpts']))} | {j['sigma']:.3f} |" for j in jobs)
    pp = " · ".join(f"{POTCAR_MAP[s]} (`{PP_EXPECTED_TITEL[s]}`)" for s in SPECIES_ORDER)
    return f"""# A′ V5 — VASP 단일점 외주 패키지 v5 (LPSCl | Ag(111) 작은 주기 계면)

> 상태: **준비본 (실행 미정)** · Codex CE·CF·CG·CI NO-GO 반영판 · 재리뷰 전 · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` **proposed**
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
   최종 반송에는 파일럿 두 잡의 폴더가 **봉인한 그 실행 그대로**(run_id · attempt.json · OUTCAR) 들어 있어야 합니다 — 다른 폴더에서 다시 돌린 파일럿이 오면
   최종 집계가 그 잡을 막습니다 (재실행은 새 승인). 파일럿 뒤에 VASP 입력이 바뀌어야 하면 새 패키지 버전이 나가고, 파일럿은 구판 진단으로만 남습니다.
3. 성능 태그는 `PERF_TAGS_FILE=perf.txt` 로만 — **한 줄에 대입 하나**, 허용: NCORE NPAR KPAR NSIM (양의 정수) · LPLANE LSCALU LSCALAPACK (.TRUE./.FALSE.).
   세미콜론(;) · 역슬래시(\\) · 같은 태그 두 번 · 줄 끝 주석은 거부됩니다. **INCAR·POSCAR·KPOINTS 는 고치지 마세요.**
4. 시도 폴더 `run/<잡>` 이 이미 있으면 러너가 그 잡을 **돌리지 않습니다** (지난 출력 재사용 방지). 재시도 상한은 잡마다 사전등록 1 회이고,
   **그 밖의 수동 재실행은 새 승인 없이는 하지 않습니다** — 필요해 보이면 먼저 연락 주세요.
5. 한 잡이 실행 실패·미종료·미수렴이면 러너가 미리 정한 재시도(INCAR.r1 · AMIX 0.1 · BMIX 0.01 · NELM 300)를 **한 번만** 합니다.
   그래도 안 되면 그 잡은 비워 둡니다 — 다른 설정으로 더 돌리지 마세요. 실행 상한 = 18 × 2 = **36 회** (파일럿 재사용 시).
6. 반송 묶음은 러너가 **허용 목록**(아래 '돌려받을 것')의 파일만 담습니다 — POTCAR 본문 · WAVECAR · CHGCAR 는 준비 실패·중단·`PACK_ONLY` 에서도
   들어가지 않고, 혹시 들어가면 묶음을 만들지 않습니다 (종료코드 4). 포장의 어느 단계(목록 생성 · tar · 구성원 열람·검사 · sha256)가 실패해도 **종료코드 4** 이고,
   계산 결과는 `run/` 에, 이미 있던 묶음 쌍은 그대로 남습니다. 계산을 다시 돌리지 말고 `PACK_ONLY=1 bash run_all.sh` 로 **포장만** 다시 해 주세요.
   보내는 것은 종료코드 0 뒤 `sha256sum -c V5_vasp_return.tgz.sha256` 까지 통과한 쌍만입니다.
   러너 종료코드: 0 전 잡 성공 · 1 일부 잡 실패 (묶음은 만듦 — 실패도 반송) · 2 패키지·성능 파일 오류 (아무것도 안 돎) · 4 포장 실패.

## VASP 버전 · POTCAR — 이 조합으로 고정
- **VASP**: 파일럿과 본 배치가 **같은 빌드**여야 합니다 (OUTCAR 첫 줄로 확인 · 다르면 그 배치는 쓰지 않습니다). 버전·빌드를 `run/env.txt` 에 적어 주세요.
  INCAR 의 VDW_S6 는 문서상 VASP 6.6.0 부터 사용자 조정이 되지만, 값 1.0 은 PBE 기본값과 같습니다 (구버전이어도 같은 값).
- **POTCAR** {PP_SET}: {pp}.
  파일럿에서 TITEL(날짜 포함)·종별·조립본 sha256 을 확인해 **등록부로 봉인**하고, 이후 모든 잡이 그 등록부와 같아야 합니다. 다른 PP 트리로 바꾸지 마세요.
  POTCAR 파일은 **보내지 마세요** — 러너가 TITEL/ZVAL/LEXCH 줄 · 종별 sha256 · 조립본 sha256 만 남깁니다.

## 돌려받을 것
`V5_vasp_return.tgz` + `.sha256` (러너가 만듭니다 — 허용 목록만): 시도마다 {' · '.join(RETURN_ALLOWED)} (있는 것만)
· `run/status.tsv` · `run/env.txt` · `MANIFEST.sha256`. 이 밖의 파일({' · '.join(RETURN_FORBIDDEN)} · EIGENVAL · DOSCAR 등)은 묶음에 넣지 않습니다.
VASP 버전·빌드·컴파일러·노드/코어 수·**잡별 peak RSS·벽시계** 를 `run/env.txt` 에 한 줄씩 덧붙여 주세요.
실패한 잡도 폴더째 보내 주세요 (실패도 기록입니다). 묶음은 러너로만 만들어 주세요 (손으로 tar 하면 POTCAR 본문이 섞일 수 있습니다).

## 규모 (대략 · 우리 추정 — 견적은 파일럿 벽시계·peak RSS 로)
NIONS 176–200 · NELECT {est['nel_min']:.0f}–{est['nel_max']:.0f} · 기본 NBANDS ~{est['nb_max']} · 평면파 최대 ~{est['npw_520']:,}/k (ENCUT 520) · ~{est['npw_650']:,}/k (ENCUT 650 · G4 변형 2 잡)
· 파동함수 몫만 ~{est['wfc_max']} GB (k 합 · **peak RSS 아님** — FFT·투영자·작업 배열·MPI 복제는 따로) · 환원 k 추정 Γ3×2×1 ≈ 4 · Γ4×3×1 ≈ 7 (IBZKPT 로 확인).
비스핀 · 금속(Ag) 슬랩 · 진공 포함 · LREAL=F · 실행 최대 36 회. KPAR 는 실제 k 수·메모리·노드 배치에 맞춰 업체가 고릅니다.

## English summary
18 single-point PBE+D3(BJ) SCF runs (no relaxation) on fixed geometries. PAW_PBE {PP_SET} Li_sv/P/S/Cl/Ag (TITELs above; sealed after the pilot);
the pilot and the main batch must use the same VASP build. ENCUT 520 eV (650 eV for two G4 jobs); ISMEAR 1, SIGMA 0.136 eV; IVDW 12 with explicit
PBE-BJ parameters and explicit VDW_RADIUS/VDW_CNRADIUS; dipole correction along z (LDIPOL, IDIPOL 3, DIPOL given). Run the two pilot jobs first and
return them. Do not edit INCAR/POSCAR/KPOINTS (performance tags only via PERF_TAGS_FILE, one assignment per line, no ';'); existing attempt folders
are never overwritten; one pre-registered retry per job (max 36 runs) and no other manual reruns without approval; if packaging fails (exit 4)
rerun with PACK_ONLY=1 to repackage only. The runner packs only an allow-list of files ({', '.join(RETURN_ALLOWED)}, status.tsv, env.txt,
MANIFEST.sha256) — POTCAR bodies, WAVECAR and CHGCAR are never included (exit 4 if they would be); please do not tar by hand. The two pilot job folders
must be returned unchanged in the final bundle (same run_id / attempt.json / OUTCAR as sealed); a re-run pilot is rejected at collection. Do not send
POTCAR files. Please report VASP version/build and per-job peak RSS and wall time.
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
    _write(os.path.join(out, "run_all.sh"), run_all_text()); os.chmod(os.path.join(out, "run_all.sh"), 0o755)
    _write(os.path.join(out, "JOBS.txt"), "\n".join(x["dir"] for x in jobs) + "\n")
    meta = {"schema": "aprime_v5_vasp_package/v5", "date": "2026-09-27", "status": "준비본 v5 (Codex CE·CF·CG·CI NO-GO 반영 · 재리뷰 전 · 결정 proposed · 실행 미정)",
            "source_package": pkg, "source_s3_manifest_sha256": qe["s3_manifest_sha256"], "source_seal": "db/properties/wad_aprime_s3v2_seal_2026_09_26.json",
            "card": "db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json", "amendment": "db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json",
            "tool_sha256": _sha(os.path.abspath(__file__)),
            "settings": {"potcar": POTCAR_MAP, "pp_set": PP_SET, "pp_expected_titel": PP_EXPECTED_TITEL, "zval": ZVAL, "encut": ENCUT_BASE, "encut_g4e": ENCUT_G4E,
                         "sigma": SIGMA_BASE, "d3": D3_PARAMS, "d3_cutoffs_A": {"VDW_RADIUS": VDW_RADIUS_A, "VDW_CNRADIUS": VDW_CNRADIUS_A},
                         "d3_ref": "simple-dftd3 2체 · VASP 절단에 맞춤", "perf_tags_int": PERF_INT, "perf_tags_bool": PERF_BOOL, "rescue": RESCUE,
                         "r1_eligible": R1_ELIGIBLE, "d3_gross_rel_tol": D3_REL_TOL, "d3_pair_budget_J_m2": D3_PAIR_BUDGET, "d3_g3_budget_J_m2": D3_G3_BUDGET,
                         "d3_same_geom_tol_eV": D3_SAME_GEOM_TOL_EV, "dipol_cut_grid_tol": DIPOL_CUT_GRID_TOL, "uma_required": UMA_REQ, "pilot_jobs": PILOT_JOBS,
                         "pp_registry_schema": REG_SCHEMA, "return_allowed": RETURN_ALLOWED, "return_forbidden": RETURN_FORBIDDEN},
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


# ───────────────────────── 승인본 대조 (CE P1-1) ─────────────────────────
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
    """반송 묶음에 들어 있는 MANIFEST.sha256 (러너가 실행 때 쓴 것) 이 고정값과 같은가 — 정보 (입력 대조가 이미 결박한다).
    + 반송 폴더에 금지 파일(POTCAR 본문 · WAVECAR · CHGCAR · CHG · vasprun.xml)이 있으면 목록으로 보고한다 (CG P1-1 · 판정 아님 — 저장하지 말고 지우라는 신호)."""
    p = os.path.join(ret, "MANIFEST.sha256")
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    forb = sorted(os.path.relpath(os.path.join(r_, f), ret).replace(os.sep, "/") for r_, _, fs in os.walk(run) for f in fs if f in RETURN_FORBIDDEN) if os.path.isdir(run) else []
    return {"present": os.path.isfile(p), "matches_pinned": (_sha(p) == str(pinned).lower()) if os.path.isfile(p) else None, "forbidden_files": forb}


# ───────────────────────── OUTCAR 판독 ─────────────────────────
_HEADER = re.compile(r"^\s*(vasp\.\d.*)$", re.M)
_FINAL_HDR = re.compile(r"FREE ENERGIE OF THE ION-ELECTRON SYSTEM")


def _last(pat, text, flags=re.M):
    m = re.findall(pat, text, flags)
    return m[-1] if m else None


def _last_rec(pat, text):
    """패턴의 **마지막 레코드** → (토큰, 위치) · 없으면 (None, None)."""
    m = None
    for m in re.finditer(pat, text, re.M):
        pass
    return (m.group(1), m.start()) if m else (None, None)


def _strip_incar_echo(text):
    """` INCAR:` 줄 다음부터 첫 ` POTCAR:` 줄 전까지(= 입력 에코)를 뺀다 — 설정은 VASP 가 해석해 찍은 구획에서만 읽는다. 반환 (본문, 뺀 줄 수)."""
    out, skip, n = [], False, 0
    for ln in text.splitlines(keepends=True):
        if not skip and re.match(r"^\s*INCAR:\s*$", ln):
            skip = True; out.append(ln); continue
        if skip:
            if re.match(r"^\s*POTCAR:", ln):
                skip = False; out.append(ln)
            else:
                n += 1
            continue
        out.append(ln)
    return "".join(out), n


def parse_outcar(text):
    body, n_echo = _strip_incar_echo(text)
    heads = _HEADER.findall(body)
    r = {"n_runs": len(heads), "version": " ".join(heads[0].split()) if heads else None,
         "terminated": "General timing and accounting" in body,
         "converged": ("aborting loop because EDIFF is reached" in body) and ("EDIFF was not reached" not in body),
         "incar_echo_lines_excluded": n_echo}
    fh = [m.start() for m in _FINAL_HDR.finditer(body)]
    fpos = fh[-1] if fh else None
    def final_energy(pat):
        tok, pos = _last_rec(pat, body)
        if fpos is None or tok is None or pos < fpos:        # 마지막 레코드가 최종 구획 뒤가 아니면 (SCF 단계 값 · D3 빠짐) 쓰지 않는다
            return None
        return _tok_float(tok)
    # 레코드 = 머리말('TOTEN =' 등) · 값 = 같은 줄의 다음 토큰 (없으면 빈 값 → None). 값 패턴이 줄을 넘지 않는다 — 값이 빈 마지막 레코드도 마지막 레코드다 (CG 권고 1).
    r["TOTEN_eV"] = final_energy(r"free[ \t]+energy[ \t]+TOTEN[ \t]*=[ \t]*(\S*)")
    r["E_sigma0_eV"] = final_energy(r"energy\(sigma->0\)[ \t]*=[ \t]*(\S*)")
    r["E_noentropy_eV"] = final_energy(r"energy[ \t]+without[ \t]+entropy[ \t]*=[ \t]*(\S*)")
    tok, _ = _last_rec(r"Edisp[ \t]*(?:\(eV\))?[ \t]*[:=]?[ \t]*(\S*)", body)
    r["Edisp_eV"] = _tok_float(tok)
    num = lambda pat: _tok_float(_last(pat, body))
    s = {}
    v = _last(r"NIONS\s*=\s*(\d+)", body); s["NIONS"] = int(v) if v else None
    s["NELECT"] = num(r"NELECT\s*=\s*(\S+)")
    s["ENCUT"] = num(r"^\s*ENCUT\s*=\s*(\S+)\s*eV")
    v = re.findall(r"ISMEAR\s*=\s*(-?\d+)\s*;\s*SIGMA\s*=\s*(\S+)", body)
    s["ISMEAR"], s["SIGMA"] = (int(v[-1][0]), _tok_float(v[-1][1])) if v else (None, None)
    v = _last(r"^\s*ISPIN\s*=\s*(\d+)", body); s["ISPIN"] = int(v) if v else None
    v = _last(r"^\s*IVDW\s*=\s*(\d+)", body); s["IVDW"] = int(v) if v else None
    v = _last(r"^\s*LDIPOL\s*=\s*(\S+)", body); s["LDIPOL"] = (v.strip(".").upper()[:1] if v else None)
    v = _last(r"^\s*IDIPOL\s*=\s*(\d+)", body); s["IDIPOL"] = int(v) if v else None
    v = re.findall(r"^\s*DIPOL\s*=\s*(\S+)\s+(\S+)\s+(\S+)", body, re.M); s["DIPOL_z"] = _tok_float(v[-1][2]) if v else None
    s["EFIELD"] = num(r"^\s*EFIELD\s*=\s*(\S+)")
    for k in ("VDW_S6", "VDW_S8", "VDW_A1", "VDW_A2", "VDW_RADIUS", "VDW_CNRADIUS"):
        s[k] = num(rf"^\s*{k}\s*=\s*(\S+)")
    r["settings"] = s
    r["outcar_titel"] = list(dict.fromkeys(" ".join(x.split()) for x in re.findall(r"TITEL\s*=\s*(.+)", body)))
    v = _last(r"dimension x,y,z NGXF=\s*\d+\s+NGYF=\s*\d+\s+NGZF=\s*(\d+)", body); r["NGZF"] = int(v) if v else None
    v = _last(r"direction\s+3\s+min\s+pos\s+(\d+)", body); r["dipole_min_pos"] = int(v) if v else None
    return r


def parse_titel(text):
    return [" ".join(x.split()) for x in re.findall(r"TITEL\s*=\s*(.+)", text)], [float(x) for x in re.findall(r"ZVAL\s*=\s*(-?\d+\.?\d*)", text)]


def dipol_evidence(o, dz):
    """DIPOL 해석값 증거 → (근거 목록, 모순 목록). (가) 해석값 DIPOL 줄 · (나) min pos / NGZF 로 본 cut 위치 = (DIPOL_z + ½) mod 1."""
    got, bad = [], []
    v = (o.get("settings") or {}).get("DIPOL_z")
    if v is not None:
        d = abs(v - dz) % 1.0
        (got if min(d, 1 - d) <= DIPOL_ECHO_TOL + 1e-9 else bad).append(f"DIPOL 줄 {v}" if min(d, 1 - d) <= DIPOL_ECHO_TOL + 1e-9 else f"DIPOL_z {v} ≠ {dz}")
    mp, ng = o.get("dipole_min_pos"), o.get("NGZF")
    if mp is not None and ng:
        cut, want = mp / ng, (dz + 0.5) % 1.0
        d = abs(cut - want) % 1.0; d = min(d, 1 - d)
        if d <= DIPOL_CUT_GRID_TOL / ng + 1e-12:
            got.append(f"min pos cut {mp}/{ng}")
        else:
            bad.append(f"쌍극자 cut {mp}/{ng} = {cut:.4f} ≠ DIPOL_z+½ = {want:.4f}")
    return got, bad


def audit_settings(o, job):
    """OUTCAR 해석값(입력 에코 제외) 대조 → (없는 키, 모순 목록, 근거)."""
    s = o["settings"]
    exp = {"NIONS": job["nions"], "NELECT": job["nelect_expected"], "ENCUT": job["encut"], "ISMEAR": 1, "SIGMA": job["sigma"], "ISPIN": 1,
           "IVDW": 12, "LDIPOL": "T", "IDIPOL": 3, "VDW_S6": D3_PARAMS["s6"], "VDW_S8": D3_PARAMS["s8"], "VDW_A1": D3_PARAMS["a1"],
           "VDW_A2": D3_PARAMS["a2"], "VDW_RADIUS": VDW_RADIUS_A, "VDW_CNRADIUS": VDW_CNRADIUS_A}
    missing, bad = [], []
    for k, e in exp.items():
        v = s.get(k)
        if v is None:
            missing.append(k); continue
        if k == "SIGMA":
            ok = abs(v - e) <= SIGMA_ECHO_TOL + 1e-9
        elif k in ("ENCUT", "NELECT"):
            ok = abs(v - e) <= 0.05
        elif k in ("VDW_S6", "VDW_S8", "VDW_A1", "VDW_A2"):
            ok = abs(v - e) <= D3_PARAM_TOL + 1e-12
        elif k in ("VDW_RADIUS", "VDW_CNRADIUS"):
            ok = abs(v - e) <= D3_RADIUS_TOL + 1e-12
        else:
            ok = v == e
        if not ok:
            bad.append(f"{k} {v} ≠ {e}")
    got, dbad = dipol_evidence(o, job["dipol_z"])
    bad += dbad
    if not got and not dbad:
        missing.append("DIPOL")
    if s.get("EFIELD") is not None and abs(s["EFIELD"]) > 1e-12:
        bad.append(f"EFIELD {s['EFIELD']} (외부장 금지)")
    return missing, bad, {"DIPOL": got}


def _spec_key(job):
    return ",".join(job["potcar_spec"])


# ───────────────────────── 반송 검사 ─────────────────────────
def check_job(job, pkgdir, attdir, attempt="0", pp_registry=None):
    """한 시도 폴더 → 상태 dict. OK 가 아니면 값은 판정에 안 쓴다.
    순서 (CF P0-1): 실행 기록 결박 → 입력 무결성 → 복수 실행 → **있는 증거의 모순** (POTCAR · TITEL · 버전 · 설정 · D3 — 재시도 자격 없음)
      → 실행 상태 (rc · 미종료 · 미수렴 — 재시도 자격) → 완결성 (성공한 실행만: 결측 = 미검증)."""
    r = {"dir": os.path.basename(attdir), "attempt": attempt}
    def done(status, why=None, **kw):
        r["status"] = status
        if why:
            r["why"] = why
        r.update(kw)
        return r
    if not os.path.isdir(attdir):
        return done("MISSING", missing=["(폴더)"])
    miss = [f for f in ("INCAR", "KPOINTS", "POSCAR", "attempt.json") if not os.path.isfile(os.path.join(attdir, f))]
    if miss:
        return done("MISSING", missing=miss)
    try:
        a = json.load(open(os.path.join(attdir, "attempt.json"), encoding="utf-8"))
    except Exception as e:
        return done("ATTEMPT_MISMATCH", f"attempt.json 읽기 실패 {e}")
    if not isinstance(a, dict) or a.get("job") != job["dir"] or str(a.get("attempt")) != str(attempt) or not isinstance(a.get("sha256"), dict):
        return done("ATTEMPT_MISMATCH", "attempt.json 의 잡·시도·sha 형식")
    rid, t0, t1, rc = a.get("run_id"), a.get("t_start"), a.get("t_end"), a.get("rc")
    isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
    if not (isinstance(rid, str) and RUN_ID_RE.match(rid)) or not (isint(t0) and isint(t1) and t1 >= t0) or not isint(rc):
        return done("ATTEMPT_MISMATCH", f"실행 기록 형식 (run_id {rid!r} · t {t0!r}→{t1!r} · rc {rc!r})")
    for f in ("INCAR", "POSCAR", "KPOINTS", "OUTCAR", "OSZICAR"):
        p = os.path.join(attdir, f)
        if (a["sha256"].get(f) or "") != (_sha(p) if os.path.isfile(p) else ""):
            return done("ATTEMPT_MISMATCH", f"{f} 가 실행 기록(attempt.json)과 다르다 — 실행 뒤 바뀌었거나 생겼거나 없어진 파일")
    r["run_id"], r["rc"] = rid, rc
    r["attempt_json_sha256"], r["outcar_sha256"] = _sha(os.path.join(attdir, "attempt.json")), str(a["sha256"].get("OUTCAR") or "")   # 파일럿 봉인 결속용 (CG P1-2 · 권고 3)
    for f in ("POSCAR", "KPOINTS"):
        if _sha(os.path.join(attdir, f)) != job["files_sha256"][f]:
            return done("INPUT_MODIFIED", f)
    ours, e0 = parse_incar_strict(open(os.path.join(pkgdir, "jobs", job["dir"], "INCAR.r1" if attempt == "r1" else "INCAR"), encoding="utf-8").read())
    ran, e1 = parse_incar_strict(open(os.path.join(attdir, "INCAR"), encoding="utf-8", errors="replace").read())
    extra = {k: v for k, v in ran.items() if k not in ours}
    badperf = [k for k, v in extra.items() if k not in PERF_TAGS or not perf_value_ok(k, v)]
    diff = [k for k in ours if ran.get(k) != ours[k]]
    if e0 or e1 or badperf or diff:
        return done("INPUT_MODIFIED", f"INCAR 문법 {e1[:3]} · 다른 태그 {diff} · 허용 밖·형식 이상 추가 {badperf}")
    op = os.path.join(attdir, "OUTCAR")
    o = parse_outcar(open(op, encoding="utf-8", errors="replace").read()) if os.path.isfile(op) else None
    if o:
        r.update({k: v for k, v in o.items() if k != "settings"}); r["settings"] = o["settings"]
        if o["n_runs"] > 1:
            return done("MULTIPLE_RUNS", f"OUTCAR 실행 머리줄 {o['n_runs']} 개 (정적 단일점은 1 개)")
    # ── ① 있는 증거의 모순 — 재시도 자격 없음 ──
    tp, sp_, spp = (os.path.join(attdir, f) for f in ("POTCAR.titel", "POTCAR.sha256", "POTCAR.species.sha256"))
    if not all(os.path.isfile(x) for x in (tp, sp_, spp)):
        return done("POTCAR_UNVERIFIED", "POTCAR 기록 (titel · sha256 · species.sha256) 결측 — 러너가 실행 전에 쓰는 파일이다")
    psha = open(sp_, encoding="utf-8").read().strip().lower()
    sps = [l.split() for l in open(spp, encoding="utf-8").read().splitlines() if l.strip()]
    if not HEX64.match(psha) or psha != str(a["sha256"].get("POTCAR", "")).lower() or len(sps) != len(job["potcar_spec"]) \
            or any(len(x) != 2 or not HEX64.match(x[1].lower()) for x in sps) or [x[0] for x in sps] != job["potcar_spec"]:
        return done("POTCAR_UNVERIFIED", "POTCAR sha 형식·순서·실행 기록 불일치")
    r["potcar_species_sha256"] = {x[0]: x[1].lower() for x in sps}; r["potcar_sha256"] = psha
    conflicts = []
    titel, zv = parse_titel(open(tp, encoding="utf-8", errors="replace").read())
    exp_t = [pp_registry["titel"][p] for p in job["potcar_spec"]] if pp_registry else job["pp_expected_titel"]
    if titel != exp_t or [round(x, 3) for x in zv] != [round(x, 3) for x in job["zval_expected"]]:
        conflicts.append(("POTCAR_MISMATCH", f"POTCAR.titel TITEL {titel} · ZVAL {zv} (기대 {exp_t})"))
    # OUTCAR TITEL (CG P1-3): 기대 목록의 **정상 접두**(같은 순서·같은 문자열로 앞부분만)는 잘린 출력의 결측이지 모순이 아니다 — 성공 시도면 아래 ③ 에서 미검증으로 막힌다.
    # 접두가 아닌 것(다른 종·날짜·순서 · 기대 뒤에 추가)은 모순이다.
    ot = o["outcar_titel"] if o else []
    titel_prefix_only = bool(ot) and ot != titel and len(ot) < len(titel) and titel[:len(ot)] == ot
    # 잘린 마지막 줄 (CI S3): 앞 항목은 다 맞고 마지막 관측 TITEL 이 기대의 앞부분 **문자열** — 모순 확정이 아니라 자동 확인 불가. 통과·r1 자격 없이 막고(fail-closed) 원문 확인·새 승인으로만 푼다.
    titel_truncated = bool(ot) and ot != titel and not titel_prefix_only and len(ot) <= len(titel) and ot[:-1] == titel[:len(ot) - 1] and titel[len(ot) - 1].startswith(ot[-1])
    if titel_truncated:
        conflicts.append(("TITEL_TRUNCATED", f"OUTCAR 마지막 TITEL {ot[-1]!r} 이 기대 {titel[len(ot) - 1]!r} 의 앞부분 문자열 — 잘린 줄일 수 있어 **자동 확인 불가** "
                                             "(모순 확정 아님 · 통과·재시도 자격 없음 · 원문 확인·새 승인으로만 해제)"))
    elif ot and ot != titel and not titel_prefix_only:
        conflicts.append(("POTCAR_MISMATCH", f"OUTCAR TITEL {ot} ≠ POTCAR.titel {titel} (접두 아님 — 다른 종·날짜·순서·추가)"))
    if pp_registry:
        if any(pp_registry["species_sha256"].get(k) != v for k, v in r["potcar_species_sha256"].items()):
            conflicts.append(("POTCAR_MISMATCH", "봉인 등록부의 종별 sha 와 다르다"))
        if pp_registry["assembled_sha256"].get(_spec_key(job)) != psha:
            conflicts.append(("POTCAR_MISMATCH", "봉인 등록부의 조립본 sha 와 다르다"))
        if o and o["version"] and o["version"] != pp_registry["vasp_version"]:
            conflicts.append(("VERSION_MISMATCH", f"VASP {o['version']!r} ≠ 등록부 {pp_registry['vasp_version']!r}"))
    missing, bad, src = audit_settings(o, job) if o else ([], [], {})
    if bad:
        conflicts.append(("SETTINGS_MISMATCH", "; ".join(bad)))
    ref = fin(job.get("d3_2body_eV_ref"))
    if o and ref is not None and o["Edisp_eV"] is not None and abs(o["Edisp_eV"] - ref) > D3_REL_TOL * abs(ref):
        conflicts.append(("D3_MISMATCH", f"Edisp {o['Edisp_eV']:.4f} vs ref {ref:.4f} eV (>1 % — 감쇠·3체·계수 오설정 의심)"))
    if conflicts:
        return done(conflicts[0][0], conflicts[0][1], conflicts=[f"{s}: {w}" for s, w in conflicts])
    # ── ② 실행 상태 — 재시도 자격 ──
    if rc != 0:
        return done("EXECUTION_FAILED", f"rc {rc}")
    if o is None or not os.path.isfile(os.path.join(attdir, "OSZICAR")):
        return done("NOT_TERMINATED", "rc 0 인데 OUTCAR/OSZICAR 없음")
    if o["n_runs"] == 0:
        return done("OUTCAR_UNPARSEABLE", "OUTCAR 에 실행 머리줄이 없다")
    if not o["terminated"]:
        return done("NOT_TERMINATED")
    if not o["converged"]:
        return done("SCF_NOT_CONVERGED")
    # ── ③ 완결성 — 성공한 실행만 · 결측 = 미검증 ──
    r["settings_sources"] = src
    if not o["outcar_titel"]:
        return done("POTCAR_UNVERIFIED", "OUTCAR 에 TITEL 이 없다")
    if titel_prefix_only:
        return done("POTCAR_UNVERIFIED", f"성공한 실행인데 OUTCAR TITEL 이 기대 목록의 앞부분만 있다 {ot} (불완전 출력 — 통과 아님 · 재시도 자격 아님)")
    if any(k in missing for k in ("NIONS", "NELECT")):
        return done("SYSTEM_UNVERIFIED", f"OUTCAR 에 {missing} 없음")
    if missing:
        return done("SETTINGS_UNVERIFIED", f"해석값을 못 읽음: {missing} (입력 에코는 세지 않는다 · 파일럿으로 파서 확인)")
    if o["TOTEN_eV"] is None or o["E_sigma0_eV"] is None:
        return done("ENERGY_UNPARSEABLE", "마지막 FREE ENERGIE 구획의 TOTEN·E(σ→0) 마지막 레코드가 없거나 유한수가 아니다")
    if ref is None or o["Edisp_eV"] is None:
        return done("D3_UNVERIFIED", "D3 기대값 또는 Edisp 마지막 레코드(유한수) 없음")
    return done("OK")


def validate_pp_registry(reg, manifest_sha256, meta=None):
    """봉인 PP 등록부 내용 검증 → 오류 목록 (빈 목록이면 통과)."""
    if not isinstance(reg, dict):
        return ["등록부가 JSON 객체가 아니다"]
    e = []
    if reg.get("schema") != REG_SCHEMA:
        e.append(f"schema {reg.get('schema')!r} ≠ {REG_SCHEMA}")
    if reg.get("pp_set") != PP_SET:
        e.append(f"pp_set {reg.get('pp_set')!r} ≠ {PP_SET}")
    want_t = {POTCAR_MAP[s]: PP_EXPECTED_TITEL[s] for s in SPECIES_ORDER}
    if reg.get("titel") != want_t:
        e.append("titel 이 PBE_54 기대 TITEL 과 다르다")
    sp = reg.get("species_sha256")
    if not (isinstance(sp, dict) and set(sp) == set(want_t) and all(isinstance(v, str) and HEX64.match(v) for v in sp.values())):
        e.append("species_sha256 형식 (다섯 종 · 64 hex)")
    need = {",".join(j["potcar_spec"]) for j in meta["jobs"]} if meta else {",".join(POTCAR_MAP[s] for s in SPECIES_ORDER)}
    asm = reg.get("assembled_sha256")
    if not (isinstance(asm, dict) and need <= set(asm) and all(isinstance(v, str) and HEX64.match(v) for v in asm.values())):
        e.append(f"assembled_sha256 형식·범위 (필요 {sorted(need)})")
    if not (isinstance(reg.get("vasp_version"), str) and reg["vasp_version"].strip().startswith("vasp.")):
        e.append("vasp_version (OUTCAR 첫 줄)")
    if str(reg.get("package_manifest_sha256", "")).lower() != str(manifest_sha256).lower():
        e.append("package_manifest_sha256 ≠ 고정 MANIFEST")
    fp = reg.get("from_pilot")
    if not (isinstance(fp, dict) and set(fp) == set(PILOT_JOBS) and all(isinstance(v, str) and RUN_ID_RE.match(v) for v in fp.values())):
        e.append("from_pilot (파일럿 두 잡의 run_id)")
    fps = reg.get("from_pilot_sha256")
    if not (isinstance(fps, dict) and set(fps) == set(PILOT_JOBS)
            and all(isinstance(v, dict) and set(v) == {"attempt.json", "OUTCAR"} and all(isinstance(h, str) and HEX64.match(h) for h in v.values()) for v in fps.values())):
        e.append("from_pilot_sha256 (파일럿 두 잡의 봉인 당시 attempt.json · OUTCAR sha)")
    return e


def check(out, ret, manifest_sha256, pp_registry=None):
    verify_manifest(out, manifest_sha256)
    meta = json.load(open(os.path.join(out, "jobs.json"), encoding="utf-8"))
    if pp_registry is not None:
        errs = validate_pp_registry(pp_registry, manifest_sha256, meta)
        if errs:
            raise PkgError(f"PP 등록부 검증 실패: {errs}")
    J = {j["dir"]: j for j in meta["jobs"]}
    run = os.path.join(ret, "run") if os.path.isdir(os.path.join(ret, "run")) else ret
    res, every = {}, []
    for job in meta["jobs"]:
        bdir, rdir = os.path.join(run, job["dir"]), os.path.join(run, job["dir"] + "_r1")
        base = check_job(job, out, bdir, "0", pp_registry); every.append((job["dir"], base))
        r1 = check_job(job, out, rdir, "r1", pp_registry) if os.path.isdir(rdir) else None
        if r1 is not None:
            every.append((job["dir"], r1))
        if r1 is None:
            res[job["dir"]] = base
        elif base["status"] in R1_ELIGIBLE:
            res[job["dir"]] = {**r1, "first_attempt": base["status"]} if r1["status"] == "OK" else {**base, "r1": r1["status"]}
        else:
            res[job["dir"]] = {**base, "r1_ignored": f"첫 시도 상태 {base['status']} 는 재시도 자격이 아니다 (사전등록: 실행 실패·미종료·미수렴만)",
                               "r1_status": r1["status"]}
    # 잡 사이 일관성 — 첫 시도·r1 **모든 시도**에서 모은다 (어긋나면 어느 쪽이 맞는지 모르므로 전부 막는다)
    by_sp, by_spec, vers = {}, {}, set()
    for n, r in every:
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
            r["status"] = "POTCAR_INCONSISTENT"; r["why"] = f"시도 사이 POTCAR sha 가 갈린다: {incons}"
        elif len(vers) > 1:
            r["status"] = "VERSION_INCONSISTENT"; r["why"] = f"시도 사이 VASP 버전 줄이 갈린다: {sorted(vers)}"
    # 파일럿 결속 (CG P1-2 · 권고 3): 등록부가 있으면 파일럿 두 잡의 **채택 시도**(0 또는 정당한 r1)가 봉인한 그 실행이어야 한다 — run_id · attempt.json·OUTCAR sha.
    # 다르면 자동 교체 없이 막는다 (다른 폴더에서 다시 돌린 파일럿 · 같은 ID 아래 파일 교체) — 재실행은 새 승인 대상.
    if pp_registry is not None:
        for p in PILOT_JOBS:
            r = res.get(p)
            if not r or r["status"] != "OK":
                continue
            want, ws = pp_registry["from_pilot"][p], pp_registry["from_pilot_sha256"][p]
            if r.get("run_id") != want:
                r["status"] = "PILOT_NOT_SEALED"; r["why"] = f"채택 시도 run_id {r.get('run_id')} ≠ 봉인 {want} — 봉인한 파일럿 실행이 아니다 (자동 교체 없음 · 재실행은 새 승인)"
            elif r.get("attempt_json_sha256") != ws["attempt.json"] or r.get("outcar_sha256") != ws["OUTCAR"]:
                r["status"] = "PILOT_NOT_SEALED"; r["why"] = "같은 run_id 인데 attempt.json·OUTCAR sha 가 봉인과 다르다 — 봉인 뒤 파일이 바뀌었다"
    return meta, res


def check_exit(res):
    return 0 if res and all(v["status"] == "OK" for v in res.values()) else 3


def seal_pp(out, ret, manifest_sha256):
    """파일럿 반송(OK 인 잡)에서 종별 TITEL·sha · 조립본 sha · VASP 버전 줄 · run_id 를 뽑아 등록부를 만든다 (등록 전 단계 — 등록부 없이 검사).
    파일럿 잡이 OK 가 아니면 만들지 않는다."""
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
    reg = {"schema": REG_SCHEMA, "pp_set": PP_SET, "titel": titel, "species_sha256": sp_sha, "assembled_sha256": asm, "vasp_version": vers.pop(),
           "from_pilot": {n: ok[n].get("run_id") for n in PILOT_JOBS},
           "from_pilot_sha256": {n: {"attempt.json": ok[n].get("attempt_json_sha256"), "OUTCAR": ok[n].get("outcar_sha256")} for n in PILOT_JOBS},
           "package_manifest_sha256": str(manifest_sha256).lower(),
           "pilot_settings_sources": {n: ok[n].get("settings_sources") for n in PILOT_JOBS},
           "⛔": "이 등록부를 봉인(커밋·해시 기록)한 뒤 나머지 16 잡을 받는다 — 이후 모든 잡이 같아야 한다 · 최종 집계는 이 파일과 그 sha 가 필수"}
    errs = validate_pp_registry(reg, manifest_sha256, meta)
    if errs:
        raise PkgError(f"등록부를 만들었지만 검증 실패: {errs}")
    return reg


def load_pp_registry(path, sha, manifest_sha256=None):
    if not path:
        if sha:
            raise PkgError("--pp_registry_sha256 만 있고 --pp_registry 가 없다")
        return None
    if not sha or not HEX64.match(sha.lower()) or _sha(path) != sha.lower():
        raise PkgError("PP 등록부 sha 가 고정값과 다르다")
    reg = json.load(open(path, encoding="utf-8"))
    if manifest_sha256 is not None:
        errs = validate_pp_registry(reg, manifest_sha256)
        if errs:
            raise PkgError(f"PP 등록부 검증 실패: {errs}")
    return reg


# ───────────────────────── UMA 입력 (CE P0-4) ─────────────────────────
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
def collect(out, ret, manifest_sha256, uma=None, pp_registry=None, pp_registry_sha256=None):
    """최종 사용 판정은 봉인 PP 등록부가 있어야만 열린다 (없으면 파일럿 단계 집계 — G5 BLOCKED · total W 인용 불가)."""
    meta, res = check(out, ret, manifest_sha256, pp_registry)
    reg_ok = pp_registry is not None
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
    # G4 — 변형 잡은 표본 ① 과 같은 기하: Edisp 가 같아야 전자 수치 변화를 읽을 수 있다 (CF P0-3)
    b0, f0 = G5_SAMPLES["①"]
    g4 = {}
    for tag, lab in (("e70", "ENCUT 650"), ("k1", "k 4×3×1"), ("s05", "SIGMA ½")):
        b, f = f"V5_s_outer_A_G4_{tag}_bound", f"V5_s_outer_A_G4_{tag}_far"
        Wx = dA(b, f, F)
        dd = {"bound": (ED[b] - ED[b0]) if (b in ED and b0 in ED) else None, "far": (ED[f] - ED[f0]) if (f in ED and f0 in ED) else None}
        dw = (Wx - base) if (Wx is not None and base is not None) else None
        if dw is None or None in dd.values():
            st = "INCOMPLETE"
        elif max(abs(v) for v in dd.values()) > D3_SAME_GEOM_TOL_EV:
            st = f"INCOMPLETE (D3 불일치 — 같은 기하 기준 잡과 Edisp 차 > {D3_SAME_GEOM_TOL_EV:g} eV)"
        else:
            st = "PASS" if abs(dw) <= G4_DW else "FAIL"
        g4[tag] = {"variant": lab, "W": Wx, "dW": dw, "d3_same_geom_diff_eV": dd, "status": st}
    st4 = [v["status"] for v in g4.values()]
    g4["status"] = "FAIL" if "FAIL" in st4 else ("INCOMPLETE" if any(s.startswith("INCOMPLETE") for s in st4) else "PASS")
    for k, s in smp.items():
        labels = []
        if not reg_ok:
            labels.append("PP 등록부 없음 (파일럿 단계)")
        if s["d3_pair_over_budget"] is None:
            labels.append("D3 쌍 오차 미산출")
        elif s["d3_pair_over_budget"]:
            labels.append("D3 쌍 오차 예산 초과")
        if g3["status"] != "PASS":
            labels.append(f"G3 {g3['status']}")
        if g4["status"] != "PASS":
            labels.append(f"G4 {g4['status']}")
        s["total_w_labels"] = labels
        s["total_w_citable"] = bool(s["W_J_m2"] is not None and not labels)
    rec = {"schema": "aprime_v5_vasp_collect/v3", "manifest_sha256": manifest_sha256, "return_bundle": return_manifest_info(ret, manifest_sha256),
           "pp_registry": ({"state": "검증됨", "sha256": pp_registry_sha256, "vasp_version": pp_registry["vasp_version"]} if reg_ok
                           else {"state": "없음 — 파일럿 단계 집계 (최종 사용 판정 불가)"}),
           "energy_convention": "W = MP1 σ 0.136 eV 에서의 TOTEN(자유에너지) 차 / A — 0 K 점착에너지·실제 전자온도 자유에너지라 부르지 않는다 (CE Q2) · E(σ→0)·−TS 항 차 병기",
           "samples": smp, "G3": g3, "G4": g4, "jobs": res, "jobs_not_ok": sorted(n for n, v in res.items() if v["status"] != "OK"),
           "⛔": "VASP 비교군 — QE V2·V4 값과 빼거나 섞지 않는다 · D3 예산은 운영 예산이지 신뢰구간이 아니다"}
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
              "pp_registry_validated": reg_ok,
              "usage_eligible": bool(raw_ok and not errs and reg_ok and g3["status"] == "PASS" and g4["status"] == "PASS"),
              "note": "①·⑤ 는 far 를 공유 — 독립 5 회 검증이 아니다 · ±0.10/±0.05 를 새 계면의 신뢰구간으로 옮기지 않는다 · PASS ≠ DEM 전달 승인 (카드 DEM 합의 별도)"}
        if errs:
            g5["status"] = "BLOCKED (UMA 입력 출처·값 검사 실패)"
        elif not reg_ok:
            g5["status"] = "BLOCKED (PP 등록부 없음 — 최종 판정은 봉인 등록부 필수 · 파일럿 단계 집계)"
        elif not complete:
            g5["status"] = "INCOMPLETE (분모 5 고정 · 교체 금지)"
        elif g3["status"] != "PASS" or g4["status"] != "PASS":
            g5["status"] = f"INCOMPLETE (G3 {g3['status']} · G4 {g4['status']} — 오차표만 · 원시 기준 {'충족' if raw_ok else '미충족'})"
        elif not raw_ok:
            g5["status"] = "FAIL"
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
                 version=DEFAULT_FAKE_VERSION, ngzf=400, min_pos="auto", dipol_line=False, incar_echo=(), final_toten=None,
                 extra_final_toten=None, vdw=None, final_block=True):
    """실물(VASP 5.4.4) 구조를 흉내 낸 합성 OUTCAR: INCAR: · POTCAR/TITEL · 배열 · Startparameter · DIPCOR min pos · SCF 단계 TOTEN(D3 빠짐)
    · DFTD3 구획 · Edisp (콜론 없음) · FREE ENERGIE 최종 구획(D3 포함) · 종료 줄."""
    tl = titel_override or job["pp_expected_titel"]
    t = [f" {version}", " ", " executed on             LinuxIFC date 2026.10.01  00:00:00", "", " INCAR:"]
    t += [f"   {x}" for x in incar_echo]
    t += [f" POTCAR:    {tt}" for tt in tl]
    for tt in tl:
        t += ["   VRHFIN =X: s p", f"   TITEL  = {tt}"]
    t.append(" Dimension of arrays:")
    if "NIONS" not in drop:
        t.append(f"   number of dos      NEDOS =    301   number of ions     NIONS = {job['nions']:6d}")
    t += [f"   dimension x,y,z NGXF= {ngzf // 2:5d} NGYF= {ngzf // 2:4d} NGZF= {ngzf:4d}",
          f"   support grid    NGXF= {ngzf:5d} NGYF= {ngzf:4d} NGZF= {2 * ngzf:4d}", "", " Startparameter for this run:"]
    echo = {"ISPIN": "   ISPIN  =      1    spin polarized calculation?",
            "ENCUT": f"   ENCUT  = {encut if encut is not None else job['encut']:7.1f} eV  38.22 Ry    6.18 a.u.",
            "NELECT": f"   NELECT = {job['nelect_expected']:12.4f}    total number of electrons",
            "SIGMA": f"   ISMEAR =     1;   SIGMA  = {job['sigma']:7.2f}  broadening in eV -4-tet -1-fermi 0-gaus",
            "LDIPOL": "   LDIPOL =      T    correct potential (dipole corrections)",
            "IDIPOL": "   IDIPOL =      3    1-x, 2-y, 3-z, 4-all directions"}
    t += [v for k, v in echo.items() if k not in drop]
    if dipol_line is not False:
        t.append(f"   DIPOL  =   0.5000  0.5000  {(job['dipol_z'] if dipol_line is True else dipol_line):.4f}")
    if efield is not None:
        t.append(f"   EFIELD = {efield}")
    mp = (round(((job["dipol_z"] + 0.5) % 1.0) * ngzf) % ngzf) if min_pos == "auto" else min_pos
    for i in range(3):
        if mp is not None:
            t += [" DIPCOR: dipole corrections for dipol", f" direction  3 min pos {mp:5d},"]
        t.append(f"  free energy    TOTEN  =  {E - Ed + 0.1 * (2 - i):18.8f} eV")
        t.append(f"  energy without entropy =  {E - Ed + 0.1 * (2 - i) + 0.01:18.8f}  energy(sigma->0) =  {E - Ed + 0.1 * (2 - i) + 0.005:18.8f}")
    t.append("------------------------ aborting loop because EDIFF is reached ----------------------------------------" if conv
             else "------------------------ aborting loop EDIFF was not reached (unconverged)  ----------------------------")
    vd = {"IVDW": "12", "VDW_S6": "1.0000", "VDW_S8": "0.7875", "VDW_A1": "0.4289", "VDW_A2": "4.4407", "VDW_RADIUS": "50.2000 A", "VDW_CNRADIUS": "21.1700 A"}
    vd.update(vdw or {})
    t += ["         DFTD3 V3.0 Rev 1        "] + [f" {k:<12s} = {v}" for k, v in vd.items() if k not in drop]
    if edisp:
        t.append(f" Edisp (eV)  {Ed:.5f}")
    if final_block:
        t += ["  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)", "  ---------------------------------------------------",
              f"  free  energy   TOTEN  =  {final_toten if final_toten is not None else format(E, '18.8f')} eV", "",
              f"  energy  without entropy=  {E + 0.01:18.8f}  energy(sigma->0) =  {E + 0.005:18.8f}"]
        if extra_final_toten is not None:
            t.append(f"  free  energy   TOTEN  =  {extra_final_toten} eV")
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
for f in ("WAVECAR", "CHGCAR", "CHG", "vasprun.xml", "IBZKPT", "EIGENVAL"):   # 실물처럼 큰 산출물도 쓴다 — 묶음 허용 목록 시험용
    B._write(f, f"FAKE {f} DO_NOT_SHIP\n")
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
    def raises(fn):
        try:
            fn()
        except PkgError:
            return True
        return False
    # ① 순수 함수
    at = Atoms("AgLiSAgClP", positions=[[0, 0, 1], [1, 0, 5], [2, 0, 6], [0, 1, 2], [3, 0, 7], [4, 0, 8]], cell=[10, 10, 30], pbc=True)
    txt, order, present = poscar_text(at, "t"); sp, nn, cell, pos = parse_poscar_cart(txt)
    ck(sp == ["Li", "P", "S", "Cl", "Ag"] and nn == [1, 1, 1, 1, 2] and all(np.allclose(pos[k], at.positions[order[k]]) for k in range(len(order))), "POSCAR 종 순서 · 대응표")
    ck(raises(lambda: poscar_text(Atoms("Fe", positions=[[0, 0, 0]], cell=[5, 5, 5]), "x")), "⛔음성 모르는 원소 Fe")
    ck(abs(dipol_z(0.85963, 0.03119) - 0.375225) < 1e-6, "DIPOL_z = 중심 − ½")
    ck(abs(check_dip_clear(Atoms("Ag2", positions=[[0, 0, 5.0], [0, 0, 22.0]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119) - 5.558) < 1e-2
       and abs(check_dip_clear(Atoms("Ag2", positions=[[0, 0, 1.0], [0, 0, 20.0]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119) - 4.5) < 1e-2, "쌍극자 여유 (위 원자 · 바닥 위 영상)")
    for z1, z2 in ((1.0, 26.0), (32.058 - 1.5, 10.0)):
        ck(raises(lambda: check_dip_clear(Atoms("Ag2", positions=[[0, 0, z1], [0, 0, z2]], cell=[10, 10, 32.058], pbc=True), 0.85963, 0.03119)), "⛔음성 쌍극자 여유 부족 통과")
    i0, e0 = parse_incar_strict(incar_text("x", 520, 0.136, 0.3752))
    ck(not e0 and i0["VDW_RADIUS"] == "50.2" and i0["VDW_CNRADIUS"] == "21.17" and i0["IVDW"] == "12" and i0["DIPOL"] == "0.5 0.5 0.375200" and "AMIX" not in i0,
       "INCAR: D3 절단 명시 · IVDW · DIPOL · 혼합 태그 없음")
    d, e = parse_incar_strict("NCORE = 1 ; EFIELD = 0.01\n")
    ck(not e and d == {"NCORE": "1", "EFIELD": "0.01"}, f"INCAR 파서: ';' 는 문장 구분 (VASP 의미) — {d} {e}")
    ck(bool(parse_incar_strict("ENCUT = 520\nENCUT = 400\n")[1]) and bool(parse_incar_strict("NCORE = 1 \\\n")[1]), "⛔음성 INCAR 파서: 중복 태그 · 줄 이음 → 오류")
    ck(perf_value_ok("NCORE", "16") and not perf_value_ok("NCORE", "two") and not perf_value_ok("NCORE", "0") and perf_value_ok("LPLANE", ".TRUE.")
       and not perf_value_ok("LPLANE", "yes") and not perf_value_ok("EFIELD", "0"), "성능 태그 값 타입")
    ck(fin(float("nan")) is None and fin(float("inf")) is None and fin(True) is None and fin("1.0") is None and fin(2) == 2.0
       and _tok_float("NaN") is None and _tok_float("*******") is None and _tok_float("-1.5") == -1.5, "fin · 토큰: NaN·Inf·bool·str·별표 거부")
    po = parse_outcar(" vasp.6.4.2 x\n   TITEL  = A\n   TITEL  = B\n   TITEL  = A\n")
    ck(po["outcar_titel"] == ["A", "B"] and po["version"] == "vasp.6.4.2 x" and po["n_runs"] == 1, "OUTCAR TITEL 반복 인쇄 → 순서 보존 중복 제거 · 버전 줄 전체")
    # ② 실물 OUTCAR 발췌 (VASP 5.4.4 · CF P1-2 · R2)
    rp = os.path.join(HERE, "..", "..", REAL_OUTCAR_544_SRC)
    if os.path.isfile(rp):
        real = {ln.strip() for ln in gzip.open(rp, "rt", encoding="utf-8", errors="replace")}
        ck(all(ln.strip() in real for ln in REAL_OUTCAR_544.splitlines() if ln.strip()), "실물 픽스처 = 저장소 원본 OUTCAR.gz 의 줄 발췌 (한 줄도 지어내지 않음)")
    else:
        print(f"  ⚠ SKIP 실물 원본 대조 ({REAL_OUTCAR_544_SRC} 없음) — 통과로 세지 않는다")
    ro = parse_outcar(REAL_OUTCAR_544); rs = ro["settings"]
    ck(ro["version"].startswith("vasp.5.4.4") and ro["n_runs"] == 1 and ro["terminated"] and ro["converged"] and rs["NIONS"] == 227 and rs["NELECT"] == 1596.0
       and rs["ENCUT"] == 520.0 and rs["ISMEAR"] == 0 and rs["SIGMA"] == 0.05 and rs["ISPIN"] == 2 and rs["IVDW"] == 11 and rs["LDIPOL"] == "T"
       and rs["IDIPOL"] == 3 and rs["DIPOL_z"] is None and rs["VDW_S6"] == 1.0 and rs["VDW_S8"] == 0.722 and rs["VDW_RADIUS"] == 50.2022 and rs["VDW_CNRADIUS"] == 21.1671,
       f"실물 5.4.4: 설정 해석값 판독 — {rs}")
    ck(ro["Edisp_eV"] == -28.80731 and ro["TOTEN_eV"] == -1151.29778848 and ro["E_sigma0_eV"] == -1151.29228248 and ro["E_noentropy_eV"] == -1151.28677648,
       f"실물 5.4.4: Edisp 무콜론 형식 · TOTEN 은 SCF 단계(-1122.49 · D3 빠짐)가 아니라 최종 구획(D3 포함) — {ro['Edisp_eV']} {ro['TOTEN_eV']}")
    ck(ro["NGZF"] == 560 and ro["dipole_min_pos"] == 520, f"실물 5.4.4: NGZF 는 support grid(1120)가 아니라 dimension 줄 · min pos 520 — {ro['NGZF']} {ro['dipole_min_pos']}")
    g_ok, b_ok = dipol_evidence(ro, REAL_OUTCAR_544_DIPOL_Z); g_bad, b_bad = dipol_evidence(ro, 0.30)
    ck(g_ok and not b_ok and not g_bad and b_bad, f"실물 5.4.4: cut 위치 min pos 520/560 = DIPOL_z(0.4278)+½ (±2 격자) · 0.30 이면 모순 — {g_ok} {b_bad}")
    ck(parse_outcar(" Edisp (eV):  -1.23456\n")["Edisp_eV"] == -1.23456 and parse_outcar(" Edisp = -2.5\n")["Edisp_eV"] == -2.5
       and parse_outcar(" Edisp (eV)  -1.0\n Edisp (eV)  NaN\n")["Edisp_eV"] is None, "Edisp 콜론·등호 변형 · 마지막 레코드가 NaN 이면 None (앞 값 안 씀)")
    stp = "  free energy    TOTEN  =  -10.00000000 eV\n  energy without entropy =  -10.10000000  energy(sigma->0) =  -10.05000000\n"
    p1, p2 = parse_outcar(stp), parse_outcar(stp + "  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)\n  free  energy   TOTEN  =  -12.00000000 eV\n"
                                               "  energy  without entropy=  -12.10000000  energy(sigma->0) =  -12.05000000\n")
    ck(p1["TOTEN_eV"] is None and p1["E_sigma0_eV"] is None and p1["E_noentropy_eV"] is None and p2["TOTEN_eV"] == -12.0 and p2["E_sigma0_eV"] == -12.05,
       "SCF 단계 레코드만 있으면 에너지 None (D3 빠진 값을 안 씀) · 최종 FREE ENERGIE 구획 뒤 값만 쓴다")
    fb = ("  FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)\n  free  energy   TOTEN  =  -12.00000000 eV\n"
          "  energy  without entropy=  -12.10000000  energy(sigma->0) =  -12.05000000\n Edisp (eV)  -1.5\n")
    pe = parse_outcar(fb + "  free  energy   TOTEN  =\n")
    ck(pe["TOTEN_eV"] is None and pe["E_sigma0_eV"] == -12.05 and pe["E_noentropy_eV"] == -12.1,
       "⛔음성 CG 권고 1: 정상 뒤 EOF 의 빈 'TOTEN =' 도 마지막 레코드 → None (앞 값 안 씀 · 다른 항목은 그대로)")
    ck(parse_outcar(fb + "  energy(sigma->0) =\n")["E_sigma0_eV"] is None and parse_outcar(fb + "  energy  without entropy=\n")["E_noentropy_eV"] is None
       and parse_outcar(fb + " Edisp (eV)\n")["Edisp_eV"] is None and parse_outcar(fb + " Edisp (eV)\n  FREE ENERGIE\n")["Edisp_eV"] is None,
       "⛔음성 CG 권고 1: 빈 σ→0 · 무엔트로피 · Edisp 레코드 → None · 값 패턴이 다음 줄의 토큰을 집지 않는다")
    eo = parse_outcar(" INCAR:\n   ENCUT = 400\n   DIPOL = 0.5 0.5 0.1\n POTCAR:    PAW_PBE X\n Startparameter for this run:\n   ENCUT  =  520.0 eV  x\n")
    ck(eo["settings"]["ENCUT"] == 520.0 and eo["settings"]["DIPOL_z"] is None and eo["incar_echo_lines_excluded"] == 2
       and parse_outcar(" INCAR:\n   ENCUT = 520 eV\n POTCAR:    PAW_PBE X\n")["settings"]["ENCUT"] is None, "INCAR 에코 구획은 설정 판독에서 뺀다 (에코에만 있으면 None)")
    # ③ 합성 S3v2 패키지 → build() 로 실제 경로 시험 (D3 가 1 % 문턱이 시험 이동보다 크도록 Ag 3 층 슬랩)
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
        PERF_OK = "NCORE = 16\nKPAR = 2\nLPLANE = .TRUE.\n"                     # 기본 시도 = 허용 성능 태그 3 개 붙은 정상 실행
        JI = {n: i + 1 for i, n in enumerate(sorted(J))}
        def mk(n, att="0", *, outcar=None, incar_extra=PERF_OK, incar=None, rc=0, titel=None, spsha=None, psha_override=None, drop=(), no_out=False,
               tamper_after=None, **kw):
            # run_id 는 잡·시도마다 고정 — 같은 내용으로 다시 만들면 같은 실행 기록이 된다 (파일럿 봉인 결속 시험이 이 성질을 쓴다)
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
            _write(os.path.join(d, "attempt.json"), json.dumps({"job": n, "attempt": att, "run_id": f"20260927T120000-4242-{JI[n]}{1 if att == 'r1' else 0}", "rc": rc,
                                                              "t_start": 1000, "t_end": 1100, "sha256": {**shas, "POTCAR": psha}}))
            for f in drop:
                os.remove(os.path.join(d, f))
            if tamper_after:
                tamper_after(d)
            return d
        def edit_attempt(d, **upd):
            aj = json.load(open(os.path.join(d, "attempt.json")))
            for k, v in upd.items():
                if v is None:
                    aj.pop(k, None)
                else:
                    aj[k] = v
            _write(os.path.join(d, "attempt.json"), json.dumps(aj))
        def st(n, reg=None):
            return check(out, ret, msha, reg)[1][n]["status"]
        for n in J:
            mk(n)
        _, res = check(out, ret, msha)
        ck(all(v["status"] == "OK" for v in res.values()) and check_exit(res) == 0,
           f"정상 대조군: 18 잡 OK (성능 태그 3 개 허용 · DIPOL 은 min pos cut 으로) — {[(n, v['status'], v.get('why')) for n, v in res.items() if v['status'] != 'OK'][:3]}")
        reg_ok = seal_pp(out, ret, msha)
        ck(not validate_pp_registry(reg_ok, msha, meta) and reg_ok["from_pilot"][PILOT_JOBS[0]].startswith("20260927T")
           and reg_ok["schema"] == "aprime_v5_pp_registry/v3" and all(HEX64.match(reg_ok["from_pilot_sha256"][p][k]) for p in PILOT_JOBS for k in ("attempt.json", "OUTCAR")),
           "seal_pp: 등록부 생성 (schema v3 · 파일럿 run_id + attempt.json·OUTCAR sha) · 스스로 검증 통과")
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
        C = lambda u=uma, reg=reg_ok: collect(out, ret, msha, u, reg, "f" * 64 if reg else None)
        rc_ = C()
        ck(rc_["G3"]["status"] == "PASS" and rc_["G4"]["status"] == "PASS" and rc_["G5"]["status"] == "PASS" and collect_exit(rc_) == 0
           and abs(rc_["G5"]["Delta_J_m2"]["①"] - 0.01) < 1e-6 and rc_["G5"]["usage_eligible"] is True and rc_["G5"]["raw_error_criteria_met"] is True
           and rc_["pp_registry"]["state"] == "검증됨" and all(s["total_w_citable"] for s in rc_["samples"].values())
           and rc_["samples"]["①"]["mTS_term_J_m2"] is not None and abs(rc_["samples"]["①"]["mTS_term_J_m2"]) < 1e-9
           and all(abs(v) < 1e-12 for t4 in ("e70", "k1", "s05") for v in rc_["G4"][t4]["d3_same_geom_diff_eV"].values()),
           f"정상 대조군: 등록부 있음 → G3·G4·G5 PASS · 종료 0 · total W 인용 가능 · G4 같은 기하 D3 차 0 — {rc_['G3']['status']} {rc_['G4']['status']} {rc_['G5']['status']}")
        json.dumps(rc_, allow_nan=False)
        F_ = "V5_s_outer_A_far"
        # ④ CE P0-1 성능 태그 우회
        mk(F_, incar_extra="NCORE = 1 ; EFIELD = 0.01\n")
        ck(st(F_) == "INPUT_MODIFIED", "⛔음성 CE P0-1 'NCORE = 1 ; EFIELD = 0.01' → INPUT_MODIFIED")
        for extra, why in (("NCORE = 1 ; ENCUT = 400\n", "세미콜론 ENCUT"), ("NCORE = 16\nNCORE = 8\n", "중복"), ("KPAR = two\n", "타입"),
                           ("NCORE = 16 \\\n", "줄 이음"), ("NWRITE = 0\n", "허용 밖")):
            mk(F_, incar_extra=extra)
            ck(st(F_) == "INPUT_MODIFIED", f"⛔음성 CE P0-1 성능 태그 {why} → INPUT_MODIFIED")
        # ⑤ CE P0-2 지난 출력 · 복수 실행 · 설정 되울림 · 실행 기록 형식
        mk(F_, rc=1)
        ck(st(F_) == "EXECUTION_FAILED", "⛔음성 CE P0-2 rc=1 (OUTCAR 는 정상이어도) → EXECUTION_FAILED")
        mk(F_, tamper_after=lambda d: _write(os.path.join(d, "OUTCAR"), open(os.path.join(d, "OUTCAR")).read() + " \n"))
        ck(st(F_) == "ATTEMPT_MISMATCH", "⛔음성 CE P0-2 실행 뒤 OUTCAR 교체 → ATTEMPT_MISMATCH")
        good_outcar = _fake_outcar(J[F_], E[F_], ED[F_])
        mk(F_, rc=1, no_out=True, tamper_after=lambda d: (_write(os.path.join(d, "OUTCAR"), good_outcar), _write(os.path.join(d, "OSZICAR"), "DAV: 1\n")))
        ck(st(F_) == "ATTEMPT_MISMATCH", "⛔음성 CE P0-2 실패한 실행(OUTCAR 없음) 뒤에 지난 정상 OUTCAR 를 넣음 → ATTEMPT_MISMATCH")
        mk(F_, extra_run=True)
        ck(st(F_) == "MULTIPLE_RUNS", "⛔음성 CE P0-2 두 번째 미완결 실행 붙임 → MULTIPLE_RUNS")
        mk(F_, encut=400.0)
        ck(st(F_) == "SETTINGS_MISMATCH", "⛔음성 CE P0-2 OUTCAR ENCUT 400 (INCAR 520) → SETTINGS_MISMATCH")
        mk(F_, efield=0.01)
        ck(st(F_) == "SETTINGS_MISMATCH", "⛔음성 OUTCAR EFIELD ≠ 0 → SETTINGS_MISMATCH")
        mk(F_, drop=("attempt.json",))
        ck(st(F_) == "MISSING", "⛔음성 attempt.json 없음 → MISSING")
        for upd, why in (({"rc": "0"}, "rc 문자열"), ({"run_id": None}, "run_id 없음"), ({"run_id": "abc"}, "run_id 형식"),
                         ({"t_end": 900}, "t_end < t_start"), ({"t_start": None}, "t_start 없음")):
            mk(F_, tamper_after=lambda d, u=upd: edit_attempt(d, **u))
            ck(st(F_) == "ATTEMPT_MISMATCH", f"⛔음성 실행 기록 {why} → ATTEMPT_MISMATCH (CF 권고)")
        for key, kw in (("IVDW", {"drop": ("IVDW",)}), ("DIPOL", {"min_pos": None}), ("SIGMA", {"drop": ("SIGMA",)}), ("ENCUT", {"drop": ("ENCUT",)}),
                        ("VDW_A2", {"drop": ("VDW_A2",)}), ("ENCUT 에코만", {"drop": ("ENCUT",), "incar_echo": ("ENCUT = 520.0 eV",)})):
            mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], **kw))
            ck(st(F_) == "SETTINGS_UNVERIFIED", f"⛔음성 해석값 {key} 못 읽음 → SETTINGS_UNVERIFIED (통과 아님)")
        for why, kw in (("min pos cut 불일치", {"min_pos": (round(((J[F_]["dipol_z"] + 0.5) % 1.0) * 400) + 20) % 400}),
                        ("DIPOL 줄 불일치", {"dipol_line": 0.1}), ("VDW_A1 0.4", {"vdw": {"VDW_A1": "0.4000"}}), ("VDW_RADIUS 95", {"vdw": {"VDW_RADIUS": "95.0000 A"}})):
            mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], **kw))
            ck(st(F_) == "SETTINGS_MISMATCH", f"⛔음성 R2 {why} → SETTINGS_MISMATCH")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], dipol_line=True, min_pos=None))
        ck(st(F_) == "OK", "DIPOL 해석값 줄만 있고 일치 → OK (min pos 없는 빌드)")
        # ⑥ CE P0-3 POTCAR · 버전
        mk(F_, drop=("POTCAR.sha256",))
        ck(st(F_) == "POTCAR_UNVERIFIED", "⛔음성 CE P0-3 POTCAR.sha256 삭제 → POTCAR_UNVERIFIED")
        mk(F_, titel=[t.replace("02Apr2005", "06Sep2000") for t in J[F_]["pp_expected_titel"]])
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 CE P0-3 TITEL 날짜 다름 → POTCAR_MISMATCH")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=[t.replace("Ag 02Apr2005", "Ag_pv 06Sep2000") for t in J[F_]["pp_expected_titel"]]))
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 CE P0-3 OUTCAR TITEL ≠ POTCAR.titel → POTCAR_MISMATCH")
        mk(F_)
        mk("V5_s_outer_A_bound", spsha={**SPSHA, "Ag": "f" * 64})
        rs_ = check(out, ret, msha)[1]
        ck(rs_[F_]["status"] == "POTCAR_INCONSISTENT" and check_exit(rs_) == 3, "⛔음성 CE P0-3 bound 만 다른 Ag sha → POTCAR_INCONSISTENT · 종료 3")
        mk("V5_s_outer_A_bound", psha_override="a" * 64)
        ck(st(F_) == "POTCAR_INCONSISTENT", "⛔음성 CE P0-3 종별 sha 는 같고 조립본 sha 만 다름 → POTCAR_INCONSISTENT")
        mk("V5_s_outer_A_bound")
        ck(st(F_, {**reg_ok, "species_sha256": {**reg_ok["species_sha256"], "Ag": "e" * 64}}) == "POTCAR_MISMATCH", "⛔음성 봉인 등록부와 다른 종별 sha → POTCAR_MISMATCH")
        mk("V5_s_outer_B_far", version="vasp.6.3.0 16May22 (build Jun 1 2022) complex")
        ck(st(F_) == "VERSION_INCONSISTENT", "⛔음성 잡 하나만 다른 VASP 빌드 → 전 배치 VERSION_INCONSISTENT")
        mk("V5_s_outer_B_far")
        ck(st(F_, {**reg_ok, "vasp_version": "vasp.6.5.1 other"}) == "VERSION_MISMATCH", "⛔음성 등록부와 다른 VASP 버전 → VERSION_MISMATCH")
        ck(st(F_, reg_ok) == "OK" and st(F_, {**reg_ok, "assembled_sha256": {_spec_key(J[F_]): "b" * 64}}) == "POTCAR_MISMATCH",
           "등록부 대조: 봉인값이면 OK · 조립본 sha 다르면 POTCAR_MISMATCH")
        # ⑦ CF P0-1 — 모순 + 실행 실패/미수렴 조합 (r1 이 덮으면 안 된다)
        for why, kw, reg, want_st in (("ENCUT 400 + rc 1", {"encut": 400.0, "rc": 1}, None, "SETTINGS_MISMATCH"),
                                      ("ENCUT 400 + 미수렴", {"encut": 400.0, "conv": False}, None, "SETTINGS_MISMATCH"),
                                      ("OUTCAR TITEL 다름 + rc 1", {"rc": 1, "titel_override": [t.replace("Ag 02Apr2005", "Ag_pv 06Sep2000") for t in J[F_]["pp_expected_titel"]]}, None, "POTCAR_MISMATCH"),
                                      ("등록부와 다른 Ag + rc 1", {"rc": 1, "spsha": {**SPSHA, "Ag": "f" * 64}}, reg_ok, "POTCAR_MISMATCH"),
                                      ("등록부와 다른 버전 + 미수렴", {"conv": False, "version": "vasp.6.5.1 other"}, reg_ok, "VERSION_MISMATCH"),
                                      ("Edisp 5 % + rc 1", {"rc": 1, "outcar": _fake_outcar(J[F_], E[F_], ED[F_] * 1.05)}, None, "D3_MISMATCH")):
            mk(F_, **kw); mk(F_, "r1")
            r7 = check(out, ret, msha, reg)[1][F_]
            ck(r7["status"] == want_st and "r1_ignored" in r7 and r7.get("conflicts"), f"⛔음성 CF P0-1 {why} + 정상 r1 → {want_st} (r1 승격 안 함) — {r7['status']}")
        mk(F_, rc=1, spsha={**SPSHA, "Ag": "f" * 64}); mk(F_, "r1")
        r7b = check(out, ret, msha)[1]
        ck(r7b[F_]["status"] == "POTCAR_INCONSISTENT" and r7b["V5_s_outer_A_bound"]["status"] == "POTCAR_INCONSISTENT",
           f"⛔음성 CF P0-1 등록부 없이: 버려진 첫 시도의 다른 Ag 도 시도 사이 일관성에서 잡힘 → POTCAR_INCONSISTENT — {r7b[F_]['status']}")
        shutil.rmtree(os.path.join(run, F_ + "_r1")); mk(F_)
        # ⑧ CE P0-4 UMA
        u_nan = json.loads(json.dumps(uma))
        for v in u_nan["energies"].values():
            v["E_UMA_eV"] = float("nan")
        rr = C(u_nan)
        ck(rr["G5"]["status"].startswith("BLOCKED (UMA") and collect_exit(rr) == 11 and rr["G5"]["usage_eligible"] is False, f"⛔음성 CE P0-4 UMA 전부 NaN → BLOCKED — {rr['G5']['status']}")
        json.dumps(rr, allow_nan=False)
        for mut, why in ((lambda u: u["calculator"].update({"checkpoint": [{"sha256": "0" * 64}]}), "체크포인트 sha"),
                         (lambda u: u["calculator"].update({"task": "omol"}), "task"), (lambda u: u["calculator"].update({"fairchem.core": "1.0.0"}), "버전"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"sha256": "1" * 64}), "구조 sha"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"pbc": [True, True, False]}), "pbc"),
                         (lambda u: u["energies"]["V5_s_outer_B_far"].update({"E_UMA_eV": True}), "bool 에너지"),
                         (lambda u: u["energies"].update({"x/V5_s_outer_B_far": dict(u["energies"]["V5_s_outer_B_far"])}), "이름 중복")):
            u = json.loads(json.dumps(uma)); mut(u)
            ck(C(u)["G5"]["status"].startswith("BLOCKED (UMA"), f"⛔음성 CE P0-4 UMA {why} 틀림 → BLOCKED")
        # ⑨ CF P0-2 — 등록부 없거나 틀리면 최종 사용 판정이 안 열린다
        rn = C(reg=None)
        ck(rn["G5"]["status"].startswith("BLOCKED (PP 등록부") and rn["G5"]["usage_eligible"] is False and collect_exit(rn) == 11
           and not any(s["total_w_citable"] for s in rn["samples"].values()) and rn["pp_registry"]["state"].startswith("없음"),
           f"⛔음성 CF P0-2 등록부 없이 집계 → G5 BLOCKED · usage false · total W 인용 불가 · 종료 11 — {rn['G5']['status']}")
        bads = {"빈 객체": {}, "schema": {**reg_ok, "schema": "nonsense"}, "MANIFEST": {**reg_ok, "package_manifest_sha256": "0" * 64},
                "버전 없음": {k: v for k, v in reg_ok.items() if k != "vasp_version"}, "조립본 없음": {k: v for k, v in reg_ok.items() if k != "assembled_sha256"},
                "run_id": {**reg_ok, "from_pilot": {PILOT_JOBS[0]: "x", PILOT_JOBS[1]: reg_ok["from_pilot"][PILOT_JOBS[1]]}},
                "TITEL": {**reg_ok, "titel": {**reg_ok["titel"], "Ag": "PAW_PBE Ag 06Sep2000"}}, "pp_set": {**reg_ok, "pp_set": "PBE_64"},
                "파일럿 sha 없음 (v2 등록부)": {k: v for k, v in reg_ok.items() if k != "from_pilot_sha256"},
                "파일럿 sha 형식": {**reg_ok, "from_pilot_sha256": {**reg_ok["from_pilot_sha256"], PILOT_JOBS[1]: {"attempt.json": "x", "OUTCAR": "y"}}}}
        for why, rg in bads.items():
            ck(raises(lambda rg=rg: check(out, ret, msha, rg)) and raises(lambda rg=rg: collect(out, ret, msha, uma, rg, "f" * 64)),
               f"⛔음성 CF P0-2 틀린 등록부({why}) → 검사·집계 시작 안 함 (PkgError)")
        up = os.path.join(T, "uma.json"); _write(up, json.dumps(uma))
        rgp = os.path.join(T, "reg.json"); _write(rgp, json.dumps(reg_ok, ensure_ascii=False))
        erp = os.path.join(T, "empty.json"); _write(erp, "{}")
        base_cli = [sys.executable, os.path.abspath(__file__), "--collect", "--out", out, "--ret", ret, "--manifest_sha256", msha, "--uma", up]
        cli = lambda extra: subprocess.run(base_cli + extra, capture_output=True, text=True, timeout=300).returncode
        ck(cli([]) == 2 and cli(["--pp_registry", erp, "--pp_registry_sha256", _sha(erp)]) == 2 and cli(["--pilot"]) == 11
           and cli(["--pp_registry", rgp, "--pp_registry_sha256", _sha(rgp)]) == 0 and cli(["--pp_registry", rgp, "--pp_registry_sha256", "0" * 64]) == 2,
           "CLI: 등록부 없음 → 2 · 빈 등록부(해시 맞음) → 2 · --pilot → 11 · 봉인 등록부 → 0 · 해시 틀림 → 2")
        # ⑩ CE P1-1 승인본
        inc = os.path.join(out, "jobs", F_, "INCAR"); orig = open(inc).read()
        _write(inc, orig.replace("ENCUT = 520.0", "ENCUT = 400.0")); mk(F_, incar=orig.replace("ENCUT = 520.0", "ENCUT = 400.0"))
        ck(raises(lambda: check(out, ret, msha)), "⛔음성 CE P1-1 기대·반송 INCAR 동시 변조 → 시작 안 함")
        _write(inc, orig); mk(F_)
        ck(raises(lambda: check(out, ret, "0" * 64)), "⛔음성 CE P1-1 틀린 고정값 → 시작 안 함")
        jobs_path = os.path.join(out, "jobs.json"); keep = open(jobs_path).read()
        jj = json.loads(keep); jj["jobs"][0]["d3_2body_eV_ref"] = None; _write(jobs_path, json.dumps(jj))
        ck(raises(lambda: check(out, ret, msha)), "⛔음성 D3 기대값 None 으로 바꾼 jobs.json → 승인본 대조에서 막힘")
        _write(jobs_path, keep)
        # ⑪ CE P1-2 결측 · CF P1-1 마지막 레코드 · 종료코드
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], drop=("NELECT",)))
        ck(st(F_) == "SYSTEM_UNVERIFIED", "⛔음성 CE P1-2 NELECT 줄 없음 → SYSTEM_UNVERIFIED")
        mk(F_, edisp=False)
        ck(st(F_) == "D3_UNVERIFIED", "⛔음성 Edisp 없음 → D3_UNVERIFIED")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_] * 1.05))
        ck(st(F_) == "D3_MISMATCH", "⛔음성 Edisp 5 % 차 → D3_MISMATCH")
        for why, kw in (("최종 TOTEN NaN", {"final_toten": "NaN"}), ("최종 TOTEN 별표", {"final_toten": "**************"}),
                        ("유한 TOTEN 뒤 마지막 TOTEN NaN", {"extra_final_toten": "NaN"}), ("최종 구획 없음 (SCF 단계 값만)", {"final_block": False})):
            mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], **kw))
            ck(st(F_) == "ENERGY_UNPARSEABLE", f"⛔음성 CF P1-1 {why} → ENERGY_UNPARSEABLE (앞 값으로 안 돌아감)")
        mk(F_)
        empty = os.path.join(T, "empty"); os.makedirs(empty)
        ck(check_exit(check(out, empty, msha)[1]) == 3, "⛔음성 CE P1-2 빈 반송 → 종료코드 3 (0 아님)")
        # ⑫ CE P1-3 r1 자격 (정당한 r1 경로 보존)
        B_ = "V5_s_outer_B_far"
        def break_poscar(d):
            _write(os.path.join(d, "POSCAR"), "x\n"); edit_attempt(d, sha256={**json.load(open(os.path.join(d, "attempt.json")))["sha256"], "POSCAR": _sha(os.path.join(d, "POSCAR"))})
        mk(B_, tamper_after=break_poscar); mk(B_, "r1")
        r9 = check(out, ret, msha)[1][B_]
        ck(r9["status"] == "INPUT_MODIFIED" and "r1_ignored" in r9, f"⛔음성 CE P1-3 첫 시도 INPUT_MODIFIED + 정상 r1 → 승격 안 함 — {r9['status']}")
        shutil.rmtree(os.path.join(run, B_))
        ck(st(B_) == "MISSING", "⛔음성 CE P1-3 첫 시도 없는 r1 → 채택 안 함 (MISSING)")
        for why, kw, fa in (("미수렴", {"conv": False}, "SCF_NOT_CONVERGED"), ("OUTCAR 없이 rc 1", {"rc": 1, "no_out": True}, "EXECUTION_FAILED"),
                            ("rc 0 인데 OUTCAR 없음", {"rc": 0, "no_out": True}, "NOT_TERMINATED"), ("정상 OUTCAR 인데 rc 1", {"rc": 1}, "EXECUTION_FAILED")):
            mk(B_, **kw)
            r9x = check(out, ret, msha, reg_ok)[1][B_]
            ck(r9x["status"] == "OK" and r9x["attempt"] == "r1" and r9x.get("first_attempt") == fa, f"정당한 r1 채택 ({why} · 등록부 있음) — {r9x['status']} {r9x.get('first_attempt')}")
        shutil.rmtree(os.path.join(run, B_ + "_r1")); mk(B_)
        # ⑬ CE P1-4 D3 예산 (운영 예산)
        G_ = G3_JOBS[2]
        mk(G_, outcar=_fake_outcar(J[G_], E[G_] + dE(0.0015), ED[G_] + dE(0.0015)))
        r10 = C()
        ck(r10["G3"]["status"].startswith("INCOMPLETE (D3") and r10["G5"]["status"].startswith("INCOMPLETE (G3") and r10["G5"]["usage_eligible"] is False,
           f"⛔음성 CE P1-4 G3 차이의 차이 0.0015 > 0.001 → G3 INCOMPLETE (D3) → G5 오차표만 — {r10['G3']['status']} / {r10['G5']['status']}")
        mk(G_)
        mk(B_, outcar=_fake_outcar(J[B_], E[B_] + dE(0.008), ED[B_] + dE(0.008)))
        r11 = C()
        ck(r11["samples"]["②"]["d3_pair_over_budget"] is True and abs(r11["samples"]["②"]["d3_pair_err_J_m2"] - 0.008) < 2e-6 and r11["samples"]["②"]["W_label"]
           and r11["samples"]["②"]["total_w_citable"] is False and r11["samples"]["①"]["total_w_citable"] is True
           and abs(r11["G5"]["Delta_J_m2"]["②"] - 0.01) < 2e-6,
           f"⛔음성 CE P1-4 표본 ② 쌍 오차 0.008 > 0.005 → total W 인용 불가 (라벨) · G5 Δ 불변 — {r11['samples']['②'].get('d3_pair_err_J_m2')}")
        mk(B_)
        # ⑭ CF P0-3 — G4 의 D3 불일치가 수치 수렴 실패를 가리면 안 된다
        G4f, G4b = "V5_s_outer_A_G4_e70_far", "V5_s_outer_A_G4_e70_bound"
        e_true = E[G4b] + dE(0.521)
        mk(G4f, outcar=_fake_outcar(J[G4f], e_true, ED[G4f]))
        r12a = C()
        ck(r12a["G4"]["e70"]["status"] == "FAIL" and r12a["G4"]["status"] == "FAIL" and r12a["G5"]["usage_eligible"] is False,
           f"CF P0-3 기준: G4 e70 ΔW 0.021 → FAIL — {r12a['G4']['e70']}")
        err = dE(-0.002)
        mk(G4f, outcar=_fake_outcar(J[G4f], e_true + err, ED[G4f] + err))
        r12b = C()
        ck(r12b["G4"]["e70"]["status"].startswith("INCOMPLETE (D3 불일치") and r12b["G4"]["status"] == "INCOMPLETE" and r12b["G5"]["status"] != "PASS"
           and r12b["G5"]["usage_eligible"] is False and collect_exit(r12b) == 11,
           f"⛔음성 CF P0-3 far 의 TOTEN·Edisp 에 같은 {err:.5f} eV (1 % 검사 통과) → e70 INCOMPLETE (D3 불일치) · G5 안 열림 — {r12b['G4']['e70']['status']} / {r12b['G5']['status']}")
        mk(G4f)
        # ⑮ 3c · G5 순서 · 누락 · 미평가
        E_bak = E[G_]; E[G_] = E[G3_JOBS[0]] + dE(0.512); mk(G_)
        r13 = C()
        ck(r13["G3"]["status"] == "FAIL" and r13["G5"]["status"] == "INCOMPLETE (G3 FAIL · G4 PASS — 오차표만 · 원시 기준 충족)"
           and r13["G5"]["raw_error_criteria_met"] is True and r13["G5"]["usage_eligible"] is False and collect_exit(r13) == 11,
           f"3c: G3 FAIL → INCOMPLETE (오차표만 · 원시 기준 충족) · 사용 자격 없음 — {r13['G5']['status']}")
        u3 = json.loads(json.dumps(uma)); u3["energies"]["V5_li_outer_A_far"]["E_UMA_eV"] -= dE(0.15)
        r13b = C(u3)
        ck(r13b["G5"]["status"] == "INCOMPLETE (G3 FAIL · G4 PASS — 오차표만 · 원시 기준 미충족)" and r13b["G5"]["raw_error_criteria_met"] is False,
           f"R4 순서: G3 FAIL + 원시 FAIL → INCOMPLETE (원시 기준 미충족 병기) — {r13b['G5']['status']}")
        E[G_] = E_bak; mk(G_)
        r14 = C(u3)
        ck(r14["G5"]["status"] == "FAIL" and collect_exit(r14) == 10, f"⛔음성 G3·G4 PASS 에서 표본 ③ |Δ| 0.17 → FAIL (종료 10) — {r14['G5']['status']}")
        os.remove(os.path.join(run, "V5_li_outer_B_bound", "OUTCAR"))
        r15 = C()
        ck(collect_exit(r15) == 3 and r15["G5"]["status"].startswith("INCOMPLETE (분모"), f"⛔음성 표본 누락 → 종료 3 · INCOMPLETE (분모 5) — {r15['G5']['status']}")
        mk("V5_li_outer_B_bound")
        ck(collect_exit(C(None)) == 12, "UMA 없음 → 종료 12 (G5 미평가)")
        # ⑯ 3b′ 진단 (G3 세 구조 UMA 가 있을 때만 · 판정 아님)
        u4 = json.loads(json.dumps(uma))
        for g in G3_JOBS:
            u4["energies"][g] = row(g, 0.0)
        u4["energies"][G_]["E_UMA_eV"] = dE(0.509 - (REF[G_] - REF[G3_JOBS[0]]) * EV_J / (A * A2_M2) - 0.01 - 0.03)
        r16 = C(u4)
        dg = r16["G5"].get("residual_endpoint_diag_3b_prime", {}).get("dDelta_J_m2", {})
        ck(dg.get("ii") is not None and abs(dg["ii"] - 0.03) < 1e-6 and r16["G5"]["status"] == "PASS", f"3b′: δΔ(ii) = +0.03 기록 · 판정 불변 — {dg} {r16['G5']['status']}")
        # ⑰ seal_pp 음성
        mk(F_, rc=1)
        ck(raises(lambda: seal_pp(out, ret, msha)), "⛔음성 파일럿이 OK 가 아닌데 등록부를 만들었다")
        mk(F_, tamper_after=lambda d: edit_attempt(d, run_id=None))
        ck(raises(lambda: seal_pp(out, ret, msha)), "⛔음성 파일럿 run_id 없으면 등록부를 안 만든다 (연결 정보 필수)")
        mk(F_)
        # ⑲ CG P1-2 · 권고 3 — 봉인 파일럿 결속: 최종 검사·집계에서 파일럿 채택 시도의 run_id · attempt.json/OUTCAR sha 가 등록부와 같아야 한다
        sealed_id = reg_ok["from_pilot"][F_]
        mk(F_, tamper_after=lambda d: edit_attempt(d, run_id="20260928T120000-99-456"))
        r19 = check(out, ret, msha, reg_ok)[1][F_]
        ck(r19["status"] == "PILOT_NOT_SEALED" and "run_id" in r19["why"] and st(F_) == "OK",
           f"⛔음성 CG P1-2 반송 파일럿의 run_id 를 다음 날 실행 ID 로 교체 → PILOT_NOT_SEALED (등록부 없이는 OK 인 정상 출력 · 리뷰어 재현: PASS 였다) — {r19['status']}")
        rr19 = C()
        ck(collect_exit(rr19) == 3 and F_ in rr19["jobs_not_ok"] and rr19["G5"]["usage_eligible"] is False and rr19["G5"]["status"].startswith("INCOMPLETE (분모")
           and rr19["samples"]["①"]["total_w_citable"] is False,
           f"⛔음성 CG P1-2 교체된 파일럿으로 집계 → 종료 3 · 사용 자격 없음 · ① 인용 불가 — {rr19['G5']['status']}")
        ck(cli(["--pp_registry", rgp, "--pp_registry_sha256", _sha(rgp)]) == 3, "⛔음성 CG P1-2 실제 CLI --collect + 봉인 등록부 + 교체된 파일럿 run_id → 종료 3 (리뷰어 재현: 0 이었다)")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_] - 0.001, ED[F_]), tamper_after=lambda d: edit_attempt(d, run_id=sealed_id))
        r19b = check(out, ret, msha, reg_ok)[1][F_]
        ck(r19b["status"] == "PILOT_NOT_SEALED" and "sha" in r19b["why"], f"⛔음성 CG 권고 3 같은 run_id 인데 OUTCAR·attempt.json 이 봉인 뒤 바뀜 → PILOT_NOT_SEALED — {r19b['status']}")
        mk(F_)
        rs19 = check(out, ret, msha, reg_ok)[1]
        ck(rs19[F_]["status"] == "OK" and rs19[PILOT_JOBS[0]]["status"] == "OK" and collect_exit(C()) == 0, "봉인 그대로의 파일럿 두 잡 → OK · 집계 종료 0 (결속 양성 경로)")
        mk(F_, conv=False); mk(F_, "r1")
        reg_r1 = seal_pp(out, ret, msha)
        r19c = check(out, ret, msha, reg_r1)[1][F_]
        ck(reg_r1["from_pilot"][F_].endswith("1") and r19c["status"] == "OK" and r19c["attempt"] == "r1" and r19c.get("first_attempt") == "SCF_NOT_CONVERGED",
           f"정당한 r1 로 봉인한 파일럿 → 최종 검사에서 r1 채택 · 결속 OK (r1 재사용 양성 경로 유지) — {r19c['status']}")
        ck(check(out, ret, msha, reg_ok)[1][F_]["status"] == "PILOT_NOT_SEALED", "⛔음성 첫 시도로 봉인한 등록부인데 r1 이 채택된 파일럿 → PILOT_NOT_SEALED")
        shutil.rmtree(os.path.join(run, F_ + "_r1")); mk(F_)
        # ⑳ CG P1-3 — 미완료 출력의 정상 TITEL 접두 = 결측 (r1 자격) · 성공 시도의 접두만 = 미검증 · 다른 종·날짜·순서·추가 = 모순
        tl = J[F_]["pp_expected_titel"]
        mk(F_, rc=1, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:1], term=False)); mk(F_, "r1")
        r20 = check(out, ret, msha)[1][F_]
        ck(r20["status"] == "OK" and r20["attempt"] == "r1" and r20.get("first_attempt") == "EXECUTION_FAILED" and "r1_ignored" not in r20,
           f"CG P1-3 올바른 첫 TITEL 만 찍히고 rc 1 (미종료) + 정상 r1 → r1 채택 (리뷰어 재현: POTCAR_MISMATCH 였다) — {r20['status']} {r20.get('why')}")
        mk(F_, rc=1, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:3], term=False))
        r20a = check(out, ret, msha)[1][F_]
        ck(r20a["status"] == "OK" and r20a["attempt"] == "r1", "CG P1-3 TITEL 셋까지 찍힌 미완료 + 정상 r1 → r1 채택")
        for why, tov in (("순서 바뀜", [tl[1], tl[0]]), ("첫 TITEL 날짜 다름", [tl[0].replace("10Sep2004", "06Sep2000")]),
                         ("둘째 TITEL 종 다름", [tl[0], tl[1].replace("P 06Sep2000", "P_h 06Sep2000")]),
                         ("기대 전부 뒤에 다른 종 추가", tl + ["PAW_PBE Fe 06Sep2000"]), ("다른 종 하나", ["PAW_PBE Fe 06Sep2000"])):
            mk(F_, rc=1, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tov, term=False))
            r20b = check(out, ret, msha)[1][F_]
            ck(r20b["status"] == "POTCAR_MISMATCH" and "r1_ignored" in r20b and r20b.get("conflicts"),
               f"⛔음성 CG P1-3 미완료 출력의 TITEL {why} + 정상 r1 → POTCAR_MISMATCH (접두 아님 = 모순 · r1 승격 안 함) — {r20b['status']}")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:2]))
        r20c = check(out, ret, msha)[1][F_]
        ck(r20c["status"] == "POTCAR_UNVERIFIED" and "r1_ignored" in r20c,
           f"⛔음성 CG P1-3 성공 시도(rc 0 · 종료 · 수렴)인데 TITEL 접두만 + 정상 r1 → POTCAR_UNVERIFIED · 승격 안 함 (미검증은 재시도 자격이 아니다) — {r20c['status']}")
        # CI S3 — 잘린 마지막 TITEL 줄: 모순 확정이 아니라 자동 확인 불가 (TITEL_TRUNCATED · 통과·r1 자격 없음 · 설명 포함)
        mk(F_, rc=1, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:2] + [tl[2][:12]], term=False))
        r20d = check(out, ret, msha)[1][F_]
        ck(r20d["status"] == "TITEL_TRUNCATED" and "r1_ignored" in r20d and "자동 확인 불가" in r20d["why"] and r20d.get("conflicts"),
           f"⛔음성 CI S3 마지막 TITEL 이 잘린 줄 ({tl[2][:12]!r}) + rc 1 + 정상 r1 → TITEL_TRUNCATED (모순 확정 아님 · 승격 안 함 · 설명) — {r20d['status']} {r20d.get('why', '')[:80]}")
        mk(F_, rc=1, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=[tl[0], "PAW_PBE S"], term=False))
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 CI S3 잘린 문자열이라도 그 자리의 기대 종(P)이 아니면(S) → POTCAR_MISMATCH (모순)")
        shutil.rmtree(os.path.join(run, F_ + "_r1"))
        ck(st(F_) == "POTCAR_MISMATCH", "⛔음성 CI S3 r1 없이도 POTCAR_MISMATCH")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:2] + [tl[2][:12]]))
        ck(st(F_) == "TITEL_TRUNCATED", "⛔음성 CI S3 성공 시도(rc 0 · 종료)인데 마지막 TITEL 잘림 → TITEL_TRUNCATED (통과 아님)")
        mk(F_, outcar=_fake_outcar(J[F_], E[F_], ED[F_], titel_override=tl[:2]))
        ck(st(F_) == "POTCAR_UNVERIFIED", "⛔음성 CG P1-3 성공 시도의 TITEL 접두만 (r1 없이) → POTCAR_UNVERIFIED (통과 아님)")
        mk(F_)
        # ⑱ 배포 러너 실제 실행 (가짜 VASP · bash) — 러너와 검사기가 같은 규칙을 쓰는지
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
            shim = os.path.join(T, "shim"); os.makedirs(shim); _write(os.path.join(shim, "tar"), "#!/usr/bin/env bash\necho SHIM_TAR_FAIL >&2\nexit 73\n")
            os.chmod(os.path.join(shim, "tar"), 0o755)
            def run_pkg(tag, vasp_cmd, mode="ok", perf_file=perf, fresh=True, extra_env=None):
                w = os.path.join(T, f"w_{tag}")
                if fresh:
                    shutil.copytree(out, w)
                env = {**os.environ, "VASP_CMD": vasp_cmd, "POTCAR_DIR": potdir, "JOBS": " ".join(PILOT_JOBS), "FAKE_TOOLDIR": HERE, "FAKE_PKG": out, "FAKE_MODE": mode}
                if perf_file is not None:
                    env["PERF_TAGS_FILE"] = perf_file
                env.update(extra_env or {})
                p = subprocess.run(["bash", os.path.join(w, "run_all.sh")], env=env, capture_output=True, text=True, timeout=300)
                return w, p.returncode, p.stdout + p.stderr
            py = f"{sys.executable} {fake}"
            w, rcode, log = run_pkg("ok", py)
            rs = check(out, w, msha)[1]
            ck(rcode == 0 and all(rs[p]["status"] == "OK" for p in PILOT_JOBS) and check_exit(rs) == 3 and os.path.isfile(os.path.join(w, "V5_vasp_return.tgz")),
               f"러너 실행: 파일럿 2 잡 성공 · 검사 OK (나머지 16 잡 MISSING → 종료 3) — rc {rcode} {[(p, rs[p]['status'], rs[p].get('why')) for p in PILOT_JOBS]} {log[-300:]}")
            rmi = return_manifest_info(w, msha)
            ck(rmi["present"] and rmi["matches_pinned"] and rmi["forbidden_files"] == [], f"반송 묶음의 MANIFEST = 고정값 · 반송 폴더에 금지 파일 없음 (러너가 지움) — {rmi}")
            import tarfile
            members = lambda wd: tarfile.open(os.path.join(wd, "V5_vasp_return.tgz")).getnames()
            forb = lambda ms: [m for m in ms if m.rsplit("/", 1)[-1] in RETURN_FORBIDDEN]
            m0 = members(w)
            ck(not forb(m0) and all(f"run/{PILOT_JOBS[0]}/{x}" in m0 for x in ("attempt.json", "OUTCAR", "OSZICAR", "INCAR", "POTCAR.titel", "POTCAR.species.sha256", "stdout.log", "IBZKPT"))
               and "run/status.tsv" in m0 and "run/env.txt" in m0 and "MANIFEST.sha256" in m0 and not any(m.endswith("/EIGENVAL") for m in m0),
               f"CG P1-1 러너 정상 실행: 묶음은 허용 목록만 (가짜 VASP 가 쓴 WAVECAR·CHGCAR·CHG·vasprun.xml·EIGENVAL 없음 · IBZKPT 는 있음) — {sorted(m0)[:6]}")
            ck(subprocess.run(["sha256sum", "-c", "--quiet", "V5_vasp_return.tgz.sha256"], cwd=w, capture_output=True).returncode == 0,
               "CG 권고 2: .sha256 은 최종 파일명으로 쓰여 sha256sum -c 가 그대로 통과")
            wreg = seal_pp(out, w, msha)
            ck(not validate_pp_registry(wreg, msha, meta) and all(RUN_ID_RE.match(v) for v in wreg["from_pilot"].values()), "러너 산출물로 등록부 봉인 (실제 run_id 형식)")
            rsw = check(out, w, msha, wreg)[1]
            ck(all(rsw[p]["status"] == "OK" for p in PILOT_JOBS), f"러너 산출물 + 그 등록부 → 파일럿 두 잡 결속 OK — {[(p, rsw[p]['status']) for p in PILOT_JOBS]}")
            potpart = os.path.join(T, "potcars_partial"); os.makedirs(os.path.join(potpart, "Li_sv"))
            shutil.copy(os.path.join(potdir, "Li_sv", "POTCAR"), os.path.join(potpart, "Li_sv", "POTCAR"))
            w10, rcode10, log10 = run_pkg("pp_partial", py, extra_env={"POTCAR_DIR": potpart})
            m10 = members(w10)
            ck(rcode10 == 1 and "준비 실패" in log10 and not forb(m10) and f"run/{PILOT_JOBS[0]}/INCAR" in m10 and f"run/{PILOT_JOBS[0]}/POTCAR.species.sha256" in m10
               and "run/status.tsv" in m10 and not os.path.isfile(os.path.join(w10, "run", PILOT_JOBS[0], "POTCAR")) and "✅" not in log10,
               f"⛔음성 CG P1-1 PP 트리에 Li_sv 만 → 준비 실패(종료 1)인데 묶음에 부분 POTCAR 본문 없음 · 폴더의 부분 POTCAR 도 지움 (리뷰어 재현: 들어갔다) — rc {rcode10} {forb(m10)}")
            leak = ("POTCAR", "WAVECAR", "CHGCAR", "vasprun.xml")
            for x in leak:
                _write(os.path.join(w, "run", PILOT_JOBS[1], x), "LEAK_DO_NOT_SHIP\n")
            _, rcode11, log11 = run_pkg("ok", "false", fresh=False, perf_file=None, extra_env={"PACK_ONLY": "1"})
            m11 = members(w)
            ck(rcode11 == 0 and not forb(m11) and f"run/{PILOT_JOBS[1]}/attempt.json" in m11 and f"run/{PILOT_JOBS[1]}/OUTCAR" in m11
               and return_manifest_info(w, msha)["forbidden_files"] == sorted(f"run/{PILOT_JOBS[1]}/{x}" for x in leak),
               f"⛔음성 CG P1-1 중단 뒤 POTCAR·WAVECAR·CHGCAR·vasprun.xml 이 남은 폴더에 PACK_ONLY=1 → 묶음에 없음 (검사기는 폴더의 금지 파일을 보고) (리뷰어 재현: 들어갔다) — rc {rcode11} {forb(m11)}")
            for x in leak:
                os.remove(os.path.join(w, "run", PILOT_JOBS[1], x))
            # ㉑ CI P1 — 포장 단계의 외부 명령 실패는 종료 4 · '✅' 없음 · 기존 tgz/sha 쌍 보존 · .part 없음 (리뷰어 방식 그대로: BASH_ENV 함수 주입 · 제품 러너 무수정)
            pair = lambda wd: (_sha(os.path.join(wd, "V5_vasp_return.tgz")), open(os.path.join(wd, "V5_vasp_return.tgz.sha256")).read())
            before = pair(w)
            for why, inj in (("find 실패(73)", 'find(){ echo INJ_FIND >&2; return 73; }\n'), ("sort 실패(73)", 'sort(){ echo INJ_SORT >&2; return 73; }\n'),
                             ("grep 오류(2)", 'grep(){ return 2; }\n'), ("grep 오류(2) — 구성원 금지 검사만", 'grep(){ case "$*" in *members*) return 2;; esac; command grep "$@"; }\n'),
                             ("grep 오류(2) — 허용 목록 필터만", 'grep(){ case "$*" in *found*) return 2;; esac; command grep "$@"; }\n'),
                             ("sort 실패 — 허용 목록 정렬만 (뒤 정렬은 정상)", 'sort(){ case "$*" in *allowed*) echo INJ_SORT1 >&2; return 73;; esac; command sort "$@"; }\n'),
                             ("tar tzf 만 실패", 'tar(){ if [ "$1" = tzf ]; then echo INJ_TAR_T >&2; return 73; fi; command tar "$@"; }\n'),
                             ("tar tzf 가 목록은 다 찍고 73 으로 끝남", 'tar(){ if [ "$1" = tzf ]; then command tar "$@"; return 73; fi; command tar "$@"; }\n'),
                             ("cmp 불일치(구성원↔목록)", 'cmp(){ return 1; }\n'), ("sha256sum 빈 출력", 'sha256sum(){ :; }\n'),
                             ("두 번째 mv 실패", 'mv(){ case "$1$2" in *sha256.part*) return 1;; esac; command mv "$@"; }\n')):
                inj_f = os.path.join(T, "inject.sh"); _write(inj_f, inj)
                _, rc_i, log_i = run_pkg("ok", "false", fresh=False, perf_file=None, extra_env={"PACK_ONLY": "1", "BASH_ENV": inj_f})
                if why.startswith("두 번째 mv"):
                    ck(rc_i == 4 and "✅" not in log_i and pair(w)[1] == before[1] and not os.path.exists(os.path.join(w, "V5_vasp_return.tgz.part")),
                       f"CI S5 PACK_ONLY 에서 {why} 주입 → 종료 4 · '✅' 없음 · 옛 sha 그대로 (새 tgz + 옛 sha 가 남는 선언된 틈 — sha256sum -c 가 잡는다) — rc {rc_i}")
                    ck(subprocess.run(["sha256sum", "-c", "--quiet", "V5_vasp_return.tgz.sha256"], cwd=w, capture_output=True).returncode != 0,
                       "CI S5 그 상태의 쌍은 sha256sum -c 가 실패한다 (발송 조건 = 종료 0 + sha256sum -c 통과)")
                    _, rc_fix, _ = run_pkg("ok", "false", fresh=False, perf_file=None, extra_env={"PACK_ONLY": "1"})
                    ck(rc_fix == 0 and subprocess.run(["sha256sum", "-c", "--quiet", "V5_vasp_return.tgz.sha256"], cwd=w, capture_output=True).returncode == 0, "PACK_ONLY 재시도로 쌍 복구")
                    before = pair(w)
                    continue
                ck(rc_i == 4 and "✅" not in log_i and pair(w) == before and not any(os.path.exists(os.path.join(w, f"V5_vasp_return.tgz{x}")) for x in (".part", ".sha256.part")),
                   f"⛔음성 CI P1 PACK_ONLY 에서 {why} 주입 → 종료 4 · '✅' 없음 · 기존 tgz/sha 쌍 보존 · .part 없음 (리뷰어 재현: 종료 0 · 관리 파일 3 개 묶음) — rc {rc_i} {log_i[-100:]}")
            _, rc_ok, _ = run_pkg("ok", "false", fresh=False, perf_file=None, extra_env={"PACK_ONLY": "1"})
            ck(rc_ok == 0 and len(members(w)) == len(m0) and not forb(members(w)), "주입 없는 PACK_ONLY 는 그대로 종료 0 · 구성원 수 불변 (양성 경로)")
            w12 = os.path.join(T, "w_empty_run"); shutil.copytree(out, w12); os.makedirs(os.path.join(w12, "run")); _write(os.path.join(w12, "run", "env.txt"), "x\n")
            p12 = subprocess.run(["bash", os.path.join(w12, "run_all.sh")], env={**os.environ, "PACK_ONLY": "1"}, capture_output=True, text=True, timeout=300)
            m12 = members(w12) if os.path.isfile(os.path.join(w12, "V5_vasp_return.tgz")) else None
            ck(p12.returncode == 0 and m12 is not None and sorted(m12) == ["MANIFEST.sha256", "run/env.txt"],
               f"CI P1 잡 파일이 하나도 없는 run/ 의 PACK_ONLY → grep 정상 무매치(1)는 오류가 아니다 · 관리 파일만 포장 · 종료 0 — rc {p12.returncode} {m12} {p12.stdout[-80:]}")
            rp = os.path.join(HERE, "..", "..", "db", "raw", "codex_CI_repro_2026_09_27", "repro_pack_ci.sh")
            if os.path.isfile(rp):
                p13 = subprocess.run(["bash", rp, out], capture_output=True, text=True, timeout=300)
                ck(p13.returncode == 0 and "runner exit = 4" in p13.stdout, f"리뷰어 CI 최소 재현 스크립트(repro_pack_ci.sh · find 주입) 그대로 → 종료 0 (= 고쳐짐) — rc {p13.returncode} {p13.stdout[-120:]}")
            else:
                print("  ⚠ SKIP 리뷰어 repro_pack_ci.sh 없음 — 통과로 세지 않는다")
            _, rcode2, log2 = run_pkg("ok", py, fresh=False)
            rs2 = check(out, w, msha)[1]
            ck(rcode2 == 1 and "이미 있거나" in log2 and all(rs2[p]["status"] == "OK" for p in PILOT_JOBS), f"⛔음성 러너 재실행: 기존 시도 폴더 거부(원자적 mkdir) · 종료 1 · 앞 결과 보존 — rc {rcode2}")
            w3, rcode3, _ = run_pkg("false", "false")
            rs3 = check(out, w3, msha)[1]
            ck(rcode3 == 1 and all(rs3[p]["status"] == "EXECUTION_FAILED" and rs3[p].get("r1") == "EXECUTION_FAILED" for p in PILOT_JOBS),
               f"⛔음성 러너 VASP_CMD=false → 종료 1 · EXECUTION_FAILED (r1 도) — rc {rcode3}")
            w4, rcode4, _ = run_pkg("badperf", py, perf_file=badperf)
            ck(rcode4 == 2 and not any(os.path.isdir(os.path.join(w4, "run", p)) for p in PILOT_JOBS), f"⛔음성 러너 성능 파일 우회 → 종료 2 · 아무것도 안 돎 — rc {rcode4}")
            _, rcode5, _ = run_pkg("noperf", py, perf_file=os.path.join(T, "없는_파일.txt"))
            ck(rcode5 == 2, f"⛔음성 러너 읽을 수 없는 성능 파일 → 종료 2 — rc {rcode5}")
            w6, rcode6, _ = run_pkg("rescue", py, mode="noconv_unless_amix")
            rs6 = check(out, w6, msha)[1]
            ck(rcode6 == 0 and all(rs6[p]["status"] == "OK" and rs6[p]["attempt"] == "r1" and rs6[p]["first_attempt"] == "SCF_NOT_CONVERGED" for p in PILOT_JOBS),
               f"러너 r1: 첫 시도 미수렴 → 사전등록 재시도 성공 · 검사 OK(r1) — rc {rcode6}")
            w7, rcode7, _ = run_pkg("rc1", py, mode="rc1")
            rs7 = check(out, w7, msha)[1]
            ck(rcode7 == 1 and all(rs7[p]["status"] == "EXECUTION_FAILED" for p in PILOT_JOBS), f"⛔음성 러너 정상 OUTCAR 인데 rc 1 → 종료 1 · EXECUTION_FAILED — rc {rcode7}")
            w8, rcode8, log8 = run_pkg("tarfail", py, extra_env={"PATH": shim + os.pathsep + os.environ.get("PATH", "")})
            n_status = len(open(os.path.join(w8, "run", "status.tsv")).read().splitlines())
            ck(rcode8 == 4 and "✅ 끝" not in log8 and not os.path.isfile(os.path.join(w8, "V5_vasp_return.tgz")) and all(check(out, w8, msha)[1][p]["status"] == "OK" for p in PILOT_JOBS),
               f"⛔음성 CF P1-3 러너 tar 실패 → 종료 4 · '✅ 끝' 없음 · tgz 없음 · 계산 결과는 보존 — rc {rcode8}")
            _, rcode9, log9 = run_pkg("tarfail", "false", fresh=False, perf_file=None, extra_env={"PACK_ONLY": "1"})
            ck(rcode9 == 0 and os.path.isfile(os.path.join(w8, "V5_vasp_return.tgz")) and os.path.isfile(os.path.join(w8, "V5_vasp_return.tgz.sha256"))
               and len(open(os.path.join(w8, "run", "status.tsv")).read().splitlines()) == n_status and not os.path.exists(os.path.join(w8, "V5_vasp_return.tgz.part")),
               f"CF P1-3 PACK_ONLY=1 → 포장만 다시 (계산 재실행 없음 · status.tsv 불변 · 임시 파일 승격) — rc {rcode9}")
    print(f"{'✅' if not bad else '⛔'} build_v5_vasp_package selftest {ok}/{ok + bad}")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for f in ("--build", "--check", "--collect", "--seal_pp", "--selftest", "--pilot"):
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
        reg = load_pp_registry(a.pp_registry, a.pp_registry_sha256, a.manifest_sha256)
        if a.seal_pp:
            r = seal_pp(a.out, a.ret, a.manifest_sha256)
            if a.json:
                _write(a.json, json.dumps(r, ensure_ascii=False, indent=1, allow_nan=False) + "\n")
            print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
        if a.collect:
            if reg is None and not a.pilot:
                raise PkgError("최종 집계(--collect)는 봉인 PP 등록부가 필수다 — --pp_registry R --pp_registry_sha256 H (파일럿 단계 집계면 --pilot 을 명시)")
            uma = json.load(open(a.uma, encoding="utf-8")) if a.uma else None
            rec = collect(a.out, a.ret, a.manifest_sha256, uma, reg, a.pp_registry_sha256 if reg is not None else None)
            for k, s in rec["samples"].items():
                print(f"  {k} W {s['W_J_m2']} · W_PBE {s['W_PBE_J_m2']} · ΔD3 {s['dD3_J_m2']} · D3 쌍 오차 {s['d3_pair_err_J_m2']} · 총 W 인용 {s['total_w_citable']}"
                      f"{' · ' + ' / '.join(s['total_w_labels']) if s['total_w_labels'] else ''}")
            print(f"  G3 {rec['G3']['status']} · G4 {rec['G4']['status']}{' · G5 ' + rec['G5']['status'] if 'G5' in rec else ''} · 미완 {rec['jobs_not_ok']} · 등록부 {rec['pp_registry']['state']}")
            if rec["return_bundle"]["forbidden_files"]:
                print(f"  ⚠ 반송 폴더에 금지 파일이 있다 (POTCAR 본문 등 — 저장하지 말고 지운다): {rec['return_bundle']['forbidden_files']}")
            if a.json:
                _write(a.json, json.dumps(rec, ensure_ascii=False, indent=1, allow_nan=False) + "\n")
            return collect_exit(rec)
        if a.check:
            _, res = check(a.out, a.ret, a.manifest_sha256, reg)
            for n, r in res.items():
                print(f"  {n:34s} {r['status']}{(' · ' + str(r.get('why'))) if r.get('why') else ''}")
            rb = return_manifest_info(a.ret, a.manifest_sha256)
            print(f"  반송 묶음 MANIFEST: {rb} · 등록부 {'검증됨' if reg is not None else '없음 (파일럿 단계 검사)'}")
            if rb["forbidden_files"]:
                print(f"  ⚠ 반송 폴더에 금지 파일이 있다 (POTCAR 본문 등 — 저장하지 말고 지운다): {rb['forbidden_files']}")
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
