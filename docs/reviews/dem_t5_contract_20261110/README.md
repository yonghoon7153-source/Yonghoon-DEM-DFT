# D-3/T5 — 합성 계획·관측 명부의 일관성 계약

**전달된 계획의 선언과 합성 관측 장부를 검사하는 새 연결이다. 실제 T5 자격·통계 등록은 완료하지 않았다. 전체 HOLD.** 바탕은 T0 후보 `c5ebaa71298691020313e272b39c0a80b51cdc4d`이며 원 B는 `13eb293cd9ac44502517c81e8f5e9b7ae02d817f`다. 이 문서의 수치는 작은 합성 시험을 위한 값이다.

## 1. 상태와 근거

| 항목 | 지금 상태 | 근거·범위 |
|---|---|---|
| 새 순수 자료 API | 2개 | `scripts/dem_gen2_t5_contract.py`의 `validate_t5_plan`, `audit_t5_coverage`. 파일·프로세스·네트워크·물리 추정기 호출 없음 |
| 작성 측 최종 시험 | 23/23 | `scripts/test_dem_gen2_t5_contract.py`; 같은 최종 시험의 스텁 red는 12 실패·0 오류 |
| 보호 조건 제거 대조 | 5/5 검출 | §6. 같은 시험의 반복이며 23개에 더하지 않음 |
| 실제 T5·MC·CI 생성 검증 | 0건 | 선언 오라클과 주어진 구간의 포함 산술만 확인 |
| 실제 통계 등록·외부 등록 진위 확인 | 0건 | `DRAFT_UNREGISTERED`, `external_preregistration_verification=NOT_PERFORMED` |
| 연구 결과·실행 GO·gate 쓰기 | 0건 | 반환 `physical_ready=false`, `execution_go=false`, `gate_write=false` |
| 기존 기하·T0·Rint·봉인·원장 수정 | 0건 | 새 모듈·새 시험·이 문서 묶음만 작성. 전체 gate/CI 실행 0회 |
| 독립 검토 | 0건 수령 | 이번 고정 후보는 반박 창 검토 대기 |

