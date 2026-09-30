# LHS 피복률 재검증 2 판정

## 결론과 검토 범위

**HOLD. 기존 반례의 수정은 재현됐다. 새 P1은 발견하지 않았으나, LHSC-03의 스키마 결손과 LHSC-04의 생산자 오차 보증·검출력 표시에 P2 잔여가 있다.**

이번 결과가 수확 피복률 값의 오염, 실 130/64 침대에서의 발생, physics v2의 물리적 부당성을 증명하는 것은 아니다. 진단 기록과 필수 단계 완료 표지가 **어디까지 보증하는가**가 남은 쟁점이다. 닫힌 P1 두 건을 다시 열거나 정상 피복률을 바꿀 이유는 발견하지 않았다.

- 일자: 2026-09-30, 한국 시간.
- 입력: `codex_lhs_coverage_reverify2_20260930.zip`, 30,334 bytes, SHA256 `8761667a740c0962502c12db5605fd1c7b43d1ab1110267de1df13051275b235`.
- 기준: 이전 독립 재검증 후보의 대상 9파일 SHA가 보존 원장과 일치함을 먼저 확인했다. 그 **비 Git 소스 사본**에 0012 → 0013을 `git apply --check` 후 적용했다.
- 제출자가 선언한 base는 `002cc288119f520a818fcb50a3f73ec87fb06e70`, tip은 `ca0471d19a5a9d914c6a31006a001d515267f3be`. 로컬 전용 브랜치의 커밋 실재를 별도 인증한 것은 아니다. 이 리뷰의 실물 핀은 **패치 바이트·diff 본문·적용 후 파일 해시**다.
- 패치 2개의 바이트/크기/diff 본문 해시 및 `SHA256SUMS` 7항목 전부 일치. [독립 소스 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/source_manifest.json).
- 생산 저장소·Git ref·원장·문턱은 수정하지 않았다. DEM, 원격 캠페인, 재수확, coverage 실 배치는 실행하지 않았다. 아래 실행은 격리 사본의 CPU 합성 시험이다.

| 항목 | 재판정 | 해제된 부분과 남은 부분 |
|---|---|---|
| LHSC-01·02·05·06 | 앞 판정 유지 | 이번 수정에서 되돌아간 증거 없음. 옛 수확 36키 × 16호출 불일치 0 |
| LHSC-03 / 0013 | **부분** | 옛 변이 10종 거부, 생산자 양성 8종 허용. 그러나 분모가 있는 분율의 누락/None 및 비어 있는 개수 원장이 `done` |
| LHSC-04 / 0012 | **부분** | 옛 공동 반올림 반례 해제, 실수 기하의 구간 구성은 타당. 생산자 binary64 오차의 전역 보증 및 `n_power_1pct` 의미는 반례 있음 |

## Q1 반올림 상자 포괄성

**실수 산술의 구조에는 동의. 아래 양수 반경·유한 정상 크기 입력 시험에서는 구간 자체의 반례를 찾지 못했다. 이것을 모든 binary64 입력에 대한 정형 증명으로 부르지는 않는다.**

[구간 구성:395](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:395), [편도함수와 꼭짓점:433](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:433), [경계 가지:460](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:460).

`d=r1+r2−δ`, `f1=2r1−δ`, `f2=2r2−δ`, `f3=2r1+2r2−δ`라 두면 내부의 면적은 `A=πδ f1 f2 f3/(4d²)`다. 코드의 세 로그 편미분은 각각 다음과 맞는다.

~~~text
∂log A/∂r1 = 2/f1 + 2/f3 − 2/d
∂log A/∂r2 = 2/f2 + 2/f3 − 2/d
∂log A/∂δ  = 1/δ − 1/f1 − 1/f2 − 1/f3 + 2/d
~~~

상자 전체가 양의 인수 영역에 있고 이 세 **포괄 구간**이 각각 0을 배제하면, 각 좌표에 대한 방향이 상자 전체에서 고정된다. 따라서 그 부호로 고른 두 꼭짓점이 실수 함수의 정확한 최소·최대다. 이는 옛 “모든 입력에 원래 단조” 주장과 다르며 정당하다. 편미분 부호를 인증하지 못하면 구간 곱/덧셈형/기하 상한의 교집합을 쓰는 것도, 각 구간이 바깥쪽으로 계산됐다는 전제에서 옳다. 경계 가지는 하한을 0으로 내려 비접촉·포함·동심 퇴화를 포함한다.

