<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-06 초판 (litdb-curator) — 사용자 질문: "sdcp랑 유사한데 요건 어케 진행됐는지".
     본문 11 pp + SI 43 pp 정독 · 크롭 44장 (자동 42 + 손 2: Fig. S27 · Table S1) 중 그림 20장 + 표 1 실독
     (본문 그림 5 전부 + SI 그림 15 + Table S1 썸네일) + 패널 확대 렌더 4회 (Fig. 2j 두 조각 · 2f · 4n) — §13.
     ⚠ 액체 전해질 LIB (LFP 반쪽셀 · MCMB 풀셀) — 황화물 ASSB 아님 · 물성 4축 A–D 에 수치로 넣지 않는다.
     ⚠ 우리 SDCP 흡착값은 citable false — 이 문서에 우리 숫자를 싣지 않는다 (마감 파일 3개의 금지 서술). -->

# Enabling ultra-high-loading LiFePO₄ cathodes via a conductive binder architecture with minimized inactive content — Noh, Oh, Kang et al. (*Energy Storage Mater.* **2026**, 86, 104987)

> slug `noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp` · DOI `10.1016/j.ensm.2026.104987` · *Energy Storage Mater.* **86 (2026) 104987** · type `exp (binder · electrode · electrochemistry) + DFT adsorption (CASTEP interaction energy, 7 bars)` · 접수 2025-12-22 · 개정 2026-02-04 · 수락 2026-02-12 · 온라인 2026-02-14 · © 2026 Elsevier B.V. (OA 아님) · PDF `litdb/inbox/70. Enabling ultra-high-loading LiFePO4 cathodes via a conductive binder architecture with minimized inactive content.pdf` (본문 11 pp) + `litdb/inbox/70. Sup) Enabling ultra-high-loading LiFePO4 cathodes via a conductive binder architecture with minimized inactive content.pdf` (SI 43 pp — DFT 방법 2 pp · Fig. S1–S38 · Table S1) · digested `2026-11-06` · status ✅ · 태그 **[외부]**

> elements: Li, Fe, P, O, S, C, H, F
> methods: DFT

<!-- 태그 근거: elements — LiFePO4 (Li/Fe/P/O) · PEDOT:PSS·PEG (C/H/O/S) · PVDF (C/H/F) · SWCNT (C) · 전해질 LiPF6 (Li/P/F).
     methods — 계산은 DFT 하나뿐 (CASTEP interaction energy 7점). AIMD·MD·MLIP·NEB·DOS·Bader·COHP 0건 · XPS·Raman 0건
     (GIWAXS·EIS·CV·SAICAS·TMA 는 목록 어휘에 없다). -->

> **저자**: Eun Hwan Noh¹ · Seongeun Oh² · Hyeri Kang³ (**공동 1저자 3인**) · Miseung Kim¹ · Jee Ho Ha¹ · Ho-Jeong Ji¹ · Won-Jin Kwak¹ · **Eunji Lee³\*** · **Se Hun Joo²·⁴\*** · **Seok Ju Kang¹·⁵\*** — ¹UNIST 에너지공학과 · ²숙명여대 화공생명공학부 · ³GIST 신소재공학부 · ⁴숙명여대 Institute of Advanced Materials and Systems · ⁵UNIST InnoCORE AI-Space Solar Initiative. 연구비 NRF (RS-2025-16064954) · UNIST 2025 Research Fund (1.250009.01) · InnoCORE (1.250021.01). **Data availability: "Data will be made available on request"** (구조 파일·원자료 비공개).
> ⚠ CRediT 에 **계산(DFT)·software 역할 표기가 없다** — 누가 계산했는지 문서로 확인 불가 (3 기관 공동 1저자 구조라 숙명여대 Joo 그룹 계산 · GIST Lee 그룹 GIWAXS 분석으로 보이지만 **추정일 뿐**).
>
> **계보**: 참고문헌 [35] **Kong … S. J. Kang**, *Energy Storage Mater.* **64** (2024) 103074 (같은 교신 그룹) — PEDOT:PSS/PEG 바인더를 **Si 음극**에 썼고 PEG 비 **1/0.3** 을 그때 정했다 → **본 논문** = 같은 바인더를 부피변화가 작은 **LFP 양극**으로 옮겨 비활성 함량을 20 % → 1–4 % 로 줄임 (+ SWCNT · 탄소 코팅 Al).

---

## 0. 이 digest 를 읽는 법

**사용자 질문**: *"sdcp랑 유사한데 요건 어케 진행됐는지"* — 그래서 이 digest 는 세 축으로 짰다.
1. **연구가 진행된 순서** (§8) — 단계마다 무엇을 확인했고 그게 다음 단계를 어떻게 정했나.
2. **계산** (§4) — 코드 · 범함수 · 분산 · 컷오프 · 모델 · 전하/스핀 · 보고량 정의 · 실험 대조를 SI 원문 기준으로.
3. **우리 SDCP 와의 비교** (§7.2) — **방법 · 보고량 정의 수준에서만.** 우리 SDCP 흡착값은 citable false 라 숫자를 나란히 두지 않는다 (`db/properties/sdcp_neutral_closed_2026_08_28.json` · `db/properties/sdcp_doped_closed_2026_08_28.json` · `db/properties/sdcp_c12_closed_2026_09_30.json` 의 금지 서술).

**세 줄 답**
- **진행**: PEG 비는 선행 연구에서 가져왔고 (1/0.3) → GIWAXS 로 "PEG 가 PEDOT 결정성을 올린다" 를 확인 → PVDF 80:10:10 대비 PPP 96:04 전극의 균일성 · 전도도 · 응집력 · Rct 를 비교 → **응집력이 왜 높은지 DFT 로 사후 설명** → 반쪽셀 (RT · 60 °C) → PPP 만으로는 3 wt% 아래에서 전도도 · 고율이 무너지므로 **SWCNT 추가** → 99/01 은 Al 에서 박리 → **탄소 코팅 Al** → 풀셀.
- **계산**: **있다** — CASTEP · PBE · Grimme 분산 · USPP 630 eV · DFT+U (Fe 5.30 eV) · LFP (010) **2층 28원자 슬랩** · 진공 10 Å · 아래층 고정. `E_int = E_total − (E_LFP + E_binder)`. PEDOT⁺/PSS⁻ 는 **술폰산 H 하나를 떼어** 표현했다 (= 이중항 · 우리 `sdcp_doped` 와 **같은 구성**). **SI 에 'spin' 이라는 낱말이 0번** — 상태 선택 규칙 · 전하 검증 · 자세 탐색 · 정규화가 없다.
- **SDCP 와**: 보고량의 **식이 같고 'doped' 구성 (H 원자 제거) 도 같다.** 다른 것은 **우리가 여덟 번 반려받으며 붙인 장치 전부** (상태 정책 · 자세 집계 · 이름 규율 · 기전 서술의 좌표 근거) 가 이 논문에는 없다는 것. ⇒ **방법 선례로는 인용 가능 · 수치 기준점으로는 불가.**

> **본 그림 (2026-11-06)**: `Fig. 1` `Fig. 2` (+ `Fig. 2j` 500 dpi 두 조각 · `Fig. 2f` 400 dpi) `Fig. 3` `Fig. 4` (+ `Fig. 4n` 450 dpi) `Fig. 5` · `Fig. S1` `Fig. S2` `Fig. S5` `Fig. S7` `Fig. S8` `Fig. S10` `Fig. S15` `Fig. S22` `Fig. S25` `Fig. S27` (손 크롭) `Fig. S28` `Fig. S30` `Fig. S33` `Fig. S34` `Fig. S37` · `Table S1` (손 크롭 — 썸네일로 크롭만 확인, 값은 PDF 텍스트) — **그림 20장 + 표 1**.
> **안 본 것 (그림 23장)**: `Fig. S3` `Fig. S4` `Fig. S6` `Fig. S9` `Fig. S11` `Fig. S12` `Fig. S13` `Fig. S14` `Fig. S16` `Fig. S17` `Fig. S18` `Fig. S19` `Fig. S20` `Fig. S21` `Fig. S23` `Fig. S24` `Fig. S26` `Fig. S29` `Fig. S31` `Fig. S32` `Fig. S35` `Fig. S36` `Fig. S38` — SEM · EDS · 면봉 사진 · 사후 SEM 이 대부분이고 캡션 · 본문 서술만 옮겼다 (§5 표에 ⬜ 로 표시). `Fig. S31` 은 PDF 텍스트층에서 축 · 범례 (0.1–0.5 mV/s) 만 읽었다.
> 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 한 산술은 **(우리 산술)** 로 표시했다.

---

## 1. 한 줄 요약

PEDOT:PSS 에 PEG (1/0.3) 를 섞은 수계 전도성 바인더 **PPP** 하나로 LFP 전극의 바인더 + 도전재 20 wt% 를 **4 wt%** 로 줄이고 (96:04 · 0.1 C ≈160 · 8 C ≈106 mAh g⁻¹ · 응집력 0.20 kN m⁻¹ = PVDF 80:10:10 의 2.7×), SWCNT 를 더해 **2 wt%** (98/02 · 8 C ≈131), 탄소 코팅 Al 위에서 **1 wt%** (99/01 · 8 C ≈132) 까지 내린 **실험 논문**이다. DFT 는 "PSS 의 술포네이트가 LFP (010) 의 Fe 에 배위해 가장 세게 붙는다 (−3.62 eV)" 는 **사후 설명** 한 장 (`Fig. 2j`) + SWCNT 대리 평판 탄소 한 장 (`Fig. S8`) 이다. ⚠ 제목의 **"ultra-high-loading" 은 활물질 *분율* (96–99 wt%)** 이지 면적 로딩이 아니다 — 주 전극은 **2.8–4.0 mg cm⁻²** 다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 계 | LFP (Advanced Lithium Electrochemistry Co.) 양극 · **액체 전해질** 1.3 M LiPF₆ EC/DEC 3:7 (v/v) + 10 wt% FEC (⚠ §2.4 본문은 LiTFSI — §10 ⑮) · 2032 코인 · Li 금속 반쪽셀 / **MCMB 풀셀** (N/P 1.0–1.2) · 2.0–4.0 V · 1 C = 160 mAh g⁻¹ |
| 바인더 | **PVDF** (Solef, Mw 1,000,000 g mol⁻¹) + Super C45 (TIMCAL) · NMP 대조 · **PPP** = PEDOT:PSS (Heraeus Clevios pH 1000 — 논문 표기, 1.1 wt% 수분산액) + PEG 6000 (TCI), 무게비 1/0.3, 실온 혼합 · **SWCNT/PPP** (SWCNT:PPP = 1:2 w/w) |
| 조성 | PVDF: 80:10:10 · 90:05:05 · 96:02:02 · PPP: 96:04 · 97:03 · 98:02 · 99:01 (**도전재 0**) · SWCNT/PPP: 97/1.0/2.0 · 98/0.6/1.4 · 99/0.3/0.7 |
| 공정 | 슬러리 볼밀 30 min → 18 µm Al 닥터블레이드 (99/0.3/0.7 만 **상용 탄소 코팅 Al**, MTI) → 110 °C 진공 12 h · SWCNT 계는 LFP · SWCNT 를 각각 아세톤 분산 → LFP 분산액을 세 번에 나눠 SWCNT 분산액에 투입 → 90 °C 교반 증발 + 120 °C 진공 12 h → 그 분말을 PPP 와 혼합 |
| 로딩 | **LFP 2.8–4.0 mg cm⁻²** (기본) · 5–7 / 8–10 mg cm⁻² (`Fig. S22`) · 풀셀 96:04 5.78 mg cm⁻² (`Fig. S37`) · 두꺼운 99/01 은 **로딩 미기재** (`Fig. S33`, 3.5 mAh cm⁻²) |
| 계산 | **CASTEP DFT** (SI pp. 2–3) — §4 |
| 연구유형 | 실험 주도 + DFT 보조 (interaction energy 7점) |
| 질문 | 바인더 + 도전재를 최소화해도 접착 · 전도 · 고율 · 수명을 유지할 수 있나? |
| 갭 (저자 주장) | PEDOT:PSS/PEG 는 Si 음극에서 ≈20 % 비활성 함량이 필요했다 (부피팽창 + PEDOT 과의 HOMO–LUMO 부정합) — 부피변화가 작은 LFP 에서는 줄일 수 있다 |

---

## 3. 핵심 수치 총정리

### 3.1 DFT

출처 그림: `Fig. 2j` (LFP) · `Fig. S8` (SWCNT 대리 평판 탄소).

