---
title: "리뷰 CF 프롬프트 — A′ V5 VASP 외주 준비본 v2 재리뷰 (CE NO-GO 대응: P0 4 · P1 5 · 3b′ · 3c · PP/버전 · D3 예산)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g5, re-review]
status: 발송 완료 · 회신 수령 2026-09-27 **NO-GO** (`codex_CF_reply_…` · P0 3 · P1 3) → v3 (커밋 c8d77dfd5) → 재리뷰 CG 발송 대기
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CF — A′ V5 VASP 외주 **준비본 v2** 재리뷰 (CE NO-GO 대응 확인)

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `e025c0db78754ab0d6117aff34b4e1133dd6968e`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 앞 리뷰: **CE (커밋 8f76b912d) = NO-GO** — 회신 원문 `kb/reviews/codex_CE_reply_wad_aprime_v5_vasp_outsourcing_2026_09_27.md`. 이번 요청은 **CE 재승인 조건 1–4 가 채워졌는지**와 **새로 생긴 구멍**을 보는 것이다.
> 상황은 그대로: V5 는 우리 GPU 한 장(48 GB)으로 RESOURCE_BLOCKED · 업체·예산 미정 · **준비본** (실행 결정 아님). 판정: GO / 조건부 GO / NO-GO.

## §0. CE 지적 → v2 대응 → 음성시험 (한 장)

