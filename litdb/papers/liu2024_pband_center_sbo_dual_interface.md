# Regulating p-Band Center of Sulfur in Li-Argyrodite to Stabilize Dual Solid–Solid Interface for Robust All-Solid-State Lithium–Sulfur Battery — Chong Liu (Adv. Funct. Mater. 2024/2025)

> slug `liu2024_pband_center_sbo_dual_interface` ·
> DOI `10.1002/adfm.202412144` ·
> type `exp 주 (합성·전기화학·XPS/XANES/NPD/TOF-SIMS) + DFT 보조 (PDOS·p-band center·CI-NEB 1건·계면 흡착/전하밀도차·AIMD 10 ps)` ·
> *Adv. Funct. Mater.* **2025, 35, 2412144** (접수 2024-07-09 · 수정 2024-09-11 · 온라인 **2024-10-10**) ·
> PDF `inbox/84. Liu2024_pBand_Center_Sulfur_Argyrodite_Dual_Interface.pdf` (본문 **14 pp**)
> + `inbox/84. Sup) …docx` (SI: Experimental + **Theoretical calculations methods** + Fig S1–S47 + Table S1–S11) ·
> digested `2026-09-01` · 태그 **[외부]** · status ✅

> elements: Li, P, S, Cl, Sb, O, C, In, Cu
> methods: DFT, AIMD, NEB, DOS, PDOS, XPS, Raman

<!-- 태그 근거 (2026-09-01):
     · elements — Li/P/S/Cl = LPSC host, Sb/O = 공도펀트(Sb2O3 전구체), S = S8 양극(host 와 겹침),
       C = CNTs 도전재, In = 파우치셀 Li-In 음극, Cu = Li/Cu 비대칭셀(CE·핵생성 과전압).
       ⛔ F 는 빼야 한다 — LiF 0.67 eV 는 이 논문이 **인용한 남의 값**이고 F 를 다루지 않는다.
     · methods — 실제로 한 것만. DFT(VASP/PBE/PAW) · AIMD(CP2K 10 ps) · NEB(CI-NEB 1건) ·
       DOS/PDOS(+p-band center) · XPS(Sb 3d·S 2p·P 2p·Li 1s·Cl 2p·O 1s, Ar⁺ depth) · Raman.
       이 논문은 **Bader·COHP/ICOHP·ELF·BVSE·포논·탄성·MLIP·grand-potential ESW 를 하나도 하지 않는다**(§8-D).
       EIS/DRT/CV/Tafel/XANES/NPD-Rietveld/TOF-SIMS/TGA/GITT 는 Glossary 어휘에 없어 뺐고 §13 에 전부 있다. -->

---

## 0. 이 digest 를 읽는 법
- **§6.4 + §8 이 이 digest 의 존재 이유다.** 1저자가 물은 "Li₂S 0.22 eV" 의 정체 판정이 §6.4 에 있고,
  "왜 우리 0.305 eV 와 직접 비교가 안 되는가" 가 §11 에 있다.
- 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다. 본문 인쇄값과 구분한다.
- 논문 수치는 전부 **소환값**이다 — 우리 db 절대값과 같은 칸에 넣지 않는다 (CLAUDE.md 규율).

## 1. 한 줄 요약
Li₆PS₅Cl 의 **P 자리에 Sb, PS₄-S 자리에 O 를 동시에 넣어**(Sb₂O₃ 고상반응, x=0.05) PS₄ 사면체 일부를 **SbS₄ 로 바꾸면
S-p 밴드중심 ε_p 가 −2.06 → −2.57 eV 로 내려가고**, 그 한 번의 전자구조 변화가 **음극쪽(Li 금속)에서는 빠른
Li_xSb_yS_z 부동태 계면 형성**을, **양극쪽(S₈)에서는 전해질→S₈ 전하이동 억제**를 동시에 만든다 — 라는 것이 주장이다.
성과는 대칭셀 **4000 h**(LPSC 225 h)·CCD **1.8 mA cm⁻²**·Li/S 풀셀 **932.6 mAh g⁻¹·150 cyc 83.7 %**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 저자 | **Chong Liu**, **Tianran Zhang\***, Ruoyu Wang, Butian Chen, **Dewen Wang**, Tenghui Wang, Ziyi Yang, Tao Liu, Qianjiang Mao, Taiguang Li, Jicheng Zhang, Xiaobai Ma, **Xiangfeng Liu\*** |
| 소속 | 中国科学院大学 **UCAS** 材料科学与光电工程中心 (전원) + 中国原子能科学研究院 CIAE 핵물리부(X. Ma, 중성자 회절) |
| 저널/년 | *Adv. Funct. Mater.* **2025**, 35, 2412144 (online 2024-10-10) |
| 조성 | `Li₆P₁₋ₓSbₓS₅₋₂.₅ₓO₂.₅ₓCl`, x = 0 / 0.02 / **0.05** / 0.08 / 0.1 / 0.15 / 0.2. **x=0.05 = "LPSC-SbO"** |
| 연구유형 | exp 주 + DFT 보조 |
| 셀 | Li‖SE‖Li 대칭 · Li‖SE‖Cu · Li‖SE‖S@CNTs 모델셀 · 무용매 파우치(Li-In 음극, ~50 MPa) |
| **★ 계보** | **[WangYO]**(`papers/wang2025_electronic_localization_yo_argyrodite.md`, Y₂O₃ 공도핑, *Angew* 2025)**와 같은 랩·같은 사람**이다 — 저기선 Dewen Wang/Chong Liu 가 공동1저자, 여기선 Chong Liu 가 1저자·Dewen Wang 이 공저, 교신은 둘 다 **Xiangfeng Liu**. ⇒ **`M₂O₃ 전구체로 M³⁺/⁵⁺ + O 를 한 번에 넣는다`는 이 랩의 연속 전략의 *앞칸*(Sb₂O₃ 2024 → Y₂O₃ 2025)**. 두 논문이 **자리 배정도 같다**: M@P_4b + O@S_16e |

**동기 (Scheme 1)**: ASSLSB 의 문제를 *한쪽* 이 아니라 **양쪽 계면 동시**로 잡겠다는 것.
(i) 음극쪽 — LPSC 는 Li 금속과 반응해 Li₂S/Li₃P/LiCl 의 **혼합 이온-전자 전도층**을 만들고, 이 층이 계속 자라
덴드라이트를 부른다. (ii) 양극쪽 — 복합양극 안에서 LPSC 가 **CNTs 와 접촉해 전하이동이 쉬워지고**(PS₄³⁻ 산화),
또 **S₈ 와 직접 반응**한다. 논문의 가설: 두 문제 다 *"PS₄ 사면체의 S 가 전자를 얼마나 쉽게 주고받는가"* 하나로
환원되고, 그 척도가 **S-p band center** 다.

---

## 3. 핵심 물성 (수치 총정리)
### 3.1 전해질 자체
| 물성 | LPSC (x=0) | LPSC-SbO (x=0.05) | 출처 |
|---|---|---|---|
| σ_ion (25 °C) | 2.6 × 10⁻³ S cm⁻¹ | **5.3 × 10⁻³ S cm⁻¹** | 본문 (LPSC 값은 대기노출 절에서 인쇄) |
| σ_e | n/a (미인쇄) | **2.06 × 10⁻⁹ S cm⁻¹** (계열 최저) | 본문 · DC 분극 |
| Ea (EIS Arrhenius) | **≈0.295 eV** | **≈0.250 eV** (계열 최소) | **`Fig. S1`c figure-read ≈** — 본문·SI 어디에도 숫자 없음 |
| 격자상수 a | 9.84627 Å | **9.85010 Å** (+0.039 %) | 본문 (Rietveld) |
| (113) d-spacing | 0.300 nm | 0.303 nm | `Fig. 1d,f` SAED |
| H₂S (35 % RH, 60 min) | **≈0.88 cm³ g⁻¹** (figure-read ≈) | 본문 "<0.2" / **figure-read ≈0.23** | `Fig. 1i` · "270 % 감소" |
| 대기노출 후 σ | 0.7 × 10⁻³ (−73 %; 본문은 "67.3 %") | 4.1 × 10⁻³ (−22 %) | 본문 · `Fig. S17,S18` |

