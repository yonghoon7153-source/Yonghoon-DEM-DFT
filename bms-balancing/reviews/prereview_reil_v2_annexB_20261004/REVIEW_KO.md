# REIL 부속 B 문서 재검토

2026-10-04. **RV2A-N1·N2·N3을 모두 종결 수용한다. v2 + 부속 A + 부속 B의 확인적 사전등록 문서 수용 조건 C2를 닫는다.** 이번 범위의 새 차단 지적이나 추가 정정본 요구는 없다.

이는 문서 설계 수용이다. 확인적 실행 준비 전체가 완료됐다는 뜻이나 구현·자료 개봉·P0·비용 측정·맞춤·설치 승인은 아니다. GATE89 및 PyBaMM 고정과 분리한다.

판정: DOCUMENT_ACCEPTED_RV2A_N1_N2_N3_CLOSED_NO_EXECUTION_AUTHORIZATION.

## 고정 원문과 수행 범위

요청 커밋은 e64f587bcd2b26876fcd005bae52aa18311d5b9b다. [요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_V2_ANNEX_B_REREVIEW_REQUEST_20261004.md), [부속 B](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md), [부속 A](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md), [v2](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md)를 전부 읽었다. 충돌 시 B > A > v2라는 선언에 따라 판정했다.

- v2 Git blob: 872ca88b3b5c57aebf295bd0109e95a830b3ae13. 이전 검토와 동일.
- 부속 A Git blob: 9f49d6061cf3c9e69ed35e3b00e5e0addafd8fd3. 이전 검토와 동일.
- 부속 B Git blob: b25f9c4eb56d0cfe609b47c5d8463e9f17fac53b.
- 부속 B: 17,210 bytes, SHA-256 fe2b39b222c84b61a39a14c05047ca7ca86cbb2872925c58eca400c7de673f95.

이번 수신 7개 문서·JSON의 Git blob을 독립 재계산했다. 이전 검토 묶음의 manifest와 대조한 v2·A는 크기·SHA가 같고, 원 회신·판정의 저장소 사본도 이곳의 이전 원본과 바이트 동일하다. 전체 저장소나 RUN_SCOPE 무변경을 별도 인증한 검토는 아니다.

문서·공식 자료형/배열 설명·자료 무관 상수 산술만 확인했다. REIL xlsx/pickle, 실험 자료, 제공 프로그램은 열거나 실행하지 않았다. 목적함수 평가·P0·맞춤·비용 측정·COMSOL·설치는 0회다.

## 항목별 판정과 Q1

| 잔여 | 판정 | 닫힘 근거 |
|---|---|---|
| RV2A-N1 | 종결 | 상태 불변 보증 삭제, 주장별 정확 집합에 대한 두 등급, 수치 의존 양립·폭의 UNRESOLVED 병기, 목적/선형 경계 라벨 분리, P0 배제 불변 |
| RV2A-N2 | 종결 | 맞춤 전 고정 배열과 해당 실행 직전 적응 배열을 분리, s2 부족과 동시 양립 min(4,n_valid), 중복 대체·부족 기록·추가 시작 금지 |
| RV2A-N3 | 종결 | 평탄 우선 거부, 정확 격자점은 index와 Q_j로 단 한 번, 엄격한 내부 교차만 보간, float Q 병합 폐지 |
| 수용 범위와 기록 | 수용 | 고정 저장 집합에서의 문턱 갱신, 모든 결합 기록 쌍 재판독, 방법별 발견 최소, v2 기록 항목 복원 및 추가 |

이미 닫힌 RV2-N1과 이전에 수용한 목적함수·영역·실용 탐색·E3 역할을 다시 열지 않는다. 새 solver, 전역 최적화 인증, 격자 세분화, 새 실험을 요구하지 않는다.

## Q2 두 등급과 라벨

