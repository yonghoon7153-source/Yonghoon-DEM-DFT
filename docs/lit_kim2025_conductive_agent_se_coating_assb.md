# Kim 2025 (Battery Energy 4, e70044) — SE-coating-on-CAM에 들어가는 도전재(Super P 0D vs VGCF 1D)가 LPSCl ASSB 복합양극을 좌우 (★★★ 우리 SuperP-vs-VGCF CBD 작업의 실험적 同소재계 검증 — 가장 직접적인 한 편)

**인용:** Dongyoung Kim, Jongjun Lee, Seungyeop Choi, Myunggeun Song, **Hyobin Lee**,
**Yong Min Lee\***, "Impact of Conductive Agents in Sulfide Electrolyte Coating on Cathode
Active Materials for Composite Electrodes in All-Solid-State Batteries", *Battery Energy*
**4** (2025) e70044, DOI **10.1002/bte2.20250027** (Research Article, **Open Access CC BY**,
© 2025 The Authors, published by Xijing University + John Wiley & Sons Australia). 접수
2025-04-29 / 수정 2025-08-01 / 게재확정 2025-08-09. D. Kim & J. Lee 동등기여. 교신
yongmin@yonsei.ac.kr.

**소속:** (1) Dept. of Chemical & Biomolecular Engineering, **Yonsei University**(Seoul = 이용민
**Digital Twin Battery Lab, DTBL**) + (2) Dept. of Energy Science & Engineering, **DGIST**(Daegu)
+ (3) Dept. of Battery Engineering, **Yonsei University**(Seoul). Funding: NST(GTL24011-000) +
MOTIE(2410009726). Keywords: all-solid-state batteries · composite electrode · conductive agent ·
fabrication process · sulfide solid electrolytes.

**위치(인덱스):** 이 논문은 연구실 2026 리스트(#260–286)에 **없다** — **2025 Battery Energy** 별도 논문.
`docs/literature_yonsei_dtbl_2026.md`에 **DTBL CBD 논문(2025, TIER-2)**으로 추가, **#275(Koo 2026 SWCNT
sheath)** + `docs/cbd_morphology_roadmap.md`와 cross-link.

**소재계:** ★★★ **우리 정확한 소재계 + 우리 정확한 비교, 실험으로:**
- **CAM:** LiNi₀.₇Co₀.₁₅Mn₀.₁₅O₂ (**NCM711**, D₅₀ **7 µm**) = 우리 **AM** (big polycrystalline).
- **SE:** Li₆PS₅Cl (**LPSCl**, POSCO JK Solid Solution, argyrodite, D₅₀ **1 µm**) = 우리 **SE**.
- **CA(도전재):** **Super P**(Imerys, **0D** carbon black, primary ~40 nm) **OR** **VGCF**(Showa
  Denko, **1D** vapor-grown carbon fibre, Ø ~150 nm × 길이 ~10 µm) = ★ **우리 SuperP-vs-VGCF 비교 그 자체**.
- **조성:** CAM:SE:CA = **68.0 : 29.1 : 2.9 wt%** (★ 우리 1 wt% gap-filler보다 carbon이 **2.9 wt%로 많다** —
  중요한 regime 차이, §9에서 다룸).
- **압력:** SE pellet 70 MPa → 복합전극 + LPSCl **370 MPa 제조압(fab, 1 min)** → Li foil → **50 MPa 작동압**.
  (우리 300 MPa 냉간압축과 인접하나 동일하진 않음.)
- **셀:** NCM/Li all-solid-state half-cell. CC/CV 충전 + CC 방전, 3.0–4.3 V, 0.1 C 전사이클 4회 후 측정, 25 °C.

★★ **핵심 차별점 = CA가 들어가는 위치:** CA는 **"SE를 CAM 표면에 코팅하는 과정(SE-coating-on-CAM)" 중에
함께 섞여 들어간다.** 즉 carbon이 **bulk interstitial(입자 사이 공극)이 아니라 CAM 표면을 덮는 SE 코팅층 내부**에
배치된다. ⇒ **우리 voxel CBD가 모델한 bulk-gap-filler regime과 다른 regime** (이것이 §9 reconcile의 심장).

DB 동반 파일: **`docs/data/densification_porosity_db.csv`에 추가하지 않음.** 이유: σ값은 **standalone SE가 아닌
복합전극(SE-coating-on-CAM)을 ion/electron-blocking cell로 측정**한 값(370 MPa fab/50 MPa 작동, 0.9–13×10⁻⁴
S/cm 범위)이라 우리 porosity/σ **절대앵커**가 아니라 **TREND·morphology 증거**다. **수치 σ/porosity 앵커는
Bazzoun(LPSCl EIS)/Minnmann(LPSCl cold-press)/#266(LPSCl bimodal)/Varkey(halide)가 담당.** 본 논문 σ값은
**LPSCl 同소재계 SE-coating regime의 morphology→σ 방향 증거**로 본 MD 표에 정리.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**황화물 ASSB 복합양극에서 SE를 CAM 표면에 코팅할 때 도전재를 함께 넣으면, 도전재의 차원(0D Super P vs
1D VGCF)이 코팅층 형태를 완전히 바꾸고 그 결과 전기화학 성능이 갈린다:**
- **SE@CAM (CA 無):** CAM 표면에 **치밀한 SE 코팅층**(50–500 nm). baseline.
- **SE–SP@CAM (Super P, 0D):** ★ **Super P가 코팅층에 과다 분포한 "Super P-rich SE 코팅"**(500 nm–2 µm,
  다공·불균질) → **CAM 활성표면적↓ + 전기전도도↓ → 성능 나쁨**(SE@CAM보다 떨어짐).
- **SE–VGCF@CAM (VGCF, 1D):** ★ **VGCF가 코팅층에 sparse 埋입된 "VGCF-embedded SE 코팅"**(다공, VGCF가
  LPSCl을 부분 분쇄 + 임베드) → **활성표면적↑ + 전자전도 촉진 → 성능 좋음**(SE–SP@CAM보다 좋고 SE@CAM과 comparable).

⇒ ★★ **실험적으로 VGCF(1D) > Super P(0D), LPSCl ASSB에서.** (Super P가 코팅을 막아 활성면적/전도를 깎는다.)

