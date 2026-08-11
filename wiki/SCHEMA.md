# Wiki Schema — Yonghoon-DEM-DFT 지식 내비게이션

## Domain
DEM↔MPM 상보 시뮬레이션 프레임(압밀·수송·전기화학·ML)의 **반복 참조 지식**을
항목화한 지도.  정본 서술은 여전히 루트 `CLAUDE.md` 와 `docs/` — 이 위키는
그 위의 **요약+포인터 층**이다 (세션이 "X 가 뭐더라" 를 찾을 때 CLAUDE.md 전체를
뒤지지 않고 여기서 시작한다 = progressive disclosure).

> 출처 계보: Karpathy LLM-wiki 패턴 → 구요한(CMD Space) llm-wiki-kit v1.7 →
> 이 리포 규약에 맞게 개조 (개조 내역은 [[llm-wiki-kit-origin]]).

## 3-Layer — 우리 리포의 대응 (킷과 다른 점 ★)
| Layer | 킷 원형 | ★ 우리 리포 |
|---|---|---|
| 1 불변 증거 | `raw/` 폴더 | **이미 있다**: `docs/data/`(측정 CSV·JSON) · litdb 정본 · `docs/reviews/findings.json` · git 이력.  `wiki/raw/` 는 litdb 소관이 아닌 외부 자료(강연 전사 등)에만 예외적으로 쓴다 |
| 2 컴파일된 위키 | 페이지 7종 | `wiki/{concepts,entities,comparisons,queries,guides,questions,syntheses}/` |
| 3 규칙 | SCHEMA.md | 이 파일 (+ 루트 `CLAUDE.md` 가 상위 규범) |

## ★ 경계 규칙 (우리 환경 특칙 — 위반 시 lint/리뷰에서 잡는다)
1. **논문은 litdb 정본 소관.**  논문 digest 는 `origin/claude/friendly-meitner-lldvar`
   의 `litdb/` 에만 만든다 (루트 CLAUDE.md litdb 규칙).  위키는 카드를 **참조**하는
   concept/comparison 만 만들고, 킷의 Paper Ingest Mode 는 **채택하지 않는다**.
2. **모델 ID 금지.**  푸시되는 산출물에 모델 식별자를 적지 않는 리포 규칙에 따라
   킷의 `model:`/`effort:` provenance 필드를 **폐기**하고 `author: agent|human|both`
   로 대체한다.  lint 가 모델 ID 패턴을 **오류**로 잡는다.
3. **수치는 옮겨 적는 순간 출처를 단다.**  페이지 본문의 모든 수치는 `sources` 의
   파일에 실재해야 한다 (lint 는 경로 존재만, 대조는 `/wiki-verify`).
4. **CLAUDE.md 를 대체하지 않는다.**  페이지는 요약+포인터.  정본 서술과 충돌하면
   정본이 이긴다 — 페이지를 고치고 `updated` bump.

## Conventions
- 파일명: lowercase-hyphens.  새 페이지는 `python3 wiki/tools/new_page.py <type> <slug>`.
- 내부 링크 `[[wikilink]]` 페이지당 **2개 이상**.  리포 파일은 상대경로로
  (`docs/...md`, `scripts/foo.py:123`), litdb 정본 카드는 `litdb-canon:<card-slug>`.
- 새 페이지는 `wiki/index.md` 등록 + `wiki/log.md` append (`## [YYYY-MM-DD] action | subject`).
- 페이지를 고치면 `updated` bump.  마무리는 `python3 wiki/tools/lint.py` 0 errors.
- 커밋 prefix: `wiki: <action> — <subject>` (action = ingest|create|update|verify|lint).

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query | guide | research-question | synthesis
tags: []
sources: [docs/foo.md, scripts/bar.py, litdb-canon:card-slug, https://...]
confidence: high | medium | low
explored: false
verificationStatus: unverified | verified | disputed
verifiedAt: YYYY-MM-DD            # verified 일 때만
verifiedBy: agent | human | both  # verified 일 때만
author: agent | human | both      # ★ 킷의 model/effort 대체 (모델 ID 금지)
claimType: definition | empirical | theoretical | historical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
anchored: anchored | assumed | mixed | n-a   # ★ §F1 축 — 수치가 실측/문헌 앵커인가
scope: absolute | relative-only | n-a        # ★ 등급 A/B 축 — 절대값 인용 가능한가
---
```
타입별 추가 키:
- `research-question` (`questions/`): `status: open | active | answered | abandoned`, `feedsInto:`
- `synthesis` (`syntheses/`): `targetVenue:`

### 품질 축 (직교 5축 — 킷 3축 + 우리 2축)
| 필드 | 추적 대상 | 규칙 |
|---|---|---|
| `confidence` | 증거 강도 | `evidenceScope: single-source` 면 `high` **금지** (lint 오류) |
| `verificationStatus` | source 대조 검증 | 새 페이지 `unverified` → `/wiki-verify` 후 `verified`, 충돌은 양쪽 `disputed` |
| `explored` | **사람이** 읽었는가 | 사람만 `true` 로 바꾼다 — 에이전트 절대 금지 |
| `anchored` | §F1 — 실측/문헌 앵커 여부 | `assumed` 페이지의 수치는 인용 전 재확인 |
| `scope` | 등급 A/B — 절대 vs 상대 | `relative-only` 수치는 절대값으로 인용 금지 (준정적 위반 런 등) |

### 페이지 3분법
- **위키 페이지** (concept/entity/comparison/query/guide) = 배운 것의 기록.
- **research-question** = 답이 안 나온 질문의 추적.  본문: 질문 1문장 → 왜 중요한가 →
  가설 → Evidence For/Against → Status Log(날짜별).  자료가 들어올 때마다 열린
  카드(open|active)에 근거를 축적한다.  `docs/reviews/findings.json` 의 open 항목과
  1:1 일 필요는 없지만, 겹치면 페이지가 ledger 항목을 sources 로 가리킨다.
- **synthesis** = 논지 하나의 방어.  Thesis 1문장 → Argument → Counter-arguments
  (반론 **보존**, 삭제 금지 — 우리 문화의 "정정 기록 보존" 과 같은 원칙) → Gap.

## Update Policy
새 정보가 기존 페이지와 충돌하면: 날짜/출처 확인 → 양쪽 입장 기록(덮어쓰기 금지) →
confidence 하향 또는 양쪽 `disputed` → lint 가 표면화.  정본(CLAUDE.md·docs)이
정정되면 (예: 2026-08-11 "DEM=TRANSPORT 과단순" 정정) 페이지도 같은 날 갱신한다.

## Tag Taxonomy (3페이지 이상 모일 주제만 승격)
시드: `pipeline` `epistemology` `calibration` `transport` `mpm` `dem` `electrochem`
`review` `environment` `ml` `wiki` `additive`

## Page Thresholds
- 출처에서 중심적이거나 **여러 세션에 걸쳐 반복 등장**하는 개념만 페이지로.
- 스치는 언급은 페이지 금지.  ~200줄 넘으면 분할 (guides 제외) — 긴 서술은
  docs/ 에 두고 여기서는 포인터.
