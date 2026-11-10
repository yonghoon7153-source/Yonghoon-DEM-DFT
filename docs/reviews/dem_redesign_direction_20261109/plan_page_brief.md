# 계획서 (웹앱 페이지 + docx) 만들기 사양 — 본 세션 첫 일 (2026-11-10 · 서브 세션이 넘김)

1저자 11-10: *"계획 브리핑 이것도 웹앱에서 주간보고 처럼 구리게 말고 좀더 계획서 같은 느낌으로 마감성있게 웹앱에 별도 페이지"* · *"웹앱용으로도 만들고 docx로도 만들어서 내가 글로 읽을 수 있게"*.
서브 세션은 시간 안에 끝내지 못해 이 사양만 넘긴다 (만든 파일 0).  결과 0 건 · 새 계산 0 건인 문서 작업이다.

## 원문 하나

- `docs/reviews/dem_redesign_direction_20261109/briefing_ko.md` (마커 `<!-- BRIEFING:UPDATED YYYY-MM-DD -->` 하나 · 1저자 11-10 결정 Q1–Q5 포함).
- 두 결과물의 글은 모두 이 파일에서 나온다.  손으로 베끼지 않는다.  원문 문장을 바꾸지 않는다 (파싱에 꼭 필요하면 HTML 주석 마커만 더하고 보고).

## 제약

- `webapp/app.py` 는 봉인 32 (`scripts/run_network_194_parallel.py` 의 `CODE_FILES`) 라 새 라우트를 만들지 않는다.  정적 페이지 꼴을 따른다: `webapp/static/explain/rint_overview_20261021.html` + `webapp/templates/base.html` 사이드바 링크 + `webapp/test_rint_explainer_page.py` 꼴 시험.
- 집안 문체 = `docs/report_making_principles.md` (한글 맑은 고딕 · 천 단위 콤마 금지 · 최상급 금지 · 약어 첫 정의).  em dash 를 쓰지 않는다.  호스트 · 주소 · 사용자 이름 · 절대 경로 · 모델 이름을 파일에 쓰지 않는다.
- docx 는 docx 스킬 (Skill 도구 `anthropic-skills:docx`) 을 먼저 불러 그 지시를 따른다 (docx-js 사용 · python-docx 설치하지 않음).

## 만들 파일

