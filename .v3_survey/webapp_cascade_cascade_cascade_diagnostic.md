# webapp — cascade 스크리닝 (/cascade · /cascade/diagnostic)

## 지금 무엇인가
Li₆PS₅Cl 호스트에 도펀트 91종을 UMA 로 걸러낸 캠페인의 **감사 화면**이다 — 결과 화면이 아니고, 화면 스스로 "승인된 current ranking 0종"이라고 못박는다. 10개 탭 · 카드 57장 · 표 32개 · 렌더 HTML 557 KB 로 이 앱에서 가장 큰 페이지이며, 47종 리더보드는 `?archive=1`, 후보명·89행 랭킹은 `/cascade/diagnostic?view=diagnostic` 로 서버가 fail-closed 게이팅한다. ⛔ 다만 화면 어디에도 회신 AL NO-GO · 2026-09-08 비준된 보고량 카드 · 같은 날 봉인(v2_2026_09_08)이 **한 글자도 없다** — 화면이 말하는 최신 날짜는 2026-08-25 다.

## 처음 오는 사람
처음 온 사람에게 이 화면은 **"무엇을 알아냈나"를 묻는 곳이 아니라 "왜 아직 아무것도 말할 수 없나"를 20분간 읽는 곳**이다. 좋은 점은 진짜로 있다 — 최상단 «이 페이지가 무엇인가» 카드가 cascade 를 "싼 계산부터 비싼 계산 순서로 떨어뜨리는 폭포"라고 설명하고, «✅ 말할 수 있다 / ⛔ 말할 수 없다» 2단 카드가 있고, 기초/심화 배지(.lv-b/.lv-a)로 난이도를 나눈다. 이 셋은 다른 라우트에 없는 자산이다.

막히는 지점은 넷이다. ① **숫자 체계가 두 개**다. 카드가 "숫자 네 개가 각각 무엇인가 — 3,615 / 681 / 90 / 47"을 가르치는데, 바로 아래 타일은 **273 / 270 / 90 / 47 / 0 / 0** 이다. 273·270 은 카드가 한 번도 설명하지 않는다. 방금 배운 어휘가 두 줄 아래에서 안 통한다. ② **현재 상태를 알 수 없다.** 캠페인이 2026-08-30 회신 AL NO-GO 로 멈춰 있고 해제조건 8개 중 넷이 2026-09-08 에 닫혔다는 사실이 화면에 없다. 처음 온 사람은 "이거 지금 돌고 있나, 멈춰 있나, 뭘 기다리나"를 알 방법이 없고, /governance 나 /ledger 로 가는 링크도 0개다. ③ **읽는 순서가 뒤집혀 있다.** 기본 탭(📋 현황·감사)의 첫 두 카드가 «심화» 배지 달린 MLIP 순위 실패론과 ML 절차 비교론이고, 정작 «그래서 지금 인용할 수 있는 것 / 없는 것» 표는 그 탭 35,826 바이트 중 **34,837 바이트 지점, 즉 맨 끝**에 있다. ④ **경고가 너무 많아 경고가 안 보인다.** 기본 화면에 ⛔ 30회 · ⚠ 59회 · callout 43개다. 그중 하나(«⚠ verified 서브셋에 미해소 값 충돌») 는 이미 2026-08-12 에 해소된 건인데 아직 빨간 위험으로 떠 있고, 그 안에 파이썬 dict 원문(`{&#39;resolution&#39;: …}`)이 그대로 노출돼 있다 — 진짜 경고와 잔해가 같은 빨간색이다.

한 문장으로: **이 화면은 "믿지 마라"는 말을 아주 잘 하고, "지금 어디까지 왔고 다음은 무엇인가"는 전혀 못 한다.**

