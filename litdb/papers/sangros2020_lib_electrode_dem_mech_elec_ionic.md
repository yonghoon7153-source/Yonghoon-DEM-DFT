<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목 -->
# LIB 전극의 역학·전기·이온 거동을 DEM으로 — calendering + 바인더 bond 모델 + 삼중 전달 — Sangrós Giménez (Energy Technology 2020)

> slug `sangros2020_lib_electrode_dem_mech_elec_ionic` · DOI `10.1002/ente.201900180` · type `DEM (+ analytic homogenization, exp 검증)` · PDF `SangrosGimenez_2020_EnergyTech_LIBElectrode_DEM_MechElecIonic.pdf` · digested `2026-06-26` · status ✅

---

## 1. 한 줄 요약
**우리와 정확히 같은 "하나의 DEM 구조 위에서 역학·전기·이온 삼중 전달을 뽑는다"는 철학의 원조 논문** — 단
대상이 **액체전해질 LIB 전극(NMC + carbon-binder domain)**이라 (a) 이온 채널이 우리와 **위상이 정반대**
(이쪽은 **빈 공극(pore)이 전도체** → porosity·tortuosity Bruggeman; 우리 ASSB는 **SE 고체 입자망이 전도체**
→ Kirchhoff/Holm 구속), (b) **바인더를 입자-입자 bond로 명시 모델링**(=Varkey 2026이 그대로 가져다 쓰는
"Sangrós bond 모델"의 출처, 동일 TU-Braunschweig 그룹). calendering(압연) 압밀 → porosity·밀도 → σ_el·σ_ion·접착강도를
모두 미세구조 지표(배위수 CN·접촉면적·bond 수·fabric tensor)로 정의하고 **실측으로 검증**.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/binder/전해질) | 연구유형 |
|---|---|---|---|---|
| **C. Sangrós Giménez, C. Schilde, L. Froböse, S. Ivanov, A. Kwade** (TU Braunschweig, Institute for Particle Technology / Battery LabFactory BLB) | **Energy Technology 8(2), 1900180 (2020)** | 10.1002/ente.201900180 | **NMC111** LiNi₁ᐟ₃Mn₁ᐟ₃Co₁ᐟ₃O₂ AM + **carbon black 4 wt% + PVDF 4 wt%** (CBD) + 액체전해질(공극) | **DEM** (Thornton–Ning 탄소성 접촉 + Sangrós bond) + 해석적 균질화(homogenization) + 실험 검증 |

