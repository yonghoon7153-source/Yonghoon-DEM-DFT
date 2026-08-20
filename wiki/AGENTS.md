# AGENTS.md — LLM Wiki Harness (portable)

이 파일은 **Claude Code 이외의 코딩 에이전트**(Codex · Cursor · Windsurf · Gemini CLI 등)를 위한 스키마다. `CLAUDE.md` 의 미러이며, 두 파일은 **Parity Contract** 로 동일하게 유지된다. 규칙의 원본은 `SCHEMA.md` — 위키 콘텐츠를 만들거나 고치기 전에 반드시 읽는다.

## Essential Rules (요약 — 상세는 SCHEMA.md)

1. **3-Layer 분리**: `raw/` = 불변 원본 (절대 수정 금지) · `concepts|entities|comparisons|queries|guides|questions|syntheses/` = 컴파일된 위키 · `SCHEMA.md` = 규칙.
2. **모든 위키 페이지에 frontmatter 필수**. 새 페이지는 `explored: false` + `verificationStatus: unverified` 로 시작하고 `tools/new-page.py` 로 만든다.
3. **품질 3축은 직교**: `confidence`(증거 강도) / `verificationStatus`(source 대조) / `explored`(사람이 읽음). **`explored` 는 사람만 바꾼다.**
4. 페이지마다 `[[wikilink]]` 2개 이상. 새 페이지는 `index.md` 등록 + `log.md` append (`## [YYYY-MM-DD] action | subject`).
5. 페이지를 고치면 `updated` 를 bump 한다. 작업 마무리는 `python3 wiki/tools/lint.py` 0 errors.
6. **새 frontmatter 축 (2026-08-06)**: 에이전트 작성 페이지는 `model`/`effort` provenance + `claimType`/`evidenceScope` 기록 (`single-source` 면 `confidence: high` 금지). 타입 2종 추가 — `questions/` research-question(열린 질문 추적), `syntheses/` synthesis(논지 방어, 반론 보존). **Paper Ingest Mode 는 opt-in** — 사용자 승인 없이 논문 atomization 금지 (`guides/paper-ingest-mode.md`).

## Operations

Operation 의 정식 절차는 repo root `.claude/commands/wiki-{operation}.md` 에 마크다운으로 있다. `/` 트리거는 Claude Code 전용이지만 파일은 어느 에이전트나 읽을 수 있다 — operation 전에 해당 파일을 읽고 따른다.

/wiki-ingest · /wiki-inbox · /wiki-query · /wiki-verify · /wiki-lint · /wiki-status · /wiki-wrap

CLI (에이전트 무관, repo root 에서): `python3 wiki/tools/lint.py` · `python3 wiki/tools/status.py` · `python3 wiki/tools/new-page.py <type> <slug>`

## Mothership 특칙

이 위키는 **Yonghoon-DEM-DFT 모노레포의 mothership**이다 (위치: repo root `wiki/`). 개별 프로젝트(satellite)는 `entities/` 1페이지로 등록하고 상태 변화 시 갱신한다 (절차: `guides/new-project-kickoff.md`). Cross-vault 참조는 `[[wikilink]]` 대신 **repo-root 상대 경로**(예: `degradation-degeneracy/docs/...`), 내용 복사 금지(living reference). 이유: satellite 이 같은 repo 안에 있고 clone 경로가 머신마다 다르다. 설계 세션 결정은 `raw/transcripts/` 세션 기록으로 남겨 source로 삼는다.

## Agent-specific Notes

- **Codex/Cursor/Windsurf**: 이 `AGENTS.md` 를 자동 로드. `raw/` 는 불변 — 수정 금지 (Claude 는 hook 으로 강제되지만 다른 에이전트는 스스로 지킨다).
- **Gemini 등 `GEMINI.md` 를 찾는 에이전트**: `ln -s AGENTS.md GEMINI.md` 심링크.
- **자동 게이트**: raw 보호 hook 과 편집 후 자동 lint 는 `wiki/tools/hooks/` + root `.claude/settings.json` 에 있어 Claude Code 전용. 다른 에이전트는 편집 후 `python3 wiki/tools/lint.py` 를 수동 실행.

## Git

커밋 prefix 는 log action 과 동일하되 모노레포 컨벤션에 맞춘 scope 를 붙인다: `ingest(wiki):` `update(wiki):` `create(wiki):` `lint(wiki):` `verify(wiki):`. push 는 **루트 `CLAUDE.md` 하드룰 1이 지정한 작업 브랜치**로만 — 브랜치 이름은 여기 적지 않는다 (lint `no-hardcoded-branch-name` 검사).
공유 remote(origin)가 있으면 **세션 시작 시 `git pull --rebase`**, 마무리는 `/wrap` 절차가 commit+push 한다. `log.md` 충돌 시 양쪽 항목 모두 보존한다 (append-only).

## Parity Contract (CLAUDE.md ↔ AGENTS.md)

두 파일은 미러다. Essential Rules / Operations / Git 규약이 동일해야 한다. 한쪽만 편집하면 drift — `python3 wiki/tools/lint.py` 가 parity 를 검사한다.
