# Lee 2025 (Nat. Commun. 16, 4200) — 건식 co-rolling 공정으로 박막 SSE + 친밀 계면 → 저(低)작동압(2 MPa) 안정 ASSB

**인용:** Dong Ju Lee, Yuju Jeon, Jung-Pil Lee, Lanshuang Zhang, Ki Hwan Koh, Feng Li,
Anthony U. Mu, Junlin Wu, Yu-Ting Chen, Seamus McNulty, Wei Tang, Marta Vicencio,
Dapeng Xu, Jiyoung Kim, **Zheng Chen\***, "Robust interface and reduced operation pressure
enabled by co-rolling dry-process for stable all-solid-state batteries," *Nature
Communications* **2025**, *16*, 4200. DOI **10.1038/s41467-025-59363-4**.
UC San Diego (Aiiso Yufeng Li Family Dept. of Chemical and Nano Engineering + Program of
Materials Science and Engineering + Sustainable Power and Energy Center) + **LG Energy
Solution** (LG Science Park, Seoul). Open Access (CC-BY 4.0).
Received 2024-07-15 / Accepted 2025-04-21 / Published online **2025-05-06**.
(저널 코드 41467 = Nat. Commun., 2025, article 59363 → vol. **16**, article no. **4200**, DOI tail
**59363-4**. SI = 공식 **MOESM1_ESM**(40 p, Supp Fig 1–33 + Supp Table 1–4 + Supp Note 1) 직접 확인 —
앞서 받은 `Sup_...` 사본과 **내용 byte-identical**(수치·캡션 전부 동일, 부분본 아님).)

**소재:** **Li₆PS₅Cl (LPSCl argyrodite, <1 µm 볼밀)** SSE + **NCM811** 양극 활물질
(PC-NCM = polycrystalline LiNi₀.₈Co₀.₁Mn₀.₁O₂ 5–15 µm, **LG Energy Solution** / SC-NCM =
single-crystal LiNi₀.₈₂Co₀.₁₁Mn₀.₀₇O₂ "NCM82" 3–5 µm, MSE Supplies) + **VGCF**(도전제,
>98 %) + **PTFE**(바인더, <300 nm, Chemours). 음극(full cell) = **Si**(>99.9 %, 1–5 µm)
+ LPSCl + VGCF + PVDF. ★ **SE·CAM·도전제·바인더가 우리 모델 소재계와 정확히 동일**(LPSCl +
NCM811 + VGCF + PTFE) — Bazzoun(LPSCl+NCM811, 도전제/바인더 無)보다 한 발 더 일치.

> ⚠ **본 digest 의 성격·중복 안내:** 이 논문은 이미 `litdb/papers/lee2025_corolling_dryprocess_lpscl_ptfe.md`
> (digest 2026-06-24)에 **CBD/binder-fibrillation 검증 + 전달 σ 앵커** 관점으로 정리되어 있다.
> 본 `docs/` digest 는 **다른 축** — **(1) 건식 co-rolling 제조공정, (2) 저작동압(2 MPa) robust 계면
> 메커니즘, (3) 우리 "제조압(fabrication 300 MPa) vs 작동압(operating 수~수십 MPa)" 구분에의 매핑
> (Doux 5 MPa·Minnmann 측정 40 MPa 와 합류)** — 을 깊게 판다. 두 파일은 보완 관계이며 수치는 일치한다.
> (papers/ 파일은 σ·CBD·파괴를, 본 파일은 공정·압력·계면·void-vs-P 를 owns.)

동반 데이터 파일:
- `docs/data/lee2025_transport_anchors.csv` — PTFE wt% σ 페널티 + 조성별 σ + bulk LPSCl 앵커
  (papers/ digest 가 생성, 본 digest 도 공유).
- `docs/data/densification_porosity_db.csv` — 본 digest 가 **Lee2025 작동압(2 MPa/75 MPa) cycling
  retention + void-ratio** 행을 *압력-구분 컨텍스트*로 추가 (절대 porosity 는 주지 않음 — §10 참조).

**같은 "압력 구분" 패밀리 안에서의 위치:**
- **Doux 2020** = 작동압 *창*을 Li-metal 단락으로 못박음 (5 MPa 최적, ≥25 MPa creep 단락).
- **Minnmann 2021 JES** = 압밀 380 MPa / EIS-TLM 측정 40 MPa (압력 3종 구분 + porosity 13–17 %).
- **Cronau 2021** = stack pressure 가 σ *측정 신뢰성*을 좌우 (protocol).
- **Lee 2025**(본 digest) = **공정(co-rolling)이 만든 robust 계면이 작동압을 75 → 2 MPa 로 낮춰도
  >80 % 유지**시킴을 실증 → **"좋은 계면 = 낮은 작동압 허용"** 의 *공정-측 인과*를 추가.
네 논문이 합쳐 **제조압(fab ~300–500 MPa) ≠ 작동압(operating ~2–70 MPa)** + **계면 품질이 작동압
하한을 정한다**는 그림을 완성한다 — 이게 본 digest 의 우리 모델에 대한 핵심 기여.

---

## ★★★ §0. 한 줄 결론 — 이게 왜 우리 모델에 중요한가 ★★★

우리 DEM/MPM 은 **제조압(300 MPa cold-press, Heckel P_y=138 MPa)** 으로 미세구조를 만들지만,
실제 셀은 훨씬 낮은 **작동 stack pressure(수~수십 MPa)** 에서 사이클된다. Lee 2025 는 **공정**으로
이 둘을 잇는 논문이다:

> **두꺼운 SSE feed 와 양극 feed 를 *함께* roll-press(co-rolling)** 하면, (a) 균일한 **박막 SSE 층(50 µm)**
> + (b) 고로딩(5 mAh cm⁻²)·고AM비(80 wt%) 양극이 *동시에* 만들어지고, (c) **roll 의 shear 가 계면에서
> PTFE 를 섬유화(fibrillate)** 시켜 SSE-양극을 **융합(fused)** 시킨다. 이 robust 계면 덕에 **작동압을 통상
> 75 MPa → 2 MPa 로 낮춰도 500 사이클 후 >80 % 유지**(freestanding 대비)된다.
> 추가로 **310 Wh kg⁻¹ / 805 Wh L⁻¹ (stack-level)** pouch cell 을 5 MPa·30 ℃ 작동으로 실증.

우리에게 주는 것 세 가지:
1. **제조 vs 작동압 분리의 *공정-인과* 버전** — Doux 가 "5 MPa 가 최적"(현상)이라면, Lee 는 "계면을
   잘 만들면 2 MPa 도 됨"(공정→압력). 우리 *제조압(300)으로 미세구조 fix → 저작동압 운용* 전략의 직접 근거.
