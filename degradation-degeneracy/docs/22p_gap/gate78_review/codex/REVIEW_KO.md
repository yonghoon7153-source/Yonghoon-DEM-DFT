# Gate78 — 설계 정정 수용 범위와 제한 오프라인 구현 판정

2026-09-27 · 고정 HEAD의 문서/소스 정적 검토, 파일 무결성 대조, 검토자 소유의 작은 산술 반례만 수행.

## 결론

**G77-N1과 G77-N3는 이번 설계 정정 범위에서 종결 수용한다. G77-N2는 arm·동일 B·단일 scalar 정정은 수용하지만, 관측 행의 pairing과 분모/누락 처리 두 항목이 남는다.** 아래 G78-N1·N2(P1 각 1건)는 이 N2의 잔여이며 새 구현 결함을 발견했다고 주장하는 것이 아니다.

**이미 사용자 승인된 단계 1+2는 수정 조건부로 적합하다.** 잔여를 단계 1 문서에서 반영하고, 단계 2의 로깅/오류 처리만 한정 구현하는 경로를 권고한다. primary 비교기·누락 대체 로직·ID/provider 구현으로 범위를 늘리지 않는다. 문서만의 동일 재심사를 한 번 더 돌리는 것을 필수로 요구하지 않으며, 수정 문서와 한정 구현 결과를 기존 예정 GATE79에서 함께 볼 수 있다. 다만 미수정 §2를 “primary 사전 등록 종결”로 승격할 수는 없다.

이것은 **설계 적합성의 조건부 판정**이다. 사용자 승인 기록(§108, GATE78 §4, 이번 전달문)을 확인했을 뿐 검토자가 새 실행 권한을 부여한 것은 아니다. 이 검토 작업에서는 실제 구현·회귀·복원·영수증 재생성에 착수하지 않았다. **76차 종결 유지, 새 과학 실행 GO 없음, grid_fit_v5 진단/no_active_claim 유지.**

## 1. 고정 대상과 확인 범위

| 항목 | 확인 |
|---|---|
| 요청 HEAD | `720f0a0e466afb595fbd73a50f89416898cc927c` |
| 코드 기준 | `23c361edbfc92fefcfbf0639b5ac40f61f7ebec7` |
| 독립 source digest | `1c67a748598baadb`, RUN_SCOPE 58파일 |
| 코드→HEAD 및 Gate77→78 RUN_SCOPE diff | 모두 0 bytes |
| 계약 본문·CLAIM_STATUS·LEG_PRESERVATION·영수증·artifacts·시험·기존 투영/게시기 | Gate77 HEAD 대비 변경 없음 |
| Gate77 원본 ZIP | SHA `5753ddfc89f1b9ee2f2bd5abd9279cb48ba38e7ebd46c3d05a390093de91ef1d`; 34 payload+manifest, 정확 집합/크기/SHA/CRC 및 보관 사본 34개 바이트 일치 |
| grid_fit_v5 | 29파일 / 27,313,017 bytes, 구성원 SHA와 receipt core/out 결속 확인. 진단 전용 그대로 |
| 고정 checkout 보존 | tracked 2,995파일. 전후 동일 및 clean 확인은 `PRESERVATION_AFTER.json` |

`DATA_AUDIT.json`은 위 데이터 확인이다. 기존 receipt가 기록한 복원/검증/재채점을 이번에 재실행한 것은 아니다. 송신 측 pytest 1,944 PASS/2 xfailed, docs-lint 358 PASS는 **기존/송신 측 실행 기록**으로 유지하며 독립 검토 건수에 더하지 않는다.

## 2. 종결 수용한 부분

### G77-N1 — 수용

12-L의 로컬/협조적 실행·보관·복원과 12-P의 운영 retention/CAS/registration/canary가 분리됐다. 묶음 8·9도 local 하위 범위와 provider 잔여를 구별한다. profile **선택 1 유지**라는 사용자 결정이 기록돼 있고 첫 pilot 전 별도 gate가 남는다. E1/E2/E4와 혼동하지 않는다.

