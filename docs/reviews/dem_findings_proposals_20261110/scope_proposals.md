# D5 고정 소스 범위 대조 — 작성측 정적 검토

고정 핀 `c571a27119ace92ca34d3d6f2b61135219a3f1b4`(D3 P2 포함). 전체 **HOLD**. 실제 자격·반박 판정과 작성측 소스 대조는 별도다. 새 구현·시험·운영 adapter·원장 변경 없음.

선택된 MV/GEN2 경계의 한정된 정적 읽기에서 새로운 재현 가능한 최소 구현 결함은 제시하지 않았다. 기존 수정을 재구현하지 않는다. 물리 자격/등록과 후속 계약 확장은 남는다.

상태 1 = 합성 방어 존재/물리 자격 남음; 2 = 서술·estimand 정정; 4 = 봉인 관련 제안만. 전체 11항목의 원장 status는 그대로 open이다.

| 항목 | 분류 | 다음 |
|---|---|---|
| MV-01 | 1_EXISTING_SYNTHETIC_GUARDS_PHYSICAL_QUALIFICATION_REMAINS | 즉시 기존 가드 재구현 없음. 후속 관측 계약에서 초기 제외 구간·사용할 drift 관측량·한계를 먼저 고정한다. |
| MV-02 | 1_DECLARATION_PRESERVED_HIDDEN_HISTORY_UNKNOWN | 기존 ID 비교를 다시 구현하지 않는다. T12에서 같은 기하·다른 최대 겹침/접선 이력의 두 작은 상태와 reset 대조를 구분할 검증 계획만 연결한다. |
| MV-03 | 4_SEALED_CORE_PROPOSAL_ONLY | 봉인 core 수정안만. 기존 T5 함수 중복 구현 금지. 실제 규약이 제공될 때 대응 estimand/ROI/분모/clip/PBC를 문서로 확정한다. |
| MV-04 | 2_CLAIM_ESTIMAND_CORRECTION | 문장 초안: 동일 체크포인트의 구조·이력을 출발점으로 삼아 강성을 바꾼 뒤 재평형하는 민감도이며, 적분 중 기하가 고정된 비교가 아니다. 기하 고정 계산과 fresh 준비 비교는 별도 estimand로 등록한다. |
| MV-05 | 1_SYNTHETIC_SCHEDULE_NOT_PHYSICAL_HISTORY_ERASURE | 과거 고중력 이력이 다른데 같은 마지막 gravity만 가진 두 선언을 별도 protocol identity로 구분하는 후속 계획. 실제 준비 이력 효과는 현장 물리 자격/등록 사항이며 즉시 renderer 중복 수정은 없음. |
| MV-06 | 1_TIME_GRID_BOUND_NOT_ENDPOINT_QUALIFIED | 동일 physical budget/control period/샘플 사건의 dt 및 dt/2 짝을 고정한 실제 자격 계획만 연결. endpoint 차이와 관측 해상도 허용량은 사전 선택이며 새 원자료·실행 없음. |
| MV-07 | 4_SEALED_CORE_PROPOSAL_ONLY | sealed core 수정은 제안만. 섞인 접촉 배분·상별/공간별 적분·벽 제외 집단/분모·평균 VM과 평균 tensor의 VM 구분을 별도 사전 계획으로 고정한다. 기존 제한 문장을 삭제하지 않는다. |
| MV-08 | 1_INVENTORY_GUARDS_EXIST_PHYSICAL_VOLUME_REMAINS | 동일 수라도 ID/type/radius/mass 바꾸는 반례는 기존 시험이므로 재구현하지 않는다. 후속 비평면 경계/주기면/부분 절단의 geometric oracle·mass-volume accounting 계약만 제안한다. |
| MV-09 | 2_REVIEW_CITED_SENTENCE_CORRECTION | 정정 문안은 MV09_correction.md로 제공; 역사 원문을 덮어쓰지 않고 출처와 한정이 있는 새 쪽지에 인용 가능. |
| GEN2-02 | 4_SEALED_CORE_PROPOSAL_ONLY | 정책 선택표와 봉인 수정 제안만. blank/제외 수 기록/대체 정의를 다른 정책으로 명시하고 사용 분모·노출 기록을 분리한다. |
| GEN2-04 | 4_SEALED_CORE_PROPOSAL_ONLY | 봉인 수정안만. 실제 간선·원자료를 재조회하거나 기존 승인 없이 에지 정책을 바꾸지 않는다. |

