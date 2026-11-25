# webapp — 조성 상세(/composition/&lt;cid&gt;) + 주기율표(/elements, /api/element, /api/property)

## 지금 무엇인가
조성 14개 각각의 "깊게 보는" 단일 페이지다 — 상단에 레지스트리에서 뽑은 canonical metric 타일 19개, 그 아래 캐스케이드 배너(b2o3·modelc_nd_doped 만), 그리고 Structure/Charts/Bonding/Raw/Record 5탭. 값의 지위(정본·잠정·철회·출처⚠·구 잣대)를 배지로 붙이는 규율은 이 화면이 repo 에서 제일 잘 되어 있다. 주기율표(/elements)는 118칸을 눌러 원소 브리핑을 /api/element 로 받아오는 별도 화면이고, /api/property/&lt;name&gt; 은 db/properties/*.json 을 artifact_policy 게이트를 통해 내보내는 라우트인데 **템플릿·JS 어디서도 부르지 않는다**.

## 처음 오는 사람
처음 온 사람이 /composition/comp1 을 열면 제목 한 줄("LPSCl · Li₆PS₅Cl · cubic-52 · argyrodite")과 숫자 타일 19개를 본다. 그중 14개가 회색 점선 `TODO` 이고 11개는 `SDCP_Eads_eV__sdcp_neutral_cross_Ni_at_Li` 같은 **기계 키 이름 그대로**다 — LPSCl 페이지에 SDCP(분자·NCM 표면) 항목이 왜 있는지 알 방법이 없다. comp3·comp4·comp5·modelc_v3·li3n·lic6·vgcf_hbn 은 19개 중 19개(또는 18개)가 TODO 라, 페이지 전체가 "아무것도 없음"의 벽이다. 이 조성이 무엇인지·왜 계산했는지·무엇이 결론인지를 말하는 문장이 **한 줄도 없고**, 본문 전체의 바깥 링크는 `/compare` **딱 하나**다(구조 다운로드 제외). ICOHP·ELF·Bader·BVSE·β 게이트 같은 용어가 카드 제목으로 나오는데 /glossary·/concept 에 이미 있는 해설로 가는 링크가 없다. 값을 눌러도 그 값을 만든 파일(레지스트리 `source_path`)로 못 가고, 값이 언제 갱신됐는지(`updated`)도 안 보인다. 반대로 잘 되어 있는 것: 각 카드가 "이 값을 왜 이렇게 읽어야 하나"(ELF 는 중앙 [0.40,0.60] 최솟값, COHP 곡선 x눈금은 패널마다 다름, Bader 절대값은 밀도 소스 의존)를 한국어로 길게 적어 둔다 — 이건 초심자에게 이 repo 최고의 자산이라 절대 지우면 안 된다.

## 건드리면 안 되는 것
- metric 타일의 **배지 3축 분리** — status(정본/잠정/철회/인용불가/출처미배선) · 출처⚠(canonical_prov) · 잣대 세대(구 잣대). 이건 2026-09-07 에 b2o3 철회값이 정상 카드처럼 뜬 사고(data.py:1074-1081 주석) 뒤에 붙인 것이고, 시험(test_webapp.py:1350-1365)이 '같은 라벨 두 번' 만 금지하고 '배지 여러 개' 는 정상이라고 못 박아 뒀다. v3 에서 타일을 재설계해도 이 세 축은 그대로 살린다.
- .metric 카드의 `mm`(방법·출처 주석)에 걸린 **claimbind 필터** — 다른 계의 정본값을 인용하는 자유 문장에 렌더 시점에 결속을 붙인다(composition.html:49-50, app.py:196-204). /composition/modelc 에서 실제로 `data-claim="MD_Ea_eV@b2o3"` 로 작동 중이다. 제거하면 철회값 인용이 다시 무표시로 돌아간다.
- b2o3 캐스케이드 배너의 **빨간 '같은 조성의 검증이 아니다' 상자**(composition.html:71-88) — 도펀트 라벨 join 을 validation 이라 부르지 않게 막는 장치이고 test_b2o3_page_does_not_claim_a_same_composition_validation(test_webapp.py:1872-1890)이 지킨다. 문구·조건 모두 손대지 말 것.
- 각 Bonding 카드에 달린 **긴 한국어 판독 규율 문장들** — ELF 판정은 [0.40,0.60] 창 최솟값이고 곡선 전체 최솟값은 Li 1s|2s 코어 노드다(composition.html:298-310) / COHP x눈금은 패널마다 다르다 · window_coverage<95% 면 면적으로 ICOHP 를 주장하지 말라(260-269) / 구형 CSV 는 sum 이라 N 이 다른 패널 높이를 비교하지 말라(250-254) / Bader 절대값은 밀도 소스에 따라 통째로 달라진다(413-416) / std 큰 자리는 평균 하나로 말하면 안 된다(357-360). 이게 이 화면이 지식 허브인 이유다 — 줄이거나 툴팁으로 접지 말 것.
- Charts 탭의 **CSV 자기 캐비앳 승격**(`#` 머리말 → `.cal-warn` 상자, composition.html:173-175)과 **y 기본 시리즈에서 `^sig` 제외**(742-743줄 NOISE 정규식). 후자가 CLAUDE.md 'MD σ 절대값 인용 금지' 를 화면에서 강제하는 유일한 장치다 — 체크박스 opt-in 은 남기되 기본 제외는 유지.
- 3D 뷰어의 **PS₄ 사면체 + 주기 이미지 ±1셀 탐색**(composition.html:593-618)과 80 ms 뒤 재적용(702-705줄). 셀 경계 P 의 파트너가 옆 셀에 있어 사면체가 4개 중 1개만 그려지던 실측 버그의 수정이다. 구조 목록을 접거나 정리하더라도 이 렌더 로직은 그대로.
- CDN 실패 시의 **정직한 실패 문구** — Plotly/3Dmol 미로드 시 '차트 라이브러리를 불러오지 못했어요', 파서 없는 확장자는 '다운로드해서 VESTA로 보세요' + 다운로드 버튼(composition.html:665-686, 776줄). 빈 화면 대신 이유를 말한다.
- artifact_policy 의 **fail-closed 원칙 자체**(webapp/artifact_policy.py) — 매니페스트에 없는 cascade artifact 를 미승인으로 다루는 것. 'cascade-estimand-403' 은 이 정책을 완화하라는 뜻이 아니라 **거버넌스 문서를 랭킹 산출물과 구별하라**는 뜻이다.
- /composition/sdcp·li3n 등의 **N/A 타일과 그 사유 문장**(data.py:744-765) — 'UMA MLIP 금지 조성', '분자계 — 주기 밴드갭 대신 HOMO–LUMO 축', '슬랩 — 벌크 탄성텐서 정의 안 됨'. TODO 정리를 하더라도 N/A 는 TODO 와 합치지 말 것. 사유 문장은 이 repo 규율의 실물이다.

## 발견

### [P0·wrong] copy-drops-status
- **어디**: `webapp/templates/composition.html:803-810 (copyComp)`
- **근거**: /composition/b2o3 의 '📋 값 복사' 가 생성하는 실제 문자열: `MD Ea: 0.199 eV  [UMA-s-1p1 · 600/800/1000 K 3점 피팅 · ⚠절대값 인용 금지. …]` 그리고 마지막 줄 `— 출처: …/composition/b2o3 (canonical, 방법 표기 포함)`. 화면 타일에는 `철회` 배지가 붙어 있는데(canonical_status_for → status='retracted') copyComp 루프는 canonical/labels/units/canonical_meta/canonical_provisional 만 읽고 **canonical_status 를 안 읽는다**. 즉 철회값 0.199 가 'canonical' 이라는 꼬리표를 달고 클립보드로 나간다. 같은 줄이 MD Ea (단일시드 앵커) 0.2234 의 `잠정` 도 떨어뜨린다.
- **고치는 법**: copyComp 루프에 canonical_status.get(k) 를 넣어 라벨 뒤에 `[철회 — 인용 금지: <why>]` / `[잠정]` / `[인용불가]` 를 강제로 붙이고, 철회·비인용 항목은 기본적으로 **복사에서 빼거나** 사유+대체값(registry `retracted.usable_instead`)까지 같이 넣는다. 꼬리말 '(canonical, 방법 표기 포함)' 은 실제로 canonical 인 항목만 있을 때만 쓴다. 회귀시험: b2o3 복사문자열에 '철회' 가 없으면 실패.
- codex 필요: False

### [P0·wrong] nd-icohp-cutoff-artifact
- **어디**: `webapp/data.py:2115-2123 (icohp_for 가 d['bonds'] 를 그대로 쓴다) → webapp/templates/composition.html:213 표`
- **근거**: /composition/modelc_nd_doped 의 첫 Bonding 카드가 `Li-S | 125 | 2.521 | -2.493`, `Li-Cl | 74 | 2.520 | -2.265` 를 경고 없이 찍는다. 같은 파일 db/properties/nd_icohp.json 의 `_CORRECTION_2026_06_18` 은 그 두 값을 이렇게 부른다: "Previous Li-S -2.49/+45% & Li-Cl -2.27/+7.7% were CUTOFF ARTIFACTS (3.2/3.4 A). Correct values below". 정정본 `bonds_4.0A_cutoff_for_comparison` 은 Li-S -1.647(N=199) · Li-Cl -2.132(N=79) 다. 게다가 같은 페이지 아래 '계 간 비교' 카드는 정정값 -1.647/-2.132 를 쓰고 그 밑에 CUTOFF ARTIFACTS 문장을 붙인다 — **한 화면에서 표 두 개가 서로를 부정한다**. 템플릿은 headline 만 `headline_CORRECTED or headline` 로 정정본을 쓰고 표는 안 고쳤다(composition.html:223).
- **고치는 법**: icohp_for 에서 `_CORRECTION*` 이 있고 `bonds_4.0A_cutoff_for_comparison` 이 있으면 그쪽을 `bonds` 로 승격(원래 bonds 는 `bonds_superseded` 로 옮겨 접힘 처리), 승격했다는 표시를 표 머리에 남긴다. 승격이 부담이면 최소한 `_CORRECTION*` 문자열을 ICOHP 표 **바로 위**에 빨간 상자로 올리고 -2.493/-2.265 에 취소선을 건다. 회귀시험: /composition/modelc_nd_doped 본문에 '-2.493' 이 있으면 그 앞 500자 안에 'CUTOFF ARTIFACT' 가 있어야 통과.
- codex 필요: False

### [P1·useless] sdcp-metric-flood
- **어디**: `webapp/data.py:770 (_METRIC_LABEL) · data.py:782 metric_meta() · composition.html:22-62`
- **근거**: metric_meta() 가 레지스트리의 **모든** metric 을 내보내고 템플릿이 그걸 전수 렌더한다 → 14개 조성 전부에 19개 타일. 그중 11개가 SDCP 전용(`SDCP_dE_site_meV__ptfe_dimer_pm1` … `SDCP_Eads_eV__sdcp_neutral_cross_Ni_at_Li`)이고 _METRIC_LABEL 에 항목이 없어 **라벨=기계 키, unit=빈칸, canonical_meta=빈칸**으로 나온다. 실측: /composition/comp3 는 19타일 전부 TODO, 그중 11개가 SDCP_ 키다. 역방향으로 /composition/sdcp 에서는 그 11개가 값을 갖는데 방법 주석(canonical_meta) 이 없어 `36.071` 이 단위·출처 없이 뜬다 — 'db/properties/electronic.json' 류의 출처 문장이 하나도 없다(CLAUDE.md '값에는 출처가 있어야 한다' 위반). 템플릿 주석(52-53줄)이 이미 '하면 안 되거나 정의되지 않는 축은 TODO 로 광고하면 안 된다' 고 적어 뒀는데 SDCP 축이 정확히 그 경우다.
- **고치는 법**: ① metric 에 `applies_to`(계열: bulk-SE / molecule-surface) 를 붙여 그 계열의 조성에만 타일을 만든다. ② 남는 SDCP_* 11개는 _METRIC_LABEL 에 label/unit(meV·eV)/short 와 CANONICAL_META 방법 문장을 채운다. ③ 값 없는 축은 타일이 아니라 카드 하단 '아직 없는 축 N개' 접힘 한 줄로.
- codex 필요: False

### [P1·ia] all-todo-pages
- **어디**: `/composition/comp3 · comp4 · comp5 · modelc_v3 · li3n · lic6 · vgcf_hbn (composition.html:60)`
- **근거**: canonical_values() 실측 — comp3/comp4/comp5/modelc_v3/vgcf_hbn/li3n/lic6 는 canonical 값이 **0개**다(modelc_nd_doped 는 ICOHP_PS 하나뿐). 그래서 화면은 `<div class="metric todo"><div class="mv">TODO</div>` 가 19개 늘어선 벽이고, comp3/comp4/comp5 는 Charts CSV 0건 · 구조 파일 1건이라 탭도 `📊 Charts (0)` `🗂 Raw (0)` 로 빈다. 사이드바 Compositions 목록은 14개를 전부 같은 무게로 나열해서, 처음 온 사람은 comp3 과 lpsocl 을 구별할 단서가 없다.
- **고치는 법**: 조성마다 '상태'(활성 캠페인 / 보류 / 참고용 후보)를 db 에 선언하고 사이드바·카드에 배지로 노출. 값 0개인 조성은 상세 페이지 상단에 '이 조성은 아직 계산 전이다 — 왜 목록에 있나'를 한 줄로 적고 TODO 타일 19개는 접는다. v3 재편에서 '최신·중요한 것이 앞' 원칙을 사이드바 Compositions 정렬에도 적용(lpsocl·modelc·b2o3 먼저).
- codex 필요: False

### [P1·stale] nd-anneal-invisible
- **어디**: `webapp/data.py:445 `_PREFIX["modelc_nd_doped"] = ["modelc_nd", "nd_"]` · structures_for()`
- **근거**: 커밋 83c868a97(2026-09-07) 이 db/structures/ndo_lpscl16_rietveld_2026_09_07/ 아래에 Rietveld 후보 21개 + anneal_2026_09_07/ 완화구조 6개 + anneal_results.json(순위 distributed < free_s < bo4)을 넣었다. 그런데 /composition/modelc_nd_doped 의 3D 구조 버튼은 `modelc_nd_doped_DFTrelax.cif` · `.xyz` **2개뿐**이다. 원인: rel.replace('/','_') = `ndo_lpscl16_...` 이라 prefix `nd_`(밑줄 포함)로 시작하지 않는다. 파일 자체는 살아 있다 — `/api/structure/ndo_lpscl16_rietveld_2026_09_07/anneal_2026_09_07/ndo_lpscl16_n4fu_O-bo4_post_relax.xyz` 는 200 · 10603 bytes 로 서빙된다. 즉 **가장 최신 Nd 작업이 화면에서만 사라졌다**.
- **고치는 법**: _PREFIX 에 'ndo' 를 추가하거나(권장) 조성↔파일 매칭을 prefix 문자열이 아니라 db 쪽 명시 매니페스트로 바꾼다. 더불어 anneal_results.json 의 순위(distributed < free_s < bo4)를 Nd 페이지 상단 카드로 올린다 — 지금 이 순위는 커밋 메시지에만 있다.
- codex 필요: False

### [P1·useless] struct-button-wall
- **어디**: `webapp/templates/composition.html:129-135 (구조 버튼 flex-wrap 루프)`
- **근거**: 실측 버튼 수 — sdcp **96개**, vgcf_hbn 64개, li3n 60개, lpsocl 11개. sdcp 목록에는 `c12_frozen/sdcp_neutral__LiNi_bridge__fib11__r270.xyz` 처럼 사람이 고를 수 없는 이름과, 같은 구조의 .xyz/.vasp/.vesta 3종 세트가 섞여 있다(예: sdcp_phaseB_complex_doped 가 3번). .vesta 는 fmt 가 없어 눌러도 '3D 파서 없음' 만 뜬다.
- **고치는 법**: 기본은 대표 구조 3~5개만 버튼으로, 나머지는 `<details> 전체 N개` 접힘. 같은 stem 의 .xyz/.vasp/.vesta 는 **한 항목으로 묶고** 형식은 다운로드 드롭다운으로. 폴더(c12_frozen/, sdcp_poses_qe/ …)로 그룹 헤더를 만든다.
- codex 필요: False

### [P1·stale] raw-tab-june-snapshot
- **어디**: `webapp/templates/composition.html:186 · db/_index.json`
- **근거**: Raw 탭 배너 렌더 결과: `⚠ 출처 = db/_index.json 스냅샷 (2026-06-02 생성) — canonical 아님`. db/_index.json 의 `built` 는 `2026-06-02T13:45:00` 으로 3개월 전이고, tools/ 안에 이 파일을 다시 만드는 스크립트가 **없다**(`grep -rln "_index.json" tools/` → 0건). 결과가 조성별로 심하게 어긋난다: comp1 97행 / modelc 51행 / lpsocl **4행** / sdcp **0행** — 즉 6월 이후 만들어진 조성일수록 Raw 탭이 비어 있다. 같은 이유로 Record 탭도 db/compositions/*.json 8개(comp1~5·modelc·modelc_v3·modelc_nd_doped)에만 있어서 lpsocl·b2o3·sdcp 는 탭 자체가 사라진다.
- **고치는 법**: 둘 중 하나로 정한다 — (A) 재생성 도구를 만들고 배너에 built 날짜+재생성 명령을 싣는다, (B) Raw/Record 탭을 은퇴시키고 '원자료 파일'은 /files 링크로 대체한다. 지금처럼 '갱신 불가능한 6월 스냅샷을 조성마다 다른 밀도로' 두는 것이 제일 나쁘다.
- codex 필요: True

### [P1·missing] lpsocl-closure-missing
- **어디**: `/composition/lpsocl (composition.html 전체) · db/properties/lpsocl_box331_closure_conditions_2026_09_07.json · db/governance/decisions.json D-2026-09-08-lpsocl-box331-closure-conditions(active)`
- **근거**: 2026-09-08 에 1저자가 LPSOCl 3×3×1 400 ps 9런의 **닫힘 조건**을 비준했고(커밋 5196c1081, decisions.json status=active), 카드 파일도 db/properties 에 있다. /composition/lpsocl 렌더 결과에는 '닫힘'·'closure'·'400 ps'·'3×3×1'·'보고량' 문자열이 **0회**다. 화면이 말하는 lpsocl MD Ea 는 여전히 `0.287 eV · 잠정 · 구 잣대` 하나뿐이고, 그 값을 대체할 캠페인이 진행 중이라는 사실이 어디에도 없다. 같은 문제로 D-2026-09-08-cascade-d-rel-estimand(active)·D-2026-09-08-b2o3-uma-vs-dft-force(active)도 해당 조성 페이지에 없다.
- **고치는 법**: 조성 페이지 상단(metric 타일 바로 아래)에 '이 조성의 살아 있는 결정' 스트립을 만든다 — decisions.json 에서 applies_to.systems 로 필터해 제목·상태(active/proposed)·날짜·/governance 링크를 카드 2~3개. 닫힘 조건 파일(`*_closed_*.json`·`*_closure_conditions_*.json`)이 있으면 '마감/재개 조건' 배지를 헤더에 단다.
- codex 필요: False

### [P1·ia] no-links-out
- **어디**: `/composition/lpsocl 본문 (composition.html:8-430)`
- **근거**: 렌더된 <main> 안의 href 를 전부 뽑으면 `['#', "/api/structure/'+encodeURIComponent(name)+'", '/compare']` — 실링크는 **/compare 하나**다(b2o3·modelc_nd_doped 만 배너에 /cascade 가 하나 더). /methods·/glossary·/concept/<term>·/governance·/files·/explorer·/log 로 가는 길이 본문에 없다. 값의 출처 경로(레지스트리 `source_path`, 예 comp1 gap → db/properties/electronic.json)도 화면에 안 나온다 — 타일에 뜨는 건 CANONICAL_META 의 일반 문장(`fixed-occ eigenvalue (DOS-threshold 금지) · comp2는 잠정…`)뿐이라 **이 조성의 이 값이 어느 파일에서 왔는지**를 화면에서 알 수 없다.
- **고치는 법**: ① 각 metric 타일에 `source_path` 를 /files 또는 /api/property 링크로 달고 `updated` 날짜를 표시. ② 카드 제목(ICOHP·ELF·Bader·COHP·BVSE)을 /concept/<id> 로 링크. ③ 페이지 하단에 '더 보기' 줄 — 방법(/methods) · 판정 원장(/governance) · 원자료(/files?q=<cid>) · 비교(/compare) · 미결(/todo).
- codex 필요: False

