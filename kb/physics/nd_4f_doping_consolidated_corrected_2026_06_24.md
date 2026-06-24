# Nd / 란탄족 4f 도핑 — 통합·교정 노트 (March 개념노트 + June DFT/MP 결합)

> 작성 2026-06-24. **통합 대상**: `260318_Nd_4f_국소화_문제와_DFT_Band_Gap_한계`, `260320_란탄족_4f_Ce_Nd_도핑_COHP_ELF_EXAFS`(사용자 제공 개념노트).
> **결합 대상(June 실측/계산)**: `kb/results/nd2o3_master_findings_2026_06_18.md`, `kb/results/nd2o3_O_effect_transfer_2026_06_24.md`, `kb/methodology/nd_vs_O_isolation_campaign_2026_06_18.md`, `db/properties/{electronic,nd_icohp}.json`, MP(`tools/oxidation/{oxophilicity_descriptor,sei_product_gaps}.py`).
> **목적**: March 노트의 4f 물리는 대체로 옳음 → **그대로 유지(§2)** + **틀리거나 outdated된 부분 교정(§1)** + **MP/June 데이터·figure와 결합(§5)**.

---

## 0. 한 줄
March 노트의 핵심 물리(4f 국소화·차폐·spectator, Mott-Hubbard vs band insulator, partial-occupation 규칙, Ce⁴⁺ vs Nd³⁺ capping/blocking, NdS₄ 불가, band gap≠formation energy)는 **옳다**. 단 **7건 교정** 필요(§1) — 가장 중요: ① **U=3.1→8 eV**(production), ② **O가 PS₄(16e)에 실제 치환됨 검증**, ③ **P–O 강결합 COHP로 정량 확인(−8.43)**, ④ **Nd는 특별한 O-getter 아님 → 도핑 이점의 주역은 O**, ⑤ **ELF는 결합(P–S/P–O) 분석엔 사용 가능**(노트의 "ELF 전면 불가"는 과함, on-Nd 4f에만 해당).

---

## 1. ⚠️ 교정 로그 (March 노트 → June 실측/계산) — **이 노트의 핵심**

