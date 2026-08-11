---
description: 위키 세션 마무리 — lint → log/index 확인 → 커밋
---

1. `python3 wiki/tools/lint.py` — 0 errors 될 때까지 커밋하지 않는다.
2. `git status` 로 이번 세션의 wiki/ 변경을 보고 `wiki/log.md` 에 대응 항목이 있는지,
   새 페이지가 `wiki/index.md` 에 등록됐는지 확인한다 (lint 가 잡아준다).
3. 커밋: prefix `wiki: <action> — <subject>`. 논리적으로 다른 작업은 나눠 커밋.
   ⚠ 커밋 메시지에도 모델 ID 금지 (리포 규칙).
4. 지정 브랜치(claude/stoic-knuth-NObVQ)로 push (리포 git 규약의 재시도 포함).
5. `python3 wiki/tools/status.py` 로 마무리 보고.
