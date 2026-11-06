<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-11-06 작성: 크로핑 25장(본문 7 + SI 17 + 표 1) 중 18장을 실제로 보고(+ Fig. 1 쪽 렌더) figure-read 값과
     그림↔본문 어긋남을 넣었다. Fig. S2 는 SI 에 박힌 원본 이미지(1069 px)를 픽셀 단위로, Fig. 6c 삽입 지도 두 장은
     픽셀 비교로 확인했다. 우리 쪽 값은 db/properties/canonical_registry.json · citation_hazards.json 규율 안에서만 적었다. -->

# Dendrite-tolerant fast-kinetics design for all-solid-state lithium-metal batteries via site-specific customized sulfide electrolytes — Kang, Lee et al. (*Energy Storage Materials* **90** (2026) 105335) — **[우리 그룹]**

> slug `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` · DOI `10.1016/j.ensm.2026.105335` · type `exp (원자단위 계산 0 — DFT·MD·NEB·grand-potential 없음)` · PDF 업로드 `78401219-12._Dendrite-tolerant_fast-kinetics_design…pdf` (본문 12 pp) + `86130ab7-12._Sup_Dendrite-tolerant…pdf` (SI 18 pp: Fig. S1–S17 · Table S1 · Supplementary Note 1) · digested `2026-11-06` · status ✅ · 태그 **[우리 그룹]**
> elements: Li, P, S, O, Cl, Ni, Co, Mn
> methods: XPS, Raman, ESW

> **저자**: **Junhee Kang**ᵃ† · **Yeokyung Lee**ᵃ† (공동 1저자) · Tae Young Leeᵃ · Gwangseok Ohᵇᶜ · **Sang-Cheol Nam**ᵇᶜᵈ\* · **Ohmin Kwon**ᵇᶜᵉ\* · **Jong-Won Lee**ᵃᶠ\*\* — ᵃ 한양대 신소재공학부 · ᵇ RIST (포항산업과학연구원) · ᶜ POSCO Holdings LiB Materials Research Center (POSCO N.EX.T Hub) · ᵈ POSCO Future M 기술연구소 · ᵉ 한양대 ERICA 재료화학공학과 · ᶠ 한양대 배터리공학과. 접수 2026-03-13 · 수정 2026-05-31 · 수리 2026-06-25 · 온라인 2026-06-26. 지원 POSCO Holdings · KEIT (20026760) · NRF (RS-2025-00512708). 데이터: 요청 시.
> **[우리 그룹]** = 한양대 Jong-Won Lee 연구실 (교신 3인 중 1). ⚠ 우리 계산 담당(안용훈)은 저자가 **아니다** — `[자체·공저]` 가 아니라 `[우리 그룹]` 이다 (선례 `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`). 공동 1저자 **Yeokyung Lee** 는 우리 `[Lee26Mech]` = `papers/lee2026_mechanical_halogen_argyrodite_drycoating.md` (*ACS Nano* 2026, 안용훈 제2저자) 의 1저자와 같은 사람이고 **AFM-FS 프로토콜 문장이 글자 그대로 같다** — 그래서 이 편은 우리 그룹 내부 재현성을 재는 자료가 된다 (§7b-④).
>
> **계보**: 우리 그룹 [Kang25] (ref [5], 고전압 기생반응) · TLM 임피던스 분리 Kim/Kang/Park/Lee *Electrochim. Acta* 542, 147413 (2025) (ref [45] — 이 논문 `Fig. 3c–e` 의 방법) · 공동 교신 Nam/Kwon (RIST·POSCO) 의 **결정학적 자리 선택 연작** — ref [24] Park *ESM* 75, 104078 (2025) *"site-selective oxygen introduction"* · ref [43] Park *eScience* 6, 100502 (2026) *"oxygen-induced lithium inter-cage conduction"* · ref [44] Park *Carbon Energy* 7, e70058 (2025) *"site-specific Nb doping"*. ⚠ **세 편 모두 litdb 에 digest 없음** (§12-①).

---

## 0. 이 digest 를 읽는 법 — 먼저 읽을 것 다섯

1. **제목의 "site-specific" 은 *셀 안의 위치* 다 — 결정학적 자리가 아니다.** 양극 촉매질(catholyte) · 분리막 · Li 계면 중간층 셋에 **서로 다른 SE 를 배정**한다는 뜻이다. 결정학적 자리 서술은 논문 전체에 **두 문장**뿐이다.
   - ① *"Rietveld refinement performed on LPSC and LPSOC (Fig. S2) confirms that O²⁻ anions occupy a portion of S²⁻ at the 16e position"* — **실험 (lab Cu Kα XRD + GSAS-II)**. 그런데 `Fig. S2` 는 적합 곡선 · 격자상수 · R 인자만 보여주고 **O 점유율 · 좌표 · 4a/4d 대안 모델 비교가 하나도 없다** (§10-①).
   - ② *"Cl⁻ substitution for S²⁻ at the 4d sites"* — **문헌 인용 [39–41]** 뿐, 이 논문의 측정이 아니다.
   - **DFT 로 자리를 정한 곳은 없다.** ⇒ CEI 트랙의 **Nd 자리 근거로는 0** 이다 (Nd 가 없다). O 자리에 대해서만 실험 한 점을 보탠다 (§7b-⑫ · §12-①).
2. **계산이 0 이다.** DFT · AIMD · MLIP · NEB · grand-potential · Bader 어느 것도 없다. *"Li₃PO₄ 띠틈 7.4 eV"* 도 인용값 [36,38] 이다 ([38] 은 흑연 음극 **액체 전해질** 논문). → §8 은 짧다.
3. **조성 대응**: `LPSC` = Li₆PS₅Cl = 우리 **comp1** 명목 · `LPSC₁.₆` = Li₅.₄PS₄.₄Cl₁.₆ = 우리 **modelc 와 명목 조성이 정확히 같다** · `LPSOC` = Li₆PS₄OCl (x = 1, Cl 1.0 모체) **≠ 우리 lpsocl** (Li₂₇P₅S₂₁OCl₈ = Li₅.₄PS₄.₂O₀.₂Cl₁.₆, Cl 1.6 모체에 O 0.2/f.u.). `M-SE` = LPSC₁.₆ (3 µm) : LPSOC (1 µm) = **4 : 1 질량비** 혼합 중간층.
4. **온도 표기**: `Fig. 2e` 축 이름은 σ_ion,**RT** 지만 같은 값 2.70 · 2.33 이 분리막 절에서 **"at 30 °C"** 로 다시 나오고, `Fig. 2d` 의 1000/T = 3.30 점 (30 °C) 이 ln σ ≈ −5.92 → 2.69 mS cm⁻¹ 로 맞는다. ⇒ **이 논문의 "RT" σ 는 30 °C 값이다.** 셀 시험 온도는 그림마다 다르다 — 양극 비교 30 °C · Li 대칭셀 45 °C (및 RT) · 풀셀 45 °C (및 RT). 전압은 전부 **vs Li/Li⁺** (Li–In 셀도 환산 표기).
5. **본 digest 에서 실제로 본 그림 (2026-11-06)**: `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. S1` `Fig. S2` `Fig. S4` `Fig. S5` `Fig. S9` `Fig. S11` `Fig. S12` `Fig. S13` `Fig. S14` `Fig. S15` `Fig. S16` `Fig. S17` — **18장** (+ `Fig. 1` 은 쪽 렌더로만 · 모식도). 확대 판독: `Fig. 2a`(x = 1 선) · `Fig. 2b` · `Fig. 2e` · `Fig. S2`(SI 임베디드 원본 1069 px 픽셀 판독, LPSC/LPSOC 대조) · `Fig. 3f,g` · `Fig. 5a,c,d,e,f` · `Fig. 6c` 삽입 지도 두 장 픽셀 비교 · `Fig. 7c,e`.
   안 본 것: `Fig. S3` (SUS 대칭 Nyquist) · `Fig. S6` (양극 Nyquist) · `Fig. S7` (등가회로 — 캡션은 PDF 텍스트) · `Fig. S8` (사이클 전 XPS) · `Fig. S10` (사이클 뒤 XRD) · `Table S1` (이미지 대신 PDF 텍스트로 전 셀 복원). 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산한 값은 *우리 산수*.

---

## 1. 한 줄 요약

전고체 Li 금속 전지에서 **한 가지 SE 로 세 계면을 다 만족시킬 수 없다**는 전제 위에 층마다 SE 를 따로 고른다 — **양극 촉매질 = O 치환 LPSOC (≈1 µm)** (100 사이클 뒤 R_int 74.0 → **47.3 Ω cm²**), **분리막 = Cl-rich LPSC₁.₆ (3 µm, 30 °C 5.49 mS cm⁻¹)** (1C 이상 용량 우위 — 단 `figure-read ≈` +2–6 mAh g⁻¹), **Li 계면 = M-SE** (45 °C CCD **3.5 mA cm⁻²** vs LPSC 1.7 · 표면 기공비 0.148 → **0.070** · AFM-FS E 14.6 GPa) → NCM811 ‖ Li 풀셀 **1C 500 사이클 (45 °C · 20 MPa) 단락 없음** (159.7 → ≈132.6 mAh g⁻¹) · RT 1C 100 사이클 85.5 %.

⚠ **같은 설계의 2C 셀은 ≈350 사이클에서 단락됐다** (`Fig. 7c` 라벨 *"Short-circuited"*) — 본문은 이를 *"stable cycling was sustained up to 350 cycles"* 로 쓴다. "dendrite-tolerant" 는 **"단락 시점을 늦춘다"** 까지가 데이터가 받치는 범위다 (§10-②). 그리고 이 데이터에서 CCD 를 가르는 변수는 **강성이 아니라 LPSOC 의 유무**다 (§6 — 가장 단단한 LPSC₁.₆ 의 CCD 가 LPSC 와 같다).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 셀 | NCM811 (COSMO AM&T) ‖ SE ‖ Li 금속 (비교 단계에선 Li–In) · PEEK 몰드 Ø10 mm · 운전 스택압 20 MPa |
| 던지는 질문 | 촉매질 (산화·계면 안정) · 분리막 (이온전도) · Li 계면 (전기화학 + 기계 강건) 의 **서로 다른 요구**를 한 SE 조성으로 타협하지 말고 **층마다 따로 맞추면** 고율·장수명이 되나 |
| 문헌 갭 (저자 주장) | 기존은 (a) SE 단일 조성 최적화 (O 치환 [24–26] · 할로겐 [39–41]) 또는 (b) SEI 개질 · 계면 공극 축소 중 **하나** [16,37] — "세 계면 동시" 는 없다 |
| 설계 3단 | (i) LPSOC 촉매질 ≈1 µm — PS₃O 사면체로 산화 안정 + "Li₃PO₄ 계 계면상" (ii) LPSC₁.₆ 분리막 3 µm — 높은 σ (iii) M-SE 중간층 — 작은 LPSOC 가 큰 LPSC₁.₆ 사이 공극을 메움 + Li₃PO₄ SEI + 높은 탄성률 |
| 메커니즘 3줄 (저자 결론) | ① 공극 채움 → Li⁺ 플럭스 균질화 ② 계면상 화학 (Li₃PO₄) → 전자 절연 ③ 강성 → 침투 저항 — "collectively" |
| 확장 주장 | Li 합금 · Si 음극에도 적용 가능 (데이터 없음) |

---

## 3. 핵심 수치 총정리 ★

### 3a. SE 물질 · 수송 (`Fig. 2`, `Fig. S2`, `Fig. S5`)

