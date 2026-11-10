# D-3 마지막 — DEMP-01/02와 두 입경 비교 요구

| 1저자 결정 칸 | 권고 한 줄 | 준비 중 적용 |
|---|---|---|
| Q-DEMP-1: 단계/수지증거 | global/contact 감쇠·signed 반력/수지·단위/창을 분리하고 CASE_GLOBAL 선언창의 순서를 대조 | **권고안 전제(Q-DEMP-1)**; 실제힘재계산/시간사상 아님 |
| Q-DEMP-2: 기하/보존증거 | 기준재고·중심통과·표면절단·관측간 미확인을 분리 | **권고안 전제(Q-DEMP-2)**; label일관성만, 실제STL/PBC/연속성자격 아님 |
| Q-DEMP-3: 두입경 비교 | 같은RA_END의 전체규약/recipe를 결속하고 N동일은 요구하지 않음 | **권고안 전제(Q-DEMP-3)**; 실제하중/면적/정적상태 미확정 |

## 1. 바탕·산출물

| 항목 | 상태 | 근거 | 다음 |
|---|---|---|---|
| 새 가지 | `codex/dem-demp-contract-1110`, 바탕 자격행렬 `b7fbe749ea8ffa3151b3e768de445c572940c43d` | 상시 D-3 | 독립 한정 검토 PENDING |
| 순수 메타 API | 1개·예정14packet | `scripts/dem_gen2_demp_contract.py`; `docs/reviews/dem_demp_contract_20261110/README.md` | 채널·분류label·누락/부분/실패 대조 |
| 50kg/입경 | 과제표지/정확뜻UNKNOWN·하중환산NOT_ESTABLISHED; 두명목입경 선언 | 같은 폴더 `contract_draft.json` | 실제분포·측정규약·면적·하중은1저자 메타 제공 뒤 |
| 실제처분 | DEMP01/02 closed=false·actual_state_comparable=false·actual facts null | 모든권한false | 실제원지적종결/재누르기/실행GO0·전체HOLD |

## 2. 시험 먼저·추가 반례

| 기록 | 결과 | 구분 |
|---|---|---|
| 최초준비중단 | 대상시험0 | 새sparse가지의 scripts디렉터리누락; 구현본문작성전 |
| 고정24메서드 스텁 red2 | 실패14·오류0·rc1 | 이관측 뒤 첫구현 작성 |
| 첫구현 green | 24/24·오류0 | 초기stage-local toyfixture |
| CASE_GLOBAL 정규화+순서반례 | 25메서드·실패2·오류0 | 이전source에서역행/겹침을먼저확인 |
| 최소순서검사 뒤 | 25/25·오류0 | 실제stage-local/reset규약은미확정그대로 |
| 최종보호조건약화 | 8/8 검출·각오류0 | 직접메서드/내부관측/반복을더하지않음 |

최종source SHA256=`7490b921d8015d237c52f18461cddb97bd8d373637f95107056309d309a18639`, test SHA256=`e399ac13ab6c5fd9f3e6eb56a61725adad38d391feace7c9446d5d5483a5fd12`. 세부순서·준비오류 보존한계·가드원기록은검증요약과일일증거에묶는다.

분류수는제공된center/sphere label행수이며 원자별기하/궤적재계산결과가아니다. force/torque/관통계산·원자료reader·자격행렬API호출도없다. D9′정책은비준대로유지한다. 기존코드·봉인32·Rint·gate·원장수정0, 실제engine/현장/연구결과0, 전체gate/CI NOT_RUN. 전체턴 문서노출예외는 `20261110-0121_dem-t5-contract.md` §3대로다.

최초준비중단 stderr는 원파일 미보존·도구대화만이며 사후관찰기록과구분했다. raw manifest는97파일(자체제외), SHA256=`290fb981fb71dd7ac9b85c9b29cd345c5be7924b53297203ab913686b6b7ce55`다.

## 3. 반입·다음

반입커밋=`<<sha:Prepare synthetic DEMP evidence contract>>`. 독립검토요청=`docs/reviews/dem_demp_contract_20261110/review_request.md`, exact핀·원시증거는11-10 하루묶음ZIP. 발송=1저자, cherry-pick -x·원장처분=Claude.

D-3의요청칸을문서·합성계약범위로이어준상태이며 실제자격완료는아니다. 다음은 D-4 전체게이트 연결의미적용패치초안, 이어D-5 열린항목의기존수정/봉인제안·문서정정으로간다. 실제gate는Claude담당이며이번창에서실행하지않는다.
