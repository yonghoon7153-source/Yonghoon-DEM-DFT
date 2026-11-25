# webapp — 대시보드(/) + 기본 골격(base.html · app.py 라우트 등록부)

## 지금 무엇인가
Flask 앱의 홈이다. `/` 는 핵심 발견 카드 41장 → 미결 리스트 47건 → SEI 분해상 표 → 통계 4칸 → Pipeline 도식 → Coverage Matrix 14×7 → family 별 조성 카드 14장을 한 페이지에 세로로 쌓는다(렌더 HTML 100 KB). base.html 은 사이드바를 '하는 일' 순서(결과 보기 / 계산 돌리기 / 문헌·검증 / 자료·기록 / Compositions)로 묶고 ⌘K 팔레트·사이드바 접기·테마 토글·skip-link 를 얹는다. app.py 에 페이지 라우트 25개 + API 18개가 등록돼 있고 전부 200 이다(`/cascade/diagnostic` 만 의도된 403).

## 처음 오는 사람
처음 온 사람이 여기서 할 수 있는 건 사실상 "읽기" 하나다. 그리고 그게 지금 제일 안 된다.

첫 화면에서 만나는 문장은 부제 한 줄("황화물 SE 전고체전지 · 조성 × 물성 지식 매트릭스 · db/ 실시간 동기화")이고, 바로 다음이 카드 1번 "⭐ LPSOCl 3×3×1 닫힘 조건 **비준** — 아레니우스를 하나도 그리기 전에 / 허용차 δEa 0.05 eV · 해상도 0.05 eV" 다. LPSOCl 이 뭔지, 3×3×1 이 뭔지, 닫힘 조건이 뭔지, δEa 가 뭔지 하나도 안 알려주고 시작한다. 두 번째 카드는 "D_rel(design, host) ≡ D*(design) / D*(host), 600 K · 2–50 ps 창 · cell-conditioned". 온보딩이 0 이다 — `grep "처음|시작하기|안내|여기서 시작"` 이 index.html·base.html 에서 0건.

막히는 지점을 순서대로 적으면:

1. **양이 벽이다.** 카드 41장, 본문 26,672자. 한국어 정독 300자/분이면 89분짜리 화면이다. 접기가 없고 CSS 에 clamp 도 없다(style.css:729 `.find-card .fc-n` 에 max-height 없음). 최장 카드가 1,619자인데 grid-3 라 같은 줄의 29자짜리 카드까지 그 높이로 늘어난다.
2. **이 앱의 골자가 첫 화면에 없다.** 이 repo 는 "인용해도 되는 값 / 안 되는 값" 으로 굴러가는데, 그걸 담은 `/governance`(인용 위험 25건 · 결정 원장 22건 · 데이터 유실 1건 · 유일본 11건)는 대시보드 본문에서 링크가 **0건**이고 ⌘K 검색에도 안 들어 있다. 새로 온 사람은 그 페이지가 있다는 걸 알 방법이 없다.
3. **정본값으로 가는 길이 없다.** `/explorer` 로 가는 링크가 본문에 0건, `/literature` 0건. 카드마다 "출처: db/properties/canonical_registry.json", "결정 원장 D-2026-09-08-lpsocl-box331-closure-conditions" 라고 적혀 있지만 전부 평문이라 못 누른다.
4. **표기 규칙을 안 알려준다.** 카드 제목의 ⭐/🔴/⛔/⚠/✅/🔑 가 사실상 체계적으로 쓰이는데(⭐ 비준·재현 4장, ⚠ 주의 4장, ⛔ 철회 2장) 범례가 앱 어디에도 없다.
5. **화면이 자기 자신과 안 맞는 데가 보인다.** 같은 스크롤 안에서 09-08 카드는 cascade 해제조건이 "남은 것 #3·#4·#7·#8"(4건)이라 하고, 미결 카드 ⏭-2 는 "해제조건 8건 중 ②만 이행 … 나머지 7건 미이행"이라 한다. 처음 온 사람은 어느 쪽이 맞는지 판단할 근거가 없다.
6. **마크다운이 새는 게 눈에 띈다.** `~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ 완료`, `*'축이 얼어 있다'*` 처럼 물결·별표가 그대로 보인다(각각 7군데·28군데). "관리 안 되는 화면" 이라는 첫인상을 준다.