### [P1·wrong] retracted-value-styling
- **어디**: `webapp/static/css/style.css:190 `.metric .mv` · webapp/data.py:1163-1168 (why 400자 절단) · composition.html:35-37`
- **근거**: 철회값도 정본과 **같은** 큰 글씨/네이비/굵게로 찍힌다 — /composition/b2o3 의 `0.199` 는 1.28rem·800·var(--navy). 구분은 옆의 작은 `철회` 배지뿐이다. 정작 같은 페이지 Raw 탭은 폐기 항목에 `text-decoration:line-through;opacity:.65`(composition.html:190)를 건다 — **한 페이지 안에서 규칙이 두 개**다. 배지 tooltip 도 부실하다: 실제 title 문자열이 `… ⛔ **2026-08-25 철회** — 위 retracted 절 참조. …(중략)… gate_detail.lineage.ol` 로 400자에서 단어 중간이 잘리고, 마크다운 `**` 가 그대로 노출되며, 레지스트리가 갖고 있는 **대체값 `저온 구간만: Ea = 0.2241 ± 0.0606 eV`** 는 안 들어간다. 웹앱은 이 대체값을 이미 렌더할 줄 안다 — /composition/modelc 의 claim-flag tooltip 에는 '· 대신: 저온 구간만: Ea = 0.2241 ± 0.0606 eV …' 가 들어 있다. 즉 **0.199 를 실제로 찍는 페이지(b2o3)에는 claim-flag 가 0개**이고, 그 값을 인용만 하는 페이지(modelc)에만 결속이 붙었다.
- **고치는 법**: status 가 retracted/non_citable 인 타일은 `.mv` 에 취소선+회색을 걸고, 값 아래 한 줄로 `대신 쓸 값: <retracted.usable_instead>` 를 **툴팁이 아니라 본문에** 적는다. 타일 값 자체에도 data-claim(`MD_Ea_eV@b2o3`)을 심어 claim 결속 검사에 잡히게 한다. why 절단은 400자 자르기 대신 요약+상세(details)로.
- codex 필요: False