## 건드리면 안 되는 것
- **fail-closed 게이팅 3종 전부** — app.py:344-383 의 `archive=1` / `view=diagnostic` 분기, `/cascade/diagnostic` 의 403(렌더 자체를 안 함), `/api/file` 의 manifest 미등록=미승인 403. 이건 Codex P0-5·Round-3 P1 이 두 번 잡아서 만든 장치이고, '경고 배너 붙이고 DOM 에는 실어 보내기' 로 되돌리면 같은 사고가 재발한다. 위 v1-47species 항목의 수정 방향은 이 게이트를 **넓히는 것**이지 푸는 게 아니다.
- **타일의 manifest 파생 + fail-closed** — cascade.html:175-185 의 `{% if not T.ok %}` 분기와 `T.tiles`. 숫자를 추측해 띄우느니 아무것도 안 띄우는 설계이고 test_manifest_tamper_fails_closed 가 위조 시나리오까지 시험한다. 하드코딩으로 되돌리지 말 것.
- **'0종' 자체는 지우지 말 것** — `승인된 current ranking 0종` · `explicit pair 라벨 0` 은 원장에 근거가 있는 진짜 0 이다(manifest `approved_current_ranking_species`). 위에서 문제 삼은 0 은 **게이트 때문에 0 이 된 파생 숫자**(리더보드 0종·Pareto 0건·테마 0개 도펀트)뿐이다. 둘을 같이 지우면 화면이 승인 상태를 잃는다.
- **superseded / diagnostic 탭 4개(🗄 47종 리더보드 · 🗄 47종 깔때기 · 🔁 90종 회수분 · 🛡 안정성 3축)와 tabstate() 배지** — '무엇으로 만든 표인가 + 왜 결과가 아닌가' 를 붙이라는 2026-08-14 Codex P0-4 의 산물이다. 접거나 게이팅하는 건 좋지만 **삭제 금지**. 특히 🛡 탭은 우리 자신의 M6 vacuous 판정을 뒤집은 음성 결과의 근거다.
- **«회수로 뒤집힌 서술» 카드(559-568행)** — 47종 문안을 그대로 뒀으면 계속 틀린 채 남았을 것들의 목록. 정정 이력이라 요약·압축하면 가치가 사라진다.
- **«⚠ 이 축의 근본 한계»(239-281행)와 «🔍 우리가 안 한 세 단계»(286-339행)** — 위에서 '맨 앞에 있어서 묻는다' 고 적었지만 그건 **위치** 문제다. 내용(Kalikadien 44–84 % 랭킹 신뢰율 · 저자 면책을 우리 실패에 쓰지 말라는 단락 · LODO −0.1805 vs 저쪽 R² 0.99 의 CV 설계 차이)은 이 repo 가 스스로 얻은 판정이라 그대로 보존하고 `<details>` 로 옮기기만 한다.
- **FORBIDDEN 마커 블록(379·400행)** — `<!--FORBIDDEN-->…<!--/FORBIDDEN-->` 는 회귀 테스트가 '금지 문구 예시' 를 본문 검사에서 걷어내는 장치다. 마크업을 정리하다 이 주석쌍을 지우면 경고문 자체가 위반으로 잡혀 테스트가 깨진다.
- **`data-claim-not="MD_Ea_eV@b2o3"` 부인 래퍼(1264-1266행)** — 회신 BG ② 의 claim 결속 산물이다. codoping 표의 `window_gain 0.199` 가 b2o3 MD Ea 0.199 eV 와 글자만 같아 결속 검사에 걸리는 것을 이름을 대서 부인한 것. 표를 옮기거나 감쌀 때 이 래퍼를 같이 옮기지 않으면 미결속이 생긴다.
- **엔진 카드의 4개 문장(118-125행: engine / score_formula / caveat / verified)** — 특히 `verified` 의 'DFT 심층검증은 Nd₂O₃·B₂O₃ 2건뿐' 과 `caveat` 의 '절대 탄성값은 실험 대비 높게 나옴 — 캐스케이드 내부 순위·상대비교만'. 짧지만 이 화면 전체의 서술 범위를 정하는 문장이다.

## 발견

### [P0·stale] al-nogo-and-estimand-absent
- **어디**: `webapp/templates/cascade.html:30-228 (페이지 전체) · webapp/app.py:344-383 (cascade_page)`
- **근거**: 렌더된 /cascade 557,619 바이트 전체에서 'NO-GO' 0회 · 'D_rel' 0회 · '보고량' 0회 · '해제조건' 0회 · '봉인' 0회 · 'estimand' 0회 (grep 실측). 템플릿 소스에도 같은 문자열이 하나도 없다. 반면 db/properties/cascade_d_rel_estimand_2026_09_08.json 은 `"status": "ratified"` · `"⚠_base_commit_이_아니다"` 까지 갖춘 1저자 비준 카드이고, db/properties/cascade_seal_v2_2026_09_08.json 은 `sealed_at 2026-09-08T14:41:28` 로 도구 9종의 sha256 을 봉인했다. 화면에 뜨는 최신 날짜는 **2026-08-25** 다(날짜 문자열 실측: 07-28×61, 07-27×38, 06-29×7, 08-14×4, 08-25×1 — 08-28·08-30·09-07·09-08 은 0회). cascade.html 이 마지막으로 손댄 커밋 12e6d0c9b 이후 HEAD 까지 26 커밋이고 그중 cascade #7 봉인 6건·보고량 카드 비준 2건이 전부 화면 밖이다. 같은 카드가 대시보드(/)에는 '⭐ cascade D_rel 보고량 카드 비준' 으로 떠 있다(webapp/data.py:4662-4682) — 정작 cascade 페이지만 모른다.
- **고치는 법**: 타일 바로 아래(현재 '승인된 랭킹 0건' 배너 자리)에 **캠페인 지위 밴드**를 신설한다: ① 회신 AL NO-GO (2026-08-30) · ② 비준된 보고량 D_rel(600 K · 2–50 ps · cell-conditioned, 2026-09-08) · ③ 남은 해제조건 #3·#4·#7·#8 · ④ 봉인 v2_2026_09_08. 값은 하드코딩하지 말고 data.py 의 `_closure_and_prereg_cards()` 가 이미 읽는 두 JSON 을 그대로 재사용해 cascade 라우트에 넘긴다(대시보드와 같은 원장 → 중복 아님, 동기화됨). '왜 멈춰 있나'는 P0 이고 '무엇을 봉인했나'는 접어도 된다.
- codex 필요: False