★ 안 본 것을 밝힌다: `/explorer` `/compare` `/cascade` `/files` `/literature` `/seminar` `/notes` `/log` 는 **status code 와 응답 크기만** 확인했고 내용은 안 봤다. 실제 브라우저 렌더(레이아웃·다크모드·모바일·JS 동작)는 못 봤다 — 전부 서버 렌더 HTML 을 텍스트로 읽은 판단이다.

## 건드리면 안 되는 것
- **카드를 db 파일에서 만드는 구조** — data.py `_closure_and_prereg_cards()` · `_nd_anneal_card()`. docstring 이 "⛔ 이 함수가 못 하는 것: … 파일이 없거나 비준 전이면 카드를 만들지 않는다 (빈 카드로 '없음' 을 흉내내지 않는다)" 라고 못 박고, 시험 `test_dashboard_closure_cards_read_db_not_hardcode` 가 db 뿌리를 빈 디렉터리로 바꿔 카드가 **사라지는지** 음성 확인한다. 재편하면서 숫자를 템플릿에 박지 말 것.
- **`key` 가 붙은 카드 3장 — `md_ea_ranking` · `lpsocl_box331_closure` · `ndo_lpscl16_anneal`.** 시험이 제목이 아니라 key 로 집는다(test_webapp.py:675 `cards = [h for h in D.dashboard_highlights() if h.get("key") == "md_ea_ranking"]`, :698). key 를 바꾸거나 카드를 빼면 시험이 깨진다. 제목 문자열로 고르면 오검된다는 사고 기록(2026-08-25 b2o3 카드 오검)도 그 자리에 남아 있다.
- **claim 결속.** `/` 실측 bound 1 · unbound 0 · disclaimed 0 · dangling 0. index.html:26 의 `<div class="card find-card"{% if h.claims %} data-claim="{{ h.claims|join(' ') }}"{% endif %}>` 와 data.py 의 `"claims": ["MD_Ea_eV@b2o3"]` 가 쌍이다. 카드를 접거나 옮겨도 이 속성은 값을 감싼 요소에 그대로 붙어 있어야 한다. 접기 자체는 안전하다 — canonical.py:571 SKIP 이 script/style 뿐이라 `<details>` 안 텍스트도 스캔된다.
- **"못 읽었다" 를 말하는 경로.** index.html:51-59(`sei.unreadable` → "이 표는 **비어 있는 게 아니라 못 그린 것**이다")와 128-134(`sei.v_unreadable` → "빈 것은 값이 없어서가 아니라 못 읽어서다"). 2026-09-07 에 일부러 넣은 것이고(그전엔 절이 통째로 사라졌다), 값 없음을 0 으로 표시하지 않는다는 규율의 실물이다. 절을 재배치하더라도 이 두 분기는 살려 옮길 것.
- **TODO 와 N/A 의 구분** — index.html:176-177 · 199-209 와 data.py NOT_APPLICABLE. 이유가 진척률이 아니라 "금지된 계산을 TODO 로 광고하지 않기" 다(주석에 li3n × ionic = UMA Li₃N 금지 사례까지 적혀 있다). cascade 열을 매트릭스에서 빼더라도 사전 자체와 툴팁 문구는 유지.
- **mdlite 의 볼드 가드 3개** — app.py:80-89 (① 코드 스팬 선격리 ② 300자 상한 ③ 여는 별표 뒤 닫는 문장부호 배제). `globstar(**)` 가 300자 뒤 별표와 짝지어 문장을 통째로 굵게 만든 실측 사고에서 나왔다. 취소선·이탤릭을 추가할 때 이 가드를 우회하거나 순서를 바꾸지 말 것 — 코드 스팬 격리 **뒤** 에 넣는다.
- **base.html 의 접근성·조작 배선.** skip-link(20행), 메뉴 토글의 `aria-expanded` 동기화, rail 접기를 DOMContentLoaded **전** 에 적용하는 FOUC 방지(123행 주석), ⌘K 의 `role=combobox` + `aria-activedescendant` 갱신(_setSel), Esc 우선순위(모달 → figpane → 팔레트). 촘촘하게 맞춰 놓은 것이라 v3 에서 통째로 다시 쓰지 말고 껍데기만 바꿀 것.
- **카드 최신순 정렬 자체** — data.py:4597. "대시보드는 훑는 화면이라 **새로 안 것이 위**에 있어야 한다" 는 1저자 요청(2026-08-20)이고 날짜 없는 카드를 안정 정렬로 뒤에 보내는 처리까지 들어 있다. 축별 묶기를 얹되 묶음 안 정렬은 이대로.
- **카드 본문의 ⛔/⚠ 문장.** 금지 서술·철회 이력이 제목이 아니라 본문(`n`)에 들어 있다 — 예: SDCP 카드의 "⛔ 금지 서술 5종: doped E_ads 수치 일체 · '중성보다 강/약하게 붙는다' …", β 카드의 "⛔ **철회**: `Ea 0.199±0.034` · `0.206` · `0.1732`". 카드를 줄일 때 제목만 남기고 본문을 버리면 금지 서술이 화면에서 사라진다. 접기는 되고, 삭제는 안 된다.
- **`/cascade` 의 archive 게이트** — app.py:344-359. 기본 화면에서 역사 47종 rank 배열을 DOM 에 아예 안 싣고 `?archive=1` 을 요구한다. 대시보드의 "도핑 스크리닝 — 승인된 current ranking 0종" 카드가 그 정책의 짝이다. 재편하면서 순위표를 홈으로 끌어올리지 말 것.