| CE | 지적 (요지) | v2 대응 | selftest 음성 (이름 요지) |
|---|---|---|---|
| P0-1 | `NCORE = 1 ; EFIELD = 0.01` 이 러너·검사기 통과 | 성능 파일 = **제한 문법**: 한 줄 한 대입 · `;` `\` `#` `!` 금지 · 태그 중복 금지 · 값 타입 (NCORE/NPAR/KPAR/NSIM 양의 정수 · LPLANE/LSCALU/LSCALAPACK 논리) · 읽을 수 없으면 종료 2. 검사기는 INCAR 를 **VASP 의미로** 읽는다 (`;` = 문장 구분 · `\` 거부 · 중복 = 오류) | `;` EFIELD · `;` ENCUT · 중복 · 타입 · 줄 이음 · 허용 밖 → INPUT_MODIFIED · 러너 실제 실행: 우회 줄 → 종료 2 · 아무것도 안 돎 · 없는 성능 파일 → 종료 2 |
| P0-2 ① | 지난 정상 OUTCAR + `VASP_CMD=false` → ✓·OK | 시도 폴더는 **새로만** (있으면 그 잡 거부 · return 3 · 재시도 아님) · 성공 = **rc 0 ∧ 종료 ∧ 수렴 ∧ OUTCAR 실행 1 개** · 잡마다 `attempt.json` {job · attempt · run_id · rc · 시각 · INCAR/POSCAR/KPOINTS/POTCAR/OUTCAR/OSZICAR sha} — 검사기가 대조 (실행 뒤 **생기거나** 바뀌거나 없어진 파일 → ATTEMPT_MISMATCH) | rc 1 + 정상 OUTCAR → EXECUTION_FAILED · 실행 뒤 OUTCAR 교체 → ATTEMPT_MISMATCH · **OUTCAR 없이 죽은 시도에 지난 정상 OUTCAR 를 넣음 → ATTEMPT_MISMATCH** · rc 문자열 → ATTEMPT_MISMATCH · 러너: 재실행 → 기존 폴더 거부·종료 1·앞 결과 보존 · `VASP_CMD=false` → 종료 1·EXECUTION_FAILED (r1 도) · 정상 OUTCAR 인데 rc 1 → 종료 1 |
| P0-2 ② | 미완결 두 번째 실행을 붙이면 조합으로 OK | OUTCAR 실행 머리줄(`vasp.x.y`) 이 **1 개가 아니면** MULTIPLE_RUNS (정적 단일점 프로토콜) | 두 번째 실행 붙임 → MULTIPLE_RUNS |
| P0-2 ③ | OUTCAR ENCUT 400 · INCAR 520 → OK | **설정 되울림 대조**: NIONS · NELECT · ENCUT · ISMEAR · SIGMA (±0.005 · 2 자리 인쇄) · ISPIN · IVDW · LDIPOL · IDIPOL · DIPOL_z (±0.005) · EFIELD ≠ 0 금지. NIONS/NELECT 결측 → SYSTEM_UNVERIFIED · 나머지 결측 → **SETTINGS_UNVERIFIED (막음)** | ENCUT 400 → SETTINGS_MISMATCH · EFIELD 0.01 → SETTINGS_MISMATCH · IVDW/DIPOL/SIGMA/ENCUT 줄 없음 → SETTINGS_UNVERIFIED |
| P0-3 | POTCAR sha 기록만 · TITEL 날짜 버림 | 종별 **전체 TITEL(날짜)·ZVAL** 기대값 (PBE_54) · `POTCAR.titel` · `POTCAR.sha256`(조립본) · `POTCAR.species.sha256`(종별) **반송 필수** · 형식·순서·attempt.json 대조 · OUTCAR 의 TITEL(순서 보존 중복 제거)과 대조 · **잡 사이 종별 sha·조립본 sha 일치** (18 잡 종 순서 동일) · 파일럿 뒤 **등록부** (`--seal_pp`: 종별·조립본 sha · VASP 버전 줄) 봉인 → 이후 대조 | POTCAR.sha256 삭제 → POTCAR_UNVERIFIED · TITEL 날짜 다름 → POTCAR_MISMATCH · OUTCAR TITEL ≠ POTCAR.titel → POTCAR_MISMATCH · bound 만 다른 Ag sha → POTCAR_INCONSISTENT · 조립본 sha 만 다름 → POTCAR_INCONSISTENT · 등록부와 다른 종별/조립본 sha → POTCAR_MISMATCH |
| P0-4 | UMA NaN → G5 PASS · 출처 무시 | UMA 입력: S1 출처 (모델 uma-s-1p1 · 체크포인트 sha 전체 · task omat · default · fairchem 2.19.0/2.21.0(교차대조 등가)) · S3 구조 sha · 원자 수 · pbc · 이름 중복 · **유한값만** — 하나라도 어긋나면 **G5 = BLOCKED** · 파생값도 유한성 필터 · JSON `allow_nan=False` | NaN 전부 → BLOCKED (종료 11) · 체크포인트 · task · 버전 · 구조 sha · pbc · bool 에너지 · 이름 중복 → BLOCKED |
| P1-1 | 기대·반송 INCAR 동시 변조 → OK | `--check/--collect/--seal_pp` **입구**에서 외부 고정 `--manifest_sha256` 과 MANIFEST 목록 **전 파일** 대조 (jobs.json · INCAR · INCAR.r1 · POSCAR · KPOINTS · POTCAR.spec · run_all.sh · JOBS.txt) — 어긋나면 시작 안 함 (종료 2) | 동시 변조 → 거부 · 틀린 고정값 → 거부 · jobs.json D3 기대값 None → 거부 |
| P1-2 | NELECT 결측·D3 기대값 None → OK · 빈 반송 exit 0 | 결측 = 미검증 (SYSTEM_UNVERIFIED · D3_UNVERIFIED · ENERGY_UNPARSEABLE) · **종료코드**: `--check` 0 전 잡 OK / 3 아닌 잡 / 2 승인본·사용법 · `--collect` 0 G5 PASS / 10 FAIL / 11 INCOMPLETE·BLOCKED / 12 UMA 없음 / 3 잡 미완 / 2 · 진단 JSON 은 실패해도 쓴다 (승인본 오류면 오류 JSON) | NELECT 없음 → SYSTEM_UNVERIFIED · Edisp 없음 → D3_UNVERIFIED · 빈 반송 → 종료 3 · 표본 누락 → 종료 3 · UMA 없음 → 12 |
| P1-3 | INPUT_MODIFIED 첫 시도 + 정상 r1 → OK | r1 자격 = 첫 시도가 **실행 실패(rc≠0) · 미종료 · 미수렴** 일 때만 (`rc 0 인데 OUTCAR 없음` = 미종료로 자격) · 첫 시도 없는 r1 · 무결성·PP·설정 위반 → 승격 안 함 (`r1_ignored` 기록) · 러너도 준비 실패(기존 폴더·입력·POTCAR)는 r1 안 함 | INPUT_MODIFIED + r1 → 승격 안 함 · 첫 시도 없는 r1 → MISSING · 미수렴 → r1 채택 · OUTCAR 없이 rc 1 → r1 채택 · rc 0 OUTCAR 없음 → r1 채택 · 러너 미수렴 → r1 성공 → 검사 OK(r1) |
| P1-4 | Edisp 1 % 는 W 오차 예산이 아님 (ΔD3 폭 0.0949) | **두 층**: ① 1 % = 큰 오설정 탐지만 (감쇠·3체·계수) · ② 오차 예산 (결과 전 제안): 표본 **쌍** \|ΔD3_VASP − ΔD3_ref\| ≤ 0.005 J/m² (넘으면 그 표본 총 W 에 인용 금지 라벨 · W_PBE·G5 Δ 불변) · **G3 차이의 차이** ≤ 0.001 (넘으면 G3 = INCOMPLETE (D3 예산)). ref = 같은 절단 s-dftd3 2체 · INCAR 에 **VDW_RADIUS 50.2 · VDW_CNRADIUS 21.17 Å 명시** | 쌍 오차 0.008 → 라벨 · G5 Δ 불변 (TOTEN 과 Edisp 에 같은 오차) · G3 차이의 차이 0.0015 → G3 INCOMPLETE (D3) → G5 오차표만 · Edisp 5 % → D3_MISMATCH |
| P1-5 | G3 예측 산술 오류 | 개정 3 v2 에 정정: 0.0095396272 + 0.0004 = **0.0099396272 < 0.01** — v1 의 'FAIL' 서술 철회 · 여유 ≈ 0.00046 · 경계선 서술만 · VASP 절단 재계산 +0.0095355740 | (문서) |

