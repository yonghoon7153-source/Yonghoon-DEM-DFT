---
title: "리뷰 CG 프롬프트 — A′ V5 VASP 외주 준비본 v3 재리뷰 (CF NO-GO 대응: 증거 먼저 · 등록부 필수 · G4 D3 동일성 · 마지막 레코드 · 실물 Edisp · 포장 실패)"
date: 2026-09-27
updated: 2026-09-27
tags: [review, codex, adhesion, wad, prereg, vasp, outsourcing, lpscl, silver, uma, d3, dipole, g4, g5, pp-registry, re-review]
status: 발송 대기 (1저자) — 도구·패키지·개정 3 v3 는 커밋 c8d77dfd5 에 고정 (원격)
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# 리뷰 CG — A′ V5 VASP 외주 **준비본 v3** 재리뷰 (CF NO-GO 대응 확인)

> 트랙 W_ad (점착) → 1저자 = 사용자. 정본 브랜치 `claude/friendly-meitner-lldvar` · **커밋 `c8d77dfd599cf2a867afa7bfdd3aef4c331b0ed3`** (아래 해시는 전부 이 커밋의 트리에서 `tools/review_manifest.py --require_pushed` 로 뽑았다 · 원격에 있음).
> 앞 리뷰: CE (8f76b912d) NO-GO → v2 (e025c0db7) → **CF NO-GO** — 회신 원문 `kb/reviews/codex_CF_reply_wad_aprime_v5_vasp_outsourcing_v2_2026_09_27.md` (재현 스크립트 원문 `db/raw/codex_CF_repro_2026_09_27/repro_cf.py`). 이번 요청은 **CF 재승인 최소조건 1–5** 가 채워졌는지와 **새로 생긴 구멍**을 보는 것이다.
> 상황은 그대로: V5 는 우리 GPU 한 장(48 GB)으로 RESOURCE_BLOCKED · 업체·예산 미정 · **준비본** (실행 결정 아님). 판정: GO / 조건부 GO / NO-GO.
> ⚠ selftest 는 합성 패키지 build 단계에서 **simple-dftd3** (python `dftd3` API) 가 필요하다 — CF 환경엔 없어 재현을 못 했다. 가능하면 설치해서 돌려 주고, 안 되면 배포본 기준값으로 독립 시험해 주면 된다.

## §0. CF 지적 → v3 대응 → 음성시험 (한 장)