| # | March 노트 주장 | 교정 / 현재 사실 | 근거 |
|---|---|---|---|
| **C1** | **U = 3.1 eV** (Nd 4f), "U=3.1로는 on-site(5–8) 부족" | production Nd₂O₃-doped 계산은 **U = 8 eV** 사용(5–8 범위 안). "U 부족" 비판은 해소. (단 doped host gap은 여전히 좁아짐 = 별개 원인, C7) | `electronic.json` → `eigenvalue_gaps_v100`.Nd2O3_doped (`U=8 eV, nspin2 AFM`) |
| **C2** | "O의 site preference(16e vs 4a/4c) **미확인** → DFT 확인 필수 (PS₄ 강화 주장 전제)" | **확인됨**: relaxed 120-atom 셀 = **1×PS₂O₂ + 1×PS₃O + 8×pristine PS₄**. O가 PS₄ 코너 S(16e)를 부분 치환 → "PS₄ 강화" 전제 충족 | `electronic.json` Nd_narrowing_mechanism ("O speciation VERIFIED") |
| **C3** | "P–O가 P–S보다 강할 것(가설)" — antibonding 고에너지 이동 | **정량 확인**: **ICOHP P–O −8.43 vs P–S −5.98 eV/bond (+41%)**, d 1.571 vs 2.064 Å, ELF P–O 0.838(강·polar 공유). COHP/ELF figure로 시각화됨 | `nd_icohp.json`; `docs/figures/icohp/nd_COHP_4panel.png`(P–O 패널); `docs/figures/nd_elf/nd_ELF_PS2O2*.png` |
| **C4** | "Nd₂O₃ 도핑" 이점 서술이 Nd 기여처럼 읽힘 | **Nd는 특별한 O-getter 아님**: MP oxophilicity **Nd 1.75 ≈ Li 1.67**(Al 3.45, Y 2.13). 결합도 약·이온(ICOHP Nd–X −0.4~−0.6). → **이점의 주역은 O**(P–O 강결합 + O-유래 wide-gap 상). Nd = O 운반·cathode 앵커·aliovalent | `nd2o3_O_effect_transfer_2026_06_24.md`; `nd_vs_O_isolation_campaign` |
| **C5** | SEI gap 값 혼재(Li₃PO₄ 5.63 vs 8; Li₃P 0.9 vs 1.54) | **MP 표준값으로 통일**: LiCl 6.65 · Li₃PO₄ **5.73** · NdPO₄ 5.55* · Li₂O **5.24** · NdCl₃ 4.30* · Li₂S 3.90 · Li₃P **0.70** · NdS 0.00 (*=Nd 4f MP 하한, 실제 더 넓음) | `sei_product_gaps.py`(MP); `docs/figures/nd_sei/sei_product_gaps_O.png` |
| **C6** | "**ELF는 Nd 화합물에 부적합**(떡짐, spectator, PBE 왜곡)" — 전면 불가로 읽힘 | **결합 분석엔 사용 가능**: P–S(0.870)·P–O(0.838)·S lone pair·Nd–X 이온 floor(0.13–0.19) 다 정상 추출(=June ELF-on-PS₄-plane 그림이 증거). **불가한 건 on-Nd 4f 원자영역(아티팩트/blob)뿐** → 4f 자체는 **spin density**(plot_num=6) | `nd_elf_bond_quant.csv`; `docs/figures/nd_elf/{nd,modelc}_ELF_PS4plane.png` (Nd/Li 코어에 speckle 아티팩트 = 노트가 경고한 그 영역) |
| **C7** | (Nd compound) "PBE+U가 band gap 실패" 만 강조 | **두 가지를 구분**: (a) **Nd 화합물 gap**(NdCl₃/NdOCl/LiNdO₂) = 4f Mott 실패 → **문헌값 사용**(노트의 옳은 결론). (b) **Nd-도핑 host(LPSCl) gap** = 2.184→1.632(**−0.55**), **Nd 5d가 CBM 끌어내림**(4f-in-gap 금속 아님; host는 clean N(E_F)=0). 둘을 섞지 말 것 | `electronic.json` Nd_narrowing_mechanism |
| (minor) | §3-5 충전순서 "…6s²→**4f⁴**" | 그건 **중성 Nd([Xe]4f⁴6s²)**. **Nd³⁺ = 4f³**(노트 다른 곳은 4f³로 맞음). 이온/중성 혼동 주의 | — |

> **유지(옳음, 교정 불필요)**: 4f 국소화·5s5p 차폐·spectator, Mott vs band insulator, SIE/static-correlation/Δxc, formation E의 오차상쇄, partial-occupation 규칙(closed d¹⁰ OK / open f^n 실패), Ce⁴⁺ vs Nd³⁺(capping/소모 vs blocking/영구), 마법수 0/7/14, **NdS₄ 불가**(아래 §2-6, MgS₄ 비판과 동일 논리), 이온반경 서열.

---

## 2. 검증된 4f 물리 (March 노트 요약 — 그대로 유지)

### 2-1. 4f 궤도 = 국소화된 spectator
핵 가까이 수축(contracted) → **5s,5p가 바깥에서 차폐** → 이웃 원자와 overlap ≈0 → **화학결합 미참여**(Nd–Cl/Nd–O 결합은 5d/6s가 담당). 4f 반발(원자 내부)과 결합(원자 간)은 **독립**. → DFT+U를 4f에만 걸어도 결합은 안 망가짐(정당성).

