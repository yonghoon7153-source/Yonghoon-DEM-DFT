# Operando analysis of electronic band structure in an all-solid-state thin-film battery — Hikima et al. (Commun. Chem. 2022)

> slug `hikima2022_operando_band_structure_assb` · DOI `10.1038/s42004-022-00664-w` · type `exp (operando HAXPES; 보조 first-principles 인용)` · PDF `da3c1e4d-25._Operando…thinfilm…pdf` · digested `2026-06-26` · status ✅
> **저자**: Kazuhiro Hikima, Keisuke Shimizu, Hisao Kiuchi, Yoyo Hinuma, Kota Suzuki, **Masaaki Hirayama, Eiichiro Matsubara, Ryoji Kanno** (Tokyo Institute of Technology / Toyohashi Univ. Tech / Kyoto Univ. / AIST / Waseda) · Communications Chemistry **5**:52 (2022) · open access
> **[외부]** — 도쿄공대 **Ryoji Kanno**(LGPS·argyrodite 분야 거두) 그룹 + AIST(Hinuma=first-principles). **우리 그룹(한양대 J-W Lee/Y.M.Lee/Cho/Kang/Cha) 아님.** ⚠ **핵심**: 이 논문은 **고체전해질을 *반도체 소자*로 취급**하여 박막 ASSB의 *전체 밴드구조*(VBM·CBM·E_F·일함수·band bending)를 **operando HAXPES**로 충전 중 실측한다. 즉 우리 grand-potential 산화분석(`oxidation_stability_VBM_vs_grandpotential_report`)의 *valence-side 관측량*(VBM/IE)을 *작동 중(operando)*으로 보는 실험판이고, [Whitten](UPS 튜토리얼)·[Banik](HAXPES VBM 불변)이 *정적*으로 본 밴드엣지를 *시간/전압 분해*로 확장한다.

---

## 0. 이 digest를 읽는 법 (왜 이걸 먹였나)
이 논문은 **"배터리를 작동시키면서 그 *전체 전자 밴드구조*(진공준위 절대기준의 VBM·CBM·Fermi level)를 측정할 수 있는가? 그리고 충전 중에 밴드가 *어떻게* 움직이는가?"** 에 답한다. 핵심 트릭 = **all-solid-state 박막셀을 *반도체 헤테로접합 소자*로 보고**, 각 구성층(Al 집전체 / Li₂MnO₃ 양극 / LASGTP 고체전해질 / Li₃PO₄ buffer / Li 음극)의 밴드를 **진공준위 절대기준**으로 정렬한 뒤, **operando HAXPES**(hard X-ray PES, 6.9 keV)로 충전 중 코어레벨 결합에너지(BE) 이동을 추적해 **계면 band bending·전해질 전위창(potential window)·과전압 위치**를 *작동 중*에 읽어낸다.

우리에게 중요한 단 하나의 프레임: **이건 우리 정적 DFT 밴드엣지(VBM=S 3p)·oxidation 보고서(VBM↔grand-potential 위계)의 *operando 실험 카운터파트*다.** [Whitten]이 "UPS로 VBM/Φ를 *어떻게* 재나"(기법)이고 [Banik]이 "HAXPES로 argyrodite VBM이 *치환 무관 불변*"(정적 결과)이라면, 이 논문은 "**그 밴드엣지가 *작동 중*에 *움직인다*** — 충전하면 양극 Fermi level이 drop하고 계면에 band bending/inversion이 생긴다"를 보인다. **단 honest**: 이 논문 재료는 **Li₂MnO₃ 양극 + LASGTP(oxide) 고체전해질**이지 **argyrodite가 아니다.** 따라서 *재료 수치 1:1 비교가 아니라 *방법·프레임·메커니즘 정합*이다(§7·§10). 우리 LPSCl/modelc와 VBM·gap 절대값을 등치하면 안 된다.

> ⚠ **전압/기준 주의**: (1) 밴드 위치는 **진공준위(vacuum level) 절대기준**(eV) — UPS/LEIPS/HAXPES로 각 층을 진공준위에 정렬. (2) cell voltage는 **Li/Li⁺ 기준**(Al|Li₂MnO₃|LASGTP|Li₃PO₄|Li 셀, 2.0–5.0 V). (3) HAXPES BE는 **Al 집전체-grounded operando 측정의 *상대* 이동(ΔBE)** — Al의 Fermi level 기준. 절대 밴드도(Fig 2·3)와 operando ΔBE(Fig 4)는 *다른* 기준이니 섞지 말 것.