## §1. CE 재승인 조건 대응

1. **P0-1–4 음성 재현 차단 + 정상 18 잡 대조군 유지** — 위 표 음성 전부 + 정상 대조군 (18 잡 OK · 성능 태그 3 개 허용 · G3·G4·G5 PASS · 종료 0 · −TS 항 차 기록).
2. **P1-1–3 승인본 대조·결측·r1 자격·종료 규약 + 생성본/배포본 재시험** — 합성 패키지를 **실제 `build()`** 로 만들어 시험하고, 배포 러너 `run_all.sh` 를 **bash + 가짜 VASP(python) + 가짜 POTCAR** 로 실제 실행 (6 시나리오). 더해 **실제 재생성 패키지** (`db/inputs/wad_aprime_v5_vasp_2026_09_27`) 로 파일럿 2 잡을 가짜 VASP 끝-끝 → `--check` OK · `--seal_pp` 등록부 생성까지 확인.
3. **D3 범위/예산 · G3 산술 정정 · 3b/3c · PP/버전 선택을 실행 전 비준** — 개정 3 v2 에 적었다 (§2). **비준은 아직** — 이 재리뷰 뒤 1저자가 한다 (결정 `D-2026-09-27-wad-aprime-v5-vasp-route` = proposed).
4. **갱신 패키지 해시로 재고정** — MANIFEST.sha256 파일 sha256 `ab945a7b07928a27d0a66f442c10ec9ebfd68b3e9fda912e7f7ee1fae5ae0561` (§5).

## §2. 개정 3 v2 에서 비준 대상이 되는 선택 (결과 전)