부속 B §1의 수정은 적합하다. 같은 반환점도 프로파일상의 발견 투영과 명목 τ 상자와의 양립에서 서로 다른 주장을 받칠 수 있으므로 등급을 주장마다 매기는 것이 맞다. 프로파일 등식 잔차는 독립 기록·수용 검사에 남기되, 폭은 실제 h_k(x)의 정확 유리수 차로 판단한다. 이것은 등식 수용 허용치를 없애는 변경이 아니다. [B §1](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md#L44-L91)

자료 무관 산술로 이전 반례를 다시 대조했다. G 위반 약 5.00000013e-11과 명목 상자 위반 약 5.00000219e-11은 여전히 양수지만 1e-10 이내다. B에서는 무조건적인 정확 증인으로 승격되지 않는다. 또 영역 안이고 격자 t와 미세하게 다른 반환점은 프로파일 투영의 정확 증인이면서도 명목 구간 경계를 넘으면 그 양립 주장에서는 수치 수용 증인이 될 수 있다. 실제 REIL 목적값을 계산한 예는 아니다.

다음 의미를 함께 유지하여 수용한다.

1. exact_feasible은 해당 선형 제약 집합에 대한 등급이다. 실제 물리량의 무오차, 목적함수의 정확 계산, 전역 최적성 인증이 아니다. 저장 float의 정확 유리수 변환은 그 저장값을 보존한다는 뜻이다. [Python Fraction 공식 설명](https://docs.python.org/3/library/fractions.html)
2. COMPATIBLE의 근거는 독립 재평가와 최종 목적 문턱도 통과한 증인이다. 단순히 witness=valid 또는 exact_feasible이라는 이유만으로 COMPATIBLE이 되지 않는다. 이는 A와 v2의 기존 조건을 유지한 해석이다.
3. 증인이 0개이면 NOT_FOUND/UNRESOLVED다. “모두 수치 수용” 규칙은 근거 증인이 실제로 있는 경우의 한정 라벨이다.
4. 무조건 WIDE는 서로 2τ 넘게 떨어진 실제 투영값을 가진 정확 증인 한 쌍으로 지지해야 한다. 가능한 쌍이 수치 수용 증인에만 의존하면 한정 WIDE + UNRESOLVED다.
5. 1e-9는 목적 문턱을 완화하는 덧셈이 아니라 목적 경계 라벨 기준이다. J ≤ T 판정은 그대로다. 선형 제약 경계 라벨과 서로 대체하지 않는다.
6. “정확 집합”은 선택한 영역에 따른다. G 없는 A2를 A0/A1의 G 제약으로 다시 제한하지 않는다.

위는 이미 유효한 문서의 적용 범위를 명확히 한 것이며, 추가 부속 C나 재심사 조건이 아니다. “LII 등식 잔차가 보통 생긴다”는 수정 동기는 이해하되 실제 모든 LII 반환점의 비영 잔차를 관측했다는 주장으로 읽지 않는다. 반환값을 고치지 않고 실제 h(x)를 보고하는 선택을 수용한다.

## Q3 봉인 시점과 시작 부족

B §2는 직전 잔여를 닫는다. 규칙·고정 Sobol 배열은 P0 뒤 첫 맞춤 전에, 앞선 결과에 의존하는 시작점은 이를 사용하는 지역 실행 전에 봉인한다. 후자의 run ID·증인 식별·변환을 기록하므로 이미 끝난 실행의 시작점을 소급 바꾸는 여지를 막는다. 시작점 구성에서의 bounds 자르기와 반환 증인의 clip 금지는 서로 다른 단계다. [B §2](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md#L93-L124)

프로파일은 명목 최대 4이며 s2가 없으면 3, 중복 대체 후보도 없으면 더 적을 수 있다. 동시 양립은 중복 제거 전 n_valid=1/2/3/4 이상에서 각각 13/14/15/16이다. n_valid=0은 기존 UNFIT 분기다. 후보가 바닥나면 실제 수를 줄이고, 복제·추가 Sobol·다른 단위 예산 전용으로 채우지 않는다. 따라서 기존 54,901 지역 실행 및 109,817,477 목적 호출 상한은 커지지 않는다. 독립 재평가·E3a·ray·기록 등 별도 비용은 여전히 그 상한 밖이다.

B의 “자료에 기대지 않는 고정 배열”은 앞선 맞춤 결과에 비적응적이라는 뜻으로 읽는다. 슬라이스 범위·P/N·max_q는 P0 결과에 의존할 수 있으며, 문서 자체가 P0 뒤 생성을 명시한다. 이를 실험 자료와 완전히 무관한 수치 배열이라고 확대하지 않는다. Sobol 16의 앞 12개에는 전체 16개의 균형 성질을 주장하지 않는 문구도 적합하다. [SciPy Sobol 공식 설명](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.qmc.Sobol.html)

## Q4 격자 index 교차

정정안을 수용한다. 정확히 cutoff인 격자점과 양 끝이 cutoff가 아닌 내부 교차를 분리하면 같은 격자점의 좌우 보간값이 마지막 비트에서 달라 중복되는 기존 반례가 사라진다. 부호가 바뀌지 않는 접촉도 한 격자점으로 세고, 평탄 구간은 그보다 먼저 거부한다. [B §3](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md#L135-L147)

자료 무관 스칼라 예에서 기존 두 보간값은 여전히 0.00010010010010010012와 0.0001001001001001001로 다르다. 새 규칙은 index 1, 원 Q_1 하나를 사용한다. 내부 교차·끝점 접촉·양쪽 접촉·평탄·두 교차의 구분도 문서 규칙과 일치했다. 이는 검토자의 작은 산술 대조이지 아직 없는 H4 구현의 기능 검증은 아니다.

A의 유일 교차·span > 0 조건, 고정 1000점 선형 근사라는 이름은 유지한다. 더 촘촘한 원 곡선에서의 교차 수나 오차를 인증한 것은 아니다.

## Q5 기록 항목과 수용 범위 문구

v2 218–219행의 원래 기록 목록은 B §2-5에서 정확히 복원됐다. 시작점 배열 SHA, 판·옵션·평가 수·종료 사유, 실패·NaN, 독립 재계산 잔차, 활성 경계·G, 근거 증인 x가 되살아났다. 추가한 원 좌표·정확 잔차·주장별 등급·termination/witness·적응적 시작 출처·실제 시작 수·부족 이유·교차 목록·결합 (J_V,J_D)는 이번 정정에 필요한 기록이다. 이 범위에서 누락된 필수 항목을 새로 발견하지 못했다. [B §2-5](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md#L126-L133)

B §4도 수용한다. 문턱이 조여진다는 성질은 같은 최종 저장 점 집합에서 비교할 때이며, 최종 ρ는 저장된 모든 유효 기록 쌍을 재비교한다. 독립 풀은 방법별 발견 최소이지 전체 관측점이나 전역 최소가 아니다. H4 기준 증인·ray를 소급 재생성하지 않고, ν와 구현 대조를 실험 오차 상계나 과학적 반증으로 확대하지 않는 제한이 적합하다. [B §4](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/e64f587bcd2b26876fcd005bae52aa18311d5b9b/bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md#L149-L166)

## Q6 문서 조건 종결과 남는 선행 조건

**문서 수용 조건 C2는 종결한다.** 세 국소 정정은 반영됐으며 같은 문서 검토를 반복하거나 새 정정판을 요구하지 않는다. 구현 정확도와 실제 탐색 충분성을 문서만으로 인증한 것은 아니다.

남는 사항은 새 발견이 아니라 기존 실행 선행 조건이다.

| 조건 | 유지할 상태 |
|---|---|
| C1-core | 논문 전문 또는 저자 제공 동등 핵심 명세의 시트 의미·명목 LII 정의·셀/step 선택 확인. 이번 자료만으로 충족됐다고 보지 않음 |
| C6 | 판·환경 고정, 실제 전달 옵션과 고정 배열 식별. 실제 환경 검증을 이번에 하지 않음 |
| C3 | 자료를 처음 여는 P0의 별도 사용자 승인. 문서 수용이 자료 개봉을 허용하지 않음 |
| C5 | 비용 측정은 맞춤이며 별도 승인·파일럿 취급. 이 회신으로 시행하지 않음 |
| C4 | 실제 E3a/H 실행의 별도 승인과 자원·시간 범위 |
| C1-E3b | 출판 비교 수치·요약 방식 확보 전 E3b 미등록. E3a/H의 새 선행 조건으로 확대하지 않음 |

다음 판단은 이 기존 선행 조건의 확보 상태와 별도 작업 범위를 정하는 것이다. 실제 결과를 보기 전에 문서·판·허용 변경을 고정한다는 원칙을 유지한다. P0나 맞춤을 지금 시작하라는 지시가 아니다.

## 검토 산출물과 한계

REVIEW_CHECKS.json은 문서 식별과 검토자 상수 산술이다. 제공된 분석 프로그램·원자료·P0·solver를 실행하지 않았고, 새 구현을 검사하지 않았다. 원 문서·원장·브랜치는 수정하지 않았다. 외부 발송도 하지 않았다.

문서 작성 스킬의 출처와 판정 분리 원칙을 적용해, 문서 조건 수용과 실행 권한을 분리한 회신을 작성했다. 원문·직전 판정은 RECEIVED_SNAPSHOT.json과 PRIOR 파일에 보존한다.