### 2-2. PBE 실패 메커니즘 (왜 Nd 화합물이 가짜 metal)
- **SIE**(자기상호작용): 국소 4f에서 큼 → 채워진 4f를 E_F 근처로 띄움 → 가짜 DOS가 gap 침범 → 프로그램이 "metal" 오판.
- **Static correlation**: 단일 Slater determinant가 4f multi-reference 못 봄.
- **Δxc=0**: KS gap = fundamental gap − Δxc → 체계적 과소.
- → Nd³⁺(4f³ open shell)에서 폭발 = **Mott-Hubbard insulator를 metal로**.
- **formation E는 OK**: total-E 차이라 reactant/product 4f 오차 상쇄(단 산화수 크게 변하면 상쇄 깨짐 → DFT+U 필요).

### 2-3. partial occupation 규칙 (DFT 신뢰도 사전판정)
| 배치 | 예 | PBE |
|---|---|---|
| s²p⁶ closed | Li⁺,Cl⁻,O²⁻ | ✅ |
| d¹⁰ closed | Sb³⁺,Zn²⁺ | ✅ (d 묻힘, spectator) |
| 3d open (d⁶ 등) | Fe²⁺ | ⚠️ +U |
| **4f open (f³)** | **Nd³⁺** | ❌ +U로도 부족 |
> 규칙: **빈자리 있는 d/f = 위험**. LPSCl(host)·Li₂S·Li₂O·Li₃PO₄(s,p)는 PBE OK(과소만), Nd 화합물은 문헌 병용.

### 2-4. Ce⁴⁺(4f⁰) vs Nd³⁺(4f³) — capping vs blocking
| | Ce⁴⁺ (4f⁰) | Nd³⁺ (4f³) |
|---|---|---|
| gap 종류 | Charge-Transfer(O 2p→빈 4f) | **Mott-Hubbard**(4f→4f, U) |
| SEI 작동 | electron **capping**(잡아 환원 Ce⁴⁺→Ce³⁺) = **소모성** | electron **blocking**(NdCl₃ Eg~5 → 벽) = **영구**(Nd³⁺ 유지) |
| DFT | 쉬움(4f⁰, U·spin 불필요) | 어려움(4f³, U=8, nspin2) |
> **아이러니**: 계산 어려운 Nd³⁺가 실용적으론 더 좋음(영구 차단). deck argument = "long-term stability(blocking)".

### 2-5. 왜 3+ / 마법수
6s→5d 떼면 3+에서 멈춤(4f는 차폐돼 안 떨어짐). 안정 배치 4f⁰/4f⁷/4f¹⁴(exchange 안정화) → Ce 4+(→4f⁰), Eu/Yb 2+(→4f⁷/4f¹⁴). Nd³⁺(4f³)는 마법수 멀어 **3+ only**.

### 2-6. NdS₄ 사면체 불가 — **(MgS₄ 비판과 동일 논리)**
- 크기: Shannon(4배위) **P⁵⁺ 0.38 ≪ Nd³⁺ 0.98 Å** → S₄ 사면체에 못 들어감(2.6× 큼).
- 전하: [PS₄]³⁻ vs [NdS₄]⁵⁻(불균형).
- 배위: Nd–S는 6–8배위(Nd₂S₃), 4배위 결핍.
- → **시뮬레이션에서 NdS₄ 보이면 안정상 아님(계면 결함/비정질). 논문 언급 금지.**
> 🔗 **litdb 연결**: 이 논리는 `papers/liu2023_…md` §12b의 **MgS₄ 비판**(Mg²⁺ 0.57 Å이 P 0.17 Å 자리에 = 무리)과 **정확히 같은 틀**. 우리 자체 4f-반경 프레임이 타 논문의 과해석(MgS₄ 사면체)을 사전 예측 = 일관성.

---

## 3. Nd₂O₃ → LPSCl1.6 도핑 메커니즘 (교정판 — 주역 = O)

