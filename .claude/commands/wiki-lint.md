---
description: 위키 건강 점검 (read-only 보고)
---

1. `python3 wiki/tools/lint.py` 를 실행한다.
2. ERRORS(깨진 링크·index 불일치·모델 ID·source 경로·single-source+high)는 원인과
   수정 방법을, warn(고아·stale·링크<2)은 조치 필요 여부를 제시한다.
3. `python3 wiki/tools/status.py` 로 unverified/explored:false backlog 를 요약하고
   다음 검증 대상 1~2개를 추천한다.

Read-only 원칙: 보고와 제안까지만. 수정은 승인 후 — 수정하면 log.md 에 기록.
