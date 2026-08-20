---
description: 위키 카운트, 검증 커버리지, 학습 진도 스냅샷
---

> 이 위키는 repo root `wiki/` 하위다 (킷 원본과 배치가 다름 — `wiki/README.md` 참조). 아래 절차의 모든 경로는 repo root 기준이다.

이 LLM Wiki 의 현재 상태를 보고한다.

1. `python3 wiki/tools/status.py` 를 실행한다.
2. 출력을 요약해 보고한다: 페이지 수(유형별), confidence/verificationStatus/explored 분포, verify 대기 큐, 최근 log.
3. 마지막에 **다음 행동 1가지**를 추천한다 — 예: "unverified 페이지 X 를 /wiki-verify", "열린 research-question 카드에 새 근거 반영", "N일째 ingest 없음 — 새 자료 하나 넣기".
