# DEM 세대 2 T11 — 합성 계획 계약 후보

**작성 측 합성 검사 24/24와 가드 제거 대조 6/6 검출을 완료했다. 실제 T11 자격·등록·실행 GO는 0건이며 전체 HOLD다.** 바탕은 `d11b60d2bc75948b0bc8a2c33f84e3b0b65869d4`, T0 고정 계약은 `c5ebaa71298691020313e272b39c0a80b51cdc4d`다. Rint·봉인 32·원장·운영 봉인·기존 자격 함수·생성기를 변경하지 않았다.

**작성 순서의 한계:** 구현 초안이 scratch에 먼저 존재했다. 그 초안을 보존한 뒤 리포 후보 적용 전 fail-closed 스텁에 동일 시험을 실행하여 19 실패·0 오류를 확인했고, 후보 적용 후 24/24를 확인했다. 이것을 엄격한 구현 전 TDD 또는 기존 코드 결함의 red 재현이라고 주장하지 않는다.

## 1. 상태와 근거

상태 숫자: 0=미실행·미수령, 1=기존 고정 계약, 2=이번 작성 측 합성 대조 완료, 3=독립 한정 검토 수령. 운영 자격 등급이 아니다.

| 항목 | 상태 | 근거·범위 |
|---|---:|---|
| T11 계획 API | 2 | `scripts/dem_gen2_t11_contract.py::validate_t11_plan`; 선언 시간·모형·T0 packet·외부 기대 digest 대조 |
| 시험 | 2 | `scripts/test_dem_gen2_t11_contract.py`; 메서드 24/24, 보호 조건 변이 6/6 검출 |
| 정본 준비 요구 | 1 | 바탕 핀의 `docs/reviews/nonrint_approved_preparation_20261109/dem_quantitative_choices_and_t12_contract.md` §3 T11-01–08 |
| 고정 T0 연결 | 1 | `c5ebaa7129869:scripts/dem_gen2_t0_contract.py::validate_t0_contract`; 원 plan+controls 3개를 다시 검증 |
| 기존 작은 오라클·bridge | 1 | 같은 핀의 `scripts/dem_gen2_qualification.py::servo_probe`, `observation_bridge`; 함수 변경 0건. 이번 suite에서 필요한 작은 합성 호출만 사용 |
| 기존 정수 step 규약 | 1 | 같은 핀의 `scripts/make_dem_gen2_decks.py::exact_steps`; 변경 0건. 새 입력 계약을 옛 반올림 결함으로 재계상하지 않음 |
| 실제 T0/T11·등록·빌드·현장 자격 | 0 | 실제 T0 `NOT_RUN`, 실제 부호·빌드·등록 영수증 `null` |
| 독립 검토 수령 | 0 | 이번 후보는 고정 핀 반박 창 검토 대기 |

## 2. 권고안 전제와 비준 경계

| 질문 | 권고 한 줄 | 이번 지원 범위 |
|---|---|---|
| Q-T11-01 | **권고안 전제(Q-T11-01):** 정확 유리수 물리시간이 정수 step/control tick에 대응할 때만 지원 | 오차 허용·round/ceil·예산 자동 연장 없음 |
| Q-T11-02 | **권고안 전제(Q-T11-02):** 유한 case 목록을 사용하고 불안정·비수렴 음성 계획도 보존 | 목록 밖 연속 K/gain/delay 범위 또는 실제 침대 안정성 주장 없음 |
| Q-T11-03 | **권고안 전제(Q-T11-03):** actuator clip과 error clip을 나누어 `error_clip=u_limit/kp`로 결속 | 양의 scalar K/kp/vmax/Ftarget, `0<u_limit<=1`의 선언 toy 모형 |
| Q-T11-04 | **권고안 전제(Q-T11-04):** 계획·T0 packet 바이트와 논리 순서를 별도 전달 context와 대조 | 실제 승인자·벽시계·실행 당시 사용·사전등록 진위 인증은 미지원 |

DEM Q2 정량 선택과 Q4 실제 자격은 미승인이다. Q-T11은 이번 준비의 권고 전제이며 실제 계획의 결과 전 등록을 완료하지 않는다. D9′의 순수 SE 침대·300 MPa 가압/이완 끝·질량 기준 ε_sphere·TD 1.64·외부 10–13 % 표적, ε_union 기록 전용 정책은 유지한다. 근거는 B `13eb293cd9ac:docs/collab/claude_to_codex/20261109-2230_nonrint-first-link-sha-map.md` §2다. toy target force·K·gain·tolerance는 그 표적이나 실제 보정값이 아니다.

