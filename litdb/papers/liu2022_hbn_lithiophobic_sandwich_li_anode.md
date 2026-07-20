# Uniform Lithium Deposition Induced by Double Lithiophobic Sandwich Structure for Stable Lithium Metal Anode — Liu et al. (Adv. Mater. Interfaces 2022)

> slug `liu2022_hbn_lithiophobic_sandwich_li_anode` · DOI `10.1002/admi.202200011` · type `exp + DFT(VASP 흡착E·CDD)` · PDF 본문 `82ea256b/093a89d8` · SI `82ea256b/f86934b1` · digested `2026-07-20` · status ✅
> **저자**: Xiaoyu Liu, Zhijian Liu, Hao Yang, Piao Qing, Weifeng Wei, Xiaobo Ji, **Yuejiao Chen***, **Libao Chen*** (Central South University, Changsha — State Key Lab of Powder Metallurgy + College of Chemistry) · Adv. Mater. Interfaces 2022, **9, 2200011** (Received 2022-01-03, Published 2022-03-03)
> **⚠ 논문 정체**: argyrodite/황화물 SE 논문 **아님**. **리튬 금속 음극(Li metal anode) + 집전체(Cu) 위 lithiophobic 코팅(h-BN)** 논문. 우리 캠페인의 *새 축*. 보관·digest 이유 = **DFT Li-흡착E 방법론을 우리 VGCF+h-BN ORCA 프로젝트가 재사용**하기 위함(§10).

---

## 0. 이 digest를 읽는 법 (+ 새 프로젝트 시드 프레이밍)

이 논문은 **"lithiophobic(리튬 싫어하는) 층을 집전체에 얹으면 왜 Li가 *더 균일하게* 증착되나?"** 를 h-BN@Cu 계로 실험+DFT로 푼다. 직관과 반대다 — 보통 "Li를 좋아하는(lithiophilic) 층이 균일 증착을 돕는다"고 생각하는데, 여기선 **Li를 *약하게* 붙드는 h-BN이 오히려 균일 증착을 유도**한다. 핵심 메커니즘 통찰: **h-BN이 Li를 자기 *바깥* 표면(전해질 쪽)에서 밀어내고(exclusion), Li는 h-BN과 Cu *사이*(가장 강하게 붙는 자리, 흡착E −3.16 eV)로 파고들어 "h-BN–Li–Cu" 샌드위치로 평평하게 자란다.** h-BN은 전자절연·화학불활성이라 그 Li를 전해질에서 격리해 부반응·dendrite도 막는다.

> 🔋 **우리에게 왜 중요한가 (새 프로젝트 시드)**: 사용자는 **VGCF(흑연질 탄소) + h-BN + 그 둘의 double-layer 샌드위치**를 **ORCA**로 모델링해 **Li 흡착 차이(lithiophobicity)** 와 **Li 확산 차이**를 계산하려 한다. 이 논문이 바로 그 *방법 원형*이다 — 다만 (a) 그들은 **Cu + h-BN**, 우리는 **VGCF + h-BN**(집전체를 탄소로 교체), (b) 그들은 **주기 slab(VASP)**, 우리는 **분자/클러스터(ORCA)**, (c) 그들은 **확산 장벽을 계산 안 함**(우리 확산 계산 = *신규 확장*). 이 세 차이가 §10의 핵심.

> ⚠ **우리 argyrodite db와 절대 섞지 말 것**: 이 논문 수치(−2.50/−0.33/−3.16 eV 등)는 **Li-metal-anode/집전체 계면** 값. 우리 comp1/modelc(Li₆PS₅Cl) band gap·ESW·σ와 **물성축이 완전히 다르다**. §10에서 대조하는 건 *숫자*가 아니라 *방법*뿐.

