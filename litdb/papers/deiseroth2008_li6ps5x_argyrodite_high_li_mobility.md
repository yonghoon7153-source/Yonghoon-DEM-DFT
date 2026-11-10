<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-10 신규 · 사용자 목록 127 번 ("이것도 많이 인용된 논문") · 본문 4 pp (Communication) · SI 없음 (본문에 SI 언급 자체가 없다).
     크롭 5장 (자동 5 · 재크롭 2 `Fig. 2` · `Fig. 5`) 을 **전부 실제로 봤다** (§0 끝 목록).
     `Fig. 2` (유일한 정량 그림) 는 PDF 안의 1-bit 스텐실 래스터에서 픽셀로 읽었다 —
     tools/litdb/deiseroth2008_readout.py (--selftest 음성 경로 4 개 포함) · litdb/figures/deiseroth2008_li6ps5x_argyrodite_high_li_mobility/digitized.csv (51 행).
     ⛔ 이 digest 의 수치는 전부 **소환값**이다. 우리 db 절대값과 같은 셀에 놓을 때는 방법을 같이 적는다 (§8). -->

# Li₆PS₅X: A Class of Crystalline Li-Rich Solids With an Unusually High Li⁺ Mobility — Deiseroth et al. (*Angew. Chem. Int. Ed.* **47**, 755–758 (2008))

> slug `deiseroth2008_li6ps5x_argyrodite_high_li_mobility` · DOI `10.1002/anie.200703900` (국제판 — PDF 1 쪽 머리에 인쇄 · 독일판 `10.1002/ange.200703900` 은 INDEX 엑셀 행이 쓰던 것) · type `exp 전용 (원자단위 계산 0 — 단결정 X-선 · 고체 NMR · 예비 임피던스)` · PDF `127._Li_PS_X_A_Class_of_Crystalline_Li_Rich_Solids_With_an_Unusually_High_Li__Mobility.pdf` (본문 4 pp) · **SI 없음** — 본문에 SI 를 가리키는 말이 없다 · 결정 자료 (좌표 · 변위인자) 는 FIZ Karlsruhe 기탁 **CSD 418490 (Cl) · 418488 (Br) · 418489 (I)** — 우리는 **안 받았다** · digested `2026-11-10` · status ✅ · 태그 **[외부 · exp · ⭐ 아지로다이트 원전]**

> elements: Li, P, S, Cl, Br, I
> methods: NMR

> *(⚠ 이 논문의 다른 두 측정 — 단결정 X-선 회절과 임피던스 — 은 webapp 용어집 어휘에 없어 위 태그 줄에 못 넣었다. 원자단위 계산은 한 건도 없다 — 밀도범함수 계산도 분자동역학도 결합원자가 해석도 없다.)*

> 🎤 **관련 발표**: 없음 — `litdb/talks/*.md` 의 '논문 에이전트 인입 대기열' 에 이 논문 행이 없다 (2026-11-10 grep 확인).
> 🔗 **직계 후속 digest** (이 원전을 무엇으로 고치거나 넓혔나 = §12): [`rao2011_argyrodite_se_studies_bvse`](rao2011_argyrodite_se_studies_bvse.md) (7 일 합성 → 밀링 + 5 h · 조성별 σ 첫 측정 · BV 경로) · [`deklerk2016_diffusion_site_disorder_argyrodite`](deklerk2016_diffusion_site_disorder_argyrodite.md) (AIMD · I 는 inter-cage 점프 0) · [`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`](kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md) (중성자로 Cl 무질서 첫 정량 · Li 48h/24g 점유) · [`adeli2019_halide_substitution_boosting_argyrodite`](adeli2019_halide_substitution_boosting_argyrodite.md) (Cl 과잉 · 무질서 61 → 83 %) · [`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`](morgan2021_anion_disorder_superionic_mechanism_li6ps5x.md) (사면체 type 0–5 · 무질서 기전) · [`shin2026_bh4_reorientation_li_transport_li6ps5x`](shin2026_bh4_reorientation_li_transport_li6ps5x.md) (같은 계의 현대 NMR 수송 — SLR · PFG · EXSY).

> **저자**: **Hans-Jörg Deiseroth\***, Shiao-Tong Kong, Hellmut Eckert, Julia Vannahme, Christof Reiner, Torsten Zaiß, Marc Schlosser — Universität Siegen Anorganische Chemie (Deiseroth · Kong · Reiner · Zaiß · Schlosser) + WWU Münster Institut für Physikalische Chemie (Eckert · Vannahme) · 투고 2007-08-24 · 수정 2007-10-11 · *Angew. Chem. Int. Ed.* 2008, **47**, 755–758 · 지원 DFG · Fonds der Chemischen Industrie · SFB 458 (Eckert · Vannahme) · **임피던스는 사사에만 나온다** — *"We would also like to thank Prof. Dr. H.-D. Wiemhöfer (WWU Münster) for performing the impedance measurements."*
>
> **계보**: 광물 argyrodite Ag₈GeS₆ (1886, refs 1·2) → Ag · Cu argyrodite 구조 · 전도 연구 (refs 3–18 · 예 Ag₉AlSe₆ = 같은 그룹 Gaudin · Deiseroth · Zaiß 2001, ref 12) → Li₇PS₆ + Li₈P₂S₉ 검은 분말 (Brice 1976, ref 19 — *"argyrodite 연결을 모른 채"*) → **본 논문 (2008 · "Li-argyrodite" 를 하나의 물질군으로 처음 묶음)** → 같은 그룹 2011 후속 (litdb 미보유 · 2 차로만 — §12) → [Rao11] → [Klerk] 2016 → [Kraft] 2017 → [Adeli] 2019 → [Morgan21] → 우리 comp1 (Li₆PS₅Cl) · modelc (Li₅.₄PS₄.₄Cl₁.₆).

---

## 0. 이 digest 를 읽는 법 — 원전이 *실제로* 말한 것과 *말하지 않은 것*

이 논문은 아지로다이트 고체전해질 분야의 **출생증명서**다. 그리고 **4 쪽짜리 Communication** 이다 —
분야 전체가 인용하는 무게에 비해 담긴 자료가 적다. 이 digest 는 그 둘을 갈라 놓는 데 목적이 있다.

**논문이 주장하는 세 가지**

| # | 주장 | 근거 | 근거의 세기 |
|---|---|---|---|
| ① | Li₆PS₅X (X = Cl, Br, I) 는 Ag/Cu argyrodite 와 같은 구조형 (F-43m) 의 **"Li-argyrodite"** 물질군이다 | 단결정 X-선 3 조성 (ref 26) | **강함** — 공간군 · 격자상수 · R 값이 다 있다 |
| ② | Li⁺ 이동도가 **유난히 높다** — "unusually high Li⁺ mobility" (제목) | 정적 ⁷Li NMR 선폭이 140–200 K 에서 좁아진다 (`Fig. 2`) + **예비 임피던스 "10⁻² to 10⁻³ S cm⁻¹"** (자료 0) | **선폭은 있고 σ 는 없다** — σ 는 숫자 한 줄뿐이다 (§11-①) |
| ③ | **할라이드와 S²⁻ 가 자리를 나눠 앉는다** (Cl · Br) — I 는 질서 | Br 단결정 점유율 (84/16 · 40/60 %) + ³¹P · 할라이드 MAS NMR 의 날카로움/넓음 (`Fig. 3`–`Fig. 5`) | **Br 은 정량 · Cl 은 정성 · I 는 정성** — Cl 은 X-선으로 S 와 구별이 안 된다 (논문 스스로) |

**우리에게 왜 1 순위인가** — 세 줄기가 이 원전에 직접 닿는다:
1. **comp1 = Li₆PS₅Cl 은 이 논문이 정의한 물질이다.** 격자상수 a = 9.859(2) Å (296 K) 가 우리 EOS 격자의 외부 기준이다 (§8-②).
2. **"Li 는 48h·24g 를 부분점유하고 이웃 자리를 동시에 못 채운다"** — 이 한 문장이 우리 *고정셀 + EOS* 규약
   (`kb/methodology/computational_methods_canonical.md` §3-1 *"우리 셀은 애초에 cubic 이 아니다"*) 의 **물리적 원전**이다 (§8-④).
3. **자리 무질서** — 이 논문은 Li₆PS₅Cl 을 **"fully disordered"** 라고 했다. 그런데 **우리 comp1 은 정렬 극한** (X 형 자리 = Cl 4 · 케이지 자리 = S 4 · 교환 0 %) 이다. 원전이 Li₆PS₅**I** 에 대해 그린 배열 (`Fig. 3a`) 이 우리 comp1 이다 (§8-③ — 우리 CIF 를 직접 셌다).

**이 digest 가 찾아낸 우리 쪽 문제 세 개** (§8-⑦ · `comparison_vs_ours.md` §I):
- 🔴 **우리 원장의 서지가 틀렸다** — `db/literature/refs.json` `deiseroth2006` = *"Angew. Chem. Int. Ed. 45, 5305 (2006)"*. 이 PDF 는 **2007 년 8 월 투고 · 2008 년 47 권 755 쪽**이다.
  같은 키가 comp1 · comp2 · modelc_nd_doped 의 `references` 와 원고 초안 `kb/papers/draft_v1.md` 에 들어가 있다.
- 🔴 `db/properties/adhesion.json` 이 *"Li₆PS₅Cl IS superionic (~3 mS/cm at 300 K, Deiseroth 2006)"* 이라 적는다 — **이 논문에 3 mS/cm 은 없다** (조성 구분 없는 예비값 "10⁻² to 10⁻³" 뿐).
- ⚠ (이미 열려 있던 정정의 독립 재확인) modelc 의 *"4d-Cl 12.5 % (1/8)"* 기록 — 우리 62 원자 CIF 를 **P 배위 기준**으로 다시 세면 **케이지 자리 5 개 중 3 개가 Cl** (Cl 8 개 중 3 개 = 37.5 % = 화학량론 최소) 이다. `feng2020_…` §7d-1 · `comparison_vs_ours.md` §A 의 *"분류기 산물"* 정정과 같은 답이다 (§8-③).

**본 그림 · 안 본 그림** — 이 논문의 크롭 **5 장 전부 실독** (`Fig. 1`–`Fig. 5`). 자동 크롭 2 장을 다시 잘랐다:
`fig_2` (자동 bbox 가 오른쪽 단의 `Fig. 3b` 와 그 캡션까지 끌고 왔다 → 왼쪽 단만) · `fig_5` (저널 머리 로고가 들어왔다 → 아래로).
`Fig. 2` 는 픽셀로 51 점을 다 읽었다 (§3d). 비교를 위해 **다른 digest 의 그림 3 장**도 실독했다 — [Kraft] 그림 3 (무질서 · Li 점유) · 그림 4 (점프 거리 · 픽셀 재판독 → kraft digest 정정 1 건, §12) · [Klerk] 그림 S2 (점프 통계 Li₆PS₅Br)
(다른 논문의 그림은 일부러 '그림 N' 으로 적는다 — 'Fig. N' 표기는 webapp 이 **이 논문** 그림으로 자동 연결한다).
**그림과 본문이 안 맞거나 그림이 본문 주장을 못 받치는 곳 3 군데**: `Fig. 2` 에 130 K 점이 있다 (본문 *"140 K, which is the lowest accessible temperature"*) · `Fig. 4` 의 x 축이 100 ppm 에서 끝나 본문의 Br 102 ppm 약신호가 그림 밖이다 · Cl 95 ppm 약신호도 인쇄 축척에서 안 보인다 (§11).