> 본 논문은 자기들 **1차 논문**(Sangrós Giménez et al., *Powder Technology* 349 (2019) 1, ref [17] — calendering의 **역학**만 다룬 검증된 모델)의 **2부**다. 1부에서 역학을 실측 calendering으로 보정·검증했고, 2부(본 논문)에서 그 **동일 구조 위에 전기·이온 전도·접착강도**를 올린다. 우리 frame[5] "한 DEM 구조 → 여러 물성"의 직접 선례.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **noncalendered porosity** | **0.522** (ρ_coating 2.13 g/cm³) | position A, 압연 전 | stated(Table 1) | 실험 앵커 |
| **calendered porosity** (C1–C4) | **0.417 / 0.368 / 0.305 / 0.270** | 압연응력 19.82/42.71/79.13/159.37 MPa | stated(Table 1) | ρ_coating 2.61/2.80/3.15/3.49 g/cm³ |
| **σ_electronic** (k_el) | **~0.45 → 1.55 S/m** (ε 0.417→0.270) | calendering ↑ → σ_el ↑ | digitized(Fig 2) | 단, ε<30 %서 모델이 실측보다 OVER (C4 form 1.55 vs exp ~1.2) |
| **σ_ionic** (k_ion) | **~0.0030 → 0.0012 S/m** (ε 0.417→0.270) | calendering ↑ → σ_ion **↓** | digitized(Fig 2) | Bruggeman ε^1.5; 압밀하면 공극↓→이온↓ (σ_el과 **반대 방향**) |
| **접착강도** (σ_n adhesion) | **~1.78 → 2.78 MPa** (ε 0.417→0.270) | calendering ↑ → 접착 ↑ | digitized(Fig 2) | bond force ↑ |
| **broken particles %** | **0 / 0.09 / 0.54 / 1.52 %** | C1/C2/C3/C4 | stated(Table 2) | C4도 1.52 %뿐 → "σ_el 감소는 파쇄 탓 아님" |
| **proportionality C_el / C_ion / C_ad** | **0.665 / 0.534 / 0.755** | 실측 fit | stated | 각 구성식의 단일 비례상수 |
| **k_p** (단일 NMC 입자 전자전도도) | **10⁻⁵ S/cm** | NMC 소재 | stated (Amin & Chiang [24]) | σ_el 식의 입력 |
| **k_ion^bulk** (전해질 벌크 이온전도도) | **0.01 S/cm** | 액체전해질 | stated | σ_ion 식의 입력 (모든 케이스 동일) |
| **bond 면적당 강성** (area-related) | **6 × 10¹² N/m³** | 바인더 bond | stated | calendered 구조용 (ref [17]) |
| **bond 파단 임계응력** | **2 × 10¹³ N/m²** | bond breakage | stated | |
| **NMC 입자강도 σ_p** | ~3.4 ×10⁸ → 1 ×10⁸ N/m² (입자 2 → 20 µm) | nanoindentation | stated/digitized(Fig 3) | **크기 ↑ → 강도 ↓** (작은 입자가 더 강함) |
| **E_NMC (delithiation 따라)** | **142.5 → 111.6 GPa** | pristine NMC → Li₀.₅NMC | stated | 리튬화에 따라 E 감소 (Xu et al. [32]) |
| **부피변화 (lithiation)** | **1.54 %** (x=0.5→1) | NMC333 격자 | stated | 등방 가정 (Kam [45], in-situ XRD) |
| **PSD / 입자 수** | 실측 NMC PSD, **2237 particles** | RVE 150×150×78.15 µm | stated | 측방 주기경계 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **DEM** (자체/그룹 구현; 1차 논문 ref [17]의 calendering 모델 계승). 후처리 균질화는 해석식(아래 eq 1–8).
- **DEM 접촉법칙** ★: **Thornton–Ning 탄소성 접촉모델** (ref [30]) — NMC 입자의 역학을 담당. (탄성 Hertz → 항복 → 선형 소성 분기 → 잔류겹침 제하. 본문은 "elasto-plastic contact model based on Thornton and Ning [30], combined with a bond model"으로만 기술; 식 자체는 1차 논문에 있음. **CONTACT 소성**이며 입자 형상은 강체 구로 유지.)
- **재료 파라미터**: E_NMC = 142.5 GPa(pristine) → 111.6 GPa(Li₀.₅NMC, delithiation 따라 가변, ref [32]); k_p(전자)=10⁻⁵ S/cm; 입자강도 σ_p는 크기의존(Fig 3, nanoindentation 80개 입자). carbon-black 4 wt% + PVDF 4 wt% = CBD(additive-binder matrix)는 **bond로** 표현.
- **bond/binder 모델** ★★ (**= "Sangrós bond 모델"의 원전**):
  - **입자-입자 bond = 바인더(additive-binder matrix, CBD)의 역학적 대리물**. 인접 NMC 입자 사이를 잇는 결합으로, **법선·접선 힘**을 전달한다 (본문: "transfers normal and tangential forces to the particles").
  - **면적당 강성**(area-related bond stiffness) = **6 × 10¹² N/m³** (calendered cathode 보정값, ref [17]).
  - **파단 기준** ★: bond에 걸린 응력이 **임계강도(ultimate strength) = 2 × 10¹³ N/m²** 에 도달하면 **bond가 끊어지고**, 해당 힘·모멘텀이 시뮬레이션에서 **제거**된다 (본문: "if a critical strength, also called the ultimate strength, is reached the bond gets broken and the corresponding forces and momentum are eliminated").
  - bond 수(B_p, bonds per particle)는 **전극 내부 연결성(connectivity)의 척도** — 바인더 망이 입자를 잡아주고 집전체와 연결하는 정도를 정량화.
  - **bond 부피** ↔ 실험 바인더 부피분율로 보정(1차 논문 절차). Varkey 2026이 `α_b`로 bond 부피=바인더 부피분율 맞춘 것이 바로 이 절차의 후속.
