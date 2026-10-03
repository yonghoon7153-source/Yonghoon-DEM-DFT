# Gate87 회신 — 2b 종결 보류 / G87-N1 P1 한 건

고정 HEAD `672ab83b209c925c3d83ab0fca9b39b90d87f1fd`, 생산 코드 `b8d4b69338f00083ece7e554660888b41d1b4905`를 검토했다. RUN_SCOPE 58개에서 source_digest `864edfb73b9695a1`을 독립 재계산했고, 생산 변경은 run.sh/fitting.py/preserve.py 세 파일뿐이다. 받은 코드·시험·COMSOL·연구 계산은 실행하지 않았다.

v5 builder AST/골든 불변, v3 spec와 envelope/index 결속, CLI 배선, 기존 preflight/prepare 유지, R2-c 이름 체계는 수용한다. 13개 원문 로그의 크기/SHA와 2109 passed/1 xfailed, smoke rc0, 전체 변이 374/374 rc0를 확인했다. history 원문 보존과 새 영수증의 제한된 차이도 수용한다. 2a 종결은 유지한다.

**G87-N1(P1): 새 비-smoke v6 fit-only 경로가 기존 grid→fit phase 완료 규칙과 맞지 않는다.**

- shell은 stage3-plan을 fit 전용으로 제한한다.
- 새 claim은 `phases={}`로 시작한다. 올바른 외부 입력 package digest는 같은 claim의 grid 영수증 없이 입력 검사를 통과한다.
- fit 본체가 정상 반환하면 `src/fitting.py:1735`의 commit 뒤 `:1740`에서 fit phase를 기록한다.
- `tools/preserve.py:3997`은 여전히 `CLAIM_PHASES=("grid","fit")`; `:6895` 이후는 grid가 없으면 fit 완료를 거부한다. finalize도 두 phase를 요구한다.
- 기존 grid production gate는 여전히 v2 spec을 만들어 v3 승인/claim과 불일치한다. 따라서 “그냥 grid를 먼저”도 제시된 v6 경로가 아니다.

이는 **정적 호출/상태 추적으로 확인한 결함**이며 새 실행 실패를 관측했다고 주장하지 않는다. `s02_04`는 claim 발급까지만, `s04_01` 완주는 smoke(claim=None)라 `_record_phase`가 건너뛰어진다. 두 양성을 합쳐 비-smoke 실행 완료로 볼 수 없다.

다음 범위는 이 한 건으로 한정한다. 외부 producer 입력의 결속과 v6 fit-only의 완료/재개/최종화 계약을 먼저 고정하고 사용자 승인 뒤 보완하라. v2 순서 규칙 삭제, 가짜 grid 영수증 삽입, smoke 우회는 수용하지 않는다. 격리 원장·비-smoke 출력에서 실제 claim/phase/종결 경로를 통과하는 양성 및 입력/attempt/순서 위반 음성을 연결하라. 수치 본체는 inert 가능하나 lifecycle을 대체하지 말라. 입력 대조는 curves 단독 SHA가 아닌 실제 input-package digest를 사용하라.

변경 파일 범위가 기존 승인을 넘으면 먼저 그 차이만 승인 요청하라. 새 연구 leg·운영 v6 계획·세대표 등록·p_ini·class/투영 게시·실행 GO는 여전히 별개다. 이번 회신 자체는 구현·시험 실행 승인이 아니다.

판정: **REQUEST_CHANGES / ROUND2B_NOT_CLOSED — P1 1건.** 이미 수용한 부분과 과거 원문·중단/실패 기록은 다시 열거나 고치지 않는다.