## 3. API와 고정 입력

`validate_t11_plan(plan, frozen_context)`는 순수 함수다. 파일·로그·환경·host를 읽지 않고 오라클도 실행하지 않는다. 성공은 `DRAFT_CONTRACT_VALID`, 실패는 `REJECTED`이며 실패에 부분 compile을 반환하지 않는다. 계획 VALID는 모형 수렴 또는 단계 전이 권한이 아니다.

T11 입력은 정확한 내장 dict/list/str/int를 사용하며 bool은 정수가 아니다. 시간·모형 수는 `[numerator, denominator]`로 받고 분모는 양의 정확 int다. T0 원 packet의 이미 지원된 유한 내장 float는 T0 API가 검증한다. raw float·NaN/inf·문자열 숫자·객체 하위형은 T11 rational을 대신할 수 없다. exact dict의 키 타입 확인은 set/hash/equality 전에 수행한다.

context에는 별도 기대 plan SHA256, 기대 T0 packet SHA256, T0 코드 핀, 원 `t0_plan`+`t0_controls`, 합성 freeze/first-observation 순번이 있다. `freeze < observation`과 전달된 기대 hash를 검사한다. **호출자가 context까지 함께 바꾸지 못한다는 인증은 없다.** 논리 순번은 벽시계 영수증이 아니며 hash·코드 핀 문자열 자체의 원격 소속·실행 당시 사용·독립 보관 사실도 조회하지 않는다. 외부 기대 digest를 고정해 두었을 때 계획만 바꾸는 대조가 이번 검증 범위다.

SHA256 규약은 exact built-in JSON의 `sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False`, ASCII bytes다. T0 packet은 `{"synthetic_plan": t0_plan, "synthetic_controls": controls}` 전체다. 원 입력의 파일 바이트를 읽는다는 뜻이 아니라 **정의된 직렬화 표현**의 신원이다. `[1,2]`와 `[2,4]`는 수학적으로 같아도 hash가 다르다. 값의 수학적 정규화나 provenance 인증을 하지 않는다. 순환 객체·JSON depth 64 초과·지원 외 타입은 거부한다.

T0 결속은 fixed code pin·원 packet 재검증·packet digest·같은 run/attempt/unit mapping·선언 합성 raw 부호·z 반력이다. 상태 문자열만 제공할 수 없다. 압축 운동은 현재 계약의 음의 z 방향이라는 별도 선언이다. 합성 T0 부호 `+1/-1` 모두 지원하며 실제 부호를 추론하지 않는다. 단위 ID `GEN2_DECK_FORCE`, `GEN2_DECK_LENGTH`, `GEN2_DECK_TIME`, 물리초 `s`는 선언이며 실제 단위 자격이 아니다. T0 toy 목표 2와 T11 toy 목표 1은 서로 다른 합성 선언이고 같은 실제 하중 사례라는 주장이 아니다.

반환에는 언제나 `actual_T0=NOT_RUN`, 실제 부호·빌드 `null`, `registration_complete=false`, `physical_ready=false`, `execution_go=false`, `gate_write=false`, `operational_seal_modified=false`, 연구 결과 0, `whole_status=HOLD`가 있다. 입력이 실제 관측인지 인증하지도 않으므로 이 함수에 실제 자료를 제공할 권한은 생기지 않는다.

## 4. 정확 시간·모형 사상

`dt_phys = dt_deck × physical_seconds_per_deck_time`이다.

| 사상 | 정확 조건 | 출력 의미 |
|---|---|---|
| `C=control_period/dt_phys` | 정수, C ≥ 1 | control 주기의 step 수 |
| `W=window/control_period` | 정수, W ≥ 2 | 창당 control tick 수 |
| `B=budget/control_period` | 정수, B ≥ 2W, B % W = 0 | 완전 예산의 tick 수 |
| `D=delay/control_period` | 정수, 0 ≤ D < B | 지연 tick 수 |
| dt/2 짝 | `2×dt_half = dt` | 같은 control/window/budget/delay의 물리시간 유지 |

첫 after-control 행은 step C·sample 1·tick 1, step stride C·sample/tick stride 1, 행 B개이며 끝 step BC·tick B다. `e[0]`는 오라클 초기조건이며 after-control 첫 행이 아니다. `window_index=(sample_id−1)//W`다. 실제 run 시작 anchor를 정하는 계약은 이번에 없다.

