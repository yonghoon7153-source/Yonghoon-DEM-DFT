---
description: 세션 마무리 — 검사, 로그 기록, 커밋, 푸시
allowed-tools: Bash(git:*), Bash(make:*), Bash(python3:*), Bash(npx:*), Read, Edit
---

1. `/check` 를 먼저 통과시킵니다.
2. `docs/log.md` 에 이번 세션의 항목을 **추가**합니다 (append-only):
   `## [YYYY-MM-DD] <action> | <무엇을>`
   action: `create` `update` `ingest` `verify` `lint` `fix` `start`
3. 새 위키 페이지나 ADR 을 만들었으면 `docs/index.md` 에 등재합니다.
4. `git add -A && git status` 로 **`data/` 가 섞이지 않았는지** 확인합니다.
5. 커밋 메시지: prefix + 한 줄 요약 + 본문.
   - 숫자가 바뀌는 변경이면 실측 파일 기준 before/after 를 본문에 넣습니다.
   - 모델 이름이나 세션 링크는 넣지 않습니다.
6. `git push` — 거절되면 `make sync && /check && git push`.
   **`--force` 는 쓰지 않습니다.**

마지막에 이번 세션에서 바뀐 것과, 다음 사람이 알아야 할 것을 3줄 이내로
정리하세요.