2. **계면 품질의 실험 정량** — peel-off(freestanding 1회 vs co-rolled 10회 안 떨어짐) + 인장강도
   (co-rolled 0.510 = SSE 0.049 + 전극 0.441 N cm⁻¹ 의 *합*) + 사이클 후 계면 void-ratio
   (75→2 MPa 서 freestanding 4.0→15.5 vs co-rolled 1.9→3.5) → 우리 coverage(Hertz/Tabor)/Stage-E 의 *현상* 대응.
3. **공정 레버(P1–P3)** — CAM 입자(PC vs SC), co-rolling 온도(30 vs 120 ℃), reduction 두께(20 vs 100 µm)
   가 미세구조·균열·층 균일성을 어떻게 바꾸나 → 우리 시뮬 입력(12:4:1 packing, E_eff 연화의 바인더판,
   over-compression 캡)에 시사.

⚠ **단, 이 논문은 *순수 실험*(DEM/MPM/FEM/RNM 없음)** 이고, **정량 압밀 porosity·Heckel·coordination Z·
E_SE·σ_y 를 주지 않는다**(void 는 *사이클 후 계면 void 상대비*, ImageJ threshold). 우리 frame[4] 의
**외부 실험 앵커**로 쓰되 — 공정·압력·계면 *현상*은 가져오고, *모델 절반*(접촉망 σ 삼중항·MPM 변형장·
Heckel·정량 porosity)은 우리가 채운다. 절대 porosity 직접 비교 금지(§10).

---

## §1. 메타 + 레시피 (우리와 거의 동일)

| 항목 | 값 |
|---|---|
| 저자 | Dong Ju Lee 외 15인, 교신 **Zheng Chen** (UC San Diego) + **LG Energy Solution** |
| 저널/년 | Nat. Commun. **16**, 4200 (2025) |
| DOI | 10.1038/s41467-025-59363-4 (Open Access CC-BY) |
| 연구유형 | **실험** (건식 co-rolling 막 제조 + EIS/DCP 전달 + cell cycling + pouch); **시뮬레이션 없음** |
| SE | **Li₆PS₅Cl (LPSCl), <1 µm** (볼밀 TMAX-PBM 400 rpm 2 h ×2) |
| CAM | **PC-NCM** = poly NCM811 (LiNi₀.₈Co₀.₁Mn₀.₁O₂, 5–15 µm, LGES) / **SC-NCM** = single-crystal NCM82 (LiNi₀.₈₂Co₀.₁₁Mn₀.₀₇O₂, 3–5 µm) → **SC-NCM 최종 채택** |
| 도전제 | **VGCF** (>98 %) |
| 바인더 | **PTFE** (<300 nm, Chemours) |
| 음극(full cell) | **Si** (1–5 µm) + LPSCl + VGCF + **PVDF** (PTFE 환원 회피용) |

**핵심 레시피 (Supp Table 1 "This work" 열):**
- **양극** CAM:SSE:VGCF:PTFE = **80:17:3:0.5 wt%** · areal **5 mAh cm⁻²** · 두께 **120 µm** ·
  areal mass **31.4 mg cm⁻²**. (우리: 80:18:1:1 → 그들 **VGCF↑(3 vs 1)·PTFE↓(0.5 vs 1)**.)
- **SSE 층** LPSCl:PTFE = **100:0.1 wt%** · 두께 **50 µm** · areal mass **8.2 mg cm⁻²** ·
  SSE:Binder ratio = 100:0.1 (=문헌 중 **최소 바인더**, Fig 3c).
- **음극** Si:LPSCl:VGCF:PVDF, 두께 15 µm, areal 7 mAh cm⁻², **N/P 1.4**.
- **셀** nominal **3.35 V**, 총 두께 **205 µm**, 총 areal mass **53.2 mg cm⁻²**.

---

## §2. 건식 co-rolling 공정 (★ 핵심 — 우리 cold-press 와의 대조)

### 2.1 conventional dry-process vs co-rolling (Fig 1a,b,c)
- **conventional**: 두꺼운 SSE feed 를 일련의 roll-press 로 *점진적으로* 얇게 → **박막 freestanding SSE 막**.
  하지만 얇아질수록 **균열·찢김(crack & tear) 위험↑** (Fig 1c: SSE 두께↓ → 기계적 실패↑ 선형).
  박막 freestanding 막은 cutting/transfer/stacking(셀 조립)이 *어렵다*. 바인더를 늘리면 기계강도는
  올라가지만 **이온전도·전기화학 안정성이 희생**된다 → 박막 SSE 는 *기계강도 vs 가공성*의 병목.
- **co-rolling** (Fig 1b): **두꺼운 SSE feed + 양극 feed 를 *함께* roll-press**.
  - 박막 SSE(50 µm)를 **freestanding 형태로 만들 필요가 없음** → 균열·찢김 위험 우회.
  - co-rolling 중 **robust SSE-양극 계면이 *형성*** → 셀 조립시 기계적 실패 완화.
  - 결과: 박막 SSE + 고로딩·고AM비 양극 + robust 계면을 *한 번에* (Fig 1d "Practical ASSB").
- **Supp Fig 1**: conventional 박막 freestanding SSE = **심한 crack & tear**(사진); co-rolled 박막 =
  SSE 면·전극 면 둘 다 **crack-free**.

### 2.2 3단계 제조공정 (Methods + Fig 2a, S1–3)
1. **S1 — 양극 feed**: CAM + SSE + VGCF + PTFE 를 막자사발 30 min 혼합 → vial 에서 vortex(3000 rpm) →
   dough 형성 → roll-press(roller gap **2 mm 고정**) + **folding/rotating 30회 반복**(PTFE 섬유화,
   calendar loop) → 양극 feed 층.
2. **S2 — SSE feed**: 볼밀 LPSCl + PTFE(100:0.1) 동일 절차 → SSE feed 층.
3. **S3 — feed reduction**: 양극 feed 위에 SSE feed 를 올리고(areal weight ratio 양극:SSE = **3.5:1**,
   SSE feed 초기 두께 **600 µm**), 두 feed 를 **함께** roll-press 로 desired reduction thickness 까지
   점진 압연 → 박막 co-rolled film. (목표 두께 도달 후 양극 로딩 5 mAh cm⁻² 달성.)
- **제조 press(fabrication)**: co-rolled film 또는 freestanding 막을 셀 조립 전 **500 MPa, 3 min** 으로
  press(uniaxial) — 이게 **우리 300 MPa cold-press 에 대응하는 *제조압*** (단 그들 500 MPa).
- **pouch cell**: Al bag laminate → **CIP(cold isostatic press) 500 MPa, 10 min** → 작동 5 MPa.

