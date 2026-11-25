# webapp — 문헌 (/literature · /api/paper/<pid> · /talk/<slug> · litdb/)

## 지금 무엇인가
litdb 는 논문 1편 = digest 1개(litdb/papers/*.md, 219 파일)로 굴러가는 문헌 시스템이고, 그 위에 사람이 손으로 쓴 큐레이션 층이 셋 더 있다 — INDEX.md(MUST-READ 계층 + 22개 주제 섹션), comparison_vs_ours.md(물성축 A–L, 1281줄), our_dft_baseline.md(비교 기준값). 웹앱 /literature 는 그 중 **digest 파일 목록 하나만** 읽어 222장(논문 215 + 발표덱 7)의 카드를 알파벳순 평면 그리드로 깔고, 카드를 누르면 /api/paper/<pid> 가 digest 를 통째로 렌더해 모달에 넣는다. 그림 크로핑(179편 · 캡션 검색 · 여백 메모)은 실제로 잘 붙어 있고 렌더도 깨끗하다.

## 처음 오는 사람
처음 온 사람은 "Literature"를 눌러 899 KB 짜리 한 페이지를 받는다. 맨 위에 보이는 것은 숫자 세 개(215 / 98 / 117)와 칩 15개(연구책임자 10 · 주제 3 + 전체 + 즐겨찾기), 그리고 칩보다 긴 주의문 두 덩이다. 화면이 답해 주지 않는 질문이 이것들이다 — **이게 뭘 모은 것인가**(왜 215편인가, 무슨 기준으로 들어왔나), **뭘 먼저 읽어야 하나**(INDEX.md 에 "📌⭐ MUST-READ" 계층이 실제로 있는데 화면엔 없다), **우리 것은 어디 있나**(우리 원고 2편이 외부 논문 213편 사이에 아무 표시 없이 섞여 있다 — ahn2026 은 index 1, 제목 안 저자명 "An" 이 색으로 칠해진 게 유일한 단서다), **이걸 읽고 뭘 하나**(문헌↔우리 대조는 comparison_vs_ours.md 에 A–L 축으로 다 정리돼 있는데 그 파일은 웹앱 어디에서도 열리지 않는다 · /api/file 로도 404).

그리고 "digest" 라는 낱말을 화면이 설명 없이 세 번 쓴다(부제 · 정렬 버튼 · 카드 날짜 툴팁). 카드를 하나 열면 58~63 KB 짜리 문서가 모달에 통째로 들어오고, 이게 훑기용인지 정독용인지 화면이 말하지 않는다 — 발표덱에는 "📖 전체 페이지로 정독" 버튼이 있는데 논문 215편에는 그 버튼도, 그에 해당하는 라우트(/paper/<slug>)도 없다.

정렬은 슬러그 알파벳순이다. 그래서 방금 들어온 두 편이 qian2025 → 149번째, wu2026 → 198번째에 박혀 있다. "📅 최신 digest순" 토글이 있긴 한데 기본값이 아니라, 처음 온 사람은 새 게 뭔지 영원히 모른다. 학회 발표덱 7건은 페이지 바이트의 97 % 지점(871521/899637)에 있고, 트랙 탭이 전체/DFT/DEM 셋뿐이라 발표덱만 골라 보는 방법 자체가 없다.

한 문장으로: **지식 허브의 "지식"에 해당하는 층(무엇이 중요한가 · 문헌이 우리와 어떻게 다른가 · 무엇을 인용하면 안 되는가)은 전부 litdb 파일 안에 살아 있고, 화면에는 파일 목록만 나온다.**

## 건드리면 안 되는 것
- **digest 본문 그 자체 (litdb/papers/*.md 219개)** — 이게 이 영역의 전 재산이다. qian2025 62796 B · wu2026_ta 63632 B 급의 정독 digest 는 §0 '이 digest 를 읽는 법' 부터 §7 우리 대비, ⛔ 인용금지 목록까지 층이 잡혀 있다. 줄이거나 요약본으로 갈아치우지 말 것 — v3 재편은 **찾는 길**을 고치는 것이지 문서를 깎는 게 아니다.
- **그림 크로핑 파이프라인 전체** (litdb/figures/<slug>/ 179폴더 + figures.json + figref.js + docnote.js). 무결성 실측 결과 figures.json 없는 폴더 0 · 참조하는데 없는 파일 0 · digest 없는 그림폴더 4개는 전부 talks/ 라 정상. 카드의 `🔍 캡션` / `💬 코멘트` 배지, F 단축키 그림점프, 여백 메모 앵커도 손대지 말 것. 페이지 무게를 줄일 때도 **잘라낸 PNG 와 캡션 데이터는 그대로 두고 색인 전달 방식만** 바꾼다.
- **발표덱 인용등급 경고**(literature.html:128-134 callout: "발표 덱은 위 논문 수에 합산하지 않는다 … 소환값보다 한 단계 낮은 신뢰 등급 … 덱은 부재의 증거가 아니므로")와 /talk/<slug> 의 manifest 배지 로직(app.py:1113-1121, manifest 없으면 '없다고 말한다'). 발표덱을 위로 올리더라도 이 경고는 그 묶음에 **붙어서** 같이 움직여야 한다.
- **litdb/topics.json 의 손 큐레이션 13항목**(gloss 13 · caution 9)과 `_primer`(계산 스크리닝 3분 입문). 지금 gloss/caution 이 화면에 안 나오는 게 문제지 내용이 문제가 아니다 — 칩을 정리하더라도 json 의 산문은 지우지 말고 렌더처를 만든다.
- **comparison_vs_ours.md 의 §H '우리가 아직 못 하는 것(정직 목록)' · §I '출처 재귀속' · §J-6 '이 축에서 인용하면 안 되는 것' · §L-0 '이 축을 여는 규율'** — 전부 반론·한계 절이라 kb 규율상 삭제 금지 대상이다. 화면으로 끌어올릴 때 요약하지 말고 통째로 렌더한다.
- **data.py:3196 의 `__seminar` 제외 규칙**과 그 근거 주석("digest 로 세면 인덱스 정합 점검이 '미등재 digest' 오탐을 낸다"). 카운트 불일치를 고칠 때 이 쪽을 218 로 맞추는 게 아니라 **대시보드를 215 로** 내려야 한다.
- **정렬 토글의 tie-breaker**(literature.html:214 `(b.digested).localeCompare(a.digested) || a.dataset.t.localeCompare(b.dataset.t)`) — digest 날짜가 없는 2편(bzox_dry_zro2x_… · hollmann2025_tabpfn_…)이 조용히 사라지지 않게 잡아 주는 장치다. 기본 정렬을 날짜순으로 바꿔도 이 폴백은 유지한다.
- **litdb/_INDEX_proposals.md 의 '⛔ 여기서 INDEX.md 로 옮기는 것은 사람이 한다' 규율.** 뼈대 5편을 화면에서 접더라도 자동 승격 장치를 만들지 말 것 — 그 파일이 명시적으로 금지한 것이다.

## 발견

### [P0·wrong] lit-count-218-vs-215
- **어디**: `webapp/data.py:2328 ↔ webapp/templates/literature.html:6`
- **근거**: 대시보드 실측 218 (`<div class="num">218</div><div class="lbl">litdb 문헌</div>`), /literature 실측 215 (`litdb · 215편`). data.py:2326 주석은 정반대를 주장한다 — "⚠ list_papers() 와 같은 정의를 써야 대시보드 카운트와 /literature 목록이 안 어긋난다 (예전엔 _TEMPLATE.md 를 세서 106 vs 105 로 갈렸음)". 실제 차이 3편은 `__seminar` 동반대본이다: deng2026_…__seminar_5min_qa · kim2025_…__seminar_5min_qa · tu2026_…__seminar_5min_qa. list_papers 는 data.py:3196 에서 `if "__seminar" in f.stem: continue` 로 빼는데 literature_count 는 `f.stem.startswith("_")` 만 본다.
- **고치는 법**: literature_count 를 `len(list_papers())` 로 바꾼다(정의를 두 번 쓰지 말고 한 번 계산해 나눈다). 주석이 주장하는 불변식을 실제로 성립시키는 것이고, 덤으로 대시보드 숫자를 /literature 로 링크한다.
- codex 필요: False

### [P0·buried] comparison-vs-ours-invisible
- **어디**: `litdb/comparison_vs_ours.md (1281줄) · litdb/INDEX.md · litdb/our_dft_baseline.md — webapp 참조 0건`
- **근거**: `grep -rn "comparison_vs_ours|INDEX.md|our_dft_baseline" webapp/*.py webapp/templates/*.html` → 출력 없음. /api/file 로도 못 연다: `/api/file/litdb/comparison_vs_ours.md` → **404** (허용 뿌리가 docs·db·litdb/figures 뿐, app.py:566 주석). 그 안에 든 것: §A 이온전도 ~ §L 까지 12축, §G "우리 계산이 문헌을 검증하는 지점", §H "우리가 아직 못 하는 것(정직 목록)", §J-6 "이 축에서 인용하면 안 되는 것", 그리고 **§L 자기감사 축 — 우리 CEJ 투고본 (2026-09-07 신설)** 의 P0 2건("P0-1 Fig. 5d 가 Li₃N 을 실선 연속 MEP 로 그리고… 계산한 Li₃N 점은 2개뿐", "P0-2 Methods §4.6 이 LiC₆ 를 'CI-NEB + UMA-oc20' 로만 기술하고 QE 단일점 단계를 빠뜨렸다 … 그 경로 단독 우리 값은 0.241 eV 이지 0.290 이 아니다"). 이 P0 2건이 /todo · /governance · / 어디에도 안 나온다(문자열 검색 전부 False). INDEX.md 의 "## 📌⭐ MUST-READ (최상위 우선 — 분야 전체 field-map)" 계층도 화면에 없다.
- **고치는 법**: v3 에서 /literature 를 두 층으로 나눈다 — 위는 **축별 대조**(comparison_vs_ours.md §A–L 를 렌더한 라우트, 예: /literature/axes), 아래가 카드 그리드. 최소한 safe_repo_path 허용 뿌리에 `litdb/`(md 만) 를 넣어 /api/file 로 열리게 하고, INDEX.md 의 MUST-READ 슬러그를 /literature 최상단 "먼저 읽을 것" 줄로 올린다. §L 은 문헌이 아니라 우리 원고 감사이므로 /literature 가 아니라 /todo·/governance 로 보내는 게 맞다.
- codex 필요: False

### [P0·useless] skeleton-cards-placeholder
- **어디**: `webapp/templates/literature.html:96 (.ptype) — 대상 5편, 예: litdb/papers/liu2026_planar_li_deposition_dissolution_enable_practical.md:6`
- **근거**: 카드 5장이 type 칩에 플레이스홀더 원문을 그대로 띄운다: `⏳ 문서 대기 (exp|DFT|AIMD|MLIP|DEM|MPM|FEM|mixed)` — ketter2025 · kissel2026 · liu2026_planar · **unknown2025**_revealing_neglected_role_passivation_layers_current · wang2026_domain_oriented. 파일 첫 줄에 인용금지가 박혀 있다: `<!-- 🌱 research-agent 가 만든 **뼈대**다. … ⛔ '⏳ 문서 대기' 가 하나라도 남아 있으면 이 카드를 **인용하지 않는다**. -->`. 그런데 화면에서는 62796 바이트짜리 정독 digest(qian2025)와 4584 바이트짜리 뼈대가 **똑같이 생긴 카드**다. 게다가 이 5편은 215편 카운트와 DFT/DEM 탭 숫자에도 그대로 들어간다(track: dft 4 · dem 1 — 파이프 안에 DFT/DEM 이 둘 다 있어 분류가 사실상 임의다).
- **고치는 법**: digest 본문의 `status 🌱 skeleton (문서 대기)` 를 읽어 카드에 `🌱 뼈대 · 인용금지` 배지를 달고 기본 그리드에서 접는다(별도 "채울 것 5" 묶음). type 칩은 플레이스홀더면 렌더하지 않는다. 헤드라인 카운트는 완성 digest 만 세고 뼈대는 옆에 따로 적는다.
- codex 필요: False

### [P0·missing] citation-ban-not-on-card
- **어디**: `webapp/templates/literature.html:80-107 (카드 배지 영역)`
- **근거**: `grep -rl "인용 금지|인용금지" litdb/papers/*.md | wc -l` → **80** / 219. 실제 문구 예(litdb/INDEX.md:15 [Liu24SbO] 행): "⚠ **ε_p 0.51 eV 정량 인용 금지**", tu2026 digest: "**⛔ 인용금지**: D·Ea·σ 절대값 전부 · '21 후보' · … 우리 LODO 와 병치". 카드에는 이런 표시가 하나도 없다 — 배지는 `🔍 캡션` · `💬 코멘트` · `🖼 N` 셋뿐이고 전부 **검색 결과 표시용**이지 인용 지위가 아니다. 즉 어떤 논문이 인용 제한을 달고 있는지 알려면 58 KB digest 를 열어 읽어야 한다. db 쪽은 이미 db/properties/citation_hazards.json 로 원장이 있고 /governance 에 올라와 있는데(templates/governance.html:9), 문헌 쪽에는 같은 장치가 없다.
- **고치는 법**: digest 에서 `⛔ 인용금지`/`인용 금지` 블록을 파싱해 카드에 `⛔ 인용제한` 배지 + 툴팁(무엇이 금지인지 첫 줄)을 달고, 그것만 거르는 칩을 하나 둔다. 파서는 이미 있는 type/digested 파서(data.py:3204-3213) 옆에 붙이면 된다.
- codex 필요: False

### [P1·stale] index-header-stale
- **어디**: `litdb/INDEX.md:6, litdb/INDEX.md:8`
- **근거**: 6행: "두 인덱스 어디에도 없는 digest 는 … `--check` 로 잡는다 (**2026-08-06 기준 0편** — open_items #7 해결)". 지금 `python3 tools/litdb/build_index.py --check` 실물 출력: "=== 정합 점검: digest 215편 · **어느 인덱스에도 없는 것 5편**" (ketter2025 · kissel2026 · liu2026_planar · unknown2025 · wang2026_domain_oriented). 8행: "자동 생성 from Excel (`dbce603a`). **갱신: 2026-06-23**" — 이 파일의 마지막 커밋은 2026-09-08(66d5a3f3f)이다.
- **고치는 법**: 머리말의 '0편' 을 지우고 --check 를 돌려 나온 수를 쓰거나, 아예 숫자를 빼고 "--check 로 확인" 만 남긴다. '갱신: 2026-06-23' 은 build_index.py 가 쓰게 하거나 삭제한다(사람이 손으로 못 따라간다는 게 증명됐다).
- codex 필요: False

### [P1·wrong] comparison-header-wrong
- **어디**: `litdb/comparison_vs_ours.md:10`
- **근거**: 10행: "**현재: DFT 트랙 64/64 편입 (2026-08-06).**" — 완전편입을 주장한다. `--check` 실물: "DFT  **94/98**  → comparison_vs_ours.md   미편입 4편" + "DEM  **46/117** → comparison_vs_ours_DEM.md   미편입 71편". 분모(64→98)도 분자도 틀렸고, '전부 들어왔다' 는 상태 주장이 사실이 아니다.
- **고치는 법**: 머리말에서 편입률 숫자를 빼고 --check 가 출력하는 값을 참조하게 한다(같은 실수를 세 번 하는 자리다). DEM 46/117 은 별도 미결 항목으로 세운다 — 71편 미편입은 머리말 한 줄로 감출 크기가 아니다.
- codex 필요: False

### [P1·ia] default-sort-alphabetical
- **어디**: `webapp/data.py:3191 (`for f in sorted(pd.glob("*.md")):`) · webapp/templates/literature.html:13 (정렬 토글)`
- **근거**: 기본 정렬이 슬러그 알파벳순이다. 실측 위치: `qian2025_lipo2f2_coating_stable_cei` = **148번째**(digested 2026-09-08), `wu2026_dilute_electrolyte_zn_calendar_aging` = **197번째**(digested 2026-09-08), 215편 중. '📅 최신 digest순' 버튼은 있지만 `sortMode=false` 로 시작하고 localStorage 로 기억하지도 않는다. digest 날짜는 215편 중 213편이 있다(없는 2편: bzox_dry_zro2x_… · hollmann2025_tabpfn_…).
- **고치는 법**: 기본 정렬을 digested 내림차순으로 바꾸고, 토글을 '가나다순' 쪽으로 뒤집는다. 그리고 최근 30일 안에 들어온 것은 상단에 `🆕 이번 주 새로 들어온 것 N편` 스트립으로 따로 뽑는다 — 목표("최신·중요한 것이 앞")를 정렬만으로는 못 채운다.
- codex 필요: False

### [P1·buried] talks-buried-no-tab
- **어디**: `webapp/templates/literature.html:127 (`🎤 학회 발표자료`) · :9-13 (track-tabs)`
- **근거**: 렌더 HTML 실측: 첫 카드가 15813 바이트 지점, `학회 발표자료` 제목이 **871521** 바이트 지점(전체 899637 = 97 %). 그 앞에 카드 215장이 있다. 트랙 탭은 `data-track` 값 `all/dft/dem` 셋뿐인데 발표덱 카드는 `data-track="talk"` 7장이다 — 필터 로직 `okT = curTrack==='all' || c.dataset.track===curTrack` 이라 **DFT 나 DEM 을 누르면 발표덱은 사라지고, 발표덱만 보는 탭은 존재하지 않는다.** 즉 '전체' 에서 끝까지 스크롤하는 것이 유일한 접근 경로다.
- **고치는 법**: `🎤 발표덱 7` 탭을 track-tabs 에 추가하고, 발표덱 묶음을 논문 그리드 **위**(혹은 접힌 섹션)로 올린다. 인용등급 경고 callout 은 그 묶음 안에 붙여 유지한다.
- codex 필요: False

### [P1·broken] talk-search-anchor-404
- **어디**: `webapp/data.py:3350`
- **근거**: ⌘K 전역 검색이 발표덱을 `f"/literature#{t_['id']}"` 로 건다. 그런데 렌더된 페이지에 그 id 가 없다 — 실측: `id="do2026_bml_alzib_preconditioning"` **False**, `data-id="do2026_bml_alzib_preconditioning"` 도 **False**(발표덱 카드에는 data-id 자체가 없다, literature.html:139-141). 논문은 같은 인덱스에서 `f"/literature?open={p['id']}"` 를 쓰고 이건 실제로 동작한다(literature.html:349 의 ?open= 자동열기). 결과: 검색에서 발표덱을 고르면 899 KB 페이지 맨 위로 떨어지고 아무 일도 안 일어난다.
- **고치는 법**: 3350행을 논문과 같은 `?open=` 로 통일한다(모달 openPaper 는 talks/ 폴백이 이미 있다 — app.py:1080). 한 글자짜리 수정이다.
- codex 필요: False

### [P1·useless] gloss-caution-dead-path
- **어디**: `webapp/data.py:3153-3159 · 3220-3221 → webapp/templates/literature.html (소비처 없음)`
- **근거**: `paper_topics()` 가 `gloss`·`caution` 을 돌려주고 `list_papers()` 가 매 카드 dict 에 실어 라우트까지 넘긴다. 그런데 `grep -rn "\.gloss|\.caution" webapp/templates/` → **출력 없음**. litdb/topics.json 실측: 항목 13개 중 **gloss 13개 · caution 9개**가 손으로 쓰여 있는데 화면에 단 한 글자도 안 나온다. 즉 사람이 쓴 큐레이션 22줄이 계산돼서 버려진다.
- **고치는 법**: 카드 툴팁이나 모달 머리에 gloss 한 줄 + caution 을 노란 줄로 띄운다. 렌더 안 할 거면 data.py 에서 계산을 빼고 topics.json 의 그 필드를 정리한다 — 둘 중 하나는 해야 한다.
- codex 필요: False

### [P1·missing] no-paper-fullpage-route
- **어디**: `webapp/app.py:1099 (talk_page docstring) ↔ 라우트 목록에 /paper/<slug> 없음`
- **근거**: /talk/<slug> 는 있고 그 존재 이유를 스스로 이렇게 적는다 — "왜 별도 라우트인가: /literature 의 모달은 훑기용이라 **40 KB 넘는 digest 를 읽기 어렵다**". 그런데 논문 digest 는 그보다 크다: /api/paper 실측 html 크기 qian2025 **58101 B** · wu2026_ta **63632 B**. 라우트 전수(url_map)에 `/paper/…` 는 없다. 발표덱 7건에는 '📖 전체 페이지로 정독' 버튼(literature.html:158)이 있고 논문 215편에는 없다.
- **고치는 법**: /talk/<slug> 를 그대로 복제한 /paper/<slug> 를 판다(doc.html + toc + parent=/literature). 카드/모달에 같은 '📖 전체 페이지' 버튼을 달면 목차·형광펜·여백메모가 정독 모드에서 살아난다.
- codex 필요: False

### [P1·broken] litdb-dead-paths
- **어디**: `litdb/README.md:12,25,32 · litdb/INDEX.md:8 · litdb/comparison_vs_ours_DEM.md:3 · litdb/INDEX_DEM_snapshot_2026-07-16.md:3,5`
- **근거**: 존재하지 않는 경로를 정본처럼 가리킨다. 실측: `litdb/properties` **없음**(README:12 "| `properties/*.md` | 물성별 교차표 (ionic / oxidation / mechanical / electronic) |", README:25 "`comparison_vs_ours.md` · `properties/` 갱신", INDEX.md:8 "물성 교차표는 `properties/`"). `litdb/our_dem_baseline.md` **없음**(comparison_vs_ours_DEM.md:3 "기준값: `our_dem_baseline.md`" — DEM 비교문서 전체의 기준값 파일이다). `docs/literature_review_dem_mpm_assb.md` **없음**(INDEX_DEM_snapshot:3 "★ **종합 리뷰(60편)** = …").
- **고치는 법**: 세 경로를 실물로 교체하거나(그 내용이 어디로 갔는지 찾아 링크) 문장을 지운다. our_dem_baseline.md 는 DEM 비교의 기준선이라 '없음' 인 채로 두면 §C·§F 의 모든 대조가 근거 없는 상태가 된다 — 여기만은 어디로 갔는지 확인이 필요하다.
- codex 필요: True

### [P1·ia] our-own-papers-unmarked
- **어디**: `webapp/templates/literature.html:80-107 · litdb/INDEX.md:412 (`## 🧪 자체·공저 논문`)`
- **근거**: 우리 논문 2편이 외부 213편과 구분 없이 섞여 있다 — `ahn2026_cej_agno3_pvp_li3n_anodefree`(index **1**/215, digested 2026-09-07, INDEX.md 표기 "**[자체·공저·⚠미출판 투고본]** … **Yonghoon An (DFT 담당)**")와 `lee2026_mechanical_halogen_argyrodite_drycoating`(INDEX.md "**[자체·공저]** … **Yonghoon An (제2저자 = 계산 담당)**", ACS Nano 2026). 카드가 주는 유일한 단서는 제목 안 `**An**` 이 색으로 칠해진 것뿐이고, 미출판 투고본이라는 사실도 화면에 없다. INDEX.md 에는 `## 🧪 자체·공저 논문 (2026-08-19 추가)` 섹션이 이미 있다.
- **고치는 법**: PI 칩 옆에 `🏠 우리 논문` 칩을 하나 만들고(litdb 표기 `[자체·공저]` 파싱), 카드에 `자체·공저` + 미출판이면 `⚠ 투고본` 배지를 단다. 지식 허브의 첫 화면에서 '우리 것' 을 못 고르는 것은 구조 문제다.
- codex 필요: False

