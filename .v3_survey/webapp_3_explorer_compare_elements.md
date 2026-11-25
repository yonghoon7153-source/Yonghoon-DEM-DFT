# webapp — 값 탐색 3종 (/explorer · /compare · /elements)

## 지금 무엇인가
세 화면 다 db/properties/canonical_registry.json 이라는 한 원장을 표로 그린다 — /explorer 는 14조성 × 24열 전체 행렬(+ provenance 범례 + 방법검증 앵커), /compare 는 그중 고른 조성만 나란히 + 막대/레이더 + 손으로 쓴 해설 카드 4장, /elements 는 주기율표에서 원소를 눌러 조성·ICOHP·논문으로 되짚는 색인이다. 값의 상태 배지(잠정·철회·출처⚠)와 비교묶음 강제는 explorer/compare 둘 다 레지스트리에서 자동으로 끌어오고, 손 목록을 안 쓴다. /elements 만 본문이 /api/element JSON 으로 브라우저에서 그려져서, 서버 HTML 을 훑는 결속·hazard 검사가 이 화면을 아예 못 본다.

## 처음 오는 사람
처음 오면 사이드바 '결과 보기' 에 Property Explorer · Comparison · Periodic Table 셋이 나란히 있고, 어느 게 정본 진입점인지 알려주는 게 없다. 셋 중 둘(explorer·compare)이 같은 레지스트리를 표로 그려서 "왜 두 개지?" 가 첫 질문이 된다.

/explorer 를 열면 가로로 27칸짜리 표가 나오고 화면에 TODO 가 272개 찍힌다(24개 값 열 × 14행 중 채워진 건 45칸, 나머지가 TODO/'—'). 그 중 MD_sigma_ratio_600K/800K/1000K 3열은 14행 전부 TODO 고, SDCP_Eads_eV__sdcp_neutral_cross_Ni_at_Li 같은 원시 키 11열은 sdcp 한 행에만 값이 있다. 헤더는 라벨 없이 키 그대로고 ⓘ 툴팁은 비어 있으며, 맨 아래 provenance 카드 22장 중 14장이 그냥 '—' 다. 그리고 표 안에는 '잠정' 배지 14개 · '철회' 1개 · '출처⚠' 2개가 떠 있는데 그게 무슨 뜻인지 알려주는 범례가 화면에 없다(툴팁뿐). TODO 와 '—' 가 서로 다른 뜻이라는 설명도 Jinja 주석에만 있다. 반대로 정말 먼저 봐야 할 "우리 계산기가 얼마나 맞나"(UMA 힘 30.0 meV/Å 등 4건)는 그 표와 22장 카드를 다 지나야 나온다.

/compare 는 더 나쁘다. 첫 화면에서 기본 물성이 E_VRH_GPa 인데 그 축의 비교묶음은 comp1·comp2 뿐이라 4개를 골라도 막대가 2개만 그려지고, 레이더는 공통축이 2개(B₀·ICOHP)라 3축 미달로 "그릴 수 없어요" 안내문만 뜬다. 즉 대표 페이지의 두 그림이 첫 로드에서 둘 다 반쪽이다(강제 로직 자체는 옳다 — 기본값 선택이 틀렸다). 표는 19행인데 그중 11행이 SDCP_* 라 기본 선택에서 전부 TODO 다. 그 아래로는 2026-07-29~08-05 사이에 손으로 쓴 해설 카드 4장이 접힘 없이 펼쳐져 있고, 최신(09-07~08 LPSOCl 마감 비준)은 어디에도 없다.

/elements 가 셋 중 제일 친절하다. 주기율표를 누르면 브리핑이 뜨고 "Nd + Cl 을 같이 눌러 보라" 는 예시가 실제로 동작한다(modelc_nd_doped + Nd–Cl ICOHP −0.571). 다만 초록 12칸(캠페인) 말고 33칸이 '도핑 스크리닝 도펀트' 로 강조돼 있는데, 눌러 보면 그 안에 "⛔ superseded 스냅샷 — 현재 승인된 랭킹은 0종" 이라고 적혀 있다. 처음 보는 사람 눈엔 주기율표의 3분의 1이 '살아있는 결과' 처럼 보이는데 실은 폐기된 스냅샷이고, 거기서 /cascade 로 가는 화살표는 빈 표에 떨어진다.

없는 것 — 세 화면 어디에도 (a) 이 앱이 무엇인지 한 줄, (b) 배지 범례, (c) "여기부터 보세요" 안내, (d) 값 상태(정본/잠정/철회/비인용) 4단계가 뭔지의 설명이 없다. 지식 허브가 되려면 이 넷이 첫 화면 위쪽에 있어야 한다.