## 발견

### [P0·wrong] nd-gap-mp-citation
- **어디**: `webapp/templates/index.html:117 · webapp/data.py:4050`
- **근거**: 화면이 두 곳에서 지시형으로 틀린 말을 한다. index.html:117 `<b>MP frozen-4f 값을 인용할 것.</b>` · data.py:4050 `"→ **Nd 상 갭은 MP frozen-4f 인용.** 우리 숫자는 인용 금지. "`. 그런데 kb/open_items.md:772 는 `### O. ✅ **Nd 갭 — 3종 자체 측정 완료 (2026-08-12 마감)**` 이고 :783 은 "**MP 인용 우회를 폐기하고 우리 값을 쓴다**" 다. 실제로 같은 표가 이미 우리 값을 그리고 있다 — db/properties/sei_electronic.json 의 `nd2o3_mp-2763_frozen4f` gap 3.9479 · `lindo2_mp-1222355_frozen4f` 3.698 · `nd2s3_mp-438_frozen4f` 0.77 (status 정상). 철회된 건 4f-in-valence 3건(`status: retracted`, gap −6.4598 / −0.0284 / −0.0213)뿐이다. 27일 낡았다.
- **고치는 법**: index.html:117 을 "→ 우리 frozen-4f 값(3.948 / 3.698 / 0.770)을 쓴다. 4f-in-valence 시도 3건은 철회" 로 교체하고, data.py:4050 의 카드 문장도 같이. 그리고 표 행 이름에 `(frozen-4f)` 를 붙여 철회본과 눈으로 갈리게 한다 — 지금은 data.py:1258 `stem = tag.split("_mp")[0]` 때문에 `_frozen4f` 꼬리가 표시명에서 사라진다(대신 mp 칸에 `mp-2763_frozen4f` 라는 없는 MP id 가 찍힌다).
- codex 필요: False

### [P0·useless] highlights-wall
- **어디**: `webapp/templates/index.html:22-37 (데이터: webapp/data.py:3929-4598 dashboard_highlights)`
- **근거**: 카드 41장이 통째로 펼쳐진다. t+v+n 합 26,672자 — 한국어 정독 300자/분이면 89분. 접기·더보기 없음. 최장 카드 n=1,619자("🔴 β 문턱 **0.8 을 폐기한다** — 근거가 없었다"), 최단 카드 전체 80자("comp2 disorder ensemble / d=0.50 anneal+relax 파이프라인 가동 / cfg0 3온도 완료 · 멀티 config 판정 대기"). CSS 에 높이 제한이 없다 — style.css:729 `.find-card .fc-n{font-size:.8rem;color:var(--dim);line-height:1.55; overflow-wrap:anywhere;word-break:break-word}` 에 max-height 도 -webkit-line-clamp 도 없다. `.grid-3` 는 `repeat(auto-fill,minmax(300px,1fr))` 라 한 줄의 모든 카드가 최장 카드 높이로 늘어난다.
- **고치는 법**: 최신 6장만 펼치고 나머지는 `<details>` 로 접는다. 접어도 결속 시험은 안 깨진다 — canonical.py:571 `SKIP = frozenset(("script", "style"))` 라 HTMLParser 가 details 안 텍스트도 그대로 스캔한다(실측 확인). 카드 본문은 **버리지 말고** 접기 안에 그대로 둔다 — ⛔ 금지 서술이 거기 들어 있다.
- codex 필요: False