## 1. 한 줄 요약
박막 ASSB(Al|Li₂MnO₃|LASGTP|Li₃PO₄|Li)를 **반도체 헤테로접합 소자로 취급**해 **operando HAXPES**로 충전 중 *전체 밴드구조*를 진공준위 절대기준으로 결정: pristine에서 **Al/Li₂MnO₃ = staggered(Type II) 정렬**이고, 충전 시 **Li₂₋ₓMnO₃ Fermi level이 ~0.8 eV drop → n-형에서 p-형으로 전이**, **Al/Li₂₋ₓMnO₃ 계면이 Ohmic→Schottky(정류)→inversion layer 형성** → **고전압에서 전류가 한 방향(방전)으로만 흐름 → 충전이 진행 불가**(이론용량 459 mAh/g 미달의 *전자구조적* 원인). **전해질 LASGTP의 potential window·과전압 위치**도 *작동 중*에 직접 읽음 — 이는 "**작동 중 밴드구조를 봐야만** 얻을 수 있는 정보"이고 배터리 설계의 새 프로토콜을 제시.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 셀 (5층) | **Al 집전체(10 nm) / Li₂MnO₃ 양극(35 nm) / LASGTP 고체전해질(기판) / Li₃PO₄ buffer(500 nm) / Li 음극(1 µm)** — *thin-film* model SSB |
| 양극 | **Li₂MnO₃** (Li₂₋ₓMnO₃) — 이론용량 **459 mAh/g**(2Li 추출), 실용 ~300; *unrivaled layered oxide*. O3→O1 stacking 전이(선행 in-situ XRD/DFT, ref29) |
| 전해질 | **LASGTP** = Li₁₊ₓ₊ᵧAlₓ(Ti,Ge)₂₋ₓSiᵧP₃₋ᵧO₁₂ (NASICON-type oxide SE, glass ceramic) |
| buffer | **Li₃PO₄**(RF sputter) — LASGTP가 Ti⁴⁺→Ti³⁺ 환원되는 것을 막는 *전해질/Li 사이 보호층* |
| 동기 | 배터리 특성화(충방전·CV·임피던스·XAS·XPS)는 **밴드구조를 고려 안 함**. 액체전해질 셀은 분해·복잡성으로 operando 밴드구조 측정 불가. **ASSB = 모든 계면이 고체 정션 → *반도체 소자*처럼 다룰 수 있음** → HAXPES(반도체 heterojunction 에너지정렬 표준기법)를 배터리에 적용 |
| 질문 | (a) 작동 중 *전체* 밴드구조(진공준위 절대기준)를 측정 가능한가? (b) 충전 시 밴드가 어떻게 움직이나(band bending·정렬 전이)? (c) 그것이 셀 거동(고용량 미달·과전압·계면 부반응)을 어떻게 설명하나? |
| 방법 3종 | **UPS**(He I 21.22 eV, VBM·Φ) + **LEIPS**(low-energy inverse photoemission, CBM/EA) + **operando HAXPES**(6.9 keV, 깊은 층까지 코어레벨) — 각 층을 진공준위에 정렬 + 작동 중 BE 추적 |

## 3. 핵심 물성 (수치 총정리) ★
> 모든 밴드 위치는 **진공준위 기준**(Fig 2). WF=일함수, EA=전자친화도, IP=이온화퍼텐셜, Eg=밴드갭. **재료가 argyrodite 아님** — 절대값은 *프레임·방법 참고*용, 우리 LPSCl과 등치 금지.

### 3.1 각 구성층의 밴드 위치 (pristine, 진공준위 기준 — Fig 2)
| 층 | WF (eV) | EA (eV) | IP (eV) | Eg (eV) | VBM/CBM·E_F 비고 |
|---|---|---|---|---|---|
| **Al**(집전체) | **4.3** | — | — | (금속) | E_F만(금속). WF 4.24도 병기 |
| **Li₂MnO₃**(양극) | **3.74** | **3.51** | **6.34** | **2.83** | CBM=EA 3.51 / VBM=IP 6.34; E_F−E_VBM=2.1. Mn 3d–O 2p VBM |
| **LASGTP**(전해질) | **3.45** | **2.71** | **7.80** | **4.09** | wide-gap; E_F−E_VBM=4.06 (E_F가 VBM 위로 높이 = n쪽 가까움) |
| **Li₃PO₄**(buffer) | — | — | **8.48** | **5.77** | wide-gap 절연 buffer; E_F−E_VBM=5.03 |
| **Li**(음극) | **2.5–2.6** | — | — | (금속) | Li metal WF; Li 2s |

> 🔑 **Li₃PO₄ Eg=5.77 eV** = 우리 sei_products.json **Li₃PO₄ 5.73 eV**와 *거의 정확히 일치*(독립 실측+계산 앵커, §7·§9). **LASGTP Eg=4.09**(oxide SE) — 우리 LPSCl PBE 2.07보다 큼(다른 재료·다른 측정).

### 3.2 계면 정렬 & band bending (Fig 3)
| 계면/조건 | 정렬 타입 | 핵심 수치 | 의미 |
|---|---|---|---|
| **Li₂MnO₃/LASGTP** (pristine) | **staggered (Type II)** | CBM(Li₂MnO₃) > CBM(LASGTP) by **0.2 eV** (EA 차 3.71−3.51); VBM(Li₂MnO₃) > VBM(LASGTP) by **1.46 eV** (IP 차 7.80−6.34) | 양극↔전해질 정상 정렬 |
| Al–Li 전위차 | — | ΔE_F(Al,Li) = **2.6 eV** (eV_cell); 셀 단자전압의 밴드 기원 | E_F 차 = 셀 전압 |
| **Li₂₋ₓMnO₃** (charge 5.0 V, band bending 고려) | **straddling (Type I)** | 전위창 *안*으로 들어옴 | 충전 시 양극 밴드가 전위창 내부로 |
| **Li₂MnO₃/LASGTP** (discharge 2.0 V, band bending 무시) | **staggered (Type II)**, LASGTP가 전위창 *밖* by **0.53 eV** | 방전 2.0 V서 LASGTP가 Li₂₋ₓMnO₃에 의해 환원 위험 | 저전압 환원 부반응 단서 |

### 3.3 충전 중 Fermi level / 결합에너지 이동 (operando, Fig 4) ★ — 논문의 정량 심장
| 단계(stage) | 전압 범위(V vs Li) | 조성(x) | 핵심 ΔBE / E_F 이동 | 전자구조 사건 |
|---|---|---|---|---|
| **Stage 1** | 2.8→3.25 V | 0 ≤ x < 0.04 | Li 1s·O 1s **약간 downward**(증가); Al 1s shift와 상관; **E_F(Li₂₋ₓMnO₃) downward ~0.45 eV** (Al 3.25–2.8 eV shift 대비 ~0.32–0.14 더 큼) | 미량 Li 추출이 **Li₂₋ₓMnO₃ 전자구조를 격하게 바꿈**(Fermi level drop) — *operando HAXPES로 처음 관측* |
| **Stage 2** | 3.25→4.38 V | 0.04 ≤ x < 0.27 | E_F **gradually downward ~0.8 eV**; Li 1s·O 1s **upward**(감소)+**두 번째 O 1s peak가 downward**; 총 **Fermi level downward shift ~1.1 eV** (2.2→1.1 eV, E_F가 VBM 수준까지) | **n-형 → p-형 전이.** Al/Li₂₋ₓMnO₃ 계면이 **Ohmic→Schottky(정류)** → **inversion layer** 형성 |
| **Stage 3** | 4.38→4.65 V | 0.27 ≤ x < 0.63 | 전압 **~4.6 V plateau**; Li 1s·두 O 1s peak **BE 변화 없음**; O 1s 상대강도만 변(새 peak↑·원 peak↓) | 충전은 진행되나 **전자구조 변화 없음** = **progressive oxygen redox**(격자 O 산화, 조성/전압 변화 없는 평탄부) |
| **Stage 4** | 4.65→5.0 V | 0.63 ≤ x < 1.0 | Li 1s·두 O 1s **downward parallel** to Al E_F | (de)intercalation 동반 조성변화; O3→O1 stacking 전이도 이 단계 |
| **과전압** | 5.0 V 후 OCV 이완 | — | 5.0 V→4.7 V 이완 시 ΔBE *비가역적으로 즉시 안 풀림* | **과전압 위치 = HAXPES로 확인** — Li₂₋ₓMnO₃가 5.0 V서 *열역학 평형 아님*; 충전 4.6→5.0 V는 *대부분 가역* |

