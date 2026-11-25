# webapp — /benchmarks · /nd-survey

## 지금 무엇인가
/benchmarks 는 2026-08 심포지엄 덱·논문에서 뽑은 외부 소환값 재현 표적 페이지인데, 실제로는 우리 자신의 판정 정정 이력(V1–V7)·MLIP 위원회 기준선(T1)·힘 벤치(T1b)까지 얹힌 1,500줄짜리 단일 화면이다. /nd-survey 는 Nd 치환 문헌 54편을 system_class(우리 화학과의 거리)로 줄 세운 색인 한 장이다. 둘 다 db/properties/ JSON 하나(+data.py 하드코딩 원장)를 순서대로 통째로 뿌리는 구조다.

## 처음 오는 사람
/benchmarks 는 맨 위 다섯 줄이 전부 "⛔ 하지 마라"다 — 이게 무엇을 모은 화면인지 말해 주기 전에 금지부터 나온다. 바로 아래 "덱 정정 원장 6건" 표가 오는데 그 6건 중 3건은 같은 페이지 아래에서 이미 철회된 판정이라(2026-08-03 "덱 오류가 아니라 우리 전사 오류"), 위만 읽고 나가면 "저 랩 덱이 6번 틀렸구나"로 잘못 안다. 그 다음 T1·T2·T3·T5·T9–T15·G1–G4·M6·V1–V7·Q1–Q7·J-1 이 60번 넘게 나오는데 이 코드의 뜻이 페이지에도 /glossary 에도 없다(kb/CODES.md 와 /ledger 에만 있고 링크도 없다). 페이지 전체에서 클릭 가능한 링크는 plink() 로 나가는 /literature 하나뿐이라, "덱"이 뭔지 보려 해도 /talk/lee2026_skku_mlip_materials_design 이 실제로 있는데 아무도 안 걸어 놨다. 정작 우리가 가장 최근에 잰 것(T1b, 2026-08-26 힘 정확도·softening)은 화면 70 % 아래에 있다. /nd-survey 는 사정이 낫다 — "우리 화학과의 거리"를 앞세운 구성 자체가 좋다. 다만 계열 카드가 필터가 아니라 클릭해도 아무 일이 없고, 가장 가까운 3편(032·053·037)은 litdb digest 가 실제로 있는데 링크가 없다. 물질 칸은 42/54 행이 130자에서 말줄임 없이 잘려 "…Nd L3-/Ti K-edge EXAFS analys" 로 끝난다. 그리고 이 페이지 어디에도 우리가 실제로 한 Nd 계산(2026-09-08 Nd₂O₃-LPSCl1.6 어닐 O-모티프 순위)이 없다 — 그건 대시보드에만 있다. 두 화면 모두 /cascade·/compute 에 있는 "처음 보는 사람용(2026-08-25)" 입구 카드가 없다.