**우리 hook(이 디제스트의 심장 — §9):** 이 논문은 우리 voxel CBD의 두 발견과 **한 축은 일치, 한 축은 regime 차이**다.
- **(이온축) ✅ 일치(실험적 확증):** 우리 voxel은 **Super P가 SE 이온망을 VGCF보다 ~1.8× 더 막는다**(σ_ionic SuperP
  0.0168 < VGCF 0.0298 mS/cm)를 측정. 이 논문은 **Super P가 SE 코팅을 점유해 활성표면적·이온경로를 줄인다**를 실험으로
  보인다(SE–SP@CAM 활성표면적 0.51 S = SE@CAM의 절반, 이온전도 0.9 vs 1.3×10⁻⁴ S/cm로 약간 낮음). ⇒ **Super P가
  SE/이온망을 더 막는다 = 우리 ionic 발견의 실험적 확증.**
- **(전자축) ⚠ regime 차이(정직하게):** 우리 voxel은 **bulk gap-filler regime(1 wt% carbon, 입자간 공극에 분포)**에서
  **Super P 1.3× > VGCF 1.1×**(density beats reach — 분산 Super P가 dead-AM 틈을 더 많이 접촉). 이 논문은 **SE-coating-on-CAM
  regime(2.9 wt% carbon, CAM 표면 SE 코팅 내부)**에서 **VGCF > Super P**(Super P의 분산 density가 **backfire** — Super
  P-rich 코팅이 CAM 활성표면 + 전도를 막음). ⇒ **두 verdict는 서로 다른 regime의 결과** — 우리 SuperP>VGCF는
  bulk-gap-filler corner에서 옳고, 실험 성능을 좌우하는 regime은 SE-coating-on-CAM이며 거기선 VGCF가 이긴다.
- ★ **정직한 model-setup gap:** 우리 `scripts/additives.py`는 carbon을 **bulk-interstitial(입자 사이)** 로 seed하지,
  **CAM 표면 SE 코팅 내부(interface layer)** 로 seed하지 않는다 → 우리 voxel은 **"Super P-rich 코팅이 CAM 활성표면을 막는"
  메커니즘 자체를 모델하지 못한다** → 그래서 실험의 VGCF>Super P verdict를 못 잡는다. = **우리 모델셋업의 진짜 gap**(아래 §9에서 명시).

⇒ **이 논문 = 우리 SuperP-vs-VGCF CBD 작업의 同소재계 실험 reference. 이온축은 확증, 전자축은 regime 차이 + model-setup gap.**

---

## 1. 배경 / 동기 (Introduction, p.1–2)

- **황화물 SE = 고에너지 ASSB의 가장 유망한 후보:** 상온 이온전도 >10⁻³ S/cm(액체 수준), t_Li⁺≈1, soft하여
  계면접촉·가공성 우수. (단점: 좁은 전기화학창, 수분민감, H₂S 발생.) Oxide(10⁻³–10⁻⁴, 계면 brittleness +
  고온소결)·polymer(<10⁻⁴, 낮은 전도·기계강도)보다 실용적.
- **복합전극(composite electrode)이 ASSB 성능의 핵심:** CAM + SE + CA(+필요시 binder). 성능은 구성재료뿐
  아니라 **전극의 구조**(혼합·응집·void)에 강하게 의존. 복합전극은 **큰 활성표면적 + 잘 연결된 이온/전자
  경로**가 필요한데, 불균질 혼합·응집·void로 **CAM 이용률↓ + 굴곡진(tortuous) 이온/전자 경로**가 흔한 문제.
- **★ SE-coating-on-CAM = 이 문제의 효과적 전략:** SE를 CAM 표면에 코팅하면 **활성표면적↑ + 잘 연결된 이온경로**
  형성 + **입자응집 완화 + 재료분산 개선** → 전기화학성능↑ + cycling 열화 완화. 그래서 SE-coating 연구가 많다.