## 건드리면 안 되는 것
- compare.html:60-77 의 domGroup/splitByGroup 비교묶음 강제와 125-151 의 cmp-caveat 문구 생성. 첫 로드에서 막대가 2개뿐이고 레이더가 안 그려지는 건 **이 장치가 제대로 일하고 있다는 증거**다. 차트를 채우려고 이 강제를 느슨하게 하면 단일시드 MD Ea 와 4-seed 값, legacy DOS-문턱 갭과 fixed-occ 갭이 다시 한 폴리곤에 올라간다(2026-08-07 리뷰 P1 재발). 고칠 것은 기본 선택이지 강제가 아니다.
- data.py:782-789 metric_meta() 의 레지스트리 자동 생성과 explorer.html:4-6 의 경고 주석(`metric 목록을 여기 하드코딩하면 레지스트리에 metric 이 늘어도 화면이 안 따라온다 — 2026-08-07 Codex 5라운드`). 열이 22개로 지저분하다고 손 목록으로 되돌리면 ordered/disorder 두 metric 이 통째로 사라졌던 사고가 재현된다. 정리는 family 필터·열 그룹으로 한다.
- explorer.html:70 의 파생 결속 `data-claim="{{ key }}@{{ cid }}"`. 손 목록 없이 모든 셀이 자기 (metric, system) 이름을 댄다 — 이 구조가 BG ② 이주의 핵심이고 래칫을 은퇴시킨 근거다. 셀 단위 결속을 걷어내고 '문제 있는 것만' 붙이는 방식으로 되돌리지 말 것.
- 상태 배지를 **하나만** 붙이는 규칙 — explorer.html:74-79 와 compare.html:95-100 의 `레지스트리 status 우선, 없을 때만 CANONICAL_PROVISIONAL` 분기. 2026-08-07 Codex 4라운드에서 '잠정' 이 두 번 찍혔던 자리다. 배지 범례를 새로 만들 때도 이 우선순위를 그대로 따를 것.
- explorer.html:157-168 의 '방법 검증 앵커는 조성 물성 표와 다른 그룹' 분리와 그 문구(`위 표는 이 물질의 값이 얼마냐이고, 여기는 우리 계산기가 얼마나 맞나다`). 위로 올리는 건 좋지만 표에 합치면 'UMA 힘 오차' 가 comp1 의 물성처럼 읽힌다.
- explorer 의 TODO(미계산)와 '—'(그 계에 그 분석을 안 했거나 정의가 다름)를 **다른 기호로 두는 규칙** 자체(explorer.html:9-10 주석). 통일하지 말고 설명을 화면에 올려라. 다만 '비인용' 은 세 번째 상태이므로 TODO 로 뭉뚱그리지 말 것(위 P1 항목).
- app.py:344-399 의 /cascade archive·diagnostic 게이트와 그 docstring. 47종 랭킹이 기본 DOM 에 안 실리는 것은 유지한다 — 고칠 대상은 이 게이트를 우회하는 /api/element 쪽이지 게이트 완화가 아니다.
- compare.html:117-124 의 `_noPlotly` 오프라인 가드와 컨테이너 id 'cmpchart'/'cmpradar'. 두 번 고쳐서 지금 맞다(가드가 'chart' 를 찾던 2026-08-07 P3 · cascade 에만 있던 가드).
- compare.html:202-225 BVSE 카드의 `⛔ 정량·순위는 원본 주기셀 값만` 경고와 큐빅 대조표, `onset 차이는 격자 칸 수로 판정한다(1칸 = ±0.05 val²)` 규칙. CLAUDE.md BVSE 규율의 화면 구현이고 onset 배지는 실제 db 값(0.40/0.35/1.40)과 일치함을 확인했다.
- elements 의 다중선택 조합 브리핑(`?sel=Nd,Cl` → 공통 조성 modelc_nd_doped + Nd–Cl ICOHP −0.571 + 논문 합집합 23편)과 118종 전량 원소 kb. 이 앱에서 제일 잘 도는 기능이고 힌트 문구의 예시가 실제로 동작한다 — 재편해도 이 상호작용은 그대로 두라.
- tests/test_webapp.py:2897 test_retracted_claims_are_id_bound_on_every_surface · test_legacy_ratchet_is_retired_not_reintroduced · test_each_surface_zero_comes_from_declarations_not_from_absence 3종. 확장(/elements 추가, forbidden_phrases 보강)은 하되 예외표(_LEGACY_UNBOUND)를 다시 채워 통과시키는 방식은 금지 — 그 시험이 그걸 막고 있다.
- canonical.py 의 gate_outcome/gate_prefix 를 **서버가 만들어 내려보내는** 구조(app.py:325-336). compare.html:54-56 주석대로 템플릿 JS 에서 게이트 문구를 다시 조립하면 미평가(not_assessed)를 실패로 오역한다.

## 발견