- **MPM/continuum**: 없음 (전부 DEM + 해석적 균질화).
- **전달 솔버** ★ (해석적 **homogenization/constitutive** 식 — 명시적 Kirchhoff 풀이가 아니라 **RVE 평균 fabric 기반 구성식**):
  - **전기(electronic), eq (1)**:
    `k_el = C_el · (1−ε) · (CN/π) · 3 · F_zz · (r_c/r_p) · k_p`
    — C_el(비례상수, 실측 fit=0.665), (1−ε)=고체분율, CN=NMC 입자당 접촉수(배위수), **F_zz=법선방향(집전체 수직) 대각 fabric tensor**(접촉의 방향성!), r_c/r_p=평균 접촉반경/평균 입자반경, k_p=단일 NMC 전도도. **Batchelor–O'Brien**[25] 단일입자 연결성식 기반.
  - **이온(ionic), eq (2)–(4)**: 두 표현이 같이 제시됨.
    - 해석(Bruggeman): `k_ion,anal = k_ion^bulk · ε/τ`, **τ = ε^(−0.5)** (eq 3, Bruggeman) → `k_ion ∝ ε^1.5`. (eq 2/3은 **실측 porosity로 σ_ion을 유도·검증**하는 데 씀.)
    - DEM-구조식(eq 4): `k_ion = C_ion · FSA · (CN_zz/CN_xx) · k_ion^bulk` — **FSA=specific free surface area**(어떤 접촉에도 안 쓰인 입자 표면적 = Li⁺ 삽입/탈리에 전기화학적으로 활성인 면적), **CN_zz/CN_xx = 법선/평면 방향 배위수 비**(방향성). **공극(전해질)을 통한** Li⁺ 전달이므로 "자유표면적·방향성"이 키.
  - **접착강도(coating adhesion), eq (5)**:
    `σ_n = C_ad · (A_CC−NMC / A_CC) · F_b · B_p`
    — C_ad(=0.755), A_CC−NMC/A_CC=집전체 중 NMC 접촉면적분율, **F_b=평균 bond force**(바인더 응집력), B_p=입자당 bond 수.
  - **응력장(eq 7–8)**: 입자별 viral 응력 `σ_ij = −[½ Σ_{Nb}(r₁F₁+r₂F₂)_pair + ½ Σ_{Nbonds}(r·F_b)_bond]` (eq 7, **pairwise 접촉항 + bond항** 합), 거시응력 `σ_electrode = −1/(3V)·Σ(σxx+σyy+σzz)` (eq 8). lithiation 시 응력 발달을 SOC 함수로 추적.
- **입자 처리** ★ (DEM판 "무질서 처리"): **구만** (NMC=강체 구, 실측 PSD 다분산). **rigid 입자 + CONTACT 탄소성(Thornton–Ning) + 입자-입자 bond** — 입자 **형상은 안 변함**(δ-overlap은 소성의 기하 프록시). 파쇄는 **취성 파단 기준**(stress-based, "NMC는 stiff → 소성으로 응력 안 풀림 → 임계응력서 깨짐", brittle fracture)으로 별도 처리.
- **도메인/RVE / servo / seeds / 압력범위**:
  - RVE = **150 × 150 × 78.15 µm** (78.15 µm = noncalendered 전극 두께), x·y **주기경계**.
  - calendering 모식(Fig 10): position A(압연 전) → 위 plate가 내려와 **목표 최대응력**까지 압축(position B) → 압력 해제 후 **탄성회복(springback)** → 최종 구조(position C). 바닥 plate = **집전체(current collector)** (점착 wall property).
  - calendering 응력 4수준: **19.82 / 42.71 / 79.13 / 159.37 MPa** (C1–C4). 초기 porosity sweep 0.48–0.60(별도 연구, 응력 42.71 MPa 고정).
  - **2237 particles**.
