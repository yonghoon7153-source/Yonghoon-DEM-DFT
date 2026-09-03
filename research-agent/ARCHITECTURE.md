---
title: research-agent Architecture
tags: [research-agent, architecture]
version: 0.1.0
---

# ARCHITECTURE

## 설계 원칙
1. **결정적 배관 / 판단 분리** — 메일 파싱, IF 조회, DB, vault, git, 메일 발송은 `ra`(Python)가 재현 가능하게 처리한다. LLM은 관련도 재평가·심층 분석·문장 다듬기만 한다. 따라서 LLM이 없어도 파이프라인은 멈추지 않고(큐에 쌓임), LLM이 바뀌어도 데이터 계약(JSON 스키마)은 그대로다.
2. **한 계약, 세 실행자** — Hermes(로컬 상주), Claude Code(브랜치), Cowork(클라우드)가 모두 `prompts/deep_analysis.md`의 JSON 스키마와 `ra` CLI를 쓴다. 실행자를 갈아끼워도 DB·vault는 동일하다.
3. **메일함 = 메시지 버스** — 클라우드와 로컬은 파일시스템을 공유하지 않는다. 대신 사용자 메일함(`[RA-HANDOFF]` self-mail, JSON 첨부)을 큐로 쓴다. 컴퓨터가 꺼져 있어도 메일은 쌓이고, 켜지면 `ra sync`가 병합한다. 별도 토큰·서버가 필요 없다.
4. **DB는 하나, 뷰는 여럿** — 진실은 `data/papers.sqlite`. `papers.jsonl`(git diff용), Obsidian vault(사람이 읽는 뷰), `litdb`(기존 문헌 DB)는 모두 파생물이라 언제든 `ra vault`/`ra litdb`로 재생성한다.
5. **버전화·확장 여지** — 설정(키워드·IF·프로필)은 코드 밖(config/). 스키마는 additive migration. 새 소스(arXiv RSS, PubMed)는 `research_agent/sources/`에 파서 하나 추가하면 끝.

## 데이터 흐름과 상태 기계
```
alert mail ──parse──▶ Paper(status=new)
   new ──triage(IF, relevance)──▶ triaged | rejected
   triaged ──analysis JSON──▶ analyzed | rejected(LLM이 관련도 낮춤)
   analyzed ──digest 발송──▶ digested
   (known: 이미 읽은 논문으로 표시, 디제스트 제외)
```
`priority = IF×1000 + relevance×100 (+ keyword bonus)` → 정렬 키. IF 우선, 관련도는 tie-break.

## 모듈
| 모듈 | 책임 | 외부 의존 |
|---|---|---|
| `sources/scholar_email.py` | Scholar alert HTML/텍스트 파서 (`gse_alrt_title`, byline, snippet, `scholar_url` unwrap, DOI 추출) | bs4/lxml |
| `sources/imap_client.py` | IMAP(앱 비밀번호)로 alert 메일 수집, raw JSON 보관 | imaplib |
| `sources/manual.py` | 수동/bootstrap JSON 드롭 폴더 | – |
| `enrich.py` | Crossref → OpenAlex → Semantic Scholar 메타·초록 보강 (로컬 전용) | requests |
| `journals.py` | 저널명 정규화 + IF 조회(정확/별칭/부분 일치/프리프린트) | – |
| `triage.py` | 규칙 기반 관련도(용어 가중치) + LLM 재평가 병합, tier·priority | – |
| `llm.py` | anthropic / claude-cli / hermes(큐) / none 백엔드 | anthropic(선택) |
| `analyze.py` | 프롬프트 조립, 큐 파일 생성, 결과 검증·적용(tier 재계산) | – |
| `db.py` | SQLite 스키마, idempotent upsert(DOI/제목 병합), JSONL 미러, runs/alerts/digests 기록 | sqlite3 |
| `vault.py` | Obsidian 노트/키워드 MOC/홈/디제스트 렌더 (템플릿 치환) | – |
| `digest.py` | 디제스트 선택(마지막 발송 이후) + 결정적 렌더 + LLM 다듬기(선택) | – |
| `mailer.py` | SMTP 발송, md→html, 위키링크/콜아웃 변환, .md 첨부 | markdown |
| `handoff.py` | 클라우드↔로컬 릴레이 payload 생성·IMAP 수집·병합 | imaplib |
| `exporters/litdb.py` | litdb 적재 (file: JSONL/SQLite 병합, cli: `litdb add DOI`) | litdb(선택) |
| `scheduler.py` | crontab/hermes/launchd/systemd 스케줄 렌더 | – |
| `cli.py` | `ra` 명령 (status/ingest/triage/analyze/vault/litdb/digest/noon/morning/sync/handoff/schedule) | – |

## 클라우드 ↔ 로컬 프로토콜 (`ra-handoff/1`)
```json
{"protocol":"ra-handoff/1","origin":"cowork-cloud","created_at":"…",
 "papers":[{…Paper.to_dict() with analysis…}],
 "digest":{"date":"2026-09-04","markdown":"…","sent_at":"…","mail_message_id":"…"},
 "notes":"…"}
```
- 제목: `[RA-HANDOFF] <date> <job> <n> papers`. 첨부 `ra-handoff-<stamp>-<job>.json`.
- 병합 규칙: DOI/제목으로 upsert → 로컬 triage 필드가 비면 채움 → 로컬 `analysis`가 비어 있을 때만 클라우드 분석 채택 → 같은 논문에 둘 다 있으면 `evidence_level` 높은 쪽 유지(fulltext > abstract > snippet > title).
- 멱등: `alerts` 테이블에 message_id 기록 → 같은 메일 재처리 안 함.

## 장애 모드와 대응
| 상황 | 동작 |
|---|---|
| IMAP 자격증명 없음 | alert 수집 건너뜀, 수동 JSON만 처리, 로그에 경고 |
| enrich API 실패/차단 | 빈 필드로 진행(관련도는 제목·스니펫 기반), 로컬에서 재시도 |
| LLM 없음 | 큐만 생성 → 다음 실행자가 채움; 디제스트는 분석된 것만 |
| SMTP 실패 | 디제스트는 vault에 저장, DB에 `sent_at=null` → 다음 morning에 재포함 |
| 클라우드/로컬 중복 분석 | evidence_level 규칙으로 하나만 유지 |
| 저널 IF 미등록 | 기본 3.0, 로그에 저널명 → `journal_if.yaml`에 추가 |

## 확장 포인트
- 새 키워드: `config/agent.yaml: keywords` + Scholar alert 등록. 코드 수정 불필요.
- 새 소스: `sources/<name>.py`에 `-> list[Paper]` 함수 추가, `cli._ingest_*`에 연결.
- 새 뷰: `vault.py`에 렌더 함수 추가(예: 주간 리뷰), `templates/`에 템플릿.
- 새 실행자: `prompts/deep_analysis.md` 스키마만 지키면 어떤 에이전트든 큐를 채울 수 있다.
