---
description: kb 위키 lint + index 신선도 검사 (0 errors 될 때까지)
---

1. `python3 tools/kb_wiki.py index` 로 kb/index.md 재생성.
2. `python3 tools/kb_wiki.py lint` 실행.
3. **errors 가 있으면 고친다** — 규칙 해석이 필요하면 kb/SCHEMA.md 를 먼저 읽는다.
   경로 깨짐 error 는 (a) 실제 파일 경로로 고치거나 (b) 존재하지 않는 예시 경로면
   글롭/서버경로 표기로 바꿔 검사 대상에서 뺀다. 레거시 warning 은 소급하지 않는다.
4. 0 errors 확인 후, 바뀐 파일이 있으면 `kb:` prefix 로 커밋한다.
