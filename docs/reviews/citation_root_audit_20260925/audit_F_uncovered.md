# 감사 F — 아무도 판정하지 않은 247 인용 키 (SELF-51 뿌리 감사 · 커버리지 보완)

> ⛔ **기록 사본** — 2026-09-26 읽기 전용 감사 에이전트 보고 원문 (scratchpad → 리포).  판정의 정본은 원장 `docs/reviews/claims.json` · `findings.json` `SELF-51` 이다.  file:line 은 보고서 머리의 기준 커밋 기준.  종합 = `docs/reviews/citation_root_audit_20260925.md`.


작성 2026-09-26 · 읽기 전용 (리포 변경 0, 쓰기는 스크래치패드만) · 산출물 = 이 문서 + `audit_F_uncovered.tsv` (247 행)

## 0. 범위 · 기준 · 방법

- **범위**: `coverage_uncovered.tsv` 의 **247 키 / 459 출현** (감사 A–E 가 판정하지 않은 저자-연도 키 전부). 출현 목록은 `cite_occ.tsv`.
- **기준 커밋**: 리포 `e8c4ea84c` (HEAD, 브랜치 `claude/stoic-knuth-NObVQ`, 2026-09-25 22:36 UTC). 표의 `file:line` 은 모두 이 커밋 기준.
- **정본**: `origin/claude/friendly-meitner-lldvar:litdb/papers/` — 시작 `ae22bf37b` (336 장), 끝에서 다시 fetch 한 `b15a56bf3` (338 장). 새로 도착한 카드는 **Böger 2023 · Stallard 2022** (Sharma 2023 · Wheatcroft 2023 은 아직 없음; Shi 2019 는 기존 카드).
  이번 키 가운데 새 카드에 기대는 것은 **Kondrakov 2017** 하나이고 Stallard 카드로 근거를 보강했다 ⇒ **"카드 도착 대기" 로 남긴 키는 없다.**
- **카드 조회**: 파일 목록(`git ls-tree`)과 본문 `git grep` 만 썼다. INDEX*.md 는 쓰지 않았다.
- **웹 검색**: 논문 실재와 서지 필드 확인에만 썼다. 검색 요약에서 본 숫자는 **"검색 요약 — 미확인"** 으로만 적었고 V 의 근거로 쓰지 않았다. 출판사 사이트(pubs.acs.org · arxiv.org)는 컨테이너에서 차단돼 원문 대조를 못 했다.
- **판정 어휘** (감사 A–E 와 같음):

| 라벨 | 뜻 |
|---|---|
| V | 정본 카드가 그 값·주장을 그 재료·조건으로 적는다 |
| P | 부분 지지 (카드가 일부만 확인 · 2차 카드 · 표기 일부가 카드와 다름) |
| M | 논문은 있으나 그 값·재료·조건이 아니다. 서지 필드가 틀리면 **M(서지)** |
| B | 웹 검색으로 실재 확인, 값은 원문 대조 안 됨 |
| F | 제목·저자·저널로 찾을 수 없음 → 지어낸 것으로 보임 |
| C | 방법·법칙 인용 (수치 귀속 없음) — 서지 정체가 그럴듯한지만 확인 |
| U | 판정 불가 |
| NOISE | 인용이 아님 (정규식 오탐) |

- **NOISE 규칙**: ① 상태 표기 + 날짜 (`CLOSED (2026-06-30)` 류) ② 원고 이력 날짜 (Received/Revised/Accepted/Published/Copyright) ③ 상표 (`Thinky 2000 rpm`) ④ **Klár 2016 원문 추출 텍스트** (`docs/literature_coverage/pdfs/Klar_2016_…txt`, 커밋 `94cbc48c7`) 안의 참고문헌 — 제3자 논문의 인용이지 리포의 주장이 아니다.
  학술지명 키(`Joule 2026` · `Magazine 2024` · `Letters 2025` · `Sources 2022` · `Batteries 2023` …)는 같은 줄의 실제 인용으로 풀어서 판정했다 — NOISE 로 처리한 학술지명 키는 없다.
- **한 키 안에서 판정이 갈릴 때**: 가장 무거운 줄(코드·웹앱 노출 우선)로 키를 대표하고, 나머지 줄의 판정은 근거 칸에 적었다 (Kato 2016 · Nature 2025 · Zhou 2019).
- **⚠ 커버리지 측정의 거짓 커버** (범위 밖이지만 기록): `coverage_measure.py` 는 "저자 뒤 40 자 안에 연도" 로 '판정됨' 을 셌다. 12 자로 조이면 판정된 키는 **199** 이고, **19 키는 우연 일치로만 '판정됨'** 이다 —
  `Sakuda 2017` (감사 A 의 "sakuda … cheng 2017") · `Kang 2023` · `Shi 2023` · `McMeeking 2000` · `Thorpe 2009` · `Energy 2024/2025/2026` · `Materials 2026` · `Chem 2024` · `Mater 2025` · `Comm 2025` · `FINAL 2026` · `PROGRESS 2026` · `GPa 2026` · `MPa 2021` · `Li 1993` · `Ge 2021` · `Mo 2018`.
  이 가운데 **Sakuda 2017** 은 Kato 2016 과 같은 웹앱 줄이라 이번에 함께 봤다 (서지 미특정 → U). 나머지는 판정하지 않았다 — 실제 인용으로 보이는 것은 Kang 2023 · Shi 2023 · Energy 2024/2025/2026 · Materials 2026 · Chem 2024 · Mater 2025 · Comm 2025 (학술지명 키) 정도다.

- **⚠ 인벤토리 자체의 사각지대** (규율 ⑤ 와 같은 부류): `cite_inventory.py` 는 `.py .md .js .html .txt .liggghts .sh` 만 훑었다 — **원고 `docs/paper/main.tex` · `refs.bib`, 그리고 `.csv` · `.json` 데이터 파일은 처음부터 인벤토리에 없다.** 같은 정규식으로 그 파일들(1,250 개)을 재면 인벤토리에 한 번도 오르지 않은 키가 **95 개 / 157 출현** 이고, 그중 **26 키가 main.tex · refs.bib** 에서 나온다:
  Bistri 2021 · Boulineau 2013 · Cronau- 2022 · CundallStrack 1979 · DiRenzo 2004 · Hopkins 2013 · JanekZeier 2023 · Kamaya 2011 · Kawakita 1971 · Landauer 1952 · Lewis 2022 · LiuYin 2025 · Majmudar 2005 · Milton 2002 · Mizuno 2005 · Mueth 1998 · Sahimi 1994 · Sohn 1968 · Sonnergaard 1999 · StaufferAharony 1994 · Storakers 2000 · Sun 2017 · Walther 2019 · Yang 2019 · Yi 2004 · Yu--Standish 1996 (일부는 bib 키 표기).
  이번 감사는 247 키 범위라 이것들을 판정하지 않았다 — 다만 원고 줄 가운데 이번 키와 같은 인용(Yu–Standish 1996 · Sridhar–Fleck–McMeeking · Storåkers 2000 · Bergman · Torquato · Cundall–Strack · Holm)은 §3 에 적었다. **원고 main.tex · refs.bib 전수 대조는 별도 감사로 남는다.**

## 1. 집계

**커버리지: 판정 247 / 247 키 (NOISE 96 · 실제 인용 151). 판정 불가(U) 5 키는 아래 목록.**

| 판정 | 키 | 출현 | 그중 scripts/·webapp/ 에 걸린 키 (출현) |
|---|---|---|---|
| V | 40 | 99 | 2 (2) |
| P | 7 | 19 | 0 |
| M | 13 | 25 | 5 (7) |
| B | 30 | 49 | 8 (10) |
| F | 3 | 7 | 1 (1) |
| C | 53 | 94 | 23 (30) |
| U | 5 | 8 | 2 (2) |
| NOISE | 96 | 158 | — |
| **합** | **247** | **459** | 41 (52) |

M 13 의 내역: M(서지) 7 (Inorganics 2025 · Letters 2025 · Dewald 2021 · Nature 2025 · Storåkers-Fleck-McMeeking 2000 · Sridhar-Fleck-McMeeking 2000 · Frontiers 2023) · 값·조건·주제 M 6 (Kato 2016 · Asia 2024 · Materials 2024 · Wenzel 2016 · Zhou 2019 · Yu-Standish 1996).

**판정 불가 (U) 5 키와 사유**

| 키 | 사유 |
|---|---|
| Kang 2024 | 웹앱 예측기 탄소 σ_el 블록의 근거 목록 (`webapp/predictor_engine.py:865`). 랩 2024 논문 둘(Cho 외 Electrochim. Acta 481 · Cha 외 JPS 617)은 Kang 이 제1저자가 아니고, Kang 제1저자 판은 2025 — 어느 논문인지 특정 불가 |
| Schmidt 2024 | "확률적 재습윤" · `--recontact elastic` 의 근거. 리포에 서지 없음. 후보(Schmidt·Sinzig·Wall, JES 2024 박리 모델)는 결정론적이라 "확률적" 과 맞지 않음 |
| Haile 2003 | brick-layer 입계 스케일링의 근거. 서지를 검색으로 특정하지 못함 |
| Birkholz 2022 | "DEM-ASSB 선행 논문" (반박 노트). Birkholz 의 저항망 논문은 2019 · 2021 만 확인, 2022 판 미확인. 원고에도 없음 |
| Jung 2022 | 동료 카톡 표의 2차 인용 ("0.003–0.4 mS/cm") — 서지 미특정 |

**가장 결과적인 발견 (코드·수치 우선)**

