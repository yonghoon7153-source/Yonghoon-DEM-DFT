# Bollard-Anchored Binder System for High-Loading Cathodes Fabricated via Dry Electrode Process — Kang, Jihyeon (Adv. Mater. 2025)

> slug `kang2025_bollard_anchored_binder_dry_electrode` · DOI `10.1002/adma.202416872` · type `exp + MLP-DFT/MD (molecular)` · PDF `docs/literature_coverage/pdfs/Kang_2025_AdvMater_Bollard_Anchored_Binder_Dry_Electrode.pdf` · digested `2026-07-08` · status ✅
>
> ⚠ **동명 구분**: 제1저자 **Jihyeon Kang (중앙대 Chung-Ang)** ≠ 랩 자체논문의 **Junhee Kang (한양대, `kang2025_toughened_bimodal_nca_lzo`)** — 다른 사람, 다른 논문.
> 데이터 CSV: `docs/data/kang2025_bollard_binder_anchors.csv`

## 1. 한 줄 요약
건식전극(DBE)의 유일한 fibrillation 바인더 PTFE(PFAS 규제·이온절연·약한 접착)를 **"bollard hitch(계선주 매듭)" 이중-바인더**로 보완:
**PAA-grafted CMC(=PC)가 NMC 산화물 표면에 Na⁺-매개 화학흡착(E_ads −2.24 eV)으로 붙는 "bollard(계선주)"**가 되고, **PTFE fibril이 그 bollard에 Na–F 결합(−0.35 eV)+물리 얽힘으로 계류되는 "rope"**가 되어 — PTFE를 2→0.6 wt%(>70% 감축)로 줄이고도 30 mg/cm²(4.0 mAh/cm²@2C)~90 mg/cm²(15.6 mAh/cm²) 고로딩 양극을 만든다.  앵커링 물리를 **MLP-DFT 흡착에너지 + 400 K NVT-MD 탈착 동역학**으로 정량 — **우리 SDCP 술폰산-NCM 화학앵커(E_bind −4.8 eV MLIP)와 정확히 같은 개념-클래스**(CAM 산화물 표면 이온성 화학흡착이 PTFE의 vdW-only 접착을 대체)의 독립 선례.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| Jihyeon Kang, Hojong Eom, Seohyeon Jang (공동1저자), Doehyeob Yoo, Hyeonha Lee, Minju Kim, Myeong-Lok Seol, Jeong Woo Han*, Inho Nam*, Hannah Song* (중앙대 + 현대차 배터리제조엔지니어링 + NASA Ames/USRA + 서울대) | Adv. Mater. 2025, 37, 2416872 (OA, CC BY-NC; rec. 2024-11-02 / online 2025-02-18) | 10.1002/adma.202416872 | **NMC622 (LiNi₀.₆Mn₀.₂Co₀.₂O₂) + Super P + PTFE + PC(PAA-g-CMC)**, Al collector, **액체 전해질 LIB** (⚠ SE 없음 — ASSB 아님) | exp (건식전극 제조·전기화학·XPS/XRM) + **MLP-DFT 흡착 + NVT-MD** (분자스케일; DEM/MPM/전달솔버 없음) |

- **바인더 명명**: PC = **P**AA-grafted **C**MC (탈수-축합 grafting; 내부 최적 PAA:CMC = 5:5 = "PC55").  PC_PTFE73 = 바인더 내 PC:PTFE = 7:3.
- **전극 조성**: 스크리닝 반쪽셀 NMC:SuperP:PTFE:additive = **93:5:1:1 wt%** (@18 mg/cm²); production **PC_PTFE73 = 93:5:1.4:0.6** (총 바인더 2 wt%, PTFE 0.6 wt%).
- **공정**: 용매-free 건식 — 혼합(ball mill ×3 채택) → PTFE fibrillation dough → free-standing film → Al 라미네이션.  캘린더링/롤 조건은 SI Note S1 (본문 미기재).

## 3. 핵심 물성 (수치)

