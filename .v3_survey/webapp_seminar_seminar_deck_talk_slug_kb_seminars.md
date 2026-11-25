# webapp — 세미나 · 발표 (/seminar · /seminar/deck · /talk/<slug> · kb/seminars/)

## 지금 무엇인가
2026-08 cascade 연구세미나 **한 건**을 위한 연단 콘솔이다 — 정본 덱(29장) 내려받기 2개, 대본을 파싱해 만든 진행표(21장·26분), 그리고 대본·Q&A·용어·출처원장·파이프라인·ML 6개 문서를 한 페이지에 통째로 인라인한 탭(162 KB HTML). /talk/<slug> 는 별개로 litdb/talks/ 의 남의 발표 digest 7편을 정독용 전체 페이지로 편다(manifest 배지로 citable 여부 표시). kb/seminars 에는 38개 파일(pptx 10 · md 25 · js 2 · dir 1)이 있는데 화면이 여는 것은 6개뿐이다.

## 처음 오는 사람
처음 온 사람이 /seminar 에서 **실제로 할 수 있는 것은 pptx 두 개 내려받기뿐**이다. 그리고 막히는 지점이 순서대로 이렇다. ① **언제 발표인지 화면에 없다.** "진행표 · 합계 26분 0초 · 부록은 발표하지 않고 질문 때 띄운다" 는 현재형이라 다음 주에 할 발표처럼 읽히는데, 실제로는 2026-08 에 끝났다(kb/reviews/codex_K_what_next_after_seminar_2026_08_28.md = "세미나 이후 무엇을 할 것인가"). 끝난 발표인지 앞둔 발표인지 판단할 근거가 화면 어디에도 없다. ② **덱을 볼 방법이 없다.** 페이지 전체의 `<img>` 가 **0개**다. 29장짜리 발표를 이해하려면 2 MB pptx 를 받아 PowerPoint 를 열어야 한다 — 웹 지식허브에서 가장 먼저 기대하는 "슬라이드를 화면에서 넘겨 보기" 가 없다. ③ **어디서부터 읽을지 안내가 없다.** 탭 6개는 라벨만 있고 순서 근거가 없는데, 정작 이 영역에서 초심자용으로 쓰인 유일한 문서 — `docs/cascade_pipeline_guide_codex_2026_08_11.md` 첫 줄 "### 처음 보는 대학원생을 위한 자립형 안내서 (2026-08-10 개정판)" — 가 **6개 중 5번째 탭**에 숨어 있고 /cascade·/methods 어디에서도 링크되지 않는다. ④ **⌘K 로 이 페이지를 못 찾는다.** 검색 인덱스에 /seminar 가 없다(아래 findings). 사이드바 "자료·기록" 9개 중 7번째를 눈으로 찾아야 한다. ⑤ **남의 발표 7편은 /literature 98 % 지점**(215편 논문 아래)에 있고 사이드바 항목이 없어, 존재 자체를 모른다. ⑥ 화면 위쪽 절반을 차지하는 것이 우리 발표가 아니라 **남의 세션 판독 패널**(이상욱 교수님)과 **1저자에게 논문 6편 부탁하는 표**다 — 처음 온 사람에게는 잡음이다. ⇒ 지금 이 화면은 "발표 하루 전의 발표자 본인" 한 사람만을 위한 도구이고, 지식허브로서의 진입로는 사실상 없다.