### [P1·broken] cascade-estimand-403
- **어디**: `webapp/app.py:1062 /api/property/<name> · webapp/artifact_policy.py · db/properties/cascade_audit_manifest.json`
- **근거**: `GET /api/property/cascade_d_rel_estimand_2026_09_08` → **403**, 본문: `{"error": "원장(cascade_audit_manifest.json)에 없는 cascade artifact 다 — 미등록은 미승인으로 다룬다. python3 tools/cascade/build_cascade_audit_manifest.py 로 등록할 것"}`. 이 파일은 2026-09-08 에 1저자가 **비준한(active)** 보고량 카드다(decisions.json D-2026-09-08-cascade-d-rel-estimand, record 필드가 이 경로를 가리킨다). 매니페스트를 확인하면 문자열 'cascade_d_rel_estimand' 가 없다. 정책이 파일명 prefix 'cascade' 만 보고 랭킹 산출물과 거버넌스 카드를 구별하지 못한다.
- **고치는 법**: build_cascade_audit_manifest.py 를 돌려 등록하거나(즉효), 정책에서 `*_estimand_*.json`·`*_closure_conditions_*.json` 처럼 **거버넌스 문서**는 랭킹 게이트 대상에서 빼는 규칙을 명시한다. 회귀시험: decisions.json 의 record/card 경로는 전부 /api/property 200 이어야 한다.
- codex 필요: False

