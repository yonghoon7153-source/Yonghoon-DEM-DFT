# Boosting Solid-State Diffusivity and Conductivity in Lithium Superionic Argyrodites by Halide Substitution — Adeli et al. (Angew. Chem. Int. Ed. 2019)

> slug `adeli2019_halide_substitution_boosting_argyrodite` · DOI `10.1002/anie.201814222` (German edn 10.1002/ange.201814222) · type `exp (중성자 Rietveld + EIS + ⁷Li PFG/MAS NMR; 자체 DFT/MD 0 — ⚠ 사용자 분류 폴더는 'DFT'이나 본문 계산 없음)` · PDF 본문 = 업로드 `82ea256b/68956c35`(6 pp, inbox #33, 사용자 분류 `DFT`) + **SI = `82ea256b/7c048d8a` ≡ `inbox/33. Sup)…pdf`(파일 14 pp = 내부 번호 1–12 + Wiley 표지·기여 2 pp) — 본문·SI 전문 정독 + SI 실물 감사 2026-07-28 완료(§3f: Table S1–S3 전값 일치, 사용자 분류 `DFT`)** · digested `2026-07-28` · status ✅
> elements: Li, P, S, Cl, Br
> methods: impedance-spectroscopy, neutron-diffraction, Rietveld, PFG-NMR, MAS-NMR, Haven-ratio, EDX, CV
> **저자**: Parvin Adeli⁺, J. David Bazak⁺(공동 1저자), Kern Ho Park, Ivan Kochetkov, Ashfia Huq, **Gillian R. Goward***, **Linda F. Nazar*** (Univ. Waterloo Chemistry/WIN · McMaster Univ. · ORNL SNS Neutron Scattering Division) · Angew. Chem. Int. Ed. **2019**, 58, 8681–8686. Received 2018-12-14 / accepted 2019-04-30 / online 2019-05-23. 지원: BASF Battery Network·NSERC·CRC(Nazar); SNS(DOE). **[외부]** (Waterloo Nazar 그룹).

---

> [!note] 현장 판단 병기 (2026-07-28, 사용자)
> "LPSCl1.6은 기업에서도 널리 쓰는 배합" — 이 논문의 고용한계(x=0.5 end member, x=0.6 LiCl 석출·3.3 mS/cm)는
> **이 논문의 550 °C 고상 공정 한정**으로 읽을 것 (사용자 평: 한계 서술은 다소 과장). 후속 문헌(박막/RTA/Nazar 2024,
> Cl 1.6–1.7에서 10.8–17 mS/cm)도 같은 방향. → modelc(Cl1.6) 정당성: 산업 표준 배합의 계산 모형.

## 0. 이 digest를 읽는 법 (왜 2순위였나)
이 논문은 **halogen-rich 아지로다이트 Li₆₋ₓPS₅₋ₓCl₁₊ₓ 고용체의 실험 원전**이자, **Li₅.₅PS₄.₅Cl₁.₅(x=0.5)의 중성자 TOF Rietveld 점유율 원본**이다. 우리에게 세 가지가 걸려 있다:
1. **modelc(Li₅.₄PS₄.₄Cl₁.₆) 셀의 실측 ground truth** — 4a/4c 자리별 S²⁻/Cl⁻ SOF·Li 48h 점유·좌표·격자상수의 유일한 halogen-rich 중성자 정련값(§3a). 우리 Cl-rich 셀 decorate가 옳은지 이 표로 판정한다.
2. **σ 9.4 mS/cm의 정확한 조건**(cold-press 2 t·298 K·total·In 블로킹; 소결 12.0) — litdb 곳곳에 재인용되는 그 수치의 원출처·방법 조건(§3b).
3. **⚠ 우리 modelc 조성(Cl 1.6) = 이 논문의 x=0.6 = 고용한계 *밖*** — 이 합성(550 °C·5–7 h)에서는 LiCl 석출로 σ 3.3 mS/cm까지 떨어진다(§5.3). "Cl 1.6 단일상"은 공정 의존적 가정임을 이 원전이 직접 보여준다.

**핵심 발견 한 문장**: Cl⁻/S²⁻ 비를 높이면(x 0→0.5) (i) 2가 S²⁻→1가 Cl⁻ 치환으로 **Li–골격 정전 상호작용 약화**(⁷Li 화학이동이 "LiCl-like"로 이동), (ii) **Li 공공 증가**(48h 점유 0.5급→0.456), (iii) **자리 무질서 증가**(S자리 Cl 점유 61→83 %)가 겹쳐 **Ea 0.34→0.29 eV·σ 2.5→9.4 mS/cm(약 4×)·D(PFG) LGPS의 ~5배**가 되고, Haven ratio 0.3→0.23 하락은 **공공 매개 협동(correlated) 이동 강화**를 가리킨다. 고용한계는 x=0.5(= Li₅.₅PS₄.₅Cl₁.₅가 end member).

## 1. 한 줄 요약
Li₆₋ₓPS₅₋ₓCl₁₊ₓ (x≤0.5) 고용체를 만들고 중성자 Rietveld + EIS + ⁷Li PFG/MAS NMR 3축으로, Cl-rich화가 **정전 약화 + Li 공공 + 자리 무질서**의 3중 기작으로 Li⁺ 확산·전도를 체계적으로 끌어올림을 실증 — **Li₅.₅PS₄.₅Cl₁.₅: cold-pressed 9.4±0.1 mS/cm(298 K, total)·소결 12.0±0.2·Ea 0.29 eV·D*(300 K)=1.01×10⁻¹¹ m²/s·H_R 0.23** — 단 x>0.5는 LiCl 석출로 역효과(x=0.6=우리 modelc 조성은 3.3 mS/cm).

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 계 | **Li₆₋ₓPS₅₋ₓCl₁₊ₓ**, x = 0, 0.25, 0.375, 0.5 (+한계 시험 0.55, 0.6) — 전부 F4̄3m cubic argyrodite |
| 질문 | Cl⁻/S²⁻ 비(=음이온 전하·Li 공공·무질서)를 올리면 Li⁺ 수송이 어떻게·왜 변하나 |
| 선행 맥락 | Li₆PS₅Cl 1.9 mS/cm(Rao/Adams)·용액법 10⁻⁵–10⁻⁴·혼합음이온 2.4–3.9·장기어닐 5 mS/cm; Deiseroth ⁷Li 모셔널내로잉; **de Klerk MD**(ref 24): 3종 점프(doublet 48h–24g–48h / intra-cage 48h–48h / **inter-cage=장거리 율속**), 무질서가 inter-cage에 유리, 이론조성 Li₅PS₄X₂(4a·4c 전부 할라이드) 제안 — 단 "**할로겐 증량은 σ를 크게 안 바꾼다**(X=Cl,Br)"가 그 MD의 결론이었고, 본 실험이 이를 **4× 증가로 뒤집음** |
| 방법 3축 | (1) 구조 = **중성자 TOF Rietveld**(x=0.5) + 랩 XRD 전 시리즈; (2) 전도 = **EIS**(cold-press·소결·VT·195 K); (3) 미시 동역학 = **⁷Li PFG NMR(D*)** + **MAS NMR(화학이동)** + **Haven ratio(H_R=D*/D_σ)** |
| **계산** | **자체 계산 0** — MD/DFT/BVSE 없음. 이론은 de Klerk ref 24 인용뿐(§8) |
| 후속 맥락 | 같은 Nazar 그룹이 2024년 Li₅.₃PS₄.₃Cl₁.₇(σ 11.4 mS/cm)까지 확장(litdb survey ⚠ PDF 미보유) — 2019 시점 "x=0.5 end member"는 *이 공정 조건*의 한계였음 |

## 3. 핵심 물성 (수치 총정리)

### 3a. ★ 중성자 Rietveld 원본 (Table 1) — 우리 modelc 셀의 실측 ground truth
**시료 = Li₅.₅PS₄.₅Cl₁.₅ 명목 조성. POWGEN(SNS, ORNL) TOF, 298 K(25 °C), 바나듐 캔. 공간군 F4̄3m, a = 9.8061(1) Å. GOF 3.37, R_wp 4.88 %. 부수상 LiCl 1.7 wt%. 정련 조성 = Li₅.₄₇PS₄.₅₅Cl₁.₄₅ (명목과 거의 일치; EDX Cl/P 1.51도 부합).**

| Atom | Wyckoff | x | y | z | **SOF** | U_iso [Å²] |
|---|---|---|---|---|---|---|
| Li | **48h** | 0.3173(7) | 0.3173 | −0.0201(9) | **0.456(16)** | **0.075(4)** |
| P | 4b | 1/2 | 1/2 | 1/2 | 1 | 0.030(2) |
| Cl1 | **4a** (0,0,0) | 0 | 0 | 0 | **0.615(17)** | 0.029(1) |
| S1 | 4a | 0 | 0 | 0 | 0.385(17) | 0.029(1) |
| Cl2 | **4c** (¼,¼,¼) | 1/4 | 1/4 | 1/4 | **0.834(16)** | 0.037(1) |
| S2 | 4c | 1/4 | 1/4 | 1/4 | 0.166(16) | 0.037(1) |
| S3 | 16e | 0.1188 | −0.1188 | 0.6188 | 1 | 0.050(1) |

- **Li는 48h 단일 자리만 점유**(24g 미포함 — 정련이 48h만 요구; §14 한계). 48h×0.456 = 21.9 Li/cell = **5.47 Li/f.u.** → 명목 5.5와 정합 = **Li 공공이 실측으로 확인**.
- **Li U_iso 0.075 Å² (대형)** = Li 고이동성의 변위 파라미터 신호 (본문 명시).
- **총 Cl = 0.615+0.834 = 1.449/f.u.** → 정련 조성 Cl 1.45.
- **Fig 2 비교 (vs Li₆PS₅Cl, ref 23 = Kraft 2017)**: 4a: Cl 0.385→**0.615** / 4c: Cl 0.615→**0.834**. 추가 Cl은 두 자리에 고루 분배되되 **4c(S²⁻ 자리)를 더 채움**. 저자 정의 "site disorder = S²⁻ 자리의 Cl 점유율" = **61 %(x=0) → 83 %(x=0.5)**.
- **자리 라벨 매핑 주의**: 이 논문의 **4c(¼,¼,¼) = Kraft/de Klerk 계열 문헌의 4d**(설정 차이). Adeli가 인용한 Li₆PS₅Cl 4c-Cl 0.615는 우리 kraft2017 digest의 "4d 무질서 ~62 %"와 **정확히 일치** → 두 digest 교차검증 통과. (Liu2022의 자체 Rietveld는 같은 LPSCl인데 4d 무질서 13.3 % — **무질서 자체가 합성 의존 변수**라는 우리 논지의 실례.)
- **[deklerk2016]과의 분배 대조** (같은 날 digest, `deklerk2016_diffusion_site_disorder_argyrodite.md`): de Klerk AIMD의 Li₆PS₅Cl 최적 Cl 분배 = 4a:4c=1:3(총 Cl의 75 %가 4c). **실측**: x=0(Kraft) 총 Cl의 61.5 %가 4c / x=0.5(Adeli) 57.6 %(=0.834/1.449)가 4c — 실측 분배는 50:50과 이론 최적(75 %) 사이. 즉 실험 합성물은 de Klerk 최적점에 미달인 채로도 9.4 mS/cm — 분배 튜닝 여지가 남아 있다는 독해 가능(단 75 %는 Cl1.0·450 K·단일배열 조건부 값).
- **Li 가시성**: 중성자는 x=0.5 **한 조성만**. 나머지 시리즈(x=0.25/0.375/0.55/0.6)는 **랩 XRD(Cu Kα, 모세관)** — 격자상수·상순도만, **Li/SOF 정보 없음**(X-ray는 Li 사실상 비가시).
- Rietveld 제약(SI): S1/Cl1(및 S2/Cl2) 좌표·ADP 동일 고정, Occ(S)+Occ(Cl)=1, 4b·16e occ=1, **Li 48h occ·ADP는 무제약 자유 정련**, 이후 전 파라미터 동시 정련. GSAS II. 시작 모형 = Rayavarapu Li₆PS₅Cl.

### 3b. 이온전도도·활성화에너지 (Table 2 전체 — cold-press 2 t, 298 K, **total σ**)
| 조성 (x) | σ(tot) [mS/cm] | Ea(EIS) [eV] ±0.01 | Ea(PFG) [eV] |
|---|---|---|---|
| Li₆PS₅Cl (0) | 2.5(1) | 0.34 | 0.35(1) |
| Li₅.₇₅PS₄.₇₅Cl₁.₂₅ (0.25) | 4.2(2) | 0.33 | 0.343(9) |
| Li₅.₆₂₅PS₄.₆₂₅Cl₁.₃₇₅ (0.375) | 5.6(2) | 0.31 | 0.320(3) |
| **Li₅.₅PS₄.₅Cl₁.₅ (0.5)** | **9.4(1)** | **0.29** | **0.29(1)** |
| Li₅.₅PS₄.₅Cl₁.₅ **소결**(550 °C 10 min) | **12.0(2)** | — | — |
| Li₅.₄₅PS₄.₄₅Cl₁.₅₅ (0.55) | 5.9(2) | N/A | — |
| **Li₅.₄PS₄.₄Cl₁.₆ (0.6) = 우리 modelc 조성** | **3.3(1)** | N/A | — |

- **9.4 mS/cm의 정확한 조건**: 분말 **cold-press 2 metric tons·2 min·⌀10(9) mm**, 펠릿 밀도 **이론의 87±1 %**, **In 호일 블로킹 전극**, VMP3, 1 MHz–0.1 Hz, **298 K**(본문 "25 °C", SI 초록 "300 K" 혼용). RT에서는 CPE/R 반원이 분석기 대역(>1 MHz) 밖 → **Warburg 꼬리 직선 외삽의 실수축 절편으로 R 결정**. **bulk/GB 분리 안 됨 = total σ** (195 K에서도 분리 실패, SI 명시). 시료 4계열(A–D) 반복으로 표준편차 산출(Table S2: 9.4/9.3/9.5/9.4 → 9.4±0.1).
- x=0 기준값 2.5 mS/cm는 문헌 범위(1.1–3.15)와 정합 → 시리즈 신뢰. σ는 x에 대해 "거의 지수적" 증가.
- **소결 12.0±0.2** = 펠릿을 550 °C 10 min 재소성 → **입계(GB) 전도 최적화** 효과로 해석.
- **195 K EIS**(x=0.5): 완전 반원 관측, R1/Q1+Q2 피팅 (R1 5233 Ω, Q1 1.487 nF·s^(a−1), α1 0.8825, Q2 29.26 µF, α2 0.5937, r=0.45 cm). apex 1.11×10⁵ Hz → C 1.7×10⁻⁹ F, α≈0.9 → 저자는 "이상적 CPE·해당 정전용량 = bulk 수송"으로 읽고 **Ea 트렌드는 GB에 크게 오염 안 됨**이라 주장(§14 비판).
- Ea는 σ와 역상관(Fig 3d), **최대 하락 구간 = x 0.375→0.5**. VT-EIS: 0.5 t 정압 셀, MTZ-35, 35 MHz–0.1 Hz, 298–338 K 5 K 간격·각 2 h 평형. 저온점(**286 K**·195 K)은 밀폐 EIS 셀을 냉각조에 침지해 별도 측정(SI 실물 확인 — 286 K 존재는 SI에만 언급).
- **전자전도도 σ_e ≈ 3×10⁻⁹ S/cm**(DC 분극, SS 블로킹, Fig S3) → **transference number ≈ 1**.
- 벤치마크: cold-press 9.4 = **준안정 Li₇P₃S₁₁급**; 소결 12.0 = 당시 최고 수준 근접.

### 3c. ⁷Li PFG NMR — 미시 확산 실측 (Fig 4·5, S5·S6)
| 지표 | x=0 | x=0.25 | x=0.375 | x=0.5 | 비고 |
|---|---|---|---|---|---|
| D*(300 K) [m²/s] | (낮음, Fig 4a 최하) | 중간 | — | **1.01×10⁻¹¹** | **LGPS(PFG) 2.2×10⁻¹² 의 ~5배**, Li₁₁Si₂PS₁₂ 3.5×10⁻¹² 의 ~3배 |
| Ea(PFG) [eV] | 0.35(1) | 0.343(9) | 0.320(3) | **0.29(1)** | lnD vs T⁻¹, 270–340 K; **EIS Ea와 오차 내 일치** |
| **Haven ratio H_R** | ~0.3 | ~0.3 | ~0.29 | **0.23** | H_R=D*/D_σ; T-둔감(Fig S6); LGPS 0.3–0.4·LLZO 0.43·LaF₃ ~0.1과 비교 |
| ⁷Li δ_iso 이동 | 기준 | ↓ | ↓ | **최저(LiCl 쪽)** | 비선형(0.375→0.5 변화 둔화); 고x서 선폭 비대칭(할로겐 무질서) |

- **H_R < 1 = 공공 매개 협동(correlated/cooperative) 이동**; x=0→0.25 불변, 그 뒤 하락 → **0.23(x=0.5)**. 하락 onset = Ea 최대 하락·δ_iso 변화 둔화 구간과 일치 → 낮은 치환 = 정전 약화 지배, 높은 치환 = **공공 농도 증가로 협동성 강화** 지배(시너지 서사).
- **H_R 산정의 c(캐리어 수) 규약 = 4 Li/unit cell**(케이지당 1/6×4케이지×Li 화학량론; **하한**이라 저자 명시) — H_R 절대값은 이 규약에 민감(§14).
- D_σ = (k_B T / c q²)·σ (Nernst–Einstein 역변환, eq 1). PFG 온도는 ¹H 화학이동 온도계(에틸렌글리콜/메탄올)로 교정, EIS 온도와 2차보간 매칭.

### 3d. 격자·고용한계 (Fig 3a, S2)
| 항목 | 값 |
|---|---|
| a(x=0) | **9.8598(4) Å** (XRD full-profile) |
| a(x=0.5) | **9.8061(1) Å** (중성자) — 단조 수축, **Vegard 준수**(Fig 3a: 0→0.25→0.375→0.5) |
| 수축 원인 | **주로 Li 공공** (S²⁻ 170 pm ≈ Cl⁻ 167 pm로 거의 등반경) |
| inter-cage 점프거리 | 2.88 Å(x=0) → **2.81 Å**(x=0.5) — 점프율에 유리하나 효과는 작다고 저자 판단 |
| **고용한계** | **x = 0.5 (Li₅.₅PS₄.₅Cl₁.₅ = end member)**. x>0.5: **LiCl 유의 석출**(Fig S2) → σ 급락(5.9→3.3). 원인 추정 = 고공공 함량에서 격자 열역학 불안정 |
| 불순물 상세(Fig S2) | x=0: 미량 Li₃PS₄ / x=0.25: Li₃PS₄ / x=0.375: 미량 LiCl+Li₃PO₄ / x=0.55: **LiCl+Li₃PS₄** / x=0.5 중성자: LiCl 1.7 wt% |
| Br 유사계 | Li₆₋ₓPS₅₋ₓBr₁₊ₓ는 **x=0.25에서 이미 LiBr 상당량** → Br-rich 고용체 불가(Br⁻ 182 pm 과대) — 이론 Li₅PS₄X₂(ref 24)의 Br·I판 실현 불가 판정 |

### 3e. 재인용 감사 (litdb 교차검증, 2026-07-28)
| litdb 위치 | 인용 내용 | 판정 |
|---|---|---|
| `liu2022…md` §2 | "Adeli(Li₅.₅PS₄.₅Cl₁.₅ 9.4 mS/cm, Ea 낮음)"·"Ea 0.28 (Adeli 보고와 유사)" | **✓ 정확** (9.4±0.1·0.29 eV) |
| `rao2025…md` §2 | "Adeli(Li₆PS₅Cl 2.5 / Li₅.₇₅PS₄.₇₅Cl₁.₂₅ 4.2 mS/cm)" | **✓ 정확** (Table 2) |
| INDEX 실험값 #4 행 | "2.5/0.34; 4.2/0.33; 5.6/0.31; 9.4/0.29…" | **✓ 정확** (본 digest로 ✅ 승격) |
| INDEX DFT시트 #3 행 | "냉간가압 σ=9.4 (Li₆PS₅Cl의 약 4배)" | **✓ 정확** |
| survey `md_structure_setup…` L52 | "4a/4c SOF 비교·9.4/12.0·D=1.01e-11·Vegard" | **✓ 정확** (PGSE→PFG(BPP-STE) 표기만 정밀화; ⚠→PDF 확보로 승격) |
| kraft2017 digest와의 정합 | Adeli Fig 2의 Li₆PS₅Cl SOF(4c-Cl 0.615) ↔ kraft2017 "4d 무질서 ~62 %" | **✓ 일치** (자리 라벨 4c↔4d 설정 차이만) |

### 3f. ★ SI 실물 감사 (2026-07-28, `inbox/33. Sup)…pdf` 전문 텍스트 추출 대조 — kraft2017 #31 Sup 감사와 동일 프로토콜)
**판정: SI 유래 수치 전값 일치 — digest 수정 사항 0.** 파일은 14 pp(내부 번호 1–12 + Wiley 표지·Author Contributions 2 pp; 종전 "12 pp" 표기는 내부 번호 기준).
- **Table S2 (σ 반복 시료) 전값 일치**: x=0.5 시리즈 A–D σ 9.4/9.3/9.5/9.4 → 9.4±0.1; 두께 0.630–1.03 mm·R 10–51.3 Ω·⌀1.0 cm. **정밀화**: 4계열 전부 측정된 건 x=0.5뿐 — x=0은 A–C(2.6/2.4/2.6→2.5), x=0.25는 A–C(4.2/4.0/4.4→4.2), x=0.375는 B–D(5.5/5.9/5.5→5.6). 표준편차는 √(Σ(x−x̄)²/n).
- **Table S3 (195 K 등가회로) 전값 일치**: R1 5233 Ω·Q1 1.487×10⁻⁹ F·s^(α−1)·α1 0.8825·Q2 29.26×10⁻⁶·α2 0.5937·r_electrode 0.45 cm.
- **Table S1 (EDX) 전값 일치**: Cl/P 평균 0.99/1.25/1.51 — 개별 측정 M1/M2 = 1.04/0.94·1.26/1.24·1.50/1.52 (시료당 2회).
- **신규 디테일(SI에만)**: ① PFG — π/2 8.1 µs@40 W·5 mm Shigemi 관(시료 깊이 3–4 mm)·최대 구배 2725 G/cm = **프로브 용량의 99 %**·T₂는 CPMG(에코 0.5 ms)·recycle 3.5 s(>5T₁이나 구배코일 duty cycle 제약)·구배 전후 1 ms 링다운 지연 + LED 5 ms·z-저장 중 spoiler 143 G/cm·2 ms·16스캔/스텝·표적 268.2–343.2 K; ② MAS — π/2 3.5 µs@110 W·명목 기준 = 밀봉 모세관 1 M LiCl(aq)(내부 기준 LiCl 불순물은 드리프트 보정용); ③ Haven c 규약 원문 — "엄밀히는 24 Li/cell 전부 가동적(6/f.u.×Z=4)이나 장거리 수송을 지배하는 것은 4케이지 간 48h–48h intercage 점프 → c = Li 화학량론×4케이지×1/6 ≈ 4/cell"을 **명시적 하한**으로 채택(Frank–Kasper 다면체의 인접 Li도 변위로 참여); H_R 온도 무관성은 x=0.375에서 가장 뚜렷(Fig S6); ④ 중성자 캔 = 바나듐 캔 + **구리 개스킷·알루미늄 뚜껑** 밀봉; ⑤ 저자 기여 — 합성·전기화학·중성자 해석 P.Adeli, **CV는 K.H.Park**, NMR 전담 J.D.Bazak, 중성자 측정 A.Huq.
- **부재 확정(figure-read 캐비앗 유지)**: **D*(T)·Ea 수치표 없음**(D*는 Fig S5의 300 K 1점 1.01×10⁻¹¹ m²/s만 캡션 명기, 나머지는 Fig 4 figure-read); 중간 조성 SOF 없음(중성자는 x=0.5뿐 재확인); Fig S2 불순물 동정(LiCl/Li₃PS₄/Li₃PO₄)은 그림 내 라벨 — 텍스트 추출로 검증 불가, figure-read 유지.
- SI 초록도 "9.4±0.1 mS/cm **at 300 K**" — 본문 298 K와의 온도 표기 혼재 재확인(§14).

## 4. 재료 & 방법 (실험) ★
- **합성**: Li₂S(99.98 %)+P₂S₅(99 %)+LiCl(99 %, 전부 Sigma) 화학량론, 총 ~1 g. Ar 글러브박스(H₂O·O₂<1.5 ppm) 유발 혼합 10 min → **지르코니아 133볼·밀폐 지르코니아 자, Fritsch PULVERISETTE 7 Premium, 380 rpm·17 h 볼밀** → 회수·재혼합 → **2 t 펠릿화**(⌀10 또는 9 mm) → glassy carbon 뚜껑 도가니 + 진공 석영관(사전 100 °C·2일 진공 베이킹) → **550 °C·5–7 h 열처리, 승·강온 0.5 °C/min**. ⇒ **볼밀(기계화학) + 저속 어닐**의 2단 공정 — 무질서·상순도가 이 공정 변수의 함수(cf. Liu2022는 450 °C 5 h가 최적).
- **XRD**: PANalytical Empyrean Cu Kα, 10–90°, 0.3 mm 석영 모세관 Debye–Scherrer(대기 차단). 전 조성 full-profile → 격자상수(Fig 3a).
- **중성자**: §3a 참조 (POWGEN TOF, λ_center 1.5 Å, d 0.50097–13.0087 Å, GSAS II).
- **EIS**: §3b 참조. 반복(시리즈 A–D)로 오차 산정 — Table S2에 두께(0.63–1.03 mm)·R(10–51.3 Ω)·σ 전 시료 공개(투명성 좋음).
- **전기화학**: σ_e = DC 분극(SS 블로킹, decay fit 후 정상전류 외삽, Ohm). CV = **Li|SE|SS 평판**, 5.0→−0.1 V, **1 mV/s**, RT, 펠릿 125 MPa(두께 0.158/0.155 cm). 대칭셀 Li|SE|Li: **0.25 mA/cm²·1.0 mAh/cm²**, 전해질 0.7 mm, ~160 h(Fig S8, ±~12 mV 안정).
- **⁷Li PFG NMR**: Bruker Avance III **300 MHz(7.0 T)**+Diff50 프로브. **BPP-STE(양극성 구배 자극에코)+LED** 시퀀스. 16-step 선형 구배 램프, **최대 2725 G/cm**, SINE.100 파형, 기본 δ=2 ms·Δ=20 ms(저온은 Δ·δ 연장), 최종 스텝 감쇠 <5 % 목표. T₁ 105–114 ms·T₂ 9–14 ms. 구배 선형성 검증(구배 반감+δ 보상, b 고정)·⁷Li MRI로 시료 센터링·구배 발열 ≤0.1 K 확인·¹H 화학이동 온도계 교정(268–343 K)·5 K 간격 20 min 평형. 피팅 = TopSpin 3.2, Stejskal–Tanner(BPP-STE 보정), FWHM 적분강도.
- **⁷Li MAS NMR**: 850 MHz(20 T, ⁷Li 330 MHz), 1.9 mm 로터 30 kHz. 자기장 드리프트 보정을 위해 **시료 내 LiCl 불순물(−1.18 ppm, T₁≈60 s)을 내부 기준**으로 활용(펌프형 자석). Fig S7(300 MHz 정적 VT): 270–340 K 모셔널내로잉 영역·위성전이 없음·FWHM ~400 Hz → Fig 5 이동 트렌드는 2차 사중극 이동으로 설명 불가(shielding 변화 = 진짜 화학 변화).
- **Haven ratio**: §3c 규약 참조. IUPAC 정의(H_R ≠ correlation factor 명시).

> ‼ **무질서 처리**: 계산적 무질서 처리(SQS/enumerate) 없음 — **무질서는 중성자 Rietveld SOF로 실측**. 이것이 우리 modelc 단일배열 decorate의 **실험 검증 기준**(Kraft가 x=0의 기준이듯 Adeli는 Cl-rich의 기준).

## 5. 결과 — 섹션별 상세

### 5.1 합성·조성 확인 (Fig 1, S1, Table S1)
표적 x=0–0.6 합성. **EDX Cl/P 비**: 목표 1.0/1.25/1.5 → 실측 평균 **0.99/1.25/1.51** (S는 SEM 이송 중 가수분해로 정량 제외). EDS 매핑: µm 스케일서 P/S/Cl 균질. x=0.5 중성자 Rietveld(Fig 1): GOF 3.37·R_wp 4.88 %·LiCl 1.7 wt%(마젠타 틱) — 정련 조성 Li₅.₄₇PS₄.₅₅Cl₁.₄₅.

### 5.2 구조 — 자리 점유의 재배치 (Table 1, Fig 2)
x=0(Kraft) 대비 x=0.5: 4a-Cl 0.385→0.615, 4c-Cl 0.615→0.834. **추가 Cl⁻는 양쪽 자리에 분배**되지만 4c를 우선 채움 → "S²⁻ 자리의 Cl 점유"로 정의한 site disorder **61→83 %**. 동시에 **Li 48h 점유 하락(0.456)** = 공공 증가, **Li U_iso 0.075 Å²** = 고이동성. Cl⁻(1가)이 S²⁻(2가)를 대체 → 케이지 음이온의 평균 전하 감소.

### 5.3 고용체·격자·한계 (Fig 3a, S2)
XRD 전 시리즈 단상성(x<0.5 "essentially single-phase" — 단 Fig S2에 미량 Li₃PS₄/LiCl/Li₃PO₄ 존재, §14). 격자 **Vegard 선형 수축** 9.8598→9.8061 Å; S²⁻/Cl⁻ 등반경이라 수축은 **Li 공공 몫**. **x>0.5: LiCl 유의 석출 + σ 급락(5.9→3.3 mS/cm)** — 저자 해석: 고공공 격자의 열역학 불안정이 용해한계를 결정. **이론(ref 24)의 Li₅PS₄Cl₂ 안정 예측과 달리 실험 end member = Li₅.₅PS₄.₅Cl₁.₅**. Br-rich는 x=0.25부터 LiBr → 고용체 불가(반경 182 pm); I-rich는 실현성 없음 판단.

### 5.4 전도도 (Fig 3b–d, Table 2, S2–S4)
σ가 x에 거의 지수적으로 증가, x=0.5서 **9.4±0.1**(cold-press·total) = x=0의 ~4×. 소결(550 °C 10 min) 시 **12.0±0.2** = GB 저항 감소. Ea(EIS) 0.34→0.29 eV 단조 감소(중간 조성 0.33/0.31, Fig S4). 195 K 반원의 capacitance·CPE 이상성(α~0.9)을 근거로 "관찰 트렌드는 bulk 지배" 주장. σ_e 3×10⁻⁹ S/cm.

### 5.5 PFG 확산 (Fig 4, S5)
270–340 K에서 D* 직접 실측: 전 온도서 x↑=D*↑. **x=0.5 D*(300 K)=1.01×10⁻¹¹ m²/s** — PFG 기준 LGPS(2.2×10⁻¹²)·Li₁₁Si₂PS₁₂(3.5×10⁻¹²)를 크게 상회. **Ea(PFG)와 Ea(EIS)가 전 조성서 오차 내 일치**(0.35/0.34 → 0.29/0.29) → (i) NMR(µm 스케일 확산)과 임피던스(거시 total)가 같은 장벽을 봄 = cold-press 펠릿에서 GB 기여가 Ea를 크게 왜곡하지 않음, (ii) x=0 Ea(PFG) 0.35는 문헌 0.33–0.37과 정합.

### 5.6 MAS NMR — Li–골격 상호작용 약화의 분광 증거 (Fig 5a, S7)
x↑에 따라 ⁷Li 공명이 **저주파수(LiCl 방향)로 이동** = 할로겐의 낮은 이온 전하가 Li⁺에 대한 정전 인력을 감소("점점 LiCl-like 이온성 환경"). **이동이 x에 비선형**(0.375→0.5 변화 둔화) → 음이온 통계 분포만으로 설명 불가 = **Li–골격 상호작용 자체의 감소**. 고x에서 선형 비대칭 = 할로겐 무질서 증가의 지문. (정적 VT 스펙트럼으로 사중극 기원 배제.)

### 5.7 Haven ratio — 협동 이동의 정량 (Fig 5b, S6, eq 1)
H_R = D*(PFG)/D_σ(EIS→NE 역변환). 전 상 ~0.3(LGPS·LLZO급), **온도 둔감**(= 조사 온도창에서 확산 메커니즘 불변). x=0→0.25 불변 → 이후 하락 → **x=0.5서 0.23**. H_R=1=무작위(희박계), **낮은 H_R = 공공 매개 강한 협동 hop**(극단 사례 LaF₃ ~0.1). **하락 onset이 Ea 최대 하락·화학이동 변화 둔화와 동시** → 두 영역 해석: 저치환 = 정전 약화(framework 효과) 지배 / 고치환 = **공공 급증 → 케이지 근처 빈 Li 자리 확률↑ → intercage jump 촉진 + 협동성↑**. 격자 수축의 점프거리 단축(2.88→2.81 Å)은 부차 효과.

### 5.8 안정성 (Fig S8–S10)
- **Li 대칭셀**: 0.25 mA/cm²·1.0 mAh/cm²서 Li₆PS₅Cl과 "동등하거나 약간 나은" 스트리핑/플레이팅(±~12 mV, ~160 h) — 정량 임피던스 추적은 없음.
- **CV(Li|SE|SS 평판, 1 mV/s)**: x=0.5는 1차 스캔서 **미소 양극 전류**(격자 황화물 → 절연성 황 산화로 귀속) → **2차 스캔서 사실상 0**(자기제한/passivation 시사). x=0은 초기 양극 전류가 더 크고 2차에도 잔존 → 저자 결론 "**x=0.5가 낮은 황화물 함량 덕에 양극(anodic) 안정성 우수**". 단 저자 스스로 "**CV는 오도 가능 — 실제 양극(cathode) 활물질 셀 검증 필요**" 명시. (⚠ Zuo 2022의 카본 복합 CV는 정반대로 Cl-rich 전류 2× — §11·§14 방법 함정.)
- 어필 포인트: Ge/Sn 같은 易환원 금속 없음 + 저가 원료 → Li 금속 대비 상대적 양호.

## 6. 메커니즘 종합 (3중 기작 + 1 부차)
1. **정전 약화(framework)**: S²⁻(2가)→Cl⁻(1가) 치환 → 케이지 음이온의 Li⁺ 인력 감소 (⁷Li 이동의 "LiCl-like" 진행; 비선형 = 상호작용 자체 감소).
2. **Li 공공 증가(carrier/vacancy)**: 전하 보상으로 Li 5.5/f.u. → 48h 점유 0.456 — 케이지 근처 빈자리 확률↑ → intercage jump 촉진.
3. **자리 무질서 증가(disorder)**: S자리 Cl 점유 61→83 % → Ea 하락에 기여 (de Klerk 무질서-intercage 논리의 실험 확장).
4. (부차) 격자 수축 → intercage 거리 2.88→2.81 Å — 효과 작음.
→ 저치환 구간은 1이, 고치환 구간(0.375→0.5)은 2(+H_R 0.23의 협동성)가 지배하는 **시너지**. 결과: Ea 0.34→0.29 eV, σ 4×, D* LGPS의 5배.

## 7. 전체 논증 흐름
표적 조성 합성(EDX 확인) → 중성자 Rietveld(x=0.5): Cl 4a/4c 분배·48h 공공·큰 Li ADP ⟹ **구조적 전제 확립** → XRD Vegard + x>0.5 LiCl 석출 ⟹ **고용창 0≤x≤0.5 확정** → EIS: σ 지수적 증가·9.4(4×)·소결 12.0·Ea 0.34→0.29 ⟹ **거시 수송 개선** → PFG: D* 직접 실측·Ea(PFG)=Ea(EIS) ⟹ **개선이 bulk 확산 기원임을 미시로 못박음** → MAS 이동(정전 약화) + H_R 0.3→0.23(공공 협동) ⟹ **기작 분해** → CV/대칭셀 ⟹ **응용 전망** → 결론: "할라이드 증량 = Li–골격 약화 + 무질서 + 공공으로 에너지 landscape를 바꾸는 전략".

## 8. DFT/계산 방법 ★ — **자체 계산 없음**
- **code/functional/k/ecut/supercell/무질서 처리 = 전부 해당 없음 (순수 실험).**
- 이론 인용 1건 = **de Klerk & Wagemaker 2016 MD (ref 24 = 우리 deklerk2016 digest 대상)**: 3종 점프 분류·무질서의 intercage 이점·Li₅PS₄X₂ 이론 조성. **본 논문의 위치 = 그 MD 예측의 실험 판정**: (a) "할로겐 증량은 σ를 크게 안 바꾼다"(MD) → **실험은 4× 증가로 반박/초과**; (b) "Li₅PS₄Cl₂ 안정"(MD) → **실험 end member는 x=0.5**; (c) "무질서·공공이 intercage jump를 돕는다"(MD) → **실험 지지**. 서베이 비교표에는 계산 세팅 행 추가 대상 아님(계산 0) — 대신 Adeli 행을 "실험 원전(⚠→확보)"으로 승격.

## 9. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | x=0.5 중성자 TOF Rietveld fit (GOF 3.37, R_wp 4.88 %, LiCl 1.7 wt%) | SOF 신뢰도의 원판 — modelc decorate 인용 시 이 fit 품질 근거 |
| **2** | 결정구조(PS₄ 사면체·Li 케이지·자유 S/Cl) + **4a/4c SOF 표(x=0 vs 0.5)** | **modelc ground-truth 그림** — 우리 셀 자리 분배 검증의 1차 참조 |
| 3a | 격자상수 vs x (Vegard) | Cl-rich 수축 = 우리 EOS V0 감소(254.16→243.29 Å³/fu)와 방향 대조 |
| 3b | 298 K Nyquist(cold-press 3조성+소결; 두께 정규화 inset) | "RT 반원 없음·Warburg 절편" 방법 명시 — σ 재인용 시 조건 병기용 |
| 3c | x=0.5 아레니우스(Ea 0.29) + **195 K Nyquist inset**(α 0.9·C 1.7 nF) | total vs bulk 논쟁의 원자료 |
| **3d** | σ & Ea vs x (역상관, x=0.5 정점) | 조성 시리즈 마스터 곡선 — comp1→modelc 아레니우스 비교 짝 |
| **4a,b** | PFG D* vs T(270–340 K) + lnD·ln(σT) 아레니우스(x=0 vs 0.5) | **bulk-급 D* 실측** — 우리 MLIP-MD D의 실험 대응물(외삽 아님) |
| **5a** | ⁷Li MAS(x 시리즈; LiCl −1.18 ppm) | "Li–골격 약화" 분광 관측 — 우리 정전/ICOHP 논의의 실험 짝 |
| **5b** | Ea(EIS·PFG)·δ_iso·**H_R** vs x 종합 상관 | **논문 전체 요약 1장** — H_R 0.3→0.23 = NE(Haven=1) 보정 정량 |
| S1/Table S1 | EDS 매핑/Cl/P 정량 | 조성 신뢰 |
| **S2** | x=0/0.25/0.375/0.55 XRD 불순물 | **modelc(Cl1.6) 고용한계 리스크의 직접 증거** |
| S3 | DC 분극(σ_e 3e-9) | transference ~1 |
| S4 | x=0.25/0.375 아레니우스(0.33/0.31 eV) | 중간 조성 Ea |
| S5 | PFG 감쇠곡선 예시(fit) | PFG 방법 신뢰 |
| **S6** | H_R vs T (4조성, 평균±표준오차) | H_R 온도 둔감 = 메커니즘 불변 근거 |
| S7 | 정적 VT ⁷Li(사중극 배제) | 이동 해석의 대조군 |
| S8 | Li 대칭셀 0.25 mA/cm² ~160 h | 음극 안정성(약한 증거) |
| S9 | CV 전범위(Li plating/stripping 가역) | — |
| **S10** | CV 2.0–4.5 V 확대: **x=0 양극전류 > x=0.5, 2차 스캔 잔존 vs 소멸** | ⚠ Zuo(카본 복합, 2×)와 정반대 — **평판 vs 복합 CV 방법 함정의 표본** |

## 10. Post-processing ★
- **Rietveld(GSAS II)**: 공유자리 제약(좌표·ADP 동일, occ 합=1) + Li 48h 자유 정련 → SOF·조성·ADP. 기록 = a, SOF, U_iso, GOF/R_wp, 부수상 wt%.
- **EIS→σ**: RT는 Warburg 꼬리 선형외삽 절편(σ=t/RA); 195 K는 R/Q+Q 등가회로(EC-Lab). 반복 시료(A–D)로 σ±std. **아레니우스 = ln(σT) vs 1000/T**.
- **PFG→D***: Stejskal–Tanner(BPP-STE 보정) 감쇠 피팅(TopSpin), FWHM 적분강도, b-범위 설계(최종 감쇠 <5 %), 온도 교정(¹H 온도계)·구배 선형성·시료 센터링 QC. **lnD vs T⁻¹ → Ea(PFG)**.
- **Haven**: D_σ=(k_BT/cq²)σ (c=4 Li/cell 규약, 하한) → H_R=D*/D_σ, 온도 평균±표준오차.
- **NMR 이동 분석**: LiCl 내부 기준(−1.18 ppm) 드리프트 보정; 정적 VT로 사중극 배제.
> 우리 적용: (1) **"EIS Ea ≈ PFG Ea" 이중 측정 프로토콜** = σ 논문에서 GB 오염 반박하는 표준 수(우리가 문헌 Ea 읽을 때 "어느 층인가" 판별 기준). (2) **H_R 산정 규약(캐리어 수 선택)** — 우리 MD에서 Haven 계산 시 규약 명시 필수의 선례. (3) Warburg-절편 σ = RT 황화물 EIS의 흔한 관행 — 문헌 σ가 "반원 없이" 나온 값임을 알고 인용.

## 11. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> **방법 분리 절대 원칙**: Adeli σ/Ea = **cold-press total EIS + PFG(bulk-급)** 실측 / 우리 = **MLIP-MD(UMA-s-1p1) bulk 단결정, MSD 2–50 ps, 600–1000 K 아레니우스**. 절대값 혼합 금지, 방향·비율만.

| 항목 | **Adeli (실측)** | **우리 (계산)** | 판정 |
|---|---|---|---|
| **조성 대응** | 시리즈 x=0(=comp1 조성)…x=0.5(주인공)…**x=0.6(=modelc 조성, 고용한계 밖·LiCl 석출·σ 3.3)** | comp1=Li₆PS₅Cl / **modelc=Li₅.₄PS₄.₄Cl₁.₆ 단일상 가정** | **⚠ 핵심 괴리**: 우리 modelc는 이 공정에선 단일상으로 실재하지 않음. 단 후속 공정(급속열처리·나노결정핵생성 등; INDEX exp#6 Cl1.6 10.8 / exp#7 Cl1.7 17 mS/cm·Nazar 2024 Cl1.7 11.4)은 도달 → **"고용한계 = 공정 변수"로 서술**하고 modelc는 "실험적으로 접근 가능한 Cl-rich 극한의 계산 모형"으로 위치 |
| σ(RT) | 2.5→**9.4**(4×, x 0→0.5; total) / 소결 12.0 | 절대 σ 인용 금지(NE·단일시드) — D(600 K) 3.09→7.90×10⁻⁶ cm²/s (**2.6×**) | **✓ 방향·크기급 일치** (실측 4× vs 우리 D 2.6×; 조성도 Cl1.5 vs 1.6으로 다름 — 등치 금지) |
| Ea | EIS 0.34→**0.29** / PFG 0.35→**0.29** (Δ≈−0.05) | MLIP-MD 0.253→**0.224** (Δ=−0.029; 단일궤적) | **✓ 방향 일치**. 절대값 갭(~0.07–0.10 eV) = 온도창(270–340 vs 600–1000 K)·방법(실측 vs UMA)·조성 차 — **Kraft total 0.46보다 Adeli(0.29–0.35)가 우리 bulk 값에 훨씬 가까움**(PFG=bulk-급이라 당연) |
| D | **D*(300 K)=1.01×10⁻¹¹ m²/s (x=0.5, PFG 실측)** | D(600 K)만 인용(2–50 ps 창) — RT 외삽은 규율상 헤드라인 금지 | **○ 소환값으로 보관**: 우리 modelc MD를 300 K로 (내부 점검용) 외삽할 때의 실측 anchor. 공식 비교는 Ea·비율만 |
| **Haven ratio** | **0.3(x=0) → 0.23(x=0.5)** (c=4/cell 규약, 하한) | 우리 σ 환산 = **NE(Haven=1)** 가정 — H_R 미계산 | **🔑 우리 규율의 정량 보완**: NE(H=1)는 correlated 계에서 σ를 H_R배 만큼 과소(σ_true=σ_NE/H_R ≈ 3–4×σ_NE, 이 규약 기준). "절대 σ 인용 금지" 규칙의 물리적 근거 수치가 이 논문에 있음. 단 H_R 절대값은 캐리어-수 규약 의존 → 우리 MD Haven 계산 시 규약 명시 후에만 대조 |
| 격자/부피 | a 9.8598→9.8061 Å(수축, Vegard; 원인=Li 공공) | EOS V0 254.16→243.29 Å³/fu(수축) — comp1 relaxed a≈10.055 Å(+2 %, PBE 통상 과대) | **✓ 수축 방향·기작(공공) 일치**; 절대 a는 PBE offset |
| **자리 점유(무질서)** | 4a-Cl 0.615/4c-Cl 0.834/Li48h 0.456 (실측 SOF) | modelc = 단일배열 decorate (4a/4d 분배 우리 기록 미명세) | **★ 액션**: modelc 셀의 Cl 4a:4c(4d) 분배·Li 공공 배치를 이 SOF와 정량 대조해 문서화 — "실험 점유 decorate" 주장 가능 여부 판정 |
| Li–골격 상호작용 | ⁷Li 이동 "LiCl-like" = **정전 인력 약화**(1가 Cl) | ICOHP(Li–Cl) comp1 −1.86 → modelc −2.10 (**개별 Li–Cl 결합은 강화**) | **△ 다른 물리량 — 모순 아님**: Adeli = Li–(전체 골격) 평균 정전 환경(S²⁻ 감소가 지배), 우리 ICOHP = Li–Cl 쌍별 공유결합 성분. "Cl-rich가 Li를 약하게 잡는다"를 ICOHP(Li–Cl)로 뒷받침하려 하면 **역방향 인용 오류** — 반드시 구분 |
| 산화(양극 CV) | 평판 CV: x=0.5 양극전류 **작음**·2차 소멸("낮은 황화물 함량") | grand-potential onset **comp1=modelc 2.256 V 동일(S²⁻-limited)**; Zuo(카본 복합 CV)는 Cl-rich 전류 **2×** | **⚠ 3자 정합 정리**: onset(thermo)은 조성 무관(우리·축 B①) / 분해 "양"은 측정계 의존 — **평판 SS CV(Adeli, 접촉면적·1 mV/s 과속 → 분해 과소·상대비교도 신뢰 낮음) vs 카본 복합 CV(Zuo, 증폭)**. Adeli 스스로 "CV 오도 가능" 경고 → **"Cl-rich가 anodic 안정"을 이 논문 근거로 일반화 금지** |
| σ_e | 3×10⁻⁹ S/cm (DC 분극) | gap 2.099 eV(PBE, fixed-occ) = wide-gap 절연체 | ✓ 정성 정합 (t≈1); 절대 gap 비교 금지 규율 유지 |
| 기계·ESW·전자구조 | n/a (미측정) | E_VRH·B0·ESW·gap 보유 | n/a — 이 논문은 축 A(이온전도)+구조 전용 |

## 12. 적용 인사이트 (깊게)
1. **modelc 셀의 실측 ground truth 확보 (최우선 수확)**: Table 1의 SOF(4a-Cl 0.615 / 4c-Cl 0.834 / Li 48h 0.456)가 halogen-rich 아지로다이트의 유일한 중성자 정련 원본. **후속 액션 — 우리 modelc(Cl1.6) 배열의 4a:4c Cl 분배를 이 값과 정량 대조**하고, 어긋나면 "이상화 배열"임을 명시(cf. survey의 Zhou 2025: 4a 전부 Cl 이상화 사례).
2. **modelc 조성은 이 공정의 고용한계 밖**: x=0.6 실측 = LiCl 석출 + σ 3.3 mS/cm. 그러나 동일 조성이 다른 공정(박막·급속열처리)에선 10.8 mS/cm, Cl1.7은 17 mS/cm(Excel 소환값)·Nazar 2024 11.4 mS/cm — **"고용한계·무질서 = 열역학 상수가 아니라 공정 변수"**가 이 원전+후속으로 완성. 우리 논문에서 modelc를 다룰 때 이 문장으로 방어.
3. **Haven ratio 0.23–0.3 = NE(Haven=1) 규율의 정량 근거**: 우리 σ 환산이 왜 "절대값 인용 금지"인지의 실측 이유(협동 이동 → NE가 3–4× 과소, 규약 의존). 향후 우리 MD에서 D_tracer vs D_collective로 H_R을 직접 뽑아 x-트렌드(0.3→0.23)와 대조하면 **협동성 강화 서사를 계산으로 재현**하는 저비용 아이템.
4. **Ea 사다리 정리**: 문헌 Ea는 층이 있다 — Kraft total(GB 포함) 0.46 ≫ **Adeli EIS≈PFG(펠릿 total이나 bulk-일치 입증) 0.29–0.35** > 우리 MLIP-MD bulk 0.224–0.253. Adeli의 "EIS=PFG 일치" 프로토콜이 **문헌 Ea를 bulk로 신뢰해도 되는지 판별하는 기준**: PFG 짝이 있는 값만 bulk-급으로 인용.
5. **3중 기작(정전·공공·무질서) = comp1→modelc 서사의 실험 원판**: 우리 D↑·Ea↓(MLIP-MD)·BVSE 채널·inter-cage 멘탈모델이 이 논문의 기작 분해와 1:1. deck에서 "Adeli 실험 3중 기작 — 우리 계산이 각 축을 분리 재현" 구도로 인용.
6. **소결 9.4→12.0 = σ의 GB/미세구조 몫**: [KimICCF]·[Cha]의 "lever=microstructure" 서사에 halogen-rich 원전의 소결 데이터 포인트 추가.
7. **평판 CV의 함정 표본**: Adeli(평판 SS, Cl-rich 전류↓) vs Zuo(카본 복합, Cl-rich 전류 2×) — 같은 물질쌍·정반대 겉보기. 산화 축 서술 시 "측정계 명시 없으면 인용 금지"의 최적 교보재.

## 13. 인용 가능 문장 (deck/paper용)
- "Adeli et al. established the halogen-rich argyrodite solid solution Li₆₋ₓPS₅₋ₓCl₁₊ₓ (x ≤ 0.5): cold-pressed σ = 9.4±0.1 mS/cm (298 K, total) and 12.0±0.2 mS/cm sintered for Li₅.₅PS₄.₅Cl₁.₅ — with Ea dropping 0.34→0.29 eV, confirmed independently by EIS and ⁷Li PFG NMR."
- "Neutron Rietveld refinement (POWGEN TOF) gives the ground-truth site occupancies for Cl-rich argyrodite: Cl SOF 0.615 on 4a and 0.834 on 4c, Li 48h occupancy 0.456 (Li₅.₄₇PS₄.₅₅Cl₁.₄₅), a = 9.8061(1) Å — the experimental template for our model-c cell decoration."
- "The Haven ratio drops from ≈0.3 (Li₆PS₅Cl) to 0.23 (Li₅.₅PS₄.₅Cl₁.₅), signalling vacancy-mediated cooperative Li⁺ motion — and quantifying why Nernst–Einstein (Haven = 1) conversions systematically underestimate σ in argyrodites."
- "Beyond x = 0.5 the lattice rejects further chlorine (LiCl exsolution; σ collapses to 3.3 mS/cm at nominal Li₅.₄PS₄.₄Cl₁.₆ under 550 °C/5–7 h annealing) — the solid-solution limit, later pushed to Cl₁.₇ by different processing, is a *process variable*, not a constant."
- "Contrary to the MD prediction that higher halogen content would not alter conductivity (de Klerk 2016), experiment shows a near-exponential, ~4-fold increase up to the x = 0.5 end member."

## 14. 주의 / 한계 (over-claim 방지)
- **σ = total(bulk+GB)**: 195 K에서도 bulk/GB 분리 실패(저자 명시). "9.4 mS/cm bulk"로 인용 금지 — bulk-지배 주장은 Ea(EIS=PFG) 간접 논증. RT는 반원 없이 **Warburg 절편**으로 R 결정.
- **중성자는 x=0.5 한 조성뿐** — 중간 조성의 SOF·Li 점유는 미실측(격자상수만 XRD). x 시리즈 무질서 진화(61→83 %)는 끝점 2개 기반.
- **Li 자리 모형 = 48h 단독**: 24g·T5a 등 대안 자리 검토 서술 없음 — 이후 문헌(Nazar 2024 등)은 Cl-rich에서 16e(T4) interstitial 점유 보고 → 이 정련은 2019 수준의 최선이지 최종 Li 분포는 아님.
- **H_R 절대값은 캐리어-수 규약(c=4/cell, 하한) 의존** — 규약 바꾸면 값 스케일이 바뀜(트렌드는 견고). "argyrodite Haven=0.23"을 규약 없이 이식 금지.
- **"essentially single-phase"의 실상**: x=0.5조차 LiCl 1.7 wt%(내부 NMR 기준으로 활용), x=0.375에 미량 LiCl·Li₃PO₄, x=0/0.25에 Li₃PS₄ 미량 — 완전 순상 아님.
- **CV(평판 Li|SE|SS·1 mV/s)는 분해 과소평가** — 저자 자인("misleading"). "Cl-rich 양극 안정성 우수"는 이 측정계 한정; Zuo 카본-복합 CV(2×)와 정반대 = 방법 함정. thermo onset은 S²⁻-limited로 조성 무관(우리 축 B①).
- **온도 표기 혼재**: 298 K(Table 2) vs 25 °C(본문) vs 300 K(SI 초록·PFG D*) — 인용 시 298 K(σ)/300 K(D*)로 구분.
- x=0.55/0.6의 Ea는 N/A(다상이라 미보고) — 3.3 mS/cm에 Ea 붙여 인용 금지.
- 이 논문에 **DFT·MD·BVSE 없음** → 계산 방법 비교 대상 아님. de Klerk 인용 관계는 §8로만.
- 대칭셀 증거는 약함(~160 h·저전류·CCD 없음) — "Li 금속 안정" 강주장 금지 (Liu2022·Lu2025가 그 축의 본대).

## 15. 기법 용어 미니사전
- **PFG(pulsed-field gradient) NMR**: 자기장 구배 펄스로 스핀 위치를 위상에 각인 → 확산에 의한 에코 감쇠에서 **tracer 확산계수 D\***를 직접 측정(μm 스케일, 모델 무관). 여기선 ⁷Li로 Li⁺만 선택 관측.
- **BPP-STE(+LED)**: 양극성 구배쌍(bipolar pair) 자극에코 시퀀스 + 종방향 와전류 지연 — 와전류 상쇄·T₁(≫T₂) 저장 활용으로 고체 전해질처럼 T₂ 짧은 시료에 적합.
- **Stejskal–Tanner 식**: ln(I/I₀) = −b·D, b∝(γgδ)²(Δ−δ/3) — 감쇠 vs 구배 세기에서 D 추출(BPP-STE 보정 포함).
- **MAS(magic-angle spinning)**: 54.7° 고속회전(30 kHz)으로 이방성 상호작용 평균화 → 고분해능 δ_iso. **δ_iso의 저주파 이동 = 더 이온성(LiCl-like) 환경**.
- **모셔널 내로잉**: 이온 hop이 NMR 시간척도보다 빠르면 선폭이 좁아짐 — 여기선 270–340 K 전 구간 내로잉 영역(=빠른 Li 운동 전제 성립).
- **Haven ratio H_R = D*(tracer)/D_σ(전도)**: 1=무상관, <1=협동(vacancy-mediated correlated) 이동. D_σ=(k_BT/cq²)σ — **c 규약이 절대값을 좌우**.
- **Warburg-절편법**: 블로킹 전극 저주파 꼬리(확산 스파이크)를 직선 외삽해 실수축 절편 = 전해질 총 저항 — 반원이 대역 밖일 때의 RT 관행.
- **CPE 이상성 α**: 반원 눌림의 지수(1=이상 커패시터). α~0.9 + C~nF를 근거로 bulk-지배 주장(브루그 환산).
- **TOF 중성자(POWGEN)**: 백색 중성자 비행시간 분산 — 넓은 d-범위(0.5–13 Å)·Li 감도(X-ray 대비) → Li 점유·ADP 정련 가능.
- **Vegard 법칙**: 고용체 격자상수의 조성 선형성 — 단상 고용 형성의 표준 증거.
- **자리 무질서(site disorder)**: 명목 S²⁻ 자리(여기 4c=타문헌 4d)의 할라이드 점유율 — inter-cage 장벽을 낮추는 아지로다이트 σ의 핵심 레버.