- **❗ 그러나 SE-coating 연구는 대부분 "코팅공정·성능"에만 집중 — CA(도전재)가 코팅공정 중 어떻게 분포하는지,
  그것이 전극구조에 미치는 영향은 거의 탐구되지 않았다.** CA는 전자경로·활성표면적·SE 분해 등 전기화학·cycling에
  큰 영향. 특히 **SE-coated 전극에서는 CA의 영향이 더 커진다** — SE 코팅이 CAM↔CA 접촉면적을 제한해 전자전도를
  방해할 수 있기 때문(서론 명시: "SE coating limits the contact area between the CAM and CA, potentially
  impeding electron conduction pathways"). + **혼합 protocol(mixing)이 재료분산을 크게 좌우.**
- ★ **본 연구(명시):** **SE-coating 과정 중 CA 투입이 CA 분포와 전극구조에 미치는 영향**을 조사. CA로
  **carbon black(Super P)** 투입 시 **Super P-rich SE 코팅층** 형성 / CA 없는 SE-coated CAM은 **순수 SE 코팅층**.
  서로 다른 코팅 morphology가 뚜렷한 전극구조 차이 → 큰 전기화학 차이. 추가로 **CA 차원(0D Super P vs 1D VGCF)**의
  효과 비교 → VGCF는 **VGCF-embedded SE 코팅층** 형성. ⇒ CA가 SE-coating에서 하는 역할 + **혼합 protocol·CA 선택**의
  중요성을 제시.

**약어:** CAM = cathode active material(양극활물질, 여기 NCM711). SE = (sulfide) solid electrolyte(LPSCl).
CA = conductive agent(도전재; Super P 또는 VGCF). SP = Super P(0D carbon black). VGCF = vapor-grown carbon
fibre(1D). CE = Coulombic efficiency. GITT = galvanostatic intermittent titration technique(D_Li⁺·활성표면적
추출). ASA = active surface area(활성표면적). ion/electron-blocking cell = 이온/전자 차단셀(아래 §3).
SE@CAM / SE–SP@CAM / SE–VGCF@CAM = 3종 전극 코드.

---

## 2. SE-coating-on-CAM에 CA를 넣는 공정 + 결과 morphology (Fig 1, §2.1, §3 morphology)

★ 핵심 발견 1: **CA를 SE-coating 과정에 넣는 방식이 코팅층 morphology를 좌우 — 純 SE / Super P-rich / VGCF-embedded.**

**제조공정(§2.1, Fig 1a 모식):**
- **SE@CAM (CA 無, 2-step):** ① NCM711 + LPSCl을 **planetary mixer(Thinky AR-100) 2000 rpm 5 h**로 혼합
  (= SE를 CAM에 코팅) → ② 그 SE-coated CAM에 **Super P를 mortar·pestle로 수동 혼합**(hand mixing). 결과:
  NCM은 LPSCl로만 코팅, Super P는 나중에 외부에 분산.
- **SE–SP@CAM / SE–VGCF@CAM (CA 有, 1-step):** NCM711 + LPSCl + (Super P 또는 VGCF)를 **동시에 planetary
  mixer 2000 rpm 5 h** 단일공정. 결과: 코팅층이 **LPSCl + carbon 둘 다**로 구성.
- ⇒ ★ 차이는 **carbon이 코팅단계에서 함께 들어가느냐(1-step, 코팅층 내부)** vs **코팅 후 외부 분산(2-step)**.
  1-step에서 carbon이 SE 코팅층 안에 갇힘.

**표면 SEM (Fig 1b–d):**
- ★ **bare NCM(Fig 1b):** 다면체·각진(polyhedral, angular) 형상 + 매끈 표면 + 뚜렷한 입계(grain boundary).
- **SE@CAM(Fig 1c):** 각진 형상이 **둥글어지고 입계가 흐려짐 + bumpy 표면** = SE 코팅층 성공적 형성. **응집 Super P가
  SE-coated 표면에 불균질 산재**(mortar 추가혼합 탓).
- ★ **SE–SP@CAM(Fig 1d):** **치밀 SE 코팅층이 안 보임** — 대신 **불규칙 LPSCl 입자가 원형 유지한 채 표면에 빽빽이
  산재** + **CAM 표면에 Super P가 거의 안 보임**(Super P가 코팅층 안으로 들어감) → CA 투입이 morphology를 바꿈.

**단면 SEM + EDS (Fig 2, SE@CAM vs SE–SP@CAM):**
- ★ **SE@CAM(Fig 2a–e):** 코팅층 두께 **≈ 50–500 nm**, **치밀(dense)**. EDS: 코팅층 = LPSCl + 외곽에 **Super P
  산재**(코팅 바깥). ★ **코팅이 CAM 표면을 완전히 덮지 않음 → 노출된 CAM 영역(white arrow)이 CAM↔CA 접촉점 제공 →
  전자전도(CA–CA, CA–CAM) 형성 촉진.**
- ★ **SE–SP@CAM(Fig 2f–j):** 코팅층 **500 nm – 2 µm로 더 두껍고 다공(porous)**. **2상 혼재 — 밝은 LPSCl + 어두운
  Super P가 불균질 분포, Super P가 코팅층의 상당부분 점유.** LPSCl이 코팅 내부·표면 모두에서 **원형 유지**(Super P가
  혼합 중 LPSCl의 전단변형을 완화). ⇒ **코팅층에 들어간 SE(LPSCl)가 응집 Super P에 의해 SE–SE 이온경로에서 고립** →
  SE–SP@CAM 이온전도 약간↓.

**단면 SEM + EDS, 더 큰 스케일 (Fig 3a–h, SE@CAM vs SE–SP@CAM):**
- CAM·SE 분포(Ni, S map)는 두 전극 큰 차이 없음. ★ **차이는 dark-gray Super P(C map):**
  - **SE@CAM(Fig 3a–d):** Super P가 **균질 분산**(homogeneous).
  - **SE–SP@CAM(Fig 3e–h):** Super P가 **주로 CAM 입자 주변에 응집**(agglomerated around CAM), 다른 영역엔 소량 →
    부분 응집·불균질. ⇒ **응집 Super P가 코팅 CAM 입자 간 전기연결을 방해(impeded electrical connection) → 매우 낮은
    전기전도.**

**SE–VGCF@CAM morphology (Fig 5a,b 표면·단면 SEM, Fig S7 VGCF):**
- ★ **SE–VGCF@CAM**: SE–SP@CAM과 **같은 1-step 공정인데 morphology가 크게 다름.** **LPSCl이 NCM 표면에서 부분
  분쇄(partial crushing)** (SE–SP@CAM은 LPSCl 원형 유지였음 — Super P가 보호했기 때문). 표면에 **막대형 VGCF 소량 관찰.**
  단면(Fig S8/S9 EDS): **CAM 표면에 다공(porous) LPSCl 코팅층 형성 → 활성표면적↑** + **VGCF가 코팅층 전반에 sparse
  埋입(embedded) → 전자경로 형성.** CAM/SE 응집 없음, SE–SP@CAM/SE@CAM과 분포 유사(Fig S9).
- ★ **물리(차원 효과, p.7):** Super P = **0D, primary ~40 nm** → **변형하는 LPSCl 안에 쉽게 埋입 → 상대적으로
  치밀한(compact) 코팅층**(SE–SP@CAM). VGCF = **1D, Ø ~150 nm × 길이 ~10 µm(NCM 입경에 필적하는 길이)** → **높은
  aspect ratio가 LPSCl로의 전단응력 전달을 방해(hinders shear stress transfer) → LPSCl 변형 억제 → 더 다공(porous)
  코팅층, VGCF가 sparse 埋입.** ⇒ **CA의 차원/크기가 코팅층 morphology를 결정.**

---

## 3. 전기·이온 전도 측정 — ion/electron-blocking cell (Fig 3i–k, Fig 5c, §2.3)

★ 핵심 발견 2: **전자전도는 SE–SP@CAM이 3桁(orders) 폭락, SE–VGCF@CAM은 회복; 이온전도는 셋 다 비슷(VGCF가 약간↑).**

**방법(§2.3):**
- **전자전도(electron-blocking cell):** 복합전극 분말 200 mg을 **370 MPa**로 펠릿 → **Ti/composite/Ti**(Ti가 이온
  차단, 전자만 통과) → **DC 50 mV** 인가 → DC polarization으로 σ_e 산출.
- **이온전도(ion-blocking cell):** 복합전극 분말 200 mg을 370 MPa로 펠릿 → **양쪽에 LPSCl 150 mg을 더 얹어 다시 370
  MPa** → **Li/LPSCl/composite/LPSCl/Li** electron-blocking-아닌-ion-conducting 구조(Li가 이온 가역, LPSCl이 전자
  차단) → **AC EIS**(VSP-300 BioLogic, 14.1 mV, 5 MHz–10 mHz)로 σ_ion 산출. (Fig S2 = 두 셀 모식.)

**★★ EXACT 수치 (Fig 3k 막대 + Fig 5c 막대 + 본문):**

| 전극 | 전기전도 σ_e (S/cm) | 이온전도 σ_ion (S/cm) | morphology |
|---|---|---|---|
| **SE@CAM** (CA 無) | **3.3 × 10⁻²** | **1.3 × 10⁻⁴** | 치밀 SE 코팅 + Super P 외부 균질분산 |
| **SE–SP@CAM** (Super P 0D) | ★ **1.0 × 10⁻⁵** (**3桁 낮음**, ÷3300) | **0.9 × 10⁻⁴** (약간 낮음) | Super P-rich 다공 코팅(Super P 응집·CAM간 전기연결 차단) |
| **SE–VGCF@CAM** (VGCF 1D) | ★ **1.4 × 10⁻²** (**3桁 회복**, SE@CAM의 ~42%) | **1.6 × 10⁻⁴** (가장 높음, SE@CAM과 유사) | VGCF-embedded 다공 코팅(VGCF 균질분산, 전자경로) |

- ★★ **전자축(σ_e)의 핵심:** SE–SP@CAM이 **1.0×10⁻⁵로 SE@CAM(3.3×10⁻²)보다 3桁 낮다.** Super P를 SE-coating에
  함께 넣었더니 **오히려 전기전도가 폭락** — 응집 Super P가 코팅 CAM 입자 사이의 전기연결을 끊었기 때문. **VGCF를 같은
  방식으로 넣으면 1.4×10⁻²로 SE@CAM과 comparable**(균질 VGCF 분산 = 더 균일한 CA 분포). ⇒ ★ **VGCF(1D) > Super P(0D)
  전자전도, SE-coating regime에서.** (★ 우리 voxel bulk-gap-filler verdict와 반대 — §9.)
- **이온축(σ_ion):** 셋 다 0.9–1.6×10⁻⁴ S/cm 좁은 범위. SE–SP@CAM이 **가장 낮음(0.9)** — 코팅 내부 LPSCl이 응집
  Super P에 의해 SE–SE 이온경로에서 고립. SE–VGCF@CAM이 **가장 높음(1.6)** — VGCF는 SE 분쇄로 다공코팅 + SE를 덜
  방해. SE@CAM 1.3 중간. ⇒ ★ **Super P가 이온경로를 가장 많이 막는다 = 우리 SuperP 1.8× ionic-blocking 발견의 실험적
  확증(§9 이온축).** (절대 σ_ion 차이는 작지만 — 셋 다 같은 LPSCl 코팅이고 carbon은 부차적 — **순서는 SuperP가 최저**.)

**DC polarization·Nyquist (Fig 3i,j; Fig 5c):** Fig 3i = SE@CAM vs SE–SP@CAM의 DC 전류-시간(SE@CAM 높은 정상전류
= 높은 σ_e / SE–SP@CAM 낮음). Fig 3j = electron-blocking Nyquist(SE–SP@CAM이 큰 반원 = 높은 저항). Fig 5c = 3종
σ_e/σ_ion 막대 비교(VGCF가 σ_e에서 SE@CAM 거의 회복). (SI Fig S10 = SE–VGCF@CAM DC polarization 50 mV + Nyquist.)

---

## 4. 활성표면적 + 전기화학 성능 (Fig 4, Fig 5d–g, §2.4)

★ 핵심 발견 3: **SE–SP@CAM은 활성표면적 절반·용량·rate·수명 모두 나쁨; SE–VGCF@CAM은 SE@CAM과 comparable.**

**활성표면적 (ASA, GITT로 산출, Fig 4c):**
- GITT 정상상태/순간 전압변화 + 확산방정식 D = (4/πτ)(m_NCM·V_M/M_NCM·S)²(ΔE_s/ΔE_t)² 에서 **상대 활성표면적 S**
  추출(SE@CAM의 ASA를 **1.00 S**로 기준).
- ★★ **SE–SP@CAM 상대 ASA = 0.51 S = SE@CAM의 절반(−49%).** Super P가 코팅층을 지배 → **CAM↔SE 접촉이 크게
  감소**(코팅 내 Super P가 CAM-SE 접촉 방해). = ★ **Super P-rich 코팅이 활성표면적을 절반으로 깎는다**(우리 ionic 발견 ↔, §9).

**SE@CAM vs SE–SP@CAM 전기화학 (Fig 4a,b,d–f):**
- **초기 충방전 0.1 C (Fig 4a):** **SE@CAM 방전용량 185.3 mAh/g, 초기 CE 81.6%** (mortar-mixed CAM 단독보다도 높음
  = SE-coating이 성능↑, Fig S3). **SE–SP@CAM 151.6 mAh/g, CE 78.0%**(나쁨).
- **GITT 분극 (Fig 4b, SI Fig S4):** SE–SP@CAM이 **더 큰 분극**(ΔV) — 나쁜 전극구조 탓.
- **rate (Fig 4e, SI Fig S5/S6):** SE–SP@CAM이 **전 C-rate에서 SE@CAM보다 나쁨**(낮은 σ_e + 작은 ASA).
- **cycling (Fig 4f, 0.1C 충전/0.5C 방전, 200 cyc):** **SE@CAM 방전용량 113.0 mAh/g, 200사이클 70.9% 유지** vs
  SE–SP@CAM은 현저히 낮은 용량 유지(throughout cycling). ⇒ Super P 투입이 전극구조·전기화학을 크게 악화.

**SE–VGCF@CAM 전기화학 (Fig 5d–g):**
- ★ **초기 방전 0.1 C: 183.5 mAh/g, 초기 CE 82.7%** — **SE–SP@CAM(151.6, 78.0%)보다 훨씬 좋고 SE@CAM(185.3, 81.6%)과
  comparable.** rate(Fig 5e) = SE@CAM과 유사한 우수한 rate(SE–SP@CAM은 고율서 급락). cycling(Fig 5f, 200 cyc):
  **SE–VGCF@CAM 방전용량 117.3 mAh/g, 76.8% 유지** — SE@CAM(113.0, 70.9%)과 comparable(오히려 약간 높음).
- ⇒ ★★ **VGCF-embedded 코팅(다공 + 활성표면적↑ + 전자경로) → SE–SP@CAM을 명확히 능가, SE@CAM과 comparable.**
  = **VGCF(1D) > Super P(0D), 성능 전반.**

**메커니즘 모식 (Fig 5g):** ★ SE–SP@CAM = **Super P가 CAM 주위에 응집해 코팅을 덮음 → e⁻/Li⁺ 경로 둘 다 방해**
(작은 활성표면, 끊긴 전자망). SE–VGCF@CAM = **VGCF가 코팅 전반에 그물처럼 埋입 → 균일 전자망 + 다공코팅으로 Li⁺
경로 유지**(큰 활성표면, 연결된 전자망). ⇒ **0D는 코팅을 막고, 1D는 코팅을 뚫는다.**

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.4):** ★ 공정 + 표면 morphology — (a) **SE@CAM(2-step: planetary→hand-mix) vs SE–SP@CAM(1-step
  planetary) 모식**. (b) **bare NCM**(각진·매끈·입계). (c) **SE@CAM**(둥글·bumpy·SE코팅, Super P 외부산재).
  (d) **SE–SP@CAM**(치밀 SE코팅 無, LPSCl 원형산재, Super P 표면에 안보임=코팅내부). → ★ **CA 1-step 투입이
  코팅 morphology를 바꾼다**(우리 1-step thinky mixing seeding의 실험 대응 + carbon-in-coating regime 증거).
