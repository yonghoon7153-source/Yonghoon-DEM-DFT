<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-11-09 작성 (litdb-curator · 사용자 요청 117번 · Kang 2026 문장 24 [43,44] 대조용).
     크롭 43장 (본문 그림 8 + SI 그림 25 + SI 표 10) 중 그림 12장을 실제로 봤다 + Kang 2026 `Fig. 2` (비교용).
     `Fig. 5` 는 도구가 놓쳐서 손으로 잘랐고, XAS 세 패널은 PDF 벡터 경로 좌표를 직접 읽어 수치화했다 (§5.7).
     `Fig. 2c` · `Fig. S8` 막대/표지도 벡터 좌표로 읽었다. Rietveld 좌표로 Li–Li · Li–4d 거리를 우리가 다시 계산했다 (§5.5).
     우리 쪽 값은 db/properties/canonical_registry.json · citation_hazards.json 규율 안에서 '방향만' 적었다. -->

# Oxygen-induced lithium inter-cage conduction for enhanced performance in all-solid-state batteries — Park, Jang, Kim et al. (*eScience* **6** (2026) 100502) — **[외부 · Kang 2026 공동 교신 (Nam/Kwon) 그룹 · Kang 2026 의 ref [43]]**

> slug `park2026_oxygen_induced_li_intercage_conduction` · DOI `10.1016/j.esci.2025.100502` · type `mixed (실험 주 · 계산 = MTP-MLIP MD 보조 · XANES 시뮬레이션 · PDOS · Bader 0)` · PDF 업로드 `6a52c417-117._Oxygen-induced_lithium_inter-cage_conduction…pdf` (본문 15 pp) + `94a6e1d1-117._Sup_Oxygen-induced…pdf` (SI 41 pp: Fig. S1–S25 · Table S1–S10) · digested `2026-11-09` · status ✅ · 태그 **[외부]**
> elements: Li, P, S, O, Cl, Ni, Co, Mn
> methods: DFT, AIMD, MD, MLIP, XPS, Raman, ESW

> **저자**: **Yongsun Park**ᵃ¹ · **Myeongcho Jang**ᵇ¹ · **Jiyu Kim**ᶜ¹ (공동 1저자) · Joon Ha Changᵈᶠ · Hae-Yong Kimᵉ · Seung-Deok Seoᶜ · Gwangseok Ohᵃᶜ · Min Jae Youᶜ · Sunho Koᵉ · Jung Ho Kimᵍ · Kyung-Wan Namᵉ · **Seungho Yu**ᵇ\* · **Sang-Cheol Nam**ᵃᵇᶜ\* · **Ohmin Kwon**ᵃᵇᶜʰ\* — ᵃ RIST (인천) · ᵇ KIST 에너지저장연구센터 · ᶜ POSCO Holdings LiB Materials Research Center (POSCO N.EX.T Hub) · ᵈ RIST 분석평가 (포항) · ᵉ 동국대 에너지신소재공학 · ᶠ 한국교통대 · ᵍ Univ. of Wollongong · ʰ 한양대 ERICA 배터리화학공학과. 접수 2025-07-06 · 수정 2025-09-12 · 수리 2025-11-07 · 온라인 2025-11-18. 지원 MOTIE 기술혁신 (20010044 · 20012224) · NST (GTL24011-000) · KIST (2E33941) · tender XAS = NSLS-II **8-BM (TES)** (DOE DE-SC0012704). 데이터: *"available from the corresponding author upon reasonable request"* — 원자료 공개 없음.
> **[외부]**: 우리 랩 (한양대 Jong-Won Lee) 저자 없음. 단 교신 **Nam · Kwon** 은 `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` (우리 그룹 논문) 의 공동 교신이고, Kang 은 이 논문을 **ref [43]** 로 인용한다 (서지 대조 §0-1).
>
> **계보**: 같은 1저자의 **ref [7] Park *ESM* 75, 104078 (2025) "site-selective oxygen introduction"** (Li₃PO₄ 경로 — Kang 의 [24]) · ref [11] Park *Small* 2023 (Li₁₀SnP₂S₁₂ 코팅) · ref [9] Kwon 2015 LGPS. 이 편은 산소원을 **Li₂SO₄** 로 바꾼 후속이다. 공동 교신 그룹의 *결정학적 자리 선택* 연작 셋 중 **litdb 에 들어온 첫 편** ([24] · [44] 는 아직 없음).

---

## 0. 이 digest 를 읽는 법 — 먼저 읽을 것 다섯

1. **이 논문이 Kang 2026 의 [43] 이다 — 그리고 Kang 문장 24 가 [43] 에 기대는 기전은 [43] 에 없다.**
   - 서지: Kang digest (2026-11-06 PDF 직독 시 기록) 의 [43] = *"Park eScience 6, 100502 (2026) 'oxygen-induced lithium inter-cage conduction'"* ↔ 이 PDF 메타 = *eScience* 6 (2026) 100502 · 제1저자 Yongsun Park · 같은 제목 · DOI 10.1016/j.esci.2025.100502 — **저널 · 권 · 논문번호 · 제1저자 · 제목 다섯이 일치**. [44] (*Carbon Energy* 7, e70058 (2025) "site-specific Nb doping") 는 다른 논문이고 이 세션에 없다.
   - 이 논문의 P K-edge 서술 (`Fig. 5d`): *"LSO-LiPSCl shows a **marked increase** in peak intensity … attributed to the **formation of P–O bonds, which reduce the local symmetry of the PS₄ units and consequently increase transition probabilities**."* — **인용 0 · 계산 0** (§5.7).
   - Kang 문장 24: *"a **slight rise** of the white-line intensity at ~2147 eV in LPSOC, attributed to the **increase in unoccupied P states induced by the higher electronegativity of O** [43,44]."* ⇒ 관측 방향은 같고 **기전이 다르다** (대칭 저하 → 전이확률 vs 전기음성 → P 비점유 상태). [43] 은 O 의 전기음성을 *XAS 절 머리말* 과 **S K-edge** (S 주변 전자밀도↓) · **Cl K-edge** 해석에만 쓴다.
   - 크기: 이 논문 백색선 증가는 PDF 벡터 판독으로 **≈ +20 %** (`figure-read ≈` · §5.7) · Kang `Fig. 2g` 의 LPSOC 증가는 픽셀 판독 **≈ +18 %** — **같은 크기를 한쪽은 "marked", 한쪽은 "slight" 라 부른다.** 그런데 명목 O 함량은 **10 배** 다르다 (이 논문 3LSO 0.10 O/f.u. vs Kang LPSOC 1.0 O/f.u.).
