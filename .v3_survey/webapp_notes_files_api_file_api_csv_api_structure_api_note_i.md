# webapp — 메모 · 파일 · 첨부 (/notes /files /api/file /api/csv /api/structure /api/note-image /api/comments /api/highlights /api/file-rename)

## 지금 무엇인가
/files 는 docs/figures · db/properties · db/structures 를 통째로 훑어 파일 카드 1122개를 한 페이지에 날짜별로 깔아 주는 갤러리고(943 KB HTML, 썸네일 img 286개), 클릭하면 모달에서 이미지·CSV·PDF·텍스트를 미리 본다. /notes 는 db/file_comments.json 에 쌓인 여백 메모(📝 50건)와 그림 코멘트(💬 27건) 총 77건을 날짜별로 모아 보여주는 읽기 화면이고, 카드를 누르면 그 논문 digest 의 메모 자리로 간다. 나머지 /api/* 는 이 두 화면과 문서 옆 메모 UI 가 쓰는 서빙·저장 엔드포인트인데, 쓰기 계열은 Render 배포에선 기본 403(읽기 전용)이다.

## 처음 오는 사람
처음 온 사람한테 /files 는 "1122개 · 날짜별 (최근순)" 이라고 적힌 뒤 파일 카드가 끝없이 깔리는 화면이다. 이 파일들이 뭔지, 어디서 나온 건지, 어떤 건 인용하면 안 되는지 화면 어디에도 없다. 실제로 걸리는 지점이 셋이다. ① 스크롤을 조금 내리면 "2026-09-03 | 5일 전 | 917개" 라는 덩어리가 나오는데 이건 파일이 만들어진 날이 아니라 이 컨테이너가 repo 를 체크아웃한 날(.git/HEAD 도 같은 날짜)이다 — 즉 82%가 가짜 날짜다. ② 카드 132개는 눌러도 403 이라 썸네일이 깨진 채로(이미지 63개) 그냥 놓여 있고, 왜 막혔는지 카드에는 한 글자도 없다. ③ 제일 나쁜 건 `md_conductivity_SUPERSEDED_single_seed_2026_06_30.csv` 처럼 헤더 첫 줄이 "SUPERSEDED (2026-07-07) - SINGLE-SEED. DO NOT QUOTE." 인 파일이 아무 표시 없이 보통 카드로 있고, 눌러 보면 그 경고는 접힌 `<details>` 안에 들어가고 철회된 숫자만 표로 활짝 펼쳐진다는 것이다. 처음 온 사람은 그 숫자를 그대로 베껴 간다.
/notes 는 상대적으로 낫다 — "메모는 읽던 문서에서 오른쪽 클릭으로 답니다 … 카드를 누르면 적어 둔 그 자리로 갑니다" 라는 안내가 실제로 맞는 말이라 어떻게 쓰는 화면인지 바로 안다. 다만 (a) 최신 메모가 2026-08-31 이고 77건 중 70건이 2026-08-28 하루치(논문 두 편 세미나 준비)라 "살아 있는 기록" 처럼 생겼는데 사실은 그날 오후의 박물관이고, (b) 10건은 본문에 `![](/api/note-image/…png)` 라는 글자가 그대로 찍혀 있고 그 URL 은 404 라서 무슨 말인지 알 수 없고, (c) 21건은 `**` 가 짝이 안 맞은 채로 노출되거나 엉뚱한 데까지 굵어져 있다. 그리고 배포판(Render)에서는 안내대로 오른쪽 클릭해 메모를 다 쓴 다음에야 "읽기 전용 모드예요" alert 를 만난다.
지식 허브가 되려면 /files 첫 화면이 "이 repo 의 산출물 1122개" 가 아니라 "지금 인용 가능한 것 / 조건부 / 금지" 로 갈라져 있어야 하고, /notes 는 최근 것이 실제로 최근이어야 한다.

## 건드리면 안 되는 것
- **db/file_comments.json · db/file_highlights.json 의 글은 한 글자도 지우지 않는다.** 메모 77건·형광펜 19건은 1저자가 논문을 읽으며 내린 판단이고, 편집 이력도 item.history 에 쌓이는 구조다(app.py:960 PATCH). 대상 파일이 사라진 1건(adeli2019 fig_20.png)도 '대상 없음' 표시만 붙이지 삭제 금지.
- **/notes 의 딥링크 규약**(data.py:5864 note_url → `?note=<id>`, docnote.js:326 이 그 자리로 데려가고 반짝인다). 이 화면의 유일한 진짜 강점이다 — 카드를 누르면 읽던 자리로 돌아간다. v3 에서 목록 모양을 바꾸더라도 이 링크 규칙과 docnote 의 앵커 복원은 그대로 가져간다.
- **쓰기 잠금의 기본값 로직**(app.py:38-64: Render 는 잠그고 로컬은 열고, ALLOW_MUTATIONS 를 명시하면 양방향으로 그게 이긴다). 2026-08-16 에 '로컬까지 잠갔다' 로 한 번 물린 자리라 건드리면 같은 사고가 난다. render.yaml 의 `ALLOW_MUTATIONS: "0"` 과 그 위 주석(인증 없음·파일시스템 휘발)도 그대로.
- **경로 방어 3종**: data.safe_repo_path(docs/·db/ 밖 차단), note_image_path(해시+확장자 규격만), _NOTE_DOC_DIRS(메모를 달 수 있는 문서 화이트리스트를 서빙 화이트리스트와 **분리**해 둔 것, data.py:4768 주석). '메모 달려고 넓히면 배포판이 kb 전체를 내려받게 된다' 는 판단이 이미 나와 있다 — v3 에서 kb 문서에 메모를 붙이고 싶어도 safe_repo_path 를 넓히는 방식은 금지.
- **md_html 의 raw HTML 차단 + _sanitize_urls**(app.py:151, 212). litdb digest 는 외부 PDF 요약이라 입력이 신뢰 대상이 아니라는 판단과 `[click](javascript:...)` 실측 사례가 근거로 붙어 있다. 마크다운 렌더러를 통합하더라도 이 두 겹은 유지.
- **_mdlite 의 별표 가드 3종**(코드스팬 격리 · MAXB 300자 상한 · 여는 별표 뒤 닫는 문장부호 배제). `globstar(**)` 가 300자 뒤 진짜 `**` 와 짝지어 문장을 통째로 굵게 만든 실측이 근거다. 이미지 지원을 추가하되 이 가드는 제거하지 말 것.
- **comments.js 의 IMG_SRC 화이트리스트**(`/api/note-image/[0-9a-f]{32}\.(png|jpg|gif|webp)` 만 <img> 로 편다). 임의 URL 을 허용하면 메모 한 줄로 외부 요청을 만들 수 있다는 판단이 주석에 있다 — 서버 쪽에 이미지 렌더를 추가할 때 **같은 규칙**을 복사하지 말고 공유해야 한다.
- **CSV 헤더 주석을 버리지 않고 모으는 read_csv 의 notes 수집**(data.py:3266-3270). '절대 σ 캐비앳이 UI 에 도달 못 해 무경고로 그려질 뻔한' 2026-07-29 감사가 근거다. 접는 위치는 고쳐야 하지만 수집 자체는 유지.
- **utf-8-sig 로 여는 것**(data.py:3259). Origin 호환 BOM 때문에 안 그러면 첫 줄 주석이 헤더로 잡혀 표가 1열이 된다(2026-07-30).
- **artifact_policy 를 /api/csv·/api/file 양쪽에 건 것**과 gov_rel 정규화(app.py:849-863). 화면에서 숨긴 artifact 를 이 경로로 그냥 받던 구멍(Codex Round-3 P0-3)과 봉투 식별자가 원장 source_path 와 어긋나던 건(2026-09-07)을 막은 자리다. 갤러리에 정책을 붙이라는 위 제안은 이걸 **끄자는 게 아니라 화면에도 같이 걸자는 것**이다.
- **_paper_cmt_index 로 POST/PATCH 응답이 GET 과 같은 모양을 돌려주는 것**(app.py:941, 986-989). '방금 단 코멘트가 새로고침 전엔 검색에 안 걸린다' 는 1저자 신고(2026-08-06)와 'POST 에만 색인이 빠져 조용히 아무 일도 안 나던' 회귀가 주석에 적혀 있다.