| 계 (그림 라벨) | 기판 | 실제 모델 | E_int (eV) | 출처 |
|---|---|---|---|---|
| LFP–PVDF | LFP (010) | PVDF 주기 사슬 | **−2.06** | 본문 |
| LFP–PEG | LFP (010) | PEG 주기 사슬 (그림에선 고리 모양) | **−0.73** | 본문 |
| LFP–"PEDOT" | LFP (010) | **PEDOT:PSS 복합체, PEDOT 이 표면 접촉** (PEDOT 이량체 + PSS 사슬 · 술폰산 H 1개 제거) | **−2.26** | 본문 |
| LFP–"PSS" | LFP (010) | **같은 PEDOT:PSS 복합체, PSS 가 표면 접촉** (술포네이트 O–Fe 배위 인셋) | **−3.62** | 본문 |
| SWCNT–PEG | 평판 sp² 탄소 ("π-conjugated sp² carbon surface") | PEG | figure-read ≈ **−0.85** | `Fig. S8` (본문 수치 없음) |
| SWCNT–"PEDOT" | 〃 | PEDOT:PSS, PEDOT 면이 판에 평행 접촉 | figure-read ≈ **−2.13** | 〃 |
| SWCNT–"PSS" | 〃 | PEDOT:PSS, PSS 페닐/술포네이트 쪽 접촉 | figure-read ≈ **−2.37** | 〃 |

- PSS 배향이 PEDOT 배향보다 **1.36 eV** 더 음수 (우리 산술: −3.62 − (−2.26)).
- 정규화 없음 (셀당 총량) · 자세 1개씩 (PEDOT:PSS 만 2개) · 오차막대 없음.

### 3.2 바인더 막 구조 (GIWAXS)

출처 그림: `Fig. S1`.

| 항목 | PP (PEDOT:PSS) | PPP (+PEG) | 비고 |
|---|---|---|---|
| 강해진 반사 | — | q = **1.26 Å⁻¹ (PSS)** · **1.7 Å⁻¹ (PEDOT)** | 본문 배정 |
| 결정자 크기 face-on (q_z) | **1.268 nm** | **1.866 nm** | `Fig. S1c` 라벨 |
| 결정자 크기 edge-on (q_xy) | **0.949 nm** | **1.356 nm** | 〃 |
| 상대 결정도 ((010) 적분강도) | **1.000** | **1.732** | `Fig. S1d` 라벨 |
| 측정 | PAL 6D UNIST-PAL · λ = 1.0722 Å · 입사각 0.12° · O₂ 플라즈마 처리 Si 위 스핀코팅 | | 방법 |

### 3.3 전극 — 응집력 · 전도도 · Rct

출처 그림: `Fig. 2f,g,i` · `Fig. 4c–e` · `Fig. S2` · `Fig. S7` · `Fig. S15` · `Fig. S25`.

| 전극 | 비활성 | Rct (Ω) | σ_DC (S cm⁻¹) | SAICAS 응집력 (kN m⁻¹) |
|---|---|---|---|---|
| PVDF 80:10:10 | 20 % | **≈150** (본문) · figure-read ≈145 | **0.35** | **0.074** |
| PVDF 90:05:05 | 10 % | **≈370** | figure-read ≈0.06 | **0.049** |
| PVDF 96:02:02 | 4 % | figure-read ≈420 | figure-read ≈0.03 | **0.048** |
| PPP 96:04 | 4 % | **≈120** · figure-read ≈115 | **0.76** | **0.20** |
| PPP 97:03 | 3 % | figure-read ≈125 | figure-read ≈0.54 | figure-read ≈0.17 |
| PPP 98:02 | 2 % | figure-read ≈160 | figure-read **≈0.04** | figure-read ≈0.11 |
| PPP 99:01 | 1 % | figure-read ≈180 | figure-read **≈0.01** | **0.07** (figure ≈0.069) |
| SWCNT/PPP 97/1.0/2.0 | 3 % | **88** | **3.02** | **≈0.10** (figure ≈0.108) |
| SWCNT/PPP 98/0.6/1.4 | 2 % | **110** | **1.55** | **≈0.10** (figure ≈0.103) |
| SWCNT/PPP 99/0.3/0.7 | 1 % | **≈147** | **0.394** | **0.07** (figure ≈0.065) |
| PEG 효과 (`Fig. S2` · `Fig. S7`) | — | 90/10 조성에서 figure-read ≈230 → ≈95 | 96/4 에서 **0.248 → 0.763** | 96/04 에서 figure-read ≈0.173 → ≈0.200 |
| SWCNT:PPP 비 (97/03, `Fig. S15`) | 3 % | figure-read 1:2 ≈88 · 1:1 ≈100 · 2:1 ≈135 | — | — |
| 100 cyc 전후 σ (`Fig. S25`) | 3 % | — | figure-read PPP 97/03 ≈0.64 → ≈0.44 · SWCNT 97/01/02 ≈3.03 → ≈2.92 | — |

- **96:04 응집력 / 80:10:10 = 2.70×** (우리 산술 0.20/0.074 · 본문 "≈2.7"). σ 비 **2.17×** (0.76/0.35).
- ★ **PPP 단독은 97:03 → 98:02 에서 σ 가 한 자릿수 이상 떨어진다** (figure-read ≈0.54 → ≈0.04) — 본문은 96:04 값만 인용한다 (§10 ⑲).
- ★ **같은 3 wt% 에서 SWCNT 를 섞으면 응집력이 낮아진다** (PPP 97:03 figure-read ≈0.17 → SWCNT 97/03 ≈0.108) — 본문은 "maintaining robust cohesion" (§10 ⑩).
- HR-TEM 피막: 96:04 **5.43 nm** (`Fig. 2e` 라벨 · 본문 "≈5 nm") · 99/01 SWCNT **3.29 nm** (`Fig. 4k` 라벨).

### 3.4 반쪽셀 (RT · Li 대극)

| 전극 | 0.1 C | 고율 | 3 C 수명 | 출처 |
|---|---|---|---|---|
| PVDF 80:10:10 | ≈160 (방전 3.4 V) | **8 C ≈87** · 7 C ≈100 | (`Fig. S11`, 안 봄) | `Fig. 3a,b` |
| PVDF 90:05:05 | figure-read ≈155 | figure-read 1 C ≈87 · 2 C ≈52 · 3 C ≈32 · 4 C 이후 ≈0 | — | `Fig. 3b` |
| PVDF 96:02:02 | figure-read ≈153 | figure-read 1 C ≈52 · 2 C ≈9 · 3 C 이후 ≈0 | — | `Fig. 3b` |
| PPP 96:04 | ≈160 | **8 C ≈106** | **1000 cyc 94.8 %** | `Fig. 3c–e` |
| PPP 97:03 | figure-read ≈160 | **7 C ≈105** → 8 C figure-read ≈8 (붕괴) | — | `Fig. S10` |
| PPP 98:02 | figure-read ≈160 | **5 C ≈119** → 6 C figure-read ≈7 (붕괴) | — | `Fig. S10` |
| PPP 99:01 | figure-read ≈160 | figure-read 4 C ≈128 → 5 C ≈7 (붕괴) | — | `Fig. S10` |
| SWCNT 97/03 | figure-read ≈165 | **8 C 138** (80:10:10 대비 +58 % · 96:04 대비 +30 %) | **1000 cyc 96 %** | `Fig. 4f,h,i` |
| SWCNT 98/02 | figure-read ≈158 | **8 C 131** (80:10:10 대비 +51 %) | **1000 cyc 96 %** | `Fig. 4g,h,i` |
| SWCNT 98/02 · 5–7 mg cm⁻² | figure-read ≈160 | figure-read 8 C ≈128 | figure-read 3 C 200 cyc ≈143 | `Fig. S22` |
| SWCNT 98/02 · 8–10 mg cm⁻² | figure-read ≈163 | figure-read **8 C ≈90 (평탄부 소실)** | figure-read ≈137 → ≈133 | `Fig. S22` |
| SWCNT 99/01 @ 탄소 코팅 Al | ≈157 | **8 C ≈132** | **1000 cyc 91 %** (§10 ⑭) | `Fig. 4l–n` |
| SWCNT 99/01 @ 일반 Al | figure-read ≈157 | figure-read **8 C ≈70** | — | `Fig. S30` |
| 두꺼운 99/01 @ 탄소 코팅 Al | **3.5 mAh cm⁻²** @ 0.1 mA cm⁻² | — | — | `Fig. S33` |

- 단위는 mAh g⁻¹ (LFP 기준). 유지율 % 의 **기준 사이클이 어디에도 안 적혀 있다.**

### 3.5 60 °C

| 항목 | PVDF 80:10:10 | PPP 96:04 | 출처 |
|---|---|---|---|
| C-rate 별 유지율 (0.1 → 5 C) | 100 · 96.9 · 96.2 · 95.3 · 86.3 · **58.8** · **1.65** · **0.39** % | 100 · 98.3 · 96.5 · 95.0 · 91.1 · 87.6 · 83.8 · **79.6** % | `Fig. 3i` 라벨 |
| 3 C 400 cyc | figure-read ≈78 → ≈38 (≈95 cyc) → **≈97 cyc 에서 ≈0 으로 급사** | figure-read ≈123–130 유지 | `Fig. 3j` |
| TMA 치수변화 (막) | figure-read ≈0.2 µm (50 °C) · ≈0.65 (60) · ≈1.7 (70) · ≈3.2 (80) · ≈4.5 (90) · ≈5.4 µm (97 °C) | ≈0 (30–97 °C) | `Fig. S27` |
| 전해액 팽윤 (60 °C) | figure-read ≈48 % (2 h) · ≈50 (4 h) · ≈41 (6 h) | ≈9.5 · ≈10.8 · ≈11.8 % | `Fig. S28` |
| 풀셀 99/01 @ 60 °C | — | 8 C 에서 0.1 C 의 **94.1 %** (라벨) · 3 C 200 cyc figure-read ≈145 → ≈135 | `Fig. 5h–j` |

### 3.6 풀셀 (‖ MCMB — MCMB:SuperC45:SBR:CMC = 90:5:2.5:2.5 · Li 대극으로 선(先)사이클해 SEI 형성)

| 양극 | 0.1 C | 8 C | 3 C 수명 | 출처 |
|---|---|---|---|---|
| PVDF 80:10:10 | figure-read ≈157 | figure-read **≈78** | figure-read 600 cyc ≈139 → ≈136 | `Fig. S34` |
| SWCNT 98/02 (일반 Al) | ≈160 | **≈124** (기존 대비 ≈+60 %) | **600 cyc 96.5 %** | `Fig. 5a–c` |
| SWCNT 99/01 (탄소 코팅 Al) | **≈157** | **≈125** | **600 cyc 95.2 %** | `Fig. 5d–f` |
| PPP 96:04 · 5.78 mg cm⁻² | figure-read ≈160 | figure-read ≈93 | **없음** (율속만) | `Fig. S37` |
| Ragone | "This work" figure-read ≈500 Wh kg⁻¹ (≈50 W kg⁻¹) → ≈350 Wh kg⁻¹ (≈3,500 W kg⁻¹) — **기준 질량 미기재** | | | `Fig. 5g` |

### 3.7 "ultra-high-loading" 이 뜻하는 것 — 면적 환산 (우리 산술)

| 전극 | 로딩 | 면적용량 (160 mAh g⁻¹ 가정) |
|---|---|---|
| 기본 전극 전부 | 2.8–4.0 mg cm⁻² | **≈0.45–0.64 mAh cm⁻²** (1 C ≈0.45–0.64 mA cm⁻²) |
| `Fig. S22` | 5–7 / 8–10 mg cm⁻² | ≈0.8–1.1 / ≈1.3–1.6 mAh cm⁻² |
| `Fig. S37` | 5.78 mg cm⁻² | ≈0.92 mAh cm⁻² |
| `Fig. S33` | **미기재** | 측정 3.5 mAh cm⁻² ⇒ 역산 **≈22 mg cm⁻²** |

⇒ **"ultra-high" 는 분율 (96–99 wt%)** 의 말이다. 면적 기준의 "초고로딩" 은 litdb 에서 [Han25] ICEP **62.4 mg cm⁻²** · [Jung26] PAMPS-CNT **58.4 mg cm⁻²** 같은 수준을 가리킨다 — **같은 낱말, 다른 축.**

---

## 4. DFT / 계산 방법 ★★ — SI pp. 2–3 원문 기준

### 4.1 세팅 전표