## MV-01

**기존 source/guard**
- scripts/dem_gen2_qualification.py:165–210: first hit는 진단이며 전체 예산·마지막 창·pending queue를 확인
- scripts/dem_gen2_qualification.py:262–375: 선언된 전체 trace의 identity/시각/창/예산을 결속
- scripts/dem_gen2_live_contract.py:181–265,269–328: 회전 KE·힘/토크 성분·고정 판·독립 R-a 예산; 반환 실제 GO false
- scripts/make_dem_gen2_decks.py:172–179,271–276: main 및 각 gate 정지; budget 소진은 NOT_CONVERGED

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_dem_gen2_qualification.py:131–160: 기존 지연 first-hit/후발 발산/pending 반례
- scripts/test_dem_gen2_observation_bridge.py:142–172: 조기창/늦은 불안정/미소비 지연
- scripts/test_dem_gen2_live_contract.py:240–276: 추가 채널·전체 budget·pending·독립 R-a

**남은 것**: 새 scalar/LIVE 계약은 초기 평형화가 실제 끝났다는 인증이 아니다. first_step/선언 예산과 실제 준비 이력의 결합, 관측량(높이/공극률 등) drift, 모든 필요한 시간 해상도의 완전성, 실제 채널 계산과 사전 수치 예산은 남는다. 현 LIVE schema에 height/porosity drift가 없다는 사실을 물리 자격 완료로 포장하면 안 된다.

**후속 설계만**
- 즉시 기존 가드 재구현 없음. 후속 관측 계약에서 초기 제외 구간·사용할 drift 관측량·한계를 먼저 고정한다.
- 후속 시험 설계만: 동일 force/KE인데 높이 또는 등록된 구조 관측량만 drift하는 작은 trace, 초기 구간만 안정한 trace, 고주파 왕복이 성긴 끝점에서 사라지는 trace. 현재 좁은 schema 밖 현상이며 새 실제 실패로 계상하지 않음.

## MV-02

**기존 source/guard**
- scripts/make_dem_gen2_decks.py:244–245,269–271,294–298: top mesh/wall은 한 번 설치하고 motion fix만 교체; 분리 뒤 mesh/wall 유지
- scripts/dem_gen2_live_contract.py:248–252: mesh/wall/history 선언 불일치 거부
- scripts/dem_gen2_s0_contract.py:171,246–250,267–297: hidden-history qualified false, LIVE 재검증·전체 boundary 결속
- scripts/dem_gen2_p2_contract.py:300,326–335: 같은 선언과 MOVE_CLEAR 사건

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_make_dem_gen2_decks.py:74–82: top mesh/wall 한 번, unfix 없음
- scripts/test_dem_gen2_live_contract.py:278–291: 고정 R-a 판·이력 선언 교체 거부
- scripts/test_dem_gen2_s0_contract.py:198–216,267–276: 객체 사슬·overlap≠hidden history
- scripts/test_dem_gen2_p2_contract.py:294–315: 조기 clear/legacy 삭제/누락 사건 거부

**남은 것**: 동일 fix 이름/선언/파일 해시는 엔진의 정상·접선·rolling history 보존 증명이 아니다. 실제 바이너리/모델 조합의 연속↔재개↔전환 T12 검증과 reset 대조가 남는다.