### [P1·ia] highlights-no-grouping
- **어디**: `webapp/data.py:4597`
- **근거**: 정렬 기준이 날짜 하나다 — `hi.sort(key=lambda c: c.get("d") or "", reverse=True)`. 그 결과 같은 논쟁이 화면 여기저기에 흩어진다. 실측 주제 중복: NEB 12장(idx 11,14,17,18,19,20,21,28,29,34,35,39) · β/게이트 9장(8,9,10,22,25,27,31,35,37) · 유한크기/셀 10장(0,11,12,14,15,18,21,24,29,31) · 본문에 '철회' 가 나오는 카드 10장. 예를 들어 유한크기 논의는 08-18 "상자 크기가 D 를 1.65배 움직인다", 08-27 "유한크기 — modelc 도 같은 방향", 08-27 "🔴 2×2×2 도 똑같이 움직인다" 로 세 장이 따로 떠 있고, 어느 게 현재 판정인지 화면이 안 말한다.
- **고치는 법**: 카드에 축 태그(`axis: "finite-size"|"beta"|"neb"|"gap"|"closure"|"screening"`)를 달고 축별로 묶는다. 묶음 안 정렬은 최신순 유지(1저자 요청 2026-08-20). 축마다 최신 1장만 펼치고 나머지는 접어 "이 축의 이력 N건" 으로.
- codex 필요: False

### [P1·wrong] open-items-count-wrong
- **어디**: `webapp/templates/index.html:40 · webapp/data.py:364-377`
- **근거**: 화면이 `📋 미결 리스트 — 판정·트리거 대기 47건` 이라 쓴다. 실측하면 47건 중 8건이 이미 완료 표시다: `⏭-1. T13 확인 — ✅ **판정 완료 (2026-08-29)**` · `3. ~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ **완료 (2026-07-30)**` · `6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ **완료 (2026-07-29)**` · `7. ~~litdb 인덱스 정합…~~ → ✅ **닫음 (2026-08-06)**` · `10. ~~ELF·그림 계 표시명이 4가지로 갈렸다~~ → ✅ **닫음 (2026-08-06)**` · `O. ✅ **Nd 갭 — 3종 자체 측정 완료 (2026-08-12 마감)**` · `R. ✅ **litdb 인덱스 미편입 5편 …— 닫음 (2026-08-19)**` · `~~M6~~. ✅ cascade 양극 반응성 게이트 — **완료·판정 완료** (2026-08-20)`. 원인은 data.py:371 `if not title.startswith("✅"):` — 닫힌 것을 `## ` **절 단위로만** 거르고 `### ` 항목 단위 완료는 안 본다. 실제 대기는 39건이다.
- **고치는 법**: 항목 제목이 `~~` 로 시작하거나 `✅` 를 포함하면 대기 카운트에서 빼고 "닫힘 8건" 으로 따로 센다. 다만 원장 원문(kb/open_items.md)을 옮길지 화면에서만 접을지는 결정이 필요하다.
- codex 필요: True

### [P1·broken] beta-gate-anchor-dead
- **어디**: `webapp/templates/index.html:14`
- **근거**: `<a href="/glossary#beta-gate">β 문턱 폐기</a>`. /glossary 를 렌더해 id 를 전수하면 13개뿐이고 전부 레이아웃 것이다 — `railbtn, nav-res, nav-run, nav-lit, nav-ref, nav-comps-label, main, gl-empty, cmdk, cmdk-input, cmdk-results, toast, cmdk-opt-…`. `beta-gate` 라는 id 는 없다. glossary.html 에 hash 처리 JS 도 없다(`grep -n "hash\|scrollIntoView" webapp/templates/glossary.html` → 0건). 누르면 152 KB 용어집 맨 위로 떨어지고 β 카드는 스크롤로 찾아야 한다.
- **고치는 법**: `/concept/beta-gate` 로 바꾸면 바로 맞다 — 같은 glossary 페이지가 이미 `<a class="gmore" href="/concept/beta-gate">더보기 — 상세 개념 문서 (유도·수식) →</a>` 를 세 군데서 쓴다.
- codex 필요: False

