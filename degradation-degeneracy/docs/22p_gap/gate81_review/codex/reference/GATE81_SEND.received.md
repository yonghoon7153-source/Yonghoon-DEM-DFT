# 81차 게이트 리뷰 요청 — 발송문 (2026-09-28)

**요청문:** `degradation-degeneracy/docs/22p_gap/GATE81_REQUEST.md`
**브랜치:** `claude/gate80-standby-9a26dd5f` (임시 대피 서브 — 본진 `claude/14-gate-code-review-9qkx05` 는 `9a26dd5f31ca6fae45d5a55f5c59e33408371984` 에서 동결 · 서브는 그 ff 후손)
**발송 SHA (요청 HEAD):** `88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e`
**판정 대상 코드 (RUN_SCOPE 마지막 변경):** `6ffa98d4df542aa42abde2f94685beffec33312c` · `source_digest eda3feb8f4536511` — 80차와 같다. 이 요청은 코드를 바꾸지 않는다 (RUN_SCOPE diff 9a26dd5f→HEAD 0 파일 · 6ffa98d4→HEAD 0 파일, 실측).

**묻는 것:** 단계 3 의 **제한 구현 범위**(GATE78 §3.2 단계 3 을 3-A 결속 · 3-B provider DAG · 3-C 행·검증 세 조각으로) 와 **사전 고정 사항**(GATE78 §3.1 재확인) 의 확인, 갈림 4곳(unit-cube bank · 혼합 restart 행 정책 · provider 봉인 실물 · ID 도메인 불변) 판정. **묻지 않는 것:** 구현 착수 (회신 뒤 사용자 별도 승인) · 실행 GO · pilot · 새 연구 계산.

## 실측 (요청문 커밋 `88ac144a` = clean HEAD 에서 · 시작 HEAD = 끝 HEAD = `88ac144a` · 시작/끝 미추적 0 · 실행 중 커밋 없음 · 2026-09-28 01:55:13Z → 03:09:28Z)

```
docs-lint (tests/test_docs_lint.py 단독)      358 passed · 0 failed (1321.73 s) · rc 0
전체 pytest (tests/)                          0 failed · 1960 passed · 1 xfailed (2951.96 s = 49:11) · rc 0
strict smoke (scripts/smoke_e2e.sh)           rc 0 · "✅ pipeline smoke 통과" (176 s — 작은 grid/fit/score/restore 계산 포함, 연구용 새 실행 0)
source_digest                                 eda3feb8f4536511
RUN_SCOPE diff 9a26dd5f..HEAD / 6ffa98d4..HEAD   0 / 0 파일
```

## 스스로 신고하는 것 (같은 SHA 의 첫 실행)

- 이 SHA 의 **첫 실행은 환경 때문에 실패**했다 (코드·문서 변경 없음). 새 컨테이너가 (a) 얕은 클론(커밋 598 개)이라 과거 요청문이 인용한 커밋이 없었고 (b) `requirements.txt` 의존성(`pybamm` · `matplotlib` · `joblib` · `pytest-json-report` 등)이 설치돼 있지 않았다. 결과: docs-lint 4 failed / 354 passed — 그중 `test_committed_gate_requests_are_self_contained` 는 "존재하지 않는 커밋" (얕은 클론) 을 확인했고 나머지 3 건은 원인을 개별 확인하지 않았다 · 전체 pytest 수집 오류 3 (`ModuleNotFoundError: matplotlib`) · smoke rc 1 (`ModuleNotFoundError: pybamm`/`joblib`).
- 조치: `pip install -r requirements.txt` · `git fetch --unshallow` (커밋 1106 개). 트리·HEAD 는 그대로 (`88ac144a`, 미추적 0) — 그 뒤 **같은 SHA 에서 처음부터 다시** 실행한 값이 위 표다.

## fetch

```
git fetch origin claude/gate80-standby-9a26dd5f
git checkout 88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e
git merge-base --is-ancestor 9a26dd5f31ca6fae45d5a55f5c59e33408371984 88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e && echo FF_OK
```

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요. 이 발송문과 요청문은 같은 말을 한다: **단계 3 의 제한 구현 범위와 사전 고정 사항의 확인을 요청한다. 구현 착수도 실행 GO 도 묻지 않는다.**