| CF | 지적 (요지) | v3 대응 | selftest 음성 (이름 요지) |
|---|---|---|---|
| P0-1 | 설정·PP 모순이 rc/미수렴과 겹치면 r1 이 덮는다 | `check_job` 순서를 바꿨다: 실행 기록 → 입력 무결성 → 복수 실행 → **있는 증거의 모순** (POTCAR 기록 결측·형식 · TITEL/ZVAL · OUTCAR TITEL · 등록부 종별·조립본 sha · 등록부 버전 · 설정 해석값 · Edisp 1 %) = **재시도 자격 없음** (`conflicts` 목록에 전부) → 실행 상태 (rc · 미종료 · 미수렴 = r1 자격) → 완결성 (성공한 실행만). 증거가 **없는** 조기 종료(OUTCAR 없음)는 모순이 아니다. 시도 사이 POTCAR·버전 일관성은 첫 시도·r1 **모든 시도**에서 모은다 | ENCUT 400 + rc 1 · ENCUT 400 + 미수렴 · OUTCAR TITEL 다름 + rc 1 · 등록부와 다른 Ag + rc 1 · 등록부와 다른 버전 + 미수렴 · Edisp 5 % + rc 1 — 각각 + 정상 r1 → 모순 상태 · `r1_ignored` · 등록부 없이 버려진 첫 시도의 다른 Ag → POTCAR_INCONSISTENT · **정당한 r1 네 경로 보존** (미수렴 · OUTCAR 없이 rc 1 · rc 0 OUTCAR 없음 · 정상 OUTCAR 인데 rc 1) |
| P0-2 | 등록부 생략·`{}` 로 최종 PASS | 최종 `--collect` 는 봉인 등록부 + 고정 sha **필수** (없으면 종료 2) · 파일럿 단계 집계는 `--collect --pilot` 만 (G5 = `BLOCKED (PP 등록부 없음)` · total W 인용 불가) · `validate_pp_registry`: schema `aprime_v5_pp_registry/v2` · pp_set PBE_54 · 다섯 종 TITEL · 종별 sha 다섯 · 조립본 sha (잡 종 순서 키) · 버전 줄(`vasp.`) · 패키지 MANIFEST sha · 파일럿 두 잡 run_id 형식 — 틀리면 검사·집계 **시작 안 함** · 결과 JSON 에 검증한 등록부 sha · `usage_eligible` 에 등록부 검증 · attempt.json 의 run_id(`YYYYmmddTHHMMSS-PID-RANDOM`)·t_start ≤ t_end·rc 정수 **필수** · `seal_pp` 는 파일럿 run_id 없으면 안 만든다 | 등록부 없이 집계 → BLOCKED · usage false · 종료 11 · 틀린 등록부 8 종(빈 객체 · schema · MANIFEST · 버전 없음 · 조립본 없음 · run_id · TITEL · pp_set) → PkgError · CLI: 등록부 없음 2 · 빈 등록부(해시 맞음) 2 · `--pilot` 11 · 봉인 등록부 0 · 해시 틀림 2 · run_id 없음/형식/t_end<t_start/t_start 없음/rc 문자열 → ATTEMPT_MISMATCH |
| P0-3 | G4 의 D3 불일치가 수렴 실패를 가린다 (0.021 → 0.019) | G4 변형(e70·k1·s05)은 표본 ① 과 같은 POSCAR·셀·D3 설정 → 끝점마다 \|Edisp(변형) − Edisp(①)\| ≤ **1e-4 eV** (VASP 인쇄 5 자리) 아니면 그 변형 `INCOMPLETE (D3 불일치)` · G4 전체는 FAIL 우선 → INCOMPLETE → PASS · 차이는 `d3_same_geom_diff_eV` 로 기록 | e70 ΔW 0.021 → FAIL · 같은 far 에 TOTEN·Edisp 동일 이동 −0.02524 eV (1 % 검사 통과) → e70 INCOMPLETE (D3 불일치) · G5 안 열림 · 종료 11 · 정상 대조군은 차 0 |
| P1-1 | 마지막 NaN TOTEN 을 무시하고 앞 값 | 에너지 = **마지막 레코드**의 토큰을 유한수로 해석 (NaN·Inf·별표·잘림 → None → ENERGY_UNPARSEABLE · 앞 값으로 안 돌아감) · TOTEN·E(σ→0)·E(무엔트로피)는 마지막 `FREE ENERGIE OF THE ION-ELECTRON SYSTEM` 구획 **뒤**의 레코드만 — 실물 확인: VASP 5.4.4 는 SCF 단계 TOTEN(−1122.49)에 D3 를 안 넣고 최종 구획(−1151.30)에만 넣는다 | 최종 TOTEN NaN · 별표 · 유한 뒤 마지막 NaN · 최종 구획 없음(SCF 단계 값만) → ENERGY_UNPARSEABLE · SCF 단계 레코드만 있으면 세 에너지 None (단위 시험) |
| P1-2 | 실물 `Edisp (eV)  -28.80731` 을 못 읽음 | 정규식 `Edisp\s*(?:\(eV\))?\s*[:=]?\s*(\S+)` (무콜론·콜론·등호) + 마지막 레코드 유한성 · **실물 발췌 픽스처** `REAL_OUTCAR_544` (저장소 `…/static/OUTCAR.gz` 에서 33 줄 · selftest 가 원본 gz 와 **줄마다 대조**해 지어낸 줄이 없음을 확인) · 합성 OUTCAR 도 실물 구조로 바꿨다 (INCAR: · POTCAR/TITEL · 배열 · Startparameter · DIPCOR · SCF 단계 · DFTD3 구획 · 무콜론 Edisp · FREE ENERGIE · 종료) | 실물 판독 전 항목 (NIONS 227 · NELECT 1596 · ENCUT 520 · ISMEAR 0 · SIGMA 0.05 · ISPIN 2 · IVDW 11 · LDIPOL · IDIPOL · VDW_S6/S8/RADIUS/CNRADIUS · Edisp · 최종 TOTEN · E(σ→0) · NGZF 560 · min pos 520) · 콜론/등호 변형 · 마지막 Edisp NaN → None |
| P1-3 | 포장 실패인데 '✅ 끝' exit 0 | 반송 묶음은 `.part` 임시 파일에 쓰고 성공해야 승격 · tar·sha256 실패 → **종료 4** · '✅ 끝' 금지 · `PACK_ONLY=1` 로 계산 없이 포장만 재시도 (VASP_CMD·POTCAR_DIR 불필요 · env.txt 에 기록) | 배포 러너 실제 실행: tar 실패 shim → 종료 4 · '✅ 끝' 없음 · tgz 없음 · 계산 결과 보존 → `PACK_ONLY=1` → 종료 0 · tgz·sha 생성 · status.tsv 불변 · `.part` 없음 |