**후속 설계만**
- 기존 ID 비교를 다시 구현하지 않는다. T12에서 같은 기하·다른 최대 겹침/접선 이력의 두 작은 상태와 reset 대조를 구분할 검증 계획만 연결한다.

## MV-03

**기존 source/guard**
- scripts/dem_analysis_core.py: 봉인 CODE_FILES32; 이번 내용 열람/수정 없음
- scripts/dem_gen2_qualification.py:29–70,94–122: lens와 기하 접촉면 정의 구분, 모든 겹침 차수 union MC·box clipping·표준오차와 NOT_RUN
- scripts/dem_gen2_t5_contract.py:108–139,170–198,255–283: sphere/union×full/interior 네 estimand·등록 분모·missing 보존

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_dem_gen2_qualification.py:15–43,69–103: 기하·벽 clipping·삼중 포함·극단 반경비 기존 시험
- scripts/test_dem_gen2_t5_contract.py:99–149: 독립 oracle·고정 예정분모·missing/실패

**남은 것**: 합성 union/정의 계약이 sealed core의 역사 pair-only 추정이나 실험 질량 공극률 불일치를 고친 것이 아니다. epsilon_sphere 비준 표적과 실제 측정 규약·보존·압축성·벽 관입·MC/PBC 자격을 별도 확보해야 한다.

**후속 설계만**
- 봉인 core 수정안만. 기존 T5 함수 중복 구현 금지. 실제 규약이 제공될 때 대응 estimand/ROI/분모/clip/PBC를 문서로 확정한다.

## MV-04

**기존 source/guard**
- 원 finding 지정 docs/reviews/codex_review_model_validation_20261008.md §2 MV-04 / §5 Q6–Q7 (이번에는 원장 명세만 사용)
- scripts/make_dem_gen2_decks.py:302–313: synthetic renderer·미등록·physical_ready false

**기존 시험 텍스트(이번 실행 아님)**
- 해당 과학적 estimand를 검증하는 새 시험은 이번 준비 범위에 없음. source/시험을 실행하지 않음.

**남은 것**: 기하 고정 힘 재평가, 동일 체크포인트의 E 변경 뒤 재평형, 새 준비 이력부터의 민감도는 서로 다른 질문이다. 작은 연화 변화에서 실재료 끝점/조성 순위 강건성을 외삽할 수 없다.

**후속 설계만**
- 문장 초안: 동일 체크포인트의 구조·이력을 출발점으로 삼아 강성을 바꾼 뒤 재평형하는 민감도이며, 적분 중 기하가 고정된 비교가 아니다. 기하 고정 계산과 fresh 준비 비교는 별도 estimand로 등록한다.

## MV-05

**기존 source/guard**
- scripts/make_dem_gen2_decks.py:229–258,262–266: 준비/최종 gravity 및 단계 damping을 명시한 합성 렌더
- scripts/dem_gen2_p2_contract.py:129,238,272,353: P2 중 gravity 선언 강제·변경 거부

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_make_dem_gen2_decks.py:100–108: 준비 damping 누출과 최종 gravity 텍스트
- scripts/test_dem_gen2_p2_contract.py:230–238,326–333: 중력/경우를 이름에서 추론하지 않고 post 변경 거부

**남은 것**: P2 중 gravity 고정은 삽입/안정화 과거를 지우지 않는다. 준비 중력·최종 중력·축척·감쇠 및 바꾼 시점을 보정 전 고정해야 한다. 현 합성 상수를 실제 비준 제조 이력으로 승격하지 않는다.

**후속 설계만**
- 과거 고중력 이력이 다른데 같은 마지막 gravity만 가진 두 선언을 별도 protocol identity로 구분하는 후속 계획. 실제 준비 이력 효과는 현장 물리 자격/등록 사항이며 즉시 renderer 중복 수정은 없음.

## MV-06