- **Fig 2 (p.5):** ★★ 단면 코팅층 — (a–e) **SE@CAM**(코팅 50–500 nm 치밀, Super P 외곽, white arrow=노출 CAM
  접촉점, EDS Ni/S/C). (f–j) **SE–SP@CAM**(코팅 500 nm–2 µm 두껍·다공, LPSCl+Super P 2상 불균질, Super P가
  코팅 상당부 점유, LPSCl 원형유지). → ★ **Super P-rich 코팅이 CAM↔SE 접촉을 줄이는 직접 증거**(우리가 모델
  못하는 SE-coating-interface 메커니즘).
- **Fig 3 (p.6):** ★★ 大스케일 단면 + 전도 — (a–d) **SE@CAM EDS**(Ni/S/C, Super P 균질). (e–h) **SE–SP@CAM
  EDS**(Super P CAM주위 응집·불균질). (i) **DC polarization 50 mV**(SE@CAM 높은 정상전류). (j) **electron-blocking
  Nyquist**(SE–SP@CAM 큰 반원=고저항). (k) **σ_e/σ_ion 막대**(SE@CAM 3.3e-2/1.3e-4 vs SE–SP@CAM 1.0e-5/0.9e-4 —
  σ_e 3桁 폭락). → ★★ **"Super P를 SE-coating에 넣으면 σ_e가 3桁 떨어진다"의 정량 증거.**