> 🔑🔑 **핵심 비대칭(Fig 3e,f)**: 충전 5.0 V서 **Al/Li₂₋ₓMnO₃ = p-형(정류)** → **전자가 LASGTP(전해질)→Al(집전체) 한 방향(p→n)으로만** → **방전만 가능, 충전 불가**(고전압서). = "**고전압서 미량 충전만 되는** 실험사실"의 *전자구조적* 설명. Li₂MnO₃ 459 mAh/g 이론용량 미달의 근본 원인 중 하나.

## 4. DFT/계산 방법 ★
> ⚠ **이 논문은 *실험(operando HAXPES)* 중심.** First-principles는 *직접 수행이 아니라 선행연구 인용*(ref29, "first-principles formation energy + in-situ XRD로 O3→O1 stacking 전이 규명")으로만 등장. 공저자 **Yoyo Hinuma(AIST)**가 first-principles 전문이나, *이 논문 본문엔* 밴드구조를 DFT로 계산한 절차·파라미터가 **없음**(n/a).

- **code / version**: n/a (이 논문서 DFT 직접 계산 없음)
- **functional / pseudo / k / ecut / supercell / nat**: n/a
- **DFT+U / AIMD / MLIP / 무질서 처리**: n/a (모두 실험)
- **밴드구조 취득 = *실험* 3종 조합**:
  - **UPS** (He I **21.22 eV**, PHI VersaProbe III, bias −5 V로 SECO): 각 층 **VBM + 일함수 Φ** → IP. (= [Whitten] 튜토리얼의 정확한 적용)
  - **LEIPS** (low-energy inverse photoemission, e⁻ gun 1 µA/20 V): **CBM / 전자친화도 EA**(점유 안 된 측). UPS+LEIPS = 실험 밴드갭·전체 밴드 정렬.
  - **operando HAXPES** (SPring-8 **BL22XU**, hemispherical analyzer R4000, **incident photon ~7.9 keV**, take-off 89°, escape depth **~47 nm** = 표준 Al Kα(수 nm)로 못 보는 *깊은 매립 계면*까지; Al 집전체 *통과*해 Li₂MnO₃·계면을 봄). operando = current **0.467 µA/cm²**(0.1 C), constant 전류 충방전 + peak-fitting time-resolved.
- **밴드 정렬 = 반도체 heterojunction 표준**: 각 층 진공준위 정렬(Fig 2) → 계면 band offset → band bending(Fig 3d–f). E_F(반도체)를 금속 E_F에 맞춰 전자이동(전하 carrier density 변화)으로 BE 이동 해석.
- **특이사항/튜닝**: (1) **2가지 grounding**(working=Al, 또는 anode=Li) 비교(Supplementary Fig 5) — Al 1s가 cell voltage와 linear(slope 1 eV/V), P 1s는 거의 불변 → **편의상 Al-grounded** 채택(peak fitting 동일). (2) Al spectrum = Al 집전체 기여를 빼서 보정(raw는 Supplementary Fig 4). (3) 셀은 Ar-filled glove box, O₂<1 ppm/H₂O<0.1 ppm, 공기/수분 노출 없이 진공챔버 이송.

## 5. 결과 — 섹션별 상세 (모든 논점)

### 5.1 각 구성층 밴드 위치 (Fig 1, 2) — 진공준위 절대기준
- **개념도(Fig 1a–c)**: 액체 LIB(복잡·분해) → ASSB(고체 정션=반도체 소자) → thin-film model(복잡성 회피). **Fig 1d** = operando HAXPES setup(potentiogalvanostat + 빔라인). **Fig 1e** = operando spectra(Al 1s·Li 1s·P 1s vs time·cell voltage). **Fig 1f** = 결과 밴드도식(Cathode|SE|Anode의 CBM/E_F/VBM/Eg + Mn 3d/O 2p/Li 2s).
- **Fig 2 (밴드도)**: 5층을 진공준위에 정렬. WF: Al 4.3 / Li₂MnO₃ 3.74 / LASGTP 3.45 / Li₃PO₄ (n/a, IP 8.48) / Li 2.5–2.6. Eg: Li₂MnO₃ **2.83** / LASGTP **4.09** / Li₃PO₄ **5.77**. → **셀 전압의 밴드 기원**: Al과 Li의 E_F 차 = **2.6 eV**(= eV_cell). LASGTP는 E_F가 VBM서 4.06 eV 위(wide-gap·n쪽).