---

## 1. 한 줄 요약

Li₂S + P₂S₅ + LiX 를 550 °C 에서 7 일 반응시켜 **Li₆PS₅X (X = Cl, Br, I) 를 단상 결정으로 처음 확립**하고, 단결정 X-선으로
**Ag/Cu argyrodite 와 같은 F-43m 구조** (PS₄³⁻ + 고립 S²⁻ + X⁻ 의 사면체 밀집 골격 · Li⁺ 는 48h/24g 부분점유) 임을 보였다.
정적 ⁷Li NMR 선폭이 **140–200 K 에서 이미 좁아지는 것** (Br 이 가장 낮은 온도) 으로 "유난히 높은 Li⁺ 이동도" 를 주장하고,
**Cl · Br 에서는 S²⁻ 와 할라이드가 두 자유 음이온 자리를 섞어 앉고 (Br: 84/16 · 40/60 %) I 는 질서**임을
X-선 + ³¹P/할라이드 MAS NMR 로 보였다. 이온전도도는 **"예비 측정 10⁻²–10⁻³ S cm⁻¹" 한 문장**뿐이다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 동기 | Li⁺ 고체 이동도에 관심이 큰데 결정질 Li 유사체 실험이 거의 없고, 있는 것들 (Li₇PS₆ 검은 분말 ref 19 · Li₂S–P₂S₅ NMR ref 20 · 볼밀 유리세라믹 refs 21–23) 은 **"argyrodite 연결을 언급조차 안 한다"** |
| 왜 Li 가 가능한가 | 4 배위 반지름 **Cu⁺ 74 · Li⁺ 73 pm ≈ · Ag⁺ 114 pm** → Li⁺ ↔ Cu⁺ 치환이 자연스럽다 · 지금까지 안 된 이유 = **고온에서 Li 의 반응성** (용기 재질 문제) |
| 구조 논리 | 고온상 argyrodite = 비금속 (칼코겐/할로겐) 의 **사면체 밀집** (cubic Laves 상 MgCu₂ 위상) · Ag₉AlSe₆ (Z = 4) 의 Se 24 개가 **사면체 구멍 136 개**를 만들고 Al³⁺ 4 (질서) + Ag⁺ 36 (동적/정적 무질서) 이 채운다 |
| Li₆PS₅X 의 치환 | 칼코겐 하나 → 할로겐 하나 (S 와 X 가 **별도 결정학적 자리**에 질서) ⇒ f.u. 당 Li 7 → **6** · P 는 S1 로만 된 구멍 4 개에 (PS₄ 끼리 S1 공유 없음) · 나머지 **132 구멍** (S2 · X 가 만든) 을 **중심에서 벗어난 Li⁺** 가 무질서하게 부분점유 ⇒ 이온식 **(Li⁺)₆(PS₄³⁻)S²⁻X⁻** |
| 질문 | (a) Li-argyrodite 가 결정 단상으로 존재하나 (b) Li 자리는 어디인가 (c) Li 는 얼마나 움직이나 (d) S/X 는 질서인가 |
| 조성 | Li₆PS₅Cl · Li₆PS₅Br · Li₆PS₅I (화학량론 셋 · 고용체 없음) |
| 유형 | exp 전용 — 단결정 X-선 (STOE IPDS) · 정적 ⁷Li NMR · ³¹P/³⁵Cl/⁷⁹Br/¹²⁷I MAS NMR · 예비 임피던스 (사사) · **계산 0** |
| 분량 | 본문 4 쪽 · 그림 5 · 표 0 · 참고문헌 26 (ref 26 = 결정 자료 각주) · SI 없음 |

---

## 3. 핵심 수치 총정리 ★

> 표지 규칙: 본문 숫자는 그대로 · **`figure-read ≈`** = 그림에서만 읽은 값 · **(우리 산수)** = 우리가 논문 숫자로 계산한 값.

### 3a. 결정 자료 — ref 26 (세 조성 · 296(2) K · Mo Kα λ = 71.073 pm · STOE IPDS · SHELXL-97 · F² 정련)

| 항목 | Li₆PS₅Cl | Li₆PS₅Br | Li₆PS₅I |
|---|---|---|---|
| M_r | 268.36 | 312.82 | 359.81 |
| 공간군 | F-43m (No. 216) | F-43m | F-43m |
| **a** | **985.9(2) pm** | **998.8(2) pm** | **1014.5(2) pm** |
| V (Z = 4) | 0.9581(4) nm³ | 0.9963(4) nm³ | 1.0441(3) nm³ |
| V / f.u. (우리 산수) | 239.5 Å³ | 249.1 Å³ | 261.0 Å³ |
| a 의 Cl 대비 (우리 산수) | — | +1.31 % | +2.90 % |
| ρ_calc | 1.860 g cm⁻³ | 2.085 | 2.289 |
| ρ 재계산 Z·M_r/(N_A·V) (우리 산수) | 1.8605 ✓ | 2.0855 ✓ | 2.2890 ✓ |
| μ(Mo Kα) | 1.570 mm⁻¹ | 5.253 | 4.143 |
| 결정 크기 | 0.15 × 0.08 × 0.06 mm³ | 0.28 × 0.11 × 0.11 | 0.23 × 0.06 × 0.05 |
| 2θ_max | 60.62° | 60.92° | 60.68° |
| 반사 (측정 / 독립 / 관측) | 2092 / 181 / 140 | 1433 / 183 / 151 | 2315 / 195 / 178 |
| R_int | 0.0601 | 0.0571 | 0.0419 |
| 정련 변수 | **12** | 18 | 15 |
| R1 (전체 / 관측) | 0.0544 / 0.0367 | 0.0441 / 0.0311 | 0.0257 / 0.0230 |
| wR2 (전체 / 관측) | 0.0993 / 0.0919 | 0.0750 / 0.0693 | 0.0516 / 0.0503 |
| GooF | 1.066 | 1.031 | 1.103 |
| Flack η | 0.021(13) | 0.009(5) | **−0.035(5)** |
| 흡수 보정 (면 수 · 투과 min/max) | 12 면 · 0.8856/0.9257 | 7 면 · 0.5252/0.6930 | 7 면 · 0.6259/0.8205 |
| 이방성 | Li1 빼고 전부 · **Li2 정련 불가** | Li 빼고 전부 | Li 빼고 전부 |
| 기탁 | CSD 418490 | CSD 418488 | CSD 418489 |

- V = a³ 도 맞는다 (우리 산수: 985.9³ pm³ = 0.9583 nm³ · 998.8³ = 0.9964 · 1014.5³ = 1.0441).
- ⚠ **좌표 · 점유율 표 · 결합 길이는 본문에 없다** — CSD 기탁분에만 있다 (우리 미입수). 그래서 Li–S · Li–X 거리를 이 논문에서 가져올 수 없다.

### 3b. 자유 음이온 자리의 S/X 섞임 (`Fig. 3` · 본문 p.756–757)

| 자리 (논문 표기) | 위치 | Li₆PS₅I | **Li₆PS₅Br** | Li₆PS₅Cl |
|---|---|---|---|---|
| **S1** | PS₄ 꼭짓점 | S (섞임 없음) | **Br 1–2 %** (< 2 %) | NMR: 할라이드 "매우 적다" |
| **S2** | 고립 S²⁻ · "단위포 팔분공간 4 곳" | S | **S 84 % · Br 16 %** | **X-선 정량 불가** (S · Cl 대비 차 작음) |
| **X** | "단위포 꼭짓점 · 면 중심" (= 4a) | I | **Br 60 % · S 40 %** | 〃 · NMR: **"fully disordered"** |
| 판정 | | **질서** (X-선 + NMR) | **질서 영역 + 무질서 영역 혼재** (NMR) | **완전 무질서** (NMR · 정성) |

- **(우리 산수) Br 점유율이 화학량론으로 닫히지 않는다.** f.u. 당 Br = 0.16 (S2) + 0.60 (X) + 4 × (0.01–0.02) (S1) = **0.80–0.84** (명목 1.00) ·
  S2 + X 두 자리의 S = 0.84 + 0.40 = **1.24** (명목 1.00). 교환이 대칭이면 'S2 의 Br' = 'X 의 S' 여야 하는데 16 ≠ 40 % 다.
  논문은 점유율의 표준편차도 · 정련 제약 (합 고정 여부) 도 적지 않았고 이 차이를 언급하지 않는다 — **오차인지 실제 비화학량론인지 이 논문으로는 못 가른다.**
- ⚠ **Wyckoff 문자는 X 자리 (모서리 · 면 = 4a) 와 Li (48h · 24g) 에만 나온다.** 고립 S²⁻ 자리는 문자로 부르지 않는다 —
  후속 문헌이 이 자리를 **4c 또는 4d** 로 부르는 것은 원점 · 세팅 선택 차이다 (de Klerk 4c ≡ Kraft 4d ≡ Adeli 4c · `deklerk2016_…` §0 · `adeli2019_…` 자리 라벨 매핑).
  INDEX 엑셀 행의 *"4a/4c 자리를 공유"* 는 후속 문헌의 표기를 원전에 입힌 것이다.

### 3c. Li 자리 (`Fig. 1b` · 본문 p.755–756)

| 항목 | 값 / 서술 |
|---|---|
| Li1 | **48h** — 24g 위아래로 **가까이 붙은 두 자리**, 연결된 두 사면체의 중심 쪽으로 약간 치우침 |
| Li2 | **24g** — 두 사면체의 **공유 삼각면 중심** |
| **d(Li1–Li1)** | **≈ 115 pm (Li₆PS₅I)** — 다른 조성 값은 없다 |
| 동시 점유 | **배제** (*"Simultaneous occupation of these positions is excluded"*) |
| 차이 Fourier | 세 자리 (Li1 · Li2 · Li1) 모두 **≈ 1 e Å⁻³** 의 낮지만 유의한 전자밀도 · 확산 경로의 다른 자리는 < 1 e Å⁻³ (어느 조성인지 문장상 불명확 — 앞 문장이 Li₆PS₅I) |
| 정련 | 본문: *"Both these positions could be refined significantly for the title compounds but with high standard deviations"* ↔ ref 26: Li₆PS₅Cl 은 **Li2 정련 불가** · 세 조성 모두 Li 는 등방 (§11-⑤) |
| 이중 사면체 | `Fig. 1b` = **면공유 S₃I₂ 이중 사면체** (꼭짓점: S2 1 · S1 2 · I 2) — 공유면은 S2–S1–S1 삼각형, 그 중심에 Li2 · 위아래에 Li1 |