## 건드리면 안 되는 것
- /benchmarks 상단 honesty_header 5줄(⛔ 발표 소환값 · 우리 db 절대값과 같은 표 금지 · 부재의 증거 아님 · MLIP σ 절대값 금지 · peer_reviewed_anchors 등급 차이) — 위치는 내려도 되지만 문구는 그대로. 이 페이지가 우리 값과 분리돼 존재하는 이유 자체다.
- '🔁 판정 정정 이력' V1–V7 전체 — 우리가 냈다가 뒤집은 판정이다. '한쪽만 있으면 정직성이 아니라 남 탓이 된다'는 절 머리 문장을 포함해 지우거나 요약하지 말 것. 각 항목의 ⚠ caveat 절(예: V1 의 'Li 음극 축 적용 조건', '생존 3종이라는 숫자 자체도 결론으로 쓰지 말 것')도 삭제 금지.
- '덱 정정 원장' 자체를 지우지 말 것 — 철회된 케이스 1·2·3 도 지우는 게 아니라 '철회' 상태로 표시해 남긴다. 철회 이력을 없애면 2026-08-03 의 '정정의 정정' 교훈(덱이 틀렸다고 기록하기 전에 원해상도로 재판독한다)이 증발한다.
- T1 위원회 절의 '⛔ 이 지표는 절대 정확도를 말하지 않는다'·'⚠ 위원회의 독립성이 보이는 것보다 낮다 — 실질 2진영(MPtrj vs OMat24)'·'⚠ 문턱은 이 표본의 분포에서 유도한 것' 세 경고와 by_element_relative 의 '정규화한 값만 해석한다' 규칙.
- 온도 스윕 절의 '두 열의 방향이 반대인 게 핵심이다' 설명과 2026-09-08 에 새로 들어온 '⚠ 이 적합은 webapp 파생이다 / 두 모형이 사실상 구분되지 않아 모형 선택은 미결정' 단서(커밋 cdb86404c). 이건 리뷰 지적으로 막 들어온 것이라 재편 중 유실 위험이 가장 크다.
- msd_window_trap 문구('영역분해 D 의 시간창이 구획마다 다르다 — 0-11 ns 창을 쓰면 반대 결론이 나온다')와 D 비 0.36 행의 '절대값보다 이 비율만 인용 안전' — MSD 창·MD 절대값 규율의 화면 표면이다.
- /nd-survey 의 '우리 화학과의 거리' 정렬 원칙(sulfide_Li → halide_Li → garnet/perovskite → cathode → other_ion → proton/oxide)과 '가장 큰 덩어리(22편)가 우리와 가장 먼 계열이다' 경고, classification_note('제목+Material studied 문자열 규칙으로 자동 분류한 것이라 완전하지 않다'), 중복 고지('040=039 · 042=002 · 044=020, 파일 57 → 고유 54'). 이 페이지의 존재 이유가 이 네 개다.
- '깔때기 방법론' 카드의 '층이 다르므로 이 서베이 숫자와 합산 금지' 한 줄.
- 두 화면이 우리 db 절대값 페이지와 물리적으로 분리돼 있다는 구조 자체 — 한 화면으로 합치자는 제안은 하지 말 것.
- claim 결속 경로(data-claim / md_html / canonical.scan_claim_bindings) 와 그것을 강제하는 표면별 음성시험 — 템플릿을 재배치할 때 결속 선언이 붙은 요소를 통째로 옮기고, 문자열만 다른 요소로 복사하지 말 것.

## 발견

### [P0·wrong] deck-ledger-3-of-6-retracted
- **어디**: `webapp/data.py:2584-2599 (deck_correction_ledger) → /benchmarks §덱 정정 원장`
- **근거**: 원장 표는 케이스1 을 '덱 표기 17,233 Li·P·S·O → 논문 실물 17,230 Li·O / 개수(3 차이)와 원소집합 둘 다 오기', 케이스2 를 '자릿수 10배 오기 (두 값 모두)', 케이스3 을 "'25 vs 80 °C' 는 논문 어디에도 없음" 으로 살아 있는 판정처럼 싣는다. 같은 페이지 아래 db/properties/external_benchmarks_symposium_2026.json:102 는 '⛔ 2026-08-03 정정의 정정 — 아래 3건은 덱 오류가 아니라 2026-07-28 저해상도 판독의 전사 오류였다. 덱 실물: D 둘 다 x10^-7, 온도 라벨 25/60 degC. kim2026_hts 의 17,233 건도 같은 이유로 철회(덱 원문 17,230 Li, O)' 라고 적혀 있고, coating_screening_scale 신뢰도 칸도 "종전 기록 '17,233 Li-P-S-O'는 우리 전사 오류로 철회" 다. 케이스3 의 '80 °C' 자체도 덱 실물(60 degC)과 다른 우리 오기다. 헤더는 '6건'으로 세고 '아래는 우리가 덱에서 읽어 db에 넣었다가 논문 실물로 정정한 사례 전부다' 라고 단정한다.
- **고치는 법**: data.py 의 하드코딩 원장을 지우지 말고 케이스1·2·3 에 '철회 2026-08-03 — 덱이 아니라 우리 전사 오류' 상태 필드를 달아 취소선+사유로 렌더하고, 헤더 카운트를 '살아 있는 덱 오류 3건 / 철회 3건'으로 갈라 센다. 장기적으로 이 원장은 data.py 하드코딩이 아니라 JSON 으로 옮겨 _deck_corrections_2026_07_28 와 한 원본을 보게 한다.
- codex 필요: False