### 2.3 3가지 공정 파라미터 (P1–P3, Fig 2a + Supp Fig 2,3,8,10)
| 파라미터 | 비교 | 결과 | 채택 | 우리 시뮬 시사 |
|---|---|---|---|---|
| **P1 CAM 입자** | large **PC-NCM**(5–15 µm) vs small **SC-NCM**(3–5 µm) | PC-NCM = 거친 표면 + 큰 CAM/작은 SE 사이 **큰 void**(Supp Fig 6) → press 시 **심한 균열·debris**(Fig 2b, SEM "Cracked CAM"); SC-NCM = press 전부터 dense·**intimate contact**(Supp Fig 7) → **무손상**(Fig 2c "Intact CAM"). 300→500 MPa 서 PC 균열↑ (Supp Fig 8). | **SC-NCM** | ★ 우리 **12:4:1 packing**(작은 SE 가 큰 CAM void 채움) + **AM_P 다결정 파괴/AM_S rigid** 가정의 실험 대응 |
| **P2 co-rolling 온도** | 30 ℃ vs 120 ℃ | 30 ℃ = **비균일 층**(Fig 2d, 단면 SSE/전극 경계 흐림) + SSE 면 spots(Supp Fig 2c); 120 ℃ = **균일 층**(Fig 2e). PTFE storage modulus 가 30→120 ℃ 서 **67% 감소**(Supp Fig 10, ≈150→50 MPa) → 온도↑ → 바인더 연화 → feed 더 쉽게 변형 → 균일 압연 | **120 ℃** | ★ "온도↑→바인더 연화→압밀 균일" = 우리 **E_eff 18× 연화의 *바인더 측* 물리** (Bouvard2000 σ_y(T) 와 같은 결) |
| **P3 reduction 두께** | step 당 20 µm vs 100 µm | 100 µm = 큰 변형 → **전극이 SSE 로 침투**(Fig 2f "Electrode layer penetration", over-deformation) + 100 µm SSE 면 wrinkles(Supp Fig 2d); 20 µm = **distinct SSE-cathode 층**(Fig 2g) — feed 에 가해지는 응력↓ | **20 µm** | ★ **over-compression(과변형)** = 우리 ε_sphere 음수/접촉면적 over-report 를 캡하는 것과 같은 맥락(적정 step 필요) |

→ 최종 production 막 = **SC-NCM / 120 ℃ / 20 µm reduction / line speed 4 m min⁻¹**.

### 2.4 계면 형성 메커니즘 — shear-induced PTFE fibrillation (Fig 2j, 3j, Supp Fig 18)
- co-rolling 과 freestanding 의 *공정적* 차이 = **계면에 가해지는 shear**.
- **freestanding**(shear 無, dual-layer 적층): 계면 접착 = 양 막 표면의 바인더에만 의존, 접촉 = 적층시
  층-대-층 → **heterogeneous(부분 접착) 계면** (Fig 3f, Supp Fig 16a "Gap").
- **co-rolling**(과도한 shear): reduction step 마다 입자·바인더의 복잡한 역학 → (i) **바인더 섬유화가
  계면을 *가로질러* 일어남** + (ii) 계면에서 **intimate 입자-대-입자 접촉** 형성 → press 후 **fused 계면**.
- **Supp Fig 18a 5단계 모식**: (i) 계면 초기 접촉 3종(SSE binder↔양극 binder / SSE 입자↔양극 binder /
  SSE binder↔VGCF) → (ii) shear 로 입자 이동 + 바인더 응력 → (iii) 바인더 **stretched & fibrillated
  across interface** → (iv) 새 접촉 형성 → (v) 두께감소 step 마다 반복. (Supp Fig 18b,c: 초기 단계
  "binder contacts at interface" → 최종 단계 "binder fibrillation across interface".)

---

## §3. 저작동압(2 MPa) robust 계면 — ★★ 본 digest 의 핵심 발견

### 3.1 작동 stack pressure 의 의미 (Fig 4a, §reduced operation pressure)
- 통상 lab ASSB 는 **높은 stack pressure(>50 MPa)** 로 입자-대-입자 접촉을 보장하며 측정한다.
- 하지만 실용에는 **낮은 작동압**이 필수 — 활물질 부피변화(delithiation 수축)가 **접촉 손실 → void →
  분극↑ → 용량↓** 를 일으키는데, 높은 stack pressure 가 이를 막아주는 것이므로 *압력을 못 낮춘다*.
- 본 논문 전략: **공정(co-rolling)으로 robust 계면을 *미리* 만들면** 낮은 작동압에서도 접촉 유지 →
  **작동압을 낮출 수 있다**.

### 3.2 핵심 cycling 데이터 (Fig 5a,b + Supp Fig 22,24)
> ⚠ 모두 **실험 측정 (stated)**. LiIn‖LPSCl‖NCM(NCM82 SC) half-cell, 60 ℃, 5 mAh cm⁻², LTO 부재 시.

| 조건 | co-rolled | freestanding | 비고 |
|---|---|---|---|
| **75 MPa, 1 C, 500 cyc** | **>95 % 유지** (areal 3.55→) | <95 % | 고압에선 둘 다 양호 (Fig 5a) |
| **2 MPa, 0.5 C, 500 cyc** | **>80 % 유지** (areal 3.65→3.06 mAh cm⁻²) | **<80 %**(3.06→2.5 추정) | ★ **저압 격차**: co-rolled 가 freestanding 보다 명확히 우월 (Fig 5b) |
| voltage profile loss @2 MPa | **8.5 %** (Fig 5c) | **13.2 %** (Fig 5d) | 저압서 분극 손실 차 |
| 첫 사이클 방전 @2 MPa | **177 mAh g⁻¹** | 141 mAh g⁻¹ | co-rolled 가 +36 mAh g⁻¹ (저압) |
| 첫 사이클 방전 @75 MPa | ~191 mAh g⁻¹ | ~191 mAh g⁻¹ | 고압선 거의 동일 |
| Coulombic eff. (전 조건) | **>99.9 %** (500 cyc) | >99.9 % | Supp Fig 26 |

→ **핵심**: 고압(75 MPa)에선 co/free 차이 작지만, **저압(2 MPa)에서 co-rolled 가 확연히 우월** —
즉 co-rolling 의 robust 계면이 *저작동압에서 진가*를 발휘한다.

### 3.3 *왜* 저압에서 co-rolled 가 우월한가 — void-vs-pressure 정량 (Fig 5e,f + Supp Fig 28,29)
- 사이클 후 단면 SEM → ImageJ void segmentation → **양극/계면(10 µm 고정)/SSE** 3영역 void-ratio
  (SSE 영역 대비 *상대*비, 5개 region 평균).
- **계면(interface) void-ratio** (SSE 대비, Fig 5f / 본문 page 7):
  | 압력 | co-rolled | freestanding |
  |---|---|---|
  | 75 MPa | 1.9 | 4.0 |
  | 2 MPa | 3.5 | **15.5** |
  → 75→2 MPa 로 낮추면 co-rolled 는 **1.9→3.5 (약간↑)** 인데 freestanding 은 **4.0→15.5 (급증)**.