### [P0·wrong] resolved-conflict-shown-as-open
- **어디**: `webapp/templates/cascade.html:205-215`
- **근거**: 타일 바로 아래 빨간 callout 제목이 `⚠ verified 서브셋에 미해소 값 충돌이 있다` 이고 꼬리말이 `그래서 이 서브셋의 verdict 는 전부 잠정이다 — 순위를 확정으로 읽지 말 것.` 인데, 그 안에 실린 본문 첫 글자가 `[해소됨 2026-08-12 — _CONFLICT_RESOLVED_2026_08_12 참조]` 다. 정본 db/properties/citation_hazards.json 도 이 건을 `"level": "RESOLVED", "resolved": "2026-08-12"` 로 등재하고 `'최연질 = Sc2O3 18.7' 는 실제 42.082 … → 재정렬 완료` 라고 적는다. 그리고 db/properties/doping_cascade_verified.json 전체에서 '잠정' 은 **1회**(그 충돌 문자열 자체) 뿐이라 '전부 잠정' 이라는 꼬리말은 파일에 근거가 없다. 루프 조건이 `k.startswith('_CONFLICT')` 라(211행) RESOLVED 키까지 '미해소' 제목 아래로 끌어온 것이 원인이다.
- **고치는 법**: 루프를 `k.startswith('_CONFLICT_UNRESOLVED')` 로 좁히고, UNRESOLVED 가 0건이면 callout 자체를 렌더하지 않는다. 해소분은 별도의 회색 `<details>`(«해소된 충돌 1건 — 2026-08-12») 로 접는다. 꼬리말 '전부 잠정' 은 파일 근거가 없으므로 삭제한다.
- codex 필요: False

### [P0·broken] python-dict-repr-leak
- **어디**: `webapp/templates/cascade.html:212 (`{% for c in _conf %}<li>{{ c|bold }}</li>{% endfor %}`)`
- **근거**: `_CONFLICT_RESOLVED_2026_08_12` 은 str 이 아니라 dict 라(webapp/data.py load_cascade 실측: `TYPE: dict`) `|bold` 가 파이썬 repr 을 그대로 이스케이프해 화면에 찍는다. 렌더 HTML 원문: `<li>{&#39;resolution&#39;: &#39;doping_cascade_trivalent_M3.json 이 <b>전부 맞았다</b>. 이 파일이 틀렸다.&#39;, &#39;evidence&#39;: &#39;gabia:/data/work/runs/… &#39;, &#39;checked&#39;: {&#39;Sc2O3_x002&#39;: {&#39;E_young_GPa&#39;: 42.082, …}}, &#39;consequence&#39;: &#34;…&#34;, &#39;note&#39;: …}</li>` — 중괄호·작은따옴표·`&#39;` 가 페이지 최상단 빨간 상자 안에 노출된다. 커밋 fc3624184(«webapp: 카드·메모의 마크다운이 화면에 기호로 노출되던 것 정정»)가 같은 계열 버그를 대시보드에서만 고쳤고 cascade 는 안 훑었다.
- **고치는 법**: 위 항목과 같은 수정으로 사라진다(RESOLVED 키를 제외). 재발 방지로 `{{ c|bold }}` 앞에 `{% if c is string %}` 가드를 두거나, data.py 쪽에서 dict 를 사람이 읽을 문장으로 접어 넘긴다. 회귀 테스트: `/cascade` 응답에 `&#39;resolution&#39;` 또는 `{&#39;` 이 없을 것.
- codex 필요: False

### [P0·broken] deeplink-typeerror-kills-theme-tab
- **어디**: `webapp/templates/cascade.html:1488-1491 (딥링크 하이라이트) → 1494-1495 (THEMES/TDOP 할당)`
- **근거**: `if(location.hash){var d=…; document.querySelectorAll('#board-tbl tbody tr').forEach(function(r){ if(r.cells[1].innerText…` 인데, 기본 화면과 `?view=diagnostic` 에서는 `#board-tbl` 의 tbody 가 **archive 게이트 안내 행 하나**(`<tr><td colspan="10" …>`)뿐이다 — 렌더 실측: casc.html·casc_diagv.html 둘 다 `<tbody> <tr><td colspan="10"`, casc_arch.html 만 `<td class="num">1</td>`. 따라서 `r.cells[1]` 이 undefined → `TypeError: Cannot read properties of undefined (reading 'innerText')` (node 로 확인). 이 문이 최상위라 같은 `<script>` 블록의 뒤쪽 1494·1495행 `var THEMES=…` / `var TDOP=…` 가 실행되지 않고 undefined 로 남는다 → 🎯 테마 탭에서 체크박스를 누르면 `TDOP.forEach` 가 다시 throw 한다. 아이러니하게 바로 위 1455행 주석이 같은 실패 모드를 이미 적어 뒀다: `아래 THEMES/TDOP/selThemes 가 미할당으로 남고 🎯 테마 탭 + #딥링크가 전부 죽는다`. 이 링크는 페이지가 스스로 48개 뿌린다(`/cascade#CoO`, `/cascade#Fe2O3`, … 787행) + 페이지 자신의 버튼 `/cascade?view=diagnostic#theme`(1088행) 도 여기에 걸린다.
- **고치는 법**: 1490행을 `if(r.cells.length>1 && r.cells[1].innerText…)` 로 가드하고, 딥링크 블록 전체를 `try{}catch(e){}` 로 감싼다. 그리고 게이트 안내 행은 `<tbody>` 밖(예: 표 위 callout)으로 빼서 데이터 행과 섞이지 않게 한다.
- codex 필요: False