1. **웹앱 예측기 j₀ = 0.01 mA/cm² "NCM811/LPSCl" ← "Ref: Sakuda (2017), Kato (2016)"** (`webapp/predictor_engine.py:948–949`) — M. 검색 요약상 Kato 2016 (Nat. Energy) 의 전해질은 Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ 계라서 (미확인) NCM811/LPSCl 계면 j₀ 의 출처로 볼 근거가 없다. Sakuda (2017) 은 특정 불가. 이 값은 이용률 ν 계산에 들어가 사용자에게 보이는 예측을 바꾼다. 뿌리 = 04-24 import `660600a44`.
2. **등급 가이드 "4–6 = packed, <3 = sparse (Mukhopadhyay 2014)"** (`scripts/grade_engine.py:152`, 웹앱 등급 가이드에 노출) — F. 좌표수 기준으로 그런 논문이 없다. `41f3a9d9a` (05-20).
3. **STEP5 웹앱 패널 "Nature2025 Ni≥85"** (`webapp/templates/step5.html:35`) — M(서지). 실제는 *Nature Energy* 10, 479 (2025) 이고, 검색 요약상 소재는 NCA 계 Ni 80–95 % 라서 "Ni≥85" 문턱은 확인되지 않는다. `docs/data/rint_eis_anchors.csv:31` 은 이 논문을 "SC_NMC_Ni85plus" 로 적는다. `6c9296fe0` (07-23).
4. **등급 가중치 "Multi-crack 0.25 = healable (NPG Asia 2024)"** (`grade_engine.py:293`, GRADING_STORY) — M(조건). 그 논문은 다공 LIB 전극에 **SE 용액을 침투**시키는 공정이다. 건식 압밀 균열이 치유된다는 근거가 아니며, 리포 자신도 "ASSB 에선 SE 가 균열에 침투 불가" 라고 적는다. `83e3101c2` (05-22).
5. **"Mohayman 2025 DFT B/G = 1.47 → LPSCl 취성 → Hertzian 이 이긴다"** (`scripts/compare_hertzian_vs_physics.py:14`) — B. 논문은 있지만 값은 확인되지 않았고, 정본 deng2016 카드(B 28.7 · G 8.1 → B/G ≈ 3.5, "23 종 중 가장 연성")와 정반대다.
6. **다공도 예측기 문헌 사슬 "Sridhar-Fleck-McMeeking 2000 … α_KC = 2 (published)"** (`predict_porosity_strict_physics.py:16`) — M(서지) (두 논문의 저자명을 섞은 이름). 문서 쪽 "Storåkers-Fleck-McMeeking 2000" 도 연도 오기 (실제 1999, JMPS 47). 감사 C D1·D2 와 같은 뿌리 (`288d7b27c` · `1e3070493`, 05-13).
7. **원고 5-1 절 초안(`paper_brittle_caveat.md`)의 "Solid Power 2023 disclosures, internal cell-aging data"** — F (5 곳). 같은 초안의 "Wenzel 2016 = 입경–전도도 교과서 설명" 도 M 이다 (정본에 기록된 Wenzel 2016 판본은 전부 계면 논문). `afd760adf` · `d62ba398b` (04-30).
8. **반박 노트 "DEM-ASSB 선행 paper → paper Sec 5-1 (Bielefeld 2019, Birkholz 2022, Grießer 2021)"** — Grießer 2021 은 F, Birkholz 2022 는 U. 둘 다 원고 main.tex · refs.bib 에 없다. `148d0f5fb` (05-04).
9. **Alabdali 2024 사이클 DEM 의 "AM 반경 ±6 %"** (a10 설계 · 문헌 리뷰) — P. 카드는 "±6 % **부피**" 로 읽는다 (원문은 "size … by 6 %"). 반경으로 구현하면 부피 변형이 약 3 배가 된다. `0822e6adf` · `4f8d33b6f`.
10. **원고 main.tex 에 걸린 서술 오류** (인벤토리 밖이지만 이번 키와 같은 인용): "Yu–Standish 1996 multimodal RCP" (:659 · :710 · :1013 — 1996 판은 **비구형** 입자 모델, 다성분 모델은 1991 판 → M) · "Sridhar–Fleck–McMeeking … α_KC = 2 \citep{Sridhar2000}" (:563 — 저자명 혼합) · refs.bib `Storakers2000` = "JMPS 48 (2000)" (실제 47 (1999)). 셋 다 `144e18b60` (05-13).
11. **서지 연도 오기 3 건**: Inorganics "2025" → 2026, 14(7), 180 · ACS Energy Letters "2025" (bimodal) → 2026, 11, 2103 (감사 B 의 Oh 2026 과 같은 뿌리) · Frontiers "2023" → 2024 (matthews2024 카드). 이 밖에 Dewald 2021 은 Minnmann 2021 데이터에 저자를 잘못 붙인 것 (주석 처리됨), Attia 2020 `n_cells: 224` 는 검색 요약상 후보 프로토콜 수 (셀 ≈169–180, 미확인), Zhou 2019 는 README 에서 "Halide SE σ" 의 출처로 잘못 쓰였다.

긍정 쪽: **V 40 키**는 정본 카드와 일치한다. GeoDict 판본 7 개가 전부 맞고, Franco 그룹 카드(Weitze · Alabdali · Zhang 2026), Bielefeld 2020 이 인용한 입력들(Kato 2016/2018 · Braun · Nam · Froboese · Wiegmann), hare2026 이 쓴 Lischka 세트, Koo 2025/2026 서지가 모두 일치한다.

## 2. 판정 표 — 실제 인용 151 키 (M → F → U → P → B → C → V; 같은 판정 안에서는 코드·웹앱 줄이 있는 키 먼저, 이어서 출현 수)

최초 커밋 칸은 M·F·U·P 행에 채웠다 (`git log -S` 로 해당 문자열이 처음 들어온 커밋). 근거 칸의 "(검색)" 은 웹 검색으로 실재만 확인했다는 뜻이다.