## 발견

### [P0·wrong] files-hazard-unmarked
- **어디**: `webapp/templates/files.html (전체) · webapp/data.py:5045 gallery_files · webapp/app.py:1050 files_gallery`
- **근거**: `grep -c "claim|hazard|철회" webapp/templates/files.html` → 0. gallery_files 는 artifact_policy 도 canonical 도 부르지 않는다. 그런데 citation_hazards.json 의 25건 중 23건이 갤러리에 그대로 카드로 있다 — BLOCKED 5건(sei_neb.json "전량 철회", sdcp_phaseB_dftu_v1.json, vgcf_hbn_binding_matrix.json, sdcp_wave1_citable.json, lpsocl_md_arrhenius.json 계간비교), HOLD 2건, PREVIEW 1건(lpsocl_box331_two_point_2026_08_31.json — what: "'3×3×1 Ea = 0.170 eV' — **인용 금지**"), CONDITIONAL 12건, STALE 1건. 그리고 db/properties/md_conductivity_SUPERSEDED_single_seed_2026_06_30.csv 는 헤더가 `# ===== SUPERSEDED (2026-07-07) - SINGLE-SEED. DO NOT QUOTE. =====` / `The sigma ratio they reconstruct (18.51/13.94 = 1.33x) was RETRACTED` 인데 카드에는 파일명 말고 아무 표시가 없다. CLAUDE.md 가 이름 대서 금지한 바로 그 1.33× 다.
- **고치는 법**: webapp/canonical.py:438 `hazard_claims()` 가 이미 citation_hazards.json 을 file 경로 키로 읽는다. gallery_files 결과에 `hazard = {level, what, why, fix}` 를 붙이고 ① 카드에 레벨 배지(⛔ BLOCKED / ⏸ HOLD / ⚠ CONDITIONAL), ② 모달 상단에 표 위로 접히지 않는 경고 배너, ③ 파일명에 SUPERSEDED/RETRACT 가 들어간 것은 기본 목록에서 접고 '옛 판(archive)' 탭으로 뺀다. 정본은 db/properties/citation_hazards.json · canonical_registry.json.
- codex 필요: False