독립 검산은 제출자의 샘플을 재사용하지 않았다. seed=20260930, 반경 r1=10⁻⁶–10⁻¹ sim, r2/r1=10⁻²–10²에서 얕은 접촉·일반 겹침·포함 경계·거의 동심·극값·음수 δ·완전 포함·일반 전 구간을 만들었다. **12,000 상자 × 24점 = 288,000점**을 80자리 Decimal의 독립 원판 식 및 실제 `lens_geometry` 함수로 각각 대조했다.

| 방법 | 상자 수 | Decimal / 실제 함수 이탈 |
|---|---:|---:|
| corner | 6,489 | 0 / 0 |
| zero | 4,099 | 0 / 0 |
| interval | 429 | 0 / 0 |
| boundary | 983 | 0 / 0 |

옛 R2 반례 `(0.00123456, 0.00123456, 0.00246909, 4.27727e-6)`은 구간 **[2.660084532696906e-6, 4.7882607651360736e-6] sim²**와 만나므로 초과 0이다. 폭 넓은 행 1로 기록된다. 옛 깊은 겹침 세 사례도 제출표대로 rounding=0, Hertz=0, 3e-5 치환=1 초과였다. 비접촉 0면적 대조는 허용하고, δ=0인데 양수 면적인 대조는 검출했다.

한정: 양수 반경의 실수 기하, 그 로컬 함수, **실제 LIGGGHTS 생산 산술**은 같은 인증 대상이 아니다. 마지막 항은 다음 Q2가 남는다. 언더플로·오버플로를 포함한 모든 유한 double 범위를 인증하지 않았다.

## LHSC-04-R3a 생산자 부동소수 오차의 보증은 닫히지 않음

**P2. Q2는 현재의 전역 주장에 반대.** 무너지는 결론은 “`32·eps·π·max(r)²`를 더하면 LIGGGHTS 생산자 계산 오차까지 덮는다”이다. **Q1의 실수 기하 포괄성 자체를 반박하는 것은 아니다.**

위치: [고정 fp 여유:421](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:421), [기하 cap과 결합:461](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:461).

요청서의 “LIGGGHTS 덧셈형”이라는 전제부터 구별해야 한다. 09-30 열람한 [공식 PUBLIC `add_pair` 소스](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/src/compute_pair_gran_local.cpp)는 좌표 거리 `r=sqrt(rsq)`를 구한 다음 **거리 기반 네 인수의 곱을 rsq로 나누는 형태**다. 로컬 `lens_geometry`의 두 제곱 차와 평가 순서가 다르고, 그 자리에서 음수 면적을 0으로 자르지도 않는다. 실수 항등식이 같다는 사실만으로 부동소수 오차가 같지는 않다.

공식 식의 연산 순서를 보존한 binary64 스칼라 계산과 **실제 `contact_area_check`**를 연결했다. DEM 엔진이나 설치된 생산 바이너리를 실행한 시험은 아니다.

~~~text
r1 = r2 = 0.001 sim
실제 중심거리 = 1.0e-15 sim   (d/r = 1.0e-12)
생산 식의 δ       = 0.001999999999999 sim
생산 식의 A       = 3.142020451916476e-6 sim²
실수 기하 상한    = 3.1415926535897933e-6 sim²

6자리 토큰 = (0.001, 0.001, 0.002, 3.14202e-6)
검사 구간 = [0, 3.1416240695948997e-6] sim²
n_tested = 1, n_beyond_tol = 1
~~~

`r+r1−r2` 등의 작은 인수가 큰 반경과의 덧셈·뺄셈에서 반올림되고, 나눗셈에서 그 오차가 증폭된다. `eps·r²`만으로 거리와 무관하게 덮을 수 없다. 이 사례에서는 변조 없이 생산 식을 %.6g로 적었는데 초과다. 반대로 d=1e-16 sim 사례는 오차가 아래쪽이고 넓은 구간 안에 남아 초과 0이다. 단순히 “더 깊으면 반드시 초과”라는 주장도 하지 않는다.