## §1. CF 의 R2·R3·R4·권고 대응

- **R2 해석값 출처** — OUTCAR 의 **INCAR 에코 구획**(` INCAR:` 다음 ~ 첫 ` POTCAR:` 전)은 설정 판독에서 뺀다 (에코에만 있는 값은 None → SETTINGS_UNVERIFIED · 음성시험 있음). D3 계수는 **DFTD3 구획의 해석값**(VDW_S6/S8/A1/A2/RADIUS/CNRADIUS)을 기대값과 대조 (계수 ±5e-4 · 절단 ±0.01 Å · VDW_A1 0.4 → MISMATCH · VDW_A2 결측 → UNVERIFIED). **DIPOL 증거 두 길**: (가) 해석값 DIPOL 줄 (±0.005) · (나) `direction 3 min pos` / NGZF(**dimension 줄** · support grid 아님)로 본 cut 위치 = (DIPOL_z + ½) mod 1 (±2 격자). (나) 의 뜻은 **실물로 확인**했다 — 같은 실물 계산의 INCAR `DIPOL = 0.5 0.5 0.4278` · OUTCAR `min pos 520` / NGZF 560 = 0.9286 vs 기대 0.9278 (0.43 격자). 5.4.4 는 DIPOL 줄을 찍지 않는다. 둘 다 없으면 SETTINGS_UNVERIFIED (자동 통과 없음). 둘 중 하나라도 모순이면 SETTINGS_MISMATCH.
- **파서 적응 정책 (결과 전 · 개정 3 v3)** — 실물로 확인한 형식은 VASP 5.4.4 한 건이다. 업체 버전 형식이 다르면 파일럿 원문으로 **파서만** 적응 (판정 규칙·문턱·기대값·상태 순서 불변 · 적응 내용·전후 selftest·새 도구 sha 기록). 적응 전에는 못 읽은 항목이 미검증으로 막힌다.
- **R3** — 0.005 · 0.001 J/m² 은 **운영 예산**이지 신뢰구간이 아니라고 개정·도구 docstring 에 적었다. 예산 통과 ≠ 기준 D3 대비 오차 0. 잔차(G5 Δ) 자격과 총 W 인용 자격은 별개.
- **R4** — G5 상태 순서: UMA 입력 BLOCKED → 등록부 BLOCKED → 분모 INCOMPLETE → G3/G4 비통과면 `INCOMPLETE (G3 x · G4 y — 오차표만 · 원시 기준 충족/미충족)` → 원시 FAIL → PASS (G3 FAIL + 원시 FAIL → INCOMPLETE · 원시 미충족 병기 · 음성시험 있음). `usage_eligible` = 원시 기준 ∧ UMA 입력 ∧ **등록부 검증** ∧ G3 PASS ∧ G4 PASS.
- **권고** — `total_w_citable`·`total_w_labels` 기계 필드 (등록부 ∧ 쌍 오차 ≤ 0.005 ∧ G3 PASS ∧ G4 PASS) · run_id·시각 형식 검사 · 시도 폴더 **원자적 `mkdir`** (없음 확인 뒤 `mkdir -p` 제거) · README: 수동 재실행 = 새 승인 · 포장 재시도는 계산 없음 · 러너 종료코드 0/1/2/4.

## §2. CF 재승인 최소조건 대응

