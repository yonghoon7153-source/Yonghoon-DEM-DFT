# LHS 피복률 재검증 3 판정

## 0. 결론 · 실물 핀

**HOLD 유지. 새 P1 없음. 앞 라운드의 구체적 반례는 수정됐다. 남은 P2는 ① 설치 빌드 인증 표지, ② 완료 검사기의 피복률·개수 장부 모순이다.** 새 E 모델을 옛 고정 eps 여유와 같은 이유로 기각하지 않는다. `n_detect_1pct`도 옛 `n_power_1pct`와 달리 입력 기하에만 의존하며, 아래 독립 시험에서 보증 후 누락은 없었다.

이 판정은 **실 130/64 데이터가 오염됐다는 증거가 아니다.** item 2는 진단 기록이며 수확 피복률을 바꾸지 않는다. 스키마 반례도 실제 생산자의 정상 출력을 변조해 검사기에 넣은 시험이지, 정상 생산자가 그 모순을 생성했다는 주장이 아니다. LHSC-01·02의 닫힌 P1을 다시 열지 않는다.

- 일자: 2026-09-30. 입력 ZIP 77,108 bytes, SHA256 `10addd2049cc17504c0f9ae5fde66eaa6ca9adec0e4d2fba066ac367b50d5382`.
- 선언 base `ca0471d19a5a9d914c6a31006a001d515267f3be`, tip `220b1426ea39eae13f077e9f0585388f3eb61d08`. 원격에 없는 커밋의 실재를 별도로 인증한 것이 아니라 **제출 패치와 적용 후 파일 바이트**를 검증했다.
- 이전 재검증 후보의 보존 대상 5파일 해시 확인 → 별도 비 Git 사본 생성 → 0014·0015 순서로 `git apply --check` 및 적용. 제출 SHA256SUMS 13건 일치. 변경 3파일 모두 LF 정규화 후 크기·SHA256·Git blob이 manifest와 일치한다. [독립 소스 원장](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/source_manifest.json).
- 생산 코드·Git ref·원장은 변경하지 않았다. DEM, 설치 엔진, 원격 캠페인, 실 재수확·coverage 배치는 실행하지 않았다. 아래는 격리 사본의 CPU 합성 시험이다.

| 항목 | 재판정 | 경계 |
|---|---|---|
| LHSC-03-R3의 기존 반례 | **닫힘** | 이전 변이 20종 거부, 정상 생산자 8종 허용. 새로 찾은 장부 모순은 §4의 별도 R4 |
| LHSC-04-R3a의 동심 오탐·음수 혼동 | **닫힘** | 동심 2건은 미인증·시험 0, 음수 2건은 별도 집계. 설치 빌드 인증은 아직 아님 |
| LHSC-04-R3b | **조건부 닫힘** | 공개 식·지원 수치영역·6자리 출력 전제. A_dump 의존성 제거, 보증 후 누락 반례 없음 |
| 이전 P3: 하한 0 / blank h_film | **닫힘** | 실제 lo==0과 boundary를 분리. 잘못된 h_film 거부, 정당한 None/키 부재 허용 |
| 새 LHSC-04-R4-PIN | **열림, P2** | 증거 없는 JSON으로 `installed_build_pinned=True` |
| 새 LHSC-03-R4 | **열림, P2** | 불가능한 피복률·장부가 필수 단계 `done` |
| LHSC-04-R4-DOMAIN | **P3, 한정 명시 필요** | 모든 유한 double에 대한 E 보증은 아님. 비현실적 크기의 언더플로 반례 |

## 1. Q1 — 새 생산자 오차 E

**지원 수치영역에서 방향과 연산 분해에 동의한다. 모든 binary64 입력·임의 컴파일 옵션·설치 바이너리에 대한 무조건 인증에는 반대한다.**

위치: [δ 상자 확장:418](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:418), [E 구성:509](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:509).