| 물성 | x = 0 (LPSC) | x = 0.5 | x = 1 (LPSOC) | x = 1.75 | 조건 / 출처 |
|---|---|---|---|---|---|
| 격자상수 a (Å, Rietveld) | **9.850** | — | **9.844** | — | `Fig. S2` (GSAS-II · Cu Kα) · 본문 p.4 |
| Rietveld R_exp / R_wp / R_p / GOF | 7.39 / 8.04 / 6.22 / **1.49** | — | 7.34 / 9.79 / 7.32 / 1.33 | — | `Fig. S2` · ⚠ LPSC GOF 1.49 ≠ R_wp/R_exp 1.09 (§10-①) |
| 2차상 | 없음 | 없음 | 본문 "단일상" · ⚠ `Fig. S2` 원본에 ≈22.0 / 23.0 / 24.6° 약한 반사 (§5.1) | **잔류 전구체** 22.1° · 23.0° · 34.7° (본문) | `Fig. 2a` · `Fig. S2` |
| σ (30 °C, mS cm⁻¹) | **2.70** | 2.58 | **2.33** | 1.50 | `Fig. 2e` 라벨 · ⚠ x = 0 막대는 `figure-read ≈` 3.05 높이 (§10-④) |
| Ea (eV) | **0.22** | 0.23 | **0.26** | **0.30** | `Fig. 2f` · 20–60 °C 5 점 · ln σ vs 1000/T · 오차막대 `figure-read ≈` ±0.01 (정의 미기재) |
| 홉 수 검산 (ν₀ 10¹³ s⁻¹ 가정 · 303 K) | Γ ≈ 2.2×10⁹ s⁻¹ · 대기 ≈ 0.45 ns | — | Γ ≈ 4.8×10⁸ s⁻¹ · ≈ 2.1 ns | Γ ≈ 1.0×10⁸ s⁻¹ · ≈ 9.7 ns | `tools/sei/collect_neb.py::hop_check` · 차수 검산 (확산계수·전도도 아님) — ns 대기라 "빠른 전도" 서술과 모순 없음 |

| LPSC₁.₆ (Li₅.₄PS₄.₄Cl₁.₆ = 우리 modelc 명목) | 20 °C | 30 °C | 40 °C | 50 °C | 출처 |
|---|---|---|---|---|---|
| σ (mS cm⁻¹) | 4.79 | **5.49** (본문 "5.5") | 6.99 | 10.06 | `Fig. S5` (SUS 대칭 · 고주파 절편 `figure-read ≈` 22 → 10 Ω) |
| *우리 산수* — 구간 기울기 Ea | 20→30 °C **0.104 eV** | 30→40 °C **0.198** | 40→50 °C **0.317** | 한 직선 적합 **0.200** | ⚠ **비-아레니우스** (§10-⑤) — 논문은 LPSC₁.₆ Ea 를 보고하지 않는다 |

- **tender XAS** (NSLS-II 8-BM TES, `Fig. 2g`): P K-edge — LPSOC 백색선 (≈2147 eV) 만 약간 높다 (O 전기음성 → P 비점유 상태↑ 해석) · LPSC₁.₆ 는 ≈2151.5 eV 두 번째 봉우리가 LPSC 보다 높다 (`figure-read` · 본문 언급 없음) · S K-edge 세 시료 거의 같다 · **Cl K-edge 는 LPSOC 만 주봉우리가 `figure-read ≈` 1 eV 고에너지 쪽 + 2833–2838 eV 진동** (본문: PS₃O 형성 → 비대칭·비점유 DOS↑).
- **입자 크기**: 합성 직후 입자는 x 와 무관하게 `figure-read ≈` **2.5–3.5 µm** (`Fig. S1` 네 장 · `Fig. S4` LPSC₁.₆ 한 장 — **각각 입자 1 개 사진**). 촉매질은 "~1 µm 로 분쇄" (본문) — **분쇄 뒤 분말 사진 · 입도분포 (D50) 가 어디에도 없다** (§10-⑦).

### 3b. 양극 — 촉매질 비교 (NCM811 ‖ Li–In, 30 °C, `Fig. 3`, `Table S1`)

| 항목 | x = 0 (LPSC) | x = 0.5 | x = 1 (LPSOC) | 조건 |
|---|---|---|---|---|
| 0.1C 첫 방전 (mAh g⁻¹) | **184.0** | `figure-read ≈` 197 | **206.4** | `Fig. 3a` · 첫 충전 `figure-read ≈` 218 / 220 / 228 → 첫 CE ≈84 / 90 / 90 % (*우리 산수*) |
| 0.5C 100 사이클 | `figure-read ≈` 139 → 110 (≈79 %) | `≈` 170 → 131 (≈77 %) | `≈` 174 → 145 · 본문 유지율 **84.6 %** | `Fig. 3b` · 개선의 대부분이 **첫 0.5C 용량 차 (≈35 mAh g⁻¹)** 이고 감쇠율 차는 ≈5 %p (§10-⑥) · 사이클 1 의 점 (`≈`173 / 191 / 193) 은 `Fig. 3a` 0.1C 값과 달라 조건 불명 |
| R_Ohmic (Ω cm², 0 → 100 cyc) | 23.6 → 25.8 | 26.1 → 26.5 | 20.5 → 21.9 | `Table S1` (TLM, 충전 상태) |
| R_ion | 1.1 → 1.6 | 1.2 → 1.6 | 1.3 → 1.5 | ″ — **양극 이온저항은 1–2 Ω cm² 로 미미** |
| **R_int** | 17.7 → **74.0** | 16.4 → 67.5 | 14.1 → **47.3** | ″ — 핵심 지표 |
| **R_w** | 62.2 → **142.0** | 53.2 → 89.5 | 53.7 → **71.6** | ″ — 142.0 − 71.6 = **70.4** (본문 "70.4 Ω cm² 감소" 와 일치) |
| CPE_int C (mF s^(η−1) cm⁻²) / η | 1.06 → 0.08 / 0.52 → 0.51 | 7.87 → 0.07 / 0.56 → 0.54 | 7.20 → 1.42 / 0.54 → 0.54 | ″ |

| XPS (100 사이클 뒤 양극, `Fig. 3f,g`) | 본문 값 | 그림 판독 |
|---|---|---|
| S 2p PS₄³⁻ | 161.3 / 162.5 eV | 두 성분 — ⚠ 스핀-궤도 짝 규칙 위반 (§10-③) |
| S 2p Li₂Sₙ (n > 1) / P₂S_y (y > 5) | 162.7 / 163.4 eV | `figure-read ≈` 163.1 / 164.0 eV (그림이 본문보다 0.4–0.6 eV 높다) |
| P 2p PO₄³⁻ (Li₃PO₄ · P–O–S) | 134.5 eV | x = 0 `≈`134.2 (뚜렷) · x = 1 `≈`134.4 (**아주 작다**) |
| 사이클 전 | "산물 미미, 차이 없음" (`Fig. S8` — 안 봄) | — |
| 원자료 포락선 | — | x = 0 S 2p 는 ≈163 eV 중심의 **평평하고 넓은 봉우리** · x = 1 은 ≈161.6 eV 날카로운 봉우리 + ≈162.8 어깨 → **"LPSOC 가 PS₄³⁻ 를 더 남긴다" 는 원자료 수준에서 보인다** |

| CV (`Fig. S9` · SE : Super P = 9 : 1 vs Li · 2.0–4.5 V · 0.05 mV s⁻¹) | x = 0 | x = 1 |
|---|---|---|
| 겉보기 산화 개시 | `figure-read ≈` **2.45 V** | `figure-read ≈` **2.55 V** |
| 어깨 (≈3.0 V) | `≈`18 µA | `≈`12 µA |
| 주봉우리 (≈3.5 V) | `≈`35 µA | `≈`28 µA (**0.8×**) |
| 4.0–4.5 V 평탄 | `≈`31 µA | `≈`26 µA — **둘 다 4.5 V 까지 계속 산화** |
| 정규화 | **전류 µA 그대로** (전극 질량·면적 미기재) · 단일 측정 | |

### 3c. 분리막 — 이온전도도와 rate (`Fig. 4` · NCM–LPSOC ‖ X ‖ Li–In · 30 °C · 20 MPa)

| 분리막 (σ 30 °C) | 0.1C | 0.2C | 0.5C | **1C** | **2C** | 0.5C 복귀 |
|---|---|---|---|---|---|---|
| LPSC (2.70) | `≈`190 | `≈`179 | `≈`165 | `≈`**154.5** | `≈`**141** (→ 135 하강) | `≈`165 |
| LPSOC (2.33) | `≈`193 | `≈`180 | `≈`166 | `≈`**153** | `≈`**137.5** | `≈`162 |
| LPSC₁.₆ (5.49) | `≈`192 | `≈`181 | `≈`168 | `≈`**160** | `≈`**143** | `≈`164 |

- 전부 `figure-read ≈` (mAh g⁻¹). LPSC₁.₆ 의 LPSC 대비 우위: **1C +5.5 · 2C +2** — ⚠ **율속이 분리막 σ 라면 2C 에서 차이가 더 커져야 하는데 줄었다** (§10-⑥). `Fig. 4b` 는 y 축을 끊은 (broken axis) 막대라 차이가 시각적으로 부풀려진다.

### 3d. Li 계면 (Li ‖ SE ‖ Li 대칭셀 · SE 0.1 g · 400 MPa 냉간압축 · 스택 20 MPa)

| 항목 | LPSC | LPSC₁.₆ | LPSOC | **M-SE** | 조건 / 출처 |
|---|---|---|---|---|---|
| M-SE 혼합비 고르기 | — | — | — | 8:1 / **4:1** / 2:1 → 벌크 절편 `≈`35 / 36.5 / 43 · 계면 호 `≈`25–30 / **14.5** / 21 Ω cm² | `Fig. S11` (RT · 세로 오프셋 그림) |
| 혼합비별 분극 (0.5 mA cm⁻², 45 °C, 150 h) | — | — | — | 8:1 `≈`±22→±33 · **4:1 `≈`±12–13** · 2:1 `≈`±17–20 mV | `Fig. S12` |
| 갓 만든 셀 — 고주파 절편 → 호 끝 (Ω cm²) | `≈`38 → 62 | `≈`29.5 → 70 (**호 폭 최대 ≈40**) | `≈`42 → 59 | `≈`37 → 51 | `Fig. 5a` (RT · 계열마다 세로 위치가 다르다 — 오프셋으로 보임) |
| 1 일 숙성 뒤 호 끝 (증가) | `≈`80 (**+18**) | `≈`82 (+12) | `≈`74 (+15) | `≈`61 (+10) | `Fig. 5a` · ⚠ 본문은 LPSC₁.₆ 의 *"relatively large rise"* — 그림에선 LPSC 가 더 크다 (§10-⑮) |
| 0.5 mA cm⁻² (0.5 mAh cm⁻²) 45 °C 250 h 분극 | `≈`±20 mV | `≈`±25 → ±31 (상승) | `≈`±14 | `≈`±12 | `Fig. 5c` 왼쪽 |
| 2.0 mA cm⁻² (2.0 mAh cm⁻²) 45 °C | `≈`±75–80 mV → **≈17–20 h 단락** | — | — | `≈`±40 mV · **250 h 안정** | `Fig. 5c` 오른쪽 |
| **CCD 45 °C** (0.1 mA cm⁻² 단계 · 단계당 1 h) | **1.7** (본문) / 1.8 (그림 라벨) | **1.8** (본문) / 1.7 (그림 라벨) | **3.1** | **3.5** | `Fig. 5d` · ⚠ 본문↔그림 값이 **뒤바뀌어** 있다 (§10-⑧) |
| **CCD RT** | **1.4** (그림만) | — | — | **1.9** | `Fig. 5e` |
| 문헌 대비 (RT CCD) | — | — | — | 1.9 vs [59] `≈`1.87 · [58] `≈`1.52 · [55]·[57] `≈`1.5 · [17] `≈`1.4 · [56] `≈`1.1 | `Fig. 5f` · ⚠ 그림 참고문헌 번호가 본문 [15, 54–58] 과 다르다 (§10-⑨) |
| Raman (Li/SE 계면, 사이클 뒤) | 없음 | — | (사이클 뒤 미측정) | **≈940 cm⁻¹** (본문) · `figure-read ≈`950 · 주 PS₄ 봉우리의 **수 %** 크기 | `Fig. S13` · 사이클 전 LPSOC · LPSC₁.₆ 에 이 대역 없음 |
| P 2p XPS (Li/SE 계면) | — | — | — | 24 h 접촉 → 환원 P (≈130 eV) 만 · 5 사이클 → **134.3 eV (Li₃PO₄)** = `figure-read` **포락선의 몇 % 인 작은 성분** | `Fig. S14` (어느 SE 인지 캡션 미기재 — 본문 맥락상 M-SE) |
| Li₃PO₄ 띠틈 | — | — | — | **7.4 eV** | **인용값** [36,38] — 이 논문의 측정·계산 아님 |