### [P0·wrong] explorer-cite-copies-retracted
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:70-73, 126-128`
- **근거**: 셀 클릭 인용 복사가 화면 배지와 다른 것을 복사한다. 템플릿: `data-method="{{ canonical_meta.get(key,'') }}{% if prov %} · ⚠ {{ prov }}{% endif %}"` · `onclick="citeVal('{{ c.label }}','{{ label }}','{{ v }}','{{ unit }}',this.dataset.method)"` · JS `function citeVal(comp,prop,val,unit,method){copyText(comp+' — '+prop+' = '+val+' '+unit+'  ['+method+']');}`. 여기서 `prov` 는 옛 CANONICAL_PROVISIONAL 이고 레지스트리 status 가 아니다. 실측: CANONICAL_ENTRY[('MD_Ea_eV','b2o3')] = {"value":0.199, "status":"retracted", "source_key":"/FINAL_for_paper/Ea_eV_PAPER_RETRACTED_2026_08_23"} 인데 CANONICAL_PROVISIONAL[('MD_Ea_eV','b2o3')] 은 None → ⚠ 분기를 안 탄다. 화면 배지는 '철회'(canonical_status_all 이 별도로 만든다)인데, 복사된 문자열에는 '철회' 도 'retracted' 도 없다. lpsocl 0.287(잠정·게이트 탈락)도 같다.
- **고치는 법**: data-method 를 서버에서 만들 때 canonical_status_all()/canonical_provenance_flags() 를 합쳐 넣는다. status 가 retracted/superseded 면 복사 문자열 맨 앞에 `⛔ 철회값 — 인용 금지 · ` 를 강제로 붙이거나(권장) 복사 자체를 막고 사유 툴팁만 띄운다. 회귀시험: 철회 셀의 클립보드 문자열에 '철회' 가 없으면 실패하는 음성 시험 1건.
- codex 필요: False

### [P0·wrong] compare-beta-hardgate-as-verdict
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:472, 491, 505-509, 531, 542-549`
- **근거**: 카드가 폐기된 β≥0.80 하드게이트를 **판정**으로 쓴다. 화면 문자열: `<h3>Li MSD 200 ps ... · β 게이트</h3>` · `<b>3계 전 곡선 멀티시드 평균 (v2) — 유일한 탈락은 LPSOCl 600 K</b> (β 0.61 &lt; 0.8 — MSD 97 Å²로 크기는 충분` · `R² 0.975여도 β가 낮으면 확산이 아니다 — 그 D는 인용 금지.` · 표 셀 `<b style="color:#b91c1c">0.61 ⛔</b>`. 원장 db/properties/citation_hazards.json 의 HZ-beta-hard-gate: {"level":"SUPERSEDED", "what":"β ≥ 0.80 하드게이트 — **판정으로 인용 금지**. β 는 경보로만", "why":"...우리 운영점에서 고정문턱 0.8 은 거짓탈락률 50 %", "fix":"판정축은 D_inc plateau · 창 안정성 · 홉 수"}. 자동 스캐너가 못 잡는 이유도 확인했다 — forbidden_phrases 가 ["β ≥ 0.80","베타 하드게이트","β 하드게이트"] 리터럴뿐인데 화면은 `β 0.61 < 0.8` 로 쓴다. 실측 scan_claim_bindings('/compare') = bound 4 · unbound 0 (통과).
- **고치는 법**: 카드 판정축을 D_inc 4창 plateau · 창 안정성 · 홉 수로 바꿔 쓰고, β 표는 '경보(진단)' 로 강등해 접는다. 해당 블록에 data-claim="HZ-beta-hard-gate" 결속을 붙인다. citation_hazards 의 forbidden_phrases 에 `< 0.8`·`β 게이트`·`0.80 하드` 변형을 추가해 같은 누출이 다시 통과하지 못하게 한다.
- codex 필요: False

### [P0·broken] api-element-bypasses-cascade-archive-gate
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/data.py:3908-3925 · /home/user/Yonghoon-DEM-DFT/webapp/app.py:447-451 (대조: app.py:344-362)`
- **근거**: /cascade 는 47종 랭킹을 정책으로 막는다: docstring `⛔ 2026-08-16 (Codex f9 webapp P0-5) — ... 사이트가 "승인된 ranking 0종" 이라고 쓰면서 순위표를 같이 내보내는 자기모순이다.` 구현 `if not archive: casc["ranked"] = {**(casc.get("ranked") or {}), "data": [], "archive_gated": True}`. 그런데 _cascade_by_element_c 는 `rows = load_cascade().get("ranked", {}).get("data", [])` 로 **게이트 앞 원본**을 읽고, /api/element 는 게이트가 없다. 실측 `GET /api/element?syms=Ti` → "cascade": [{"E_GPa":46.2,"dopant":"TiF4","group":"TM","ox_V":2.024,"pugh":0.96,"rank":39.0,"score":0.358},{"dopant":"TiO2","rank":41.0,"score":0.351,...}]. /elements 주기율표에는 이 경로로 33칸이 'pt-casc' 로 강조돼 있다(렌더 실측: pt-on 12 · pt-casc 33 · pt-off 73).
- **고치는 법**: cascade_for_element 에 /cascade 와 같은 archive 게이트를 건다 — 기본 응답은 도펀트 이름·존재 여부까지만, rank/score/ox_V/E_GPa/pugh 는 ?archive=1 에서만. 주기율표 범례도 '도핑 스크리닝 도펀트' → 'historical 스크리닝(superseded)' 로 바꿔 클릭 전에 지위를 알린다. 회귀시험은 /api/element 응답에 rank 키가 게이트 없이 나오면 실패하도록.
- codex 필요: False

### [P1·wrong] explorer-noncitable-sigma-columns-render-as-TODO
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:7-8, 85 · /home/user/Yonghoon-DEM-DFT/webapp/data.py:782-789`
- **근거**: MD_sigma_ratio_600K/800K/1000K 3열이 14행 전부 `<span class="cell-todo">TODO</span>` 다 (canonical_table 채움 0/14, 실측). 그런데 값이 없는 게 아니라 **비인용**이다 — canonical_registry.json: {"metric":"MD_sigma_ratio_600K","status":"source_pending","citable":false,"comparison_group":"md-sigma-ratio-v1__NON_CITABLE","why_non_citable":"Codex BH P0-1 (2026-09-07). 원자료 CSV 가 등가·보존·순위·기전 주장을 **명시적으로 금지**한다. ... ① framework gate NOT ASSESSED ② 고온 원궤적 미보존 ③ lineage UNWIRED"}. 배지는 v가 None 이라 렌더 분기를 못 타서 안 붙는다. 헤더도 라벨 없이 `MD_sigma_ratio_1000K ⓘ` 고 단위는 빈칸, provenance 카드는 '—'.
- **고치는 법**: citable:false 인 metric 은 본 표에서 빼고 표 아래 '비인용 축(사유 포함)' 접힘 절로 옮긴다. 남길 거면 셀을 TODO 대신 `비인용` 배지 + why_non_citable 툴팁으로 그린다 — TODO(=아직 안 함)와 비인용(=했지만 못 쓴다)을 같은 기호로 쓰면 안 된다.
- codex 필요: False

