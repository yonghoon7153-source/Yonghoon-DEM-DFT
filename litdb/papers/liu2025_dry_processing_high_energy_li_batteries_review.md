<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest (리뷰). -->
# 건식공정(DPT)으로 고에너지밀도 Li 전지 전극·SE막 만들기 — DPC / 분무 / 압출 / **바인더 섬유화(PTFE)** 4대 기법 총설, LIB→ASSB 적용 — Liu et al. (Small 2025, 리뷰)

> slug `liu2025_dry_processing_high_energy_li_batteries_review` · DOI `10.1002/smll.202510454` · type `REVIEW (건식공정 총설; 실험·시뮬 *원저 아님* — 문헌 종합)` · PDF `Liu_2025_Small_DryProcessing_HighEnergyDensity_LiBatteries_Review.pdf` · digested `2026-06-26` · status ✅

---

## 1. 한 줄 요약
**용매를 안 쓰는 건식공정(Dry Processing Technique, DPT)** 으로 **두꺼운 고로딩 전극 + 초박막 고체전해질(SE)막**을 만드는 4대 기법
(① 직접분말압축 DPC, ② 건식분무 DPSD, ③ 분말압출성형 PEM, ④ **바인더 섬유화 BF — PTFE**)을 **메커니즘·장단점·재료별 적용성**으로
정리한 **리뷰**.  LIB(액체전해질)와 ASSB(전고체) **양쪽**을 다루며, **PTFE 섬유화가 산업화 잠재력 최고**(Tesla 4680 채택)지만
**(a) 공정 민감성**(온도·습도·입경·기계물성), **(b) PTFE의 Li-metal 환원분해**(저전위서 LiF화 → 음극 SEI 파괴), **(c) 두꺼운 전극의
이온/전자 percolation 한계**가 상용화의 3대 장벽이라 결론.  ★ **우리(DEM+MPM)에겐 경쟁 시뮬이 아니라** — (i) **PTFE 섬유화 CBD =
우리 CBD morphology 모델의 공정-물리 출처**(Fig 3 + §2.2.4), (ii) **DPC = 우리 cold-press 압밀의 공정 명칭**, (iii) **SE막
바인더 wt%↔σ↔두께 trade-off 표**(Table 2 = porosity/σ 데이터 앵커), (iv) **"바인더가 σ 막는다"의 정성 문헌 종합**(우리 backlog A3/Stage-2의 동기) 을 주는 **공정-맥락/CBD 청사진**.

**소재·이온위상 주의(리뷰 전반):** 이 리뷰는 **LIB(액체전해질) + ASSB(고체) 모두**를 섞어 다룬다.  **LIB 섹션(§2–§3)** 은 전해질이
*공극(pore)* 에 차서 **porosity = GOOD**(이온경로) — 우리 ASSB(SE 고체망=전도체, porosity = BAD)와 **위상 정반대**.  **ASSB 섹션
(§4)** 만 우리와 같은 위상(LPSCl SE 입자망).  → 수치·결론을 끌어올 때 **반드시 LIB-칸인지 ASSB-칸인지 구분**(§B 캐비엇 참조).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (다룬 범위) | 연구유형 |
|---|---|---|---|---|
| **Yu Liu, Pengbo Fang, Bohua Wen, Xiangkun Wu*(교신, xkwu@ipe.ac.cn), Lan Zhang*(교신, zhangl@ipe.ac.cn)** — **Institute of Process Engineering(IPE), Chinese Academy of Sciences(CAS)**, Beijing; + Univ. of CAS; + Tsinghua Shenzhen Int'l Grad School(Wen); + Longzihu New Energy Lab, Henan Univ.(Zhang) | **Small 2025, 21, e10454** (REVIEW; 접수 2025-08-27, 개정 2025-09-26, 게재 2025-10-19) | **10.1002/smll.202510454** | **건식공정 전반**: LIB 양극(LFP/NCA/NCM/LCO/LTO·graphite·Si 음극) + **ASSB**(LPSCl·LGPS·LPS·Li₃InCl₆·할라이드 SE + NCM·LCO·S/Li₂S·LMO CAM); 도전제 PTFE/PVDF/CNT/그래핀/Super-P/KB; 두꺼운 전극·초박 SE막 | **REVIEW**(문헌 종합 — *원저 실험·시뮬 데이터 아님*; 모든 수치는 인용된 1차 문헌에서 옴) |