- **3c 채택안** — 총 W 의 G3 FAIL → G5 = `INCOMPLETE (G3 FAIL · G4 <상태> — 오차표만)` · 별도 필드 `raw_error_criteria_met` (Δ 문턱) · `usage_eligible` (원시 기준 ∧ UMA 입력 검사 ∧ G3 PASS ∧ G4 PASS) · G3 FAIL 에서 갈래1/DEM 전달 안 엶.
- **3b 원안 폐기 → 3b′ 제한된 잔차 진단** — δΔ_x = Δ(G3 c+2, 검사 x) − Δ(①) = δW_PBE − δW_UMA · G3 세 구조의 UMA 단일점이 있을 때만 기록 · **문턱 없음 · 판정 아님** · G5 자격·DEM 전달을 열지 않음 · 기록 문구 "V2 결과 및 V5 D3 진단을 본 뒤, V5 전자에너지 전에 채택한 개정".
- **PP = PBE_54 고정** (전체 TITEL 기대값) · PBE_64 는 금지가 아니나 이번엔 54 · PBE_54 인지 내용 해시로 보증 못 함은 한계로 적음.
- **VASP 버전** — 파일럿과 본 배치 같은 빌드 (OUTCAR 첫 줄 · 공백 정규화 일치) · VDW_S6 는 문서상 6.6.0 부터 조정 가능 — 값 1.0 = PBE 기본값이라 구버전도 값은 같다고만 적음 (6.6 이상 요구 안 함).
- **D3 예산** — 쌍 0.005 (G5 표본 문턱 0.10 의 5 %) · G3 차이의 차이 0.001 (G3 문턱 0.01 의 10 %) · V2 실측 QE↔s-dftd3 (쌍 0.0025 · 차이의 차이 0.0001) 은 달성 가능성 참고 (그 수치를 본 뒤 정했다는 사실은 적음).
- **에너지 규약** — W = MP1 σ 0.136 eV 에서의 TOTEN 차 / A (0 K 점착에너지·실제 전자온도 자유에너지로 부르지 않음) · E(σ→0) · −TS 항 차 병기.
- **파일럿 2 잡 (표본 ① bound·far)** — 설정·파서·실패 규칙은 파일럿 **전에** 고정 · W 를 보고 설정을 고르지 않음 · 패키지 sha 같으면 본 배치에 재사용 (실행 최대 36 회) · 방법 변경 불가피하면 파일럿은 구판 진단으로 보존하고 새 버전.
- 바꾸지 않은 것 (CE 권고 범위): σ 일괄 교체 안 함 · ALGO/믹싱 사전 변경 안 함 · V2 VASP 다리 추가 안 함 (권고이지 필수 아님).

## §3. 시험

- `python3 tools/wad/build_v5_vasp_package.py --selftest` → **82/82** (Linux · LF 고정 쓰기라 Windows 에서도 해시가 갈리지 않아야 한다 — CE 에서 CRLF 로 selftest 가 멈췄던 문제).
- **돌연변이 20/20 빨간불** (제품 코드만 깨고 selftest 재실행): `;` 문장 구분 제거 · rc 검사 제거 · attempt sha 대조 제거 · 복수 실행 허용 · ENCUT 되울림 제거 · 잡 사이 일관성 제거 · TITEL 앞 두 단어만 · UMA 유한성 무시 · 승인본 대조 생략 · r1 자격 = OK 아님 전부 · G3 D3 예산 제거 · 러너 기존 폴더 허용 · 러너 성공에서 rc 제외 · 러너 성능 문법 느슨 · UMA 오류 무시 · 사용 자격에서 G3 제외 · D3 1 % 검사 제거 · POTCAR sha 결측 허용 · 러너 r1 을 준비 실패에도 · 버전 일관성 제거.
- 합성 구조는 Ag 3 층(63 원자)을 붙여 |D3| > 12 eV — 1 % 문턱(≥ 0.19 eV)이 예산 시험의 이동(≤ 0.10 eV)을 가리지 않게 했다 (첫 판은 5 원자라 1 % 검사가 먼저 터져 예산 시험이 헛것을 쟀다 → 고침).
- 실제 재생성 패키지 v1→v2 차이: POSCAR·KPOINTS·POTCAR.spec **불변** (구조 sha 동일) · INCAR/INCAR.r1 에 두 줄 (VDW_RADIUS · VDW_CNRADIUS) · D3 기대값 VASP 절단 재계산 (최대 0.031 eV · 0.05 %) · run_all.sh · jobs.json · README.

## §4. 질문 (보내기 전 필수 수정만 P0/P1 · 나머지는 권고)