### [P1·missing] cmdk-pages-missing
- **어디**: `webapp/data.py:3352-3371`
- **근거**: 그 목록 바로 위 주석이 "순서·묶음은 사이드바(base.html)와 같게 — 두 군데가 어긋나면 찾는 사람이 헷갈린다" 인데 실제로 어긋나 있다. 사이드바 항목 21개 vs `/api/search` 의 `t=='페이지'` 항목 15개. 빠진 6개: `/governance`(판정 원장) · `/ledger`(T·Q 원장) · `/fairchem`(Fair-Chem·UMA) · `/seminar` · `/requests`(1저자 요청) · `/sdcp`(SDCP wave1). ⌘K 에 '판정'·'원장'·'governance' 를 쳐도 판정 원장이 안 나온다. 사이드바↔검색 짝을 지키는 테스트도 없다(`grep -n "def test_" webapp/tests/test_webapp.py` 에 sidebar/search 짝 검사 없음).
- **고치는 법**: 6개를 pages 목록에 추가하고, base.html 의 `.nav-links a[href]` 를 긁어 pages 목록과 대조하는 테스트를 하나 붙인다 — 손으로 맞춘 두 목록은 반드시 또 갈라진다.
- codex 필요: False

### [P1·stale] v2-badge-stale
- **어디**: `webapp/templates/index.html:6-14`
- **근거**: 배지 `v2` 와 부제 `<span class="muted"> · v2: <a href="/ledger">T·Q 원장</a> · <a href="/benchmarks">T1b 힘 벤치</a> · <a href="/glossary#beta-gate">β 문턱 폐기</a></span>` — 셋 다 2026-08-26 산출이다(파일 주석도 `v2 (2026-08-26)` 라 적고 있다). 그 뒤 09-03 modelc 갭 재현, 09-07 LPSOCl 마감 조건 비준·Nd₂O₃ 어닐 6셀 회수, 09-08 cascade 보고량 카드 비준·cascade #7 봉인, 커밋 d7d838896 `webapp: 결정 원장을 화면에 올리고 09-07~08 비준·회수분 반영` 이 들어왔는데 부제는 그대로다. 정작 같은 파일 주석이 이걸 경고한다 — "⚠ 판 번호를 올릴 때는 **화면에 실제로 뭐가 늘었는지** 확인하고 올린다 — v2 라고 써 놓고 대시보드가 그대로였던 적이 있다 (2026-08-26 오전)."
- **고치는 법**: 손으로 쓰는 판 번호를 버리고 "최근 변화 3건" 을 highlights 최신 3장(제목 + 날짜 + 해당 카드로 가는 앵커)에서 자동 생성한다. 손으로 쓰는 요약은 반드시 낡는다 — 이미 두 번 낡았다.
- codex 필요: False

### [P1·buried] governance-buried
- **어디**: `webapp/templates/base.html:78 · webapp/templates/index.html (본문 링크 0건)`
- **근거**: 대시보드 본문 링크 전수: `/composition/*` 각 2건(14종) · `/ledger` 1 · `/benchmarks` 1 · `/glossary#beta-gate` 1 · `/methods` 1 · `/compare` 1 · `/todo` 1 · `/api/file/*` 4. `/governance` 는 **0건**이다. 사이드바에서도 마지막 묶음 '자료 · 기록' 의 다섯 번째다. 그런데 그 페이지가 실은 경보판이다 — 렌더하면 "⛔ 인용 위험 원장 — 25건 · citation_hazards.json · 갱신 2026-08-31", "🚨 데이터 위험 유실은 되돌릴 수 없고, 유일본은 매체 하나가 죽으면 유실이 된다. 유실 1건 — A-highT-reseed-traj", "유일본(사본 1) 11건", "⚠ 복제 필요로 표시된 것 9건", "결정 원장 22건" 이 나온다. 되돌릴 수 없는 데이터 유실 경보가 홈에서 링크조차 안 된다.
- **고치는 법**: 유실·유일본·인용위험 세 숫자를 대시보드 최상단 한 줄 배너로 올리고 /governance 로 링크. 그리고 카드 본문의 "결정 원장 D-2026-09-08-lpsocl-box331-closure-conditions" 같은 결정 ID 를 평문에서 링크로 승격(그 ID 들은 /governance 에 실제로 있다 — 렌더 확인).
- codex 필요: False