- **양극(electrode) void-ratio** (75→2 MPa): co-rolled **4.4→4.8**, freestanding **7.9→15.7**.
- **메커니즘 결론**: freestanding 의 *부분 접착(heterogeneous)* 계면은 저압에서 활물질 부피변화에
  **계면 void(균열)** 가 심하게 생김 → 분극↑ → 용량↓. co-rolled 의 *융합(fused)* 계면은 저압에서도
  void 형성에 **덜 취약** → 저압 cyclability 우월. (Supp Fig 29: co-rolled "maintained contact",
  freestanding "severe interfacial voids and cracks".)
- **In-situ DRT**(Fig 4i + Supp Fig 23): stack pressure 를 75→2 MPa 로 낮추면 **SSE-양극 저항**이 증가
  하는데, co-rolled 는 **freestanding 보다 적게 증가** → 같은 결론(저압서 접촉 더 유지).

### 3.4 작동압을 제대로 측정하기 위한 셀 설계 (★ Supp Fig 25 — 우리 압력 구분에 직접 시사)
저압 cycling 을 정직하게 측정하려면 두 가지 setup 이 필요:
- **fixed gap (Δd≈0, 고정 간격)**: plunger 위치 고정 → 사이클 중 압력이 *변함*. 75 MPa 시작 →
  20 사이클 후 **ΔP ≈ −1.5 MPa** drop (활물질 수축으로 압력 빠짐, Supp Fig 25d).
- **constant pressure (ΔP≈0, 스프링)**: 스프링이 압력을 *유지* → 사이클 중 ΔP 거의 없음.
  2 MPa constant pressure → **ΔP ≈ −0.1 MPa** (Supp Fig 25f). (75 MPa 는 스프링 한계로 fixed gap.)
- **LTO 음극** 사용(zero-strain, ΔV≈0)으로 *양극* 압력효과를 *음극과 분리* — 양극 SSE-계면 구조만 평가.
- → **2 MPa 장기 cycling 은 constant-pressure setup** 사용. (이 압력-유지 vs 압력-변동 구분은 우리
  MPM 의 **servo[const-stress] vs hold[displacement-stop]** protocol 선택과 *정확히 같은 물리* — §7.)

---

## §4. 미세구조 / 계면 특성 (SEM/EDS/XCT/XRD/XPS)

### 4.1 박막 SSE 층 + 친밀 계면 (Fig 2h,i,j + Supp Fig 12)
- **SSE 층 두께 50 µm** (균일, Fig 2e). 양극 **120 µm**. 셀 총 205 µm.
- Fig 2h: co-rolled 막의 **SSE 면 = LPSCl dense 표면** + EDS(S/Cl).
- Fig 2i: **양극 면 = SC-NCM 이 LPSCl 로 친밀하게 덮임** + EDS(S/Ni).
- Fig 2j: **micro-CT**(Zeiss Xradia) → 더 큰 스케일로 SSE+양극 층 구조 확인.
- Supp Fig 12: 단면 EDS(S/Cl on SSE side, Ni on electrode side) → **desired SSE-양극 interphase** 형성.
- Supp Fig 13/14: **XRD**(LPSCl + NCM811 상 유지, 부반응 무) / **XPS**(S 2p PS₄³⁻, Cl 2p Cl⁻, Ni 2p
  유지) → co-rolling 이 화학 분해 없이 물리적 계면만 형성.

### 4.2 계면 접착 — peel-off + 인장 + fibril 망 (Fig 3)
- **flexibility**(Fig 3a): co-rolled 막은 bending/twisting/folding 가능 (Supp Fig 15: fold→unfold→
  push→recover, 균열 없이 회복).
- **인장강도**(Fig 3b, n=5): SSE **0.049** / 전극 **0.441** / co-rolled **0.510 N cm⁻¹**.
  → co-rolled ≈ **두 막의 *합*** → 둘 다 하중 분담 (우리 AM-shielding 의 결과 같음: 강한 쪽이 하중 받음).
- **바인더-두께 trade-off**(Fig 3c): 다른 dry-process 문헌(Ref 35/46/47/48/49/50)은 SSE 두께↑일수록
  바인더 wt%↑인데, **본 논문은 바인더 <0.1 wt% 로 *최소*면서 박막 50 µm 달성** → fibrillated network
  reinforcement 덕.
- **peel-off**(Fig 3d,g): freestanding = **1회 trial 에 완전 분리**(Fig 3d, Supp Movie 1) vs co-rolled =
  **10회 trial 해도 안 떨어짐**(Fig 3g, Supp Movie 2) → robust 접착.
- **side-view SEM**(Fig 3e,h): freestanding = SSE-전극 사이 **큰 gap + 부분 접착**(Fig 3e, Supp Fig 16a) vs
  co-rolled = **entirely attached + binder-VGCF network**(Fig 3h, Supp Fig 17).
- **모식**(Fig 3f,i): freestanding = limited adhesion(점선 부분접착) vs co-rolled = **꼬불꼬불 binder-VGCF
  network 가 계면을 그물침**(improved adhesion). ★ 이 fibril 망 SEM/모식 = **우리 PTFE CBD curl +
  nucleate-on-carbon 모델의 실험 검증** (papers/ digest §5,8 + `docs/cbd_morphology_roadmap.md`).
- **shear→fibril+contact**(Fig 3j,k,l): shear 가 (i) 바인더 fibrillation (ii) 접촉 형성 →
  freestanding(pressed) = heterogeneous 계면, co-rolled(pressed) = fused 계면.

---

## §5. 전기화학 — 전달(EIS/DCP) + 전지 (Context + 전달 앵커)

### 5.1 Li⁺/e⁻ 전달 (Fig 4b–f + Supp Fig 5,19,20 + Supp Table 2,3)
> 모두 실험 측정. σ = l/(R·A), R 은 EIS(Li⁺) 또는 DCP(e⁻). co-rolled vs freestanding 은 *조성 동일*,
> **두께만 다름**(co SSE 50 µm vs free 500 µm — free 는 막 품질 위해 의도적 두껍게).

| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **σ_ionic (SSE 층, intrinsic)** | **1.04 (co) / 1.29 (free) mS/cm** | LPSCl:PTFE 100:0.1 | ★ co<free 는 *압밀 차 아님* — **측정 형상차**(free 500 µm). conductance 는 **164 (co) / 20 (free) mS** (co 가 박막 덕 높음). intrinsic σ 비교 주의 |
| σ_e (SSE 층) | **1.4×10⁻⁷ / 2.6×10⁻⁷ mS/cm** | co / free | SSE 전자절연 ✓ (전자누설 적음, shelf-life 양호) |
| **σ_ionic (양극)** | **0.076 (co) / 0.069 (free) mS/cm** | 0.5 wt% PTFE, 80:17:3 | 거의 동일(조성 set) → SSE 가 양극에 잘 분산 |
| **σ_e (양극, VGCF망)** | **33 (co) / 34 (free) mS/cm** | 0.5 wt% PTFE | VGCF 전자망 잘 형성 (co/free 무관) |
| **★ PTFE wt% 페널티** | σ_ionic **0.069 / 0.024 / 0.007** · σ_e **34 / 4.5 / 0.011 mS/cm** | PTFE **0.5 / 2 / 5 wt%** (80:17:3 고정) | ★★ **바인더↑ → σ 양쪽 다 급감**(σ_e 3,000×). Supp Fig 5. → 우리 Stage-2 흡수 1순위 |
| bulk LPSCl σ | pristine **2.19** / ball-mill **1.64 mS/cm** (σ_e 5e-4 / 3.3e-4) | pellet | Supp Fig 4. 세 번째 LPSCl bulk 앵커 |

### 5.2 셀 성능 (context — 전달 앵커 아님)
- **내부저항**(Fig 4g, Supp Fig 21): co-rolled 가 분극 기울기 *낮음*(−1.24 vs −1.97 방전 / 1.48 vs 2.18 충전)
  — 박막 SSE 의 짧은 이온경로.
- **shelf-life**(Fig 4h): 4.0 V 충전상태 100 h rest 후 전압 유지 co≈free → 전자누설(SSE 통한) 유사.
- **rate**(Supp Fig 31, full cell Si): 0.1–0.5 C, 5 mAh cm⁻², 0.5 C 까지 short 없이 작동.
- **pouch cell**(Fig 6 + Supp Fig 32,33 + Supp Note 1): Si‖LPSCl‖NCM82, **stack-level 310 Wh kg⁻¹ /
  805 Wh L⁻¹** (5 mAh cm⁻², 30 ℃, **5 MPa**, 0.05 C), CAM-level 660 Wh kg⁻¹. 30 cyc 데모.
  Supp Table 1 비교: 본 논문 = 타 dry-process 문헌 대비 최고 specific energy/energy density(Fig 6f).

---

## §6. Figure / SI 전수 설명 (★ 우리 참고점 위주)

### 본문 figure
| Fig | 내용 | 우리 참고점 |
|---|---|---|
| **1a–c** | conventional(점진박막→crack) vs co-rolling 모식 + SSE두께↔균열위험 선형 | 박막 SSE 제조 맥락 (우리 RVE 는 *막 제조* 단계 안 다룸) |
| **1d** | "Practical ASSB" 셀 설계(고용량 음극+박막 SSE+robust 계면+고AM비 양극+저stack압) | **저작동압 + robust 계면**의 그림 |
| **2a** | P1–P3 공정 모식 | CAM 크기·온도·두께 레버 |
| **2b,c** | ★ PC-NCM "Cracked CAM"(debris) / SC-NCM "Intact CAM" (press 후) | ★ 우리 DEM AM_P 파괴·AM_S rigid 의 실험 증거 |
| **2d,e** | 30 ℃ 비균일 / 120 ℃ 균일 층 (단면) | 바인더 연화 = E_eff 연화의 바인더판 |
| **2f,g** | 100 µm 전극침투(과변형) / 20 µm distinct 층 | over-compression 캡 맥락 |
| **2h,i** | SSE 면(S/Cl)·양극 면(S/Ni) EDS — 친밀 coverage | press 가 SSE 접촉망 형성(우리 접촉망 대응) |
| **2j** | micro-CT 막 재구성 | XCT 대형 스케일 검증 |
| **3a** | bending/twisting/folding flexibility | 박막 robust |
| **3b** | 인장 SSE 0.049/전극 0.441/co-rolled 0.510 N cm⁻¹ | co-rolled ≈ 합 → 하중분담 (AM-shielding 결) |
| **3c** | 바인더 wt% vs SSE 두께 (본 논문 = 최소 바인더 박막) | fibril 망이 강도 보강 → 바인더 줄여도 됨 |
| **3d,g** | peel-off freestanding 1회/co-rolled 10회 안 떨어짐 | 계면 접착 정량 (coverage 현상) |
| **3e,f,h,i** | ★ side-view SEM + 모식: free=gap/부분접착 vs co=binder-VGCF fibril 망/융합 | ★★ 우리 CBD curl+carbon-nucleation 모델 검증 |
| **3j,k,l** | shear→fibrillation+contact → free=heterogeneous / co=fused 계면 | shear→fibril 시드 가정 |
| **4a** | Li⁺/e⁻ 전달 경로 + (내부저항/shelf-life/stack압) 모식 | 전달-셀물성 연결 |
| **4b** | co(50µm SSE)/free(500µm SSE) 형상 | 측정 형상차 명시 |
| **4c,d** | SSE 층 Li⁺(1.04/1.29) / e⁻(절연) EIS·DCP | SSE σ 앵커 + 두께-conductance 구분 |
| **4e,f** | 양극 Li⁺(0.076/0.069) / e⁻(33/34, VGCF) | 전달 절대 앵커(조성별·co/free) |
| **4g** | 내부저항 분극 기울기(co 낮음) | 박막 짧은 이온경로 |
| **4h** | shelf-life 100 h (전자누설 co≈free) | SSE 전자절연 |
| **4i** | ★ stack pressure DRT γ(τ): 2 vs 75 MPa, co vs free | ★ 저압서 SSE-양극 저항 증가, co 가 덜 |
| **5a** | ★ 75 MPa 1C 500 cyc: co/free 둘 다 >95 % | 고압 양호 |
| **5b** | ★★ 2 MPa 0.5C 500 cyc: co **>80 %** / free <80 % | ★★ 저작동압 robust 계면 핵심 |
| **5c,d** | voltage profile loss: co 8.5 % / free 13.2 % (@2 MPa) | 저압 분극 손실 차 |
| **5e** | 사이클 후 단면 SEM(co/free × 75/2 MPa) + void map | 계면 void 시각화 |
| **5f** | ★ void-ratio 막대(5 region): 양극/계면 × 4조건 | ★ void-vs-P 정량 (계면 free 4.0→15.5 vs co 1.9→3.5) |
| **6a–f** | high-energy Si full-cell + pouch (310 Wh/kg, 805 Wh/L) + 문헌비교 | 실용 데모 (우리 범위 밖) |