### [P0·buried] csv-caveat-folded
- **어디**: `webapp/templates/files.html:136`
- **근거**: 모달 CSV 미리보기가 `#` 로 시작하는 줄을 골라 `'<details …><summary …>헤더 주석 ' + notes.length + '줄 (출처·규율)</summary>'` 로 **접어** 두고, 숫자 40행은 표로 펼쳐 놓는다. 실물: db/properties/b2o3_vs_lpscl16_conductivity.csv 는 열이 `…,sig600_mScm,sig800,sig1000` 이고 값이 `768,1197,2249` 인데(CLAUDE.md: MD σ 절대값 인용 금지), 접힌 세 줄이 `# PROTOCOL GENERATION: gen0_pre_gate … Ea values are protocol-conditioned; not comparable to the 400 ps campaign.` 와 `Gates G1(MTO)=NO, G2(traj retained)=NO -> … NOT ASSESSED (that is not a pass).` 다. 게다가 이 모달은 /api/csv 가 아니라 /api/file 로 받아서 read_csv 가 붙여 주는 `_artifact_status` 봉투(app.py:849)도 안 온다.
- **고치는 법**: 규율 문구(DO NOT QUOTE · NOT reportable · 인용 금지 · SUPERSEDED · NOT ASSESSED)를 담은 주석 줄은 `<details>` 밖으로 꺼내 표 **위**에 경고 박스로 고정하고, 나머지 서지성 주석만 접는다. 모달 CSV 경로를 /api/csv 로 바꿔 `_artifact_status` 봉투와 read_csv 의 `notes` 를 같이 쓰는 게 더 낫다(파서가 한 곳으로 모인다).
- codex 필요: False