### [P0·wrong] v1-47species-tables-outside-manifest
- **어디**: `webapp/templates/cascade.html:1100-1115 (champions) · 1138-1143 (litransport) · 1166-1171 (synergy) · 1036-1096 (themes)`
- **근거**: 기본 /cascade DOM 에 `cascade_v23_champions.csv` **141행 전량**이 `combined_score` 열까지 포함해 정렬·검색 가능한 표로 실린다(렌더 실측 첫 행 `Ag2O | 0.250 | -0.507 | -7.970 | 26.462 | 48.346 | 30.076 | 19.620 | 0.652 | 0.850`). 같은 파일을 API 로 받으려 하면 **403** 이고 사유가 `"error": "원장(cascade_audit_manifest.json)에 없는 cascade artifact 다 — 미등록은 미승인으로 다룬다", "approval_status": null, "use_scope": null` 이다. 즉 **같은 파일을 다운로드는 막고 화면은 전량 내보낸다.** manifest 22개 항목을 확인하면 v2(`cascade_v23_champions_v2.csv` diagnostic_only)·`cascade_v23_ranked.csv`(archive_only) 는 등재됐는데 v1 champions·litransport·themes·synergy 는 **한 줄도 없다**. app.py:344-357 의 archive 게이트는 `casc["ranked"]` 하나만 비우므로 이 넷은 정책 밖이다. 그 게이트를 만든 사유(«사이트가 "승인된 ranking 0종" 이라고 쓰면서 순위표를 같이 내보내는 자기모순»)가 champions 표에 그대로 재현돼 있다. 덤: `codoping_ml_v2.csv` 는 «절대값·순위 인용 금지» 라고 써 놓고 `/api/csv/properties/codoping_ml_v2.csv` 가 200·319 KB 로 열린다(1267행 링크).
- **고치는 법**: 두 갈래. ① `tools/cascade/build_cascade_audit_manifest.py` 로 v1 네 산출물을 `superseded / archive_only` 로 **등재**하고, ② app.py 의 archive 게이트를 `ranked` 뿐 아니라 `champions`·`litransport`·`synergy`·`themes.dopants` 까지 확장한다(themes 는 이미 diagnostic 게이트가 있다). 화면에는 표 대신 «🗄 47종 champions 141행 — 보관함 열기 →» 버튼 하나만 남긴다. 데이터는 지우지 않는다.
- codex 필요: False

### [P1·wrong] gated-rendered-as-zero
- **어디**: `webapp/templates/cascade.html:644 (`{{ stats.dopants }}종 · Pareto {{ stats.pareto }}건`) · 1082 (`전 {{ casc.themes.dopants|length }}개 도펀트`) · 1556-1557 (JS 빈 메시지)`
- **근거**: app.py:355-361 이 `casc["ranked"]["data"]=[]` · `casc["themes"]["dopants"]=[]` 로 응답에서만 비우는데, 템플릿은 그 길이를 사실처럼 찍는다. 실측 비교 — 기본: `아래 0종 리더보드 · Pareto 0건 · champion 141행은 2026-06-29 에 멈춘 취합 경계의 산물이다`, `?archive=1`: `아래 47종 리더보드 · Pareto 4건 · champion 141행…`. 테마 탭도 기본에서 `⚗️ 조합 랭킹 … 전 0개 도펀트` 로 뜬다. 그리고 테마 체크박스를 2개 누르면 `combineRows()` 가 빈 TDOP 를 돌아 1557행 문구 `선택한 축 조합에 데이터가 모두 있는 도펀트가 없다.` 를 띄운다 — 데이터는 있고 이 응답에서 빠졌을 뿐인데 화면은 '없다'고 단정한다. CLAUDE.md «없는 것을 0 으로 표시하지 않는다 — 원장 부재라고 적는다» 의 정확한 반대.
- **고치는 법**: 게이트가 걸린 자리에서는 숫자를 찍지 말고 **가려짐**을 찍는다. `casc.ranked.archive_gated` / `casc.themes.diagnostic_gated` 플래그가 이미 있으니 `{% if …gated %}🔒 보관함(archive=1){% else %}{{ stats.dopants }}종{% endif %}` 로 분기한다. JS 쪽은 `TDOP.length===0 && GATED` 일 때 '데이터 없음' 이 아니라 '이 화면에서 가려져 있다 → 진단 화면 열기' 로 문구를 바꾼다.
- codex 필요: False