정본 요구는 B `13eb293cd9ac:docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §2 T5-01–08과 그 문서가 인용하는 정본 §12 A3다. 구현은 그 전체 자격 중 **선언 명부와 포함·편향 장부**만 다룬다. 기존 `scripts/dem_gen2_qualification.py`의 coverage 분모 정책은 바꾸거나 새 결함으로 재개방하지 않는다.

이미 비준한 D9′는 B `13eb293cd9ac:docs/collab/claude_to_codex/20261109-2230_nonrint-first-link-sha-map.md` §2다. 순수 SE 침대의 300 MPa 가압·이완 끝에서 **질량 기준 ε_sphere, TD 1.64, 외부 표적 10–13 %**를 유지하며 ε_union은 함께 기록만 한다. 이 보정 표적은 T5 연산자의 오차 폭·coverage 문턱이 아니다. 출처를 다시 묻거나 수치를 새로 선택하지 않는다.

## 2. 권고안 전제와 실제 미등록 항목

| 전제 | 이번 합성 선택 | 실제 자격에서 남은 것 |
|---|---|---|
| 권고안 전제(Q-T5-01) | sphere/union × full/interior의 4개 명부. 같은 영역의 ROI·분모·절단·PBC 선언은 두 연산자 사이에 동일해야 함 | 실제 프레임·ID·기하·ROI·분모·단위·PBC 증거 및 주/보조 역할 등록 |
| 권고안 전제(Q-T5-02) | §4의 독립 수식 5개 사례. 표본 단계 `[16,64]`, 반복 4개, seed `[11,17,23,29]` | 실제 RNG·seed·표본 예산·실행 순서·반복 의존성·수렴 판정 등록 |
| 권고안 전제(Q-T5-03) | 입력 구간의 오라클 포함 여부를 세고 `covered/planned`를 주 장부로 유지. toy nominal `19/20`, 목표 `3/4` | 실제 CI 생성식·모형·평가 불확실성·coverage 추론과 합격선 등록 |
| 권고안 전제(Q-T5-04) | 40개 셀 각각 alpha `1/4000`, 합계 `1/100` ≤ family `1/20`. 결손/실패를 planned에서 유지하고 재시도 없음 | 실제 다중 판단 범위·구간/검정과 alpha의 관계·동시 판정 근거 등록 |
| 권고안 전제(Q-T5-05) | 평균 편향·최대 절대 오차·RMSE를 분리. toy ABS budget `0.1`; REL은 영 오라클을 거부 | 실제 사례별 ABS/REL 분류·오차 예산·영 기준 예외·사다리 수렴 규칙 등록 |

위 다섯 가지는 검토를 기다리는 **준비 권고 전제**이며 실제 정량값의 저자 비준이 아니다. `preregistration_draft.json`의 실제 등록 칸은 `null`/`UNSELECTED`다. toy 값과 실제 등록 칸을 분리했다. 스키마의 최대 16,384개 예정 행, 사례 5–16개, 표본 단계 1–16개, 반복 2–128개, 정수 상한 1,000,000,000은 작은 오프라인 계약의 자원 한도이며 물리 예산 권고가 아니다.

## 3. API 입력·출력 계약

`validate_t5_plan(plan)`은 exact built-in dict/list/int/float/str로만 구성된 계획을 받는다. boolean을 정수로 받지 않는다. dict의 키가 정확한 str인지 확인한 뒤 집합·해시·동등 비교를 수행하므로 문자열 하위형의 hash/equality hook을 호출하지 않는다. 불명 필드·미지원 연산자·중복/누락 명부·비유한·미정 필드는 거부한다.

계획은 `schema`, `purpose`, `identity`, `quantity`, `output_unit`, `cases`, `estimands`, `sample_sizes`, `seeds`, `dependence`, `interval_definition`, `error_policy`, `family`, `missing_policy`, `retry_policy`를 모두 갖는다. 정확한 키 집합과 타입은 모듈 및 시험의 `fixture()`가 실행 가능한 합성 예시다. `preregistration_draft.json`은 **문서 봉투**여서 미등록 빈칸을 포함하며 API에 그대로 넣는 실행 계획이 아니다.

신원은 계획 ID·판, producer/operator/oracle/interval-method의 40자리 핀, frame/inventory/unit-system ID다. 행은 같은 신원과 case/estimand/n/repetition/seed/oracle/unit을 갖는다. 셀은 `(case_id, estimand_id, n)`, 예정 행은 셀과 repetition의 곱집합이다. 주어진 행의 seed·핀·ROI 사상과 선언을 비교할 뿐 **핀의 Git 소속·원 자료·현재 기하·실제 독립성은 조회하지 않는다**. fixture의 반복 문자 핀은 의도한 가짜 신원이다.

`audit_t5_coverage(plan, rows)`는 계획과 행을 변경하지 않는다. 행이 명부 밖이거나 중복·다른 신원·비유한·역전 구간이면 `REJECTED`다. `VALID`는 값과 유한한 `[lower,upper]`가 필요하고 failure code는 `null`이다. `FAILED`/`MISSING`은 failure code가 필요하며 값과 구간은 `null`이어야 한다. 완전히 없는 행도 결손으로 장부에 남긴다.

| 반환 상태/필드 | 의미 | 자동으로 뜻하지 않는 것 |
|---|---|---|
| `SYNTHETIC_PLAN_VALID` | 선언의 키·타입·논리적 명부·예산 합계가 일치 | 실제 등록·기하·표본 모형 인증 |
| `SYNTHETIC_BOOKKEEPING_COMPLETE` | 예정 행이 모두 유효 payload로 수령됨 | toy 목표 충족, 실제 T5 통과, 연구 GO |
| `INCOMPLETE` | 최소 1개 결손 또는 실패를 예정 분모에 보존 | 자동 재시도·실패 제외 허용 |
| `REJECTED` | 입력 계약 불충족 | 부분 정상 결과의 재사용 허용 |
| `eligible_coverage_diagnostic` | `covered/valid` 진단. valid=0이면 `null` | 주 coverage 또는 완전성 대체 |
| `declared_toy_*_met` | 전달된 toy 기준과 산술 비교만 | 참 coverage·실제 편향 자격 판정 |

**외부 동결 한계:** 계획과 행을 함께 바꾼 호출은 새로운 일관된 입력으로 받을 수 있다. 외부 기대 plan digest·등록 판·시각·서명과 비교하지 않으므로 결과 후 변경 방지를 증명하지 않는다. 반환에 `validation_scope=CALLER_SUPPLIED_PLAN_INTERNAL_CONSISTENCY_ONLY`를 명시한다. 실제 동결은 별도 고정 원본·독립 영수증·저자 승인 계약이 있어야 한다.

## 4. 독립 해석 fixture와 단위

반경 1, 유클리드 비주기 공간, 해당 구를 모두 포함하는 영역을 합성 정의역으로 둔다. 별도 interior fixture도 같은 구를 포함하도록 선언했으므로 시험에서는 full과 같은 수식 값을 쓴다. 실제 interior 절단 구현을 검증했다는 뜻이 아니다. 벽 사례는 중심을 지나는 평면의 한쪽 반공간으로 절단한다.

| 사례 | 독립 수식·기대 관계 | 이번 사용 |
|---|---|---|
| 분리 2구 | 중심 간 거리 > 2; sphere=union=`8π/3` | 고정 선언 오라클 |
| 접선 2구 | 중심 간 거리 = 2; 접촉 부피 0, sphere=union=`8π/3` | 부피와 접촉 면적을 혼동하지 않음 |
| 겹침 2구 | 중심 간 거리 = 1; 렌즈=`5π/12`, sphere=`8π/3`, union=`9π/4` | 독립 해석식을 시험에 직접 작성 |
| 일치 3구 | 중심 모두 같음; sphere=`4π`, union=`4π/3`; 삼중항을 빼면 pair-only 결과 0 | 삼중항 필요성을 수식으로 표시 |
| 벽 절단 | 구 중심을 지나는 평면; half sphere=`2π/3` | 절단 부피 선언을 구간 포함 장부에 사용 |

생산 `q` 함수의 출력을 오라클로 복사하지 않았다. 동시에 이 API는 좌표를 받거나 해석식을 재검증하지도 않는다. **수식 fixture의 산술 대조와 실제 기하 추정기 검증은 다르다.** PBC는 `NONE` 또는 `XY_PERIODIC` 선언을 받고 후자는 `REQUIRED_UNQUALIFIED`로 남긴다. 어느 경우도 `pbc_qualification=NOT_QUALIFIED`를 바꾸지 않는다.

`VOLUME` 값의 단위는 `SYNTHETIC_LENGTH_CUBED`, `POROSITY`는 `FRACTION`이다. 구간 끝점을 확률처럼 `[0,1]`에 자르지 않는다. 부피 오라클 `8π/3`과 음수 porosity `−0.25` 선언도 그대로 처리한다. 음수 fixture는 signed 산술 보존 시험이며 실제 침대·물리 union·공극률의 적격 사례가 아니다. 부피 관측·오라클은 비음수, 구간 끝점은 유한/순서만 검사한다. 물리적으로 제약된 CI를 생성하는 기능은 없다.

## 5. coverage·편향·family의 정확한 범위

주 장부는 예정 반복 `R`을 분모로 쓰는 `covered/R`이다. 포함은 `lower ≤ oracle ≤ upper`로 센다. 결손과 기술 실패를 성공 사례에서 제외하지 않는다. `covered/valid`는 보조 진단만 제공한다. 반복 4개 중 3개 포함인 완전 toy 셀은 0.75다. 비포함 행 1개를 지워도 주 값은 0.75이고 상태는 `INCOMPLETE`다. 실패 1개·결손 1개·유효 2개 중 1개 포함이면 주 값은 0.25다.

이 산술은 **주어진 구간의 포함 장부**다. 반복 독립성·RNG·CI 생성식·명목 수준의 보장·참 coverage의 추정 불확실성은 시험하지 않는다. nominal level을 `19/20`에서 `99/100`으로 바꿔도 장부의 포함률은 0.75다. 실제 coverage 추론은 항상 `NOT_QUALIFIED`다.

평균 편향은 유효 값들의 `(value−oracle)` 평균이다. 개별 최대 절대 오차와 RMSE도 따로 출력한다. RMSE는 평균을 중심으로 한 표준편차가 아니며 이들은 편향과 개별 오차 진단이다. 유효 값이 없으면 세 통계는 `null`이다. 결손이 있어도 유효 부분 통계가 나올 수 있으므로 `INCOMPLETE`를 함께 소비해야 한다. 표본 사다리는 완전 명부로 유지하되 수렴 기울기·최종 수렴 판정은 구현하지 않았다. REL 예산은 `budget×|oracle|`이며 정확히 oracle=0인 계획을 거부한다. 거의 0인 경우의 ABS 전환 문턱은 미선택·미구현이다. 실제 사례별 혼합 ABS/REL 규칙은 미등록이고 이번 모듈에는 전역 toy 규칙만 있다.

nominal level은 `(0,1)`, coverage target과 alpha는 `(0,1]`의 양의 정수 비로 받는다. 0 확률은 이 준비 계약에서 미지원이다. family 셀 집합은 전체 case×estimand×n과 정확히 같아야 하고 `sum(alpha_cell) ≤ alpha_family`를 Fraction으로 검사한다. 이것은 **명부와 선언 예산 합계의 논리 검사**다. cell alpha가 실제 구간·검정의 오류 보장이라는 증거를 만들거나 union-bound 전체 인증을 수행하지 않는다.

## 6. 시험 먼저와 가드 제거 증거

| 고정 실행 | 메서드 | 실패 | 오류 | rc | 의미 |
|---|---:|---:|---:|---:|---|
| 새 feature의 fail-closed 스텁 + 최종 시험 | 23 | 12 | 0 | 1 | 양성 동작 미구현을 먼저 검출. 기존 기하 API 결함 재현이 아님 |
| 최종 구현 + 같은 시험 | 23 | 0 | 0 | 0 | 23/23 통과 |
| planned 분모를 valid로 바꾼 변이 | 23 | 2 | 0 | 1 | 결손/실패 분모 오염 검출 |
| 중복 행 거부 제거 | 23 | 1 | 0 | 1 | 명부 덮어쓰기 검출 |
| 행 신원 비교 제거 | 23 | 8 | 0 | 1 | 핀·프레임·재고·단위 신원 교체 검출 |
| 결손/실패의 INCOMPLETE 판정 제거 | 23 | 3 | 0 | 1 | 불완전 장부의 완료 승격 검출 |
| family 명부·합계 보호 제거 | 23 | 3 | 0 | 1 | 셀 누락/교체·예산 초과 검출 |

23개 메서드, 내부 subtest 실패 개수, 5개 변이, 전후 반복은 서로 다른 단위다. 합산하여 새 고유 시험 수로 부르지 않는다. 스텁의 음성 거부는 일반적인 무조건 거부여서 구현 검증 근거로 세지 않는다.

실행은 Windows Python 3.12.14, `-I -B`, 고정 소스 바이트 compile/exec다. 프로젝트 코드 전에 audit hook으로 프로세스·네트워크를 거부했다. 각 시험 호출의 실제 engine 호출 0·금지 시도 0·실제 값 접근 0은 해당 호출에 한정한다. 이를 전체 작업 턴의 문서 열람 이력으로 확대하지 않는다. 다른 OS/Python·전체 gate·현장 자격은 수행하지 않았다.

| 소스 | SHA256 |
|---|---|
| red 스텁 | `30128cdeb1818f808ba5ae93b296f756b86db0cb281eae6270a78ee89db2fdd2` |
| green 구현 | `82ac11cc3a4264565e3d08d744d3d9c1ff8dd6ed47deee4d675bf3cb6d75161f` |
| red/green/변이 공통 시험 | `38c3cda7d2ba24b2c22c5bd2f88e5169837c61b9df73cac825b1725ed0baa520` |

바이트·시각·rc·원본 보존·변이별 SHA는 `verification_summary.json` 및 전달 묶음의 원 로그/보고서로 대조한다. 원 소스·시험·red/green·변이·검사 runner는 고정 검토 묶음에 포함한다.

## 7. 남은 검토와 승인

반박 창은 이번 새 연결의 타입/명부/단위·분모·실패 보존 및 외부 동결 한계의 정확성을 검토한다. 그 한정 수용도 실제 T5, T11, T12, P2 ULPR, 실제 build/이력/재개/dt/2, 현장·운영 봉인·실행 GO를 승인하지 않는다. 실제 T5의 정량 선택과 오라클·모형·구간 생성·수렴·coverage 추론·PBC 자격은 별도 등록·검토·승인으로 남긴다. 전체 HOLD.
