# repo — kb/projects + kb/reports + kb/seminars + kb/papers + kb/templates

## 지금 무엇인가
프로젝트 24 · 보고 4 · 세미나 38(md 25 + pptx 13, 23 MB) · 원고 23(md 22 + pptx 1) · 템플릿 3 — 총 92개가 다섯 폴더에 평면으로 쌓여 있다. 2026-04~05 의 "디지털 트윈" 세대, 2026-06~08 의 cascade 세미나 세대, 2026-08~09 의 마감·보고량 규율 세대가 **분리 표시 없이 한 목록에 섞여** 있고, 최신 규율(마감 JSON · claim 결속 · 용어 개정)이 이 다섯 폴더에는 거의 도달하지 않았다. 실제로 본 것: 전 92개의 frontmatter/앞 13줄, 전문 정독 9개(estimand_card · seminar_script_5min_template · MUST_READ · restart_runbook · adhesion_charts_comparison · origin_adhesion_guide · computational_methods_draft · gabia_server_usage · adhesion_100seeds 대조용), 표적 정독 18개(1저자 요청 대장 · PRESENTATION · sdcp_phaseB · sdcp_preliminary · 20min_script · seminar_v1 배너 · 교수 지침 앞 76줄 · 원고 3종 · 세미나 대본 헤더 전수 등). **본문을 안 본 것 30여 개**(cascade build_v3 754줄 · dopant_screening_story 1274줄 · spec_codex 766줄 · round3 499줄 · audit_rev6 660줄 · paper2_FINAL_briefing 1604줄 · mechanism_anion_O 788줄 · decision_registry_design 476줄 · external_review_prompt 854줄 · sei_products 437줄 등)와 **pptx 13개 전부**(바이너리, 안 열었다).

## 처음 오는 사람
처음 온 사람(또는 기억을 잃은 다음 세션의 나)은 `kb/index.md` 로 들어와 폴더별 알파벳 목록을 본다. 제목만 있고 **날짜·지위·정본 표시가 없다.** projects/ 맨 위 셋이 하필 대문자 파일명이라 `HANDOFF_2026_08_31`(옛 인수인계) → `MULTI_CATEGORY_BATCH_PLAN_v22`(2026-05-25 superseded) → `MUST_READ_digital_twin_north_star`(🚨🚨🚨 · 2026-05-18 상태) 순서로 뜬다. 즉 **제일 크게 소리치는 문서가 제일 낡았다.** 그걸 시키는 대로 "첫 5분 안에" 읽으면 (a) 273 캠페인이 "~7/273 진행 중"이라고 배우고 (b) "Nd 서사 강화는 안티패턴"이라고 배운다 — 둘 다 지금 사실과 반대다(캠페인 종료 · 2026-09-03 교수 지침이 Nd/O 를 1차 과제로 지정). 세미나로 넘어가면 cascade 대본이 12개인데 둘이 동시에 "정본"을 주장하고 가장 최근 커밋된 것은 지위 표기가 없다. 원고 폴더에는 같은 SDCP 문단의 삽입안이 09-04·09-05·09-08 세 개인데 앞의 것이 뒤의 것을 가리키지 않는다. **막히는 지점은 하나로 요약된다 — "지금 살아 있는 게 무엇인지 알려 주는 문서가 이 다섯 폴더에 없다."**