| 항목 | 값 | 비고 |
|---|---|---|
| **코드** | **CASTEP** [1] — 평면파 DFT | NNP · MLIP 아님. 수렴 기준 조합이 Materials Studio CASTEP 프리셋 값처럼 보인다 (추정 — 논문은 GUI 를 안 적었다) |
| **범함수** | **GGA-PBE** [2] | |
| **스핀** | **기재 없음** — SI 에 'spin' 이라는 낱말이 **0번** | ⚠ Fe²⁺ 고스핀 d⁶ 기판인데도 (§4.3) |
| **의퍼텐셜** | **ultrasoft, "generated on the fly"** (CASTEP OTFG) | |
| **컷오프** | **630 eV** | |
| **분산** | **"Grimme's dispersion correction method [3]"** — D2/D3 **판 미기재** | [3] 이 목록에 없어 판을 확인할 수 없다 (§4.10) |
| **k 점** | Monkhorst–Pack, **간격 0.07 Å⁻¹** [4] | 슬랩의 격자 수는 미기재 |
| **SCF** | 5.0 × 10⁻⁷ eV atom⁻¹ | |
| **기하 수렴** | 에너지 5.0 × 10⁻⁶ eV atom⁻¹ · 힘 **1.0 × 10⁻² eV Å⁻¹** · 변위 5.0 × 10⁻⁴ Å · 응력 2.0 × 10⁻² GPa | 응력 기준 = 벌크 셀 최적화용 |
| **DFT+U** | **Fe 3d, U = 5.30 eV** [5] | Materials Project 의 Fe U 와 같은 수 (우리 쪽 상식 — 논문은 [5] 만 적었고 그 [5] 가 목록에 없다) |
| **벌크** | LFP *Pnma*, **MP mp-19017** → "full geometry optimization" | 셀까지 최적화 (응력 기준이 그 근거) |
| **면** | **(010)** — "thermodynamically most stable … lowest surface energy" [6] | [6] 목록 누락 |
| **슬랩** | 화학양론 · 대칭 종단 · **2층, 층당 14원자 (2 f.u.) = 28원자** | 측면 셀 크기 **미기재** (§4.4) |
| **진공** | **10 Å** (⊥(010)) | 흡착체 포함 여부 미기재 |
| **구속** | **아래층 고정** · 위층 + 고분자 전부 이완 | 슬랩 원자의 절반이 고정 |
| **dipole correction** | 언급 없음 | 흡착은 한쪽 면에만 |
| **AIMD / MD / MLIP / NEB** | **없음** | 0 K 정적 최적화만 |
| **전하 · 스핀 분석** (Bader · Mulliken · 스핀밀도 · DOS) | **없음** | 'PEDOT⁺/PSS⁻' 를 검증한 자료 0 |

### 4.2 보고량 정의 — SI 원문

> "To quantify the interfacial interactions between the LFP cathode and polymer binders, the interaction energy … was calculated using the following equation:
> **E_interaction = E_total − (E_LFP + E_binder)**
> where E_total is the total energy of the optimized LFP–binder complex, E_LFP and E_binder are the energies of the isolated LFP (010) surface and binder system, respectively."

⇒ **분리 기준 (separated-reference) 상호작용 에너지** — 음수 = 발열 = 유리. 우리 SDCP 정의식과 **같은 꼴**이다 (§7.2).

**식에 없는 것** (SI 전수 확인):

| 빠진 것 | 왜 중요한가 |
|---|---|
| `E_binder` 를 **같은 셀**에서 쟀나 · 큰 상자에서 쟀나 · 따로 이완했나 | 주기 사슬은 셀 길이에 묶인다 — 셀이 다르면 사슬 간 상호작용 · 변형 에너지가 `E_int` 에 섞인다 |
| **스핀 상태 · 자기 배열** (슬랩 · 복합체 · 기준 셋 다) | 열린 껍질 + 자성 기판 + 산화환원 활성 = 우리 규율의 위험 신호 셋 (§4.3) |
| **정규화** (셀당 · 단량체당 · 접촉면적당) | PVDF 주기 사슬 vs PEDOT 이량체 + PSS 사슬 — 크기 · 접촉 수가 다른 조각의 총량을 한 축에 놓았다 |
| **자세 탐색 · 집계 규칙** | 바인더당 1개 (PEDOT:PSS 만 2개 — 그 둘을 '성분' 처럼 따로 막대로 그렸다, §4.6) |
| BSSE (평면파라 불필요) · ZPE · 열 · 용매 | 바인더는 **물에서** 캐스팅된다 — 수화 · 잔류수 영향 0 |

### 4.3 ⭐ PEDOT⁺/PSS⁻ 를 어떻게 만들었나 — **H 원자 제거 = 이중항** (우리 `sdcp_doped` 와 같은 구성)

> SI 원문: "For the PEDOT:PSS system, **one of the sulfonate groups in PSS chain was dehydrogenated to represent PEDOT⁺ and PSS⁻ states**, and two distinct interfacial configurations were considered …"

**읽기**:
- '탈수소 (dehydrogenated)' = **H 원자 (= H⁺ + e⁻) 를 계에서 뺐다**. 전하를 −1 로 둔 것이 아니다 (주기 CASTEP 계산에 jellium · 총전하 언급 0).
- 그러면 남은 복합체는 **알짜 중성 · 홀전자 1개 (이중항)** 다. 의도는 "SO₃• 가 PEDOT 에서 전자를 받아 **PEDOT•⁺ / SO₃⁻**" 가 되는 것 — 즉 **hole 이 PEDOT 이량체 위에 폴라론으로 앉는다**는 가정이다.
- ⭐ 이것은 우리 `kb/concepts/sdcp_self_doping_explainer_2026_08_26.md` 의 **"프로톤이 아니라 수소 원자를 뗀다"** 와 **정확히 같은 구성**이다 (`sdcp_doped` = C₁₁H₁₅O₆S₂, 중성 이중항). 차이는 SO₃⁻ 가 **별개 사슬 (PSS)** 에 있느냐 (외부 도핑 2성분) **같은 분자에 끈으로 묶였느냐** (자기도핑 1성분) 뿐이다.
- [Han25] ICEP 의 `(−H)` 는 **H 를 슬랩으로 옮긴 것** (조성 보존 · TM 환원) 이었다 — **이 논문은 H 를 계 밖으로 뺐다.** 같은 '−H' 라도 다른 계산이다 (`kb/syntheses/binder_adsorption_charge_state_2026_08_29.md`).

**🔴 그런데 상태가 정해져 있지 않다** — `kb/methodology/estimand_before_running_2026_08_28.md` 의 위험 신호가 **셋 다** 켜져 있다:

| 위험 신호 | 이 계 | 논문이 한 것 |
|---|---|---|
| **열린 껍질** | 이중항 복합체 (홀전자 1개) | 스핀 언급 0 |
| **자성 기판** | LFP = Fe²⁺ 고스핀 d⁶ (벌크는 반강자성 — 일반 지식) · DFT+U | 자기 배열 언급 0 |
| **산화환원 활성** | Fe²⁺/Fe³⁺ — LFP 는 바로 그 짝으로 작동하는 양극이다. hole 이 **PEDOT 이 아니라 표면 Fe** 로 갈 수 있다 (= 흡착이 아니라 전하이동이 `E_int` 에 섞인다) | hole 위치 확인 0 (Bader · 스핀밀도 · Fe 모멘트 없음) |

⇒ 회신 N 문구 그대로: *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다."* **−2.26 · −3.62 eV 는 어느 상태의 값인지 말할 수 없다.** 특히 −3.62 (PSS 배향 · 술포네이트–Fe 접촉) 는 hole 이 Fe 로 넘어가기 가장 쉬운 배치라, **"정전기 + Fe–O 배위" 라는 기전 서술과 "Fe 산화 (전하이동)" 를 이 자료로는 가를 수 없다.**

**도핑 수준** — 이량체에 hole 1개 = **EDOT 당 0.5** (우리 산술). 우리 `db/properties/sdcp_doped_closed_2026_08_28.json` 이 n=1 (+1 hole/repeat) 모델을 *"25–35 % 평균 도핑과 extended-polaron 보고량을 대표하지 않는다"* 고 적은 것과 **같은 축의 한계**다 (값 이식이 아니라 논리만).

### 4.4 슬랩 모델 — SI 서술 + figure-read

- **2층 · 층당 14원자 = 28원자** (LiFePO₄ 2 f.u./층). *Pnma* 의 b 방향 한 주기가 두 층이므로 **b 한 주기 두께**다 (우리 해석).
- **측면 셀 크기는 안 적었다.** 층당 2 f.u. 이면 (010) 면 단위 a × c 한 칸 (≈10.3 × 4.7 Å — 격자상수는 일반 지식) 과 맞는다 → **1×1 측면 셀일 가능성** (추정). 그렇다면 흡착체는 **사실상 단분자층 피복**이고 이웃 영상과 측면으로 맞닿는다.
- `Fig. 2j` 500 dpi 판독 (figure-read): 슬랩은 면 법선을 오른쪽으로 눕혀 그렸고 가로선 둘이 셀 경계로 보인다. **PVDF 사슬은 그 경계를 넘어 주기적으로 이어진다** (경계 사이에 CF₂ 3–4개). **PEG 는 경계 안의 고리 모양** — 주기 방향이 지면 안쪽이면 SI 의 '주기 사슬' 과 맞지만 그림만으로는 확인 불가. PEDOT:PSS 복합체는 슬랩 두께의 **≈2.3–2.8배 길이**로 법선 방향으로 뻗어 있다 (거친 어림으로 ≈11–15 Å).
- ⇒ **진공 10 Å 이 슬랩 위 기준이면 복합체가 위쪽 영상 슬랩과 겹친다.** 흡착체 위 기준인지 SI 가 말하지 않고, 그림의 가로선 길이로 셀 길이를 확정할 수도 없다 — **판단 불가**로 둔다 (우리 SDCP 는 슬랩–영상 거리와 복합체 꼭대기–셀 경계 거리를 따로 검사했다, §7.2).
- 아래층 고정 = 슬랩 원자의 **절반**이 벌크 좌표에 묶인다. 2층 슬랩에서 '아래층 = 벌크' 가정은 거칠다.

### 4.5 고분자 조각 모델

| 고분자 | SI 서술 | 그림에서 보이는 것 (figure-read) |
|---|---|---|
| PVDF | 주기 사슬 | 경계를 넘는 지그재그 사슬, F 가 양쪽 |
| PEG | 주기 사슬 | 고리 (crown 비슷한) 모양 — 헬릭스를 축 방향에서 본 모습일 수도 |
| PSS | 주기 사슬 · 술폰산 중 1개 탈수소 | 페닐-술포네이트 3개 정도가 보이는 토막 (경계를 넘는지 불명) |
| PEDOT | **이량체** ("significant lattice mismatch would otherwise lead to unrealistic structural distortion") | 고리 둘 — LFP 위에서는 면을 세운 배치, 평판 탄소 위에서는 눕힌 배치 |

### 4.6 ⚠ "PEDOT −2.26 · PSS −3.62" 의 정체 — **같은 복합체의 두 배향**

- 본문: *"the **individual components** of PEDOT:PSS demonstrated considerably stronger interactions, with PEDOT and PSS exhibiting interaction energies of −2.26 eV and −3.62 eV"*.
- SI: *"two distinct interfacial configurations were considered: one in which PEDOT is positioned in direct contact with the LFP surface, and the other in which PSS forms the primary interface"*.
- `Fig. 2j` 구조 (직접 봄): 'LFP–PEDOT' 칸에도 PSS 가, 'LFP–PSS' 칸에도 PEDOT 이량체가 **같이 있다.**
- ⇒ 두 막대는 **성분별 기여가 아니라 PEDOT:PSS 복합체 하나의 두 흡착 자세**다. "individual components" 라는 본문 서술은 **틀린 이름**이다. 자세 집계 규칙으로 읽으면 'PEDOT:PSS 의 최저 자세 = −3.62' 하나이고, 그것이 PVDF (−2.06) 와 비교할 짝이다 — 단 **크기가 다른 조각**의 셀당 총량끼리다.

### 4.7 SWCNT 대리 모델 (평판 sp² 탄소)

- 캡션: *"The SWCNT surface is modeled as a π-conjugated sp² carbon surface."* — 그림 (직접 봄): **평판 탄소 한 장** 위에 PEG / PEDOT 면-평행 / PSS 접촉 세 배치, 축 c↑ b← a⊗.
- 값 (figure-read): PEG ≈ −0.85 · PEDOT ≈ −2.13 · PSS ≈ −2.37 eV. **본문에 수치 없음.**
- 휜 CNT (지름 수 nm) 가 아니다 — 곡률 · 끝단 · 결함을 다 뺐다. 셀 · k · 진공은 따로 적지 않았다.
- 본문은 이것으로 *"enabling uniform SWCNT dispersion while preserving conductive network formation"* 까지 말한다 — 결합 에너지에서 분산성으로 가는 다리는 없다.

### 4.8 실험과 어떻게 대조했나 — **정성 연결 넷, 정량 연결 0**