### [P1·useless] explorer-sdcp-11-raw-key-columns
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:7-8, 112-121`
- **근거**: 렌더된 thead 실측 27칸 중 12~22번이 `SDCP_Eads_eV__ptfe_c10_Nitop ⓘ` · `SDCP_dE_site_meV__sdcp_neutral_pm1 ⓘ` 같은 레지스트리 원시 키 11개다(라벨·단위 없음 — _METRIC_LABEL 에 없어서 metric_meta 가 키를 그대로 돌려준다). 채움은 각 1/14 (sdcp 행만). 맨 아래 provenance 카드 22장 중 14장이 `—` 다(실측). sdcp 는 molecular family 이고 나머지 13행은 고체다 — 같은 표에 둘 이유가 없다.
- **고치는 법**: family 를 표의 축으로 쓴다 — 선택된 family 에 값이 있는 metric 만 열로 그린다(molecular 를 고르면 SDCP_* 11열, argyrodite 를 고르면 gap/B₀/E_VRH/ICOHP/MD Ea). 최소 조치로는 SDCP_* 를 '분자계' 접힘 열 그룹으로 묶고 라벨을 _METRIC_LABEL 에 채운다.
- codex 필요: False

### [P1·ia] compare-default-selection-draws-nothing
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:12, 84, 179-180`
- **근거**: 기본값이 `let activeKey='E_VRH_GPa';` + `{% if cid in ['comp1','comp2','modelc','lpsocl'] %}checked{% endif %}` 다. splitByGroup 을 그대로 재현해 보니 E_VRH 의 지배 묶음 elastic-dft-relaxedion-comp1comp2-v1 은 comp1·comp2 만 남기고 modelc·lpsocl 을 뺀다 → 4개 선택인데 막대 2개. 레이더는 4조성 전부가 같은 묶음에 든 축이 B0_GPa·ICOHP_PS 2개뿐이라 `if(sel.length<2||uk.length<3)` 에 걸려 `레이더는 <b>2개 이상</b> 조성 + <b>같은 방법으로 잰</b> 공통 물성 <b>3축 이상</b>일 때만 그려요` 안내문만 뜬다. 즉 대표 화면의 그림 두 개가 첫 로드에서 둘 다 못 그린다. (강제 로직 자체는 옳다 — 기본값이 틀렸다.)
- **고치는 법**: 기본 activeKey 를 ICOHP_PS 또는 B0_GPa(둘 다 4/4 유지)로 바꾸고, 기본 선택도 그 묶음이 성립하는 조성으로 맞춘다. 그리고 물성 칩에 각 축의 '이 선택에서 몇 개가 남는지'(예: `E_VRH (2/4)`)를 미리 찍어 고르기 전에 알 수 있게 한다.
- codex 필요: False