## 건드리면 안 되는 것
- **kb/papers/lpscl_vs_lpscl16_seminar_v1.md:11-20 의 SUPERSEDED 표** — 이 repo 에서 배너를 가장 잘 쓴 실물이다(폐기값 / 이유 / 정본 / 단일 출처를 한 표에). 지우지 말고 **다른 문서에 복제할 서식의 원본**으로 삼아라. 배너가 딸린 pptx 아카이브도 «전달이 끝난 발표의 아카이브이므로 고치지 않는다» 는 원칙 그대로 둔다.
- **kb/projects/MULTI_CATEGORY_BATCH_PLAN_v22.md:19-30 의 SUPERSEDED 블록** — 22-compound 계획이 273 으로 커진 설계 진화 이력이다. 문서 자신이 «아래 22-compound 내용은 **설계 진화 history로 보존**» 이라고 적어 두었다. 내용을 지우면 왜 273 이 되었는지를 잃는다.
- **kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md** — 이 다섯 폴더에서 가장 값비싼 문서다(교수 육성 지침 · D-1~D-3 · '왜 하필 Nd냐' 8회 반복 · 허용된 두 경로). 인용부호 안의 전사 원문과 `[ ]` 복원 표기, «⚠ STT 전사라 오인식이 많다» 경고를 **한 글자도 고치지 마라**. 옮긴다면 kb/projects 로 올려 눈에 띄게 하되 파일 내용은 그대로.
- **kb/projects/restart_runbook_2026_09_07.md 전문** — 실측(`ps -eo pid,lstart,args` · `readlink /proc/…/cwd` · `rc=143`)에 근거한 절차서이고 «⚠ 여기 처음엔 \"LEANSCF 오류면\" 이라고 적었는데 **근거 없는 추측이었다**» 같은 자기정정까지 남아 있다. 특히 §2 의 «⛔ `/root/work/Yonghoon-DEM-DFT` 는 b2o3run 브랜치 작업 폴더 — 손대지 말 것» 과 §3-1 의 «⛔ 다시 걸 때는 `for s in 3 4`» 는 실물 사고 방지선이다.
- **kb/templates/seminar_script_5min_template.md 와 estimand_card.md 의 «⛔ 이 도구/템플릿이 못 하는 것» 절** — CLAUDE.md 코드 규율이 요구하는 한계 명시의 모범이다. 위에서 지적한 것은 카드 §머리말의 철회 문장 하나와 용어뿐이고, 구조(§1 원하는 것 → §2 재는 식 → §3 잘 정의되는가 → §4 결과 보기 전 게이트 → §5 허용/금지 → §6 규약 대조)는 손대지 마라.
- **kb/reports/paper_first_author_requests_2026_08.md 의 취소선·철회 관행** — L4 «답이 바뀌면 원래 답을 지우지 말고 취소선·철회 표시로 남긴다», §1-1 의 «⛔⛔ 2026-08-11 재판정 — 아래 답의 앞 문장은 실측으로 반증됐다 ... ~~500/700/900 K 는 셋 다 표준 200 ps 로 된다~~». 갱신하되 **누적 원칙을 깨지 마라** — 이 문서는 1저자와의 왕복 이력 자체가 근거다.
- **kb/papers/draft_v1.md:7-13 의 인용 금지 배너** — «본문 다른 절의 수치도 정본 대조 전까지 인용 금지» 까지 적어 둔, 결속이 제대로 된 유일한 원고 초안이다. 다른 원고 문서를 이 수준으로 올리는 게 목표지 이걸 지우는 게 아니다.
- **kb/papers/final_report_v2.md:286-287 의 「Wad paper vs Wad 100s」 나란한 표** — 5 시드 판과 100 시드 판을 같은 표에 놓아 독자가 차이를 보게 한다. adhesion 정리를 할 때 이 표가 대조의 기준점이다.
- **pptx·js 를 옮기더라도 파일 자체는 삭제 금지** — codex_closed_2026_08_11/ 안의 덱과 대본, draft27_claude 계열까지 전부 '전달·리뷰가 끝난 산출물'이다. 이동·접기는 하되 지우지 마라(SCHEMA: 불변 원본 수정 금지 정신).

## 발견

### [P0·wrong] lpscl-20min-script-dead-gap
- **어디**: `kb/papers/lpscl_vs_lpscl16_20min_script.md:3,33,36,58,79`
- **근거**: 헤더가 스스로 보증한다 — L3 «숫자는 전부 repo(2026-06 paper-grade)와 일치.» 그런데 L33 «두 조성의 밴드갭은 **1.76과 1.82 eV로 차이가 0.06 eV**», L58 «밴드갭 1.76 대 1.82, 거의 동일». 같은 캠페인의 마스터 문서 kb/papers/lpscl_vs_lpscl16_seminar_v1.md:16 은 이 값을 «밴드갭 1.76 / 1.82 eV | **폐기** — DOS-threshold 판독(~0.3 eV 과소 아티팩트) | fixed-occ nscf 고유값 **comp1 2.066 / modelc 2.099**» 로 못박아 두었다. 더 나쁜 것은 L79 «**Figure X(DOS) caption "2.28 eV"는 옛 값** — paper-grade는 1.76 eV. M1/Summary와 맞추려면 figure caption을 **1.76 eV**로 수정.» — 폐기된 값으로 그림을 고치라고 **지시**한다. 같은 문서 L36 은 MD 절대 σ «상온 외삽하면 약 3.4와 14 mS/cm»(CLAUDE.md 절대값 인용 금지)와 «이 값은 실험과 정확히 일치합니다(0.25/0.22 eV)»(마스터 배너: Schlem2020 귀속 철회 2026-07-28 → 실험범위 0.29–0.46) 를 함께 싣는다. 이 파일에는 SUPERSEDED 배너가 **한 줄도 없다**(grep 결과 0건).
- **고치는 법**: 마스터(seminar_v1.md:11–20)의 SUPERSEDED 표를 이 파일 상단에 그대로 복제하고, L79 의 '캡션을 1.76 으로 수정' 지시는 삭제한다(정본 2.066/2.099). L36 의 σ 절대값 문장은 '절대값은 인용하지 않는다'로 교체. 그리고 이 파일과 seminar_script_outline.md 를 kb/seminars/ 로 옮긴다(같은 발표의 세 조각이 두 폴더에 흩어져 있는 게 배너 누락의 구조적 원인이다).
- codex 필요: False