### [P1·wrong] esw-grade-contradicts-itself
- **어디**: `webapp/templates/cascade.html:341-355 (축별 완성도) vs 622-637 (그래서 지금 인용할 수 있는 것)`
- **근거**: 같은 📋 현황·감사 탭 안에서 같은 축이 두 등급을 받는다. 앞 표(원장 `casc.v2.meta.status` 파생, 렌더 위치 5,452 B): `grand-potential ESW | partial | **record-complete 90 · phase-set comparable 270/270 · 효과 귀속 0/17.** … 'complete · 그대로 사용 가능' 이 아니다`. 뒤 표(템플릿 하드코딩, 렌더 위치 34,837 B): `grand-potential ESW 90종 | complete | ✅ 옛 141건과 ox_V 차이 0 — 드리프트 없음`. 뒤 표는 배지 문자열 `complete` 를 HTML 에 직접 박아 뒀다(628행). 원장은 partial 이라고 말하는데 요약표가 complete 라고 고쳐 부른다.
- **고치는 법**: 622-637 표를 하드코딩에서 원장 파생으로 바꾼다 — `casc.audit_axes` × `casc.v2.meta.status` 를 그대로 읽어 배지를 만들고, '쓸 수 있나' 열만 사람 문장으로 둔다. 그러면 두 표가 갈라질 수 없다. 회귀 테스트: 두 표의 같은 축 배지 문자열이 동일할 것.
- codex 필요: False

### [P1·broken] literal-markdown-asterisks
- **어디**: `webapp/templates/cascade.html:196 · 350 · 399 · 430 · 465-470 · 1131 · 1156 · 1317`
- **근거**: 렌더 HTML(스크립트 제외)에 리터럴 `**` 가 **48회** 남아 화면에 기호로 보인다. 가장 눈에 띄는 자리 — 타일 아래 빨간 배너: `승인 0 은 '실패' 가 아니라 **현재 상태의 정확한 이름**이다`(196행 `{{ T.why_zero }}`). 축별 완성도 표: `**record-complete 90 · phase-set comparable 270/270 · 효과 귀속 0/17.**`(350행 `{{ txt }}`). 20-stage 카드: `10: **NOT RUN · 0/270** (TOP_K_SIGMA=0…)`, `09f: **NOT A TRUE GRAND-POTENTIAL ESW**`(470행 `{{ w }}`). G4 입력 카드: `**어닐 기하 위에서 계산한 정적 프록시 두 개**`, `⛔ **정본 BVSE 와 다른 파라미터다.**`(1131행). ESW 각주: `**경쟁상의 mp-ID·MP 스냅샷 버전이 기록돼 있지 않다**`(1156행). 같은 파일 안에서 다른 자리는 `|bold` 를 쓴다(예: 133·565·604행) — 필터를 빠뜨린 곳만 새는 것이다. 커밋 fc3624184 가 같은 증상을 카드·메모에서만 고쳤다.
- **고치는 법**: 위 8곳에 `|bold` 를 붙인다. 그리고 회귀 테스트를 하나 추가한다 — 렌더된 `/cascade` 본문(스크립트 제외)에 `**` 가 0회일 것. 이 검사를 전 라우트로 넓히면 같은 계열 재발이 끊긴다.
- codex 필요: False

### [P1·stale] esw-missing-for-43-is-stale
- **어디**: `webapp/templates/cascade.html:70-75`
- **근거**: 처음 보는 사람용 카드가 이렇게 쓴다: `47 순위표에 오른 것 — 산화물 37 + 불화물 10. 나머지 43종은 **전기화학 창(ESW)이 아직 없어서** 빠졌다 — 성적이 나빠서가 아니다.` 그리고 `⇒ 47 vs 90 을 가른 축은 ESW 하나다.` 그런데 같은 페이지 탭 배지가 `🧪 Oxidation ESW  90종` 이고, ESW 탭 본문이 `✅ 90종 전수 (oxidation_stability_cascade_v2.csv · 90행). 옛 141건과 ox_V 차이 0 — 드리프트 없음` 이다(실측: `casc.v2.oxidation` 90행). 즉 '아직 없어서' 는 2026-06-29 취합 경계 시점의 사실이고 지금은 아니다. 처음 온 사람이 첫 화면에서 배우는 인과가 화면 다른 곳에서 반증된다.
- **고치는 법**: `아직 없어서 빠졌다` → `그 시점(2026-06-29)에 ESW 가 47종분만 취합돼 있어서 빠졌다 — 지금은 90종 전수가 있다(🧪 탭)` 로 시제를 박고 탭 앵커를 건다. 4개 타일 자체는 좋으니 유지.
- codex 필요: False