이는 **상태 정정의 종결**이지 12-P 구현·운영 canary의 종결이 아니다. 이미 확인한 로컬 실물 근거를 다시 시험할 필요가 없다.

### G77-N3 — 수용

미정인 최종 채택 B와 pilot 전 고정해야 할 ladder/max/미채택/floor/provider/panel/자원 항목을 나눴다. candidate_id/bank_index를 단계 3으로 미뤘고 단계 2를 로깅·parquet 오류 처리로 한정했다. `[5,10,20,40]`, 최대 40, 미달이면 추가 증량 없이 미채택은 **설계 제안으로 수용 가능**하다. 이 수용이 floor·pilot 실행 승인은 아니다.

실제 budget-adoption을 구현할 단계 5 전에는 “연속 두 doubling이면 **그 N**”을 정확히 정의해야 한다. 예를 들어 5→10·10→20 통과가 채택 5/10/20 중 무엇인지와, 40까지 이미 계산한 prefix 진단을 어디까지 보고할지 명시한다. 이는 이번 단계 1+2 착수를 막는 새 차단 항목이 아니라 후속 알고리즘 명세 항목이다.

### G77-N2 — 수용된 축

grid, p_ini=null, 두 warm=false, 실제 `[base_init]+bank[:B-1]`, 두 objective 동일 B·bank prefix·bounds, 단일 Δ와 네 칸 분해, secondary 분리·union 제외, 기술통계 범위는 수용한다. 다음 두 잔여만 닫히면 해당 primary 문장의 정합성을 다시 판단할 수 있다.

## 3. G78-N1 · P1 — pair_group_id는 공통 bank의 그룹이지 유일한 관측 쌍 key가 아니다

**좌표:** `GATE78_REQUEST.md:58–60`; `STAGE3_CONTRACT.md:201–269`; `src/grid.py:88–114`.

요청은 treatment·noise·noise_seed·objective를 제외한 pair_group_id를 정확히 인용했다. 문제는 다음 행에서 **condition = 한 pair_group_id의 두 fit 쌍**으로 정의한 것이다. 같은 물리좌표의 noise/seed가 여러 개면 한 그룹에 각 objective의 행이 여러 개다. 동일 그룹의 bank를 공유하는 것과, 같은 잡음 실현의 두 objective를 짝짓는 것은 다르다.

현행 `Condition.cond_id`는 noise/seed까지 포함한 dataclass 전체에서 도출된다. 계약 §4.3도 `cond_id → pair_group_id`의 mapping과 중복도를 구별한다. 그 mapping의 SHA만으로 어느 관측끼리 비교할지가 자동 결정되지는 않는다.

검토자 제작 예:

| 동일 pair_group G의 관측 | 33p | 34p |
|---|---|---|
| seed s1 | pass | fail |
| seed s2 | fail | pass |

정상 짝은 2개, 전이표는 PF=1·FP=1이다. group만으로 join하면 4행이 생겨 PP/PF/FP/FF 각 1개가 된다. 이 예에서는 Δ가 우연히 0으로 같아도 **분모와 필수 전이 분해는 틀린다.** first/last 한 행 선택 역시 어느 seed를 버리는지 정의되지 않았다.

**최소 수정:** pair_group_id/bank ID의 정의는 바꾸지 말고, 별도 **관측 쌍 key**를 적는다.

- 승인된 비교-family/primary arm 범위 안에서 `pair_group_id + treatment + noise_level + noise_realization_id(또는 정확 seed) + 반복 식별(있을 때)`로 각 관측을 구분한다. 이번 primary에서 고정인 축은 고정값으로 명시한다.
- 같은 key에 objective 두 개가 정확히 한 행씩 있어야 한다. objective는 비교의 두 열이지 동일 key의 같은 값이 아니다. reference/bounds/조건 입력 identity도 동일성 제약으로 대조한다.
- 봉인된 cond_id를 사용하는 간단한 설계도 가능하다. 다만 위 축과의 일대일 관계·충돌·중복 거부를 명세에 넣는다. 서로 다른 leg를 무조건 같은 cond_id로 합치지는 않는다.
- planned denominator는 이 key의 사전 집합에서 세고, 한쪽 행 부재도 그 집합에서 발견한다. 중복·교차 seed pairing은 누락 민감도 대상이 아니라 구조 오류다.