### 3e. 미세구조 · 기계 (`Fig. 6`, `Fig. S15`, `Fig. S16`)

| 항목 | LPSC | LPSC₁.₆ | LPSOC | M-SE | 조건 |
|---|---|---|---|---|---|
| SEM 표면 기공비 (void ratio) | **0.148** | **0.125** | — | **0.070** | `Fig. 6a` · 회색조 → 이진화 (방법 원전 [59]) · **시료당 사진 1 장** · 문턱 미기재 |
| AFM-FS 영률 E (GPa) | **10.5 ± 0.2** | **15.1 ± 0.4** | **13.4 ± 0.4** | **14.6** | `Fig. 6c` · `Fig. S15` (히스토그램 최빈값 · **30 GPa 에서 절단**) · `Fig. S16` |
| 참고 | Li 금속 E ≈ 5 GPa | | | | 인용 [60] (Xu 2017 *PNAS*) |
| 프로토콜 | Park NX-10 · 드라이룸 · Si 탐침 PPP-NCHR · PinPoint FS · **256 × 256 px / 5 × 5 µm** (SI Note 1) ↔ 본문 **"2 µm × 2 µm scan area"** · `Fig. 6c` 지도 축척 500 nm (≈2.2 µm 폭) · `Fig. S16` 지도 축척 **3 µm** (≈9 µm 폭) | | | | ⚠ 세 숫자가 서로 다르다 (§10-⑩) |

### 3f. 풀셀 (NCM811 ‖ Li · 2.5–4.25 V · 20 MPa · `Fig. 7`)

| 구성 | 온도 · rate | 첫 1C 방전 | 결과 | 출처 |
|---|---|---|---|---|
| (a) NCM–LPSC ‖ LPSC ‖ Li | 45 °C · 1C | **149.0** | `figure-read ≈` 118 까지 감쇠 뒤 **≈108 사이클 단락** (본문 "within 100 cycles") | `Fig. 7a` |
| (b) NCM–LPSOC ‖ LPSC₁.₆ ‖ Li | 45 °C · 1C | **167.3** | **147 사이클 뒤 급락** → 단락 라벨 · CE `≈`30–50 % (연성 단락) | `Fig. 7b` |
| (c) NCM–LPSOC ‖ LPSC₁.₆ ‖ M-SE ‖ Li | 45 °C · **1C** | **159.7** (초록) | **500 사이클 ≈132.6** · 단락 없음 | `Fig. 7c` |
| ″ | 45 °C · **2C** | `figure-read ≈` 141 | `≈`124 (≈348 cyc) → **≈350 사이클 단락** (그림 라벨) | `Fig. 7c` · 본문 "stable … up to 350 cycles" |
| (d) 이중층 (LPSC₁.₆ + M-SE) | **RT** · 1C | `figure-read ≈` 158 | **100 사이클 85.5 %** (그림 문구) · 로딩 9.3 mg cm⁻² | `Fig. 7d` |
| (d) 대조 NCM–**LPSC** ‖ LPSC₁.₆ ‖ Li (캡션) | RT · 1C | `≈`153 | `≈`15–25 사이클에 무너짐 | `Fig. 7d` · ⚠ 대조의 촉매질이 LPSC — 변수 두 개가 같이 바뀐다 (§10-⑥) |
| 문헌 대비 (RT 100 사이클 이상) | — | — | [34] 0.2C `≈`8.8 · [57]/[62]/[63]/[64] 0.5C `≈`1.8 · [54] 1C `≈`6.4 · **본 연구 1C 9.3 mg cm⁻²** | `Fig. 7e` · ⚠ [64] 는 참고문헌에 없다 (총 63 편) · [34] 는 DFT 전용 논문 (§10-⑨) |

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부

### 4a. 합성
- 원료: Li₂S (Alfa Aesar 99.9 %) · P₂S₅ (Sigma-Aldrich 99 %) · LiCl (Sigma-Aldrich > 99.0 %) · **Li₃PO₄ (Junsei 98 %) = O 공급원**.
- ZrO₂ 용기 · Ar 글러브박스 밀봉 · 유성 볼밀 Fritsch PULVERISETTE 5 · **400 rpm 10 h**.
- ⚠ 본문은 *"mechanical milling **and subsequent solid-state synthesis**"* 라 쓰지만 **열처리 온도·시간이 본문·SI 어디에도 없다** · 초록은 *"synthesized via high-energy ball milling"* (§10-⑦).
- 조성: Li₆PS₅₋ₓOₓCl (x = 0, 0.5, 1, 1.75) · Li₅.₄PS₄.₄Cl₁.₆ "같은 공정" (`Fig. S4`).
- 촉매질은 "~1 µm 로 분쇄" (방법 미기재) · 분리막 LPSC₁.₆ "3 µm".

### 4b. 셀
- 복합양극: NCM811 : SE : Super P = **72 : 27 : 1** (wt) 볼밀 혼합 · 로딩 **9.3 mg cm⁻²** (복합양극 기준) · SE 층 위에 얹어 **400 MPa**.
- 상대극: In 100 µm + Li 200 µm (Li–In) · RT 1C 풀셀은 **Li 50 µm** · 45 °C 풀셀의 Li 두께는 미기재.
- 집전체 SUS 10 µm 양쪽 · 풀셀 조립 150 MPa · 운전 스택압 **20 MPa**.
- 대칭셀: SE **0.1 g** · 400 MPa 냉간압축 · Li 양면 · 20 MPa. ⚠ 펠릿 두께·밀도 미기재. *우리 산수*: 진밀도 1.64 g cm⁻³ · 상대밀도 85 % 가정이면 두께 ≈0.91 mm, LPSC 벌크 R·A (25 °C) ≈38 Ω cm² — `Fig. 5a` 의 LPSC 고주파 절편 (≈38) 과 맞는다.
- 층 구성 (분리막 + 중간층) 의 각 층 질량·두께 **미기재**.

### 4c. 전기화학
- 사이클: 2.5–4.25 V vs Li/Li⁺ · 45 °C · 첫 사이클 0.1C CC–CV (CV 컷 = CC 전류의 20 %) 충전 / CC 방전. ⚠ 1C 의 mA g⁻¹ 정의 미기재.
- EIS: Bio-Logic SP-300 · 7 MHz–10 mHz · 5 mV.
- CCD: **0.1 mA cm⁻² 간격 · 단계당 1 h**. 단락과 전압 발산 중 무엇을 CCD 로 셌는지 미기재.
- CV: SE : Super P = 9 : 1 작업전극 · Li 상대극 · 2.0–4.5 V · 0.05 mV s⁻¹.
- 양극 EIS = **TLM 등가회로** (`Fig. S7`: r_ion · r_int · cpe_int · z_w 분포 소자) — 우리 그룹 ref [45] 의 방법.

### 4d. 분석
- SEM FEI Verios G4UC · XRD Bruker D8 ADVANCE Cu Kα 2° min⁻¹ · Rietveld GSAS-II · XPS Thermo ESCALAB 250Xi (Al Kα) · tender XAS (P · S · Cl K) NSLS-II 8-BM TES (폴리이미드 테이프 + S-free Mylar 봉지) · Raman (기종 미기재) · AFM Park NX-10 (드라이룸 · PinPoint FS · PPP-NCHR).
- 기공비: SEM 회색조 → 이진 지도 → 공극 면적 분율 (원전 [59] Jung 2023 *AFM*).

### 4e. 이론
- **없다.** 메커니즘 서술의 근거는 전부 인용: PS₄₋ₙOₙ 강화 [29,30] · Li₃PO₄ 저전자전도 [36,38] · Cl 4d 치환 → Li cage 연결 [39–41] · Li₃PO₄ 7.4 eV [36,38] · Li E ≈ 5 GPa [60] · SE 전자전도 10⁻⁹ mS cm⁻¹ 이하면 덴드라이트 완화 [23].

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 O 치환 사다리 — 구조 (`Fig. 2a–c`, `Fig. S1`, `Fig. S2`)
- x 가 늘면 XRD 봉우리가 고각으로 이동 → 격자 수축이라 해석. `figure-read`: `Fig. 2b` 의 (311) · (222) 봉우리가 x = 0 → 1 에서 **≈ +0.08–0.10°** 움직인다 (30.09 → 30.17° · 31.44 → 31.54°).
- Rietveld (`Fig. S2`) — **a = 9.850 → 9.844 Å** (Δa = −0.006 Å = −0.06 %). 본문: O²⁻ 가 16e 의 S²⁻ 일부를 대체 · `Fig. 2c` 는 16e 꼭짓점을 S/O 공유로 그린 모식도.
- ⚠ **두 숫자가 안 맞는다** (*우리 산수*, Cu Kα 1.5406 Å): x = 0 봉우리는 a ≈ 9.842–9.849 Å 로 Rietveld 와 맞지만 x = 1 봉우리는 a ≈ **9.817 Å** 를 준다. Rietveld Δa 라면 (311) 이동은 +0.019° 여야 하는데 보이는 이동은 그 **≈5 배**다. 내부표준이 없으니 시료 높이 오차가 봉우리를 옮겼고 정련이 영점/변위 항으로 흡수했을 수 있다 — 그러면 **"뚜렷한 이동 = 격자 수축" 서술은 정량 근거를 잃는다** (§10-①).
- x ≥ 1.75 에서 잔류 전구체 봉우리 (본문 22.1° · 23.0° · 34.7°) → **O 고용 한계**. `Fig. 2a` 의 x = 1.75 에는 별표가 다섯 개 (≈22 · ≈22.5 · ≈27 · ≈33.5 · ≈34.7°).
- ⚠ **x = 1 (LPSOC) 에도 같은 자리에 약한 반사가 있다**: `Fig. S2` 임베디드 원본에서 LPSOC 패턴만 (200) 18.0° 와 (220) 25.6° 사이에 작은 봉우리 셋 (≈22.0 · 23.0 · 24.6°) 이 있고, **LPSC 패턴은 같은 구간이 평평하다**. F-43m argyrodite 는 이 각도에 허용 반사가 없다. 계산 (빨간) 곡선이 이 봉우리를 따라가고 차이 (파란) 곡선이 평평하다 = **정련에 2차상이 들어가 있는 것으로 보이는데 상분율이 보고되지 않았다**. `Fig. 2a` 의 x = 1 선에도 ≈22.1 · 23.1° 에 희미한 혹 (`figure-read`, 잡음 경계).
  - 반대 증거: 사이클 전 LPSOC Raman (`Fig. S13` 왼쪽) 에 Li₃PO₄ 대역 (≈940–950 cm⁻¹) 이 **안 보인다** → 잔류상이 있어도 소량이다.

