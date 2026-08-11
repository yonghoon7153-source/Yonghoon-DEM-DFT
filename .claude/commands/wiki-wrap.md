---
description: 세션 마무리 — lint, log 정리, git commit 원터치
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

이 세션의 위키 작업을 마무리한다.

절차:

1. **Lint**: `python3 wiki/tools/lint.py` 실행. ERRORS 가 있으면 사용자 승인 하에 고치고 재실행 — 0 errors 가 될 때까지 커밋하지 않는다.
2. **Log 확인**: `git status` 로 이번 세션의 변경 파일을 보고, `wiki/log.md` 에 대응하는 항목이 있는지 확인한다. 빠진 작업이 있으면 `## [YYYY-MM-DD] action | subject` 형식으로 append 한다.
3. **Index 확인**: 새 페이지가 있었다면 `wiki/index.md` 등록과 Total pages 카운트를 확인한다 (lint 가 잡아준다).
4. **Commit**: 변경을 스테이지하고 커밋한다. 메시지는 세션의 지배적 작업에 맞는 prefix (`ingest:` `update:` `create:` `lint:` `verify:`) + 한 줄 요약 + 필요하면 본문 bullet. 논리적으로 다른 작업이 섞여 있으면 나눠 커밋한다.
5. **Push**: remote 가 설정되어 있으면 push 한다. 없으면 로컬 커밋까지만.
6. **스냅샷**: `python3 wiki/tools/status.py` 를 실행해 현재 상태와 다음 추천 행동 1가지로 마무리 보고한다.