**종결 기준:** 그룹 ID와 관측 key를 별도로 정의하고 one-to-one/중복/교차 seed 거부 및 planned roster 기준을 문서에 고정한다. 실제 ID 코드 변경은 승인된 단계 2가 아니라 이후 단계 3의 일이다.

## 4. G78-N2 · P1 — missing-as-fail은 Δ의 worst-case가 아니며 5%는 zero-failure gate와 분리해야 한다

**좌표:** `GATE78_REQUEST.md:61–64`; `STAGE3_CONTRACT.md:316–350,445–477`; `src/scoring.py:6–11,75–102,318–345`.

### 4.1 방향이 다른 두 outcome에서 fail 대입은 한 방향의 worst-case가 아니다

raw-degeneracy fail을 1, pass를 0으로 쓰면 각 쌍의 기여는 `d = y34 − y33`이다. 양수는 34p에서 실패가 더 많다는 뜻이다.

| 관측 | 누락을 fail로 대입한 d | 가능한 d의 범위 |
|---|---:|---:|
| 33 누락 / 34 pass | -1 | [-1, 0] |
| 33 pass / 34 누락 | +1 | [0, +1] |
| 33 누락 / 34 fail | 0 | [0, +1] |
| 33 fail / 34 누락 | 0 | [-1, 0] |
| 양쪽 누락 | 0 | [-1, +1] |

첫 행은 34p에 **가장 유리한 쪽**이고, 양쪽 누락은 가장 불리한 +1을 놓친다. 따라서 현재 Δ_worst는 일반적인 worst-case가 아니다. 실패를 operational outcome으로 정의한 별도 composite estimand라면 가능하지만 raw-degeneracy 민감도 bound와 같은 것은 아니다.

**40쌍 반례:** complete 38쌍의 d 합=+1, 나머지 2쌍은 모두 33만 누락·34 pass다. 누락률은 정확히 5%라 요청의 `>5%` 조건은 작동하지 않는다.

- complete-pair Δ = `1/38 ≈ +2.632%p`.
- 누락-as-fail 후 전체 40쌍 Δ = `-1/40 = -2.5%p` — 34p에 유리한 방향으로 뒤집힌다.
- 알려진 한쪽 결과를 유지한 전체 40쌍의 가능한 범위는 `[-1/40, +1/40]`. 요청의 worst는 상한이 아니라 이 예의 **하한**이다.

### 4.2 명세를 닫는 최소 수식

사전 고정한 분석 대상 관측 쌍을 N, 그중 평가 가능한 complete-pair를 n, 누락 쌍을 m=N−n, 관측된 complete d의 합을 D라 하자. 누락은 **쌍 단위**이며 양쪽 누락도 1쌍이다.

- complete-pair 통계: `Δ_cc=D/n` (n>0). 전체 planned set 결과가 아니라 **양쪽이 관측/수렴한 부분집합의 조건부 기술통계**라고 적는다.
- 전체 planned set 민감도: 각 누락 쌍의 알려진 쪽은 유지하고 미관측 label만 0/1로 놓아 `l_i=min d_i`, `u_i=max d_i`를 구한다. `Δ_lower=(D+Σl_i)/N`, `Δ_upper=(D+Σu_i)/N` (N>0).
- 단순하고 더 넓은 보수 범위를 원하면 `[(D−m)/N,(D+m)/N]`도 가능하나, 한쪽 관측 정보를 일부 버리는 bound임을 표시한다.
- 상·하한은 새 co-primary 두 개가 아니라 같은 Δ의 누락 민감도 범위다. 신뢰구간/p-value/누락 무작위성 가정을 뜻하지 않는다. n=0이면 Δ_cc는 미정, N=0이면 전체 지표도 미정이다.
- “fail” label을 만들 수 있는 truth·복원값·채점 필드의 유한성과 유효성도 필요하다. 유한 J와 converged만 보고 NaN parameter/정의되지 않은 label을 pass로 채우지 않는다.