### [P0·broken] note-images-404
- **어디**: `webapp/templates/notes.html:69 (`{{ c.text|mdlite }}`) · webapp/app.py:95 _mdlite · .gitignore:83`
- **근거**: 메모 77건 중 10건이 `![](/api/note-image/<32자해시>.png)` 를 포함한다(id: c1787895101859, c1787894637107, c1787894303339, c1787894258114, c1787894270635, c1787894170835, c1787894187596, c1787894199827, c1787890760805, c1787890669799). _mdlite 는 이미지 문법을 모른다 → 화면에 그 문자열이 글자 그대로 찍힌다. 게다가 `/api/note-image/d1281804ec7577fed5a1eb16eeee7c0a.png` 는 실제로 **404** 다 — .gitignore 83행이 `db/note_images/` 라 커밋된 적이 없고 이 체크아웃엔 디렉터리 자체가 없다. 두 겹으로 깨졌다. 반면 같은 글을 팝오버에서 보면 comments.js:34 의 `inline()` 이 `<img class="note-img">` 로 편다 — 같은 텍스트가 두 화면에서 다르게 보인다.
- **고치는 법**: ① _mdlite 에 comments.js 와 **같은 규칙**의 이미지 변환을 넣는다(`/api/note-image/[0-9a-f]{32}\.(png|jpg|gif|webp)` 만 허용 — 임의 URL 금지, 규격 밖은 글자 그대로). ② 이미지가 404 면 카드에 '그림 원본 없음(로컬 전용, 커밋되지 않음)' 이라고 적는다 — 빈 칸으로 두지 않는다. ③ 1저자에게 db/note_images 를 커밋 대상으로 올릴지 물어야 한다(안 올리면 배포판에선 영구히 못 본다).
- codex 필요: False

### [P1·broken] files-403-cards
- **어디**: `webapp/templates/files.html:53 · webapp/app.py:868 api_file · webapp/data.py:5045`
- **근거**: 1122개 전부에 /api/file 을 때려 보니 **132개가 403**(image 63 · csv 25 · pdf 22 · file 22, 폴더로는 docs/figures/cascade 85 · db/properties 47). 본문 예: `{"error":"원장(cascade_audit_manifest.json)에 없…"}`, `"diagnostic_only artifact 다…"`, `"archive_only artifact 다 — ?archive…"`. 화면은 이걸 모른다 — 이미지 63개는 깨진 썸네일로 그냥 놓이고, CSV 25개는 모달 JS 가 `fetch(...).then(r=>r.text())` 로 r.ok 를 안 봐서 **403 JSON 본문을 CSV 표로 그린다**, PDF 22개는 빈 embed, ⬇ 저장은 에러 JSON 을 받아 온다.
- **고치는 법**: gallery_files 가 artifact_policy.resolve 를 태워서 카드에 상태(archive_only / diagnostic_only / 원장 미등재)와 `?archive=1`·`?view=diagnostic` 로 여는 버튼을 같이 준다. 최소한 모달 fetch 에 r.ok 검사를 넣어 403 사유를 그대로 띄운다.
- codex 필요: False

### [P1·wrong] mtime-is-checkout-date
- **어디**: `webapp/data.py:5089-5091 (gallery_files 의 mtime/day) · webapp/data.py:5095 gallery_days · webapp/templates/files.html:40`
- **근거**: day 를 `_dt.datetime.fromtimestamp(st.st_mtime)` 로 만든다. 이 체크아웃에서 렌더한 실제 헤더: `2026-09-08 | 오늘 | 36개` / `2026-09-07 | 어제 | 119개` / … / `2026-09-03 | 5일 전 | 917개`. 그런데 `.git/HEAD` 의 mtime 이 `2026-09-03 13:36`, `find db docs -newermt 2026-09-03 ! -newermt 2026-09-04 | wc -l` = 1240 이다 — 917 은 파일이 생긴 날이 아니라 **체크아웃한 날**이다. 화면은 이걸 `날짜별 (최근순)` · `오늘/어제/N일 전` 로 출처인 양 보여준다. Render 는 배포마다 새로 clone 하므로 배포판에서는 전체가 배포일 한 덩어리가 된다.
- **고치는 법**: 날짜의 출처를 git 으로 바꾼다(`git log -1 --format=%cI -- <path>`, 캐시). 못 얻는 파일은 '날짜 미상' 묶음으로 — CLAUDE.md 규율대로 없는 걸 오늘로 채우지 않는다. 그게 무거우면 날짜 그룹을 아예 접고 폴더/계열 묶음을 1차 축으로 올린다.
- codex 필요: False

