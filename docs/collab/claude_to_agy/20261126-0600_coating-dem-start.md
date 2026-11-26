# 코팅 과정 DEM — 가능성 메모 시작 (Claude → agy 실무 · 2026-11-26)

[믹서 · 코팅 활물질] · 1저자 11-26 *"코팅 관련해서는 지금 … 안티그래비티한테"* = 주인 agy 실무 (relay 스킬 §3-1 · 트랙마다 주인 하나) · 서두르지 않음 (1저자 11-26 *"믹서랑 함께 천천히"*) · 개발 자료 · 결과 0 건 · 이 메모가 agy 실무의 첫 품질 확인을 겸한다.

붙일 문안 (1저자 · agy 실무 창 "DEM 실무" · relay 스킬 §5-1 공통 다음에):

```
[1저자 11-26] 할 일 = 코팅 과정 DEM (논문 밖 · 구현 시도) 의 가능성 메모. 문서만 쓴다 — 계산 · 서버 실행 없음.
- 근거: docs/collab/claude_to_codex/20261123-2330_mixer-q1-q4-direction.md 의 표 4 번 줄 · docs/reviews/mixer_direction_feedback_20261123.md (11-23 Q3) · CLAUDE.md 용훈 포메이션 Ⓒ 줄.
- 메모 = docs/reviews/coating_dem_feasibility_memo_<YYYYMMDD>.md — 넣을 것:
  1. 먼저 볼 장치 꼴 (메카노퓨전 · 텀블러 · 칼날 가운데 하나) 과 고른 이유
  2. 규모 어림 (입자 수 · Δt · 1 초를 계산하는 데 드는 시간 · 우리 기계 기준) — 산술은 [추정] 표지
  3. 충돌 → SE 파쇄 → 부착 → 소성 가운데 지금 우리 DEM (LIGGGHTS 덱) 으로 바로 되는 것 / 안 되는 것
  4. 피복률로 볼 지표 (게스트 피복률 · 충돌 에너지 분포 등)
  5. 첫 샌드박스 크기와 끝 기준
- 문헌 값 · 서지는 litdb 정본 카드 (claude/friendly-meitner-lldvar 가지의 litdb/papers/) 에서만 가져온다. 카드가 없으면 [미확인] 으로 두고 짓지 않는다.
- 끝나면 Claude 인계 ZIP (반입할 커밋의 패치 · stable patch-id · 바꾼 파일 사본 · sha256 목록 · 쪽지 docs/collab/agy_to_claude/<UTC>_coating-dem-memo.md) 을 만들어 1저자에게 준다.
```

바탕: 11-23 밤 1저자 결정 Q3 (`docs/reviews/mixer_direction_feedback_20261123.md`) · 규모 어림 선례 (`docs/handoff_return_to_stoic_knuth_20261124.md` 의 chen2004 줄 · 카드 산술) · 이전 Codex 쪽지 (`docs/collab/claude_to_codex/20261126-1022_coating-dem-status.md` — 주인이 바뀌어 대체됨).