**기존 source/guard**
- scripts/dem_gen2_t0_contract.py:70–72,82–119: 부호·단위 산술과 실제 T0 미실행 구분
- scripts/dem_gen2_t11_contract.py:133–144,213–224: rational 시간격자·dt/2·동일 physical end/control tick
- scripts/dem_gen2_p2_contract.py:240–244: 동일 물리 window·2배 steps

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_make_dem_gen2_decks.py:119–123
- scripts/test_dem_gen2_t11_contract.py:131–176,213–241
- scripts/test_dem_gen2_p2_contract.py:221–228,249–254

**남은 것**: T0 문법/극성·명목 dt·rational 일치가 endpoint 오차와 이력 정확도를 인증하지 않는다. 현재 source는 실제 build/sign을 None, 자격 NOT_RUN으로 돌려준다. 고강성 시나리오는 재료 정답이 아닌 민감도 조건이다.

**후속 설계만**
- 동일 physical budget/control period/샘플 사건의 dt 및 dt/2 짝을 고정한 실제 자격 계획만 연결. endpoint 차이와 관측 해상도 허용량은 사전 선택이며 새 원자료·실행 없음.

## MV-07

**기존 source/guard**
- scripts/dem_analysis_core.py: 봉인 CODE_FILES32; 이번 내용 열람/수정 없음
- scripts/dem_gen2_live_contract.py:181–220: 선언 frame/units/channel stamp 일치
- scripts/dem_gen2_s0_contract.py:267–338: LIVE boundary·6객체/semantic mapping·bytes 결속

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_dem_gen2_live_contract.py:194–218: channel frame·source/units 바꿔치기
- scripts/test_dem_gen2_s0_contract.py:177–240,252–288: boundary/inventory/atom열/pair 사상

**남은 것**: 전역 virial 합·합성 frame label·6객체 해시는 물리 frame/ID/힘/접촉점 출처나 상별 배분 인증이 아니다. pair 물리 ID, LIVE contact count↔pair/wall 행 수, atom force/velocity/omega→LIVE 채널 재계산은 현 S0 범위 밖이다.

**후속 설계만**
- sealed core 수정은 제안만. 섞인 접촉 배분·상별/공간별 적분·벽 제외 집단/분모·평균 VM과 평균 tensor의 VM 구분을 별도 사전 계획으로 고정한다. 기존 제한 문장을 삭제하지 않는다.

## MV-08

**기존 source/guard**
- scripts/dem_gen2_qualification.py:378–427: exact ID/type/radius/mass·중복/누락·center crossing·surface cut 분리
- scripts/dem_gen2_live_contract.py:257–259: 모든 frame의 전수 재고
- scripts/dem_gen2_s0_contract.py:281–315: 16열 atoms와 boundary 전수 재고
- scripts/dem_gen2_p2_contract.py:377–394: 각 샘플 재고 완전성·동일 S0 재고

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_dem_gen2_qualification.py:185–229: 동일 수/다른 identity·절단·큰 원점/작은 침투
- scripts/test_dem_gen2_live_contract.py:219–230
- scripts/test_dem_gen2_s0_contract.py:218–250
- scripts/test_dem_gen2_p2_contract.py:321–324

**남은 것**: 기존 원자 수만의 방어에서 전수 inventory로 확장된 합성 범위는 이미 있다. 실제 재고의 출처·상별 질량/구체적·유출 부피와 복잡 STL/PBC 경계의 보존 및 공극률 오차 예산은 별도다.

**후속 설계만**
- 동일 수라도 ID/type/radius/mass 바꾸는 반례는 기존 시험이므로 재구현하지 않는다. 후속 비평면 경계/주기면/부분 절단의 geometric oracle·mass-volume accounting 계약만 제안한다.

## MV-09

**기존 source/guard**
- docs/reviews/codex_review_model_validation_20261008.md:145–151의 MV-09 부분만 직접 읽음; 이 문장이 가리키는 docs/data/README·JSON·로그는 읽지 않음