### SI figure (핵심만)
| SI Fig | 내용 | 참고점 |
|---|---|---|
| **1** | conventional 박막 freestanding = crack&tear / co-rolled = crack-free (사진) | 공정 우위 시각 |
| **2** | P1–P3 후 SSE/전극 면 사진 (PC/SC × 30/120 ℃ × 20/100 µm) | uniform vs spots/wrinkles |
| **3** | PC-NCM(5–15 µm) vs SC-NCM(3–5 µm) 입자 SEM | PSD 입력 |
| **4** | pristine vs ball-mill LPSCl: σ_ion 2.19→1.64, σ_e 5e-4→3.3e-4 | bulk LPSCl σ 앵커 |
| **★ 5** | ★★ PTFE 0.5/2/5 wt% → σ_ion 0.069/0.024/0.007 · σ_e 34/4.5/0.011 | ★★★ 우리 Stage-2 바인더 페널티 |
| **6** | PC-NCM 표면 as-fab(Void)→pressed(Microvoids)→BSE(Cracked debris) | AM_P 파괴 정성 |
| **7** | SC-NCM Smooth→Intimate contacts→Intact particles | AM_S 무손상 |
| **8** | PC/SC @300 vs 500 MPa: PC 500서 균열↑, SC 균열無·접촉↑ | 압력↑→PC 더 깨짐 |
| **★ 10** | ★ PTFE storage modulus 30→120 ℃ 서 **67%↓** (≈150→50 MPa) | 바인더 연화 정량 = E_eff 연화 바인더판 |
| **11** | line speed 4 m min⁻¹ (타 문헌은 "not reported") | high-throughput 잠재력 |
| **12** | 단면 EDS(S/Cl/Ni) interphase | 계면 화학 |
| **13,14** | XRD(LPSCl+NCM811 유지)/XPS(PS₄³⁻,Cl⁻,Ni 유지) | 부반응 무 |
| **15** | fold/unfold/push/recover (균열 없이 회복) | 기계 회복성 |
| **16** | side-view: free=Gap / co=attached (tearing 후) | 계면 접착 |
| **★ 17** | ★ "Fibrillated network of binder-VGCF at interface"(SE/BSE) | ★★ CBD fibril 망 SEM |
| **★ 18** | ★ (a) fibrillation 5단계 모식 (b) 초기/최종 co-rolling 단면 | ★★ CBD 메커니즘 그림 |
| **19,20** | 전달 측정 셀 형상(Li⁺ EIS / e⁻ DCP) + 등가회로(SSE R1-CPE1 / 전극 R1-(R2‖CPE2)-(R3‖CPE3)-CPE4) | 측정법 |
| **21** | 내부저항 voltage curve (rate별 ΔV) | 분극 |
| **★ 22** | ★ stack pressure 2/5/10/25/75 MPa EIS + voltage profile (2 vs 75) | ★ 압력별 임피던스 |
| **23** | in-situ EIS+DRT, 2 MPa, 충/방전 SSE-양극 저항 진화 | 저압 저항 |
| **24** | CAM 60/70/80 wt% × 75/2 MPa 전기화학 (고AM서 저압 악화↑) | 고AM·저압 |
| **★ 25** | ★★ 셀 설계: fixed gap(ΔP≈−1.5) vs constant pressure(ΔP≈−0.1) + LTO 분리 | ★★ servo vs hold protocol 대응 |
| **26** | CE >99.9 % (4조건 500 cyc) | 부반응 무 |
| **27** | void 분석 영역 할당(양극/계면 10µm/SSE) | void 방법 |
| **28,29** | ★ void segmentation 75 / 2 MPa (co maintained vs free severe) | ★ void-vs-P 원본 이미지 |
| **30** | LTO‖LPSCl‖NCM 압력변화 20 cyc (co −2 vs free −3 MPa) | 압력 drop |
| **31** | Si full-cell rate (0.1–0.5 C) | full cell |
| **32,33** | pouch cell cycling + specific energy(310/805) | 실용 |
| **Table 1** | ★ dry-process SSE 문헌 비교 (Ref 35/46/47/48/49/50 vs This work) | ★ 레시피 출처 + 정합 |
| **Table 2,3** | EIS 등가회로 피팅 R/CPE (SSE: R1 6.1 vs 49.5 Ω; 전극) | 회로값(직접 물성 아님) |
| **Table 4** | 바인더 6종 co-rolling 호환성 (PTFE compatible / PVDF not) | 바인더 선택 |
| **Note 1** | specific energy 계산 (areal mass 8.2/31.4/2.0/2.7/8.96, 두께 50/120/15/10/10 µm) | stack 계산 |

---

## §7. ★ 비교 vs 우리 DEM+MPM (focused §)

> 기준: `our_dem_baseline.md`. 이 논문은 **순수 실험** → frame[4] *외부 실험 앵커*(경쟁 모델 아님).
> 공정·압력·계면 *현상*을 가져오고, *모델 절반*(접촉망 σ 삼중항·MPM 변형장·Heckel·정량 porosity)은 우리가 채운다.

### 7.1 제조(processing): co-rolling vs 우리 cold-press — 압밀 물리는 비교 가능한가?
- **같은 점**: 둘 다 **uniaxial pressure-densification**. 그들 제조 press = **500 MPa, 3 min** (pouch 는
  CIP 500 MPa) → 우리 **300 MPa cold-press** 와 *같은 종류*(냉간 가압 치밀화, Sakuda "상온 가압소결"
  물리). 압력↑ → 밀도↑ → 접촉 형성 (우리 DEM 압밀과 결 같음).
- **다른 점 ①**: co-rolling 은 **roll-press + shear**(전단) → 단순 uniaxial 보다 **계면 fibrillation**
  추가. 우리 DEM/MPM 은 **shear 없는 uniaxial RVE** → *막 제조 shear 공정은 재현 안 함*. 따라서
  fibrillation 은 **개념 검증**으로만(우리 시뮬이 그 shear 를 모사한다고 주장 금지).
- **다른 점 ②**: 그들은 **정량 압밀 porosity 를 주지 않는다**(void 는 *사이클 후 계면 void 상대비*만).
  → 우리 DEM 15.6 % / MPM 16.7 % @300 MPa, Minnmann 복합 13–17 %, Doux pure-SE 18 %@370, Sakuda
  >90 %@>350 와 **직접 비교 불가**. 그들 압밀 밀도 = **n/a**.
- **판정**: 압밀 *물리*(가압 치밀화·온도→바인더연화→압밀균일·과변형 캡)는 *추세*로 정합 →
  우리 DEM 압밀 + Bouvard2000 σ_y(T) + over-compression 캡과 같은 계보. *절대 porosity*는 그들이 없으니
  우리/Minnmann/Doux/Sakuda 쪽이 owns. (densification CSV 에 Lee 행은 *압력-구분 컨텍스트*로만 추가, porosity 칸 비움.)

### 7.2 작동압(operation pressure): 2 MPa robust 계면 → 우리 fab-vs-operating 그림에 합류 (★ 핵심)
- **우리 인식**: 미세구조는 **제조압 300 MPa**(Heckel P_y=138 MPa = *제조압* 무릎)로 fix, 셀은
  **작동 수~수십 MPa**에서 사이클. (Doux 5 MPa 최적·Minnmann 측정 40 MPa.)