### [P1·wrong] compare-handtyped-ea-table-mixes-protocols
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:398-427`
- **근거**: 한 열 `MD E<sub>a</sub> (eV)` 안에 성격이 다른 넷을 나란히 찍는다 — LPSCl 0.253(레지스트리상 MD_Ea_eV_singleseed, 단일 궤적) · LPSCl1.6 0.197(MD_Ea_eV) · LPSOCl1.6 0.287(MD_Ea_eV, status provisional, gate beta_600K 미통과) · B₂O₃ 0.199(MD_Ea_eV, status **retracted**). 배지는 0개, 상태 표시도 0개다. CANONICAL_META['MD_Ea_eV'] 자신이 `시드 프로토콜 혼재: comp1/modelc=단일 궤적(오차막대 없음), lpsocl=4-seed×3-T ... 조성 간 비교는 같은 프로토콜끼리만` 이라고 적고 있고, 같은 페이지 위쪽 대화형 차트는 splitByGroup 으로 정확히 이 혼합을 막는다. 파생값 `σ_BV/σ_MD @298 K` 열(9.6× / 0.30× / 12.0× / 0.04×)도 이 혼합 Ea 에서 나온다.
- **고치는 법**: 이 표를 레지스트리에서 생성하도록 바꾸고 각 셀에 status 배지 + 등록 묶음 ID 를 단다. 정적으로 남기려면 열 이름을 `MD Eₐ (프로토콜 병기)` 로 바꾸고 셀마다 '단일궤적/4시드/철회' 를 적는다. σ 비 열은 절대값 인용 금지 규율과의 관계를 명시하거나 뺀다.
- codex 필요: True

### [P1·broken] data-claim-bound-but-invisible
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:248, 422, 536 · /home/user/Yonghoon-DEM-DFT/webapp/app.py:185-190 · /home/user/Yonghoon-DEM-DFT/webapp/static/css/style.css:1341-1344`
- **근거**: compare.html:422 `<tr data-claim="MD_Ea_eV@b2o3">` 로 철회값 0.199 가 결속돼 있고 시험은 통과한다(scan_claim_bindings('/compare') bound 4 · unbound 0). 그런데 렌더된 HTML 에 `claim-flag` 는 0건이다(세 화면 다 0). app.py:185 주석은 `⚠ 자동이라서 **눈에 보여야** 정직하다: .claim-flag 가 밑줄+⛔ 를 그리고 사유를 띄운다` 인데, 실제로 .claim-flag 를 붙이는 건 canonical.annotate_claims → md_html/claimbind 경로뿐이라(canonical.py:505) 손으로 쓴 템플릿 HTML 에는 안 붙는다. 결과: 기계 원장은 초록인데 사람 눈에는 0.199·+82 meV·0.04× 가 살아있는 값으로 보인다.
- **고치는 법**: CSS 에 `[data-claim]` 셀렉터를 추가해 템플릿 결속에도 밑줄+⛔ 가 붙게 하고, title 에 사유를 서버에서 채운다(claim id → 원장 사유). 회귀시험: 결속이 있는 화면에 claim-flag/시각 표식이 0이면 실패.
- codex 필요: False

### [P1·broken] elements-surface-blind-to-claim-scan
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/elements.html:34-39, 72-82 · /home/user/Yonghoon-DEM-DFT/webapp/tests/test_webapp.py:2866-2882, 2955-2959`
- **근거**: 실측 scan_claim_bindings('/elements') = bound 0 · unbound 0. 자매 시험이 바로 그 상태를 이렇게 부른다: `"결속이 0 이다 — 이 화면은 검사에 안 걸린다(대상 문자열이 없다)"`. 그런데 그 시험의 must 목록에 /elements 가 없다: `must = ["/", "/compare", "/explorer", "/glossary", "/governance", "/log", "/methods", "/requests", "/todo", "/api/handoff/..."]`. 이유는 구조다 — 본문이 `fetch('/api/element?syms='+...)` 로 오는데 _surface_html 은 JSON 응답에서 `d.get("html")` 이 없으면 None 을 돌려 그 URL 을 통째로 건너뛴다. 즉 /elements 가 무엇을 그리든 결속·hazard 검사는 못 본다.
- **고치는 법**: ① must 목록에 /elements 를 넣되 서버가 대표 원소(예: Nd·Cl) 브리핑을 HTML 로 한 번 렌더해 초기 DOM 에 남기거나, ② _surface_html 이 /api/element?syms=<대표> 응답을 문자열로 이어붙여 스캔하도록 DYNAMIC_FIXTURES 에 추가한다. 어느 쪽이든 '검사에 안 걸리는 화면' 이 남지 않게 한다.
- codex 필요: False

### [P1·broken] dead-anchor-concept-headings
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:378, 462 (링크) · /concept/dft, /concept/md, /concept/bvse (렌더)`
- **근거**: compare.html 이 같은 죽은 앵커를 두 번 건다: `href="/concept/dft#12-활성화-에너지는-방법마다-다른-양이다--bv--neb--md-2026-08-05"`. 렌더 실측: /concept/dft 의 h2/h3 41개 중 `id=` 가 붙은 건 0개(페이지 전체 id 25개는 전부 레이아웃용 railbtn·cmdk 따위). /concept/md 21개 중 0, /concept/bvse 18개 중 0. 결과: 92 KB 페이지 최상단에 떨어지고 §12 는 손으로 찾아야 한다. `→ MD 개념 정리 §4b–4d` 링크(compare.html:551)는 아예 앵커 없이 /concept/md 로만 간다.
- **고치는 법**: md_html 렌더에 heading slug id 생성을 넣는다(python-markdown 의 toc 확장 또는 직접 slugify). 그러면 이 두 링크와 앞으로 생길 §-링크가 전부 산다. 그 뒤 compare 의 §4b 링크에도 앵커를 붙인다.
- codex 필요: False

