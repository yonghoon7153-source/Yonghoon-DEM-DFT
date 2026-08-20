# Wiki Schema

## Domain
Yonghoon-DEM-DFT 모노레포의 mothership LLM Wiki. 배터리 열화 연구(degradation-degeneracy: PyBaMM 합성 truth 로 LLI/LAM fitting degeneracy 판별)와 DEM/MPM 계열 프로젝트의 지식 — 연구 개념, 검증·재현성 설계 원칙, 게이트 리뷰 프로세스, 실행 환경(V100·컨테이너·Windows) 절차 — 을 등록·연결·재사용한다. 개별 프로젝트는 satellite(모노레포 하위 폴더 또는 타 브랜치)로 분리해 entity 로 참조한다.

## Conventions
- File names: lowercase, hyphens, no spaces.
- Raw source files live under `raw/` and are treated as immutable.
- Wiki pages live under `concepts/`, `entities/`, `comparisons/`, `queries/`, `guides/`, `questions/`, `syntheses/`.
- Every wiki page starts with YAML frontmatter (below).
- Use `[[wikilinks]]` for internal links; each page should target at least 2 related pages.
- Every new page must be listed in `index.md`. Every meaningful action goes to `log.md`.
- When updating a page, bump `updated`.
- 새 페이지는 `python3 wiki/tools/new-page.py <type> <slug>` 스캐폴더로 만든다.
- Lint: `python3 wiki/tools/lint.py` (repo root 기준) · Status: `python3 wiki/tools/status.py`
- Claude Code 커맨드 (repo root `.claude/commands/`, 연구 파이프라인 명령과 충돌 방지 위해 `wiki-` 접두): /wiki-ingest /wiki-inbox /wiki-query /wiki-verify /wiki-lint /wiki-status /wiki-wrap

