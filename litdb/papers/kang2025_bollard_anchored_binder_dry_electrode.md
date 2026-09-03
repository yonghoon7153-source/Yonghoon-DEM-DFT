# Bollard-Anchored Binder System for High-Loading Cathodes Fabricated via Dry Electrode Process — Kang, Jihyeon (Adv. Mater. 2025)

> slug `kang2025_bollard_anchored_binder_dry_electrode` · DOI `10.1002/adma.202416872` · type `exp + NNP(PFP) 흡착/MD + Gaussian16 DFT(IR)` · PDF 본문 `f5fb19c3-…Bollard_Anchored…pdf` · SI `26749347-adma202416872sup0001suppmat.pdf` · digested `2026-09-03` (**SI Movies S1–S3 전수 판독 + 픽셀 재측정**; 2판 SI-전수 `2026-08-29`; 초판 본문-only `2026-07-08`) · status ✅
>
> elements: C Co F H Li Mn Na Ni O
> methods: dft, md, mlip, xps
>
> ⚠ **동명 구분**: 제1저자 **Jihyeon Kang (중앙대 Chung-Ang)** ≠ 랩 자체논문의 **Junhee Kang (한양대, `kang2025_toughened_bimodal_nca_lzo`)** — 다른 사람, 다른 논문.
> 데이터 CSV: `docs/data/kang2025_bollard_binder_anchors.csv` · 크로핑 그림 42장: `litdb/figures/kang2025_bollard_anchored_binder_dry_electrode/`

---

## 0. 이 digest를 읽는 법 — 2026-08-29 재digest에서 무엇이 바뀌었나

초판(2026-07-08)은 **본문만** 보고 썼다. 이번엔 **SI 56 pp 전수 + 그림 실물 판독**으로 다시 썼고,
초판이 "SI 미확보"로 남겨둔 칸이 전부 채워졌다. 바뀐 것 6가지:

| # | 초판 | 재digest (확정) |
|---|---|---|
| ① | "MLP-DFT" (종류 미상) | **PFP v3.0.0 (Matlantis 범용 NNP)** — **DFT가 아니다**. 논문의 "deep-learning based DFT" 는 명명 오류 (§4.1) |
| ② | E_ads 3값만 | **15개 배열 개별값 전부** 확보 (Fig S15) — 8/3/4 로 나뉜 **사후분류**이고 보고값은 **class 평균** (§4.4) |
| ③ | porosity "25.9% 절대? 상대?" 중의적 | **Table S3 로 확정: 절대 25.90 / 19.47 / 17.68 %.** 단 **가정한 tap density 로 계산한 값**이라 독립 측정이 아니다 (§6.3, §10) |
| ④ | Fig 4c 축 = eV로 가정 | **축 라벨 `kJ mol⁻¹` 은 오류, 실제 eV 확정** (§5, Q1) |
| ⑤ | Na의 역할 불명 | **sodium CMC 의 실재 Na**이자 **–COO⁻ 2개의 전하중화 짝이온** — 15배열 전부 Na 2개 고정, 라벨 2/1/0 은 *표면접촉 Na 수* (§4.5 ★ 우리 SDCP 직결) |
| ⑥ | — | **내부 불일치 6건 신규 적발** (§10.1) |

### 0b. — 보강 2026-09-03 (3판): SI **동영상** 판독 + 전달물성 측정조건 복원

2판(08-29)은 SI **PDF** 를 전수로 읽었지만 **Supporting Movies S1–S3 (mp4 3편) 은 열지 않았다** —
그런데도 §4.8 이 "Na 가 표면 O 층 위를 **이동**한다" 를 *Movies S1–S3* 을 근거로 인용하고 있었다
(= **본 적 없는 매체를 근거로 단 문장**).  이번에 그 3편을 프레임 단위로 열고, 덤으로
전달물성(σ_e/σ_ion) 의 **빠져 있던 측정조건**을 역산으로 복원했다.  바뀐 것 6가지:

| # | 2판 | 3판 (보강) |
|---|---|---|
| ⑦ | Movies S1–S3 **미열람** (§4.8 이 인용만 함) | **337 프레임 × 3편 전수 판독 + 픽셀 궤적 재측정** (§4.10) — Fig 4f 를 *다른 매체에서 독립 재현*, **S1 최대 들뜸 t = 8.48 ps** 가 2판의 Fig 4f 디지타이즈 "8–8.5 ps 피크" 와 일치 |
| ⑧ | "Na migration … **정량 없음**(이동거리·hop 횟수 미보고)" (§4.8) | ★ **정량화됨**: 표면 Na 가 **가로 ~5 Å 미끄러지는 동안 세로 변화 ≲0.4 Å** = *탈착 없는 표면 활주* (§4.10-C).  2판이 비워둔 칸이 채워졌다 |
| ⑨ | PC_1Na 의 "자유 Na" = **본문 문장으로만** 확정 (§4.5) | ★ **영상으로 직접 확인** — S3 에서 Na 2개가 **337/337 프레임 전부**에서 분리 판별되고, 자유 Na 는 10 ps 내내 표면에 **한 번도 안 내려앉는다** (수직간격 64.4 ± 5.1 px) (§4.10-C) |
| ⑩ | Fig 3b 를 "시트저항 [Ω cm⁻²]" 로 그대로 옮김 | ★ **단위·명칭 오기 확정 + 빠진 측정조건 복원**: R_s→σ 역산이 5개 전극에서 **t = 99.3 ± 1.4 µm** 로 수렴 ⇒ 실제 양은 **Ω/□**, 두께는 **≈100 µm 공통** (§3e).  불일치 ⑦ 신규 |
| ⑪ | σ_ion 측정 = "SS│필름│전해질│SS, 25 °C" | ★ SI 원문이 **`L` = 필름 **+ 분리막** 두께**라고 적는다 — **블랭크 차감 없음** ⇒ 보고된 σ_ion 은 필름 고유값이 아니라 **(필름+분리막) 겉보기값**, 전 계열 상향 편향 (§3e).  불일치 ⑧ 신규 |
| ⑫ | — | **불일치 3건 추가 (⑦⑧⑨)** → 누계 **9건**, + **논지 결함 1건**(다공성이 σ_e 를 올린다는 귀속, §10.5) |

★ 이번에 **찾아봤지만 이 논문에 없는 것** (우리 축의 음성 결과 — §3e 에 별도 정리):
**접촉저항 수치 0건** · **성형압 수치 0건**(문서 전체에 `MPa/kPa/bar/psi/ton/kgf` 가 **한 번도** 안 나온다) ·
**탄소 퍼콜레이션 문턱 0건**(Super P 5 wt% **고정**, 스윕 없음) · **σ 의 온도·압력 조건 미기록**.

---

## 1. 한 줄 요약

건식전극(DBE)의 유일한 fibrillation 바인더 PTFE(PFAS 규제·이온절연·약한 접착)를 **"bollard hitch(계선주 매듭)" 이중-바인더**로 보완한다:
**PAA-grafted sodium CMC(=PC)가 NMC622 산화물 표면에 Na⁺-매개 화학흡착(E_ads −2.24 eV)으로 붙는 "bollard(계선주)"**가 되고,
**PTFE fibril이 그 bollard에 Na–F 상호작용(−0.35 eV)+PAA 가지와의 물리 얽힘으로 계류되는 "rope"**가 되어 —
PTFE를 2 → 0.6 wt%(>70% 감축)로 줄이고도 30 mg/cm²(4.0 mAh/cm²@2C) ~ 90 mg/cm²(15.6 mAh/cm²) 고로딩 양극을 만든다.
앵커링 물리는 **DFT가 아니라 범용 NNP(PFP v3.0.0)** 로 계산했고, **우리 SDCP 술폰산-NCM 화학앵커와 정확히 같은 개념-클래스**
(CAM 산화물 표면의 *이온성* 화학흡착이 PTFE의 vdW-only 접착을 대체)의 독립 선례다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **Jihyeon Kang†, Hojong Eom†, Seohyeon Jang†** (공동1저자), Doehyeob Yoo, Hyeonha Lee, Minju Kim, Myeong-Lok Seol, **Jeong Woo Han\***, **Inho Nam\***, **Hannah Song\*** | *Adv. Mater.* **2025**, 37, 2416872 (OA, CC BY-NC; 접수 2024-11-02 / 온라인 2025-02-18) | 10.1002/adma.202416872 | **NMC622 (LiNi₀.₆Mn₀.₂Co₀.₂O₂) + Super P + PTFE + PC(PAA-g-Na-CMC)**, C-coated Al, **액체 전해질 LIB** (⚠ SE 없음 — ASSB 아님) | exp (건식전극 제조·전기화학·XPS/XRM/UTM) + **NNP 흡착 + NVT-MD** + **Gaussian16 DFT (IR만)** |

- **소속**: 중앙대 화공/신소재/지능형에너지산업 + **현대차 배터리제조엔지니어링 R&D팀** + **NASA Ames/USRA** + 서울대 재료공학부(Jeong Woo Han).
- **바인더 명명**: PC = **P**AA-grafted **C**MC. 내부 최적 PAA:CMC = 5:5. `PC_PTFE73` = 바인더 내 PC:PTFE = 7:3.
- **PC 합성** (SI p.3): CMC 0.5 g + PAA 0.5 g / 증류수 50 mL → **155 °C, 250 rpm, 2 h** 탈수-축합 → 100 °C 12 h 건조 → ball mill 분쇄.
  **PC의 Mw = 7,107 g/mol (HPLC 측정)** ← ★ 계산 fragment(단량체 수준)와 실제 폴리머의 크기 차이를 재는 자.
- **원료** (SI p.3): NMC622 Umicore, Graphite Sigma, Super P(C65) Imerys, **PTFE = Solvay DF130**, PAA Sigma **Mv 450,000**, PVdF Sigma **Mw 534,000**,
  **Sodium carboxymethyl cellulose (Samchun C0292)** ← ★ **"sodium" CMC — Na는 실재 성분이다** (§4.5).
- **전극 조성**: NMC:SuperP:binder = **93:5:2 wt%** 고정. production `PC_PTFE73` = 93:5:**1.4(PC):0.6(PTFE)**.
- **공정** (SI p.4): 무용매 건식 — NMC+PC 30 min → +Super P 30 min → +PTFE **10 min**(마지막) → 반죽(dough) → 롤 압연 → C-coated Al 라미네이션.
  **hot roller: 하부 롤 145 °C > 상부 롤 130 °C**(전극이 상부에 붙는 것 방지), **feed 120 cm/min**, 목표밀도 3.0 g/cm³까지 반복 압연.
  로딩 15–90 mg/cm², 두께 50–333 μm. 믹서: planetary 30 min/cycle vs **ball mill 10 min/cycle**(과열 방지, 입자파쇄 회피 — Note S2).

## 3. 핵심 물성 (수치 총정리)

### 3a. 바인더 필름·바인더시스템 물성 (Fig 3; additive:PTFE = 1:1 필름)