### 5.2 계면 정렬 & band bending (Fig 3a–f) — staggered/straddling 전이
- **Pristine(Fig 3a,d)**: **Li₂MnO₃/LASGTP = staggered(Type II)** junction. CBM(Li₂MnO₃) > CBM(LASGTP) **0.2 eV**(EA 3.71 vs 3.51), VBM(Li₂MnO₃) > VBM(LASGTP) **1.46 eV**(IP 7.80 vs 6.34). LASGTP CBM bending **0.20**, Li₂MnO₃ CBM 0.16, VBM 0.63 (Fig 3d 화살표).
- **Charge 5.0 V(Fig 3b,e)**: band bending 고려 시 **Li₂₋ₓMnO₃가 전위창 *안*으로(straddling/Type I)**. **Fermi level downward ~0.8 eV** + **total Fermi level shift ~1.1 eV(2.2→1.1 eV)** → **VBM 수준까지 E_F drop = n→p 전이**. Al/Li₂₋ₓMnO₃ 계면 **Ohmic→Schottky→inversion layer**.
- **Discharge 2.0 V(Fig 3c,f)**: band bending 무시 시 **staggered(Type II)**, **LASGTP가 전위창 *밖* by 0.53 eV** → **저전압서 LASGTP가 Li₂₋ₓMnO₃에 의해 환원될 수 있음**(계면 부반응 단서). bending 고려 시 LASGTP 0.53→음전위창 밖.
- **🔑 메커니즘(BE 이동의 3원인, p.4–5)**: (1) **Li₂₋ₓMnO₃ vs Al/Li의 E_F 위치차**(서로 다른 WF, Fig 2), (2) **carrier density 변화로 E_F 이동**(VBM/CBM/코어 대비), (3) **cycling 반응(crystal structure·composition 변화)**. → operando HAXPES가 이 셋을 *작동 중* 분리.

### 5.3 충전 중 전자구조 변화 — 4단계 (Fig 4a,b) ★ — 논문의 심장
- **4단계 정의(충방전 용량 기준)**: stage1 2.8–3.25 V(0≤x<0.04) / stage2 3.25–4.38 V(0.04≤x<0.27) / stage3 4.38–4.65 V(0.27≤x<0.63) / stage4 4.65–5.0 V(0.63≤x<1.0). 임계조성 Li₁.₉₆/Li₁.₇₃/Li₁.₃₇/Li₁.₀MnO₃.
- **Stage 1 (Fig 4a-1,a-2,b)**: Li 1s·O 1s(O²⁻) **약간 downward**(BE 증가), Al 1s shift와 *매우 잘* 상관. **Fermi level downward ~0.45 eV**(Al 3.25–2.8 eV shift보다 0.32(Li 1s)–0.14(VBM) 더 큰 drop, Supplementary Fig 3·11). → **미량 Li 추출(x<0.04)이 Li₂₋ₓMnO₃ Fermi level을 격하게 내림** — 이전엔 못 본 것.
- **Stage 2 (Fig 4)**: **n→p 전이.** E_F가 *constant band gap 가정*하에 VBM 수준으로 **total ~1.1 eV downward(2.2→1.1 eV)**. Li 1s·O 1s **upward**(BE 감소, = LiCoO₂ 선행 ref34와 동형: Li deintercalation시 lower-BE shift) + **두 번째 O 1s peak downward**. → **Al/Li₂₋ₓMnO₃ Ohmic→Schottky(정류) → inversion layer(고전압서 p-형이라)**.
- **Stage 3 (Fig 4)**: **~4.6 V plateau**, Li 1s·두 O 1s **BE 불변** = **Li₂₋ₓMnO₃ 전자구조 변화 없음**. 단 **O 1s 상대강도 변화**(새 peak↑·원 peak↓, Supplementary Fig 4) = **progressive oxygen redox**(격자 산소 산화, ref21). 충전은 되나 *전자구조는 정지*.
- **Stage 4 (Fig 4)**: Li 1s·두 O 1s **downward parallel** to Al E_F = Li₂₋ₓMnO₃ 전자구조는 *Al 대비 불변*(평행이동) = stage4 충전은 **조성변화 동반((de)intercalation + O3→O1 stacking)**.
- **OCV 이완(5.0→4.7 V)**: 충전 후 전위 *즉시 안 풀림* → **Li₂₋ₓMnO₃ 5.0 V는 열역학 평형 아님(과전압)**; 4.6→5.0 V는 *대부분 가역* → **과전압 위치를 HAXPES로 확인**. 가능 기전 2: (a) bulk Li₂₋ₓMnO₃ 활성화장벽(높은 과전압/전자전도 필요), (b) **Li₂₋ₓMnO₃/LASGTP 계면의 *capacitor* 가역형성**(>4.6 V, 선형 V↔축적전하). depth profiling서 O 1s broadening 없음 → bulk 전위구배 없음 → **계면 capacitor가 stage4 주역**(분해 아니라 가역 축적).

### 5.4 종합 — 셀 거동의 전자구조적 설명 (Discussion, p.5–6)
- **고전압 충전 불가의 원인**: stage2서 **n→p 전이 + inversion layer** → Al/Li₂₋ₓMnO₃가 **정류(rectifying)** → 전류가 *방전 방향(LASGTP→Al, p→n)*으로만 → **충전이 더 진행 못 함** = 459 mAh/g 미달. ("only discharging would proceed at high voltage" = 실험의 *slight charge capacity at high voltage*와 정합.)
- **stage4 capacitor**: Li₂₋ₓMnO₃/LASGTP 계면에 가역 capacitor 형성(전압↔전하 선형) → "충전이 되는데 redox 아닌" 거동. *전자구조 변화 없는 stage3·4의 plateau를 설명.*
- **저전압 부반응**: discharge 2.0 V서 LASGTP가 전위창 밖(0.53 eV) → **LASGTP 환원**(Ti⁴⁺→Ti³⁺) 위험 → Li₃PO₄ buffer가 그래서 필요(전해질/Li 보호).
- **결론**: "**작동 중 밴드구조를 봐야만** 계면 부반응(분해층·space charge layer)·전위창·과전압을 알 수 있다 → 배터리 설계의 새 프로토콜."