두 시간 격자는 같은 물리 control/window/budget/delay를 쓰므로 half 쪽 step 수는 두 배이고 W/B/D·물리 끝 시각·control tick은 같다. 실제 DEM의 dt/2 endpoint 수렴 자격을 수행한 것이 아니다.

```text
e = (F_target - F_comp) / F_target
v = -vmax * clip(kp * e_delayed, -u_limit, +u_limit)
a = K * kp * vmax * control_period / F_target
servo_probe.saturation = u_limit / kp
servo_probe.delay = D
servo_probe.budget = B
servo_probe.consecutive = 2 * W
```

`a`와 error clip은 정확 유리수로 반환한다. 기존 float 오라클 인자로 바꿀 때 overflow·underflow 0·비유한·tolerance/divergence 경계의 float 붕괴를 거부한다. 일반 float 근사 자체를 무오차로 인증하지 않는다. 이것은 step 반올림과도 다르다. scalar K=0·음수·비선형 강성·실제 힘/토크/KE/감쇠·재고/에너지 수지는 지원 범위 밖이다.

validator는 a<2 같은 안정성 필터로 음성 계획을 지우지 않는다. a=2·2.2·지연 불안정·포화 비수렴도 유효한 선언 계획이다. 자동으로 모든 필수 물리 음성 목록을 생성하거나 목록 완전성을 인증하지 않으며 명시 유한 목록의 정확 입력만 검사한다. 기존 q 함수의 첫 hit 진단·전체 예산·pending 규칙을 그대로 재사용한다.

정수/분수 크기와 case 수에 별도 유한 자원 상한은 현재 없다. 사용 범위는 신뢰된 작은 합성 입력이며 적대적인 초대형 입력의 시간·메모리 자격까지 검증하지 않았다. 함수는 실제 case나 예산을 실행하지 않으며 시험에서만 아래 작은 오라클을 호출한다.

## 5. 같은 시험의 실행 결과와 독립 기대식

새 `scripts/test_dem_gen2_t11_contract.py`는 24개 메서드다. 기존 오라클 호출·T0 controls·내부 subtest·전후 반복을 더해서 고유 시험 수로 세지 않는다.

| 시험 | 실제 확인 범위 |
|---|---|
| 01–06 | 손 계산 가능한 dt/control/window/budget 격자·dt/2 물리 시간 보존·scale 2·비정수/짧은/불완전 창·잘못된 half·지연 경계 거부 |
| 07 | 무지연 a=1/2·clip 1의 `e[n]=2^−n`을 독립 Fraction 수식과 대조. 최초 hit 7·끝 budget 8 |
| 08–09 | a=2 비감쇠와 a=11/5 발산도 계획 VALID. 같은 a=1/2라도 clip 1/10000이면 예산 내 비수렴 |
| 10 | 작은 지연 대조 a=1/16·delay 32·clip 10·budget 1000: first hit 17 뒤 step 402 불안정. 실제 침대 결과가 아님 |
| 11 | compile grid를 별도로 작성한 합성 force 행과 기존 bridge에 연결. 완전 행·마지막 행 누락·terminal 양호/pending 불량 분리 |
| 12–14 | 원 T0 packet 재검증. hash를 다시 붙여도 틀린 control 거부. 고정 바이트·코드/부호/축/단위/run/attempt 대조 |
| 15–17 | 외부 기대 hash를 유지한 계획 변경 거부. 선언 순서·빈/중복 목록·연속 안정성 주장 거부. 음성 계획 보존 |
| 18–21 | exact rational·지원 영역·float 표현 실패·누락/추가/실제 권한 키·하위형 hook 거부 |
| 22–24 | 입력 무변경·뒤 case 실패에 부분 compile 없음·독립 canonical byte 대조·validator가 oracle을 호출하지 않음 |

일반 양성 recurrence는 독립 수식과 대조했다. 지연 반례는 기존 작은 q 오라클의 회귀 대조이며 실제 비선형 침대 또는 연속 범위 안정성 증명이 아니다. bridge의 합성 force 행은 오라클 error로부터 실제 힘을 역산한 것이 아니다.

## 6. 작성 순서·변이·증거