1. **모순 + 실행 실패 조합 음성시험** — §0 P0-1 행 (6 조합 + 시도 사이 일관성 + 정당한 r1 네 경로).
2. **최종 판정에 봉인 등록부·스키마·패키지 결속 필수 · 파일럿 예외 분리** — §0 P0-2 행 (`--pilot` 로만 · CLI 5 경우 · 틀린 등록부 8 종).
3. **G4 D3 뒤집힘 차단** — §0 P0-3 행 (리뷰어 재현 0.021 → 0.019 를 같은 수치로 재현해 막음).
4. **비유한 에너지 · 실물 Edisp · 포장 실패 종료코드 수정 + 배포본 재시험** — §0 P1 행 + 배포 러너 실제 실행 9 시나리오 (정상 · 재실행 거부 · VASP_CMD=false · 성능 파일 우회 · 없는 성능 파일 · r1 · rc 1 · tar 실패 → 4 · PACK_ONLY). 더해 **실제 재생성 패키지**로 파일럿 2 잡 가짜 VASP 끝-끝: OK (DIPOL 근거 `min pos cut 350/400`) → `--seal_pp` (실제 run_id) → `--collect` 등록부 없음 = 2 · `--collect --pilot` = 3 (16 잡 없음) · `--check` + 등록부 = 등록부 검증됨.
5. **정상 18 잡·정당한 r1 유지 + 재생성 패키지 해시 고정** — 정상 대조군 18 잡 OK · 등록부로 G3·G4·G5 PASS · 종료 0. 패키지 MANIFEST.sha256 파일 sha256 `da260794745bdbda2d827f116162115af90e82e229f897aad00166aff16dcdd4` (§5). 1저자 비준은 이 재리뷰 뒤 (결정 `D-2026-09-27-wad-aprime-v5-vasp-route` = proposed).

## §3. 시험

- `python3 tools/wad/build_v5_vasp_package.py --selftest` → **130/130** (실물 원본 대조 1 건은 저장소 경로가 있을 때만 — 없으면 SKIP 을 찍고 통과로 세지 않는다).
- **돌연변이 38/38 빨간불** (제품 코드만 깨고 selftest 재실행). CF 대응 19 개: 모순을 실행 성공일 때만 · 일관성을 최종 결과만 · 등록부 없이 G5 열림 · 등록부 내용 검증 안 함 · CLI 등록부 필수 해제 · G4 D3 동일성 제거 · TOTEN 숫자만 매치 · 최종 구획 요구 제거 · Edisp 콜론 필수 · 포장 실패 무시 · PACK_ONLY 제거 · INCAR 에코 안 뺌 · min pos cut 검사 제거 · NGZF 를 support grid 로 · D3 계수 A1 대조 제거 · run_id 형식 검사 제거 · G5 순서 뒤집기 · total W 인용이 라벨 무시 · mkdir 비원자적. ⚠ 첫 판은 **37/38** 이었다 — '최종 구획 요구 제거' 가 살아남았다 (합성 OUTCAR 의 SCF 단계에 E(σ→0) 줄이 없어 시험이 헛것을 쟀다). 합성 OUTCAR 에 실물처럼 단계별 E(σ→0) 줄을 넣고 단위 시험을 더해 38/38.
- 패키지 v2→v3 차이: INCAR·INCAR.r1·POSCAR·KPOINTS·POTCAR.spec **불변** (입력·D3 기대값 동일) · run_all.sh · README · jobs.json (schema v3 · 도구 sha · 설정 필드)만.

## §4. 질문 (보내기 전 필수 수정만 P0/P1 · 나머지는 권고)

