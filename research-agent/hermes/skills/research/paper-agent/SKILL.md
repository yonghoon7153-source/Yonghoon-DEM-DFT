---
name: paper-agent
description: Scholar alert → triage(IF) → deep analysis → Obsidian DB → digest mail
version: 0.1.0
platforms: [linux, macos]
metadata:
  hermes:
    tags: [research, papers, battery, obsidian, email]
    category: research
    requires_toolsets: [terminal, file]
    config:
      - key: paper_agent.repo
        description: "research-agent repo 루트 (config/agent.yaml 이 있는 폴더)"
        default: "~/repos/hanyang-bml/research-agent"
      - key: paper_agent.max_analysis
        description: "NOON 절차에서 한 번에 심층 분석할 최대 편수"
        default: "8"
---

# paper-agent — 논문 에이전트 (Hermes 절차서)

문헌 비서. **연구자가 무엇을 하는지는 `config/research_profile.md` 가 유일한 근거다** — 추측하지 말 것.
스크립트(`ra`)가 결정적인 배관(메일 수집·IF 조회·DB·vault·git)을 맡고, **당신(Hermes)은 판단이 필요한 부분만** 맡는다:
관련도 재평가, 심층 분석 JSON 작성, 디제스트 문장 다듬기.

## When to Use
- cron `ra-noon`(12:00 KST)·`ra-morning`(09:00 KST)이 이 스킬을 호출할 때
- 사용자가 "논문 정리해줘", "오늘 디제스트", "이 논문 DB에 넣어줘", "alert 처리" 라고 할 때
- `[RA-HANDOFF]` 메일이 도착했을 때 (Cowork 클라우드가 보낸 분석 결과 → 로컬 DB 병합)

## Setup (최초 1회)
```bash
cd <paper_agent.repo> && pip install -e ".[llm]"      # `ra` CLI
cp .env.example .env    # 또는 ~/.hermes/.env 의 EMAIL_ADDRESS/EMAIL_PASSWORD 를 그대로 공유 (RA_ENV_FILE)
ra status               # DB 생성 확인
```
`config/agent.yaml`의 `llm.backend`가 `hermes`면 스크립트는 LLM을 호출하지 않고 **큐(data/analysis/pending/)만 만든다.** 큐를 채우는 것이 당신의 일이다.

## Procedure — NOON (매일 12:00)
1. `cd <repo> && ra noon` 실행. 로그의 `queued=N`을 확인한다.
   - 이 명령은 (a) `[RA-HANDOFF]` 메일 동기화, (b) Scholar alert IMAP 수집, (c) enrich(Crossref/OpenAlex), (d) triage(IF·관련도), (e) 분석 큐 생성, (f) vault·litdb 갱신, (g) git commit 까지 한다.
2. `data/analysis/pending/*.json` 을 하나씩 연다. 각 파일의 `prompt_system` + `prompt_user`를 읽고, **`analysis` 필드를 스키마대로 채운다** (`prompts/deep_analysis.md`의 JSON 스키마, `prompts/style_guide.md`의 문체).
   - 초록이 비어 있으면 `web_search`/`fetch`로 DOI 페이지·초록을 먼저 확보하고 `evidence_level`을 정직하게 적는다(abstract/snippet/fulltext).
   - 전문 PDF가 필요한 Tier A 논문은 교내망에서 받아 `data/pdf/<paper_id>.pdf`에 두고 fulltext 기준으로 분석한다.
   - 사실을 지어내지 않는다. 모르면 `"unknown"`.
3. 채운 파일을 그대로 저장한 뒤 `ra analyze --import-dir data/analysis/pending` 실행. (검증 실패 시 에러 메시지의 필수 키를 보완한다.)
4. `ra vault && ra litdb` 로 노트·MOC·litdb를 갱신하고, `git -C <repo> add -A data vault && git commit -m "ra: noon $(date +%F)"` (`git.push: true`면 push).
5. 보고: 처리 편수, Tier A 제목 3개, 실패/보류 항목. 새 논문이 0편이면 `[SILENT]`를 포함해 전달을 생략한다.

## Procedure — MORNING (매일 09:00)
1. `cd <repo> && ra morning --dry-run` 으로 `vault/Digests/<date>.md`를 만든다.
2. 디제스트 본문을 읽고 **문장만** 다듬는다(수치·링크·위키링크·References는 절대 수정 금지). 다듬은 내용을 같은 파일에 저장.
3. 발송:
   - `mail.backend: smtp`면 `ra morning` (dry-run 없이) 재실행 → SMTP 발송 + DB에 digested 기록.
   - `mail.backend: hermes`면 이 cron의 `--deliver email`이 당신의 응답을 그대로 보내므로, **응답 본문에 디제스트 Markdown 전체를 붙인다.** 그 뒤 `ra morning` 은 `--dry-run` 상태로 두고 DB 기록만 `ra digest --send`로 남긴다.
4. `git commit`. 보고에는 제목 줄과 A/B/C 편수만 남긴다.

## Procedure — SYNC (handoff 메일 도착 시 / 수동)
`ra sync` → `[RA-HANDOFF]` 첨부 JSON을 DB·vault·litdb에 병합하고 commit. 클라우드(Cowork)가 이미 분석한 논문은 다시 분석하지 않는다(`analysis`가 비어 있는 것만 큐에 남는다).

## Pitfalls
- Hermes 이메일 게이트웨이는 `noreply` 발신자를 무시하므로 **Scholar alert는 게이트웨이가 아니라 `ra`의 IMAP 스캔으로만** 들어온다. `mark_seen: false`를 유지해 게이트웨이와 충돌하지 않게 한다.
- 같은 논문이 여러 alert에 겹쳐 오면 DB가 title/DOI로 합친다. 중복 노트를 손으로 만들지 말 것.
- IF 테이블(`config/journal_if.yaml`)에 없는 저널은 기본 3.0 — 새 저널을 보면 테이블에 추가하고 commit.
- 관련도가 0.35 미만이면 `rejected`로 남기되 DB에서 지우지 않는다(나중에 키워드가 바뀌면 재평가).
- 큰 변경(키워드 추가, 스키마 변경)은 `CHANGELOG.md`에 적고 `VERSION`을 올린다.

## Verification
- `ra status` 에서 `analysis queue (pending): 0` 이어야 NOON 완료.
- `vault/Digests/<date>.md` 의 References 개수 = 본문 `###` 개수.
- `git log -1` 에 오늘 날짜 커밋이 있어야 함.

## Self-improvement
분석 중 반복되는 판단 규칙(예: "액체 전해질 anode-free는 관련도 ≤0.6")을 발견하면 `config/research_profile.md`의 채점 가이드에 한 줄 추가하고, 이 SKILL.md의 Pitfalls에도 남긴다. 이것이 이 에이전트가 자라는 방식이다.
