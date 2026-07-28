# Stability Issues in Sulfide-Based All-Solid-State Batteries: From Material Properties to Electrode Interfaces — Yang Li / … / Hong Liu* / Ce-Wen Nan / Li-Zhen Fan* (Electrochemical Energy Reviews, **미출판 manuscript draft ECER-D-26-00097**)

> slug `fan2026_sulfide_assb_stability_review_ECERD2600097` · DOI **없음(미출판; draft 내 placeholder "10.1002/((please add manuscript number))" — EER은 Springer인데 Wiley prefix가 박혀 있는 템플릿 잔재)** · type **review (문헌 컴파일, 자체 계산/실험 0)** · PDF 4분할 `653a4e87-ECERD2600097___1.pdf`(30p) + `eb8d18d5-…___2.pdf`(30p) + `5d14fe59-…___3.pdf`(30p) + `38482998-…___4.pdf`(23p) — **총 113 pp, 전 페이지 정독** · digested `2026-07-16` · status ✅ · **📌 우선순위 must-read (INDEX 최상단)**

## 0. 이 digest를 읽는 법
- 이 논문은 **황화물 ASSB "안정성" 전 분야의 field-map 리뷰** (본문 56 pp + 참고문헌 239개 + Figure 26개). [Bai](argyrodite 전용)·[Rupp](oxide/sulfide 광역)·[Kang](우리 그룹 electrochemo-mechanical)에 이은 **네 번째 리뷰 좌표계** — 이번 것은 "**안정성 축**"으로 짠 지도이며, 우리 캠페인(자유-S 산화 서사·B₂O₃/O 도핑·음극 SEI json)이 **여섯 칸에 동시에 꽂힌다** (§11).
- **미출판 draft**라는 점 주의: 인용 시 "ECER-D-26-00097, submitted to Electrochem. Energy Rev." 로만; 수치·주장은 게재본에서 바뀔 수 있음.
- 저자진이 **[Li25](CuBr₂ 도핑, ESM 2025)와 같은 그룹**(USTB Fan Li-Zhen·Tsinghua Ce-Wen Nan; 제1저자 Yang Li 동일 인물로 추정 — ref 218에 자기 논문 인용, Fig 24b가 그 논문 그림). 즉 이 리뷰는 **우리가 이미 digest한 [Li25]·[Liu23]의 모(母)그룹 시점**에서 쓴 것.
- 섹션별 상세는 §5, 수치 총정리는 §4, 황화물 SE 계열 카탈로그는 §6, **열화 메커니즘 분류(taxonomy)는 §7, 완화 전략 매트릭스는 §8**, DFT/계산 콘텐츠는 §9, Figure 26개 전체는 §10, 우리 캠페인 대응은 §11.

## 1. 한 줄 요약
황화물 SE의 실용화 병목을 **"안정성"이라는 단일 렌즈**로 재구성한 리뷰 — (i) 재료 고유 불안정 5축(공기/용매/열/전기화학/기계), (ii) 양극 계면 실패(화학·전기화학 산화 + 화학-기계 결합), (iii) 음극 계면 실패(덴드라이트·환원분해·공극/접촉손실)를 메커니즘 수준으로 분해하고, 각 축마다 공학적 완화 전략(도핑·코팅·인공 SEI·신규 CAM·압력/공정)을 대응시킨다. 핵심 명제: **"황화물 SE의 안정성 문제는 단일 재료 결함이 아니라 화학·전기화학·열·기계 인자의 결합 효과이며, 해법은 'passive stabilization'에서 'intrinsic stability'로, 정적 계면에서 동적 계면 조절로 옮겨가야 한다."**

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 제목 | Stability Issues in Sulfide-Based All-Solid-State Batteries: From Material Properties to Electrode Interfaces |
| 원고번호 / 상태 | **ECER-D-26-00097 · Review article · Electrochemical Energy Reviews 투고 draft (미출판, DOI 없음, Received/Revised/Published 공란)** |
| 저자 | Yang Li¹, Xianyi Zhao¹, Jiachen Hu¹, Huan Li¹, Dabing Li², Peng Lei¹, Xiaoxue Zhao³, **Hong Liu³,⁴,***, **Ce-Wen Nan³**, **Li-Zhen Fan¹,⁴,*** |
| 소속 | ¹ Institute for Advanced Materials and Technology, **USTB(北京科技大)** · ² CDLCEM, Zhengzhou Univ. · ³ State Key Lab of New Ceramics and Fine Processing, **Tsinghua** · ⁴ State Key Lab of New Ceramic Materials, Beijing Tsinghua Institute for Frontier Interdisciplinary Innovation |
| 교신 | fanlizhen@ustb.edu.cn (Fan) · liuhong.2023@tsinghua.org.cn (Liu) |
| Keywords | all-solid-state batteries; sulfide solid-state electrolyte; intrinsic stability; interfacial stability |
| Funding | National Key R&D Program of China 2023YFB2503902 · NSFC 22479009 · Beijing NSF QG26003 |
| 유형 | **리뷰(자체 데이터 0)** — 본문 56 pp, refs 239, Figures 26 (part 3–4가 figure pages) |
| 그룹 맥락 | **[Li25] CuBr₂ 논문(ESM 2025, ref 218)·자기 그룹 terpolymer 막(ref 88, AEM 2026)의 모그룹** — 우리 litdb와 직접 연결 |
| 동기 | 황화물 SE가 σ·성형성으로는 상용화 최근접이나, **재료 고유 불안정(공기/용매/열/전기화학/기계) + 전극 계면 반응**이 실용화 핵심 병목 → "안정성" 관점의 체계적 종설 필요 |

## 3. 리뷰 구조 지도 (섹션 트리)
```
1 Introduction
2 All Solid-State Batteries
  2.1 ASSB 장점 5개: ①안전 ②에너지밀도(LMA 3860 mAh/g·>5V창) ③수명 ④온도적응(−30~>150 °C) ⑤구조설계 유연성
  2.2 SE 재료 4군 비교 (polymer/oxide/halide/sulfide) — 이상적 SE 기준 제시
  2.3 황화물 SE 우위 4개: ①고속 이온수송 ②가공성/가소성(cold-press) ③계면 호환 ④스케일러블 합성
3 Intrinsic Stability of Sulfide SEs   ← 재료 고유 5축
  3.1 Air / 3.2 Solvent / 3.3 Thermal / 3.4 Electrochemical / 3.5 Mechanical
4 Interface of Sulfide/Cathode
  4.1 문제: 4.1.1 화학·전기화학 불안정 → 4.1.2 고전압 반응(O 방출) → 4.1.3 기전(HOMO·공간전하) → 4.1.4 화학-기계 결합실패
  4.2 전략: 4.2.1 복합양극 조성/공정 최적화 → 4.2.2 코팅 → 4.2.3 신규 CAM(할라이드·황화물·균질 S-Se)
5 Interface of Sulfide/Anode
  5.1 문제: 5.1.1 덴드라이트 핵생성/성장 → 5.1.2 미세구조 결함×전자전도 시너지 → 5.1.3 기계 불일치 → 5.1.4 계면 진화(공극)
  5.2 전략: 5.2.1 음극재 최적화(흑연/Si/합금/Li-free) → 5.2.2 SE 개질(할로겐/F/LiI/복합) → 5.2.3 SEI 구축(무기/폴리머/in-situ/LiF/gradient/압력)
6 Summary and Future Prospects — 미래 4방향
```

## 4. 핵심 수치 총정리 (리뷰 본문·그림에 등장하는 **모든** 정량값)
> ⚠ **정직 note**: 이 리뷰는 **수치가 드문 정성 리뷰**다. 셀 성능(용량 유지율 %, CCD mA/cm², 사이클 수)은 본문에 **거의 등장하지 않고** "excellent cycling stability" 식 정성 서술로 대체된다 — 유지율 %가 필요하면 개별 원전(refs)을 파야 함. 아래는 실제로 등장하는 정량값 **전부**.

### 4.1 전도도·재료 스펙
| 값 | 대상 | 위치 |
|---|---|---|
| σ(RT) 10⁻³~10⁻² **mS** cm⁻¹ | 황화물 SE (⚠ **draft 단위 오타** — §2.2의 10⁻⁴~10⁻² **S**/cm과 모순; 액체 상회 주장과도 안 맞음) | Intro |
| σ(RT) 10⁻⁴~10⁻² S/cm | 황화물 SE (정상 표기) | §2.2 |
| σ(RT) ~10⁻² S/cm | LGPS (액체 전해질급) | §2.3 |
| σ(RT) 10⁻⁷~10⁻⁵ S/cm | 폴리머 SE (PEO/PAN/PVDF + LiTFSI/LiClO₄/LiDFO₄) | §2.2 |
| σ(RT) ~10⁻⁴ S/cm | 산화물 SE (garnet/perovskite/NASICON) | §2.2 |
| 이상적 SE 기준 | σ>10⁻³ S/cm·t_Li≈1·ESW>4.5 V vs Li⁺/Li·저 σ_e·기계강도·저비용 | §2.2 |
| >5 V | SE류 일반의 넓은 전압창 주장(oxide) | §2.1/2.2 |
| 소결 >1000 °C | oxide SE 치밀화 요구(황화물은 RT cold-press) | §2.3 |
| 3860 mAh/g | LMA 이론용량 | §2.1 |
| −30 °C 이하 / >150 °C | SE 저온 가동·고온 구조안정(열폭주 없음) | §2.1 |

### 4.2 공기/용매 안정성
| 값 | 의미 | 위치 |
|---|---|---|
| ΔE_ad(H₂O) LPSC **−1.63/−1.54 eV** vs LPSOCF **−1.19/−1.11 eV** (가스/액상) | O·F 치환이 물 흡착을 약화 (Fig 3a, ref 81) | §3.1 |
| H₂S 발생·Li₂O/LiOH 부산물 | 가수분해 산물(HSAB: S²⁻ soft base ↔ H soft acid; O는 격자 Li 산화) | §3.1 |
| σ 유지 0→3 days (1-undecanethiol 코팅, 21.9→7.2 %RH 별) | 소수성 분자층이 습윤공기 처리 가능케 함 (Fig 3d, ref 86) | §3.1 |
| Li₇P₃S₁₁ σ_SE'/σ_SE vs donor number: decane·1,2-dichloroethane·toluene ≈1 / anisole 약간↓ / 1,4-dioxane ~0.1 / PC·propanenitrile·2-butanone·diglyme "overload"(붕괴) | 용매 극성(donor number)↑ → 열화↑ (Fig 4a, ref 92) | §3.2 |
| E_ad(toluene@LPSClInF) = **−0.12 eV** | InF₃ 치환이 용매 내성 부여; PS₄는 공격받아 P₂S₆+Li₃P, InS₄는 무분해 (Fig 4c, ref 97) | §3.2 |