### [P2·useless] topic-chips-thin
- **어디**: `webapp/templates/literature.html:38-52 · litdb/topics.json`
- **근거**: 주제 칩이 세 개뿐이고 덮는 논문이 **13/215 (6 %)** 다 — 실측 tcounts `{'DFT-screening': 8, 'exp-screening': 1, 'descriptor': 7}`, 태그 없는 논문 **202편**. `exp-screening` 은 논문 **1편**짜리 필터다. 그런데 그 칩 줄 아래에 5줄짜리 설명문("⚠ 주제 태그는 손으로 큐레이션한다 … 그래도 본문 전수는 아니라('screening' 제목 7편 vs 본문 13편) 태그를 따로 둔다")과 접힌 3분 입문서가 붙어, 첫 화면 chrome 8482 바이트 중 상당 부분을 6 % 를 위한 장치가 쓴다.
- **고치는 법**: n<3 인 칩은 숨긴다(exp-screening). 주제축은 INDEX.md 가 이미 22개 섹션으로 나눠 놨으니 topics.json 을 손으로 늘리기보다 INDEX 섹션명을 주제로 승격하는 쪽이 싸다. 5줄 설명은 칩 옆 ⓘ 툴팁으로 접는다.
- codex 필요: False

### [P2·ia] single-page-899kb
- **어디**: `webapp/templates/literature.html:73-125 (전체 papers 루프) · webapp/data.py:5280 (paper_figure_search)`
- **근거**: /literature 실측 **899637 바이트**, 카드 222장을 한 번에 렌더한다(페이지네이션·가상스크롤 없음). 무게 내역 실측: `data-fig` 174개 = **278788 B**, `data-t` 222개 = 52495 B, `data-cmt` 5개 = 20094 B, 스크립트 15134 B. 캡션 색인 docstring(data.py:5285)은 "캡션당 앞 110자만 (전체를 넣으면 300 KB+)" 라고 쓰지만 **잘라낸 지금도 279 KB** 다 — 주석이 말하는 절약이 실제로는 안 일어난다(9000자 상한에 걸린 논문은 0편이라 잘림 손실도 없다).
- **고치는 법**: 검색 색인을 DOM 속성에서 빼고 `/api/lit-search?q=` 서버 검색이나 별도 JSON(캐시 가능)으로 옮긴다. 그러면 페이지가 ~600 KB 줄고 캡션 110자 상한도 풀 수 있다. data.py:5285 주석은 실측치로 고친다.
- codex 필요: False