| # | 인용 (리포 표기) | 값·주장 | 리포 위치 (file:line, 건수) | 판정 | 근거 | 최초 커밋 |
|---|---|---|---|---|---|---|
| 1 | **Asia 2024** — "NPG Asia 2024 \"Infiltration-driven enhancement\"" (grade_engine.py:293 주석) · GRADING_STORY.md:17,109 | Microcrack/Multi-crack = "SE infiltration 으로 healing 가능" ⇒ 등급 가중치 0.25 ("healable") | docs/GRADING_STORY.md:17,109 · scripts/grade_engine.py:293 (3) | **M** | 실재: "Infiltration-driven performance enhancement of poly-crystalline cathodes in all-solid-state batteries", NPG Asia Mater. 16 (2024) (검색). 검색 요약: LIB 다공 전극에 **SE 용액을 침투**시키는 공정 논문 — 건식 300 MPa 압밀 중 생긴 균열이 치유된다는 근거가 아님 (조건 불일치). 리포 자신도 "ASSB 에선 SE 가 균열에 침투 불가" 라고 적는다 (ncm_sc_poly_electrochem_anchors.md:18 · Trevisanello 카드) | 83e3101c2 (05-22, grade_engine) · 06aece281 (05-22, GRADING_STORY) |
| 2 | **Dewald 2021** — 주석 처리된 앵커 ('Dewald 2021 25% NCM', 0.65, 2.4) ×3 스크립트 | τ² ≈ 2.4 @ 25 % NCM | scripts/build_tau_regime_db.py:228 · scripts/compare_hertzian_vs_physics.py:118 · scripts/plot_tau_regime_si.py:108 (3) | **M(서지)** | 리포가 이미 "Minnmann 과 같은 논문 (DOI 10.1149/1945-7111/abf8d7) ⇒ 이중계상" 으로 뺐다 (GAP3-37). 정본 minnmann2021 카드 저자 = Minnmann · Quillman · Burkhardt · Richter · Janek — **Dewald 없음** ⇒ 저자 표기 자체가 틀림. 값 2.4 는 카드의 τ_ion² @25 vol% (~2.4) 와 일치 | 660600a44 (04-24 import) |
| 3 | **Kato 2016** — "# Ref: Sakuda (2017), Kato (2016)" (웹앱 예측기) · "(Kato 2016)" (Bielefeld 2020 요약 2곳) | 웹앱 예측기 j₀ = 0.01 mA/cm² "NCM811/LPSCl interface" (`j0 = 0.01e-3`, 이용률 ν 계산에 들어감) | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:19,148 · webapp/predictor_engine.py:948 (3) | **M** | 웹앱 줄: Kato 2016 = Nat. Energy 1, 16030 — 검색 요약상 이 논문의 전해질은 Li9.54Si1.74P1.44S11.7Cl0.3 (25 mS/cm) 계 (미확인) ⇒ NCM811/LPSCl 계면 j₀ 의 출처로 볼 근거가 없음 (소재 불일치). 같은 줄의 "Sakuda (2017)" 은 커버리지 측정의 거짓 커버 (§0) — 서지 미특정, 판정 U. 문서 2곳(lit_bielefeld2020 :19 · :148)은 정본 bielefeld2020 카드 "σ_bulk,SE = 2.7 mS/cm (Kato 2016)" 과 일치 = V | 660600a44 (04-24 import) · 문서 2곳 a6bcce934 (06-26) |
| 4 | **Nature 2025** — "Nature2025 Ni≥85" (웹앱 STEP5 패널) · "TabPFN (Nature 2025, 637, 319–326)" (랩 주간 요약) | CAM/SE 이탈(접촉손실)이 Ni≥85 에서 지배 = "OTHER(모델 밖)" 채널 | docs/lab_weekly_20260727_digest.md:11 · webapp/templates/step5.html:35 (2) | **M(서지)** | 웹앱이 가리키는 DOI(docs/step5_cycle_degradation.md:68) 10.1038/s41560-025-01726-8 = *Nature Energy* 10, 479–489 (2025) "High-energy, long-life Ni-rich cathode materials with columnar structures for ASSBs" (검색) ⇒ 학술지명 오기. 검색 요약: Li[NixCoyAl]O₂ Ni 80–95 %, "detachment increases with Ni content" — "Ni≥85" 문턱은 미확인. TabPFN 줄은 정본 hollmann2025 카드 "Nature 637, 319–326" 과 일치 = V | 6c9296fe0 (07-23, step5.html) |
| 5 | **Sridhar-Fleck-McMeeking 2000** — "Sridhar-Fleck-McMeeking 2000 SFM constraint: KC = 1 + α_KC · f_AM² with α_KC = 2 (published, no fit)" | α_KC = 2 를 "published" 값으로 (생산 다공도 예측기의 문헌 사슬) | scripts/predict_porosity_strict_physics.py:16 (1) | **M(서지)** | 저자명 혼합: Sridhar & Fleck 2000 (Acta Mater. 48, 3341) 과 Storåkers · Fleck · McMeeking 1999 (JMPS 47) 를 섞은 이름. α = 2 "published/typical" 은 감사 C D1 에서 원문 미확인 (다른 스크립트는 같은 인용으로 α = 3) | 288d7b27c (05-13) |
| 6 | **Inorganics 2025** — "MDPI Inorganics 2025 14(7):180 — DRT" | 황화물 복합양극 임피던스 → DRT 5 성분 (LiNbO₃ 코팅 Ni-rich, 로딩 의존) | docs/rint_anchor_db_research.md:69,169 · docs/rint_reference_growthlaw_design.md:138 (3) | **M(서지)** | DOI 10.3390/inorganics14070180 = *Inorganics* **2026**, 14(7), 180 (2026-07-03 게재, 검색). 내용(5 성분·로딩 의존)은 검색 요약과 일치, 연도만 틀림 (권 14 = 2026) | 84bc3b354 (07-20) |
| 7 | **Wenzel 2016** — "literature consensus (Knauth 2009, Wenzel 2016, Cronau 2022)" (영·한 2곳) | 세라믹 전해질 σ ↔ 입경의 "표준 교과서 설명" (N_GB ∝ 1/R) | docs/paper_brittle_caveat.md:928,1126 (2) | **M** | 리포가 서지를 특정하지 않음. 정본에 기록된 Wenzel 2016 판본들(chaney2024 · lai2025 · li2026 카드: ACS AMI Na₃PS₄\|Na EIS · SSI Li₇P₃S₁₁\|Li 전하이동 · LPSC XPS)은 전부 **계면 반응** 논문 — 입경–전도도 설명이 아님. 같은 문장의 "Cronau 2022 … D50 5–10 µm → <0.3 µm ≈1/3" 은 정본 cronau2022 카드상 σ 가 입경이 아니라 밀링 손상을 따름 (다른 감사 소관) | d62ba398b (04-30) |
| 8 | **Yu-Standish 1996** — "Yu-Standish 1996 multimodal RCP → principled extension" · "cite Yu-Standish 1996 multimodal RCP … as principled future work" | 다성분(multimodal) 구 충전 RCP 확장의 근거 | docs/porosity_wave_shape_physics.md:63,71 (2) | **M** | 1996 판은 Yu · Zou · Standish, Ind. Eng. Chem. Res. 35, 3730 "Modifying the linear packing model for predicting the porosity of **nonspherical** particle mixtures" (검색 — 제목) — 주제가 비구형 입자. 다성분 선형충전 모델은 1991 판 (Ind. Eng. Chem. Res. 30, 1372 "Estimation of the porosity of particle mixtures by a linear-mixture packing model"). ⚠ 같은 서술이 원고 docs/paper/main.tex:659 · :710 · :1013 에도 있다 (인벤토리가 .tex 를 안 훑어서 이 키에 안 잡힘) | 1e3070493 (05-13, 문서) · 144e18b60 (05-13, main.tex) |
| 9 | **Zhou 2019** — README §4 "Zhou 2019 ACS Energy Lett (σ_SE baseline)" · 표 "Halide SE σ (cold-press) \| 1 mS/cm \| Zhou 2019" | ① Li6PS5Cl σ 2.4 mS/cm 등 argyrodite 표 (σ_grain 앵커 후보) ② 할라이드 SE σ 1 mS/cm | docs/literature_coverage/README.md:140,275 (2) | **M** | 실재: Zhou · Park · Sun · Lalère · Adermann · Hartmann · Nazar, ACS Energy Lett. 4, 265 (2019) "Solvent-engineered design of argyrodite Li6PS5X" (검색) — ① 은 B (값 미확인). ② 이 논문은 **황화물 argyrodite** 라 "Halide SE σ" 의 출처가 될 수 없음 (소재 불일치) | 660600a44 (04-24 import) |
| 10 | **Frontiers 2023** — "Lit (Frontiers 2023 fenrg.2023.1336344; …)" | PTFE 피브릴 형태(1차 수 µm Ø·수백 µm 길이 → 수십 nm) 근거 5 편 중 하나 | docs/cbd_morphology_roadmap.md:14 (1) | **M(서지)** | 정본 matthews2024 카드: "Front. Energy Res. 11, 1336344 (**2024**) — DOI 의 2023 은 채택연도, 인용에는 2024". 피브릴 수치는 5 편을 합친 요약이고 이 카드는 "구간 서술만" | 1381fbc0d (06-24) |
| 11 | **Letters 2025** — "[Bimodal Composite Cathodes (ACS Energy Letters 2025)](…5c03923)" | P:S 7:3 최적 근거 목록의 첫 항 | docs/GRADING_STORY.md:182 (1) | **M(서지)** | DOI 10.1021/acsenergylett.5c03923 = ACS Energy Lett. **11**(2), 2103–2114, 2026-02-13 게재 (Oh · S.-Y. Lee · H.-G. Jung 외, 검색) — 연도 오기. 감사 B 의 "grade_engine 'Lee 2025 ACS EL' = 실제 Oh 2026" 과 같은 뿌리 (같은 날 같은 세션) | 06aece281 (05-22) |
| 12 | **Materials 2024** — "[Infiltration-driven enhancement (NPG Asia Materials 2024)](…s41427-024-00555-7)" (GRADING_STORY 참고문헌) | 위 Asia 2024 와 같은 인용 (healing 근거) | docs/GRADING_STORY.md:185 (1) | **M** | Asia 2024 행과 같음 (같은 논문의 링크 줄) | 06aece281 (05-22) |
| 13 | **Storåkers-Fleck-McMeeking 2000** — "Storåkers-Fleck-McMeeking 2000, Jacobs 2009" | SE 60→30 % 구간 "stress-bearing percolation 활성 → 소성 개시" | docs/porosity_wave_shape_physics.md:30 (1) | **M(서지)** | SFM 논문은 J. Mech. Phys. Solids **47** (1999) 785–815 (감사 C D2). 연도 오기 — 감사 C 가 같은 계열의 "Acta Mater. 48 (2000) 4203" 을 M(서지)로 판정 | 1e3070493 (05-13) |
| 14 | **Mukhopadhyay 2014** — grade_engine 'meaning': "4–6 = packed, <3 = sparse (Mukhopadhyay 2014). RCP ≈ 6." | SE–SE 좌표수 등급 기준 (문턱 5.5 … 3.0) | scripts/grade_engine.py:152 (1) | **F** | 좌표수 기준으로 그런 논문을 찾지 못함 (검색 2 회). 알려진 Mukhopadhyay & Sheldon 2014 (Prog. Mater. Sci.)는 전극 응력 총설 (일반 지식 — 미확인). 이 문자열은 웹앱 등급 가이드 "자세히 (기술적 근거)" 로 사용자에게 노출 (app.py:892 · :9341–9344) | 41f3a9d9a (05-20) |
| 15 | **Power 2023** — "Solid Power 2023 disclosures, internal cell-aging data" · "Solid Power (2023 roadmap)" (영·한 5곳) | 서브µm 펠릿이 Li 금속 압력에서 creep·덴드라이트 채널↑ · 업계(Samsung SDI 2024 · Solid Power 2023 · QuantumScape)가 모두 fine+coarse SE 이중층 | docs/paper_brittle_caveat.md:961,1083,1108,1156,1271 (5) | **F** | 공개 공시·논문을 찾지 못함 (검색). "internal cell-aging data" 는 공개 출처가 될 수 없음. 같은 문장은 QuantumScape 를 fine/coarse 황화물 SE 사례로 드는데 그 회사 분리막은 산화물 세라믹으로 알려져 있음 (일반 지식 — 미확인) | afd760adf (04-30) |
| 16 | **Grießer 2021** — "DEM-ASSB 선행 paper? → paper Sec 5-1 (Bielefeld 2019, Birkholz 2022, Grießer 2021)" | DEM-ASSB 선행 논문 (원고 5-1 절 인용이라고 적음) | docs/Reviewer_Defence_Notes.md:308 (1) | **F** | 저자-연도만 있음; ASSB/DEM 로 검색해도 찾지 못함 (2 회). 원고(docs/paper/main.tex · refs.bib)에 **없음** ⇒ "paper Sec 5-1" 인용이라는 서술부터 사실이 아님 | 148d0f5fb (05-04) |
| 17 | **Schmidt 2024** — "확률적 재습윤 (Schmidt 2024)" · "--recontact elastic … (Schmidt 2024 방향)" | 파단 접촉의 재접촉 규약 (코드 옵션 근거) | docs/a10_cycle_chemomech_design.md:58,107 · scripts/cycle_contact_ledger.py:16 (3) | **U** | 리포에 서지 없음. 후보: Schmidt · Sinzig · Wall, JES 171 (2024) "An Electro-Chemo-Mechanic Model Resolving Delamination between Components…" (검색) — 결정론적 접촉 모델로 보여 "확률적" 과 맞지 않음. 확정 불가 | 0822e6adf (07-21) |
| 18 | **Kang 2024** — "# Ref: Reisacher 2023 (C65 σ_e …) · Minnmann 2021 · Kang 2024" · "우리 랩 케이스(Kim/Cho/Kang 2024-25)" | 탄소 첨가제 σ_el 블록의 근거 | docs/mpm_wallP_conditional_troubleshooting.md:410 · webapp/predictor_engine.py:865 (2) | **U** | 식별 불가: 랩 2024 논문 둘(Cho·Yun·Kang·Kim·Lee, Electrochim. Acta 481 · Cha·Yun·Kim·Kang·Cho·Lee, JPS 617)은 Kang 이 제1저자가 아니고, Kang 제1저자 판은 2025 (정본 kang2025 카드들) | 660600a44 (04-24 import) |
| 19 | **Birkholz 2022** — 같은 줄 "(Bielefeld 2019, Birkholz 2022, Grießer 2021)" | DEM-ASSB 선행 논문 | docs/Reviewer_Defence_Notes.md:308 (1) | **U** | Birkholz(·Gan·Kamlah)의 저항망 논문은 2019·2021 (Powder Technol.) 이 실재하고 정본 bazzoun2026 · electromechanical_contact_model 카드도 Birkholz 2019 를 인용 — "2022" 판과 "DEM-ASSB" 성격은 확인 불가. 원고에 없음 | 148d0f5fb (05-04) |
| 20 | **Haile 2003** — "소결 세라믹 이온전도체에서 확립된 입계 수 스케일링 (Haile et al., 2003)" + brick-layer 식 | R_gb = ρ_gb·w_gb·L/(L_g·A), N_GB ∝ GB_d × T | GB_correction_fitting_report.md:153 (1) | **U** | brick-layer 모델 자체는 고전이나 "Haile et al. 2003" 서지를 검색으로 특정하지 못함 | 660600a44 (04-24 import) |
| 21 | **Jung 2022** — 동료 표 "Jung 2022 0.003–0.4" (σ_e, mS/cm) | 복합양극 σ_e 범위 | docs/session_20260923_progress.md:121 (1) | **U** | 동료(카톡) 표의 2차 인용 — 서지 미특정 | 0489233c8 (09-23) |
| 22 | **Weitze 2024** — "Weitze 2024 (Franco, NMC622+LPSCl wet-process) … resolved multisphere … rigid … Fig 7" 외 4곳 | nano-CT 실제 형상 AM 을 multisphere+harmonic bond 로 강체화; Fig 7 에서 압연이 AM-SE 계면을 못 키운다고 저자 자인 | docs/literature_review_dem_mpm_assb.md:36,119,233,315 · docs/positioning_vs_geodict.md:41 (5) | **P** | 정본 wet_processing_resolved_am_ssb_cathode_manufacturing 카드: Weitze · Zanotto · Zapata Dominguez · Franco, ESM 73 (2024) 103747 — 형상·강체·Fig 7(AM-SE ~1, 저자 한계 자인) 모두 일치. 다만 ① "NMC622+LPSCl" → 카드 정정(08-19): NMC622 는 형상 공여체, 슬러리 AM 은 Ni-rich ② literature_review:36 이 "LIGGGHTS" 행에 분류 → 카드: LAMMPS | 4f8d33b6f (06-26) |
| 23 | **Strauss 2018** — README §5 "Strauss 2018 ACS Energy Lett" · 표 "NCM secondary d 3-5 μm \| Strauss 2018, Bielefeld 2019" · "CAM vol% (carbon-free) ≥60 \| Strauss 2018" · Minnmann 2022 요약 | 탄소 없는 NCM622+β-Li₃PS₄ 입경별 비활성 CAM 2/27/31 % · 용량 162/95/84 mAh/g · 3–5 µm 최적 · ≥60 vol% | docs/lit_minnmann2022_designing_cathodes_solidstate.md:77 · docs/literature_coverage/README.md:154,268,272 (4) | **P** | 서지: 정본 cronau2022 카드 ref [21] Strauss · Bartsch · de Biasi · Kim · Janek · Hartmann · Brezesinski, ACS Energy Lett. 3, 992 (2018). 내용: bielefeld2019 카드 "carbon-free NCM-622 + LPS, AM 입경↑ → 전자전도 급락·비활성 NCM↑"; minnmann2022 카드 "3–5 µm (refs 36, 37)", ">60 vol% (refs 11, 36)" (2차). README 표의 숫자는 카드에 없음 | — |
| 24 | **Alabdali 2024** — "Alabdali 2024 (ESM 70:103527, Franco그룹) … AM 반경 ±6% 팽창/수축" · "AM 반지름 ±6% `fix adapt` swing" | LIGGGHTS 강체구 베드(NMC532+LPSCl, 11k 입자)에 AM ±6 % 사이클 → 응력 재분배 | docs/a10_cycle_chemomech_design.md:54 · docs/literature_review_dem_mpm_assb.md:39,286 (3) | **P** | 정본 dem_mechanical_stresses_ssb_electrode_cycling 카드: Alabdali … Franco, ESM 70 (2024) 103527 — LIGGGHTS Hertz · LPSCl+NMC532 · 11,002 입자 · 375 MPa → 1/3/5 MPa · 5 사이클 일치. 단 리포는 "반경(반지름) ±6 %", 카드는 "±6 % 부피" (원문 "size … by 6 %") — 반경으로 구현하면 부피변형이 약 3 배 | 0822e6adf (07-21, a10) · 4f8d33b6f (06-26, review) |
| 25 | **Auvergniot 2017** — "Auvergniot 2017 (Chem. Mater.) — XPS … (LPSCl → S⁰, Li polysulfides, P2Sx, phosphates, LiCl) at uncycled / 2nd / 50th cycle" | LPSCl–양극 계면 산물과 사이클별 변화 | docs/rint_anchor_db_research.md:70,169 (2) | **P** | 정본 nolan2018 카드(ref 111): Auvergniot, Cassel, Ledeuil, Viallet, Seznec, Dedryvère, Chem. Mater. 29, 3883–3890 (2017) — 계면 산물 S · 폴리설파이드 · P₂Sₓ · LiCl 확인 (2차). "phosphates" 와 "uncycled/2nd/50th" 는 미확인 | — |
| 26 | **Hlushkou 2018** — README §3 "Hlushkou 2018 JPS (user-supplied main + SI)" · k_spread 표 | 276 MPa · LCO/LPSI · 재구성 33.1/53.7/13.2 % · τ 1.6/1.74/1.34/1.27 · coverage ~80 % (UB) | docs/literature_coverage/README.md:95,130 (2) | **P** | 정본에는 bielefeld2020 카드의 "void 15 % 가정 (Kato 미보고 → Hlushkou 13.2 %류)" 뿐 — 13.2 % 만 확인. 나머지 표 값은 카드 밖 (사용자 제공 PDF 요약) | — |
| 27 | **Ruess 2020** — "(Ruess 2020: 고체 셀은 균열 무관 = monolithic 거동)" · "선행연구(ref [21], 같은 그룹 Ruess 2020)" | 액체는 균열에 침투해 겉보기 D↑, 고체전해질은 침투 불가 | docs/lit_trevisanello2021_sc_pc_ncm_cracking_diffusion.md:82 · docs/ncm_sc_poly_electrochem_anchors.md:18 (2) | **P** | 정본 trevisanello2021 카드가 "ref [21] Ruess 2020 … 이 효과는 기계적으로 단단한 고체전해질로는 일어나지 않는다" 를 Trevisanello 의 서술로 기록 (2차). Ruess 원문 카드는 없음 | — |
| 28 | **Franco 2024** — "DEM-cycling-stresses (Alabdali/Franco 2024, ENSM) … AM 반지름 ±6% Vegard swing 5사이클" | Alabdali 2024 와 같은 인용 | docs/literature_review_dem_mpm_assb.md:169 (1) | **P** | Alabdali 2024 행과 같음 | 4f8d33b6f (06-26) |
| 29 | **Kondrakov 2017** — "--dv-pct 5.1 (Kondrakov 2017 NMC811 격자, 3.0–4.3V)" (코드 기본값·provenance 문자열) · a10 표 · stage4 "de Biasi/Kondrakov 2017" | NMC811 격자 ΔV −5.1 % (c 14.467→14.030 Å) · high-Ni ~8 % (c 14.469→13.732 Å) | docs/a10_cycle_chemomech_design.md:21 · docs/stage4_electrochem_research.md:87 · scripts/cycle_contact_ledger.py:10,340,605 (5) | **B** | 실재: Kondrakov 외, JPCC 121, 3286 (2017) — 검색 요약 "NCM811 ≈5.1 % @3.0–4.3 V" (미확인). 정본 stallard2022 카드(09-26 도착): NMC811 V/V₀ −4.8 % @x 0.20 · −7.0 % @x 0.11 (derived) ⇒ −5.1 % ≈ x 0.19, "인용 시 x 병기" 권고. "~8 %" 줄은 de Biasi 2017 (JPCC, 10.1021/acs.jpcc.7b06363) 쪽 — stallard 카드 ref [37] 로 실재 | — |
| 30 | **Balberg 1984** — "φ_perc·(L/D) ≈ 0.7 (Balberg 1984, excluded-volume percolation)" | 막대 퍼콜레이션 개시 상수 | docs/dem_perturbation_layer.md:131 · scripts/dem_perturbation.py:233 (2) | **B** | 실재: Balberg 외, PRB 30, 3933 (1984) (검색). 0.7 은 미확인 | — |
| 31 | **Mohayman 2025** — "Expected (per Mohayman 2025 DFT, B/G = 1.47 < 1.75): LPSCl is brittle-dominated → Hertzian should win" · README §10 표 | LPSCl Y 30.08 · B 18.07 · G 12.3 GPa · B/G 1.47 (취성) | docs/literature_coverage/README.md:330 · scripts/compare_hertzian_vs_physics.py:14 (2) | **B** | 실재: Mohayman · Diaz · Kushima, ACS Appl. Eng. Mater. 3, 2299 (2025) (검색). 수치 미확인. ⚠ 정본 deng2016 카드 Li₆PS₅Cl B 28.7 · G 8.1 GPa ⇒ B/G ≈ 3.5 ("23 종 중 가장 연성") 와 정반대 — 스크립트의 "Hertzian 이 이긴다" 예상이 이 한 값에 기대고 있음 | — |
| 32 | **Philipse 1996** — "φ_jam = C_rod·D/L (Philipse 1996 … C_rod=5.4)" | VGCF L/D≈67 → φ_jam ≈ 8 vol% | docs/dem_perturbation_layer.md:59 · scripts/dem_perturbation.py:279 (2) | **B** | 실재: Philipse, Langmuir 12, 1127 (1996) — 검색 요약 φ·(L/D) = ⟨c⟩ = 5.4 ± 0.2 로 일치 (미확인). 5.4/67 = 0.081 산술 맞음 | — |
| 33 | **Attia 2020** — {'name': 'Stanford-SLAC (Attia 2020 CLO)', 'n_cells': 224} | 셀 224 개 | scripts/cycling_data_ingest.py:243 (1) | **B** | 실재: Attia 외, Nature 578, 397 (2020). 검색 요약: 224 는 **후보 충전 프로토콜** 수이고 데이터셋 셀은 ~169–180 — n_cells 224 는 정의가 다를 가능성 (미확인) | 79f78e093 (07-23) |
| 34 | **Clausnitzer 2023** — "# Ref: Minnmann 2021, Clausnitzer 2023, Bielefeld 2019" (dead-AM 추정) | dead AM 문턱 "~25–30 vol% AM" | webapp/predictor_engine.py:827 (1) | **B** | 실재: Clausnitzer 외, Batteries & Supercaps 6, e202300167 (2023) (검색). 문턱 값은 리포 스스로 AUD-02 로 Bielefeld 2019 와 불일치 표기 | — |
| 35 | **ScienceDirect 2021** — grade_engine 'meaning': "(b) ScienceDirect 2021 \"cathode architecture\": geometric packing 큰 입자 위주 + 작은 입자 void 채움" | P:S 7:3 최적 밴드의 근거 (웹앱 등급 가이드에 노출) | scripts/grade_engine.py:435 (1) | **B** | Direct 2021 과 같은 논문 — 검색 요약 "1·2차 입자 주변 충전을 기하 모델로 모사" 는 서술과 부합. "7:3 최적" 은 이 논문으로 미확인 | — |
| 36 | **Severson-MIT-Toyota 2019** — {'name': 'Severson-MIT-Toyota 2019', 'n_cells': 124} | LFP/흑연 124 셀 데이터셋 | scripts/cycling_data_ingest.py:237 (1) | **B** | 실재: Severson 외, Nature Energy 4, 383 (2019) — 검색 요약 124 셀 일치 (미확인) | — |
| 37 | **Zhou 2025** — "Zhou 2025 (ACS Energy Lett.) — fine vs coarse LPSCl: R_ct(fine) < R_ct(coarse) at 2 MPa" · "tailored-low-P(Zhou2025)" | fine LPSCl 이 2 MPa 에서 R_ct 낮음 | docs/literature_review_dem_mpm_assb.md:38 · docs/rint_anchor_db_research.md:76,169 · docs/rint_reference_growthlaw_design.md:86 (4) | **B** | 실재: Zhou · Lu · Mish 외, ACS Energy Lett. 10, 966 (2025), DOI …4c03256 "Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure" (검색). 검색 요약은 "2 MPa 에서 사이클 안정성 우위" — R_ct 비교는 미확인 | — |
| 38 | **Feng 2025** — "Feng 2025 review — …cssc.202501033 (PMC12665888)" | Modified NCM811-sulfide 80 % @250 cyc @4.3 V | docs/rint_anchor_db_research.md:49,84,165 (3) | **B** | 실재: Feng 외, ChemSusChem 18, e202501033 (2025) "NCM811–Sulfide Electrolyte Interfacial Degradation…" (검색). 수치 미확인 | — |
| 39 | **Frontiers 2021** — "Frontiers 2021 (dry 2.39 / wet 1.0–1.9)" · σ_e 2.2–2.9e-6 S/cm · Eₐ 0.20–0.245 | LPSCl 냉간압 펠릿 σ·σ_e·Eₐ | docs/data/lpscl_electrolyte_params.md:12,24,29 (3) | **B** | 실재: Frontiers in Chemistry 2021 (10.3389/fchem.2021.778057) "Ionic and Electronic Conductivities of Li6PS5Cl … Wet Milling" — 검색 요약 습식 1.0–1.9 mS/cm 일치; 나머지 미확인. 문서 스스로 "검색 스니펫 값" 이라 명시 | — |
| 40 | **Ebner 2013** — "Ebner et al. (2013)의 tomography 기반 실험 … Bruggeman exponent n = 1.27–1.53" | Bruggeman n 1.27–1.53 (복합 양극) | docs/electronic_conductivity_derivation.md:46,319 (2) | **B** | 실재: Ebner · Geldmacher · Marone · Stampanoni · Wood, AEM 3, 845 (2013) (검색). 대상은 액체 LIB 다공 전극 — 수치·"복합 양극" 적용 미확인. 같은 표의 "σ_AM 0.05 S/cm — ACS Mater. Lett. (2024)" 는 감사 E 소관 | — |
| 41 | **Makse 2004** — "Makse, Gland, Johnson, Schwartz (2004, Phys. Rev. E 70, 061302) … K, G ∝ Z²" · "Makse (2004) 유사: K,G ∝ Z²" | granular 탄성률이 좌표수의 제곱에 비례 (σ_e 폼의 CN² 항 정당화) | GB_correction_fitting_report.md:908 · docs/electronic_conductivity_derivation.md:98 (2) | **B** | 서지 실재 (PRE 70, 061302). 검색 요약은 "모듈러스가 EMT 의 p^{1/3} 보다 빨리 증가" 를 다룸 — "K, G ∝ Z²" 는 확인 안 됨 (표준 EMT 는 Z 의 1 차 또는 2/3 승 — 일반 지식, 미확인) | — |
| 42 | **Payandeh 2023** — "Payandeh 2023 (admi.202201806 [B])" | 코팅 SC-NMC 93 % @200 cyc vs 비코팅 ~79 % | docs/pipeline_step1_to_step5_guide.md:449 · docs/step5_cycle_degradation.md:67 (2) | **B** | 실재: Payandeh 외, Adv. Mater. Interfaces 2023 "The Effect of Single versus Polycrystalline Cathode Particles on ASSB Performance" — 검색 요약 93 % vs 79 % @200 cyc 로 리포 값과 일치 (미확인) | — |
| 43 | **Pritzl 2019** — "Pritzl 2019 JES — 10.1149/2.0451904jes" | R_contact ≈10 (형성) → ≈30 Ω·cm² @50 cyc | docs/rint_anchor_db_research.md:52 · docs/rint_reference_growthlaw_design.md:79 (2) | **B** | 실재: Pritzl … Gasteiger, JES 166, A582 (2019), LNMO/Al 집전체 접촉저항 (검색). 수치 미확인 | — |
| 44 | **Shozib 2024** — "Shozib 2024 (조립 350→530 MPa, 원문 미확인)" | Ag–C/SE 점착 vs 조립압 | docs/adhesion_agc_interlayer_20260923.md:152,196 (2) | **B** | 후보: JES 2024 (10.1149/1945-7111/ad7c82) Ag–C 중간층 — 검색 요약 "조립압 350→530 MPa 에서 점착↑, 530 초과 시 분리막 균열". 리포 스스로 원문 미확인이라 적음 | — |
| 45 | **Brouwers 2006** — "Regime transition at d_L/d_S≈4~5 \| Brouwers(2006)" | 충전 regime 전이 크기비 | docs/Packing_Regime_Analysis.md:152 (1) | **B** | 실재: Brouwers, PRE 74, 031309 (2006) (검색). 4~5 는 미확인 | — |
| 46 | **Chem 2025** — "Al/C 화학안정(argyrodite): SS/Ni/Al/Al-C 안정, Cu/Li 부식 (Nat Commun Chem 2025)" | 집전체 화학 안정성 | docs/rint_reference_growthlaw_design.md:82 (1) | **B** | 실재: *Communications Chemistry* 8 (2025) "Probing the chemical stability between current collectors and argyrodite Li6PS5Cl" — 검색 요약 SS/Ni/Al/Al-C 안정, Cu/Li 부식으로 일치. 저널명 "Nat Commun Chem" 은 틀린 표기 | — |
| 47 | **Dec 2025** — "Sung Beom Cho, Junghyun Choi, Jun Hyuk Kang, … *Communications Materials* 6 (Dec 2025). DOI 10.1038/s43246-025-01046-0" | PTFE 피브릴화 다중스케일 설계 (FEM+GPR+Bayes) | docs/literature_dry_assb.md:379 (1) | **B** | DOI 실재 (Communications Materials, PTFE 피브릴화 다중스케일, 검색). 검색 요약상 권·연도 vol 7, art. 34 (2026) · 저자 첫머리 Jun Hyuk Kang — 리포의 "6 (Dec 2025)" · 저자 순서와 다를 수 있음 (미확인) | — |
| 48 | **Direct 2021** — "[Cathode architecture for energy density (Sci Direct 2021)](…S240582972100204X)" | P:S 7:3 근거 목록 | docs/GRADING_STORY.md:186 (1) | **B** | 실재: ESM 2021 (ORNL) "Understanding implications of cathode architecture on energy density of SSBs" (10.1016/j.ensm.2021.05.001, 검색). "Sci Direct" 는 플랫폼명 | — |
| 49 | **Doerrer 2021** — "SC-NMC83 5.5% … Doerrer 2021 (secondary)" | SC-NMC83 부피변화 5.5 % | docs/a10_cycle_chemomech_design.md:25 (1) | **B** | 실재: Doerrer … Grant, ACS AMI 13, 37809 (2021) SC-NMC/Li6PS5Cl — 검색 요약 "5.5 % volume change" 로 일치 (미확인) | — |
| 50 | **Mayer 2022** — "Mayer 2022 \"inner CB porosity\"" | 분산상태를 전극 미세구조 파라미터로 정량화 | docs/additive_test_campaign.md:304 (1) | **B** | 실재: Mayer · Bockholt · Kwade, JPS 529, 231259 (2022) "Inner carbon black porosity as characteristic parameter…" (검색) | — |
| 51 | **McClelland 2023** — "McClelland 2023 Chem.Mater." | operando µSR 격자 D ≈ 3.4e-11 cm²/s | docs/ncm_sc_poly_electrochem_anchors.md:33 (1) | **B** | 실재: McClelland 외, Chem. Mater. 35, 4149 (2023) operando µSR NMC811 (검색). 수치 미확인 | — |
| 52 | **Naik 2025** — "Naik 2025 aenm.202403360" | 127.6→109.1 Ω (압력 17× → 17 %↓), SC-NMC532/LPSCl | docs/rint_reference_growthlaw_design.md:74 (1) | **B** | 실재: Naik 외, AEM 2025 "Interrogating the Role of Stack Pressure in Transport-Reaction Interaction…" — SC-NMC532/LPSCl 소재 일치 (검색). 수치 미확인 | — |
| 53 | **Schwartz 2004** — 같은 문장의 "Makse, Gland, Johnson, Schwartz (2004 …)" | Makse 2004 와 같은 인용 | docs/electronic_conductivity_derivation.md:100 (1) | **B** | Makse 2004 행과 같음 | — |
| 54 | **Singer 2023** — "\"Drying process of sulfide-based ASSB components\" Singer 2023 Energy Technol. 10.1002/ente.202300098" | 극성 용매 노출 시 σ_ionic ~1/100 이하 (여러 문헌 묶음) | docs/literature_dry_assb.md:369 (1) | **B** | 실재: Singer · Kopp · Aruqaj · Daub, Energy Technol. 11 (2023) (검색) — 건조 공정·점착 논문. "1/100" 수치는 이 논문으로 미확인 | — |
| 55 | **Sources 2024** — "J. Power Sources 2024 — …pii/S0378775324003173" | NCM@LPO 복합 90.48 % @200 cyc @0.5C | docs/rint_anchor_db_research.md:86 (1) | **B** | 실재: JPS 2024 "Regulating and understanding the compatibility of sulfide composite solid-state electrolyte in nickel-rich lithium metal batteries" (검색). 수치 미확인 | — |
| 56 | **Tech 2024** — "Powder Tech 2024 S0032591024010957" | PTFE 피브릴 계층 형태 | docs/cbd_morphology_roadmap.md:14 (1) | **B** | 실재: Powder Technol. 2024 "Effect of active material morphology on PTFE-fibrillation, powder characteristics and electrode properties in dry electrode coating processes" (검색) | — |
| 57 | **Tron 2023** — 동료 표 "Tron 2023 VGCF ≤0.4 / C65 ≤70" | 복합양극 σ_e 상한 (mS/cm) | docs/session_20260923_progress.md:121 (1) | **B** | 후보: Nanomaterials 13, 327 (2023) "Rational Optimization of Cathode Composites for Sulfide-Based ASSBs" — C65 vs VGCF 비교 (검색). 동료 표의 수치 미확인 (2차 인용) | — |
| 58 | **Zhang 2017** — README §6 "Zhang 2017 ACS AMI (Tier 1, LCO/LGPS composition sweep)" | LCO(LNTO 코팅)+LGPS 조성 A–D, d_diff, 유지율 | docs/literature_coverage/README.md:179 (1) | **B** | 실재: Zhang … Janek, ACS AMI 2017 (검색). 표 수치 미확인 | — |
| 59 | **Moulinec-Suquet 1998** — FFT 균질화 · 주석 "σ_0 > σ_max/3" | — | docs/Reviewer_Defence_Notes.md:255 · docs/Tabor_framework_reference.md:243 · docs/paper_brittle_caveat.md:2371,2430 · scripts/fft_homogenize.py:171 (5) | **C** | CMAME 157, 69 (1998) 정합. 주석의 수렴조건은 표준(σ_max/2)과 다르나 구현 σ_0 = (σ_min+σ_max)/2 는 표준 선택 — 무해 | — |
| 60 | **Yovanovich 1982** — R_c = ψ/(2ka) 의 자리 (p.86 식 1–3) | — | docs/reviews/codex_verdict_area_contract_20260913.md:219 · docs/reviews/codex_verdict_area_round2_20260913.md:87,287 · docs/session_20260911_progress.md:582 · scripts/network_conductivity.py:431 (5) | **C** | Yovanovich, AIAA Prog. Astronaut. Aeronaut. 83 (1982) 로 추정. 리포 Codex 판정문이 원문 p.86 대조를 기록. 원장 L2-01 (open, ψ 위치) 이 이 인용을 이미 추적 | — |
| 61 | **Mikić 1974** — "Mikić 1974" 주석 (ψ 보정 Holm 저항) | — | docs/reviews/codex_verdict_dem_stack_L2_20260913.md:65 · docs/reviews/review_before_after.html:246 · scripts/build_review_before_after.py:51 (4) | **C** | Int. J. Heat Mass Transfer 17 (1974) 로 추정. 적용 범위 문제는 원장 L2-01 (open) · Codex L2 판정문이 추적 | — |
| 62 | **Peaceman 1978** — PEACEMAN_B_FRAC = 0.2 (r_o = 0.2·Δx) | — | docs/reviews/codex_review_response_20260816.md:142 · docs/reviews/review_request_20260816.md:111 · scripts/fibre_1d_network.py:210,230 (4) | **C** | SPE J. 18(3), 183 (1978) 정합. 0.2Δx 는 고전 결과 (원문 대조 안 함); 코드가 스스로 "얇은 선원 전제 위반" 을 경고 | — |
| 63 | **Sulsky 1994** — MPM 원전 | — | docs/literature_coverage/pdfs/Klar_2016_ACMTOG_DruckerPrager_SandAnimation.txt:98 · docs/literature_review_dem_mpm_assb.md:218,221 · scripts/seminar_deck/build.js:647 (4) | **C** | 정본 klar2016 · devaucorbeil2020 · stomakhin2013 카드가 원전으로 인용 | — |
| 64 | **Eyre-Milton 1999** — 고대비 가속 FFT | — | docs/paper_brittle_caveat.md:2392,2449 · scripts/fft_homogenize.py:85 (3) | **C** | Eur. Phys. J. Appl. Phys. 6, 41 (1999) 정합 | — |
| 65 | **Mikic 1974** — "R = (1 − a/r_min)^1.5/(2a) — Mikic (1974) · Rigorous correction" | — | docs/voxel_contact_free_gap.md:40 · scripts/network_conductivity.py:410,501 (3) | **C** | 같은 인용. "rigorous" 는 과장 — ψ 근사는 0<a/b≤0.3 한정 (Codex 가 Yovanovich 1982 원문으로 지적, L2-01) | — |
| 66 | **Bernal 1960** — ε_pure_AM = 0.36 | — | scripts/predict_porosity_final.py:29 · scripts/predict_porosity_strict_physics.py:9 (2) | **C** | Bernal & Mason 1960 (Nature) 로 추정 — 고전값 | — |
| 67 | **Bernal 1965** — EPS_RCP = 36.0 % (mono RCP) | — | scripts/fit_porosity_physics_decomposition.py:68,171 (2) | **C** | RCP 공극 ≈ 0.36 은 고전값. 다른 스크립트는 같은 값을 "Bernal 1960" 으로 적음 | — |
| 68 | **Glover 2010** — Additive Bruggeman (m = 1.5) | — | docs/thermal_conductivity_derivation.md:40 · scripts/thermal_regression.py:1394 (2) | **C** | Geophysics 75(6) 일반화 Archie 법칙으로 추정 — 방법 인용 | — |
| 69 | **Storakers-Fleck-McMeeking 1999** — SFM KC framework | — | scripts/predict_porosity_final.py:33 · scripts/predict_porosity_physics.py:9 (2) | **C** | JMPS 47 (1999) 785 — 연도 정합 (감사 C D2 의 올바른 서지) | — |
| 70 | **Yu-Standish 1987** — trimodal RCP | — | scripts/predict_porosity_physics.py:6,70 (2) | **C** | Powder Technol. (1987) 로 추정 — 방법 인용 | — |
| 71 | **Yu-Standish 1991** — LPM (탐색 스캐폴드) | — | scripts/predict_porosity_yu_standish.py:5,49 (2) | **C** | Ind. Eng. Chem. Res. 30, 1372 (1991) 정합 | — |
| 72 | **Contacts 1967** — "Holm, Electric Contacts (1967)" (세미나 덱) | — | scripts/seminar_deck/build.js:323 (1) | **C** | Holm 4판 Springer 1967 정합 (refs.bib Holm1967 은 @article·journal=Springer-Verlag — 형식 오류만) | — |
| 73 | **Cundall 1979** — "Cundall & Strack 1979" (세미나 덱) | — | scripts/seminar_deck/build.js:646 (1) | **C** | Géotechnique 29, 47 (1979) 정합 (refs.bib CundallStrack1979 도 같음) | — |
| 74 | **Methods 2001** — "Bard & Faulkner, Electrochemical Methods (2001)" (세미나 덱) | — | scripts/seminar_deck/build.js:418 (1) | **C** | 2판 Wiley 2001 정합 | — |
| 75 | **Newman 1962** — "Newman & Tobias (1962)" tanh(ν)/ν | — | webapp/predictor_engine.py:924 (1) | **C** | JES 109, 1183 (1962) — 방법 인용 | — |
| 76 | **Newman 1994** — "Fuller, Doyle, Newman (1994)" 이용률 식 | — | webapp/predictor_engine.py:924 (1) | **C** | JES 141, 1 (1994) — 방법 인용 | — |
| 77 | **Powell 1979** — φc ∈ [0.15, 0.30] 적합 경계 | — | scripts/fit_constrained.py:16 (1) | **C** | PRB 20, 4194 (랜덤 충전 구의 site percolation) — 주석의 "overlap-sphere" 는 부정확, 경계는 리포 적합값 | — |
| 78 | **Yu 1987** — "Yu & Standish 1987 modified-mode multimodal packing" | — | scripts/predict_porosity_physics.py:72 (1) | **C** | 방법 인용 | — |
| 79 | **Yu 1991** — "Yu, A.B. & Standish, N. Ind. Eng. Chem. Res. 30 (1991) 1372" | — | scripts/predict_porosity_yu_standish.py:21 (1) | **C** | 서지 정합 | — |
| 80 | **Yu 1996** — "Yu, Zou & Standish. Ind. Eng. Chem. Res. 35 (1996) 3730" | — | scripts/predict_porosity_yu_standish.py:22 (1) | **C** | 서지 정합 | — |
| 81 | **Yu-Zou-Standish 1996** — 3-파라미터 개정판 | — | scripts/predict_porosity_yu_standish.py:12 (1) | **C** | Ind. Eng. Chem. Res. 35, 3730 (1996) 정합 | — |
| 82 | **Cooper 2016** — TauFactor · τ = ε·D/D_eff | — | docs/literature_review_dem_mpm_assb.md:43,106,303 (3) | **C** | SoftwareX 5 (2016), PDF 가 리포 docs/literature_coverage/pdfs 에 있음. 정의 정합 | — |
| 83 | **Torquato 2002** — EMT 정본 교재 | — | docs/Reviewer_Defence_Notes.md:478,496,692 (3) | **C** | Springer IAM 16 (2002) 정합 (main.tex · refs.bib 도 같음). refs.bib note 의 "proof" 는 [0,1] 가중평균이라는 사소한 사실 | — |
| 84 | **AlexNet 2012** — CNN 계보 | — | machine-learning/lectures/lecture17-cnn-architectures.md:5,15 (2) | **C** | ML 강의노트 — ILSVRC 연도 정합 | — |
| 85 | **Bergman 1978** — Bergman–Milton 경계 | — | docs/Reviewer_Defence_Notes.md:496,689 (2) | **C** | Phys. Rep. 43, 377 (1978) 정합 (main.tex · refs.bib 도 같음) | — |
| 86 | **Deiseroth 2008** — t₊ ≈ 1 (doi:10.1002/anie.200703900) | — | docs/data/lpscl_electrolyte_params.md:23,32 (2) | **C** | Li-argyrodite 원전 DOI 정합; t₊≈1 은 일반 서술 | — |
| 87 | **GoogLeNet 2014** — CNN 계보 | — | machine-learning/lectures/lecture17-cnn-architectures.md:6,54 (2) | **C** | ML 강의노트 — ILSVRC 연도 정합 | — |
| 88 | **Knauth 2009** — 입경–전도도 "교과서 설명" | — | docs/paper_brittle_caveat.md:928,1125 (2) | **C** | Solid State Ionics 180, 911 (2009) 총설로 추정 — 주장 대조 안 함 (같은 문장의 Wenzel 2016 은 M) | — |
| 89 | **Moulinec 1998** — "Comput. Methods Appl. Mech. Eng. 157: 69" | — | docs/Tabor_framework_reference.md:278 · docs/paper_brittle_caveat.md:2494 (2) | **C** | 서지 정합 | — |
| 90 | **ResNet 2015** — CNN 계보 | — | machine-learning/lectures/lecture17-cnn-architectures.md:6,80 (2) | **C** | ML 강의노트 — ILSVRC 연도 정합 | — |
| 91 | **SENet 2017** — CNN 계보 | — | machine-learning/lectures/lecture17-cnn-architectures.md:6,139 (2) | **C** | ML 강의노트 — ILSVRC 연도 정합 | — |
| 92 | **ZFNet 2013** — CNN 계보 | — | machine-learning/lectures/lecture17-cnn-architectures.md:5,32 (2) | **C** | ML 강의노트 — ILSVRC 연도 정합 | — |
| 93 | **Zheng 1990** — replacement regime (정성) | — | docs/Packing_Regime_Analysis.md:151,158 (2) | **C** | 충전 이론 정성 인용 | — |
| 94 | **Anseán 2022** — ICA best practice (10.3389/fenrg.2022.1023555) | — | docs/stage4_electrochem_research.md:93 (1) | **C** | Dubarry & Anseán, Front. Energy Res. 2022 DOI 정합 | — |
| 95 | **Brisard 2010** — "Comput. Mater. Sci. 49: 663" | — | docs/paper_brittle_caveat.md:2496 (1) | **C** | 서지 정합 | — |
| 96 | **Dauphin 2014** — saddle point 빈도 | — | machine-learning/lectures/lecture10-optimization-ii.md:25 (1) | **C** | ML 강의노트 — NeurIPS 2014 방법 인용 | — |
| 97 | **Doyle-Fuller-Newman 1993** — DFN (10.1149/1.2221597) | — | docs/stage4_electrochem_research.md:36 (1) | **C** | JES 140, 1526 (1993) DOI 정합 | — |
| 98 | **Eyre 1999** — "Eur. Phys. J. Appl. Phys. 6: 41" | — | docs/paper_brittle_caveat.md:2495 (1) | **C** | 서지 정합 | — |
| 99 | **German 2014** — replacement regime (정성) | — | docs/Packing_Regime_Analysis.md:151 (1) | **C** | 충전 이론 정성 인용 | — |
| 100 | **Grey 2019** — "Märker/Grey 2019 (10.1021/acs.chemmater.9b00140)" | — | docs/stage4_electrochem_research.md:88 (1) | **C** | DOI 정합 (NMC811 사이클 구조·Li 동역학) | — |
| 101 | **ILSVRC 2012** — AlexNet ILSVRC 2012 우승 | — | machine-learning/lectures/lecture17-cnn-architectures.md:16 (1) | **C** | ML 강의노트 — 연도 정합 | — |
| 102 | **Jackson 2017** — "Jackson 2017 review (plastic contact mechanics)" | — | docs/literature_coverage/README.md:480 (1) | **C** | = Ghaednia … Jackson, Appl. Mech. Rev. 69, 060804 (2017) 로 추정 (제1저자 Ghaednia) — 읽을거리 목록 | — |
| 103 | **Jain 2011** — DFT 표 S1 의 Ref. S4 (build.js 메모) | — | docs/manuscript_draft/build.js:404 (1) | **C** | 서지 전문은 DFT 파트(다른 브랜치 `sdcp_dft_methods_build.js`)에 있어 이 브랜치에서 대조 불가 — 원고 인용이므로 그쪽에서 확인 필요 | — |
| 104 | **Marquis 2019** — SPMe | — | docs/stage4_electrochem_research.md:36 (1) | **C** | JES 166, A3693 (2019) — 방법 인용 | — |
| 105 | **O'Kane 2022** — SEI 파라미터 (할 일 메모) | — | docs/rint_reference_growthlaw_design.md:139 (1) | **C** | PCCP 2022 열화 모델로 추정 — 수치 인용 없음 | — |
| 106 | **Polyak 1964** — 모멘텀법 | — | machine-learning/lectures/lecture10-optimization-ii.md:59 (1) | **C** | ML 강의노트 — 방법 인용 | — |
| 107 | **Seok 2026** — "다음 추적: Seok 2026 AEM(aenm.202506351)" | — | docs/step5_cycle_degradation.md:70 (1) | **C** | 실재 확인: AEM 2026 "Decoupling Chemical and Mechanical Contributions to Capacity Fading in Ni-Rich Cathodes…" (검색) — 추적 메모만, 주장 없음 | — |
| 108 | **Springer 1967** — "R. Holm, Electric Contacts, 4th ed., Springer (1967)" | — | docs/seminar_20260806_glossary.md:183 (1) | **C** | 서지 정합 | — |
| 109 | **Sulzer 2021** — PyBaMM (10.5334/jors.309) | — | docs/stage4_electrochem_research.md:61 (1) | **C** | JORS 2021 DOI 정합 | — |
| 110 | **Wiley 2001** — "Bard & Faulkner, Electrochemical Methods, 2nd ed., Wiley (2001)" | — | docs/seminar_20260806_glossary.md:201 (1) | **C** | 서지 정합 | — |
| 111 | **Yovanovich 1998** — 원문 p.171–172 | — | docs/reviews/codex_verdict_area_round2_20260913.md:287 (1) | **C** | Codex 판정문의 원문 대조 기록 (2005 리뷰와 함께) | — |
| 112 | **Klár 2016** — "Klár 2016 … Drucker–Prager 원뿔 yield (DPC 원전)" · "(Klár 2016 friction …)" | — | docs/literature_review_dem_mpm_assb.md:41,216 · scripts/mpm_dem_match.py:226 (3) | **V** | 정본 klar2016 카드: ACM TOG 35(4) 103, DP 원뿔·Coulomb 마찰 — 일치. 단 Klár 는 cap 없는 DP 라 "DPC 원전" 은 느슨한 표현 | — |
| 113 | **Batteries 2023** — "Reisacher, Kaya, Knoblauch — Batteries 2023, 9(12), 595" | — | docs/reviews/fable_selfreview_request_20260909.md:207 · scripts/grade_engine.py:1699 (2) | **V** | 정본 reisacher2023 카드: DOI 10.3390/batteries9120595 · 저자 일치 | — |
| 114 | **GeoDict 2023** — "GeoDict 2023 (Math2Market)" — Koo 2026 · Lim 2025 · Yoo 2026 · Bak 2024 요약 | — | docs/lit_bak2024_binder_distribution_multilayer.md:138,390 · docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md:49,187,403 · docs/lit_koo2026_swcnt_sheath_thick_electrode.md:229,497,498 · docs/lit_lim2025_virtual_calendering_framework.md:126 · docs/lit_yoo2026_porosity_gradient_dry_electrode.md:196 · docs/literature_yonsei_dtbl_2026.md:462,514,634 (13) | **V** | 정본 koo2026 · lim2025 · yoo2026 · bak2024 카드가 같은 판본 "GeoDict 2023" 을 기록 (소프트웨어 인용) | — |
| 115 | **GeoDict 2022** — "GeoDict 2022" — Koo 2025 · Lee 2023 요약 | — | docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md:49,184,187,194,310,403… · docs/lit_lee2023_sicspe_digitaltwin_assb.md:87,260 · docs/literature_yonsei_dtbl_2026.md:514,516,538 (12) | **V** | 정본 koo2025 · lee2023 카드 "GeoDict 2022" 일치 | — |
| 116 | **GeoDict 2025** — "GeoDict 2025 … voxel 0.01 µm" — Hong 2026 CBD · Kim 2026 A3D | — | docs/lit_hong2026_cbd_viscoelasticity_springback.md:119 · docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md:71,119,131,132 · docs/literature_yonsei_dtbl_2026.md:329 (6) | **V** | 정본 hong2026_cbd · kim2026_a3d 카드 일치 (voxel 0.01 µm 포함) | — |
| 117 | **GeoDict 2020** — "GrainGeo module in GeoDict 2020" (직접 인용) — Park 2020 | — | docs/lit_park2020_digitaltwin_assb_foundational.md:101,259,455 · docs/positioning_vs_geodict.md:128 (4) | **V** | 정본 park2020 카드 일치 | — |
| 118 | **Joule 2026** — "#275 (Koo, Joule 2026)" | — | docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md:1,15,465 · docs/literature_yonsei_dtbl_2026.md:500 (4) | **V** | 정본 koo2026 카드: Joule 10, 102392 (10.1016/j.joule.2026.102392) | — |
| 119 | **Song 2023** — "E_NCM622 = 2.61 GPa (ref 4 = Song 2023, AEM)" · "Lim E_NCM622 2.61 도 … Song 2023 유래" | — | docs/lit_lim2025_virtual_calendering_framework.md:132 · docs/literature_yonsei_dtbl_2026.md:185 · docs/positioning_in_dt_lineage.md:388,467 (4) | **V** | 정본 lim2025 카드 SI Table S4 "E_NCM622 = 2.61 GPa (ref 4 = Song 2023, AEM)". positioning:388 의 2.611 · σ_y 0.1534 · ν 0.25 는 정본 song2025 카드(NMC711 나노압입) 값 | — |
| 120 | **Zhang 2024** — "electromechanical-contact (Zhang 2024) R_c = (ρᵢ+ρⱼ)/(4r_c) = the Holm model" | — | docs/literature_review_dem_mpm_assb.md:40,88,194,281 (4) | **V** | 정본 electromechanical_contact_model_particulate_systems 카드 (Chao Zhang, Powder Technol. 2024): eq 12 Holm, 단상이면 1/(2σr_c) 와 정확히 일치 | — |
| 121 | **Kato 2018** — "Kato 2018 재구성 (LCO+LGPS+AB) 0.68 vs 0.73" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:196,463 · docs/literature_coverage/README.md:482 (3) | **V** | 정본 bielefeld2020 카드 일치 | — |
| 122 | **Magazine 2024** — "E.Chem Magazine 2024 digital-twin review" | — | docs/lit_choi2024_digital_twin_review_echem.md:11,553 · docs/literature_yonsei_dtbl_2026.md:824 (3) | **V** | 정본 choi2024_digital_twin_review_echem 카드: E.Chem 매거진 Vol.16 No.1 | — |
| 123 | **Nam 2018** — "Nam et al. 2018 (NCM622:LPSCl:C65:NBR)" · "Nam 2018 JPS (dry vs slurry)" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:26,263 · docs/literature_coverage/README.md:479 (3) | **V** | 정본 bielefeld2020 카드: 실험 비교점 Nam 2018, GITT, 접촉면적 overlay | — |
| 124 | **Vaucorbeil 2020** — "de Vaucorbeil 2020 … MPM 25년 리뷰 (339 ref)" | — | docs/literature_review_dem_mpm_assb.md:217,221,294 (3) | **V** | 정본 devaucorbeil2020 카드: Adv. Appl. Mech. 53, 185–398, 339 ref | — |
| 125 | **Wiegmann 2006** — "EJ-HEAT 솔버 (Wiegmann & Zemitis 2006, ref 50)" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:29,108,490 (3) | **V** | 정본 bielefeld2020 카드 일치 | — |
| 126 | **Bosch 2014** — "Shenouda 2020/Bosch 2014 (LIGGGHTS 튜토리얼)" | — | docs/literature_review_dem_mpm_assb.md:36,232 (2) | **V** | 정본 boschpadros2014 카드: Swansea MSc 2014, LIGGGHTS 방법론 | — |
| 127 | **Braun 2018** — "ρ_AM/SE = 40 Ω·cm² (Braun 2018)" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:23,118 (2) | **V** | 정본 bielefeld2020 카드 일치 | — |
| 128 | **Franco 2026** — "Zhang/Meng/Franco 2026 (Nature Energy)" | — | docs/data_inventory_20260825.md:298 · docs/plan_vgcf_ptfe_coupling_20260811.md:1 (2) | **V** | 정본 zhang2026_dryprocess_electrode_architecture 카드: Nature Energy 2026, 10.1038/s41560-026-01981-3, 저자에 Chouchane · Franco · Shpyrko · Meng | — |
| 129 | **GeoDict 2024** — "GrainGeo (GeoDict 2024)" — Hong 2026 바인더 디지털트윈 | — | docs/lit_hong2026_sulfide_cathode_binder_digitaltwin.md:104,446 (2) | **V** | 정본 hong2026_sulfide_cathode_binder_digitaltwin 카드 일치 | — |
| 130 | **Lim 2023** — "Hyobin Lee·Jaejin Lim (2023+ 디지털트윈 모델러)" | — | docs/lit_park2020_digitaltwin_assb_foundational.md:433 · docs/literature_yonsei_dtbl_2026.md:28 (2) | **V** | 정본 lee2023 카드 저자에 Hyobin Lee · Jaejin Lim (kim2024 카드도) | — |
| 131 | **Lischka 2023** — "Lischka & Nirschl 2023 [85] 세트 {G 1e8 · ρ 2500 · d 2 mm · μ_s 0.9 · γ 0.25/0.04 …}" | — | docs/reviews/mixing_model_design_20260919.md:968 · docs/reviews/self_review_mixer_20260921.md:121 (2) | **V** | 정본 hare2026 카드: DEM 파라미터 출처 [85] Lischka & Nirschl, Energy Technol. 2023 — 세트 값 일치 | — |
| 132 | **Amira 2019** — "Amira 2019.1 + Fiji 재구성" | — | docs/lit_doux2020_stack_pressure_assb.md:95 (1) | **V** | 정본 doux2020 카드 일치 (소프트웨어 판본) | — |
| 133 | **Boyce 2022** — "K_IC(NCA) … γ = 1 J/m² 차용 — Boyce 2022 (NMC 모델)" | — | docs/nca_material_preset.md:34 (1) | **V** | 정본 kang2025_toughened_bimodal 카드: "G_c 1 J/m² — ref [S4] Boyce 2022" | — |
| 134 | **Brodu 2015** — "Brodu 2015 (같은 축 유일 경쟁자 + 다입자 광탄성 실측)" | — | docs/session_20260825_dem_litdb_progress.md:408 (1) | **V** | 정본 giannis2021 카드: Brodu · Dijksman · Behringer, PRE 91, 032201 (2015) MC-strain. "광탄성 실측" 은 카드에 없음 | — |
| 135 | **CNT-wrapping 2025** — "Koo 그룹 CNT-wrapping (2025 ESM …)" | — | docs/lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md:381 (1) | **V** | 정본 koo2025 카드: ESM 78, 104270 (99.6 wt%, 4.0 g/cm³ 포함) | — |
| 136 | **Energy 2018** — "Wang Nat. Energy 2018 [36]" (Choi 2026 요약) | — | docs/lit_choi2026_elastomeric_li_metal_anode.md:67 (1) | **V** | 정본 choi2026_elastomeric_li_metal_anode 카드 같은 문장 | — |
| 137 | **Froboese 2019** — "τ² abruptly rises … (Froboese 2019 일치)" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:192 (1) | **V** | 정본 bielefeld2020 카드 일치 | — |
| 138 | **GeoDict 2018** — "GeoDict 2018 SP5" — Bielefeld 2019 | — | docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md:280 (1) | **V** | 정본 bielefeld2019 카드 "Version 2018 SP 5, ref 30" 일치 | — |
| 139 | **GeoDict 2019** — "GeoDict 2019 SP2" — Bielefeld 2020 | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:324 (1) | **V** | 정본 bielefeld2020 카드 일치 | — |
| 140 | **Grieves 2000** — "Grieves 2000s 제조공정" | — | docs/positioning_in_dt_lineage.md:50 (1) | **V** | 정본 park2020 카드: "2000년대 Michael Grieves" | — |
| 141 | **Han 2021** — "ref 86 Han 2021, 88 % retention/200 cyc" | — | docs/lit_minnmann2022_designing_cathodes_solidstate.md:196 (1) | **V** | 정본 minnmann2022 카드 같은 서술 | — |
| 142 | **Harthong 2009** — "Harthong 2009 (IJSS 46:3357, 비국소 + 탄소성 + 고밀도)" | — | docs/session_20260825_dem_litdb_progress.md:408 (1) | **V** | 정본 demirtas2021 카드 [30] IJSS 46 (2009) 3357 고밀도 압밀 DEM · gonzalez2012 카드 (FEM 격자에서 소성 접촉법칙 적합) | — |
| 143 | **Letters 2024** — "그룹 자신의 ACS Energy Letters 2024 도구논문의 한국어 동반판" | — | docs/lit_choi2024_digital_twin_review_echem.md:16 (1) | **V** | 정본 kim2024_digital_twin_acsenergyletters 카드: 10.1021/acsenergylett.4c01931 | — |
| 144 | **Pantaleev 2017** — "FT4 보정이 맞았는데도 혼합속도는 정성적으로만 맞았다" | — | docs/reviews/mixing_model_design_20260919.md:247 (1) | **V** | 정본 jadidi2023 카드 Table 12 (Pantaleev 2017) 일치 | — |
| 145 | **Rabbani 2014** — "open-source (Rabbani 2014)" (PNM) | — | docs/lit_koo2026_swcnt_sheath_thick_electrode.md:233 (1) | **V** | 정본 koo2026 카드: "PNM = MATLAB + Rabbani 2014 오픈소스" | — |
| 146 | **Samsung 2024** — "interfacial-impedance (Choi/Samsung 2024) TLM 분해" | — | docs/literature_review_dem_mpm_assb.md:80 (1) | **V** | 정본 interfacial_impedance_formulation_assb_cathode 카드: Choi 외 (SAIT), ACS AMI 16, 26066 (2024), TLM | — |
| 147 | **Shi 2020** — "SE 잘게·AM 굵게 = 이온 최적, Shi 2020 권고" | — | docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md:361 (1) | **V** | 정본 shi2019_high_am_loading 카드 (AEM 2019/2020, 1902881): "SE 를 CAM 보다 작게 (λ↑)" | — |
| 148 | **Sources 2022** — "so2022 (J. Power Sources 2022, litdb 정본) … >90 % @25 MPa … AM perc 0.3 @25 → 1.0 @100 MPa" | — | docs/reviews/mixing_model_design_20260919.md:818 (1) | **V** | 정본 so2022_dem_compaction_coated_particles 카드: JPS 530, 231279 — 수치 일치 | — |
| 149 | **Vu-Quoc 2001** — "[24] = Vu-Quoc 2001 (= 층①②)" | — | docs/session_20260825_dem_litdb_progress.md:338 (1) | **V** | 정본 demirtas2021 카드: "[24] = Vu-Quoc 2001" | — |
| 150 | **Worlds 1991** — "Gelernter Mirror Worlds 1991" | — | docs/positioning_in_dt_lineage.md:50 (1) | **V** | 정본 park2020 카드: 디지털트윈 계보 Gelernter Mirror Worlds (1991) → Grieves | — |
| 151 | **Zeier 2020** — "Round-robin (ref 23, Ohno/Zeier 2020 interlab study) … 같은 합성 배치" | — | docs/lit_cronau2021_stack_pressure_ionic_conductivity.md:96 (1) | **V** | 정본 ohno2020 카드: ACS Energy Lett. 2020 round robin, "같은 배치 argyrodite 5종 × 8 데이터셋" | — |

