<!-- digest 초판 2026-11-23 (논문 에이전트 · 대피 세션 — git 안 씀 · 이 파일과 litdb/figures/<slug>/ 만 썼다).
     쪽 표기 "p.N" = 인쇄 쪽 "N of 33" = PDF N 쪽 (표지 없음). SI 없음.
     ① PDF 33 쪽 텍스트 층 전문 정독 — 본문 p.1–26 · 참고문헌 p.27–32 (166 항목) · 저자 소개 p.32–33. 2단 조판이라 PyMuPDF 블록을 열 단위로 다시 엮어 읽었다 (scratchpad 에만).
     ② 크롭 23 장 = 도구 20 (그림 16 + 표 4) + 손 3 (`Fig. 5` p.9 · `Fig. 11` p.17 — 도구가 '영역 없음' 으로 놓친 번호 공백 · `Fig. 19` p.25 — **마지막 번호라 번호 공백 검사에도 안 걸린 누락**, 본문 'Figure 19' 참조로 찾았다).
        세 장 모두 래스터 한 장 (xref 228 · 312 · 395) 이고 자른 영역 안에 본문 글자 0 개 — figures.json 의 manual_crop 에 좌표 · 사유.
        figures.json 캡션 18 건 교정 (그림 14 · 표 4 — 도구 캡션에 본문 문장 · 쪽 꼬리말 · 표 칸이 붙어 있었다 — caption_fix 표시) · 전 항목에 viewed / viewed_how 표시.
     ③ 그림 **11 장 실독**: `Fig. 1` · `Fig. 2` · `Fig. 5` · `Fig. 7` · `Fig. 10` · `Fig. 11` · `Fig. 13` · `Fig. 15` · `Fig. 16` · `Fig. 18` · `Fig. 19`.
        안 본 것 8 장: `Fig. 3` · `Fig. 4` · `Fig. 6` · `Fig. 8` · `Fig. 9` · `Fig. 12` · `Fig. 14` · `Fig. 17` (액상 막 · 슈퍼커패시터 · 탈염 · 형상 사진 — 우리 축 밖. 캡션 + 본문만).
        표 4 장은 PNG 대신 PDF 텍스트 층 (PyMuPDF find_tables) 으로 전사했다.
     ④ 본문 대괄호 인용 ↔ 참고문헌 목록을 스크립트로 전수 대조 (166 번호 전부 본문에 나옴 · [6] = [25] 같은 책) + 주요 주장 ↔ 인용 항목 **제목 수준** 대조 (원 논문은 하나도 열지 않았다 — §10a).
     ⑤ 값 표지 — [리뷰] 리뷰 자신의 서술 · [2차 · ref N] 리뷰가 ref N 의 결과로 옮긴 값 (N = 리뷰 인쇄 번호) · [그림 인쇄] 그림 안에 찍힌 값 · `figure-read ≈` 그림에서 읽은 값 · [우리 산술] · [litdb 카드] 우리 litdb 다른 카드가 옮긴 문헌값 · [추정] 배경지식 · 원문 미대조.
     ⑥ 우리 계산값은 싣지 않았다 — 우리 쪽은 방법 · 정의 · 원장 위치로만 적는다 (값은 db/properties/canonical_registry.json → citation_hazards.json). 점착 W 값 0.
     ⑦ talk 인입 대기열 (`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → lee2026_skku_mlip_materials_design.md 하나) 에 이 논문 없음 → 역링크 없음. -->
# **MXene (2D 전이금속 탄화물 · 질화물)** 을 고체전지의 '이온전도 계면' 으로 — 고분자 복합 전해질 충전재 · Li/Na 금속 인터레이어 · 다가 이온 숙주를 묶은 리뷰: 자체 자료 0 · **황화물 SE 1차 사례는 MXene → Li₂TiO₃ 전환 코팅 하나** · 금속성 인터레이어와 '전자 차단 계면상' 을 같이 말하고 정리하지 않는다 · 그림–본문 어긋남 6 · 인용 어긋남 다수 — Pandey et al. (*The Chemical Record* 2026, e70267)

> slug `pandey2026_mxene_ion_conducting_interfaces_ssb_review` · DOI `10.1002/tcr.70267` · type `review (자체 자료 0 · 자체 계산 0 — "No new data were created or analyzed in this study" · 참고문헌 166 = 고유 165 · 그림 19 · 표 4 · 식 (1)–(8) + 반응식 (I)–(VII) · MXene–고분자 복합 전해질 · 금속 음극 인터레이어 · 다가 이온 숙주 · 황화물 SE 본문 5회 · Li₆PS₅Cl 0회)` · PDF `litdb/inbox/20fa5823-Two_Dimensional_MXenes_for_Ion_Conducting_Interfaces_in_Solid_State_Energy_Storage_Systems.pdf` (33 쪽 · SI 없음) · digested `2026-11-23` · status ✅ · 태그 **[외부]**
> elements: Ti, Nb, Mo, V, C, N, O, F, H, Cl, Br, Li, Na, K, Mg, Zn, Al
> methods: DFT, MD, ELF, XPS, ESW
>
> **저자 · 소속 (p.1)**: Raghvendra Pandey (ARSD College, Univ. of Delhi · 물리) · Anuja Dhingra · Ravinshu (Netaji Subhas Univ. of Technology · 물리) · Hera Tarique (ARSD College) · Sumanta Sahoo (Gachon Univ. · 화학) · **Rajesh Kumar\*** (TU Darmstadt, Institute of Materials Science · 교신).
> **매체 · 지위**: *The Chemical Record* (Chem. Soc. Japan + Wiley-VCH) · **REVIEW** · 투고 2026-07-29 · 수정 2026-09-19 · 수락 2026-10-16 · e70267 · 33 쪽 · 연구비 SERB-DST ECRA (ECR/2016/001151) · 이해충돌 없음 · "No new data were created or analyzed in this study" (p.27).
> ⛔ **이 리뷰의 수치는 전부 2 차 소환이다 — 원 논문 확인 없이 인용 금지.** 리뷰가 단 인용 번호가 그 주장과 제목 수준에서 안 맞는 곳이 많다 (§10a). 쓸모는 **MXene 쪽 원전 목록**과 **'금속성 인터레이어 대 전자 차단 계면상' 이라는 질문**이다.
> **우리 축과의 거리**: 멀다. 황화물 argyrodite · Li₆PS₅Cl · 수분 · H₂S · 스택 압력 · 임계전류밀도 모두 본문 0 회. 걸리는 것은 (i) 금속성 MXene 을 황화물 계면에 놓을 때의 전자 경로 (§11-1), (ii) MXene → Li₂TiO₃ 전환 코팅 ([107] · [혁주] LZO 트랙과 같은 Li₂MO₃ 계열, §11-2), (iii) −OH 말단 · 친수성 = 황화물에는 위험 (§11-3) 셋이다.
> **정본 litdb 이웃 (링크만)**: [`spencerjolly2023_ag_graphite_interlayer_operando_xrd`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) (전자전도 Ag–흑연 인터레이어 · anodeless Li₆PS₅Cl) · [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (탄소 인터레이어 ↔ LPSCl 접착이 Li 석출 위치를 정한다) · [`kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode`](kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md) · [`liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl`](liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl.md) (절연 유전체 양극 계면층 · 건식 LPSCl) · [`kim2026_hts_li3sc2po43_coating_midni_ncm`](kim2026_hts_li3sc2po43_coating_midni_ncm.md) (Li₂TiO₃ 의 LPSCl 반응에너지 행) · [`kim2026_moisture_surface_degradation_lpscl_dryroom`](kim2026_moisture_surface_degradation_lpscl_dryroom.md) (LPSCl 가수분해) · [`zhu2015_esw_grand_potential_origin`](zhu2015_esw_grand_potential_origin.md) · [`schwietert2021_intrinsic_vs_decomposition_window_sse`](schwietert2021_intrinsic_vs_decomposition_window_sse.md) (LPSCl 창) · [`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`](haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md) (공간전하 DFT 원전) · [`alharbi2026_coupled_design_ultrathin_composite_se_review`](alharbi2026_coupled_design_ultrathin_composite_se_review.md) (형제 리뷰 · 고분자 복합막) · [`luo2026_lis_separator_crystal_engineering_review`](luo2026_lis_separator_crystal_engineering_review.md) (MXene 분리막 · 액체 Li–S).
> **본 digest 에서 실제로 본 그림 (2026-11-23)**: `Fig. 1` `Fig. 2` `Fig. 5` `Fig. 7` `Fig. 10` `Fig. 11` `Fig. 13` `Fig. 15` `Fig. 16` `Fig. 18` `Fig. 19` — **11 장**. 안 본 것: `Fig. 3` `Fig. 4` `Fig. 6` `Fig. 8` `Fig. 9` `Fig. 12` `Fig. 14` `Fig. 17` (캡션 · 본문만) · `Table 1`–`Table 4` (PDF 텍스트로 전사). 그림에서만 읽은 값은 **`figure-read ≈`**, 그림에 글자로 찍힌 값은 **[그림 인쇄]**.

---

## 0. 결론 먼저 — 우리 질문 다섯에 대한 답

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 무엇을 주장하나** | MXene 이 고체전지에서 세 역할 — **이온수송 조절자** (고분자 전해질 충전재) · **계면 개질자** (Li/Na 금속 · 양극 쪽 완충층) · **다가 이온 숙주** (Zn²⁺ · Mg²⁺ · Al³⁺) — 를 한다는 것. 리뷰가 내세우는 새로움은 '이온전도 계면' 에 초점을 맞춘 점 (p.2) | 초록 · §1 · `Fig. 1` · `Table 1` |
| **Q2 우리 축 (황화물 argyrodite DFT) 에 걸리나** | **거의 안 걸린다.** 황화물 SE 1차 사례는 **하나** — Ti₃C₂Tₓ 를 LiCoO₂ 위에서 Li₂TiO₃ 로 바꾼 코팅 ([107] · "up to 4.5 V") 이다. Li₆PS₅Cl · argyrodite 0 회 · "sulfide-based conductors" 의 인용 [129–131] 은 **Li–S 전지 · Zn 음극 논문** · 수분 · H₂S 0 회 | §4 p.12 · §6 p.17 · §10a |
| **Q3 계산은** | 자체 계산 0. 인용 수치는 흡착 · 결합에너지 (`Fig. 7` [그림 인쇄] · `Fig. 13g`) · "Li⁺ 결합 −1.2 ~ −2.5 eV · 이동 장벽 ≈0.2–0.4 eV" (출처 [18] 은 Chem. Rev. 리뷰 → 3 차) · ELF 그림 한 장 (**색 막대 없음**) · MD (`Fig. 14` · 액상 막). **범함수 · U · vdW · 셀 · k 점 · 전하 상태 처리 0 줄** | §6 |
| **Q4 '금속성 인터레이어' 와 '전자 차단' 이 충돌하나** | 충돌한다 — 리뷰는 둘을 **다 말하고 정리하지 않는다.** `Fig. 1` · `Fig. 10` · `Table 3` · 결론은 맨 MXene 인터레이어가 계면 저항을 낮추고 덴드라이트를 막는다고 그리지만, p.4 · p.11 · p.20 에서는 "electronically blocking but ion-conductive MXene-derived interphases" · "isolated by an insulating matrix or converted …" 를 단서로 단다. 황화물에서는 금속성 MXene 이 전자 차단층이 될 수 없다 — 유일한 황화물 성공 사례가 MXene 을 **절연성 Li₂TiO₃ 로 바꾼** 경우다 | §11-1 |
| **Q5 신뢰도** | **낮음–중간.** 심사를 거친 리뷰지만 간판 주장 (Li 금속과 무기 SSE 사이 MXene 인터레이어) 에 단 1차 근거가 **제목 수준에서 0 편**이고, 그림–본문 어긋남 6 건 · 인용 어긋남 10 건 이상 (제목 수준) · 같은 리뷰 안의 모순 4 건이 있다 | §10 |

⇒ **한 문장**: MXene 을 고체전지 '이온전도 계면' 소재로 소개하는 2026 년 리뷰 — 우리에게 쓸 것은 적다. 쓸모는 **(i) 금속성 계면층을 황화물에 놓을 때 물어야 할 질문 (전자 경로 · 환원 계면 이동)** 과 **(ii) MXene 을 Li₂TiO₃ 같은 절연 Li 산화물 코팅의 전구체로 쓰는 경로 ([107])** 이고, 수치와 귀속은 원 논문을 거쳐서만 쓴다.

---

## 1. 한 줄 요약
MXene (Mₙ₊₁XₙTₓ — 조기 전이금속 M · 탄소/질소 X · 표면 말단 Tₓ = −O · −OH · −F · −Cl) 은 금속 수준의 전자전도 · 바꿀 수 있는 표면 말단 · 층간 간격 · 유연성을 가져서, 고분자 전해질에서는 염 해리를 돕고 결정성을 낮추는 극성 충전재로, Li/Na/Zn/Mg 금속 음극과 양극 쪽에서는 핵생성 · 전류 분포를 고르게 하는 계면층으로, 다가 이온 전지에서는 층간 숙주로 쓰일 수 있다는 것이 이 리뷰의 주장이다. 동시에 리뷰는 MXene 의 **전자전도가 전해질 안에서는 누설 · 자가방전 · 단락 경로가 된다**는 것, **고전압 · 습기에서 산화된다**는 것, 그리고 **액상 · 겔 · 수계 결과를 전고체 성능과 같다고 볼 수 없다**는 것을 단서로 단다. 자체 자료 · 계산은 없고, 수치는 전부 2 차 (일부 3 차) 소환이다.

## 2. 메타 / 범위 / 구성

| 저자 | 매체 / 년 | DOI | 범위 | 유형 |
|---|---|---|---|---|
| R. Pandey · A. Dhingra · Ravinshu · H. Tarique · S. Sahoo · **R. Kumar\*** (Delhi Univ. · NSUT · Gachon Univ. · TU Darmstadt) | *The Chemical Record* 2026, e70267 (33 쪽) | 10.1002/tcr.70267 | MXene 을 쓴 고체 전해질 · 계면 (Li · Na · Zn · Mg · Al) | 리뷰 (자체 자료 0 · 자체 계산 0) |

- **구성** (절 번호 = 원문): 1 서론 (1.1 역사 · `Fig. 1` · `Fig. 2` · `Table 1`) → 2 이온 수송에 걸리는 MXene 화학 · 구조 (반응식 I–III · `Fig. 3` · `Fig. 4`) → 3 MXene–고분자 복합 고체 전해질 (`Table 2` · `Fig. 5` · `Fig. 6` · 식 1–3) → 4 MXene 계면 공학 (`Fig. 7`–`Fig. 10` · `Table 3` · 식 4–7 · 반응 IV) → 5 이온전도 계면에서의 기전 → 6 이온 수송 · 삽입 (식 8 · `Fig. 11`–`Fig. 14`) → 7 다가 이온 전지 (`Fig. 15` · `Fig. 16` · 반응 V–VII) → 8 안정성 · 확장성 (`Fig. 17` · `Fig. 18`) → 9 전망 (`Table 4` · `Fig. 19`) → 10 결론.
- **분량 감각**: 본문 26 쪽 · 참고문헌 166 (2025 년 38 · 2024 년 27 · 2026 년 8 · 2027 년 1 — 최근 문헌 위주) · 그림 19 중 **출처 표기 없는 저자 작성 개념도 8** (`Fig. 1` · `Fig. 2` · `Fig. 5` · `Fig. 10` · `Fig. 11` · `Fig. 16` · `Fig. 18` · `Fig. 19`) · 재수록 11.
- **리뷰가 내세우는 새로움** (p.2): 기존 MXene 리뷰는 합성 · 막 · 전극 · 복합체 가공을 다뤘고 이온 수송 물리 · SSE 통합 · 전기화학 계면 공학은 빠졌다 → 이 리뷰가 원자 단위 MXene 화학을 이온전도 기전 · 계면 안정화 · 1가/다가 전지와 잇는다. 근거로 `Table 1` 에 2020–2025 리뷰 여섯 ([18]–[24]) 을 놓는다.
  - ⚠ `Table 1` 에 **정면으로 같은 주제의 선행 리뷰 둘이 빠져 있다** — [14] Narayanasamy 2023 *"2D MXenes for All-Solid-State Batteries: A Comprehensive Review"* (*Mater. Today Energy* 37, 101405) · [47] Man 2023 *"MXenes and Their Derivatives for Advanced Solid-State Energy Storage Devices"* (*Adv. Funct. Mater.* 33, 2303668). 둘 다 본문에서는 인용한다 (p.2 · p.3). 새로움 주장의 기준선이 좁게 잡혔다.

## 3. 핵심 수치 총정리 ★ (전부 2 차 소환 — 원 논문 확인 전 인용 금지)

> 이 리뷰의 원 논문 중 우리 litdb 에 digest 가 있는 것은 **0 편**이다 (주요 원전 13 편 DOI 로 확인 — §12a). 아래 표의 수치는 모두 원 논문을 열어 보지 않았다.

### 3a. MXene 물질 · 구조 · 합성

| 항목 | 값 (리뷰 인쇄) | 조건 · 계 | 원전 · 비고 |
|---|---|---|---|
| 일반식 | Mₙ₊₁XₙTₓ — M = Ti · V · Nb · Mo (조기 전이금속) · X = C · N · Tₓ = −OH · −O · −F (용융염이면 −Cl) | — | [7] · [20] |
| 층간 간격 | ≈ **0.5–1.5 nm** | 말단 종류 · 수화 정도에 따라 | [2차 · ref 119, 120] — 기름–물 분리막 · 이온성액체 슈퍼커패시터 MD 논문 |
| 박리 나노시트 두께 | ≈ **1.27 nm** ("few-layer" 로 해석) | HRTEM | [2차 · ref 62] · `Fig. 3c` (미실독). ⚠ 단층 MXene 두께 (≈1 nm 안팎 [추정 · 배경지식]) 와 견주면 단층–2 층 수준이라 'few-layer' 해석은 원전 확인 필요 |
| 진공 여과 막 두께 | ≈ **3.2 µm** | 단면 SEM | [2차 · ref 62] · `Fig. 3d` (미실독) |
| 열 안정 | **300–500 °C** 까지 구조 유지 | 불활성 분위기 | [리뷰] p.23 — **인용 없음** |
| 고분자 결정화 (iPP) | 0.5 wt% MXene → 결정화 피크 온도 **+2.9 °C** · 속도 ↑ / ≥ 1 wt% → 결정화 억제 | 동시차 비등온 결정화 | [2차 · ref 60] — **전해질이 아니라 폴리프로필렌** |
| 습식 식각 (반응 I · II) | Mₙ₊₁AXₙ + 3HF → Mₙ₊₁Xₙ + AF₃ + 3/2 H₂ · Ti₃AlC₂ + 3HF → Ti₃C₂Tₓ + AlF₃ + 3/2 H₂ | HF 또는 LiF/HCl | (II) 는 Tₓ 를 오른쪽에 쓰고 말단을 만드는 HF · H₂O 를 왼쪽에 안 써서 **물질수지가 안 맞는 '단순화' 식** — 리뷰 스스로 "multiple step reactions" 라 적음 |
| 용융염 식각 (반응 III) | 2Ti₃AlC₂ + 5ZnCl₂ → 2Ti₃C₂Cl₂ + 2AlCl₃ + 5Zn | 무플루오린 · Cl 말단 | [리뷰] p.5 — Ti · Al · C · Zn · Cl 모두 맞는 식 ([우리 산술]). "conductivity 높고 결함 적다" 는 **인용 없음** |
| Lewis 염기 할라이드 처리 (LB-MXene) | AlBr₃/NaBr/KBr 공정염 융점 ≈ **90 °C** · AlI₃/NaI/KI ≈ **155 °C** · Br 가 F 를 친핵 치환 → 층간 확장 · Ti–Br 결합 | — | [2차 · ref 132] · `Fig. 12` (미실독) |

### 3b. MXene–고분자 복합 전해질 (`Table 2` 전사 · p.8)

| MXene | 고분자 | 제조 | σ (S cm⁻¹) | 전기화학 창 (V) | 리뷰가 적은 이점 | 인용 → 제목 수준 대조 |
|---|---|---|---|---|---|---|
| Ti₃C₂Tₓ | PEO | 용액 주조 | ~10⁻⁴ (60 °C) | ~4.0 | Li⁺ 수송 ↑ · 유연막 | [85] Ti₃C₂Tₓ 강화 PEO/SN 전해질 — 맞음 |
| Ti₃C₂Tₓ | PVDF-HFP | in situ 중합 | ~10⁻⁵ (RT) | ~4.2 | 기계 무결성 | [86] **Ti₃C₂Tₓ 처리 PVDF-HFP 분리막 (액체 전해질 용매화)** · [87] PVDF-HFP 복합 전해질 (제목에 MXene 없음) — 'in situ 중합 MXene 전해질' 근거로 안 맞아 보임 |
| Ti₃C₂Tₓ | PAN (+NaPF₆) | 전기방사 | ~10⁻⁶ (RT) | ~3.3 | 열 안정 · 계면 양호 | [88] MXene 전기방사 고분자 전해질 섬유 — 맞음 |
| Nb₂CTₓ | 젤라틴 | 용액 혼합 | ~10⁻⁶ (RT) | ~3.8 | 생체적합 · 유연 계면 | [89] **KI 도핑 젤라틴 하이드로겔 (EDLC)** · [90] **젤라틴–알지네이트 겔 (슈퍼커패시터)** — 둘 다 제목에 MXene · Nb₂C 없음, 물 함유 겔 |

- 같은 표에서 **전자전도도 σ_e · 이온 수송수 t_ion 열이 없다** — 리뷰 자신이 p.9 에서 *"both ionic and electronic conductivity, together with the ionic transference number, should be systematically reported"* 라고 요구한 바로 그 두 양이다.
- "전기화학 창" 은 측정법 (LSV 주사속도 · 전극 · 전류 문턱) 이 안 적혀 있다 — 우리 grand-potential 산화 개시 (층①) 와 **다른 양**이다 (§7).
- 본문 수치: Nb₂CTₓ–PEO **RT ≈ 10⁻⁴ S cm⁻¹** [2차 · ref 81 — 전고체 Li–S 용 PEO] · MXene–PEO 가 순수 PEO 대비 **2 배** σ [2차 · ref 96 · `Table 3`] · MXene–고분자 복합 전해질 일반 "approaching 10⁻⁴ S cm⁻¹" [리뷰 · ref 14–17] · 100 °C 이상에서 구조 유지 [2차 · ref 84].
- 서론의 비교 기준 (p.2 · [14–17]): LLZO ~10⁻⁴–10⁻³ · LATP ~10⁻⁵–10⁻⁴ · **황화물 > 10⁻² S cm⁻¹**. ⚠ 황화물 값은 고성능 끝값만 적은 것이다 — [16] Seino 2014 (Li₂S–P₂S₅ 유리세라믹) 류. 냉간 가압 Li₆PS₅Cl 은 그보다 한 자리 낮게 보고된다 ([litdb 카드] [Zuo] 25 °C **2.9 mS cm⁻¹** · Cl1.5 조성 7.0 mS cm⁻¹ — `zuo2022_chlorination_cathode_interface.md` §3a).

### 3c. 계면 (Li/Na 금속 · 양극) — 리뷰가 든 사례

| 항목 | 값 (리뷰 인쇄) | 계 · 조건 | 원전 · 비고 |
|---|---|---|---|
| **MXene → Li₂TiO₃ 전환 코팅** ★ | 초기 방전 **138.8 mAh g⁻¹** · 0.2 C **100 사이클 86.2 %** 유지 · "up to 4.5 V" 에서 황화물 전해질의 계면 분해를 막음 | LiCoO₂ 위 Ti₃C₂Tₓ 를 **500 °C** 에서 in situ Li₂TiO₃ 로 전환 · **황화물 전고체 셀** (SE 조성 리뷰 미기재) | [2차 · ref 107] Wang 2024 *Chin. Chem. Lett.* 35, 108776 — **리뷰 전체에서 유일한 황화물 SE 1차 사례**. 남는 것은 MXene 이 아니라 **절연성 Li 산화물** 이다 (§11-2) |
| COF-1 + Ti₃C₂ 혼성 보호층 (Li 금속) | 대칭셀 **1000 h** 뒤 과전압 감소 · 실험실 **1.6 Ah** 파우치 **366.7 Wh kg⁻¹** | 전해질 종류 리뷰 미기재 | [2차 · ref 104] — 제목상 액체 전해질 Li 금속 셀로 보임 [추정] |
| 산화물 SSE 셀의 Ti₃C₂Tₓ 인터레이어 | 계면 저항 감소 · "hundreds of cycles" 단락 없음 | Li 금속 / 산화물 SSE | [리뷰] p.12 — 이 문단의 유일한 인용은 문단 끝 [108–112] 인데 **제목 수준에서 산화물 SSE 인터레이어 연구가 없다** (§10a) |
| Na 금속의 Nb₂CTₓ · Ti₂CTₓ 인터레이어 | Na 덴드라이트 억제 · 계면상 안정 | Na 금속 | [리뷰] p.12 — 같은 문단 · 같은 문제 |
| `Table 3` 네 행 (p.14) | 음극 계면 "Li metal/MXene/SSE · 안정 사이클 · 과전압 ↓" [108] / 양극 "LFP/MXene 코팅/SSE · 100 사이클 유지" [109] / 벌크 "MXene–PEO · 순수 PEO 대비 2 배 σ" [96] / 양쪽 "Li/MXene/LATP/LFP · 수명 · CE ↑" [110] | — | [108] **Mo 계 MXene 전극의 LiF-rich SEI** (Li 금속 전지 — SSE 아님) · [109] **준고체 MXene Li–I 전지** (LFP 아님) · [110] **자립형 LATP/LFP 복합 양극 미세구조** (제목에 MXene 없음). 맞는 것은 [96] 하나 |

### 3d. DFT · MD 가 낸 수치 (리뷰가 옮긴 것 전부)

| 양 | 값 | 계 · 조건 | 출처 · 우리 규율 적용 |
|---|---|---|---|
| PVDF-HFP 사슬–MXene "계면 결합에너지" E_i | **−1.166 eV** (MXene–PH) · **−3.268 eV** (MP–PH) [그림 인쇄] | MP = mPEG 그래프트 MXene · 셀 크기 다름 · 정규화 (셀당? 사슬당?) 미기재 | [2차 · ref 103] `Fig. 7b`. ⚠ eV/셀 단위라 우리 점착 W_ad (J m⁻² · 면적 정규화) 와 **다른 양** — 같은 표에 놓지 않는다 |
| Li⁺ · TFSI⁻ "흡착에너지" (그림 표기 **E_a**) | MXene–Li⁺ **−0.650** · MXene–TFSI⁻ **−2.148** · MP–Li⁺ **−1.096** · MP–TFSI⁻ **−3.605 eV** [그림 인쇄] | 전하 종 (Li⁺ · TFSI⁻) 을 금속성 슬랩 위에 — 기준 상태 · 전하 보정 미기재 | [2차 · ref 103] `Fig. 7c,d`. ⚠ **E_a 는 활성화에너지가 아니라 흡착에너지**다. ≳ 2 eV 셋 (−2.148 · −3.268 · −3.605) 은 우리 규율 (`D-2026-10-05-adsorption-site-coordination`) 상 결합 자리 배위수부터 세야 하는데 **공개 구조 없음 → 배위 미확인**. `figure-read`: MP–TFSI⁻ 의 TFSI⁻ 는 MXene 면이 아니라 **mPEG 사슬 끝 · 셀 윗면 근처**에 있다 — 'MXene 흡착' 이라는 이름과 안 맞고, 주기 이미지 슬랩 아랫면과의 거리는 그림으로 판단 불가 |
| Li⁺ 결합에너지 · 이동 장벽 (일반론) | 결합 **−1.2 ~ −2.5 eV** · 장벽 **≈0.2–0.4 eV** | MXene 층간 | [리뷰 · ref 18] — ref 18 은 *Chem. Rev.* 리뷰라 **3 차 소환** · 계 · 말단 · 범함수 0. 결합 −2.5 eV 끝은 ≳ 2 eV — **배위 미확인** |
| K⁺ · Mg²⁺ 수송 "에너지 장벽" | K⁺ `figure-read ≈` **3.9 / 4.6 / 5.1 / 5.5** · Mg²⁺ ≈ **7.0 / 8.5 / 9.6 / 11.2 kcal mol⁻¹** (전하밀도 7.0 / 14.2 / 17.6 / 22.0 −mC m⁻²) · 차이 **3.09 / 3.88 / 4.43 / 5.78** [그림 인쇄] | MLM-EDTA-1.5 막 · 0.2 M 혼합염 **수용액** | [2차 · ref 24] `Fig. 13f`. eV 환산 [우리 산술]: K⁺ 0.169–0.239 · Mg²⁺ 0.304–0.486 eV · 계산 장벽인지 온도 의존 투과의 겉보기 값인지 리뷰만으로 불명 (겉보기 값으로 보인다 [추정]) |
| K⁺ · Mg²⁺ 흡착 (EDTA 탈양성자 정도 0–4) | K⁺ `figure-read ≈` −0.2 → −1.1 eV · Mg²⁺ ≈ −1.05 → −3.9 eV | DFT · EDTA 분자 (MXene 아님) | [2차 · ref 24] `Fig. 13g`. Mg²⁺–EDTA⁴⁻ 의 −3.5 · −3.9 eV 는 **2 가 양이온 · 다가 음이온 킬레이트** — 배위는 리간드 쪽 (표면 자리 아님) · 용매화 처리 미확인 → 수용액 선택도의 크기로 읽지 않는다 |
| Li⁺ 의 SO₃H 자리 결합 | Na⁺ · K⁺ 보다 약함 (수치 없음) | MXene–PSS 막 | [2차 · ref 67] |
| MD — K⁺ · Mg²⁺ 진입 · 통과 시간 · RDF | 수치 본문 없음 | 수화 이온 · 막 채널 | [2차 · ref 24] `Fig. 14` (미실독) |

**홉 수 검산** (`D-2026-09-27-barrier-hop-count` · Γ = ν₀·exp(−Ea/kT) · ν₀ 10¹³ s⁻¹ **가정** · T = 298 K · [우리 산술]):
- 리뷰의 Li⁺ 장벽 **0.2 eV → Γ ≈ 4×10⁹ s⁻¹ (대기 ≈ 0.24 ns)** · **0.4 eV → Γ ≈ 1.7×10⁶ s⁻¹ (대기 ≈ 0.6 µs)** — '낮은 장벽 · 빠른 확산' 서술과 차수 모순 없음.
- `Fig. 13f`: K⁺ 0.169 eV → 대기 ≈ 72 ps · 0.239 eV → ≈ 1.1 ns / Mg²⁺ 0.304 eV → ≈ 14 ns · 0.486 eV → ≈ 16 µs.
  🔎 **차수 모순 1 건**: 장벽 차 3.09 → 5.78 kcal mol⁻¹ 를 홉 속도비로 읽으면 exp(ΔE/kT) ≈ **1.9×10² → 1.5×10⁴** 인데, 같은 그림의 측정 선택도 (`Fig. 13c` · `figure-read ≈`) 는 **54 → 103** (≈2 배) 다. 앞 인자가 같다는 가정으로는 차수가 안 맞는다 ⇒ 이 막대들은 **단일 홉 장벽이 아니라 겉보기 활성화에너지** (분배 · 농도 · 앞 인자가 다름) 로만 읽는다. 선택도의 기전 근거로 장벽 차를 그대로 쓰지 않는다.

### 3e. 막 · 분리 (액상 — 리뷰 스스로 고체 SSE 와 비교하지 말라고 단 것)

| 계 | 값 | 원전 |
|---|---|---|
| MXene–PSS (SO₃H) 막 — 염도차 발전 | 출력밀도 **1.57 W m⁻²** (시험면적 0.24 mm²) · 선택도 Li⁺/Na⁺ **2.5** · Li⁺/K⁺ **3.2** | [2차 · ref 67] `Fig. 4e,f` (미실독) |
| 수평 정렬 MXene (H-MXene) 막 — 1 M NaCl 수용액 | σ **0.2067 S cm⁻¹** · 확산 전류밀도 **308 A m⁻²** (10 배 염도차) · 삼투 출력 **9.47 W m⁻²** · 변환효율 **45.7 %** | [2차 · ref 70] — 리뷰: *"should not be directly compared with that of dry SSEs"* (p.6) |
| B 치환 −OH (초임계 CO₂) SCB-MXene 막 | 부피 정전용량 **742.7 C cm⁻³** (1000 mV s⁻¹) · **66.3 Wh L⁻¹** @ **132.5 kW L⁻¹** | [2차 · ref 71] (슈퍼커패시터) |
| Ag/MXene/H₃PO₄–PVA/Ag 소자 | 이력 이온 수송 · 메모리 커패시터 ON/OFF (10 kHz) | [2차 · ref 62] `Fig. 4a–d` (미실독) |
| MLM-EDTA 막 — K⁺/Mg²⁺ | 전하밀도 `figure-read ≈` MLM 1.3 / 6.5 / 9.0 / 11 · MLM-EDTA-1.5 7.0 / 14.2 / 17.6 / 22.0 −mC m⁻² (pH 2.5 / 4 / 6 / 8) · 선택도 MLM ≈ 6 / 8 / 9 / 10 → MLM-EDTA ≈ **54 / 83 / 92 / 103** · K⁺/Ca²⁺ ≈ 43 → 76 · K⁺/Li⁺ ≈ 3–4 · K⁺/Na⁺ ≈ 2 | [2차 · ref 24] `Fig. 13a,c,d` |
| 1 wt% 양성자화 g-C₃N₄ 삽입 Ti₃C₂Tₓ | **140 F g⁻¹** (1 M MgSO₄) · **10,000** 사이클 | [2차 · ref 127] (슈퍼커패시터) |

### 3f. 다가 이온 (Zn · Mg — 대부분 전극 · 겔 전해질)

| 계 | 값 | 원전 |
|---|---|---|
| PVA 겔 + MXene 유래 TiO₂ 나노시트 (PZ3T) | Zn 대칭셀 **> 3000 h** · V₂O₅/Zn 전셀 CE **99.8 %** · **216 mAh g⁻¹** (115 사이클 뒤) | [2차 · ref 133] |
| Mo₂CTₓ 충전 겔 (EMITFSI/Zn(OTf)₂/PVHF) | 대칭셀 **300 h** 덴드라이트 ↓ · CaV₆O₁₆·3H₂O 전셀 CE ~100 % · 유지 99 % · **155 mAh g⁻¹** | [2차 · ref 134] |
| 3D 거대기공 Ti₃C₂Tₓ 막 (Mg 양극) | ~**210 / 140 / 55** "mA g⁻¹" @ 0.5 / 1 / 5 C | [2차 · ref 135] — ⚠ 단위 오기 (용량이면 mAh g⁻¹) |
| Ti₃C₂Tₓ/CNT 종이 (Mg²⁺/Li⁺ 혼성) | ≈ **105 mAh g⁻¹** @ 0.1 C · **80 mAh g⁻¹** 로 500 사이클 이상 @ 1 C | [2차 · ref 136] |
| 선리튬화 V₂C (Mg²⁺/Li⁺ 동시 삽입) | **230.3 mAh g⁻¹** @ 0.02 A g⁻¹ · 480 사이클 **82 %** | [2차 · ref 137] |
| VS₄@Ti₃C₂/C (Mg) | 900 사이클 뒤 **147 mAh g⁻¹** @ 500 mA g⁻¹ (≈80 %) · **129** @ 1000 mA g⁻¹ · **492** @ 50 mA g⁻¹ | [2차 · ref 138] |
| NiSe₂–CoSe₂@TiVCTₓ (Mg) | **136 mAh g⁻¹** @ 0.05 A g⁻¹ · > 500 사이클 · 파우치 | [2차 · ref 139] |
| TAP/Ti₃C₂Tₓ (수계 Zn) | **303 mAh g⁻¹** @ 0.04 A g⁻¹ · 10,000 사이클 이상 **81.6 %** | [2차 · ref 140] |
| MXene/Bi-3 (수계 Zn) | **178.1 mAh g⁻¹** @ 0.25 A g⁻¹ · 4500 사이클 @ 2.5 A g⁻¹ 거의 무손실 | [2차 · ref 141] |
| H₂V₃O₈/MXene 자립막 (준고체 Zn) | 25 °C **3000 사이클** 뒤 **180 mAh g⁻¹** · GITT (0.1 A g⁻¹ · 30 min 펄스 + 120 min 이완) D_Zn 본문 **"10⁻⁷–10⁻⁸ cm² s⁻¹"** · `figure-read ≈` **2×10⁻⁹ – 1.5×10⁻⁸** · R_ct **22 Ω** [그림 인쇄] | [2차 · ref 142] `Fig. 15` — 본문 범위가 그림보다 **한 자리 높다** (§10a) |

### 3g. 안정성

| 항목 | 리뷰 서술 | 원전 |
|---|---|---|
| 갓 만든 MXene 말단 | XPS 로 **F 가 가장 많다** (Ti₃C₂Tₓ · Ti₂CTₓ · Ti₃CNTₓ · Nb₂CTₓ · Nb₄C₃Tₓ) → 시간이 지나며 산화해 **금속 옥시플루오라이드** | [2차 · ref 144] |
| 열화의 매개 | **물이 매개하고 산소가 아니다** → 물에서 차단해야 | [2차 · ref 145] (콜로이드 가수분해) |
| 제일원리 표면 조성 | Mₙ₊₁XₙO₂ (M = Sc · Ti · V · Cr · Zr · Nb · Mo · Hf · Ta · X = C · N · n = 1–3) 은 합성 중 산소 포화 표면 · Sc 계는 플루오린화 권장 | [2차 · ref 146] |
| 분산액 산화 속도 | 고농도에서 느림 (입체 차폐) · 염기 조건에서 빠름 | [2차 · ref 147] |
| 전기화학 창 | p.21 *"relatively narrow electrochemical stability window, particularly in aqueous"* ↔ p.23 *"relatively wide potential window … onset of faradaic degradation occurring outside the typical operational range"* | 둘 다 **인용 · 수치 없음** — 같은 리뷰 안 모순 (§10a) |

### 3h. 리뷰에 **없는** 지표 (우리 축 대조)
- MXene 전자전도도 수치 0 ('high · metallic' 서술만) · 복합 전해질의 전자 퍼콜레이션 문턱 0 · t_ion 0.
- 황화물 SE 의 σ · 창 · 계면 저항 0 (Li₆PS₅Cl · argyrodite · LGPS 0 회 · "sulfide" 본문 5 회 — p.2 · p.12 · p.17 ×2 · p.20).
- MXene 의 Li 대비 산화 · 환원 전위 수치 0 · Li 금속과의 반응 (Ti 환원 · 말단 환원) 열역학 0.
- 임계전류밀도 0 · 스택 압력 0 ("pressure" 0 회) · Monroe–Newman 은 참고문헌 [3] 에만 (본문 이름 0 회).
- 수분 → H₂S 0 · 건식 공정 0.

## 4. 본문 절별 정리 (그림 실독 포함)

### 4.1 서론 · 역사 (§1 · p.1–4 · `Fig. 1` · `Fig. 2` · `Table 1`)
- SSB 의 장벽: 고체–전극 접촉 불량 · 높은 계면 저항 · 상온 σ 부족 · Li 덴드라이트 · 무기 SE 의 강성 · 취성 [2–5].
- MXene 의 세 쓰임 (p.2): ① 고분자 · 혼성 매트릭스에서 염 해리 · 결정성 · 수송 · 기계 조절 [9] ② 전극 표면에 순응해 접촉 저항 ↓ · 덴드라이트 ↓ 완충층 [10] ③ Li · Na · Zn · Mg · Al 삽입 [11].
- 역사 (§1.1 p.2–4): 2011 Ti₃C₂Tₓ 첫 보고 → 말단의 역할 인식 [29–34] → (2016–2020) 층간 갤러리를 이온 통로로 [본문] → 고분자 전해질 충전재 [35–40] → 2020 이후 복합 전해질 · 고분자–세라믹 [41–43] → 금속 음극 계면 코팅 [44–46] · 양극 [47]. *"excessive MXene loading can produce electronically conductive pathways through the electrolyte"* (p.3) · *"pristine MXenes may undergo oxidation … under high-voltage or humid processing conditions"* (p.3).
- 현 단계 (p.4): '경험적 혼입 → 합리적 계면 설계' — 말단 선택 합성 · 필러링 · 고분자 그래프트 · 내산화 조성 · 무플루오린 · **"electronically blocking but ion-conductive MXene-derived interphases"** · DFT · MD · ML · operando [48–52].
- p.4 단서: *"Results from liquid, gel, or aqueous systems cannot be directly equated with the performance of fully SSBs."*
- `Fig. 1` (실독 · 저자 작성): 왼쪽 '과제' (느린 Li⁺ · 균열 · 덴드라이트), 가운데 MXene (−O · −OH · −F), 오른쪽 '해결' (빠른 Li⁺ · SSE/MXene/Li 적층 · 덴드라이트 억제). 아래 목록 **"High conductivity · Surface chemistry tunability · Mechanical flexibility · Hydrophilic interlayers"** 를 이점으로 나열 — 'High conductivity' 가 이온인지 전자인지 안 적혔고, 친수성은 황화물에는 위험 인자다 (§11-3). 'M⁺' 옆 글리프가 깨져 있고 오른쪽 적층의 'Li' 위에 회색 상자가 덮여 있다.
- `Fig. 2` (실독 · 저자 작성): 7 단계 연표 — 2011–13 발견 / 2014–16 삽입 · 말단 / 2016–18 막 · 나노채널 / **2018–20 고분자 복합 전해질** / 2020–22 계면 공학 · 덴드라이트 / 2022–24 다가 이온 / 2024– 안정성 · 실용. 본문은 *"From 2020 onward, MXene–polymer composite electrolytes … received increasing attention"* (p.3) · *"Between approximately 2016 and 2020, ion intercalation studies and MXene membrane research …"* (p.2) 라 적어 **그림과 연대가 한 칸씩 어긋난다**. 황화물 SE 는 연표 어디에도 없다.
- `Table 1` (PDF 텍스트 전사): 선행 리뷰 여섯 — [18] 원자 단위 설계 (DFT + 실험) · [19] 이온 선택 막 · [20] 개관 · [21] Li 이온 음극 · [22] MXene–고분자 복합체 · [23] 질화물 MXene · [24] 생체모방 서브나노 채널 막. 각 행에 '한계' 와 '이 리뷰가 메우는 것' 열. [14] · [47] 누락은 §2.

### 4.2 MXene 화학 · 구조 (§2 · p.4–7 · `Fig. 3` · `Fig. 4`)
- 식각 반응 (I)–(III) (§3a). 대표 MXene: Ti₃C₂Tₓ (원형) · Nb₂CTₓ · Mo₂TiC₂Tₓ · Ti₂CTₓ · 단층 · 다층 · 필러링 형태 [21].
- 말단: −OH · −O 는 친수성 ↑ · 고분자 사슬과 수소결합 · 양이온과 정전 상호작용 → 배위 · 홉 · 구획 운동 보조 수송 [22, 55] / **−F 는 표면 극성 ↓ · 양이온 흡착 방해 → 이온 전도에 덜 유리** [56] / 말단이 정하는 표면 전하 · 전자 분포가 이동 장벽을 바꾼다 [57].
- 층간 간격: 건조 · 열처리 시 수축 (이온 접근 ↓) · 팽윤 · 용매화 시 확장 (수송 ↑) [58] → '반응형 이온 채널' [59]. 고분자 (PEO · PVDF-HFP · PAN) 분산 [22]. 결정성 영향은 농도 · 계면 의존 — 저함량은 핵생성제, 고함량은 사슬 운동 제약 · 비정질 ↑ → **"ionic conductivity cannot be attributed solely to crystallinity suppression"** (p.5 · 근거 [60] 은 폴리프로필렌 결정화 논문).
- `Fig. 3` (미실독): 박리 나노시트 SEM · TEM · HRTEM (≈1.27 nm) · 진공 여과 막 단면 (≈3.2 µm) [62].
- 다른 2D 와 비교 (p.6): GO — 전자전도 낮고 간격 · 조성 조절 부족 [63] / h-BN — 절연 · 열 안정이지만 화학적으로 불활성이라 이온과 상호작용 약함 [64] / TMD (MoS₂ · WS₂) — 중간 전도 · 이방성 · 조절성 낮음 [65, 66] → MXene 이 "금속 전도 · 풍부한 기능화 · 구조 적응" 균형.
- 막 사례: Chang [62] 메모리 커패시터 (`Fig. 4a–d` · 미실독) · Tong [67] MXene–PSS (`Fig. 4e,f`) — 본문 문단 끝 인용은 엉뚱하게 **[38]** (Ti 탄질화물 Na 이온 전지 논문) · Zhu [68] Cs 삽입 막 · "Gogotsi et al." [69] (1 저자는 Athreya) 전압 게이트 막 · Qian [70] 수평 정렬 막 · Liu [71] B 치환 · PDA 구속 채널 [72].
- p.7 결론 문장: *"Their ability to act as mixed ionic–electronic conductors also opens possibilities for creating conductive interphases that can both transport ions and **electronically passivate** unstable interfaces"* — 전자전도체로 '전자적 부동태화' 를 한다는 문장은 그 자체로 모순이다 (§10b).

### 4.3 MXene–고분자 복합 고체 전해질 (§3 · p.7–9 · `Table 2` · `Fig. 5` · `Fig. 6` · 식 1–3)
- 제조: 용액 주조 (ACN · DMF · 물) [77, 78] · in situ 중합 [79, 80] · 층별 적층 (LbL — 경사 · 비대칭 전해질).
- 대표계: MXene–PEO (결정성 ↓ · 연속 경로) · Nb₂CTₓ–PEO RT ≈10⁻⁴ [81] · MXene–PVDF-HFP (열 안정 · 낮은 유전 손실) [82, 83] · MXene–PAN (Na · 다가). 기계: 영률 · 인장강도 ↑ → 덴드라이트 억제 · 열전도 ↑ · 100 °C 이상 유지 [84]. `Table 2` (§3b).
- **이온–전자 균형 (p.8–9)** — 이 리뷰에서 우리에게 제일 맞는 문단: MXene 의 높은 전자전도는 국소 전극–전해질 계면에서는 전하 재분배에 유리할 수 있지만, **벌크 전해질 안 과량 MXene 은 전자 퍼콜레이션 → 누설 · 자가방전 · 내부 단락**. Anasori [92]: 이중 전이금속 MXene 바깥층 Ti → Mo 치환이 금속성 → **반도체성** 수송 (Mo₂TiC₂Tₓ 반도체성 · Ti₃C₂Tₓ 금속성). 퍼콜레이션 문턱 아래에서는 극성 충전재 · 표면 절연 · 고분자 그래프트 · 유전 스페이서 · 배향 제어로 이온–전자 수송 분리 [60]. *"For a solid electrolyte, the ionic transference number should ideally approach unity … both ionic and electronic conductivity, together with the ionic transference number, should be systematically reported"* (p.9).
- `Fig. 5` (실독 · 손 크롭 · 저자 작성): 왼쪽 제조 전략 (in situ 중합 · **"Layer-by-layar"** 오타) · 가운데 −OH · O–F 말단 MXene 적층 + 고분자 사슬 + 이온 · 대표계 (MXene–PEO · PVDF-HFP · PAN) · 오른쪽 '물성 영향' ↑ 이온전도 · ↑ 기계강도 · ↑ 열 안정. **전자 누설 · 퍼콜레이션 경고는 그림에 없다** — 바로 앞 본문 (p.8–9) 의 핵심 단서가 빠졌다. 본문 (p.9) 은 *"The effects of −F terminations are more system-dependent"* 라 했는데 그림은 −F 도 같이 '이점' 쪽.
- `Fig. 6` (미실독 · 캡션): (a) MXene 결합 수송망 고분자 전해질 · (b) MXene 복합 전해질 제조 · (c,d) **PEO/LiTFSI/MnO₂ 나노시트** · (e) **판상 LLZAO** — (c)–(e) 는 MXene 이 아니다. 본문은 (e) 를 *"Li et al. [95]"* 로 부르는데 [95] 의 1 저자는 **Cheng** 이고 Li 는 [98] (MnO₂) 이다. 저작권 줄의 [97] (MOF 나노시트) 은 어느 패널인지 캡션 · 본문에 없다.
- 식 (1) Nernst–Einstein · (2) Arrhenius · (3) VTF — MXene 이 n (염 해리) 과 D (층간 확장 · 장벽 ↓) 를 같이 올린다 · Ea 를 낮춘다 (인용 없음). PEO 계는 VTF 형.
- 절 끝 *"[61–65]"* — 헤테로원자 도핑 리뷰 · 메모리 커패시터 · EMI 차폐 리뷰 · h-BN 리뷰 · TMD 패시베이션 MXene HER — MXene–고분자 SSE 전망의 근거가 아니다.

### 4.4 계면 공학 (§4 · p.9–15 · `Fig. 7`–`Fig. 10` · `Table 3` · 식 4–7 · 반응 IV)
- 문제 [99–102]: 접촉 · 공간전하층 · 계면상 불안정 · 덴드라이트 (Li/Na 음극) · 부반응 · 박리 (고전압 양극).
- 원리 (p.10–11): MXene 인터레이어의 이점은 물리 장벽이 아니라 국소 화학 · 구조 · 정전 환경을 바꾸는 것 · 2D 순응 피복 · 말단 = 화학 활성 자리 [100, 102]. 단서 둘 — *"dendrite suppression should not be attributed solely to the mechanical strength of MXene"* · 양극 쪽은 *"conversion of the original MXene into a chemically stable, ion-conductive interphase may be more relevant than the retention of the pristine MXene structure"* (p.11).
- `Fig. 7` (실독 · [103] He 2025 *Adv. Funct. Mater.*): (a) ELF 단면 MXene–PH · MP–PH — **색 막대 · 단면 위치 · 등치값이 없다** → 값을 읽을 수 없는 그림 (본문도 해석 0 줄: *"Figure 7 shows the electron localization function plots, interface bonding energy, adsorption energy, and stripping/plating cycling"* 한 문장). (b)–(d) 결합 · 흡착 에너지 (§3d). 모형은 O 말단 Ti₃C₂ 슬랩 (범례 Ti · O · H · C · N · F · Si · S · Li — mPEG 은 Si 앵커로 접목 `figure-read`). (e) 모식: pH-Li (노란 막) → 불균일 SEI → 덴드라이트 / pH-Li-SN-2MP (파란 막) → 균일 SEI → 덴드라이트 적음. ⇒ 대상은 **고분자 (PVDF-HFP + SN) 전해질**이지 무기 SSE 가 아니다.
- Li/Na 금속 코팅: Ti₃C₂Tₓ 순응 피복 · −O · −OH '친리튬' 말단 → 균일 핵생성. COF-1 + Ti₃C₂ 혼성층 [104] (§3c). [72] (막 분리 논문) 를 'Li 석출 균일화' 근거로 · [105] (VN MXene + Fe 원자 자리 — 제목은 **Li–S 전지**) 를 'Li 덴드라이트 억제' 근거로 인용.
- `Fig. 8` · `Fig. 9` (미실독 · [106]): MXene–F,N 도핑 탄소–CoSe₂ 이종구조 합성과 CV · GCD · 율속 · Nyquist — 원전 제목은 **수소 발생 · 슈퍼커패시터**. 리뷰 스스로 *"primarily reported as an electrode architecture"* (p.12).
- **Li₂TiO₃ 전환 코팅 [107]** (p.12 · §3c) — 이 리뷰의 유일한 황화물 SE 1차 사례.
- 바로 뒤 문단 (p.12–13): *"in lithium metal cells using oxide-based SSEs, the introduction of a Ti₃C₂Tₓ interlayer … stable cycling over hundreds of cycles"* · *"Na metal systems, where Nb₂CTₓ or Ti₂CTₓ interlayers …"* — 문단의 인용은 끝의 [108–112] 하나인데 그 다섯은 Mo-MXene LiF-rich SEI · 준고체 Li–I 전지 · LATP/LFP 복합 양극 · **실어증 환자 간호용 열전 하이드로겔** · Ti₃C₂@TiO₂ LIB 전극이다 (제목 수준).
- 공간전하 (식 4 · p.13–14): 1차원 공핍 근사 Δφ = qN_D d² / (2εε₀) — 반도체 공핍층 식을 그대로 가져왔고 SSE 의 결함 화학 (Li 공공 · 침입) 으로 옮긴 설명 · 수치 예 없음. 리뷰 스스로 실제 계면은 결함 편석 · 반응 · 보상으로 더 복잡하다고 단다. 이어서 *"MXenes, owing to their metallic conductivity …, can homogenize the local electrostatic environment and mitigate such potential gradients"* — 인용 없음 (§10b).
- '능동' 역할 (p.14): *"partial ionic conductivity and high surface redox activity allow them to participate in interfacial charge compensation"* — 계면에서 산화환원 활성이라는 말은 곧 **소모 · 변환**된다는 뜻이기도 하다.
- `Fig. 10` (실독 · 저자 작성): 위에서 아래로 Li 금속 음극 / MXene 인터레이어 / 고체 전해질 + 확대 그림 (MXene 나노시트 · −O · −OH · −F · Li⁺ · "Tunable interlayer spacing" · "Li⁺ transport in interlayer channels") + 아래 줄 *(i) Lower interfacial resistance (ii) Improved ionic conductivity (iii) Homogeneous Li deposition (iv) Dendrite suppression*. ⚠ **기하가 물리와 안 맞는다** — "Uniform Li⁺ deposition" 화살표와 덴드라이트 아이콘이 **Li 금속의 바깥 윗면** (전해질이 없는 쪽) 에 있고, Li⁺ 는 Li → MXene → SE 방향 (박리 방향) 으로 그려져 있다. 확대 그림은 Li⁺ 가 **기저면을 수직으로 뚫고** 지나가게 그렸는데, 결함 없는 MXene 기저면은 이온이 통과할 구멍이 없어 층간 수송은 면 방향이다 — 수평으로 쌓인 인터레이어의 두께 방향 수송은 플레이크 가장자리 · 틈으로 돌아가야 한다 (리뷰 자신이 인용한 [70] 도 '수평 수송' 이다). 그리고 **전자 경로가 그려져 있지 않다** — 금속성 인터레이어는 Li 와 같은 전위에 놓인다 (§11-1).
- 말단 효과는 전해질 의존 · −F 도 일률적이지 않다 (p.15) — p.5 의 "−F 는 덜 유리" 와 다른 결.
- EIS (식 5 · p.15): R_int = R_SEI + R_ct · R_int = 1 / (2π f_max C_eff) — RC 한 쌍의 관계식이지 독립 추정법이 아니다 (C_eff 를 따로 알아야 한다). *"MXene-modified interfaces consistently show lower R_int"* — 인용 없음.
- Li 석출 (반응 IV) · Sand 시간 (식 6) · Butler–Volmer (식 7) — 'j₀ 증가' 의 인용 [16–21] 은 Seino 2014 (황화물 유리세라믹) · SSB 리뷰 · MXene Chem. Rev. · 막 리뷰 · 개관 · 음극 리뷰라 j₀ 측정 근거가 아니다. Sand 시간은 리뷰 스스로 *"complementary framework rather than a standalone descriptor"* 라 단서 — 우리 쪽 판단은 §5.

### 4.5 기전 (§5 · p.15–16)
넷 — ① 말단이 국소 전하 분포 · 선호 자리 [113–117] ② 층간 갤러리 = 구속 통로 (확장 ↔ 과구속 시 입체 · 정전 장벽) ③ 고체–고체 계면에서 정전 환경 균질화 · 전기장 집중 완화 · '친리튬/친나트륨' 핵생성 [28, 118] ④ 고분자 전해질에서 결정성 ↓ · 염 해리 ↑ [94]. 결론: '수동 충전재 · 보호 코팅' 이 아니라 '다기능 계면 조절자'. 정량 0.

### 4.6 이온 수송 · 삽입 (§6 · p.16–18 · `Fig. 11`–`Fig. 14` · 식 8)
- σ = nqμ · μ = qD / k_BT (식 8) — MXene 이 n 과 μ 를 동시에 올린다.
- 층간 0.5–1.5 nm [119, 120] · 말단 극성 자리 [121] · *"−O-terminated Ti₃C₂Tₓ … stronger binding and improved transport kinetics for Li⁺ and Na⁺ [122, 123]"* — [122] 는 제목상 **F · Cl · Br 말단** Ti₃C₂ 의 Li 저장 논문. XRD · XPS · NMR 로 가역 삽입 확인 · DFT 결합 −1.2 ~ −2.5 eV · 장벽 ≈0.2–0.4 eV [18] (§3d).
- 2 가 (Zn²⁺ · Mg²⁺): 탈용매 에너지 · 정전 상호작용 [124] · Ti₃C₂Tₓ · Mo₂TiC₂Tₓ 의 Zn²⁺ 삽입 · 수화 Zn²⁺ 공동 삽입 · MXene 유래 수화 바나데이트 [125] · 간격 확장 [126] · g-C₃N₄ 1 wt% [127] · 전기음성 말단 과다 → 이온 포획 [128].
- *"MXene-based materials offer certain advantages over conventional SSEs such as LLZO …, LATP …, and sulfide-based conductors [129–131]"* — [129] **황 담지 MXene 숙주 (알칼리금속–황 전지)** · [130] **Li–S 전지용 MXene 리뷰** · [131] **MXene 전해액 첨가제 Zn 석출** — 'sulfide-based conductors' (황화물 고체 전해질) 와 **'Li–S 전지의 황'** 을 섞은 인용이다.
- `Fig. 11` (실독 · 손 크롭 · 저자 작성): 붉은 구 격자 두 장 (M · X 구분 없음) · O⁻/OH⁻ · F⁻ 말단 · "Interlayer spacing" · "Surface Diffusion" · 이온 **Li⁺ · Na⁺ · Zn²⁺ · Zn²⁺** — 본문 (p.17) 은 *"insertion of various cations (Li⁺, Na⁺, Zn²⁺, and Mg²⁺)"* 라 했는데 **Mg²⁺ 가 없다** (Zn²⁺ 가 두 번).
- Zhang [132] LB-MXene (`Fig. 12` · 미실독): Br/I 공정염으로 F → Br 치환 · 층간 확장 · Ti–Br.
- Xu [24] MLM-EDTA (`Fig. 13` 실독 · `Fig. 14` 미실독): pH 로 전하밀도 조절 → K⁺/Mg²⁺ 선택도 · 수송 저항 · 장벽 · DFT 흡착 · MD 진입/통과 시간 · RDF. 리뷰의 단서: *"primarily performed in liquid-phase membrane systems … useful mechanistic guidance"* (p.17).
- `Fig. 13` (실독): (a) 전하밀도–pH 막대 · (b) 음전하 기원 (수산기 · 카복실 탈양성자) · (c) K⁺/Mg²⁺ 선택도–pH · (d) K⁺/Mⁿ⁺ 선택도–전하밀도 (Mg²⁺ R² 0.98 · Ca²⁺ 0.97 · Li⁺ 0.85 · Na⁺ 0.99) · (e) 선택도 · 수송 저항 · (f) 장벽 막대 (축 단위 'Kcal·mo' 로 잘림) · (g) EDTA 탈양성자 정도별 DFT 흡착 · (h) 저 · 고 전하밀도 채널 모식 (ΔE₁ < ΔE₂). 값은 §3d · §3e.

### 4.7 다가 이온 전지 (§7 · p.18–22 · `Fig. 15` · `Fig. 16` · 반응 V–VII)
- 리뷰의 단서 (p.18): *"much of the current literature on MXenes in multivalent batteries concerns electrode materials rather than true SSEs"* — 이 절은 전극 문헌에서 기전을 옮기는 절이라고 스스로 밝힌다.
- Zn 겔 전해질 [133, 134] · Mg/Al: 분극성 말단이 탈용매 · 이동 장벽을 낮춘다 (DFT "intermediate binding · moderate barriers" — 수치 없음) · Al³⁺ 계는 **"provided that the MXene is electronically isolated by an insulating matrix or converted into a suitable electronically blocking interphase"** (p.20) — 금속성 MXene 의 전자 문제를 리뷰가 가장 분명히 적은 문장.
- 전극 사례 [135–142] (§3f). 한계: 수계 창 좁음 · 다가 이온 이동도 낮음 · 산성 · 할라이드 풍부 전해질에서의 안정성.
- `Fig. 15` (실독 · [142]): (a) GITT 충방전 (*"Disharge"* 원 그림 오타) · (b) 한 펄스 (IR drop · ΔE_τ · ΔE_s — 세로축 맨 위 눈금이 '76' 으로 찍힘 = 0.76) · (c) D_Zn²⁺ — 점들이 `figure-read ≈` **2×10⁻⁹ – 1.5×10⁻⁸ cm² s⁻¹** 에 있다 (본문 "10⁻⁷–10⁻⁸") · (d) Nyquist + 등가회로 (R_s · CPE1‖R_f · CPE2‖(R_ct + Z_W)) · 반원 위 **"22 Ω"** [그림 인쇄] (반원은 Z_re ≈ 2–32 Ω 걸침 `figure-read`). ⚠ 본문 p.21 은 *"illustrated in Figure 15 … In this schematic, multivalent cations such as Zn²⁺, Mg²⁺, and Al³⁺ intercalate …"* 라고 **개념도로 설명**하는데 실제 `Fig. 15` 는 GITT · EIS 자료다. 본문의 GITT 문장 인용은 **[50]** (일반 MXene 리뷰) 이고 캡션은 [142] 다.
- `Fig. 16` (실독 · 저자 작성): 수계 · 비수계 'MXene-Based Electrolyte' 상자 → 육각 판 적층 사이로 Zn²⁺ · Mg²⁺ 경로 → Mg 음극. **Al³⁺ 가 없다** (본문 p.22 는 Zn²⁺ · Mg²⁺ · **Al³⁺** 라 적음) · 'Zn²' (+ 빠짐) · 'Non-aqueous' 상자 안에 **물 분자**가 그려져 있다.
- 반응 V–VII (Zn · Mg · Al 석출) · 건조 SSE 에서는 수화 이온 공동 수송이 아니라 고분자 배위 · 말단 · 결함 · 자유부피가 지배 (p.22 — 맞는 구분) · 비-Ti MXene [143].

### 4.8 안정성 · 확장성 (§8 · p.22–24 · `Fig. 17` · `Fig. 18`)
- 산화 [144–147] (§3g) · 고온 공정 (열간 가압 · 어닐) 에서 가속 → 캡슐화 (고분자 · 불활성 산화물 · 보호 매트릭스) · in situ 중합으로 순응 피복.
- 열 300–500 °C (인용 없음) · 넓은 창 (인용 없음) · **Li/Na 금속 쪽 기생 피막 · 전이금속 환원** 가능 (p.23 — 금속 음극 인터레이어 서술과 긴장 관계인데 같은 절에서 풀지 않는다).
- `Fig. 17` (미실독 · [144, 148]): 탈염 성능 · 안정성 · 전도도 · pH · 염 흡착 · 에너지 효율 + Ar 스퍼터 전후 말단 정량 (식단위당 Tₓ 이론값 2) — 축전식 탈염 (CDI) 논문을 '안정성' 절에 놓음.
- 확장성: HF → 플루오라이드염–HCl · 용융염 · 전기화학 박리 · 롤투롤 · 잉크젯.
- `Fig. 18` (실독 · 저자 작성): 상자 넷 — Oxidation (말단 산화 · 대기 열화) / Stability (열 · 전기화학 안정 · 캡슐화) / Scalability (대량 안전 합성) / Properties (전하 이동도 · 기계 · 일함수 · 전기전도 · **광학**). 전압 · 수치 0 · 본문의 '물이 매개' [145] 와 '저전위 · Li 금속 접촉 열화' 는 그림에 없다.

### 4.9 전망 · 결론 (§9–10 · p.24–26 · `Table 4` · `Fig. 19`)
- `Table 4` (텍스트 전사): MXene (조절 가능 · −O · −OH · −F · 중간 (산화 민감) · SSE 충전재 · 계면층 · [96]) / GO (중간 · 에폭시 · 수산 · 카복실 · 카보닐 · 좋음 · 충전재 · 장벽층 · [19] — **MXene 막 리뷰**) / h-BN (낮음 · 불활성 · 열 안정 우수 · 분리막 · 절연층 · [149]) / MoS₂ (중간 · 불활성 기저면 · 고전압 제한 · Na⁺ · Zn²⁺ 인터레이어 · [150] — **축전식 탈염**) / g-C₃N₄ (중간 (Na⁺ · Li⁺) · 질소 풍부 · 건조 SSE 안정 · 복합체 이온 수송 매트릭스 · [151] — 일반 리뷰). 정성 칸뿐이다.
- 네 기둥 (p.25–26): ① DFT · ML 설계 규칙 [148, 152–156] — [155] · [156] 은 **저자 자신의 헥사페라이트 · 영구자석 ML 논문** ② 덜 탐색된 조성 (Mo₂TiC₂Tₓ · Nb₄C₃Tₓ · 질화물) · MOF/COF 이종구조 [18, 23, 157] ③ 전셀 통합 (Li–MXene SSE–LFP · Na–MXene SSE–Na₃V₂(PO₄)₃) [158–160] — **미생물 연료전지 · NH₃ 가스 센서 · 연료전지 리뷰** ④ 시험 · 보고 표준화 [161] — MXene 안전 · 지속가능성 논문.
- `Fig. 19` (실독 · 손 크롭 · 저자 작성): 중앙 'MXene-Based SSEs' + 기둥 넷 (Design Rules — HT DFT 선별 · ML 표면 조정 · 이온별 경로 최적화 / Less Explored MXenes & Heterostructures — **"Mo₂TiC₃Tₓ"**, Nb₄C₃Tₓ · 질화물 · MXene–MOF/COF / Full-Cell Integration — Li–SSE–양극 · 계면 안정 / Standardization & Reporting — σ · EIS 프로토콜 · 습도 · 온도 통제). 본문 (p.25) 은 **Mo₂TiC₂Tₓ** — 그림과 다르다.
- 장기 안정 (p.26): 보관만이 아니라 전기화학 · 열 · 기계 · 화학 응력 동시 · Li/Na 금속 · 양극 · 고분자 · 세라믹 · 분해 산물과의 반응 → **"stability maps"** (조성 · 말단 · 환경 · 전위 · 온도) · operando · *"realistic conditions involving high areal loadings, limited excess metal, elevated temperatures, and long-term cycling rather than … short-term symmetric-cell measurements"* [163–166].
- 결론 (p.26): MXene 이 *"address some of the most critical challenges faced by conventional SSE systems"* — 본문 단서보다 강한 문장으로 끝난다.

## 5. 식 · 반응식 — 리뷰가 쓴 것과 우리 판단

| 식 | 리뷰가 쓴 것 | 우리 판단 |
|---|---|---|
| 반응 (I) · (II) | HF 식각 | (II) 는 말단 형성 반응물 (HF · H₂O) 을 안 써서 **물질수지가 안 맞는 단순화** |
| 반응 (III) | ZnCl₂ 용융염 → Ti₃C₂Cl₂ | 물질수지 맞음. **Cl 말단 · 무 O/H** 경로라 황화물과의 화학 궁합을 물을 때 이쪽이 출발점이다 [추정 — §11-3] |
| (1) Nernst–Einstein | σᵢ = Σ nᵢzᵢ²e²Dᵢ / k_BT | 우리 MLIP σ 환산과 같은 형식 (Haven = 1 가정) — 상관 무시라는 같은 한계 |
| (2) Arrhenius · (3) VTF | PEO 계는 VTF | 맞는 구분. 'MXene 이 Ea 를 낮춘다' 는 **인용 없음** |
| (4) 공간전하 Δφ = qN_D d² / (2εε₀) | 1차원 공핍 근사 | 반도체 식 (도너 농도 N_D) 그대로 — SSE 에서는 Li 공공 · 침입 결함 농도로 읽어야 한다. 수치 0. 계면 공간전하의 DFT 원전은 [Haru14] (산화물 양극–황화물) — 리뷰 미인용 |
| (5) R_int = 1 / (2π f_max C_eff) | 계면 저항 '추정' | RC 관계식 — C_eff 를 따로 알아야 해서 독립 추정법이 아니다 |
| (6) Sand 시간 t = πD(zFc₀)² / [4J²(1−t₊)²] | 덴드라이트 없는 사이클 근거 | **t₊ → 1 (단일 이온 전도체 — 황화물 · 산화물 SSE) 이면 t_Sand → ∞** — 농도 고갈 기준이 성립하지 않는다. 무기 SSE 의 덴드라이트는 기계 · 공극 · 전자 누설 쪽이다. 리뷰는 '보조 틀' 이라 단서를 달았지만 t₊ 극한은 말하지 않는다 |
| (7) Butler–Volmer | MXene 이 j₀ 를 올린다 | 인용 [16–21] 이 j₀ 측정 근거가 아니다 (§10a) |
| (8) σ = nqμ · μ = qD/k_BT | n · μ 동시 증가 | (1) 과 같은 내용 |
| 반응 (IV)–(VII) | Li · Zn · Mg · Al 석출 | 서술용 |

## 6. DFT / 계산 방법 ★ — 이 리뷰의 계산 층위
- **code / functional (+vdW) / pseudo · PAW / k-points · ecut · supercell · nat / DFT+U / AIMD / MLIP / 무질서 처리**: 전부 **n/a** — 자체 계산이 없고, 인용한 계산의 조건도 한 줄도 옮기지 않았다 (본문에 PBE · VASP · vdW 0 회).
- **리뷰가 계산을 쓰는 자리**:

| 종류 | 인용 | 무엇의 근거로 | 쪽 |
|---|---|---|---|
| DFT 흡착 · 결합 (고분자 · Li⁺ · TFSI⁻ — MXene 슬랩) + ELF | [103] `Fig. 7` | mPEG 그래프트가 PVDF-HFP 결합 · Li⁺ · TFSI⁻ 흡착을 세게 한다 | p.11 |
| DFT 결합 (SO₃H 자리) | [67] | Li⁺ 선택 수송 (약한 결합) | p.6 |
| DFT 결합 · 장벽 범위 (Li⁺) | [18] (리뷰) | MXene 층간 Li⁺ 수송이 빠르다 | p.16 |
| DFT 흡착 (EDTA–K⁺ · Mg²⁺) + MD (진입 · 통과 · RDF) | [24] `Fig. 13` · `Fig. 14` | 전하밀도 → K⁺/Mg²⁺ 선택 | p.17 |
| 제일원리 표면 조성 · 안정 | [146] | O 포화 표면 · Sc 플루오린화 | p.23 |
| ML (밴드갭 예측 · 슈퍼커패시터 · MXene–AI) | [152–154] | 설계 규칙 기둥 | p.25 |
| "DFT studies support … intermediate binding energies and moderate diffusion barriers for Mg²⁺ and Al³⁺" | **인용 없음** | 다가 이온 이동 | p.19 |

- **리뷰가 계산에 대해 하지 않은 것**: 전하를 띤 흡착종을 금속성 슬랩에서 어떻게 다뤘는지 · 흡착 기준 상태 · 슬랩 두께 · 진공 · 말단 배열 (−O/−OH/−F 혼합의 무질서 처리) · 스핀 · U · 분산 보정 — 하나도 없다. MXene 말단은 실제로 −O · −OH · −F 가 섞인 **무질서 표면**이라 단일 말단 슬랩의 결합에너지는 '그 배열에서의 값' 이다 (우리 쪽 무질서 규율과 같은 질문).

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md` · `db/properties/canonical_registry.json`

> 이 리뷰에는 argyrodite 값이 **하나도 없다**. 그래서 이 절은 **값 대조가 아니라 양 · 정의 · 방향 대조**다. 우리 쪽 칸에는 숫자를 싣지 않는다 (값은 원장에서만).

| 항목 | 이 리뷰 | 우리 (값은 원장에서만) | 차이 / 이유 |
|---|---|---|---|
| 전자구조 (축 D) | Ti₃C₂Tₓ 금속성 · Mo₂TiC₂Tₓ 반도체성 [92] — 수치 0 | comp1 · modelc **넓은 띠틈 절연체** (fixed-occ nscf 고유값 · `gap-fixedocc-eigenvalue-v1` canonical) | 전자 성격이 정반대다. MXene 을 SE 계면에 넣으면 그 계면의 **전자 경로를 무엇이 끊는지**를 먼저 적어야 한다 — 우리 계에서는 SE 자신이나 절연 코팅이 그 역할 (§11-1) |
| 이온전도 (축 A) | MXene–고분자 ~10⁻⁶–10⁻⁴ S cm⁻¹ (`Table 2` · 2 차) · 'sulfides > 10⁻²' (서론) · Li⁺ 층간 장벽 ≈0.2–0.4 eV (3 차) | MLIP-MD (UMA) Arrhenius · Nernst–Einstein — **계 간 상대차로만** | 계 · 양 · 방법이 다 다르다. 비교 행 없음. MXene 충전재가 황화물 SE 의 벌크 σ 를 올린다는 근거는 이 리뷰에 없다 |
| 산화 안정 (축 B) | MXene 은 '고전압 · 습기에서 산화' (수치 0) · 복합 전해질 '창' 3.3–4.2 V (LSV 조건 미기재) · Li₂TiO₃ 코팅 "up to 4.5 V" [107] | grand-potential **층① 분해 개시** (S²⁻ 한정) · 양극 쪽 판단은 우리 셀 작동창 2.5–4.25 V vs Li | 리뷰의 '창' 은 겉보기 LSV 창 · 우리 것은 열역학 분해 개시 — **다른 양**. 금속성 MXene 이 양극 쪽에서 LPSCl 에 닿으면 SE 에 양극 전위의 전자 통로를 붙이는 셈이라 산화를 막는 쪽이 아니다 — 막는 것은 Li₂TiO₃ 같은 절연 전환층 (§11-2) |
| 기계 (축 C) | MXene 나노시트가 고분자 영률 · 인장강도 ↑ (수치 0) · 덴드라이트 물리 장벽 | DFT 탄성 (C_ij · VRH) · BM3 EOS | 대응 양 없음 |
| 환원 · Li 금속 (축 E) | MXene 인터레이어 = 덴드라이트 억제 · 계면 저항 ↓ (Li 금속 과 무기 SSE 사이 1차 근거 0) · Sand 시간 | 환원 가장자리 = 문헌 경계와 같은 자리 (`our_dft_baseline.md` 2026-09-22 정정 절) | 0 V (Li 전위) 는 LPSCl 창 밖이다 (문헌 환원 개시 ≈1.7 V vs Li · [Zhu15] · [Schw21]). 금속성 인터레이어는 그 0 V 를 SE 면으로 그대로 옮긴다 (§11-1) |
| 흡착 · 결합에너지 규율 | ≳ 2 eV 값 셋 (`Fig. 7`) · 전하 종 · 기준 상태 미기재 | `D-2026-10-05-adsorption-site-coordination` — 결합 자리 배위수부터 · 구조 없으면 '배위 미확인' | 이 리뷰의 값은 '배위 미확인' 등급으로만 다룬다 |
| ELF | 색 막대 · 단면 · 등치값 없는 그림 한 장 | 우리 ELF (Nd 트랙 · `D-2026-10-19-nd-q23-ppswap-structure`) | 우리 그림은 색 막대 · 단면 (hkl · 오프셋) · 판별량 (예 P–S 중앙 최솟값) 을 같이 싣는다 — 반면교사 |
| 점착 | `Fig. 7b` E_i (eV/셀) | 점착 W_ad (J m⁻² · 값은 원장 · 여기 싣지 않음) | 다른 양 · 같은 표 금지 |

## 8. Figure set ★
크롭 23 장 (그림 19 + 표 4 · 손 크롭 3) · **그림 11 장 실독** · 저자 작성 개념도 8 · 재수록 11.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (실독 · 저자 작성) SSB 과제 (느린 Li⁺ · 균열 · 덴드라이트) ↔ MXene 해결 (빠른 Li⁺ · SSE/MXene/Li · 덴드라이트 억제) + 이점 목록 (High conductivity · 표면 조절 · 유연성 · **Hydrophilic interlayers**) | 쓰지 않는다. 'High conductivity' 가 전자전도라면 SE 계면에서는 위험 인자 · 친수성은 황화물에 위험 (§11-3). 깨진 글리프 · 덮인 'Li' |
| 2 | (실독 · 저자 작성) 7 단계 연표 2011 → 현재 | 연대가 본문과 한 칸 어긋남 (고분자 복합 2018–20 ↔ 본문 '2020 이후'). 황화물 SE 없음 |
| 3 | (미실독 · 캡션) 박리 MXene SEM · TEM · HRTEM · 여과막 단면 [62] | — (두께 1.27 nm · 막 3.2 µm 는 본문 값) |
| 4 | (미실독 · 캡션) 메모리 커패시터 C–V · ON/OFF [62] + MXene–PSS 막 확산 전위 · 출력 [67] | — (액상 막) |
| 5 | (실독 · 손 크롭 · 저자 작성) MXene–고분자 복합 전해질 개념도 — 제조 · 대표계 · ↑σ ↑강도 ↑열 안정 | 전자 누설 경고가 그림에서 빠졌다 — 본문 p.8–9 의 단서와 함께 봐야 한다. 'Layer-by-layar' 오타 |
| 6 | (미실독 · 캡션) MXene 결합 수송망 SPE · 제조 · PEO/LiTFSI/**MnO₂** · 판상 **LLZAO** [94–98] | (c)–(e) 는 MXene 이 아니다 · '[95] Li et al.' 은 1 저자 Cheng |
| 7 | (실독) ELF (MXene–PH · MP–PH · **색 막대 없음**) · E_i −1.166 / −3.268 eV · 흡착 E_a −0.650 / −2.148 / −1.096 / −3.605 eV [그림 인쇄] · Li 석출 모식 [103] | ≳ 2 eV 셋은 배위 미확인 · 'E_a' = 흡착 (활성화 아님) · MP–TFSI⁻ 의 음이온은 MXene 면이 아니라 사슬 끝 (`figure-read`). 대상은 고분자 전해질 |
| 8 | (미실독 · 캡션) MXene–F,N 탄소–CoSe₂ 이종구조 합성 [106] | — (HER · 슈퍼커패시터 원전) |
| 9 | (미실독 · 캡션) 같은 계의 CV · GCD · 율속 · Nyquist [106] | — 바로 뒤 'SSB 인터레이어 개선' 문단과 무관한 자료 |
| 10 | (실독 · 저자 작성) Li 금속 / MXene 인터레이어 / SSE + 층간 Li⁺ 수송 확대 · (i)–(iv) 이점 | 기하 오류 둘 (석출 화살표 · 덴드라이트가 Li 바깥 면 · Li⁺ 가 기저면 수직 관통) · 전자 경로 없음 — §11-1 질문의 반례 그림 |
| 11 | (실독 · 손 크롭 · 저자 작성) MXene 층간 이온 수송 · 삽입 모식 (Li⁺ · Na⁺ · Zn²⁺ · Zn²⁺ · O⁻/OH⁻ · F⁻ · 표면 확산) | 본문의 Mg²⁺ 가 그림에 없다 |
| 12 | (미실독 · 캡션) Lewis 염기 할라이드 처리 LB-Ti₃C₂Tₓ — SEM · XRD · HAADF · EDS · XPS (Ti–Br) [132] | 할라이드 말단 MXene 경로의 원전 위치만 |
| 13 | (실독) MLM-EDTA 막 전하밀도 · K⁺/Mⁿ⁺ 선택도 · 수송 저항 · 장벽 (kcal mol⁻¹) · DFT 흡착 · 기전 모식 [24] | 홉 수 검산으로 장벽 차 ↔ 선택도 차수 모순 (§3d) — '겉보기 장벽' 으로만 |
| 14 | (미실독 · 캡션) MD 스냅숏 · K⁺ · Mg²⁺ 진입/통과 시간 · RDF · 기전 [24] | — (수화 이온 · 액상) |
| 15 | (실독) HVO/MX GITT · 한 펄스 · D_Zn²⁺ (`figure-read ≈` 2×10⁻⁹–1.5×10⁻⁸) · Nyquist (22 Ω) [142] | 본문 D 범위가 한 자리 높고 본문은 이 그림을 '개념도' 로 설명한다 |
| 16 | (실독 · 저자 작성) 다가 이온 MXene 전지 모식 — 수계 · 비수계 · Zn²⁺ · Mg²⁺ · Mg 음극 | 본문의 Al³⁺ 가 그림에 없다 · 'Non-aqueous' 상자에 물 분자 |
| 17 | (미실독 · 캡션) Ti₃C₂Tₓ 계 탈염 성능 · 안정 · 전도 · pH · 흡착 · 효율 + Ar 스퍼터 전후 말단 정량 [144, 148] | 말단 정량 (식단위당 Tₓ ≈ 2 기준선) 의 원전 위치만 |
| 18 | (실독 · 저자 작성) 과제 · 완화 인포그래픽 (산화 · 안정 · 확장성 · 물성) | 정성 · 수치 0 — 쓰지 않는다 |
| 19 | (실독 · 손 크롭 · 저자 작성) 전망 로드맵 네 기둥 | 'Mo₂TiC₃Tₓ' ↔ 본문 'Mo₂TiC₂Tₓ' |
| Table 1 | 선행 MXene 리뷰 여섯 [18]–[24] 의 범위 · 한계 · 이 리뷰가 메우는 것 | [14] · [47] (같은 주제 리뷰) 누락 |
| Table 2 | MXene–고분자 복합 전해질 네 행 (σ · 창 · 제조) | §3b 전사 · σ_e · t_ion 열 없음 · 젤라틴 행 인용은 MXene 없는 하이드로겔 |
| Table 3 | MXene 계면 적용 네 행 (음극 · 양극 · 벌크 · 혼성) | §3c — 넷 중 셋의 인용이 그 행의 계와 안 맞는다 |
| Table 4 | MXene · GO · h-BN · MoS₂ · g-C₃N₄ 정성 비교 | 정성 칸 · 인용 셋이 막 리뷰 · 축전식 탈염 · 일반 리뷰 |

## 9. Post-processing ★
- **무엇**: 해당 없음 (리뷰 · 자체 분석 0).
- **리뷰가 근거로 든 분석 기법** (이름만 · 조건 없음): XPS (말단 정량 · Ti–Br · 옥시플루오라이드) · XRD (층간 간격) · NMR (삽입 가역성) · HAADF-TEM · EDS · EIS + 등가회로 (식 5) · GITT (D_Zn) · LSV '창' (`Table 2`) · ELF · DFT 흡착 · MD RDF.
- **수치화 · 플롯 · 기록 방식**: 없음. 리뷰가 요구만 한다 — σ_ion · σ_e · t_ion 동시 보고 (p.9) · 습도 통제 · 셀 구성 · 보고 지표 표준화 (p.25) · '안정성 지도' (p.26).

## 10. 비판 ★

### 10a. 직접 확인한 것 (PDF 안에서 본문 ↔ 그림 ↔ 표 ↔ 참고문헌 목록을 맞춘 결과)

**(1) 그림–본문 어긋남 (그림을 실제로 보고 찾은 것)**

| 자리 | 본문 · 캡션 | 그림 |
|---|---|---|
| `Fig. 11` (p.17) | "Li⁺, Na⁺, Zn²⁺, and Mg²⁺" | Li⁺ · Na⁺ · Zn²⁺ · Zn²⁺ — **Mg²⁺ 없음** |
| `Fig. 15` (p.21) | "In this schematic, multivalent cations such as Zn²⁺, Mg²⁺, and Al³⁺ intercalate …" | 개념도가 아니라 **GITT · EIS 자료** ([142]) |
| `Fig. 15c` (p.22) | D_Zn "mainly concentrated in the range of 10⁻⁷–10⁻⁸ cm² s⁻¹" | 점이 `figure-read ≈` **2×10⁻⁹ – 1.5×10⁻⁸** — 10⁻⁷ 근처 점 없음 |
| `Fig. 16` (p.22) | "Zn²⁺, Mg²⁺, and Al³⁺" | Zn²⁺ · Mg²⁺ 만 — **Al³⁺ 없음** |
| `Fig. 19` (p.25) | "Mo₂TiC₂Tₓ and Nb₄C₃Tₓ" | **"Mo₂TiC₃Tₓ"** · Nb₄C₃Tₓ |
| `Fig. 2` (p.2–3) | 삽입 · 막 "approximately 2016 and 2020" · 고분자 복합 "From 2020 onward" | 삽입 2014–16 · 막 2016–18 · 고분자 복합 **2018–20** |

그 밖에 그림 자체의 문제: `Fig. 10` 석출 화살표 · 덴드라이트 위치 · 기저면 수직 관통 (§4.4) · `Fig. 7a` 색 막대 없음 · `Fig. 5` 전자 누설 단서 누락 · `Fig. 1` 깨진 글리프.

**(2) 인용 어긋남 — 제목 수준 대조 (원 논문은 열지 않았다)**

| 본문 자리 | 인쇄 인용 | 그 번호의 목록 항목 (제목 요지) | 판정 |
|---|---|---|---|
| p.6 Tong MXene–PSS 문단 끝 | [38] | Ti 탄질화물 MXene Na 이온 전지 (2018) | 어긋남 — Tong 은 [67] |
| p.3 이온–전자 퍼콜레이션 균형 | [41–43] | [43] **FeS/FeOx 중공 나노구 양극 자기조립** | [43] 무관 |
| p.5 "−F 는 이온 전도에 덜 유리" | [56] | 2D 반도체와 Schottky 장벽 없는 MXene 접촉 (JACS 2016) | 주제 다름 (전자 접촉) |
| p.9 이온–전자 분리 전략 (절연 · 그래프트 · 유전 스페이서 · 배향) | [60] | 폴리프로필렌 비등온 결정화 | 어긋남 |
| p.9 MXene–고분자 SSE 전망 | [61–65] | 도핑 리뷰 · 메모리 커패시터 · EMI 차폐 리뷰 · h-BN 리뷰 · TMD 패시베이션 HER | 어긋남 |
| p.9 "Li et al. [95] … LLZAO" | [95] | Cheng 외 판상 가넷 (1 저자 Cheng) | 이름 어긋남 — Li 는 [98] (MnO₂) |
| p.12 MXene 층이 Li 석출 균일 · 덴드라이트 억제 | [72] | MXene 막의 전압 게이트 1가 양이온 분리 (Sci. Adv. 2024) | 어긋남 (막 분리) |
| p.12 VN MXene Fe 자리 → Li 덴드라이트 억제 | [105] | 제목 "… Toward Invigorated **Lithium–Sulfur** Batteries" | 계가 다름 (Li–S) [제목 수준] |
| p.12–13 산화물 SSE Ti₃C₂Tₓ 인터레이어 · Na 금속 Nb₂C · Ti₂C 인터레이어 · `Table 3` | [108–112] | Mo-MXene LiF-rich SEI · 준고체 Li–I · LATP/LFP 복합 양극 (MXene 없음) · **열전 하이드로겔 (실어증 환자 간호)** · Ti₃C₂@TiO₂ LIB | 간판 주장의 1차 근거 0 |
| p.15 MXene 이 j₀ 를 올린다 | [16–21] | Seino 2014 황화물 유리세라믹 · SSB 리뷰 · MXene Chem. Rev. · 막 리뷰 · 개관 · 음극 리뷰 | j₀ 근거 아님 |
| p.16 "−O 말단 Ti₃C₂Tₓ 가 Li⁺/Na⁺ 결합 · 수송에 유리" | [122, 123] | [122] **F · Cl · Br 말단** Ti₃C₂ Li 저장 | [122] 말단이 다름 |
| p.17 LLZO · LATP · **sulfide-based conductors** 대비 장점 | [129–131] | **황 담지 MXene (알칼리금속–S 전지)** · **Li–S 전지 MXene 리뷰** · MXene 전해액 첨가제 Zn 석출 | 황화물 SE 와 Li–S 의 황을 섞음 |
| p.21 HVO/MX GITT | [50] | 일반 MXene 리뷰 (에너지 · EMI · 생체의학) | 어긋남 — 캡션은 [142] |
| `Table 2` PVDF-HFP 행 · 젤라틴 행 | [86, 87] · [89, 90] | Ti₃C₂Tₓ 처리 분리막 (액체) · MXene 없는 PVDF-HFP 전해질 · KI 젤라틴 하이드로겔 EDLC · 젤라틴–알지네이트 겔 슈퍼커패시터 | 행의 계를 받치지 않음 |
| `Table 4` GO · MoS₂ · g-C₃N₄ 행 | [19] · [150] · [151] | MXene 막 리뷰 · MXene/MoS₂ **축전식 탈염** · g-C₃N₄ 일반 리뷰 | 행의 성질을 받치지 않음 |
| p.25 ML 설계 규칙 | [155, 156] | 저자 자신의 Sr 헥사페라이트 보자력 · 영구자석 (BH)max ML | 주제 다름 (자기 인용) |
| p.25 전셀 시제품 · 실패 양식 | [158–160] | 미생물 연료전지 생체막 · Pt/MXene NH₃ 가스 센서 · 연료전지 MXene 리뷰 | 어긋남 |

- 참고문헌 목록: 166 번호 전부 본문에서 한 번 이상 인용 · **[6] = [25]** (같은 Gogotsi 책 · 출판사 표기만 CRC Press / Jenny Stanford) · 저자 이름이 겹치는 항목 7 ([12] · [13] · [61] · [66] · [143] · [155] · [156] — 이름 일치 기준).
- ⚠ 이 표는 **제목 수준** 판정이다. 원 논문 본문에 그 내용이 들어 있을 가능성은 남아 있다 (특히 리뷰 [14] · [44] · [47]). 그래도 '그 문장의 근거로 이 번호를 단다' 는 대응은 성립하지 않는다.

**(3) 같은 리뷰 안의 모순**
- 전기화학 창: p.21 "relatively narrow" ↔ p.23 "relatively wide … outside the typical operational range" — 둘 다 인용 · 수치 없음.
- −F 말단: p.5 "less favorable for ion conduction" ↔ p.15 "cannot be classified universally" ↔ `Fig. 5` 는 −F 도 '이점' 쪽.
- 보고 규율: p.9 σ_ion · σ_e · t_ion 동시 보고 요구 ↔ 자기 `Table 2` 에 σ_e · t_ion 열 없음.
- 간판 서사: `Fig. 1` · `Fig. 10` · `Table 3` · 결론 (맨 MXene 인터레이어 = 해결) ↔ p.4 · p.11 · p.20 (전자 차단 MXene 유래 계면상 · 절연 매트릭스로 격리 · 전환).

### 10b. 과학 내용에 대한 판단
1. 🔴 **금속성 인터레이어는 전자 차단층이 아니다** — 리뷰가 "conductive interphases that … electronically passivate unstable interfaces" (p.7) 라 쓴 문장은 그 자체로 모순이다. 전자전도 층을 SE 와 전극 사이에 넣으면 그 층은 전극 전위에 놓이고 SE 의 분해 계면을 **옮기거나 넓힌다**. 이것이 해로운지는 SE 의 분해 산물이 부동태화하는지에 달려 있다 (LPSCl 은 Li 쪽에서 Li₂S · Li₃P · LiCl 계면상 — 문헌은 대체로 자기 제한적으로 보고 ([Banerjee20Rev] 2 차), 우리 원장은 Li₃P 를 conductor-LEAK 후보로 둔다 · `comparison_vs_ours.md` §E 맨 위 행). 리뷰는 이 질문을 묻지 않는다 (§11-1).
2. 🔴 **간판 주장의 1차 근거 부재** — Li 금속과 무기 SSE 사이 MXene 인터레이어 실험이 이 리뷰의 인용 안에 (제목 수준) 없다. 확인된 무기 SSE + MXene 1차 사례는 양극 쪽 [107] 하나이고 거기서 MXene 은 사라졌다 (Li₂TiO₃ 로 전환).
3. 🟠 **흡착 · 결합에너지 보고** — 금속성 슬랩 위 전하 종 (Li⁺ · TFSI⁻) 의 기준 상태 · 전하 보정 · 셀 크기 의존이 없고, 'E_a' 표기가 활성화에너지와 겹친다. ≳ 2 eV 값은 배위 미확인. MP–TFSI⁻ 그림은 음이온이 MXene 면에서 멀다.
4. 🟠 **Sand 시간 · 공간전하 · R_int 식** — 일반식을 나열하고 무기 SSE 극한 (t₊ → 1) · 결함 화학 · RC 관계의 순환을 말하지 않는다. 식에 대입한 예가 하나도 없다.
5. 🟠 **'친수성 = 이점' 서사** — 고분자 · 수계 · 겔에서는 맞을 수 있지만 황화물 SE 에서는 수분 → H₂S · P–O 치환 경로다 ([Kim26Moist]). 리뷰는 SSE 화학별로 이 판단을 가르지 않는다.
6. 🟢 **리뷰가 잘한 것** — 단서 문장은 정확하다: 액상 · 겔 · 수계 결과 ≠ 전고체 (p.4) · H-MXene σ 를 건조 SSE 와 비교 말 것 (p.6) · 덴드라이트 억제를 기계 강도로만 돌리지 말 것 (p.11) · 양극 쪽은 원래 MXene 보다 전환된 계면상이 중요할 수 있다 (p.11) · 다가 이온 문헌 대부분은 전극이지 SSE 가 아니다 (p.18) · σ_ion · σ_e · t_ion 동시 보고 (p.9) · 짧은 대칭셀 대신 현실 조건 (p.26). **문제는 단서가 그림 · 표 · 결론으로 올라가지 않는다는 것**이다.

## 11. 우리 일과의 연결 ★★ (값을 섞지 않는다 — 방법 · 정의 수준)

### 11-1. 금속성 계면층을 황화물 계면에 놓으면 — 물어야 할 순서
1. **이 층은 전자를 통하나 막나** — MXene (Ti₃C₂Tₓ) 은 통한다. 그러면 그 층과 닿은 SE 면은 전극 전위에 놓인다.
2. **그 전위가 SE 창 안인가** — Li 쪽 0 V 는 LPSCl 창 밖 (문헌 환원 개시 ≈1.7 V vs Li · [Zhu15] · [Schw21]) · 양극 쪽 우리 셀 작동창 2.5–4.25 V 는 통째로 산화 개시 위다 (문헌 [Schw21] 산화 2.01 V) ⇒ 어느 쪽에서도 금속성 층은 SE 를 보호하지 못하고 **반응 면을 옮긴다**.
3. **옮겨진 반응 면이 부동태화하나** — 문헌은 Li 쪽 LPSCl 계면상 (Li₂S · Li₃P · LiCl) 을 대체로 자기 제한적으로 본다 ([Banerjee20Rev] 2 차 서술). 우리 원장은 Li₃P 를 전자 누설 후보로 둔다 (`comparison_vs_ours.md` §E 맨 위 행 — 인용 시 조건절). 표면적이 큰 MXene 은 그 반응 면을 넓힌다 [추정].
4. **그래도 이점이 있나** — 전자전도 인터레이어가 황화물에서 쓰이는 실례는 있다: Ag–흑연 ([`spencerjolly2023_…`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) — Li 가 전기화학적으로 흑연에 들어간 뒤 Ag 와 합금화) · 탄소 인터레이어 ([`liao2025_…`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) — **접착 인성이 Li 석출 위치를 정한다**: 인터레이어 위냐 아래냐). 즉 금속성 층의 판정 변수는 '친리튬 말단' 이 아니라 **Li 가 어디서 석출되고 그 면이 SE 와 어떻게 붙어 있느냐**다 — 이 리뷰는 그 축을 다루지 않는다.
⇒ 우리 계에서 MXene 류를 말할 때는 **'전자전도 인터레이어'** 와 **'전자 차단 코팅'** 을 이름으로 갈라 쓴다 (ESW 의 '층①/층②' 명명 규율과 같은 꼴).

### 11-2. MXene → Li₂TiO₃ 전환 코팅 ([107]) 과 [혁주] LZO 트랙
- [107] 에서 실제로 계면을 지키는 것은 **Li₂TiO₃** (절연 Li 산화물) 다 — LiNbO₃ · Li₂ZrO₃ 와 같은 '절연 Li 이온전도 코팅' 계열이고, MXene 은 균일 피복을 위한 **전구체** 역할이다. [혁주] 트랙의 Li₂ZrO₃ (LZO) 코팅과 같은 Li₂MO₃ 꼴이라 비교 대상 후보로 적어 둔다 (`kb/projects/hyeokju_lzo_interface_2026_11_16.md`).
- 같은 물질의 문헌 계산값 ([litdb 카드] [Kim26HTS] `Table S1` · 재입력 CSV `db/properties/kim2026_tableS1_88_candidates.csv` · MP-PBE · 그 논문의 규약): Li₂TiO₃ 산화 한계 **3.68 V** · 환원 한계 **0.50 V** · ΔE_rxn(NCM523) **0** · ΔE_rxn(LPSCl) **−60.12 meV/atom**. ⇒ (i) 산화 한계 3.68 V 가 [107] 의 "up to 4.5 V" 작동보다 낮다 — '전기화학적으로 안정' 은 열역학 창 밖 운용이라 **동역학 보호로 읽어야** 한다 [추정]. 우리 셀 작동창 2.5–4.25 V 의 윗부분도 그 한계 위다. (ii) LPSCl 과의 반응에너지가 0 이 아니다 — 양극 쪽에서는 안 반응하고 SE 쪽에서 반응하는 모양은 [Kim26HTS] 가 지적한 코팅 일반의 비대칭 (`comparison_vs_ours.md` §B③ — 구속은 SE 쪽이 건다) 과 같다.
- ⛔ 이 값들은 [Kim26HTS] 의 규약 값이다 — 우리 [혁주] 계산값과 같은 표에 놓지 않는다. 비교는 '같은 양 (혼합 반응에너지) 을 같은 규약으로 다시 낸 뒤' 에만.

### 11-3. 친수성 · −OH 말단 = 황화물에는 위험
- 리뷰는 −OH · −O 말단 · 친수성 · 층간 물을 이점으로 쓴다 (`Fig. 1` "Hydrophilic interlayers"). MXene 열화는 **물이 매개**한다 ([145]) — MXene 은 층간에 물을 붙들고 있다.
- LPSCl 은 수분과 만나면 P–O 치환 · H₂S 로 간다 ([Kim26Moist] — `comparison_vs_ours.md` §B⑤). ⇒ 황화물 쪽에서 MXene 을 생각한다면 출발점은 **무 O/H 말단 · 건조 공정** — 리뷰 반응 (III) 의 ZnCl₂ 용융염 **Cl 말단 Ti₃C₂Cl₂** 나 LB 할라이드 처리 ([132]) 쪽이다. Cl 말단 MXene 과 Cl 풍부 argyrodite 의 화학 궁합은 **아무도 계산하지 않은 질문**으로 보인다 (이 리뷰 · 우리 litdb 범위에서 0 건) [추정].

### 11-4. 우리 브리핑 · 원고에 쓸 수 있는 논리 (값 아님)
- Sand 시간은 t₊ → 1 극한에서 발산한다 — '무기 SSE 의 덴드라이트를 농도 고갈로 설명하지 않는다' 는 문장의 교과서 근거 (식 6 자체 · 리뷰 인용 불필요).
- 'MXene 이 공간전하를 균질화한다' 류 주장에는 계면 E_v · 공간전하 정량 원전 ([Haru14] · `comparison_vs_ours.md` §J-34 · §J-77) 으로 대응한다.

### 11-5. ⛔ 이 리뷰에서 가져오면 안 되는 것
- 수치 전부 (원 논문 확인 전) — 특히 'sulfides > 10⁻² S cm⁻¹' · `Table 2` 창 · `Fig. 7` 흡착에너지 · 'Li⁺ 장벽 0.2–0.4 eV' (3 차).
- `Table 3` 행을 'MXene 인터레이어로 Li/SSE 계면이 안정' 의 근거로 쓰기 (인용이 받치지 않음).
- `Fig. 10` · `Fig. 1` 을 발표 그림으로 재사용 (기하 오류 · 깨진 글리프).
- 'sulfide-based conductors' 비교 문장 (인용이 Li–S · Zn 논문).

## 12. 원전 대조표

### 12a. 리뷰가 인용한 문헌 중 우리 litdb 에 카드가 있는 것
**없다.** DOI 로 확인한 13 편 — [3] Monroe–Newman 2005 · [5] Wang 2021 *Joule* · [14] Narayanasamy 2023 · [16] Seino 2014 · [18] Zhou 2023 *Chem. Rev.* · [24] Xu 2023 · [96] Pan 2019 · [99] Huo 2025 · [100] Wang 2025 *Science* · [102] De Gol 2024 · [103] He 2025 · [107] Wang 2024 · [110] Ihrig 2024 — 전부 litdb digest 없음. Monroe–Newman 은 여러 카드에 이름만 나온다 (digest 없음).

### 12b. 다음에 열 만한 원전 (리뷰 목록 서지 그대로 · 우리 축 기준 우선순위)
1. **[107]** Y. Wang, P. Yuan, Z. Xu, et al., "Ti₃C₂T MXene In-Situ Transformed Li₂TiO₃ Interface Layer Enabling 4.5 V-LiCoO₂/Sulfide All-Solid-State Lithium Batteries With Superior Rate Capability and Cyclability," *Chin. Chem. Lett.* 35 (2024) 108776. DOI 10.1016/j.cclet.2023.108776 — 황화물 SE 조성 · 코팅 두께 · 전압 기준 확인 ([혁주] 비교 후보).
2. **[14]** M. Narayanasamy, S. Zaman, C. M. Koo, "2D MXenes for All-Solid-State Batteries: A Comprehensive Review," *Mater. Today Energy* 37 (2023) 101405 — 무기 SSE + MXene 1차 연구 목록을 여기서 찾는다.
3. **[47]** Q. Man, Y. An, H. Shen, et al., "MXenes and Their Derivatives for Advanced Solid-State Energy Storage Devices," *Adv. Funct. Mater.* 33 (2023) 2303668.
4. **[103]** X. He, Y. Xiang, W. Yao, et al., "MXene Surface Engineering Enabling High-Performance Solid-State Lithium Metal Batteries," *Adv. Funct. Mater.* 35 (2025) 2416040 — `Fig. 7` DFT 조건 · 흡착 기준 상태 확인.
5. **[145]** S. Huang, V. N. Mochalin, "Hydrolysis of 2D Transition-Metal Carbides (MXenes) in Colloidal Solutions," *Inorg. Chem.* 58 (2019) 1958 — '물이 매개' 원전 (§11-3).
6. **[132]** T. Zhang, L. Chang, X. Zhang, et al., "Simultaneously Tuning Interlayer Spacing and Termination of MXenes by Lewis-Basic Halides," *Nat. Commun.* 13 (2022) 6731 — 할라이드 말단 경로.
7. **[92]** B. Anasori, C. Shi, E. J. Moon, et al., "Control of Electronic Properties of 2D Carbides (MXenes) by Manipulating Their Transition Metal Layers," *Nanoscale Horiz.* 1 (2016) 227 — 금속성 ↔ 반도체성 (전자 차단 MXene 의 가능성).

## 13. 적용 인사이트 (가장 날카로운 셋)
1. **'금속성 인터레이어' 와 '전자 차단 코팅' 을 이름으로 가른다** — 이 리뷰의 혼란 (같은 MXene 이 전자를 통하면서 '전자적으로 부동태화' 한다) 이 바로 축을 안 부르면 생기는 일이다. 황화물 계면에서 전자전도 층은 SE 를 보호하지 않고 반응 면을 옮긴다 · 판정 변수는 석출 위치와 그 면의 접착이다 ([liao2025]).
2. **이 리뷰의 유일한 황화물 성공 사례는 MXene 이 사라진 경우다** — Ti₃C₂Tₓ → Li₂TiO₃ ([107]). [혁주] LZO (Li₂ZrO₃) 와 같은 Li₂MO₃ 절연 코팅 계열이고, [Kim26HTS] 계산값으로는 LPSCl 과의 반응에너지가 0 이 아니며 산화 한계가 4.5 V 작동보다 낮다 — '안정' 은 동역학 보호로 읽는다. 원전 [107] 을 열면 [혁주] 비교 후보 하나가 생긴다.
3. **친수성은 황화물에서 이점이 아니다** — MXene 을 황화물에 붙이려면 무 O/H 말단 (Cl 말단 용융염 MXene) · 건조 공정이 출발점이다. 그 밖의 소득은 보고 규율의 반면교사 (흡착 'E_a' 표기 · 색 막대 없는 ELF · ≳ 2 eV 배위 미확인 · 장벽 차 ↔ 선택도 홉 수 모순) 정도다. **우리 일에 직접 쓸 수치는 없다.**

## 14. 인용 가능 문장 (영문 초안 — 이 리뷰가 아니라 원전을 인용하는 꼴 · 원전 확인 뒤에만)
- "An electronically conducting interlayer placed between a sulfide solid electrolyte and an electrode does not block electrons; it holds the electrolyte surface at the electrode potential and relocates, rather than suppresses, the reactive interface." (논리 문장 · 인용 불필요 — 근거는 창 원전 [Zhu15] · [Schw21])
- "MXene has also been used as a precursor of an electronically insulating Li₂TiO₃ coating on LiCoO₂ in sulfide all-solid-state cells, where the protective phase is the converted oxide rather than the pristine MXene [107 원전]."
- "For single-ion conductors (t₊ → 1), Sand's time diverges, so concentration depletion does not set the onset of lithium penetration in inorganic solid electrolytes." (식 자체 · 인용 불필요)

## 15. 주의 / 한계 (인용 규율)
- 이 리뷰를 수치 출처로 쓰지 않는다 — 모든 값은 2 차 (일부 3 차) 이고 인용 대응이 자주 어긋난다.
- 이 카드의 인용 어긋남 판정은 **제목 수준**이다 — 원 논문 본문은 확인하지 않았다.
- `figure-read ≈` 값 (`Fig. 13` · `Fig. 15`) 은 래스터 그림 눈대중이다 — ±한 눈금.
- [Kim26HTS] 의 Li₂TiO₃ 값은 그 논문의 규약 (MP-PBE · 그들의 혼합 반응에너지 정의) 이다 — 우리 계산값과 같은 표 금지.
- 우리 쪽 값은 이 카드에 싣지 않았다 — 필요하면 `canonical_registry.json` → `citation_hazards.json` 순으로.

## 16. 기법 · 용어 미니사전
- **MAX 상**: Mₙ₊₁AXₙ 층상 세라믹 (예 Ti₃AlC₂). M–X 층 사이에 A (Al · Ga) 원자층이 끼어 있다.
- **MXene**: MAX 에서 A 층만 산 (HF · LiF/HCl) 이나 용융염으로 녹여 낸 2D 판. 화학식 Mₙ₊₁XₙTₓ. 대표 Ti₃C₂Tₓ 는 금속처럼 전자를 잘 통한다.
- **표면 말단 Tₓ**: 식각 중 판 표면에 붙는 원자단 (−O · −OH · −F · 용융염이면 −Cl · −Br). 실제 표면은 이들이 섞인 무질서 배열이고, 말단이 친수성 · 흡착 · 일함수 · 산화 안정을 바꾼다.
- **층간 간격 (d-spacing)**: 쌓인 판 사이 거리 — XRD (002) 봉우리로 잰다. 물 · 양이온 · 분자를 끼우면 (삽입 · 필러링) 넓어진다. 리뷰 값 ≈0.5–1.5 nm.
- **박리 (delamination)**: 다층 MXene 을 단층 · 소수층 판으로 떼어 내는 것.
- **친리튬성 (lithiophilicity)**: 표면이 Li 를 잘 적시고 Li 핵생성을 쉽게 한다는 뜻의 정성 표현 — 보통 흡착에너지나 접촉각으로 말한다.
- **전자 퍼콜레이션 문턱**: 전도성 충전재가 서로 이어져 전해질을 관통하는 전자 경로가 생기는 최소 함량. 그 위에서는 전해질이 전자를 통해 누설 · 자가방전 · 단락.
- **이온 수송수 t_ion (t₊)**: 전체 전류 중 (양) 이온이 나르는 몫. 고체 전해질은 1 에 가까워야 한다.
- **ELF (전자국재함수)**: 0–1 사이 값으로 전자가 얼마나 '쌍으로 국재' 돼 있는지 보이는 함수 — 공유결합 · 고립쌍은 1 근처, 금속적 전자는 0.5 근처. 그림에는 **색 막대 · 단면 위치**가 있어야 읽힌다.
- **흡착에너지 E_ads (리뷰 그림은 'E_a')**: E(슬랩+흡착종) − E(슬랩) − E(흡착종). 음수가 클수록 세게 붙는다. **활성화에너지 Ea 와 다른 양**이다. 전하 종 (Li⁺ · TFSI⁻) 은 기준 상태를 어떻게 잡았는지가 값을 바꾼다.
- **Sand 시간**: 일정 전류에서 전극 표면의 염 농도가 0 이 되는 시간. t₊ → 1 이면 발산 — 단일 이온 전도체에는 해당 없음.
- **공간전하층**: 이종 계면에서 전하 운반자 (반도체는 전자 · 정공 · SSE 는 Li 공공 · 침입) 가 쏠려 생긴 전위 강하 층.
- **VTF 식**: 고분자 전해질 σ(T) = σ₀·exp[−B/(T−T₀)] — 사슬 구획 운동에 묶인 수송의 비아레니우스형.
- **GITT**: 짧은 전류 펄스 + 긴 이완을 반복해 확산계수를 내는 전기화학 측정.
- **전환 코팅 (conversion coating)**: 전구체 층 (여기서는 MXene) 을 열처리 · 반응으로 다른 상 (Li₂TiO₃) 으로 바꿔 만든 보호층.