### 3d. 정적 ⁷Li NMR 선폭 FWHH vs T (`Fig. 2`) — 본문 + `figure-read ≈` (픽셀 판독 51 점)

본문 숫자·서술:
- 140–160 K: 강한 ⁷Li–⁷Li 쌍극자 상호작용 → 정적 선폭 **"around 6000 Hz" (I · Cl)**.
- Br: **경직 선폭에 140 K 에서도 도달하지 않는다** (*"140 K, which is the lowest accessible temperature"*) · 좁아짐 **200 K 에서 완료**.
- ⇒ *"Li₆PS₅Br has the highest lithium-ion mobility amongst the title compounds"*.
- I: **2 단 좁아짐** — 중간 온도 (170–250 K) 에서 **"더 제한된 운동"** · 이 중간 과정은 **S²⁻/I⁻ 가 질서인 I 에만** 있다.

판독값 (`figure-read ≈` · 단위 Hz · □ ○ ±20 Hz · △ 는 상자 중심 vs 무게중심 모호성 ±60 Hz · T ±0.2 K · 전체는 `digitized.csv`):

| T (K) | **Li₆PS₅Cl** (□) | **Li₆PS₅Br** (○) | **Li₆PS₅I** (△) |
|---|---|---|---|
| **130** | ≈ 6350 ※ | ≈ 4780 ※ | — (점 없음) |
| 140 | ≈ 5800 | ≈ 3750 | ≈ 6160 |
| 150 | ≈ 5580 | ≈ 3140 | ≈ 5370 |
| 160 | ≈ 4910 | ≈ 2620 | ≈ 3380 |
| 170 | ≈ 4010 | ≈ 2340 | ≈ 3000 |
| 180 | ≈ 3120 | ≈ 1920 | ≈ 2850 |
| 200 | ≈ 1890 | ≈ 1320 | ≈ 2540 |
| 250 | ≈ 1080 | ≈ 710 | ≈ 2030 |
| 280 | ≈ 820 | ≈ 580 | ≈ 1620 |
| **295 / 300** | ≈ 730 (295 K) | ≈ 500 (295 K) | ≈ 1240 (300 K) |

※ 130 K 점은 y 축 선 위에 걸쳐 있어 오른쪽 반쪽 + 같은 판 마커 너비 중앙값으로 중심을 복원했다 (도구 docstring).

판독에서 나온 것 (본문 대조 · **우리 산수**):
- **그림의 최저 온도는 130 K** 다 (Cl · Br 둘 다 · `figure-read ≈` 129.9 · 130.0 K) — 본문 · 실험절 (*"140–300 K"*) 과 어긋난다. Br 의 130 K 점도 ≈ 4780 Hz 로 경직 선폭 (≈ 6000) 보다 낮아 **"경직 선폭 미도달" 결론은 130 K 에서도 그대로**다.
- Br 의 "200 K 완료": 130 → 295 K 전체 감소의 **81 %** 가 200 K 까지 일어난다. 200 → 295 K 에도 ≈ 1320 → 500 Hz (**2.6 배**) 더 좁아진다 — "완료" 는 큰 폭 기준이다.
- I 의 2 단: 기울기 140→160 K **≈ 139 Hz/K** · 170→250 K **≈ 12 Hz/K** (평탄) · 260→300 K **≈ 18 Hz/K** (두 번째 하강) — 본문 서술과 맞는다.
- **반폭 온도 T½** (첫 점과 끝 점 선폭의 중간값을 지나는 온도 · 선형 보간 · 우리 정의): **Cl ≈ 175 K · I ≈ 158 K · Br ≤ 159 K** (Br 은 경직 기준점이 창 밖이라 상한 · 경직 선폭을 Cl/I 의 6000 Hz 로 두면 ≈ 148 K).
  ⇒ **같은 잣대로 보면 I 의 첫 단이 Cl 보다 먼저 좁아진다.** 논문은 Cl 과 I 의 순서를 말하지 않는다 (§11-②).
- 300 K 근처 잔류 선폭: **Br ≈ 500 < Cl ≈ 730 < I ≈ 1240 Hz** — I 는 실온에서도 쌍극자 결합이 덜 평균된다.
- 운동 좁아짐 조건 (표준 근사 · §16): 점프율 τ⁻¹ 가 경직 선폭의 각진동수 2π × 6000 Hz ≈ **4 × 10⁴ s⁻¹** 를 넘을 때 ⇒ **T½ 부근 (150–175 K) 에서 Li 점프율 ~10⁴–10⁵ s⁻¹** (우리 산수 · 어떤 운동인지 — 국소 왕복인지 장거리인지 — 는 선폭이 말해 주지 않는다).

### 3e. ³¹P · 할라이드 MAS NMR (`Fig. 4` · `Fig. 5` · 본문 p.757)

| 핵 (조건) | Li₆PS₅Cl | Li₆PS₅Br | Li₆PS₅I |
|---|---|---|---|
| ³¹P (15 kHz MAS · `Fig. 4` 라벨) | **매우 넓다** — 85.1 · 83.6 · 81.6 ppm (분해 안 된 여러 성분) | **날카로운 93.7 ppm (27 ± 2 %) = 질서 영역** + 넓은 성분 (92.6 · 91.0 ppm · **73 ± 2 %**) = 무질서 영역 | **96.3 ppm 단일 · 날카로움** |
| 할라이드 (`Fig. 5` 라벨) | ³⁵Cl **−78 ppm** (넓은 단일선 · 14 kHz) | ⁷⁹Br **109 ppm (날카로움 · 면적 25 %) = 질서** + **−40 ppm (넓음 · 75 %) = 무질서** (15 kHz · 회전 측대역 다수) | ¹²⁷I **188 ppm** + **384 ppm (불순물 추정 — 캡션)** |
| S1 의 할라이드 (PS₃X²⁻) 후보 | **95 ppm** 약신호 — 불순물 배제 못 함 | **102 ppm** 약신호 — 〃 | — |

- 무질서 영역의 넓은 ³¹P = PS₄³⁻ 의 **두 번째 이웃 4 개**가 S 4 · S 3 + X 1 · S 2 + X 2 로 갈리는 다중 환경 (+ 세 번째 껍질 6 자리의 S/Br 분포) — 저자 해석.
- Br 의 질서 분율이 **두 핵에서 맞는다**: ³¹P 27 ± 2 % · ⁷⁹Br 25 % ⇒ Br 시료 = 질서 결정 (영역) 약 1/4 + 무질서 약 3/4.
- ⚠ **약신호 두 개는 그림에서 안 보인다** — `Fig. 4` 의 x 축이 **100 ppm 에서 끝나** Br 의 102 ppm 은 축 밖이고, Cl 곡선의 95 ppm 부근은 인쇄 축척에서 평탄하다 (확대 실독). **본문 서술만 근거다.**

### 3f. 이온전도도 (본문 p.756 — 전부)

> *"Preliminary impedance measurements at room temperature show promising specific Li-ion conductivities in the range **10⁻² to 10⁻³ S cm⁻¹**, and thus support the single-crystal results."*

- 조성별 값 · 온도 의존 · Ea · Nyquist · 전극 · 펠렛 밀도 · 측정 주파수 — **전부 없다**. 임피던스 실험 방법도 실험절에 없다 (측정자 = 사사의 Wiemhöfer).
- ⛔ 그래서 **"Deiseroth 2008 σ = 10⁻² S cm⁻¹"** 로 인용하지 않는다 (§11-① · §15).

### 3g. 이온 반지름 (논문이 쓴 값 · 출처 미기재)

| 이온 | 반지름 | 쓰인 곳 |
|---|---|---|
| Cu⁺ / Li⁺ / Ag⁺ (CN 4) | 74 / 73 / 114 pm | Li ↔ Cu 치환 논리 (ref 24 = 11 족 1 가 반지름 논쟁) |
| **Cl⁻ / S²⁻ / Br⁻ / I⁻** | **181 / 184 / 196 / 220 pm** | S²⁻ 자리 치환 선호 Cl ≈ Br > I 의 설명 (Cl/S 비슷 · Br/S 중간 · I/S 큰 차) |

---

## 4. 재료 & 방법 (exp) ★

### 4a. 합성
- 원료: **Li₂S** (ref 25 = Furukawa 특허 EP-0802159) · **P₂S₅** (Acros, 98+ %) · **LiX** (Fluka, p.a.) — 화학량론.
- Ar 글러브박스 (H₂O < 1 ppm · O₂ < 1 ppm) 에서 혼합 → 펠렛 → **550 °C · 7 일**.
- 일반 분말 X-선으로 **다른 상 없음** (패턴은 실리지 않음).
- 결정은 **무색 · 공기 민감**.

### 4b. 단결정 X-선
- 글러브박스 현미경으로 단결정을 골라 X-선 모세관에 넣고 봉입 · STOE IPDS · Mo Kα · 296(2) K.
- SHELXL-97 (F²) · 수치 흡수 보정 X-RED 1.19 (결정 면 12 · 7 · 7 개로 기술) · 결과 §3a.
- 차이 Fourier 로 Li 자리 전자밀도 확인 (§3c).

### 4c. NMR
| 측정 | 장비 · 주파수 | 조건 |
|---|---|---|
| 정적 ⁷Li (변온) | Bruker DSX 400 · **155.45 MHz** | 봉입 유리 앰풀 · 140–300 K (N₂ 흐름 · Bruker VT 3000) · 에코 **45°–30 µs–90°–20 µs** · 이완 대기 1–10 s |
| ³¹P MAS | DSX 400 · 161.92 MHz | 단일 펄스 · **15 kHz** · 90° 펄스 2 µs · 대기 60 s |
| ³⁵Cl MAS | DSX 400 · 39.19 MHz | **14 kHz** · 4.5 µs 펄스 · 대기 0.1 s |
| ⁷⁹Br · ¹²⁷I MAS | DSX 500 · 125.3 · 100.1 MHz | 15 kHz · 1 µs (2 µs) 펄스 · 대기 1 s |
| 화학적 이동 기준 | 1 M 수용액 LiCl · KBr · KI · 85 % H₃PO₄ | |

### 4d. 임피던스
- **방법 기술 0.** 결과는 §3f 한 문장.

### 4e. 계산
- **없다.** (§5)

---

## 5. DFT/계산 방법 ★

이 논문은 계산을 하지 않는다. 템플릿 항목을 다 적어 둔다 (나중에 "원전의 DFT 설정" 을 찾는 사람을 위해):