### [P1·useless] na-dead-entry
- **어디**: `webapp/data.py:744-766 CANONICAL_NA · composition.html:52 `{% elif canonical_na.get(key) %}``
- **근거**: CANONICAL_NA 의 두 항목이 **절대 렌더되지 않는다**. ① `("sigma_300K_mS_cm","b2o3")` — canonical_values() 가 내는 19개 키에 sigma_300K_mS_cm 이 없어(레지스트리에 그 metric 이 조성 축으로 없다) 루프에 아예 안 들어온다. 그 안에 담긴 '⛔ 2026-08-25 철회 — MD_Ea_eV 와 같은 사유(골격 재배열). 단일시드 1.33× 는 2026-07-09 에 이미 철회됐고…' 라는 중요한 철회 기록이 화면에서 사라진 상태다. ② `("MD_Ea_eV","b2o3")` 의 긴 철회 설명 — 템플릿이 `{% if val is not none %}` 을 먼저 타는데 b2o3 MD_Ea 는 값 0.199 가 있어서 elif N/A 가지에 절대 도달하지 않는다. 두 텍스트 모두 '…TODO 아님' 으로 끝나는 공들인 설명인데 죽어 있다.
- **고치는 법**: N/A 판정을 '값이 없을 때만'이 아니라 **값 유무와 독립인 축**으로 바꾼다(값이 있어도 N/A/철회 사유를 같은 타일에 표시). 레지스트리에 없는 metric 의 NA 항목은 lint 로 잡아 '원장 부재' 로 표시하거나 삭제한다 — 지금은 조용히 사라진다.
- codex 필요: False

