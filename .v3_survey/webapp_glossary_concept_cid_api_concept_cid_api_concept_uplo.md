# webapp — 용어집 · 개념 문서 (/glossary · /concept/<cid> · /api/concept/<cid> · /api/concept-upload · kb/concepts/)

## 지금 무엇인가
/glossary 는 webapp/glossary.py 의 파이썬 리스트 33개 용어를 8카테고리 3열 카드로 뿌리는 한 페이지(HTML 149 KB, 카드는 전부 접힘)이고, 각 카드는 무엇/어떻게/우리 계산(+neb 만 '문헌에서 본 것') 칸으로 돼 있다. /concept/<cid> 는 kb/concepts/*.md 13개를 브라우저 marked + 서버 python-markdown fallback 으로 렌더하고 자동 첨부 갤러리·드래그 업로드·여백 메모를 붙인다. 33개 용어 중 9개만 자기 개념 문서가 있고 13개는 다른 문서의 절로 보내며(doc/doc_sec) 11개는 '더보기'가 아예 없다.

## 처음 오는 사람
할 수 있는 것: 사이드바 '자료·기록' 여섯 번째에서 /glossary 로 들어가면 DFT·SCF·k-point 부터 BVSE·MSD·NEB 까지 33개가 카테고리로 묶여 있고, 카드를 열면 '무엇 → 어떻게(계산·판독) → 우리 계산' 3단으로 개념에서 우리 값까지 이어진다. 이 3단이 이 앱에서 물리는 알지만 계산은 배우는 사람에게 제일 잘 맞는 표면이다. 9개는 '더보기'로 유도·수식이 있는 긴 문서까지 간다.

막히는 지점 (실제로 눌러 보고 확인한 것):
① 홈 부제의 `β 문턱 폐기` 링크가 /glossary#beta-gate 인데 그 페이지에 카드 id 가 하나도 없다 — 맨 위에 떨어지고 정작 β 카드는 접혀 있다. 카드 본문의 "ESW 항목 참조" · "(→ STO/MTO 항목)" · "(→ Adhesion 항목)" 도 전부 평문이다(용어 4칸 전체에서 <a> 0개). 상호참조를 따라갈 방법이 손 스크롤뿐이다.
② 검색창이 term+full+id+'무엇' 만 훑는다. `b2o3` 를 치면 실제로 언급한 10장 중 1장, `철회` 는 6장 중 1장만 남는다 — 철회를 확인하러 온 사람이 못 찾는다.
③ 카드 길이가 157자(MSD)부터 3986자(NEB)까지 25배 차이 난다. NEB 한 장 안에 대칭안장·li3nd 철회·align_check·dimer 철회·VGCF/hBN 갤러리가 다 들어 있어 어디서 끊어 읽어야 할지 모른다.
④ 가장 친절하게 쓰인 최신 문서 4개(msd_reading · neb_intermediate_minimum · oxidation_vs_mechanical · sdcp_self_doping_explainer_2026_08_26)가 /glossary 어디에도 안 걸린다. URL 을 직접 치면 제목이 `msd_reading` 처럼 슬러그 그대로 뜨고, 그 위에 YAML frontmatter 15줄이 커다란 제목으로 박히며 목차 1번 항목도 그 덩어리다.
⑤ 어느 카드에도 '언제 갱신됐나' 가 없다. 갱신일은 파일 frontmatter 에 있는데 화면은 그걸 쓰는 대신 쓰레기로 찍는다.
⑥ 모든 개념 문서 아래에 "파일을 여기로 끌어다 놓으면 첨부돼요" 드롭존이 있는데, 공개 배포(Render)는 읽기 전용이라 떨구면 403 이 오고 화면에는 엉뚱하게 "실패 — 허용되지 않는 형식" 이 뜬다.
⑦ 그리고 배우러 온 사람이 이 repo 에서 제일 자주 마주칠 말 — 보고량 · 닫힘 조건 · 대조 잡 · 허용 서술 범위 — 의 정의가 용어집에 하나도 없다.

못 본 것(정직하게): 브라우저를 띄우지 않았다 — CSS 최종 배치·다크모드·모바일 폭·드래그 업로드 실제 동작·여백 메모(docnote) 동작은 확인 못 했다. marked/KaTeX/mermaid 는 CDN 이고 webapp/static/vendor/ 는 비어 있어(README 만) 실제 브라우저 렌더는 CDN 도달 여부에 달려 있다. litdb 그림은 이번 범위 밖이라 안 봤다.

## 건드리면 안 되는 것
- '무엇 / 어떻게(계산·판독) / 우리 계산' 3칸 구조 (webapp/glossary.py 항목 스키마 + glossary.html:26-28). 물리는 알고 계산은 배우는 독자에게 맞춘 CLAUDE.md 소통 규칙이 그대로 구현된 자리다. v3 에서 카드 수를 줄이더라도 이 3칸은 유지한다.
- '문헌에서 본 것'(lit) 칸의 분리와 주황색 스타일 (glossary.html:29-34, 63-67 · glossary.py:203-210 neb). 주석에 이유가 있다 — "우리 값과 문헌 소환값이 한 칸에 섞이면 안 된다(litdb 규율)". '우리 계산' 과 합치거나 같은 색으로 만들면 안 된다. 오히려 다른 카드로 늘려야 할 패턴이다.
- 철회 표시 span 과 data-claim 결속 (glossary.py:190-191 의 `data-claim='MD_Ea_eV@b2o3'` · `data-claim='HZ-cross-system-Ea'` + 취소선 + ⛔). 회신 BG ② 이주(커밋 12e6d0c9b)의 산물이라 지우면 원장 결속이 끊긴다. 문구를 고칠 때도 span 과 claim id 는 남긴다.
- glossary_papers 의 '선언이 있으면 선언만' 규칙 (data.py:3771-3793). 예전 '태그 ∪ 토큰스캔' 이 deng2026 의 부정문("이 논문은 NEB·Bader·COHP·ELF·BVSE·phonon 을 하지 않는다")과 kim2025_csp 의 정정 주석을 긁어 오답을 냈고, 회귀시험(test_webapp.py:2576)이 그걸 지킨다. 합집합으로 되돌리지 않는다.
- artifact_policy 의 fail-closed ('미등록 = 미승인', webapp/artifact_policy.py). cascade-403 발견은 정책을 느슨하게 하라는 뜻이 아니다 — 고칠 곳은 첨부 수집기(_auto_matched)이지 정책이 아니다.
- '본문 = 진실의 근원' 불변식 (data.py:4851-4880 concept_attachments · 4995-5040 save_concept_upload). 첨부 목록을 별도 테이블로 빼면 문서와 어긋난다는 것이 도입 사유고, 업로드가 본문 끝에 경로를 append 하는 것도 같은 이유다. 별도 첨부 DB 를 만들지 않는다.
- XSS 이중 방어 — 서버 md_html 의 raw HTML 차단 + _sanitize_urls(app.py:151-178, 207-209)와 브라우저 sanitizeHTML(concept.html:206-246). 개념 문서를 에이전트가 외부 PDF 요약으로 쓰기 때문에 넣은 것이고, marked 경로는 서버 방어를 안 거치므로 둘 다 필요하다.
- 경로 탈출 방어 — read_concept 의 is_relative_to(data.py:58-63), safe_repo_path(data.py:4801-4812), rename_upload 의 uploads 밖 금지(data.py:4917-4925).
- doc / doc_sec 필드 (예: scf→dft §8, msd→md §3, d-inc→beta-gate §7-8b). 2026-08-04 전수 감사로 생긴 것이고 지금 13개 용어가 이걸로 상세 문서에 닿는다. 자기 문서가 없다고 '더보기' 를 없애면 그 13개가 막다른 길이 된다.
- 빈 카테고리 접기 + 빈 검색 안내 (glossary.html:9-11 #gl-empty, 75-79 의 .gsec 숨김). 검색했을 때 제목만 줄줄이 남는 것을 막는 장치다.
- 카테고리 누락 회귀시험 (test_webapp.py:2725-2752 test_every_glossary_term_reaches_a_rendered_category). CATS_G 에 없는 카테고리를 쓰면 용어가 화면에서 통째로 사라지는 것을 음성 프로브까지 넣어 잡는다. 카테고리를 개편하더라도 이 시험은 같이 옮긴다.
- kb/concepts/*.md 본문 자체 — 특히 md.md §6 의 Haven 부호 정정 표(0.84±0.06 vs Adeli 0.23, '곱하지 않는다')와 beta-gate.md 의 반론 절. kb 규율상 반론 절 삭제 금지다. 위 발견의 수정은 문구 교체·링크 추가이지 문단 삭제가 아니다.
- 서버 렌더 fallback 경로 (app.py:1213 `fallback = md_html(md)` + concept.html:176 의 `if (typeof marked !== 'undefined' && raw)`). webapp/static/vendor/ 가 비어 있어 CDN 이 막히면 이 경로만 남는다 — 지우면 에어갭에서 화면이 빈다.

## 발견

### [P0·wrong] haven-contradiction
- **어디**: `kb/concepts/msd_reading.md:50, :343  ↔  kb/concepts/md.md:190-195 (/concept/msd_reading vs /concept/md)`
- **근거**: msd_reading.md:50 "`q` = e · Haven ratio 1 = **상한 가정**." / :343 "NE(Haven=1)은 상한이고". 같은 앱의 md.md:190 "⛔ 2026-09-07 정정 — **\"$H_R=1$ 이라서 상한\" 은 부호가 틀렸다**" / :195 "**\"상한\" 의 근거로 Haven 을 대면 안 된다.**" md.md 는 커밋 fb542dce2(2026-09-07)로 H_R = 0.84±0.06 실측까지 실었다. 두 라우트 모두 200 이고, msd_reading 은 md.md 를 6번 인용한다.
- **고치는 법**: msd_reading.md:50 의 `Haven ratio 1 = 상한 가정` → `Haven=1 은 상관 무시 근사 — H_R<1 이면 NE 가 과소(부호 정정 2026-09-07, md.md §6)` 로 교체하고 :343 의 '상한이고' 를 '방향이 정해지지 않아' 로 바꾼다. 같은 양을 두 문서가 각자 말하는 것이 원인이므로 Haven 문단은 md.md §6 한 곳만 두고 msd_reading 은 링크만 건다.
- codex 필요: False

### [P0·wrong] b2o3-interval-ea-forbidden
- **어디**: `webapp/glossary.py:191 (arrhenius · /glossary '이온 수송')`
- **근거**: 화면 문구: "<s>b2o3 0.199±0.034</s> ⛔ 철회 (2026-08-23) — … 아레니우스가 800 K 위에서 굽는다(600→800 **0.222** / 800→1000 0.077 eV). **저온 구간 Ea 로만 쓴다**". db/properties/b2o3_md_closed_retrospective_2026_08_25.json 의 금지_서술 첫 줄은 "⛔ b2o3 의 D · Ea · σ · **구간 Ea** 중 **어느 것도** 물질 값으로 인용 — **0.222 eV 포함**" 이고 확정값은 "⛔ 없다. 이 축에서 인용 가능한 수는 0개다" 다. 마감은 D-2026-09-07-b2o3-md-closure-retrospective 로 active.
- **고치는 법**: '저온 구간 Ea 로만 쓴다' 절과 0.222/0.077 두 수를 지우고 "⛔ 축 전체 마감 (2026-08-25, 소급기록 09-07) — 인용 가능한 수 0개 · 상태명 closed_no_action / non-citable" 로 교체하고 마감 json 으로 링크한다.
- codex 필요: False

### [P0·broken] frontmatter-dumped-as-heading
- **어디**: `webapp/data.py:58-63 (read_concept) · webapp/app.py:151-178 (md_html) · webapp/templates/concept.html:231, 276-287`
- **근거**: kb_wiki 로 만든 4개(msd_reading · neb_intermediate_minimum · oxidation_vs_mechanical · sdcp_self_doping_explainer_2026_08_26)만 YAML frontmatter 를 갖는데 어느 경로도 안 벗긴다. 서버 fallback 실측: `<hr /><p>title: "MSD 그림을 읽는 법 …" date: 2026-09-07 … evidenceScope: multi-source-primary</p><hr />`. 브라우저 경로(marked 12.0.2 로 직접 실행해 확인)는 setext 규칙에 걸려 그 15줄이 통째로 <h2> 가 되고, concept.html:277 의 `querySelectorAll('h2')` 목차가 그것을 1번 항목으로 싣는다(msd_reading h2 11개 중 1개, oxidation_vs_mechanical 29개 중 1개).
- **고치는 법**: read_concept 에서 선행 `---\n…\n---` 를 떼어 dict 로 파싱하고 본문만 렌더한다. 뗀 updated·status·confidence 는 버리지 말고 concept 헤더 배지로 올린다.
- codex 필요: False

### [P0·wrong] sei-neb-retracted-attachments
- **어디**: `/concept/neb 첨부 목록 (webapp/data.py:4813-4831 `_CONCEPT_FILE_RULES["neb"]=("neb",)` · concept.html:96-107)`
- **근거**: /concept/neb 첨부 23건 중 7건이 sei_neb 계열이고 목록 맨 위가 db/properties/sei_neb.json 이다. 그 파일 안: `"retracted": true`, `"n_citable": 0`, `"retraction_reason": "인용 가능한 결과가 0건이다. … 이 파일의 어떤 값도 인용하지 말 것."` db/properties/citation_hazards.json 도 같은 파일을 `level: BLOCKED · "전량 철회 (retracted=true, n_citable=0)"` 로 싣는다. 화면 카드는 `📦 sei_neb.json · 🔗 · ⬇ 저장` 뿐이고 철회 표지가 하나도 없다 — 클릭하면 모달에 원본 JSON 이 그대로 뜬다(concept.html:392-396). 같은 계열 CSV 3개(sei_neb_mep/images/barriers_origin.csv)와 그림 4장도 같다.
- **고치는 법**: concept_attachments 가 카드마다 citation_hazards + `retracted` 를 읽어 `⛔ 철회 (n_citable=0)` 배지와 사유 툴팁을 붙인다. 배지는 무조건 붙이고, 다운로드 버튼을 남길지 막을지는 governance 판단이라 별도로 묻는다.
- codex 필요: True

### [P1·stale] b2o3-600k-hedge
- **어디**: `webapp/glossary.py:237 (framework_gate · /glossary 'MLIP·자동화')`
- **근거**: 화면 문구 끝: "다만 **600 K 는 2/3 rigid** 라 **800 K 이상만 확실히 무효**다." 마감 기록(b2o3_md_closed_retrospective_2026_08_25.json, 09-07 작성)은 "**600 K 도 1/3 이 0.55**" 이고 닫는 범위가 "UMA-MD 전도도 축 **전체** — D · Ea · σ · 구간 Ea", 확정값이 "인용 가능한 수는 0개" 다. 즉 '600 K 는 살아 있을 수 있다' 로 읽히는 문장이 비준된 마감과 어긋난다.
- **고치는 법**: 마지막 문장을 "600 K 도 3시드 중 1개가 0.55 였고, 이 축은 온도와 무관하게 통째로 마감됐다 (closed_no_action / non-citable)" 로 교체.
- codex 필요: False

### [P1·broken] cascade-attachments-403
- **어디**: `/concept/beta-gate · /concept/bvse · /concept/elastic · /concept/ordered_vs_disordered 첨부 카드 8개 (webapp/data.py:4832-4849 `_auto_matched` ↔ webapp/artifact_policy.py)`
- **근거**: 8개 링크를 전부 눌러 확인했고 전부 403. docs/figures/cascade/msd_b2o3_vs_modelc.png · msd_modelc_comp1.png · bvse_channel_volume.png · bvse_channel_2p5d.png · b2o3_eos_dft_vs_modelc.png · .pdf · b2o3_voronoi_disorder.png · db/properties/cascade_v23_eos_refit.json. AP.resolve 사유는 "원장(cascade_audit_manifest.json)에 없는 cascade artifact 다 — 미등록은 미승인으로 다룬다" 이고 needs=None 이라 ?archive=1·?view=diagnostic 어떤 파라미터로도 안 열린다. 8건 전부 src=auto(본문 인용이 아니라 접두사 규칙이 끌어온 것). 카드는 `<img src="/api/file/…">` 라 화면에는 깨진 썸네일 8장 + 눌러도 403 나는 저장 버튼으로 나온다.
- **고치는 법**: `_auto_matched` 끝에 `artifact_policy.resolve(rel, {})['allowed']` 필터를 건다. 정책을 느슨하게 하는 방향은 금지(fail-closed 가 설계다). 본문이 명시 인용한 governed 파일은 지우지 말고 '원장 미등록 — 볼 수 없음' 회색 카드로 남긴다.
- codex 필요: False

### [P1·ia] orphan-concept-docs
- **어디**: `webapp/glossary.py:10-244 (GLOSSARY) ↔ kb/concepts/ · webapp/templates/concept.html:11 · webapp/data.py:3390-3392`
- **근거**: 개념 문서 13개 중 msd_reading · neb_intermediate_minimum · oxidation_vs_mechanical · sdcp_self_doping_explainer_2026_08_26 4개가 GLOSSARY id 집합에 없다. /glossary 어디에도 링크가 없고 ⌘K 색인(data.py:3391)에만 `label = cid.upper()`, `sub = "상세 개념 문서"` 로 들어가 `SDCP_SELF_DOPING_EXPLAINER_2026_08_26` 같은 이름으로 뜬다. 직접 열면 concept.html:11 의 `{{ term.term if term else cid }}` 때문에 h1 이 `msd_reading` 이고, term=None 이라 카테고리 배지도 '같은 분야 개념 문서' 블록도 안 나온다(4개 모두 렌더해 확인). 하필 이 4개가 최근에 쓴, 처음 온 사람 대상 설명 카드다.
- **고치는 법**: ① 이 4개에 GLOSSARY 항목을 만들거나(msd_reading = 'MSD 판독', sdcp_self_doping = '자기도핑' 등) ② /glossary 하단에 '용어에 안 걸린 설명 문서' 섹션을 둔다. 어느 쪽이든 concept.html 의 h1 fallback 을 슬러그가 아니라 본문 첫 H1(또는 frontmatter title)로 바꾼다.
- codex 필요: False

### [P1·broken] no-anchors-no-crosslinks
- **어디**: `webapp/templates/glossary.html:12-53 · webapp/templates/index.html:14 · webapp/glossary.py:39, 108, 202, 237`
- **근거**: /glossary 렌더 결과에 `id="beta-gate"` 없음 — 페이지 전체 id 13개가 railbtn·nav-*·main·gl-empty·cmdk*·toast 뿐이다. 그런데 index.html:14 가 `<a href="/glossary#beta-gate">β 문턱 폐기</a>` 로 홈 부제에서 거기로 보낸다. 카드 본문 상호참조도 링크가 아니다 — what/how/ours/lit 전체에서 `<a href=` 가 0개인데 참조 문구는 "ESW 항목 참조"(bandgap) · "(→ STO/MTO 항목)"(beta-gate) · "(→ Adhesion 항목)"(neb) · "(→ 절대 바닥 항목)"(framework_gate) 등 5군데다.
- **고치는 법**: 카드에 `id="{{ g.id }}"` 를 넣고 로드 시 location.hash 에 맞는 카드를 열고 스크롤한다. 본문 참조는 `<a href="#esw">ESW</a>` 식 같은 페이지 앵커로 바꾼다(새 라우트 불필요).
- codex 필요: False

### [P1·useless] search-index-misses-ours
- **어디**: `webapp/templates/glossary.html:17 `data-t="{{ g.term|lower }} {{ g.full|lower }} {{ g.id }} {{ g.what|striptags|lower }}"``
- **근거**: 색인이 term·full·id·what 만 담고 how/ours/lit 을 뺀다. 실측: `b2o3` 는 실제 언급 10장 중 검색으로 1장(놓침 arrhenius·bader·bvse·dos·elf·framework_gate·md·pdos·sto-mto), `철회` 는 6장 중 1장(놓침 arrhenius·framework_gate·neb·ordered_vs_disordered·time-vs-ions), `uma` 6장 중 2장, `lobster` 5장 중 2장, `아레니우스` 3장 중 1장. 철회·인용금지가 거의 다 '우리 계산' 칸에 있어서 정확히 확인이 필요한 검색어가 다 빠진다.
- **고치는 법**: data-t 에 `{{ g.how|striptags|lower }} {{ g.ours|striptags|lower }} {{ g.lit|striptags|lower }}` 를 더한다(한 줄). 페이지가 이미 149 KB 라 추가분은 무시할 수준이다.
- codex 필요: False

### [P1·wrong] readonly-dropzone-lies
- **어디**: `webapp/templates/concept.html:115-122, 352-359 · webapp/app.py:52-63, 929-939`
- **근거**: ALLOW_MUTATIONS=0 으로 띄워 POST /api/concept-upload/dft → 403 `{"error":"읽기 전용 모드예요 — 이 서버에서는 저장이 꺼져 있어요.", "why":…, "how":…}`. 같은 조건에서 /concept/dft 에 드롭존이 그대로 렌더된다("파일을 여기(또는 페이지 아무 데나)로 끌어다 놓으면 이 문서에 첨부돼요" 문자열 존재 확인). JS 는 d.saved/d.rejected 만 읽어 `((d.rejected || []).join(', ') || '허용되지 않는 형식')` 로 떨어지므로 화면에는 "실패 — 허용되지 않는 형식" 이 뜬다. RENDER 환경변수가 있으면 기본이 읽기 전용이라 외부인은 항상 이 거짓말을 본다.
- **고치는 법**: ① 템플릿에 READ_ONLY 를 넘겨 읽기 전용이면 드롭존 대신 한 줄 안내로 바꾼다. ② JS 오류 분기에서 d.error·d.how 를 우선 표시한다.
- codex 필요: False

### [P1·missing] values-without-source
- **어디**: `webapp/glossary.py — 'ours' 필드 33개 중 24개`
- **근거**: 출처(db/·kb/·tools/·.json·.csv)를 한 글자도 안 대는 카드가 24장이다: dft·scf·pseudo·kpoint·functional·pdos·cohp·cobi·lobster·eos·elastic·bvse·md·msd·d-inc·lag-tier·sto-mto·pmf·arrhenius·phonon·esw·mlip·abs_floor·framework_gate. 그 안에 맨숫자가 그대로 있다 — eos "comp1 26.23 / comp2 25.8 / modelc 21.71 / lpsocl 24.71 GPa", cohp "comp1 −5.938 / comp2 −5.913", pmf "ΔF_perc 0.173 eV vs BV 0.228", elastic "comp2 E_VRH 20.03 < comp1 22.06". 출처를 대는 카드는 9장뿐(bandgap·dos·elf·bader·beta-gate·time-vs-ions·neb·adhesion·ordered_vs_disordered).
- **고치는 법**: GLOSSARY 항목에 `src: ["db/properties/…json", …]` 필드를 추가해 카드 하단에 출처 칩을 자동으로 그린다. 원장에 없으면 칩 자리에 '원장 부재' 를 찍는다 — 빈칸이나 0 으로 두지 않는다.
- codex 필요: False

### [P1·missing] no-governance-vocabulary
- **어디**: `webapp/glossary.py 전체 · /glossary '방법론·모델링'(2장뿐)`
- **근거**: `grep -c "보고량\|estimand\|대조 잡\|닫힘 조건\|허용 서술\|claim ceiling" webapp/glossary.py` = 0. CLAUDE.md 가 2026-08-28 에 채택하고 09-01 에 용어까지 개정한 규율(보고량 카드 · 마감/닫힘 조건 · 대조 잡 · 허용 서술 범위 · 사전등록·봉인)이 이 repo 에서 제일 자주 쓰이는 개념인데(09-07~08 에만 D-2026-09-08-lpsocl-box331-closure-conditions · D-2026-09-08-cascade-d-rel-estimand 두 건 비준) 용어집에 정의가 하나도 없다. /governance 에 원장은 있지만 '이게 무엇인가' 를 배울 자리는 /glossary 뿐이다.
- **고치는 법**: '연구 규율' 카테고리를 신설해 최소 5장(보고량 · 닫힘 조건/마감 · 대조 잡 · 허용 서술 범위 · 사전등록·봉인)을 만들고, '우리 계산' 칸은 kb/templates/estimand_card.md · db/governance/decisions.json · db/properties/*_closed_*.json 을 실제 사례로 링크한다. 기계 필드명(estimand·canary)은 안 바꾸고 부르는 이름만 한국어로 쓴다.
- codex 필요: False

### [P2·ia] neb-card-three-topics
- **어디**: `webapp/glossary.py:199-210 (neb — 'ours' 한 칸만 3986자)`
- **근거**: 카드 길이 실측: neb 3986자 · beta-gate 2503 · sto-mto 1479 … 반대쪽은 msd 157 · adhesion 166 (25배 차이). neb 'ours' 한 칸에 (a) symmetric_saddle 2026-08-16 (b) li3nd 3×3×3 근거 철회·--align_check (c) dimer '싼 우회로 없다' 철회 (d) 협동 이동 명명 규약 (e) VGCF/hBN 갤러리 확산(전혀 다른 계) 다섯 덩어리가 줄글로 붙어 있다. 3열 그리드 카드 안이라 한 화면을 넘긴다.
- **고치는 법**: neb 카드는 개요만 남기고 (b)(c)(d) 는 kb/concepts/neb.md 로 옮겨 '더보기' 로 보낸다. (e) VGCF/hBN 은 별도 용어(gallery-diffusion 등)로 뗀다. 카드 안에 접힘(details)을 두어 최신 몇 줄만 펴 둔다.
- codex 필요: False

### [P2·useless] empty-attachment-header
- **어디**: `webapp/templates/concept.html:41-43, 115-122`
- **근거**: 첨부 0인 문서(/concept/oxidation_vs_mechanical · /concept/sdcp_self_doping_explainer_2026_08_26)에서도 헤더가 그대로 나온다 — 렌더 원문: `<div class="section-title">첨부 · 0 <span …>— 📌 본문 인용 0 · 🔗 자동 연결 0 · 클릭 미리보기 · 파일을 끌어오면 추가</span></div>` 바로 아래 커다란 `⤵` 드롭존. 이미지·데이터 탭은 `{% if imgs or data %}` 로 숨는데 헤더와 드롭존만 조건이 없다.
- **고치는 법**: `{% if attachments %}` 로 헤더를 감싸고, 0건이면 드롭존만(그것도 쓰기 가능할 때만) 한 줄로 줄인다.
- codex 필요: False

### [P2·duplicate] glossary-vs-concept-duplication
- **어디**: `webapp/glossary.py:109, 154 ↔ kb/concepts/beta-gate.md:527 (그리고 md/arrhenius ↔ md.md 전반)`
- **근거**: 같은 수치가 두 곳에 손으로 복사돼 있다. glossary.py:109 "같은 런을 STO 로 읽으면 시드 산포가 <b>8.7배</b>(0.52 vs 0.06)" ↔ beta-gate.md:527 "시드 산포가 STO 0.52 vs MTO 0.06, 8.7배". glossary.py:154 "MTO 로는 0.76/0.76/0.81 · STO 로는 0.85/0.83/0.80" 도 같은 계열. 이 복사가 실제로 갈라진 사례가 haven-contradiction 이다(md.md 는 09-07 에 고쳐졌고 msd_reading 은 안 고쳐졌다).
- **고치는 법**: 값은 db/properties JSON 한 곳에 두고 glossary 카드는 개요 + 링크로 줄인다. 최소한 tools/convention_check.py 에 'glossary.py 와 kb/concepts 가 같은 수를 다르게 말하는가' 검사를 추가한다.
- codex 필요: False

### [P2·missing] no-updated-date-on-screen
- **어디**: `webapp/templates/glossary.html:17-24 · webapp/templates/concept.html:8-18`
- **근거**: 카드 헤더는 term + full + '📄 상세' 칩뿐이고 개념 문서 헤더는 crumb + h1 + 카테고리 배지 + 🖨 인쇄 버튼뿐이다. 어디에도 날짜가 없다. 정작 4개 문서 frontmatter 에는 `updated: 2026-09-07`, `verifiedAt`, `confidence`, `status` 가 들어 있는데 지금은 본문 쓰레기로 나온다(frontmatter-dumped-as-heading). 철회·마감이 자주 바뀌는 repo 에서 '이 설명이 언제 것인가' 를 화면에서 알 길이 없다.
- **고치는 법**: frontmatter 파싱하는 김에 updated·status·confidence 를 concept 헤더 배지로 올린다. frontmatter 없는 옛 9개는 '갱신일 미기재' 로 찍는다(0 이나 today 로 채우지 않는다). GLOSSARY 항목에도 updated 필드를 추가해 카드에 표시하고 카테고리 안 정렬 키로 쓴다.
- codex 필요: False

### [P2·broken] dead-heading-anchors
- **어디**: `webapp/templates/concept.html:231 (`headerIds:true`), :276-287 (TOC) ↔ webapp/templates/compare.html:378, 462`
- **근거**: compare.html 이 두 곳에서 `/concept/dft#12-활성화-에너지는-방법마다-다른-양이다--bv--neb--md-2026-08-05` 로 링크한다. 서버 렌더 실측: /concept/dft 본문 h2 14개 중 id 를 가진 것 0개, `12-활성화` 문자열 없음. 브라우저 경로도 같다 — marked 12.0.2 에서 headerIds 는 제거된 옵션이라 무시된다(직접 실행해 `<h2>12. 활성화 에너지는 …</h2>` 로 id 없음을 확인). TOC 는 concept.html:282 가 `h.id = 'h'+idx` 로 뒤늦게 붙여 페이지 안에서는 되지만, 위치 기반 id 라 절이 하나 추가되면 외부 딥링크가 전부 어긋난다.
- **고치는 법**: marked-gfm-heading-id 를 쓰거나 서버 md_html 에 python-markdown `toc` extension 을 켜서 안정적 슬러그를 만들고 TOC 가 그 id 를 쓰게 한다. 그 전까지 compare.html 의 두 딥링크는 /concept/dft 로 낮춘다.
- codex 필요: False

### [P2·stale] md-card-b2o3-seed-anchor
- **어디**: `webapp/glossary.py:99 (md · 'ours')`
- **근거**: 화면 문구: "modelc의 멀티시드 값은 3-seed×3-T 0.197±0.032, **b2o3 3-seed**, LPSOCl 4-seed, comp2 3-seed. 조성 간 비교는 같은 시드 프로토콜끼리만." b2o3 를 살아 있는 프로토콜 앵커로 나열하는데 같은 페이지 framework_gate 카드는 b2o3 를 ⛔ 로 찍고 마감 원장은 그 축 전체를 non-citable 로 닫았다. 한 페이지 안에서 두 카드가 다른 지위를 말한다.
- **고치는 법**: `b2o3 3-seed` 뒤에 `(⛔ 골격 게이트 탈락 — 수송축 마감, 2026-08-25)` 를 붙이거나 목록에서 빼고 framework_gate 카드로 링크한다.
- codex 필요: False