## 6. 메커니즘 종합 (한 흐름)
박막 ASSB를 **반도체 소자로 취급**(모든 계면=고체정션) → UPS+LEIPS로 각 층 밴드를 진공준위 정렬(Fig 2: Al/Li₂MnO₃/LASGTP/Li₃PO₄/Li의 WF·EA·IP·Eg) → pristine **Li₂MnO₃/LASGTP = staggered Type II**(Fig 3a,d) → **operando HAXPES**로 충전 중 코어레벨 BE 추적(Fig 4) → **stage1 미량 Li추출이 E_F 격하게 drop(0.45 eV)** → **stage2 E_F가 VBM까지 ~1.1 eV drop = n→p 전이 → Al계면 Ohmic→Schottky→inversion** → **stage3 plateau=oxygen redox(전자구조 정지)** → **stage4 capacitor(가역 축적)+stacking 전이** → **고전압서 정류 때문에 충전 불가(이론용량 미달)** + **과전압 위치·LASGTP 전위창(저전압 환원위험) 직접 확인** → "**operando 밴드구조 = 계면 부반응·전위창·과전압의 직접 관측 도구**".

## 7. 우리 DFT 대비 (comp1 / modelc) ★ → `../our_dft_baseline.md`, `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md`
> ⚠⚠ **method/material-dependence 먼저 (이 비교가 가장 조심스러운 이유)**: (i) **재료가 다름** — 이 논문 = **Li₂MnO₃ 양극 + LASGTP(NASICON oxide SE)**; 우리 = **LPSCl/modelc(sulfide argyrodite SE)**. VBM·CBM·Eg·일함수 *절대값 1:1 비교 절대 금지*(다른 화합물·다른 음이온·다른 측정). (ii) **관측량 종류** — 이 논문 밴드엣지는 **진공준위 절대기준 *실측*(UPS/LEIPS/HAXPES)**; 우리 DFT VBM은 **셀 평균전위 기준(정렬 미보정·비엄밀, report §4b)**. (iii) **물리 정의** — 이 논문 핵심은 **band alignment/bending(전자적 계면)**이지 **grand-potential 분해 onset이 아님** → 우리 oxidation 보고서 §6 위계로 정확히 "**밴드엣지(상한·band alignment) vs 분해창(실제 onset)**"의 *밴드엣지 측* 관측. (iv) 따라서 비교는 **수치 등치가 아니라 *프레임·방법·메커니즘 정합***.

| 항목 | Hikima (이 논문) | 우리 (comp1/modelc; oxidation report) | 일치/차이 + 이유 |
|---|---|---|---|
| **밴드구조를 *진공준위 절대기준*으로 측정** | UPS+LEIPS+HAXPES로 5층 VBM/CBM/E_F/Φ 정렬(Fig 2) | 우리 DFT 절대 VBM은 **셀 간 정렬 미보정 → 비엄밀**(report §4b·`concepts/dos_vbm_efermi_methods.md`); slab WF도 **포기**(asymmetric slab dipole → spurious 6.5–7.2 eV; 문헌 WF Braga 2026 (100)=3.40 eV 사용) | **🔑 보완 관계**: 이 논문이 *실험으로* 제공하는 "진공준위 절대 밴드정렬"이 **우리 DFT가 못 가진 외부 절대기준**. [Whitten]·[Banik]과 같은 결: UPS/HAXPES가 우리 DFT VBM의 *절대 앵커*. 단 우리 slab-WF 포기와 동형 난점(이 논문도 LASGTP 위 박막이라 잘 정렬됨) |
| **밴드엣지 = band alignment용 (≠ 산화 onset)** | 명시적으로 **계면 정렬·band bending·전위창**을 위해 밴드 측정; 전해질 LASGTP "potential window"를 밴드로 정의 | 우리 report §6 핵심: **VBM/UPS=band alignment(상한), 산화 onset=grand-potential/CV(실제)** | **✓✓✓ 동일 프레임** — 이 논문이 밴드를 *band alignment/전위창*에 쓰는 것이 우리 "VBM은 band alignment용" 용도구분(report §5 표)과 정확히 일치. **단 이 논문은 oxide SE라 "분해창 2–3× 과대" 문제는 직접 다루지 않음**(Li₂MnO₃ redox 중심) |
| **밴드엣지가 *작동 중 움직인다*(operando)** | 충전 시 E_F downward ~1.1 eV, n→p 전이, band bending/inversion (Fig 4) | 우리 = **정적 0 K VBM 1개**(comp1 2.128/modelc 2.445, 절대·비엄밀); operando 거동 *못 봄* | **△ 차원 확장(우리 밖)**: 우리 정적 VBM ↔ 이 논문 *operando 밴드엣지 운동*. **우리 H목록(향후)** "전압별 밴드·계면" 의 실험 선례. [Banik] HAXPES는 *정적 VBM 불변*, 이 논문은 *operando VBM 운동* → 둘이 정적/동적 짝 |
| **Li₃PO₄ buffer Eg** | **5.77 eV**(IP 8.48 − VBM, 실측 UPS) | sei_products.json **Li₃PO₄ 5.73 eV**(MP DFT) | **✓✓✓ 거의 정확 일치(Δ0.04 eV)** — 우리 wide-gap 절연 SEI/buffer 산물(Li₃PO₄)의 *외부 독립 실측 앵커*. (단 우연성 주의: 측정 IP-VBM vs MP gap; 그래도 같은 ~5.7 eV) |
| **LASGTP(oxide SE) Eg** | **4.09 eV** | comp1 2.066 / modelc 2.099 (PBE, sulfide) | **△ 재료 다름** — oxide SE(LASGTP 4.09) > sulfide(우리 2.07). [Rupp] "oxide wide-gap·sulfide 좁은 gap"의 정렬. **절대 비교 금지**(다른 재료·PBE 과소) |
| **셀 전압 = 밴드(E_F)차** | Al−Li E_F 차 = **2.6 eV = eV_cell** | 우리 OCV 1.717 V(grand-potential, 다른 정의=분해평형) | **△ 다른 정의**: 이 논문 = 전극 Fermi level 차(밴드); 우리 OCV = 분해 자유에너지 평형. *같은 "전압"이라도 기원 다름* — 섞지 말 것 |
| **고전압 충전불가 = 정류(p-형 inversion)** | stage2 n→p → Al계면 Schottky → 충전 차단 | 우리 = (양극 Li₂MnO₃ 미보유; LPSCl SE만) 해당 없음 | ✗ **범위 밖**(우리 hull에 Mn·Ti·Ge·NASICON 없음). *양극 전자구조* 현상이라 우리 SE-bulk DFT 밖 |
| **operando HAXPES 기법** | 6.9 keV·escape 47 nm로 *매립 계면* 작동 중 측정 | 우리 = ORCA ΔSCF **XPS core-hole**(P 2p/S 2p/Nd 3d, `xps_reference_sei.csv`) — *정적·계산* | **△ 상보**: 우리 XPS=정적 코어레벨 화학상태(계산); 이 논문 HAXPES=*operando* 코어레벨 BE 이동(밴드/Fermi). 같은 광전자분광의 정적-계산 vs 작동-실측 |

