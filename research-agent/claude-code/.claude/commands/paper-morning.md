---
description: 논문 에이전트 MORNING 절차 — 디제스트 생성·문장 다듬기·발송·commit
allowed-tools: Bash(ra:*), Bash(git:*), Read, Edit
---
research-agent MORNING 절차를 수행하라. $ARGUMENTS

1. `ra morning --dry-run` → `vault/Digests/<오늘 KST 날짜>.md` 생성.
2. 파일을 열어 prompts/style_guide.md 기준으로 **문장만** 다듬는다. 수치·DOI·[[위키링크]]·References 목록은 그대로 둔다.
3. SMTP 자격증명이 있으면 `ra morning` 을 다시 실행해 발송·DB 기록. 없으면 발송을 건너뛰고 "미발송"이라고 보고한다 (Cowork 클라우드 작업이 대신 보낼 수 있다).
4. `git add -A data vault && git commit -m "ra: morning $(date +%F)"`.
5. 보고: 제목 줄, A/B/C 편수, 첫 번째 논문 한 줄 요약.