### [P0·wrong] presentation-md-sigma-absolute
- **어디**: `kb/projects/PRESENTATION_digital_twin_overview.md:183,364,387,434`
- **근거**: 발표용(«비전공자/지도교수/투자자에게 쉽게 설명») 문서인데 MD 절대 전도도를 네 번 싣는다. L183 «5개 winner σ_Li 측정: 최고 **3.78 mS/cm** (LPSCl 수준 유지)», L364 «Label: "σ_300K = 3.78 mS/cm (LPSCl-level)"» (슬라이드 라벨 지시), L387 «"Nd₂O₃ winner: σ_300K = 3.78 mS/cm"», L434 §10 키 메시지 «Demonstrated on Nd₂O₃ doping (σ=3.78 mS/cm winner)». CLAUDE.md: «σ는 Nernst–Einstein(Haven=1) — **절대값 인용 금지**, 비율도 멀티시드 판정만». 같은 §10 은 «validated with **R=0.989 against experimental adhesion data**» 도 싣는데 그 R 은 20 시드 중 5 시드를 고른 표에서 나온 값이다(아래 adhesion 항목). 같은 문서 L429 «paper 언제 나오나? 12 oxide batch 후 4-6주» 는 2026-05 계획이고 실제는 91종×3=273 캠페인이었다.
- **고치는 법**: σ 절대값 4곳을 전부 지우고 '비율·Ea 만 인용'으로 대치. §10 키 메시지 문단은 통째로 재작성하거나 '2026-05 발표 아카이브 — 재사용 금지' 배너를 달아 동결한다. 12-oxide 문구는 273 캠페인 결과로 교체하거나 함께 동결.
- codex 필요: False

### [P0·stale] must-read-north-star-stale
- **어디**: `kb/projects/MUST_READ_digital_twin_north_star.md:12,61,89,136,164`
- **근거**: L8 «**새 session / 압축 후 첫 5분 안에 무조건 읽기**», L12 «마지막 갱신: 2026-05-18». 실제로 지금 틀린 것 넷: ① L61 «❌ *"Nd2O3 narrative 강화하자"* — Nd는 1개 datapoint» — 그런데 kb/seminars/group_meeting_2026_09_03_nd_professor_directives.md 는 «이 문서의 지위: 앞으로 Nd 논문·연구세미나·원고를 쓸 때의 **1차 지침**» 이고 커밋 83c868a97(2026-09-08) 이 Nd2O3-LPSCl1.6 어닐 6셀을 회수했다. ② L136 «gabia 진행 중 (2026-05-25 기준 ~7/273)» — 2026-08-13 대본들은 «273개 슬롯 가운데 270개가 완료» 라고 쓴다. ③ L89 «`run_md_sigma.py` | σ_Li Arrhenius MD | ✅ verified (paper-grade σ_300K)» — 300 K σ 는 커밋 cc7096eda 에서 보고량에서 «300 K σ·Deng 0.90·2온도 외삽 삭제» 로 빠졌다. ④ L164 «`CODE_INVENTORY.md` — 검증된 script 목록» · L113 «필독/adhesion/v30u_ensemble» — 둘 다 실물 없음(ls 확인).
- **고치는 법**: 이 문서를 '2026-05 아카이브'로 강등하고, 그 자리에 **현재 살아 있는 것만 적은 새 north star** 를 만든다(내용: 활성 캠페인 4개 · 활성 마감 JSON 목록 · 활성 지침 카드 = 교수 지침 · 금지 서술 링크). 최소한 L61 의 Nd 안티패턴 줄과 L136 진행률, L89 σ_300K, L164 없는 경로는 즉시 정정.
- codex 필요: False

### [P1·stale] sdcp-phaseB-vs-closure
- **어디**: `kb/projects/sdcp_phaseB_direction_2026_08_06.md:3,12,16`
- **근거**: L3 «Phase-B 는 **E_ads(doped) · E_ads(neutral) 둘 다 낸다**(논문 수치)», L12 «그 가설을 판정하는 양이 **Δ 하나**다», L16 «| **freeze_frac 1.0** | **−0.258** | **−0.0879** | **−0.170 eV** |». db/properties/sdcp_doped_closed_2026_08_28.json 은 active(1저자 ratify 2026-08-28e)이고 금지 서술에 «doped E_ads 수치 일체 (−0.32 eV 등 과거 값 포함)» · «'doped 가 중성보다 강하게/약하게 붙는다' — **비교 자체가 미정의**» 가 글자 그대로 있다. 즉 이 문서의 논지 전체(Δ)가 지금은 금지 서술인데, 문서 안에 마감 JSON 을 가리키는 문자열이 **0건**이다(grep: sdcp_doped_closed / 2026-08-28 / 마감 전부 미검출).
- **고치는 법**: 상단에 «⛔ 2026-08-28 범위 마감 — db/properties/sdcp_doped_closed_2026_08_28.json 이 이 문서의 Δ 판정을 금지 서술로 바꿨다. 재개 조건은 그 파일 §재개» 배너를 달고, Δ 표에 철회 표시. 값은 지우지 않는다(SCHEMA Update Policy).
- codex 필요: False

