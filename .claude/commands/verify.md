---
description: 실측 .wrd 파일로 물리 검증을 돌립니다
argument-hint: [.wrd 파일 경로]
allowed-tools: Bash(python3:*), Bash(ls:*), Read
---

숫자를 만드는 코드는 자기 자신과의 일관성이 아니라 **물리와의 일치**로
검증합니다. `.claude/skills/verifying-against-a-real-file/SKILL.md` 참조.

파일 경로: `$ARGUMENTS` (없으면 `data/uploads/` 에서 찾습니다)

```bash
PYTHONPATH=packages/wrdkit/src python3 -m wrdkit.cli info <파일>
WRDKIT_SAMPLE=<파일> python3 -m pytest
```

확인할 것:

1. `trailing_bytes == 0` — 파일을 남김없이 소비했는가
2. 전류 적분값과 보고된 방전용량이 2% 안에서 일치하는가
3. 전압이 스케줄의 컷오프를 벗어나지 않는가
4. formation 이후 쿨롱효율이 100% 를 넘지 않는가
5. 비용량이 50–400 mAh/g 안에 들어오는가
6. 시간이 단조 증가하는가

어긋나는 항목이 있으면 **어떤 가정이 틀렸는지**까지 짚어서 보고하세요.
"테스트가 실패했다" 가 아니라 "질량이 틀렸거나 UnitCoulomb 해석이 틀렸다".