| DFT 서술 | 대응시킨 실험 | 연결의 성격 |
|---|---|---|
| PEDOT:PSS (특히 PSS) 가 PVDF 보다 세게 붙는다 | SAICAS 응집력 0.20 vs 0.074 kN m⁻¹ (`Fig. 2i`) | 순위 일치만 · 에너지 → 힘 환산 없음 |
| "PEDOT:PSS/PEG 가 PVDF 보다 얇고 균일하게 덮는다" 를 뒷받침 | HR-TEM 5.43 nm (`Fig. 2e`) · EDS S 분포 | 결합 세기 → 피막 두께는 논증 없음 |
| PEG 는 앵커가 아니다 (−0.73) · 그런데 "PEG strengthens PEDOT:PSS–LFP interaction" | `Fig. S7` 응집력 figure-read ≈0.173 → ≈0.200 | ⚠ **PEDOT:PSS/PEG 3성분 계산은 없다** — 계산은 PEG 가 약하다고만 말한다 |
| PEDOT:PSS 가 sp² 탄소에 세게 붙는다 | SWCNT 분산 SEM (`Fig. 4a,b`) · 분산 상태별 σ (`Fig. S19`, 안 봄) | 결합 → 분산은 논증 없음 |

### 4.9 배위수 규칙 적용 (`D-2026-10-05-adsorption-site-coordination`)

세 값 (−2.06 · −2.26 · −3.62 eV) 이 **화학결합 규모 (≳2 eV)** 다. 규칙대로라면 결합 자리의 배위수를 먼저 세야 하는데 —
- **구조 파일이 없다** ("Data will be made available on request").
- `Fig. 2j` 인셋 (500 dpi 로 봄) 은 술포네이트 O 하나가 표면 Fe 하나에 붙는 모습이다. 그 Fe 가 (010) 절단으로 O 를 잃은 저배위 자리인지는 **그림으로 셀 수 없다**. 인셋의 술포네이트 근처에 흰 원자 (H 로 보임) 가 있어 **Fe 에 붙은 것이 탈수소된 SO₃⁻ 인지 SO₃H 인지도 가를 수 없다.**
- ⇒ **"배위 미확인"** 을 값 옆에 같이 적는다. −3.62 eV 는 '그 자리의 결합 포화 에너지' 일 수 있고, 'PSS 가 LFP 표면에 일반적으로 붙는 세기' 로 읽으면 안 된다.

### 4.10 SI 참고문헌 [1]–[6] 이 **없다**

SI 의 References 는 **[7]–[14] (`Table S1` 용) 만** 있다. DFT 절이 인용한 [1] CASTEP · [2] PBE · [3] Grimme · [4] Monkhorst–Pack · [5] U 값 · [6] (010) 표면 안정성은 **목록에 없다** (SI pp. 2–3 · 42–43 확인). ⇒ Grimme **판 (D2/D3)**, **U 의 출처**, **(010) 이 최저 표면에너지라는 근거**를 이 문서로는 확인할 수 없다.

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 개념도 — PVDF + Super C45 ("LFP 80 %", 탄소 응집으로 전자 경로가 끊기는 그림) vs PPP + SWCNT ("LFP 99 %") · 하단 ① PEG screening (PEDOT/PSS 상분리 → PEDOT 결정성↑ → 전도도↑) ② SWCNT (전자전도↑) ③ 흑연 코팅 Al (접착↑) | 설계를 바인더 → 도전재 → 집전체 3단으로 쌓는 그림 양식. ⚠ "High energy-density" 는 셀 에너지밀도로 검증되지 않았다 (`Fig. 5g` 기준 질량 미기재) |
| 2j | ★ DFT — LFP (010) 위 PVDF · PEG · PEDOT:PSS (PEDOT 배향 / PSS 배향) 최적화 구조 + interaction energy −2.06 · −0.73 · −2.26 · −3.62 eV · 인셋 "Fe–O coordination" | ★★ 우리 SDCP 보고량의 문헌 대조군 — 'PEDOT' · 'PSS' 막대 = 같은 복합체의 두 배향 · 스핀 · 상태 · 배위 미기재 (§4.3–§4.9) |
| 2a–e | SEM 평면 · 단면 + EDS (a 80:10:10 평면 · 균열 보임 / b 96:04 평면 / c 80:10:10 단면 Fe · F · C / d 96:04 단면 Fe · S) · e HR-TEM — PPP 피막 **5.43 nm** (인셋 200 nm 저배율) | ⚠ 본문 §2.2 는 2b 를 PVDF 단면, 2c,d 를 PPP 로 부른다 — 캡션 · 그림과 어긋남 (§10 ⑮) · TEM 은 단일 영상 · DMC 분산 슬러리 시료 · bare LFP 대조 없음 (§10 ⑫) |
| 2f–i | f Nyquist (figure-read 반원 끝: PVDF ≈145 · ≈370 · ≈420 Ω / PPP 96:04 ≈115 · 97:03 ≈125 · 98:02 ≈160 · 99:01 ≈180 Ω) · g 전극 σ (PVDF 0.35 · ≈0.06 · ≈0.03 / PPP 0.76 · ≈0.54 · **≈0.04 · ≈0.01** S cm⁻¹) · h SAICAS 모식 (절삭 → t50 박리) · i 응집력 (PVDF 0.074 · 0.049 · 0.048 / PPP 0.20 · ≈0.17 · ≈0.11 · 0.07 kN m⁻¹) | ★ PPP 단독 98:02 의 σ 절벽 = SWCNT 도입의 실제 이유 (본문 미논의) · 96:04 응집력 = 80:10:10 의 2.7× · t50 **응집력** ≠ 집전체 **접착력** · EIS 는 피팅 없는 2전극 |
| 3a–d | PVDF 3 조성 0.1 C 곡선 + 율속 (80:10:10 8 C ≈87 · 90:05:05 · 96:02:02 는 3–4 C 에서 ≈0) · PPP 96:04 율별 곡선 + 율속 (8 C ≈106) | 저바인더 PVDF 의 고율 붕괴 = 전자 경로 부족 · PPP 는 도전재 0 으로 8 C 동작 |
| 3e–g | PPP 96:04 3 C 1000 cyc (94.8 %) + 1000 cyc 후 SEM (평면 · 단면) | 유지율 기준 사이클 미기재 · SEM 은 정성 |
| 3h–j | 60 °C — 율속 · C-rate 별 유지율 (PVDF 5 C 0.39 % · PPP 79.6 %) · 3 C 400 cyc (PVDF ≈97 cyc 에서 ≈0 으로 급사) | 급사 모양은 셀 급사에 가깝다 · 3h 와 3j 의 3 C 값이 다르다 (§10 ⑬) |
| 4c–e | SWCNT 3 조성 — Rct 88 · 110 · 147 Ω · σ 3.02 · 1.55 · 0.394 S cm⁻¹ · 응집력 figure-read ≈0.108 · ≈0.103 · ≈0.065 kN m⁻¹ | ★ 같은 3 wt% 의 PPP 단독 (≈0.17) 보다 응집력이 낮다 — 본문 "maintaining robust cohesion" 과 어긋남 (§10 ⑩) |
| 4a,b,f–i | a,b SWCNT 분산 SEM (SWCNT 를 빨간색으로 덧칠) · f–h 97/03 · 98/02 율별 곡선 · 율속 (8 C 138 · 131) · i 3 C 1000 cyc (96 %) | 덧칠은 주석 — 분산의 정량이 아니다 |
| 4j–n | j 99/01 @ 탄소 코팅 Al 단면 (노란 화살표 = 코팅층) · k HR-TEM (SWCNT · 피막 3.29 nm) · l,m 율별 곡선 · 율속 (8 C ≈132) · n 3 C 1000 cyc (본문 91 %) | figure-read 로 91 % 가 재현되지 않는다 (§10 ⑭) · 99 % 성능은 탄소 코팅 Al 에 기댄다 (`Fig. S30`) |
| 5g | Ragone — "This work" figure-read ≈500 → ≈350 Wh kg⁻¹ vs 문헌 10편 | 기준 질량 미기재 (≈500 은 LFP 질량 기준일 때의 크기) · 범례 번호 [44] · [62]–[70] 이 캡션 [67–76] · 참고문헌과 안 맞음 |
| 5a–f | 풀셀 98/02 ‖ MCMB (8 C ≈124 · 600 cyc 96.5 %) · 99/01 @ 탄소 코팅 Al ‖ MCMB (0.1 C ≈157 · 8 C ≈125 · 600 cyc 95.2 %) | 전압축이 'vs. Li/Li⁺' 로 적혀 있다 (풀셀 축 오기) · 기존 80:10:10 풀셀도 3 C 수명은 안정 (`Fig. S34`) — 차이는 고율 |
| 5h–j | 60 °C 풀셀 — 율속 (8 C 에서 0.1 C 의 94.1 %) · 3 C 200 cyc | |
| S1 | GIWAXS — 2D 패턴 · 방위각 프로파일 · 결정자 1.268 → 1.866 (face-on) · 0.949 → 1.356 nm (edge-on) · 상대 결정도 1 → 1.732 | PEG 단독 막 대조 없음 (§10 ⑪) — SDCP 막 구조 실험 설계에 그대로 쓸 수 있는 프로토콜 |
| S2 | PEG 유무 — EIS (**90/10** 조성) · σ 0.248 → 0.763 (**96/4**) · 0.1 C 곡선 | 패널마다 조성이 다르다 |
| S3 | ⬜ 안 봄 — PVDF 3 조성 평면 SEM (캡션: 균열 빨간 화살표) | |
| S4 | ⬜ 안 봄 — PPP 4 조성 평면 SEM | |
| S5 | SAICAS — 칼날 각 (rake 20° · clearance 10°) 모식 + 50–200 s 응집력 트레이스 (PVDF 3 · PPP 4) | 막대 평균의 원자료 — PPP 97:03 은 요동이 크다 (figure-read ≈0.145–0.19) |
| S6 | ⬜ 안 봄 — 면봉 4회 긁기 사진 (PVDF 2 · PPP 4 조성) | 정성 |
| S7 | PEG 유무 응집력 (96/04) — figure-read ≈0.173 → ≈0.200 kN m⁻¹ | 차이 ≈15 % · 오차막대가 거의 맞닿는다 |
| S8 | ★ DFT — 평판 sp² 탄소 위 PEG · PEDOT · PSS 구조 + 값 figure-read ≈−0.85 · ≈−2.13 · ≈−2.37 eV | 휜 CNT 아님 · 본문 수치 0 |
| S9 | ⬜ 안 봄 — 80:10:10 율별 곡선 | |
| S10 | PPP 4 조성 — 0.1 C 곡선 + 율속: 97:03 은 8 C · 98:02 는 6 C · 99:01 은 5 C 에서 ≈0 으로 붕괴 → 0.1 C 에서 회복 | 본문은 붕괴 직전 값만 인용 · 가역 붕괴 = 분극이 차단전압에 닿는 문턱 거동 |
| S11 | ⬜ 안 봄 — PVDF 80:10:10 · 90:05:05 3 C 사이클 + 사후 SEM | |
| S12 | ⬜ 안 봄 — 1000 cyc 후 EDS | |
| S13 | ⬜ 안 봄 — 60 °C 400 cyc 후 PPP SEM | PVDF 의 60 °C 사후 분석은 없다 |
| S14 | ⬜ 안 봄 — LFP/SWCNT 혼합 분말 공정 모식 + SEM | |
| S15 | SWCNT:PPP 비 (97/03) EIS — figure-read 1:2 ≈88 · 1:1 ≈100 · 2:1 ≈135 Ω | 비 선택 근거가 EIS 하나 |
| S16 | ⬜ 안 봄 — 단면 EDS (97/1.0/2.0 · 98/0.6/1.4) | |
| S17 | ⬜ 안 봄 — 저배율 TEM (SWCNT 분포) | |
| S18 | ⬜ 안 봄 — 광학 사진 (분산 좋음 / 나쁨) | |
| S19 | ⬜ 안 봄 — 분산 상태별 σ | |
| S20 | ⬜ 안 봄 — SWCNT 3 조성 면봉 (99/01 박리) | 99/01 의 집전체 접착 실패 근거 (정성) |
| S21 | ⬜ 안 봄 — SWCNT 3 조성 SAICAS | |
| S22 | 98/02 면적 로딩 5–7 · 8–10 mg cm⁻² — figure-read 8 C ≈128 · **≈90 (평탄부 소실)** · 3 C 200 cyc | 본문 "decent voltage plateaus … at elevated C-rates" 와 8–10 mg cm⁻² 의 8 C 곡선이 어긋난다 |
| S23 | ⬜ 안 봄 — 사이클 중 EIS (PPP 97:03 · SWCNT 97/03) | |
| S24 | ⬜ 안 봄 — 1000 cyc 후 SEM (SWCNT 97/03 · 98/02) | |
| S25 | 100 cyc 전후 σ — figure-read PPP 97/03 ≈0.64 → ≈0.44 · SWCNT 97/01/02 ≈3.03 → ≈2.92 S cm⁻¹ | PPP 쪽 오차막대가 평균의 절반 크기 |
| S26 | ⬜ 안 봄 — 98/02 60 °C 율속 · 사이클 | |
| S27 | TMA — PVDF 막 figure-read ≈0.2 µm (50 °C) → ≈5.4 µm (97 °C) · PPP ≈0 (**손 크롭**) | 초기 두께 · 하중 · 승온속도 미기재 → 변형률 환산 불가 |
| S28 | 60 °C 전해액 팽윤 — figure-read PVDF ≈48–50 % · PPP ≈10–12 % | 방법 · 시료 수 미기재 · PVDF 가 6 h 에 줄어든다 (≈41 %) |
| S29 | ⬜ 안 봄 — 99/01 @ 탄소 코팅 Al 면봉 | |
| S30 | 99/01 율속 — 일반 Al figure-read 8 C ≈70 vs 탄소 코팅 Al ≈132 | ★ 99 % 성능은 집전체 탄소층에 기댄다 (그 질량은 '비활성 함량' 에 안 셈) |
| S31 | ⬜ 안 봄 — CV 0.1–0.5 mV s⁻¹ (96:04 vs 99/01) — PDF 텍스트층에서 축 · 범례만 확인 | 주사속도 계열인데 확산계수 추출을 안 했다 |
| S32 | ⬜ 안 봄 — 99/01 1000 cyc 후 SEM (캡션: SWCNT 가 균열을 잇는 모습) | |
| S33 | 두꺼운 99/01 — 0.1 mA cm⁻² 에서 **3.5 mAh cm⁻²** (로딩 미기재) | 역산 ≈22 mg cm⁻² (우리 산술) · 율속 · 사이클 없음 |
| S34 | 기존 80:10:10 ‖ MCMB — figure-read 8 C ≈78 · 600 cyc ≈139 → ≈136 | 기존 전극도 3 C 수명은 안정 — 차이는 고율뿐 |
| S35 | ⬜ 안 봄 — 풀셀 98/02 600 cyc 후 SEM | |
| S36 | ⬜ 안 봄 — 풀셀 99/01 600 cyc 후 SEM | |
| S37 | 96:04 ‖ MCMB · 5.78 mg cm⁻² — figure-read 8 C ≈93 | 사이클 없음 — 본문 "stable … without significant degradation" 근거 부족 · 캡션의 "ultra-high-loading" 은 ≈0.9 mAh cm⁻² |
| S38 | ⬜ 안 봄 — 60 °C 200 cyc 후 풀셀 SEM | |
| Table S1 | 문헌 비교 9행 — 활물질 분율 · 율속 · 사이클 (**손 크롭**) | 면적 로딩 칸이 없다 — 율속 비교의 핵심 변수가 빠졌다 |