> ⚠ **σ 계열 곡선(figure-read ≈, `Fig. S1`c)**: x = 0 / .02 / .05 / .08 / .1 / .15 / .2 →
> **2.6 / 4.0 / 5.3 / 3.6 / 3.2 / 2.4 / 1.8 mS cm⁻¹**, Ea → **0.295 / 0.265 / 0.250 / 0.272 / 0.282 / 0.313 / 0.330 eV**.
> **Arrhenius 창이 25–60 °C 5점(35 K)뿐** — Ea 절대값의 오차가 작지 않다.

### 3.2 Li 금속 계면 (음극축)
| 물성 | LPSC | LPSC-SbO |
|---|---|---|
| 대칭셀 수명 (0.1 mA cm⁻² / 0.1 mAh cm⁻²) | **225 h** 에서 단락 | **> 4000 h** |
| 초기 과전압 | 7.2 mV | **3.6 mV** |
| CCD (25 °C) | 0.6 mA cm⁻² | **1.8 mA cm⁻²** (≈3×) |
| Tafel 교환전류밀도 j₀ | 0.302 mA cm⁻² | **0.194 mA cm⁻²** (부식전류 낮음 = 계면반응 억제) |
| Li/Cu 핵생성 과전압 / ICE | 13.6 mV / 72.9 % | 9.9 mV / **79 %** (60 cyc 후 CE **99.1 %**) |
| 계면상 | Li₂S + Li₃P + LiCl (혼합 전도) | **Li₃Sb (PDF#04-0791) + Li₂S (PDF#26-1188) + LiSbS₂ (PDF#40-1331)** = "Li_xSb_yS_z" |
| 추가 안정성 | — | 0.5 mA cm⁻² 1500 h · 1 mA cm⁻² 500 h (`Fig. S23,S24`) |

### 3.3 S 양극 계면 + 풀셀
| 항목 | LPSC | LPSC-SbO |
|---|---|---|
| CV(복합양극) 산화/환원 전류 | 큼 | 작음 (`Fig. 4c`) |
| Tafel 기울기 (환원 / 산화) | 97.5 / 57.6 mV dec⁻¹ | **90.8 / 21.4 mV dec⁻¹** |
| 0.1 C 25 °C | 931.7 → 502.0 mAh g⁻¹ (50 cyc, **53.9 %**) | **932.6 mAh g⁻¹, 150 cyc 83.7 %** |
| rate (0.1/0.2/0.5/1 C) | 921.8 / 624.9 / 326.7 / 179.4 | **933.5 / 797.1 / 573.7 / 396.3** mAh g⁻¹ |
| 0.2 C 60 °C | 60 cyc 만에 급감 | **300 cyc 83 %** |
| 고로딩 1.8 mg cm⁻² | — | 0.1 C 100 cyc **79.7 %** |
| 파우치 (무용매, Li-In, ~50 MPa) | — | 초회 **773.4 mAh g⁻¹**, 20 cyc 안정, 굽힘/절단/천공 후 점등 |
| 에너지밀도 (S 기준, 평균 1.9 V) | — | **612.7 Wh kg⁻¹** (S 28 wt%, `Table S11`) |

### 3.4 계산값 (이 논문이 직접 계산한 것)
| 양 | 값 | 어디 |
|---|---|---|
| **ε_p (S-p band center), LPSC 의 PS₄-S** | **−2.06 eV** (vs E_F) | `Fig. 5b` **그림 안 라벨이 전부** — 본문에 숫자 없음 |
| **ε_p, LPSC-SbO 의 SbS₄-S** | **−2.57 eV** (vs E_F) → **Δ = −0.51 eV** | `Fig. 5b` |
| **CI-NEB: Li⁺ across LiSbS₂** | **0.23 eV** (정방향) · figure-read 역방향 ≈**0.37 eV** | `Fig. 3h` |
| E_ads(Li₂S / LPSC) | **−5.14 eV** | **`Fig. S36` 그림 안에만** — 본문·캡션 어디에도 없다 |
| E_ads(Li₂S / LPSC-SbO) | **−6.39 eV** | 〃 |
| Li₂S 0.22 eV · LiF 0.67 eV | **이 논문 계산 아님 — ref [30b] 소환값** | §6.4 |

---

## 4. 재료 & 방법 (실험)
- **합성**: Li₂S + P₂S₅ + LiCl + **Sb₂O₃** 화학량비 → 볼밀 500 rpm 10 h (ball:material 30:1) → ~350 MPa 성형 →
  석영관 진공봉입 → **550 °C 10 h**(승온 5 °C/min, 냉각 2 °C/min) → 유발 분쇄. 전 공정 Ar 글로브박스.
- **양극**: S:CNTs = 3:1 볼밀 → 155 °C 12 h melt-diffusion = S@CNTs (TGA S ≈75 wt%, `Fig. S35`).
  복합양극 = S@CNTs : CNTs : SE = **3:1:4** ⇒ 복합양극 내 S = 28 wt%.
- **셀**: SE 100 mg → 300 MPa (Ø10 mm, ~800 µm), Li foil 100 µm 양면, Cu 집전체 10 MPa. 양극 5 mg.
- **분석**: NPD(**CARR/CIAE HRND, λ=1.479875 Å**) + XRD Rietveld(FullProf), Raman 532 nm,
  XPS(ESCALAB 250Xi, Ar⁺ depth 0/120/240/360 s), **Sb K-edge XANES**, ⁷Li·³¹P MAS NMR(600 MHz, 8 kHz),
  TOF-SIMS(PHI nanoTOF II, 2 keV Cs⁺, 10 nm/min on SiO₂, 400×400 µm), ICP-OES, GEIS + **DRT(MATLAB GUI)**.

---

## 5. 결과 — 섹션별 상세

### 5.1 조성 스크리닝 · 구조 (Fig 1a,b; Fig S1–S7; Table S1–S8)
x=0.05 가 **불순물 없는 순수 argyrodite**를 유지하면서 σ 최대·σ_e 최소·Ea 최소. 격자상수는 x=0→0.1 에서
**선형 증가(Vegard)** — P⁵⁺(38 pm) → Sb⁵⁺(60 pm) 치환의 증거로 제시. NPD+XRD Rietveld 는
**Sb1 @ 4b (P 자리, occ 0.05)** · **O2 @ 16e (PS₄-S 자리, occ 0.075)** 로 정련(`Table S3`, `Table S7`).
TEM 은 3–5 µm 입자, SAED (113) 면간거리 0.300 → 0.303 nm 로 팽창.

> 🔴 **우리 판독 적발 3건 (이 절)**
> ① **화학식이 전구체와 안 맞는다.** 공칭식은 O/Sb = **2.5** 인데 O 원천이 Sb₂O₃ 하나뿐이면 O/Sb = **1.5** 다.
>    (그리고 DFT 모델은 2 Sb + 3 O = **1.5** 로 만든다 — 즉 계산 모델이 공칭식이 아니라 전구체 비를 따른다.)
> ② **`Table S8`(ICP) 이 본문 주장을 부정한다.** 본문 *"align well with the feed ratio"* ↔ 표 실물:
>    Li 15.4/15.5 ✅ · P 10.8/10.5 ✅ · Sb 2.2/2.3 ✅ · **S 58.1 / 검출 32.1 wt% (−45 %)** ❌.
>    (계산 wt% 는 우리가 재계산해도 맞다 → 틀린 쪽은 검출값 또는 인쇄.) **Cl·O 는 아예 미측정.**
> ③ **Rietveld ADP 가 물리적이지 않다.** `Table S1–S5` 의 S2/O2(16e) Uiso 가 **0.60 / 0.95 / 1.04 / 1.07 / 1.43 Å²**,
>    P1 도 0.606 — 정상값(0.02–0.05)의 20–50배. 자리 점유(특히 O 0.075)를 이 정련으로 확정했다는 주장은 약하다.
>    ✅ 단 **NPD**(`Table S7`, b_O 5.80 vs b_S 2.85 fm)는 O/S 대비가 좋아 O 자리 배정 자체는 살아 있다.

### 5.2 Sb·O 의 화학상태 (Fig 1g,h; Fig S10–S13)
- **Sb 3d XPS**: 이중선 2쌍 — **529.7/539.1 eV = Sb³⁺–S**, **530.6/540.0 eV = Sb⁵⁺–S** ⇒ **혼합가**.
  O 1s **531.9 eV = P–O** (Sb 3d 와 겹침), P 2p 에 **133.7 eV = P–O** 신규 ⇒ O 가 PS₄ 안으로 들어감.
- **Sb K-edge XANES**: 흡수단이 **Sb₂O₃ 와 Sb₂O₅ 사이** → 3+/5+ 혼합 확인 (XPS 와 정합).
- **S 2p (`Fig. S11`c)**: **Sb–S 162.8·161.7 eV** 신규, P–S 162.3·161.1 eV 잔존.
- **Raman**: **341.5 cm⁻¹ 신규 = SbS₄**. ⁷Li NMR 은 단일 공명(Li⁺ 환경 불변), ³¹P 는 약화(P 자리 치환).

> ⚠ **혼합가(Sb³⁺/Sb⁵⁺)는 DFT 모델에 반영되지 않는다.** DFT 는 P⁵⁺↔Sb⁵⁺ 등가치환 하나뿐이다.

### 5.3 대기 안정성 (Fig 1i; Fig S14–S18)
H₂S 발생이 **270 % 감소**. XRD: 노출 후 LPSC 에만 Li₂HPO₄·Li₄P₂S₆·Li₂S₂O₇ 등 불순물,
in-situ Raman 에서 LPSC 의 430.5 cm⁻¹ 세기 감소(P–S 분해) — LPSC-SbO 는 Sb–S·P–S 거의 불변.
기전은 **HSAB 정성 논변 하나** (soft base S²⁻ → hard base O²⁻ 로 바꾸면 hard acid H⁺/H₂O 와 덜 반응).

### 5.4 Li 금속 계면 (Fig 2, Fig 3a–f)
- `Fig. 2a`: LPSC 225 h 에서 임피던스가 **0 Ω 쪽으로 급락**(내부 단락) ↔ LPSC-SbO 4000 h 안정.
- `Fig. 2e,f` **operando GEIS + DRT**: LPSC 는 용량 0.6 mAh cm⁻² 에서 **SEI 피크(τ≈10⁻⁴ s)가 사라지고**
  총 임피던스가 급락 = 덴드라이트 관통. LPSC-SbO 는 2 mAh cm⁻² 까지 SEI 피크 유지.
- `Fig. 3a` XRD: 사이클 후 Li 표면에 **Li₃Sb + Li₂S + LiSbS₂**. 단주기에서는 LiSbS₂ 만 표면(`Fig. S28`).
- `Fig. 3c,d` **XPS depth (0→360 s)**: 깊이 들어갈수록 **Li₃Sb 증가 · Sb⁵⁺ 종 감소** = Sb⁵⁺ 가 Li 에 환원됨.
  S 2p 에서 **Li₂S 성분이 깊이에 따라 증가**.
- `Fig. 3e,f` TOF-SIMS: LiS⁻·Sb⁻·LiSbS₂⁻ 가 800 s 스퍼터 내내 **평탄** = 균질한 층 (`Fig. S31` 의 LPSC 대조군은
  PS₃⁻·LiS⁻ 만).
- ⇒ 모형(`Fig. 3b`): 초기 LiSbS₂ 층 → 동적 진화 → **Li₃Sb + Li₂S 하부 + LiSbS₂ 상부**.

### 5.5 S₈ 양극 계면 (Fig 4)
- `Fig. 4c` 반차단셀 CV(0–5 V, 0.1 mV/s): LPSC-SbO 의 산화·환원 전류가 전 구간 작다.
  피크 배정 — 환원 P⁵⁺→P³⁻(≈0.2 V)·S⁰→S²⁻, 산화 P³⁻→P⁰(≈0.6–1.0 V)·**S²⁻→S⁰ (figure-read ≈2.7 V)**·
  P⁰→P⁵⁺(figure-read ≈3.9 V). ⚠ 이건 **한 번 환원된 종의 재산화**라 *pristine SE 의 산화 개시*가 아니다.
- `Fig. 4f,g` ex-situ Raman: LPSC 쪽은 방전 종료(1.4 V)에도 **S₈ 신호가 남고**(불완전 전환), 충전 3.0 V 에서
  **P₂S₅ 신규 286 cm⁻¹**, PS₄³⁻(414 cm⁻¹) 지속 약화. LPSC-SbO 는 PS₄³⁻ 유지·P₂S₅ 없음.
- `Fig. 4h` XPS(충전 후): LPSC 만 **thiosulfate 165.1/166.2 eV (P–Sₓ–P)** + **sulfate 166.6/168.1 eV**.
- `Fig. 4d,e` **전하밀도차**: LPSC–S₈ 는 S₈ 위에 큰 등가면(전자 이동 있음), LPSC-SbO–S₈ 는 거의 없음.

### 5.6 기전 (Fig 5) — **이 논문의 논지 사슬**
1. Sb 가 P 자리에 들어가 **SbS₄ 사면체**가 생긴다 (Raman 341.5 · XPS Sb–S · Rietveld 4b).
2. SbS₄ 의 **S-p 밴드중심이 PS₄ 대비 −0.51 eV 내려간다** (`Fig. 5b`, ε_p −2.06 → −2.57).
3. **음극쪽**: 같은 하강으로 **S-p 의 전도대(빈 상태)가 E_F 쪽으로 내려온다** →
   친핵성 Li 금속에서 전자를 **더 쉽게 받는다** → SbS₄ 가 **우선 반응**해 Li_xSb_yS_z 로 빠르게 바뀌고
   그 층이 **전자를 안 통하는 부동태**라 반응이 멈춘다 (`Fig. 5c` 위·`Fig. 5a` Li-s 가 E_F 에서 멀어짐).
4. **양극쪽**: 같은 하강으로 **점유 S-p(가전자대)는 E_F 에서 멀어진다** →
   S 주위에 전자가 더 몰려 **이웃 Li 과의 상호작용이 강해지고** → 그 Li 이 **S₈ 로 전자를 못 넘긴다**
   (`Fig. 4d,e` 전하밀도차) → 계면 부반응 억제. 동시에 **S 자체를 뽑아내기 어려워 자기산화도 억제**.
5. ⇒ **하나의 서술자(ε_p)로 양쪽 계면을 동시에 설명**한다는 것이 논문의 셀링포인트.

> 🔎 **논리 점검** — 3 과 4 는 모순이 아니다. 밴드 전체가 내려가면 (VBM 하강 = 산화 어려움) + (CBM 하강 =
> 환원 쉬움) 이 동시에 성립한다. 다만 `Fig. 5b` 실물은 **강체 이동(rigid shift)이 아니라 갭 축소**다
> (figure-read ≈ LPSC S-p 갭 3.2 eV → LPSC-SbO 1.7 eV): 내려온 전도대는 host 의 것이 아니라 **Sb 유래 빈 상태**다.
> 즉 정확한 문장은 *"p-band 가 통째로 내려갔다"* 가 아니라 **"Sb 가 갭 안쪽에 낮은 빈 밴드를 넣었다"** 다.
> 이건 논문 서사를 무너뜨리진 않지만 **σ_e 실측 2.06×10⁻⁹ S/cm(계열 최저)와 긴장 관계**다 (§10-③).

---

## 6. DFT / 계산 방법 ★ (SI "Theoretical calculations methods" 전문 기준)

### 6.1 공통 (VASP)
| 항목 | 값 | 비고 |
|---|---|---|
| code | **VASP** (버전 **명시 없음**) | |
| functional | **PBE-GGA** · **vdW 보정 명시 없음** | |
| pseudo | **PAW** | 원소별 POTCAR 종류 명시 없음 |
| ecut | **400 eV** | ⚠ VASP 표준 O PAW 의 ENMAX 가 정확히 400 eV — 셀 이완/응력에는 권고 1.3×ENMAX 미달 |
| smearing | **Gaussian, σ = 0.2 eV** | 절연체에 0.2 eV 는 큰 편(밴드엣지가 뭉갠다) |
| k-points | **Monkhorst-Pack 3×3×3**, *"격자상수 최적화용"* | **슬랩·NEB·PDOS 용 k-mesh 는 명시 없음**. 진공 15 Å 방향에 3점을 그대로 쓰면 안 된다 |
| 진공 / dipole | **z 축 진공 15 Å + dipole correction** | 어느 모델에 적용했는지 구분 없음(벌크 2×2×1 에도?) |
| 수렴 | 전자 **1×10⁻⁵ eV** · 힘 **< 0.02 eV/Å** | |
| 스핀 | **명시 없음** | |
| DFT+U | **없음** (Sb 5p/5s 는 U 대상 아님 — 타당) | |

### 6.2 PDOS / p-band center 모델 ★ (1저자 요청 ②)
- **셀**: Li₆PS₅Cl 의 **2×2×1 슈퍼셀** (관용 입방셀 a≈9.85 Å 기준 ⇒ ≈19.7×19.7×9.85 Å, **208 원자** Li₉₆P₁₆S₈₀Cl₁₆).
- **치환**: **P 2개 → Sb 2개**, **S 3개 → O 3개**. ⇒ 모델 조성 ≈ `Li₆P₀.₈₇₅Sb₀.₁₂₅S₄.₈₁O₀.₁₉Cl`.
  - ⚠ **실험 조성(x=0.05)이 아니다** — 모델은 **x=0.125 = 2.5배 과도핑**.
  - ⚠ **O/Sb = 1.5** (공칭식 2.5 아님, Sb₂O₃ 비와 일치).
  - ⚠ **O 를 어느 S 자리에 넣었는지 명시 없음**(16e/4a/4d). 실험 Rietveld 는 16e.
- **무질서 처리**: ⛔ **한 줄도 없다.** Li 48h **점유 0.5** 를 어떻게 정했는지, S/Cl 의 4a·4d **혼합 점유
  (0.385/0.615)** 를 어떻게 결정했는지, 배열을 몇 개 봤는지 — **SQS·enumerate·앙상블 언급 0**.
  사실상 **단일 배열**로 봐야 한다. (우리 관례에선 이게 ±0.2–0.3 eV 를 흔드는 축이다.)
- **p-band center 정의** ★:
  | 물어야 할 것 | 이 논문 |
  |---|---|
  | 정의식 (∫ E·ρ dE / ∫ ρ dE) | **없음** — 식을 안 쓴다 |
  | **참조 준위** | **E_F** (그림 축이 `E − E_f`, ε_p 를 E_F 로부터의 거리로 표시) |
  | **적분 창** | **명시 없음.** `Fig. 5b` 위치상 **점유대(가전자대)만** 쓴 것으로 보이나 하한이 −10 eV 인지 −8 인지 알 수 없다 |
  | **스핀 처리** | **명시 없음** |
  | 어느 원자? | **사면체별 S** (LPSC=PS₄ 의 S, LPSC-SbO=SbS₄ 의 S) — **자리분해(free-S vs PS₄-S)는 하지 않는다** |
  | 값 | LPSC **−2.06** / LPSC-SbO **−2.57** eV — **본문에 없고 `Fig. 5b` 그림 라벨이 유일한 출처** |

> 🔴 **참조 준위 문제 (§10-② 로 이어짐)**: 절연체에서 E_F 는 갭 안 어디든 놓일 수 있어 **유일하지 않다**.
> `Fig. 5b` figure-read ≈ 로 재면 **LPSC 의 S-p 점유대 상단이 E_F 보다 0.7 eV 아래**, LPSC-SbO 는 **1.0 eV 아래**다
> (±0.2). 즉 두 계의 E_F–VBM 간격이 다르다. **VBM 기준으로 다시 재면 하강폭은 0.51 이 아니라 ≈0.2 eV** 로 줄어든다.
> ⇒ **주장한 하강의 절반 이상이 E_F 배치 차이일 수 있다.** 이건 이 논문이 답을 안 준 축이다.

### 6.3 계면 모델
| 모델 | 무엇 | 알려진 것 / 모르는 것 |
|---|---|---|
| **Li / LPSC-SbO** | `Fig. 3g`·`Fig. S32` — 최적화 전/후 + AIMD 전/후 | 원자수·슬랩 두께·표면 종단·초격자 정합 변형률 **전부 명시 없음** |
| **S₈ / LPSC**, **S₈ / LPSC-SbO** | `Fig. 4d,e` 전하밀도차 | **isovalue 명시 없음** · 정량(Bader·ΔQ) **없음** · 두 패널의 접촉 기하가 눈으로도 다르다(통제 안 됨) |
| **Li₂S / LPSC**, **Li₂S / LPSC-SbO** | `Fig. S36` | **E_ads −5.14 vs −6.39 eV 가 그림 안에만 있다** — 본문·캡션 미인용. 두 슬랩의 크기·종단이 그림상 다르다 |
| **AIMD** | **CP2K** (VASP 아님) · PBE · **GTH pseudo + DZVP-MOLOPT-SR-GTH** · **Γ-only** · 1.5 ps 승온 → **300 K NVT** · dt **1 fs** · 총 **10 ps** | ⚠ SI 원문 *"a time step of 10 ps, an interval of 1 fs"* 는 뒤바뀐 표현. thermostat 종류·시드 수 **명시 없음**. **단일 궤적** |

### 6.4 ★★ NEB / Li 이동장벽 — 전수 표 (1저자 요청 ①)
| # | 계 | 값 | **출처** | 경로 (어디→어디) | 셀 / 슈퍼셀 | 이미지 수 | CI | 전하 규약 | code/범함수/컷오프 | 수렴 임계 |
|---|---|---|---|---|---|---|---|---|---|---|
| **N1** | **LiSbS₂ 계면상** | **0.23 eV** (정방향)<br>figure-read 역방향 ≈**0.37 eV** | **이 논문 자체 계산** (`Fig. 3h`) | *"Li⁺ across the LiSbS₂"* — **슬랩을 가로지르는 관통 경로**. 반응좌표 0→**≈9.6 Å**, 삽화상 Li 이 슬랩 **윗면 → 아랫면** 으로 이동. **어느 자리→어느 자리인지 논문에 없음** | **명시 없음** (진공 15 Å + dipole = 슬랩으로 추정) | **명시 없음** — `Fig. 3h` 의 초록 마커 **figure-read ≈ 7개**(끝점 포함) | 본문 "climbing image NEB", SI "climbing-image under elastic band" ⇒ **CI 사용이라 서술**, 설정 세부 없음 | **명시 없음.** 여분 Li 을 넣었는지 공공을 만들었는지, `NELECT`/배경전하를 건드렸는지 **한 줄도 없다** ⇒ 기본값이면 **중성 셀** | VASP / PBE-PAW / **400 eV** (공통 사양 상속으로 추정, NEB 전용 사양 미기재) | 공통값 상속 추정: 1e−5 eV / 0.02 eV/Å. **NEB 힘 임계 별도 명시 없음** |
| **N2** | **Li₂S 층** | **0.22 eV** | ⛔ **이 논문 계산 아님 — 소환값**<br>ref **[30b] = C. Lai, C. Shu, W. Li, L. Wang, X. Wang, T. Zhang, X. Yin, I. Ahmad, M. Li, X. Tian, P. Yang, W. Tang, N. Miao, G. W. Zheng, *Nano Lett.* 2020, 20, 8273** | **이 PDF 안에 정보 0** | — | — | — | — | — | — |
| **N3** | **LiF 층** | **0.67 eV** | ⛔ **소환값, 같은 ref [30b]** | 〃 | — | — | — | — | — | — |

**원문 그대로 (p.8, 좌단):**
> *"Figure 3h shows that the calculated Li⁺ migration energy barrier through the LiSbS₂ interphase is only **0.23 eV**.
> This value is comparable to the reported energy barrier for Li⁺ migration through the **Li₂S layer (0.22 eV)** and
> significantly lower than that through a **LiF layer (0.67 eV)**.[30b]"*

**⇒ 판정: 0.22 eV 는 이 논문이 Li₂S 를 계산한 값이 아니다.** 이 논문이 계산한 유일한 장벽은
**LiSbS₂ 의 0.23 eV** 이고, 0.22(Li₂S)·0.67(LiF) 은 **Lai et al. Nano Lett. 2020 에서 끌어온 2차 인용**이다.
1저자가 "Li₂S 장벽 0.22 eV" 로 읽은 것은 **문장 자체는 맞지만 귀속이 틀렸다** — 이 논문에는
Li₂S NEB 가 없고, 그림 h 의 0.23 은 **LiSbS₂** 다. 두 값이 가까운 것은 저자들이 *"우리 계면상이 Li₂S 만큼
잘 통한다"* 를 말하려고 나란히 놓았기 때문이지, 같은 계산에서 나온 쌍이 아니다.

**추가 (`Fig. 3h` figure-read)**: 끝점이 **대칭 등가가 아니다** — 최종상태가 초기보다 **≈0.14 eV 낮다**.
그래서 SI 의 정의 `E_m = E_h − E_i` 는 **방향 의존 장벽**이고, 반대 방향으로 가면 ≈0.37 eV 다.
논문은 이 비대칭을 언급하지 않는다.

---

## 7. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| Scheme 1 | LPSC vs LPSC-SbO 의 양쪽 계면 문제/해결 개념도 | "dual interface" 프레이밍. 우리 축 B(양극)·E(음극) 를 한 그림에 얹는 방식 |
| 1a,b | LPSC-SbO Nyquist(25–60 °C) + **NPD Rietveld**(SbS₄/PS₄ 삽화) | NPD 로 O@S 를 잡는 법(b_O/b_S 대비). 우리 LPSOCl 의 **O@PS₄-S** 배정과 같은 자리 |
| 1c–f | TEM + SAED, (113) d 0.300→0.303 nm | 도핑 격자팽창의 국소 증거 (XRD 보완) |
| 1g,h | Sb 3d XPS(Sb³⁺/Sb⁵⁺ 이중선) + **Sb K-edge XANES** | **혼합가 판정의 2중 증거 포맷.** 우리 도펀트(Nd·Y·B) 산화수 주장에 그대로 이식 가능 |
| 1i | H₂S 발생량 (35 % RH, 60 min) | 대기 축의 표준 관측량. **본문 "<0.2" ↔ figure-read ≈0.23 불일치** |
| 2a–d | 대칭셀 4000 h · 계단 CCD(0.6 vs 1.8) · 문헌 CCD 비교 | CCD 는 **셀 형상·압력 의존**이라 절대값 비교 금지 ([Deng26PS]·[Taklu21] 행과 같은 주의) |
| 2e,f | **operando GEIS + DRT** (SEI 피크 τ≈10⁻⁴ s 소멸) | 계면 열화를 *시간분해*로 보는 법. 우리에게 없는 실험축 |
| 2g | Tafel j₀ 0.302 → 0.194 mA cm⁻² | "부식전류" 로 계면 반응성을 정량화하는 관측량 |
| 3a–f | 사이클 후 XRD / XPS depth / TOF-SIMS 3D — Li₃Sb·Li₂S·LiSbS₂ | **계면상 동정의 3중 교차검증 포맷**(회절+깊이 XPS+SIMS). 우리 `interface_reactivity` 예측의 검증 템플릿 |
| **3g** | **AIMD 10 ps 전/후 Li/LPSC-SbO 계면 재구성** (Li–Sb–S 형성) | 우리 UMA-MD 계면 재구성과 같은 그림. **단 10 ps·단일궤적** = 통계 없음 |
| **3h** | **CI-NEB — Li⁺ across LiSbS₂, 0.23 eV** | ★ §6.4 · §11. **끝점 비대칭(figure-read ≈−0.14 eV)** 과 **관통경로(≈9.6 Å)** 를 반드시 같이 인용 |
| 4a,b | 계면반응 I(CNTs)·II(S₈) 개념도 | PS₄ 분해 vs SbS₄ 무분해 만화 — **x=0.05 면 사면체 95 % 가 여전히 PS₄** 라는 [LiInF] 지적이 여기도 걸린다 |
| 4c | 반차단셀 CV 0–5 V, 피크 배정 | **S²⁻→S⁰ 가 P⁰→P⁵⁺ 보다 먼저** (figure-read ≈2.7 vs ≈3.9 V) = 우리 축 B① "S-limited" 순서의 실험 지지. ⚠ 재산화 피크라 onset 아님 |
| **4d,e** | **S₈/LPSC vs S₈/LPSC-SbO 전하밀도차** | 우리 CDD 그림과 같은 양. **isovalue·Bader 없음** ⇒ 정성까지만 |
| 4f–h | ex-situ Raman(전압별) + 충전후 XPS(thiosulfate/sulfate) | 산화 *산물* 앵커: **P₂S₅ 286 cm⁻¹**, thiosulfate 165.1/166.2, sulfate 166.6/168.1 eV |
| **5a** | Li-s PDOS (LPSC vs LPSC-SbO) | 🔴 **LPSC 패널이 갭이 없다**(E_F 에 뾰족한 피크) — LPSCl 이 wide-gap 절연체라는 사실과 충돌 (§10-②) |
| **5b** | **S-p PDOS + ε_p = −2.06 → −2.57 eV** | ★★ **우리 site-PDOS ⟨3p⟩ 축의 문헌 짝**. 창·참조준위가 달라 **수치 이식 금지** (§11-B) |
| 5c | 기전 모식도 (양쪽 계면 + ε_p 하강) | 논지 사슬 한 장 요약. 발표용으로 유용 |
| 6a–g | 풀셀 사이클/rate/60 °C/파우치/문헌비교 | 성능 맥락. 로딩 1.07 mg cm⁻² 는 낮다 |
| S1 | σ·Ea vs x (7 조성) | **figure-read Ea 0.295→0.250 eV**. Arrhenius 창 25–60 °C 5점뿐 |
| S32 | Li/LPSC-SbO 계면 최적화 3단계 (I 벌크 → II 미이완 계면 → III 이완 계면) | 계면 이완만으로 Li–Sb–S 결합이 생김 = **정적 계산에서도 반응 활성** |
| **S36** | **Li₂S/LPSC vs Li₂S/LPSC-SbO 구조 + E_ads −5.14 / −6.39 eV** | ★ **그림 안에만 있는 수치**. −5~−6 eV 는 흡착이 아니라 **반응 에너지 영역**이고 두 슬랩이 통제되지 않았다 |

**내가 실제로 본 그림 / 안 본 그림 (정직 목록)**
- 🔍 **고해상 실물 판독**: `Fig. 1`(전체) · `Fig. 3`(전체 + **3h 확대**) · `Fig. 4`(전체 + **4c 확대**) ·
  `Fig. 5`(전체 + **5a·5b 확대**) · SI `Fig. S1` · `Fig. S32` · `Fig. S36` (+ 우연히 `S31`·`S35`).
- 👁 **페이지 렌더로만 훑음(확대 안 함)**: `Scheme 1` · `Fig. 2` · `Fig. 6`.
  두 그림의 수치(4000 h·CCD 1.8·932.6 mAh g⁻¹ 등)는 **본문 인쇄값**이라 그림 판독이 필요 없다.
- ⛔ **안 본 것**: SI `Fig. S2–S30`, `S33–S34`, `S37–S47` (총 40장). 전기화학 반복·SEM·임피던스라
  우리 축에 새 정보가 없다고 판단했다.
- **본문 서술과 어긋난 그림 4건** → §10-①②④⑤.

## 8. Post-processing ★
- **무엇을 했나**: PDOS(원자·궤도 분해) → **p-band center** · **CI-NEB**(1건) · **전하밀도차(CDD)** ·
  **흡착에너지 E_ads**(`Fig. S36`) · **AIMD 궤적의 전/후 구조 비교**(정성).
- **도구**: 논문에 **후처리 도구 언급 0** (VASPKIT/pymatgen/LOBSTER/VESTA 등 전부 미기재).
  구조 그림 렌더러도 미기재(VESTA 계열로 보임).
- **수치화·기록 방식**: ε_p 는 **그림 안 라벨**, E_ads 도 **그림 안 텍스트**. 표로 정리된 계산값 **0개**.
  원자좌표·입력파일 **미공개**("available from the corresponding author upon reasonable request").
- **(D) 이 논문이 하지 않은 것** — 우리 축에서 비는 칸:
  **Bader · COHP/ICOHP · COBI · ELF · BVSE · grand-potential ESW · 탄성상수 · 포논 · MLIP · 확산계수/MSD ·
  형성에너지/hull · 결함 형성에너지 · 밴드갭 수치**. 전부 없다.

---

## 9. 전체 논증 흐름 (한 줄씩)
1. Sb₂O₃ 로 x 를 훑어 x=0.05 가 최적(σ↑·σ_e↓·Ea↓·순수상) → 2. NPD/XRD/XPS/XANES/Raman/NMR 로
**Sb@P_4b + O@S_16e + SbS₄ 사면체 생성** 확정 → 3. 대기 축(H₂S −270 %)은 HSAB 로 설명 →
4. 음극축: 대칭셀 4000 h·CCD 1.8·j₀ 하락 → 5. 계면상을 XRD+XPS depth+SIMS 로 **Li₃Sb/Li₂S/LiSbS₂** 로 동정 →
6. AIMD 10 ps 로 그 층의 **생성 경로**를, CI-NEB 로 그 층의 **Li 통과 비용(0.23 eV)** 을 보임 →
7. 양극축: CV/Raman/XPS 로 LPSC 만 분해(P₂S₅·thiosulfate·sulfate), CDD 로 전하이동 차이 →
8. **PDOS 로 두 축을 하나로 묶음**: ε_p −0.51 eV 하강 ⇒ (CB↓ = 음극에서 빠른 부동태) + (VB↓ = 양극에서 산화 억제) →
9. 풀셀·파우치로 마무리.

**약한 고리**: 8 번이 전부 **단일 배열 · 과도핑(x=0.125) · 참조준위 미정의 · 창 미기재**의 PDOS 하나에 걸려 있고,
6 번의 NEB 는 **끝점 비대칭·전하규약 미기재**다. 실험 쪽(2·5·7)은 튼튼하다.

---

## 10. 주의 / 한계 (over-claim 방지) — **비판**
① 🔴 **`Fig. 1i` 본문–그림 불일치**: 본문 *"minimal amount of H₂S (< 0.2 cm³ g⁻¹) after 60 min"* ↔
  그림 60 min 종점 **figure-read ≈0.23**. 작지만 "<0.2" 로 인용하면 안 된다.
② 🔴🔴 **`Fig. 5a` 의 LPSC 패널에 갭이 없다.** Li-s PDOS 가 −5 eV 부터 +8 eV 까지 끊기지 않고 **E_F 에 뾰족한
  피크**가 서 있다. LPSCl 은 wide-gap 절연체다(우리 PBE fixed-occ: comp1 **2.066** / modelc **2.099** eV).
  즉 그들의 **기준계 자체가 결함준위/금속성 인공물을 갖고 있을 가능성**이 크고, 그러면 **E_F 가 그 준위에 pin 되어
  ε_p 의 참조점이 오염된다**. 같은 그림 LPSC-SbO 패널은 정상적으로 갭이 있다 ⇒ **두 계의 E_F 성격이 다르다.**
  ⇒ **ε_p 하강 0.51 eV 를 그대로 인용 금지.** VBM 기준으로 다시 재면 figure-read ≈**0.2 eV** 로 줄어든다(§6.2).
③ ⚠ **DFT 는 갭이 1.5 eV 줄었다는데(figure-read) 실측 σ_e 는 계열 최저(2.06×10⁻⁹ S/cm)** 다.
  둘 다 맞으려면 그 새 빈 밴드가 **국재(localized)** 여야 하는데 논문은 국재성을 재지 않았다(ELF·Bader·유효질량 0).
  [WangYO] 가 같은 랩에서 *"electronic localization"* 을 제목으로 걸었던 것과 대비된다.
④ 🔴 **`Table S8` ICP 가 본문 주장을 부정한다** (S 58.1 → 검출 32.1 wt%). §5.1-②.
⑤ 🔴 **`Fig. S36` 의 E_ads(−5.14 / −6.39 eV)** 가 본문에서 **한 번도 인용되지 않는다.** 그리고 그 크기는
  **흡착이 아니라 화학반응 영역**이다 — *"Li₂S 와 호환된다"* 의 근거로 쓰기엔 **더 강하게 붙는다**(−6.39 < −5.14)는
  결과가 오히려 반응성을 시사할 수 있다. 두 패널의 슬랩 크기·종단이 눈으로도 다르다 ⇒ **통제된 비교가 아니다**.
⑥ ⚠ **σ 가 2배 오른 이유가 논문에 없다.** Li 함량 불변·공공 생성 없음·격자팽창 +0.039 % 뿐인데 2.6→5.3 mS/cm.
  ("vacancy" 라는 단어가 본문에 **0회**.) x=0.05 에서만 뾰족한 최적점이 나오는 이유도 미설명.
⑦ ⚠ **DFT 모델 조성이 실험과 다르다** (x=0.125 vs 0.05 = 2.5배 과도핑, O/Sb 1.5 vs 공칭 2.5).
⑧ ⚠ **무질서 처리 전무** (Li 48h 0.5 · S/Cl 4a·4d 혼합점유 · 배열 개수 · SQS/enumerate 언급 0).
⑨ ⚠ **NEB 사양 대부분 미기재** — 이미지 수·셀·전하규약·NEB 힘 임계·스프링상수. §6.4.
⑩ ⚠ **CCD·대칭셀 수명은 셀 형상(펠릿 800 µm)·압력(10 MPa) 의존** — 타 논문 값과 절대 비교 금지.
⑪ ⚠ **로딩 1.07 mg cm⁻²** (고로딩 실험도 1.8). 실용 셀(>3 mAh cm⁻²)과는 거리가 있다.
⑫ ⚠ **Sb 혼합가(3+/5+)가 DFT 에 없다** — 계산은 Sb⁵⁺ 등가치환 하나.
⑬ ⚠ **AIMD 10 ps·단일 궤적·300 K** — 계면 반응의 *발생*은 보여도 *속도·통계*는 못 준다. thermostat 미기재.
⑭ ⚠ 본문 산술 오류: 2.6 → 0.7 mS/cm 는 **−73 %** 인데 "67.3 % reduction" 으로 인쇄.

---

## 11. 우리 DFT 대비 → `../our_dft_baseline.md`

### 11-A. ★★ NEB 축 — **값 비교가 아니라 방법 비교** (1저자 요청 ③)
> **우리 값의 지위를 먼저 못박는다** (`db/properties/sei_neb.json :: results["v2/li2s"]`):
> `citable: false` · **`absolute_citable: false`** · **`cell_convergence_status: untested`** ·
> **`scientific_status: provisional_single_cell`**.
> **허용된 문장은 이것 하나다**:
> *"For the Li2S antifluorite 3x3x3 model, the charged-vacancy (V_Li-, jellium) nearest-neighbour c->c
> CI-NEB barrier is 0.305 eV under this finite-cell protocol."*
> ⛔ **금지**: 이 값을 Li₂S 의 수렴된 고유 물성으로 인용하거나 **실험·문헌 값과 나란히 놓는 것**.
> ⇒ 그래서 **아래 표에는 값 열이 없다.** 두 계산이 "무엇을 재고 있는가" 만 비교한다.

| 방법 축 | 이 논문 (N1, LiSbS₂) | 우리 (`v2/li2s`) | 이게 왜 값을 못 나란히 놓게 만드나 |
|---|---|---|---|
| **대상 상** | **LiSbS₂** (이 논문의 계면상) | **Li₂S** (반형석) | **애초에 다른 물질이다.** 이 논문은 Li₂S NEB 를 하지 않았다(§6.4) |
| **차원 / 경계조건** | **슬랩 + 진공 15 Å + dipole 보정**(추정) | **3D 주기 벌크** 3×3×3 (λ₁ = 12.1 Å) | 슬랩 표면 경로 vs 벌크 홉 — 정전 환경·이완 자유도가 다르다 |
| **경로 정의** | **막을 가로지르는 관통** (반응좌표 ≈9.6 Å, 슬랩 윗면→아랫면) | **최근접 c→c 단일 홉** (d = **2.8526 Å**) | 관통 장벽은 여러 홉의 **직렬 합성**일 수 있다. 단일 홉 Ea 와 같은 양이 아니다 |
| **운반체 정의** | Li 를 **추가**한 것으로 보임(공공 언급 0, "vacancy" 본문 0회) | **공공 매개** (V_Li⁻) | 간극형 vs 공공형은 **다른 기전** |
| **전하 규약** ★ | **명시 없음** ⇒ 기본값이면 **중성 셀** | **하전 공공 q = −1 + jellium 배경** (tot_charge −1) | 하전 결함은 유한셀 정전 보정이 붙고 중성 셀은 안 붙는다. **같은 축에서 잰 값이 아니다** |
| **끝점 대칭성** | ❌ **비대칭** (figure-read ΔE ≈ −0.14 eV) ⇒ 방향 의존 | ✅ **대칭 등가** (E_f = E_b = 0.305, 비대칭 1e−5 eV) | 그들 값은 "정방향 장벽", 우리 값은 "가역 홉 장벽" |
| **CI 여부** | CI 라 서술 (설정 미기재) | CI (`CI_scheme: auto`) | 같음 |
| **이미지 수** | **명시 없음** (figure-read ≈**7 마커**) | **7 images** | 우연히 같아 보이지만 **그들 값은 그림에서 센 것**이라 확정 불가 |
| **code / 범함수 / 컷오프** | VASP · PBE-PAW · **400 eV** | **QE `neb.x`** · PBE · **ecutwfc 60 / ecutrho 480 Ry** | 코드·기저·의사퍼텐셜 전부 다름 |
| **수렴 임계** | 1e−5 eV / 0.02 eV/Å (NEB 전용 미기재) | (프로토콜 해시 `c24cf37e7a0e`) | |
| **셀 수렴 시험** | **없음**(셀 크기조차 미기재) | **없음** (`cell_convergence_status: untested`) | **양쪽 다 미시험** — 그래서 어느 쪽도 상대를 검증할 수 없다 |

**⇒ 판정: 이 논문은 우리 0.305 eV 에 대해 반증도 지지도 되지 않는다.**
이유 3단: (i) 이 논문에는 **Li₂S NEB 자체가 없다**(0.22 는 Lai 2020 소환값). (ii) 이 논문이 실제로 계산한 것은
**다른 상(LiSbS₂)·다른 차원(슬랩)·다른 경로(관통)·다른 운반체·다른 전하규약**이다. (iii) 소환된 0.22 조차
방법이 이 PDF 안에 없어 **우리 규약과 대조할 수 없다**.

**비교가 성립하려면 무엇을 맞춰야 하나 (우리 쪽 할 일)**
- (a) **우리 쪽 두 번째 셀** (4×4×4 또는 2×2×2) 로 `v2/li2s` 셀 수렴을 시험 → `cell_convergence_status` 해제.
  이게 우리 값의 지위를 올리는 **유일한 경로**이고, 문헌 비교의 전제조건이다.
- (b) 중성 공공 + 대칭 홉으로 **같은 셀에서 한 번 더** 재서 jellium 보정의 크기를 우리 손으로 재기
  (전하규약이 얼마짜리 축인지 우리 계에서 확정).
- (c) 문헌과 붙이고 싶으면 **Lai 2020 Nano Lett. 20, 8273 원문**을 litdb 로 끌어와 그쪽 규약을 읽어야 한다.
  ⇒ **inbox 후보로 등록** (이 digest 만으로는 0.22 의 방법을 알 수 없다).

### 11-B. ★★ p-band center 축 — **우리 free-S ⟨3p⟩ 서사의 문헌 짝** (개념 일치 / 수치 이식 금지)
| 항목 | 이 논문 | 우리 (`db/properties/site_pdos_mean3p_summary.csv`) | 판정 |
|---|---|---|---|
| 서술자 | S-p band center ε_p | site-resolved p-PDOS **⟨3p⟩ centroid** | **같은 물리량** |
| 참조 준위 | **E_F** | **VBM** (E−VBM 정렬) | ❌ **다르다** — 절연체 E_F 는 유일하지 않다 |
| 적분 창 | **명시 없음** | **−8..0 eV 고정** (그림 표시 창과 동일, CLAUDE.md 규율) | ❌ 다르다 |
| 분해 단위 | **사면체별**(PS₄-S vs SbS₄-S) | **자리별**(free-S / PS₄-S / Cl / B–S / O) | **우리가 더 잘게 본다** — free-S 를 이 논문은 아예 안 본다 |
| 값 | PS₄-S **−2.06** → SbS₄-S **−2.57** | free-S **−1.14**(+B₂O₃계) / **−0.90**(modelc) · PS₄-S **−2.23 / −2.25** · Cl **−2.99/−2.83** · B–S **−2.15** · O **−3.64** | ⚠ **PS₄-S 가 −2.06 vs −2.23 로 가까워 보이지만 우연일 수 있다** — 참조준위가 다르고, 그들 E_F 가 VBM 위 ≈0.7 eV(figure-read)면 VBM 기준 ≈−1.36 이 되어 **안 맞는다** |
| 결론 방향 | "깊을수록 산화 안정 + 이웃 Li 과 결합 강화" | "free-S 가 제일 얕다 = 먼저 산화된다 / 도핑이 만든 B–S·O 는 더 깊다 = 안정" | ✅ **방향 완전 일치** |

**⇒ 우리 위치**: 이 논문은 우리 서사의 **문헌 짝 3번째**다 —
**[BZOx]**(계면 S 상태 E_F 직하 → −1..−2 eV 하강, *계면판*) · **[Banik]/[Ong13]**(VBM=S 3p 가 onset 을 pin, *조성판*) ·
**본편**(사면체 치환으로 S-p 를 내린다, *벌크 도핑판*). **우리만 자리분해(free-S vs PS₄-S)+고정창을 갖고 있다.**
⇒ **기여 여지 확정**: "ε_p 를 내린다" 는 문헌 서사에 대해 **"어느 S 의 ε_p 를 내려야 하는가"** 를 답할 수 있는 것은
현재 우리 데이터뿐이다 (그들 도펀트는 **PS₄-S** 를 건드리고, 우리 계산상 **정작 얕은 것은 free-S** 다).

### 11-C. O 도핑 자리 — **우리 LPSOCl 모델이 이 논문 실험으로 지지된다** ✅
| 항목 | 이 논문 (실험) | 우리 (`db/properties/lpsocl_dos_gap.json`) |
|---|---|---|
| O 자리 | **S 16e (= PS₄-S)**, NPD Rietveld occ 0.075 + XPS **P–O 133.7 eV / O 1s 531.9 eV** | **PS₃O 단위** — P#30–O#50 **1.559 Å**, free-S 2 / PS₄-S 19 / Cl 8 / O 1 (62원자 셀) |
| 결과 | (전자구조는 Sb 와 뒤섞여 분리 불가) | **gap 2.2309 eV (+0.132 vs modelc), clean insulator, O 2p 가 VBM 아래 2.3–5.5 eV 에 매몰, VBM 은 S 3p 유지** |
| 판정 | — | ✅ **우리 O 자리 선택이 실험 Rietveld+XPS 와 같다** = 외부 지지. 그리고 **우리 쪽이 O-only 단일 도펀트 대조군**을 갖고 있다(그들은 Sb+O 를 분리 못 함) |

> 🔑 **여기서 우리가 더 말할 수 있는 것**: 이 논문의 갭 축소(figure-read)는 **O 가 아니라 Sb 탓**이다.
> 우리 +O-only 결과는 **갭이 오히려 0.132 eV 넓어지고 O 2p 가 매몰된다**. ⇒ *"O 는 밴드엣지를 안 건드린다,
> 밴드엣지를 내리는 건 Sb 다"* 를 우리 데이터로 분리해 말할 수 있다. **이 논문은 못 하는 분해다.**

### 11-D. 나머지 축 (요약)
| 축 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| **A 이온전도** | EIS Ea **≈0.295 → ≈0.250 eV** (figure-read), σ 2.6 → 5.3 mS/cm | comp1 Ea **0.253** / modelc **0.224** eV (**MLIP-MD** UMA, MSD 2–50 ps) | ⚠ **다른 양** (EIS 총합 Ea = 입내+입계 vs MD tracer Ea). **자릿수만 같다고 적는다.** 직접 비교 금지 |
| **B 산화 (축 B①)** | CV 재산화 순서 **S²⁻→S⁰ (≈2.7 V) 가 P⁰→P⁵⁺ (≈3.9 V) 보다 먼저** (figure-read) | grand-potential onset **2.256 V, S²⁻-limited** (comp1=modelc) | ✅ **순서 일치**(S 가 먼저). ⚠ 그들 것은 *재산화* 피크라 onset 이 아님 ⇒ **값 대조 금지, 순서만** |
| **B 산화 (축 B②, 전자 접근)** | σ_e **2.06×10⁻⁹ S/cm** | 우리 축에 **σ_e 없음** (gap 만) | ⛔ 대응 없음. [Deng26PS] 행과 같은 공백 |
| **C 기계** | 없음 | E_VRH 22.06 / 27.66 GPa | ⛔ 대응 없음 |
| **D 전자구조** | 갭 수치 **미제시**, `Fig. 5a` LPSC 패널은 **갭 없음** | comp1 **2.066** / modelc **2.099** / +B₂O₃ 1.9671 / LPSOCl **2.2309** eV (fixed-occ nscf) | 🔴 **우리가 우위.** 그들 기준계의 전자구조가 우리 canonical 과 정성적으로 충돌 ⇒ **그들 PDOS 를 정량 근거로 쓰지 말 것** |
| **E 음극 계면** | Li_xSb_yS_z 부동태 (실험 3중 확인) + AIMD 10 ps | 우리는 음극 축 계산을 안 한다 | ⭕ **기록·이식 후보**. "전자 안 통하는 계면상을 *의도적으로* 만든다" = [Ke]·[LiInF] 와 같은 계열 |
| **F 도핑** | **Sb₂O₃ (Sb⁵⁺@P_4b + O@S_16e)** | cascade v23: **M³⁺ 26/26 이 Li_24g** (UMA) | ⚠ 충돌 축. **단 Sb 는 5+ 라 M³⁺ 규칙의 대상이 아니다** — Sb⁵⁺@P 는 등가치환이라 우리 site-rule 과 **모순이 아니다**. [WangYO] 의 **Y³⁺@P** 주장과는 다르다 |

---

## 12. 적용 인사이트 (우리 연구에 어떻게)
1. **★ 우리 free-S ⟨3p⟩ 지표를 "설계 서술자" 로 승격시킬 근거가 생겼다.** AFM 급 저널이 ε_p 하나로
   양쪽 계면을 설명하는 논문을 실었다. 우리는 **같은 서술자를 자리분해 + 고정창(−8..0 eV) + VBM 참조**로
   갖고 있고, 그들이 못 하는 **"어느 S 를 내려야 하는가"** 를 답한다. ⇒ 원고에서 ε_p 를 **인용 가능한 선행 개념**으로
   쓰고, 우리 기여를 *"site-resolved, window-fixed, VBM-referenced"* 로 명시하면 차별화가 선명하다.
2. **★ O 자리 선택의 외부 지지 확보.** 우리 LPSOCl 의 **O@PS₄-S (PS₃O, P–O 1.559 Å)** 가 이 논문의 NPD+XPS 와
   같은 자리다. 원고 §방법에 *"consistent with the O@16e assignment refined from NPD in Liu 2024"* 로 한 줄 넣을 수 있다.
3. **★ NEB 축의 우리 할 일이 확정됐다.** 이 논문은 우리 0.305 eV 를 검증하지 못한다. 그 대신
   **(a) 셀 수렴 2번째 셀** 이 `absolute_citable` 을 여는 유일한 문이라는 것이 더 분명해졌다.
   덤으로 이 논문은 **"끝점 비대칭 장벽을 방향 표시 없이 인용하면 안 된다"** 의 교보재다(우리 `Ea_effective` 규약의 정당화).
4. **계보 추적**: `Sb₂O₃(2024) → Y₂O₃(2025)` 가 같은 랩의 연속 전략이다. **다음 칸을 예측할 수 있고**,
   우리 cascade 도펀트 스크리닝(M+O 공도핑)의 **직접 경쟁·비교 대상**이 된다.
   ⇒ `comparison_vs_ours.md` §F "한 염 두 도펀트" 계보에 **7번째**로 등록.
5. **관측량 포맷 2개 차용**: (i) **XPS + XANES 이중 확인**으로 도펀트 산화수 주장하기,
   (ii) **XRD + XPS depth + TOF-SIMS 3D 삼중 확인**으로 계면상 동정하기. 우리 `interface_reactivity` 예측을
   실험팀에 넘길 때 이 포맷으로 요청하면 검증 가능한 주장이 된다.

## 13. 인용 가능 문장 (deck/paper 용)
- "Liu et al. (*Adv. Funct. Mater.* 2025, 35, 2412144) showed that Sb/O co-doping of Li₆PS₅Cl lowers the
  sulfur p-band centre of the tetrahedral unit from −2.06 eV (PS₄) to −2.57 eV (SbS₄) relative to E_F,
  and used this single descriptor to rationalise stabilisation of **both** the Li-metal and the S₈ interface."
- "In that work the only barrier computed by the authors is 0.23 eV for Li⁺ crossing the LiSbS₂ interphase;
  the frequently quoted 0.22 eV for Li₂S and 0.67 eV for LiF are **cited from Lai et al., *Nano Lett.* 2020, 20, 8273**,
  not calculated there."
- "The O dopant refines onto the 16e (PS₄-sulfur) site by neutron powder diffraction, consistent with the
  PS₃O unit used in our O-substituted argyrodite model."
- ⛔ **쓰면 안 되는 문장**: *"문헌 Li₂S 장벽 0.22 eV 는 우리 0.305 eV 와 …"* — `forbidden_statement` 위반.
- ⛔ **쓰면 안 되는 문장**: *"ε_p 가 0.51 eV 내려간다"* 를 **정량 근거**로 이식하는 것 (§10-②).

## 14. 기법 용어 미니사전
- **p-band center (ε_p)**: 어떤 원자의 p-PDOS 를 에너지로 가중평균한 무게중심. d-band center 이론
  (Hammer–Nørskov, 촉매)의 p-궤도판. **깊을수록**(음수 클수록) 그 전자를 뽑기 어렵다 = 산화 저항.
  **참조준위(E_F vs VBM)와 적분창을 안 밝히면 서로 다른 논문끼리 비교 불가**. → 우리 규약: VBM 참조 · −8..0 eV.
- **CI-NEB (climbing-image nudged elastic band)**: 두 끝점 사이에 이미지(중간 구조)를 스프링으로 꿰고 이완시켜
  최소에너지경로를 찾는 방법. CI 는 최고점 이미지만 스프링을 끄고 **에너지를 거슬러 올라가게** 해 안장점을 정확히 잡는다.
  **끝점이 대칭 등가가 아니면 정/역 장벽이 다르다** — 방향을 밝히지 않은 장벽값은 반쪽이다.
- **jellium 배경 (우리 규약)**: 하전 결함(V_Li⁻)을 주기 셀에 넣으면 셀 전체 전하가 발산한다. 균일 반대전하
  배경(jellium)을 깔아 중화하는데, 이건 **유한셀 근사**라 셀 크기를 바꿔가며 수렴을 봐야 절대값을 쓸 수 있다.
  ⇒ 우리 `v2/li2s` 가 `provisional_single_cell` 인 이유.
- **DRT (distribution of relaxation times)**: EIS 를 완화시간 τ 축으로 역변환해 겹친 반원을 분리.
  τ≈10⁻⁴ s 대역이 SEI 응답으로 배정된다 — 이 논문의 `Fig. 2f` 가 그것.
- **XANES 흡수단 위치**: 원소의 형식산화수가 높을수록 흡수단이 고에너지로 이동. Sb₂O₃(3+)와 Sb₂O₅(5+) 사이면
  **혼합가**로 읽는다.
- **전하밀도차 (CDD)**: ρ(AB) − ρ(A) − ρ(B). 노랑=축적, 파랑=고갈이 관례. **isovalue 를 안 쓰면 크기 비교 불가**.
- **HSAB**: hard/soft acid–base. S²⁻(soft base)를 O²⁻(hard base)로 바꾸면 H⁺·H₂O(hard)와 덜 반응 → 대기 안정.
  **정성 논변이지 계산량이 아니다.**