### 4.3 열 안정성
| 값 | 의미 | 위치 |
|---|---|---|
| **400–500 °C** | LGPS·LPSCl·Li₇P₃S₁₁ 결정구조 유지 상한(불활성 분위기) — 카보네이트 액체전해질 대비 압도적 | §3.3 |
| **200–300 °C** | 충전 상태 high-Ni CAM(예 LiNi₀.₈Co₀.₁Mn₀.₁O₂) 격자 불안정 → 반응성 산소종 방출 → 황화물과 강발열(P–S 절단, P₂Sₓ·SOₓ·금속황화물 생성) | §3.3 |
| 발열량 **~40–50 % 감소** | 성형 압력↑ → 계면에 dense amorphous P₂Sₓ 반응층 in-situ 형성 → O 확산 차단 (Fig 5d–f, refs 108–109) | §3.3 |
| 200→400 °C 가열 시퀀스 | SE/Li 시료별 발화 여부 상이 — LPSCl계는 외관 안정, 일부 조성(사진 3행)은 발화 (Fig 5c, ref 99; ⚠ 라벨 저해상) | §3.3 |
| Th₀ 삼원상도(Li/P/S 전 비율)·**Th′ 도핑 서술자**(주기율표 전 원소, Li₃PS₄ 기준) | 조성-가중 결합에너지형 열안정 서술자 (Fig 5d,e; ref 109 InfoMat 2022; ⚠ 식 일부 판독불가) | §3.3 |

### 4.4 전기화학 안정성 (ESW)
| 값 | 의미 | 위치 |
|---|---|---|
| **LGPS 고유창 ≈1.7–2.1 V vs Li⁺/Li** | first-principles 진짜 열역학 창은 CV 겉보기 창보다 훨씬 좁음 | §3.4 (ref 114) |
| 환원 산물 **Li₂S·Li₃P** / 산화 산물 **P₂S₅·GeS₂·S/폴리설파이드** | 창 밖 분해 방향 | §3.4 |
| 황화물 산화전위 **≈2 V** | 4.1.1 재확인 — S²⁻ 우선 산화, 원소 S·폴리설파이드·인황화물·금속황화물 생성 (refs 130–131) | §4.1.1 |
| 계면 3유형 | ① 열역학 안정 ② mixed ion–electron conductive(MCI: Li₂S·Li₄GeS₄·P₂Sₓ) ③ passivated(SEI형: 고 σ_ion·저 σ_e) — ③이 바람직 | §3.4 (ref 116 Wenzel) |
| **2.5–4.1 V** | LPSCl–NCM 실작동 구간에서 산화분해 진행 관측 (Fig 8d, ref 137) | §4.1.2 |
| Fig 6d 창 모음: **LiPON 0.7–1.1 V · LGPS 1.71–2.14 V · LLZO 0.05–2.91 V · Li₃YCl₆ 0.6–4.23 V**; 0 V 산물(Li₃P/Li₃N/Li₂O·Zr/Li₂O/La₂O₃·Y/LiCl)·5 V 산물(N₂O₅/P₂O₅/O₂·GeS₂/P₂S₅/S·La₂Zr₂O₇·Cl₂/YCl₃) | SE 4군 열역학 창 표준값(Zhu/Mo 계열) | Fig 6d (ref 33) |
| Fig 6c LPSCl large-potential phase diagram | Li uptake per f.u. 계단: 저전압 Li₃P+Li₂S+LiCl(환원 최종) → Li₂S+P+LiCl → **안정창(~1.7–2.1)** → 산화측 Li₃PS₄+LiCl+S → P₂Sₓ+LiCl+S (⚠ 일부 라벨 저해상) | Fig 6c (ref 33) |
| Fig 8b LPSCl 작동창 도식 | LPSCl 환원/산화 한계 박스(≈1.7–2.1)와 Li-ion/Li-S 화학의 전위영역 대비 | Fig 8b (ref 134 Tan) |

### 4.5 기계 안정성
| 값 | 의미 | 위치 |
|---|---|---|
| **E(Young) 10–30 GPa** | 황화물 SE — oxide보다 훨씬 연함(접촉 유리, buffer 가능) | §3.5 |
| **파괴인성 K_IC 0.2–0.4 MPa·m¹ᐟ²** | 낮음 → 초박막 SE·반복응력에서 취성파괴 위험 | §3.5 (refs 123–124) |
| 입자 **>~3 µm** | 계면반응 부피팽창의 탄성 변형에너지 축적 → 파괴인성 초과 시 입자 파쇄 | §3.5 |
| 입자 **<1 µm (서브미크론)** | 부피팽창 균일 분산 → 응력집중↓, 균열 대신 협동변형 | §3.5 |
| 펠릿 **>360 µm** vs 시트 **<50 µm** | 랩 펠릿→대면적 박막 시트 전환 시 표면 불균일·저강도·내부결함 (Fig 7a, ref 124) | §3.5 |

### 4.6 양극·음극·셀 수치
| 값 | 의미 | 위치 |
|---|---|---|
| 면적용량 현재 **1–2 mAh/cm²** vs 목표 **>3 mAh/cm²** | 액체계와 경쟁하기 위한 문턱 | §4.2.1 |
| void 분율 **3.95 % → 1.19 %** (cycled SC811 vs AZ@SC811) | 코팅/구조 개선이 사이클 후 공극 억제 (Fig 12d, ref 161, synchrotron XCT) | §4.2.2 |
| 금속염화물 CAM 변환용량 수백 mAh/g·**>1500 Wh/kg**급 막대 | LiCl~CuCl₂류 비교 (Fig 14b, ref 167) |§4.2.3 |
| Li-free 변환 양극 **>1200 Wh/kg** | CuF₂·FeF₃·FeS₂·V₂O₅ 등 전위 vs 용량 산포 (Fig 15a, ref 169) | §4.2.3 |
| **Si 리튬화 부피팽창 ~300 %** | Si 음극 기계 실패 근원(전기화학 분해가 아니라) | §5.2.1 |
| Ag→Li-Ag 합금층 두께 260→~440→~850→~1000 nm→(EoL) ~300 nm | anode-free Ag 중간층 미세구조 진화 (Fig 23b, ref 214) | §5.2.1 |
| 양극/음극 용량비(A/C)→1 | anode-free에서 비가역 Li 손실이 수명 직접 결정 (Fig 23c, ref 216) | §5.2.1 |
| 응력창(stack pressure window) 존재 | 압력 부족=공극/접촉손실, 과다=Li가 GB 침투·소성변형 — Li 변형기구 지도(grain size×응력)로 최적압 예측 (Fig 19d, ref 191) | §5.1.4/5.2.3 |

## 5. 섹션별 상세 (전 섹션)

### 5.1 §1–2 서론·ASSB·SE 4군
- LIB 한계(가연 유기전해액·이론 성능 한계) → ASSB = 차세대 중심. SE가 이온전도+분리막 이중 기능 → 액체·염·분리막·(일부)바인더 제거로 공정 단순화.
- **ASSB 장점 5**: ① 안전(불연·불휘발; 기계/열 충격 내성; 고탄성률이 덴드라이트 부분 억제) ② 에너지밀도(넓은 전압창→고전압 CAM; LMA 3860 mAh/g; bipolar 적층) ③ 수명(안정한 고체-고체 접촉층; 완만한 열화곡선) ④ 온도적응(−30 °C 가동, >150 °C 무열폭주) ⑤ 구조 유연(박막·플렉서블·적층).
- **SE 4군**: polymer(가볍고 유연하나 σ 10⁻⁷~10⁻⁵·좁은 창) / oxide(안정·>5 V이나 σ~10⁻⁴·취성·소결>1000 °C) / halide(고 σ·고전압 CAM 호환이나 LMA 불안정·습기·원료비) / **sulfide(σ 10⁻⁴~10⁻²·가소성·저온공정 — 최유망)**. 황화물 우위의 물리: S²⁻의 큰 반경·낮은 전기음성도 → Li⁺ 결합 약화 → free-ion 농도·이동도↑.
- **황화물 우위 4**: 고속수송(argyrodite·glass-ceramic 3D 채널) / cold-press 치밀화(계면 접촉) / 계면 호환(높은 CCD로 Li 증착 안정 주장) / 스케일러블(볼밀·고상·기계합성; 초박막 시트).

### 5.2 §3.1 Air Stability (공기/수분)
- **근원**: P–S·M–S(M=Ge,Sn,Si) 결합이 M–O 대비 결합에너지 낮고 분극률 큼 → H₂O/O₂ 공격에 취약. **HSAB**: S²⁻(soft base)가 물의 H(soft acid)와 결합 → P–S/M–S 절단 → **H₂S 방출** + 구조붕괴 + σ 급락; 동시에 O가 격자 Li 산화 → **Li₂O·LiOH** 부산물 → 계면상전이·수송 열화. 이론 확장: **Hard-Soft-Electron-Hole(HSEH) 이론**(Mulks, Chem 2024, ref 80)이 HSAB를 다전자계로 확장 — 전자·홀 거동으로 환경 자극 하 황화물 격자의 전자구조 진화 설명.
- **전략 3계열**: ① **격자 결합에너지 강화** — O²⁻ 부분도입 → 열역학적으로 강한 **P–O 결합** 형성 → 가수분해 속도↓ (Fig 3a: LPSC→LPSOCF ΔE_ad 완화; refs 81–83 — ref 83은 Li₅.₅PS₄.₅Cl₁.₅ O-doping!); 강한 M–S 결합 양이온 치환(격자 경도↑·분극률↓; Fig 3b = Zhu & Mo 설계원리, ref 84). ② **표면 공학** — 치밀 무기 보호층·소수성 유기/무기 하이브리드층(산화물 코팅, 기상증착 초소수층 Fig 3c ref 87, 1-undecanethiol 분자층 Fig 3d ref 86 → 습윤공기 처리 가능). ③ **조성 최적화/결함 제어** — 양이온:음이온 비·국소구조 조정으로 물 흡착능↓ 또는 초기 접촉 시 안정 passivation층 자발형성.
- 리뷰 평가: **근본 미해결** — 향후 HSAB 화학의 체계적 조절 + "공기안정성 정량 예측 이론모델"(결합에너지 강화·다중스케일 상전이 kinetics·전자-홀 결합·고체-기체 반응 열역학) 필요; 공기안정 ↔ σ ↔ 계면호환 ↔ 비용 동시 만족이 핵심 난제.