### 4.3 분석 대상과 5% 정책

complete-pair를 정의하기 **전에** 분석 대상 N의 사전 inclusion mask를 고정해야 한다. 기존 §7.1의 prior는 recoverable 조건이고 현행 scoring의 주 지표도 recoverable 군을 분리한다. 새 표의 “조건 수”가 전체 생성 격자인지 그 군인지 명시하지 않았다. 기존 의미를 유지하려면 geometry/reference로 정하는 recoverable mask를 사전에 결속하고, 구조적 제외와 solver 누락을 별도 집계한다. 전체 격자를 새 대상으로 선택하려면 이것도 명시적인 estimand 변경이다.

§6.2의 solver-health 조건은 **실패·비유한 0건**이다. 요청의 5%는 별도 reporting 정책일 수는 있지만 그 gate의 완화로 취급할 수 없다. 예를 들어 100쌍 중 실제 solver failure 1건은 `>5%`는 아니어도 zero-failure gate에는 실패다. 미수렴을 어떤 phase/단위에서 실패로 셀지도 분리해야 한다.

**최소 권고:** zero-failure plateau gate를 그대로 유지하고, 누락이 생긴 결과의 Δ_cc/bounds는 진단·미완 보고로 분리한다. 5%를 유지하고 싶다면 **결측된 primary의 보고 가능성에 관한 별도 사전 정책**임을 적고, §6.2 통과 또는 전체 planned set의 관측 완료를 뜻하지 않는다고 명시한다. “5%라 과학적으로 안전하다”는 근거는 이번 자료에 없으며 이 리뷰도 부여하지 않는다. zero-missing primary를 선택하면 가장 단순하지만, 그것을 이미 사용자 선택으로 기록하지는 않는다.

**종결 기준:** N/n/m과 대상 mask, Δ_cc와 전체 집합 bound의 분모, 양쪽/한쪽 누락 및 zero denominator, 5%와 solver gate의 관계를 문서에 고정한다. 이번 단계 2에 새 분석기/대체 로직 구현을 추가하라는 요구가 아니다.

산술 근거는 `DESIGN_ARITHMETIC.json`이다. 9개 label 상태 및 작은 가상 표를 검토자 코드로 계산했으며, 제공 suite나 실제 데이터/solver는 실행하지 않았다.

## 5. 요청 §5 답과 구현 경계

| 질문 | 답 |
|---|---|
| ① 12-L/12-P·8/9·profile 1 | **예. G77-N1 정정 종결.** 12-P는 여전히 부분/첫 pilot 전 gate다. |
| ② primary 한 행 | warm/B/scalar/secondary는 수용. **관측 key와 분모·누락은 G78-N1/N2 수정 필요.** 현재 문구 그대로 등록 완료 아님. |
| ③ ladder/max/미채택·floor | **설계 제안 수용. G77-N3 정정 종결.** floor 승인과 budget-adoption 판정 분리 유지. 채택 N의 정확한 위치는 단계 5 전에 정의. |
| ④ 단계 1+2 범위 | **수정 조건부 적합.** 아래 좁은 해석으로 기존 사용자 승인 범위의 코드 라운드를 진행할 수 있다. 이번 검토자는 실행하지 않는다. |
| ⑤ 실행 GO 아님·진단 전용 | **예.** pilot/본 계산/provider canary/floor/class/투영 승격 없음. |

단계 1+2의 좁은 해석:

1. 단계 1에서 위 두 잔여를 정정하거나 아직 미확정인 설계로 정확히 남긴다. 미수정 primary를 정본이라고 쓰지 않는다. 이 설계 상태와 무관하게 새 comparator/ID/provider/adoption 구현으로 넘어가지 않는다.
2. 단계 2는 restart별 `converged/termination_status/n_eval` 보존과 parquet 읽기 실패 구조화다. 기존 optimizer 초기값·후보 선택·횟수·tolerance·J/p·scoring 정의를 바꾸지 않는다. 수치 동작 변경이 필요하면 별도 범위로 회신한다.
3. 종료 사유는 solver의 native 종료와 `_minimize_until_stable` 바깥 반복의 종료 사유를 구별한다. 이 함수는 내부 minimize를 여러 번 호출하며 best p/J와 마지막 반복이 다를 수 있다. 어떤 결과/반복의 상태를 기록하는지 명세·회귀로 연결하고, 새 `converged` 의미를 조용히 바꾸지 않는다. 이는 로깅 구현의 수용 기준이지 현 코드를 이번에 수정한 결과가 아니다.
4. historical reader는 옛 restart 필드 부재를 그 세대의 미기록으로 취급한다. false/0/가짜 native status를 과거의 실제 관측값처럼 채우거나 v6 완료로 승격하지 않는다. 입력/과거 fits 바이트 보존, 구조화 실패 이유, 기존 수치 결과 불변을 검증한다.
5. 요청 §4:115의 “복원 안 함”과 :116의 receipt 재생성 허용은 **기존 대상 leg의 영수증 검증용 격리 복원만 예외로 허용, 다른 복원 금지**로 정리한다. 사용자가 receipt의 restore/validate/rescore를 명시 승인했다고 이번 메시지와 §108에 있으므로 다시 승인 전체를 묻지는 않는다. 다만 실제 대상 leg 목록과 final digest를 시작 전에 고정한다. 현재 근거 대상은 기존 `grid_fit_v5`와 `paired_fixed5_v4`이며 다른 leg를 임의로 추가하지 않는다.
6. strict smoke는 이름만 정적인 검사가 아니다. 코드상 작은 grid/fit/score/restore를 수행한다. 사용자가 승인한 회귀·strict smoke 범위의 검증 계산과 **새 연구용 leg/floor/pilot 0회**를 구분해 기록한다. “solver 호출 총 0”이라고 쓰면 안 된다. 운영 실행/class/투영 상태를 바꾸는 별도 시나리오로 확대하지 않는다.
7. 최종 코드 고정 뒤 leg별 receipt 재생성·원본 history 보존·새 validator 식별 대조. 중간 receipt로 현행 PASS를 주장하지 않으며, 실패를 숨기거나 새 code identity를 과거 producer 값에 소급 쓰지 않는다.

§4의 미래 실행 권한은 이번 사용자가 보고한 범위와 원장 기록에 근거한다. 첨부 문서만을 승인으로 취급하지 않았다. 요청 머리/끝의 “승인 요청/승인 대기” 잔여 문구는 §108의 최신 상태인 **사용자 승인됨·78차 회신 후 한정 착수**로 통일하면 된다. 이는 비차단 기록 정리다.

## 6. 다음 전달물 — 추가 계획 루프를 늘리지 않는 범위

다음 GATE79에는 **G78-N1/N2 수정 문장 + 단계 1+2의 제한 diff·수치 불변/역사 reader 회귀 + 허용된 검증·receipt 결과**를 함께 제출하면 된다. primary 설계를 고치려고 실제 새 primary 데이터를 계산할 필요가 없다. 단, 실험 결과 없이 닫히는 문서 반례를 그대로 둔 채 claim만 등록하는 것은 수용하지 않는다.

이번 범위 밖: 단계 3–6 구현, provider 설정/canary, numerical floor/pilot, 새 연구 계산, COMSOL/Java 실행, class/투영 승격. 76차 종결·기존 실패/승인 편차·원본 영수증과 진단 제한은 유지한다.

## 검토 한계

이 검토는 고정 checkout의 정적·데이터 관측이다. 등록부·원격 전체 파일·외부 provider·실제 CPU나 solver는 재측정하지 않았다. 검토자 산술 반례는 새 source 회귀 통과 수가 아니다. 조회 중 잘못된 상대 경로 1건은 올바른 절대 경로로 다시 읽었으며, 이를 대상 프로그램 실패로 분류하지 않았다.