- **Fig 4 (p.7):** ★ SE@CAM vs SE–SP@CAM 전기화학 — (a) **초기 충방전**(SE@CAM 185.3/CE81.6 vs SE–SP@CAM
  151.6/78.0 mAh/g). (b) **GITT 전압+분극**(SE–SP@CAM 큰 분극). (c) ★★ **상대 활성표면적**(SE@CAM 1.00 S vs
  SE–SP@CAM **0.51 S = 절반**). (d) **Nyquist**(SE–SP@CAM 고저항). (e) **rate**(SE–SP@CAM 나쁨). (f) **200 cyc
  cycling**(SE@CAM 113.0 mAh/g·70.9% 유지). → ★ **활성표면적 절반 + 성능 악화 = Super P-rich 코팅의 결과**.
- **Fig 5 (p.8):** ★★ VGCF + 3종 종합 — (a,b) **SE–VGCF@CAM 표면·단면 SEM**(LPSCl 부분분쇄·다공코팅·VGCF 막대).
  (c) **3종 σ_e/σ_ion 막대**(VGCF σ_e 1.4e-2 = SE@CAM 거의 회복, SE–SP@CAM 1.0e-5 폭락; σ_ion VGCF 1.6e-4 최고).
  (d) **초기 충방전**(VGCF 183.5/CE82.7). (e) **rate**(VGCF≈SE@CAM). (f) **200 cyc**(VGCF 117.3·76.8% 유지). (g)
  ★ **메커니즘 모식**(SE–SP@CAM Super P 코팅 막음 e⁻/Li⁺ 방해 vs SE–VGCF@CAM VGCF 그물 埋입 균일 전자망+다공 Li⁺).
  → ★★ **VGCF(1D) > Super P(0D) 종합 + 차원효과 메커니즘 = 이 논문의 헤드라인 그림**(우리 reconcile 핵심).

### SI Figures (skim: SEM·blocking-cell·voltage)
- **Fig S1:** LPSCl·Super P SEM. **Fig S2:** ★ **ion-/electron-blocking cell 모식**(우리 방법참조). **Fig S3:**
  CAM vs SE@CAM 초기 전압프로파일 + rate(SE-coating이 mortar-CAM보다 성능↑ = SE-coating 효과). **Fig S4:** SE@CAM
  vs SE–SP@CAM SOC 50% GITT 확대. **Fig S5:** SE@CAM·SE–SP@CAM 0.1–2.0 C 충방전. **Fig S6:** SE@CAM·SE–SP@CAM
  rate. **Fig S7:** **VGCF SEM**(Ø~150 nm×~10 µm). **Fig S8,S9:** ★ **SE–VGCF@CAM 단면 SEM + EDS(Ni/S/C)** — 다공
  LPSCl 코팅 + VGCF C분포 확인. **Fig S10:** SE–VGCF@CAM DC polarization 50 mV + electron-blocking Nyquist.
  **Fig S11:** SE–VGCF@CAM 0.1–2.0 C 충방전. **Fig S12:** ★ 3종(SE@CAM·SE–SP@CAM·SE–VGCF@CAM) rate 비교.

---

## 6. 기술 미니용어집 (우리 맥락)

- **SE-coating-on-CAM(CAM 표면 SE 코팅):** SE(LPSCl)를 CAM(NCM711) 입자 표면에 planetary mixing으로 코팅 → 활성
  표면적↑ + 연결된 이온경로. ★ **이 논문의 CA는 이 코팅층 안에 배치된다**(우리 voxel의 bulk-interstitial carbon과 다른
  위치 = §9 regime 차이의 근원).
- **CA(conductive agent, 도전재) 차원(0D vs 1D):** Super P = 0D(carbon black, ~40 nm 구) / VGCF = 1D(섬유, Ø150
  nm×10 µm, AR≈67). ★ **차원이 코팅층 변형·morphology를 결정**(0D는 LPSCl에 埋입돼 치밀·막음, 1D는 전단전달 방해로
  다공·뚫음). = 우리 SuperP(구)/VGCF(섬유) morphology 구분과 동일 物理 축, 단 **위치가 코팅층**.
- **ion-blocking cell / electron-blocking cell(이온/전자 차단셀):** σ_ion·σ_e를 분리측정. electron-blocking =
  Li/LPSCl/composite/LPSCl/Li(Li 이온가역·LPSCl 전자차단 → AC EIS로 σ_ion). ion-blocking(전자전도용) =
  Ti/composite/Ti(Ti 이온차단 → DC polarization으로 σ_e). ★ **우리 Kirchhoff σ_ionic/σ_e의 실험 측정법** — 우리는
  contact-network solver로 같은 두 양을 분리해서 푼다(같은 분해, 측정 vs 계산).