**§7 한 줄 결론**: 이 논문은 **우리 oxidation 보고서 §6(UPS↔CV↔DFT 위계)·[Whitten](기법)·[Banik](정적 HAXPES VBM)의 *operando 실험 확장***이다 — "밴드엣지는 *band alignment/전위창*용(우리 용도구분과 일치)이고, 그것이 *작동 중에 움직인다*". 가장 깨끗한 *수치* 정합은 **Li₃PO₄ Eg 5.77 ≈ 우리 5.73 eV**(wide-gap 절연 buffer 산물의 외부 앵커). **단 재료가 oxide(Li₂MnO₃/LASGTP)라 argyrodite 산화 onset·VBM 절대값과 등치 금지** — 연결은 *프레임·방법·메커니즘*이지 수치가 아니다.

## 8. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a–c** | 액체 LIB → ASSB(반도체 소자) → thin-film model 개념 진화 | "**ASSB=반도체 헤테로접합**" 프레임의 원전 도식. 우리 [Semi]("When Electrolytes Are Semiconductors")와 같은 세계관 |
| **1d** | operando HAXPES setup(potentiogalvanostat + 빔라인) | operando 광전자분광 실험 구성 — 우리 협업 HAXPES/operando XPS 측정 시 참조 |
| **1e** | operando spectra: Al 1s·Li 1s·P 1s vs time/cell voltage | **작동 중 코어레벨 추적**의 데이터 형식(시간축 vs BE) |
| **1f** | 결과 밴드도식(Cathode\|SE\|Anode: CBM/E_F/VBM/Eg + Mn 3d·O 2p·Li 2s) | 셀 전체 밴드정렬 *도식화* 템플릿 — 우리 SE/SEI 밴드정렬도 만들 때 모델 |
| **2** | **5층 밴드도(진공준위 기준)**: WF/EA/IP/Eg 전부 | **🔑 진공준위 절대기준 밴드정렬의 실측 예** — 우리 DFT 절대 VBM 비엄밀의 *실험 해법*. **Li₃PO₄ Eg 5.77 ≈ 우리 5.73** 앵커 |
| **3a–c** | pristine/charge5.0/discharge2.0 밴드도(최소가정) | staggered(Type II)↔straddling(Type I) **정렬 타입 전이** — 충전이 계면 정렬을 바꿈 |
| **3d–f** | 같은 조건의 **band bending**(E_F 기준 CBM/VBM 휘어짐) | **계면 band bending 정량**(0.16/0.20/0.63 eV 등) — 계면 전자 안정성의 직접 관측 |
| **4a (a-1 Al 1s, a-2 P 1s)** | 집전체·전해질 ΔBE vs 충전/OCV; Al 1s ~2 eV 상승, P 1s 불변 | **P 1s 불변 = LASGTP 내부 정렬 불변**(Li 확산 무관) — reference층 거동 |
| **4b (b-1 Li 1s, b-2 O 1s)** | **양극 ΔBE 4단계**: Li 1s·O 1s(O²⁻·O^(2−δ)) 이동 + 두 번째 O peak | **🔑 operando 전자구조 4단계의 정량 심장**(stage1 drop·stage2 n→p·stage3 plateau·stage4 parallel). oxygen redox(새 O peak) 직접 |

## 9. Post-processing ★
- **밴드 정렬(진공준위)**: **UPS**(VBM onset 선형외삽 + SECO로 Φ → IP) + **LEIPS**(CBM/EA) → 각 층을 진공준위에 정렬 → 계면 band offset(EA차=CBM offset, IP차=VBM offset). = [Whitten] §5 절차의 다층 적용.
- **band bending**: E_F를 기준으로 CBM/VBM이 계면서 휘는 양(eV)을 도식화(Fig 3d–f). 반도체 heterojunction depletion 이론.
- **operando BE 추적**: HAXPES 코어레벨(Al 1s·Li 1s·O 1s·P 1s) **peak fitting** → 시간/전압별 ΔBE → **Fermi level 이동**(carrier density 변화) 해석. grounding(Al vs Li) 비교로 reference 확정.
- **정렬 타입 판정**: VBM/CBM offset 부호로 straddling(Type I)/staggered(Type II)/broken(Type III) 분류 → 충전에 따른 전이.
- **과전압/평형 진단**: 충전 정지 후 OCV 이완 시 ΔBE가 *즉시 안 풀리면* 과전압(비평형); depth profiling O 1s broadening 없음 → bulk 전위구배 없음(계면 capacitor).
- **도구**: 표준 광전자분광 분석기(hemispherical R4000, FAT) + peak fitting. 싱크로트론 HAXPES(SPring-8 BL22XU). (DFT 도구는 이 논문서 미사용.)
- **수치화·기록**: 밴드 위치(eV, 진공준위/E_F 기준 명시)·Eg·Φ·band bending(eV)·ΔBE(eV) vs V·정렬 타입.
> **우리 적용**: 이 논문의 **"진공준위 절대 밴드정렬(UPS+LEIPS) + operando 코어레벨 BE 추적"** = 우리가 *언젠가* SE/SEI 밴드정렬을 실험검증할 때의 템플릿. 특히 **우리 DFT 절대 VBM(비엄밀)의 외부 절대기준**을 이 방법이 준다(slab-WF 포기를 우회). 우리 XPS ΔSCF(정적 코어레벨)와 짝이 되는 *operando* 코어레벨.

