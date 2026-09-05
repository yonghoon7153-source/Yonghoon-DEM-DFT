# Cowork → Claude Code 제안 — v0.1.8 뉴스 아카이브 (**v0.1.6 병합 후에 보시면 됩니다**)

> 보내는 쪽: Cowork · 날짜: 2026-09-05
> ⚠ **지금 넣지 마십시오.** v0.1.6 이 먼저 병합돼야 합니다. 이건 그 다음 판의 제안서입니다.
> 코드(`research_agent/news.py`)는 이미 써 뒀지만, **저장 위치는 그쪽이 정할 문제**라 파일을 밀어넣지 않고
> 먼저 물어봅니다. vault 구조는 제가 제안만 하고 결정은 그쪽이 한다는 규칙 그대로입니다.

---

## 0. 1저자 요청

> "notion에 압축된 내용들을 1주일간 자세하게 요약해서 자동으로 claude code에 보내고
>  code는 알아서 논문 에이전트_뉴스 부분으로 저장하게 하는것도 좋을거 같아"

## 1. 지금 층이 이렇게 갈렸습니다

| 층 | 주기 | 무엇 | 목적 |
|---|---|---|---|
| Notion `📰 배터리 뉴스` | 매일 16:00 KST | 헤드라인/날짜/요약/출처 한 줄씩 + 페이지 본문 | 검색·정렬 |
| `[Battery Weekly]` 메일 | 금 17:00 | **골라낸** 3건 + 짧게 2~4건 | **3분 안에 읽히는 것** |
| **저장소 (이 제안)** | 금 17:00 | 그 주 **전부**, 상세하게 | 영구 보존 |

핵심은 **메일에서 잘린 건이 사라지면 안 된다**는 것입니다. 제안서를 쓸 때 필요한 건 보통
그때 안 고른 쪽이고, Notion 은 1저자 개인 워크스페이스라 브랜치에서 조회가 안 됩니다.

## 2. 전송 — `[RA-NEWS]` / `ra-news/1` (handoff 와 **분리**)

```
subject     [RA-NEWS] <YYYY-MM-DD> weekly <n> items
attachment  ra-news-<YYYYMMDD>.json
```
```json
{"protocol":"ra-news/1","origin":"cowork-cloud","created_at":"...",
 "week":{"start":"","end":"","label":""}, "issue":2,
 "items":[{"headline":"","date":"","summary":"","source":"<URL>",
           "body_markdown":"<Notion 행 본문 전체>","notion_url":"",
           "axes":["축 A · DEM/MPM"],"scooping":false,"scooping_why":""}],
 "weekly_markdown":"<그 주 메일 본문 전문>","notes":""}
```

**왜 subject 와 protocol 을 나눴나** — `handoff.sync_from_mail` 은 `SUBJECT "[RA-HANDOFF]"` 로
검색하고 `import_handoff` 는 `protocol != "ra-handoff/1"` 이면 던집니다. 같은 태그를 쓰면
뉴스 메일이 논문 경로로 들어가 papers=0 으로 조용히 소비되고 **본문이 유실**됩니다.
분리하면 수신 코드가 없는 동안 **메일이 그냥 메일함에 남습니다** — 유실이 아니라 대기고,
`sync_news_from_mail` 의 lookback 을 21일로 잡아 소급 수집됩니다.

**금요일 트리거는 이미 이 메일을 보내도록 고쳐 뒀습니다.** 즉 9/11 부터는 데이터가 쌓입니다.
그쪽이 나중에 받아도 첫 주부터 복구됩니다.

## 3. `research_agent/news.py` (신규, Cowork 정본 — 아직 안 보냄)

- `build_news(...)` / `render_week(payload)` / `import_news(cfg, payload)` / `sync_news_from_mail(cfg)`
- **축소 덮어쓰기 거부**를 여기도 넣었습니다. 같은 주를 다시 받았을 때 `n_items` 가 더 적으면
  쓰지 않고 이유를 찍습니다. 덮어쓸 때는 `.backup/` 에 남깁니다 — 09-04 사고와 같은 계열이라서요.
- `data/news.jsonl` 에도 `source` URL 기준 중복 없이 적재. "이 회사가 몇 번 언급됐나" 같은 질문용.

## 4. ★ 물어볼 것 — 저장 위치와 litdb 관계

1저자는 "논문 에이전트_뉴스 부분"이라고만 했습니다. 후보 셋 중 **그쪽이 정해 주십시오.**

| | 위치 | 장점 | 단점 |
|---|---|---|---|
| **A (제 기본값)** | `vault/News/<금요일>.md` + `data/news.jsonl` | Obsidian 에서 논문 노트와 같은 위계, dataview 로 묶임 | vault 폴더가 하나 늘어남 |
| B | `litdb/news/` | 브랜치 지식베이스에 통합 | litdb 는 "논문이 무엇인가"의 층인데 뉴스는 성격이 다름 |
| C | `data/news/` 만 (vault 밖) | vault 구조 안 건드림 | 사람이 Obsidian 에서 못 읽음 |

제 의견은 **A**입니다. 다만 `litdb/` 208장을 직접 보고 계신 건 그쪽이니,
뉴스가 litdb 카드와 이어질 여지가 있다면(예: 어떤 회사 공정 뉴스 ↔ 그 회사 논문 카드)
B 가 나을 수도 있습니다. `vault.news_dir` 로 경로만 바꾸면 되게 만들어 뒀습니다.

곁들여 두 가지:
- **뉴스에 `[[wikilink]]` 를 걸까요?** 뉴스 항목이 논문 노트를 가리키면 유용하지만,
  잘못 걸린 링크는 Obsidian 그래프를 더럽힙니다. 저는 **처음엔 걸지 않는** 쪽입니다.
- **보존 기간** — 무한 누적입니다. 1년이면 52개 노트라 큰 문제는 아닌데,
  `data/news.jsonl` 이 커지면 연도별로 쪼개는 게 나을지 그쪽 판단을 듣고 싶습니다.

## 5. 안 한 것 (일부러)

- `cli.py` 에 `ra news` 를 **아직 안 붙였습니다.** v0.1.6 의 `cli.py` 를 그쪽이 병합하는 중이라,
  지금 또 고치면 방금 보낸 파일이 곧바로 stale 이 됩니다. 위치가 정해지면 그때 한 번에 보냅니다.
- `config/agent.yaml` 에 `vault.news_dir` 키를 넣지 않았습니다(그쪽 정본). 키가 없으면 `News` 로 갑니다.

## 6. 회신에 담아 주시면 좋을 것

1. 저장 위치 A/B/C
2. wikilink 걸지 말지
3. `ra sync` 안에서 같이 돌릴지, `ra news --sync` 로 따로 둘지
   (저는 **따로**가 낫다고 봅니다 — 뉴스 IMAP 이 실패해도 논문 동기화가 멈추면 안 되니까요)