### 5.2 O 치환 사다리 — 수송 (`Fig. 2d–f`, `Fig. S3`)
- 20–60 °C 5 점 아레니우스 (`Fig. 2d`): x = 1.75 만 기울기가 확연히 가파르다 · x = 0 · 0.5 · 1 선은 거의 겹친다.
- σ (30 °C) 2.70 → 2.58 → 2.33 → 1.50 · Ea 0.22 → 0.23 → 0.26 → 0.30 eV. 저자: "x = 1 까지 효과적, 그 너머는 구조·수송 열화".
- *우리 산수* (`Fig. 2d` 기울기): x = 0 ≈0.23 · x = 1.75 ≈0.31 eV — 막대 라벨과 맞는다.
- ⚠ `Fig. 2e` 의 x = 0 막대는 ≈3.05 높이로 그려져 있다 (라벨 2.70 · `Fig. 2d` 와 본문은 2.70 쪽). 막대만 보면 x = 0 → 1 감소가 −24 % 로 보이지만 실제는 **−14 %** (§10-④).

### 5.3 XAS — O·Cl 치환의 국소 구조 (`Fig. 2g`)
- P · S K-edge 큰 변화 없음 · LPSOC 의 P 백색선 (≈2147 eV) 약간↑ · Cl K-edge LPSOC 2833–2838 eV 진동 → PS₃O 형성에 따른 비대칭·비점유 DOS↑ 로 해석 (인용 [43,44] — 공동 교신 그룹 선행).
- `figure-read`: LPSOC Cl K-edge 주봉우리가 ≈1 eV 고에너지로 이동 · 2835–2838 eV 에 골. **O 가 16e (P 결합) 에만 있다면 Cl 주변 변화는 간접이어야 하는데 Cl edge 변화가 P edge 보다 크다** — 저자 해석과 모순은 아니지만 O 일부가 자유 음이온 자리 (4a/4d, Cl 과 공유) 쪽에 있는 경우도 배제하지 못한다. 자리 판정엔 쓰지 않는다.
- LPSC₁.₆: 단일상 XRD (`Fig. S4` 관련 본문 서술) · σ 5.5 mS cm⁻¹ (`Fig. S5`).

### 5.4 양극 — 촉매질 O 치환 효과 (`Fig. 3`, `Fig. S6–S10`, `Table S1`)
- Li–In 상대극 (Li 금속 부반응 배제) + 30 °C (열 가속 배제) 로 양극만 본다고 밝힌다.
- 0.1C 첫 방전 184.0 → 206.4 mAh g⁻¹ (x = 0 → 1) · 저자: 첫 사이클 고전압 SE 산화분해·계면 열화 억제.
- 0.5C 100 사이클 LPSOC 84.6 %. `figure-read`: 첫 0.5C 사이클부터 x = 0 ≈139, x = 0.5 · 1 ≈170–174 — **35 mAh g⁻¹ 차이가 0 사이클에 이미 있다.**
- TLM 분해: R_ion 은 거의 그대로 (1–2 Ω cm²) · **R_int 74.0 (LPSC) vs 47.3 (LPSOC)** · R_w 70.4 Ω cm² 감소 → "계면 열화 완화가 활물질 확산 동역학을 보존" 해석.
- XPS (`Fig. 3f,g`): LPSOC 쪽이 PS₄³⁻ 를 더 남긴다 — 원자료 포락선 모양으로 확인된다. 성분 분해는 신뢰하기 어렵다 (§10-③).
  - ⚠ **PO₄³⁻ 는 LPSC 양극 (`Fig. 3f`) 이 LPSOC 양극 (`Fig. 3g`) 보다 크다.** 저자는 이 phosphate 를 "비균일·저항성 산물" 로 읽는데 (p.5), 같은 논문 p.3 은 "LPSOC 산화분해로 생긴 Li₃PO₄ 계 계면상이 저전자전도라 추가 분해를 억제한다" 고 쓴다 — **같은 종이 한 쪽에선 보호막, 한 쪽에선 열화 산물**이다 (§10-⑪).
- CV (`Fig. S9`): LPSOC 가 산화 봉우리 낮고 개시가 양 (+) 으로 이동 → "~4.5 V 고전압 운전 가능성". `figure-read`: 개시 이동 ≈0.1 V · 전류 0.8× · **둘 다 2.5 V 부근부터 4.5 V 까지 계속 산화한다** — "4.5 V 적용 가능" 은 이 CV 가 받치지 않는다 (§10-⑫).
- 사이클 후 XRD (`Fig. S10` — 안 봄): NCM811 · LPSOC 봉우리 보존 (본문).

### 5.5 분리막 — σ 와 rate (`Fig. 4`)
- 분리막 LPSC / LPSOC / LPSC₁.₆ (σ 30 °C 2.70 / 2.33 / 5.49) · 0.5C 까지 같다 · 1C · 2C 에서 LPSC₁.₆ 우위 → "고 σ 분리막이 고속충전에 결정적".
- `figure-read`: 우위는 **1C ≈+5.5 · 2C ≈+2 mAh g⁻¹** (LPSC 대비) — 작고, 율이 오를수록 줄어든다 (§10-⑥).

### 5.6 Li 계면 — M-SE 혼합비 (`Fig. S11`, `Fig. S12`)
- 8:1 / 4:1 / 2:1 → 4:1 이 8:1 보다 계면저항 낮고 2:1 보다 벌크저항 낮다 → 4:1 채택. 세 점 · 셀 하나씩.

### 5.7 Li 계면 — 대칭셀 비교 (`Fig. 5`)
- `Fig. 5a,b`: LPSC₁.₆ 는 벌크 R_ion 이 낮은데도 **계면저항이 크다** (`figure-read` 호 폭 ≈40 vs LPSC ≈24 · LPSOC ≈17 · M-SE ≈14 Ω cm²) · 본문은 숙성 중 증가도 크다고 하지만 **그림에선 LPSC (+18) 가 LPSC₁.₆ (+12) 보다 더 자란다** (호 끝 기준, §10-⑮). DRT 는 긴 시정수 (계면) 가 지배. M-SE 는 작은 LPSOC 가 LPSC₁.₆–Li 사이 공극을 메워 접촉 면적↑ + Li₃PO₄ SEI 로 해석.
  - DRT 는 3D 원근 폭포 그림이라 봉우리 높이를 계열 간에 비교할 수 없다 · 숙성 전/후 어느 스펙트럼의 DRT 인지 캡션에 없다.
- `Fig. 5c`: 0.5 mA cm⁻² — M-SE 최저 분극 (LPSOC 와 거의 같다) · 2.0 mA cm⁻² — LPSC 는 ≈17–20 h 단락 · M-SE 250 h 안정.
- Raman ≈940 cm⁻¹ (Li₃PO₄) · XPS P 2p 134.3 eV (5 사이클 뒤 · 24 h 접촉만으로는 없음) → "Li₃PO₄ 는 Li–LPSOC 전기화학 반응으로 *in situ* 생성" · "전자 절연체로 덴드라이트 억제".
- CCD 45 °C: LPSC 1.7 · LPSC₁.₆ 1.8 · LPSOC 3.1 · M-SE 3.5 (본문) · RT: M-SE 1.9 (LPSC 1.4 는 그림에만).
  - `figure-read` 실패 모양이 다르다: LPSC · LPSC₁.₆ · M-SE 는 전압이 0 근처로 **붕괴 (단락)**, LPSOC 는 −60 mV 너머로 **튀고 불규칙** (접촉 상실형) — CCD 정의 (단락 vs 전압 발산) 미기재.
  - RT 의 LPSC (`Fig. 5e`) 는 분극이 **비대칭** (+75 vs −25 mV) 이고 반주기 안에서 전압이 계속 오른다 = **박리 쪽 공극 형성** 신호 — "덴드라이트" 만의 실패가 아니다. M-SE 의 공극 채움 서사와는 오히려 잘 맞는다.
  - ⚠ CCD 셀의 분극이 **옴 하한 아래**다 (§10-⑯): 45 °C · 0.5 mA cm⁻² 단계에서 LPSC `figure-read ≈`±5–6 mV — 논문 자신의 `Fig. 5a` 절편 (≈38 Ω cm², RT) 과 `Fig. 2d` σ(T) 로 환산한 45 °C 벌크만의 하한은 ≈11–12 mV (*우리 산수*). 같은 조건의 사이클 셀 (`Fig. 5c`) 은 ≈±20 mV 로 하한 위다.
- `Fig. 5f`: RT CCD 1.9 가 문헌 최고 수준 — 최근접 [59] ≈1.87 과 차가 **0.03 mA cm⁻²** 로 **측정 단계 (0.1) 아래**다.

### 5.8 미세구조 · 기계 (`Fig. 6`, `Fig. S15`, `Fig. S16`)
- 기공비 0.148 / 0.125 / **0.070** (SEM 1 장씩).
- AFM 지형 (`Fig. 6b`): M-SE 표면이 더 매끈 · ⚠ 그림 패널은 **LPSC · LPSOC · M-SE** 인데 캡션은 *"LPSC, LPSOC, and LPSC₁.₆"* · 본문은 *"smoother … than those of LPSC and LPSC₁.₆"* — 셋이 서로 다르다 (§10-⑩).
- AFM-FS E: LPSC 10.5 · LPSOC 13.4 · LPSC₁.₆ 15.1 · M-SE 14.6 GPa — "O 치환 · S/Cl 무질서로 강성↑ [36,40]" · Li ≈5 GPa 보다 높으니 침투 저항.
  - 🔴 **`Fig. 6c` 의 LPSC₁.₆ 패널 삽입 지도는 LPSC 지도와 같은 그림이다** — 지도 안 라벨이 "LPSC" 이고 선택 사각형 11 개의 위치 · 청록 줄무늬까지 같다 (픽셀 비교: 평균 절대차 14.5/255, 다른 지도와는 40.8). F–d 곡선 (시작 힘 ≈0.43 vs ≈0.57 µN) 은 다르다. LPSC₁.₆ 15.1 GPa 의 근거는 `Fig. S15` 히스토그램뿐이다 (§10-⑩).
  - `Fig. S15`: 세 분포 모두 오른쪽 꼬리가 길고 **30 GPa 에서 잘렸다** (LPSOC 는 30 GPa 칸에도 ≈20 카운트) · 보고값은 적합 곡선의 **최빈값** (평균 아님) · ± 는 적합 오차로 보인다 (정의 미기재) · 카운트 축 상한 400 / 100 / 150 → 시료마다 표본 수가 다르다.
- 결론 3줄: 공극 채움 → Li⁺ 플럭스 균질화 · 계면상 화학 → 전자 절연·계면 안정 · 강성 → 침투 저항.

### 5.9 풀셀 (`Fig. 7`, `Fig. S17`)
- 단계 비교 (45 °C, 1C): (a) LPSC 단독 → 단락 · (b) LPSOC 촉매질 + LPSC₁.₆ 분리막 → 첫 용량 149.0 → 167.3 · 147 사이클 뒤 실패 · (c) + M-SE → 500 사이클 ≈132.6 · 단락 없음. 저자 역할 배분: 촉매질 = 양극 계면 · LPSC₁.₆ = rate · **M-SE = 장수명의 핵심**.
- ⚠ (b) → (c) 에서 첫 1C 용량은 **167.3 → 159.7 (−4.5 %)** — M-SE 를 넣으면 초기 용량이 준다 (셀 하나씩이라 셀 간 편차일 수도 있다). 본문은 *"any additional transport penalty … is negligible"* (§10-⑥).
- 2C: ≈350 사이클 **단락** (그림) — 본문 *"stable cycling was sustained up to 350 cycles"* · 결론 *"remained operable up to 350 cycles even at 2C"* · 또 다른 문장 *"cycling stability over 300 cycles at 2C"*.
- `Fig. S17` (1C 500 사이클 뒤 Li/M-SE 단면): 저자 "치밀·균일, 필라멘트·공극·단락 경로 없음". `figure-read`: SEM 축척 **20 µm** — 서브 µm 필라멘트는 이 배율에서 안 보인다 · **S EDS 지도는 계면 위 ≈20 µm 띠가 S 결핍인데 P 지도는 균일** — argyrodite 라면 P · S 는 같이 다녀야 한다. 언급 없음 (§10-⑬).
- RT 1C 100 사이클 85.5 % (로딩 9.3 mg cm⁻²) · 대조 (NCM–LPSC ‖ LPSC₁.₆ ‖ Li) 는 ≈15–25 사이클에 무너짐 · `Fig. 7e` 문헌 대비 1C × 9.3 mg cm⁻² 가 최고.
- 온도 논의: 45 °C 는 이온전도·계면 동역학↑로 Li 도금/박리 안정, 그러나 양극 부반응 가속 → RT 와 45 °C 의 경향이 같다는 점을 설계 유효성 근거로 든다.