### Mothership 특칙 (이 모노레포 적응판)
- Satellite 프로젝트는 `entities/`에 1 페이지로 등록하고, 상태가 바뀌면 해당 entity의 `updated`와 상태 섹션을 갱신한다. 등록 절차는 `guides/new-project-kickoff.md`.
- Cross-vault 참조(satellite 내부 파일 등)는 `[[wikilink]]` 대신 **repo-root 상대 경로**로 표기한다 (예: `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`). 원본 킷은 절대 경로였지만, 이 위키는 satellite 과 **같은 git repo** 안에 있고 컨테이너·V100·Windows 로 clone 경로가 달라 상대 경로가 유일하게 이식 가능하다. 내용 복사는 금지, 참조만 한다 (living reference).
- 타 브랜치에서 운영되는 satellite(MPM/DEM 계열)는 entity 에 `브랜치:` 를 명시하고, 그 브랜치의 파일은 이 브랜치에서 안 보일 수 있음을 적는다.
- 설계 세션에서 나온 결정은 `raw/transcripts/`에 세션 기록으로 남겨 페이지의 source로 삼는다.
- **연구 파이프라인과의 경계**: degradation-degeneracy 의 인용 게이트(서명·validator·smoke)는 `src/tools/configs/scripts` 만 code identity 로 본다. `wiki/` 는 그 밖이므로 위키 커밋이 `source_digest` 를 바꾸지 않는다 — 위키 작업이 게이트 리뷰 대상 커밋을 오염시키지 않는다. 반대로 위키는 연구 결과 수치의 **정본이 아니다** — 수치의 정본은 언제나 artifact + `docs/RESULTS*.md` 이고 위키는 지도다.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: concept | entity | comparison | query | guide | research-question | synthesis
tags: []
sources: [raw/articles/source-name.md]
confidence: high | medium | low
explored: false
verificationStatus: unverified | verified | disputed
verifiedAt: YYYY-MM-DD            # verified 일 때만
verifiedBy: agent | human | both  # verified 일 때만
model: claude-fable-5             # 에이전트 작성 페이지만 — 쓴 모델 ID (사람 작성이면 생략)
effort: low | medium | high | max # model 과 세트 — 추론 강도
claimType: definition | empirical | theoretical | historical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
---
```

타입별 추가 키:
- `research-question` (`questions/`): `status: open | active | answered | abandoned`, `feedsInto:` (답이 흘러갈 곳 — 가설/논문/결정)
- `synthesis` (`syntheses/`): `targetVenue:` (논지를 쓸 곳)

### 세 가지 직교 품질 축
| 필드 | 추적 대상 | 규칙 |
|---|---|---|
| `confidence` | 증거 강도 | high 로 올릴 때 반대해석/데이터 공백 1줄 기록 |
| `verificationStatus` | source 대조 검증 | 새 페이지 `unverified`, 검증 후 `verified`, 충돌은 양쪽 `disputed` |
| `explored` | 사람이 읽었는가 | **사람만** `true` 로 바꾼다 |

### Provenance (v1.8 채택, 2026-08-06)
- 에이전트가 만들거나 크게 고친 페이지는 `model`/`effort` 를 기록한다. 사람 작성이면 생략. 기존 페이지 소급 없음 — 새 페이지부터.
- `description` 등 자유 텍스트 frontmatter 값에 콜론·괄호가 들어가면 따옴표로 감싼다 (YAML 파싱 보호). lint 가 검사한다.
- `claimType`(지배적 주장 유형)과 `evidenceScope`(근거 폭)도 새 페이지부터 기록. **`evidenceScope: single-source` 페이지는 `confidence: high` 금지** — 근거 폭이 confidence 상한을 정한다 (lint warning).

### 페이지 3분법 (v1.9 채택)
- **위키 페이지** (concept/entity/comparison/query/guide) = 배운 것의 기록.
- **research-question** = 답이 안 나온, 계속 돌아오는 질문의 추적. 본문: 질문 1문장 → 왜 중요한가 → 가설 → Evidence For / Against → Status Log(날짜별). `/ingest` 때마다 열린 카드(status: open|active)에 새 자료가 근거를 주는지 확인해 축적한다.
- **synthesis** = 논지 하나의 방어. 본문: Thesis 1문장 → Argument → Counter-arguments(반론 **보존**, 삭제 금지) → Gap(빈 근거). 답이 모인 research-question 이 synthesis 로 승격될 수 있다.

### Paper Ingest Mode (v1.10 채택 — opt-in)
논문의 수치·정의·인용문을 verbatim 재사용 가능한 atom 으로 분해하는 모드. **자동 실행 금지**:
- 에이전트가 필요하다고 판단하면 (프로젝트가 그 논문의 수치/정의를 반복 참조할 때) 사용자에게 **제안하고 승인 후** 실행한다.
- 논문 전체가 아니라 **필요한 좌표만** 부분 atomization 한다.
- 절차: `guides/paper-ingest-mode.md`.

## Raw Frontmatter
```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body after frontmatter, leading blank lines stripped>
---
```

## Tag Taxonomy
도메인에 맞게 채워 나간다. 규칙: 소문자, 하이픈, 페이지 3개 이상 모일 주제만 태그로 승격.

시드 (mothership 공통):
- project: 진행 중인 프로젝트
- satellite: 별도 폴더/저장소로 운영되는 satellite 참조
- research: 연구 내용 일반
- design: 설계 결정과 아키텍처 기록
- tooling: 개발 환경, 도구, API 설정
- wiki: LLM Wiki 운영 자체

시드 (이 도메인):
- battery: 배터리 전기화학 일반
- degradation: 열화 모드 (LLI/LAM) 와 그 추정
- pybamm: PyBaMM 모델링·solver
- provenance: 재현성·서명·검증 설계
- gate-review: 적대적 게이트 리뷰 프로세스
- dem-mpm: DEM/MPM 계열 시뮬레이션 (타 브랜치 satellite)

## Page Thresholds
- Create a page when a concept is central to a source or recurs across sources.
- Do not create pages for passing mentions.
- Split pages over ~200 lines (guides 제외).

## Update Policy
새 정보가 기존 내용과 충돌하면: 날짜/출처 품질 확인 → 양쪽 입장 기록(덮어쓰기 금지) → confidence 하향 또는 disputed → lint 에서 표면화.

## Git
커밋 prefix 는 log action 과 동일하되 이 모노레포 컨벤션에 맞춰 scope 를 붙인다: `ingest(wiki):` `update(wiki):` `create(wiki):` `lint(wiki):` `verify(wiki):`.
push 는 항상 **루트 `CLAUDE.md` 하드룰 1이 지정한 작업 브랜치**로만 한다. 브랜치 이름을 여기 적지 않는다 — 2026-08-20 에 이 위키 5개 파일이 이미 대체된 브랜치 이름을 붙들고 있었다 (lint 검사 16).