### [P1·broken] elements-cascade-deeplink-lands-empty
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/elements.html:131 · /home/user/Yonghoon-DEM-DFT/webapp/templates/cascade.html:1489-1491`
- **근거**: 원소 브리핑의 캐스케이드 칩이 `href="/cascade#'+c.dopant+'"` 로 간다(예: /cascade#TiO2). cascade.html 의 딥링크 핸들러는 `document.querySelectorAll('#board-tbl tbody tr')` 를 훑는다. 렌더 실측: /cascade 의 #board-tbl 에는 행이 2개(사실상 비어 있음)이고 'TiO2' 문자열이 없다. /cascade?archive=1 에서만 48행이 되고 TiO2 가 나온다. 즉 화면은 rank #39 · score 0.358 을 이미 보여 주면서(위 P0 항목), 그 출처로 가는 링크는 빈 표에 떨어진다.
- **고치는 법**: P0 게이트를 고친 뒤 링크를 `/cascade?archive=1#TiO2` 로 바꾸고 라벨을 '보관함에서 보기(superseded)' 로 명시한다. 게이트 정책상 안 되면 링크를 없애고 '이 값은 보관함 전용' 만 남긴다.
- codex 필요: False

### [P1·broken] explorer-hasval-hides-analyzed-rows
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:56-57, 98-104, 132-138`
- **근거**: has.v 를 props/xprops 로만 계산하고 '보유 분석'(amatrix)은 안 본다: `{% for key,label,unit in props %}{% if canonical.get(key,{}).get(cid) is not none %}{% set has.v = true %}{% endif %}{% endfor %}`. 렌더 실측: `<tr data-fam="anode" data-hasval="0" data-s="vgcf-hbn vgcf / h-bn + li vgcf_hbn">`, `<tr data-fam="interphase" data-hasval="0" ... li3n">`. 그런데 analysis_matrix 는 vgcf_hbn={Barrier,Binding,Drag,NEB} · li3n={Barrier,Drag,NEB} 로 실제 분석을 갖고 있다. 기본이 '값 있는 조성만' 켜짐이라 두 행은 첫 화면에서 숨고, family 칩 'anode'/'interphase' 를 눌러도 필터가 AND 라 `조건에 맞는 조성이 없어요.` 만 뜬다 — 자료가 있는데 없다고 말한다.
- **고치는 법**: has.v 계산에 `amatrix.get(cid)` 를 포함한다(한 줄). 겸해서 family 칩을 누르면 hasval 필터를 자동으로 풀거나, 빈 상태 문구에 '이 family 는 canonical 값 대신 분석 파일만 있어요' 를 넣는다.
- codex 필요: False

### [P1·stale] compare-msd-card-stale-vs-lpsocl-closure
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:470-510`
- **근거**: 카드가 09-04/09-08 비준 결정을 모른다. 화면: `<h3>Li MSD 200 ps ... 3계 × 600/800/1000 K</h3>` · `<b>Ea 0.287±0.024는 이 점을 포함한 적합이라 재검토 대상</b>; 처방 = 6점 아레니우스 30런(신규 27 + lpsocl 600 재실행 3)과 기존 게이트-통과 점으로 재적합.` 원장 db/governance/decisions.json: D-2026-09-04-lpsocl-box331-400ps-uniform (status active, 1저자 비준) `"600·800·1000 K × 3시드 = 9런을 **전부 400 ps 로 재실행**하고 기존 200 ps 9런은 superseded 한다"`; D-2026-09-08-lpsocl-box331-closure-conditions (active) `"C1(궤적 무결성)·C2(4창 D_inc plateau ≤10 %)·C2b(독립 홉 ≥3.0/이온)... **HOLD 가 나오면 HOLD 를 결과로 보고하고 닫는다(추가 계산 0).**"`. 즉 화면에 적힌 '30런 처방' 과 '200 ps' 헤드라인이 둘 다 대체됐다.
- **고치는 법**: 카드를 3×3×1 · 400 ps · 9런 · C1–C6 닫힘 조건 축으로 다시 쓰고, 200 ps 3계 곡선은 '이력(superseded)' 접힘으로 내린다. 화면이 decisions.json 의 해당 결정 id 를 읽어 상태·날짜를 자동으로 찍게 하면 다음 개정 때 또 어긋나지 않는다.
- codex 필요: False

### [P2·missing] no-status-badge-legend
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:74-85, 112-123 · /home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:44-48`
- **근거**: 렌더된 /explorer 표 안 배지 실측: '잠정' 14개 · '철회' 1개 · '출처⚠' 2개. 화면 어디에도 이 배지들이 뭔지 설명하는 범례가 없다 — 툴팁(title)뿐이고 모바일/인쇄에선 사라진다. 어휘 자체는 data.py:_STATUS_BADGE 와 compare.html 의 SLAB 에 6종(미검토·출처오류·잠정·출처미배선·철회·retracted)이 정의돼 있다. 같은 표의 'TODO' 와 '—' 도 뜻이 다른데(전자는 미계산, 후자는 '그 계에 그 분석을 안 했거나 정의가 다름') 그 설명은 Jinja 주석 `{# ... 빈칸은 TODO 가 아니라 '—' #}` 안에만 있다.
- **고치는 법**: 표 바로 위에 배지 범례 한 줄(6종 + TODO/'—')을 둔다. _STATUS_BADGE 를 템플릿에 내려보내 손으로 쓰지 말고 자동 생성 — 화면마다 어휘가 갈리는 걸 막는 게 이 dict 의 원래 목적이다.
- codex 필요: False