| 항목 | 이 논문 |
|---|---|
| code / version | n/a |
| functional (+ vdW) | n/a |
| pseudo / PAW | n/a |
| k-points / ecut / supercell / nat | n/a |
| DFT+U | n/a |
| AIMD | n/a |
| MLIP | n/a |
| **무질서 처리** | 계산 없음 — **실험 점유율 (평균 구조)** 만: Br 은 X-선 정련 점유율 · Cl 은 NMR 정성 · I 는 질서 |

> 후속 계산들이 이 원전 구조를 어떻게 썼는지는 §12 (예: `[Zhu15]` 의 Li₆PS₅Cl E_hull 83 meV/atom 은 *"Deiseroth 2008 구조의 ordered 배열"* 에 자체 DFT — `zhu2015_esw_grand_potential_origin.md`).

---

## 6. 결과 — 섹션별 상세 (그림 실독 포함)

### 6.1 "argyrodite 연결" — 서론의 논증 (p.755)
- Ag⁺ argyrodite 의 높은 이온전도 · 이동도는 오래 연구됐다 (refs 3–18) · Ag⁺ 는 Cu⁺ 로 바꿀 수 있고 P · S 치환도 위상을 유지한다.
- **Li 유사체는 거의 없고, 있는 보고들은 argyrodite 라는 걸 모른다** → 이 논문의 첫 기여는 **물질군의 명명 · 연결**이다.
- Cu⁺ ≈ Li⁺ 반지름 (74 vs 73 pm) → Li-argyrodite 가 존재해야 한다는 논리 · 지금까지 없던 이유 = Li 의 고온 반응성 (용기).

### 6.2 구조 (`Fig. 1`) ★
- `Fig. 1a` (Li₆PS₅I 단위포 일부 · 실독): **회색 PS₄ 사면체** (꼭짓점 S1) · **회색 큰 구 = 고립 S²⁻ (S2)** 가 단위포 안쪽 4 곳 · **흰 구 = I⁻** 가 모서리 · 면 중심 · **검은 작은 점 = Li 자리**들이 S2 둘레에 고리 모양으로 모여 있다 (오른쪽 화살표 **Li1 · Li2 · Li1** 세 점이 한 묶음 = 48h–24g–48h). 축 표시 b ↑ · c ← · a 는 화면 밖.
- `Fig. 1b`: 면공유 이중 사면체 — 꼭짓점 S2 · S1 · S1 (공유면) + 양쪽 끝 I (흰 구) · 가운데 Li2 · 위아래 Li1 (검은 구 셋이 겹쳐 보인다). 이 기하에서 Li1–Li1 ≈ 115 pm.
- 읽어야 할 핵심: **Li 는 '자리' 가 아니라 '자리 묶음' 에 확률적으로 있다.** 한 묶음의 셋 (Li1 · Li2 · Li1) 은 서로 너무 가까워 **하나만** 찰 수 있다.
  ⇒ 이 구조는 **평균 구조**다. 어느 순간의 실제 배치는 F-43m 이 아니다 — 우리 고정셀 규약의 출발점 (§8-④).
- 48h · 24g 는 **Ag/Cu argyrodite 확산 경로의 핵심 자리**와 같다 (Cu/Ag 가 이웃 사면체의 공유면을 지나 뛸 때 쓰는 자리 · refs 8, 10, 12, 18).

### 6.3 전도도 (p.756)
- 예비 임피던스 한 문장 (§3f). *"thus support the single-crystal results"* — 무엇을 지지하는지 (Li 무질서 → 높은 이동도) 의 연결도 서술만이다.

### 6.4 ⁷Li 정적 NMR 선폭 (`Fig. 2`) ★
- 그림 (재크롭 후 실독): **세 판이 위아래로** (Cl □ · Br ○ · I △) · 공통 x 축 **T / K, 130–300 K** (긴 눈금 140 · 160 · … · 300 에 라벨, 짧은 눈금 130 · 150 · … · 290) · 각 판 y 축 **FWHH / Hz** (라벨 2000 · 4000 · 6000 · 사이 눈금 1000 · 3000 · 5000) · 판마다 17 점.
- **Cl**: 130–150 K 에서 ≈ 6350 → 5580 Hz 로 경직에 가깝다가 160–210 K 사이에 급격히 좁아진다 (4910 → 1560) · 이후 완만 (295 K ≈ 730).
- **Br**: 첫 점부터 ≈ 4780 Hz (경직 미도달) · 140–200 K 에 3750 → 1320 · 이후 완만 (≈ 500).
- **I**: 140 → 160 K 에 ≈ 6160 → 3380 (**가파른 1 단**) · 170–250 K 평탄 (3000 → 2030 · 기울기 1/10) · 260 K 위에서 다시 하강 (≈ 1240 @ 300 K).
- 논문의 결론 (Br 최고 이동도 · I 의 제한 운동) 은 그림과 맞는다. **그림이 더 말하는 것**: ① 130 K 점의 존재 ② 같은 반폭 잣대로 I 의 1 단이 Cl 보다 먼저라는 것 ③ 실온 잔류 선폭 순서 Br < Cl < I (§3d).

### 6.5 S/X 섞임 (`Fig. 3`) ★
- 그림 (실독): **P 를 가운데 둔 단위포** — P (검은 점) · PS₄ 사면체 (회색 면) · S1 · 두 번째 이웃 음이온들 (점선 연결).
  `Fig. 3a` (Li₆PS₅I): **검은 구 = S (S1 · S2)** · **흰 구 = I1** — 섞임 없음.
  `Fig. 3b` (Li₆PS₅Br): 자유 음이온 구가 **부채꼴로 칠해져** 있다 — **S2/Br2** (대부분 검정 = S 84 %) · **S3/Br3** (대부분 흰색 = Br 60 %) · S1 은 검정 (1–2 % Br 은 *"not shown"*).
- 할라이드는 대개 별도 자리에 앉아 **P (또는 13·14·15 족 원자) 와 직접 접촉을 피한다** — I 는 그렇다 · **Br · Cl 은 아니다** (세 자리에 걸쳐 분포).
- Cl 은 **X-선으로 정량 불가** (S 16 · Cl 17 전자 — 산란 대비가 없다) — 캡션 *"No quantitative information can be given for Li₆PS₅Cl"*.

### 6.6 ³¹P MAS (`Fig. 4`) ★
- 그림 (실독): x 축 **δ / ppm 100 → 75** (오른쪽이 낮은 주파수) · 위에서부터 Cl · Br · I.
  Cl = 바닥 폭 ≈ 79–89 ppm (`figure-read ≈`) 의 **하나의 넓은 덩어리** (85.1 꼭대기 · 83.6 · 81.6 어깨) · Br = **93.7 ppm 의 매우 날카로운 선** + 92.6 · 91.0 ppm 쪽으로 꼬리 · I = **96.3 ppm 의 날카로운 단일선**.
- ³¹P 이동이 **I 96.3 > Br 93.7 > Cl ≈ 85 ppm** 로 할라이드에 따라 체계적으로 움직인다 (논문은 이 경향 자체는 논의하지 않는다).

### 6.7 할라이드 MAS (`Fig. 5`)
- 그림 (재크롭 후 실독): 세 판 모두 x 축 **δ / ppm +1000 → −1000**.
  ³⁵Cl = −78 ppm 꼭대기의 넓은 단일선 · ⁷⁹Br = **109 ppm 의 매우 좁은 선** + −40 ppm 의 넓은 혹 + 양쪽으로 등간격 회전 측대역 · ¹²⁷I = **188 ppm 의 강한 선** + 384 ppm 의 작은 선 + 측대역.
- ⚠ 세 핵 (³⁵Cl I = 3/2 · ⁷⁹Br 3/2 · ¹²⁷I 5/2) 은 **사중극자 핵**이라 선폭에 국소 대칭 (전기장 기울기) 의 기여가 섞인다 — 논문은 이 기여를 분리하지 않는다 (§11-⑥).

### 6.8 S1 자리의 할라이드
- X-선 (Br < 2 %) 과 NMR 둘 다 **"매우 적다"** 로 일치 · PS₃X²⁻ 가 있으면 별도 약신호가 보여야 하는데 102 (Br) · 95 ppm (Cl) 에 약신호가 있기는 하나 **불순물일 수 있다** (저자).

### 6.9 반지름 논증 (p.757)
- S²⁻ 자리 치환은 **Cl⁻ (181 pm) ≈ S²⁻ (184) → 쉽다 · Br⁻ (196) → 중간 · I⁻ (220) → 어렵다** — 관측된 섞임 순서 (Cl > Br > I) 와 맞는 **사후 설명**이다.

---

## 7. 논증 흐름 종합 — 사슬의 고리마다 근거가 무엇인가

```
[Cu⁺ ≈ Li⁺ 반지름] ──(논리)──▶ Li-argyrodite 가 있어야 한다
        │
[550 °C 7 일 합성 + 단결정 X-선] ──(강함 §3a)──▶ Li₆PS₅X = F-43m argyrodite (①)
        │
[차이 Fourier · Li 부분점유 48h/24g] ──(중간 · Li 는 X-선에 약하다 · Cl 의 Li2 정련 불가)──▶ Li 무질서
        │
[⁷Li 선폭 좁아짐 140–200 K] ──(중간 · 국소/장거리 구분 불가)──▶ "유난히 높은 이동도" (②)
[예비 임피던스 10⁻²–10⁻³]   ──(약함 · 자료 0)──────────────────▲
        │
[Br 점유율 · ³¹P/할라이드 MAS 의 날카로움/넓음] ──(Br 정량 · Cl/I 정성)──▶ S/X 자리 섞임 Cl·Br, I 질서 (③)
        │
[I 에만 2 단 좁아짐] ──(정성 연결 · 저자 해석)──▶ "질서 = 운동 제한" (②와 ③을 잇는 고리)
        │
[반지름 Cl≈S > Br > I] ──(사후 설명)──▶ 섞임 순서
```

- **가장 강한 고리 = ① 구조.** 그 뒤 15 년의 후속이 이 구조를 그대로 쓴다.
- **가장 약한 고리 = σ.** 제목의 "unusually high mobility" 는 사실상 **NMR 선폭** 위에 서 있다.
- **가장 생산적인 고리 = ②–③ 연결 ("I 만 질서 · I 만 제한 운동")** — 이것이 de Klerk (2016 · I 는 inter-cage 점프 0) · Kraft (2017 · 무질서 소멸 → σ 붕괴) 로 이어지는 **"무질서가 장거리 수송을 켠다"** 서사의 씨앗이다. 원전은 이 연결을 *"It is interesting to note …"* 수준으로만 적었다.

---

## 8. 우리 DFT 대비 ★★ (comp1 = Li₆PS₅Cl · modelc = Li₅.₄PS₄.₄Cl₁.₆) → `../our_dft_baseline.md`

### 8-① 한눈에 — 우리 모델이 이 원전에서 가져온 것 / 안 가져온 것