### [P0·wrong] d-li-10x-caption-contradicts-retraction
- **어디**: `db/properties/external_benchmarks_symposium_2026.json:64,71 → /benchmarks §재현 표적 li_argyrodite_interface_md 표`
- **근거**: D_Li 두 행의 신뢰도 칸이 '논문값. 덱 대비 10배 정정됨' 인데, 바로 그 위 같은 패널의 덱 정정 블록이 '없음 — 이전의 "덱 자릿수 10배 오기" 판정 철회(우리 전사 오류였음)' 라고 말한다. 덱 실물 0.4e-7 = 논문 4e-08 이라 10배 차이는 존재하지 않는다. 한 패널 안에서 두 줄이 정반대를 말한다.
- **고치는 법**: 두 행의 confidence 를 '논문값. 덱 실물과 일치(2026-08-03 재판독) — 종전 10배 정정 주장은 철회' 로 교체.
- codex 필요: False

### [P0·stale] bibliography-status-all-stale
- **어디**: `db/properties/external_benchmarks_symposium_2026.json:754-820 (lee_lab_bibliography) → /benchmarks §📚 이상욱 랩 서지`
- **근거**: _note 가 'PDF 실물 확보 전까지 서지 확인됨, 본문 미확인 상태다' 라고 하고 5개 항목 status 가 전부 '⏳ PDF 확보 대기' / '⏳ 프리프린트 — 최우선 입수' / '⏳' / '⏳ 낮은 우선순위' / '⏳ 신규 — 사용자에게 요청' 이다. 실제로는 5편 전부 litdb digest 가 있고 전문 정독이 끝났다 — litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md(56 KB, '본문+SI 전문 정독', 'Table S1 88행 전수 기계 재입력'), kim2026_li_argyrodite_sei_reactive_md.md(83 KB), kim2025_csp_metastable_edge_sharing_sse.md(195 KB), kim2025_li3ycl6_new_crystal_structure.md(77 KB), lee2024_multicomponent_argyrodite_mixed_oxidation_mtp.md(58 KB). 같은 페이지의 V1 이 그 Table S1 을, V3 이 lee2024 ESI Table S1 을 인용한다.
- **고치는 법**: status 를 '✅ digest 보유(litdb/papers/<slug>) · 본문+SI 정독 <날짜>' 로 바꾸고 _note 를 갱신. 각 행에 plink(slug) 를 붙여 /literature 모달로 열리게 한다.
- codex 필요: False

### [P1·stale] q5-closed-elsewhere-open-here
- **어디**: `db/properties/external_benchmarks_symposium_2026.json:735 (open_questions Q5) → /benchmarks §❓ 미해결 질문`
- **근거**: /benchmarks 는 Q5 를 'Adv. Energy Mater. revision 이 config-variance 오차막대를 추가했는가 / 닫는 방법: 논문 / 막고 있는 것: 우리 우위 주장 3-2의 유효 범위' 로 열린 채 싣는다. db/properties/tq_ledger_2026_08_26.json 의 Q_닫힌_것 에 같은 Q5(문서 'symposium + talk')가 '✅ 종결 — 그 AEM 논문은 [36] BH₄⁻ 회전동역학이지 Kim 2024 후속이 아니다 … 우리 §3-2 config-variance 카드 유효범위 걱정 해소' 로 등록돼 있고 이건 /ledger 에 뜬다. 같은 앱의 두 화면이 같은 Q 를 반대로 말한다. 미출판 서지 각주(:816)도 'Q5 가 여기 걸려 있다' 로 같이 낡았다.
- **고치는 법**: Q5 를 CLOSED 로 옮기고 근거를 tq_ledger_2026_08_26 로 지목. 표 자체를 '열린 것 / 닫힌 것' 두 묶음으로 나누고, 열린 것만 기본 노출하고 닫힌 것은 접는다. 표 머리에 /ledger 링크를 건다.
- codex 필요: False

### [P2·ia] q1-closed-still-in-open-table
- **어디**: `db/properties/external_benchmarks_symposium_2026.json:711 → /benchmarks §❓ 미해결 질문 Q1 행`
- **근거**: 질문 칸이 '[CLOSED 2026-08-03] 이상욱 랩 코팅 스크리닝 17,230 -> 최종 후보의 실체 = Li3Sc2(PO4)3 …' 로, 닫힌 사실을 질문 문자열 앞에 붙여 놓고 '미해결 질문' 표에 그대로 둔다. 상태가 데이터 필드가 아니라 문자열 접두어다.
- **고치는 법**: status 필드를 신설(open/closed/half)해 표를 분리 렌더. 문자열 접두어 해킹을 없앤다.
- codex 필요: False