### [P2·buried] method-anchors-buried
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:157-188`
- **근거**: '🔬 방법 검증 앵커' 4건(UMA 힘 30.0 meV/Å · Li 13.2 / 셀 비용 52원자 6921→416원자 1532 / DFT 잔여력 fmax 0.0205 / NEB 셀 추세 1.32–3.24× 하락, 전부 ⭕)이 27칸 표 + provenance 카드 22장 아래 맨 끝에 있다. 카드 자신이 `위 표는 <b>이 물질의 값이 얼마냐</b>이고, 여기는 <b>우리 계산기가 얼마나 맞나</b>다` 라고 쓴다 — 처음 온 사람이 표의 숫자를 믿을지 말지 정하는 정보인데 제일 아래다.
- **고치는 법**: 표 **위**로 올리고(4칸 타일 한 줄) 축이 다르다는 것은 지금처럼 배지와 문구로 계속 명시한다. 표에 합치지는 말 것 — 분리 자체는 옳다.
- codex 필요: False

### [P2·broken] compare-dark-mode-broken-blocks
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:312, 341, 429, 291-293, 567-570`
- **근거**: 세 강조 블록이 배경만 밝게 박고 color 를 안 준다: `background:#f8fafc`(용어 정리) · `background:#e2f6ec`(★ 같은 부피로 잘라 보면 모양이 다르다) · `background:#fef9c3`(★ 계통 편향이 아니다). 다크 토큰은 `--text:#e8ebf2`(style.css:31 블록)라 거의 흰 글자가 거의 흰 배경 위에 온다 — 페이지의 별표 결론 둘이 다크에서 사라진다. 차트도 둘: plotBvse 의 `Plotly.newPlot('bvse-chart', tr, {margin:...,xaxis:...,yaxis:...,legend:...})` 와 msd3 의 newPlot 은 base.html 이 제공하는 plotlyFont()/plotlyBG() 를 안 쓰고 `window.addEventListener('themechange',...)` 에도 안 걸려 있다(cmpchart/cmpradar 만 걸려 있다). 덤으로 `var(--line,#e5e7eb)` 13회는 정의된 적 없는 토큰이라 항상 밝은 회색 폴백이다(정의된 이름은 --border).
- **고치는 법**: 세 블록에 `color:var(--text)` 를 주거나 .callout 계열 클래스로 바꾼다. 두 차트에 plotlyFont()/plotlyBG() 를 넣고 themechange 리스너에 재렌더를 추가한다. var(--line) 은 var(--border) 로 일괄 교체.
- codex 필요: False

### [P2·wrong] elements-icohp-system-is-raw-key
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/elements.html:88, 165 · /home/user/Yonghoon-DEM-DFT/webapp/data.py (_all_icohp_bonds)`
- **근거**: ICOHP 칩이 `'</b> eV <span class="muted">@'+x.system+'</span>'` 로 내부 키를 그대로 찍는다. 실측 systems = ['b2o3','lpsocl','nd'] 인데 'nd' 는 조성 id 가 아니다(해당 조성은 modelc_nd_doped). Nd+Cl 브리핑 실측 결과: {"bond":"Nd-Cl","d":2.772,"icohp":-0.571,"system":"nd"} → 화면에 `Nd-Cl −0.571 @nd`. 링크도 없어서 어느 계산인지 되짚을 수 없다. 그리고 per-bond ICOHP 는 3계뿐이라 P·S 를 눌러도 comp1/comp2/modelc 결합은 안 나온다(반면 explorer 의 ICOHP_PS 는 6조성에 값이 있다).
- **고치는 법**: system 키를 COMPOSITIONS 라벨로 매핑해 표시하고 /composition/<cid> 로 링크한다('nd' → modelc_nd_doped). 매핑이 없는 키는 조용히 숨기지 말고 '조성 미배선' 으로 표시.
- codex 필요: False

### [P2·useless] elf-column-has-no-discriminating-power
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:11-13 · /home/user/Yonghoon-DEM-DFT/webapp/data.py:1009-1012`
- **근거**: ELF P–S 열의 실측 전량: {'comp1': 0.924, 'modelc': 0.923, 'lpsocl': 0.924} — 셋이 0.001 안에 있다. EXTRA_META 자신이 그렇게 적어 놨다: `⚠ midpoint 는 짧은 결합에서 lone-pair 에 걸려 다 0.94 로 뭉친다(판별력 없음)`. 그런데 이 열은 정렬 가능(`onclick="expSort(...)" class="sortable-h num xcol"`)이라 화면이 무의미한 순위를 매기라고 권한다. Bader P 열도 3계뿐이다.
- **고치는 법**: 두 xcol 을 '세부 분석' 접힘 그룹으로 내리고 ELF 열은 정렬을 끈다(또는 '판별력 없음' 을 헤더에 직접 표시). 값을 지우자는 게 아니라 순위 지표처럼 보이지 않게 하자는 것.
- codex 필요: False