### 2-b. NOISE 96 키 (인용 아님)

| 이유 | 키 (건수) |
|---|---|
| 원고 이력 날짜(Received/Revised/Accepted/Published/Copyright) — 인용 아님 | Accepted 2020 (1), Accepted 2021 (1), Accepted 2024 (1), Accepted 2025 (1), Copyright 2020 (1), Published 2018 (1), Published 2020 (1), Published 2021 (1), Published 2022 (1), Published 2023 (1), Received 2018 (1), Received 2019 (2), Received 2020 (2), Received 2021 (2), Received 2022 (2), Received 2024 (2), Revised 2018 (1), Revised 2019 (1), Revised 2020 (1), Revised 2022 (2) |
| 상태 표기 + 날짜 (문서 이력 헤더) — 인용 아님 | ADAPTIVE 2026 (1), Adopted 2026 (2), ADOPTED 2026 (2), Aligned 2026 (1), ATTRIBUTION 2026 (1), BUILT 2026 (6), CHANGED 2026 (1), CHECK 2026 (1), CLOSE-OUT 2026 (4), CLOSED 2026 (15), COMPLETE 2026 (2), CONFIRMED 2026 (1), CONVERGENCE 2026 (1), CORRECTED 2026 (1), CORRECTION 2026 (1), CORRECTIONS 2026 (1), Created 2026 (1), CROSS-CHECK 2026 (1), CROSS-VALIDATION 2026 (1), Excluded 2026 (1), EXHAUSTED 2026 (1), FINALIZED 2026 (2), GPU-CONFIRMED 2026 (1), GRID-CONVERGENCE 2026 (1), HISTORICAL 2026 (2), IMPORTANT 2026 (2), LOGIC 2026 (1), MERGE 2026 (1), MOMENT 2026 (1), PENDING 2026 (1), PREFERRED 2026 (1), REFINEMENT 2026 (1), RESOLVED 2026 (2), RETIRED 2026 (1), SOLUTION 2026 (1), STATUS 2026 (1), STRIP 2026 (1), SUPERSEDED 2026 (2), SUPPRESSION 2026 (1), TIMELOG 2026 (1), UNCHANGED 2026 (1), UPDATE 2026 (3), USABLE 2026 (1), VALIDATION 2026 (1) |
| 날짜 'Apr-2026' (재적합 시점 주석) — 인용 아님 | Apr- 2026 (1) |
| 날짜 'Aug 2026' (세미나 덱 프레임 부제) — 인용 아님 | Aug 2026 (1) |
| 제3자 논문 원문 추출 텍스트(docs/literature_coverage/pdfs/Klar_2016_…txt) 속 Klár 2016 자신의 참고문헌 — 리포 주장 아님 | Bardenhagen 2000 (2), Bell 2005 (1), Bonet 2008 (3), Chang 2012 (1), Chen 2013 (1), Cummins 2002 (1), Drucker 1952 (2), Gast 2015 (1), Imhsen 2013 (1), Jiang 2015 (9), Laenerts 2009 (1), Macklin 2014 (2), Mast 2013 (5), Mast 2014 (2), Mazhar 2015 (1), Milenkovic 1996 (1), Miller 1989 (1), Narain 2010 (4), Nkulikiyimfura 2012 (1), Otaduy 2011 (2), Pla-Castells 2006 (1), Ram 2015 (1), Steffen 2008 (1), Stuart 2008 (1), Sumner 1999 (1), Wood 2008 (1), Yasuda 2008 (1), Yue 2015 (1), Zhu 2005 (2) |
| 혼합기 상표 + 회전수 ('Thinky 2000 rpm') — 인용 아님 | Thinky 2000 (2) |