| 물성 | PVdF_PTFE | CMC_PTFE | **PC_PTFE** | PAA_PTFE | PTFE | 출처 |
|---|---|---|---|---|---|---|
| σ_ionic (필름, EIS) [10⁻⁶ S/cm] | **255** | 178 | **131** | 127 | **4.88** | Fig 3a (stated) |
| 시트저항 [Ω cm⁻²] | 540.1 | 374.6 | **77.2** | 494.0 | 173.8 | Fig 3b (wet PVdF 2259.3) |
| σ_electronic (양극, 4-probe) [S/cm] | 0.19 | 0.27 | **1.30** | 0.20 | 0.58 | Fig 3c (wet PVdF 0.04) |
| swelling ratio (전해질 침지) | 1.45 | 1.23 | **1.13** | 0.99 | 1.01 | Fig 3d |
| **E (Young's, 필름)** [MPa] | 0.83 | 0.80 | **0.15** | 0.66 | **3.50** | Fig 3e (⚠ 필름-스케일 MPa) |
| 파단 strain [%] | 10.8 | 7.4 | **21.9** | 1.2 | **5.2** | Fig 3f |
| 180° peel (전극↔Al) [N/cm] | – | – | **0.9615** | – | 0.5733 | Fig S6 (**1.68×**) |

- ★ **초판이 놓친 나쁜 소식**: **σ_ionic 1위는 PC가 아니라 PVdF_PTFE(255)** 다. PC(131)는 CMC(178) 뒤 3위.
  "PC가 이온전도를 올린다"는 서술은 **PTFE-only(4.88) 대비 27×** 라는 뜻일 뿐, 바인더 5종 중 최고가 아니다. 인용 시 반드시 기준을 밝힐 것.
- **측정법** (SI p.5): σ_ionic = SS│binder film│liquid electrolyte│SS, σ = L/(R_b·S), 25 °C, φ19.0 mm 펀칭, 진공건조.
  **⚠ 액체전해질을 머금은 필름의 값**이지 건조 바인더의 고유 이온전도가 아니다 → swelling이 큰 바인더가 유리해지는 측정.
- **UTM** (SI p.6): 인장 1 cm × 3 cm, **0.5 mm/min**; peel = 3M 테이프 **12 mm 폭**, **6 mm/min**.
- ⚠ swelling "ratio" 정의 불일치: SI 식은 `S = (W_after−W_before)/W_before × 100%` (= % 증가율)인데 Fig 3d 값은 0.99–1.45 (= 배율). PAA의 0.99는 %로 읽으면 무의미. 축 라벨이 맞고 SI 식이 틀린 것으로 보인다.

### 3b. 앵커링 에너지 (PFP-NNP + MD) ★★

| 항목 | 값 | 출처 / 비고 |
|---|---|---|
| E_ads **PC_2Na** (Na 2개가 표면 O에 접촉) | **−2.24 eV** (본문) · **재계산 평균 −2.251 eV**, n=8 | Fig S15a 개별값: −2.33, −2.32, −2.32, −2.27, −2.25, −2.20, −2.16, −2.16 |
| E_ads **PC_1Na** | **−1.12 eV**, n=3 | Fig S15b: −1.14, −1.12, −1.10 (스프레드 ±0.02 — 사실상 1점) |
| E_ads **PC_0Na** (–OH/–COOH 장거리 쌍극자만) | **−0.37 eV** (재계산 −0.365), n=4 | Fig S15c: **−0.71, −0.34, −0.29, −0.12** (스프레드 6배 — 본문의 "substantial variance") |
| E_ads **PTFE dimer** | **−0.09 eV** | Fig 4c에 box는 있으나 **개별 배열은 SI에 없다** (n 미상) |
| E(Na–F) PC↔PTFE | **−0.35 eV** | PTFE–NMC 대비 **2–4.5×** 강함 |
| MD 탈착 (400 K, 10 ps) | PTFE-only **4.75 → 6.60 Å** (`figure-read`; 본문은 "4.2→6.6") / PC 동반 **4.53–5.04 Å 유지** | Fig 4f 디지타이즈 |
| XPS 검증 | F1s: C–F 688.89(PTFE) → 689.22 + **신규 691.99 eV(Na–F, 면적 우세)**; Na1s: 1070.5(Na–COO⁻) → +**1073.5 eV(Na–F, 우세)** | Note S3 / Fig S17 (⚠ 배정 의심 — §10.2) |

**사다리**: 이온성(−2.24) ≫ 이온성 절반(−1.12) ≫ 극성 쌍극자(−0.37) ≫ vdW(−0.09 eV). **25× 스팬.**

### 3c. 전극·전기화학 (LIB, 액체 전해질 1 M LiPF₆ EC/DMC 1:1, 33 μL/cm²)

| 물성 | 값 | 조건 | 출처 |
|---|---|---|---|
| **porosity** ★확정 | **PC_PTFE73 25.90 % / PTFE 19.47 % / PVdF 17.68 %** | 모두 밀도 3.0 g/cm³ | **Table S1**→**Table S3** (본문 문장은 중의적, 표가 정본) |
| tap density (porosity 계산 입력) | NMC **4.86** / Super P **1.60** / PC_PTFE73 **1.17** / PTFE **0.52** / PVdF **0.45** g/cm³ | 가정값 | Table S3 ★ porosity 차이의 **유일한** 원인 |
| tortuosity τ | PC_PTFE **1.30** vs PTFE **1.40** | 단면 SEM 기반 | 본문 (τ² 아님 주의) |
| PTFE 최소 fibrillation 함량 | **0.6 wt%** (PC_PTFE73). PC_PTFE91(0.2 wt%)는 **dough 형성 실패**; PTFE-only는 **2 wt%** 필요 | dough 성형성 | 본문 + Fig S10 ★ |
| 혼합-분산 산포 (2C, 30 mg/cm²) | wet 88.12±**11.37** → 기본 103.65±**16.52** → planetary×1 118.22±**5.59** → **ball mill×3 127.67±4.28** mAh/g | PTFE-only 전극 | Fig 2 ★ 분산 CV 앵커 |
| rate (30 mg/cm², PC_PTFE73) | 1/3C **168.5**(5.0 mAh/cm²) · 1C **159.5**(4.8) · 2C **133.2**(4.0) | vs PTFE 2C 108.1(3.2) · PVdF 2C 76.5(2.3) | Fig 5c |
| 사이클 (25 mg/cm², 1/3C, 100 cyc) | PC_PTFE73 **139.2 mAh/g = 83 %** / PTFE 84.0 = **51 %** / PVdF wet 77.6 = **47 %** | PTFE·PVdF는 ~70 cyc 후 급락 | Fig 5d |
| R_ct | 10 cyc **39.01** vs 68.65 Ω; 100 cyc **48.08** vs 91.52 Ω | PC_PTFE73 vs PTFE, 3.7 V, 10⁵–10⁻³ Hz, 10 mV | Fig 5e,f / S24 |
| D_Li⁺ | **5.09e-14** vs 2.53e-15 m²/s (**20×**) | 10 cyc 후, EIS Warburg | Fig S25 |
| 초고로딩 | **90 mg/cm² = 15.6 mAh/cm²** (⚠ Table S1/S2는 **15.3**), 0.1C 50 cyc 안정 | | Fig 5g,h |
| 사이클 후 AM 균열 | PTFE: NMC 2차입자 **파쇄**(흰 원) / PC_PTFE73: 균열 無 | 100 cyc | Fig S21 (정성) ★ |
| CEI LiF 분율 (F1s) | PC_PTFE73 **29.8 %** vs PTFE **37.4 %** | 100 cyc, 스퍼터 10/20/30 s | Fig S28 |
| 풀셀 | dry-dry(Graphite@PTFE): 2C 119.8 mAh/g, 0.5C 50 cyc **84 %**; dry-wet: 0.2C 100 cyc **86 %**; 파우치 **8 mAh/cm²**@0.5C | N/P = **1.08**, graphite:NMC ≈ 1:1.5 | Fig S32–S35 / Table S4 |
| 고전압 | CV 첫 사이클 패시베이션 후 **5.0 V까지 안정**; LSV 2.5–5.0 V, 1 mV/s, SS│PC_PTFE73 film | | Fig S23 / S39 |

### 3d. Table S1 / S2 — 선행 DBE·습식 고로딩 대비 (이 논문의 self-positioning)

- **This work**: 30 mg/cm², 3.0 g/cm³, 93:5:2, 2.5–4.25 V → **5.28 / 5.0 / 4.8 / 4.0 mAh cm⁻²** (0.1 / 0.33 / 1 / 2 C), **651 / 622 / 592 / 492 Wh kg⁻¹**;
  90 mg/cm² → **15.3 mAh cm⁻², 629 Wh kg⁻¹** @0.1C.
- 비교 대상 중 areal capacity가 더 큰 것들: [29] LCO 101 mg/cm² 15 mAh/cm²(단 1C 3.3 → 2C 0.5로 붕괴), [32] NMC721 press 100 mg/cm² 17.6 mAh/cm²(0.1C만).
  → 이 논문의 실제 우위는 **절대 areal capacity가 아니라 고율에서의 유지**(2C 4.0 mAh/cm²는 표 내 최고급).
- ⚠ **에너지밀도 산정법이 자의적** (Table S2 각주): `Wh/kg = 비용량 × 공칭전압 3.7 V`. **활물질 기준**이고 집전체·분리막·전해질·케이스를 안 뺀다.
  즉 **셀 수준 Wh/kg이 아니다** — 651 Wh/kg 를 셀 값처럼 인용하면 안 된다.

### 3e. ★★ 전달물성의 **측정조건** — 복원한 것과 끝내 없는 것 (— 보강 2026-09-03)

우리 규약("측정 조건 없는 값을 앵커로 적지 말 것")에 맞춰 σ_e·σ_ion 의 조건을 **끝까지** 추적했다.

**(가) σ_e = 1.30 S/cm — 조건 대부분 복원됨, 단 하나가 논문에 없다**

| 조건 | 값 | 출처 |
|---|---|---|
| 방법 | **4-probe, Keithley 2400** (Tektronix) | SI p.7 |
| 시편 | **전극**(필름 아님). 조성 **NMC622 : Super P : PTFE : 첨가바인더 = 93 : 5 : 1 : 1 wt%** | 본문 p.6 ★ |
| 밀도 | 3.0 g/cm³ (전 시편 공통 목표밀도) | SI p.4 |
| 두께 | 논문 서술 = *"The thickness of each fabricated electrode was **identical**"* — **수치 없음** | SI p.7 |
| **압력** | ⛔ **없다.** 자립(free-standing) 시트에 4-probe → **무가압**.  스택압 개념 자체가 등장하지 않는다 | 전문 |
| 온도 | ⛔ **미기록** (25 °C 는 σ_ion·셀시험에만 명시되고 4-probe 에는 없다) | — |

★★ **빠진 두께를 역산으로 복원했다.**  Fig 3b(R_s)와 Fig 3c(σ_e)는 같은 시편의 짝이므로
`σ = 1/(R_s · t)` 가 성립해야 한다.  6쌍 전부 풀면:

| 바인더 | R_s [Ω/□] | σ_e [S/cm] | 함의 두께 `t = 1/(σ·R_s)` |
|---|---|---|---|
| PVdF_PTFE | 540.1 | 0.19 | 97.4 µm |
| CMC_PTFE | 374.6 | 0.27 | 98.9 µm |
| **PC_PTFE** | **77.2** | **1.30** | **99.6 µm** |
| PAA_PTFE | 494.0 | 0.20 | 101.2 µm |
| PTFE | 173.8 | 0.58 | 99.2 µm |
| (습식 PVdF) | 2259.3 | 0.04 | 110.7 µm |

**건식 5종 = 99.3 ± 1.4 µm** (범위 97.4–101.2).  세 가지가 동시에 확정된다:
1. **양의 정체 = 시트저항 `R_s` [Ω/□]** 다.  본문은 *"sheet resistance"*, Fig 3b 축은 *"Resistivity (Ω cm⁻²)"* 로
   **이름이 둘, 단위가 셋 다 틀렸다**(시트저항 Ω/□ · 비저항 Ω·cm · 인쇄된 Ω·cm⁻² 는 셋 다 다른 차원) → **불일치 ⑦**(§10.1).
2. **두께 ≈ 100 µm 공통** — 논문이 "identical" 이라고만 하고 안 적은 값이다.  **Table S4 의 양극 100 µm**(30 mg/cm², 3.0 g/cm³) 와 일치 ⇒ 독립 정합.
3. σ_e 는 **독립 측정이 아니라 R_s 의 유도량**이고, 그 유도가 **자기일관**하다 (±2 %).  ⇒ **σ_e 값 자체는 신뢰 가능**하다.

⚠ **그러나 이 σ_e 는 production 조성이 아니다.**  1.30 S/cm 는 **PC : PTFE = 1 : 1**(=`93:5:1:1`) 전극 값이고,
production 은 **PC_PTFE73 = `93:5:0.6(PTFE):1.4(PC)`** 다.  **1.30 을 PC_PTFE73 의 σ_e 로 인용하면 안 된다** — 논문은 73 조성의 σ_e 를 재지 않았다.

**(나) σ_ion (필름) — 분모가 아니라 *분자*에 분리막이 들어간다** ★ 신규

SI p.6 원문: *"σ = L/(R_b·S), where R_b represents the bulk resistance according to the EIS measurement,
**L represents the thickness of the binder film and separator**, and S represents the area of the stainless steel."*

- 즉 **`L` 에 분리막 두께가 포함**되어 있고, **분리막-only 블랭크 차감이 언급되지 않는다.**
- 결과: 보고된 σ_ion 은 **필름 고유값이 아니라 (필름 + 분리막) 직렬 스택의 겉보기 전도도**이고,
  분자를 `L_film + L_sep` 로 키웠으므로 **전 계열이 `(L_film+L_sep)/L_film` 배만큼 상향 편향**된다.
- **필름 두께가 논문 어디에도 없다** ⇒ 편향 크기를 계산할 수 없다.  분리막이 25 µm(Table S4)이므로
  필름이 25 µm면 2배, 100 µm면 1.25배 — **바인더마다 필름 두께가 다르면 순위까지 흔들린다.**
- 이미 알려진 편향(§3a: 액체전해질을 머금은 필름이라 **swelling 큰 바인더가 유리**)과 **독립적인 두 번째 편향**이다.
- ⇒ **불일치 ⑧**(§10.1).  **σ_ion 5개 값은 "겉보기·상대"로만 쓸 것**; PTFE 대비 배수(27×)도 이 편향을 공유한 채의 배수다.
- 나머지 조건은 명시돼 있다: **25 °C**, SS│필름│액체전해질│SS, φ19.0 mm 펀칭, 진공건조, 첨가제:PTFE = **1:1** 필름, EIS 10 mV / 10⁵–10⁻³ Hz (ZIVE SP1, ZMAN 피팅).

**(다) ⛔ 이 논문에 *없는* 것 — 우리 축의 음성 결과** (추측으로 채우지 않는다)

| 우리 축 | 이 논문의 상태 |
|---|---|
| **접촉저항 (입자-입자 / 집전체 계면)** | ⛔ **0건.**  `contact resistance` 라는 말이 본문·SI에 **한 번도** 없다.  유일한 "저항" 3종은 (i) 필름 EIS 의 **벌크저항 R_b**, (ii) **시트저항 R_s**, (iii) 반쪽셀 EIS 반원 = *"interfacial resistance"* **39.01 / 48.08 Ω (PC_PTFE73) vs 68.65 / 91.52 Ω (PTFE)** @10·100 cyc.  ⚠ 이 (iii)은 **전하이동(R_ct) 계열**이지 **입자접촉 협착저항이 아니다** — 우리 CL-38(복셀 솔버가 접촉저항을 0 으로 둠) 의 **제3자 근거가 되지 못한다** (§7 참조) |
| **성형압 ↔ porosity / Heckel** | ⛔ **0건.**  본문+SI 전문에 **압력 단위가 하나도 없다** (`MPa` `kPa` `bar` `psi` `ton` `kN` `kgf` 전수 검색 = 0).  압밀은 **압력이 아니라 목표밀도로 규정**된다: 열간 롤(하부 **145 °C** / 상부 **130 °C**, feed **120 cm/min**)로 **3.0 g/cm³ 에 도달할 때까지 여러 번 통과**.  ⇒ 다압력 곡선·Heckel 불가 (§7 ★ 이 "밀도-목표" 규약 자체는 우리 MPM `--protocol hold` 의 산업판이다) |
| **탄소 퍼콜레이션 문턱** | ⛔ **0건.**  `percolation` 이라는 말이 전문에 없고, **Super P 는 5 wt% 로 전 시편 고정**이다.  탄소 함량 스윕이 없으므로 문턱도 σ_e-vs-탄소% 곡선도 못 얻는다.  변화한 것은 **바인더 종류**뿐 |
| **기계 물성 (우리 MPM 입력)** | 🔶 **필름 스케일만.**  E = PTFE **3.50** / PC_PTFE **0.15** MPa 등(Fig 3e) — 이는 **다공 fibril 시트**의 유효값이고 `MPa`·`GPa` 문자열은 **본문 텍스트에 없다**(그림에서만 읽힘).  우리 `PTFE 1.8 GPa` 와 **~500–1000× 차이** ⇒ **MPM 입력 불가, 서열만** (§10.4 기존 항목과 동일 판정) |
| **바인더 함량 효과** | ✅ **있다** (이 논문의 강점): PTFE fibrillation 하한 **0.6 wt%**(앵커 지원) / **2 wt%**(단독) / **0.2 wt% 실패**; PC:PTFE 비 스윕(Fig 3j)·PAA:CMC 비 스윕(Fig 3i) |

---

## 4. 계산 방법 ★★★ (이 digest의 본체)

### 4.1 무엇으로 계산했나 — "deep-learning based DFT" 는 명명 오류

SI p.7 원문:
> *"Deep-learning based density functional theory (DFT) and molecular dynamics (MD) simulations were conducted using the **preferred potential (PFP)** version **v3.0.0** as a **universal neural network potential (NNP) estimator** for the computation of atomic forces. The calculations were performed using **Matlantis** software, which was integrated with the PFP model through its API client."*

**판정: 흡착에너지·MD는 DFT가 아니다.** PFP(Takamoto et al., *Nat. Commun.* **13**, 2991 (2022))는 45원소 범용 NNP이고,
Matlantis는 PFN/ENEOS의 상용 SaaS다. 전자구조를 푸는 단계가 **한 번도 없다**. 본문의 *"machine learning potential based density functional theory calculations"* 도 같은 오용.

- **우리 언어로**: 이 논문의 E_ads·MD는 우리 `uma-s-1p1` SDCP 계산과 **완전히 같은 층위**(범용 MLIP single-point/relax)다. **DFT 층위가 아니다.**
- 따라서 이 논문 값과 *DFT* 값을 나란히 놓는 비교는 전부 부적절하다. 우리 MLIP 값과는 층위가 맞다 (그래도 절대값 비교는 금지 — §7).
- **PFP 버전만 있고 학습셋·컷오프·앙상블·불확실도 추정이 전혀 없다.** OOD(분자-산화물 계면, Na⁺ 브리지) 신뢰도를 판단할 근거 0.

### 4.2 진동수(IR)만 진짜 DFT — Gaussian16

SI p.7:
> *"Vibrational frequency calculations were performed using the **Gaussian16** program … within DFT formalism using **B3LYP** hybrid functional and a **6-31G basis set supplemented by two diffuse functions**. One set of **d polarization** functions were added to the heavy atoms, and **two sets of p polarization** functions were added to the H atoms."*

- 즉 **B3LYP / 6-31++G(d,2p)** 급 (표기가 비표준이라 정확한 Pople 라벨은 재구성). 기체상, 용매모델 언급 없음.
- **주파수 scale factor = 0.945** (Fig S13 캡션). B3LYP/6-31G* 계열의 통상 스케일(0.960–0.965)보다 **낮다** — 특정 밴드에 맞춘 흔적.
- 계산 결과 (Fig S13, 실물 판독): **PAA C=O 1710** / **CMC COO⁻ 1527** / **CMC C–O–C 1043 cm⁻¹**.
  실험(Fig 4a): 1710 / **1590** / **1021**. → **C=O는 정확히 일치(1710↔1710)**, COO⁻는 **63 cm⁻¹**, C–O–C는 **22 cm⁻¹** 어긋난다.
  → C=O가 소수점까지 맞는 것은 우연이 아니라 **scale factor를 그 밴드에 맞춰 뽑았기 때문**으로 읽힌다. 나머지 밴드의 정합은 그만큼 약하다.
  IR 계산의 역할은 **피크 배정 보조**까지이고, "DFT가 구조를 증명했다"로 확대하면 안 된다.

### 4.3 표면 모델 (NMC622 슬랩)

SI p.7–8:
> *"The **fully lithiated NMC 622 (LiNi₀.₆Mn₀.₂Co₀.₂O₂)** surface with an **R-3m** space group was constructed. The **Co and Ni atoms in the transition metal layer were arranged such that each atom of the same element was spaced √3 units apart.** A **2 × 2 × 1 NMC slab** with a **40 Å vacuum** was prepared."*

| 항목 | 값 | 우리 관점 코멘트 |
|---|---|---|
| 조성/상 | LiNi₀.₆Mn₀.₂Co₀.₂O₂, `R-3m` layered, **fully lithiated** (SOC 0 %) | 실제 앵커링은 충전상태(delithiated)에서 문제가 되는데 **가장 안전한 상태만 계산**했다 |
| 슬랩 | **2 × 2 × 1**, 진공 **40 Å** | 원자수·층수·표면 facet **전부 미기재**. Fig S15 측면도로는 **O–TM–O 트라이레이어 1–2겹**으로 보인다 (얇음) |
| 표면 종단 | **미기재**. Fig S15에서 최상층은 **O**, 그 아래 회색(Ni)/분홍(Mn) TM 열 | ⚠ **Li 층이 어디 있는지 그림에서 안 보인다.** Fig 4c/S15 색 범례에 **Li와 Co가 아예 없다** — "fully lithiated"인데 표면 Li의 거동(Na⁺와 O 사이트 경쟁)을 확인할 수 없다 |
| **무질서 처리** ★ | **SQS 아님, enumerate 아님.** TM층에서 **같은 원소끼리 √3 간격**이 되도록 배치한 **단일 규칙적 배열 1개** | 조성 무질서를 **의도적으로 없앤 결정론적 decoration**. 배열 앙상블 없음 → E_ads의 TM-배열 의존성 미측정 |
| 고정 | **슬랩 하반부 고정**, 상반부 + adsorbate만 완화 | 표준 |
| dipole correction / 쌍극자 보정 | **언급 없음** | 비대칭 슬랩 + 극성 흡착종(Na⁺-COO⁻)인데 보정 언급 0. NNP라 전기장 보정 개념 자체가 없다는 점도 관련 |

### 4.4 최적화·흡착에너지 프로토콜

- **최적화**: **ASE 라이브러리의 L-BFGS**, `fmax_threshold = 0.01` (SI는 단위를 **"0.01 eV"** 로 적었다 — force의 단위는 eV/Å 이므로 **단위 오기**).
- **최적화 대상 단일종 5개**: `PAA dimer` · `CMC monomer` · **`PAA dimer grafted CMC (PC)`** · `PTFE dimer` · **`PTFE long chain (n = 48)`**.
- **흡착에너지 정의**: `E_ads = E_slab-binder − (E_slab + E_binder)` — 표준 부호(음수 = 안정). 분산·ZPE·엔트로피 보정 없음(NNP라 vdW는 포텐셜에 내재).

**샘플링과 집계 — 이 논문 계산의 핵심 설계** (본문 p.7):
> *"Following the construction of the NMC surface model, the **PC molecule was rotated through 15 different configurations**, and the corresponding adsorption energies were calculated. **The adsorption states were classified into three primary categories**: 1) two Na atoms from PC adsorbed onto the O atoms of the NMC surface (PC_2Na), 2) one Na atom adsorbed (PC_1Na), and 3) long distance interactions … (PC_0Na). … **The average adsorption energy values for each of the corresponding adsorption states were calculated** and used for further analysis (Figure S15)."*

**→ 판정: 완전한 사후분류(post-hoc classification)다.** 근거 3중:
1. 문장 구조가 "15개 회전 → 계산 → *그 다음* 분류". 초기구조를 2Na/1Na/0Na로 **설계한 게 아니다**.
2. **Fig S15 실물 판독으로 class 크기가 8 / 3 / 4 = 15 로 정확히 맞는다.** 설계였다면 5/5/5 같은 균형 배분이 나왔을 것이다.
3. 라벨 자체가 **완화 후 결과**의 서술("Na 몇 개가 표면 O에 붙었나")이지 입력 조건이 아니다.

**→ 그래서 보고값 −2.24 / −1.12 / −0.37 eV는 "상태의 흡착에너지"가 아니라 "사후에 묶은 군집의 표본평균"이다.**
우리 CLAUDE.md 규율의 언어로: **admissible state가 여럿인데 집계 규칙(class-mean)을 결과를 보고 정했다.**
논문의 결론(사다리 방향)은 이걸로 안 흔들리지만, **숫자를 estimand로 이식하는 것은 금지**다.

| class | n | 개별값 (eV) | 평균 | median | 스프레드 |
|---|---|---|---|---|---|
| PC_2Na | **8** | −2.33 −2.32 −2.32 −2.27 −2.25 −2.20 −2.16 −2.16 | **−2.251** (논문 ≈−2.24) | −2.26 | 0.17 |
| PC_1Na | **3** | −1.14 −1.12 −1.10 | **−1.12** ✓ | −1.12 | **0.04** |
| PC_0Na | **4** | −0.71 −0.34 −0.29 −0.12 | **−0.365** (논문 −0.37) ✓ | −0.315 | **0.59** |
| PTFE_dimer | **미상** | SI에 개별 구조 없음 | −0.09 | — | Fig 4c box ≈0.12 폭 |

- "PC_1Na가 PC_2Na의 **정확히 절반**"은 물리 법칙이 아니라 **n=3, 스프레드 0.04 eV의 우연**일 수 있다. 논문은 이 우연을 "약 절반"이라고 서술만 하고 해석하지 않는다 — 그 절제는 적절하다.
- **PC_0Na의 스프레드(0.59 eV)가 class 평균(0.37)보다 크다.** 이 class의 평균은 사실상 의미가 없다.

### 4.5 ★★ Na⁺ 짝이온 — 왜, 어떻게 들어갔나 (우리 SDCP에 직결)

**질문**: PC의 −COO⁻ 를 중성계로 만들려고 Na를 인위로 넣은 것인가, 아니면 sodium CMC라 원래 있는 것인가?

**답: 둘 다다. 순서가 중요하다 — ① 실재하기 때문에 넣었고, ② 넣고 보니 그게 전하중화도 해결했고, ③ 결국 그게 결합 자리 자체가 됐다.**

**근거 (인용)**

1. **화학적으로 실재한다** — 원료 자체가 나트륨염이다.
   - SI p.3: *"**Sodium carboxymethyl cellulose** (CMC, No.C0292, Mw = 263) was purchased from Samchun chemical."*
   - 초록: *"Poly(acrylic acid)-grafted **sodium carboxymethyl cellulose** (PC) acts as the 'bollard'"*
   - Note S3: *"the Na 1s spectra displayed peaks at **1070.5 eV** in the PC film, corresponding to **Na–COO⁻ bonds**"* → Na는 카복실레이트의 짝이온으로 **실험적으로 검출**된다.
   - 본문 p.7: *"EDS analysis showed that **Na elements remained within the molecular structure of PC** and were evenly distributed on the surface of NMC."* → Na를 **PC의 EDS 마커**로 쓴다 (Fig 1h, Fig S14b).
   - FTIR에서 CMC 밴드가 **carboxylate(COO⁻) 1590 cm⁻¹**로 배정된다(카복실산 C=O 1710이 아니라) → **염 형태 확정**.
2. **계산에서의 역할은 정확히 전하중화 짝이온이다.**
   - Fig S15 실물 판독: **15개 배열 전부 노란 Na 구가 2개**다. PC_0Na 배열에서도 Na 2개가 그대로 있고, 단지 표면에 안 닿아 있을 뿐이다.
   - Fig 4b(PC 형성 모식)에서도 −COO⁻ 2개에 Na 2개가 붙어 있다.
   - 즉 fragment = (PAA-dimer-grafted CMC-monomer)²⁻ + 2 Na⁺ = **총전하 0의 닫힌 껍질 중성종**.
     → 배경전하(jellium)·Makov-Payne 보정·대전 슬랩 문제를 **전부 회피**한다. NNP는 애초에 대전계를 다룰 수 없으므로 이건 **필수 선택**이었다.
3. **라벨 2Na/1Na/0Na는 조성이 아니라 "표면에 접촉한 Na 수"다.**
   - 본문이 이걸 확정한다: *"The **free Na site** in the PC_1Na system strongly interacted with the F atoms of the detached PTFE"* — PC_1Na에도 **두 번째(자유) Na가 존재**한다.
   - Fig S16c,d의 빨간 화살표가 가리키는 것이 바로 그 자유 Na가 PTFE의 F를 붙잡은 장면이다.

**결합 모티프 (Fig S15a 확대 판독)**: 각 Na⁺는 **위로 카복실레이트 O 2개(4원환 킬레이트) + 아래로 표면 O 2개**에 배위한다.
즉 앵커의 실체는 **`–COO⁻ ··· Na⁺ ··· O²⁻(surface)` 양이온 브리지**다. 유기 음이온기가 산화물에 *직접* 붙는 게 아니라, **짝이온이 다리를 놓는다.**

> ### ★ 우리 SDCP 캠페인으로 가져갈 것 (이 논문에서 가장 값진 한 조각)
> 우리도 **음이온기(–SO₃⁻)를 중성계에서 다뤄야** 한다. 이 논문이 보여준 처방과 그 함정:
> - **처방**: 짝이온(Na⁺/Li⁺)을 명시적으로 넣어 fragment를 중성으로 만든다 → 대전 셀 보정 불필요, MLIP에서 유일하게 가능한 길.
> - **함정 ①**: 짝이온을 넣는 순간 **그 짝이온이 결합 자리가 되어 버린다.** 이 논문의 −2.24 eV는 "–COO⁻ 가 NMC에 붙는 에너지"가 **아니라** "Na⁺ 2개가 표면 O에 붙는 에너지"다.
>   우리가 −SO₃⁻ + Li⁺ 로 중성화하면, 측정되는 것은 술폰산-표면 결합이 아니라 **Li⁺ 브리지**일 수 있다. **estimand가 조용히 바뀐다.**
> - **함정 ②**: 짝이온의 **초기 배치가 곧 상태 선택**이다. 이 논문은 15개 회전으로 우연히 3개 상태를 얻었지만, 그 상태 분포는 **초기 배치 프로토콜의 함수**다.
> - **우리 대응**: `kb/templates/estimand_card.md` §1–3에 **"짝이온을 어디에 두는가"와 "무엇을 X로 정의하는가"를 미리 적는다.**
>   `X(짝이온 배치정책)` 으로 상태를 선언하거나, 짝이온-없는 대전계 + 보정과의 **두 경로를 모두** 계산해 차이를 보고한다.
>   ⛔ 이 논문처럼 "결과를 보고 상태를 3개로 나눈 뒤 class 평균" 을 하면 우리 규율 위반이다 (decisions.json 등록 대상).

### 4.6 ★ PTFE `n = 48` 장쇄는 어디에 쓰였나 (Q4)

**답: MD 전용이다. 흡착에너지(Fig 4c)에는 PTFE _dimer_ 가, MD(Fig 4d–f, S16)에는 _n=48 장쇄_ 가 쓰였다.**

근거:
- SI p.8이 최적화 단일종 목록에 `PTFE dimer` 와 `PTFE long chain (n = 48)` 을 **따로** 올린다.
- Fig 4c의 x축 라벨이 명시적으로 **`PTFE_dimer`** 다 (−0.09 eV는 dimer 값).
- Fig 4d,e 캡션: *"**The same length of the PTFE binder was used in both calculations.**"* + 그림 실물에서 사슬이 **40개 이상의 CF₂ 단위**로 길게 그려져 있다(Fig S16a에서 U자로 감긴 장쇄).
- ⚠ **따라서 −0.09 eV(dimer)를 MD에 등장하는 장쇄의 결합력으로 읽으면 안 된다.** 장쇄의 E_ads는 **계산되지 않았다**.
  n=48이면 표면 접촉 원자수가 dimer의 수십 배라 총 vdW 결합에너지는 훨씬 클 것이다 — 실제로 Fig 4f에서 PTFE-only 사슬은 10 ps 동안 **완전히 떨어지지 않고 ~6.6 Å에서 멈춘다.**
  "PTFE는 −0.09 eV라 약하다"는 서술과 "MD에서 장쇄가 안 날아간다"는 관찰 사이의 간극이 여기서 나온다.

### 4.7 MD 프로토콜

SI p.8:
> *"MD simulations were performed using the **NVT ensemble (Langevin heat bath method)**. The simulation time was **10 ps** with a **1 fs** time step **after reaching 400 K** while **fixing the lower half of the NMC surface**. The **friction coefficient was 0.01**."*

| 항목 | 값 | 코멘트 |
|---|---|---|
| 앙상블/열욕 | NVT, Langevin, **friction 0.01** (단위 미기재, ASE 관례상 fs⁻¹ 또는 무차원) | 우리 MLIP-MD 표준(friction 0.02, dt 2 fs)과 같은 계열 |
| T | **400 K** — *"To guarantee sufficient binder dynamics, MD was performed at high temperatures"* | 가속 목적의 가혹조건. **온도 1점**이라 아레니우스·활성화에너지 없음 |
| 시간 | **10 ps** 생산 (승온 구간 길이 미기재) | ⚠ 폴리머 사슬 완화시간에 비해 **매우 짧다**. 결합 파괴 통계 아님 |
| 시드 | **1개 추정** (복수 시드 언급 0) | 오차막대 없음 |
| 계 3종 | (a) PTFE only, (b) PC_2Na + PTFE, (c) PC_1Na + PTFE | **PC_0Na + PTFE 는 안 돌렸다** (사다리 하단이 비었다) |
| 산출 지표 | **표면으로부터의 평균거리 시계열** (Fig 4f) | 정의가 문서마다 다르다 — 아래 |

**⚠ 거리 지표의 정의가 세 곳에서 서로 다르다:**
- 본문: *"The average distance of **the F atoms** in PTFE near the surface"* → **F만**, 게다가 "near the surface"라는 미정의 필터.
- Fig 4 캡션: *"the **C and F atoms** in dark brown and blue from (d) and (e) were **only considered**"* → **C+F**, 그리고 **색으로 지정된 부분집합만**.
- Fig S16 캡션: *"The **C and F atoms** in dark brown and blue, respectively, are **only considered** for the average distance calculation (Figure 4f)."* → 캡션끼리는 일치.

그림 실물(Fig 4d,e / S16)에서 PTFE 사슬은 **진한 파랑/진한 갈색 구간과 옅은 파랑/옅은 갈색 구간의 2색**으로 그려져 있다.
→ **평균에 들어가는 것은 사슬 전체가 아니라 손으로 고른 진한 색 구간뿐이고, 그 선택 규칙은 어디에도 없다.**
이것이 4.75→6.60 Å 라는 숫자의 신뢰도를 결정적으로 깎는다 (§10.1-③).

**MD가 실제로 보여준 것 (Fig 4f 디지타이즈, `figure-read`)**

| 계 | t=0 | 궤적 | t=10 ps |
|---|---|---|---|
| PTFE only | **≈4.75 Å** | 0–4 ps 상승 → 4–7 ps 고원 6.1–6.3 → 8–8.5 ps **≈6.71** | **≈6.60 Å** |
| PC_2Na + PTFE | ≈4.83 | 4.55–**5.04** 요동 | ≈4.57 |
| PC_1Na + PTFE | ≈4.58 | 4.53–4.80 요동 | ≈4.54 |

- 본문의 *"an initial **4.2 Å**"* 는 **그림에서 읽히지 않는다** (y축 하한이 4.0인데 어떤 곡선도 4.2 근처에 없다).
  화해 가능한 해석: 4.2 Å은 **승온 전 초기 기하**의 값이고 Fig 4f의 t=0은 400 K 도달 후 시점일 수 있다. 논문은 그 구분을 안 한다.
- 본문의 *"fluctuated between 4.5 and 4.9 Å"* 도 PC_2Na가 8.3 ps에서 **5.04 Å**까지 올라가므로 살짝 낙관적이다.
- ★ **정직하게 읽으면 "탈착"이 아니라 "≈1.9 Å 들뜬 뒤 정지"다.** 10 ps 안에 PTFE 장쇄가 표면을 떠나지 않는다.
  주장으로 남는 것은 **"PC가 있으면 그 1.9 Å 들뜸조차 일어나지 않는다"** 이고, 그건 그림이 실제로 지지한다.

### 4.8 MD의 부가 관찰 (정성)

- **PC 골격은 붕괴/분해하지 않는다.** 저자 해석: 흡착 Na가 표면 O층 위를 **이동(migration)** 하면서 구조 응력을 완화 (Movies S1–S3).
  → ★ 이건 우리에게 흥미롭다: **앵커가 "고정 못"이 아니라 "미끄러지는 못"** 이라는 뜻이고, 그게 오히려 파괴를 막는다는 논리다. 정량 없음(이동거리·hop 횟수 미보고).
- **PC_1Na의 자유 Na가 떨어져 나온 PTFE의 F를 포획**한다 (Fig S16c,d 빨간 화살표). 그 상호작용에너지가 −0.35 eV.
  → 다수의 Na–F가 생기면 하중이 결합망 전체로 분산되어 파단에 필요한 총에너지가 커진다 — **순수 정성 논변**(네트워크 모델·계산 없음).

### 4.9 인용 오배정 (SI 참고문헌)

SI 계산 절의 각주가 **한 칸씩 밀려 있다**:

| 본문이 붙인 각주 | 실제 [n]의 정체 | 판정 |
|---|---|---|
| Matlantis software **[10]** | Chakraborty, Kunnikuruvan, Dixit, Major, *Isr. J. Chem.* 2020, 60, 850 (NMC 양극 DFT 논문) | ❌ Matlantis 아님 |
| Co/Ni √3 배열 **[11]** | Larsen et al., *J. Phys.: Condens. Matter* 2017, **29, 273002** = **ASE 논문** | ❌ |
| ASE library **[12]** | Connor et al., *J. Power Sources* 2022, 546, 231972 | ❌ ASE 아님 |
| PFP **[9]** | Takamoto et al., *Nat. Commun.* 2022, **13**, 2991 | ✅ 정확 |

→ 정합적 재구성: **√3 배열의 출처는 [10] Chakraborty(NMC DFT)**, **ASE는 [11] Larsen** 이다. Matlantis 인용은 애초에 없다.
소프트웨어 재현성 관점에서 실질적 손해는 없지만, **계산 절이 교정을 안 받은 신호**로 읽어야 한다 (§10 전반의 근거).

---

### 4.10 ★★★ Supporting Movies S1–S3 — 실물 판독 + 픽셀 궤적 재측정 (— 보강 2026-09-03)

2판까지 이 3편은 **인용만 되고 열린 적이 없었다.**  §4.8 이 *"흡착 Na 가 표면 O 층 위를 이동(migration)"* 을
**Movies S1–S3 을 근거로** 적어 놓고 *"정량 없음(이동거리·hop 횟수 미보고)"* 이라고 닫아 두었는데,
그 정량은 **논문이 안 준 게 아니라 우리가 안 본 매체 안에 있었다.**  이번에 셋 다 전수로 열었다.

**사양** (3편 동일): `H.264 960×720`, **14.04 s @ 24 fps = 337 프레임**, 오디오 없음.
캡션(SI p.55) — S1 `PTFE on the NMC surface after running MD simulations at 400 K for 10 ps` ·
S2 `PC_2Na with PTFE …` · S3 `PC_1Na with PTFE …`.
⇒ **§4.7 의 MD 3계와 1:1 대응**하고, **337 프레임 = 10 ps** 이므로 **1 프레임 ≈ 0.0297 ps**.

#### A. 무엇을 보여주나 (한 줄)

**공정 영상이 아니다.**  압연·조립·in-situ 관찰이 **전혀 아니고**, 셋 다 **§4.7 MD 궤적의 3D 렌더 애니메이션**이다
(고정 카메라, 회전 없음).  ⇒ 우리 DEM/MPM 압밀의 실시간 대조군으로는 **쓸 수 없다** (그 층위의 영상은 이 논문에 없다).
대신 **Fig 4d–f 의 원자료**이므로, Fig 4f 곡선을 **다른 매체에서 독립 검증**하는 데 쓸 수 있다 — 그것을 했다.

| 영상 | 계 | 화면에 보이는 것 |
|---|---|---|
| **S1** | PTFE 장쇄 only | 흰 NMC 슬래브 위에 U자로 감긴 PTFE 장쇄 1개.  **사슬이 진한색/옅은색 2구간으로 칠해져 있다** (진한 갈색 C + 진한 파랑 F = 바닥에 닿은 중앙 구간 / 옅은 갈색·옅은 파랑 = 위로 뻗은 양 팔).  시간이 가면 중앙 구간이 **왼쪽부터 들려 기울어진다** |
| **S2** | PC_2Na + PTFE | 위 + PC 분자(갈색 C·빨강 O·연분홍 H) + **노란 Na 구 2개**.  Na 2개가 슬래브 표면에 앉아 있고 그 위·옆을 PTFE 가 지난다.  PTFE 중앙 구간이 **끝까지 표면에 붙어 있다** |
| **S3** | PC_1Na + PTFE | 위와 같으나 **Na 2개가 확연히 분리**: 하나는 표면에, 하나는 **공중에 떠서 카복실레이트 O 에만 배위**.  PTFE 는 표면에 깔려 있고 **양쪽 Na 모두 파란 F 원자와 접촉**한다 |

#### B. ★ Fig 4f 의 독립 재현 (픽셀 궤적)

카메라가 고정임을 먼저 확인했다 — **흰 슬래브 픽셀 수가 전 구간 ±1 % 이내로 일정**(S1 47,583–48,112).
따라서 프레임 간 픽셀 좌표 비교가 성립한다.  그 위에서 **진한 파랑 F 마스크의 중심 y** 를 337 프레임 전부에서 뽑았다.
★ 이 마스크는 우연이 아니라 **저자가 Fig 4f 평균에 넣은 바로 그 부분집합**이다 (Fig 4/S16 캡션:
*"The C and F atoms in **dark brown and blue** … are **only considered** for the average distance calculation"*).
2판 §10.1-③ 이 *"선택 규칙이 미기재"* 라고 적은 그 선택이, 영상에서는 **눈으로 보인다** — 사슬 중앙의 접촉 구간이다.

| 계 | 최대 들뜸 | **최대 시점** | 최종(9.5–10 ps) | 궤적 모양 |
|---|---|---|---|---|
| **S1 PTFE only** | **24.3 px** | **t = 8.48 ps** | **22.1 px** | 0→5.5 ps 단조 상승 → 6–8 ps 고원(≈20) → **8.5 ps 재상승 피크** → 소폭 하강 |
| **S2 PC_2Na** | 8.9 px | 2.77 ps | **3.3 px** | 추세 없는 요동 |
| **S3 PC_1Na** | 3.3 px | 9.14 ps | **0.6 px** | 사실상 평평 |

★★ **두 가지가 2판의 Fig 4f 디지타이즈와 독립적으로 일치한다:**
1. **피크 시점** — 영상 **8.48 ps** vs 2판이 Fig 4f 곡선에서 읽은 **"8–8.5 ps 에서 ≈6.71 Å"**.
   **서로 다른 매체**(플롯 이미지 vs 3D 렌더)에서 같은 시점이 나왔다 ⇒ 2판의 디지타이즈가 검증됐다.
2. **서열과 크기차** — S1 이 S2 의 **2.7×**, S3 의 **7.4×** (최대 들뜸 기준), 최종값 기준으로는 **6.7× / 37×**.
   즉 **"PC 가 있으면 들뜸이 일어나지 않는다"** 는 논문 주장이 영상 자체에서 재현된다.

**스케일 환산** (⚠ **차용된 스케일이다 — 독립 눈금이 아니다**): 2판의 Fig 4f 디지타이즈(PTFE-only 4.75→6.60 Å,
즉 +1.85 Å)를 S1 의 최종 22.1 px 에 맞추면 **≈11.9 px/Å**.  이 눈금으로 S1 피크 24.3 px = **2.04 Å**,
2판이 곡선에서 읽은 피크 상승분 **1.96 Å** 과 **4 % 차** ⇒ 자기일관.
⇒ **S1 의 들뜸은 ≈2 Å 규모**이고, 이는 2판 §4.7 의 결론 — *"탈착이 아니라 ≈1.9 Å 들뜬 뒤 정지"* — 을 **영상이 확인**한다.
10 ps 동안 사슬이 표면을 **떠나지 않는다**(마지막 프레임에서도 오른쪽 절반이 표면 근처).

⚠ **이 재측정의 한계 (인용 시 반드시 동반)**
- **2D 투영 중심**이다.  논문 지표는 3D 평균거리 → **같은 추정량이 아니다.**  가로 이동·원근이 섞인다.
- **스케일이 차용**됐다(위).  ⇒ **Å 절대값을 이 영상에서 새로 인용하지 말 것**; 쓸 수 있는 것은 **시점·서열·배수**다.
- S2/S3 의 작은 값(3.3 / 0.6 px ≈ 0.3 / 0.05 Å)은 **내 방법의 잡음 바닥**이다.
  실제로 2판은 Fig 4f 에서 S2 가 t=10 ps 에 **살짝 내려간다**(4.83→4.57)고 읽었는데 영상 투영은 **살짝 올라간다**(+3.3 px).
  **부호가 반대**다 — 둘 다 S1 신호의 1/7 이하라 **어느 쪽도 유의하지 않다.**  ⇒ **S2/S3 는 "평평하다" 까지만 말한다.**
- 시드 1개·온도 1점·10 ps 라는 **원 계산의 한계는 그대로**다 (§10.3).  영상은 그 한계를 **보여줄 뿐 고치지 못한다.**

#### C. ★★ 2판이 못 채운 두 칸을 영상이 채운다

**(1) "Na migration" 이 정량화됐다** — §4.8 의 *"정량 없음"* 해소.
노란(Na) 마스크의 중심을 337 프레임 추적:

- **S2 (PC_2Na)**: 10 ps 동안 **가로 −65.2 px 이동, 세로 +3.7 px**.
  위 눈금으로 **≈5.5 Å 가로 활주 / ≈0.3 Å 세로 변화**.
- **S3 (PC_1Na)**: 두 Na 가 **337/337 프레임 전부에서 분리 판별**된다.
  표면 Na 가로 범위 475–533 px(**58 px ≈ 4.9 Å**), 세로 순변화 **−3.8 px (≈0.3 Å)**.

⇒ **표면 흡착 Na 는 "가로로 ~5 Å 미끄러지되 세로로는 거의 안 움직인다"** = **탈착 없는 표면 활주**.
이것이 저자가 *"Na 이동이 구조 응력을 완화한다"* 로 서술한 현상의 실체이고,
2판 §4.8 이 붙인 해석 — **"앵커가 고정 못이 아니라 *미끄러지는 못*"** — 에 **크기(≈5 Å)** 가 붙었다.
⚠ **인과는 아니다**: 영상은 "미끄러진다" 를 보여줄 뿐, 그 미끄러짐이 *응력을 완화한다*는 저자의 인과 주장은
여전히 **정성 논변**이다(에너지·응력 시계열이 계산에 없다, §6.1).
⚠ S2 는 두 Na 가 투영에서 **275/337 프레임 겹쳐 보이고** 노란 픽셀 수가 996–1,755 로 ±25 % 흔들린다(가림) ⇒
S2 의 −65 px 는 **가림이 섞인 상한**이다.  S3 는 항상 분리되므로 **S3 의 58 px 쪽이 더 믿을 만하다.**

**(2) PC_1Na 의 "자유 Na" 가 눈으로 확인됐다** — §4.5 의 핵심 주장이 **문장 근거에서 영상 근거로 승격**.

2판은 *"라벨 2Na/1Na/0Na 는 조성이 아니라 **표면에 접촉한 Na 수**"* 를 본문 문장
(*"The **free Na site** in the PC_1Na system…"*)과 Fig S15 정지화면만으로 확정했다.  영상은 이것을 **전 구간** 보여준다:

- S3 에서 **Na 는 처음부터 끝까지 2개**다 (조성은 PC_2Na 와 동일 = 15배열 전부 Na 2개라는 §4.5 확정과 정합).
- 자유 Na ↔ 표면 Na 의 **수직 간격 = 64.4 ± 5.1 px (≈5.4 Å), 337 프레임 내내 한 번도 안 닫힌다.**
  ⇒ **자유 Na 는 10 ps 안에 표면에 내려앉지 않는다.**  "1Na" 는 **동역학적으로도 안정한 상태**이지 초기배치의 우연이 아니다.
- 그 자유 Na 는 **파란 F 원자와 접촉**한 채로 있다 — Fig S16c,d 의 빨간 화살표(자유 Na 가 PTFE 의 F 를 포획, E = −0.35 eV)가
  가리키는 장면이 **정지화면이 아니라 지속 상태**임을 확인.  ★ 즉 **rope 계류의 시각적 증거는 실재한다**
  (⚠ 그 결합의 *성격*은 여전히 미측정 — 전하분석 0, §6.1; XPS 근거에는 §10.2 의 반론이 그대로 유효).

#### D. 영상이 **닫지 못한** 칸 (정직하게)

- **슬래브 종단·TM 배열 여전히 불명** (§4.3 의 공백 유지).  영상에서 **NMC 슬래브 원자가 전부 같은 흰색**으로
  렌더돼 Li/Ni/Mn/Co/O 를 구분할 수 없다.  Fig S15 색 범례에 Li·Co 가 없던 문제가 **영상에서도 그대로**다.
  ⇒ *"fully lithiated 인데 표면 Li 가 어디 있나"* 는 **미해결**.
- 슬래브 측면이 얇게(수 원자층) 보이는 것은 2판의 *"O–TM–O 트라이레이어 1–2겹"* 읽기와 모순되지 않으나,
  **원근 때문에 층수를 셀 수 없다** → 확정하지 않는다.
- **PC_0Na + PTFE 영상은 없다** (애초에 그 MD 를 안 돌렸다, §4.7).  사다리 하단은 **영상으로도 비어 있다.**
- 온도 승온 구간·초기 4.2 Å 문제(§10.1-④)는 **영상도 t=0 부터 시작**해서 해소하지 못한다.
  (영상 t=0 의 F-중심이 이후 최저점이므로, 본문의 "초기 4.2 Å" 이 어디서 왔는지는 **여전히 불명**.)

---

## 5. Figure set ★

크로핑 42장: `litdb/figures/kang2025_bollard_anchored_binder_dry_electrode/` (본문 5 + SI 33 + 표 4).
**Fig 3은 자동 bbox 탐지가 실패해 수동 렌더**(`fig_3.png`, figures.json에 `note` 로 표시).

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a–f | 3-바인더 모식: PVdF **sheet-like**(파란 필름이 면을 덮고 두꺼운 목을 만든다) / PTFE **fibril bridge**(분홍 실이 입자를 감고 건너간다, 고정점 없음) / PC_PTFE **bollard-anchored**(청록 계선주 스터드가 표면에 점점이 박히고 그 밑동에 분홍 로프가 감겨 입자 사이로 팽팽히 건너간다) | ★ bollard = **표면 앵커된 불연속 패치 + 입자간 fibril 스팬** = 우리 SDCP `particle`+`surface_frac` 시딩 그림과 동형 (conformal 필름 아님) |
| 1g,h | FE-SEM+EDS: (g) PTFE 전극 Ni/Mn/Co/F 맵 / (h) PC_PTFE 전극 Ni/Mn/F/**Na** 맵 — **Na(파랑)가 입자 전면을 균일하게 덮는다**, F(주황)는 상대적으로 옅고 얼룩 | 앵커 분산 실측 증거. ⚠ (h)에서 Co 맵을 Na로 갈아끼워 g/h가 같은 세트가 아니다 |
| 2a–i | 로딩 15–30 mg/cm² × wet/dry C-rate + **혼합법별 STD** | ★ **분산 불균일 → 용량 산포** 정량 = 우리 A5 dispersion-CV 실험앵커 (11.37→16.52→5.59→4.28) |
| 3a–f | 바인더 5종 물성 6종 (σ_ion / 시트저항 / σ_e / swelling / E / strain). b는 막대가 아니라 **범위 박스** | §3a 표. ★ **σ_ion 1위는 PVdF(255)** — PC 우위 주장 시 기준 명시 필수 |
| 3g | 5축 레이더 (Ionic conductivity / Flexibility / Electrical conductivity / Swelling ratio / Strain) — PC_PTFE가 면적 최대 | ⚠ **정규화 규칙 미기재**, swelling은 낮을수록 좋은데 축 방향 불명 → 정성 그림으로만 |
| 3h | 바인더별 반쪽셀 rate | ★ **0.1–1C에서는 5종이 ±5 mAh/g 안에 다 몰려 있고, 차이는 2C에서만 벌어진다**(PC 149 vs PAA 130) — 18 mg/cm²에서 바인더는 고율에서만 변수 |
| 3i | **PAA:CMC 비 스윕** (x축 = CMC/PC, 0.1–0.8) | 2C가 **CMC/PC = 0.5에서 최대(≈149)**, 0.6부터 급락(122→103) = PC55 채택 근거. 비단조 절벽 |
| 3j | **PC:PTFE 비 스윕** (x축 = PTFE/(PC_PTFE), 0.1–0.9) | ★ **2C 용량이 사실상 평평하다**(≈138–148, 추세 없음). 73(0.3, 148.3)과 91(0.1, 147.9)의 차이는 **0.4 mAh/g = 노이즈** → **73 선택의 실제 근거는 용량이 아니라 dough 성형성**(Fig S10) |
| 4a,b | FTIR(PAA 1710 / CMC 1590·1021 / PC에 양쪽 보존) + PC 축합 모식 (노란 Na 구가 −COO⁻에 붙어 있다) | PC의 화학 정체성 + **Na가 처음부터 분자의 일부**임을 보여주는 그림 |
| **4c** | **흡착에너지 박스플롯** 4군 + 각 군의 대표 구조 삽화 | ★ 사다리 −2.24 / −1.12 / −0.37 / −0.09 eV. **⚠ y축 라벨 `kJ mol⁻¹` 은 오류 — 실제 단위는 eV** (§10.1-①) |
| 4d,e | MD 400 K 후 스냅샷: (d) PTFE 장쇄만 — 표면에서 **9 Å** 뜸 / (e) PC_2Na 동반 — **3 Å**, 노란 Na 2개가 표면에 앉고 PTFE가 그 위를 지난다 | ★ 우리 single-point E_bind에 없는 **동역학 hold-test**. 사슬은 2색으로 칠해져 있고 **진한 색만 거리평균에 들어간다** |
| **4f** | 표면거리 시계열 3곡선, y 4.0–7.0 Å / x 0–10 ps | ★ 디지타이즈 결과 §4.7. **본문 "초기 4.2 Å"이 그림에 없다**(t=0 ≈4.75) |
| 5a–d | GCD 0.1C/2C + rate + 100 cyc (83 / 51 / 47 %) | binder cohesion ↔ 수명 실험앵커 |
| 5e,f | Nyquist + R_ct (39.01→48.08 vs 68.65→91.52 Ω) | 열화 시그니처(R_ct 성장률) — binder-망 붕괴 척도 |
| 5g–i | 90 mg/cm² 15.6 mAh/cm² + 50 cyc + 선행 DBE 대비 | 고로딩 한계치 (⚠ Table S1은 15.3) |
| S6 | PC_PTFE / PTFE 180° peel 곡선 | 0.9615 vs 0.5733 N/cm |
| S10 | PC_PTFE91 전극 사진 — **dough가 안 뭉쳐 갈라진 상태** | ★ PTFE 0.2 wt%에서 fibrillation 실패의 **직접 증거** |
| S13 | **DFT(Gaussian16) 계산 IR** 3종 (PAA/CMC/PC), scale 0.945 | 계산 1710 / **1527** / **1043** vs 실험 1710 / 1590 / 1021 → §4.2 |
| S14 | NMC622 단독 vs PC 볼밀 후 EDS (Ni/Mn/Co/O vs Ni/Mn/Co/**Na**) | PC가 입자 표면에 균일 부착 |
| **S15** | ★★ **15개 최적화 구조 + 개별 E_ads 전부** — (a) 2Na 8개, (b) 1Na 3개, (c) 0Na 4개 | **이 논문 계산의 원자료.** class 크기·스프레드·사후분류 판정의 근거 (§4.4). 캡션은 "14 different"라 적혀 있으나 **실제 15개** |
| **S16** | MD **초기** 스냅샷 (a) PTFE (b) PC_2Na+PTFE (c) PC_1Na+PTFE + **(d) PC_1Na 최종**. 빨간 화살표 = 자유 Na가 F를 잡은 지점 | ★ **before/after 쌍이 존재하는 것은 PC_1Na(c→d) 뿐**. PTFE-only·PC_2Na의 "after"는 Fig 4d,e에만 있다 |
| **S17** | XPS 필름: (a) PTFE F1s — C–F 단일피크 ≈688.9 / (b) PC_PTFE73 F1s — **Na–F ≈692가 지배** + C–F ≈689 / (c) PC Na1s — Na–COO⁻ ≈1070.8 단일 / (d) PC_PTFE73 Na1s — **Na–F ≈1073.5 지배** + Na–COO⁻, **잡음·기울어진 배경** | ★ 저자의 앵커 실험증거. **⚠ 배정 의심 — §10.2에서 반론** |
| S18 | 단면 SEM + F(청록)/Al(녹색) EDS: PVdF / PTFE / PC_PTFE73 | (a) PVdF는 **선행논문[21] 재사용** 이미지 |
| S19 | PVdF 고로딩 전극의 기계적 균열·집전체 박리 | 습식 고로딩의 실패 모드 |
| S20 | XRM 3D 토모: NMC만 보이고 카본·바인더는 투명(청록 = 카본+바인더) | ⚠ **porosity를 여기서 뽑은 게 아니다**(§6.3) |
| S21 | 100 cyc 후 FE-SEM: (a) PC_PTFE73 매끈 / (b) PTFE — **흰 원 안 NMC 2차입자 파쇄** | ★ binder cohesion ↔ AM 파괴 억제 (정성) |
| S23 | CV(초기 패시베이션 후 5.0 V까지 안정) + LSV | 고전압 대응 주장 |
| S25 | D_Li⁺ (5.09e-14 vs 2.53e-15 m²/s) | 20× |
| S28 | 100 cyc CEI XPS (C1s/O1s/F1s, 깊이 프로파일) | LiF 29.8 vs 37.4 % |
| S37, S38 | 10 cm × 8 cm 시트 · 대면적 시트 사진 | 스케일업 시연 |
| **Table S1** | 선행 **DBE** 고로딩 대비 표 (16행) | this work 5.28/5.0/4.8/4.0 mAh cm⁻² · 651/622/592/492 Wh kg⁻¹ |
| **Table S2** | 선행 **습식** 고로딩 대비 표 (7행) + 산정식 | ⚠ Wh/kg = 비용량 × 3.7 V (**활물질 기준**, 셀 기준 아님) |
| **Table S3** | ★ **porosity 원자료** — 9개 로딩 × 3 바인더 + tap density 5종 | 25.90 / 19.47 / 17.68 %. **계산식 기반**(§6.3) |
| **Table S4** | 코인셀 부품 상세 (양극 30 mg/cm², 3.0 g/cm³, 0.95 cm², 100 μm; 흑연 20 mg/cm², 1.4 g/cm³, 140 μm; 분리막 25 μm 0.02117 g; 케이스 3.52515 g) | 셀-레벨 Wh/kg 재계산이 필요하면 여기 값으로 |

**내가 실제로 본 그림 / 안 본 그림**은 §11에 정리.

---

## 6. Post-processing ★

### 6.1 계산 쪽
- **후처리라 할 것이 거의 없다.** 산출물은 (i) 완화 후 총에너지 차 = E_ads, (ii) MD 궤적의 원자-표면 거리 시계열, 두 가지뿐.
- **없는 것**: Bader/전하분석 0, DOS/PDOS 0, COHP 0, ELF 0, NEB/장벽 0, 진동 열역학(ZPE·엔트로피) 0, 자유에너지 0, RDF/배위수 0, MSD/확산 0, 결합수명 통계 0.
  → **결합의 성격(이온성/공유성)에 대한 직접 증거는 이 논문에 없다.** "이온성"은 **Na–O 거리와 E_ads 크기로부터의 해석**이고, 전하분석으로 뒷받침되지 않았다.
- **도구**: ASE(구조·최적화·MD 구동) + Matlantis API(PFP 호출). pymatgen/VESTA/LOBSTER 등 언급 0. 시각화 도구 미기재.
- **수치화 방식**: class별 **산술평균 1개 숫자**로 압축 → Fig 4c 박스플롯으로만 분포를 보여줌. **표로 된 수치 목록이 없다**(개별값은 Fig S15 그림 안 텍스트로만 존재).
  → ★ 재현·재분석을 하려면 **그림에서 숫자를 읽어내야 한다**. 우리가 이번에 한 게 정확히 그것이다.

### 6.2 실험 쪽
- **XPS 디컨볼루션**: PC 정체성(C1s 284.1 C–C / 285.7 C–O / 287.2 COO⁻ / 288.1 COOH = 에스터 형성, Fig S11) + **계면 Na–F**(Note S3, Fig S17) + **CEI 조성·깊이 프로파일**(10/20/30 s 스퍼터; LiF 685.0 vs Li_xPO_yF_z 687 eV).
- **FTIR + 계산 IR 대조**: 실험 피크 배정을 Gaussian16 IR로 교차검증 (§4.2).
- **XRM(3D X-ray 토모, Xradia 810 Ultra)**: FOV **18×18×18 μm³**, 화소 **128 nm**. 카본·바인더는 X선 투명 → NMC 입자만 가시. 분산 균일성 확인용.
- **tortuosity**: 단면 SEM 이미지 기반 계산 (알고리즘·소프트웨어 미기재). τ = 1.30 / 1.40 — **τ이지 τ² 아님**.
- **기계**: UTM 인장(필름 E·strain) + **180° peel-off**(전극↔Al) — binder cohesion의 시스템-레벨 수치화.
- **전기화학**: 4-probe 시트저항→σ_e; 필름 EIS→σ_ion; 반쪽셀 EIS 반원→R_ct(ZMAN 피팅); D_Li⁺(Warburg); radar chart(5축).

### 6.3 ★ porosity는 "측정"이 아니라 "계산"이다 (Table S3 정독 결과)

Table S3의 식:
`ε = 1 − (m_areal / L) × Σ_i (w_i / ρ_i)`, i ∈ {NMC, Super P, binder}, ρ = **tap density**.

- 입력 tap density: NMC **4.86**, Super P **1.60**, **PC_PTFE73 1.17**, **PTFE 0.52**, **PVdF 0.45** g/cm³.
- 세 전극의 밀도(3.0 g/cm³)와 조성(93:5:2)이 **모두 같으므로**, ε 차이는 **binder tap density 하나로 전부 결정된다.**
  PC_PTFE73(1.17) vs PTFE(0.52) vs PVdF(0.45) → 25.90 / 19.47 / 17.68 %.
- **PC_PTFE73 행이 로딩 0.015→0.100 g/cm²에서 25.15–25.90 %로 사실상 상수**인 것도 같은 이유다. 조성·밀도가 고정이니 **로딩 축은 정보가 없다.**
- ⚠ **재계산 검증**: 명시된 입력으로 내가 다시 계산하면 28.1 / 21.7 / 19.9 % 가 나와 **일률적으로 +2.2 %p 어긋난다.**
  다만 **차이는 정확히 재현된다**(PC−PVdF: 내 계산 8.2 %p vs 표 8.22 %p) → 공유 성분(NMC 또는 Super P) 밀도를 표에 적힌 것과 다른 값으로 썼을 가능성이 크다.
  **결론: 순위와 격차는 신뢰, 절대값은 신뢰하지 말 것.**
- ★ 그래서 "PC_PTFE73이 다공성이 높다"는 **가정된 tap density의 귀결**이지 독립 측정(수은/가스 흡착/토모 세그먼테이션)이 아니다.
  XRM이 있는데도 거기서 porosity를 안 뽑았다 — 카본·바인더가 투명해서 못 뽑는다.

---

## 7. 우리 대비 (SDCP / DEM+MPM) → `our_dem_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **앵커링 개념** ★ | **bollard hitch**: PC의 **Na⁺ 짝이온이 표면 O에 브리지**(−2.24 eV) = 계선주; PTFE fibril이 **Na–F**(−0.35 eV) + PAA 가지 얽힘으로 계류 | **SDCP**: 술폰산 −SO₃⁻가 NCM **Li-O층 삽입형** 화학흡착, E_bind **−4.797 eV**(doped, uma-s-1p1) / −3.02(neutral) · O–Li 1.83 Å×2 · γ≈0.93 J/m² | **같은 개념-클래스** — CAM 산화물 표면의 *이온성* 화학흡착이 PTFE vdW-only(−0.09)를 대체. 차이: 그들 **양이온(Na⁺) 표면 브리지 / 표면 위 흡착** vs 우리 **음이온기 격자 삽입**. 결합 자리가 다르다 |
| **계산 층위** ★신규 | **PFP v3.0.0 (범용 NNP)** — DFT 아님 | **uma-s-1p1 (범용 MLIP)** | **층위가 같다.** 그래서 "그들 DFT vs 우리 MLIP" 프레이밍은 틀렸다. 둘 다 범용 NNP. 단 **학습셋·표면·fragment가 전부 달라 절대값 비교는 여전히 금지** |
| 이온성≫극성≫vdW 사다리 | −2.24 ≫ −1.12 ≫ −0.37 ≫ −0.09 eV (25× 스팬) | doped −4.8 > neutral −3.0 (≫ PTFE) | **방향 독립 재현.** "하전/이온 채널이 중성 극성 채널을 지배"를 다른 계·다른 NNP가 확인. **서열만 전이, 절대값 ⛔** |
| **음이온기의 중성화 처리** ★★ | −COO⁻ 2개 + **Na⁺ 2개 = 중성 fragment**. 15배열 전부 동일 조성 | −SO₃⁻ 처리 방식이 캠페인 현안 | ★ **직접 이식 대상.** 단 §4.5의 함정 ①②(짝이온이 결합자리가 되어 estimand가 바뀜 / 초기배치가 상태선택) 를 estimand 카드에 먼저 적고 갈 것 |
| **상태 집계 규칙** ★ | 15배열 → **사후 3분류 → class 평균** (8/3/4) | 우리 규율: 집계 규칙을 결과 전에 선언 | ⛔ **그들 방식은 우리 규율 위반.** 반면교사. 그들 결론(사다리)은 견고하나 **숫자는 estimand가 아니다** |
| 아키텍처 | **이중-바인더**: 절연 bollard(PC 1.4 wt%) + **PTFE rope 유지(0.6 wt%)** | **단일 도전바인더**: SDCP가 앵커+전자전도 겸업, PTFE-free 지향 | 그들은 fibrillation 공정 유지가 목표 → PTFE 최소화. ★ 그들 데이터 = "**anchored+rope 하이브리드 > rope-only**"(동일 총바인더) → 우리 비교셋에 **SDCP+PTFE 소량** 추가 근거 |
| σ_e 이득의 기원 | PC_PTFE 1.30 S/cm 최고 — 그러나 **분산·3D망 효과**(PC 자체는 절연 이오노머) | SDCP는 **재료 자체가 도전**(self-doped S-PEDOT) | 다른 채널. 그들 σ_e↑는 우리 **A5 dispersion** 축의 증거이지 SDCP 전도축과 혼동 금지 |
| binder σ_ion | 필름: PTFE 4.88e-6 → PC_PTFE 1.31e-4 S/cm (**27×**). ⚠ **PVdF가 2.55e-4로 1위** | W2 whatif: PTFE σ_ion **×0.74** 고정 페널티(바인더 무관) | 우리 페널티를 **바인더별 입력**으로 세분할 근거. 단 그들 값은 **액체전해질 팽윤 필름** — ASSB SE-neck 차단과 물리가 다르다. 비율 방향만 |
| binder cohesion 실험앵커 | peel **0.9615 vs 0.5733 N/cm (1.68×)**; R_ct 성장 39→48 vs 69→92 Ω; **AM 2차입자 파쇄 유무** | A3 `binder_cap`(PTFE, 비단조) + SDCP coh ≈ **10× coh_ptfe**(γ-비 anchor) | ★ 계층 정합: 계면(그들 E_ads비 25× / 우리 γ비 ~10×) ≫ 시스템(peel 1.68×). peel은 소성산일+테이프 포함이고 두 계가 **PTFE web을 공유**해 희석된다. **peel(N/cm ≈ J/m², 96/57)을 γ(0.93 J/m²)와 동일시 ⛔** — 비율만 |
| PTFE fibrillation 하한 | **0.6 wt%**(bollard 지원 시 dough 성립), **0.2 wt% 실패**, 단독 **2 wt%**; 과잉 fibrillation 역효과 | `--ptfe-fibril` ∈ (0,1] morphology knob (magnitude 미앵커) | ★ 우리 fibril-web 성립 하한의 **첫 실험앵커 후보**. LIB 건식이지만 fibrillation 자체는 공정물리 공통(Lee2025 / Liu2025 / Mun2025 계열) |
| 혼합(전단) | ball mill ×3 > planetary ×1 (용량↑ · STD 16.52→4.28) | ADDITIVE_PROCESS 3×3 (ballmill/thinky/handmix) — 방향만 | ★ **분산도→성능산포** 정량 = A5 dispersion-CV 실험앵커 |
| porosity/τ | 25.90 / 19.47 / 17.68 %(⚠ tap density 계산), τ 1.30 / 1.40; **높은 porosity = 장점** | 우리 ASSB: porosity = 죽은 공간(σ_ionic↓); real_14 15.6 % | ⚠ **이온위상 역전**(LIB pore=전도체 / ASSB SE망=전도체). "binder가 porosity 올려서 좋다"는 **전이 ⛔**. 숫자는 binder-종속 porosity 변화 사례로만 |
| 시뮬 스케일 | **분자만**(NNP 흡착 + 10 ps MD) | DEM(전달) + MPM(역학) + additives 시딩 | 상보. 그들 방법론(15-배향 샘플링 · 400 K hold-test)은 이식 가치, 우리 입자스케일은 그들이 비운 칸 |
| AM 균열 | 사이클 후 PTFE계 NMC 2차입자 파쇄 vs PC_PTFE73 무균열 | Auerbach 압밀-접촉응력 파괴(A9); 사이클-버전 미보유(A10) | driver 다름(사이클 응력 vs 압밀 접촉응력). binder-cohesion↔AM-fracture 결합은 우리 fracture 모델에 없는 축 |


### 7b. — 보강 2026-09-03: 3판이 추가한 우리-대비 4줄

| 항목 | 이 논문 | 우리 | 판정 / 왜 |
|---|---|---|---|
| **접촉저항 앵커 (CL-38)** ★ | ⛔ **없다.**  가장 가까운 값은 반쪽셀 EIS 반원 *"interfacial resistance"* **39.01 Ω**(PC_PTFE73) / **68.65 Ω**(PTFE) @10 cyc — 그러나 이것은 **R_ct(전하이동) 계열**이고, 게다가 **액체전해질 반쪽셀 전체**의 값이라 면적·전극 두 개·CEI 가 다 섞여 있다 | CL-38: 복셀 솔버가 **접촉저항을 0** 으로 두어 σ_e 가 실측 TLM 대비 **~440×** 높다는 판정 | ⛔ **제3자 근거로 쓸 수 없다.**  세 층위가 전부 어긋난다 — (i) **양이 다르다**(R_ct ≠ 입자접촉 협착저항), (ii) **계가 다르다**(액체전해질 LIB ≠ 우리 황화물 ASSB), (iii) **분해가 없다**(TLM 처럼 전자/이온/접촉을 나누지 않은 단일 반원).  ⇒ CL-38 의 440× 는 **여전히 TLM 문헌으로만** 앵커해야 한다.  이 논문은 그 칸을 **못 채운다** |
| **압밀 규약** ★ 신규 | **압력이 아니라 밀도로 정지**한다 — 열간 롤(145/130 °C, 120 cm/min)을 **3.0 g/cm³ 에 닿을 때까지 반복 통과**.  성형압 수치 0 | MPM `--protocol servo`(정압) vs **`hold`**(변위/밀도 정지); DEM 은 300 MPa 정압 | ★ **산업 건식라인의 실제 규약이 `hold` 쪽이다** = 우리 `hold` 분기가 인위적 선택이 아님을 보이는 문헌 근거.  ⚠ 동시에 **경고**이기도 하다 — CLAUDE.md 플래튼 트랙이 확정했듯 `hold` 에서 **porosity 는 정지 프레임의 함수**다.  이 논문의 porosity(§6.3)가 *측정이 아니라 밀도에서 역산한 계산값*인 것은 같은 구조의 귀결이다.  ⇒ **"둘 다 정지규약이 값을 정한다"** 는 공통 취약점이지, 상호 검증이 아니다 |
| **σ_e ↔ porosity 부호** ★ 신규 | 저자 귀속: *"higher porosity and lower tortuosity"* 때문에 **electrical conductivity 가 높다** (본문 §2.4 결론문) | Stage 22.5 σ_e 폼의 **`φ_AM⁴`** (Stauffer-Bruggeman, n=76 코퍼스에서 지수 4 가 **정확히** 선택됨; 3.5→ΔLOOCV −0.007, 4.5→−0.027) | ⛔ **부호가 반대다.**  공극이 늘면 φ_AM 이 줄고 σ_e 는 **4제곱으로 급감**한다.  이 논문 자신도 앞 문단에서는 σ_e 상승을 **분산·3D 망**으로 설명해 놓고(그쪽이 옳다), 결론문에서 porosity 로 갈아탄다 — **내부 논지 충돌** (§10.5).  ⇒ **"다공성이 σ_e 를 올린다" 를 이 논문 근거로 인용 금지**; 인용할 것은 **분산 개선** 쪽 |
| **MD hold-test 이식 사양** ★ 갱신 | 영상 판독으로 원 계산의 해상도가 확정: **337 프레임 = 10 ps**, 1 시드, 400 K 1점, 부분집합 평균 | §8-③ 이 제안한 이식 사양(≥50 ps · 3 시드 · 2 온도 · 전-원자 평균) | ★ 이식 사양이 **여전히 옳다**, 그리고 이제 **넘어야 할 기준선이 정확히 무엇인지** 안다.  추가로 영상이 알려준 것: 그들의 신호(≈2 Å 들뜸)는 **10 ps 안에 포화**하므로 우리가 50 ps 를 돌리면 *새 현상*(재부착·hop)이 보일 여지가 있다 — 그들이 못 본 구간이다 |

### 🔧 방법 원전으로서의 가치 (물성값 이식과 별개)

> **↔ 대조군 ICEP (Han 2025, *Adv. Mater.* 37, 2506266 — 우리 −SO₃⁻ 와 *같은 작용기*)와의 정면대조는
> `comparison_vs_ours_DEM.md` 의 "Kang(bollard) vs Han(ICEP) 정면대조" 블록에 있다** (정리본
> `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md`).
> 요지: 같은 문제(음이온성 산성기를 중성계에서 다루기)를 **Kang은 짝이온 Na⁺ 투입**으로, **ICEP는 양성자를
> 슬랩으로 이전(`(−H)`)** 으로 풀었다. **Kang만 그 상태를 이름 붙여(`PC_2Na/1Na/0Na`) 본문에서 논했고**,
> ICEP는 `(−H)`가 그림 라벨에만 있고 본문에 없다(그 선택이 −2.243 vs −1.819 eV = **0.424 eV**를 가른다).
> ⚠ 단 §4.4에서 확정했듯 **Kang의 3분류도 사후 분류**라, 우위는 "명명·논의"까지이고 "사전 선언"은 아니다.
- **짝이온 중성화 레시피** (§4.5) — 우리 SDCP 음이온기 처리의 선례이자 함정 목록.
- **회전 샘플링 → 상태 분포** (§4.4) — 우리가 *반대로* 해야 할 것(집계 규칙 선언 후 실행)의 대조군.
- **400 K NVT hold-test** (§4.7) — single-point E_bind를 보강하는 값싼 동역학 검증(단 10 ps·1시드·1온도는 우리 기준 미달, **최소 3시드 + 2온도**로 올려서 이식).

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **★ 음이온기 중성화 프로토콜 (SDCP 직결)** — −SO₃⁻ 를 MLIP에서 다루려면 짝이온을 넣어 중성화하는 것이 사실상 유일한 길이고, 이 논문이 그 선례다.
  **다만 estimand가 바뀐다**: 측정되는 건 "술폰산–NCM 결합"이 아니라 "짝이온 브리지"일 수 있다.
  → estimand 카드에 `X(짝이온 종·개수·초기배치 정책)` 을 **먼저** 선언하고, 가능하면 **짝이온 없는 대전계 + 보정** 경로와 **둘 다** 계산해 차이를 보고한다.
- ② **SDCP 개념 정당화 인용** — "이온성 표면앵커 바인더로 PTFE 접착·규제 한계를 넘는다"가 *Adv. Mater.* 2025 독립 선례로 존재.
  우리 SDCP의 novelty는 **앵커+전자전도 겸업(단일 도전바인더)** + **입자스케일(MPM/DEM) 매핑**에 있음이 오히려 선명해진다.
- ③ **MD hold-test 이식 (단, 업그레이드해서)** — 우리 E_bind는 single-point. 그들처럼 400 K NVT로 표면거리 시계열을 뽑되,
  그들의 약점(10 ps · 1시드 · 1온도 · 부분집합 평균)을 고쳐서 **≥50 ps, 3시드, 2온도, 전-원자 평균 + 정의 명시**로 돌린다.
  그러면 "앵커가 동역학적으로도 유지된다"를 그들보다 강하게 말할 수 있다 (A4′ 검증 ④와 연결).
- ④ **A5 dispersion-CV 앵커** — 혼합법→용량 STD(11.37 / 16.52 → 5.59 → 4.28 mAh/g). "분산 불균일 → 성능 산포"의 실험 대응물.
- ⑤ **PTFE fibrillation 하한 앵커** — dough 성립 PTFE ≥0.6 wt%(앵커 지원) / 2 wt%(단독) / 0.2 wt% 실패. `--ptfe-fibril` 축의 문헌 하한.
- ⑥ **비교셋에 SDCP+PTFE 콤보** — 그들 최적이 "anchored 7 : rope 3" 하이브리드.
  우리 비교셋(VGCF+PTFE / SDCP-only)에 **SDCP + PTFE 소량**을 추가하면 "앵커가 rope 필요량을 줄인다"를 우리 프레임에서 시험 가능.
  (SDCP–PTFE 결합에너지 = 그들 Na–F −0.35 eV의 대응물 — 우리 미계산, MLIP 후보.)
- ⑦ **A3 cohesion 실험앵커 목록 등록** — peel 1.68× / R_ct 성장률 / 사이클 후 AM 파쇄 유무 (계면 γ와 계층 구분해 사용).
- ⑧ **반면교사 (계산 QC)** — 축 단위 오기, class 크기 미보고, 거리 지표 3중 정의, 인용 한 칸 밀림.
  ★ *Adv. Mater.* 급에서도 **계산 절은 교정을 거의 안 받는다.** 우리 원고의 계산 절은 **축 라벨·n·지표 정의·인용 매핑**을 별도 체크리스트로 돌린다.

## 9. 인용 가능 문장 (deck/paper용)

- "An ionically chemisorbed 'bollard' binder that anchors PTFE fibrils to the cathode-oxide surface (Na-mediated adsorption, −2.24 eV vs −0.09 eV for a vdW-only PTFE dimer; Kang et al., *Adv. Mater.* 2025, 37, 2416872) independently establishes the concept class of surface-anchored binders for dry electrodes — our SDCP extends this class by making the anchor itself electronically conductive and by mapping the anchor energy to a particle-scale interface cohesion."
- "Their molecular-scale ladder (ionic ≫ polar ≫ van der Waals adsorption, spanning ~25×) and their 400 K hold-test provide an independent methodological template for validating anchoring beyond single-point binding energies."
- "A dual-binder architecture in which a surface-anchored ionomer carries the adhesion and a fibrillating fluoropolymer carries only the network reduces PTFE from 2 wt% to 0.6 wt% while enabling 90 mg cm⁻² cathodes."
- ⛔ **쓰면 안 되는 문장**: "DFT calculations show …" (PFP는 DFT가 아니다) / "651 Wh kg⁻¹ cell-level" (활물질 기준이다) / 흡착에너지 절대값을 우리 값과 나란히.

---

## 10. 주의 / 한계 / 비판 (over-claim 방지)

### 10.1 ★ 내부 불일치 6건 (SI 전수 + 그림 실물 판독으로 신규 적발)

| # | 무엇 | 어디 | 판정 |
|---|---|---|---|
| ① | **Fig 4c y축 라벨이 `Adsorption energy (kJ mol⁻¹)`** | Fig 4c | **단위 오기 확정 — 실제는 eV.** 근거: (i) 축 범위 0.5 ~ −2.5가 본문 eV 값과 정확히 일치, (ii) Fig S15의 개별 라벨이 전부 **"eV"**, (iii) kJ/mol이라면 −2.24 kJ/mol = −0.023 eV로, 저자 스스로 "약하다"고 한 PTFE vdW(−0.09 eV)보다도 약해져 논지가 자기모순. **그림에서 값을 읽을 때 eV로 읽으면 된다** |
| ② | **Fig S15 캡션 "14 different stabilized structural configurations"** vs 본문 "**15** different configurations" | S15 캡션 / 본문 p.7 | 그림에 **에너지 라벨이 15개**(8+3+4) 실재 → **본문 15가 맞고 SI 캡션이 오기** |
| ③ | **거리 지표 정의 3중 불일치** | 본문 "**F atoms**" / Fig 4 캡션 "**C and F**" / S16 캡션 "**C and F**" | 캡션 2개가 일치하므로 **C+F가 맞고 본문이 오기**로 보인다. 더 큰 문제는 **"dark brown / blue로 칠해진 부분집합만" 이라는 선택 규칙이 미기재**라는 것 — 그림에서 사슬이 진한색/옅은색 2색이다 |
| ④ | **"초기 4.2 Å"이 Fig 4f에 없다** | 본문 vs Fig 4f | 디지타이즈: t=0 ≈**4.75 Å**(`figure-read`). y축 하한 4.0에 4.2 근처 데이터 없음. 승온 전 기하의 값일 수 있으나 **논문이 구분하지 않음** |
| ⑤ | **90 mg/cm² areal capacity: 본문 15.6 vs Table S1/S2 15.3 mAh/cm²** | 본문 3곳 / Table S1,S2 | 2 % 차. 어느 쪽이 정본인지 불명 → **인용 시 "≈15.3–15.6"** |
| ⑥ | **SI 계산 절 인용이 한 칸 밀림** | SI p.7–8 refs [10][11][12] | ASE의 실제 번호는 [11](Larsen)인데 본문은 [12]를 붙였다 (§4.9) |

추가 소소한 것: `fmax_threshold = 0.01 **eV**`(force 단위 오기) · swelling "ratio" 정의 불일치(§3a) · 초록의 metaphor 역전("PC가 bollard, **PTFE가 anchor**" ↔ 본문은 PC가 앵커).

### 10.2 ★ XPS Na–F 배정에 대한 반론 (저자 주장의 유일한 실험 기둥)

저자 논리: PC_PTFE73에서 F1s에 **691.99 eV** 신규 피크, Na1s에 **1073.5 eV** 신규 피크 → Na–F 화학결합 형성 → bollard–rope 계류의 실험 증거.

**반론 3가지 (전부 §10.1과 독립):**

1. **방향이 반대다.** 이온성 플루오라이드(NaF)의 F1s는 **≈684–685 eV**로, 공유결합 C–F(PTFE ≈689 eV)보다 **낮다**.
   Na⁺와 상호작용해 F가 음전하를 더 얻으면 결합에너지는 **내려가야** 한다. 저자는 **더 높은 692 eV**를 Na–F로 배정하고,
   근거로 *"a reduction in electron density around the F atoms"*(Note S3)를 든다 — Na⁺···F⁻ 이온 상호작용의 물리와 어긋난다.
2. **더 단순한 설명: 차등 대전(differential charging).** F1s의 신규 성분은 C–F 대비 **+2.77 eV**, Na1s의 신규 성분은 Na–COO⁻ 대비 **+3.0 eV** 다.
   **두 원소가 거의 같은 양만큼 밀렸다** — 이는 새 화학종보다 **두 번째 상(PTFE-rich 도메인)이 다르게 대전된** 신호에 훨씬 잘 맞는다.
   절연성 폴리머 필름 XPS의 고전적 인공물이고, 논문은 대전 보정(C1s 284.8 eV 참조 등)이나 flood gun 사용을 **언급하지 않는다**.
3. **화학량론이 안 맞는다.** PC_PTFE73은 PC 70 : PTFE 30 wt%. F는 거의 전부 PTFE(–CF₂–, ≈50 g/mol per CF₂)에서 오므로 F ≈ 1.2 mol/100 g,
   Na는 Na-CMC에서 오므로 대략 0.1–0.2 mol/100 g 규모다. **Na가 F의 1/6 이하**인데 F1s **면적의 다수**가 Na–F로 배정됐다.
   표면 편석으로 부분 설명은 가능하나, 논문은 이 정량 점검을 하지 않는다.
   또한 Fig S17d(Na1s of PC_PTFE73)는 **잡음이 크고 배경이 기울어져** 있어 (c)와 피팅 품질이 눈에 띄게 다르다.

**⇒ 판정**: Na–F 상호작용의 **존재 가능성 자체를 부정할 근거는 없다**(계산도 −0.35 eV를 준다).
하지만 **XPS는 그것의 결정적 증거가 아니다.** 우리 문서에서 인용할 때는 *"XPS shifts were interpreted as Na–F bonding"* 처럼 **저자 해석임을 명시**하고, 우리 주장의 하중을 여기 걸지 않는다.

### 10.3 계산 방법 자체의 한계

- **PFP는 DFT가 아니다** (§4.1). 학습셋·불확실도 미기재 → 분자/산화물 계면이라는 OOD 영역에서의 신뢰도 판단 불가. **벤치마크 0건**(DFT와의 대조 계산이 하나도 없다).
- **fragment 스케일**: CMC monomer / PAA dimer / PC(단량체 graft) / PTFE dimer. 실제 PC는 **Mw 7,107**(≈단량체 30개 규모).
  → **절대 E_ads는 fragment 값**이고, 폴리머 사슬의 다점 결합(avidity)을 담지 못한다. **우리 −4.8 eV와 절대 비교 ⛔, 사다리만.**
- **표면이 하나뿐**: facet 미기재, 종단 불명, **fully lithiated(SOC 0 %)만**. 실제 문제가 되는 **충전상태(delithiated, O 반응성 높음)** 표면은 계산 안 함.
- **무질서 없음**: TM 배열을 **√3 규칙 단일 배열**로 고정. NMC의 실제 TM 무질서·표면 Li/Ni 혼합·표면 재구성 전부 미반영. 배열 앙상블 없음.
- **PC_0Na + PTFE MD를 안 돌렸다** — 사다리 하단(가장 약한 앵커)에서 PTFE가 어떻게 되는지가 정작 비어 있다.
- **PTFE 장쇄의 E_ads가 없다** (§4.6). "PTFE는 −0.09 eV라 약하다"와 "MD에서 장쇄가 안 떨어진다"가 같은 그림에 공존한다.
- **통계 부재**: MD 시드 1개, 온도 1점, 오차막대 0, class 크기 미보고(그림에서 세야 함), PTFE_dimer의 n 불명.
- **후처리 부재** (§6.1): 전하분석 0 → "이온성 결합"은 해석이지 측정이 아니다.

### 10.4 실험·주장 층위

- **LIB 액체전해질** — SE 없음. porosity·swelling·D_Li⁺·CEI는 **이온위상 역전**(pore = 전도체) 아래의 결과 → 우리 ASSB로 **절대 전이 금지**(부호까지 반대로 읽힐 수 있다).
- **porosity는 계산값** (§6.3): 가정한 tap density가 순위를 전부 결정하고, 명시 입력으로 재계산하면 +2.2 %p 어긋난다. **순위·격차만 인용.**
- **필름 E = MPa 스케일**(PTFE 3.50, PC_PTFE 0.15 MPa) — 다공 fibril 시트의 유효값. bulk PTFE ~0.3–0.5 GPa(우리 ADD dict 0.30 GPa)와 **1000× 차이** → MPM 재료입력으로 직접 사용 ⛔, soft-phase 서열/비율만.
- **peel(N/cm) ≠ 계면 γ**: 0.96 N/cm ≈ 96 J/m² 규모는 테이프·소성산일 포함 시스템값. 우리 DFT γ 0.93 J/m²와 **100× 층위 차이**. 비율(1.68×)만 전이.
- **"first PTFE-less binder"는 마케팅** — 실제는 PTFE **감축**(2→0.6 wt%, >70%↓). fibrillation은 여전히 PTFE가 한다(PC는 fibril화 안 함). 키워드 줄은 스스로 "PFAS-**less**"라고 적는다.
- **Fig 3j가 73의 우위를 지지하지 않는다** — 2C 용량이 PTFE 분율 0.1–0.9에서 평평하다(148.3 vs 147.9 = 0.4 mAh/g). **73 선택의 진짜 근거는 dough 성형성**이고, 논문도 그렇게 쓴다. "73이 최적 조성"이라는 요약은 과하다.
- **σ_ion 1위는 PVdF** (§3a) — "PC가 이온전도를 개선한다"는 PTFE-only 대비에서만 참.
- **Wh/kg 산정이 활물질 기준** (Table S2 각주) — 셀 수준 아님. Table S4에 부품 질량이 있으니 필요하면 재계산 가능.
- **Fig S18a(PVdF 단면)는 선행논문 [21] 재사용 이미지** — 캡션에 명시되어 있다. 비교군이 같은 조건에서 새로 찍힌 게 아니다.
- **소속상 현대차 공동연구**(응용 지향) — 선행 DBE 대비 우월 주장(Fig 5i, Table S1)은 자사-우호 셀렉션 가능성 감안.

---


### 10.1b ★ 내부 불일치 — 3판 추가 3건 (누계 9건) (— 보강 2026-09-03)

| # | 무엇 | 어디 | 판정 |
|---|---|---|---|
| ⑦ | **Fig 3b 의 양이 이름 2개 · 단위 1개로 셋 다 안 맞는다** | 본문 p.5–6 *"sheet resistance"* / Fig 3b 축 *"Resistivity (Ω cm⁻²)"* | **시트저항 `R_s` [Ω/□] 이 맞다.**  근거는 역산 자기일관성 — `t = 1/(σ·R_s)` 가 건식 5종에서 **99.3 ± 1.4 µm** 로 수렴하고 Table S4 의 양극 **100 µm** 와 맞는다 (§3e).  ⇒ 값은 **살리고**, 축 라벨과 단위는 **버린다** |
| ⑧ | **σ_ion 의 `L` 에 분리막 두께가 포함**되고 블랭크 차감이 없다 | SI p.6 식 정의 | 보고된 σ_ion 은 **필름 고유값이 아니라 (필름+분리막) 겉보기값** → 전 계열 **상향 편향**.  필름 두께 미기재라 편향 크기 계산 불가.  ⇒ **σ_ion 5값은 상대·겉보기로만** (§3e-나) |
| ⑨ | **Fig S1 의 "장점" 퍼센트가 이 논문 자신의 데이터와 안 맞는다** | SI p.11 Fig S1 (모식도) | 도식에 인용 없는 수치가 7개(**+45 % 용량 · −19 % 제조비 · −38 % 에너지비 · −90 % 임피던스 · +96 % 접착 · −2 % 재료비 · −14 % 설비비**).  검산: 접착은 논문 실측 0.5733→0.9615 N/cm = **+67.7 %**(≠ +96), 임피던스는 68.65→39.01 Ω = **−43.2 %**(≠ −90).  ⇒ **Fig S1 은 이 논문의 측정이 아니라 출처 없는 업계 로드맵 수치**다.  ⛔ **Fig S1 의 어떤 퍼센트도 이 논문 근거로 인용 금지** |

### 10.5 ★ 논지 결함 — "다공성이 전자전도를 올린다" (— 보강 2026-09-03)

본문 §2.4 마지막 문장: *"the PC_PTFE73-based cathode positively influenced electrolyte conductivity,
lithium diffusion coefficient enhancement and **high electrical conductivity due to its higher porosity**
and lower tortuosity."*  그리고 바로 앞: *"Its low tortuosity further shortens the **electron** transport pathways."*

**두 군데가 틀렸다:**
1. **다공성↑ → σ_e↑ 는 부호가 반대다.**  전자는 고체 접촉망으로만 흐른다 — 공극이 늘면 고체분율이 줄어 σ_e 는
   **감소**한다.  우리 Stage 22.5 폼이 **`φ_AM⁴`** 를 쓰고 그 지수 4 가 n=76 코퍼스에서 **정확히** 선택된 것이
   그 정량판이다(§7b).  25.90 % vs 17.68 % 의 공극 차이는 σ_e 를 **올릴** 수 없다.
2. **τ 를 전자 경로에 붙인 것도 자리가 틀렸다.**  이 논문의 τ(1.30 / 1.40)는 **단면 SEM 기반**으로 뽑은 것이고,
   문맥상 **기공(이온) 경로**의 굴곡도다.  전자 굴곡도는 **고체상**에서 따로 정의되는 다른 양이다.

**그런데 이 논문 자신이 앞에서는 옳게 설명한다** — Fig 3c 문단: σ_e 상승은 PC 가
*"maintain a uniform distribution of electrode particles and form a three-dimensional network structure …
increases the **direct contact area** between electrode materials"* 때문이라고 적는다.  **이쪽이 맞다**
(접촉면적↑ = Holm 협착저항↓ = 우리 `√A_AM-AM` 항과 같은 물리).
⇒ **결론문에서 근거를 porosity 로 갈아탄 것이 오류**다.  두 서술이 **같은 논문 안에서 충돌**한다.

**우리 인용 규칙**: σ_e 1.30 S/cm 는 **분산·접촉면적 개선의 증거로만** 인용하고,
*"다공성이 전자전도를 개선한다"* 는 **인용하지 않는다**(우리 폼과 부호가 반대이며 이 논문의 자기 서술과도 충돌).
⚠ 참고로 **이온 쪽은 이 논문이 맞다** — LIB 액체전해질에서는 기공이 전도체이므로 porosity↑ → 이온 유리.
그 위상 역전이 우리 ASSB 로 전이하면 안 된다는 것은 §7 의 기존 경고 그대로다.

## 11. ★ 이번 재digest에서 실제로 본 그림 / 안 본 그림

크로핑 **42장** 중 **실물 판독 8장** (+ 좌표 디지타이즈 1건):

| 본 것 | 왜 골랐나 | 본문과 어긋났나 |
|---|---|---|
| `fig_4.png` (+ 4c·4f 확대) | 축 단위 질문(Q1)의 대상 · 계산 결과 전부 | ✅ **어긋남 2건** — 축 라벨 kJ/mol(①), t=0 4.75 vs 본문 4.2(④) |
| `fig_4.png` 4f **픽셀 디지타이즈** | "4.2 Å"을 눈대중으로 판정하면 안 되므로 | 축 눈금 7단(119/191/264/336/409/481/554 px) 보정 후 3곡선 추출 |
| `fig_S15.png` (+ 라벨행 4개 확대) | Q3 · 계산의 원자료 | ✅ **어긋남 1건** — 캡션 "14" vs 실제 15(②). 평균은 논문값과 일치(검산 통과) |
| `fig_S15.png` 개별 배열 확대 | Na 결합 모티프·슬랩 종단 확인 (Q2) | Na가 **카복실레이트 O 2 + 표면 O 2**에 배위 확인. **Li·Co가 색 범례에 없다** |
| `fig_S16.png` | MD 스냅샷·자유 Na의 F 포획 | ✅ **어긋남 1건** — a/b/c는 **before**인데 본문이 탈착 근거로 S16a를 인용(③ 주변) |
| `fig_S17.png` | Q3 (Na–F XPS) | 값은 Note S3와 일치. **배정 자체에 반론**(§10.2) |
| `fig_S13.png` | Gaussian16 IR 계산 결과 | 계산 1710/1527/1043 vs 실험 1710/1590/1021 — C=O만 정확 |
| `fig_3.png` (**수동 렌더**) | 자동 추출 실패분 복구 · 바인더 물성 원자료 | ✅ **어긋남 1건** — 3j가 73 최적을 지지하지 않는다(§10.4). σ_ion 1위가 PVdF |
| `fig_1.png` | 논문의 중심 주장(bollard 형상) | 모식이 **불연속 스터드 + 팽팽한 스팬** = 우리 시딩과 동형임 확인 |

**안 본 것 (33장)** — Fig 2, Fig 5, S2–S12, S14, S18–S28, S32–S38, 그리고 표 4장.
이유: Fig 2·5와 S18–S38의 수치는 **본문/SI 텍스트에 전부 명시**되어 있어 그림 판독으로 얻을 것이 없고(텍스트가 더 정확),
표(`tab_S1`–`tab_S4`)는 글자라 PDF 텍스트로 읽는 편이 정확하다(그렇게 했다 — §3c, §3d).
**따라서 이 digest에서 Fig 2 / Fig 5 / S18–S38의 서술은 "그림을 봤다"가 아니라 "텍스트를 읽었다"에 기반한다.**

---


### 11b. — 보강 2026-09-03: 이번에 실제로 본 매체

| 본 것 | 어떻게 | 무엇이 나왔나 |
|---|---|---|
| **Movie S1** (PTFE only) | 337 프레임 전수 + 6장 육안 + **진한-파랑 F 마스크 중심 추적** | 최대 들뜸 **24.3 px @ t=8.48 ps** → 2판 Fig 4f 디지타이즈("8–8.5 ps 피크") **독립 확인**.  2색 사슬 = 저자 평균 부분집합임을 **육안 확인** |
| **Movie S2** (PC_2Na+PTFE) | 337 프레임 전수 + 노란(Na) 마스크 추적 | PTFE **평평**(최종 3.3 px = S1 의 1/6.7).  Na **가로 −65.2 px / 세로 +3.7 px** = 표면 활주.  ⚠ Na 2개가 275/337 프레임 겹쳐 보임(가림) → 상한값 |
| **Movie S3** (PC_1Na+PTFE) | 337 프레임 전수 + **2-blob 분리 추적** | ★ Na 2개 **337/337 프레임 분리 판별**, 수직간격 **64.4 ± 5.1 px 내내 유지** = 자유 Na 가 10 ps 안에 **안 내려앉는다** → §4.5 의 "라벨은 표면접촉 Na 수" **영상 확정** |
| **본문 PDF 14 pp · SI PDF 56 pp** | 텍스트 전수 재검색 (압력·저항·퍼콜레이션 키워드) | §3e-(다) 의 **음성 결과 4건** 확정 + Fig 3b 역산으로 **두께 99.3 µm 복원** |

**안 본 것**: 2판이 이미 정리한 42장 크로핑 중 미판독 33장은 **이번에도 안 봤다**(§11 의 이유 그대로).
⚠ 이번 3판의 서술 중 **Fig 3b·3c 의 값**은 여전히 **2판의 그림 판독 + 본문 텍스트**에 기반하고,
내가 새로 판독한 것은 **영상 3편뿐**이다.

⚠ **재현 방법 메모** (이 픽셀 재측정을 누가 다시 하려면): 프레임 추출은 `ffmpeg -i <mp4> %04d.png`(337장),
마스크는 RGB 임계 — 진한 파랑 F `B>110 & B<215 & B−R>45 & B−G>25 & R<170`,
흰 슬래브 `R>195 & G>190 & B>190 & |R−B|<28`, 노랑 Na `R>170 & G>150 & B<110`.
고정 카메라 검증 = **흰 픽셀 수 변동 ±1 %**.  스케일은 **2판 Fig 4f 디지타이즈에서 차용**(≈11.9 px/Å) — 독립 눈금 아님.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