**Dual substitution + 결함화학** (March §10–11 + June 교정):
1. **O → PS₄ S(16e) 치환**(검증, C2): P–O 강결합(−8.43, C3) → P–S* antibonding 고에너지화 → **PS₄ 환원붕괴 억제**. = March의 "PS₄ 강화" 가설을 June COHP가 입증.
2. **Nd³⁺ → Li 자리**(크기상 P 자리 불가): +3 Li(2 vacancy) = aliovalent. Nd는 결합·전자구조엔 미미(C4).
3. **self-limiting SEI**(분해산물이 wide-gap 전자절연):
   - **bulk/GB·anode**: **O-유래 Li₃PO₄ 5.73 / Li₂O 5.24** → σ_e↓(GB percolation 차단) → dendrite·self-discharge 억제 → cycle↑. (= 논문 central, O 주역)
   - **cathode(고전압)**: **Nd³⁺ 생존 → NdPO₄ 5.55* / NdCl₃ 4.30*** wide-gap passivation. (= 여기서만 Nd가 직접 기여, electron blocking §2-4)
4. **고전압/대기 안정성**: O 치환 → VBM↓(산화창↑), P–O/Nd–O(hard-hard)로 H₂S 억제.

> **March vs June 종합**: March는 Nd 기여를 다소 넓게 서술 → June은 **anode/bulk=O, cathode=Nd**로 역할 분리. Nd의 electron-blocking은 **cathode 한정 진짜**(Nd³⁺ 생존), bulk/anode는 O상이 담당. (상세 `nd2o3_master_findings` §3, `comparison_vs_ours.md` §E.)

---

## 4. Nd 포함 시 분석 도구 전략 (교정판)

| 분석 | E_F 의존? | Nd 포함 시 | 비고/대안 |
|---|---|---|---|
| Band gap (Nd 화합물) | ✅ | ❌ 4f Mott 실패 | **문헌값**(NdCl₃ 5.0 / NdOCl 4.5 / LiNdO₂ ~3.5); MP는 하한 |
| Band gap (Nd-도핑 host) | ✅ | △ 좁아짐(Nd 5d, −0.55) | host는 clean; "wide-gap insulator"+trend만 |
| **ELF (결합)** | ✅ | **✅ P–S/P–O/lone pair/Nd–X floor** | June 그림이 증거(C6). **on-Nd 4f 영역만 ❌** |
| PDOS (4f) | ✅ | ❌ 4f 위치 왜곡 | — |
| **Spin density**(plot_num=6) | ❌ | ✅ **4f 홀전자만** 선택적 시각화 | ρ↑−ρ↓ → 짝전자 자동상쇄; 4f³ 국소화 증거 |
| Formation E / convex hull | ❌ | ✅ 정확(오차상쇄) | — |
| Bader / 산화수 | ❌ | ✅ 정확 | XPS BE shift 예측 |
| Elastic | ❌ | ✅ 정확 | — |
| **COHP/ICOHP** | ❌(적분량) | ✅ P–S/P–O/Nd–X 다 OK | June LOBSTER figure |
| EXAFS(Nd L₃) | (실험) | ✅ Nd–O+Nd–S 공존 = 도핑성공 증거 | CN≠4(NdS₄ 아님) 확인 |

> **핵심 규칙(유지)**: "**4f의 *에너지*를 직접 보지 말고, 4f의 *결과*(전하·힘·스핀)만 봐라.**" — 단 **ELF 결합 영역은 4f 에너지가 아니므로 사용 가능**(C6 교정).

---

## 5. MP / June 데이터·figure 결합 (← "mp로 만든 걸 이거랑 결합")

### 5-1. SEI 산물 band gap (MP) — O가 만드는 wide-gap passivation
`docs/figures/nd_sei/sei_product_gaps_O.png` (O-유래 녹색 wide-gap vs 전도성 빨강 누설).
LiCl 6.65 · **Li₃PO₄ 5.73**(O) · NdPO₄ 5.55* · **Li₂O 5.24**(O) · NdCl₃ 4.30* · Li₂S 3.90 · **Li₃P 0.70**(누설) · NdS 0.00. (*=Nd MP 하한.)

