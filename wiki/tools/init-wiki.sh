#!/bin/bash
# Scaffold a fresh LLM Wiki for a new project, copying the generic harness
# (tools, slash commands, hooks, CI) from this wiki — content stays behind.
#
# Usage: tools/init-wiki.sh <target-dir> ["domain one-liner"] [--no-git]
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${1:?usage: init-wiki.sh <target-dir> [\"domain one-liner\"] [--no-git]}"
DOMAIN="${2:-이 저장소의 도메인을 한 문장으로 적는다 (무엇에 관한 자료를 모아 무엇에 재사용하는가).}"
NO_GIT=false
[[ "${2:-}" == "--no-git" || "${3:-}" == "--no-git" ]] && NO_GIT=true
[[ "${2:-}" == "--no-git" ]] && DOMAIN="이 저장소의 도메인을 한 문장으로 적는다 (무엇에 관한 자료를 모아 무엇에 재사용하는가)."
TODAY="$(date +%F)"

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null)" ]; then
  echo "ERROR: $TARGET already exists and is not empty" >&2; exit 1
fi

mkdir -p "$TARGET"/{raw/{articles,papers,transcripts,repositories},concepts,entities,comparisons,queries,guides,questions,syntheses,tools,inbox,.claude/{commands,hooks},.github/workflows}
# keep empty dirs under git (git tracks files only — a clone would lose them)
touch "$TARGET"/{concepts,entities,comparisons,queries,guides,questions,syntheses}/.gitkeep \
      "$TARGET"/raw/{articles,papers,transcripts,repositories}/.gitkeep

# --- copy the generic harness verbatim ---
cp "$SRC"/tools/{lint.py,status.py,new-page.py,init-wiki.sh} "$TARGET/tools/"
cp "$SRC"/.claude/commands/*.md "$TARGET/.claude/commands/"
cp "$SRC"/.claude/hooks/*.sh "$TARGET/.claude/hooks/"
cp "$SRC"/.claude/settings.json "$TARGET/.claude/"
cp "$SRC"/.github/workflows/lint.yml "$TARGET/.github/workflows/" 2>/dev/null || true
cp "$SRC"/inbox/README.md "$TARGET/inbox/"
chmod +x "$TARGET"/tools/*.py "$TARGET"/tools/*.sh "$TARGET"/.claude/hooks/*.sh

# --- generate project files ---
cat > "$TARGET/SCHEMA.md" <<EOF
# Wiki Schema

## Domain
$DOMAIN

## Conventions
- File names: lowercase, hyphens, no spaces.
- Raw source files live under \`raw/\` and are treated as immutable.
- Wiki pages live under \`concepts/\`, \`entities/\`, \`comparisons/\`, \`queries/\`, \`guides/\`, \`questions/\`, \`syntheses/\`.
- Every wiki page starts with YAML frontmatter (below).
- Use \`[[wikilinks]]\` for internal links; each page should target at least 2 related pages.
- Every new page must be listed in \`index.md\`. Every meaningful action goes to \`log.md\`.
- When updating a page, bump \`updated\`.
- 새 페이지는 \`python3 tools/new-page.py <type> <slug>\` 스캐폴더로 만든다.
- Lint: \`python3 tools/lint.py\` · Status: \`python3 tools/status.py\`
- Claude Code 커맨드: /ingest /inbox /query /verify /lint /status /wrap

## Frontmatter
\`\`\`yaml
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
model: claude-model-id            # 에이전트 작성 페이지만 (사람 작성이면 생략)
effort: low | medium | high | max # model 과 세트
claimType: definition | empirical | theoretical | historical | prescriptive | interpretive | mixed
evidenceScope: single-source | multi-source-primary | multi-source-mixed | synthesis-only | user-original
---
\`\`\`

타입별 추가 키: \`research-question\`(\`questions/\`) — \`status: open | active | answered | abandoned\`, \`feedsInto:\` · \`synthesis\`(\`syntheses/\`) — \`targetVenue:\`

### 세 가지 직교 품질 축
| 필드 | 추적 대상 | 규칙 |
|---|---|---|
| \`confidence\` | 증거 강도 | high 로 올릴 때 반대해석/데이터 공백 1줄 기록 |
| \`verificationStatus\` | source 대조 검증 | 새 페이지 \`unverified\`, 검증 후 \`verified\`, 충돌은 양쪽 \`disputed\` |
| \`explored\` | 사람이 읽었는가 | **사람만** \`true\` 로 바꾼다 |

### Provenance
- 에이전트 작성/대폭 수정 페이지는 \`model\`/\`effort\` 기록. \`claimType\`/\`evidenceScope\` 도 채운다 — **\`single-source\` 면 \`confidence: high\` 금지** (lint warning).
- 자유 텍스트 frontmatter 값(\`description\` 등)에 콜론·괄호가 들어가면 따옴표로 감싼다.

### 페이지 3분법
위키 페이지 = 배운 것 기록 · \`questions/\` research-question = 열린 질문 추적 (/ingest 마다 근거 라우팅) · \`syntheses/\` synthesis = 논지 방어 (반론 보존).

### Paper Ingest Mode (opt-in)
논문 수치·정의를 verbatim atom 으로 분해하는 모드 — **사용자 승인 없이 실행 금지**, 필요한 좌표만 부분 atomization. 절차는 원본 위키의 \`guides/paper-ingest-mode.md\` 참고.

## Raw Frontmatter
\`\`\`yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body after frontmatter, leading blank lines stripped>
---
\`\`\`

## Tag Taxonomy
도메인에 맞게 채워 나간다. 규칙: 소문자, 하이픈, 페이지 3개 이상 모일 주제만 태그로 승격.

## Page Thresholds
- Create a page when a concept is central to a source or recurs across sources.
- Do not create pages for passing mentions.
- Split pages over ~200 lines (guides 제외).

## Update Policy
새 정보가 기존 내용과 충돌하면: 날짜/출처 품질 확인 → 양쪽 입장 기록(덮어쓰기 금지) → confidence 하향 또는 disputed → lint 에서 표면화.

## Git
커밋 prefix 는 log action 과 동일: \`ingest:\` \`update:\` \`create:\` \`lint:\` \`verify:\`.
EOF

cat > "$TARGET/CLAUDE.md" <<'EOF'
# CLAUDE.md — LLM Wiki Harness

이 폴더는 **Karpathy LLM Wiki 패턴을 구현한 위키**다. 너(에이전트)는 이 위키의 컴파일러이자 사서다. 규칙의 원본은 `SCHEMA.md` — 위키 콘텐츠를 만들거나 고치기 전에 반드시 읽는다.

## Essential Rules (요약 — 상세는 SCHEMA.md)

1. **3-Layer 분리**: `raw/` = 불변 원본 (절대 수정 금지) · `concepts|entities|comparisons|queries|guides|questions|syntheses/` = 컴파일된 위키 · `SCHEMA.md` = 규칙.
2. **모든 위키 페이지에 frontmatter 필수**. 새 페이지는 `explored: false` + `verificationStatus: unverified` 로 시작하고 `tools/new-page.py` 로 만든다.
3. **품질 3축은 직교**: `confidence`(증거 강도) / `verificationStatus`(source 대조) / `explored`(사람이 읽음). **`explored` 는 사람만 바꾼다.**
4. 페이지마다 `[[wikilink]]` 2개 이상. 새 페이지는 `index.md` 등록 + `log.md` append (`## [YYYY-MM-DD] action | subject`).
5. 페이지를 고치면 `updated` 를 bump 한다. 작업 마무리는 `python3 tools/lint.py` 0 errors.
6. **새 frontmatter 축**: 에이전트 작성 페이지는 `model`/`effort` + `claimType`/`evidenceScope` 기록 (`single-source` 면 `confidence: high` 금지). 타입 2종 — `questions/` research-question(열린 질문), `syntheses/` synthesis(논지 방어). **Paper Ingest Mode 는 opt-in** — 사용자 승인 없이 논문 atomization 금지.

## Operations

/ingest (자료 흡수) · /inbox (대기 큐 처리) · /query (위키 근거 답변) · /verify (페이지 검증) · /lint (건강 점검) · /status (스냅샷) · /wrap (세션 마무리: lint→log→commit)

CLI: `tools/lint.py` · `tools/status.py` · `tools/new-page.py <type> <slug>`

## Parity Contract
`CLAUDE.md` 와 `AGENTS.md` 는 같은 규칙의 미러다. 규칙을 바꾸면 두 파일을 함께 고치고 `python3 tools/lint.py` 로 parity 를 확인한다.
EOF

cat > "$TARGET/AGENTS.md" <<'EOF'
# AGENTS.md — LLM Wiki Harness (portable)

이 파일은 **Claude Code 이외의 코딩 에이전트**(Codex · Cursor · Windsurf · Gemini CLI 등)를 위한 스키마다. `CLAUDE.md` 의 미러이며, 두 파일은 **Parity Contract** 로 동일하게 유지된다. 규칙의 원본은 `SCHEMA.md` — 위키 콘텐츠를 만들거나 고치기 전에 반드시 읽는다.

## Essential Rules (요약 — 상세는 SCHEMA.md)

1. **3-Layer 분리**: `raw/` = 불변 원본 (절대 수정 금지) · `concepts|entities|comparisons|queries|guides|questions|syntheses/` = 컴파일된 위키 · `SCHEMA.md` = 규칙.
2. **모든 위키 페이지에 frontmatter 필수**. 새 페이지는 `explored: false` + `verificationStatus: unverified` 로 시작하고 `tools/new-page.py` 로 만든다.
3. **품질 3축은 직교**: `confidence`(증거 강도) / `verificationStatus`(source 대조) / `explored`(사람이 읽음). **`explored` 는 사람만 바꾼다.**
4. 페이지마다 `[[wikilink]]` 2개 이상. 새 페이지는 `index.md` 등록 + `log.md` append (`## [YYYY-MM-DD] action | subject`).
5. 페이지를 고치면 `updated` 를 bump 한다. 작업 마무리는 `python3 tools/lint.py` 0 errors.
6. **새 frontmatter 축**: 에이전트 작성 페이지는 `model`/`effort` + `claimType`/`evidenceScope` 기록 (`single-source` 면 `confidence: high` 금지). 타입 2종 — `questions/` research-question(열린 질문), `syntheses/` synthesis(논지 방어). **Paper Ingest Mode 는 opt-in** — 사용자 승인 없이 논문 atomization 금지.

## Operations

Operation 의 정식 절차는 `.claude/commands/{operation}.md` 에 마크다운으로 있다. `/` 트리거는 Claude Code 전용이지만 파일은 어느 에이전트나 읽을 수 있다 — operation 전에 해당 파일을 읽고 따른다.

/ingest · /inbox · /query · /verify · /lint · /status · /wrap

CLI (에이전트 무관): `tools/lint.py` · `tools/status.py` · `tools/new-page.py <type> <slug>`

## Agent-specific Notes

- **Codex/Cursor/Windsurf**: 이 `AGENTS.md` 를 자동 로드. `raw/` 는 불변 — 수정 금지 (Claude 는 hook 으로 강제되지만 다른 에이전트는 스스로 지킨다).
- **Gemini 등 `GEMINI.md` 를 찾는 에이전트**: `ln -s AGENTS.md GEMINI.md` 심링크.
- **자동 게이트**: raw 보호 hook 과 편집 후 자동 lint 는 `.claude/hooks/` 에만 있어 Claude Code 전용. 다른 에이전트는 편집 후 `python3 tools/lint.py` 를 수동 실행.

## Git

커밋 prefix 는 log action 과 동일: `ingest:` `update:` `create:` `lint:` `verify:`.

## Parity Contract (CLAUDE.md ↔ AGENTS.md)

두 파일은 미러다. Essential Rules / Operations / Git 규약이 동일해야 한다. 한쪽만 편집하면 drift — `python3 tools/lint.py` 가 parity 를 검사한다.
EOF

cat > "$TARGET/index.md" <<EOF
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Last updated: $TODAY | Total pages: 0

## Entities

## Concepts

## Comparisons

## Guides

## Questions

## Syntheses

## Queries
EOF

cat > "$TARGET/log.md" <<EOF
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: \`## [YYYY-MM-DD] action | subject\`
> Actions: ingest, update, query, lint, create, verify, archive, delete

## [$TODAY] create | Wiki initialized
- Scaffolded from llm-wiki harness (tools + commands + hooks + CI).
- Domain: $DOMAIN
EOF

cat > "$TARGET/.gitignore" <<'EOF'
.DS_Store
.claude/settings.local.json
EOF

# --- verify + git ---
(cd "$TARGET" && python3 tools/lint.py >/dev/null) && echo "lint: OK (empty wiki)"

if ! $NO_GIT && command -v git >/dev/null; then
  (cd "$TARGET" && git init -qb main && git add -A \
    && git commit -qm "create: LLM wiki scaffold — harness from llm-wiki template")
  echo "git: initialized with initial commit"
fi

echo
echo "✓ new LLM wiki at: $TARGET"
echo "next steps:"
echo "  1. SCHEMA.md 의 Domain 확정, Tag Taxonomy 시드 추가"
echo "  2. 첫 raw source 3개를 inbox/ 에 넣고 claude 에서 /inbox 실행"
echo "  3. /status 로 확인"