### [P2·ia] empty-composition-shells
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/base.html:94-99 · /home/user/Yonghoon-DEM-DFT/webapp/templates/compare.html:10-13 · /home/user/Yonghoon-DEM-DFT/webapp/data.py COMPOSITIONS`
- **근거**: COMPOSITIONS 14개 중 5개(comp3 LPSCl I · comp4 LPSBr · comp5 LPSI · modelc_v3 · lic6)가 canonical 값 0 · 분석 파일 0 이다(실측). 그런데 사이드바 Compositions 목록에 14개가 다 뜨고, /compare 의 체크박스 칩도 14개 전부 고를 수 있으며 골라도 열 전체가 TODO 로 채워질 뿐이다. explorer 에서는 hasval=0 으로 숨겨져 세 화면이 서로 다른 답을 준다.
- **고치는 법**: 빈 조성은 '계획됨(자료 없음)' 로 묶어 사이드바 하단 접힘에 넣고 compare 칩에서는 비활성으로 표시한다. 지우지는 말 것 — 캠페인 범위 선언이다.
- codex 필요: False

### [P2·missing] analysis-chips-missing-why-and-dead-order
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/data.py:1014-1026, 1028-1044 · /home/user/Yonghoon-DEM-DFT/webapp/templates/explorer.html:101-102`
- **근거**: '보유 분석' 칩에 쓰이는 태그 24종 중 8종(Binding·Conductivity·Drag·Gap·MD·PMF·Voronoi·탄성)이 ANALYSIS_WHY 에 없어 툴팁이 태그명 그대로다(템플릿 `title="{{ awhy.get(tag, tag) }}..."`). 반대로 ANALYSIS_WHY 의 'Diffusion' 은 아무 조성에도 안 붙는다. 그리고 정렬 상수 `_ANALYSIS_ORDER = ["DOS","PDOS","ELF",...]`(data.py:1014)는 repo 전체에서 정의부 말고 참조가 0건이다 — 템플릿은 `{% for tag, n in am|dictsort %}` 로 알파벳순을 쓴다.
- **고치는 법**: 빠진 8종의 설명을 ANALYSIS_WHY 에 채우고, 칩 정렬을 _ANALYSIS_ORDER 로 되돌리거나 그 상수를 지운다(둘 중 하나 — 지금은 있는 척만 하고 있다).
- codex 필요: False

### [P2·broken] elements-ships-118kb-mo-blob
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/elements.html:43 · /home/user/Yonghoon-DEM-DFT/webapp/app.py:402-409`
- **근거**: `<script>window.MO_DB={{ mo_db|tojson }};</script>` 가 매 요청마다 117,792 바이트를 인라인으로 싣는다(실측). /elements 전체 응답 298 KB 중 40%다. 실제로는 사용자가 '⚛ MO' 배지를 누른 화합물 하나(114개 중)만 필요하다.
- **고치는 법**: MO_DB 를 /api/mo/<key> 로 lazy 로 가져오거나, 최소한 static JSON 파일로 빼서 캐시가 듣게 한다. 같은 blob 이 /cascade 에도 실린다.
- codex 필요: False

### [P2·duplicate] three-value-views-no-canonical-entry
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/templates/base.html:50-55 (nav '결과 보기') · /explorer · /compare · /composition/<cid>`
- **근거**: 세 화면이 같은 canonical_registry 를 그린다 — /explorer 는 14조성 × 24열 전체, /compare 는 선택분 × 19행(b.canonical 키 실측 19개)에 차트 2개, /composition/<cid> 는 한 조성의 같은 값 + 같은 배지 체계. compare 만의 고유 가치는 (a) 비교묶음 강제 차트와 (b) 손으로 쓴 해설 카드 4장인데, (b)는 카드 주석 자신이 `(/concept/bvse §7-9 요약)` · `상세는 /concept/dft §12` 라고 출처를 대며 개념 페이지의 복제임을 밝힌다. 사이드바에는 셋이 같은 무게로 나열돼 있고 어느 게 정본 진입점인지 표시가 없다.
- **고치는 법**: v3 재편안: /explorer 를 정본 값 진입점으로 선언(부제에 명시), /compare 는 '두 계를 나란히' 도구로 좁혀 표를 explorer 로 링크하고, 해설 카드 4장은 /concept/* 로 옮겨 compare 에는 한 줄 요약 + 링크만 남긴다. 남기더라도 최신순으로 재배열하고 옛 카드는 접는다(현재 순서는 07-29 → 08-05 → 08-05 → 08-04 로 아무 기준도 아니다).
- codex 필요: False

### [P2·duplicate] element-electronegativity-two-sources
- **어디**: `/home/user/Yonghoon-DEM-DFT/webapp/data.py:element_info / ELEMENT_EN · load_element_kb`
- **근거**: element_info 는 하드코딩 dict ELEMENT_EN(88종)만 읽는다. 원소 kb 는 118종 전부 있고 그중 13종(Xe·Kr·Rn·Pa·Pm·Am·Bk·Cf·Cm·Es·Fm·Md·No)은 kb 에 electronegativity 가 있는데 ELEMENT_EN 에 없어 화면에서 '전기음성도' 줄이 통째로 빠진다(실측: Xe kb 2.6, element_info en=None). Tb 는 두 출처가 다르다 — kb 1.2 vs ELEMENT_EN 1.1.
- **고치는 법**: element_info 가 kb 값을 우선 읽고 ELEMENT_EN 은 폴백으로만 쓴다. 불일치(Tb)는 출처를 하나로 정리.
- codex 필요: False