### [P1·wrong] t1b-conclusion-stronger-than-ledger
- **어디**: `webapp/templates/benchmarks.html:419-422 → /benchmarks §T1b`
- **근거**: 화면은 '⛔ 따라서 b2o3 골격 붕괴는 softening 으로 설명되지 않는다 — 다른 원인이다' 라고 단정한다. 원장 db/properties/uma_force_benchmark.json 의 ★_T1b_verdict_2026_08_26.b2o3_판정 은 '설명하는 길이 사실상 닫힌다' 이고 바로 옆 ⛔_남은_한계 가 'Li₃PO₄ 는 황화물이 아니고 B 가 없다 / 융액이지 700 K 결정 골격이 아니다' 를 붙인다. 같은 JSON 의 ⛔_do_not 4건('LiPS 한 계, 251 프레임, 한 stride 의 값이다', 'OMat24 표와 같은 줄에 놓고 순위를 매기지 말 것', '에너지 편향 −37.43 을 오차로 인용하지 말 것', 'σ 절대값 인용 금지 규율은 그대로')과 🔴_정정_2026_08_26('처음 쟀다 는 틀렸다 — 2026-08-19 에 이미 쟀다'), ⛔_도구_중복(CLAUDE.md 코드 규율 위반 자백)은 화면에 한 글자도 안 나온다 — grep 으로 확인.
- **고치는 법**: 결론 문장을 원장 문구('설명하는 길이 사실상 닫힌다')로 낮추고 ⛔_남은_한계 2건을 그 옆에 붙인다. ⛔_do_not 4건을 T1b 절 상단 callout 으로 올린다(honesty_header 와 같은 대우).
- codex 필요: False

### [P1·broken] mdlite-swallows-zero
- **어디**: `webapp/app.py:96 (_mdlite: `str(escape(text or ""))`) · 사용처 webapp/templates/benchmarks.html:316-317`
- **근거**: `_mdlite(0)` 이 '' 을 돌려준다(직접 실행 확인). db/properties/committee_temperature_sweep.json 의 400 K 행은 n_above_fixed = 0 인데 렌더된 HTML 이 `<td ... style="color:#b91c1c">/200</td>` 다 — 실측 0 이 화면에서 사라져 결측처럼 보인다. 같은 필터가 q.value(:156,:221)·rank·frame_level_baseline 값에도 걸려 있어 0 이 들어오면 전부 같은 증상이 난다. 참고로 `|bold` 는 0 을 '0' 으로 제대로 찍는다.
- **고치는 법**: _mdlite 첫 줄을 `s = str(escape('' if text is None else text))` 로 바꿔 0/False 를 살린다. 회귀시험에 `_mdlite(0) == '0'` 음성시험 추가.
- codex 필요: False

### [P1·broken] target-value-python-repr-and-blank
- **어디**: `webapp/templates/benchmarks.html:154-161 (재현 표적 값 칸)`
- **근거**: 값 칸에 파이썬 repr 이 그대로 찍힌다: csp 항목의 'n-Li2SiS3 Ea (실험)' 이 `{'280-375 K': 0.278, '228-280 K': 0.347}`, 'R_total' 이 `{'228': 3475.7, '240': 1523.7, …}`, coating 의 '스크리닝 축' 이 `['electrochemical stability', 'mechanical stability', 'electronic stability', 'Li-ion conductivity']`, 그 밖에 `[11, 30]`·`[0.6, 0.8]`·`[0, 42]`. 그리고 electrode_microstructure_rate 의 '3C 방전용량 랭킹'·'through-plane tortuosity tau_z (근사)' 두 행은 value 가 null 이라 값 칸이 **완전히 빈칸**으로 나온다 — 없는 것을 빈칸으로 두면 결측인지 0 인지 구분이 안 된다.
- **고치는 법**: 값 렌더를 타입별로 갈라 dict 는 '창별 값' 소표, list 는 '[a, b] 범위' 또는 불릿, null 은 '값 없음 — 조건 칸 참조' 로 명시 표기.
- codex 필요: False