### [P2·duplicate] index-dem-snapshot-duplicate
- **어디**: `litdb/INDEX_DEM_snapshot_2026-07-16.md (239줄) ↔ litdb/INDEX_DEM.md`
- **근거**: 같은 DEM 인덱스가 둘이다. 스냅샷은 2026-07-16 커밋 이후 손대지 않았고(마지막 커밋 2026-07-16), 머리말이 "> 갱신: 2026-07-16 …" 로 시작하며 존재하지 않는 파일 두 개(`our_dem_baseline.md` · `docs/literature_review_dem_mpm_assb.md`)를 가리킨다. 현행 INDEX_DEM.md 는 `tools/litdb/build_index.py` 자동생성이라 성격도 다르다. 어느 쪽이 정본인지 파일 안에 적혀 있지 않다.
- **고치는 법**: 스냅샷 머리에 `⛔ 동결본 — 정본은 INDEX_DEM.md` 한 줄을 박거나 litdb/_archive/ 로 옮긴다. 파일명에 날짜가 있는 것만으로는 '옛것' 이라는 신호가 약하다.
- codex 필요: False

### [P2·broken] template-served-200
- **어디**: `webapp/app.py:1078 (api_paper)`
- **근거**: `/api/paper/_TEMPLATE` → **200** (3842 바이트). list_papers 는 data.py:3192 에서 `_` 접두를 빼는데 API 는 안 뺀다. 목록에 안 보이는 파일이 URL 로는 열린다 — 빈 서식이라 해로울 건 없지만, 링크가 새면 '빈 digest' 로 보인다.
- **고치는 법**: api_paper 에 `if pid.startswith('_'): abort(404)` 한 줄. /talk/<slug> 는 이미 `slug.startswith("_")` 를 막고 있다(app.py:1112) — 같은 가드를 맞춘다.
- codex 필요: False

