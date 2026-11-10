# D-3/S0 — 선언 경계·6객체·순수 bytes 한정 검토

발송=1저자. 고정 핀은 11-10 하루 묶음 `PIN_MANIFEST.json`에 제공한다. 바탕은 LIVE `63a513560c2770990920065be94ef966a8be018b`. **독립 판정 PENDING·실제 S0/T12 NOT_RUN·전체 HOLD.**

| 이번에 닫으려는 것 | 닫지 않는 것 |
|---|---|
| 원 LIVE 입력 재검증 뒤 동일 R-a 끝 후보·고정 digest에 6종 객체를 결속하는 선언 계약 | 실제 생성 시점·출처 진위·물리 동시관측·숨은 이력·복원 자격 |
| atom16·전수 ID/type/radius/mass, pair26/wall U·R의 명시 사상, payload 바이트·길이/hash·생성 순서/부모 사슬 검사 | pair의 물리 ID 의미·LIVE contact count와 pair/wall 행 수 일치·atom 힘/속도/omega로 LIVE 채널 재계산 |
| canonical JSON/UTF-8/base64 encode/decode, 중복 키·비유한·다른 bytes·누락 객체/열 거부 | 실제 파일 기록·checkpoint/restart 해석·P1/r8 소비자 수정·운영 source seal 교체·발사 GO |

**권고안 전제(Q-S0-1/2)**. mesh/restart/state는 불투명한 합성 바이트다. pair 현재 overlap이나 wall 관측 열·hash가 숨은 이력의 물리 자격이라는 뜻이 아니다. 실제 상세 P2 사상·빌드/이력 자격은 미정이다.

## 1. 독립 확인 질문

1. caller가 준 PASS 문자열 대신 원 LIVE plan/servo/R-a trace를 다시 검사하는가? frozen boundary hash 및 후보 전체 bytes가 모두 맞아야 하는가?
2. atom/pair/wall/mesh/restart/state 순서·끝 step·mesh/wall/history/inventory·generation ordinal·부모 사슬이 다른 경계의 객체를 거부하는가?
3. atom의 필수16열·고유 정수 ID·type/radius/mass 전수 대조가 작동하는가? mass/omega 결손이나 같은 개수의 다른 ID가 정상 부분표로 축소되지 않는가?
4. pair26·wall U/R은 명시한 열/단위/의미 사상에 결속되는가? 현재 overlap을 hidden δmax로 이름만 바꾸거나 hidden-history-qualified=true로 승격할 수 없는가?
5. 전달 payload 원바이트로 길이·SHA를 다시 계산하고 canonical base64/JSON/UTF-8을 강제하는가? body hash의 순환을 피하고 decode 뒤 전체 입력을 재검증하는가?
6. 작은 합성 크기 한계·비유한·중복 JSON key·unknown field·하위형·깨진 원본이 거부되며, 실패 뒤 다른 파일/프레임 자동 대체가 없는가?
7. 시험 수와 순서가 정확한가? 사전 구현 초안 존재, 스텁 red의 assertion/subtest 실패 82와 오류 1, 후보 22/22, 변이8개, 시험 실행 전 준비 중단1회를 구분했는가? 오류1은 명시 미구현 serializer 호출이며 물리 반례로 세지 않는가?

## 2. 증거와 제한

README·계약 양식·`verification_summary.json`과 고정 원 소스/시험, 스텁·선작성 초안·후보, 원 영수증·변이·원시 manifest를 대조한다. 새 scratch의 작은 합성 입력만 사용한다. 기존 전체 suite·현장/자료/로그·engine/MPI/Slurm·Rint·전체 gate/CI는 이 검토 범위 밖이다.

이 후보의 형식/선언/바이트 수용으로 실제 물리 S0, P2 ULPR/T12, binary/재개/시간 자격, 운영 봉인 또는 실행 GO가 생기지 않는다.