### 5.3 §3.2 Solvent Compatibility (습식공정 용매)
- 문제 설정: 기존 LIB 습식(슬러리·막 코팅) 인프라에 황화물을 태우려면 용매 내성이 필수 — 용매 불내성이 구조열화+계면실패+비용상승+일관성 저하 유발.
- **메커니즘**: 극성 유기용매 중 미량 수분도 가수분해(H₂S·Li₂O·LiOH); **NMP**(고유전율·강용매화)는 PS₄³⁻/P₂S₇⁴⁻와 **비가역 반응** → P–S 절단·구조단위 재배열 → 저전도 분해상. HSAB로 일반화: **P⁵⁺ = 비교적 soft Lewis acid** → 고립전자쌍 가진 극성 용매(N·O 함유)가 친핵 공격 → P–S 절단; 방향족 고리·무배위 관능기 용매(톨루엔·헵탄 등 비극성)는 불활성. donor number와 σ 보존율의 상관 (Fig 4a).
- **전략**: 공정 측 — 저극성/비극성 슬러리 용매 선택; **dry electrode 공정으로 원천 회피**. 재료 측 — **InF₃ 등 안정화 성분 도입**(격자 결합에너지↑·분극률↓ → 유기용매 침지 후에도 σ 유지, Fig 4c ref 97); 용매-호환 바인더 시스템·공용매(cosolvent) 전략(ref 98 Hofmeister "salting-in").

### 5.4 §3.3 Thermal Stability (열)
- **2단 구조**: (i) 전해질 자체 열분해 — 결정질 황화물은 불활성 분위기 **400–500 °C**까지 구조 유지(공유-이온 혼성 결합망·저휘발 성분); (ii) **전극과의 계면 열반응이 실제 한계** — 충전된 high-Ni CAM이 **200–300 °C**에서 반응성 산소 방출 → 황화물과 강발열(P–S 절단·S 산화 → P₂Sₓ·SOₓ·금속황화물) → 시스템 총발열↑·열 안전마진↓.
- **계면 미세구조의 조절 역할**: 복합양극 성형압↑ → 계면에 **dense amorphous P₂Sₓ 층** in-situ 형성 → 산소종 확산 차단 → **총발열 ~40–50 %↓** (Fig 5d–f) — "적당히 제어된 계면반응은 오히려 kinetic 안정층"이라는 역설.
- **재료 측**: 산소 도입(oxysulfide, P–O 비율↑·결합에너지↑) → 고온 분해경향↓; 양극 표면 **LiNbO₃·Al₂O₃** 코팅 → 산소 방출 buffer + 직접 접촉 차단 → 발열 onset 지연.
- **계산 콘텐츠**: Li/LGPS 계면 AIMD 시간열 스냅샷(0→11.7 ps, 사면체 붕괴; Fig 5b, ref 107 cryo-EM 논문) + **Th₀/Th′ 열안정 서술자**(Li/P/S 전 조성 삼원상도 + Li₃PS₄ 도핑 주기율표 지도; ref 109) — 조성가중 결합에너지형 스칼라로 열안정을 스크리닝하는 "intrinsic theoretical paradigm".

### 5.5 §3.4 Electrochemical Stability (전기화학)
- **핵심 프레임**: 진짜 열역학 창(first-principles)은 CV 겉보기 창보다 **크게 좁다** — LGPS ≈**1.7–2.1 V**. 하한 아래 환원(Li₂S·Li₃P), 상한 위 산화(P₂S₅·GeS₂·S/폴리설파이드). 둘 다 큰 열역학 구동력 → 황화물은 넓은 전압범위에서 **본질적 준안정(metastable)**. 실제 셀이 창 밖에서 도는 이유 = **분해산물 계면막의 kinetic 안정화** — 초기 분해막이 이후 반응경로·속도를 지배.
- **계면 3유형**(ref 116, Wenzel): 열역학 안정 / **MCI(혼성 전도)** = 지속 분해 / **passivated(SEI형)** = 고 σ_ion·저 σ_e — 세 번째가 목표.
- 양극측: 고전위 layered oxide 작동전압 ≫ 황화물 임계 → **산화안정 oxide buffer 코팅**으로 화학퍼텐셜 구배 완화. 음극측: 분해산물이 전자전도성이면 지속 부반응+덴드라이트 가속 → **인공 계면층(이온전도·전자차단)** 구축 (Fig 6f, ref 22).
- 결론: "황화물의 전기화학 안정성은 고유 열역학이 아니라 **계면반응이 지배하는 kinetic 안정성**" — 양극·음극 모두 안정·제어가능·전자절연 계면층 구축이 핵심 과학경로.

### 5.6 §3.5 Mechanical Stability (기계)
- 근원 = **화학-기계 결합 실패**: 저 E(10–30 GPa)·소성변형 능력은 접촉에 유리하나 **낮은 파괴인성(0.2–0.4 MPa·m¹ᐟ²)** + 계면반응 부피효과가 취약점. Li 접촉 분해(Li₂S·Li₃P 등)는 모상과 몰부피가 크게 달라 → 계면 국소 부피팽창 → SE 입자 내 인장응력 집중 = **마이크로크랙 핵생성의 1차 구동력**; 입자 >~3 µm는 탄성 변형에너지 축적 → 파쇄 → 이온망 단절 + 저임피던스 경로(덴드라이트 침투로) → 내부단락.
- **완화**: 입자 서브미크론화(<1 µm, 응력 균일분산·협동변형); **황화물-폴리머 복합 SE**(유연상이 응력 분산, 파괴인성↑; refs 125–127); 조립압 최적화; 계면반응 부피변화가 작은 조성 개발·도핑으로 분해경로 조절 (Fig 7c–d).
- 요지: 기계 안정성 = 단일 재료 파라미터가 아니라 **계면 화학반응 × 미세구조 × 외부 구속의 결합 효과**.

### 5.7 §4.1 양극 계면 — 문제
- **4.1.1 화학·전기화학 불안정**: 황화물 산화분해전위 ≈2 V ≪ layered oxide 고SOC 작동전위 → 접촉 즉시/충전 중 산화분해 불가피. 개시 = **S²⁻ 우선 산화** → 원소 S·폴리설파이드·인황화물·전이금속 황화물 (refs 130–131 = Zhu/He/Mo·Hakari). 산물 대부분 절연 또는 **MCI**(Li₂S·Li₄GeS₄·P₂Sₓ) → 임피던스 누적 + 전자경로 제공 → **자가촉진 비가역 열화**.
- **4.1.2 고전압 시너지**: high-Ni CAM 탈리튬화 → 격자산소 불안정 → **O²⁻/O₂ 방출** → S²⁻와 직접 반응 **SOₓ** 생성; 계면반응이 "전해질 단방향 산화"에서 "**양극↔전해질 양방향 결합반응**"으로 전환 — O-vacancy 풍부 TM oxide 표층이 다시 황화물과 반응(금속황화물·인산화물, Fig 8c). LPSCl–NCM은 **2.5–4.1 V** 운전창 내에서도 지속 분해(Fig 8d) — Ni-rich NCM/NCA에서 특히 심각.
- **4.1.3 기전 (전자구조 관점)**: ① **에너지준위 불일치** — 충전 시 양극 전기화학퍼텐셜이 황화물 **HOMO 아래**로 → 전해질→양극 전자 이동 = 산화분해(황화물은 HOMO 높아 취약); ② **Li 화학퍼텐셜 차** — oxide 양극이 Li 퍼텐셜 높음 + 황화물의 약한 Li 결합 → Li이 SE→양극 자발이동 → **Li-depleted 공간전하층** → 계면 σ↓·임피던스↑; ③ 단 공간전하층이 유일 원인 아님 — **조성변화·부산물 축적이 더 직접적**(refs 116/133/136) → 계면 불안정 = 준위불일치 × 퍼텐셜 구동 Li 이동 × 반응층 성장의 합.
- **4.1.4 화학-기계 결합**: 고체-고체 접촉의 낮은 습윤성·제한된 유효접촉면적 → 높은 계면저항 기본값; 사이클 중 CAM 상전이/부피변화 ↔ SE 산화분해 부피수축의 **불일치 응력** → 균열·이차입자 파쇄·접촉손실; in-situ 역학측정: **전해질 산화의 부피변화 자체가 응력원**(ref 141 operando 압력) → 화학×기계 결합이 열화를 비가역화.

### 5.8 §4.2 양극 계면 — 전략
- **4.2.1 복합양극 최적화**: ① SE 질량분율 = 이온/전자 수송 **동적 평형점** 탐색(과다 CAM=이온망 단절, 과다 SE=전자망 단절; Fig 9a). ② 면적용량 1–2 → **>3 mAh/cm²** 가려면 고로딩 수송·분극 해결 — 양극측 **고전도 할라이드 SE 저로딩** 전략(Fig 9b, ref 145 Nat Energy). ③ **도전재**: carbon은 e⁻수송↑이나 고전위서 황화물 산화 촉진 + **0D carbon black은 3D 패킹으로 전해질 부피 잠식**(이온채널 협착·국소 전자집중) vs **1D/2D 섬유·플레이크**는 공간 잠식↓(Fig 9c; ⭐ 우리 그룹 [KimCA] 0D/1D 결론과 동일 방향) — 함량도 정밀조절 필요. ④ **gradient 설계**: 집전체 쪽 도전재↑ / 분리막 쪽 SE↑ (Fig 9d). ⑤ 공정: 기계혼합(수동<제어 볼밀; 과도 볼밀은 CAM 결정 손상)·quasi-coated 구조; **성형압**: 압↑→기공↓접촉↑이나 과압은 채널 꼬임·이방성 접촉(Fig 10b); **단결정 CAM + gradient 결합**(입계밀도↓·응력집중↓, Fig 10c–d).
- **4.2.2 코팅**: 이상적 코팅 4조건 — 고전압 열역학/화학 안정 · 충분한 σ_ion(저장벽) · **최소 σ_e** · 기계 유연성; +두께 정밀제어(얇으면 부반응 억제 실패, 두꺼우면 확산저항). 재료 계열: **LiNbO₃(ref 111)·Li₂CO₃(ref 155, 피복률 조절)·LiTa₂PO₈/LATPO(ref 156, LCO 4.6 V)** 등 무기 산화물/Li염(졸겔·in-situ·ALD); **LiPON 비정질**(넓은 창+성막성, 결정립계 없는 균일 조성, Fig 11d); **이중/다층 복합 코팅**(열·전기화학·수송 시너지, ref 112); **유기/유무기 하이브리드**(부피변화 흡수 탄성 buffer, MLD/in-situ 중합, Fig 12a–b); **전자구조 조절 코팅**(PEDOT로 CNT를 반도체화 Fig 12c; 2D graphene-like carbon으로 물리차단+전도조절 ref 162); **도핑+표면상 조절**(rock-salt/gradient 표층으로 CAM 구조 안정화, Fig 12d).
- **4.2.3 신규 CAM (비산화물)**: 작동전위가 황화물 안정창 근처 → 산화 구동력 자체를 제거; O 방출 없음. ① **할라이드 양극**: Li₁.₃Fe₁.₂Cl₄(ref 163 Nature)·Li₂FeCl₄(164)·Li₂₋₂ₓFe₁₊ₓCl₄(165) — Fe³⁺/Fe²⁺ 다전자 redox·저변형(Li/Fe비로 zero-strain 설계)·계면 임피던스 성장 느림; FeCl₃(166 Nat Sustain) 단순조성·저비용; 금속염화물 일반: 낮은 반응전위·약한 산화력·유연 기계특성 + **Cl 매장량/가격 압도적 우위**(Fig 14c). ② **금속황화물**: FeS₂ 등 초고용량·SE와 화학 유사(계면 호환)하나 **변환반응 부피변화**가 한계 → 나노구조·유연 전도망·pre-sulfidation. ③ **균질 황(S–Se) 화합물**: 단일 결정상에 e⁻+Li⁺ 혼성수송 내장 = "**cathode homogenization**"(ref 173 Nat Energy; Li₂SeₓS₁₋ₓ ref 174) — 다상 계면 의존 탈피, 저변형.

