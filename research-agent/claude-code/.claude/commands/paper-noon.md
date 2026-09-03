---
description: 논문 에이전트 NOON 절차 — alert 수집·triage·심층분석·DB·vault·litdb·commit
allowed-tools: Bash(ra:*), Bash(git:*), Bash(python:*), Read, Write, Edit, Agent, WebFetch, WebSearch
---
research-agent NOON 절차를 수행하라. $ARGUMENTS

1. `ra noon` 실행 (IMAP 자격증명이 없으면 `ra noon --no-imap`). 로그의 new/queued 수를 확인.
2. `data/analysis/pending/*.json` 각각에 대해 paper-analyst 서브에이전트를 병렬로 띄워 `analysis` 필드를 채우게 한다 (5편 초과 시 5개씩).
   초록이 비어 있으면 서브에이전트가 DOI 페이지를 WebFetch 해 초록을 확보하고 evidence_level을 정직하게 기록한다.
3. `ra analyze --import-dir data/analysis/pending` → 검증 오류가 있으면 해당 파일만 고쳐 재실행.
4. `ra vault && ra litdb`, 그리고 `git add -A data vault && git commit -m "ra: noon $(date +%F)"`. config/agent.yaml의 git.push가 true면 push.
5. 마지막에 `ra status` 출력과 함께 Tier A 논문 제목·한 줄 요약을 보고한다. 새 논문이 0편이면 그렇게만 말하고 끝낸다.
