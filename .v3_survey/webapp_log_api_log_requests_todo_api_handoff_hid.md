# webapp — 작업기록 · 요청 · 미결 (/log · /api/log · /requests · /todo · /api/handoff/<hid>)

## 지금 무엇인가
이 앱의 "지금 무슨 일이 벌어지고 있나" 를 맡은 세 화면이다. /log 는 journal.jsonl(81건, 오늘 5건 추가)을 최신순 타임라인으로 깔고 그 아래 kb/results/*.md 94편을 카드 격자로 붙인다. /requests 는 1저자 요청 10건의 상태 요약을 먼저 세우고 kb/reports/paper_first_author_requests_2026_08.md(1587줄) 본문을 잇고, /todo 는 kb/open_items.md(141 KB · 헤딩 56개)를 통째로 한 페이지에 편다. 셋 다 렌더는 200 이고 내부 링크 36개 전부 살아 있다 — 문제는 깨진 게 아니라 낡음·과잉·항해 불가다.

## 처음 오는 사람
처음 온 사람이 여기서 얻는 건 "이 랩이 뭘 하는지" 가 아니라 "정신 없다" 다. 세 화면 모두 **오늘이 어디인지 말해 주지 않는다.** /log 타임라인 맨 위는 2026-09-08 인데 그 다음이 2026-08-25 다 — 그 사이 13일에 커밋 806개가 있었는데 기록은 0건이고, 화면은 그걸 "작업 기록" 이라 부르며 빈 구간을 표시조차 안 한다. 그래서 신참은 8월 말에 캠페인이 멎었다고 읽는다. /todo 는 141 KB 짜리 단일 스크롤인데 목차가 없다(`toc` 확장은 켜져 있지만 `[TOC]` 마커가 없어 실제 TOC 가 안 생긴다) — 56개 헤딩 사이를 검색 없이 굴러다녀야 하고, 맨 위 최우선 항목 ⏭-2 는 오늘 기준으로 이미 틀린 말을 한다. /requests 는 셋 중 유일하게 제대로 안내한다("📘 처음 읽는 사람은 §16 부터") — 그런데 그 문장이 헤더가 아니라 본문 5.3% 지점, 요약 카드 **아래**에 묻혀 있다. 그리고 무엇보다: 이 세 화면 어디에도 `/governance`(판정 원장) 링크가 없다. 09-07~08 에 비준된 결정 4건(LPSOCl 닫힘조건 · cascade D_rel 보고량 · b2o3 힘 대조 · b2o3 마감 소급)이 앱에서 가장 최신인데, 작업기록 본문엔 `D-2026-09-08-cascade-d-rel-estimand` 가 **누를 수 없는 맨 글자**로만 나온다. 신참이 밟아야 할 길 — "오늘 뭐가 정해졌나 → 그래서 뭘 못 쓰나 → 지금 막힌 건 뭔가" — 가 화면상 연결돼 있지 않다. 반대로 잘 된 것 하나는 /requests 의 순서다: 1000줄 문서를 열기 전에 완료 5 / 부분 2 / 막힘 3 을 먼저 보여준다. v3 는 이 패턴을 /todo 와 /log 에 그대로 옮기면 된다.

## 건드리면 안 되는 것
- **data-claim 결속 (BG ②)** — /log(templates/log.html:47)·/requests·/todo 전부 결속 검사를 통과한다. `pytest -k "claim or binding or retract"` 9 passed, `_LEGACY_UNBOUND == {}`(래칫 은퇴 완료), 그리고 test_each_surface_zero_comes_from_declarations_not_from_absence 가 /log·/todo·/requests·/api/handoff 를 각각 따로 검사한다. v3 재편 때 카드·행 구조를 바꾸더라도 **data-claim 속성을 떨어뜨리면 안 된다** — 떨어뜨리면 테스트가 잡아 주긴 하지만, 마크업 재작성 전에 이 계약을 먼저 알고 들어가야 한다.
- **journal.jsonl 의 과거 항목 원문** — 정정·철회가 본문 안에 그대로 남아 있는 게 근거의 일부다(예: 2026-08-25T15:00 "앞 기록의 표현을 바로잡는다", 14:00 "b2o3 UMA-MD 전도도 축 철회"). 문구를 다듬거나 kind 를 소급 수정하지 말 것. 어휘 통일은 표시층 매핑으로만 한다.
- **/requests 의 '요약 카드 먼저, 본문 나중' 구조**(app.py:530-534 docstring + requests.html:35-70). 1000줄 문서 앞에 완료/부분/막힘을 세운 이 순서가 세 화면 중 유일하게 제대로 된 IA 다 — v3 에서 /todo·/log 에 그대로 이식할 원형이다.
- **`requests_ledger()` 의 '판정하지 않는다' 규율과 conflict 표시 장치**(data.py:320-325 docstring, :345-351). 지금 conflict 가 0 이라고 장치를 걷어내면, 원문 이모지와 문장이 다시 갈릴 때 화면이 조용히 한쪽을 고르게 된다. 주석만 시제를 고치고 기계는 남긴다.
- **'못 읽었다 / 없다 / 대기' 를 세 문장으로 가르는 폴백들** — requests.html:66-69("⚠ 요청 대장 표를 못 읽었다"), doc.html:72-82("이 표가 비어 있는 것은 잡이 없어서가 아니라 원장을 못 읽어서다"), ledger_page docstring. 빈 화면을 '값 없음' 으로 읽히게 하지 않는 이 규율은 이 앱의 자산이다.
- **mdlite 필터로 journal 본문을 찍는 것**(log.html:53-54, 오늘 커밋 fc3624184). 원문을 raw 로 되돌리면 별표가 노출되고, `|safe` 로 바꾸면 저장 경로가 열려 있는 필드에 HTML 이 들어간다. 지금 형태를 유지한다.
- **doc.html 의 subtitle/banner 를 라우트가 넘기는 구조**(doc.html:5-6, 19-20 주석 — 2026-07-29 감사 결과). 템플릿에 문구를 다시 하드코딩하면 /methods·/sdcp 에도 같은 배너가 새어 나간다.
- **kb/results/*.md 94편 파일 자체** — 격자 표현이 문제지 문서가 문제가 아니다. 목록을 접거나 정렬을 바꾸는 것은 되지만 파일 삭제·통합은 안 된다(지우면 '안 돌린 계산' 으로 보인다 — doc.html:66-67 과 같은 이유).
- **READ_ONLY 기본값 정책**(app.py:31-49): 로컬은 열림, Render 는 잠금, ALLOW_MUTATIONS 로 명시 해제. 과거에 로컬까지 잠갔던 회귀가 주석에 남아 있다 — 화면에 잠금 상태를 **표시**하는 건 고쳐야 하지만 이 기본값은 건드리지 않는다.
- **open_items.md 안의 취소선·'⛔ 철회' 표기**(예: ⏭-3 의 `~~실패 조건 |ρ| < 0.2 ⇒ 이동도 축 근거 소멸~~ ⛔ 회신 AL P0-4 로 삭제`). 닫힌 항목을 접을 때 이 취소선 이력까지 감추면 '무엇이 언제 바뀌었나' 가 사라진다 — 접되 펼치면 그대로 보이게 한다.

## 발견

### [P1·wrong] log-sdcp-card-forbidden-phrases
- **어디**: `webapp/templates/log.html:15-18`
- **근거**: /log 상단 하위페이지 카드: "🧪 SDCP wave1 — 바인더가 앉는 자리 … 게이트 오탐 30→0, 자기 basin 벌점 50 meV, ptfe_dimer 2-seed 0.1 meV 일치." 세 숫자 전부 그 카드가 스스로 출처로 댄 kb/results/sdcp_wave1_explainer_2026_08_25.md 가 금지한 표현이다. ① L223: "고친 뒤 INCAR 불일치 **30 → 0**, 게이트 **0/30 → 17/30**." / L224: "남은 13건은 위 5·6절의 진짜 물리 문제다." — 30→0 은 INCAR 불일치지 게이트가 아니고, 게이트는 13건이 여전히 실패다. ② L165: "🔴 그 basin 차이는 **~50 meV 진단값**이다 (⚠ \"측정\" 아님 — 2026-08-25 교차리뷰로 정정)", L236 금지문구 표: "basin 벌점을 **측정**했다: 50.2 ± 0.2 meV" ← 쓰면 안 되는 쪽. ③ L199: "k-점 미검증이라 \"0.1 meV 정확도\" 라는 말도 쓰지 않는다." — 카드가 바로 그 말을 쓴다.
- **고치는 법**: 카드 문구를 원본 판정문으로 교체: "INCAR 불일치 30→0 · 게이트 0/30→17/30(남은 13건은 물리 문제) · basin 어긋남 ~50 meV **진단값**(측정 아님) · ptfe_dimer 두 branch 0.09 meV(정확도 주장 아님)". 또는 숫자를 빼고 제목+한 줄 성격만 남긴다. 카드가 요약 숫자를 들 거면 원본 §5·§7 의 단서와 한 몸으로만 든다.
- codex 필요: False

### [P1·stale] todo-cascade-item-stale
- **어디**: `kb/open_items.md:75 (렌더: /todo 최상단 두 번째 항목)`
- **근거**: 화면 문구 그대로: "⏭-2. 39설계 D_rel 측정 — **회신 AL = NO-GO.** 해제조건 8건 중 ②(anneal seed 고정)만 이행(`34a400e9`), 나머지 7건 미이행 (2026-08-31 갱신)". 그런데 오늘 db/governance/decisions.json 에 D-2026-09-08-cascade-d-rel-estimand 가 status=active 로 들어 있고(제목: "cascade D_rel — 보고량·설계 대표·판정 규칙 (회신 AL 해제조건 #1·#2b·#5·#6)"), 커밋 22b00e909 "cascade 보고량 카드 비준 (proposed → active)" · 8c9338c96 Step 1 · 46566ca64 Step 2 · c221ac933 "cascade #7 — 실제 봉인" 이 이미 들어왔다. journal 2026-09-08T17:00 항목도 같은 말을 한다. 즉 '7건 미이행' 은 오늘 기준 최소 5건이 틀렸다.
- **고치는 법**: open_items.md ⏭-2 를 09-08 상태로 갱신하고(해제조건 표 8행 · 남은 것 #3·#4·#8), /todo 상단에 '이 문서 최종 갱신 vs db/governance/decisions.json 최신 비준일' 을 나란히 찍는 신선도 줄을 넣는다. 원장이 더 최신이면 화면이 그렇다고 말해야 한다.
- codex 필요: False

### [P1·stale] requests-lpsocl-decision-stale
- **어디**: `kb/reports/paper_first_author_requests_2026_08.md:18 (렌더: /requests 요약 카드 요청 3행)`
- **근거**: 화면: "3 | LPSOCl MSD plot | 🟡 도구 완성 · 셀 확대판(243 Li) 확보 — **어느 판을 쓸지 판정 대기** | 본문 §2 · §9 · §15". 그런데 그 '어느 판' 은 이미 두 번 결정됐다 — decisions.json 의 D-2026-09-04-lpsocl-box331-400ps-uniform(active) 과 D-2026-09-08-lpsocl-box331-closure-conditions(active, "② bulk 축은 심사자 요구(R1) 때만 — 이번 원고는 cell-conditioned Ea 로만 쓴다"). 커밋 5196c1081 "LPSOCl 3×3×1 닫힘 조건 — 1저자 비준 (proposed → active), 결과 보기 전". 소스 문서의 마지막 내용 갱신은 2026-08-25 이고(그 뒤 40ffb7b97 은 링크 수선뿐), 문서 안에 2026-09 문자열이 하나도 없다.
- **고치는 법**: 요청 3 행을 '판정 완료(2026-09-08, cell-conditioned Ea) · 남은 것은 그림 산출' 로 갱신. 그리고 요약 카드에 **각 행이 언제 갱신됐는지**와 '이 대장 갱신일 2026-08-25 · 그 뒤 관련 결정 3건 → /governance' 링크를 붙인다.
- codex 필요: False

### [P1·wrong] open-items-count-includes-closed
- **어디**: `webapp/data.py:371 (필터) · webapp/data.py:375 (집계) → 대시보드 "📋 미결 리스트 … 대기 47건"`
- **근거**: `if not title.startswith("✅"):  # 닫힌 항목은 카드에서 제외` 가 `## ` 레벨에만 걸리고, 바로 아래 `elif line.startswith("### ") and cur is not None: cur["items"].append(...)` 는 무조건 담는다. 실측 47건 중 8건이 이미 닫힌 항목이다: ⏭-1(✅ 판정 완료 2026-08-29) · 3(~~VGCF~~ → ✅ 2026-07-30) · 6(~~LPSOCl COHP~~ → ✅ 2026-07-29) · 7(~~litdb 인덱스~~ → ✅ 2026-08-06) · 10(~~ELF 표시명~~ → ✅ 2026-08-06) · O(✅ Nd 갭 마감 2026-08-12) · R(✅ 닫음 2026-08-19) · ~~M6~~(✅ 2026-08-20). 게다가 '이상욱 랩 논문 확보 위시리스트' · '🔁 판정 정정 이력' 같은 절 라벨도 항목으로 세고 있다.
- **고치는 법**: `###` 제목에도 같은 마감 판정을 건다 — 선행 ✅ / `~~…~~` 취소선 / '→ ✅ 닫음' 패턴을 닫힘으로 보고 제외하고, 절 라벨(항목 번호·⏭ 접두 없음)은 세지 않는다. 숫자를 고치기 전에 '무엇을 미결로 세는가' 를 한 줄 규칙으로 코드에 적어 둘 것.
- codex 필요: False

### [P1·ia] todo-no-toc-141kb-wall
- **어디**: `webapp/app.py:518 (`md_html(md, ("tables","fenced_code","toc"))`) · webapp/templates/doc.html:151`
- **근거**: kb/open_items.md 는 140,899 바이트, 렌더 HTML 190 KB, 헤딩 56개. `toc` 확장이 켜져 있는데 문서에 `[TOC]` 마커가 0개라 실제 목차는 생성되지 않는다(렌더 결과에 `class="toc"` 0건). 생성된 앵커도 한글이 다 깎여 쓸모가 없다 — `id="2026-08-28-2026-08-31"`, `id="-3"`, `id="-1-t13-2026-08-29"`. 페이지에 검색창·필터·접기 아무것도 없다.
- **고치는 법**: doc.html 에 좌측 목차(또는 sticky 섹션 점프)와 검색 상자를 붙이고, ⏭ / 🔴 판정 대기 / PDF / ML / 심포지엄을 접이식 섹션으로 나눈다. 앵커는 md 헤딩에서 뽑지 말고 항목 번호(⏭-2, N, Q, M1…)를 슬러그로 쓴다.
- codex 필요: False

### [P1·useless] log-handoff-94-card-wall
- **어디**: `webapp/app.py:1245-1251 (`_handoffs`) · webapp/templates/log.html:61-71`
- **근거**: "Session Handoffs · kb/results (94)" 아래 카드 94장이 3열로 깔린다. 정렬은 `sorted(rd.glob("*.md"), reverse=True)` — 즉 **파일명 역알파벳순**이라 화면 첫 줄이 vgcf·uma·slide2·site… 다. 카드에는 제목(밑줄→공백 치환)과 `<id>.md` 뿐 — 날짜·조성·한 줄 요약이 없다. 그리고 kb/results 에 2026-09 파일이 **0개**라(`ls kb/results | grep 2026_09` → 없음) 09-07~08 작업(LPSOCl 마감 비준·cascade 보고량 카드·Nd 어닐·QE-GPU 런타임)은 이 격자에 아예 없다. 요청 대장에서 지적한 /sdcp '3D 구조 파일 버튼 95개' 와 같은 유형이다.
- **고치는 법**: 기본은 **최근 10편만** 펼치고 나머지는 접는다. 정렬 키를 파일명이 아니라 파일명 안의 날짜(또는 git mtime)로 바꾸고, 카드에 날짜 배지 + 조성 태그 + 첫 문장 한 줄을 싣는다. 검색 상자 하나면 94편이 다시 쓸모를 얻는다. 파일은 지우지 않는다.
- codex 필요: False

### [P1·missing] log-13day-gap-invisible
- **어디**: `webapp/journal.jsonl (81줄) · webapp/templates/log.html:6,43`
- **근거**: 타임라인 첫 항목 2026-09-08T18:00, 둘째부터 다섯째까지 09-08, 여섯째가 곧바로 2026-08-25T21:00 이다. 2026-08-26~09-07 구간 journal 항목 0건, 같은 구간 커밋 806개(`git log --since=2026-08-26 --until=2026-09-08 --oneline | wc -l` → 806). 화면 부제는 "결정·계산등록·결과·메모를 남기면 webapp/journal.jsonl에 저장" 이고 섹션 제목은 "기록 타임라인 · 81건" — 이게 손으로 적는 일지라는 말도, 806커밋 구간이 비었다는 말도 없다.
- **고치는 법**: 타임라인을 **날짜별로 묶고**(/notes 가 이미 하는 방식), 항목이 없는 날 구간은 "2026-08-26 ~ 09-07 · 기록 없음(커밋 806)" 같은 회색 갭 줄로 명시한다. 부제에 '수기 일지 — 전수 기록이 아니다' 를 한 줄 넣는다. 비어 있는 것과 일이 없었던 것은 다른 말이다.
- codex 필요: False

### [P1·ia] no-link-to-governance-ledger
- **어디**: `webapp/templates/log.html (전체) · webapp/app.py:519-521 (/todo banner) · webapp/templates/requests.html:30-32`
- **근거**: 세 화면 어디에도 `/governance` 링크가 없다. /todo 배너는 `{"url": "/ledger", ...}` 하나뿐이고, /requests 상단 버튼은 /log · /todo · / 셋뿐이며, /log 하위페이지 카드는 /requests · /sdcp 둘뿐이다. 그런데 journal 본문은 결정 ID 를 맨 글자로 인용한다 — "근거: db/properties/lpsocl_box331_closure_conditions_2026_09_07.json · 결정 D-2026-09-08-lpsocl-box331-closure-conditions" (2026-09-08T14:00), "D-2026-09-08-cascade-d-rel-estimand, active" (17:00). /governance 는 이 ID 세 건을 실제로 렌더한다(D-2026-09-08-cascade / D-2026-09-08-lpsocl / D-2026-09-07-b2o3 전부 포함, 64 KB).
- **고치는 법**: ① /log·/todo·/requests 헤더에 '⚖ 판정 원장' 버튼 추가. ② journal·open_items 본문의 `D-YYYY-MM-DD-...` 패턴을 mdlite/md_html 에서 /governance#<id> 링크로 자동 승격(레지스트리에 있는 ID 만 — 없으면 링크 안 검, 유령 결속 금지 규율과 같은 방식). 이게 v3 의 '오늘 뭐가 정해졌나' 동선의 뼈대다.
- codex 필요: False

### [P2·stale] todo-tq-banner-says-today
- **어디**: `webapp/app.py:519-521`
- **근거**: 주석은 "⚠ 날짜를 하드코딩하지 않는다 — 원장 파일이 늘어도 이 문구는 그대로 맞다" 인데, 배너 문구가 "이 리스트의 T 번호가 **오늘** 어디까지 움직였는지는 하루치 원장에서 본다" 다. 실물 원장 파일은 db/properties/tq_ledger_2026_08_26.json **하나**뿐(`D.load_tq_ledger()` → n=1, date 2026-08-26). 오늘은 09-08 이라 13일 전 것이고, 배너에는 날짜가 안 찍힌다.
- **고치는 법**: 배너 텍스트에서 '오늘' 을 빼고 최신 원장 날짜를 데이터에서 읽어 찍는다 — "가장 최근 하루치 원장: 2026-08-26 (13일 전)". 날짜를 하드코딩하지 말라는 주석의 취지는 지키면서 '오늘' 이라는 시간 주장도 없앤다.
- codex 필요: False

### [P2·useless] todo-empty-closed-section
- **어디**: `kb/open_items.md:1481-1482 (렌더: /todo 맨 끝)`
- **근거**: 파일 마지막 두 줄이 `## ✅ 닫힌 항목` / `- (여기로 이동)` 이고 그 아래 `###` 이 0개다. 렌더 결과 꼬리도 그대로 "✅ 닫힌 항목 / (여기로 이동)". 즉 닫힌 항목 전용 절을 만들어 놓고 비워 뒀고, 실제 닫힌 8건은 위쪽 열린 항목 사이에 원래 분량 그대로 섞여 있다(⏭-1 이 최상단 두 번째 자리를 차지한다).
- **고치는 법**: 둘 중 하나만 한다 — 닫힌 8건을 이 절로 실제로 옮기고 화면에서 접거나, 절을 지우고 각 항목에 ✅ 배지+접기를 준다. '(여기로 이동)' 플레이스홀더가 화면에 남아 있는 건 /sdcp 의 TODO 칸과 같은 잡음이다.
- codex 필요: False

### [P2·broken] log-journal-not-sorted-by-ts
- **어디**: `webapp/app.py:1234-1242 (`_load_journal` → `return list(reversed(entries))`)`
- **근거**: ts 로 정렬하지 않고 파일 줄 순서만 뒤집는다. journal.jsonl 자체가 시간순이 아니다 — 어긋난 쌍 3개: 2026-08-04T23:59 > 23:40, 2026-08-06T03:00 > 2026-08-04T13:44, 2026-08-25T14:30 > 13:30. 렌더 결과에서도 08-25 구간이 15:40 → 15:00 → 13:30 → 14:30 → 14:00 순으로 나온다.
- **고치는 법**: `sorted(entries, key=lambda e: e.get("ts",""), reverse=True)`. ts 가 없거나 깨진 줄은 버리지 말고 맨 뒤에 '시각 없음' 으로 모은다(값이 없는 걸 0 으로 만들지 않는 규율).
- codex 필요: False

### [P2·ia] log-kind-vocabulary-split
- **어디**: `webapp/templates/log.html:25-30 (select) · :49 (`<span class="badge b-fam">{{ e.kind }}</span>`) · webapp/app.py:1273 (`kind = _s(d.get("kind"), "note")`)`
- **근거**: 파일 안 kind 값이 24종이다: webapp 17 · note 10 · figure 7 · 결과 6 · result 5 · compute 4 · fix 4 · tool 4 · data 3 · review 3 · calc 2 · litdb 2 · kb 2 · 결정 2 · retract 1 · figures+db 1 · plan 1 · kb+webapp 1 · db+kb 1 · analysis 1 · 미결 1 · 도구 1 · 정정 1 · 메모 1. 폼은 네 가지만 주는데 그 value 가 영어(decision/calc/result/note)라 라벨은 '메모' 인데 저장·표시는 `note` 다. 같은 뜻이 둘로 갈린 쌍이 넷: note/메모 · result/결과 · tool/도구 · fix/정정. 서버는 kind 를 `[:40]` 자르기만 하고 검증하지 않는다(comp 는 `D.COMPOSITIONS` 로 검증하면서).
- **고치는 법**: 어휘를 하나로 고정하고(한국어 라벨 + 안정적 영문 key), 표시 시 옛 값을 매핑 테이블로 흡수한다. 뱃지에 색을 주고, 종류 칩 필터를 단다(/notes 의 📝/💬 칩과 같은 방식). ⛔ journal.jsonl 의 과거 kind 문자열은 고치지 않는다 — 표시층에서만 접는다.
- codex 필요: False

### [P2·broken] log-save-button-swallows-403
- **어디**: `webapp/templates/log.html:87 · webapp/app.py:52-63 (`_guard_mutation`)`
- **근거**: 가드는 403 과 함께 친절한 세 필드를 돌려준다 — "읽기 전용 모드예요…", why: "공개 배포에는 인증이 없고, Render 기본 파일시스템은 재시작 때 초기화돼서…", how: "로컬이면 ALLOW_MUTATIONS 를 지우고…". 그런데 화면 쪽은 `.then(d=>{if(d.ok){…}else{showToast('저장 실패');}})` 라 그 설명을 통째로 버리고 '저장 실패' 네 글자만 띄운다. 게다가 템플릿 어디에도 READ_ONLY 를 아는 곳이 없다(`grep -rn "READ_ONLY" webapp/templates/` → 0건) — Render 배포판에서는 눌러도 반드시 실패하는 '저장' 버튼이 그대로 보인다.
- **고치는 법**: READ_ONLY 를 템플릿 전역으로 내려보내 잠겨 있으면 폼을 비활성화하고 이유를 그 자리에 적는다. 그리고 실패 토스트는 서버가 준 `err`/`why` 를 그대로 보여준다. /notes·/api/concept-upload 도 같은 구조라 함께 본다.
- codex 필요: False

### [P2·broken] handoff-modal-404-hangs
- **어디**: `webapp/app.py:1287-1294 (`abort(404)`) · webapp/templates/log.html:90-95 (`openH`)`
- **근거**: 없는 hid 는 Flask 기본 HTML 404 를 돌려준다(실측 Content-Type text/html, 본문 `<!doctype html><title>404 Not Found</title>`). 반면 `openH` 는 `fetch('/api/handoff/'+id).then(r=>r.json()).then(d=>…innerHTML=d.html)` 이고 `.catch()` 가 없다 — JSON 파싱이 던지면 모달이 '로딩...' 상태로 굳는다. 격자 카드가 렌더 시점의 파일 목록이라 파일이 지워지거나 이름이 바뀌면 바로 이 경로다.
- **고치는 법**: 라우트가 404 도 JSON 으로 내고(`jsonify({"error": ...}), 404`), openH 에 `.catch(()=>{본문에 '문서를 못 읽었다 — kb/results/<id>.md 없음'})` 를 붙인다. '사라진 표는 잡이 없다로 읽힌다'(doc.html:73-74) 와 같은 규율을 모달에도 적용한다.
- codex 필요: False

### [P2·stale] requests-conflict-comment-stale
- **어디**: `webapp/app.py:535 · webapp/data.py:347 · webapp/templates/requests.html:57-61`
- **근거**: app.py:535 "…어긋났다고 **표시**한다 (요청 5 가 그렇다)." 와 data.py:347 "⚠ 이모지와 문장이 어긋나는 행이 실제로 있다 (요청 5: 🔴 인데 \"재작성 완료\")." 그런데 지금 요청 5 는 `✅ **완료** (초판은 철회 후 재작성)` 이고 `requests_ledger()` 실측 conflict 는 10행 전부 False, 렌더 HTML 에 '표시 불일치' 문자열 0건이다. 즉 코드 주석 두 곳이 없는 사례를 현재형으로 말하고, 템플릿 57-61 의 설명 문단은 영원히 안 뜬다.
- **고치는 법**: 주석을 '2026-08 에 요청 5 가 그랬고 그 뒤 원문이 정정됐다 — 장치는 다음 사례를 위해 남긴다' 로 고친다. 기계는 그대로 두고(다음에 또 생긴다), 화면 설명 문단은 conflict 가 0 일 때 '현재 어긋난 행 없음' 한 줄로 대체해 장치가 살아 있음을 보인다.
- codex 필요: False

### [P2·stale] requests-지금-상태-without-asof
- **어디**: `webapp/templates/requests.html:40 · kb/reports/paper_first_author_requests_2026_08.md:11`
- **근거**: 요약 카드 제목이 "지금 상태 10건" 인데 소스 표 헤더는 "📋 요청 대장 (**2026-08-25** 갱신)" 이고 문서 전체에 '2026-09' 문자열이 0건이다. 카드 자체에는 기준 날짜가 안 찍혀서 '지금' 이 오늘로 읽힌다. 각 행 상태에는 날짜가 붙어 있으나(예: '재판정 진행 — 36런 회수·게이트 판정 (2026-08-25)') 카드 머리에는 없다.
- **고치는 법**: 제목을 "요청 상태 (대장 기준 2026-08-25)" 로 바꾸고, 그 옆에 db/governance/decisions.json 최신 비준일을 함께 찍어 격차를 보이게 한다. 화면이 판정하지 않는 원칙은 유지 — 날짜 두 개를 나란히 놓기만 한다.
- codex 필요: False

### [P2·buried] requests-onboarding-buried
- **어디**: `kb/reports/paper_first_author_requests_2026_08.md (렌더 /requests 본문 5.3% 지점)`
- **근거**: "📘 처음 읽는 사람은 §16 부터. b2o3 의 전도도가 왜 닫혔는지, 그럼 무엇이 남았는지(밴드갭·탄성·ICOHP)를 용어 정의부터 풀어 썼다. 나머지 절은 그 위에 선다." — 이 앱에서 신참 안내로 가장 잘 쓴 문장인데, 위치가 요약 카드 아래·본문 안이고 §16 로 가는 링크도 없다(앵커 미생성). 바로 뒤 "⚠ 1·2·3 이 한 덩어리다 … §9 를 먼저 읽을 것" 도 같은 처지 — 이건 그나마 requests.html:62-63 이 카드 안에 하드코딩해 올려 놨다.
- **고치는 법**: 헤더 바로 아래 '처음 오셨나요' 한 줄 배너로 올리고 §16·§9 로 실제 점프하는 앵커를 만든다. 이 문장은 v3 의 첫 화면 안내 문구 원형으로 쓸 만하다.
- codex 필요: False

### [P2·duplicate] log-no-filter-duplicated-effort
- **어디**: `webapp/templates/log.html:43-59 vs webapp/templates/notes.html:13-30 · webapp/app.py:1035-1046`
- **근거**: /notes 는 이미 '검색 상자 + 종류 칩(📝/💬) + 날짜별 묶음 + 최신순' 을 브라우저에서 즉시 거르는 방식으로 갖췄다(notes.html 주석: "⚠ 필터는 전부 브라우저에서 — 서버 왕복 없이 즉시 걸러야 \"찾아보는\" 맛이 난다"). /log 는 같은 성격의 시계열인데 81건이 필터·검색·날짜묶음 없이 한 줄로 쏟아진다(렌더 166 KB). 사이드바 '자료 · 기록' 그룹에도 📝 메모와 ✎ Work Log 가 따로 서 있어 신참은 둘의 차이를 못 읽는다.
- **고치는 법**: notes.html 의 필터·날짜묶음 패턴을 /log 에 재사용한다(새로 짜지 말 것 — 코드 규율 사다리 ③ '기존 도구 확장'). 나아가 v3 에서 '메모 / 작업기록' 을 한 화면 두 탭으로 합칠지 판단한다.
- codex 필요: True

### [P2·stale] todo-header-self-contradiction
- **어디**: `kb/open_items.md:6 vs :237`
- **근거**: L6: "## ⏭ 다음 세션이 **바로 이어서 할 것** (2026-08-28 등록 · **최종 갱신 2026-08-31**)" · L237: "### ⏭-7. 폴라론 S0 (ORCA) — 🔴 **회신 V = NO-GO · P0 5건** (2026-09-02 갱신)". 파일 자체가 09-02 갱신분을 담고 있는데 절 머리는 08-31 이라 하고, git 최종 수정은 4d0b49f76(2026-09-05)다. 화면은 이 08-31 을 그대로 옮긴다.
- **고치는 법**: '최종 갱신' 은 손으로 적지 말고 git mtime 이나 파일 안 최대 날짜에서 유도해 화면에서 찍는다. 문서 안 하드코딩 날짜는 '등록일' 만 남긴다.
- codex 필요: False

### [P2·ia] todo-subtitle-omits-top-section
- **어디**: `webapp/app.py:523-524 (subtitle="kb/open_items.md · 판정 대기 · PDF 확보 대기 · ML 후속 · 심포지엄 대응")`
- **근거**: 실제 문서의 첫 절이자 가장 중요한 "## ⏭ 다음 세션이 **바로 이어서 할 것**"(⏭-0 ~ ⏭-7, 9개 항목)이 부제 목록에 없다. 부제는 그 아래 네 절만 나열한다.
- **고치는 법**: 부제 맨 앞에 '⏭ 바로 이어서 할 것' 을 넣고, 가능하면 그 절의 미해결 개수를 함께 찍는다. 최신·중요한 것이 앞이라는 원칙이 부제부터 어긋나 있다.
- codex 필요: False
