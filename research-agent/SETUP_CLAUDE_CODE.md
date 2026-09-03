---
title: SETUP — Claude Code 쪽에서 할 일
tags: [research-agent, setup]
---

# Claude Code에서 해야 할 일 (브랜치 `claude/friendly-meitner-lldvar`)

> [!info] 이 문서는 "내가 Claude Code에서 환경을 구축하고 다시 부탁할게"에 대한 체크리스트다. 아래 프롬프트를 Claude Code 세션에 그대로 붙여 넣으면 된다.

## 0. 준비물
- `research-agent-v0.1.0.tar.gz` (Cowork가 전달) — 또는 Cowork 세션이 데스크톱 앱으로 컴퓨터에 링크돼 있으면 폴더가 이미 들어가 있음
- Gmail **앱 비밀번호** (2단계 인증 → myaccount.google.com/apppasswords), IMAP 활성화
- (선택) `ANTHROPIC_API_KEY` — crontab만으로 완전 자동 분석을 원할 때. Claude Code 구독으로 돌리려면 `llm.backend: claude-cli`

## 1. 브랜치에 넣기
Claude Code에 붙여 넣을 프롬프트:
```
브랜치 claude/friendly-meitner-lldvar 를 체크아웃하고, 첨부한 research-agent-v0.1.0.tar.gz 를 repo 루트의 research-agent/ 폴더로 풀어라.
research-agent/claude-code/CLAUDE.md 는 repo 루트 CLAUDE.md에 "## research-agent" 섹션으로 병합하고,
research-agent/claude-code/.claude/commands/paper-*.md 와 .claude/agents/paper-analyst.md 는 repo 루트 .claude/ 아래로 복사해라.
그 다음 cd research-agent && pip install -e ".[dev,llm]" && python -m pytest -q 로 8개 테스트가 통과하는지 확인하고 커밋해라.
```

## 2. 기존 논문에이전트·litdb와 통합
```
repo 안의 기존 논문 에이전트 코드와 litdb(스키마/저장 경로)를 찾아 정리해줘.
그 스키마에 맞춰 research-agent/config/agent.yaml 의 litdb.path / litdb.format / litdb.field_map 을 채우고
(research_agent/exporters/litdb.py DEFAULT_FIELD_MAP 참고), `ra litdb` 를 실행해 bootstrap 6편이 litdb에 들어가는지 검증해라.
기존 에이전트가 이미 하던 기능(예: PDF 요약)이 있으면 research-agent 의 분석 큐 프로토콜(data/analysis/pending)에 연결해라.
```

## 3. 자격증명·백엔드
```bash
cd research-agent && cp .env.example .env
# EMAIL_ADDRESS=yonghoon71@hanyang.ac.kr / EMAIL_PASSWORD=<앱 비밀번호> / (선택) ANTHROPIC_API_KEY
# llm.backend: hermes(기본, 큐만) | claude-cli | anthropic
ra status && ra noon --no-imap && ra morning --dry-run
```
`.env`는 `.gitignore`에 있다 — 절대 커밋하지 않는다.

## 4. 스케줄 (셋 중 하나)
| 방식 | 명령 | 특징 |
|---|---|---|
| **Hermes Agent** (권장) | `SETUP_HERMES.md` | 상주 게이트웨이, 스킬이 큐를 채움, 이메일 전달 내장 |
| crontab / launchd / systemd | `ra schedule --target crontab` | `llm.backend: anthropic` 또는 `claude-cli` 필요 |
| Claude Code 헤드리스 | `0 12 * * * cd <repo> && claude -p "/paper-noon"` | 구독으로 동작, `claude` CLI 필요 |

## 5. Cowork 클라우드 작업과 맞물리기
- Cowork가 09:00/12:00에 보내는 `[RA-HANDOFF]` 메일은 `ra sync` 또는 `/paper-sync` 로 병합된다. Hermes NOON 절차에 이미 포함돼 있다.
- git push를 켜면(`git.push: true`) Cowork(데스크톱 링크 시)도 최신 DB를 읽을 수 있다.

## 6. 검증 체크리스트
- [ ] `python -m pytest -q` 8 passed
- [ ] `ra status` 에 bootstrap 6편(analyzed 5 / rejected 1)
- [ ] `vault/` 를 Obsidian vault로 열었을 때 `Research Agent Home` → 키워드 MOC → 논문 노트 링크가 살아 있음
- [ ] `ra morning --dry-run` 이 `vault/Digests/<date>.md` 생성
- [ ] (자격증명 후) `ra noon` 이 실제 Scholar alert를 수집 — Scholar에서 `dem battery`, `dft battery`, `anode-less assb` alert를 **yonghoon71@hanyang.ac.kr**로 등록해 두어야 함
- [ ] `ra litdb` 가 기존 litdb에 레코드 추가

## 7. 이후 Cowork에 다시 부탁할 때
"브랜치에 research-agent 넣었고 litdb 스키마는 이거야" + 스키마 파일 첨부 → Cowork가 `field_map`·클라우드 작업 프롬프트를 맞춰 갱신하고 v0.1.1로 올린다.