---

## 6. 메커니즘 종합 — 저자의 세 기둥과 각각의 증거 강도

| 기둥 | 저자 주장 | 이 논문 안의 직접 증거 | 강도 |
|---|---|---|---|
| ① 공극 채움 | 1 µm LPSOC 가 3 µm LPSC₁.₆ 사이를 메워 Li 계면 치밀 · 플럭스 균질 | 기공비 0.148/0.125 → 0.070 (`Fig. 6a`, 1 장씩) · AFM 지형 (`Fig. 6b`) · 계면 호 폭 (`Fig. 5a`) · RT LPSC 의 박리형 실패 모양 (`Fig. 5e`) | **중** — 방향은 여러 독립 관측이 받친다 · 정량은 단일 이미지 |
| ② 계면상 화학 | LPSOC 가 Li 와 반응해 Li₃PO₄ (7.4 eV) SEI → 전자 절연 → 덴드라이트 억제 | Raman ≈940–950 cm⁻¹ 소봉우리 (`Fig. S13`) · P 2p 134.3 eV 소성분 (`Fig. S14`) · LPSOC 단독 CCD 3.1 (`Fig. 5d`) | **약** — Li₃PO₄ 는 소수 성분 · 다른 주산물 (Li₂S · Li₃P · LiCl · Li₂O) 은 안 봤다 · 전자 절연을 잰 데이터 (σ_e) 없음 · 열역학은 0 V 에서 Li₃PO₄ 를 환원한다 (§7b-⑦) |
| ③ 강성 | M-SE 의 높은 E (14.6 GPa > Li ≈5) 가 침투 저지 | AFM-FS E (`Fig. 6c`, `Fig. S15`, `Fig. S16`) | **약** — 펠릿 표면 접촉강성 · 같은 그룹 같은 프로토콜 재현이 31 % 다르다 · `Fig. 6c` 지도 중복 · 강성↔CCD 상관을 시험하지 않았다 |

> 🔑 **③ 의 내부 반례가 이 논문 안에 있다**: E 순위는 LPSC₁.₆ (15.1) > M-SE (14.6) > LPSOC (13.4) > LPSC (10.5) 인데 CCD 순위는 M-SE (3.5) > LPSOC (3.1) ≫ LPSC₁.₆ (1.8) ≈ LPSC (1.7) 다. **가장 단단한 LPSC₁.₆ 의 CCD 가 LPSC 와 같다** ⇒ 이 데이터에서 CCD 를 가르는 변수는 **강성이 아니라 LPSOC 의 유무**다 (② 또는 ① 쪽). 저자는 셋을 *"collectively"* 로 묶어 이 대조를 흐린다.

---

## 7. 우리 계산과의 대조 ★★ (`../our_dft_baseline.md` · `db/properties/` · `db/properties/citation_hazards.json`)

> 이 논문은 **계산이 0** 이라 "방법 차이" 는 *실험 양 ↔ 우리 계산 양* 의 차이다. 그리고 **우리 쪽 조성 간 순위는 레지스트리가 대부분 막고 있다** — 그것부터 적는다.

### 7a. 먼저 확인한 것 — 우리 쪽에서 *인용 가능한* 방향이 있나

| 축 | 우리 값 (방법) | 레지스트리 · 원장 상태 | 이 논문과 맞춰 볼 수 있나 |
|---|---|---|---|
| Ea · σ (Cl-rich · O 효과) | MLIP-MD (UMA-s-1p1) Ea 기록이 comp1 · modelc · lpsocl 에 각각 있다 (`md-ea-multiseed-v1` · `md-ea-singleseed-anchor-v1` · box331 400 ps gen2) — **값은 레지스트리에서 본다 · 여기 나란히 적지 않는다** | **`HZ-cross-system-Ea` (BLOCKED)** — 계간 Ea 직접 비교 citable:no · single-seed anchor: **`cross_composition_ranking` 금지** · lpsocl multiseed: **provisional · `cite_until_beta_gate_passes`** · modelc box331: **`difference_with_lpsocl_as_O_effect` 금지** | ⛔ **없다.** "우리 MLIP-MD 도 O 가 Ea 를 올린다 / Cl-rich 가 Ea 를 내린다" 를 이 논문 옆에 쓰지 않는다 |
| 탄성 | relaxed-ion DFT E_VRH — comp1 22.06 · modelc 27.66 · lpsocl 35.04 GPa | 세 값이 **서로 다른 comparison_group** (comp1comp2-v1 · modelc-standalone · lpsocl-standalone — "네 조성을 한 묶음으로 자동 순위화 금지") · modelc_2x 전단 기반 G·E 는 **보고 안 함** (`D-2026-11-03-shear-pair-closed`) | ⚠ **방향만 — "검증된 일치" 아님** |
| 산화 onset (축 ①) | grand-potential (MP hull, Li open) — comp1 = modelc **2.256 V** (LiS4·SCl3·Li5PS4Cl2 제외 GG 집합) / 2.14 V (LiS4 포함) · O 단독 대조 Li₅.₄PS₄.₁O₀.₃Cl₁.₆ **2.14 V** (LiS4 포함 집합 · `cei_esw_Li_controls_2026_09_16.json` o_only_03) — 전부 **grand-potential 경계의 Li-rich facet 값** (`HZ-esw-reduction-limit-facet-convention` · 다음 breakpoint 는 LiS4 포함 집합 2.36 V · GG 집합 2.385 V) | 같은 방법 · 같은 규약 · 같은 상 집합 | ✅ 방향 (같은 규약 · 같은 상 집합 안, 대조 한 점) — 실험 개시 전위와 절대값으로 맞추지 않는다 |
| 분해 산물 | 같은 grand-potential (o_only_03 profile) | 같은 방법 | ✅ 산물 종류 |
| SEI 산물 띠틈 | MP PBE (최소 E_hull 항목, 2026-09-13 정정본) — Li₃PO₄ **5.818 eV** (Pmn2₁ · mp-13725 · role **insulator**) | 옛 값 5.73 은 `HZ-sei-gaps-pre-20260913-nonground-polymorph` (CONDITIONAL) — **정정본만** | ✅ **역할 (insulator) 만** |
| Li 수송 장벽 | Li₂S 4×4×4 V_Li⁻ CI-NEB (`HZ-sei-neb-li2s-cc-cellconv` · CONDITIONAL · 고정 문장으로만) · Li₃Nd 2×2×2 (`HZ-li3nd-neb-si-conditional` · SI 전용 · 다른 상·문헌값과 나란히 금지) | | ⛔ **대응 양이 이 논문에 없다** (장벽 0 · Li₂S · Li₃Nd 언급 0) — 값을 옮겨 적지 않는다 |
| O 자리 | UMA — **"O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)"** (`HZ-nd-site-cfg23-mislabeled` 가 허용하는 문장) | BLOCKED 항목의 허용 서술 | ✅ 방향 (조성 · 방법 다름) |

### 7b. 항목별 대조

| # | 항목 | 이 논문 | 우리 | 같은가 / 다른가 · 이유 |
|---|---|---|---|---|
| ① | 조성 | LPSC · **LPSC₁.₆** · LPSOC (Li₆PS₄OCl) | comp1 · **modelc** · lpsocl (Li₅.₄PS₄.₂O₀.₂Cl₁.₆) | LPSC₁.₆ = modelc **명목 일치** · LPSOC ≠ lpsocl (O 5 배 · Cl 모체 다름) — O 축은 **조성부터 다르다** |
| ② | Cl-rich σ | LPSC₁.₆ / LPSC = 5.49 / 2.70 = **2.0×** (30 °C, 같은 실험실) | MLIP-MD 조성 간 순위 막힘 (7a) | **문헌 합의 (§A 머리 "Cl-rich 가 빠르다") 와 같은 방향** · 우리 쪽은 대조 불가. LPSC 대 Cl₁.₅ 쌍 [Zuo] 7.0/2.9 (2.4×) 와 같은 차수 |
| ③ | O 치환 σ·Ea | x 0→1: σ −14 % · Ea +0.04 eV | 대조 불가 (7a) | 문헌 방향 (O → σ 손해, `comparison_vs_ours.md` §A [Nosrati26Rev] 행) 과 같다 |
| ④ | **같은 실험실 재현** (우리 그룹 내부) | LPSC: a 9.850 Å · σ(30 °C) 2.70 · **Ea 0.22 eV** · AFM-FS **E 10.5 GPa** | `[Lee26Mech]` (같은 1저자 Y. Lee · 같은 NX-10 / PPP-NCHR / 256² · 5 × 5 µm · 같은 20–60 °C 5 점 창): LPSC a 9.852 · σ(25 °C) 2.0 · **Ea 0.32** · **E 8.0 GPa** | 🔴 **같은 랩 · 같은 명목 조성 · 같은 측정 창에서 Ea 가 0.10 eV, E 가 31 % 갈린다** — 합성 경로 차이 (이 논문 400 rpm 10 h 밀링 + 미기재 열처리 vs `[Lee26Mech]` 800 rpm 2 h + 400 °C 2 h 소성). ⇒ 이 논문의 O 효과 (ΔEa 0.04) 보다 **랩 내 배치 간 차이가 더 크다** — 실험 Ea · E 를 절대 앵커로 쓰지 않는 규율의 우리 그룹 실례 |
| ⑤ | 산화 onset (축 ①) | CV 겉보기 개시 `figure-read ≈` 2.45 (LPSC) · 2.55 V (LPSOC) | comp1 = modelc 2.256 V (GG) / 2.14 (LiS4 포함) · O 단독 대조 2.14 (LiS4 포함) — Li-rich facet 값 (`HZ-esw-reduction-limit-facet-convention`) | **방향 일치 — "O 치환은 onset 을 거의 안 움직인다"**: 우리 O 단독 대조 (한 점) 의 onset 이 같은 상 집합의 comp1 · modelc 와 같고, CV 개시 이동도 ≈0.1 V 로 작다. CV 개시가 우리 값보다 0.2–0.3 V 높은 것은 **겉보기 개시 = 동역학 · 검출 한계** ([Zuo] 와 같은 해석) — 절대값 일치를 주장하지 않는다. ⛔ "O 는 onset 을 안 바꾼다" 로 일반화 금지 (도핑 D_plain 1.893–2.356 V 선례) |
| ⑥ | 산화 산물 | 양극 100 사이클 뒤 PO₄³⁻ · P₂S_x · Li₂Sₙ (XPS) | O 단독 대조 산화 onset 산물 = **Li₃PS₄ + LiS₄ + Li₃PO₄ + LiCl** (+ Li) | **산물 종류 일치** (인산염 + 폴리설파이드) · 우리 grand-potential 도 O 가 산화 쪽에서 **Li₃PO₄** 로 간다고 말한다 = 논문 p.3 의 "산화분해 Li₃PO₄ 계 계면상" 과 같은 화학 |
| ⑦ | **Li 쪽 산물** | Li₃PO₄ (Raman ≈940 · XPS 134.3 · 소성분) = "SEI" | O 단독 대조 (전압 profile 단계 — `reduction_limit_V` 필드가 아니다): **0 V 산물 = 0.3 Li₂O + Li₃P + 4.1 Li₂S + 1.6 LiCl** · Li₃PO₄ 는 **0.687 V 단계 위에서만** 남는다 (그 아래에서 Li₃P + Li₂O) · `[Zhu15]` Li₃PO₄ 창 0.69–4.21 V 와 같다 | 🔴 **열역학 방향이 다르다.** Li 금속 접촉면 (0 V) 에서 O 의 바닥 산물은 Li₂O 다. 논문이 본 Li₃PO₄ 는 (i) 동역학적 준안정 (LiPON 류) (ii) 접촉면에서 떨어진 (전위가 0.69 V 위인) 자리의 산물 (iii) 잔류 전구체 중 하나다 — 이 논문 데이터로는 못 가른다. 그리고 그 환원 산물 **Li₃P 는 우리 원장에서 `conductor-LEAK` (MP PBE 0.70 eV)** — "Li₃PO₄ SEI 가 전자를 막는다" 는 Li₃PO₄ 가 **환원되지 않을 때만** 성립한다 |
| ⑧ | Li₃PO₄ 띠틈 | **7.4 eV** (인용 [36,38] · 방법 미기재) | MP PBE **5.818 eV** (정정본) · role insulator (문턱 ≥ 4 eV) · exp_anchor ~8 | **역할 일치 (와이드갭 절연체)** · 숫자는 나란히 놓지 않는다 (PBE 과소평가 + 상대 방법 불명) |
| ⑨ | 기계 | AFM-FS E: LPSC 10.5 < LPSOC 13.4 < LPSC₁.₆ 15.1 GPa | relaxed-ion E_VRH: comp1 22.06 · modelc 27.66 · lpsocl 35.04 GPa | ⛔ **같은 양이 아니다** — 냉간압축 펠릿 *표면* 의 접촉강성 (팁 반경 · 접촉모델 · 포아송비 가정 미기재, 기공·입계 뺀 ROI) vs 0 K 단결정 VRH 평균. 방향: LPSC < LPSC₁.₆ 는 우리 baseline 이 찍는 comp1 → modelc 증가와 **어긋나지 않는다** — 단 두 값이 다른 comparison_group 이라 "검증된 일치" 라 쓰지 않는다. LPSOC < LPSC₁.₆ (AFM) 는 우리 lpsocl > modelc 와 반대 순서지만 **조성이 다르고 (Cl 1.0 vs 1.6 모체) 우리 쪽 순위가 금지**라 판정 불가 |
| ⑩ | Li 수송 · SEI 동역학 | 셀 수준 (EIS · DRT · CCD · 대칭셀 분극) | Li₂S · Li₃Nd NEB (단일 홉 · 벌크 모형) | **양이 다르다** — 이 논문엔 장벽이 없고, 우리 NEB 대상 (Li₂S · Li₃Nd) 은 이 논문에 등장하지 않는다. 옮겨 적을 값이 없다 |
| ⑪ | SE 전자구조 | 없음 (Li₃PO₄ 인용 1 개) | comp1 2.066 · modelc 2.099 · lpsocl 2.2309 eV (fixed-occ nscf) | 대조 없음 |
| ⑫ | O 자리 | **16e** (Rietveld "확인" — 점유율 미제시) | UMA: **O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)** | **방향 일치 (16e)** — 단 (i) 이 논문 조성에 Nd 가 없고 (ii) 증거 등급이 낮다 (§10-①) (iii) 우리 쪽은 Nd 가 든 셀의 UMA 비교라 이 문장 그대로만 쓴다. 문헌은 갈린다: Zhao 2025 Rietveld 는 O@**4d** (`db/compositions/modelc_nd_doped.json` O_placement_ambiguity) |
| ⑬ | Cl-rich 의 Li 계면 (§E 충돌) | LPSC₁.₆: 벌크 저항 최저인데 **계면 호 폭 최대** (`Fig. 5a`) · CCD 1.8 ≈ LPSC 1.7 | §E: "Cl 함량은 음극측 계면 수송을 거의 안 바꾼다" (우리 산물 부피비 재계산) | **어긋나지 않는다** — Cl-rich 의 벌크 이점이 Li 계면으로 넘어가지 않는다는 실험 한 점. 단 입도 (3 µm) · 숙성 조건이 섞여 있고, 숙성 증가는 LPSC 가 더 크다 (§10-⑮) |