- **특이사항/튜닝**: (1) σ_el·σ_ion·σ_n 각각 **단일 비례상수**(C_el/C_ion/C_ad)를 실측으로 fit — 나머지는 전부 미세구조 지표에서 결정. (2) **방향성(F_zz, CN_zz/CN_xx)을 명시 도입** — "전도도는 방향의존량이므로 단일 스칼라로 못 줄인다"(집전체 수직방향이 핵심). (3) electrochemical cycling(5 cycle) 시 NMC 부피팽창/수축(1.54 %)을 SOC 따라 반영, E도 lithiation 따라 가변.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 전체 개념 모식 — DEM(noncalendered→calendering→Li de/intercalation) → micro-scale 지표(CN, bond 수, 입자-집전체/입자-입자 접촉면적, FSA, fabric tensor) → electrode-scale 물성(σ_el, σ_ion, 접착) | **우리 "DEM 구조 → 미세지표 → 거시물성" 파이프라인의 1:1 선례.** frame[5] 그림으로 인용 |
| **2** | **σ_el / σ_ion / 접착강도 vs 최종 porosity** (실측 ■ + 모델 ●, calendering degree 화살표) — σ_el과 접착은 ε↓(압밀)에 **증가**, σ_ion은 ε↓에 **감소**(공극↓). | **삼중 물성 한 그래프**; σ_ion이 σ_el과 **반대로** 가는 것(공극=이온 전도체이므로)이 우리 ASSB와 정반대인 핵심 증거 |
| **3** | NMC 입자강도 σ_p vs 입자크기(nanoindentation, 2–20 µm) — **작을수록 강함**(2 µm ~3.4×10⁸ → 20 µm ~1×10⁸ N/m²), 회색=산포밴드 | 파쇄 기준의 크기의존; 우리 Auerbach/fracture와 비교(우리는 SE) |
| **4** | (a) **CN vs cycle**(5 cycle), (b) **bonds per particle B_p vs cycle** — 두 지표 모두 사이클마다 진동하되 **사이클 끝에서 감소**(de/intercalation으로 접촉·bond 상실=구조붕괴=열화) | **사이클링이 접촉망/bond를 갉아먹는 것 = 열화 메커니즘.** 우리 morphology 열화(MPM Σdg)와 개념 대응 |
| **5** | **거시응력 vs SOC**(첫 사이클, C1–C4) — 압밀 강한 C4가 응력 최대(저porosity→접촉구속 큼), delithiation서 응력 감소(부피수축) | 압밀도↑ → 내부응력↑. 우리 MPM 응력장과 대응 |
| **6** | **거시응력 vs SOC, bond on/off**(C2·C4) — bond 있으면 응력이 **약간 더 높음**(바인더가 응력 buffer/전달) | bond(바인더)의 역학 기여 정량 — 우리 CBD 효과 추정 시 참고 |
| **7** | **electrode porosity vs 압연응력**(초기 porosity 0.48–0.60 4종) — 압연응력 증가에 모두 급강하 후 포화; 초기 porosity 높을수록 **더 빨리·더 낮게** 압밀(position B) | calendering 압밀곡선 형태(우리 P-vs-porosity와 비교; 단 LIB calendering) |
| **8** | **최종 porosity(posB=최대응력, posC=springback 후) vs 초기 porosity** — 초기 porosity ↑ → posB·posC 둘 다 ↓ (단 posC>posB, 탄성회복). **"치밀 전극 원하면 코팅/건조 단계에서 high porosity로 시작하라"** | springback 정량; 초기상태가 최종에 미치는 영향 |
| **9** | **σ_el / σ_ion / 접착 vs 초기 porosity**(모델) — 초기 porosity ↑ → σ_el ↑·접착 ↑(최종 더 치밀→CN↑), σ_ion ↓(FSA↓) | 초기 porosity가 transport에 미치는 비자명 영향 |
| **10** | calendering DEM 모식(position A/B/C, plate·집전체, h_A/h_B/h_C) + RVE 150×150×78.15 µm | 시뮬 셋업 그림 |