### [P1·broken] strikethrough-raw
- **어디**: `webapp/app.py:95-140 (_mdlite)`
- **근거**: 렌더된 / 본문에 `~~` 가 7군데 그대로 보인다: `· 3. ~~VGCF 2×2 barrier 행렬 + 기전 판정~~ → ✅ <strong>완료 (2026-07-30)</strong>` · `· 6. ~~LPSOCl COHP 곡선 원자료 회수~~ → ✅ <strong>완료 (2026-07-29)</strong>` · `· ~~M6~~. ✅ cascade 양극 반응성 게이트` · `<td>~~10 meV 선언~~ → <strong>재서 정한다</strong></td>` · `② ~~1.240 Å 자체가 물리인지 미확정이다~~ → <strong>저녁 측정에서 기각.</strong>`. mdlite 는 `**`(_MDL_BOLD) · 백틱(_MDL_CODE) · `==`(_MDL_MARK) · 파이프 표만 승격한다. 바로 직전 커밋 fc3624184 `webapp: 카드·메모의 마크다운이 화면에 기호로 노출되던 것 정정` 이 잡은 것과 정확히 같은 종류인데 `~~` 만 남았다.
- **고치는 법**: 코드-스팬 격리 뒤에 `_MDL_DEL = re.compile(r"~~(?!\s)(.{1,300}?)(?<!\s)~~", re.S)` 를 넣고 `<s>` 로 승격. 이걸 고치면 취소선이 눈에 보이므로 open-items-count-wrong 도 사람 눈에 바로 잡힌다.
- codex 필요: False

### [P2·broken] italic-raw
- **어디**: `webapp/app.py:95-140 (_mdlite)`
- **근거**: 카드 본문에 `*…*` 가 별표째 28군데 나온다: `*'축이 얼어 있다'*` · `*"3주가 비싸서 안 하고 싶은 것과 안 해야 하는 것은 다르다 — 거기를 봐 달라"*` · `*확산 이벤트 수*` · `*'세 계를 같은 5.67 Å 상자에 두는 게 공정하다'*` 등. ⚠ 함정: 09-08 cascade 카드에 `D_rel(design, host) ≡ D*(design) / D*(host)` 가 있어서 순진한 `\*(.+?)\*` 를 넣으면 `*(design) / D*` 가 이탤릭으로 먹힌다(실측으로 확인한 유일 충돌).
- **고치는 법**: 단어경계를 요구한다 — `(?<![\w*])\*(?!\s)([^*\n]{1,120}?)(?<!\s)\*(?![\w*])`. `D*(` 는 여는 별표 앞이 단어문자라 안 걸린다. 새 도구 규율대로 음성 시험에 `D*(design) / D*(host)` 를 픽스처로 넣을 것.
- codex 필요: False

### [P1·missing] first-run-panel-missing
- **어디**: `webapp/templates/index.html:4-22 · webapp/templates/base.html`
- **근거**: `grep -n "처음\|시작하기\|안내\|온보딩\|여기서 시작\|어떻게 읽" webapp/templates/index.html webapp/templates/base.html` → 0건. 처음 온 사람이 읽는 첫 두 덩어리가 h1 밑 부제 한 줄과 카드 1번 "⭐ LPSOCl 3×3×1 닫힘 조건 **비준** — 아레니우스를 하나도 그리기 전에 / 허용차 δEa 0.05 eV · 해상도 0.05 eV" 다. 페이지 상단 버튼도 `▤ Canonical Methods` · `⇄ 비교` 둘뿐이라 "어디 가면 값이 있나 / 뭘 인용하면 안 되나" 로 안 데려간다.
- **고치는 법**: h1 밑에 4칸 패널: ① 정본값 → /explorer·/compare ② 인용 금지·철회·결정 → /governance(인용위험 25건) ③ 용어 → /glossary(33개) ④ 방법 규약 → /methods. 각 칸에 실제 숫자를 db 에서 읽어 넣고, 숫자가 있으면 반드시 링크로 건다.
- codex 필요: False