별도 구분: r1=.002, r2=.001, d=.0009 sim인 완전 포함에서는 공개 생산 식이 **−1.5088371383490986e-6 sim²**, 로컬 함수는 0을 낸다. 이것은 부동소수 바닥으로 해결할 차이가 아니라 **정의역 밖 생산값과 클립된 기준 기하의 의미 차이**다. 음수 원면적을 진단하는 것은 합리적이지만 “정상 반올림 여부 검사”와 같은 사유로 묶지 않는다.

한정: 동심 근접 반례는 매우 극단적이다. 실 LHS 발생률은 미측정이고, 공개 master와 사용자의 설치 빌드가 같다는 증거도 이번 ZIP에는 없다. 따라서 “실 130건이 오탐”이라고 결론 내리지 않는다. 다만 그 미확인을 생략하고 **생산자 전체에 대한 보증**을 선언할 수는 없다.

**최소 해제:** 실제 생산 빌드의 식·컴파일 규약을 핀하고, 지원 수치 영역에서 오차 한계를 도출하거나 불안정/정의역 밖 행을 별도 미인증 상태로 센다. 거리 하한이 0에 닿는 상자까지 고정 eps 여유 하나로 인증하지 않는다. 넓은 실수 기하 구간과 생산자 오차 미인증을 서로 다른 상태로 남긴다. 32를 임의로 키우는 것은 해결이 아니다.

재현: `python evidence/audit_producer.py`. [수치 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/evidence/producer_results.json).

## LHSC-04-R3b 폭의 분류를 1퍼센트 검출 보증으로 읽을 수 없음

**P2. Q3는 방향에 동의하나 현재 표지에는 수정이 필요하다.** 모든 행을 시험하고 검출력 부족을 공개하는 설계는 좋다. 그러나 `n_power_1pct`는 실제 보증과 다르다.

위치: [폭 분류:509](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:509), [검출력 개수:520](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:520), [등록 의미:166](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/scripts/lhs_descriptor_harvest.py:166).

반올림 전 입력과 원 면적:

~~~text
r1    = 0.003484275000005 sim
r2    = 0.0016462850000049998 sim
delta = 0.003289594999995 sim
A     = 5.816751192126276e-8 sim²

길이 토큰 = (0.00348428, 0.00164629, 0.00328959)
포괄 구간 = [5.816736279407535e-8, 5.8753032122697924e-8] sim²
정상 면적 토큰       = 5.81675e-8 sim²
1.01 A를 적은 토큰   = 5.87492e-8 sim²  (+1.00002227966125 %)
~~~

| 실제 함수 출력 | 정상 토큰 | +1% 치환 토큰 |
|---|---:|---:|
| n_beyond_tol | 0 | **0** |
| n_lower_bound_zero | 0 | 0 |
| n_wide_enclosure | 1 | **0** |
| n_power_1pct | 0 | **1** |
| (hi−lo)/A_dump | 0.0100686694223161 | 0.00996897538387879 |

면적을 +1% 바꾸자 검출은 하지 못하면서 오히려 “1%를 잡을 수 있는 행”으로 분류한다. 분모가 검사 대상인 `A_dump`여서 폭 분류까지 바뀌기 때문이다. 이는 “정상 원본에서 이미 power=1인 행을 변이했는데 놓쳤다”는 다른 주장과 구분한다. 반례는 **현재 보고서가 변이된 행에 power=1을 찍는다는 것**이다.

또한 `n_lower_bound_zero`는 실제 `lo==0`이 아니라 **boundary 가지 진입 수**다. zero 가지와 fp를 빼고 0으로 클립된 corner 가지에서는 lo=0이어도 이 개수가 0이다. 예를 들어 `(r1,r2,δ,A)=(.002,.001,.0021,0)`은 lo=0·방법 zero·`n_lower_bound_zero=0`이다. 이 부수 라벨 오류는 P3이며, 아래 최소 수정으로 함께 해소할 수 있다.

**최소 해제는 둘 중 하나다.**