### [P2·duplicate] hardcoded-cascade-counts
- **어디**: `webapp/templates/composition.html:97-99 · webapp/templates/elements.html:130 · webapp/data.py:1725 CASCADE_META.scope`
- **근거**: composition.html 이 직접 박아 둔 문장: `⛔ 아래 rank·score 는 <b>superseded 47종 스냅샷</b>이다 — 현재 승인된 랭킹은 <b>0종</b>. 완주분은 90종이고 재랭킹은 게이트 정의가 닫힌 뒤에 한다.` elements.html:130 이 거의 같은 문장을 또 박았다: `⛔ superseded 스냅샷 — 현재 승인된 랭킹은 0종. 완주분은 90종.` 한편 data.py 의 CASCADE_META.scope 는 `도펀트 91종 스크리닝`, cascade.html 은 88·89·90 을 문맥별로 쓴다. 숫자 셋(90/91/89)이 세 파일에 손으로 흩어져 있어 캐스케이드 상태가 바뀌면 조성 페이지·주기율표가 조용히 거짓이 된다.
- **고치는 법**: '승인 랭킹 종수 / 완주 종수 / 후보 종수'를 data.py 한 곳(또는 cascade_audit_manifest)에서 계산해 세 템플릿이 그 값을 렌더한다. 문구도 include 한 조각으로 공유.
- codex 필요: False