---

## 6. 분석 기법 · 후처리 — 어떻게 수치화했나

| 기법 | 이 논문의 방식 | 메모 |
|---|---|---|
| **GIWAXS** | PAL 6D (λ 1.0722 Å · 0.12°) · 2D 패턴 → 방위각 프로파일 → **피크 폭으로 결정자 크기** (식 미기재 — Scherrer 로 보임, 추정) · **(010) 적분강도로 상대 결정도** (PP = 1 로 정규화) | face-on (q_z) / edge-on (q_xy) 분리 |
| **전극 전자전도도** | 식 (1): **σ_DC = 1 / (면저항 × 두께)** · 면저항 = Hioki RM2610 (electrode resistance measurement system) | ⚠ 두께 표 없음 · 집전체 위에서 쟀는지 미기재 · 바인더 막 자체의 σ 는 **없다** |
| **SAICAS** | 다이아몬드 칼날 폭 1 mm · clearance 10° · rake 20° · 수평 2 µm s⁻¹ · 수직 0.2 µm s⁻¹ 로 t50 까지 절삭 → **박리 모드 평균 수평력 / 칼날 폭** · 시료당 ≥3 회 | 참고문헌 [61] Son 2014 *ACS Appl. Mater. Interfaces* 방법 |
| **EIS** | BioLogic VSP-300 · 1 MHz–0.1 Hz · 10 mV · **반원 지름을 Rct 로** | 등가회로 · 피팅 소프트웨어 언급 없음 |
| **정전류** | Wonatech WBCS3000S · 2.0–4.0 V · 1 C = 160 mAh g⁻¹ | 셀 수 · 오차막대 없음 |
| **CV** | 0.1–0.5 mV s⁻¹ (`Fig. S31`) · 피크 날카로움 · 피크 간격으로 정성 비교 | Randles–Sevcik 같은 정량 없음 |
| **HR-TEM** | JEM-2100 · 200 kV · 슬러리를 DMC 에 분산해 Cu 그리드에 드롭캐스트 · 대기 중 취급 | 피막 두께 = 영상 한 장의 점선 사이 |
| **TMA · 팽윤** | 결과 그림만 (`Fig. S27` · `Fig. S28`) | **방법 절에 기재 없음** |
| **DFT 후처리** | interaction energy 막대 + 구조 그림 (VESTA 류 표현, 도구 미기재) | Bader · 전하밀도차 · DOS · COHP **0** — 기전 서술은 구조 그림에서 나왔다 |
| **문헌 비교** | `Table S1` (반쪽셀 9행) · `Fig. 5g` Ragone (풀셀 10편) | 둘 다 면적 로딩 · 정규화 기준 없음 |

---

## 7. 우리 대비

### 7.1 물성 4축 (A 이온 · B 산화 · C 기계 · D 전자) — **전부 축 밖**

| 축 | 이 논문 | 판정 |
|---|---|---|
| A 이온전도 | Li⁺ 이온전도 측정 0 (EIS Rct 는 전하이동 저항) | ⛔ 제외 |
| B 산화안정 | LSV · 산화 onset 없음 · 운전창 2.0–4.0 V | ⛔ 제외 |
| C 기계 | SAICAS 응집력 · TMA · 팽윤 — 우리 E_VRH (SE 결정) 와 **다른 물체** | ⛔ 제외 (DEM 바인더 축 후보로만) |
| D 전자구조 | gap · DOS 없음 | ⛔ 제외 |

⇒ [Han25] · [Jeong25] · [Jun26] 와 같은 취급 — `comparison_vs_ours.md` 에는 Reference key 1행 + 전용 🧲 note 만 둔다.

### 7.2 ★ 진짜 접점 — SDCP 와 **방법 · 보고량 정의** 비교 (숫자 없음)

> ⛔ 우리 SDCP 흡착값은 이 절에 **싣지 않는다**: neutral 은 비교 보류 (spin-equivalence 복구 전) · doped 는 *"현재 n=1 wave1 프로토콜은 인용 가능한 doped E_ads 를 식별하지 못한다"* · C-12 는 citable false (원고 · SI · 슬라이드 금지). 문헌 절대값과 방법 명시 없이 나란히 놓는 것도 금지다 (`db/properties/sdcp_c12_closed_2026_09_30.json`).

**개념부터** — PEDOT:PSS 와 SDCP 는 '전도성 고분자 바인더' 로 묶이지만 도핑 구조가 다르다:

| | PEDOT:PSS (+PEG) — 이 논문 | SDCP (PEDOT-S 계열) — 우리 |
|---|---|---|
| 도핑 | **외부 도핑** — 짝음이온 SO₃⁻ 가 **별개 사슬 (PSS)** 에 있다 · 2성분 | **자기도핑** — SO₃⁻ 가 알킬 끈으로 **같은 분자**에 묶였다 · 1성분 |
| 형태 조절 | PEG 가 PEDOT/PSS 상분리를 유도해 PEDOT 결정성↑ (`Fig. S1`) | 상분리할 별개 짝이 없다 — PEG screening 기전은 **그대로 옮겨지지 않는다** |
| 계산 조각 | PEDOT 이량체 + PSS 주기 사슬 (술폰산 1개 탈수소) | 단량체 (중성 / H 원자 제거 doped) |

**같은 점**

| 층위 | 이 논문 | 우리 SDCP |
|---|---|---|
| 보고량 식 | `E_int = E_total − (E_LFP + E_binder)` | `E_bind = E_complex − E_slab_iso − E_SDCP_iso` — **같은 꼴** (`kb/projects/sdcp_linio2_binding.md` §Binding Energy Method) |
| 'doped' 구성 | 술폰산 **H 원자 제거** → 중성 이중항 · hole 을 PEDOT 에 둔다는 가정 | **같다** — `sdcp_doped` C₁₁H₁₅O₆S₂ 중성 이중항 (`kb/concepts/sdcp_self_doping_explainer_2026_08_26.md` §4) |
| 슬랩 이완 | 아래층 고정 · 위층 + 흡착체를 **DFT 로** 이완 | 슬랩 하부 층 고정은 같다 — 단 우리 C-12 값은 **UMA 로 이완한 기하 위 DFT 단일점**이다 ('DFT 로 이완한 흡착에너지' 라고 부르지 않는다 — C-12 마감 금지 서술) |
| 해밀토니안 등급 | GGA-PBE + U (TM) + Grimme 분산 | PBE + U + D3 (같은 등급 · 코드는 다름) |
| 가설 | 술포네이트가 산화물 표면 TM 쪽에 붙는다 | 같은 가설군 (술포네이트 앵커링) |

**다른 점 — 우리가 여덟 번 반려받으며 붙인 장치 전부** (`kb/methodology/estimand_before_running_2026_08_28.md`)