### [P1·broken] mdlite-incomplete
- **어디**: `webapp/app.py:95-139 _mdlite · webapp/static/js/comments.js:34 inline() · webapp/static/js/mdfix.js:31`
- **근거**: 커밋 fc3624184(2026-09-08) 가 /notes 에 `|mdlite` 를 붙였는데 아직 **77건 중 21건이 `**` 를 화면에 노출**한다. 실물 렌더 결과: `**SVR (Support Vector Regression) — 완전히 다른 계열<br>**` (닫는 `**` 앞이 개행이라 `(?<![\s([{<])` 에서 탈락), `<strong>GBRT (**Gradient Boosted Regression Tree</strong>) — 부스팅**` (짝을 잘못 물었다), `<strong>RF, GBRT, XGB, SVR</strong>의 예측 정확도를** MAE, MSE, RMSE, R²<strong>로 평가했다.` (굵기 경계가 엉뚱한 데로 밀렸다). 같은 텍스트를 그리는 렌더러가 넷인데(서버 _mdlite · comments.js inline · mdfix.js · md_html) 지원 문법이 서로 다르다 — _mdlite 는 표·다줄 굵게가 되고 이미지가 안 되고, inline() 은 이미지가 되고 다줄 굵게(`[^*\n]+`)가 안 된다.
- **고치는 법**: 메모 서식의 정본을 하나로 정하고(서버 _mdlite 를 정본으로 두고 comments.js 가 같은 규칙을 따르게) 지원 문법 표를 docstring 에 적는다. 개행 앞뒤 `**` 는 정규식 앞에서 한 번 `\s*\*\*` 로 정리(trim)하고 짝짓기한다. 회귀시험은 지금 깨지는 21건 중 3건을 픽스처로 박는다 — 음성 경로 포함.
- codex 필요: False

### [P1·broken] files-facet-reset
- **어디**: `webapp/templates/files.html:13-23 (form) · 18-21 (kind 탭)`
- **근거**: `/files?kind=image&folder=db/structures` 를 렌더해서 form 안을 보면 컨트롤이 `<input … name="q">` 하나뿐이다(cmt hidden 도 이 경우엔 안 붙는다). kind·used·folder 는 form 밖의 `<a>` 라 GET 제출에 안 실린다 → 검색 버튼을 누르는 순간 `kind=image` 와 `folder=db/structures` 가 조용히 사라진다. 반대로 kind 탭 href 는 `"/files?kind=image&q={{ q }}&cmt={{ cmt }}"` 라 **used 와 folder 를 떨어뜨린다**(folder 탭은 q·kind·used·cmt 를 다 들고 간다 — 세 줄이 서로 다른 규칙이다).
- **고치는 법**: 현재 쿼리를 한 곳에서 만드는 헬퍼(`qs(**overrides)`)를 두고 세 줄이 다 그걸 쓰게 한다. form 에는 kind/used/folder 를 hidden 으로 넣는다.
- codex 필요: False

### [P1·useless] cmt-facet-always-empty
- **어디**: `webapp/templates/files.html:32 · 15 (placeholder) · 71-73 (cmt-badge) · webapp/data.py:5041 _GAL_DIRS`
- **근거**: `💬 코멘트 단 것` 탭의 결과는 **항상 0** 이다: `gallery_files('','','','','yes')` → 0. 코멘트가 달린 파일 20개는 전부 `litdb/figures/…` · `litdb/papers/…` 인데 _GAL_DIRS 는 `[('docs/figures',…),('db/properties',…),('db/structures',…),('docs/uploads',…)]` 라 litdb 를 안 본다. 그래서 카드의 `cmt-badge` 는 1122개 전부 `style="display:none"` 이고, 검색창 placeholder 의 `이름·경로·💬코멘트로 검색` 중 코멘트 갈래(`cmt_hit`)도 절대 안 걸린다.
- **고치는 법**: 둘 중 하나로 정한다 — (a) litdb/figures 를 갤러리에 편입해 이 탭이 실제로 20개를 보여주게 하거나, (b) 탭·배지·placeholder 문구를 지우고 코멘트는 /notes 한 곳으로 모은다. 지금처럼 있으면 '눌러도 아무것도 안 나오는 버튼' 이다.
- codex 필요: False

