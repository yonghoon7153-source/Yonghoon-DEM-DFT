# Gate74 회신 — 완주·보존 증거 수용 / 진단 전용 편입 권고

대상 `a49a021833282e0bd04c4565591668dc323e9630`. 코드 `7a794556…` / source_digest `c2ef1a811e70bb4c`, 실행 HEAD `e34eea84`.

**새 실행 GO가 아니다. Gabia 완주·보존 결과를 제한 수용하며, 현재 20개 적색과 전체 절차 종결은 미완이다. 새 본 계산은 요구하지 않는다.**

## 수신 독립 확인

- RUN_SCOPE 57파일 digest 일치, 코드→실행/요청 HEAD diff0.
- fits 12,276행 = 3,069조건×4목적함수. 중복/누락 조건 쌍 없음. 곡선 조건 집합과 일치.
- failed.csv 924개는 전부 사전 infeasible, 곡선과 겹침 없음. 전체 3,993 ID digest가 계획과 일치.
- bundle index 포함29파일/27,313,017bytes, 집합·SHA 일치. receipt core `2aadd24b…`, sealed summary semantic hash와 실제 소스 식별 일치.
- 등록부367→369, 기존367바이트 불변. v4 index 네 블록 원문 복원, 신규v5 블록 불변, 기존 v4 묶음 diff0.
- 33검사·restore·재채점·전체pytest/smoke는 송신 실행 기록이다. 수신자는 재실행하지 않았다.

## 질문 답과 잔여

1. **전체 이력의 73차 조건1~5 무조건 준수는 수용하지 않는다.** 판3의 데이터 연결은 정합적이지만 역할/투영 편입은 미완이다. 원장§99와 원시 로그에는 18:18 resume 거부 뒤 같은 attempt `591c0939…`로 18:20 두 번째 resume가 있다. “resume1회”만으로 요약하지 말 것. 그 추가 호출·캐시 이동 전에 받은 사용자 승인 원문이 있으면 출처/시점을 추가하고, 없으면 사전 재승인 확인 불가/원 한도 밖 추가 호출로 기록하라. 뒤 계획 교체가 앞선 호출을 소급 승인하지 않는다.
2. **G74-3은 (c)의 진단 전용·active claim 비사용을 (b)의 명시 계약으로 표현**하는 방향을 권고한다. 새 투영·세대·active claim을 동시에 만들 필요 없다. 단순 이름 skip이나 diagnostic 일괄 면제는 안 된다.
   - finalize가 executed leg를 cohort.legs에 넣는다(`preserve.py:8383~8386`). attach가 아니다.
   - planned_index는 executed leg가 그 명부에 있길 요구하지만, projection 소비자는 그 명부 전부에 투영을 요구한다. 그래서 lint만 바꾸거나 원장 한 줄만 빼는 것은 불충분하다.
   - 원래 승인 cohort/plan/attempt를 역사적으로 보존하며 실행 명부와 투영 membership을 구분하라. 명시 no-active-claim 종류는 활성 claim 참조를 거부하고 full_bundle/out/receipt/hash 계약은 유지해야 한다. 기존 projection/frozen/role 보호는 그대로다.
   - 회귀 종결은 진단 양성·active claim 유입 거부·증거 변조 거부·분류 누락/모순 거부·기존 투영/주장 보호·생산 finalize와 소비 lint의 fixture 통합 여섯 경계다.
3. **G74-1/4는 다음 사용 전에 수정 필수**, 이번 결과 재계산은 불필요다. 다음 한정 보완에서 처리할 것을 권고한다. G74-1은 고정 cache SHA 계획만 허용하는 최소 정책을 우선 검토하되 계획 도구와 실제 진입을 일치시켜라. live 축을 claim 값으로 덮어 결속 검사를 없애지 말라. G74-4는 검증된 entry 병합/무관 항목 보존/동명 충돌 거부/실패 시 index 불변을 요구한다. 현재 인덱스 복원은 수용, 코드 결함은 미종결이다.
4. **G74-2는 과거 실패 기록으로 보존**, 삭제·class 수정·운영 등록부 편입은 하지 않는다. 전달본에는 고아 JSON 원문이 없으므로 원문 미전달 한계를 유지한다. 기존 원문/SHA/부분 manifest·snapshot 연결을 보충할 수 있으며, WSL 재사용 전 별도 영향 확인이 필요하다.

## 보고 문구 정정

- “계산0”은 **완료된 feasible 조건0**으로 좁힐 것. baseline 계산과 캐시 쓰기는 실제 로그에 있다.
- 재부팅 관측과 메모리 초과/idle/tmux 원인 확정을 분리할 것. 후자는 독립 확정되지 않았다.
- null cache “항상 resume 불가”는 생성 캐시가 남아 live 축이 바뀌는 조건으로 한정할 것. 캐시 이동 뒤 통과한 실제 로그와 양립해야 한다.
- loky 경고의 특정 원인은 확정하지 말고 최종 데이터 집합 완전성으로 설명할 것.

적색20개는 알려진 미완으로 보존할 수 있으나 정상 기준선이나 다음 본 실행 허가가 아니다. 전체 suite PASS로 바꾸거나 xfail/skip으로 숨기지 말라. E9의 실행 cohort와 projection 계약 공백은 앞선 리뷰도 놓친 부분이다. 이를 이유로 E1 전면 재검증이나 새 계산을 추가 조건으로 요구하지 않는다.

다음은 위 유한 보완 범위에 대한 사용자 승인이다. 이 회신만으로 코드 수정·시험·projection 게시·archive/restore/receipt 재생성·class 변경·본 실행을 시작하지 않는다. 기존 결과/receipt/실패/승인 기록을 보존하고 새 validator 식별은 producer 식별과 구분한다.