- **Lee 가 추가하는 것**: **공정-인과**. Doux 가 "5 MPa 가 최적"(현상)이라면, Lee 는 **"계면을 잘 만들면
  2 MPa 까지 낮춰도 >80 % 유지"**(공정 → 작동압 하한). 즉 **계면 품질이 작동압 하한을 정한다**.
  - co-rolled(융합 계면) → 2 MPa 서 계면 void 1.9→3.5 (거의 안 늘음) → >80 % 유지.
  - freestanding(부분 계면) → 2 MPa 서 계면 void 4.0→**15.5** (급증) → <80 %.
  → **"고압-제작(500/300 MPa) + 저압-운용(2–5 MPa)"** 전략의 직접 실증. 우리 *제조압으로 미세구조
    만들고 저작동압 운용* 프레임의 **권위 있는 LPSCl 공정 근거** (Doux 의 *비가역 이력*[25→5 MPa release
    절반 유지]과 결합 → "한 번 잘 만든 계면/구조는 저압서 유지").
- **압력 4종 위치**: 제조(fab) Lee 500 / 우리 300 / Doux 370 / Minnmann 380 / Sakuda >350 ≈ "수백 MPa
  냉간가압" ‖ 작동(operating) Lee **2(half)/5(pouch)** / Doux **5** / Minnmann 측정 **40** / Cronau 5–50.
  → Lee 가 **작동압 하단(2 MPa)** 을 가장 낮게 못박음(계면 공정 덕).

### 7.3 계면/접촉 품질 → 우리 coverage(Hertz/Tabor)/Stage-E
- 그들 계면 품질 정량 = **peel-off(1 vs 10회)** + **인장(합)** + **사이클 후 계면 void-ratio**.
- 우리 대응 = **coverage**(AM-SE 접촉면적, Hertz=접촉·Tabor=소성스프레드) + **Stage-E**(소성 접촉면적).
  우리 real_14: Hertz coverage 16 % / Tabor 52 %, MPM scaffold coverage 49.6/48.2 % (DEM Tabor 와 일치).
- **현상 매핑(절대 매핑 아님)**: 그들 "co-rolled 가 계면 void 적음/잘 붙음" ↔ 우리 "coverage 높음/
  Stage-E 접촉면적 큼". 단 **그들은 *사이클 후 계면 void*(시간축), 우리는 *제조 직후 coverage*(정적)** →
  *추세·현상*으로만 대응(절대 수치 직접 비교 금지). 그들 void 는 ImageJ 상대비지 우리 접촉면적 아님.

### 7.4 셀 설계 압력-유지 vs 압력-변동 = 우리 MPM servo vs hold (★ 새 매핑)
- Supp Fig 25: **fixed gap**(Δd≈0, 압력 변동 ΔP≈−1.5) vs **constant pressure**(스프링, ΔP≈−0.1).
- 우리 MPM scaffold: **servo**(const-stress dwell ≈ 실제 press) vs **hold**(displacement-stop = LIGGGHTS
  변위정지+이완). → **Lee 의 constant-pressure ↔ 우리 servo**, **Lee 의 fixed-gap ↔ 우리 hold**.
  - 우리는 scaffold 에서 **servo 가 plastic SE 를 OVER-COMPACT**(const-σ ratchet) → **hold 채택**
    (porosity 15.93 % EMERGE). Lee 도 같은 이유로 **2 MPa 장기 cycling 은 *유지가 어렵다***
    (fixed gap 75 MPa 는 −1.5 MPa drop) → constant-pressure 가 필요.
  - → **압력-유지 vs 압력-변동의 물리적 구분**이 *실험 셀 설계*와 *우리 MPM protocol*에서 *같은 형태*로
    나타남 = frame[4] 적 교차(우리 servo/hold 선택의 실험 정당화).