## 6. Post-processing ★
- **무엇**:
  - **porosity / 밀도**: 압밀 후 ε, ρ_coating (Table 1).
  - **σ_electronic**: eq (1) — fabric tensor F_zz(법선 접촉 방향성) + CN + r_c/r_p + (1−ε) 균질화. 입력 k_p=10⁻⁵ S/cm.
  - **σ_ionic**: **두 길** — (i) **Bruggeman 해석**(eq 2/3, τ=ε^−0.5 → ε^1.5) 실측 porosity로, (ii) **DEM 구조식**(eq 4) FSA·CN_zz/CN_xx로. 입력 k_ion^bulk=0.01 S/cm.
  - **접착강도**: eq (5) — A_CC−NMC/A_CC, 평균 bond force F_b, B_p.
  - **fracture**: 압밀 최대응력 지점에서 각 입자 응력 vs 크기의존 입자강도(Fig 3) 비교 → broken % (Table 2).
  - **fabric tensor**: 접촉 방향분포(F_zz, CN_zz/CN_xx) — **방향성**이 전기·이온 모두에 들어감.
  - **응력장**: viral(접촉+bond) per-particle 응력(eq 7) → 거시응력(eq 8), SOC 함수.
- **도구**: DEM(자체) + 해석식 후처리; 실측(σ_el은 Westphal 4-point [39], 접착은 Haselrieder pull-off [20], 입자강도는 McDowell–Bolton nanoindentation [40], σ_ion은 Bruggeman로 실측 porosity에서 유도).
- **수치화·플롯·기록 방식**: C1–C4 각각 σ_el·σ_ion·접착을 실측 vs 모델로 parity(Fig 2); 비례상수 3개(0.665/0.534/0.755)로 전 케이스 동시 맞춤.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (LIB) | 우리 (ASSB) | 차이 / 이유 |
|---|---|---|---|
| **삼중 전달 on one DEM 구조** | σ_el + σ_ion + 접착 (한 구조) | σ_e + σ_ionic + σ_thermal (한 구조) | **철학 동일 ✓** — 본 논문이 원조 선례 |
| **★ 이온 채널 위상** | **공극(pore)=전도체**: Li⁺가 액체전해질로 흐름 → ε·τ Bruggeman (ε^1.5) | **SE 고체 입자망=전도체**: Li⁺가 SE 접촉으로 흐름 → Kirchhoff/Holm 구속저항 | **★★ 위상 정반대.** LIB는 비울수록(공극↑) 이온↑; ASSB는 채울수록(SE 접촉↑) 이온↑. **우리 ASSB가 LIB의 pore-Bruggeman을 SE-network 구속으로 대체** |
| **σ_ion의 압밀 방향** | calendering ↑ → σ_ion **↓** (공극↓) | 압밀 ↑ → σ_ionic **↑** (SE 접촉↑) | **부호 반대** — 같은 물리 아님(전도체가 다름) |
| **전자 전달** | eq(1) fabric F_zz·CN·(1−ε) 균질화 | Kirchhoff Σ(φi−φj)/R=0, Holm R | **방법 유사**(접촉망 전자전도). 그들=해석 균질화, 우리=명시 Kirchhoff |
| **★ bond/binder** | **Sangrós bond**(법선·접선, 강성 6e12 N/m³, 파단 2e13 N/m²) | CBD = Stage-2(PTFE/VGCF) 부피점유; 명시 bond **아직 없음**(backlog A3) | **이게 우리가 binder bond 넣을 때의 템플릿.** Varkey 2026이 이 모델 그대로 사용 |
| **접촉 소성** | Thornton–Ning **CONTACT** 탄소성(δ 프록시) | MPM 진짜 SHAPE 소성 + DEM hooke/hysteresis | 둘 다 입자 형상 안 변함(DEM); **형상변화 = 우리 MPM 고유** |
| **압밀 모드** | **calendering**(압연 line-load, 회복 springback) | **cold-press**(단축 정수압 유지) | LIB 압연 ≠ ASSB 프레싱 — 압밀 메커니즘·springback 다름 |
| **E_AM** | E_NMC 142.5→111.6 GPa(SOC 가변) | E_CAM 140 GPa(고정) | 유사 스케일; 그들은 lithiation 가변 도입 |
| **검증** | **실측**(σ_el 4-point, 접착 pull-off, porosity calendering) | solver=ground truth(외부 실측 일부) | 그들 calendering·접착 실측이 LIB쪽 앵커(ASSB로 직접 전이는 불가) |
| **소재** | **NMC + 액체전해질**(LIB) | **LPSCl SE + NMC811**(ASSB) | **다른 셀 화학** → 절대값/이온위상 직접 전이 금지 |