### 5.9 §5.1 음극 계면 — 문제
- **3대 결합 실패**: ① 덴드라이트 핵생성·성장 → 단락; ② LMA↔황화물 지속 전기화학 분해 → 고임피던스 계면상 축적; ③ 증착/탈리 부피변화 응력 → 접촉열화 — 상호증폭 공진화.
- **5.1.1 덴드라이트**: 액체와 달리 **SE 내부에서 핵생성**해 저임피던스 경로 따라 전파. 2단계: **핵생성**(계면 근처 subsurface 기공·결함·마이크로크랙 — 국소 이온플럭스 집중·전기장 왜곡·저증착장벽) → **성장**: "**wedge-opening**" 기전 — 균열 **후단**에서 Li이 지속 주입되어 쐐기로 벌림(전통적 선단응력 모델과 다름); 쐐기응력 > 파괴인성 → 불안정 전파 → 관통단락 (ref 177 Ning Nature 2023). 원자 관점: **SEI 내부도 핵생성 자리** — 비정질 분해산물 복합층의 **밴드갭 협소화/전자전도** → 전자가 계면층 침투 → Li⁺ 국소환원 = "**dead Li**" 클러스터(ref 178, MD; Fig 16c) → 예측불가성↑. 전류밀도↑ → 과전위↑ → mossy/dendritic 전환; 박리 시 hollow shell = dead Li 축적.
- **5.1.2 결함×전자전도 시너지**: 불순물·GB·균열·국소 불균일 = 국소 전류밀도↑ = 우선 개시점. **Li₃PS₄의 특정 사면체 자리·결함영역은 Li 증착장벽 낮음**(Fig 17a, ref 180 — "ionization level" 서술자로 분해상별 덴드라이트 억제/성장 판별); 황화물의 **비무시 고유 σ_e**(결함·분해산물 영역에서 특히) → 전해질 내부에서 Li⁺+e⁻ 재결합 = **음극에서 먼 곳 자발 Li 핵생성**(ref 181; ref 175 Nat Mater "Li filament"); 다결정 GB·입계 균열 = 팽창경로, 표면 전자전도가 전기장 왜곡 → **CCD 하락**(Fig 17c–d, ref 182 Nat Commun 2025 원자 기전).
- **5.1.3 기계 불일치**: Li 부피변화 ↔ 황화물 취성 → 응력집중; 증착=압축응력, 탈리=공극/접촉손실; 주기 응력 → 기존 균열 전파 + GB mixed-mode 파괴 → 새 덴드라이트 경로(Fig 18a–b); 분해상 MCI 형성 → 전자전도↑ → "**기계-화학-전기 3중 결합 실패경로**". CCD = 계면 치밀도 × σ_ion × 기계 건전성; 고전류 = 미세 whisker/dendrite 경향; 박리 지연 backfill → 국소 전류 증폭(Fig 18c).
- **5.1.4 계면 진화 (공극)**: 탈리속도 > Li 공공 확산 문턱 → **µm급 공극** 누적 → 접촉면적↓·분극 급증; 공공 확산은 농도구배+응력장 동시구동 → 새 증착 hotspot(Fig 19a); **적정 stack pressure** → LMA 탄성/creep 변형 → 접촉 유지·공극 지연(Fig 19b–d); 과압 → Li이 SE 입계로 압출 → 덴드라이트/구조손상 → **압력창 존재**; LMA의 강환원성상 대부분 황화물과 열역학 공존 불가 → 분해 계면상(저 σ_ion) 지속 축적, 전자전도상 포함 시 연쇄반응·열폭주까지.

### 5.10 §5.2 음극 계면 — 전략
- **5.2.1 음극재 최적화**:
  - **흑연**: 초기 상용화 최현실적(인프라·저팽창·수명) — 단 황화물과 직접 접촉 시 저전위 환원분해 산물이 전자절연+저이온전도+무정형·제어불가 성장 = 액체식 자가 passivation 부재. **표면 비정질 카본이 계면반응 증폭**(고표면적·결함states·전자전달; ref 194 LGPS+carbon) → **고결정 흑연**(비정질 제거)이 얇고 치밀·고이온전도 계면층 형성(Fig 20b) — SE 비율 줄여도 안정 = "**계면 화학안정성 > 이온전도**"; 흑연 표면 기능성 코팅으로 전자구조 조절(전자 hopping 차단+Li⁺ 수송 유지; MoON@Gr Fig 20c). 핵심 = 덴드라이트가 아니라 **저전위 환원분해 억제**.
  - **Si**: 실패 주인 = 전기화학 분해가 아니라 **~300 % 부피팽창** — 고체계는 구조재배열/계면 슬립으로 흡수 불가 → channel-type 균열·계면 delamination·개폐 반복 microcrack 망(XCT, Fig 21a); 3-레벨 동시 최적화(입자: 나노화·도핑 / 계면: buffer 코팅 / 전극: 입도분포·기능 바인더·집전체 결합, Fig 21b); 순수 Si 단독은 난망 — **흑연 복합**이 현실 절충.
  - **합금(Li-Al 등)**: 흑연↔LMA 가교; 1주기 결정↔비정질 전이·비가역 팽창·응력 히스테리시스; 입자 재배열의 응력 자기조절은 구조 건전성 희생; **입자 미세화**(기공 buffer)·**압력-항복강도 매칭**(부족=공극, 과다=비가역 소성; Fig 22c) ·**pre-lithiation·저탄성 buffer상**(Fig 22d Li₄.₄Si-nSi).
  - **Li-free(anode-free)**: 집전체 위 in-situ Li 증착 — 최고 에너지밀도·공정 단순(Fig 23a); 성패 = 증착 가역성/균일성(불균일→고표면적→dead Li→한정 Li 재고 소진); **집전체/SE 사이 기능성 interlayer**(가역 합금화 → 균일 핵생성·저곡률 증착·전자 buffer; Fig 23b); **CE 극한 민감**(A/C≈1이면 미소 비가역도 수명 직결) → 양극 비가역까지 통합 분석 필요(Fig 23c).
- **5.2.2 SE 개질** (⭐ 우리 캠페인과 최밀접): 헤테로원자 도핑 = 국소배위·캐리어 이동·계면 반응산물 재구성 3중 레버(Fig 24a–b — **각각 우리 [Liu23] MgF₂·[Li25] CuBr₂ digest 그림!**). **할로겐 도핑 이중효과**: (i) σ↑ → 농도분극↓·Li⁺ 플럭스 균질화(kinetic); (ii) 할로겐-농축 영역이 LMA 접촉 시 **in-situ Li-halide 계면층**(전자절연·고이온전도) 자발형성 → 전자침투 차단·환원분해 정지(Fig 24c 고엔트로피 argyrodite Cl/Br 점유↔σ, ref 68). **F 도입** → in-situ 불화물층(고계면에너지·전자절연) → 균일 증착·핵생성 억제(Fig 24d). **LiI 도입** → 증착/탈리 중 **가역 확산·재구성하는 동적 self-healing LiI 나노층**(플럭스 균질화·국소 전류피크↓) + LiI 가소성이 입자간 공극 충전(Fig 24e–f; "dynamic-mechanical-electrochemical" 다중 시너지). **세라믹/폴리머 복합 SE**: 황화물=수송, 폴리머=응력 buffer; 화학결합 anchoring으로 상분리·공간전하 제거(ref 223).
- **5.2.3 인공 SEI 구축**: **이상 SEI 4조건** = 나노스케일 두께(분극 최소) · 연속 저장벽 Li⁺ 경로 · **고유 전자절연**(전자누출 차단 → LMA 유효 화학퍼텐셜을 SE 창 안으로) · 구조 건전성/기계 적응성. 전략 사다리: ① **무기/복합 interlayer**(µm 황화물 + nm oxide/인산염 속이온전도체 다상구조 — oxide=전자장벽·화학안정, 황화물=σ 유지; Fig 25a) ② **폴리머 초박층**(in-situ 가교 치밀망 — 부반응 제거+기계 buffer+Li⁺ 용매화/수송 유지) ③ **in-situ 희생층/혼합전도층**("trading reaction for stability": 할라이드·금속염이 LMA와 자발반응 → Li 합금 골격+Li-rich 이온전도상, 화학퍼텐셜 차 완충; Fig 25b) + **하이브리드 전도 interlayer**(고 σ_ion 무기상 + 전자수송 tunable carbon/nitride상 → 계면 전기화학 퍼텐셜 구배 제어; Fig 25c) ④ **생체모방/탄성층**(강화학결합 SEI — 접착·균일 피복·자가치유; Fig 25d–e) ⑤ **LiF-rich SEI**: bulk LiF는 σ_ion 낮지만 **나노스케일 저확산장벽+고계면에너지** → Li⁺ 플럭스 균일 유도·**self-limiting 전자장벽**(Fig 26a–c) ⑥ **gradient 계면층**: LMA측 Li-합금층(유효 화학퍼텐셜↓·기계강도↑·불균일 증착 억제) + SE측 Li염층(전자절연·이온선택 수송) 연속 조성/전도도/기계 구배(Fig 26d–f) ⑦ **압력 시너지**: 임계압 이상 유지(접촉·공극 억제) — 창 안에서 creep 재접착; 유연 buffer/고변형 SE로 저압화(refs 238–239).

### 5.11 §6 Summary & Future
- 재료: σ는 액체급 도달 = 산업화 최근접; 그러나 공유-이온 혼성 결합 특성상 공기·수분·용매에 화학 불안정, 고온·고전압서 열/전기화학 창 제한, **저 파괴인성·제한된 소성** → 안정성 문제 = 화학×전기화학×열×기계 **결합 효과**.
- 양극 계면: 산화분해→고임피던스층→분극·용량감쇠 + CAM 구조진화·TM 용출·O 방출이 가속 + 화학-기계 결합실패; 전략(조성/미세구조 최적화·코팅·신규 CAM)은 진전했으나 장기 유효성·공정 복잡성·고로딩 호환 검증 필요.
- 음극 계면: 더 복잡 — LMA 반응성·부피변화 → MCI 계면·연속 진화·단락; 미세구조 결함·국소 전도 불균일·기계강도 한계가 Li 증착과 시너지 → 덴드라이트. **무기/유기 복합 계면층·LiF/Li₃N-rich 계면·gradient 계면**이 전자차단·플럭스 균질화·기계 불일치 완화에 유효.
- **미래 4방향**: ① 재료 — "passive stabilization"→"**intrinsic stability**"(다중 음이온 시너지·국소 rigid-flexible 하이브리드 구조·저에너지 결함공학으로 반응 구동력 자체 축소) ② 계면 — 정적 이해→**동적 조절**(in-situ 특성화 + 다중스케일 시뮬레이션으로 시공간 진화 규명) ③ 구조/공정 — **저압/무압 설계**(랩 성능의 고압 의존 탈피) ④ 시스템 — **평가 표준화**(전해질 두께·로딩·시험압·사이클 조건 통일 없이는 전략 간 비교 불가).

