---
description: kb 새 문서 스캐폴드 (frontmatter + 타입별 필수 절)
argument-hint: <dir> <slug>  예) questions li3nd_barrier · syntheses xu2026_rebuttal · concepts mto
---

1. kb/SCHEMA.md 를 읽는다 (frontmatter 스펙 + 문서 3분법).
2. `python3 tools/kb_wiki.py new $ARGUMENTS` 로 스캐폴드 생성 —
   `questions` 는 research-question 절(왜 중요한가/Evidence For/Against/결정 실험/Status Log),
   `syntheses` 는 Thesis/Counter-arguments/Gap 절이 자동으로 들어간다.
3. 본문을 채운다: 관련 repo 경로 ≥2개 인용 (lint 가 존재 검사), 근거가 하나뿐이면
   confidence 는 medium 이하, `explored: false` 는 그대로 둔다 (사람 전용).
4. `python3 tools/kb_wiki.py index` 재생성 → `lint` 0 errors → `kb:` prefix 커밋.