## 10. 주의/한계 (over-claim 방지) — 비판적으로
- **🔑 재료가 argyrodite 아님**: Li₂MnO₃ 양극 + **LASGTP(NASICON oxide SE)**. **우리 LPSCl/modelc와 VBM·CBM·Eg·일함수 절대값 1:1 비교 절대 금지.** 연결은 *프레임(반도체 소자)·방법(UPS+LEIPS+operando HAXPES)·메커니즘(밴드엣지 운동)·용도구분(밴드=alignment)*뿐. 유일한 *수치* 앵커 = **Li₃PO₄ Eg 5.77 ≈ 우리 5.73**(공통 산물).
- **DFT 직접 계산 없음**: first-principles는 ref29 *인용*만(O3→O1 stacking). 공저자 Hinuma(AIST)가 first-principles 전문이나 *이 논문 본문엔* 밴드 DFT 절차·파라미터 없음 → §4 전부 n/a. "이 논문이 DFT로 우리 VBM을 검증" 류 금지.
- **밴드엣지 ≠ 산화 onset(우리 핵심 규율 재확인)**: 이 논문은 밴드를 *band alignment·전위창·band bending*에 쓰지 **grand-potential 분해 onset**에 쓰지 않음. 우리 oxidation 보고서 §6 위계(밴드엣지=상한, 분해창=실제) 그대로 — 이 논문을 "operando 산화 onset"으로 읽으면 우리가 거부한 프레임. **LASGTP "potential window"도 *전자적*(band) window이지 분해창이 아님**(단 저전압 LASGTP 환원위험은 별개로 언급).
- **operando HAXPES 표면/매립 민감성**: escape depth ~47 nm로 *깊은 계면*을 보지만, **Al 집전체(10 nm) 통과 신호**라 Al 기여를 빼야(Supplementary Fig 4) + grounding(Al vs Li) 선택이 BE 기준을 바꿈. 절대 BE 해석에 reference 가정 개입.
- **band gap "일정 가정"**: stage2 Fermi level shift(~1.1 eV)는 *constant band gap 가정* 하 VBM까지 drop으로 환산 — gap이 cycling 중 변하면(Mn 산화상태) 수치 흔들림. 저자도 "assuming constant band gap of Li₁.₉₆MnO₃" 명시.
- **thin-film model = 실셀 아님**: 35 nm Li₂MnO₃·박막 LASGTP. 저자 명시 "**두꺼운 양극·음극의 실 ASSB 논의엔 추가 고려 필요** — 이 연구는 thin-film 탐색에 한정". 두꺼운 복합전극의 공간전하·다결정 효과는 안 봄.
- **과전압·capacitor 기전은 *해석*(간접)**: stage4 "계면 capacitor 가역형성"은 depth-profiling(O 1s broadening 없음)+선형 V-Q 추론이지 *직접* 증명 아님. bulk 활성화장벽 vs 계면 capacitor 둘 다 가능성으로 제시.
- **Li₂MnO₃ 특정**: 다른 양극(NCM 등)이면 n→p 전이·정류 거동 다를 수 있음(Mn-redox+O-redox 특유). 일반화 주의.

## 11. 적용 인사이트 (깊게) — 우리 연구에 어떻게
1. **우리 oxidation 보고서 §6의 *operando 실험 선례* 확보**: 보고서가 "**UPS↔CV↔DFT 위계** + 밴드엣지는 band alignment용"을 *정적*으로 논했다면, 이 논문은 **그 밴드엣지가 *작동 중*에 어떻게 움직이는지(E_F drop·n→p·band bending)를 operando로 실측**. → deck/보고서에 "밴드엣지의 band-alignment 용도는 *작동 중*에도 유효하며 *동적*이다(Hikima 2022 operando HAXPES)" 한 줄 추가 가능. **[Whitten](기법)→[Banik](정적 결과)→[Hikima](operando)** 3단 계보 완성.
2. **Li₃PO₄ Eg 5.77 ≈ 우리 5.73 = wide-gap 절연 산물의 외부 실측 앵커**: 우리 sei_products.json Li₃PO₄(5.73, MP DFT)가 *독립 실측(UPS IP-VBM)*과 0.04 eV 일치. **우리 "Li₃PO₄=전자절연 buffer/SEI(전자차단)" 논리(Nd cascade·Rupp ALD)의 실측 근거**. + 이 논문 셀이 **Li₃PO₄를 실제 buffer로** 쓴다(LASGTP 환원 보호) = "wide-gap 절연 buffer가 전해질을 보호"의 device 실증.
3. **"진공준위 절대 밴드정렬(UPS+LEIPS)"이 우리 DFT 절대-VBM 비엄밀의 *실험 해법***: 우리는 slab-WF를 포기(dipole)·절대 VBM 정렬 미보정. 이 논문 방법(각 층 진공준위 정렬)이 *외부 절대기준*을 줌 → 우리 협업 실험이 SE/SEI 밴드정렬을 실측한다면 이 템플릿. (단 우리 SE는 절연체라 [Whitten] 대전 경고 적용.)
4. **"ASSB=반도체 소자" 프레임 = 우리 [Semi] digest와 합류**: 이 논문(Kanno)과 [Semi]("When Electrolytes Are Semiconductors", HSE06)가 같은 세계관 — *고체전해질을 반도체로*. 우리 전자구조(gap·VBM·σ_e) 서사를 이 프레임에 얹으면 deck 일관성↑. **단 우리 SE는 wide-gap insulator(2.07 PBE), 이 논문 LASGTP는 4.09**(다른 재료).
5. **정직한 한계 = 우리 차별화 명확화**: 이 논문은 (a) *oxide* SE(LASGTP)·(b) *양극*(Li₂MnO₃) 전자구조 중심·(c) DFT 없음·(d) *분해 onset 아님*. **우리 기여 = sulfide argyrodite의 (i) grand-potential 분해 onset(이 논문이 안 다룸), (ii) VBM=S 3p 화학([Banik] COHP), (iii) Cl-rich 4축.** 이 논문은 *밴드 alignment/운동*의 operando 실험이지 *분해 열역학*이 아니므로, "Hikima가 우리 산화 onset을 검증" 같은 over-claim 금지 → "**밴드엣지 운동의 operando 관측**"으로만.
6. **operando 코어레벨 BE 추적 = 우리 XPS ΔSCF의 *작동* 짝**: 우리 ORCA ΔSCF(정적 코어레벨 화학상태)와 이 논문 operando HAXPES(작동 중 코어레벨 BE/Fermi 이동)는 같은 광전자분광의 정적-계산 vs 동적-실측. 우리 SEI 산물 BE(133.3/168.0/160.2/198.6)를 *operando*로 추적하면 분해 진행을 *실시간*으로 볼 수 있다는 방법 영감.