## 건드리면 안 되는 것
- **진행표를 대본에서 파싱하는 구조**(webapp/data.py:6199 seminar_runsheet). docstring 이 이유를 적어 뒀다 — "하드코딩하지 않는 이유 — 대본을 고치면 화면이 따라와야 한다. 어긋나면 그게 바로 '화면과 정본이 갈라진' 상태고, 우리가 제일 싫어하는 종류의 오류다." v3 에서 진행표를 접거나 옮기더라도 **파싱 구조 자체는 유지**한다. 부록 표까지 같은 방식으로 확장하는 것이 옳은 방향이다.
- **패널 스스로 붙인 ⛔ 한계 문구 3종.** ① "⛔ 이 패널은 **자동 검사가 아니다** — 덱이 새 CSV 를 읽도록 바뀌면 위 문구는 조용히 거짓이 된다"(seminar.html:70-71) ② talkprep 의 "⛔ citable = no — 음성 미보유 · 권리 미상 · Q&A 동의 미상 → 외부 사용·직접 인용 전면 금지. 발표에서 '저 교수님이 그랬다' 를 논거로 쓰지 않는다"(seminar.html:92-93) ③ "⚠ 그래도 조심할 것 — 덱이 '3축 랭킹' 이라는 표현을 쓰면 그건 2026-08-25 이전엔 사실이 아니었다"(data.py:6118). 이 셋은 화면을 지저분하게 만드는 잡음이 아니라 **이 repo 가 화면에 요구하는 정직성의 실물**이다. 재편하면서 절대 정리 대상으로 삼지 않는다.
- **doc.html:50-54 의 'manifest 가 없다' 회색 배너.** talk_manifest 가 없을 때 조용히 빠지지 않고 "⚠ source manifest 가 없다 — 승격 상태(citable·권리·동의)를 알 수 없다" 를 띄운다. 7편 중 5편이 이 상태다. 빈 배지를 내면 '인용 가능' 으로 오해되므로 fail-loud 가 맞다 — 시각적으로 거슬려도 지우지 않는다.
- **litdb/talks/yang2026_bml_ml_radial_cathode.md 묘비 stub 과 /talk 에서의 노출.** 파일 스스로 "⇒ 그 두 건이 실재한다면 **이 stub 을 지우지 말고** 정본 §21 에 검증 결과를 추가하면 된다" 라고 남겨 뒀다(미확인 2건: scripts/ml_shap_pareto.py · claims.json CL-41). 목록에서 눈에 거슬려도 삭제 금지. 오히려 이 `> ⤳ superseded by` 양식은 파이프라인 가이드 중복 정리에 그대로 재사용할 모범이다.
- **/literature 의 발표덱 분리 규율 블록**(literature.html:129-132) — "발표 덱은 위 논문 수(215편)에 합산하지 않는다. peer-review를 거치지 않았고 방법 명세가 슬라이드 수준이라 소환값보다 한 단계 낮은 신뢰 등급이다 — 덱 수치를 우리 db 절대값과 같은 표에 넣지 말 것. 덱은 부재의 증거가 아니므로…". 발표를 위로 끌어올릴 때 **이 문구를 함께 옮긴다**. 등급 분리 없이 노출을 올리면 CLAUDE.md 의 '문헌 수치는 소환값 — 우리 db 절대값과 섞지 않기' 를 화면이 깨뜨린다.
- **SEMINAR_DECKS 화이트리스트와 /seminar/deck 전용 라우트**(app.py:1132-1150). 주석대로 kb/ 를 /api/file 허용목록에 넣으면 리뷰 노트까지 열린다. 덱 노출을 늘리더라도 **키 화이트리스트 방식은 유지**한다(?v=nope → 404 실측 확인).
- **md_html 의 raw HTML 차단 + URL scheme 화이트리스트**(app.py:151-178, 208-226). litdb digest 는 외부 PDF 요약이라 신뢰 입력이 아니다. /talk 를 어떻게 개편하든 이 두 방어는 건드리지 않는다.
- **kb/seminars 의 pptx 10개와 옛 대본 md 들.** 화면에서 접거나 숨기는 것은 좋지만 **파일 삭제는 안 된다** — 출처원장의 재현성 메모가 옛 커밋(`origin commit 9ee411a3`)과 판본 차이를 근거로 쓰고 있고, release=final+A3b 라는 계보가 이 파일들로만 확인된다.
- **kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md 의 STT 오인식 경고 블록** — "⚠ STT 전사라 오인식이 많다 (전고체→'정보체', DFT→'TFT/DFD' …) 아래는 문맥으로 복원한 것이고 … **원문 전사는 repo 밖**". 이 카드를 화면에 올릴 때 이 경고를 잘라내면 안 된다.

## 발견

### [P0·wrong] rerank-audit-evidence-backwards
- **어디**: `webapp/data.py:6110-6112 (화면: /seminar 최상단 ✅ 패널 '그런데 왜 이 덱은 안 걸리나')`
- **근거**: 패널 문구: "덱은 자기 CSV 를 읽는다 — plot_cascade_seminar_47.py 가 읽는 것은 cascade_seminar_*.csv (2026-06-25 frozen) 이고 cascade_v23_all.csv 가 아니다. 그림을 다시 그려도 같은 숫자다." ⛔ 데이터 흐름이 거꾸로다. tools/figures/plot_cascade_seminar_47.py 는 그 CSV 들을 **쓴다**: docstring 'Outputs ... db/properties/cascade_seminar_scorecard_47.csv', 코드 381·469·565·647 행 `write_csv(PROP / "cascade_seminar_*.csv", ...)`. 실제 **입력**은 63행 `LITRANSPORT = PROP / _csv("cascade_v23_litransport.csv")` + 61행 `FUNNEL = PROP / "cascade_screening_funnel.json"` + 62행 `PINNED_ESW = ...v3_pinned.json` 이다. 둘째 오류: '(2026-06-25 frozen)' 도 사실이 아니다 — `git log -1 db/properties/cascade_seminar_scorecard_47.csv` = **2026-08-16 f9adc9d2b** (oxidation_transport_47.csv 도 동일). ※ 결론 자체('덱 unaffected')는 우리가 재확인했다: 그 CSV 헤더에 li_mobility_score 열이 없고, 스크립트가 litransport 에서 읽는 것은 `bvs_li_proxy_score` 와 `tier2_dopant_blocking_fraction` 둘뿐이다(코드 202-208행). 틀린 것은 **근거 문장**이고, 패널 스스로 '검증 경로가 그대로인지 사람이 본다'고 적어 둔 바로 그 경로다.
- **고치는 법**: 두 문장을 실측대로 고친다 — "plot_cascade_seminar_47.py 는 cascade_v23_litransport.csv · cascade_screening_funnel.json · oxidation_stability_cascade_v3_pinned.json 을 읽어 cascade_seminar_*.csv 를 **생성한다**. 재랭킹이 건드린 li_mobility_score 는 그 입력 세 파일 어디에도 열로 없다(2026-09-08 재확인)". 'frozen' 날짜는 47종 스냅샷의 versioning 일(2026-06-25)과 CSV 최종 기록일(2026-08-16)을 분리 표기한다. verified_by 목록에 입력 세 파일을 명시한다.
- codex 필요: False