- **active surface area(ASA, 활성표면적):** GITT로 추출하는 CAM 반응가능 표면적. SE–SP@CAM 0.51 S = SE@CAM의 절반.
  = 우리 **coverage / active-fraction / dead-AM map**의 셀-수준 대응(우리 Tabor/StageE coverage의 실험 ASA판; 단
  ASSB에서 CAM↔SE 접촉이 줄면 활성면적↓ = 우리 coverage↓).
- **Super P-rich coating(Super P 과다 코팅):** Super P가 SE 코팅층을 지배해 CAM↔SE 접촉·이온경로·전자연결을 막는
  morphology. ★ **우리 voxel이 모델 못하는 메커니즘** — 우리는 carbon을 입자 사이에 seed하지 코팅층 안에 안 넣는다.
- **VGCF-embedded coating(VGCF 埋입 코팅):** VGCF가 다공 LPSCl 코팅에 그물처럼 sparse 埋입돼 전자경로 + 활성표면적을
  살리는 morphology. = #275 SWCNT sheath의 carbon-black-대비-1D 우월성과 같은 방향(연속/1D가 discrete/0D를 이김).

---

## ★ 7. 우리 SuperP-vs-VGCF CBD 발견과 reconcile (★★★ 이 디제스트의 심장 — 정직하게)

⚠ **대전제(맨 먼저):** 이 논문은 ★ **우리 정확한 소재계(LPSCl sulfide ASSB + NCM711 + Super P/VGCF)**다. #275/#284
(NCMA/SiOx·액체)와 달리 **소재계 전이장벽이 없다** — 그래서 우리 CBD 작업의 **가장 직접적인 실험 reference**다.
그러나 핵심은 ★ **carbon의 위치(regime)가 우리 voxel과 다르다**:
- **이 논문:** carbon이 **SE-coating-on-CAM 안(CAM 표면을 덮는 SE 코팅층의 interface layer)**, 2.9 wt%.
- **우리 voxel:** carbon이 **bulk-interstitial(입자 사이 공극)**, 1 wt% (`scripts/additives.py`가 입자간 공간에 seed).

이 regime 차이가 ★ **이온축=일치 / 전자축=반대**를 만든다. 아래에서 두 축을 분리해 **정직하게** 정리한다(전자축 차이를
덮지 않는다).

### (a) ✅ 이온축 — CONFIRMED: "Super P가 이온망/접촉을 VGCF보다 더 막는다" (우리 voxel과 동일 방향)
- **우리(`docs/cbd_morphology_roadmap.md`, voxel σ_ionic, real_10):** **SuperP가 SE 이온망을 VGCF보다 ~1.8× 더
  막는다 — σ_ionic SuperP 0.0168 < VGCF 0.0298 mS/cm.** 物理: SuperP의 **분산 aggregate가 SE 사이로 끼어들어 SE
  이온 packing을 교란**(MPM SE-rearrangement), VGCF의 **집중 섬유는 SE를 거의 그대로 둠.**
- **그들(이 논문, Fig 3k·4c·5c):** 정확히 같은 방향을 실험으로 보인다 —
  - **σ_ion 순서: SE–SP@CAM 0.9 < SE@CAM 1.3 < SE–VGCF@CAM 1.6 (×10⁻⁴ S/cm)** → **Super P가 셋 중 최저**(코팅
    내부 LPSCl이 응집 Super P에 SE–SE 이온경로에서 고립), **VGCF가 최고**(SE 분쇄로 다공 + SE 덜 방해).
  - **활성표면적: SE–SP@CAM 0.51 S = SE@CAM의 절반** → Super P가 CAM↔SE 접촉(이온계면)을 절반으로 깎음.
- ✅ **판정 — 우리 이온 발견의 실험적 확증:** 우리 voxel "SuperP가 SE 이온망을 1.8× 더 막는다"를, 이 논문이 **同소재계
  (LPSCl)에서 "Super P가 σ_ion 최저 + 활성표면적 절반"**으로 실험 확증한다. ★ **주체는 다르다**(우리 = SE 망 packing
  교란 / 그들 = SE 코팅층 점유로 CAM↔SE 접촉 차단) **그러나 物理 방향은 동일: Super P(0D 분산)가 이온수송 접촉을 VGCF보다
  더 막는다.** 우리 ionic-blocking finding이 시뮬 artifact가 아닌 **同소재계 일반 物理**임을 확증. (단 절대 σ_ion 차이는
  작다 — 셋 다 같은 LPSCl 코팅이고 carbon은 부차적 — **순서/방향이 일치하는 것이 핵심**이지 1.8× 배율의 실험 재현은 아님.)

### (b) ⚠ 전자축 — REGIME 차이: 우리 bulk-gap-filler SuperP>VGCF vs 이 논문 SE-coating VGCF>SuperP (정직하게)
- **우리(`docs/cbd_morphology_roadmap.md`, voxel σ_e, real_10 + decimation sweep):** **bulk gap-filler regime**
  (1 wt% carbon, 입자간 공극 분포)에서 **SuperP 1.3× > VGCF 1.1×**, 그리고 **AM density 100→60%에서 안정적으로
  SuperP가 13–17% 더 이김**(crossover 無). 物理: real_10은 **AM 망이 이미 좋다**(DEM σ_e 8.64) → carbon은 backbone이
  아니라 **흩어진 dead-AM을 mop-up하는 supplement** → **density beats reach**(SuperP의 1.4M 분산 aggregate가 critical
  AM gap을 통계적으로 더 많이 접촉; VGCF의 32k 긴 섬유는 1 wt%에서 self-percolate 못해 reach 이점이 안 산다). 즉 우리
  결론은 명시적으로 **"1 wt% gap-filler regime의 corner verdict"**다.
- **그들(이 논문, Fig 3k·5c):** **SE-coating-on-CAM regime**(2.9 wt% carbon, CAM 표면 SE 코팅층 내부)에서 **VGCF >
  Super P** — **SE–SP@CAM σ_e 1.0×10⁻⁵(3桁 폭락) < SE–VGCF@CAM 1.4×10⁻²(SE@CAM 거의 회복).** 物理: carbon이 코팅층
  안에 있으면 **Super P의 분산 density가 backfire** — 응집 Super P가 **코팅 CAM 입자 사이의 전기연결을 끊고**(Fig 3e–h
  Super P가 CAM 주위 응집), VGCF의 1D는 **코팅 전반에 그물처럼 埋입돼 전자경로를 살린다.** 즉 같은 "Super P density"가
  **bulk에선 mop-up 이점(우리), 코팅 interface에선 차단 단점(그들)**으로 정반대로 작용.