### ★★ 핵심 대비 1 — 이온 채널 위상이 정반대 (LIB pore vs ASSB SE-network)
- **LIB(이 논문)**: 활물질·바인더는 **절연 매트릭스**, Li⁺는 그 사이 **빈 공극을 채운 액체전해질**로 흐른다. 따라서 σ_ion = f(공극율 ε, 굴곡도 τ) = **Bruggeman ε^1.5** (eq 2–3). **압밀(calendering)하면 공극이 줄어 σ_ion이 감소**한다(Fig 2 중단 — ε 0.417→0.270에 σ_ion ~0.0030→0.0012 S/m). 추가로 DEM 구조식(eq 4)은 **FSA(자유표면적)**과 **방향성(CN_zz/CN_xx)**으로 이를 미세구조와 연결 — 공극과 맞닿은 자유표면이 곧 Li⁺ 활성면이기 때문.
- **우리 ASSB**: 액체전해질이 없다. Li⁺는 **고체전해질(SE) 입자가 서로 맞닿은 접촉망**을 통해서만 흐른다. 따라서 **공극은 전도체가 아니라 방해물**이고, σ_ionic은 **SE-SE 접촉의 구속저항**(Holm R=1/(2σr_c)) + Kirchhoff로 푼다. **압밀하면 SE 접촉이 늘어 σ_ionic이 증가**한다 — 본 논문과 **정확히 반대 부호**.
- **→ 깔끔한 paper 대조**: "액체전해질 LIB에서는 *공극*이 이온 전도체(Bruggeman porosity·tortuosity)인 반면, all-solid-state 전극에서는 *고체전해질 입자망*이 이온 전도체다 — 본 연구의 pore-기반 이온 모델을 SE-네트워크 구속저항 솔버가 **대체**한다." 전자(σ_el)·접착은 양쪽이 같은 접촉/bond 물리라 직접 대응되지만, **이온만 위상이 뒤집힌다**는 게 우리 ASSB work의 정체성을 드러내는 가장 선명한 한 컷.

