<!-- digest 초판 2026-10-27 (논문 에이전트 · 병렬 9 편 중 1 편 · 사용자 목록 #14).
     ① PDF 45 pp 텍스트 전문 정독 (본문 ≈ 38.5 pp + 참고문헌 192) · SI 없음 · 우리 그룹 아님 · talk 인입 대기열 미등재 (확인).
     ② 크롭 18장 (그림 17 + 표 1). 도구가 Fig. 2 를 놓쳤다 (p.5 캡션 블록 'FIGURE 2 \nFrom …' 앵커 실패 → '번호 공백' 절에 뜸)
        → 손 크롭 1장 (figures.json `manual_crop` 사유 + `missing_labels[f2].resolved`).
     ③ 그림 17장 **전부** 실독 + 확대 재크롭 7회 (`Fig. 3c2` · `3g1` · `7a1` · `7a2` · `10d` · `14a1` · `14e` — scratchpad 에만, repo 에 안 넣음).
        `Table 1` 은 이미지 대신 PDF 텍스트 + 단어 좌표로 판독 (각주 (b) 귀속 · 미보고 칸 수를 좌표로 셈).
     ④ 이 편은 **리뷰**다 — 자체 계산 0 · 자체 실험 0. DFT 수치 전량 2차 소환이고 범함수·vdW·U·k·스핀 같은 계산 조건은 원전 어디서도 옮겨 오지 않았다.
     ⑤ 1순위 목적 = 우리 트랙과의 거리 판정 (§0). 결론: 황화물 SE 물성 4축과 직접 관련 없음 ·
        흡착·장벽·상태 정의 규율의 사례 + Li₂S 벌크 물리 (§2) 방향잡기만 가져온다. -->

# Tailoring Lithium–Sulfur Battery Separators via Crystal Engineering: From Fundamental Modulation to Multidimensional Synergy — Luo et al. (*Small* 2026, e76191)

> slug `luo2026_lis_separator_crystal_engineering_review` · DOI `10.1002/smll.76191` · type `review (자체 계산 0 · 자체 실험 0 · 액체 전해질 Li–S 분리막 코팅 문헌 정리)` · PDF `c54c1ba8-14._Tailoring_Lithium_Sulfur_Battery_Separators_via_Crystal_Engineering_From_Fundamental_Modulation_to_Multidimensional_Synergy.pdf` (업로드 원본 · litdb/inbox 미복사 · 45 pp · sha256 `f04c1397d49fe21a…`) · **SI 없음** · digested `2026-10-27` · status ✅ · 태그 **[외부]**

> elements: Li, S, C, N, O, Ti, Mo, Co, Fe, Ni, Zn, Ce, V, Se, P
> methods: DFT, phonon, elastic, DOS, PDOS, XPS, Raman

> **저자**: **Yun Luo** (1저자) · Fan Zhang · **Nanping Deng\*** · **Jingge Ju\*** · Yuzhu Li · Penghui Su · Ying Wang · Qichen Shi · **Weimin Kang\*** — 전원 **Tiangong University** (天津工业大学) School of Textile Science and Engineering · MoE Key Lab for Advanced Textile Composite Materials (Tianjin) · 교신 3 인 · 투고 2026-07-10 → 수정 2026-09-14 → 수락 2026-10-02 · © Wiley-VCH (OA 아님 · Hanyang Univ. Library 경유 2026-10-25 다운로드) · 자금 NSFC 52573089 · 52403046 · 61904123 외 · Data availability *"no datasets were generated or analysed"* · 이해상충 없음.
> 저자 기여 표기: 5 인 *"writing – review and editing"* · 4 인 *"supervision"* — *conceptualization* · *writing – original draft* 항목이 **아무에게도 없다** (서지 관찰일 뿐 · 판단 근거로 쓰지 않음).
>
> **구성**: 본문 §1–§6 · **그림 17** (자체 작성 3 = `Fig. 2` · `Fig. 4` · `Fig. 17` · 나머지 14 는 원전 재사용) · **표 1** · refs **192** (정규식 자동 집계로 연도가 잡힌 179 편 중 2022–2026 ≈ 156 편 · 2026 년 ≈ 24 편 — 근사 ±수 편).

---

## 0. 이 digest 를 읽는 법 — 우리 트랙과의 거리 판정 (먼저)

**판정: 황화물 SE 물성 4축 (이온 · 산화 · 기계 · 전자) 과 직접 관련 없음 · 방법(보고 규약) 교훈 + Li₂S 벌크 물리 방향잡기만.**
무대는 **액체 전해질 (에테르계) Li–S 전지의 PP·Celgard 분리막 위 기능성 코팅** — 폴리설파이드(LiPS) 셔틀을 막고 전환을 촉매한다. 우리 argyrodite 와 겹치는 물성값은 **0 건**이다.

`rg` 로 우리 쪽 연결점을 직접 훑은 결과 (2026-10-27 · `litdb/papers` · `db/properties/*.json` · `kb/*.md` · `db/governance/decisions.json`):

| 후보 | 실제로 본 것 | 판정 |
|---|---|---|
| **li2s 트랙** (Li₂S 계면상 · 외부 1저자) | §2 의 Li₂S 밴드갭 3.398 eV · S Born 유효전하 1.91 · ε₀ 7.80 · LO–TO 132 cm⁻¹ · B₀(T) — 전부 **벌크 결정 Li₂S 2차 인용** · 우리 db 에 Li₂S gap·탄성·유전 값은 없다 (`canonical_registry.json` 에 Li₂S 항목 0 · `db/properties` 의 li2s 파일은 전부 계면·수송 카드) | 🟡 **문헌 방향잡기만** — 수치 이식 0. ⚠ 같은 `Fig. 3` 안에서 c-Li₂S LO–TO 가 80 vs 132 cm⁻¹ 로 어긋난다 (§10-⑥) |
| **흡착에너지 배위수 규율** (`D-2026-10-05-adsorption-site-coordination` · active) | `Fig. 12f` TiO(001) 위 S₈ **−18.45 eV** · Li₂S₈ −14.33 eV … 구조 비공개 · 리뷰는 '가장 강한 화학흡착' 으로만 읽음 | ⭕ **규율 적용의 교과서 반례** — "배위 미확인 · 결합 포화(아마 분해) 에너지" (§3d · §10-②) |
| **장벽 홉 수 검산** (`D-2026-09-27-barrier-hop-count` · active) | ICOF(100) Li⁺ 이동 장벽 **0.715 kcal mol⁻¹ (= 0.031 eV)** · Li₂S 해리 0.48 eV 와 대조군 0.78–1.55 eV (`Fig. 10d`) | ⭕ 검산 결과 **차수 모순** — 0.031 eV 는 1.2 kT, 1.55 eV 는 상온 1 h 창에서 사실상 안 넘는다 (§3d) |
| **보고량 카드 규율** (상태 선택 규칙 · CLAUDE.md §계산 규율) | §4.3–4.4 *"the working-state catalyst may be entirely different from the initial-state catalyst"* (Fe₂O₃ → Li₃Fe₂S₄) · CoB 의 Co 스핀 상태 서술 | ⭕ **같은 원리의 외부 목소리** — 단 리뷰 자신은 스핀 규약 0 줄 |
| SE 기초 (`famprikis2019_fundamentals_inorganic_sse.md`) | `Fig. 5g` = Famprikis 2019 *Nat. Mater.* 의 양이온 이동 3 기구 그림을 '양이온 공공 (촉매 코팅)' 절에 재사용 | 🟡 맥락 이탈 (SE 이동 기구 ≠ 촉매 코팅의 공공 안정성) |
| ASSB 복합양극 (ref [123] Cui *Nat. Energy* 2024) | `Fig. 9c` = 이종 vs 균질 복합양극의 탈리튬 미세구조 (균열 · 박리 · 고저항상) | 🟡 원전이 우리 DEM·ASSB 축에 닿는다 — **litdb 미보유** (`rg "homogenization"` → fan2026 · miao2023 에 언급만) · 본문은 이 그림을 황 팽창 설명에 잘못 붙였다 (§10 표) |
| p-band center (`liu2024_pband_center_sbo_dual_interface.md`) | `Fig. 6g` PSN 의 **O** p-band center −4.627 → −3.475 eV (vs E_F) | 🟡 이름만 같은 서술자 — 계·원소·기준 에너지 다름 → 수치 비교 금지 |
| 비교 가능성 (`canonical_registry.json` 의 `comparison_group`) | `Table 1` 각주: R_ct·σ·LiPS 차단이 셀 구성마다 다른 방법이라 *"not directly comparable across rows"* | ⭕ 우리 규율의 분야판 |
| 🎤 talk 인입 대기열 (`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 1개) | 대기열 표에 이 편 없음 (걸린 'Luo' 는 Luo 2022 cryo-TEM 다른 논문) | ✗ 역링크 해당 없음 |

⇒ `comparison_vs_ours.md` 에는 **물성 4축 행을 만들지 않는다** — 넣는다면 🔧 방법 원전 블록 한 줄 (흡착 배위수 · 홉 수 검산 · 상태 정의 규율의 외부 사례).

> **실제로 본 그림 (2026-10-27)**: `Fig. 1`–`Fig. 17` **17장 전부** + 확대 재크롭 7회 (`Fig. 3c2` · `Fig. 3g1` · `Fig. 7a1` · `Fig. 7a2` · `Fig. 10d` · `Fig. 14a1` · `Fig. 14e`).
> 안 본 것: `Table 1` 이미지 — PDF 텍스트 + 단어 좌표로 판독했다 (표는 텍스트가 더 정확).
> 그림에서 눈금으로 읽은 값은 **`figure-read ≈`**, 그림 속 **인쇄 라벨**을 옮긴 값은 **`figure-read (인쇄값)`** 으로 구분한다.
> **본문 서술과 그림이 어긋난 곳 ≥ 15 군데** — §10b 표에 모았다.

---

## 1. 한 줄 요약

Tiangong 대학 섬유학과 (전기방사 분리막 그룹) 의 **Li–S 분리막 코팅 리뷰** — '결정공학' 6 전략 (결함 · 도핑 · 상/변형 · 결정면 · 엔트로피 · 동적 재구성) 을 분리막의 세 기능 (**Li⁺ 수송 · LiPS 차단 · 화학/기계 안정**) 에 대응시키고 (`Fig. 4`) 사례 ≈ 55 건의 셀 성능 숫자를 모은다. 리뷰의 진짜 기여는 후반 **§4.4–4.5 와 `Table 1`** 이다: *코팅의 초기 구조는 작동 구조가 아니고, 전해질은 첫 사이클 안에 LiPS 용액으로 바뀌므로, 끝점 용량 유지율은 분리막 성능 지표가 못 된다* — 실제로 24 행 중 **t_Li⁺ 16 · σ 17 행이 미보고**다.

⚠ 단 앞쪽 §2–§3 은 원전 DFT 수치를 **계산 조건 없이** 옮기고 (범함수 0 줄), **그림 참조·캡션 오류가 ≥ 15 군데**이며, S₈ 흡착에너지 **−18.45 eV** 같은 값을 아무 단서 없이 '강한 화학흡착' 으로 읽는다 — 리뷰 자신이 §4.5 에서 '너무 강한 결합 = 피독' 이라고 쓰면서.

---

## 2. 메타 / 구성 / 던지는 질문

| 항목 | 내용 |
|---|---|
| 저널 | *Small* (Wiley-VCH) 2026, 0:e76191 · **REVIEW** · DOI `10.1002/smll.76191` · PDF 생성 2026-10-19 |
| 범위 | **액체 전해질** Li–S 의 분리막 쪽 — PP·Celgard 위 코팅 · 자립 인터레이어 · 탄소천 자체 분리막 (고체 전해질 Li–S 는 다루지 않는다) |
| 'crystal engineering' 의 뜻 | *"a powerful paradigm for tailoring the physicochemical properties of materials through the precise manipulation of atomic arrangements"* (§1) — 분자결정의 고전적 '결정공학' (분자간 상호작용 설계) 이 아니라 사실상 **'격자 공학'** (결함·도핑·변형·결정면) |
| 던지는 질문 | 원자·결정 수준 섭동 (*"anion vacancy-induced local charge redistribution and lattice strain-mediated d-band center modulation"*) 이 LiPS 흡착 · 촉매 전환 · Li⁺ 수송이라는 거시 지표를 어떻게 지배하나 |
| 리뷰가 내세우는 '처음' | *"the first systematic account of crystal engineering strategies specifically applied to lithium–sulfur battery separators"* (§1) |
| 분리막의 세 기능 목표 (§3 머리) | (i) *undisturbed Li⁺ transport* (ii) *effective blocking of polysulfide shuttling through chemisorption and catalytic conversion* (iii) *chemical and mechanical stability of the separator–electrolyte interface* |
| 다섯 설계 원리 (§6) | ① function before structure ② **balance, not maximum** ③ **initial state ≠ working state** ④ **separator-specific descriptors** (끝점 용량 아님) ⑤ **minimal inactive mass** (코팅 질량당 활성) |
| 세 난제 (§6) | ① vacancy stability ② compatibility (기계강도·기공·두께 손실) ③ standardized evaluation |
| 네 전망 (§6) | ① AI-assisted design (전매개체 *pre-mediator* 식 자가응답 분리막) ② structure matching (채널 크기 ↔ Li⁺ 탈용매화 껍질 · 구배 비대칭 분리막) ③ minimalist design (sp-N 도핑 · 무게 0 에 가까운 첨가로 > 450 Wh kg⁻¹) ④ advanced in situ characterization |

### 2a. 절 구조 (section tree) — 그림 대응

| 절 | 내용 | 그림·표 |
|---|---|---|
| §1 Introduction | LIB 한계 → Li–S (2600 Wh kg⁻¹) · 세 문제 (셔틀 · 덴드라이트 · ~80 % 부피팽창) · 분리막 개질의 위치 · 결정학 역사 (Laue 1912 → Bragg 1913 → Debye 1912 → Taylor 전위 1934 → 초격자 1970s) | `Fig. 1` · `Fig. 2` |
| §2 Mechanistic Insights | 2.1 격자 진동 (포논 공학 · Li₂S/Li₂S₂ 밴드·포논·광학 · 폴라론) · 2.2 탄성·격자 안정 (2.2.1 Li₂S 고압 포논·B₀(T) · 2.2.2 계면 안정 (그래핀/SnO) + 벌크 안정 (고체 LiPS 탄성)) | `Fig. 3` |
| §3 Strategies | 3.1 결함 (3.1.1 음이온 공공 · 3.1.2 양이온 공공) · 3.2 도핑 (3.2.1 음이온 · 3.2.2 양이온 · 3.2.3 배위 조절) · 3.3 상/변형 (3.3.1 외부 유도 상전이 · 3.3.2 격자 변형 · 3.3.3 이종접합) · 3.4 결정면 (3.4.1 고지수면 · 3.4.2 형상·배향 성장) | `Fig. 4`–`Fig. 12` |
| §4 Multidimensional Synergy | 4.1 다차원 설계 · 4.2 엔트로피 · 4.3 동적 결정공학 · **4.4 장기 구조 진화** · **4.5 진화하는 전해질** (+ `Table 1`) | `Fig. 13`–`Fig. 15` · `Table 1` |
| §5 Characterization | 5.1 격자 구조 특성분석 (XRD · STEM · HAADF · XAFS · XPS · Raman · EPR · FTIR · SAED · SEM/TEM) · 5.2 계산법 (DFT-D3 · PBE · HSE06 · AIMD — 한 쪽 분량 일반론) | `Fig. 16` |
| §6 Conclusion | 다섯 설계 원리 · 세 난제 · 네 전망 | `Fig. 17` |

---

## 3. 핵심 수치 총정리 ★

> **전부 리뷰 재인용 (원전 확인 전)**. 셀 조건 (C-rate · S 적재량 · E/S) 이 행마다 다르므로 **행 사이 비교 금지** — 리뷰 자신이 `Table 1` 각주에서 같은 말을 한다.
> `figure-read ≈` = 그림 눈금 판독 · `figure-read (인쇄값)` = 그림 속 인쇄 라벨.

### 3a. Li₂S · Li₂S₂ 벌크 물리 (§2 · `Fig. 3`) — li2s 트랙 방향잡기용

| 물성 | 값 | 출처 · 조건 | 비고 |
|---|---|---|---|
| c-Li₂S 밴드갭 | **3.398 eV** (간접 · VBM Γ → CBM X, `Fig. 3a` 화살표) | [54] Jiang *PCCP* 25, 6362 (2023) · **범함수 n/a** | 같은 3.398 이 [57] 에도 (`Fig. 3d` 인쇄 3.40) |
| o-Li₂S 밴드갭 | 4.061 eV | [57] Peng *Solid State Sci.* (2025) | `Fig. 3d` DFT·DFT-D 모두 4.06 (인쇄값) |
| h-Li₂S₂ | 1.010 eV | [57] | `Fig. 3d` 1.00 (DFT) / 1.01 (DFT-D) (인쇄값) |
| t-Li₂S₂ | 1.814 eV | [57] | `Fig. 3d` 1.77 (DFT) / 1.81 (DFT-D) (인쇄값) |
| VBM 정공 유효질량 | m_v* = −0.77 | `Fig. 3a` figure-read (인쇄값) · 본문 언급 없음 | 단위 표기 없음 |
| S Born 유효전하 | ≈ 1.91 \|e\| | [54] | 공칭 2 와 4.5 % 차 — 리뷰는 *"notably deviating"* 이라 씀 (§10-⑤) |
| 정적 유전상수 ε₀ | 7.80 | [54] | *"primarily attributed to ionic polarization"* |
| Raman (계산) | 한 줄 ≈ 373 cm⁻¹ · 라벨 "Li⁺ s-str." | `Fig. 3c1` figure-read ≈ (이 작업 vs Xue et al. 겹침) | 반형석 T2g — Li 만 움직이는 모드 |
| IR (계산) | 한 줄 ≈ 320 cm⁻¹ · 라벨 "Li⁺ a-str." | `Fig. 3c2` figure-read ≈ (확대 재크롭) | T1u TO |
| LO / TO @ Γ (Peng) | c-Li₂S **452 / 372** · o-Li₂S 483 / 455 · h-Li₂S₂ 402 / 310 · t-Li₂S₂ 400 / 342 cm⁻¹ | `Fig. 3f` figure-read (인쇄값) | c-Li₂S 분리 = **80 cm⁻¹** |
| LO–TO 분리 (Saib) | **132 cm⁻¹** (0 GPa) → 107 cm⁻¹ (10 GPa) | [63] Saib & Bouarissa *Mater. Res. Express* 4, 105901 (2017) | `Fig. 3g1` Γ 의 광학 가지 ≈ 325 · ≈ 377 · ≈ 456 cm⁻¹ (figure-read ≈) → 456 − 325 ≈ **131** ✓ |
| 포논 최고 진동수 | 500 (0 GPa) · 566 cm⁻¹ (10 GPa) | [63] | 허수 없음 → 10 GPa 까지 동역학 안정 |
| 격자상수 a(T) | ≈ 5.688 Å (0 K) → ≈ 5.737 Å (1000 K) | `Fig. 3h1` figure-read ≈ | 0–100 K 거의 평평 |
| 체적탄성률 B₀(T) | ≈ 40.2 GPa (0 K) → ≈ 32 GPa (1000 K) | `Fig. 3h2` figure-read ≈ | 비조화 연화 |
| 고체 LiPS 상대 에너지 | α-S₈ + Li₂S 대비 *"tens of meV/atom"* 위 (준안정) · vdW 가 안정화 | [69] Guo — **Michigan Tech 박사논문 (2021)** | 동시에 그래핀/SnO 이종접합 · 계산 XANES 의 출처 |
| 광흡수 최대 | h-Li₂S₂ 8.4 eV · t-Li₂S₂ 7.9 eV | [57] | `Fig. 3e` 세 상 모두 흡수 개시 ≈ 4.5 eV (figure-read ≈) |
| 그래핀/SnO 이종접합 | gap 이 외부장 0.3×10¹⁰ V m⁻¹ (= 0.3 V Å⁻¹) 까지 유지 · SnO 한 층 제거 → p 형 Schottky | [69] | 장 방향에 따라 p→n 전환 / Ohmic |

### 3b. 사례 수치 — 절별 (셀 성능 · 리뷰 재인용)

> '위치' 열은 **리뷰 본문이 말한 대로** 적었다 — *(리뷰 표시)* = 리뷰가 스스로 '분리막 사례 아님' 을 밝힌 것, *(표시 없음)* = 분리막 사례가 아닌데 표시가 없는 것.

| 절 | 재료 — 위치 | 전략 | 핵심 수치 | ref |
|---|---|---|---|---|
| §1 | V₂C MXene 구 (VC) — 분리막 | 구 크기 조절 → 활성 자리 | 1206.4 mAh g⁻¹ @0.1 C (초기) · 600 사이클 @1 C **0.04 %/cycle** | [37] |
| §1 | PEG-VN@PP — 분리막 코팅 | PEG (Li⁺ 선택) + VN (흡착·촉매) | 700 사이클 후 782.0 mAh g⁻¹ @1 C · 평균 0.048 %/cycle | [38] |
| §1 | 상용 PP | — | 과전압 > 250 mV → 에너지밀도 ≥ 20 % 하락 | [32, 33] |
| §2.1 | Ni₂P (P 공공 → small polaron) — 위치 미상 | 공공 + 폴라론 | d-band center → E_F 쪽 · Li₂S₂→Li₂S 장벽 ↓ · 901.2 mAh g⁻¹ @1 C · 1000 사이클 0.06 %/cycle | [60] |
| §3.1.1 | Sb₂Se₃₋ₓ/RGO — 분리막 코팅 | V_Se (화학환원 + 열충격) | EPR g = 2.00 · **8.0 C** 율속 · 0.027 %/cycle @1 C · **7.46 mAh cm⁻² @ S 8.1 mg cm⁻²** | [78] |
| §3.1.1 | CeO₂/CNT (Ar/H₂ 환원) — 분리막 코팅 | V_O (Lewis 산 자리) | CeO₂(111) d = 0.32 nm (`Fig. 5c1` 인쇄값) · **셀 수치 없음** | [79] |
| §3.1.1 | TiO₂₋ₓ@NMC — 분리막 코팅 | V_O (탄소열 처리) | 젖음 ↑ · 자가방전 ↓ · 인장강도 `figure-read ≈` 250 vs 128 MPa (`Fig. 5d`, 변형 ≈ 42 % 파단) | [80] |
| §3.1.1 | SC-Co (원자 Co @ 초분자 유래 메조탄소) — 분리막 | 원자 Co | 300 사이클 후 837 mAh g⁻¹ · 0.086 %/cycle | [81] |
| §3.1.2 | Fe₀.₉₆S@C — **양극** *(리뷰 표시)* | Fe 공공 = 'S 저장고' | 5.0 C · S 3.5 mg cm⁻² · 400 사이클 @1 C 93 % 유지 | [85] |
| §3.1.2 | STMnₓ (SrTiO₃ B-자리 Mn, x = 0.1–0.3) — 분리막 코팅 | 원자가 차 → V_O ↑ | 정성만 (V_O ↑ → LiPS 결합 ↑ · 분해 장벽 ↓) | [72] |
| §3.1.2 | VCFN (V₂O₅/Cys/FeNi-LDH) — 분리막 코팅 | 혼합 원자가 (V⁵⁺·Fe²⁺·Fe³⁺·Ni²⁺) | 1035.2 → 920.1 mAh g⁻¹ (300 사이클 @0.5 C) · 0.039 %/cycle · D_Li⁺ ≈ 10⁻¹⁰ cm² s⁻¹ | [86] |
| §3.1.2 | Co₀.₅Ni₀.₅Te₂@CS (NiCo-LDH 의 Te 교환) — 분리막 개질제 | 음이온 교환 | 전자전도 1.15×10⁶ S m⁻¹ · 699.5 mAh g⁻¹ @7 C · 500 사이클 후 784.8 @2 C | [87] |
| §3.2.1 | SVO/AB (N-도핑 VO₂ + 아세틸렌블랙) — 분리막 코팅 | N 도핑 · '보조 집전체' | 본문 수치 없음 · `Table 1` R_ct 16.93 Ω | [95] |
| §3.2.1 | T-NSCC (N,S 공도핑 중공 탄소천) — **천 자체가 분리막** | 음이온 공도핑 | 피리딘 N 74.9 % · 피롤 N 23.6 % · XPS Li–N 56.4 / Li–S 55.3 eV (`Fig. 6b` 인쇄값) · 1028.7 → 794.5 mAh g⁻¹ (200 사이클 @0.2 C) · 1000 사이클 @2.0 C 0.02 %/cycle | [96] |
| §3.2.1 | FSI⁻ + TTE (약용매화) 전해질 — **분리막 아님** *(리뷰 표시)* | 경쟁 배위 | Ah 급 파우치 622 Wh kg⁻¹ @0.35 C | [97] |
| §3.2.2 | Fe-ZIF-8/PP — 분리막 코팅 | Fe 도핑 MOF 체거름 | 1000 사이클 · 초기 863 @0.5 C · 746 mAh g⁻¹ @3 C · `Table 1` H-cell *"negligible, 24 h"* (`Fig. 6d` 는 12 h 까지만) | [101] |
| §3.2.2 | Ni-ZIF-8-C — 분리막 코팅 | Ni/Zn 이원 | 972.4 mAh g⁻¹ @2 C · S 2.0 mg cm⁻² · 1000 사이클 0.05 %/cycle | [102] |
| §3.2.2 | PSN/MXene 2D 나노채널 — 인터레이어 | 표면전하 선택 + O p-band | zeta −25.0 (MXene) / −10.9 mV (PSN/MXene) (`Fig. 6f` 인쇄값) · O p-band center −4.627 → −3.475 eV (`Fig. 6g` 인쇄값) · 1443 @0.1 C · 592 mAh g⁻¹ @4 C · 800 사이클 @2 C 0.049 %/cycle | [103] |
| §3.2.3 | W/NG SAC (W–N₂O₂–C) — 분리막 개질제 | 비대칭 배위 | 200 사이클 후 986 mAh g⁻¹ @0.5 C | [104] |
| §3.2.3 | Co–N₃Cl₁ SAC ('REV' 개념) — 양극 쪽 분리막 코팅 | Cl 치환 비대칭 배위 | **804.3 mAh g⁻¹ @5.0 C** · 0.023 %/cycle | [105] |
| §3.2.3 | M SA/N-Ti₃C₂Tₓ (M = Cu, Co, Ni, Mn, Zn, In, Sn, Pb, Bi) — 분리막 | 공공 구속 N 고정 | 본문 수치 없음 · `Table 1` Cu 행 **전부 '—'** | [106] |
| §3.2.3 | Fe–NSC@GO (주변 S 도핑 Fe–N₄) — 분리막 | 이웃 음이온 도핑 | 300 사이클 @3.0 C 70.8 % 유지 (`Fig. 7e` figure-read ≈ 735 → 520 mAh g⁻¹ ⇒ ≈ 71 % ✓ · S 2 mg cm⁻²) | [108] |
| §3.2.3 | KPW-CR6/GO/PP (POM + 크라운에테르) — 분리막 | 초분자 배위 | 250 사이클 후 874.7 mAh g⁻¹ @1 C · 81.5 % 유지 · CCDC 2366133 | [109] |
| §3.2.3 | Se₀.₀₆SPAN/MMT@PP — 분리막 코팅 | 층상 점토 + Se-SPAN | 1000 사이클 @1 C 0.034 %/cycle · 재사용 가능 | [110] |
| §3.3.1 | MWCE 1T-MoS₂ — **양극 host** *(표시 없음)* | 2H → 1T (Li 삽입) | 전도도 ×10⁷ · 상전이 72 h → 30 s · 1T ≈ 100 % · > 1200 mAh g⁻¹ @ E/S 2.1 µL mg⁻¹ | [112] **박사논문** |
| §3.3.1 | TiN/1T-MoS₂ 중공구 — 위치 미상 | 전기화학 삽입 상전이 | 1273 @0.1 C · 689 mAh g⁻¹ @2 C · 800 사이클 @1 C 0.051 %/cycle | [117] |
| §3.3.1 | F-Co@NC vs H-Co@NC — 위치 미상 | Co 결정상 (FCC/HCP) | E_F − E_VBM **1.13 vs 2.38 eV** (`Fig. 8b` 인쇄값) · 셀 수치 없음 | [118] |
| §3.3.1 | P-CoSe₂/MXene — 분리막 (개질 PP) | P 도핑 → 상전이 + 인장 변형 | Co–Se 2.08 → 2.11 Å · 603 mAh g⁻¹ @4 C | [119] |
| §3.3.2 | La₂Ce₂O₇/rGO — 기능성 분리막 | La 도핑 '격자 변형' | d(111) 0.324 vs CeO₂ 0.318 nm (`Fig. 9b` 인쇄값 · 우리 산수 +1.9 %) · 1264.4 @0.2 C · 100 사이클 75.5 % · ≈ 0.09 %/cycle @1 C · 1094.9 mAh g⁻¹ @ S 4.59 mg cm⁻² | [120] |
| §3.3.2 | 황 팽창 완충 | 중간 침전물 | Li₂S₄·Li₂S₂·Li₂S 가 황 팽창의 ≈ **48.64 %** 완충 · 고전류는 팽창 완화 대신 용량 손실 | [121] |
| §3.3.2 | zero-strain 일반론 | 부피변화 < 1 % | > 20,000 사이클의 열쇠 | — |
| §3.3.2 | Zr-LAO (Zr 도핑 LiAl₅O₈ 나노막대) — **음극** *(표시 없음)* | zero-strain | 20,000 사이클 후 227.2 mAh g⁻¹ @5 A g⁻¹ | [122] |
| §3.3.2 | Cui 2024 ASSB 양극 균질화 — **양극** *(리뷰 표시)* | zero-strain 양극 냉간압축 | 충방전 부피변화 **1.2 %** | [123] |
| §3.3.2 | 인(phosphorene) 압축 변형 — 계산 | 변형 | 최적 **−7 %** (SRR · Li₂S 산화 양방향) | [124] |
| §3.3.2 | 이축 변형 MoS₂ 계 (MSS) — 촉매 (위치 미상) | 고차원 변형 | Mo d-band · S p-band ↑ · 623 mAh g⁻¹ @6.7 mA mg⁻¹ · 파우치 396 Wh kg⁻¹ | [125] |
| §3.3.3 | Ti₃C₂@TiO₂ (UV 40 min) — 분리막 | Schottky 이종접합 | 1283 → 691 mAh g⁻¹ (200 사이클 @1 C) | [130] |
| §3.3.3 | Co-MoS₂/Ti₃C₂Tₓ (S 공공) — 분리막 코팅 | 도핑 + 이종접합 | 750.43 mAh g⁻¹ @4 C · S 5.7 mg cm⁻² · E/S 6 µL mg⁻¹ 에서 957.3 @0.2 C · 80 사이클 93.5 % | [131] |
| §3.3.3 | MoS₂-Edge@NCO (= MoS₂@CF-NRGO, Mo–O–C) — 분리막 코팅 | 공유결합 이종계면 | ΔG(RDS) **0.19 eV** · Li₂S 해리 **0.48 eV** · 615 mAh g⁻¹ @5 C · 6.11 mAh cm⁻² · 5 일 휴지 자가방전 8.6 % | [39] |
| §3.3.3 | CoB/Co–CoP@HNC — 위치 미상 | BIEF + 스핀 + 쌍극자 | Co 중간 → 저스핀 (정성) · 수치 없음 | [132] |
| §3.4.1 | ZnTe(111)/ZnO(101) — 분리막 기능화 | 결정면 분극 BEF | BEF ≈ **0.38 V Å⁻¹** · 결정면 불일치 ≈ 5 % (`Fig. 11a` 인쇄값) · 1000 사이클 @1 C 0.047 %/cycle (`Fig. 11c` figure-read ≈ 1040 → 540 mAh g⁻¹ ⇒ ≈ 0.048 % ✓) | [134] |
| §3.4.1 | C-Fe₂O₃-G (오목 나노큐브 · 고지수면) — 위치 미상 ('이기능 촉매') | 고지수면 | 1521 mAh g⁻¹ @0.1 C · 1600 사이클 @2 C 0.025 %/cycle | [137] |
| §3.4.1 | H-Fe-Ce NPs (Fe₂O₃ (113)·(104) + CeO₂) — 분리막 (H-Fe-Ce/PP) | 고에너지 계면 | **0.016 %/cycle** (*"under identical conditions"*) · **7.53 mAh cm⁻² @ S 10.17 mg cm⁻²** | [138] |
| §3.4.2 | CF@ICOF (배향 (100)) — 셀룰로오스 복합 분리막 | 배향 자기조립 | 채널 2.6 nm · Li⁺ 이동 장벽 **0.715 kcal mol⁻¹** · Li⁺/Sₓ²⁻ 선택도 275.97 · σ 2.186 mS cm⁻¹ · **S 11.12 mg cm⁻² + E/S 3.5 µL mg⁻¹ 에서 800 사이클 92.73 %** (0.047 %/cycle) · 유연 파우치 440.98 Wh kg⁻¹ | [141] |
| §3.4.2 | ANF/β-FeOOH@PP — 분리막 코팅 | 아라미드 템플릿 축 배향 | δ = 1.3–5.9 % (`Fig. 12d`) · 1146 mAh g⁻¹ @0.1 C · 500 사이클 @1 C 0.048 %/cycle | [142] |
| §3.4.2 | TiO-NFs ((001) 우세 · PDA 보조 마그네슘열 환원 950 °C Ar) — 분리막 (TiO-NFs@PP) | 결정면 | 1492 mAh g⁻¹ @0.1 C · 1000 사이클 0.067 % · 흡착에너지 `Fig. 12f` (§3d) | [143] |
| §4.1 | δ-Bi₂O₃-Ov/Bi@CNFs (리그닌 전기방사) — 분리막 맥락 (명시 약함) | 결함 + 상 + 방사 구배 | 580 mAh g⁻¹ @1.0 C · 1000 사이클 0.039 %/cycle | [145] |
| §4.1 | Fe₃N/Fe-NC (ZIF-PDA · 별 모양) — 분리막 (@PP) | 형상 + 다상 + 전자구조 | 600 사이클 @2 C 0.0603 % · S 6.668 mg cm⁻² | [146] |
| §4.2 | MS-HEO (Mn·Mg·Ni·Cu·Zn 암염 · S_config ≥ 1.5 R) — Celgard 코팅 **0.23 mg cm⁻²** | 엔트로피 안정 | S 7 mg cm⁻² · CV ΔV ≈ 140 (vs MEO 260) mV · R_ct ≈ 90 / 95 / 116 Ω (HEO/MEO/LEO) · Tafel **13 vs 42 mV dec⁻¹** · 450 사이클 0.055 % · 코팅 < 0.3 mg cm⁻² (양극 첨가 ≥ 10 wt% 대비) | [155] |
| §4.2 | HEO850/S/KB — **양극** *(표시 없음)* | 고엔트로피 | CV 전압차 40 / 300 mV (vs S/KB 50 / 320) | [156] |
| §4.2 | SA-Fe/HEO@NC (Cu·Zn·Al·Ce·Zr) — 분리막 개질제 | SAC + HEO | t_Li⁺ **0.60** (vs HEO@NC 0.40 · MEO@NC 0.36) · 1035 mAh g⁻¹ (100 사이클 @0.2 C) · 1000 사이클 @1 C 0.048 % · 0 °C 751 (100 사이클 @0.1 C) · 588 @1 C | [158] |
| §4.2 | Pt₀.₂₅Cu₀.₂₅Fe₀.₁₅Co₀.₁₅Ni₀.₂ HEA@HC — **양극 촉매** *(표시 없음)* | 칵테일 효과 | FCC Cu₃Pt (JCPDS 65-3247) · 피크 43.4° / 50.6° + '불순' 43.94° / 51.2° (본문) | [159] |
| §4.2 | (Co₀.₂Mn₀.₂V₀.₂Fe₀.₂Zn₀.₂)₃O₄ — **음극** *(리뷰 표시 · 유비)* | 엔트로피 안정 스피넬 | M₃O₄ + 8Li⁺ → 4Li₂O + 3M · 투영면적 +41 % ≈ 부피 +68 % · 균열 없음 | [160] |
| §4.3 | TiNb₂O₇ (TNO) 'Li⁺ 호흡' — `Table 1` 'Liₓ TNO reservoir' | 동적 캐스케이드 촉매 | 100 사이클 유지 73.9 % (60 °C) · 83.4 % (−20 °C) · 파우치 94.6 % @0.3 C · t_Li⁺ 0.79 | [161] |
| §4.3 | Fe₂O₃ → Li₃Fe₂S₄ → Fe₂O₃ (Fe₂O₃/NCS) — 위치 미상 | 전기화학 재구성 | 1387.1 → 684.4 mAh g⁻¹ (500 사이클 @0.5 C) | [162] |
| §4.3 | PW@g-C₃N₄/rGO — 분리막 | 격자 정합 + 일시적 N–Li | 160 °C 까지 안정 · 1000 사이클 @1 C · Li 도금 1000 h @1 mA cm⁻² · 정합률 96.2 / 95.3 / 97.1 % (`Fig. 15c` 인쇄값) | [163] |
| §4.4 | Co₃O₄ (산성 OER) — **다른 반응계** *(리뷰 표시)* | 결정면 진화 | 저지수 {110}·{100}·{211} 용해 · 고지수 {311}·{402} 출현 · 활성 ≠ 내구 결정면 | [166] |
| §4.5 | 폴리머 코팅 분리막 40–400 nm | 두께 | 가장 두꺼운 것 = 자가방전 최선 · 가장 얇은 것 = 율속·수명 최선 | [174] |
| §4.5 | SAC 의 S 피독 | 흡착 세기 | 너무 강한 M–S → 탈착 장벽 ↑ → 활성 자리 피복 · 피독 | [173] |
| §4.5 | 용존 LiPS 정량 (SI 소급 operando XANES) | 측정 | 충전 중 음극→양극 이동 억제 → 음극 쪽 누적 · LiPS 농도는 SOC·SOH 에 결합된 변수 | [169] |
| §4.5 | DME/DOL vs HME/DME (PS 포화 vs 신선) | 측정 | σ 가 (방)충전 상태에 따라 *"drastically"* 증가 (DME/DOL · 희박 전해질에서 최대) · 희박 용매화 전해질이 다층 파우치 율속 우위 | [170] |

### 3c. `Table 1` 전사 — *Separator-specific mass-transport metrics* (PDF 텍스트 + 단어 좌표 판독)

| Material/coating | t_Li⁺ | σ (mS cm⁻¹) | LiPS rejection | R_ct (Ω) | Ref |
|---|---|---|---|---|---|
| Janus LCL–TCL (V₂O₅/Al₂O₃) | — | — | H-cell: colorless, 12 h | — | [22] |
| V₂C MXene spheres | — | — | H-cell: 6.0 h | — | [37] |
| Janus PIM-1 (LCPIM-PEP-APIM) | 0.65 | 3.15 | — | — | [64] |
| PH/P/PH electrospun trilayer | — | 0.11–0.39 ⁽ᵃ⁾ | — | — | [66] |
| TPE covalent organic polymer@PP | 0.71 | 0.81 | — | — | [67] |
| APAN/Co-G electrospun bilayer | 0.72 | 1.73 | Self-discharge: 2 % | 56.29 | [68] |
| MoS₂₋ₓ-500@Celgard | — | — | H-cell: no change, 3 h | — | [75] |
| TiO₂₋ₓ@NMC@PP | — | — | Adsorption: 6 h | — | [80] |
| HNT@NC@Celgard 2325 | — | — | — | 201.5 | [91] |
| SVO/AB (N-doped VO₂) | — | — | — | 16.93 | [95] |
| Fe-ZIF-8/PP | — | — | H-cell: negligible, 24 h | — | [101] |
| Ni-ZIF-8-C@PP | — | — | H-cell: no permeation, 24 h | — | [102] |
| PSN/MXene 2D nanochannel | 0.70 | 1.48 | H-cell: blocked, 12 h | 38.6 | [103] |
| Cu SA/N–Ti₃C₂Tₓ@PP | — | — | — | — | [106] |
| Fe₁/NG@Celgard 2400 | — | — | H-cell: no diffusion, 48 h | — | [107] |
| KPW-CR6/GO/PP | — | — | UV-vis: 417 nm | — | [109] |
| Co-MoS₂/Ti₃C₂Tₓ@Celgard | — | — | Adsorption: 48 h | — | [131] |
| ZnTe–ZnO (polarized facet) | — | — | — | — | [134] |
| CF@ICOF (oriented (100)) | 0.925 | 2.19 | Permeation: 7.8 %, 24 h | 47.94 ⁽ᵇ⁾ | [141] |
| ANFs/β-FeOOH@PP | — | 0.85 | H-cell: transparent, 12 h | 112 | [142] |
| MS-HEO@Celgard | — | — | — | 90 | [155] |
| SA-Fe/HEO@NC | 0.60 | — | — | 22.90 | [158] |
| Liₓ TNO reservoir | 0.79 | — | — | — | [161] |
| SnSe₂@Ti₃C₂Tₓ@Celgard | 0.501 | — | H-cell: no equilibrium, 24 h | 21.88 | [175] |

각주 (원문): *"'–' = not reported. Values are not directly comparable across rows: R_ct was measured in full cells, Li‖Li or Li₂S₆ symmetric cells; σ by blocking-electrode or S–S symmetric cells; LiPS rejection by H-cell permeation, static adsorption/UV–vis, or self-discharge test."* ⁽ᵃ⁾ S cm⁻¹ 에서 환산 · ⁽ᵇ⁾ 풀셀 값 — Li‖Li 구성에서는 17.41 Ω (단어 좌표로 확인: ⁽ᵇ⁾ 는 ZnTe–ZnO 행이 아니라 **CF@ICOF 의 R_ct 47.94** 에 붙는다).

**우리 집계 (단어 좌표로 셈)**: 24 행 중 미보고 — t_Li⁺ **16** · σ **17** · LiPS 차단 **10** · R_ct **15** · **네 칸 모두 '—' 인 행 2** ([106] Cu SA · [134] ZnTe–ZnO). 리뷰 본문은 *"17 of 24 entries each"* (t_Li⁺·σ 각각) 라고 썼는데 t_Li⁺ 는 16 이다 (사소한 셈 오류 · §10b). 'LiPS rejection' 칸의 값도 시간 (h) · 투과율 (%) · 파장 (417 nm) · '색 없음' 이 섞여 **단위가 하나도 공통이 아니다**.

### 3d. DFT 서술자 값 (원전 2차 인용) + 홉 수 검산

| 서술자 | 계 | 값 | 그림 · 판독 | 계산 조건 기재 |
|---|---|---|---|---|
| O p-band center (vs E_F) | PSN → PSN/MXene | −4.627 → −3.475 eV (+1.15 eV 상향) | `Fig. 6g` figure-read (인쇄값) | n/a |
| SRR 단계 자유에너지 (S₈* → Li₂S₈* → Li₂S₆* → Li₂S₄* → Li₂S₂* → Li₂S*) | Co–N₄ | −2.70 · +0.23 · +0.49 · +0.67 · **+0.78** | `Fig. 7a2` figure-read (인쇄값 · 확대 재크롭) | 전위·용매 n/a |
| 〃 | Co–N₃Cl₁ | −2.57 · −0.11 · **+0.70** · +0.46 · +0.69 ⁽*⁾ | 〃 | 〃 |
| Li₂S 흡착 거리 | Fe–NC · Fe–NS₁C · Fe–NS₂C · Fe–NS₃C | 2.18 · 2.26 · 2.22 · 2.19 Å | `Fig. 7d` figure-read (인쇄값) | n/a |
| E_F − E_VBM (탄소 껍질) | H-Co@NC vs F-Co@NC | 2.38 vs 1.13 eV | `Fig. 8b` figure-read (인쇄값 · 도식) | n/a |
| Co–Se 결합 | CoSe₂ → P-CoSe₂ | 2.08 → 2.11 Å (+1.4 %) | 본문 | n/a |
| 최적 압축 변형 | phosphorene | −7 % | 본문 | n/a |
| ΔG(RDS) / Li₂S 해리 | NCO | ≈ 1.25 / ≈ 0.88 eV | `Fig. 10d` figure-read ≈ (확대 재크롭) | NEB 0 회 언급 |
| 〃 | MoS₂ | ≈ 1.21 / ≈ 0.78 eV | 〃 | 〃 |
| 〃 | MoS₂-Edge | ≈ 0.11 / ≈ 1.11 eV | 〃 | 〃 |
| 〃 | MoS₂@NCO | ≈ 1.06 / ≈ 1.55 eV | 〃 | 〃 |
| 〃 | MoS₂-Edge@NCO | **0.19 / 0.48 eV** (본문) | 본문 + 그림 일치 | 〃 |
| 내장 전기장 BEF | ZnTe(111)/ZnO(101) | ≈ 0.38 V Å⁻¹ | 본문 · `Fig. 11b` Δρ(z) 최대 ≈ +0.55 · 최소 ≈ −0.34 ×10⁻³ e Å⁻³ (figure-read ≈) | 부호 규약 n/a |
| Li⁺ 이동 장벽 | ICOF (100) 면 | **0.715 kcal mol⁻¹ = 0.031 eV** (우리 환산) | 본문 | n/a |
| 격자 불일치 δ | β-FeOOH ↔ PPTA | 5.9 % (12.136 vs 12.900 Å) · 2.1 % (10.600 vs 10.380 Å) · 1.3 % (10.513 vs 10.380 Å) | `Fig. 12d` figure-read (인쇄값) · 우리 재계산 일치 | — |
| **흡착에너지 'E_a'** | TiO(111) / **TiO(001)** / TiO₂(101) | S₈ −1.53 / **−18.45** / −9.33 · Li₂S₈ −3.05 / **−14.33** / −11.58 · Li₂S₆ −2.51 / −12.57 / −9.26 · Li₂S₄ −3.01 / −11.16 / −7.89 · Li₂S₂ −3.36 / −6.60 / −4.09 · Li₂S −3.08 / −3.88 / **−4.84** (eV) | `Fig. 12f` figure-read (인쇄값) | **구조 비공개 · 정의식 n/a** |
| 'lattice matching ratio' | PW 클러스터 O ↔ LiPS·Li₂S 의 Li | 96.2 · 95.3 · 97.1 % · 거리 1.677 · 1.727 Å | `Fig. 15c` figure-read (인쇄값) | 정의 n/a |
| 계산 XANES 주 피크 | S₈ vs 입방 Li₂S₃ | 2472.0 vs 2471.0 eV | 본문 · `Fig. 16d` (계산 스펙트럼 · 박사논문) | 에너지 정렬법 n/a |
| configurational entropy | HEO 단일상 기준 | S_config ≥ 1.5 R | 본문 | — |

⁽*⁾ `Fig. 7a2` 의 마지막 붉은 라벨은 저해상도에서 '0.09' 처럼 보이지만 **0.69 로 읽었다** — 누적합 −2.57 − 0.11 + 0.70 + 0.46 + 0.69 = **−0.83 eV** 가 그림에 그려진 Li₂S* 준위 (≈ −0.83 eV, figure-read ≈) 와 맞고, 0.09 면 −1.43 eV 가 되어 그림과 어긋난다 (우리 산수).
⇒ 가장 높은 오르막 계단: Co–N₄ **0.78 eV** (Li₂S₂*→Li₂S*) vs Co–N₃Cl₁ **0.70 eV** (Li₂S₆*→Li₂S₄*) — 차이 **0.08 eV ≈ 3 kT** (298 K) 이고 율속 단계의 정체가 바뀐다. 이 패널은 **방전 방향 (S₈ → Li₂S) 자유에너지**다 — 본문이 이 그림에 붙인 *"reduced Li₂S decomposition barriers"* 가 아니다 (§10b).

**홉 수 검산** (`D-2026-09-27-barrier-hop-count` · `tools/sei/collect_neb.py::hop_check` · ν₀ 10¹³ s⁻¹ **가정** · 298 K · 창 t = 1 h = 3600 s — 차수 검산이지 속도·전도도가 아니다):

| 장벽 | Ea | Γ | 평균 대기 1/Γ | 1 h 동안 N |
|---|---|---|---|---|
| ICOF(100) Li⁺ 이동 | 0.031 eV (= **1.2 kT**) | ≈ 3.0×10¹² s⁻¹ | ≈ 0.33 ps | ≈ 1.1×10¹⁶ |
| MoS₂-Edge@NCO Li₂S 해리 | 0.48 eV | ≈ 7.6×10⁴ s⁻¹ | ≈ 13 µs | ≈ 2.7×10⁸ |
| MoS₂ Li₂S 해리 | ≈ 0.78 eV (figure-read) | ≈ 0.64 s⁻¹ | ≈ 1.6 s | ≈ 2.3×10³ |
| NCO Li₂S 해리 | ≈ 0.88 eV (figure-read) | ≈ 1.3×10⁻² s⁻¹ | ≈ 76 s | ≈ 47 |
| MoS₂-Edge Li₂S 해리 | ≈ 1.11 eV (figure-read) | ≈ 1.7×10⁻⁶ s⁻¹ | ≈ 5.9×10⁵ s (≈ 7 일) | ≈ 0.006 |
| MoS₂@NCO Li₂S 해리 | ≈ 1.55 eV (figure-read) | ≈ 6×10⁻¹⁴ s⁻¹ | ≈ 1.6×10¹³ s (≈ 50 만 년) | ≈ 2×10⁻¹⁰ |

1 h 창에서 한 번이라도 넘을 수 있는 장벽의 상한 ≈ **0.98 eV** (`observation_window(298 K, 3600 s)`).
⇒ 읽는 법: ① **0.031 eV 는 활성화 장벽이 아니라 열 요동 크기**다 — "(100) 면이 가장 낮은 장벽" 이라는 결정면 순위의 근거가 못 되고, 측정된 σ 2.186 mS cm⁻¹ 는 기공 속 액체 전해질이 정한다. ② 0.48 eV 와 대조군 0.78–0.88 eV 는 **둘 다** 1 h 충전 창보다 몇 자릿수 빠르다 → 셀 율속 차이를 이 장벽 하나로 설명하면 차수가 안 맞는다. ③ 1.11 · 1.55 eV 를 글자 그대로 읽으면 그 자리의 Li₂S 는 상온 충전 중 **분해되지 않는다** — 영 바이어스 · 중성 클러스터 해리라는 **모델 서술자 (상대 순위)** 이지 속도가 아니다.

### 3e. 리뷰 자체 집계 (우리 분류 · ±2)

- **사례 ≈ 55 건**의 위치: 본문이 분리막 쪽 (코팅 · 인터레이어 · 자립 분리막) 이라고 명시한 것 ≈ **35** · 리뷰가 스스로 '분리막 아님' 을 밝힌 것 **5** ([85] 양극 · [97] 전해질 · [123] ASSB 양극 · [160] 음극 · [166] OER) · **표시 없이 분리막이 아니거나 위치 미상 ≈ 12** ([60] [112] [117] [118] [122] [124] [125] [132] [137] [156] [159] [162]) — 그리고 §5 특성분석 예시 5 건은 Na 이온 양극 ([176] [177] [183]) · Li–S 양극 ([35]) · 흡유 스펀지 ([182]) 다.
- 셀 성능 숫자는 거의 전부 **끝점 지표** (초기 용량 · n 사이클 후 용량 · %/cycle 감쇠) — §4.5 가 *"insufficient for establishing separator performance"* 라고 부른 바로 그 형식이다.
- 고적재·희박 전해질 조건이 같이 보고된 사례는 소수: Sb₂Se₃₋ₓ (8.1 mg cm⁻²) · Co-MoS₂/Ti₃C₂Tₓ (5.7 mg cm⁻² · E/S 6) · H-Fe-Ce (10.17 mg cm⁻²) · CF@ICOF (11.12 mg cm⁻² · E/S 3.5) · MS-HEO (7 mg cm⁻²) · Fe₃N/Fe-NC (6.668 mg cm⁻²) · 1T-MoS₂ (E/S 2.1, 양극 host).

---

## 4. DFT / 계산 방법 ★

- **리뷰 자체 계산: 0.** 모든 계산 수치는 원전의 2차 소환이다.
- **원전 계산 조건이 옮겨진 정도** (본문 텍스트 전수 검색):
  - 범함수: *"PBE"* **3 회** (전부 §5.2 일반론) · *"HSE06"* **1 회** (일반론 *"were further employed to correct the electronic structure"* — 어느 연구가 썼는지 없음) · *"DFT-D3"* **1 회** ([187] MSi₂P₄ 단층과 Li₂Sₓ/S₈ 의 vdW 상호작용) · `Fig. 3d` 캡션 *"DFT (black) and DFT-D (blue)"*.
  - **vdW · +U · k-점 · 컷오프 · 셀 크기 · 스핀 처리 · 용매 · 전위 기준: 0 줄.** d-band center (본문 16 회) · p-band center (5 회) · 흡착에너지 · ΔG 계단 · 해리 장벽 · 스핀 상태 서술 전부 조건 n/a.
  - 코드·도구 이름: VASP · QE · CASTEP · LOBSTER · pymatgen · VESTA · Materials Studio **각 0 회**. NEB · climbing image **0 회** (장벽 수치는 나오는데 계산법이 없다).
- **무질서 처리**: 고엔트로피 산화물·합금 절 (§4.2) 은 전부 실험 (XRD · EIS · Tafel · t_Li⁺) — SQS · 배열 열거 같은 계산 언급 없음.
- **AIMD**: §5.2 와 결론의 일반론 3 회 (*"accurately simulates diffusion paths … estimates migration energy barriers to predict ionic conductivity"*) — **구체 AIMD 결과 0 건** → 관측창 규율 (`D-2026-10-05-md-observation-window`) 을 적용할 대상이 없다.
- **MLIP: 0 회.** AI 는 §6 전망 한 문단 (*"AI-assisted design"* · 구체 모델 0).
- **§5.2 의 인용 역할 불일치**: *"DFT calculations are employed to predict and verify the impact of crystal engineering strategies … [186]"* 의 [186] 은 **Na 이온 NASICON 양극** 논문 · *"AIMD predicts the dynamic migration behavior of ions … [188]"* 의 [188] 은 **Na 이온 층상 고엔트로피 양극 리뷰** — 둘 다 그 문장의 원전 역할이 아니다.
- **스핀**: *"Boron, acting as a strong ligand, reduced the spin state of Co from intermediate to low spin"* ([132]) — 스핀 상태 에너지는 범함수·U 에 민감한데 조건 0 줄. 우리 보고량 규율이 말하는 *"여러 허용 상태 + 선택 규칙 없음"* 의 위험 신호 (열린 껍질 Co · 자성 기판) 가 그대로 있다.
- **Li₂S 계산** (§2): [54] [57] [63] 이 밴드 · 포논 · DFPT 류 (Born 전하 · 유전상수 · LO–TO) · 준조화 (a(T) · B₀(T)) 를 했다고 읽히지만, 리뷰는 어느 범함수인지 말하지 않는다 — `Fig. 3d` 의 *"DFT vs DFT-D"* 만으로는 GGA 인지조차 확정할 수 없다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 §1 서론 — 왜 분리막이고 왜 '결정공학' 인가 (`Fig. 1` · `Fig. 2`)

- Li–S 의 세 문제: ① LiPS 셔틀 (용해 → 음극과 반응 → 활물질 손실·CE 저하·Li 부식) ② Li 덴드라이트 (분리막 관통 → 단락) ③ S₈ → Li₂S **~80 % 부피팽창**.
- 분리막 개질의 장점: *"without significantly sacrificing the energy density, volume, or weight"*. 상용 PP 는 전자 절연 · Li⁺ 통로는 있으나 LiPS 를 못 막는다 · **과전압 > 250 mV 면 에너지밀도 ≥ 20 % 하락** ([32] [33]).
- van der Waals 로 붙인 복합체는 계면 전자 상호작용이 약해 촉매 효과가 제한된다 → **공유결합 이종계면** (MoS₂ 의 Mo–O–C) 사례로 넘어간다.
- `Fig. 1` (실독): (a) Li–S 셀 모식 (Manthiram 2014) (b) 셔틀 모식 (c) V₂C MXene 구 분리막의 *"dual effect"* — 양극 쪽 빠른 LiPS 전환 + 음극 쪽 조절된 Li⁺ 흐름 (d) 촉매 크기 ↓ → 활성 자리 이용률·비활성 ↑ 도식. 캡션 (c,d) *"Copyright 2026"* 인데 ref [37] 은 *Adv. Mater.* 35 (**2023**) — 연도 어긋남.
- `Fig. 2` (실독 · 도구 누락분 손 크롭): 1912–2026 연표 — 이론 기초 (Bragg · Debye · Bloch 1928 · 격자결함 1934 · 결정성장 1950) → 다공 격자 (MOF 1999 · 그래핀 박리 2004) → 에너지 응용 (2D MXene 2011–15 · SAC 2016–18 · 격자결함 공학 2019–22 · 격자변형 공학 2023–24 · **동적 격자 응답 2025–26**). Bragg 법칙을 1912 에 놓았는데 본문은 1913.

### 5.2 §2.1 격자 진동 — Li₂S 의 전자·포논 (`Fig. 3a–f`)

- 리뷰의 출발 명제: *"The insulating nature of Li₂S … imposes two major obstacles: sluggish reaction kinetics and the shuttle effect"* · *"the insulating behavior of Li₂S is dictated by its intrinsic electronic structure, an inherent property of its crystal lattice."*
- [54] Li₂S: 간접 gap 3.398 eV → *"implying that neither electrons nor holes can migrate through the Li₂S lattice"* (과대서술 · §10-⑤) · 포논 분산은 동역학 안정 + 큰 LO–TO 분리 · S Born 전하 ≈ 1.91 · ε₀ 7.80 (격자 분극 지배).
- Raman/IR 계산: 주 Raman 피크는 Li⁺ 대칭 신축, S²⁻ 신호는 *"remarkably weak"* → *"experimentally challenging to … monitor … Li₂S using conventional Raman"* (§10-⑤ 에서 대칭 논리로 반박).
- 처방: *"p-band doping strategies"* 로 Li₂S 전도도 향상 + Raman 신호 증폭 + S²⁻ 용해 억제 — **근거 인용 없음**.
- [57] Peng: c-/o-Li₂S 와 h-/t-Li₂S₂ 의 gap · 흡수 · LO–TO → 빛–격자 결합 (*"photon-phonon coupling"*) 으로 Li₂S₂ 의 S–S 절단을 촉진해 *"steers the reduction pathway toward the direct generation of Li₂S"* — LO–TO 분리라는 극성 결정 일반 현상에서 셔틀 억제까지 건너뛴다 (§10-⑤).
- 폴라론: Ni₂P 의 P 공공 → 작은 폴라론 → 전자전도 ↑ · Ni 배위수 ↓ · 표면 전자밀도 ↑ (π–π · π–d) · d-band center ↑ → Li₂S₂ → Li₂S 장벽 ↓ (901.2 mAh g⁻¹ @1 C · 1000 사이클 0.06 %).
- `Fig. 3` (실독 · 확대 2회):
  - (a) W–L–G–X–W–K 밴드, VBM 0 eV, Γ → X 화살표에 **3.398 eV** · m_v* = −0.77 표기.
  - (b) 포논 분산 + DOS, G 근처 'LO' · 'TO' 라벨.
  - (c1) Raman: ≈ 373 cm⁻¹ 한 피크 'Li⁺ s-str.' (이 작업 vs Xue et al. 겹침) · (c2) IR: ≈ 320 cm⁻¹ 한 피크 'Li⁺ a-str.' (figure-read ≈).
  - (d) 네 상 밴드, 검정 = DFT · 파랑 = DFT-D: h-Li₂S₂ 1.00 / 1.01 · t-Li₂S₂ 1.77 / 1.81 · c-Li₂S 3.40 / 3.40 · o-Li₂S 4.06 / 4.06 eV (인쇄값) — **본문 숫자 (1.010 · 1.814 · 3.398 · 4.061) 는 DFT-D 쪽**이다. 분산 보정이 gap 을 거의 안 바꾼다.
  - (e) 흡수계수 α (10⁵ cm⁻¹) vs 에너지 0–10 eV: c-Li₂S · h-Li₂S₂ · t-Li₂S₂ **세 곡선** (캡션은 두 상만 말함) · 셋 다 개시 ≈ 4.5 eV · ≈ 2.6×10⁵ cm⁻¹ 에서 평탄 (figure-read ≈). 본문의 *"high propensity for optical transitions within the visible and near-ultraviolet regions"* (Li₂S₂ 의 작은 gap) 는 이 축척에선 **보이지 않는다** — 1–4 eV 구간 α 는 0 에 붙어 있다.
  - (f) LO/TO 인쇄값 (§3a) — c-Li₂S **80 cm⁻¹**.

### 5.3 §2.2 탄성·격자 안정 — 그리고 분리막으로의 다리 논증 (`Fig. 3g–h`)

- **2.2.1** [63] Saib: Li₂S 원시 셀 3 원자 → 음향 3 + 광학 6 · 입방이라 독립 탄성상수 3 개 · 압력에 따라 탄성상수 선형 증가 · 0 → 10 GPa 에서 포논 상한 500 → 566 cm⁻¹ · LO–TO 132 → 107 cm⁻¹ · 결합 짧아짐 → 힘상수 ↑ · 이온성 ↓.
  - `Fig. 3g1/g2` (실독 · g1 확대): Γ–K–X–Γ–L–X–W–L 분산 + Li (빨강) · S (초록) PDOS — **고진동수 (> 250 cm⁻¹) 는 Li, 저진동수는 S** 가 지배 (질량비대로). Γ 의 광학 가지 ≈ 325 · ≈ 377 · ≈ 456 cm⁻¹ (figure-read ≈) → LO − TO ≈ 131 ✓ (본문 132 와 일치).
  - `Fig. 3h1` a(T) ≈ 5.688 → 5.737 Å (0 → 1000 K) · `Fig. 3h2` B₀(T) ≈ 40.2 → 32 GPa (figure-read ≈) — *"crystal elasticity … increases monotonically with applied pressure but decreases as temperature rises."*
  - 리뷰는 *"Li₂S remains dynamically stable up to 10 GPa, a pressure range that covers by a wide margin the mechanical stress levels relevant to separator operation"* 라고 쓴다 — 맞지만 **분리막 응력 (MPa) 보다 3–4 자릿수 큰 범위의 정수압 안정성**이라 아무것도 말해 주지 않는다. Li₂S 가 기공 안에서 실패하는 방식 (파괴 · 박리 · 재용해) 은 이 숫자와 무관하다.
- **다리 논증 — 이 리뷰에서 가장 좋은 단락** (§2.2.1 끝): Li₂S 는 전자 절연이라 **전자가 닿는 곳 (전도성 코팅 표면) 에서만 핵생성**한다 → Li₂S 는 양극 벌크만이 아니라 **분리막 코팅 위·기공 안에도 쌓인다** → 세 귀결:
  1. 절연 Li₂S 가 기공을 막아 Li⁺ 통로 ↓ · 계면저항 ↑ (분리막의 1차 기능 훼손).
  2. 코팅이 제공하려던 촉매 자리를 **패시베이션** → 결함·결정면 공학 분리막의 활성이 방전 산물이 쌓일수록 감소 — *"a failure mode that static, ex situ characterization of the pristine coating cannot predict"*.
  3. 좁은 기공 안 고체 Li₂S 의 반복 석출·용해 → 주기적 국소 응력.
  ⇒ *"the challenge for separator design is therefore not the stability of Li₂S, but managing where it nucleates, how quickly it passivates the coating, and how completely it can be re-oxidized on charge."*
- **2.2.2 격자 안정** ([69] Guo 박사논문):
  - 계면: 그래핀을 SnO 단층 둘 사이에 끼우면 그래핀에 gap 이 열리고 0.3×10¹⁰ V m⁻¹ 장까지 유지 · SnO 한 층을 빼면 p 형 Schottky · 장 방향에 따라 p→n 전환 / Ohmic → *"functional separators may possess the electronic stability required to adapt to varying charge-discharge potentials"* (그래핀/SnO 계산에서 분리막 일반론으로의 비약).
  - 벌크: 고체 LiPS 는 α-S₈ + Li₂S 대비 수십 meV/atom 준안정 · vdW 가 안정화 · Li₂S₂ 는 전부 S–S 이량체 · 이량체 방향이 탄성 이방성을 정한다 · 고차 → 저차 LiPS 로 갈수록 **E · G · B 가 증가** — 그런데 같은 단락 끝에서 *"Low-order products, especially Li₂S, possess low moduli and large volumetric strains"* — **같은 단락 안 자기모순** (§10-⑤).

### 5.4 §3 머리 + `Fig. 4` — 6 전략 × 3 기능 매트릭스

- §3 머리: 분리막 연구는 대부분 **코팅 개질**이다. 각 전략은 (i) Li⁺ 수송 (ii) LiPS 차단 (iii) 계면 화학·기계 안정 중 하나 이상을 노린다. *"no single strategy optimizes all three functions simultaneously, since each entails a balance between competing properties (Section 4.5)"*.
- `Fig. 4` (실독 · 리뷰 자체 작성) — 등급 전사 (●● 지배 · ● 중요 · ○ 부차/위험):

| 전략 | Li⁺ 수송 | LiPS 차단 | 화학·기계 안정 |
|---|---|---|---|
| Defect | ○ defect-assisted channels | ●● vacancy adsorption / catalytic sites | ○ vacancy annihilation risk |
| Doping | ● conductivity, d-band tuning | ●● heteroatom anchoring, SAC coordination | ● stable coordination environment |
| Phase/Strain | ●● metallic phase, strain channels | ●● d-band upshift, BIEF charge separation | ● strain management, zero-strain design |
| Facet/Morph | ●● oriented channels, ion selectivity | ●● high-index facets, polarization field | ● uniform Li⁺ flux, anti-dendrite |
| Entropy | ● lattice distortion, Ov-mediated | ● multi-element "cocktail" synergy | ●● entropy stabilization, phase reversibility |
| Dynamic | ●● transient N–Li bonds, ion network | ●● adaptive reconstruction catalysis | ● reversibility to be verified |

  ⚠ 등급의 근거 데이터는 없다 (정성 판단). 그림 오타 *"Dopingn"* · 머리칸 *"Defect Engineering"* 중복 · Dynamic 의 안정 칸은 라벨이 *"to be verified"* 인데 ○(위험) 가 아니라 ● 다.
- §3.1 의 **방법 규약 단언**: *"the modified separator was always benchmarked against the unmodified separator … within identical cell configurations … Under such protocols, the observed differences … can be attributed to the separator itself"* — 192 편 전수 확인 근거 없음 · §4.4 의 '분리막 열화와 양극 열화가 뒤섞인다' 와 긴장 (§10-⑫).

### 5.5 §3.1 결함 공학 (`Fig. 5`)

- 결함의 세 차원: (i) 전자구조 (음이온 공공 = 전하보상 중심 → 이웃 원자 전자 재분배 · gap 내 결함 준위 → 유효 gap ↓ · 전도 ↑) (ii) 표면화학 (배위 불포화 → 표면에너지 ↑ · Lewis 산/염기 → 물리흡착 → 화학흡착) (iii) 촉매 자리 (특정 양이온 공공·결함쌍이 d-band 재구성 → **Sabatier** 최적 근처로).
- **3.1.1 음이온 공공** — V_O · V_S · V_Se:
  - Sb₂Se₃₋ₓ/RGO: `Fig. 5b` (실독) EPR — Sb₂Se₃₋ₓ/rGO (주황) 가 가장 크고, **Sb₂Se₃/rGO (파랑) 에도 작은 신호**, 탄소 없는 Sb₂Se₃ (초록) 은 평평 · g = 2.00. 본문은 이 신호를 Se 공공의 짝짓지 않은 전자로 읽는데, **g ≈ 2.00 은 rGO 탄소 라디칼과 겹치는 값**이라 귀속이 유일하지 않다 (§10-⑦).
  - CeO₂/CNT: `Fig. 5c1` HAADF CeO₂(111) d = 0.32 nm · `Fig. 5c2` 강도 지도 'Oxygen vacancy' 표시 — 국소 격자 왜곡을 V_O 의 지문으로 읽음 · 셀 수치 없음.
  - TiO₂₋ₓ@NMC: 탄소열로 V_O 생성 · 젖음 ↑ · Li⁺ 전달 ↑ · 자가방전 ↓ · `Fig. 5d` (실독) 인장 응력–변형 — 코팅 PP ≈ 250 · 맨 PP ≈ 128 MPa (≈ 42 % 변형에서 파단, figure-read ≈) · 축 라벨 'Stress (Mpa)'. 응력의 단면적 기준 (코팅 두께 포함?) 은 그림에 없다.
  - 탄소는 비극성이라 LiPS 친화도 ↓ → 원자 Co 주입 (SC-Co · `Fig. 5f`).
  - 리뷰의 경고: *"V_O sites may undergo self-repair during prolonged cycling"* → 공공 농도·코팅 기계 무결성을 operando 로 추적해야 양극 열화와 분리된 분리막 내구성을 안다.
- **3.1.2 양이온 공공**: 이종 원자가 치환 → 전하보상 공공·틈새 → 배위 기하 변화 · 활성 표면 노출 · 전도 ↑ · 장벽 ↓.
  - `Fig. 5g` (실독) = **Famprikis 2019 의 SE 이온 이동 3 기구** (vacancy · direct interstitial · correlated interstitialcy) — 촉매 코팅의 공공 이야기에 고체전해질 이동 기구 그림을 가져왔다.
  - 양이온 공공은 도입·안정화가 음이온 공공보다 어렵다 → 연구가 적고 대부분 **양극 벌크 개질** — 리뷰가 Fe₀.₉₆S@C 를 *"should accordingly be attributed to the cathode side"* 로 **스스로 표시**한 몇 안 되는 자리다.
  - STMnₓ: Mn³⁺/Mn⁴⁺ 평균 원자가 < Ti⁴⁺ → V_O ↑ → LiPS 결합 ↑ · 분해 장벽 ↓ · 상전이 속도 ↑ (정성).
  - LDH: VCFN (V=O–LiPS Lewis 산염기) · Co₀.₅Ni₀.₅Te₂ (전자전도 1.15×10⁶ S m⁻¹).

### 5.6 §3.2 도핑 공학 (`Fig. 6` · `Fig. 7`)

- **3.2.1 음이온 도핑** (N · S · B · P): 도핑 원자 = Lewis 염기 ↔ LiPS 의 Li⁺ (Lewis 산) · 전하 재분배로 전도·촉매 ↑ · 단일 vs 다중 음이온 공도핑.
  - `Fig. 6a` SVO/AB 합성 (V-ZIF → Ar 350 → 700 °C → SVO + 아세틸렌블랙 → PP 코팅) · SVO/AB 가 **'보조 집전체'** 역할 (= 양극의 일부처럼 일한다).
  - T-NSCC: `Fig. 6b` (실독) Li 1s Li–N 56.4 · Li–S 55.3 eV · `Fig. 6c` 기능 모식 — ⚠ `Fig. 6c` 왼쪽 끝에 이 패널과 무관한 **'Coulombic Efficiency (%)' 세로축 라벨**이 남아 있다 (재조립 흔적).
  - 액체상 '음이온 공학' (FSI⁻ · TTE) 은 *"entirely outside the separator's structural scope"* 라고 리뷰가 스스로 표시.
- **3.2.2 양이온 도핑**: d-band center 이론 — 상향 = 흡착 ↑ (과하면 탈착 방해) · 적당히 하향 = 흡착·전환 균형.
  - `Fig. 6d` (실독) Fe-ZIF-8/PP H-cell 투과 시험 10 min · 3 h · 6 h · 12 h — 오른쪽 칸 끝까지 투명. `Table 1` 은 *"24 h"* 인데 그림은 **12 h 까지만**.
  - `Fig. 6e` Ni-ZIF-8-C 합성 (2-메틸이미다졸 + Zn 아세트산 + Ni²⁺ → ZIF-8@Ni²⁺ → 탄화).
  - **나노유체 이온 선택**: *"when the Debye screening length of the fluid electrolyte exceeds the dimension of nanofluidic (NF) channels, the electric double layers … overlap"* → 표면전하 지배 선택 수송. `Fig. 6f` (실독) zeta: MXene −25.0 mV · **PSN/MXene −10.9 mV** (덜 음전하) · `Fig. 6g` (실독) PDOS (electrons/eV) — PSN O p-band center **−4.627 → −3.475 eV** (PSN/MXene, E_F 쪽 상향) → 극성–극성 포획 ↑ · 수산기의 Grotthuss 류 Li⁺ 홉핑. ⚠ 1 M 에테르 전해질의 Debye 길이 문제는 §10-⑨.
- **3.2.3 배위 조절**:
  - W/NG (W–N₂O₂–C) · **REV** (*Relative Electronegativity Value* = 치환 원자 X 와 N 의 전기음성도 차) → Cl 치환이 최적 REV → Co–N₃Cl₁.
  - `Fig. 7a1` (실독 · 확대) 비대칭 배위 SAC 감쇠율 비교 — 0.5 · 1 · 2 · 4 · 5 C 가 섞인 x 축 · E/S > 20 / < 20 / = 20 µL mg⁻¹ · '미상' 기호 · **S ≈ 1 mg cm⁻²** · 'This work Co–N₃Cl₁ 804.3 mAh g⁻¹' 별표 ≈ 0.023 %/cycle (figure-read ≈). = 리뷰 §4.5 가 비판하는 **조건이 다른 끝점 지표의 교차 비교**를 그대로 실었다.
  - `Fig. 7a2` (실독 · 확대) S₈ → Li₂S **방전** 자유에너지 계단 (§3d) — 최대 오르막 0.78 (Co–N₄) vs 0.70 eV (Co–N₃Cl₁).
  - `Fig. 7b,c` M SA/N-Ti₃C₂Tₓ (MAX → 식각·박리 → 멜라민 어닐링) · 주기율표에 Mn · Co · Ni · Cu · Zn · In · Sn · Pb · Bi 표시.
  - `Fig. 7d` Fe–NC vs Fe–NSₓC 의 Li₂S 전하차밀도 · 거리 2.18–2.26 Å · *"lower electronegativity of sulfur results in a higher charge density around the Fe-NSC configuration"*.
  - `Fig. 7e` 3 C · S 2 mg cm⁻² · 300 사이클: Fe–NSC@GO ≈ 735 → 520 · Fe–NC@GO ≈ 660 → 345 mAh g⁻¹ (figure-read ≈) — 본문은 이 그림을 *"Figure 6e"* 라고 잘못 가리킨다.
  - `Fig. 7f` KPW-CR6: [PW₁₂O₄₀]³⁻ 1 + [K(Cr6)]⁺ 2 + [K(Cr6)(CH₃CN)₂]⁺ 1 의 수소결합 3D 골격 · 크라운에테르가 POM 을 감싸 이온 채널.
  - Se₀.₀₆SPAN/MMT@PP — 분리막 **재사용** 가능 (기계·구조 내구성의 사례로 읽음).

### 5.7 §3.3 상전이 · 격자 변형 · 이종접합 (`Fig. 8` · `Fig. 9` · `Fig. 10`)

- **3.3.1 외부 유도 상전이** (이온 삽입 · 온도 · 결함):
  - MoS₂ 2H (반도체) → 1T (금속) — 전도도 10⁷ 배 · 마이크로파 박리 (MWCE) 로 72 h → 30 s · 1T ≈ 100 % · `Fig. 8a1/a2` (실독) J1 · A1g Raman 강도 지도 (Void · Edge oxidation 표시 · 10 µm) — 1T (J1) 가 넓게 균일. 단 이 재료는 **양극 host** 다 ([112] 박사논문 · 표시 없음).
  - TiN/1T-MoS₂: `Fig. 8d` (실독) SiO₂ → TiO₂ 코팅 → NaOH 식각 → 수열 200 °C (TiO₂/2H-MoS₂) → NH₃ 800 °C (TiN/2H-MoS₂). 본문 *"decorated on tin nanospheres"* 는 **TiN 의 오기**.
  - F-Co@NC vs H-Co@NC: FCC Co 의 E_F 가 HCP 보다 높아 탄소 껍질 VBM–E_F 간격 ↓ → 전자 공여 ↑ · `Fig. 8b` (실독) 띠 도식 **2.38 vs 1.13 eV** · `Fig. 8c` (실독) HCP(0001) ABAB vs FCC(111) ABC · 낮은/높은 전위구배 · 'moderate shuttling' vs 'suppressed shuttling'.
  - P-CoSe₂/MXene: P 도핑 → 입방/사방 혼합 → 순수 사방 · **인장 변형** (Co–Se 2.08 → 2.11 Å) · DFT 로 d-band 상향 · `Fig. 8e1–e3` (실독) 치환 도식 · d-band 상향 도식 · 분리막 '선택적 이온체'. 본문 *"increased the concentration of the 1T phase"* 는 CoSe₂ 에 안 맞는 표기 (§10b).
- **3.3.2 격자 변형**:
  - La₂Ce₂O₇/rGO: `Fig. 9a` (실독) Ce⁴⁺ + La³⁺ + 트리메스산 → 오일조 → La/Ce-MOF → 머플 소성 → 볼밀 + rGO · `Fig. 9b1/b2` d(111) **0.324 vs 0.318 nm** — 리뷰는 이것을 *"La doping induced lattice strain and local expansion"* 으로 읽지만, **다른 화합물 (La₂Ce₂O₇) 의 평형 격자상수가 큰 것 (화학 팽창)** 이지 탄성 변형이 아니다 (§10-⑧).
  - 황 팽창: 리튬화 4 단계 · 중간 침전물이 팽창의 ≈ 48.64 % 완충 ([121]) — 본문은 이것을 `Fig. 9c` 로 가리키는데, `Fig. 9c` (실독) 는 **Cui 2024 *Nat. Energy* 의 ASSB 복합양극** (집전체 · 고체 전해질 층 · 양극 활물질 · 도전재) 이 탈리튬 중 **이종 (균열 · 박리 · 고저항상)** vs **균질** 로 갈리는 미세구조 도식이다. 황 리튬화 4 단계도 응력 곡선도 없다.
  - zero-strain (부피변화 < 1 %) → > 20,000 사이클 · Zr-LAO (음극) · Cui 2024 (ASSB 양극, 부피변화 1.2 % — 리뷰가 *"demonstrated on the cathode side rather than as a separator modification"* 으로 표시).
  - 압축 변형이 LiPS 흡착 ↑ · phosphorene 최적 −7 % · 이축 변형 MoS₂ 계 (MSS): 곡률 ↑ · S 공공 생성 장벽 ↓ · 저배위 Mo 노출 · Mo d-band · S p-band 상향 → 흡착 기구가 약한 Li–S 결합에서 강한 S*–Mo 결합으로 · `Fig. 9d` (실독) 도식 (배위 조정 → 전자 비편재화 → d-band 상향 → 반결합 상태 감소 → d–p 결합 강화) · 623 mAh g⁻¹ @6.7 mA mg⁻¹ · 파우치 396 Wh kg⁻¹.
  - 경고: *"any artificially introduced lattice strain must remain within the elastic limit"* — §2.2 로 되돌아가는 연결 문장.
- **3.3.3 이종접합**: '흡착–촉매–전환 삼위일체' 계면 · 내장 전기장 (BIEF) 이 전하 분리 · 계면 원자배위 변화가 활성 자리.
  - Ti₃C₂@TiO₂: UV 조사 시간으로 TiO₂ 양 조절 (가장자리 → 중심) · 최적 40 min · `Fig. 10a` (실독).
  - Co-MoS₂/Ti₃C₂Tₓ: S 공공 + Co 도핑 + MXene 전자 경로 · `Fig. 10b` (실독) 5 단계 도식 (빠른 전환 · 강한 흡착 · 빠른 핵생성 · 빠른 분해 · 빠른 전자 수송).
  - MoS₂@CF-NRGO: `Fig. 10c1/c2` (실독) MoS₂@NCO · MoS₂-Edge@NCO 전하차밀도 · `Fig. 10d` (실독 · 확대) ΔG(RDS) · Li₂S 해리 막대 (§3d). 본문은 *"Gibbs free energy of merely 0.19 eV, indicating excellent catalytic activity of MoS₂ nanobelts"* 라고 쓰는데 그림에서 **0.19 eV 는 MoS₂-Edge@NCO (결합 후)** 값이고, 결합 전 MoS₂-Edge 단독은 ≈ 0.11 eV 로 더 낮다 · 기저면 MoS₂@NCO 는 해리 ≈ 1.55 eV 로 **결합이 오히려 나쁘게** 만든다 — '이종계면이 전환을 촉진한다' 는 가장자리 모델에서만 성립한다.
  - CoB/Co–CoP: 비정질 CoB 가 BIEF 세기 조절 · B 가 강한 리간드로 Co 를 중간 → 저스핀 · d–p 간격 ↓ · 쌍극자 정렬 · `Fig. 10e1–e3` (실독) 합성 (Co²⁺/Zn²⁺ + 이미다졸 · CTAB 24 h → TA 식각 10 min → 900 °C 2 h Ar 탄화 → 350 °C 2 h PH₃/Ar 인화 → NaBH₄ 1 h 붕소화) + '전기–스핀–쌍극자' 도식 — 수치 0.

### 5.8 §3.4 결정면 공학 (`Fig. 11` · `Fig. 12`)

- 극성 표면이 LiPS (말단 S 에 음전하) 를 잡는다 · 격자 불일치로 특정 방위를 만들어 계면 분극 → 방향성 내장장 (BEF) → *"lower the redox reaction barrier via the Stark effect"* · 분리막 코팅이면 계면 전기장을 균일화해 덴드라이트 억제.
- **3.4.1 고지수면**: 계단 · 꺾임 · 전위 같은 저배위 원자 밀도 ↑ → 표면에너지 ↑ · 불포화 결합 → 강한 화학흡착 + 전환 장벽 ↓.
  - ZnTe(111)/ZnO(101): `Fig. 11a` (실독) 결정면 불일치 ≈ 5 % · 자발 분극 → 분극 전기장 · 양극 쪽 (다중 흡착 자리) + 음극 쪽 (균일 Li⁺) · `Fig. 11b` (실독) 평면평균 Δρ(z) (10⁻³ e Å⁻³) vs 거리 0–16 Å — ZnO(101) 영역 (파랑, ≈ 5.3–7 Å) 음 · ZnTe(111) 영역 (빨강, ≈ 7–8.7 Å) 양 (figure-read ≈) · 본문 *"electrons flow from ZnTe to ZnO … BEF ≈ 0.38 V Å⁻¹"* · `Fig. 11c` (실독) 1 C: PP ≈ 740 → 350 (500 사이클) · ZnO/C@PP ≈ 870 → 525 · ZnO NW/C@PP ≈ 990 → 575 · ZnO NW/ZnTe-ZnO/C@PP ≈ 1040 → 540 (**1000 사이클** — 대조군은 500 사이클까지만) (figure-read ≈).
  - C-Fe₂O₃-G: 오목 나노큐브의 고지수면 · `Fig. 11d` (실독) C-Fe₂O₃ 의 두 고지수면 –Li₂S 모델은 'Fast', P-Fe₂O₃ 의 저지수면 모델 (그림 라벨 'Fe₂O₃(0112)-Li₂S', 막대 표기는 해상도상 판독 불가) 은 'Slow' (Li₂S → LiS + Li).
  - H-Fe-Ce NPs: Fe₂O₃ (113)·(104) + CeO₂ 이종에피택시 · `Fig. 11e1/e2` (실독) Fe 2p (Fe³⁺·Fe²⁺·위성) · Ce 3d (µ·ν 피크) — 그림의 시료는 **L-Fe · L-Fe-Ce · H-Fe · H-Fe-Ce NPs** (Li₂Sₓ 노출 전) 인데 캡션은 *"L−Fe−Ce/C−Li₂Sₓ … H−Fe−Ce/C−Li₂Sₓ"* 를 말한다 · `Fig. 11f` (실독) UV–vis 흡광 (%) — **맨 Li₂Sₓ 가 300 – ≈ 550 nm 에서 100 % 로 포화** (figure-read ≈) → 흡착량 정량에는 쓸 수 없다 (희석 없이 포화된 기준선).
  - 경고: *"the long-term stability of these high-surface-energy facets … warrants further investigation to prevent facet reconstruction."*
- **3.4.2 형상 제어·배향 성장**:
  - CF@ICOF: 생체 이온채널 모사 · 키토산 (CS) + 셀룰로오스 섬유 (CF) + 이온성 COF · AA 적층 → (100) 배향 · `Fig. 12a` (실독) PP vs CF@ICOF (덴드라이트·셔틀) · `Fig. 12b` (실독) 정전 반발 → 정전 인력 → 수소결합 → π–π 적층 (100) 의 4 단계 조립 · **2.6 nm 채널** · 크기 배제 + 정전 반발 · Li⁺ 이동 장벽 0.715 kcal mol⁻¹ (§3d 검산) · 선택도 275.97 · σ 2.186 mS cm⁻¹ · 고적재 희박 800 사이클 92.73 % · 파우치 440.98 Wh kg⁻¹ (웨어러블 디스플레이 구동).
  - ANF/β-FeOOH@PP: 아라미드 나노섬유의 피브린 모사 템플릿 → β-FeOOH 나노선 축 배향 · `Fig. 12c` (실독) XRD 0 · 3 · 6 · 12 · 24 h — ≈ 20° 넓은 ANF 피크가 줄고 아카가나이트 반사 (30-1)·(21-1)·(41-1)… 가 약하게 · `Fig. 12d` (실독) δ 공식과 세 값 · 본문은 이 둘을 **12c ↔ 12d 뒤바꿔** 가리킨다.
  - TiO-NFs: `Fig. 12e` (실독) Ti 부톡사이드 + H₂O + HF 수열 → TiO₂-NFs ((001)/(101)) → PDA 코팅 → 마그네슘열 환원 → TiO-NFs ((001)/(110)) · **`Fig. 12f` (실독) 흡착에너지 'E_a' 막대 (§3d)** — 캡션은 *"differential charge densities … confirm the highest chemical adsorption capacity of TiO (001)"* 인데 패널은 전하차밀도가 아니라 **흡착에너지 막대**고, 본문 *"(001) facet lowers the Li₂S decomposition barrier via strong electronic interactions (Figure 12f)"* 의 '분해 장벽' 도 이 패널에 없다. 그리고 **Li₂S 는 TiO₂(101) (−4.84) 가 TiO(001) (−3.88) 보다 세게 잡는다** — '(001) 이 가장 강하다' 는 S₈ ~ Li₂S₂ 에서만 참.

### 5.9 §4.1–4.3 다차원 · 엔트로피 · 동적 (`Fig. 13` · `Fig. 14` · `Fig. 15`)

- **4.1 다차원 설계** — 단일 변수에서 격자·결함·상·전자구조 여러 자유도의 동시 설계로.
  - δ-Bi₂O₃-Ov/Bi@CNFs: 리그닌 탄소나노섬유 + 열구동 환원 → δ-Bi₂O₃ 의 방사 구배 상전이 + Ov + Bi 금속 이종접합 → Bi 6p 오비탈·p-band center 조절 · `Fig. 13a` (실독) 전기방사 20 kV · 1.0 mL h⁻¹ · 수열 150 °C 8 h · 방사–축 정렬 이종계면.
  - Fe₃N/Fe-NC: 별 모양 끝의 곡률 → 전자 전달 · Fe⁰/Fe²⁺/Fe³⁺ 다가 · *"triggering electron tunneling from the 3d orbitals towards the nucleus"* (물리적으로 뜻이 서지 않는 표현) · `Fig. 13b1–b3` · `Fig. 13c` (실독) 오비탈 채움 도식 + 'BARRIER — a shortcut for electron tunneling' 만화 — **계산값 0**.
  - 단서: *"scalability and cost-effectiveness … warrant further investigation."*
- **4.2 성분 엔트로피 공학** — 엔트로피 안정 · 심한 격자 왜곡 · 느린 확산 · '칵테일' 효과.
  - MS-HEO (Mn·Mg·Ni·Cu·Zn 암염, Fm-3m, S_config ≥ 1.5 R): `Fig. 14a1` (실독 · 확대) 850 °C XRD — 본문 *"confirm the single-phase nature of HEO"* 인데 **HEO 곡선에도 불순물 '*' 표시가 둘** (≈ 31.7° · ≈ 38.9°, figure-read ≈) · 암염 (Fm-3m) 에서 금지된 **(310)** 라벨 · `Fig. 14a2` (실독) 대칭셀 Nyquist (HEO 반원 ≈ 90–100 Ω · AC 가장 큼) · `Fig. 14a3` (실독) Tafel 막대 — 환원 I / 환원 II / 산화: MS-HEO 29 / 28 / **13** · MS-MEO 34 / 32 / 42 · MS-LEO 47 / 113 / 49 · Celgard 48 / **201** / 45 mV dec⁻¹ (인쇄값). 13 mV dec⁻¹ 는 2.303RT/F (≈ 59 mV dec⁻¹, 25 °C) 의 ≈ 1/4.5 — 다전자 선행 평형을 가정해야 나오는 값인데 해석이 없다. 저적재 코팅 (< 0.3 mg cm⁻²) 이 양극 첨가 (≥ 10 wt%) 의 에너지밀도 손실을 피한다는 논리는 설계 원리 ⑤ 와 이어진다.
  - HEO850: `Fig. 14b` (실독) Ni·Co·Mg·Cr·Mn·Zn + PVP/BPY → 80 °C 24 h MOF → 850 °C 10 h → HEO850 · **S/KB 양극** 에 들어간 사례 (표시 없음) · 본문은 HEO850 의 CV 피크를 *"(Figure 14a3)"* 로 가리키는데 그 패널은 MS-HEO 들의 Tafel 막대다.
  - SA-Fe/HEO@NC: `Fig. 14c` (실독) Cu·Zn·Al·Ce·Zr 2D HEO 위 Fe 원자 · 용매화 Li⁺ 가 층을 지나며 탈용매 · `Fig. 14d1` (실독) t_Li⁺ 0.60 / 0.40 / 0.36 (전류 감쇠 2000 s) · `Fig. 14d2` 대칭셀 CV 피크 0.171 · 0.451 · −0.173 · −0.454 V.
  - HEA@HC: `Fig. 14e` (실독 · 확대) Cu₃Pt (JCPDS 65-3247) — 주 피크가 figure-read ≈ 41.4° · 48.2° (축 눈금 판독 ±0.5°) 로 보여 본문 43.4° · 50.6° 와 ≈ 2° 어긋나 보인다 (원전 확인 전) · **양극 촉매** (표시 없음).
  - 고엔트로피 스피넬 음극 (M₃O₄) 은 *"a mechanistic analog"* 로 표시 — 첫 리튬화 투영면적 +41 % ≈ 부피 +68 % · 균열 없음 → 고엔트로피 코팅이 초기 스피넬상 회복으로 무결성을 지킬 수 있다는 **외삽**.
- **4.3 동적 결정공학** — 정적 최적 구조를 미리 정하는 대신 전위·Li⁺ 농도에 실시간 응답하는 재료.
  - TNO 'Li⁺ 호흡': Li⁺ 삽입 → NbO₆ 왜곡 → 격자 산소 활성화 · 반결합 오비탈 점유 조절 → S–S 활성화 · `Fig. 15a` (실독) 전위 독립 단방향 촉매 (TMO: 강한 상호작용 → 느린 전환 → 표면 패시베이션) vs 전위 의존 캐스케이드 (Li₀TNO 강 → Li₀.₅TNO 중 → Li₁.₀TNO '적당' → 빠른 전환) · 범례 오타 'Week' · `Fig. 15b` (실독) 단계 A 2.60–2.15 V (S₈→Li₂S₆ · TNO→LiₐTNO) · B 2.15–1.95 V (Li₂S₆→Li₂S₂) · C 1.95–1.70 V (Li₂S₂→Li₂S).
  - Fe₂O₃ → Li₃Fe₂S₄: 방전 중 V_O 를 S 가 채워 중간상 Li₃Fe₂S₄ 형성 → 더 리튬화되면 Fe₂O₃ 로 복귀 · d-band 상향 → ***"the working-state catalyst may be entirely different from the initial-state catalyst"*** — 이 리뷰의 핵심 문장.
  - PW@g-C₃N₄/rGO: PW 클러스터의 O 가 LiPS 의 Li 를 잡는 '격자 정합' · g-C₃N₄ 의 일시적 N–Li 결합 · `Fig. 15c` (실독) 정합률 96.2 · 95.3 · 97.1 % · 160 °C 열안정.
  - 정리: 정적 결정공학 = '반응 전 정보에 근거한 사전 설정' · 동적 = '반응과 함께 진화' · 단서: *"long-term reversibility … and their impact on the overall energy efficiency … warrant further investigation."*

### 5.10 §4.4 결정공학 코팅의 장기 구조 진화 — 이 리뷰의 중심 (그림 없음)

- 출발: 위 전략은 전부 **준안정이거나 일부러 불안정하게 만든 구조적 특징** (공공 · 변형 · 고지수면 · 배향 채널 · 엔트로피 단일상 · 재구성 자리) 에 기댄다 → 장기 사이클의 화학·전기화학·기계 응력 아래 진화한다. 근거: Li–S 전기촉매의 in situ 재구성 리뷰 [165] (질화물 · 산화물 · 셀렌화물 · 불화물 · 금속/합금 · 황화물 전부).
- ⇒ *"the structural features deliberately introduced … define the initial state of the coating, but they do not necessarily define its working state."* → 동적 결정공학 (§4.3) 은 정적 전략의 대안이 아니라 **필수 보완** — 재구성 경로를 '활성 종점' 으로 유도해야 한다.
- 전략별 진화 위험 분류 (리뷰 본문 그대로):

| 전략 | 진화 경로 | 결과 |
|---|---|---|
| 결함 (§3.1) | 공공 자가 회복 · 원자가 분포 요동 | 공공 농도에 묶인 흡착·촉매 활성이 깎인다 |
| 상·변형 (§3.3) | 변형 이완 · 평형상으로 회귀 | d-band 상향 같은 전자구조 이점 소실 |
| 고지수면 (§3.4.1) | 저에너지·저활성 면으로 재구성 | 활성 자리 소멸 |
| 배향·형상 (§3.4.2) | 반복 팽창·수축에 정렬 구조 붕괴 | 이온 선택성 소실 |
| 엔트로피 (§4.2) | **부분 예외** — 높은 S_config 가 상분해에 저항 · 단일상 가역 회복 | 조성 복잡성은 별개의 문제 |
| 다차원 (§4.1) | 각 차원 모두 유지해야 함 | 하나만 무너져도 전체 실패 |
| 동적 (§4.3) | 재구성이 가역으로 남는가, 비활성 종점으로 표류하는가 | — |

- 직접 증거는 **다른 반응계** (산성 OER Co₃O₄ [166]): 저지수 {110}·{100}·{211} 용해 · 고지수 {311}·{402} 출현 · **가장 불안정한 면의 식각이 인접한 가장 활성·가장 내구 면의 용해를 가속** → 활성 면과 내구 면이 분리 → 활성–내구 trade-off.
- 둘째 쟁점 — **분리막 안정성과 양극 열화가 문헌에서 뒤섞인다**: 용량 감쇠 = 양극 황 손실·고립 + 도전망 열화 + Li 음극 열화 + 전해질 고갈 + (따로) 코팅 진화 · 셀 수준 지표만으로는 분리막 탓을 할 수 없다. 이를 가르는 방법:
  - **대칭 Li₂S–S 셀** [167] (하나는 선리튬화된 같은 C/S 양극 둘) — 양극·분리막·전해질·Li 음극 열화를 구분 · 일반 셀에선 Li 상대전극의 SEI 재형성이 전해질·LiPS 를 소모해 평가를 흐린다.
  - **분리막 지지층 분리 실험** [168] — 분리막 위 정렬 메조탄소 (OMC) 층 · operando SAXS + EDX · 양극에는 KB 만 (황 0) 두고 분리막 층에 S 70 wt% → 분리막 층이 반응 자리임을 분리해 보임.
- 결론: *"at present, the field largely infers separator stability from cycle life, which … is an unreliable proxy."*

### 5.11 §4.5 계속 변하는 전해질 속의 결정공학 분리막 (+ `Table 1`)

- 설계 표적 (결함 농도 · d-band 위치 · 결정면 노출 · 이온 선택성) 은 **정해진 상태의 재료**에 대해 정의된다 — 암묵적으로 환경이 일정하다고 가정. 그러나 LiPS 용해는 Li–S 화학 자체에 내재 → 전해질은 **LiPS 농도 · 점도 · 이온전도 · Li⁺ 용매화 · Lewis 산염기성** 이 SOC 와 사이클 수에 따라 계속 변하는 매질이 된다.
  - 증거: SI 소급 operando XANES 로 **양 전극의 용존 LiPS 절대정량** [169] (충전 중 음극→양극 이동 억제 → 음극 쪽 누적 → 용량 감쇠 원인) · DME/DOL vs 희박 용매화 HME/DME 의 σ·점도 (신선 vs PS 포화) [170] · 용매화력에 따른 전해질 분류 (고·희박·약 용매화) [171] · 불소화 에테르 희석제 [172].
  - ***"a separator coating characterized only in pristine electrolyte is characterized in a medium that the cell leaves behind within the first cycle."***
- 분리막에 직접 걸리는 세 성질:
  1. **이온 수송** — LiPS 축적 → 점도 ↑ · Li⁺ 종분화·용매화 껍질 변화 → 벌크 σ ↓ 경향 + 기공 안 흡착·침전 → 통로 축소 ⇒ 코팅의 유효 이온 전도는 *"not a fixed material constant"*. ⚠ 같은 절 앞에서 [170] 을 *"ionic conductivity increases drastically over the state of (dis)charge"* 로 옮겼다 — 부호가 반대인 두 서술이 정리 없이 공존 (§10-⑰).
  2. **젖음** — 접촉각이 기공 함침을 정하는데 LiPS 농도에 따라 표면장력·극성이 변함 → 신선 전해질에서의 젖음이 유지된다는 보장 없음 · **LiPS 농도 함수의 접촉각·전해질 흡수 데이터는 문헌에 없다**.
  3. **촉매 활성** — 반대 방향 두 효과: 자리가 계속 접근 가능해야 하는데, 높은 농도의 바로 그 기질이 자리를 점유·차단·재구성한다 · **너무 강한 M–S 결합 → 탈착 장벽 → 피독** [173] ⇒ 흡착 세기와 피독 저항은 **경쟁** 성질.
- 하나의 설계 원리 — **최적점은 최대가 아니라 균형점** — 세 길이 척도에서:
  - 거시: 폴리머 코팅 40–400 nm — 가장 두꺼운 것이 자가방전 (LiPS 차단) 최선, 가장 얇은 것이 율속·수명 (이온 수송) 최선 [174] ⇒ 차단과 전도는 경쟁.
  - 원자: 활성 vs 피독 저항 (SAC) [173].
  - 메조: 활성 vs 내구 (결정면 진화) [166].
- 보고 관행 비판: 끝점 용량 유지율은 *"a terminal, aggregated metric"* — 같은 유지율의 두 분리막이 전혀 다른 궤적일 수 있다 (하나는 기능 유지·감쇠는 다른 곳, 하나는 막힘·재구성으로 기능 상실).
- **처방 4 가지** (분리막 고유 서술자):
  1. 사이클 도중 주기적으로 **대칭셀 EIS** 로 분리막 이온 전도 측정 — 가능하면 **LiPS 농도를 통제한 전해질**에서.
  2. LiPS 농도를 바꾼 전해질에서 **접촉각 · 전해질 흡수**.
  3. LiPS 농도 · 사이클 수를 바꿔 **CV · 대칭셀** 로 촉매 활성 추적.
  4. 장기 사이클 후 코팅의 형상 · 화학상태 · 기공 구조 post-mortem / operando.
  ⇒ 이온 전도 · LiPS 차단 · t_Li⁺ 를 **전해질 조성과 사이클 수의 함수로** — *"constitute the evidence base that is currently missing."*
- `Table 1` (§3c) 은 이 주장을 숫자로 받친다: 미보고가 지배적이고, 보고된 값도 셀 구성이 달라 행끼리 비교할 수 없다 → *"The absence of a shared protocol — rather than any deficiency of individual materials — thus emerges as a central impediment to cross-study comparison."*

### 5.12 §5 특성분석 · 계산법 (`Fig. 16`)

- 5.1 기법 일람: XRD (상 · 격자상수 · 단 *"cannot explicitly distinguish cubic Li₂S₃ from other possible solid intermediate products"*) · STEM-EDS · HAADF (Z 대비) · XAFS (XANES = 원자가·전자구조 · EXAFS = 결합길이·배위수) · XPS · Raman (D/G · 응력 · 상전이) · EPR · FTIR · SAED (결정 방위·노출면) · SEM/TEM/HRTEM · Debye–Scherrer 고리 (고에너지 XRD 로 격자 수축·팽창) · operando XRD/XAS 권고.
  - `Fig. 16a` (실독) Rietveld (Rp 2.7 % · Rwp 3.5 % · χ² 2.92) · `Fig. 16c` HAADF 0.539 nm [010] — 둘 다 **Na 이온 고엔트로피 층상 양극** (Na₀.₉₅LNCFM) · `Fig. 16b` CoSe₂ 방전산물 STEM-EDS (Co · Se · S) — 본문은 [35] 인데 캡션은 (a)–(c) 를 모두 [176] 으로 묶는다.
  - `Fig. 16d1/d2` (실독) **계산** XANES (박사논문 [69]): S₈ 주 피크 ≈ 2472 eV · Li₂S 결정은 ≈ 2474–2477 eV 쪽 다중 피크 · Li₂S₃ 분자는 ≈ 2467 eV 전단 피크 (말단 S_T) · 입방 Li₂S₃ 결정은 ≈ 2471 eV 작은 피크 + ≈ 2479 eV 주 피크 (figure-read ≈). 본문 설명 *"the reduction in sulfur valence (0 to −2) still requires higher energy to excite core electrons … Consequently, the absorption edge of Li₂S shifts noticeably to higher energies"* 은 인과가 뒤엉켰다 (§10-⑯).
  - `Fig. 16e` (실독) hBNN → hBNN-PEO → hBNN-PEO-LA FTIR — **흡유 스펀지** 논문 [182].
  - `Fig. 16f–h` (실독) 탄화 MF SEM (200 µm) · MoS₂@CF-NRGO TEM (500 nm) · HRTEM 2–7 층 · 층간 0.67–0.68 nm — **이 절에서 유일한 분리막 재료** [39].
  - *"EPR can quantitatively detect surface oxygen vacancies, XPS can quantify bulk oxygen vacancies"* — 탐지 깊이가 뒤바뀌었다 (§10-⑮).
- 5.2 계산법: §4 참조 (DFT-D3 1 례 · PBE · HSE06 · AIMD 일반론 · 인용 역할 불일치 [186] [188]).
- 맺음: 특성분석 = 현상 발견·확인 · 계산 (DFT · AIMD) = 기구 설명·예측.

### 5.13 §6 결론 · 전망 (`Fig. 17`)

- 요약: Li₂S 의 고유 전자구조가 느린 반응·셔틀을 *"dictated"* 한다 → 결정공학이 전자구조 조절 · 계면 전기장으로 *"suppress insoluble LiPS formation"* (용해성의 오기로 보임) · 전도·계면 안정 · 장벽 ↓ 로 셔틀을 근원에서 억제.
- 역할 세 갈래: ① 원자 수준 (결함·도핑 → 표면 전자구조 · d-band) ② 구조 진화 (외부장 상전이 · 내장장 · 결정면 · 배향 성장) ③ 다차원 시너지 (사이클 중 동적 조절).
- 다섯 설계 원리 · 세 난제 · 네 전망 (§2 표) · 그리고 다시: *"a separator that is active only in the pristine state — but degrades as the electrolyte evolves — cannot be relied upon."*
- `Fig. 17` (실독) 'Lattice Leap' 톱니 도식 — 다차원 시너지 (원자 · 계면 · 구조 · 동적 수준) · 검증·기구 ('DFT & AIMD Calculations') · 전망 (Intelligence · Minimalism · Practicality '> 450 Wh kg⁻¹ Long Cycle Life') · 작은 톱니 (셔틀 · 덴드라이트 · 패시베이션) · '저고도 경제' (드론).

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | (a) Li–S 셀 모식 (b) 셔틀 모식 (c) V₂C MXene 구 분리막의 이중 효과 (d) 촉매 크기 ↔ 활성 자리 이용률 | 배경 — 활용 없음 · 캡션 (c,d) 연도 2026 ≠ ref [37] 2023 |
| 2 | 1912–2026 연표: 이론 기초 → 다공 격자 (MOF 1999 · 그래핀 2004) → 에너지 응용 (MXene → SAC → 결함 → 변형 → 동적) · 리뷰 자체 작성 | 없음 · **도구가 놓쳐 손 크롭** · Bragg 법칙 1912 (본문 1913) |
| 3 | Li₂S/Li₂S₂ 전자·포논·탄성: (a) Γ→X 3.398 eV (b) 포논+DOS (c1) Raman ≈ 373 (c2) IR ≈ 320 cm⁻¹ (d) 네 상 밴드 DFT vs DFT-D (e) 흡수계수 (f) LO/TO 인쇄값 (g1,g2) 0·10 GPa 포논 + Li/S PDOS (h1) a(T) (h2) B₀(T) | li2s 트랙 **문헌 방향잡기** (범함수 n/a 라 수치 이식 금지) · ⚠ (f) c-Li₂S LO–TO 80 vs (g1)·본문 131–132 cm⁻¹ · (d–f) 캡션 [55] 은 오인용 (내용은 [57]) |
| 4 | 6 전략 × 3 기능 매트릭스 (●● 지배 · ● 중요 · ○ 부차/위험) · 리뷰 자체 작성 | 정성 지도 — 근거 데이터 없음 · 'Dopingn' 오타 · 머리칸 중복 |
| 5 | (a,b) Sb₂Se₃₋ₓ/rGO 합성 + EPR g = 2.00 (c1,c2) CeO₂(111) d 0.32 nm + V_O 지도 (d) 인장 응력–변형 (e1,e2) TiO₂₋ₓ@NMC (f) SC-Co (g) 양이온 이동 3 기구 (Famprikis 2019) | (g) = SE 교과서 그림 (`famprikis2019_fundamentals_inorganic_sse.md` 원전) · ⚠ g ≈ 2.00 은 rGO 탄소 신호와 겹침 · 캡션 (d) 누락 · 본문 5d/5e 뒤바뀜 |
| 6 | (a) SVO/AB 합성 (b) T-NSCC Li 1s Li–N 56.4 / Li–S 55.3 eV (c) 기능 모식 (d) Fe-ZIF-8 H-cell 10 min–12 h (e) Ni-ZIF-8-C 합성 (f) zeta −25.0 / −10.9 mV · 2D 나노채널 (g) PDOS O p-band center −4.627 → −3.475 eV | p-band center 는 liu2024 와 **이름만 같음** · ⚠ (c) 에 무관한 CE 축 라벨 · (d) 12 h 인데 `Table 1` 은 24 h |
| 7 | (a1) 비대칭 SAC 감쇠율 교차 비교 (C-rate · E/S 혼재 · S ≈ 1 mg cm⁻²) (a2) S₈ → Li₂S 자유에너지 Co–N₄ vs Co–N₃Cl₁ (b,c) M SA/N-Ti₃C₂Tₓ (d) Fe–NSₓC Li₂S 전하차밀도 · 2.18–2.26 Å (e) 3 C 300 사이클 (f) KPW-CR6 구조 | (a2) = **방전 방향 ΔG** (본문의 'Li₂S 분해 장벽' 아님) · 최대 계단 0.78 vs 0.70 eV · (a1) = 리뷰 §4.5 가 비판하는 교차 비교 그 자체 |
| 8 | (a) MWCE MoS₂ J1/A1g Raman 지도 (b) H-/F-Co@NC 띠 도식 2.38 / 1.13 eV (c) Co HCP/FCC 모식 (d) TiN/2H-MoS₂ 합성 (e1–e3) P-CoSe₂/MXene · d-band 상향 · 분리막 | ⚠ 캡션 (b)(c)(d) 가 그림 패널과 한 칸씩 어긋남 · (e3) 캡션 'P-MoSe₂' |
| 9 | (a) La₂Ce₂O₇/rGO 합성 (b1,b2) d(111) 0.324 vs 0.318 nm (c) **ASSB 복합양극 이종 vs 균질 (Cui 2024 *Nat. Energy*)** (d) 이축 변형 d–p 결합 도식 | (c) 는 우리 DEM·ASSB 축 원전 **단서** (litdb 미보유) — 본문은 이 그림을 황 팽창 설명에 잘못 붙임 · (b) +1.9 % 는 '변형' 이 아니라 다른 화합물의 격자상수 |
| 10 | (a) Ti₃C₂@TiO₂ UV 산화 (b) Co-MoS₂/Ti₃C₂Tₓ 5 단계 (c1,c2) MoS₂@NCO · MoS₂-Edge@NCO 전하차밀도 (d) ΔG(RDS) · Li₂S 해리 막대 (e1–e3) CoB/Co–CoP@HNC · BIEF · 스핀 | (d) 는 **홉 수 검산 대상** (§3d) · 0.19 eV 는 MoS₂-Edge@NCO 값 · 기저면 결합은 해리를 ≈ 1.55 eV 로 악화 |
| 11 | (a) ZnTe(111)/ZnO(101) 분극장 (불일치 ≈ 5 %) (b) 평면평균 Δρ(z) (c) 1 C 1000 사이클 (d) C-/P-Fe₂O₃ 결정면–Li₂S (e1,e2) Fe 2p · Ce 3d XPS (f) UV–vis 흡광 | ⚠ (b) 부호 규약 미기재 (§10-㉑) · (e) 캡션 시료명 ≠ 그림 라벨 · (f) 맨 Li₂Sₓ 300– ≈ 550 nm **포화** |
| 12 | (a,b) CF@ICOF 분리막 · 4 단계 배향 조립 (c) ANF/β-FeOOH XRD 0–24 h (d) 격자 불일치 δ 5.9 / 2.1 / 1.3 % (e) TiO-NFs 합성 (f) TiO(111) · TiO(001) · TiO₂(101) 흡착에너지 막대 | ⭐ (f) = **흡착 배위수 규율의 교과서 반례** (S₈ −18.45 eV · 구조 비공개) · 본문 12c/12d 뒤바뀜 · (f) 캡션 '전하차밀도' 오기 |
| 13 | (a) δ-Bi₂O₃-Ovs/Bi@CNFs 합성 (b1–b3) Fe₃N/Fe 전자 '터널링' · 끝 효과 (c) d–p 오비탈 채움 도식 | 정량값 없는 도식 — 활용 없음 |
| 14 | (a1) HEO/MEO/LEO XRD (a2) 대칭셀 Nyquist (a3) Tafel 막대 13–201 mV dec⁻¹ (b) HEO850 MOF 경로 (c) SA-Fe/HEO@NC (d1) t_Li⁺ 0.60 / 0.40 / 0.36 (d2) 대칭셀 CV (e) HEA@HC XRD | ⚠ (a1) '단일상' HEO 에도 불순물 '*' 2 개 · 암염에 (310) 라벨 · (e) 피크 위치가 본문과 ≈ 2° 어긋나 보임 (figure-read) |
| 15 | (a) 전위 독립 단방향 vs 전위 의존 캐스케이드 촉매 (Li₀ / Li₀.₅ / Li₁.₀TNO) (b) 단계 A · B · C (2.60–2.15 · 2.15–1.95 · 1.95–1.70 V) (c) PW 클러스터 O ↔ LiPS·Li₂S 의 Li 정합률 96.2 / 95.3 / 97.1 % | **'작동 상태 ≠ 초기 상태'** 의 사례 그림 — 우리 보고량 규율의 외부 예시 |
| 16 | (a) Rietveld (Na 이온 양극) (b) CoSe₂ 방전산물 STEM-EDS (c) HAADF 0.539 nm (d1,d2) **계산** XANES S₈ · Li₂S · Li₂S₃ (박사논문) (e) hBNN FTIR (스펀지) (f–h) MoS₂@CF-NRGO SEM/TEM/HRTEM | 특성분석 절인데 분리막 재료는 (f–h) 뿐 · (b) 출처 [35] ≠ 캡션 [176] |
| 17 | 'Lattice Leap' 톱니 도식 (다차원 시너지 · 검증·기구 · 전망 '> 450 Wh kg⁻¹') · 리뷰 자체 작성 | 활용 없음 |
| Table 1 | 분리막 고유 수송 지표 24 행 (t_Li⁺ · σ · LiPS 차단 · R_ct) + '행 사이 비교 불가' 각주 | ⭐ 미보고 집계 (t_Li⁺ 16 · σ 17 / 24) · 우리 `comparison_group` 규율의 분야판 |

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> **공유 물성값 0.** 계 (액체 전해질 Li–S 분리막 코팅 vs argyrodite SE) · 양 · 측정법이 모두 다르다. 아래는 '같은 줄에 놓지 말아야 하는 이유' 와 방법 교훈이다. 우리 수치는 여기 다시 적지 않는다 (`our_dft_baseline.md` · `canonical_registry.json` 이 정본).

| 항목 | 이 리뷰 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 대상 계 | 액체 전해질 Li–S · PP 위 코팅 (탄소 · MXene · 산화물 · SAC · HEO) | argyrodite 황화물 SE (comp1 · modelc · 도핑 계) | 계가 다르다 → 물성 비교 0 |
| 밴드갭 | Li₂S 3.398 eV · Li₂S₂ 1.010 / 1.814 eV — 범함수 · k · 판독법 n/a (`Fig. 3d` 는 'DFT vs DFT-D' 만) | gap 정본은 fixed-occupations nscf VBM/CBM 고유값만 (DOS-threshold 금지) | 물질이 달라 비교 금지 · 방법 교훈: 4 자리 유효숫자 (3.398) 인데 범함수 미기재 · *"neither electrons nor holes can migrate"* 는 gap → 이동도 비약 (우리 규율: gap 은 'wide-gap' 수준으로만) |
| 탄성 | Li₂S B₀ ≈ 40 GPa (0 K, figure-read) · 독립 C_ij 3 개 (값 n/a) | argyrodite E_VRH (relaxed-ion C_ij) | 물질도 양도 다름 (B vs E) → 비교 금지 |
| 흡착에너지 | TiO(001) S₈ −18.45 eV 등 (인쇄값) · 구조 비공개 · 정의식 n/a | 흡착 기록엔 결합 자리 배위수를 같이 싣는다 (`D-2026-10-05-adsorption-site-coordination`) · SDCP 흡착은 마감 (`sdcp_neutral_closed_2026_08_28.json` — 값 인용 안 함) | 규율 적용 사례 — **"배위 미확인 · 결합 포화 (아마 분해) 에너지"** 로만 읽는다 |
| 장벽 | ICOF Li⁺ 0.031 eV · Li₂S 해리 0.11–1.55 eV | Ea 는 계 간 상대차로만 (1저자 정책 2026-09-18) + 홉 수 검산 한 줄 의무 | 검산 결과 차수 모순 (§3d) — 리뷰의 '빠르다/느리다' 서술을 그대로 옮기지 않는다 |
| 이온 수송 | `Table 1` σ 0.11–3.15 mS cm⁻¹ (분리막 + 액체 전해질 · 측정 셀 혼재) | MLIP-MD σ 는 절대값 인용 금지 | 매질 자체가 다르다 (기공 속 액체 vs 고체 격자) → 비교 0 |
| 서술자 | d-band center 16 회 · p-band center 5 회 (적분 창 n/a) | 평균류 지표는 그림 표시 창과 같은 창으로 계산·인용 (-8..0 eV) | 창이 없으면 재현 불가 · liu2024 S p-band 와 이름만 같음 |
| 상태 정의 | *"working-state catalyst ≠ initial-state catalyst"* (§4.3–4.4) · 스핀 규약 0 줄 | 보고량 카드: 허용 상태가 여럿이면 선택·집계 규칙을 먼저 박는다 | **같은 원리** — 리뷰는 원리를 말하지만 자기 서술자 (흡착·ΔG·스핀) 엔 적용하지 않는다 |

---

## 8. Post-processing ★

- **무엇** (원전들이 한 것 — 리뷰가 옮긴 범위):
  - 밴드 구조 (Γ→X 간접 gap) · 포논 분산 + 원소 투영 포논 DOS · Raman/IR 활성 계산 · Born 유효전하 · 유전상수 · LO–TO 분리 (DFPT 로 보이나 리뷰 미기재) · 준조화 a(T) · B₀(T) · 광학 흡수계수.
  - 전하차밀도 (3D 등치면 · `Fig. 7d` · `Fig. 10c`) · 평면평균 Δρ(z) (`Fig. 11b`) → 내장장 세기 (0.38 V Å⁻¹).
  - d-/p-band center (PDOS 1차 모멘트로 보이나 적분 창 n/a · `Fig. 6g`).
  - SRR 자유에너지 계단 (CHE 형으로 보이나 전위 · 용매 · 엔트로피 보정 n/a · `Fig. 7a2`).
  - Li₂S 해리 장벽 (방법 n/a · NEB 0 회) · 흡착에너지 (정의식 n/a · 부호 '음 = 결합').
  - 격자 불일치 δ 공식 (`Fig. 12d`) · 'lattice matching ratio' (정의 n/a · `Fig. 15c`) · 계산 XANES (정렬법 n/a · `Fig. 16d`) · 스핀 상태.
- **도구**: 코드·후처리 도구 이름 **0 회** (VASP · QE · CASTEP · LOBSTER · pymatgen · VESTA · Materials Studio 전부 없음).
- **수치화·플롯·기록**: 리뷰 자체 정량 그림 0 — 원전 그림 재사용 14장 + 자체 도식 3장 (`Fig. 2` · `Fig. 4` · `Fig. 17`). 자체 정리 수치는 `Table 1` 이 유일하다. 원자료 공개 없음 (*"no datasets were generated"*).
- **우리 규율에 대 보면**: 평균류 지표 (band center) 는 창이 없으면 재현이 안 되고, 흡착에너지는 구조가 없으면 배위수를 못 센다 — 이 리뷰가 옮긴 서술자 대부분이 **재현 불가 상태**로 인용된다.

---

## 9. 적용 인사이트 ★ (우리 작업에)

- ① **큰 |E_ads| 를 보면 '흡착인가 반응인가' 부터 묻는다** — `Fig. 12f` 의 S₈ −18.45 eV 는 S 원자당 ≈ −2.3 eV (8 개 다 결합한다고 가정한 우리 산수) 로 화학결합 규모 그 자체이고, 기판은 과환원된 TiO (Ti²⁺) 다. 고리가 깨져 표면 황화가 일어났을 가능성이 크다 (구조가 없어 확인 불가 · '배위 미확인'). 우리 계면·흡착 계산 (W_ad · B₂O₃ 자리 · Nd 계면) 에서 수 eV 급 값이 나오면 **배위수 + 원자당 정규화 + 최종 구조의 결합 절단 여부**를 같은 줄에 싣는다 — 규율 `D-2026-10-05-adsorption-site-coordination` 의 분야 규모 반례로 쓸 수 있다.
- ② **'초기 상태 ≠ 작동 상태' 는 우리 보고량 규율과 같은 말**이다 — 우리 계면 DFT (B₂O₃ · Nd · Li₂S 계면상) 는 거의 다 초기 (완화된 정적) 구조의 서술자다. 기구 근거로 인용할 때 '어느 상태의 값인가' 를 명시하는 습관 (보고량 카드 §1–3) 에 외부 리뷰 인용 한 줄을 댈 수 있다 (§11 문장 ②).
- ③ **li2s 트랙 — Li₂S 벌크 물리의 방향잡기**: gap (~3.4 eV · 범함수 미상) · ε₀ 7.80 · Z*_S ≈ 1.91 · LO–TO ≈ 130 cm⁻¹ · B₀ ≈ 40 GPa (figure-read) 는 문헌 쪽 '대략 이 정도' 다. 단 같은 그림 안 LO–TO 80 vs 132 cm⁻¹ 불일치처럼 2차 인용이 서로 안 맞는다 → Li₂S 포논·유전 값이 정말 필요해지면 원전 [54] [63] 을 직접 보거나, 3 원자 원시셀이라 우리 기준선에서 직접 내는 쪽이 2차 인용보다 낫다 (제안일 뿐 · 결정 아님 · 계산은 li2s 외부 1저자 트랙의 규칙을 따른다).
- ④ **`Table 1` 각주 형식** — '값 + 측정 셀 구성' 을 한 칸에 묶고 '행 사이 비교 불가' 를 표 머리에 박는 방식은 우리 `comparison_vs_ours.md` 문헌 행 (측정법 · comparison_group 명시) 과 같은 처방이다. 문헌 값을 표로 모을 때 '미보고 수' 를 같이 세는 습관도 가져올 만하다.
- ⑤ **후속 추적 단서 하나**: `Fig. 9c` 의 원전 Cui et al. *Nat. Energy* 9, 1084 (2024) (ASSB 양극 균질화 · zero-strain · 냉간압축 · 부피변화 1.2 %) — 우리 DEM·복합양극 미세구조 축에 닿는데 litdb 에 없다 (§14).

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

### 10a. 과학 내용

1. **계산 조건 0 줄** — d-band (16 회) · p-band (5 회) · 흡착 · ΔG · 해리 장벽 · 스핀 · BEF 어디에도 범함수 · vdW · U · k · 셀 · 스핀 처리 · 용매 · 전위 기준이 없다. §5.2 의 PBE · HSE06 언급은 일반론이고 어느 수치에 붙는지 말하지 않는다.
2. **흡착에너지 −18.45 eV 를 단서 없이 '가장 강한 화학흡착' 으로** (`Fig. 12f`) — S 원자당 ≈ −2.3 eV (우리 산수) · 과환원 TiO 표면 · 구조 비공개 → 흡착이 아니라 분해·황화 반응 에너지일 가능성. 같은 리뷰 §4.5 가 *"excessively strong metal–sulfur interaction … the catalyst is progressively poisoned"* ([173]) 라고 쓰면서 이 값엔 적용하지 않는다. 기호 'E_a' 는 활성화 에너지와 겹친다. Li₂S 는 오히려 TiO₂(101) 이 더 세게 잡는다 (−4.84 vs −3.88 eV).
3. **0.715 kcal mol⁻¹ (0.031 eV) '이동 장벽'** — 298 K 에서 1.2 kT · 평균 대기 0.33 ps (§3d 검산). 활성화 장벽으로 읽을 수 없는 크기이고, 결정면 순위의 근거가 못 된다.
4. **Li₂S 해리 장벽의 차수** (`Fig. 10d`) — 개선값 0.48 eV 와 대조군 0.78–0.88 eV 가 둘 다 1 h 충전 창보다 몇 자릿수 빠르고, 1.11 · 1.55 eV 는 상온에서 사실상 일어나지 않는 값 → 영 바이어스 클러스터 해리라는 **상대 서술자**이지 속도가 아니다. 본문은 0.19 eV 를 결합 전 MoS₂ 나노벨트 값처럼 쓴다 (실제는 MoS₂-Edge@NCO).
5. **Li₂S 물리 서술의 오류·비약** (§2): (a) Born 전하 1.91 은 공칭 2 와 4.5 % 차 — *"notably deviating"* 은 과장이고, 공칭에 가깝다는 것이 이온성의 근거인데 '벗어남 → 이온성' 으로 논리가 뒤집혔다. (b) gap 3.4 eV → *"neither electrons nor holes can migrate"* 는 과대서술 (gap 은 고유 운반자 농도를 정하지 이동 자체를 금하지 않는다 · 폴라론·결함 경로). (c) **Raman** — 반형석 (Fm-3m) 에서 S 는 반전중심 (4a) 이라 Raman 활성 T2g 모드에서 움직이지 않는다 (우리 판단 · 군론). 'S²⁻ Raman 이 약하다' 가 아니라 '1차 Raman 에 S 기여 0' 이고, Li₂S 의 Raman 지문은 원래 그 Li T2g 피크 (`Fig. 3c1` 의 ≈ 373 cm⁻¹) 다 — 'Raman 으로 Li₂S 를 보기 어렵다' 는 결론이 자기 그림과 어긋난다. (d) *"p-band doping strategies"* 로 Li₂S 전도도 향상 — 근거 인용 0. (e) LO–TO 분리 (극성 결정의 일반 현상) → 빛으로 S–S 절단 · 셔틀 근원 억제는 비약.
6. **같은 그림 안 LO–TO 불일치** — c-Li₂S 가 `Fig. 3f` (Peng) 에선 452 − 372 = **80 cm⁻¹**, 본문·`Fig. 3g1` (Saib) 에선 **≈ 131–132 cm⁻¹**. `Fig. 3g1` 의 Γ 가지 (≈ 325 · ≈ 377 · ≈ 456) 와 `Fig. 3c2` IR (≈ 320) 을 보면 TO ≈ 320–325 이고, (f) 의 '372' 는 Raman T2g 가지 (≈ 373–377) 와 맞는다 — (f) 가 T2g 를 TO 로 적었거나 두 원전의 모드 지정이 다르다 (figure-read · 원전 확인 전). 리뷰는 둘을 나란히 싣고 언급하지 않는다.
7. **EPR g = 2.00 의 귀속** (`Fig. 5b`) — 탄소 없는 Sb₂Se₃ 는 무신호, Sb₂Se₃/rGO 에도 신호 → rGO 탄소 라디칼이 같은 g 에 기여. Se 공공 단독 귀속은 유일하지 않다.
8. **'변형' 과 '다른 화합물' 의 혼동** — La₂Ce₂O₇ 의 d(111) 이 CeO₂ 보다 1.9 % 큰 것은 조성이 다른 평형 격자상수 (화학 팽창) 이지 탄성 변형이 아니다. '격자 변형 공학' 절의 대표 사례가 변형을 보여 주지 않는다.
9. **나노유체 표면전하 선택성의 전제** — 1 M LiTFSI/DOL-DME (ε_r ≈ 7) 의 Debye–Hückel λ_D ≈ **0.09 nm** (우리 산수 · 이 농도는 DH 적용 범위 밖이라 차수만) → 'Debye 길이 > 채널 크기' 가 성립하려면 채널이 용매화 Li⁺ 보다 작아야 한다. 게다가 PSN/MXene 의 zeta (−10.9 mV) 가 MXene (−25.0 mV) 보다 **덜 음전하** — 리뷰가 내세운 '음전하 채널의 양이온 선택' 근거와 방향이 반대다 (zeta 측정 매질 미기재).
10. **'단일상' HEO 의 불순물 표시** (`Fig. 14a1`) — HEO 곡선에도 '*' 두 개 · 암염에 금지 반사 (310) 라벨. Tafel 13 mV dec⁻¹ (2.303RT/F 의 ≈ 1/4.5) 은 해석 없이 '빠른 역반응' 근거로 쓰였다.
11. **스스로 비판한 지표로 §3–4 를 채움** — 사례 숫자는 거의 전부 끝점 용량 · %/cycle 이고, `Fig. 7a1` 은 C-rate · E/S 가 섞이고 S ≈ 1 mg cm⁻² 인 교차 비교 차트다. §4.5 의 비판이 §3–4 의 서술 방식에 되먹임되지 않았다.
12. **§3.1 '항상 같은 셀 조건 대조' 단언** — 192 편 전수 확인 근거 없음 · 탄소천 자체가 분리막인 T-NSCC 와 PP 는 같은 셀 구성이 아니다 · SVO/AB 는 '보조 집전체' (양극 기능) 로 일한다고 리뷰 자신이 쓴다 → §4.4 (분리막 열화와 양극 열화의 혼동) 와 긴장.
13. **범위 이탈** — 분리막이 아니거나 위치 미상인데 표시 없는 사례 ≈ 12 건 (1T-MoS₂ host · HEO850 양극 · HEA 양극 촉매 · Zr-LAO 음극 …) + §5 의 Na 이온 양극 · 흡유 스펀지 예시. 몇 건만 스스로 표시했다 (Fe₀.₉₆S · FSI⁻ · Cui · M₃O₄ · Co₃O₄ OER).
14. **인용 역할 불일치·서지 결함** — [186] (Na NASICON 양극) · [188] (Na 층상 HE 리뷰) 를 DFT · AIMD 일반론 근거로 · [191] (불소 없는 압축 용매화 전해질) 을 '유체역학 영감의 구배 비대칭 분리막' 근거로 · `Fig. 3d–f` 캡션 [55] (BiFeO₃ 나노입자) 는 [57] 의 오기 · [63] DOI 가 *"10.1088/2053-1591."* 에서 잘림 · 박사논문 둘 ([69] · [112]) 이 계면 안정 · 고체 LiPS 탄성 · 계산 XANES · 1T-MoS₂ 의 단독 근거.
15. **XPS ↔ EPR 탐지 깊이 뒤바뀜** — *"EPR can quantitatively detect surface oxygen vacancies, XPS can quantify bulk oxygen vacancies"* — XPS 는 수 nm 표면 민감 기법이고 EPR 은 시료 전체의 짝짓지 않은 전자를 본다.
16. **XANES 설명의 인과 혼동** — '0 → −2 환원이 더 높은 에너지를 요구해 Li₂S 흡수단이 높은 쪽으로' 는 화학 이동의 통상 직관과 반대 방향을 그럴듯하게 꾸민 설명이다. S₈ 의 낮은 에너지 흰선은 1s → σ*(S–S) 전이이고 S²⁻ (3p 꽉 참) 엔 그 낮은 빈 준위가 없다는 것이 통상의 읽기다 (우리 판단 · 원전 확인 전). 그림은 박사논문의 **계산** 스펙트럼이고 에너지 정렬법이 없다.
17. **§4.5 안의 부호 긴장** — [170] 을 'σ 가 (방)충전 상태에 따라 *drastically* 증가' 로 옮긴 몇 줄 뒤, 'LiPS 축적은 점도 ↑ · 용매화 변화로 σ 를 낮추는 경향' 이라 쓴다 — 정리 없이 공존 (원전 확인 전).
18. **§2 의 탄성 자기모순** — 고차 → 저차 LiPS 로 갈수록 E · G · B '증가' 라고 쓰고, 같은 단락 끝에서 *"Li₂S, possess low moduli"*.
19. **'10 GPa 까지 안정' 의 무의미** — 분리막 응력 (MPa) 보다 3–4 자릿수 큰 정수압 안정성은 기공 속 Li₂S 의 실패 (파괴 · 박리 · 재용해) 를 말해 주지 않는다.
20. **'Stark 효과' · '전자 터널링이 핵 쪽으로'** — 물리 용어를 정량 근거 없이 은유로 쓴다 (`Fig. 13c` 도 계산값 없는 오비탈 도식).
21. **`Fig. 11b` 부호 규약 미기재** — 통상 규약 (Δρ > 0 = 전자 축적) 으로 읽으면 ZnTe 쪽 축적 · ZnO 쪽 고갈 → 본문 *"electrons flow from ZnTe to ZnO"* 와 반대 방향이 된다 (규약이 반대면 일치 · 판정 보류 · 원전 확인 전).
22. **UV–vis 정량 불가** (`Fig. 11f`) — 맨 Li₂Sₓ 기준선이 300 – ≈ 550 nm 에서 100 % 포화. `Table 1` 의 KPW-CR6 'UV-vis: 417 nm' 는 파장이지 차단 지표가 아니다.

**좋은 점 (공정하게)**: §2.2.1 끝의 '전자 절연 Li₂S 는 전도성 코팅 위에서 핵생성 → 기공 막힘 · 촉매 패시베이션 · 주기 응력' 다리 논증 · §4.4 의 전략별 진화 위험 분류 · §4.5 의 '전해질이 첫 사이클 안에 바뀐다' 논증과 네 가지 분리막 고유 측정 처방 · `Table 1` 의 비교 불가 각주 · 대칭 Li₂S–S 셀과 분리막층 분리 실험을 끌어온 것 · 다섯 설계 원리 (특히 '균형 · 작동 상태 · 질량당 활성').

### 10b. 그림 · 캡션 · 본문 참조 불일치 (실독으로 확인)

| 위치 | 본문 / 캡션의 표기 | 실제 그림 | 판정 |
|---|---|---|---|
| `Fig. 1` 캡션 (c,d) | *"[37] Copyright 2026"* | ref [37] = *Adv. Mater.* 35 (2023) | 연도 오기 |
| `Fig. 2` | Bragg 법칙을 1912 위치에 | 본문은 1913 | 연표 불일치 |
| `Fig. 3` 캡션 (d–f) | *"[55] Copyright 2025, Elsevier"* | [55] = BiFeO₃ (*APL Mater.* 2024) · 내용은 [57] Peng (*Solid State Sci.* 2025) | 인용 번호 오기 |
| `Fig. 3e` 캡션 | *"cubic Li₂S and tetragonal Li₂S₂"* | 범례 세 곡선 (h-Li₂S₂ 포함) | 캡션 누락 |
| `Fig. 3f` vs 본문 | c-Li₂S LO–TO 132 cm⁻¹ (Saib) | (f) 452 / 372 → 80 cm⁻¹ | 모드 지정 불일치 (§10a-6) |
| `Fig. 5` | 캡션: (d) 없음 · 응력–변형을 (e) 로 · *"TiOSb₂Se₃@NMC"* · 본문: 5d = V_O 생성 · 5e = 기계강도 | 그림: (d) = 응력–변형 · (e2) = TiO₂₋ₓ@NMC V_O 도식 | 라벨 어긋남 + 이름 깨짐 |
| `Fig. 5b` 본문 | *"EPR signal of Sb₂Se₃/RGO exhibited a g-value of 2.00"* | 가장 큰 신호는 Sb₂Se₃₋ₓ/rGO · Sb₂Se₃/rGO 는 작음 | 시료 혼동 |
| 본문 §3.2.3 | Fe-NSC@GO 사이클 *"(Figure 6e)"* | 그 그림은 `Fig. 7e` (`Fig. 6e` 는 Ni-ZIF-8-C 합성) | 그림 번호 오기 |
| `Fig. 7a1/a2` 본문 | 7a1 = *"reduced Li₂S decomposition barriers"* · 7a2 = 분리막 코팅 적용 | 7a1 = 감쇠율 교차 비교 · 7a2 = **방전** ΔG 계단 | 패널 대응 어긋남 |
| `Fig. 8` 캡션 | (b) TiN/2H-MoS₂ 합성 · (c) 띠 구조 · (d) Co@NC 모식 [117] | (b) = 띠 도식 · (c) = Co@NC 모식 · (d) = TiN/2H-MoS₂ 합성 · Co@NC 모식 출처는 [118] | 캡션이 한 칸씩 밀림 · 출처 오기 |
| 본문 §3.3.1 | *"(Figure 8b)"* TiN/1T-MoS₂ · *"(Figure 8d)"* VBM–E_F 간격 · *"tin nanospheres"* | 각각 `Fig. 8d` · `Fig. 8b` · TiN | 뒤바뀜 + 오기 |
| `Fig. 8e3` 캡션 · 본문 | *"P-MoSe₂/MXene"* · CoSe₂ 의 *"1T phase"* | 그림·원전은 P-CoSe₂ | 이름 오기 · 상 표기 부적절 |
| `Fig. 9c` 본문 | 황 리튬화 4 단계 · 리튬화 응력 · 48.64 % 완충 [121] | Cui 2024 ASSB 복합양극 탈리튬 미세구조 [123] | 내용 불일치 |
| `Fig. 11e` 캡션 | *"L−Fe−Ce/C−Li₂Sₓ · H−Fe−Ce/C−Li₂Sₓ"* | 라벨: L-Fe · L-Fe-Ce · H-Fe · H-Fe-Ce NPs | 시료명 불일치 |
| 본문 §3.4.2 | *"Theoretical calculations (Figure 12c)"* · *"XRD (Figure 12d)"* | 12c = XRD · 12d = 격자 불일치 계산 | 뒤바뀜 |
| `Fig. 12f` 캡션 · 본문 | 캡션 *"differential charge densities"* · 본문 *"lowers the Li₂S decomposition barrier"* | 패널 = 흡착에너지 'E_a' 막대 | 내용 불일치 |
| 본문 §4.2 | 단일상 HEO *"(Figure 14a1)"* · HEO850 CV 피크 *"(Figure 14a3)"* | 14a1 HEO 에 불순물 '*' 2 · 14a3 = MS-HEO 들의 Tafel 막대 | 내용 불일치 |
| `Fig. 14e` vs 본문 | (111) 43.4° · (200) 50.6° | 주 피크 figure-read ≈ 41.4° · 48.2° (±0.5°) | ≈ 2° 어긋나 보임 (원전 확인 전) |
| `Fig. 16` 캡션 | (a)–(c) 를 모두 [176] 으로 | 본문은 (b) 를 [35] (CoSe₂) 로 | 출처 오기 |
| `Fig. 4` · `Fig. 15` · `Fig. 6c` | — | 'Dopingn' · 'Week' · 무관한 CE 축 라벨 | 도판 위생 |
| §4.5 본문 | `Table 1` *"17 of 24 entries each"* (t_Li⁺ · σ) | t_Li⁺ 미보고 16 · σ 17 | 셈 오류 (사소) |
| §6 결론 | *"suppress insoluble LiPS formation"* | 셔틀의 원인은 **용해성** LiPS | 용어 오기로 보임 |

---

## 11. 인용 가능 문장 (영문 초안)

- ① (리뷰 원문 인용) *"A separator coating characterized only in pristine electrolyte is characterized in a medium that the cell leaves behind within the first cycle."* — *Small*, e76191 (2026).
- ② (리뷰 원문 인용) *"The structural features deliberately introduced by defect, doping, phase/strain, facet, or entropy engineering define the initial state of the coating, but they do not necessarily define its working state."* — *Small*, e76191 (2026). → 우리 '보고량은 상태를 선언한다' 규율의 외부 인용 후보.
- ③ (우리 서술 · 리뷰 표에서 센 값) *"In a recent compilation of 24 modified Li–S separators, only 8 reported a Li⁺ transference number and 7 an ionic conductivity, and the reported values were obtained in non-equivalent cell configurations [Small, e76191 (2026)]."* — 셈은 우리 것 (§3c) 이라 '리뷰가 말했다' 로 쓰지 않는다.
- ④ (방법 교훈 · 우리 서술) *"Adsorption energies of several electron-volts on reduced oxide surfaces should be reported together with the coordination of the binding site, because values of that magnitude can reflect bond saturation or decomposition rather than adsorption."* — 이 리뷰는 **반례**로만 인용하고 리뷰가 그렇게 말했다고 쓰지 않는다.
- ⑤ (리뷰 원문 인용) *"Capacity retention is a terminal, aggregated metric."* — 짧은 표어로 쓸 때.

---

## 12. 주의 / 한계 (인용 규율)

- **전부 리뷰 재인용 (원전 확인 전)** — 셀 성능 · DFT 수치 모두. 원전을 보기 전에 숫자를 옮기지 않는다.
- **우리 db 절대값과 같은 표에 넣지 않는다** — 계 · 매질 · 양이 다르다 (CLAUDE.md §litdb).
- `Fig. 12f` 흡착에너지는 **'흡착 세기' 로 인용 금지** — 쓸 일이 있으면 "배위 미확인 · 결합 포화 (아마 분해) 에너지" 단서를 같이 단다.
- Li₂S 값 (gap · ε₀ · Z* · LO–TO · B₀) 은 범함수 미상 · 2차 인용끼리 불일치 → li2s 트랙 문서에 넣을 때는 **원전 [54] [57] [63] 확인 후**, '문헌 방향잡기' 로만.
- 장벽 값을 옮길 때는 §3d 의 홉 수 검산 줄을 같이 싣는다 (`D-2026-09-27-barrier-hop-count`).
- `figure-read ≈` 값은 저해상도 재사용 그림의 눈금 판독이다 (±수 %). `figure-read (인쇄값)` 은 라벨 글자라 정확하지만, `Fig. 7a2` 처럼 흐린 숫자는 누적합 대조로 판독했다 (0.69).
- 사례 위치 분류 (§3e) · 참고문헌 연도 집계는 **우리 분류·자동 집계 (±2 · ±수 편)**.
- 이 리뷰는 *Small* 2026 게재본 (VoR) 이다 — 판본 문제는 없다. 단 OA 가 아니라 원문 재배포 불가.

---

## 13. 기법 용어 미니사전

| 용어 | 뜻 (이 리뷰 맥락) |
|---|---|
| LiPS (Li₂Sₓ, x = 4–8) | 고차 폴리설파이드 — 에테르 전해질에 녹아 양·음극 사이를 오간다 (셔틀) |
| 셔틀 효과 | 용해 LiPS 가 음극으로 가서 Li 와 반응 → 활물질 손실 · CE 저하 · Li 부식 |
| SRR | sulfur reduction reaction — 방전 방향 S₈ → Li₂S 다단계 환원 |
| E/S 비 (µL mg⁻¹) | 황 질량당 전해질 부피 — 작을수록 '희박 전해질' (실용 조건) |
| %/cycle 감쇠 | (초기 − 최종)/초기 ÷ 사이클 수 — 리뷰 §4.5 가 '끝점 지표' 라 비판한 바로 그 수 |
| H-cell 투과 시험 | 두 칸 사이에 분리막을 끼우고 LiPS 색이 넘어오는 시간을 보는 정성 시험 |
| t_Li⁺ (Li⁺ 전달수) | 전류 중 Li⁺ 가 나르는 몫 — 보통 Bruce–Vincent (정전압 분극 전후 전류·임피던스) |
| 대칭 Li₂S₆ 셀 | 같은 전극 둘 + Li₂S₆ 전해질 — CV 로 LiPS 산화환원 촉매 활성을 본다 |
| 대칭 Li₂S–S 셀 | 하나는 선리튬화된 같은 C/S 양극 둘 — Li 음극 없이 양극·분리막·전해질 열화를 가른다 ([167]) |
| d-band center | 전이금속 d 상태 밀도의 에너지 1차 모멘트 — E_F 에 가까울수록 흡착 강화 (Hammer–Nørskov) |
| p-band center | 같은 개념의 p 상태 판 (O · S · Bi 6p) — 적분 창에 민감 |
| Sabatier 원리 | 흡착이 너무 약해도 (못 잡음) 너무 강해도 (못 놓음) 촉매가 나쁘다 → 화산형 |
| BIEF / BEF | built-in electric field — 이종접합 계면의 페르미 준위 정렬로 생기는 내장 전기장 |
| Schottky 접합 | 금속–반도체 접합의 정류 장벽 — 내장장으로 전하 분리 |
| LO–TO 분리 | 극성 결정에서 Γ 점 광학 포논이 거시 전기장 때문에 종파 (LO) > 횡파 (TO) 로 갈라지는 현상 |
| Born 유효전하 Z* | 원자 변위에 대한 분극 응답 — 공칭 이온 전하에 가까우면 이온 결합성 |
| T2g / T1u (반형석) | Fm-3m Li₂S 의 Γ 광학 모드 — T2g Raman 활성 (Li 만 움직임) · T1u IR 활성 (LO/TO 로 갈라짐) |
| EPR g ≈ 2.00 | 자유전자에 가까운 g — 공공에 갇힌 전자 · 탄소 라디칼 모두 이 근처라 귀속 주의 |
| HEO · S_config | 고엔트로피 산화물 · 배열 엔트로피 (≥ 1.5 R 를 '고엔트로피' 기준으로 흔히 씀 · 5 성분 등몰이면 R ln 5 ≈ 1.61 R) |
| SAC | single-atom catalyst — M–N₄ 같은 원자 분산 금속 자리 |
| REV | relative electronegativity value — 비대칭 배위 SAC 에서 치환 원자와 N 의 전기음성도 차 ([105]) |
| MXene | Ti₃C₂Tₓ · V₂C 같은 2D 전이금속 탄화물 (MAX 상 식각) |
| MOF / ZIF / COF / POM | 금속유기골격 · 제올라이트형 이미다졸 골격 · 공유유기골격 · 폴리옥소메탈레이트 |
| zero-strain | 충방전 부피변화 < 1 % 재료 — 장수명의 열쇠로 제시 |
| Tafel 기울기 | 과전압 vs log 전류 기울기 — 2.303RT/(αF) · 25 °C 에서 α = 1 이면 ≈ 59 mV dec⁻¹ |
| Debye 길이 · EDL 중첩 | 전해질의 전하 차폐 길이 — 채널보다 길면 벽 전하가 채널 전체를 지배 (농도 높으면 매우 짧다) |
| XANES / EXAFS | X선 흡수단 근처 (원자가·전자구조) / 흡수단 위 진동 (결합길이·배위수) |
| 홉 수 검산 | Γ = ν₀·exp(−Ea/kT) 로 장벽이 서술 ('빠르다/느리다') 과 차수에서 맞는지 보는 우리 규율 |

---

## 14. 후속 추적 참고문헌 (우선순위)

1. **[123]** L. Cui, S. Zhang, J. Ju *et al.*, "A Cathode Homogenization Strategy for Enabling Long-cycle-life all-solid-state Lithium Batteries," *Nat. Energy* 9, 1084 (2024) — ASSB 양극 균질화 · zero-strain 1.2 % · `Fig. 9c` 원전 → **우리 DEM·복합양극 미세구조 축에 직접**. litdb 미보유.
2. **[54]** C.-L. Jiang *et al.*, *Phys. Chem. Chem. Phys.* 25, 6362 (2023) · **[63]** S. Saib & N. Bouarissa, *Mater. Res. Express* 4, 105901 (2017) (DOI 잘림) · **[57]** Y.-F. Peng *et al.*, *Solid State Sci.* (2025) 108021 — Li₂S 밴드 · 포논 · 탄성 원전 → li2s 트랙이 Li₂S 벌크 값을 필요로 할 때만 (범함수 · LO–TO 불일치 해소).
3. **[173]** C. Li *et al.*, "Atomic Insights into the S Poisoning Effects of Single-Atom Catalysts in Li–S Batteries," *ACS Omega* 8, 45348 (2023) — 흡착 세기 ↔ 피독 (Sabatier) 의 계산 근거 → 흡착 규율의 '강할수록 좋다가 아니다' 쪽 원전.
4. **[143]** X. Wu *et al.*, *J. Mater. Chem. A* 14, 13411 (2026) — `Fig. 12f` −18.45 eV 의 원전 → 구조가 공개돼 있으면 **배위수 감사 후보** (yuan2026 SiO₂–TFSI⁻ 감사와 같은 절차).
5. **[167]** M. Piwko *et al.*, *J. Electrochem. Soc.* 165, A1084 (2018) — 대칭 Li₂S–S 셀 · **[169]** C. Zech *et al.*, *J. Mater. Chem. A* 9, 10231 (2021) — SI 소급 operando XANES 용존 LiPS 정량 → 측정 프로토콜 참고 (우리 계산과 직접 연결은 약함).
6. **[165]** P. Zeng *et al.*, *Adv. Funct. Mater.* 33, 2301743 (2023) — Li–S 전기촉매 in situ 재구성 리뷰 → '초기 ≠ 작동 상태' 의 원전 묶음.
7. **[84]** Famprikis *et al.*, *Nat. Mater.* 18, 1278 (2019) — 이미 litdb (`famprikis2019_fundamentals_inorganic_sse.md`).