## 1. 한 줄 요약
Cu 집전체에 **lithiophobic·전자절연·화학불활성 h-BN 분말층(300 nm 입자, 15 µm)** 을 슬러리 코팅하면, DFT상 Li가 h-BN 위(−0.33 eV, 약함)가 아니라 **h-BN과 Cu 사이(−3.16 eV, 최강)** 로 파고들어 **"h-BN–Li–Cu" 샌드위치**로 평평하게 증착 → dendrite·dead-Li 억제 → 대칭셀 **>500 h**(Cu는 250 h 단락), LFP full-cell **300cyc 73.3 % vs 33.3 %**. 핵심은 h-BN의 *기계강도가 아니라*(코팅 E=1.655 GPa ≪ Li 4.9 GPa) **lithiophobicity(약한 Li 결합)와 exclusion 효과**.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 계 | **h-BN@Cu** (Cu foil 8 µm + h-BN 코팅 15 µm) vs bare Cu |
| 음극 | Li 금속 (집전체 위 electrodeposition) |
| 양극(full-cell) | **LFP (LiFePO₄)** |
| 전해질 | **에터계**: 1 M LiTFSI in DOL:DME 1:1 v/v + **1.0 % LiNO₃**, 80 µL |
| 질문 | lithiophobic h-BN이 (a) Li 흡착·핵생성·확산을 어떻게 바꾸나, (b) 왜 균일 증착을 유도하나 |
| 갭 | 기존 h-BN 음극 연구는 전부 **"h-BN의 *기계강도*가 dendrite 억제"** 로만 설명(단원자층 Young's ~1.0 TPa). 이 논문은 코팅 h-BN이 **기계적으로 약한데도**(1.655 GPa) 효과가 있음을 보여 → **기계론이 아닌 *Li 수송·핵생성* 메커니즘**을 주장 |
| 방법 | 실험(wettability·in-situ optical·SEM·EDS·XPS·nanoindentation·scratch·EIS·CE·대칭셀·full-cell) + **DFT(VASP, 흡착E 3-모델 + charge density difference)** |

## 3. 핵심 물성 (수치 총정리)

### 3.1 ★ DFT 흡착에너지 (Fig 2c–e, S6) — 우리가 복제할 핵심 숫자
| 모델 | Li 흡착E ΔE | 의미 |
|---|---|---|
| **Li–Cu(111)** | **−2.50 eV** | Li on bare Cu 표면 (중간 결합) |
| **Li–h-BN(001)** | **−0.33 eV** | Li on h-BN 표면 (**약한 결합 = lithiophobicity 지표**) |
| **h-BN–Li–Cu(111)** (샌드위치) | **−3.16 eV** | Li가 h-BN과 Cu *사이*에 낀 자리 = **최강 결합 = 가장 안정 = 증착 모드** |

> 서열 **−3.16 < −2.50 < −0.33 eV**(더 음수 = 더 안정). 이 세 숫자의 *순서*가 논문 전체 DFT 논증의 전부다.
> **흡착E 정의식·Li 기준상태(원자 vs bulk metal)는 논문·SI에 명시 없음** → n/a (§10에서 우리 ORCA 재현 시 반드시 고정해야 할 항목).

### 3.2 실험 물성
| 물성 | 값 | 조건/출처 |
|---|---|---|
| 용융 Li on h-BN 접촉각 | **124°** (완전 비젖음) | Fig 1b, Video S1 (Li 250 °C 용융) |
| h-BN 코팅 탄성률 | **1.655 GPa** (평균; 1.739/1.089/2.293/1.366/1.789) | Table S2 nanoindentation. **≪ Li metal 4.9 GPa**, ≪ 단원자 h-BN Young's ~1.0 TPa |
| h-BN/Cu 접착강도 | **198.761 mN** (평균; 191.0/198.0/207.3) | Table S1 micron scratch |
| h-BN 입자 크기(최적) | **300 nm** (vs 50 nm, 1 µm) | Fig S11; 300 nm = 최적 stacking |
| h-BN 코팅 두께(최적) | **15 µm** (검토 6/8/15/19 µm) | Fig 3a, S12 |
| Cu foil 두께 | 8 µm | Fig S4, Exp. Section |
| **Nucleation overpotential** (0.5 mA/cm², 1 mAh/cm²) | Cu **73** / 6µm 94 / 8µm 90 / 15µm **73** / 19µm 73 mV | Fig 3l, S15 |
| CE (0.5 mA/cm², 1 mAh/cm²) | **15µm h-BN: >95 % / 240 cyc** (19µm: 200 cyc부터 하락) | Fig 3a |
| 대칭셀 수명 (0.25 mA/cm², 0.5 mAh/cm²) | Cu **~250 h 단락** / h-BN@Cu **>500 h**, 분극 **~10 mV** | Fig 3n |
| R_SEI (0.2 mA/cm², 1 mAh/cm²) | Cu 31.22→4.32→9.24 / **h-BN@Cu 29.35→8.81→9.17 Ω** (1st/30th/80th) | Table S3, Fig 3u,v |
| Full-cell 300cyc 유지 (1C, LFP) | Li–Cu \|LFP **50.48 mAh/g (33.31 %)** / **h-BN–Li–Cu \|LFP 106.62 mAh/g (73.32 %)** | Fig 5c |
| in-situ Li 층 두께 (1.5 mA/cm²) | Cu: 60 min **62.7 µm**(dendrite) / h-BN@Cu: 41.0→45.5→50.0→57.4 µm(0/10/20/40 min, 평평, Δ≈21.7 µm) | Fig 2a,b |

### 3.3 XPS (전자상태) — Fig 1g, S3
| 피크 | 값 | 해석 |
|---|---|---|
| **Li 1s** (Li 증착 후 h-BN@Cu) | **56.1 eV** | LiF형 *결합 상태*(≠금속 Li ~52.5 eV) → **h-BN *위*엔 금속 Li 핵생성 없음**(Li는 아래로 들어감) |
| B 1s | 190.23 → **190.46 eV** (증착 후) | h-BN 상 유지 |
| N 1s | 398.03 → **397.80 + 399.38 eV** (증착 후 신규 성분) | 399.38 = **N–Li 상호작용**(계면 전하이동의 XPS 증거) |

## 4. DFT/계산 방법 ★ (우리가 ORCA로 복제·확장할 부분)

> 방법 서술은 **SI "Theoretical calculations" 문단 + Fig 2 caption + Fig S6**에 전부 있음. 본문/SI를 글자 단위로 옮기면 아래.

- **code / version**: **VASP** (Vienna Ab-initio Simulation Package). 버전 명시 없음.
- **functional**: **GGA-PBE** (Perdew–Burke–Ernzerhof). **vdW/dispersion 보정 언급 없음** ← ⚠ Li-on-sp²(h-BN/graphene) 흡착에서 분산력은 중요한데 *안 씀*. 우리 ORCA에선 이걸 개선점으로(§10).
- **pseudo/PAW**: 명시 없음(VASP 기본 PAW로 추정, n/a).
- **k-points**: **Γ-centered, 해상도 2π × 0.04 Å⁻¹** (uniform mesh). 기하 최적화용.
- **smearing**: **Methfessel-Paxton** (금속 Cu 있으므로).
- **ecut (평면파)**: **500 eV** (throughout). "총에너지 1 meV/atom 수렴 보장".
- **수렴 기준**: 힘 **< 1 meV/Å**, 응력텐서 목표값 **0.01 GPa 이내**, 에너지 1 meV/atom.
- **supercell/nat**: 명시 없음. Fig S6/Fig 2 top-view로 보면 **h-BN(001) ~수 unit 셀 슈퍼셀 + Cu(111) 슬랩 몇 층**. 정확한 층수·진공두께·nat = n/a.
- **DFT+U**: 없음(전이금속 산화물 없음 — 불필요).
- **AIMD / MLIP**: **없음**.
- **NEB / 확산장벽**: **없음** ← ★★ 중요. 논문은 **흡착E와 CDD만** 계산. abstract·본문의 "reduce the deposition energy barrier / lower adsorption barrier" 표현은 *계산된 barrier가 아니라* **실험 nucleation overpotential**(Fig 3l,m)을 가리킴. **Li *확산* 장벽은 이 논문에 없다** → 우리 ORCA 확산 계산은 *논문 밖의 신규 기여*.
- **무질서 처리**: 해당 없음(Cu 금속 + 결정질 h-BN, SQS/enumerate 불필요).
- **계산 모델 3종** (Fig S6, Fig 2c–e):
  1. **Li–Cu(111)**: Cu(111) 슬랩 위 Li 원자 1개 흡착.
  2. **Li–h-BN(001)**: h-BN(001) 단층 위 Li 원자 1개 흡착.
  3. **h-BN–Li–Cu(111)** (샌드위치): Cu(111) 슬랩 위에 Li, 그 위를 h-BN(001) 단층이 덮음 → Li가 두 층 *사이*에 낌.
- **후처리**: **Charge Density Difference (CDD)** — Li on Cu(111) vs Li on h-BN@Cu(111) (Fig 2f,g, S6). 노랑 등치면 = 전하 획득(charge gain), 파랑 = 전하 손실(charge loss). N 원자가 Li로 전자를 내주는 걸 시각화.
- **원자 색 규약** (Fig 2 caption): Cu 파랑 / N 회색 / B 초록 / Li 주황. (좌 side-view, 우 top-view.)

> 🔑 **한 줄로 우리가 베낄 레시피**: *"VASP/PBE/500 eV/Γ 2π·0.04 Å⁻¹/MP-smearing 로 세 모델(surface-A/surface-B/A–Li–B 샌드위치)의 총에너지를 구해 흡착E 서열을 매기고, CDD로 전하이동을 시각화."* — 이걸 ORCA(클러스터·Gaussian 기저)로 옮기고 **확산 장벽을 추가**하는 것이 우리 프로젝트.

## 5. ★ "Double Lithiophobic Sandwich" 구조 — 정확한 구성

사용자 최우선 질문. 논문의 표현을 있는 그대로 해부한다.

### 5.1 두 lithiophobic 층이 정확히 뭔가
- **위층 (전해질 쪽, "outside")**: **h-BN 분말 코팅** (hexagonal boron nitride, 300 nm 나노시트, 15 µm). **lithiophobic**(용융 Li 접촉각 124°, Li 흡착 −0.33 eV로 약함) + **전자절연**(wide-gap 절연체) + **화학불활성**(chemical inertia).
- **아래층 (집전체, "current collector")**: **Cu foil** (8 µm). 논문은 Cu도 **lithiophobic**로 취급("h-BN is lithiophobic, just like Cu[38]"). 단 Cu의 Li 흡착E는 −2.50 eV(중간).
- **가운데 (증착 Li)**: 전기증착된 **Li 금속층**이 h-BN과 Cu *사이*에 형성 → **"h-BN–Li–Cu"** 샌드위치.

> **"double lithiophobic" = 두 lithiophobic 층(h-BN 위 + Cu 아래)이 Li를 위아래로 감싼다**는 뜻. Li는 샌드위치 *안(inside)* 에 갇히고, 바깥 h-BN 면은 평평하게 유지된다.

### 5.2 순서·두께·역할 (위→아래)
| 위치 | 물질 | 두께 | 역할 |
|---|---|---|---|
| 최상 (전해질 접촉) | **h-BN 코팅** | 15 µm (최적) | lithiophobic exclusion(Li를 위로 못 나오게)·전자절연(전해질과 Li 격리→부반응 차단)·물리장벽(dendrite 관통 차단)·Li⁺ 통로 제공(입자 간 gap + 결함) |
| 중간 | **증착 Li** | 용량 따라 (1·3·5 mAh/cm² 등) | 실제 활물질. h-BN–Cu 사이를 채우며 평평하게 성장 |
| 최하 | **Cu foil** | 8 µm | 집전체. Li와 중간 결합(−2.50 eV) |

### 5.3 실험적 증거 (샌드위치가 진짜 형성됨)
- **EDS 단면 line-sweep (Fig 1h–j)**: 1·3·5 mAh/cm² 모든 증착량에서 **B·N(위 h-BN) → Li(중간) → Cu(아래)** 순서 = "h-BN–Li–Cu" 확인. B·N이 Li층 안에도 조금 존재(Li가 h-BN 입자 사이 pore에도 일부 석출).
- **in-situ optical (Fig 2b)**: h-BN 표면은 40 min간 평평, 그 아래 **중간 Li층 두께만 41→57 µm 증가**(Δ≈21.7 µm) = Li가 아래에서 자람.
- **XPS Li 1s (Fig 1g)**: h-BN 위엔 금속 Li 없음(56.1 eV=LiF형) → Li가 위로 안 나옴.

### 5.4 DFT가 뒷받침하는 논리
Li가 셋 중 **가장 안정한 자리 = h-BN–Li–Cu 샌드위치(−3.16 eV)** 로 감. h-BN 위(−0.33 eV)는 너무 약해서(lithiophobic) Li가 안 앉음 → Li는 h-BN을 *뚫고 들어가* Cu와의 사이에 자리. **N→Li 전하이동**(CDD)이 샌드위치 결합을 −2.50(Cu만)보다 더 강하게 만듦.

> **우리 프로젝트 매핑**: 사용자의 "VGCF + h-BN double-layer 샌드위치"는 이 개념의 *탄소판*이다. 논문의 double = (h-BN + Cu). 우리 double = (h-BN + VGCF), 즉 **두 lithiophobic 층을 서로 다른 두 물질로 명시적으로 구현**. 그래서 우리가 계산할 것은 최소 3~4개: Li–VGCF / Li–h-BN / (h-BN–Li–VGCF 또는 VGCF–Li–h-BN) 샌드위치 / (필요 시 double-layer 적층). 흡착E 서열이 논문처럼 "샌드위치가 최강"으로 나오는지, VGCF가 Cu 역할을 하는지가 핵심 질문.

## 6. 결과 — 섹션별 상세 (모든 수치)

### 6.1 h-BN은 lithiophobic (Fig 1a,b)
용융 Li(250 °C)를 h-BN 코팅에 떨어뜨림 → **완전 비젖음**(Video S1), **접촉각 124°**. → h-BN은 Cu처럼 lithiophobic.

### 6.2 h-BN@Cu 제작·특성 (Fig 1c–j, S1–S10)
- 슬러리 코팅(PVDF 바인더). Cu 표면 은색→약간 변색(Li가 h-BN *아래* Cu 계면에 증착됨).
- h-BN 코팅 탄성률 **1.655 GPa** ≪ Li 4.9 GPa → **기계강도로 dendrite 막는 게 아님**(기존 연구와 결별점). 단원자 h-BN Young's ~1.0 TPa지만 분말코팅은 훨씬 약함.
- h-BN/Cu 접착 **198.5 mN**(약함) → h-BN–Cu 사이에 Li⁺ 증착 여지.
- **EDS line-sweep(Fig 1h–j)**: 1/3/5 mAh/cm² 전부 "h-BN–Li–Cu". N > B(SEI 내 N 잔류). Li층 내 B·N = h-BN pore 내 부분 석출.
- h-BN 순도: XRD PDF#34-0421, Raman 1366 cm⁻¹, TEM (100) 0.21 nm(Fig S8–S10).

### 6.3 in-situ 광학 증착 관찰 (Fig 2a,b), 1.5 mA/cm²
- **bare Cu**: 10 min 미세입자 → 20 min 크기 불균일 bump → protrusion 주변 우선 핵생성 → dendrite 핵생성·성장 → 40 min 무질서한 구형 덩어리 → **60 min d=62.7 µm**(거침).
- **h-BN@Cu**: 첫 40 min 표면 변화 없음. **중간 Li층 41.0→45.5→50.0→57.4 µm**(0/10/20/40 min), Δ≈21.7 µm. h-BN 표면 평평 유지 → Li가 균일하게 아래로. → "h-BN–Li–Cu" 샌드위치 실시간 확인.

### 6.4 DFT 흡착E·CDD (Fig 2c–g, S6) — §3.1, §4 참조
Li–Cu(111) −2.50 / Li–h-BN −0.33 / **h-BN–Li–Cu(111) −3.16 eV**. CDD: h-BN@Cu 계면이 bare Cu보다 Li와 전하이동 강함. **N이 Li로 전자 내줌** → 계면 흡착E 강화.

### 6.5 CE·입자크기·두께 최적화 (Fig 3a, S11, S12)
- **15 µm h-BN: CE >95 %, 240 cyc** (0.5 mA/cm², 1 mAh/cm²). 19 µm는 200 cyc부터 95 %→하락.
- 입자 크기: **300 nm 최적**(0.5·1.0 mA/cm²). 큰 입자(1 µm)=stacking 밀도↑→Li⁺ migration 저항↑; 작은 입자(50 nm)=안정 stacking 불가.
- 두께 **15 µm** 채택.

### 6.6 Nucleation overpotential (Fig 3l,m, S15, S16) — ⚠ 효과가 *미묘*
- **두께 의존(Fig 3l, S15, 0.5 mA/cm²)**: Cu 73 / 6µm 94 / 8µm 90 / **15µm 73** / 19µm 73 mV. → h-BN 두께 무관하게 **bare Cu와 비슷**(gap·결함이 Li⁺ 통로라 큰 장벽 없음). 15µm가 h-BN 중 최저.
- **전류밀도 의존(Fig 3m, S16, 15µm)** [Cu / h-BN@Cu] mV:
  | j (mA/cm²) | 0.5 | 0.8 | 1.0 | 1.2 | 1.4 | 2.0 | 2.4 | 3.0 |
  |---|---|---|---|---|---|---|---|---|
  | Cu | 73 | 89 | 80 | 84 | 107 | 105 | 100 | 103 |
  | h-BN@Cu | 73 | 77 | 76 | **98** | 107 | **190** | 104 | 110 |
- 본문 주장: "0.5–1.4 mA/cm²서 h-BN이 overpotential *낮춤*, 고전류선 *안 됨*(Li⁺ flux↑ → lithiophobic exclusion↑ → h-BN 통과 방해)".
- 🔑 **critical**: 데이터는 *섞여* 있다 — 0.8·1.0선 낮지만 1.2·2.0선 **오히려 높다**. **즉 h-BN의 이점은 "핵생성 과전압을 크게 낮춤"이 아니다.** overpotential은 bare Cu와 비슷하거나 고전류선 나쁨. **진짜 이점은 *공간적 균일성*(어디에 증착되나) + 전자·화학 격리**이지, 열역학적 핵생성 우위가 아니다.

### 6.7 대칭셀·EIS (Fig 3n, u,v, S17, S18, Table S3)
- **대칭셀(0.25 mA/cm², 0.5 mAh/cm²)**: Cu 100 h부터 분극 상승, **~250 h 급상승→단락**. h-BN@Cu **>500 h, 분극 ~10 mV**.
- **EIS(0.2 mA/cm², 1 mAh/cm²)**: 두 반원(고주파=SEI 내 Li⁺ 확산, 저주파=전하이동). 등가회로 R0-[R_SEI/C_SEI]-[R_ct/C_dl-W](Fig S17). R_SEI: **h-BN@Cu 29.35→8.81→9.17 Ω(안정)**, Cu 31.22→4.32→9.24(변동 큼). → h-BN이 계면 안정화.

### 6.8 사이클 후 형태 (Fig 3o–t, S13, S14, S19–S21)
- **Cu**: 1.0 mAh/cm² 증착 후 smooth-edge dendrite(3o); 36 cyc 후 dendrite 미세밴드 "dead Li"로 파쇄(3q); 100 cyc 후 dead Li+dendrite 다수(S13a,b).
- **h-BN@Cu**: 전 과정 평평(3r–t); h-BN 벗겨낸 Cu는 원상태 유지·dead Li 거의 없음(S13c,d). 1–8 mAh/cm² 평평·치밀(S19). 10 mAh/cm²선 h-BN도 일부 dendrite지만 Cu보다 훨씬 적음(S20, S21).

### 6.9 Full-cell (Fig 5, LFP)
- 음극 = **1.5 mAh/cm² Li 예비증착한 (h-BN@)Cu**, 양극 = LFP, 2.4–4.2 V.
- CV(5b) 0.1/0.3/0.5 mV/s.
- **1C 300 cyc**: Li–Cu\|LFP **50.48 mAh/g(33.31 %)** vs **h-BN–Li–Cu\|LFP 106.62 mAh/g(73.32 %)** — 2배 이상 유지율.
- rate(5j) 0.1→5C: h-BN 우수(특히 5C).
- SEM 110 cyc(5d–g): Cu=dead Li+dendrite 얽힘; h-BN@Cu=평평, 원 h-BN이 덮음.

## 7. ★ Lithiophobic 메커니즘 — 왜 약한 Li 결합이 균일 증착을 유도하나

사용자 질문 #3. 논문이 제시하는 논리(Fig 4 도식) + 비판적 평가.

### 7.1 논문의 메커니즘 (3+1 요소)
1. **Exclusion(배제) → surface tension → 균일 핵생성**: h-BN이 lithiophobic(약한 −0.33 eV)이라 Li를 자기 위에 못 앉힘 → Li 핵생성·성장의 *표면장력을 높임* → Li가 뭉쳐 cluster로 자라는 걸 막고 **균일하게 흩뿌려 핵생성**. (bare Cu는 protrusion 끝 "tip effect"로 국소 강전기장→dendrite; Fig 4a.)
2. **샌드위치 우선 증착(−3.16 eV) + 전하이동**: 가장 안정한 자리가 h-BN–Li–Cu 사이 → Li가 **h-BN *아래*로 파고들어** 평평한 seed layer 형성 → 그 위 균일 성장(Fig 4b). N→Li 전하이동이 이 자리를 특히 안정화.
3. **전자절연 격리 + 물리장벽**: h-BN은 전자절연·화학불활성 → 증착 Li를 전해질에서 **격리**(부반응·SEI 계속파괴 억제) + **dendrite가 h-BN 뚫고 분리막 도달하는 걸 물리적으로 차단**(단락 방지).
4. **Li⁺ 통로 2종**(Fig 4b inset): channel 1 = h-BN 입자 *사이* gap, channel 2 = h-BN 결정 *결함*. → h-BN이 절연이라 e⁻는 못 지나지만 Li⁺는 이 통로로 통과 → 아래 Cu 계면서 환원·증착.

### 7.2 비판적 평가 (over-claim 걸러내기)
- ✅ **탄탄한 부분**: (a) 샌드위치 흡착E 서열(−3.16<−2.50<−0.33)은 명확하고 EDS·in-situ·XPS가 "Li가 아래에 형성"을 독립 확인. (b) 전자절연 h-BN이 Li를 전해질에서 격리 = 물리적으로 합당하고 EIS R_SEI 안정성이 뒷받침. (c) "기계강도 아님"(1.655 GPa)은 정량 근거로 잘 반박됨.
- ⚠ **약한/미묘한 부분**:
  - "lithiophobic → 균일" 논리(요소 1)는 **정성적**. surface-tension 논변은 손으로 그린 것이고, DFT는 "샌드위치가 안정"만 증명하지 "균일"을 직접 증명 안 함. 균일성의 실제 증거는 *전부 실험*(in-situ/SEM).
  - **nucleation overpotential은 거의 안 낮아진다**(§6.6) — 심지어 고전류선 나쁨. 즉 "약한 결합이 *핵생성 장벽을 낮춰* 균일화"는 **아니다**. 이점은 열역학 핵생성이 아니라 *공간 균일성 + 격리*.
  - abstract의 **"reduce deposition energy barrier"** 는 오해 소지 — *계산된 확산 장벽 없음*. 실험 overpotential을 말한 것. → 우리 프로젝트가 진짜 확산 장벽을 계산하면 이 공백을 메움.
  - "Cu도 lithiophobic"인데 흡착E는 −2.50 eV(강함) — **거시적 lithiophobicity(젖음/접촉각)와 원자 흡착E를 혼용**. Cu는 용융 Li가 안 젖지만 Li 원자는 잘 붙는다. 논문은 서사에 유리한 쪽을 골라 씀. (§13 주의.)

## 8. Figure set ★

### 8.1 본문 Figure
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | 용융 Li on h-BN 접촉각 124° 비젖음 | lithiophobicity 거시 증거 |
| 1c–f | bare Cu vs h-BN@Cu 광학(증착 전후) | — |
| 1g | **XPS Li 1s 56.1 eV(LiF형, 금속Li 없음)** | h-BN 위 Li 무핵생성 증거 |
| 1h–j | **EDS 단면 line-sweep(1/3/5 mAh/cm²) → h-BN–Li–Cu** | 샌드위치 구조 직접 증거 |
| 2a,b | **in-situ 광학**: Cu dendrite(62.7µm) vs h-BN@Cu 평평(중간층 41→57µm) | 균일 증착 실시간 |
| **2c** | **Li–Cu(111) ΔE=−2.50 eV** (side+top view) | ★ 우리 복제 대상 |
| **2d** | **Li–h-BN ΔE=−0.33 eV** | ★ lithiophobicity 수치 |
| **2e** | **h-BN–Li–Cu(111) ΔE=−3.16 eV** (샌드위치 최안정) | ★ 샌드위치 모드 근거 |
| **2f,g** | **CDD** Li on Cu(111) / h-BN@Cu(111) (노랑=획득/파랑=손실) | ★ 전하이동 시각화 방법 |
| 3a | CE vs h-BN 두께(6/8/15/19µm), 15µm >95%/240cyc | 두께 최적화 |
| 3l,m | **nucleation overpotential** vs 두께/전류밀도 | ⚠ 효과 미묘(§6.6) |
| 3n | **대칭셀** Cu 250h 단락 vs h-BN@Cu >500h/10mV | 수명 |
| 3o–t | 사이클 후 형태(Cu dendrite/dead-Li vs h-BN 평평) | dendrite 억제 |
| 3u,v | EIS R_SEI 안정성 | 계면 안정 |
| 4a,b | **메커니즘 도식** (Cu tip-effect vs h-BN 균일+채널) | 메커니즘 프레이밍 |
| 5a–j | full-cell(LFP): 300cyc 73.3% vs 33.3% | 실셀 성능 |

### 8.2 SI Figure/Table
| Fig/Table | 내용 | 활용 |
|---|---|---|
| **Theoretical calc. 문단** | **VASP/PBE/500 eV/Γ 2π·0.04 Å⁻¹/MP-smearing/힘<1meV·Å** | ★ DFT 레시피 원문(§4) |
| **S6** | **Li on Cu(111) / h-BN@Cu(111) charge density**(side+top) | ★ 흡착 모델 구조·CDD |
| S1 | Cu·h-BN@Cu SEM | — |
| S2 | B EDS 균일 분포 | — |
| S3 | **XPS B1s(190.23→190.46)·N1s(398.03→397.80+399.38)** | N–Li 전하이동 XPS |
| S4 | 단면 SEM (Cu 8µm / h-BN@Cu 25µm) | — |
| S5, **Table S1** | scratch, **접착 198.761 mN** | 약한 접착 |
| **Table S2** | **nanoindentation E=1.655 GPa** | ★ 기계론 반박 |
| S7,S8 | h-BN 50/300nm/1µm SEM·TEM((100) 0.21nm) | 입자 크기 |
| S9,S10 | XRD PDF#34-0421 / Raman 1366 cm⁻¹ | h-BN 순도 |
| S11 | CE 입자크기(50/300nm/1µm) | 300nm 최적 |
| S12 | 두께 SEM(6/8/15/19µm) | — |
| S13,S14 | 100cyc 후 SEM+EDS | dead-Li 대비 |
| S15,S16 | **overpotential 두께/전류밀도 상세**(73–190 mV) | ⚠ 데이터 원본(§6.6) |
| S17,**Table S3** | 등가회로 + **R_SEI 수치** | EIS 정량 |
| S18 | voltage profile(120cyc) | — |
| S19–S21 | 고용량(8/10 mAh/cm²) 증착·stripping | 고부하 한계 |

## 9. Post-processing ★
- **DFT 흡착E**: 3-모델 총에너지 차 → ΔE 서열. (정의식·Li 기준상태 미공개.)
- **CDD (charge density difference)**: `Δρ = ρ(Li+substrate) − ρ(substrate) − ρ(Li)` 형태로 추정(논문 식 미제시). VASP 전하밀도 차분 → 등치면 렌더(노랑 획득/파랑 손실). N→Li 전자이동 시각화. **도구 = VASP + 시각화(VESTA류 추정, 명시 없음)**.
- **실험 후처리**: nucleation overpotential(voltage dip 최저점−plateau), CE(strip/plate 용량비), EIS(등가회로 fitting → R_SEI), in-situ 광학(층두께 정량), EDS line-sweep(원소 깊이분포), XPS(BE→화학상태).
> 우리 적용: **흡착E 서열 + CDD**가 우리 ORCA 프로젝트의 *정확히* 재현 대상. 여기에 **확산 장벽(NEB/scan)** 을 우리가 추가.

## 10. ★★ 우리 DFT/ORCA 대비 + 복제 계획 → `../our_dft_baseline.md`

### 10.1 물성 대조 — *다른 축이라 수치 비교 없음*
| 항목 | 이 논문 | 우리 baseline (comp1/modelc) | 관계 |
|---|---|---|---|
| 재료계 | Li-metal 음극 / Cu 집전체 / h-BN 코팅 | 황화물 SE Li₆PS₅Cl (양극·벌크) | **완전 다른 축** — 직접 물성 비교 n/a |
| 대표 계산량 | **Li 흡착E**(−2.50/−0.33/−3.16 eV) | band gap 2.07/ESW onset 2.256 V/Ea 0.22–0.25/elastic | **겹치는 물성 없음** |
| code/functional | VASP / PBE / (vdW 없음) | QE(대부분)·VASP / PBE·PBEsol·D3 | functional 계열 동일(PBE), 우리가 D3 씀 |
| 무질서 | 없음(Cu·h-BN 결정) | SQS/enumerate(argyrodite) | 해당 없음 |
| **전이되는 것** | **흡착E = 총에너지 차 + CDD 전하이동** 방법 | 우리 W_ad/adhesion·계면 흡착 방법과 *같은 과(科)* | **✓ 방법만 전이** (§10.2) |

> 즉 §7-표는 "**숫자 대조가 아니라 방법 대조**"다. 우리 argyrodite 산화·이온전도·기계 축과 이 논문은 물성이 안 겹친다. 겹치는 건 **"표면 위/사이 원자 흡착E를 총에너지 차로 뽑고 CDD로 전하이동 본다"** 는 계산 *기술*.

### 10.2 ORCA 복제 계획 (우리 VGCF + h-BN 프로젝트) — 실무 체크리스트
논문(VASP 주기 slab)을 **ORCA(분자·클러스터·Gaussian 기저)** 로 옮길 때 반드시 정할 것:

1. **모델 형태 = slab → cluster 전환** ★ 최대 이슈. ORCA는 기본이 *분자* 코드. 세 방법:
   - (a) **유한 클러스터/flake**: VGCF=유한 graphene/coronene류 조각(가장자리 H-종단), h-BN=유한 BN flake. Li 1개 흡착. 가장자리 효과 주의(충분히 크게).
   - (b) ORCA 주기(제한적) — 권장 안 함(성숙도·비용).
   - → **cluster 권장**. 논문의 slab 절대 흡착E와 직접 등치 금지(모델계 다름) — 우리도 **세 모델 *내부* 서열**만 본다(논문과 같은 논리).
2. **흡착E 정의식·Li 기준상태 고정** ★ 논문이 안 밝혔으니 우리가 명시:
   - `E_ads = E(Li+substrate) − E(substrate) − E(Li_ref)`.
   - **Li_ref 선택**(원자 Li vs bulk-Li 원자당 vs Li⁺+e⁻)이 절대값을 크게 바꿈. → 세 모델 모두 *같은 기준*으로 계산해 서열만 비교. 리포트에 기준 명기.
3. **분산 보정(vdW)**: 논문은 *안 씀*. 하지만 **Li on sp²(graphene/h-BN)은 분산이 중요** → 우리는 **D3(BJ) 또는 D4를 켜는 걸 권장**(개선점). 단 "논문 대비 절대값 차이"는 이 vdW 차이 탓일 수 있음을 명시.
4. **functional/기저**: 논문 PBE. ORCA 재현이면 PBE+D3 + def2-TZVP(Cu/전이금속은 def2 ECP 또는 all-electron), 필요 시 RIJCOSX 가속. 벤치마크로 r²SCAN-3c(우리 desktop ORCA 관례, CLAUDE.md)도 가능.
5. **집전체 교체 Cu → VGCF**: ★ 물리 다름. Cu는 금속(자유전자), VGCF는 흑연질(반금속·π). **graphene basal plane의 Li 흡착은 pristine면 약함**(논문 h-BN −0.33과 비슷한 결); 결함·edge·다층 stacking(AB)이 Li 결합을 크게 바꿈. → VGCF 모델의 *결함/가장자리/층수*를 명시적으로 다뤄야(단순 완전 basal면은 Cu의 −2.50 역할을 못 할 수 있음). 이게 우리 프로젝트의 *과학적 질문*(VGCF가 샌드위치서 Cu 역할을 하나?).
6. **★ 확산(diffusion) = 신규 확장**: 논문에 없음. ORCA로:
   - **NEB**(ORCA `NEB-TS`/`NEB-CI`)로 Li가 표면 위/샌드위치 안에서 hop하는 장벽, 또는 **relaxed PES scan**(Li 위치 고정 스캔).
   - "VGCF vs h-BN vs 샌드위치서 Li 확산 장벽 차이" = 우리 고유 결과. 논문의 "barrier"(실험 overpotential)와 혼동 금지 — 우리 건 *계산된 마이그레이션 장벽*.
7. **CDD 재현**: ORCA에서 밀도 차(`Δρ`) 출력 → 우리 house-style 렌더. N→Li(또는 C→Li) 전하이동 확인. Löwdin/Hirshfeld/CHELPG 전하로 정량 보강 가능(논문은 정성 CDD만).
8. **검증 앵커**: 논문 세 숫자(−2.50/−0.33/−3.16)를 *같은 VASP-slab 세팅*으로 우리가 한 번 재현해 보면(가능하면) ORCA-cluster ↔ VASP-slab 간 *서열 일치*를 확인하는 sanity check가 됨.

### 10.3 우리 그룹 내부 연결 (개념 다리, 수치 아님)
- **VGCF 공유**: 우리 그룹 [KimCA](`kim2025_conductive_agent_se_coating_cathode.md`)가 **1D VGCF**를 SE-코팅 도전재로 씀(0D Super P보다 우수). 이번 새 원자단위 프로젝트가 *같은 VGCF*를 다룸 → 복합전극 거시 실험(KimCA)과 원자 흡착/확산(신규)의 **물질적 연결고리**. 단 물성·스케일 달라 수치 이식 금지.
- **흡착E/W_ad 방법 계보**: 우리 UMA W_ad·adhesion 계산, [Choi2025](`choi2025_mlip_cu_taxn_interfacial_adhesion.md`) MLIP 계면접착과 **총에너지 차 기반 계면E**라는 점에서 동과. 이번 ORCA 흡착E도 같은 철학(단 MLIP 아닌 DFT, cluster).

## 11. 적용 인사이트 (우리 새 프로젝트에)
1. **복제 최소단위 확정**: 세 모델(Li–VGCF / Li–h-BN / 샌드위치) 흡착E 서열 + CDD가 논문 재현의 코어. 논문 레시피(PBE/500 eV/Γ 2π·0.04)를 *slab*이면 그대로, *ORCA cluster*면 §10.2 전환 규칙으로.
2. **lithiophobicity 지표 = 약한 흡착E(−0.33 eV급)**. h-BN이 이 값이면 "lithiophobic 확인". VGCF도 basal면이 비슷하게 약하면 "이중 lithiophobic" 개념이 성립.
3. **샌드위치가 최강이어야 서사 성립**: 우리 결과에서 (h-BN–Li–VGCF) 흡착E가 단일 표면들보다 더 음수여야 "샌드위치 증착 모드"가 재현됨. 안 그러면 논문과 다른 물리 — 그 자체가 발견.
4. **확산이 우리 차별화**: 논문은 흡착만, 우리는 **확산 장벽**까지 → "lithiophobic 표면이 Li 확산을 어떻게 바꾸나(균일화의 kinetic 근거)"를 논문이 못 준 걸 우리가 제공. abstract의 "barrier 낮춘다"를 *진짜 계산*으로 검증/반증.
5. **vdW·Li기준·cluster-edge**를 리포트에 못박기 — 이 세 개가 흡착E 절대값을 흔드는 method-artifact. 논문과의 절대값 차이를 "물리 차이"로 오해 금지.
6. **기계론 배제 승계**: 논문의 "1.655 GPa인데도 효과 = 기계 아님"을 우리도 프레이밍에 활용(우리 계산은 전자·흡착·확산 = 논문 서사와 정합).

## 12. 인용 가능 문장 (deck/paper용)
- "Liu et al. (Adv. Mater. Interfaces 2022) computed Li adsorption energies of −2.50 eV (Cu(111)), −0.33 eV (h-BN(001)) and −3.16 eV (h-BN–Li–Cu(111) sandwich) with VASP/PBE, establishing that Li is thermodynamically driven *between* the lithiophobic h-BN and Cu rather than onto the h-BN surface."
- "The weak Li–h-BN binding (−0.33 eV) is the atomistic signature of lithiophobicity; the strongest binding in the sandwich site (−3.16 eV), aided by N→Li charge transfer, rationalizes the observed 'h-BN–Li–Cu' deposition mode."
- "Notably the h-BN coating is mechanically soft (1.655 GPa ≪ Li 4.9 GPa), so the benefit is not mechanical dendrite suppression but lithiophobic exclusion + electronic/chemical isolation — a Li-transport/nucleation mechanism."
- "We reuse this adsorption-energy + charge-density-difference protocol in ORCA for VGCF + h-BN, and extend it with an explicit Li migration-barrier calculation that the original study did not perform."

## 13. 주의/한계 (over-claim 방지)
- **다른 축**: Li-metal-anode/집전체 논문. 우리 argyrodite 산화·σ·기계·gap과 **수치 비교 금지**. 전이는 *방법*뿐.
- **흡착E 정의식·Li 기준상태 미공개** → 논문 절대값(−2.50/−0.33/−3.16)을 우리 값과 등치 금지. *서열*만 의미.
- **vdW 미사용**: Li-on-sp² 흡착에서 분산 누락 = 절대 흡착E 신뢰도 제한. 우리 D3/D4 결과와 절대값 차이는 이 탓일 수 있음.
- **확산 장벽 없음**: abstract "reduce deposition energy barrier"는 *실험 overpotential*이지 계산 값 아님. 확산은 미계산.
- **nucleation overpotential 효과 미묘/혼재**(§6.6): h-BN이 과전압을 크게 낮추지 않고 고전류선 오히려 높임. "약한 결합→핵생성 장벽↓→균일" 서사는 데이터가 완전히 지지하진 않음. 이점의 실체 = 공간 균일성 + 격리.
- **"Cu도 lithiophobic" 혼용**: 거시 젖음(접촉각) ≠ 원자 흡착E(−2.50 eV, 강함). 서사 편의적 사용.
- **모델 정보 부족**: 슬랩 층수·진공·nat·흡착 site(top/hollow/bridge)·h-BN–Cu 계면 정합성 미공개 → 정확 재현엔 우리 판단 필요.
- **VGCF≠Cu**: 우리 프로젝트는 집전체를 탄소로 바꿈 → basal graphene의 약한 Li 흡착이 Cu의 −2.50 역할을 못 할 수 있음. 결함/edge/층수 처리가 결과를 좌우(우리 과학적 질문).
- **full-cell 조건 관대**: 예비증착 Li 1.5 mAh/cm²(과잉), 에터계+LiNO₃(LFP엔 우호적), LFP 저전압. 고-Ni·고전압·저 N/P로의 일반화 주의.

## 14. 기법 용어 미니사전
- **Lithiophobic / lithiophilic**: Li를 싫어함(약한 결합·큰 접촉각) / 좋아함(강한 결합·작은 접촉각). 이 논문의 반직관 = **lithiophobic이 균일 증착 유도**.
- **Nucleation overpotential(핵생성 과전압)**: Li 증착 초기 voltage dip(최저점)과 이후 plateau의 차 = 핵생성에 드는 여분 전압. 낮을수록 핵생성 쉬움.
- **흡착에너지(adsorption/binding energy)**: `E(전체) − E(기판) − E(흡착종)`. 음수 클수록 안정. 이 논문 DFT의 주 관측량.
- **CDD (charge density difference)**: `ρ(전체) − ρ(기판) − ρ(흡착종)`. 결합 시 전자 재배치 시각화(획득/손실). N→Li 전하이동 증명에 사용.
- **h-BN (hexagonal boron nitride)**: graphene 유사 2D BN. 절연(wide-gap)·화학불활성·기계강함(단원자). 여기선 분말코팅이라 기계적으론 약함.
- **VGCF (vapor-grown carbon fiber)**: 기상성장 흑연질 탄소섬유(1D). 우리 프로젝트의 집전체/도전 상 — 논문 Cu를 대체.
- **Dead Li**: 전기적으로 단절된 비활성 Li(dendrite 파쇄/SEI 매몰) → 용량 손실·CE 저하.
- **Sandwich deposition mode ("h-BN–Li–Cu")**: Li가 두 lithiophobic 층 사이에 갇혀 평평하게 자라는 증착 양식(이 논문 핵심).
- **NEB (nudged elastic band)**: 확산 장벽(전이상태 에너지) 계산법. **논문엔 없음** — 우리 확산 확장에 쓸 도구.