### 7c. 🔑 층위를 갈라 쓴 결론
- **같은 화학**: O 도핑 argyrodite 의 산화 산물에 Li₃PO₄ 가 낀다 (논문 XPS ↔ 우리 grand-potential O 단독 대조) · Cl-rich 의 이점은 벌크 σ 이지 Li 계면이 아니다 (논문 `Fig. 5a` ↔ 우리 §E).
- **다른 화학 (열역학 vs 관측)**: Li 금속 쪽 Li₃PO₄ "SEI" — 우리 열역학은 0 V 에서 Li₂O + Li₃P 로 간다. 실재 차이 (동역학 준안정) 인지 측정 해석의 문제 (소성분 · 잔류 전구체) 인지 이 논문으로는 못 가른다.
- **비교 불가 (규율)**: Ea · σ · E 의 조성 간 순위 — 우리 쪽이 막혀 있다. 이 논문의 실험 순위를 우리 계산이 "재현했다" 고 쓰지 않는다.
- **비교 불가 (양이 다름)**: AFM-FS E ↔ E_VRH · CCD ↔ NEB 장벽.

---

## 8. DFT / 계산 방법 ★
- **code · functional · pseudo · k · ecut · supercell · +U · AIMD · MLIP · 무질서 처리 — 전부 n/a.** 이 논문은 원자단위 계산을 하지 않는다.
- 계산처럼 보이는 숫자는 전부 인용: Li₃PO₄ 띠틈 7.4 eV [36,38] (⚠ [36] = Wang 2022 *JMCA* 도핑 리뷰 · [38] = Wang 2024 *Angew* **흑연 음극 · 액체 전해질** Li₃PO₄-rich SEI — 출처의 계산·측정 방법을 이 논문에서 알 수 없다).
- 구조 모델 `Fig. 2c` 는 Rietveld 결과를 그린 모식도 — 계산 구조 아님.
- 정량 후처리는 전부 실험: TLM 적합 · DRT · Rietveld · XPS 피팅 · SEM 이진화 · AFM-FS 곡선 적합.

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 설계 모식도: ① 양극 (NCM + 1 µm LPSOC + Super P) ② 분리막 (3 µm LPSC₁.₆) ③ Li 계면 (M-SE = 1/3 µm 혼합) — 층마다 요구 · 해법 문구 | "층마다 다른 SE" 개념도 — 우리 축 배치 (산화 = 촉매질 · σ = 분리막 · 환원/기계 = Li 계면) 설명에 그대로 대응 |
| 2a,b | XRD x = 0–1.75 · 고각 이동 (`figure-read ≈` +0.08–0.10° @30–31.5°) · x = 1.75 잔류 전구체 | ⚠ 이동량이 Rietveld Δa (−0.006 Å) 의 ≈5 배 — 격자 수축 정량 근거로 쓰지 않는다 |
| 2c | LPSOC 모식 구조 — 16e 를 S/O 공유로 표시 | O@16e **주장** 의 그림. 점유율 근거 아님 |
| 2d–f | 아레니우스 (20–60 °C) · σ(30 °C) 2.70/2.58/2.33/1.50 · Ea 0.22/0.23/0.26/0.30 | O 치환 → σ↓ · Ea↑ 실험 방향 (한 실험실). ⚠ 2e 의 x = 0 막대 높이 오류 (≈3.05) |
| 2g | tender XAS P · S · Cl K-edge | Cl K-edge 변화가 P edge 보다 크다 — O 자리 판정엔 안 쓴다 |
| 3a,b | NCM811 ‖ Li–In 0.1C 첫 사이클 · 0.5C 100 사이클 (30 °C) | 촉매질 O 치환의 첫 용량 이득 (184.0 → 206.4) — 개선 대부분이 0 사이클 용량 차 |
| 3c–e | TLM: R_ion · R_int · R_w (0/100 사이클) | **R_int 74.0 vs 47.3** — 우리 B③ (양극 계면) 축의 실험값 · R_ion 1–2 Ω cm² 는 무시 가능 |
| 3f,g | 100 사이클 뒤 양극 XPS S 2p · P 2p | 원자료 포락선 차이만 인용 · 성분 분해는 스핀-궤도 짝 위반이라 수치 인용 금지 · PO₄³⁻ 는 LPSC 쪽이 더 크다 |
| 4a,b | 분리막 3 종 rate (30 °C, Li–In) | Cl-rich 분리막 우위가 1C +5.5 · 2C +2 mAh g⁻¹ (`figure-read`) 로 작다 — σ 2 배가 셀 rate 에 얼마나 남는지의 실측 |
| 5a,b | Li 대칭셀 Nyquist (숙성 전후) · DRT | **Cl-rich LPSC₁.₆ 의 Li 계면 호가 가장 크다** — §E 실험 한 점 · 숙성 증가는 LPSC 가 더 크다 (본문과 어긋남) |
| 5c | 0.5 · 2.0 mA cm⁻² 대칭셀 (45 °C) | M-SE ≈ LPSOC 분극 · LPSC 2.0 mA cm⁻² 단락 |
| 5d,e | CCD 45 °C (1.7/1.8/3.1/3.5) · RT (LPSC 1.4 · M-SE 1.9) | ⚠ 45 °C LPSC · LPSC₁.₆ 라벨이 본문과 뒤바뀜 · CCD 셀 분극이 옴 하한 아래 · LPSOC 실패는 접촉 상실형 · LPSC RT 는 박리 비대칭 |
| 5f | RT CCD 문헌 비교 (y 축 단위 "mAh cm⁻²" 오기) | ⚠ 참고문헌 번호가 본문과 다르다 — 문헌값 재인용 금지 |
| 6a | SEM 표면 + 공극 지도 · 기공비 0.148/0.125/0.070 | 입도 혼합으로 표면 기공 절반 — 우리 DEM 패킹 축의 실험 대조 후보 (사진 1 장씩이라 정량 약함) |
| 6b | AFM 지형 (LPSC · LPSOC · M-SE) | ⚠ 캡션은 LPSC₁.₆ 라 씀 — 패널과 다르다 |
| 6c | F–d 곡선 + E 지도 · 10.5 / 13.4 / 15.1 GPa | ⛔ E_VRH 옆에 같은 양으로 놓지 않는다 · 🔴 LPSC₁.₆ 패널 지도 = LPSC 지도 중복 |
| 7a–c | 풀셀 단계 비교 (45 °C, 1C · 2C) | 설계 효과의 본체 — **2C 셀은 ≈350 사이클 단락** (그림 라벨) |
| 7d | RT 1C 100 사이클 85.5 % | 대조의 촉매질이 다르다 (LPSC) — M-SE 단독 효과 아님 |
| 7e | RT 100 사이클 이상 문헌 대비 (로딩 × C-rate) | ⚠ [64] 는 참고문헌에 없고 [34] 는 DFT 전용 논문 — 비교 근거로 재인용 금지 |
| S1 | Li₆PS₅₋ₓOₓCl 입자 SEM (입자 1 개씩, `figure-read ≈` 2.5–3.5 µm) | 분쇄 전 입자 크기 — "1 µm" 의 근거 아님 |
| S2 | Rietveld LPSC (a 9.850) · LPSOC (a 9.844) · R 인자 | ⚠ 점유율 없음 · LPSC GOF 1.49 ≠ R_wp/R_exp 1.09 · LPSOC 패턴에 ≈22.0/23.0/24.6° 약한 반사 (계산 곡선이 따라감) |
| S3 | SUS 대칭셀 Nyquist (온도별) | (안 봄) |
| S4 | LPSC₁.₆ 입자 SEM (1 개, `figure-read ≈` 2.5–3 µm) | "3 µm" 와 맞는다 |
| S5 | LPSC₁.₆ Nyquist + σ 20/30/40/50 °C = 4.79/5.49/6.99/10.06 | **우리 modelc 명목 조성의 실측 σ(T)** — 구간 Ea 0.10 → 0.32 eV 로 비-아레니우스 (*우리 산수*) · 우리 MLIP Ea 와 절대 비교 금지 |
| S6 | 양극 Nyquist (사이클 전후) | (안 봄) |
| S7 | TLM 등가회로 | (안 봄 — 캡션 텍스트) 우리 그룹 ref [45] 방법 |
| S8 | 사이클 전 양극 XPS | (안 봄) |
| S9 | CV LPSC vs LPSOC (2–4.5 V, µA) | 축 ① — 개시 이동 ≈0.1 V · 전류 0.8× · 4.5 V 까지 계속 산화 → "4.5 V 운전" 근거 아님 |
| S10 | 사이클 후 NCM–LPSOC XRD | (안 봄) |
| S11 | M-SE 혼합비 Nyquist (8:1 · 4:1 · 2:1) | 4:1 = 계면 · 벌크 절충 (셀 1 개씩) |
| S12 | 혼합비별 대칭셀 0.5 mA cm⁻² 45 °C | 4:1 최저 분극 (≈±12–13 mV) |
| S13 | Raman — 사이클 전 (LPSC₁.₆ · LPSOC) · 사이클 뒤 (LPSC · M-SE) | M-SE 사이클 뒤 ≈950 cm⁻¹ 소봉우리 = Li₃PO₄ 주장의 근거 · 사이클 전 LPSOC 에 없음 · LPSOC 단독 사이클 뒤는 미측정 |
| S14 | Li/SE 계면 P 2p (24 h 접촉 · 5 사이클) | 134.3 eV 는 **소성분** — 본문 "clear peak" 는 과장 |
| S15 | AFM-FS E 히스토그램 (LPSC · LPSOC · LPSC₁.₆) | 30 GPa 절단 · 최빈값 보고 · 표본 수 다름 — LPSC₁.₆ 15.1 GPa 의 실제 근거 |
| S16 | M-SE F–d · 지도 (축척 3 µm) · 히스토그램 14.6 GPa | 지도 크기가 다른 시료와 다르다 |
| S17 | 1C 500 사이클 뒤 Li/M-SE 단면 SEM + P · S EDS | 20 µm 축척 · 계면 위 ≈20 µm S 결핍 띠 (P 는 균일) — "덴드라이트 없음" 근거로 약하다 |
| Table S1 | TLM 적합값 전부 (R_Ohmic · R_ion · R_int · R_w · CPE) | §3b 에 전 셀 복원 (PDF 텍스트) |

