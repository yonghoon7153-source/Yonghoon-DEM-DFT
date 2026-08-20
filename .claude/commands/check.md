---
description: 커밋 전 필수 검사 — 테스트, 타입, 린트, 문서 정합성
allowed-tools: Bash(make:*), Bash(python3:*), Bash(npx:*), Bash(npm:*)
---

커밋하기 전에 전부 통과해야 합니다.

```bash
python3 -m pytest                       # wrdkit + api
python3 -m ruff check packages apps/api # CI 와 `bml check` 가 같은 검사를 돌린다
cd apps/web && npm run typecheck && npx vitest run && npm run lint
python3 tools/wiki_lint.py              # docs 정합성 + CLAUDE/AGENTS parity
```

실측 `.wrd` 파일이 있으면 물리 검증도 함께 돌립니다:

```bash
WRDKIT_SAMPLE=/path/to.wrd python3 -m pytest
```

실패한 항목이 있으면 **고친 뒤 다시 돌리고**, 무엇이 왜 실패했는지 한 줄로
보고하세요. 실패를 남긴 채 "대부분 통과" 라고 보고하지 않습니다.