### [P1·stale] notes-stale-museum
- **어디**: `/notes (webapp/app.py:1036 notes_page · webapp/data.py:5876 notes_by_date)`
- **근거**: 날짜 묶음이 넷뿐이다 — 2026-08-31(1) · 2026-08-28(**70**) · 2026-08-27(5) · 2026-08-05(1), 총 77. 70건은 논문 두 편(tu2026_diffusion_descriptor_ml_li_sse_interface 등)에 하루 몰아 단 세미나 준비 메모다. 2026-09-01~09-08 — LPSOCl 마감 비준(5196c1081) · cascade 보고량 카드 비준(22b00e909) · Nd 어닐 회수(83c868a97) · claim 결속 이주(12e6d0c9b) · QE-GPU ldd(5769e2328) 가 몰린 주간 — 메모가 **0건**이다. 화면은 '최신순 · 총 77건' 이라 살아 있는 기록처럼 보인다.
- **고치는 법**: 빈 게 문제가 아니라 화면이 그걸 말 안 하는 게 문제다. 헤더에 '마지막 메모 2026-08-31 (8일 전)' 을 박고, 최근 7일이 비면 그렇게 적는다. v3 에서는 /notes 를 '작업기록(journal) + 결정 원장 + 메모' 를 한 타임라인으로 합치는 쪽이 맞다 — 지금은 같은 주의 기록이 /log · /governance · /notes 셋으로 흩어져 있다.
- codex 필요: False

### [P1·missing] highlights-orphan
- **어디**: `webapp/app.py:991 api_highlights · webapp/data.py:5736 file_highlights · db/file_highlights.json`
- **근거**: db/file_highlights.json 에 논문 3편 19건의 형광펜이 있다(kim2025_csp_metastable_edge_sharing_sse.md 16건 · deng2026_polysulfate… 2건 · tu2026… 1건). 이걸 보여주는 화면이 **하나도 없다** — /notes 는 db/file_comments.json 만 읽고(notes_by_date), search_index(data.py:3400 근처)도 comment_all 만 넣는다. 그 digest 를 다시 열어야만 보인다. 저장은 되는데 되찾을 길이 없다.
- **고치는 법**: /notes 에 '형광펜' 세 번째 칩을 넣고 file_highlights 를 같은 날짜 타임라인에 섞는다(색·붙인 문장·논문 링크). search_index 에도 `t: "형광펜"` 으로 넣는다. add_file_highlight 가 `at` 을 이미 기록하니 날짜 묶기는 그대로 된다.
- codex 필요: False

### [P1·wrong] deeplink-divergence
- **어디**: `webapp/data.py:5827 comment_all(docstring) · 3405 (search_index) · 5864 note_url`
- **근거**: comment_all 의 docstring 이 이렇게 적혀 있다 — "출처(kind·where·url)를 여기서 한 번만 정해 둔다 — 화면마다 rel 을 다시 파싱하면 규칙이 갈라진다(⌘K 와 /notes 가 서로 다른 링크를 주는 식으로)." 그런데 실제로 갈라져 있다: /notes 는 notes_by_date 가 넣어 준 `c["deep"]`(= `/literature?open=<slug>&note=<id>`) 를 쓰고, ⌘K 색인은 data.py:3405 에서 `"url": c["url"]`(= `/literature?open=<slug>`, note 없음) 를 쓴다. ⌘K 로 메모를 찾아 들어가면 논문만 열리고 그 메모 자리로는 안 간다.
- **고치는 법**: search_index 도 `note_url(c)` 를 쓴다(한 줄). docstring 이 막겠다던 바로 그 증상이다.
- codex 필요: False

### [P2·ia] pdf-no-facet
- **어디**: `webapp/templates/files.html:18-21 · webapp/data.py:4757 _att_kind`
- **근거**: _att_kind 는 image/csv/**pdf**/file 넷을 돌려주고 카드도 `'📕' if f.kind=='pdf'` 로 pdf 를 안다. 그런데 탭은 전체/🖼 이미지/📊 CSV/📦 기타(kind=file) 셋뿐이라 PDF 33개는 `?kind=file` 에도 안 들어간다(kind=file 528 · image 286 · csv 275 · pdf 33 = 1122). 전체 탭에서만 만날 수 있다.
- **고치는 법**: `📕 PDF` 탭을 넣는다. 탭 목록을 _att_kind 가 실제로 내는 값에서 생성하면 다음에 확장자가 늘어도 안 어긋난다.
- codex 필요: False

