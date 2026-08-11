# kb/SCHEMA.md — kb 위키 규율 (규칙 원본)

> 2026-08-11 채택. Karpathy LLM Wiki 패턴(구요한 llm-wiki-kit 260730)을 이 repo 에
> 번안한 것 — 무엇을 채택/번안/기각했는지는 `kb/methodology/llm_wiki_adoption_2026_08_11.md`.
> 에이전트는 kb 문서를 만들거나 크게 고치기 전에 이 파일을 읽는다.

## 레이어 (기존 구조 유지 — 폴더 재구성 없음)

| 레이어 | 위치 | 규칙 |
|---|---|---|
| **数値 정본** | `db/properties/` `db/structures/` | 숫자의 유일한 권위. 철회는 `retracted:true` 블록 — 삭제 금지 |
| **불변 원본** | `runs/` (납품·실행 산출물) · litdb PDF(repo 밖) | **수정 금지.** 해석은 kb/litdb 문서에서만 |
| **위키(해석)** | `kb/*/` · `litdb/` · `docs/` | 이 스키마의 관할. 숫자는 **경로 인용**으로만 (living reference — 복사 금지) |

kb 디렉터리 ↔ 타입: `concepts`(개념) `physics`(물리 노트) `methodology`(방법·결정 기록)
`results`(우리 결과 해석) `reviews`(리뷰 왕복) `reports`(대외 문서) `projects`(프로젝트)
`questions`(research-question) `syntheses`(논지 방어) `platforms` `descriptors` `papers`
`literature_db`(구세대 — 신규 금지, litdb/ 로) `seminars` `elements`(생성물) `templates`.

## Frontmatter

**새 문서부터 필수. 기존 199개 소급 없음** (lint 는 frontmatter 있는 문서만 깊이 검사).
생성: `python3 tools/kb_wiki.py new <dir> <slug>`.

```yaml
---
title: 제목
date: YYYY-MM-DD          # 생성일
updated: YYYY-MM-DD       # 마지막 실질 수정 (고치면 bump)
tags: [x, y]
status: 자유문             # 예: 진행 · 회신 대기 · 확정 · 철회
confidence: high | medium | low
verificationStatus: unverified | verified | disputed | retracted
verifiedAt: YYYY-MM-DD    # verified 일 때만
verifiedBy: codex | self | both | human   # verified 일 때만
explored: false           # ⚠ 사람만 true 로 바꾼다 (사용자가 읽었는가)
authoredBy: agent | human
effort: low | medium | high | max         # agent 작성일 때
claimType: definition | empirical | theoretical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
---
```

### 품질 3축은 직교다
- `confidence` = 증거 강도. **high 로 올리면 본문에 반대해석/한계 1줄** 을 남긴다.
- `verificationStatus` = 대조 검증. 우리 문화 그대로: Codex 교차검증 = `verifiedBy: codex`,
  자체 적대 리뷰 = `self`, 둘 다 = `both`. 충돌하면 양쪽 다 `disputed`, 반증되면 `retracted`
  (본문 보존 + 반증 근거 추가 — 오늘 §11 BVSE 철회가 표준례).
- `explored` = **사용자가 읽었는가.** 에이전트는 절대 true 로 바꾸지 않는다.

### 근거 폭이 confidence 의 상한이다
`evidenceScope: single-source` 문서는 `confidence: high` 금지 (lint 경고).
근거가 하나뿐이면 아무리 그럴듯해도 medium 이 상한이다.

## 문서 3분법

- **위키 문서** (concepts/results/methodology/…) = 배운 것·결정한 것의 기록.
- **research-question** (`kb/questions/`) = 답이 안 난, 계속 돌아오는 질문의 추적 카드.
  frontmatter 에 `status: open | active | answered | abandoned` + `feedsInto:` (답이 흘러갈 곳).
  본문 필수 절: 질문 1문장 → **왜 중요한가** → 가설 → **Evidence For** / **Evidence Against**
  → **결정 실험** (무엇이 결판내나) → **Status Log** (날짜별 append).
  새 자료·리뷰가 올 때마다 열린 카드(open|active)에 근거를 축적한다.
  ⚠ `kb/open_items.md` 는 **원장(ledger)** 으로 유지 — 큰 항목이 카드로 승격되면 상호 링크.
- **synthesis** (`kb/syntheses/`) = 논지 하나의 방어 카드. `targetVenue:` (논지를 쓸 곳).
  본문 필수 절: **Thesis** 1문장 → Argument → **Counter-arguments** (반론 **보존** — 삭제 금지)
  → **Gap** (빈 근거). 근거가 모인 research-question 이 synthesis 로 승격될 수 있다.

## 링크 규칙 — [[wikilink]] 대신 repo-상대경로

경로 인용이 이 repo 의 링크다: `db/properties/x.json` · `tools/y.py` · `kb/z.md`.
lint 가 **존재를 검사**한다 (rename 이 조용히 깨지는 것 방지). 서버 절대경로(`/data/...`)와
글롭(`*`)은 검사 대상 아님. 문서마다 관련 경로 2개 이상을 인용한다.
**존재하지 않는 경로를 일부러 기록**할 때(리뷰어 오인용의 정정, 커밋 안 된 구세대 스크립트
목록, 미생성 예정 산출물)는 그 줄에 `<!-- lint-skip-path -->` 를 붙인다 — 남용 금지,
실존 파일 인용에는 절대 붙이지 않는다.

## index / lint / 커밋

- `kb/index.md` 는 **`python3 tools/kb_wiki.py index` 가 생성**한다 — 손으로 고치지 않는다.
  문서를 만들거나 지우면 재생성. lint 가 신선도를 검사한다.
- 마무리는 `python3 tools/kb_wiki.py lint` **0 errors** (경고는 허용 — 레거시 소급 안 함).
- 커밋 prefix 는 기존 관행 유지 (`kb:` `db:` `sei:` …). 별도 log.md 없음 — git 이 로그다.

## litdb 와의 관계

문헌은 `litdb/` 가 정본 (digest + INDEX.md + comparison_vs_ours.md + figures/, CLAUDE.md §litdb).
`kb/literature_db/` 와 `db/literature/` 는 구세대 — **신규 작성 금지**, 필요하면 litdb 로 승격.
문헌 수치는 소환값 — 우리 db 절대값과 같은 표에 놓지 않는다 (방법 명시 없이 이식 금지).

## Update Policy (kit 그대로 채택)

새 정보가 기존 내용과 충돌하면: 날짜·출처 품질 확인 → **양쪽 입장 기록** (덮어쓰기 금지) →
confidence 하향 또는 `disputed` → lint 가 표면화. 철회는 원문 보존 + 반증 병기
(이 repo 의 superseded/retracted 관행과 동일).