| 항목 | 이 논문 (원전 · 평균 구조) | 우리 comp1 | 우리 modelc | 같은가 · 왜 다른가 |
|---|---|---|---|---|
| 공간군 | **F-43m** (Li 부분점유 평균) | 셀 **계량만 cubic** (a = b = c · 90°) · 원자는 **P1** (Li 배열 하나) | rhombo-62 (fcc 원시 셀 1 × 1 × 5 · 60° · **5 f.u.**) · P1 | 원전 = 시공간 평균 · 우리 = 정적 스냅숏 1 개 — cubic 은 **사람이 부과한 평균 대칭** (methods canonical §3-1) |
| 셀 내용 | 관용 셀 Z = 4 (52 원자 상당) | **52 원자 = 관용 셀 4 f.u.** | 62 원자 = 5 f.u. | **comp1 만** 원전과 같은 셀 내용 → 격자 직접 대조는 comp1 만 (`HZ-eos-v0-extensive` — f.u. 로 정규화) |
| 격자 | **a = 9.859(2) Å** (296 K) | **a = 10.055 Å** (EOS V₀ 1016.62 Å³ · 0 K) | n/a (원전에 이 조성 없음) | +2.0 % — **방법 (PBE)** 로 읽는다 (§8-②) |
| Li 자리 | 48h (Li1) · 24g (Li2) **부분점유** · 묶음 안 동시점유 불가 | 24 Li 를 **한 배열로 고정** (Li screening 20 개 + UMA 500 K 50 ps 어닐 챔피언 — `db/compositions/comp1.json`) | 27 Li (공공 0.6/f.u.) 를 같은 파이프라인으로 고정 | 원전의 '확률' 을 우리는 '실현 하나' 로 바꿨다 |
| S/X 자리 | Cl: **"fully disordered"** (NMR · 정성) · Br: S2 16 % Br · X 40 % S · I: 질서 | **X 형 4 = Cl 4 · 케이지 4 = S 4 → 교환 0 %** (CIF 직접 셈 §8-③) | **X 형 5 = Cl 5 · 케이지 5 = Cl 3 + S 2** (Cl 의 37.5 % · 케이지 자리의 60 %) | **comp1 = 원전 `Fig. 3a` (I 형 질서) 배열** — 원전이 Li₆PS₅Cl 에 대해 *아니라고* 한 배열 |
| 이완 | — | **고정셀 + 등방 EOS (BM3) → V₀ 에서 이온만** | 〃 | 원전의 평균 구조가 이 규약의 물리적 이유 (§8-④) |
| 이동도 | 정적 ⁷Li 선폭 (130–300 K) | MLIP-MD (UMA) | 〃 | **양이 다르다 → 수치 대조 안 함** (§8-⑤) |
| σ | RT 10⁻²–10⁻³ S cm⁻¹ (예비) | 절대값 비인용 (원장 금지) | 〃 | — |
| 전자구조 | "무색" 결정 (값 없음) | PBE 갭 2.066 eV (fixed-occ nscf) | 2.099 eV | 'wide-gap' 수준 정성만 (§8-⑥) |
| 기계 | **없음** | 우리 탄성 · B₀ 있음 (`our_dft_baseline.md`) | 〃 | 원전에 대조값 없음 — 이 논문을 탄성 출처로 쓰면 오귀속 (`lee2026_lpscl_coating_thickness_ncm811.md` 의 ref 48 사례) |

### 8-② 격자상수 — 우리 PBE EOS 는 원전보다 +2.0 %

| | a (Å) | V / f.u. (Å³) | 조건 |
|---|---|---|---|
| **원전** Li₆PS₅Cl 단결정 | **9.859(2)** | 239.5 | X-선 · 296 K |
| [Rao11] 분말 (밀링 + 550 °C 어닐) | 9.850(4) | — | `rao2011_…` 표 |
| [Kraft] 중성자 Rietveld | 9.8614(1) | — | `kraft2017_…` §3a (SI 정확값) |
| **우리 comp1** (`eos.json` comp1_v3 · V₀ 1016.62 Å³ / 4 f.u.) | **10.0551** | **254.16** | DFT · USPP (li/s/cl v1.4 + P pbe-n-rrkjus = PBE 계) · 52/520 Ry · k444 · 0 K · 분산 보정 기록 없음 |
| 차 (우리 산수) | **+1.99 %** | **+6.11 %** | |

- 세 실험값이 0.01 Å 안에서 모인다 → **실험 기준은 9.85–9.86 Å 로 단단하다.**
- 우리 +2.0 % 는 **방법 차**로 읽는다: PBE (분산 보정 없음) 는 무른 황화물의 격자를 크게 잡는 쪽으로 치우치고, 실험은 296 K (열팽창 포함) 라 0 K 끼리면 차가 조금 더 커진다. **"우리 격자가 실험과 다르다" 를 물리로 쓰지 않는다.**
- ⚠ 무질서 효과는 이 차의 설명이 못 된다 — comp1 (정렬) 과 실험 (무질서) 의 차이는 남지만, 우리 원장의 V/atom 비교 (comp1 → modelc **+0.4 %**, `eos.json` `_normalization_warning`) 를 보면 자리 배열이 부피에 주는 몫은 % 이하 차수다 (조성까지 다른 쌍이라 참고만).
- 쓰는 법 (원고 · SI 한 줄): *"PBE fixed-cell EOS gives a = 10.055 Å for Li₆PS₅Cl, 2.0 % above the single-crystal value at 296 K (9.859 Å)."*

### 8-③ 자리 무질서 — **우리 comp1 은 원전이 "아니다" 라고 한 배열이다** ★

**우리 구조 파일을 직접 셌다** (2026-11-10 · 스크래치 스크립트 · 분류 기준 = 주변 P 배위: X 형 자리 = P 6 개 ≈ a/2 (팔면체) · 케이지 자리 = P 4 개 ≈ a√3/4 (사면체) · 모든 주기 영상 포함):

| 구조 파일 | X 형 자리 | 케이지 자리 | 판정 |
|---|---|---|---|
| `db/structures/comp1_V0_k444.cif` (52 원자 · 정본) | **Cl 4 / S 0** | **Cl 0 / S 4** | **교환 0 % — 완전 정렬** |
| `db/structures/modelc_v3_62atom_V0.cif` (62 원자) | Cl 5 / S 0 | **Cl 3 / S 2** | Cl 8 개 중 **3 개가 케이지** = 화학량론 최소 (X 형이 5 개뿐이라 8 개 중 최소 3 개는 케이지로 가야 한다) |