| 장치 | 이 논문 | 우리 SDCP | 왜 그 장치가 생겼나 |
|---|---|---|---|
| **스핀 상태 정책** | **기재 0** (SI 에 'spin' 0번) | 분자 · 슬랩 · 복합체의 스핀 제약을 기록하고 **같은 상태 선택 정책**을 요구 | wave1: 제약된 기준에서 자유 복합체를 뺐다 (회신 O) |
| **hole 위치 검증** | 없음 (Bader · 스핀밀도 · Fe 모멘트 0) | 총자화만으로는 배정 불가 → 분자 영역 전하/스핀 적분 · TM 국소모멘트 · spin-density difference 를 요구 | 회신 N · O — 총자화는 hole 위치의 증거가 아니다 |
| **자세 집계** | 바인더당 1 자세 (PEDOT:PSS 2 자세를 '성분' 막대로) | 격자 스캔 + top-K + 짝 자세 (Li-top vs Ni-top) · 자리 판정은 사전등록 matched pose n ≥ 3 | 단일 자세 값이 대표값이 아니었다 (#3–5) |
| **셀 검사** | 2층 28원자 · 진공 10 Å (기준 불명) · 측면 셀 미기재 | 슬랩–영상 거리 · 복합체 꼭대기–셀 경계 거리 · 측면 영상 간격을 따로 검사 (`kb/projects/sdcp_linio2_binding.md` §6) | #1 주기영상 샌드위치 (당일 철회) |
| **조각 크기** | PVDF 주기 사슬 vs PEDOT:PSS 복합체 — 정규화 없이 한 축 | '조각 대 조각' 으로만 · 고분자로의 확장 금지 | neutral 마감 금지 서술 |
| **이름 · 허용 범위** | "interaction energy" → SAICAS **응집력** · **피막 두께**까지 설명 | '결합 세기 · binding energy · 접착 에너지' 라고 부르지 않는다 · 접착력 · 계면저항 · 피복률로 확장 금지 | C-12 · neutral 마감 금지 서술 |
| **기전 서술** | 구조 그림에서 "정전기 + Fe–O 배위" | 좌표를 다시 재서 "술포네이트 O 가 표면 Li 에 배위" 문장을 **철회**한 이력 · ≳2 eV 는 배위수부터 센다 | 회신 T P0-1 · `D-2026-10-05-adsorption-site-coordination` |
| **코드 · 기저** | CASTEP OTFG USPP 630 eV | VASP PAW (+ UMA 로 자세 선별 · ORCA 기체상) | 다른 코드 절대값의 직접 비교 금지 (neutral 마감) |
| **기판 화학** | LFP (010) — Fe²⁺, 다가음이온 (PO₄) 골격 | LiNiO₂ (104) — Ni³⁺, 층상 산화물 | hole 이 기판으로 넘어갈 경향이 기판마다 다르다 — 같은 구성이라도 같은 거동이 아니다 |

### 7.3 시사점 — 우리에게

1. **이 논문은 "PEDOT⁺/PSS⁻ = 술폰산 H 원자 제거" 구성의 문헌 선례**다. 우리 SDCP 원고에서 'doped' 구성을 설명할 때 **방법 선례로는 인용할 수 있다** (단 *"그들은 스핀 상태 · hole 위치를 보고하지 않았다"* 를 같이). **수치 기준점으로는 못 쓴다** — 상태가 정의되지 않은 값이다.
2. 리뷰어가 *"Noh 2026 처럼 그냥 E_ads 를 내면 되지 않나"* 라고 물으면, 이 논문은 **반례가 아니라 대조군**이다 ([Jeong25] note 와 같은 결론): 같은 구성 · 같은 위험 신호 셋인데 상태 정책이 없으면 스칼라가 정의되지 않는다는 것을 이 논문이 **그대로 보여 준다** (PEDOT 배향 vs PSS 배향이 1.36 eV 갈리는데 어느 것이 대표인지 규칙이 없다).
3. **'PSS 배향 (술포네이트–TM 접촉) 이 가장 깊다'** 는 그림은 우리 neutral 마감이 열어 둔 질문 — *"술포네이트-down 자세는 DFT 로 시험한 적이 없다"* — 과 같은 자리를 가리킨다. ⛔ 그러나 **이 논문은 재개 사유가 아니다** (마감 파일: *"새 자세를 하나 더 봤다는 것은 재개 사유가 아니다"*). 다시 연다면 각 마감 파일의 재개 조건 (matched pose n ≥ 3 · 비교 복합체의 총자화 맞춤 · Li/Ni 쌍 이완) 으로만 연다. 그리고 ≳2 eV 가 나오면 **배위수부터** 센다.
4. **실험 쪽 틀은 그대로 쓸 수 있다** (SDCP 실험 협업 시): GIWAXS 결정자 · 결정도 · 면저항 × 두께 σ · SAICAS t50 **응집력**과 집전체 **접착력**의 분리 (이 논문은 후자를 면봉 사진으로만 했다 — 둘 다 정량으로 하는 것이 맞다) · 고온 TMA · 팽윤.
5. **INDEX 🧵 SDCP 앵커 절의 'σ_e(SDCP) 시편규약' 문제에는 답을 주지 않는다** — 이 논문의 σ 는 전부 **복합전극** 값 (≈0.01–3 S cm⁻¹) 이고 바인더 막 σ 는 없다.
6. **전도성 바인더 단독의 문턱**: PPP 만으로는 97:03 → 98:02 사이에서 σ 가 한 자릿수 이상 떨어지고 율속이 계단식으로 무너진다 (figure-read) — 전도성 바인더 함량에 **퍼콜레이션 문턱 같은 거동**이 있다는 실측 사례 (LFP · 액체 · 2.8–4.0 mg cm⁻² 조건 한정 — 황화물 복합양극으로 이식 금지).

### 7.4 litdb 바인더 계보 안에서의 위치

| 편 | 계산 | 상태를 어떻게 다뤘나 | 비고 |
|---|---|---|---|
| [Kang25] `kang2025_bollard_anchored_binder_dry_electrode` | PFP NNP 슬랩 (DFT 아님) · 회전 15 배열 | Na⁺ 짝이온 개수를 **상태 이름**에 박음 (사후 분류) | 결합하는 것이 음이온기가 아니라 Na⁺ 브리지 |
| [Han25] `han2025_icep_binder_ultrahigh_loading_ncm811` | CASTEP · PBE · TS · U (Ni/Co/Mn) · 300 eV · Γ · NCM811 (001) 8층 | `(−H)` = **H 를 슬랩으로 이동** (조성 보존 · TM 환원) · spin-polarized 라고는 적음 · 상태 정책 없음 | 면적 초고로딩 62.4 mg cm⁻² |
| **[Noh26] (이 논문)** | CASTEP · PBE · Grimme · U (Fe 5.30) · 630 eV · 0.07 Å⁻¹ · LFP (010) **2층** | 술폰산 **H 를 계 밖으로 제거** (이중항) · **스핀 언급 0** · 두 배향을 '성분' 막대로 | 분율 '초고로딩' 96–99 wt% · 면적 2.8–4.0 mg cm⁻² |
| [Jeong25] `jeong2025_tough_adhesive_binder_shield_ncm811` | Gaussian 16 분자 계산 (슬랩 없음) | 상태 이름도 없음 | 계보의 최하한 |
| [Jun26] `jun2026_ppma_econductive_binder_si_lowpressure_assb` | 계산 0 | — | PEDOT:P(SS-co-MA) — PSS 쪽을 개조해 접착을 넣은 **같은 설계 논리** (전도 기전 유지를 GIWAXS 로 확인) · ASSB Si 음극 |
| [Jung26] `jung2026_pamps_cnt_crosstalk_high_loading_lmb` | VASP PBE-D3 spin-polarized | (그 digest 참조) | 술폰산 고분자 + CNT 라는 **같은 조합** · 면적 58.4 mg cm⁻² |
| [Patil87] `patil1987_self_doped_conducting_polymers` | — | — | 자기도핑의 원전 — SDCP 와 PEDOT:PSS 를 가르는 개념의 출처 |

⇒ `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` 에 **네 번째 사례**로 넣을 값이 있다 (이번엔 안 건드렸다 — [Jeong25] 도 그 카드에는 아직 안 들어갔다).

---

## 8. 연구 진행 순서 — 단계별 (무엇을 확인했고, 그게 다음을 어떻게 정했나)

### 8.1 동기 → 설계 (Introduction · `Fig. 1`)

- LFP 는 싸고 안전하지만 전압 (≈3.2 V) · 이론용량 (≈160–170 mAh g⁻¹) 이 낮아 **비활성 20 % (80:10:10)** 가 에너지밀도를 더 깎는다.
- 전도성 고분자 바인더 (PPy · PANI · PEDOT:PSS) 는 접착 + 전도를 한 물질로 한다. PEDOT:PSS 는 전도도가 모자라 PSS 제거나 이종 용매 도핑이 필요하다.
- 선행 [35] (같은 그룹) 이 Si 음극에서 PEDOT:PSS/PEG 를 썼지만 Si 의 부피팽창 때문에 ≈20 % 비활성이 필요했다 → **부피변화가 작은 LFP 로 옮기면 줄일 수 있다**는 것이 출발점.
- 설계 3단 (`Fig. 1`): ① PEG 로 PEDOT/PSS 상분리 → 결정성 · 전도도↑ ② SWCNT 로 전자 경로 보강 ③ 탄소 코팅 Al 로 집전체 접착 보강.

### 8.2 바인더 구조 확인 (§2.1 · `Fig. S1` · `Fig. S2`)

- **PEG 비 1/0.3 은 이 논문에서 최적화하지 않았다** — *"Based on previous studies, the optimal PEG content in PEDOT:PSS was determined as a 1/0.3 ratio"*.
- GIWAXS (스핀코팅 막): PPP 에서 q = 1.26 (PSS) · 1.7 Å⁻¹ (PEDOT) 반사가 강해지고 결정자 1.268 → 1.866 nm (face-on) · 0.949 → 1.356 nm (edge-on) · 상대 결정도 1 → 1.732.
- 전극 수준 확인 (`Fig. S2`): σ 0.248 → 0.763 S cm⁻¹ (96/4) · EIS 반원 figure-read ≈230 → ≈95 Ω (90/10) · 0.1 C 용량 figure-read ≈155 → ≈160.
- **→ 결정**: 이후 모든 전극에 PPP (PEG 포함) 를 쓴다.

### 8.3 전극 제작 + 1차 비교 (§2.2 · `Fig. 2a–i` · `Fig. S3`–`Fig. S6`)

- PVDF 80:10:10 은 바인더 · 도전재 응집과 불균일 분포 (SEM/EDS) · 균열 (`Fig. S3`, 캡션). PPP 96:04 는 응집 없이 균일, S 가 고르게 분포.
- HR-TEM: LFP 를 덮는 ≈5 nm (5.43 nm) 연속 피막.
- Rct: PPP 96:04 ≈120 Ω < PVDF 80:10:10 ≈150 Ω ≪ 90:05:05 ≈370 Ω. σ: 0.76 vs 0.35 S cm⁻¹ (2.17×).
- SAICAS (t50): PVDF 0.074 · 0.049 · 0.048 kN m⁻¹ vs **PPP 96:04 0.20 (2.7×)** · 99:01 도 0.07 (≈80:10:10).
- 면봉 4회: PPP 는 안 벗겨지고 PVDF (90:05:05 · 96:02:02) 는 벗겨진다 (`Fig. S6`, 캡션).
- **→ 결정**: 주 전극 = **PPP 96:04**. 그리고 *"바인더가 이렇게 적은데 왜 응집력이 높나"* 를 묻는다 → 8.4.

### 8.4 DFT — 응집력의 사후 설명 (§2.3 · `Fig. 2j` · `Fig. S7` · `Fig. S8`)

- LFP (010) 위 interaction energy: PVDF −2.06 (vdW + 이온–쌍극자) · PEG −0.73 (앵커 아님) · PEDOT:PSS **PEDOT 배향 −2.26** (vdW + 양이온–π + 정전기) · **PSS 배향 −3.62** (술포네이트 정전기 + Fe–O 배위).
- PEG 의 역할을 묻는 실험: PEG 유무 응집력 (`Fig. S7`) figure-read ≈0.173 → ≈0.200 → *"the PEG strengthens PEDOT:PSS–LFP interaction"* (3성분 계산 없음).
- SWCNT 대리 평판 탄소 (`Fig. S8`): PEDOT:PSS figure-read ≈−2.1 ~ −2.4 ≫ PEG ≈−0.85 → *"enabling uniform SWCNT dispersion"* — **다음 단계 (SWCNT 도입) 의 근거로 미리 깔아 둔 계산**이다.
- **→ 결정에 실제로 쓰였나**: PEG 비 (선행 연구) · SWCNT 비 (EIS, `Fig. S15`) · 조성 (전기화학) 어느 것도 DFT 로 정하지 않았다. **DFT 는 설계 도구가 아니라 해석 도구**다.

### 8.5 반쪽셀 — RT · 60 °C (§2.4 · `Fig. 3` · `Fig. S9`–`Fig. S13`)

- PVDF 80:10:10 = 0.1 C ≈160 · 8 C ≈87. 90:05:05 · 96:02:02 = 고율에서 사실상 0 (도전재가 모자라면 PVDF 는 못 버틴다).
- PPP 96:04 = 8 C ≈106 · 3 C 1000 cyc 94.8 % · 사후 SEM 변화 적음.
- PPP 97:03 · 98:02 · 99:01 (`Fig. S10`): 7 C ≈105 · 5 C ≈119 · figure-read 4 C ≈128 까지는 버티다가 **다음 단계에서 ≈0 으로 붕괴** (figure-read) — 0.1 C 에서 회복하므로 기계적 파손이 아니라 분극 문턱이다.
- 60 °C: PVDF 는 4–5 C 에서 무너지고 3 C 사이클 ≈97 cyc 에 급사 · PPP 는 5 C 에서 79.6 % · 400 cyc 유지. 기전으로 PVDF 의 α-이완 (>50 °C) 치수변화 (`Fig. S27`) · 팽윤 (`Fig. S28`) 을 제시.
- **→ 결정**: PPP 만으로는 3 wt% 아래에서 전도 경로가 모자란다 (σ 절벽 · 고율 붕괴) → **SWCNT 를 넣어 바인더를 더 줄인다.**

### 8.6 SWCNT 도입 (§2.5 · `Fig. 4a–i` · `Fig. S14`–`Fig. S26`)

- SWCNT:PPP 비 1:2 · 1:1 · 2:1 중 **EIS 최저 (≈88 Ω) 인 1:2** 채택 (`Fig. S15`).
- LFP/SWCNT 를 아세톤에서 먼저 섞어 분말로 만든 뒤 PPP 와 혼합 (`Fig. S14`) — 분산이 나쁘면 σ 가 떨어진다 (`Fig. S18` · `Fig. S19`, 캡션).
- 97/03 · 98/02 · 99/01: Rct 88 · 110 · ≈147 Ω · σ **3.02 · 1.55 · 0.394** S cm⁻¹ · 응집력 ≈0.10 · ≈0.10 · 0.07 kN m⁻¹.
- 율속: 97/03 8 C **138** · 98/02 **131** · 1000 cyc 96 %. 5–10 mg cm⁻² (`Fig. S22`) · 사이클 중 EIS 안정 (`Fig. S23`, 안 봄) · 100 cyc 전후 σ 변화 작음 (`Fig. S25`) · 60 °C 안정 (`Fig. S26`, 안 봄).
- 99/01 은 Rct · σ 는 괜찮지만 **PPP 0.7 wt% 라 Al 에서 박리** (`Fig. S20` 면봉, 캡션).
- **→ 결정**: 99/01 을 살리려면 집전체 쪽을 고친다 → 8.7.

### 8.7 99 % 활물질 — 탄소 코팅 Al (§2.6 · `Fig. 4j–n` · `Fig. S29`–`Fig. S33` · `Table S1`)

- 상용 탄소 (흑연) 코팅 Al 위 99/01: 단면에 Al · 코팅층 · 전극 3층 (`Fig. 4j`) · HR-TEM 피막 3.29 nm (`Fig. 4k`).
- 0.1 → 8 C 정상 곡선 · **8 C ≈132** (일반 Al 에선 figure-read ≈70, `Fig. S30`) · CV 피크가 더 날카롭고 간격이 좁다 (`Fig. S31`, 안 봄 — 본문 서술) · 3 C 1000 cyc 91 %.
- 두꺼운 99/01: 3.5 mAh cm⁻² (`Fig. S33`) · 문헌 비교 `Table S1` (활물질 분율 99 % 가 표에서 최고).

### 8.8 풀셀 (§2.7 · `Fig. 5` · `Fig. S34`–`Fig. S38`)

- 98/02 ‖ MCMB: 0.1 C ≈160 · 8 C ≈124 (기존 figure-read ≈78 대비 ≈+60 %) · 600 cyc 96.5 %.
- 99/01 @ 탄소 코팅 Al ‖ MCMB: ≈157 · 8 C ≈125 · 600 cyc 95.2 % · Ragone (`Fig. 5g`).
- 96:04 · 5.78 mg cm⁻² ‖ MCMB: 율속만 (`Fig. S37`).
- 60 °C 99/01 풀셀: 8 C 에서도 0.1 C 의 94.1 % · 3 C 200 cyc (`Fig. 5h–j`).

### 8.9 한눈에

```
[선행 연구] PEG 비 1/0.3 (Si 음극)
   │
   ▼  GIWAXS: PEG → PEDOT 결정성↑   (S1)   ─ 전극 σ 0.25→0.76 (S2)
   ▼  PPP 96:04 vs PVDF 80:10:10 :  균일 · σ 2.2× · 응집력 2.7× · Rct↓   (Fig. 2)
   │      └─ "왜 적은 바인더로 응집력이 높나?" → DFT (Fig. 2j · S7 · S8)  ← 사후 설명
   ▼  반쪽셀: 96:04 = 8 C ≈106 · 1000 cyc · 60 °C 안정   (Fig. 3)
   │      └─ PPP 3 wt% 미만: σ 절벽 + 고율 계단 붕괴   (Fig. 2g · S10)
   ▼  SWCNT 추가 (비는 EIS 로): 98/02 = 8 C 131 · σ 1.55   (Fig. 4a–i)
   │      └─ 99/01: Al 박리 (면봉)   (S20)
   ▼  탄소 코팅 Al: 99/01 = 8 C ≈132 · 3.5 mAh cm⁻²   (Fig. 4j–n · S30 · S33)
   ▼  풀셀 ‖ MCMB: 8 C ≈124–125 · 600 cyc · 60 °C   (Fig. 5)
```

---

## 9. 논증 구조 — 어디가 측정이고 어디가 해석인가

| 주장 | 측정 근거 | 해석 / 빈 곳 |
|---|---|---|
| PEG 가 PEDOT 결정성을 올린다 | GIWAXS 결정자 · 결정도 (`Fig. S1`) | PEG 단독 막 대조 없음 — PEG 결정 반사와 겹칠 수 있다 (§10 ⑪) |
| PPP 가 LFP 를 ≈5 nm 로 고르게 덮는다 | HR-TEM 한 장 · EDS | bare LFP 대조 없음 |
| PPP 응집력이 PVDF 의 2.7× | SAICAS (≥3 회) | — |
| 그 이유는 PSS–Fe 결합 | DFT 단일 자세 | 상태 미정 · 배위 미확인 · 3성분 계산 없음 |
| SWCNT 가 전도를 높이고 응집력은 유지 | σ · Rct · SAICAS | 응집력은 PPP 단독보다 낮아졌다 (§10 ⑩) |
| 99 % 가 탄소 코팅 Al 로 가능 | 율속 · 면봉 | 집전체 접착력 정량 없음 · 탄소층 질량 미산입 |
| 60 °C 에서 PVDF 실패는 팽윤 · α-이완 때문 | TMA · 팽윤 (방법 미기재) | PVDF 60 °C 사후 분석 없음 · 급사 모양 |
| 높은 에너지밀도 | Ragone | 기준 질량 미기재 · 면적용량 낮음 |

---

## 10. 비판 — 이 논문의 약한 곳

### ① 🔴 DFT 상태 선택 규칙이 없다 — 가장 큰 하자
열린 껍질 (H 원자 제거 이중항) · 자성 기판 (Fe²⁺ 고스핀 + U) · 산화환원 활성 (Fe²⁺/Fe³⁺) — 위험 신호 셋이 다 켜졌는데 스핀 · 자기 배열 · hole 위치를 **한 줄도** 안 적었다 (SI 에 'spin' 0번). −3.62 eV 는 흡착인지 Fe 산화 (전하이동) 인지 가를 수 없는 값이다. (§4.3)

### ② 🔴 'PEDOT' · 'PSS' 막대 = 같은 복합체의 두 배향인데 '성분' 이라 불렀다
본문 "individual components" ↔ SI "two distinct interfacial configurations". 그리고 크기 · 접촉 수가 다른 조각 (PVDF 주기 사슬 · PEG · PEDOT:PSS 복합체) 의 셀당 총량을 정규화 없이 한 축에 순위로 놓았다. (§4.6)

### ③ 🟠 슬랩이 작고 셀 정보가 빠졌다
2층 28원자 · 아래층 (절반) 고정 · 진공 10 Å (흡착체 포함 여부 불명 — 그림의 복합체 길이로 보면 겹칠 수 있다) · 측면 셀 · 피복률 · k 격자 수 · dipole correction 미기재. (§4.4)

### ④ 🟠 배위 미확인 (≳2 eV)
화학결합 규모 값 셋인데 구조 비공개 (data on request) · 인셋으로 Fe 배위 · SO₃⁻/SO₃H 구분 불가. (§4.9)

### ⑤ 🟠 DFT 참고문헌 [1]–[6] 이 SI 목록에 없다
Grimme 판 · U 출처 · (010) 최저면 근거를 확인할 수 없다. (§4.10)

### ⑥ 🟠 DFT → 실험 연결이 정성적이다
에너지 순위 → SAICAS 순위 일치만. "the PEG strengthens PEDOT:PSS–LFP interaction" 은 **계산이 없는** 문장이다 (PEG 단독은 −0.73 eV 로 약하다고 계산이 말한다) · 근거인 `Fig. S7` 차이는 ≈15 % 이고 오차막대가 거의 맞닿는다. "binding affinity → thinner, more uniform coating" 도 논증이 없다.

### ⑦ 🟠 "ultra-high-loading" = 분율이지 면적이 아니다
기본 2.8–4.0 mg cm⁻² (≈0.45–0.64 mAh cm⁻², 우리 산술) — 8 C 라도 전류밀도가 작다. 8–10 mg cm⁻² 에서 8 C 가 무너지는데 (`Fig. S22` figure-read ≈90 · 평탄부 소실) 본문은 "decent voltage plateaus" 로 적었다. 3.5 mAh cm⁻² 는 0.1 mA cm⁻² 한 번 (로딩 미기재 · 역산 ≈22 mg cm⁻²) · 율속 · 사이클 없음. `Table S1` 비교에 **면적 로딩 칸이 없다** — 율속 비교의 핵심 변수다. `Fig. S37` 캡션은 5.78 mg cm⁻² (≈0.9 mAh cm⁻²) 를 "ultra-high-loading" 이라 부른다.

### ⑧ 🟠 99 % 성능은 탄소 코팅 집전체에 기댄다
일반 Al 의 99/01 은 8 C figure-read ≈70 (`Fig. S30`) vs 탄소 코팅 Al ≈132. 그 탄소층은 '비활성 1 %' 에 안 들어간다.

### ⑨ 🟠 응집력과 접착력을 섞었다
SAICAS 는 **t50 응집력** (복합층 안) 이다. 99/01 의 실패 모드라고 한 **집전체 접착력**은 면봉 사진뿐 (`Fig. S20` · `Fig. S29`). 초록은 SAICAS 결과를 "strong adhesion" 으로 쓴다.

### ⑩ 🟠 SWCNT 가 응집력을 '유지' 하지 않는다
같은 3 wt% 에서 PPP 단독 figure-read ≈0.17 → SWCNT 97/03 ≈0.108 kN m⁻¹ (`Fig. 2i` vs `Fig. 4e`). 98/02 는 ≈0.11 vs ≈0.103 으로 비슷하다. 본문은 "surpassed the 0.07 kN m⁻¹ of the conventional" 로만 비교한다.

### ⑪ 🟡 GIWAXS 해석의 대안과 비율의 모호함
PEG 6000 은 반결정성이라 자체 결정 반사가 q ≈1.36 · ≈1.65 Å⁻¹ 근처에 있다 (Cu Kα 2θ ≈19° · ≈23° — **우리 배경지식, 논문에 없음**) — 저자가 PSS (1.26) · PEDOT (1.7) 로 배정한 대역과 가깝다. PEG 단독 막 대조가 없어 "with PEG" 의 강도 증가 중 PEG 자체 결정의 몫을 가를 수 없다. 그리고 "PEDOT:PSS 용액과 PEG 의 무게비 1/0.3" 이 **용액 기준**이면 바인더 고형분의 ≈96 % 가 PEG 가 된다 (1.1 wt% 용액 기준 우리 산술) — 고형분 기준이면 ≈23 %. 이 논문만으로는 어느 쪽인지 모른다 (선행 [35] 확인 필요).

### ⑫ 🟡 HR-TEM 피막의 정체
영상 한 장 · DMC 에 분산한 슬러리 시료 · bare LFP · PVDF 대조 없음. 상용 LFP 는 보통 탄소 코팅 제품으로 나온다 (일반 지식 — 이 논문은 LFP 의 탄소 코팅 여부를 적지 않았다) → 5.43 nm 가 PPP 인지 원래 탄소층을 포함하는지 가를 수 없다. 만약 탄소 코팅 LFP 라면 실제 바인더–입자 계면은 bare LFP (010) 보다 `Fig. S8` 의 sp² 탄소 모델 쪽에 가깝다 (조건부 추론).

### ⑬ 🟡 60 °C PVDF 실패의 모양
3 C 사이클이 ≈95 cyc 까지 서서히 내려가다 ≈97 cyc 에 ≈0 으로 **급사**한다 (`Fig. 3j` figure-read) — Li 금속 대극 · 전해질 쪽 셀 급사의 모양에 가깝다 (추정). 셀 하나 · PVDF 60 °C 사후 분석 없음 · TMA · 팽윤 방법 미기재 (`Fig. S27` 은 µm 만 있고 초기 두께가 없다). 그리고 같은 60 °C · 3 C 인데 `Fig. 3h` 의 3 C 단계 (figure-read PPP ≈143 · PVDF ≈95) 와 `Fig. 3j` 의 사이클 시작 (PPP ≈130 · PVDF ≈78) 이 다르다 (다른 셀로 보인다).

### ⑭ 🟡 유지율 기준이 없다
모든 'x % after N cycles' 의 기준 사이클이 미기재. `Fig. 4n` 의 91 % 는 그림에서 재현되지 않는다 — figure-read 끝값 ≈130 은 3 C 첫 점 (≈135) 대비 ≈96 %, 맨 앞 두 점 (≈153, 형성 사이클로 보임) 대비 ≈85 %. (`Fig. 3e` 의 94.8 % 는 최대값 ≈140 을 기준으로 하면 맞는다.)

### ⑮ 🟡 본문 ↔ 그림 ↔ 방법 불일치 (직접 확인)
- §2.4 가 인용하는 `Fig. 2e` (3 C 사이클) · `Fig. 2f,g` (사후 SEM) · `Fig. 2h–j` (60 °C) 는 **실제로는 `Fig. 3e` · `Fig. 3f,g` · `Fig. 3h–j`** 다.
- §2.2: 본문은 `Fig. 2b` 를 PVDF 단면, `Fig. 2c,d` 를 PPP 로 부르는데 캡션 · 그림은 a/b = 평면 (PVDF/PPP), c/d = 단면 (PVDF/PPP) 이다.
- 결론의 응집력 "0.20 N m⁻¹" · "≈0.10 N m⁻¹" ↔ 본문 · 그림은 **kN m⁻¹** (1000배).
- 전해질: §2.4 "1.3 M **LiTFSI**" ↔ 방법 · 재료 "1.3 M **LiPF₆**" (두 곳이 LiPF₆ 라 §2.4 가 오기로 보인다 — 추정).
- 분리막 Celgard 2400 을 §4.1 은 **polyethylene**, §4.3 은 **polypropylene** 이라 적었다.
- 재료 목록의 **단결정 NCM811 (MTI)** 은 논문 어디에도 안 쓰인다.
- 풀셀 전압축 (`Fig. 5a,d` · `Fig. S34` · `Fig. S37`) 이 "Potential vs. Li/Li⁺" 다.
- `Fig. 5g` 범례 번호 [44] · [62]–[70] 이 캡션 [67–76] · 참고문헌과 안 맞는다 (예: 범례 [44] 'LFP–SCNTs-W2 ‖ Graphite' 인데 목록 [44] 는 Si 음극 논문).
- 참고문헌 [49] 와 [69] 가 같은 논문 (Fan 2022 *Adv. Energy Mater.*) 이다.
- `Fig. S2` 는 EIS 만 90/10, σ 는 96/4 — 패널마다 조성이 다르다.

### ⑯ 🟡 Ragone 의 기준 질량
"Energy density (Wh kg⁻¹)" 의 기준이 없다. ≈500 Wh kg⁻¹ 는 LFP 질량만으로 나눌 때 나오는 크기다 (157 mAh g⁻¹ × ≈3.2 V ≈ 500 — 우리 산술). 문헌 점들과 기준이 같은지 확인할 수 없다.

### ⑰ 🟡 "stable … without significant degradation" (5.78 mg cm⁻² 풀셀)
`Fig. S37` 에는 율속뿐이고 사이클이 없다.

### ⑱ 🟡 EIS 해석
2전극 반쪽셀 — 반원에 Li 금속 쪽 기여가 섞인다. 등가회로 · 피팅 없이 반원 지름을 Rct 로 읽었다.

### ⑲ 🟡 전도도의 시편 규약과 빠진 논의
σ = 1/(R_s × t) 인데 두께 표가 없고 측정 배치 (집전체 위?) 를 안 적었다. PPP 단독 98:02 · 99:01 의 σ 절벽 (figure-read ≈0.04 · ≈0.01) 을 본문이 다루지 않는다 — 98:02 PPP 단독은 PVDF 90:05:05 (≈0.06) 와 σ 가 비슷한데 5 C 에서 ≈119 를 낸다 (PVDF 90:05:05 는 3 C 에서 ≈32). **전극 σ 하나로는 율속이 설명되지 않는다** — 입자마다 감싼 전도 피막의 효과로 볼 수 있지만 논문은 이 대비를 쓰지 않았다.

### ⑳ 🟡 재현성
SAICAS 외에는 셀 · 시료 수 미기재 · 율속 · 사이클 오차막대 없음.

---

## 11. 기술 미니 용어집

- **PEDOT:PSS** — 폴리(3,4-에틸렌다이옥시티오펜) (전자가 흐르는 백본) + 폴리스티렌술폰산 (짝음이온이자 수분산제). PEDOT 위 hole (폴라론) 을 PSS⁻ 가 상쇄하는 **외부 도핑** 계. Clevios PH 1000 은 고전도 등급 수분산액.
- **2차 도핑 / PEG screening** — PEG · DMSO · EG 같은 첨가물이 PEDOT 과 PSS 사이 정전기를 가려 (screening) 상분리를 유도 → PEDOT 사슬이 펴지고 쌓여 결정성 · 전도도가 오른다.
- **자기도핑 (self-doping)** — 짝음이온 (SO₃⁻) 이 같은 고분자 사슬에 공유결합으로 묶인 도핑. 우리 SDCP 가 이 계열이다 ([Patil87]).
- **GIWAXS** — 스침각 광각 X선 산란. 얇은 막의 결정 방향을 2D 로 본다. **face-on** (π 적층 방향이 막 법선, q_z) / **edge-on** (막면 안, q_xy). 피크 폭 → 결정자 크기 · 적분강도 → 상대 결정도.
- **SAICAS** — 다이아몬드 칼날로 비스듬히 파고들어 (cutting) 원하는 깊이 (t50 = 두께 절반) 에서 수평으로 밀며 (peeling) 수평력을 잰다. **힘 / 칼날 폭 = kN m⁻¹**. 깊이에 따라 응집력 (층 안) · 접착력 (집전체 계면) 을 따로 잴 수 있는 장비인데 이 논문은 t50 만 썼다.
- **면저항 (sheet resistance)** — 막 한 변 정사각의 저항 (Ω/sq). 두께를 곱하면 비저항 → σ = 1/(R_s · t).
- **Nyquist · Rct** — 임피던스의 실수부–허수부 그림. 중고주파 반원 지름 ≈ 전하이동 저항 (계면 반응 저항). 반쪽셀이면 Li 쪽 기여도 섞인다.
- **C-rate** — 1 C = 1 시간에 다 쓰는 전류 (여기선 160 mAh g⁻¹ 기준). 8 C = 7.5 분.
- **MCMB · N/P** — 메소카본 마이크로비드 (흑연 음극) · 음극/양극 용량비 (1.0–1.2 → 음극 여유가 작다).
- **탄소 (흑연) 코팅 Al** — 집전체에 얇은 탄소층을 입혀 접착 · 계면 전자전도를 높인 상용 박.
- **CASTEP · OTFG USPP** — 평면파 DFT 코드 (Materials Studio 계열) · 계산 때 즉석 생성하는 초연성 의퍼텐셜.
- **Grimme 분산 보정** — 경험적 쌍 분산 항 (D2/D3). DFT 가 놓치는 vdW 인력을 더한다.
- **DFT+U** — 국소화된 d 전자 (Fe 3d) 의 자기상호작용 오차를 Hubbard U 로 보정. U 를 쓰면 자기 배열 · 산화 상태 선택이 결과를 바꾼다.
- **interaction energy (분리 기준)** — E(복합) − E(표면) − E(분자). 음수일수록 유리. 정의만으로는 **상태 · 자세 · 크기 정규화**가 정해지지 않는다.
- **이중항 (doublet)** — 홀전자 1개 (스핀 1/2) 상태. H 원자를 떼면 생긴다.
- **Ragone plot** — 에너지밀도 vs 출력밀도 로그-로그 그림. 기준 질량 (활물질 / 전극 / 셀) 을 밝혀야 비교가 된다.
- **TMA · α-이완** — 온도에 따른 치수변화 측정 · 고분자 사슬의 큰 분절 운동이 풀리는 전이 (PVDF 는 실온보다 수십 °C 위).
- **팽윤비 (swelling ratio)** — 전해액을 머금은 뒤 무게 (부피) 증가율.

---

## 12. 인용 규율 (⛔ / ✅)

**⛔ 인용 금지**
- **−2.26 · −3.62 eV 를 "PEDOT · PSS 의 결합 세기"** 로 — 같은 복합체의 두 배향이고 상태가 정의되지 않았다 (§4.3 · §4.6)
- **−3.62 eV 를 "술포네이트–LFP 결합 에너지"** 로 — 배위 미확인 · 전하이동과 미분리 (§4.9)
- 이 논문의 DFT 값을 **우리 SDCP 값과 나란히** — 코드 · 기판 · 상태 정책이 전부 다르고 우리 값은 citable false 다
- **"ultra-high-loading" 을 면적 로딩으로** — 분율이다 (§3.7)
- 응집력 **"0.20 N m⁻¹"** (결론의 단위 오기) — kN m⁻¹ 다
- Ragone **≈500 Wh kg⁻¹ 를 셀 에너지밀도로** — 기준 질량 미기재
- `Fig. S8` 값을 **CNT 결합 에너지로** — 평판 탄소 모델이고 figure-read 다
- σ 값 (≈0.01–3 S cm⁻¹) 을 **바인더 막 σ 로** — 복합전극 값이다
- 유지율 % 에 **기준 사이클을 붙여서** (논문에 없다)

**✅ 인용 가능**
- **계산 세팅 전표 그대로** (§4.1): CASTEP · PBE · Grimme (판 미기재) · OTFG USPP 630 eV · MP k 간격 0.07 Å⁻¹ · U(Fe) 5.30 eV · LFP (010) 2층 28원자 · 진공 10 Å · 아래층 고정 · `E_int = E_total − (E_LFP + E_binder)`
- **'doped' 구성의 선례**: *"one of the sulfonate groups in PSS chain was dehydrogenated to represent PEDOT⁺ and PSS⁻ states"* (SI p. 2) — 단 *"spin states and hole localization were not reported"* 를 같이
- 정성 순서 (그들 모델 안에서): PSS 배향 < PEDOT 배향 ≈ PVDF < PEG (깊은 순) · 단일 자세 · 상태 미정
- 실험값 (조건을 붙여서): SAICAS t50 응집력 0.20 vs 0.074 kN m⁻¹ (96:04 vs 80:10:10) · σ 0.76 vs 0.35 S cm⁻¹ · 8 C 106 / 131 / 138 / ≈132 mAh g⁻¹ (각 조성 · 2.8–4.0 mg cm⁻² · 액체 반쪽셀) · 풀셀 8 C ≈124–125 · GIWAXS 결정자 1.268 → 1.866 nm
- 공정 레시피 (LFP/SWCNT 아세톤 선혼합 → PPP · SWCNT:PPP 1:2 · 탄소 코팅 Al)

---

## 13. 무엇을 보고 무엇을 안 봤나

- **읽은 것**: 본문 11 pp 전체 (참고문헌 포함) · SI 43 pp 전체 텍스트 (DFT 방법 pp. 2–3 · 캡션 38개 · `Table S1` · 참고문헌 [7]–[14]).
- **크롭**: 자동 42장 + **손 2장** (`Fig. S27` — 벡터 전용이라 '그래픽 없음' 으로 빠짐 · `Table S1` — 표가 캡션 **위**에 있어 백지로 잘림). `figures.json` 의 `missing_labels` fS27 은 resolved 로 표시. 본문 그림 5장 캡션은 옆 단 본문이 섞여 들어가 PDF 캡션으로 교체 (`caption_note`).
- **실제로 본 그림 20장 + 표 1**: `Fig. 1`–`Fig. 5` 전부 · `Fig. S1` `Fig. S2` `Fig. S5` `Fig. S7` `Fig. S8` `Fig. S10` `Fig. S15` `Fig. S22` `Fig. S25` `Fig. S27` `Fig. S28` `Fig. S30` `Fig. S33` `Fig. S34` `Fig. S37` · `Table S1` (썸네일 — 크롭 확인용).
- **확대 렌더**: `Fig. 2j` (500 dpi 두 조각 — 구조 · 인셋 · 막대) · `Fig. 2f` (400 dpi — Nyquist) · `Fig. 4n` (450 dpi — 91 % 재현 시도).
- **안 본 그림 23장**: `Fig. S3` `Fig. S4` `Fig. S6` `Fig. S9` `Fig. S11` `Fig. S12` `Fig. S13` `Fig. S14` `Fig. S16` `Fig. S17` `Fig. S18` `Fig. S19` `Fig. S20` `Fig. S21` `Fig. S23` `Fig. S24` `Fig. S26` `Fig. S29` `Fig. S31` `Fig. S32` `Fig. S35` `Fig. S36` `Fig. S38` — 캡션과 본문 서술만 옮겼다.
- **본 그림 중 본문과 어긋난 것**: `Fig. 2a–d` (패널 배정) · `Fig. 3` (§2.4 가 Fig. 2 로 인용) · `Fig. 4e` vs `Fig. 2i` (SWCNT 응집력 '유지') · `Fig. 4n` (91 % 재현 안 됨) · `Fig. S22` (8–10 mg cm⁻² 의 8 C 평탄부) · `Fig. S37` (사이클 없음) · `Fig. 5g` (범례 번호) · `Fig. 5a,d` · `Fig. S34` · `Fig. S37` (풀셀 축) · `Fig. 2j` (본문 'individual components' ↔ 그림의 두 배향).

## 14. 후속 조치 (열린 항목)

1. **구조 파일 요청** (data on request) — 받으면 §4.9 배위수 · §4.4 셀 크기 · 진공 기준을 바로 판정한다 (우리 쪽에 필요할 때만).
2. `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` 에 [Jeong25] · [Noh26] 를 3 · 4번째 사례로 넣을지 — 사용자 결정.
3. 선행 [35] (Kong 2024 *Energy Storage Mater.* 64, 103074) 가 inbox 에 들어오면 **PEG 1/0.3 의 기준 (용액 vs 고형분)** 을 확정한다 (§10 ⑪).
4. ⛔ 이 논문은 SDCP 마감 (neutral · doped · C-12) 의 **재개 사유가 아니다** — 재개는 각 마감 파일의 재개 조건으로만.