### [P0·stale] seminar-is-a-past-event-with-no-date
- **어디**: `webapp/templates/seminar.html:5-20,126-131 · webapp/data.py:6071`
- **근거**: 화면 머리에 날짜가 없다. 렌더 텍스트 상단은 "🎤 연구 세미나 — cascade / 정본은 kb/seminars/ 의 파일이고 이 화면은 뷰어다" 로 시작하고, 곧바로 "진행표 · 본문 21장 · 합계 26분 0초 · 부록은 발표하지 않고 질문 때 띄운다" 가 온다 — 전부 현재형·예정형이다. 발표 시점이 나오는 곳은 탭을 열어야 보이는 대본 본문("# 발표 대본 최종본 — Research Seminar 2026-08 · Cascade", "## 시작 전 30초 (무대에서)")뿐이다. 그런데 kb/reviews/codex_K_what_next_after_seminar_2026_08_28.md 제목이 "교차리뷰 K — **세미나 이후** 무엇을 할 것인가" 이고, kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md 는 2026-09-03 그룹미팅 기록이다 ⇒ 발표는 최소 열흘 전에 끝났다.
- **고치는 법**: 머리에 상태 뱃지를 박는다 — `발표 완료 · 2026-08 · 정본 덱 29장` (끝난 발표는 회색, 예정은 강조). 진행표 블록은 기본 접힘(연습용 도구는 끝난 뒤엔 아카이브다). v3 에서는 /seminar 를 **한 발표 전용 콘솔**이 아니라 `발표 이력` 목록(2026-08 cascade · 2026-09-03 그룹미팅 · 남의 세션 7편)으로 재편하고, 각 항목이 지금의 콘솔을 하위 페이지로 갖게 한다.
- codex 필요: False

### [P1·wrong] support-docs-point-at-a-different-deck
- **어디**: `kb/seminars/Research_Seminar_2026_08_cascade_final_source_ledger.md:3 · ..._defense_QA_ko.md:3 · ..._terminology_symbols.md:3 (화면: /seminar 탭 🛡·📖·🧾)`
- **근거**: 세 문서 모두 3행이 "대상 덱: `Research_Seminar_2026_08_cascade_final.pptx`" 이고 출처원장은 이어서 "구성: 본문 S1–S21, 부록 A1–A7, **총 28장**" 이라고 못박는다. 그런데 같은 화면이 정본으로 내려주는 것은 `Research_Seminar_2026_08_cascade_release.pptx` = "정본 · 29장 (본문 21 + 부록 8)"(webapp/data.py:6194)이고, 화면은 final.pptx 를 "**다른 판**"(codex28)으로 강등해 놓았다. 실제 차이는 커밋 378ee2846 "seminar: release 덱에 A3b 레이더 삽입 (28->29장, XML 수술)" — 부록에 A3b 가 끼어들어 대본 부록표는 P22=A1·P23=A2·P24=A3·**P25=A3b**·P26=A4…P29=A7 로 밀렸다. 즉 화면은 29장 덱을 주면서 28장 덱용 슬라이드 번호표 셋을 '정본 부속문서'로 붙여 놓았고, 그 사실을 한 줄도 적지 않았다. 덤으로 이 셋을 ACCEPT 판정한 감사보고서(kb/seminars/cascade_final_release_review_2026_08_11.md:1 "최종 release 감사 보고 — Research_Seminar_2026_08_cascade_final (**28장**)")도 화면에 없다.
- **고치는 법**: 탭 라벨 옆에 대상 덱을 찍는다 — `🧾 출처 원장 (28장 codex 판 기준 · A4–A7 은 release 에서 P26–P29)`. 또는 세 문서 3행을 release 기준으로 갱신하고 A3b 행을 추가한다(문서 수정 쪽이 옳다). 어느 쪽이든 **화면이 두 덱을 구분해 말해야** 한다.
- codex 필요: False

### [P1·broken] markdown-symbols-leak-in-two-panels
- **어디**: `webapp/templates/seminar.html:46,56,63,88,101,113 (데이터: webapp/data.py:6096 SEMINAR_RERANK_AUDIT · 6138 SEMINAR_TALK_PREP)`
- **근거**: 렌더된 /seminar 평문에서 실측: 탭 앞 패널 구간에 리터럴 `**` **34개**, 리터럴 백틱 **18개**. 실물 예 — "발표의 funnel 은 가중합 score_combined 가 아니라 **post-hoc G1–G4 게이트**다", "이 랩은 **MTP = 동력학 / uMLIP(...) = static** 으로 용도를 나눈다 `[STT 26:50]`". 템플릿이 `{{ how }}` · `{{ why|safe }}` 로 그냥 꽂는데 `|safe` 는 이스케이프만 끄지 마크다운을 변환하지 않는다. 이 repo 에는 이미 전용 필터가 있고(webapp/app.py:95 `_mdlite`, 142행 등록) 8개 템플릿에서 73번 쓰이는데 **seminar.html 은 한 번도 안 쓴다**. 게다가 그 필터는 바로 어제 같은 종류의 사고로 확장됐다 — 커밋 fc3624184 "webapp: 카드·메모의 마크다운이 화면에 기호로 노출되던 것 정정", app.py:108 주석 "② 표 (2026-09-08) — ... **화면에 파이프가 그대로 노출됐다** (1저자 신고)". 이 화면만 그 수리에서 빠졌다.
- **고치는 법**: seminar.html 의 자유문장 출력 6곳을 `|mdlite` 로 바꾼다(`{{ how|mdlite }}` · `{{ why|mdlite }}` · `{{ claim|mdlite }}` · `{{ rerank.still_watch_out|mdlite }}` · `{{ talkprep.why|mdlite }}` · `{{ talkprep.blockers|mdlite }}`). `|safe` 는 전부 제거한다(원문에 HTML 이 없어 필요 없고, 있으면 오히려 위험).
- codex 필요: False

