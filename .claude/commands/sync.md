---
description: 세션 시작 — 안전하게 최신 상태로 맞추고 상대가 뭘 했는지 확인합니다
allowed-tools: Bash(git:*), Bash(make:*), Bash(bml:*), Bash(bash tools/*), Bash(python3 tools/*)
---

두 사람이 같은 브랜치를 공유하고, **각자 다른 Claude Code 세션에서** 일합니다.
세션은 서로의 대화를 볼 수 없으므로, 상대가 왜 그렇게 고쳤는지는
`docs/log.md` 에만 남아 있습니다. 작업을 시작하기 전에:

1. `make sync` (= `git pull --rebase --autostash`) 를 실행합니다.
   작업 중이던 변경은 자동으로 넣었다 빼주므로 커밋하지 않아도 됩니다.
2. **`bml feed`** — 최근 커밋과 `docs/log.md` 항목을 나란히 봅니다.
   `○` 로 표시된 커밋은 기록이 없는 것입니다. 그 커밋이 무엇을 왜 고쳤는지는
   아무도 모르므로, 그 영역을 건드릴 참이면 `git show` 로 직접 읽습니다.
3. `docs/log.md` 의 최근 항목을 실제로 읽습니다 — 특히 "일부러 남긴 것" 과
   "다음 사람이 건드리면 안 되는 것".
4. `python3 tools/wiki_status.py` 로 저장소 현황을 봅니다.
5. rebase 충돌이 나면 `.claude/skills/shared-branch-workflow/SKILL.md` 의
   규칙을 따릅니다 — `docs/log.md` 는 양쪽 항목을 모두 남깁니다.

마지막에 이번 세션에서 무엇을 할지 한 문장으로 정리하고, 상대의 최근 커밋과
겹치는 부분이 있으면 지적하세요. 큰 작업이면 시작 전에 `docs/log.md` 에
`## [YYYY-MM-DD] start | <무엇을>` 을 먼저 남겨 상대가 보게 합니다.