- **comp1** — 원전 `Fig. 3a` 의 *"S1, S2, and I ordered without any significant mutual substitution"* 을 **Cl 로 그린 것**이다. 원전은 같은 논문에서 Li₆PS₅Cl 을 *"fully disordered"* 라 했고 (³¹P · ³⁵Cl MAS), [Kraft] 중성자는 케이지 자리 Cl **≈ 62 %** 를 쟀다 (그 논문 그림 3c 실독 · SI 정확값은 kraft digest §3a).
  우리 원장은 이걸 이미 알고 있다 — 할로겐 열거 70 배열 중 *Li 를 Rietveld 자리에 고정한 1 단계* 는 2/2 섞인 배열 (#39) 을 골랐지만 Li screening + 어닐 뒤 챔피언은 정렬이었다 (`kb/papers/lpscl_vs_lpscl16_seminar_v1.md` *"comp1 enumeration & champion 역전"* 카드 · `db/compositions/comp1.json` `pipeline_v2`) · 그 카드가 *"우리 0 K champion 은 lower bound"* 라는 caveat 도 달아 두었다.
  ⇒ **0 K 에너지 물성 (갭 · B₀ · 탄성) 의 기준점으로는 방어된다** (`kb/concepts/ordered_vs_disordered.md` §3 — *"0 K 미분·에너지는 ordered 로"*). 그러나 **유한온도 수송의 대표로는 원전 · [Kraft] 와 반대 극단**이다.
- **수송 쪽에서 이것이 뜻하는 것 (가설 · 판정 아님)** — [Klerk] 2016 의 인공 배열 **"all-4a" (Cl 전부 X 형 자리 = 우리 comp1 배열)** 은 AIMD 에서 **inter-cage 점프 0** (케이지 고립 · Li₆PS₅I 와 같은 이유) 이었다 (`deklerk2016_…` §1 · §5). 우리 원장에도 정렬 comp1 셀의 MD 가 **케이지에 갇혔다**는 기록이 있다
  (`canonical_registry.json` `MD_Ea_eV_singleseed@comp1` → `gate_detail` *"6/6 런 전부 케이지 판정"* · 그 β 게이트는 폐기됐고 지위는 **미평가** · `li_transport.json` `disorder_ensemble_2026_06_09` 의 *"Ordered Li₆PS₅Cl is essentially frozen at 600–800 K"* — 같은 파일의 확산영역 게이트 경고로 **수치 인용 보류**).
  원장이 적은 원인은 *"200 ps 부족"* 이다. **원전 + [Klerk] 를 겹쳐 보면 '구조 선택 (정렬 = I 형 배열)' 도 같은 방향의 후보다.** 둘을 가르려면 보고량 카드부터 (CLAUDE.md 계산 규율) — 이 digest 는 판정하지 않는다.
- **modelc** — 케이지 자리 Cl 60 % (3/5) · X 형 자리 Cl 100 %. 같은 계열의 실측 [Adeli] Li₅.₅PS₄.₅Cl₁.₅ 는 **케이지 Cl 83.4 % · X 형 Cl 61.5 %** (중성자 · Adeli 표기 4c = 케이지 · `adeli2019_…` §3a) — 실측은 X 형 자리에도 S 가 38 % 들어가는 **양쪽 섞임**이고, 우리 modelc 는 **넘치는 Cl 만 케이지로 보낸 최소 섞임**이다. 방향 (Cl 과잉 → 케이지 Cl ↑) 은 같고 정도는 다르다.
- ⚠ **"modelc 4d-Cl 12.5 % (1/8)"** (세미나 · `li_transport.json` 등) 는 위 직접 셈과 맞지 않는다 — 이미 `comparison_vs_ours.md` §A · `feng2020_li_deficient_argyrodite_cl_disorder.md` §7d-1 이 *"Li 배위수 Z(Li) 분류기의 산물 · 기하로 다시 세면 3/5"* 로 정정 후보에 올려 두었다. 이번 셈은 **다른 분류기 (P 배위)** 로 같은 3/5 에 닿았다 = 독립 재확인.
- (곁가지 관측 · 우리 산수) comp1 정본 CIF 에서 Cl 부격자와 케이지 S 부격자는 각각 완전한 fcc 지만 **P 부격자에 대해 x 방향으로 평행이동**해 있다 (P→Cl 오프셋 x 성분 0.4215 vs 이상값 0.5 = **0.079a ≈ 0.79 Å** · P→케이지 S 0.7105 vs 0.75 = **0.040a ≈ 0.40 Å**) — 그래서 Cl 의 P 이웃이 이상적 6 × 5.03 Å 대신 4.24 · 5.09 × 4 · 5.81 Å 로 갈린다.
  원전의 X 는 4a 특수 자리에 정확히 앉는다 (평균 구조). 이것이 *"정적 스냅숏은 cubic 이 아니다"* (methods canonical §3-1 · 잔류 편차응력 ±1.3 GPa 기록) 의 원자 수준 모습이다. ⇒ **우리 정적 구조의 Cl–P · Li–Cl 거리를 원전 (CSD) 의 평균 구조 거리와 같은 양으로 비교하지 않는다.**

### 8-④ 고정셀 + EOS 규약의 물리적 원전

`kb/methodology/computational_methods_canonical.md` §3-1 은 *"진짜 Li₆PS₅Cl 이 cubic 인 것은 Li 가 48h/24g 를 동적으로 돌아다녀 시간평균이 cubic 이기 때문"* 이라 적는다.
**그 문장의 실험 원전이 이 논문이다**: Li 는 48h · 24g 를 무질서하게 부분점유하고 (`Fig. 1`) · 한 묶음 (Li1–Li2–Li1) 을 동시에 못 채운다 (§3c) ⇒ **F-43m 은 평균에서만 성립한다.**
정적 DFT 가 Li 배열 하나를 고르면 대칭이 깨지고 (위 §8-③ 곁가지가 실제 크기), vc-relax 는 그 배열의 인공물로 셀을 비튼다 → **등방 스케일 + BM3 로 평균 계량을 부과**하는 것이 우리 규약이다.
- 원고 Methods 에 쓸 때: *"Because Li⁺ statistically occupies the 48h/24g sites of the F-43m average structure (Deiseroth et al., Angew. Chem. Int. Ed., 47, 755 (2008)), any single static Li configuration breaks the cubic symmetry; we therefore fixed the cell shape and optimised the volume through an isotropic E(V) Birch–Murnaghan fit, relaxing ions only."*

### 8-⑤ 이동도 · 전도도 — 수치로 대조하지 않는다

| 이유 | 내용 |
|---|---|
| 양이 다르다 | 원전 = 정적 ⁷Li **선폭** (쌍극자 결합을 평균하는 모든 운동 · 10⁴–10⁵ s⁻¹ 척도 · 130–300 K) · 우리 = MLIP-MD **MSD** (600–1000 K · 장거리) |
| 원전 σ 는 자료가 없다 | 예비 한 문장 (§3f) |
| 우리 쪽 원장 규율 | comp1 MD Ea = `provisional` + **HOLD** (`HZ-comp1-Ea-diffusive-gate` · `cross_composition_ranking` 금지) · σ · D 절대값 비인용 · Ea 도 계 간 상대차로만 |
| 할 수 있는 것 | **방향만**: 원전의 "무질서 Cl · Br = 빠름 / 질서 I = 제한" 과 우리의 "Cl 과잉 쪽이 빠른 방향" 은 같은 레버 (무질서) 를 가리킨다 — 배수는 싣지 않는다 |

### 8-⑥ 전자구조 · 산화 — 원전에는 값이 없다
- 원전의 정보는 **"colorless" 한 단어**다 → 가시광 흡수가 없다 = 광학 갭 ≳ 3 eV 수준 (우리 추론). 우리 PBE 갭 2.066 eV (comp1 · fixed-occ nscf) 는 PBE 과소평가라 **'wide-gap' 정성 일치**까지만 말한다 (CLAUDE.md · baseline 규율).
- 산화 안정성 · ESW: **없음.** *"air-sensitive"* 는 화학 안정성 한마디다.

### 8-⑦ 🔴 우리 원장의 이 논문 인용 — 서지 · 귀속 오류 (→ `comparison_vs_ours.md` §I)

| 위치 | 적혀 있는 것 | 이 PDF 실물 | 판정 |
|---|---|---|---|
| `db/literature/refs.json` `deiseroth2006` | *"Li6PS5X (X=Cl, Br, I): synthesis, crystal structure, ionic conductivity"* · *Angew. Chem. Int. Ed.* **45, 5305 (2006)** · key_content *"4a/4c site S/halogen disorder. Li-X bond lengths."* | 제목 *"Li₆PS₅X: A Class of Crystalline Li-Rich Solids With an Unusually High Li⁺ Mobility"* · **47, 755–758 (2008)** · 투고 2007-08-24 → **2006 일 수 없다** · Wyckoff 4c 표기 없음 · **Li–X 결합 길이 없음** (CSD 기탁분에만) | **서지 오기 + 내용 요약 부정확** (45, 5305 (2006) 이 무엇인지는 실물이 없어 확인 안 했다) |
| 같은 키를 쓰는 곳 | `db/compositions/comp1.json` · `comp2.json` · `modelc_nd_doped.json` `references` · `kb/papers/draft_v1.md` 참고문헌 *"[Deiseroth2006] … 45, 5305 (2006)"* | 위와 같다 | **원고 초안에 틀린 서지가 들어가 있다** |
| `db/properties/adhesion.json` `vacancy_mechanism_consolidated_CORRECTED_2026_05_08` | *"Li6PS5Cl IS superionic (~3 mS/cm at 300 K, Deiseroth 2006)"* · `ionic_conductivity_300K_S_per_cm: 0.003` · `ref: "Deiseroth 2006, …"` | **3 mS/cm 이 없다** — 조성 구분 없는 예비 범위 10⁻²–10⁻³ S cm⁻¹ 뿐 | **유형 A (그 논문이 그 말을 안 했다)** |
| `kb/papers/paper2_FINAL_briefing_2026_05_08.md` · `paper2_briefing_2026_05_08.md` | *"Li6PS5Cl도 superionic — Deiseroth 2006 … ~3 mS/cm 측정"* | 〃 | 〃 |
| ✅ 맞게 쓴 곳 | `db/literature/argyrodite_dft_littable.csv` 1 행 · `argyrodite_lpscl_lit_values_2026_06_21.md` (a = 9.859 Å · DOI anie.200703900) · 세미나 v1 의 *"Angew. Chem. Int. Ed., 47, 755 (2008)"* | 일치 | — |

- 조치 제안 (**사용자 결정** — 이 digest 는 원장 파일을 고치지 않았다): 서지를 **H.-J. Deiseroth, S.-T. Kong, H. Eckert, J. Vannahme, C. Reiner, T. Zaiß, M. Schlosser, Li₆PS₅X: A class of crystalline Li-rich solids with an unusually high Li⁺ mobility, Angew. Chem. Int. Ed. 47 (2008) 755–758. https://doi.org/10.1002/anie.200703900** (BML 양식) · 덱은 *Angew. Chem. Int. Ed.*, 47, 755 (2008). (랩 표준) 으로 · 3 mS/cm 은 이 논문에서 떼고 **실측 출처**로 (예 [Rao11] 1.9 mS cm⁻¹ · [Adeli] x = 0 냉간압축 2.5 mS cm⁻¹ — 각자 조건을 같이 적는다).

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | Li₆PS₅I 단위포 일부 (PS₄ 사면체 · 고립 S2 4 곳 · I 모서리/면) + 면공유 S₃I₂ 이중 사면체 안의 Li1 (48h) · Li2 (24g) · Li1 묶음 (실독) | **평균 구조 · 동시점유 불가** 의 원전 그림 — 우리 고정셀 + EOS 규약 설명 (§8-④) · 발표용 구조 도식 출처 |
| 2 | 정적 ⁷Li FWHH vs T, 세 판 (Cl □ · Br ○ · I △) · x 130–300 K · y 0–6000+ Hz · 판당 17 점 — **픽셀 판독 51 점** (`digitized.csv`) · `figure-read ≈` Cl 6350→730 · Br 4780→500 · I 6160→1240 Hz | "이동도" 주장의 **유일한 정량 근거** · 국소 vs 장거리 구분 불가의 교보재 · ⚠ 130 K 점 vs 본문 140 K (§11-③) · T½ Cl 175 · I 158 · Br ≤ 159 K (우리 산수) |
| 3a,b | P 둘레 배위와 S/X 자리 섞임 — a) I 질서 · b) Br: S2/Br2 (84/16 %) · S3/Br3 (40/60 %) 부채꼴 표시 (실독) | **우리 comp1 = `Fig. 3a` 형 (질서) 배열** (§8-③) · Br 정량 점유율 (화학량론 닫힘 문제 §3b) |
| 4 | ³¹P MAS — Cl 넓은 덩어리 (85.1 · 83.6 · 81.6) · Br 날카로움 93.7 (27 ± 2 %) + 넓음 (92.6 · 91.0) · I 단일 96.3 ppm · x 100→75 ppm (실독) | "Cl 완전 무질서 · Br 혼재 · I 질서" 의 NMR 근거 · ⚠ x 축 100 ppm 끝 → Br 102 ppm 약신호는 축 밖 · Cl 95 ppm 약신호 안 보임 (§11-⑦) |
| 5 | ³⁵Cl (−78) · ⁷⁹Br (109 날카로움 25 % + −40 넓음 75 %) · ¹²⁷I (188 + 384 불순물) MAS · x +1000→−1000 ppm (재크롭 후 실독) | Br 질서/무질서 분율의 두 번째 핵 근거 (³¹P 27 % 와 일치) · 사중극자 핵 caveat (§11-⑥) |

---

## 10. Post-processing ★

| 무엇 | 도구 | 수치화 · 기록 방식 |
|---|---|---|
| 단결정 구조 정련 | **SHELXL-97** (F²) · 수치 흡수 보정 **X-RED 1.19** (결정 면 기술) | R1 · wR2 · GooF · Flack · 변수 수를 ref 26 각주에 · 좌표는 **CSD 기탁** (418488–418490) |
| Li 자리 찾기 | **차이 Fourier 합성** | 세 자리 ≈ 1 e Å⁻³ (서술값) |
| 자리 점유 | 정련 점유율 (Br) | 백분율만 (84/16 · 40/60 · 1–2 %) · 표준편차 없음 |
| ⁷Li 이동도 | 정적 스펙트럼의 **반치폭 (FWHH)** vs T | `Fig. 2` 만 · 숫자표 없음 · 선폭 추출법 (적합/직독) 미기재 |
| 질서/무질서 분율 | MAS 스펙트럼 **봉우리 면적 적분** | ³¹P 27 ± 2 / 73 ± 2 % · ⁷⁹Br 25 / 75 % |
| 전도도 | 임피던스 (방법 미기재) | 범위 한 줄 |
| **(우리)** `Fig. 2` 판독 | `tools/litdb/deiseroth2008_readout.py` — 1-bit 스텐실 래스터 추출 (크기 · ImageMask 가드) → 축 · 눈금 선형 보정 (잔차 x 0.40 · y ≤ 0.43 px) → 연결성분 마커 (크기 거름 · y 축 걸침 마커 복원) | `litdb/figures/deiseroth2008_li6ps5x_argyrodite_high_li_mobility/digitized.csv` (51 행 · 열 `figure, compound, marker, T_K, FWHH_Hz, x_px, y_px, note`) · `--selftest` 양성 2 + 음성 4 (잘못된 크기 거부 · 눈금 빠짐 거부 · 옮긴 마커를 옮긴 대로 읽기 · 글자 크기 성분 거부) · 일부러 깨서 빨간불 확인 (크기 거름 30 px · 걸침 복원 끔) |