### [P2·ia] files-no-pagination
- **어디**: `webapp/templates/files.html:43-79 · webapp/app.py:1050`
- **근거**: `/files` 응답이 943,558 bytes · att-card 1123개 · `<img loading="lazy"` 286개다(서버 렌더 0.21 s — 느린 건 서버가 아니라 브라우저 쪽이다). 폴더 facet 은 최상위 3개뿐인데 실제 분포는 db/properties 386 · db/structures/neb_paths 92 · docs/figures/cascade 90 · db/structures 79 … 로 하위가 훨씬 의미 있다.
- **고치는 법**: 날짜 대신 계열(cascade · neb_paths · sdcp_wave1 · dos/pdos · bvse …)을 1차 축으로 올리고 각 묶음은 기본 접힘 + 상위 N개만. 폴더 facet 을 2단계(최상위 → 하위 디렉터리)로 낸다. 전체 나열이 필요하면 '더 보기' 뒤로 보낸다.
- codex 필요: False

### [P2·useless] rename-path-dead
- **어디**: `webapp/templates/files.html:74 · webapp/static/js/rename.js · webapp/app.py:1021 api_file_rename`
- **근거**: ✏ 버튼 조건이 `{% if f.rel.startswith('docs/uploads/') %}` 인데 `docs/uploads` 디렉터리가 **없다**(`ls: cannot access 'docs/uploads'`). 갤러리 1122개 중 docs/uploads 로 시작하는 파일은 0개다. gallery_folders() 도 3개만 돌려준다(_GAL_DIRS 에는 4개가 있는데 존재 검사에서 떨어진다). 즉 /files 에서 ✏ 는 절대 안 뜨고 rename.js·/api/file-rename 은 이 화면에선 죽은 경로다(개념 문서 첨부 쪽에서는 살아 있을 수 있으나 거기는 내 범위 밖이라 확인 안 했다).
- **고치는 법**: 지우는 게 아니라 '어디서 살아 있는지' 를 먼저 확인해야 한다 — /concept 첨부에서 쓰이면 그쪽에만 두고 files.html 에서는 뺀다. _GAL_DIRS 의 docs/uploads 항목도 같이 정리한다.
- codex 필요: False

### [P2·broken] delpen-no-ok-check
- **어디**: `webapp/static/js/docnote.js:466-472 delPen`
- **근거**: `}).then(function () { loadPens(); }).catch(function () { alert("⛔ 통신 실패"); });` — r.ok 검사가 없다. 이 파일의 다른 쓰기 경로는 전부 `then(r => r.json().then(d => ({ok:r.ok,d})))` → `if (!x.ok) alert(...)` 를 한다(:175, :462, :502). 형광펜 삭제만 빠졌다 → 읽기 전용 서버에서 지우면 아무 말 없이 실패하고 loadPens() 뒤에 그대로 돌아온다.
- **고치는 법**: 다른 경로와 같은 모양으로 r.ok 검사 + alert 추가. 세 줄.
- codex 필요: False

### [P2·wrong] notes-invites-write-on-readonly
- **어디**: `webapp/templates/notes.html:26 · 32-33 · webapp/app.py:52 _guard_mutation`
- **근거**: 안내가 `메모는 읽던 문서에서 <b>오른쪽 클릭</b>으로 답니다` 이고 빈 상태 문구는 `아직 메모가 없어요 — 논문 digest 나 개념 문서를 열고 본문에서 오른쪽 클릭해 보세요.` 다. render.yaml 은 `ALLOW_MUTATIONS: "0"` 이라 배포판에서는 저장이 403 이고, 사용자는 메모를 다 쓴 다음에야 comments.js:224 의 `alert("⛔ 읽기 전용 모드예요 …")` 를 본다.
- **고치는 법**: 템플릿에 READ_ONLY 를 내려 주고(context_processor 에 한 줄) 읽기 전용이면 안내를 '이 서버에서는 읽기만 됩니다 — 메모는 로컬에서' 로 바꾼다. 지금 문구는 로컬에서는 맞는 말이라 조건부로만 바꾸면 된다.
- codex 필요: False