2. **조성 대응**: `LiPSCl` = Li₆PS₅Cl = 우리 **comp1** 명목. `LSO-LiPSCl` (본문 기본 시료) = **3LSO-LiPSCl** = 3 mol% Li₂SO₄ + 97 mol% Li₆PS₅Cl → 정련 조성 **Li₅.₉₉PS₄.₉₂O₀.₁₀Cl₀.₉₈** (O 0.10/f.u.). 1LSO · 5LSO 는 `Table S3` · `Table S5`. MD 셀 (`Fig. 5a,b`) 은 **Li₆PS₄.₉₁O₀.₀₉Cl** ("LiPSCl-O 1.9 %") 로 실험 시료와 다르다. **우리 lpsocl (Li₂₇P₅S₂₁OCl₈ = Li₅.₄PS₄.₂O₀.₂Cl₁.₆, Cl 1.6 모체) 와는 모체 Cl 함량이 다르다** — 같은 계가 아니다.
3. **계산은 MLIP-MD 뿐이다.** DFT (VASP · PBE · 550 eV) 와 AIMD 는 **MTP 학습 자료를 만드는 데만** 썼고 (레이블은 optB88-vdW 단일점), **PDOS · Bader · COHP · XANES 시뮬레이션 · O 자리 에너지 비교는 하나도 보고하지 않는다.** SI 는 *"the lowest-energy configuration was selected from all possible site arrangements"* 라고만 쓰고 **그 결과 (O 가 어느 자리가 낮았는지 · 얼마나) 를 안 싣는다** (§8).
4. **"inter-cage 전도 활성화" 의 근거는 ND Rietveld 의 T2–T2 거리 1.77 → 1.65 Å 한 쌍이다** — 우리가 `Table S2`–`Table S5` 좌표로 다시 계산하면 이 값은 **재현된다** (1.771 → 1.645 Å · 그 쌍이 실제로 서로 다른 cage 사이임도 확인). 그러나 같은 계산으로 **5LSO 는 1.786 Å — 무도핑보다 길다** (논문 미보고). 그리고 그 다리 자리 **T2 의 점유는 0.181 → 0.101 로 44 % 줄었다** (§5.5 · §10-②). MTP-MD σ 는 O 에 따라 **단조 감소** (`Fig. S8`) — '활성화' 를 수치로 보인 결과는 없다.
5. **본 digest 에서 실제로 본 그림 (2026-11-09)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` (손 크롭 · XAS 600 dpi + 벡터 판독) `Fig. 6` `Fig. 8` `Fig. S6` `Fig. S8` `Fig. S11` `Fig. S19` `Fig. S22` — **12장** + 비교용 Kang 2026 `Fig. 2` (P K-edge 픽셀 판독).
   썸네일 몽타주 (저해상) 로 크롭만 확인: `Fig. S4` `Fig. S5` `Fig. S7` `Fig. S12` `Fig. S18` `Table S3` — 내용 판독은 안 했고, `Fig. S5` (a 값) · `Fig. S18` (단락 시점) 두 곳만 썸네일에서 대강 읽어 `figure-read ≈ (썸네일)` 로 표시했다.
   **안 본 것**: `Fig. 7` (파우치) · `Fig. S1` `Fig. S2` (ND 적합 — `Fig. 1e,f` 와 같은 꼴) · `Fig. S3` · `Fig. S9` `Fig. S10` (MD 궤적 — `Fig. 5a,b` · `Fig. S11` 과 같은 꼴) · `Fig. S13`–`Fig. S17` · `Fig. S20` · `Fig. S21` · `Fig. S23`–`Fig. S25`. 표 10장은 이미지 대신 **PDF 텍스트로 전 셀 복원**. 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산한 값은 *우리 산수*.

---

## 1. 한 줄 요약

Li₆PS₅Cl 에 **Li₂SO₄ 1–5 mol%** 를 넣어 O 를 들이면 (ND Rietveld 모델상 **16e = PS₄ 꼭짓점** 의 S 를 2.5–4.5 % 치환) σ 는 2.8 → 2.6 mS cm⁻¹ (−7 %) · Ea 0.17 → 0.19 eV 로 **조금만** 나빠지고, 대신 NCM811 복합양극에서 **계면 열화가 줄어** 율속 (9000 mA g⁻¹ 에서 26 → 57 mAh g⁻¹) · 수명 (2C 300 cyc 유지율 76.9 → 83.8 % · 1000 cyc 74.7 %) · 400 Wh L⁻¹ 파우치 500 cyc 이 좋아진다. 저자는 σ 손실이 작은 이유를 **"O 가 Li 를 T2 → T5 로 재배치하고 T2–T2 (cage 사이) 거리를 1.77 → 1.65 Å 로 줄여 inter-cage 전도를 활성화했다"** 로 설명한다 — 이 설명은 ND 평균구조의 작은 변화 + MEM · MD 그림 (정성) 위에 서 있다.

⚠ XAS (`Fig. 5c–e`) 는 **좁은 창 (P 2144–2148 eV) · 0.3 eV 간격 · 정규화/검출 방식 미기재 · 계산 0** 이다. P 백색선 ≈ +20 % 를 저자는 **"P–O 결합의 대칭 저하 → 전이확률↑"** 로 읽는데, Kang 2026 은 같은 현상을 이 논문을 인용하며 **"O 전기음성 → P 비점유 상태↑"** 로 옮겼다 (§0-1 · §5.7 · Kang digest ⏩ 절).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 질문 | 황화물 SE 에 O 를 넣어 **계면 안정** 을 얻되 **σ 손실을 최소화** 하려면 O 를 *어디에* · *무엇으로* 넣어야 하나 |
| 전략 | 산소원 = **Li₂SO₄** (P 가 없어 PS₄ 를 새로 만들지 않음 · Li/(S+O) ≈ 0.4 로 과잉 Li 가 적음) — 선행 [7] 의 Li₃PO₄ · 비교군 Li₂O (`Fig. S21`) |
| 시료 | xLSO-LiPSCl (x = 0 / 1 / 3 / 5 mol% Li₂SO₄) — 볼밀 → 370 MPa 펠릿 → 석영관 **823 K 8 h** (2.6 K min⁻¹ 승온 · 자연냉각) |
| 구조 | ND Rietveld (HANARO · 300 K · Z-Rietveld · Li 4자리 모델 48h(T5) · 48h(T2) · 16e · 24g) + MEM · XRD (Si 내부표준) · Raman · XPS · ³¹P/⁷Li MAS-NMR · tender XAS (P · S · Cl K) · cryo-TEM |
| 계산 | VASP-PBE AIMD → optB88-vdW 단일점 → **MTP** (MLIP) → LAMMPS NPT 300 K · 4×4×4 셀 · MSD → D → Nernst–Einstein σ |
| 셀 | LZO 코팅 NCM811 복합양극 (catholyte 만 LiPSCl vs LSO-LiPSCl) · 분리막 LiPSCl · In–Li (본문) / Li 박 (SI) · 45 °C · 2.5–4.25 V · 파우치 NCM811 ‖ 흑연 |
| 주장 | ① O 는 **16e 선택 치환** ② Li 재배치 (T2 → T5) ③ T2–T2 단축 → **inter-cage 전도 활성화** → σ 손실 최소화 ④ 계면 부반응 억제 (CV · EIS · XPS · cryo-TEM) ⑤ 율속 · 수명 · 파우치 |

---

## 3. 핵심 수치 총정리 ★

### 3a. ND Rietveld 네 시료 (`Table S2`–`Table S5` 전 셀 · 300 K · F-43m) + *우리 산수*

| 항목 | LiPSCl | 1LSO | **3LSO (= "LSO-LiPSCl")** | 5LSO | 출처 |
|---|---|---|---|---|---|
| 표기 조성 | Li₆PS₅Cl | Li₆.₀₀PS₄.₉₅O₀.₀₄Cl₀.₉₈ | **Li₅.₉₉PS₄.₉₂O₀.₁₀Cl₀.₉₈** | Li₆.₁₀PS₄.₈₄O₀.₁₈Cl₀.₉₉ | 표 제목 |
| 명목 O/P (*우리 산수*, 4x/(100−x)) | 0 | 0.040 | 0.124 | 0.211 | SI 합성 비 |
| a (Å, ND) | **9.8584(2)** | 9.8579(1) | **9.8571(2)** | 9.8532(1) | 표 꼬리 · `Fig. 2b` |
| χ² / R_wp / R_p (%) | 1.99 / 4.30 / 3.39 | 2.00 / 4.37 / 3.44 | 1.86 / 4.10 / 3.24 | 2.54 / 4.85 / 3.83 | 표 꼬리 |
| 불순물 Li₂S / LiCl / Li₃PO₄ (wt%) | 0.46 / 0.07 / **0.35** | 0.19 / 0.46 / 0.19 | 0.46 / 0.47 / 0.27 | 0.08 / 0.25 / 0.38 | 표 꼬리 — ⚠ 무도핑에도 Li₃PO₄ |
| **O @16e 점유** | — (S3 = 1 고정) | **0.025(2)** | **0.025(3)** | 0.045(1) | O 좌표 = S3 좌표로 묶음 (`Table S1`) |
| O/f.u. = 4 × occ (*우리 산수*) | 0 | **0.10** (명목 0.04 의 2.5 배) | 0.10 | 0.18 | §10-③ |
| S 4a / S 4d | 0.569 / 0.431 | 0.577 / 0.423 | 0.590 / 0.431 | 0.608 / 0.409 | |
| Cl 4a / Cl 4d | 0.431 / 0.569 | 0.423 / **0.557** | 0.410 / 0.569 | **0.402** / 0.591 | ⚠ 1LSO 4d 합 0.98 · 5LSO 4a 합 1.010 (제약과 불일치) |
| S16e x | 0.1181(2) | 0.1181(1) | 0.1181(2) | 0.1181(1) | **네 정련이 소수 넷째 자리까지 같다** |
| Li 48h(T5) 점유 | **0.301(3)** | 0.343(2) | **0.380(1)** | 0.408(3) | 단조 ↑ |
| Li 48h(T2) 점유 | **0.181(2)** | 0.138(2) | **0.101(3)** | 0.082(1) | 단조 ↓ (−55 % @5LSO) |
| Li 24g / Li 16e | 0.021 / 0.024 | 0.021 / 0.024 | 0.021 / 0.024 | 0.022 / 0.023 | 거의 고정 |
| T2 좌표 | (0.5635, 0.0635, 0.2655) | (0.5590, 0.0590, 0.2610) | (0.5590, **0.5590**, 0.2610) | (0.5641, 0.0641, 0.2661) | ⚠ 3LSO y 는 제약 (x−0.5) 과 어긋남 = 오기로 보임 · **1LSO = 3LSO 좌표 동일** |
| Li/f.u. (*우리 산수*) | 6.01 | 5.99 | 5.99 | 6.10 | 본문 "Li/P 5.99" |
| T5 몫 (*우리 산수*) | 60 % | 69 % | **76 %** | 80 % | 본문 "~76 %" 와 일치 |
| **T2–T2 (cage 사이 · *우리 산수*)** | **1.771 Å** | 1.645 | **1.645** | **1.786** | 본문 `Fig. 4h` 1.77 → 1.65 재현 · **5LSO 는 무도핑보다 길다 (미보고)** |
| 4d–T5 / 4d–T2 (Å, *우리 산수*) | 2.357 / 2.605 | 2.403 / 2.665 | 2.416 / 2.665 | 2.382 / 2.595 | `Table S6` 2.358/2.416 · 2.605/2.665 와 일치 |
| 4d–24g / 4d–Li16e (Å, *우리 산수*) | 2.375 / 4.030 | 2.395 / 4.028 | **2.405 / 4.126** | 2.466 / 4.079 | ⚠ `Table S6` LSO 열 2.388 / 4.030 은 3LSO 좌표로 재현 안 됨 |
| P–S16e (모델 · *우리 산수*) | 2.017 | 2.016 | 2.016 | 2.016 | O 도 같은 좌표 → 모델 안 P–O = 2.02 Å (§10-③) |

*우리 산수* 방법: F-43m 24 개 점대칭 × fcc 4 병진으로 각 자리 궤도를 만들고 주기 경계 최소 거리를 쟀다 (스크래치 스크립트 · 입력 = 표의 좌표와 a 그대로). 가장 짧은 T2–T2 쌍의 두 T2 는 **최근접 4d (cage 중심) 가 서로 다르다** — 논문이 말하는 inter-cage 쌍이 맞다.

### 3b. 수송

| 항목 | 값 | 조건 / 출처 |
|---|---|---|
| σ (RT) | LiPSCl **2.8** · 3LSO **2.6** mS cm⁻¹ (본문) — 벡터 판독 `figure-read ≈` **2.73 / 2.59 / 2.56 / 2.45** (0 / 1 / 3 / 5LSO) | SUS/SE/SUS · 100 mg · 370 MPa · `Fig. 2c` (표지 중심 좌표 ↔ 로그축 눈금 적합) · ⚠ 프레임 밖에 잘린 다섯째 표지 (≈2.41) 가 벡터에 남아 있다 — 무엇인지 미기재 |
| Ea | LiPSCl **0.17** · LSO-LiPSCl **0.19** eV | `Fig. 2d` · 1000/T 3.0–3.41 (≈293–333 K) · 시료당 5 점 · 오차 미기재 · *우리 산수* 기울기 0.169 / ≈0.18 |
| 홉 수 검산 | 0.17 eV: Γ ≈ 1.3×10¹⁰ s⁻¹ · 평균 대기 ≈ 75 ps / 0.19 eV: Γ ≈ 6.1×10⁹ s⁻¹ · ≈ 0.16 ns | ν₀ 10¹³ s⁻¹ **가정** · 298 K · `tools/sei/collect_neb.py::hop_check` · 차수 검산 (확산계수·전도도 아님) — "빠른 전도" 서술과 모순 없음 |
| −10 °C EIS | R_bulk **32 → 40 Ω** · R_gb 453 → 552 Ω · bulk/gb 0.071 → 0.073 | `Table S10` · `Fig. S22` — **고주파 반원이 측정 범위 밖** (첫 점이 이미 −Z″ ≈ 180 Ω) · α₁ = 0.5 두 시료 같음 · 저자도 *"incomplete Nyquist plot limits the reliability"* |
| MTP-MD σ (300 K) | `figure-read ≈` (벡터 막대) **13.0 / 12.1 / 11.8 / 11.4 / 8.0** mS cm⁻¹ (Li₆PS₅Cl / O₀.₀₆ / O₀.₀₉ / O₀.₁₂ / O₀.₂₅) | `Fig. S8` · 시드 · 길이 · 오차 · MSD 창 미기재 · 실험의 ≈4.8 배 · **O 에 단조 감소** |

### 3c. 분광 · 국소구조

| 항목 | 값 | 출처 |
|---|---|---|
| Raman | PS₄ 주봉우리 ≈424 cm⁻¹ + **≈415 cm⁻¹ 어깨** (POₓS₄₋ₓ, 인용 [32,33]) · `figure-read ≈` 어깨 성분 높이 ≈6–8 % | `Fig. 2e` · ⚠ O 함량별 Raman 계열 그림은 **없다** (`Fig. S6` 은 XPS — §10-④) |
| XPS P 2p | PS₄ 이중선 `figure-read ≈` 131.6/132.4 + **≈133 eV 소성분** (POₓS₄₋ₓ, 인용 [34,35]) · O 함량 따라 커진다 (`figure-read ≈` 주성분 대비 0.02 / 0.05 / 0.1) | `Fig. 2f` · `Fig. S6` |
| ³¹P MAS-NMR | 4 성분 A–D (`figure-read ≈` 86.5 / 85 / 83.3 / 81.3 ppm) · O 넣어도 **변화 없음** → "4d 점유 불변" | `Fig. 3a` · ⚠ O 관련 성분을 따로 맞추지 않음 |
| ⁷Li MAS-NMR | 봉우리 **1.33 → 1.20 ppm** (상자장 쪽) · 4 성분 E/F/G/H = 24g / T5 / T2 / 16e 로 배정 | `Fig. 3b` · ⚠ 자리 분리 배정은 빠른 교환과 충돌 (§10-⑤) |
| 전도 평면 넓이 | Plane A **6.757 → 6.755** · Plane B **6.673 → 6.671 Å²** | `Table S7` · `Fig. 4c` — 변화 0.03 % = **a² 비례 축소와 같다** (*우리 산수*: 6.757 × (9.8571/9.8584)² = 6.7552) |
| 4d–S16e | 4.0683 → 4.0677 Å | `Table S8` — 이것도 a 비례 축소 그대로 (분율좌표 동일) |
| T2–T2 | **1.77 → 1.65 Å** | `Fig. 4h` (`figure-read ≈` 1.78 / 1.645) |
| MEM | 음의 산란밀도만 · 등치면 0.035 · 실온 | `Fig. 4e,f` |

### 3d. tender XAS (`Fig. 5c–e` · PDF 벡터 경로 판독 — y 축 눈금값 없음 → 프레임 바닥 기준 상대 높이)

| edge | 표시 창 | 측정 간격 | LSO vs LiPSCl | 저자 해석 |
|---|---|---|---|---|
| **P K** | **2144–2148 eV** | **0.30 eV** (15 점) | 백색선 **≈2147.2 eV** 에서 높이 `figure-read ≈` **+19–21 %** · 상승 가장자리는 겹침 (이동 ≤0.02 eV) · 2148.1 eV 에서 다시 같아짐 | "marked increase" → **P–O 결합이 PS₄ 대칭을 낮춰 전이확률↑** (인용 0 · 계산 0) |
| S K | 2468–2472 eV | 0.30 eV | 주봉우리 `figure-read ≈` +3 % · 가장자리 발치 ≤0.08 eV 고에너지 · 급경사부 이동 ≈0 | "subtle shift" → S 주변 전자밀도↓ (O 가 전자를 끌어감) |
| Cl K | 2824–2830 eV | 0.30 eV | 주봉우리 `figure-read ≈` −5 % (더 넓고 평평) · 상승부 **+0.14–0.20 eV** 이동 · 2829.4 eV 위로는 LSO 가 높음 | "slight shift" → Li(T5)–4d 거리↑ + O16e–4d 거리↓ (`Table S6` · `Table S8`) |

### 3e. 전기화학 · 셀

| 항목 | LiPSCl | LSO-LiPSCl | 조건 / 출처 |
|---|---|---|---|
| CV (Li/SE/SUS · 1 mV s⁻¹ · 30 °C · 0–5 V · 50 cyc) | 1.5–2.7 V 산화환원 봉우리가 사이클 따라 자람 (`figure-read ≈` ≤0.04 mA) | 전류 작음 (≤0.01 mA) | `Fig. 6a,b` · 차이는 **2.5–3.0 V 에서 가장 크다** · 4–5 V 는 둘 다 `figure-read ≈` ≤0.005 mA |
| 0.1C 첫 방전 | ≈230 mAh g⁻¹ · 첫 CE 93.4 % | ≈230 · 94.4 % (1LSO 231.1) | 2.5–4.25 V · 45 °C · `Fig. 6c` · `Fig. S15` |
| 9000 mA g⁻¹ (50C) | **26** | **57** mAh g⁻¹ | `Fig. 6d–f` |
| 900 mA g⁻¹ 300 cyc (율속 뒤) | `figure-read ≈` 135 → 65 | ≈165 → 150 | `Fig. 6d` |
| 360 mA g⁻¹ (2C) 300 cyc | 179.3 → 유지 **76.9 %** · CE 99.91 % | 197.0 → **83.8 %** · 99.93 % | `Fig. 6g` |
| LSO 1000 cyc (2C · 45 °C) | — | 80.9 % (500) · **74.7 % (1000)** · CE 99.94 % | `Fig. 6h,i` · 무도핑 대조 없음 |
| R₂ (양극/SE 계면, 1 → 100 cyc) | **18.5 → 65.3 Ω** | **17.0 → 30.1 Ω** | 45 °C · 4.25 V 충전 후 · `Fig. S17` · `Table S9` |
| 파우치 (NCM811 ‖ 흑연 · N/P 1.2 · 30×40 mm · 45 °C) | — | 0.1C 237.6/210.8 (CE 88.7 %) · 0.33C 195.1 → **78 % (100) · 56.7 % (500)** | `Fig. 7` (안 봄 · 본문 수치) · 400 Wh L⁻¹ 은 집전체 · 파우치 부피 **제외** |
| S 2p XPS (300 cyc 뒤) | 폴리설파이드 (C′) · Li₂S (B′) 크게 증가 | 소폭 | `Fig. S19` |
| cryo-TEM (300 cyc 뒤) | SE 비정질 · NCM 암염층 **≈27 nm** | SE 결정 유지 (0.236 nm 격자줄무늬) · 암염층 **≈8 nm** | `Fig. 8` · 각 1 영역 |

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 전부

### 4a. 합성
- 원료: Li₂S (Alfa 99.9 %) · P₂S₅ (Sigma 99 %) · LiCl (Sigma >99 %) · **Li₂SO₄ (Alfa 99.7 %)**. Ar 글로브박스 (H₂O · O₂ ≤ 0.01 ppm) · ZrO₂ 용기 · Fritsch P-5 유성밀 (**rpm · 시간 미기재**) → 370 MPa 펠릿 → 석영관 823 K 8 h · 2.6 K min⁻¹ · 자연냉각.
- 조성: 1 / 3 / 5 mol% Li₂SO₄ + 99 / 97 / 95 mol% Li₆PS₅Cl (명목). 비교: 10 mol% Li₂SO₄ vs 10 mol% Li₂O (`Fig. S21`) · Li₂SO₄ 를 같은 조건으로 열처리 후 **물리 혼합만** 한 대조 "LSO-mixed LiPSCl" (`Fig. S25`).

### 4b. 구조 분석
- **ND**: HANARO (KAERI) · 10 h · 300 K · 2θ 0–160° · 0.05° 간격 · λ = 1.834467 Å · 바나듐 용기 He 밀봉 · Z-Rietveld · FCJ 프로파일 · Li 4자리 모델 (Masuda 2022) · 다상 (Li₂S · LiCl · Li₃PO₄) · 좌표 → Biso · 점유 순서로 정련. **제약 (`Table S1`)**: O 는 **16e 에만** · 좌표는 S3 와 같게 · 점유 = 1 − S3 · 4a/4d 는 S/Cl 만 (O 선택지 없음).
- **XRD**: X'Pert3 MRD · Cu Kα · 10–60° · 0.013° · Kapton · Si 내부표준 (`Fig. S3` · `Fig. S5`).
- **Raman**: Nanophoton Ramantouch · 532 nm · 3 s × 10 · Ar. **XPS**: Thermo Nexsa · Al Kα · 400 µm · pass 50 eV · 0.1 eV · Ar 이송.
- **NMR**: Bruker Neo 600 · 3.2 mm · MAS 22 kHz · ⁷Li 233.17 MHz (45° 3.4 µs) · ³¹P 242.87 MHz (90° 3.75 µs) · 기준 1 M LiCl(aq) / H₃PO₄(aq). **반복 지연 (recycle delay) 미기재** → ³¹P 성분 넓이의 정량성 판단 불가.
- **tender XAS (P · S · Cl K)**: NSLS-II **8-BM (TES)** · Ar 글로브박스에서 **Mylar 필름 밀봉** — **이것이 전부다.** 검출 방식 (형광/전자수율) · 에너지 보정 기준 · 정규화 (pre/post-edge 창) · 반복 측정 · 시료 두께/희석 **미기재**.
- **cryo-TEM**: FIB Helios 5 UC · 불활성 이송 (IGST) · −130 °C 이하 밀링 · JEOL ARM 200F 200 kV · −160 °C 이하 · EDS X-Max 100TLE.

### 4c. 전기화학
- σ: SUS/SE/SUS · 100 mg · 370 MPa · VMP-300 · 50 mV · 1 MHz–10 mHz · RT (펠릿 두께 미기재). CV: Li/SE/SUS · 30 °C · 1 mV s⁻¹ · 0–5 V · 50 cyc.
- 복합양극: LZO-NCM811 (POSCO Future M) : SE (<1 µm) : Super C65 : NBR = 68.4 : 29.3 : 1 : 1.3 (isobutyl isobutyrate) · Thinky 2000 rpm 3 min · Al 박 · 130 °C 진공 · 5.0–6.0 mg cm⁻² (1C ≈ 0.8 mA cm⁻²). SE 펠릿 10 mm 120 MPa · 양극 370 MPa · **Li 박 9 mm · 200 µm · 20 MPa (SI)** ↔ 본문 그림 캡션은 **In–Li** (§10-⑨). 45 °C · 2.5–4.25 V · 0.1C 화성 · 2C 수명 · CC-CV (CV 종지 = CC 의 20 %) · *"triplicate"* (그림엔 산포 없음).
- 파우치: 양극 12 mg cm⁻² (≈2.5 mAh cm⁻²) · 음극 흑연 : Li₆PS₅Cl : NBR = 60 : 38 : 2 (SUS306 · 3 mAh cm⁻²) · 30×40 / 35×45 mm · 음극 위 Li₆PS₅Cl 50 µm · 분리막 SE (D50 3 µm) : NBR 98 : 2 · WIP 500 MPa · 0.1C 화성 → 0.33C · 45 °C · 10 MPa.

### 4d. 계산 (§8 에 상세)
VASP-PAW-PBE 550 eV · k 밀도 1000/atom · 힘 0.03 eV Å⁻¹ → AIMD (NVT Nosé–Hoover · 350 eV · Γ) → optB88-vdW 단일점 6930 + 1050 구조 → MTP (6 Å · level 10 · 가중 100 : 1 : 0.01) → LAMMPS NPT 300 K · 4×4×4 셀 · MSD → D → σ (Nernst–Einstein).

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 구조 틀 · 상순도 (`Fig. 1`, `Fig. 2a,b`, `Fig. S3`–`Fig. S5`)
- `Fig. 1a–d`: argyrodite 틀 · Li 4 자리 (T5 · T2 · 16e · 24g) · 전도 평면 (S16e–S16e–S/Cl4a · S16e–S16e–S/Cl4d 의 삼각형) · `Fig. 1d` 에 **두 cage 사이 맞닿은 T2 · T2 쌍** 을 그려 놓았다 (우리 거리 계산의 1.77 Å 쌍과 같은 것). ⚠ 범례가 노란 구 (PS₄ 꼭짓점 S16e) 를 **"Li16e"** 로 적었다 — `Fig. 2g` · `Fig. 4a,b` 도 같다.
- `Fig. 1e,f`: ND 적합 (10–150°) — 차분선이 평평하다. 전체 적합의 질은 좋지만, 16e 의 O 2.5 % 같은 작은 신호를 그림으로 판정할 수는 없다.
- `Fig. 2a`: XRD 두 시료 · Si 반사 (○) · 2차상 안 보임. `Fig. S4` (썸네일만 확인 · 서술은 본문 기준): 3LSO 확대 창에 Li₂S (≈27°) · LiCl (≈35°) · Li₂SO₄ 기준선 — 본문: 해당 반사 없음.
- `Fig. 2b`: a 9.8584 → 9.8579 → 9.8571 → **9.8532 Å** (ND 표 값과 같다). ⚠ 캡션은 *"Peak positions were calibrated using added Si"* (XRD 서술) 인데 값은 ND 정련값이다 — XRD 쪽 값은 `Fig. S5` (`figure-read ≈ (썸네일)` 9.849 · 9.849 · 9.848 · 9.8466 — ND 보다 ≈0.009 Å 작고 1LSO 는 무도핑과 같다).

### 5.2 수송 (`Fig. 2c,d`, `Fig. S22`, `Table S10`)
- `Fig. 2c` (로그축 1–4 mS cm⁻¹): 표지 넷 — 벡터 판독 2.73 / 2.59 / 2.56 / 2.45. 삽입 Nyquist 의 고주파 절편이 시료 순서대로 오른쪽으로 밀린다. 전체 −10 % 범위 (5LSO).
- `Fig. 2d`: 두 직선이 거의 평행 — 5 점 · 40 K 창에서 0.02 eV 차는 오차 미기재라 판정하기 어렵다.
- `Fig. S22` · `Table S10` (−10 °C): 두 시료 모두 **하나의 찌그러진 반원** 이고 측정 첫 점이 이미 반원 중간 (Z′ ≈ 20 Ω · −Z″ ≈ 180 Ω) 에 있다 → R_bulk 32 vs 40 Ω 은 **α = 0.5 로 둔 CPE 의 외삽값**이다 (데이터가 받치지 않는다). 다만 총저항 비 (≈1.2) 는 RT σ 비 1.08 에 Ea 차 0.02 eV 를 −10 °C 로 옮긴 값 (*우리 산수* 1.08 × exp(0.02/k × (1/263 − 1/298)) ≈ 1.20) 과 맞는다.

### 5.3 O 자리 판정 (`Fig. 2e–g`, `Fig. S6`, `Fig. 3a`, `Table S1`–`Table S5`)
- 판정 사슬: **(i) ND Rietveld** — O 를 16e 에만 허용한 모델이 O 0.025 (3LSO) 로 수렴 · **4a/4d 에 O 를 둔 대안 모델과의 R 비교는 없다** (`Table S1` 에 그 선택지가 없다). **(ii) Raman** ≈415 cm⁻¹ 어깨 = POₓS₄₋ₓ (인용 [32,33]). **(iii) XPS** P 2p ≈133 eV 소성분 = 산화된 PS₄ (인용 [34,35]). **(iv) ³¹P NMR** 불변 → 4d S/Cl 비 불변 (ND 도 4d 불변 · 4a 의 S↑). 저자: *"conclusive evidence that oxygen is incorporated into the Wyckoff 16e sites"*.
- 우리 평: (ii) · (iii) 은 **P–O 결합이 생겼다** 는 직접 증거 (= O 가 P 에 붙은 자리 = 16e 형) 이다. 그러나 **"O 가 4a/4d 에는 없다" 는 시험되지 않았다** — ND 모델이 처음부터 그 선택지를 뺐고, 중성자 산란길이로 O 는 S 와 Cl 의 사이 값이라 4d 의 S/Cl 비와 O 가 서로 상관된다 (일반 산란 지식 · 이 논문 서술 아님). DFT 자리 에너지는 SI 에 *"lowest-energy configuration"* 한 줄뿐이고 결과가 없다.
- 무도핑 LiPSCl 에도 Li₃PO₄ 0.35 wt% 가 정련된다 (O 오염원 존재) — 그런데 무도핑 XPS 에는 133 eV 성분이 없다 → XPS 소성분은 벌크 Li₃PO₄ 불순물보다는 시료 차이를 따라간다 (방향은 저자 해석 편).
- `Fig. S6` (본 그림): 캡션은 **"Deconvoluted Raman spectra … PS₄³⁻ symmetric stretching"** 인데 그림은 **P 2p XPS** (134–130 eV · LiPSCl / LiPSOCl1 / 3 / 5) 다. 본문은 `Fig. S6` 을 *"Raman … 415 cm⁻¹ 어깨가 O 함량 따라 커진다"* 의 근거로 든다 → **O 함량별 Raman 계열은 어디에도 없다.** XPS 소성분은 함량 따라 커진다 (`figure-read ≈` 0.02 → 0.05 → 0.1). ⚠ 이중선 2p₁/₂ : 2p₃/₂ 높이 비가 LiPSCl ≈0.37 · 나머지 ≈0.5 로 다르다 (스핀궤도 넓이 비 1 : 2 고정 여부 미기재).

### 5.4 Li 재배치와 NMR 배정 (`Fig. 3`, `Table S6`)
- ND: T5 0.301 → 0.380 · T2 0.181 → 0.101 (3LSO) — 네 시료에서 **단조** (T5 0.301 / 0.343 / 0.380 / 0.408 · T2 0.181 / 0.138 / 0.101 / 0.082). 총 Li 는 6.0 근처로 유지.
- `Fig. 3b` ⁷Li: 전체 봉우리가 −0.13 ppm 이동 (1.33 → 1.20). 저자는 0.15 ppm 폭 안을 4 성분으로 나눠 **F = T5 · G = T2 · E = 24g · H = 16e** 로 배정하고, 그 세기 변화 (F↑ · G↓) 가 ND 점유 변화와 맞는다고 쓴다. → §10-⑤ 에서 이 배정이 물리적으로 버티기 어려운 이유.
- `Fig. 3d` 막대 = `Table S6` (LSO 열 2.388 / 2.416 / 2.665 / 4.030 Å). 우리 좌표 재계산으로 T5 · T2 열은 3LSO 와 맞고, 24g · 16e 열은 3LSO 좌표 (2.405 · 4.126) 와 안 맞는다.
- 저자 해석: 4d–Li 거리↑ → 차폐↑ → 상자장 이동. 4d 는 Cl-rich 라 주변 Li 의 전자밀도를 끈다는 서술.

### 5.5 전도 평면 · T2–T2 · MEM (`Fig. 4`, `Table S7`) + 우리 재계산
- `Fig. 4c`: 평면 A · B 넓이가 −0.002 Å² (y 축을 0.01 Å² 폭으로 확대해 큰 차이처럼 보인다). **분율좌표가 네 정련에서 같으므로 이 변화는 a 의 등방 축소 그대로다** (*우리 산수*) — "O 가 국소적으로 통로를 좁혔다" 는 정보가 이 표에는 없다.
- `Fig. 4h`: T2–T2 1.78 → 1.645 Å (`figure-read`). 우리 재계산 1.771 → 1.645 (1LSO · 3LSO 같은 좌표라 같은 값) → **5LSO 1.786 Å**. 저자의 "O 가 T2–T2 를 줄인다" 는 1 · 3LSO 에서만 성립하고 O 가 가장 많은 5LSO 에서 뒤집힌다 — 5LSO 의 σ 가 가장 낮은 것 (2.45) 과는 같은 방향이지만, 논문은 이 값을 내지 않았다.
- `Fig. 4e,f` (MEM · 등치면 0.035): 붉은 선 (LiPSCl) 과 검은 선 (LSO) 은 **손으로 그은 경계** 다. LSO 쪽 노란 등치면이 cage 사이에서 더 이어져 보이지만 정량 (등치면 위상 · 경로 밀도) 은 없다.
- 긴장: **다리 자리 T2 의 점유가 44 % 줄었는데 (0.181 → 0.101) "다리에 Li 가 더 조밀하게 분포한다"** (본문 · MEM · MD 그림) — 자리 간격이 줄어 두 T2 분포가 더 겹쳤다는 해석은 가능하지만, 논문은 이 긴장을 다루지 않는다.
- Li₃PO₄ 경로 (선행 [7]) 는 전도 평면이 *커졌는데* Li₂SO₄ 는 아니다 — 저자: P 공급 유무로 PS₄ 형성이 달라서.

### 5.6 MTP-MD (`Fig. 5a,b`, `Fig. S8`–`Fig. S11`)
- `Fig. S8` (벡터 막대): σ(300 K) 13.0 → 12.1 → 11.8 → 11.4 → 8.0 mS cm⁻¹ (O 0 → 1.25 → 1.875 → 2.5 → 5 %). 저자: 1.9 · 2.5 % 는 *"no significant degradation"* (실험 3LSO 와 같은 거동). 막대 하나씩 · 오차 · 시드 · 궤적 길이 · MSD 창 · 4a/4d 배치 처리 미기재.
- *우리 산수* (Haven = 1 역산): σ ≈13 mS cm⁻¹ 이면 D ≈ 8×10⁻⁸ cm² s⁻¹ → MSD 는 ns 당 ≈5 Å² — 궤적이 수 ns 보다 짧으면 확산 영역 진입이 불확실하다 (길이 미기재라 판정 불가).
- `Fig. 5a,b` (본 그림): 단일 투영 궤적 그림 · 확대창 둘 (두 LiT2 원) — LiPSCl 은 두 원 사이가 성기고 LiPSCl-O 1.9 % 는 꽉 찼다. 검은 점 하나 = "oxygen". **cage 사이 홉 수 · 다리 밀도 같은 수치는 없다**.
- `Fig. S11` (본 그림): 5 % O 에서 O 주변 Li 국재 (확대창 B) · Li 가 빈 영역 (확대창 A). 패널 가운데 세로 검은 선은 두 그림을 이어 붙인 경계로 보인다. 정성.
- ⚠ MD 학습 셀은 **단위정당 O 1 개** (SI *"O : 0.0625 %"* — 16e 16 자리 중 1 = 6.25 % 의 오기로 보인다) — 5 % 셀 (O₀.₂₅ = 단위정당 1 개 평균) 이 학습 조성이고, 낮은 함량은 그 사이 보간이다. PS₄ 하나에 O 둘 (PS₂O₂) 같은 배치는 학습에 없다.

### 5.7 tender XAS (`Fig. 5c–e`) — Kang 문장 24 의 원전 ★★
**측정 조건**: §4b 가 전부 — NSLS-II 8-BM (TES) · Mylar 밀봉. 검출 방식 · 에너지 보정 · 정규화 · 반복 · 두께 미기재. 그림 y 축은 *"Normalized intensity [a.u.]"* 인데 **눈금값이 없다**.
**조성 계열**: **LiPSCl vs LSO-LiPSCl 두 시료뿐** (1 · 5LSO 측정 없음 → O 함량 의존성은 XAS 로 못 본다).

벡터 판독 (`Fig. 5d` P K-edge · 곡선은 PDF 안의 꺾은선 — LSO 실선 15 점 · LiPSCl 은 점선 조각 끝점으로 복원 · 높이 = 프레임 바닥에서 pt):

| E (eV) | 2146.02 | 2146.33 | 2146.63 | 2146.92 | **2147.23** | 2147.53 | 2147.83 | 2148.13 |
|---|---|---|---|---|---|---|---|---|
| LSO-LiPSCl | 34.9 | 54.1 | 80.5 | 120.9 | **132.5** | 121.5 | 92.5 | 69.5 |
| LiPSCl | 36.5 | 52.8 | 76.5 | 102.9 | **≈110.5–111.3** | 106.3 | 86.0 | 69.6 |

- **크기**: 정점 비 1.19 (프레임 바닥 기준) – 1.21 (2143.9 eV 시작값 기준) → **`figure-read ≈` +20 %**. 상승 가장자리 (2146.0–2146.3 eV) 는 두 곡선이 겹치고 (LSO 가 오히려 2 pt 낮음), 2148.1 eV 에서 다시 같다 → **에너지 이동 없이 백색선 꼭대기만 커졌다**.
- **창이 좁다**: 표시 창이 2148 eV 에서 끝난다. Kang `Fig. 2g` (2130–2160 eV) 에는 ≈2151.5 eV 둘째 봉우리 (LPSC₁.₆ ≥ LPSOC > LPSC) 가 보이는데 이 논문 창 밖이다. **P–O 쪽 반결합 상태가 나올 법한 더 높은 에너지 쪽이 그림에 없다** (§7b).
- **간격 0.3 eV**: 백색선 꼭대기는 한 격자점 (2147.23) 에서 정해진다. 두 시료가 같은 격자라 비교는 같은 조건이지만, 시료 간 0.1 eV 보정 차만으로도 꼭대기 높이가 몇 % 움직일 수 있다.
- **저자 해석의 근거**: 인용 0 · 계산 0. *"P–O 결합 → PS₄ 대칭 저하 → 전이확률↑"* 은 **가정** 이다. 우리 평: P 1s → t₂ (P 3p–S 3p 반결합) 는 T_d 에서 이미 쌍극 허용이라, "대칭 저하가 전이확률을 올린다" 는 원래 금지 전이 (전-가장자리) 에 쓰는 논리다 — 주 백색선 20 % 증가의 설명으로는 약하다.
- **양의 산수**: 3LSO 에서 PS₃O 는 P 의 ≈10 % (*우리 산수* — 16e O 0.025 무작위 · 1 − 0.975⁴ = 9.6 %). 백색선 +20 % 를 PS₃O 만으로 내려면 PS₃O 하나가 **같은 에너지에서 PS₄ 의 ≈3 배** 백색선을 가져야 한다 ((1.2 − 0.904)/0.096 ≈ 3.1). PS₃O 는 P–S 결합이 셋으로 줄었으니 오히려 반대다. ⇒ 구조 효과만으로는 크기가 안 맞는다 — 정규화 · 자기흡수 (형광 검출이면 P 농도가 높아 백색선을 누른다) · 입자 크기 · 두께 차를 먼저 의심해야 하는데 그 조건이 하나도 적혀 있지 않다.
- **Kang 과의 교차**: 같은 빔라인 · 같은 교신 그룹의 Kang LPSOC (명목 O 1.0/f.u. · 무작위면 P 의 ≈68 % 가 O 하나 이상 — *우리 산수*) 도 **≈ +18 %** (픽셀 판독). O 가 10 배 많은데 증가가 같다 → O 함량에 비례하는 구조 효과라는 읽기와 맞지 않는다 (Kang 의 O 가 격자에 다 들어갔다는 보장도 없다).
- S K (`Fig. 5c`): 가장자리 발치만 ≤0.08 eV 고에너지 · 급경사부 이동 ≈0 — 측정 간격 (0.3 eV) 보다 작은 이동이다. 저자 해석 (S 전자밀도↓) 은 **인용 0 · 계산 0**. ⚠ 범례 "LPSCl" (다른 패널은 "LiPSCl").
- Cl K (`Fig. 5e`): 상승부 +0.14–0.20 eV · 주봉우리 −5 % 로 넓어짐. 저자 근거 `Table S8` (4d–S16e 4.0683 → 4.0677 Å) 은 **a 비례 축소 그대로이고 O 좌표가 S 와 같게 묶인 모델의 값**이다 — "O16e 가 4d 에 가까워졌다" 는 이 표가 말해 줄 수 없다.

### 5.8 전기화학 (`Fig. 6`, `Fig. S15`–`Fig. S17`)
- `Fig. 6a`: LiPSCl 은 1.5–2.7 V 산화환원 봉우리 (`figure-read ≈` 1.9 · 2.6 V 산화 · 1.5 · 1.8 V 환원) 가 1 → 50 사이클 동안 자란다 — 분해산물 (황 · 폴리설파이드 계열) 의 가역 산화환원으로 보이는 꼴. LSO 는 같은 꼴이 훨씬 작다. `Fig. 6b`: 50 번째 사이클 2.5–3.0 V 에서 차이가 가장 크고 4–5 V 는 둘 다 작다 (`figure-read ≈` ≤0.005 mA).
- `Fig. 6d`: 율속 라벨 "3500" (d) ↔ "3600" (e,f) ↔ SI "20C (3500 mA g⁻¹)" — 20C × 180 mA g⁻¹ = 3600 이 맞다.
- `Fig. 6g`: 2C 300 cyc — 개선의 상당 부분이 **첫 용량 차 (179 vs 197)** 이고, 감쇠 차는 ≈7 %p.
- `Fig. S17` · `Table S9`: R₂ (양극/SE) 증가가 LiPSCl 3.5 배 · LSO 1.8 배. 셀 1 개씩 (산포 없음).

### 5.9 파우치 (`Fig. 7` — 안 봄 · `Fig. S18` 썸네일만)
- 본문: 0.33C 100 cyc 78 % · **500 cyc 56.7 %** — 초록의 *"robust cycling over 500 cycles"* 와 결론의 *"stable operation over 500 cycles"* 는 유지율 57 % 를 말하지 않는다. `Fig. S18`: 30 °C 셀 하나는 단락 (SI 본문 · 시점은 `figure-read ≈ (썸네일)` 33 cyc).

### 5.10 사이클 뒤 화학 · 계면 (`Fig. S19`, `Fig. 8`)
- `Fig. S19` (본 그림): LiPSCl 은 300 cyc 뒤 C′ (`figure-read ≈` 163–165 eV · 폴리설파이드) 가 크게 · B′ (`figure-read ≈` 160 eV · Li₂S) 가 커진다. LSO 는 C′ 소폭 · B′ 거의 그대로.
- `Fig. 8` (본 그림): LSO 쪽 SE 확대창 S1 에 격자줄무늬 (*"0.236 nm (331) plane"*) — ⚠ 저자 자신의 a (9.857 Å) 로 d(331) = a/√19 = **0.226 nm** (*우리 산수* · 4 % 차). LiPSCl 쪽 S2 는 줄무늬 없음 + FFT 무늬 흐림 = 비정질. NCM 표면 암염층 ≈8 nm (LSO) vs ≈27 nm (LiPSCl) — 노란 점선 경계는 손으로 그었고 **시료당 1 영역** 이다.

### 5.11 산소원 비교 · 도핑 확인 (`Fig. S21`–`Fig. S25` — S22 만 봄)
- 10 mol% 에서 Li₂SO₄ → **Li₃PO₄ 2차상** · Li₂O → **Li₂S + LiCl 석출** (본문 · `Fig. S21` 안 봄). 저자: Li₂O 는 O 당 Li 2 개를 더 들여 과잉 Li 가 Li₂S/LiCl 로 빠진다 · Li₂SO₄ 는 (S + O) 당 Li ≈0.4.
- STEM-EDS (`Fig. S23`–`Fig. S25` 안 봄): LSO 는 O 고르게 · 물리혼합 대조는 Li₂SO₄ 나노입자 응집. 저자 스스로 *"EDS analysis alone cannot directly confirm oxygen doping"*.

---

## 6. 메커니즘 종합 — 저자의 사슬과 증거 강도

| 고리 | 저자 주장 | 증거 | 강도 |
|---|---|---|---|
| ① O → 16e (PS₄ 꼭짓점) | "conclusive" | Raman ≈415 어깨 · XPS ≈133 eV (둘 다 인용 해석) + ND (16e 만 허용한 모델) + ³¹P 불변 | **중** — P–O 결합 존재는 서고, 4a/4d 배제는 시험 안 됨 |
| ② Li T2 → T5 재배치 | ND 점유 | 네 시료 단조 (T5↑ · T2↓) · ⁷Li 성분 세기 | **중–약** — ND 평균구조 · RT 큰 Uiso · T5/T2 위치·점유 상관 · NMR 배정은 물리적으로 약함 (§10-⑤) |
| ③ T2–T2 단축 → inter-cage 활성화 | 1.77 → 1.65 Å · MEM · MD 그림 | 좌표 재계산으로 1 · 3LSO 재현 · **5LSO 1.786 역전** · T2 점유 −44 % · MEM 경계 손그림 · MD 수치 0 | **약** |
| ④ intra-cage 는 불리 (평면 축소 · Ea↑) | `Table S7` · `Fig. 2d` | 평면 변화 = a² 축소 (0.03 %) · Ea 차 0.02 eV (오차 미기재) | **약** — '보상' 서사의 한 축이 사실상 0 |
| ⑤ 그래서 σ 손실이 작다 | 2.8 → 2.6 | σ · Ea · MTP-MD 단조 감소 · −10 °C 저항 비 일관 | **관측은 강** · 기전 (③④) 은 약 |
| ⑥ 계면 부반응 억제 → 셀 성능 | CV · EIS R₂ · XPS · cryo-TEM | 방향 일관 · 셀 · 영역 1 개씩 | **중** |
| ⑦ XAS: O 가 전자분포를 바꾼다 | S · P · Cl K | 두 시료 · 좁은 창 · 조건 미기재 · 인용 0 · 계산 0 | **약** (§5.7) |

---

## 7. 우리 계산과의 대조 ★★ (`../our_dft_baseline.md` · `db/properties/` · `db/properties/citation_hazards.json`)

> 규율: 문헌 수치는 소환값이고 우리 절대값과 섞지 않는다. 아래 우리 쪽 칸은 **방향만** 쓴다 (COHP · Bader 는 레지스트리 항목이 아니다).

### 7a. 먼저 확인한 것 — 우리 쪽에서 *인용 가능한* 방향이 있나
- **O 자리**: 원장 허용 문장은 **"O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)"** 하나 (`HZ-nd-site-cfg23-mislabeled` · 크기 인용 금지). 우리 LPSOCl 구조는 O 를 POS₃ (16e 형) 에 **구성으로** 넣었다 — 자리 선호의 근거가 아니다.
- **수송**: 우리 lpsocl · modelc MD 의 순위 · O 효과 서술은 원장상 막혀 있다 — `HZ-cross-system-Ea` (BLOCKED) · `HZ-lpsocl-Ea-diffusive-gate` (HOLD) · b2o3 쪽 `HZ-sigma-ratio-non-citable` · `HZ-b2o3-md-ea` (BLOCKED). ⇒ **이 논문의 σ · Ea 옆에 우리 MD 를 나란히 쓰지 않는다.**
- **전자구조 (방향)**: `kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md` (b2o3 COHP 비점유측) · `kb/methodology/electron_localization_framework_2026_07_08.md` · `db/properties/lpsocl_bader_ae.json` (같은 AE-PAW 방법 3 계) · `db/properties/lpsocl_dos_gap.json` (O 단독 계 DOS 노트) · `db/properties/lpsocl_cohp_curves_origin.csv` (O 단독 계 COHP 곡선). 전부 PBE 바닥상태 · 코어홀 없음 · XANES 계산 아님.

### 7b. P K-edge 백색선 ↔ 우리 비점유 상태 (방향만)

P K-edge 백색선 = P 1s → (쌍극) P p 성분을 가진 비점유 상태 ≈ **전도띠의 P p 투영** — 우리 언어로 P–S · P–O 반결합 σ\*.

| 질문 | 이 논문 / Kang 문장 24 | 우리 (방향) | 판정 |
|---|---|---|---|
| ≈2147 eV 백색선은 무엇인가 | (둘 다 말하지 않음) | LPSCl 계 CB 바닥 = **P–S σ\*** — COHP 상 P–S 반결합은 CBM 에서 사실상 바로 시작 · CB 바닥 조성 S · P 대부분 (O 0 %) | 같은 대상을 본다 — 백색선 = P–S σ\* 의 P p 몫 |
| O 가 P 의 전자를 끄는가 | Kang: 전기음성 → (암묵) · 이 논문: P 에 대해선 말 안 함 (S 에 대해서만) | **Bader: P 순전하가 O 결합 수를 따라 + 쪽으로 단조** (LPSCl1.6 → LPSOCl → b2o3 · 같은 AE-PAW) | **같은 방향** |
| 새 비점유 P 상태는 *어디* 에 생기나 | Kang: ≈2147 eV 백색선에서 "unoccupied P states↑" · 이 논문: 같은 에너지에서 "전이확률↑" | **P–O σ\* 는 P–S σ\* 보다 훨씬 위** (b2o3 COHP onset 차) · **O 단독 계 (LPSOCl) 에서도 P–O 반결합 주봉우리는 CB 바닥 (P–S) 위쪽** · LPSOCl DOS: *"O introduces NO states at either band edge"* | **다른 말** — 바닥상태 그림에선 O 가 만드는 P 쪽 빈 상태는 백색선 꼭대기가 아니라 **더 높은 에너지** (이 논문 창 2148 eV 밖) 에 놓인다 |
| 백색선 자체 (P–S σ\*) 의 P p 몫이 PS₃O 에서 커지나 | (둘 다 이 경로를 말하지 않음) | **안 쟀다** — PS₃O 대 PS₄ 의 자리분해 P-p PDOS 없음 | 열림 — 유일하게 남는 구조적 경로 |
| S 의 전자밀도 | 이 논문: S K-edge 고에너지 이동 → **S 전자밀도↓** | **Bader: S 평균 순전하는 O 를 넣을수록 − 쪽** (P 가 내준 만큼 S 가 받는다) | **반대 방향** — 단 그 이동은 ≤0.08 eV (간격 0.3 eV 미만) |
| Cl | 이 논문: Cl K-edge +0.14–0.20 eV (기하 해석) | Bader: Cl 불변 | 전하 이동으로 읽을 근거가 우리 쪽에 없다 (기하 · Li 배위 효과는 가능) |

- **한 줄**: "O 가 P 에서 전자를 끈다" 는 우리 Bader 와 **같은 방향**이다. 그러나 "그래서 ≈2147 eV 백색선 (= P–S σ\*) 에 P 빈 상태가 늘어난다" 는 우리 바닥상태 COHP/DOS 와 **다른 말**이다 — 우리 계산에서 O 쪽 반결합은 CB 바닥보다 높은 곳에 따로 생기고, CB 바닥 조성에 O 몫은 0 이다. 이 논문 자신의 해석 (대칭 저하 · 전이확률) 은 우리가 평가할 계산이 없다.
- **한계**: PBE 바닥상태 · 코어홀 (최종상태) 효과 없음 · b2o3 계에는 B 가 섞여 있다 · LPSOCl 은 P 5 개 중 1 개만 PS₃O. 이 질문을 닫는 계산은 **코어홀 XANES 시뮬레이션 (PS₄ vs PS₃O)** 또는 최소한 **PS₃O 자리의 P-p 투영 PDOS** 다 — 계산하려면 먼저 보고량 카드 (`kb/templates/estimand_card.md`) 부터.

### 7c. O 자리
- 이 논문: **16e** (Raman · XPS 로 P–O 결합 존재 + 16e 만 허용한 ND 모델). 우리: "O 는 16e 를 4d 보다 선호 (UMA · Nd@Li 셀)" — **방향이 같다**. 증거 종류는 다르다 (분광 + 모델 가정 vs MLIP 에너지). ⛔ 크기 (원장 차단 수치) 는 쓰지 않는다.
- Kang 2026 (lab XRD, 점유 미제시) · Zhao 2025 (O@4d) 와 함께 보면 O 자리는 **합성 경로 의존** 일 수 있다 — 이 논문은 Li₂SO₄ 고상법 · 823 K.

### 7d. 수송 — 나란히 쓰지 않음
- 이 논문 σ 2.8 → 2.6 · Ea 0.17 → 0.19 · MTP-MD 13.0 → 11.8 (1.9 %) 는 **문헌값으로만** 둔다. 우리 MD 와의 대조는 위 원장 차단 때문에 하지 않는다.
- 다만 **방법 교훈** 은 쓸 수 있다: 이 논문의 MD 수송값도 단일 막대 · 길이/시드/창 미기재 — 우리 규율 (멀티시드 · MSD 2–50 ps 창 · 확산 게이트) 로 보면 판정 불가 범주다.

### 7e. 🔑 층위를 갈라 쓴 결론
1. **관측**: O 를 넣은 시료에서 P K 백색선이 ≈20 % 크다 — 측정은 있다 (조건 미기재).
2. **해석 (이 논문)**: 대칭 저하 → 전이확률 — 인용 · 계산 없는 가정.
3. **해석 (Kang 문장 24)**: 전기음성 → P 비점유 상태 — [43] 에 없는 기전. 우리 바닥상태 계산은 '전자를 끈다' 까지만 같은 방향이고 '백색선 에너지에서 빈 상태 증가' 는 지지하지 않는다.

---

## 8. DFT / 계산 방법 ★

- **code**: VASP (PAW) · LAMMPS (MD) · MLIP 패키지 (MTP, Novikov 2021) · 참고 Qi 2021 (*Mater. Today Phys.*).
- **functional**: 구조 이완 · AIMD = **PBE** · 학습 레이블 = **optB88-vdW 단일점** (AIMD 표본 위에서 다시 계산).
- **ecut / k**: 550 eV · k 밀도 1000/atom (이완) · AIMD 350 eV · Γ 만. 힘 수렴 0.03 eV Å⁻¹ · 전자 10⁻⁵ eV.
- **AIMD (학습 자료)**: 결정 3 계 — 4a/4d 무질서 · 4a/4d 질서 · O 1 개 넣은 무질서 계 — 각각 *"lowest-energy configuration … from all possible site arrangements within the unit cell"* (결과 미보고). 300 / 600 / 900 / 1200 K × 변형 −5 / 0 / +5 % · 0.5 K fs⁻¹ 가열 · 20 ps 평형 · 10 ps 생산 · 0.1 ps 간격 → 계당 1200 표본. 비정질: 4000 K 10 ps 용융 → 2000 K 20 ps → 100 K ps⁻¹ 로 300 K 담금질 · 변형 3 종 → 계당 1110. 원소 (Li · P · S) · 이원 (LiCl · Li₂O): 300 → 1000 K 42 ps 가열 · 0.2 ps 간격. 합계 argyrodite **6930** + 전구체 **1050** 구조 (*우리 산수*: 3 계 × (1200 + 1110) = 6930 · 맞는다).
- **MLIP**: MTP · 차단 6 Å · max level 10 · 손실 가중 에너지 : 힘 : 응력 = 100 : 1 : 0.01. 검증 지표 (RMSE · 시험셋 · 외삽 등급) **미보고**.
- **MD**: LAMMPS NPT 300 K · 4×4×4 셀 (≈3328 원자 — *우리 산수*, 52 원자 × 64) · MSD → D (식 1) → σ (Nernst–Einstein, Haven 언급 없음) · 궤적 길이 · 시간간격 · 시드 · MSD 창 · O 배치 규칙 **미기재**.
- **무질서 처리**: 학습에 무질서 · 질서 모두 포함 · MD 셀의 4a/4d · O 배치 방법 미기재 (단일 배치로 보인다).
- **특이사항**: 계산은 **σ 의 O 의존성 정성 확인 + 궤적 그림** 에만 쓰였다. 전자구조 (DOS · Bader · COHP) · XANES · 자리 에너지 · NEB 는 없다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a–d | argyrodite 틀 · Li 4 자리 · 전도 평면 · 두 cage 사이 T2 · T2 쌍 (본 그림) | Li 자리 이름 (T5/T2/16e/24g) 대응표 — ⚠ 범례 "Li16e" 가 S16e 를 가리킴 |
| 1e,f | ND Rietveld 적합 LiPSCl / LSO (본 그림) | 적합 질 확인용 — 16e O 판정 근거로는 부족 |
| 2a,b | XRD · a (ND 값) (본 그림) | a 축소 9.8584 → 9.8532 Å (O 넣을수록) |
| 2c,d | σ · Nyquist · 아레니우스 (본 그림 · 2c 벡터 판독) | σ 2.73/2.59/2.56/2.45 (`figure-read ≈`) · Ea 0.17/0.19 — 문헌값으로만 |
| 2e,f | Raman 415 어깨 · P 2p 133 eV (본 그림) | P–O 결합 존재의 분광 근거 (O@16e 형) |
| 2g | O@16e 모식도 (본 그림) | ⚠ 범례 오기 |
| 3a,b | ³¹P · ⁷Li MAS-NMR 성분 분해 (본 그림) | ³¹P 불변 (4d 불변 주장) · ⁷Li 자리 배정은 쓰지 않는다 (§10-⑤) |
| 3c–f | 4d 주변 Li 배치 · 4d–Li 거리 · 점유 (본 그림) | T5 0.30 → 0.38 · T2 0.18 → 0.10 |
| 4a–c | 전도 평면 A/B 넓이 (본 그림) | 변화 = a² 축소 — 기전 근거로 쓰지 않는다 |
| 4d–g | MEM Li 분포 · cage 연결 모식 (본 그림) | 정성 그림 (손그림 경계) |
| 4h | T2–T2 1.78 → 1.645 Å (본 그림) | 우리 재계산 재현 · 5LSO 1.786 역전 (§5.5) |
| 5a,b | MTP-MD 궤적 투영 LiPSCl vs LiPSCl-O 1.9 % (본 그림 · 손 크롭) | 정성 — 수치 없음 |
| 5c–e | tender XAS S · P · Cl K (본 그림 · 벡터 판독) | **P 백색선 `figure-read ≈` +20 % · 창 2144–2148 eV · 0.3 eV 간격** — Kang 문장 24 원전 (§5.7 · §7b) |
| 6a,b | CV 0–5 V 50 cyc (본 그림) | 차이는 2.5–3.0 V · 산화 축 B① 의 실험 측 (S 계 산화환원) |
| 6c–i | 화성 · 율속 · 2C 300/1000 cyc (본 그림) | 셀 성능 — 축 밖 |
| 7 | 파우치 (안 봄) | 본문 수치만 (500 cyc 56.7 %) |
| 8 | cryo-TEM SE 결정성 · NCM 암염층 8 vs 27 nm (본 그림) | 계면 열화 정성 · ⚠ d(331) 0.236 vs 0.226 nm |
| S1, S2 | 1LSO · 5LSO ND 적합 (안 봄) | — |
| S3 | XRD 계열 + Si (안 봄) | — |
| S4 | Li₂S · LiCl · Li₂SO₄ 확대 비교 (썸네일만) | 2차상 없음 주장 |
| S5 | XRD a (Si 보정) (썸네일만) | ND 보다 ≈0.009 Å 작다 (`figure-read ≈ (썸네일)`) |
| S6 | **캡션은 Raman, 그림은 P 2p XPS** (본 그림) | O 함량 따라 133 eV 성분↑ · Raman 계열은 없다 |
| S7 | 4a/4d S/Cl 섞임과 P 배위 모식 (썸네일만) | — |
| S8 | MTP-MD σ vs O 함량 (본 그림 · 벡터 판독) | 13.0 → 8.0 단조 감소 · 오차 없음 |
| S9, S10 | MD 궤적 비교 · O 함량별 (안 봄) | — |
| S11 | 5 % O 에서 O 주변 Li 국재 (본 그림) | 정성 |
| S12 | LZO-NCM811 XRD (썸네일만) | — |
| S13, S14 | NCM SEM-EDS · SE 입자 (안 봄) | — |
| S15, S16 | 화성 · 율속 계열 (안 봄) | 1LSO 231.1 mAh g⁻¹ (본문) |
| S17 | 등가회로 · 1/100 cyc Nyquist (안 봄) | R₂ 18.5 → 65.3 vs 17.0 → 30.1 Ω (`Table S9`) |
| S18 | 파우치 30 vs 45 °C (썸네일만) | 30 °C 셀 하나 단락 |
| S19 | 사이클 전후 S 2p XPS (본 그림) | 폴리설파이드 · Li₂S 증가 억제 |
| S20 | 사이클 뒤 EDS 지도 (안 봄) | — |
| S21 | 10 mol% Li₂SO₄ vs Li₂O 2차상 · σ (안 봄) | Li₃PO₄ vs Li₂S + LiCl (본문) |
| S22 | −10 °C Nyquist · 등가회로 (본 그림) | R_bulk 은 외삽값 — 정량 근거로 약함 |
| S23–S25 | HAADF-STEM-EDS O 분포 · 물리혼합 대조 (안 봄) | 저자도 EDS 로 도핑 확정 불가라 씀 |
| Table S1 | ND 정련 제약 (텍스트) | **O 는 16e 에만 · 좌표 = S3** |
| Table S2–S5 | 네 시료 정련 결과 (텍스트) | §3a 전 셀 · 우리 거리 재계산 입력 |
| Table S6 | 4d–Li 거리 (텍스트) | LSO 열 일부가 3LSO 좌표로 재현 안 됨 |
| Table S7, S8 | 전도 평면 넓이 · 4d–S16e (텍스트) | 둘 다 a 비례 축소 그대로 |
| Table S9, S10 | EIS 적합값 (텍스트) | — |

---

## 10. 비판 — 이 논문의 약한 곳 ★

1. 🔴 **"Oxygen doping enables inter-cage conduction in argyrodite *for the first time*" (Highlights) 는 성립하지 않는다.** 무도핑 Li₆PS₅Cl 이 이미 2.8 mS cm⁻¹ 을 낸다 — 장거리 확산에는 cage 사이 홉이 반드시 들어간다. 이 논문이 보인 것은 많아야 "cage 사이 자리 간격이 줄었다" 다.
2. 🔴 **inter-cage '활성화' 근거의 내부 긴장**: ① T2–T2 단축은 1 · 3LSO 에서만 · **5LSO 는 1.786 Å 로 역전** (우리 재계산 · 미보고) ② **다리 자리 T2 점유가 44 % 감소** 하는데 "다리에 Li 가 조밀" ③ MEM 경계는 손그림 · MD 는 그림뿐 · MTP-MD σ 는 O 에 단조 감소. '보상' 의 다른 축 (평면 축소) 은 a² 축소 0.03 % 라 사실상 0.
3. 🔴 **Rietveld 표의 정합성**: ① 1LSO 정련 O 0.025 → **0.10 O/f.u. = 명목 (0.04) 의 2.5 배** (*우리 산수*) — Li₂SO₄ 1 mol% 가 공급할 수 없는 양 ② 1LSO 와 3LSO 의 T2 좌표 · O 점유가 같다 ③ S16e x 가 네 정련에서 0.1181 로 같다 ④ 1LSO 4d 점유합 0.98 · 5LSO 4a 합 1.010 (`Table S1` 제약 위반) ⑤ 3LSO T2 y 오기 ⑥ `Table S6` LSO 열 일부 재현 안 됨 ⑦ **O 를 S 좌표에 묶은 모델** — 모델 안 P–O = P–S ≈ 2.02 Å (*우리 산수*) 인데 실제 P–O 결합은 그보다 훨씬 짧다. ⇒ O 점유 0.025 의 정밀도 (±0.002–0.003) 를 그대로 믿기 어렵다 · **O@4a/4d 대안 모델 비교 없음**.
4. 🟠 **그림–본문 어긋남**: `Fig. S6` (캡션 Raman · 그림 XPS · 본문은 Raman 계열의 근거로 인용) · `Fig. 2b` 캡션 (XRD Si 보정) ↔ 값 (ND) · 범례 "Li16e" (`Fig. 1` `Fig. 2g` `Fig. 4`) · `Fig. 5c` "LPSCl" · `Fig. 6d` "3500" ↔ "3600" · `Fig. 8` d(331) 0.236 vs 0.226 nm · 1LSO 표기 조성 (O₀.₀₄ · S₄.₉₅) ↔ 정련 (O 0.10 · S 4.90). SI 텍스트층에 옛 번호 캡션이 겹쳐 남아 있다 (S3 ↔ S1 · S6 ↔ S3 · S8 ↔ S5 · S12 ↔ S8 · S16 ↔ S12) — 재번호 과정의 흔적.
5. 🔴 **⁷Li 자리 분리 배정**: 실온 argyrodite 의 Li 는 자리 사이를 ns 이하 시간척도로 오가고 (위 홉 검산: 대기 ≈0.1 ns), 자리 간 화학적 이동 차 ≈0.1 ppm 은 233 MHz 에서 ≈23 Hz 다 — **빠른 교환 한계라 한 줄로 평균된다.** 0.15 ppm 폭 안의 4 성분을 T5 · T2 · 24g · 16e 로 배정하고 세기를 점유와 맞추는 것은 물리적으로 받치기 어렵다 (선 모양 비대칭은 시료 불균일 · 자화율 등으로도 생긴다). −0.13 ppm 이동도 외부 기준 · MAS 마찰열 범위 안이다.
6. 🔴 **XAS (§5.7)**: 두 시료 · 좁은 창 · 0.3 eV · 정규화/검출/보정 미기재 · 인용 0 · 계산 0 · 크기가 PS₃O 비율로 설명 안 됨 (≈3 배 필요) · Kang (O 10 배) 과 같은 크기 · S K 이동은 간격보다 작음 · Cl K 근거 (`Table S8`) 는 모델이 고정한 값.
7. 🟠 **³¹P NMR 의 침묵**: PS₃O 가 P 의 ≈10 % (*우리 산수*) 라면 ³¹P 에 별도 성분이 기대되는데, 100–70 ppm 창에서 S/Cl 배위 4 성분만 맞추고 O 관련 성분은 다루지 않는다. 반복 지연 미기재.
8. 🟠 **MD**: 시드 · 길이 · 창 · 오차 미기재 · 300 K 한 점 · MTP 검증 지표 없음 · O 자리 선택 결과 미보고 · 학습 O 함량 단일 (단위정당 1 개).
9. 🟠 **셀 기록**: 본문 In–Li ↔ SI Li 박 · *"triplicate"* 인데 산포 없음 · 파우치 400 Wh L⁻¹ 은 집전체 · 케이스 제외 · 500 cyc 56.7 % 를 "robust/stable" 로 씀 · 2C 개선의 상당 부분은 첫 용량 차.
10. 🟠 **−10 °C 벌크 저항** 은 측정 범위 밖 반원의 외삽 (α = 0.5 고정으로 보임) — 저자 스스로 신뢰도 한계를 적었다.
11. 🟡 **cryo-TEM** 시료당 1 영역 · 손그림 경계 · "for the first time" (결정→비정질 직접 관찰) 은 우리가 검증할 수 없다.
12. 🟡 **데이터 공개 없음** (요청 시).

---

## 11. 우리 원장 매핑 (요약)

| 원장 항목 | 이 논문이 주는 것 | 처리 |
|---|---|---|
| `HZ-nd-site-cfg23-mislabeled` (O 자리 허용 문장) | O@16e 실험 주장 한 점 (분광 + 모델 가정) | 허용 문장과 **방향만 같다** · 크기 비교 안 함 |
| `HZ-cross-system-Ea` · `HZ-lpsocl-Ea-diffusive-gate` · `HZ-sigma-ratio-non-citable` · `HZ-b2o3-md-ea` | 문헌 σ · Ea · MTP-MD σ | **나란히 쓰지 않음** |
| 전자구조 (b2o3 COHP · LPSOCl DOS · AE-PAW Bader) | P K 백색선 ≈+20 % · 두 갈래 해석 | §7b — '전자를 끈다' 같은 방향 · '백색선 에너지에서 빈 상태↑' 다른 말 |
| Kang 2026 문장 24 [43,44] | [43] = 이 논문 · 기전 불일치 | Kang digest 끝 ⏩ 절 |
| 산화 축 B① (CV) | Li/SE/SUS CV 차이는 2.5–3.0 V 쪽 | 축 명명 규율 그대로 — ESW onset 은 S 지배 |

---

## 12. 적용 인사이트 ★

1. **Kang 문장 24 를 원고 · 덱에서 쓸 때**: 관측 ("O 치환 시 P 백색선 소폭↑") 은 [43] 으로 받칠 수 있지만 **기전 ("O 전기음성 → P 비점유 상태↑") 은 [43] 이 말하지 않는다** — 쓰려면 기전을 빼거나 "attributed by the authors to symmetry lowering by P–O bonds" 로 바꿔야 한다. 우리 바닥상태 계산은 그 기전 문장을 지지하지 않는다 (§7b).
2. **XANES 를 계산으로 붙일 기회**: 우리에겐 PS₃O 를 품은 이완 구조 (LPSOCl V0) 가 이미 있다. 코어홀 P K-edge 시뮬레이션 (PS₄ vs PS₃O) 한 쌍이면 "백색선 +20 % 가 구조로 설명되는가" 를 가를 수 있다 — 단 새 계산이므로 보고량 카드부터 · GPU · 사용자 결정.
3. **O 자리 근거 지도**: Kang (lab XRD · 점유 미제시) · 이 논문 (ND 16e 만 허용 + Raman/XPS) · Zhao 2025 (4d) — 셋 다 대안 모델 비교가 없다. CEI 트랙의 O · Nd 자리 서술은 여전히 "방향만" 이다.
4. **방법 교훈 (수송)**: 평균구조 Rietveld 의 Li 거리 0.1 Å 변화를 기전으로 쓰기 전에 **같은 표의 다른 조성** 으로 단조성을 확인한다 — 이 논문은 5LSO 에서 스스로 뒤집혔다.

---

## 13. 인용 가능 문장 (영문 초안 · 조건 포함)

- ✅ "Oxygen introduced via Li₂SO₄ forms P–O-bonded PS₄₋ₓOₓ units in Li₆PS₅Cl, as indicated by a Raman shoulder at ~415 cm⁻¹ and a P 2p component at ~133 eV, with only a small decrease in ionic conductivity (2.8 → 2.6 mS cm⁻¹) (*eScience*, 6, 100502 (2026))."
- ✅ "In O-doped Li₆PS₅Cl, the P K-edge white line at ~2147 eV is higher than in the undoped material (*eScience*, 6, 100502 (2026)); the authors attribute this to symmetry lowering of PS₄ units by P–O bonds." — 조건: 기전은 저자 해석으로만.
- ⛔ "…attributed to an increase in unoccupied P states induced by the higher electronegativity of O (*eScience*, 6, 100502 (2026))" — [43] 에 없는 기전.
- ⛔ "Oxygen doping enables inter-cage conduction for the first time" — 무도핑에도 inter-cage 홉은 있다.
- ⛔ 이 논문의 MD σ (13 → 8 mS cm⁻¹) 를 실험 σ 의 확인 · 우리 MD 의 대조로 인용.

---

## 14. 주의 / 한계 (인용 규율)

- 문헌 σ · Ea · MD σ 는 소환값 — 우리 MD 값과 같은 표 · 같은 문장에 두지 않는다 (§7a 원장 차단).
- XAS 수치는 전부 **벡터/픽셀 `figure-read ≈`** (눈금값 없는 축의 상대 높이) — 절대 백색선 세기로 쓰지 않는다.
- 우리 재계산 거리 (§3a) 는 **논문 표 좌표의 산수** — 새 측정이 아니다. 오기 (3LSO T2 y) 는 제약대로 고쳐 계산했다.
- O@16e 는 "P–O 결합 존재 + 16e 만 허용한 모델" 까지가 근거다 — "4a/4d 에 O 가 없다" 로 쓰지 않는다.

---

## 15. 기법 용어 미니사전

- **tender XAS**: 2–5 keV X-선 흡수 분광 — P (≈2145 eV) · S (≈2470 eV) · Cl (≈2825 eV) K-edge 가 이 영역이다. 진공/He 환경 · 얇은 창 (Mylar) 이 필요하다.
- **백색선 (white line)**: K-edge 바로 위 첫 큰 흡수 봉우리 — 쌍극 허용 (1s → p) 최종상태의 비점유 p 상태밀도와 국소 구조를 반영한다. 세기는 정규화 · 자기흡수 · 두께에 민감하다.
- **정규화 (edge-step normalization)**: 가장자리 아래 (pre-edge) 를 0, 훨씬 위 (post-edge) 를 1 로 맞추는 처리 — post-edge 창이 그림에 없으면 독자가 확인할 수 없다.
- **자기흡수 (self-absorption)**: 형광 검출에서 흡수원 농도가 높으면 백색선이 눌리는 효과 — 입자 크기 · 충전 밀도에 따라 시료마다 달라진다.
- **Rietveld 정련 (ND)**: 중성자 회절 패턴 전체를 구조 모델로 맞춰 좌표 · 점유 · 열진동을 얻는다. 중성자는 Li 가 보인다 (음의 산란길이). **모델에 없는 선택지 (예: O@4d) 는 결과에도 없다.**
- **MEM (최대 엔트로피법)**: 정련된 구조인자로 산란밀도 지도를 재구성 — Li 는 음의 밀도로 보인다. 등치면 값 선택에 따라 '연결' 이 달라 보인다.
- **T5 / T2 (48h)**: argyrodite Li 의 두 48h 자리 — T5 는 cage 안 주 자리, T2 는 이웃 cage 와 맞닿은 면 쪽 자리 (inter-cage 다리).
- **inter-cage / intra-cage 홉**: 4d 를 중심으로 한 Li cage 안의 홉 vs cage 사이 홉 — 장거리 확산에는 둘 다 필요하다.
- **MTP (moment tensor potential)**: 원자 주변 환경을 모멘트 텐서로 표현하는 MLIP — 학습 자료 밖 (외삽) 배치에서 오차가 커진다.
- **빠른 교환 (fast exchange) 한계**: 자리 사이 교환 속도가 화학적 이동 차 (Hz) 보다 훨씬 빠르면 NMR 에 한 줄 평균만 남는다.
- **CPE (constant phase element)**: 등가회로에서 이상 커패시터 대신 쓰는 요소 — α = 1 이면 커패시터, 0.5 면 확산형.
