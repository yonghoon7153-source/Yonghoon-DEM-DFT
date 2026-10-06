# 92차 게이트 범위 검토 회신

2026-10-06 · 단계 4 묶음 6 · 구현 전 정적 검토

## 판정

**수정 조건부 적합.** 요청한 최소 방향과 Q1–Q9의 취지는 수용한다. 다만 아래 G92-N1–N3를 시작 전 고정 표 §16에 반영해야 구현 승인 범위가 명확해진다. 이것은 코드 구현 결과의 수용, 묶음 6 종결, 구현 착수 승인 또는 실행 GO가 아니다.

단계 3의 이미 수용된 라운드 1·2a·2b는 **이번 제한 오프라인 단계 4를 설계할 선행 조건을 충족**한다. 이를 단계 3의 모든 기능 완료로 확대하지 않는다. 76차 및 91차 종결, grid_fit_v5 진단 전용 지위는 유지한다.

## 고정 대상과 확인 수준

| 항목 | 확인 |
| --- | --- |
| 발송 HEAD | 7a8a22a2d61a17ec360a1589615a36c5c223cd1f |
| 요청문 커밋 | 37e3b5c46715c2414147894db58392be5b94c597 |
| 변경 없는 판정 코드 | b08bb6944b03511c97c8deeb38e6a347bbb1f1fb |
| 수용된 source_digest | f0175fff71132003 |
| 요청문 blob | 2664ad6985d85780668c8978adcbcdd464c56641 |
| 범위 조사 문서 blob | 6385aab2584baaa95aa7a09a3ceb73076d84ac5a |
| RUN_SCOPE | 코드 커밋과 발송 HEAD의 60개 파일 집합·Git blob·mode 모두 동일 |
| 요청문 이후 프로젝트 변경 | 요청문 커밋 → 발송 HEAD의 비교 21개 파일 중 degradation-degeneracy 변경 0 |

RUN_SCOPE는 두 고정 커밋의 잘리지 않은 Git tree에서 직접 대조했다. 300개 파일에서 끊긴 큰 commit 비교 목록을 불변 근거로 사용하지 않았다. source_digest 함수는 실행하지 않았으며, 91차 수용 identity를 같은 RUN_SCOPE 바이트에 연결했다.

이번에는 원문과 코드의 정적 비교만 했다. 후보 import, pytest, smoke, 변이, production 함수 호출, 복원·재채점·영수증 재생성 및 COMSOL/Java 계산은 하지 않았다. 발송문에 적힌 신규 docs-lint/citations 360 PASS는 제출자 보고로 구분한다. G91의 2182 PASS / 1 xfailed·smoke rc0는 이전 수용 기록이며 이번 새 실행으로 세지 않는다.

F1의 “전체 git 역사·운영 산출·미추적 파일에서도 0건”은 이번 검토가 독립 재탐색한 범위가 아니다. 현재 주요 writer/consumer와 아래 코드 사실은 직접 읽었다. 이 한계는 닫힌 schema와 신규 음성 증거를 고정하자는 방향을 막지 않는다.

## 수용하는 코드 사실

- io.py:1873–1878은 stage3의 필수 키 누락만 검사한다. 추가 키의 거부가 없다.
- io.py:1927–1934는 candidate_map의 schema·entries·record digest를 보지만 최상위·항목의 정확한 키 집합을 닫지 않는다.
- stage3 사본 9개는 필수 존재와 전체 서명에 들어가지만, 해당 사본 자체와 계획 값을 키별로 대조하는 검사가 없다. 재유도 함수가 env의 값을 쓰는 것은 사본 검증과 다르다.
- fitting.py:1545는 기본 공백 구분자의 json.dumps를 해시하고, preserve.py:138–150·6656은 compact canonical digest를 쓴다. 비어 있지 않은 provider edge의 직렬화 정의가 다르다. 현재 정상 no-provider 대조만으로는 이 차이를 드러낼 수 없다.
- preserve.py:6168–6175의 계획 index 검사는 stage3 승인 축 전체를 유도값과 비교한다. 이곳은 신규 알고리즘 변경보다 누락된 키별 증인의 보강이 맞다.

따라서 사본 9개를 삭제하지 않고 결속시키고, provider hash를 기존 canonical digest로 통일하며, sig 6의 두 객체를 닫는 최소 변경은 타당하다. 아직 실행 반례를 재현했다는 판정은 아니다.

## G92-N1 P1 소비자와 키의 증거 대응을 먼저 고정

**좌표:** GATE92_REQUEST.md:42·54·57, 조사 문서:169–181·238–247.

요청의 완료 조건은 “키마다 그 키를 읽는 consumer마다”인데, k09는 C4의 두 키, C6의 header/order, C2의 세 키만 적었다. 조사표의 C5 사전 검사, C8 승인 대조, C9 최종화, C11 roster/edge 및 C7 행 재유도 항목은 신규 또는 재사용 증인과의 대응이 없다. 기존 검사가 존재한다는 사실만으로 per-key 증거까지 갖췄다고 결론내릴 수 없다.