### [P2·duplicate] two-day-groupers
- **어디**: `webapp/data.py:5095 gallery_days · webapp/data.py:5876 notes_by_date · webapp/templates/files.html:44-48 · webapp/templates/notes.html:39-43`
- **근거**: 같은 '날짜별 카드 목록' 을 두 벌로 구현했다. gallery_days 는 mtime 기준에 `오늘/어제/{delta}일 전` 라벨(`.day-head/.day-date/.day-rel`)을 붙이고, notes_by_date 는 `at` 문자열 앞 10자 기준에 라벨 없이 날짜만(`.nday/.nday-d/.nday-n`) 낸다. 그래서 나란히 놓으면 같은 패턴이 다르게 보인다.
- **고치는 법**: 묶음+헤더를 한 매크로로 빼고 라벨 규칙(오늘/어제/N일 전)을 공유한다. 단 날짜의 **출처**는 다르니(mtime vs at) 그 사실은 헤더에 명시한다 — 합치면서 mtime 을 진짜 날짜인 척하게 만들면 안 된다.
- codex 필요: False

### [P2·broken] dead-comment-target
- **어디**: `db/file_comments.json 의 `litdb/figures/adeli2019_halide_substitution_boosting_argyrodite/fig_20.png` (2026-08-05)`
- **근거**: comment_all() 77건 중 rel 이 디스크에 없는 게 1건 — 그 fig_20.png 는 지금 repo 에 없다(크로핑 재생성 때 사라진 듯). /notes 카드는 그대로 뜨고 링크는 논문으로 가지만, 그 코멘트가 '어느 그림' 이었는지는 복구가 안 된다. _fig_keys 도 figures.json 에서 못 찾아 키가 빈 문자열이 된다.
- **고치는 법**: /notes 카드에 '대상 파일 없음' 표시를 붙인다(지우지 말 것 — 글은 살아 있는 판단이다). 그림 재크로핑 도구가 파일을 지울 때 file_comments 의 rel 을 같이 옮기거나 최소한 경고하게 한다.
- codex 필요: False

### [P2·wrong] searchindex-parity-comment-false
- **어디**: `webapp/data.py:3351-3371`
- **근거**: 주석이 `# 순서·묶음은 사이드바(base.html)와 같게 — 두 군데가 어긋나면 찾는 사람이 헷갈린다` 인데 실제 pages 리스트에는 사이드바에 있는 Fair-Chem·UMA(/fairchem) · 판정 원장(/governance) · T·Q 원장(/ledger) · Seminar(/seminar) · 1저자 요청(/requests) · SDCP wave1(/sdcp) 이 **없다**. /notes 만 리스트 밖에서 따로 append 된다(:3399).
- **고치는 법**: 사이드바 항목을 한 곳(파이썬 리스트)에 두고 base.html 과 search_index 가 둘 다 그걸 렌더한다. 지금은 주석이 지키겠다고 한 규약을 코드가 안 지킨다.
- codex 필요: False

### [P2·broken] api-csv-no-ext-check
- **어디**: `webapp/app.py:848 api_csv · webapp/data.py:3234 read_csv`
- **근거**: `/api/csv/properties/electronic.json` → **200** 에 `{"columns":["{"],"data":[{"{":"  \"property\": \"electronic_structure\""}, …]}`. JSON 을 쉼표로 쪼개 표로 만들어 돌려준다. read_csv docstring 이 `⛔ 이 함수가 못 하는 것 · CSV 가 맞는지 확인하지 않는다 — 확장자를 안 본다` 로 한계를 정직하게 적어 두긴 했다(그래서 P2).
- **고치는 법**: `.csv`(+`.tsv`) 가 아니면 `{"error": "CSV 가 아니다"}` 로 400. 지금은 200 이라 부르는 쪽이 성공으로 알고 쓰레기 표를 그린다.
- codex 필요: False