## 6. 황화물 SE 계열 카탈로그 (리뷰가 다루는 재료 패밀리)
| 계열 | 대표 조성 | 리뷰 내 key 수치/역할 | refs |
|---|---|---|---|
| **Glass / glass-ceramic LPS** | xLi₂S·yP₂S₅ (Li₃PS₄, **Li₇P₃S₁₁**) | 용매 민감성 대표(Fig 4a donor-number 실험은 Li₇P₃S₁₁); 400–500 °C 결정 안정; Li₃PS₄ = Th′ 도핑 지도·덴드라이트 ionization-level 분석 기준물질 | 15–17, 92, 109, 180 |
| **LGPS형 (thio-LISICON계)** | Li₁₀GeP₂S₁₂ | σ ~10⁻² S/cm(액체급); **고유창 1.71–2.14 V**; 환원 Li₂S+Li₃P / 산화 P₂S₅+GeS₂; Li/LGPS AIMD 붕괴(Fig 5b); carbon 첨가 유해(ref 194) | 64, 67, 102, 114–115 |
| **Argyrodite** | Li₆PS₅X(X=Cl,Br,I), **LPSCl**, Cl-rich Li₅.₅PS₄.₅Cl₁.₅(ref 83, 111) | 본문 실전 사례 최다: LPSCl–NCM 2.5–4.1 V 분해(Fig 8d)·Li/LPSCl 덴드라이트 XCT(Fig 16b)·MD SEI 핵생성(Fig 16c)·고엔트로피 Cl/Br 점유↔σ(Fig 24c)·CuBr₂/MgF₂ 도핑(Fig 24a–b) | 18–19, 65, 68, 81–83, 137, 177–178, 217–218 |
| **Oxysulfide / O·F 치환** | LPSOCF, O-doped Li₅.₅PS₄.₅Cl₁.₅, F-doped LGPS, InF₃-LPSCl | 공기(ΔE_ad 완화)·용매(E_ad −0.12 eV)·열(P–O 결합↑) 3축 동시 개선 전략의 본체 | 77, 81–83, 97 |
| **Thioarsenate 등 변형** | Br-rich Li 계열 | 공기안정+σ 동시 부스팅 예 | 76 |
| (비교군) oxide / halide / polymer / LiPON | LLZO·Li₃YCl₆·PEO계·LiPON | 창: LLZO 0.05–2.91 V·Li₃YCl₆ 0.6–4.23 V·LiPON 0.7–1.1 V; halide는 양극측 catholyte·LiPON은 비정질 코팅으로 재등장 | 33, 57, 62–63, 157 |

## 7. 열화 메커니즘 taxonomy (리뷰 전체를 분해한 분류 체계)
| # | 축 | 메커니즘 (개시 → 전파 → 실패) | 지배 인자 | 리뷰 위치 |
|---|---|---|---|---|
| D1 | **공기/수분** | S²⁻(soft base)+H₂O → P–S/M–S 절단 → H₂S↑ + Li₂O/LiOH → 채널 폐색·σ 급락 | 결합에너지·분극률·HSAB/HSEH | §3.1 |
| D2 | **용매** | 극성용매(고 donor number·N/O 고립전자쌍) 친핵공격 → P–S 절단·PS₄ 재배열 → 저전도 분해상 | 용매 극성·P⁵⁺ soft acidity | §3.2 |
| D3 | **열(고유)** | >400–500 °C 결정 분해/상전이 | 결합망·휘발성분 | §3.3 |
| D4 | **열(계면)** | 충전 CAM 200–300 °C O 방출 → S 산화 강발열(P₂Sₓ·SOₓ·MSₓ) → 열폭주 마진 축소 | SOC·CAM Ni 함량·계면 미세구조(P₂Sₓ 치밀층이 완화) | §3.3, Fig 8a |
| D5 | **전기화학-산화(양극)** | ~2 V 이상 S²⁻ 우선 산화 → S/폴리설파이드/P₂Sₓ/MSₓ (MCI) → 전자누출 → 자가촉진 분해·임피던스 누적 | 열역학 창(1.7–2.1)·HOMO 준위·분해산물 σ_e | §3.4, 4.1.1 |
| D6 | **전기화학-산화 × O 방출 (양방향)** | 반응성 O가 S²⁻ 산화(SOₓ) + O-vacancy 표층이 재반응 → 다상 후막 | 고SOC·Ni-rich | §4.1.2 |
| D7 | **공간전하/준위 불일치** | Li 화학퍼텐셜 차 → Li-depleted층; HOMO 위 전자 이동 | 준위 정렬(단 조성변화가 더 직접적) | §4.1.3 |
| D8 | **화학-기계(양극)** | CAM 부피변화 ↔ SE 산화 수축 불일치 → 응력집중 → 균열·접촉손실 → 비가역 | 입경(>3 µm 파쇄)·K_IC 0.2–0.4·성형압 | §3.5, 4.1.4 |
| D9 | **전기화학-환원(음극)** | LMA 접촉 → Li₂S·Li₃P 등 분해 → MCI면 지속분해 | 창 하한·산물 σ_e | §3.4, 5.1 |
| D10 | **덴드라이트** | subsurface 기공/결함 핵생성 → **wedge-opening**(균열 후단 주입) 전파 → 관통단락; SEI 내부 dead-Li 핵생성(좁은 gap 분해상 전자침투) | 결함밀도·파괴인성·**분해산물 밴드갭/σ_e**·전류밀도 | §5.1.1–5.1.2 |
| D11 | **고유 σ_e 내부 석출** | SE 내부 Li⁺+e⁻ 재결합 → 음극서 먼 Li 핵 → GB 따라 성장 → CCD↓ | σ_e(결함·분해상에서 증폭)·GB | §5.1.2 |
| D12 | **공극/접촉 진화(음극)** | 탈리속도>공공확산 → µm 공극 → 국소전류 증폭 → hotspot 재증착·분극 | 전류밀도·stack pressure(창 존재)·creep | §5.1.3–5.1.4 |
| D13 | **음극재 고유** | 흑연: 비정질 카본이 환원분해 증폭 / Si: 300 % 팽창 균열망 / 합금: 1주기 비가역·응력 히스테리시스 / anode-free: dead Li·CE 민감 | 재료별 | §5.2.1 |

## 8. 완화 전략 매트릭스 (재료 ↔ 전략 ↔ 리뷰가 보고하는 개선)
> ⚠ 개선 효과는 대부분 **정성 서술**(원전 수치 미전재). 정량이 있는 것만 숫자 표기.

| 전략 | 구체 재료/수단 | 표적 메커니즘 | 보고 개선 | refs |
|---|---|---|---|---|
| **O/음이온 도핑** | O²⁻→PS₄(P–O), LPSOCF, O-doped Cl-rich LPSCl | D1(가수분해)·D3/D4(열) | ΔE_ad(H₂O) −1.63→−1.19 eV; 가수분해 속도↓; 고온 분해경향↓ | 81–83, 89, 110 |
| **양이온/강결합 치환** | 강 M–S 양이온(Zhu-Mo 선택지도), InF₃, F-doped LGPS | D1·D2 | 용매 침지 후 σ 유지(E_ad −0.12 eV); 습기안정 | 77, 84, 97 |
| **표면 소수화/코팅(SE 입자)** | 초소수 기상증착층, 1-undecanethiol 분자층, 산화물 피복 | D1 | H₂S 억제; 습윤공기(7–33 %RH) 노출 0→3일 σ 유지 | 85–87 |
| **공정 회피** | 비극성 용매 슬러리·**dry electrode**·용매호환 바인더·cosolvent | D2 | 구조/σ 보존 | 95–98 |
| **성형압↑ (계면 P₂Sₓ 치밀층)** | 복합양극 가압 성형 | D4 | **총발열 40–50 %↓** | 99, 106–109 |
| **CAM 코팅** | LiNbO₃·Al₂O₃(열) / LiNbO₃·Li₂CO₃·LATPO·LiPON·다층(전기화학) / 유기·하이브리드(기계) / PEDOT@CNT·2D carbon(전자구조) | D4–D8 | 발열 onset 지연; 임피던스 억제; 사이클 안정↑; void 3.95→1.19 % | 111–112, 154–162 |
| **복합양극 설계** | SE 분율 동적 평형·1D/2D 도전재·gradient·단결정 CAM·압력 최적화 | D5·D8 + 수송 | 고로딩(>3 mAh/cm² 지향)·분극↓ | 142–153 |
| **신규 CAM** | Li₁.₃Fe₁.₂Cl₄/Li₂FeCl₄/FeCl₃(할라이드)·FeS₂(황화물)·Li₂SeₓS₁₋ₓ(균질 S-Se) | D5–D6 원천 제거 | 가역용량·완만한 임피던스 성장; zero-strain 설계; >1200 Wh/kg 잠재 | 163–174 |
| **음극재 공학** | 고결정 흑연(비정질 제거)·표면 코팅(MoON@Gr)·Si 3-레벨 설계·흑연-Si 복합·pre-Li 합금·interlayer(anode-free) | D13 | 얇고 치밀한 계면층·저 R_ct; 균열 억제(Li₄.₄Si-nSi "no cracks") | 192–216 |
| **SE 개질(음극향)** | 할로겐 도핑(in-situ Li-halide SEI)·F(불화물층)·LiI(동적 self-healing)·MgF₂/CuBr₂류 전자재분배·세라믹/폴리머 복합 | D9–D11 | 전자침투 차단·플럭스 균질화·공극 충전(가소성 LiI) | 41, 68, 97, 217–223 |
| **인공 SEI** | 무기 복합 interlayer·가교 폴리머 초박층·in-situ 희생층("trading reaction for stability")·하이브리드 전도층·생체모방 탄성층·**LiF-rich**·**gradient(합금/염 이중층)** | D9–D12 | 전자 self-limiting 장벽·균일 증착·자가치유·저압 운전 | 220–237 |
| **압력 조절** | stack pressure 창 유지·creep 재접착·Li 변형기구 지도 기반 최적압·유연 buffer로 저압화 | D12 | 공극 억제 vs GB 침투 회피의 절충 | 188–191, 238–239 |

