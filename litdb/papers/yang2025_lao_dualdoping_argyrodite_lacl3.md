# Lanthanum and oxygen co-doping of lithium argyrodite for enhanced humid air stability and lithium metal compatibility — Yang et al. (Electrochimica Acta 2025)

> slug `yang2025_lao_dualdoping_argyrodite_lacl3` · DOI `10.1016/j.electacta.2025.146619` · type `exp (계산 0)` · PDF 본문 `cc9fb4bc-LaO_co_doped_LPSC_PO_bond_LaCl3____1.pdf` (11 pp) + **SI `a2f73b4e-1s2.0S0013468625009806mmc1.pdf` (12 pp — Fig S1–S15·Table S1–S4 전부 확보·정독)** · digested `2026-07-14` · status ✅
> **저자**: Jie Yang, Yi Wang, Ziling Jiang, Lin Li, Ziyu Lu, Miao Deng, Qiyue Luo, Siwu Li, Chen Liu, Zhenyu Wang, **Chuang Yu**(교신) — HUST Wuhan(화학·전기전자) · Guilin Univ. of Electronic Tech. · Xidian Univ. · Electrochimica Acta **535** (2025) 146619 (accepted 2025-06-02)

---

## 0. 이 digest를 읽는 법
이 논문은 **우리 Nd₂O₃-doped modelc 프로그램의 가장 가까운 실험 자매편**이다: **Cl-rich argyrodite(Li₅.₅PS₄.₅Cl₁.₅)에 희토류 산화물(RE₂O₃=La₂O₃)을 격자 도핑** → **σ는 희생(9.58→6.23 mS/cm)하고 대기안정(P–O 결합) + Li-금속 계면(LiCl·La⁰·"LaCl₃" SEI)을 얻는** trade-off. 우리와 조성계(Cl-rich)·도판트 패밀리(RE³⁺+O²⁻)·트레이드(σ-비용 vs interphase-이득)가 전부 평행하다.
- ⚠ **명명 주의 ①**: 이 논문의 "**LPSC**" = **Li₅.₅PS₄.₅Cl₁.₅ (Cl-rich)** 다. litdb 다수 문헌([Taklu]·[Ma24])의 LPSC=Li₆PS₅Cl(=comp1)과 다름. 우리 modelc(Li₅.₄PS₄.₄Cl₁.₆)와 **가깝지만 동일 아님**(Cl 1.5 vs 1.6).
- ⚠ **명명 주의 ②**: 도핑 조성 `Li₅.₅₊₂ₓP₁₋ₓLaₓS₄.₅₋₁.₅ₓO₁.₅ₓCl₁.₅` — x=0.04 최적 = **Li₅.₅₈P₀.₉₆La₀.₀₄S₄.₄₄O₀.₀₆Cl₁.₅** (전하균형 ✓: La³⁺가 P⁵⁺ 치환 → +2 Li/La; O:La=1.5:1=La₂O₃ 화학량론 그대로). Excel 시트의 "Li5.48"은 오타(5.5+2×0.04=5.58).
- ⚠ **증거 위계 주의**: **계산 0** (DFT·AIMD·NEB 전무). 그리고 **음극 LaCl₃/La⁰ 메커니즘은 본문+SI 어디에도 분광 증거가 없다** — 도식(Fig 3h–j)+선행문헌(refs 38–40, Yao Nature LaCl₃ SE 계열) 차용. §6이 이 논문의 핵심 질문("LaCl₃ 어디서 오나")을 주장 vs 증거로 분해한다.
- **SI 정독 결과(12 pp)가 오히려 결정적** — 3가지 부재의 확인: ① **음극(Li) 계면 XPS·La 3d·Cl 2p 전무** (유일 post-cycling XPS = Fig S15 **양극** S 2p/P 2p) → **LaCl₃-at-anode는 측정이 아니라 가설**; ② 논문 전체에서 유일하게 *관측된* La-함유 계면종 = **양극 계면의 "LaSₓ"**(Fig S15b S 2p 성분 — 단 SE 자체 LaS₄ 신호일 수도); ③ **Table S1 Rietveld는 La·O를 P1·S2와 완전 동일 좌표·동일 U_iso·명목 조성 고정**으로 "칠해 넣은" 템플릿 → **La@4b/O@16e는 fit의 가정이지 독립 결정이 아님**; O 1s XPS·Raman/FTIR P–O 밴드도 전무 → **P–O/PS₃O 주장 역시 직접 분광증거 0**.

## 1. 한 줄 요약
Cl-rich argyrodite Li₅.₅PS₄.₅Cl₁.₅에 **La₂O₃를 dilute 격자 도핑(La→4b(P자리)=LaS₄, O→PS₄ 코너=PS₃O)** 하면 σ는 9.58→6.23 mS/cm로 **떨어지지만**, (a) **P–O 결합이 가수분해를 억제**해 습윤공기(RH 40–55%) 안정성·500 °C 어닐 회복률(43.5% vs 11.9%)이 크게 좋아지고, (b) **Li 금속 계면에서 La⁰·LiCl(+논문 주장 LaCl₃) SEI가 형성**돼 CCD 0.9→**3.1 mA/cm²**·대칭셀 ~200 h·NCM955 full cell 1C 500사이클 **83.6%** 를 달성한다 — **"σ를 팔아 interphase를 산다"** 는 우리 Nd₂O₃ 서사의 실험판.