> ★ **저자 그룹 성격**: IPE-CAS(Lan Zhang 그룹 — "advanced electrolytes(liquid+solid), functional binders, high-energy cathode,
> electrode structure optimization").  1저자 Yu Liu = 석사과정, "dry processing 전극 kinetic 최적화" 전공.  → **건식공정 + 바인더 +
> 구조최적화** 가 그룹 코어 = 우리 CBD/구조 작업과 같은 관심사의 *공정/리뷰 쪽* 동반자.

## 3. 핵심 물성 (수치)  ★
> ⚠ **전부 인용 문헌값(stated, 2차 인용)** — 이 리뷰 자체의 측정/시뮬 아님.  digitized 표기는 Fig 곡선에서 추세로만 읽은 것.
> LIB-칸/ASSB-칸 구분 컬럼 필수.

### (가) ASSB SE막 — bafinder wt% ↔ 두께 ↔ σ_ionic (Table 2, **우리와 같은 위상**) ★★
| SE | 바인더·함량 | 두께 µm | σ_ionic mS/cm | 출처 ref | 우리 관점 비고 |
|---|---|---|---|---|---|
| **LPSCl** | **PTFE 0.5 %** | **15–20** | **1.7** | [102] Wang | ★ 얇은 LPSCl막·저-PTFE → σ 높음 (Lee2025 SSE 1.04 계열) |
| **LPSCl** | PTFE 0.2 % | 40 | **8.4** | [112] Li | ★ PTFE *더 적을수록* σ↑ (8.4 = 바인더 최소) |
| LPSCl | Polycaprolactone(PCL) 7 % | 80 | 0.85 | [113] Su | 폴리머 바인더 多 → σ↓ |
| LPSCl | Thermoplastic polyamide(TPA) 3 % | 25 | **2.1** | [17] Hu | TPA = 비-PTFE 대안, σ 양호 |
| Li₃InCl₅(할라이드) | PTFE 0.5 % | 15–20 | 1.0 | [102] | 할라이드 SE (LPSCl ~1.7의 ~0.6×) |
| Li₆.₅La₃Zr₁.₅Ta₀.₅O₁₂(LLZTO, 산화물) | PTFE 0.5 % | 15–20 | 0.52 | [102] | 산화물 가넷 (σ 더 낮음) |
| Li₅.₇PS₄.₇Cl₁.₃ | 0.5 % PTFE + **PEVA scaffold** | 40 | 1.1 | [101] Fan | scaffold가 PTFE 환원 완화 |
| LGPS(Li₁₀GeP₂S₁₂) | PTFE 1 % | 100 | 0.34 | [110] | 두꺼운 막(100 µm) |
| Li₅.₄PS₄.₄Cl₁.₆ | PTFE 0.2 % | 30 | 8.4 | [22] | |
| LPSCl | PTFE 0.5 % | 18 | 0.85 | [111] | |

### (나) ASSB 양극 — 조성·로딩·사이클 (Table 3, **우리와 같은 위상**) ★
| 양극 조성 wt% | SE | 음극 | areal 로딩 | 사이클 성능 | 출처 |
|---|---|---|---|---|---|
| NCM622:LPNS:AB = 57.7:38.5:3.8 | LPNS | In | 61.22 mg cm⁻² | 0.1C, 50 cyc, **91.7 %** | [129] |
| **NCM811:LPSC:VGCF = 85:12.66:2.34** | LPSCl | Li | **122.4 mg cm⁻²** | 0.2C, 50 cyc, **>90 %** | [126] Kim core-shell |
| LiCoO₂:Li₃InCl₆ = 85:15 | LPSCl | Li/C | 15 mAh cm⁻² | 5 mA cm⁻², 100 cyc, ~90 % | [124] |
| **NCM:LPSC:VGCF:PTFE = 79.6:16.9:2.98:0.5** | LPSCl | Li/In | **5 mAh cm⁻²** | 1C, 500 cyc, **>95 %** | [134] **Lee 2025(=co-rolling 자매)** |
| S:VS₂:LPS = 20:40:40 | LPS | Li/In | 15.5 mg cm⁻² | 0.12 mA cm⁻², 10 cyc, 67 % | [132] |
| LiCoO₂:4-Aminobenzonitrile = 99:1 | LPSCl | Li | 3.06 mg cm⁻² | 0.2C, 100 cyc, 77.2 % | [133] |
| LTG₀.₂₅PSSe₀.₂(=AEA) | LPSCl | Li/Si | 2 mAh cm⁻² | 2.5C, 1000 cyc, 82.3 % | [135] |
| Li₁.₃Fe₁.₂Cl₄(=AEA) | LZO/LPSCl | Li/In | 3.8 mAh cm⁻² | 5C, 3000 cyc, 90 % | [136] |

### (다) LIB 상용셀 — porosity (Table 1, **위상 정반대 LIB**, 절대 동일시 금지)
| 셀 | CAM | 양극 porosity % | areal mAh cm⁻² | 출처 |
|---|---|---|---|---|
| Tesla 4680(Model Y) | NCM811 | n/a(Fig2서 ~10–13 추정) | **5.00**(음극 5.49) | [31,36] |
| CATL LFP6228082 | LFP | **32** | 2.74 | [32] |
| LG M50-21700 | NCM811 | **25** | 4.87 | [35] |
| Samsung 25R/30Q-18650 | NCA | **9** | 2.73/2.99 | [30] |
| Sony VTC5A/6 | NCA | **13/15** | 2.50/3.16 | [30] |
> ⚠ LIB porosity 9–32 % 는 **전해질이 차는 *좋은* 공극** — 우리 ASSB porosity(나쁜 공극, 채울 SE 필요)와 **물리 의미 정반대**.
> 에너지형(energy-type)은 porosity↓·로딩↑, 출력형(power-type)은 porosity↑(Table 1 + Fig 2 = "porosity는 좁은 범위로 관리").

### (라) 핵심 정량 수식·앵커 (본문 stated)
| 항목 | 값/식 | 맥락 | 비고 |
|---|---|---|---|
| **SOA LIB 에너지밀도 한계** | **~300 Wh kg⁻¹** | intercalation 화학 한계 | 리뷰 동기(Si·S·Li-metal로 돌파) |
| **두께 한계식 h_max** (Eq 1) | **h_max = 0.41·(G·M·φ_rcp·R³/2γ)^(1/2)** | 슬러리 캐스팅 두께가 *고체-공기 계면장력*에 제약 | G=전단계수, M=배위수, φ_rcp=RCP 부피분율, R=입경, γ=표면에너지 (Johns ref) |
| **유효용량식 Q_eff** (Eq 2) | **Q_eff = Q₀·(ε/h·τ)·D₀C₀F/((1−t₊)I)** | 두꺼운 전극 kinetics: porosity ε / 두께 h / tortuosity τ | ★ **ε, h, τ 가 두꺼운 전극 핵심**(우리 porosity·τ 모델과 같은 변수) |
| **전해질 침투깊이 L_d** (Eq 3, Gallagher) | **L_d = (ε/τ)·D₀C₀F/((1−t₊)I)** | Li⁺ 농도가 0이 되는 깊이 = AM 활용 한계 깊이 | ★ τ↓ → L_d↑ → 두꺼운 전극 활용↑ ⇒ **"tortuosity 저감이 두꺼운 전극의 궁극 목표"** |
| **Tesla 4680** | 양극 **5.00**/음극 5.49 mAh cm⁻², 음극 건식공정 | Panasonic·Tesla | 건식공정 상용화 1호(graphite 음극) |
| **PEM 초후막** | LCO **180 mg cm⁻²**, areal **17 mAh cm⁻²**@C/25 | Sotomayor [61] | 압출성형 최고 로딩 |
| **DPC 초후막** | LFP **~15 mAh cm⁻²**(최대 1 mm 두께), 98 % 활용 | Hu [50] | 직접압축 ~26 mg cm⁻²(porous graphene, Walker [51]) |
| **bulk σ (ASSB SE)** | LPSCl·LGPS 등 ASSB SE bulk σ는 cold-press만으로 발현 | (Eq context) | E < 25 GPa SE = cold press / E > 50 GPa 산화물 = hot press 필요 |
| **LLZAO 소결** | 62 MPa서 900/1000/1100 ℃ → rel.density 86/97/99 % | 산화물 = 고온소결 필요 | ★ **황화물은 냉간가압만으로 치밀화**(우리 cold-press 전제) ↔ 산화물 대조 |

**Heckel / coordination Z / coverage% / E_SE / σ_y / 정량 porosity@P / DEM 파라미터**: **n/a** — 리뷰라 *압밀 정량 모델·접촉면적·배위수·탄성계수
원저 데이터 없음*.  porosity는 LIB 상용셀 표(Table 1, 전해질-공극)뿐, ASSB 압밀 porosity 정량 없음(§B 캐비엇).

## 4. 시뮬레이션 방법 ★
- **code / version**: **없음** — 리뷰.  DEM·MPM·FEM·RNM **원저 시뮬 일절 없음**.
- **DEM 접촉법칙 / 재료 파라미터 (E,ν,μ,COR,σ_y)**: **n/a**.  단 **Eq 1(h_max)** 에 **G(전단계수)·M(배위수)·R(입경)·φ_rcp(RCP)·γ(표면에너지)**
  가 등장 — 이는 *슬러리 캐스팅 두께 한계* 의 연속체 표면장력 모델(Johns)이지 입자 DEM 아님.  그래도 **M(배위수)·φ_rcp(random close packing)·R(입경)
  = 우리 DEM descriptor(coordination Z, packing, PSD)와 같은 물리량** 이 두께 한계식에 직접 들어간다는 점이 흥미(우리 packing 변수가 *제조 두께*에도 인과).
- **bond/binder 모델**: 모델 없음.  **그러나 PTFE 섬유화 메커니즘을 본문·Fig 3로 서술**(§2.2.4 + 5.1):
  "AM 거친 표면이 먼저 바인더를 *anchor*, 그 다음 상호 *전단력*으로 PTFE가 *fibrous structure로 fibrillate*"(Matthews [64] 나노섬유망 형성기구 인용) —
  = 우리 CBD 시드 모델(curl + nucleate-on-carbon + shear-draw)의 *공정 물리 출처*.  "AM morphology(구형 vs 플레이크) + 화학이 fibrillation 효율을 좌우"(Shen/[65,66,67]).
- **MPM/continuum / 전달 솔버**: **n/a**.  σ_ionic·porosity·tortuosity는 모두 **인용 문헌의 측정/시뮬**(예: 일부 인용 논문이 nano-CT·tortuosity 산출, Fig 4a Jin [78] LCO τ 4.49→4.76→3.80→5.30, Fig 4b LFP-MWCNT/SuperP/GNP τ).
- **입자 처리** ★ (DEM판 "무질서 처리"): 리뷰라 입자 모델 없음.  단 **리뷰가 종합한 *실험적 입자 거동* 두 가지가 우리 모델이 흉내내는 것의 문헌 확인**:
  (a) **입경비(AM/SE) 의존 percolation** — "AM 입자↑·SE 입자↓ → AM-SE seepage network↑ → AM 활용↑ + AM 비율 60→70 wt%까지 SE 가용성 유지"(Ceder [125], Fig 8a) = 우리 12:4:1 packing·size=packing;
  (b) **PTFE는 진짜 소성 draw·fibrillate**(섬유망 SEM 인용 Matthews [64]·Shen [63]) = 우리 CBD vol-conserve draw.
  ⚠ AM 파괴(PC-NCM crack)는 이 리뷰엔 **명시 없음**(자매 Lee2025·Kang2025가 소유) — 여기선 다루지 않음.
- **도메인/RVE / servo / seeds / 압력범위**: **n/a**.  단 공정 압력 종합: **DPC 100–300 psi(~0.7–2 MPa) 예열압축**(Hu [50]) / 압연 **20–25 MPa**(Walker [51]) /
  ASSB cold press **수백 MPa**(LPSCl·LGPS) — 우리 제조 300 MPa·작동 수 MPa 구분과 같은 계열(단 인용 문헌별 상이).
- **특이사항/공정 레버 (우리 시뮬 입력에 시사점)**:
  - **L1 PTFE 함량**: SE막 PTFE 0.2→0.5→1→3→7 %로 갈수록 두께·σ trade-off(Table 2: 0.2 % → σ 8.4 / 7 % PCL → 0.85) — **저-PTFE가 σ 최선**(우리 backlog A3 "바인더 페널티" 정량 근거).
  - **L2 칼렌더링 온도**: PVDF(DPSD) ~177 ℃ 근처(바인더 융점)서 입자결합↑; BF는 전단력 상온/가열.
  - **L3 두께 vs tortuosity**: 두꺼운 전극은 ε·τ 관리(Eq 2,3) — vertical channel(template/freeze-dry/magnetic alignment)로 τ↓ 하나 *기계강도·압밀저항↓*(trade-off 명시).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **Fig 1 a,b** | 고체 LMB 에너지밀도 추정: (a) NCM vs S 양극 areal 용량 ↑ → 에너지↑(3 vs 9 mAh cm⁻²); (b) **SE 막 두께 100→20 µm ↓ → 에너지 300→650 Wh kg⁻¹↑** | ★ **초박 SE막이 에너지밀도 핵심** = 우리 박막 SSE 맥락(Lee2025 50 µm); 우리 RVE는 막 제조 안 다룸 |
| **Fig 2** | 상용 LIB 양극 16종 areal 용량 + porosity(LFP/NCA/NCM 그룹별) — **에너지형 porosity↓·로딩↑** | LIB porosity 9–32 % = **전해질 공극(GOOD)**; 우리 ASSB와 위상 반대(직접 비교 금지) |
| **★ Fig 3** | ★★ **전형 전극 미세구조 모식 + 핵심 descriptor**: AM 입자들 + **CBD(carbon-binder domain)** 가 표면을 코팅 + SEI/CEI; σ_eff,e(전자, 빨강)·**σ_eff,i(이온, 초록)** 경로 화살표; 5대 파라미터(AM 부피분율·CBD/CC 접촉비·σ_eff,e·porosity ε·노출 AM 표면) | ★★★ **우리 CBD 모델·σ_e/σ_i 경로·coverage의 *교과서 모식*** — Fig 3i(Lee2025)와 같은 "CBD가 AM 코팅+전자/이온 경로" 그림.  우리 5 descriptor(φ_AM·coverage·σ_e·porosity·노출표면)와 1:1 |
| **Fig 4 a** | DP-LCO에 flour 첨가(0 % vs 1 % F): nano-CT로 **작은 공극→큰 공극 병합 → τ 4.76→3.80↓**(rate↑); SC/0%F/1%F/2.5%F τ 비교 + 사이클 | tortuosity 저감 기법(공극구조 조절) = 우리 τ_Laplace·pore network 관점 |
| **Fig 4 b** | DP-LFP에 **0D Super-P / 1D MWCNT / 2D GNP**: 섬유상 MWCNT가 **interconnected 망 → τ↓·porosity 유지**(rate 최고 4C); GNP/Super-P는 응집→τ↑ | ★ **도전제 형상(0D/1D/2D)이 τ·porosity·σ 좌우** = 우리 VGCF(1D 섬유) vs Super-P(0D) 모델 근거 |
| **Fig 4 c** | NCM811 전극: **M@EP(MWNT+epoxy resin) 3D 가교망** → 저항 0.25 Ω·cm 로 급감 + CV/peak-current kinetics | 도전제망 3D 연결성 = 우리 percolation f_p |
| **Fig 5 a** | DPT 두꺼운 전극 전하수송: **PAN이 C≡N–Li⁺ 상호작용으로 Li⁺ 보조수송**(LCB=PTFE+PAN binder) → 22.2/53.8 mg cm⁻² 고로딩 80.8 % 유지 | **이온전도성 바인더** = PTFE 절연 페널티의 대안(우리 CBD 양역할 A3) |
| **Fig 5 b,c** | (b) PPC(polypropylene carbonate) 바인더 Li⁺ 전도(C=O 배위) 800 cyc; (c) **LiPF₆ vs LiClO₄ 전해질이 PTFE-CEI 조성 결정**(LiF/LiCl) | 바인더·전해질 화학이 계면 결정 — 우리 모델 밖(화학 축) |
| **★ Fig 6 a,b,c** | ★ **PTFE 환원분해 억제 전략 3종**: (a) graphite에 **PEO·P(VDF-TrFE-CFE) 코팅** → ICE 67.2→79.1/77.8 %; (b) **FEC 첨가제** → PTFE 분해 피크↓·안정 SEI(D/G 0.62→0.92); (c) **PVP 바인더** → 비가역용량 48→24 mAh g⁻¹↓ | ★ **PTFE의 Li-metal/저전위 환원분해(LiF화)가 음극의 핵심 약점** — ASSB Li-metal 음극서 동일 위험(§4 음극) |
| **Fig 7 a,b,c** | ASSB SE막 BF 이슈: (a) PTFE+Li → Li₂S+LiF로 분해; (b) **PEVA scaffold** 가 LPSCl막에 강성 부여; (c) **저융점 이온전도 폴리머(PCL+LiTFSI+IL)** 가 SE 균일 코팅 → 입자간 이온수송↑ | ★ **PTFE 환원 + scaffold 보강** = SE막 제조의 역학·화학 trade-off(우리 backlog A3 scaffold) |
| **★ Fig 8 a** | ★★ **ASSB 복합양극 전하수송**: **SE 입경(1.5/3/5 µm) ↓ → 미세 seepage network↑ → 용량↑**; AM(CAM) 입경 4–12 µm ↑ → 용량↑ (모델+실험 둘 다, 1.5·3 µm SE) | ★★★ **우리 "작은 SE → σ↑(packing) / 큰 CAM → 용량↑" 의 리뷰-종합 근거**(Ceder [125], = 우리 size=packing + Bazzoun) |
| **Fig 8 b** | **NCM core-shell**: 비코팅 NCM vs **LPSC shell 코팅(mechanofusion)** → 표면 microvoid 제거·packing porosity void 감소 | ★ **SE-코팅 CAM = 우리 coverage/SE-film 모델**(Kim [126], 122 mg cm⁻² 고로딩) |
| **Fig 8 c,d** | (c) **redox mediator**(Li₂S/NbSe₂) 전하경로; (d) **LBPSI glass-phase SE = 전자+이온 동시수송** 매질 | S-양극 redox 매개(우리 범위 밖, S 화학) |
| **Fig 9 a–d** | ASSB 계면 완화 전략: (a) **AEA(all-electrochem-active) 양극**(SE 없이 전 활물질); (b) all-in-one 전극(MS+S, DCC 경로); (c) **MH(monophase homo-interface) LTMO**(LCO·LMNC, SE-free); (d) 균질 LTG₀.₂₅PSSe₀.₂(σ 0.22 mS/cm + 작은 부피변형 1.2 %) | SE-free 전극 설계(우리 SE-입자망 모델과 다른 패러다임) |

## 6. Post-processing ★
- **무엇** (리뷰가 *종합한* 기법들, 원저는 인용처):
  - **tortuosity**: nano-CT 3D 재구성 → τ 산출(Fig 4a Jin LCO, Fig 4b LFP). Eq 2,3의 ε/τ가 두꺼운 전극 활용 핵심.
  - **σ_ionic/σ_e**: 인용 문헌별 EIS(이온)·DC(전자) — 리뷰 자체 측정 아님(Table 2 σ는 인용값).
  - **porosity**: LIB 상용셀 = "추정"(material density 기반, Table 1 footnote); ASSB는 정량 porosity 종합 없음.
  - **morphology**: SEM/advanced microscopy로 PTFE 섬유망 구조 분해(Matthews [64] 나노섬유망 형성기구).
- **도구**: 리뷰라 도구 없음 — 인용 문헌이 nano-CT(Fig 4)·SEM·EIS 사용.
- **수치화·플롯·기록**: 모든 수치 = **2차 인용**(stated from refs).  Fig 1,8a 만 *모델 추정 곡선*(에너지밀도·용량, 인용 모델).  → **절대값 전이 시 반드시 원저 확인**.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 리뷰 (Liu 2025) | 우리 (DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| 성격 | **리뷰**(공정 종합, no 원저 data/model) | DEM(전달)+MPM(역학) 원저 시뮬 | frame[5] — 우리는 *구조→σ 정량*; 리뷰는 *공정-기법 지형도* (보완) |
| 범위 | **LIB + ASSB**, 4대 건식기법 | ASSB(LPSCl+NCM) 압밀·전달·역학 | 리뷰가 *공정 상류*(제조법)·*LIB까지* 넓음; 우리가 *ASSB 미세구조-σ*로 깊음 |
| 소재 | LPSCl·LGPS·할라이드·산화물 SE + NCM/LCO/S CAM + PTFE/CNT/그래핀 | LPSCl + NCM811/82 + VGCF + PTFE | ★ 핵심소재(LPSCl+NCM+PTFE) **겹침**; 리뷰가 SE·CAM·도전제 종류 더 넓게 |
| **PTFE 섬유화 CBD** | ★ **공정 메커니즘 서술**(Fig 3 + §2.2.4: anchor→shear→fibrillate) | 우리 CBD: curl·vol-conserve·nucleate-on-carbon 시드 모델 | ★ **리뷰 = 우리 CBD 모델의 *공정-물리 출처/교과서 모식*** (Fig 3 ≈ 우리 5 descriptor) |
| **바인더 σ 페널티** | ★ **정성 종합**: PTFE↑→σ↓·절연; 이온전도 바인더(PAN/PPC)로 대안 | 우리 CBD는 σ_e *기여*만, PTFE 절연 미반영 | ★ **backlog A3/Stage-2 동기**: 리뷰가 "바인더가 막는다 + 대안"을 *지형도*로; 정량은 자매 Lee2025(0.5→5 %→σ 3000×↓) |
| **DPC = cold-press** | ★ **DPC**(direct powder compaction) = 분말 고압압축 후 CC 결합 | 우리 DEM cold-press @300 MPa + MPM 소성 | ★ **우리 압밀의 *공정 명칭* = DPC**; 리뷰가 ASSB cold-press(E<25 GPa SE)/hot-press(산화물 E>50) 경계 정리 |
| **입경비 packing** | ★ Ceder [125] 종합: 작은 SE+큰 CAM → seepage↑, AM 60→70 wt% (Fig 8a) | 우리 12:4:1 + Furnas dip + size=packing | ★ **우리 size=packing의 리뷰-종합 근거** (Bazzoun·Minnmann과 합류) |
| SE막 두께-σ | Table 2: PTFE wt%·두께·σ trade-off | 우리는 RVE(막 제조 안 함) | 리뷰가 *막 제조* 다룸(우리 영역 밖); 우리가 *RVE 미세구조-σ* 깊음 |
| porosity 정량 | LIB 상용(9–32 %, 전해질-공극) only; ASSB 정량 없음 | DEM 15.6 % / MPM 16.7 % @300(Minnmann 10 %) | ★ **우리 강점**(정량 ASSB 압밀 porosity·Heckel); 리뷰는 LIB-공극(위상 반대)뿐 |
| 전달 솔버 | 없음(인용 EIS/nano-CT τ) | Kirchhoff/Holm + Stage-E + 삼중항 σ_i/σ_e/σ_thermal | **우리 강점**(명시적 접촉망·삼중항·constriction) |
| morphology/변형장 | Fig 3 모식·SEM 인용(정성) | MPM 진짜 소성 형상변화·void-fill·Σdg | **우리 강점**(MPM 정량 변형장); 단 리뷰 Fig 3 = 우리 CBD 그림의 검증 |

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 건식공정 미세구조 ↔ 우리 packing+CBD+morphology
- **① DPC(직접분말압축) = 우리 DEM cold-press 압밀의 공정 명칭.** 리뷰 §2.2.1: DPC = "AM+CA+binder 균질분말을 *고압*으로 몰드에서 압축 → CC와 결합".
  Hu [50] LFP 100–300 psi 예열압축 → 최대 1 mm 두께 15 mAh cm⁻²; Walker [51] 압연 20–25 MPa → ~26 mg cm⁻². ★ **= 우리 cold-press @300 MPa + MPM 소성**의
  *상용 공정 짝*.  단 리뷰가 강조하듯 DPC는 "극단적 압축력 필요 + post-heat" → 우리 18× 연화/소성 흐름이 *왜 그 고압이 필요한가*(강체 floor 깨기)를 미세구조로 설명.
- **② ASSB cold-press vs hot-press 경계 = 우리 E_SE 항의 공정 근거.** 리뷰: **E < ~25 GPa SE(황화물 LPSCl·LGPS) = cold press만으로 입자간 intimate contact** /
  **E > 50 GPa 산화물(LLZO) = hot press(900–1100 ℃) 필요**(LLZAO 62 MPa+1100 ℃ → 99 %). ★ **= 우리 "E_SE 강성이 porosity floor를 정한다"(Varkey halide stiffer→37 %)**
  의 *공정 레벨* 확인 — 뻣뻣한 SE일수록 압밀 어려움.  우리 LPSCl(soft 황화물)이 cold-press로 치밀화되는 게 리뷰의 황화물-냉간가압 종합과 정합.
- **③ PTFE 섬유화 CBD = 우리 CBD morphology 모델의 *공정 물리 + 교과서 모식*.** Fig 3(전극 미세구조 + CBD가 AM 코팅 + σ_e/σ_i 경로) ≈ 우리 5 descriptor
  (φ_AM·coverage·σ_e·porosity·노출표면)와 1:1.  §2.2.4 fibrillation 기구("AM 거친표면 anchor → 상호 전단 → PTFE fibrous fibrillate", Matthews [64]·Shen [63]·Tao [62]) =
  우리 `docs/cbd_morphology_roadmap.md` 의 **shear-draw + nucleate-on-carbon** 그림.  ★ **frame[4]: 자매 Lee2025 SEM(Fig 3i/SI 17,18)이 *실험 검증*, 이 리뷰가 *공정-종합 검증*** → 우리 CBD 시드 모델이 *공정-grounded* 임을 이중 인용.
- **④ 도전제 형상(0D/1D/2D) → τ·σ·packing.** Fig 4b: 1D MWCNT(섬유) = interconnected 망 → τ↓·rate↑ vs 0D Super-P·2D GNP = 응집 → τ↑. ★ **= 우리 VGCF(1D 섬유 fibre seed) vs Super-P(0D point seed) 모델링 차이**
  의 리뷰 근거(우리 voxel σ: SuperP 0.0168 < VGCF 0.0298 mS/cm = SuperP가 더 막음 ↔ 리뷰 "Super-P 응집 τ↑"와 같은 방향).
- **⑤ 입경비 packing (Fig 8a, Ceder [125]) = 우리 size=packing·12:4:1.** "SE 입경↓·CAM 입경↑ → AM-SE seepage network↑ → AM 활용↑ + AM 60→70 wt%까지 SE 가용" = 우리 작은 SE가 큰 CAM 간극을 채우는 Furnas packing.
  단 리뷰는 *dip(porosity-vs-AM% 최소)을 다루지 않음* → dip은 여전히 우리(de Larrard/McGeary 기하)가 소유.
- **⑥ porosity 위상 차이 — 절대 동일시 금지.** 리뷰 LIB 칸(Table 1, 9–32 %)은 *전해질이 차는 좋은 공극*; 우리 ASSB porosity는 *채워야 할 나쁜 공극*. ASSB 칸(Table 2,3)은 *두께·σ·로딩*만 주고
  *정량 압밀 porosity 없음* → 우리 15.6 %와 비교할 ASSB porosity 데이터가 이 리뷰엔 없다(자매 Doux 18 %·Minnmann 14 %·우리 DEM 소유).

## B. 적용가능성 (applicability to our model) — CBD 모델(A3) + 압밀 protocol
- **★ A3(CBD 바인더 양역할 / σ 페널티) — 이 리뷰가 *정성 지형도*를 줌(정량은 자매 Lee2025).** backlog A3 = "MPM `--coh` distribution-aware: 과잉 PTFE = σ차단/전해질차단, 부재 = delamination".
  이 리뷰가 **그 양역할의 문헌 종합**을 제공:
  - *부재/약함* → "바인더 낮으면(0.1 wt%) SE막 깨지기 쉬워 scaffold 필요"(§5.2, Fan PEVA / Su PCL) = delamination 쪽.
  - *과잉* → "PTFE↑ → σ↓·절연 + Li-metal 환원분해(LiF화) → 음극 SEI 파괴"(Fig 6,7) = σ차단 쪽.
  - *대안* → **이온전도 바인더(PAN·PPC·PVP·TPA)**, **코팅(PEO/P(VDF-TrFE-CFE))**, **첨가제(FEC/PTFSI)** = A3 "비단조 cap" 의 재료 옵션 목록.
  → **흡수 형태**: A3에 binder modulus(MPa) 항 + **σ 페널티 비단조성**(저-PTFE σ 최선, 과-PTFE σ급감) 추가. **정량 곡선은 Lee2025 Table(0.5/2/5 %→σ)**, 이 리뷰는 *왜·대안*을 채움.
- **★ 압밀 protocol — DPC 공정 압력의 *문헌 범위* 확인.** 우리 제조 300 MPa(Heckel P_y 138) / 작동 수 MPa 구분에 대해 리뷰는 **ASSB cold-press = 수백 MPa**(LPSCl/LGPS, E<25 GPa) 를 종합
  (구체값은 인용 문헌별; Lee2025 자매 500 MPa, Doux 370). **흡수**: 우리 "수백 MPa 냉간가압" 계열이 리뷰의 황화물-cold-press 종합과 정합(절대값은 인용 문헌별 상이 → 추세만).
- **★ SE-코팅 CAM(coverage) — Fig 8b core-shell.** Kim [126] LPSC-shell NCM811(mechanofusion) → microvoid 제거 → 122 mg cm⁻² 고로딩. ★ **= 우리 coverage/SE-film(A4 se_coating) 모델의 *공정 실증***
  — SE가 CAM 표면을 film으로 덮는 것이 packing void↓·계면반응↓. (단 *기계 coverage* 우리 모델 ↔ Kim의 *화학 mechanofusion coating* 은 종류 다름 — coverage 정량은 우리 소유.)
- **★ tortuosity / 두꺼운 전극 식 (Eq 2,3) — 우리 τ_Laplace 변수 정렬.** Q_eff·L_d ∝ ε/τ → **τ↓ 가 두꺼운 전극 활용의 궁극 목표**. 우리 τ_Laplace,eff·R_brug·pore-τ(backlog A6 DiffuDict)와 같은 변수.
  단 **Eq 2,3은 LIB(전해질-공극 τ)** → 우리 ASSB(SE-망 τ)와 *위상 반대* (LIB τ = 공극의 우회, ASSB τ = SE 입자망의 우회). → **공식 형태는 차용, 위상은 구분.**
- **★ 도전제 형상 모델 (Fig 4b) — 우리 VGCF(1D)/Super-P(0D) 시드 정당화.** 1D 섬유 = 망 형성 τ↓ / 0D = 응집 τ↑. 우리 additives.py가 VGCF=straight fibre, Super-P=point seed로 두는 게 리뷰와 정합.
- **⚠ LIB vs ASSB 캐비엇(흡수 시 필수):**
  - **porosity 의미 반대**: LIB porosity↑ = 이온경로↑(GOOD); ASSB porosity↑ = SE-망 단절(BAD). Table 1 의 9–32 % 를 *우리 floor 비교에 쓰지 말 것*.
  - **이온 위상 반대**: LIB 이온은 *공극의 액체전해질*, ASSB 이온은 *SE 고체 입자망(Holm 구속)*. Eq 2,3 τ는 *공극 τ* → 우리 Stage-E constriction(고체 점접촉)과 물리 다름.
  - **σ 절대값**: 리뷰 σ는 *2차 인용* + 인용마다 PTFE %·두께·소재 상이 → **추세/형태만**, 절대 매핑 금지.
  - **PTFE 환원분해**(Fig 6,7)는 *Li-metal/저전위 화학* — 우리 DEM/MPM(역학·전달)이 *안 다루는 화학 축*. "PTFE가 음극서 LiF로 분해"는 *흡수 대상 아님*(맥락 인지만).

## C. frame[5] 위치 (review = positioning) — 우리 시뮬을 어디에 놓나 (softer framing)
이 논문은 **원저가 아니라 리뷰** 라 frame[4](모델 교차검증)·frame[5](DEM↔MPM 분업)에 *경쟁/검증 데이터*를 주지 않는다 — 대신 **우리 작업이 들어앉을 *공정 지형도*** 를 그려준다.
부드럽게 자리매김하면:
- **우리가 owns 하는 칸(리뷰가 비운 정량):** 리뷰는 건식공정의 *기법·장단점·재료 적용성* 을 종합하지만 **(i) ASSB 정량 압밀 porosity·Heckel, (ii) 명시적 접촉망 σ 삼중항(σ_i/σ_e/σ_thermal),
  (iii) 소성 morphology·void-fill 변형장, (iv) Furnas dip 정량** 은 *원저 데이터로 주지 않는다*. ★ **바로 이 네 칸이 우리 DEM(전달·packing·dip)+MPM(역학·morphology)이 채우는 자리** —
  리뷰가 "두꺼운 전극은 ε·τ·percolation이 관건, tortuosity 저감이 궁극 목표"(Eq 2,3)라고 *문제를 정의*하면, 우리가 그 ε·τ·percolation·σ 를 *구조에서 정량 예측* 한다.
- **리뷰가 owns 하는 칸(우리가 안 다루는 상류/넓이):** *막 제조 공정*(co-rolling shear, 칼렌더링 온도, DPC 압축력), *바인더 화학*(PTFE 환원분해·이온전도 바인더·CEI), *LIB까지의 폭*,
  *Li-metal 음극*. → 우리 RVE는 *제조된 미세구조에서 출발* 하므로 리뷰의 *공정 상류* 와 **상보**(우리가 그 공정을 재현한다고 주장 금지).
- **CBD = 두 영역이 만나는 다리.** 리뷰의 PTFE 섬유화 기구(Fig 3, §2.2.4)는 *공정* 이고, 우리 CBD 시드 모델(curl·draw·nucleate)은 *그 결과 morphology* 다 → **리뷰가 공정 물리를, 우리가
  결과 구조-σ를** 맡는 자연스러운 분업.  자매 Lee2025(실험 SEM)·Lyu2025(건조+압연 DEM)와 함께 **"건식공정 미세구조"** 를 3각(리뷰-지형도 / 실험-검증 / DEM-MPM-정량)으로 덮는다.
- **gap(아직 못 채우는 것):** (i) *막 제조 단계의 shear 응력장* — 우리 RVE 압밀은 정수압-유사, co-rolling 전단 아님; (ii) *바인더 화학 분해* — 우리 전달/역학 모델 밖; (iii) *LIB 전해질-공극 위상* —
  우리는 ASSB SE-망만. → 이들은 frame[5] 분업상 *우리 영역 아님* 으로 명시(리뷰·실험·화학계산이 소유).

## 8. 적용 인사이트 (내 연구에 어떻게)  ★
- ① **★ CBD morphology 모델(A3)의 *공정-종합 출처*로 인용.** Fig 3(CBD가 AM 코팅 + σ_e/σ_i 경로 + 5 descriptor) + §2.2.4(PTFE anchor→shear→fibrillate 기구) = 우리
  `docs/cbd_morphology_roadmap.md` 그림의 *리뷰 근거*. 자매 Lee2025(SEM 실험)와 합쳐 **"공정-종합(Liu) + 실험-SEM(Lee) + 우리 시드모델"** 삼중 인용 → CBD 모델이 literature-grounded.
- ② **★ 바인더 σ 페널티 비단조성(A3/Stage-2)의 *정성 지형도 + 대안 목록*.** Table 2(LPSCl PTFE 0.2 %→σ 8.4 / 7 % PCL→0.85) + Fig 5,6,7(이온전도 바인더 PAN/PPC/PVP/TPA, 코팅, FEC 첨가제) →
  A3 에 "저-바인더 σ 최선·과-바인더 σ급감 + 부재시 delamination(scaffold 필요)" 비단조 cap + 재료 옵션 추가. 정량 곡선은 Lee2025, *왜·대안*은 이 리뷰.
- ③ **★ DPC = 우리 cold-press 압밀의 공정 명칭 + 황화물 cold-press / 산화물 hot-press 경계.** "E<25 GPa 황화물 SE는 cold-press만으로 치밀화"(LPSCl) ↔ "E>50 GPa 산화물은 hot-press" =
  우리 "E_SE 강성이 floor 결정"(Varkey)의 공정 근거 + 우리 LPSCl(soft) cold-press 전제 정당화.
- ④ **★ 입경비 packing(Fig 8a) + SE-코팅 CAM(Fig 8b) = 우리 size=packing·coverage·A4 리뷰 근거.** "작은 SE+큰 CAM→seepage↑·AM 60→70 wt%"(Ceder) + "LPSC-shell NCM811 122 mg cm⁻²"(Kim) =
  우리 12:4:1·coverage·se_coating 의 종합 근거(Bazzoun·Minnmann과 합류).
- ⑤ **두꺼운 전극 식 Q_eff·L_d ∝ ε/τ(Eq 2,3) = 우리 τ_Laplace·pore-τ(A6) 변수 정렬** — 단 *LIB 공극-τ 위상* 이므로 공식 형태만 차용, ASSB SE-망-τ 와 위상 구분.

## 9. 인용 가능 문장 (deck/paper용)
- "A 2025 Small review of dry-processing techniques (Liu et al.) positions binder fibrillation (PTFE) as the most
  industrializable solvent-free route (adopted in Tesla's 4680 cell), and frames its electrode microstructure exactly
  by the descriptors we model — AM volume fraction, carbon-binder-domain (CBD) coverage of the AM surface, effective
  electronic conductivity, porosity, and exposed AM area (their Fig 3)."
- "The review consolidates that lowering the PTFE binder content maximizes solid-electrolyte-film conductivity
  (e.g. 0.2 wt% PTFE LPSCl → 8.4 mS cm⁻¹ vs 7 wt% polymer → 0.85 mS cm⁻¹, Table 2) while too little binder leaves the
  film mechanically fragile (requiring a scaffold) — the non-monotonic binder penalty we are encoding into our CBD model."
- "Direct powder compaction (DPC) — the solvent-free high-pressure consolidation route reviewed here — is the process
  name for the cold-press densification our DEM+MPM models; the review's sulfide-cold-press vs oxide-hot-press boundary
  (E<25 GPa cold-pressable LPSCl vs E>50 GPa sinter-required LLZO) is the process-level confirmation that SE stiffness
  sets the densification regime."
- "Smaller solid-electrolyte particles plus larger active-material particles enlarge the AM–SE seepage network and
  sustain AM utilization up to 60–70 wt% AM (review Fig 8a, after Ceder) — the literature synthesis behind our
  size-as-packing 12:4:1 treatment."

## 10. 주의/한계 (over-claim 방지)
- **리뷰 = 원저 데이터/시뮬 0.** DEM/MPM/FEM/RNM 없음. porosity(정량 ASSB)·Heckel·coordination Z·coverage%·E_SE·σ_y·접촉면적 **전부 n/a**.
  모든 수치는 *2차 인용* — **절대값 전이 시 반드시 원저 확인**(예: Table 2 σ는 인용 논문별 측정).
- **LIB vs ASSB 혼재 — 칸 구분 필수.** §2–3(LIB)는 *전해질-공극 위상*(porosity=GOOD, 이온=액체-공극), §4(ASSB)만 우리 위상(SE-망). Table 1 porosity 9–32 %·Eq 2,3 τ는
  **LIB 칸** → 우리 ASSB floor·Stage-E constriction 과 *직접 비교 금지*. Table 2,3 만 ASSB.
- **ASSB 압밀 porosity 정량 없음.** Table 2,3 은 *두께·σ·로딩·사이클*만 — *정량 압밀 porosity 없음*. → 우리 DEM 15.6 %/MPM 16.7 % 와 *비교할 ASSB porosity 데이터가 이 리뷰엔 없다*
  (자매 Doux 18 %·Minnmann 14 %·Sakuda >90 % 가 소유).
- **PTFE 섬유화 = *공정* 검증, 우리 RVE는 그 shear 공정 재현 안 함.** Fig 3·§2.2.4 fibrillation 기구는 *막 제조 전단* — *개념/morphology 검증* 으로만 쓰고, 우리 시뮬이 그 전단 공정을 굴린다고 주장 금지(자매 Lee2025 CBD digest와 같은 캐비엇).
- **PTFE 환원분해(Fig 6,7) = 화학 축, 우리 모델 밖.** "PTFE+Li → LiF·Li₂S 분해 → 음극 SEI 파괴"는 *전기화학 화학* — 우리 DEM/MPM(역학·전달)이 *안 다룸*. 맥락 인지만, 흡수 대상 아님.
- **bulk σ 절대값 스프레드.** 리뷰 Table 2 LPSCl σ(0.85–8.4, 두께·PTFE·측정 상이)는 우리 bulk 앵커 {Cronau 3.0, Lee 2.19, Minnmann/Kim 1.6, Bazzoun 1.02} 와 *측정조건이 다름* →
  **스프레드/추세로만**, 절대 직접대조 금지(특히 8.4 = 박막 conductance, 우리 intrinsic σ 아님).
- **에너지밀도 곡선(Fig 1,8a)은 *모델 추정*** — 인용 모델의 추정치(NCM vs S, SE 두께-vs-에너지). 실측 셀(Lee2025 310 Wh kg⁻¹ 등)과 구분.
- **Mun 2025(#30) 자매 리뷰 부재 확인:** 요청된 `mun2025_dry_electrode_technology_assb_review.md` 는 현재 litdb에 **없음**(파일 미존재). 대신 **자매 건식 digest 2편 존재**:
  (i) **Lee 2025**(`lee2025_corolling_dryprocess_lpscl_ptfe.md`) = *실험 원저*(co-rolling, σ·CBD SEM·PC/SC 파괴 소유);
  (ii) **Lyu 2025**(`lyu2025_3d_dem_drying_calendering_lib.md`) = *DEM 원저*(LIB 건조+압연, σ_e 정성).
  → **이 Liu 리뷰의 UNIQUE 기여 = "건식공정 4대 기법(DPC/DPSD/PEM/BF)의 *교과서적 지형도* + LIB↔ASSB 폭 + 바인더 σ 페널티/대안 *정성 종합* + Table 2,3 SE막·양극 데이터 표"**.
  Lee=실험-깊이, Lyu=DEM-깊이, Liu=리뷰-폭. 겹치는 PTFE 섬유화 CBD는 *세 렌즈*(공정-종합/실험-SEM/DEM)로 상보.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