- **S1 재현 차단** — CF 재현(repro_cf.py 의 조합·등록부·G4·NaN·Edisp·tar)이 이 커밋에서 모두 막히는가. 같은 계열의 새 우회가 있는가 (특히 "증거 없음 vs 모순" 경계 — 예: POTCAR 기록은 정상인데 OUTCAR 가 TITEL 줄 없이 잘린 실패 시도, 부분 OUTCAR 의 설정 줄만 있는 경우).
- **S2 등록부 결속** — 등록부 스키마·검증 항목이 "파일럿에서 봉인한 것과 대조" 를 보증하기에 충분한가. 등록부를 봉인(커밋·sha 기록)하는 절차를 도구 밖에 두는 것이 괜찮은가.
- **S3 G4 동일성 문턱** — 같은 기하 Edisp 차 ≤ 1e-4 eV 가 적절한가 (VASP 는 5 자리 인쇄 · 같은 바이너리·같은 입력이면 사실상 0). k·ENCUT·σ 가 D3 에 영향을 주지 않는다는 전제에 예외가 있는가.
- **S4 DIPOL 둘째 길** — min pos / NGZF cut 대조(±2 격자)를 해석값 증거로 쓰는 것이 실물 한 건 확인으로 충분한가. min pos 가 0/1 기준인지 모르는 채 ±2 격자로 흡수한 판단이 괜찮은가.
- **S5 최종 구획 규칙** — TOTEN·E(σ→0)·E(무엔트로피)를 마지막 `FREE ENERGIE` 구획 뒤 레코드로만 제한하는 것이 VASP 6.x 에서도 타당한가 (헤더 문구가 다르면 미검증으로 막히고 파서 적응 대상이 된다).
- **S6 그 밖에 보내기 전 막는 것** — README(업체용 · 재실행 문구 · PACK_ONLY) · 개정 3 v3 의 허용·금지 서술 · 파서 적응 정책.

## §5. 첨부 (커밋 c8d77dfd5 · sha256)

```
db/properties/wad_aprime_pilot_prereg_v5_amendment_3_vasp_v5_2026_09_27.json                        a12ab7e5eb978e8f93a48312bfd96eb528656f8c2cfefd643bea2f576452c21a
db/inputs/wad_aprime_v5_vasp_2026_09_27/jobs.json                                                   07ab5f7451003892fe2a3bc1d1c3fb26e737897299f2acc00e03a1b2af0ea12b
db/inputs/wad_aprime_v5_vasp_2026_09_27/MANIFEST.sha256                                             da260794745bdbda2d827f116162115af90e82e229f897aad00166aff16dcdd4
db/inputs/wad_aprime_v5_vasp_2026_09_27/run_all.sh                                                  512b4681c20c55066d5edb2b0c7ea29ac6ebeb648ca24fba23da37a1ad4998dd
db/inputs/wad_aprime_v5_vasp_2026_09_27/README.md                                                   0185cf1b454672308fc114e6939993b5cc31f01bc5835d16a7525e94a3324249
tools/wad/build_v5_vasp_package.py                                                                  2c9f9ab97e54a6bff884ff231b5aa2f9c39b881238354f7c0ecc0da38ca200f3
db/governance/decisions.json                                                                        e7c2968f0b114e6096b15a5abcbe49d5ff75828b669aae901b695bac7557b9c2
kb/reviews/codex_CF_reply_wad_aprime_v5_vasp_outsourcing_v2_2026_09_27.md                           dee27633f35efbac52eef5fe1cb43d29d81e473f00c2761e92dd668432c91f2b
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/OUTCAR.gz  a168ffd15d6657f2e2272fbe3a6f2af416150abb0690cbcd200825af710dee72
db/properties/sdcp_c12_v41_partial_raw/prospective/sdcp_neutral__b00__afm2424_pm1/static/INCAR      a83650c276dce85e5caa570537a439cab1e557254fad3ee8f37174e29f005a7a
db/properties/wad_aprime_s3v2_seal_2026_09_26.json                                                  8862a8e97d007361ee778ff0b643abea870701caabc1429d89c90c20f8b268c2
db/properties/wad_aprime_pilot_prereg_v5_2026_09_25.json                                            3d35dfb9e8fbcbc79c757fe9205fa78437f8e250d9c16522ac14f5ef1f2f0059
```

개정 3 v3 content_digest `sha256:a4ac661db7a5dc0215e0b93f8cc964219985195a08ca933562cf0a662458640c` · 도구 sha 는 jobs.json 의 `tool_sha256` 과 같다 (`2c9f9ab9…`). 실물 OUTCAR·INCAR 두 줄은 픽스처 출처 확인용이다 (다른 계 · V5 결과 아님).

## §6. 회신 형식

판정 (GO / 조건부 GO / NO-GO) → **보내기 전 필수 수정** (P0 · P1, 재현 가능한 근거와 함께) → 권고 (선택) → S3·S4·S5 에 대한 명시 의견.