### [P1·wrong] sdcp-preliminary-direction-claim
- **어디**: `kb/reports/sdcp_preliminary_final_2026_08_03.md:149`
- **근거**: L149 «doped 는 화학흡착(−4 ~ −5 eV), neutral 은 O-배위(−2 ~ −2.7 eV) — **방향성은 확고**». sdcp_doped_closed_2026_08_28.json 금지 서술: «'doped 가 중성보다 강하게/약하게 붙는다' — 비교 자체가 미정의» · «doped E_ads 수치 일체». 이 보고서는 L150·L253 에서 chelation_r90 −5.196 eV 한 건만 «주기이미지 샌드위치로 철회» 로 묶어 두었고, 나머지 −4~−5 / −2~−2.7 범위와 '방향성은 확고' 는 결속 없이 살아 있다. 문서 어디에도 08-28 마감 링크가 없다.
- **고치는 법**: §6 상단에 doped 마감 배너 + '방향성' 문장에 철회 표시. 참고로 같은 문서 L87(0.43/1.27 eV)·L125–127(DPE 14.17 / LCA −6.76)은 **철회가 아니라** 2026-09-08 1저자 결정으로 원고에서만 빠진 것이므로(kb/papers/self_doping_dft_paragraph_2026_09_08.md:22–24 «⛔ 뺀 것 ②/③») 그 구분을 명시해 적는다 — 둘을 섞으면 다음 세션이 멀쩡한 기체상 값까지 버린다.
- codex 필요: False

### [P1·stale] first-author-ledger-stale
- **어디**: `kb/reports/paper_first_author_requests_2026_08.md:10,25`
- **근거**: L10 «## 📋 요청 대장 (**2026-08-25 갱신**)», 마지막 절은 «## 16. b2o3 는 왜 ... (2026-08-25)» 로 끝난다(grep '^## ' 전수). 그 사이에 2026-09-07 LPSOCl 3×3×1 닫힘 조건이 만들어지고 2026-09-08 에 비준됐는데(db/properties/lpsocl_box331_closure_conditions_2026_09_07.json 지위 «✅ **active — 1저자 비준 완료 (2026-09-08)**»), 대장의 요청 3 «LPSOCl MSD plot | 🟡 도구 완성 · 셀 확대판(243 Li) 확보 — **어느 판을 쓸지 판정 대기**» 는 그대로다 — 그 판정이 바로 09-07/08 에 났다. 요청 1·2 도 같은 MD 축 위에 있다. 덤으로 L25 가 «**§13** · §14» 를 가리키는데 §14 는 존재하지 않는다(§13 다음이 §15). 문서 자신의 규칙은 L4 «이 문서는 **누적**한다».
- **고치는 법**: §17 로 'LPSOCl 3×3×1 마감 비준(2026-09-08)' 절을 잇고 대장 1·2·3 행의 상태를 마감 계약 기준으로 갱신. §14 참조는 실제 절 번호로 고치거나 '§14 결번' 을 명시.
- codex 필요: False