### [P2·missing] emoji-legend-missing
- **어디**: `webapp/templates/index.html:22-37`
- **근거**: 카드 제목의 표지가 사실상 체계적이다 — ⭐(비준·재현) 4장 · ⚠(주의) 4장 · ⛔(철회) 2장 · 🔑(교훈) 2장 · 🔴(P0) 2장 · ✅ 1장. 그런데 뜻이 어디에도 안 적혀 있다: `grep -rn "범례\|legend\|표지 뜻" webapp/templates/*.html` 은 Plotly 의 `showlegend` 만 걸린다. glossary 33개 용어에도 없다.
- **고치는 법**: 핵심 발견 제목줄 옆에 한 줄 범례. 단 적기 전에 실제 용례부터 확인할 것 — 지금은 규칙이 아니라 관례라서, 범례를 적는 순간 규칙이 되고 새 카드가 그걸 어기면 그때부터 거짓말이 된다.
- codex 필요: False

### [P2·duplicate] comp-links-duplicated
- **어디**: `webapp/templates/index.html:172 · webapp/templates/index.html:191`
- **근거**: 조성 14개가 전부 두 번 링크된다 — Coverage Matrix 행 머리 `<td class="rowh"><a href="/composition/{{ cid }}">` 와 그 아래 family 카드 `<a class="comp-card" href="/composition/{{ cid }}">`. 본문 링크 전수에서 `/composition/comp1` 2건 … `/composition/sdcp` 2건, 예외 없이 전부 2다. 담는 정보도 사실상 같다 — 매트릭스는 ✓/·/— 칸, 카드는 같은 걸 `+N TODO` / `+N N/A` 칩으로 요약한다.
- **고치는 법**: 하나만 남긴다. 매트릭스 쪽이 정보량이 크니 family 카드를 접거나, FAMILY_ORDER 를 매트릭스의 행 그룹 머리로 흡수해 한 표로 합친다.
- codex 필요: False

### [P2·useless] cascade-column-mostly-na
- **어디**: `webapp/data.py:2476-2478 · 렌더 webapp/templates/index.html:164-182`
- **근거**: `for _c in COMPOSITIONS: if _c not in ("modelc_nd_doped", "b2o3"): NOT_APPLICABLE.setdefault((_c, "cascade"), "DFT 심층검증 대상 도핑 히트가 아님")`. 실측하면 Screening·ML 열 14칸 중 12칸이 `—` 이고 ✓ 는 Nd₂O₃-LPSCl · B₂O₃-LPSCl 둘뿐, TODO 는 0 이다. 커버리지 통계의 N/A 18칸 중 12칸이 이 한 열 — 매트릭스의 '해당 없음' 이 거의 이 열 하나다. (분모 효과는 작다: 열을 빼면 65/80=81% → 63/78=81%.)
- **고치는 법**: cascade 는 조성별 물성이 아니라 47종 스크리닝 캠페인이다 — 열에서 빼고 매트릭스 위에 "도핑 스크리닝은 별도 축 → /cascade (승인된 current ranking 0종)" 한 줄 배너로. NOT_APPLICABLE 사전 자체는 건드리지 말 것(다른 조합이 거기 걸려 있다).
- codex 필요: False

