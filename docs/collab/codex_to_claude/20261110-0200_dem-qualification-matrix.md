# D-3 — T12·재개·dt/2 선언 사례의 통합 장부

| 1저자 결정 칸 | 권고 한 줄 | 준비 중 적용 |
|---|---|---|
| Q-QUAL-A: 등록 사례/수령 | 고정source·정의·원입력과 전체 예정 분모를 유지하고 기대음성/실패/부분을 분리 | **권고안 전제(Q-QUAL-A)**; 실제 등록·수령인증 없음 |
| Q-QUAL-B: 재개/비교 | checkpoint 부모 선언·같은물리시간·선택한 초기bytes를 명시 대조 | **권고안 전제(Q-QUAL-B)**; 실제binary·숨은이력·T12 자격 없음 |

## 1. 바탕·변경

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 새 가지 | `codex/dem-qualification-matrix-1110`, 바탕 P2 `c571a27119ace92ca34d3d6f2b61135219a3f1b4` | 상시 D-3 | 원 P2/S0/LIVE 입력으로 결속 |
| 통합 API | 1개·지원 역할2종 | `scripts/dem_gen2_qualification_matrix.py`; `docs/reviews/dem_qualification_matrix_20261110/README.md` | 독립 한정 검토 PENDING |
| fixture 분모 | 예정3사례(positive2·expected-negative1) | 같은 폴더 `contract_draft.json` | 세 실제 자격 성공으로 계상하지 않음 |
| 실제 자격/등록 | 실제 T0/T2/T5/T10/T11/T12/T13 NOT_RUN·binary null·등록false | 같은 README의 실제 자격 잔여표 | 지정실제환경·등록값·반박범위GO·1저자GO 별도 |
| gate/운영 | 작성/변경0 | 모든 권한false | 전체 HOLD |

## 2. 순서·검증

구현 본문 전에 시험·fail-closed 스텁을 만들고 실제 red를 기록했다. 고정25메서드: 실패42(내부 assertion/subtest)·오류0·rc1 → 첫 구현 뒤25/25·오류0·rc0. source SHA256=`b407782264018f0bf2ff704169ff6ef3f9da7c05a865278679daa16d4f950d77`, test SHA256=`ef659db192b8abc965c3dbfa7e070fd48a3a60b8093982b5921fdf0ab346192e`. 보호조건 대조·의존 해시·원기록은 검증요약에 분리하며 반복을 새고유시험으로 더하지 않는다.

같은시간·opaque checkpoint·source label 대조는 실제 재개/물리수렴/원천인증이 아니다. dt/2의 초기 일치 대조는 atom/mesh/restart payload와 history label 부분집합이며 pair/wall/state·전체물리채널까지 동등하다고 쓰지 않는다. 원자로부터힘/접촉을 다시 계산하거나 실제binary를 호출하지 않는다.

기존 q/T0/T11/LIVE/S0/P2·봉인32·Rint·공용gate·원장 변경0. 시험은 프로젝트 코드 전에 process/network를 차단한 합성 입력만 사용했고 전체gate/CI·현장·연구결과0이다. 전체턴 문서노출 예외는 `20261110-0121_dem-t5-contract.md` §3대로 보존한다.

보호조건 약화는 **8/8 검출·각 오류0**, 원 의존은9/9 바이트 일치다. 원시 manifest는242파일(자체제외)을 결속하며 SHA256=`96ad3171a35b1af49b373c7d593661f6e9823d818d4b96393abeedfec19431b4`다.

## 3. 반입·다음

반입 커밋=`<<sha:Prepare synthetic qualification case matrix>>`. 독립 요청은 같은 폴더 `review_request.md`, 고정pin·원증거는11-10 하루ZIP. 발송=1저자, cherry-pick -x·원장처분=Claude.

다음은 D-3 마지막 DEMP-01/02·두 입경의 같은정적상태 비교 요구 계약이다. 압축 전역감쇠와 접촉감쇠/반력채널을 분리하고, 재고손실·중심통과·표면절단·미기록구간을 혼동하지 않는 작은 합성 반례를 먼저 만든다. 실제하중/면적/규약·정량허용값은미확정으로 보존한다.