### [P1·stale] lineage-md-protocol-contradicts-ratified-card
- **어디**: `webapp/data.py:2007-2014 (METHOD_LINEAGE 'MD 통계 규율' 체인) → 화면 webapp/templates/cascade.html:128-170`
- **근거**: 📜 방법 계보 카드의 세 번째 체인 끝단이 `우리 MLIP-MD 규율 — MSD 창 2–50 ps 고정 · **600/800/1000 K 아레니우스** · 멀티시드 판정 · σ 절대값 인용 금지` 다. 그런데 2026-09-08 비준 카드 §1 이 cascade 보고량을 `D_rel(design, host) ≡ D*(design)/D*(host), **600 K** · 2–50 ps 창 · cell-conditioned` 로 한정하고 §1 ⛔삭제한_것 에 `2온도 외삽` 을 명시 삭제했다. 봉인 파일도 `phase_melting` 규칙에서 `비준 카드가 보고량을 600 K 단일 온도로 한정했다 … 다온도 규칙(D-2026-09-04-…)은 **이 캠페인에 해당 없음**` 이라고 못박는다. 게다가 같은 화면이 `10 σ MD ⛔ 껐다 (비용) — TOP_K_SIGMA=0`, `이온전도도 순위 — MD σ 는 비용 때문에 **안 돌렸다**(설계 결정)` 라고 쓰므로, cascade 는 아직 MD 를 한 번도 안 돌린 채 'MD 규율 계보' 를 자기 것으로 표시하고 있고 그 규율 내용마저 비준 카드와 어긋난다. 같은 체인 첫 번째 끝단도 `우리 cascade v23 (G1–G5) — **47종** 큐레이션 로스터` 로 superseded 숫자다.
- **고치는 법**: MD 체인 끝단을 두 줄로 쪼갠다: (a) repo 공통 MLIP-MD 규율(600/800/1000 K) — 다른 캠페인 것, (b) **이 캠페인의 보고량**: D_rel · 600 K 단일 · 2–50 ps · cell-conditioned(2026-09-08 비준, 아직 미실행). 첫 체인 끝단 '47종' 은 '90종 완주(47종은 2026-06-29 스냅샷)' 로 고친다. 값은 estimand JSON 에서 읽는다.
- codex 필요: False

### [P1·buried] citable-table-buried-at-bottom
- **어디**: `webapp/templates/cascade.html:622-637 (기본 탭 마지막 카드)`
- **근거**: 기본 탭(tab-audit) 패널 35,826 바이트 중 카드 15장의 h3 위치를 실측하면: 86 «⚠ 이 축의 근본 한계(심화)» → 2,584 «🔍 우리가 안 한 세 단계(심화)» → 5,452 «축별 완성도(심화)» → … → 32,308 «90종 랭킹이 왜 확정이 아닌가» → 34,089 «⛔ G4 는 …» → **34,837 «그래서 지금 인용할 수 있는 것 / 없는 것»**. 사용자가 가장 먼저 원하는 표(원자료 ✅ / ESW ✅ / 47종 ⛔ / 89종 ⛔ / DFT 2건 ✅)가 맨 끝이고, 그 앞에 두 장의 «심화» 논증이 서 있다. 5장짜리 감사 그림(«기본 공개가 허용된 유일한 그림») 도 12번째 카드(29,313 B)다.
- **고치는 법**: 기본 탭 순서를 뒤집는다 — ① «지금 인용할 수 있는 것 / 없는 것» ② 캠페인 지위 밴드(위 al-nogo 항목) ③ 감사 그림 5장 ④ 축별 완성도, 그다음에 «심화» 두 논증과 G3/2×2/20-stage/게이트 분모를 `<details>` 로 접는다. «심화» 배지가 이미 있으니 배지=접힘 규칙으로 통일하면 기계적으로 정리된다.
- codex 필요: False

### [P1·duplicate] duplicate-audit-tables
- **어디**: `webapp/templates/cascade.html:341-355 ↔ 1310-1319 (축별 완성도) · 537-557 ↔ 1295-1308 (완결성/ingestion 감사)`
- **근거**: «축별 완성도» 표가 audit 탭(렌더 오프셋 29,909)과 v2 탭(283,058) 두 곳에 **같은 원장·같은 문장**으로 실린다 — 둘 다 `raw | complete | 90종 원자료 …`, `oxidation | partial | **record-complete 90 · phase-set comparable 270/270 …**`. 완결성 감사도 두 벌인데, audit 탭 쪽은 부제에 스스로 `2026-08-14 · **위 게이트별 표가 더 정확하다**` 라고 적어 놓고도 그대로 남아 있다(539행). 열등하다고 자백한 표를 지우지 않은 것이다.
- **고치는 법**: 축별 완성도는 audit 탭 한 곳만 남기고 v2 탭에서는 앵커 링크로 대체한다. «gate 입력 ingestion 감사»(537-557)는 스스로 열등하다고 적었으므로 삭제하거나 «게이트 분모 계약» 카드 안 `<details>` 로 흡수한다.
- codex 필요: False

