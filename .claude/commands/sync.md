---
description: 세션 시작 — 안전하게 최신 상태로 맞추고 상대가 뭘 했는지 확인합니다
allowed-tools: Bash(git:*), Bash(make:*)
---

두 사람이 같은 브랜치를 공유합니다. 작업을 시작하기 전에:

1. `make sync` (= `git pull --rebase --autostash`) 를 실행합니다.
   작업 중이던 변경은 자동으로 넣었다 빼주므로 커밋하지 않아도 됩니다.
2. `git log --oneline -15` 로 상대가 방금 무엇을 했는지 확인합니다.
3. `python3 tools/wiki_status.py` 로 저장소 현황을 봅니다.
4. rebase 충돌이 나면 `.claude/skills/shared-branch-workflow/SKILL.md` 의
   규칙을 따릅니다 — `docs/log.md` 는 양쪽 항목을 모두 남깁니다.

마지막에 이번 세션에서 무엇을 할지 한 문장으로 정리하고, 상대의 최근 커밋과
겹치는 부분이 있으면 지적하세요.