### ★★ 핵심 대비 2 — Sangrós bond 모델 = 우리 CBD/Varkey 링크
- **이 논문이 "Sangrós bond 모델"의 원전**이다. 입자-입자 bond가 바인더(CBD: carbon black + PVDF)의 역학을 대리하며, **법선·접선 힘 전달 + 임계응력 파단**(2×10¹³ N/m²)으로 정의된다.
- **계보**: 동일 그룹(TU Braunschweig, **Schilde·Kwade 공저자 공통**)의 **Varkey 2026**(`papers/varkey2026_multicontact_elastoplastic_dem.md`)이 이 bond 모델을 ref [38]로 인용해 **그대로 사용**(SBR+CB 실린더 bond, α_b로 bond 부피=바인더 부피분율). 즉 **Sangrós(2020, 원전) → Varkey(2026, 적용)** 라인이고, 둘 다 우리 wishlist Tier-2.
- **우리에게**: 우리는 CBD를 **Stage-2 부피점유**(PTFE/VGCF가 SE 도메인 부피를 차지)로만 다루고 **명시적 입자-입자 bond는 아직 없다**(backlog A3 — `docs/digest_model_application_backlog.md`). 만약 우리가 LIGGGHTS에 explicit binder bond를 넣는다면 **이 식(법선·접선 강성, 파단 임계응력, B_p, F_b)이 정확한 템플릿**이고, 접착강도 eq(5)는 그 bond망의 거시 발현을 어떻게 읽는지(F_b·B_p·집전체 접촉분율)까지 알려준다.

### ★ 핵심 대비 3 — 탄소성 접촉·calendering·σ_el 추출의 대응
- **Thornton–Ning CONTACT 탄소성** ↔ 우리 Luding hooke/hysteresis(`papers/luding2008_*`)/path-A. 둘 다 **CONTACT 레벨 소성**(δ 프록시), 입자 형상 불변. (Thornton–Ning 자체는 `papers/thorntonning1998_*`에 별도 digest.)
- **calendering 압밀** ↔ 우리 cold-press. 단 calendering은 **압연 line-load + 탄성회복(springback)**이라 정수압 단축 프레싱과 압밀경로가 다르다 — Fig 7/8의 "초기 porosity ↑ → 더 빨리·더 낮게 압밀되나 springback도 큼"은 LIB calendering 특유.
- **σ_el vs porosity·calendering** ↔ 우리 σ_e. 그들의 **eq(1) 균질화(F_zz·CN·r_c/r_p·(1−ε))** = 우리 **Stage-E/네트워크 솔버**의 해석적 대응물. 단 그들은 **단일 비례상수 + fabric tensor**로 닫고, 우리는 **명시 Kirchhoff + Holm + Stage-E 소성면적**으로 푼다(우리가 더 미시적). 둘 다 **방향성**(F_zz / CN_zz/CN_xx — 집전체 수직)이 핵심임을 독립 확인.

### frame[5] 위치
- **이 논문 = 전달/패킹 측**(rigid 구 + bond + 접촉역학 → 저항망/균질화 전달). **입자 형상소성·void-fill은 없음** — 우리 MPM이 메우는 그 절반이 빠져 있다(Varkey와 동일 한계, 같은 그룹).
- **그들 LIB 이온(pore-Bruggeman) = 우리 ASSB가 SE-network 구속으로 대체하는 바로 그 방법** — 깔끔한 대조축.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **paper 대조축 확보 — "이온 전도체의 위상 역전"**: LIB(공극=이온 전도체, Bruggeman ε^1.5, 압밀↓이온) ↔ ASSB(SE 입자망=이온 전도체, Holm 구속, 압밀↑이온). 우리 ASSB σ_ionic 솔버의 **존재 이유**를 한 문장으로 정당화하는 대비. σ_el·접착은 같은 접촉/bond 물리라 양쪽 직접 대응 → "삼중 전달 중 이온만 위상이 뒤집힌다"가 핵심 메시지.
- ② **explicit binder bond 템플릿(backlog A3)**: 우리가 CBD를 부피점유→명시 bond로 올릴 때 이 식이 청사진 — 법선·접선 bond 강성(면적당 6×10¹² N/m³ 류), 파단 임계응력(2×10¹³ N/m²), 거시 접착 = C_ad·(A_CC−NMC/A_CC)·F_b·B_p. **Varkey 2026이 이미 우리 인접 소재(halide)에서 이 bond를 돌렸으므로**, 두 논문을 묶어 "Sangrós bond 라인을 LPSCl에 이식" 가능.
- ③ **방향성(fabric/CN 비)을 전달에 넣을 근거**: 그들은 σ_el(F_zz)·σ_ion(CN_zz/CN_xx) 모두에 **집전체 수직방향 접촉 방향성**을 명시 도입. 우리 σ 스케일링은 등방 가정이 많은데, graded-z/층상(Phase-5)으로 가면 방향성 항이 필요할 수 있다 — 이 논문이 그 선례.
- ④ **데이터**: `docs/data/sangros2020_lib_electrode_dem_mech_elec_ionic.csv` — calendering 시리즈(porosity·밀도·응력·broken%, stated) + Fig 2/8/9 digitized(σ_el/σ_ion/접착, 초기·최종 porosity). **단 LIB라 절대값 ASSB 전이 금지, 추세·방법 대조용**.