### [P1·useless] source-ledger-paths-are-dead-text
- **어디**: `webapp/data.py:6082-6083 (탭 '🧾 출처 원장' — 숫자가 어디서 왔는지) · 렌더러 webapp/data.py:5947 md_to_html`
- **근거**: 이 탭의 존재 이유가 "슬라이드별 정본 출처 — 숫자가 어디서 왔는지" 인데, 표 안의 경로 **35개 중 단 하나도 클릭되지 않는다**. md_to_html 의 inline() 은 escape → `code` → `**` → `*` 만 처리하고 링크 문법이 아예 없다(5959-5964행). 실측: 그 35개 중 **23개는 이미 `/api/file/<rel>` 로 열 수 있는 db/·docs/ 아래 파일**이다(D.safe_repo_path 로 확인). 못 여는 12개도 4개는 litdb/papers/*.md 라 /literature 모달로 열 수 있다. 즉 "어디서 왔는지" 를 눈으로 읽고 손으로 다시 찾아야 한다.
- **고치는 법**: md_to_html 에 **경로 자동 링크**를 붙인다 — `<code>` 로 감싸는 자리에서 safe_repo_path 가 통과하면 `/api/file/<rel>`, litdb/papers|talks 면 `/literature#…`(앵커 신설 후) 또는 `/talk/<slug>` 로 감싼다. 이미 app.py:608-614 에 "근거 문서 — 링크로 열 수 있는 것만 링크한다 (safe_repo_path 밖이면 경로만)" 라는 같은 관례가 구현돼 있으니 새로 만들지 말고 그것을 md_to_html 로 끌어온다.
- codex 필요: False

### [P1·broken] talk-page-promises-toc-but-has-none
- **어디**: `webapp/app.py:1099(약속) · 1126(`md_html(md, ("tables","fenced_code","toc"))`) · webapp/templates/doc.html:151`
- **근거**: 라우트 docstring: "논문세미나를 준비할 때는 §99(구술 판독)처럼 긴 절을 **목차와 함께** 펼쳐 놓고 봐야 한다." 실측: /talk/lee2026_skku_mlip_materials_design 렌더 HTML 143 KB, 제목 h2 16 + h3 22 + h4 25 = **63개**, 그런데 목차 요소는 **0개**다. 원인은 Python-Markdown 의 `toc` 확장이 본문에 `[TOC]` 마커가 있을 때만 목차를 뿌리는데, `grep -rl "\[TOC\]" --include=*.md .` 결과가 **repo 전체 0건**이라는 것. 확장이 실제로 한 일은 제목에 id 를 단 것뿐이고(`<h2 id="1">`, `<h2 id="2-pdf">` — 한글이 죽어 의미도 없다), 같은 인자가 /methods·/sdcp·/todo·/requests 등 6곳에서 똑같이 헛돌고 있다. 정작 /seminar 는 JS 로 목차를 만든다(seminar.html:230-242 buildToc) — 짧은 문서엔 목차가 있고 95 KB 문서엔 없다.
- **고치는 법**: doc.html 에 seminar.html 의 buildToc·검색 블록을 공용 부분템플릿으로 빼서 붙인다(길이 임계 이상일 때만). 그게 과하면 최소한 `md_html` 앞에 `[TOC]\n` 을 붙여 확장을 실제로 동작시키고, slug 생성이 한글을 죽이지 않게 `toc` 확장의 slugify 를 지정한다. seminar.html:227 slug() 가 이미 `[^\w가-힣]` 로 한글을 살리고 있으니 그 규칙을 재사용한다.
- codex 필요: False

### [P1·broken] seminar-missing-from-cmdk-search
- **어디**: `webapp/data.py:3352-3369 (search_index 의 pages 목록) · webapp/templates/base.html:80`
- **근거**: search_index() 의 pages 목록 바로 위 주석: "순서·묶음은 사이드바(base.html)와 같게 — 두 군데가 어긋나면 찾는 사람이 헷갈린다"(3351행). 실측 대조 결과 **어긋나 있다** — 사이드바에 있고 검색 인덱스에 없는 페이지: `/fairchem` · `/governance` · `/ledger` · **`/seminar`** · `/requests` · `/sdcp` (6개). 즉 ⌘K 에 '세미나'/'seminar' 를 쳐도 이 화면이 안 나온다.
- **고치는 법**: pages 목록에 6개를 사이드바 순서대로 추가한다. 그리고 이런 어긋남이 다시 생기지 않게 webapp/tests/test_webapp.py 에 **음성 시험**을 하나 신설한다 — base.html 의 nav href 집합 ⊆ search_index 의 페이지 url 집합(조성 링크 제외). 지금 이 어긋남을 잡는 시험이 없다.
- codex 필요: False

### [P1·buried] talks-buried-at-98-percent
- **어디**: `webapp/templates/literature.html:126-127 · webapp/data.py:3349-3350 · webapp/templates/base.html:64-71(nav '문헌·검증')`
- **근거**: 렌더 실측: /literature 평문 85,018자 중 "🎤 학회 발표자료 (7건)" 이 시작되는 위치가 **82,995자 = 98 %** 지점이다. 논문 215편을 전부 지나야 나온다. 사이드바에 발표자료 항목이 없고, /talk/<slug> 로 가는 링크는 repo 전체에서 딱 둘 — literature.html:156 (그 98 % 지점의 카드 안)과 seminar.html:84 (lee2026 하나만). 나머지 6편은 사실상 도달 불가다. 여기 묻혀 있는 것 중에는 do2026_bml_alzib_preconditioning(2026-09-02, 이 영역에서 **가장 최신** 자료)도 있다.
- **고치는 법**: /literature 상단에 '🎤 발표자료 7건' 요약 줄 + 앵커를 두고, 사이드바 '문헌·검증' 에 `🎤 발표자료` 항목을 신설한다(라우트는 /literature#talks 또는 새 /talks 목록). v3 에서는 /seminar 를 '발표' 허브로 만들고 남의 발표 7편을 우리 발표와 같은 화면에서 나란히 보이게 한다 — 지금은 lee2026 한 편만 특별대우다.
- codex 필요: False

### [P1·broken] talk-search-anchor-does-not-exist
- **어디**: `webapp/data.py:3349-3350 · webapp/templates/literature.html:136`
- **근거**: 검색 인덱스가 발표 항목의 url 을 `f"/literature#{t_['id']}"` 로 만든다. 그런데 literature.html 의 발표 카드에는 `id` 속성이 없다 — 실측: `'id="do2026_bml_alzib_preconditioning"' in html` → **False**, `<div class="card paper" ... id=` 정규식 매치 **0건**. 즉 앵커가 어디에도 없어서 브라우저는 그냥 /literature 맨 위(215편 목록 머리)에 떨어뜨린다. 게다가 목표 카드는 98 % 지점에 있다.
- **고치는 법**: 발표·논문 카드에 `id="{{ t.id }}"` 를 단다(비용 0). 더 나은 fix 는 검색 url 을 `/talk/{{ id }}` 로 바꾸는 것 — 그쪽이 정독용 전체 페이지이고 라우트가 이미 있다. 논문(litdb/papers)은 전체 페이지가 없으니 앵커 유지.
- codex 필요: False

### [P1·duplicate] two-pipeline-guides-both-called-canonical
- **어디**: `docs/cascade_pipeline_guide.md ↔ docs/cascade_pipeline_guide_codex_2026_08_11.md (화면: webapp/data.py:6084 탭 '🧭 파이프라인' vs 같은 화면 '🧾 출처 원장' 본문)`
- **근거**: 두 파일 모두 1행이 "# 황화물 SE 도펀트 스크리닝 캐스케이드 — 파이프라인 전 과정 설명서", 3행이 "### 처음 보는 대학원생을 위한 자립형 안내서" 로 같고 부제만 다르다 — 전자 "(2026-08-06판)" 24,075 B, 후자 "(2026-08-10 개정판)" 26,322 B. **한 화면 안에서 둘 다 정본 행세를 한다**: 탭 '🧭 파이프라인' 은 후자를 열고, 바로 옆 탭 '🧾 출처 원장' 은 전자 `docs/cascade_pipeline_guide.md` 를 S1·S4·S7·S9·S11·S16·S17·A2·A7 등 **10회** 정본으로 지목한다. webapp/data.py:4067 도 "상세: docs/cascade_pipeline_guide.md §3" 로 전자를 가리킨다.
- **고치는 법**: 1저자가 어느 쪽이 정본인지 정하고, 진 쪽은 머리에 `> ⤳ superseded by <정본>` 한 줄만 남긴다(litdb/talks/yang2026_bml_ml_radial_cathode.md 가 이미 쓰는 묘비 양식). 지우지는 않는다. 이긴 쪽으로 출처원장 10곳과 data.py:4067 을 함께 갱신한다.
- codex 필요: False

### [P1·buried] beginner-guide-buried-in-tab-5
- **어디**: `webapp/data.py:6084-6087 (SEMINAR_DOCS 의 pipeline·ml 항목)`
- **근거**: `docs/cascade_pipeline_guide_codex_2026_08_11.md`(26 KB, "처음 보는 대학원생을 위한 자립형 안내서")와 `docs/cascade_ml_integration_guide.md`(30 KB)는 **webapp 전체에서 /seminar 의 5·6번째 탭으로만** 열린다 — `grep -rn "cascade_pipeline_guide\|cascade_ml_integration_guide" webapp/*.py webapp/templates/*.html` 결과가 data.py 세 줄뿐이고 /cascade·/methods 템플릿에는 없다. 세미나와 무관하게 cascade 를 이해하러 온 사람은 '연구 세미나' 페이지를 열어 탭 다섯 개를 지나야 이 문서에 닿는다.
- **고치는 법**: 두 문서를 /cascade 와 /methods 머리에 올린다(세미나 탭에서 빼도 되고, 양쪽에 두되 /seminar 쪽은 '같은 문서' 표시). v3 IA 로는 '방법 문서'는 /methods, '이 발표를 위한 문서'는 /seminar — 지금은 그 경계가 없다.
- codex 필요: False

### [P1·missing] kb-seminars-32-of-38-unreachable
- **어디**: `kb/seminars/ (38개) vs webapp/data.py:6075-6088 · 6193-6196 · webapp/data.py:4801 safe_repo_path`
- **근거**: 실측 구성: pptx 10 · md 25 · js 2 · dir 1 = 38. 화면이 여는 것은 md 4 + pptx 2 = **6개**. 나머지는 웹앱에서 아예 못 연다 — safe_repo_path 의 허용 뿌리가 docs/·db/ 라 kb/ 는 /api/file 로도 막혀 있고(4802행 "docs/ · db/ 안의 파일만 허용"), kb 문서 전용 라우트도 없다(라우트 46개 전수 확인). 못 여는 것 중에 **kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md** 가 있다 — frontmatter `date: 2026-09-03 · status: 활성 · confidence: high`, 본문 "**이 문서의 지위**: 앞으로 Nd 논문·**연구세미나**·원고를 쓸 때의 **1차 지침**", 첫 항목 "★★★ D-1. 'DFT 자체는 노블티가 아니다'". 이 영역에서 가장 새롭고 구속력이 명시된 문서가 화면에 한 글자도 없다. 같이 묻힌 것: cascade_final_release_review_2026_08_11.md(ACCEPT 감사), cascade_deck_3to7/8to12_script_2026_08_20.md(대본 정정판), seminar_redirect_2026_08_11.md.
- **고치는 법**: ① `group_meeting_2026_09_03_nd_professor_directives.md` 를 /seminar **맨 위 탭**(또는 상단 배너)으로 올린다 — 최신·최고 구속력이 앞. ② SEMINAR_DOCS 를 손으로 나열하는 대신 kb/seminars/*.md 를 frontmatter `status`·`date` 로 정렬해 자동 나열하고, 옛것은 `<details>` 안으로. ③ pptx 10개는 전부 노출하지 말고 '정본 1 + 이전 판 9(접힘)' 로 — 지우지는 않는다.
- codex 필요: False

### [P1·missing] deck-has-no-visual-on-screen
- **어디**: `webapp/templates/seminar.html 전체 (렌더 결과 `<img>` 0개) · webapp/app.py:1132 seminar_deck`
- **근거**: 렌더된 /seminar 162 KB 안에 `<img` 태그가 **0개**다. 발표의 실체인 29장을 화면에서 볼 방법이 없고, `docs/figures/cascade/` 에 92개 파일(그 중 cascade_seminar_scorecard_47.png · cascade_seminar_pareto_47.png · cascade_seminar_oxidation_transport_47.png · cascade_seminar_pool_attrition_273_to_47.png · cascade_radar_6panel.png 등 덱에 실제로 들어간 그림)이 있는데도 한 장도 붙지 않았다. 슬라이드 이미지 export 자체가 repo 에 없다(`find -name '*slide*'` 로 확인 — 있는 것은 다른 계열의 slide05/06/09/14/15/16 그림 폴더뿐).
- **고치는 법**: 단기: 진행표의 각 P 항목에 해당 슬라이드가 쓰는 `docs/figures/cascade/*.png` 를 썸네일로 붙인다(경로는 출처원장·대본에 이미 적혀 있고 docs/ 는 /api/file 로 서빙된다). 중기: pptx → PNG 29장 export 를 tools/seminar 에 넣고(이미 build_seminar_pptx.py·rebuild_cascade_deck.py 가 있으니 새 파일 대신 플래그 추가) 슬라이드 뷰어를 단다. **이게 이 화면에서 가장 큰 한 방이다.**
- codex 필요: False

### [P1·stale] rerank-audit-not-rechecked-after-0908
- **어디**: `webapp/data.py:6096-6135 (date: '2026-08-25') vs db/properties/cascade_d_rel_estimand_2026_09_08.json · 커밋 22b00e909·8c9338c96·c221ac933`
- **근거**: 패널이 스스로 적어 둔 만료 조건: "⛔ 이 상수가 못 하는 것: 자동 검사가 아니다. 덱이 새 CSV 를 읽도록 바뀌면 이 문구는 조용히 거짓이 된다"(data.py:6093-6095). 마지막 감사일은 **2026-08-25**. 그 뒤 cascade 쪽에서 P0 두 건이 나왔다 — db/properties/cascade_d_rel_estimand_2026_09_08.json §0: "39개_target_은_실재하지_않았다 ... aggregate_designs 가 **축마다 독립적으로** 중앙값을 냈다 ... 합성 벡터다(35/39)", "집계_순서가_두_가지였다 ... **227설계 중 169개가 다르다**" — 그리고 커밋 8c9338c96 이 aggregate_designs 를 대표행 선택으로 **교체**했다. 화면에는 이 사건이 한 줄도 없고 초록 ✅ 만 있다. 우리 쪽 확인으로는 덱 CSV 에 li_mobility_score 열이 없어 **결론은 아직 성립**하지만, '2026-09-08 재확인함' 이라는 기록이 없으면 다음 사람이 같은 검산을 처음부터 다시 해야 한다.
- **고치는 법**: 패널에 `last_verified` 필드를 추가하고 매 재확인마다 날짜를 올린다(값 없이 초록만 있으면 안 된다). 그리고 2026-09-08 estimand 카드(D-2026-09-08-cascade-d-rel-estimand)와의 관계를 한 줄로 적는다 — "그 재정의는 D_rel 캠페인의 집계식이고, 이 덱의 게이트 입력(bvs_li_proxy_score)은 그 경로를 타지 않는다". 판정은 우리가 실측으로 내렸지만, **이 결론을 공식 기록으로 승격할지**는 사람/외부 리뷰가 도장을 찍어야 한다.
- codex 필요: True

### [P2·missing] runsheet-hides-8-of-29-slides
- **어디**: `webapp/data.py:6218-6221 (seminar_runsheet 의 `if line.startswith("# ") and cur is not None: cur = None`) · webapp/templates/seminar.html:129-130`
- **근거**: 화면은 "진행표 · 본문 21장 · 합계 26분 0초 · **부록은 발표하지 않고 질문 때 띄운다**" 라고만 말하고 부록 8장이 무엇인지 안 보여준다. 파서가 Part 밖 `# ` 구획을 잘라내기 때문이다. 정작 대본에는 완성된 부록 지도가 있다 — kb/seminars/cascade_speaker_script_FINAL_ko.md:137 "# 부록 P22–P29 — 발표하지 않고, 질문 때 띄운다" 아래 표로 P22=A1 용어·기호 … P25=A3b 레이더 … P29=A7. 질문이 들어와 부록을 띄워야 하는 **바로 그 순간**에 필요한 표가 진행표에 없고 탭 본문 137행까지 스크롤해야 한다.
- **고치는 법**: seminar_runsheet 를 확장해 부록 표(`# 부록 …` 구획의 마크다운 표)를 파싱하고, 진행표 옆에 '질문 대비 — 부록 8장' 카드로 붙인다. 하드코딩하지 않는다는 기존 원칙(6201-6205행 docstring)을 그대로 지킨다.
- codex 필요: False

### [P2·wrong] dynamic-exempt-reason-is-false
- **어디**: `webapp/tests/test_webapp.py:809-816 (DYNAMIC_EXEMPT['/talk/<slug>'])`
- **근거**: 면제 사유 원문: "발표 슬러그가 **kb/seminars 파일명과 1:1 이 아니다** — 대응 규칙을 확인하기 전에는 임의 슬러그를 넣어 404 를 통과로 세게 된다. ⏳ 규칙 확인 후 fixture 로 옮긴다." ⛔ 전제가 틀렸다. 라우트는 kb/seminars 를 보지 않는다 — webapp/app.py:1108 `p = D.LITDB / "talks" / f"{slug}.md"` 다. 슬러그는 litdb/talks/*.md 의 stem 이고 **정확히 1:1** 이다(D.list_talks() 가 `f.stem` 을 그대로 id 로 쓴다, data.py:3120). 우리가 7개 슬러그를 전부 밟아 봤고 전원 200 이다. 이 잘못된 사유 때문에 스모크가 못 미는 라우트가 하나 남아 있고, 그 파일 주석은 "⚠ 여기 넣는 것은 '검사 안 함' 이라는 선언이다. 늘어나면 그만큼 눈이 먼다" 라고 스스로 경고한다.
- **고치는 법**: EXEMPT 에서 빼고 DYNAMIC_FIXTURES 에 넣는다 — `"/talk/<slug>": ["lee2026_skku_mlip_materials_design", "yang2026_bml_ml_radial_cathode"]` (둘째는 묘비 stub 이라 회귀에 좋다). 존재하지 않는 슬러그가 404 인지 보는 음성 케이스도 같이 넣는다.
- codex 필요: False

### [P2·ia] seminar-prose-skips-claim-binding
- **어디**: `webapp/app.py:1170 `D.md_to_html(...)` vs webapp/app.py:178 `_bind_claims(_sanitize_urls(md.convert(...)))``
- **근거**: kb 산문의 철회 결속은 md_html **한 곳**에서 자동으로 붙게 설계돼 있다 — app.py:180-184 주석 "손으로 data-claim 을 심으면 원장이 화면 형식에 오염되고 ... 그래서 md_html 한 곳에서 자동으로 붙인다 — 새 문서가 들어와도 자동으로 결속된다". 그런데 /seminar 만 다른 렌더러 `D.md_to_html`(data.py:5947)을 쓰고 그 함수는 `_bind_claims` 를 호출하지 않는다. 실측: 렌더된 /seminar 에 `claim-flag`·`data-claim` **0개**. **지금은 무해하다** — 6개 문서에 `canonical.annotate_claims` 를 직접 돌려 보니 전부 0건이고, 대본 109행의 "단일 시드로 낸 1.33배 전도도 비교 — 멀티시드 판정으로 바꿨습니다" 는 철회 서사 문맥이라 결속 대상이 아니다. 문제는 앞으로다 — 새 철회가 등록되면 다른 화면은 전부 ⛔ 를 띄우는데 이 화면만 조용히 지나간다.
- **고치는 법**: md_to_html 반환값을 `_bind_claims` 로 감싸거나(순환 import 는 지연 import 로), /seminar 를 md_html 로 옮긴다. 후자가 낫다 — 렌더러가 둘인 것 자체가 이 균열의 원인이다. webapp/tests 의 `test_markdown_render_binds_claims_and_can_fail` 에 /seminar 경로를 포함시킨다.
- codex 필요: False

### [P2·broken] md_to_html-breaks-nested-emphasis
- **어디**: `webapp/data.py:5962-5963 (`_re.sub(r"\*\*([^*]+)\*\*", ...)`) · 증상: /seminar 탭 '🧭 파이프라인'`
- **근거**: 굵게 안에 기울임이 들어가면 별표가 화면에 노출된다. 정규식이 `[^*]+` 라 안쪽 `*` 를 허용하지 않고, 그 다음 em 규칙이 안쪽만 먹어 바깥 `**` 둘이 남는다. 실물 1건 — docs/cascade_pipeline_guide_codex_2026_08_11.md:143 `**그들은 10만 종을 계산하지 않았다. 10만 종을 *조회*했다.**` 가 화면에 "**그들은 10만 종을 계산하지 않았다. 10만 종을 조회 했다.**" 로 별표째 나온다. (나머지 4개 `**` 노출은 코드펜스 안이라 렌더러 잘못이 아니라 원문 잘못이다: `분류기 훈련셋 = **실측 40종**`, `CI-NEB (비싼 계산) → **6 종**`.)
- **고치는 법**: bold 를 em 보다 먼저 처리하되 안쪽을 허용한다 — `\*\*(.+?)\*\*` 를 non-greedy 로 쓰고 치환 결과를 다시 em 규칙에 태운다(app.py:89 `_MDL_BOLD` 가 이미 그 형태다 — 새로 짜지 말고 그 패턴을 가져온다). 코드펜스 안의 `**` 두 곳은 원문에서 지운다.
- codex 필요: False

### [P2·ia] top-of-page-is-someone-elses-talk
- **어디**: `webapp/templates/seminar.html:76-123 (talkprep 패널) · webapp/data.py:6138-6191`
- **근거**: '🎤 연구 세미나 — cascade' 페이지의 첫 화면 절반을 우리 발표가 아닌 것이 차지한다 — "🎤 이상욱 교수님(성균관대 CMS Lab) 세션 — 덱 31장 + 구술 31:44 전수 판독"(가져올 것 7건 기본 펼침) + "📌 사용자에게 요청 — litdb 에 없어서 필요한 논문 (6건)". 진행표·대본은 그 아래다. 패널 자신은 "이 패널은 **우리 발표 준비**의 일부다" 라고 하지만 날짜가 2026-08-26 로 발표가 끝난 뒤이고, 논문 6편 요청은 성격상 /requests(1저자 요청 대장) 나 /todo 쪽 물건이다. 또 이 판독은 남의 발표 7편 중 **한 편만** 특별대우한 것이라 나머지 6편과 형평이 안 맞는다.
- **고치는 법**: v3 에서 이 패널을 '경쟁 좌표' 로 이름을 바꿔 /literature 발표 섹션(또는 새 발표 허브)으로 옮기고, /seminar 에는 한 줄 링크만 남긴다. 논문 6건 요청은 /todo·/requests 로 이관해 요청 대장을 한 곳으로 모은다(지금은 요청 표면이 둘이다).
- codex 필요: False

### [P2·broken] governance-decision-is-plain-text
- **어디**: `webapp/templates/seminar.html:69 · webapp/data.py:6134 · /governance`
- **근거**: 패널 꼬리: "판정 기록: db/governance/decisions.json → D-2026-08-25-missing-axis-is-unknown-not-worst" · "근거 카드: kb/methodology/cascade_rerank_runbook_2026_08_25.md" — 둘 다 클릭 불가 평문이다. 그런데 /governance 는 존재하고 그 결정을 실제로 담고 있다(렌더 실측: 문자열 `missing-axis-is-unknown-not-worst` 포함 True). 다만 링크를 걸어도 못 뛴다 — /governance 에 결정별 앵커가 없다(정규식 `id="D-` 매치 **0건**).
- **고치는 법**: /governance 의 결정 카드마다 `id="{{ d.id }}"` 를 달고, 세미나 패널의 판정 기록을 `<a href="/governance#D-2026-08-25-...">` 로 만든다. kb/ 경로(근거 카드)는 safe_repo_path 밖이라 링크가 안 되니 그건 평문 유지가 맞다 — 대신 '웹앱에서 못 여는 경로' 라는 표시를 주면 더 정직하다.
- codex 필요: False