## 10. 비판 — 이 논문의 약한 곳 ★ (우리 그룹 논문이라 더 엄격하게)

> 🔴 = 결론 · 인용에 영향 · 🟠 = 정량 신뢰도 · 🟡 = 표기 오류

1. 🔴 **O@16e "확인" 의 근거가 보이지 않는다** (`Fig. S2`). 보여준 것은 적합 곡선 · a · R 인자뿐이고 **O 점유율 · 원자 좌표 · B · 4a/4d 대안 모델과의 비교가 없다.** x = 1 의 O 는 16e 자리의 ¼ 이고 전구체 (Li₃PO₄) 잔류 가능성이 있어 점유율 정련이 핵심인데 빠졌다. 덧붙여 (i) LPSC 의 GOF 1.49 는 자기 R_wp/R_exp (8.04/7.39 = 1.09, χ² = 1.18) 와 안 맞는다 (ii) LPSOC 패턴에 F-43m 금지 각도 (≈22.0 · 23.0 · 24.6°) 반사가 있고 계산 곡선이 그것을 따라간다 = **2차상을 넣고 정련했는데 본문은 "단일상"** (iii) `Fig. 2b` 의 봉우리 이동은 a ≈ 9.817 Å 를 주는데 정련값은 9.844 Å. ⇒ **"x = 1 의 O 가 실제로 격자에 얼마나 들어갔나" 가 이 논문에서 안 정해진다.**
2. 🔴 **"dendrite-tolerant" 의 범위**: 같은 설계의 **2C 셀은 ≈350 사이클 단락** (`Fig. 7c` 라벨) — 본문은 *"stable cycling was sustained up to 350 cycles, thereby confirming that the designed M-SE effectively suppresses dendrite growth"*. 1C 500 사이클 단락 없음은 사실이지만 데이터가 받치는 서술은 **"단락을 늦춘다"** 다. 셀 반복 수 (n) 도 없다.
3. 🟠 **XPS 피팅 규칙 위반** (`Fig. 3f,g`): PS₄³⁻ 짝이 네 패널 모두 스핀-궤도 규칙 (2p₃/₂ 가 낮은 BE · 면적 2 : 1 · 같은 FWHM · 간격 S 1.18 / P 0.87 eV) 을 어긴다 — `Fig. 3f` 는 2p₁/₂ 가 2p₃/₂ 보다 크고, `Fig. 3g` S 2p 는 라벨이 BE 순서와 반대이고 두 성분 폭이 다르다. 새 산물 (P₂S_x · Li₂Sₙ · PO₄³⁻) 은 짝 없이 단일 봉우리. 본문 BE (162.7 / 163.4) 와 그림 성분 위치 (≈163.1 / ≈164.0) 도 0.4–0.6 eV 다르다. ⇒ **성분 면적 · 비율 인용 금지 · 원자료 포락선 차이만 인용.**
4. 🟡 `Fig. 2e` x = 0 막대가 라벨 (2.70) 이 아니라 ≈3.05 높이 — 감소 폭이 −14 % 가 아니라 −24 % 로 보인다.
5. 🟠 **LPSC₁.₆ σ(T) 가 비-아레니우스** (`Fig. S5`): 구간 Ea 0.104 → 0.198 → 0.317 eV (*우리 산수*). 온도 평형 · 접촉 문제가 의심된다. 논문은 LPSC₁.₆ Ea 를 내지 않는다. **우리 modelc 와 명목 조성이 같은 실측이지만 Ea 앵커로 쓰지 않는다.**
6. 🟠 **"분리막 σ 가 rate 를 지배" 와 "수송 손실은 무시 가능" 의 자기모순**: rate 우위 (1C +5.5 · 2C +2 mAh g⁻¹) 는 작고 율이 오를수록 줄어든다 (σ 율속이면 반대) · 같은 논문이 M-SE 의 σ 불일치를 반박할 때는 *"interfacial resistances … dominate the overall cell impedance, significantly exceeding the contribution of Li⁺ transport resistance"* 라 쓴다 · M-SE 를 넣으면 첫 1C 용량이 167.3 → 159.7 (−4.5 % · 셀 하나씩). 비교마다 변수가 둘씩 바뀐다: `Fig. 7d` RT 대조는 촉매질까지 LPSC · `Fig. 3b` 개선은 0 사이클 용량 차가 대부분 (감쇠율 차 ≈5 %p).
7. 🟠 **합성 · 형상 기록 누락**: "subsequent solid-state synthesis" 의 온도 · 시간 없음 · 촉매질 "~1 µm" 분쇄 방법 · 입도분포 없음 (`Fig. S1` · `Fig. S4` 는 분쇄 전 입자 한 개씩, 전부 ≈3 µm) · 층별 질량 · 두께 · 대칭셀 펠릿 두께 · 1C 정의 · 45 °C 풀셀 Li 두께 미기재.
8. 🟡 **CCD 값이 본문과 그림에서 뒤바뀌어 있다** (45 °C): 본문 LPSC 1.7 / LPSC₁.₆ 1.8 · 그림 라벨 LPSC 1.8 (검정) / LPSC₁.₆ 1.7 (빨강) · 그림에서는 검정이 한 단계 더 버틴다. 차이는 한 단계 (0.1) 라 결론엔 영향 없다.
9. 🟡 **문헌 비교 그림의 참고문헌 번호가 출판본 목록과 안 맞는다**: `Fig. 5f` [55][56][17][57][58][59] ↔ 본문 [15, 54–58] · `Fig. 7e` [34][57][62][63][64][54] — **[64] 는 없다** (참고문헌 63 편) · [34] 는 Se 도핑 LGPS **DFT 전용** 논문 · [62] 는 탄소천 리뷰. 수정 과정의 번호 이동으로 보인다. ⇒ 두 비교 그림의 문헌값을 재인용하지 않는다. 덧붙여 `Fig. 5f` y 축 단위 "mAh cm⁻²" (→ mA cm⁻²) · `Fig. 5` 캡션의 두 번째 "(e)" 는 (f) 여야 하고 내용 (C-rate × 로딩) 은 `Fig. 7e` 의 것이다.
10. 🔴 **AFM 쪽 그림 · 프로토콜 불일치**: `Fig. 6c` LPSC₁.₆ 지도 = LPSC 지도 (중복, 라벨까지 "LPSC") · `Fig. 6b` 패널 (LPSC · LPSOC · M-SE) ↔ 캡션 (LPSC · LPSOC · LPSC₁.₆) ↔ 본문 (M-SE vs LPSC · LPSC₁.₆) 셋이 다르다 · 스캔 면적 2 × 2 µm (본문) vs 5 × 5 µm (SI Note) vs ≈9 µm (`Fig. S16`) · 히스토그램 30 GPa 절단 · 최빈값 보고. 같은 그룹 `[Lee26Mech]` 의 같은 프로토콜 LPSC 는 **8.0 GPa** (이 논문 10.5). ⇒ AFM-FS E 는 **같은 측정 세트 안의 순위로만** 읽는다.
11. 🟠 **Li₃PO₄ 의 역할 서술이 자기모순**: p.3 *"Li₃PO₄-based interphase formed via the oxidative decomposition of LPSOC … low electronic conductivity, thereby effectively suppressing further decomposition"* vs p.5 *"Such species [phosphate-related, e.g. Li₃PO₄] formed at the cathode are typically non-uniform and resistive … accelerating interfacial degradation"* — 그리고 `Fig. 3f,g` 에서 PO₄³⁻ 는 LPSC 양극이 더 크다. 양극에서 LPSOC 의 이점은 데이터상 **"분해가 적다"** 이지 "보호막을 만든다" 가 아니다.
12. 🟠 **"~4.5 V 적용 가능" 은 CV 가 받치지 않는다** (`Fig. S9`): LPSOC 도 ≈2.5 V 부터 4.5 V 까지 LPSC 의 0.8 배 전류로 계속 산화한다 · 전류 미정규화 · 단일 측정.
13. 🟠 **Li 계면 "Li₃PO₄ SEI" 의 근거가 약하고 열역학과 어긋난다**: Raman · XPS 모두 소성분 · LPSOC 단독 사이클 뒤 Raman · M-SE 사이클 전 Raman 미측정 · 주산물 (Li₂S · Li₃P · LiCl · Li₂O) 을 볼 S 2p · Cl 2p · O 1s · Li 1s 가 없다 · 전자 절연을 잰 데이터 (σ_e) 가 없다 · Li₃PO₄ 의 계산 환원 한계는 0.69 V (`[Zhu15]` · 우리 O 단독 대조 0.687 V) 라 0 V Li 접촉면에선 Li₃P + Li₂O 가 열역학 산물이다 · 띠틈 7.4 eV 는 액체 전해질 논문 인용. `Fig. S17` EDS 의 S 결핍 · P 균일 띠도 설명이 없다.
14. 🟡 사소: 본문 "이후 모든 전기화학 평가는 Li 금속 음극" ↔ `Fig. 4` 는 Li–In · 결론 *"M-SE composed of LPSOC and **LPSC**"* (→ LPSC₁.₆) · `Table S1` 캡션 "TML" (→ TLM) · `Fig. 5d` "3.5 mA cm2" (지수 누락) · 서론 "10⁻⁹ **mS** cm⁻¹" (원전 단위 확인 필요) · `Fig. 7a` 단락 ≈108 사이클 vs 본문 "within 100 cycles".
15. 🟡 **숙성 증가 서술이 그림과 안 맞는다** (`Fig. 5a`): 본문은 LPSC₁.₆ 의 *"relatively large rise in resistance during rest"* 를 말하지만 호 끝 기준 `figure-read` 증가는 LPSC ≈+18 · LPSOC ≈+15 · LPSC₁.₆ ≈+12 · M-SE ≈+10 Ω cm² 다. LPSC₁.₆ 에 대해 그림이 받치는 것은 "계면 호 자체가 크다" 까지다.
16. 🟠 **CCD 셀 분극이 그 셀의 옴 하한보다 낮다** (*우리 산수*, 가정 명시): `Fig. 5a` 의 LPSC 고주파 절편 ≈38 Ω cm² (RT) 를 `Fig. 2d` σ(T) 로 45 °C 에 옮기면 벌크만 ≈21.5–24 Ω cm² → 0.5 mA cm⁻² 에서 최소 ≈11–12 mV 여야 하는데 `Fig. 5d` 의 LPSC 는 그 단계에서 `figure-read ≈`±5–6 mV (마지막 단계 1.8 mA cm⁻² 에서도 ≈±19 mV, 하한 ≈39–43 mV) 다. 같은 45 °C 의 사이클 셀 (`Fig. 5c`) 은 ≈±20 mV 로 하한 위다. M-SE 도 같은 모양이다 (`Fig. 5d` 3.4 mA cm⁻² 에서 ≈±31 mV · `Fig. 5e` RT 1.4 mA cm⁻² 에서 ≈±22 mV — `Fig. S11` 4:1 벌크 절편 ≈36.5 Ω cm² 와 안 맞는다). ⇒ CCD 셀이 대칭셀 절 (0.1 g) 과 다른 두께였거나 처음부터 부분 전자 누설이 있었다 — 후자라면 CCD 가 부풀려진다. 두께 미기재 · 반복 없음이라 못 가른다. (전제: CCD 셀이 `Fig. 5a` 셀과 같은 구조 — 방법 절은 대칭셀 구조를 하나만 적는다.)