### 3a. 바인더 필름·바인더시스템 물성 (Fig 3; additive:PTFE=1:1 필름)
| 물성 | PVdF_PTFE | CMC_PTFE | **PC_PTFE** | PAA_PTFE | PTFE | stated/dig. |
|---|---|---|---|---|---|---|
| σ_ionic (필름, EIS) [S/cm] | 2.55e-4 | 1.78e-4 | **1.31e-4** | 1.27e-4 | **4.88e-6** | stated |
| 시트저항 (건식 양극) [Ω cm⁻²] | 540.1 | 374.6 | **77.2** | 494.0 | 173.8 | stated (wet PVdF 2259.3) |
| σ_electronic (양극, 4-probe) [S/cm] | 0.19 | 0.27 | **1.30** | 0.20 | 0.58 | stated (wet PVdF 0.04) |
| swelling (전해질 120 h) [배] | 1.45 | 1.23 | **1.13** | 0.99 | 1.01 | stated |
| **E (Young's, 필름)** [MPa] | 0.83 | 0.80 | **0.15** | 0.66 | **3.50** | stated (⚠ 필름-스케일 MPa — bulk 바인더 GPa 아님) |
| 파단 strain [%] | 10.8 | 7.4 | **21.9** | 1.2 | 5.2 | stated (PTFE 본문 병기 6.0%) |
| 180° peel (전극↔Al) [N/cm] | – | – | **0.9615** | – | 0.5733 | stated (**1.68×**; 3M 테이프 12 mm, 6 mm/min) |

- 요점: PC 도입 시 바인더 필름 σ_ionic **27× ↑**(4.88e-6→1.31e-4; –OH/–COOH 극성사이트 간 Li⁺ hop), 양극 σ_e **최고 1.30 S/cm**(균일분산+3D망 = 분산효과, PC 자체는 절연 이오노머), E 23× 연화 + 연신 4×(soft PC + PTFE 시너지), peel 1.68×.

### 3b. 앵커링 에너지 (MLP-DFT + MD) ★
| 항목 | 값 | 비고 |
|---|---|---|
| E_ads PC_2Na (Na 2개가 NMC 표면 O에 흡착) | **−2.24 eV** | 가장 강함 = "bollard" 상태 |
| E_ads PC_1Na | **−1.12 eV** | 정확히 절반 규모 |
| E_ads PC_0Na (–OH/–COOH 장거리 쌍극자만) | **−0.37 eV** | 이온성 없이 극성만 |
| E_ads PTFE dimer | **−0.09 eV** | O(NMC)–F(PTFE) 정전 반발 → 본질적 저흡착 |
| E(Na–F) PC↔PTFE | **−0.35 eV** | PTFE–NMC보다 **2–4.5×** 강함 → PTFE가 bollard에 계류 |
| MD 탈착 (400 K, 10 ps, Langevin NVT) | PTFE-only: 표면거리 **4.2→6.6 Å** (탈착) / PC 동반: **4.5–4.9 Å 유지** (계류) | Fig 4d 라벨 9 Å(탈착 스냅샷) vs 4e 3 Å(계류) |
| XPS 검증 | F1s 디컨볼루션 **Na–F 피크면적 > C–F** | 계면 Na–F 결합 실존 (Note S3/Fig S17) |

### 3c. 전극·전기화학 (LIB, 액체 전해질)
| 물성 | 값 | 조건 | stated/dig. |
|---|---|---|---|
| porosity | PC_PTFE73 **"25.9% higher ... than PVdF wet (17.7%)"** | 두 전극 동일 밀도 3.0 g/cm³; 밀도계산 기반(단면측정 아님) | stated but **문장 중의적** — PC=25.9%(절대) 또는 17.7×1.259≈22.3%(상대) 두 독해 가능; Table S3(SI 미확보) 확인 필요 |
| tortuosity τ | PC_PTFE **1.30** vs PTFE **1.40** | 단면 SEM 기반 계산 | stated |
| PTFE 최소 fibrillation 함량 | **0.6 wt%** (PC_PTFE73) — PC_PTFE91(0.2 wt%)는 dough 형성 실패; PTFE-only는 **2 wt%** 필요 | dough 성형성 | stated ★ |
| 혼합-분산 산포 (2C 용량 STD, 30 mg/cm²) | 기본혼합 103.65±**16.52** → planetary ×1 118.22±**5.59** → **ball mill ×3 127.67±4.28** mAh/g | PTFE-only 전극 | stated ★ (분산 CV 앵커) |
| 고로딩 용량 | 30 mg/cm²: 1/3C **168.5**(5.0 mAh/cm²)/1C 159.5(4.8)/2C **133.2**(4.0); PTFE 2C 108.1(3.2); PVdF 2C 76.5(2.3) mAh/g | PC_PTFE73 | stated |
| 사이클 (25 mg/cm², 1/3C, 100 cyc) | PC_PTFE73 139.2 mAh/g = **83%** / PTFE 84.0 = **51%** / PVdF wet 77.6 = **47%** (PTFE·PVdF ~70 cyc 후 급락) | | stated |
| R_ct (EIS 반원) | 10 cyc: **39.01** vs 68.65 Ω (1.76×↓); 100 cyc: **48.08** vs 91.52 Ω | PC_PTFE73 vs PTFE | stated |
| D_Li⁺ | **5.09e-14** vs 2.53e-15 m²/s (**20×**) | 10 cyc 후 | stated |
| 초고로딩 | **90 mg/cm² = 15.6 mAh/cm²**, 0.1C 50 cyc 안정 | PC_PTFE73 | stated |
| 사이클 후 AM 균열 | PTFE: NMC 2차입자 **파쇄**(FE-SEM S21b) / PC_PTFE73: 균열 無 | 100 cyc 후 | stated(정성) ★ |
| CEI LiF 분율 (F1s) | PC_PTFE73 **29.8%** vs PTFE **37.4%** | 100 cyc; PTFE 자체분해→LiF 과다·불균일(깊이불균일) | stated |
| 풀셀 | dry-dry(Graphite@PTFE): 2C 119.8 mAh/g, 0.5C 50 cyc **84%**; dry-wet(흑연 습식): 0.2C 100 cyc **86%**; 파우치 **8 mAh/cm²**@0.5C | | stated |
| 고전압 | LNMO 4.9 V 급 대응 — CV/LSV 2.5–5.0 V 안정 (S23) | | stated(정성) |

## 4. 시뮬레이션 방법 ★ (분자스케일 — DEM/MPM/전달솔버 없음)
- **스케일**: 이 논문의 시뮬레이션은 **전부 분자스케일**(흡착에너지+MD). 입자·전극 스케일 시뮬 없음 →
  DEM 접촉법칙/PSD/RVE/servo 등 템플릿 항목 **n/a**. "입자 처리" 항목의 답 = **입자 없음**(분자 fragment).
- **MLP-DFT 흡착**: "machine learning potential based DFT" (딥러닝 MD로도 지칭; MLP 종류·트레이닝은 SI만).
  NMC 표면 슬랩 모델 구성(면지수 본문 미기재) 위에 PC 분자를 **15개 배향 회전**시켜 E_ads 산출(Fig S15).
  흡착상태 3분류: PC_2Na(−2.24) / PC_1Na(−1.12) / PC_0Na(−0.37 eV); PTFE dimer −0.09 eV.
- **계산 fragment** (Fig S13): CMC monomer, PAA dimer, **PC = PAA-dimer-grafted CMC-monomer**, PTFE dimer —
  전부 소형 fragment (폴리머 전체 아님) → 절대 E_ads는 fragment-스케일 값.
- **NVT-MD**: Langevin heat bath, **400 K 도달 후 10 ps** ("고온에서 바인더 동역학 보장"). 산출 = 표면 최근접
  F(PTFE) 평균거리 시계열(Fig 4f): PTFE-only 4.2→6.6 Å 탈착 vs PC 동반 4.5–4.9 Å 계류.  부가 관찰:
  (i) PC 골격은 붕괴/분해 없음 — 흡착 Na가 표면 O층 위를 **이동(migration)**하며 구조 응력 완화(Movies S1–S3);
  (ii) PC_1Na의 **자유 Na 사이트가 탈착 PTFE의 F를 포획**(Na–F −0.35 eV) — 다수 Na–F 결합 → 하중이 결합망
  전체로 분산되어 파단에 필요한 총에너지 증가(정성 논변).
- **DFT-IR**: FTIR 피크 배정(PAA C=O 1710 / CMC COO⁻ 1590·C–O–C 1021 cm⁻¹ / PC에 양쪽 보존)을 DFT IR 스펙트럼으로 검증.
- **입자/무질서 처리** ★: n/a — 전극스케일 구조는 실험(XRM/SEM)만. **바인더의 기계·전달 역할을 입자스케일로
  올리는 모델은 없음** (= 우리 additives.py/MPM coh가 채우는 칸).

## 5. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1a–f | 3-바인더 모식: PVdF **sheet-like**(습식, 면덮음) / PTFE **bridge-like fibril**(건식) / PC_PTFE **bollard-anchored**(표면 계선주 + fibril rope) | ★ bollard = **표면 앵커된 불연속 입자/패치 + 입자간 fibril 스팬** = 우리 SDCP `particle`+`surface_frac` 시딩 그림과 동형 (conformal 필름 아님) |
| 1g,h | FE-SEM+EDS: PTFE(F맵) vs PC_PTFE(F+**Na맵** — Na가 PC 마커, NMC 표면에 균일분포) | 앵커링 실측 증거; Na 균일분포 = surface_frac 높음 방향 |
| 2a–i | 로딩 15–30 mg/cm² × wet/dry C-rate + **혼합법별 STD**(g: wet 88.12±11.37 / h: planetary 118.22±5.59 / i: ball mill×3 127.67±4.28) | ★ **분산 불균일 → 용량 산포** 정량 = 우리 A5 dispersion-CV 실험앵커 |
| 3a–g | 바인더 5종 물성 매트릭스(σ_ion/저항/σ_e/swelling/E/strain + radar) | §3a 표 전체; W2 바인더별 σ 페널티 입력 후보 |
| 3h–j | 바인더별 반쪽셀 rate + **PAA:CMC 비 스윕**(PC55 최적) + **PC:PTFE 비 스윕**(73 최적; 91은 dough 실패) | ★ PTFE fibrillation 하한 0.6 wt% + anchored:rope 비율 최적화 데이터 |
| 4a,b | FTIR(PAA/CMC/PC) + PC 축합반응 모식 | PC 화학 정체성 |
| 4c | **흡착에너지 박스플롯**(PC_2Na −2.24 / PC_1Na −1.12 / PC_0Na −0.37 / PTFE −0.09 eV) | ★ 우리 SDCP E_bind −4.8 eV(doped)/−3.0(neutral)와 비교할 이온성≫극성≫vdW 사다리 |
| 4d–f | MD 400 K 스냅샷(PTFE 9 Å 탈착 vs PC계류 3 Å) + 거리 시계열(4.2→6.6 vs 4.5–4.9 Å) | ★ 우리 single-point E_bind에 없는 **동역학 hold-test** — SDCP에 이식 후보 |
| 5a–d | GCD/rate/사이클(83 vs 51 vs 47%@100cyc) | binder cohesion↔수명 실험앵커 |
| 5e,f | Nyquist + R_ct(39→48 vs 68.65→91.52 Ω) | 열화 시그니처(R_ct 성장률) — binder-망 붕괴 척도 |
| 5g–i | 90 mg/cm² 15.6 mAh/cm² + 50 cyc + 선행 DBE 대비 최고 | 고로딩 한계치 |

## 6. Post-processing ★
- **XPS 디컨볼루션**: PC 정체성(C1s 284.1 C–C/285.7 C–O/287.2 COO⁻/288.1 COOH = 에스터 형성) + **계면 Na–F**
  (F1s에서 Na–F 면적 > C–F — 앵커링의 실험 카운터파트) + **CEI 조성·깊이 프로파일**(10/20/30 s 스퍼터;
  LiF 685.0 vs LiₓPOᵧF_z 687 eV; ROCO₂Li/Li₂CO₃; PTFE분해→LiF 과다·깊이 불균일).
- **XRM(3D X-ray 토모)**: NMC 입자만 가시(카본·바인더 투명) → 고로딩 분산 균일성 확인; **porosity는 토모가
  아니라 밀도계산**(동일 3.0 g/cm³에서 바인더 tap density 차이로 산출 — 방법 low-resolution, §10).
- **tortuosity**: 단면 SEM 이미지 기반 계산(방법 상세 미기재; τ=1.30/1.40 — τ² 아님 주의).
- **기계**: UTM 인장(필름 E·strain), **180° peel-off**(3M 테이프 12 mm, 6 mm/min, 전극↔Al) — binder cohesion의
  시스템-레벨 수치화.
- **전기화학**: 4-probe 시트저항→σ_e; 필름 EIS→σ_ion; 반쪽셀 EIS 반원→R_ct(10/100 cyc); D_Li⁺(S25);
  radar chart(5축 종합) — 바인더 선택 논리의 시각화.
- **FTIR+DFT-IR 대조**: 실험 피크 배정을 계산 IR로 검증(그들의 frame[4]-스타일 소규모 교차검증).

## 7. 우리 DEM+MPM(+SDCP/additives) 대비 → `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **앵커링 개념** ★ | **bollard hitch**: PC가 NMC 산화물 표면에 **Na⁺-매개 화학흡착**(−2.24 eV) = 계선주; PTFE fibril이 **Na–F**(−0.35 eV)+PAA가지 물리얽힘으로 계류 | **SDCP**: 술폰산 −SO₃⁻가 NCM **Li-O층 삽입형 화학흡착** E_bind **−4.797 eV**(doped, uma-s-1p1 MLIP; neutral −3.02) · O–Li 1.83 Å×2 · γ≈0.93 J/m² | **같은 개념-클래스** — CAM 산화물 표면 *이온성* 화학흡착이 PTFE vdW-only(−0.09 eV)를 대체.  차이: 그들 **양이온(Na⁺) 표면 브리지** vs 우리 **음이온(−SO₃⁻) 격자삽입**; 그들 fragment-흡착(E_ads) vs 우리 분자+footprint→γ 환산(역학 매핑은 우리가 앞섬) |
| 이온성≫극성≫vdW 사다리 | 2Na −2.24 ≫ 0Na(쌍극자) −0.37 ≫ PTFE −0.09 eV | doped −4.8 > neutral −3.0 (≫ PTFE) | **방향 독립 재현** — "하전/이온 채널이 중성 극성 채널을 지배"를 다른 계·다른 코드가 확인 (분자스케일 frame[4]-형 방향 교차검증; 절대값은 fragment·표면·코드 달라 서열만) |
| 아키텍처 | **이중-바인더**: 절연 bollard(PC) + 도전 아님 + **PTFE rope 유지**(0.6 wt%) | **단일 도전바인더**: SDCP가 앵커+전자전도 겸업, PTFE-free 지향 (비교셋 VGCF+PTFE 1+1 / 0.5+0.5 / SDCP 0.5) | 그들은 fibrillation **공정** 유지가 목표(DBE dough에 PTFE 필수) → PTFE 최소화; 우리는 fibril web 없는 대안까지 시험.  ★ 그들 데이터 = "**anchored+rope 하이브리드 > rope-only**"(동일 총바인더) — 우리 비교셋에 **SDCP+PTFE 콤보** 추가할 근거 |
| σ_e 이득의 기원 | PC_PTFE 1.30 S/cm 최고 — 그러나 **분산·3D망 효과**(PC 자체는 절연 이오노머) | SDCP는 **재료 자체가 도전**(self-doped S-PEDOT) | 다른 채널 — 그들 σ_e↑는 우리 **A5 dispersion-CV**축의 증거, 우리 SDCP 전도축과 혼동 금지 |
| binder σ_ion | 필름: PTFE 4.88e-6 → PC_PTFE 1.31e-4 S/cm (**27×**) | W2 whatif: PTFE σ_ion **×0.74** 고정 페널티 (binder 종류 무관) | 우리 페널티를 **바인더별 입력**으로 세분할 근거 (단 그들 값은 액체전해질 팽윤 필름 — ASSB SE-neck 차단과 물리 다름, 비율 방향만) |
| binder cohesion 실험앵커 | peel **0.9615 vs 0.5733 N/cm (1.68×)**; 사이클 R_ct 성장 39→48 vs 69→92 Ω; **AM 2차입자 파쇄 유무** | A3 `binder_cap` (PTFE, 비단조 w/w*) + SDCP coh ≈ **10× coh_ptfe**(γ-비 anchor) | ★ 계층 정합: 계면(그들 E_ads비 25×·우리 γ비 ~10×) ≫ 시스템(peel 1.68×) — peel은 소성산일·테이프 포함 + 두 계 모두 PTFE web 공유라 희석.  **peel(N/cm=J/m² 규모 96/57)을 γ(0.93 J/m²)와 동일시 금지** — 비율만 |
| PTFE fibrillation | **명시 하한**: bollard 지원 시 0.6 wt%로 dough 성립, 0.2 wt% 실패; 단독 2 wt%; 과잉 fibrillation은 역효과; 저전단에도 fibril화 | `--ptfe-fibril`∈(0,1] morphology knob(§F1 hook, magnitude 미앵커) + PTFE fibril 기하(D,L) | ★ 그들 0.6/2 wt% = 우리 fibril-web 성립 하한의 **첫 실험앵커 후보** (LIB 건식이지만 fibrillation 자체는 공정물리 공통 — Lee2025/Liu2025/Mun2025와 같은 계열) |
| 혼합(전단) | ball mill ×3 > planetary ×1 (용량↑·STD 16.52→4.28) | ADDITIVE_PROCESS 3×3(ballmill/thinky/handmix) — 방향만, magnitude 미앵커 | ★ **분산도→성능산포** 정량 = A5 dispersion-CV 실험앵커 (그들 STD가 우리 CV의 실험 대응) |
| porosity/τ | PC_PTFE73 porosity↑(25.9% 또는 ~22.3% — 중의적) vs PVdF 17.7; τ 1.30/1.40; **높은 porosity = 장점**(전해질 침투) | 우리 ASSB: porosity = 죽은 공간(σ_ionic↓); real_14 15.6%; τ_Laplace 채널 | ⚠ **이온위상 역전** (LIB pore=전도체 / ASSB SE망=전도체) — "binder가 porosity 올려 좋다"는 **전이 금지**.  숫자는 binder-종속 porosity 변화 사례로만 |
| 시뮬 스케일 | **분자만**(MLP-DFT+MD 10 ps); 입자·전극 스케일 모델 없음 | DEM(전달)+MPM(역학)+additives 시딩; 분자스케일은 SDCP MLIP(사용자) | 상보 — 그들 분자스케일 방법론(15-배향 E_ads·400 K MD hold-test)은 우리 SDCP 검증에 이식 가치; 우리 입자스케일은 그들이 비운 칸 |
| AM 균열 | 사이클 후 PTFE계 NMC 2차입자 파쇄 vs PC_PTFE73 무균열 — **binder cohesion이 AM 파괴 억제** | Auerbach 압밀-접촉응력 파괴(A9 압밀-버전 충족); 사이클-버전 미보유(A10) | driver 다름(사이클 응력 vs 압밀 접촉응력) — binder-cohesion↔AM-fracture 결합은 우리 fracture 모델에 없는 축(정성 참고) |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **SDCP 개념 정당화 인용**: "이온성 표면앵커 바인더(bollard)로 PTFE 접착·규제 한계를 넘는다"는 아이디어가
  Adv. Mater. 2025에 독립 선례로 존재 — 우리 SDCP(술폰산 앵커)의 novelty는 **앵커+전자전도 겸업(단일 도전바인더) +
  입자스케일(MPM/DEM) 매핑**에 있음을 명확화.  E_ads 사다리(이온성≫극성≫vdW)는 우리 doped≫neutral 방향의 외부 확인.
- ② **MD hold-test 이식** (SDCP 검증 강화): 우리 E_bind는 single-point — 그들처럼 **400 K NVT-MD 수 ps 탈착
  시험**(표면거리 시계열)을 SDCP-NCM에 돌리면 "앵커가 동역학적으로도 유지"를 보일 수 있음 (가압 후 anchoring
  잔존 SEM-루프의 계산 짝; A4′ 검증항목 ④와 연결).
- ③ **A5 dispersion-CV 앵커**: 혼합법→용량 STD(16.52→5.59→4.28 mAh/g) = "분산 불균일→성능 산포" 정량 —
  우리 dispersion CV축(⛔ A5)을 설계할 때 실험 대응물.  ball mill ×3 채택 논리도 ADDITIVE_PROCESS 행과 정합.
- ④ **PTFE fibrillation 하한 앵커**: dough 성립 PTFE ≥0.6 wt%(앵커 지원)·2 wt%(단독), 0.2 wt% 실패 —
  `--ptfe-fibril`/PTFE 함량 축의 문헌 하한.  W2 바인더 σ_ion 페널티도 바인더별 세분화 근거(27× 필름차).
- ⑤ **비교셋에 SDCP+PTFE 콤보 후보**: 그들 최적이 "anchored 7 : rope 3" 하이브리드 — 우리 비교셋(VGCF+PTFE /
  SDCP-only)에 **SDCP+PTFE 소량** 셀을 추가하면 "앵커가 rope 필요량을 줄인다" 가설을 우리 프레임에서 시험 가능.
  (SDCP–PTFE 결합에너지는 그들 Na–F −0.35 eV의 대응물 — 우리 미계산, MLIP 후보.)
- ⑥ **A3 cohesion 실험앵커 목록에 등록**: peel 1.68× / R_ct 성장률 / 사이클 후 AM 파쇄 유무 — SAICAS/peel 계열
  system-레벨 앵커(계면 γ와 계층 구분해 사용).

## 9. 인용 가능 문장 (deck/paper용)
- "An ionically chemisorbed 'bollard' binder that anchors PTFE fibrils to the cathode-oxide surface
  (Na-mediated E_ads −2.24 eV vs −0.09 eV for vdW-only PTFE; Kang et al., Adv. Mater. 2025) independently
  establishes the concept class of surface-anchored binders for dry electrodes — our SDCP extends this
  class by making the anchor itself electronically conductive (sulfonate–NCM insertion, E_bind −4.8 eV MLIP)
  and by mapping the anchor energy to a particle-scale interface cohesion (γ ≈ 0.9–2 J/m²)."
- "Their molecular-scale ladder (ionic ≫ polar ≫ vdW adsorption) and 400 K MD hold-test provide an
  independent methodological template for validating our SDCP anchoring beyond single-point binding energies."

## 10. 주의/한계 (over-claim 방지)
- **LIB 액체전해질** — SE 없음.  porosity·swelling·D_Li⁺·CEI는 **이온위상 역전**(pore=전도체) 아래의 결과 →
  우리 ASSB porosity/σ_ionic로 절대 전이 금지 (binder-porosity 부호까지 반대로 읽힐 수 있음).
- **porosity 문장 중의적**: "25.9% higher porosity than PVdF (17.7%)" — 절대 25.9% vs 상대 +25.9%(≈22.3%) 판별
  불가(Table S3 = SI, 미확보).  게다가 **밀도계산 porosity**(tap density 기반)지 토모/porosimetry 아님 — 수치
  신뢰 중간, TREND로만.
- **필름 E = MPa 스케일**(PTFE 3.50, PC_PTFE 0.15 MPa) — 다공 fibril 시트의 유효값.  bulk PTFE ~0.3–0.5 GPa
  (우리 ADD dict 0.30 GPa)와 **1000× 차이** → MPM 재료입력으로 직접 사용 금지, soft-phase 서열/비율만.
- **peel(N/cm) ≠ 계면 γ**: 0.96 N/cm ≈ 96 J/m² 규모는 테이프·소성산일 포함 시스템값 — 우리 DFT γ 0.93 J/m²와
  100× 층위 차이.  비율(1.68×)만 전이.
- **E_ads = fragment-스케일**(CMC monomer/PAA dimer/PC monomer-graft/PTFE dimer) + NMC 표면 facet 미기재 +
  MLP 종류/트레이닝 SI-only → 우리 −4.8 eV와 **절대 비교 금지**, 사다리(서열)만.  MD도 10 ps(짧음)·400 K(가혹) —
  탈착 kinetics의 정성 시연.
- **"first PTFE-less binder" 표현은 마케팅** — 실제는 PTFE-**감축**(2→0.6 wt%, >70%↓); fibrillation은 여전히
  PTFE가 수행 (PC는 fibril화 안 함).
- 캘린더링/롤 조건·MLP 상세·Table S1–S3 등 **SI 미확보** — 본문 stated 값만 수록.
- 저자 소속상 현대차 공동연구(응용 지향) — 선행 DBE 대비 우월 주장(Fig 5i)은 자사-우호 셀렉션 가능성 감안.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