### [P2·broken] bader-undefined-500
- **어디**: `webapp/templates/composition.html:405`
- **근거**: `{%- if icohp._comparison_bader.get(el) %}` 가 `{% if icohp.bader %}` 안에만 들어 있고 `_comparison_bader` 존재 검사 밖이다. Jinja 재현 확인: `{% if d.bader %}{% if d._comparison_bader.get(1) %}…` 에 `d={'bader':{...}}` 를 넣으면 `UndefinedError: 'dict object' has no attribute '_comparison_bader'` 로 즉사한다. 현재는 bader 가 있는 유일한 계(lpsocl)가 _comparison_bader 도 갖고 있어 14페이지 전부 200 이지만, bader 만 있는 ICOHP JSON 이 하나 들어오면 그 조성 페이지가 500 이 된다(같은 패턴으로 comp1/modelc 가 500 났던 전례가 205줄 주석에 적혀 있다).
- **고치는 법**: 400줄의 `{% if icohp._comparison_bader %}` 가드를 note 셀(404-406줄)까지 감싸거나, `icohp.get('_comparison_bader', {})` 로 방어. 음성 경로 시험 추가(bader 만 있는 픽스처).
- codex 필요: False

### [P2·duplicate] li3n-vgcf-csv-overlap
- **어디**: `webapp/data.py:446 `"vgcf_hbn": ["vgcf", "hbn", "li3n", "lic6"]` · _PREFIX 에 li3n·lic6·sdcp 항목 없음`
- **근거**: vgcf_hbn 이 li3n·lic6 를 자기 prefix 로 갖고, li3n·lic6 는 _PREFIX 에 없어 fallback [cid] 로 같은 문자열을 쓴다. 결과: `li3n_eads_origin.csv` · `li3n_barrier_origin.csv` · `li3n_neb_fit_optimal.csv` · `li3n_drag_profile_kisti.csv` 등이 /composition/li3n 과 /composition/vgcf_hbn **양쪽 Charts 탭에 동시에** 뜬다(li3n 8칩 중 8개, vgcf_hbn 13칩 중 5개가 li3n_* 파일). 구조도 li3n 60개 · vgcf_hbn 64개로 대부분 겹친다. /composition/lic6 는 CSV 1개(`li3n_lic6_profile_origin.csv`)·구조 0개라 사실상 빈 페이지다.
- **고치는 법**: '이 파일은 어느 조성의 것인가'를 파일명 prefix 가 아니라 db 매니페스트(파일→조성 목록)로 선언한다. 공유 파일은 '공유' 배지를 달아 어느 쪽이 주인인지 화면에 적는다. li3n/lic6/sdcp 를 _PREFIX 에 명시(현재 fallback 이라 규칙이 안 보인다).
- codex 필요: False