1. 현재 통계를 그대로 둘 경우 이름·설명을 `상대 구간폭 ≤1%인 양수 덤프 행`, `경계 가지 행`처럼 **폭/분기 기술량**으로 낮춘다. 검출 가능/불가능의 증명이라고 부르지 않는다.
2. 실제 1% 보증이 필요하면 참 면적이 `[lo,hi]` 어디에 있더라도 ±1% 치환의 **토큰 구간**이 원 구간과 분리되는지 검사한다. 면적 출력 반올림도 포함하고, 미인증 생산자 오차 행은 제외한다. 참 면적 기준 ±1%라면 개념적으로 `1.01·lo > hi + 출력반올림 여유`, `0.99·hi < lo − 출력반올림 여유`의 양쪽을 인증해야 한다. 이것은 이번 리뷰의 코드 구현 제안이 아니라 필요한 보증의 정의다.

폭 넓은 행을 버리거나 피복률을 바꾸라는 요구가 아니다. 현재 구간 교차 시험과 별도 기술 통계를 유지해도 된다.

재현: `python evidence/audit_power.py` (고정 seed, 431번째 상자에서 발견). [전체 입력·출력](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/evidence/power_results.json).

## LHSC-03-R3 값이 없는 분율과 빈 원장도 완료로 받음

**P2. Q4는 부분 해제.** 옛 10종 변이는 모두 거부하고, 실제 생산자 양성 8종은 모두 허용했다. 특히 n_am 부재와 면적 NaN은 실제 `_coverage_stage` → `summarize`에서 **failed**다. 이 수정은 유효하다.

남은 위치: [개수 dict 검사:3243](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/webapp/app.py:3243), [분율 조건:3247](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/webapp/app.py:3247), [AM 없음 반환:3258](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/candidate/webapp/app.py:3258).

실제 `compute_case` 정상 산출물은 접촉 **11**, cap 가지 **9**, cap 충돌 **2**, 두 분율 **0.181818 / 0.222222**다. 여기에서 다음 변경만 했다.

| 변이 | 검증기 | 실제 필수 단계 |
|---|---|---|
| 두 분율 키 삭제 | True | 직접 검증기 호출 |
| 두 분율을 None으로 변경, n=11/ncap=9/nconf=2 유지 | True | **done** |
| 세 개수 dict를 `{}`로 변경 | True | **done** |
| 총 결속 원장 elastic 개수를 1,000,000으로 변경, n=11 유지 | True | 직접 검증기 호출 |
| nconf=0인데 전체 충돌 분율=1 | True | 직접 검증기 호출 |
| 실제 SE-only 산출물(n_am=0)에 AM–SE 면적 123 μm²만 삽입 | True | **done** |

분율은 “키가 있고 None이 아닐 때만” 범위를 보므로 **분모가 양수인 누락도 면제**한다. dict는 값에 대한 `all`만 검사하므로 빈 dict가 참이다. 이는 물성이나 피복식을 다시 구현하지 않고도 막을 수 있는 **스키마 완전성·집계 항등식**이다.

실제 필수 단계 시험은 계산 subprocess만 변이 파일을 쓰는 대역으로 바꿨다. 검증기·필수 단계·최종 요약은 실제 함수다. **현재 정상 생산자가 이 잘못된 파일을 만든다고 주장하지 않는다.** 무너지는 결론은 “done이면 필수 v2 값·진단 원장이 온전하다”이다.

**최소 해제:**

- 두 분율 키는 존재해야 한다. `n>0`이면 전체 분율, `ncap>0`이면 cap 가지 분율을 유한 값으로 요구하고, 해당 분모가 0일 때만 None을 허용한다. 생산자의 6자리 반올림 규약에 맞춰 개수의 비와 대조한다.
- 개수 dict의 필수 분류 집합과 총합을 검사한다. `sum(A_binding_counts_total)=n`, `sum(cap_conflict_n_by_pair)=nconf`, AM–SE 결속 개수는 총 결속 개수 이하라는 집계 규약을 별도 시험한다. 결속 원장을 다시 계산하라는 뜻이 아니다.
- n_am=0이면 AM 관련 면적이 0이어야 한다. 접촉 0과 양수 총 접촉면적 등 명시적 모순을 거부한다. 이것을 SE-only의 정상 0과 혼동하지 않는다.
- 위 변이와 실제 생산자 8종을 함께 상주 회귀에 둔다. 결손을 기본 0으로 채우지 않는다.