### 7.5 비교표
| 항목 | Lee 2025 (실험) | 우리 (DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| 성격 | **실험 막** (no model) | DEM(전달)+MPM(역학) 시뮬 | frame[4] — 실험 앵커, 경쟁 모델 아님 |
| 소재 | **LPSCl + NCM811/82 + VGCF + PTFE** | **동일** | ★ 소재·도전제·바인더 모두 동일 |
| 제조 공정 | co-rolling(roll+shear) **500 MPa** press | uniaxial cold-press **300 MPa** RVE | shear→fibril 추가(우리 RVE 미모사); 가압치밀화 *추세* 정합 |
| 제조압 vs 작동압 | ★ **명시 분리** (제조 500 / 작동 **2–5 MPa**) | 제조 300(Heckel P_y 138) / 작동 수~수십 | ★ 우리 fab-vs-operating 구분의 *공정-인과* 근거 |
| 저작동압 | ★ **2 MPa 서 >80 % 500 cyc** (co-rolled) | (작동압 cycling 모사 안 함) | ★ "계면 품질이 작동압 하한 정함" — 우리에 *없던* 공정 인과 |
| 계면 품질 | peel-off 1 vs 10회, 인장 합, void 1.9→3.5 vs 4.0→15.5 | coverage Hertz 16/Tabor 52 %, Stage-E | 현상 대응(절대 매핑 금지 — 그들 *사이클후 void*) |
| 압력 protocol | fixed gap(ΔP−1.5) vs const-P(ΔP−0.1) | hold(변위정지) vs servo(const-σ) | ★ 같은 물리 — 우리 hold 채택 정당화 |
| 정량 porosity | **없음** (void 상대 segmentation만) | DEM 15.6 % / MPM 16.7 % @300 | **우리 강점**(정량 porosity·Heckel) |
| 전달 솔버 | 없음 (실험 EIS/DCP) | Kirchhoff/Holm + Stage-E + 삼중항 | **우리 강점**(명시적 접촉망·삼중항) |
| σ 절대 앵커 | σ_ion 양극 0.076, σ_e 33–34, PTFE% 페널티 | σ_ionic LOOCV 0.975, σ_e 0.953 | ★ 외부 절대 검증점(함량 보정 후) |
| morphology/변형장 | SEM 정성(PC 깨짐, fibril 망) | MPM 진짜 소성 형상변화·void-fill·Σdg | **우리 강점**(MPM 정량 변형장) |
| AM 파괴 | ★ PC-NCM 깨짐 / SC-NCM 무손상 | DEM AM_P 파괴 37–40 %, Auerbach | ★ 실험 검증(AM_P 다결정·AM_S rigid) |

---

## §8. 적용 인사이트 (★ 내 연구에 어떻게)

1. **★ 제조-vs-작동압 그림의 *공정-인과* 완성 (Doux/Minnmann 와 합류, 압력 4종)**:
   Lee = "공정(co-rolling)으로 robust 계면 → **작동압 2 MPa 까지 낮춰도 >80 %**". Doux = "5 MPa 가 최적"(현상),
   Minnmann = "측정 40 MPa / 압밀 380 MPa". → 우리 **"300 MPa 제조(Heckel P_y 138) ≠ 수~수십 MPa 작동"**
   인식에 **"계면 품질이 작동압 하한을 정한다"** 는 *인과*를 추가. **deck 한 문장**: 고압-제작+저압-운용은
   LPSCl 실험(Lee 2 MPa·Doux 5 MPa·Doux 비가역 이력)으로 정당화된 전략이다.

2. **★ 작동압 cycling 의 계면 void-vs-pressure = 우리 transport 가 *못 다루는* 시간축**:
   freestanding 계면 void 4.0→15.5(75→2 MPa) vs co-rolled 1.9→3.5. → 우리 모델은 *제조 직후* 정적
   미세구조만 다룸 → **사이클 후 계면 void 진화**는 우리 frame[5] 분업의 *바깥*(향후: 작동압 sweep +
   부피변화 → void → σ↓ 모델). 지금은 **현상 앵커**로 기록(coverage 잘 된 구조가 저압서 void 적음).

3. **★ 셀 압력-protocol(fixed gap vs constant pressure) = 우리 MPM servo/hold 의 실험 정당화**:
   우리가 scaffold 에서 **servo→over-compact → hold 채택**한 것이, Lee 가 **fixed gap 75 MPa →ΔP−1.5 →
   2 MPa 는 constant-pressure 필요**로 본 것과 *같은 물리*. → "압력-유지 vs 압력-변동" 구분이 실험·
   시뮬 양쪽에서 같은 형태 = 우리 protocol 선택이 *literature-consistent*.

4. **공정 레버 → 우리 시뮬 입력**:
   - **P1(PC vs SC)** = 우리 **12:4:1 packing**(작은 SE 가 큰 CAM void 채움) + **AM_P 파괴/AM_S rigid**.
   - **P2(온도→바인더 67%↓)** = 우리 **E_eff 18× 연화의 바인더판**(온도↑→σ_y↓→압밀↑, Bouvard2000).
   - **P3(20 vs 100 µm, 과변형)** = 우리 **over-compression 캡**(과변형시 ε_sphere 음수/접촉면적 over-report 캡).

5. **σ 앵커 (papers/ digest 와 공유)**: PTFE wt% σ 페널티(0.5/2/5→σ_e 34/4.5/0.011) = Stage-2 흡수 1순위;
   양극 σ_ion 0.076·σ_e 33–34 = 외부 절대점; bulk LPSCl 2.19 = 세 번째 bulk 앵커. → `docs/data/lee2025_transport_anchors.csv`.

---

## §9. 인용 가능 문장 (deck/paper용)

- "An industrial dry-processed LPSCl/NCM811 cell fabricated by **co-rolling** (Lee et al., Nat. Commun.
  2025; the identical SE/CAM/VGCF/PTFE system we model) demonstrates **>80 % capacity retention over
  500 cycles at only 2 MPa operating stack pressure** — direct evidence that a robust, processing-formed
  SSE–cathode interface lowers the *operating* pressure floor, complementing the *fabrication* pressure
  (their 500 MPa press / our 300 MPa cold-press)."
- "Lee et al. separate fabrication from operation pressure at the process level: the cell is *pressed* at
  500 MPa but *cycled* at 2–5 MPa, and a co-rolled fused interface keeps interfacial void-ratio at 1.9→3.5
  (75→2 MPa) versus 4.0→**15.5** for a freestanding interface — the *cause* (interface quality) behind the
  Doux 5-MPa operating optimum."
- "The cell-design distinction between a fixed-gap (ΔP ≈ −1.5 MPa per cycle) and a constant-pressure
  (ΔP ≈ −0.1 MPa) setup in Lee et al. maps onto our MPM displacement-stop (*hold*) versus constant-stress
  (*servo*) protocols — independently justifying our choice of *hold* for the resolved-grain scaffold."

---

## §10. 주의 / 한계 (over-claim 방지)

- **시뮬레이션 0** — DEM/MPM/FEM/RNM 없음. **정량 압밀 porosity·Heckel·coordination Z·coverage %·E_SE·σ_y·
  접촉면적 전부 n/a**. void 분석은 **사이클 후 계면 void 의 상대비**(ImageJ threshold 하위 5 %)이지 *제조
  압밀 porosity 아님* → 우리 DEM 15.6 % / MPM 16.7 % 와 **직접 비교 금지**. densification CSV 의 Lee 행은
  *압력-구분 컨텍스트*(작동압 2/75 MPa retention)로만, **porosity 칸은 비움**.
- **제조압 다름**: 그들 **500 MPa** press (CIP 500) vs 우리 **300 MPa** cold-press → 압밀 *밀도 절대값*
  직접 동일시 금지 (압력 다름 + 그들 porosity 미제공). 가압-치밀화 *추세*만.
- **레시피 차**: 그들 양극 **VGCF 3 wt%·PTFE 0.5 wt%** vs 우리 1·1 → σ_e 절대값을 그대로 옮기지 말 것
  (VGCF↑→σ_e↑, PTFE↓→손실↓). σ 는 *추세·페널티 형태*로 흡수, 절대 매핑은 함량 보정 후.
- **σ_ionic(SSE) 1.04(co) < 1.29(free)**: co 가 *낮다* — **압밀이 나빠서가 아니라** free 가 500 µm 두꺼운
  SSE 라 측정 형상이 다름(논문 명시). conductance(164 vs 20 mS)는 두께차. **intrinsic σ 비교는 조심**.
- **막 제조 shear(co-rolling)** = 우리 RVE 가 *안 다루는* 공정 영역. fibrillation/계면형성은 *개념·현상
  검증*으로만 — 우리 시뮬이 그 roll-shear 공정을 재현한다고 주장 금지.
- **저압 cyclability·void·310 Wh/kg** = *실용 셀 성능* → 우리 *미세구조-transport 모델*의 절대 검증
  아님. 공정·압력·계면 *현상*을 가져오고 용량·에너지밀도 절대값은 context 로만.
- **bulk LPSCl σ 2.19**(pristine pellet)는 측정·입자·GB 조건이 Bazzoun 1.02·Cronau 3.0·Doux 2–2.5 와 달라
  — 절대 직접대조 말고 "여러 LPSCl bulk 앵커의 스프레드"로만.
- **frame[4]/[5]**: 이 논문은 *실험 절반*(공정·압력·계면·transport 실측 + morphology SEM); *모델 절반*
  (명시적 접촉망 σ 삼중항·MPM 정량 변형장·Auerbach·Heckel·정량 porosity)은 **우리가 추가**. 수렴=교차검증,
  공정/함량차로 인한 불일치=정량화된 효과(실패 아님).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