## 2. 메타 / 동기 / 설계 계보
| 항목 | 내용 |
|---|---|
| Host | **Li₅.₅PS₄.₅Cl₁.₅** ("LPSC", Cl-rich; σ ~10 mS/cm급, 기계 연성) |
| 문제 | Cl-rich의 2대 약점 = **대기(수분) 불안정**(H₂S, σ 붕괴) + **Li-금속 비호환**(dendrite, 계면 부반응) |
| 도핑 | `Li₅.₅₊₂ₓP₁₋ₓLaₓS₄.₅₋₁.₅ₓO₁.₅ₓCl₁.₅`, x = 0, 0.02, **0.04(최적)**, 0.05, 0.10 — **La₂O₃ 단일 전구체로 La+O 동시 공급**(RE³⁺ 양이온 + O²⁻ 음이온 dual-doping; [Taklu] CuCl·[Li25] CuBr₂와 같은 "한 염 두 도펀트" 계열) |
| 설계 계보 | ① Yao et al. **Nature 616 (2023) 77–83** [ref 38]: Li₀.₃₈₈Ta₀.₂₃₈La₀.₄₇₅Cl₃(LTLC) SE — σ 3.02 mS/cm@30 °C·Ea 0.197 eV, **cycling 중 gradient 계면 passivation층** 형성, Li 대칭셀 >5000 h(1 mAh/cm²); **Li dendrite 접촉 시 LiCl + La(금속) 계면층 형성**. ② Xu et al. Adv. Mater. 36 (2024) 2310356 [ref 39]: LTLC를 Li₆PS₅Cl에 **interlayer("sandwich")** 로 삽입 → 대칭셀 >500 h@0.5 mA/cm². ③ 본 논문: **"그럼 La를 아예 황화물 격자에 도핑하면 LiCl–La passivation층이 계면에서 in-situ로 생기지 않겠나"** |
| 논문이 내세운 La·O의 3대 이점 (intro) | (1) La³⁺ 큰 반경(~1.06 Å) → **확장된 Li 확산채널·짧은 경로**; (2) **안정한 La–S–Cl 종 + 강한 P–O 결합** → 가수분해·환원 확률↓; (3) SEI 형성 시 **LiCl 등 Li-염 유도체의 분산 촉진** → Li 계면 안정화 |
| LaCl₃ 구조 논거 (인용) | LaCl₃ 결정 = **여섯 개 edge-sharing [LaCl₉] trigonal prism이 만드는 1D 채널**(내경 ~4.6 Å) — Li⁺ 이동용 octahedral 자리 풍부 → "O-도핑으로 잃은 σ를 고전류에서 보상" [refs 38, 40]. **+ "lithium-induced reduction of La³⁺ to La⁰ helps mitigate lithium dendrites"** (p.2 원문) |
| 연구유형 | 순수 실험 (XRD/Rietveld·SEM/EDS·EIS·DC-pol·H₂S·CCD·대칭셀·full cell·DRT·XPS) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSC (x=0) | LPSC-La₀.₀₄ (x=0.04) | 시리즈 (x=0.02/0.05/0.10) | 출처 |
|---|---|---|---|---|
| σ (RT) | **9.58 mS/cm** | **6.23** (0.65×) | 6.78 / 5.15 / 3.45 | Fig 1f |
| Ea | **0.238 eV** | **0.254** | 0.249 / 0.259 / 0.289 | Fig 1g, S3 |
| σ_e (DC-pol 0.5 V) | **2.59×10⁻⁹ S/cm** | **2.2×10⁻⁸** (**8.5×↑** ⚠) | n/a | Fig 1h |
| 격자상수 a (Rietveld) | 9.792987 Å | **9.823359 Å** (+0.031, 팽창; 본문. ⚠ Table S1은 a=9.823930·Rwp 4.12·Rp 5.76로 본문(Rwp 4.14/Rp 2.98)과 불일치) | 4a/4d 무질서: Cl 4a 0.385 / 4d 0.615 | Fig 1b, Table S1 |
| 구조 배치 | — | **La→4b(P자리)=LaS₄ 사면체 · O→PS₄ 코너 S 치환=PS₃O 사면체** | x≥0.05 불순물 피크(용해한계) | Fig 1a–c |
| H₂S (RH 50–55%, 30 min) | ~3.2 cm³/g (계속 증가) | **~2.3 cm³/g** (15 min 후 포화) | n/a | Fig 2a |
| σ after 노출 (RH 50–55%) | 9.58→**2.53×10⁻³** mS/cm | 6.23→**9.98×10⁻²** (39× 우위) | n/a | Fig 2c |
| Ea after 노출 | 0.238→**1.099 eV** | 0.254→**0.597** | n/a | Fig 2d, S5 |
| 어닐 회복 (RH 40–45% 30 min→500 °C, 펠릿) | 1.14 mS/cm = **11.90%** | **2.71 = 43.5%** (300/350/400/450 °C: 0.159/0.168/2.30/2.42) | n/a | Fig 2e,f,g |
| 분말 직접노출→어닐 | n/a | 노출 7.48×10⁻² → 어닐 **0.64 mS/cm (10.3%)** | n/a | Fig 2f,h |
| 물 직접반응 | **~150 s 내 격렬 완전반응** | 같은 시간 훨씬 느림 | n/a | Fig S7 |
| CCD (Li 대칭, ramp) | **0.9 mA/cm²** | **3.1** (3.4×) | 2.4 / 2.2 / 2.0 — **σ와 무상관(논문 명시)** | Fig 3a–f |
| Li 대칭셀 (0.5 mA/cm²·0.5 mAh/cm²) | ~25 h 과전압 급증→국부단락 | **~200 h** (말기엔 부반응) | n/a | Fig 3g |
| CV (**Li/SE/SS 비대칭 planar**, 0–5 V) | 곡선 사실상 **동일**(겹침) | 〃 — **창 확대 없음** | planar SS-CV=저감도 kinetic(Dewald 비판 지형) | Fig S8 |
| Full cell 1C (ZrO₂@NCM955/Li-In, 2.4–3.7 V vs Li-In) | 초기 158.1 → 250cyc 140.0 (88.6%) → 500cyc 130.1 (**82.2%**) | 초기 **179.1** → 165.9 (**92.6%**) → **149.7 (83.6%)** | 1C = 200 mA/g | Fig 4a |
| EIS 100cyc@1C: R_ce / R_ae | 41.7 / 39.9 Ω | **37.6 / 27.7 Ω** (부속: R_b 13.2→**18.6**=벌크 σ↓ 반영 · R_gb 5.26→**1.92** · Warburg 22.4→10.9) | Table S2 | Fig 4b |
| Rate 0.1/0.2/0.5/1/2C | 222.7/197.3/181.4/157.2/124.3 | 206.9/193.5/182.2/167.2/**144.5** (**저율 열세·고율 우세**) | n/a | Fig 4c,d |
| 0.2C 100cyc | 초기 200.2→177.2 (88.5%); R_ce/R_ae **191/448 Ω** | 초기 193.8→**182.9 (94.4%)**; **18.5/171 Ω** | Table S3 | Fig S12 |
| 60 °C 0.5C | (Liu et al. ref16 동일구성 172.6) | 초기 **231.76**·30cyc 223.2 (**96.3%**; 초기 CE 88.5%) | n/a | Fig S13a,b |
| −20 °C 0.1C | n/a | 초기 144.2·50cyc **148.4** (활성화; 초기 CE 67.5%) | n/a | Fig S13c,d |
| NCM712(LiNbO₃@)/**Li 금속** 0.5C·**3.0–4.2 V** | — | 초기 125.5→100cyc 87.6 (**69.8%**) — **논문 내 유일한 진짜 Li-금속 full cell**(헤드라인 500cyc는 Li-In) | Table S4 자기보고 | Fig S9 |
| Cycled 양극 XPS (100cyc@1C, NCM/SE 계면) | S 2p: PS₄³⁻+**P₂Sₓ(164.2/163.4 eV)+Li₂Sₓ(162.9/161.9 eV)**; P 2p: PS₄³⁻+P₂Sₓ | S 2p: PS₄³⁻+**"LaSₓ"**(P₂Sₓ/Li₂Sₓ 성분 없음); P 2p: PS₄³⁻만 | **음극 XPS 없음·La 3d 없음** | Fig S15 |

## 4. 재료 & 방법
- **합성**: Li₂S(99.8%, Aladdin) + P₂S₅(99%, Macklin) + LiCl(99.9%, Aladdin) + **La₂O₃(99.9%, Macklin)** 화학량론 혼합 → **고에너지 볼밀 500 rpm·16 h(WC 용기)** → 360 MPa 펠릿 → **500 °C·5 h 소결**(muffle furnace, Ar, 2 °C/min). ⚠ **LaCl₃는 전구체가 아님** — Cl원은 LiCl뿐.
- **대칭셀**: SE 100 mg 펠릿(⌀10 mm, 360 MPa) 양면에 ⌀5 mm Li 디스크.
- **Full cell**: 양극 = **ZrO₂@LiNi₀.₉₀Co₀.₀₅Mn₀.₀₅O₂(NCM955)** : SE : VGCF = **70 : 28 : 2**(planetary mill 180 rpm 1 h), 5 mg 양극혼합물 + 100 mg SE, **Li-In 합금** 음극, 2.4–3.7 V vs Li-In(≈3.0–4.3 V vs Li⁺/Li), 1C=200 mA/g, NEWARE CT-4000. ZrO₂ 코팅의 2중 역할 명시: 물리 배리어 + **격자 O 포획(ZrO₂→Li₂ZrO₃)**.
- **Li-금속 전지**: SE 120 mg(Li₅.₅₈P₀.₉₆La₀.₀₄S₄.₄₄O₀.₀₆Cl₁.₅) + LiNbO₃@NCM712 + **Li 복합음극**.
- **특성화**: XRD(PANalytical, Cu Kα, 10–80°, 5°/min) + Rietveld · XPS(Thermo K-Alpha+, Al Kα) · SEM/EDS(TESCAN MIRA LMS) · EIS(Admiral Squidstat Plus, **0.1 Hz–2 MHz**; 저주파까지 내린 이유=SOC/SOD별 계면임피던스+Warburg 확산 포착 명시) · DC 분극(0.5 V, 3600 s) · H₂S 부피측정(RH 50–55%, 30 min) · 습도노출(RH 40–45%/50–55%)+단계별 어닐(300–500 °C) · CCD(전류 계단 상승) · **DRT**(4개 시간영역 분해) · 온도변수 사이클(60 °C·−20 °C).

## 5. 결과 — 섹션별 상세

### 5.1 구조: La→4b, O→PS₄, 격자 팽창 (Fig 1a–e)
- XRD: 전 조성 cubic argyrodite(F-43m, Li₇PS₆ PDF#34-0688 기준) 주상. **x≥0.05에서 불순물 피크(♦, 미동정)** → "dopant 용해한계" (Li/Jiang의 산화물 도핑 문헌과 동일 현상 인용). **x=0.04까지 상순수.**
- Rietveld(x=0.04): a=9.823359 Å vs undoped 9.792987 Å — **미세 팽창**. 저자 해석: **La가 4b(P 자리) 치환 → LaS₄ 사면체 형성, O는 PS₄의 S 자리 → PS₃O 사면체**.
- ⚠ **Table S1 정독 판정 — "자리 결정"이 아니라 "자리 가정"**: ① **La(4b)는 P1(4b)과 좌표(0,0,0.5)·U_iso(0.0553) 완전 동일, frac=명목값 0.04 고정**; **O(16e)도 S2(16e)와 좌표(0.123621,−0.12362,0.623621)·U_iso(0.0704) 완전 동일, frac 0.06 고정** — 점유·위치·ADP 어느 것도 독립 refine되지 않은, 명목 조성을 P/S 자리에 "칠해 넣은" 모델. lab-XRD에서 La(Z=57) 정도는 보이지만 이 fit 구조로는 La@4b vs La@Li(48h) 판별 불가([Liu23] Mg 자리 논쟁과 동형). ② 템플릿 자체가 **Li₆PS₅Cl형**: Li 48h frac 0.5(=Li 6.0/f.u., 명목 5.58 아님)·cage 4a/4d Cl+S 합 1.0/f.u.(명목 Cl 1.5 미반영; Cl 4a 0.385/4d 0.615)·O frac 0.06을 16e에 두면 활자 그대로는 0.24/f.u.(명목 0.06의 4×, 점유 규약이 다르지 않는 한 내부 불일치). ③ **지표 불일치**: 본문 Rwp 4.14/Rp 2.98/a 9.823359 vs Table S1 Rwp 4.12/**Rp 5.76**/a **9.823930**. → 격자 팽창 trend만 취하고, 자리 배치는 "가정"으로 인용할 것.
- SEM: 입자 크기 undoped와 동급. EDS(Figure S1): P·S·Cl·La·O 균일분포 = 응집 없는 균일 도입.