- **R1 재현 차단** — CE 의 P0-1–4 · P1-1–3 재현이 이 커밋에서 모두 막히는가. 같은 계열의 **새 우회**가 있는가 (예: 성능 파일 문법과 VASP 파서의 차이 · `attempt.json` 을 러너가 쓰는 구조의 한계 · 버전 줄 정규화).
- **R2 설정 되울림 파서** — `parse_outcar` 의 정규식 (NIONS · NELECT · `ENCUT = … eV` · `ISMEAR = …; SIGMA = …` · ISPIN · IVDW · LDIPOL · IDIPOL · DIPOL · EFIELD · `Edisp (eV):`) 이 VASP 6.x OUTCAR 에서 **해석된 값**을 읽는가, 아니면 일부(IVDW · DIPOL)는 INCAR 에코 줄을 읽게 되는가. 못 읽으면 SETTINGS_UNVERIFIED 로 막는 지금 선택이 맞는가 (파일럿에서 확인 예정).
- **R3 D3 예산** — 쌍 0.005 (라벨) · G3 차이의 차이 0.001 (G3 INCOMPLETE) 의 배분과 결과(라벨 vs 차단)가 결과 전 제안으로 적절한가. G3 에서 D3 예산 초과를 FAIL 이 아니라 INCOMPLETE 로 두는 것이 맞는가.
- **R4 3b′ · 3c** — 3b′ 의 이름·정의·허용 문구·DEM 제한 · 3c 의 상태 문자열과 두 필드가 CE §5 의 조건을 채우는가.
- **R5 PP · 버전** — 전체 TITEL + 종별·조립본 sha 잡 사이 일치 + 파일럿 등록부 + 버전 줄 일치로 P0-3 가 해소되는가. 파일럿 두 잡만으로 등록부를 봉인하는 순서에 구멍이 있는가.
- **R6 r1 · 종료 규약** — `rc 0 인데 OUTCAR 없음` 을 미종료(r1 자격)로 두는 것 · 러너 준비 실패는 r1 안 함 · 종료코드 표가 자동 파이프라인에 충분한가.
- **R7 그 밖에 보내기 전 막는 것** — README(업체용 · 파일럿 2 잡 · 재사용 · 36 회 · 16 GB 는 파동함수 몫) · 추정 · 개정 3 v2 의 허용·금지 서술.

## §5. 첨부 (커밋 e025c0db7 · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json  36eda928788275b5aa377e4dbf3613351b6d3a73fdf8b5ec4ce70655cb81544f
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                             480559b8309ed38e1b544e6a041503e7a85a427c4fe837108aa138ed8100bc76
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                       ab945a7b07928a27d0a66f442c10ec9ebfd68b3e9fda912e7f7ee1fae5ae0561
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                            36bfed57377f3be3a09b6ee7e77d3bb4ae66d7007c43c3de0676741865fddc1d
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                             2d3357a0ddf7a69c324de6ba09493e93e0304ff79824836c84b3cda4686b4fe1
tools/wad/build_v5_vasp_package.py                                            3bc7cde52c5529cff65d80ac5678a48d484925a036aa6dce224199e59e925dd0
db/governance/decisions.json                                                  56e8d507d3e27c57ec02ed4519d43b3fb6feb2a10548e1d89dd0f68f4c064a61
kb/reviews/codex_CE_reply_wad_aprime_v5_vasp_outsourcing_2026_09_27.md        26769b09da6451fc5b22857b5509b383858099ec68de5b37aefae2b428918930
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                            8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                      3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

개정 3 v2 content_digest `sha256:243ccf8c7536800e624a1df90501b77319b0e266ca97298c77c3ed94b26ecf8d` · 도구 sha 는 jobs.json 의 `tool_sha256` 과 같다 (`3bc7cde5…`). 같이 보면 좋은 것: `db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs/V5_s_outer_A_bound/` (INCAR · INCAR.r1 · KPOINTS · POSCAR · POTCAR.spec) · 결정 `D-2026-09-27-wad-aprime-v5-vasp-route` (proposed · status_history v2) · CE 프롬프트 `codex_CE_prompt_wad_aprime_v5_vasp_outsourcing_2026_09_27.md` (구판 설계 설명).

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께) → 권고 (선택) → R3·R4 에 대한 명시 의견 (1저자가 비준할 선택으로 넣어도 되는지).