### [P2·ia] chip-label-data
- **어디**: `webapp/templates/composition.html:166 (Charts 칩) · datafiles_for kind 분류`
- **근거**: /composition/sdcp 의 CSV 칩 15개 중 11개가 `data` 로 같은 이름이다 (`sdcp_n6_ring_profile_fig.csv`, `sdcp_nseries_spin_2026_09_08.csv`, `sdcp_wave1_results.csv`, `sdcp_v7c_phaseB_energies.csv` …). modelc 은 24칩 중 8개, lpsocl 은 23칩 중 여러 개가 `data`. 칩만 보고는 어느 걸 눌러야 할지 알 수 없고, 눌러야만 파일명이 chart-src 에 뜬다.
- **고치는 법**: 칩 라벨을 kind 대신 '파일 stem 축약 + kind 배지'로 바꾸거나, kind 미분류 파일은 CSV 첫 줄 주석/열 이름으로 kind 를 추론한다. 최소한 칩 title 에 파일명을 넣는다.
- codex 필요: False

### [P2·useless] api-property-unused
- **어디**: `webapp/app.py:1062 `/api/property/<name>``
- **근거**: `grep -rn "api/property" webapp/` 결과는 app.py 정의 1건, artifact_policy.py 독스트링 1건, tests 3건뿐 — **템플릿·static/js 어디서도 호출하지 않는다**. 즉 화면 기능이 아니라 사람이 URL 을 직접 치는 용도인데 그 안내도 어디에도 없다. 반면 artifact_policy 게이트(403·envelope)는 이 라우트에만 실질적으로 걸려 있다.
- **고치는 법**: 조성 페이지의 metric 타일·차트 출처를 이 라우트로 링크해 실제 소비자를 만들거나(권장 — 'no-links-out' 과 한 번에 해결), 쓰지 않을 거면 문서화된 공개 API 로 명시하고 /files 또는 /methods 에서 사용법을 안내한다.
- codex 필요: False