### 5.2 이온·전자 전도: σ↓·Ea↑, "entropy–enthalpy compensation" (Fig 1f–h)
- σ: 9.58 → 6.78 → 6.23 → 5.15 → 3.45 mS/cm (x=0→0.10). **단조 감소** — 저자는 O 도입 자체를 주원인으로 지목("PS₃O³⁻ 사면체 형성이 이온전도 감소로 이어진다는 유사보고 [24,43] 인용"), x=0.05의 급락은 2차상 탓.
- Ea: 0.238 → 0.249 → 0.254 → 0.259 → 0.289 eV — 단조 증가. 해석: **전기음성 O가 강한 공유 P–O 결합 형성 → Li⁺ 이동 국소 장벽(엔탈피)↑**; 동시에 **La³⁺ 큰 반경이 O²⁻와 mismatch → 격자 왜곡·O/S 공공 증식 → 배열 엔트로피↑**; transition state theory로 "엔탈피·엔트로피가 선형 보상 → 활성화 자유에너지 준정상" — **x=0.02에서 σ는 크게 떨어지는데 Ea는 거의 안 변하는 현상**의 설명으로 제시. (정량 뒷받침 없는 서사적 TST 논변임에 주의 — §14.)
- σ_e: 2.59×10⁻⁹ → **2.2×10⁻⁸ S/cm (8.5× 증가)**. 저자는 "여전히 Li 금속 호환에 충분히 낮다"고 downplay + "늘어난 σ_e가 추가 저항요소 도입해 전체 Ea에 영향" 언급. ⚠ σ_e↑인데 CCD↑ — [Taklu]/[Li25]의 "σ_e↓→CCD↑" 서사와 **역방향 사례**(§11).