## 3. 원고에 걸리는 것

**3-1. 원고 생성기 · 원고 파일**

| 파일 | 이번 키 | 판정 · 조치 거리 |
|---|---|---|
| `docs/manuscript_draft/build.js:404` | Jain 2011 (DFT 표 S1 의 Ref. S4 라고 적은 메모) | C. 서지 전문이 DFT 파트(`sdcp_dft_methods_build.js`, 다른 브랜치)에 있어서 이 브랜치에서는 대조할 수 없다 — 원고 인용이므로 그쪽에서 확인해야 한다 |
| `docs/manuscript_draft/build.js:116` | "DRAFT STATUS (2026-08-25 …)" | NOISE |
| 표 S2 (`build.js:198–206`, Ref. S6–S8) | 없음 | 이번 247 키는 표 S2 의 값과 출처(Sedlatschek · Sakuda · Cronau 2021)에 닿지 않는다. SI 번호도 build.js 안에서는 충돌하지 않는다 (DFT 표 S1 = S1–S5, DEM 표 S2 = S6–S8) |
| `docs/paper/main.tex` · `refs.bib` | Bergman 1978 (:875) · Torquato 2002 (:877) · Cundall–Strack 1979 (:109, :237) · Holm 1967 | 전부 C (서지 정합). 사소한 것 둘 — ① `refs.bib` Holm1967 이 `@article` 에 `journal = {Springer-Verlag}` (책인데 형식이 틀림) ② Torquato2002 의 note 가 "[0,1] 가중평균은 [0,1] 안에 있다는 증명" 을 이 책의 몫으로 적는다 (사소한 수학 사실이지 이 책의 결과가 아니다) |
| `docs/manuscript/Methods_simulation_v7_for_coauthors.docx` (+ `.md` 초안) | 없음 | docx XML 을 풀어서 확인 — 이번 키가 하나도 없다 |
| `docs/paper/main.tex:659` · `:710` · `:1013` | "Yu–Standish 1996 multimodal RCP" (향후 확장으로 인용) | **M** (주제) — 1996 판(Yu · Zou · Standish, Ind. Eng. Chem. Res. 35, 3730)은 **비구형** 입자 혼합물 모델이다. 다성분 구 충전 모델은 1991 판(30, 1372). `144e18b60` (05-13) |
| `docs/paper/main.tex:563` (+ `:910` "α_KC = 2.0 from \citet{Sridhar2000}") | "Sridhar–Fleck–McMeeking constraint factor with α_KC = 2 \citep{Sridhar2000}" | **M(서지)** — :563 은 두 논문의 저자명을 섞은 이름 (스크립트 키 Sridhar-Fleck-McMeeking 2000 과 같음). α = 2 의 원문 근거는 감사 C D1 에서 미확인. `144e18b60` |
| `docs/paper/refs.bib:225` (`Storakers2000`, main.tex:569) | "JMPS 48 (2000) 785–815" | **M(서지)** — 실제 JMPS **47 (1999)** (감사 C D2; 문서 키 Storåkers-Fleck-McMeeking 2000 과 같은 오기) |