### [P2·wrong] title-block-says-dft
- **어디**: `webapp/templates/literature.html:2`
- **근거**: `{% block title %}Literature · DFT{% endblock %}` — 브라우저 탭·북마크 이름이 'Literature · DFT' 다. 실제 구성은 DFT 98 · **DEM 117** 로 DEM 이 다수(54 %)이고, 같은 페이지 부제는 두 축을 대등하게 적는다("**DFT·MLIP**(전해질 화학) ↔ **DEM·MPM**(미세구조·역학)").
- **고치는 법**: 'Literature · litdb' 로 바꾼다. 탭 이름이 축 하나를 대표하면 다른 축을 찾는 사람이 이 페이지를 지나친다.
- codex 필요: False

### [P2·duplicate] nd-survey-split-from-literature
- **어디**: `webapp/app.py:793 (/nd-survey) · webapp/data.py:3065 ↔ litdb/surveys/nd_substitution_54papers_2026-07.md (9534줄)`
- **근거**: 문헌 서베이가 사이드바에 별도 항목으로 떨어져 있다(base.html:69 '🧬 Nd 치환 서베이'). 화면이 읽는 것은 `db/properties/nd_substitution_survey_index.json` 이고, 그 JSON 이 스스로 `"source_md": "litdb/surveys/nd_substitution_54papers_2026-07.md"` 를 가리킨다. 화면은 그 경로를 **링크 없는 mono 텍스트**로만 찍는다(`원문 <span class="mono">litdb/surveys/…</span>`) — /api/file 이 litdb/*.md 를 404 로 막으므로 링크로 만들 수도 없다. litdb/surveys 에는 다른 한 편(md_structure_setup_halogen_rich_2026-07.md)도 있는데 웹앱 어디에도 안 나온다.
- **고치는 법**: 서베이류를 /literature 안의 한 묶음(`📚 서베이 2`)으로 끌어오고, JSON 인덱스가 있는 것은 그 뷰로, 없는 것은 md 렌더로 연다. litdb/*.md 를 /api/file 허용에 추가하는 것이 선행조건이다(위 comparison-vs-ours-invisible 과 같은 처방).
- codex 필요: False

### [P2·stale] notion-leftover-in-survey
- **어디**: `litdb/surveys/nd_substitution_54papers_2026-07.md:10`
- **근거**: "- 각 논문 제목을 누르면 전체 분석이 열립니다." — Notion 토글 안내가 그대로 남아 있다. 이 파일은 마크다운이고 제목을 눌러도 아무 일도 안 일어난다(웹앱에 렌더 경로 자체가 없다). 같은 블록의 나머지 세 줄(직접 근거/전이 가설 분리, 중복 3건 대응)은 지금도 유효하다.
- **고치는 법**: 10행만 지운다. 나머지 <aside> 블록은 규율 설명이라 살린다.
- codex 필요: False