## 11. 우리 원장 매핑 (요약)

| 이 논문 항목 | 우리 원장 | 판정 |
|---|---|---|
| LPSC₁.₆ σ(T) (`Fig. S5`) | modelc (명목 일치) · MLIP-MD Ea (`md-ea-*`) | 실측 참고값으로만 · 우리 Ea 와 절대 비교 금지 |
| O 치환 σ · Ea (`Fig. 2e,f`) | lpsocl (조성 다름) | 대조 불가 (레지스트리 금지 3 건) |
| AFM-FS E (`Fig. 6c`, `Fig. S15`) | `db/properties/elastic.json` E_VRH | ⛔ 같은 양 아님 |
| CV (`Fig. S9`) | `esw_lis4excluded.json` · `cei_esw_Li_controls_2026_09_16.json` | 축 ① 방향 일치 (onset 거의 불변) |
| 양극 산물 (`Fig. 3f,g`) | `cei_esw_Li_controls_2026_09_16.json` o_only_03 산화 산물 | 종류 일치 (인산염 + 폴리설파이드) |
| Li 쪽 Li₃PO₄ (`Fig. S13`, `Fig. S14`) | 같은 파일 o_only_03 profile (0.687 V) · `sei_products.json` (Li₃P conductor-LEAK) | 🔴 열역학 방향 어긋남 |
| Li₃PO₄ 7.4 eV | `sei_products.json` Li₃PO₄ 5.818 (정정본) | 역할만 일치 |
| O@16e (`Fig. S2`) | `HZ-nd-site-cfg23-mislabeled` 허용 문장 · `modelc_nd_doped.json` Track 1A/1B | 방향 일치 · Nd 자리엔 무관 |
| Li 수송 장벽 | `sei_neb.json` (Li₂S CONDITIONAL · Li₃Nd SI 전용) | 대응 양 없음 |

## 12. 적용 인사이트 ★
1. **CEI 트랙 (NdO-LPSCl₁.₆ · 1저자 = 실험 쪽 박재현) — 자리 질문**: 이 논문은 **Nd 자리에 대해 아무 말도 하지 않는다** ("site-specific" = 셀 위치). O 자리에 대해서만 *lab-XRD Rietveld 주장* 으로 **16e** 한 점을 보탠다 — 우리 "O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)" 와 같은 방향이고 Zhao 2025 (O@4d) 와는 반대다. ⇒ 문헌의 O 자리는 **합성 경로 의존** 일 가능성이 크고, 그 질문의 정본은 이 논문이 아니라 공동 교신 그룹의 **[24] Park *ESM* 2025 "site-selective oxygen introduction"** · **[43] *eScience* 2026** · **[44] *Carbon Energy* 2025 "site-specific Nb doping"** 이다 (전부 미digest — 받아 오면 O · 도펀트 자리를 *어떤 증거로* (중성자? NMR? DFT?) 정했는지부터 본다). ⛔ `HZ-nd-site-cfg23-mislabeled` 의 옛 비교 (1.633 eV/cell) 를 이 논문으로 되살리지 않는다 — 그것은 O 자리 비교다.
2. **cascade novelty 후보 A · B**: **A ('이로운 분해' 도펀트 설계) 에 정면으로 걸린다** — 같은 그룹이 "O 도핑 → (Li 쪽) Li₃PO₄ SEI = 이로운 분해 산물" 을 실험으로 이미 주장했다 (서론 *"tailoring the SE composition to induce a beneficial solid–electrolyte interphase (SEI) chemistry is also a highly promising strategy"*). 남는 갭은 **계산 설계**: 도펀트 → 전위별 분해 산물 → 산물 물성 (띠틈 · 이온전도 · Li 안정창) 을 예측 · 순위화하는 층 — 이 논문엔 0 이고, 우리 grand-potential 은 이미 "0 V 에선 Li₃PO₄ 가 아니라 Li₂O" 라는 비자명한 답을 준다. **B (분해 부피 변화 화학-기계) 에는 안 걸린다** — 분해 산물 부피 · 응력 데이터 0, 기계는 펠릿 AFM 탄성률뿐.
3. **우리 그룹 내부 재현 편차가 가장 쓸모 있는 숫자다**: 같은 랩 · 같은 1저자 · 같은 측정 창에서 LPSC Ea 0.22 vs 0.32 eV · AFM E 10.5 vs 8.0 GPa. 계산값을 상대 차이로만 쓰는 이유를 실험 쪽에서 설명할 때 이 쌍이 제일 설득력 있다 (외부 문헌보다 반박하기 어렵다).
4. **Li 금속 쪽 산물 질문은 우리가 답할 수 있는 꼴이다**: "O 도핑 argyrodite 가 Li 에서 만드는 O 산물은 Li₃PO₄ 인가 Li₂O 인가" — grand-potential 이 이미 0.687 V 경계를 준다. 다음 단계는 계산이 아니라 문헌 확인: Li₃PO₄|Li 계면이 동역학적으로 버티는 근거 (LiPON 류) · O 원이 소수 성분 (M-SE 의 20 wt%) 일 때 계면 전위 분포.
5. **강성 서사에 대한 내부 반례** (§6): LPSC₁.₆ 가 가장 단단한데 CCD 는 LPSC 와 같다 → 우리 탄성 축을 "덴드라이트 억제" 로 연결할 때 이 반례를 먼저 적는다.

## 13. 인용 가능 문장 (영문 초안 · 조건 포함)
- "Kang et al. assigned different argyrodite electrolytes to the catholyte (Li₆PS₄OCl), separator (Li₅.₄PS₄.₄Cl₁.₆) and Li-metal interlayer (a 4:1 Li₅.₄PS₄.₄Cl₁.₆/Li₆PS₄OCl mixture), and reported a critical current density of 3.5 mA cm⁻² at 45 °C for the mixed interlayer versus 1.7 mA cm⁻² for Li₆PS₅Cl (*Energy Storage Mater.*, 90, 105335 (2026))."
- "In the same study, an NCM811‖Li cell with the full layered design cycled 500 times at 1C (45 °C, 20 MPa) without short-circuiting, whereas the corresponding 2C cell short-circuited after about 350 cycles (Fig. 7c)."
- "Oxygen substitution in Li₆PS₅₋ₓOₓCl (x = 0 → 1) lowered the 30 °C ionic conductivity from 2.70 to 2.33 mS cm⁻¹ and raised the activation energy from 0.22 to 0.26 eV in one laboratory series (20–60 °C)."
- ⛔ 쓰지 말 것: "O occupies the 16e site, as confirmed by Rietveld refinement" (점유율 미제시) · "Li₃PO₄ forms a 7.4 eV SEI at the Li interface" (인용값 · 소성분 · 열역학 반대) · AFM-FS E 를 DFT E_VRH 와 같은 표에.

## 14. 주의 / 한계 (인용 규율)
- 이 논문의 모든 값은 **소환값** — 우리 `db/properties/` 절대값과 같은 표에 섞지 않는다 (§7 은 방향 · 역할 · 산물 종류만).
- "site-specific" 을 자리 선택 치환 근거로 인용하지 않는다.
- AFM-FS E 는 같은 세트 안 순위로만 · CCD 는 단일 셀 (반복 없음) · σ "RT" = 30 °C.
- `Fig. 5f` · `Fig. 7e` 의 문헌값은 번호 불일치로 재인용 금지.
- [우리 그룹] 논문이다 — §10 의 그림 오류 (특히 `Fig. 6c` 지도 중복 · `Fig. 7c` 2C 단락 서술) 를 밖에서 지적하기 전에 저자 쪽과 먼저 확인한다.

## 15. 기법 용어 미니사전
- **CCD (critical current density)**: 대칭셀 전류를 단계적으로 올려 단락 (또는 전압 발산) 이 나는 전류. 여기선 0.1 mA cm⁻² · 1 h 단계. 정의 (단락 vs 발산) 와 반복 수 · 펠릿 두께가 값을 좌우한다.
- **TLM (transmission-line model)**: 복합전극을 이온 경로 저항 r_ion 과 계면 임피던스 (r_int ‖ CPE + Warburg) 가 사다리처럼 분포된 회로로 보는 적합. R_ion · R_int · R_w 를 분리한다.
- **DRT (distribution of relaxation times)**: 임피던스를 시정수 τ 분포 γ(τ) 로 바꿔 겹친 과정을 가르는 해석. 긴 τ = 계면 · 짧은 τ = 벌크.
- **AFM-FS (PinPoint force spectroscopy)**: 픽셀마다 탐침을 눌렀다 떼며 힘–거리 곡선을 얻고 접근 기울기에서 E 를 낸다 (접촉 모델 · 탐침 반경 · 포아송비 가정 필요). 펠릿 *표면* · nm 깊이 · ROI 선택에 의존한다.
- **Rietveld GOF**: R_wp/R_exp (또는 그 제곱 χ²). 1 에 가까울수록 좋다 — 보고된 R 값과 GOF 가 서로 맞아야 한다.
- **스핀-궤도 짝 (XPS 2p)**: 2p₃/₂ (낮은 BE) : 2p₁/₂ = 면적 2 : 1 · 같은 FWHM · 간격 S 1.18 · P 0.87 eV 로 묶어 적합하는 것이 표준.
- **백색선 (white line, tender XAS)**: K-edge 바로 위 첫 큰 흡수 봉우리 — 비점유 p 상태 밀도와 국소 대칭을 반영한다.
- **void ratio (SEM 이진화)**: 표면 SEM 을 회색조 문턱으로 공극/고체 이진 지도로 바꿔 얻은 면적 분율 — 문턱 · 사진 수가 값을 좌우한다.
- **M-SE**: 이 논문의 혼합 SE 중간층 (LPSC₁.₆ 3 µm : LPSOC 1 µm = 4 : 1 질량비).
- **옴 하한 (ohmic floor)**: 대칭셀 분극의 최솟값 = 전류 × 벌크 저항 (계면이 0 이라 해도 남는 몫). 관측 분극이 이보다 낮으면 셀 두께가 다르거나 전자 누설이 있다는 뜻이다.