### [P1·stale] nd-survey-no-our-nd-result
- **어디**: `webapp/templates/nd_survey.html:37-55 (우리 db 접점)`
- **근거**: 접점 카드 3장이 /composition/modelc_nd_doped, cascade 로스터 순위(Nd₂O₃ 24위·NdF₃ 28위), 깔때기 방법론 문서뿐이다. 렌더된 /nd-survey 전문에 '어닐'·'anneal'·'모티프'·'Rietveld'·'2026-09' 가 0회(grep 확인). 2026-09-08 커밋 83c868a97 이 db/structures/ndo_lpscl16_rietveld_2026_09_07/anneal_2026_09_07/anneal_results.json 을 넣었고 webapp/data.py:4685 _nd_anneal_card() 가 그 결과(distributed < free_s < bo4, 두 셀 같은 방향)를 카드로 만들지만 dashboard_highlights() 에만 붙는다(data.py:4591). /composition/modelc_nd_doped 에도 안 뜬다(확인).
- **고치는 법**: _nd_anneal_card() 를 /nd-survey 상단 '우리 db 접점' 에 재사용해 붙인다(같은 함수 호출, 새 코드 아님). ⛔ UMA 순위 전용·DFT 재채점 전 인용금지 문구를 카드 그대로 승계.
- codex 필요: False

### [P1·ia] newest-content-buried-below-old-ledgers
- **어디**: `webapp/templates/benchmarks.html:37-116(2026-07-28 원장) vs 247-426(T1·T1b)`
- **근거**: 페이지 순서가 덱 정정 원장(2026-07-28) → 판정 정정 이력 7건 → 재현 표적 6건 → 논문 앵커 2건 → T1 위원회 → T1b(2026-08-26) → 방법론 참조 → 서지 → 미해결 질문 이다. 우리가 실제로 최근에 잰 유일한 실측(T1b, 2026-08-26)이 1,536줄 텍스트 중 1,304줄째에 있고, 그 앞은 전부 한 달 반 전 소환값 정리다. 화면 상단 배너도 '덱 분석 기준일 2026-07-28 · 마지막 갱신 2026-08-06' 이다.
- **고치는 법**: 절 순서를 뒤집는다 — ① 우리 실측(T1b → T1 위원회+온도 스윕) ② 우리가 뒤집은 판정(V1–V7, 접힘) ③ 외부 재현 표적·논문 앵커 ④ 덱 정정 원장(접힘) ⑤ 방법론 참조 ⑥ 서지·미해결 질문. 각 절 제목 옆에 그 절 원자료의 날짜 배지를 단다.
- codex 필요: False

### [P2·missing] section-dates-missing
- **어디**: `webapp/templates/benchmarks.html:249-368 (T1 위원회 절)`
- **근거**: 템플릿 22행 주석이 '이 파일이 언제 기준인지 화면에서 바로 보이게 — 2026-07-28 에 멈춘 걸 모르고 읽던 문제' 라며 날짜 배너를 달아 놨는데, 그건 external_benchmarks JSON 에만 적용된다. 같은 페이지가 렌더하는 다른 세 원자료 중 mlip_committee_baseline.json 의 date '2026-07-28' 은 화면에 안 나오고(출처 줄은 system·T_K·프레임·엔진만 찍는다), committee_temperature_sweep.json 은 date 필드 자체가 없다. 렌더 전문에서 '2026-08-26' 은 T1b 제목 1회뿐이다.
- **고치는 법**: 각 절 헤더에 그 절 JSON 의 date 를 배지로 찍고, 날짜가 없는 committee_temperature_sweep.json 은 '생성일 원장 부재' 로 명시(0 이나 빈칸 금지). 도구 재생성 시 date 를 넣도록 tools/ionic/committee_sweep_verdict.py 에 항목 추가.
- codex 필요: False

### [P2·broken] italic-asterisks-leak
- **어디**: `webapp/app.py:230-243 (_bold, `**` 만 처리) → /benchmarks 렌더 10곳`
- **근거**: 렌더된 텍스트에 별표가 그대로 남는다: '*Appl. Phys. Rev.*'(V5 ③), '*\"Lithium is a very common dopant of NiO …\"*'(V6 ③), '*\"direct contact\"*'(T3 재검증), '*\"many materials exhibited stable interfaces …\"*'(V1 ③), "*'실험이 검증했다'*"·"*'같은 자리, clamped 배제'*"·"*'단단하게 만들면 덴드라이트가 막힌다'*"·"*'few reports'*"(논문 앵커 판정). 2026-09-08 커밋 fc3624184 가 `**`·표 노출을 고쳤지만 홑별표 이탤릭은 그대로다.
- **고치는 법**: _bold/_mdlite 에 `*…*` → <i> 규칙 추가(여는 별표 뒤·닫는 별표 앞 공백 금지, `**` 먼저 소비, 코드 스팬 격리 후). 음성시험: `a * b * c` 가 이탤릭이 되지 않을 것.
- codex 필요: False