**blank의 rule=None에는 동의.** 물리 값이 전부 None/부재이고 사유·진단 키가 있는 내부 오류 기록은 빈칸 판정으로 보존할 수 있다. 실제 양성 대조를 막으면서 문자열만 강제할 이유는 없다. 단 blank의 `h_film_sim_physics_v2='broken'`도 현재 허용된다. 이건 물리 값 유출과 다른 P3 메타데이터 타입 보완 사항이다. 유효한 None은 유지하고, 값이 있으면 유한 양수로 검사하면 된다.

참고로 `10**400` 면적은 직접 helper에서 OverflowError지만 필수 단계는 그 예외를 잡아 failed로 만든다. 이를 false-green이나 신규 P1으로 세지 않았다.

재현: `python evidence/audit_schema.py`. [생산물·변이·단계 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/evidence/schema_results.json).

## Q5 병합 순서와 최소 해제

의존 순서 **0001 → … → 0013 → 최종 게이트 → 최종 트리 해시 고정 → 새 디렉터리 재수확/coverage 배치**에는 이의 없다. 다만 **지금 03·04까지 일괄 claimed_fixed로 종결하는 데는 반대**한다. 다른 항목의 닫힘 근거는 보존한다.

추가 코드 수정과 재판정 후 진행한다. 이번 리뷰가 실제 병합·원장 수정·배치 실행을 대신하지 않는다. 후보 physics v2의 소프트웨어 계약 GO와 물리 모델·학습 코퍼스 적격성 GO도 분리한다.

남은 최소 목록:

1. **LHSC-03:** 양수 분모의 분율 누락/None, 빈 개수 원장, 명시적 집계 모순을 막는다.
2. **LHSC-04 / Q2:** 실제 생산 산술과 빌드를 핀하고, 수치적으로 인증 못 하는 행을 별도로 표시한다. 실수 구간 증명을 생산자 전역 오차 보증으로 확장하지 않는다.
3. **LHSC-04 / Q3:** `n_power_1pct`를 폭 기술량으로 재라벨하거나, 출력 반올림까지 포함한 검출 보증을 구현한다. 하한 0/경계 분기 이름도 실제 의미와 맞춘다.

## 독립 실행과 한계

| 시험 | 독립 결과 |
|---|---|
| lens_geometry | 7 check, rc=0 |
| plastic_coverage | 28 check, rc=0 |
| coverage_physics_vs_hertzian | 16 check, rc=0 |
| webapp/test_pipeline_provenance | **209/209**, rc=0 |
| 수확기 원형 | 실패 2: fixture CRLF 해시와 τ median 핀 |
| 수확기 LF fixture 통제 | 실패 1: τ median 핀. 이번 새 구간 시험들은 통과 |
| τ 플랫폼 대조 | baseline/candidate 둘 다 median=2.080532952769607, 고정 핀 2.0805329527696066과 1 ULP 차이. 새 회귀로 세지 않음 |
| legacy 수확량 | 16호출 × 36키, 불일치 **0** |
| lhs_webapp_batch 원형 | Windows symlink 권한 WinError 1314로 실패 |
| symlink만 byte-copy로 치환한 통제 | rc=0. 배포 환경 symlink 성공 증서 아님 |
| 전체 check_all | 독립 실행하지 않음 |
| 원시 실 130/64 / 실제 LIGGGHTS 바이너리 | 실행·재수확하지 않음 |

원형 실패를 숨기거나 “전수 초록”이라고 요약하지 않았다. 무작위 스트레스 시험은 정형 증명이 아니고, 정상 생산자 양성 8종은 가능한 모든 침대의 인증이 아니다. `plastic_coverage` 미적재는 별도 깨끗한 수확기 import 과정에서도 유지됐다.

[증거와 재현 안내](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify2_20260930/evidence/README.md)에 스크립트·의존성·대역 범위를 적었다. 줄 번호는 이번 패치 적용 후 후보 사본 기준이다. ZIP은 **부분 소스와 독립 증거**이며 완전한 저장소/설치 LIGGGHTS 빌드를 포함하지 않는다.

**HOLD**