### [P2·ia] elements-mo-inline
- **어디**: `webapp/templates/elements.html:43 `window.MO_DB={{ mo_db|tojson }}` · app.py:403 elements()`
- **근거**: /elements 응답은 총 **298,365 bytes** 이고 그중 두 번째 인라인 <script> 가 **117,806 bytes** — 분자오비탈 DB 전체다. 이 데이터는 사용자가 원소를 고르고 그 원소의 대표 화합물 '⚛ MO' 배지를 눌렀을 때만 쓰인다. 주기율표를 그냥 보러 온 사람도 매번 118 KB 를 받는다.
- **고치는 법**: MO_DB 를 `/api/mo` 또는 정적 JSON 으로 빼고 모달 열 때 fetch. 또는 화면에 실제로 있는 대표 화합물 키만 서버에서 골라 내려보낸다.
- codex 필요: False

### [P2·buried] default-tab-structure
- **어디**: `webapp/templates/composition.html:115-121 (탭 순서·기본 활성)`
- **근거**: 기본 활성 탭이 `🧊 Structure` 다(116줄 `class="active"`). 이 화면에서 가장 밀도 높은 과학 — ICOHP 표 · COHP 곡선 · ELF 판정 · Bader 전하 · 자리별 결합 세기 · 계 간 비교(도핑이 host 를 건드렸나) — 는 3번째 `🔗 Bonding` 탭 안에 통째로 들어가 있고, 그 탭 버튼은 icohp/cohp/elf 중 하나라도 있는 4개 조성에만 나온다. Charts 도 탭을 눌러야 비로소 첫 CSV 를 그린다(`window._firstCsv`). 즉 페이지를 열었을 때 보이는 것은 회전하는 3D 공-막대와 TODO 타일 벽이다.
- **고치는 법**: 기본 탭을 Bonding(있으면)→Charts→Structure 순으로 내리거나, 탭 대신 '핵심 결론 카드'를 상단에 고정하고 3D 는 그 아래로. URL 해시(#bonding)로 직접 열 수 있게 하고, 탭 라벨에 건수뿐 아니라 '무엇이 들었나'(ICOHP·COHP·ELF·Bader)를 적는다.
- codex 필요: False