- ⚠ **판정 — 모순이 아니라 REGIME 차이(정직하게, 덮지 않는다):**
  - 우리 SuperP>VGCF는 ★ **bulk-gap-filler corner에서 옳다**(테스트로 확인 — density beats reach, AM 모든 밀도서 stable).
  - 그들 VGCF>Super P는 ★ **SE-coating-on-CAM regime에서 옳다**(실험 — Super P-rich 코팅이 전자연결 차단).
  - ★★ **두 regime은 다른 物理:** bulk에선 carbon이 **AM 골격 위 흩어진 gap을 mop-up**(분산=많은 접촉=이점), 코팅에선
    carbon이 **CAM↔CAM 전기연결을 매개하는 interface**(분산 응집=연결 차단=단점). ⇒ **carbon density의 부호가 regime에
    따라 뒤집힌다.** 우리 voxel은 bulk regime만 모델하므로 SuperP>VGCF가 나오고, **실험 성능을 좌우하는 regime은
    SE-coating-on-CAM이며 거기선 VGCF가 이긴다.**
  - ★ **추가 lever 일치:** 우리는 명시적으로 **"VGCF가 이기는 regime은 carbon LOADING↑/thin-electrode(carbon-as-backbone)
    이지 AM-poorness가 아니다"**(roadmap, decimation sweep 결론)라고 적었다. 이 논문은 **carbon 2.9 wt%(우리 1 wt%의 ~3배) +
    coating-interface**라는 **다른 lever(loading↑ + 위치)**에서 VGCF가 이기는 것을 보여 — **우리 "VGCF는 backbone/loading
    regime에서 이긴다"는 예측과 방향 일치**(단 그들 lever는 loading만이 아니라 **coating-interface 위치**가 결정적).

### (c) ★ 정직한 model-setup gap — 우리 voxel이 SE-coating-on-CAM 메커니즘을 모델하지 않는다
- **우리 `scripts/additives.py`:** carbon을 **2가지 morphology × bulk-interstitial 위치**로 seed — **SuperP**(0D,
  distributed aggregates, 입자간 공극) + **VGCF**(1D, interstitial fibres, 입자간 공극). 둘 다 **입자 사이 공간**에
  배치된다(mixing=thinky면 SuperP가 AM 표면 일부 코팅하지만, **CAM을 덮는 SE 코팅층의 interface layer로 carbon을 넣는
  메커니즘은 없다**).
- **그들(이 논문) = 우리가 모델 안 하는 메커니즘:** carbon이 **CAM 표면을 덮는 SE 코팅층 안**에 들어가 — Super P면 **코팅을
  Super P-rich로 만들어 CAM 활성표면 + CAM↔CAM 전기연결 + 이온경로를 막고**, VGCF면 **다공코팅에 埋입돼 다 살린다.** 이
  **"코팅층 내부 carbon이 CAM 활성표면/접촉을 막는다"**가 실험 verdict(VGCF>Super P)를 좌우하는 메커니즘이다.
- ★ **이것이 진짜 model-setup gap이다(정직하게):** 우리 voxel은 **bulk-interstitial carbon만 seed**하므로 **Super
  P-rich 코팅이 CAM 활성표면을 막아 σ_e를 3桁 떨어뜨리는 메커니즘 자체를 표현하지 못한다** → 그래서 **실험의 VGCF>Super P
  전자 verdict를 못 잡는다.** 우리 SuperP>VGCF(전자)는 **우리가 모델한 regime(bulk gap-filler)에서만 유효한 답**이고,
  **실험적으로 성능을 좌우하는 SE-coating regime은 우리 모델 밖**이다. ⇒ 우리 전자 verdict는 **regime-specific**임을
  명시해야 한다(SuperP>VGCF = bulk-gap-filler corner only; 실험 = SE-coating regime에서 VGCF wins).

### (d) ★ audit ✅#4 + cbd_morphology_roadmap에 무엇을 의미하나 (사용자가 직접 fold — 여기선 제안만)
> ⚠ 본 디제스트는 `docs/stage2_model_audit_vs_literature.md` / `docs/cbd_morphology_roadmap.md` /
> `docs/positioning_vs_geodict.md`를 **수정하지 않는다**(사용자가 직접 fold). 아래는 **fold용 정리**다.

- **audit ✅#4(기존: "discrete carbon 퍼콜 불가 = #275 정합"):** 이 논문은 **이온축은 강화**(Super P가 LPSCl
  同소재계에서 σ_ion 최저 + 활성표면적 절반 = 우리 SuperP ionic-blocking의 실험 확증). 그러나 **전자축에는 nuance를
  추가** — audit이 "SuperP>VGCF 전자"를 일반 verdict로 적었다면, 이 논문은 **그것이 bulk-gap-filler regime에 국한되고
  성능-관련 SE-coating regime에선 VGCF가 이긴다**는 同소재계 실험 반례를 제공한다. ⇒ audit ✅#4를 ★ **"이온축:
  Super P-blocking 同소재계 실험 확증(Kim 2025) / 전자축: SuperP>VGCF는 bulk-gap-filler regime-specific, SE-coating
  regime은 VGCF wins(Kim 2025) — 우리 additives.py가 SE-coating-interface carbon을 모델 안 하는 model-setup gap"**으로
  **정직하게 규정**할 것을 제안.
- **cbd_morphology_roadmap의 SuperP>VGCF 전자 verdict:** ★ **regime-specific으로 라벨**할 것 — "SuperP 1.3× > VGCF
  1.1×"는 **real_10의 1 wt% bulk-gap-filler corner**의 답이고, **실험(Kim 2025, LPSCl 同소재계, SE-coating, 2.9 wt%)은
  VGCF>Super P**다. roadmap의 PENDING "4 wt% VGCF-regime 테스트"(carbon loading↑ → carbon-as-backbone → VGCF 이김)
  옆에 ★ **"SE-coating-on-CAM regime"을 두 번째 VGCF-win 경로로 추가** — Super P-rich 코팅이 CAM 활성표면을 막는 것을
  voxel로 재현하려면 **`additives.py`에 `se_coating_interface` carbon 옵션**(carbon을 입자간이 아니라 **AM 표면을 덮는 SE
  코팅 셀 안**에 seed → Super P면 코팅을 막아 CAM 활성표면/전자연결↓, VGCF면 다공埋입) 필요. (이건 §(c)의 model-setup gap을
  메우는 구체 도구 제안이다.)