### [P1·broken] funnel-chips-point-at-gated-board
- **어디**: `webapp/templates/cascade.html:787`
- **근거**: 깔때기 탭의 «여기서 탈락 N종 — 펼치기» 안에서 `<a class="fn-chip" href="/cascade#{{ d }}" title="리더보드에서 보기">{{ d }}</a>` 로 도펀트 칩을 만든다. 렌더 실측으로 `/cascade#CoO` `/cascade#Fe2O3` `/cascade#MnO` … 총 **48개**. 그런데 도착지 리더보드는 `?archive=1` 없이는 비어 있고(위 v1-47species 항목 참조), 하이라이트 JS 는 도착 즉시 TypeError 로 죽는다(위 deeplink 항목). 즉 title 이 약속한 '리더보드에서 보기' 가 세 겹으로 안 된다: 표가 비었고 · JS 가 죽고 · 그 리더보드는 superseded 라 봐도 안 된다.
- **고치는 법**: href 를 `/cascade?archive=1#{{ d }}` 로 바꾸거나(보관함을 명시적으로 여는 링크), 리더보드가 superseded 인 이상 링크를 빼고 평범한 칩으로 둔다. 후자가 정직하다 — title 도 '리더보드에서 보기' 대신 '이 게이트에서 탈락' 으로.
- codex 필요: False

### [P2·ia] two-number-systems-side-by-side
- **어디**: `webapp/templates/cascade.html:62-75 (4개 타일) vs 187-194 (6개 타일)`
- **근거**: «숫자 네 개가 각각 무엇인가» 카드가 `3,615 계산한 구조 / 681 하류까지 간 구조 / 90 완주한 화합물 / 47 순위표에 오른 것` 을 가르친다. 그 아래 stat-tiles 는 `273 계획 슬롯 / 270 완주 슬롯 / 90 완주 종 / 47 역사 스냅샷 / 0 승인된 ranking / 0 explicit pair 라벨` 이다. 겹치는 건 90·47 뿐이고 273·270 은 앞 카드가 설명하지 않으며, 3,615·681 은 아래 타일에 없다. 처음 온 사람은 '구조 3,615개' 와 '슬롯 273개' 의 관계를 어디서도 배울 수 없다.
- **고치는 법**: 한 카드로 합친다 — `91종 × 3 라벨 = 273 계획 슬롯 → 270 완주 → 90 완주 종` 이 세로줄이고, `3,615 구조 / 681 하류` 는 그 안쪽 괄호(한 종이 여러 자리·시드를 갖는다는 앞 문장과 붙여서)로 내린다. 6타일은 그대로 두되 273/270 툴팁을 카드 문장과 같은 어휘로 맞춘다.
- codex 필요: False

### [P2·missing] first-card-numbers-hardcoded-no-source
- **어디**: `webapp/templates/cascade.html:63-72`
- **근거**: `3,615` `681` `90` `47` 과 그 분해(`산화물 37 · 염화물 19 · 불화물 10 · 황화물 10 · 브롬 5 · 질화 5 · 요오드 4`)가 전부 HTML 리터럴이고 출처 줄이 없다. 지금은 맞다(실측: db/properties/cascade_v23_all.csv 3,615행 · li_mobility_score 채워진 행 681 · concentration 전부 0.25). 문제는 아래 6타일이 `T.ok` manifest 해시 검증 + fail-closed 로 보호되는데(175-185행) 이 4개는 그 밖이라, CSV 가 바뀌어도 화면이 조용히 옛 숫자를 유지한다는 점이다. 카드 스스로 «3,615행 전부 0.25 — 차원 하나가 상수» 라고 다른 곳(303행)에서 인용하는 숫자이기도 하다.
- **고치는 법**: 3,615·681 을 data.py 에서 CSV 로부터 계산해 넘기고 카드 하단에 `출처: db/properties/cascade_v23_all.csv` 한 줄을 붙인다. 계보 분해(37/19/10/…)도 ESW v2 에서 세면 자동 유지된다.
- codex 필요: False

### [P2·useless] mo-db-117kb-inline-every-load
- **어디**: `webapp/templates/cascade.html:1407 (`<script>window.MO_DB={{ mo_db|tojson }};</script>`)`
- **근거**: 기본 /cascade 응답 557,619 바이트 중 인라인 스크립트가 149,667 바이트이고 그중 **117,806 바이트가 MO_DB** 하나다(실측). 분자오비탈 모달은 사용자가 도펀트 칩을 클릭해야 열리는 부가 기능인데, 전 항목이 매 요청마다 통째로 실린다. 페이지 전체의 21%다.
- **고치는 법**: MO_DB 를 `/api/mo/<dopant>` 로 지연 로드하거나(모달 열 때 fetch), 최소한 이 페이지가 실제로 참조하는 도펀트 키로 서브셋을 만들어 넘긴다. 다른 라우트(elements·compare)도 같은 blob 을 싣는지 함께 본다.
- codex 필요: False