1. `scripts/build_dem_redesign_plan.py` — 원문을 절 단위 모델로 파싱해 (a) HTML 페이지와 (b) docx 빌더가 읽는 JSON 을 쓴다.  `--write` = 둘 다 다시 만듦 · `--check` (기본) = HTML 을 메모리에서 다시 만들어 커밋된 파일과 바이트가 다르면 rc 1.  HTML 은 바이트 결정적 (시각 없음 · LF · UTF-8).  쓰는 문법만 지원하고 낯선 구성은 줄 번호와 함께 rc 2.  외부 파이썬 패키지 없음.
2. `scripts/build_dem_redesign_plan_docx.js` — docx-js 로 JSON 을 읽어 docx 를 쓴다.
3. `webapp/static/explain/dem_redesign_plan_20261110.html` — 생성물.  한 파일로 닫힘 (script · link · src · 외부 URL 없음 · DOI 는 글자로) · 인라인 style · 색 토큰을 `:root` 에 두고 `@media (prefers-color-scheme: dark)` (`:root:not([data-theme="light"])` 로 막음) 와 `:root[data-theme="dark"]` 에서 같은 이름으로 덮음 · body 배경 명시 · 폰 폭에서 표는 가로 스크롤 상자 · `@media print` = A4 (흰 바탕 · 큰 절 앞 쪽 나눔 · 그림자 없음).
   계획서 꼴: 표지 머리 (제목 "DEM 재설계 (수영) 계획서" · 원문 부제 · 날짜 · 지위 줄의 작은 배지 = 결과 0 건 · 실행 GO 아님 · Codex 판정 = 방향 지지 · 규칙 수정 필요 (HOLD)) · 요약 상자 ("한 줄로") · 번호 붙은 절 머리 · §3 단계 0–7 과 일정 = 순서 있는 로드맵 카드 (단계 번호 · 이름 · 괄호 안 기계 · 기간 · 문 · 내용) · 갈림 표 = 결과 칩 색 (가) (나) (마) (라) (다) 의 결정표 · §4 = 강조 상자 · §5 = 경고 상자 · §6 = "하지 않는 말" 테두리 상자 · §8 = 질문 · 권고 · 1저자 답 세 칸 표 (답 = 원문의 "답:" 뒤 글) · §9 = Codex 판정 상자 (P1 둘 `DRD-01` · `DRD-02` 는 눈에 띄게) · 논문 표와 참고문헌 표 = 번호 붙은 서지 (litdb slug 는 작은 고정폭).  웹앱 처음으로 가는 링크 `<a href="/">`.  글꼴 = 시스템 스택만 ("Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif).
4. `docs/reviews/dem_redesign_direction_20261109/briefing_ko.docx` — 생성물.  A4 · 본문 맑은 고딕 약 10.5 pt (라틴 = Aptos 또는 Calibri) · 제목 블록 (제목 · 부제 · 날짜 · 지위) · Word 제목 스타일 (Heading 1/2 · 탐색 창이 되게) · 머리 행 음영 표 · 요약과 §4 · §5 · §6 = 음영 · 테두리 상자 · 번호 참고문헌 · 바닥글 쪽 번호.  스킬의 검사기가 있으면 돌리고, LibreOffice 로 PDF 를 만들어 한두 쪽을 그림으로 본다 (이 컨테이너에 한글 글꼴이 없으면 네모로 보일 수 있다 · 그 사실을 적는다).
5. `webapp/test_dem_redesign_plan_page.py` — 시험 (test_rint_explainer_page.py 꼴 · chk 계수 · 모두 통과일 때만 rc 0): 생성기 `--check` 통과 (프로세스 안) + 원문을 바꾼 사본이면 출력이 바뀜 · 닫힌 파일 규칙 · HTML 에 원문 핵심이 남음 (참고문헌 10 행 · litdb slug 10 · 원문의 DOI · "진밀도 1.64" · "10–13 %" · "하지 않는 말" · "SELF-161" · "DRD-01" · "DRD-02" · "Q1." – "Q5." · 마커 날짜) · docx 의 `word/document.xml` 글 (w:t 이어 붙임) 에 같은 핵심 · 보이는 HTML 글에 천 단위 콤마 없음 (`\d,\d{3}\b`) · 색 토큰 세 블록 · 처음 링크 · base.html 링크 + 실제 앱이 그 경로를 200 · text/html · 파일과 같은 바이트로 서빙 + 렌더된 `/seminar` 에 링크가 보임 · 파서가 낯선 구성을 거부.
6. `webapp/templates/base.html` — "Rint 설명" `<li>` 바로 뒤에 `<li>` 하나 (이웃과 같은 꼴의 Jinja 주석 · 링크 글 "DEM 재설계 계획서 (수영)" · 짧은 한국어 title) · 그 밖은 바꾸지 않는다.

## 순서 (시험 먼저)

1. 시험을 먼저 쓰고 돌려 실패 수를 남긴다.
2. 생성기 · docx 빌더 → `--write` → `--check`.
3. base.html → 새 시험 통과 → `webapp/test_rint_explainer_page.py` · `webapp/test_dem_method_figs_page.py` 로 사이드바 회귀 확인.
4. Playwright 로 페이지 스크린샷 (데스크톱 · 390 px · deviceScaleFactor 1) 과 docx PDF 두 쪽을 보고 겹침 · 넘침을 고친다.
5. `scripts/check_all.sh` 에 단계 한 줄 (`python3 webapp/test_dem_redesign_plan_page.py`) · 게이트 · push · docx 를 1저자에게 보낸다.