---

## 11. 비판 — 이 논문의 약한 곳 ★

① **σ 는 근거가 없다.** "예비 측정" · 조성 구분 없음 · 온도 · 방법 · 그림 0. 후속 측정과 비교하면:
   [Rao11] (밀링 + 어닐) Cl **1.9 × 10⁻³** · Br **6.8 × 10⁻³** · I **4.6 × 10⁻⁷ S cm⁻¹** → Cl · Br 은 10⁻³ 차수로 맞지만 **I 는 3–4 자릿수 아래**다.
   화학량론 Li₆PS₅Cl 의 litdb 실측은 1–4 mS cm⁻¹ 대 ([Rao11] 1.9 · [Adeli] x = 0 냉간압축 2.5 · [Zuo] 2.9) 이고, **10⁻² 끝을 받치는 화학량론 기록은 이번에 찾지 못했다** (litdb 전수 검색은 안 했다).
   같은 그룹의 2011 후속은 Li₆PS₅Cl 실온 **≈ 10⁻⁶ S cm⁻¹** 이었다는 2 차 기록이 있다 (`lynch2026_greenkubo_mlip_conductivity_thesis.md` §3e — 그 학위논문의 재수록 그림 `figure-read` · 원문 litdb 미보유).
   ⇒ 원전의 σ 문장은 **"초기 시료에서 높은 값이 나왔다는 보고"** 이상으로 쓰지 않는다.

② **"이동도" = 선폭.** 정적 ⁷Li 선폭은 쌍극자 결합을 평균하는 **모든** 운동 (48h–48h 왕복 · 케이지 안 · 케이지 간) 을 합쳐서 본다. 그래서:
   - "Br 이 가장 빠르다" 는 선폭 잣대로는 맞다 (T½ 최저 · 실온 잔류 선폭 최저). [Rao11] 의 σ 순서 (Br > Cl) 와도 맞는다 — 그러나 [Kraft] 는 Cl · Br 이 비슷하고 최대가 Cl₀.₅Br₀.₅ 라 했다 = **시료 · 공정에 따라 Cl/Br 순서는 바뀐다.**
   - 같은 잣대로 **I 의 첫 단 (T½ ≈ 158 K) 이 Cl (≈ 175 K) 보다 먼저** 온다 (우리 산수) — 그런데 I 의 σ 는 Cl 보다 3–4 자릿수 낮다. **선폭 순위 ≠ σ 순위.** 논문은 I 의 "제한된 운동" 을 언급해 반쯤 이것을 인정한다 · [Klerk] 가 원인을 줬다 (I = 48h–48h 초고속 왕복만 · inter-cage 0).

③ **`Fig. 2` 의 130 K 점** — 본문은 140 K 가 *"lowest accessible temperature"* · 실험절은 *"140–300 K"* 인데 그림에는 Cl · Br 의 130 K 점이 있다 (`figure-read ≈` 129.9 · 130.0 K · x 축도 130 K 에서 시작). 결론 (Br 경직 미도달) 은 안 바뀌지만 **그림과 본문 중 하나는 틀렸다.**

④ **Br 점유율이 화학량론으로 안 닫힌다** (§3b · Br 0.80–0.84/f.u.) · 점유율 표준편차 · 제약 조건 미기재 · 단결정 하나 (질서/무질서 영역이 섞인 시료에서 고른 결정) 의 값이라 대표성도 모른다.
   참고: 후속 [Kraft] 그림 3c (실독) 에서 Br 의 S²⁻ 자리 할라이드 분율은 **중성자 ≈ 22 % · X-선 PDF ≈ 13–14 %** 다 — **X-선 계열 (원전 16 % 포함) 이 중성자보다 낮게 나오는 경향**이 Kraft 자신의 그림 안에서도 보인다. 무질서 % 는 **측정법 의존**이다.

⑤ **Li 자리 정련의 자기모순** — 본문 *"Both these positions could be refined significantly for the title compounds"* ↔ ref 26 *"Li2 could not be refined"* (Cl). Li 는 전자 3 개라 X-선에 약하다. 후속 [Kraft] 중성자가 답을 줬다: **Li₆PS₅Cl 의 24g 점유 = 0** (I 는 0.22) — Cl 에서 Li2 가 안 잡힌 것은 실패가 아니라 **실제로 비어 있어서**였을 가능성이 크다.
   d(Li1–Li1) ≈ 115 pm (I) 도 X-선 · 높은 표준편차의 값이다 — [Kraft] 중성자 그림 4 는 I 의 48h–48h ≈ **1.31 Å** (우리 픽셀 판독) 이다.

⑥ **"Cl 완전 무질서" 는 정성이다.** ³¹P 가 넓다 · ³⁵Cl 이 넓다 → 무질서. 그러나 ³⁵Cl · ⁷⁹Br · ¹²⁷I 는 **사중극자 핵**이라 넓음에는 국소 대칭 저하 · 사중극자 상호작용도 섞인다 (논문 미분리) · "완전 무질서" 는 50/50 과 62/38 ([Kraft]) 을 못 가른다.

⑦ **S1 할라이드 약신호 (102 · 95 ppm)** 는 그림에서 안 보인다 (§3e) — 본문 서술 + "불순물일 수 있다" 라서 **아무 결론도 받치지 못한다.** 결론 ("S1 할라이드는 매우 적다") 은 X-선 쪽이 받친다.

⑧ **상순도 주장** — "standard X-ray powder diagrams did not show contamination" · 패턴 없음. 후속 [Kraft] 중성자는 Li₆PS₅Cl 에서 Li₃PO₄ 6.6 % · LiCl 1.2 % 를 정련했다 (다른 시료 · 다른 합성 — 원전 시료가 불순했다는 뜻은 아니고, **분말 X-선만으로는 그 수준을 못 본다**는 뜻).

⑨ 사소한 것: Li₆PS₅I 의 Flack **−0.035(5)** 는 0 보다 7σ 아래 (물리적 범위 0–1 밖 · 논의 없음) · 반지름 표의 출처 미기재 · 좌표가 본문에 없어 (CSD 기탁) 독자가 결합 길이를 못 본다.

---

## 12. 후속 연구가 이 원전의 무엇을 고치거나 넓혔나 ★

| 후속 (digest) | 원전의 어느 고리 | 고친 것 / 넓힌 것 |
|---|---|---|
| **[Rao11]** Rao & Adams 2011 (`rao2011_argyrodite_se_studies_bvse.md`) | 합성 · σ | **7 일 → 20 h 밀링 + 5 h 어닐** · **조성별 σ 첫 측정** (Cl 1.9 · Br 6.8 × 10⁻³ · I 4.6 × 10⁻⁷ S cm⁻¹ = 원전 범위는 I 에 안 맞는다) · 격자 9.850(4) / 9.980(8) / 10.142(3) Å (원전과 ≤ 0.01 Å) · 원전 단결정 모델 + Pecher 2010 NMR Li 분포를 BV 격자에 넣어 경로 위계 (케이지 안 vs 케이지 간) |
| 같은 그룹 2011 후속 (litdb **미보유** · 2 차로만) | σ · 확산 경로 | `lynch2026_…` §3e: Li₆PS₅Cl 실온 ≈ 10⁻⁶ S cm⁻¹ (재수록 그림 `figure-read`) · `morgan2021_…` §2-B: *"type 5 쌍만으로는 장거리 불가 — 비-type-5 사면체를 거쳐야 한다"* 를 이미 지적 (ref 45) |
| **[Klerk]** de Klerk 2016 (`deklerk2016_…`) | ②–③ 연결 ("I 만 질서 · 제한 운동") | AIMD 52 원자 · 300–600 K: **I 는 inter-cage 점프 0** (모든 T) · 48h 쌍 왕복만 초고속 → 원전 I 의 2 단 좁아짐의 미시 원인 · **Cl 인공 배열 "all-4a" (= 우리 comp1) 도 inter-cage 0** · 무질서 4a/4c 분포가 거시 확산의 필요조건 · 최적은 내부점 (450 K · 75 %) |
| **[Kraft]** Kraft 2017 (`kraft2017_…`) | ③ Cl 정량 · Li 점유 | **중성자로 Cl 무질서 첫 정량 ≈ 62 %** (원전 *"No quantitative information … Li₆PS₅Cl"* 을 메움) · Br ≈ 22 % (X-선 PDF ≈ 13–14 % — 원전 16 % 와 같은 쪽) · I 0 % · **Li 48h 0.500 (Cl) → 0.391 (I) · 24g 0 (Cl) → 0.219 (I)** = 원전 Cl 의 Li2 정련 불가를 설명 · 점프 거리 (그 논문 그림 4 픽셀 재판독: 48h–48h Cl ≈ 1.97 → Br ≈ 1.61 → I ≈ 1.31 Å) · 격자 무름 ↔ σ (원전엔 없는 축) |
| **[Adeli]** Adeli 2019 (`adeli2019_…`) | ③ 을 조성으로 | 원전은 화학량론 셋뿐 → **Li₆₋ₓPS₅₋ₓCl₁₊ₓ** 로 Cl 을 늘려 무질서 **61 → 83 %** · σ 2.5 → 9.4 mS cm⁻¹ (냉간압축) — 우리 modelc 조성의 실측 이웃 |
| **[Morgan21]** Morgan 2021 (`morgan2021_…`) | ① 의 사면체 구멍 | 원전의 "136 사면체 구멍 = P 4 + 나머지 132" 를 **type 0–5 로 분류** (4 + 16 + 48 + 4 + 16 + 48 = 136 · 우리 산수로 원전 수와 일치) · Li 는 type 5 · 2 · 4 만 점유 · 무질서가 type 2 점유를 늘려 장거리를 연다. ⚠ Morgan digest 는 그 분류를 *"Deiseroth 분류 (ref 36)"* 라 부른다 — **이 2008 원전에는 type 분류가 없다** (ref 36 의 서지는 digest 에 없어 확인 못 했다) |
| **[Zhu15]** (`zhu2015_esw_grand_potential_origin.md`) | ① 구조를 계산 입력으로 | Li₆PS₅Cl 만 MP-id 가 없어 **원전 구조의 정렬 배열**에 자체 DFT → E_hull 83 meV/atom (정렬 단일 배열 값이라 과대 — 그 digest §15) |
| **[Shin26]** (`shin2026_bh4_reorientation_li_transport_li6ps5x.md`) | ② 의 측정법 | 선폭 하나 대신 **SLR · PFG · 2D EXSY** 로 국소 · 장거리를 갈라 재는 현대 NMR 수송 — 원전 §11-② 의 한계를 넘는 방법 |

