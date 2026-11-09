# 비 Rint 첫 연결·좁은 메타 초안 — 2026-11-09

**DEM 합성 연결 1개, LHS 명령 초안 1개, 믹서 명령 초안·계획 틀 2개. 전체 HOLD.** 1저자가 전달한 11-09 밤 후속 지시의 범위다. 실제 연구 결과·현장 접근·값/원로그 열람·운영 재봉인·예약 변경은 모두0건이다. 새 `[DEM 우선 (수영)]` 재설계는 Claude 담당이며 이 후보의 범위가 아니다.

## 1. 바탕과 반입

| 구분 | 확인한 신원·범위 | 반입 방법 |
|---|---|---|
| 시작 B | `e91bd1c948362712def3f16b5b995027cc10011f` = 작업 시작 때 fetch로 확인한 `origin/claude/sdcp-dem-manuscript-si-pqwtv8` | 새 가지 `codex/nonrint-first-link-1109`. 기존 가지 rebase/force/amend·동기 merge 없음 |
| 예고된 후속 | `1f71b5b7c` 및 `20261109-1900_nonrint-approved-forms-sha-map.md`는 시작 fetch에서 확인되지 않음 | 1저자가 전달한 O1 결정/후속 범위는 대화 비준으로 적용. 원격 반입·§6 확인으로 바꿔 쓰지 않음 |
| 승인 양식 사본 | 원 `6b9d8e14917060465e059d91e6e63f19b1d8bd52` → 이 가지 `43eb8a28c95b92faa120793c0f720d8d3cd409bd` (7문서) | B에 같은 patch/blob가 이미 있으면 건너뜀. 없으면 새 후보보다 먼저 `cherry-pick -x` |
| LHS O1 선택지 사본 | 원 `476e736e251991f4f5916fe02d990454acaa064d` → 이 가지 `b492a206205958a7f5ab2a53d2e14e5403690f2e` (3문서) | 동일하게 조건부 선행 반입. superseded 초안/동기 merge를 추가 반입하지 않음 |
| 이번 새 후보 | 고정 DEM 핀 및 최종 문서 핀은 전달 ZIP의 `SOURCE_PIN.txt`·`CHERRY_PICK_COMMITS.md`로 제공 | 기존 사본 둘과 이번 새 커밋을 구분. Claude가 실제 B 대응표를 작성 |

## 2. DEM 우선

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| 첫 연결 | 합성 servo→relaxation 진단 후보 1개. 실제 live reader·stage 전이·gate 쓰기0 | 이번 DEM 고정 핀: `docs/reviews/dem_gen2_observation_bridge_20261109/README.md` §API와 이전 계약의 구분·§관측·후보 판정 순서 | 별도 반박 창 한정 검토. 1저자가 DEM 전용 ZIP 발송 |
| 시험 먼저 | 이전 scalar guard에서 assertion 실패를 확인한 뒤 연결 구현. 최종 전후 동일 시험·내부 routing 수정·변이 근거를 따로 보존 | 같은 폴더 `verification_summary.json`·`review_request.md`, ZIP 원로그 | 자체 회귀를 독립 판정으로 기록하지 않음. 실제 T0/T5/T11/T12 자격은0 |
| 비결과 메타 | 실제 수령0. 빌드/기존 자격 기록의 신원과 하중·면적·입경·측정 규약만 질문 | `43eb8a28c:docs/reviews/nonrint_approved_preparation_20261109/dem_nonresult_intake_form.md` §1–5; 이번 인계 쪽지 §DEM Q3 | 1저자 한 번에 답할 M1–M9. 모르는 항목은 UNKNOWN; 원로그/실제 값 제외 |
| 남는 구현·승인 | 정확 경계·S0·P2 ULPR·live 엔진 연결0, Q2 정량값·Q4 실제 자격 미승인 | `43eb8a28c:docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §3–5 | 지금 재질문하지 않음. 연결마다 다음 별도 지시·시험 먼저·고정 핀·반박 검토. gate 정지 |

## 3. 믹서

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| Q1 다음 문서 | ibb Linux/SLURM 한 설치·1저자 담당. ASCII 초안1, 고정 계획 빈틀1 | `mixer_ibb_metadata_command_draft.md` §1–4; `mixer_ibb_fixed_qualification_plan.md` §1–4 | 1저자가 대상·읽기 범위·크기/시간 예산을 보고 실행 여부 별도 결정 |
| 수집/자격 | 명령 실행·구문 검사·현장 조회·링크/경합/실제 binary/MPI 시험0. 실제 필드 null/UNKNOWN | 같은 두 문서의 출력→필드 표와 남은 영수증 | 현재 파일 hash/FS 메타만으로 실제 운영 신원·자격·자원 GO를 채우지 않음 |
| 승인·수령 | Q2/Q3/Q5 미승인. 최종 과거 한정 수용 ZIP은 지금 미전달·Claude 미수령 유지 | `mixer_ibb_fixed_qualification_plan.md` §1·§4–5 | 최종 발사 묶음 검토 때 함께 전달. 이번 문서 인계 ZIP과 구분 |

## 4. LHS

| 항목 | 상태 | 근거 | 다음 / 사용자 결정 |
|---|---|---|---|
| Q1=O1 | 현재 덱1개/회: 별칭·선언 종류·bytes·현재 SHA256·관측 UTC만 받는 ASCII 초안1 | `b492a2062:docs/reviews/lhs_q1_remaining_options_20261109.md` O1; `lhs_current_identity_only_draft.md` §1–4 | 1저자가 실제 대상·읽기 예산을 확인한 뒤만 실행. 지금 실행/구문 검사0 |
| 실행 신원 | WSL30 `NOT_ESTABLISHED`; 원 실행 영수증0/30이라는 제공자 보고를 현재 hash로 대체하지 않음 | 같은 초안 §1·§4, 기존 O1 선택지 | 현재 파일 신원과 실행 당시 사용을 별개로 유지 |
| 정본·값·분석 | 원로그 본문·실제 값 수령0; Q2–Q4 미승인 | 같은 초안 §5 및 기존 문서 승인 경계 | 이번에 Q2–Q4를 묻지 않음. A/C·명부/구간·노출/값 GO를 자동 확정하지 않음 |

## 5. 전달과 금지 경계

- DEM 반박용 ZIP: 새 순수 합성 API 연결 1개와 전후·회귀·변이/보존 근거. 외부 판정 전 후보다.
- Claude 인계용 ZIP: 새 커밋 패치·정확 Git snapshot·조건부 선행 문서 사본의 표·DEM 반박 ZIP·인계 쪽지. 반입은 Claude의 `cherry-pick -x`.
- LHS·믹서 ASCII 블록은 문서 바이트로만 검사했다. 그 안의 셸·원격 도구·대상 binary를 실행하지 않았다. 실제 메타 수령0, 연구 결과0.
- Rint 코드·시험·리뷰 문서, 원장·공유 진행 기록·운영 source seal은 변경0. 전체 gate/CI·엔진·MPI·Slurm·host 접근은 수행하지 않는다. 새 합성 회귀를 전체 gate 통과로 표기하지 않음.

**전체 HOLD.** 문서/합성 후보 수용과 실제 자격·운영 봉인·발사/배포는 별도다. 반박 창 GO 아래로 발사·배포 기준을 낮추지 않는다.