### [P2·broken] nd-material-truncated-midword
- **어디**: `webapp/templates/nd_survey.html:75`
- **근거**: `{{ (r.material or '')[:130]|mdlite }}` — 54행 중 42행이 130자를 넘어 잘린다(계산 확인). 화면 실물: '…계산상 최적 조성 Li₂', '…La site에 nominal하게 치환한 Nd(La', '…lithium lanthanum t', '…Pt blocking-electrode ce', '…Nd L3-/Ti K-edge EXAFS analys'. 말줄임표도 전체보기도 없다. 같은 칸에 원문 LaTeX 이 그대로 새기도 한다 — '(M=mathrm{Y^{3+},Gd^{3+},Sm^{3+},Nd^{3+},La^{3+}})'.
- **고치는 법**: 잘린 경우 '…' 를 붙이고 title 대신 <details> 나 행 확장으로 전문을 볼 수 있게 한다. 잘림이 `**` 쌍 중간에 떨어지면 별표가 노출되므로 절단은 mdlite 앞이 아니라 뒤(또는 안전 절단 헬퍼)로 옮긴다.
- codex 필요: False

### [P2·useless] nd-doi-placeholder-shown
- **어디**: `db/properties/nd_substitution_survey_index.json (papers id 016·017) → nd_survey.html:74`
- **근거**: 두 편의 doi 값이 문자열 '논문' 이다. 템플릿이 `{% if r.doi %} · {{ r.doi }}{% endif %}` 라 화면에 'Solid State Ionics · 논문' 으로 찍힌다 — 저널 이름 옆에 아무 뜻 없는 글자가 붙는다.
- **고치는 법**: 플레이스홀더 값을 데이터에서 null 로 바꾸거나, 템플릿에서 '10.' 으로 시작하지 않는 doi 는 'DOI 원장 부재' 로 표기.
- codex 필요: False