## 12. 인용 가능 문장 (deck/paper용)
- "Hikima et al. (Kanno group) treat an all-solid-state thin-film battery as a semiconductor heterojunction and measure its *entire* band structure (VBM/CBM/E_F/Φ on an absolute vacuum-level scale, by UPS + LEIPS + operando HAXPES), showing that during charging the cathode (Li₂₋ₓMnO₃) Fermi level drops ~1.1 eV, the material undergoes an n-to-p transition, and the current-collector interface turns Ohmic→Schottky with an inversion layer — so only discharge proceeds at high voltage." [Hikima 2022]
- "This is the *operando* counterpart to our static band edges: it confirms that the valence-band edge is a band-alignment / electronic-interface observable (consistent with our oxidation report's UPS↔CV↔DFT hierarchy and with Banik's static HAXPES VBM), and that it *moves* under bias — extending the band-edge picture from static (our DFT VBM, Banik) to dynamic." [Hikima 2022 + our oxidation report §6]
- "Their UPS-measured Li₃PO₄ band gap (5.77 eV) matches our DFT value (5.73 eV) to 0.04 eV, providing an external experimental anchor for the wide-gap insulating buffer/SEI products (Li₃PO₄) that underpin our electron-blocking-interphase logic." [Hikima 2022 + sei_products.json]
- "Because the band edges are used for band alignment, potential windows and band bending — not for a grand-potential decomposition onset — this work reinforces our rule that oxidative-stability onset is set by grand-potential/CV, while VBM/UPS/HAXPES report the (operando) band alignment." [Hikima 2022 + our oxidation report §6]

## 13. 주의/한계 재요약 (한 줄)
Hikima = **박막 ASSB를 반도체 소자로 보고 *전체 밴드구조*(진공준위 절대)·계면 band bending·전해질 전위창·과전압을 operando HAXPES로 작동 중 실측한 외부(Kanno) 논문** — 우리 oxidation 보고서 §6(밴드엣지=band alignment 관측량)·[Whitten](기법)·[Banik](정적 VBM)의 *operando 확장*. **⚠ 재료가 oxide(Li₂MnO₃/LASGTP)라 argyrodite VBM/Eg/산화 onset과 *수치* 등치 금지**(유일 앵커 Li₃PO₄ Eg 5.77≈5.73); DFT 직접 계산 없음; 밴드엣지≠분해 onset(우리 규율 재확인). 연결 = *프레임·방법·메커니즘·operando*이지 수치가 아님.

## 14. 기법 용어 미니사전
- **operando HAXPES** (hard X-ray photoelectron spectroscopy): 고에너지 X선(~6.9 keV)으로 *깊은 매립 계면*(escape depth ~47 nm)의 코어레벨을 **배터리 작동 중** 측정. UPS/soft-XPS(수 nm)로 못 보는 집전체-아래 양극·계면을 봄.
- **UPS / LEIPS**: UPS(He I 21.22 eV)=가전자대 **VBM·일함수**(점유측); **LEIPS**(low-energy inverse photoemission)=**CBM/전자친화도 EA**(빈자리측). 둘 합쳐 실험 밴드갭·전체 밴드정렬. (UPS는 [Whitten] 참조.)
- **진공준위(vacuum level) 기준 밴드정렬**: 각 층의 VBM/CBM/E_F를 *공통 진공준위*에 정렬 → 계면 band offset 산출. 반도체 heterojunction 표준(우리 DFT 절대 VBM 비엄밀의 실험 해법).
- **WF/EA/IP/Eg**: 일함수(진공−E_F)·전자친화도(진공−CBM)·이온화퍼텐셜(진공−VBM)·밴드갭(CBM−VBM).
- **band bending**: 계면서 carrier 재분포로 밴드(VBM/CBM)가 E_F 기준 휘는 현상. depletion/inversion/accumulation의 원천.
- **staggered (Type II) / straddling (Type I) / broken (Type III) junction**: 두 반도체 VBM/CBM offset 부호에 따른 정렬 분류. 충전이 Li₂MnO₃/LASGTP를 Type II↔Type I로 전이.
- **Ohmic vs Schottky(정류) contact**: 금속/반도체 계면이 양방향 전도(Ohmic) vs 한 방향만(Schottky, rectifying). 충전 시 Al/Li₂₋ₓMnO₃가 Ohmic→Schottky.
- **inversion layer**: 반도체 표면 carrier가 *반대 타입*으로 뒤집힌 층(n쪽 표면이 p처럼). 고전압 Li₂₋ₓMnO₃(p-형)에서 형성 → 정류.
- **n→p 전이**: Li 추출(산화)로 Fermi level이 VBM 쪽으로 내려가 다수 carrier가 전자→정공으로 바뀜. 산화의 *밴드 신호*.
- **oxygen redox (progressive)**: 격자 산소(O²⁻→O^(2−δ))가 redox에 참여 — stage3 plateau의 새 O 1s peak. 고용량 layered oxide 특유.
- **potential window (전자적)**: 전해질의 VBM/CBM이 정의하는 *전자적* 안정 전압창(band-edge). ≠ grand-potential 분해창(우리 oxidation 규율).