공개 [LIGGGHTS-PUBLIC add_pair](https://github.com/CFDEMproject/LIGGGHTS-PUBLIC/blob/master/src/compute_pair_gran_local.cpp#L509-L533)를 다시 읽었다. 구형 입자의 면적은 거리 기반 네 인수 곱/rsq, δ는 반경 합에서 거리의 제곱근을 빼는 식이다. superquadric의 δ는 별도 가지이므로 이 리뷰는 구형 경로만 다룬다. 이 공개 소스 열람은 사용자의 설치 빌드 확인을 대신하지 않는다.

### 왜 고정 eps 바닥보다 낫나

`u=2^-53`, `eps=2u`라 두자. 모든 중간 연산이 유한 정상 범위이고 round-to-nearest인 통상 오차 모형에서, 세 좌표 차·제곱·두 합의 거리 제곱 오차는 경로별 γ 계수로 다룰 수 있다. 좌표 차의 반올림까지 포함해 γ₅ 수준, sqrt까지 약 3.5u·d 수준이다. 여기에 각 인수를 만드는 두 덧셈/뺄셈의 **절대** 오차를 합해도 `eps·(3S+m_k)`는 여유가 있다. 작은 인수에서 상대오차가 발산하는 문제를 절대 오차로 옮긴 것이 핵심이다.

곱·상수·나눗셈·분모 오차도 포함해야 한다. 코드의 13eps=26u는 단순 11u 선형합보다 넉넉하고, 15개 양의 교차항을 더하는 방식은 작은 두 큰 곱을 빼는 상쇄를 피한다. 다만 증명 문장의 `1/rsq ≤ 1/d_min²`를 **반올림된 rsq에 대한 독립 부등식**으로 인용해서는 안 된다. 엄밀히는 분모의 `1/(1−γ)` 팽창도 총 상대오차 예산에 포함하는 설명이어야 한다. 코드의 여유가 그 역할을 하더라도, 1차 항의 개수만 나열한 것이 모든 입력의 정형 증명은 아니다.

`−π/4`의 부호는 오차를 만들지 않고, 정상 범위에서 4로 나누기는 이진 스케일링이다. π의 double 근사와 최종 곱의 반올림은 남는다. dy·dz가 0인 저자 시험에만 의존하지 않고 아래에서 세 성분과 좌표 뺄셈을 함께 시험했다. FMA는 무조건 오류를 늘리는 연산이 아니지만, 재결합·역수 근사·FTZ/DAZ 등을 포함하는 빌드가 같다는 증거 없이 현재의 평가 순서를 설치 바이너리에 이식할 수는 없다.

### 독립 검산

`audit_error_3d.py`: seed=309302026, 비영 세 좌표 성분·서로 다른 좌표 원점, r1=10⁻⁶–10⁻¹ sim, r2/r1=10⁻³–10³. 얕음·깊음·포함 경계·동심 근접·비접촉·완전 포함 여섯 영역을 만들었다. **저장된 double 좌표의 정확한 차와 norm을 Decimal 90자리로 계산**해 공개 식의 실제 binary64 순서와 대조했다.

| 검산 | 결과 |
|---|---:|
| 거리 양수인 생성점 | 17,926 |
| 점별 \|A_producer−A_exact\| > E | **0** |
| 관측 최대 오차/E | 0.21310838611670851 |
| 6자리 토큰의 인증·비음수 행 / 거짓 초과 | 8,170 / **0** |
| 산술 미인증 행 / 음수 면적 행 | 2,363 / 7,393 |

마지막 두 범주는 서로소 분할이라고 주장하지 않는다. 표본 검산이지 설치 엔진 시험·전역 증명은 아니다. [독립 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/error_3d_results.json).

옛 독립 geometry 시험도 재실행했다. 12,000 상자×24점=288,000점에서 Decimal 80자리/실제 로컬 함수 이탈 **0/0**, corner 6,489·zero 4,099·interval 429·boundary 983. 이것은 실수 기하 enclosure 검산이며 E의 별도 증명으로 중복 계산하지 않는다. [결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/geometry_results.json).

### LHSC-04-R4-DOMAIN — P3: “d_min>0이고 E가 유한”만으로 모든 double을 인증하지 말 것

실제 `producer_area_binary64`와 `_producer_abs_error` 호출:

~~~text
r1 = r2 = 1e-100 sim, d = 1.9e-100 sim
생산 면적 = 0 sim²                 # 네 인수 곱의 언더플로
정확 면적 = 3.0630528372500500e-201 sim²
E = 0 sim²                        # E의 곱 항도 언더플로
|오차| > E = True
~~~

거리 하한은 양수다. 따라서 “미인증 조건은 d_min≤0뿐이면 전역적으로 충분”은 틀리다. **실 LHS 단위와 전혀 다른 비현실적 반경**이므로 이 반례를 생산 결함의 P1/P2로 올리지 않는다. 지원 수치영역·중간 연산 정상성 전제를 명시하거나, 일반 목적 인증기를 원하면 스케일 정규화/정의역 검사를 넣어야 한다. 이번 P2 해제 때문에 1e-100 크기의 DEM을 지원하라고 요구하는 것은 아니다.

재현: `python evidence/audit_numeric_domain.py`. [결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/numeric_domain_results.json).

## 2. Q2 — 미인증과 검출력 부족은 다르다

**E가 유한하지만 큰 행을 산술 “미인증”으로 바꿀 필요는 없다.** 옳은 넓은 상한은 인증된 상한이되 정보가 적다. `E > h(A_dump)`를 새 실패 문턱으로 쓰면 관측값 의존성이 다시 들어가고, 1% 치환 검출과도 직접 같지 않다.

현재의 `producer_bound_rel_*`와 `n_detect_1pct=0`을 공개하는 방향에 동의한다. 단, 보고 문구는 다음을 구별해야 한다.

- `n_producer_uncertified`: 이 산술 모델에서 E를 주지 못한 행.
- `n_tested`: 이 모델로 비교한 비음수 행. **정밀 비교 통과·설치 빌드 인증과 동의어가 아니다.**
- `n_detect_1pct`: 등록된 양방향 치환을 구별할 충분조건이 성립한 기하 행.
- `installed_build_pinned`: 별도 provenance 축이며 현재 구현은 §5의 수정이 필요하다.

`lo=0`인 행은 E/lo 통계에서 빠지므로 상대오차 요약만 따로 제시하지 말고 `n_lower_bound_zero`, 미인증, 음수 개수를 함께 보존한다. E/lo 분포를 더 자세히 내는 것은 유용하지만, 임의의 새 문턱을 만들어야 이번 수정이 옳아지는 것은 아니다.

옛 d=1e-15·1e-16 sim 동심 사례는 이제 둘 다 미인증 1·시험 0·초과 0이다. 완전 포함/비접촉의 음수 공개 식 출력은 음수 1·시험 0으로 분리된다. 이는 **거짓 통과로 바꾼 것이 아니라 판정 불능/의미 차이를 노출한 수정**이다. [재실행 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/producer_results.json).

## 3. Q3 — ±1% 검출 보증

**조건부 CONFIRMED / 이번 검증에서 반례 없음. 옛 R3b는 닫는다.**

위치: [행별 허용 구간·검출식:579](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:579), [h± 계산:596](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:596).

`L=lo−E`, `H=hi+E`라 두면, 정상 생산값이 [L,H] 안에 있다는 전제하에 증가 치환의 최솟값과 감소 치환의 최댓값을 각각 허용 구간 밖으로 밀어야 한다. 출력값을 토큰으로 반올림하는 오차뿐 아니라, 검사기가 **그 토큰을 다시 ±h 구간으로 해석하는 폭**도 필요하므로 2h를 넣은 방향이 맞다. 충분조건일 뿐 필요조건은 아니다. detect=0이라고 치환이 반드시 누락되는 것은 아니다.

이번 코드는 lo·hi·E·길이 토큰으로만 분류한다. `A_dump`는 beyond 판정에는 쓰지만 detect 식에는 들어가지 않는다. 따라서 옛 반례처럼 치환 자체가 분류를 좋게 만드는 결함은 제거됐다.

- 옛 `(0.00348428, 0.00164629, 0.00328959)` sim 상자: 정상 `5.81675e-8`, +1% 치환 `5.87492e-8` sim² 모두 **wide=1·detect=0·beyond=0**.
- 새 3D 시험: detect=1인 5,928행에서 +1%·−1% 토큰 각각 누락 **0**, 분류 변화 **0**.
- 별도 출력 자릿수 경계 시험: 500,000개의 합성 허용 구간을 소수 지수 전환 근처에 집중시켰다. 양방향 보증이 켜진 263,988구간에서 끝점·중점·10의 거듭제곱 전후 **1,980,567 치환값**을 실제 %.6g 반올림과 토큰 구간 판정에 통과시켜 누락 **0**. 이는 물리 입력 샘플이 아니라 검출 부등식 자체의 스트레스 시험이다. [결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/power_boundary_results.json).

주의: `_half_unit(x)`는 반올림 뒤 10의 거듭제곱으로 올라간 토큰의 반폭과 다를 수 있다. 따라서 “모든 x에서 반올림+토큰폭≤2h(x)”라는 단독 명제는 쓰지 않는다. 여기서는 범위 양 끝의 최대 h와 **양방향 조건을 함께** 시험했다. 지수 경계의 이 개별 주의점을 실제 반례 없이 새 HOLD 이유로 올리지 않는다. 전제의 범위는 공개 식, 정상 중간 산술, 구형 입자, 등록 6자리 출력이며 설치 빌드의 실증과는 다르다.

## 4. Q4 / LHSC-03-R4 — 피복률과 장부의 공존은 아직 미완성

**P2 · REFUTED. 무너지는 결론: “필수 coverage 단계의 done은 v2 레코드의 범위·공존·장부 항등식을 만족한다.”** 실제 생산값 전체의 정확성을 재계산하라는 요구가 아니다. 현재 이미 실리는 값들끼리 불가능한 조합을 받아들이는 반례다.

위치: [검증기:3250](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/webapp/app.py:3250), [피복률을 개별 0–100만 검사:3290](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/webapp/app.py:3290).

정상 생산자 `compute_case`를 실제 호출했다. 기존 fixture는 n_am=2, n_contacts=11, n_cap=9, 평균 피복률 **1.218%**, binding은 elastic=1/tabor=5/volume=3/geom=1/none=1이었다. 별도 fixture는 같은 AM 2개를 두고 접촉만 전부 비워 정상 평균 0%를 얻었다. 그 산출물에서 다음만 바꿨다.

| 변이 | 왜 불가능한가 | 검사기 / 필수 단계 |
|---|---|---|
| 접촉 0, 모든 면적·결속 0인데 상별/전체 평균을 **50%** | 생산자의 분자 합이 모두 0이며 유효 분모는 양수 | True / **done** |
| n_am=2, n_coverage_clipped_100=**2**, 전체 평균은 **1.218%** 유지 | 둘 다 클립 후 100이면 전체 평균도 100 | True / **done** |
| 각 상의 population std를 **75%p** | [0,100] 값의 population std는 최대 50%p | True / **done** |
| n_cap를 **9→11**, 분율을 **2/11=0.181818**로 함께 변경, binding 장부는 유지 | cap binding 5+3+1=9. elastic/none 두 행은 cap 가지 아님 | True / **done** |

피복률 계산은 [분자·분모 및 클립:326](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:326), 통계는 [평균·population std:344](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:344)에서 직접 확인했다. cap 개수는 [장부 add:276](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/coverage_physics_vs_hertzian.py:276), [elastic/none 반환:525](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/plastic_coverage.py:525), [cap 반환:545](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/plastic_coverage.py:545)에서 확인했다.

### 최소 해제 — 물리 계산 복제 없이 가능

1. AM–SE 접촉 수가 0이면 해당 AM 피복률 평균·std·클립 수는 0이어야 한다. **반올림된 총 면적이 0이라는 이유만으로** 피복률을 강제로 0으로 만들지 않는다. 면적은 0.01 µm²로 반올림되므로 그 역추론은 과잉차단이다.
2. `mean_AM ≥ 100*n_clip/n_am`을 생산자의 평균 반올림 폭(0.0005%p)을 감안해 검사한다. 특히 n_clip=n_am이면 평균 100이다. n_am=0 분기는 별도로 둔다.
3. std의 범위를 population 정의에 맞게 최대 50%p로 제한한다. 평균까지 활용한 더 강한 분산 상한은 선택 사항이지 이번 최소 해제의 필수는 아니다.
4. `n_cap = binding_total[tabor]+[volume]+[geom]`을 검사한다.
5. 위 네 변이가 helper False뿐 아니라 **필수 단계 failed**가 됨을 상주 시험으로 남긴다. 정상 0접촉 AM, SE-only, 부분/전체 클립 정상 레코드도 통과시킨다.

상별 개수 없이 임의의 두 상 평균을 단순 평균해 전체 평균과 비교하는 것은 금지한다. 생산자는 입자 수 가중이다. 존재하지 않는 상의 키를 무조건 요구하는 것도 안 된다. 더 강한 per-phase 완전성 계약은 상별 개수/타입 집합을 명시한 뒤 별도 도입할 수 있다.

재현: `python evidence/audit_r4.py`. subprocess 실행만 합성 레코드 전달로 대체했고, `_coverage_stage`·`pipeline_service`·검증기·summarize는 실제 함수다. [전체 입력·판정 결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/r4_results.json).

## 5. Q5 / LHSC-04-R4-PIN — 자기 신고를 설치 빌드 인증으로 승격

**P2 · REFUTED. 무너지는 결론: “이 pin 파일이면 실제 생산 빌드의 식·컴파일 규약이 핀됐다.”** 현재 핀이 없을 때 False를 내는 것은 맞지만, 핀이 있을 때 무엇을 확인하는가는 별도 문제다.

위치: [producer_pin:553](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:553), [True로 승격:568](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:568), [출력 표지:619](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:619).

다음 JSON을 실제 함수에 넣었다. source_file은 존재하지 않고, host/date/build는 **아예 없다**.

~~~json
{
  "schema": "liggghts_add_pair_pin/1",
  "source_file": "<시험 폴더>/nonexistent.cpp",
  "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "formula_confirmed": true
}
~~~

결과는 `pinned=True`, pin의 host/date/build는 null이다. 같은 환경변수로 실제 `contact_area_check`를 부르면 **`producer_model.installed_build_pinned=True`**가 실린다. 두 번째로 add_pair가 없는 파일을 만들고 전혀 다른 0×64 해시를 적어도 True다. 즉 JSON의 문법만 맞으면 파일 해시 불일치·소스 부재·빌드 부재를 모두 통과한다.

이것은 악의적인 파일 위조만의 문제가 아니다. 오래된 source 경로, 다른 빌드의 hash, 빠진 build 필드가 정상 인증으로 기록될 수 있다. 현재 selftest도 [형식 맞음→True:2606](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/candidate/scripts/lhs_descriptor_harvest.py:2606)를 기대하므로 이 결함을 잡지 않는다.

### 처방: 주장 수준을 분리한다

- 현재 JSON은 최대한 **`source_formula_attested` 또는 `pin_claim_present`**다. 이 기능을 유지하려면 이름을 그 수준으로 낮추고, 설치 빌드 검증 없이 installed 표지를 True로 만들지 않는다. 단순히 문자열 필드 셋을 필수로 만드는 것만으로는 충분하지 않다.
- 실제 인증이 필요하면 source 바이트·해시 재계산, source revision/dirty patch, 실행파일 경로·SHA256, 컴파일러 버전/실제 compile 명령·부동소수 옵션, 그 실행파일을 해당 dump 생산에 사용했다는 실행 영수증을 연결한다. `vectorMag3D(Squared)` 등 관련 구현·구형 분기도 그 출처에 포함한다.
- 원격 source 경로가 이 Windows에 없다는 사실 자체를 오류로 삼을 필요는 없다. **해당 호스트에서 수집한 검증 결과/증거 바이트**를 반입하면 된다. 현재 코드처럼 경로 문자열과 sha 형식만 읽은 것은 그 검증 결과가 아니다.
- 오늘의 source hash가 과거 dump를 만든 바이너리의 증거는 아니다. 그 연결을 회수할 수 없으면 설치 인증은 False로 남기고, 결과를 “공개 식 가정하의 진단”으로 한정한다. 이 리뷰가 그 이유만으로 DEM 재실행을 요구하지는 않는다.

최소 해제는 **없는 인증을 True라고 부르지 않기**다. 완전한 빌드 영수증 확보와 재수확 착수 승인은 별도 운영 조건이다. `0001→…→0015→게이트→트리 해시→새 디렉터리` 순서는 소스 세대 봉인으로 타당하지만, 순서 자체가 producer provenance를 채우지는 않는다.

재현: `python evidence/audit_r4.py`의 pin 두 대조. [결과](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/r4_results.json).

## 6. 실행 결과와 한정

| 시험 | 이번 독립 실행 |
|---|---|
| lens / plastic / coverage | rc=0 / 0 / 0 |
| pipeline provenance | **212/212**, rc=0 |
| harvest 원본 selftest | rc=1, 이전과 같은 두 환경 의존 실패: CRLF fixture hash·τ median 1 ULP |
| harvest LF fixture 대조 | CRLF 실패는 사라짐. τ 1 ULP 실패만 남음 |
| batch 원본 selftest | Windows symlink 권한 실패 후 calls[0] IndexError, rc=1 |
| batch 파일 복사 대조 | symlink_to만 byte-copy로 대체하면 rc=0. 실제 배포 symlink 인증 아님 |
| 이전 정상 생산자/스키마 회귀 | 정상 8종 허용. 옛 변이 10종+R3 잔여 변이 10종 전부 거부. 정당한 blank rule=None·h_film 부재 허용 |
| 새 R4 장부 변이 | **4/4 허용·done** — §4 |
| 옛 수확 값 대조 | baseline 36키×16호출 불일치 0; τ 구조 전체도 baseline/candidate 동일 |

τ median은 baseline과 후보가 모두 **2.080532952769607**, selftest 고정값은 **2.0805329527696066**이었다. 이를 이번 패치 회귀라고 하지 않는다. 반대로 제출자의 Linux 전수 녹색 로그를 이 Windows에서 독립 재현한 것처럼 “전부 통과”라고도 적지 않는다. 전체 `check_all.sh`는 이번에 독립 실행하지 않았다.

[selftest 로그 요약](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/selftests.json) · [환경 대조와 옛 키 비교](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/regression_results.json) · [스키마 재검산](C:/Users/Administrator/Documents/Codex/2026-08-24/claude-stoic-knuth-nobvq-x20/lhs_coverage_reverify3_20260930/evidence/schema_results.json).

## 7. 이번 최소 해제 목록

1. **LHSC-03-R4:** §4의 네 장부 불변식을 추가하고 정상 대조+필수 단계 음성 대조를 남긴다. 물성식·피복률 값을 바꾸지 않는다.
2. **LHSC-04-R4-PIN:** source 자기 신고와 설치 빌드 검증의 상태/이름을 분리한다. 미존재 source·hash 불일치·build 결손으로 설치 인증이 켜지지 않는 시험이 필요하다. 원격 빌드 증거가 없으면 False 유지라는 선택도 가능하다.
3. **P3/문구:** E는 정상 중간 산술·공개 구형 식의 모델임을 명시한다. 감도 없음과 산술 미인증을 혼동하지 않는다. 비현실적인 모든 double 범위 지원을 새 생산 요구로 확대하지 않는다.

옛 R3b를 다시 설계하거나, 정상 피복률을 수정하거나, 새 DEM을 돌려야 이 세 항목이 닫히는 것은 아니다.

**HOLD**