## 9. DFT/계산 콘텐츠 ★ (리뷰가 *인용*하는 계산 — 자체 계산 아님)
- **grand-potential/상도 기반 ESW**: LGPS 1.7–2.1 V·Fig 6c LPSCl Li-uptake 상도·Fig 6d 4군 창 = Mo/Ceder–Zhu/He/Mo 계열(refs 114–115, 130, 33) — **우리 esw 파이프라인과 동일 방법**. 리뷰는 "진짜 열역학 창 ≪ CV 겉보기 창, 실운전은 kinetic passivation" 프레임을 그대로 채택.
- **계면 AIMD**: Li/LGPS 계면 시간열 스냅샷(0→11.7 ps 사면체 붕괴; Fig 5b, ref 107) — 열·환원 결합 시뮬. Li₆PS₅Cl/SEI/Li 3층 **대규모 MD**(t=0→100 ps)로 **SEI 내부 Li 클러스터 핵생성**(g(r)이 anode Li와 일치; Fig 16c, ref 178).
- **열안정 서술자 Th₀/Th′**(ref 109): Li/P/S 삼원 전조성 Th₀ 지도 + Li₃PS₄ 도핑 원소별 Th′ 주기율표 지도 — 조성·결합에너지 가중 스칼라 스크리닝(⚠ draft 그림 식 일부 판독불가). **우리가 아직 안 쓰는 축** — B₂O₃/O-doped 조성의 열안정 서열화에 이식 가능.
- **공기안정 DFT**: H₂O 흡착 배열/에너지(Fig 3a)·**가수분해 반응에너지 원소 지도 + 환원안정성 2D 선택 차트**(Fig 3b, Zhu & Mo ref 84) — HSAB의 정량판. 용매 공격 DFT(PS₄+용매 → P₂S₆+Li₃P vs InS₄ 무분해; Fig 4c).
- **덴드라이트 이론**: "**ionization level**" 서술자(분해상별 Li 증착 traffic-light; Fig 17a, ref 180) · 다결정 전위분포/Li⁺ 분포 시뮬(덴드라이트 관통 t=0→0.8 ns; Fig 17c–d, ref 182) · Li 변형기구 지도→최적 stack pressure 예측(Fig 19d, ref 191) · 미세구조 모델링(Fig 9a/10a: SOC·전류밀도·von Mises 3D 콘투어, refs 140/150).
- **전자구조 도핑 설계**: Mg/F 전자재분배(ΔE≈−2.0→−4.2, S-p 아래 Mg-s; Fig 24a = [Liu23]) · CuBr₂ ELF/구조(Fig 24b = [Li25]) · 고엔트로피 배열 엔트로피 ΔS_conf/R ↔ σ 상관(Fig 24c, ref 68) · PEDOT@CNT 밴드정렬(일함수/반도체화; Fig 12c).
- **방법 스펙트럼 총평**: 리뷰는 DFT(ESW/흡착/서술자)+AIMD/MD(계면·덴드라이트)+연속체(미세구조·압력)를 **한 서사로 엮지만 자체 계산은 0** — 모든 수치는 원전 소환. 무질서 처리·functional 등 **계산 디테일은 일절 없음**(리뷰 특성상 n/a).

## 10. Figure set ★ (전 26개)
| Fig | 패널·내용 | 원전 | 우리가 쓸 점 |
|---|---|---|---|
| **1** | 리뷰 전체 도식: (a) 고유 특성(공기/용매 polar attack·전기화학/열폭주·기계 gas/break) (b) 황화물/양극(간극·균열·박리·부산물·Li⁺ 확산 차단) (c) 황화물/음극(dead Li·불균일 전류·부산물·덴드라이트·부피변화) | 자체 | 우리 발표 "안정성 3분할(고유/양극/음극)" 오프닝 프레임으로 차용 |
| **2** | (a) 액체 LIB vs ASSB 구조 (b) 작동원리 (c) SE 6군 radar(이온선택성/산화·환원 안정성/화학·열·기계/집적/비용/ASR) (d) 대표 SE σ 산포(LGPS·LPS·argyrodite·thio-LISICON vs oxide vs polymer) | 1, 42, 50, 57 | σ 산포도(d) = 우리 서론 "황화물=액체급" 한 장 근거 |
| **3** | 공기: (a) H₂O 흡착 LPSC −1.63/−1.54 vs LPSOCF −1.19/−1.11 eV (b) 가수분해 반응E 원소지도+환원안정 선택차트 (c) 기상증착 초소수층 (d) 티올 코팅 σ vs 노출 0→3일 | 81, 84, 87, 86 | (a)(b) = 우리 O-doping·free-S 서사의 실험/DFT 사촌; (b) Zhu-Mo 차트는 도핑 후보 선별에 직접 사용 가능 |
| **4** | 용매: (a) Li₇P₃S₁₁ σ 보존율 vs donor number (b) 극성별 상호작용 기전 (c) InF₃-LPSCl 용매내성(E_ad −0.12 eV; PS₄→P₂S₆+Li₃P vs InS₄ 무분해) | 92, 24, 97 | 습식공정 스크리닝 기준(donor number)·우리 B–S 안정화와 동형 논리(강결합 단위=공격 면역) |
| **5** | 열: (a) SE vs 액체 분해온도 (b) Li/LGPS AIMD 0→11.7 ps (c) SE/Li 가열 200→400 °C 발화 시퀀스(⚠ 라벨 저해상) (d) Th₀ 삼원상도 (e) Th′ 주기율표 (f) 열안정 새 패러다임 도식 | 101, 107, 99, 109 | **Th′ 서술자 = 우리 도핑 조성 열안정 스크리닝의 즉시 이식 후보**; AIMD 계면 프로토콜 참고 |
| **6** | 전기화학: (a) CAM/황화물 에너지도 (b) SE 관통 화학퍼텐셜 진화 (c) LPSCl large-potential 상도(Li uptake 계단) (d) 4군 ESW(LiPON 0.7–1.1/LGPS 1.71–2.14/LLZO 0.05–2.91/Li₃YCl₆ 0.6–4.23 V + 0/5 V 산물) (e) SE 산화·환원 한계 산포 | 114, 21, 33, 22 | (c)(d) = 우리 grand-potential staircase의 문헌 표준 그림 — 발표 대조용 |
| **7** | 기계/공정: (a) 펠릿 >360 µm vs 시트 <50 µm 갭 (b) TPA 무용매 융착 막 (c) PTFE dry 공정 (d) SE 필름 4요소(SE/접착제/지지체/기판) | 124, 127, 129, 56 | 시트化 = [KimICCF] 문제의식과 동일; 무용매 공정 지도 |
| **8** | 양극 실패: (a) GSR(~200 °C, O₂+황화물→SO₂+인산염) vs SSR(~300 °C, TM-O+황화물→TM-S+인산염) 2경로 (b) LPSCl 작동창 vs Li-S/Li-ion (c) NCM/황화물 interphase+접촉손실 → 비가역용량·R_SE/NCM (d) LPSCl-NMC 2.5–4.1 V 전기화학+화학 반응 글로벌 스킴(Li₃PS₄→P₂S₅→MSₓ/SOₓ) | 132, 134, 136, 137 | (d)의 단계별 산물 = 우리 산화 staircase·[Zuo] SIMS와 정렬; (a) 열폭주 2경로 분류 신규 어휘 |
| **9** | 복합양극: (a) CAM wt%×입경 grid의 이온/전자 채널 단절 (b) 코팅 NCM+황화물 vs bare NCM+염화물 percolation (c) 부피점유 삼원도+카본 효과 (d) 층상 gradient 전극(CA-H-L/균질/CA-L-H) | 143, 145, 147, 149 | (c) 0D 카본의 부피 잠식 = [KimCA]와 동일 결론 — 그룹 실험의 문헌 좌표 |
| **10** | (a) 3D SOC·전류밀도·von Mises 콘투어(NCM 75/83/92 wt%) (b) 가압 형태변화(force line·void) (c) 3층 gradient 유효 σ_e/σ_ion sim vs exp (d) PC- vs SC-LRMO 분쇄/사이클 SEM(단결정=접촉 유지) | 150–153 | 미세구조 연속체 모델링 축 — 우리 DFT 밖, 그룹 실험과 연결 |
| **11** | 코팅: (a) bare vs NCM@LPSCl(접촉손실/공극 vs 밀착/무공극) (b) Li₂CO₃ 피복률 3단(부족/적정/과잉→LPSC 분해) (c) LATPO@LCO 750 °C 표면반응 구축 (d) LiPON@NCM(양성자 소거·분해억제·전류밀도 시뮬) | 154–157 | 코팅 두께/피복률 "적정창" 개념 — [Sundar] 스크리닝과 접목 |
| **12** | (a) I-FPG 통합전극(PVDF 섬유망 전방사+FPG 전해질) (b) "polymer-patched inorganics" 프로토콜 (c) PEDOT@CNT 밴드(금속→p형 반도체) (d) XCT: SC811 vs AZ@SC811 void 3.95→1.19 % | 158–161 | (c) 도전재 전자구조 조절 = 우리 SDCP(전도성 바인더) 프로그램과 어휘 공유 |
| **13** | 할라이드 CAM 구조: (a) Li₁.₃Fe₁.₂Cl₄ Cmmm+이온경로+가역 Fe 국소이동 (b) Li₂FeCl₄ (c) Li₂₋₂ₓFe₁₊ₓCl₄ (de)lithiation 구조진화 vs FeCl₃ | 163–165 | 황화물 SE 호환 신규 CAM 축 — 우리 hull 밖(Fe/Cl-CAM)이나 산화 구동력 제거 논리는 동일 |
| **14** | (a) FeCl₃ 적층+operando XRD 상진화 (b) 금속염화물 용량/에너지밀도 막대 (c) catholyte-free 개념+Cl 매장량/가격 vs Co·Ni·Mn | 166–168 | 저비용 CAM 방향 감각 |
| **15** | (a) Li-free 변환양극 전위 vs 용량(>1200 Wh/kg) (b) FeS₂/argyrodite 전압곡선·미세구조 (c) 균질화 양극 충전 미세구조 진화 (d) Li₂S vs Li₂SeₓS₁₋ₓ | 169, 171, 173–174 | "cathode homogenization" = 혼성전도 단일상 개념 |
| **16** | 덴드라이트: (a) 액체 vs SE 개시(전자누출·독립 dendrite·anode/GB-개시) (b) Li/LPSCl/Li operando XCT 균열 개시→전파→단락(0 s→60 min) (c) MD: LPSCl/SEI/Li, SEI 내 Li 클러스터 핵생성(g(r)) | 176–178 | (c) = **우리 anode_interface/SEI gap 서사의 MD 판** — "SEI 내부 전자침투→dead Li"의 원자 그림 |
| **17** | (a) ionization-level traffic light(c-LPS/a-LPS vs Li₃PS₄ glass; +Li 0→3.33 삽입 진화) (b) SE/Li 공공확산·기공·adatom 도식 (c) 다결정 전위분포 (d) 덴드라이트 관통 중 Li⁺ 분포 t=0→0.8 ns | 180–182 | (a) **ionization level = 우리 SEI-gap(전자차단) 지표의 형제 서술자** — b2o3_sei_gaps.json과 직접 대조 후보 |
| **18** | (a) 계면 기공+SE 내 덴드라이트 SEM (b) 균열 내 Li 성장(diffusion creep·columnar) (c) 사이클 중 계면 부피변화(interphase↑/Li↓)·공극 형성/폐쇄 SEM | 184–186 | 공극-덴드라이트 결합의 실측 갤러리 |
| **19** | (a) 임계전류 초과 탈리 공극→측면성장→차단 (b) AFM 스택압 하 void 수축/유지 상도(ζ vs P vs i) (c) 30 vs 5 MPa 계면 (d) **Li 변형기구 지도 → 최적 stack pressure 예측** | 188–191 | (d) = 압력 축의 정량 설계도구 — 우리 기계축(C축) 확장 후보 |
| **20** | 흑연: (a) 전자구조→열역학/kinetics→성능 3층 프레임 (b) 비정질+결정 vs 결정 카본 SEI(Li₂S/LiCl/Li₃P/LiF) (c) MoON@Gr 합성(370→500 °C 질화) | 192, 195, 197 | 흑연 ASSB의 "계면 화학안정 > σ" 명제 |
| **21** | Si: (a) Si/LPSCl XCT 시간열(수직균열·계면균열·delamination) (b) 입자/계면/전극 3-레벨 한계 | 200–201 | Si 음극 기계 실패 지도([Jun26] 바인더 문제의식과 연결) |
| **22** | (a) 음극 3종 radar+표면 거칠기/침습성 (b) all-electrochem-active µ-LiₓSi 설계 (c) LE vs SE 저/고압 dealloying(φ vs σ/σ_y) (d) Li₄.₄Si-nSi 무균열 구조진화 | 204, 207, 210–211 | 합금 음극 압력-항복강도 매칭 개념 |
| **23** | anode-free: (a) 에너지밀도 비교+실패인자 wheel (b) Ag/SE/Li 미세구조 진화(260 nm→~1 µm→300 nm) (c) Li/Cu·NMC/Li·NMC/Cu 충방전 상태+비가역 분해 프로토콜 | 213–214, 216 | CE 민감성·양극-음극 통합 분석 프레임 |
| **24** | SE 개질: (a) **Mg/F 전자재분배(ΔE −2.0→−4.2)** (b) **CuBr₂ ELF** (c) 고엔트로피 ΔS_conf/R↔σ (d) F-rich 계면 gradient (e) LiI-rich 재생 계면 TEM (f) 동적 적응 interphase 탈리 4단계 | **217(=[Liu23]), 218(=[Li25])**, 68, 221–222, 41 | **우리 digest 2편이 리뷰 Figure로 등장** — 우리 캠페인이 이 리뷰 §5.2.2의 정중앙에 위치함을 증명 |
| **25** | SEI: (a) 유전상(LATP) 다기능층+Li⁺ 농도 위상장 (b) LiAl 합금화 원소분포 (c) Li₃N 계면층(SC vs SC-10Li₃N 무덴드라이트) (d) MPDMS 처리 인공 SEI (e) 유무기 나노필러/그래프트 폴리머 SEI | 225, 227–230 | 인공 SEI 설계 사다리 — 우리 SEI-gap 지표로 서열화 가능한 대상들 |
| **26** | LiF/gradient: (a) LiFSI-DME 전처리 LiF-rich SEI (b) PHI@Li (c) 요오드 증기 LiI층 (d) LiₓMg/LiF/폴리머 lithiophilic-lithiophobic gradient (e) (de)solvation vs adsorption 합금보호 (f) LiF/LiAl gradient 3D 원소분포 | 231, 233–237 | LiF-rich = [KimICCF] LiF-SEI·우리 wide-gap 절연 SEI 패밀리의 문헌 본진 |