또한 run_spec 최상위·solution map header·운영 원장 항목은 조사표에서 열린 것으로 남고 이번 변경에서는 제외된다. 그러므로 “모든 v6 consumer가 구 필드를 거부한다”는 무제한 표현은 이번 상한보다 넓다.

**§16에 고정할 것**

1. consumer·키·기대값의 독립 출처·실제 호출 경로·양성 대조·음성 node·기대 이유·비교 위치의 변이·재사용/신규를 한 행으로 연결한다.
2. 이미 수용된 시험은 고정 커밋과 정확 node/증인을 참조해 재사용할 수 있다. 과거 시험을 모두 새로 RED로 만들거나 동일 비교 위치의 변이를 키 수만큼 늘리지 않는다.
3. C5/C8/C9/C11과 C7 행 단위도 “기존 증거로 충족 / 이번 보강 / 명시적 이월” 중 하나를 적는다. 이월이 있으면 해당 범위를 묶음 6 전체 종결로 선언하지 않는다.
4. 부재 보증은 이번에 열거한 닫힌 객체와 정상 writer 출력에 한정한다. 제외된 최상위·header·원장까지 닫혔다고 쓰지 않는다.

이는 production 범위를 넓히라는 요구가 아니다. 기존 증인의 대응만으로 충족하면 추가 production 변경은 필요 없다.

## G92-N2 P2 키 집합과 자료형 거부를 함께 정의

**좌표:** GATE92_REQUEST.md:49·57, io.py:1880–1910·1927–1932·1961, _stage3_rederive:1714 이후.

제안된 k03/k04는 추가 키만 다룬다. 그러나 현재 candidate_map이 배열/null이면 1929의 cm.get에서 AttributeError가 날 수 있고, entries에 비객체 항목이 있으면 뒤 재유도의 m.get 경로가 안전하지 않다. stage3.planned_envelope를 유효하지 않은 자료형으로 바꾸는 경우도 실패 기록을 만든 뒤 그 객체를 계속 쓰는 경로가 있다. 위 구간은 정적 근거이며 이번에 실행해 관측한 예외가 아니다.

**§16에 고정할 것**

- 새로 닫는 두 객체에 대해 정확한 키 집합뿐 아니라 객체/list/항목의 자료형, 필수 값의 자료형과 허용 null을 적는다. 기존 source·index·bank_index 규칙을 그대로 사용하고 새 수치 정책을 만들지 않는다.
- 누락·두 구 이름·제3의 임의 추가 키·잘못된 컨테이너·잘못된 항목 자료형을 검사한다. int 자리에 bool/문자열을 조용히 동등 취급하거나 입력을 변환해 통과시키지 않는다.
- schema/env 검사가 실패하면 그 객체를 재유도에 넘기지 않는다. 실제 validate_provenance 경로가 키 또는 항목 위치가 있는 구조화된 실패를 돌려야 한다.
- 새 stage3_axis_from_envelope 호출이 유효하지 않은 입력 때문에 PreserveError를 낼 경우에도 validator의 실패 결과에 연결한다. 아무 예외나 나면 음성 PASS로 세지 않는다.
- 변경은 sig 6의 해당 자료 경계 안에 둔다. legacy reader나 모든 JSON 소비자를 일괄 재작성하지 않는다.

이 보강은 이미 제안한 schema 닫힘의 완료 기준이지, 새로운 native 기능 요구가 아니다.

## G92-N3 P2 직접 비교 네 키의 증인을 정정

**좌표:** 조사 문서:227·243–244·259, 요청문:50·59, io.py:1684–1697·2015–2048.

“env 직접 비교 4키를 끄면 k05의 그 4키가 물어야 한다”는 표가 맞지 않는다. k05의 9개에는 bank_version·budget_by_objective·warm_provider_map만 있고, exact_bounds_sha256은 k06에 있다. 더구나 exact_bounds는 이미 run_spec.bounds에서 다시 계산해 s3와 env에 연결한다. 새 직접 비교가 중복이면 그 비교만 꺼도 기존 검사가 거부할 수 있다.

**§16 정정**

- run_spec.stage3 16키의 근거를 다음처럼 나눈다: 기존 helper에서 겹치는 키의 투영, env 직접 비교, 기존 독립 재계산.
- exact_bounds는 기존 3자 대조를 유지하고 k06 및 기존 재계산 증인에 연결한다. pairing_design·base-config closure의 독립 재계산도 helper/복사값 비교로 대체하지 않는다.
- 같은 비교 위치를 두 번 세지 않고, 중복 방어 때문에 생존한 변이를 죽이려고 기존 검사를 약화하지 않는다. k05/k06의 실제 담당 node와 이유를 적는다.
- 비교 위치별 변이 하나가 원칙이다. 새 공통 루프 하나가 여러 키를 검사하면 그 루프의 변이 하나와 키별 데이터 음성들을 연결하면 된다.