### [P1·wrong] estimand-card-retracted-line
- **어디**: `kb/templates/estimand_card.md:8`
- **근거**: 카드 L8 «> 일곱 번은 안 돌려도 됐다.» CLAUDE.md 계산 규율 절이 이 문장을 명시적으로 철회했다 — «(⚠ 회신 N: "일곱 번은 안 돌려도 됐다" 는 **철회** — 카드 블라인드 재생 시 확실히 잡는 것은 #7–8 정도다. 여덟 실패의 원인은 하나가 아니라 층위다.)». 템플릿은 새 계산마다 복사되는 원본이라 철회 문장이 계속 재생산된다.
- **고치는 법**: L8 을 회신 N 문구로 교체 — «블라인드 재생 시 이 카드가 확실히 잡는 것은 #7–8 정도다. 여덟 실패의 원인은 하나가 아니라 층위다.» 원문은 취소선으로 남겨 이력 보존.
- codex 필요: False

### [P2·stale] estimand-card-terminology
- **어디**: `kb/templates/estimand_card.md:1,42-44,47-49,93`
- **근거**: L1 «# estimand 카드», L42–44 «scalar estimand 는 정의되지 않는다 ... 전부 정당한 estimand 가 될 수 있다», L47 «estimand core». CLAUDE.md 용어 규율(2026-09-01, 1저자 결정): «사람이 읽는 표면 — 원고·SI·슬라이드·발표·웹앱 화면·**리뷰 프롬프트**·1저자 설명 — 에는 필드에서 쓰는 말만 쓴다. estimand → **보고량**». 그리고 이 카드 L93 이 «**계산 전에** §1–3 을 리뷰에 보낸다» 라고 스스로 리뷰 프롬프트임을 선언한다. 파일명·기계 필드는 그대로 두는 게 규율이지만 본문 산문은 개서 대상이다.
- **고치는 법**: 제목과 §3·§4 산문의 estimand 를 '보고량'으로, canary 계열 표현이 있으면 '대조 잡'으로 교체. 파일명 estimand_card.md 와 decisions.json 의 kind:"estimand" 는 건드리지 않는다.
- codex 필요: False

### [P1·wrong] adhesion-seed-selected-as-paper
- **어디**: `kb/papers/origin_adhesion_guide.md:5-11 · kb/papers/adhesion_charts_comparison.md:18-29`
- **근거**: adhesion_charts_comparison.md 는 두 표를 나란히 놓는다 — «## Chart 1: 20 Seeds Full Average (**Honest**)» (comp3 2.375 / comp4 1.642 / comp1 1.153 / comp2B 1.538, L15 «C4>C5:NO(reversed!) C1>C2:NO(reversed!)») 와 «## Chart 2: Selected 5 Seeds (**Paper**)» (comp3 2.103 / comp4 1.970 / comp1 1.277 / comp2B 1.183, L28 «R = 0.9999. All ratio errors < 0.7%», L29 «ALL MATCH!»). origin_adhesion_guide.md 는 Chart 2 만 아무 단서 없이 싣는다. 한편 kb/results/adhesion_100seeds_analysis.md 는 100 시드 짝지은 비교에서 comp3-comp4 «NO» · comp3-comp5 «NO» · comp4-comp5 «NO» · comp1-comp2B «**-0.464 ... YES**»(역전이 유의) 로 Chart 2 의 4개 순위 일치를 전부 무력화한다. kb/papers 의 두 문서 어디에도 100 시드로 가는 링크가 없다. **원장 부재**: db/properties/citation_hazards.json 25건 중 W_ad/adhesion 항목 0건, canonical_registry.json 에도 adhesion 키 없음(grep 0건) — 즉 이 값들은 정본 등록도 위험 등록도 안 돼 있다.
- **고치는 법**: 두 파일 상단에 «⚠ 이 표는 20 시드 중 5 시드를 고른 판이다. 100 시드 통계(kb/results/adhesion_100seeds_analysis.md)에서 Li5.4 내부 순위는 유의하지 않고 comp1↔comp2B 는 유의하게 역전된다» 배너. 그리고 W_ad 를 canonical_registry.json 에 등록하거나 citation_hazards.json 에 CONDITIONAL 로 올려 결속을 만든다 — 어느 세대를 정본으로 삼을지는 1저자 결정.
- codex 필요: True

### [P1·duplicate] manuscript-inserts-no-chain
- **어디**: `kb/papers/dft_sentences_for_manuscript_v6_2026_09_04.md · kb/papers/figure2e_dropin_v7_2026_09_05.md:19-23 · kb/papers/self_doping_dft_paragraph_2026_09_08.md`
- **근거**: figure2e_dropin_v7 이 명시한다 — «대체하는 것: `kb/papers/dft_sentences_for_manuscript_v6_2026_09_04.md` §1·§4 ... 왜 대체하나: 그 둘의 **잡 설계 서술이 낡았다** — "twelve poses per species, four pre-registered and eight drawn from a stratified prospective holdout" 라고 적혀 있는데, 실제로 나간 것은 **C-12 v36 · 19잡**이고 구성이 다르다». 그런데 v6 쪽 frontmatter 는 여전히 «status: 1저자 확인 대기» 이고 v7 을 가리키는 문자열이 0건이다(grep: figure2e_dropin 미검출). 09-08 의 self_doping_dft_paragraph 는 v6·v7 어느 쪽도 언급하지 않는다(grep: figure2e/dft_sentences 0건). 같은 원고의 같은 자리를 두고 세 문서가 서로를 모른다.
- **고치는 법**: v6 상단에 «⛔ §1·§4 는 figure2e_dropin_v7_2026_09_05.md 가 대체» 배너 + status 를 '부분 대체됨'으로. 세 문서 중 무엇이 어느 절을 담당하는지 한 줄 지도를 09-08 문서 상단에 만든다(원고 §Results 자가도핑 문단 = 09-08 / Figure 2e 문단·캡션·Methods = 09-05 / 나머지 = 09-04).
- codex 필요: False

### [P1·duplicate] seminar-two-canonicals
- **어디**: `kb/seminars/cascade_speaker_script_rev3_FINAL_ko.md:1 · cascade_speaker_script_rev4_ko.md:6 · cascade_speaker_script_audit_rev6_ko.md:1`
- **근거**: cascade 대본이 12개다(FINAL·rev2·rev3_FINAL·rev4·round3·audit_rev6·release_v2·final_script_ko·2026_08_script·deck_3to7·deck_8to12·dopant_screening_story). 둘이 동시에 정본을 주장한다 — rev3_FINAL L1 «# 발표 대본 — Research Seminar 2026-08 · Cascade **rev3 (정본)**» (SUPERSEDED 배너 없음, grep 0건) 와 rev4 frontmatter «status: 확정 — 사용자 작성본이 정본. 덱 30장과 1:1 대응 확인». 그런데 rev4 는 «본문: 19장» 인데 status 는 «덱 30장» 이라 자체 모순도 있다. 커밋 기록상 rev3→rev4 는 같은 날(2026-08-13, 83f0de117 «adopt the user's rev3 script as canonical, drop my draft» → 1911cd86f «seminar rev4: deck + script in»). 가장 나중까지 손댄 audit_rev6(커밋 40ffb7b97, 2026-09-01)은 **frontmatter 도 지위 표기도 없다**.
- **고치는 법**: rev4 를 정본으로 확정하고 rev3_FINAL 제목의 '(정본)' 을 '(rev4 로 대체됨)' 으로, 나머지 10개에 대체 배너 한 줄씩. 그리고 kb/seminars/ARCHIVE_2026_08_cascade/ 하위로 대체본을 내려 index 에서 한 덩어리로 접는다.
- codex 필요: False

### [P1·ia] kb-index-flat-no-recency
- **어디**: `kb/index.md:290-293,344-345,373-374`
- **근거**: index 는 폴더별 알파벳 나열이고 제목만 있다 — 날짜도 status 도 없다. projects/ 첫 세 줄이 «HANDOFF_2026_08_31_session.md», «MULTI_CATEGORY_BATCH_PLAN_v22.md»(본문 L19 «⚠️ SUPERSEDED (2026-05-25)»), «MUST_READ_digital_twin_north_star.md»(L12 «마지막 갱신: 2026-05-18») 다 — 대문자 파일명 때문에 **제일 낡은 셋이 맨 위에 온다**. 반대로 2026-09-07 restart_runbook 은 306행, 2026-09-03 handoff 는 302행에 파묻힌다. 문서 3종(HANDOFF_2026_08_31 · handoff_2026_09_03 · restart_runbook_2026_09_07)은 세션 상태라는 같은 종류인데 이름 규칙이 셋 다 다르고 서로를 가리키는 링크가 없다(grep: 09_03 문서만 L157 «앞 세션의 ... 판단을 정정한다» 한 줄).
- **고치는 법**: kb_wiki.py index 를 고쳐 각 줄에 `updated` 와 `status` 를 붙이고 **updated 역순** 정렬 + status 가 '대체됨/아카이브'인 것은 접이식 <details> 로 내린다(frontmatter 없는 레거시는 git 마지막 커밋일로 대체). 세션 상태 3종은 이름을 `session_state_YYYY_MM_DD.md` 로 통일하고 최신본이 이전 것을 한 줄로 가리키게 한다.
- codex 필요: False

### [P1·missing] kb-outside-claim-binding
- **어디**: `db/properties/citation_hazards.json (hazards 25건) · kb/papers/ 전 22개`
- **근거**: citation_hazards.json 의 25개 hazard 를 파일 접두어로 세면 db/ 23 · tools/ 1 · docs/ 1 — **kb/ 는 0건**이다. how_to_use 도 «원고나 그림에 **db 값**을 넣기 전에 이 표를 먼저 본다» 로 db 만 대상이다. 그런데 원고 문장이 실제로 쓰이는 곳은 kb/papers/ 이고, 위에서 확인했듯 폐기된 밴드갭 1.76/1.82(20min_script)·금지된 σ 3.78 mS/cm(PRESENTATION)·마감 금지 서술(sdcp_preliminary L149)이 전부 이름 없이 살아 있다. CLAUDE.md 는 «철회·비인용 값은 화면에서 이름을 대야 한다(claim 결속)» 인데 그 결속망이 kb 산문에는 닿지 않는다.
- **고치는 법**: hazard 항목에 file 대신 claim ID 를 쓰고 kb/ 문서도 대상에 넣는다(이미 커밋 12e6d0c9b 에서 웹앱 쪽은 claim ID 구조로 이주했다 — 같은 그래프에 kb 를 붙인다). 최소 1차 조치로 tools 쪽에 `kb 문서에서 hazard 값 문자열을 찾아 배너 유무를 검사`하는 lint 규칙 하나 추가.
- codex 필요: True

### [P2·useless] seminars-binary-dump
- **어디**: `kb/seminars/ (pptx 13개 · 23 MB · js 2개 124 KB) · kb/papers/lpscl_vs_lpscl16_seminar_v1.pptx`
- **근거**: `du -sh kb/seminars` = 23M. 그 안에 pptx 13개(cascade.pptx · _17d9a373_final · _codex_revised · _final · _release · _rev2 · _rev3 · _rev4 · draft27_claude · 2026_08_final · codex_closed/_closed 등)와 생성기 js 2개(generate_seminar_deck_2026_08.js 84 KB · generate_draft27_claude.js 40 KB)가 섞여 있다. kb/index.md 는 .md 만 세므로 «## seminars/ (25)» 로 표시되고 **이 13+2 는 목록에 아예 안 나온다**(kb/reports/gabia_server_usage_2026_07.txt 도 같은 이유로 «reports/ (3)» 에 안 나온다 — 실제 파일은 4개). 즉 화면에는 안 보이면서 폴더 용량의 90% 를 먹고, 어느 pptx 가 정본인지 아무 표시가 없다.
- **고치는 법**: pptx 는 정본 1개(rev4)만 kb/seminars 에 남기고 나머지는 kb/seminars/ARCHIVE_2026_08_cascade/ 로. 생성기 js 2개는 tools/seminar/ 로 이동(코드 규율상 kb 는 해석 레이어다). kb_wiki.py index 가 비-md 자산도 한 줄 요약으로 세게 한다(«pptx 13 · js 2 — ARCHIVE» 수준).
- codex 필요: False

### [P2·ia] papers-holds-seminars
- **어디**: `kb/papers/lpscl_vs_lpscl16_20min_script.md · lpscl_vs_lpscl16_seminar_script_outline.md · lpscl_vs_lpscl16_seminar_v1.md · lpscl_vs_lpscl16_seminar_v1.pptx`
- **근거**: kb/seminars/ 가 따로 있는데 kb/papers/ 안에 세미나 대본 3개와 pptx 1개가 있다 — 제목도 «세미나», «20분 학회 발표 대본», «Slide Master v1» 로 스스로 세미나라고 말한다. 폴더가 갈린 결과 SUPERSEDED 배너가 마스터(seminar_v1.md)에만 붙고 나머지 둘에는 안 붙었다(위 P0 항목의 직접 원인). kb/SCHEMA.md 는 디렉터리↔타입을 «`papers` ... `seminars`» 로 구분해 두었다.
- **고치는 법**: 네 파일을 kb/seminars/lpscl_vs_lpscl16_2026_06/ 로 옮기고 옮기면서 배너를 한 번에 통일. kb/papers 는 '원고에 들어갈 문장·표·레퍼런스'만 남긴다.
- codex 필요: False

### [P2·missing] no-closure-card-template
- **어디**: `kb/templates/ (파일 3개: estimand_card.md · manuscript_prompts.md · seminar_script_5min_template.md)`
- **근거**: CLAUDE.md 마감 규율은 «캠페인을 닫을 때 **`db/properties/<계>_closed_<날짜>.json`** 를 남긴다: 확정값 · **허용 서술(이대로만)** · **금지 서술** · **재개 조건(이것들만)**» 이고 «순서가 핵심 — 조건을 먼저 정하고, 그게 채워졌으므로 닫는다» 인데, 그 카드의 템플릿이 없다. grep -rl 'campaign_closure_prereg|campaign_closed' kb/ db/governance/ tools/ = **0건**(스키마 문자열이 실물 JSON 안에만 있다). 실제로 스키마가 이미 갈렸다 — sdcp_neutral/doped 는 `campaign_closed/v1`, lpsocl_box331 은 `campaign_closure_prereg/v1`. CLAUDE.md 는 템플릿 대신 «선례: db/properties/sdcp_neutral_closed_2026_08_28.json» 하나를 가리킬 뿐이다.
- **고치는 법**: kb/templates/closure_card.md 를 만든다(보고량 카드와 짝). 필수 절: 닫는 범위 · **닫힘 조건(결과 보기 전)** · 판정 규칙 · 허용 서술 · 금지 서술 · 재개 조건 · 시각 증거(커밋 해시) · status_history. 두 스키마(prereg vs closed)의 차이를 그 문서에서 정의해 이후 갈리지 않게 한다.
- codex 필요: False

### [P2·broken] broken-paths-15
- **어디**: `kb/papers/si_figures_plan.md(6) · kb/projects/sdcp_linio2_binding.md(2) · kb/projects/sdcp_master_v2_2026_07_11.md(2) · kb/reports/paper_first_author_requests_2026_08.md(2) · kb/papers/choi2025_adoption_guide.md(1) · kb/seminars/cascade_speaker_script_round3_ko.md(1) · kb/seminars/seminar_redirect_2026_08_11.md(1) · kb/projects/MUST_READ_digital_twin_north_star.md:164,113`
- **근거**: `python3 tools/kb_wiki.py lint --legacy` 의 «레거시 깨진 경로 20건» 중 **15건이 이 다섯 폴더**다 — 예: si_figures_plan.md 가 tools/plot_wad_stats.py · tools/plot_ncm_convergence.py · tools/plot_method_comparison.py · tools/analyze_halogen_bonds.py · tools/li_layer_partition.py · tools/br_swap_test.py 여섯 개를 가리키는데 전부 없다. paper_first_author_requests 는 docs/figures/msd_hosts.png · db/properties/msd_window_sensitivity.csv. 추가로 lint 가 못 잡는 두 건을 직접 확인했다 — MUST_READ L164 `CODE_INVENTORY.md` 와 L113 `필독/adhesion/v30u_ensemble/` 은 실물 없음(ls 확인). lint 는 frontmatter 없는 문서를 깊게 안 보므로(이 다섯 폴더 92개 중 frontmatter 17개뿐) 실제 깨짐은 이보다 많을 수 있다.
- **고치는 법**: 실물로 이름만 바뀐 것은 repoint(커밋 40ffb7b97 이 이미 8건을 그렇게 처리했다). 정말 없는 것은 그 줄에 `<!-- lint-skip-path -->` + '미생성/폐기' 표기. 그리고 이 다섯 폴더의 레거시 문서에 frontmatter 를 소급해 넣어 lint 깊이검사 대상으로 올린다(적어도 projects·reports·templates 는 31개뿐이라 비용이 작다).
- codex 필요: False

### [P2·stale] gabia-usage-report-orphan
- **어디**: `kb/reports/gabia_server_usage_2026_07.txt:11`
- **근거**: L11 «"전고체 배터리용 황화물 고체전해질(Argyrodite Li₆PS₅Cl 계)의 첨가제 **디지털 트윈** 스크리닝 플랫폼 구축"». 이 파일의 커밋일은 2026-08-03 으로, 용어 전환(2026-07-28, kb/projects/MUST_READ...:3–6 «대외 자료에서 "디지털 트윈" → "AI 계산 기반 스크리닝"») **이후**에 대외 문서로 나갔다. 본문이 «저번 달이 ... 요번달은» 이라 월간 제출물인데 repo 에는 2026-07 한 건뿐이다(find -iname '*usage*' · grep '서 버 용 도' 전 repo 각각 1건). 08·09 분이 어디 있는지는 **확인하지 못했다**(repo 밖일 수 있다). 또 .txt 라 kb/index.md 의 «## reports/ (3)» 에 안 나온다 — 실제 파일은 4개.
- **고치는 법**: 다음 달 제출분부터 용어를 'AI 계산 기반 스크리닝'으로 고정하고, 이 파일은 kb/reports/server_usage/ 하위로 옮겨 월별로 쌓는다(.md 로 바꾸면 index 에도 뜬다). 08·09 분이 repo 밖이면 그 사실을 README 한 줄로 남긴다.
- codex 필요: False

### [P2·stale] cascade-fixes-status-frozen
- **어디**: `kb/projects/cascade_pipeline_fixes_2026_08_19.md:7`
- **근거**: frontmatter L7 «status: 진행 — 진단 확정, 수정 미착수 (**내일 codex 교차리뷰 예정**)». lint 가 «status ... 인 채 20일 — 닫혔으면 status 갱신» 으로 잡는다. 그 사이 git log 에 cascade 관련 커밋이 최소 6건 들어왔다 — 8c9338c96 «cascade Step 1 — aggregate_designs 를 대표 행 선택으로 교체», 46566ca64 «cascade Step 2 — 어닐의 seed·구조해시를 축 CSV 까지», 93d1eb98b «cascade #7 — 실행 전 봉인 모드(--seal)», c221ac933 «cascade #7 — 실제 봉인 (v2_2026_09_08)». 즉 '수정 미착수' 는 사실이 아니다. 그리고 kb/projects 에 지금 살아 있는 cascade 캠페인(보고량 카드 비준 · #7 봉인 · 잔여 해제조건 #3·#4·#8)을 설명하는 프로젝트 카드가 **없다** — 관련 문서는 kb/methodology/cascade_lessons_transfer_2026_09_08.md 와 db/governance/decisions.json 에만 있다.
- **고치는 법**: 이 문서 status 를 '해소 — 항목별 대응 커밋 명시'로 바꾸고 항목마다 커밋 해시를 단다. 그리고 kb/projects 에 'cascade 캠페인 현황' 카드 하나(해제조건 8개 중 무엇이 닫혔고 무엇이 남았는지 + decisions.json 링크)를 신설한다 — 이 다섯 폴더에서 지금 제일 비어 있는 자리다.
- codex 필요: False

### [P2·broken] 5min-template-loop-broken
- **어디**: `kb/templates/seminar_script_5min_template.md:60 (작성 순서 4)`
- **근거**: 템플릿 마지막 단계 «4. digest 에 역링크 추가 + `python3 tools/litdb/build_index.py --check` **0 미등재 확인**». 그런데 `tools/kb_wiki.py lint` 가 «litdb INDEX*.md 어디에도 없는 digest 8개: deng2026_polysulfate_layer_moisture_oxidation_lpsc__seminar_5min_qa, kim2025_csp_metastable_edge_sharing_sse__seminar_5min_qa, ...» 를 찍는다 — 템플릿이 준거로 삼는 실물 세 편(Deng·Kim·Tu) 전부가 INDEX 미등재다. 즉 템플릿의 마지막 단계가 실제로는 한 번도 통과된 적이 없다.
- **고치는 법**: 세 준거 대본을 litdb INDEX 에 등재하거나(그게 맞다면), 반대로 `__seminar_5min_qa` 는 digest 가 아니라 동반문서이므로 INDEX 집계에서 제외하도록 build_index/lint 를 고친다. 어느 쪽이든 템플릿 step 4 의 문구를 실제 규칙과 맞춘다.
- codex 필요: False