### [P2·stale] open-items-header-stale
- **어디**: `webapp/templates/index.html:44 (원문 kb/open_items.md:6)`
- **근거**: 미결 첫 카드 제목이 `⏭ 다음 세션이 **바로 이어서 할 것** (2026-08-28 등록 · **최종 갱신 2026-08-31**)`. 오늘 09-08 인데 그 절에 09-07~08 것이 하나도 없다(LPSOCl 마감 비준 · cascade 보고량 카드 비준 · cascade #7 봉인 · Nd 어닐 6셀 · QE-GPU 런타임 ldd 규율). 게다가 같은 화면 안에서 충돌한다 — ⏭-2 는 `해제조건 8건 중 ②(anneal seed 고정)만 이행(34a400e9), 나머지 7건 미이행 (2026-08-31 갱신)` 이라 하고, 그 위 09-08 카드는 `남은 해제조건: #3(전 시드 end-to-end 재실행) · #4(label-blind v2 동결) · #7(builder·런처·manifest·게이트 규칙 봉인) · #8(39 밖 sentinel 파일럿)` 이라 한다.
- **고치는 법**: 본체는 kb/open_items.md 갱신이라 화면에서 못 고친다. 대시보드 쪽 대응은 하나 — 절 제목의 `최종 갱신 YYYY-MM-DD` 를 파싱해 7일 넘게 낡으면 카드에 경고 배지를 붙인다. 화면이 낡음을 감추는 대신 낡았다고 말하게.
- codex 필요: False

### [P2·useless] stat-grid-not-actionable
- **어디**: `webapp/templates/index.html:146-153`
- **근거**: 네 칸이 `14 / 조성 · 프로젝트`, `188 / post-processing 파일`, `218 / litdb 문헌`, `81% / 커버리지 · 65/80`. "188 post-processing 파일" 은 처음 온 사람에게 아무 뜻이 없고, 넷 다 클릭이 안 된다 — 대시보드 본문 링크 전수에 `/literature` 도 `/explorer` 도 0건이다. 게다가 커버리지 매트릭스를 먹이는 `index_metrics` 는 db/_index.json 스냅샷에서 오는데(data.py:2322 `"built": idx.get("built")`), 그 파일의 `built` 가 `2026-06-02T13:45:00` 이다. 조성 페이지는 그 사실을 밝힌다(composition.html:185 "⚠ 출처 = db/_index.json 스냅샷 (2026-06-02 생성)") — 대시보드만 안 밝히고 부제에서 "db/ 실시간 동기화" 라고 쓴다.
- **고치는 법**: 네 칸을 갈 데가 있는 숫자로 교체 — 정본값 N건→/explorer · 인용 위험 25건→/governance · 미결 39건→/todo · 문헌 218→/literature. 그리고 매트릭스 밑에 조성 페이지와 같은 스냅샷 날짜 한 줄을 넣거나, 부제의 "실시간 동기화" 를 실제 범위에 맞게 좁힌다.
- codex 필요: False

### [P2·ia] sidebar-comps-flat
- **어디**: `webapp/templates/base.html:87-93`
- **근거**: 사이드바 Compositions 는 14개 평면 목록이다 — `{% for cid, c in COMPS.items() %}` 로 family 구분도, 구분선도 없다. 같은 것을 대시보드는 5개 family 로 묶는다(index.html:184 `{% for fam in FAMILY_ORDER %}` → Argyrodite / Doped / Anode / Interphase / Molecular). 그리고 평면 목록이라 `Cl-rich LPSCl1.6` 과 `Cl-rich LPSCl1.6 v3` 가 바로 붙어 있어 눈으로 안 갈린다.
- **고치는 법**: 사이드바도 FAMILY_ORDER 로 묶고 argyrodite 6개는 기본 접힘. 대시보드와 같은 묶음·같은 순서를 쓰는 게 규칙이어야 한다(⌘K pages 목록도 마찬가지 — cmdk-pages-missing 과 한 번에 고칠 것).
- codex 필요: False

### [P2·ia] sei-section-oversized
- **어디**: `webapp/templates/index.html:61-144`
- **근거**: SEI 분해상 절이 축 카드 3장 + 9행 6열 표 + 제외 3종 캡션 + 참조계 줄 + note 2개 + 파일 버튼 4개로 대시보드 세로의 큰 덩어리를 먹는다. 캠페인 날짜는 2026-08-07 이고 상태는 축 ② ③ "완료", 축 ① 은 `DFT CI-NEB — 요청 6종 중 값 나온 것 2/6 · 셀 수렴 확인 0/6 (인용 가능)` 이다(진행이 한 달째 2/6). 반대로 09-07~08 에 비준된 마감 계약·보고량 카드는 41장 중 두 장으로만 있고 전용 자리가 없다. 최신·중요한 것이 앞이라는 목표와 어긋난다.
- **고치는 법**: SEI 는 캠페인 페이지(또는 조성 계열)로 옮기고 대시보드엔 요약 한 줄 + 링크만. 그 자리에 "지금 살아 있는 계약 — 마감 조건 · 보고량 카드 · 재개 조건" 절을 넣는다(db/properties/*_closed_*.json · *_estimand_*.json 에서 자동 생성 — 이미 _closure_and_prereg_cards 가 그 일을 한다).
- codex 필요: False