**3-2. 원고 후보 초안 · 반박 노트** (원고 파일은 아니지만 원고 문장의 공급원)

- `docs/paper_brittle_caveat.md` (머리말 "Paper Caveat — Working draft", 원고 5-1 절 영·한 초안):
  **Solid Power 2023 (F, 5 곳)** · **Wenzel 2016 (M, 2 곳)** · Knauth 2009 (C) · Moulinec–Suquet 1998 · Eyre–Milton 1999 · Brisard 2010 (C, 서지 정합).
  같은 문장의 "Cronau 2022 … D50 5–10 µm → <0.3 µm ≈ 1/3" 은 다른 감사 소관이지만, 정본 cronau2022 카드(σ 는 입경이 아니라 밀링 손상을 따른다)와 충돌한다.
- `docs/Reviewer_Defence_Notes.md` (반박 노트): **Grießer 2021 (F)** · **Birkholz 2022 (U)** — 노트는 이 둘을 "paper Sec 5-1" 인용이라고 적지만 main.tex/refs.bib 에 없다. Torquato 2002 · Bergman 1978 · Moulinec–Suquet 1998 은 C.

**3-3. 웹앱 — 사용자에게 보이는 것**

| 위치 | 이번 키 | 판정 | 어떻게 보이나 |
|---|---|---|---|
| `webapp/templates/step5.html:35` | "Nature2025 Ni≥85" | **M(서지)** | STEP5 패널 문구. 실제 *Nature Energy* 10, 479 (2025); "Ni≥85" 문턱은 미확인 |
| `scripts/grade_engine.py:152` → 등급 가이드 (`app.py:892`, `/results/<id>/grade-guide` "자세히 (기술적 근거)") | Mukhopadhyay 2014 | **F** | 좌표수 축 설명문 |
| `scripts/grade_engine.py:435` → 같은 경로 | ScienceDirect 2021 (ESM 2021 ORNL) | **B** | P:S 7:3 밴드 설명문 — "7:3 최적" 은 이 논문으로 확인되지 않는다. 같은 문자열의 "Lee 2025 ACS EL" 은 감사 B 가 실제 Oh 2026 으로 판정했다 |
| `webapp/predictor_engine.py:948–949` | Kato 2016 · (Sakuda 2017) | **M** · (U) | 주석이지만 j₀ = 0.01 mA/cm² 가 이용률 예측값에 들어간다 |
| `webapp/predictor_engine.py:827` · `:865` · `:924` | Clausnitzer 2023 (B) · Kang 2024 (U) · Newman 1962/1994 (C) | — | 주석 (값은 리포 자체 규칙) |
| `webapp/predictor_engine.py:51` · `webapp/app.py:1177, 6164, 6218` | CLOSED · SUPPRESSION · STRIP · MERGE 2026 | NOISE | — |

**3-4. 표 S2 값** — 이번 키 가운데 표 S2 값에 걸리는 것은 없다.