### 비교 요약표
| 축 | Kim 2025 (LPSCl ASSB, SE-coating regime, 실험) | 우리 (LPSCl ASSB, bulk-gap-filler regime, voxel) | 판정 |
|---|---|---|---|
| 소재 | NCM711 + LPSCl + Super P/VGCF, 68:29.1:2.9, 370/50 MPa | NMC811 + LPSCl + SuperP/VGCF, ~80:18:1, 300 MPa | ✅ **同소재계**(전이장벽 없음); ⚠ carbon 위치·wt% 다름 |
| carbon 위치 | **SE-coating-on-CAM 내부**(CAM 표면 SE 코팅층 interface) | **bulk-interstitial**(입자 사이 공극) | ★ **regime 차이의 근원** |
| 이온: Super P가 더 막음 | σ_ion SE–SP 0.9 < SE@ 1.3 < VGCF 1.6 (×10⁻⁴) + ASA 0.51 S | σ_ionic SuperP 0.0168 < VGCF 0.0298 (1.8×) | ✅ **CONFIRMED**(방향 일치; 주체 다름: 코팅점유 vs SE-packing) |
| 전자: 누가 이기나 | ★ **VGCF > Super P** (σ_e SE–SP 1.0e-5 ≪ VGCF 1.4e-2, 3桁) | ★ **SuperP > VGCF** (1.3× vs 1.1×, AM 모든밀도 stable) | ⚠ **REGIME 차이**(우리=bulk gap-filler corner / 그들=SE-coating; carbon density 부호 뒤집힘) |
| model-setup gap | (SE-coating-interface carbon = 실험 verdict 메커니즘) | additives.py는 bulk-interstitial만 seed | ★ **우리 voxel이 Super P-rich 코팅 차단 메커니즘 미모델 → 전자 verdict 못 잡음** |
| 성능 | SE–VGCF@CAM ≈ SE@CAM ≫ SE–SP@CAM (183.5 vs 185.3 vs 151.6 mAh/g) | (성능 아닌 σ만) | ★ 실험 성능-관련 regime = SE-coating, VGCF wins |
| 측정 vs 예측 | post-mortem SEM/EDS + blocking-cell σ + GITT ASA | 압력→구조→σ 예측 + voxel FV carbon σ | frame[5] 분업(그들=측정, 우리=예측); ⚠ 우리 regime이 실험과 어긋남 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) ✅ **이온축 = 同소재계 실험 확증(가장 강한 결과).** Kim 2025는 **우리 정확한 LPSCl ASSB**에서 **Super P가 σ_ion
   최저(SE–SP 0.9 < SE@ 1.3 < VGCF 1.6 ×10⁻⁴) + CAM 활성표면적을 절반(0.51 S)으로 깎는다**를 실험으로 보인다 —
   우리 voxel "SuperP가 SE 이온망을 VGCF보다 1.8× 더 막는다"의 **直接 同소재계 실험 확증**(주체는 다르나 방향 동일).
   #275(NCMA/액체, 소재 전이 필요)와 달리 **소재 전이장벽이 없는** 우리 ionic-blocking 발견의 가장 강한 reference.

2) ⚠ **전자축 = REGIME 차이 + 정직한 model-setup gap(가장 중요한 자기-점검).** 실험은 **VGCF > Super P**(SE–SP σ_e
   1.0e-5 3桁 폭락; Super P-rich 코팅이 CAM↔CAM 전기연결 차단), 우리 voxel은 **SuperP > VGCF**(bulk gap-filler에서
   density beats reach). ★ **모순이 아니라 carbon 위치(regime)가 다른 것** — 우리는 **bulk-interstitial carbon**(`additives.py`)을
   모델하고, 실험의 verdict를 좌우하는 건 **SE-coating-on-CAM 안의 carbon**(Super P-rich 코팅이 활성표면/전자연결을 막는
   메커니즘, 우리 미모델). ⇒ 우리 SuperP>VGCF(전자)는 ★ **bulk-gap-filler corner에서만 유효한 regime-specific 답**임을
   명시; **실험적으로 성능을 좌우하는 SE-coating regime은 우리 모델 밖이고 거기선 VGCF가 이긴다.** (덮지 말 것 — 이건
   우리 additives.py 셋업의 진짜 한계다.)

3) ★ **`additives.py`에 `se_coating_interface` carbon 옵션 = gap을 메우는 구체 도구 + #275와 합쳐지는 강한 same-group
   증거.** model-setup gap(§(c))을 닫으려면 carbon을 **입자간이 아니라 CAM 표면을 덮는 SE 코팅 셀 안**에 seed하는 옵션이
   필요 — Super P면 코팅을 막아 CAM 활성표면/전자연결↓(VGCF면 다공埋입으로 살림) → voxel σ_e가 실험 VGCF>Super P를
   재현하는지 테스트. ★ 또한 **Kim 2025(0D coating 막음 < 1D embed) + #275(0D discrete < 연속 1D sheath)**를 합치면
   **같은 그룹(이용민)의 同소재계+일반계 실험 2편이 "1D/연속 carbon morphology가 0D/discrete를 이긴다"를 ASSB에서 증명** —
   우리 voxel의 SuperP>VGCF(전자)는 **bulk-gap-filler corner**의 답이지 **SE-coating reality가 아님**을 두 논문이 함께
   못박는다. (cross-ref: `docs/lit_koo2026_swcnt_sheath_thick_electrode.md` #275 + `docs/cbd_morphology_roadmap.md`.)

### 보너스 — 혼동 금지(역할 구분)
- **Kim 2025(이 논문, LPSCl ASSB·SE-coating·Super P vs VGCF):** ★ **우리 SuperP-vs-VGCF의 同소재계 실험 reference** —
  이온축 확증 + 전자축 regime 차이 + model-setup gap. **carbon 위치(SE-coating-interface)** 축. **σ/porosity 절대앵커 아님**
  (복합전극 blocking-cell σ = TREND).
- **#275(Koo 2026, NCMA/흑연·액체 dry):** **우리 voxel CBD 발견(전자 σ=0 퍼콜 + 이온 blocking)의 실험적 증명** +
  **연속 SWCNT sheath = 제3 morphology** + digital-twin blueprint. **carbon 연속성/discrete** 축. 소재 전이 필요.
- **#284(Oh, SiOx/흑연·액체):** **CBD ion/electron trade-off 독립확증 + balance point(moderate-C 최적)** + 분산정량법.
  **carbon 양/두께** 축. 소재 전이 필요.
- **세 논문 모두 우리 CBD 작업과 다른 축에서 보완 — Kim 2025만 同소재계(LPSCl)이고, 유일하게 "우리 전자 verdict가
  regime-specific"이라는 同소재계 반례를 준다.** σ/porosity 절대앵커는 Bazzoun(LPSCl EIS)·Minnmann(LPSCl cold-press)·
  #266(LPSCl bimodal)·Varkey(halide)가 담당 — 혼동 금지.