| 단계 | 메서드 | 실패 | 오류 | rc | 해석 |
|---|---:|---:|---:|---:|---|
| 사전 구현 초안 존재 | 0회 실행 | — | — | — | 원 staging을 보존. 구현 전 TDD 주장 불가 |
| 리포 후보 적용 전 fail-closed 스텁 | 24 | 19 | 0 | 1 | 양성 계약·특정 거부 사유 assertions의 미구현 검출 |
| 동일 시험 + 후보 | 24 | 0 | 0 | 0 | 24/24 통과 |
| 외부 plan digest 비교 제거 | 24 | 6 | 0 | 1 | 계획 변경/동치 분수 바이트 교체 검출 |
| 정확 dt/2 짝 조건 제거 | 24 | 1 | 0 | 1 | 각자 정수 격자여도 잘못된 pair 검출 |
| `limit/gain`을 `limit`로 교체 | 24 | 3 | 0 | 1 | actuator clip/error clip 혼동 검출 |
| dt와 dt_half의 물리 scale 두 줄 제거 | 24 | 1 | 0 | 1 | deck 시간과 물리시간 혼동 검출 |
| T0 재검증 결과의 거부 조건 제거 | 24 | 1 | 0 | 1 | hash만 맞는 잘못된 control 검출 |
| `_exact_count`의 정수성 조건 제거 | 24 | 2 | 0 | 1 | 비정수 control·delay의 잘못된 정수 반환 검출 |

스텁 red는 새 API가 준비되지 않았음을 확인한 것이다. 기존 T0/q 결함의 재현이나 첫 구현 전 반례 설계로 소급하지 않는다. 변이는 고정 후보 복사본에서 검사했고 리포 소스·시험·의존 소스를 수정하지 않았다. 24개 메서드와 6개 변이는 별도 수이며 반복·subtest 실패 개수와 합산하지 않는다.

| 바이트 | SHA256 |
|---|---|
| 스텁 | `d54b98183c4204dd2b31e65110fba026c3fc01ae9b89dbbf41ce34bc5c7b3b43` |
| 후보 T11 | `b12daff4201c7b1424f47e9a558587b5f0216d6207061fbd6bf2de40814cfd59` |
| 전후·변이 공통 시험 | `58324ef5b949372915d1b750cd84917074455a49c39f3f8b9a6bf8790a4cea22` |
| 보존 q | `9bcf11ba48403f1073a0bbd6c6c2d93cbd34d7512c8ff810a48d57493f1f9c2c` |
| 보존 T0 | `1518197eaa68c8baf7e356f0f5fad5cbadc38af5f5455ebade3b2ed8585b84fd` |

Windows Python 3.12.14, `-I -B`에서 고정 copied source를 compile/exec했다. 프로젝트 코드 적재 전에 audit hook으로 프로세스·네트워크를 차단했고 해당 호출들의 금지 시도·실제 engine·원 자료/로그 접근은 각각 0이다. 이는 이 시험 호출의 범위이며 부모 턴 전체의 문서 열람 이력을 대신하지 않는다. 다른 OS/Python, 기존 전체 suite, 전체 gate/CI, 실제 물리·현장 자격 실행은 0회다.

`verification_summary.json`은 시각·rc·출처 SHA·초안 선행 사실과 한계를 기록한다. 전달 증거의 `pre_red_staging/`은 원 초안의 바이트 사본, `red/`와 `green/`은 원 소스·원 로그, `mutants/`는 6개 변이의 원본 보존 대조다. `raw_manifest.json`은 이 묶음의 원시 파일 집합을 결속한다. 파일 시각은 보조 메타이고 독립 등록 진위 증거로 쓰지 않는다.

staging 시험과 red/green 시험의 차이는 첫 docstring에서 미실행 staging 표지를 지운 한 줄뿐이다. 실행 가능한 시험 본문은 같으며 원 staging 바이트도 보존했다. 수령 증거 작성 helper는 처음에 두 파일의 완전 바이트 동일성을 가정했다가 이 차이에서 중단했다. 그 단계의 프로젝트 시험 실행은 0회이며, 차이를 분리 기록한 뒤 문서 증거를 완성했다. 이 메타 작성 중단을 새 본안 시험 실패로 세지 않는다.

## 7. 문서 초안과 남은 경계

`contract_draft.json`은 문서 양식이며 실제 API packet이 아니다. toy 수식 예시를 담되 기대 hash·원 T0 packet은 `null`이므로 그대로 전달하면 거부된다. 실제 build·T0 극성·K/gain·단위/시간 규약·정량 문턱·실행 범위·등록/자격 영수증은 채우지 않았다.

다음은 이번 고정 후보의 독립 한정 검토다. 수용되더라도 실제 T0/T11, DEMP-01 힘 수지, live 관측·정확 경계·T12/P2 ULPR, build/이력/재개/dt/2 자격, 운영 봉인·실행 GO는 별도다. 실제 값 열람·연구 실행·현장 접근·원장 변경 권한은 생기지 않는다. 전체 HOLD.