## 경계 문구 정정

조사 문서:247의 “빠진 키가 RED로 드러나면 그 키만 범위에 넣음”은 요청문:43·79의 중지 규칙과 맞춰야 한다.

> 기존 증인의 누락은 승인된 시험 파일에서 보강할 수 있다. 승인한 production 파일 또는 허용 함수 변경 범위를 넘는 결함은 기록하고 중지하며 별도 승인을 요청한다. 같은 파일이라는 이유만으로 다른 제어 경로의 수정을 자동 포함하지 않는다.

기존 변이 증인의 뜻이나 도달 단계가 달라지면 먼저 보고한다. --emit-expect는 관측 도구이지 증인 교체의 승인이나 그 정당성 증명이 아니다. 의미가 같은 단순 좌표 이동과 이유 변경을 구분하고, 이유 변경의 허용 범위를 사용자 승인문에 먼저 적는다.

v5/v6_prep “바이트 불변”은 기존 봉인과 수치·분기·schema 의미를 가리킨다. RUN_SCOPE 변경에 따른 새 validator identity 및 승인된 새 영수증 identity의 변화는 별도 표로 적는다. 현행 history와 과거 오류는 변경하지 않는다.

## Q1부터 Q9까지 답

| 질문 | 답 |
| --- | --- |
| Q1 claim 세대 게시 | 제외 수용. §13-5의 실물 v6 leg 이후 별도 등록 원칙 유지. |
| Q2 음성 시험과 변이 | 둘 다 수용. 키별 데이터 음성 + 독립 비교 위치별 변이. G92-N1/N3의 대응표가 조건이다. |
| Q3 단계 3 선행 | 이번 제한 단계 4의 선행 조건 충족. 전체 기능 완료·실물 v6 실행 준비 완료는 아님. |
| Q4 provider hash | 기존 canonical digest 한 정의로 통일. warm edge 양성으로 writer와 승인 축 일치를 고정. |
| Q5 9개 사본 | 유지하고 계획에 대조하는 안 수용. 기존 독립 재계산은 보존. |
| Q6 상태표 | 묶음 6 행만 제출 상태로 갱신. 이번에는 닫힘 표시 금지. |
| Q7 순서 | 범위 검토 → 정정된 §16 → 사용자 별도 구현 승인 → 결과 검토. |
| Q8 io.py와 영수증 | sig 6 안의 제한 변경 수용. history 보존 후 두 leg 각 1회 제안 수용. v5 검사 집합 35/34 유지, 다른 변화면 중지. |
| Q9 묶음 9 | 나중에 묶음 6이 실제 종결되면 선행 하나만 충족. provider 운영 보존/registration/canary 등의 남은 범위를 해소하지 않음. |

## 다음 제출 조건

새로운 개괄 계획을 반복할 필요는 없다. 위 세 조건을 §16과 승인 범위에 반영하고, 사용자에게 **제한 오프라인 구현** 승인을 별도로 받으면 된다. 범위를 넓히지 않는 명확화에 대해서는 동일한 사전 검토를 자동 반복할 필요가 없다. 구현 이후에는 고정 표 대비 diff, 정확한 이유의 RED/GREEN, 키별 대응표, 비교 위치별 변이, legacy 대조, history와 새 영수증, 최종 clean 검증 로그를 제출한다.

이번 회신은 구현 실행 명령이 아니다. COMSOL, 새 연구 계산, pilot/floor, 운영 v6 계획, 세대표·claim 게시, class/투영, p_ini/adaptive, requirements 변경은 승인하지 않는다.

## 근거

모든 행 번호는 발송 HEAD 기준이다. source 식별과 발췌는 SOURCE_IDENTITIES.json 및 reference/SOURCE_EXCERPTS.json에 있다.

- [GATE92 요청문](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/7a8a22a2d61a17ec360a1589615a36c5c223cd1f/degradation-degeneracy/docs/22p_gap/GATE92_REQUEST.md)
- [단계 4 범위 조사](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/7a8a22a2d61a17ec360a1589615a36c5c223cd1f/degradation-degeneracy/docs/22p_gap/STAGE4_SCOPE_RESEARCH_20261006.md)
- [sig 6 validator](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/7a8a22a2d61a17ec360a1589615a36c5c223cd1f/degradation-degeneracy/src/io.py#L1862)
- [writer](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/7a8a22a2d61a17ec360a1589615a36c5c223cd1f/degradation-degeneracy/src/fitting.py#L1539)
- [공통 승인 축](https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT/blob/7a8a22a2d61a17ec360a1589615a36c5c223cd1f/degradation-degeneracy/tools/preserve.py#L6640)

