---
description: 저장소 현황 스냅샷
allowed-tools: Bash(python3:*), Bash(git:*), Bash(ls:*)
---

```bash
python3 tools/wiki_status.py
```

여기에 더해:

- `data/uploads/` 에 파일이 몇 개인지, DB 에 셀이 몇 개인지
- 미커밋 변경과 업스트림 대비 ahead/behind
- 미해결 TODO 나 `docs/log.md` 의 `start` 항목 중 마무리되지 않은 것

behind 가 0 이 아니면 `make sync` 를 먼저 하라고 알려 주세요.