### 5.3 대기·수분 안정성: P–O 결합의 효과 (Fig 2)
- **H₂S**(RH 50–55%, 30 min): 둘 다 초기 급증 후 완만 — undoped는 계속 증가(~3.2 cm³/g), **doped는 15 min 후 정체(~2.3 cm³/g)**.
- **메커니즘(저자)**: ① O의 높은 전기음성도 → **P–O 결합이 P–S보다 절단에 강함**; ② O 도입이 **PS₃O³⁻ 구조** 형성 → 물과 **물리흡착** 위주(vs PS₄³⁻는 **화학흡착**) [ref 15 = 자기 그룹 Sn 논문]. — 우리 ICOHP P–O −8.43 vs P–S −5.98(+41%)·O@PS₄ −0.67 eV/O가 이 주장의 원자단위 정량판(§11).
- 노출 후: XRD 둘 다 열화+미지 불순물, **undoped가 더 많음**(Fig 2b). σ: 9.58→2.53×10⁻³ vs 6.23→**9.98×10⁻²** mS/cm(Fig 2c) — 노출 후 절대 σ가 39× 우위. Ea: 0.238→**1.099** vs 0.254→**0.597 eV**(Fig 2d) — 구조손상 정도 지표.
- **어닐 회복**(RH 40–45% 30 min 노출 펠릿): 300→500 °C 단계별 σ = 0.159/0.168/**2.30/2.42/2.71** mS/cm — 400 °C부터 회복 개시, 500 °C 최대 = **43.5% 회복** (undoped 동일조건 **11.90%**). 분말 직접 자연노출(40–45%RH)조차 어닐 후 0.64 mS/cm(10.3%). 색상 사진(Fig 2g,h): 노출 시 변색 → 500 °C 어닐로 백색 회복.
- **물 직접 침지**(Fig S7): undoped **150 s 내 격렬 완전반응** vs doped 훨씬 느림.

### 5.4 Li 금속 호환: CCD·대칭셀 — "σ가 아니라 계면화학이 결정" (Fig 3)
- CCD: 0.9(x=0) → 2.4(0.02) → **3.1(0.04)** → 2.2(0.05) → 2.0(0.10) mA/cm² — 화산형. **저자 명시: "CCD 크기는 이온전도도와 상관없어 보인다 … La₂O₃ dopant가 전해질–Li 계면의 화학적 성질을 바꿔 Li 석출·용해 거동을 조절"** — σ 최고(undoped 9.58)가 CCD 최저(0.9)라는 역상관. 과도핑(x≥0.05)에서는 "계면 이질성·구조 무질서·기계 취약(공간전하·dendrite 관통·경로 봉쇄)"의 시너지 실패로 분극 급증.
- 대칭셀(0.5 mA/cm²·0.5 mAh/cm²): undoped **~25 h부터 과전압 급증 → 전압 급락(~0 mV) = dendrite 관통 완전단락**. doped **~200 h 안정**, 말기 고전류 부반응으로 종료 — **passivation도 무한하지 않음**(저자 자인).
- **메커니즘 도식**(Fig 3h–j): undoped=dendrite 관통 / doped=Li 계면에 **LaCl₃(녹)+LiCl(적) 블록층** + **La⁰ 사이트가 Li의 질서 있는 석출 유도**[ref 39] + LaCl₃의 [LaCl₉] 1D 채널이 Li⁺를 통과시킴(Fig 3j 확대). 원문: "The suppression of dendrite growth is primarily attributed to the presence of other inorganic components, such as **LiCl and LaCl₃**" [refs 38,40]; "**the by-product LaCl₃** forms a crystalline lattice of edge-sharing [LaCl₉] trigonal prisms, creating one-dimensional channels that facilitate lithium-ion migration" (p.8). → §6에서 증거 수준 해부.

### 5.5 전기화학 창: "도핑해도 안 변한다" (Fig S8)
- CV 실측(SI 확인): **비대칭 Li/SE/SS(스테인리스) planar 셀, 0–5 V** — 두 곡선(LPSC vs La₀.₀₄)이 **사실상 겹침**: <~0.5 V 환원전류, ~3.3–3.7 V 부근 미세 산화 봉우리(둘 다, mA 이하). 본문 결론: **"the electrochemical stability window of the electrolyte does not exhibit a significant change after La-O co-doping"**.
- 근거 서술(본문): "SE의 안정창은 intrinsic 전자구조가 일차 결정 [ref 43] … La-O 공도핑은 LPSC의 밴드구조(CB·VB 위치)를 바꾸지 않는다 … 격자 일부 원자만 치환하므로 전체 전자구조 불변 → 창 확대 없음." ⚠ **아무 계산 없이 단언된 band-edge 논리**(우리 규율: band-edge≠분해 onset; [He19]·[Banik] 참조).
- 방법 감도 ⚠: **planar SS-CV는 분해를 과소평가하는 대표 지형**(Dewald가 비판한 carbon-free 셀) — "창 불변"은 조성 간 *상대* 비교로만 유효, 절대 창(0–5 V에서 조용함)을 intrinsic 안정으로 읽기 금지. 단 **관측 자체(dilute 도핑에 onset 불변)는 우리 S²⁻-limited grand-potential과 정합**(§11).

### 5.6 Full cell: 저율 열세·고율/장기 우세, DRT·XPS로 계면 귀속 (Fig 4·5)
- 1C 500cyc: 179.1→149.7(**83.6%**) vs 158.1→130.1(82.2%) — 초기용량·유지율 모두 doped 우위. 전압곡선(Fig S10): undoped는 사이클에 따라 충-방전 갭 확대(분극 누적) vs doped 안정. ⚠ 이 헤드라인 셀의 음극은 **Li-In 합금**(Li 금속 아님).
- EIS(100cyc@1C, 등가회로 R_b + 3×(R‖CPE) + W, Fig S11; Table S2): **R_ce 41.7→37.6 Ω·R_ae 39.9→27.7 Ω** — 양·음극 계면저항 모두 doped가 낮음. 부속값: R_b 13.2→**18.6 Ω**(벌크 — doped가 *높음*, σ 0.65×와 정합), R_gb 5.26→**1.92 Ω**, Warburg 22.4→10.9.
- Rate: **0.1C에선 undoped 우세(222.7>206.9)**, 0.5C부터 역전, 2C에서 **144.5>124.3**. 저자: 저율에서 undoped의 부반응 산물 누적이 이후 사이클을 갉아먹음 — 0.2C 실험으로 확인: 100cyc 후 **R_ce 191 vs 18.5 Ω(10×)**, R_ae 448 vs 171 Ω, 유지율 88.5 vs **94.4%**.
- 온도: 60 °C 0.5C 초기 231.76·30cyc 96.3%(문헌 동일구성 172.6 대비 우위) · −20 °C 0.1C 50cyc 148.4(활성화 경향).
- **DRT**(Fig 5, 100cyc 후 SOC/SOD 스캔): τ<10⁻⁵ s=벌크+GB(충전상태 무관) · 10⁻⁴–10⁻² s=**양극 계면** · 10⁻¹–10⁰ s=**음극 계면** · 10⁰–10¹ s=Li 확산. doped가 **양쪽 계면 피크 모두 축소**, 특히 양극 계면(upper-middle) 억제 뚜렷.
- **XPS**(Fig S15, 100cyc@1C NCM/SE 계면 = **양극**): undoped S 2p = PS₄³⁻ + **P₂Sₓ(164.2/163.4 eV) + Li₂Sₓ(162.9/161.9 eV)**, P 2p = PS₄³⁻+P₂Sₓ; doped S 2p = PS₄³⁻ + **"LaSₓ"** 성분(P₂Sₓ/Li₂Sₓ 피팅 없음), P 2p = PS₄³⁻만 → doped의 양극 부반응 억제. **🔑 "LaSₓ" = 논문 전체에서 유일하게 실측된 La-함유 계면종 — 그리고 그것은 음극이 아니라 양극이다.** (단 LaSₓ가 분해산물인지, SE 자체 LaS₄ 결합의 표면 신호인지 논문은 구분 안 함.) (⚠ 음극 XPS·La 3d·Cl 2p는 본문·SI 어디에도 없음 — §6.)

## 6. ⭐ LaCl₃ — 어떻게 생기고, 어디에 있고, Li와 닿으면 어떻게 되나 (주장 vs 증거)
> 사용자 핵심질문 정면 대응. **요지: LaCl₃는 (i) 전구체 아님, (ii) 합성 산물로 주장되지 않음, (iii) "cycling 중 Li 계면에서 in-situ 형성되는 by-product"로 주장됨 — 단 본문+SI 통틀어 직접 분광증거 0, 반응식 0. SI 정독(12 pp)으로 확정: 음극 계면 측정 자체가 존재하지 않는다.**

| 질문 | 논문의 답 | 증거 수준 |
|---|---|---|
| **전구체인가?** | ✗ — 전구체는 Li₂S·P₂S₅·LiCl·**La₂O₃** (§2.1). Cl원은 LiCl뿐 | 확정 (방법 절) |
| **합성 중 생기나?** | ✗ 주장 없음 — as-synthesized 벌크는 **La가 4b에 들어간 LaS₄ + PS₃O 고용체**(Rietveld, Fig 1b). x≥0.05 불순물 피크는 **미동정**("solubility limit"라고만; LaCl₃로 동정 안 함) | XRD/Rietveld (Fig 1a,b) — 단 Table S1은 La/O 좌표·U_iso·점유를 P/S와 동일·명목 고정한 템플릿(§5.1) → "고용체" 자체도 가정 성분 있음 |
| **언제/어디서 생기나?** | **Li 스트리핑/플레이팅 중, 전해질/Li-금속 계면에서 in-situ** — intro 가설 "doping La directly … could promote **in situ formation of a LiCl–La passivation layer** at the electrolyte/lithium metal interface"(p.2) + 결과 "**by-product LaCl₃**"(p.8) | **도식(Fig 3h–j) + 선행문헌 [38–40]** — 본문 자체 증거 없음 |
| **형성 반응식?** | **없음** — LaS₄ 격자 La + 전해질 Cl⁻가 어떻게 LaCl₃가 되는지 화학식 미제시 | n/a |
| **XRD/TEM/XPS 증거?** | 계면 LaCl₃의 **XRD ✗·TEM/EDS ✗·XPS ✗ — SI 포함 확정**. SI 전체 목록(S1 EDS·S2/S4/S6 EIS·S3/S5 Ea·S7 물·S8 CV·S9–S14 셀/EIS·**S15 XPS=양극 S 2p/P 2p만**·Table S1–S4)에 음극 계면 분석·**La 3d·Cl 2p 스펙트럼이 하나도 없다**. 유일한 실측 La-계면종 = **양극 계면 "LaSₓ"**(Fig S15b) — La–Cl이 아니라 La–S이고, 위치도 음극이 아니라 양극 | **없음 (본문+SI 확정)** → **LaCl₃-at-anode = 가설** |
| **(참고) 실측된 La 계면종은?** | **양극(NCM/SE) 계면의 "LaSₓ"** (Fig S15b, S 2p ~161 eV대 성분) — 단 분해 신생상인지 SE 자체 LaS₄ 결합의 표면 신호인지 미구분 | XPS 피팅 1건 (해석 이중성) |
| **Li와 닿으면 살아남나?** | **논문 스스로 부분 환원을 인정**: "lithium-induced **reduction of La³⁺ to La⁰** helps mitigate lithium dendrites"(p.2) · "formation of **La⁰ sites** at the interface, which effectively guide the ordered deposition of lithium"(p.7) · **결론(p.10): "La doping effectively mitigates dendrite formation by promoting the reduction of lithium and the formation of La and LiCl"** — 결론부의 passivation 성분은 **La(금속)+LiCl**이고 LaCl₃가 아님 | 원문 인용 (직접측정 아님) |
| **어디에 있나(공간)?** | **음극(Li/SE) 계면에만** 주장(Fig 3i·j: Li 위에 LaCl₃+LiCl 블록층, 그 안 [LaCl₉] 1D 채널로 Li⁺ 통과). GB·입자표면·**양극 계면 LaCl₃ 주장 없음** | 도식 |
| **역할 주장** | ① dendrite 억제(LiCl·LaCl₃ 계면 안정화 + La⁰ 유도 석출) ② [LaCl₉] 1D 채널(내경 ~4.6 Å)이 **O-도핑으로 잃은 σ를 고전류에서 보상** ③ "LaCl₃ 도입이 공공·결함 만들어 σ 향상"(p.8, 반복 서술) ④ (abstract) "passivation층의 기계적 성질이 dendrite 억제" — **기계 측정 0** | 서사 (분광·역학 증거 없음) |
| **소모/열화 관찰?** | 정량 없음. 단 doped 대칭셀도 **~200 h 후 부반응으로 종료**("prolonged cycling under high currents eventually led to side reactions as well") = passivation 비영구 자인 | Fig 3g |

**계보 노트**: "Li 접촉 → LiCl + La(금속)" 그림 자체가 ref 38(Yao Nature 2023, LTLC)의 **gradient passivation layer** 발견을 그대로 가져온 것이다 — Yao는 *순수 LaCl₃-계 SE*에서 Li 접촉면에 LiCl+La⁰가 생기고 그 바깥에 LaCl₃가 남는 구배층을 보고했다. 본 논문은 그 화학을 "황화물에 La를 도핑하면 같은 층이 in-situ로 생길 것"이라는 **전제**로 차용했고, 자기 시스템에서 재검증하지는 않았다.

## 7. 전체 논증 흐름
La₂O₃ 도핑(단일 전구체, x=0.04 상순수) → [비용] σ 9.58→6.23·Ea↑·σ_e 8.5×↑ → [이득 1: 대기] P–O/PS₃O가 가수분해 억제 → H₂S↓·노출후 σ 39×↑·500 °C 어닐 회복 43.5% → [이득 2: Li 계면] CCD 3.4×·대칭셀 25→200 h — CCD는 σ와 무상관 ⟹ 계면화학(La⁰·LiCl·"LaCl₃") 귀속 → [셀] 1C 500cyc 83.6%·저율 열세/고율·장기 우세·DRT/XPS로 계면저항·부산물 감소 확인 → 결론: "La는 dendrite(환원→La⁰+LiCl), O는 대기(P–O)" 분업.

## 8. DFT/계산 방법 ★
**전무 (계산 0).** code/functional/k/supercell/AIMD/MLIP/무질서 처리 전부 n/a.
- 이론적 주장들은 모두 **정성 서사**: Lewis 산성도(O)·이온반경(La³⁺ 1.06 Å)·HSAB류 결합논리(P–O>P–S)·TST 엔탈피–엔트로피 보상·band-edge ESW 논리(§5.5, 무계산 단언).
- 인용으로 때운 계산: 가수분해 억제 first-principles는 Zhang et al.[33](Sn 도핑), 계면 passivation은 refs 38–40. → **이 논문의 모든 원자단위 공백을 우리 DFT가 채울 수 있음**(§11·§12).

## 9. Figure set ★ (본문 Fig 1–5 + SI Fig S1–S15·Table S1–S4 전부 정독)
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | XRD 시리즈 (x=0–0.10; x≥0.05 ♦불순물) | RE₂O₃ 용해한계 (우리 Nd x=0.2 DFT는 실험 도핑농도의 ~5×임을 상기) |
| 1b | Rietveld (x=0.04, Rwp 4.14%) | 격자 팽창 +0.030 Å — 우리 Nd-doped 격자변화와 대조 가능 |
| 1c | 결정구조 모식 ((P,La)(S,O)₄ 사면체) | La@4b·O@PS₄ = 우리 O@PS₄ site-preference(−0.67 eV/O)와 동일 그림 |
| 1d,e | SEM (undoped/doped) | 입형 불변 — σ 차이가 미세구조 아님 방증 |
| 1f–h | σ 막대·Arrhenius·DC-pol | **σ-비용 정량**; σ_e 8.5×↑(⚠) |
| 2a | H₂S 곡선 (RH 50–55%) | doped 15 min 포화 = 표면 보호층 형성 시사 |
| 2b | 노출 후 XRD (미지 불순물) | 분해상 미동정 — 우리 hydrolysis hull로 후보 제시 가능 |
| 2c,d | 노출 전후 σ·Ea | **노출 후 σ 39× 우위·Ea 0.597 vs 1.099** |
| 2e,f | 어닐 온도별 회복·회복률 비교 | **43.5% vs 11.9%** — "구조 복원력" 지표 |
| 2g,h | 펠릿/분말 사진 | deck용 시각자료 |
| 3a–e | CCD 곡선 (조성별) | 화산형; x=0.04 최적 |
| 3f | CCD 요약 (0.9→3.1→2.0) | **CCD–σ 무상관** = interphase 지배 증거 |
| 3g | 대칭셀 0.5/0.5 (25 h vs 200 h) | ⚠ 캡션 오타 "LPSC-Sn₀.₀₈"(자기 그룹 Sn 논문 잔재) |
| 3h–j | 계면 도식 (dendrite vs LaCl₃+LiCl+[LaCl₉] 채널) | **주장의 전부가 이 도식** — 증거 아님(§6) |
| 4a | 1C 500cyc | 83.6% vs 82.2%·초기 +21 mAh/g |
| 4b | Nyquist 100cyc | R_ae 27.7 vs 37.6 Ω |
| 4c,d | 율속 프로파일·rate | **저율 열세·고율 우세** 교차 |
| 5a–d | DRT (SOC/SOD, 100cyc) | 4 시간영역 귀속; 계면피크 축소 — 우리도 DRT 귀속 어휘 차용 가능 |
| S1 | SEM+EDS 맵: (a) LPSC P/S/Cl, (b) doped **O/P/S/Cl/La** 균일 | 응집 없음 (단 O·La 신호 희미 — x=0.04 dilute) |
| S2 | RT Nyquist (x=0–0.10; x↑ 저항 증가, x=0.10 뚜렷) | σ 시리즈 원자료 |
| S3 | Ea 막대 (0.238/0.249/0.254/0.259/0.289 eV) | 단조 증가 확인 |
| S4 | 노출 후(RH 50–55%) Nyquist — LPSC ~35 kΩ 반원 vs doped ~10 kΩ대 | 노출 후 σ 39× 차 원자료 |
| S5 | 노출 전후 Ea 막대 (0.238→1.099 vs 0.254→0.597 eV) | 손상 정도 지표 |
| S6 | RH 40–45% 30 min 후 EIS (LPSC ~1.2 kΩ vs doped ~0.6 kΩ) | 저습도 손상도 |
| S7 | **수돗물 침지 사진 0–150 s** (undoped 격렬 용해 vs doped 형상 유지) | 시각 증거 (deck) |
| S8 | **CV, 비대칭 Li/SE/SS planar, 0–5 V — 두 곡선 사실상 겹침** | "창 불변" 관측 확정; ⚠ planar SS=저감도 kinetic (절대창 해석 금지) |
| S9 | LiNbO₃@NCM712/La₀.₀₄/**Li 금속**, 0.5C, **3.0–4.2 V**, 100cyc 125.5→87.6 (69.8%) | **유일한 진짜 Li-금속 full cell** — 헤드라인(500cyc 83.6%)은 Li-In |
| S10 | 1C 1/100/300/500th 충방전 곡선 | undoped 분극 확대 vs doped 안정 |
| S11 | 등가회로 R_b+(R_gb‖CPE1)+(R_ce‖CPE2)+(R_ae‖CPE3)+W | EIS 5성분 정의 |
| S12 | 0.2C 100cyc + fresh/cycled EIS | cycled 반원 LPSC ≫ doped (Table S3: R_ce 191→18.5) |
| S13 | 60 °C 0.5C (**초기 CE 88.5%**·30cyc 96.3%) · −20 °C 0.1C (**초기 CE 67.5%**) | 온도창; −20 °C 초기 비가역 큼 |
| S14 | in-situ EIS (SOC/SOD 전압별, 100cyc 후) | DRT(Fig 5) 원자료 |
| S15 | **cycled 양극(NCM/SE) XPS S 2p·P 2p**: LPSC=PS₄³⁻+P₂Sₓ+Li₂Sₓ vs doped=PS₄³⁻+**"LaSₓ"** | **음극 아님·La 3d 없음** — LaCl₃ 증거 부재의 핵심(§6); LaSₓ=유일 실측 La 계면종 |
| Table S1 | Rietveld 좌표표: **La=P1 좌표·U_iso 동일·frac 0.04 고정 / O=S2 동일·0.06 고정**; Li 48h 0.5; Cl 4a 0.385/4d 0.615; Rp 5.76/Rwp 4.12/a 9.823930 | **자리 "가정" 증거**(§5.1 판정); 본문 수치와 불일치 |
| Table S2 | 1C 100cyc EIS: R_b 13.2/18.6·R_gb 5.26/1.92·**R_ce 41.7/37.6·R_ae 39.9/27.7**·W 22.4/10.9 | 본문 문장의 모호한 나열을 확정하는 원표 (⚠ 표제 "…/Li batteries"지만 실제 Li-In) |
| Table S3 | 0.2C 100cyc EIS: R_ce **191/18.5**·R_ae **448/171**·R_gb 38.9/9.46 | 저율 부반응 누적의 정량 |
| Table S4 | 성능 자기비교: **NCM712/La₀.₀₄/Li = 100cyc 69.8%** vs NCM955/La₀.₀₄/**Li-In** = 500cyc 83.6%; 비교 문헌 = SeS₂-doped [Kim 2023 EA 442,141869]·**Nb-O-doped Cl-rich [S.L.Li 2025 EA 509,145341 — 같은 그룹 자매편]** | Li-금속 헤드라인의 실체 + 그룹 M-O 도핑 시리즈 확인 |

## 10. Post-processing ★
- **Rietveld**: 격자상수·자리배치(소프트웨어 미명시). 기록 = a, Rwp/Rp.
- **EIS→σ/Ea**: 0.1 Hz–2 MHz, RT–70 °C Arrhenius. 노출 전/후·어닐 후 반복 = **"σ retention %"를 안정성 지표로 수치화** (43.5/11.9/10.3%) — 우리도 문헌비교 시 이 지표 채용 가치.
- **DC 분극**: 0.5 V·3600 s → σ_e.
- **H₂S 부피**: cm³/g vs 시간 (RH·시간 명시) — 절대값은 프로토콜 의존([Taklu] Li₆PS₅Cl 1.07 cm³/g과 직접 비교 금지).
- **CCD**: 전류 계단상승 대칭셀, 급락점=CCD.
- **EIS 5성분 등가회로**(R_b/R_gb/R_ce/R_ae/Z_w) + **DRT**(γ(τ), 도구 미명시): τ 영역별 벌크/GB/양극계면/음극계면/확산 귀속 — **SOC/SOD 스캔과 결합해 "어느 계면이 언제 나빠지나"를 분해**. 우리 그룹 실험([KimICCF] 등)과 접점.
- **XPS**: S 2p/P 2p 피크 귀속(P₂Sₓ 164.2/163.4·Li₂Sₓ 162.9/161.9 eV) — 우리 `xps_reference_sei.csv` 앵커와 정합군.

## 11. 우리 DFT 대비 (comp1/modelc/Nd₂O₃) → `../our_dft_baseline.md`
> 총평: **이 논문 = 우리 Nd₂O₃-doped modelc의 "La 버전" 실험 평행선.** 정합 3·긴장 2·우리가 채울 공백 3.

| 항목 | Yang (exp) | 우리 (DFT/MLIP) | 판정 |
|---|---|---|---|
| Host | Li₅.₅PS₄.₅Cl₁.₅ (Cl 1.5) | modelc Li₅.₄PS₄.₄Cl₁.₆ (Cl 1.6) | ≈ 같은 Cl-rich 급 (동일시 금지) |
| 도핑 | **La₂O₃**: La→**4b(P자리)**+2Li, O→PS₄ | **Nd₂O₃**: Nd→**Li 부격자**(3Li→Nd), O→PS₄(−0.67 eV/O 선호) | **패밀리 동일(RE³⁺+O), 자리 다름(P vs Li)** — 자리배치는 양쪽 다 확증 부족(그들 lab-XRD Rietveld만·우리 모델 선택). [Liu23] Mg@P 논쟁과 동형 |
| σ 비용 | 9.58→6.23 mS/cm (**0.65×**), Ea 0.238→0.254 (+0.016 eV) | Nd: σ300 **0.52×**·D 0.62×, Ea 0.224→0.227 (**불변**) | **✓ 같은 방향(RE-O 도핑=σ 희생)**. 미시분해는 다름: Yang은 Ea↑로 절반 이상 설명(exp(−ΔEa/kT)≈0.54× ≈ 관측 0.65×), 우리는 **prefactor/connectivity blocking**(Ea 불변) — 자리(P vs Li)·농도 차이의 반영 가능. 절대값 비교 금지(EIS vs MLIP-AIMD) |
| ESW/CV | "도핑 후 창 불변"(Fig S8 = **Li/SE/SS planar CV 0–5 V, 곡선 겹침**; band-edge 논리로 무계산 단언) | dilute 도핑 대부분 onset 2.14/2.256 V pin(S²⁻-limited); **단 nd intrinsic 창은 오히려 축소**(1.52–1.92 vs 1.24–2.14 V) — 산물이 wide-gap이라 kinetic passivation으로 벌충 | **△ 관측은 정합·논리는 부정합**: "창 불변" 관측 = S-pin과 결. 그러나 **planar SS-CV는 분해 과소평가 지형(저감도)**이라 RE-redox 미세단차(우리 1.92 V Nd-sulfide 산화 등)를 원리적으로 못 분해; "밴드구조 불변→창 불변" 추론은 band-edge 오류([He19]·[Banik] 규율) |
| **음극 RECl₃** | **LaCl₃가 Li 계면 by-product**로 형성·잔존 주장(도식) **+ La³⁺→La⁰ 환원 병기** + 결론은 "**La and LiCl**" | **NdCl₃는 V=0에서 불가능**: hull staircase V=0 → 0.3Li₂O+0.8Li₃P+4.1Li₂S+**0.2NdP**+1.6LiCl (NdCl₃ 없음); NdCl₃+3Li→3LiCl+Nd 치환 발열(~−1 eV급); **NdCl₃는 ≥2.62 V 산화 산물로만** 출현(gap 4.30) | **🔑 심층 화해 — §11b** |
| 대기안정 P–O | P–O가 P–S보다 강함·PS₃O=물리흡착(정성, ref 인용) | **ICOHP P–O −8.43 vs P–S −5.98 (+41%)**·O@PS₄ site-preference **−0.67 eV/O**·500 K AIMD서 P–O 자발형성 | **✓✓ 우리가 그들 주장의 원자단위 정량판** — 상호 인용 가치 최고 지점 |
| σ_e | 2.59e-9→**2.2e-8 (8.5×↑)** 인데 CCD 3.4×↑ | 우리 실험쪽 Nd-doped는 σ_e↓(3.45→2.33e-10 mS/cm @x=0.02); sei_products 논리 = 전자절연 SEI가 dendrite 레버 | **⚠ 긴장**: [Taklu]/[Li25] "σ_e↓→CCD↑"와 역방향 — Yang은 bulk σ_e 올라도 **계면 interphase(LiCl/La⁰)가 지배**함을 시사. "bulk σ_e만으로 CCD 못 예측" 사례로 기록 |
| 셀 성능 | 1C 500cyc 83.6%·CCD 3.1·60 °C 96.3% | (범위 밖 — 우리 DFT 무대상) | 실험 인용용 |

### 11b. ⭐ LaCl₃(그들) vs NdCl₃(우리 hull 지도) — 정면 대조 (2026-07-14, `tools/oxidation/esw_nd_result.txt`·`kb/results/nd_anode_cathode_sei_formation_2026_06_24.md`)
우리 6원소(Cl-Li-**Nd**-O-P-S) grand-potential 지도의 판정:
1. **환원측(Li 접촉, V→0): RECl₃ 열역학적 불가** — V=0 산물에 NdCl₃ 없음(NdP+LiCl+Li₂S+Li₂O+Li₃P); Li가 RECl₃를 치환(NdCl₃+3Li→3LiCl+Nd⁰). Nd는 0–1.28 V에서 **전도성 NdP/NdP₅/NdPS**, ≥1.52 V에서 Nd₂S₃.
2. **산화측: NdCl₃는 ≥2.62 V에서만** (NdPO₄ 2.45 V·LiNd(PO₃)₄ 3.08·Nd(PO₃)₃ 3.66 V와 함께 wide-gap 전자차단 passivator, NdCl₃ gap 4.30 eV).

이 지도로 Yang의 주장을 읽으면:
- **정합 ①**: Yang의 **결론 문장 자체("the formation of La and LiCl")와 La³⁺→La⁰ 환원 인정** = 우리 치환반응(RECl₃+3Li→3LiCl+RE⁰)의 산물과 **정확히 동일**. 즉 **논문의 데이터가 실제로 지지하는 음극 화학은 우리 지도와 일치**한다(La⁰+LiCl).
- **정합 ②**: 합성 중 LaCl₃ 형성 주장 없음(벌크=LaS₄/PS₃O 고용체) → "합성-형성 RECl₃가 음극에 미리 존재" 시나리오는 **이 논문에선 성립하지 않음** — 우리 지도와 충돌할 여지 자체가 없다.
- **긴장(유일)**: **"LaCl₃가 Li 계면에 잔존하며 [LaCl₉] 1D 채널로 기능"** 도식은, LaCl₃가 **Li와 직접 접촉**하는 그림이라면 우리 지도(즉시 3LiCl+La⁰로 치환)와 모순. **화해 경로 = gradient SEI**(ref 38 Yao의 원래 그림): Li 직접접촉면은 La⁰+LiCl, **국소전위가 올라간 바깥층에만 LaCl₃ 잔존** — 이 배치는 우리 staircase(높은 V에서 RECl₃ 안정)와 양립. Yang은 이 공간 구배를 **측정하지 않았고, SI 정독으로 음극 계면 측정 자체가 없음이 확정**(§6) → **"LaCl₃가 음극 보호층" 주장은 미검증 차용(가설)**으로 분류.
- **비대칭 관찰 + 유일 실측 La 계면종**: 우리 지도의 **양극측 RECl₃(≥2.62 V)**는 Yang이 전혀 다루지 않음. 대신 논문의 유일한 실측 La 계면종은 **양극 계면의 "LaSₓ"**(Fig S15b) — 흥미롭게도 우리 nd staircase에서 **양극 저전압 구간(1.92–2.45 V)의 산화 경로가 정확히 RE-황화물**(Nd₁₀S₁₉/NdS₂/NdPS₄)이고 RE-인산염/염화물(NdPO₄ 2.45/NdCl₃ 2.62 V)은 그 위 전압에서만 나온다. 즉 **"양극 계면에서 La–S 종이 보인다"는 관측은 우리 RE-sulfide 산화 분지와 방향 정합**(단 LaSₓ가 신생 분해상인지 SE 자체 LaS₄ 표면신호인지 논문 미구분 → 약한 정합으로만). **La 3d 양극 XPS(≥2.6 V 구간 충전 상태)를 찍으면 우리 지도의 신규 예측(RECl₃=양극 산물) 검증 가능** = 협업/후속 제안 포인트.
- ⚠ **정직 한계**: 우리 hull은 **Nd 전용**(La 미포함 chemsys). La³⁺(1.06 Å)≈Nd³⁺(0.98 Å)·같은 RE³⁺ 염화물/산화물 안정성 패밀리라 **화학 유추는 강하나 정량 이식은 금지** — La-hull(Cl-Li-**La**-O-P-S)을 돌리면 문장 그대로 검증 가능(MP에 LaCl₃/LaPO₄/La₂S₃/LaP 전부 있음). 후속 계산 1순위.

## 12. 적용 인사이트
1. **"실험 자매편" 확보**: RE₂O₃(La) 도핑 Cl-rich argyrodite가 **σ 0.65×를 감수하고 CCD 3.4×·대기안정·500cyc 83.6%를 얻는다** — 우리 Nd₂O₃ cascade의 "σ-비용 vs interphase-이득" 프레임이 실험으로 실증된 최근접 사례. deck에서 "우리 계산 설계와 같은 논리의 실험이 이미 성공(La)"으로 인용.
2. **우리 hull이 이 논문의 빈칸을 정확히 채움**: (a) P–O 대기안정의 원자 정량(ICOHP·site-preference), (b) 음극 RECl₃ 불가/La⁰+LiCl 필연(그들 결론과 일치), (c) **양극 RECl₃(≥2.6 V) 신규 예측** — La 3d XPS 한 장이면 검증되는 falsifiable 제안.
3. **CCD–σ 무상관 + σ_e 8.5×↑에도 CCD↑** = "dendrite 레버는 bulk 수송이 아니라 interphase 화학" 의 또 하나 실험증거 — 단 [Taklu]/[Li25] σ_e 서사와 역방향이므로 "σ_e는 필요조건이지 결정변수 아님"으로 어휘 교정.
4. **자리 문제(La@4b vs Nd@Li)**: 그들 근거는 격자팽창+**명목-고정 Rietveld 템플릿**(Table S1: La=P1 좌표·U_iso 동일·frac 고정)뿐 — 우리 site-preference 머신(P-site vs Li-site swap 에너지)으로 **La 도핑 자리를 계산 판정** 가능([Liu23] Mg 자리 논쟁과 동일한 under-determined 상황). P–O/PS₃O도 분광증거 0(O 1s·Raman 부재) → 우리 ICOHP·site-preference가 사실상 유일한 원자단위 근거.
5. **어닐 회복률(%)이라는 지표**: 노출→어닐 σ retention(43.5 vs 11.9%)은 "가역 물리흡착 vs 비가역 가수분해"를 가르는 실험 지표 — 우리 hydrolysis 산물 hull(P–O 잠금)과 연결하면 "왜 O-doped만 되돌아오나"를 설명하는 그림 하나가 나옴.
6. **그룹 M-O 공도핑 시리즈의 한 칸**: 같은 그룹(HUST Chuang Yu)의 Sn-O[ref15]·Sb/Bi-O[refs34,35]·**Nb-O**(Table S4 ref2, Electrochim. Acta 509, 145341)·**La-O**(본편) — "금속+O 공도핑" 실험 시리즈가 이미 존재. 우리 Nd₂O₃는 이 시리즈의 **4f-희토류 칸 + 열역학 지도(hull)라는 그들에게 없는 층**을 채운다([Bai] 리뷰 "metal+O cooperate" 처방과도 정합).

## 13. 인용 가능 문장 (deck/paper용)
- "Yang et al. (Electrochim. Acta 2025) provide the closest experimental sibling to our Nd₂O₃ design: La₂O₃ co-doping of a Cl-rich argyrodite trades ~35% of σ for P–O-bond air stability and a Li-interface passivation (CCD 0.9→3.1 mA/cm², 500 cycles at 83.6%)."
- "Their own conclusion — dendrite mitigation 'by the formation of **La and LiCl**' upon Li contact — is exactly the Li-displacement chemistry our grand-potential map predicts for RECl₃ (NdCl₃ + 3Li → 3LiCl + Nd); the surviving-LaCl₃ layer they sketch is only viable as the outer, higher-potential part of a gradient SEI, never in direct Li contact."
- "Our map adds a falsifiable prediction they did not test: RE chlorides re-appear as **oxidation** products (NdCl₃ ≥ 2.62 V) — one La 3d XPS scan of their cycled cathode would decide it."
- "Their observed CCD increase despite an 8.5× rise in bulk σ_e shows bulk electronic conductivity alone does not set dendrite resistance — interphase chemistry does."
- "Across the full SI there is no anode-side XPS, no La 3d, no Cl 2p: the LaCl₃-at-the-anode layer is a hypothesis imported from LaCl₃-electrolyte literature, while the paper's only measured La-containing interphase species is a La–S component at the cathode (Fig S15b) — directionally matching the RE-sulfide oxidation branch of our hull (Nd-S phases at 1.92–2.45 V) rather than an anode chloride."

## 14. 주의/한계 (over-claim 방지)
- **계산 0 + 음극 interphase 실측 0(본문)**: LaCl₃/La⁰/[LaCl₉] 채널 서사는 **도식+refs 38–40 차용**. "Yang이 LaCl₃ SEI를 증명"이라고 인용 금지 — "주장/도식"으로만.
- **PS₃O 유닛 직접증거 없음(본문)**: P–O 결합은 Rietveld 격자+화학량론+선행문헌 추론. XPS O 1s/P 2p·Raman·³¹P NMR 부재(SI 미확인). "PO₄ 단위"는 아예 등장 안 함 — **oxysulfide PS₃O(x=0.04, O 0.06/f.u. = S 자리의 1.3%)** 수준.
- **CV 창 "불변"**: 수치·전극구성·스캔속도 n/a(Fig S8, SI 미보유). band-edge 논리로 무계산 단언 — 관측만 취하고 논리는 버릴 것.
- **σ_e 8.5× 증가를 "여전히 낮다"로 처리** — La³⁺ 4f⁰라 gap-state 우려는 적으나 측정상 분명한 악화. 이를 CCD·σ 논의에 연결하지 않음.
- **abstract "passivation층의 기계적 성질이 dendrite 억제"** — 기계 물성 측정 전무(nanoindentation·모듈러스 0).
- **편집 완성도**: Keywords "**Choline**-rich argyrodite"(Chlorine 오타)·Fig 3g 캡션 "LPSC-**Sn₀.₀₈**"(자기 그룹 Sn 논문[ref 15] 잔재)·p.8 LaCl₃ 채널 문단 사실상 동일 문장 3회 반복 — 검증 부담이 낮은 저널 프로세스였음을 시사, 수치는 교차확인된 것만 신뢰.
- **H₂S 절대값 프로토콜 의존**: RH 50–55%·30 min·cm³/g — [Taklu](1.07→0.49)와 습도·시간·셀부피 달라 절대 비교 금지.
- **저율(0.1C) 성능은 undoped가 우위** — "전면 우위" 아님; 이득은 계면·장기·고율에 국한.
- **σ 하락의 조성 의존이 가파름**: x=0.05부터 2차상+σ 급락 — 실험 용해한계(x~0.04–0.05)는 우리 DFT x=0.2보다 4–5× 낮음. 우리 결과를 실험 스케일로 말할 때 항상 환기.
- SI 미보유: S-피규어 수치는 본문 인용문 한정. Table S4(문헌비교) 내용 n/a.

## 15. 기법 용어 미니사전
- **CCD (critical current density)**: 전류 계단상승 대칭셀에서 전압 급락(단락) 직전 전류밀도 — dendrite 내성 지표.
- **DRT (distribution of relaxation times)**: EIS를 τ-공간 γ(τ)로 역변환해 중첩된 저항 프로세스를 시간상수별로 분해 — 여기선 벌크/GB(<10⁻⁵ s)·양극계면(10⁻⁴–10⁻² s)·음극계면(10⁻¹–10⁰ s)·확산(10⁰–10¹ s) 귀속.
- **DC 분극(σ_e)**: 정전압(0.5 V) 인가 후 정상상태 잔류전류로 전자전도도 추출(이온 차단).
- **H₂S 테스트**: 습윤공기 노출 시 발생 H₂S 부피(cm³/g) — 황화물 가수분해 정도.
- **엔탈피–엔트로피 보상**: ΔG‡=ΔH‡−TΔS‡에서 ΔH‡↑와 ΔS‡↑가 상쇄돼 겉보기 Ea 불변 — 여기선 P–O(ΔH↑)·격자왜곡/공공(ΔS↑) 서사.
- **[LaCl₉] 1D 채널**: UCl₃형 LaCl₃ 구조의 9배위 La-Cl trigonal prism이 c축으로 edge-sharing → 내경 ~4.6 Å 1D 터널(Yao Nature 2023이 Ta⁵⁺ 도핑+La 공공으로 Li⁺ 전도 활성화).
- **gradient SEI**: 전위 구배를 따라 층상 조성이 바뀌는 계면층 — Li 접촉면(0 V)엔 금속/이원 환원상(La⁰·LiCl), 바깥(높은 국소전위)엔 모상 잔존(LaCl₃).
- **ZrO₂@NCM955**: ZrO₂ 코팅 고니켈 양극 — 물리 배리어 + 격자 O 포획(→Li₂ZrO₃) 이중 기능.
