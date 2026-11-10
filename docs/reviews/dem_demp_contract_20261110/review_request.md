# D-3/DEMP 선언·비교 요구 계약 — 독립 한정 검토 요청

바탕=`b7fbe749ea8ffa3151b3e768de445c572940c43d`. 후보 exact pin/blob과 증거는11-10 하루 묶음에 고정한다. 발송은1저자, 반입·원장처분은Claude다. 본 요청은 작성측 자료이며 독립 판정이 아니다.

## 1. 검토할 것

**권고안 전제(Q-DEMP-1/2/3)** 아래 `validate_demp_contract(plan, packets, context)`의 선언·상태 대조만 확인한다. 7단계×두명목입경의 예정분모, global/contact damping·반력/수지/KE의 서로 다른 signed/units/frame 선언, 고정재고, 중심/표면 분류label, 같은RA_END 비교규약을 다룬다. 원자/접촉으로 힘·토크를 계산하거나 좌표/STL의 실제관통을 계산하는 함수가 아니다.

| 질문 | 대조 | 닫지 않는 범위 |
|---|---|---|
| Q1 DEMP-01 | 압축에 준비감쇠 암묵상속·global/contact 합침·unsigned/단위/창혼입·채널누락 거부 | 실제 감쇠기여·힘수지·허용예산·원물리지적 종결 |
| Q2 DEMP-02 | 같은N/다른 ID·상·radius/mass 정의, history교체, center와surface claim모순, 중간OUTSIDE/UNKNOWN | 분류는 제공된 label 행수; per-particle 기하/연속궤적·실제누설 인증 아님 |
| Q3 두입경 | 두명목입경의 전체RA_END 규약·recipe·단위/면적/종점 사상 일치, N동일 강제없음 | 실제입경분포·50kg하중환산·정적상태·실제 비교가능성 |
| Q4 단계/분모 | CASE_GLOBAL_DECLARATION에서 뒤단계창의 역행/겹침, 누락·부분·실패·추가/중복을 구분 | 실제 stage-local/reset_timestep 사상은 미확정·미지원; 실패를 실제자료결함으로 일반화 금지 |
| Q5 권한 | actual facts null·demp01/02_closed false·actual_state_comparable false·GO false | 원장종결·운영재봉인·현장/값접근·실행권한 |

자격행렬 핀은 선언된 의존 신원이며 이함수에서 자격행렬 API를 호출한 것은 아니다. 실제 source/metadata 진위 인증을 하지 않는다. D9′의 비준된 ε_sphere 표적·ε_union 기록정책을 유지하며 다시 비준받거나 새 실측값으로 만들지 않는다.

## 2. 반례와 증거

시험·fail-closed stub 작성 후24메서드 red2=실패14·오류0→첫구현24/24. 초기 fixture는 단계별local step이었다. 작성측 정적 검토에서 단계간순서 공백을 찾아 CASE_GLOBAL로 정규화하고25번째 반례를 먼저추가했다. 이전source에서 역행/겹침 실패2·오류0→최소순서검사뒤25/25다. CASE_GLOBAL은 이번합성지원전제이지 실제엔진의 시간정의를 임의변경한 것이아니다.

최종 source SHA256=`7490b921d8015d237c52f18461cddb97bd8d373637f95107056309d309a18639`, test SHA256=`e399ac13ab6c5fd9f3e6eb56a61725adad38d391feace7c9446d5d5483a5fd12`. 최종 보호조건 약화8/8 검출·각오류0. 최초 준비중단은 sparse새가지의 scripts디렉터리누락으로 대상시험0이며, 원기록 보존범위는 `verification_summary.json`에 구분한다. 서로다른suite·실패관측·변이 반복을 합산하지 않는다.

실제 T0/T5/T11/T12·binary/이력/재개·정적상태·운영봉인/실행GO·전체gate/CI는 이검토로닫지않는다. 원자료·원로그/값·호스트 접근과 연구결과0, 전체HOLD.