## 9. 인용 가능 문장 (deck/paper용)
- "Sangrós Giménez et al. (2020) pioneered extracting **mechanical, electrical and ionic** behaviour from a **single DEM electrode structure** for Li-ion cathodes, with the additive-binder matrix represented as **explicit particle-particle bonds** (the 'Sangrós bond' model later reused by Varkey 2026) and a Thornton–Ning elasto-plastic contact for the NMC particles."
- "In a **liquid-electrolyte** LIB electrode the ionic conductor is the **pore phase** — σ_ion follows the Bruggeman relation σ_ion ∝ ε^1.5, so **calendering reduces σ_ion** by closing pores. In an **all-solid-state** electrode the ionic conductor is the **solid-electrolyte particle network**, so the pore-tortuosity description is **replaced** by a Kirchhoff/Holm constriction-resistance solver and **densification raises σ_ionic** — the two share electronic and adhesion physics but their **ionic topology is inverted**."

## 10. 주의/한계 (over-claim 방지)
- **LIB (액체전해질)** — 이온 채널이 **공극(Bruggeman)**이라 σ_ion 절대값·부호를 우리 ASSB(SE-network)로 전이 **금지**. 전자·접착만 물리 대응; **이온은 위상 자체가 다름**(대조용으로만).
- **강체 구 + CONTACT 탄소성** — 입자 형상 안 변함(δ=기하 프록시). NMC 파쇄는 brittle 임계응력 기준(소성 풀림 없음). **형상소성·void-fill은 없음** → 우리 MPM 영역과 별개(frame[5]).
- **σ_el·σ_ion·접착의 절대값은 단일 비례상수(C_el/C_ion/C_ad) fit에 의존** — 미세구조 추세는 모델이 주지만 절대 스케일은 실측 calibration. 비례상수 없이는 절대값 비교 불가.
- **σ_el 모델은 ε<~30 %(고압밀, C4)서 실측보다 OVER-predict** — 본문이 "고calendering이 전도망에 contact loss를 유발해 저항을 높일 수 있다(바인더 전도도 미반영)"고 인정. 즉 그들 σ_el 균질화도 고밀도서 한계(우리 Stage-E와 대조 가능).
- **Fig 2/8/9의 σ·porosity 값은 디지타이즈**(작은 그래프에서 읽음) → **추세만(±)**, Table 1(porosity·밀도·응력)·Table 2(broken%)·비례상수·bond 강성·k_p·k_ion^bulk만 **stated**.
- **압밀 = calendering(압연)** ≠ ASSB cold-press(정수압) — 압밀경로·springback이 달라 P-vs-porosity 곡선 형태도 직접 겹치면 안 됨.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