### [P2·missing] no-links-anywhere
- **어디**: `webapp/templates/benchmarks.html (href 전수: /literature 1종) · nd_survey.html (href 2종)`
- **근거**: grep 결과 /benchmarks 의 href 는 `/literature?open={{ slug }}` 하나뿐이다. 화면에 mono 텍스트로만 찍히는 것들: 소스 덱 digest(litdb/talks/lee2026_skku_mlip_materials_design.md, moon2026_cau_llm_agent_battery_automation.md — /talk/<slug> 라우트가 실재하고 둘 다 200), 논문 앵커 digest 3건(famprikis2019·miao2023·zhu2020 — 셋 다 litdb/papers 에 있고 plink 가능), 서지 DOI 5건, db/properties/*.json 10여 개(/api/property/<name> 200), kb/*.md, tools/*.py. /nd-survey 는 digest 필드가 있는 3편(032 zhou2026_high_entropy_lgps_multicationic · 053 ren2026_li2zrcl6_low_ion_potential_doping · 037 anderson2024_llzo_comprehensive_dopant_screening)에 링크가 없다 — 하필 우리 화학에 가장 가까운 세 편이다.
- **고치는 법**: 덱 출처를 /talk/<slug> 로, 논문 앵커 digest·nd-survey digest 를 기존 plink() 매크로로, db 경로를 /api/property/<name> 로 건다. 새 매크로 만들지 말고 benchmarks.html 의 plink 를 nd_survey.html 로 옮겨 공유.
- codex 필요: False

### [P2·missing] code-vocabulary-no-legend
- **어디**: `/benchmarks 전면 (T·Q·V·G·M 코드 60회 이상)`
- **근거**: 렌더 텍스트에서 T3 8회·T1 7회·T2 4회·T10 4회·T11 4회·G1 4회·T12 3회·V1–V7 각 1–2회·Q1–Q7·M6·J-1 이 나온다. /glossary 를 열어 확인하니 'T1'·'T1b'·'softening'·'위원회'·'재현 표적'·'덱' 어느 것도 없다. 뜻은 kb/CODES.md 와 /ledger('T=실행항목(전역) · Q=미해결질문(⚠문서별 로컬) · J=문헌대비축 · M=원고항목')에만 있는데 /benchmarks 에서 그리로 가는 링크가 없다.
- **고치는 법**: 페이지 상단에 한 줄 범례 + /ledger·/glossary 링크. 최소한 'Q 는 이 문서 로컬 번호다' 를 미해결 질문 표 머리에 명시(/ledger 는 이미 그 경고를 단다).
- codex 필요: False

### [P2·buried] json-content-not-rendered
- **어디**: `webapp/templates/benchmarks.html vs db/properties/external_benchmarks_symposium_2026.json`
- **근거**: reproduction_targets 의 키 12개가 렌더되지 않는다: ⛔_RETRACTED_2026_07_28(σ 3값 철회 + 'Fig 4b 실측 e = 1.8e-3 mS/cm → 덱 값은 약 18배 낮다' + still_retracted), method_dependence_red_flag('🔴 PBE 단독인데 SCAN 이 PBE 를 흔든다 … 3건 부호 반전'), contradicts('Jun 2022 Nat. Mater. Ceder 와 정면 충돌'), ⚠_cross_composition_warning, supports_our_no_csp_decision, lab_internal_inconsistency, mlip_accuracy_reported, our_experimental_anchor, experimental_anchor_cited_by_them, bruggeman_note, caveat(agent_model_fitting: '베이스라인(수동 피팅) 비교치가 덱에 없다 — 절대 성능 판단 불가'), source·slide(어느 덱·몇 번 슬라이드). 최상위도 sources(두 발표자 정보)·industry_context·description·_provenance_audit 가 안 나온다. mlip_committee_baseline.json 의 threshold_select·threshold_break(선별/중단 문턱 분리 — T1 논리의 핵심)도 안 나온다.
- **고치는 법**: 우선 세 가지만 올린다 — ① ⛔_RETRACTED 블록(철회는 화면에서 이름을 대야 한다) ② caveat/method_dependence_red_flag 처럼 '이 값을 믿지 말라'는 단서 ③ source·slide(두 발표자 덱이 한 목록에 섞여 있는데 화면에 구분이 없다). 나머지는 '원자료 전체 보기' 링크로 /api/property 에 넘긴다.
- codex 필요: True

### [P2·ia] changelog-unsorted
- **어디**: `db/properties/external_benchmarks_symposium_2026.json changelog → benchmarks.html:27-35`
- **근거**: 화면 '🕘 갱신 이력 4건' 이 2026-08-03 → 2026-08-04 → 2026-08-06 → 2026-08-05 순으로 나온다. 최신이 마지막도 아니고 정렬도 아니다.
- **고치는 법**: 템플릿에서 `|sort(attribute='date', reverse=true)` 로 최신 먼저.
- codex 필요: False

### [P2·broken] webapp-derived-stutter
- **어디**: `webapp/templates/benchmarks.html:336 + webapp/data.py:3027`
- **근거**: 화면 문장이 '⚠ 이 적합은 webapp 파생이다 — webapp 파생 (구판 JSON — 도구가 fit 을 지속하지 않던 판).' 로 같은 말이 두 번 나온다. 템플릿이 'webapp 파생이다' 를 쓰고 _derived 값도 'webapp 파생 (구판 JSON …)' 으로 시작한다. 2026-09-08 커밋 cdb86404c 에서 들어온 신규 문구다.
- **고치는 법**: _derived 값을 '구판 JSON — 도구가 fit 을 지속하지 않던 판' 으로 줄이거나 템플릿 쪽 접두어를 뺀다.
- codex 필요: False

### [P2·ia] nd-class-cards-not-filters
- **어디**: `webapp/templates/nd_survey.html:17-28 (계열 카드) · 60(검색 입력) · 91-98(ndfilt)`
- **근거**: 페이지의 논지가 '우리 화학에 가까운 것부터 읽으라' 인데, 계열 카드 8장은 순수 표시용이고 클릭해도 아무 일이 없다. 검색은 title·material·journal·doi 만 보고 system_class 라벨·purpose 필드는 대상이 아니다(data-q 구성 확인). 결과 개수 피드백도 없다 — 0건일 때만 '검색 결과 없음' 이 뜬다.
- **고치는 법**: 계열 카드를 토글 필터로 만들고(같은 ndfilt 확장), data-q 에 system_class 라벨을 넣고, 필터 결과 '54편 중 n편' 을 표시.
- codex 필요: False

### [P2·missing] nd-survey-no-date-no-provenance
- **어디**: `webapp/templates/nd_survey.html:4-8 (page-header)`
- **근거**: JSON 에 date '2026-07-28' 과 _provenance_audit(audited 2026-08-12, generator '(없음 — 손으로 작성)', confidence high, caveat '이 블록은 사후 추적 결과다') 가 있는데 화면에는 description 과 source_md 경로만 나온다. /benchmarks 는 날짜 배너를 다는데 여기는 없다 — 같은 앱에서 규칙이 갈린다.
- **고치는 법**: /benchmarks 와 같은 날짜 줄('색인 기준일 2026-07-28 · 출처 감사 2026-08-12 · 손으로 작성')을 헤더 아래에 단다.
- codex 필요: False

### [P2·buried] nd-reclassified-hover-only
- **어디**: `webapp/templates/nd_survey.html:71`
- **근거**: 오분류 교정 표시가 `<span title="{{ r._reclassified }}">⚠</span>` 로 hover 전용이다. 대상 4편(JSON:362,377,406,491, 전부 'Li 미포함 — perovskite 문자열만 보고 Li 계열로 오분류됐던 것 교정')이고 터치 기기에서는 이유를 볼 방법이 없다. 표 어디에도 ⚠ 범례가 없다.
- **고치는 법**: ⚠ 옆에 짧은 라벨('재분류')을 붙이고 표 머리 또는 classification_note 옆에 범례 한 줄. 전체 분류가 자동 규칙이라는 경고는 이미 있으니 그 옆에 붙이면 된다.
- codex 필요: False

### [P2·missing] no-first-timer-block
- **어디**: `webapp/templates/benchmarks.html:9-20 · webapp/templates/nd_survey.html:3-12`
- **근거**: 두 파일 어디에도 '처음 보는 사람용' 블록이 없다(grep). 같은 앱의 webapp/templates/cascade.html:35 과 compute.html:18 에는 '{# ══ 처음 보는 사람용 (2026-08-25) ══ }' 카드가 있고 기초/심화 배지(.lv-b/.lv-a)와 숫자 해설 카드까지 갖췄다. /benchmarks 는 대신 ⛔ 금지 5줄로 시작한다.
- **고치는 법**: cascade.html 의 패턴을 그대로 재사용해 두 페이지 상단에 '이 페이지가 무엇인가(기초)' 카드를 넣는다 — /benchmarks 는 '외부 값과 우리 값을 왜 갈라 두는가 + 이 화면의 네 덩어리', /nd-survey 는 '왜 54편 중 22편이 우리와 가장 먼가'. 기존 honesty_header 는 그 아래로 내리되 지우지 않는다.
- codex 필요: False

### [P2·broken] unit-filter-precedence
- **어디**: `webapp/templates/benchmarks.html:157, 222`
- **근거**: `{{ q.unit or '—'|mdlite }}` — Jinja 에서 필터가 or 보다 먼저 묶여 `q.unit or ('—'|mdlite)` 가 된다. 의도는 `(q.unit or '—')|mdlite` 다. 지금은 unit 문자열이 mdlite 를 안 지나므로 다른 칸과 렌더 규칙이 다르다(현재 데이터에는 unit 안에 마크다운이 없어 증상은 안 보인다).
- **고치는 법**: 괄호를 넣어 `(q.unit or '—')|mdlite` 로 교정.
- codex 필요: False

### [P2·useless] engine-empty-dash
- **어디**: `webapp/templates/benchmarks.html:130 (`{{ t.engine or '—' }}`)`
- **근거**: electrode_microstructure_rate 와 agent_model_fitting 은 engine 이 null 이라 접힌 제목이 'electrode_microstructure_rate · — · BEARS (arXiv, peer-review 미통과)' 처럼 의미 없는 대시로 나온다. 두 항목은 다른 발표자(moon2026_cau) 덱인데 그 사실도 화면에 없다.
- **고치는 법**: engine 이 없으면 그 조각을 통째로 빼고, 대신 source(어느 덱)를 찍는다.
- codex 필요: False
