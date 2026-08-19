---
title: litdb 는 브랜치를 넘어 공유된다 — DEM 세션과 같은 서랍을 쓴다
date: 2026-08-19
updated: 2026-08-19
tags: [litdb, webapp, branch, workflow, dem, collision]
status: 확정 — 규약 원본은 DEM 세션 문서
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-19
verifiedBy: user
explored: false
authoredBy: agent
effort: low
claimType: procedural
evidenceScope: multi-source-primary
---

# litdb 는 브랜치를 넘어 공유된다

2026-08-19, litdb 작업 중 push 가 non-fast-forward 로 막혔다. 1저자 설명:
*"DEM section 에서 우리 webapp 이랑 litdb 를 공유하고 있거든."*

## 무슨 일이 벌어지나

**DEM 세션(`claude/stoic-knuth-NObVQ`)이 자기 브랜치에서 작업하지만
litdb 커밋은 `claude/friendly-meitner-lldvar` 로 푸시한다.** 그쪽 문서
(`docs/session_20260819_litdb_pending.md`)의 규약 원문:

> **커밋·푸시는 `claude/friendly-meitner-lldvar` 로만** (litdb 단일 서랍 규약).
> 이 리포 `litdb/` 는 동결 스냅샷.
> webapp 은 `scripts/litdb_sync.py` 가 `origin/<branch>` 를 **직접 읽으므로 푸시 = 반영**.

⇒ **우리 브랜치는 litdb 의 정본 서랍이다.** 남이 언제든 여기에 푸시한다.

## 그래서 지켜야 할 것

1. **push 전에 항상 `git fetch` → rebase.** non-fast-forward 는 사고가 아니라 정상이다.
   `--force-with-lease` 도 쓰지 말 것 — 남의 litdb 카드를 지운다.
2. **litdb 작업 전에 `git pull --rebase` 를 먼저.** 오래된 트리 위에서 큰 카드를 쓰면
   충돌 해결이 비싸진다.

## ⚠ 충돌이 나는 파일 — 셋뿐이다

| 파일 | 누가 쓰나 |
|---|---|
| `litdb/papers/<slug>.md` | 각자 자기 slug — **안 겹친다** |
| `litdb/comparison_vs_ours_DEM.md` | DEM 전용 — 안 겹친다 |
| **`litdb/INDEX.md`** | ⚠ **둘 다 쓴다** |
| **`litdb/comparison_vs_ours.md`** | ⚠ **둘 다 쓴다** (DEM 편도 몇 줄씩) |
| **`litdb/figures/_sources.json`** | ⚠ **둘 다 쓴다** (`extract_figures.py` 가 전편 색인을 다시 씀) |

⇒ 서브에이전트에 litdb 를 맡길 때는 **위 셋을 건드리지 말라고 지시하고**, 넣을 항목을
digest 끝 절에 적게 한 뒤 **사람이 병합**한다. (2026-08-19 에 실제로 그렇게 했다 —
두 에이전트를 동시에 돌리면서 하나에만 INDEX 권한을 줬다.)

## ⛔ slug 가 webapp 분류를 정한다

`webapp/data.py:literature_track(slug, type, title)` 이 **slug·type·title 을 한 문자열로
합쳐 DEM/DFT 키워드 수를 센다.** DEM 세션 문서의 경고:

> slug 에 `dryprocess` 를 넣어야 webapp 이 **dem** 으로 분류한다 (없으면 dft 로 오분류).

우리 쪽도 같은 함정이 있다 — **DFT 논문 slug 에 DEM 키워드가 섞이면 dem 으로 튄다.**
`LIT_TRACK_OVERRIDE` 로 강제할 수 있으나, **slug 를 먼저 맞추는 게 낫다.**

**검증 방법** (카드 만든 뒤 한 줄):
```python
import sys; sys.path.insert(0,'webapp')
from data import literature_track
print(literature_track("<slug>", "<type 문자열>", "<제목>"))
```
2026-08-19 실측 — 오늘 만든 넷 전부 `dft` 로 정상:
`ling2026_…_fg_cuox` · `lee2026_…_drycoating` · `deklerk2016_…` · `wu2026_…`
(`drycoating` 은 DEM 키워드가 아니라 안 튄다. `dryprocess` 였으면 튀었다.)

## 이 카드가 말하지 않는 것

- DEM 세션이 **언제** 푸시하는지 — 알 방법이 없다. 그래서 매번 fetch 한다.
- `litdb_sync.py` 가 어느 브랜치를 읽는지 이 카드에서 확인하지 않았다(그쪽 문서 인용).
- `LIT_DEM_KW` / `LIT_DFT_KW` 목록 전체를 옮겨 적지 않았다 — 바뀔 수 있으니 코드를 볼 것.
