# Codex 리뷰 과제 — 워크벤치 전수 리뷰

[codex-session-bootstrap.md](codex-session-bootstrap.md) 로 세션을 연 뒤, 아래를
붙여넣는다. 목적은 **독립** 리뷰다 — Claude 쪽 감사 결과와 교차검증해서
양쪽이 다 놓친 것을 줄이는 게 목표이므로, Codex 가 우리 결과를 먼저 보면
의미가 없다.

## 붙여넣는 프롬프트

```text
이 브랜치의 코드와 Markdown 전체를 전수 리뷰해줘. 결과는
docs/reviews/2026-08-20-codex-review.md 한 파일로 작성해서 이 브랜치에
커밋해줘 (push 는 내가 말하면).

중요 — 독립성: docs/reviews/2026-08-20-internal-audit.md 는 Claude 쪽 감사
결과다. 너의 리뷰가 끝나서 커밋하기 전까지 절대 열지 마라. 커밋한 뒤에만
열어서 마지막 절(교차표)을 작성하라.

리뷰 범위와 우선순위 (위에서부터 중요):

1. 도메인 수치의 정확성 — 틀리면 데이터가 조용히 망가지는 곳:
   - 시간: .NET tick(100ns) → 초 변환이 wrd.seconds() 를 거치는가, 직접
     나누는 곳은 없는가
   - 용량: UnitCoulomb 플래그(False=Ah, True=C) 처리, charge_mah()/
     discharge_mah() 우회 경로
   - CHARGE Q/DISCHARGE Q 는 사이클마다 리셋되는 누적값 — 사이클 용량을
     차분이 아닌 방식으로 구하는 곳이 있는가
   - 스텝 분할이 TOTAL STEP 기준인가 (전류 부호나 CELL STATUS 로 나누는
     곳은 없는가), CELL STATUS 1/3/4 의 해석
   - 평균 전압이 에너지 가중(E/Q)인가
   - 기준 사이클 3 (1~2 는 formation) — 유지율·초기 쿨롱효율·knee 탐색이
     전부 이 기준을 지키는가
   - 미완료 마지막 사이클(CycleSummary.complete=False)이 보고되는 경로
   - mAh/g 분모: 활물질 질량만. 미인식 성분이 활물질로 분류되는 경로.
     0 wt% 성분 처리
2. 파서 vs 스펙: packages/wrdkit/nrbf.py, wrd.py 를
   docs/raw/specs/wrd-binary-format.md 와 바이트 단위로 대조. 오프셋,
   가변폭 문자열, dtype 구성, 경계(잘린 파일·빈 파일)
3. 저장 원칙: DB 에 정규화된 값이 저장되는 곳은 없는가 (raw mAh/V/s 만).
   질량을 고치면 재파싱 없이 모든 수치가 따라오는가
4. API: 업로드(sha256 중복, 크기 제한, 부분 실패), npz 캐시 무효화,
   _add_missing_columns 마이그레이션의 한계, SPA 서빙의 경로 탈출,
   라우터가 wrdkit 불변식을 우회하는 곳
5. 프론트: TypeScript 타입 vs 실제 API 응답, uPlot 다중 시리즈 병합,
   i18n 폴백, 숫자 포맷, 질량 수정 후 즉시 반영
6. tools/bml: 포트 소유 판정(남의 프로세스를 죽일 수 있는 경로),
   pull 이 자기 자신을 갱신할 때의 재실행, 워크벤치가 아닌 체크아웃 가드.
   tools/tests/test_bml_ownership.sh 가 고정하는 규칙과 코드의 일치
7. 테스트: packages/wrdkit/tests/synthetic.py 가 실제 .wrd 규약과 같은
   방식으로 픽스처를 만드는가 (픽스처가 틀리면 테스트 전체가 같은 방향으로
   틀린다). 커버되지 않는 실패 경로
8. 문서-코드 일치: CLAUDE.md/AGENTS.md parity 와 3장 불변식, SCHEMA.md vs
   models.py, ADR 0001~0009 vs 구현, guides 의 명령·출력 예시 vs 실제

보고 형식 (2026-08-20-codex-review.md):

## 요약
전체 평가 3~5문장, 발견 수(심각도별).

## 발견
심각도 내림차순 표. 각 항목:
| # | 심각도 | 파일:줄 | 제목 | 실패 시나리오 | 제안 수정 |
실패 시나리오는 "어떤 입력/상태 → 어떤 잘못된 출력" 형식의 구체적 경로.
스타일·취향은 싣지 않는다. 확신이 없으면 다음 절로.

## 질문 / 확신 없음
결함인지 판단이 안 서는 것들. 왜 애매한지 한 줄씩.

## 이상 없음을 확인한 것
검토했고 문제 없다고 판단한 영역 목록 (교차검증에서 커버리지 비교에 쓴다).

## 교차표 (리뷰 커밋 후에만 작성)
internal-audit.md 를 열고:
| 항목 | 우리만 | Codex만 | 양쪽 | 판정 |
불일치 항목은 어느 쪽 판단이 왜 맞는지 근거를 적는다.
```

## 종결 절차 (사람 + Claude)

1. Codex 리뷰 커밋을 받으면 Claude 세션에 "codex 리뷰 나왔어" 라고 알린다.
2. Claude 가 교차표를 검토한다:
   - **양쪽 발견** → 즉시 수정 대상
   - **한쪽만 발견** → 상대 근거로 재검증 후 판정 (반박 라운드 한 번 더)
   - **판정 불일치** → 코드로 재현해 보는 쪽이 이긴다. 재현 안 되면 기각
3. 확정 결함은 claude/battery-charge-discharge-webapp-dq4ja3 에 수정 커밋,
   internal-audit.md 의 해당 항목에 처리 결과를 적는다.
4. 남는 것 없으면 리뷰 종료 — log.md 에 한 줄 남기고 닫는다.