### [P2·missing] no-link-to-governance-ledger-kb
- **어디**: `webapp/templates/cascade.html (본문 링크 전수) · 대상 /governance · /ledger`
- **근거**: 본문 영역 링크를 전부 뽑으면 /benchmarks · /fairchem · /literature(digest 8건) · /composition/<id>(archive 게이트 안쪽뿐) · /cascade 계열 · /api/file 뿐이다. **/governance 0건 · /ledger 0건**. 그런데 /governance 는 `D-2026-09-08-cascade-d-rel-estimand` 를 «보고량 ✅ 유효 🔒 결과 보기 전 prospective» 로 이미 싣고 있다(실측). 판정 원장이 있는데 판정 대상 화면이 그리로 가는 문이 없다. kb 문서 경로(kb/methodology/cascade_lessons_transfer_2026_09_08.md 등)도 `<code>` 텍스트로만 있고 링크가 아니다.
- **고치는 법**: 캠페인 지위 밴드(al-nogo 항목)에 `⚖ 판정 원장에서 보기 → /governance#D-2026-09-08-cascade-d-rel-estimand` 를 넣는다. 본문의 `<code>kb/...</code>` 는 /doc 라우트가 있으면 링크로 승격한다.
- codex 필요: False

### [P2·buried] only-trustworthy-values-have-no-link
- **어디**: `webapp/templates/cascade.html:634-635`
- **근거**: «그래서 지금 인용할 수 있는 것» 표 마지막 행이 `DFT 심층검증 | 2건 | ✅ Nd2O3 · B2O3 — 조성 페이지의 DFT 값만이 실제 신뢰선` 인데, 도펀트 이름이 `{{ deep_map.keys()|join(' · ') }}` 로 **평문**이다. `deep_map` 이 `{'modelc_nd_doped':'Nd2O3','b2o3':'B2O3'}` 라 /composition/modelc_nd_doped · /composition/b2o3 링크를 만들 재료가 이미 손에 있다. 페이지가 유일하게 '믿어도 된다' 고 지목한 두 값으로 가는 길만 막혀 있다(archive 게이트 안쪽 682행에서는 같은 deep_map 으로 링크를 만든다).
- **고치는 법**: 682행과 같은 방식으로 `<a href="/composition/{{ k }}">` 를 건다. 한 줄 수정.
- codex 필요: False

### [P2·ia] nav-places-audit-screen-under-run
- **어디**: `webapp/templates/base.html:60 (`계산 돌리기` 그룹 안 `🤖 Screening·ML`)`
- **근거**: 사이드바 그룹이 `결과 보기`(explorer·compare·elements) / `계산 돌리기`(compute · **cascade** · methods) / `문헌·검증` / `자료·기록` 인데, /cascade 는 라우트 docstring 부터 `감사 화면` 이고 캠페인은 NO-GO 로 멈춰 있어 여기서 돌릴 수 있는 것이 없다. 라벨 `Screening·ML` 만으로는 그게 cascade 인지도, 멈춰 있는지도 알 수 없다.
- **고치는 법**: 두 갈래 중 택일 — (a) `문헌·검증` 이나 새 `감사` 그룹으로 옮긴다, (b) 그대로 두되 nav 라벨에 상태 점(멈춤/진행)을 붙인다. v3 재편에서 다른 라우트의 상태 표시와 같은 규칙으로 정하는 게 낫다.
- codex 필요: False

### [P1·ia] default-visible-scope-vs-round3-contract
- **어디**: `webapp/templates/cascade.html:187-228 (타일~탭 사이, 신설 예정 자리) · 계약 docs/reviews/cascade_dftweb_source_of_truth_2026_08_14.md`
- **근거**: 위 al-nogo 항목의 수정은 «보고량 D_rel(600 K · 2–50 ps · cell-conditioned)» · «남은 해제조건 #3·#4·#7·#8» · «봉인 v2_2026_09_08» 을 **기본 화면(default_visible)** 에 새로 올리자는 것이다. 그런데 cascade 화면의 노출 범위는 Round-3 공개 경계 계약이 항목별로 열거해 정하고(manifest 의 `use_scope` 어휘 `default_visible / diagnostic_only / archive_only`, 실측 22항목), 비준 카드에는 §4 허용 서술·§5 금지 서술·§6 구조적 공백(«cascade 는 MLIP 로 만든 순위를 MLIP 로 검증한다») 처럼 계약이 다룬 적 없는 새 종류의 문장이 들어 있다. 특히 §6 은 카드 스스로 `신설 해제조건으로 올릴지는 1저자·리뷰 판단` 이라고 유보한 건이라, 기본 화면에 얼마나·어떤 어휘로 실을지를 우리가 정하면 계약을 우회하는 셈이 된다.
- **고치는 법**: '무엇을 올릴지' 가 아니라 '어느 use_scope 로 올릴지' 를 리뷰에 묻는다 — 후보안: 지위·보고량 정의·남은 해제조건 4건 = default_visible / §5 금지 서술 전문 = default_visible / §6 구조적 공백 = default_visible 이되 '신설 해제조건 제안(미채택)' 이라는 지위 라벨을 달아 접음 / §2 대표 행 선택 절차·§3 판정 규칙 = diagnostic_only. 이 배치가 Round-3 경계와 어긋나지 않는지 확인받고, 확정되면 manifest 에 estimand·seal JSON 을 등재해 화면이 원장 파생이 되게 한다.
- codex 필요: True