### 5-2. 결합 (ICOHP/COHP, LOBSTER) — P–O 강결합 = O actor
`docs/figures/icohp/{nd,modelc}_COHP_4panel.png` (+ `*_curves.csv`, σ=0.10 평활) · `icohp_nd_bars.png/.csv`.
host **불변**(P–S modelc −6.00 vs nd −5.976) · **P–O −8.43(O actor)** · Nd–S −0.44(이온).

### 5-3. ELF — 결합 character
`docs/figures/nd_elf/{modelc,nd}_ELF_PS4plane.png`, `clean/nd_ELF_{PS4,PS3O,PS2O2}_clean.png`, `nd_ELF_PO_vs_PS_profile.png` (+ `nd_elf_bond_quant.csv`).
P–S 0.870(공유 백본) · P–O 0.838(강·polar) · Nd–X floor 0.13–0.19(이온).

### 5-4. oxophilicity (MP) — Nd ≠ 특별 getter
Al 3.45 > Y 2.13 > **Nd 1.75 ≈ Li 1.67** → 이점은 O 효과(C4).

### 5-5. 우리 baseline / band gap
doped host: U0 **2.184** → Nd+O **1.632**(−0.55, Nd 5d). comp1/modelc host gap ~2.07/2.10(clean). (상세 `our_dft_baseline.md`, `electronic.json`.)

---

## 6. 논문/세미나 표현 (교정 반영)
- **band gap(host)**: "PBE는 fundamental gap을 20–30% 과소(Δxc 결여) — structural/thermodynamic trend엔 영향 없음." (March 표현 유지.)
- **band gap(Nd 화합물)**: "Nd 화합물 gap은 문헌값 채택 — PBE+U가 4f on-site Coulomb(5–8 eV, 본 계산 U=8) 불충분으로 과소/금속화." (U=3.1→8 반영, C1.)
- **메커니즘**: "도핑 이점의 주역은 **O**: O→PS₄(16e) 치환으로 P–O 강결합(ICOHP −8.43) 형성 → PS₄ 환원저항↑; O-유래 Li₃PO₄/Li₂O wide-gap이 σ_e↓ → self-limiting SEI. Nd³⁺는 cathode에서 NdPO₄/NdCl₃ wide-gap passivation(electron blocking, 영구)·O 운반·aliovalent." (C2–C5 반영.)
- **NdS₄ 언급 금지**(§2-6). **CeO₂(capping/소모) 대비 Nd₂O₃(blocking/영구)** = long-term stability argument(§2-4).

## 7. 출처
- 개념(통합대상): March 260318·260320 노트(사용자 제공).
- June: `kb/results/nd2o3_master_findings_2026_06_18.md`, `nd2o3_O_effect_transfer_2026_06_24.md`, `kb/methodology/nd_vs_O_isolation_campaign_2026_06_18.md`, `kb/physics/260617_Nd2O3_doping_bandgap_narrowing_mechanism.md`.
- 데이터: `db/properties/{electronic,nd_icohp}.json`; figure `docs/figures/{nd_sei,icohp,nd_elf}/`; tool `tools/oxidation/{oxophilicity_descriptor,sei_product_gaps,esw_grand_potential}.py`, `tools/modelc_v3/plot_lobster_4panel.py`, `tools/figures/{plot_icohp_bars,plot_nd_sei_gaps,plot_elf_plane}.py`.

## 태그
#Nd #4f #란탄족 #MottHubbard #ChargeTransfer #ElectronBlocking #ElectronCapping #Ce_vs_Nd #PBE+U #BandGap #SIE #NdS4불가 #MgS4동일논리 #PS4강화 #P_O결합 #COHP #ELF #SpinDensity #EXAFS #oxophilicity #SEI #SelfLimiting #O주역 #교정노트