## 11. 우리 DFT/캠페인 대비 (comp1 / modelc(LPSCl1.6) / +B₂O₃ / LPSOCl) → `../our_dft_baseline.md`
> 우리 캠페인 값: **eigenvalue gap** comp1 2.066 / modelc 2.099 / +B₂O₃ 1.967 / LPSOCl(+O) 2.231 eV · **BVSE Li-채널 부피(iso0.5)** 3.32/4.74/6.73 %(modelc→LPSOCl(+O)→+B₂O₃) · **UMA-MD σ300 비** b2o3/modelc **동등**(멀티시드 1.08/0.82/1.15, 단일시드 1.33× 철회 — SEMIFINAL 07-09; Ea 0.199±0.034 vs 0.197±0.032) · **free-S site-PDOS ⟨3p⟩ −1.1 eV**(최천층=산화 취약) → **B–S 결합 시 −2.15 eV**(안정화) · O-doping = gap 확장+O 2p 매몰(깨끗한 밴드엣지) · 음극 계면/SEI: `db/properties/anode_interface_b2o3.json`·`db/properties/b2o3_sei_gaps.json`.

| 리뷰의 칸 | 리뷰 내용 | 우리 결과 | 판정 |
|---|---|---|---|
| §3.4/4.1.1 산화 개시 = **S²⁻ 우선 산화**, 황화물 산화전위 ~2 V, LGPS 창 1.7–2.1 V | 정성 서술 + 표준 인용(refs 114/130) | grand-potential onset **2.256 V**(S²⁻-limited, comp1=modelc 동일) + **free-S site-PDOS ⟨3p⟩ −1.1 eV = "어느 S가 먼저"의 자리-분해 정량** | **✓✓ 재현+심화** — 리뷰가 "S²⁻ 우선"이라 말하는 것을 우리는 *free S(4d) vs PS₄ S*까지 분해; [Banik] S-pin과 3자 정합 |
| §3.1 공기 전략① "O 도핑 → P–O" + Fig 3a(ΔE_ad 완화) + HSAB | LPSC→LPSOCF ΔE_ad −1.63→−1.19 eV; ref 83 = **Li₅.₅PS₄.₅Cl₁.₅ O-doping**(우리 modelc 사촌 조성!) | LPSOCl gap **2.231 eV**(확장)+O 2p 매몰(깨끗한 엣지); ICOHP P–O 강결합(기존 baseline) | **✓ 같은 전략 칸** — 우리 O-doping은 리뷰 전략①의 전자구조 관측량(gap·엣지 청정도) 버전; 단 가수분해(H₂O/H₂S 기체)는 우리 0K hull 밖 — "우리가 H₂S 억제 계산" 주장 금지 |
| §3.1/3.2 "격자 결합에너지 강화 → 공격 면역"(InF₃ 예) | E_ad −0.12 eV; InS₄ 무분해 vs PS₄ 분해 | **B–S 결합이 free-S를 −1.1→−2.15 eV로 안정화** = 같은 논리의 B₂O₃판 | **✓ 동형 기전** — "취약 단위를 강결합으로 묶는다"; 우리 것은 자리-분해 PDOS라는 신규 관측량 |
| §5.2.2 SE 개질 → in-situ 전자절연 SEI (Fig 24a–b = [Liu23]/[Li25]) | 할로겐/F/LiI 도핑 → Li-halide/불화물 SEI(전자절연·이온전도) | `anode_interface_b2o3.json`·`b2o3_sei_gaps.json` = **B₂O₃ 유래 SEI 산물의 gap(전자차단성) 정량 서열** | **✓✓ 정중앙 적중** — 리뷰 §5.2.2의 설계 rubric(전자절연 SEI)을 우리는 *산물별 gap 수치*로 구현; Fig 24a/b가 우리 digest 2편의 그림이라 계보 직접 연결 |
| §5.2.3 이상 SEI 4조건(나노두께·저장벽 Li⁺·**전자절연**·기계 적응) | 정성 rubric | b2o3_sei_gaps = 조건③의 정량 지표; 조건①②④는 우리 미계산 | **○ 부분** — 조건③만 커버; 두께/기계(①④)는 H-리스트 |
| §5.1.1–5.1.2 덴드라이트 = 분해산물 **좁은 gap→전자침투→dead Li**; ionization-level 서술자(Fig 17a) | MD(ref 178)·서술자(ref 180) | 우리 SEI-gap 지표와 **형제 서술자** — wide-gap 산물(LiCl·Li₂O류)=차단, narrow-gap=위험 | **✓ 개념 일치** — ref 180 ionization level vs 우리 gap 지표의 정식 비교가 유망한 후속 과제 |
| A축(σ): 할로겐 도핑 σ↑·플럭스 균질화; 고엔트로피 ΔS_conf↔σ(Fig 24c) | 정성+σ 산포 | BVSE 채널부피 **3.32→4.74→6.73 %**(modelc→LPSOCl(+O)→B₂O₃)·UMA σ300 **b2o3/modelc 동등(멀티시드; 1.33× 철회)** — **B₂O₃는 σ를 깎지 않는(보존) 안정화 도핑** | **✓ trend 재현+반례 보유** — [Yang25] La-O(σ 0.65×)와 달리 우리 B₂O₃는 σ·안정 동시 개선 → 리뷰 미래방향①("intrinsic stability, 반응 구동력 축소")의 구체 실현 후보 |
| §3.5 기계: E 10–30 GPa·K_IC 0.2–0.4·>3 µm 파쇄 | 범위 서술 | comp1 E_VRH 22.06 / modelc **27.66 GPa**(relaxed-ion) — 리뷰 범위 내 | **✓ 정합** — 단 K_IC·입경 효과는 우리 밖(H-리스트); relaxed vs clamped 구분은 리뷰에 없음(우리 vacancy-paradox가 더 세밀) |
| §3.4 계면 3유형(안정/MCI/passivated) | Wenzel 분류 | interface_reactivity + SEI gap으로 우리 산물들을 ②vs③으로 분류 가능 | **✓ 분류 어휘 이식** — 우리 json 산물 라벨링에 "MCI vs passivating" 열 추가 가치 |
| §3.3 열: Th₀/Th′ 서술자·계면 40–50 % 발열↓ | ref 109 서술자 | **미보유 축** — 우리 열안정 계산 없음 | **✗ 공백(H-리스트)** — Th′를 B₂O₃/O 조성에 계산하는 것이 저비용 확장 |
| gap 절대값 | (리뷰 gap 수치 없음) | comp1 2.066/modelc 2.099/**B₂O₃ 1.967**/LPSOCl 2.231 eV (PBE) | — PBE 과소+무질서 민감 → 문헌 절대 비교 금지, "wide-gap" 수준만. **B₂O₃ gap 1.967 = 소폭 협소**이나 free-S 안정화(−2.15)와 SEI gap이 실전 지표 — "gap 하나로 안정성 판정 금지"의 자기 사례 |

