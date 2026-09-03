---
title: research-agent
tags: [research-agent, readme]
version: 0.1.2-dev
---

# research-agent — 논문 자동비서 (v0.1.2-dev)

> [!abstract] 한 줄
> Google Scholar alert 메일 → **IF 우선 triage** → 논문 에이전트의 심층 분석 → SQLite/JSONL DB + Obsidian vault + litdb → **매일 09:00 디제스트 메일**. 배관은 `ra` CLI(결정적), 판단은 LLM 에이전트(Hermes / Claude Code / Cowork)가 맡는다.

> [!warning] `config/research_profile.md` 는 STUB 상태다
> "연구자가 무엇을 하는가"는 이 파일이 유일한 근거이고, 그 내용은 **브랜치를 읽은 Claude Code가 채운다**. 비어 있는 동안 에이전트는 연결점을 지어내지 않고 `follow_up`에 미작성 표시만 남긴다.

## 파이프라인

```mermaid
flowchart LR
  GS[Google Scholar alert<br/>dem battery · dft battery] -->|메일 즉시| GM[(Gmail<br/>yonghoon71@hanyang.ac.kr)]
  GM -->|12:00 ra noon| ING[ingest<br/>Scholar HTML 파서]
  ING --> ENR[enrich<br/>Crossref/OpenAlex/S2]
  ENR --> TRI[triage<br/>관련도 게이트 → IF desc 정렬 → Tier A/B/C]
  TRI --> Q[분석 큐<br/>data/analysis/pending]
  Q -->|Hermes · Claude Code · Cowork| AN[심층 분석 JSON<br/>선정 이유·핵심·내 연구 연결·논문 활용·비판]
  AN --> DB[(papers.sqlite<br/>papers.jsonl)]
  DB --> V[Obsidian vault<br/>Papers/ Keywords/ Digests/ MOC]
  DB --> L[litdb]
  DB -->|09:00 ra morning| DG[디제스트 md] -->|SMTP/Gmail| GM
  V & DB --> GIT[git commit<br/>claude/friendly-meitner-lldvar]
```

## 3자 분업 (사용자 개입 없음)
| 주체 | 어디서 | 맡는 일 | 통신 |
|---|---|---|---|
| **Cowork (클라우드)** | claude.ai 예약 작업 12:00 / 09:00 KST | Gmail에서 alert 읽기, triage·분석 초안, 디제스트 발송 | 결과를 `[RA-HANDOFF]` 메일(JSON 첨부)로 같은 계정에 보냄 |
| **Hermes Agent (로컬 상주)** | 항상 켜진 PC, `hermes cron` | `ra sync`(handoff 병합), alert IMAP 재확인, 전문 PDF 기반 재분석, vault/litdb/git | 메일함 + git 브랜치 |
| **Claude Code** | 브랜치 `claude/friendly-meitner-lldvar`, `claude/stoic-knuth-NObVQ` | **`config/research_profile.md` 작성·유지**, 코드·설정 유지보수, `/paper-noon`·`/paper-morning`·`/paper-sync`, 헤드리스 `claude -p` 분석 백엔드 | git 브랜치 |

세 주체 모두 **같은 `ra` CLI와 같은 DB 스키마**를 쓴다. 누가 먼저 처리하든 결과는 한 곳(DB → vault → litdb)으로 모인다.

## 빠른 시작 (로컬)
```bash
pip install -e ".[dev,llm]"
cp .env.example .env        # EMAIL_ADDRESS / EMAIL_PASSWORD(앱 비밀번호) / ANTHROPIC_API_KEY(선택)
python -m pytest -q         # 8 tests
ra status
ra noon                     # alert 수집 → triage → 분석(큐 또는 직접) → vault/litdb → commit
ra morning --dry-run        # 디제스트 미리보기 → vault/Digests/<date>.md
ra schedule --target hermes # 또는 crontab | launchd | systemd
```

## 폴더 구조
```
research-agent/
├── config/            agent.yaml(키워드·스케줄·백엔드·litdb) · journal_if.yaml(IF 테이블) · research_profile.md(관련도 기준)
├── prompts/           style_guide.md · deep_analysis.md(JSON 스키마) · triage.md · digest.md
├── templates/         paper_note.md · daily_digest.md   (Obsidian 템플릿)
├── research_agent/    ra CLI 패키지 — sources/(scholar_email, imap, manual) enrich triage analyze digest vault mailer handoff exporters/litdb scheduler
├── hermes/            Hermes 스킬(paper-agent/SKILL.md, scripts/) + cron_jobs.md
├── claude-code/       CLAUDE.md · .claude/commands/paper-*.md · .claude/agents/paper-analyst.md  → 브랜치 루트로 복사
├── cowork/            클라우드 예약 작업 프롬프트(noon/morning) — 버전 관리용 사본
├── vault/             Obsidian vault (00_MOC · Papers/<year>/ · Keywords/ · Digests/ · Templates/)
├── data/              papers.sqlite · papers.jsonl · litdb.jsonl · inbox/(raw alert) · analysis/(pending|done|results) · handoff/
├── tests/             파서·triage·DB 테스트 + Scholar alert HTML fixture
├── ARCHITECTURE.md · SETUP_CLAUDE_CODE.md · SETUP_HERMES.md · CHANGELOG.md · VERSION
```

## 우선순위 규칙
1. 관련도(`config/research_profile.md` 기준, 0~1) < 0.35 → `rejected` (DB에는 남김)
2. 남은 논문을 **IF 내림차순**, 동률이면 관련도 내림차순으로 정렬 (`priority = IF×1000 + relevance×100`)
3. Tier A: IF ≥ 15 & 관련도 ≥ 0.55 · Tier B: IF ≥ 8 & ≥ 0.45 · Tier C: 나머지 (`config/agent.yaml: triage.tiers`)
4. 프리프린트는 IF 0 → 관련도만으로 판단, 디제스트에서는 Tier C

## 디제스트·노트 문체
`prompts/style_guide.md` — 자연스러운 한국어 평서체, 번역투 금지, 재료명·기법명·저널명·인명은 영어 유지, Obsidian frontmatter·`[[wikilink]]`·callout.

## 버전 정책
semver. `VERSION` = `research_agent.__version__` = `pyproject.toml`. 동작 변화는 `CHANGELOG.md`. 스키마 변경은 `db.py: SCHEMA_VERSION` 증가 + 마이그레이션.

## 로드맵
- v0.2: alert 도착 직후 3줄 인사이트 회신(`ra quick`), Gmail API 백엔드, 전문 PDF 자동 확보(교내망) + `article-skill` 연계
- v0.3: Notion DB 미러, 주간 리뷰(주제별 흐름·인용 네트워크), 저자/그룹 추적 alert
- v0.4: 내 논문 원고(Introduction/Discussion) 초안 생성기 — vault의 `use_in_my_paper` 필드 집계
