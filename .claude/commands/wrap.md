---
description: 세션 마무리 — 검사, 로그 기록, 커밋, 푸시
allowed-tools: Bash(git:*), Bash(make:*), Bash(bml:*), Bash(python3:*), Bash(npx:*), Read, Edit
---

1. `/check` 를 먼저 통과시킵니다.
2. `docs/log.md` 에 **커밋마다 한 줄씩** 추가합니다 (append-only):
   `## [YYYY-MM-DD] <action> | <무엇을>`
   action: `create` `update` `ingest` `verify` `lint` `fix` `start`
   - **항목 제목은 커밋 제목과 같게 씁니다.** `fix: <제목>` ↔
     `## [날짜] fix | <제목>`. 같아야 `bml feed` 가 둘을 짝지어 주고, 상대
     세션이 "이 커밋이 왜 있는지" 를 찾을 수 있습니다.
   - 담을 것은 **커밋 메시지에 안 들어간 것**입니다: 무엇을 보고 그렇게
     판단했는지, 실측 값, 일부러 남긴 것과 그 이유, 다음 사람이 건드리면
     안 되는 것.
3. 새 위키 페이지나 ADR 을 만들었으면 `docs/index.md` 에 등재합니다.
4. `git add -A && git status` 로 **`data/` 가 섞이지 않았는지** 확인합니다.
5. 커밋 메시지: prefix + 한 줄 요약 + 본문.
   - 숫자가 바뀌는 변경이면 실측 파일 기준 before/after 를 본문에 넣습니다.
   - 모델 이름이나 세션 링크는 넣지 않습니다.
6. `git push` — 거절되면 `make sync && /check && git push`.
   **`--force` 는 쓰지 않습니다.**
7. **`bml feed`** 로 마무리합니다. `○` 가 남아 있으면 그 커밋의 기록이
   빠진 것이고, 상대 세션은 그 '왜' 를 볼 수 없습니다. push 전에 채웁니다.

마지막에 이번 세션에서 바뀐 것과, 다음 사람이 알아야 할 것을 3줄 이내로
정리하세요.