## 12. 적용 인사이트 (우리 연구에 어떻게)
- ① **서사 배치도**: 논문/deck 서론을 이 리뷰의 3분할(고유 5축 → 양극 → 음극)로 짜고, 우리 기여를 "고유-전기화학(free-S 자리분해)·고유-공기(O/B 결합강화)·음극-SEI(gap 정량)" 세 칸에 명시적으로 꽂는다 — Fig 24a/b가 [Liu23]/[Li25]인 만큼 **우리 litdb 계보가 리뷰 §5.2.2의 직계**임을 활용.
- ② **B₂O₃ 스토리의 차별점**: 리뷰(및 [Yang25])의 안정화 도핑은 대개 σ 비용을 치름 — 우리 B₂O₃는 **σ300 보존(멀티시드 동등, Ea 동일)+free-S 안정화+SEI gap 확보** = 미래방향①(intrinsic stability)과 ②(계면 동적 조절)의 교집합 사례로 포지셔닝.
- ③ **즉시 이식 가능한 외부 도구 2개**: (a) **Th′ 열안정 서술자**(ref 109)를 우리 조성군에 계산 → 우리가 비어 있는 열 축(D3/D4)을 저비용으로 커버; (b) **ionization-level 서술자**(ref 180) vs 우리 SEI-gap 지표 벤치마크 → 덴드라이트 축의 정량 언어 통일.
- ④ **비교축 규율**: 리뷰의 "황화물 산화 ~2 V·LGPS 1.7–2.1 V"는 우리 axis-①(intrinsic 0-pressure) 값과만 비교; 실험 CV 창(2.5–4.1 V 운전)은 kinetic — 리뷰 자신이 이 구분(§3.4)을 명문화하므로 인용하기 좋다.
- ⑤ **평가 표준화 결핍(미래방향④)** = 우리 계산의 셀링포인트: 두께·압력·로딩이 제각각인 실험 지형에서, 동일 프로토콜 DFT/MLIP 서열(same-footing ranking)이 갖는 가치를 서론에서 주장 가능.

## 13. 인용 가능 문장 (deck/paper용)
- "A recent comprehensive review of sulfide-ASSB stability (Fan group, USTB/Tsinghua) frames degradation as the *coupled* action of chemical, electrochemical, thermal and mechanical factors, and calls for a shift from passive interfacial stabilization to *intrinsic* stability by design — our free-S site-resolved electronic-structure screening and B₂O₃/O co-stabilization follow exactly this prescription." (미출판 draft 인용 주의: "ECER-D-26-00097, under review")
- "The review reiterates that sulfide oxidation initiates at S²⁻ with a thermodynamic window of only ~1.7–2.1 V (LGPS); our grand-potential onset of 2.256 V for Li₆PS₅Cl/Li₅.₄PS₄.₄Cl₁.₆ and the site-PDOS identification of free S (⟨3p⟩ ≈ −1.1 eV) as the shallowest, most oxidation-prone site provide the site-resolved version of this picture."
- "Consistent with the review's 'ideal SEI' criteria (nanoscale, Li-conducting, electronically insulating, mechanically adaptive), we rank B₂O₃-derived SEI products by their computed band gaps as a quantitative electron-blocking metric."

## 14. 주의/한계 (비판적으로)
- **미출판 draft** — 수치·그림·참고문헌이 게재 과정에서 바뀔 수 있음; DOI 없음; 인용은 원고번호로만.
- **자체 데이터 0인 정성 리뷰** — 셀 성능 수치(유지율 %·CCD·사이클)가 본문에 사실상 없음. "종합 리뷰"지만 **전략 간 정량 비교표가 없다**는 점이 최대 약점(우리가 원전을 직접 파야 함). [Bai]·[Kang]보다 폭은 넓고 깊이는 얕음.
- **draft 품질 문제**: ① Intro σ 단위 오타(10⁻³~10⁻² **mS**/cm — §2.2의 10⁻⁴~10⁻² S/cm와 모순) ② DOI placeholder가 Wiley prefix(10.1002)인데 EER은 Springer(템플릿 잔재) ③ refs 38=193 완전 중복(Oh, Angew 2022) ④ Fig 5c 조성 라벨·Fig 5e Th′ 식 판독 곤란 ⑤ 영문 어색("Machine" for mechanical 등).
- **방법 의존성 무경고 인용**: ESW·흡착에너지·서술자 값들을 functional/무질서 처리 명시 없이 소환 — 절대값 이식 금지, 우리 baseline 규율(PBE gap 과소·onset은 S-limited·기계값은 relaxed/clamped 구분) 유지.
- **우리 그룹(한양대 J-W Lee 계열) 문헌 미인용** — 시야 보정용: 이 리뷰의 계보는 USTB/Tsinghua(Fan-Nan) 중심.
- 리뷰의 "황화물 CCD 높다/Li 증착 안정"(§2.3) 같은 우호 서술은 §5.1의 자체 내용(덴드라이트가 핵심 병목)과 긴장 — 선전 문구는 걸러 읽을 것.

## 15. 후속 추적 참고문헌 (읽을 것 — 우선순위순)
| 우선 | ref# | 논문 | 왜 |
|---|---|---|---|
| ★★★ | 109 | Wang S. et al., *InfoMat* 2022, 4, e12316 — "Improving thermal stability of sulfide SEs: an intrinsic theoretical paradigm" (**Th₀/Th′ 서술자**) — **✅ digest 완료 (2026-07-17): `wang2022_sulfide_thermal_stability_th_descriptor.md`** (⚠ 원논문 기호 Th/Th′; "Th₀"는 이 리뷰 표기. 교신 Fan Wu=IOP CAS ≠ 본 리뷰 Li-Zhen Fan/USTB. Eq 5 = {[Li]%×312.5+[P]%×346}×4+E_doped+k — Li–Cl 항 부재 주의) | 우리 열 축 공백을 채울 서술자; 도핑 조성 열안정 스크리닝 즉시 이식 |
| ★★★ | 84 | Zhu & Mo, *Angew* 2020, 59, 17472 — 공기안정 SE 설계원리(가수분해 반응E 지도) | 우리 free-S/O-doping 공기 서사의 정량 원전(Fig 3b) |
| ★★★ | 180 | Hao W. et al., *Angew* 2025, 64, e202500245 — "Origin of Li Dendrite Formation in Sulfide Electrolyte" (**ionization level**) | 우리 SEI-gap 지표의 형제 서술자 — 정식 벤치마크 대상 |
| ★★ | 103 | Cao C. et al., *Cell Rep. Phys. Sci.* 2024, 5, 101909 — 황화물 산화열화 원자 기전 | 우리 축 B 메커니즘 심화(자리-분해 관점 비교) |
| ★★ | 137 | Naillou P. et al., *ESM* 2025, 75, 104050 — LPSCl–NMC 반응성 직접 관찰(2.5–4.1 V) | 우리 onset·[Zuo]와 삼각측량할 최신 operando |
| ★★ | 134 | Tan D.H.S. et al., *ACS Energy Lett.* 2019, 4, 2418 — LPSCl 가역 redox 규명 | B① kinetic 확장(indirect (de)lithiation)의 LPSCl 원전 |
| ★★ | 132 | Rui X. et al., *EES* 2023, 16, 3552 — 황화물 ASSB 열폭주 2경로(GSR/SSR) | 열 축 어휘·Fig 8a |
| ★★ | 68 | Li S. et al., *Angew* 2023, 62, e202314155 — 고엔트로피 argyrodite(ΔS_conf↔σ) | 우리 disorder-ensemble·Cl-rich 무질서 서사와 직접 접점 |
| ★ | 83 | Peng L. et al., *Chin. Chem. Lett.* 2025 — **Li₅.₅PS₄.₅Cl₁.₅ O-doping**(공기+Li 호환) | modelc 사촌 조성의 O-doping 실험 — 우리 LPSOCl과 정면 비교 |
| ★ | 86 | Liu M. et al., *Nat. Commun.* 2025, 16, 213 — 티올 분자층 습윤공기 처리 | 공정 축(습식 핸들링) 대표 |
| ★ | 191 | Jeong & Kim, *ACS Energy Lett.* 2024, 9, 3237 — Li 변형기구 지도→stack pressure | 기계/압력 축 정량 설계도구 |
| ★ | 163 | Fu J. et al., *Nature* 2025, 643, 111 — all-in-one 할라이드(Li₁.₃Fe₁.₂Cl₄) | 황화물-호환 신규 CAM 지형 |
| ★ | 178 | An Y. et al., *ACS Nano* 2025, 19, 14262 — SEI 내 Li 핵생성 MD | 우리 음극 json과 방법 비교(MD vs 정적 hull) |
| ★ | 41 | Cen G. et al., *Nat. Sustain.* 2025, 8, 1360 — 무압 ASSB 적응형 interphase | 미래방향③(저압) 대표 |

## 16. 기법 용어 미니사전
- **HSAB / HSEH**: hard-soft acid-base; S²⁻=soft base가 H₂O의 H(soft acid)와 우선 결합 → 가수분해. HSEH(ref 80)는 이를 전자·홀 언어로 다전자 확장.
- **donor number**: 용매의 전자쌍 공여능 — 클수록 황화물 공격성↑(Fig 4a의 x축).
- **Th₀ / Th′**: 조성(Li/P/S 비·도펀트)에 결합에너지를 가중해 만든 열안정 스칼라 서술자(ref 109).
- **MCI (mixed ion–electron conductive interphase)**: 이온·전자 둘 다 통하는 분해 계면상 — 분해를 지속시키는 나쁜 유형(vs passivating SEI).
- **공간전하층(space-charge layer)**: Li 화학퍼텐셜 차로 계면에 생기는 Li-결핍층 — 단 조성변화가 임피던스에 더 직접적.
- **wedge-opening**: 덴드라이트가 균열 *후단*에서 Li 주입으로 쐐기처럼 벌리며 전파하는 기전(선단 응력 모델과 대비; Ning Nature 2023).
- **ionization level**: 분해상별로 Li 증착(전자 받아 환원)이 유리한지 판정하는 전자구조 서술자(ref 180) — 우리 SEI-gap 지표의 사촌.
- **CCD (critical current density)**: 단락 없이 견디는 최대 전류밀도 — 계면 치밀도×σ×기계 건전성의 함수.
- **dead Li**: 전기적으로 고립된 Li — SEI 내부 핵생성·박리 hollow shell로 축적, 용량 손실+임피던스 상승.
- **catholyte / cathode homogenization**: 양극측 전용 전해질(할라이드) / 단일상에 이온+전자 수송을 내장한 양극 설계(ref 173).
- **GSR vs SSR**(Fig 8a): 열폭주 시 기상(O₂) 매개 gas-solid reaction(~200 °C) vs 고상(TM-O) solid-solid reaction(~300 °C) 경로.
- **anode-free(Li-free)**: 음극 활물질 없이 집전체에 in-situ Li 증착 — CE에 극도로 민감.
- **stack pressure window**: 접촉 유지(하한)와 GB Li 압출(상한) 사이의 조립 압력 적정 구간.