**기존 시험 텍스트(이번 실행 아님)**
- 새 산술/시험/원자료 접근 없음; 지정 판정문에 이미 적힌 서술 오류를 인용하는 문서 정정만 가능

**남은 것**: 보편 ±경계 인용을 철회하면 되는 역사 문장 문제이며 새 런이나 저장 JSON 재산술이 선행 조건이 아니다. 상대값 전체가 잘못됐다는 일반 결론은 아님.

**후속 설계만**
- 정정 문안은 MV09_correction.md로 제공; 역사 원문을 덮어쓰지 않고 출처와 한정이 있는 새 쪽지에 인용 가능.

## GEN2-02

**기존 source/guard**
- scripts/plastic_coverage.py 및 scripts/coverage_physics_vs_hertzian.py: CODE_FILES32 봉인; 기존 census가 확인한 완전 포함 negative-area 거부만 인용
- scripts/dem_gen2_qualification.py:48–61: 별도 합성 기하 contact circle은 containment를 명시 거부

**기존 시험 텍스트(이번 실행 아님)**
- scripts/test_dem_gen2_qualification.py:20–25는 합성 기하 함수 범위; sealed coverage 정책 재현/실행 아님

**남은 것**: 현재 비준은 전체 blank+사유 유지. 포함 쌍 제외 또는 원판 면적 대체를 이 합성 함수로 조용히 대입할 수 없다.

**후속 설계만**
- 정책 선택표와 봉인 수정 제안만. blank/제외 수 기록/대체 정의를 다른 정책으로 명시하고 사용 분모·노출 기록을 분리한다.

## GEN2-04

**기존 source/guard**
- scripts/network_conductivity.py: CODE_FILES32 봉인; 원장에 기재된 mode별 nonpositive area 차이만 사용; source/실제 값 미열람

**기존 시험 텍스트(이번 실행 아님)**
- 새 시험 실행 없음. mode별 synthetic A<0/A=0/A>0 처리 결과·사유·분모 계약 제안만

**남은 것**: 과거 도달성 제한 기록은 원덤프를 새로 읽은 인증이 아니다. mode별 정책 통일/표지/거부 선택은 봉인·등록 경계에 속한다.

**후속 설계만**
- 봉인 수정안만. 실제 간선·원자료를 재조회하거나 기존 승인 없이 에지 정책을 바꾸지 않는다.

## 중복 방지와 방법 한정

- G2PREP-01 signed reaction, -02 지연 first-hit, -03 극단 반경비 contact-area, -04 큰 좌표 inventory 보완은 기존 source·시험이 있다. 수정/재실행하지 않았다.
- 새 LIVE/S0/P2의 전수 재고·경계·byte 결속을 역사 B 결과 종결로 옮기지 않는다. generator의 UNIMPLEMENTED/gate-stop 표시는 실제 engine adapter 미연결을 뜻하며, 새 합성 계약이 없다는 뜻으로 다시 쓰지 않는다.
- 봉인 관련 네 항목(MV-03, MV-07, GEN2-02, GEN2-04)은 제안만. 이번에 해당 sealed source 내용·원자료·docs/data·JSON·로그를 읽지 않았다. 원장 명세에 들어 있는 역사 수치 인용은 원자료 접근/재산술과 구분한다.
- MV-09는 지정 판정문 해당 부분만 직접 읽고 별도 정정 초안을 작성했다. 정정 때문에 새 런/새 연구값 열람이 필요하다고 주장하지 않는다.
- 17개 unsealed source/test의 고정 SHA·Git blob OID는 d5_scope.json에 있다. 소스 텍스트를 읽었고 실행하거나 import하지 않았다. 신규 구현/시험 코드0·프로젝트 실행0·repo/원장/봉인 변경0·host0.
- 이 보고서는 제한된 범위의 구현 큐 진단이다. 전수 보안/수학/물리 감사나 새 독립 반박 판정, 모든 정적 결함 부재 주장은 아니다.