> ⚠ **kraft2017 digest 정정 1 건 (이번에 발견)** — 그 digest §3d · §5.2 의 *"doublet (48h–48h) ~1.5 → ~1.2 Å"* · *"intra-cage ~2.35 Å (Cl)"* 는 그 논문 그림 4 픽셀 재판독 (y 눈금 6 개 선형 보정 · 마커 연결성분 중심) 과 다르다: **doublet Cl ≈ 1.97 · Br ≈ 1.61 · I ≈ 1.31 Å · intra-cage Cl ≈ 2.25 · I ≈ 2.55 Å · inter-cage Cl ≈ 2.77 · I ≈ 3.32 Å** (inter-cage 는 그 digest 와 맞다). [Klerk] 본문의 doublet 1.9 Å (Cl) 와도 재판독 쪽이 맞는다. kraft digest 에 정정 주석을 달았다 (옛 값은 취소선으로 남김).

---

## 13. 적용 인사이트 (우리 연구에 어떻게) ★

① **comp1 의 이름표를 정확히 단다.** comp1 은 "Li₆PS₅Cl" 이지만 자리 배열로는 **원전 `Fig. 3a` (I 형 정렬)** 이다. 0 K 에너지 물성 (갭 · B₀ · 탄성) 에는 기준점으로 쓰되, 발표 · 원고에서 **"ordered Li₆PS₅Cl (X-site Cl, 0 % site exchange)"** 로 부르고 실험의 무질서 (원전 NMR · [Kraft] 62 %) 와의 차이를 한 줄로 적는다.

② **comp1 MD 의 '케이지' 해석에 구조 후보를 하나 더 둔다.** 원장은 "200 ps 부족" 을 원인으로 적었다. 원전 (Cl = 무질서) + [Klerk] (all-4a = inter-cage 0) 를 겹치면 **"정렬 배열이라 장거리가 꺼졌다"** 도 같은 방향이다. 다시 볼지는 사용자 결정이다 — 연다면 보고량 카드 §1–3 에 *"comp1(정렬) vs comp1(실측 무질서 ≈ 62 % 앙상블)"* 을 먼저 선언한다. 이 digest 는 판정하지 않는다.

③ **고정셀 + EOS 규약의 근거 문장을 원전으로 단다** (§8-④ 영문 초안). 지금 규약 문서는 이유를 우리 말로만 적고 있다 — 리뷰어가 물으면 1 차 문헌이 있다.

④ **격자 한 줄 검증** (§8-②): PBE +2.0 % 는 방법 지문이다. SI 의 "computational details" 에 실험 a 와 나란히 적으면 독자가 우리 셀을 믿는 근거가 된다 (절대 격자를 물리 결론으로 쓰지 않는다).

⑤ **원장 서지 정정** (§8-⑦) — 원고 초안 (`draft_v1.md`) 에 틀린 서지가 들어가 있다. 2026-07 Kim/Cui 교훈 (로컬 PDF 기준 · 인용 역할 확인) 의 재현 사례다.

⑥ **"이동도" 라는 말을 쓸 때 국소 / 장거리를 가른다.** NMR 선폭 · 쌍 왕복 · MSD 초기 구간은 국소 운동에도 반응한다 — 원전의 I 가 그 함정의 교과서다.

---

## 14. 인용 가능 문장 (영문 초안 · deck/paper 용)

- "Li₆PS₅X (X = Cl, Br, I) adopts the cubic argyrodite structure (F-43m), in which Li⁺ statistically occupies the 48h and 24g sites and neighbouring Li positions cannot be occupied simultaneously (*Angew. Chem. Int. Ed.*, 47, 755 (2008))."
- "Single-crystal X-ray diffraction gives a = 9.859(2) Å for Li₆PS₅Cl at 296 K (*Angew. Chem. Int. Ed.*, 47, 755 (2008)); our PBE fixed-cell equation of state yields 10.055 Å, a 2.0 % overestimate typical of PBE."
- "S²⁻ and halide ions share the two free-anion sites in Li₆PS₅Br (S2 site: 84 % S/16 % Br; X site: 40 % S/60 % Br) and appear fully disordered in Li₆PS₅Cl by ³¹P/³⁵Cl MAS NMR, whereas Li₆PS₅I is ordered (*Angew. Chem. Int. Ed.*, 47, 755 (2008))."
- ⛔ 쓰지 않는 문장: *"Deiseroth et al. reported σ = 10⁻² S cm⁻¹"* · *"Li₆PS₅Br is the best conductor (Deiseroth 2008)"* (선폭 순위다) · *"Deiseroth 2008 reported ~3 mS cm⁻¹ for Li₆PS₅Cl"* (없다) · *"… elastic modulus (Deiseroth 2008)"* (없다).

---

## 15. 주의 / 한계 (인용 규율)

- **σ**: 원전의 σ 는 인용하지 않는다 — 인용하려면 "preliminary, no data shown" 을 같이 적는다.
- **이동도 순위**: NMR 선폭 순위로만 쓴다 ("⁷Li line narrowing occurs at the lowest temperature in Li₆PS₅Br") · σ 순위로 옮기지 않는다.
- **무질서 %**: Br 의 16 / 40 % 는 **단결정 X-선 · 화학량론 미닫힘** 표지를 같이 · Cl 은 **정성** ("fully disordered" — 수치 없음) · 정량이 필요하면 [Kraft] 중성자 ≈ 62 % (측정법 명시).
- **Li–Li 115 pm**: Li₆PS₅I 한정 · X-선 · 높은 표준편차.
- **`figure-read ≈`** 표지 (§3d 판독값) 를 떼지 않는다 · 130 K 점은 본문과 어긋난다는 주석을 같이.
- **우리 값과 나란히 놓을 때**: 격자 (comp1 만 · f.u. 정규화 · PBE 방법 명시) 외에는 **수치 대조 없음** — MD 절대값 · comp1 MD Ea (HOLD) 는 싣지 않는다.
- **자리 라벨**: 원전은 고립 S²⁻ 자리를 Wyckoff 문자로 부르지 않는다 — 인용문에 "4c" · "4d" 를 넣을 때는 **누구의 세팅인지** 적는다.

---

## 16. 기법 용어 미니사전

- **argyrodite**: 광물 Ag₈GeS₆ 의 이름이자 그 구조형. 음이온이 **사면체 밀집** (Laves 상 MgCu₂ 위상) 을 이루고, 그 사면체 구멍에 작은 양이온이 (일부는 질서, 일부는 무질서로) 들어간다. Ag/Cu 판은 오래전부터 초이온 전도체로 알려져 있었다.
- **사면체 밀집 (tetrahedral close packing)**: 원자를 쌓았을 때 빈틈이 **사면체 구멍만** 생기게 하는 배열 (Frank–Kasper 형). Li₆PS₅X 단위포의 음이온 24 개가 구멍 136 개를 만든다.
- **Wyckoff 자리 (4a · 4b · 48h · 24g …)**: 공간군의 대칭이 같은 자리끼리 묶은 이름. 숫자 = 단위포 안의 자리 수. F-43m 에서 4a·4b·4c·4d 는 각각 4 자리 (Z = 4 라 f.u. 당 1 개), 48h 는 48 자리 (Li 24 개가 반쯤 채운다).
- **부분점유 (partial occupancy)**: 결정학이 주는 것은 **시공간 평균 전자밀도**다. "48h 점유 0.5" 는 "이 자리에 Li 가 있을 확률 1/2" 이지 반쪽 Li 가 아니다 (`kb/concepts/ordered_vs_disordered.md` §5).
- **차이 Fourier 합성**: 측정 회절 세기와 모델 세기의 **차이**를 다시 실공간으로 바꾼 지도. 모델에 빠진 전자밀도 (예: 가벼운 Li) 가 봉우리로 보인다.
- **R1 · wR2 · GooF**: 정련 품질 지표. R1 = 관측 구조인자와 계산값의 상대 차 (작을수록 좋다, 0.02–0.05 면 우수) · wR2 = F² 기준 가중판 · GooF ≈ 1 이면 오차 모델이 맞다.
- **Flack 매개변수**: 반전 중심이 없는 구조 (F-43m) 에서 **절대 구조** (거울상 중 어느 쪽인지) 를 판정. 0 = 맞는 쪽 · 1 = 뒤집힌 쪽 · 0.5 = 쌍정. 물리적 범위는 0–1.
- **정적 NMR 선폭 · 쌍극자 결합**: Li 핵들은 작은 자석이라 서로의 자기장을 느낀다 (⁷Li–⁷Li 쌍극자 결합). 원자가 멈춰 있으면 이 결합이 공명선을 넓힌다 (경직 선폭, 여기서 ≈ 6000 Hz).
- **운동 좁아짐 (motional narrowing)**: Li 가 뛰는 속도가 경직 선폭 (각진동수 2π × 6000 ≈ 4 × 10⁴ s⁻¹) 보다 빨라지면 쌍극자 결합이 시간평균돼 선이 좁아진다. **어떤 운동이든** (제자리 왕복이든 장거리든) 결합을 평균하면 좁아지므로, 선폭만으로는 국소 · 장거리를 못 가른다. 2 단 좁아짐 = 서로 다른 운동이 다른 온도에서 켜진다는 신호.
- **MAS (magic-angle spinning)**: 시료를 54.7° 기울여 kHz 로 돌려 고체 NMR 선을 좁힌다. 회전 속도 간격으로 **회전 측대역**이 생긴다 (`Fig. 5` 의 등간격 작은 봉우리).
- **화학적 이동 δ (ppm)**: 핵 주변 전자가 외부 자기장을 가리는 정도. 같은 원자라도 **이웃 (두 번째 · 세 번째 껍질)** 이 다르면 다른 δ 가 나온다 → 무질서 = 넓은/여러 봉우리 · 질서 = 날카로운 단일선.
- **사중극자 핵 (I > 1/2)**: ³⁵Cl · ⁷⁹Br (3/2) · ¹²⁷I (5/2) 처럼 핵 전하분포가 구형이 아닌 핵. 국소 대칭이 cubic 에서 벗어나면 선이 크게 넓어진다 — 무질서와 대칭 저하가 같은 신호로 섞인다.
- **임피던스 분광 (impedance spectroscopy)**: 교류 주파수를 훑으며 저항 · 축전 성분을 분리해 이온전도도를 잰다. bulk · 입계 · 전극 반원을 가르려면 주파수 범위 · 온도 · 등가회로가 필요하다 — 원전에는 그 어느 것도 없다.

---

## 🗨️ Q&A 로그

*(아직 없음)*
