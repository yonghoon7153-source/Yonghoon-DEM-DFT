# Diffusion Mechanism of Li Argyrodite Solid Electrolytes for Li-Ion Batteries and Prediction of Optimized Halogen Doping: The Effect of Li Vacancies, Halogens, and Halogen Disorder — de Klerk, Rosłoń & Wagemaker (Chem. Mater. 2016)

> slug `deklerk2016_diffusion_site_disorder_argyrodite` · DOI `10.1021/acs.chemmater.6b03630` · type `DFT-AIMD (순수 계산, 실험 0)` · PDF `82ea256b/f8e6711f-32._Diffussorder.pdf` (inbox #32, 사용자 분류 `DFT`, 본문 9 pp 7955–7963) + **SI 확보(2026-07-28, 인박스 #32 Sup = `82ea256b/428d530d-32._Sup_Disorder.pdf`, 6 pp: Tables S1–S3 전표(300/450/600 K σ·점프율·Ea) + Fig S1(PSe₆/Br 밀도)·S2(PSe₆/Br 점프그래프)·S3(4a-RDF))** · digested `2026-07-28` (동일자 SI 반영 갱신) · **SI 독립 재검증 `2026-08-03`(불일치 0건 — §3 상단)** · status ✅ 종결
> elements: Li, P, S, Se, Cl, Br, I
> methods: DFT, AIMD
> **저자**: Niek J. J. de Klerk, Irek Rosłoń, **Marnix Wagemaker*** — Department of Radiation Science and Technology, **TU Delft** (네덜란드). Chem. Mater. 2016, 28, 7955−7963. Received 2016-08-29 / Revised 09-29 / Published **2016-10-14**. **[외부]** (ADEM 네덜란드 + ERC FP7 307161 지원).

---

## 0. 이 digest를 읽는 법 (우리에게 왜 1순위인가)
이 논문은 argyrodite Li⁺ 전도의 **"halogen site disorder → inter-cage 활성화 → 거시 σ"** 서사의 **AIMD 원전(2016)** 이다 — Kraft 2017(실험 무질서 62→0 %)·Rao 2013/Rayavarapu 2012(실험)·[GG]/[Liu]/[Liang](후속 계산)·[Bai](리뷰)가 전부 이 논문을 무질서-메커니즘의 계산 근거로 소환한다. 우리 캠페인의 세 줄기가 이 논문에 정면으로 닿는다:
1. **무질서 decorate 방법론** — 그들이 AIMD 셀에 4a/4c S/X 무질서를 *어떻게* 넣었나 = 우리 **comp2 disorder ensemble**(라벨스왑 d-level·cfg0/1/2·anneal+relax)의 10년 전 원형. §4.2에 전 절차 복원.
2. **"무질서 75 %에서 σ 최고" 주장의 정확한 형태** — 인용 사슬에서 뭉개지기 쉬운 이 주장의 원문 조건(어느 조성·몇 K·무슨 지표·왜 100 %가 아닌가)을 §5.7에 고정. [Liu] digest의 재인용 판정 포함(§13).
3. **inter-cage = 율속** — 우리 `li_percolation` F*(0.191→0.078 eV)·BVSE 경로 위계·[Rao11]/[Dyre]/[Perc] 서사의 **jump-statistics 1차 계산 증거**.

> ⚠ **사이트 표기 주의 (이 논문 전체에 걸림)**: de Klerk는 free-anion 두 자리를 **4a("outside the cages") / 4c("inside the cages"=Li 48h 케이지 중심)** 로 부른다. Kraft 2017·[Liu]·우리 baseline 계열 표기로는 **de Klerk 4c ≡ 4d(cage-center, free-S²⁻ 기본 자리)**, 4a는 공통(F-43m 원점 선택 차이). 즉 이 논문의 "Cl 4c 점유 75 %" = 실험 문헌의 **"4d-자리 Cl 점유 75 %"**. 아래에서는 원문 표기(4a/4c)를 유지하되 필요 시 (=4d)로 병기.

## 1. 한 줄 요약
Li₇PS₆·Li₇PSe₆·Li₆PS₅Cl/Br/I 전 계열을 **VASP GGA AIMD(단위셀 52원자, 100 ps, 300/450/600 K)** 로 돌려 Li⁺ 점프를 **doublet(48h쌍 내)·intracage(케이지 내)·intercage(케이지 간, 율속)** 3종으로 분해 — (a) Cl/Br는 빠르고 I는 **intercage 점프 0**(모든 T)으로 느린 이유가 **halogen의 4a/4c 분포**임을 인공 배열(all-4a vs all-4c)로 입증하고, (b) Li vacancy와 halogen 치환 효과를 가상 조성(Li₆PS₆·Li₇PS₅Cl)으로 분리해 **둘 다 필요**함을 보이고, (c) Cl 주위 케이지엔 평균 **5 Li vs S 주위 7 Li**(빈 doublet 상존 → intercage 촉진)라는 국소 메커니즘을 RDF로 제시한 뒤, (d) **Li₆PS₅Cl의 최적 Cl 분포 = 4a:4c = 1:3(4c 점유 75 %)** 에서 limiting jump rate가 50:50 대비 **2×** → "합성으로 무질서를 조절하면 σ 2배" 예측, (e) 보너스로 **Li₅PS₄X₂**(할로겐-rich)가 Li₆PS₅Cl/Br급 σ + 공기/수분 안정 개선 후보라고 제안한, **halogen-disorder 엔지니어링의 계산 원전**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 시스템 | HT phase(F-43m, No. 216, a≈10 Å) 고정: **Li₇PS₆·Li₇PSe₆·Li₆PS₅Cl·Li₆PS₅Br·Li₆PS₅I** + 가상 **Li₆PS₆·Li₇PS₅Cl** + 신규 **Li₅PS₄Cl₂/Br₂/I₂** + Li₆PS₅Cl 무질서 5분포 |
| 질문 | (1) 왜 Cl/Br는 10⁻³ S/cm급인데 I는 수 자릿수 낮나? (2) σ↑의 원인이 Li vacancy인가 halogen인가 disorder인가? (3) 무질서를 *어떻게* 조절하면 σ 최대인가? |
| 당시 알려진 것 | 실험 σ(Cl/Br ~10⁻³ ≫ I)·I는 4a만 점유(Rayavarapu ref 12)·**4c-Cl 점유↑ → σ↑ 실험**(Rao 2013 in-situ 중성자, ref 19)·NMR 다중 점프 과정(refs 18/23) — **미시 메커니즘은 미해명** |
| 방법 계보 | 저자들 직전 Na₃PS₄ 논문(ref 24, Chem. Mater. 2016)의 **site-visit jump-statistics** 방법을 Li argyrodite로 이식 |
| 시점 | **Kraft 2017보다 1년 앞** — 참조 실험 무질서 값은 Kraft가 아니라 **Rayavarapu 2012(ref 12)·Rao 2013(ref 19)·Kong/Deiseroth 2010(refs 4·15)** |

## 3. 핵심 물성 (수치 총정리)
> ⚠ **출처 규율**: σ·점프율·Ea 정량은 **SI Tables S1–S3 정확값**(2026-07-28 SI 확보로 figure-read 전면 대체). 전부 **소환값**(우리 db 절대값과 혼합 금지; 그들 AIMD σ·Ea는 GGA·단위셀·100 ps 조건값). 괄호 = 1 표준편차(10-블록).
>
> **🔁 SI 독립 재검증 (2026-08-03, 인박스 #32 Sup 6 pp 2차 통독)**: SI 실물을 처음부터 다시 읽어 §3b 전표를 기계 대조 — **Tables S1–S3 × 14조성 × 8열(σ*_MSD·σ_J·점프율 3종·Ea 3종) 전값 및 괄호 표준편차·"−"·각주 a 표기까지 완전 일치, 불일치 0건**. Fig S1–S3 캡션 3건도 문구 단위 일치. **신규 사실 1건**(σ_J 재구성 검증, §9)·**표기 정밀화 1건**(Fig S2b, §8)만 추가 — 그 외 새로운 사실 없음 → **이 digest는 본문+SI 실물 기준으로 종결 상태**.
>
> **✅ figure-read → SI 표값 교정 이력 (2026-07-28)**: ① 450 K intercage 25/50/75/100 % ≈2/3/6/13×10¹⁰ → **1.79/3.12/6.20/14.36×10¹⁰ s⁻¹**(정합·정밀화); ② 450 K doublet 0→100 % ≈100/50/30/10/0.2×10¹⁰ → **103.68/52.44/26.11/10.09/0.21**(정합); ③ **limiting-rate 비 75 %/50 % "2×" → 6.20/3.12 = 1.99× 확정**; 100 % 붕괴 "~15×" → 3.12/0.21 = **14.9×**; ④ 600 K σ_J(Cl/Br) ≈4–5 → **4.66/4.32 S/cm**(정합), σ* ≈1–2 → **1.01/0.85**(상한 과대 판독이었음); ⑤ 300 K σ_J ≈1 → **0.89/1.23**(정합); **σ* ≈0.15–0.3 → Cl 0.04/Br 0.19 — Cl 오판(교정)**; ⑥ 본문 Ea 요약 "doublet·intracage 0.10–0.14 / intercage 0.20–0.25 eV"는 **대략치**로 판명 — SI 정밀값: Cl(50 %)·Br intercage **0.18–0.27**(온도별), doublet·intracage **0.10–0.17 eV**.

| 항목 | 값 | 조건/출처 |
|---|---|---|
| 점프 3종 거리 | **doublet 1.9 Å**(48h쌍 내) · **intracage 2.25 Å**(케이지 내 쌍간) · **intercage 가변**(케이지 연결) | 본문 §Results; 케이지 중심간 거리 **7.0 Å**(σ_J 환산용) |
| 케이지 구조 | 4c(=4d) 중심당 **48h 12개(6쌍)**; Li–Li쌍 거리 1.9 Å → **쌍당 1 Li**(≈50 % 점유) | 본문·ref 12 |
| σ (MD, 600 K) | σ_J: Cl(50 %) **4.66(0.66)** · Br **4.32(1.39)** S/cm; σ*(MSD): **1.01 / 0.85** | **Table S3** |
| σ (MD, 450 K) | σ_J: Cl(50 %) **2.56(1.04)** · Br **2.54(1.34)**; σ*: 0.52 / 0.39 | **Table S2** |
| σ (MD, 300 K) | σ_J: Cl(50 %) **0.89(1.29)** · Br **1.23(0.87)**(오차>값 = 통계 취약 표면화); σ*: **0.04 / 0.19** | **Table S1**; 임피던스 실측(~10⁻³)보다 **수 자릿수 높음**(단결정 상한 + GB 부재로 저자 해석) |
| Li₆PS₅I | **intercage 점프 0 — 300/450/600 K 전부**(S1–S3 모두 "−") → 거시 확산 없음; doublet만 **145.26/203.25/243.89 ×10¹⁰ s⁻¹**(Ea 0.05–0.07 eV) = 초고속 국소 왕복; σ* 0.02/0.05/0.08 | **Tables S1–S3** |
| Li₇PS₆·Li₇PSe₆ | 300 K intercage 0; 450 K 겨우 0.07/0.15·600 K 1.72/2.23 ×10¹⁰(Ea 0.32–0.37) → Cl/Br 대비 낮은 σ(600 K σ_J 1.24/1.37) | **Tables S1–S3** |
| σ 순위 (MD) | **Cl ≈ Br > PS₆ ≈ PSe₆ ≫ I** — 실험 순위 재현(ref 12) | 본문·S1–S3 |
| correlation factor | **f = D*/D_J < 0.2** (Cl·Br, 전 온도; 예: Cl 600 K σ*/σ_J = 1.01/4.66 = 0.22) → back-and-forth 다수 | 본문 + S1–S3 재계산 |
| Ea (MD, eq 2, ν₀=10¹³ s⁻¹) | **Cl(50 %)**: intercage **0.18/0.27/0.25**·intracage 0.10/0.13/0.15·doublet 0.10/0.14/0.17 eV (300/450/600 K) · **Br**: intercage **0.18/0.22/0.26**·intracage 0.11/0.14/0.17·doublet 0.10/0.13/0.17 | **Tables S1–S3** (본문 요약 0.10–0.14/0.20–0.25는 대략치) |
| Ea (문헌 대조) | NMR 단거리 0.08–0.09 / 장거리 **0.20(Br)·0.29(Cl)**; 임피던스 0.16–0.56(합성 의존); BV 단거리 0.10–0.20·intercage 0.30–0.35 | 본문 (refs 18·23·12·19) |
| 율속 판정 | **전 조성에서 intercage 점프율이 타 점프의 ≤1/5**(예: Cl 450 K 3.12 vs 26.11/36.75) → intercage가 거시 σ 지배 | 본문·S2 |
| NMR 정합 | Li₆PS₅Cl ⁷Li NMR 점프율 **~1×10⁹ s⁻¹ @350 K**(ref 18); MD 300 K intercage **7.3×10⁹ s⁻¹**(S1) ≈ 1자릿수 높음(통계 부족); **450/600 K→350 K 외삽은 NMR과 정합** | 본문 + Table S1 |
| RDF (450 K, Li₆PS₅Cl) | 4c-**Cl 주위 Li ≈5개 / 4c-S 주위 ≈7개**(≤3.5 Å 적분; **4a도 동일 경향 — Fig S3 실물 확인**: S(검정) 피크 > Cl(빨강), 피크 ~2.5 Å) → **Cl 근처 빈 doublet 상존** | Fig 6 + Fig S3; **5–7 분포가 6–6보다 안정**(전 온도·Cl/Br 공통) |
| 무질서 최적 (450 K) | **4c-Cl 75 %(4a:4c=1:3)**: min-rate = intercage **6.20(2.13)** vs 50 % **3.12(1.27)** ×10¹⁰ s⁻¹ = **1.99×**; σ_J도 **5.12 vs 2.56 = 2.00×** → "σ 2배" 예측의 표값 근거 | **Table S2** |
| 무질서 시리즈 σ_J (S/cm) | 0/25/50/75/100 %: 300 K **0.05/0.91/0.89/1.59/−**; 450 K **−/1.50/2.56/5.12/0.18**; 600 K **−/1.82/4.66/7.40/0.82** — **전 온도에서 75 % 최고** | **Tables S1–S3** (0 %는 300 K에 우발 점프 0.04×10¹⁰ 하나 잡힘; 100 % σ_J는 doublet-limited 환산, §9) |
| Li₅PS₄X₂ | 600 K σ_J: Cl₂ **5.91** · Br₂ **4.47** · I₂ **3.76** S/cm(**I₂도 거시 전도!** 300 K만 I₂ intercage 0); 450 K 2.90/1.36/1.00 — Li₆PS₅Cl/Br **동급~상회** | **Tables S1–S3**·Fig 9 |
| 격자 효과 | Br 격자 +0.13 Å(vs Cl)·Se +0.48 Å(vs S) — **intercage 점프율엔 유의 영향 없음**(Cl 3.12 vs Br 3.16 @450 K; doublet/intracage만 변화) → 이온반경/부피는 거시 σ 비지배 | 본문 (ref 12·15) + S2 |

### 3b. SI Tables S1–S3 전문 (300/450/600 K — σ: S/cm, 점프율: ×10¹⁰ s⁻¹, Ea: eV, 괄호 = 1σ)
> 표기: "−" = 해당 점프 미발생(또는 σ_J 미산출). "(−)" = 점프율 오차가 너무 커 Ea 오차 미산출(SI 각주 a). Li₆PS₅Cl 무질서 시리즈의 %는 4c-Cl 점유율(=Kraft/우리 표기 4d).

**Table S1 — 300 K**
| Material | σ*_MSD | σ_J | intercage rate / Ea | intracage rate / Ea | doublet rate / Ea |
|---|---|---|---|---|---|
| Li₇PS₆ | 0.04 | − | − | 16.56(1.37) / 0.11 | 0.73(0.63) / 0.18 |
| Li₇PSe₆ | 0.06 | − | − | 27.58(4.25) / 0.09 | 2.64(2.26) / 0.15 |
| Li₆PS₅Cl (50 % Cl@4c) | 0.04 | 0.89(1.29) | 0.73(1.05) / 0.18(0.02) | 17.78(3.20) / 0.10 | 21.58(3.82) / 0.10 |
| Li₆PS₅Br | 0.19 | 1.23(0.87) | 1.03(0.72) / 0.18(0.02) | 13.97(5.31) / 0.11 | 18.85(6.33) / 0.10 |
| Li₆PS₅I | 0.02 | − | − | − | 145.26(9.68) / 0.05 |
| Li₆PS₆ | 0.06 | 0.49(0.83) | 0.38(0.65) / 0.19 | 18.76(4.99) / 0.10 | 5.51(2.73) / 0.13 |
| Li₇PS₅Cl | 0.04 | 0.76(0.56) | 0.55(0.41) / 0.19 | 3.99(3.23) / 0.15 | 13.26(2.43) / 0.11 |
| Li₅PS₄Cl₂ | 0.15 | 0.60(1.28) | 0.56(1.20) / 0.18 | 24.21(14.31) / 0.10 | 2.46(3.14) / 0.15 |
| Li₅PS₄Br₂ | 0.17 | 0.15(0.33) | 0.15(0.33) / 0.23(−) | 9.13(3.50) / 0.12 | 10.05(3.37) / 0.12 |
| Li₅PS₄I₂ | 0.06 | − | − | 1.33(1.40) / 0.16 | 31.90(6.36) / 0.09 |
| Li₆PS₅Cl (0 % Cl@4c) | 0.29 | 0.05(0.16) | 0.04(0.13) / 0.26(−) | 8.12(5.34) / 0.13 | 74.36(6.62) / 0.07 |
| Li₆PS₅Cl (25 %) | 0.26 | 0.91(1.04) | 0.73(0.83) / 0.19(−) | 19.32(4.10) / 0.10 | 39.83(5.65) / 0.08 |
| Li₆PS₅Cl (75 %) | 0.14 | 1.59(0.79) | 1.28(0.63) / 0.17(0.01) | 20.94(2.55) / 0.10 | 6.09(2.01) / 0.13 |
| Li₆PS₅Cl (100 %) | 0.29 | − | 5.34(1.47) / 0.14 | 17.82(3.89) / 0.10 | **−** (doublet 0 → σ_J 미산출) |

**Table S2 — 450 K** (Fig 7·8의 온도)
| Material | σ*_MSD | σ_J | intercage rate / Ea | intracage rate / Ea | doublet rate / Ea |
|---|---|---|---|---|---|
| Li₇PS₆ | 0.18 | 0.07(0.21) | 0.07(0.21) / 0.37(−) | 30.99(9.37) / 0.14 | 7.55(2.38) / 0.19 |
| Li₇PSe₆ | 0.13 | 0.12(0.36) | 0.15(0.44) / 0.34(−) | 47.77(3.75) / 0.12 | 7.62(3.41) / 0.19 |
| Li₆PS₅Cl (50 %) | 0.52 | 2.56(1.04) | 3.12(1.27) / 0.27(0.02) | 36.75(5.54) / 0.13 | 26.11(4.73) / 0.14 |
| Li₆PS₅Br | 0.39 | 2.54(1.34) | 3.16(1.67) / 0.22(0.02) | 26.54(4.70) / 0.14 | 36.03(4.23) / 0.13 |
| Li₆PS₅I | 0.05 | − | − | 0.26(0.55) / 0.32(−) | 203.25(7.26) / 0.06 |
| Li₆PS₆ | 0.10 | 0.62(0.40) | 0.73(0.47) / 0.27 | 41.80(11.71) / 0.12 | 10.85(4.43) / 0.18 |
| Li₇PS₅Cl | 0.18 | 1.62(0.85) | 1.76(0.92) / 0.25 | 19.01(3.24) / 0.15 | 21.25(4.46) / 0.15 |
| Li₅PS₄Cl₂ | 0.70 | 2.90(1.08) | 4.10(1.52) / 0.22 | 32.77(6.89) / 0.13 | 13.08(5.55) / 0.17 |
| Li₅PS₄Br₂ | 0.64 | 1.36(1.07) | 2.05(1.62) / 0.24 | 16.21(4.05) / 0.16 | 31.95(6.29) / 0.13 |
| Li₅PS₄I₂ | 0.70 | 1.00(0.94) | 1.64(1.54) / 0.24 | 9.03(2.98) / 0.18 | 55.90(8.93) / 0.11 |
| Li₆PS₅Cl (0 %) | 0.18 | − | − | 21.67(5.54) / 0.15 | 103.68(6.64) / 0.09 |
| Li₆PS₅Cl (25 %) | 0.62 | 1.50(0.81) | 1.79(0.97) / 0.25 | 34.10(3.85) / 0.13 | 52.44(5.82) / 0.11 |
| **Li₆PS₅Cl (75 %)** | 0.60 | **5.12(1.76)** | **6.20(2.13) / 0.20(0.01)** | 38.89(5.97) / 0.13 | 10.09(1.54) / 0.18 |
| Li₆PS₅Cl (100 %) | 0.25 | 0.18(0.28) | 14.36(2.75) / 0.17 | 42.91(3.11) / 0.12 | **0.21(0.34) / 0.33(−)** |

**Table S3 — 600 K**
| Material | σ*_MSD | σ_J | intercage rate / Ea | intracage rate / Ea | doublet rate / Ea |
|---|---|---|---|---|---|
| Li₇PS₆ | 0.48 | 1.24(0.83) | 1.72(1.15) / 0.33(0.03) | 54.84(7.70) / 0.15 | 16.96(4.20) / 0.21 |
| Li₇PSe₆ | 0.74 | 1.37(1.22) | 2.23(1.98) / 0.32(0.04) | 66.37(5.70) / 0.14 | 15.31(4.32) / 0.22 |
| Li₆PS₅Cl (50 %) | 1.01 | 4.66(0.66) | 7.56(1.06) / 0.25(0.01) | 56.88(5.21) / 0.15 | 37.48(6.51) / 0.17 |
| Li₆PS₅Br | 0.85 | 4.32(1.39) | 7.18(2.31) / 0.26(0.02) | 40.47(4.93) / 0.17 | 41.07(4.78) / 0.17 |
| Li₆PS₅I | 0.08 | − | − | 3.08(2.45) / 0.30(0.03) | 243.89(10.51) / 0.07 |
| Li₆PS₆ | 0.55 | 4.36(1.57) | 6.79(2.44) / 0.26(0.03) | 64.49(7.78) / 0.14 | 8.42(1.94) / 0.25 |
| Li₇PS₅Cl | 1.18 | 3.63(1.14) | 5.27(1.65) / 0.27(0.02) | 31.54(4.27) / 0.18 | 14.21(5.55) / 0.22 |
| Li₅PS₄Cl₂ | 2.04 | 5.91(1.40) | 11.13(2.64) / 0.23(0.01) | 52.41(7.00) / 0.15 | 35.33(5.78) / 0.17 |
| Li₅PS₄Br₂ | 1.61 | 4.47(1.01) | 8.97(2.03) / 0.25(0.01) | 31.90(3.57) / 0.18 | 42.87(4.86) / 0.16 |
| Li₅PS₄I₂ | 1.15 | 3.76(0.81) | 8.21(1.78) / 0.25(0.01) | 18.10(2.99) / 0.21 | 78.56(7.77) / 0.13 |
| Li₆PS₅Cl (0 %) | 0.18 | − | − | 45.21(7.79) / 0.16 | 120.90(4.78) / 0.11 |
| Li₆PS₅Cl (25 %) | 0.82 | 1.82(0.65) | 2.91(1.04) / 0.31(0.02) | 52.26(6.09) / 0.15 | 66.24(5.29) / 0.14 |
| Li₆PS₅Cl (75 %) | 0.91 | 7.40(1.50) | 11.92(2.42) / 0.23(0.01) | 57.35(4.59) / 0.15 | 14.10(2.85) / 0.22 |
| Li₆PS₅Cl (100 %) | 0.47 | 0.82(0.66) | 24.15(3.04) / 0.19(0.01) | 57.78(4.75) / 0.15 | 1.32(1.07) / 0.34(0.03) |

> **SI 전표에서 새로 보이는 것 4가지 (우리 독해)**: ① **무질서 최적 75 %는 σ_J 기준 전 온도(300/450/600 K) 일관** — 450 K 한 점이 아니라 시리즈 전체에서 성립(75 %/50 % σ_J비 1.79/2.00/1.59×). ② **σ*_MSD로는 75 % 우위가 약함**(450 K 0.60 vs 0.52 소폭; **600 K는 0.91 vs 1.01로 역전**) — "2×"는 limiting-rate(σ_J) 지표의 결론이지 MSD 지표가 아님(→§13). ③ **σ*_MSD는 국소 왕복에 오염** — 300 K에서 0 %(0.29)·100 %(0.29)가 50 %(0.04)보다 높게 나옴(doublet/intracage 왕복이 MSD에 잡힘): 저자들이 σ_J를 주지표로 쓴 이유의 수치 실증. ④ **100 % 배열에서 doublet Ea 0.33–0.34 eV**(450/600 K) = 전 표에서 최고 장벽 — "doublet 붕괴가 새 율속"의 정량 확인(50 % 배열 doublet 0.14 대비 +0.2 eV).

## 4. 방법 ★ (사용자 최우선 — 전 절차 복원)

### 4.1 AIMD 셋업
| 항목 | 값 |
|---|---|
| code | **VASP** (ref 25 Kresse/Hafner) |
| functional | **GGA**(ref 26 = **PBE**) — vdW 없음, DFT+U 없음 |
| basis/pseudo | **PAW-PBE** (ref 27 Blöchl) |
| ecut | **280 eV** (⚠ 낮음 — 현대 기준 soft; S/P 표준 400+ eV 대비 절감 셋업) |
| 셀 | **단위셀 1×1×1, a≈10 Å** — Li₆PS₅X = **52원자**(24 Li+4 P+20 S+4 X)·Li₇PS₆ 56·Li₅PS₄X₂ 48. **supercell 없음** |
| k-points | minimization **2×2×2** → MD **1×1×1**(Γ) |
| MD | **NVT, temperature scaling every 1000 steps**(=2 ps마다 velocity rescale; Langevin/Nosé 아님), **dt 2 fs**, **총 100 ps**, equilibration **2.5 ps** |
| 온도 | **300 / 450 / 600 K** (전 조성) |
| 초기구조 | 문헌 구조 사용(있으면; 없으면 최유사 구조) → minimization → MD |
| 오차 | 각 시뮬을 **10블록 분할** 후 표준편차(점프 과정 비상관 가정, 블록간 재평형 불필요 논리) |

### 4.2 무질서 decorate 방법론 ★★ (우리 comp2 ensemble의 원형 — 정밀 복원)
- **무질서 자유도**: 4 f.u. 단위셀의 free-anion 8자리(4a×4 + 4c×4)에 S 4개·X 4개 배치. **Fig 8 시리즈 = Cl의 4c 점유 5단계: 0/25/50/75/100 %** = 셀당 4c-Cl 0/1/2/3/4개(나머지 Cl은 4a; S는 보수적으로 반대 배치).
- **각 %당 배열 수 = 1개(단일 배열)**. 복수 배열·앙상블 평균 **없음**. 배열 선택 기준(랜덤/Ewald/enumerate) **일절 언급 없음** — **SI 실물 확인(2026-07-28)으로 확정: SI에도 배열 좌표·배치 그림·선택 기준 없음**(SI 구성 = Fig S1–S3 + Tables S1–S3이 전부).
  - *우리 해석(원문 아님)*: 1×1×1 셀에서는 4c 부격자(FCC 4자리)에서 1개(C=4)·2개(C=6)·3개(C=4) 고르기가 **입방 대칭으로 사실상 등가**라 "분포 %만 정하면 anion 배열은 거의 유일" — 단일 배열이 우연히 정당화되는 셀 크기. **더 큰 셀에선 성립 안 함**(배열 다양성 발생) → 이 방법을 supercell로 확장하려면 우리처럼 config 앙상블 필수.
- **표준 Li₆PS₅Cl(Fig 2·3·4의 기본 시뮬) = 50:50 배열** — Fig 4b(4c에 Cl 2 + S 2) 추론이 **SI 표 라벨 "Li₆PS₅Cl (50 % Cl@4c)"로 공식 확정**(Tables S1–S3). "currently prepared materials"(refs 12·19의 실험 ≈even 분포)를 모사. **Li₆PS₅I = all-4a**(실험 ref 12 그대로). **+ 신규 확인(Fig S2b): 표준 Li₆PS₅Br 런도 4c가 S+Br mixed = 50 % 배열**(본문엔 미명시였던 것; 캡션은 "Br at 4c"까지·"2개"는 그림 판독 — §8 정밀화 2026-08-03).
- **Li 배치**: 48h 24쌍에서 **쌍당 1 Li 제거**(쌍내 1.9 Å 동시점유가 에너지적 불리) → 24 Li. 쌍 안에서 어느 쪽 48h를 남기는지 기준 **미명시**(**SI에도 없음 — 2026-07-28 확정**). Li-vacancy는 조성으로 내재(Li₆ vs Li₇) — **명시적 공공 배치 규칙 없음**; 흥미롭게도 "Cl 케이지 5 Li / S 케이지 7 Li"의 불균등 분포는 **MD 중 자발 형성**(§5.6, 초기 배치 아님).
- **가상 조성 분리실험**: **Li₆PS₆**(=Li₇PS₆−1Li/f.u.: vacancy만, Cl 없음)·**Li₇PS₅Cl**(=Li₆PS₅Cl+1Li/f.u.: Cl만, vacancy 없음) — 변수 분리를 *조성 조작*으로 구현(우리 grand-canonical이 아니라 중성 위반을 감수한 인공 셀; 전하보상 처리 언급 없음 → 사실상 jellium 배경 가정으로 추정, **원문 미명시**).
- **Li₅PS₄X₂**: free-anion 8자리 전부 X(4a 4 + 4c 4 전부 halide), Li 20개.

### 4.3 점프 통계 → 물성 환산 (post-processing 수식 체계)
1. **site-visit 추적**: 각 Li가 방문하는 결정학 자리를 MD 내내 기록(방법 = ref 24 Na₃PS₄ 논문). **자리 반경 ≈0.9 Å**(이웃 자리 겹침 직전 최대).
2. **τ = J/(N·t)** (eq 1): J=점프 수, N=Li 수, t=시간 → 점프유형별 평균 점프율.
3. **ΔE_A = −kT·ln(τ/ν₀)** (eq 2, Vineyard ref 28): **ν₀ = 1×10¹³ s⁻¹ 가정** — Ea는 점프율의 로그 재표현(아레니우스 기울기 아님!).
4. **D_J = τ·a²/(2d)** (eq 3, Einstein–Smoluchowski, d=3): 점프율 확산계수. **σ_J용 a = 7.0 Å**(케이지 중심간 — "케이지 내 평균 위치=중심"이라 intercage 점프가 실질 변위라는 논리).
5. **D\*** = MSD tracer (eq 4).
6. **σ = ne²z²D/(k_BT)** (eq 5, **Nernst–Einstein**) → σ_J(점프율)·σ*(MSD) 두 벌. **Haven 보정 없음** — 대신 **f = D*/D_J**를 상관계수로 별도 보고(f<0.2 = back-and-forth 다수 = σ_J이 σ*보다 과대).

## 5. 결과 — 섹션별 상세

### 5.1 구조·점프 분류 (Fig 1)
HT F-43m: PS₄는 4b, free S는 4a+4c, Li는 4c를 둘러싼 48h(≈50 % 점유). 할로겐 치환 시 X는 4a 또는 4c만 차지(PS₄의 S는 불가침, ref 9). 48h 6쌍 = 케이지. MD 궤적에서 점프 3종 확인: **doublet(1.9 Å) → intracage(2.25 Å) → intercage(가변)**. **거시 확산엔 3종 모두 필요, 최저 점프율이 율속** — 이 프레임이 논문 전체의 렌즈.

### 5.2 조성별 σ (Fig 2)
5조성 아레니우스(σ_J·σ* 쌍). **Cl·Br 최고, PS₆·PSe₆ 중간, I는 거시 확산 0**(실험 순위 재현). MD σ ≫ 임피던스 실측: (a) PS₆/PSe₆는 실험이 LT phase라서, (b) Cl/Br는 **grain boundary가 실측을 지배**(수십 nm 전하수송, ref 18)라서 — MD는 결정 bulk **상한**. ⁷Li NMR(bulk 국소 점프)과는 동일 자릿수 → AIMD 검증. f<0.2 (Cl·Br): 점프의 8할이 왕복. **이온반경 무관론**: Br(+0.13 Å)·Se(+0.48 Å) 격자 팽창에도 intercage 점프율 유사 → "부피/Li"는 거시 σ 비지배(doublet/intracage만 민감) — Kraft 2017의 "무름/분극성" 서사와 *다른 축*으로 격자 크기를 기각한 선행 판정.

### 5.3 Li⁺ 밀도 시각화 (Fig 3, 450 K)
Li₇PS₆·Li₆PS₅Cl·Li₆PS₅I 밀도맵 — 전 조성 4c 둘레 케이지 4개 구조. **I: 48h쌍 고밀도만**(doublet, XRD·NMR과 정합) → 쌍간 경로 없음 = 국소 진동만. **PS₆: 케이지 내 국소화 강함**(큰 maxima). **Cl: maxima 작고 퍼짐** = 케이지 내 고속 순환 + 케이지 연결 시작. [GG]/[Liu]의 확률밀도 그림들의 원형.

### 5.4 점프 통계·Ea (Fig 4)
450 K 점프 그래프(선 굵기=점프율): PS₆=doublet+intracage 위주(intercage 소수), **Cl=3종 모두 + intercage 다수(빨강 망)**, I=doublet뿐. MD Ea(ν₀=10¹³): 단거리 0.10–0.14 / **intercage 0.20–0.25 eV**(본문 요약 — SI 정밀값은 온도별: Cl intercage 0.18/0.27/0.25 @300/450/600 K, §3) — NMR(0.08–0.09/0.20–0.29)·BV(0.10–0.20/0.30–0.35)와 정합, 임피던스(0.16–0.56)는 합성 의존 산포. **"intercage rate가 전 조성에서 ≥5× 낮음 → σ 올리려면 intercage부터"** — 설계 지침의 근거 문장.

### 5.5 vacancy vs halogen 분리 (Fig 5) — 가상 조성 실험
"Cl→S 치환의 σ↑가 단지 전하보상 Li-vacancy 때문인가?" 검증: **Li₆PS₆**(vacancy만)과 **Li₇PS₅Cl**(Cl만) 모두 케이지+intercage 연결이 나타나고 **rate-limiting intercage 점프율은 실제 Li₆PS₅Cl과 유사**(doublet/intracage는 서로 크게 다름). → **vacancy와 Cl 치환 둘 다 유의하게 작용, σ↑는 둘의 합작** — "vacancy가 전부"라는 단순론 기각. (우리 dual_mechanism 기록 — barrier와 prefactor/carrier 반반 — 과 같은 결의 2016년 판.)

### 5.6 국소 메커니즘: 5–7 Li 분포 (Fig 6) — 이 논문의 미시 화학 핵심
450 K Li₆PS₅Cl에서 4c-Cl vs 4c-S 주위 Li-RDF: 피크(≈2.5 Å) 위치·폭은 같으나 **Cl 주위 적분(≤3.5 Å) ≈5 Li vs S 주위 ≈7 Li**(4a도 동일 경향). 해석: **Cl⁻(−1)은 S²⁻(−2)보다 Li를 덜 묶음** → 전하보상 공공이 Cl 케이지에 몰림 → **Cl 근처엔 항상 빈 doublet** → intercage 점프의 착지 자리 상존 → 촉진. 전 온도·Cl/Br 공통으로 **5–7 분포 > 6–6 안정**. 부수 통찰: argyrodite 안정성 계산(ref 6)은 Li-배치(할로겐 유도)에 강민감할 것 — Li-배치 공간이 너무 커 본 논문 범위 밖 선언(→ 우리 enumeration/Ewald 접근이 채우는 자리).

### 5.7 ★ Halogen disorder — "75 % 최적"의 정확한 형태 (Fig 7·8)
- **동기**: vacancy로는 Cl vs I의 수 자릿수 차이를 설명 못 함. 실험(ref 12)은 I=4a만/Cl=4a+4c 분포, 실험(ref 19)은 4c-Cl↑→σ↑.
- **인공 배열 실험 (Fig 7, 450 K, Li₆PS₅Cl)**:
  - **all-4a**(I 모사): **intercage 점프 0** — 케이지들이 고립(Fig 7a: 초록+파랑만). Li₆PS₅I가 느린 이유 = 화학이 아니라 **자리 분포**.
  - **all-4c**: intercage 폭발적 증가(Fig 7b: 빨강 망; 450 K 14.36×10¹⁰ s⁻¹ = 50 % 배열의 4.6배)하나 **doublet 점프율 급락(0.21×10¹⁰, Ea 0.33 eV = 전 표 최고 장벽) → doublet이 새 율속** → intercage가 "국소 운동"으로 전락, σ 여전히 낮음(σ_J 0.18 — doublet-limited 환산, §9).
  - → **무질서(4a+4c 동시 점유) 자체가 거시 확산의 필요조건**. 두 자리 치환이 서로 다른 점프 유형을 켠다: **4c-X → intercage↑ / 4a-X(=4c-S 유지) → doublet 유지**.
- **분포 스캔 (Fig 8, 450 K, 단일 배열/점; SI 표값으로 정밀화)**: 4c-Cl 0/25/50/75/100 %에서 intercage 단조↑(−/1.79/3.12/6.20/14.36×10¹⁰ s⁻¹)·doublet 단조↓(103.68/52.44/26.11/10.09/0.21)·intracage 평탄(21.67–42.91) → **doublet과 intercage 곡선이 75 %와 100 % 사이에서 교차**. min(3종 점프율)의 최대 = **75 %**:
  - 75 % min = intercage **6.20(2.13)** vs 50 % min = intercage **3.12(1.27)** ×10¹⁰ s⁻¹ = **1.99×** — 본문 "limiting jump rate 2×"의 표값 (원문: *"the highest Li-ion conductivity can be obtained when three-quarters of the 4c sites (and one-quarter of the 4a sites) are occupied by Cl ions... a limiting jump rate 2 times larger compared to when the Cl ions are evenly distributed"*). **σ_J도 5.12 vs 2.56 = 2.00×**.
  - 100 %는 min = doublet **0.21×10¹⁰**(Ea 0.33 eV) → 50:50 limiting 대비 **14.9× 낮음** — "무질서↑=σ↑ 단조"가 **아님**.
  - **SI 3온도 일관성(+뉘앙스)**: σ_J 기준 75 % 최고는 **300/450/600 K 전부 성립**(75/50 비 1.79/2.00/1.59×) — 450 K 한 점 결론이 아님. **단 σ*_MSD 기준으로는 우위 약함**(450 K 0.60 vs 0.52; **600 K 0.91 vs 1.01 역전**) — "2×"는 limiting-rate(σ_J) 지표의 결론(§13).
- **주장 형태 요약(재인용 검증용)**: ① 조성 = **Li₆PS₅Cl**(Cl 1.0; Br·I는 "최적 분포 다를 것" 명시 — Tables S1–S3 근거), ② 온도 = 본문 Fig 8은 **450 K**, SI 표는 300/600 K도 제공(σ_J 기준 75 % 최적 전 온도 일관·σ*는 편차), ③ 지표 = **min-jump-rate 극대화**(σ 직접 계산 아님; "σ 2배"는 σ_J∝limiting rate 논리의 예측 — σ_J 2.00× 표값 뒷받침), ④ 셀 = 단위셀·분포당 단일 배열·100 ps, ⑤ 실행 제안 = **열처리로 무질서 조절 가능**(ref 19) → "1:3 분포 합성 시 σ 2배" 전망.
- **성립 이유(원문 논리)**: 4c-Cl은 intercage를 켜지만 doublet을 끄는 **이율배반 레버** → 최적은 양 끝이 아닌 내부점. 3:1은 "intercage를 충분히 켜되 doublet이 아직 안 죽는" 지점 — 정량적 이유 설명은 없음(점프율 곡선의 교차가 사실상 전부).

### 5.8 Li₅PS₄X₂ — 할로겐-rich 제안 (Fig 9)
"무질서가 좋다면 할로겐을 더 넣어 4a·4c를 모두 X로": Li₅PS₄Cl₂/Br₂/I₂ AIMD → **전부 거시 전도**(Li₅PS₄I₂도 450/600 K에서 Cl₂/Br₂급 — Li₆PS₅I와 극명 대조), σ ≈ Li₆PS₅Cl/Br 동급~상회 — 600 K σ_J **Cl₂ 5.91 / Br₂ 4.47 / I₂ 3.76** vs Li₆PS₅Cl 4.66 / Br 4.32 S/cm (Tables S3). 역설 포인트: Li₆PS₅Cl에서 all-4a·all-4c는 나빴는데 **4a+4c 완전 점유(X₂)는 좋음** → "4a와 4c가 *둘 다* (같은 halide로라도) 점유되는 것"이 관건. I-rich 함의: Li₇₋ₓPS₆₋ₓIₓ에서 x>1이면 I가 4c로 밀려 들어감 → σ↑ 전략(ref 30 Pecher와 연결; [Rao2025]의 10년 전 예고). **안정성 보너스 추정**: free-S²⁻를 Cl⁻/Br⁻로 바꾸면 **산소·수분 안정 개선 "not unlikely"** — 정량 없음, 순수 추정( [Zhu20] 가수분해 지도·[Zuo]/[Liu] Cl-rich 서사의 씨앗 문장).

## 6. 메커니즘 종합 (Conclusions 재구성)
1. 할로겐 치환은 전하보상 Li-vacancy를 만들지만, **vacancy 양만큼이나 halogen "분포"가 중요** — 분포가 **vacancy 분포를 결정**(5–7 Li)하고, 그것이 국소 확산(빠름)을 거시 σ로 번역하는 스위치.
2. **4a·4c 각 자리의 치환이 서로 다른 점프 유형을 가속**(4c→intercage, 4a쪽 구성→doublet 유지) + 거시 확산은 3종 전부 필요 → **두 자리에 걸친 분포(=site disorder)가 고-σ의 필요조건**.
3. 처방 둘: (a) 분포 최적화(Li₆PS₅Cl 1:3 → σ 2×), (b) 할로겐 총량 증가(Li₅PS₄X₂ — σ 동급 + 공기/수분 안정 가능성).

## 7. 전체 논증 흐름
점프 3종 정의(Fig 1) → 5조성 σ·순위 재현+NMR 정합(Fig 2) → 밀도맵으로 I=doublet-only 시각화(Fig 3) → 점프통계·Ea로 intercage=율속 확정(Fig 4) → 가상 조성으로 vacancy/halogen 분리(Fig 5) → RDF 5–7 Li로 국소 메커니즘(Fig 6) → 인공 배열 all-4a/all-4c로 무질서=필요조건 입증(Fig 7) → 분포 스캔 최적 75 %(Fig 8) → 할로겐-rich 일반화(Fig 9) → "분포 조절 + 함량 증가" 처방으로 닫음.

## 8. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | HT Li₇PS₆ 구조(48h 노랑·4a 분홍·4c 빨강·PS₄) | 사이트 표기 매핑(4c=cage center) 기준 그림 |
| 2 | 5조성 σ_J·σ* 아레니우스(300–600 K) | MD σ=bulk 상한·GB 격차 논리의 원전; **σ_J vs σ*(f<0.2) 분리 보고** 양식 |
| 3 | Li 밀도맵 3조성(450 K) | I=doublet-only·Cl=퍼짐 — [GG]/[Liu] 확률밀도의 원형; 우리 li_density_cube 그림과 동종 |
| 4 | 점프 그래프(선굵기=rate) PS₆/Cl/I | **jump-network 시각화** — 우리 percolation 그림의 그래프 판; deck용 3종 점프 도식 |
| 5 | 가상 Li₆PS₆·Li₇PS₅Cl 점프 그래프 | **변수분리(vacancy vs halogen) 설계** — 우리 가상 조성 실험 템플릿 |
| 6 | Li-RDF: 4c-Cl vs 4c-S (450 K) | **5–7 Li 메커니즘** — 우리 site-분해 분석(어느 케이지에 공공이 모이나)으로 재현 가능 |
| 7 | all-4a vs all-4c 점프 그래프 | **무질서=필요조건의 결정적 실험** — 우리 comp2 ordered(d=0) frozen과 동일 물리 |
| 8 | **점프율 vs 4c-Cl 점유(0–100 %)** | **★ 75 % 최적의 원자료** — 우리 disorder ensemble의 d-level 스캔과 정면 대응 |
| 9 | Li₅PS₄X₂ 아레니우스 | 할로겐-rich(우리 modelc Cl1.6 계열) σ 동급의 최초 계산 근거 |
| Fig S1 | Li₇PSe₆·Li₆PS₅Br 밀도맵(450 K) | Br=Cl과 유사한 퍼진 케이지+연결; PSe₆=국소화 — Fig 3 보완 |
| Fig S2 | Li₇PSe₆·Li₆PS₅Br 점프그래프(450 K) | **Br 표준 런의 4c가 mixed**(캡션 원문: *"black: Se/S at 4c, **pink: Br at 4c**"* — 같은 4c에 S와 Br이 함께 앉음 = 무질서 배열) — §4.2 배열 판정 근거. **정밀화(2026-08-03)**: 캡션이 직접 말하는 것은 "Br이 4c에 있다"까지이고 **"2개(=50 %)"는 구슬 개수 판독값**(SI 표도 Br 행엔 % 라벨을 안 붙임 — % 라벨은 Li₆PS₅Cl 시리즈에만). 50 % 판정 자체는 본문의 "currently prepared materials(≈even 분포) 모사"와 정합하나, **표기 근거는 캡션이 아니라 그림 판독**임을 구분해 인용 |
| Fig S3 | **4a-사이트 Li-RDF**(S vs Cl, 450 K) | 4a에서도 S 주위 > Cl 주위 — 5–7 Li 메커니즘이 두 자리 공통임의 증거 |
| **Tables S1–S3** | **300/450/600 K × 14조성 σ*_MSD·σ_J·점프율 3종·Ea 전표(±1σ)** | **→ §3b 전문 수록** — figure-read 전면 대체·75 % 최적의 3온도 검증·σ* vs σ_J 지표 분리 |

## 9. Post-processing ★
- **site-visit jump statistics**(자리 반경 0.9 Å) → 점프유형별 τ → Ea(eq 2)·D_J(eq 3) — **NEB 없이 유한온도 점프율로 장벽 서열화**. 도구 자작(ref 24 방법).
- **MSD → D\*** + **f=D*/D_J** 상관 진단(Haven 대신).
- **σ_J**: intercage rate + a=7.0 Å(케이지 중심간) — "intercage만이 실변위" 가정의 명시적 구현.
  - **SI 표 역산으로 드러난 규칙(우리 관찰, 원문 미서술)**: σ_J는 엄밀히는 **limiting-rate 기반** — 100 % Cl@4c처럼 doublet이 율속이 되면 σ_J를 intercage(14.36)가 아니라 **doublet rate(0.21→σ_J 0.18 @450 K; 1.32→0.82 @600 K)** 로 환산하고, 300 K처럼 doublet=0이면 σ_J 자체를 "−" 처리(intercage 5.34가 있어도). 본문 "intercage 거리 사용" 서술의 예외 처리 — "intercage가 국소 운동으로 전락"의 수치 구현.
  - **★ 신규 (2026-08-03 SI 재검증): 위 규칙을 추정이 아니라 수치로 확정** — eq 3+5를 그대로 조립해 SI의 σ_J를 **독립 재계산**했다: σ_J = (n/V)·e²·D_J/(k_BT), D_J = τ_min·a²/6, **a = 7.0 Å 고정**, n = 셀당 Li 수(Li₆PS₅X 24 / Li₇PS₆·Li₇PSe₆ 28 / Li₅PS₄X₂ 20), V ≈ 10 Å 급 단위셀. 결과: **11개 대조 케이스(3온도·4계열) 전부 SI 표값과 1–4 % 내 일치** — 예) Cl 50 % 450 K 계산 2.64 vs SI 2.56, 600 K 4.79 vs 4.66, 75 % 450 K 5.24 vs 5.12, 0 % 300 K 0.051 vs 0.05, Li₇PS₆ 600 K 1.27 vs 1.24, Li₅PS₄Cl₂ 450 K 2.89 vs 2.90. 확정되는 것 셋:
    1. **τ_min(3종 점프율의 최솟값)이 σ_J의 유일한 입력** — 100 % Cl@4c 450 K를 doublet(0.21)로 넣으면 **0.178 ≈ SI 0.18**, intercage(14.36)로 넣으면 **12.1 = 67× 과대**. limiting-rate 해석이 배타적으로 성립.
    2. **doublet이 율속일 때도 a = 7.0 Å(케이지 중심간)를 그대로 쓴다** — 실제 doublet 변위 1.9 Å을 쓰면 (7.0/1.9)² ≈ 13.6× 작아진다. 즉 **100 % 배열의 σ_J 0.18/0.82는 "doublet 빈도로 케이지-간 거리를 뛴다"는 상한 가정값** — all-4c가 나쁘다는 결론의 방향은 안전하지만, 그 절대값은 이 환산 규약에 종속(인용 시 명시할 것).
    3. **부수 산출: 그들 AIMD 셀 크기 역산** — 위 일치를 정확히 맞추는 V ≈ **985 ± 15 Å³ → a ≈ 9.95 ± 0.05 Å**(논문·SI 모두 격자상수 미기재). 실험 Li₆PS₅Cl a ≈ 9.86 Å 대비 **+1 %**로, PBE 과대추정과 정확히 부합 → "문헌 구조 → PBE minimization 후 MD"라는 §4.1 서술의 독립 확인.
- **Li 밀도맵·점프 그래프**(선굵기=rate) 시각화, **원소별 RDF**(Li around 4c-Cl/S).
- **10-블록 오차**: 시계열 블록 분할 표준편차.
> 우리 적용: (1) **min-of-three-rates 지표** — 우리 MD에서도 doublet/intracage/intercage를 분리 집계하면 "무엇이 율속인가"를 d-level별로 말할 수 있음(현재 우리는 총 MSD만). (2) **f=D*/D_J** — 우리 Haven 논의와 등가지만 점프율 기반이라 저렴. (3) 케이지 중심간 7.0 Å 환산은 우리 F*(PMF percolation) 지표와 상보 — 같은 "inter-cage 병목"을 각각 rate와 free-energy로 잼.

## 10. 우리 DFT 대비 (comp1/modelc/comp2) → `../our_dft_baseline.md`
> **방법 라벨**: 그들 = **진짜 AIMD**(VASP GGA, 힘=DFT). 우리 Ea·D = **MLIP-MD**(UMA-s-1p1 omat) — "둘 다 AIMD" 표현 금지. 그들 절대 σ·Ea = 소환값.

| 항목 | de Klerk 2016 (AIMD) | 우리 (MLIP-MD·DFT) | 판정 |
|---|---|---|---|
| **무질서 → σ↑ 방향** | all-4a=intercage 0 → 분포 걸치면 켜짐; 최적 75 % | comp1→modelc D(600 K) 3.09→7.90×10⁻⁶ cm²/s·Ea 0.253→0.224 eV; disorder_ensemble comp1 d=0.5 **Ea 0.177±0.027**(ordered frozen은 artifact 1.17); comp2 ordered champion **Ea 0.276 ≥ comp1** → disorder 런 진행 | **✓✓ 방향·물리 일치** — "ordered/한쪽-몰림 = frozen"을 우리 d=0 아티팩트와 comp2 ordered가 독립 재현 |
| **inter-cage = 율속** | intercage rate ≤1/5 · Ea 0.20–0.25 vs 단거리 0.10–0.14 | **li_percolation F\*** comp1 **0.191** → modelc **0.078 eV**(600 K Li-밀도 PMF, anti-site가 inter-cage 평탄화); BVSE 위계·[Rao11] 정합 | **✓✓ 정면 일치** — 그들 "intercage rate만 켜면 σ↑" = 우리 "F* 하락이 σ↑ 설명". 지표만 다름(rate vs PMF 문턱) |
| **5–7 Li (공공이 Cl 케이지로)** | RDF 적분 5 vs 7; 자발 형성 | 우리 site-분해 미실시(재현 후보) — modelc vacancy 서사(prefactor·carrier)와 정합적 | ○ 재현가치 높음: UMA 궤적에서 케이지별 Li 수 히스토그램이면 즉시 검증 |
| **무질서 decorate** | 분포 %당 **단일 배열**·선택기준 없음·단위셀 52원자·minimize 후 MD 100 ps | comp2 ensemble: 같은 52원자 단위셀이지만 **d-level(0/0.5/1.0)×cfg 3개**, Cl·Br↔free-S 라벨스왑 → **UMA anneal 700 K 20 ps + FIRE relax(fmax 0.03)** 후 NVT 600/800/1000 K 200 ps | **우리가 엄밀** — 특히 un-relaxed 스왑이 σ₃₀₀ ~70 mS/cm 아티팩트를 낸 우리 v1 사례(2026-07-27)는 "단일 배열+2.5 ps equil"의 위험을 실증. 단 그들은 힘이 DFT(정확)·우리는 MLIP(빠름·앙상블 가능) — 상보 |
| **온도·창 규율** | 300/450/600 K·100 ps·점프 수 부족 시 300 K 통계 취약(자인) | 600/800/1000 K 3점 아레니우스(400/500 제외)·**MSD 2–50 ps 고정창**·멀티시드 판정·절대 σ 인용 금지 | 우리 규율이 그들 약점(300 K 저통계·10-블록 가정)을 정확히 겨냥 |
| **σ 절대값** | σ_J(300 K) Cl 0.89±1.29 / Br 1.23±0.87 S/cm (Table S1; 오차>값) — 실측 대비 수 자릿수 과대(GB 부재·상한 해석) | UMA σ 3–5× 과대 인지 → 비율만 | ✓ 같은 캐비앳 계보 — "MD σ=bulk 상한" 문장 인용 가능 |
| **vacancy vs halogen 분리** | 가상 Li₆PS₆·Li₇PS₅Cl — 둘 다 필요 | 우리 dual_mechanism(장벽↓+prefactor/carrier↑ 합작) | **✓ 결론 동형** — 2016 AIMD가 우리 반반 서사의 선행 |
| **격자 크기 무관론** | Br/Se 팽창해도 intercage 불변 | Kraft(무름·prefactor)와 별개 축; 우리 EOS(modelc 수축)·comp2 진행 | △ 주의: de Klerk는 "크기 무관", Kraft는 "무름이 Ea·σ₀ 지배" — 둘은 모순 아님(크기≠강성) but 인용 시 축 구분 |
| **75 % 최적의 강건성** | σ_J 기준 3온도 일관(75/50 비 1.79/2.00/1.59×, Tables S1–S3)·단일 배열·**σ*_MSD 기준은 편차**(600 K 역전 0.91<1.01) | (우리 미검증) INDEX 계산값 #8(2024 MTP-MLIP, 대규모)은 **"σ 피크 = 4c-Cl 25 %"** 보고 — 원문과 상충 | **⚠ 방법 의존 플래그** — "최적 %" 숫자는 셀 크기·배열 수·**지표(limiting-rate σ_J vs MSD)**·MLIP에 민감(σ* 600 K 역전이 그 민감성의 내부 증거). 안전 인용은 "중간 무질서에 최적 존재(양 끝 나쁨)"까지 |
| **할로겐-rich** | Li₅PS₄X₂ σ 동급 + 안정 추정 | modelc(Cl1.6) D 2.6×·[GG]/[Zuo]/[Liu] Cl-rich 계열 | ✓ 우리 modelc 노선의 최초 계산 선례(단 그들 X₂=완전치환, 우리 1.6) |

## 11. 적용 인사이트 (깊게)
1. **comp2 disorder ensemble의 문헌 정당화 + 차별화 논리 완성**: "왜 config 3개씩 돌리나?"의 답이 이 논문 — 원전은 **분포당 1배열·2.5 ps equil**로 75 %를 뽑았고, 2024 MLIP 재검(#8)은 25 %로 뒤집었다. 즉 **최적 %는 배열·통계 민감** → 우리 anneal+relax+멀티 config 설계가 정확히 그 빈틈을 메운다. 논문/deck 문장: "the optimal halogen distribution has been debated (75 % [de Klerk] vs 25 % [MTP-MLIP 2024]); our relaxed multi-config ensemble addresses the single-configuration ambiguity."
2. **F\*와 min-jump-rate는 같은 병목의 두 척도**: 그들 "min(doublet, intracage, intercage) 극대화" = 우리 "F* 최소화"와 동일 목적함수. 우리 li_percolation 그림에 de Klerk 점프 위계(0.10–0.14/0.20–0.25 eV)를 소환값 눈금으로 병기하면 서사가 잠긴다.
3. **5–7 Li 재현 = 저비용 고가치**: UMA 궤적에서 4d(=그들 4c) 중심별 ≤3.5 Å Li 적분 히스토그램만 뽑으면 "공공이 Cl 케이지로 몰린다"를 comp1/modelc/comp2에서 검증 가능 — vacancy-prefactor 서사의 미시 그림.
4. **doublet 붕괴 경고 = Cl-rich 상한의 물리**: all-4c에서 doublet이 죽어 σ가 꺾인다는 관찰은 "무질서·Cl은 다다익선"이 아님을 원전이 이미 못박은 것 — modelc(1.6)·comp2 d=1.0 해석 시 "어느 점프가 새 율속이 됐나"를 점검할 것.
5. **Li₅PS₄X₂·I-rich 예고**: [Rao2025]의 I-rich·[Son]의 물질군 교체 이전에, 2016년에 이미 "free-S²⁻를 halide로 바꿔 공기/수분 안정"을 추정으로 적어둠 — 우리 axis-④(대기) 서사의 최초 씨앗 인용처.

## 12. 인용 가능 문장 (deck/paper용)
- "de Klerk et al. (AIMD, 2016) showed that macroscopic diffusion in Li₆PS₅X requires all three jump types — doublet, intracage, and the rate-limiting intercage — and that halogen site disorder over 4a/4c is what switches the intercage jumps on: with all halides on 4a (as in Li₆PS₅I) no intercage jump occurs at any simulated temperature."
- "Their predicted optimum, 75 % of the cage-center (4c/4d) sites occupied by Cl (a 1:3 4a:4c distribution), maximizes the *minimum* jump rate — 6.20 vs 3.12 ×10¹⁰ s⁻¹ at 450 K (1.99×, SI Table S2), consistent at 300–600 K in the jump-rate conductivity but not in the MSD-based one; note this is a single-configuration, single-cell prediction, and a 2024 large-scale MLIP study instead reports a 25 % optimum."
- "On average only five Li surround a 4c-Cl cage versus seven around a 4c-S cage: the charge-compensating vacancies condense next to the halide, so an empty 48h doublet is always available to receive an intercage jump — the microscopic origin of disorder-enhanced conduction."
- "Artificial compositions Li₆PS₆ (vacancies only) and Li₇PS₅Cl (Cl only) both reproduce the rate-limiting intercage jump rate of Li₆PS₅Cl — vacancies and halogen substitution are jointly, not singly, responsible."
- "Our percolation threshold F* (0.191→0.078 eV, comp1→modelc) is the free-energy analogue of de Klerk's min-jump-rate criterion: both measure the same inter-cage bottleneck that anion disorder flattens."

## 13. 주의/한계 (over-claim 방지) + 재인용 판정
- **75 % 주장의 조건 4중 축약 금지**: Li₆PS₅Cl 전용(Br/I 상이 명시)·**σ_J(limiting-rate) 지표**(σ 직접 아님)·분포당 단일 배열·단위셀. "argyrodite는 75 % 무질서가 최적" 일반화는 원문 초과. SI 확보로 정밀화: σ_J 기준 75 % 최고는 **3온도 일관**(비 1.79/2.00/1.59×)이나, **σ*_MSD 기준은 편차**(600 K 75 % 0.91 < 50 % 1.01 역전) — 지표(σ_J vs MSD)에 따라 결론 강도가 달라짐을 명시하고 인용할 것.
- **[Liu] digest 재인용 판정 (요청 항목)**: liu2022 digest의 "Klerk … 75% 무질서 시 최고" — **핵심은 정확**(4d(=Klerk 4c) Cl 점유 75 %=1:3에서 limiting rate 최대). 단 ① 같은 행의 "무질서↔σ 양의 관계"는 **비단조**(0 %·100 % 모두 저전도, doublet↔intercage 교차)를 단조로 축약, ② Klerk 최적은 **Cl 1.0** 기준이라 Liu의 LPSCl₁.₅(61.7 %)에 그대로 씌우는 건 원문도 경고한 외삽. → liu2022 §14에 정정 각주 추가(2026-07-28).
- **후속 상충**: INDEX 계산값 #8(2024, MTP-MLIP 대규모·비-아레니우스)은 **σ 피크 = 4c 25 %** — 최적 위치는 방법 의존. 안전한 합의는 "양 끝(0/100 %)이 나쁘고 중간에 최적 존재"까지.
- **Excel 메모 오류 정정**: INDEX 계산값 #6의 "LPSCl Ea ~0.38 eV"는 **이 논문의 LPSCl 값이 아님**(SI 정밀값: Cl(50 %) intercage 0.18/0.27/0.25 eV @300/450/600 K; 0.38 후보 = Rao2011 임피던스 Ea(Cl) 0.38 혼입 또는 **SI의 Li₇PS₆ 450 K intercage 0.37(−)** 오독 — 어느 쪽이든 LPSCl 아님) → INDEX 행 교정함.
- ~~SI 미보유~~ → **SI 확보(2026-07-28, 인박스 #32 Sup)**: Tables S1–S3 전문 §3b 수록, figure-read 전면 교체(교정 이력 §3 상단). 남는 캐비앗: ① **300 K는 오차>값**(예: Cl σ_J 0.89±1.29, intercage 0.73±1.05) — 300 K 정량 인용 부적합이 표준편차로 정량 확인됨; ② SI Ea는 **온도별 값**(eq 2의 T-의존 환산)이라 단일 "Ea" 인용 시 온도 명시 필수(Cl intercage 0.18/0.27/0.25 @300/450/600 K); ③ 본문 Ea 요약(0.10–0.14/0.20–0.25)은 SI 표 대비 **대략치**.
- **무질서 배열 좌표·Li 공공 배치 규칙·점프 카운팅 추가 세부는 SI에도 없음(확정)** — "단일 배열·기준 미명시" 판정 유지(§4.2). **격자상수도 본문·SI 모두 미기재**(우리 역산 a ≈ 9.95 Å, §9-3).
- **★ 100 % Cl@4c의 σ_J(450 K 0.18 / 600 K 0.82)는 "doublet 빈도 × 케이지-간 7.0 Å" 환산의 상한값** — 2026-08-03 재구성으로 확정된 규약(§9-2). doublet의 실제 변위 1.9 Å로 환산하면 ≈1/13.6. **"all-4c도 σ가 0.18은 나온다" 식 인용 금지** — 안전한 진술은 "all-4c에서는 doublet이 새 율속이 되어 최적 분포(75 %) 대비 σ_J가 ~28× 낮다"(5.12→0.18, 같은 환산 규약 내 비교)까지.
- **SI 재검증 결과(2026-08-03)**: Tables S1–S3 전값·Fig S1–S3 캡션 전부 재확인, **불일치 0건**. 신규 = σ_J 재구성 검증(§9)뿐 → digest **종결 상태**.
- **셋업 연대적 한계**: ecut 280 eV·Γ-only MD·velocity-rescale NVT·100 ps·단위셀 52원자·10-블록 오차(점프 비상관 가정) — 2016 기준 표준이나 현대 기준 soft. 절대 Ea·σ는 이 조건값으로만 소환.
- **Ea는 아레니우스 기울기가 아님**: eq 2(τ와 ν₀=10¹³ 가정의 로그 변환) — 우리·실험 아레니우스 Ea와 정의가 다름. 직접 등치 금지(방향·서열만).
- **가상 조성(Li₆PS₆·Li₇PS₅Cl)의 전하 처리 미명시** — 결과는 시사적, 정량 인용 비권장.
- **300 K 통계 취약 자인**: 점프 수 부족(I·PS₆·PSe₆ intercage 0; NMR 대비 1자릿수 편차) — 300 K 값 인용 금지, 450/600 K·외삽만.
- 안정성·기계·전자구조·ESW = **범위 밖**(n/a). Li₅PS₄X₂ 공기/수분 안정은 **추정 문장**("not unlikely")이지 계산 아님.

## 14. 기법 용어 미니사전
- **doublet jump**: 1.9 Å 떨어진 48h 자리쌍 내 왕복 점프. 가장 빠름·국소.
- **intracage jump**: 같은 케이지의 다른 48h쌍으로 점프(2.25 Å). 케이지 내 순환.
- **intercage jump**: 이웃 케이지로 점프(거리 가변, 중심간 7.0 Å). **전 조성에서 최저 rate = 거시 σ 율속**.
- **site-visit jump statistics**: MD 궤적에서 각 Li의 결정학 자리 방문 이력(자리 반경 ~0.9 Å)으로 점프를 세는 방법 — NEB 없이 유한온도 rate/장벽 서열.
- **σ_J vs σ\***: 점프율 기반(D_J=τa²/6, a=7.0 Å) vs MSD 기반(D*) Nernst–Einstein σ. **f=D*/D_J<1**이면 왕복 상관(σ_J 과대).
- **halogen(site) disorder**: X⁻와 free-S²⁻가 4a("케이지 밖")·4c(=4d, "케이지 중심") 두 자리에 섞여 앉는 것. Rietveld 점유율로 실측(Rayavarapu/Rao/Kraft), 열처리로 조절(ref 19).
- **5–7 Li distribution**: Cl 중심 케이지 평균 5 Li / S 중심 7 Li — 전하보상 공공이 할라이드 케이지에 응집, 빈 doublet이 intercage 착지점 제공.
- **velocity-rescale NVT**: 1000스텝(2 ps)마다 속도 재조정으로 온도 유지 — Langevin/Nosé보다 조악한 구식 서모스탯(동역학 교란 가능).
- **min-of-three-rates 최적화**: σ를 올리려면 3종 점프율의 최솟값을 키워야 한다는 설계 지표 — Fig 8의 75 % 최적이 이 지표의 산물.
